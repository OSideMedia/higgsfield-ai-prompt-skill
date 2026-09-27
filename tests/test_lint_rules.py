"""seedance_lint.py — filter rules, structural rules, settings parsing.

The two headline cases the preflight exists to catch:
  * Seedance 2.0 `fast` mode + 1080p  → FAIL (mode-constraint)
  * Kling 3.0 + 21:9                  → FAIL (ar-not-supported)
"""

import pytest

import seedance_lint as sl

CLEAN = ("Style: desaturated noir, hard key light. Interior warehouse at "
         "dusk. Slow dolly-in on a figure in a wool coat.")


def fails(findings):
    return {f.rule for f in findings if f.severity == "FAIL"}


def warns(findings):
    return {f.rule for f in findings if f.severity == "WARN"}


# ── Filter lint (content rules) ─────────────────────────────────────────────

def test_clean_prompt_passes():
    assert fails(sl.lint(CLEAN)) == set()


@pytest.mark.parametrize("prompt,rule", [
    ("Taylor Swift walks through a neon alley at night", "real-person-name"),
    ("A Nike billboard glows over the street", "brand-ip"),
    ("He stabs the door panel in frustration", "violence-verb"),
    ("A rifle leans against the wall of the cabin", "weapon-noun"),
    ("A young boy runs across the courtyard", "age-marker"),
])
def test_filter_fail_rules(prompt, rule):
    assert rule in fails(sl.lint(prompt))


def test_overlength_fails_short_form():
    assert "overlength" in fails(sl.lint("word " * 230))


# ── Regime detection (HARD RULE 8 carve-out) ────────────────────────────────

BLOCK_PROMPT = "\n".join([
    "SCENE CONTEXT: an evacuated coastal city at dawn, streets empty.",
    "LOCATION MAP: the promenade runs left to right; the pier sits far right.",
    "CAMERA: FOV 63 degrees, slow dolly-in, tripod-steady.",
    "ACTION: " + "the figure walks the promenade, coat lifting in the wind. " * 40,
    "LIGHTING: soft even morning daylight, gentle atmospheric haze.",
    "POSITIVE LOCKS: the set contains only what the reference shows.",
])


def test_block_scaffold_detected():
    assert sl.detect_regime(BLOCK_PROMPT) == "block"
    assert sl.detect_regime(CLEAN) == "short"
    assert sl.detect_regime("Strictly 2 shots. 【镜头1】walk. 【镜头2】turn.") == "block"


def test_block_regime_suspends_word_caps():
    findings = sl.lint(BLOCK_PROMPT)
    assert "overlength" not in fails(findings)
    assert "long" not in warns(findings)
    assert "block-scaffold-regime" in {f.rule for f in findings
                                       if f.severity == "INFO"}


def test_block_regime_keeps_content_rules():
    hot = BLOCK_PROMPT + "\nACTION: Taylor Swift crosses the street."
    assert "real-person-name" in fails(sl.lint(hot))


def test_regime_override_forces_short():
    assert "overlength" in fails(sl.lint(BLOCK_PROMPT, regime="short"))


def test_shot_as_film_noun_passes():
    # "shot" is core film vocabulary — the violence rule must only fire on
    # verb/violence constructions, never on cinematography usage.
    for text in ("Medium two-shot of two colleagues at the bench.",
                 "Wide shot of the harbour at dawn, one shot per scene.",
                 "The shot opens on the pier; each shot holds 5s."):
        assert "violence-verb" not in fails(sl.lint(text))


def test_shot_as_violence_still_fails():
    for text in ("He was shot in the alley at midnight.",
                 "She shot him across the courtyard."):
        assert "violence-verb" in fails(sl.lint(text))


# ── Specs-driven enum / constraint checks ───────────────────────────────────

def spec_for(mini_spec, model_id):
    _, path = mini_spec
    return sl.resolve_model(sl.load_specs(path), model_id)


