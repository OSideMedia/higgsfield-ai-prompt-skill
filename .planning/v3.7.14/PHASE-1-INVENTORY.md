# v3.7.14 — Phase 1 Locked Sub-Skill Draft Inventory

**Date:** 2026-05-18
**Carry-forward from Phase 0:** Option B holds, font target = DejaVu Sans Condensed (DVC), descope path closed.
**Convention:** `.planning/<version>/PHASE-1-INVENTORY.md` per v3.7.13-established pattern.

---

## §1A — File-by-file change inventory

Every file touched by v3.7.14, ordered roughly by Phase 2 sequencing. Line-count estimates are conservative ceilings — actual diffs may be smaller.

### NEW: `assets/fonts/` directory + 3 TTF files

- `assets/fonts/DejaVuSansCondensed.ttf` — 668 KB binary (regular)
- `assets/fonts/DejaVuSansCondensed-Bold.ttf` — 652 KB binary
- `assets/fonts/DejaVuSansCondensed-Oblique.ttf` — 588 KB binary
- `assets/fonts/README.md` — **NEW**, ~15 lines. Documents:
  - Bundled font source (DejaVu Fonts v2.37 official tarball, GitHub release URL)
  - Why bundled (no system install on user machines guaranteed; ensures deterministic PDF regeneration across environments)
  - License — Bitstream Vera + public domain (redistribution allowed; see file header in TTFs)
  - Why DVC over DV regular — points at `.planning/v3.7.14/PHASE-0-VERIFICATION.md` §VERIFY 0.3

**Total bundled weight:** ~1.9 MB. Under Phase 0's 5 MB threshold.

### MODIFIED: `generate_user_guide.py` (1258 lines → ~1290 lines)

Estimated ~30 LoC net addition across 5 change clusters:

1. **Top-of-file imports + font setup (~6 LoC, new)**
   - Add `from pathlib import Path` near existing import block (or extend if already there — check at edit time)
   - Add `FONT_DIR = Path(__file__).resolve().parent / "assets" / "fonts"` constant
   - No imports beyond `Path`; FPDF object handles add_font internally

2. **`build_pdf()` font registration (~3 LoC, new — inserted just after `pdf = HiggsfieldPDF()` ctor at L208-ish)**
   ```python
   pdf.add_font("Body", "",  str(FONT_DIR / "DejaVuSansCondensed.ttf"))
   pdf.add_font("Body", "B", str(FONT_DIR / "DejaVuSansCondensed-Bold.ttf"))
   pdf.add_font("Body", "I", str(FONT_DIR / "DejaVuSansCondensed-Oblique.ttf"))
   ```
   Family alias `"Body"` chosen so the swap is a single find-replace from `"Helvetica"` → `"Body"`. `"Courier"` stays as-is (ASCII-only code blocks; D1 carry-forward + Phase 0 §VERIFY 0.1 open-question close-out).

3. **`set_font("Helvetica", ...)` swap to `set_font("Body", ...)` (~30 sites, mechanical replace)**
   - L100, L105, L112, L122, L129, L135, L141, L163, L173, L183, L188, L191, L196, L214, L218, L223, L232, L267, L272, L1249 (plus any others surfaced by grep)
   - All are pure family-name swaps; no point-size or style-string changes
   - Per Phase 2 visual-checkpoint, body point-size 0.5pt bump remains a deferred option pending readability spot-check

4. **`--dry-run` flag (~12 LoC, new — replaces the L1257-1258 `__main__` block)**
   ```python
   def build_pdf(dry_run: bool = False):
       ...                                  # existing body unchanged
       if dry_run:
           print(f"DRY-RUN: pipeline OK ({pdf.page_no()} pages). Output NOT written.")
           return
       pdf.output("docs/user-guide/USER-GUIDE.pdf")
       print(f"Generated docs/user-guide/USER-GUIDE.pdf ({pdf.page_no()} pages)")

   if __name__ == "__main__":
       import argparse
       parser = argparse.ArgumentParser(description="Regenerate USER-GUIDE.pdf.")
       parser.add_argument(
           "--dry-run",
           action="store_true",
           help="Run dict-parity + full PDF render pipeline in-memory without writing the output file.",
       )
       args = parser.parse_args()
       build_pdf(dry_run=args.dry_run)
   ```
   Per Phase 0 §VERIFY 0.5 confirmed-no-refactor: `pdf.output(...)` at L1253 is the only file-write site; gating is one-line.

