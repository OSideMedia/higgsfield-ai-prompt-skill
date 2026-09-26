#!/usr/bin/env python3
"""
claims_lint.py
==============
Doctrine-vs-specs claim linter. The gate that would have caught the ~25 stale
"Seedance 2.5 caps at 720p / has no start_image role" lines after the
2026-09-26 spec refresh made them false.

A hand-maintained registry (evals/spec-claims.json — NOT under specs/, which
is generated) lists machine-checkable claim PATTERNS. Each entry binds a
regex to an assertion about the CURRENT specs:

  {
    "id": "s25-caps-at-720p",
    "finding": "<the audit finding the entry came from>",
    "pattern": "<Python regex; matched across the whole file, reported at
                the line where the match starts>",
    "paths":   ["optional fnmatch globs limiting where the pattern applies"],
    "heading": "optional regex the nearest preceding Markdown heading must
                match (binds a claim that doesn't name its model)",
    "assert":  {"kind": "...", "model": "<id>", "field": "...", "value": ...},
    "polarity": "asserts" | "denies"   (default asserts)
  }

Assertion kinds (all evaluated against specs/*.json):
  enum_max           the highest `field` value (resolution-ranked) == value
  has / lacks        value is / is not in `field` (resolutions, aspect_ratios,
                     modes, media_roles, params)
  model_present      the model id is in the catalog (optional "catalog":
                     video | image | audio)
  longest_duration   model's max duration == value AND no other video model
                     is longer
  listed_set_equals  the tokens the pattern captures in group `list` equal
                     the model's `field` set (order- and case-insensitive)

"asserts" = the matched text claims the assertion is true; "denies" = the
text claims it is false. A hit whose claim is false against today's specs is
a FAIL naming file:line. A model the assertion names that is no longer in
the specs FAILs too (the claim can't be verified — fail closed).

Scanned: every *.md in the tree EXCEPT specs/ (generated), docs/archive/ and
CHANGELOG.md (historical record — true when written), INDEX.md (generated
headings); plus evals/cases/*.json (golden responses).

Usage:
  python3 scripts/claims_lint.py                   # lint the repo
  python3 scripts/claims_lint.py --root DIR --specs-dir DIR
  python3 scripts/claims_lint.py --json            # machine-readable
  python3 scripts/claims_lint.py --verbose         # also list entries with no hits

Exit codes: 0 = no false claims, 1 = at least one false claim,
2 = registry / specs unreadable or malformed.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_DEFAULT = ROOT / "evals" / "spec-claims.json"
SPEC_FILES = {"video": "model-specs.json", "image": "image-model-specs.json",
              "audio": "audio-model-specs.json"}
KINDS = {"enum_max", "has", "lacks", "model_present", "longest_duration",
         "listed_set_equals"}
FIELDS = {"resolutions", "aspect_ratios", "modes", "media_roles", "params"}
PRUNE_DIRS = {".git", "workspace", "node_modules", "__pycache__", ".venv", "venv",
              ".pytest_cache"}
PRUNE_PATHS = {"specs", "docs/archive", ".claude/worktrees"}
SKIP_FILES = {"CHANGELOG.md", "INDEX.md"}
HEADING_RE = re.compile(r"^#{1,6}\s+(.*)$", re.M)


class RegistryError(ValueError):
    """The registry itself is malformed — the gate cannot run honestly."""


@dataclass
class Claim:
    id: str
    finding: str
    rx: re.Pattern
    assertion: dict
    polarity: str = "asserts"
    paths: tuple = ()
    heading: re.Pattern | None = None


@dataclass
class Hit:
    claim: Claim
    path: str
    line: int
    text: str
    ok: bool
    why: str


def load_registry(path: Path) -> list[Claim]:
    try:
        doc = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise RegistryError(f"cannot read registry {path}: {e}") from e
    claims, seen = [], set()
    for i, raw in enumerate(doc.get("claims") or []):
        where = f"registry entry #{i} ({raw.get('id', '?')})"
        for key in ("id", "finding", "pattern", "assert"):
            if not raw.get(key):
                raise RegistryError(f"{where}: missing '{key}' — every entry must "
                                    "name its pattern, assertion and source finding")
        if raw["id"] in seen:
            raise RegistryError(f"{where}: duplicate id")
        seen.add(raw["id"])
        a = raw["assert"]
        if a.get("kind") not in KINDS:
            raise RegistryError(f"{where}: unknown assert kind {a.get('kind')!r}")
        if not a.get("model"):
            raise RegistryError(f"{where}: assert needs a 'model'")
        if a["kind"] in ("enum_max", "has", "lacks", "listed_set_equals") \
                and a.get("field") not in FIELDS:
            raise RegistryError(f"{where}: field must be one of {sorted(FIELDS)}")
        if a["kind"] in ("enum_max", "has", "lacks", "longest_duration") \
                and "value" not in a:
            raise RegistryError(f"{where}: assert needs a 'value'")
        polarity = raw.get("polarity", "asserts")
        if polarity not in ("asserts", "denies"):
            raise RegistryError(f"{where}: polarity must be asserts|denies")
        try:
            rx = re.compile(raw["pattern"], re.M)
            heading = re.compile(raw["heading"]) if raw.get("heading") else None
        except re.error as e:
            raise RegistryError(f"{where}: bad regex: {e}") from e
        if a["kind"] == "listed_set_equals" and "list" not in rx.groupindex:
            raise RegistryError(f"{where}: listed_set_equals needs a (?P<list>…) group")
        claims.append(Claim(raw["id"], raw["finding"], rx, a, polarity,
                            tuple(raw.get("paths") or ()), heading))
    if not claims:
        raise RegistryError(f"registry {path} has no claims — the gate would be vacuous")
    return claims


def load_specs(specs_dir: Path) -> dict:
    """{"by_id": {id: model}, "by_type": {type: {id: model}}}."""
    by_id, by_type = {}, {}
    for otype, name in SPEC_FILES.items():
        p = Path(specs_dir) / name
        try:
            spec = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            raise RegistryError(f"cannot read specs {p}: {e}") from e
        by_type[otype] = {m["id"]: m for m in spec.get("models", [])}
        by_id.update(by_type[otype])
    return {"by_id": by_id, "by_type": by_type}


_RES_RE = re.compile(r"^(\d+(?:\.\d+)?)\s*([pk])?$", re.I)


def res_rank(value: str) -> float:
    """480p → 480, 1080p → 1080, 2k → 1440, 4k → 2160; unknown → -1."""
    m = _RES_RE.match(str(value).strip())
    if not m:
        return -1
    n, unit = float(m.group(1)), (m.group(2) or "").lower()
    if unit == "k":
        return {1: 1024, 1.5: 1080, 2: 1440, 4: 2160, 8: 4320}.get(n, n * 540)
    return n


def field_values(model: dict, field: str) -> list:
    if field == "media_roles":
        return [r for roles in (model.get("media_roles") or {}).values() for r in roles]
    if field == "params":
        return [p.get("name") for p in model.get("params", [])]
    return list(model.get(field) or [])


def _norm(v) -> str:
    return str(v).strip().lower()


def _max_duration(model: dict):
    d = model.get("duration") or {}
    if "max" in d:
        return d["max"]
    if d.get("values"):
        return max(d["values"])
    return None


def evaluate(assertion: dict, specs: dict, match: re.Match | None = None) -> tuple[bool | None, str]:
    """(truth of the assertion against specs, explanation). None = the
    assertion can't be evaluated (model gone) — callers fail closed."""
    kind, mid = assertion["kind"], assertion["model"]
    if kind == "model_present":
        pool = specs["by_type"].get(assertion.get("catalog"), specs["by_id"]) \
            if assertion.get("catalog") else specs["by_id"]
        present = mid in pool
        return present, (f"{mid} is in the {assertion.get('catalog') or 'specs'} catalog"
                         if present else
                         f"{mid} is not in the {assertion.get('catalog') or 'specs'} catalog")
    model = specs["by_id"].get(mid)
    if model is None:
        return None, f"{mid} is no longer in specs/ — the claim cannot be verified"
    if kind == "longest_duration":
        mine = _max_duration(model)
        others = [(m["id"], _max_duration(m)) for m in specs["by_type"].get("video", {}).values()
                  if m["id"] != mid and _max_duration(m) is not None]
        longer = [(i, d) for i, d in others if mine is None or d > mine]
        ok = mine == assertion["value"] and not longer
        top = max(others, key=lambda x: x[1]) if others else None
        return ok, (f"{mid} max duration {mine}s"
                    + (f"; longer: {', '.join(f'{i} {d}s' for i, d in sorted(longer, key=lambda x: -x[1])[:4])}"
                       if longer else f"; nothing longer (next: {top[0]} {top[1]}s)" if top else ""))
    field = assertion.get("field")
    values = field_values(model, field)
    if kind == "enum_max":
        if not values:
            return None, f"{mid} has no {field} in specs"
        top = max(values, key=res_rank)
        return _norm(top) == _norm(assertion["value"]), \
            f"{mid} {field} = {', '.join(map(str, values))} (max {top})"
    if kind in ("has", "lacks"):
        present = _norm(assertion["value"]) in {_norm(v) for v in values}
        ok = present if kind == "has" else not present
        return ok, f"{mid} {field} = {', '.join(map(str, values)) or '(none)'}"
    if kind == "listed_set_equals":
        listed = {t for t in re.split(r"[\s,/·|]+", match.group("list") if match else "")
                  if t}
        want = {_norm(v) for v in values}
        got = {_norm(t) for t in listed}
        return got == want, (f"text lists {', '.join(sorted(got))}; {mid} {field} = "
                             f"{', '.join(map(str, values))}")
    raise RegistryError(f"unhandled kind {kind}")  # pragma: no cover


