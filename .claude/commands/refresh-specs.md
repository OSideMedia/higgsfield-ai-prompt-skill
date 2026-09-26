---
description: Tier-2 spec refresh — dump models_explore (video/image/audio/3d), sync specs, cross-check vs the live CLI, audit evals, gates, accept the CLI baseline
---

The whole Tier-2 refresh as one guided run (CLAUDE.md § Rules → "Spec
refreshes"). Run it when the weekly spec-drift tripwire reports CHANGE, when a
spec snapshot nears 30 days, or on request. Work on a branch, never on `main`.

Hard limits for this command: read-only catalog calls only — `models_explore`
(action=`list`) on the Higgsfield MCP and `higgsfield model list|get`,
`higgsfield --version` on the CLI. Never call a `generate_*` tool or
`higgsfield generate`; nothing here spends credits.

Steps — stop at the first failure and report it:

1. **Dump the catalog, verbatim, per type.** Call `models_explore` with
   action=`list` for each type: `video`, `image`, `audio`, `3d`. Write each
   response UNCHANGED (no reformatting, no trimming) to
   - `specs/models_explore_snapshot_<YYYY-MM-DD>.json` (video)
   - `specs/models_explore_snapshot_<type>_<YYYY-MM-DD>.json` (image / audio / 3d)
   using today's date. **If a response says `has_more: true`, it is one page
   of a paginated list — do not write it as a snapshot.** Fetch the complete
   list; if that is not possible, stop and report (sync_specs.py refuses a
   partial dump anyway).

2. **Sync each type:** `python3 scripts/sync_specs.py --type video` (then
   `image`, `audio`, `3d`). Read the stderr WARN lines: an "unmapped" claim or
   a duration "sentinel" warning means prose the generator would not guess
   at — report each one. New retired ids are printed as "tombstoned" (they
   are appended to `specs/retired-model-ids.json`; never delete entries).

3. **Structural cross-check against the live CLI:**
   `python3 scripts/snapshot_crosscheck.py` (read-only `model list/get`).
   It compares, per model in both sources, every snapshot enum option and
   default with `higgsfield model get --json`, every CLI enum with the
   snapshot, aspect ratios, and media roles. For each `✗ DISAGREE` decide:
   - the snapshot is wrong or incomplete → re-dump (step 1), or
   - it is a known representation difference → add an entry to
     `specs/crosscheck_allowlist.json` naming `model`, `field`, `kind`, the
     date `seen`, and the exact `detail` the checker printed, plus a `note`.
   Remove every entry reported as `STALE`. The check must exit 0 before you
   continue. Known CLI↔MCP disagreements already allowlisted (seen
   2026-09-26): gpt_image_2 defaults (resolution 1k vs 2k, quality low vs
   high), aspect ratios (CLI adds 4:5/5:4/auto) and media roles (`mask`);
   soul_cinematic `soul_id` (MCP-only); role naming `image` (MCP) vs
   `image_references` (CLI) on image_auto, soul_cinematic, image_to_3d,
   multi_image_to_3d, sam_3_3d. Note: the CLI has no `model list --3d`
   flag — 3d rows come from the unfiltered list by their `type` field.

4. **Audit the eval cases for moved models (v3.11.3 lesson):**
   `python3 scripts/sync_specs.py --type <t> --changed` for each type lists
   models added / removed / changed since the previous snapshot and every
   `evals/cases/` entry that names them (by id or display name). Open each
   listed case, check its claims against the new specs, and fix it in the
   same PR.

5. **Gates:** `python3 scripts/validate.py --strict`,
   `python3 -m pytest tests/ -q`, `python3 scripts/validate.py --evals`.
   `--strict` also checks the README specs-snapshot badge and the
   snapshot stamps in `image-models.md` / `photodump-presets.md` — update
   them to the new date if it flags them.

6. **Accept the live CLI surface:**
   `python3 scripts/refresh_specs.py --update-baseline` (read-only CLI
   calls), then `python3 scripts/refresh_specs.py` — it must exit 0 (Fresh).
   If it exits 1, quote its `kind=` and `CLI said:` lines and the remedy;
   exit 4 means the CLI output shape changed (fix the parser, not the auth).

7. **Report:** snapshot files written, model counts per type, added/removed
   models, tombstones added, cross-check result (allowlist changes with
   their reasons), eval cases touched, gate results, baseline capture date.
   Add a CHANGELOG entry and release through `/release`.
