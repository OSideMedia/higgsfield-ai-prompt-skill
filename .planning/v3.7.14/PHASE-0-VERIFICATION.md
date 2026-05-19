# v3.7.14 — Phase 0 Verification Report

**Date:** 2026-05-18
**Scope under verification:** Option B — `--dry-run` flag + FPDF Unicode font upgrade + Section 24 row addition
**Convention carried from v3.7.13:** `.planning/<version>/PHASE-0-*.md`

---

## Headline finding

**Option B holds, with one substitution:** swap target font from **DejaVu Sans regular** to **DejaVu Sans Condensed** (DVC). DVC keeps glyph-width drift inside the user-stated 5% threshold for real content, while DV regular triggers the descope criterion (11-18% drift, one current sub-skill description overflows the 115mm column).

If the user prefers strict DV regular instead of DVC, the descope path (Option A: --dry-run alone for v3.7.14) becomes the right call. Otherwise B-DVC is clean.

---

## VERIFY 0.1 — DejaVu Sans availability

**Result:** Not installed on system. Bundle in repo.

System search (macOS, this dev environment):
- `/Library/Fonts/`, `/System/Library/Fonts/`, `/System/Library/Fonts/Supplemental/`, `~/Library/Fonts/`, `/opt/homebrew/share/fonts/`, `/usr/local/share/fonts/`, `/usr/share/fonts/` — **none contain DejaVu**.
- Homebrew: `font-dejavu` cask NOT installed; `fontconfig` IS installed (irrelevant — no DejaVu fonts registered).
- fpdf2 package data dir (`site-packages/fpdf/data/`) — no bundled TTFs.

**Proposed bundle path:** `assets/fonts/` (new directory, sibling to `db/`, `docs/`, `templates/`).

**Files needed** (Helvetica `""`, `"B"`, `"I"` styles used in `generate_user_guide.py`; no `"BI"` combination):
- `DejaVuSansCondensed.ttf` — 668 KB
- `DejaVuSansCondensed-Bold.ttf` — 652 KB
- `DejaVuSansCondensed-Oblique.ttf` — 588 KB
- **Total bundled weight: ~1.9 MB** (well under 5 MB threshold)

**Source:** Official release tarball `https://github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/dejavu-fonts-ttf-2.37.tar.bz2` (Bitstream Vera + public domain license — redistribution OK).

**Open question (flag for Phase 1):** `generate_user_guide.py:149` uses `Courier` for code blocks. Courier is also a latin-1 core font with the same Unicode constraint. Code blocks today are ASCII-only (CLI commands, paths). Two paths:
- Leave Courier; document that code blocks must remain ASCII (matches current de-facto convention).
- Also bundle `DejaVuSansMono*.ttf` (+ ~600 KB, total ~2.5 MB). Symmetric with Helvetica swap.

**Recommendation:** leave Courier as-is for v3.7.14; revisit if a code block ever needs Unicode (so far none have).

---

## VERIFY 0.2 — FPDF Unicode font API

**Result:** PASS. fpdf2 v2.8.7 installed. Swap pattern works on a minimal test PDF.

**Confirmed:**
- Package: `fpdf2` v2.8.7 (the maintained fork, not classic FPDF 1.x).
- `add_font` signature:
  ```
  FPDF.add_font(family, style='', fname=<path>, *, unicode_range=None, variations=None, palette=None, collection_font_number=0)
  ```
  Modern positional API: `pdf.add_font("DejaVu", "", "/path/DejaVuSans.ttf")` works.
- `set_font` signature unchanged from current usage: `pdf.set_font(family, style='', size=0)`.
- No `uxn` flag or `.pkl` cache file requirements in fpdf2 2.x (those were FPDF 1.x relics).

**Smoke test result** (control vs. DejaVu swap):
- Control (Helvetica + em-dash): `FPDFUnicodeEncodingException: Character "—" at index 13 in text is outside the range of characters supported by the font used: "helvetica"`. ✅ Reproduces the v3.7.13 crash exactly.
- Swap (DejaVu + em-dash, en-dash, curly quotes, ellipsis at regular/bold/italic): **clean render, no exception, output PDF written**.

**Glyph metrics surfaced:** see VERIFY 0.3 below.

---

## VERIFY 0.3 — Glyph width / layout cascade risk

**Result:** DescopeTrigger fires for **DejaVu Sans regular**. Does NOT fire for **DejaVu Sans Condensed**.

**Drift measured at body 9pt (Section 22 column 115mm) and 10pt (body text), comparing each candidate font's `get_string_width` against Helvetica's:**

| Sample (real-text where possible)          | Helv→DVC drift | Helv→DV drift |
|--------------------------------------------|----------------|---------------|
| 71×'x' synthetic worst case @ 9pt          | +6.40%         | +18.40%       |
| Typical sub-skill desc (70 chars) @ 9pt    | +2.82%         | +14.29%       |
| Realistic body paragraph @ 10pt            | +0.62%         | +11.86%       |
| Section 24 row label `generate_user_guide.py` @ 10pt | +0.57% | +11.77%       |

**Real SUB_SKILL_DESCRIPTIONS column utilization** (115mm column at 9pt, measured against every existing entry):

