# PDF Integration Audit — v3.6.0 candidate

Date: 2026-04-25
Source material: 8 community/creator PDFs (reviewed externally, not stored in repo) plus hands-on UI verification of Cinema Studio 3.5 conducted on 2026-04-25.

This report is an analytical summary of what the eight PDFs cover, compared to the current state of the higgsfield-ai-prompt-skill, and how that material lines up with what was verified directly in the Cinema Studio 3.5 UI on 2026-04-25. All PDF content is described in paraphrase; no verbatim tables, prompts, or long quotes from the source material appear in this report. Three of the eight PDFs are sibling pairs (a slide-deck and a long-form/prose version of the same body of work), and the overlap is collapsed in the Cross-PDF overlaps section. The Cinema Studio 3.5 platform changes themselves came out of live UI verification, not from any single PDF — the CinemaStudioRecap PDF served as a visual confirmation pass against what the UI surfaces.

---

## Summary table

| PDF | Total items | DUPLICATE | REINFORCE | GAP | PHILOSOPHICAL |
|-----|-------------|-----------|-----------|-----|---------------|
| Building a Cinematic Universe — Mr. Core slide deck | 8 | 8 | 0 | 0 | 0 |
| Building a Cinematic Universe — Mr. Core long-form | 12 | 6 | 2 | 4 | 0 |
| CinemaStudioRecap (Cinema Studio 3.5 visual guide) | 14 | 0 | 0 | 14 | 0 |
| ONESHOT (creator workflow memoir) | 6 | 0 | 0 | 0 | 6 |
| Seedance 2 — Serious Examples Supplement | 9 | 7 | 1 | 1 | 0 |
| Seedance 2.0 Prompt Modes & Prompt Building Framework (slide deck) | 8 | 7 | 0 | 1 | 0 |
| Seedance Promt modes (prose handbook) | 8 | 8 | 0 | 0 | 0 |
| UNDERNEATH THE CHAOS (creator workflow memoir) | 5 | 0 | 0 | 0 | 5 |
| **TOTAL** | **70** | **36** | **3** | **20** | **11** |

---

## Per-PDF findings

### Building a Cinematic Universe — Mr. Core slide deck

A short slide-deck condensation of the Mr. Core long-form workflow document. Functions as a TL;DR of the long-form companion PDF (next entry). Every item in the deck appears in fuller form in the long-form document, so every item is classified DUPLICATE relative to the long-form treatment.

**Content items:**

1. **Pre-production discipline as cost lever** — DUPLICATE of long-form item 1.
2. **AI as collaborator, not vending machine** — DUPLICATE of long-form item 2.
3. **Studio character vs cinematic character distinction** — DUPLICATE of long-form item 3.
4. **Action choreography around AI strengths** — DUPLICATE of long-form item 4.
5. **Location selection rules for AI-friendly spaces** — DUPLICATE of long-form item 5.
6. **Single-generation-per-shot strategy** — DUPLICATE of long-form item 6.
7. **Smooth-cut / morph-cut breathing room** — DUPLICATE of long-form item 7.
8. **Wardrobe-as-generation-cost (piano test)** — DUPLICATE of long-form item 8.

All items: see corresponding entries in the long-form PDF below.

---

### Building a Cinematic Universe — Mr. Core long-form

A creator-author long-form workflow document covering pre-production discipline, location selection, action design around model limits, single-generation strategy, the cost of wardrobe complexity, and the studio-vs-cinematic character distinction. Four GAP candidates surface here. None are in scope for v3.6.0 — all four are deferred to v3.6.1+ planning.

**Content items:**

1. **Pre-production discipline as cost lever** — DUPLICATE
   - Concept: front-load script, shot list, and reference assets before generation.
   - Where it exists: Pre-Prompt Checklist in `skills/higgsfield-prompt/SKILL.md`; Hero Frame and Reference Sheet workflow in `skills/higgsfield-cinema/SKILL.md`.

2. **AI as collaborator, not vending machine** — DUPLICATE
   - Concept: iterative direction beats one-shot prompting.
   - Where it exists: Iteration Rule shipped in v3.4.1 (`skills/higgsfield-prompt/SKILL.md`).

