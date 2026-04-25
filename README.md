[![Version](https://img.shields.io/badge/version-3.6.2-blue)](https://github.com/OSideMedia/higgsfield-ai-prompt-skill)
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
- **Seedance 2.0 prompting best practices** — Intent over Precision, Genre Router, I2V Gate, Anti-Slop, Physics Language, SCELA audio, Reference-Based / Continuation / Expand Shot / Edit Shot prompt modes, Continuation Prompt Formula, the Iteration Rule
- **Shared negative constraints reference** — categorized artifacts + prevention phrases (positive alternatives for 3.0); Kling 3.0 Motion Control failure diagnostic; Physics Rendering — Resolution Decision Matrix (cross-model 480p / 720p / 1080p routing rule for Seedance 2.0 + Cinema Studio 3.x)
- **Identity vs. Motion separation** — hard rule for character consistency across shots
- **10 annotated genre templates** — production-quality examples with Cinema Studio 3.0 genre mappings

## Install

### Claude Code
```bash
git clone https://github.com/OSideMedia/higgsfield-ai-prompt-skill ~/.claude/skills/higgsfield
```

### Claude Cowork
Drop the repo folder into your Cowork workspace. The skill dispatcher is at `SKILL.md` in the repo root.

### Claude.ai Projects
Upload `SKILL.md` (root) as your project instruction base. Upload files from `skills/` as project documents.

## Structure

```
.
├── SKILL.md                          ← Main dispatcher (routes to sub-skills — start here)
├── README.md                         ← This file
├── CHANGELOG.md                      ← Version history
├── CONTRIBUTING.md                   ← Contribution guidelines
├── USER-GUIDE.pdf                    ← Exported user guide
├── .markdownlint.json                ← Linter config (CHANGELOG convention silencing — v3.6.1)
├── model-guide.md                    ← Model comparison tables + decision flowchart
├── image-models.md                   ← Image model reference + pricing tiers
├── vocab.md                          ← Full platform vocabulary reference
├── prompt-examples.md                ← High-quality example prompts + Before/After pairs
├── photodump-presets.md              ← Photodump mode presets
├── higgsfield_memory.py              ← Memory system script
├── seedance_lint.py                  ← Seedance preflight linter
├── validate.py                       ← Pre-release validation script
├── db/
│   ├── filter-memory.json            ← Content filter memory (seeded)
│   └── quality-memory.json           ← Quality failure memory (seeded)
├── docs/                             ← Extended reference documents
│   └── pdf-audit/                    ← PDF integration audit reports (v3.4.0, v3.6.0)
├── templates/                        ← 10 annotated genre-specific prompt templates
│   ├── 01-cinematic-action-chase.md
│   ├── 02-product-ugc-showcase.md
│   ├── 03-horror-atmosphere.md
│   ├── 04-fashion-editorial.md
│   ├── 05-sci-fi-vfx.md
│   ├── 06-portrait-character-intro.md
│   ├── 07-landscape-establishing-shot.md
│   ├── 08-comedy-social-media.md
│   ├── 09-romantic-intimate.md
│   └── 10-dance-music-performance.md
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
    ├── higgsfield-seedance/SKILL.md      ← Seedance prompt director + content-filter preflight
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

Built February 2026 · v3.6.2 (updated 2026-04-25) · Platform: [higgsfield.ai](https://higgsfield.ai)