| Sub-skill                       | chars | Helv %col | DVC %col | DV %col   | Wraps under |
|---------------------------------|-------|-----------|----------|-----------|-------------|
| higgsfield-cinema (longest)     | 71    | 91.6%     | 93.3%    | **103.8%**| **DV only** |
| higgsfield-seedance             | 66    | 84.5%     | 87.6%    | 97.4%     | none        |
| higgsfield-camera               | 63    | 86.4%     | 87.7%    | 97.5%     | none        |
| higgsfield-soul                 | 63    | 81.5%     | 82.4%    | 91.6%     | none        |
| higgsfield-marketing-studio     | 61    | 75.5%     | 77.5%    | 86.2%     | none        |
| ...22 entries total, all others well under | — | <60% | <60% | <70% | none |

**Effective char ceiling at 9pt in 115mm column** (derived from longest existing entry's avg char width):
- Helvetica: ~77 chars (current empirical ceiling 71 has 6-char safety margin)
- **DVC: ~76 chars** (-1 char vs Helvetica; current 71 ceiling still safe with 5-char margin)
- DV regular: ~68 chars (-9 chars vs Helvetica; current 71 ceiling INVALID — would need lowering to ~63)

**Why DV regular trips the descope criterion:**
- User stated: *"if column-width drift exceeds ~5% across any single column, table headers/cells may wrap unexpectedly. If wrap risk is high, flag for descope consideration."*
- DV regular drift: 11.77% – 18.40% across measured samples. **3-4× the 5% threshold.**
- One existing sub-skill description (`higgsfield-cinema`, 71 chars) renders to 119.33mm under DV regular vs. the 115mm column — wraps.
- Recalibrating `SUB_SKILL_DESCRIPTION_CEILING` from 71→63 in `validate_user_guide.py` would invalidate the current `higgsfield-cinema` entry, forcing a same-PR content rewrite of the description. Infrastructure-change cascading into content-change is the failure mode the descope criterion is designed to catch.

**Why DVC stays under threshold:**
- DVC drift on real content: 0.57% – 2.82% (worst case 6.40% only on a synthetic 71×'x' string, which is not real content).
- Zero existing entries overflow.
- `SUB_SKILL_DESCRIPTION_CEILING = 71` stays valid (-1 effective char headroom; current longest is 71 chars renders at 93.3% utilization — still has wrap margin).
- Section 24 row label measurements (`generate_user_guide.py` and similar paths) show 0.57% drift — invisible at the table-column level.

**Visual difference (qualitative):** DVC glyphs are narrower than Helvetica's by ~2-3% on real text. Reader-perceptible only on side-by-side comparison; on a freestanding USER-GUIDE.pdf no one would notice. Maintains Sans look, no serif/style shift.

---

## VERIFY 0.4 — `validate_user_guide.py` normalization audit

**Result:** No structural change required. Layer 1 normalization is sound. Re-baseline is the natural transition (would happen for Section 24 row addition regardless).

**Layer-by-layer audit:**

- **Layer 0** (`validate_sub_skill_descriptions`, L143-172): char-count check against `SUB_SKILL_DESCRIPTION_CEILING = 71`.
  - Under **DVC**: ceiling stays valid. No change needed.
  - Under **DV regular**: ceiling becomes invalid (effective ~63). Would need lowering AND a content rewrite of `higgsfield-cinema`. (Descope trigger.)

- **Layer 1** (text-extract diff, L122-217): normalizes version/date/sub-skill-count patterns only. Compares the **extracted text** from baseline vs. candidate via `pdftotext -layout`.
  - The font swap changes *rendering*, not *text content*. UTF-8 chars coming out of `pdftotext` are the same.
  - However: `pdftotext -layout` reconstructs spacing from glyph positions. If glyph widths shift enough, column boundaries can reflow and the diff fires.
  - **Mitigating factor:** v3.7.14 is already a planned re-baseline event (Section 24 row addition is a content change that alone re-fires Layer 1). The Layer 1 re-baseline procedure is already the v3.7.0 → v3.7.12 → v3.7.13 pattern. Simply update `DEFAULT_BASELINE` from `baseline-v3.7.12` to `baseline-v3.7.14`. Same edit `validate_user_guide.py:98`.
  - No new normalization patterns needed.

- **Layer 2** (binary diff, L219-233): informational only. Font swap completely changes PDF binary structure (new font subsetting, embedded glyph tables, descriptor objects). Layer 2 will report many byte diffs. This is its expected output and is documented as informational — not a regression signal.

**Verdict:** Re-baseline (option `b` from the task brief) is the right path. Option `a` (extend Layer 1 to normalize over font-rendering differences) was the alternative — not needed.

---

## VERIFY 0.5 — `--dry-run` flag scope

**Result:** Mechanically simple. ~10 LoC added to `generate_user_guide.py`, no refactor of `build_pdf()`.

**Current shape:**
```python
# generate_user_guide.py
def build_pdf():
    ...
    # L1188-1198: dict-parity check (raises RuntimeError if drift) — already runs in-process
    discovered = set(discover_sub_skills())
    declared = set(SUB_SKILL_DESCRIPTIONS.keys())
    if discovered != declared:
        raise RuntimeError(...)
    ...
    # L1253: single file-write call
    pdf.output("docs/user-guide/USER-GUIDE.pdf")
    print(f"Generated docs/user-guide/USER-GUIDE.pdf ({pdf.page_no()} pages)")

if __name__ == "__main__":
    build_pdf()
```

**Proposed --dry-run patch (Phase 2 work):**
```python
def build_pdf(dry_run: bool = False):
    ...
    # dict-parity check (unchanged — runs in both modes)
    ...
    # font registration + pdf.cell/table_row calls all run in both modes
    ...
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

**Verified:**
- `build_pdf()` does NOT write intermediate state to disk before `pdf.output(...)`. fpdf2's in-memory model holds the PDF buffer until `output()` serializes it. Confirmed via fpdf2 source inspection — no early writes.
- `build_pdf()` does NOT depend on the output path being set anywhere else. The single `pdf.output(...)` at L1253 is the only file-write site.
- Both `pdf.page_no()` (used in the success print at L1254) and the dict-parity check (L1188-1198) work identically in dry-run mode.

**Validator-integration plan (Phase 2 work, separate file):**
- `validate.py` (the root pre-release health check, not `validate_user_guide.py`) gains a new check that subprocess-invokes `python3 generate_user_guide.py --dry-run` and asserts return code 0.
- This catches latent rendering bugs (the v3.7.12 RuntimeError and v3.7.13 em-dash crash class) before ship-time regeneration writes a half-broken PDF.

**No complications surfaced.** Scope is bounded.

---

## Section 24 row addition — content delta inventory (pre-Phase 1 sketch)

Per backlog item from v3.7.13: a new row for `skills/higgsfield-marketing-studio/` in Section 24 "Root Files" / sub-skill listing. This is a content edit, not infrastructure.

**Note:** `SUB_SKILL_DESCRIPTIONS` at L67 already contains `higgsfield-marketing-studio` (added in v3.7.13 per the v3.7.13 changelog). What was deferred was the PDF-side Section 24 row that surfaces it in the sub-skill rundown. Phase 1 should locate Section 24 in `build_pdf()`, confirm the existing rows pattern, and add one row for marketing-studio matching the established structure.

Out of scope for Phase 0 — flagged here so Phase 1 inventory knows it's a focused content edit.

---

## Phase 0 recommendation

**Primary: Proceed with Option B, font target = DejaVu Sans Condensed (DVC).**

Rationale:
1. DVC keeps drift within the user-stated 5% threshold for real content (0.6% – 2.8% on actual SUB_SKILL_DESCRIPTIONS entries; 6.4% only on a synthetic worst-case string).
2. No existing entries overflow the 115mm column under DVC.
3. `SUB_SKILL_DESCRIPTION_CEILING = 71` stays valid — no Layer 0 validator change.
4. Layer 1 re-baseline is happening regardless (Section 24 content change), so the font-swap-induced re-baseline is "free" — no incremental work.
5. Closes the em-dash constraint that bit v3.7.13 (and forced workaround commits).
6. Bundles ~1.9 MB of fonts into the repo — well under 5 MB threshold; license is redistributable.
7. `--dry-run` is a 10-line addition with no refactor risk.

Single release (v3.7.14) ships:
- `--dry-run` flag (infrastructure)
- DVC swap (em-dash constraint closed)
- Section 24 row for marketing-studio (deferred content)
- New `USER-GUIDE.pdf.baseline-v3.7.14` replacing v3.7.12 as validator target

**Descope path if user prefers strict DV regular (NOT recommended):** drop to Option A — `--dry-run` alone as v3.7.14, defer font + Section 24 row to v3.7.15. Strict-DV-regular adoption would force a same-PR content rewrite of `higgsfield-cinema` and a Layer 0 ceiling recalibration — exactly the cascade the descope criterion was written to prevent.

**Open user decision before Phase 1 inventory:** confirm DVC substitution is acceptable, OR direct descope to Option A. (Question deferred per "STOP after Phase 0 report" — not auto-deciding.)

---

## Phase 0 artifacts (NOT committed to repo)

- `/tmp/dejavu-test/dejavu-fonts-ttf-2.37/` — DejaVu Sans family TTFs (downloaded for measurement only; bundling decision deferred to Phase 1/2)
- `/tmp/dejavu-test/fpdf_smoke.py` — FPDF API + glyph-width verification script
- `/tmp/dejavu-test/condensed_test.py` — DVC vs DV vs Helvetica comparison
- `/tmp/dejavu-test/real_descriptions.py` — real SUB_SKILL_DESCRIPTIONS column-utilization measurement
- `/tmp/dejavu-test/ctrl.pdf` (Helvetica em-dash crash — file not produced, crash confirmed)
- `/tmp/dejavu-test/dejavu.pdf` — sample PDF rendered with DejaVu Sans

These can be removed once Phase 0 is accepted. They live in `/tmp` precisely so they don't leak into the repo before the bundling decision is locked.

---

**STOP. Awaiting user review before Phase 1 inventory.**
