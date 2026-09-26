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
        assert e["model"] and e["field"] and e["kind"] and e["detail"]
        assert e["seen"] == "2026-09-26" or len(e["seen"]) == 10
    kinds = {(e["model"], e["kind"]) for e in entries}
    assert ("gpt_image_2", "default") in kinds and ("soul_cinematic", "param_missing_in_cli") in kinds


def test_cli_shape_surprise_exits_3(tmp_path):
    argv = _write(tmp_path, RES_SNAP, _cli_res("1k", "2k"))
    (tmp_path / "cli" / "get_m1.json").write_text(json.dumps(["not", "an", "object"]))
    assert xc.main(argv) == 3
