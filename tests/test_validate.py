"""validate.py — exit-code contract and the guide↔specs contradiction checker."""

import importlib.util
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


def test_range_endpoints_against_values():
    results = run_checks(HEADER + "| Veo 3.1 Lite | ★★★★☆ | 4–8s | budget |\n")
    assert [ok for ok, *_ in results] == [True]


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


@pytest.mark.skipif(importlib.util.find_spec("fpdf") is not None,
                    reason="fpdf2 installed — strict-mode SKIP path not reachable")
def test_strict_fails_without_fpdf2():
    result = subprocess.run([sys.executable, str(REPO / "scripts" / "validate.py"), "--strict"],
                            capture_output=True, text=True)
    assert result.returncode == 1
    assert "skipped check" in result.stdout
