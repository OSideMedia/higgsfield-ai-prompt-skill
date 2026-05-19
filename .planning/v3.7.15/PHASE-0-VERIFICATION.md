# v3.7.15 — Phase 0 Verification Report

**Date:** 2026-05-18
**Scope under verification:** cinematic-motion-language.md → vocab.md gap-fill arc (5-pillar system)
**Convention carried from v3.7.13 / v3.7.14:** `.planning/<version>/PHASE-0-*.md`, read-only across Phase 0, cite-by-line, plausibility-over-verification discipline
**Substrate inherited:** DVC Unicode-safe PDF pipeline (v3.7.14); `--dry-run` smoke gate (v3.7.14); `.planning/<version>/` artifact convention (v3.7.13 → v3.7.14)

---

## Headline finding

**v3.7.13's audit holds, with one nuance:** 4 of 5 pillars are full gaps in vocab.md (Camera Contract, Motion Physics Anchor, Spatial Zoning, Lens Behavior Sequence). The 5th (Negative Space) is *partial-coverage-with-additive-content* — vocab.md L338 names the concept but does not capture Adil's negative-prompt-reinforcement pattern or his zone-naming vocabulary. The v3.7.13 framing "already covered under some name" undersells what Adil's pillar adds.

Arc shape recommendation: **patch release (v3.7.15), content-translation-only, $0 probe budget.** The 5-pillar system is craft framework, not API surface. Live-probing universalizing craft claims is high-cost-low-confidence per the calibration we landed in v3.7.13.

Architectural insertion question (where these pillars LAND in vocab.md) is genuinely open — three viable reads, surfaced in VERIFY 0.3 without pre-picking. Phase 1 inventory should resolve it.

One Phase-1 tension flagged: **Motion Physics Anchor directly contradicts the existing `Movement Quality` adjective list** at vocab.md L205-209 (Fluid, jerky, precise, hesitant, etc.). Adil's pillar says "never use these alone." Phase 1 must decide: coexist as different registers, cross-reference, or reorganize.

---

## VERIFY 0.1 — Source file actual content read

Read in full: `~/Desktop/EVEN MORE SKILLS/MORE CUSTOM SKILLS/cinematic-motion-language.md` (209 lines, ~7.7 KB on disk).

**Frontmatter (L1-8):** `name: cinematic-motion-language`. Single-line description claims structured prompt vocabulary for "high-precision cinematic video generation," covering "camera contracts, motion physics anchors, spatial zoning, lens/focus behavior sequences, and negative space as compositional tool."

**Purpose section (L9-19):** sets the core principle —
> "the model understands physics, geometry, sequence, and constraint — not adjectives. Replace every vague descriptor with a physical analogy, spatial coordinate, temporal sequence, or hard rule."

This is the foundational craft-opinion claim that the entire skill rests on. It is universalizing — applies to "the model" generically with no scope qualifier. (See VERIFY 0.4 register analysis.)

**Per-pillar extraction:**

