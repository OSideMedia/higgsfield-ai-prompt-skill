# v3.0.0 Inventory — Cinema Studio 3.0 + Seedance 2.0

Generated: 2026-04-06

---

## File Inventory

### Root Files

| File | Current Version | Needs CS 3.0 | Needs Seedance 2.0 | Notes |
|------|----------------|---------------|---------------------|-------|
| `SKILL.md` | 2.0.2 | ✅ Add to model list | ❌ | Root model selection guide |
| `README.md` | 2.0.2 (badge) | ✅ Version badge, intro, file tree | ❌ | Public-facing |
| `CHANGELOG.md` | — | ✅ v3.0.0 entry | ✅ | Version history |
| `CLAUDE.md` | — | ❌ | ❌ | No model/version refs |
| `CONTRIBUTING.md` | — | ❌ | ❌ | No model/version refs |
| `USER-GUIDE.pdf` | — | ⚠️ PDF — cannot edit directly | ⚠️ | Flag to user |
| `model-guide.md` | — | ✅ Add 3.0 model entry + comparison table | ✅ Remove "(upcoming)" | Root reference |
| `image-models.md` | — | ❌ | ❌ | Image-only models |
| `vocab.md` | — | ❌ | ❌ | Camera vocabulary |
| `prompt-examples.md` | — | ❌ | ❌ | Example prompts |
| `photodump-presets.md` | — | ❌ | ❌ | Photodump presets |
| `validate.py` | — | ❌ | ❌ | Schema checks still valid |
| `higgsfield_memory.py` | — | ❌ | ❌ | No version strings |

### Dispatcher

| File | Current Version | Needs CS 3.0 | Needs Seedance 2.0 | Notes |
|------|----------------|---------------|---------------------|-------|
| `mnt/.../SKILL.md` | 2.0.2 | ✅ Add to routing, "What Is Higgsfield?" | ✅ Remove "(upcoming)" concept | Main dispatcher |

### Core Sub-Skills (Phase 2 targets)

| File | Lines | Current Version | Needs CS 3.0 | Needs Seedance 2.0 | Scope |
|------|-------|----------------|---------------|---------------------|-------|
| `higgsfield-cinema/SKILL.md` | 1,054 | 2.0.2 | ✅ **MAJOR** — Full 3.0 spec section | ❌ | New 3.0 section with specs, comparison table, @ patterns |
| `higgsfield-prompt/SKILL.md` | 250 | 2.0.2 | ❌ | ✅ **MAJOR** — Best practices section | Intent over Precision, Genre Router, I2V Gate, Anti-Slop |
| `higgsfield-camera/SKILL.md` | 184 | 2.0.2 | ✅ Smart Mode docs | ✅ One-Move Rule, genre presets | Camera best practices |
| `higgsfield-motion/SKILL.md` | 208 | 2.0.2 | ❌ | ✅ Intent-first choreography | Motion best practices |
| `higgsfield-style/SKILL.md` | 175 | 2.0.2 | ❌ | ✅ One Style Anchor Rule | Style best practices |
| `higgsfield-audio/SKILL.md` | 239 | 2.0.2 | ✅ **MAJOR** — Native stereo, SCELA | ✅ Remove "(upcoming)", elevate audio | Audio-video joint generation |
| `higgsfield-soul/SKILL.md` | 330 | 2.0.2 | ✅ Soul Cast 3.0 section | ❌ | Character consistency for 3.0 |
| `higgsfield-troubleshoot/SKILL.md` | 160 | 2.0.2 | ❌ | ✅ Diagnostic tree | 6-step troubleshooting for 3.0 engine |

### Other Sub-Skills (unchanged content, version bump only)

| File | Lines | Current Version | Action |
|------|-------|----------------|--------|
| `higgsfield-apps/SKILL.md` | — | 2.0.2 | Version bump only |
| `higgsfield-assist/SKILL.md` | — | 2.0.2 | Version bump only |
| `higgsfield-image-shots/SKILL.md` | — | 2.0.2 | Version bump only |
| `higgsfield-mixed-media/SKILL.md` | — | 2.0.2 | Version bump only |
| `higgsfield-moodboard/SKILL.md` | — | 2.0.2 | Version bump only |
| `higgsfield-pipeline/SKILL.md` | — | 2.0.2 | Version bump only |
| `higgsfield-recall/SKILL.md` | — | 2.0.2 | Version bump only |
| `higgsfield-recipes/SKILL.md` | — | 2.0.2 | Version bump only |
| `higgsfield-vibe-motion/SKILL.md` | — | 2.0.2 | Version bump only |

### Models Sub-Skill

