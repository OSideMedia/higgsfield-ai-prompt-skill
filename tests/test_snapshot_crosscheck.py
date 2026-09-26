"""snapshot_crosscheck.py — two-way CLI <-> models_explore structural check.

Every test drives main() over RECORDED payloads (--cli-dir), so nothing here
touches the network. The positive control comes first: a snapshot that LACKS
an option the CLI has must exit non-zero — a checker that cannot go red on
that proves nothing.
"""
import json

import pytest

import snapshot_crosscheck as xc


def _write(tmp_path, snap_params, cli_params, snap_aspect=("1:1",), cli_aspect=("1:1",),
           snap_roles=("image_references",), allow=None):
    snap = tmp_path / "models_explore_snapshot_image_2026-09-26.json"
    snap.write_text(json.dumps({"has_more": False, "items": [{
        "id": "m1", "name": "M1", "output_type": "image",
        "aspect_ratios": list(snap_aspect), "parameters": snap_params,
        "medias": [{"name": "medias", "type": "image", "roles": list(snap_roles)}]}]}))
    cli = tmp_path / "cli"
    cli.mkdir()
    (cli / "list_all.json").write_text(json.dumps(
        [{"job_type": "m1", "type": "image", "display_name": "M1"},
         {"job_type": "other_video", "type": "video", "display_name": "V"}]))
    params = list(cli_params)
    if cli_aspect:
        params.append({"name": "aspect_ratio", "type": "string", "default": cli_aspect[0],
                       "required": False, "enum": list(cli_aspect)})
    (cli / "get_m1.json").write_text(json.dumps(
        {"job_type": "m1", "type": "image", "params": params, "rules": []}))
    allowlist = tmp_path / "allow.json"
    allowlist.write_text(json.dumps({"entries": allow or []}))
    return ["--type", "image", "--cli-dir", str(cli), "--snapshot", str(snap),
            "--allowlist", str(allowlist)]


RES_SNAP = [{"name": "resolution", "type": "string", "default": "1k", "options": ["1k", "2k"]}]
ROLE_CLI = [{"name": "image_references", "type": "array", "default": None, "required": False}]


def _cli_res(*opts, default="1k"):
    return [{"name": "resolution", "type": "string", "default": default, "required": False,
             "enum": list(opts)}] + ROLE_CLI


def test_positive_control_snapshot_missing_a_cli_option_fails(tmp_path, capsys):
    argv = _write(tmp_path, RES_SNAP, _cli_res("1k", "2k", "4k"))
    assert xc.main(argv) == 1
    out = capsys.readouterr().out
    assert "m1.resolution [options] snapshot-only=[] cli-only=[4k]" in out


def test_negative_control_identical_sources_pass(tmp_path, capsys):
    argv = _write(tmp_path, RES_SNAP, _cli_res("1k", "2k"))
    assert xc.main(argv) == 0
    assert "agree" in capsys.readouterr().out


@pytest.mark.parametrize("snap_params,cli_params,kwargs,fragment", [
    (RES_SNAP, _cli_res("1k", "2k", default="2k"), {}, "[default] snapshot='1k' cli='2k'"),
    (RES_SNAP + [{"name": "soul_id", "type": "string"}], _cli_res("1k", "2k"), {},
     "m1.soul_id [param_missing_in_cli]"),
    (RES_SNAP, _cli_res("1k", "2k") + [{"name": "background", "type": "string|null",
                                        "default": None, "required": False,
                                        "enum": ["auto", "opaque"]}], {},
     "m1.background [param_missing_in_snapshot] cli enum=[auto, opaque]"),
    (RES_SNAP, _cli_res("1k", "2k"), {"cli_aspect": ("1:1", "auto")},
     "[aspect_ratios] snapshot-only=[] cli-only=[auto]"),
    (RES_SNAP, _cli_res("1k", "2k"), {"cli_aspect": ()},           # one-sided
     "[aspect_ratios] snapshot-only=[1:1] cli-only=[]"),
    (RES_SNAP, _cli_res("1k", "2k"), {"snap_roles": ("image",)},   # role naming
     "[media_roles] snapshot-only=[image] cli-only=[image_references]"),
    (RES_SNAP, _cli_res("1k", "2k") + [{"name": "mask", "type": "object|null",
                                        "default": None, "required": False}], {},
     "[media_roles] snapshot-only=[] cli-only=[mask]"),
])
def test_each_disagreement_kind_is_caught(tmp_path, capsys, snap_params, cli_params,
                                          kwargs, fragment):
    assert xc.main(_write(tmp_path, snap_params, cli_params, **kwargs)) == 1
    assert fragment in capsys.readouterr().out


