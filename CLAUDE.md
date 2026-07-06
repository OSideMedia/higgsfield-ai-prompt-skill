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
DISCIPLINE.md             ← Operating discipline (cites HARD RULES by number)
model-guide.md            ← Video + image model comparison tables
image-models.md           ← Image model specs, UI controls, pricing
vocab.md                  ← Camera movement + cinematic vocabulary
prompt-examples.md        ← Production prompt examples by genre
photodump-presets.md      ← 29 Photodump style presets
production-benchmarks.md  ← Iteration/cost benchmarks referenced by templates
scripts/                  ← Python tooling (run from the repo root)
  ├── validate.py         ← Pre-release health checks (--strict for releases)
  ├── higgsfield_memory.py ← DB operations for learning memory
  ├── seedance_lint.py    ← Seedance preflight linter
  ├── sync_specs.py       ← Regenerates specs/ from a models_explore snapshot
  ├── refresh_specs.py    ← Spec-drift tripwire (live CLI vs specs/cli_baseline.json)
  ├── generate_user_guide.py ← Release PDF generator (+ validate_user_guide.py,
  │                         sub_skill_descriptions.py)
  └── build_index.py      ← Regenerates INDEX.md + checks QUICK FACTS anchors
specs/                    ← Machine-readable model specs (generated — never hand-edit;
                            video + image + audio, each generated from a dated
                            models_explore snapshot)
INDEX.md                  ← Generated heading index of every SKILL.md
tests/                    ← pytest suite for the Python tooling (CI-run)
evals/                    ← Behavioral eval cases + run_evals.py (CI-run)
skills/                   ← 30 sub-skill directories + shared/
templates/                ← 10 genre templates + ad-asset-prep.md,
                            character-design/ (6), seedance/ (8), text-overlays/ (3)
db/                       ← Filter + quality memory JSON databases
db/ledger/                ← Generation ledger (one append-only file per project;
                            _global.json generated; see db/ledger/README.md)
docs/                     ← Extended reference documents
workspace/                ← Git-ignored working area (input/ → processed/, output/)
.claude/
  ├── settings.json       ← Permission rules
  ├── rules/              ← Thin pointers to root reference files (no duplication)
  └── commands/           ← /validate, /release
```

## Key Commands

- `python3 scripts/validate.py` — health check (frontmatter, paths, JSON schemas)
- `python3 scripts/validate.py --strict` — release gate (skips become failures)
- `python3 -m pytest tests/ -q` — Python tooling test suite (CI-run)
- `python3 scripts/validate.py --evals` — behavioral eval cases (evals/cases/)
- `python3 scripts/build_index.py` — regenerate INDEX.md after any heading change
- `python3 scripts/sync_specs.py --type video|image|audio` — regenerate specs/ from the newest dated snapshot
- `python3 scripts/refresh_specs.py` — spec-drift tripwire (exit 0 fresh / 3 changed / 1 pull-failed / 4 CLI-shape-changed); `--update-baseline` to accept a reviewed change
- `python3 scripts/higgsfield_memory.py stats` — memory database statistics
- `/validate` — run validation via slash command
- `/release <version>` — guided version bump + tag + GitHub release

## Rules

- The agent-facing operating HARD RULES live in root `SKILL.md` § HARD RULES — pre-delivery checklist, and ONLY there. Do not restate or renumber them here or in `DISCIPLINE.md`; cite them by number (`scripts/validate.py` checks for drift between the three surfaces).
- Every SKILL.md must have frontmatter: `name`, `description`, `metadata.version`, `metadata.updated`. Sub-skills additionally require `metadata.parent: higgsfield`; the root dispatcher has no parent. (`scripts/validate.py` enforces this.)
- Sub-skill `metadata.version` values are **independent** and intentionally out of sync with the root release version (newer surfaces sit at 1.x, legacy ones at 3.x). Do not "fix" them to match the root version — the root SKILL.md frontmatter is the single source of truth for the release version.
- The root SKILL.md is the dispatcher. Sub-skills live in skills/. Never nest the dispatcher under mnt/ — that path is a Claude runtime artifact location, not a skill install path. Every buildable `skills/higgsfield-*/` must be routed from root SKILL.md (`scripts/validate.py` reconciles disk ↔ dispatcher).
- Update `CHANGELOG.md` for every user-facing change
- Release gate: `python3 scripts/validate.py --strict` + `python3 -m pytest tests/ -q` + `python3 scripts/validate.py --evals` — all three green before any release
- Version bumps require a git tag + GitHub release, not just a commit. Full ceremony: `.claude/commands/release.md` (main is protected — tag the **merge commit**; the USER-GUIDE PDF is an untracked release artifact: regenerate → refresh MANIFEST → `gh release upload`; delete release branches after merge)
- Spec refreshes (Tier 2): dump `models_explore` → dated snapshot in `specs/` → `scripts/sync_specs.py` → **audit `evals/cases/` in the same PR** (v3.11.3 lesson) → `scripts/refresh_specs.py --update-baseline`
- Commit format: `feat: vX.Y.Z — description` or `fix: vX.Y.Z — description`
