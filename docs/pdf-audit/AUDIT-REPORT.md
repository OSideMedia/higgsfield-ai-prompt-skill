# PDF Integration Audit — v3.4.0 candidate

Date: 2026-04-18
Source material: 7 official Higgsfield handbooks (reviewed externally, not stored in repo)

This report is an analytical summary of what the seven PDFs cover, compared to the current state of the higgsfield-ai-prompt-skill. All PDF content is described in paraphrase; no verbatim tables, prompts, or long quotes from the source material appear in this report. Three of the seven PDFs (Ai Promting Guide, Cinema Studio 3.0 HandBook, CS3 Doc) are slide-based or text-based presentations of the same Cinema Studio 3.0 material; overlap across those three is collapsed in the Cross-PDF overlaps section.

---

## Summary table

| PDF | Total items | DUPLICATE | REINFORCE | GAP | PHILOSOPHICAL |
|-----|-------------|-----------|-----------|-----|---------------|
| AI_prompting_handbook_image_video_models_en | 14 | 11 | 2 | 1 | 0 |
| Ai Promting Guide (CS slide deck variant) | 9 | 8 | 1 | 0 | 0 |
| Cinema Studio 3.0 HandBook (slide deck) | 8 | 7 | 0 | 0 | 1 |
| CS3 Doc (text Cinema Studio 3.0) | 12 | 9 | 1 | 1 | 1 |
| Seedance 2.0 Handbook | 18 | 14 | 1 | 2 | 1 |
| HiggsfieldTools Guide | 9 | 4 | 1 | 3 | 1 |
| Kling Motion Control | 10 | 7 | 0 | 3 | 0 |
| **TOTAL** | **80** | **60** | **6** | **10** | **4** |

---

## Per-PDF findings

### AI_prompting_handbook_image_video_models_en

A cross-ecosystem prompting handbook covering nine model families (OpenAI/Sora, Midjourney, Runway, Veo, FLUX, Firefly, Stability, Kling, Luma). It frames Higgsfield as a workflow layer rather than a model family and teaches universal prompt skeletons, reusable building blocks, image-to-video best practices, consistency rules, camera language, and common failures.

**Content items:**

1. **Scope framing — Higgsfield as platform/workflow, not a model family** — classification: PHILOSOPHICAL (handled in item 7 below; not counted here as a gap)
2. **Universal image prompt skeleton (subject/scene/composition/lighting/style/constraints)** — classification: DUPLICATE
   - Concept: seven-slot image prompt scaffold with a compact one-liner form.
   - Where it exists: `skills/higgsfield-image-shots/SKILL.md` + `prompt-examples.md` (shot size + angle + movement + subject + pose + environment + lighting + style formula).
   - Priority: N/A
3. **Universal video prompt skeleton (subject/action/camera/change-over-time/environment/look)** — classification: DUPLICATE
   - Concept: nine-slot video scaffold with a compact one-liner.
   - Where it exists: MCSLA five-layer formula in `skills/higgsfield-prompt/SKILL.md:14-26`; same five axes with different labels.
   - Priority: N/A
4. **Reusable prompt blocks (subject / composition / camera / lighting / motion / constraint)** — classification: DUPLICATE
   - Concept: modular blocks you can mix into any prompt.
   - Where it exists: equivalent block thinking in `higgsfield-prompt` (MCSLA), `higgsfield-camera`, `higgsfield-style`, and the Identity/Motion separation rule.
   - Priority: N/A
5. **Image-to-video rule: do not re-describe the static image, only describe motion** — classification: DUPLICATE
   - Concept: the prompt's job in I2V is the motion layer, not scene re-description.
   - Where it exists: `skills/higgsfield-prompt/SKILL.md:74-78` (explicit I2V rule), Cinema Studio 3.0 Soul Cast section in `higgsfield-soul`.
   - Priority: N/A
6. **Consistency rules + character bible template** — classification: REINFORCE
   - Concept: keep identical face/body/wardrobe descriptors across shots, and maintain a short "character bible" paragraph that gets pasted verbatim into every prompt in a sequence.
   - Where it exists: Identity/Motion separation rule in `higgsfield-prompt/SKILL.md:172-213` and `higgsfield-soul/SKILL.md:72-173` — but neither skill teaches the "one short paragraph, pasted unchanged every time" bible pattern outside Soul ID. There's no explicit template for users who are NOT using Soul ID and need manual identity locking (e.g., Popcorn-only workflows, non-Higgsfield models).
   - Target: small addition to `higgsfield-soul` or `higgsfield-pipeline` — a "manual character bible" pattern for when Soul ID is not in use.
   - REINFORCE justification: the current skill assumes Soul ID is the primary lock mechanism. The PDF's template is cleaner for manual-only workflows.
   - Priority: MEDIUM
7. **Higgsfield-as-workflow-layer framing** — classification: PHILOSOPHICAL
   - Concept: treat Higgsfield as a platform that orchestrates third-party model engines, rather than as a single generator. (See Philosophical shifts section.)
   - Priority: See Philosophical shifts.
8. **Camera language cheat sheet (locked-off, push-in, pull-back, pan, tilt, tracking, crane, orbit, POV, OTS)** — classification: DUPLICATE
   - Where it exists: `vocab.md`, `skills/higgsfield-camera/SKILL.md`, with richer naming (Higgsfield-specific presets like Action Run, FPV Drone, Snorricam, Robo Arm).
   - Priority: N/A
9. **Model-specific notes — OpenAI/Sora, Midjourney, Runway, Veo, FLUX, Firefly, Stability, Kling, Luma** — classification: DUPLICATE (partial)
   - Concept: per-model prompt preferences.
   - Where it exists: `skills/higgsfield-models/SKILL.md` + `MODELS-DEEP-REFERENCE.md` cover all Higgsfield-integrated engines in deeper detail. The PDF also covers OpenAI DALL-E, Midjourney, FLUX, Firefly, Stability, Luma — but these are NOT Higgsfield-integrated engines, so they are outside the skill's scope by design.
   - Priority: N/A (out of scope)
