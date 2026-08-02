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
