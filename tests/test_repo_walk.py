"""Repo walks never wander into `.claude/worktrees/` or a nested checkout.

Claude Code creates agent worktrees INSIDE the repo; the old
`ROOT.rglob("SKILL.md")` walks in validate.py and build_index.py descended into
them, so the main checkout reported `missing metadata.parent` once per worktree.
"""

import build_index
import validate
from repo_walk import walk_files

SKILL = "---\nname: x\n---\n# X\n"


def _tree(root):
    """A repo with real content plus three kinds of foreign trees."""
    (root / "skills" / "higgsfield-a").mkdir(parents=True)
    (root / "SKILL.md").write_text(SKILL)
    (root / "skills" / "higgsfield-a" / "SKILL.md").write_text(SKILL)
    # 1. a Claude Code agent worktree (its .git is a FILE)
    wt = root / ".claude" / "worktrees" / "agent-abc"
    (wt / "skills" / "higgsfield-a").mkdir(parents=True)
    (wt / ".git").write_text("gitdir: /elsewhere\n")
    (wt / "SKILL.md").write_text(SKILL)
    (wt / "skills" / "higgsfield-a" / "SKILL.md").write_text(SKILL)
    # 2. any nested checkout (its .git is a DIRECTORY), not under .claude
    nested = root / "vendor" / "other-repo"
    (nested / ".git").mkdir(parents=True)
    (nested / "SKILL.md").write_text(SKILL)
    # 3. a worktree dir that lost its .git file still sits under .claude/worktrees
    orphan = root / ".claude" / "worktrees" / "stale"
    orphan.mkdir(parents=True)
    (orphan / "SKILL.md").write_text(SKILL)
    return {root / "SKILL.md", root / "skills" / "higgsfield-a" / "SKILL.md"}


def test_walk_files_prunes_worktrees_and_nested_checkouts(tmp_path):
    expected = _tree(tmp_path)
    assert set(walk_files(tmp_path, "SKILL.md")) == expected


def test_build_index_skill_files_skip_worktrees(tmp_path, monkeypatch):
    expected = _tree(tmp_path)
    monkeypatch.setattr(build_index, "ROOT", tmp_path)
    assert set(build_index.skill_files()) == expected


def test_validate_skill_walk_skips_worktrees(tmp_path, monkeypatch):
    expected = _tree(tmp_path)
    monkeypatch.setattr(validate, "ROOT", tmp_path)
    assert set(validate.find_skill_files()) == expected


def test_validate_filename_index_skips_worktrees(tmp_path, monkeypatch):
    _tree(tmp_path)
    (tmp_path / ".claude" / "worktrees" / "agent-abc" / "only-in-worktree.md").write_text("x")
    (tmp_path / "vendor" / "other-repo" / "only-in-nested.md").write_text("x")
    monkeypatch.setattr(validate, "ROOT", tmp_path)
    monkeypatch.setattr(validate, "_repo_filename_index", None)
    names = validate.repo_filename_index()
    assert "SKILL.md" in names
    assert "only-in-worktree.md" not in names and "only-in-nested.md" not in names


def test_walk_from_a_subdirectory_keeps_the_root_rule(tmp_path):
    _tree(tmp_path)
    got = walk_files(tmp_path / ".claude", "SKILL.md", repo_root=tmp_path)
    assert got == []


def test_gitignore_ignores_agent_worktrees():
    from conftest import REPO
    lines = (REPO / ".gitignore").read_text(encoding="utf-8").splitlines()
    assert ".claude/worktrees/" in lines
