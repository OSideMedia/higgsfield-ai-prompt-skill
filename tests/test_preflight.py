"""scripts/preflight.py — the any-model platform-constraint preflight.

Three things are proven here:
  * coverage: every rule in the committed specs/cli_baseline.json parses, and
    the coverage check itself goes RED on a planted unparseable rule;
  * truth tables: the live 2026-09-26 Seedance 2.5 rules (fixture captured
    verbatim from `higgsfield model get seedance_2_5 --json`) — start_image in
    t2v FAILs, in omni_reference PASSes, 31 image refs FAIL;
  * fail-closed: a rule the evaluator can't parse or evaluate is UNCHECKED,
    and --strict turns UNCHECKED into a non-zero exit — never a silent pass.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

import preflight as pf

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "preflight.py"
BASELINE = REPO / "specs" / "cli_baseline.json"
LIVE = Path(__file__).parent / "fixtures" / "cli_rules_live_2026-09-26.json"


@pytest.fixture(scope="module")
def live():
    return pf.load_baseline(LIVE)


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                          capture_output=True, text=True)


def verdict(live, model, params, media=None):
    return pf.run_preflight(model, params, media or {}, baseline=live).verdict()


# ── Coverage: every committed rule parses; the gate can go red ─────────────

def test_every_committed_baseline_rule_parses():
    baseline = pf.load_baseline(BASELINE)
    total = sum(len(r) for r in baseline["rules"].values())
    assert total > 0, "baseline carries no rules — the coverage check is vacuous"
    bad = pf.check_rule_coverage(baseline)
    assert bad == [], "unparseable baseline rules (extend the CEL subset or " \
                      "accept them as UNCHECKED deliberately):\n" + \
        "\n".join(f"{m}: {c} — {e}" for m, c, e in bad)


def test_every_live_fixture_rule_parses(live):
    assert pf.check_rule_coverage(live) == []
    assert sum(len(r) for r in live["rules"].values()) >= 20


def test_coverage_check_goes_red_on_a_planted_rule(tmp_path):
    doc = json.loads(BASELINE.read_text(encoding="utf-8"))
    doc["video"]["seedance_2_5"]["rules"].append('params.prompt.startsWith("A")')
    planted = tmp_path / "cli_baseline.json"
    planted.write_text(json.dumps(doc), encoding="utf-8")
    bad = pf.check_rule_coverage(pf.load_baseline(planted))
    assert [(m, c) for m, c, _ in bad] == [("seedance_2_5", 'params.prompt.startsWith("A")')]
    strict = run("--check-rules", "--strict", "--baseline", str(planted))
    assert strict.returncode == 1 and "UNCHECKED" in strict.stdout
    lenient = run("--check-rules", "--baseline", str(planted))
    assert lenient.returncode == 0 and "UNCHECKED" in lenient.stdout
    clean = run("--check-rules", "--strict", "--baseline", str(BASELINE))
    assert clean.returncode == 0, clean.stdout


def test_new_baseline_sections_are_read(tmp_path):
    # A regenerated baseline that grows a catalog (3D) must be covered
    # without an edit to preflight.py — sections are discovered, not listed.
    b = pf.load_baseline(LIVE)
    assert "meshy_v6_text_to_3d" in b["rules"] and b["sections"]["meshy_v6_text_to_3d"] == "3d"


def test_no_python_eval():
    import ast
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
    calls = {n.func.id for n in ast.walk(tree)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    assert not calls & {"eval", "exec", "compile", "__import__"}
    # The detector itself must be able to go red.
    planted = ast.parse("x = eval('1')")
    assert any(isinstance(n, ast.Call) and getattr(n.func, "id", "") == "eval"
               for n in ast.walk(planted))


# ── Seedance 2.5 truth tables (live 2026-09-26 rules) ───────────────────────

@pytest.mark.parametrize("mode,media,expected", [
    ("t2v", {"start_image": 1}, "FAIL"),
    ("t2v", {}, "PASS"),
    ("omni_reference", {"start_image": 1}, "PASS"),
    ("omni_reference", {"start_image": 1, "end_image": 1}, "PASS"),
    ("omni_reference", {}, "FAIL"),                       # needs ≥1 reference
    ("omni_reference", {"image_references": 31}, "FAIL"),
    ("omni_reference", {"image_references": 30}, "PASS"),
    ("omni_reference", {"image_references": 29, "start_image": 1}, "PASS"),
    ("omni_reference", {"image_references": 30, "start_image": 1}, "FAIL"),
    ("omni_reference", {"image_references": 30, "video_references": 21}, "FAIL"),  # >50
    ("video_edit", {"video_references": 1}, "PASS"),
    ("video_edit", {"video_references": 1, "start_image": 1}, "FAIL"),
])
def test_seedance_2_5_truth_table(live, mode, media, expected):
    assert verdict(live, "seedance_2_5", {"mode": mode}, media) == expected


def test_seedance_2_5_default_mode_is_t2v(live):
    # Omitted mode = the platform default (t2v), so a start frame alone fails.
    assert verdict(live, "seedance_2_5", {}, {"start_image": 1}) == "FAIL"


def test_extension_mode_rules(live):
    assert verdict(live, "seedance_2_5", {"mode": "video_extension"},
                   {"video_references": 1}) == "FAIL"
    assert verdict(live, "seedance_2_5", {"mode": "video_extension",
                                          "extension_mode": "forward"},
                   {"video_references": 1}) == "PASS"
    assert verdict(live, "seedance_2_5", {"mode": "t2v",
                                          "extension_mode": "forward"}) == "FAIL"


def test_rule_messages_are_carried(live):
    rep = pf.run_preflight("seedance_2_5", {"mode": "t2v"}, {"start_image": 1},
                           baseline=live)
    msgs = {r.rule.message for r in rep.rules if r.status == "FAIL"}
    assert "start_image and end_image are only allowed for mode 'omni_reference'" in msgs


# ── Other live rule families ────────────────────────────────────────────────

@pytest.mark.parametrize("duration,expected", [(1, "FAIL"), (0, "FAIL"), (-1, "PASS"),
                                               (2, "PASS"), (30, "PASS"), (31, "FAIL")])
def test_wan3_smart_duration(live, duration, expected):
    assert verdict(live, "wan3_0", {"duration": duration}) == expected


def test_wan3_start_image_excludes_references(live):
    assert verdict(live, "wan3_0", {}, {"start_image": 1, "image_references": 1}) == "FAIL"
    assert verdict(live, "wan3_0", {}, {"end_image": 1}) == "FAIL"   # end needs start
    assert verdict(live, "wan3_0", {}, {"start_image": 1, "end_image": 1}) == "PASS"


def test_gemini_hyphenated_modes(live):
    assert verdict(live, "gemini_omni_flash_1_1", {"mode": "text-to-video"},
                   {"start_image": 1}) == "FAIL"
    assert verdict(live, "gemini_omni_flash_1_1", {"mode": "image-to-video"},
                   {"start_image": 1}) == "PASS"
    assert verdict(live, "gemini_omni_flash_1_1", {"mode": "edit"},
                   {"video_references": 1}) == "PASS"


# ── type() / unary ! (the rules the live CLI itself refused to evaluate) ────
# `higgsfield generate cost` fails on these with "Unsupported validation
# rule"; preflight implements type()/string/int/double and unary ! properly.

@pytest.mark.parametrize("params,expected", [
    ({"mode": "preview"}, "PASS"),
    ({"mode": "preview", "texture_prompt": "weathered bronze"}, "FAIL"),
    ({"mode": "preview", "enable_pbr": True}, "FAIL"),
    ({"mode": "full", "texture_prompt": "weathered bronze", "enable_pbr": True}, "PASS"),
    ({"mode": "full", "enable_animation": True}, "FAIL"),            # needs rigging
    ({"mode": "full", "enable_animation": True, "enable_rigging": True}, "FAIL"),  # needs int id
    ({"mode": "full", "enable_animation": True, "enable_rigging": True,
      "animation_action_id": 7}, "PASS"),
    ({"mode": "full", "rigging_height_meters": 1.8}, "FAIL"),
    ({"mode": "full", "rigging_height_meters": 1.8, "enable_rigging": True}, "PASS"),
])
def test_meshy_type_rules(live, params, expected):
    assert verdict(live, "meshy_v6_text_to_3d", params) == expected


@pytest.mark.parametrize("params,expected", [
    ({"mode": "std", "enable_pbr": True}, "FAIL"),
    ({"mode": "std"}, "PASS"),
    ({"mode": "pro", "enable_pbr": True}, "PASS"),
    ({"mode": "std", "prompt": "x" * 201}, "FAIL"),
    ({"mode": "std", "face_count": 5000}, "FAIL"),
    ({"mode": "pro", "generate_type": "Geometry", "enable_pbr": True}, "FAIL"),
    ({"mode": "pro", "generate_type": "Normal", "enable_pbr": True}, "PASS"),
])
def test_hunyuan_type_and_not_rules(live, params, expected):
    assert verdict(live, "hunyuan3d_v3_1_text_to_3d", params) == expected


def test_type_values():
    p = pf.Params({"s": "a", "i": 3, "d": 1.5, "n": None, "b": True})
    env = {"params": p}
    ev = lambda src: pf._eval(pf.parse_rule(src), env)  # noqa: E731
    assert ev("type(params.s) == string") is True
    assert ev("type(params.i) == int") is True
    assert ev("type(params.d) == double") is True
    assert ev("type(params.n) == null_type") is True
    assert ev("type(params.b) == bool && type(params.i) != double") is True


# ── Fail closed ─────────────────────────────────────────────────────────────

@pytest.mark.parametrize("rule", [
    'params.prompt.startsWith("A")',        # unsupported method
    "timestamp(params.t) > 0",              # unsupported function
    "params.mode ~ 1",                      # unsupported token
    "someVar == 1",                         # unbound identifier
    "params.mode == ",                      # truncated
])
def test_unparseable_rule_is_unchecked(rule):
    [res] = pf.evaluate_rules([pf.Rule(rule)], {"mode": "t2v", "prompt": "A"})
    assert res.status == "UNCHECKED"


@pytest.mark.parametrize("rule", [
    'params.mode < 3',                      # string vs int ordering
    'size(params.duration) == 1',           # size() of a number
    '{"a": 1}[params.mode] == 1',           # missing map key
    '!params.mode',                         # ! on a string
])
def test_unevaluable_rule_is_unchecked(rule):
    [res] = pf.evaluate_rules([pf.Rule(rule)], {"mode": "t2v", "duration": 5})
    assert res.status == "UNCHECKED"


def test_unchecked_rule_makes_strict_exit_nonzero(tmp_path):
    doc = {"captured": "2026-09-26", "video": {"seedance_2_5": {
        "params": {}, "rules": ['params.prompt.startsWith("A")']}}}
    b = tmp_path / "b.json"
    b.write_text(json.dumps(doc), encoding="utf-8")
    lenient = run("--model", "seedance_2_5", "--baseline", str(b), "--param", "mode=t2v")
    strict = run("--model", "seedance_2_5", "--baseline", str(b), "--param", "mode=t2v",
                 "--strict")
    assert lenient.returncode == 0 and "UNCHECKED" in lenient.stdout
    assert strict.returncode == 1


def test_model_without_rules_on_record_is_unchecked_not_pass(tmp_path):
    b = tmp_path / "b.json"
    b.write_text(json.dumps({"captured": "2026-08-07", "video": {}}), encoding="utf-8")
    r = run("--model", "seedance_2_5", "--baseline", str(b), "--param", "mode=t2v",
            "--strict")
    assert r.returncode == 1 and "no platform rules on record" in r.stdout


def test_error_is_absorbed_by_a_decisive_side():
    # CEL commutative error absorption: `false && <error>` is false,
    # `true || <error>` is true — the rule is decided, not unchecked.
    [a, b] = pf.evaluate_rules([pf.Rule('params.mode == "x" && params.mode < 3'),
                                pf.Rule('params.mode == "t2v" || params.mode < 3')],
                               {"mode": "t2v"})
    assert (a.status, b.status) == ("FAIL", "PASS")


def test_unknown_inputs_are_three_valued():
    rules = [pf.Rule('params.mode != "t2v" || size(params.image_references) == 0')]
    # Mode known and not t2v → decided without the media.
    [r1] = pf.evaluate_rules(rules, {"mode": "omni_reference"}, missing="unknown")
    # Mode t2v, media undeclared → not knowable, never guessed.
    [r2] = pf.evaluate_rules(rules, {"mode": "t2v"}, missing="unknown")
    # Complete request: omitted media = absent.
    [r3] = pf.evaluate_rules(rules, {"mode": "t2v"}, missing="null")
    assert (r1.status, r2.status, r3.status) == ("PASS", "UNKNOWN", "PASS")
    assert r2.depends_on == ["image_references"]


def test_in_list_and_ternary_and_map_index():
    p = {"mode": "fast", "resolution": "4k", "variant": "minimax", "prompt": "x" * 20}
    rules = [pf.Rule('params.mode != "fast" || !(params.resolution in ["1080p", "4k"])'),
             pf.Rule('(params.start_image == null ? 0 : 1) == 0'),
             pf.Rule('size(params.prompt) <= {"minimax": 10, "seed": 50}[params.variant]'),
             pf.Rule('!has(params.colors) || params.colors.all(c, c.matches("^#[0-9A-F]{6}$"))')]
    got = [r.status for r in pf.evaluate_rules(rules, p)]
    assert got == ["FAIL", "PASS", "FAIL", "PASS"]
    ok = [r.status for r in pf.evaluate_rules(rules[3:], {"colors": ["#A0B0C0"]})]
    bad = [r.status for r in pf.evaluate_rules(rules[3:], {"colors": ["red"]})]
    assert (ok, bad) == (["PASS"], ["FAIL"])


# ── Spec surface + CLI ──────────────────────────────────────────────────────

def test_spec_surface_enum_and_roles(live):
    rep = pf.run_preflight("seedance_2_0", {"resolution": "8k", "aspect_ratio": "5:1"},
                           {"image_references": 1}, baseline=live)
    fails = {c.what for c in rep.checks if c.status == "FAIL"}
    assert fails == {"resolution=8k", "aspect_ratio=5:1"}


def test_cli_seedance_2_5_start_image_in_t2v():
    r = run("--model", "seedance_2_5", "--baseline", str(LIVE),
            "--param", "mode=t2v", "--media", "start_image=1")
    assert r.returncode == 1 and "FAIL" in r.stdout


def test_cli_json_input():
    req = json.dumps({"model": "seedance_2_5", "params": {"mode": "omni_reference"},
                      "media": {"image_references": 31}})
    r = run("--json", req, "--baseline", str(LIVE), "--report-json")
    out = json.loads(r.stdout)
    assert r.returncode == 1 and out["verdict"] == "FAIL"


def test_cli_ambiguous_and_unknown_models_exit_2():
    amb = run("--model", "Cinema Studio Video", "--param", "duration=12")
    assert amb.returncode == 2 and "cinematic_studio_video_v2" in amb.stderr
    unk = run("--model", "no_such_model_9", "--param", "mode=t2v")
    assert unk.returncode == 2
