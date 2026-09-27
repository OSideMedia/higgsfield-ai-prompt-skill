"""Spec-drift tripwire (refresh_specs.py, Wave C Tier 1) — pure-function tests.

The diff's whole value is its severity classification: a NEW live capability the
snapshot lacks is DRIFT (the Seedance-4K staleness case); the CLI reporting LESS
than the snapshot (enum:null, missing params/models) is NOTICE, not drift —
because the two sources diverge in detail and a removal-shaped signal is usually
the CLI under-reporting, not a real withdrawal.
"""
import json
import re
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


# ── v3.37.0: the diff walks the UNION of params + extended fields ────────────
# Pre-fix, diff_model walked only the OLD view's params and cli_view kept only
# enum+default: seedance_2_5 gained start_image/end_image/bitrate_mode between
# the 08-07 baseline and 09-26 and the tripwire never said so.

def _v2(params, aspect=()):
    return {"id": "m", "view": 2, "output_type": "video",
            "aspect_ratios": sorted(aspect), "params": params}


def _p(**kw):
    base = {"options": [], "default": None, "type": "string", "required": False}
    base.update(kw)
    return base


def test_new_param_is_change_even_against_old_format_baseline():
    old = _view([], {"prompt": {"options": [], "default": None}})          # pre-v3.37 shape
    new = _v2({"prompt": _p(required=True),
               "enable_thinking": _p(type="boolean", default=False)})
    d = r.diff_model(old, new)
    assert [c["kind"] for c in d["drift"]] == ["param_added"]
    assert d["drift"][0]["param"] == "enable_thinking"
    assert r.any_change(r.diff_catalog({"m": old}, {"m": new})) is True


def test_new_media_role_param_is_reported_as_media_role():
    old = _view([], {"prompt": {"options": [], "default": None}})
    new = _v2({"prompt": _p(), "start_image": _p(type="object|null")})
    d = r.diff_model(old, new)
    assert d["drift"] == [{"kind": "media_role_added", "param": "start_image",
                           "type": "object|null", "required": False}]


def test_media_role_param_gone_is_media_role_removed():
    old = _v2({"prompt": _p(), "mask": _p(type="object|null")})
    new = _v2({"prompt": _p()})
    d = r.diff_model(old, new)
    assert d["notice"] == [{"kind": "media_role_removed", "param": "mask"}]


@pytest.mark.parametrize("field,before,after", [
    ("type", "object|null", "array"),          # single image -> a list of images
    ("required", False, True),                 # optional -> required flip
    ("min", None, 2),                          # a range appears
    ("max", 15, 30),                           # a range widens
])
def test_extended_field_change_is_drift(field, before, after):
    op, np = _p(), _p()
    if before is not None:
        op[field] = before
    np[field] = after
    d = r.diff_model(_v2({"x": op}), _v2({"x": np}))
    assert d["drift"] == [{"kind": f"{field}_changed", "param": "x",
                           "from": before, "to": after}]
    assert r.any_change(r.diff_catalog({"m": _v2({"x": op})}, {"m": _v2({"x": np})}))


def test_old_format_baseline_never_false_alarms_on_unrecorded_fields():
    # The committed pre-v3.37 baseline has no type/required — the same params
    # with the same enum/default must read as unchanged, not as "type" drift.
    old = _view(["16:9"], {"resolution": {"options": ["720p"], "default": "720p"}})
    new = _v2({"resolution": _p(options=["720p"], default="720p")}, ["16:9"])
    assert r.diff_model(old, new) == {"drift": [], "notice": []}


def test_snapshot_view_never_counts_cli_only_params_as_added():
    # models_explore keeps aspect ratios + media roles outside `parameters`;
    # against a snapshot view the CLI "adding" them is representation.
    snap = r.snapshot_view({"id": "m", "output_type": "video", "aspect_ratios": ["16:9"],
                            "parameters": [{"name": "resolution", "options": ["720p"]}]})
    cli = _v2({"resolution": _p(options=["720p"]), "aspect_ratio": _p(options=["16:9"]),
               "start_image": _p(type="object|null")}, ["16:9"])
    assert r.diff_model(snap, cli)["drift"] == []


