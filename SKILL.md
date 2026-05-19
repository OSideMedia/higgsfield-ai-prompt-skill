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
  version: 3.7.16
  updated: 2026-05-18
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

3. **Named vocabulary verified, not invented.** Camera preset names, motion preset names, model names, CLI flag forms, and MCP tool parameter names all come from the skill files or from live verification (`higgsfield model get <model>` for CLI param schemas; `models_explore` for MCP). If you found yourself thinking "this flag probably looks like X" or "this preset is probably called Y" — stop. Read the file or run the verification command. Plausibility is not validity. Do not substitute generic video-prompt vocabulary for named Higgsfield presets; do not invent model versions, camera presets, or motion-preset names. If the user names one you don't see in the skill files, say so and ask for clarification.

4. **MCSLA structure intact on video prompts.** Model · Camera · Subject · Look · Action. Five layers, every video prompt, unless the user explicitly opted out.

5. **Shared negative constraints appended.** Pull positive-phrasing prevention phrases from `skills/shared/negative-constraints.md`. Do not paraphrase from training; use the exact phrasing from the file. (Kling 3.0 prefers positive phrasing over negations; using negation-form constraints when the file says positive is a fidelity miss.)

6. **Preflight surfaced when applicable.** If execution intent is signaled (CLI / MCP / bundled-skills mentioned) AND a video-class or high-cost model is named OR a budget concern is named, surface the two-step preflight (`model get` / `models_explore` for schema, then cost estimate). See `skills/higgsfield-stack/SKILL.md` § Preflight discipline.

7. **Aspect ratio is an enum, not a free-form value.** Check the model's allowed ratios via schema verify before writing them into the header. Anamorphic / 2.35:1 / 2.39:1 are *style register* vocabulary for the Look line, not output ratios. See `vocab.md` § Aspect Ratio: output spec vs. style register.

8. **Prompt under 200 words.** Soft cap from MCSLA section. Going over is a signal you're padding rather than locking — tighten.

**If any of items 1–8 are missing or unverified, the response is incomplete. Complete them before sending, not after.**

---

## What Is Higgsfield?

Higgsfield is a cinematic AI video and image generation platform built for filmmakers and
creators. Unlike single-model tools, Higgsfield hosts **multiple generation engines** on one
platform — Kling 3.0/3.0 Omni/3.0 Motion Control, Sora 2, Google Veo 3.1/3.1 Lite, Wan 2.7/2.6/2.5,
Seedance 2.0/Pro, Minimax Hailuo 2.3/02, Higgsfield DoP (Lite/Standard/Turbo) for video; Soul 2.0, Soul Cinema Preview,
Soul Cast, Nano Banana Pro/2, Kling Image 3.0/Omni, Seedream 4.0, GPT Image 1.5,
Flux 2/Kontext for images — plus a library of 100+ named **Motion Presets**, a **Soul ID**
character consistency system, **Cinema Studio 2.5**, **Cinema Studio 3.0** (Business/Team plan), and **Cinema Studio 3.5** with Soul Cast AI actors, native dual-channel stereo audio, and 80+
one-click **Apps**.

---

## Workflow

### Fast Path — Simple Creative Requests

If the user provides a clear creative intent ("write me a prompt for a car chase at night")
with no specific constraints, **generate immediately** using these sensible defaults:

> **Fast Path still requires reading `skills/higgsfield-prompt/SKILL.md` first — Fast Path means skip clarifying questions, NOT skip the file read.**

| Parameter | Default |
|-----------|---------|
| Aspect ratio | 16:9 |
| Duration | 8s |
| Style | Cinematic |
| Video model | Kling 3.0 (character-focused) or Sora 2 (action/scale) |
| Image model | Soul 2.0 (portrait) or Nano Banana 2 (everything else) |

Do not ask clarifying questions. Deliver a ready-to-paste prompt. Mention the defaults
used so the user can adjust if they want something different.

> If you did not read `skills/higgsfield-prompt/SKILL.md` earlier in this conversation, read it now before writing the prompt.

### Full Path — Production Requests

When the user signals production-grade intent (Cinema Studio, multi-shot, specific model,
budget constraints, client work), **confirm before generating:**