def _entry(**kw):
    e = {"model": "m1", "field": "resolution", "kind": "options", "seen": "2026-09-26",
         "detail": "snapshot-only=[] cli-only=[4k]"}
    e.update(kw)
    return e


def test_allowlisted_disagreement_passes_but_is_printed(tmp_path, capsys):
    argv = _write(tmp_path, RES_SNAP, _cli_res("1k", "2k", "4k"), allow=[_entry()])
    assert xc.main(argv) == 0
    assert "allowlisted (seen 2026-09-26) m1.resolution [options]" in capsys.readouterr().out


def test_allowlist_pins_the_detail_a_changed_disagreement_fails_again(tmp_path, capsys):
    argv = _write(tmp_path, RES_SNAP, _cli_res("1k", "2k", "4k", "8k"), allow=[_entry()])
    assert xc.main(argv) == 1
    assert "allowlisted detail was" in capsys.readouterr().out


def test_stale_allowlist_entry_is_reported(tmp_path, capsys):
    argv = _write(tmp_path, RES_SNAP, _cli_res("1k", "2k"), allow=[_entry()])
    assert xc.main(argv) == 0
    assert "STALE allowlist entry" in capsys.readouterr().out


@pytest.mark.parametrize("bad", [
    {k: v for k, v in _entry().items() if k != "seen"},
    {k: v for k, v in _entry().items() if k != "model"},
    _entry(seen="last week"),
])
def test_malformed_allowlist_is_a_usage_error(tmp_path, bad):
    argv = _write(tmp_path, RES_SNAP, _cli_res("1k", "2k"), allow=[bad])
    assert xc.main(argv) == 2


def test_committed_allowlist_is_well_formed_and_dated():
    entries = xc.load_allowlist()
    assert entries, "specs/crosscheck_allowlist.json should document the known disagreements"
    for e in entries:
        if e["kind"] in xc.MEMBERSHIP_KINDS:
            continue                  # checked in test_committed_membership_entries_…
        assert e["model"] and e["field"] and e["kind"] and e["detail"]
        assert e["seen"] == "2026-09-26" or len(e["seen"]) == 10
    kinds = {(e["model"], e["kind"]) for e in entries}
    assert ("gpt_image_2", "default") in kinds and ("soul_cinematic", "param_missing_in_cli") in kinds


def test_cli_shape_surprise_exits_3(tmp_path):
    argv = _write(tmp_path, RES_SNAP, _cli_res("1k", "2k"))
    (tmp_path / "cli" / "get_m1.json").write_text(json.dumps(["not", "an", "object"]))
    assert xc.main(argv) == 3


# ── v3.37.0 review: nothing compared is not agreement; membership blocks ────

def _member(model="m2", kind="cli-only", type_="image", **kw):
    e = {"model": model, "kind": kind, "type": type_, "seen": "2026-09-26",
         "note": "CLI-only utility id, verified live"}
    e.update(kw)
    return e


def _add_cli_row(tmp_path, row):
    p = tmp_path / "cli" / "list_all.json"
    rows = json.loads(p.read_text())
    rows.append(row)
    p.write_text(json.dumps(rows))


def test_zero_shared_models_is_unchecked_never_agree(tmp_path, capsys):
    # An empty `model list` used to print "0 shared model(s)" and "agree", exit 0.
    argv = _write(tmp_path, RES_SNAP, _cli_res("1k", "2k"),
                  allow=[_member("m1", "snapshot-only")])
    (tmp_path / "cli" / "list_all.json").write_text("[]")
    assert xc.main(argv) == 3
    out = capsys.readouterr().out
    assert "UNCHECKED" in out and "agree" not in out.split("UNCHECKED")[-1]


