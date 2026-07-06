#!/usr/bin/env python3
"""
validate.py
===========
Pre-release health check for the Higgsfield AI Prompt Skill repo.

Checks:
  - All SKILL.md files exist and have required frontmatter fields
  - Relative path references inside SKILL.md files resolve to real files
  - JSON databases are valid and schema-complete
  - Entry counts match _total_entries declarations
  - Root SKILL.md version/updated agree with the README badge + footer

Usage (from the repo root):
  python3 scripts/validate.py            # standard run — optional-dep checks may SKIP
  python3 scripts/validate.py --strict   # release mode — SKIPs become failures
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # scripts/ → repo root
SPECS_DIR = ROOT / "specs"
SPECS_JSON = SPECS_DIR / "model-specs.json"
SNAPSHOT_MAX_AGE_DAYS = 30

# model-guide.md row names that don't normalize directly to a snapshot model
# name. Guide rows with NO mapping (legacy/deprecated/unsnapshotted models)
# are intentionally skipped — the specs layer is authoritative only for the
# models the snapshot actually contains.
GUIDE_NAME_OVERRIDES = {
    "veo31": "veo3_1",
    "veo3": "veo3",
    "grokimaginevideo": "grok_video",
    # Hailuo variants share one snapshot entry (variant = a `model` param)
    "minimaxhailuo23": "minimax_hailuo",
    "minimaxhailuo23fast": "minimax_hailuo",
    "minimaxhailuo02": "minimax_hailuo",
    "minimaxhailuo02fast": "minimax_hailuo",
}
DB_FILES = {
    "filter": ROOT / "db/filter-memory.json",
    "quality": ROOT / "db/quality-memory.json",
}
FILTER_REQUIRED_FIELDS = {"id", "category", "blocked_terms", "error_message",
                           "substitution", "fix_confirmed", "substitution_worked", "tags"}
QUALITY_REQUIRED_FIELDS = {"id", "failure_type", "model_used", "original_prompt",
                            "failure_description", "outcome", "fix_confirmed",
                            "improvement_confirmed", "tags"}
# Supported top-level SKILL.md frontmatter attributes (tags now lives inside metadata)
FRONTMATTER_REQUIRED = {"name", "description", "user-invocable"}
# Fields that must live nested under `metadata:` per the CLAUDE.md contract.
# `parent` is required on sub-skills only — the root dispatcher has no parent.
METADATA_REQUIRED = {"version", "updated"}
METADATA_REQUIRED_SUBSKILL = {"parent"}
# Canonical root-level reference docs. Bare backtick refs to these names (no
# path prefix) are validated to resolve at the repo root; other bare filenames
# are treated as prose citations and left unchecked (see check_relative_paths).
ROOT_REFERENCE_DOCS = {
    "vocab.md", "model-guide.md", "image-models.md", "prompt-examples.md",
    "photodump-presets.md", "production-benchmarks.md", "DISCIPLINE.md",
}
# Bare backticked filenames that are PROSE CITATIONS of files living outside
# this repo (source corpus, sibling team skills). They intentionally do not
# resolve here and must not be flagged. Keep this list short and reviewed —
# anything else that fails to resolve repo-wide gets a WARN.
EXTERNAL_CITATIONS = {
    "gpt-image-2-director.md", "seedance-2-pro-director.md",
    "shotlist-builder.md", "banana-pro-director.md",
    "cinema-worldbuilder.md", "screenwriter-skill.md",
    # Adil Aliyev source-corpus siblings cited as translation provenance
    # (note: `higgsfield-content-factory.md` cites the EXTERNAL source skill,
    # not this repo's skills/higgsfield-content-factory/SKILL.md):
    "marketing-studio-director.md", "higgsfield-content-factory.md",
    "cinematic-motion-language.md",
}

_repo_filename_index: set | None = None


def repo_filename_index() -> set:
    """Set of every *.md/*.py/*.json basename tracked in the repo tree.

    Lets the bare-ref checker accept a backticked filename that exists
    somewhere in the repo even when the prose doesn't path-qualify it
    (common for cross-skill mentions), while still flagging names that
    exist nowhere — the class of bug where an agent follows a reference
    and finds nothing."""
    global _repo_filename_index
    if _repo_filename_index is None:
        _repo_filename_index = {
            p.name for ext in ("md", "py", "json")
            for p in ROOT.rglob(f"*.{ext}")
            if ".git" not in p.parts and "__pycache__" not in p.parts
        }
    return _repo_filename_index

PASS = "\033[32m✓\033[0m"
FAIL = "\033[31m✗\033[0m"
WARN = "\033[33m⚠\033[0m"
SKIP = "\033[36m∅\033[0m"

issues = []
warnings = []
# Checks that could not run because an OPTIONAL dependency is missing (e.g. the
# PDF smoke test without fpdf2). A skip is not a failure on a contributor
# machine — the repo's content checks all still ran — but a release build must
# not ship with anything unverified, so --strict promotes skips to issues.
skips = []


def check(ok: bool, label: str, detail: str = "") -> bool:
    symbol = PASS if ok else FAIL
    suffix = f"  ({detail})" if detail else ""
    print(f"  {symbol} {label}{suffix}")
    if not ok:
        issues.append(f"{label}{suffix}")
    return ok


def warn(label: str, detail: str = ""):
    print(f"  {WARN} {label}" + (f"  ({detail})" if detail else ""))
    warnings.append(label)


def skip(label: str, detail: str = ""):
    print(f"  {SKIP} {label}" + (f"  ({detail})" if detail else "") + "  [SKIP]")
    skips.append(f"{label}" + (f"  ({detail})" if detail else ""))


def metadata_block(fm: str) -> str:
    """Return only the lines nested under the top-level `metadata:` key.

    Anchoring metadata lookups to this block (rather than searching the whole
    frontmatter) prevents a stray `version:`/`updated:` line elsewhere in the
    frontmatter from being mistaken for the canonical metadata value.
    """
    out, in_meta = [], False
    for line in fm.splitlines():
        if re.match(r"^metadata:\s*$", line):
            in_meta = True
            continue
        if in_meta:
            # A new top-level key (column-0, non-space) ends the metadata block.
            if line and not line[0].isspace():
                break
            out.append(line)
    return "\n".join(out)


def check_frontmatter(skill_file: Path):
    rel = skill_file.relative_to(ROOT)
    text = skill_file.read_text(encoding="utf-8")
    # Extract YAML frontmatter between --- delimiters
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        check(False, f"{rel}: missing frontmatter")
        return
    fm = match.group(1)
    for field in FRONTMATTER_REQUIRED:
        present = re.search(rf"^{field}:", fm, re.MULTILINE) is not None
        if not present:
            check(False, f"{rel}: missing frontmatter field '{field}'")
    # tags should be nested inside metadata, not at the top level
    if re.search(r"^tags:", fm, re.MULTILINE):
        check(False, f"{rel}: tags should be inside metadata, not at top level")
    # Enforce the metadata.* contract from CLAUDE.md.
    meta = metadata_block(fm)
    if re.search(r"^metadata:\s*$", fm, re.MULTILINE) is None:
        check(False, f"{rel}: missing 'metadata:' block")
        return
    is_root = skill_file.parent == ROOT
    required = METADATA_REQUIRED if is_root else METADATA_REQUIRED | METADATA_REQUIRED_SUBSKILL
    for field in sorted(required):
        if re.search(rf"^\s+{field}:", meta, re.MULTILINE) is None:
            check(False, f"{rel}: missing metadata.{field}")


def check_relative_paths(skill_file: Path):
    text = skill_file.read_text(encoding="utf-8")
    # 1. Path-style refs (require a `../` or `dir/` prefix) resolve relative to
    #    the referencing file's own directory.
    refs = re.findall(r'`((?:\.\.\/|[\w-]+\/)[\w./%-]+\.(?:md|py|json))`', text)
    for ref in sorted(set(refs)):
        target = (skill_file.parent / ref).resolve()
        exists = target.exists()
        label = f"{skill_file.relative_to(ROOT)}: ref '{ref}'"
        check(exists, label, "" if exists else f"resolves to {target} — not found")
    # 2. Bare refs (no path prefix). Known root reference docs must resolve at
    #    the repo root (FAIL otherwise). Every other bare filename must exist
    #    somewhere — referencing file's dir, repo root, or anywhere in the repo
    #    tree — or it gets a WARN: an agent following it from this file's
    #    directory would find nothing. Allowlisted external citations (files
    #    that live outside this repo by design) are exempt.
    bare = re.findall(r'`([\w-]+\.(?:md|py|json))`', text)
    rel = skill_file.relative_to(ROOT)
    for ref in sorted(set(bare)):
        if ref in ROOT_REFERENCE_DOCS:
            exists = (ROOT / ref).exists()
            check(exists, f"{rel}: root ref '{ref}'",
                  "" if exists else "named as a root reference doc but not found at repo root")
        elif ref in EXTERNAL_CITATIONS:
            continue
        elif not ((skill_file.parent / ref).exists() or (ROOT / ref).exists()
                  or ref in repo_filename_index()):
            warn(f"{rel}: bare ref '{ref}' resolves nowhere in the repo",
                 "path-qualify it, or add to EXTERNAL_CITATIONS if it cites an external file")


def check_template_paths():
    """Path-style refs inside templates/ must resolve (same rule as SKILL.md
    part 1 — templates link back to root reference docs, and a bad `../`
    prefix silently strands the reader; the v3.18 ad-asset-prep link rotted
    exactly this way). Bare refs are left to prose."""
    for md in sorted(ROOT.glob("templates/**/*.md")):
        text = md.read_text(encoding="utf-8")
        refs = re.findall(r'`((?:\.\.\/|[\w-]+\/)[\w./%-]+\.(?:md|py|json))`', text)
        for ref in sorted(set(refs)):
            target = (md.parent / ref).resolve()
            exists = target.exists()
            label = f"{md.relative_to(ROOT)}: ref '{ref}'"
            check(exists, label, "" if exists else f"resolves to {target} — not found")


