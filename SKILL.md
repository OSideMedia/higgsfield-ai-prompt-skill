---
name: higgsfield
description: >
  Use this skill whenever the user asks anything about Higgsfield AI — writing or
  refining video/image prompts, choosing a model (Kling, Sora 2, Veo, Wan, Seedance,
  Minimax Hailuo, DoP, Soul, Nano Banana, Seedream, Flux, GPT Image, etc.), camera
  controls, named motion presets, Soul ID character consistency, Cinema Studio 2.5/3.0,
  Vibe Motion, troubleshooting failed generations, credit optimization, Photodump,
  or any mention of higgsfield.ai. Also trigger on generic "write me a video prompt"
  or "make me an AI video prompt" requests when Higgsfield is the user's configured
  platform.
user-invocable: true
metadata:
  tags: [higgsfield, video, image, prompt, cinematic, AI, filmmaking, motion, camera]
  version: 3.32.0
  updated: 2026-08-21
  author: O-Side Media
  license: MIT
---

# Higgsfield AI Prompt Skill

**Language rule:** Reply in whatever language the user writes in.

---

## HARD RULES — pre-delivery checklist

These rules apply to every Higgsfield response. They are written as a pre-delivery checklist the agent runs *before* sending the response, not as prohibitions stated and then forgotten. The failure mode they prevent is **plausibility-over-verification** — producing a response that looks correct because the agent's training data knows the rough shape of Higgsfield work, rather than because the agent actually read the skill files and verified the platform's ground truth.

**Before delivering any Higgsfield response, confirm in this order:**

1. **Routing line present.** First line of response names which sub-skills you routed to (e.g. "Routing to higgsfield-prompt + higgsfield-camera for an Atmosphere push-in"). One line, then the work. Missing routing line = response is incomplete; add it.

2. **Routed sub-skills opened and read in this conversation.** Match the user's ask to the routing table below, open the matching sub-skill files with the read tool, and READ them. Root `SKILL.md` and `skills/higgsfield-prompt/SKILL.md` are mandatory at minimum on any prompt request. Grepped snippets do not satisfy this rule. Full reads do. If your only access to root `SKILL.md` or `skills/higgsfield-prompt/SKILL.md` in this conversation came from grep results, you have not satisfied this rule — open the file. Platform vocabulary, preset names, and model parameters must come from the files because this platform's lineup changes between releases.

3. **Named vocabulary verified, not invented.** Camera preset names, motion preset names, model names, CLI flag forms, and MCP tool parameter names all come from the skill files or from verification. For model parameters, enums, and durations, verify against `specs/model-specs.yaml` first — it is generated from a dated `models_explore` snapshot (see `snapshot_date` inside the file); if the snapshot is stale (>30 days), verify live instead (`higgsfield model get <model>` for CLI param schemas; `models_explore` for MCP). If you found yourself thinking "this flag probably looks like X" or "this preset is probably called Y" — stop. Read the file or run the verification command. Plausibility is not validity. Do not substitute generic video-prompt vocabulary for named Higgsfield presets; do not invent model versions, camera presets, or motion-preset names. If the user names one you don't see in the skill files, say so and ask for clarification.

4. **MCSLA structure intact on video prompts.** Model · Camera · Subject · Look · Action. Five layers, every video prompt, unless the user explicitly opted out.

5. **Shared negative constraints appended.** Pull positive-phrasing prevention phrases from `skills/shared/negative-constraints.md`. Do not paraphrase from training; use the exact phrasing from the file. (Kling 3.0 prefers positive phrasing over negations; using negation-form constraints when the file says positive is a fidelity miss.)

6. **Preflight surfaced when applicable.** If execution intent is signaled (CLI / MCP / bundled-skills mentioned) AND a video-class or high-cost model is named OR a budget concern is named, surface the two-step preflight (`model get` / `models_explore` for schema, then cost estimate). See `skills/higgsfield-stack/SKILL.md` § Preflight discipline.

