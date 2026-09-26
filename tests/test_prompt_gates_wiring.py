"""validate.py wiring of the prompt-side gates (preflight coverage, claims
lint, USER-GUIDE content guard): reached from main(), strict/non-strict
severity as documented, and a hard gate that goes red in both modes."""

import inspect
import subprocess
from types import SimpleNamespace

import pytest

import validate


def test_main_calls_the_gates():
    assert "check_prompt_gates()" in inspect.getsource(validate.main)


@pytest.fixture
def fresh(monkeypatch):
    monkeypatch.setattr(validate, "issues", [])
    monkeypatch.setattr(validate, "warnings", [])
    return monkeypatch


def _fake_run(codes):
    def run(argv, **kw):
        script = argv[1].rsplit("/", 1)[-1]
        return SimpleNamespace(returncode=codes.get(script, 0),
                               stdout=f"{script} summary\n  ✗ a.md:1  [x] claim\n", stderr="")
    return run


@pytest.mark.parametrize("strict,claims_issue", [(True, True), (False, False)])
def test_claims_red_is_fatal_only_under_strict(fresh, strict, claims_issue):
    fresh.setattr(validate, "STRICT", strict)
    fresh.setattr(subprocess, "run", _fake_run({"claims_lint.py": 1}))
    validate.check_prompt_gates()
    assert any("claims_lint" in i for i in validate.issues) is claims_issue
    assert any("claims_lint" in w for w in validate.warnings) is (not claims_issue)


def test_rule_coverage_red_is_always_fatal(fresh):
    fresh.setattr(validate, "STRICT", False)
    fresh.setattr(subprocess, "run", _fake_run({"preflight.py": 1}))
    validate.check_prompt_gates()
    assert any("preflight.py" in i for i in validate.issues)


def test_all_green_adds_nothing(fresh):
    fresh.setattr(validate, "STRICT", True)
    fresh.setattr(subprocess, "run", _fake_run({}))
    validate.check_prompt_gates()
    assert validate.issues == [] and validate.warnings == []