def check_json_db(label: str, path: Path, required_fields: set):
    print(f"\n  Checking {label} database ({path.relative_to(ROOT)})...")
    if not check(path.exists(), f"{label}: file exists"):
        return

    try:
        with open(path, encoding="utf-8") as f:
            db = json.load(f)
    except json.JSONDecodeError as e:
        check(False, f"{label}: valid JSON", str(e))
        return

    check(True, f"{label}: valid JSON")

    entries = db.get("entries", [])
    if not isinstance(entries, list):
        check(False, f"{label}: 'entries' is a list", f"got {type(entries).__name__}")
        return
    declared = db.get("_total_entries", -1)
    check(len(entries) == declared,
          f"{label}: entry count matches _total_entries",
          f"declared={declared}, actual={len(entries)}")

    for entry in entries:
        if not isinstance(entry, dict):
            check(False, f"{label}: entry is a JSON object", repr(entry)[:60])
            continue
        eid = entry.get("id", "?")
        for field in required_fields:
            if field not in entry:
                check(False, f"{label} entry {eid}: missing field '{field}'")


def check_routing():
    """Routing telemetry log (item 6): schema + every skill in the canonical
    sub-skill roster. Reuses higgsfield_memory.validate_route_entry so the rule
    lives in one place."""
    path = ROOT / "db" / "routing-log.json"
    if not check(path.exists(), "routing-log: file exists"):
        return
    try:
        db = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        check(False, "routing-log: valid JSON", str(e))
        return
    entries = db.get("entries", [])
    if not check(isinstance(entries, list), "routing-log: 'entries' is a list"):
        return
    check(len(entries) == db.get("_total_entries", -1),
          "routing-log: entry count matches _total_entries",
          f"declared={db.get('_total_entries')}, actual={len(entries)}")
    import higgsfield_memory as hm
    problems = []
    for e in entries:
        problems.extend(hm.validate_route_entry(e))
    check(not problems, f"routing-log: {len(entries)} entry(ies) schema-valid",
          "; ".join(problems[:3]))