10. **Common failure patterns (three-prompts-glued-together, conflicting camera+composition, underspecified motion, static request with motion words, inconsistent identity, abstract-style-no-subject)** — classification: DUPLICATE
    - Where it exists: `skills/higgsfield-prompt/SKILL.md:217-230` (Common Prompt Mistakes table), `skills/higgsfield-troubleshoot/SKILL.md`.
    - Priority: N/A
11. **Quick templates (portrait / product / environment / subtle I2V / dynamic action / static shot)** — classification: DUPLICATE
    - Where it exists: `templates/` (10 annotated genre templates), `skills/higgsfield-recipes/SKILL.md`.
    - Priority: N/A
12. **Fast workflow recommendation — iterate one variable at a time** — classification: GAP
    - Concept: when iterating, change only one variable (subject, composition, motion, or style) per regeneration so you can identify what changed the result.
    - Where it exists: absent. Closest thing is the general "iterate" advice in `higgsfield-troubleshoot` and the Hero Frame workflow in `higgsfield-cinema`, but neither teaches the explicit one-variable-per-iteration loop as a named methodology. The HiggsfieldTools Guide PDF reinforces this same rule (see that section).
    - Target: small addition to `higgsfield-prompt` as a named pattern ("Iteration rule: one variable per regeneration") OR a new short section in `higgsfield-troubleshoot`.
    - Priority: MEDIUM
13. **Prompt weighting / negative prompts guidance (Stability-specific)** — classification: DUPLICATE
    - Where it exists: `skills/shared/negative-constraints.md` handles negative constraints for Higgsfield. Stability weighting syntax is out of scope for the Higgsfield skill.
    - Priority: N/A (out of scope)
14. **REINFORCE — camera language tied to emotional effect (push-in = tension/intimacy, pull-back = isolation, low-angle = power, handheld = urgency)** — classification: REINFORCE
    - Concept: a compact "camera term → typical effect" lookup tied to emotional intent.
    - Where it exists: `higgsfield-camera/SKILL.md` has "Best for" columns per movement, and the CS3 Business/Team section has genre-based camera presets. The emotional-intent angle exists but is scattered across multiple movement tables rather than consolidated as a standalone cheat sheet.
    - Target: minor reorganization — could add a single "camera-intent cheat sheet" table at the top of `higgsfield-camera` pulling the Best-for columns together.
    - Priority: LOW

---

### Ai Promting Guide (Cinema Studio 3.0 slide deck)

A visual slide-based version of the Cinema Studio 3.0 material. Covers the practical formula (subject + action + camera + lighting + vibe), core principles, image vs. video prompt structure, reusable blocks, character bible, camera language, and common failures. OCR quality was mixed on this deck; several slides rendered fragmented.

**Content items:**

1. **Prompt-as-blueprint, not essay** — classification: DUPLICATE
   - Where it exists: `higgsfield-prompt/SKILL.md` intent-over-precision section (lines 242-244), anti-slop vocabulary.
   - Priority: N/A
2. **Image vs video prompt contrast (spatial vs temporal logic)** — classification: DUPLICATE
   - Where it exists: `higgsfield-prompt` T2V vs I2V sections, `higgsfield-image-shots` for stills.
   - Priority: N/A
3. **Compact practical formula "Subject + Action + Camera + Lighting + Vibe"** — classification: DUPLICATE
   - Where it exists: MCSLA in `higgsfield-prompt`. "Vibe" maps to Look; the slide formula is a rephrasing.
   - Priority: N/A
4. **Failure patterns preview (prompt bleed, motion conflict, detail overload)** — classification: DUPLICATE
   - Where it exists: `higgsfield-prompt/SKILL.md` Common Prompt Mistakes, `higgsfield-troubleshoot`.
   - Priority: N/A
5. **Universal image skeleton (Subject + Environment + Lighting + Camera/Angle + Style/Render)** — classification: DUPLICATE
   - Where it exists: `higgsfield-image-shots/SKILL.md`.
   - Priority: N/A
