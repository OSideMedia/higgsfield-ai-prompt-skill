# Changelog

## v3.2.0 — 2026-04-10

### Added
- **`higgsfield-seedance` sub-skill** — dedicated Seedance 2.0 / Pro prompt director
  that enforces the filmmaker-voice discipline required to pass Seedance's LLM-based
  content filter on the first try. Routes from the parent skill on any Seedance
  prompt request, flagged-prompt report, or Seedance credit-waste complaint.
  - Filter model explainer (LLM reads full-scene intent, not a keyword blacklist)
  - Instant-fail vs. delayed-fail diagnostic heuristic
  - Six-slot Seedance prompt formula (Camera + Subject + Action + Setting + Style + Lighting)
  - Rewrite playbook for real names, brands/IP, violence, weapons, horror
  - "Filmmaker not Friend" voice rewrite pass (6 rules)
  - Failure-loop recovery protocol with filter-memory logging
- **`seedance_lint.py` — pre-flight linter** at the project root. Pure stdlib,
  no dependencies. Scans a drafted prompt for 11 filter-risk patterns before
  the user burns credits on an instant-fail rejection.
  - FAIL rules: real-person names, brand/IP, violence verbs, weapon nouns,
    age markers, overlength (>220 words)
  - WARN rules: antislop adjectives, long prompts (>180 words), too-short
    prompts (<15 words), missing Style/Mood clause, missing camera move,
    missing setting, contradictory instructions
  - Output: PASS / WARN / FAIL verdict with per-rule fix suggestions
  - Usage: `python3 seedance_lint.py "<prompt>"` or pipe via stdin or `--file`
  - Exit code 1 on FAIL for CI / script integration
  - **Filter-memory loopback:** `--log` appends FAIL verdicts to
    `db/filter-memory.json` with rule hits as `blocked_terms` + `tags` and
    fix suggestions as `substitution`. `--confirmed` logs a rewrite that
    passed Seedance's filter in a real generation (outcome=workaround,
    substitution_worked=True). Update outcomes later with
    `python3 higgsfield_memory.py update-filter <id> <outcome>`.
- Parent skill routing table + sub-skills list updated to surface
  `higgsfield-seedance` for Seedance / flagged-prompt triggers.

## v3.1.0 — 2026-04-10

### Added
- **Seedance 2.0 Scene Archetype Router** (`higgsfield-prompt`) — planning layer on top of MCSLA
  - Action archetypes: Pursuit / Duel / Impact with decision tree
  - General archetypes: Journey / Atmosphere / Reveal with decision tree
  - Dialogue archetypes: Confrontation / Interrogation / Negotiation with decision tree
  - Dialogue word-limit rule (~25–30 spoken words per 15s)
- **Seedance 2.0 Engine Constraints** (`higgsfield-prompt`) — hard rendering rules
  - ≤3 characters tracked across cuts
  - Exit-frame = implicit cut (never choreograph exit + re-entry)
  - Off-screen = nonexistent (state changes must be shown before referenced)
  - Avoid reflection shots (breaks scene geography)
  - Only see-or-hear (no smell/taste/internal thoughts)
  - Action beats = intent + named technique, not joint mechanics
  - Double-contrast cut rule (shot size AND camera character both change)
  - Causally-motivated inserts with named subject
  - Age-blind character rule (describe by role/clothing/action)
  - Default in medias res
- **Pipeline E: Multi-Style Short Film** (`higgsfield-pipeline`) — Soul Cinema + Nano Banana Pro + Seedance 2.0 chain
  - Style-first keyframe generation with Soul Cinema enhancer ON + minimal prompts
  - Style keyword locators (swap 1–2 words to change whole aesthetic)
  - Edit-don't-regenerate workflow via Nano Banana Pro
  - Prop sheet technique (one-time, multi-angle, material breakdown)
  - Previous-video-as-continuity-reference feedback loop (the key consistency trick)
  - 15-second-per-scene cap rationale
  - 6 pipeline-specific pitfalls
- **Cut & Continuity Vocabulary** section in `vocab.md`
  - Double contrast, camera character, re-anchoring, 180° rule
  - Exit-frame = implicit cut, causally-motivated insert
  - Match cut, smash cut, hard cut, L-cut / J-cut, whip-pan transition
- `docs/Seedance 2 Skill.md` — reference file for the full bilingual EN+ZH Seedance director mode (standalone JSON API pattern)

### Changed
- `higgsfield-prompt` bumped to v3.1.0 (Seedance archetype router + engine constraints added)
- `higgsfield-pipeline` bumped to v3.1.0 (Pipeline E added, decision guide updated)

## v3.0.0 — 2026-04-06

### Added
- Cinema Studio 3.0 support (Business/Team plan only) across all sub-skills
  - Full specs: 15s max duration, 720p video, 2K image, 48 credits, 7 genres, 7 aspect ratios (+ 21:9 ultrawide)
  - Smart shot control (auto camera planning) + Custom multi-shot (up to 6 scenes, 12s)
  - Native dual-channel stereo audio (unified multimodal architecture)
  - Soul Cast 3.0: General (2K) / Character (4K) / Location (4K) modes, 0.125 credits
  - @ reference patterns: up to 9 images, 3 video clips, 3 audio clips (≤12 total)
  - Resolution Comparison Table (Cinema Studio 2.5 vs 3.0) in higgsfield-cinema and higgsfield-models
  - "When to Use 3.0 vs 2.5" decision table
- Seedance 2.0 prompting best practices integrated into MCSLA framework
  - Intent over Precision (30–100 word sweet spot)
  - Director's Formula → MCSLA mapping with early-token priority
  - Genre Router with 7 genre-specific prompt length and lead-with targets
  - I2V Gate rule for image-to-video workflows
  - Anti-Slop vocabulary check (kill: beautiful, stunning, epic, amazing, dynamic, energetic)
  - Physics Language — concrete consequences instead of mood words
  - Degree Adverbs for intensity guidance
  - Narrative Structure Options (fluid vs timestamp storyboard)
  - Three-Act Rhythm for action prompts (Charge-up → Burst → Aftermath)
  - No Negative Prompts guidance (positive constraints only)
- One-Move Rule for camera control (one primary camera move per shot)
- Genre-Based Camera Presets table (8 genres with primary/secondary/avoid)
- Reliable Camera Phrasing Library (7 tested phrases)
- Camera Transfer via @Video reference + Dual Video Reference patterns
- Smart Mode documentation for Cinema Studio 3.0 auto-camera
- Intent-First choreography for motion (describe intent, not timestamps)
- @Video Reference as primary method for action/fight scenes
- Beat Density Diagnostic (1–2 beats per 5 seconds)
- One Style Anchor Rule + "Cinematic Does Nothing" guidance
- CGI Material Contract (4 properties per surface)
- Period Control (materials + lighting, not decade labels)
- Style Transfer via @Reference
- Audio elevated to first-class prompt element (SCELA integration)
  - Native audio-video joint generation documentation
  - Input constraints (MP3/WAV, 3 clips, ≤15s, <15MB)
  - Lip-sync (experimental, single face)
  - Tone/Voice cloning via @Reference
  - Dialect support and timestamp anchoring
  - Sound design specificity guidance
- Character consistency best practices for Soul Cast 3.0
- 6-symptom diagnostic tree for Cinema Studio 3.0 troubleshooting
- Cinema Studio 3.0 genre mappings + prompt length targets in all 10 genre templates
- @reference workflow examples in all 10 genre templates
- Cinema Studio 3.0 Notes in shared negative constraints (positive alternatives table)
- Cinema Studio 3.0 comparison section in higgsfield-models

