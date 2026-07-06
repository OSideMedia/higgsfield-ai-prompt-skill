"""Shared fixtures for the tooling test suite.

The scripts/ directory is added to sys.path so the flat-module tooling
(seedance_lint, sync_specs, higgsfield_memory, validate) imports directly.
DB redirection uses the HF_DB_DIR env var (see scripts/higgsfield_memory.py)
because it works identically for in-process imports and subprocess CLI
invocations.
"""

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
FIXTURES = Path(__file__).parent / "fixtures"
MINI_SNAPSHOT = FIXTURES / "models_explore_snapshot_2026-06-11.json"

sys.path.insert(0, str(SCRIPTS))


@pytest.fixture
def tmp_db(tmp_path, monkeypatch):
    """Empty filter/quality DBs in a temp dir, exported via HF_DB_DIR."""
    db = tmp_path / "db"
    db.mkdir()
    for name in ("filter-memory.json", "quality-memory.json"):
        (db / name).write_text(
            json.dumps({"entries": [], "_total_entries": 0}), encoding="utf-8")
    monkeypatch.setenv("HF_DB_DIR", str(db))
    return db


@pytest.fixture(scope="session")
def mini_spec(tmp_path_factory):
    """Specs built from the committed 4-entry mini snapshot (seedance_2_0 +
    its video_standard duplicate, kling3_0, veo3_1_lite). Returns
    (spec_dict, json_path) — the path feeds seedance_lint.load_specs."""
    import sync_specs
    spec = sync_specs.build_spec(MINI_SNAPSHOT)
    p = tmp_path_factory.mktemp("specs") / "model-specs.json"
    p.write_text(sync_specs.emit_json(spec), encoding="utf-8")
    return spec, p
