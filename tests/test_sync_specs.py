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


def test_empty_snapshot_rejected():
    # A dump with no items (truncated file / wrong payload) must never
    # generate specs — empty specs silently blind every enum check.
    with pytest.raises(ValueError, match="no 'items'"):
        sync_specs.normalize_models({}, "video")
    with pytest.raises(ValueError, match="no 'items'"):
        sync_specs.normalize_models({"items": []}, "video")


def test_wrong_type_snapshot_rejected():
    snap = {"has_more": False, "items": [{"id": "m1", "name": "M1", "output_type": "image",
                                          "parameters": []}]}
    with pytest.raises(ValueError, match="output_type='video'"):
        sync_specs.normalize_models(snap, "video")


def test_divergent_alias_rejected(tmp_path):
    snap = json.loads(MINI_SNAPSHOT.read_text(encoding="utf-8"))
    dup = next(m for m in snap["items"] if m["id"] == "video_standard")
    dup["aspect_ratios"] = ["16:9"]  # diverge from canonical seedance_2_0
    bad = tmp_path / "models_explore_snapshot_2026-06-11.json"
    bad.write_text(json.dumps(snap), encoding="utf-8")
    with pytest.raises(ValueError, match="aliases"):
        sync_specs.build_spec(bad)


@pytest.mark.parametrize("output_type", ["video", "image", "audio", "3d"])
def test_repo_specs_in_sync(output_type):
    """The committed specs/ files of EVERY type must match regeneration from
    that type's newest snapshot — same gate validate.py enforces. (Pre-v3.37
    this ran `--check` with no --type, i.e. video only.)"""
    import subprocess
    import sys
    result = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "sync_specs.py"), "--check",
         "--type", output_type],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_all_four_types_are_wired():
    assert sync_specs.TYPES == ("video", "image", "audio", "3d")
    names = [p.name for p in sync_specs.output_paths("3d")]
    assert names == ["3d-model-specs.yaml", "3d-model-specs.json", "3D-MODEL-SPECS.md"]
    for p in sync_specs.output_paths("3d"):
        assert p.exists(), f"{p.name} not generated"


# ── v3.37.0: paginated partial dumps are refused ─────────────────────────────

@pytest.mark.parametrize("has_more", [True, None, "true", 1])
def test_partial_paginated_dump_refused(has_more):
    snap = json.loads(MINI_SNAPSHOT.read_text(encoding="utf-8"))
    snap["has_more"] = has_more
    with pytest.raises(ValueError, match="has_more"):
        sync_specs.normalize_models(snap, "video")


def test_dump_without_has_more_key_is_refused():
    # Every models_explore list response carries has_more; a dump without
    # the key is hand-trimmed or not a list response — it used to pass.
    snap = json.loads(MINI_SNAPSHOT.read_text(encoding="utf-8"))
    del snap["has_more"]
    with pytest.raises(ValueError, match="<absent>"):
        sync_specs.normalize_models(snap, "video")


def test_every_committed_snapshot_carries_has_more_false():
    for p in sorted((REPO / "specs").glob("models_explore_snapshot_*.json")):
        assert json.loads(p.read_text(encoding="utf-8")).get("has_more", "absent") is False, p.name


def test_complete_dump_accepted():
    snap = json.loads(MINI_SNAPSHOT.read_text(encoding="utf-8"))
    snap["has_more"] = False
    assert sync_specs.normalize_models(snap, "video")


def test_partial_dump_refused_end_to_end(tmp_path):
    snap = json.loads(MINI_SNAPSHOT.read_text(encoding="utf-8"))
    snap["has_more"] = True
    p = tmp_path / "models_explore_snapshot_2026-06-11.json"
    p.write_text(json.dumps(snap), encoding="utf-8")
    with pytest.raises(ValueError, match="has_more"):
        sync_specs.build_spec(p)


# ── v3.37.0: `nullable` is carried; unknown keys still are not ───────────────

def test_nullable_carried_but_keys_not_widened():
    snap = {"has_more": False, "items": [{"id": "m", "name": "M", "output_type": "3d", "parameters": [
        {"name": "seed", "type": "number", "required": "optional", "nullable": True,
         "format": "int32", "pattern": "^x$"}]}]}
    p = sync_specs.normalize_models(snap, "3d")[0]["params"][0]
    assert p["nullable"] is True
    assert "format" not in p and "pattern" not in p


