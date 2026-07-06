"""Spec-drift tripwire (refresh_specs.py, Wave C Tier 1) — pure-function tests.

The diff's whole value is its severity classification: a NEW live capability the
snapshot lacks is DRIFT (the Seedance-4K staleness case); the CLI reporting LESS
than the snapshot (enum:null, missing params/models) is NOTICE, not drift —
because the two sources diverge in detail and a removal-shaped signal is usually
the CLI under-reporting, not a real withdrawal.
"""
import json
from pathlib import Path

import pytest

import refresh_specs as r

FIXTURES = Path(__file__).parent / "fixtures"


# ── Normalization: both sources collapse to one comparable shape ─────────────

def test_snapshot_view_normalizes_options_and_aspect():
    item = {"id": "seedance_2_0", "output_type": "video",
            "aspect_ratios": ["16:9", "21:9"],
            "parameters": [{"name": "resolution", "type": "string",
                            "default": "720p", "options": ["720p", "1080p", "4k"]}]}
    v = r.snapshot_view(item)
    assert v["id"] == "seedance_2_0"
    assert v["aspect_ratios"] == ["16:9", "21:9"]
    assert v["params"]["resolution"]["options"] == ["1080p", "4k", "720p"]  # sorted
    assert v["params"]["resolution"]["default"] == "720p"


def test_cli_view_maps_enum_and_aspect_param():
    get = {"job_set_type": "seedance_2_0", "type": "video",
           "params": [{"name": "aspect_ratio", "enum": ["16:9", "21:9"]},
                      {"name": "resolution", "default": "720p",
                       "enum": ["720p", "1080p", "4k"]}]}
    v = r.cli_view(get)
    assert v["id"] == "seedance_2_0"
    assert v["aspect_ratios"] == ["16:9", "21:9"]          # from aspect_ratio param
    assert v["params"]["resolution"]["options"] == ["1080p", "4k", "720p"]


# ── CLI 1.0.1 shape: `job_type` rename, enum-less params, CEL rules ───────────
# Recorded fixtures from `higgsfield 1.0.1 (2dae25b)` — the release whose
# `job_set_type` → `job_type` rename crashed the tripwire (KeyError masquerading
# as auth expiry). Any future output-shape change should fail HERE, not in CI.

def test_cli_view_accepts_1_0_1_job_type_fixture():
    get = json.loads((FIXTURES / "cli_1_0_1_model_get_seedance_2_0.json").read_text())
    v = r.cli_view(get)
    assert v["id"] == "seedance_2_0"
    assert v["output_type"] == "video"
    assert "generate_audio" in v["params"]
    # 1.0.1 dropped per-param enums; the view must degrade, not crash
    assert v["params"]["resolution"]["options"] == []
    # ...and the new CEL rules channel must be captured
    assert any("4k" in rule or "1080p" in rule for rule in v["rules"])


def test_model_id_accepts_both_key_generations():
    assert r._model_id({"job_type": "a"}, "t") == "a"
    assert r._model_id({"job_set_type": "b"}, "t") == "b"
    assert r._model_id({"job_type": "a", "job_set_type": "b"}, "t") == "a"  # newest wins


def test_model_id_raises_shape_error_not_key_error():
    with pytest.raises(r.ShapeError, match="shape changed"):
        r._model_id({"model_identifier": "x"}, "model list --video")


def test_cli_view_legacy_job_set_type_still_works():
    v = r.cli_view({"job_set_type": "m", "type": "video", "params": []})
    assert v["id"] == "m" and v["rules"] == []


# ── CEL rules channel: both-sides-present only, added=drift, removed=notice ──

def test_rules_added_is_drift_when_both_sides_carry_rules():
    old = dict(_view([], {}), rules=["size(params.video_references) <= 3"])
    new = dict(_view([], {}), rules=["size(params.video_references) <= 3",
                                     "size(params.video_references) <= 5"])
    d = r.diff_model(old, new)
    assert d["drift"] == [{"kind": "rules_added",
                           "added": ["size(params.video_references) <= 5"]}]


def test_rules_removed_is_notice():
    old = dict(_view([], {}), rules=["a", "b"])
    new = dict(_view([], {}), rules=["a"])
    d = r.diff_model(old, new)
    assert d["drift"] == []
    assert d["notice"] == [{"kind": "rules_removed", "removed": ["b"]}]


def test_missing_rules_channel_never_alarms():
    # snapshot views and pre-1.0.1 baselines have no `rules` key — silence
    old = _view([], {})                      # no rules key
    new = dict(_view([], {}), rules=["a"])   # CLI now reports rules
    assert r.diff_model(old, new) == {"drift": [], "notice": []}


def test_pull_cli_views_end_to_end_on_1_0_1_fixtures(monkeypatch):
    catalog = json.loads((FIXTURES / "cli_1_0_1_model_list_video.json").read_text())
    get = json.loads((FIXTURES / "cli_1_0_1_model_get_seedance_2_0.json").read_text())

    def fake_cli_json(args):
        return catalog if args[:2] == ["model", "list"] else get

    monkeypatch.setattr(r, "_cli_json", fake_cli_json)
    views, catalog_ids = r.pull_cli_views("video", ids={"seedance_2_0"})
    assert "seedance_2_0" in catalog_ids          # job_type rows parsed
    assert views["seedance_2_0"]["id"] == "seedance_2_0"
    assert views["seedance_2_0"]["rules"]         # CEL rules captured


