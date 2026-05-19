[![Version](https://img.shields.io/badge/version-3.7.13-blue)](https://github.com/OSideMedia/higgsfield-ai-prompt-skill)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Claude%20Cowork%20%7C%20Claude%20Code-purple)](https://github.com/OSideMedia/higgsfield-ai-prompt-skill)

# Higgsfield AI Prompt Skill

A comprehensive Claude skill library for generating high-quality prompts on
[Higgsfield AI](https://higgsfield.ai) — the cinematic video and image generation platform.

## What This Skill Does

Transforms natural language requests into production-ready Higgsfield prompts using:
- The **MCSLA formula** (Model · Camera · Subject · Look · Action)
- Named camera controls and motion presets the platform recognizes
- Model selection guidance across Kling 3.0 / 3.0 Omni / 3.0 Motion Control, Sora 2, Veo 3.1, Wan, Seedance 2.0, Minimax Hailuo, Higgsfield DoP, and more
- Genre recipe templates for action, horror, romance, sci-fi, product ads, and more
- Soul ID character consistency guidance + Character Sheet creation
- Troubleshooting for failed or poor generations
- **Cinema Studio 2.5** advanced features: Soul Cast AI actors, built-in color grading, 3D Mode (Gaussian Splatting), Grid Generation, Resolution Settings, Frame Extraction Loop, Object & Person Insertion, Per-Character Emotions, Clustering, Five-View Location Reference Sheet, Reference Sheet Types (Motion / Outfit / Palette), Elements System with library surface (5 source tabs × 6 element categories)
- **Cinema Studio 3.0** (Business/Team plan): native dual-channel stereo audio, Smart shot control, 15s max duration, 7 genres, @ reference patterns, Soul Cast 3.0
- **Cinema Studio 3.5**: three-pill main UI (Genre / Style / Camera), Style Settings panel (8 Color Palette / 6 Lighting / 9 Camera Moveset Style + Manual Style mode), Camera Settings four-axis panel (3 Camera Body / 5 Lens / 5 Focal Length including new 75mm / 3 Aperture), Image Mode with four Cinematic models picker (Soul Cinema default, Cinematic Characters, Cinematic Locations, Cinematic Cameras with 2.5 vocabulary)
- **Seedance 2.0 prompting best practices** — Intent over Precision, Genre Router, I2V Gate, Anti-Slop, Physics Language, SCELA audio, Reference-Based / Continuation / Expand Shot / Edit Shot / Transformation prompt modes, Continuation Prompt Formula, the Iteration Rule
- **Shared negative constraints reference** — categorized artifacts + prevention phrases (positive alternatives for 3.0); Kling 3.0 Motion Control failure diagnostic; Physics Rendering — Resolution Decision Matrix (cross-model 480p / 720p / 1080p routing rule for Seedance 2.0 + Cinema Studio 3.x)
- **Identity vs. Motion separation** — hard rule for character consistency across shots
- **Annotated templates library** — 10 genre templates with Cinema Studio 3.0 genre mappings, plus Seedance multi-character coordination + text-overlay sub-libraries (17 files across 3 categories)
- **DISCIPLINE.md cross-cutting framework** — 9 named discipline patterns in 3-3-3 tier symmetry (prompt-construction, model-selection, iteration-discipline) governing decisions across all sub-skills
- **production-benchmarks.md** — Hell Grind 90-min Cannes feature reference, per-character iteration anchors, acceptance-rate calibration; what "production quality" means in practice
- **FAILURE-MODES.md (Seedance)** — 8 named render failures documented with symptom + mechanism + counter for diagnosis-first iteration
- **C-arc Building Complete AI Projects — 10-Step Methodology** — end-to-end pipeline from idea to delivered project; complements the genre/scene templates
- **Expanded Seedance methodology + Soul refinement** — Iteration Rule + 6-Pass Diagnostic Sequence + Four Questions + Next-Shot Decision Tree + Bridging / Continuation / Repair working modes; Character Anchor Block + Two-Tool Refinement Pipeline for character consistency at production scale

## Install

### Claude Code
```bash
git clone https://github.com/OSideMedia/higgsfield-ai-prompt-skill ~/.claude/skills/higgsfield
```

### Claude Cowork
Drop the repo folder into your Cowork workspace. The skill dispatcher is at `SKILL.md` in the repo root.

### Claude.ai Projects
Upload `SKILL.md` (root) as your project instruction base. Upload files from `skills/` as project documents.

## Higgsfield Stack Integration

This skill is the prompt-construction layer. Higgsfield ships official execution tooling — a CLI, an MCP custom connector, and a bundled skills package. They complement each other: this skill produces the prompt, their tooling executes it. None of their tooling is required for this skill to work — you can always paste prompts directly into higgsfield.ai. But if you want an end-to-end loop, you'll want one of the three.

**A Higgsfield account is required** for any of the tooling below. Sign up at [higgsfield.ai](https://higgsfield.ai).

### Higgsfield CLI

Command-line tool for terminal-native agents (Claude Code, Codex, Cursor). Per Higgsfield's own guidance, prefer the CLI over the MCP if you're working in a terminal.

- Repo: [github.com/higgsfield-ai/cli](https://github.com/higgsfield-ai/cli)
- Install: `curl -fsSL https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh | sh` or `brew install higgsfield-ai/tap/higgsfield`
- Auth: `higgsfield auth login`

### Higgsfield MCP

Custom connector for claude.ai web and the Claude desktop app. Separate product from the CLI.

- Connector URL: `https://mcp.higgsfield.ai/mcp`
- Install: claude.ai → Settings → Connectors → Add custom connector → paste the URL above → sign in

### Higgsfield Bundled Skills

Markdown skill bundle for agents that consume Cowork-style skills. All three skills drive the CLI under the hood.

- Repo: [github.com/higgsfield-ai/skills](https://github.com/higgsfield-ai/skills)
- Install: `npx skills add higgsfield-ai/skills`
- Skills included: `higgsfield-generate`, `higgsfield-soul`, `higgsfield-product-photoshoot`
- Invoke: `/higgsfield:generate`, `/higgsfield:soul`, `/higgsfield:product-photoshoot`

### End-to-end example

How the layers fit together for a real request:

```
USER:    "Make me a cinematic chase scene through a night market.
          Use my trained Soul character — reference_id abc123."
   ↓
THIS SKILL — higgsfield-ai-prompt-skill
   • routes to higgsfield-prompt + higgsfield-camera + higgsfield-soul
   • picks Kling 3.0 (character-focused, supports --soul-id)
   • applies MCSLA: model, camera preset, subject, look, action
   • appends shared negative constraints
   • outputs a production-grade Higgsfield prompt
   ↓
PRE-FLIGHT (optional, recommended for Veo / Kling / Sora / Seedance video):

   SCHEMA VERIFY (recommended for any model you haven't called recently):
   CLI path:        higgsfield model get kling3_0
                    → returns schema: aspect_ratio enum, duration range,
                      mode/sound options, media roles
   MCP path:        models_explore(action="get", model_id="kling3_0")
                    → returns same schema as CLI

   COST ESTIMATE (no job submitted):
   MCP path:        generate_video(..., get_cost: true)
                    → returns credit cost + adjustments block

   CLI path:        higgsfield generate cost kling3_0 \
                      --prompt "<prompt from this skill>" \
                      --aspect_ratio 16:9 \
                      --duration 8
                    # (add reference flags as needed: --soul-id, --start-image,
                    #  --end-image — consult `higgsfield model get kling3_0`
                    #  for supported media roles)

   Bundled skills:  drop to CLI for the cost check (same auth, same workspace),
                    then invoke /higgsfield:generate

   Optional account checks (same data across surfaces):
   MCP path:        balance / transactions tools
   CLI path:        higgsfield account status
                    higgsfield account transactions --size 50

   Note: 2.35:1 is anamorphic STYLE vocabulary, not a valid Kling 3.0 output
         ratio. Output ratios are platform-bounded: 16:9 / 9:16 / 1:1 only.
   ↓
HIGGSFIELD STACK — one of three execution surfaces:

   CLI path:
     higgsfield generate create kling3_0 \
       --prompt "<prompt from this skill>" \
       --aspect_ratio 16:9 \
       --duration 8 \
       --wait
     # (add reference flags as needed: --soul-id, --start-image, --end-image —
     #  consult `higgsfield model get kling3_0` for supported media roles)

   Bundled skills path:
     /higgsfield:generate — takes the prompt as its --prompt argument,
     formats the CLI call above under the hood

   MCP path (claude.ai web/desktop):
     Claude invokes the Higgsfield connector with the prompt as input
   ↓
USER:    Result URL returned. Iterate if needed (this skill's
         iteration discipline applies regardless of execution surface).
```

The layer split holds in every case: this skill always produces the prompt, the Higgsfield stack always handles the generation call. None of the three execution paths reach back into prompt construction; this skill never shells out to their CLI or API.

> Full preflight discipline — when to surface it, marketing-studio caveat, CLI naming gotchas (`account status`, not `balance`), and the plan-tier-vs-surface framing — lives in [`skills/higgsfield-stack/SKILL.md`](skills/higgsfield-stack/SKILL.md) § Preflight discipline.

### Coexistence rules

For the full coexistence rules, detection signals, naming-collision callouts, and handoff templates, see [`skills/higgsfield-stack/SKILL.md`](skills/higgsfield-stack/SKILL.md).

## Structure

```
.
├── SKILL.md                          ← Main dispatcher (routes to sub-skills — start here)
├── README.md                         ← This file
├── CHANGELOG.md                      ← Version history
├── CONTRIBUTING.md                   ← Contribution guidelines
├── LICENSE                           ← MIT license
├── CLAUDE.md                         ← Project instructions for Claude Code
├── .markdownlint.json                ← Linter config (CHANGELOG convention silencing — v3.6.1)
├── model-guide.md                    ← Model comparison tables + decision flowchart
├── image-models.md                   ← Image model reference + pricing tiers
├── vocab.md                          ← Full platform vocabulary reference
├── prompt-examples.md                ← High-quality example prompts + Before/After pairs
├── photodump-presets.md              ← Photodump mode presets
├── DISCIPLINE.md                     ← Cross-cutting discipline framework (9 patterns, 3-3-3 tier symmetry)
├── production-benchmarks.md          ← Production-quality anchors + acceptance-rate calibration
├── higgsfield_memory.py              ← Memory system script
├── seedance_lint.py                  ← Seedance preflight linter
├── validate.py                       ← Pre-release validation script
├── generate_user_guide.py            ← USER-GUIDE.pdf generator (Path B refactor — v3.7.0)
├── validate_user_guide.py            ← USER-GUIDE.pdf drift validator (text-extract + binary diff)
├── db/
│   ├── filter-memory.json            ← Content filter memory (seeded)
│   └── quality-memory.json           ← Quality failure memory (seeded)
├── docs/                             ← Extended reference documents
│   ├── Seedance 2 Skill.md           ← Bilingual EN+ZH Seedance director reference
│   ├── archive/                      ← Historical artifacts
│   │   └── v3.0.0/                   ← v3.0.0 audit + inventory snapshot
│   ├── pdf-audit/                    ← PDF integration audit reports (v3.4.0, v3.6.0)
│   └── user-guide/                   ← Exported USER-GUIDE.pdf + version baselines
├── templates/                        ← Genre templates + Seedance coordination + text-overlays
│   ├── 01-cinematic-action-chase.md
│   ├── 02-product-ugc-showcase.md
│   ├── 03-horror-atmosphere.md
│   ├── 04-fashion-editorial.md
│   ├── 05-sci-fi-vfx.md
│   ├── 06-portrait-character-intro.md
│   ├── 07-landscape-establishing-shot.md
│   ├── 08-comedy-social-media.md
│   ├── 09-romantic-intimate.md
│   ├── 10-dance-music-performance.md
│   ├── seedance/                     ← Multi-character coordination templates
│   │   ├── multi-character-anchor.md
│   │   ├── single-character-position.md
│   │   ├── top-down-map.md
│   │   └── worked-example-two-character.md
│   └── text-overlays/                ← Text overlay templates
│       ├── slogan.md
│       ├── speech-bubble.md
│       └── subtitle.md
└── skills/
    ├── shared/
    │   └── negative-constraints.md       ← Shared artifact prevention reference
    ├── higgsfield-prompt/SKILL.md        ← Core MCSLA formula + prompt structure + Identity/Motion separation
    ├── higgsfield-image-shots/SKILL.md   ← Cinematic image prompting (shots, angles, composition)
    ├── higgsfield-models/
    │   ├── SKILL.md                      ← Compact model selection guide
    │   └── MODELS-DEEP-REFERENCE.md      ← Full per-model documentation (on-demand)
    ├── higgsfield-camera/SKILL.md        ← All camera controls + usage
    ├── higgsfield-motion/SKILL.md        ← Named motion presets library
    ├── higgsfield-style/SKILL.md         ← Visual styles + color grades + lighting
    ├── higgsfield-soul/SKILL.md          ← Soul ID character consistency
    ├── higgsfield-audio/SKILL.md         ← Audio prompting + Cinema Studio 3.0 native audio
    ├── higgsfield-apps/SKILL.md          ← One-click Apps guide
    ├── higgsfield-recipes/SKILL.md       ← Genre scene templates
    ├── higgsfield-troubleshoot/SKILL.md  ← Fix failing generations
    ├── higgsfield-assist/SKILL.md        ← General assistant + platform guidance
    ├── higgsfield-mixed-media/SKILL.md   ← Mixed media + hybrid generation
    ├── higgsfield-moodboard/SKILL.md     ← Moodboard creation workflows
    ├── higgsfield-pipeline/SKILL.md      ← Multi-step generation pipelines
    ├── higgsfield-recall/SKILL.md        ← Recall + regeneration patterns
    ├── higgsfield-cinema/SKILL.md        ← Cinema Studio 2.5 + 3.0 + 3.5 (Soul Cast, Color Grading, 3D Mode, Smart Mode, @ References, Native Audio, three-pill UI, Image Mode, Cinematic models picker)
    ├── higgsfield-seedance/
    │   ├── SKILL.md                      ← Seedance prompt director + content-filter preflight
    │   └── FAILURE-MODES.md              ← 8 named Seedance render failures (symptom · mechanism · counter)
    ├── higgsfield-vibe-motion/SKILL.md   ← Vibe-based motion direction
    └── higgsfield-workspaces/SKILL.md    ← Workspace-first decision layer (Cinema Studio / Lipsync / Draw-to-Video / Sora 2 Trends / Click to Ad / Higgsfield Audio)
```

## Example Prompts

**Basic:**
> "Write me a Higgsfield prompt for a cinematic action chase through a night market"

**Specific:**
> "I need a horror prompt using VHS style, Dutch angle camera, and the Horror Face preset"

**With reference:**
> "I have a Soul ID character. Write 3 different scene prompts with her — office, party, rooftop"

**Model question:**
> "Should I use Kling 3.0 or Sora 2 for a large-scale battle scene?"

**Troubleshoot:**
> "My image-to-video isn't animating, it's just static. What am I doing wrong?"

## The MCSLA Formula

| Letter | Layer | Example |
|--------|-------|---------|
| M | Model | Kling 3.0 |
| C | Camera | FPV Drone weaving through the alley |
| S | Subject | A woman in a tactical jacket |
| L | Look | Cinematic, cold blue shadows, 16:9 |
| A | Action | She sprints, slides under a gate |

---

Built February 2026 · v3.7.13 (updated 2026-05-18) · Platform: [higgsfield.ai](https://higgsfield.ai)