def check_version_consistency():
    """Cross-check the single-source version/date in root SKILL.md against the
    README badge, README footer, and the CHANGELOG.md top entry. Catches drift
    like a stale frontmatter `updated:` or a forgotten CHANGELOG header that the
    per-file frontmatter check can't see (it validates one file at a time)."""
    skill = ROOT / "SKILL.md"
    readme = ROOT / "README.md"
    changelog = ROOT / "CHANGELOG.md"
    # Evaluate all three existence checks (don't short-circuit) so each is reported.
    skill_ok = check(skill.exists(), "SKILL.md exists")
    readme_ok = check(readme.exists(), "README.md exists")
    changelog_ok = check(changelog.exists(), "CHANGELOG.md exists")
    if not (skill_ok and readme_ok and changelog_ok):
        return

    fm_match = re.match(r"^---\n(.*?)\n---", skill.read_text(encoding="utf-8"), re.DOTALL)
    if not fm_match:
        check(False, "SKILL.md frontmatter parses")
        return
    # Anchor version/updated to the nested `metadata:` block so an unrelated
    # `version:`/`updated:` line elsewhere in the frontmatter can't be read by
    # mistake (the values are the single source of truth for the whole repo).
    meta = metadata_block(fm_match.group(1))
    readme_text = readme.read_text(encoding="utf-8")
    changelog_text = changelog.read_text(encoding="utf-8")

    skill_version = re.search(r"^\s*version:\s*([0-9]+\.[0-9]+\.[0-9]+)", meta, re.MULTILINE)
    skill_updated = re.search(r"^\s*updated:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", meta, re.MULTILINE)
    # README badge: .../badge/version-3.8.1-blue
    badge_version = re.search(r"badge/version-([0-9]+\.[0-9]+\.[0-9]+)-", readme_text)
    # README footer: ... v3.8.1 (updated 2026-06-03) ...
    footer = re.search(r"v([0-9]+\.[0-9]+\.[0-9]+)\s*\(updated\s*([0-9]{4}-[0-9]{2}-[0-9]{2})\)", readme_text)
    # CHANGELOG top entry: first heading like "## v3.8.1 — 2026-06-03"
    changelog_top = re.search(r"^##\s*v([0-9]+\.[0-9]+\.[0-9]+)", changelog_text, re.MULTILINE)

    if not check(bool(skill_version), "SKILL.md frontmatter has a version"):
        return
    if not check(bool(skill_updated), "SKILL.md frontmatter has an updated date"):
        return
    if not check(bool(badge_version), "README has a version badge"):
        return
    if not check(bool(footer), "README footer has 'vX.Y.Z (updated YYYY-MM-DD)'"):
        return
    if not check(bool(changelog_top), "CHANGELOG.md has a top '## vX.Y.Z' entry"):
        return

    sv, su = skill_version.group(1), skill_updated.group(1)
    bv = badge_version.group(1)
    fv, fu = footer.group(1), footer.group(2)
    cv = changelog_top.group(1)

    check(sv == bv, "SKILL.md version matches README badge",
          "" if sv == bv else f"SKILL.md={sv}, badge={bv}")
    check(sv == fv, "SKILL.md version matches README footer",
          "" if sv == fv else f"SKILL.md={sv}, footer={fv}")
    check(su == fu, "SKILL.md updated date matches README footer",
          "" if su == fu else f"SKILL.md={su}, footer={fu}")
    check(sv == cv, "SKILL.md version matches CHANGELOG top entry",
          "" if sv == cv else f"SKILL.md={sv}, CHANGELOG={cv}")