def test_pull_cli_views_non_list_catalog_is_shape_error(monkeypatch):
    monkeypatch.setattr(r, "_cli_json", lambda args: {"error": "new envelope"})
    with pytest.raises(r.ShapeError, match="expected a JSON array"):
        r.pull_cli_views("video", ids=None)


def _view(aspect, params):
    return {"id": "m", "output_type": "video", "aspect_ratios": sorted(aspect),
            "params": params}


# ── DRIFT: a new live capability the snapshot lacks ──────────────────────────

def test_new_enum_option_is_drift():
    old = _view(["16:9"], {"resolution": {"options": ["720p", "1080p"], "default": "720p"}})
    new = _view(["16:9"], {"resolution": {"options": ["720p", "1080p", "4k"], "default": "720p"}})
    d = r.diff_model(old, new)
    assert d["drift"] == [{"kind": "options_added", "param": "resolution", "added": ["4k"]}]
    assert d["notice"] == []


def test_new_aspect_ratio_is_drift():
    old = _view(["16:9"], {})
    new = _view(["16:9", "21:9"], {})
    d = r.diff_model(old, new)
    assert d["drift"] == [{"kind": "aspect_ratios", "added": ["21:9"]}]


def test_default_change_is_drift():
    old = _view([], {"resolution": {"options": ["1k", "2k"], "default": "1k"}})
    new = _view([], {"resolution": {"options": ["1k", "2k"], "default": "2k"}})
    d = r.diff_model(old, new)
    assert d["drift"] == [{"kind": "default", "param": "resolution", "from": "1k", "to": "2k"}]


# ── NOTICE: CLI under-reporting must NOT flip the drift state ─────────────────

def test_option_removed_is_notice_not_drift():
    # snapshot enumerates more than the CLI (e.g. clipify fonts: CLI enum=null)
    old = _view([], {"font": {"options": ["inter", "bangers"], "default": None}})
    new = _view([], {"font": {"options": [], "default": None}})  # CLI enum:null → []
    d = r.diff_model(old, new)
    assert d["drift"] == []
    assert d["notice"] == [{"kind": "options_undetailed", "param": "font"}]


def test_both_enumerate_but_cli_dropped_one_is_notice():
    old = _view([], {"mode": {"options": ["std", "fast", "turbo"], "default": "std"}})
    new = _view([], {"mode": {"options": ["std", "fast"], "default": "std"}})
    d = r.diff_model(old, new)
    assert d["drift"] == []
    assert d["notice"] == [{"kind": "options_removed", "param": "mode", "removed": ["turbo"]}]


def test_param_missing_from_cli_is_notice():
    old = _view([], {"resolution": {"options": ["720p"], "default": "720p"}})
    new = _view([], {})
    d = r.diff_model(old, new)
    assert d["drift"] == []
    assert d["notice"] == [{"kind": "param_missing", "param": "resolution"}]


def test_aspect_removed_is_notice():
    old = _view(["16:9", "21:9"], {})
    new = _view(["16:9"], {})
    d = r.diff_model(old, new)
    assert d["drift"] == []
    assert d["notice"] == [{"kind": "aspect_ratios_gone", "removed": ["21:9"]}]


def test_identical_views_are_clean():
    v = _view(["16:9"], {"resolution": {"options": ["720p", "4k"], "default": "720p"}})
    assert r.diff_model(v, dict(v)) == {"drift": [], "notice": []}


# ── Catalog level: membership is notice, added capability is drift ───────────

def test_catalog_membership_is_notice_not_drift():
    old = {"a": _view([], {}), "b": _view([], {})}      # snapshot tracks a, b
    new = {"a": _view([], {}), "c": _view([], {})}      # CLI has a, c
    diff = r.diff_catalog(old, new)
    assert diff["models_removed"] == ["b"]   # snapshot-only → notice
    assert diff["models_added"] == ["c"]     # CLI-only (new/utility) → notice
    assert r.has_drift(diff) is False        # membership alone is NOT drift


def test_catalog_surfaces_shared_model_drift():
    old = {"a": _view(["16:9"], {})}
    new = {"a": _view(["16:9", "21:9"], {}), "util": _view([], {})}
    diff = r.diff_catalog(old, new)
    assert r.has_drift(diff) is True
    assert diff["models_changed"]["a"]["drift"][0]["kind"] == "aspect_ratios"


# ── v2 self-diff: any_change counts EVERY difference (both sides are the CLI) ──

def test_any_change_false_when_identical():
    v = {"a": _view(["16:9"], {"r": {"options": ["720p"], "default": "720p"}})}
    assert r.any_change(r.diff_catalog(v, {k: dict(x) for k, x in v.items()})) is False


def test_any_change_true_on_new_model():
    old = {"a": _view([], {})}
    new = {"a": _view([], {}), "b": _view([], {})}
    assert r.any_change(r.diff_catalog(old, new)) is True


def test_any_change_true_on_removed_model():
    old = {"a": _view([], {}), "b": _view([], {})}
    new = {"a": _view([], {})}
    assert r.any_change(r.diff_catalog(old, new)) is True


def test_any_change_true_on_a_notice_that_has_drift_false():
    # an option REMOVED is a notice (has_drift False) but a real CLI change
    # (any_change True) — this is the whole point of the self-diff vs snapshot-diff
    old = {"a": _view([], {"mode": {"options": ["std", "fast", "turbo"], "default": "std"}})}
    new = {"a": _view([], {"mode": {"options": ["std", "fast"], "default": "std"}})}
    diff = r.diff_catalog(old, new)
    assert r.has_drift(diff) is False   # snapshot-diff would stay quiet
    assert r.any_change(diff) is True   # self-diff catches it
