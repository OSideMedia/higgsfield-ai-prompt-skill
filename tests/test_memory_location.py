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
from pathlib import Path

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
    ("tmp/.claude/skills/archive/higgsfield", False),     # a clone nested deeper
    ("Users/me/.CLAUDE/Skills/higgsfield", True),         # another casing, same folder
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


def test_an_install_under_a_symlinked_dot_claude_is_still_an_install(tmp_path):
    real = tmp_path / "dotfiles" / "claude"               # ~/.claude -> dotfiles/claude
    (real / "skills" / "higgsfield").mkdir(parents=True)
    home = tmp_path / "home"
    home.mkdir()
    (home / ".claude").symlink_to(real)
    for root in (home / ".claude" / "skills" / "higgsfield", real / "skills" / "higgsfield"):
        assert hm.default_db_dir(root, home=home) == hm.USER_DB_DIR


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
    assert not list(dest.parent.glob(".db.*"))            # no temp folder left behind
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
    assert not list(dest.parent.glob(".db.*"))


def test_a_read_only_seed_gives_a_writable_memory(tmp_path):
    seed, dest = _seed(tmp_path), tmp_path / "home" / ".higgsfield-skill" / "db"
    paths = [seed / "filter-memory.json", seed / "ledger" / "README.md", seed / "ledger", seed]
    for path in paths:
        path.chmod(0o555 if path.is_dir() else 0o444)    # an install made read-only
    try:
        assert hm.seed_db_dir(dest, seed) is True
        for path in (dest, dest / "ledger", dest / "filter-memory.json"):
            assert os.access(path, os.W_OK), path
    finally:
        for path in paths:
            path.chmod(0o755 if path.is_dir() else 0o644)


def test_an_incomplete_memory_gets_the_missing_databases(tmp_path):
    seed, home = _seed(tmp_path), tmp_path / "home" / ".higgsfield-skill"
    dest = home / "db"
    (dest / "ledger").mkdir(parents=True)                 # a ledger written while no seed existed
    (dest / "ledger" / "adze.json").write_text('{"rows": []}', encoding="utf-8")
    kept = hm.prepare_user_db(dest, seed, home / "sources", home / "unmerged")
    assert kept is None
    assert (dest / "filter-memory.json").read_text(encoding="utf-8") == \
        (seed / "filter-memory.json").read_text(encoding="utf-8")
    assert (dest / "ledger" / "adze.json").read_text(encoding="utf-8") == '{"rows": []}'


def _entries(path, *ids):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"entries": [{"id": i, "outcome": "unknown"} for i in ids]}),
                    encoding="utf-8")


def test_a_racing_fill_never_replaces_the_other_installs_file(tmp_path, monkeypatch):
    home = tmp_path / "home" / ".higgsfield-skill"
    dest, seed = home / "db", tmp_path / "b" / "db"
    (dest / "ledger").mkdir(parents=True)                 # incomplete: no filter memory
    _entries(seed / "filter-memory.json", "F-902")        # install B's own entry
    real_link = os.link

    def install_a_writes_first(src, dst, *a, **k):        # A wins the gap after the check
        if Path(dst).name == "filter-memory.json" and not Path(dst).exists():
            _entries(Path(dst), "F-901")
        return real_link(src, dst, *a, **k)

    monkeypatch.setattr(hm.os, "link", install_a_writes_first)
    kept = hm.prepare_user_db(dest, seed, home / "sources", home / "unmerged")
    assert _ids(dest / "filter-memory.json") == {"F-901"}           # A's file intact
    assert kept and _ids(kept / "filter-memory.json") == {"F-902"}  # B's entry kept


def test_an_updated_starter_entry_is_not_an_installs_own_memory(tmp_path):
    home = tmp_path / "home" / ".higgsfield-skill"
    dest, sources, unmerged = home / "db", home / "sources", home / "unmerged"
    first, second = tmp_path / "a" / "db", tmp_path / "b" / "db"
    for seed in (first, second):
        _entries(seed / "filter-memory.json", "F-001")    # the same starter entry
    assert hm.prepare_user_db(dest, first, sources, unmerged) is None
    data = json.loads((dest / "filter-memory.json").read_text(encoding="utf-8"))
    data["entries"][0]["outcome"] = "fixed"               # the user updates it
    (dest / "filter-memory.json").write_text(json.dumps(data), encoding="utf-8")
    assert hm.prepare_user_db(dest, second, sources, unmerged) is None
    assert not unmerged.exists()