def check_dispatcher_parity():
    """Reconcile the skills/ directory against the root SKILL.md dispatcher.

    Every buildable sub-skill on disk must be referenced from root SKILL.md
    (otherwise it is orphaned — unreachable from the dispatcher), and every
    higgsfield-* skill named in root SKILL.md must exist on disk (otherwise the
    route dangles). Catches the exact class of bug where a fully-built sub-skill
    ships without a routing row."""
    skills_dir = ROOT / "skills"
    if not check(skills_dir.exists(), "skills/ directory exists"):
        return
    disk_skills = sorted(
        d.name for d in skills_dir.iterdir()
        if d.is_dir() and d.name != "shared" and (d / "SKILL.md").exists()
    )
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    referenced = set(re.findall(r"higgsfield-[a-z0-9-]+", skill_text))

    for name in disk_skills:
        ok = name in referenced
        check(ok, f"dispatcher routes '{name}'",
              "" if ok else "built on disk but never referenced in root SKILL.md")
    for name in sorted(referenced):
        if name == "higgsfield":  # the skill-family root token, not a sub-skill
            continue
        ok = (skills_dir / name).is_dir()
        check(ok, f"dispatcher ref '{name}' exists on disk",
              "" if ok else "referenced in root SKILL.md but no matching skills/ dir")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Pre-release health check for the Higgsfield skill repo.")
    parser.add_argument("--strict", action="store_true",
                        help="Release mode: optional-dependency SKIPs become "
                             "failures (use for release builds / CI).")
    parser.add_argument("--evals", action="store_true",
                        help="Also run the golden-case eval harness "
                             "(evals/run_evals.py). Opt-in so corpus growth "
                             "doesn't slow the default health check.")
    return parser.parse_args()