6. **Universal video skeleton (OCR rendered fragmented; appears to mirror the handbook's scaffold)** — classification: DUPLICATE
   - Where it exists: MCSLA.
   - Priority: N/A
7. **Character bible example (one-sentence identity template)** — classification: REINFORCE (already covered in item 6 of the AI Prompting Handbook)
   - Priority: MEDIUM (consolidated with item 6 of handbook)
8. **Camera language cheat sheet (term → effect → best used for)** — classification: DUPLICATE
   - Where it exists: `higgsfield-camera/SKILL.md`.
   - Priority: N/A
9. **Model-specific notes — cross-model (OpenAI DALL-E, Midjourney, Runway, Veo, FLUX, Firefly, Stability, Kling, Luma)** — classification: DUPLICATE (partial, same out-of-scope caveat as handbook)
   - Priority: N/A

---

### Cinema Studio 3.0 HandBook (slide deck)

A second Cinema Studio 3.0 slide deck. Short, promotional-feeling deck emphasizing: scene-building tool mental model, character+environment asset creation, the practical formula, genre/pacing as behavior modifiers, camera techniques, common mistakes, three starter templates, and a "think like a filmmaker" closing.

**Content items:**

1. **Core six-step workflow (ideation → character → environment → scene prompt → audio → export)** — classification: DUPLICATE
   - Where it exists: `higgsfield-cinema/SKILL.md:75-91` (the 10-step Cinema Studio 2.5 workflow); 3.0 workflow steps overlap tightly.
   - Priority: N/A
2. **Asset creation — stable characters and environments via reference sheets** — classification: DUPLICATE
   - Where it exists: `higgsfield-soul/SKILL.md:194-224` (character sheet creation) + `higgsfield-cinema` Reference Anchor.
   - Priority: N/A
3. **Practical formula "Subject + Action + Camera + Lighting + Vibe"** — classification: DUPLICATE (same as Ai Promting Guide item 3)
   - Priority: N/A
4. **Genre & pacing — rhythm follows genre** — classification: DUPLICATE
   - Where it exists: `higgsfield-cinema/SKILL.md` Speed Ramp tables + Genre tables per-version.
   - Priority: N/A
5. **Camera techniques — close-up = emotion, establishing = context, tracking = movement** — classification: DUPLICATE
   - Where it exists: `higgsfield-camera/SKILL.md` shot size table, genre-based camera presets section.
   - Priority: N/A
6. **Common mistakes (conflicting keywords, ignored lighting, missing seeds, inconsistent ratios)** — classification: DUPLICATE
   - Where it exists: `higgsfield-troubleshoot/SKILL.md` + `higgsfield-prompt/SKILL.md`.
   - Priority: N/A
7. **Three starter templates (hero intro, dialogue scene, action sequence)** — classification: DUPLICATE
   - Where it exists: `templates/` provides 10 genre-specific templates including character intro, action chase, and several dialogue-capable recipes.
   - Priority: N/A
8. **"Think like a filmmaker" — tools don't make the movie, directors do** — classification: PHILOSOPHICAL
   - Concept: director's mindset over prompt-writer mindset. See Philosophical shifts.

---

### CS3 Doc (Cinema Studio 3.0 text-heavy version)

The fullest text version of the Cinema Studio 3.0 material. Ten numbered sections covering: CS3.0 as a scene-building tool, six-step workflow, building characters properly, building locations, prompt-writing mindset, story-first prompting, genre/pacing, camera thinking, common mistakes, simple starter templates.

**Content items:**

1. **CS3.0 as scene-building tool, not clip generator** — classification: PHILOSOPHICAL
   - See Philosophical shifts.
2. **Six-step core workflow (character → location → upload references → describe scene → choose genre/pace/camera → generate and iterate)** — classification: DUPLICATE
   - Where it exists: `higgsfield-cinema/SKILL.md:75-91`.
   - Priority: N/A
3. **Character-first principle: build character asset BEFORE scene** — classification: DUPLICATE
   - Where it exists: `higgsfield-soul/SKILL.md` (Soul ID/Soul Cast flows), `higgsfield-cinema` Reference Anchor + Elements system.
   - Priority: N/A
4. **Character reference sheet structure (front/left profile/right profile/back/close-up portraits)** — classification: REINFORCE
   - Concept: a specific five-view character sheet layout — the PDF names the exact angles.
   - Where it exists: `higgsfield-soul/SKILL.md:208-214` mentions front / 3-4 / side profile / back (4 views). The PDF's list is subtly different (adds close-up portraits as a named variant, drops 3/4).
   - Target: minor edit to `higgsfield-soul` character sheet angle list — either align the angle set to the PDF's five-view pattern or note both variants.
   - Priority: LOW
5. **Location sheet structure (straight-on wide / left-angle / right-angle / reverse / close-up environmental details)** — classification: GAP
   - Concept: a parallel location reference-sheet pattern with five prescribed angles — separate from character reference sheets.
   - Where it exists: absent. `higgsfield-cinema` mentions `@Locations` and Reference Anchors for characters, but there is NO structured "location sheet" pattern. The skill currently conflates location handling with character handling or pushes it into generic Element description.
   - Target: new subsection in `higgsfield-cinema` (Elements section) OR new subsection in `higgsfield-soul` — "Location reference sheets" with five-view angle spec.
   - Priority: HIGH — this is a concrete missing asset class.
6. **Location-as-asset principle (treat environments like characters: establish once, reuse, keep architecture/light/color treatment stable)** — classification: DUPLICATE (principle) / GAP (named workflow)
   - Where it exists as principle: `higgsfield-cinema` Elements system, `higgsfield-pipeline` Popcorn stage.
   - Where it's a gap: the explicit "build the location as an asset first, before scene generation" workflow is only implicit. The PDF frames this as a named methodology parallel to character-first.
   - Priority: covered by item 5 above.
7. **Weak prompt vs strong prompt diagnostic (keyword soup vs scene direction)** — classification: DUPLICATE
   - Where it exists: `higgsfield-prompt` anti-slop vocabulary, `higgsfield-seedance` filmmaker-not-friend pass, prompt-examples before/after section.
   - Priority: N/A
8. **Seven-slot prompt formula ([shot type] + [subject] + [action] + [environment] + [lighting] + [camera behavior] + [tone])** — classification: DUPLICATE
   - Where it exists: MCSLA (five-layer), Seedance six-slot formula.
   - Priority: N/A
9. **Story-first prompting — prompt answers "what's happening, what's the character feeling, what changes, what should the audience feel"** — classification: DUPLICATE
   - Where it exists: `higgsfield-prompt` Intent-over-Precision, `higgsfield-seedance` physics-not-emotion (the CS3 approach lands between these two — emotion as dramatic intent without the physics-only rewrite).
   - Priority: N/A
10. **Genre as performance tool (noir doesn't move like action; horror doesn't pace like comedy)** — classification: DUPLICATE
    - Where it exists: `higgsfield-cinema` Genre table, `higgsfield-camera` genre-based camera presets.
    - Priority: N/A
11. **Camera supports emotion (close-up = intimacy/fear/realization, wide = isolation/scale, handheld = instability/urgency, push-in = tension, static = restraint/dread)** — classification: REINFORCE
    - See item 14 in AI_prompting_handbook — already flagged as a low-priority consolidation opportunity.
    - Priority: LOW
12. **Five common mistakes (scenes before locked characters, disposable locations, keyword soup, over-controlling, ignoring emotional intention)** — classification: DUPLICATE
    - Where it exists: `higgsfield-prompt` + `higgsfield-troubleshoot`.
    - Priority: N/A

---

### Seedance 2.0 Handbook

Seedance's own handbook. Covers the mental model, beginner mistakes, seven core operating principles, the prompt modes, single-shot and multi-shot structures, reference-role rules, continuation formula, reference-sheet types (environment / outfit / motion-camera / palette-mood), beat-based timing, nine-slot prompt structure, anti-patterns, troubleshooting-by-symptom, and reference vocabulary for camera/lighting/sound/constraints.

**Content items:**

1. **Mental model — "controlled directing system, not poetic toy"** — classification: PHILOSOPHICAL
   - See Philosophical shifts (compatible with current framing).
2. **Six biggest beginner mistakes (prompt overload, role-less references, too many actions, too many camera ideas, too many style words, no hierarchy)** — classification: DUPLICATE
   - Where it exists: `higgsfield-seedance/SKILL.md` filter playbook, `higgsfield-prompt` one-action-per-scene rule, anti-patterns list in existing Seedance skill.
   - Priority: N/A
3. **Principle 1 — one shot = one dominant readable action** — classification: DUPLICATE
   - Where it exists: `higgsfield-prompt/SKILL.md:155-168` (One Action Per Scene rule).
   - Priority: N/A
4. **Principle 2 — camera is not decoration, it serves story** — classification: DUPLICATE
   - Where it exists: `higgsfield-camera` genre-based camera presets + `higgsfield-seedance` voice-rewrite pass ("name the camera move").
   - Priority: N/A
5. **Principle 3 — action must be physical (visible behavior, not dialogue/exposition)** — classification: DUPLICATE
   - Where it exists: `higgsfield-seedance/SKILL.md` voice rewrite + engine constraints ("describe physics, not emotion").
   - Priority: N/A
6. **Principle 4 — environment is active, not wallpaper** — classification: REINFORCE
   - Concept: the environment should participate in the scene (weather responds, ambient motion carries mood), not just sit as a static backdrop.
   - Where it exists: `templates/` use environmental motion as secondary action; `higgsfield-prompt` lists environmental motion in the Motion Block. But there's no named principle "environment = active participant" framed as a Seedance operating rule.
   - Target: small addition to `higgsfield-seedance` as a named operating principle.
   - Priority: LOW
7. **Principle 5 — references need assigned roles (identity / motion / audio / palette)** — classification: DUPLICATE
   - Where it exists: `higgsfield-seedance/SKILL.md` rule of 12, `higgsfield-cinema/SKILL.md` @ Reference Patterns section (character identity, environment, motion reference, audio reference, multi-image spatial mapping).
   - Priority: N/A
8. **Principle 6 — continuity is not just linking (flow vs sequence)** — classification: DUPLICATE
   - Where it exists: `higgsfield-pipeline` master chain, Cinema Studio multi-shot workflow.
   - Priority: N/A
9. **Principle 7 — structure beats length** — classification: DUPLICATE
   - Where it exists: `higgsfield-prompt` keep-under-200-words rule, Seedance short-prompt preference.
   - Priority: N/A
10. **Six prompt modes — Single-Shot, Multi-Shot, Reference-Based, Continuation, Expand Shot (canvas extension), Edit Shot** — classification: GAP
    - Concept: Seedance supports six named generation modes. The handbook names them as first-class mode labels with specific use cases: Reference-Based uses a source image to guide generation; Continuation extends a prior output; Edit Shot modifies specific elements in an existing image; Expand Shot extends the canvas/scene.
    - Where it exists: `higgsfield-seedance/SKILL.md` covers single-shot / multi-shot style implicitly, but does NOT name or distinguish Reference-Based, Continuation, Expand Shot, or Edit Shot as distinct modes with distinct prompt patterns. `higgsfield-cinema` covers @ Reference Patterns but conflates them with Cinema Studio-specific behavior rather than Seedance modes.
    - Target: new subsection in `higgsfield-seedance` — "Seedance 2.0 prompt modes" with one paragraph per mode and a minimal example pattern.
    - Priority: HIGH — this is directly applicable to Seedance users and not currently documented.
11. **Reference roles: image = identity/wardrobe/palette/composition; video = motion rhythm/camera behavior/blocking; audio = timing/speech/ambience** — classification: DUPLICATE
    - Where it exists: `higgsfield-cinema/SKILL.md` @ Reference Patterns section distinguishes these uses by input type.
    - Priority: N/A
12. **Continuation formula: last-frame anchor + identity anchor + previous clip as secondary memory; start immediately after final frame; never repeat previous action; preserve character/outfit/environment/emotional carryover** — classification: GAP
    - Concept: a specific five-rule formula for writing continuation prompts so the model doesn't repeat actions, loses state, or drifts identity.
    - Where it exists: absent as a named pattern. `higgsfield-pipeline` discusses chaining shots but not the continuation-specific rules. `higgsfield-cinema` has frame extraction loop (2.5) but doesn't document continuation prompt rules. Veo 3.1 video extension is covered in `higgsfield-models/MODELS-DEEP-REFERENCE.md:710-711` at the model level only, not at the prompt-construction level.
    - Target: new subsection in `higgsfield-seedance` OR `higgsfield-pipeline` — "Continuation prompt formula" with the five rules.
    - Priority: HIGH — continuation is a recurring failure mode and this is a clean, portable ruleset.
13. **Reference-sheet types (environment / outfit-material / motion-camera / palette-mood)** — classification: REINFORCE
    - Concept: four parallel reference-sheet categories, each reducing one specific kind of ambiguity. The motion-camera sheet and palette-mood sheet are under-documented in the current skill.
    - Where it exists: `higgsfield-soul` covers character sheets; `higgsfield-moodboard` covers palette/mood via Soul Hex and curated moodboards. But motion-camera sheets (a short reference clip of the camera behavior you want repeated) and outfit-material sheets (dedicated wardrobe reference) are not documented as dedicated artifacts.
    - Target: small addition to `higgsfield-soul` or `higgsfield-cinema` — name the four reference-sheet types and which artifact they correspond to in Higgsfield's UI.
    - Priority: MEDIUM
14. **Beats-and-timing framework (beat = meaningful unit of progression; use seconds when timing matters, shot numbers when storyboard logic matters; three-beat structure establish/develop/payoff)** — classification: DUPLICATE
    - Where it exists: `higgsfield-prompt` three-act rhythm for action (charge-up / burst / aftermath), Cinema Studio Multi-Shot Manual scene structure, timestamped prompt format.
    - Priority: N/A
15. **Nine-slot prompt structure (format-goal / asset-roles / scene / action / camera / lighting-color / sound / timeline-shot-structure / constraints / continuity)** — classification: DUPLICATE
    - Where it exists: MCSLA + the `higgsfield-seedance` six-slot formula + Cinema Studio UI settings. Nine slots is a more granular repackaging of material already covered.
    - Priority: N/A
16. **Seedance anti-patterns (adjective soup, too many camera moves, unassigned reference stacks, controlling everything equally, continuation without start lock, contradictory identity, literary emotion vs visible behavior, changing too many variables at once)** — classification: DUPLICATE
    - Where it exists: `higgsfield-seedance` voice rewrite + existing anti-patterns section; `higgsfield-prompt` common mistakes.
    - Priority: N/A
17. **Troubleshooting-by-symptom matrix (chaotic result / style ignored / character drift / camera resets / previous beat replays / motion feels fake / clip feels unstable)** — classification: DUPLICATE
    - Where it exists: `higgsfield-troubleshoot/SKILL.md` symptom-based organization.
    - Priority: N/A
18. **Vocabulary tables (camera / lighting / sound / constraint language)** — classification: DUPLICATE
    - Where it exists: `vocab.md`, `higgsfield-camera`, `higgsfield-audio`, `skills/shared/negative-constraints.md`.
    - Priority: N/A

---

### HiggsfieldTools Guide

A concise guide to the Higgsfield platform's workspaces — Cinema Studio, Lipsync Studio, Draw-to-Video/Sketch-to-Video, Sora 2 Trends, Click to Ad, Higgsfield Audio — with an emphasis on "choose the workspace by task, not the model." Six-step project workflow. A decision matrix mapping production problems to workspaces. OCR had occasional slide-layout confusion but the core structure was readable.

**Content items:**

1. **Platform is organized around tools/workspaces, not a single generator** — classification: PHILOSOPHICAL
   - See Philosophical shifts. Not currently a primary framing in the skill.
2. **Workspace-first decision framework — "What are you trying to make?" precedes "Which model?"** — classification: GAP
   - Concept: the user should start by identifying the production problem (cinematic scene / speaking character / rough idea / trend-led short / product ad / narration), pick the matching workspace, THEN select the model inside it.
   - Where it exists: partially in `higgsfield-models/SKILL.md` decision flowchart (model-first) and in `higgsfield-apps/SKILL.md` (by-use-case tables). But the root `SKILL.md` routes by SUB-SKILL based on what the user mentions — there's no workspace-first decision layer. The Fast Path table in root `SKILL.md:74-79` jumps straight to default models.
   - Target: either a new subsection at the top of root `SKILL.md` ("Workspace-first decision — choose the workspace by task, then the model by result") OR a new sub-skill `higgsfield-workspaces` acting as the entry-point router.
   - Priority: HIGH — this is a meaningful philosophical layer plus a concrete routing matrix, and the skill currently has no equivalent.
3. **Cinema Studio workspace description (cinematic scenes with deliberate camera direction)** — classification: DUPLICATE
   - Where it exists: `higgsfield-cinema/SKILL.md`.
   - Priority: N/A
4. **Lipsync Studio workspace (speaking characters, dubbing, avatars)** — classification: DUPLICATE (but sparsely)
   - Where it exists: `higgsfield-audio/SKILL.md` mentions Lipsync Studio; `higgsfield-apps/SKILL.md:90` lists it as an app. The skill does NOT have a dedicated Lipsync Studio workspace write-up.
   - Priority: covered by item 2 above (workspace-first framework would surface this)
5. **Draw to Video / Sketch to Video workspace (early ideation, storyboard blocking)** — classification: GAP
   - Concept: dedicated workspace for turning a rough sketch or blocking drawing into a generated video — fundamentally different workflow from text-to-video.
   - Where it exists: `higgsfield-apps/SKILL.md:81` has a one-liner ("Sketch-to-Real — turn sketch into realistic image/video"). CHANGELOG notes mention Draw-to-Video was on the backlog but not implemented. There is no documented sketch-to-video prompt pattern, example, or decision point.
   - Target: either a new sub-skill `higgsfield-sketch` OR a dedicated section in `higgsfield-apps` with prompt patterns.
   - Priority: MEDIUM — not huge, but this is a concrete missing workflow.
6. **Sora 2 Trends workspace (fast trend-led short-form content)** — classification: GAP
   - Concept: dedicated workspace for trend/viral short-form. Different from Sora 2 the model — a templated workflow on top.
   - Where it exists: absent. `higgsfield-models` covers Sora 2 as a model but doesn't describe a Trends workspace or workflow.
   - Target: dedicated section in `higgsfield-apps` OR in a new `higgsfield-workspaces` sub-skill.
   - Priority: MEDIUM
7. **Click to Ad workspace (product-focused ad generation from URL or image)** — classification: DUPLICATE
   - Where it exists: `higgsfield-apps/SKILL.md:36-47` covers Click to Ad and the product-ad family.
   - Priority: N/A
8. **Higgsfield Audio workspace (voiceovers, voice swaps, translation)** — classification: REINFORCE
   - Concept: a workspace dedicated to generative voice — distinct from Lipsync Studio.
   - Where it exists: `higgsfield-audio/SKILL.md` is primarily about audio IN video generations. A dedicated Higgsfield Audio workspace for voiceover/voice swap/translation is not separately documented.
   - Target: new subsection in `higgsfield-audio` — "Higgsfield Audio workspace (standalone voice tools)".
   - Priority: MEDIUM
9. **Six-step project logic (open workspace → choose feature → select model → prepare input → add prompt/controls → generate and iterate)** — classification: DUPLICATE (partial)
   - Where it exists: `higgsfield-cinema` 10-step workflow covers much of this; `higgsfield-pipeline` covers cross-workspace chaining. The PDF's six-step version is a simpler, more generic rendering for any workspace. No flat cross-workspace "open → feature → model → input → prompt → iterate" six-step recipe is written down.
   - Priority: covered by item 2 above.

---

### Kling Motion Control

A focused handbook on Kling 3.0 Motion Control and the Higgsfield workflow for using it. Covers when to choose Motion Control, what it does (character image + motion reference video = motion transfer), the one-screen Higgsfield workflow (8 clickable steps), input-quality best practices, face/orientation modes (Image Orientation vs Video Orientation + Element Binding), scene-source selection, prompt role (shape the world, not the base motion), and recommended reference-clip duration (3-30s).

**Content items:**

1. **When to choose Motion Control — directed repeatable motion, dance/sports/acting beats, motion-across-characters transfer, scene prototyping, ad/social/creator repeatability** — classification: REINFORCE
   - Concept: a specific decision shortlist for when Motion Control beats standard generation.
   - Where it exists: `skills/higgsfield-models/MODELS-DEEP-REFERENCE.md:102-127` covers Motion Control at the model level with "best for" list (reference-video motion transfer, full-body choreography, complex dance/action, talking head with precise gestures). The model reference has most of the content; the PDF adds "ad/social repeatability" as a use case which is absent.
   - Priority: LOW
2. **Motion Control core definition: character image + motion reference video = gesture/body-motion/facial-performance/timing transfer** — classification: DUPLICATE
   - Where it exists: `skills/higgsfield-models/MODELS-DEEP-REFERENCE.md:102-126` covers this in detail.
   - Priority: N/A
3. **Image Orientation vs Video Orientation mode (camera movements + static body vs complex full-body motion)** — classification: DUPLICATE
   - Where it exists: `MODELS-DEEP-REFERENCE.md:108-110`.
   - Priority: N/A
4. **Element Binding — connects facial identity to motion data for face stability during movement** — classification: DUPLICATE
   - Where it exists: `MODELS-DEEP-REFERENCE.md:112`.
   - Priority: N/A
5. **Motion reference input best practices (one clear subject, head+body visible, real human motion, avoid cuts/fast transitions, avoid very fast actions, 3-30s range)** — classification: GAP
   - Concept: a structured "input quality checklist" for the motion reference clip itself — what makes a clip a good motion source.
   - Where it exists: `MODELS-DEEP-REFERENCE.md` mentions 3-30s duration and motion transfer capability, but does NOT give a structured "what makes a good motion reference clip" checklist (clean subject, readable face/body, avoid cuts, avoid fast actions). The whole "input quality determines output quality" pre-flight check is absent.
   - Target: new subsection in `higgsfield-motion` or as an addition to the Kling 3.0 Motion Control section in `MODELS-DEEP-REFERENCE.md` — "Motion reference input checklist".
   - Priority: HIGH — this is a concrete, teachable pre-flight check that prevents wasted credits.
6. **Face binding + orientation preflight (close-up face input required, what to do if output suddenly cuts/snaps to different source clip = motion source too fast)** — classification: GAP
   - Concept: a specific diagnostic pattern for common Motion Control failures — if the output jumps between motions, your motion source has cuts or is too fast.
   - Where it exists: absent from the skill entirely.
   - Target: new troubleshooting entry in `higgsfield-troubleshoot/SKILL.md` AND in the motion-control section of `MODELS-DEEP-REFERENCE.md`.
   - Priority: MEDIUM
7. **Kling Motion Control one-screen workflow (8 steps: Video tab → Kling Motion Control 3.0 → upload motion reference → upload character image with readable face+body → pick resolution → set Scene source → describe environment/lighting in Advanced Settings → Generate)** — classification: GAP
   - Concept: a named, step-by-step workflow for running Motion Control specifically on Higgsfield (not generic Kling). The PDF walks through the actual Higgsfield UI flow.
   - Where it exists: `MODELS-DEEP-REFERENCE.md` describes what Motion Control does but does NOT walk through the Higgsfield UI workflow for invoking it. No step-by-step exists.
   - Target: new subsection in `higgsfield-motion` OR in the Kling Motion Control section of `MODELS-DEEP-REFERENCE.md` — "Running Kling Motion Control 3.0 in Higgsfield".
   - Priority: HIGH — this is a concrete missing workflow walkthrough.
8. **Scene source options (pull environment from the motion video vs from the character image)** — classification: GAP (subset of item 7)
   - Priority: covered by item 7.
9. **Prompt role in Motion Control — prompt shapes the world around the motion, not the base motion itself** — classification: DUPLICATE
   - Where it exists: `MODELS-DEEP-REFERENCE.md:118` ("Describe camera direction + scene context; don't describe the motion itself").
   - Priority: N/A
10. **Pre-flight checklist (clean reference with no cuts / readable face+body / correct scene source / correct orientation mode / prompt describes world not motion)** — classification: GAP (overlaps items 5, 7)
    - Priority: covered by items 5 and 7.

---

## New sub-skill candidates

### 1. `higgsfield-workspaces` (PROPOSED)

**What it would cover:** The workspace-first decision layer. Before a user picks a model, they identify which Higgsfield workspace fits their production problem: Cinema Studio (deliberate cinematic direction), Lipsync Studio (speaking characters), Draw-to-Video / Sketch-to-Video (ideation from rough sketches), Sora 2 Trends (trend-led shorts), Click to Ad (product ads), Higgsfield Audio (standalone voice work). Each workspace gets a short "when to use this" paragraph, the model(s) available inside, and the entry-point to the existing sub-skill that covers its prompt patterns.

**Which PDF items feed into it:**
- HiggsfieldTools Guide items 1, 2, 4, 5, 6, 8, 9 (workspace-first framework, workspace descriptions, Lipsync / Draw-to-Video / Sora Trends / Higgsfield Audio workspace entries, six-step project logic)
- Philosophical framing from item 1 (platform as workspaces, not a generator)

**Why it can't live in an existing sub-skill:** The root `SKILL.md` is already a dispatcher routed by sub-skill name. `higgsfield-apps` is a flat list of one-click workflows, not a decision layer. `higgsfield-models` is model-first, not task-first. The workspace-first decision layer is an orthogonal axis to both. It would be the user's first stop after the root dispatcher, then the existing sub-skills handle the prompt-level work.

**Alternative:** Could live as a new top section in the root `SKILL.md` rather than a sub-skill — but the root is already dense. A dedicated sub-skill is cleaner.

### 2. `higgsfield-motion-control` OR expansion of `higgsfield-motion` (EXPANSION PREFERRED)

**What it would cover:** Running Kling 3.0 Motion Control in Higgsfield specifically. Motion-reference input quality checklist (what makes a clip a good motion source). Face binding + orientation preflight. Step-by-step Higgsfield UI workflow. Scene source selection. Common failure diagnostics (output jumps = source too fast, etc.).

**Which PDF items feed into it:** Kling Motion Control items 1, 5, 6, 7, 8, 10.

**Why it might not need a new sub-skill:** `higgsfield-motion` currently covers named motion PRESETS (VFX library), not motion CONTROL (reference-video motion transfer). The two share the word "motion" but are different systems. Options:
- Add a new top section "Kling Motion Control 3.0 workflow" inside `higgsfield-motion` — cleanest, no new file.
- Create `higgsfield-motion-control` as its own sub-skill — cleaner separation but adds routing complexity.

**Recommendation:** expand `higgsfield-motion` first; promote to standalone only if content grows beyond a single section.

---

## Philosophical shifts

### A. Higgsfield as workflow-layer, not a model family

**The shift:** The external AI Prompting Handbook treats Higgsfield as a platform/workflow layer that sits on top of third-party model engines (Kling, Sora, Veo, Wan, etc.). The user's primary question is "which workspace fits my production problem" rather than "which model should I use."

**How it would change the skill:** The root `SKILL.md` currently opens with a mandatory workflow (route to sub-skill → apply MCSLA → use named vocabulary → append negative constraints). It treats Higgsfield as a coherent prompting platform with MCSLA as the core formula. Adding the workspace-first layer would slot IN FRONT of MCSLA: the user first picks a workspace (Cinema Studio / Lipsync / Sketch-to-Video / Sora Trends / Click to Ad / Higgsfield Audio), and only then applies MCSLA for the prompt inside that workspace.

**Compatible with MCSLA?** Yes. MCSLA is the prompt-construction formula; workspace-first is a routing layer one level above it. They compose cleanly. The risk is redundancy: the current root `SKILL.md` already has a "Route to the Right Skill" table routed by user intent, and parts of that are already workspace-ish. Adding a formal workspace layer means reconciling the two routing tables.

### B. Director-first / story-first mindset (Cinema Studio 3.0 and Seedance handbook)

**The shift:** CS3 Doc and the Seedance handbook both emphasize thinking like a director — who is the scene about, what changes, what should the audience feel — rather than like a prompt-writer assembling keywords. Seedance frames it as "controlled directing system, not poetic toy."

**How it would change the skill:** The current `higgsfield-prompt/SKILL.md` has "Intent over Precision" and "Story-first" is implicit in the Three-Act Rhythm for Action. `higgsfield-seedance` has the "filmmaker not friend" voice rewrite. The PDF framing is a slightly different cut: it puts "dramatic purpose of the shot" as question #1 before any prompt construction.

**Compatible with current approach?** Fully compatible. This is not a competing framework — it's the same mindset phrased as an upfront question. Minor edit opportunity to lead `higgsfield-prompt` with "before writing, answer: who is the scene about, what changes, what should the audience feel."

**Priority:** LOW — stylistic reinforcement, not a real gap.

### C. Character and location as ASSETS to be built first (CS3 Doc, Seedance handbook)

**The shift:** Treat characters AND locations as reusable assets with dedicated reference sheets, generated BEFORE any scene work. The skill covers this for characters (Soul ID, character sheets) but treats locations as a subset of the Elements system in Cinema Studio. The PDFs frame locations as equal to characters: you should have a location sheet with five prescribed views and lock its architecture/light/color treatment before generating scenes.

**How it would change the skill:** Small reframing in `higgsfield-soul` and `higgsfield-cinema` — add a "Location Reference Sheet" pattern with five-view structure. Possibly promote locations from "one of three Element types" to "first-class asset with its own workflow."

**Compatible with current approach?** Fully compatible. Additive.

**Priority:** MEDIUM (and also captured as a GAP — CS3 Doc item 5).

### D. Seedance mental model — "controlled directing system"

**The shift:** The Seedance handbook frames Seedance as a system you direct, not a tool you describe to. The current `higgsfield-seedance` has this in spirit via the voice-rewrite and engine-constraints sections, but doesn't name the mental model upfront.

**Compatible?** Fully compatible — it's the current skill's implicit framing, made explicit.

**Priority:** LOW — one-line addition to `higgsfield-seedance` opener.

---

## Cross-PDF overlaps

Content that appears in multiple PDFs (integrate once, not repeatedly):

1. **Universal image prompt skeleton** — AI_prompting_handbook + Ai Promting Guide. Duplicate in both; integrate once (already duplicate in skill).
2. **Universal video prompt skeleton / practical formula** — AI_prompting_handbook + Ai Promting Guide + Cinema Studio 3.0 HandBook + CS3 Doc. Four overlapping formulations. All map to MCSLA.
3. **Character bible / character reference sheet** — AI_prompting_handbook + CS3 Doc + Cinema Studio 3.0 HandBook + Seedance handbook. Four sources, one concept. Target: single REINFORCE edit in `higgsfield-soul`.
4. **Camera language cheat sheet (term → effect)** — AI_prompting_handbook + Ai Promting Guide + CS3 Doc + Seedance handbook. All four reference the same ~10-term list. Single source of truth: `higgsfield-camera`.
5. **"Do not re-describe the image in I2V — describe motion only"** — AI_prompting_handbook + Seedance handbook. Already in `higgsfield-prompt`.
6. **Six-step workflow (ideation → character → location → scene → generate → iterate)** — Cinema Studio 3.0 HandBook + CS3 Doc + HiggsfieldTools Guide. Three sources, same workflow.
7. **Common failure patterns (keyword soup, conflicting movements, underspecified motion, inconsistent identity, prompt bleed)** — AI_prompting_handbook + Ai Promting Guide + Cinema Studio 3.0 HandBook + CS3 Doc + Seedance handbook. Heavily duplicated across all PDFs. Target: keep `higgsfield-troubleshoot` + `higgsfield-prompt` common-mistakes tables as-is — they already subsume these.
8. **Genre/pacing as behavior modifier, not decoration** — Cinema Studio 3.0 HandBook + CS3 Doc + Seedance handbook.
9. **One action per shot** — Seedance handbook + `higgsfield-prompt` already has this rule. Heavily duplicated upstream.
10. **"Think like a filmmaker / director"** — Cinema Studio 3.0 HandBook + CS3 Doc + Seedance handbook. Philosophical shift item B.
11. **Iterate one variable at a time** — AI_prompting_handbook + HiggsfieldTools Guide. Two sources, and currently absent from the skill (GAP item).
12. **Workspace/tool-first mindset** — HiggsfieldTools Guide + AI_prompting_handbook (latter in the form of "Higgsfield is a platform, not a model"). Philosophical shift item A.

---

## Overall recommendation

**How much new content actually exists:** Rough estimate — 60 of 80 items (75%) are DUPLICATE, 6 (7.5%) are REINFORCE, 10 (12.5%) are GAP, and 4 (5%) are PHILOSOPHICAL. The skill already covers the dominant majority of this material, often in more depth than the PDFs. The PDFs are a useful external calibration check — they confirm the skill is complete on MCSLA, camera language, character consistency, I2V rules, and common failures. Where they add value is in a small number of concrete workflow gaps (location sheets, continuation formula, motion-control workflow, workspace-first decision, sketch-to-video, Sora Trends) and one philosophical layer (workspace-first routing).

**The five additions that would deliver the most value:**

1. **Location reference-sheet workflow** (CS3 Doc item 5) — target `higgsfield-cinema` or `higgsfield-soul`. Concrete, actionable, fills a real asymmetry in how the skill treats characters vs locations. HIGH.
2. **Seedance prompt modes — Reference-Based, Continuation, Expand Shot, Edit Shot** (Seedance handbook item 10) — target `higgsfield-seedance`. Core Seedance capability currently absent. HIGH.
3. **Seedance continuation formula** (Seedance handbook item 12) — target `higgsfield-seedance` or `higgsfield-pipeline`. Named five-rule pattern for continuation prompts; prevents recurring failures. HIGH.
4. **Kling Motion Control workflow + reference-input checklist** (Kling PDF items 5, 7) — target `higgsfield-motion` (expanded) + `MODELS-DEEP-REFERENCE.md`. Concrete pre-flight checks for a credit-expensive feature. HIGH.
5. **Workspace-first decision layer** (HiggsfieldTools Guide item 2 + philosophical shift A) — target either new top section in root `SKILL.md` or new `higgsfield-workspaces` sub-skill. Routing layer above MCSLA; surfaces Draw-to-Video / Sora Trends / Lipsync / Higgsfield Audio workspaces that currently get thin coverage. HIGH.

**v3.4.0 scope decision:** All five HIGH-priority gaps are small, additive, and independent. None require rewriting existing sub-skills. They can ship together as a single v3.4.0 release titled something like "v3.4.0 — PDF-sourced gap fills: location sheets, Seedance modes + continuation, Motion Control workflow, workspace-first routing." MEDIUM-priority items (Sora 2 Trends section, Sketch-to-Video section, Higgsfield Audio workspace, environment-as-active principle, motion-camera/outfit/palette reference sheets, active-environment principle, character-bible template for non-Soul-ID workflows, motion-control failure diagnostic) could roll into v3.4.0 or a v3.4.1 cleanup release depending on appetite.

**Integration risks:**

- **Workspace-first layer (GAP #5)** is the one item that touches the root `SKILL.md` routing. The current routing table is dense and well-tuned. Adding a workspace-first layer means reconciling it with the existing "Route to the Right Skill" table — not a rewrite, but a careful insert. If this is too invasive, a standalone `higgsfield-workspaces` sub-skill with a pointer from the root is a safer option.
- **"Director-first" philosophical framing (shift B)** is already implicit in the skill. Making it explicit risks tone drift if overdone. One-line additions only.
- **Location-as-asset reframing (shift C)** is purely additive to Elements system — low risk.
- **All other HIGH items** are additive subsections inside existing sub-skills — no rewrites, no risk.

Nothing in the PDFs requires rewriting existing skill files. The current skill is in strong shape; v3.4.0 would be a focused gap-fill release on top of a solid foundation.