**Required:**
- **Generation type**: Image / Video / App (one-click)
- **Video duration**: 5s / 10s (image-to-video clips are 3–5s; text-to-video up to 10s+)
- **Aspect ratio**: 16:9 / 9:16 / 1:1 / 4:5 / 4:3 / 2.35:1 (default: 16:9)
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
| Cinematic still image prompt (shot framing, angles) | `higgsfield-image-shots` |
| Choose the right model | `higgsfield-models` |
| Camera movement guidance (video) | `higgsfield-camera` |
| Named motion preset (Explosion, Werewolf, etc.) | `higgsfield-motion` |
| Visual style selection | `higgsfield-style` |
| Character consistency across shots | `higgsfield-soul` |
| VFX presets (Air Bending, Plasma, etc.) | `higgsfield-motion` |
| One-click App workflow | `higgsfield-apps` |
| Genre recipe (action, horror, ad, etc.) | `higgsfield-recipes` |
| Fix a failing generation | `higgsfield-troubleshoot` |
| Moodboard, style direction, Soul Hex color | `higgsfield-moodboard` |
| Visual consistency across a project | `higgsfield-moodboard` |
| Mixed Media presets (Noir, Sketch, Particles, etc.) | `higgsfield-mixed-media` |
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
| Multi-shot workflow, chaining tools, full production pipeline | `higgsfield-pipeline` |
| Short film, branded content, Popcorn → video → assembly | `higgsfield-pipeline` |
| Vibe Motion, motion graphics, kinetic typography, brand animation | `higgsfield-vibe-motion` |
| Animated text, logo animation, Remotion-based output | `higgsfield-vibe-motion` |
| Pre-generation memory check, apply past failure fixes | `higgsfield-recall` |
| Audio design, dialogue cues, SFX, ambient sound | `higgsfield-audio` |
| Seedance 2.0 / Pro prompt, flagged prompt, credit waste on Seedance | `higgsfield-seedance` |
| User has Higgsfield CLI / MCP / bundled skills installed and asks how this skill works alongside them | `higgsfield-stack` |
| User mentions `higgsfield auth login`, `higgsfield generate create`, `mcp.higgsfield.ai/mcp`, `/higgsfield:generate`, or asks "do I need both" | `higgsfield-stack` |
| User asks where the prompt construction ends and the CLI/MCP execution begins (handoff questions) | `higgsfield-stack` |

---

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
- Keep prompts under 200 words
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

## @ Reference Rules

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
| `templates/seedance/` | 4 Seedance technique templates: top-down-map, multi-character-anchor, single-character-position, worked-example-two-character | When Seedance request is technique-shaped (spatial blocking, multi-character anchoring) |
| `templates/text-overlays/` | 3 text-rendering templates: slogan, subtitle, speech-bubble | When user request includes on-screen text rendering |

---

## Sub-Skills (auto-loaded as needed)

| Skill | Trigger |
|-------|---------|
| `higgsfield-workspaces` | User is choosing a workspace / asking "what should I use for X" / hasn't picked a tool yet |
| `higgsfield-prompt` | Any prompt writing or refinement request |
| `higgsfield-image-shots` | Cinematic image prompts — shot framing, angles, composition |
| `higgsfield-models` | "Which model should I use?" / model comparison |
| `higgsfield-camera` | Camera movement questions (video) |
| `higgsfield-motion` | Named preset requests (Explosion, Werewolf, VFX, etc.) |
| `higgsfield-style` | Visual style / aesthetic questions |
| `higgsfield-soul` | Character consistency / Soul ID |
| `higgsfield-apps` | One-click app recommendations |
| `higgsfield-recipes` | Genre scene templates |
| `higgsfield-troubleshoot` | Failed generations / quality issues |
| `higgsfield-moodboard` | Moodboard / Soul Hex / project-level style consistency |
| `higgsfield-mixed-media` | Artistic preset overlays (Noir, Sketch, Particles, etc.) |
| `higgsfield-assist` | Higgsfield Assist copilot / credit optimization / plan selection |
| `higgsfield-cinema` | Cinema Studio 2.5 + 3.0 + 3.5 / Soul Cast / color grading / optical physics / multi-shot / Elements / Smart mode / @ references / Style Settings / Camera Settings / Manual Style |
| `higgsfield-marketing-studio` | Marketing Studio / DTC Ads / ad video / UGC video / Hyper Motion / TV Spot / Wild Card / Pro Virtual Try On / hook + setting picklists / 4–15s ad video / `marketing_studio_video` MCP / cross-surface workflow |
| `higgsfield-pipeline` | Multi-shot workflow / tool chaining / full production pipeline |
| `higgsfield-vibe-motion` | Vibe Motion / motion graphics / kinetic typography / brand animation |
| `higgsfield-recall` | Pre-generation memory check / apply past failure fixes |
| `higgsfield-audio` | Audio design, dialogue, SFX, ambient sound for audio-capable models |
| `higgsfield-seedance` | Seedance 2.0 / Pro prompt director + content-filter preflight linter |
| `higgsfield-stack` | User mentions the Higgsfield CLI / MCP connector / bundled skills, or asks how this skill coexists with those execution surfaces |

> Full vocabulary in `vocab.md`
> Full motion preset library in `skills/higgsfield-motion/SKILL.md`
> Model comparison in `model-guide.md`
> Example prompts in `prompt-examples.md`
> Shared negative constraints in `skills/shared/negative-constraints.md`
> Genre-specific annotated templates in `templates/`