def test_recorded_08_07_baseline_vs_live_1_1_23_reports_the_missed_params():
    """End to end on recorded data: the committed 08-07 baseline entries vs the
    live CLI 1.1.23 payloads the pre-fix tripwire compared them to."""
    base = json.loads((FIXTURES / "cli_baseline_2026-08-07_excerpt.json").read_text())
    live_s = r.cli_view(json.loads(
        (FIXTURES / "cli_1_1_23_model_get_seedance_2_5.json").read_text()))
    live_g = r.cli_view(json.loads(
        (FIXTURES / "cli_1_1_23_model_get_gpt_image_2.json").read_text()))
    ds = r.diff_model(base["video"]["seedance_2_5"], live_s)
    added = {(c["kind"], c["param"]) for c in ds["drift"]
             if c["kind"] in ("param_added", "media_role_added")}
    assert added == {("media_role_added", "start_image"), ("media_role_added", "end_image"),
                     ("param_added", "bitrate_mode")}
    dg = r.diff_model(base["image"]["gpt_image_2"], live_g)
    added_g = {c["param"] for c in dg["drift"] if c["kind"] in ("param_added", "media_role_added")}
    assert added_g == {"background", "is_inpaint", "mask"}
    text = r.render_self_diff("video", base, r.diff_catalog(
        base["video"], {"seedance_2_5": live_s}))
    assert "new media role: start_image" in text and "new param: bitrate_mode" in text


def test_cli_view_v2_carries_type_and_required():
    v = r.cli_view(json.loads((FIXTURES / "cli_1_1_23_model_get_seedance_2_5.json").read_text()))
    assert v["view"] == 2
    assert v["params"]["prompt"]["required"] is True
    assert v["params"]["start_image"]["type"] == "object|null"
    assert "min" not in v["params"]["duration"]      # absent upstream -> not invented


def test_describe_never_renders_a_change_as_nothing():
    for c in ({"kind": "param_added", "param": "p"},
              {"kind": "type_changed", "param": "p", "from": "a", "to": "b"},
              {"kind": "some_future_kind", "x": 1}):
        lines = r.describe("m", c)
        assert lines and all(line.strip() for line in lines)


# ── v3.37.0: shape surprises are ShapeError (exit 4), never a fake auth error ─

@pytest.mark.parametrize("payload,fragment", [
    ({"job_type": "m", "type": "video", "params": [], "rules": None}, "`rules` is NoneType"),
    (["not", "an", "object"], "payload is list"),
    ("plain string", "payload is str"),
    ({"job_type": "m", "params": None}, "`params` is NoneType"),
    ({"job_type": "m", "params": [{"type": "string"}]}, "not an object with a name"),
    ({"job_type": "m", "params": [{"name": "r", "enum": "720p,1080p"}]}, "enum is str"),
    ({"job_type": "m", "params": [], "rules": [{"note": "x"}]}, "neither `cel` nor `message`"),
])
def test_cli_view_shape_surprises_are_shape_errors(payload, fragment):
    with pytest.raises(r.ShapeError, match=re.escape(fragment)):
        r.cli_view(payload)


@pytest.mark.parametrize("payload", [
    {"job_type": "m", "type": "video", "params": [], "rules": None},
    ["a list, not an object"],
])
def test_main_exits_4_not_1_on_shape_surprise(monkeypatch, tmp_path, payload):
    catalog = [{"job_type": "m", "type": "video"}]
    monkeypatch.setattr(r, "_cli_json",
                        lambda args: catalog if args[:2] == ["model", "list"] else payload)
    monkeypatch.setattr(r, "load_baseline", lambda: {"captured": "x", "video": {}})
    assert r.main(["--type", "video"]) == 4


# ── v3.37.0: pull failures are CLASSIFIED from the CLI's own stderr ──────────

@pytest.mark.parametrize("stderr,kind", [
    ("Error: No workspace selected.\n", "workspace"),
    ("Session expired. Please run `higgsfield auth login`.\n", "auth"),
    ("Error: 401 Unauthorized\n", "auth"),
    ("Error: upstream timeout contacting api\n", "other"),
])
def test_classify_cli_failure(stderr, kind):
    assert r.classify_cli_failure(stderr) == kind


class _Proc:
    def __init__(self, code, out="", err=""):
        self.returncode, self.stdout, self.stderr = code, out, err