3. **Studio character vs cinematic character — studio output is intermediate** — GAP
   - Concept: when a model returns a character that reads as "studio plastic" (clean, evenly-lit, glossy), treat that as an intermediate frame, not a final — feed it through a Soul Cinema re-pass or a downstream restyle to land on a cinematic-feeling result. The studio look is a stop on the path, not the destination.
   - Where it would go: a new "Intermediate vs final character" section under `skills/higgsfield-soul/SKILL.md` or in the Cinema Studio Hero Frame workflow.
   - Status: deferred to v3.6.1+ backlog. Not in scope for v3.6.0.

4. **Action choreography around AI strengths** — GAP
   - Concept: design action around what the model renders well — circular arenas (the camera can hide most of the choreography), vague ruins (no continuity to break), repeating textures (less drift). Avoid choreography the model fails on (precise hand-to-hand, prop combat, multi-character grappling). Plan one transformation per shot, not a chain of beats.
   - Where it would go: extension of the Fight Scene Rules section in `skills/higgsfield-cinema/SKILL.md`, or a new "Action design discipline" subsection in `skills/higgsfield-prompt/SKILL.md`.
   - Status: deferred to v3.6.1+ backlog. Not in scope for v3.6.0.

5. **Location selection rules for AI-friendly spaces** — GAP
   - Concept: select locations whose geometry forgives drift — circular arenas, repeating textures, vague ruins, fog/dust environments. Avoid locations whose continuity the audience can audit (familiar landmarks, geometric architecture with sight lines).
   - Where it would go: new section in `skills/higgsfield-cinema/SKILL.md` near Location Reference Sheets, or a section in `skills/higgsfield-pipeline/SKILL.md`.
   - Status: deferred to v3.6.1+ backlog. Not in scope for v3.6.0.

6. **Single-generation-per-shot strategy** — GAP
   - Concept: rather than generate-and-pick from many candidates, plan the shot well enough that the first generation lands. Treat each generation as the work, not as exploration.
   - Where it would go: extension of the Iteration Rule in `skills/higgsfield-prompt/SKILL.md`, or a new "Generation budgeting" section.
   - Status: deferred to v3.6.1+ backlog. Not in scope for v3.6.0.

7. **Smooth-cut / morph-cut breathing room — 2-second prompted gaps** — GAP
   - Concept: prompt explicit 2-second still-or-near-still moments at the start AND end of every shot, so editors have material to land morph cuts and smooth cuts on. Without this, every cut has to happen mid-action, which the model renders poorly.
   - Where it would go: addition to the Multi-Shot Manual workflow in `skills/higgsfield-cinema/SKILL.md`, or a new "Cut-friendly shot construction" section in `skills/higgsfield-pipeline/SKILL.md`.
   - Status: deferred to v3.6.1+ backlog. Not in scope for v3.6.0.

8. **Wardrobe-as-generation-cost (piano test)** — REINFORCE
   - Concept: each piece of wardrobe complexity (buttons, ties, jewelry, scarves) is a generation cost; the "piano test" is the rule that if a costume element is as visually demanding as a piano in the frame, the model will spend its budget rendering it instead of the action. Strip wardrobe to the simplest silhouette that still reads as the character.
   - Where it would go: extension of the Outfit / Material Sheet section in `skills/higgsfield-cinema/SKILL.md`, or addition to `skills/higgsfield-soul/SKILL.md`.
   - Status: deferred to v3.6.1+ backlog. Reinforces existing Outfit Sheet pattern; not in scope for v3.6.0.

9. **Reference photography matters more than prompt language** — DUPLICATE
   - Concept: a strong reference image carries the work that prompt prose cannot.
   - Where it exists: Reference-Based Prompt Mode in `skills/higgsfield-seedance/SKILL.md`; @ Element rules in `skills/higgsfield-cinema/SKILL.md`.

10. **Color palette discipline across a project** — DUPLICATE
    - Concept: lock palette early, treat it as a project-wide constraint.
    - Where it exists: Palette / Mood Sheet in `skills/higgsfield-cinema/SKILL.md` (added v3.4.1); Soul Hex color in `skills/higgsfield-moodboard/SKILL.md`.