def test_seedance_fast_1080p_fails(mini_spec):
    spec = spec_for(mini_spec, "seedance_2_0")
    s = sl.Settings(mode="fast", resolution="1080p")
    assert "mode-constraint" in fails(sl.structural_lint(CLEAN, s, spec))


def test_kling_21_9_fails(mini_spec):
    spec = spec_for(mini_spec, "kling3_0")
    s = sl.Settings(ar="21:9")
    assert "ar-not-supported" in fails(sl.structural_lint(CLEAN, s, spec))


def test_legal_combination_passes(mini_spec):
    spec = spec_for(mini_spec, "seedance_2_0")
    s = sl.Settings(ar="21:9", mode="std", resolution="1080p", duration=8)
    assert fails(sl.structural_lint(CLEAN, s, spec)) == set()


def test_alias_resolves_to_canonical(mini_spec):
    spec = spec_for(mini_spec, "video_standard")
    assert spec is not None and spec["id"] == "seedance_2_0"


def test_duration_out_of_range(mini_spec):
    spec = spec_for(mini_spec, "seedance_2_0")
    assert "duration-out-of-range" in fails(
        sl.structural_lint(CLEAN, sl.Settings(duration=20), spec))
    lite = spec_for(mini_spec, "veo3_1_lite")
    assert "duration-out-of-range" in fails(
        sl.structural_lint(CLEAN, sl.Settings(duration=5), lite))


def test_requires_constraint(mini_spec):
    lite = spec_for(mini_spec, "veo3_1_lite")
    # 1080p requires duration=8 (snapshot-extracted)
    s = sl.Settings(resolution="1080p", duration=6)
    assert "constraint-requires" in fails(sl.structural_lint(CLEAN, s, lite))
    s_ok = sl.Settings(resolution="1080p", duration=8)
    assert fails(sl.structural_lint(CLEAN, s_ok, lite)) == set()


# ── Structural rules (no spec needed) ───────────────────────────────────────

def test_shot_count_mismatch():
    text = "Strictly 3 shots. 【镜头1】walk. 【镜头2】turn. " + CLEAN
    findings = sl.structural_lint(text, sl.Settings(), None)
    assert "shot-count-mismatch" in fails(findings)


def test_shot_count_match_passes():
    text = "Strictly 2 shots. 【镜头1】walk. 【镜头2】turn. " + CLEAN
    assert "shot-count-mismatch" not in fails(
        sl.structural_lint(text, sl.Settings(), None))


def test_beats_exceed_envelope():
    text = "[0-4s] walk. [4-12s] turn. " + CLEAN
    findings = sl.structural_lint(text, sl.Settings(duration=8), None)
    assert "beats-exceed-envelope" in fails(findings)


def test_beat_gap_and_overlap_warn():
    gap = "[0-2s] walk. [4-8s] turn. " + CLEAN
    assert "beat-gap" in warns(sl.structural_lint(gap, sl.Settings(duration=8), None))
    overlap = "[0-4s] walk. [3-8s] turn. " + CLEAN
    assert "overlapping-beats" in warns(
        sl.structural_lint(overlap, sl.Settings(duration=8), None))


def test_beats_start_late_and_undershoot_warn():
    text = "[2-6s] walk. " + CLEAN
    findings = sl.structural_lint(text, sl.Settings(duration=8), None)
    assert "beats-start-late" in warns(findings)
    assert "beats-undershoot-envelope" in warns(findings)


def test_contiguous_full_coverage_beats_pass():
    text = "[0-4s] walk. [4-8s] turn. " + CLEAN
    findings = sl.structural_lint(text, sl.Settings(duration=8), None)
    for rule in ("beat-gap", "overlapping-beats", "beats-start-late",
                 "beats-undershoot-envelope"):
        assert rule not in warns(findings)


def test_declared_shots_without_structure_warns():
    text = "Strictly 3 shots. " + CLEAN
    assert "declared-shots-unstructured" in warns(
        sl.structural_lint(text, sl.Settings(), None))


