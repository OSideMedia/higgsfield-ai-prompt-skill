"""sync_specs.py — normalization, alias folding, constraint extraction."""

import json

import pytest

import sync_specs
from conftest import MINI_SNAPSHOT, REPO


def test_alias_folded_into_canonical(mini_spec):
    spec, _ = mini_spec
    ids = [m["id"] for m in spec["models"]]
    assert "video_standard" not in ids
    seedance = next(m for m in spec["models"] if m["id"] == "seedance_2_0")
    assert seedance["aliases"] == ["video_standard"]


def test_fast_mode_constraint_extracted(mini_spec):
    spec, _ = mini_spec
    seedance = next(m for m in spec["models"] if m["id"] == "seedance_2_0")
    cons = [c for c in seedance["constraints"] if c.get("forbids")]
    assert cons, "fast→no-1080p constraint missing"
    assert cons[0]["param"] == "mode"
    assert cons[0]["value"] == "fast"
    assert cons[0]["forbids"] == {"resolution": ["1080p"]}


def test_requires_constraint_extracted(mini_spec):
    spec, _ = mini_spec
    lite = next(m for m in spec["models"] if m["id"] == "veo3_1_lite")
    reqs = [c for c in lite["constraints"] if c.get("requires")]
    assert reqs == [{"param": "resolution", "value": "1080p",
                     "requires": {"duration": "8"},
                     "source": reqs[0]["source"]}]


def test_duration_shapes(mini_spec):
    spec, _ = mini_spec
    by_id = {m["id"]: m for m in spec["models"]}
    assert by_id["kling3_0"]["duration"] == {"min": 3, "max": 15}
    assert by_id["veo3_1_lite"]["duration"] == {"values": [4, 6, 8]}


def test_kling_has_no_21_9(mini_spec):
    spec, _ = mini_spec
    by_id = {m["id"]: m for m in spec["models"]}
    assert "21:9" not in by_id["kling3_0"]["aspect_ratios"]
    assert "21:9" in by_id["seedance_2_0"]["aspect_ratios"]


def test_emit_json_deterministic():
    spec = sync_specs.build_spec(MINI_SNAPSHOT)
    assert sync_specs.emit_json(spec) == sync_specs.emit_json(
        sync_specs.build_spec(MINI_SNAPSHOT))
    assert sync_specs.emit_yaml(spec) == sync_specs.emit_yaml(
        sync_specs.build_spec(MINI_SNAPSHOT))


def test_divergent_alias_rejected(tmp_path):
    snap = json.loads(MINI_SNAPSHOT.read_text(encoding="utf-8"))
    dup = next(m for m in snap["items"] if m["id"] == "video_standard")
    dup["aspect_ratios"] = ["16:9"]  # diverge from canonical seedance_2_0
    bad = tmp_path / "models_explore_snapshot_2026-06-11.json"
    bad.write_text(json.dumps(snap), encoding="utf-8")
    with pytest.raises(ValueError, match="aliases"):
        sync_specs.build_spec(bad)


def test_repo_specs_in_sync():
    """The committed specs/ files must match regeneration from the committed
    snapshot — same gate validate.py enforces, asserted here for pytest runs."""
    import subprocess
    import sys
    result = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "sync_specs.py"), "--check"],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