def test_rows_without_a_type_are_a_shape_change_not_zero_rows(tmp_path):
    argv = _write(tmp_path, RES_SNAP, _cli_res("1k", "2k"))
    (tmp_path / "cli" / "list_all.json").write_text(json.dumps([{"job_type": "m1"}]))
    assert xc.main(argv) == 3


def test_a_type_without_a_snapshot_is_unchecked(tmp_path, monkeypatch, capsys):
    def no_snapshot(*a, **k):
        raise FileNotFoundError("no snapshot")
    monkeypatch.setattr(xc.sync_specs, "find_snapshot", no_snapshot)
    argv = _write(tmp_path, RES_SNAP, _cli_res("1k", "2k"))
    argv = [a for a in argv]
    i = argv.index("--snapshot")
    del argv[i:i + 2]
    assert xc.main(argv) == 3
    assert "UNCHECKED" in capsys.readouterr().out


def test_catalog_membership_difference_fails_unless_allowlisted(tmp_path, capsys):
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    argv = _write(tmp_path / "a", RES_SNAP, _cli_res("1k", "2k"))
    _add_cli_row(tmp_path / "a", {"job_type": "m2", "type": "image", "display_name": "M2"})
    assert xc.main(argv) == 1
    assert "m2.membership [cli-only]" in capsys.readouterr().out
    argv = _write(tmp_path / "b", RES_SNAP, _cli_res("1k", "2k"), allow=[_member()])
    _add_cli_row(tmp_path / "b", {"job_type": "m2", "type": "image", "display_name": "M2"})
    assert xc.main(argv) == 0
    assert "allowlisted (seen 2026-09-26) m2 [cli-only]" in capsys.readouterr().out


def test_membership_entry_is_per_kind_and_type(tmp_path):
    # allowlisted as snapshot-only, observed cli-only → still blocking
    argv = _write(tmp_path, RES_SNAP, _cli_res("1k", "2k"),
                  allow=[_member(kind="snapshot-only")])
    _add_cli_row(tmp_path, {"job_type": "m2", "type": "image", "display_name": "M2"})
    assert xc.main(argv) == 1


def test_stale_membership_and_never_checked_entries_are_reported(tmp_path, capsys):
    ghost = _entry(model="ghost_model")      # a structural entry nobody compared
    argv = _write(tmp_path, RES_SNAP, _cli_res("1k", "2k"), allow=[_member(), ghost])
    _add_cli_row(tmp_path, {"job_type": "ghost_model", "type": "image", "display_name": "G"})
    assert xc.main(argv) == 1          # ghost_model is now an unadjudicated cli-only id
    out = capsys.readouterr().out
    assert "STALE allowlist entry — no longer disagrees, remove it: m2 [cli-only]" in out
    assert "STALE allowlist entry — its model was not compared this run, remove it: " \
           "ghost_model.resolution [options]" in out


@pytest.mark.parametrize("bad", [
    {k: v for k, v in _member().items() if k != "note"},
    {k: v for k, v in _member().items() if k != "type"},
    _member(type_="hologram"),
])
def test_malformed_membership_entry_is_a_usage_error(tmp_path, bad):
    argv = _write(tmp_path, RES_SNAP, _cli_res("1k", "2k"), allow=[bad])
    assert xc.main(argv) == 2


def test_committed_membership_entries_carry_type_and_reason():
    members = [e for e in xc.load_allowlist() if e["kind"] in xc.MEMBERSHIP_KINDS]
    got = {(e["model"], e["kind"], e["type"]) for e in members}
    assert {("depth_anything_video", "cli-only", "video"), ("fps_boost", "cli-only", "video"),
            ("sync_so", "snapshot-only", "video"), ("soul_2", "snapshot-only", "image"),
            ("nano_banana_flash", "cli-only", "image")} <= got
    for e in members:
        assert len(e["note"]) > 40 and "Verified" in e["note"], e
