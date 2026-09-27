#!/usr/bin/env python3
"""
repo_walk.py
============
The one way the repo tooling walks the tree. Stdlib only.

Claude Code creates agent worktrees INSIDE the repo at `.claude/worktrees/<name>/`
— each a full second checkout of every SKILL.md. A plain `ROOT.rglob("SKILL.md")`
walked straight into them, so validate.py reported
`✗ .claude/worktrees/agent-…/SKILL.md: missing metadata.parent` once per worktree
and build_index.py would have indexed them. Pruned here, before descending:

  * `.claude/worktrees/` under the root
  * any directory that carries its OWN `.git` (file or directory) — a nested
    checkout or worktree is another repository, never this one's content
  * `.git` and `__pycache__`
"""

from __future__ import annotations

import fnmatch
import os
from pathlib import Path

SKIP_DIR_NAMES = {".git", "__pycache__"}
SKIP_REL_PREFIXES = ((".claude", "worktrees"),)


def is_foreign_dir(path: Path, root: Path) -> bool:
    """True for a directory the walk must not enter (see module doc)."""
    if path.name in SKIP_DIR_NAMES:
        return True
    try:
        rel = path.relative_to(root).parts
    except ValueError:
        rel = ()
    if any(rel[:len(p)] == p for p in SKIP_REL_PREFIXES):
        return True
    return path != root and (path / ".git").exists()


def walk_files(root: Path, pattern: str, repo_root: Path = None) -> list[Path]:
    """Sorted files under `root` whose NAME matches `pattern` (fnmatch),
    pruning foreign directories before descending. `repo_root` anchors the
    `.claude/worktrees` rule when `root` is a subdirectory."""
    repo_root = repo_root or root
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        here = Path(dirpath)
        dirnames[:] = sorted(d for d in dirnames
                             if not is_foreign_dir(here / d, repo_root))
        out.extend(here / f for f in filenames if fnmatch.fnmatchcase(f, pattern))
    return sorted(out)
