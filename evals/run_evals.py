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

A malformed case is a harness ERROR, never a pass: a case with no
assertions, an unknown assertion type, an unknown `expect` value, an
`enum_legal` on a response that declares no settings, a `word_count` with no
bounds, an empty `names` list — each would otherwise "pass" having checked
nothing.

When an `enum_legal` verdict flips, the harness re-runs the same check
against the earlier committed specs snapshots (specs/models_explore_snapshot_
<date>.json) and says which one the case last held under: a flip the specs
caused is reported as a spec-driven flip (re-audit the case), not as a
checker regression.

Exit codes: 0 all pass, 1 any failure or harness error.
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

SPECS_DIR = ROOT / "specs"
SPECS_PATH = SPECS_DIR / "model-specs.json"
ENUM_RULES = {"ar-not-supported", "resolution-not-supported", "mode-not-supported",
              "duration-out-of-range", "mode-constraint", "constraint-requires",
              "extension-mode-missing", "extension-mode-not-allowed",
              # platform legality through scripts/preflight.py
              "platform-rule", "media-role-not-supported"}
VERDICT_ORDER = {"PASS": 0, "WARN": 1, "FAIL": 2}
VALID_EXPECT = ("legal", "illegal")
_SNAPSHOT_RE = re.compile(r"models_explore_snapshot_(\d{4}-\d{2}-\d{2})\.json")


class HarnessError(Exception):
    """The case or assertion is malformed — it could only pass vacuously."""


def _spec_index() -> dict:
    index = sl.load_specs(SPECS_PATH)
    if not index:
        raise SystemExit(f"specs missing/invalid: {SPECS_PATH} — run python3 scripts/sync_specs.py")
    return index


def _settings(case: dict, response: str) -> "sl.Settings":
    return sl.parse_settings_header(response)


def _require(params: dict, key: str, kind: str):
    if key not in params:
        raise HarnessError(f"{kind} assertion is missing its '{key}' field")
    return params[key]


def _resolve(specs: dict, model: str):
    try:
        return sl.resolve_model(specs, model)
    except sl.AmbiguousModelError as e:
        raise HarnessError(f"case model {e}") from e


def assert_lint_verdict(case, response, params, specs) -> list[str]:
    max_allowed = params.get("max", "WARN")
    if max_allowed not in VERDICT_ORDER:
        raise HarnessError(f"lint_verdict max {max_allowed!r} is not one of "
                           f"{', '.join(VERDICT_ORDER)}")
    spec = _resolve(specs, case["model"]) if case.get("model") else None
    findings = sl.lint(response) + sl.structural_lint(
        response, _settings(case, response), spec)
    fails = [f for f in findings if f.severity == "FAIL"]
    warns = [f for f in findings if f.severity == "WARN"]
    verdict = "FAIL" if fails else ("WARN" if warns else "PASS")
    if VERDICT_ORDER[verdict] > VERDICT_ORDER[max_allowed]:
        detail = "; ".join(f"{f.rule}({f.hit})" for f in (fails or warns)[:4])
        return [f"lint verdict {verdict} exceeds allowed {max_allowed}: {detail}"]
    return []


def assert_regex_present(case, response, params, specs) -> list[str]:
    pattern = _require(params, "pattern", "regex_present")
    if re.search(pattern, response, re.MULTILINE):
        return []
    return [f"pattern not found: {pattern!r}"]


def assert_regex_absent(case, response, params, specs) -> list[str]:
    pattern = _require(params, "pattern", "regex_absent")
    m = re.search(pattern, response, re.MULTILINE)
    return [f"forbidden pattern present: {m.group(0)!r}"] if m else []


def assert_sections_present(case, response, params, specs) -> list[str]:
    names = _require(params, "names", "sections_present")
    if not names:
        raise HarnessError("sections_present with an empty 'names' list checks nothing")
    return [f"missing section/label: {name!r}"
            for name in names if name not in response]


def _illegal_findings(response: str, spec: dict) -> list:
    findings = sl.structural_lint(response, sl.parse_settings_header(response), spec)
    return [f for f in findings if f.severity == "FAIL" and f.rule in ENUM_RULES]


