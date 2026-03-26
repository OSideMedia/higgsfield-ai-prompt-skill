[![Version](https://img.shields.io/badge/version-1.6.0-blue)](https://github.com/OSideMedia/higgsfield-ai-prompt-skill)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Claude%20Cowork%20%7C%20Claude%20Code-purple)](https://github.com/OSideMedia/higgsfield-ai-prompt-skill)

# Higgsfield AI Prompt Skill

A comprehensive Claude skill library for generating high-quality prompts on
[Higgsfield AI](https://higgsfield.ai) — the cinematic video and image generation platform.

## What This Skill Does

Transforms natural language requests into production-ready Higgsfield prompts using:
- The **MCSLA formula** (Model · Camera · Subject · Look · Action)
- Named camera controls and motion presets the platform recognizes
- Model selection guidance across Kling 3.0, Sora 2, Veo 3.1, WAN, Seedance, MiniMax Hailuo, Higgsfield DOP, and more
- Genre recipe templates for action, horror, romance, sci-fi, product ads, and more
- Soul ID character consistency guidance + Character Sheet creation
- Troubleshooting for failed or poor generations
- Cinema Studio 2.5 advanced features: Soul Cast AI actors, built-in color grading, 3D Mode (Gaussian Splatting), Grid Generation, Resolution Settings, Frame Extraction Loop, Object & Person Insertion, Per-Character Emotions, Clustering

## Quick Start

### 1. Claude Cowork (recommended)
Drop the entire repo folder into your Cowork workspace. The main dispatcher is at:
```
mnt/user-data/outputs/higgsfield/SKILL.md
```

### 2. Claude Code
```bash
git clone https://github.com/OSideMedia/higgsfield-ai-prompt-skill
cp -r higgsfield-ai-prompt-skill ~/.claude/skills/higgsfield
```

### 3. Claude.ai Projects
Upload `SKILL.md` (the root-level one) as your project instruction base, then upload the sub-skill files from `mnt/user-data/outputs/higgsfield/skills/` as project documents.

> **Path note:** The `mnt/user-data/outputs/higgsfield/` directory mirrors the Claude Cowork filesystem layout intentionally. If you're using Claude Code or Claude.ai Projects, adapt the paths to your own environment (e.g. `~/.claude/skills/higgsfield/`).

## Structure

```
.
├── SKILL.md                          ← Model selection guide (routes model questions)
├── README.md                         ← This file
├── CHANGELOG.md                      ← Version history
├── model-guide.md                    ← Model comparison tables + decision flowchart
├── image-models.md                   ← Image model reference + pricing tiers
├── vocab.md                          ← Full platform vocabulary reference
├── prompt-examples.md                ← High-quality example prompts + Before/After pairs
├── photodump-presets.md              ← Photodump mode presets
├── higgsfield_memory.py              ← Memory system script
├── db/
│   ├── filter-memory.json            ← Content filter memory (seeded)
│   └── quality-memory.json           ← Quality failure memory (seeded)
└── mnt/user-data/outputs/higgsfield/
    ├── SKILL.md                      ← Main dispatcher (routes to sub-skills — start here)
    └── skills/
        ├── higgsfield-image-shots/SKILL.md   ← Cinematic image prompting (shots, angles, composition) NEW
        ├── higgsfield-prompt/SKILL.md      ← Core MCSLA formula + prompt structure
        ├── higgsfield-models/
        │   ├── SKILL.md                    ← Compact model selection guide
        │   └── MODELS-DEEP-REFERENCE.md    ← Full per-model documentation (on-demand)
        ├── higgsfield-camera/SKILL.md      ← All camera controls + usage
        ├── higgsfield-motion/SKILL.md      ← Named motion presets library
        ├── higgsfield-style/SKILL.md       ← Visual styles + color grades + lighting
        ├── higgsfield-soul/SKILL.md        ← Soul ID character consistency
        ├── higgsfield-audio/SKILL.md       ← Audio prompting (NEW in v1.3.7)
        ├── higgsfield-apps/SKILL.md        ← One-click Apps guide
        ├── higgsfield-recipes/SKILL.md     ← Genre scene templates
        ├── higgsfield-troubleshoot/SKILL.md ← Fix failing generations
        ├── higgsfield-assist/SKILL.md      ← General assistant + platform guidance
        ├── higgsfield-mixed-media/SKILL.md ← Mixed media + hybrid generation
        ├── higgsfield-moodboard/SKILL.md   ← Moodboard creation workflows
        ├── higgsfield-pipeline/SKILL.md    ← Multi-step generation pipelines
        ├── higgsfield-recall/SKILL.md      ← Recall + regeneration patterns
        ├── higgsfield-cinema/SKILL.md      ← Cinema Studio 2.5 (Soul Cast, Color Grading, 3D Mode, Grid Gen, Resolution, Frame Extraction, Object Insertion, Emotions, Clustering)
        └── higgsfield-vibe-motion/SKILL.md ← Vibe-based motion direction
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

Built February 2026 · v1.6.0 (updated March 2026) · Platform: [higgsfield.ai](https://higgsfield.ai)