def test_zh_overlength():
    text = "汉" * (sl.ZH_CHAR_CAP + 1)
    assert "zh-overlength" in fails(sl.structural_lint(text, sl.Settings(), None))


def test_zh_antislop_warns():
    text = "镜头缓慢推进，视觉盛宴，仓库内部。"
    assert "zh-antislop" in warns(sl.structural_lint(text, sl.Settings(), None))


def test_handle_used_before_declared():
    text = "@Hero walks toward the door.\n@Hero: tall figure in a wool coat"
    assert "handle-used-before-declared" in fails(
        sl.structural_lint(text, sl.Settings(), None))


def test_handle_declared_first_passes():
    text = "@Hero: tall figure in a wool coat\n@Hero walks toward the door."
    findings = sl.structural_lint(text, sl.Settings(), None)
    assert "handle-used-before-declared" not in fails(findings)
    assert "undeclared-handle" not in fails(findings)


# ── Settings parsing ────────────────────────────────────────────────────────

def test_parse_settings_header():
    text = ("**Aspect ratio**: 21:9  **Duration**: 8s\n"
            "Resolution: 1080p, mode: fast\n" + CLEAN)
    s = sl.parse_settings_header(text)
    assert (s.ar, s.resolution, s.mode, s.duration) == ("21:9", "1080p", "fast", 8)


def test_cli_overrides_header():
    header = sl.Settings(ar="16:9", resolution="720p", mode="std", duration=5)
    cli = sl.Settings(resolution="1080p")
    merged = sl.merge_settings(header, cli)
    assert merged.resolution == "1080p"
    assert (merged.ar, merged.mode, merged.duration) == ("16:9", "std", 5)


# ── v3.37.0 root fixes: header parsing, smart duration, ambiguity, roles ───
#
# Each test below was run against the pre-fix seedance_lint.py
# (git show 9b86817:scripts/seedance_lint.py) and went RED there.

import json  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402
from pathlib import Path  # noqa: E402

import preflight  # noqa: E402

REPO_SPECS = Path(__file__).resolve().parents[1] / "specs" / "model-specs.json"
LIVE_RULES = Path(__file__).parent / "fixtures" / "cli_rules_live_2026-09-26.json"
LINT = Path(__file__).resolve().parents[1] / "scripts" / "seedance_lint.py"
NO_RULES = {"rules": {}}

WAN3 = {  # shape of specs/model-specs.json wan3_0 as sync_specs emits it (2026-09-26)
    "id": "wan3_0", "name": "Wan 3.0", "aliases": [], "modes": [],
    "aspect_ratios": ["auto", "16:9", "9:16", "1:1", "4:3", "3:4"],
    "resolutions": ["480p", "720p", "1080p"], "constraints": [],
    "duration": {"min": -1, "max": 30},
    "media_roles": {"medias": ["start_image", "end_image", "image_references",
                               "video_references", "audio_references"]},
    "params": [{"name": "duration", "min": -1, "max": 30, "type": "number",
                "description": "Duration in seconds (2-30), or -1 to let the "
                               "model choose the length from the prompt and "
                               "media. Smart duration is billed as 10 seconds."}],
}


def repo_spec(model_id):
    spec = sl.resolve_model(sl.load_specs(REPO_SPECS), model_id)
    if spec is None:
        pytest.fail(f"fixture premise gone: {model_id} not in specs — re-point the test")
    return spec


def lint_header(text, spec, baseline=NO_RULES):
    return sl.structural_lint(text, sl.parse_settings_header(text), spec,
                              baseline=baseline)


# Item 1 — mode header: hyphens kept, block-scaffold labels are not the mode.

def test_hyphenated_mode_is_not_truncated():
    s = sl.parse_settings_header("**Mode**: text-to-video  **Duration**: 8s\n" + CLEAN)
    assert s.mode == "text-to-video"
    s = sl.parse_settings_header("Mode: reference-to-video\n" + CLEAN)
    assert s.mode == "reference-to-video"