### Changed
- Seedance 2.0 status: removed all "(upcoming)" labels — now documented as active
- Negative constraints updated: Cinema Studio 3.0 does not support negative prompt syntax — positive alternatives provided
- Genre templates updated with Cinema Studio 3.0 genre mappings and Speed Ramp recommendations
- Dispatcher routing table updated with Cinema Studio 3.0 entries
- Unique Feature Matrix expanded with Cinema Studio 3.0 capabilities

### Preserved
- All Cinema Studio 2.5 documentation remains intact and fully supported
- MCSLA formula retained as primary framework throughout
- All v2.0.2 content preserved — this update is purely additive

---

## v2.0.2 — 2026-03-26

### Fixed: Higgsfield DoP documented as model family
- "Higgsfield DOP" was treated as a single model. DoP is actually the family/brand name for Higgsfield's I2V system with three quality tiers: Higgsfield Lite, Standard, and Turbo (all 720p, 3–5s).
- Added DoP family section to model-guide.md with tier breakdown, 50+ preset categories, and optical physics capabilities.
- Added DoP row to video model comparison tables and decision flowcharts in model-guide.md and higgsfield-models/SKILL.md.
- Updated root SKILL.md, dispatcher SKILL.md, README.md, and CHANGELOG.md references from "Higgsfield DOP" to "Higgsfield DoP (Lite/Standard/Turbo)".

### Fixed: Kling 2.1 Master marked as deprecated
- Kling 2.1 Master is no longer on the platform. Marked as "(deprecated)" in model-guide.md and MODELS-DEEP-REFERENCE.md with notice to use Kling 2.6 or 3.0.
- Removed from Create Video tab model list in model-guide.md.

### Fixed: Grok Imagine Image removed from image model listings
- "Grok Imagine Image" does not exist on the Higgsfield platform — Grok Imagine is a video-only model family.
- Removed from image model quick selection table and decision flowchart in higgsfield-models/SKILL.md.
- Removed from cost table in image-models.md.
- Added "NOT available on Higgsfield" notice to the xAI API documentation section in MODELS-DEEP-REFERENCE.md (documentation preserved for reference).
- Updated Quick Decision Table to redirect former Grok Imagine Image recommendations to GPT Image 1.5, Multi Reference, and Flux Kontext.

### Fixed: Seedance 2.0 labeled as upcoming
- Seedance 2.0 is pre-documented but not yet live on the platform. Added "(upcoming)" labels across model-guide.md, higgsfield-models/SKILL.md, MODELS-DEEP-REFERENCE.md, higgsfield-audio/SKILL.md, higgsfield-troubleshoot/SKILL.md, and shared/negative-constraints.md.
- Decision flowcharts now note "use Seedance 1.5 Pro until launch" as fallback.

### Updated: Version bumped to 2.0.2
- All 21 SKILL.md files, MODELS-DEEP-REFERENCE.md, and README.md bumped from 2.0.1 to 2.0.2.

---

## v2.0.1 — 2026-03-26

### Fixed: Broken shared/negative-constraints.md paths (14 instances)
- 13 sub-skill SKILL.md files referenced `shared/negative-constraints.md` using paths relative to their own directory, which didn't resolve. Fixed to `../shared/negative-constraints.md` in all sub-skills.

### Fixed: Model name accuracy
- **"Nano Banana Pro 2" does not exist.** Corrected to "Nano Banana Pro" across 5 files (13 instances). "Nano Banana", "Nano Banana 2", and "Nano Banana Pro" are three separate models — they were previously conflated.
- **"MiniMax" → "Minimax"** — platform spells it "Minimax Hailuo" (lowercase 'imax'). Fixed across 13 files (26 instances).

### Fixed: Templates missing Identity/Motion guidance
- Templates 01 (action chase), 02 (product UGC), and 07 (landscape) now include Identity/Motion Block callouts referencing template 06 and `higgsfield-soul`.
- Template 03 (horror) restructured: Identity/Motion Block sections moved before Variations to match the format used by the other 9 templates.

### Fixed: MODELS-DEEP-REFERENCE.md frontmatter regression
- `tags` was at the top level instead of inside `metadata` — the exact bug v1.5.1 fixed. Moved back inside `metadata`.

### Fixed: Memory system bugs (higgsfield_memory.py + JSON DBs)
- **ID prefix mismatch:** Seeded entries used `filt-`/`qual-` prefixes but code generates `F-`/`Q-`. Aligned seeded data to match code (`F-001`–`F-004`, `Q-001`–`Q-005`).
- **Date field mismatch:** Seeded entries used `"date"` but code reads `"date_added"`. Renamed in all 9 seeded entries.
- **Missing `outcome` field:** Added `"outcome": "workaround"` to all 4 filter entries.
- **Docstring:** Added `update-quality` to usage docstring (command was wired but undocumented).

### Fixed: README.md structure tree
- Added `validate.py`, `CONTRIBUTING.md`, and `USER-GUIDE.pdf` to the project tree.

### Fixed: validate.py
- Added check for `tags` at top level of frontmatter (the regression it was created to prevent).
- Removed unused `SKILL_DIRS` variable.

### Fixed: Minor consistency
- `higgsfield-recall/SKILL.md`: moved non-standard `compatibility` block inside `metadata`.

### Updated: Version bumped to 2.0.1
- All 21 SKILL.md files, MODELS-DEEP-REFERENCE.md, and README.md bumped from 2.0.0 to 2.0.1.

---

## v2.0.0 — 2026-03-26

### New: Shared Negative Constraints Reference
- Created `skills/shared/negative-constraints.md` — a consolidated, categorized reference of all AI video/image generation artifacts and the prompt phrasing to prevent them.
- Six categories: Body/Motion Artifacts, Face/Identity Artifacts, Texture/Lighting Artifacts, Temporal/Consistency Artifacts, Content Filter/Safety Artifacts, Cinema Studio–Specific Artifacts.
- Each entry includes: the artifact, why it happens in AI video, and the recommended prevention phrase.
- All 18 sub-skills updated to reference this shared file for their relevant artifact categories.
- Domain-specific constraints that only apply to one sub-skill remain in that sub-skill — the shared file supplements, not replaces.

### New: Identity vs. Motion Separation Rule
- Added hard rule to `higgsfield-prompt` and `higgsfield-soul`: when Soul ID or character consistency is involved, prompts must be split into two blocks:
  - **Identity Block** — static visual descriptors only (face, clothing, body, marks). No motion, no camera, no temporal language.
  - **Motion Block** — camera movement, action, speed, environmental changes. No character description repetition.
- Includes 3 before/after examples showing mixed (bad) vs. separated (good) prompts with explanations.
- Added "which descriptors belong where" reference table.
- Updated `higgsfield-recipes`, `higgsfield-pipeline`, `higgsfield-cinema`, and `higgsfield-recall` to reference this separation rule.
- All 10 genre templates include Identity Block + Motion Block sections for character-involved prompts.

