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
sync_specs.py             ← Regenerates specs/ from a models_explore snapshot
specs/                    ← Machine-readable model specs (generated — never hand-edit;
                            video models now, image models TODO pending snapshot)
build_index.py            ← Regenerates INDEX.md + checks QUICK FACTS anchors
INDEX.md                  ← Generated heading index of every SKILL.md
tests/                    ← pytest suite for the Python tooling (CI-run)
skills/                   ← 29 sub-skill directories + shared/
templates/                ← 10 genre templates
db/                       ← Filter + quality memory JSON databases
db/ledger/                ← Generation ledger (one append-only file per project;
                            _global.json generated; see db/ledger/README.md)
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

- The agent-facing operating HARD RULES live in root `SKILL.md` § HARD RULES — pre-delivery checklist, and ONLY there. Do not restate or renumber them here or in `DISCIPLINE.md`; cite them by number (`validate.py` checks for drift between the three surfaces).
- Every SKILL.md must have frontmatter: `name`, `description`, `metadata.version`, `metadata.updated`. Sub-skills additionally require `metadata.parent: higgsfield`; the root dispatcher has no parent. (`validate.py` enforces this.)
- Sub-skill `metadata.version` values are **independent** and intentionally out of sync with the root release version (newer surfaces sit at 1.x, legacy ones at 3.x). Do not "fix" them to match the root version — the root SKILL.md frontmatter is the single source of truth for the release version.
- The root SKILL.md is the dispatcher. Sub-skills live in skills/. Never nest the dispatcher under mnt/ — that path is a Claude runtime artifact location, not a skill install path. Every buildable `skills/higgsfield-*/` must be routed from root SKILL.md (`validate.py` reconciles disk ↔ dispatcher).
- Update `CHANGELOG.md` for every user-facing change
- Run `python3 validate.py` before any release
- Version bumps require a git tag + GitHub release, not just a commit
- Commit format: `feat: vX.Y.Z — description` or `fix: vX.Y.Z — description`