def test_a_record_in_another_projects_file_is_its_own(tmp_path):
    home = tmp_path / "home" / ".higgsfield-skill"
    dest, sources, unmerged = home / "db", home / "sources", home / "unmerged"
    first, second = tmp_path / "a" / "db", tmp_path / "b" / "db"
    _entries(first / "projects" / "alpha-filter-memory.json", "F-001")
    _entries(second / "projects" / "beta-filter-memory.json", "F-001")   # the same record
    assert hm.prepare_user_db(dest, first, sources, unmerged) is None
    kept = hm.prepare_user_db(dest, second, sources, unmerged)
    assert kept and (kept / "projects" / "beta-filter-memory.json").exists()


def test_a_failed_read_leaves_no_empty_database(tmp_path, monkeypatch):
    home = tmp_path / "home" / ".higgsfield-skill"
    dest, sources, unmerged = home / "db", home / "sources", home / "unmerged"
    (dest / "ledger").mkdir(parents=True)
    seed = tmp_path / "a" / "db"
    _entries(seed / "filter-memory.json", "F-001")
    real_read = type(seed).read_bytes

    def unreadable(self):
        raise PermissionError("denied")

    monkeypatch.setattr(type(seed), "read_bytes", unreadable)
    with pytest.raises(OSError):
        hm.prepare_user_db(dest, seed, sources, unmerged)
    assert not (dest / "filter-memory.json").exists()
    monkeypatch.setattr(type(seed), "read_bytes", real_read)
    hm.prepare_user_db(dest, seed, sources, unmerged)              # the next run fills it
    assert _ids(dest / "filter-memory.json") == {"F-001"}


def test_a_filled_database_counts_as_a_starting_record(tmp_path):
    home = tmp_path / "home" / ".higgsfield-skill"
    dest, sources, unmerged = home / "db", home / "sources", home / "unmerged"
    (dest / "ledger").mkdir(parents=True)                 # created while no seed existed
    first, second = tmp_path / "a" / "db", tmp_path / "b" / "db"
    for seed in (first, second):
        _entries(seed / "filter-memory.json", "F-001")
    assert hm.prepare_user_db(dest, first, sources, unmerged) is None   # fills it
    data = json.loads((dest / "filter-memory.json").read_text(encoding="utf-8"))
    data["entries"][0]["outcome"] = "fixed"               # the user updates it
    (dest / "filter-memory.json").write_text(json.dumps(data), encoding="utf-8")
    assert hm.prepare_user_db(dest, second, sources, unmerged) is None
    assert not unmerged.exists()


def test_the_seed_records_are_the_bytes_that_were_filled(tmp_path, monkeypatch):
    home = tmp_path / "home" / ".higgsfield-skill"
    dest, sources, unmerged = home / "db", home / "sources", home / "unmerged"
    (dest / "ledger").mkdir(parents=True)
    seed = tmp_path / "a" / "db"
    _entries(seed / "filter-memory.json", "F-001")
    real_publish = hm._publish

    def seed_changes_after_the_copy(target, data):          # a write lands mid-fill
        done = real_publish(target, data)
        _entries(seed / "filter-memory.json", "F-001", "F-902")
        return done

    monkeypatch.setattr(hm, "_publish", seed_changes_after_the_copy)
    kept = hm.prepare_user_db(dest, seed, sources, unmerged)
    assert kept and "F-902" in _ids(kept / "filter-memory.json")   # not taken as seeded


def test_a_copy_that_fails_is_not_recorded_as_kept(tmp_path, monkeypatch):
    home = tmp_path / "home" / ".higgsfield-skill"
    dest, sources, unmerged = home / "db", home / "sources", home / "unmerged"
    _entries(dest / "filter-memory.json", "F-901")
    seed = tmp_path / "b" / "db"
    _entries(seed / "filter-memory.json", "F-902")

    def rename_fails(self, target):
        raise PermissionError("sharing violation")

    monkeypatch.setattr(type(tmp_path), "rename", rename_fails)
    with pytest.raises(OSError):
        hm.prepare_user_db(dest, seed, sources, unmerged)
    assert not sources.exists() or not list(sources.iterdir())    # checked again next time


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
    return home, skill, _env(home)


def _env(home):
    """The environment with `home` as the home folder on every platform."""
    env = {k: v for k, v in os.environ.items()
           if k not in ("HF_DB_DIR", "HOMEDRIVE", "HOMEPATH")}
    env["HOME"] = env["USERPROFILE"] = str(home)
    return env


def _install(home, rel, extra=None):
    """Install the skill at home/rel; `extra` adds a filter entry of the
    user's own, as an install older than v3.42.0 would hold."""
    skill = home / rel
    skill.mkdir(parents=True)
    for part in ("scripts", "db", "specs"):
        shutil.copytree(REPO / part, skill / part,
                        ignore=shutil.ignore_patterns("__pycache__"))
    if extra:
        path = skill / "db" / "filter-memory.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["entries"].append({"id": extra, "category": "c", "blocked_terms": [],
                                "error_message": "e", "tags": []})
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return skill