### New: Templates Folder (10 annotated genre templates)
- Created `templates/` directory with 10 production-quality annotated prompt templates:
  1. `01-cinematic-action-chase.md` — Chase/pursuit sequences
  2. `02-product-ugc-showcase.md` — Product ads and UGC content
  3. `03-horror-atmosphere.md` — Horror and atmospheric dread
  4. `04-fashion-editorial.md` — Fashion/editorial portraits
  5. `05-sci-fi-vfx.md` — Sci-fi and VFX spectacle
  6. `06-portrait-character-intro.md` — Character introductions
  7. `07-landscape-establishing-shot.md` — Landscape/establishing shots
  8. `08-comedy-social-media.md` — Comedy and social media content
  9. `09-romantic-intimate.md` — Romance and intimate moments
  10. `10-dance-music-performance.md` — Dance/music performances
- Each template includes: genre header, trigger conditions, recommended model, full example prompt, line-by-line annotation, negative constraints reference, common mistakes, and 3-4 variations.
- Templates based on and expanded from proven `prompt-examples.md` prompts.
- Main dispatcher SKILL.md updated with genre-matching routing table for templates.

### New: Sub-Skill Cross-References
- Added "Related skills" footer to all 18 sub-skills pointing to relevant sibling skills.
- Added `shared/` and `templates/` paths to the main dispatcher routing table.
- Updated dispatcher with new "Shared Resources" section.

### Updated: Main Dispatcher
- Version bumped to 2.0.0.
- Added template genre-matching routing table ("Check Templates for Genre Match").
- Added Shared Resources section with paths to `shared/negative-constraints.md` and `templates/`.
- Added template and shared constraint references to the footer resource list.

### Updated: All sub-skills version bumped to 2.0.0
- All 18 sub-skill SKILL.md files + MODELS-DEEP-REFERENCE.md bumped from 1.6.0 to 2.0.0.
- Root SKILL.md and dispatcher SKILL.md both at 2.0.0.

---

## v1.6.0 — 2026-03-26

### New: Kling 3.0 Model Family
- **Kling Video 3.0 (V3)**: 15s max duration, multi-shot generation (up to 6 camera cuts), native audio-visual co-generation with multilingual support (EN, ZH, JA, KO, ES + regional accents), Voice Binding, multi-character dialogue (3+ speakers), physics engine, 4K HDR output, professional export (16-bit HDR, EXR sequences), text rendering, Elements 3.0 tagging, sequential action syntax, motion endpoint pattern.
- **Kling Video 3.0 Omni (O3)**: Same quality as V3 plus Video Element referencing, Performance Cloning, Voice Extraction from static images, custom storyboard, multi-character coreference, video-to-video, natural language editing, 4K/60fps.
- **Kling 3.0 Motion Control**: Reference video → motion transfer (3–30s), Image/Video Orientation modes, Element Binding for face stability, camera sync, audio passthrough.
- **Kling Image 3.0**: Native 4K (up to 3840×2160), Image Series Mode, up to 10 reference images, Visual Chain-of-Thought, style transfer + portrait + character reference + multi-image blending, local re-editing, cinematic color grading.
- **Kling Image 3.0 Omni**: Same as Image 3.0 plus advanced editing with stronger prompt fidelity. Native 2K and 4K output.
- Added V3 vs O3 selection guidance, Audio Speaker Attribution Format, Multi-Shot Storyboard Format.
- Marked Kling 2.6 and O1 as legacy (still documented).
- Updated model comparison tables, decision flowcharts, and unique feature matrix across all model reference files.

### New: Cinema Studio 2.5
- Updated Cinema Studio from 2.0 to 2.5 across all files.
- **Soul Cast integration**: Character-and-location-first workflow with up to 3 AI actors per keyframe. 8 parameter categories (Genre, Budget, Era, Archetype, Identity, Physical Appearance, Details, Outfit). Auto-generated backstory + character sheet. Powered by Nano Banana 2.
- **Soul Cast vs Soul ID** distinction documented: Soul Cast = generate AI actors from parameters (no photos needed); Soul ID = upload 20+ photos to train identity consistency.
- **Built-in Color Grading Suite**: Color temperature, contrast, saturation, sharpness, film grain, exposure, bloom. Applied to keyframes before video generation.
- Extended workflow: pre-production (Soul Cast + location) → generation → post-production (color grade).

### New: Nano Banana 2 expanded documentation
- Expanded prompting-relevant capabilities: subject consistency (5 characters, 14 objects), precision text rendering + translation, advanced world knowledge, 512px to 4K, full aspect ratio list, infographic/diagram generation, reference image editing, style transfer.
- Added prompting patterns: structured JSON, short direct, style transfer, location+time, blueprint/schematic, infographic overlays, multi-panel comics, product ad recreation.
- Added NB2 vs NB Pro comparison note.

### New: Soul Cinema Preview (image model)
- Higgsfield proprietary cinematic-grade image model (launched March 4, 2026).
- Prompt-driven only (no preset panel). Excels at close-up shots. Works with Soul ID + Soul HEX.
- Key workflow: generate cinematic keyframe → feed into Kling 3.0 I2V.
- Documented Soul HEX color palette system.

### New: Expanded cinematic vocabulary (UPDATE 5)
- **Camera angles**: Low Angle, High Angle, Eye Level, Bird's-Eye View, Worm's-Eye View, Ground Level, Canted Angle Left/Right, Static Oblique, OTS, POV, Two-Shot, Cowboy Shot added to `higgsfield-camera`.
- **Shot sizes**: Full standard ladder (ELS through Insert Shot) added to `higgsfield-camera`.
- **Micro-expressions**: 19 nuanced facial performance directions (Core set + Extended set) added to `higgsfield-soul`.
- **Cinematic lighting techniques**: 13 named lighting techniques (Rembrandt, Butterfly, Split, Rim, Motivated, Practical, Chiaroscuro, High-key, Low-key, Golden hour, Blue hour, Harsh midday, Overcast diffused) added to `higgsfield-style`.
- **Key prompting principle**: "#1 mistake in video prompting" callout added to `higgsfield-prompt`.

### Updated: Platform model lineup
- Video: Kling 3.0, Kling O1, Kling 2.6, Kling 2.5 Turbo, Kling 3.0 Motion Control, Sora 2, Google Veo 3.1, Wan 2.5/2.6, Seedance Pro, Minimax Hailuo 02, Higgsfield DoP (Lite/Standard/Turbo).
- Image: Nano Banana Pro, Nano Banana 2, Soul 2.0, Soul Cinema Preview, Soul Cast, Flux 2, Flux Kontext, GPT Image 1.5, Seedream 4.0.
- Updated root SKILL.md, dispatcher, model-guide.md, and higgsfield-models sub-skill.

### Updated: Audio skill for Kling 3.0
- Multi-character dialogue (3+ speakers with correct attribution).
- Voice Binding and Voice Extraction (O3).
- Performance Cloning (O3).
- Audio Speaker Attribution Format template.

### All sub-skills version bumped to 1.6.0

---

## v1.5.2 — 2026-03-18

### Fixed: higgsfield_memory.py — Robustness
- Added `ValueError` handling around `int(sys.argv[3])` in `query-filter` and `query-quality` — passing a non-integer `top_n` argument now returns a clean JSON error instead of an unhandled crash.
- Made `export_summary()` atomic — writes to `.tmp` then renames, consistent with `save_db()`. Prevents partial/corrupted output on interrupted writes.

### Fixed: higgsfield-recall/SKILL.md — Broken command references
- Changed `python higgsfield_memory.py ...` → `python3` in all three code blocks. `python` is not in PATH on modern macOS/Linux.
- Replaced reference to non-existent `higgsfield-learn` skill with the correct `higgsfield-troubleshoot`.