7. **Aspect ratio is an enum, not a free-form value.** Check the model's allowed ratios against `specs/model-specs.yaml` before writing them into the header; if the snapshot is stale (>30 days), verify live via schema (`models_explore` / `model get`). Example of why this matters: Seedance 2.0 supports native 21:9, Kling 3.0 does not. Anamorphic / 2.35:1 / 2.39:1 are *style register* vocabulary for the Look line, not output ratios. See `vocab.md` § Aspect Ratio: output spec vs. style register.

8. **Prompt under 200 words — short-form regime only.** Soft cap from MCSLA section. Going over is a signal you're padding rather than locking — tighten. **Regime exception:** block-scaffold production prompts (`skills/higgsfield-seedance/SKILL.md` § Official Prompt Architecture) replace the word cap with structural lint — harvested production Seedance briefs run 218–2,059-word medians depending on register `[FIELD — 13-project community harvest, 2026-07-18]`. The cap governs single-shot MCSLA prompts; a block-scaffold prompt over 200 words is not a rule-8 violation.

**If any of items 1–8 are missing or unverified, the response is incomplete. Complete them before sending, not after.**

---

## What Is Higgsfield?

Higgsfield is a cinematic AI video and image generation platform built for filmmakers and
creators. Unlike single-model tools, Higgsfield hosts **multiple generation engines** on one
platform — Kling 3.0/3.0 Omni/3.0 Motion Control, Sora 2 incl. Pro/Max/Pro Max tiers (UI-only — confirmed in the UI 2026-07-06, absent from the API/MCP catalog), Google Veo 3.1/3.1 Lite, Wan 2.7/2.6/2.5,
Seedance 2.5/2.0/Pro, FLUX 3 Video, Minimax Hailuo 2.3/02, Higgsfield DoP (Lite/Standard/Turbo) for video; Soul 2.0, Soul Cinema Preview,
Soul Cast, Nano Banana Pro/2, Kling Image 3.0/Omni, Seedream 4.0, GPT Image 2.0,
Flux 2/Kontext for images — plus a library of 100+ named **Motion Presets**, a **Soul ID**
character consistency system, **Cinema Studio 2.5**, **Cinema Studio 3.0** (Business/Team plan), and **Cinema Studio 3.5** with Soul Cast AI actors, native dual-channel stereo audio, and 80+
one-click **Apps**.

---

## Working Folders — file handling

The project has a `workspace/` folder with three subfolders. Use them for every
task that involves a user-provided document or a file you produce. This keeps
uploads and deliverables out of the project root.

| Folder | Role | Your behavior |
|--------|------|---------------|
| `workspace/input/` | Documents the user wants you to read (scripts, story bibles, briefs, character sheets, references). | Read from here first. If the user uploaded a file that landed elsewhere in the project root, **move it into `workspace/input/` before working with it**. When you need a document from the user, ask them to drop it in `workspace/input/`. |
| `workspace/output/` | Files you generate for the user (prompt packs, shot breakdowns, batch CSVs, reports, exported docs). | **Write every file deliverable here**, not to the project root. Tell the user the path when you finish. |
| `workspace/processed/` | Inputs you have finished consuming. | When a task is complete, **move the source from `input/` to `processed/`** so `input/` stays clean. Never delete the user's files — relocate them. |

Rules:
- Never scatter user uploads or generated files across the project root or skill folders — route them through `workspace/`.
- Treat `workspace/input/` as the canonical place to look when the user says "the script / bible / reference I gave you."
- These three folders' contents are local-only (git-ignored); do not assume anything in them is committed.

### Fast Path — Simple Creative Requests

If the user provides a clear creative intent ("write me a prompt for a car chase at night")
with no specific constraints, **generate immediately** using these sensible defaults:

> **Fast Path still requires reading `skills/higgsfield-prompt/SKILL.md` first — Fast Path means skip clarifying questions, NOT skip the file read.**

