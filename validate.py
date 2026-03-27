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

Usage:
  python validate.py
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
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

PASS = "\033[32m✓\033[0m"
FAIL = "\033[31m✗\033[0m"
WARN = "\033[33m⚠\033[0m"

issues = []
warnings = []


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


def check_frontmatter(skill_file: Path):
    text = skill_file.read_text(encoding="utf-8")
    # Extract YAML frontmatter between --- delimiters
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        check(False, f"{skill_file.relative_to(ROOT)}: missing frontmatter")
        return
    fm = match.group(1)
    for field in FRONTMATTER_REQUIRED:
        present = re.search(rf"^{field}:", fm, re.MULTILINE) is not None
        if not present:
            check(False, f"{skill_file.relative_to(ROOT)}: missing frontmatter field '{field}'")
    # tags should be nested inside metadata, not at the top level
    if re.search(r"^tags:", fm, re.MULTILINE):
        check(False, f"{skill_file.relative_to(ROOT)}: tags should be inside metadata, not at top level")


def check_relative_paths(skill_file: Path):
    text = skill_file.read_text(encoding="utf-8")
    # Find all relative paths referenced with backticks or markdown links
    # Matches: `../../../vocab.md` or `skills/higgsfield-prompt/SKILL.md`
    refs = re.findall(r'`((?:\.\.\/|[\w-]+\/)[\w./%-]+\.(?:md|py|json))`', text)
    for ref in refs:
        target = (skill_file.parent / ref).resolve()
        exists = target.exists()
        label = f"{skill_file.relative_to(ROOT)}: ref '{ref}'"
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
    declared = db.get("_total_entries", -1)
    check(len(entries) == declared,
          f"{label}: entry count matches _total_entries",
          f"declared={declared}, actual={len(entries)}")

    for entry in entries:
        eid = entry.get("id", "?")
        for field in required_fields:
            if field not in entry:
                check(False, f"{label} entry {eid}: missing field '{field}'")


def main():
    print(f"\nHiggsfield Skill Repo — Validation Report")
    print(f"Root: {ROOT}\n")

    # ── 1. Find all SKILL.md files ──────────────────────────────────────────
    print("[ SKILL.md FILES ]")
    skill_files = list(ROOT.rglob("SKILL.md"))
    print(f"  Found {len(skill_files)} SKILL.md files")

    for sf in sorted(skill_files):
        print(f"\n  — {sf.relative_to(ROOT)}")
        check_frontmatter(sf)
        check_relative_paths(sf)

    # ── 2. JSON databases ───────────────────────────────────────────────────
    print("\n[ JSON DATABASES ]")
    check_json_db("filter-memory", DB_FILES["filter"], FILTER_REQUIRED_FIELDS)
    check_json_db("quality-memory", DB_FILES["quality"], QUALITY_REQUIRED_FIELDS)

    # ── 3. Key root files present ───────────────────────────────────────────
    print("\n[ ROOT FILES ]")
    expected_root_files = [
        "SKILL.md", "README.md", "CHANGELOG.md", "model-guide.md",
        "image-models.md", "vocab.md", "prompt-examples.md",
        "photodump-presets.md", "higgsfield_memory.py",
        "db/filter-memory.json", "db/quality-memory.json",
    ]
    for name in expected_root_files:
        path = ROOT / name
        check(path.exists(), name)

    # ── Summary ─────────────────────────────────────────────────────────────
    print(f"\n{'='*50}")
    if issues:
        print(f"\033[31m  FAILED — {len(issues)} issue(s) found:\033[0m")
        for i in issues:
            print(f"    • {i}")
        sys.exit(1)
    else:
        print(f"\033[32m  ALL CHECKS PASSED\033[0m" +
              (f" ({len(warnings)} warning(s))" if warnings else ""))
        sys.exit(0)


if __name__ == "__main__":
    main()