### Fixed: validate.py — Typo
- Corrected "Highsfield" → "Higgsfield" in the validation report header.

## v1.5.1 — 2026-03-18

### Fixed: higgsfield_memory.py — Critical error handling
- Added try-except around `json.loads()` in `add_filter()` and `add_quality()` — malformed JSON no longer crashes the script; returns a structured error response instead.
- Made `save_db()` atomic — writes to a `.tmp` file then renames it, preventing database corruption if the process is interrupted mid-write.
- Added try-except to `load_db()` covering missing file and corrupted JSON cases.
- Added deterministic secondary sort key (`date_added`) to `query_filter()` and `query_quality()` — equal-scored results now return in consistent order.
- Improved tokenizer — hyphenated terms (e.g. `real-person`) now match as a whole phrase AND as individual component words, improving filter memory accuracy.
- Removed unused `import os`.

### Fixed: higgsfield_memory.py — New `health` command
- Added `python3 higgsfield_memory.py health` — runs a quick integrity check on both database files (validates JSON, verifies entry counts match `_total_entries`).

### Fixed: db/filter-memory.json — Schema completeness
- Added missing `substitution_worked` field (was `null`-defaulted in code but absent from all 4 seeded entries).

### Fixed: db/quality-memory.json — Field naming consistency
- Renamed `model` → `model_used` and `category` → `failure_type` in all 5 entries to match what `add_quality()` writes.
- Added missing `outcome` and `improvement_confirmed` fields to all 5 entries.

### Fixed: SKILL.md frontmatter — Invalid top-level attributes
- Moved `tags` from top-level into `metadata` block across all 20 SKILL.md files (`tags` is not a supported top-level skill attribute).
- Moved `references` from top-level into `metadata` block in `SKILL.md` and `higgsfield-models/SKILL.md`.

### Fixed: Broken relative paths
- Main dispatcher (`mnt/user-data/outputs/higgsfield/SKILL.md`): corrected bare filenames `vocab.md`, `model-guide.md`, `prompt-examples.md` to proper relative paths (`../../../../`).
- `higgsfield-models/SKILL.md`: corrected `image-models.md` reference to `../../../../../../image-models.md`.

### Fixed: README — Incorrect install command
- Changed `cp -r higgsfield_v140` to `git clone … && cp -r higgsfield_v150` with correct repo path.
- Corrected directory diagram label from `higgsfield_v150/` to `higgsfield/ (repo root)`.
- Corrected Cowork install instruction (was referencing a non-existent `higgsfield_v150/` subfolder).

### New: validate.py — Pre-release health checker
- Added `validate.py` at repo root: verifies all SKILL.md files have valid frontmatter, all relative path references resolve to real files, both JSON databases are valid and schema-complete, and all expected root files are present.
- Run with `python3 validate.py` before any release. Exits 0 on pass, 1 on failure with itemised report.

## v1.5.0 — 2026-03-13

### New: Cinema Studio 2.0 — 3D Mode (Gaussian Splatting)
- Documented the 3D exploration feature that builds a 3D Gaussian splat from any generated image.
- Virtual camera orbit around generated scenes — front, side, back, above.
- Creative workflow: generate image → enter 3D Mode → orbit to new angle → capture as new start frame → animate.
- Best practices for source images (single subjects, clear geometry, even lighting).

### New: Cinema Studio 2.0 — Grid Generation (Batch Variations)
- Documented 2×2 and 4×4 grid generation modes for producing multiple variations from a single prompt.
- 2×2 = 4 variations per credit; 4×4 = 16 variations per credit.
- Use cases: A/B testing compositions, character sheet creation, finding the best start frame.

### New: Cinema Studio 2.0 — Resolution Settings
- Documented explicit resolution control: 1K (fast drafts), 2K (default production), 4K (final delivery).
- Higher resolution = longer generation time, same credit cost.

### New: Cinema Studio 2.0 — Frame Extraction Loop
- Documented the iterative Build → Animate → Extract → Feed Back → Repeat workflow.
- Extract any frame from a generated video as a new start image for the next generation.
- Key technique for extending sequences beyond single-clip duration limits.

### New: Cinema Studio 2.0 — Object & Person Insertion
- Documented the ability to insert characters or objects not present in the original start frame.
- Describe the new element in the prompt; the model composites it into the scene.
- Best practices: match lighting, keep scale plausible, one insertion per generation.

### New: Cinema Studio 2.0 — 12-Second Total Runtime Cap
- Added critical warning to Multi-Shot Manual section: total runtime across all scenes is capped at 12 seconds.
- Duration allocation strategy: plan scene durations before building to avoid hitting the cap.

### New: Cinema Studio 2.0 — Per-Character Emotion Controls
- Documented per-character emotion settings in the Elements system: Joy, Fear, Surprise, Sadness.
- Applied per character per scene in Multi-Shot Manual mode.

### New: Cinema Studio 2.0 — Clustering (Automatic Generation Grouping)
- Documented the automatic grouping feature that clusters generations from the same prompt.
- Expand/collapse cluster groups for project organization.

### New: Soul ID — Character Sheet Creation
- Added Character Sheet workflow to the Soul ID skill.
- Multi-angle reference images (front, 3/4, side, full body) for improved consistency.
- How to create character sheets using Grid Generation and 3D Mode.
- Why multi-angle references improve Soul ID consistency across extreme angle changes.

### Updated: Cinema Studio comparison table
- Added rows for 3D exploration and batch generation to the Cinema Studio vs Standard comparison.

### Updated: All sub-skills version bumped to 1.5.0

---

## v1.4.0 — 2026-03-05

### Fixed: MODELS-DEEP-REFERENCE.md — Duplicate YAML key
- Removed duplicate `user-invokable: true` key from frontmatter (kept correct `user-invocable: true`).

### New: Cinematic Still Images section in prompt-examples.md
- Added 3 fully worked cinematic still image examples using the v1.3.9 Image Prompt Formula (`[Shot size] + [Angle] + [Movement keyword] of [character]. [Pose]. [Environment]. [Lighting]. [Style].`).
- **Example 8 — Sci-Fi Character Tension** (Nano Banana Pro, 16:9): MCU + Low Angle + Dolly Zoom. Cyber-enhanced operative in neon rain.
- **Example 9 — Epic Fantasy Scale** (Seedream 4.5, 16:9): EWS + Overhead + Crane Up. Lone warrior on a shattered bridge over a lava chasm.
- **Example 10 — Psychological Thriller Detail** (Nano Banana Pro, 3:4): ECU + Dutch Angle + Rack Focus. Lipstick-smeared mirror reflection in a dim bathroom.
- Covers a mix of models, aspect ratios, and genres.

### Fixed: higgsfield_memory.py — Directory fallback bug
- Replaced fragile `if not DB_DIR.exists(): DB_DIR = SCRIPT_DIR` fallback with `DB_DIR.mkdir(parents=True, exist_ok=True)`.
- Ensures the `db/` directory is always created rather than silently falling back to the script directory (which would misplace database files).

### Fixed: prompt-examples.md — Audio duration correction
- Example 5 (Audio-Driven Scene): changed duration from `10s` to `8s` to match Seedance 1.5 Pro's recommended lip-sync sweet spot (3–8s).