def test_hyphenated_mode_passes_enum_check_on_real_spec():
    spec = repo_spec("gemini_omni_flash_1_1")
    if "text-to-video" not in spec.get("modes", []):
        pytest.fail("fixture premise gone: gemini_omni_flash_1_1 lost its "
                    "hyphenated text-to-video mode — re-point the test")
    text = "**Mode**: text-to-video  **Duration**: 8s\n" + CLEAN
    assert "mode-not-supported" not in fails(lint_header(text, spec))


@pytest.mark.parametrize("label", [
    "FORMAT MODE: multi-segment", "Extension mode: forward", "Shot Mode:  Smart",
    "Image mode:** Cinema", "the failure mode: the camera drifts",
])
def test_non_mode_labels_are_not_the_model_mode(label):
    assert sl.parse_settings_header(label + "\n" + CLEAN).mode is None


def test_block_scaffold_format_mode_does_not_shadow_real_mode():
    text = "FORMAT MODE: multi-segment\n**Mode**: std  **Duration**: 8s\n" + CLEAN
    assert sl.parse_settings_header(text).mode == "std"


def test_format_mode_label_is_not_linted_as_a_mode(mini_spec):
    spec = spec_for(mini_spec, "seedance_2_0")
    text = "FORMAT MODE: multi-segment\n**Duration**: 8s\n" + CLEAN
    assert "mode-not-supported" not in fails(lint_header(text, spec))


@pytest.mark.parametrize("header,mode", [
    ("**Mode**: video_extension  **Extension mode**: forward", "video_extension"),
    ("Resolution: 1080p, mode: fast", "fast"),
    ("**Aspect ratio**: 16:9  **Mode**: t2v", "t2v"),
    ("Generation mode: std", "std"),
])
def test_real_mode_labels_still_parse(header, mode):
    assert sl.parse_settings_header(header + "\n" + CLEAN).mode == mode


# Item 2 — smart duration: -1 is a sentinel, never a length; 0/1 are illegal.

@pytest.mark.parametrize("duration,rule_fires", [
    (0, True), (1, True), (-1, False), (2, False), (30, False), (31, True), (-2, True),
])
def test_smart_duration_sentinel_only(duration, rule_fires):
    findings = sl.structural_lint(CLEAN, sl.Settings(duration=duration), WAN3,
                                  baseline=NO_RULES)
    assert ("duration-out-of-range" in fails(findings)) is rule_fires


def test_smart_duration_header_parses():
    for header in ("**Duration**: -1", "**Duration**: -1s", "Duration: smart"):
        assert sl.parse_settings_header(header + "\n" + CLEAN).duration == -1
    assert sl.parse_settings_header("**Duration**: 8s\n" + CLEAN).duration == 8


def test_smart_duration_is_not_a_beat_envelope():
    # -1 is not a length: beats are bounded by the model max (30s), not by -1.
    text = "[0-4s] walk. [4-8s] turn. " + CLEAN
    findings = sl.structural_lint(text, sl.Settings(duration=-1), WAN3,
                                  baseline=NO_RULES)
    assert "beats-exceed-envelope" not in fails(findings)
    assert "beats-undershoot-envelope" not in warns(findings)


def test_negative_duration_fails_where_no_sentinel(mini_spec):
    spec = spec_for(mini_spec, "seedance_2_0")
    assert "duration-out-of-range" in fails(
        sl.structural_lint(CLEAN, sl.Settings(duration=-1), spec, baseline=NO_RULES))


def test_smart_duration_on_real_wan_spec():
    spec = repo_spec("wan3_0")
    for d, bad in ((0, True), (1, True), (-1, False), (10, False)):
        got = "duration-out-of-range" in fails(
            sl.structural_lint(CLEAN, sl.Settings(duration=d), spec, baseline=NO_RULES))
        assert got is bad, d


# Item 3 — an ambiguous display name is an error naming the candidates.

