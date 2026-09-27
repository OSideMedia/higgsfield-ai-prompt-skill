"""CI workflows — the shell blocks are EXECUTED here, not just grepped.

Steps are extracted from the workflow text (stdlib only, no YAML library) and
run with `bash -e`, the runner's default shell, against controlled inputs:

  * spec-drift.yml's classifier must give EVERY refresh_specs.py exit code a
    branch (pre-v3.37 codes other than 0/1/3/4 matched no step and the job went
    green) and quote the CLI's own line with the kind's remedy (it blamed the
    credentials for 10 weeks while the CLI said "No workspace selected.").
  * validate.yml's lint self-check must demand the FAIL exit code AND the rule
    id (pre-v3.37 any non-zero exit — a traceback, an unknown-model exit 2 —
    passed as "expected FAIL").
"""
import os
import re
import shutil
import subprocess
import sys

import pytest

from conftest import REPO

WF = REPO / ".github" / "workflows"
BASH = shutil.which("bash")
pytestmark = pytest.mark.skipif(BASH is None, reason="bash not available")


def step_run(workflow: str, name_prefix: str) -> str:
    """The literal `run: |` block of the step whose name starts with prefix."""
    lines = (WF / workflow).read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^(\s*)- name: (.*)$", line)
        if not (m and m.group(2).startswith(name_prefix)):
            continue
        step_indent = len(m.group(1))
        for j in range(i + 1, len(lines)):
            r = re.match(r"^(\s*)run: \|\s*$", lines[j])
            if r:
                base = None
                body = []
                for k in range(j + 1, len(lines)):
                    ln = lines[k]
                    if ln.strip() == "":
                        body.append("")
                        continue
                    ind = len(ln) - len(ln.lstrip())
                    if ind <= len(r.group(1)):
                        break
                    base = ind if base is None else base
                    body.append(ln[base:])
                return "\n".join(body) + "\n"
            if re.match(rf"^\s{{0,{step_indent}}}- ", lines[j]):
                break
    raise AssertionError(f"{workflow}: no step starting with {name_prefix!r} with a run block")


def run_bash(script: str, cwd, env: dict):
    return subprocess.run([BASH, "-e", "-c", script], cwd=cwd, capture_output=True,
                          text=True, env={**os.environ, **env})


# ── spec-drift.yml: every outcome is classified ─────────────────────────────

@pytest.mark.parametrize("code,state", [
    ("0", "fresh"), ("3", "changed"),
    ("1", "blind"), ("4", "blind"), ("2", "blind"),
    ("", "blind"),          # the tripwire never ran (install failed)
    ("7", "blind"),         # an exit code nobody planned for
])
def test_spec_drift_classifier_handles_every_exit_code(tmp_path, code, state):
    out = tmp_path / "out"
    out.write_text("")
    script = step_run("spec-drift.yml", "Classify the outcome")
    r = run_bash(script, tmp_path, {"CODE": code, "KIND": "", "LINE": "", "REMEDY": "",
                                    "GITHUB_OUTPUT": str(out)})
    assert r.returncode == 0, r.stderr
    assert f"state={state}" in out.read_text().splitlines()
    assert ("::error::" in r.stdout) == (state == "blind")


def test_spec_drift_quotes_the_cli_line_and_the_right_remedy(tmp_path):
    out = tmp_path / "out"
    out.write_text("")
    script = step_run("spec-drift.yml", "Classify the outcome")
    r = run_bash(script, tmp_path, {
        "CODE": "1", "KIND": "workspace", "LINE": "Error: No workspace selected.",
        "REMEDY": "set the HIGGSFIELD_WORKSPACE_ID repo secret", "GITHUB_OUTPUT": str(out)})
    err = [l for l in r.stdout.splitlines() if l.startswith("::error::")]
    assert len(err) == 1
    assert "Error: No workspace selected." in err[0]
    assert "kind=workspace" in err[0] and "HIGGSFIELD_WORKSPACE_ID" in err[0]
    assert "HIGGSFIELD_CREDENTIALS" not in err[0]


def test_spec_drift_wiring():
    text = (WF / "spec-drift.yml").read_text(encoding="utf-8")
    assert "refresh_specs.py --status-json" in text
    assert "validate.py --snapshot-age" in text                 # auth-free staleness gate
    assert "higgsfield workspace set" in text and "HIGGSFIELD_WORKSPACE_ID" in text
    assert 'LAST_VERIFIED_CLI: "1.1.23"' in text
    for step in ("Blind → open or update the BLIND issue", "Sighted again → close the BLIND issue",
                 "Drift detected → open or refresh the drift issue",
                 "Fresh → close the drift issue", "Fail the job when blind or stale"):
        assert f"- name: {step}" in text, step


def test_spec_drift_final_gate_fails_blind_or_stale(tmp_path):
    script = step_run("spec-drift.yml", "Fail the job when blind or stale")
    assert run_bash(script, tmp_path, {"STATE": "fresh", "AGE": "success"}).returncode == 0
    assert run_bash(script, tmp_path, {"STATE": "changed", "AGE": "success"}).returncode == 0
    assert run_bash(script, tmp_path, {"STATE": "blind", "AGE": "success"}).returncode != 0
    assert run_bash(script, tmp_path, {"STATE": "", "AGE": "success"}).returncode != 0
    assert run_bash(script, tmp_path, {"STATE": "fresh", "AGE": "failure"}).returncode != 0


# ── validate.yml: known-FAIL needs the FAIL code AND the rule id ─────────────