### New: Memory summary for cold-start resolution
- Generated `db/memory-summary.md` via `python3 higgsfield_memory.py export-summary`.
- Human-readable snapshot of all 4 filter memory entries and 5 quality memory entries.
- Added to project knowledge base for automatic context loading — eliminates cold-start gap where Claude previously had no recall of past generation failures.

---

## v1.3.9 — 2026-03-04

### New: higgsfield-image-shots sub-skill — Cinematic Image Prompting
- New dedicated sub-skill for **still image** prompt composition, separate from video camera controls.
- **10 Distance & Size shots** with AI prompt keywords and examples: Extreme Wide Shot (EWS), Wide Shot / Long Shot, Full Shot, Medium Long Shot (MLS), Cowboy Shot, Medium Shot (MS), Medium Close-Up (MCU), Close-Up (CU), Extreme Close-Up (ECU), Macro Shot.
- **10 Camera Angles** with emotional purpose and prompt patterns: Eye-Level, Low Angle, High Angle, Overhead / Bird's Eye, Worm's Eye, Dutch Angle / Canted Angle, Over-the-Shoulder (OTS), Point of View (POV), Selfie Angle, Ground Level.
- **17 Camera Movements for stills** across three tiers — Static/Basic (Static, Pan, Tilt, Zoom In/Out, Pedestal), Advanced Physical (Dolly In/Out, Truck, Orbit, Crane), Cinematic & AI (Dolly Zoom/Vertigo, Crash Zoom, FPV, Bullet Time, Handheld Follow, Camera Roll, Rack Focus, Pull Back Reveal, Fly-Through).
- Every entry includes: AI Prompt Keyword, definition, primary purpose/effect, and a ready-to-paste prompt example using the `[img 1]` reference pattern.
- **Quick reference tables** for Distance & Size and Angles for fast lookup.
- **Combination formula** — how to layer shot size + angle + movement keyword into a single image prompt with 4 worked examples.
- **Image Prompt Formula** — structured pattern: `[Shot size] + [Angle] + [Movement keyword] of [character]. [Pose]. [Environment]. [Lighting]. [Style].`

### Updated: Dispatcher SKILL.md
- Added `higgsfield-image-shots` to routing table and sub-skills index.
- Clarified `higgsfield-camera` label as video-specific to distinguish from the new image shots skill.
- Version bumped to 1.3.9.

### Updated: README.md
- Added `higgsfield-image-shots/SKILL.md` to the directory structure listing.

---

## v1.3.8 — 2026-03-04

### New: Cinema Studio 2.0 — Prompt Character Limit (512 chars)
- Documented the **hard 512-character limit** on Cinema Studio prompt fields.
- @ Element chips consume ~80–100 hidden characters each for internal metadata.
- Added character budget guidelines: ~250 visible chars with 2 tags, ~350 with 1, ~450 with 0.

### New: @ Element Persistence Rule
- Discovered that @ Elements added in **Scene 1 persist across all scenes** in Multi-Shot Manual.
- No need to re-add @ tags in Scenes 2–6. Characters carry through via Reference Anchor.
- Recommended pattern: @ Elements in Scene 1, visual descriptions in subsequent scenes.

### New: Fight Scene Rules (Tested)
- Documented what Cinema Studio CAN and CANNOT render in two-character fight sequences.
- CAN: facing each other, general fighting energy, pinned against wall, falling, walking away.
- CANNOT: specific punch contact, kicks, martial arts, cause-and-effect choreography, prop weapons, grappling.
- Documented **character swap problem**: two @ tags in action scenes causes the AI to confuse hero/villain roles.
- Added fight sequence template alternating @ Element scenes (character) with plain text scenes (action).

### New: Prompting Best Practices (from Higgsfield official)
- Added **pre-prompt checklist**: Who, Where, What's happening, Camera, Mood/Genre.
- Added **one action per scene rule** with breakdown strategy.
- Added **fast motion trick**: generate in Slow Mo, speed up in post.

### Updated: Common Prompt Mistakes table
- Added 4 new entries: over 512 chars, impact before action, specific martial arts, multiple @ tags in action.

## v1.3.7 — 2026-02-28

### Architecture: De-duplication pass
- **Root SKILL.md** stripped from 146 to 42 lines — removed full model tables and quick reference that duplicated `model-guide.md`. Now a lean index with cross-references only.
- **Dispatcher SKILL.md** stripped from 219 to ~170 lines — removed duplicated MCSLA definition (lives in `higgsfield-prompt`), model selection table (lives in `higgsfield-models`), and platform quick reference. Keeps only workflow, routing table, output format.
- Net token savings: ~300 lines of duplicated content removed from default context window load.

### New: Fast Path for simple requests
- Dispatcher now distinguishes between **fast path** (clear creative intent, no constraints → generate immediately with sensible defaults) and **full path** (production-grade → confirm parameters first).
- Defaults: 16:9, 8s, Cinematic, Kling 3.0 (character) or Sora 2 (action), Soul 2.0 (portrait) or Nano Banana Pro (other images).

### Fixed: Recall system paths
- `higgsfield_memory.py` path changed from `SCRIPT_DIR.parent / "db"` to `SCRIPT_DIR / "db"` with fallback to same-directory. Matches actual directory layout.
- Created `db/` directory and moved `filter-memory.json` into it.
- Created `quality-memory.json` (was missing entirely).
- Updated all `higgsfield-recall/SKILL.md` bash commands from `scripts/higgsfield_memory.py` to `higgsfield_memory.py`.

### New: Seeded memory databases
- `filter-memory.json` seeded with 4 entries: real-person blocks, brand/IP blocks, violence filter, Seedance 2.0 face upload restriction.
- `quality-memory.json` seeded with 5 entries: character drift (Sora 2), VHS style ignored (Kling 2.6), I2V static output, camera conflict, lip-sync desync (Seedance 1.5 Pro).

### Slimmed: higgsfield-models
- Split into compact `SKILL.md` (~200 lines, handles 90% of model selection) and `MODELS-DEEP-REFERENCE.md` (full 1021-line per-model documentation, loaded on-demand).
- SKILL.md contains: comparison table, decision flowchart, image quick selection, budget tiers, unique feature matrix, key model notes.

### New: higgsfield-audio sub-skill
- Full audio prompting guide covering all audio-capable models (Kling 3.0, Seedance 1.5 Pro/2.0, Veo 3/3.1, Grok Imagine Video).
- Four audio layers: Dialogue, SFX, Ambient, BGM — with prompt structure and best practices.
- Lip-sync rules: timing, framing, token conflicts, multi-character workaround.
- Per-model audio notes and common failure/fix table.

### New: Before → After prompt examples
- 5 transformation examples added to `prompt-examples.md` showing weak → strong prompt improvement.
- Covers: vague→specific, over-described I2V, slop words, camera conflicts, missing audio direction.

### Consistency pass
- All sub-skills bumped to version 1.3.7.
- `higgsfield-troubleshoot` updated: character consistency recommendation changed from "Kling 2.6" to "Kling 3.0 (or 2.6 if no audio needed)". VFX recommendation updated. Audio troubleshooting sections added.
- Removed duplicate `user-invokable: true` typo key from all frontmatter blocks.
- Dispatcher routing table updated with `higgsfield-audio` entry.

---

## v1.3.6 — 2026-02-28

### higgsfield-models/SKILL.md — Grok Imagine family added (was completely absent)

Grok Imagine (`grok-imagine-image` and `grok-imagine-video`) had zero entries anywhere in the library despite being live on the platform. Both models documented from scratch using the official xAI API docs (docs.x.ai/developers/model-capabilities/images/generation and video/generation).

