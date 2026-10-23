"""Where the learning memory lives (v3.42.0).

A Claude Code skill install is replaced by a reinstall and updated by
`git pull`, so the memory moves out of it into ~/.higgsfield-skill/db/,
seeded from the skill's db/ on first use. Anywhere else the memory stays in
the skill's own db/. The end-to-end tests build a real install layout under a
throwaway HOME and run the scripts the way the skill does.
"""

import json
import os
import shutil
import subprocess
import sys

import pytest

import higgsfield_memory as hm
import validate
from conftest import REPO


# ── default_db_dir: the path rule ────────────────────────────────────────────

@pytest.mark.parametrize("rel,installed", [
    (".claude/skills/higgsfield", True),                  # personal install
    ("work/film/.claude/skills/higgsfield", True),        # project install
    ("Projects/higgsfield", False),                       # a checkout
    ("cowork/higgsfield-ai-prompt-skill-main", False),    # a Cowork workspace
    ("Projects/higgsfield/.claude/worktrees/agent-1", False),
    ("skills/.claude/higgsfield", False),                 # both words, wrong order
])
def test_default_db_dir_follows_the_install_path(tmp_path, rel, installed):
    root = tmp_path / rel
    root.mkdir(parents=True)
    expected = hm.USER_DB_DIR if installed else hm.SEED_DIR
    assert hm.default_db_dir(root) == expected


def test_a_symlinked_dev_checkout_keeps_its_own_db(tmp_path):
    checkout = tmp_path / "Projects" / "higgsfield"
    checkout.mkdir(parents=True)
    link = tmp_path / ".claude" / "skills" / "higgsfield"
    link.parent.mkdir(parents=True)
    link.symlink_to(checkout)
    assert hm.default_db_dir(link) == hm.SEED_DIR         # resolved: a checkout


# ── seed_db_dir: first use only, never a merge ───────────────────────────────

def _seed(tmp_path):
    seed = tmp_path / "seed"
    (seed / "ledger").mkdir(parents=True)
    (seed / "filter-memory.json").write_text('{"entries": [{"id": "F-001"}]}', encoding="utf-8")
    (seed / "ledger" / "README.md").write_text("# ledger\n", encoding="utf-8")
    return seed


def test_seed_copies_the_whole_db_once(tmp_path):
    seed, dest = _seed(tmp_path), tmp_path / "home" / ".higgsfield-skill" / "db"
    assert hm.seed_db_dir(dest, seed) is True
    assert (dest / "filter-memory.json").read_text(encoding="utf-8") == \
        (seed / "filter-memory.json").read_text(encoding="utf-8")
    assert (dest / "ledger" / "README.md").exists()
    assert not list(dest.parent.glob(".db.seeding-*"))   # no temp folder left behind
    (dest / "filter-memory.json").write_text('{"entries": []}', encoding="utf-8")
    assert hm.seed_db_dir(dest, seed) is False            # an existing memory is never touched
    assert (dest / "filter-memory.json").read_text(encoding="utf-8") == '{"entries": []}'


def test_seed_loses_a_race_cleanly(tmp_path, monkeypatch):
    seed, dest = _seed(tmp_path), tmp_path / "home" / ".higgsfield-skill" / "db"
    real_copytree = shutil.copytree

    def copy_while_another_process_wins(src, dst, *a, **k):
        monkeypatch.setattr(hm.shutil, "copytree", real_copytree)   # copytree recurses
        real_copytree(src, dest)                          # the other process lands first
        (dest / "winner").write_text("x", encoding="utf-8")
        return real_copytree(src, dst, *a, **k)

    monkeypatch.setattr(hm.shutil, "copytree", copy_while_another_process_wins)
    assert hm.seed_db_dir(dest, seed) is False
    assert (dest / "winner").exists()                     # the winner's folder is intact
    assert not list(dest.parent.glob(".db.seeding-*"))


# ── end to end: a real install layout under a throwaway HOME ─────────────────