| Parameter | Default |
|-----------|---------|
| Aspect ratio | 16:9 |
| Duration | 8s (Kling lanes — see Seedance exception below) |
| Style | Cinematic |
| Video model | Kling 3.0 (character-focused) or Seedance 2.0 (action/scale/references) |
| Image model | Soul 2.0 (portrait) or Nano Banana 2 (everything else) |

Do not ask clarifying questions. Deliver a ready-to-paste prompt. Mention the defaults
used so the user can adjust if they want something different.

> **Seedance exception:** Seedance 2.0 never gets a silently defaulted runtime
> (`skills/higgsfield-seedance/SKILL.md` — always ask, never default). On Fast
> Path that means: if the user named no duration, route video to Kling 3.0;
> pick Seedance 2.0 only when the request names a duration — or when the user
> asked for Seedance by name, in which case state the assumed runtime as the
> first adjustable default in the delivery.

> If you did not read `skills/higgsfield-prompt/SKILL.md` earlier in this conversation, read it now before writing the prompt.

### Full Path — Production Requests

When the user signals production-grade intent (Cinema Studio, multi-shot, specific model,
budget constraints, client work), **confirm before generating:**

**Required:**
- **Generation type**: Image / Video / App (one-click)
- **Video duration**: model-dependent enum — check the model's `duration` values in `specs/model-specs.yaml` before offering choices (e.g. Seedance 2.0 4–15s, Veo 3.1 4/6/8s; image-to-video clips trend short)
- **Aspect ratio**: 16:9 / 9:16 / 1:1 / 4:5 / 4:3 / 21:9-where-supported (default: 16:9) — enums per model in `specs/model-specs.yaml` (HARD RULE 7); anamorphic / 2.35:1 / 2.39:1 are **Look-line style register**, never output ratios
- **Model preference** (or ask Claude to recommend — see `skills/higgsfield-models/SKILL.md`)

**Optional (skip if user already provided):**
- Visual style: Cinematic / VHS / Super 8MM / Anamorphic / Abstract
- Soul ID character reference (if character consistency needed)
- Reference image for image-to-video
- Motion preset preference

> Ask everything in one message — do not split across multiple rounds.

---

### Route to the Right Skill