def check_evals():
    """Run evals/run_evals.py as a subprocess (same isolation rationale as the
    PDF smoke: a crashing eval case must not take this report down)."""
    runner = ROOT / "evals" / "run_evals.py"
    if not check(runner.exists(), "evals/run_evals.py exists"):
        return
    try:
        result = subprocess.run([sys.executable, str(runner)],
                                capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        check(False, "eval harness", "timeout after 120s")
        return
    tail = (result.stdout or "").strip().splitlines()
    summary = tail[-1] if tail else "(no output)"
    if result.returncode == 0:
        check(True, "eval harness", summary)
    else:
        failing = [l.strip() for l in tail if l.strip().startswith("✗")]
        check(False, "eval harness",
              summary + ("; " + "; ".join(failing[:3]) if failing else ""))


def _norm_model_name(s: str) -> str:
    s = re.sub(r"\*\*", "", s)
    s = re.sub(r"\([^)]*\)", "", s)  # strip qualifiers like "(legacy)"
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def _parse_duration_cell(cell: str):
    """Parse a guide Duration cell into a comparable shape.

    Returns ("range", (lo, hi)) | ("values", [..]) | ("single", n) | None.
    Only these number patterns are ever read, so stars/emoji/notes in other
    columns can't produce false positives."""
    cell = cell.replace("**", "")
    m = re.search(r"(\d+)\s*[–\-]\s*(\d+)\s*s", cell)
    if m:
        return ("range", (int(m.group(1)), int(m.group(2))))
    m = re.search(r"(\d+(?:/\d+)+)\s*s", cell)
    if m:
        return ("values", sorted(int(v) for v in m.group(1).split("/")))
    m = re.search(r"(\d+)\s*s\b", cell)
    if m:
        return ("single", int(m.group(1)))
    return None


def check_guide_against_specs(guide_text: str, spec: dict) -> list:
    """Cross-check model-guide.md Duration cells against the specs layer.

    The Duration column documents the model's supported envelope, so a guide
    range must equal the spec envelope exactly and a single value passes only
    when the spec envelope IS that single value — "10s" against a 4–15s model
    is precisely the confidently-wrong number this layer exists to catch.
    Returns (ok, label, detail) tuples so it stays unit-testable."""
    name_index, seen, ambiguous = {}, {}, set()
    for m in spec.get("models", []):
        nm = _norm_model_name(m["name"])
        if nm in seen and seen[nm] != m["id"]:
            ambiguous.add(nm)  # e.g. two "Cinema Studio Video" entries
        seen[nm] = m["id"]
    name_index = {nm: mid for nm, mid in seen.items() if nm not in ambiguous}
    by_id = {m["id"]: m for m in spec.get("models", [])}

    results = []
    duration_idx = None
    for line in guide_text.splitlines():
        if not line.lstrip().startswith("|"):
            duration_idx = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if re.match(r"^\s*\|[\s|:\-–]+\|?\s*$", line):
            continue  # separator row
        if "Duration" in cells:
            duration_idx = cells.index("Duration")
            continue
        if duration_idx is None or len(cells) <= duration_idx:
            continue
        nm = _norm_model_name(cells[0])
        mid = GUIDE_NAME_OVERRIDES.get(nm) or name_index.get(nm)
        model = by_id.get(mid)
        if model is None or model.get("duration") is None:
            continue
        parsed = _parse_duration_cell(cells[duration_idx])
        if parsed is None:
            continue  # "—" / prose cell — nothing checkable
        d = model["duration"]
        spec_env = ((d["min"], d["max"]) if "min" in d
                    else (min(d["values"]), max(d["values"])))
        kind, val = parsed
        if kind == "range":
            ok = val == spec_env
        elif kind == "values":
            ok = ("values" in d and val == d["values"]) or (
                "min" in d and (val[0], val[-1]) == spec_env)
        else:  # single value claims the whole envelope
            ok = spec_env == (val, val) or d.get("values") == [val]
        spec_fmt = (f"{d['min']}–{d['max']}s" if "min" in d
                    else "/".join(map(str, d["values"])) + "s")
        results.append((
            ok,
            f"model-guide.md: '{cells[0].replace('**', '')}' duration matches specs ({mid})",
            "" if ok else f"guide says {cells[duration_idx]!r}, snapshot says {spec_fmt}",
        ))
    return results


def check_model_specs():
    """The specs layer: present, fresh, regenerable, and not contradicted."""
    if not check(SPECS_JSON.exists(), "specs/model-specs.json exists",
                 "" if SPECS_JSON.exists() else "run: python3 scripts/sync_specs.py"):
        return
    try:
        spec = json.loads(SPECS_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        check(False, "specs/model-specs.json is valid JSON", str(e))
        return
    check(True, "specs/model-specs.json is valid JSON")

    # Snapshot age — stale specs are how confidently-wrong numbers come back.
    try:
        age = (date.today() - date.fromisoformat(spec["snapshot_date"])).days
    except (KeyError, ValueError) as e:
        check(False, "specs snapshot_date parses", str(e))
        return
    if age > SNAPSHOT_MAX_AGE_DAYS:
        warn(f"specs snapshot is {age} days old (>{SNAPSHOT_MAX_AGE_DAYS})",
             "re-dump models_explore into specs/ and rerun sync_specs.py")
    else:
        check(True, f"specs snapshot fresh ({spec['snapshot_date']}, {age}d old)")

    # Generated files must match a regeneration from the committed snapshot —
    # catches hand-edits of generated files AND snapshot/generator changes.
    try:
        import sync_specs
        snapshot_path = SPECS_DIR / spec["snapshot_file"]
        rebuilt = sync_specs.build_spec(snapshot_path)
        regen = {
            sync_specs.YAML_OUT: sync_specs.emit_yaml(rebuilt),
            sync_specs.JSON_OUT: sync_specs.emit_json(rebuilt),
            sync_specs.MD_OUT: sync_specs.emit_markdown(rebuilt),
        }
        stale = [p.name for p, content in regen.items()
                 if not p.exists() or p.read_text(encoding="utf-8") != content]
        check(not stale, "specs files match regeneration from snapshot",
              "" if not stale else f"stale: {', '.join(stale)} — rerun python3 scripts/sync_specs.py")
    except Exception as e:  # noqa: BLE001 — report, don't crash the validator
        check(False, "specs regeneration check", f"{type(e).__name__}: {e}")
        return

    # model-guide.md numbers must not contradict the snapshot.
    guide = ROOT / "model-guide.md"
    if guide.exists():
        for ok, label, detail in check_guide_against_specs(
                guide.read_text(encoding="utf-8"), spec):
            check(ok, label, detail)

    # Image side (Brief #2 item 9): WARN while the type=image snapshot TODO
    # stands; once specs/image-model-specs.json exists this flips to a real
    # freshness check mirroring the video side.
    image_specs = SPECS_DIR / "image-model-specs.json"
    image_snapshots = list(SPECS_DIR.glob("models_explore_snapshot_image_*.json"))
    if image_specs.exists() or image_snapshots:
        check(image_specs.exists() and bool(image_snapshots),
              "image specs generated from an image snapshot",
              "run: python3 scripts/sync_specs.py --type image")
    else:
        warn("image-model specs are TODO (no type=image snapshot yet)",
             "image-models.md / photodump-presets.md stay hand-maintained; "
             "dump models_explore type=image into specs/ when ready")
    for name in ("image-models.md", "photodump-presets.md"):
        path = ROOT / name
        if path.exists():
            stamped = "Specs snapshot:" in path.read_text(encoding="utf-8")
            check(stamped, f"{name} carries a specs-snapshot stamp",
                  "" if stamped else "add the snapshot/TODO header line")

    # README specs-snapshot badge must show the snapshot date.
    readme = ROOT / "README.md"
    if readme.exists():
        m = re.search(r"specs%20snapshot-(\d{4})--(\d{2})--(\d{2})",
                      readme.read_text(encoding="utf-8"))
        badge_date = "-".join(m.groups()) if m else None
        check(badge_date == spec["snapshot_date"],
              "README specs-snapshot badge matches snapshot date",
              "" if badge_date == spec["snapshot_date"]
              else f"badge={badge_date}, snapshot={spec['snapshot_date']}")


def check_description_coverage():
    """Every skills/<dir>/ has a SUB_SKILL_DESCRIPTIONS entry and vice versa.

    generate_user_guide.py enforces the same parity, but only where fpdf2 is
    installed — which is exactly where new-sub-skill PRs usually aren't built.
    This stdlib copy of the gate runs everywhere."""
    try:
        from sub_skill_descriptions import SUB_SKILL_DESCRIPTIONS
    except ImportError as e:
        check(False, "sub_skill_descriptions.py imports", str(e))
        return
    skills_dir = ROOT / "skills"
    on_disk = {d.name for d in skills_dir.iterdir()
               if d.is_dir() and d.name != "shared" and (d / "SKILL.md").exists()}
    described = set(SUB_SKILL_DESCRIPTIONS)
    missing = sorted(on_disk - described)
    orphans = sorted(described - on_disk)
    check(not missing, "every sub-skill has a description entry",
          "" if not missing else f"add to sub_skill_descriptions.py: {', '.join(missing)}")
    check(not orphans, "no orphan description entries",
          "" if not orphans else f"no skills/ dir for: {', '.join(orphans)}")


def check_index_and_quick_facts():
    """INDEX.md must match regeneration; QUICK FACTS contract must hold.

    build_index.py is the single authority for both checks — this wrapper
    just maps its findings into the validation report."""
    try:
        import build_index
    except ImportError as e:
        check(False, "build_index.py imports", str(e))
        return
    problems = build_index.run_checks()
    index_path = ROOT / "INDEX.md"
    if not index_path.exists() or index_path.read_text(encoding="utf-8") != build_index.build_index_text():
        problems.append("INDEX.md stale — rerun: python3 scripts/build_index.py")
    check(not problems, "INDEX.md current + QUICK FACTS anchors resolve",
          "" if not problems else "; ".join(problems[:3])
          + (f" (+{len(problems) - 3} more)" if len(problems) > 3 else ""))


def check_memory_summary():
    """Keep db/memory-summary.md in step with the memory databases.

    The summary was generated once (2026-03-08) and silently went stale as
    entries accumulated. Compare a fresh render (timestamp line excluded)
    against the file; regenerate automatically on drift so the human-readable
    view can never lag the databases again."""
    summary_path = ROOT / "db" / "memory-summary.md"

    def body(text: str) -> str:
        return "\n".join(l for l in text.splitlines()
                         if not l.startswith("Generated:"))

    try:
        import higgsfield_memory as hm
        fresh = hm.build_summary()
    except SystemExit:
        check(False, "memory summary renders", "memory databases missing/corrupt")
        return
    except Exception as e:  # noqa: BLE001
        check(False, "memory summary renders", f"{type(e).__name__}: {e}")
        return

    if summary_path.exists() and body(summary_path.read_text(encoding="utf-8")) == body(fresh):
        check(True, "db/memory-summary.md is current")
        return

    warn("db/memory-summary.md was stale — regenerated",
         "review and commit the refreshed summary")
    tmp = summary_path.with_suffix(".tmp")
    try:
        tmp.write_text(fresh, encoding="utf-8")
        tmp.replace(summary_path)
    except OSError as e:
        tmp.unlink(missing_ok=True)
        check(False, "memory summary regeneration", str(e))


def check_ledger():
    """Generation-ledger integrity (db/ledger/ — see its README.md).

    Every project ledger is schema-checked row by row (required fields,
    controlled-vocabulary membership, outcome enum, model ids against the
    specs layer, append-only supersedes rules, unique ids); the generated
    _global.json view is regenerated on drift like memory-summary."""
    try:
        import higgsfield_memory as hm
    except ImportError as e:
        check(False, "higgsfield_memory imports", str(e))
        return
    ledger_dir = ROOT / "db" / "ledger"
    if not ledger_dir.is_dir():
        skip("db/ledger/ directory", "not created yet — nothing to check")
        return
    model_ids = hm.load_specs_models()
    check(bool(model_ids), "specs model ids available for ledger validation")

    for path in sorted(ledger_dir.glob("*.json")):
        if path.name == "_global.json":
            continue
        rel = path.relative_to(ROOT)
        try:
            db = json.loads(path.read_text(encoding="utf-8"))
            rows = db["rows"]
            assert isinstance(rows, list)
        except Exception as e:  # noqa: BLE001
            check(False, f"{rel}: readable ledger (dict with rows list)",
                  f"{type(e).__name__}: {e}")
            continue
        problems, prior, superseded = [], set(), set()
        for row in rows:
            if not isinstance(row, dict):
                problems.append(f"non-object row: {repr(row)[:50]}")
                continue
            if row.get("id") in prior:
                problems.append(f"duplicate id {row.get('id')}")
            problems.extend(hm.validate_ledger_row(
                row, path.stem, prior, superseded, model_ids))
            if row.get("supersedes"):
                superseded.add(row["supersedes"])
            prior.add(row.get("id"))
        check(not problems, f"{rel}: {len(rows)} row(s) schema-valid",
              "" if not problems else "; ".join(problems[:3])
              + (f" (+{len(problems) - 3} more)" if len(problems) > 3 else ""))

    # _global.json is a generated view — regenerate on drift.
    fresh = hm.build_global()
    global_path = ledger_dir / "_global.json"
    try:
        on_disk = json.loads(global_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        on_disk = None
    if on_disk == fresh:
        check(True, "db/ledger/_global.json matches regeneration")
    else:
        warn("db/ledger/_global.json was stale — regenerated",
             "commit the refreshed view (generated, never hand-edit)")
        hm.write_global()


def check_hard_rules_canonical():
    """Root SKILL.md is the single home of the HARD RULES checklist.

    CLAUDE.md and DISCIPLINE.md reference the rules; they must carry the
    canonical-home pointer and must not cite a rule number that doesn't
    exist — the drift mode where a rule gets added/removed in SKILL.md and
    a stale '#9' (or a re-stated checklist) lives on elsewhere."""
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    section = re.search(r"^## HARD RULES.*?(?=^## )", skill_text,
                        re.MULTILINE | re.DOTALL)
    if not check(bool(section), "root SKILL.md has a HARD RULES section"):
        return
    rule_numbers = [int(n) for n in
                    re.findall(r"^(\d+)\.\s+\*\*", section.group(0), re.MULTILINE)]
    count = len(rule_numbers)
    ok = rule_numbers == list(range(1, count + 1)) and count > 0
    check(ok, f"HARD RULES numbered 1..{count} with no gaps",
          "" if ok else f"found numbering {rule_numbers}")

    # SKILL.md's own prose must agree with the actual count ("items 1–8").
    for m in re.finditer(r"items\s+1[–-](\d+)", section.group(0)):
        n = int(m.group(1))
        check(n == count, f"SKILL.md prose 'items 1–{n}' matches rule count",
              "" if n == count else f"checklist has {count} rules")

    for name in ("CLAUDE.md", "DISCIPLINE.md"):
        path = ROOT / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        has_pointer = re.search(r"HARD RULES.*(live|lives) in root `?SKILL\.md`?",
                                text) or re.search(
                                r"root `?SKILL\.md`?\s*§\s*HARD RULES", text)
        check(bool(has_pointer), f"{name} carries the canonical-home pointer",
              "" if has_pointer else "add the 'HARD RULES live in root SKILL.md' note")
        stale = sorted({int(n) for n in
                        re.findall(r"(?:HARD RULES?|rule)s?\s*#?\s*\(?(?:items?\s+)?(\d+)",
                                   text, re.IGNORECASE)
                        if int(n) > count})
        check(not stale, f"{name} cites no HARD RULE beyond #{count}",
              "" if not stale else f"stale rule reference(s): {stale}")


def check_repo_hygiene():
    """Fail if generated artifacts are tracked in git.

    Python bytecode was committed once before the .gitignore rule landed
    (Brief #2 item 3); this check makes that class of regression impossible
    instead of relying on the ignore file alone (.gitignore does not untrack
    already-tracked paths)."""
    try:
        result = subprocess.run(
            ["git", "ls-files"], capture_output=True, text=True,
            cwd=ROOT, timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        skip("git ls-files hygiene scan", f"git unavailable: {e}")
        return
    if result.returncode != 0:
        skip("git ls-files hygiene scan",
             "not a git checkout — hygiene scan needs git metadata")
        return
    tracked = result.stdout.splitlines()
    bytecode = [p for p in tracked
                if "__pycache__" in p.split("/") or p.endswith(".pyc")]
    check(not bytecode, "no Python bytecode tracked in git",
          "" if not bytecode else f"git rm -r --cached: {', '.join(bytecode[:5])}")
    # PDFs are release artifacts (gh release upload) as of v3.9.0 — tracking
    # them bloats history on every regeneration. MANIFEST.json carries the
    # shipped guide's identity instead.
    pdfs = [p for p in tracked if ".pdf" in p.lower()]
    check(not pdfs, "no PDF binaries tracked in git",
          "" if not pdfs else f"git rm --cached: {', '.join(pdfs[:5])}")


def main():
    args = parse_args()
    print(f"\nHiggsfield Skill Repo — Validation Report"
          + (" (--strict)" if args.strict else ""))
    print(f"Root: {ROOT}\n")

    # ── 1. Find all SKILL.md files ──────────────────────────────────────────
    print("[ SKILL.md FILES ]")
    skill_files = list(ROOT.rglob("SKILL.md"))
    print(f"  Found {len(skill_files)} SKILL.md files")

    for sf in sorted(skill_files):
        print(f"\n  — {sf.relative_to(ROOT)}")
        check_frontmatter(sf)
        check_relative_paths(sf)

    print("\n[ TEMPLATE PATHS ]")
    check_template_paths()

    # ── 2. JSON databases ───────────────────────────────────────────────────
    print("\n[ JSON DATABASES ]")
    check_json_db("filter-memory", DB_FILES["filter"], FILTER_REQUIRED_FIELDS)
    check_json_db("quality-memory", DB_FILES["quality"], QUALITY_REQUIRED_FIELDS)
    check_routing()

    # ── 3. Key root files present ───────────────────────────────────────────
    print("\n[ ROOT FILES ]")
    expected_root_files = [
        "SKILL.md", "README.md", "CHANGELOG.md", "DISCIPLINE.md",
        "model-guide.md", "image-models.md", "vocab.md",
        "prompt-examples.md", "photodump-presets.md",
        "production-benchmarks.md",
        "scripts/higgsfield_memory.py", "scripts/sync_specs.py",
        "scripts/build_index.py", "INDEX.md",
        "specs/model-specs.yaml", "specs/model-specs.json", "specs/MODEL-SPECS.md",
        "db/filter-memory.json", "db/quality-memory.json",
    ]
    for name in expected_root_files:
        path = ROOT / name
        check(path.exists(), name)

    # ── 4. Version / date consistency ───────────────────────────────────────
    print("\n[ VERSION / DATE CONSISTENCY ]")
    check_version_consistency()

    # ── 4b. Dispatcher ↔ disk sub-skill parity ──────────────────────────────
    print("\n[ DISPATCHER / SKILL PARITY ]")
    check_dispatcher_parity()
    check_description_coverage()

    # ── 4c. Model specs layer ───────────────────────────────────────────────
    print("\n[ MODEL SPECS ]")
    check_model_specs()

    # ── 4d. Heading index + QUICK FACTS contract ────────────────────────────
    print("\n[ INDEX / QUICK FACTS ]")
    check_index_and_quick_facts()

    # ── 4e. Learning-memory summary freshness ───────────────────────────────
    print("\n[ MEMORY ]")
    check_memory_summary()

    # ── 4f. Generation ledger ───────────────────────────────────────────────
    print("\n[ LEDGER ]")
    check_ledger()

    # ── 4g. HARD RULES canonical home ───────────────────────────────────────
    print("\n[ HARD RULES ]")
    check_hard_rules_canonical()

    # ── 4g. Repo hygiene ────────────────────────────────────────────────────
    print("\n[ HYGIENE ]")
    check_repo_hygiene()

    # ── 5. PDF dry-run smoke check ──────────────────────────────────────────
    print("\n[ PDF DRY-RUN SMOKE ]")
    try:
        result = subprocess.run(
            # sys.executable, not "python3": the smoke must run in the SAME
            # environment as this validator, or a bare venv would silently
            # borrow the system interpreter's fpdf2 and mask the skip path.
            [sys.executable, str(ROOT / "scripts" / "generate_user_guide.py"), "--dry-run"],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        check(False, "generate_user_guide.py --dry-run", "timeout after 60s")
    else:
        if result.returncode == 0:
            check(True, "generate_user_guide.py --dry-run", "exit 0")
        elif re.search(r"ModuleNotFoundError: No module named ['\"]?fpdf",
                       result.stderr or ""):
            # fpdf2 is an OPTIONAL dependency (requirements.txt: only the PDF
            # generator needs it). Every content check above already ran, so a
            # missing PDF toolchain must not report the repo as broken.
            skip("generate_user_guide.py --dry-run",
                 "optional dep fpdf2 not installed — pip install -r requirements.txt")
        else:
            stderr_lines = result.stderr.strip().splitlines() if result.stderr else []
            stderr_excerpt = stderr_lines[0] if stderr_lines else "(no stderr output)"
            check(
                False,
                "generate_user_guide.py --dry-run",
                f"exit {result.returncode}; stderr: {stderr_excerpt[:150]}",
            )

    # ── 6. Eval harness (opt-in) ────────────────────────────────────────────
    if args.evals:
        print("\n[ EVALS ]")
        check_evals()

    # ── Summary ─────────────────────────────────────────────────────────────
    print(f"\n{'='*50}")
    if args.strict and skips:
        # A release build may not ship with unverified surfaces.
        for s in skips:
            issues.append(f"[strict] skipped check must pass for release: {s}")
    if issues:
        print(f"\033[31m  FAILED — {len(issues)} issue(s) found:\033[0m")
        for i in issues:
            print(f"    • {i}")
        sys.exit(1)
    else:
        suffix = ""
        if warnings:
            suffix += f" ({len(warnings)} warning(s))"
        if skips:
            suffix += f" ({len(skips)} skipped — optional deps; --strict to enforce)"
        print(f"\033[32m  ALL CHECKS PASSED\033[0m{suffix}")
        sys.exit(0)


if __name__ == "__main__":
    main()