@pytest.fixture
def install(tmp_path):
    """A Claude Code install of this skill at <HOME>/.claude/skills/higgsfield."""
    home = tmp_path / "home"
    skill = home / ".claude" / "skills" / "higgsfield"
    skill.mkdir(parents=True)
    for part in ("scripts", "db", "specs"):
        shutil.copytree(REPO / part, skill / part,
                        ignore=shutil.ignore_patterns("__pycache__"))
    env = {k: v for k, v in os.environ.items() if k != "HF_DB_DIR"}
    env["HOME"] = str(home)
    return home, skill, env


def _run(env, script, *args):
    r = subprocess.run([sys.executable, str(script), *args],
                       capture_output=True, text=True, env=env)
    return r.returncode, r.stdout


def test_an_install_keeps_its_memory_outside_the_skill_folder(install):
    home, skill, env = install
    shipped = (skill / "db" / "filter-memory.json").read_bytes()
    code, out = _run(env, skill / "scripts" / "higgsfield_memory.py", "where")
    assert code == 0, out
    where = json.loads(out)
    user_db = home / ".higgsfield-skill" / "db"
    assert where["db_dir"] == str(user_db) and where["source"] == "skill install"
    assert (user_db / "filter-memory.json").read_bytes() == shipped   # seeded on first use

    entry = json.dumps({"category": "c", "blocked_terms": ["x"], "error_message": "blocked",
                        "failed_prompt": "x", "tags": ["t"]})
    code, out = _run(env, skill / "scripts" / "higgsfield_memory.py", "add-filter", entry)
    assert code == 0, out
    assert (skill / "db" / "filter-memory.json").read_bytes() == shipped   # install untouched
    added = json.loads((user_db / "filter-memory.json").read_text(encoding="utf-8"))
    assert len(added["entries"]) == len(json.loads(shipped)["entries"]) + 1


def test_the_linter_can_be_the_first_script_an_install_runs(install):
    home, skill, env = install
    code, out = _run(env, skill / "scripts" / "seedance_lint.py", "--preflight",
                     "A woman walks through a quiet street at dusk.")
    assert code in (0, 1), out                            # a verdict, never a crash
    assert (home / ".higgsfield-skill" / "db" / "filter-memory.json").exists()   # seeded on import


def test_a_checkout_keeps_its_memory_in_db(tmp_path):
    env = {k: v for k, v in os.environ.items() if k != "HF_DB_DIR"}
    env["HOME"] = str(tmp_path)                           # nothing may be seeded here
    code, out = _run(env, REPO / "scripts" / "higgsfield_memory.py", "where")
    assert code == 0 and json.loads(out)["db_dir"] == str(REPO / "db")
    assert not (tmp_path / ".higgsfield-skill").exists()


# ── validate certifies the shipped db/, not whichever memory is active ───────

@pytest.fixture
def fresh_report(monkeypatch):
    monkeypatch.setattr(validate, "issues", [])
    monkeypatch.setattr(validate, "warnings", [])


def test_validate_reads_the_shipped_db_not_the_active_memory(tmp_path, monkeypatch, fresh_report):
    shipped = tmp_path / "repo" / "db"                    # an empty shipped memory
    shipped.mkdir(parents=True)
    for name in ("filter-memory.json", "quality-memory.json"):
        (shipped / name).write_text(json.dumps({"entries": []}), encoding="utf-8")
    monkeypatch.setattr(hm, "FILTER_DB", shipped / "filter-memory.json")
    monkeypatch.setattr(hm, "QUALITY_DB", shipped / "quality-memory.json")
    (shipped / "memory-summary.md").write_text(hm.build_summary(), encoding="utf-8")
    # The active memory is a user's, with this repo's real entries in it.
    monkeypatch.setattr(hm, "FILTER_DB", REPO / "db" / "filter-memory.json")
    monkeypatch.setattr(hm, "QUALITY_DB", REPO / "db" / "quality-memory.json")
    monkeypatch.setattr(validate, "ROOT", tmp_path / "repo")
    monkeypatch.setattr(validate, "STRICT", True)
    validate.check_memory_summary()
    assert validate.issues == []