def test_ambiguous_display_name_is_an_error_listing_candidates():
    index = sl.load_specs(REPO_SPECS)
    ids = sorted(m["id"] for m in json.loads(REPO_SPECS.read_text())["models"]
                 if m["name"] == "Cinema Studio Video")
    if len(ids) < 2:
        pytest.fail("fixture premise gone: 'Cinema Studio Video' is no longer "
                    "shared by two ids — re-point the test")
    with pytest.raises(sl.AmbiguousModelError) as exc:
        sl.resolve_model(index, "Cinema Studio Video")
    assert exc.value.candidates == ids
    for mid in ids:
        assert mid in str(exc.value)
    assert sl.resolve_model(index, ids[0])["id"] == ids[0]   # exact ids resolve


def test_ambiguity_via_cli_exits_2():
    r = subprocess.run([sys.executable, str(LINT), "--model", "Cinema Studio Video",
                        "--duration", "12", CLEAN], capture_output=True, text=True)
    assert r.returncode == 2
    assert "ambiguous" in r.stderr and "cinematic_studio_video_v2" in r.stderr


# Item 4 — media roles: header syntax + the live Seedance 2.5 platform rules.

@pytest.mark.parametrize("header,expected", [
    ("**References**: 2 images, 1 video, 1 audio",
     {"image_references": 2, "video_references": 1, "audio_references": 1}),
    ("**References**: @Image 1, @Image 2, @Video 1",
     {"image_references": 2, "video_references": 1}),
    ("**Start frame**: @Image 1  **End frame**: @Image 2",
     {"start_image": 1, "end_image": 1}),
    ("**References**: none", {}),
    ("**Start frame**: none", {}),
])
def test_media_header_parses(header, expected):
    media = sl.parse_settings_header(header + "\n" + CLEAN).media
    want = {r: 0 for r in sl.MEDIA_ROLES}
    want.update(expected)
    assert media == want


def test_no_media_header_means_undeclared():
    assert sl.parse_settings_header("**Mode**: t2v\n" + CLEAN).media is None


def test_block_label_active_references_is_not_a_media_line():
    assert sl.parse_settings_header("ACTIVE REFERENCES: @video1 source\n" + CLEAN).media is None


def test_unparseable_references_line_warns():
    s = sl.parse_settings_header("**References**: the usual suspects\n" + CLEAN)
    assert s.media_error
    findings = sl.structural_lint(CLEAN, s, WAN3, baseline=NO_RULES)
    assert "media-declaration-unparsed" in warns(findings)


@pytest.fixture(scope="module")
def live_rules():
    return preflight.load_baseline(LIVE_RULES)


def test_start_frame_in_t2v_fails_live_rules(live_rules):
    text = "**Mode**: t2v  **Duration**: 8s  **Start frame**: @Image 1\n" + CLEAN
    assert "platform-rule" in fails(lint_header(text, repo_spec("seedance_2_5"), live_rules))


def test_start_frame_in_omni_reference_passes_live_rules(live_rules):
    text = ("**Mode**: omni_reference  **Duration**: 8s  **Start frame**: @Image 1\n"
            + CLEAN)
    assert "platform-rule" not in fails(
        lint_header(text, repo_spec("seedance_2_5"), live_rules))


def test_31_image_refs_fail_live_rules(live_rules):
    spec = repo_spec("seedance_2_5")
    over = "**Mode**: omni_reference  **References**: 31 images\n" + CLEAN
    at = "**Mode**: omni_reference  **References**: 30 images\n" + CLEAN
    assert "platform-rule" in fails(lint_header(over, spec, live_rules))
    assert "platform-rule" not in fails(lint_header(at, spec, live_rules))