5. **Section 24 marketing-studio row** — **NO MANUAL EDIT NEEDED.**
   - Section 24 layout (verified L1167-1204):
     - Line 1167: `pdf.section_title("24. Repository Contents")`
     - Line 1168: `pdf.subsection_title("Root Files")` — hardcoded 11-file table at L1171-1183
     - Line 1200: `pdf.subsection_title(f"Sub-Skills ({len(SUB_SKILL_DESCRIPTIONS)} total)")` — **auto-generated** from `SUB_SKILL_DESCRIPTIONS` dict at L1203-1204
   - `higgsfield-marketing-studio` was already added to `SUB_SKILL_DESCRIPTIONS` at L85 in v3.7.13: `"Marketing Studio - 9 ad presets + 4-15s video + cross-surface"` (60 chars, DVC-safe per Phase 0 §VERIFY 0.3 utilization table = 77.5% of column).
   - **Row will surface in regenerated PDF as a byproduct of running `generate_user_guide.py`** — the v3.7.13 deferral closes mechanically when the PDF regenerates against the existing dict state. No code edit required for the marketing-studio row itself.
   - Phase 1 §1B below documents this finding + a separate flag for the PR #36 Root Files staleness item.

### MODIFIED: `validate_user_guide.py` (240 lines → ~241 lines)

Estimated ~2 LoC change + docstring update:

1. **L98 — `DEFAULT_BASELINE` retarget (1 LoC)**
   ```python
   DEFAULT_BASELINE = REPO / "docs" / "user-guide" / "USER-GUIDE.pdf.baseline-v3.7.14"
   ```
2. **L85 — docstring `Defaults:` block update (1 LoC, prose)**
   ```python
   #   baseline_path  = docs/user-guide/USER-GUIDE.pdf.baseline-v3.7.14
   ```
3. **Optional docstring note on font swap (~3 LoC, prose)** — under VALIDATION LAYERS, add a line clarifying Layer 1 is rendering-agnostic per Phase 0 §VERIFY 0.4 finding. Phase 1 recommendation: include this note; it future-proofs against an ambiguous reader question ("does font swap break this validator?"). Flag for user to confirm at Phase 2 STOP.

**No Layer 1 normalization changes** per Phase 0 §VERIFY 0.4 locked decision (D3).
**No Layer 0 ceiling change** — `SUB_SKILL_DESCRIPTION_CEILING = 71` stays valid under DVC.

### NEW: `docs/user-guide/USER-GUIDE.pdf.baseline-v3.7.14`

- Byte-for-byte copy of the freshly regenerated `docs/user-guide/USER-GUIDE.pdf` after Phase 2 confirms the regeneration is clean.
- Phase 2D step: `cp docs/user-guide/USER-GUIDE.pdf docs/user-guide/USER-GUIDE.pdf.baseline-v3.7.14`
- Tracked in git per v3.7.0-established baselines-accumulate convention.

### RETAINED (no edit): `docs/user-guide/USER-GUIDE.pdf.baseline-v3.7.12`

- Baselines accumulate; v3.7.12 retained alongside v3.7.14.
- v3.7.13 was a no-PDF-regen release so it produced no baseline file — natural gap.
- v3.7.0 through v3.7.7 baselines also retained (see existing `docs/user-guide/` directory).

### REGENERATED: `docs/user-guide/USER-GUIDE.pdf`

- Current: 52,711 bytes (helvetica + v3.7.13 metadata, marketing-studio row missing because PDF was reverted in v3.7.13 per its Phase 1 scope decision).
- Post-v3.7.14: ~115 KB-ish estimate (DVC fonts subset-embedded adds bytes; em-dashes/Unicode render natively; 22nd sub-skill row added). Exact size emerges during Phase 2C.
- Layer 2 binary diff against v3.7.12 baseline will report MANY byte diffs (informational only — font subset structure changes).
- Layer 1 text-extract diff against v3.7.14 baseline (the new one we copy in Phase 2D): **byte-identical** after the copy step; passes by construction.

### MODIFIED: Root `SKILL.md`

- Frontmatter L15: `version: 3.7.13` → `version: 3.7.14`
- Frontmatter L16: `updated: 2026-05-18` → updated to Phase 3 ship date (same-day cascade per v3.7.10/11/12/13 pattern)

### MODIFIED: `README.md`

- L1: badge `version-3.7.13` → `version-3.7.14`
- L262: footer `v3.7.13 (updated 2026-05-18)` → `v3.7.14 (updated <ship-date>)`

### MODIFIED: `CHANGELOG.md`

- New top entry per §1C framing below. Estimated ~50-80 lines of new content.

### TOTAL DELTA SUMMARY

| Category                       | Files | LoC estimate | Notes |
|--------------------------------|-------|--------------|-------|
| New (TTF binaries)             | 3     | binary       | ~1.9 MB |
| New (README, baseline)         | 2     | ~15 + binary | bundle docs + new PDF baseline |
| Modified (code)                | 2     | ~32          | generate_user_guide.py + validate_user_guide.py |
| Modified (metadata)            | 3     | ~5           | SKILL.md, README.md, CHANGELOG.md (header lines only) |
| Modified (changelog content)   | 1     | ~80          | CHANGELOG.md body |
| Regenerated (binary)           | 1     | binary       | USER-GUIDE.pdf |

---