@pytest.mark.parametrize("stderr,kind,remedy_word", [
    ("Error: No workspace selected.\n", "workspace", "HIGGSFIELD_WORKSPACE_ID"),
    ("Session expired\n", "auth", "HIGGSFIELD_CREDENTIALS"),
    ("Error: something new\n", "other", "unrecognized"),
])
def test_main_pull_failure_carries_kind_verbatim_line_and_remedy(
        monkeypatch, tmp_path, capsys, stderr, kind, remedy_word):
    monkeypatch.setattr(r.shutil, "which", lambda name: "/usr/bin/higgsfield")
    monkeypatch.setattr(r.subprocess, "run", lambda *a, **k: _Proc(1, "", stderr))
    monkeypatch.setattr(r, "load_baseline", lambda: {"captured": "x", "video": {}})
    out = tmp_path / "status.json"
    assert r.main(["--type", "video", "--status-json", str(out)]) == 1
    st = json.loads(out.read_text())
    assert st["kind"] == kind
    assert st["line"] == stderr.strip()           # verbatim, not paraphrased
    assert remedy_word in st["remedy"]
    err = capsys.readouterr().err
    assert f"kind={kind}" in err and stderr.strip() in err
    if kind != "auth":
        assert "auth login" not in err            # never the old blanket advice


def test_missing_baseline_type_is_classified_no_baseline(monkeypatch, tmp_path):
    monkeypatch.setattr(r, "load_baseline", lambda: {"captured": "x", "video": {}})
    out = tmp_path / "s.json"
    assert r.main(["--type", "3d", "--status-json", str(out)]) == 1
    assert json.loads(out.read_text())["kind"] == "no-baseline"


def test_fresh_and_changed_write_status(monkeypatch, tmp_path):
    get = json.loads((FIXTURES / "cli_1_1_23_model_get_seedance_2_5.json").read_text())
    view = r.cli_view(get)
    monkeypatch.setattr(r, "_cli_json",
                        lambda args: [{"job_type": "seedance_2_5", "type": "video"}]
                        if args[:2] == ["model", "list"] else get)
    monkeypatch.setattr(r, "load_baseline",
                        lambda: {"captured": "x", "video": {"seedance_2_5": view}})
    out = tmp_path / "s.json"
    assert r.main(["--type", "video", "--status-json", str(out)]) == 0
    assert json.loads(out.read_text())["state"] == "fresh"
    older = json.loads(json.dumps(view))
    del older["params"]["start_image"]            # baseline predates start_image
    monkeypatch.setattr(r, "load_baseline",
                        lambda: {"captured": "x", "video": {"seedance_2_5": older}})
    assert r.main(["--type", "video", "--status-json", str(out)]) == 3
    assert json.loads(out.read_text())["state"] == "changed"


# ── v3.37.0: 3d — no CLI list flag; rows selected by their own `type` ────────

def test_3d_pull_uses_unfiltered_list_and_type_field(monkeypatch):
    rows = json.loads((FIXTURES / "cli_1_1_23_model_list_all_excerpt.json").read_text())
    seen = []

    def fake(args):
        seen.append(args)
        if args[:2] == ["model", "list"]:
            return rows
        return {"job_type": args[2], "type": "3d", "params": [], "rules": []}

    monkeypatch.setattr(r, "_cli_json", fake)
    views, ids = r.pull_cli_views("3d")
    assert seen[0] == ["model", "list"]                      # no invented --3d flag
    assert set(ids) == {"meshy_v6_text_to_3d", "tripo_3d"}   # data/video/image rows excluded


def test_3d_rows_without_type_field_are_shape_error(monkeypatch):
    monkeypatch.setattr(r, "_cli_json", lambda args: [{"job_type": "a"}])
    with pytest.raises(r.ShapeError, match="no `type` field"):
        r.pull_cli_views("3d")


def test_all_types_include_3d():
    assert r.TYPES == ("video", "image", "audio", "3d")


# ── v3.37.0 review: empty pulls, default appear/vanish, crashes, dates, redaction ──

def _cli_view_with_default(default):
    return {"id": "m", "view": 2, "output_type": "video", "aspect_ratios": [],
            "params": {"resolution": {"options": ["720p", "1080p"], "default": default,
                                      "type": "string", "required": False}},
            "rules": []}


@pytest.mark.parametrize("old,new", [(None, "720p"), ("720p", None)])
def test_a_default_that_appears_or_vanishes_is_a_change(old, new):
    # preflight fills omitted params from the baseline defaults, so a default
    # appearing/disappearing changes verdicts — it used to be invisible.
    d = r.diff_model(_cli_view_with_default(old), _cli_view_with_default(new))
    assert {"kind": "default", "param": "resolution", "from": old, "to": new} in d["drift"]
    assert r.any_change({"models_added": [], "models_removed": [],
                         "models_changed": {"m": d}})