| # | Pillar name (verbatim from source) | Adil's definition (paraphrased) | Problem solved | Concrete examples Adil gives | Cross-refs | Register signal |
|---|---|---|---|---|---|---|
| 1 | **Camera Contract** (L24, `### 1. Camera Contract`) | State the camera's behavior as a hard rule before describing anything else. "The model treats the camera as a character — define it or it will improvise." (L26) | Camera improvisation when behavior is left implicit. | "Static locked-off camera. Zero movement. No pan, no zoom, no dolly, no shake." / "Slow push-in only — 10% scale change over the full duration." / "Single handheld drift, slight organic sway, no cuts." (L29-31). Closing rule: "Always reinforce camera rules in the negative prompt as well." (L33) | No external citations. No Higgsfield-product cross-refs. Internal cross-ref forward to Negative Prompt usage. | **Mixed.** The "treats camera as a character" framing is craft opinion at HARD RULE volume. The concrete patterns (state-as-hard-rule + negative-prompt-reinforce) are specific, falsifiable production discipline. |
| 2 | **Motion Physics Anchor** (L37, `### 2. Motion Physics Anchor`) | "Give every moving element a speed reference from the physical world, not an adjective. Pair physical analogies with time-anchored measurements for maximum precision." (L38-39) | Adjectival speed descriptors ("slow," "fast," "gentle," "subtle") producing unpredictable model output. | Speed analogies: "like dust suspended in honey" / "like embers floating in still air" / "like smoke through a cathedral at dawn" / "like the surface of a lake disturbed by a single drop" (L42-45). Time anchors: "one full revolution across the entire 10-second clip" / "roughly 6 degrees per second" / "the pace of a clock's hour hand — imperceptibly slow" / "travels the full arc in 8 seconds with no pause" (L48-51). HARD RULE: "Never use 'slow', 'fast', 'gentle', 'subtle' alone — always anchor to physics or time." (L53) | No external citations. No product cross-refs. | **Mixed.** Concrete analogies + time-anchor structure are valuable production patterns (specific, transferable). The HARD-RULE prohibition on adjectives is universalizing craft opinion that should be softened. |
| 3 | **Spatial Zoning** (L57, `### 3. Spatial Zoning`) | "Divide the frame into named regions and assign explicit rules to each. This prevents the model from filling empty space with invented content." (L58-59) | Model filling unspecified frame regions with invented content. | Region naming: "Left third / center third / right third" / "Foreground plane / midground / background" / "Upper half / lower half" / "Right two-thirds / left void" (L62-65). Zone rules: "Left third: pure black, no light, no particles, no movement." / "Right two-thirds: all action contained here." / "Foreground plane: particle layer only — no subject." / "Background: unlit void, no detail." (L68-71). Closing rule: "Always cross-reference spatial zones in the negative prompt." (L73) | No external citations. No product cross-refs. | **Mostly production-knowledge.** Specific, falsifiable, low metaphysical volume. Aligns with existing vocab.md Composition Vocabulary entries (Negative space, Crossing rule, Coordinate notation) in shape and register. |
| 4 | **Lens Behavior Sequence** (L77, `### 4. Lens Behavior Sequence`) | "Describe focus and depth of field as a narrative event with a beginning, middle, and end. Models can simulate focus-breathing, rack focus, and lens diffusion — but only when the sequence is described explicitly as cause and effect." (L78-80). Structure: "trigger → shift → state → return → repeat" (L82) | Static / single-state focus descriptions producing flat depth-of-field renders that don't evolve. | Full worked example at L85-87 (foreground crossing → focus shift → bokeh → focus return → cycle 2-3×). Lens vocabulary list at L90-95: "shallow depth of field" / "focus-breathing" — organic in/out shift / "rack focus" — deliberate, directional shift / "bokeh silhouette" — subject dissolves into soft out-of-focus warmth / "lens plane crossing" — moment a foreground element passes between camera and subject / "anamorphic lens rendering" — oval bokeh, horizontal flare, widescreen feel. | No external citations. No product cross-refs. | **Mixed leaning production-knowledge.** Cause-effect structure + vocabulary list are concrete and useful. The "but only when" universalizing claim about model behavior is craft opinion that should be softened to "tends to produce." |
| 5 | **Negative Space as Compositional Tool** (L99, `### 5. Negative Space as Compositional Tool`) | "Name empty areas of the frame as intentional design decisions, not absences. Then reinforce them in the negative prompt." (L100-101) | Empty frame regions read as absence/oversight rather than intentional weight. | Naming examples: "Sacred emptiness — the left third is a deliberate compositional weight." / "No light bleed into the dark half." / "The darkness is active, not background." / "Void occupies the left two-thirds — no fill, no ambient spill, no movement." (L104-107). Negative-prompt pattern: "particles on the left side, light on the left side, movement on the left side" (L110). | No external citations. Implicit cross-ref to Spatial Zoning (zones include negative-space zones). | **Production-knowledge** for the negative-prompt reinforcement pattern. **Stylistic** for the evocative naming ("sacred emptiness," "active darkness") — borrows from cinematography register but not metaphysically. |