| User wants | Route to |
|------------|----------|
| User unsure which workspace/tool fits, or asks "what should I use for X" | `higgsfield-workspaces` |
| Write or improve a prompt | `higgsfield-prompt` + relevant sub-skills |
| Develop a character / world / story / premise before prompting, build a character sheet / story bible, lock a visual style ("visual DNA"), keep a character consistent across many shots, or "I keep getting generic AI characters" | `higgsfield-character-design` |
| Cinematic still image prompt (shot framing, angles) | `higgsfield-image-shots` |
| GPT Image 2.0 / gpt-image-2 prompt, UI mockup, infographic, character/reference sheet, layout-dense image, or static-ad recreation | `higgsfield-gpt-image-2` |
| Choose the right model | `higgsfield-models` |
| Camera movement guidance (video) | `higgsfield-camera` |
| Named motion preset (Explosion, Werewolf, etc.) | `higgsfield-motion` |
| Visual style selection | `higgsfield-style` |
| Character consistency across shots | `higgsfield-soul` |
| **Consistency tie-break:** character consistency via a live Soul ID / reference images inside Higgsfield → `higgsfield-soul`; developing WHO the character is first (sheet, story bible, visual DNA) → `higgsfield-character-design`. Both may apply in sequence: design first, then lock with Soul. | — |
| VFX presets (Air Bending, Plasma, etc.) | `higgsfield-motion` |
| One-click App workflow | `higgsfield-apps` |
| Genre recipe (action, horror, ad, etc.) | `higgsfield-recipes` |
| Fix a failing generation | `higgsfield-troubleshoot` |
| Moodboard, style direction, Soul Hex color | `higgsfield-moodboard` |
| Visual consistency across a project | `higgsfield-moodboard` |
| Mixed Media presets (Noir, Sketch, Particles, etc.) | `higgsfield-mixed-media` |
| Photodump style preset / social-feed photo-dump aesthetic | `photodump-presets.md` (root reference) |
| Artistic style transformation, preset stacking | `higgsfield-mixed-media` |
| Higgsfield Assist (GPT-5 copilot) | `higgsfield-assist` |
| Credit optimization, plan selection, budget strategy | `higgsfield-assist` |
| Cinema Studio 2.5 / Cinema Studio 3.0 / Cinema Studio 3.5 / multi-shot sequence workflow / Soul Cast | `higgsfield-cinema` |
| Optical physics, camera bodies, lenses, Hero Frame | `higgsfield-cinema` |
| Elements system (@Characters/@Locations/@Props) | `higgsfield-cinema` |
| Director Panel, Speed Ramp, shot modes, Popcorn | `higgsfield-cinema` |
| Cinema Studio 3.0 Smart mode, @ references, native audio | `higgsfield-cinema` |
| Cinema Studio 3.5 — three-pill UI, Style Settings, Camera Settings, Manual Style, AI director toggle | `higgsfield-cinema` |
| User mentions Marketing Studio, DTC Ads, `ms_image`, or `marketing_studio_video` model | `higgsfield-marketing-studio` |
| User wants UGC / Tutorial / Unboxing / Hyper Motion / Product Review / TV Spot / Wild Card / UGC Virtual Try On / Pro Virtual Try On ad video | `higgsfield-marketing-studio` |
| User mentions hook+setting picklists, preset / custom / text-generated avatars in MS context, or 4–15s ad video constraints | `higgsfield-marketing-studio` |
| User wants to run a full campaign pipeline — research → plan → generate → publish → report, "create a campaign", "100 UGC videos", content plan, batch ads, cost-savings report | `higgsfield-content-factory` |
| User mentions Higgsfield Canvas, a node-based / node-graph workspace, an infinite board, chaining prompts→images→videos into a pipeline, Shared Canvas, or a ComfyUI-style node workflow | `higgsfield-canvas` |
| Multi-shot workflow, chaining tools, full production pipeline | `higgsfield-pipeline` |
| Short film, branded content, Popcorn → video → assembly | `higgsfield-pipeline` |
| Vibe Motion, kinetic typography, animated text, infographic/data/presentation animation, logo/brand animation as **code** (Remotion — crisp text, exact brand colors, deployable, real-time edits) | `higgsfield-vibe-motion` |
| Animated AD / brand promo as an **AI-generated video** built brief → storyboard sheet → Seedance ("make a motion", "motion design ad", "animate my logo into a video", "promo/ad video", classicMD/highMD) | `higgsfield-motion-design` |
| **Vibe Motion vs Motion Design** (both say "motion graphics / brand / logo animation"): want **crisp text, exact colors, deployable code, editable canvas** → `higgsfield-vibe-motion` (Remotion code); want a **cinematic/kinetic AI video clip** (pixel render, native audio, no guaranteed-crisp text) → `higgsfield-motion-design` (Seedance). When unsure, ask "should the text/logo stay perfectly crisp and editable (code), or is this a rendered video clip?" | — |
| Pre-generation memory check, apply past failure fixes | `higgsfield-recall` |
| User reports a generation result (kept/rejected/flagged) — log it to the ledger | `higgsfield-recall` |
| Takes-per-kept ratios, credit budgeting from logged data | `higgsfield-assist` |
| Audio design, dialogue cues, SFX, ambient sound | `higgsfield-audio` |
| **Standalone audio generation** — soundtrack, ambience bed, multi-speaker scene audio, Seed Audio 1.0 (`seed_audio`), TTS voiceover / narration as its own deliverable | `higgsfield-audio` |
| **Extend / continue an existing clip** — "make it longer", "what happens next / before", prequel, last-frame handoff, extension chains | `higgsfield-seedance` (§ Extension Prompting) + `higgsfield-pipeline` (§ Continuation & Extension Handoff) |
| **Prep assets / reference sheets before video** — character sheet, prop three-view, location plate, "build my elements", variety sheet for crowds | `templates/ad-asset-prep.md` + `higgsfield-gpt-image-2` (props) + `higgsfield-soul` (people & crowds) |
| Audition / screen-test a designed character (how they move, speak, react) before scene generation | `higgsfield-character-design` (§ Screen Test / Audition) |
| Seedance 2.0 / Pro prompt, flagged prompt, credit waste on Seedance | `higgsfield-seedance` |
| **Seedance 2.5** — user names 2.5 / Dreamina / Jimeng, wants a single clip longer than 15s, wants to **edit** or **extend** a video that already exists, or supplies many image/video/audio references (up to 30/10/10) | `higgsfield-seedance-2-5` |
| **2.0 vs 2.5** (both say "Seedance"): needs 4K/1080p, a platform start/end frame, or a `genre` hint → `higgsfield-seedance`; needs >15s in one generation, video editing, forward/backward extension, or heavy multi-reference → `higgsfield-seedance-2-5`. 2.5 caps at 720p | — |
| **Character performance** — acting, behavior, mannerisms, tics, a gait, subtext, "my characters look wooden / dead-eyed / AI", keeping a character themselves across many shots, an acting master profile | `higgsfield-acting` |
| **Feature-film production pipeline on Seedance** — headless character sheets, location sheets, a scene geography block reused across shots, dialogue construction, iteration discipline, giants / crowds / threshold transitions | `higgsfield-seedance` (`HELL-GRIND.md`) |
| **Transform footage the user already has** (video-to-video): "make a Seedance prompt for this video/clip", add a VFX element (set my head/hair on fire, transform my hand, make a limb invisible), swap the world/background around a preserved subject (desert, clouds, lava, neon city), put a giant creature behind me or on a landmark, relight/regrade to match, sync a crash-zoom/push-in to a line — a **real source clip** is the starting point | `higgsfield-seedance-vfx` |
| **Replace a VFX/3D pipeline with generation** — "can AI do this instead of VFX", put myself in this plate, put a creature in my footage, a dragon/monster shot without buying or rigging a 3D model, "how do I build a whole VFX shot", asset sheets → size-ref → locations → shots as one pipeline; also "my v2v keeps failing / turns to slop", scale drift between two subjects, which image model for faces vs creatures vs clothing vs locations | `higgsfield-seedance-2-5` (`VFX-PIPELINE.md`) |
| Precise facial expression / FACS / Action Unit codes (AU12, AU6…), forced or uncanny or mixed expression, close-up micro-performance, monologue/dialogue facial acting, "which AU code for anger/fear", FACS reference sheet | `higgsfield-facs` |
| "Make a shotlist", break a script/brief/treatment into many connected Seedance prompts, director's shotlist, global style prefix + `@`-glossary + named per-scene prompts as one editable HTML | `higgsfield-shotlist-director` |
| User has Higgsfield CLI / MCP / bundled skills installed and asks how this skill works alongside them | `higgsfield-stack` |
| User mentions `higgsfield auth login`, `higgsfield generate create`, `mcp.higgsfield.ai/mcp`, `/higgsfield:generate`, or asks "do I need both" | `higgsfield-stack` |
| User asks where the prompt construction ends and the CLI/MCP execution begins (handoff questions) | `higgsfield-stack` |