def test_cross_source_default_gap_is_still_not_drift():
    snap = {"id": "m", "source": "snapshot", "aspect_ratios": [],
            "params": {"resolution": {"options": ["720p"], "default": None}}}
    cli = _cli_view_with_default("720p")
    assert [c for c in r.diff_model(snap, cli)["drift"] if c["kind"] == "default"] == []


@pytest.fixture
def tmp_baseline(tmp_path, monkeypatch):
    path = tmp_path / "cli_baseline.json"
    monkeypatch.setattr(r, "BASELINE_PATH", path)
    return path


def test_update_baseline_refuses_an_empty_pull(monkeypatch, tmp_baseline, tmp_path):
    tmp_baseline.write_text(json.dumps({"captured": "2026-09-26", "video": {"m": {}}}))
    before = tmp_baseline.read_text()
    monkeypatch.setattr(r, "_cli_json", lambda args: [])
    out = tmp_path / "s.json"
    assert r.main(["--update-baseline", "--type", "video", "--status-json", str(out)]) == 1
    assert tmp_baseline.read_text() == before          # nothing accepted
    assert json.loads(out.read_text())["kind"] == "empty"


def test_an_empty_3d_selection_is_refused_too(monkeypatch):
    monkeypatch.setattr(r, "_cli_json", lambda args: [{"job_type": "v", "type": "video"}])
    with pytest.raises(r.PullError) as e:
        r.pull_cli_views("3d")
    assert e.value.kind == "empty"


def test_partial_recapture_keeps_each_types_own_date(monkeypatch, tmp_baseline):
    from datetime import date
    tmp_baseline.write_text(json.dumps({"captured": "2026-08-07", "video": {},
                                        "image": {"i": {"id": "i"}}}))
    get = json.loads((FIXTURES / "cli_1_1_23_model_get_seedance_2_5.json").read_text())
    monkeypatch.setattr(r, "_cli_json",
                        lambda args: [{"job_type": "seedance_2_5", "type": "video"}]
                        if args[:2] == ["model", "list"] else get)
    assert r.main(["--update-baseline", "--type", "video"]) == 0
    doc = json.loads(tmp_baseline.read_text())
    today = date.today().isoformat()
    assert doc["captured_by_type"] == {"video": today, "image": "2026-08-07"}
    assert doc["captured"] == "2026-08-07"            # the oldest view's date
    assert doc["image"] == {"i": {"id": "i"}} and "seedance_2_5" in doc["video"]


def test_a_crash_is_exit_5_not_a_pull_failure(monkeypatch, tmp_path, capsys):
    def boom():
        raise KeyError("specs")
    monkeypatch.setattr(r, "load_baseline", boom)
    out = tmp_path / "s.json"
    assert r.main(["--type", "video", "--status-json", str(out)]) == 5
    st = json.loads(out.read_text())
    assert (st["code"], st["state"], st["kind"]) == (5, "crashed", "crash")
    assert "Traceback" in capsys.readouterr().err


def test_cli_line_is_redacted_before_it_reaches_status_or_logs(monkeypatch, tmp_path, capsys):
    stderr = ("Error: session expired for peter@example.com "
              "(token=abcdef0123456789abcdef0123) workspace 3f2b1c9e-1111-2222-3333-444455556666\n")
    monkeypatch.setattr(r.shutil, "which", lambda name: "/usr/bin/higgsfield")
    monkeypatch.setattr(r.subprocess, "run", lambda *a, **k: _Proc(1, "", stderr))
    monkeypatch.setattr(r, "load_baseline", lambda: {"captured": "x", "video": {}})
    out = tmp_path / "s.json"
    assert r.main(["--type", "video", "--status-json", str(out)]) == 1
    st = json.loads(out.read_text())
    printed = capsys.readouterr().err + out.read_text()
    for secret in ("peter@example.com", "abcdef0123456789abcdef0123",
                   "3f2b1c9e-1111-2222-3333-444455556666"):
        assert secret not in printed
    assert st["kind"] == "auth" and "<email>" in st["line"]


@pytest.mark.parametrize("text", ['Error: No model with job_type "nano_banana_2_skin_enhancer"',
                                  "Error: No workspace selected."])
def test_redaction_keeps_model_ids_and_plain_errors(text):
    assert r.redact(text) == text