_PRIOR_CACHE: list | None = None


def _prior_indexes() -> list[tuple[str, dict]]:
    """(snapshot date, spec index) for every committed video snapshot OLDER
    than the one specs/model-specs.json was generated from, newest first.
    Built with sync_specs (read-only) — no git history needed, so it works on
    a shallow CI checkout. A snapshot the current generator can't read is
    skipped."""
    global _PRIOR_CACHE
    if _PRIOR_CACHE is not None:
        return _PRIOR_CACHE
    out: list[tuple[str, dict]] = []
    try:
        import sync_specs
        current = json.loads(SPECS_PATH.read_text(encoding="utf-8")).get("snapshot_file", "")
        cur = _SNAPSHOT_RE.fullmatch(current)
        dated = sorted((m.group(1), p) for p in SPECS_DIR.glob("models_explore_snapshot_*.json")
                       if (m := _SNAPSHOT_RE.fullmatch(p.name)))
        for stamp, path in reversed(dated):
            if cur and stamp >= cur.group(1):
                continue
            try:
                out.append((stamp, sl.index_spec(sync_specs.build_spec(path))))
            except Exception:  # noqa: BLE001 — an unreadable old snapshot is skipped
                continue
    except Exception:  # noqa: BLE001 — attribution is advisory; never crash a run
        out = []
    _PRIOR_CACHE = out
    return out


def _current_snapshot(specs: dict) -> str:
    return specs.get("_snapshot_date") or "current"


def _flip_origin(model: str, response: str, expect: str) -> str | None:
    """Newest earlier snapshot under which this case's expectation HELD —
    i.e. the snapshot it was last green against. None = it held under none."""
    for stamp, index in _prior_indexes():
        try:
            spec = sl.resolve_model(index, model)
        except sl.AmbiguousModelError:
            continue
        if spec is None:
            continue
        if bool(_illegal_findings(response, spec)) == (expect == "illegal"):
            return stamp
    return None


def assert_enum_legal(case, response, params, specs) -> list[str]:
    expect = params.get("expect", "legal")
    if expect not in VALID_EXPECT:
        raise HarnessError(f"enum_legal expect {expect!r} is not one of "
                           f"{', '.join(VALID_EXPECT)}")
    model = case.get("model")
    if not model:
        raise HarnessError("enum_legal requires a case-level 'model'")
    if not _settings(case, response).declared():
        raise HarnessError("enum_legal found no declared settings in the response "
                           "(mode / aspect ratio / resolution / duration / media) — "
                           "it would pass having checked nothing")
    spec = _resolve(specs, model)
    if spec is None:
        return [f"model {model!r} not found in specs/model-specs.json — "
                "golden cites a model the snapshot no longer carries (stale!)"]
    illegal = _illegal_findings(response, spec)
    detail = "; ".join(f"{f.rule}({f.hit})" for f in illegal)
    now = _current_snapshot(specs)
    if expect == "legal" and illegal:
        origin = _flip_origin(model, response, expect)
        if origin:
            return [f"spec-driven flip — this golden was legal against specs "
                    f"snapshot {origin}; snapshot {now} makes it illegal for "
                    f"{spec['id']}: {detail}. The platform changed since the case "
                    f"was last green — re-audit the golden (Tier-2 rule: audit "
                    f"evals/cases/ in the same PR as a spec refresh)."]
        return [f"illegal settings for {spec['id']}: {detail}"]
    if expect == "illegal" and not illegal:
        origin = _flip_origin(model, response, expect)
        if origin:
            return [f"spec-driven flip — this trap held against specs snapshot "
                    f"{origin} but snapshot {now} makes these settings legal for "
                    f"{spec['id']}. The platform changed since the case was last "
                    f"green, not the checker — re-audit the trap (Tier-2 rule: "
                    f"audit evals/cases/ in the same PR as a spec refresh)."]
        return [f"trap case expected the checker to flag illegal settings for "
                f"{spec['id']}, but none were flagged — checker regression (the "
                f"trap holds against no committed specs snapshot either)"]
    return []