---

### Load Map — how much to read

The routing table says *where*; this says *how much*. Loads are cumulative — every path starts from HARD RULE 2's mandatory reads.

| Situation | Load |
|-----------|------|
| Simple creative prompt (Fast Path) | root `SKILL.md` + `skills/higgsfield-prompt/SKILL.md` — nothing else |
| Any Seedance prompt | + `skills/higgsfield-seedance/SKILL.md` (+ the matching `templates/seedance/` file when the request is technique-shaped) |
| Multi-scene / sequence / script breakdown | + `higgsfield-shotlist-director` + `higgsfield-pipeline` |
| Model choice unclear or contested | + `higgsfield-models` + `specs/` (the generated spec for the output type) |
| User reports a generation result | + `higgsfield-recall` (ledger write) |
| Budget / credits / plan question | + `higgsfield-assist` |
| Anything else | one routing-table row → that sub-skill; resist loading more than the row names |

### Check Templates for Genre Match

Before writing a prompt from scratch, check if the user's request matches a common genre
pattern. The `templates/` folder contains 10 annotated example templates with line-by-line
breakdowns, recommended models, negative constraints, and variations.

| User request matches | Check template |
|---------------------|----------------|
| Chase, pursuit, action, parkour | `templates/01-cinematic-action-chase.md` |
| Product, commercial, ad, UGC | `templates/02-product-ugc-showcase.md` |
| Horror, scary, creepy, dread | `templates/03-horror-atmosphere.md` |
| Fashion, editorial, lookbook | `templates/04-fashion-editorial.md` |
| Sci-fi, cyberpunk, VFX, space | `templates/05-sci-fi-vfx.md` |
| Portrait, character intro, close-up | `templates/06-portrait-character-intro.md` |
| Landscape, nature, establishing shot | `templates/07-landscape-establishing-shot.md` |
| Comedy, social media, TikTok, skit | `templates/08-comedy-social-media.md` |
| Romance, intimate, couple, wedding | `templates/09-romantic-intimate.md` |
| Dance, music, performance, concert | `templates/10-dance-music-performance.md` |

