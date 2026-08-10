# Changelog

## v3.29.0 — 2026-08-09

**Two approved cherry-picks from the Emily2040/seedance-2.0 skill evaluation** (2026-08-09, MIT-licensed). Idea-ports re-derived in house voice — no source text copied. The source's same-seed-experiment clause ("same seed + one prompt change ≈ controlled experiment") was deliberately NOT adopted: it contradicts the measured fact that this surface exposes no seed parameter and every roll is fresh (`higgsfield-seedance` § Drafts Validate the Prompt, Not the Take). Re-roll is documented as "same prompt again, unchanged" with zero seed language.

### Added
- `skills/higgsfield-troubleshoot/SKILL.md` § **Take Triage — Five Verdicts for a Delivered Take**: every delivered take gets exactly one verdict — keep / fix-in-post / edit-don't-regenerate / re-roll / rewrite — before anything re-fires. Carries three sub-rules:
  - **Two takes with the same flaw = rewrite, by rule** (stop re-rolling into the same wall) — cut the other way, different flaws per roll = stochastic = batch-and-cull, keeping the verdict consistent with the iterate-vs-batch fork.
  - **Attempt budget declared before take one** `[heuristic]` — a take budget sized against `production-benchmarks.md` plus a *written* "good enough" bar; half-budget with no progress on the same flaw forces a strategy change (mode switch, shot split, or Retry Ladder rung 4).
  - **The shot log is the ledger row** — one line per take with the one changed variable in `notes`; no new logging surface invented (5-second rule stands).
  - One-variable-per-retake cites `higgsfield-prompt` § The Iteration Rule and `DISCIPLINE.md` § Single-Variable Iteration rather than restating them.
- `skills/higgsfield-troubleshoot/SKILL.md` § **Sequence & Continuation Failure Atlas**: 12-row symptom → likely cause → single-repair-variable table for chained work (continuations, extensions, start-frame-pinned handoffs), each row cross-wired to the existing owner section (`higgsfield-pipeline` § Source-carries-state / § Chain management, `higgsfield-seedance` § Reference Roles / § Single-vs-multi-shot).

### Changed
- `skills/higgsfield-pipeline/SKILL.md`: § Continuation & Extension Handoff now points to the atlas for symptom-level repair; Step 08+09 routes the keep/post/edit/re-roll/rewrite call to Take Triage. Version 3.4.1.
- `skills/higgsfield-seedance/FAILURE-MODES.md`: cross-reference to the atlas (this catalog = single-clip render failures; the atlas = the joins). Version 1.1.1.
- Sub-skill version: troubleshoot 3.2.0.

### Known limitations (accepted)
- Both additions are `[FIELD — community, Emily2040/seedance-2.0 skill (MIT), re-derived]` — transferable craft judged sound by evaluation, not measured on our routes. The atlas rows' likely-cause column is diagnostic default, not a distribution.
- The source's allocation-model reference (fidelity-budget allocation across identity/motion/density) did not merge naturally into either section and was deferred, not ported.

## v3.28.0 — 2026-08-09

**Seven approved cherry-picks from the 2026-08-09 third-party evaluation sweep** (liyue-aigc director skills, MiniMax-H3 bundled skills, and a third-party Seedance 2.5 storyboard skill audited by the dialect-warden). All content re-derived in house voice — no source text copied (the xianxia repo carries no license; MiniMax skills carry no per-file attribution). Provider-steering lines and the invalid "Negative Prompt:" field in the sources were deliberately NOT adopted.

### Added
- `skills/higgsfield-seedance-2-5/SKILL.md` § Reference Roles → **Fidelity — say how much of each material must survive**: four grades per material (full-preserve / partial-preserve / attribute-transfer / loose-guide), with attribute-transfer requiring a named target — the case a bare role line cannot express. Plus two new role rules: **character sheets leak their staging** (backdrop/panel-layout exclusion) and **beat lines name characters, never handles** (name + one visible marker at first appearance; `[OFFICIAL — SD25-PE mapping priority]`).
- `skills/higgsfield-seedance-2-5/MODE-PLAYBOOKS.md` § Storyboard grids — the **anti-monochrome-bleed sentence**: when the board is monochrome and the film is not, exclude the board's *medium* explicitly or the render comes back gray and sketchy.
- `skills/higgsfield-shotlist-director/SKILL.md`:
  - § **Sequence tempo and variety** — whole-sequence delivery checks no per-prompt rule can catch: **tempo budget** (runtime → cut count at ~4–6s average, one 6–8s hero hold, stated durations must sum exactly to the requested runtime) and **monotony audit** (no 3 consecutive cuts sharing shot size AND camera move; vary function and scale, not just duration).
  - Per-scene prompt law gains an **Off-screen line** — just-departed characters carry exit side + last visible state for one prompt (dropped after two consecutive absences), keeping re-entry direction legal.
  - `@`-glossary entries now carry a **fidelity grade** (pointer to the 2.5 fidelity section).
- `skills/higgsfield-camera/SKILL.md` § Micro-moves — the **reverse consistency check**: the stated travel must be able to produce the stated end framing; when move and end frame disagree the prompt is internally impossible.
- `skills/higgsfield-audio/SKILL.md` § **Cutting to music — assembling separately-generated clips on one track**: one master track law · cuts land on musical punctuation, never inside a sung vowel (ECU mouth-match exception) · unified grain + LUT as a deliberate batch-color-drift mask.
- `skills/higgsfield-troubleshoot/SKILL.md` § **Retry Ladder** — four terminating rungs; rung 2 treats a second failure as evidence the shot is over-packed (shorten/split + re-lint before re-firing, not a re-roll); rung 4 stops after three paid attempts with named options — silent omission is never one.

### Changed
- QUICK FACTS routing lines updated in shotlist-director, seedance-2-5, and audio for the new sections.
- Sub-skill versions: shotlist-director 1.2.0, seedance-2-5 1.1.0, camera 3.5.0, audio 3.5.0, troubleshoot 3.1.0.

- `skills/higgsfield-seedance-2-5/MODE-PLAYBOOKS.md` § Storyboard grids → **Panel-to-timestamp mapping — the optional adherence raiser**. Probe P1 (2026-08-09 A/B, (2.5, Ark), 480p) came back positive: order was followed in BOTH arms, but the mapping landed cuts on the declared stamps and kept each panel's props in its own shot, while the unmapped arm paced itself and leaked a shot-3 prop into shot 1. Shipped `[MEASURED — one pair]` with the vendor non-strict disclaimer and the keyframes pointer kept; same probe day also measured slot order as non-semantic (board-first vs board-last: identical order adherence — SD25-PE confirmed) and the image-reference aspect bound [0.4, 2.5] enforced at create.

### Known limitations (accepted)
- The seven evaluation-sweep additions are `[EMPIRICAL — third-party skill corpora, re-derived]` except where marked `[OFFICIAL — SD25-PE]` — transferable craft judged sound by evaluation, **not measured on our routes**. The tempo-budget bands and the 3-consecutive-cuts monotony threshold are re-derived defaults to tune, not findings.
- The panel-to-timestamp A/B is a single pair on one synthetic board — a strong directional read, not a distribution.

## v3.27.0 — 2026-08-09

**Two approved cherry-picks from the dramaclaw evaluation.** Motion-prompt laws earned in dramaclaw's Seedance production corpus (model-agnostic i2v craft, carried as `[EMPIRICAL]` practitioner findings), plus the audio-reference enforcement bounds surfaced by the dialect-warden reconciliation (drift item S2).

### Added
- `skills/higgsfield-seedance/SKILL.md` § Prompt-Craft Laws → **Motion-prompt laws (dramaclaw production corpus)**, three laws none of which the repo carried before:
  - **Unidirectional motion only** — a short action finishes early and the model reverses it to fill the clip (walks forward then steps back, leans in then pulls away). Chain 2–3 connected actions in the same direction; a there-and-back is two shots.
  - **Name the camera endpoint** — a move needs a destination: state what the frame shows when the move finishes, not just the move's name.
  - **Detail scale follows shot size** — close-ups earn micro-detail, wides earn broad arcs; cross-matching is unrenderable. Cross-linked against the existing snake-cam cherry-pick (composition answer to detail-in-a-wide) so the two don't read as contradicting.
- `skills/higgsfield-seedance/FAILURE-MODES.md` — new catalog entry **§ Action-reversal fill** (symptom / mechanism / counter face of the unidirectional law) + a matching self-repair checklist bullet.
- **Seedance 2.0 audio-reference enforcement bounds** in `skills/higgsfield-audio/SKILL.md` (§ Audio by Model → Seedance 2.0) and `skills/higgsfield-models/MODELS-DEEP-REFERENCE.md` (§ Audio — Rules and Failure Modes): per-clip duration **1.8–15.2s** AND **total across all attached clips ≤15.2s** — three individually-legal 6s clips get rejected. The previously-documented caps (15s/clip, 3 files, 10MB) had **no per-clip minimum and no total cap**, so a multi-clip attach that obeyed every documented limit could still 400.

### Changed
- `skills/higgsfield-seedance/SKILL.md` QUICK FACTS — prompt-craft-laws routing line now names the three motion laws.
- Sub-skill versions: higgsfield-seedance SKILL 1.12.0, FAILURE-MODES 1.1.0, higgsfield-audio 3.4.0, MODELS-DEEP-REFERENCE 3.2.0.