**Beyond the pillars** — the source file also contains:
- **The Prompt Template** (L114-149): a structured CAMERA / ASPECT / DURATION / Style&Mood / Narrative / Action / Lens / Lighting / Spatial Zones / Audio / Quality / Negative Prompt template integrating all 5 pillars. **Not part of any pillar; an integration artifact.** Phase 1 decision: do we adopt the template wholesale, or just the pillar vocabulary?
- **Key Vocabulary Reference** (L153-178): a flat-list quick-reference duplicating the per-pillar vocabulary in compact form (Camera / Motion Speed / Particle Behavior / Lens / Focus / Lighting / Negative Space). Useful as a translation source.
- **Advanced Techniques** (L182-184): single forward-pointer to `references/implied-off-screen-motion.md`. **Relative path internal to Adil's skill — not portable, do not import.**
- **Worked Example — Dervish Shot** (L186-209): concrete worked example applying all 5 pillars. **Not part of any pillar; pedagogical artifact.** Phase 1 decision: adopt as an example in our skill, link out, or leave behind?

**Author-signature calibration check** (carrying forward from v3.7.13's "strong craft, weak provenance"):

The hypothesis strengthens on this read. Specific signals:
- The HARD RULE volume is high throughout — "Always," "Never," "non-negotiable" framing is the dominant register
- Zero external citations (no textbooks, no named films, no DPs, no documentation)
- Zero falsifiable claims tied to verifiable model behavior (no "as of v3 of model X" or "tested against N runs")
- The vocabulary itself (anamorphic, focus-breathing, bokeh, rack focus, chiaroscuro, golden hour) is standard cinematography terminology — Adil is *applying* craft language, not *inventing* it
- The synthesis (the 5-pillar grouping) is Adil's contribution and is genuinely useful as a teaching scaffold

So the calibration: **the pillar names and grouping are Adil's craft synthesis (translate freely); the vocabulary inside each pillar is standard cinematography (already plausibly correct, adopt close to verbatim); the universalizing claims about "how the model thinks" are craft opinion at HARD RULE volume (downgrade register).**

---

## VERIFY 0.2 — Current vocab.md structure + gap-check lexical grep

Read in full: `~/Projects/higgsfield/vocab.md` (371 lines).

### 0.2a — Top-level structure

vocab.md is organized **thematically**, not alphabetically or by-axis. Top-level sections:

| # | Section | Line | Sub-sections present |
|---|---|---|---|
| 1 | Camera Movement Terminology | L3 | Linear / Vertical / Orbit-Arc / Zoom / Follow-Immersive / Cinematic Techniques / Camera Angles / Time-Based / Cut & Continuity / Editing Syntax / Motion Hierarchy |
| 2 | Shot Size Vocabulary | L94 | (flat table) |
| 3 | Visual Style Vocabulary | L115 | Named Platform Styles / Aspect Ratio / Color Grade / Color rules / Film Stock |
| 4 | Lighting Vocabulary | L161 | (table) + Scene-physics lighting |
| 5 | Subject & Character Vocabulary | L197 | Body Language / Movement Quality / Emotion Cues / Emotion as Visible Behavior |
| 6 | Environment & Atmosphere Vocabulary | L242 | Time of Day / Weather / Environment Types / World Through Recurrence |
| 7 | Audio / Sound Vocabulary | L286 | (table) |
| 8 | Platform Feature Vocabulary | L299 | (table) + Image Reference Notations |
| 9 | **Composition Vocabulary** | L334 | (flat bullets: Negative space, Crossing rule, Coordinate notation) |
| 10 | Production Vocabulary | L344 | (flat bullets) |
| 11 | Micro-Expression Vocabulary | L353 | (table) |

**Frontmatter:** vocab.md has NO YAML frontmatter — it is a reference document with a single `# Higgsfield Vocabulary Reference` H1 at L1. This is consistent across `vocab.md`, `model-guide.md`, `image-models.md`, `photodump-presets.md`, `prompt-examples.md` (the root-level reference docs the dispatcher cites). Phase 1 implication: new content lands as new H2/H3 sections, not as new files.

**Organizational scheme:** thematic-by-craft-domain (camera, shot size, visual style, lighting, subject, environment, audio, platform, composition, production, micro-expression). Each domain section has sub-sections for specific concepts. This shapes the architectural insertion question (VERIFY 0.3).

### 0.2b — Negative Space current coverage

**Location:** vocab.md L338, single bullet under § Composition Vocabulary.

**Full text (L338):**
> **Negative space** — the deliberately-empty area of the frame that isolates or weighs the subject. Production-direction language: `negative space sits center-left of frame, narrowing as the character advances`. Naming negative space as a compositional element prevents the model from filling it with incidental detail.

**Coverage assessment:** captures the *concept* (deliberately-empty area + naming-prevents-fill mechanism). Does NOT capture:
- The **negative-prompt reinforcement pattern** Adil teaches at L109-110 ("particles on the left side, light on the left side, movement on the left side" as explicit negative-prompt entries)
- The **evocative naming vocabulary** ("sacred emptiness," "active darkness, not background," "deliberate compositional weight," "void occupies the left two-thirds")
- The **tight binding to Spatial Zoning** (negative space as one named zone among others, not as an isolated concept)

**Verdict on v3.7.13 finding:** "Negative space is already covered" was directionally correct but undersells the additive content. Phase 1 should decide whether to *expand* the existing bullet (adding negative-prompt pattern + zone-binding) or *leave it terse* (the concept is named; depth lives elsewhere). I lean toward expansion because the negative-prompt-reinforcement pattern is the production-discipline part most likely to actually move generation quality.

### 0.2c — Gap-check lexical grep for the other 4 pillars

Each grep run case-insensitive, with the pillar name plus reasonable lexical variants (per Phase 0 brief).

| Pillar | Lexical variants tried | Hits in vocab.md | Adjacency-considered partial-coverage? |
|---|---|---|---|
| **Camera Contract** | `camera contract`, `camera promise`, `camera commitment`, `shot contract`, `shot promise` | **0 hits.** Zero matches across all variants. | No. Camera Movement section catalogs the camera-mode *vocabulary* (Dolly, Crane, Orbit, etc.) but does NOT teach the prompt-side discipline of stating camera behavior as a hard rule + negative-prompt reinforcement. The "Re-anchoring" entry at L63 is the closest in shape (a prompt-discipline rule) but it's about cross-cut continuity, not within-shot camera contracts. **Genuine full gap.** |
| **Motion Physics Anchor** | `motion physics anchor`, `motion anchor`, `physics anchor`, `motion grounding`, `physics grounding` | **0 hits.** Zero matches across all variants. | **Partial overlap with adversarial framing.** The Movement Quality section at L205-209 lists exactly the adjective vocabulary Adil's pillar prohibits ("Fluid, jerky, precise, hesitant, confident, stumbling" / "Natural, stilted, mechanical, animal-like"). And L58 has "Low Shutter — motion blur from slow shutter speed" — a *technical* speed concept, not a physics-anchor one. The 4-layer Motion Hierarchy at L83-90 separates motion *layers* but does not anchor *speed* per layer. **Genuine full gap on physics-anchor technique. Phase 1 tension flagged: Movement Quality's adjective list directly contradicts Motion Physics Anchor's HARD RULE.** |
| **Spatial Zoning** | `spatial zoning`, `spatial zones`, `frame zones`, `frame divisions`, `compositional zoning`, `grid zoning`, `left third`, `right third`, `center third`, `foreground plane`, `midground` | **1 hit:** L340 (Coordinate notation entry mentions "right third" inline as an example). | **Partial coverage by adjacency only.** Coordinate notation at L340 (`Character A stands in the right third, x-position 70%...`) uses third-region language as an *example* of qualitative spatial anchoring — it doesn't formalize the system of named regions + per-region rules + negative-prompt cross-reference that Spatial Zoning is. Negative space at L338 names the concept of a deliberately-empty region but doesn't generalize to a region-naming system. **Genuine gap on the formalized zoning system.** |
| **Lens Behavior Sequence** | `lens behavior`, `lens sequence`, `focal sequence`, `lens action sequence`, `focus event`, `focus-breathing`, `rack focus`, `bokeh silhouette`, `lens plane` | **1 hit:** L26 ("Rack Focus — refocus between near and far subjects"), under § Camera Movement → Zoom. Plus fragmentary mentions: L121 "Anamorphic" (Visual Style → Named Platform Styles, treated as *style*), L129 anamorphic-as-style row, L216 "shallow depth of field" (inline in Emotion Cues → Intimacy). | **Highly fragmented partial coverage.** Existing material treats lens concepts as one-line atoms scattered across Camera Movement, Visual Style, and Emotion Cues — not as a sequence-of-events vocabulary. No focus-breathing, no bokeh silhouette, no lens plane crossing, no trigger→shift→state→return→repeat structure. **Genuine gap on the sequence-as-narrative-event technique and most of the vocabulary list.** |

**Per-pillar lexical-variants footnote:** Variants chosen by (a) Adil's exact name + (b) reasonable rephrasings using craft-equivalent terms + (c) prompted variants from the Phase 0 brief. No exotic synonyms tried; grep was case-insensitive throughout. Confident the variants cover the conceptual surface area — additional variants would not surface coverage that this set missed.

**Amended v3.7.13 finding:** "4 of 5 pillars are genuine gaps; the 5th (Negative Space) is partial-coverage-with-additive-content." This is a more accurate characterization than v3.7.13's "Negative space is already covered under some name" — the concept is named but Adil's pillar adds production-discipline content not present in our entry.

---

## VERIFY 0.3 — Architectural insertion question

vocab.md's existing organizational scheme is **thematic-by-craft-domain**. The 4 new pillars fit into that scheme in three different ways, depending on how much we value preserving the 5-pillar-system coherence vs. integrating with existing structure.

### Option A — Per-pillar slots into best-fitting existing section

Each pillar becomes a new `###` sub-section inside the most-appropriate existing `##` section:

| Pillar | Lands in | New `###` heading position |
|---|---|---|
| Camera Contract | § Camera Movement Terminology | After § Motion Hierarchy (L81), before § Shot Size Vocabulary (L94). New `### Camera Contract`. |
| Motion Physics Anchor | § Camera Movement Terminology (or § Subject & Character Vocabulary depending on read) | If under Camera: after Motion Hierarchy. If under Subject: cross-referenced with Movement Quality (with adversarial-tension callout). Phase-1 decision. |
| Spatial Zoning | § Composition Vocabulary (L334) | Insert above Negative space at L338. New `### Spatial Zoning` ahead of the existing flat bullets. |
| Lens Behavior Sequence | § Camera Movement Terminology (or new top-level § Lens Vocabulary) | If under Camera: after Zoom (L24) or as new `### Lens Behavior Sequence`. If new top-level: § Lens Vocabulary between Shot Size and Visual Style. |

**Pros:** integrates naturally with the existing thematic-by-domain scheme; readers searching for camera-mode vocabulary find Camera Contract there; readers searching for composition find Spatial Zoning + Negative Space side-by-side. Distributes the cognitive load — no single mega-section.

**Cons:** the 5-pillar system loses visible coherence as a unit. A reader new to Adil's framework can't see the 5 pillars together. We lose the pedagogical hook that "these 5 pillars work together for high-precision video prompts." The Prompt Template (L114-149 in source) becomes orphaned — it integrates all 5, but no single section owns it.

### Option B — Dedicated "Cinematic Motion Language" section as a coherent unit

A new top-level `## Cinematic Motion Language` section is added (probably between § Composition Vocabulary and § Production Vocabulary, or before § Composition Vocabulary). It contains all 5 pillars as `###` sub-sections, with intro text that frames the system as an integrated approach. Negative Space gets a cross-reference (or is duplicated) since it already exists at L338.

**Pros:** preserves the 5-pillar coherence. New readers can see the system as a whole. The Prompt Template can live inside this section as a `### Integrated Template`. The pedagogical scaffolding stays intact. Easier to cite (`vocab.md § Cinematic Motion Language` is one reference, not 4).

**Cons:** redundancy with existing scattered coverage — Negative Space appears twice (or one moves), Rack Focus appears in both § Camera Movement → Zoom and § Cinematic Motion Language → Lens Behavior Sequence, "shallow depth of field" appears inline in Emotion Cues AND in Lens Behavior Sequence. Either we duplicate (creating drift risk), or we move content into the new section (losing existing adjacencies). Also: vocab.md becomes uneven — most sections are domain-organized, one section is system-organized.

### Option C — Distributed with explicit cross-reference scaffolding

Hybrid of A and B: each pillar lands in its best-fitting existing section (per Option A), but a new short § Cinematic Motion Language section is added with intro text + a 5-bullet jump-table pointing to where each pillar lives. The jump-table preserves the system's coherence as a *navigational* unit without duplicating content.

```
## Cinematic Motion Language (5-pillar system)

A 5-pillar approach to high-precision video prompts. The pillars are integrated
across this document — this section indexes them for readers who want the system
view first.

1. Camera Contract → § Camera Movement Terminology → Camera Contract
2. Motion Physics Anchor → [TBD — Camera Movement or Subject & Character]
3. Spatial Zoning → § Composition Vocabulary → Spatial Zoning
4. Lens Behavior Sequence → § Camera Movement Terminology → Lens Behavior Sequence
5. Negative Space → § Composition Vocabulary → Negative space (expanded)
```

**Pros:** preserves both (a) integration with existing thematic structure and (b) system-level coherence. Low duplication. Reader chooses entry path — domain-first or system-first. Citation works from both angles.

**Cons:** introduces a navigational pattern that no other section in vocab.md currently uses (could feel like one-off scaffolding). Index gets stale if a pillar moves. Slightly more cognitive overhead than pure A or pure B.

**Decision deferred to Phase 1 transition.** All three options are viable. My read is that the right answer depends on whether the user wants vocab.md to read as a *reference manual* (Option A, no system-level abstractions) or as a *teaching document* (Option B, system-level abstractions visible) or as both (Option C, hybrid scaffolding). This is a documentation-philosophy question, not a verification question.

---

## VERIFY 0.4 — Per-pillar register classification + translation strategy

Carrying forward the v3.7.13 calibration (Adil = strong craft, weak provenance), with the VERIFY 0.1 author-signature check (calibration strengthens on reading actual content). The classification:

| # | Pillar | Specific-and-unguessable parts (adopt close to verbatim) | Universalizing-craft parts (downgrade register) | Translation strategy |
|---|---|---|---|---|
| 1 | Camera Contract | "State the camera's behavior as a hard rule" — production discipline. The concrete patterns ("Static locked-off camera. Zero movement. No pan, no zoom, no dolly, no shake.") — directly transferable. "Always reinforce camera rules in the negative prompt" — production-discipline tactic that aligns with our skill's existing negative-prompt material. | "The model treats the camera as a character — define it or it will improvise" (L26) — metaphysical claim about model behavior at HARD RULE volume. Source attributes intent to an unintentful system. | **Mixed-handling.** Adopt the prompt-discipline patterns (state-as-hard-rule, reinforce-in-negative-prompt). Drop the "treats camera as a character" metaphor. Frame as: *"State camera behavior explicitly in the prompt; reinforce camera constraints in the negative prompt to prevent unintended camera moves."* |
| 2 | Motion Physics Anchor | Physical-analogy speed references (the dust/honey/embers/cathedral-smoke examples) — useful, transferable craft vocabulary. Time-anchored measurement structure (full revolution / N seconds / N degrees per second / "pace of a clock's hour hand") — concrete prompt-side technique. | The HARD RULE prohibition: "Never use 'slow', 'fast', 'gentle', 'subtle' alone — always anchor to physics or time" (L53) — universalizing. Adjectival speed descriptors are not strictly forbidden; they're just less precise. The Movement Quality section at vocab.md L205-209 uses exactly these adjectives and that section is functional. | **Mixed-handling.** Adopt the analogy-and-time-anchor vocabulary as a *higher-precision alternative* technique. Soften the "Never" to "When precision matters, anchor to physics or time rather than adjectives." Cross-reference Movement Quality (which lives in different register: general performance direction, not motion-speed specification). **Phase 1 must resolve the Movement Quality contradiction.** |
| 3 | Spatial Zoning | Named-region naming conventions, per-region rule grammar, negative-prompt cross-reference pattern — all specific, falsifiable, transferable. This pillar has the cleanest production-knowledge register of the five. | "This prevents the model from filling empty space with invented content" (L59) — falsifiable production claim, defensible (well-aligned with how transformer-based video models respond to explicit constraints). | **Adopt close to verbatim, translate to our voice.** Aligns naturally with the existing § Composition Vocabulary entries (Negative space, Crossing rule, Coordinate notation) in shape and register. Easiest pillar to translate. |
| 4 | Lens Behavior Sequence | Cause-effect structure (trigger → shift → state → return → repeat) — transferable. Vocabulary list (focus-breathing, rack focus, bokeh silhouette, lens plane crossing, anamorphic rendering) — standard cinematography, adopt as-is. Worked focus-event example (L85-87) — illustrative. | "Models can simulate focus-breathing... but only when the sequence is described explicitly as cause and effect" (L79-80) — universalizing. Plausible but the "only when" claim isn't strictly true. Models also produce focus-breathing from less structured prompts; sequence-description tends to produce more *consistent* focus-breathing. | **Mixed-handling.** Adopt structure + vocabulary. Soften "only when" to "tends to produce cleaner / more reliable focus events when." |
| 5 | Negative Space | Negative-prompt reinforcement pattern (the explicit negative-prompt entries naming the excluded zone) — production discipline, additive to our existing L338 coverage. Tight binding to Spatial Zoning (negative space as named zone among others) — production-discipline structure. | "Sacred emptiness," "active darkness, not background" — stylistic/evocative naming. Borrows from cinematography register; not metaphysical, but register-shift from our existing terse production-direction voice. | **Adopt the production-discipline parts (negative-prompt reinforcement, zone binding) into the existing L338 bullet as an expansion. Optionally surface the evocative naming as example language but at lower register volume than Adil uses (e.g., as one quoted example rather than as definitional vocabulary).** |

**Cross-pillar pattern: negative-prompt reinforcement.** Three pillars (Camera Contract, Spatial Zoning, Negative Space) all close with the same production-discipline tactic — "reinforce in the negative prompt." This is Adil's strongest cross-pillar technical claim and likely the highest-impact discipline-pattern to surface. Phase 1 should consider whether to extract this as a top-level technique with cross-refs to the three pillars that use it, or to leave it embedded per-pillar.

---

## VERIFY 0.5 — Probe scope

**Verdict: option (c) — content-translation-only arc, $0 probe budget.**

### Probe-amenability per pillar

| Pillar | Falsifiable claim a probe could target | Probe shape | Estimated credit cost | Confidence ROI |
|---|---|---|---|---|
| Camera Contract | "Models improvise camera behavior when not given a hard-rule camera contract" | A/B paired generation: same brief, one prompt with "Static locked-off camera. Zero movement." prefix, one without. Compare camera behavior in output. | $1-3 per pair on Seedance/Kling; need 3-5 pairs for low-confidence read = $5-15 | **Low.** Subjective comparison. Result tells us about THESE prompts, not the general claim. |
| Motion Physics Anchor | "Physical-analogy speed anchors produce more controlled motion than adjectives" | A/B: "slow particles drifting" vs. "particles like dust suspended in honey." | $1-3 per pair × 3-5 pairs = $5-15 | **Low.** Same comparison-fuzziness problem. The directional answer is already plausible (more specific prompt → more specific output is a widely-validated pattern across image/video models). |
| Spatial Zoning | "Naming a zone as black-with-no-content makes the model respect it" | Single prompt with explicit zone rule. Check whether the named zone is respected in output. | $1-3 for one generation | **Medium.** Single-prompt test, falsifiable. But: this is standard prompt-engineering discipline that's been validated across many models; probe would confirm what's already plausible. |
| Lens Behavior Sequence | "Models execute multi-stage focus events when described as cause-effect" | Sequence-structured prompt vs. static-DoF prompt. Compare focus behavior across the clip. | $1-3 per pair × 3-5 pairs = $5-15 | **Low.** Most expensive to verify subjectively. |
| Negative Space | Already established; existing coverage at L338. No probe needed. | — | $0 | N/A |

### Why option (c)

1. **Calibration carries forward** — v3.7.13 spent $0/$25 because schema-level evidence retired probe spend; v3.7.14 was infrastructure-only with no probes. The pattern across the arc has been: spend $0 unless probes would *change* the disposition. None of the above probes would change the TRANSLATE-WITH-VERIFICATION disposition.
2. **The 5-pillar system is craft framework, not API surface** — falsifiable claims are all of the form "more-specific prompts produce more-specific outputs," which is plausibly correct across models and doesn't need re-verification per pillar.
3. **Worst case of being mildly miscalibrated is low** — a prompt-engineering vocabulary that's 90% directionally correct (rather than 100% empirically verified) still moves generation quality. The downside risk is "users get slightly-less-effective prompts," not "users get broken outputs."
4. **Probe budget for the arc is N/A** — no budget was set, and given the cost-confidence ratios above, declaring zero is the right call.

### If user wants ONE probe anyway

Cheapest-highest-information probe: **single Spatial Zoning A/B** (named-zone vs. no-named-zone, same brief, low-cost model like Seedance Lite). Estimated cost: $1-3 total. Falsifiable on a single comparison. Doesn't change Phase 1 disposition either way, but provides one piece of empirical evidence for the strongest production-knowledge pillar.

I do not recommend running this probe — it confirms what's already plausible — but surfacing it in case the user disagrees.

---

## Phase 1 transition — open questions

Surfacing for the user, ahead of Phase 1 inventory:

1. **Architectural insertion (VERIFY 0.3):** Option A (per-pillar slots), Option B (dedicated unit), or Option C (distributed + index scaffold)? Documentation-philosophy call.

2. **Motion Physics Anchor ↔ Movement Quality tension (VERIFY 0.2c, VERIFY 0.4):** vocab.md L205-209 lists adjectives Adil's pillar prohibits. Three resolutions: (i) coexist as different registers with cross-reference, (ii) downgrade Movement Quality to "general performance direction" and add Motion Physics Anchor as "high-precision speed specification," (iii) reorganize Movement Quality. Recommend (ii) as the lowest-disruption option.

3. **Negative Space expansion (VERIFY 0.2b):** expand the existing L338 bullet with negative-prompt reinforcement + zone-binding, or leave terse and let Spatial Zoning carry the depth? Recommend expansion — the negative-prompt-reinforcement pattern is the highest-impact production-discipline element across three pillars and shouldn't be implicit.

4. **Prompt Template adoption (VERIFY 0.1):** Adil's full prompt template (L114-149 in source) integrates all 5 pillars. Do we (a) import it as an example into vocab.md or `prompt-examples.md`, (b) cite it as a teaching artifact without adopting wholesale, or (c) leave it behind entirely? Phase 1 question; my lean is (b) — the template is pedagogical not vocabulary.

5. **Worked Example — Dervish Shot (L186-209):** same question shape as #4. Adopt as an example, cite-only, or leave behind?

6. **Cross-pillar negative-prompt-reinforcement extraction (VERIFY 0.4):** three pillars share this tactic. Extract as standalone technique, or keep embedded per-pillar? Phase 1 inventory decision.

---

## Locked decisions

- **Arc shape:** patch release (v3.7.15), content-translation-only, $0 probe budget. Bumps `vocab.md` content + CHANGELOG + dispatcher SKILL.md sub-skill description (if changed) + USER-GUIDE.pdf via the hardened v3.7.14 pipeline. No infrastructure changes expected.
- **Substrate:** v3.7.14 DVC pipeline + `--dry-run` smoke gate carry forward. No font change. No new validators. If the v3.7.15 content additions trigger Layer 1 re-baseline of `USER-GUIDE.pdf.baseline`, that's a normal re-baseline event per the v3.7.13/v3.7.14 pattern.
- **Read-only Phase 0:** confirmed compliance. Zero writes to `~/Projects/higgsfield/` (this report lives under `.planning/v3.7.15/` which is the artifact directory — not a source-code edit). Zero reads or writes to `~/Desktop/EVEN MORE SKILLS/` beyond the single Read of cinematic-motion-language.md. No confidential or pre-release material encountered.
- **Disposition:** TRANSLATE-WITH-VERIFICATION confirmed from v3.7.13. Per-pillar register classifications in VERIFY 0.4 are the Phase 1 input.
- **Gap-check outcome:** 4 of 5 pillars are full gaps. Negative Space is partial-coverage-with-additive-content. Total content-translation surface: 4 new sections (or sub-sections) + 1 expansion.

---

## Phase 0 artifacts (NOT committed to repo)

None. This arc is content-translation-only; no probe artifacts, no measurement scripts, no temp font directories. The PHASE-0-VERIFICATION.md report itself is the sole Phase 0 output, living in `.planning/v3.7.15/` per convention.

---

**STOP. Awaiting user review before Phase 1 inventory.**
