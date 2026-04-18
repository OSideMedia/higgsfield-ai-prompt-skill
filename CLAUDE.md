# CLAUDE.md

## Project Overview

Higgsfield AI Prompt Skill — a Cowork skill library for generating high-quality prompts for Higgsfield's video and image AI models. Includes model selection guides, cinematic vocabulary, prompt examples, genre templates, and a learning memory system.

## Tech Stack

- **Skill format:** Cowork SKILL.md with YAML frontmatter
- **Scripts:** Python 3 (no dependencies beyond stdlib)
- **Data:** JSON databases in `db/`
- **Docs:** Markdown throughout

## Directory Structure

```
SKILL.md                  ← Main dispatcher (routes to sub-skills — start here)
model-guide.md            ← Video + image model comparison tables
image-models.md           ← Image model specs, UI controls, pricing
vocab.md                  ← Camera movement + cinematic vocabulary
prompt-examples.md        ← Production prompt examples by genre
photodump-presets.md      ← 29 Photodump style presets
validate.py               ← Pre-release health checks
higgsfield_memory.py      ← DB operations for learning memory
seedance_lint.py          ← Seedance preflight linter
skills/                   ← 19 sub-skill directories + shared/
templates/                ← 10 genre templates
db/                       ← Filter + quality memory JSON databases
docs/                     ← Extended reference documents
.claude/
  ├── settings.json       ← Permission rules
  ├── rules/              ← Thin pointers to root reference files (no duplication)
  └── commands/           ← /project:validate, /project:release
```

## Key Commands

- `python3 validate.py` — pre-release health check (frontmatter, paths, JSON schemas)
- `python3 higgsfield_memory.py stats` — memory database statistics
- `/project:validate` — run validation via slash command
- `/project:release <version>` — guided version bump + tag + GitHub release

## Rules

- Every SKILL.md must have frontmatter: `name`, `description`, `metadata.version`, `metadata.updated`, `metadata.parent`
- The root SKILL.md is the dispatcher. Sub-skills live in skills/. Never nest the dispatcher under mnt/ — that path is a Claude runtime artifact location, not a skill install path.
- Update `CHANGELOG.md` for every user-facing change
- Run `python3 validate.py` before any release
- Version bumps require a git tag + GitHub release, not just a commit
- Commit format: `feat: vX.Y.Z — description` or `fix: vX.Y.Z — description`