### Known limitations (accepted)
- **The motion laws are dramaclaw's field findings, not measured here.** Earned in dramaclaw's production corpus on Seedance; carried as `[EMPIRICAL — dramaclaw production corpus, Seedance]` per this repo's convention — strong heuristics to confirm on your own material, not guaranteed model behavior.
- **The audio bounds are a third-party measurement on the China Ark lane (2026-08, captured 400 errors) — NOT verified Higgsfield behavior.** Higgsfield's own proxy enforcement is unverified; the files say so and frame the total cap as the first suspect when a multi-clip attach fails, not as platform doctrine. `specs/` stays untouched (generated surfaces carry only snapshot-derived data).

## v3.26.0 — 2026-08-08

**The AI-VFX pipeline.** Higgsfield ran a public challenge — their host rebuilt a VFX artist's Iceland plate footage (character replacement, a cliff jump onto a dragon, a flight through a waterfall) using only Seedance 2.5, then built the same film again with no plate at all. Three sources came out of it: the *AI vs VFX* blog write-up with every production prompt, the 25-minute build video, and `prompt-builder-2-5.skill`, the prompt skill they published alongside. This release absorbs the **production doctrine** in them — the shot-building pipeline and its failure modes. The prompt-craft layer (block scaffold, FOV anchors, distributed style, optical techniques, the 4-mechanism extreme-FOV stack) was already house doctrine in `skills/higgsfield-seedance/SKILL.md` and is deliberately **not** restated.

### Added — `skills/higgsfield-seedance-2-5/VFX-PIPELINE.md`
`[FIELD — AI-vs-VFX, 2026-08-08]` + `[OFFICIAL — prompt-builder 2.5]`. The production layer under the 2.5 dialect:
- **Images first, then video** — and its consequence: a bad still cannot be rescued by the video prompt, so the cheap fix is always upstream.
- **One model per asset class**, not one per project: faces + corrective fixes → Nano Banana 2 · fantasy creatures → Seedream 5.0 · clothing → GPT Image 2 · locations → Soul Cinema (GPT skews yellow; Nano Banana makes locations too clean and symmetrical).
- Sheet construction: the **plain-grey-background law**, the **two-close-up creature sheet** (mouth open + mouth closed, so the jaw stops reshaping the skull), the **face-lock crop** (crop the heads out of the full-body panels so identity has exactly one source at the only resolution where it resolves), and small fixes as a *model switch plus one line* rather than a re-prompt.
- **The size-ref frame** — scale between two subjects survives as an asset, not a sentence: merge both sheets plus a known-good frame into one proportion reference, write the ratio in human-height comparisons, attach it to every shot, and carry the asymmetry lock (*if scale is uncertain, render smaller, never larger*) and the no-resize lock.
- **Locations batch cheap and select by light** — 7 credits buys one GPT Image 2 generation or ~56 Soul Cinema variations, so batch wide and judge; the four field rejection reasons are tabulated. Bad light in the still is the most common cause of a slop video. Plus the reverse-angle recipe with its explicit MATCH-TO-REFERENCE carry-over list (materials, grain size, palette, grade) and its dead-end lock against environment invention.
- **The `omni_reference` v2v lane.** The field footage-transformation workflow is **not** `video_edit` — it is `omni_reference` with the plate attached as a video reference, which is why `duration` is settable and **must equal the source**, and why the source must be **≥ 4 s** (the `duration` floor `[OFFICIAL — platform]`; pad a shorter clip by freeze-framing its last frame). Includes a four-row lane-routing table and the performance-inheritance clause (the `omni_reference` twin of Timeline Inheritance).
- **The four-batch rule** — the same defect across all four batches is a prompt or source fault, and further batching is burning credits. The diagnostic is *anchors*: v2v cannot render an action the plate has no anchor for. Fallback is i2v from a location screenshot, plus the **deliberate empty-frame pause** written into the prompt as an engineered stitch point.
- **The slop catalog** — "make it more natural" is a non-instruction (replace with a physical picture of the movement); the origami/low-poly wing; the CG-double fall (there are only two ways off a cliff, and a stiff soldier pose sliding at constant speed with dead clothing is neither); bad light; warped logos and colour casts; and the four take-selection rejections, which are performance notes rather than technical faults.
- **Direction patterns**: open mid-action, the cloud-punch opener, emotion with no video reference (what he says, how the voice sounds, what the hands do), the voice lock (2.5 locks voice with appearance in the character sheet, so describe it once in the role sentence), the high-speed kit (180° orbit + speed shake + lens droplets) with its two containment locks, and deliberate background improvisation as a word-budget decision.
- Cost/effort anchors from the build, quotable as comparisons rather than as a quote.

### Changed
- `skills/higgsfield-seedance-2-5/SKILL.md` — QUICK FACTS + Related rows for `VFX-PIPELINE.md`, and a Mode Router callout: **video-to-video is not automatically `video_edit`**. This is the routing correction with the most credit exposure in the release — a reader following the old text would send a subject-swap job to a mode that ignores `duration` and bills by the master's full length.
- `skills/higgsfield-seedance-2-5/MODE-PLAYBOOKS.md` — § Video editing opens with the lane check.
- `skills/higgsfield-seedance-vfx/SKILL.md` — scoped explicitly to the **2.0** v2v lane (4K, `mode=std`, platform start/end frames, genre hint), with a pointer to the 2.5 lane.
- `image-models.md` — new § Routing by Asset Class ahead of the per-model reference, with the batching economics and the fix-don't-rebuild rule.
- `skills/higgsfield-character-design/SKILL.md` — new § Sheet Construction Laws: the sheet as an *artifact* (grey background, two-close-up creature sheets, the face-lock crop, the size-ref frame, fix-don't-rebuild) alongside the existing content-side method.
- `evals/cases/seedance-2-5.json` — 2 new cases (9 total): `s25-v2v-routes-to-omni-reference` asserts a subject-swap request lands in `omni_reference` with duration matched to the source and a performance-inheritance clause; `trap-s25-four-batch-rule` asserts a repeated-failure report stops the batching and reaches for the i2v fallback rather than recommending more re-rolls.
- Routing: dispatcher row for replacing a VFX/3D pipeline with generation; sub-skill catalog row; README structure tree.

### Known limitations (accepted)
- **Not field-rated by O-Side.** This is Higgsfield's own production build, documented from their blog, video and published prompt skill — not measured on this repo's material. The `[FIELD — AI-vs-VFX, 2026-08-08]` label means "observed working in that build", not "verified here".
- **The ≥4 s source rule is inferred, not published.** The blog states it as a Seedance requirement for v2v; the platform snapshot has no video-reference minimum, only a `duration` floor of 4 s. The file says so, and derives the rule from the floor rather than asserting an undocumented constraint.
- The cost anchors (40¢ creature sheet, 7 credits → 56 Soul Cinema variations, the $50,000 comparison) are the build's own figures and its own framing; verify live before quoting prices (HARD RULE 3).
- The prompt-craft content of `prompt-builder-2-5.skill` was audited against the repo and found **already covered** (block scaffold, FOV anchor table, distributed style, observation pattern, snake cam, anti-impact locks, the 4-mechanism extreme-FOV stack, km/h and %/metre quantification). Two small items were judged not worth a surface of their own and are not carried: the sub-0.8s whip-pan-renders-as-hard-cut threshold, and the tele "compressed air column" phrasing.

## v3.25.0 — 2026-08-07

**Seedance 2.5 lands, and Higgsfield open-sourced their feature-film pipeline.** Two sources arrived together: ByteDance's *Dreamina Seedance 2.5 Prompt Guide* + *User Guide* (the model vendor's own doctrine for a model that is now live on Higgsfield), and Higgsfield's **Hell Grind** open-source brief — the production system behind their 95-minute AI feature, including the CINEDANCE prompt skill and its acting system. This release absorbs both, plus the Tier-2 spec refresh that Seedance 2.5's arrival forced.

### Specs (generated from the 2026-08-07 video dump)
- **Video +2**: `seedance_2_5` (Seedance 2.5 — four modes `t2v`/`omni_reference`/`video_edit`/`video_extension`, 4–30s, 480p/720p, `extension_mode` forward/backward, reference roles image/video/audio, **no start/end-frame role, no genre hint, no lane above 720p**) and `flux_3_video` (FLUX 3 Video, Black Forest Labs — T2V + multi-frame I2V + continuation with synchronized audio, 5–20s, 720p/1080p, the only catalog entry with a native 2:1 ratio).
- **Video −1**: `explainer_video` left the catalog (it had already dropped out of the CLI list at 2026-08-01). Noted in model-guide.md's utility list rather than silently removed.
- **Changed**: `grok_video_v15` gained `image_references` + `audio_references` roles — it is no longer I2V-only; the live CLI additionally reports three mutual-exclusion rules on it (references vs `start_image`, audio-refs require an image-ref, 1080p unavailable with references), recorded in model-guide.md. `minimax_h3` gained `batch_size` (1–4).
- Image and audio snapshots are unchanged and remain at 2026-08-01. CLI baseline re-accepted with `--update-baseline`; evals audited in the same PR (v3.11.3 lesson).

