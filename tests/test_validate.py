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


# ── v3.37.0: --strict fails on stale generated DB views (no silent repair) ───

@pytest.fixture
def fresh_report(monkeypatch):
    monkeypatch.setattr(validate, "issues", [])
    monkeypatch.setattr(validate, "warnings", [])


def _quiet(fn):
    import contextlib
    import io
    with contextlib.redirect_stdout(io.StringIO()):
        fn()


@pytest.mark.parametrize("strict", [True, False])
def test_stale_memory_summary(tmp_path, monkeypatch, fresh_report, strict):
    (tmp_path / "db").mkdir()
    stale = tmp_path / "db" / "memory-summary.md"
    stale.write_text("# STALE hand-edited summary\n", encoding="utf-8")
    monkeypatch.setattr(validate, "ROOT", tmp_path)
    monkeypatch.setattr(validate, "STRICT", strict)
    _quiet(validate.check_memory_summary)
    if strict:
        assert any("memory-summary.md is current" in i for i in validate.issues)
        assert stale.read_text(encoding="utf-8").startswith("# STALE")   # gate never repairs
    else:
        assert validate.issues == [] and validate.warnings    # warn + regenerate
        assert not stale.read_text(encoding="utf-8").startswith("# STALE")


@pytest.mark.parametrize("strict", [True, False])
def test_stale_global_ledger(tmp_path, monkeypatch, fresh_report, strict):
    import higgsfield_memory as hm
    ledger = tmp_path / "db" / "ledger"
    ledger.mkdir(parents=True)
    glob = ledger / "_global.json"
    glob.write_text(json.dumps({"rows": ["hand-edited"]}), encoding="utf-8")
    monkeypatch.setattr(validate, "ROOT", tmp_path)
    monkeypatch.setattr(validate, "STRICT", strict)
    monkeypatch.setattr(hm, "LEDGER_DIR", ledger)
    monkeypatch.setattr(hm, "GLOBAL_LEDGER", glob)
    _quiet(validate.check_ledger)
    if strict:
        assert any("_global.json matches regeneration" in i for i in validate.issues)
        assert json.loads(glob.read_text())["rows"] == ["hand-edited"]
    else:
        assert validate.issues == [] and validate.warnings
        assert json.loads(glob.read_text())["rows"] == []


def _env_without_fpdf(tmp_path):
    """An environment in which `import fpdf` fails exactly as it does when
    fpdf2 is not installed: a stub package first on PYTHONPATH that raises
    ModuleNotFoundError. validate.py passes its env to the PDF child, so the
    skip path is reachable even where fpdf2 IS installed (incl. CI) — the old
    skipif made this test run nowhere."""
    import os
    stub = tmp_path / "no_fpdf" / "fpdf"
    stub.mkdir(parents=True)
    (stub / "__init__.py").write_text(
        "raise ModuleNotFoundError(\"No module named 'fpdf'\", name='fpdf')\n",
        encoding="utf-8")
    prior = os.environ.get("PYTHONPATH", "")
    return dict(os.environ, PYTHONPATH=str(tmp_path / "no_fpdf") + (os.pathsep + prior if prior else ""))


def test_strict_fails_without_fpdf2(tmp_path):
    env = _env_without_fpdf(tmp_path)
    # Positive control: the stub really blocks fpdf in a child interpreter.
    probe = subprocess.run([sys.executable, "-c", "import fpdf"], env=env,
                           capture_output=True, text=True)
    assert probe.returncode != 0 and "No module named 'fpdf'" in probe.stderr
    validate_py = str(REPO / "scripts" / "validate.py")
    strict = subprocess.run([sys.executable, validate_py, "--strict"], env=env,
                            capture_output=True, text=True)
    assert strict.returncode == 1, strict.stdout[-1500:]
    assert ("[strict] skipped check must pass for release: generate_user_guide.py --dry-run"
            in strict.stdout)
    loose = subprocess.run([sys.executable, validate_py], env=env,
                           capture_output=True, text=True)
    assert loose.returncode == 0, loose.stdout[-1500:]
    assert "generate_user_guide.py --dry-run" in loose.stdout and "[SKIP]" in loose.stdout