Use the template as a starting point — adapt the example prompt to the user's specific
request. The annotations explain WHY each element works, helping you make informed
substitutions.

**Technique templates** (`templates/seedance/`) — structure templates for Seedance
prompts where the user request is technique-shaped rather than genre-shaped:

| Technique need | Template |
|---|---|
| Pre-visualize multi-character spatial geometry before prompting | `templates/seedance/top-down-map.md` |
| Multi-character shot with cross-character relationships | `templates/seedance/multi-character-anchor.md` |
| Single-character shot with position + pose + contact-point locks | `templates/seedance/single-character-position.md` |
| Worked example: two-character anchoring end-to-end | `templates/seedance/worked-example-two-character.md` |
| Anime / stylized-2D animation — layered formula + style block + character turnaround | `templates/seedance/anime-animation.md` |
| Close-up facial acting via FACS Action Unit codes — beat-synced expression schedule | `templates/seedance/facs-expression-beats.md` |
| Seedance **2.5** multi-reference brief — role map + staged beats with end states | `templates/seedance/omni-reference-2-5.md` |

**Text-overlay templates** (`templates/text-overlays/`) — paste-ready text-rendering
prompts for slogan / subtitle / speech-bubble overlays:

| Text overlay type | Template |
|---|---|
| Slogan / brand callout / opening title | `templates/text-overlays/slogan.md` |
| Subtitle (dialogue-synchronized) | `templates/text-overlays/subtitle.md` |
| Speech bubble (character-attributed) | `templates/text-overlays/speech-bubble.md` |

---

### Build the Prompt Using the MCSLA Formula

Full MCSLA definition and prompt structure → `skills/higgsfield-prompt/SKILL.md`

Quick summary — five layers, every prompt:

| M | C | S | L | A |
|---|---|---|---|---|
| Model | Camera | Subject | Look | Action |

**Core rules:**
- Be specific — name camera presets, describe VFX concretely
- Keep prompts under 200 words (short-form regime — block-scaffold production prompts follow their own structural rules, HARD RULE 8)
- Subject → Action → Camera → Style is the most reliable order

---

### Output Format