### Added — `skills/higgsfield-seedance-2-5/` (new sub-skill)
- `SKILL.md` — the omni-reference dialect: the four-mode router, the Higgsfield parameter surface with its three credit-relevant consequences (`video_edit` bills by source duration and ignores duration/aspect ratio; `video_extension` inherits the source ratio; there is no `genre`), reference roles that always pair "what to use" with "what not to use", the material budget (30 images / 10 videos / 10 audio, 50 total) with its stability ranges, the five-step multi-reference workflow, 30-second staging with explicit end states, timestamp pacing as a budget rather than an edit point, bracket syntax (`()` music · `<>` SFX · `{}` dialogue · `【】` subtitles), in-prompt first-last-frame and multi-keyframe control, observable-cue emotional direction, the niche-camera-term translation formula, the seven-slot real-person formula, a 2.0-vs-2.5 routing table, the hard-limits list, and a `[DREAMINA-ONLY]` table of product features Higgsfield does **not** expose (Ultra Long Video 180s, mark-based editing, Clay Renderer).
- `MODE-PLAYBOOKS.md` — the long templates: video editing (sole editing master, Timeline Inheritance, background-by-silhouette, audio-category editing, written-scope editing), forward/backward extension with the boundary-frame contract, storyboard grids, coarse-vs-fine blockouts, one-click video, seamless transitions plus the 11-entry named transition vocabulary.
- `templates/seedance/omni-reference-2-5.md` — paste-ready multi-reference brief with a filled example.
- `evals/cases/seedance-2-5.json` — 7 cases including two stale-spec traps (`video_extension` without `extension_mode`; 1080p on a 720p-capped model).

### Added — `skills/higgsfield-seedance/HELL-GRIND.md`
`[OFFICIAL — Higgsfield "Hell Grind" open-source brief]`. Deliberately scoped to what the repo did **not** already have — the CINEDANCE prompt doctrine was already harvested as § Official Prompt Architecture and is not restated:
- **Asset construction**: the descriptor+reference pair; the three-panel character sheet with a **headless front figure** (so wide shots cannot source the face from a blurry thumbnail); boring-on-purpose sheets; point changes made in NBP/Seedream then **mask-composited back onto the original**, because an image never runs through a model twice in full.
- **Location sheets**: 3/4 not frontal, an anchor object to stage against, one light logic, and two reverse-angle recipes (corner generation; or a walk-through video screenshot + texture pass).
- **The GEO SPATIAL LAYOUT block** — a per-scene floor plan with no people in it, pasted unchanged into every shot of that scene. Distinguished from the existing per-shot Spatial Layout Block.
- **The position-fixing first second** — a ~1.0s populated wide with no action, the "hm" trick, and the previous-line-tail seam trick. Reconciled explicitly with the Non-Empty Opening Frame pattern (it withholds *action*, never *people*).
- The `EXACT N CHARACTERS — NO DUPLICATES` header and counted furniture bans; the CHARACTER ACTING / STYLE / QUALITY blocks; the closing technical tag tail; wording rules (present tense, ≤3 sentences per beat, 3,000–4,000-word production prompts, positive-form actions, the ban dictionary); dialogue construction with the anti-ad-lib block and mix notes; INNER (unspoken), phased blinking, and the one-micro-event-per-1–2s rule; the surgical one-line iteration loop and the **10–15 rule** (if a shot has not converged, simplify the shot, not the words); crowds as one asset with an explicit count, threshold transitions, and the giant SCALE LAW with its named failure condition.

### Added — `skills/higgsfield-acting/` (new sub-skill)
The performance craft layer, distinct from FACS's muscle codes: acting as behavior under pressure; the five pillars (objective / obstacle+stakes / tactics / beats / subtext); listening markers; body parameters, business and the interrupted-action accent, proxemics as drama, status and status breaks; the **150–220-word acting master profile** with fixed block order, tics-with-triggers, named gaits, and the mandatory "However, when X…" mask-crack; mandatory eye life; scene adaptation that transforms rather than deletes; the locked voice prompt; states-not-transitions; ensemble wave reactions; a 15-symptom atlas of bad acting with prompt-level fixes; the 0–5 performance scale with the two-truths rule; a pre-send checklist and a worked master-profile-plus-adaptation example.

### Changed
- **Age contradiction resolved.** `skills/higgsfield-seedance/SKILL.md` § Tag naming carried the official skill's `age + role/build` template while engine rule 1 forbids age words in either language. The Hell Grind brief supplies the mechanism — the content filter tightens sharply the moment it reads a minor — so the `@TAG:` line now reads role/build first with an explicit no-age note, and the same override is stated in the 2.5 skill's real-person formula (whose source guide labels slot 1 `[Age/Race]`).
- `scripts/seedance_lint.py`: `extension_mode` is now a first-class setting (header pattern + `--extension-mode` flag), and two cross-parameter rules that `sync_specs.py` cannot extract from prose are encoded — `extension_mode` required for and only for `video_extension` (FAIL), and `video_edit` ignoring duration/aspect ratio (WARN). Both key off the model's own parameter list rather than a hard-coded id, so they disappear if the platform drops the parameter.
- `evals/run_evals.py`: the two new rules joined `ENUM_RULES` so trap cases can assert on them.
- Routing: dispatcher rows for Seedance 2.5, the 2.0-vs-2.5 tiebreaker, character performance, and the film pipeline; sub-skill catalog and `sub_skill_descriptions.py` updated; model-guide.md gained Seedance 2.5 + FLUX 3 rows, an existing-video branch and a >15s branch in the decision flowchart, and the 2026-08-07 delta note.
- README: version + specs badge, feature list (three new bullets), structure tree, template count, footer.

### Known limitations (accepted)
- **Seedance 2.5 and FLUX 3 Video are not field-rated.** No star ratings in model-guide.md until real generations back them; the 2.5 doctrine is vendor-official prompt grammar plus the platform's own parameter surface, not O-Side production experience.
- The `[DREAMINA-ONLY]` features (Ultra Long Video 180s, mark-based frame annotation, Clay Renderer) have no Higgsfield equivalent; the documented workarounds (30s + extension chains, written edit scopes, blockout prompting) are structural substitutes, not the same capability.
- Hell Grind's numbers (3,000–4,000-word prompts, the 10–15 rule, three-or-four voices per character) are that production's calibration, not measured on this repo's material.


## v3.24.0 — 2026-08-01

**Tier-2 spec refresh — 2026-08-01 snapshots.** CLI re-authenticated; `refresh_specs.py` flagged real drift since 2026-07-05, so all three catalogs were re-dumped from `models_explore`, specs regenerated, evals audited, and the CLI baseline re-accepted. Lands 4 days before the old snapshots would have crossed the 30-day trust line (which v3.23.0 made a `--strict` failure).

### Specs (generated from the 2026-08-01 dumps)
- **Video +3**: `minimax_h3` (MiniMax H3 — multimodal keyframes + image/video/audio refs, 5–15s, 2K, 21:9), `happy_horse_video` (T2V/start-frame, 3–15s, 720p/1080p), `sync_so` (Sync Lipsync 3, pipeline tool). Nothing removed.
- **Image +1**: `seedream_v5_pro` — the v3.22.0 "verify live before citing enums" flag is now resolved: in-snapshot with `resolution` 1k/1.5k/2k (default 2k) and 21:9. `seedream_v5_lite` gained 21:9.
- **Audio +1**: `qwen_audio_tts` (Qwen Audio 3.0 TTS Flash — expressive `instruction` direction, preset/cloned voices, 13 language hints); documented in higgsfield-audio's catalog table.
- CLI-surface deltas recorded in `cli_baseline.json` (accepted with `--update-baseline`): `nano_banana_2` and `explainer_video` left the **CLI** list but remain in the models_explore catalog; `grok_video_v15` gained 1080p; Topaz's CLI param surface was reshaped.

### Changed
- Snapshot-date stamps refreshed everywhere they are load-bearing: README badge, image-models.md header + Soul Cast / GPT Image notes, higgsfield-audio catalog section (incl. heading anchor), model-guide sourcing note, and the eval golden responses that cite a snapshot date (facts re-verified against the new dump).
- model-guide.md: "new in catalog — not yet field-rated" note for MiniMax H3 + Happy Horse (no invented star ratings), Sync Lipsync 3 added to the out-of-scope utility list.

### Known limitations (accepted)
- MiniMax H3 and Happy Horse Video have specs coverage but no prompt doctrine or comparison-table rows yet — pending real generations.
- Sora 2 remains UI-only (absent from the API/MCP catalog).


## v3.23.0 — 2026-08-01

**Council remediation wave.** A three-model council audit (Codex gpt-5.6-sol + Gemini 3.1 Pro + Opus, 2026-08-01) of v3.22.1 found that the harvest wave changed the doctrine while the enforcement layer — linter, validator, evals, dispatcher, templates — still implemented the old one. All verified findings fixed.