11. **Lighting language as scene description** — DUPLICATE
    - Concept: describe light as observable behavior (direction, color temperature, source), not as adjectives.
    - Where it exists: Style/Director-Language Prompt Mode in `skills/higgsfield-seedance/SKILL.md`; Anti-Slop Rules in same file.

12. **One transformation per shot** — REINFORCE
    - Concept: limit each shot to a single state change.
    - Where it exists: Beat Density rules in `skills/higgsfield-seedance/SKILL.md` (1 primary change per 4–6s); the existing rule is well-articulated. PDF reframes as "transformation per shot" rather than "beats per duration" — same idea, different surface. No action needed.

---

### CinemaStudioRecap (Cinema Studio 3.5 visual guide)

Primary source material for the v3.6.0 release. A visual recap of the Cinema Studio 3.5 UI surface, used to confirm what was visible during the 2026-04-25 hands-on UI verification. Most items classified as GAP because Cinema Studio 3.5 was previously undocumented in the skill — it sits alongside 2.5 and 3.0 in the model selector but had no skill-side coverage prior to this release.

**Content items:**

1. **Three-pill main UI surface (Genre / Style / Camera)** — GAP
   - Concept: 3.5 collapses creative control into three pills on the main UI; each defaults to Auto and can be overridden manually.
   - Where it would go: new `## Cinema Studio 3.5` section in `skills/higgsfield-cinema/SKILL.md`.
   - Status: IN SCOPE for v3.6.0 (Step 3).

2. **Style Settings — three-axis preset stacking** — GAP
   - Concept: Style pill operates in three modes — Auto, preset stacking (Color Palette / Lighting / Camera Moveset Style), and Manual Style free-form mode.
   - Where it would go: new section per above.
   - Status: IN SCOPE for v3.6.0 (Step 3D).

3. **8 Color Palette presets (Naturalistic Clean, Bleached Warm, Hyper Neon, Teal Orange Epic, Sodium Decay, Cold Steel, Bleach Bypass, Classic B&W)** — GAP
   - Where it would go: Style Settings subsection per above.
   - Status: IN SCOPE for v3.6.0.

4. **6 Lighting presets (Soft Cross, Contre Jour, Overhead Fall, Window, Practicals, Silhouette)** — GAP
   - Status: IN SCOPE for v3.6.0.

5. **9 Camera Moveset Style presets (Classic Static, Silent Machine, One Take, Epic Scale, Intimate Observer, Impossible Camera, Documentary Snap, Raw Chaos, Dreamy Flow)** — GAP
   - Status: IN SCOPE for v3.6.0.

6. **Manual Style free-form mode** — GAP
   - Concept: Manual Style toggle replaces the three-axis preset panel with a free-form Prompt input — this is prompt territory, requires Style/Director-Language Prompt Mode discipline.
   - Where it would go: cross-link to `skills/higgsfield-seedance/SKILL.md` Style/Director-Language Prompt Mode section.
   - Status: IN SCOPE for v3.6.0.

7. **Camera Settings — four-axis panel (Camera Body / Lens / Focal Length / Aperture)** — GAP
   - Concept: restored optical physics surface, with a simpler 3-body abstraction (Clean Digital, Fine Film, Raw 16mm) instead of 2.5's six camera bodies. Different vocabulary from 2.5.
   - Where it would go: new section per above.
   - Status: IN SCOPE for v3.6.0 (Step 3E).

8. **5 Lens characters (Vintage Haze, Warm Halation, Anamorphic, Extreme Macro, Clinical Sharp)** — GAP
   - Status: IN SCOPE for v3.6.0.

9. **Focal length set including new 75mm** — GAP
   - Concept: 5 focal lengths in 3.5 (8mm, 14mm, 35mm, 50mm, 75mm) — 75mm is new vs 2.5's 8/14/35/50mm set.
   - Status: IN SCOPE for v3.6.0.