def assert_antislop_absent(case, response, params, specs) -> list[str]:
    hits = [m.group(0) for pat in sl.ANTISLOP
            for m in re.finditer(pat, response, re.IGNORECASE)]
    hits += [t for t in sl.ANTISLOP_ZH if t in response]
    return [f"antislop terms present: {', '.join(sorted(set(hits)))}"] if hits else []


def assert_preset_names_valid(case, response, params, specs) -> list[str]:
    names = _require(params, "names", "preset_names_valid")
    if not names:
        raise HarnessError("preset_names_valid with an empty 'names' list checks nothing")
    source = ROOT / params.get("source", "photodump-presets.md")
    if not source.exists():
        return [f"preset source missing: {source.name}"]
    text = source.read_text(encoding="utf-8")
    return [f"preset {name!r} not found in {source.name} — invented?"
            for name in names if name not in text]


def assert_word_count(case, response, params, specs) -> list[str]:
    """Word-band assertion (HARD RULE 8 finally gets a real check).

    params: 'max' and/or 'min' (at least one — a band with no bounds is a
    harness error). Counts words the same way seedance_lint does, so the two
    layers can never disagree on the number."""
    if "max" not in params and "min" not in params:
        raise HarnessError("word_count needs 'max' and/or 'min' — with neither "
                           "it passes every response")
    n = len(re.findall(r"\b\w+\b", response.strip()))
    failures = []
    if "max" in params and n > params["max"]:
        failures.append(f"word count {n} exceeds max {params['max']}")
    if "min" in params and n < params["min"]:
        failures.append(f"word count {n} below min {params['min']}")
    return failures


ASSERTIONS = {
    "lint_verdict": assert_lint_verdict,
    "word_count": assert_word_count,
    "regex_present": assert_regex_present,
    "regex_absent": assert_regex_absent,
    "sections_present": assert_sections_present,
    "enum_legal": assert_enum_legal,
    "antislop_absent": assert_antislop_absent,
    "preset_names_valid": assert_preset_names_valid,
}


ERROR_PREFIX = "harness ERROR: "


def run_case(case: dict, specs: dict) -> list[str]:
    """Failure strings for one case; harness errors carry ERROR_PREFIX."""
    response = case.get("response")
    if response is None and case.get("response_file"):
        response = (CASES_DIR / case["response_file"]).read_text(encoding="utf-8")
    if response is None:
        return [ERROR_PREFIX + "case has neither 'response' nor 'response_file'"]
    assertions = case.get("assertions") or []
    if not assertions:
        return [ERROR_PREFIX + "case has no assertions — it would pass having "
                "checked nothing"]
    failures = []
    for assertion in assertions:
        kind = assertion.get("type")
        fn = ASSERTIONS.get(kind)
        if fn is None:
            failures.append(ERROR_PREFIX + f"unknown assertion type: {kind!r}")
            continue
        try:
            failures.extend(fn(case, response, assertion, specs))
        except HarnessError as e:
            failures.append(ERROR_PREFIX + f"{kind}: {e}")
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

    total = failed = errored = 0
    for path in case_files:
        doc = json.loads(path.read_text(encoding="utf-8"))
        for case in doc.get("cases", []):
            if args.case and case["id"] != args.case:
                continue
            total += 1
            failures = run_case(case, specs)
            is_error = any(f.startswith(ERROR_PREFIX) for f in failures)
            mark = "✗" if failures else "✓"
            print(f"  {mark} [{doc.get('skill', path.stem)}] {case['id']}"
                  + ("  (harness ERROR)" if is_error else ""))
            for f in failures:
                print(f"      - {f}")
            if is_error:
                errored += 1
            elif failures:
                failed += 1

    passed = total - failed - errored
    tail = ", ".join(x for x in (f"{failed} FAILED" if failed else "",
                                 f"{errored} harness ERROR(S)" if errored else "") if x)
    print(f"\n{passed}/{total} eval cases passed" + (f" — {tail}" if tail else ""))
    return 1 if failed or errored or total == 0 else 0


if __name__ == "__main__":
    sys.exit(main())