**Single prompt:**
```
**Model**: [model name]
**Aspect ratio**: [ratio]  **Duration**: [Xs]  **Style**: [style]

[Prompt]

**Camera**: [camera control name]
**Motion preset** (if used): [preset name]
```

**Two versions (when style varies):**
```
### Version 1 — [Style Name]
[Prompt]

---
### Version 2 — [Style Name]
[Prompt]
```

**Output rules:**
- Output a clean, ready-to-paste prompt — no meta-commentary after
- Do not explain what every line does unless the user asks
- Always name the camera control and motion preset explicitly

---

## Generation Ledger — log every result

Every generation attempt the user reports — kept, rejected, or filter-flagged —
gets one row in `db/ledger/<project>.json`. The denominator (successes too,
not just failures) is what turns the memory system into takes-per-kept ratios
and credit budgets.

**The 5-second rule:** when the user reports a result, ask at most ONE
question ("keep or reject — what failed?") and write the row yourself with
one `scripts/higgsfield_memory.py log-gen` command. Never ask twice; never present a
form. Full workflow: `skills/higgsfield-recall/SKILL.md` § Log the Generation
Result. Ratios and budgeting: `skills/higgsfield-assist/SKILL.md`.

---

## @ Reference Rules

- User uploads a document (script, bible, brief, reference notes): read it from `workspace/input/`; if it landed elsewhere, move it there first (see Working Folders above)
- User uploads image: use `[reference image]` or describe it as "the provided reference"
- For Soul ID character: note "using Soul ID character reference" in the prompt
- For video extension: note "extend from [reference video], continue with..."
- For style transfer: note "match the visual style of [reference image]"

---

## Shared Resources

| Resource | What it contains | When to use |
|----------|-----------------|-------------|
| `skills/shared/negative-constraints.md` | All generation artifacts + prevention phrases, by category | Check before every prompt — append relevant constraints |
| `templates/` | 10 annotated genre templates with examples, models, annotations, variations | When user request matches a common genre — use as starting point |
| `templates/ad-asset-prep.md` | Ad asset preparation: product sheets, hero-character sheets, location plates — generate-many → test-in-motion → lock-the-winner | When an ad/product request needs reference assets built before video |
| `templates/character-design/` | 6 character-design worksheets (9-question sheet, story bible, visual DNA) | With `higgsfield-character-design` when developing characters before prompting |
| `templates/seedance/` | 9 Seedance technique templates: top-down-map, multi-character-anchor, single-character-position, worked-example-two-character, anime-animation, facs-expression-beats, footage-vfx-transform, global-style-prefix, omni-reference-2-5 | When Seedance request is technique-shaped (spatial blocking, multi-character anchoring, anime/stylized-2D, FACS acting, footage VFX, style prefix, 2.5 multi-reference) |
| `templates/text-overlays/` | 3 text-rendering templates: slogan, subtitle, speech-bubble | When user request includes on-screen text rendering |

---

## Sub-Skills (auto-loaded as needed)