10. **Genre catalog (General, Action, Horror, Comedy, Noir, Drama, Epic + others scrollable)** — GAP
    - Concept: 7 confirmed genres from the UI, with scroll arrows visible suggesting additional unconfirmed genres exist.
    - Status: IN SCOPE for v3.6.0; documented as the seven confirmed plus a pointer to the live UI for additional genres.

11. **Output controls — Aspect Ratio (7 options including 21:9), Quality (480p / 720p / 1080p), Sound (On/Off), Batch Size, Duration (4s–15s)** — GAP
    - Concept: 480p draft tier is new; 1080p restored vs 3.0's 720p cap.
    - Status: IN SCOPE for v3.6.0 (Step 3G).

12. **AI director toggle (function unverified)** — GAP
    - Concept: toggle visible in the bottom toolbar; function and behavior not yet verified.
    - Where it would go: brief acknowledgment in the new section, with explicit "function deferred to a future release" note.
    - Status: IN SCOPE for v3.6.0 (Step 3H) — acknowledgment only, no behavioral documentation.

13. **Five recommended Style + Camera stacks (Intimate Drama, Gritty Realism, Cold Thriller, Epic Landscape, Impact Close-up)** — GAP
    - Concept: not built-in UI presets — recommended manual combinations across Style Settings and Camera Settings panels.
    - Status: IN SCOPE for v3.6.0 (Step 3F).

14. **Element library surface — source tabs (Uploads, Image Generations, Video Generations, Elements, Liked) and element categories (All, Pinned, Shared, Characters, Locations, Props)** — GAP
    - Concept: the full two-dimensional library structure (5 source tabs × 6 element categories) and cross-shot continuity workflow are not currently documented in the skill. The existing Elements System section at lines 95–154 of `skills/higgsfield-cinema/SKILL.md` covers only Character / Location / Prop element types and @-tag rules — it does not document the source tabs or the Pinned / Shared / Liked categories.
    - Where it would go: new `### Element Library Surface — Source Tabs and Categories` subsection appended to the existing Elements System section in `skills/higgsfield-cinema/SKILL.md`.
    - Status: IN SCOPE for v3.6.0 (Step 4).

---

### ONESHOT (creator workflow memoir)

A creator-voice memoir of a one-shot generation workflow. Reads as personal philosophy and process narration rather than enumerable techniques. Classification PHILOSOPHICAL throughout — no GAPs.

**Content items:**

1. **Authorial process narration** — PHILOSOPHICAL.
2. **Personal taste as creative anchor** — PHILOSOPHICAL.
3. **The role of accident in creative work** — PHILOSOPHICAL.
4. **AI as material, not as oracle** — PHILOSOPHICAL.
5. **Patience as a craft** — PHILOSOPHICAL.
6. **Authorship in the AI era** — PHILOSOPHICAL.

No actionable items extractable. Companion to UNDERNEATH THE CHAOS (sibling memoir).

---

### Seedance 2 — Serious Examples Supplement

A worked-prompt examples supplement to the Seedance 2.0 documentation. Most examples are illustrations of patterns already documented in `skills/higgsfield-seedance/SKILL.md` and `MODELS-DEEP-REFERENCE.md`. One mode (Transformation) flagged for possible example-library expansion in a later release.

**Content items:**

1. **Reference-Based Prompt Mode worked examples** — DUPLICATE of `higgsfield-seedance` Reference-Based section.
2. **Continuation Prompt Formula worked examples** — DUPLICATE of v3.4.0 Continuation Prompt Formula.
3. **Expand Shot worked examples** — DUPLICATE of v3.4.0 Expand Shot section.
4. **Edit Shot worked examples** — DUPLICATE of v3.4.0 Edit Shot section.
5. **Style/Director-Language worked examples** — DUPLICATE of existing Style/Director-Language section.
6. **Five-Layer Stack worked examples** — DUPLICATE of `MODELS-DEEP-REFERENCE.md` Seedance 2.0 Prompt System.
7. **Audio prompting worked examples** — DUPLICATE of `MODELS-DEEP-REFERENCE.md` Audio rules.
8. **Beat Density worked examples** — DUPLICATE of `MODELS-DEEP-REFERENCE.md` Beat Density table.
9. **Transformation prompt mode worked examples** — GAP (deferred)
   - Concept: a possible new mode where the prompt explicitly describes a state change (object → object, character → character, environment → environment) within the duration of a single shot. Distinct from Continuation (which extends an existing clip) and Edit Shot (which modifies a generated clip).
   - Where it would go: new mode in the Seedance 2.0 Prompt Modes section of `skills/higgsfield-seedance/SKILL.md`.
   - Status: deferred to v3.6.1+ backlog as part of an example-library expansion. Not in scope for v3.6.0.

