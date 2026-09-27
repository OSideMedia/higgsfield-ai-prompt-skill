"""evals/run_evals.py — vacuous passes are harness ERRORs; spec-driven flips
are named as such.

Written against the public run_case()/main() surface so the same tests run
on the pre-fix harness (git show 9b86817:evals/run_evals.py) — where every
test below went RED: the vacuous cases returned [] (a pass) and the flip was
reported as a "checker regression".
"""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("run_evals", REPO / "evals" / "run_evals.py")
run_evals = importlib.util.module_from_spec(_spec)
sys.modules["run_evals"] = run_evals
_spec.loader.exec_module(run_evals)

GOOD_RESPONSE = ("**Model**: Seedance 2.0\n**Mode**: std  **Aspect ratio**: 16:9  "
                 "**Duration**: 8s  **Resolution**: 1080p\n\nStyle: noir. Slow "
                 "dolly-in on a figure in a wool coat. Interior warehouse at dusk.")


@pytest.fixture(scope="module")
def specs():
    return run_evals._spec_index()


def is_error(failures):
    return bool(failures) and any("error" in f.lower() for f in failures)


def case(assertions, model="seedance_2_0", response=GOOD_RESPONSE):
    return {"id": "t", "model": model, "response": response, "assertions": assertions}


@pytest.mark.parametrize("assertions", [
    [{"type": "enum_legal", "expect": "ilegal"}],          # typo'd expect
    [],                                                    # no assertions
    [{"type": "word_count"}],                              # no bounds
    [{"type": "sections_present", "names": []}],           # empty names
    [{"type": "preset_names_valid", "names": []}],         # empty names
    [{"type": "lint_verdict", "max": "WARNING"}],          # unknown verdict
    [{"type": "enm_legal"}],                               # unknown type
], ids=["bad-expect", "no-assertions", "word-count-unbounded", "empty-sections",
        "empty-presets", "bad-max", "unknown-type"])
def test_vacuous_assertions_are_harness_errors(specs, assertions):
    failures = run_evals.run_case(case(assertions), specs)
    assert is_error(failures), failures


def test_enum_legal_without_declared_settings_is_an_error(specs):
    bare = "Style: noir. Slow dolly-in on a figure in a wool coat. Interior warehouse at dusk."
    failures = run_evals.run_case(case([{"type": "enum_legal"}], response=bare), specs)
    assert is_error(failures), failures


def test_well_formed_case_still_passes(specs):
    c = case([{"type": "enum_legal"}, {"type": "word_count", "max": 200},
              {"type": "sections_present", "names": ["Style"]}])
    assert run_evals.run_case(c, specs) == []


TRAP_1080P = ("**Model**: Seedance 2.5\n**Mode**: t2v  **Aspect ratio**: 16:9  "
              "**Duration**: 10s  **Resolution**: 1080p\n\nA kettle reaches boil on "
              "a gas stove, steam against morning window light. Static close-up.")


def _premise_1080p_flip(specs):
    s25 = run_evals.sl.resolve_model(specs, "seedance_2_5")
    old = REPO / "specs" / "models_explore_snapshot_2026-08-07.json"
    if s25 is None or "1080p" not in s25["resolutions"] or not old.exists():
        pytest.fail("fixture premise gone: needs seedance_2_5 with 1080p in the "
                    "current specs and the committed 2026-08-07 snapshot without it")


def test_spec_driven_flip_is_named(specs):
    _premise_1080p_flip(specs)
    failures = run_evals.run_case(
        case([{"type": "enum_legal", "expect": "illegal"}], "seedance_2_5", TRAP_1080P),
        specs)
    assert len(failures) == 1
    assert "spec-driven flip" in failures[0] and "2026-08-07" in failures[0]
    assert "checker regression" not in failures[0]


def test_real_checker_regression_still_says_so(specs, monkeypatch):
    # No earlier snapshot under which the trap held → it IS the checker.
    monkeypatch.setattr(run_evals, "_prior_indexes", lambda: [], raising=False)
    failures = run_evals.run_case(
        case([{"type": "enum_legal", "expect": "illegal"}], "seedance_2_5", TRAP_1080P),
        specs)
    assert len(failures) == 1 and "checker regression" in failures[0]


def test_legal_golden_flipped_by_specs_is_named(specs, monkeypatch):
    # A golden that WAS legal under an earlier snapshot and is illegal now.
    now = run_evals.sl.resolve_model(specs, "seedance_2_0")
    earlier = dict(now, aspect_ratios=now["aspect_ratios"] + ["5:1"])
    fake_index = {"seedance_2_0": earlier, "_ambiguous": {}}
    monkeypatch.setattr(run_evals, "_prior_indexes",
                        lambda: [("2026-01-01", fake_index)], raising=False)
    golden = GOOD_RESPONSE.replace("16:9", "5:1")
    failures = run_evals.run_case(case([{"type": "enum_legal"}], "seedance_2_0", golden), specs)
    assert len(failures) == 1
    assert "spec-driven flip" in failures[0] and "2026-01-01" in failures[0]


def test_main_counts_errors_and_exits_nonzero(tmp_path, monkeypatch, capsys):
    doc = {"skill": "t", "cases": [case([{"type": "enum_legal", "expect": "ilegal"}]),
                                   dict(case([{"type": "word_count", "max": 500}]), id="ok")]}
    (tmp_path / "t.json").write_text(json.dumps(doc), encoding="utf-8")
    monkeypatch.setattr(run_evals, "CASES_DIR", tmp_path)
    monkeypatch.setattr(sys, "argv", ["run_evals.py"])
    assert run_evals.main() == 1
    out = capsys.readouterr().out
    assert "1/2 eval cases passed" in out and "ERROR" in out


def test_committed_cases_have_no_harness_errors(specs):
    # The corpus itself must be well-formed; a malformed committed case is a
    # silent pass waiting to happen.
    errors = []
    for path in sorted((REPO / "evals" / "cases").glob("*.json")):
        for c in json.loads(path.read_text(encoding="utf-8")).get("cases", []):
            fs = run_evals.run_case(c, specs)
            errors += [f"{c['id']}: {f}" for f in fs if f.startswith("harness ERROR")]
    assert errors == []