| Skill | Trigger |
|-------|---------|
| `higgsfield-workspaces` | User is choosing a workspace / asking "what should I use for X" / hasn't picked a tool yet |
| `higgsfield-prompt` | Any prompt writing or refinement request |
| `higgsfield-image-shots` | Cinematic image prompts — shot framing, angles, composition |
| `higgsfield-gpt-image-2` | GPT Image 2.0 prompts — three-format taxonomy (JSON / prose / meta-prompt), UI mockups, infographics, reference sheets, static-ad recreation |
| `higgsfield-models` | "Which model should I use?" / model comparison |
| `higgsfield-camera` | Camera movement questions (video) |
| `higgsfield-motion` | Named preset requests (Explosion, Werewolf, VFX, etc.) |
| `higgsfield-style` | Visual style / aesthetic questions |
| `higgsfield-soul` | Character consistency / Soul ID |
| `higgsfield-character-design` | Pre-production story bible — premise / world / 9-question character / story spine / visual DNA (before prompting) |
| `higgsfield-apps` | One-click app recommendations |
| `higgsfield-recipes` | Genre scene templates |
| `higgsfield-troubleshoot` | Failed generations / quality issues |
| `higgsfield-moodboard` | Moodboard / Soul Hex / project-level style consistency |
| `higgsfield-mixed-media` | Artistic preset overlays (Noir, Sketch, Particles, etc.) |
| `higgsfield-assist` | Higgsfield Assist copilot / credit optimization / plan selection |
| `higgsfield-cinema` | Cinema Studio 2.5 + 3.0 + 3.5 / Soul Cast / color grading / optical physics / multi-shot / Elements / Smart mode / @ references / Style Settings / Camera Settings / Manual Style |
| `higgsfield-marketing-studio` | Marketing Studio / DTC Ads / ad video / UGC video / Hyper Motion / TV Spot / Wild Card / Pro Virtual Try On / hook + setting picklists / 4–15s ad video / `marketing_studio_video` MCP / cross-surface workflow |
| `higgsfield-content-factory` | Campaign pipeline (research → plan → generate → publish → report) / UGC-first 5-format mix / batch generation gate / Meta Ads scheduling / cost-savings report |
| `higgsfield-canvas` | Node-based Canvas workspace / infinite board / chain prompts→images→videos / named canvas patterns / build-free generate-paid cost model / Shared Canvas live collaboration |
| `higgsfield-pipeline` | Multi-shot workflow / tool chaining / full production pipeline |
| `higgsfield-vibe-motion` | Vibe Motion — motion graphics / kinetic typography / brand + logo animation as **Remotion code** (crisp text, exact colors, deployable) |
| `higgsfield-motion-design` | Animated-ad flow brief → storyboard → Seedance video (**AI pixel render**, not code; classicMD/highMD) |
| `higgsfield-recall` | Pre-generation memory check / apply past failure fixes |
| `higgsfield-audio` | Audio design, dialogue, SFX, ambient sound for audio-capable models |
| `higgsfield-seedance` | Seedance 2.0 / Pro prompt director + content-filter preflight linter (+ `HELL-GRIND.md`, Higgsfield's open-sourced feature-film pipeline) |
| `higgsfield-seedance-2-5` | Seedance 2.5 omni-reference dialect — the four modes (t2v / omni_reference / video_edit / video_extension), reference-role grammar, 30s staging, editing + forward/backward extension, keyframes, storyboards, blockouts, transitions (+ `VFX-PIPELINE.md`, the AI-VFX production pipeline: asset-class model routing, size-ref frame, the `omni_reference` v2v lane, the four-batch rule, the slop catalog) |
| `higgsfield-seedance-vfx` | Video-to-video footage transformation for Seedance 2.0 — preserve a real subject + camera move, add a VFX element / swap the environment / drop a photoreal creature / relight to match / sync a timed zoom, run in std 4K |
| `higgsfield-acting` | Character performance as behavior under pressure — objective / obstacle / tactics / beats / subtext, body + status + proxemics, mandatory eye life, the 150–220-word acting master profile and its per-scene rewrite, locked voice prompt |
| `higgsfield-shotlist-director` | Brief/script → one connected Seedance shotlist (style prefix + `@`-glossary + named per-scene prompts) as editable HTML |
| `higgsfield-facs` | FACS Action Unit codes for precise facial expressions in Seedance 2.0 — forced/uncanny/mixed expressions, close-up dialogue facial acting, emotion→AU recipes, FACS reference sheets |
| `higgsfield-stack` | User mentions the Higgsfield CLI / MCP connector / bundled skills, or asks how this skill coexists with those execution surfaces |

> Full vocabulary in `vocab.md`
> Full motion preset library in `skills/higgsfield-motion/SKILL.md`
> Model comparison in `model-guide.md`
> Example prompts in `prompt-examples.md`
> Shared negative constraints in `skills/shared/negative-constraints.md`
> Genre-specific annotated templates in `templates/`
