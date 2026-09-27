#!/usr/bin/env python3
"""USER-GUIDE content derived from disk instead of hard-coded.

Dependency-free (stdlib only) so both the fpdf generator
(generate_user_guide.py) and the validator's content guard
(validate_user_guide.py --check-content, run by validate.py) can import it —
the same split as sub_skill_descriptions.py.

Why: generate_user_guide.py went unchanged from v3.23.0 to v3.36.0, so twelve
releases shipped a PDF whose only new bytes were the version string, while its
hard-coded counts drifted ("four templates" with ten on disk, "Eight named
modes" with fifteen, a model table without Seedance 2.5 / FLUX 3, an FAQ that
stops at v3.22). Everything below is read at build time:

  - root_version()        root SKILL.md metadata.version
  - changelog_entries()   the `## vX.Y.Z — YYYY-MM-DD` entries + one-line summary
  - derived_version()     the newest CHANGELOG version — what the guide's
                          What's New section (and so the guide) reflects
  - templates()           templates/ inventory with each file's H1 title
  - failure_modes()       named modes in skills/higgsfield-seedance/FAILURE-MODES.md
  - catalog()             model rows from specs/model-specs.json + image specs
  - check_content()       the guard: problems that must block a release build
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WHATS_NEW_COUNT = 5

_NUMBER_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven",
                 "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen",
                 "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]

# ponytail: FAILURE-MODES.md has no per-entry marker every mode carries (the
# fight entry has no **Symptom** line), so the structural sections are
# excluded by name. A new non-mode section would be counted as a mode —
# upgrade path: a `<!-- mode -->` marker per entry in the doctrine file.
NON_MODE_SECTIONS = {"how to use this reference", "self-repair before delivery",
                     "cross-references"}

_CHANGELOG_HEADING = re.compile(r"^## v(\d+\.\d+\.\d+)\s*[—–-]+\s*(\d{4}-\d{2}-\d{2})\s*$", re.M)
_VERSION_RE = re.compile(r"^\s+version:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", re.M)


class ContentError(RuntimeError):
    """A disk source the guide derives content from is missing or unparseable."""


def number_word(n: int) -> str:
    return _NUMBER_WORDS[n] if 0 <= n < len(_NUMBER_WORDS) else str(n)


def version_tuple(v: str) -> tuple:
    return tuple(int(x) for x in v.split("."))


def root_version(root: Path = ROOT) -> str | None:
    """metadata.version from the root SKILL.md frontmatter (indented key)."""
    try:
        text = (Path(root) / "SKILL.md").read_text(encoding="utf-8")
    except OSError:
        return None
    fm = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    m = _VERSION_RE.search(fm.group(1) if fm else "")
    return m.group(1) if m else None


def _plain(md: str) -> str:
    """Markdown → plain one-line text for the PDF."""
    s = re.sub(r"`([^`]*)`", r"\1", md)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"\*\*|__|(?<!\w)\*(?!\s)|(?<!\s)\*(?!\w)", "", s)
    return " ".join(s.split())


def _clip(s: str, limit: int) -> str:
    if len(s) <= limit:
        return s
    cut = s[:limit].rsplit(" ", 1)[0].rstrip(",;:—-")
    return cut + "..."


def changelog_entries(root: Path = ROOT, limit: int | None = WHATS_NEW_COUNT,
                      summary_chars: int = 320) -> list[dict]:
    """[{version, date, summary}] newest first. The summary is the entry's
    first prose paragraph (the bold one-line lede every entry opens with)."""
    try:
        text = (Path(root) / "CHANGELOG.md").read_text(encoding="utf-8")
    except OSError:
        return []
    heads = list(_CHANGELOG_HEADING.finditer(text))
    out = []
    for i, m in enumerate(heads):
        body = text[m.end(): heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        para = ""
        for block in re.split(r"\n\s*\n", body):
            block = block.strip()
            if not block or block.startswith(("#", "|", "```", "---")):
                continue
            para = block
            break
        if para.startswith(("- ", "* ")):
            para = para[2:]
        out.append({"version": m.group(1), "date": m.group(2),
                    "summary": _clip(_plain(para), summary_chars)})
    out.sort(key=lambda e: version_tuple(e["version"]), reverse=True)
    return out[:limit] if limit else out


def derived_version(root: Path = ROOT) -> str | None:
    entries = changelog_entries(root, limit=1)
    return entries[0]["version"] if entries else None


def _h1_title(path: Path) -> str:
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return re.sub(r"^Template:\s*", "", line[2:].strip())
    except OSError:
        pass
    return path.stem.replace("-", " ")


def templates(root: Path = ROOT) -> dict[str, list[tuple[str, str]]]:
    """{"genre": [(file, title)], "seedance": [...], "character-design": [...],
    "text-overlays": [...], "other": [...]} — sorted by file name."""
    base = Path(root) / "templates"
    inv: dict[str, list[tuple[str, str]]] = {"genre": [], "seedance": [],
                                             "character-design": [],
                                             "text-overlays": [], "other": []}
    if not base.is_dir():
        return inv
    for p in sorted(base.glob("*.md")):
        key = "genre" if re.match(r"^\d{2}-", p.name) else "other"
        inv[key].append((p.name, _h1_title(p)))
    for sub in ("seedance", "character-design", "text-overlays"):
        for p in sorted((base / sub).glob("*.md")):
            inv[sub].append((p.name, _h1_title(p)))
    return inv


def failure_modes(root: Path = ROOT) -> list[str]:
    path = Path(root) / "skills" / "higgsfield-seedance" / "FAILURE-MODES.md"
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return []
    return [h.strip() for h in re.findall(r"^## (.+)$", text, re.M)
            if h.strip().lower() not in NON_MODE_SECTIONS]


def _fmt_duration(d) -> str:
    if not d:
        return "--"
    if "values" in d:
        return "/".join(str(v) for v in d["values"]) + "s"
    lo, hi = d.get("min"), d.get("max")
    if "smart" in d:                       # {min: 2, max: 30, smart: -1} (wan3_0)
        return f"{lo}-{hi}s or {d['smart']} (smart)"
    if lo is not None and lo < 0:          # un-normalized sentinel: floor unknown
        return f"up to {hi}s / auto"
    return f"{lo}-{hi}s"


def catalog(root: Path = ROOT) -> dict:
    """Model rows straight from the generated specs: generative video models
    (those with a duration surface) and image models with an aspect-ratio
    surface — upscalers / removers / utilities have neither."""
    specs = Path(root) / "specs"
    out = {"video_snapshot": None, "image_snapshot": None, "video": [], "image": []}
    try:
        video = json.loads((specs / "model-specs.json").read_text(encoding="utf-8"))
        out["video_snapshot"] = video.get("snapshot_date")
        for m in sorted(video.get("models", []), key=lambda m: m["name"].lower()):
            if m.get("duration"):
                out["video"].append((m["name"], m["id"], _fmt_duration(m["duration"]),
                                     ", ".join(m.get("resolutions") or []) or "--"))
    except (OSError, json.JSONDecodeError):
        pass
    try:
        image = json.loads((specs / "image-model-specs.json").read_text(encoding="utf-8"))
        out["image_snapshot"] = image.get("snapshot_date")
        for m in sorted(image.get("models", []), key=lambda m: m["name"].lower()):
            if m.get("aspect_ratios"):
                out["image"].append((m["name"], m["id"],
                                     ", ".join(m.get("resolutions") or []) or "--",
                                     f"{len(m['aspect_ratios'])} ratios"))
    except (OSError, json.JSONDecodeError):
        pass
    return out


def check_content(root: Path = ROOT) -> list[str]:
    """Problems that make the guide unable to reflect the release. Empty =
    the derived content covers the root version.

    The v3.22.0 lesson: a manifest hash was blessed over a PDF with zero new
    content. The guide now leads with a What's New derived from CHANGELOG.md,
    so the version it reflects is the newest CHANGELOG entry it can parse —
    a root version newer than that means the release would ship a guide that
    says nothing about it."""
    problems = []
    rv = root_version(root)
    dv = derived_version(root)
    if rv is None:
        problems.append("root SKILL.md metadata.version not found")
    if dv is None:
        problems.append("CHANGELOG.md has no '## vX.Y.Z — YYYY-MM-DD' entry the "
                        "guide's What's New can derive from")
    if rv and dv and version_tuple(rv) > version_tuple(dv):
        problems.append(f"root version {rv} is newer than the newest CHANGELOG entry "
                        f"(v{dv}) the guide derives its What's New from — add the "
                        f"v{rv} entry before regenerating the guide")
    if not templates(root)["seedance"] or not templates(root)["genre"]:
        problems.append("templates/ inventory came back empty — the guide's template "
                        "tables would silently drop")
    if not failure_modes(root):
        problems.append("no named modes parsed from skills/higgsfield-seedance/"
                        "FAILURE-MODES.md")
    cat = catalog(root)
    if not cat["video"] or not cat["image"]:
        problems.append("specs/ model catalog came back empty — the guide's model "
                        "table would silently drop")
    return problems
