"""validate.py — exit-code contract and the guide↔specs contradiction checker."""

import importlib.util
import json
import subprocess
import sys

import pytest

import validate
from conftest import REPO

SPEC = {
    "snapshot_date": "2026-06-11",
    "models": [
        {"id": "seedance_2_0", "name": "Seedance 2.0", "aliases": ["video_standard"],
         "duration": {"min": 4, "max": 15}},
        {"id": "veo3_1_lite", "name": "Veo 3.1 Lite", "aliases": [],
         "duration": {"values": [4, 6, 8]}},
        {"id": "kling3_0", "name": "Kling 3.0", "aliases": [],
         "duration": {"min": 3, "max": 15}},
    ],
}


def run_checks(guide):
    return validate.check_guide_against_specs(guide, SPEC)


HEADER = ("| Model | Realism | Duration | Best for |\n"
          "|-------|---------|----------|----------|\n")


def test_matching_range_passes():
    results = run_checks(HEADER + "| Kling 3.0 | ★★★★★ | 3–15s | cinematic |\n")
    assert [ok for ok, *_ in results] == [True]


def test_single_value_against_range_fails():
    # The headline drift case: '10s' claimed for a 4–15s model.
    results = run_checks(HEADER + "| Seedance 2.0 | ★★★★★ | 10s | multimodal |\n")
    assert [ok for ok, *_ in results] == [False]


def test_values_list_matches():
    results = run_checks(HEADER + "| Veo 3.1 Lite | ★★★★☆ | 4/8s | budget |\n")
    assert [ok for ok, *_ in results] == [False]  # 4/8 ≠ 4/6/8
    results = run_checks(HEADER + "| Veo 3.1 Lite | ★★★★☆ | 4/6/8s | budget |\n")
    assert [ok for ok, *_ in results] == [True]


def test_range_against_noncontiguous_values_fails():
    # "4–8s" against a [4,6,8] enum invites an illegal duration:7 — a range
    # cell is honest only when the enum is a contiguous integer run.
    results = run_checks(HEADER + "| Veo 3.1 Lite | ★★★★☆ | 4–8s | budget |\n")
    assert [ok for ok, *_ in results] == [False]


def test_unknown_model_skipped():
    results = run_checks(HEADER + "| Sora 2 | ★★★★☆ | — | epic |\n"
                                  "| Some Legacy Model | ★★★☆☆ | 5–10s | old |\n")
    assert results == []


def test_table_without_duration_column_ignored():
    guide = ("| Model | Quality | Best for |\n"
             "|-------|---------|----------|\n"
             "| Seedance 2.0 | ★★★★★ | anything |\n")
    assert run_checks(guide) == []


def test_dash_cell_skipped():
    results = run_checks(HEADER + "| Kling 3.0 | ★★★★★ | — | cinematic |\n")
    assert results == []


# ── Whole-script exit codes ─────────────────────────────────────────────────

def test_repo_validates_clean():
    result = subprocess.run([sys.executable, str(REPO / "scripts" / "validate.py")],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stdout[-2000:]


# ── v3.37.0: every spec type is regenerated from its NEWEST snapshot ────────

@pytest.fixture
def scratch_specs(tmp_path, monkeypatch):
    """A scratch COPY of specs/ that both validate and sync_specs point at
    (module paths included, so the pre-fix code is exercised fairly too).
    Fresh issue/warning lists so assertions see only this run."""
    import shutil
    import sync_specs
    s = tmp_path / "specs"
    shutil.copytree(REPO / "specs", s)
    monkeypatch.setattr(validate, "SPECS_DIR", s)
    monkeypatch.setattr(validate, "SPECS_JSON", s / "model-specs.json")
    monkeypatch.setattr(validate, "issues", [])
    monkeypatch.setattr(validate, "warnings", [])
    monkeypatch.setattr(validate, "STRICT", False)
    monkeypatch.setattr(sync_specs, "SPECS_DIR", s)
    for attr, name in (("YAML_OUT", "model-specs.yaml"), ("JSON_OUT", "model-specs.json"),
                       ("MD_OUT", "MODEL-SPECS.md")):
        monkeypatch.setattr(sync_specs, attr, s / name)
    return s


def _run_specs_check():
    import contextlib
    import io
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        validate.check_model_specs()
    return validate.issues


@pytest.mark.parametrize("fname", ["image-model-specs.json", "audio-model-specs.json",
                                   "3d-model-specs.json", "model-specs.json"])
def test_hand_edited_generated_specs_fail_for_every_type(scratch_specs, fname):
    p = scratch_specs / fname
    d = json.loads(p.read_text(encoding="utf-8"))
    d["models"][0]["name"] += " HANDEDIT"
    p.write_text(json.dumps(d, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    issues = _run_specs_check()
    assert any("match regeneration" in i and fname in i for i in issues), issues


def test_newer_unsynced_snapshot_fails(scratch_specs):
    """A newer dump committed without re-running sync_specs: the pre-fix check
    rebuilt from the snapshot the JSON names itself, so this passed."""
    snap = json.loads((scratch_specs / "models_explore_snapshot_2026-09-26.json")
                      .read_text(encoding="utf-8"))
    for m in snap["items"]:
        if m["id"] == "seedance_2_5":
            for prm in m["parameters"]:
                if prm["name"] == "resolution":
                    prm["options"].append("4k")
    (scratch_specs / "models_explore_snapshot_2099-01-01.json").write_text(
        json.dumps(snap), encoding="utf-8")
    issues = _run_specs_check()
    assert any("newest snapshot is models_explore_snapshot_2099-01-01.json" in i
               for i in issues), issues


def test_missing_tombstone_fails(scratch_specs):
    (scratch_specs / "retired-model-ids.json").unlink()
    issues = _run_specs_check()
    assert any("retired-model-ids.json" in i for i in issues), issues


def test_clean_scratch_copy_passes(scratch_specs):
    assert _run_specs_check() == []


def test_snapshot_age_mode_is_strict_and_covers_3d(scratch_specs, monkeypatch, capsys):
    import sync_specs
    p = scratch_specs / "3d-model-specs.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["snapshot_date"] = "2020-01-01"
    p.write_text(json.dumps(d), encoding="utf-8")
    validate.check_typed_snapshot_ages(sync_specs.TYPES)
    assert validate.issues == []                      # non-strict: a warning only
    monkeypatch.setattr(validate, "STRICT", True)
    validate.check_typed_snapshot_ages(sync_specs.TYPES)
    assert any("3d specs snapshot fresh" in i for i in validate.issues)


def test_snapshot_age_cli_mode_exit_codes():
    ok = subprocess.run([sys.executable, str(REPO / "scripts" / "validate.py"),
                         "--snapshot-age"], capture_output=True, text=True)
    assert "3d specs snapshot" in ok.stdout
    assert ok.returncode in (0, 1)   # 1 only once the committed snapshots age out


@pytest.mark.skipif(importlib.util.find_spec("fpdf") is not None,
                    reason="fpdf2 installed — strict-mode SKIP path not reachable")
def test_strict_fails_without_fpdf2():
    result = subprocess.run([sys.executable, str(REPO / "scripts" / "validate.py"), "--strict"],
                            capture_output=True, text=True)
    assert result.returncode == 1
    assert "skipped check" in result.stdout
