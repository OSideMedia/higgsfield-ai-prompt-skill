"""higgsfield_memory.py CLI — round-trips against a temp db via HF_DB_DIR.

Subprocess invocations on purpose: that's how the skill actually calls the
tool, and it exercises the env-var redirection end to end.
"""

import json
import os
import subprocess
import sys

from conftest import REPO

MEM = str(REPO / "scripts" / "higgsfield_memory.py")


def run(tmp_db, *args):
    env = dict(os.environ, HF_DB_DIR=str(tmp_db))
    result = subprocess.run([sys.executable, MEM, *args],
                            capture_output=True, text=True, env=env)
    return result.returncode, result.stdout.strip()


def test_filter_round_trip(tmp_db):
    entry = json.dumps({"category": "test-cat", "blocked_terms": ["foo"],
                        "error_message": "blocked", "failed_prompt": "a foo prompt",
                        "tags": ["unit-test"]})
    code, out = run(tmp_db, "add-filter", entry)
    assert code == 0 and json.loads(out)["id"] == "F-001"

    code, out = run(tmp_db, "query-filter", "foo prompt")
    results = json.loads(out)["results"]
    assert [e["id"] for e in results] == ["F-001"]

    code, out = run(tmp_db, "update-filter", "F-001", "fixed")
    assert json.loads(out)["status"] == "ok"
    db = json.loads((tmp_db / "filter-memory.json").read_text(encoding="utf-8"))
    e = db["entries"][0]
    assert e["outcome"] == "fixed"
    assert e["fix_confirmed"] is True
    assert e["substitution_worked"] is True
    assert db["_total_entries"] == 1


def test_invalid_outcome_rejected(tmp_db):
    entry = json.dumps({"category": "c", "blocked_terms": [], "error_message": "e",
                        "failed_prompt": "p", "tags": []})
    run(tmp_db, "add-filter", entry)
    code, out = run(tmp_db, "update-filter", "F-001", "fixedd")
    assert json.loads(out)["status"] == "error"
    db = json.loads((tmp_db / "filter-memory.json").read_text(encoding="utf-8"))
    assert db["entries"][0].get("outcome", "unknown") == "unknown"


def test_quality_round_trip(tmp_db):
    entry = json.dumps({"failure_type": "motion-static", "model_used": "seedance-2.0",
                        "original_prompt": "p", "failure_description": "static",
                        "tags": ["unit-test"]})
    code, out = run(tmp_db, "add-quality", entry)
    assert code == 0 and json.loads(out)["id"] == "Q-001"

    code, out = run(tmp_db, "update-quality", "Q-001", "improved", "better prompt")
    assert json.loads(out)["status"] == "ok"
    db = json.loads((tmp_db / "quality-memory.json").read_text(encoding="utf-8"))
    e = db["entries"][0]
    assert e["improvement_confirmed"] is True
    assert e["improved_prompt"] == "better prompt"


def test_stats_counts(tmp_db):
    entry = json.dumps({"category": "c", "blocked_terms": [], "error_message": "e",
                        "failed_prompt": "p", "tags": []})
    run(tmp_db, "add-filter", entry)
    code, out = run(tmp_db, "stats")
    stats = json.loads(out)
    assert stats["filter_memory"]["total_entries"] == 1
    assert stats["quality_memory"]["total_entries"] == 0
