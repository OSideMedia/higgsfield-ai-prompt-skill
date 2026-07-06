#!/usr/bin/env python3
"""
evals/run_evals.py
==================
Golden-case eval harness for the skill library. Stdlib only.

Each case in evals/cases/*.json pairs a representative user request with a
golden response and a list of assertable properties (routing line present,
MCSLA layers present, settings legal per the specs layer, no antislop terms,
no invented preset names). The harness asserts our documented exemplars stay
correct as skills and specs evolve — when a model's enum changes in the
snapshot, every golden that cites the old value fails here instead of
shipping. Deliberate stale-spec traps assert the checker itself catches
illegal combinations (expect="illegal").

Usage:
  python3 evals/run_evals.py            # run all cases
  python3 evals/run_evals.py --case ID  # run one
  python3 scripts/validate.py --evals   # same, via the health check

Exit codes: 0 all pass, 1 any failure.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES_DIR = Path(__file__).parent / "cases"

sys.path.insert(0, str(ROOT / "scripts"))
import seedance_lint as sl  # noqa: E402 — flat module in scripts/

SPECS_PATH = ROOT / "specs" / "model-specs.json"
ENUM_RULES = {"ar-not-supported", "resolution-not-supported", "mode-not-supported",
              "duration-out-of-range", "mode-constraint", "constraint-requires"}
VERDICT_ORDER = {"PASS": 0, "WARN": 1, "FAIL": 2}


def _spec_index() -> dict:
    index = sl.load_specs(SPECS_PATH)
    if not index:
        raise SystemExit(f"specs missing/invalid: {SPECS_PATH} — run python3 scripts/sync_specs.py")
    return index


def _settings(case: dict, response: str) -> "sl.Settings":
    return sl.parse_settings_header(response)


def assert_lint_verdict(case, response, params, specs) -> list[str]:
    spec = sl.resolve_model(specs, case["model"]) if case.get("model") else None
    findings = sl.lint(response) + sl.structural_lint(
        response, _settings(case, response), spec)
    fails = [f for f in findings if f.severity == "FAIL"]
    warns = [f for f in findings if f.severity == "WARN"]
    verdict = "FAIL" if fails else ("WARN" if warns else "PASS")
    max_allowed = params.get("max", "WARN")
    if VERDICT_ORDER[verdict] > VERDICT_ORDER[max_allowed]:
        detail = "; ".join(f"{f.rule}({f.hit})" for f in (fails or warns)[:4])
        return [f"lint verdict {verdict} exceeds allowed {max_allowed}: {detail}"]
    return []


def assert_regex_present(case, response, params, specs) -> list[str]:
    if re.search(params["pattern"], response, re.MULTILINE):
        return []
    return [f"pattern not found: {params['pattern']!r}"]


def assert_regex_absent(case, response, params, specs) -> list[str]:
    m = re.search(params["pattern"], response, re.MULTILINE)
    return [f"forbidden pattern present: {m.group(0)!r}"] if m else []


def assert_sections_present(case, response, params, specs) -> list[str]:
    return [f"missing section/label: {name!r}"
            for name in params["names"] if name not in response]


def assert_enum_legal(case, response, params, specs) -> list[str]:
    expect = params.get("expect", "legal")
    model = case.get("model")
    if not model:
        return ["enum_legal requires a case-level 'model'"]
    spec = sl.resolve_model(specs, model)
    if spec is None:
        return [f"model {model!r} not found in specs/model-specs.json — "
                "golden cites a model the snapshot no longer carries (stale!)"]
    findings = sl.structural_lint(response, _settings(case, response), spec)
    illegal = [f for f in findings
               if f.severity == "FAIL" and f.rule in ENUM_RULES]
    if expect == "legal" and illegal:
        return [f"illegal settings for {spec['id']}: "
                + "; ".join(f"{f.rule}({f.hit})" for f in illegal)]
    if expect == "illegal" and not illegal:
        return [f"trap case expected the checker to flag illegal settings for "
                f"{spec['id']}, but none were flagged — checker regression"]
    return []


def assert_antislop_absent(case, response, params, specs) -> list[str]:
    hits = [m.group(0) for pat in sl.ANTISLOP
            for m in re.finditer(pat, response, re.IGNORECASE)]
    hits += [t for t in sl.ANTISLOP_ZH if t in response]
    return [f"antislop terms present: {', '.join(sorted(set(hits)))}"] if hits else []


def assert_preset_names_valid(case, response, params, specs) -> list[str]:
    source = ROOT / params.get("source", "photodump-presets.md")
    if not source.exists():
        return [f"preset source missing: {source.name}"]
    text = source.read_text(encoding="utf-8")
    return [f"preset {name!r} not found in {source.name} — invented?"
            for name in params["names"] if name not in text]


ASSERTIONS = {
    "lint_verdict": assert_lint_verdict,
    "regex_present": assert_regex_present,
    "regex_absent": assert_regex_absent,
    "sections_present": assert_sections_present,
    "enum_legal": assert_enum_legal,
    "antislop_absent": assert_antislop_absent,
    "preset_names_valid": assert_preset_names_valid,
}


def run_case(case: dict, specs: dict) -> list[str]:
    response = case.get("response")
    if response is None and case.get("response_file"):
        response = (CASES_DIR / case["response_file"]).read_text(encoding="utf-8")
    if response is None:
        return ["case has neither 'response' nor 'response_file'"]
    failures = []
    for assertion in case.get("assertions", []):
        kind = assertion.get("type")
        fn = ASSERTIONS.get(kind)
        if fn is None:
            failures.append(f"unknown assertion type: {kind!r}")
            continue
        try:
            failures.extend(fn(case, response, assertion, specs))
        except Exception as e:  # noqa: BLE001 — one bad assertion ≠ dead harness
            failures.append(f"{kind} crashed: {type(e).__name__}: {e}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[2])
    parser.add_argument("--case", help="run only the case with this id")
    args = parser.parse_args()

    specs = _spec_index()
    case_files = sorted(CASES_DIR.glob("*.json"))
    if not case_files:
        print(f"no case files in {CASES_DIR}", file=sys.stderr)
        return 1

    total = failed = 0
    for path in case_files:
        doc = json.loads(path.read_text(encoding="utf-8"))
        for case in doc.get("cases", []):
            if args.case and case["id"] != args.case:
                continue
            total += 1
            failures = run_case(case, specs)
            mark = "✗" if failures else "✓"
            print(f"  {mark} [{doc.get('skill', path.stem)}] {case['id']}")
            for f in failures:
                print(f"      - {f}")
            failed += bool(failures)

    print(f"\n{total - failed}/{total} eval cases passed"
          + (f" — {failed} FAILED" if failed else ""))
    return 1 if failed or total == 0 else 0


if __name__ == "__main__":
    sys.exit(main())