**Architecture context documented:**
Aurora is an autoregressive mixture-of-experts network — architecturally distinct from diffusion models. Predicts next token from interleaved text+image data. This gives it tighter compositional control, stronger multi-element scene understanding, and reliable text/logo rendering where diffusion models fail.

**`grok-imagine-image` — new complete entry:**
- Text-to-image with full aspect ratio table (10 ratios including `auto`, `19.5:9`, `20:9`)
- Resolution: 1k / 2k
- Image editing (single image): source image + prompt, output follows input ratio. Critical note: OpenAI SDK `images.edit()` uses `multipart/form-data` which is NOT supported — must use xAI SDK or `application/json` directly
- Multi-image editing (up to 3 source images): ordered input, cross-image compositing, aspect ratio override
- Multi-turn iterative editing chain: use each output URL as next input — primary recommended workflow for complex compositions
- Style transfer: photorealistic → anime → oil painting → pencil sketch → watercolor → pop art
- Batch generation: up to 10 images per request via `n` parameter
- Aurora differentiators table: text/logo rendering, multi-person scenes, precise prompt adherence, photorealism, iterative chains, batch A/B testing
- Content moderation: `response.respect_moderation` flag documented

**`grok-imagine-video` — new complete entry:**
- Duration: 1–15s (generation); editing preserves source duration (not user-configurable)
- Resolution: 720p (cap for both generation and editing; 1080p input downsized)
- Audio: ✅ native — dialogue, SFX, ambient, music
- Generation modes: T2V, I2V, video editing/restyling
- Async workflow: `request_id` → poll until `status: "done"` → download from temporary URL
- Video editing constraints: input must be publicly accessible URL; output capped at 720p; duration not configurable
- Imagine 1.0 (Feb 1, 2026): duration extended to 10s, improved audio quality, video editing (add/remove objects, restyle, motion control)
- Grok Imagine internal decision table (8 rows, image vs video routing)

**model-guide.md:**
- Grok Imagine Video added to video table
- Grok Imagine Video added to decision flowchart

**image-models.md:**
- Grok Imagine Image added to pricing/capability table

**Quick Decision Table (higgsfield-models SKILL.md):**
- 7 new Grok Imagine rows added (5 image, 2 video)

---

## v1.3.5 — 2026-02-28


### higgsfield-models/SKILL.md — Google Veo family complete rewrite

The library had one thin "Veo 3 (Google)" entry (6 lines). The UI shows 4 Veo models on platform. Google's official API docs (ai.google.dev/gemini-api/docs/video) confirm Veo 3.1 has significant exclusive capabilities missing from all previous documentation.

**New entries: Veo 3.1, Veo 3.1 Fast, Veo 3 Fast** (in addition to expanded Veo 3)

**Veo 3.1 — new capabilities documented (3.1-exclusive features):**
- Reference images (up to 3): `reference_type: "asset"` — preserves subject appearance (character face, outfit, prop) consistently throughout video. Veo 3.1 and 3.1 Fast only, not available in Veo 3/3 Fast.
- First + last frame interpolation: specify opening and closing frame images; model generates the motion between them. Duration must be 8s when using this feature.
- Video extension: extend any Veo-generated video by 7s, up to 20 times (max 148s total). Input must be 720p. Videos stored 2 days (timer resets on each reference). Voice extension requires audio in last 1s of source.
- 4K output: 8s only, higher latency/cost. 1080p also 8s only. 720p supports all durations (4/6/8s).
- Portrait mode (9:16): available across all Veo 3/3.1 models.

**Duration constraints documented:**
- Reference images / first+last frame / 1080p / 4K → duration must be 8s
- Extension → input must be 720p; output combines original + extension up to 148s