def test_committed_specs_carry_nullable():
    spec = json.loads((REPO / "specs" / "model-specs.json").read_text(encoding="utf-8"))
    s25 = next(m for m in spec["models"] if m["id"] == "seedance_2_5")
    ext = next(p for p in s25["params"] if p["name"] == "extension_mode")
    assert ext.get("nullable") is True


# ── v3.37.0: retired-id tombstones (append-only, order-independent) ──────────

def _snap(path, ids, otype="video"):
    path.write_text(json.dumps({"has_more": False, "items": [
        {"id": i, "name": i, "output_type": otype, "parameters": []} for i in ids]}),
        encoding="utf-8")


def test_retired_id_is_tombstoned_from_snapshot_history(tmp_path):
    _snap(tmp_path / "models_explore_snapshot_2026-08-07.json", ["a", "llm_text"])
    _snap(tmp_path / "models_explore_snapshot_2026-09-26.json", ["a"])
    retired = sync_specs.compute_retired(tmp_path)
    assert retired == {"llm_text": {"type": "video", "last_seen": "2026-08-07",
                                    "last_snapshot": "models_explore_snapshot_2026-08-07.json"}}


def test_tombstones_do_not_depend_on_sync_order(tmp_path):
    # A type whose SPEC has not been generated yet (first-ever 3d sync) must
    # not have its live ids tombstoned when another type is synced first.
    _snap(tmp_path / "models_explore_snapshot_2026-09-26.json", ["v1"])
    _snap(tmp_path / "models_explore_snapshot_3d_2026-09-26.json", ["mesh1"], "3d")
    assert not (tmp_path / "3d-model-specs.json").exists()
    assert sync_specs.compute_retired(tmp_path) == {}


def test_aliases_are_never_tombstoned(tmp_path):
    _snap(tmp_path / "models_explore_snapshot_2026-06-11.json", ["video_standard", "seedance_1_5"])
    _snap(tmp_path / "models_explore_snapshot_2026-09-26.json", ["seedance_2_0"])
    assert sync_specs.compute_retired(tmp_path) == {}


def test_tombstones_are_append_only(tmp_path):
    # A proven tombstone is never rewritten or dropped as history grows —
    # even with a hand-edited last_seen, the committed entry is kept as is.
    _snap(tmp_path / "models_explore_snapshot_2026-08-07.json", ["a", "old_gone"])
    _snap(tmp_path / "models_explore_snapshot_2026-09-26.json", ["a"])
    entry = {"type": "video", "last_seen": "2026-08-07",
             "last_snapshot": "models_explore_snapshot_2026-08-07.json"}
    (tmp_path / sync_specs.RETIRED_FILE).write_text(
        sync_specs.emit_retired({"old_gone": entry}), encoding="utf-8")
    _snap(tmp_path / "models_explore_snapshot_2026-10-10.json", ["a", "b"])
    assert sync_specs.merged_retired(tmp_path) == {"old_gone": entry}
    assert sync_specs.retired_is_stale(tmp_path) is False


@pytest.mark.parametrize("fake,why", [
    ("totally_made_up_model", "no committed models_explore snapshot ever carried it"),
    ("a", "live in a newest snapshot"),
])
def test_a_hand_added_tombstone_is_unproven_and_stale(tmp_path, fake, why):
    # A tombstone whitelists its id in the ledger; a hand-added one used to
    # pass --strict because the stale check started from the committed file.
    _snap(tmp_path / "models_explore_snapshot_2026-08-07.json", ["a", "gone"])
    _snap(tmp_path / "models_explore_snapshot_2026-09-26.json", ["a"])
    good = sync_specs.compute_retired(tmp_path)
    (tmp_path / sync_specs.RETIRED_FILE).write_text(sync_specs.emit_retired(
        {**good, fake: {"type": "video", "last_seen": "2026-08-07",
                        "last_snapshot": "models_explore_snapshot_2026-08-07.json"}}),
        encoding="utf-8")
    assert sync_specs.retired_is_stale(tmp_path) is True
    assert fake not in sync_specs.merged_retired(tmp_path)
    assert fake not in sync_specs.proven_retired(tmp_path)
    assert any(fake in p and why in p for p in sync_specs.retired_problems(tmp_path))


