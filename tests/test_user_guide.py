"""USER-GUIDE generator: derived content + the staleness guards.

generate_user_guide.py went unchanged v3.23.0 → v3.36.0, so its hard-coded
counts drifted ("four templates" / "Eight named modes") and its model table
never gained Seedance 2.5 or FLUX 3. These tests compare the rendered text
against counts taken from disk INDEPENDENTLY of the generator's own
derivation, and prove the release guards can go red. All went red on
9b86817's generate_user_guide.py / validate_user_guide.py.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

import user_guide_content as ugc
import validate_user_guide as vug

REPO = Path(__file__).resolve().parents[1]


# ── Guard: root version vs the version the derived content reflects ────────

def _mini_root(tmp_path, root_version="3.37.0", changelog_top="3.37.0",
               heading_fmt="## v{v} — 2026-09-26"):
    (tmp_path / "SKILL.md").write_text(
        "---\nname: higgsfield\nmetadata:\n  version: " + root_version +
        "\n  updated: 2026-09-26\n---\n# Root\n", encoding="utf-8")
    (tmp_path / "CHANGELOG.md").write_text(
        "# Changelog\n\n" + heading_fmt.format(v=changelog_top) +
        "\n\n**A release that did a thing.** More words.\n\n## v3.30.0 — 2026-08-01\n\n"
        "**Older.**\n", encoding="utf-8")
    t = tmp_path / "templates"
    (t / "seedance").mkdir(parents=True)
    (t / "01-a.md").write_text("# Template: A\n", encoding="utf-8")
    (t / "seedance" / "x.md").write_text("# Template: X\n", encoding="utf-8")
    fm = tmp_path / "skills" / "higgsfield-seedance"
    fm.mkdir(parents=True)
    (fm / "FAILURE-MODES.md").write_text(
        "## How to use this reference\n## Drift\n## Cross-references\n", encoding="utf-8")
    s = tmp_path / "specs"
    s.mkdir()
    (s / "model-specs.json").write_text(json.dumps({"snapshot_date": "2026-09-26", "models": [
        {"id": "v", "name": "V", "duration": {"min": 4, "max": 8}, "resolutions": []}]}))
    (s / "image-model-specs.json").write_text(json.dumps({"snapshot_date": "2026-09-26",
        "models": [{"id": "i", "name": "I", "aspect_ratios": ["1:1"]}]}))
    return tmp_path


def test_guard_passes_when_changelog_covers_root(tmp_path):
    assert vug.check_content(_mini_root(tmp_path)) == []


def test_guard_fails_when_root_is_newer_than_derived_content(tmp_path):
    root = _mini_root(tmp_path, root_version="3.38.0", changelog_top="3.37.0")
    problems = vug.check_content(root)
    assert any("3.38.0" in p and "3.37.0" in p for p in problems), problems


def test_guard_fails_when_changelog_format_breaks_derivation(tmp_path):
    root = _mini_root(tmp_path, heading_fmt="## [{v}] - 2026-09-26")
    derived = ugc.derived_version(root)
    assert derived == "3.30.0"            # the renamed entry is invisible...
    assert vug.check_content(root)        # ...so the guard goes red


@pytest.mark.parametrize("missing", ["templates", "skills", "specs"])
def test_guard_fails_when_a_derived_source_is_empty(tmp_path, missing):
    import shutil
    root = _mini_root(tmp_path)
    shutil.rmtree(root / missing)
    assert vug.check_content(root)


def test_guard_cli_on_the_repo():
    r = subprocess.run([sys.executable, str(REPO / "scripts" / "validate_user_guide.py"),
                        "--check-content"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "Derived-content check: PASS" in r.stdout


def test_manifest_refuses_zero_new_content():
    old = {"version": "3.35.0", "normalized_text_sha256": "abc"}
    assert vug.manifest_progress_problem(old, {"version": "3.36.0",
                                               "normalized_text_sha256": "abc"})
    assert vug.manifest_progress_problem(old, {"version": "3.36.0",
                                               "normalized_text_sha256": "def"}) is None
    assert vug.manifest_progress_problem(old, {"version": "3.35.0",
                                               "normalized_text_sha256": "abc"}) is None
    assert vug.manifest_progress_problem(None, {"version": "3.36.0"}) is None


def test_write_manifest_exits_on_zero_new_content(tmp_path, monkeypatch):
    cand = tmp_path / "USER-GUIDE.pdf"
    cand.write_bytes(b"%PDF-1.4")
    mpath = tmp_path / "MANIFEST.json"
    mpath.write_text(json.dumps({"version": "3.35.0", "normalized_text_sha256": "abc"}))
    monkeypatch.setattr(vug, "MANIFEST_PATH", mpath)
    monkeypatch.setattr(vug, "build_manifest",
                        lambda p: {"version": "3.36.0", "normalized_text_sha256": "abc"})
    with pytest.raises(SystemExit) as exc:
        vug.write_manifest(cand)
    assert exc.value.code == 1
    assert json.loads(mpath.read_text())["version"] == "3.35.0"   # not overwritten


# ── Derived content actually reaches the rendered guide ─────────────────────

def _independent_counts():
    fm = (REPO / "skills/higgsfield-seedance/FAILURE-MODES.md").read_text(encoding="utf-8")
    heads = [h.strip().lower() for h in re.findall(r"^## (.+)$", fm, re.M)]
    structural = {"how to use this reference", "self-repair before delivery", "cross-references"}
    return {
        "modes": len([h for h in heads if h not in structural]),
        "seedance_templates": len(list((REPO / "templates/seedance").glob("*.md"))),
        "genre_templates": len([p for p in (REPO / "templates").glob("*.md")
                                if re.match(r"\d{2}-", p.name)]),
    }


@pytest.fixture(scope="module")
def rendered_text():
    pytest.importorskip("fpdf", reason="fpdf2 is the generator's optional dependency")
    import fpdf
    import generate_user_guide as g
    seen = []
    orig_cell, orig_multi = fpdf.FPDF.cell, fpdf.FPDF.multi_cell

    def cell(self, w=None, h=None, text="", *a, **k):
        seen.append(str(k.get("txt", text)))
        return orig_cell(self, w, h, text, *a, **k)

    def multi_cell(self, w, h=None, text="", *a, **k):
        seen.append(str(k.get("txt", text)))
        return orig_multi(self, w, h, text, *a, **k)

    fpdf.FPDF.cell, fpdf.FPDF.multi_cell = cell, multi_cell
    try:
        g.build_pdf(dry_run=True)
    finally:
        fpdf.FPDF.cell, fpdf.FPDF.multi_cell = orig_cell, orig_multi
    return "\n".join(seen)


def test_counts_match_disk_not_hardcoding(rendered_text):
    n = _independent_counts()
    assert f"{ugc.number_word(n['modes']).capitalize()} named modes" in rendered_text
    assert f"{ugc.number_word(n['seedance_templates'])} templates in `templates/seedance/`" \
        in rendered_text
    assert f"{n['genre_templates']} deeply annotated prompt templates" in rendered_text
    if n["modes"] != 8:
        assert "Eight named modes" not in rendered_text
    if n["seedance_templates"] != 4:
        assert "four templates in" not in rendered_text


def test_every_seedance_template_and_mode_is_named(rendered_text):
    for p in (REPO / "templates/seedance").glob("*.md"):
        assert p.name in rendered_text, p.name
    fm = (REPO / "skills/higgsfield-seedance/FAILURE-MODES.md").read_text(encoding="utf-8")
    for head in ("Walking is the hardest stunt", "Orphan limbs in a group shot"):
        if f"## {head}" in fm:
            assert head in rendered_text


def test_model_catalog_comes_from_specs(rendered_text):
    specs = json.loads((REPO / "specs/model-specs.json").read_text(encoding="utf-8"))
    generative = [m["id"] for m in specs["models"] if m.get("duration")]
    assert generative
    for mid in generative:
        assert mid in rendered_text, mid
    for name in ("Seedance 2.5", "FLUX 3 Video"):
        if any(m["name"] == name for m in specs["models"]):
            assert name in rendered_text


def test_whats_new_reflects_the_newest_changelog_entry(rendered_text):
    top = ugc.changelog_entries(REPO, limit=1)[0]
    assert "What's New" in rendered_text
    assert f"v{top['version']} -- {top['date']}" in rendered_text
    assert top["summary"][:40] in rendered_text


def test_dry_run_stays_fast():
    import time
    pytest.importorskip("fpdf")
    t = time.monotonic()
    r = subprocess.run([sys.executable, str(REPO / "scripts/generate_user_guide.py"),
                        "--dry-run"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert time.monotonic() - t < 15