def _ids(path):
    return {e["id"] for e in json.loads(path.read_text(encoding="utf-8"))["entries"]}


def _run(env, script, *args):
    r = subprocess.run([sys.executable, str(script), *args],
                       capture_output=True, text=True, env=env)
    return r.returncode, r.stdout, r.stderr


def test_an_install_keeps_its_memory_outside_the_skill_folder(install):
    home, skill, env = install
    shipped = (skill / "db" / "filter-memory.json").read_bytes()
    code, out, err = _run(env, skill / "scripts" / "higgsfield_memory.py", "where")
    assert code == 0, out + err
    where = json.loads(out)
    user_db = home / ".higgsfield-skill" / "db"
    assert where["db_dir"] == str(user_db) and where["source"] == "skill install"
    assert (user_db / "filter-memory.json").read_bytes() == shipped   # seeded on first use

    entry = json.dumps({"category": "c", "blocked_terms": ["x"], "error_message": "blocked",
                        "failed_prompt": "x", "tags": ["t"]})
    code, out, err = _run(env, skill / "scripts" / "higgsfield_memory.py", "add-filter", entry)
    assert code == 0, out + err
    assert (skill / "db" / "filter-memory.json").read_bytes() == shipped   # install untouched
    added = json.loads((user_db / "filter-memory.json").read_text(encoding="utf-8"))
    assert len(added["entries"]) == len(json.loads(shipped)["entries"]) + 1


def test_the_linter_can_be_the_first_script_an_install_runs(install):
    home, skill, env = install
    code, out, err = _run(env, skill / "scripts" / "seedance_lint.py", "--preflight",
                          "A woman walks through a quiet street at dusk.")
    assert code in (0, 1) and "Traceback" not in err, out + err
    assert (home / ".higgsfield-skill" / "db" / "filter-memory.json").exists()   # seeded on import
    assert "memory-recall — F-" in out                    # and the recall read it


def test_a_checkout_keeps_its_memory_in_db(tmp_path):
    env = _env(tmp_path)                                  # nothing may be seeded here
    code, out, _ = _run(env, REPO / "scripts" / "higgsfield_memory.py", "where")
    assert code == 0 and json.loads(out)["db_dir"] == str(REPO / "db")
    assert not (tmp_path / ".higgsfield-skill").exists()


def test_a_second_older_install_keeps_its_own_memory(tmp_path):
    home = tmp_path / "home"
    env = _env(home)
    personal = _install(home, ".claude/skills/higgsfield", extra="F-901")
    project = _install(home, "film/.claude/skills/higgsfield", extra="F-902")
    fresh = _install(home, "ads/.claude/skills/higgsfield")
    shared = home / ".higgsfield-skill" / "db" / "filter-memory.json"
    where = personal / "scripts" / "higgsfield_memory.py"

    _, _, err = _run(env, where, "where")                 # the first install seeds
    assert "not merged" not in err and "F-901" in _ids(shared)
    code, out, err = _run(env, project / "scripts" / "higgsfield_memory.py", "where")
    assert code == 0 and "not merged" in err, err         # told once...
    [kept] = json.loads(out)["unmerged"]
    assert "F-902" in _ids(Path(kept) / "filter-memory.json")
    assert "F-902" not in _ids(shared)                    # ...kept, not merged
    _, _, err = _run(env, project / "scripts" / "higgsfield_memory.py", "where")
    assert "not merged" not in err                        # and only once
    _, out, err = _run(env, fresh / "scripts" / "higgsfield_memory.py", "where")
    assert "not merged" not in err and len(json.loads(out)["unmerged"]) == 1


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
    monkeypatch.setattr(hm, "LEDGER_DIR", shipped / "ledger")
    (shipped / "memory-summary.md").write_text(hm.build_summary(), encoding="utf-8")
    # The active memory is a user's: this repo's real entries and a project ledger.
    active_ledger = tmp_path / "user-db" / "ledger"
    active_ledger.mkdir(parents=True)
    shutil.copyfile(REPO / "db" / "ledger" / "_demo.json", active_ledger / "demo.json")
    monkeypatch.setattr(hm, "FILTER_DB", REPO / "db" / "filter-memory.json")
    monkeypatch.setattr(hm, "QUALITY_DB", REPO / "db" / "quality-memory.json")
    monkeypatch.setattr(hm, "LEDGER_DIR", active_ledger)
    monkeypatch.setattr(validate, "ROOT", tmp_path / "repo")
    monkeypatch.setattr(validate, "STRICT", True)
    validate.check_memory_summary()
    assert validate.issues == []