def test_missing_tombstone_is_stale(tmp_path):
    _snap(tmp_path / "models_explore_snapshot_2026-08-07.json", ["a", "gone"])
    _snap(tmp_path / "models_explore_snapshot_2026-09-26.json", ["a"])
    assert sync_specs.retired_is_stale(tmp_path) is True


# ── v3.37.0: a negative duration floor is a sentinel, not a length ───────────

WAN_DESC = ("Duration in seconds (2-30), or -1 to let the model choose the length "
            "from the prompt and media. Smart duration is billed as 10 seconds.")


def _dur_model(desc, lo=-1, hi=30):
    return {"has_more": False, "items": [{"id": "wan3_0", "name": "Wan 3.0", "output_type": "video",
                       "parameters": [{"name": "duration", "type": "number",
                                       "min": lo, "max": hi, "default": 5,
                                       "description": desc}]}]}


def test_smart_duration_floor_derived_from_description():
    m = sync_specs.normalize_models(_dur_model(WAN_DESC), "video")[0]
    assert m["duration"] == {"min": 2, "max": 30, "smart": -1}


@pytest.mark.parametrize("desc", [
    "Duration in seconds, or -1 for smart duration.",          # no stated range
    "Duration in seconds (2-15), or -1 for smart duration.",   # range max != declared max
    "Duration in seconds (2-30).",                             # sentinel never named
])
def test_underivable_floor_is_kept_raw_and_reported(desc, capsys):
    m = sync_specs.normalize_models(_dur_model(desc), "video")[0]
    assert m["duration"] == {"min": -1, "max": 30}             # never guessed
    assert "sentinel" in capsys.readouterr().err


def test_positive_floor_unchanged():
    m = sync_specs.normalize_models(_dur_model("Duration in seconds (4-15).", 4, 15), "video")[0]
    assert m["duration"] == {"min": 4, "max": 15}


def test_smart_duration_rendered_and_committed():
    assert sync_specs._fmt_duration({"min": 2, "max": 30, "smart": -1}) == "2–30s or -1 (smart)"
    spec = json.loads((REPO / "specs" / "model-specs.json").read_text(encoding="utf-8"))
    wan = {m["id"]: m["duration"] for m in spec["models"] if m["id"].startswith("wan3")}
    assert wan == {"wan3_0": {"min": 2, "max": 30, "smart": -1},
                   "wan3_0_prime": {"min": 2, "max": 30, "smart": -1}}
    md = (REPO / "specs" / "MODEL-SPECS.md").read_text(encoding="utf-8")
    assert "| wan3_0 | 2–30s or -1 (smart) |" in md and "-1–30s" not in md


# ── v3.37.0: --changed lists moved models + the eval cases that cite them ────

def test_changed_models_and_referencing_evals(tmp_path):
    specs, cases = tmp_path / "specs", tmp_path / "cases"
    specs.mkdir()
    cases.mkdir()
    _snap(specs / "models_explore_snapshot_2026-08-07.json", ["keep", "move", "gone"])
    new = json.loads((specs / "models_explore_snapshot_2026-08-07.json").read_text())
    new["items"] = [m for m in new["items"] if m["id"] != "gone"]
    next(m for m in new["items"] if m["id"] == "move")["parameters"] = [{"name": "r"}]
    new["items"].append({"id": "fresh", "name": "Fresh Model", "output_type": "video",
                         "parameters": []})
    (specs / "models_explore_snapshot_2026-09-26.json").write_text(json.dumps(new))
    ch = sync_specs.changed_models("video", specs)
    assert (ch["added"], ch["removed"], ch["changed"]) == (["fresh"], ["gone"], ["move"])
    (cases / "a.json").write_text(json.dumps({"cases": [
        {"id": "c1", "response": "uses `move` here"},
        {"id": "c2", "response": "the Fresh Model by display name"},
        {"id": "c3", "response": "mentions move_v2 and keep only"}]}))
    refs = sync_specs.evals_referencing(["move", "fresh", "gone"], ch["names"], cases)
    assert refs == {"move": ["a.json:c1"], "fresh": ["a.json:c2"], "gone": []}


def test_committed_tombstones_include_llm_text():
    retired = sync_specs.load_retired()
    assert {"llm_text", "explainer_video", "gpt_image"} <= set(retired)
    assert sync_specs.retired_is_stale() is False