REINFORCE candidate: the worked examples themselves could be added to a dedicated example library, but the underlying patterns are all documented. Status: REINFORCE-only, no action.

---

### Seedance 2.0 Prompt Modes & Prompt Building Framework (slide deck)

A slide-deck presentation of the Seedance 2.0 prompt modes and building framework. Mostly DUPLICATE of v3.4.0 audit material that was already integrated. One candidate gap surfaces: a 6-Pass Testing Protocol — a sequenced testing pass list that may or may not duplicate the Iteration Rule shipped in v3.4.1.

**Content items:**

1. **Reference-Based / Continuation / Expand Shot / Edit Shot mode taxonomy** — DUPLICATE of v3.4.0.
2. **Five-Layer Stack (Subject / Action / Camera / Style / Sound)** — DUPLICATE of `MODELS-DEEP-REFERENCE.md`.
3. **6-Part Field Formula** — DUPLICATE of `MODELS-DEEP-REFERENCE.md`.
4. **Delegation levels (1–4 by complexity)** — DUPLICATE.
5. **Anti-Slop Rules** — DUPLICATE.
6. **Camera Control four-parameter pattern** — DUPLICATE.
7. **One-Take and Nine-Grid storyboard techniques** — DUPLICATE.
8. **6-Pass Testing Protocol — sequenced testing pass list** — GAP (PENDING-CHECK)
   - Concept: a six-pass testing sequence applied when refining a prompt — each pass isolates one variable (subject, action, camera, style, audio, output) and tests in order.
   - Status: needs comparison against the Iteration Rule shipped in v3.4.1 in `skills/higgsfield-prompt/SKILL.md`. The Iteration Rule already enforces single-variable iteration; the 6-Pass Protocol may be a more prescriptive sequencing of which variables to test in which order, OR it may be a full duplicate framed differently.
   - Where it would go: extension of the Iteration Rule in `skills/higgsfield-prompt/SKILL.md`, or a new section if the sequencing turns out to add genuinely new structure.
   - Status: deferred to v3.6.1+ backlog pending the gap-check pass. Not in scope for v3.6.0.

---

### Seedance Promt modes (prose handbook)

The prose / long-form companion to the Seedance 2.0 Prompt Modes slide deck above. Same eight items in fuller paragraph form. Full DUPLICATE of the slide deck — no items unique to the prose version. The 6-Pass Testing Protocol gap-check from item 8 of the slide deck applies here as well; not double-counted.

**Content items:** Identical taxonomy and coverage as the slide deck. All items DUPLICATE.

---

### UNDERNEATH THE CHAOS (creator workflow memoir)

Sibling memoir to ONESHOT — same author voice, same workflow philosophy, same classification. PHILOSOPHICAL throughout, no GAPs.

**Content items:**

1. **Workflow as lived process** — PHILOSOPHICAL.
2. **Embracing failure as input** — PHILOSOPHICAL.
3. **Constraint as creative driver** — PHILOSOPHICAL.
4. **The myth of the finished prompt** — PHILOSOPHICAL.
5. **Authorship and the long game** — PHILOSOPHICAL.

No actionable items extractable. See ONESHOT for sibling treatment.

---

## Cross-PDF overlaps

Three sibling pairs collapse the audit surface:

- **Mr. Core slide deck and Mr. Core long-form** — the slide deck is a strict subset of the long-form document. Every slide-deck item is DUPLICATE relative to the long-form. The four GAPs all surface from the long-form PDF.
- **Seedance 2.0 Prompt Modes slide deck and Seedance Promt modes prose handbook** — slide and prose presentation of the same eight items. The 6-Pass Testing Protocol GAP (PENDING-CHECK) appears in both and is counted once.
- **ONESHOT and UNDERNEATH THE CHAOS** — sibling creator memoirs, same author voice, both PHILOSOPHICAL throughout. No actionable extraction from either.

The CinemaStudioRecap PDF stands alone as the primary source for the v3.6.0 release, alongside the 2026-04-25 hands-on UI verification.

The Seedance 2 Serious Examples Supplement is a worked-examples companion to `MODELS-DEEP-REFERENCE.md`'s existing Seedance 2.0 documentation; it surfaces one new candidate mode (Transformation) and otherwise reinforces existing material.

---

## v3.6.0 release decisions

**IN scope:**

- **Cinema Studio 3.5 platform documentation** — new section in `skills/higgsfield-cinema/SKILL.md` covering the three-pill main UI, Style Settings (three-axis preset stacking + Manual Style free-form mode), Camera Settings (four-axis panel including new 75mm focal length), five recommended stacks, output controls, and AI director toggle acknowledgment. Source: CinemaStudioRecap PDF + 2026-04-25 hands-on UI verification.
- **Elements System extension** — new `### Element Library Surface — Source Tabs and Categories` subsection inside the existing Elements System section in `skills/higgsfield-cinema/SKILL.md`, documenting the five source tabs (Uploads / Image Generations / Video Generations / Elements / Liked) and six element categories (All / Pinned / Shared / Characters / Locations / Props), with library-first workflow guidance and cross-shot continuity tip.
- **Physics Rendering — Resolution Decision Matrix** — cross-model section in `skills/higgsfield-cinema/SKILL.md` applying to Seedance 2.0 and Cinema Studio 3.x: routing rule for fast/chaotic motion (720p), fine-detail physics (1080p), grounded weight (1080p), and draft/exploration (480p).
- **Cinema Studio 3.5 entry** in `skills/higgsfield-models/MODELS-DEEP-REFERENCE.md` mirroring the existing 2.5 / 3.0 structure, with cross-link to the new Cinema Studio 3.5 section in `higgsfield-cinema`.
- **Kling 3.0 quality range refinement** — refine the Kling 3.0 resolution line in `MODELS-DEEP-REFERENCE.md` to "720p / 1080p / 4K HDR" reflecting the current quality dropdown (4K was already documented; 720p added).
- **Cinema Studio version comparison table extension** — fourth column added for Cinema Studio 3.5 in the existing comparison table in `skills/higgsfield-cinema/SKILL.md` (existing 2.5 and 3.0 columns unchanged).
- **Routing entries and sub-skill triggers** — root `SKILL.md` updated to surface Cinema Studio 3.5 in the routing table, in the "What Is Higgsfield?" paragraph, and in the sub-skills triggers row.
- **Frontmatter version bumps** — root `SKILL.md` to 3.6.0 / 2026-04-25; `skills/higgsfield-cinema/SKILL.md` to 3.1.0 / 2026-04-25.

**OUT of scope (deferred to v3.6.1+ backlog):**

- Mr. Core methodology integration — piano test (wardrobe-as-generation-cost), Morph Cut / Smooth Cut breathing room (2-second prompted gaps at start and end of every shot), action choreography around AI strengths (location selection rules, single-generation strategy), studio character vs cinematic character distinction (Soul Cinema re-pass).
- 6-Pass Testing Protocol gap-check against the existing Iteration Rule shipped in v3.4.1.
- Transformation prompt mode addition to the Seedance 2.0 prompt modes catalog.
- Seedance 2.0 worked-example library expansion based on the Serious Examples Supplement.
- AI director toggle behavioral documentation — function not yet verified; toggle acknowledged in v3.6.0 with function deferred.

---

## Backlog — v3.6.3+ planning