def test_undeclared_media_is_not_guessed(live_rules):
    # video_edit needs exactly one video reference — a prompt that declares no
    # media must not FAIL on it (the clip may be attached in the UI); the rule
    # is reported as not evaluated instead.
    text = "**Mode**: video_edit  **Resolution**: 720p\n" + CLEAN
    findings = lint_header(text, repo_spec("seedance_2_5"), live_rules)
    assert "platform-rule" not in fails(findings)
    assert "platform-rules-need-media" in {f.rule for f in findings
                                           if f.severity == "INFO"}


def test_unevaluable_rule_warns_never_passes(mini_spec):
    spec = spec_for(mini_spec, "seedance_2_0")
    bogus = {"rules": {"seedance_2_0": [preflight.Rule('params.prompt.startsWith("a")')]}}
    text = "**Mode**: std  **Duration**: 8s\n" + CLEAN
    assert "platform-rule-unchecked" in warns(lint_header(text, spec, bogus))


def test_role_not_accepted_by_model_fails(mini_spec):
    spec = spec_for(mini_spec, "kling3_0")
    if "video_references" in preflight.media_roles(spec):
        pytest.fail("fixture premise gone: mini kling3_0 accepts video_references")
    s = sl.Settings(media={"start_image": 0, "end_image": 0, "image_references": 0,
                           "video_references": 2, "audio_references": 0})
    assert "media-role-not-supported" in fails(
        sl.structural_lint(CLEAN, s, spec, baseline=NO_RULES))


def test_cli_media_flag_reaches_the_rules():
    r = subprocess.run([sys.executable, str(LINT), "--model", "seedance_2_5",
                        "--baseline", str(LIVE_RULES), "--mode", "t2v",
                        "--media", "start_image=1", CLEAN],
                       capture_output=True, text=True)
    assert r.returncode == 1 and "platform-rule" in r.stdout


# ── v3.37.0 review: plain-text headers declare the mode again (regression) ──

@pytest.mark.parametrize("header,mode", [
    ("- Mode: fast", "fast"),                        # bullet (v3.36.0 read this)
    ("* Mode: fast", "fast"),
    ("1. Mode: fast", "fast"),
    ("Aspect ratio: 16:9 Mode: fast", "fast"),       # inline, one space after a value
    ("Resolution: 1080p Mode: fast", "fast"),
    ("Aspect: auto Mode: fast", "fast"),             # value is a plain word
])
def test_plain_text_headers_declare_the_mode(header, mode):
    assert sl.parse_settings_header(header + "\n" + CLEAN).mode == mode


@pytest.mark.parametrize("label", ["extension-mode: forward", "Camera: dolly Shot Mode: x"])
def test_qualified_mode_labels_stay_excluded(label):
    assert sl.parse_settings_header(label + "\n" + CLEAN).mode is None


def test_bullet_header_fast_1080p_fails_end_to_end():
    text = "- Mode: fast\n- Resolution: 1080p\n\n" + CLEAN
    r = subprocess.run([sys.executable, str(LINT), "--model", "seedance_2_0", text],
                       capture_output=True, text=True)
    assert r.returncode == 1 and "mode-constraint" in r.stdout, r.stdout


# ── v3.37.0 review: the platform-rule bridge never goes silent ──────────────

def test_model_without_rules_on_record_says_so():
    findings = sl.structural_lint(CLEAN, sl.Settings(mode="std"), repo_spec("seedance_2_0"),
                                  baseline={"rules": {}})
    info = [f for f in findings if f.rule == "platform-rules-not-on-record"]
    assert info and info[0].severity == "INFO" and "NOT checked" in info[0].fix


def test_undeclared_mode_is_evaluated_with_the_platform_default():
    # seedance_2_5 default mode is t2v, which rejects a start frame: the
    # prompt used to get a WARN about handles and nothing else.
    live = preflight.load_baseline(LIVE_RULES)
    text = "**Start frame**: @Image 1\n\n" + CLEAN
    findings = lint_header(text, repo_spec("seedance_2_5"), baseline=live)
    assert "platform-rule" in fails(findings)
    assert any(f.rule == "mode-defaulted" and "t2v" in f.hit for f in findings)
    declared = lint_header("**Mode**: omni_reference\n" + text, repo_spec("seedance_2_5"),
                           baseline=live)
    assert "platform-rule" not in fails(declared)
    assert not any(f.rule == "mode-defaulted" for f in declared)