def iter_doctrine(root: Path):
    """(relative posix path, text) for every scanned file under root."""
    root = Path(root)
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = Path(dirpath).relative_to(root).as_posix()
        rel_dir = "" if rel_dir == "." else rel_dir
        dirnames[:] = sorted(d for d in dirnames if d not in PRUNE_DIRS and
                             (f"{rel_dir}/{d}" if rel_dir else d) not in PRUNE_PATHS)
        for name in sorted(filenames):
            rel = f"{rel_dir}/{name}" if rel_dir else name
            if name.endswith(".md"):
                if rel in SKIP_FILES:
                    continue
            elif not (rel.startswith("evals/cases/") and name.endswith(".json")):
                continue
            try:
                yield rel, (Path(dirpath) / name).read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue


def _nearest_heading(text: str, pos: int) -> str:
    last = ""
    for m in HEADING_RE.finditer(text, 0, pos):
        last = m.group(1)
    return last


def lint(root: Path, specs: dict, claims: list[Claim]) -> list[Hit]:
    hits: list[Hit] = []
    static = {c.id: evaluate(c.assertion, specs) for c in claims
              if c.assertion["kind"] != "listed_set_equals"}
    for rel, text in iter_doctrine(root):
        for c in claims:
            if c.paths and not any(fnmatch.fnmatch(rel, g) for g in c.paths):
                continue
            for m in c.rx.finditer(text):
                if c.heading and not c.heading.search(_nearest_heading(text, m.start())):
                    continue
                truth, why = static.get(c.id) or evaluate(c.assertion, specs, m)
                if truth is None:
                    ok = False
                else:
                    ok = truth if c.polarity == "asserts" else not truth
                line = text.count("\n", 0, m.start()) + 1
                excerpt = " ".join(m.group(0).split())[:100]
                hits.append(Hit(c, rel, line, excerpt, ok, why))
    return hits


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Lint doctrine claims against the current specs.")
    ap.add_argument("--root", type=Path, default=ROOT, help="doctrine tree to scan")
    ap.add_argument("--specs-dir", type=Path, default=None,
                    help="specs directory (default: <repo>/specs)")
    ap.add_argument("--registry", type=Path, default=REGISTRY_DEFAULT)
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--verbose", action="store_true",
                    help="also list passing hits and entries with no hits")
    args = ap.parse_args(argv)

    try:
        claims = load_registry(args.registry)
        specs = load_specs(args.specs_dir or ROOT / "specs")
    except RegistryError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    hits = lint(args.root, specs, claims)
    bad = [h for h in hits if not h.ok]

    if args.json:
        print(json.dumps({
            "false_claims": [{"file": h.path, "line": h.line, "id": h.claim.id,
                              "text": h.text, "specs": h.why,
                              "finding": h.claim.finding} for h in bad],
            "checked_hits": len(hits),
            "entries_without_hits": sorted({c.id for c in claims} - {h.claim.id for h in hits}),
        }, indent=2, ensure_ascii=False))
    else:
        print(f"Claims lint — {len(claims)} registry entries, {len(hits)} hit(s), "
              f"{len(bad)} false against today's specs")
        for h in bad:
            print(f"  ✗ {h.path}:{h.line}  [{h.claim.id}] “{h.text}”")
            print(f"      specs: {h.why}")
            print(f"      finding: {h.claim.finding}")
        if args.verbose:
            for h in hits:
                if h.ok:
                    print(f"  ✓ {h.path}:{h.line}  [{h.claim.id}] {h.why}")
            for cid in sorted({c.id for c in claims} - {h.claim.id for h in hits}):
                print(f"  · [{cid}] no hits in this tree")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