| Item | Source | Target location | Priority |
|------|--------|-----------------|----------|
| Wardrobe simplification rule (piano test) | Mr. Core long-form item 8 | `higgsfield-cinema` Outfit / Material Sheet section, or `higgsfield-soul` | MEDIUM |
| Morph Cut / Smooth Cut breathing room (2-second prompted gaps) | Mr. Core long-form item 7 | `higgsfield-cinema` Multi-Shot Manual workflow, or `higgsfield-pipeline` | MEDIUM |
| Action choreography around AI strengths (location rules, single-gen strategy, action-transforming-space cadence) | Mr. Core long-form items 4–6 | `higgsfield-cinema` Fight Scene Rules extension, or `higgsfield-prompt` Action design discipline | MEDIUM |
| Studio character vs cinematic character (intermediate-vs-final, Soul Cinema re-pass) | Mr. Core long-form item 3 | `higgsfield-soul` or `higgsfield-cinema` Hero Frame workflow | MEDIUM |
| 6-Pass Testing Protocol (gap-check against Iteration Rule) | Seedance Prompt Modes slide deck item 8 / prose handbook | `higgsfield-prompt` Iteration Rule extension | LOW (PENDING-CHECK) |
| Transformation prompt mode | Seedance 2 Serious Examples Supplement item 9 | `higgsfield-seedance` Prompt Modes section | LOW |
| Seedance 2.0 worked-example library expansion | Seedance 2 Serious Examples Supplement | `higgsfield-seedance` example library (new) | LOW |
| AI director toggle behavioral documentation | CinemaStudioRecap PDF item 12 + future UI verification | `higgsfield-cinema` Cinema Studio 3.5 section | BLOCKED (function unverified) |
| Per-Cinematic-model deep workflow guidance (image and video) — when to pick each Cinematic model for which intent, prompting patterns specific to each, video-mode picker structure | 2026-04-25 UI verification (additional screenshots) | `higgsfield-cinema` — extend Cinema Studio 3.5 Image Mode subsection + add video-mode picker subsection | HIGH |
| Strip product-marketing language from skill content — file-wide pass on `MODELS-DEEP-REFERENCE.md` (e.g., ⭐ EXCLUSIVE, Current Top Model, similar superlatives) | 2026-04-25 review during v3.6.0 integration | `skills/higgsfield-models/MODELS-DEEP-REFERENCE.md` — file-wide style normalization pass | LOW |
| Path B — Refactor `generate_user_guide.py` to parse `SKILL.md` files dynamically. Eliminates manual sync burden — by v3.6.1 the PDF was 6 releases stale. Substantial release on its own (~3–4 hours of refactor + validation), should not mix with content writing. | 2026-04-25 USER-GUIDE staleness scoping during v3.6.2 planning | `generate_user_guide.py` — full refactor to read `SKILL.md` + `skills/*/SKILL.md` + `CHANGELOG.md` and generate sections dynamically | MEDIUM (v3.7.x+) |
| USER-GUIDE.pdf comprehensive expansion — full Cinema Studio 3.5 / Image Mode / Elements / Physics Matrix / Motion Control / workspace-first / Reference Sheet Types sections. Bundle with Path B refactor since hardcoded sections written now would be discarded in the refactor. | 2026-04-25 USER-GUIDE staleness scoping during v3.6.2 planning | `generate_user_guide.py` after Path B refactor — auto-pull from `SKILL.md` files | LOW (v3.7.x+) |

---

## Methodology notes

- Source material PDFs are external (not committed to this repo); analysis preserved here in paraphrase only. No verbatim tables, prompts, or long quotes from any source PDF appear in this report.
- Cinema Studio 3.5 platform changes were verified against the live Higgsfield UI on 2026-04-25; the CinemaStudioRecap PDF served as a confirmation pass against what the UI surfaced. Where the UI showed scroll arrows or other indicators of additional unconfirmed content (e.g., the Genre catalog), this report and the v3.6.0 release content document only what was visually confirmed.
- The v3.4.0 audit report at `docs/pdf-audit/AUDIT-REPORT.md` remains the methodology template; this report mirrors its structure, classification system (DUPLICATE / REINFORCE / GAP / PHILOSOPHICAL), and per-PDF analytical pattern.