# ── v3.37.0 review: media counts and duration values read what was written ──

@pytest.mark.parametrize("line,n", [
    ("**References**: 2 images (@Image 1, @Image 2)", 2),   # was counted 4
    ("**References**: @Image 1, @Image 2, @Image 3", 3),
    ("**References**: 2 images", 2),
    ("**References**: 1 image, @Image 1, @Image 2", 2),
])
def test_stated_count_and_handles_are_one_set(line, n):
    assert sl.parse_settings_header(line + "\n" + CLEAN).media["image_references"] == n


@pytest.mark.parametrize("header,duration", [
    ("**Duration**: smart pacing, 8s", None),               # was -1; only the leading value counts
    ("**Duration**: smart", -1),
    ("Duration: smart duration", -1),
    ("Duration: smart (the model picks)", -1),
    ("Duration: 8 seconds", 8),
    ("Duration: 5-10s", None),                              # a range is not a length
    ("**Duration**: smart  **Mode**: t2v", -1),
])
def test_duration_value_parsing(header, duration):
    assert sl.parse_settings_header(header + "\n" + CLEAN).duration == duration


def test_duration_unverified_when_the_floor_is_unknown():
    # A spec whose smart-duration floor cannot be derived: a length inside
    # the max is UNVERIFIED (WARN), never passed and never failed.
    spec = dict(WAN3, params=[{"name": "duration", "type": "number", "min": -1,
                               "max": 30, "description": "Duration, or -1 for smart."}])
    findings = sl.structural_lint(CLEAN, sl.Settings(duration=5), spec, baseline=NO_RULES)
    assert "duration-unverified" in warns(findings)
    assert "duration-out-of-range" not in fails(findings)


# ── v3.37.0 review 2: the word before the key decides, not an earlier colon ──

@pytest.mark.parametrize("line", [
    "Tip: extension mode: forward",          # v3.36.0 got this right too
    "Note: failure mode: drift",
    "**Watch**: failure mode: face drift",
    "Camera: dolly — Shot Mode: close",
])
def test_qualified_mode_after_a_label_is_not_the_mode(line):
    assert sl.parse_settings_header(line + "\n" + CLEAN).mode is None


def test_qualified_mode_after_a_label_does_not_fail_the_lint():
    text = "Tip: extension mode: forward\n\n" + CLEAN
    r = subprocess.run([sys.executable, str(LINT), "--model", "seedance_2_0", text],
                       capture_output=True, text=True)
    assert "mode-not-supported" not in r.stdout and r.returncode == 0, r.stdout


def test_qualified_references_after_a_label_are_not_media():
    assert sl.parse_settings_header("Note: style references: 2 images\n" + CLEAN).media is None
    assert sl.parse_settings_header("Aspect: auto Mode: fast\n" + CLEAN).mode == "fast"


@pytest.mark.parametrize("header,duration", [
    ("**Duration**: auto, beats at 2s and 5s", None),       # was 2 → FAIL at 2s
    ("**Duration**: TBD (was 10s)", None),                  # was 10
    ("**Duration**: 12s (3 beats of 4s)", 12),
    ("**Duration**: 8s", 8),
    ("**Duration**: -1s", -1),
])
def test_only_the_leading_duration_value_counts(header, duration):
    assert sl.parse_settings_header(header + "\n" + CLEAN).duration == duration


@pytest.mark.parametrize("line,n", [
    ("**References**: 2 images, @Image 3", 3),              # was 2: @Image 3 implies three
    ("**References**: @Image 1, @Image 4", 4),
    ("**References**: 5 images, @Image 2", 5),
])
def test_highest_handle_index_counts(line, n):
    assert sl.parse_settings_header(line + "\n" + CLEAN).media["image_references"] == n