| File | Lines | Current Version | Needs CS 3.0 | Needs Seedance 2.0 | Notes |
|------|-------|----------------|---------------|---------------------|-------|
| `higgsfield-models/SKILL.md` | 197 | 2.0.2 | ✅ Add 3.0 row + flowchart | ✅ Remove "(upcoming)" | Compact model guide |
| `higgsfield-models/MODELS-DEEP-REFERENCE.md` | 14,729+ | 2.0.2 | ✅ Add 3.0 entry | ✅ Remove "(upcoming)" | Full per-model docs; Seedance 2.0 already pre-documented |

### Genre Templates (Phase 3 targets)

| File | Lines | CS Mentions | Seedance Mentions | Action |
|------|-------|-------------|-------------------|--------|
| `01-cinematic-action-chase.md` | 56 | ❌ | ❌ | Add 3.0 genre mapping + prompt length |
| `02-product-ugc-showcase.md` | 57 | ✅ Grid Gen | ❌ | Add 3.0 genre mapping + prompt length |
| `03-horror-atmosphere.md` | 71 | ❌ | ❌ | Add 3.0 genre mapping + prompt length |
| `04-fashion-editorial.md` | 68 | ✅ Creative Tilt | ❌ | Add 3.0 genre mapping + prompt length |
| `05-sci-fi-vfx.md` | 68 | ❌ | ❌ | Add 3.0 genre mapping + prompt length |
| `06-portrait-character-intro.md` | 71 | ✅ Clinical Sharp | ❌ | Add 3.0 genre mapping + prompt length |
| `07-landscape-establishing-shot.md` | 54 | ❌ | ❌ | Add 3.0 genre mapping + prompt length |
| `08-comedy-social-media.md` | 67 | ❌ | ✅ Seedance Pro | Add 3.0 genre mapping + prompt length |
| `09-romantic-intimate.md` | 75 | ❌ | ❌ | Add 3.0 genre mapping + prompt length |
| `10-dance-music-performance.md` | 70 | ❌ | ❌ | Add 3.0 genre mapping + prompt length |

### Shared Resources

| File | Lines | Action |
|------|-------|--------|
| `shared/negative-constraints.md` | 111 | Add no-negative-prompt note for 3.0 + positive alternatives |

### Memory System

| File | Lines | Action |
|------|-------|--------|
| `db/filter-memory.json` | 61 | Model-agnostic — no changes needed |
| `db/quality-memory.json` | 113 | Consider adding Cinema Studio 3.0 quality entry |
| `db/memory-summary.md` | 97 | Regenerate after any JSON changes |
| `higgsfield_memory.py` | 385 | No version strings — unchanged |

### Config / Rules (unchanged)

| File | Action |
|------|--------|
| `.claude/settings.json` | ❌ Unchanged |
| `.claude/settings.local.json` | ❌ Unchanged |
| `.claude/rules/*.md` (5 files) | ❌ Unchanged — thin pointers |
| `.claude/commands/*.md` (2 files) | ❌ Unchanged |

---

## Pre-Existing Issues Found

1. **Seedance 2.0 labeled "(upcoming)"** — appears in: `higgsfield-models/SKILL.md` (lines 40, 94), `MODELS-DEEP-REFERENCE.md` (line 262), `model-guide.md` (lines 19, 104), `higgsfield-audio/SKILL.md` (lines 24, 185–191). All need "(upcoming)" removed.
2. **Seedance 2.0 in negative-constraints.md** — line 67 references lip-sync constraints but does NOT have "(upcoming)" label — already consistent.
3. **Seedance 2.0 in filter-memory.json** — entry F-004 references face upload blocking — content-accurate, no change needed.
4. **USER-GUIDE.pdf** — binary PDF, cannot be edited. User will need to regenerate from source after v3.0.0 changes.

---

## Summary

| Category | Files | Need Content Changes | Version Bump Only | Unchanged |
|----------|-------|---------------------|-------------------|-----------|
| Root docs | 13 | 4 (README, CHANGELOG, SKILL.md, model-guide.md) | 0 | 9 |
| Dispatcher | 1 | 1 | 0 | 0 |
| Core sub-skills | 8 | 8 | 0 | 0 |
| Other sub-skills | 9 | 0 | 9 | 0 |
| Models sub-skill | 2 | 2 | 0 | 0 |
| Genre templates | 10 | 10 | 0 | 0 |
| Shared resources | 1 | 1 | 0 | 0 |
| Memory system | 4 | 1 (quality-memory.json) | 0 | 3 |
| Config/rules | 8 | 0 | 0 | 8 |
| **Total** | **56** | **27** | **9** | **20** |