### Fixed — doctrine reaches the enforcement layer
- **Regime-aware pre-flight linter** (`seedance_lint.py`): the 220-word FAIL / 180-word WARN now govern the short-form regime only. Block-scaffold production prompts are auto-detected (4+ canonical block labels, or 2+ shot markers) and exempt per HARD RULE 8; `--regime auto|short|block` forces it. Previously the mandated shotlist workflow (218–2,059-word copy-blocks piped through the linter) could never pass its own preflight — and `tests/test_lint_rules.py` codified the bug.
- **"shot" false positive killed**: the violence-verb rule matched `\bshot\b` bare — failing "two-shot", "wide shot", and "one shot per scene" in a film-prompting tool. Now fires only on verb/violence constructions ("was shot", "shot him").
- **Style Prefix doctrine reconciled as regime scoping**: connected shotlists ship the compiled prefix **verbatim** (the field-proven Style-Prefix-plus-SHOT shape observed across the harvested corpus); standalone block prompts distribute style into home blocks. seedance § Distributed style, shotlist-director § Per-scene prompt law, and `templates/seedance/global-style-prefix.md` now each state their regime and cross-link the other. The field-calibration bullet no longer claims "only the distributed form ships" — the corpus says otherwise.
- **Negative-phrasing law scoped to its real target**: `negative:` lists / bare negation lists are banned; short lock tails inside declarations ("no 3D render", "no flicker" — the law's own canonical example) are fine and field-proven. Template note + seedance law scope updated.
- **The mandatory prompt skill finally carries the regime carve-out** (`higgsfield-prompt`, the file HARD RULE 2 makes mandatory on every prompt request): QUICK FACTS 200-word + Seedance 30–100w lines, § Keep it under 200 words, and § Intent over Precision all scoped; likewise troubleshoot's blur table + diagnostic tree, MODELS-DEEP-REFERENCE's Kling prompt note, and seedance's 50–80w sweet spot.
- **Fast Path Seedance runtime exception** (root dispatcher): Seedance 2.0 never gets a silently defaulted 8s — no-duration Fast Path requests route to Kling 3.0; Seedance-by-name states the assumed runtime as the first adjustable.
- **Aspect-ratio enum leaks closed**: Full Path no longer offers 2.35:1 as an output ratio; `Aspect:` headers in templates 04/05/06 and prompt-examples now carry legal enums (Kling/Sora → 16:9, Seedance → native 21:9) with anamorphic kept in the Style line where HARD RULE 7 puts it.
- **Model data corrected against specs**: Kling 2.6 HAS native audio (`sound`, default on) — models sub-skill table + decision tree fixed; Seedance 2.0 10s → 4–15s, Seedance 1.5 Pro → 4/8/12s; discrete duration enums no longer written as ranges (Veo 3.1/Lite/Fast 4/6/8s, Wan 2.6 5/10/15s, Hailuo 6/10s, Kling 2.6 5/10s) in model-guide + models sub-skill.
- **Worked example de-milimetred**: two-character Seedance template now speaks FOV 63° with anamorphic as optical character, per the FOV-anchor law.
- **Iteration anchor**: seedance § Field calibration "50–100" → the corrected 65–100 generations per kept shot.

### Added — gates that catch this class of drift
- **`validate.py`**: spec-snapshot staleness now FAILS `--strict` (release must not ship specs the HARD RULES disown) and the age gate covers image + audio spec files (previously ageless); duration cross-check gains name-index overrides (Kling 3.0/2.6, Wan 2.6, Veo 3.1 Lite, Seedance 1.5 Pro +) raising coverage 12 → 16 rows, a ≥14-row coverage floor, and range-vs-enum tightening ("4–8s" against [4,6,8] now fails); **rule-8 restatement scan** over every sub-skill, template, and the PDF generator — any unqualified 200-word-cap copy fails validation (it immediately caught two copies the council itself missed); dispatcher parity now requires a routing-TABLE row, not a prose mention.
- **Evals**: new `word_count` assertion type — the `prompt-under-200-words` case now actually asserts the cap; new `harvest.json` suite (6 cases): block-scaffold cap exemption end-to-end, FOV-degrees-not-mm, CAMERA-3rd position, environment-invention lock, 15s-envelope beat tiling, character-height lock. 43 → 49 cases.
- **`seedance_lint.py` structural**: beat-timeline shape checks (gaps, overlaps, late start, envelope undershoot — previously only overshoot); declared-shots-with-no-structure WARN; snapshot-age INFO on enum verdicts past the 30-day trust line.
- **`sync_specs.py`**: refuses to generate from a snapshot with no items or none of the requested type (a truncated dump could previously write empty specs and exit 0).
- **`build_index.py`**: GitHub-style duplicate-heading suffixes (`#continuation` / `#continuation-1`) in INDEX.md.

### Changed
- **USER-GUIDE PDF content refresh**: image-model table gains GPT Image 2 (text/logo) + Seedream 5.0 Pro (anime/manga sheets); short-form length guidance regime-scoped; release-history FAQ no longer ends at v3.8.1.

### Known limitations (accepted)
- `specs/` snapshots remain dated 2026-07-05 — they cross the 30-day trust line on 2026-08-05 and `--strict` will then fail by design until a Tier-2 refresh; the `higgsfield` CLI session must be re-authenticated first (`higgsfield auth login`).
- Sora 2 aspect ratios are undocumented (UI-only model) — its example headers use 16:9 as the conservative legal value.


## v3.22.1 — 2026-07-26

**Post-release audit fix pass.** A two-agent audit of v3.22.0 (cross-reference integrity + repo hygiene) found no broken references but six substantive contradictions between new and pre-existing rules, plus stale downstream copies of the old 200-word rule. All fixed.

### Fixed
- **The ~2,500-character "practical limit" scoped as ZH-derived** (seedance 1.11.1 § Shot density): it contradicted the same file's new Field-calibration medians (1,433–2,059w). EN block prompts have no character analogue; ZH keeps the 1,800-char hard cap. Section now cross-links the fuller shotlist-director density heuristic.
- **Runtime-default contradiction resolved** (shotlist-director 1.1.1): auto-enrichment no longer silently defaults to 8s — inside a shotlist the 15s envelope law governs; standalone prompts keep seedance's "always ask for runtime, never default."
- **Duration ladder vs 15s target reconciled** (shotlist-director): 15s is the default envelope, not a straitjacket — a scene that fills only 4–8s ships as a deliberately shorter clip rather than padded dead air.
- **Cut-density norms scoped by register** (shotlist-director): "1–3 cuts per 15s" is the live-action narrative norm; stylized recipes (3D-animated 6/15s, product montage) are denser by design, cross-linked to style § Style Recipes.
- **mm-vs-FOV leak closed** (shotlist-director + camera 3.4.1): auto-enrichment lens defaults now speak FOV degrees for Seedance block prompts (63°/47°/29°); the camera lens table carries FOV equivalents per row and flags 45mm-macro as having no FOV anchor.
- **FACS micro-beat recipes capped** (facs 1.1.1): recipes declared menus, not checklists — pick 2–4 tells per beat; the 3–4-expression cap's logic applies to physical beats.
- **HARD RULE 8 word band corrected** (root 3.22.1): "500–2,000+" → the actual harvest ladder "218–2,059-word medians".
- **Iteration-anchor arithmetic corrected** (production-benchmarks): 65–100 generations per kept shot (matches the 1.0–1.5% band; was 50–100), and the "16 finals" figure re-scoped to the most-iterated scene, not per-scene.
- **Grey-sheet hex reconciled** (ad-asset-prep): `#7f7f7f` creature / `#8a8a8a` human both proven — the rule is pin ONE exact hex per project; added back-links for populated-plate reuse and the canonical Soul ghost-mannequin recipe.
- **Motion caveat provenance split** (motion 3.2.1): catalog stats (~100 presets → ~1,900 variants) attributed to the live catalog pull, not the project harvest.
- **Stale 200-word copies given the regime carve-out**: troubleshoot 3.0.1 (fix bullet + pre-gen checklist item), audio 3.3.2, `scripts/generate_user_guide.py` tip (the v3.22.0 PDF had shipped with the old unqualified rule), and the eval-case description in `evals/cases/prompt.json`.


## v3.22.0 — 2026-07-26

**The harvest wave.** Absorbs the 13-project community-corpus harvest (2026-07-18: 13 shared Higgsfield projects, 9 creators, ~4,000 production prompts pulled with full params) plus the previously-unported assets from Higgsfield's own skill family (shotlist-builder, seedance-2-pro-director, cinematic-prompt-builder). Chinese-source material re-authored in English.

### Added
- **higgsfield-seedance 1.11.0**:
  - *Field calibration — the 13-project production corpus* `[FIELD]`: word-length ladder by register (218w → 2,059w medians — the 50–80w sweet spot is confirmed single-shot-only), register contraction for stylized work, Style Prefix as per-project compiled constant, video briefs hand-authored (`enhance_prompt` off on video / on for images), observed platform-layer Seedance params (`multi_shot_mode: custom`, `speedramp`, `bitrate_mode`).
  - *Three "helpful-instinct" drift sources* with standing locks in POSITIVE LOCKS: environment invention (**the #1 drift source, above character drift** — "the set contains only what the reference shows"), character-height equalization (heights written into every 2+ character prompt), scale drift on wides.
  - Measurable-language additions: masses/sizes in real units for PHYSICS ("50–70 g — it falls gently"), causal prop interaction ("a button press is contact, 2–3 mm travel, click, spring-back — screen lights only AFTER the click").
  - Extension prompting: *feed the tail, not just the frame* — the final 3–4 seconds as `@video` reference carries motion through the join.
  - *Build-safe construction* `[OFFICIAL — cinematic-prompt-builder]` in the Rewrite Playbook: evacuated-city / energy-standoff / contained-fight / uninhabited-terrain substitutions, containment-doubles-as-physics, the safe benchmark scene.
  - PRODUCTION-PATTERNS gains a `[FIELD]` section: selective motion blur as artifact concealment, HEX-array color lock, generate-forward-reverse-in-edit, populated-plate reuse, off-screen transformation staging.
- **higgsfield-camera 3.4.0** `[OFFICIAL — shotlist-builder]`: lens+aperture by shot purpose (85/100mm F1.4 ECU … 45mm macro F2.8) with focus-lock + distortion-forbid clauses, shot-duration-by-type table (0.3–0.5s flash establish → 8–15s full-arc CU), exact-distance micro-move rule (10–15 cm over 7s).
- **higgsfield-facs 1.1.0** `[OFFICIAL — shotlist-builder]`: *Physical Micro-Beats — the Body Beyond the Face* (7 register recipes: throat/breath/skin/posture, incl. suppressed-emotion-as-resistance), anti-AI-video defaults (no tears unless scripted, 0.3–0.5s group-reaction stagger, listeners-in-bokeh are not statues), *every line gets three beats* (pre/during/post-line), the anti-AI test.
- **higgsfield-shotlist-director 1.1.0** `[OFFICIAL — shotlist-builder + pro-director]`: *Prompt density* — group-when-ALL-5 / split-when-ANY-5 heuristic ("don't fragment grief"), complexity budget + duration ladder, err-toward-more-prompts, auto-enrichment defaults for thin briefs.
- **higgsfield-style 3.1.0**: *Register Poles* `[FIELD]` (film vs broadcast-TV vs stop-motion-on-twos vs anime-cel — the style-anchor slot swaps vocabulary by register; one saturated accent reserved for the story) + *Style Recipes* `[OFFICIAL — cinematic-prompt-builder]` (8 proven shapes: live-action epic, 3D animated 6-shots/15s, game cutscene + pinned HUD, gameplay, FPV oner, product packshot, VFX composite INPUT LOCK, kaiju containment).
- **image-models.md**: Seedream 5.0 Pro (`seedream_v5_pro`) `[FIELD]` — anime/manga sheet + manga-page dialects, art-era anchoring; flagged as absent from the 2026-07-05 spec snapshot (verify live).
- **production-benchmarks.md**: *Community-corpus anchors* — 13,626 generations for a 2–3-min solo short, TESTS = 61% of the project, 50–100 generations per kept shot (consistent with Hell Grind's 1.0–1.5%), the five-bucket folder discipline, best-second splice culture.
- **templates/ad-asset-prep.md**: exact-hex grey sheet spec (#8a8a8a) `[FIELD]`, sibling-face derivation ("spitting image, translated onto…"), ghost-mannequin outfit panel, reverse-angle plates as first-class elements (the 180°-line mechanism), master-plate exposure normalization.
- **templates/seedance/global-style-prefix.md**: *Field specimens* — the one-axis-per-clause anatomy across the corpus, per-world camera-grammar maps, the reserved-accent discipline, register-aware prefixes; audio policy documented as a project choice, not a law.
- **higgsfield-motion 3.2.0**: scope caveat `[FIELD]` — none of the 13 harvested film productions used a motion preset; presets are the viral-effects product (~100 unique names → ~1,900 per-model variants), film work free-prompts its camera.

### Changed
- **HARD RULE 8 regime carve-out** (root SKILL.md): the 200-word cap now explicitly governs the short-form MCSLA regime only; block-scaffold production prompts replace the cap with structural lint (harvest medians 500–2,000+ words by register).
- **Camera-block-at-bottom claim RESOLVED** (was "test day pending" since v3.21.0): rejected on field evidence — across ~4,000 harvested production prompts the CAMERA block sits mid-document, never at the bottom. CAMERA-3rd stands.


## v3.21.0 — 2026-07-14

### Added
- **higgsfield-seedance 1.10.0 — two new Prompt-Craft Laws** (2026-07-14):
  - *Ambiguous verbs — the homograph trap* (Peter's field find, covered by no
    known prompt guide): if a verb/noun has a plausible second reading
    ("tearing" = rip vs cry), the model may take it — replace with the phrasing
    only one thing can look like; ships with a seed homograph list.
  - *Community v3 cherry-picks* (Joey drop, audited vs this skill): camera on
    the shadow side + stated operator axis, detail-on-wide "snake cam",
    intimate wide, prompt-reset heuristic, canonical-over-plate,
    contrast-curve-stated-three-ways. Their camera-block-at-bottom claim is
    flagged, not adopted (contradicts CAMERA-3rd; test day pending).


## v3.20.1 — 2026-07-06

### Changed
- **Sora 2 UI presence confirmed** (user screenshot of the live model picker, 2026-07-06): the v3.20.0 "verify in the live UI" caveat is upgraded to fact. It is a **4-variant family** — Sora 2 (720p) / Sora 2 Pro (1080p) / Sora 2 Max / Sora 2 Pro Max (both 1080p, "BY HIGGSFIELD" enhanced tiers), all 4–12s, multi-shot with sound generation — present in the UI but still absent from the API/MCP catalog (UI generations only). model-guide.md row now carries the variant lineup and real duration/resolution; root SKILL.md and `higgsfield-assist` (3.1.1) caveats updated to the confirmed wording.


## v3.20.0 — 2026-07-06

**Audio specs pipeline + catalog-reality refresh.** The specs layer now covers all three output types end-to-end, the dispatcher gained a Load Map, and the two stalest model surfaces (higgsfield-assist, the Sora 2 / "Seedance Pro" mentions) were reconciled with the live catalog.

### Added
- **Audio specs pipeline**: `scripts/sync_specs.py --type audio` generates `specs/audio-model-specs.{yaml,json}` + `specs/AUDIO-MODEL-SPECS.md` from the dated audio snapshot (5 models incl. `seed_audio`); `scripts/refresh_specs.py` default is now `all` (video+image+audio — `both` kept as the pre-audio alias), audio captured into `specs/cli_baseline.json`, tripwire green across all three types. Typed-spec markdown footers now point at their own machine twins (was: everything pointed at the video files). `higgsfield-audio` 3.3.1 cites the generated audio specs.
- **Load Map** (root SKILL.md § Load Map — how much to read): a situation → cumulative-load table so multi-skill loads are deterministic instead of vibes — Fast Path loads two files, everything else adds only what its routing row names.

### Changed
- **Sora 2 is UI-only** — absent from the API catalog and a live `models_explore` search (verified 2026-07-05). Kept everywhere but annotated: root SKILL.md "What Is Higgsfield?", model-guide.md (video-table row, decision flowchart demoted to parenthetical, camera-control + motion-preset † footnotes, credit table), higgsfield-assist. Root Fast Path default swapped Sora 2 → Seedance 2.0 (action/scale/references).
- **"Seedance Pro" is a legacy UI label** — not in the catalog; annotated in model-guide + assist as superseded by Seedance 1.5 Pro (`seedance1_5`) and Seedance 2.0 Fast/Mini (annotate-don't-delete, per the GPT Image precedent).
- **`higgsfield-assist` 3.0.0 → 3.1.0** (first refresh since 2026-04-06): credit-cost tier roster rebuilt against the 2026-07-05 catalog; "Kling 3.0 for anything needing audio" corrected — audio is native across Seedance 2.0/Mini/1.5 Pro (`generate_audio`), Kling 3.0/2.6 (`sound`), Veo 3.1 Lite: pick by scene fit, then toggle; plans table now carries a dated verify-live caveat; audio-toggle credit-saving tip added. Kling 2.6 audio cell in model-guide fixed to match the live spec (`sound` param, default on).
- **CS3.5 shot-counter TODO closed** (`higgsfield-cinema`): API checked 2026-07-05 — `multi_prompt` exposes no maximum and no constraint rule, so the observed cap of 4 is UI behavior the API doesn't document; treat 4 as the working limit, verify live before promising more.
- CLAUDE.md: specs/ line + sync command now cover all three types.


## v3.19.1 — 2026-07-06

Housekeeping wave: activate the weekly spec-drift schedule, absorb the CLI 1.1.5 release, de-clutter the repo root, and archive the changelog backlog. No prompting-content changes.

### Changed
- **Spec-drift schedule is LIVE**: `HIGGSFIELD_CREDENTIALS` repo secret added; a manual `workflow_dispatch` run verified the full path end-to-end (install → version guard → tripwire → issue-on-drift). The run surfaced CLI **1.1.5**, which *restores* the per-param `enum` lists that 1.0.1 dropped (and keeps `job_type` + CEL rules) — the tripwire regains full enum visibility with no parser change. Local CLI upgraded, baseline re-captured with 1.1.5, `LAST_VERIFIED_CLI` bumped 1.0.1 → 1.1.5, drift issue #78 closed as a cross-version artifact.
- **Root scripts consolidated into `scripts/`**: all 9 Python tools (`validate.py`, `build_index.py`, `sync_specs.py`, `refresh_specs.py`, `higgsfield_memory.py`, `seedance_lint.py`, `generate_user_guide.py`, `validate_user_guide.py`, `sub_skill_descriptions.py`) moved via `git mv`; internal `__file__`-derived roots, test/eval importers, CI workflows, slash commands, CLAUDE.md, README, DISCIPLINE.md, and 14 skill files updated. Commands are now `python3 scripts/validate.py` etc. Root .md/.py clutter roughly halved.
- **CHANGELOG archived**: entries v3.0.0–v3.14.1 (69 releases, ~375 KB) rolled verbatim into `docs/archive/CHANGELOG-v3.0-v3.14.md`; root CHANGELOG keeps the current era (v3.15.0+) plus a pointer.


## v3.19.0 — 2026-07-05

**Seedance 4K Masterclass + Seed Audio 1.0** — content wave from six sources gathered 2026-07-05 (plan: `workspace/output/V3.19-PLAN.md`): Higgsfield's own downloadable `prompt-writter.skill`, the official Seedance-4K film tutorial (video + blog, 25 verbatim prompts archived in `workspace/input/`), spec-verified Seed Audio 1.0 research, a cross-surface video-extension workflow, selected field imports from the community seedance-2.0 repo (v6.6.0), and a character-audition system prompt. Every model claim checked against the fresh 2026-07-05 specs snapshots (shipped in v3.18.1). Provenance tiers used throughout: [OFFICIAL] / [DEMO] / [EMPIRICAL] / [FIELD].

### `higgsfield-seedance` 1.8.2 → 1.9.0
- **§ Official Prompt Architecture — the Block Scaffold** [OFFICIAL — Higgsfield prompt-writter.skill]: the 17-block scaffold (SCENE CONTEXT → POSITIVE LOCKS), distributed-style doctrine (no style prefix), FOV-in-degrees anchor table + CAMERA-3rd-position rule, measurable-language rules (positive-only, km/h, %/meters, human-height scale, left/right-from-camera, Kelvin WB, no director/equipment names), POSITIVE LOCKS, the cut-format ladder + 6-cut vocabulary, tag naming + minimal-reference-text, context isolation, and 4 special protocols (extreme-FOV 4-mechanism stack, whip-pan ≥0.8s, anti-impact locks, observation pattern). Reconciled as a "two regimes" doctrine with the existing six-slot short form; official no-director-names rule noted as overriding the empirical director-substitute trick in block prompts.
- **NEW reference `PRODUCTION-PATTERNS.md`** [DEMO — Seedance-4K film tutorial]: reference-role vocabulary ("100% matches the reference" / "STYLE REFERENCE ONLY, model extends the world" / "VARIETY reference" + the clone-army fix), coordinate blocking (x%/y%, % of frame width, locked screen direction), non-empty opening frame, per-segment LENS LOCK + timed SMASH/MATCH cuts, red-arrow prop annotation, video-reference 1:1 lock + SCREEN REALISM block + duration-match rule, prompted-imperfection realism, 60:30:10 grade, offscreen voice-only characters, specify-what-plays-on-screens, in-prompt scene transitions.
- **§ Extension Prompting — Video-Reference Continuation** [EMPIRICAL]: "The scene continues." / "Show me what happens before" openers, occluded-identity `@ImageN` binding, match-source-resolution-AND-duration, chain-degradation + B-roll chain-break, camera-angle-change endings; [FIELD] source-carries-state + references-outrank-text + chain cap ~2 (hard 3) with re-anchor-from-ORIGINAL-references.

### `higgsfield-audio` 3.2.2 → 3.3.0
- **§ Scene-Audio Generation — Seed Audio 1.0**: what it is (one-pass whole-scene audio, released 2026-06-23), decision table vs `text2speech_v2` vs Seedance `generate_audio`, verified surface [OFFICIAL — 2026-07-05 audio snapshot] (params, ≤3 audio refs ≤30s XOR 1 image ref, `@Audio1..3` tokens), script-format prompting clearly labeled [EMPIRICAL — community, NOT official] with a worked example.
- Standalone Audio catalog reconciled with the live 5-model catalog (incl. NEW `cozy_voice` engine; game-pipeline-only tools flagged), date-stamped 2026-07-05.
- [FIELD] per-language dialogue-sync budget table (EN ~16–20 reliable-sync words per ~15s, Mandarin strongest, RU weak) + voice-reference lip-sync path (rights-sensitive) under Lip-Sync Rules; Supercomputer voice-over pointer [DEMO].

### `higgsfield-pipeline` 3.3.0 → 3.4.0
- **§ Continuation & Extension Handoff**: extend-a-clip workflow, chain management (depth caps + scheduled re-anchoring), source-carries-state rule (stills can't carry motion/camera/audio phase), clean-join planning (angle-change endings, last-channel-on-TV transition trick, post-edit seam note).

### `higgsfield-soul` 3.6.1 → 3.7.0 + asset-prep surfaces
- Two-image character floor (face + full body) + grey-sheet rule [DEMO]; **§ Split-Panel Outfit-Change Sheet** (ghost-mannequin + identity panel); **§ Variety Sheets — Crowds Without Clones**.
- `templates/ad-asset-prep.md`: grey-background canonical home, **§ Location plates (3/4 angle, empty by default)**, **§ Which model makes the sheet** (GPT Image 2 4K → Nano Banana Pro on flatness → Soul Cinema for locations/characters); Elements registration.
- `skills/higgsfield-gpt-image-2/reference-sheet-workflow.md`: **§ Views the video will need** (front/side/back + BOTTOM/undercarriage for flip shots), **§ Red-arrow annotation**.

### `higgsfield-character-design` 1.0.0 → 1.1.0
- **§ Screen Test / Audition** [EMPIRICAL]: casting read → role options → playable audition lines → voice triggers (≤3 qualities) → final audition prompt (<3500 chars) with divergence rule and a worked mini-example; cross-linked to FACS (direct the takes), Soul (lock the winner), and ad-asset-prep's generate-many → test-in-motion → lock-the-winner loop.

### `higgsfield-models` 3.1.1 → 3.2.0 + guides
- New model rows [spec-verbatim]: **Gemini Omni Flash** (video), **Soul Cast**, **Soul Location**, **Nano Banana 2 Lite**, **OpenAI Hazel** (image) across model-guide.md, image-models.md, and higgsfield-models (dual-maintained tables kept in sync); recraft id rename + Seedream 4.5 quality tiers reconciled; GPT Image (original) noted as gone from the 2026-07-05 catalog; utility jobs scoped out with a one-liner.

### Root + examples + evals
- `prompt-examples.md`: **§ Seedance-4K Film Tutorial — Worked Examples** — five annotated verbatim excerpts [DEMO] (prompted imperfection, coordinate blocking + LENS LOCKs, 1:1 video reference + SCREEN REALISM, red-arrow lock, VARIETY-reference before/after).
- Root SKILL.md: four new routing rows (standalone audio / Seed Audio → audio; extend-continue a clip → seedance + pipeline; asset prep / reference sheets → ad-asset-prep + gpt-image-2 + soul; character audition → character-design). Root version → 3.19.0.
- Evals: +3 cases (Seed Audio scene script, standalone-vs-in-video audio choice, extension continuation) — 43 total.

## v3.18.1 — 2026-07-05

Repair wave: un-blind the spec-drift tripwire after the Higgsfield CLI 1.0.1 output-shape change, refresh the specs snapshots (Tier 2, 13 days early — the shape change forced it), and clear the stale-docs debt found by a full repo audit. No new prompting content (that ships in v3.19.0).

### Fixed
- **`refresh_specs.py` crashed on CLI 1.0.1** (`KeyError: 'job_set_type'` — upstream renamed the id key to `job_type` and dropped per-param `enum` lists). Now accepts both key generations via `_model_id()`, and any future output-shape change raises a typed `ShapeError` → **new exit code 4** ("fix the parser") kept distinct from exit 1 ("re-auth") — previously a crash masqueraded as auth expiry in `spec-drift.yml`. The workflow gained a dedicated exit-4 step and a `LAST_VERIFIED_CLI` version guard (warns, never fails, on unverified upstream releases). Fixture-based regression tests added from recorded CLI 1.0.1 JSON (`tests/fixtures/cli_1_0_1_*.json`); 25 tests in `test_refresh.py`.
- **New CEL-rules comparison channel**: CLI 1.0.1 ships machine-readable constraint rules (e.g. Seedance's 9-image/3-video/3-audio/12-total reference caps, `mode='fast'` forbids 1080p/4k) — exactly the cross-constraint prose the tripwire was historically blind to. `cli_view()` now captures them; added rules = DRIFT, removed = notice; the channel only compares when both sides carry it (pre-1.0.1 baselines stay silent).
- **`sync_specs.py` lost the duration envelope**: 2026-07 snapshots moved `duration_range` into a `duration` *parameter* (min/max), which silently dropped `spec["duration"]` and broke `seedance_lint`'s `duration-out-of-range` rule — caught by the `trap-seedance-overlong-duration` eval (the v3.11.2 stale-eval trap working as designed). The envelope is now derived from the duration parameter; param `min`/`max` are preserved in generated specs.
- **`model-guide.md` Seedance 2.0 Mini row**: "UI label; not a distinct API id" is no longer true — `seedance_2_0_mini` is a distinct catalog id (4–15s, 480p/720p, full image/video/audio reference surface, native audio).
- **Broken link** `templates/ad-asset-prep.md` → `../docs/production-benchmarks.md` (file lives at repo root). `validate.py` now sweeps `templates/**/*.md` path-style refs (new `[ TEMPLATE PATHS ]` section) so this class can't recur.
- **Stale docs**: `photodump-presets.md` image-snapshot TODO (the snapshot has existed since 2026-06-22); CLAUDE.md counts (30 sub-skills, full templates/ inventory), specs/ description, missing release-gate commands (`--strict` + pytest + evals), release-ceremony pointer (tag the merge commit; PDF is an untracked artifact), and stale `/project:*` slash names (now `/validate`, `/release`). `release.md` step 1 now runs all three gates, not just strict validate. Dropped `Edit(mnt/**)` from `.claude/settings.json` — it invited exactly the mistake the mnt rule forbids.

### Changed
- **Specs snapshots refreshed** (video + image, 2026-06-22 → **2026-07-05**) and a **first audio snapshot captured** (`models_explore_snapshot_audio_2026-07-05.json`: `seed_audio` = **Seed Audio 1.0**, `sonilo_music`, `mirelo_text_to_audio`, `inworld_text_to_speech`, `text2speech_v2` with a new `cozy_voice` engine) — machine-readable ground truth for the v3.19.0 Seed Audio content; the audio sync pipeline is a follow-up.
- Snapshot deltas absorbed: video +`seedance_2_0_mini`/`gemini_omni`/`explainer_video` + utility jobs; image +`nano_banana_2_lite`/`soul_cast`/`openai_hazel`/`recraft_v4_1` (renamed from `recraft-v4-1`) + utility jobs; `seedance_2_0` media roles renamed to `image_references`/`video_references`/`audio_references` (+ kept `start_image`/`end_image`); id renames recorded as spec **aliases** via `HISTORICAL_IDS` (`seedance_1_5`→`seedance1_5`, `recraft-v4-1`→`recraft_v4_1`, dropped `video_standard` dup) so ledger rows and user inputs written under old ids keep resolving.
- CLI baseline re-accepted at 2026-07-05 (tripwire green end-to-end: 0 fresh / 3 change / 1 pull-failed / 4 shape-changed all exercised).
- Root SKILL.md: Shared Resources table now lists all 8 `templates/seedance/` files and surfaces `templates/ad-asset-prep.md` + `templates/character-design/`; added a consistency tie-break row (`higgsfield-soul` = lock identity in-platform vs `higgsfield-character-design` = develop the character first).

### Deferred to v3.19.0
- Guide rows/content for the new catalog models (gemini_omni, nano_banana_2_lite, openai_hazel, soul_cast, autosprite, ms_image), Seed Audio 1.0 prompting guidance, and the Seedance 4K masterclass material — content wave, planned at `workspace/output/V3.19-PLAN.md`.

## v3.18.0 — 2026-06-30

Video-to-video **footage transformation** for Seedance 2.0 — take a clip the user already shot, **preserve** the real subject + camera move, and **change one thing** (add a VFX element, swap the world, drop in a photoreal creature, relight to match, sync a timed zoom to a line). New **30th sub-skill** `higgsfield-seedance-vfx`. Sourced from a hand-authored practitioner skill + the Higgsfield "Seedance 2.0 in 4K" VFX tutorial (`higgsfield.ai/blog/vfx_4k`, `youtube.com/watch?v=Yte-UGhYkPQ`), which demonstrates this exact skill; model-checked against the live `seedance_2_0` spec — `media_roles` include `video` (v2v input is real), `4k` is a legal resolution, plus `audio`/`start_image`/`end_image`, duration 4–15s. One goal-driven release.

### New sub-skill — `higgsfield-seedance-vfx` (1.0.0)
A video-to-video layer on top of `higgsfield-seedance` (reuses its grammar + preflight linter; only the starting point changes — a real source clip whose subject and camera move must survive). Distinct from the parent's in-clip **Transformation prompt mode** (a morph generated from scratch). Sections:
- **Preserve, then change one thing** — lock identity/face/wardrobe/performance/framing/lens/camera, change only the named element, repeat the fragile guardrail at the end.
- **Run it in 4K** — Seedance 2.0 `mode=std` 4K (faces/lip-sync hold at 4K, warp at 1080p); harmonized with the repo's existing caps (fast → 720p; Cinema Studio → 1080p). The `4k` enum is model-verified; "detail holds at 4K" is flagged as a practitioner claim.
- **Prompt anatomy** — `@source` declaration, optional `@creature`/texture reference, specs line (NON-IP guardrail, match-source-runtime, `SFX` vs `SFX and source dialogue only`), continuous-shot action, behavioral SFX.
- **Three levels** — L1 swap the world · L2 change an element in-frame · L3 full handheld cinematic (difficulty scales with camera motion).
- **Two modes** (add an element · replace the environment) + the **lighting-integration recipe** (color matching alone reads as pasted-in: match key direction, bounce, optics/haze, edges/grounding).
- **Photoreal creature integration** — biological-accuracy vocabulary (wrinkled/cracked/asymmetric/matte, never smooth/glossy/inflated), telephoto-scale illusion, real contact shadow, reference-image-beats-description.
- **Timed camera moves synced to dialogue** — dual semantic + numeric anchoring, reveal pull-back with 100%-match landing, lip-sync preservation. **Prepended-intro budget** arithmetic (`total − intro = surviving window`).
- Two reference files — `references/dialogue-timing.md` (measure `T`, convert timecodes, phrase both anchors) and `references/first-frame.md` (generate the transformed start still, hand back as `start_image`).

### Wiring + template
- Routed from root `SKILL.md` (routing table + Sub-Skills table), `sub_skill_descriptions.py`, and `INDEX.md`. Roster **29 → 30**. Root version 3.17.0 → **3.18.0**.
- New `templates/seedance/footage-vfx-transform.md` — fill-in skeleton + four worked patterns (environment swap, head-on-fire, creature-with-reveal-pull-back, full handheld cinematic).

### Cross-links (patch bumps)
- `higgsfield-seedance` § Seedance 2.0 Prompt Modes / Transformation → distinguishes the in-clip morph from v2v footage transform; also added to Related Skills. (seedance 1.8.1→1.8.2)
- `higgsfield-audio` § Related skills → the timed-zoom-to-dialogue + source-dialogue-preservation cases. (audio 3.2.1→3.2.2)
- `higgsfield-camera` § Related skills → preserve a real handheld/driving move frame-for-frame + add a camera move you never filmed. (camera 3.3.0→3.3.1)
- `vocab.md` § Lighting Vocabulary / Scene-physics → the integration recipe for compositing a preserved subject or creature into a new plate.

## v3.17.0 — 2026-06-27

FACS (Facial Action Coding System) facial-expression control for Seedance 2.0 — directing a face by **muscle** (Action Unit codes like `AU12` lip-corner puller, `AU6` cheek raiser) instead of emotion labels. New **29th sub-skill** `higgsfield-facs`. Sourced from a practitioner brain-dump (AU-grid generation prompt + codes-in-prompt technique + worked examples); model-checked against the live `seedance_2_0` spec, which exposes **no FACS/expression field** — so the technique is flagged **[EMPIRICAL]** end to end (same provenance class as v3.16.0's Prompt-Craft Laws). One goal-driven release.

### New sub-skill — `higgsfield-facs` (1.0.0)
A consolidated facial-control layer on top of `higgsfield-seedance`. Sections:
- **What FACS is** + the provenance split (the AU vocabulary is standard science; Seedance's *interpretation* of codes is empirical, high-success-rate but **not a guarantee**) — and where it sits among the repo's three facial tools (named expression → behavior channel → Action Unit).
- **The plan-first workflow** — plan 3–4 expressions → generate a FACS sheet for *only those* → write the codes; explicitly counters the "generate the full 49-AU sheet then cherry-pick" anti-pattern.
- **Step 1 — generate the FACS reference sheet** — the parameterized image prompt (GPT Image 2 / Nano Banana Pro), the iterate-on-unreadable-captions note, and the **LLM-mislabels-AUs** caveat (the circulating sheet's `AU82` vs standard `AU38` nostril dilator; cross-check melindaozel.com/facs-cheat-sheet).
- **Step 2 — codes in the Seedance prompt** — codes-only vs codes+anatomical-description (test both), **3–4 expressions max** per generation, character photo optional (identity consistency only), beat-synced structure.
- **AU Code Reference** — the full grouped table (Forehead&Brow / Eye&Eyelid / Nose&Cheek / Lip&Mouth / Head Movement / Eye Direction / Special) with the non-standard-numbering caveat.
- **Emotion → AU recipes** — standard EMFACS prototypes (Duchenne AU6+AU12, sadness AU1+AU4+AU15, fear, anger, surprise, disgust, contempt) so the agent can answer "which code for anger?".
- **Dialogue & monologue facial acting** — the payoff: AU-per-beat schedule combined with the `[AUDIO: Xs]` lip-sync block; the performed-safety-over-visible-terror mixed-emotion pattern.
- Three worked examples (14-beat sweep, emotion arc, fear-masked-as-reassurance dialogue) + QUICK FACTS.

### Wiring + template
- Routed from root `SKILL.md` (routing table + Sub-Skills table), `sub_skill_descriptions.py`, and `INDEX.md`. Roster **28 → 29**. Root version 3.16.0 → **3.17.0**.
- New `templates/seedance/facs-expression-beats.md` — beat-synced AU schedule skeleton.

### Cross-links (patch bumps)
- `higgsfield-soul` § Micro-Expressions → FACS as the muscle-level layer beneath the 19 named expressions. (soul 3.6.0→3.6.1)
- `higgsfield-seedance` § Voice Rewrite §3 ("physics not emotion") → FACS as its muscle-level extreme. (seedance 1.8.0→1.8.1)
- `higgsfield-audio` § Lip-Sync Rules → FACS drives the expressive muscles around the phonemes. (audio 3.2.0→3.2.1)
- `vocab.md` § Emotion as Visible Behavior — Channels → AUs named as the anatomical sibling of the behavioral channels.

## v3.16.0 — 2026-06-27

Prompter updates from the Higgsfield "cinematic headphones ad" tutorial breakdown + a batch of Seedance 2.0 prompt/audio practitioner tips, model-checked against the live `seedance_2_0` spec. Four goals.

### Goal 1 — Audio as a conditioning input (model-verified)
The live spec confirms `seedance_2_0` accepts an `audio` reference media role and that `generate_audio` (native output) is *independent of audio reference medias* — i.e. uploaded audio conditions the generation, separate from generated sound. New `higgsfield-audio` § **Audio as a Conditioning Input** documents the two jobs of `@Audio1` (output track vs visual driver), **beat sync** (the 3-sentence audio→visual mapping + reference stacking + the temporal-compatibility constraint), the **`[AUDIO: Xs]` script block** (dialogue lip-sync + SFX from text alone, multilingual), and the **first-15s extraction trap** (pick a build→drop window, ≥256kbps). Cross-linked from `higgsfield-seedance` § Reference Roles. (audio 3.1.0→3.2.0, seedance 1.7.0→1.8.0)

### Goal 2 — Seedance prompt-craft laws (empirical)
New `higgsfield-seedance` § **Prompt-Craft Laws**: the left-to-right **attention model** (50–80-word sweet spot, front-load the load-bearing element, reconciled with the six-slot order and the >180-word filter ceiling), **"name the thing"** (replace "cinematic"/generic adjectives with a director/lighting/lens — the positive form of anti-slop), the **"fast" degradation keyword**, and **no negative prompts in the body** (scoped to Seedance, cross-linked to `shared/negative-constraints.md`). All flagged empirical, not model-documented. Anti-slop table in `higgsfield-prompt` extended with the named-referent substitute. (prompt 3.5.0→3.6.0)

### Goal 3 — Connected shotlist gap (P0)
New sub-skill **`higgsfield-shotlist-director`** — turns a brief/script into one editable HTML shotlist (global Style Prefix → `@`-glossary → named per-scene prompts in `Style → Characters → Scene → CUT 1..N`), with edit-once-propagates + per-scene-override semantics. Built to outclass the tutorial's downloadable skill by wiring in the preflight linter, reference-role lanes, Elements `@`-auto-attach, failure-mode awareness, and acceptance-rate logging. New `templates/seedance/global-style-prefix.md` (fill-in-the-blanks prefix + per-scene override example). Routed from root SKILL.md + `sub_skill_descriptions.py`.

### Goal 4 — Ad-asset prep + scene-craft patterns (P1–P3)
- New `templates/ad-asset-prep.md` — product sheet, grey-bg character sheet, **erase-duplicate-face**, **outfit 10-ideas→mix/recolor**, **multi-state variants**, prop sheets, and the **"design for win rate"** framing cross-linked to the acceptance-rate discipline.
- `higgsfield-soul` § Two-Tool Refinement Pipeline gains the **anti-"slop" layer-mask composite** worked example. (soul 3.5.0→3.6.0)
- `higgsfield-gpt-image-2/static-ads-workflow.md` gains **Mode C — Edit an existing still** (location editing, "keep everything else the same"). (gpt-image-2 1.1.0→1.2.0)
- `templates/10-dance-music-performance.md` gains **beat-by-beat choreography** + the **`@music_track`-drives-motion** pattern.
- `vocab.md` § Cut & Continuity gains **anchor-gesture cut ("cut on action")** + **multi-take micro-slice assembly**.
- `templates/seedance/top-down-map.md` gains **prop-scale-relative-to-a-landmark**.
- `CUT 1..N` labeling is demonstrated throughout the new shotlist-director skill.

## v3.15.2 — 2026-06-22

Privacy hygiene: **untracked `.planning/`** from the public repo. The nine `.planning/v3.7.x–v3.8.0/` build-execution notes were internal per-version planning artifacts that don't belong in a public skill library and were the source of the home-path PII scrubbed in v3.15.1. They are now git-ignored — kept on the maintainer's disk, removed from tracking.

- **Dangling provenance links cleaned up:** six shipped files (the two `higgsfield-gpt-image-2` docs, the two `higgsfield-marketing-studio` docs, `assets/fonts/README.md`, and a `docs/archive/` note) cited `.planning/` paths as verification trails — 18 path references. Those were rewritten to keep the provenance prose ("the v3.7.16 Phase 0 verification notes (internal build notes)") without the now-dead links, so `validate.py`'s relative-path check passes. CI caught these (a local run masked them — the untracked files still exist on disk locally but not in a fresh checkout).
- Their prior contents remain in git history; a history rewrite was intentionally not done, as the only exposure was a macOS username + folder names, never credentials. `validate.py --strict` clean, 110 tests pass, evals 40/40.

## v3.15.1 — 2026-06-22

Post-series hygiene: activation docs, a privacy scrub, and a clean Problems panel.

- **README § Maintenance** documents the two one-time activation steps the series left dormant: adding the `HIGGSFIELD_CREDENTIALS` secret to turn on the scheduled spec-drift check, and letting `log-route` routing data accumulate before pruning the long tail. Notes that credentials live only in the GitHub secret, never committed.
- **Privacy scrub:** removed absolute home-path PII (`/Users/<user>/...`, 5 occurrences) from `.planning/v3.7.16/PHASE-0-VERIFICATION.md` → `~`. Security pass otherwise clean: no tokens/credentials in the tree or git history, `specs/cli_baseline.json` is public model schema only, `workspace/` content is gitignored.
- **markdownlint hygiene:** extended `.markdownlint.json` to opt out of the remaining cosmetic rules firing on long historical docs (MD012/MD031/MD038/MD040/MD041), consistent with the existing MD013/MD022/MD032/MD060 opt-outs. No code/CI behavior change; `validate.py --strict` and the eval suite are unaffected.

## v3.15.0 — 2026-06-22

Finale of the framework-improvement series — the two remaining closers: Wave C's **scheduling wrapper** and **item 6's routing-telemetry surface**.

### Wave C scheduling — `.github/workflows/spec-drift.yml`
A weekly scheduled run of the now-trustworthy `refresh_specs.py` tripwire (Mondays, ~3 weeks ahead of the 30-day staleness WARN). Installs the CLI, restores credentials from a `HIGGSFIELD_CREDENTIALS` secret, and branches on the three exit states:
- **0 fresh** → success, nothing.
- **3 drift** → opens (or comments on) a GitHub issue with the report + the Tier-2 next steps.
- **1 pull-failed** → **fails the job loudly.** This is the auth-refresh story: the CLI access_token expires (its refresh_token extends but eventually lapses → "Session expired"), and rather than fragile auto-rotation, expiry surfaces as a red workflow + GitHub notification — re-run `higgsfield auth login` and update the secret. Setup + the auth story are documented in the workflow header. Detect-only; it never writes specs or merges.

### Item 6 — routing telemetry (`log-route` / `routing`)
The surface that makes "find the load-bearing skills, prune the long tail" answerable from **data instead of a guess**. HARD RULE #1 already makes the agent name its routes on every response's first line; this persists that declaration. New `db/routing-log.json` (append-only) + `log-route --skills a,b,c` (validated against the canonical 27-skill roster, so a typo can't fragment the counts) + `routing` (ranks sub-skills by opens, lists the never-opened tail). `validate.py` gains a `[ ROUTING ]` schema check (reusing `validate_route_entry`). Logged in `higgsfield-recall`.
- **Honest framing baked in:** this is *instrumentation, not a verdict* — the pruning DECISION waits until enough requests accumulate to trust the distribution; a small sample is not evidence a skill is dead. (And item 6 was never unblocked by item 3's `prompt_method` — it needed this separate routing surface, which now exists.)
- 8 new pytest cases (roster validation, aggregation, never-opened tail, seed-file validity). The 12 + 4 Wave C `refresh_specs` cases unchanged.

---

Older entries (v3.0.0 – v3.14.1) are archived verbatim in `docs/archive/CHANGELOG-v3.0-v3.14.md`.