## §1B — Section 24 row content for higgsfield-marketing-studio

**Conclusion: NO manual row edit needed for the marketing-studio row.**

### Verification trail

`generate_user_guide.py` L1167-1204 (Section 24 "Repository Contents") contains two subsections:

| Subsection | Structure | marketing-studio handling |
|------------|-----------|---------------------------|
| 24.1 "Root Files" (L1168-1185) | Hardcoded `root_files = [...]` list of 11 root-level files (SKILL.md, README.md, CHANGELOG.md, USER-GUIDE.pdf, DISCIPLINE.md, model-guide.md, image-models.md, vocab.md, prompt-examples.md, photodump-presets.md, production-benchmarks.md) | N/A — `skills/higgsfield-marketing-studio/` is a sub-skill directory, NOT a root file |
| 24.2 "Sub-Skills (N total)" (L1200-1204) | Auto-generated: `for name, desc in SUB_SKILL_DESCRIPTIONS.items(): pdf.table_row([name, desc], w14)` | **Already covered** — `SUB_SKILL_DESCRIPTIONS["higgsfield-marketing-studio"] = "Marketing Studio - 9 ad presets + 4-15s video + cross-surface"` at L85 (added v3.7.13) |

**Mechanism:** v3.7.13 added the dict entry but reverted the PDF post-validation (see CHANGELOG L73: *"PDF not regenerated this release"*). v3.7.14's PDF regeneration in Phase 2C surfaces the row naturally — it's a side-effect of running `generate_user_guide.py`, not a separate edit.

### Marketing-studio row text (already locked from v3.7.13)

| Column 1 (`name`)                | Column 2 (`desc`) — 60 chars                                  |
|----------------------------------|---------------------------------------------------------------|
| `higgsfield-marketing-studio`    | `Marketing Studio - 9 ad presets + 4-15s video + cross-surface` |

DVC utilization at 9pt: 77.5% of the 115mm column (per Phase 0 §VERIFY 0.3 real-text table) — comfortable margin.

### Phase 2C verification step