FAKE_LINTER = '''import sys
args = " ".join(sys.argv[1:])
fail_case = "--mode fast" in args or "--ar 21:9" in args
MODE = {mode!r}
if fail_case and MODE == "crash":      # a traceback / unknown-model exit 2
    print("Traceback (most recent call last):\\n  KeyError: 'specs'", file=sys.stderr)
    sys.exit(2)
if fail_case and MODE == "wrong-rule":
    print("  x [FAIL] some-other-rule"); sys.exit(1)
if not fail_case and MODE == "pass-fails":
    print("  x [FAIL] mode-constraint"); sys.exit(1)
if fail_case:
    rule = "mode-constraint" if "--mode fast" in args else "ar-not-supported"
    print(f"  x [FAIL] {{rule}}"); sys.exit(1)
sys.exit(0)
'''


def _fake_repo(tmp_path, mode):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "seedance_lint.py").write_text(FAKE_LINTER.format(mode=mode))
    return tmp_path


def test_lint_selfcheck_passes_on_the_real_linter():
    script = step_run("validate.yml", "Seedance lint self-check")
    r = run_bash(script, REPO, {})
    assert r.returncode == 0, r.stdout + r.stderr
    assert "lint self-check OK" in r.stdout


@pytest.mark.parametrize("mode", ["crash", "wrong-rule", "pass-fails"])
def test_lint_selfcheck_rejects_a_wrong_failure(tmp_path, mode):
    script = step_run("validate.yml", "Seedance lint self-check")
    r = run_bash(script, _fake_repo(tmp_path, mode), {})
    assert r.returncode != 0, f"{mode}: self-check passed a broken linter\n{r.stdout}"


def test_lint_selfcheck_positive_control_fake_linter_behaving(tmp_path):
    script = step_run("validate.yml", "Seedance lint self-check")
    r = run_bash(script, _fake_repo(tmp_path, "ok"), {})
    assert r.returncode == 0, r.stdout + r.stderr


def test_validate_yml_has_no_directory_scaffolding():
    text = (WF / "validate.yml").read_text(encoding="utf-8")
    assert "if [ -d tests ]" not in text and "if [ -d evals ]" not in text
    assert "python3 -m pytest -q" in text and "validate.py --evals" in text


# ── v3.37.0 review: crashes are named; the CLI is pinned and checksum-verified ──

@pytest.mark.parametrize("code,kind,fragment", [
    ("5", "crash", "crashed (exit 5)"),
    ("1", "", "without writing a classified status"),
    ("1", "auth", "CLI said (redacted)"),
])
def test_spec_drift_names_a_crash_and_redacted_lines(tmp_path, code, kind, fragment):
    out = tmp_path / "out"
    out.write_text("")
    script = step_run("spec-drift.yml", "Classify the outcome")
    r = run_bash(script, tmp_path, {"CODE": code, "KIND": kind, "LINE": "Session expired",
                                    "REMEDY": "re-login", "GITHUB_OUTPUT": str(out)})
    assert "state=blind" in out.read_text().splitlines()
    err = [l for l in r.stdout.splitlines() if l.startswith("::error::")]
    assert len(err) == 1 and fragment in err[0], err


def _fake_release(tmp_path, body="#!/bin/sh\necho 'higgsfield 1.1.23 (test)'\n"):
    import hashlib
    import tarfile
    src = tmp_path / "src"
    src.mkdir()
    (src / "hf").write_text(body)
    (src / "hf").chmod(0o755)
    archive = tmp_path / "release.tar.gz"
    with tarfile.open(archive, "w:gz") as t:
        t.add(src / "hf", arcname="hf")
    fakebin = tmp_path / "fakebin"
    fakebin.mkdir()
    # curl stand-in: honor `-o PATH`, "download" the fake archive, log the URL.
    (fakebin / "curl").write_text(
        '#!/bin/bash\nwhile [ $# -gt 0 ]; do case "$1" in -o) OUT="$2"; shift 2;; '
        f'-*) shift;; *) echo "$1" >> "{tmp_path}/urls"; shift;; esac; done\n'
        f'cp "{archive}" "$OUT"\n')
    (fakebin / "curl").chmod(0o755)
    return hashlib.sha256(archive.read_bytes()).hexdigest(), fakebin


def test_cli_install_is_pinned_and_checksum_verified(tmp_path):
    script = step_run("spec-drift.yml", "Install Higgsfield CLI")
    assert not re.search(r"\|\s*(?:ba)?sh(?:\s|$)", script) and "install.sh" not in script
    sha, fakebin = _fake_release(tmp_path)
    (tmp_path / "home").mkdir()
    (tmp_path / "rt").mkdir()
    env = {"PATH": f"{fakebin}:{os.environ['PATH']}", "HOME": str(tmp_path / "home"),
           "RUNNER_TEMP": str(tmp_path / "rt"), "GITHUB_PATH": str(tmp_path / "gp"),
           "LAST_VERIFIED_CLI": "1.1.23", "CLI_SHA256": sha}
    ok = run_bash(script, tmp_path, env)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    assert (tmp_path / "home" / ".local" / "bin" / "higgsfield").exists()
    assert "releases/download/v1.1.23/hf_1.1.23_linux_amd64.tar.gz" in (tmp_path / "urls").read_text()
    bad = run_bash(script, tmp_path, {**env, "CLI_SHA256": "0" * 64,
                                      "HOME": str(tmp_path / "home2")})
    assert bad.returncode != 0 and "does not match CLI_SHA256" in bad.stdout
    assert not (tmp_path / "home2" / ".local" / "bin" / "higgsfield").exists()


def test_pinned_cli_checksum_is_well_formed():
    text = (WF / "spec-drift.yml").read_text(encoding="utf-8")
    m = re.search(r'CLI_SHA256: "([0-9a-f]+)"', text)
    assert m and len(m.group(1)) == 64