**Audio generation guidance added:**
- Dialogue: use quotes for specific speech
- SFX: describe sounds explicitly (tires screeching, not just "loud sounds")
- Ambient: describe environment soundscape
- Negative prompts: supported (describe what you don't want, no "no X" language)

**Full Veo prompt element framework documented:**
Subject / Action / Style / Camera / Composition / Focus+Lens / Ambiance / Audio

**Veo 3.1 vs Veo 3 comparison table** — 8 capabilities across all 4 models (audio, reference images, first/last frame, extension, 4K, portrait, negative prompts, stable/preview status)

**Veo 3.1 Fast, Veo 3 Fast** — new entries clarifying speed/quality/cost tradeoffs and use cases

**Quick Decision Table** — Veo row expanded from 1 to 5 rows

### model-guide.md
- Video table: Veo row expanded from 1 to 4, audio column corrected to ✅ for all Veo 3/3.1 (was incorrectly ❌), durations added
- Decision flowchart: Veo branch expanded to 5 decision points

---

## v1.3.4 — 2026-02-28


### higgsfield-models/SKILL.md — Seedance 2.0 full production documentation

Seedance 2.0 has not yet shipped on Higgsfield but is incoming. This version replaces the thin v1.3.3 stub with a complete, production-ready reference document built from two third-party Seedance 2.0 skill libraries (Emily/@iamemily2050's seedance-2.0 v3.8.0 and seedance-bot-1), both containing validated practitioner knowledge from 10,000+ generation testing on the Jimeng/Dreamina platform.

**New sections added to the Seedance 2.0 entry:**

- **Rule of 12** — Full asset budget table with the critical correction that video clips share a 15s combined limit (not 15s per clip). Audio 15s combined limit also documented.
- **Generation Modes (T2V / I2V / V2V / R2V)** — All four modes documented with the critical V2V distinction: reference technique vs. direct edit trigger different model pathways
- **Five-Layer Prompt Stack** — Subject/Action/Camera/Style/Sound architecture with Delegation Levels 1–4, word count ranges, decision rule, and complete examples at each level including Level 4 fight choreography
- **6-Part Field Formula** — `[SHOT TYPE] + [SUBJECT] + [ACTION] + [STYLE] + [CAMERA MOVEMENT] + [AUDIO CUES]`, cross-validated on 10,000+ generations
- **Anti-Slop / Prompt Hygiene** — Instant-delete word list and measurable replacement table; the one test: "can a camera, light meter, or stopwatch measure this word?"
- **Camera Control** — Full camera contract (framing/move/speed/angle), reliable phrasing library, anti-drift rules, One-Take technique (一镜到底) with image waypoints, Nine-Grid storyboard method (九宫格)
- **Audio Rules and Failure Modes** — Platform hard limits (MP3 only — WAV/AAC fail silently), sweet spot 3–8s, timestamp anchoring phrase for audio rewrite bug, multi-character compositing workaround, critical Jimeng platform distinction (Seedance 2.0 video generation vs. OmniHuman-1 Digital Human tool — Master/Quick/Standard modes do NOT exist in Seedance 2.0)
- **Character Identity** — Character card format, identity anchoring syntax, multi-character @Tag patterns, 360° consistency test, hand safety rules
- **Beat Density** — Max changes per duration table, Level 4 fight density guidance
- **Genre Templates** — 5 ready-to-use starters: product ad, fight scene, short drama dialogue, music beat sync, architecture walkthrough
- **Compliance / Copyright** — 6-gate pre-generation checklist, substitution table (Iron Man → descriptor, Spider-Man → descriptor, Eiffel Tower → descriptor, Bohemian Rhapsody → descriptor)
- **Emergency Fixes** — 8-row quick-fix table for all common failure modes
- **Platform Parameters** — Confirmed aspect ratios (16:9 · 9:16 · 4:3 · 3:4 · 21:9 · 1:1), resolution tiers, duration range
- **Feb 2026 status note** — Real person face uploads blocked, API delayed, Higgsfield integration incoming

**Quick Decision Table** — Seedance 2.0 expanded from 1 row to 3 rows (R2V / V2V / complex motion routing)

**Key accuracy corrections from practitioner data (vs. earlier documentation):**
- Video clip limit is 15s COMBINED total, not 15s per clip
- Negative prompts (--no syntax) are NOT supported — positive constraints only
- Lip-sync sweet spot is 3–8s, not the 15s technical maximum
- Master/Quick/Standard modes belong to OmniHuman-1 Digital Human, NOT Seedance 2.0
- API is delayed (was planned Feb 24) due to copyright enforcement actions

---

## v1.3.3 — 2026-02-28


### higgsfield-models/SKILL.md — Seedance Family Complete Rewrite

The library previously had a single thin "Seedance Pro" entry. Three properly documented tiers now replace it:

**Seedance 2.0** — new entry (most advanced tier, was completely missing):
- Architecture: unified multimodal audio-video joint generation (text + image + audio + video inputs)
- 12 simultaneous asset inputs: 9 images + 3 video clips (15s each) + 3 audio files + text
- Model auto-interprets each asset's role; use natural language to specify references
- Motion realism: industry-leading complex multi-person interaction (synchronized sports, fight choreography)
- Acoustic physics: audio calculated from visual environment geometry (not just layered on)
- Frame-level precision: control fonts, transitions, screen rhythm per frame
- Video extension + scene merging with maintained continuity
- ~30% faster generation than comparable 2K models
- Use case: reference choreography video + character images + audio clip → synchronized scene

**Seedance 1.5 Pro** — new entry (was missing — different model from Pro):
- Architecture: dual-branch Diffusion Transformer, simultaneous audio-video single-pass generation
- Multilingual lip-sync: English, Chinese (Sichuanese, Cantonese, Taiwanese Mandarin, Shanghainese), Japanese, Korean, Spanish, Indonesian
- Multi-character dialogue with correct lip-motion assignment per character
- Audio types: speech, singing, non-verbal vocalizations, SFX, BGM — all native
- Beats Kling 2.6 and Veo 3.1 on audio-visual synchronization (SeedVideoBench 1.5)
- Cinematic camera: dolly zoom (Hitchcock zoom), long takes, orbital/arc/tracking shots
- Strong in stylized content: comedy timing, theatrical/opera performance, short dramas
- Architecture note: simultaneous generation (not post-production layering) is the key distinction vs competitors

**Seedance Pro** — existing entry expanded:
- Clarified as fast iteration tier, NO native audio
- Pro (1080p) vs Lite (720p) distinction documented
- Correct positioning: use when audio not required; iterate before committing to 1.5 Pro/2.0

**Quick Decision Table** — Seedance row expanded from 1 to 3 rows

### model-guide.md
- Video table: Seedance row expanded from 1 to 3 with audio column correctly marked
- Decision flowchart: Seedance branch updated with audio/no-audio split and Seedance 2.0 option

---

## v1.3.2 — 2026-02-28


### higgsfield-models/SKILL.md — Kling Family Complete Rewrite

**Kling 3.0** — fully documented (was a thin stub): duration 3–15s, native multilingual audio (6 languages + accents), AI Director multi-shot mode, physics-aware engine, stylized output (anime/Pixar/claymation), EXCLUSIVE badge.

**Kling 3.0 Omni** — new entry: Performance Cloning (clone character appearance + voice from 3–8s video), Voice Extraction (static image + audio = voice profile), custom per-shot storyboard, Elements 3.0 (video-clip-based identity locking).

**Kling 3.0 Omni Edit** — new entry: reference-guided video transformation at 3.0 quality tier.

**Kling O1 Video** — new dedicated entry: Chain-of-Thought (CoT) reasoning pre-render, up to 7 simultaneous reference inputs, start/end frame mode, motion transfer from reference video.

**Kling O1 Video Edit (Edit Video tab)** — new entry (entire tab was undocumented):
- Relight & Atmosphere: 3D geometry-aware lighting transformation (featured UI capability)
- Full edit type catalog: Restyle, Object swap, Add elements, Delete/remove, Scene transformation, Angle change, Character replacement
- The Keep Rule prompt formula: `Change [Target] to [New State], keep [everything else] unchanged`
- 5 example edit prompts. Auto settings toggle. Input: 3–10s video + up to 4 image refs, output: 720p.

**Kling Motion Control** — new entry: up to 30s duration (longest in lineup), camera path control.

**Kling 2.5 Turbo, 2.1, 2.1 Master** — new entries: fast iteration tier and legacy tier context.

**Quick Decision Table** — expanded from 10 to 20 rows covering full Kling family + edit mode.

### model-guide.md — Full Rewrite
- Video table: 8 → 15 models, added Duration and Audio columns
- Image table: updated Seedream entries with correct capability notes
- Decision flowchart: added Edit Video branch, full Kling sub-tree, Seedream image sub-tree
- New section: Kling Generation vs Edit Mode with two-tab distinction and edit prompt formula
- Camera/preset compatibility tables updated with Kling 3.0 and Motion Control

---

## v1.3.1 — 2026-02-28

### image-models.md — Seedream Family Expansion

**Seedream 5.0 Lite** — full capability documentation: online search/real-time data grounding, deep reasoning for long complex prompts (1,000+ chars), native multi-image output, complex layout generation. Prompt tips for each.

**Seedream 4.5** — full capability documentation: enhanced reference consistency (face/lighting/identity), accurate multi-image editing (stable with 10+ refs), dense text/typographic rendering, specific editing capabilities (selective deletion, material swap, in-image translation, font/color edits).

**Seedream family** — architecture context note added (DiT + high-compression VAE, bilingual training, RLHF pipeline).

### higgsfield-models/SKILL.md — Seedream Section Expansion
- Added Seedream 5.0 Lite entry. Expanded Seedream 4.5 entry. Quick decision table: 2 new rows.

---

## v1.3.0 — 2026-02-28


### higgsfield-cinema — Complete Rewrite

Major corrections and additions based on actual Cinema Studio 2.0 UI review:

**Elements system (new — was completely missing):**
Characters, Locations, Props — create once, call via `@` in any prompt.
Full creation workflow. Multi-element prompt examples. `@` + Soul ID combination rules.

**Image Mode cameras — corrected (all previous names were wrong):**
Correct camera bodies: Premium Large Format Digital, Classic 16mm Film, Modular 8K Digital,
Full-Frame Cine Digital, Studio Digital S35, Grand Format 70mm Film.
Correct lenses: Creative Tilt Lens, Compact Anamorphic, Halation Diffusion, Extreme Macro,
70s Cinema Prime, Warm Cinema Prime, Swirl Bokeh Portrait, Vintage Prime,
Classic Anamorphic, Clinical Sharp Prime.
Focal lengths corrected: 8mm, 14mm, 35mm, 50mm.
Aperture options: f/1.4, f/4, f/11.

**Genre list — corrected:**
Previous (wrong): Action/Horror/Comedy/Suspense/Drama/Romance.
Correct: General/Action/Horror/Comedy/Western/Suspense/Intimate/Spectacle.

**Director Panel — all 18 camera movements documented:**
Static, Handheld, Zoom Out, Zoom In, Camera Follows, Pan Left, Pan Right,
Tilt Up, Tilt Down, Orbit Around, Dolly In, Dolly Out, Jib Up, Jib Down,
Drone Shot, Dolly Left, Dolly Right, 360 Roll (+ Auto).

**Speed Ramp — new (was missing):**
Linear, Slow Mo, Speed Up, Impact, Auto, Custom. Custom curve via blue line nodes.

**Shot modes — fully documented:**
Single Shot, Multi-Shot Auto, Multi-Shot Manual (6 scenes, full per-scene config).
Cost transparency: Multi-Shot Manual × 4 variations = 24 generations.

---

## v1.2.0 — 2026-02-28

### New Sub-Skills

**higgsfield-vibe-motion** — Complete Vibe Motion guide
- Core concept: Vibe Motion generates Remotion code, not pixel sequences — deterministic,
  not predictive. Text is always crisp. Edits are non-destructive.
- Powered by Claude (Anthropic) + Remotion open-source framework
- Full chat-based workflow: describe → upload assets → apply template → refine
- Color palette presets (Mosaic, Prism, Candy, Minimal, Dark, Brand)
- Animation Speed / Physics slider documentation
- Real-time editing controls (Font Family, Text Color, Font Size, Background, Speed)
- Template categories: Text Animation, Infographics, Posters, Brand, Social, Product
- Prompting patterns for: typography, logo animation, infographics/stats, social motion
  graphics, product feature animation — all with fill-in-the-blank examples
- Vibe Motion vs other Higgsfield tools decision guide
- Combining Vibe Motion with video generation: 3 practical patterns (titles + cinematic,
  product ad intro/outro, full social ad chain)
- Technical notes: 4K output, Remotion code export, data-driven animation capabilities

**higgsfield-pipeline** — End-to-end production chain skill
- Master production chain documented: Popcorn → Seedream → Animate → Recast →
  Lipsync → Vibe Motion → Upscale → Assembly (all 8 stages)
- Pipeline A: Cinematic Short Film (full chain, character-consistent narrative)
  - Stage-by-stage prompting templates with full example short film sequence
  - Model selection matrix by scene type
  - I2V animation prompt structure for multi-scene consistency
- Pipeline B: Social Content Series (Soul ID + Moodboard locked, batch generation)
  - Per-post prompt template
  - Example 3-post series with consistent character and style
- Pipeline C: Product Campaign (hero video + variants + social cuts)
  - Product hero prompt structure
  - App integration (Click to Ad, Packshot, Giant Product)
- Pipeline D: Fast Iteration / Speed Run (5 creative directions in under an hour)
- Pipeline decision guide (which pipeline for which goal)
- 5 named pipeline pitfalls with specific fixes

### Root SKILL.md Updates
- Version bumped to 1.2.0
- Routing table: 8 new rows for `higgsfield-vibe-motion` and `higgsfield-pipeline`
- Sub-skills index: 2 new entries

---

## v1.1.0 — 2026-02-28


### New Sub-Skills

**higgsfield-cinema** — Cinema Studio 2.0 complete workflow
- Full 8-step production workflow (Script → Reference → Optical Stack → Hero Frame →
  Camera Config → Start/End Frames → Generate → Export)
- Optical physics engine documentation: camera bodies (ARRI ALEXA, Panavision, Sony VENICE,
  RED, 16mm, Super 8), lens types (16mm–135mm + Anamorphic), aperture/depth of field
- Reference Anchor system — how to lock character geometry across shots
- Manual Multi-Shot mode — 12-second sequences broken into up to 6 segments
- Cinema Studio vs standard generation decision guide
- Higgsfield Popcorn (storyboard tool) integration and workflow
- Cinema Studio prompting format (adds optical stack + Reference Anchor)
- Genre selection (Action, Horror, Comedy, Suspense, Drama, Romance)
- Keyframe Interpolation — Start/End Frame for morph-free transitions
- Model selection matrix for Cinema Studio specifically

**higgsfield-moodboard** — Style definition and visual consistency
- Soul Moodboard workflow (collect → upload → synthesize → export as modifier)
- Soul Hex color transfer — extract palette from any reference image
- Project-level style modifier template
- Moodboard + Soul ID integration for complete character + aesthetic consistency
- AI Influencer campaign moodboard workflow
- When to use moodboard vs inline style descriptions

**higgsfield-mixed-media** — Complete preset library
- Full 50+ Mixed Media preset catalogue organized by category
  (Textural, Light & Atmosphere, Geometric & Digital, Organic & Elemental,
  Vintage & Film, Social / Trend, Surreal / Dark)
- Each preset: name, visual look, best use cases
- Layer Mixed Media feature — stacking presets
- Effective preset combination table
- Mixed Media vs Visual Styles decision guide
- Social content series strategy using presets

**higgsfield-assist** — GPT-5 copilot + credit optimization
- Higgsfield Assist feature (GPT-5 powered, at higgsfield.ai/chat)
- What Assist can do + how to use it
- Claude skill vs Assist — when to use each
- Coming features in Assist
- Complete credit optimization guide:
  - Plan comparison table with credit counts and costs
  - Credit cost tiers by model
  - 5 most common credit waste patterns + fixes
  - Hero Frame Efficiency Method (the single highest-leverage technique)
  - Model selection by budget scenario (tight/mid/high)
  - Platform efficiency tips (presets, community gallery, batching, etc.)
  - 4-week platform learning path

### Additions to Existing Skills

- `higgsfield-models` — Added Kling O1, Veo 3.1, Seedance 2.0 to video model list
- `higgsfield-apps` — Added Nano Strike, Nano Theft, Vibe Motion, UGC Factory,
  Draw to Video, Photodump Studio
- `SKILL.md` — Updated routing table to include new v1.1 sub-skills
- `references/model-guide.md` — Updated decision flowchart with Wan 2.6, Kling 3.0

### Known Gaps (v1.2 targets)
- Vibe Motion workflow (chat-based video generation)
- UGC Factory deep-dive workflow
- Contest / challenge strategy prompts
- Draw to Video and Sketch to Video workflows
- Kling O1 (reasoning-based video) specific prompting
- Multi-reference image generation workflow
- Upscale / Topaz post-processing workflow
- Community strategy and sharing best practices

---

## v1.0.0 — 2026-02-28

### Initial Release

**Core files:**
- `SKILL.md` — Root entry point with MCSLA formula and full workflow
- `README.md` — Installation and usage guide

**Sub-skills:**
- `higgsfield-prompt` — MCSLA formula, T2V vs I2V, narrative structure
- `higgsfield-models` — All video + image models with decision flowchart
- `higgsfield-camera` — Complete camera control library (40+ controls)
- `higgsfield-motion` — 100+ named motion presets organized by category
- `higgsfield-style` — Five named styles + color grades + lighting vocabulary
- `higgsfield-soul` — Soul ID character consistency + AI Influencer workflow
- `higgsfield-apps` — 80+ one-click Apps organized by use case
- `higgsfield-recipes` — 9 genre templates
- `higgsfield-troubleshoot` — 10 failure patterns + pre-generation checklist

**References:**
- `vocab.md` — Full vocabulary for camera, shot size, style, lighting, atmosphere
- `model-guide.md` — Head-to-head comparison tables + decision flowchart
- `prompt-examples.md` — 18 original example prompts