After PDF regeneration, eyeball-confirm the row renders:
- Located between `higgsfield-cinema` (the previous-last topical-cluster entry) and `higgsfield-recall` (per v3.7.13 dict ordering — topical-insertion, not alphabetical)
- Total row count = 22 (matches v3.7.13's count; no further dict additions in v3.7.14)
- Renders inside column boundary (DVC drift = 0.6% from Helvetica on this string per Phase 0 §VERIFY 0.3)

### Adjacent observation — flag-don't-decide for user

The Root Files table at L1175 contains:
```python
("USER-GUIDE.pdf", "This document"),
```
Per memory note `project_user_guide_section22_staleness.md`: after PR #36's `docs/user-guide/` directory move (v3.7.7 chore), `USER-GUIDE.pdf` no longer lives at repo root — it lives at `docs/user-guide/USER-GUIDE.pdf`. The Root Files row is therefore mildly stale.

**Three handling options** (NOT in v3.7.14 locked scope; flagged for user awareness):
- **(i)** Update to `("docs/user-guide/USER-GUIDE.pdf", "This document")` — accurate, ~2-char drift, safe under DVC (well below 60-char column-utilization regime per Phase 0 §VERIFY 0.3).
- **(ii)** Remove the row — the user is reading the PDF so its location is implicit; removal preserves Root Files as a literal repo-root listing.
- **(iii)** Keep as-is — v3.7.14 scope is locked elsewhere; defer to a later release.

**Phase 1 recommendation:** flag in user-review during Phase 2B STOP. The Root Files table is right next to the auto-generated Sub-Skills table; the diff review window naturally surfaces it. Cheap to fix at that moment if the user wants to; equally cheap to defer.

---

## §1C — CHANGELOG framing (v3.7.14 entry sketch)

Editorial through-line: **infrastructure hardening**. v3.7.10 → v3.7.11 → v3.7.12 → v3.7.13 ran the "plausibility-over-verification" arc at four increasing levels of recursion. v3.7.14 doesn't extend that recursion — it closes the verification gap the recursion exposed. Different through-line, same release-arc continuity.

### Proposed top-of-CHANGELOG.md entry

```markdown
## v3.7.14 — <ship-date>

Infrastructure-hardening patch release. Closes the verification gap that the
v3.7.12 RuntimeError and v3.7.13 em-dash crash both exposed: latent rendering
bugs in `generate_user_guide.py` that `validate.py` couldn't catch because
the rendering pipeline only runs on full PDF regeneration.

Option B scope per Phase 0 lock — three coupled items plus natural fallout:

1. `--dry-run` flag on `generate_user_guide.py` — runs the dict-parity check
   and full `build_pdf()` rendering pipeline in-memory without writing the
   output file. Callable as a pre-ship smoke test; eligible for invocation
   from `validate.py` in a future release as a standard pre-release check.

2. FPDF Unicode font swap from Helvetica (latin-1 core) to DejaVu Sans
   Condensed (DVC, Unicode TTF, bundled in `assets/fonts/`). Closes the
   em-dash constraint that bit v3.7.13's `SUB_SKILL_DESCRIPTIONS` entry
   for `higgsfield-marketing-studio` (workaround at the time: keep ASCII
   only). Now em-dashes, en-dashes, curly quotes, ellipses, and arbitrary
   non-ASCII glyphs render natively.

3. Section 24 sub-skill row for `higgsfield-marketing-studio` — deferred
   from v3.7.13 per its Phase 1 scope (the dict entry shipped but the
   PDF was not regenerated). Surfaces automatically in v3.7.14's
   regeneration via the existing auto-generated Sub-Skills table.

Natural fallout:
- USER-GUIDE.pdf fully regenerated with DVC + the new sub-skill row
- New baseline `docs/user-guide/USER-GUIDE.pdf.baseline-v3.7.14`
  replaces v3.7.12 as `validate_user_guide.py`'s diff target

### Infrastructure hardening — the verification gap

Two prior releases ran latent rendering bugs into PDF generation that
`validate.py` had no way to catch:

- **v3.7.12** — frontmatter parser raised `RuntimeError` at PDF render
  time when a required field was missing, AFTER `validate.py` passed clean.
  `validate.py` was checking structural integrity of inputs; the renderer
  was the only thing that exercised the cross-input contract.
- **v3.7.13** — `SUB_SKILL_DESCRIPTIONS` accepted a Unicode em-dash that
  `build_pdf()` then crashed on at L1204 (`FPDFUnicodeEncodingException`
  from helvetica latin-1). `validate.py` passed clean; `validate_user_guide.py`
  passes clean; rendering pipeline crashed only when actually run.

Both bugs surfaced post-merge during the ship-time regeneration cascade,
forcing same-day fix commits in the same release the bug was named. The
two-step `validate.py` + `generate_user_guide.py` sequence was doing
real verification work, but the rendering pipeline invocation was
outside `validate.py`'s scope.

v3.7.14's `--dry-run` flag formalizes the rendering pipeline as a
verification surface — invokable as `python3 generate_user_guide.py
--dry-run` to run the full pipeline (frontmatter parse, dict-parity
check, `build_pdf()` rendering, font subsetting, layout) without
writing the output file. The em-dash class of bug now crashes at
the dry-run step, not at ship time. Eligible for `validate.py`
integration in a future release.

### Font upgrade — DejaVu Sans Condensed (DVC) over DV regular

Phase 0 verification (`.planning/v3.7.14/PHASE-0-VERIFICATION.md`)
surfaced that DejaVu Sans regular has 11-18% glyph-width drift versus
helvetica — wide enough that one existing `SUB_SKILL_DESCRIPTIONS`
entry (`higgsfield-cinema`, 71 chars at the empirical ceiling) would
overflow the 115mm Section 24 column under DV regular. The user-stated
descope criterion ("if column-width drift exceeds ~5%, flag for descope
consideration") fired.

DejaVu Sans Condensed solves both problems: Unicode support equivalent
to DV regular, while drift on real `SUB_SKILL_DESCRIPTIONS` content stays
at 0.6-2.8% (worst case 6.4% on a synthetic 71×'x' string). Zero existing
entries overflow. `SUB_SKILL_DESCRIPTION_CEILING = 71` stays valid in
`validate_user_guide.py` Layer 0. The font-family substitution is the
discipline of accepting Phase 0's evidence over the original assumption,
not a scope change — same family, same Unicode coverage, same goal.

### .planning/<version>/ convention — inherited from v3.7.13

v3.7.13 introduced the `.planning/<version>/PHASE-N-*.md` convention
for per-release verification artifacts. v3.7.14 inherits it cleanly:

- `.planning/v3.7.14/PHASE-0-VERIFICATION.md` — five-check probe report
  (font availability, FPDF API, glyph drift, validator normalization,
  dry-run scope) with descope-criterion calibration
- `.planning/v3.7.14/PHASE-1-INVENTORY.md` — locked sub-skill draft
  inventory (this CHANGELOG entry is §1C of it)

Path convention from sub-skill files: `../../.planning/<version>/<filename>`.

### Added

- **NEW `assets/fonts/`** directory bundling DejaVu Sans Condensed TTFs
  (regular, bold, oblique). License: Bitstream Vera + public domain
  (redistribution OK). Total ~1.9 MB. Source:
  `https://github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/`.
- **NEW `assets/fonts/README.md`** documenting source, license, and the
  DVC-over-DV-regular rationale (points at `PHASE-0-VERIFICATION.md`).
- **NEW `--dry-run` flag** on `generate_user_guide.py`. Invocation:
  `python3 generate_user_guide.py --dry-run`. Exits 0 on clean pipeline,
  non-zero on any pipeline-level failure (frontmatter parse, dict-parity,
  font registration, rendering). Skips file write.
- **NEW `docs/user-guide/USER-GUIDE.pdf.baseline-v3.7.14`** baseline file.

### Changed

- **`generate_user_guide.py`** — DejaVu Sans Condensed registered as
  font family alias `"Body"`; all `set_font("Helvetica", ...)` call
  sites swapped to `set_font("Body", ...)`. `Courier` retained for
  code blocks (ASCII-only content; no Unicode pressure observed).
  `build_pdf()` gains optional `dry_run: bool = False` parameter;
  `__main__` block gains argparse with `--dry-run`. Section 24
  Sub-Skills table now lists 22 entries (was 21 in last-regenerated
  v3.7.12 baseline) — `higgsfield-marketing-studio` row surfaces
  via the existing auto-generated table from the v3.7.13-added dict
  entry.
- **`validate_user_guide.py`** — `DEFAULT_BASELINE` retargeted from
  `USER-GUIDE.pdf.baseline-v3.7.12` to `USER-GUIDE.pdf.baseline-v3.7.14`.
  Docstring `Defaults:` block updated. Layer 1 normalization unchanged;
  Layer 0 `SUB_SKILL_DESCRIPTION_CEILING = 71` unchanged.
- **`docs/user-guide/USER-GUIDE.pdf`** — regenerated with DVC + the
  marketing-studio Sub-Skills row + v3.7.14 metadata cascade.
- **Root `SKILL.md`** — frontmatter `version: 3.7.13` → `3.7.14`;
  `updated:` to <ship-date>.
- **`README.md`** — version badge (L1) and footer (L262) cascade.

### Verification

- Phase 0 verification report at `.planning/v3.7.14/PHASE-0-VERIFICATION.md`
  documents the five-check probe trail. DVC glyph drift measured against
  every existing `SUB_SKILL_DESCRIPTIONS` entry; zero overflows.
- `python3 validate.py` — ALL CHECKS PASSED.
- `python3 generate_user_guide.py --dry-run` — exits 0 (smoke-test
  validation of the new flag itself); confirms the dict-parity +
  font-registration + render pipeline runs clean before file write.
- `python3 generate_user_guide.py` — exits 0; PDF regenerated.
- `python3 validate_user_guide.py` against v3.7.14 baseline — VALIDATION
  PASSED. Layer 0: all 22 entries ≤ 71 chars (longest still
  `higgsfield-cinema` at 71). Layer 1: byte-identical (candidate copied
  from baseline file). Layer 2: byte-identical.

### Backlog closures

Two items from v3.7.13's CHANGELOG `### Backlog` subsection close in v3.7.14:

- **CLOSED: USER-GUIDE.pdf Unicode font upgrade** (v3.7.13 backlog) —
  DVC swap replaces helvetica latin-1. Em-dashes and arbitrary Unicode
  body content now render. The workaround constraint ("dict descriptions
  and PDF body content must be ASCII-only") lifts. The constraint remains
  documented in `assets/fonts/README.md` historically; the constraint
  in production is now Courier-specific (code blocks) and naturally
  ASCII per existing convention.
- **CLOSED: `validate.py` → `generate_user_guide.py` pre-ship sequence
  formalization** (v3.7.13 backlog) — `--dry-run` flag delivers the
  flagged piece (a runnable rendering-pipeline smoke test). `validate.py`
  integration is the natural next step (subprocess-invoke `generate_user_guide.py
  --dry-run`; assert return code 0); flagged for a future release where
  the integration earns its own scope.
- **CLOSED: USER-GUIDE.pdf Section 24 row for `skills/higgsfield-marketing-studio/`**
  (v3.7.13 backlog) — surfaces in regenerated PDF as the natural
  byproduct of the v3.7.13 `SUB_SKILL_DESCRIPTIONS` dict entry meeting
  v3.7.14's regeneration cascade.

### Backlog (forward-looking)

- **`validate.py` integration of `generate_user_guide.py --dry-run`**
  — split-off from this release's `--dry-run` scope. Adds a
  `check_user_guide_renders()` function that subprocesses the dry-run
  invocation; folds into `validate.py`'s standard pre-release health
  check. Estimated ~10 LoC; deferred to a release where it earns
  its own scope rather than ride coattails.
- **Section 24 "Root Files" row staleness** — `USER-GUIDE.pdf` row
  in the hardcoded Root Files table at `generate_user_guide.py:1175`
  still implies repo-root location; after PR #36's `docs/user-guide/`
  directory move (v3.7.7), it lives at `docs/user-guide/USER-GUIDE.pdf`.
  Three handling options documented in `.planning/v3.7.14/PHASE-1-INVENTORY.md`
  §1B. Flag-don't-decide for v3.7.14; awaiting user direction.
- **Courier → DejaVu Sans Mono swap** — `generate_user_guide.py:149`
  still uses Courier (latin-1 core) for code blocks. Same Unicode
  constraint applies in principle; not exercised in practice (code
  blocks are CLI commands, paths, dict keys — all ASCII by convention).
  Defer until a code block ever needs a non-ASCII glyph.
- **`--dry-run` exit-code matrix documentation** — `--dry-run` is
  binary (exit 0 / non-zero) in v3.7.14. A future release could
  distinguish frontmatter errors (exit 2), dict-parity errors (exit
  3), rendering errors (exit 4) for finer-grained CI integration.
  Deferred — current binary contract is sufficient for the
  `validate.py` integration target.
```

### Editorial note

The CHANGELOG above is a SKETCH for Phase 2E composition. Per discipline,
the actual text gets shaped by what Phase 2A-2D surface — section
numbering, exact LoC counts, ship date, any spot-check decisions.
The structure (Option B headline → Infrastructure hardening section →
Font upgrade section → .planning convention section → Added/Changed/
Verification/Backlog) is locked; the prose is draft.

---

## §1D — Sub-phase 2 ordering with STOPs

Standard v3.7.x pattern. Seven sub-phases, four STOPs.

### 2A. Bundle DVC fonts in `assets/fonts/`

**What:** Create `assets/fonts/` directory; copy three DVC TTFs from `/tmp/dejavu-test/dejavu-fonts-ttf-2.37/ttf/`; author `assets/fonts/README.md`.

**Why this first:** Other steps depend on the font files existing. Pure file-copy + small markdown write — mechanical, low-risk.

**Pass criteria:** `ls assets/fonts/` shows the three TTFs + README.md; no other files. Git status reflects the four new files.

**STOP after:** No (mechanical step; chain into 2B).

### 2B. Modify `generate_user_guide.py`

**What:** Apply the five change clusters from §1A:
- Top-of-file: `from pathlib import Path` + `FONT_DIR` constant
- `build_pdf()` font registration (3 `add_font` calls)
- 30-ish `set_font("Helvetica", ...)` → `set_font("Body", ...)` swaps
- `--dry-run` flag (argparse + `dry_run` parameter + output() gating)
- Section 24: verify no manual edit needed (already covered by §1B finding)

**Why before regeneration:** The next sub-phase regenerates the PDF — needs the source changes in place first.

**Pass criteria:** `python3 -c "import generate_user_guide"` clean import; `python3 generate_user_guide.py --dry-run` exits 0; no `set_font("Helvetica", ...)` remains in the file (`grep -c 'set_font("Helvetica"' generate_user_guide.py` returns 0).

**STOP after:** **YES.** User reviews the diff before regeneration commits the rendering output to disk.

### 2C. First PDF regeneration + visual spot-check (Phase 0 visual checkpoint)

**What:**
- Run `python3 generate_user_guide.py` (writes `docs/user-guide/USER-GUIDE.pdf`).
- Open the regenerated PDF; read 2-3 pages of body prose at typical reading distance.
- Compare against the v3.7.13 baseline PDF (helvetica) — specifically `USER-GUIDE.pdf.baseline-v3.7.12` (most recent helvetica baseline) for the same-content reference window.
- Decision per Phase 0 visual-checkpoint criteria:
  - DVC reads cleanly → ship as-is; proceed to 2D
  - DVC reads as too narrow/cramped → bump body-text point size up 0.5pt (single edit at `body_text` method, L129: `self.set_font("Body", "", 10)` → `... 10.5)`); re-regenerate; re-spot-check
  - 0.5pt bump still reads poorly → fallback to mixed-font (DVC for tables/dict entries via separate family alias, DV regular for body via "Body" family); larger refactor, surface for explicit user decision before proceeding

**Why before validator re-baseline:** The new baseline file is a byte-for-byte copy of the regenerated PDF. If readability requires a 0.5pt bump or mixed-font fallback, the baseline copy happens AFTER those decisions land — otherwise the baseline locks in a layout that gets immediately overwritten.

**Pass criteria:** Readability spot-check produces an explicit user verdict (clean / 0.5pt bump / mixed-font fallback). The PDF on disk is the one matching the verdict.

**STOP after:** **YES.** Visual approval required. This is the gate Phase 0 explicitly added to v3.7.14.

### 2D. Validator re-baseline

**What:**
- `cp docs/user-guide/USER-GUIDE.pdf docs/user-guide/USER-GUIDE.pdf.baseline-v3.7.14`
- Edit `validate_user_guide.py:98` to retarget `DEFAULT_BASELINE`
- Edit `validate_user_guide.py:85` docstring `Defaults:` line
- Optional docstring note (flagged in §1A item 3) on font-swap rendering-agnosticism

**Why after spot-check:** Baseline locks in the readability decision. No baseline before user-approved layout.

**Pass criteria:** `python3 validate_user_guide.py` against new baseline — Layer 0 PASS (22 entries ≤ 71 chars); Layer 1 PASS (byte-identical after the cp); Layer 2 PASS (byte-identical).

**STOP after:** No (mechanical; chain into 2E).

### 2E. Version cascade

**What:**
- Root `SKILL.md` frontmatter: `version: 3.7.13` → `3.7.14`; `updated:` to ship date
- `README.md` L1 badge: `version-3.7.13` → `version-3.7.14`
- `README.md` L262 footer: `v3.7.13 (updated 2026-05-18)` → `v3.7.14 (updated <ship-date>)`
- `CHANGELOG.md` top entry per §1C sketch — actual prose shaped by what 2A-2D surfaced

**Why before final validation:** `validate.py` reads SKILL.md frontmatter; baseline regeneration would re-fire if the SKILL.md changes were made after. Frontmatter-before-regen convention per memory `feedback_release_workflow.md` v3.7.6 mega-release notes.

**Wait — frontmatter-before-regen needs revisiting here.** v3.7.6's convention was for content-change releases where the PDF cover page prints the version. For v3.7.14, the PDF was already regenerated in 2C — if `META['version']` reads from SKILL.md frontmatter (which Path B refactor in v3.7.0 made it do), then 2C regenerated with version `3.7.13` STILL embedded in the PDF cover page and footer.

**Correction:** 2E should run BEFORE 2C, not after. Reordered ordering below.

**Pass criteria:** SKILL.md, README.md, CHANGELOG.md all bear `3.7.14` and the ship date.

**STOP after:** **YES.** User reviews the CHANGELOG entry before final validation.

### 2F. Full validation pass

**What:**
- `python3 validate.py` — pre-release health check (frontmatter, paths, JSON schemas)
- `python3 generate_user_guide.py --dry-run` — pipeline smoke test (validates the new flag itself + confirms no regression in pipeline)
- `python3 validate_user_guide.py` — Layer 0/1/2 check against v3.7.14 baseline

**Pass criteria:** All three exit 0. Layer 0 22 entries / 71 ceiling. Layer 1 byte-identical. Layer 2 byte-identical.

**STOP after:** **YES.** Final diff review before Phase 3 ship.

### 2G. Final repo-wide diff review

**What:** `git status` + `git diff` audit before Phase 3 (commit + tag + GitHub release).

**Pass criteria:** All changes accounted for in §1A inventory; no surprise modifications.

**STOP after:** N/A (this IS the gate before Phase 3).

### Corrected sub-phase ordering (frontmatter-before-regen applied)

Reading memory note `feedback_release_workflow.md` literally: *"v3.7.6 added mega-release additions (frontmatter-before-regen, baselines accumulate, validate.py registration, …)"*. Frontmatter must update BEFORE the PDF regenerates because the PDF embeds version metadata.

**Final ordering:**

| Step | Name | STOP after? |
|------|------|-------------|
| 2A | Bundle DVC fonts in `assets/fonts/` | No |
| 2B | Modify `generate_user_guide.py` (code changes) | **STOP — diff review** |
| 2C | Version cascade (SKILL.md / README.md / CHANGELOG.md frontmatter + cascade) | **STOP — CHANGELOG review** |
| 2D | First PDF regeneration + visual spot-check (readability decision) | **STOP — visual approval** |
| 2E | Validator re-baseline (cp + DEFAULT_BASELINE edit + docstring) | No |
| 2F | Full validation pass (validate.py + dry-run + validate_user_guide.py) | **STOP — final review** |
| 2G | Final repo-wide diff audit | N/A — gate to Phase 3 |

Four STOPs (2B / 2C / 2D / 2F). 2C reordered ahead of 2D per frontmatter-before-regen convention. CHANGELOG body lands at 2C with version-cascade in the same edit; the prose is rough at that point but the structure is locked from §1C. Visual approval and readability decision (2D) happen against the version-correct PDF — no re-regeneration needed unless the readability decision requires it.

---

## §1E — Decisions register

Format inherits v3.7.13's decisions-register pattern (DECISION N: name, source, applied to).

### Phase 0 locked decisions (carry-forward)

| ID | Decision | Source | Applied to |
|----|----------|--------|------------|
| **D1** | Font target = DejaVu Sans Condensed (DVC). Bundle `assets/fonts/DejaVuSansCondensed*.ttf` (regular, Bold, Oblique) — ~1.9 MB. Document bundling rationale in `assets/fonts/README.md`. | Phase 0 §VERIFY 0.1 + 0.3 ; user lock | 2A bundle step + `generate_user_guide.py` `add_font` calls in 2B |
| **D2** | FPDF API: fpdf2 v2.8.7. `add_font(family, style, fname=...)` + `set_font(family, style, size)`. No pinning required. | Phase 0 §VERIFY 0.2 ; user lock | 2B font registration |
| **D3** | Validator: `validate_user_guide.py` `DEFAULT_BASELINE` retarget v3.7.12 → v3.7.14. No Layer 1 normalization changes. No Layer 0 ceiling change. | Phase 0 §VERIFY 0.4 ; user lock | 2E validator re-baseline |
| **D4** | `--dry-run` flag: ~10 LoC. argparse + `dry_run: bool = False` parameter on `build_pdf()`. Single `pdf.output()` call gates cleanly. No `build_pdf()` refactor. | Phase 0 §VERIFY 0.5 ; user lock | 2B `--dry-run` cluster |
| **D5** | Probe artifacts: `/tmp/dejavu-test/` is scratch space. Discard after Phase 1. `.planning/v3.7.14/PHASE-0-VERIFICATION.md` is the durable artifact. | User lock | §1F |
| **D6** | Phase 2C visual spot-check checkpoint. DVC readability decision: clean / 0.5pt bump / mixed-font fallback. Placed BEFORE validator re-baseline. | User lock | 2D visual approval STOP |

### Phase 1 new decisions

| ID | Decision | Source | Applied to |
|----|----------|--------|------------|
| **D7** | Section 24 marketing-studio row = **no manual edit needed**. Auto-generated from `SUB_SKILL_DESCRIPTIONS` dict (entry already at L85 from v3.7.13). Surfaces as PDF regeneration byproduct. | §1B verification trail (L1200-1204 auto-generation; L85 dict entry) | 2D regeneration step (no code edit) |
| **D8** | Courier (code blocks, `generate_user_guide.py:149`) NOT swapped to DejaVu Sans Mono in v3.7.14. Code blocks remain ASCII-only by existing convention; no Unicode pressure observed. Defer Courier swap until exercised. | Phase 0 §VERIFY 0.1 open-question close-out | 2B (NO swap of L149) |
| **D9** | Font family alias = `"Body"` (not `"DejaVuSansCondensed"` or `"DVC"`). Enables single find-replace pattern in 2B (`"Helvetica"` → `"Body"`); future-flexible if the underlying font ever changes (e.g., the 0.5pt bump path or the mixed-font fallback). | §1A item 2 design choice | 2B font registration alias |
| **D10** | Sub-phase ordering: 2C (version cascade) BEFORE 2D (PDF regeneration) per frontmatter-before-regen memory convention. Validator re-baseline (2E) happens after regeneration. | Memory note `feedback_release_workflow.md` v3.7.6 mega-release ; §1D corrected ordering | 2C-2D ordering |
| **D11** | Root Files table USER-GUIDE.pdf row staleness (PR #36 deferral from memory `project_user_guide_section22_staleness.md`) = flag-don't-decide. Three options documented; user direction at 2B STOP. | §1B adjacent-observation flag | 2B STOP review window |

---

## §1F — Phase 0 probe-artifact disposition

Per **D5** (carry-forward): probe artifacts at `/tmp/dejavu-test/` are scratch space and discard after Phase 1 inventory completes.

### Artifacts to discard

- `/tmp/dejavu-test/dejavu-fonts-ttf-2.37/` — DejaVu Sans family TTFs (downloaded for measurement only; bundling decision locked = DVC subset only goes into `assets/fonts/`)
- `/tmp/dejavu-test/dejavu-fonts-ttf-2.37.tar.bz2` — original archive
- `/tmp/dejavu-test/fpdf_smoke.py` — VERIFY 0.2 API verification script
- `/tmp/dejavu-test/condensed_test.py` — VERIFY 0.3 drift-comparison script
- `/tmp/dejavu-test/real_descriptions.py` — VERIFY 0.3 real-text-utilization measurement
- `/tmp/dejavu-test/dejavu.pdf` — sample render output from VERIFY 0.2 smoke test
- `/tmp/dejavu-test/ctrl.pdf` — control PDF (Helvetica em-dash crash; never created — crash short-circuited file write; nothing to discard)

### Action

Discard timing: **after Phase 2A**. The three TTFs that go into `assets/fonts/` come FROM `/tmp/dejavu-test/dejavu-fonts-ttf-2.37/ttf/` — keep until copy completes, then clean.

Phase 2A explicit step (added to the ordering): after `cp` of TTFs into `assets/fonts/`, run `rm -rf /tmp/dejavu-test/` to close the artifact loop. Discarding earlier would force a re-download.

### Durable artifacts (retained)

- `.planning/v3.7.14/PHASE-0-VERIFICATION.md` — full five-check probe report (committed in Phase 2 alongside the rest of `.planning/v3.7.14/`)
- `.planning/v3.7.14/PHASE-1-INVENTORY.md` — this document (committed in Phase 2 alongside the rest)

---

## STOP. Awaiting user review before Phase 2 begins.

Phase 1 produces six locked deliverables (§1A-§1F). Phase 2 executes 2A → 2G ordering with four STOPs at 2B / 2C / 2D / 2F. Phase 3 is the standard v3.7.x ship cascade (commit + tag + GitHub release per memory `feedback_release_workflow.md`).

No further sub-phase chaining without approval — same v3.7.13 discipline.
