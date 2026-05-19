# v3.7.16 — Phase 1 Locked Inventory + Decisions Register

**Date:** 2026-05-18
**Carry-forward from Phase 0 (`PHASE-0-VERIFICATION.md`):** Five findings confirmed; eight Phase-0 decisions locked (D-PHASE-0-1 through D-PHASE-0-8). Architectural Option β LOCKED (consolidated `higgsfield-gpt-image-2` sub-skill + `static-ads-workflow.md` satellite + ms_image as cross-surface-workflow.md §3 expansion). Item 2 rescoped. Items 13 + 6 of 9 cross-reference sub-sites descoped to v3.7.17+.
**Substrate inherited:** v3.7.14 DVC pipeline + `--dry-run` smoke gate, v3.7.13 `.planning/<version>/` artifact convention, v3.7.15 per-claim register-downgrade discipline.
**Convention:** `.planning/<version>/PHASE-1-INVENTORY.md` per v3.7.13 → v3.7.14 → v3.7.15 pattern.

---

## §1A — File-by-file change inventory

Every file touched by v3.7.16, ordered roughly by Phase 2 sub-phase. LoC estimates are conservative ceilings reflecting both content + translation expansion overhead (~30–40% over source LoC per v3.7.13/15 translation precedent).

### NEW FILE: `skills/higgsfield-gpt-image-2/SKILL.md` (target ~400–500 lines)

The substantive new-content surface. Translated from Adil's `gpt-image-2-director.md` source corpus (206 lines, at `~/Desktop/EVEN MORE SKILLS/gpt-image-2-director/SKILL.md`).

**Structure (locked):**

| # | Section | Source mapping | Target LoC | Translation rules |
|---|---|---|---|---|
| 1 | Frontmatter | none (new) | ~10 | Standard v3.7.13/15 pattern: `name: higgsfield-gpt-image-2`, dense `description` line for routing trigger, `user-invocable: true`, `metadata.tags`, `metadata.version: 1.0.0`, `metadata.updated`, `metadata.parent: higgsfield` |
| 2 | Opener (`# Higgsfield GPT Image 2.0`) | source L6–8 + new framing | ~15 | One-paragraph mission statement; cite Adil source corpus; note relationship to companion `static-ads-workflow.md` satellite |
| 3 | `## 1. What GPT Image 2.0 is` | source L10–19 | ~25 | Apply §1B-A translation rules (per-claim register-downgrade) |
| 4 | `## 2. Three prompt formats` | source L21–35 | ~30 | Format-A/B/C overview; routing decision rules |
| 5 | `## 3. Format A — Structured JSON` | source L37–99 | ~80 | Core fields + 5 key-pattern subsections + worked JSON example |
| 6 | `## 4. Format B — Dense cinematic prose` | source L101–122 | ~50 | 8-step info order + 5 craft rules + worked prose example |
| 7 | `## 5. Format C — Auto-derive meta-prompt` | source L124–152 | ~40 | Templated meta-prompt scaffold + when-to-use trigger |
| 8 | `## 6. Routing decision` | source L21–35 + L164–172 | ~35 | Concept→format decision rules; consolidated from source L21–35 routing overview + source L164–172 routing-deep examples |
| 9 | `## 7. Output format conventions` | source L154–162 | ~15 | Code-block-wrapping rules; preserve as production discipline |
| 10 | `## 8. Quality checklist` | source L174–183 | ~15 | 6-item pre-delivery checklist (aligns with existing DISCIPLINE.md Tier 3 § Pre-Delivery Discipline) |
| 11 | `## 9. Example routings` | source L185–205 | ~40 | 6 paired concept→format examples — translate sourced examples or substitute with our voice |
| 12 | `## 10. Cross-surface workflow context` | new | ~15 | Forward-pointer to `static-ads-workflow.md` satellite; pointer to higgsfield-marketing-studio cross-surface-workflow.md §3 for ms_image (a Higgsfield-native image-generation alternative to GPT Image 2.0) |
| 13 | `## 11. Source acknowledgment` | new | ~15 | Adil credit per v3.7.13/15 pattern; verification trail to `.planning/v3.7.16/PHASE-0-VERIFICATION.md` §VERIFY 0.1 |

**Target total:** ~385 LoC ≈ ~400 lines after section dividers and house-style padding. Conservative ceiling: ~500 lines. Below the kickoff's "~600–900 lines per v3.7.13 marketing-studio precedent" estimate because gpt-image-2-director.md is materially less verbose than the marketing-studio source corpus (262 + 997 = 1259 lines) was.

**House-style notes:**
- All sections follow the production-direction register established in v3.7.13's higgsfield-marketing-studio/SKILL.md
- Per-claim translation rules from §1B-A applied mechanically during composition
- Code-block conventions: JSON examples in `json` fenced blocks; prose examples in `text` fenced blocks
- Cross-reference notation: `(see § <section name>)` for in-document refs, `(see [vocab.md](../../vocab.md) § <name>)` for cross-skill refs — matches existing skill SKILL.md patterns

### NEW FILE: `skills/higgsfield-gpt-image-2/static-ads-workflow.md` (target ~300–400 lines)

The satellite doc. Translated from Adil's `static-ads.md` source corpus (316 lines, at `~/Desktop/EVEN MORE SKILLS/MORE CUSTOM SKILLS/static-ads.md`). Mirrors the `skills/higgsfield-marketing-studio/cross-surface-workflow.md` satellite pattern.

**Structure (locked):**

| # | Section | Source mapping | Target LoC | Translation rules |
|---|---|---|---|---|
| 1 | Frontmatter | none (new) | ~10 | Standard v3.7.13 satellite pattern: `name: higgsfield-gpt-image-2` (same as parent SKILL.md per cross-surface-workflow.md convention), `user-invocable: false`, `metadata.parent: higgsfield-gpt-image-2`, `metadata.tags` including `static-ads`/`ad-recreation`/`workflow` |
| 2 | `## 1. What this document is` | new | ~20 | Connection layer between gpt-image-2 prompt-craft (parent SKILL.md) and ad-recreation workflow (this doc); cite Adil source |
| 3 | `## 2. The 10-step workflow` | source L14–287 (Steps 1–10) | ~150 | Translate the 10 sequential steps. Apply §1B-B translation rules (lowest-friction sub-class). **Two adoption gates per §1B-B:** (1) brand-folder convention — translate the workflow as the storage convention static-ads expects, with explicit "Adil's recipe assumes" framing; (2) script dependencies — document pattern conceptually, note that `generate-static-ad.py` and `generate-reformat.py` scripts live in Adil's project and are not adopted into our skill |
| 4 | `## 3. Layout zones + safe zones` | source L48–66 + L223+L229 (safe-zone rule) | ~30 | Fractional-coordinate zone notation (text_zone / product_zone / button_zone / disclaimer_zone) + safe-zone top-10%/bottom-10% rule. Highest-falsifiable-claim content in the source corpus per Phase 0 §VERIFY 0.2b |
| 5 | `## 4. Brand-vs-structure separation` | source L208–229 (Mode A + Mode B) | ~30 | The two-list rule: take layout/zones/UI element types from reference, take visual identity from brand guidelines. **Adopt close to verbatim — this is the core operational rule of the skill.** |
| 6 | `## 5. Wireframe intermediation` | source L64–66 | ~20 | The brand-neutral wireframe technique — Adil's contribution to the GPT-image-2 production knowledge surface; non-obvious; transferable to other image models |
| 7 | `## 6. Prompt template reference` | source L301–316 (3 worked examples) | ~80 | iMessage / Scarcity Countdown / Ingredient Spotlight — adopt as quoted examples in fenced `text` blocks. **Phase 2 judgment call:** substitute bracketed placeholders if source uses Adil-specific brand naming, OR preserve verbatim with attribution |
| 8 | `## 7. Forward-pointers` | new | ~15 | Cross-reference to parent SKILL.md format-routing for prompts that don't fit the 10-step ad-recreation flow; cross-reference to higgsfield-marketing-studio for ad-video workflows |
| 9 | `## 8. Source acknowledgment` | new | ~15 | Adil credit; verification trail to `.planning/v3.7.16/PHASE-0-VERIFICATION.md` §VERIFY 0.2 |

**Target total:** ~370 LoC ≈ ~400 lines after section dividers. Slightly above kickoff target of "~250–400 lines per cross-surface-workflow.md precedent" because static-ads.md (316 lines) is substantially longer than cinematic-motion-language.md (209 lines, v3.7.15 source) was. Conservative ceiling: ~430 lines.

### MODIFIED: `skills/higgsfield-marketing-studio/cross-surface-workflow.md` (currently 428 lines → ~550–600 lines)

§3 expansion. Currently L48–60 (a single brief paragraph "Path B (Higgsfield-native alternative)") becomes ~400–600 words of explicit ms_image / DTC Ads coverage. **Source-evidence boundary defined in §1C below — content stays within Probe 0.3-a evidence + Adil-corpus naming; no fabrication.**

**Net delta:** ~+100–150 lines added to §3. Other sections of cross-surface-workflow.md unchanged.

**Net structural change:** §3 acquires sub-sections (~3.a–3.d) per §1C structure. The existing "Path A / Path B" framing is preserved; Path B gets the substantive expansion.

### MODIFIED: `generate_user_guide.py` (currently 1278 lines)

Five distinct edit sites:

1. **`assets/fonts/DejaVuSansMono.ttf` registration (L101–103 vicinity)** — add one new `add_font` call alongside existing DVC `Body` registrations:
   ```python
   # NEW line, insert after L103:
   self.add_font("Mono", "", str(FONT_DIR / "DejaVuSansMono.ttf"))
   ```
   Net: +1 LoC.

2. **`code_block` method (L155–163), single set_font swap (L156)** — Courier → Mono alias:
   ```python
   # OLD
   self.set_font("Courier", "", 9)
   # NEW
   self.set_font("Mono", "", 9)
   ```
   Net: 0 LoC (token swap). Only call site in the entire file uses Courier (grep-confirmed).

3. **FAQ paragraph refresh (L1235–1247)** — update count + version per D-PHASE-0-5. Minimum-viable refresh per Phase 0 §VERIFY 0.7a recommendation: 2 token swaps for count + version. Phase 2 §2G judgment call on whether to extend with v3.7.13–v3.7.16 era summary (~+5 LoC) or ship minimum-viable (~+0 LoC; just two-token swap).
   ```python
   # OLD (L1235–1236)
   ("What changed since v3.0.0?",
    "Seventeen platform releases shipped between v3.0.0 (April 2026) and this guide (v3.7.12). "
   # NEW (minimum-viable)
   ("What changed since v3.0.0?",
    "Thirty platform releases shipped between v3.0.0 (April 2026) and this guide (v3.7.16). "
   ```
   Net: 2 token swaps (minimum-viable) OR ~+5 LoC for substantive refresh with v3.7.13–v3.7.16 era summary clause. **Phase 2 picks** between the two via §2G; my read leans substantive refresh because the existing prose ends on v3.7.12 and skipping 4 releases of era summary is noticeable.

4. **`SUB_SKILL_DESCRIPTIONS` dict (L68–91)** — add one new entry for `higgsfield-gpt-image-2` matching the existing pattern + 71-char ceiling:
   ```python
   # NEW entry, alphabetical position after higgsfield-cinema:
   "higgsfield-gpt-image-2":     "GPT Image 2.0 prompt director + static-ads workflow satellite",
   ```
   Per `validate_user_guide.py` L143–172 `SUB_SKILL_DESCRIPTION_CEILING = 71` check: the proposed description is 62 chars — passes. Net: +1 LoC. **Position 23 of 23 in dict** — net dict count goes from 22 to 23. **CRITICAL CHECK** before Phase 2H: re-verify the description length against the ceiling.

5. **`--dry-run` exit-code matrix (build_pdf + `__main__`)** — per D-PHASE-0-3 design D5-A. Defined named exception classes + argparse harness in `__main__` mapping exception subclasses to exit codes 0–6.

   **Design D5-A integration:**
   ```python
   # NEW: Exception class hierarchy at top-of-file, after imports (~L17)
   class BuildError(RuntimeError):
       """Base class for build_pdf failures."""

   class FrontmatterError(BuildError): pass
   class DictParityError(BuildError): pass
   class FontError(BuildError): pass
   class RenderError(BuildError): pass
   class OutputWriteError(BuildError): pass

   # NEW: Exit code constants
   EXIT_OK = 0
   EXIT_UNKNOWN = 1
   EXIT_FRONTMATTER = 2
   EXIT_DICT_PARITY = 3
   EXIT_FONT = 4
   EXIT_RENDER = 5
   EXIT_OUTPUT = 6
   ```

   **Re-raise at existing failure points:**
   - L29 `raise RuntimeError(f"No YAML frontmatter found...")` → `raise FrontmatterError(...)`
   - L37 `raise RuntimeError(f"Field '{name}' not found...")` → `raise FrontmatterError(...)`
   - L1200 `raise RuntimeError(f"Sub-skill list out of sync...")` → `raise DictParityError(...)`
   - Wrap `add_font` calls in try/except, re-raise as `FontError` (L101–103)
   - Wrap the body-rendering work in try/except, re-raise `FPDFUnicodeEncodingException` as `RenderError` (catch in `__main__` rather than per-call wrap to avoid noise)
   - Wrap `pdf.output(...)` call at L1263 in try/except, re-raise as `OutputWriteError`

   **Argparse harness in `__main__` (L1267 onward):**
   ```python
   if __name__ == "__main__":
       import argparse, sys
       parser = argparse.ArgumentParser(description="Regenerate USER-GUIDE.pdf.")
       parser.add_argument(
           "--dry-run",
           action="store_true",
           help="Run the dict-parity check and full build_pdf() rendering pipeline "
                "in-memory without writing the output file. Exit codes: "
                "0 OK, 1 unknown, 2 frontmatter, 3 dict-parity, 4 font, 5 render, 6 output.",
       )
       args = parser.parse_args()
       try:
           build_pdf(dry_run=args.dry_run)
           sys.exit(EXIT_OK)
       except FrontmatterError as e:
           print(f"FRONTMATTER ERROR: {e}", file=sys.stderr); sys.exit(EXIT_FRONTMATTER)
       except DictParityError as e:
           print(f"DICT-PARITY ERROR: {e}", file=sys.stderr); sys.exit(EXIT_DICT_PARITY)
       except FontError as e:
           print(f"FONT ERROR: {e}", file=sys.stderr); sys.exit(EXIT_FONT)
       except RenderError as e:
           print(f"RENDER ERROR: {e}", file=sys.stderr); sys.exit(EXIT_RENDER)
       except OutputWriteError as e:
           print(f"OUTPUT-WRITE ERROR: {e}", file=sys.stderr); sys.exit(EXIT_OUTPUT)
       except Exception as e:
           print(f"UNKNOWN ERROR: {type(e).__name__}: {e}", file=sys.stderr); sys.exit(EXIT_UNKNOWN)
   ```

   **Module docstring update (~L2–9)** — append exit-code summary to docstring per Phase 0 §VERIFY 0.5c (module docstring as documentation surface):
   ```python
   """Generate USER-GUIDE.pdf for Higgsfield AI Prompt Skill.

   Version metadata is read from the root SKILL.md frontmatter at build time.
   Sub-skill list at Section 24 is discovered by filesystem walk of skills/.
   Per-sub-skill description text remains hardcoded in SUB_SKILL_DESCRIPTIONS
   below to preserve the PDF's editorial voice (entries refreshed at v3.7.12
   to add higgsfield-stack and update higgsfield-soul + higgsfield-seedance).

   Exit codes (v3.7.16+):
     0 = success
     1 = unknown/uncaught error
     2 = frontmatter parse error (root SKILL.md)
     3 = sub-skill dict-parity mismatch (SUB_SKILL_DESCRIPTIONS vs filesystem)
     4 = font registration error (missing or malformed TTF)
     5 = rendering error (e.g., FPDFUnicodeEncodingException)
     6 = output write error (disk full, permission denied, path missing)
   """
   ```
   Net: +9 LoC for docstring.

   **Total LoC delta for site #5:** ~+45 LoC (exception class declarations + exit-code constants + 5 re-raise wrappers + argparse harness + module docstring update). Bounded at the "Design D5-A: +30–40 LoC" estimate from Phase 0 with small overage for the docstring update.

**Net `generate_user_guide.py` total delta:** ~+50 to +55 LoC. Touches 5 distinct sites; no refactor of `build_pdf()` core logic.

### MODIFIED: `validate.py` (currently 160 lines → ~180 lines)

One new check phase + subprocess invocation. Per D-PHASE-0-4 design 6-A (position: append as Phase 4 after Phase 3 root files) + 6-i binary error handling.

**Insertion point:** L144 (after the root-files check loop, before the summary at L146).

```python
# NEW after L144:
# ── 4. PDF dry-run smoke check ───────────────────────────────────────────
print("\n[ PDF DRY-RUN SMOKE ]")
import subprocess
result = subprocess.run(
    ["python3", str(ROOT / "generate_user_guide.py"), "--dry-run"],
    capture_output=True, text=True, timeout=60,
)
if result.returncode == 0:
    check(True, "generate_user_guide.py --dry-run", "exit 0")
else:
    stderr_excerpt = result.stderr.strip().splitlines()[0] if result.stderr.strip() else f"exit {result.returncode}"
    check(False, "generate_user_guide.py --dry-run",
          f"exit {result.returncode}; stderr: {stderr_excerpt[:150]}")
```

**Net LoC delta:** +15 LoC inside `main()`. Single subprocess invocation; binary pass/fail mapping; stderr first-line excerpt surfaced for diagnostic context. Timeout=60s as belt-and-suspenders (the dry-run normally runs in ~1.5s; 60s ceiling catches hung-subprocess pathology).

### MODIFIED: `validate_user_guide.py` (currently L98 area)

One-line edit. `DEFAULT_BASELINE` retarget from `USER-GUIDE.pdf.baseline-v3.7.15` to `USER-GUIDE.pdf.baseline-v3.7.16`. Net: 1 token swap.

### NEW FILE: `assets/fonts/DejaVuSansMono.ttf` (333 KB)

Bundle the regular weight only (per Phase 0 §VERIFY 0.4d recommendation). Bold / Oblique / Bold-Oblique NOT bundled — no existing code-block call site uses them (`code_block` at L156 calls `set_font("Courier", "", 9)` — regular only). License: Bitstream Vera + public domain, redistributable per the existing DVC bundle in `assets/fonts/README.md`.

**Bundle source:** `/tmp/dejavu-test/dejavu-fonts-ttf-2.37/ttf/DejaVuSansMono.ttf` (carried over from v3.7.14 Phase 0 download tarball).

**Update `assets/fonts/README.md`** to add a one-paragraph note about the DVSM bundle rationale — Phase 2 §2A. ~+5 LoC.

### MODIFIED: `templates/seedance/multi-character-anchor.md` (L80)

Per D-PHASE-0-6 and Phase 0 §VERIFY 0.7b item 12.4. Existing L80 prose:

> "**GREAT:** Use the template, fill every field including percentage notation paired with qualitative anchors, specify cross-character relationships (distance + eyeline + crossing rule + negative space)."

Proposed addition — append two parenthetical citations to the bare-named concepts:

> "**GREAT:** Use the template, fill every field including percentage notation paired with qualitative anchors, specify cross-character relationships (distance + eyeline + crossing rule + negative space — see [vocab.md](../../vocab.md) § Composition Vocabulary → Crossing rule + § Negative space)."

Net delta: 1 line edit, ~+1 LoC.

### MODIFIED: `templates/seedance/worked-example-two-character.md` (L68)

Per D-PHASE-0-6 and Phase 0 §VERIFY 0.7b item 12.6. Existing L67–69 prose:

> "- Every `multi-character-anchor.md` field filled — including cross-
>   character relationships (distance + eyeline + crossing rule +
>   negative space) per § Spatial Layout Block in the seedance SKILL.md"

Proposed addition — extend the existing `§ Spatial Layout Block` reference with an additional vocab.md citation:

> "- Every `multi-character-anchor.md` field filled — including cross-
>   character relationships (distance + eyeline + crossing rule +
>   negative space) per § Spatial Layout Block in the seedance SKILL.md
>   + [vocab.md](../../../vocab.md) § Composition Vocabulary → Crossing rule + § Negative space"

Net delta: 1-2 lines edited, ~+1 LoC.

### MODIFIED: `skills/higgsfield-seedance/SKILL.md` (L488)

Per D-PHASE-0-6 and Phase 0 §VERIFY 0.7b item 12.7. Existing L486–489 prose:

> "...Use them alongside the rest of the
> standard composition vocabulary (`over-the-shoulder`, `eye line`,
> `ground contact`, `headroom`, `nose room`, `crossing rule`) rather
> than as a substitute for it."

Proposed addition — extend the inline-vocabulary parenthetical with an explicit cross-reference at the end:

> "...Use them alongside the rest of the
> standard composition vocabulary (`over-the-shoulder`, `eye line`,
> `ground contact`, `headroom`, `nose room`, `crossing rule` — the
> last two are formalized at [vocab.md](../../vocab.md) § Composition
> Vocabulary → Crossing rule + § Spatial Zoning) rather
> than as a substitute for it."

Net delta: 1-2 lines edited, ~+1 LoC.

### MODIFIED: Root `SKILL.md`

Standard version-cascade pattern matching v3.7.10 → v3.7.11 → v3.7.12 → v3.7.13 → v3.7.14 → v3.7.15:

- `  version: 3.7.15` → `  version: 3.7.16`
- `  updated: 2026-05-18` → `  updated: <ship date>` (same-day cascade if shipped today; otherwise the actual ship date)

Net delta: 2 lines edited.

### MODIFIED: `README.md`

Same version-cascade pattern:

- Badge line: `version-3.7.15` → `version-3.7.16`
- Footer line: `v3.7.15 (updated 2026-05-18)` → `v3.7.16 (updated <ship date>)`

Net delta: 2 lines edited.

### MODIFIED: `CHANGELOG.md`

New v3.7.16 entry inserted above existing v3.7.15 entry at line 3. Following v3.7.13/14/15 prose-style template (lead paragraph + Added + Changed + Verification + Scope acknowledgment + Backlog updates).

Sketch entry — Phase 2 §2I composes the final prose:

```markdown
## v3.7.16 — <ship-date>

Mega release. New content surfaces (GPT Image 2.0 prompt-director sub-skill consolidating
gpt-image-2-director + static-ads workflow), Marketing Studio cross-surface-workflow.md
§3 ms_image expansion within Probe 0.3-a evidence boundary, infrastructure upgrade
(Courier → DejaVu Sans Mono swap for code blocks, --dry-run exit-code matrix gating
seven failure classes, validate.py subprocess integration of --dry-run as standard
pre-release gate), PDF FAQ paragraph refresh, and 3 cross-reference citations
following up on v3.7.15 vocab.md gap-fill.

### Source attribution

Adil Aliyev's gpt-image-2-director.md (~14 KB, sibling to marketing-studio-director and
content-factory translated in v3.7.13, cinematic-motion-language translated in v3.7.15)
and static-ads.md (~20 KB, the production-knowledge workflow doc for ad recreation).
[...]

### Added
[...]
### Changed
[...]
### Verification
[...]
### Scope acknowledgment
[...]
### Backlog — updated
[...]
```

Net delta: ~+120 lines (mega-release entries are larger than patch entries).

### NEW FILE: `docs/user-guide/USER-GUIDE.pdf.baseline-v3.7.16` (binary)

Regenerated PDF byte-copy, created via `cp docs/user-guide/USER-GUIDE.pdf docs/user-guide/USER-GUIDE.pdf.baseline-v3.7.16` after the v3.7.16 regen.

### MODIFIED: `docs/user-guide/USER-GUIDE.pdf` (regenerated)

Regenerated via `python3 generate_user_guide.py` after all upstream content + infrastructure changes are in place. Page count expected to increase from 28 (v3.7.15) by ~1 page because of the new sub-skill row in Section 24 (`SUB_SKILL_DESCRIPTIONS` count goes from 22 to 23). Net delta: binary refresh.

### NEW FILES: `.planning/v3.7.16/`

- `PHASE-0-VERIFICATION.md` — already shipped from Phase 0 (836 lines)
- `PHASE-1-INVENTORY.md` — this file

### TOTAL DELTA SUMMARY

| Surface | Disposition | Net lines |
|---|---|---|
| **NEW** `skills/higgsfield-gpt-image-2/SKILL.md` | new sub-skill from gpt-image-2-director.md translation | ~+400–500 |
| **NEW** `skills/higgsfield-gpt-image-2/static-ads-workflow.md` | new satellite from static-ads.md translation | ~+300–400 |
| **NEW** `assets/fonts/DejaVuSansMono.ttf` | DVSM regular weight bundle | binary (333 KB) |
| **NEW** `docs/user-guide/USER-GUIDE.pdf.baseline-v3.7.16` | new validator baseline | binary |
| `skills/higgsfield-marketing-studio/cross-surface-workflow.md` | §3 ms_image expansion | ~+100–150 |
| `generate_user_guide.py` | DVSM register + Courier→Mono swap + exit-code matrix + FAQ refresh + SUB_SKILL_DESCRIPTIONS entry + module docstring update | ~+50–55 |
| `validate.py` | subprocess integration of --dry-run | ~+15 |
| `validate_user_guide.py` | DEFAULT_BASELINE retarget | 0 (1 token) |
| `assets/fonts/README.md` | DVSM rationale note | ~+5 |
| `templates/seedance/multi-character-anchor.md` L80 | cross-reference addition | ~+1 |
| `templates/seedance/worked-example-two-character.md` L68 | cross-reference addition | ~+1 |
| `skills/higgsfield-seedance/SKILL.md` L488 | cross-reference addition | ~+1 |
| Root `SKILL.md` frontmatter | version + date cascade | 0 |
| `README.md` badge + footer | version cascade | 0 |
| `CHANGELOG.md` | new v3.7.16 entry | ~+120 |
| `docs/user-guide/USER-GUIDE.pdf` | regenerated (content + metadata cascade) | binary refresh |
| `.planning/v3.7.16/PHASE-0-VERIFICATION.md` | already shipped | n/a |
| `.planning/v3.7.16/PHASE-1-INVENTORY.md` | this file | n/a |

**Total markdown LoC delta:** ~+990 to +1250 lines (`+700–900` from the two new content surfaces + ~+100–150 from cross-surface-workflow.md expansion + ~+120 from CHANGELOG + ~+72 from infrastructure-spread + ~+3 cross-reference cites + ~+5 fonts/README). Mega-release-scale; **substantially larger than v3.7.15's ~+230–250** but smaller than v3.7.13's ~+1600 (which created the entire higgsfield-marketing-studio sub-skill from scratch).

**PDF binary:** refresh (page count increases by ~1 to ~29 pages, driven by Section 24 sub-skill table growth from 22 to 23 entries). Standard v3.7.x metadata cascade.

---

## §1B — Per-element translation rule tables (items 1 + 3)

Applying v3.7.15 §1G discipline. Per-element ADOPT/DOWNGRADE classification based on Phase 0 author-signature calibration. Phase 2 composes prose mechanically following these tables.

### §1B-A — gpt-image-2-director.md translation rules

**Source:** `~/Desktop/EVEN MORE SKILLS/gpt-image-2-director/SKILL.md` (206 lines). Disposition class from Phase 0 §VERIFY 0.1i: **TRANSLATE-WITH-VERIFICATION (LOWER-FRICTION SUB-CLASS).**

#### §1B-A-1 — Capability framing (source L10–19)

| Element | Source verbatim | Disposition | Translation rule |
|---|---|---|---|
| "Prompt following is its #1 strength" (L14) | Testable directional claim | **ADOPT under Spatial Zoning testability exception (v3.7.15).** | The claim is testable — a user can verify by running prompts with granular layout instructions against comparable models and observing the difference. Testable directional claims about prompt-side effects pass the testability boundary; universalizing metaphysical claims about model cognition would not. Translate: "GPT Image 2.0 honors granular layout instructions — top-left panel shows X, mid-right shows Y, N icons in a row labeled A/B/C — in a way other models don't reliably match." |
| "Text rendering is best-in-class" (L15) | Testable directional claim | **ADOPT under Spatial Zoning testability exception (v3.7.15).** | The claim is testable — a user can verify by running prompts with mixed scripts and small UI labels against comparable models and observing the difference. Testable directional claims about prompt-side effects pass the testability boundary; universalizing metaphysical claims about model cognition would not. Translate: "Multi-line paragraphs, mixed scripts (CJK + Latin), small UI labels, numeric data in tables — all sharp and legible. This is one of the model's distinctive strengths over comparable image generators." |
| "Design and UI mockups are its sweet spot" (L16) | Sweet-spot framing | **ADOPT.** | Concrete and falsifiable (a user can verify by testing). Translate close to verbatim. |
| "Cinematic photorealism is its weakness. Human faces often go plasticky. Lean into stylized, illustrated, or editorial aesthetics rather than hyperreal skin. When realism is requested, frame it as film photography (grain, flash, 35mm) rather than as 'photorealistic.'" (L17) | Failure-mode + workaround | **ADOPT close to verbatim — production discipline.** | The "lean into film photography not 'photorealistic'" recipe is a concrete falsifiable workaround. This is the highest-value production-knowledge content in the section. |

#### §1B-A-2 — Three-format taxonomy (source L21–35)

| Element | Source | Disposition | Translation rule |
|---|---|---|---|
| Format-A / Format-B / Format-C taxonomy | Adil's organizing principle | **ADOPT close to verbatim.** | Synthesis-level framing; preserve the three-bucket organization. |
| Per-format trigger lists ("UI mockups, landing pages, infographics…" / "portraits, cinematic scenes, landscapes…" / "concept posters, relationship diagrams, encyclopedia infographics…") | Concrete classification examples | **ADOPT.** | Direct routing rules. |
| "When in genuine doubt between A and B (e.g., 'a character with some labels around them') — default to A. Layout precision is GPT Image 2.0's main unlock and you want to use it." (L172) | Tie-break rule | **ADOPT close to verbatim.** | Concrete tie-break. Translate "main unlock" → "primary differentiator." |

#### §1B-A-3 — Format A craft patterns (source L37–99)

| Element | Source | Disposition | Translation rule |
|---|---|---|---|
| "Count-and-label pattern" (L51) | Named pattern | **ADOPT.** | Adil's framing of standard prompt-engineering. Preserve the name. |
| "Position-scoped regions" (L58) | Named pattern | **ADOPT.** | Same; preserve the name. |
| "Section objects with title, position, count, labels" (L61) | Named pattern | **ADOPT.** | Same. |
| "Templateable slots with `{argument name=\"x\" default=\"y\"}`" (L71) | Named pattern + slot syntax | **ADOPT but downgrade reach.** | The slot syntax is Adil-specific notation. Translate: "When a user explicitly wants a reusable template, slot notation like `{argument name=\"x\" default=\"y\"}` works. Don't add slots by default — keep one-off prompts concrete." Soften "Don't add them by default on one-off prompts" to a heuristic. |
| "Inline typography callouts" (L73) | Named pattern | **ADOPT.** | Translate close to verbatim. |
| JSON example for AURA brand (L76–98) | Worked example | **ADOPT.** | Decision per Phase 2 §2C judgment: keep verbatim with AURA placeholder OR substitute a different brand name. **Phase 2 call.** Either is fine; AURA is generic enough to keep. |

#### §1B-A-4 — Format B craft rules (source L101–122)

| Element | Source | Disposition | Translation rule |
|---|---|---|---|
| 8-step information order (L103–111) | Numbered scaffolding | **ADOPT close to verbatim.** | Translate: "Order the information roughly as: image type → main subject → pose/action → background → environmental details → lighting → color palette → mood. Roughly because GPT-Image-2 handles slight ordering deviation gracefully." Slight reach-extension on the "roughly" qualifier to acknowledge real-world flexibility. |
| "Specific over atmospheric" (L115) | Craft rule | **ADOPT.** | Concrete, falsifiable: more specific prompts produce more specific outputs. Plausibility-over-verification applies. |
| "Concrete props and objects" (L116) | Craft rule | **ADOPT.** | Same. |
| "Camera/film language" with examples (L117) | Craft rule + examples | **ADOPT close to verbatim.** | Standard cinematography vocabulary. |
| "Embedded text in quotation marks" (L118) | Production discipline | **ADOPT.** | Falsifiable: a user can verify quoted-text rendering produces sharper results. |
| "Avoid 'photorealistic' when faces are in frame. Use 'cinematic', 'film photograph', '35mm', 'editorial portrait' instead" (L119) | Failure-mode + workaround | **ADOPT close to verbatim.** | High-value production discipline. Cross-reference back to capability-framing failure-mode at §1B-A-1. |
| Prose worked example with CJK text (L122) | Worked example | **ADOPT with optional substitution.** | Decision per Phase 2 §2C judgment: keep verbatim (CJK example showcases text-rendering capability) OR substitute a different scene. **Phase 2 call.** My read leans keep verbatim — the CJK example IS the demonstration of the text-rendering capability claim. |

#### §1B-A-5 — Format C meta-prompt scaffold (source L124–152)

| Element | Source | Disposition | Translation rule |
|---|---|---|---|
| Meta-prompt template structure (L130–150) | Structural scaffolding | **ADOPT close to verbatim.** | Templated scaffold. Preserve placeholders + structural sections (Overall Style / Composition Rules / Visual Quality / Typography System / Signature). |
| "When to use this: the user gives you only a theme… and wants a rich, self-derived output. If they give specific layout details, use Format A instead." (L152) | Trigger rule | **ADOPT.** | Routing tie-break to Format A. |

#### §1B-A-6 — Output format conventions (source L154–162)

| Element | Source | Disposition | Translation rule |
|---|---|---|---|
| "Return only the finished prompt in a code block. No preamble, no explanation, no 'here's your prompt:', no format-choice justification. The user pastes it into GPT Image 2.0 directly." (L156) | Production discipline | **ADOPT close to verbatim.** | Matches our skill library's existing pattern (root SKILL.md HARD RULES item 7 — "Output the prompt; no preamble"). Cross-reference. |
| "For JSON prompts: wrap in a ```json code block. For prose prompts: wrap in a plain ``` code block. For meta-prompts: wrap in a plain ``` code block." (L158–160) | Mechanical rule | **ADOPT.** | Direct adoption. |
| "If the user asks for multiple variations, return them as separate code blocks with a one-line label before each" (L162) | Mechanical rule | **ADOPT.** | Direct adoption. |

#### §1B-A-7 — Quality checklist (source L174–183)

| Element | Source | Disposition | Translation rule |
|---|---|---|---|
| 6-item pre-delivery checklist | Pre-delivery discipline | **ADOPT close to verbatim.** | Aligns with existing DISCIPLINE.md Tier 3 § Pre-Delivery Discipline. Cross-reference. |

#### §1B-A-8 — Example routings (source L185–205)

| Element | Source | Disposition | Translation rule |
|---|---|---|---|
| 6 paired concept→format examples | Worked routing demonstrations | **ADOPT with optional substitution.** | Concrete and useful. Decision per Phase 2 §2C judgment: keep verbatim OR substitute a few with our own. My read leans keep verbatim — pedagogical value comes from the variety, not the specific examples chosen. |

#### §1B-A-9 — Hardcoded-artifact + cross-reference identification

Per Phase 0 §VERIFY 0.1e + 0.1f:
- **Zero share links, UUIDs, character limits, dated artifacts.** Materially cleaner than the marketing-studio source corpus was. No reconciliation needed.
- **Zero cross-references to marketing-studio-director, content-factory, or any Higgsfield surface.** Standalone skill; adopts as standalone sub-skill (Option β consolidated form with static-ads-workflow.md satellite).

#### §1B-A-10 — Source-to-translation cross-reference targets

| Translated section | Cross-references to add | Target |
|---|---|---|
| Capability framing (§1B-A-1) | "→ § Format B for prose register; → DISCIPLINE.md § Pre-Delivery Discipline for the pre-delivery checklist below" | within-doc + skill-library |
| Format A JSON craft (§1B-A-3) | "→ companion `static-ads-workflow.md` § 4 for the ad-recreation variant of structured layout" | satellite |
| Format B prose craft (§1B-A-4) | "→ vocab.md § Composition Vocabulary for spatial-anchoring vocabulary that pairs with cinematic prose" | vocab.md |
| Failure-mode workaround (§1B-A-1) | "→ vocab.md § Visual Style Vocabulary → Film Stock Emulation for the film-photography language family" | vocab.md |
| Quality checklist (§1B-A-7) | "→ DISCIPLINE.md § Pre-Delivery Discipline for the cross-cutting pre-delivery discipline" | skill-library |
| Cross-surface workflow context (§1B-A new §10) | "→ companion `static-ads-workflow.md`; → `skills/higgsfield-marketing-studio/cross-surface-workflow.md` §3 (ms_image / DTC Ads Higgsfield-native alternative)" | satellite + cross-skill |

### §1B-B — static-ads.md translation rules

**Source:** `~/Desktop/EVEN MORE SKILLS/MORE CUSTOM SKILLS/static-ads.md` (316 lines). Disposition class from Phase 0 §VERIFY 0.2f: **TRANSLATE-WITH-VERIFICATION (LOWEST-FRICTION SUB-CLASS).**

#### §1B-B-1 — Brand-folder execution layer

The source assumes a `./brands/[brand-name]/brand-identity/` folder convention with `visual-guidelines.md` + `products.json` + `product-images/`. Our skill library doesn't have this scaffold.

| Source assumption | Disposition | Translation rule |
|---|---|---|
| Brand folder structure | **TRANSLATE AS WORKFLOW RECIPE, NOT AS LITERAL EXECUTION LAYER.** | Frame: "Adil's static-ads recipe assumes a `./brands/[brand-name]/brand-identity/` directory containing `visual-guidelines.md` + `products.json` + `product-images/`. Translate to: 'when running this workflow, you'll need a brand-identity reference document and a product images folder — exact paths and file names depend on your project structure.'" |
| `/brand` slash command (L20–21) | **TRANSLATE AS POINTER, NOT AS DEPENDENCY.** | Source assumes `/brand` exists to bootstrap the brand folder. Our skill doesn't ship `/brand`. Translate: "If your brand-identity files don't exist yet, you'll need to create them before running this workflow." Don't claim `/brand` integration. |
| `WebFetch` calls for product page fetching (L84, L110) | **TRANSLATE AS PATTERN.** | Document the pattern (fetch product page for copy claims, ingredient lists, certifications) without claiming we ship a specific WebFetch tool. |

#### §1B-B-2 — Script dependencies

The source invokes `skills/references/generate-static-ad.py` and `skills/references/generate-reformat.py` — scripts not adopted into our project.

| Source | Disposition | Translation rule |
|---|---|---|
| `python3 skills/references/generate-static-ad.py …` (L238, L255, L280) | **DOCUMENT PATTERN; DO NOT CLAIM FUNCTIONAL SUPPORT.** | Frame: "Adil's static-ads skill includes generation and reformat helper scripts that take the spec.json and call FAL/GPT-image-2 API. Our translation documents the spec.json pattern; users can invoke their own generation pipeline (Higgsfield CLI, MCP, or other) using the spec.json as input." |

#### §1B-B-3 — Production-knowledge claims (highest-falsifiable content)

| Element | Source verbatim | Disposition | Translation rule |
|---|---|---|---|
| Layout zones with fractional coordinates (L56–62) | Named technique + concrete coordinate ranges | **ADOPT close to verbatim.** | Specific, falsifiable, transferable. Translate: "Express each content zone as a fraction of total frame height (0.0 = top, 1.0 = bottom). Standard zone names: `text_zone`, `product_zone`, `button_zone`, `disclaimer_zone`. Concrete example for a calling-screen format: text_zone 0.10–0.35, product_zone 0.40–0.77, button_zone 0.81–0.91, disclaimer_zone 0.91–0.97." |
| Wireframe intermediation (L64–66) | Production technique | **ADOPT close to verbatim — Adil's contribution.** | Translate: "Use the zone fractions to generate a brand-neutral wireframe at the target aspect ratio. The wireframe is what gets passed to the image model as Image 1 — not the original ad. This eliminates color, typeface, and style contamination from the reference, and there is no aspect ratio conflict regardless of source format." This is the workaround technique most worth preserving. |
| Safe-zone top-10%/bottom-10% rule (L223, L229) | Production discipline | **ADOPT close to verbatim — STRONGEST falsifiable claim in the source corpus.** | Translate verbatim: "Keep the top 10% and bottom 10% of the frame free from text, logos, icons, buttons, and UI elements — photographic content such as hands, arms, or product edges entering the frame is fine. This applies to every prompt in every mode — no exceptions." This is the only HARD-RULE volume claim in static-ads.md and it adopts because the underlying premise — Instagram and TikTok's UI overlays consume the top/bottom ~10% of the frame — is verifiable surface fact about platform UI behavior, not craft opinion. The HARD-RULE volume is justified by the platform UI reality the rule responds to. |
| Brand-vs-structure separation (L208–215) | The core operational rule | **ADOPT close to verbatim.** | Translate the two-list rule: "Take from the reference: layout format, zone positions and proportions, UI element types (toggle switches, countdown blocks, iMessage bubbles), element placement and spacing logic. Take from `visual-guidelines.md`: everything visual — background colour, typeface and weights, accent colours (CTA colour, icon colour, badge colour, toggle colours). These always override whatever appears in the reference." |

#### §1B-B-4 — Mode A vs Mode B prompt construction (source L217–229)

| Element | Source | Disposition | Translation rule |
|---|---|---|---|
| Mode A (reference swap) | Conditional logic | **ADOPT close to verbatim.** | When `reference_image` is in spec, pass it as Image 1 with explicit visual-element override prompt. |
| Mode B (text-driven layout) | Conditional logic | **ADOPT close to verbatim.** | When no reference, product images as Image 1+, prompt carries all layout/brand/copy from scratch. |
| Mode-A example prompt template (L223) | Concrete prompt scaffolding | **ADOPT close to verbatim** as quoted example in fenced text block. |

#### §1B-B-5 — Three worked template examples (source L301–316)

| Template | Source | Disposition | Translation rule |
|---|---|---|---|
| iMessage / DM Conversation | L306–308 | **ADOPT as quoted example.** | Preserve verbatim with bracketed placeholders `[FIRST NAME]`, `[OPENING LINE]`, `[BRAND]`, etc. Pedagogical value comes from the dense specification. |
| Scarcity / Countdown Urgency | L310–312 | **ADOPT as quoted example.** | Same. |
| Ingredient Spotlight / Clean Label | L314–316 | **ADOPT as quoted example.** | Same. |

#### §1B-B-6 — Hardcoded-artifact + cross-reference identification

- **No share links, UUIDs, character limits, dated artifacts.** Workflow-shape content; clean provenance.
- **Internal cross-references to brand folder paths only.** Translated per §1B-B-1 as workflow recipe, not literal paths.

#### §1B-B-7 — Source-to-translation cross-reference targets

| Translated section | Cross-references to add | Target |
|---|---|---|
| Layout zones (§1B-B-3 fractional coordinates) | "→ parent SKILL.md § Format A for JSON layout precision in non-ad contexts" | parent |
| Wireframe intermediation (§1B-B-3) | "→ parent SKILL.md § Format A for JSON layout discipline" | parent |
| Safe-zone rule (§1B-B-3) | "→ vocab.md § Composition Vocabulary → Spatial Zoning for the broader vocabulary of named regions" | vocab.md |
| Brand-vs-structure separation (§1B-B-3) | "→ skills/higgsfield-marketing-studio/cross-surface-workflow.md §2 Adil's 4-surface recipe (similar brand-identity reuse pattern in a different surface)" | cross-skill |
| Three worked template examples (§1B-B-5) | "→ parent SKILL.md § Format A example for the simpler JSON shape" | parent |
| Mode A/B prompt construction (§1B-B-4) | "→ parent SKILL.md § Format A craft patterns for the general prompt-craft scaffolding underlying Mode B's text-driven layout" | parent |

---

## §1C — ms_image / DTC Ads cross-surface-workflow.md §3 expansion content scope

**Source-evidence boundary LOCKED.** Content stays within Phase 0 §VERIFY 0.3 evidence + Adil-corpus naming + the existing brief at cross-surface-workflow.md L48–60. **No fabrication of detail beyond evidence.**

### §1C-a — Evidence inventory

| Evidence source | Specific content available |
|---|---|
| `.planning/v3.7.13/PHASE-0-PROBES.md` Probe 0.3-a (L180–245) | Full `ms_image` model JSON schema from live `models_explore(action='search', query='marketing studio')` introspection. Includes: model `id`, `name`, `description`, `output_type`, full `parameters` array (style_id required, brand_kit_id optional, resolution optional default "1k", quality optional default "low", batch_size optional max 20, folder_id optional), `medias` (max 14 image roles), 15 aspect ratios listed verbatim, tags array. |
| `cross-surface-workflow.md` L53–57 (existing) | "Brand-kit-aware (accepts `brand_kit_id`), ad-format curated (accepts `style_id`), batch generation up to 20 images per call, max 14 reference media per generation. Adil's source corpus doesn't document ms_image at all — source-corpus reconciliation #12." |
| `cross-surface-workflow.md` L55–57 (existing) | "When to recommend which path: If brand-kit awareness matters (consistent typography, color palette, logo placement across many generated images), `ms_image` is the more integrated option — that's its differentiator over GPT Image 2.0." |
| `cross-surface-workflow.md` L57 (existing) | "Naming reminder: refer to it as 'DTC Ads.' The model ID `ms_image` is internal nomenclature; the user-facing brand name is DTC Ads." |
| `higgsfield-marketing-studio/SKILL.md` L46–58 table (existing) | Three Marketing Studio models named in a table; `ms_image` row gives one-sentence summary. |
| `higgsfield-marketing-studio/SKILL.md` L55 (existing) | Naming rule quoted from MCP tool description. |
| `.planning/v3.7.13/PHASE-0-PROBES.md` L21 (existing) | "New entity types beyond source corpus: `ad_reference`, `brand_kit`, `image_style`/`ad_format`, plus `webproduct` vs `product` distinction" — the `brand_kit` entity that `ms_image`'s `brand_kit_id` references. |

**Total evidence:** ~250 words of substantive content + the full JSON schema. Adequate to expand §3 from ~80 words to ~400–600 words **without fabrication.**

### §1C-b — §3 expansion structure (locked)

The existing §3 "Brand-identity assets stage (image-side surfaces)" is reorganized into sub-sections to accommodate the expansion:

| Sub-section | Content scope | LoC est | Evidence source |
|---|---|---|---|
| §3 opening | Unchanged. "Stage 1 of the recipe — brand-identity assets — has two valid paths through Higgsfield." | ~3 | existing |
| §3.a — Path A (Adil's actual recipe) | Unchanged. Brief description + pointer to existing §3 worked examples. | ~5 | existing |
| §3.b — Path B (`ms_image` / "DTC Ads") | **EXPANDED.** Three sub-sections per §1C-c below. | ~50–70 | Probe 0.3-a + existing §3 |
| §3.b.i — Capability summary | Brand-kit awareness, ad-format style routing, batch generation, reference-media capacity — what makes `ms_image` distinct from GPT Image 2.0 | ~15–20 | Probe 0.3-a + existing brief |
| §3.b.ii — Parameter schema | The full parameter list from Probe 0.3-a verbatim: `style_id` (required), `brand_kit_id` (optional), `resolution` (1k/2k/4k default 1k), `quality` (low/medium/high default low), `batch_size` (1–20, default 1), `folder_id` (optional). Aspect ratios: 15 supported per Probe 0.3-a (verbatim list). Media: max 14 image-role items. | ~20–25 | Probe 0.3-a |
| §3.b.iii — When to recommend `ms_image` over GPT Image 2.0 | Brand-kit-consistency-matters trigger; batch-of-many-images trigger. **Frame as decision heuristic, not as universal rule** — Adil didn't use ms_image in his demos, which is itself signal. Calmer register than the GPT-Image-2 path. | ~15–20 | existing §3 + Probe 0.3-a |
| §3.b.iv — Naming reminder | "Refer to it as 'DTC Ads.' The model ID `ms_image` is internal nomenclature." | ~5 | existing + MCP tool description quoted at SKILL.md L55 |
| §3.b.v — Source-corpus reconciliation #12 | Preserved verbatim. Adil's source corpus doesn't document this surface. | ~5 | existing |

### §1C-c — Explicit non-fabrication discipline

**What we DO write into the expansion:**
- Parameter schema verbatim from Probe 0.3-a JSON
- Capability summary derived directly from the schema (e.g., "brand_kit_id parameter accepts a brand kit UUID — this is the brand-kit-awareness capability")
- Naming rule quoted from the existing MCP tool description
- Decision heuristic for when to recommend (already in existing §3, just expanded)
- Honest note that Adil's source corpus doesn't document ms_image

**What we DO NOT write into the expansion:**
- Worked examples of ms_image generations (we have none — no source corpus, no demo evidence)
- Sample brand_kit_id or style_id UUIDs (we have no observed instances; placeholder UUIDs would mislead)
- Pricing claims for ms_image specifically (Marketing Studio video pricing is documented elsewhere; ms_image has no separate pricing signal in Phase 0 evidence — explicit "pricing not separately documented for ms_image" note)
- Capability claims beyond the parameter schema (e.g., "ms_image produces 4k output with better text rendering than GPT Image 2.0" — we have no evidence)
- Specific ad-format style names (style_id is required but no style enumeration is in Probe 0.3-a evidence; flag for "live enumeration discipline" same as hooks/settings in marketing-studio SKILL.md §4)

**Phase 1 §1C reconfirms Phase 0 §VERIFY 0.3's discipline:** ms_image expansion is content within evidence boundary, not net-new authoring of unverified claims.

### §1C-d — Live-enumeration discipline parallel

The existing higgsfield-marketing-studio SKILL.md §4 has a "Live-enumeration discipline" callout for hooks + settings ("The picklist names listed above are a 2026-05-18 snapshot. New hooks and settings get added; existing ones can be revised. For production work — especially when documenting a campaign or building a multi-shot plan — call the live enumeration first and pull the current UUIDs."). The §3.b expansion gets a parallel callout for `style_id` + `brand_kit_id` enumeration: "Style and brand-kit IDs are user-specific (brand-kit) and platform-managed (style). For canonical current values, call `show_marketing_studio(action='list', type='brand_kit')` and the equivalent for style enumeration. Hardcoded UUIDs from this doc are not appropriate; the parameter schema is what's stable."

This reuses the v3.7.13 live-enumeration discipline pattern, which is itself reuse-precedent (the discipline first surfaced in marketing-studio SKILL.md §4 hooks/settings; reapplying it to brand_kits/styles is the same discipline at a different surface).

---

## §1D — Infrastructure design specifics

### §1D-1 — DVSM swap (item 6)

Per Phase 0 §VERIFY 0.4 + D-PHASE-0-2.

**Bundle location:** `assets/fonts/DejaVuSansMono.ttf` (333 KB regular weight; no bold / oblique / bold-oblique).

**Font alias:** `Mono` (new), parallel to existing `Body` alias for DVC family.

**add_font registration:** insert after the existing 3 `Body` registrations at `generate_user_guide.py:101–103`:
```python
self.add_font("Body", "",  str(FONT_DIR / "DejaVuSansCondensed.ttf"))
self.add_font("Body", "B", str(FONT_DIR / "DejaVuSansCondensed-Bold.ttf"))
self.add_font("Body", "I", str(FONT_DIR / "DejaVuSansCondensed-Oblique.ttf"))
self.add_font("Mono", "", str(FONT_DIR / "DejaVuSansMono.ttf"))   # NEW
```

**Courier→Mono swap site:** ONE site only — `code_block` method at `generate_user_guide.py:156`:
```python
# OLD
self.set_font("Courier", "", 9)
# NEW
self.set_font("Mono", "", 9)
```

**Grep confirmation:** `grep -nE "Courier|set_font|add_font" generate_user_guide.py` returns 22 matches: 1 set_font("Courier", ...) call at L156, 21 set_font("Body", ...) calls (untouched). Zero Courier usage anywhere else.

**LoC delta:** +1 (add_font) + token swap. Total: 1 LoC actually added; 1 token swap.

### §1D-2 — `--dry-run` exit-code matrix (item 7)

Per Phase 0 §VERIFY 0.5 D5-A design + D-PHASE-0-3.

**Exit code assignments:**

| Code | Class | Trigger |
|---|---|---|
| 0 | OK | `build_pdf()` returns normally |
| 1 | Unknown | Any uncaught exception class |
| 2 | Frontmatter | `read_root_metadata()` raises `FrontmatterError` (no YAML block found, or required field missing) |
| 3 | Dict-parity | `build_pdf()` raises `DictParityError` (filesystem walk of `skills/` mismatches `SUB_SKILL_DESCRIPTIONS` dict) |
| 4 | Font | `add_font()` raises (font file missing, malformed TTF, etc.) — wrapped to `FontError` |
| 5 | Render | `FPDFUnicodeEncodingException` or other fpdf2 rendering exception — wrapped to `RenderError` |
| 6 | Output | `pdf.output(...)` raises (disk full, permission, path missing) — wrapped to `OutputWriteError`. N/A under `--dry-run` (skipped). |

**Implementation pattern:**
- 5 named exception classes at top-of-file
- 7 exit-code constants (`EXIT_OK` through `EXIT_OUTPUT`)
- Re-raise wrappers at the 5 known failure points
- argparse harness in `__main__` mapping exception class → exit code with stderr message

**Documentation surfaces:**
- Module docstring (updated, see §1A `generate_user_guide.py` site #5)
- argparse `--help` text (one-liner exit-code summary in the `--dry-run` flag's `help=`)

**LoC delta:** ~+45 LoC total (constants + classes + re-raise wrappers + harness + docstring).

### §1D-3 — `validate.py` subprocess integration (item 5)

Per Phase 0 §VERIFY 0.6 design 6-A + 6-i + D-PHASE-0-4.

**Position:** Append as Phase 4 after Phase 3 (root files), before summary. Insertion at `validate.py:144` (between existing root-file check loop and summary).

**Integration shape:** Unconditional subprocess invocation (no `--with-dry-run` opt-in flag). Binary exit-code mapping (returncode 0 = PASS; non-zero = FAIL). First-line stderr capture for diagnostic context.

**Error-handling shape:**
- `result.returncode == 0` → `check(True, ...)` → PASS
- `result.returncode != 0` → `check(False, ..., f"exit {result.returncode}; stderr: {stderr_excerpt[:150]}")` → FAIL with the stderr first-line excerpt
- This means validate.py decouples from the exit-code matrix designed in §1D-2: validate.py treats all non-zero as failure but surfaces the failure-class label that `generate_user_guide.py --dry-run` prints to stderr (FRONTMATTER ERROR / DICT-PARITY ERROR / FONT ERROR / RENDER ERROR / OUTPUT-WRITE ERROR / UNKNOWN ERROR). User gets the failure class without validate.py needing to mirror the exit-code matrix.

**Timeout:** 60 seconds (subprocess `timeout=60` parameter). Real wall-clock for `--dry-run` is ~1.5s; 60s ceiling catches hung-subprocess pathology.

**LoC delta:** +15 LoC inside `main()`.

---

## §1E — Cross-reference 3-site disposition

Per Phase 0 §VERIFY 0.7b + D-PHASE-0-6. Three sub-sites ship; 6 others descope to v3.7.17+ backlog.

### §1E-1 — `templates/seedance/multi-character-anchor.md` L80

**Existing (L78–81):**
```
**GREAT:** Use the template, fill every field including percentage
notation paired with qualitative anchors, specify cross-character
relationships (distance + eyeline + crossing rule + negative space).
Pre-visualize the scene with `top-down-map.md` first and paste the
```

**Proposed change (modify L80 to extend the parenthetical):**
```
**GREAT:** Use the template, fill every field including percentage
notation paired with qualitative anchors, specify cross-character
relationships (distance + eyeline + crossing rule + negative space —
see [vocab.md](../../vocab.md) § Composition Vocabulary → Crossing rule
+ § Negative space). Pre-visualize the scene with `top-down-map.md` first
and paste the
```

**Net delta:** +1 line (the parenthetical extension wraps onto a new line at ~80-char width).

### §1E-2 — `templates/seedance/worked-example-two-character.md` L68

**Existing (L66–69):**
```
- Every `multi-character-anchor.md` field filled — including cross-
  character relationships (distance + eyeline + crossing rule +
  negative space) per § Spatial Layout Block in the seedance SKILL.md
```

**Proposed change (extend existing reference with vocab.md citation):**
```
- Every `multi-character-anchor.md` field filled — including cross-
  character relationships (distance + eyeline + crossing rule +
  negative space) per § Spatial Layout Block in the seedance SKILL.md
  + [vocab.md](../../vocab.md) § Composition Vocabulary → Crossing
  rule + § Negative space
```

**Net delta:** +2 lines.

### §1E-3 — `skills/higgsfield-seedance/SKILL.md` L488

**Existing (L486–489):**
```
... model treats them as directorial
intent — the same way a DP reads "right third" on a storyboard —
not as pixel-exact targets. Use them alongside the rest of the
standard composition vocabulary (`over-the-shoulder`, `eye line`,
`ground contact`, `headroom`, `nose room`, `crossing rule`) rather
than as a substitute for it.
```

**Proposed change (extend inline vocabulary parenthetical):**
```
... model treats them as directorial
intent — the same way a DP reads "right third" on a storyboard —
not as pixel-exact targets. Use them alongside the rest of the
standard composition vocabulary (`over-the-shoulder`, `eye line`,
`ground contact`, `headroom`, `nose room`, `crossing rule` — the last
formalized at [vocab.md](../../vocab.md) § Composition Vocabulary →
Crossing rule) rather than as a substitute for it.
```

**Net delta:** +2 lines.

### §1E-4 — Aggregate cross-reference cite delta

**Total Phase 2 §2F edits:** 3 files, ~+5 lines total. Mechanical edits; no prose authoring.

### §1E-5 — Descoped 6 sub-sites (NOT shipped in v3.7.16)

For v3.7.17+ backlog:
- 12.1: `templates/10-dance-music-performance.md` L32 — awkward cite shape (table cell)
- 12.2: `templates/seedance/multi-character-anchor.md` L38 — cite-target inside fenced code block
- 12.3: `templates/seedance/multi-character-anchor.md` L40 — cite-target inside fenced code block
- 12.5: `templates/seedance/worked-example-two-character.md` L44/L46/L62 — cite-targets inside fenced code block (worked-example prompt body)
- 12.8: `skills/higgsfield-camera/SKILL.md` — Camera Contract integration → requires prose authoring
- 12.9: `skills/higgsfield-prompt/SKILL.md` — MCSLA Action layer integration → requires prose authoring

These earn their own scope as a future "sub-skill cross-reference review" arc.

---

## §1F — Sub-phase 2 ordering with STOPs

**Phase 2 is the most complex v3.7.x phase to date.** 13 sub-phases reflect the actual mega-scope. Each sub-phase has a focused goal and a clear STOP point. Estimated total Phase 2 effort: 2-3 sessions depending on prose-composition pace.

### 2A — Bundle DVSM + apply Courier→Mono swap + register exit-code matrix scaffolding

**Smallest blast radius. Goes first to establish infrastructure before content depends on it.**

Steps:
1. Copy `DejaVuSansMono.ttf` (333 KB) from `/tmp/dejavu-test/dejavu-fonts-ttf-2.37/ttf/` to `assets/fonts/DejaVuSansMono.ttf` (only the regular weight).
2. Update `assets/fonts/README.md` to add the DVSM rationale note (~+5 LoC).
3. Edit `generate_user_guide.py:101–103` area — insert new `add_font("Mono", ...)` line (per §1D-1).
4. Edit `generate_user_guide.py:156` — swap `set_font("Courier", "", 9)` → `set_font("Mono", "", 9)`.
5. Edit `generate_user_guide.py` top-of-file (after imports, ~L17) — add 5 named exception classes + 7 exit-code constants.
6. Edit `generate_user_guide.py:29, L37` — convert `raise RuntimeError(...)` in `read_root_metadata()` to `raise FrontmatterError(...)`.
7. Edit `generate_user_guide.py:1200` — convert `raise RuntimeError(...)` dict-parity check to `raise DictParityError(...)`.
8. Wrap `add_font` calls (now 4 calls) in try/except, re-raise as `FontError`.
9. Wrap `pdf.output(...)` at L1263 in try/except, re-raise as `OutputWriteError`.
10. Edit `__main__` block (L1267 onward) — full argparse + try/except harness per §1D-2.
11. Edit module docstring (top-of-file) — add exit-code summary section.
12. Run `python3 generate_user_guide.py --dry-run` — confirm exit 0.
13. Quick smoke: `python3 generate_user_guide.py` (full run) — confirm exit 0, PDF generated.

**STOP for infrastructure review.** This is the only point where infrastructure changes could destabilize the build. User reviews before content sub-phases begin to ensure the PDF generation pipeline is healthy.

### 2B — validate.py subprocess integration

Depends on 2A (exit-code matrix needs to exist before validate.py invokes it).

Steps:
1. Edit `validate.py:144` area — insert new Phase 4 PDF-dry-run check (per §1D-3).
2. Add `import subprocess` if not already at the top (existing imports are at L17–20; subprocess can be a local import inside `main()` since it's only used there — Phase 2 picks).
3. Run `python3 validate.py` — confirm:
   - All existing checks pass
   - New `[ PDF DRY-RUN SMOKE ]` phase appears
   - generate_user_guide.py --dry-run reports exit 0
   - Summary still shows ALL CHECKS PASSED

**STOP for validation gate review.** This is the new pre-release gate; confirm it works end-to-end before adding the larger content surfaces.

### 2C — NEW skills/higgsfield-gpt-image-2/SKILL.md

**The largest content sub-phase.** ~400–500 lines of new prose. Apply §1B-A translation rules mechanically.

Steps:
1. Create directory `skills/higgsfield-gpt-image-2/`.
2. Create `SKILL.md` with frontmatter + 11 sections per the §1A structure table.
3. Compose each section per §1B-A per-element translation rules.
4. Run `python3 validate.py` — confirm new SKILL.md passes frontmatter + cross-reference checks. (Note: the new SKILL.md may surface relative-path failures if it references files not yet existing; the satellite is created in 2D.)
5. Visual review of the prose for register-consistency with v3.7.13/15 voice.
6. Produce a per-section verification table inline with the STOP report. For each row of §1B-A, show:
   - Source element (per §1B-A row reference)
   - Composed prose location (line range in the new SKILL.md)
   - Translation rule applied (ADOPT verbatim / DOWNGRADE per testability / EXTRACT / DISCARD)
   - Confirmation that the §1B-A row's discipline label matched what was composed

   Same pattern as v3.7.15's §1G table → composed-prose verification report. This makes 2C's STOP reviewable without re-reading 400-500 lines of prose for compliance.

**STOP for content review.** Largest judgment-call sub-phase. User reviews the new sub-skill + the §1B-A verification table from step 6 before satellite + cross-surface expansion compounds further.

### 2D — NEW skills/higgsfield-gpt-image-2/static-ads-workflow.md

Depends on 2C (parent SKILL.md needs to exist for satellite to reference it).

Steps:
1. Create `static-ads-workflow.md` with frontmatter + 9 sections per the §1A structure table.
2. Compose each section per §1B-B per-element translation rules.
3. Run `python3 validate.py` — confirm satellite cross-references resolve.

**STOP for satellite review.** Same judgment-call surface as 2C, smaller scope; user catches register drift before downstream cross-references depend on the satellite's section names.

### 2E — cross-surface-workflow.md §3 ms_image expansion

Depends on 2C (parent gpt-image-2 SKILL.md needs to exist so the §3 expansion's cross-reference to it resolves).

Steps:
1. Edit `skills/higgsfield-marketing-studio/cross-surface-workflow.md` §3 — restructure into §3 / §3.a / §3.b.i–v per §1C structure.
2. Compose §3.b.i–v content within source-evidence boundary per §1C-c.
3. Add live-enumeration discipline callout per §1C-d.
4. Add cross-reference back to new `higgsfield-gpt-image-2/SKILL.md` and `static-ads-workflow.md` from §3.a (Adil's Path A pattern doesn't need to change; new pointer is for navigation).
5. Run `python3 validate.py` — confirm cross-reference health.

**STOP if any §3.b content drifts beyond source-evidence boundary** — surface the drift for user review before committing fabricated content. §1C is the rule; §1C-c is the explicit DO-NOT-WRITE list.

### 2F — 3 cross-reference site additions

Mechanical. Depends on 2C/2D in the sense that any new vocab.md or sub-skill sections referenced from the cite sites must exist — but the 3 cite sites all point at EXISTING vocab.md sections (Composition Vocabulary → Crossing rule, Negative space), so no upstream dependency.

Steps:
1. Edit `templates/seedance/multi-character-anchor.md` L80 per §1E-1.
2. Edit `templates/seedance/worked-example-two-character.md` L68 per §1E-2.
3. Edit `skills/higgsfield-seedance/SKILL.md` L488 per §1E-3.
4. Run `python3 validate.py` — confirm cross-references resolve.

### 2G — FAQ paragraph refresh

Depends on knowing v3.7.16 will ship + release count + version.

Steps:
1. Edit `generate_user_guide.py:1236` area — refresh the FAQ paragraph per §1A site #3.
2. **Phase 2 judgment call:** minimum-viable refresh (2 token swaps) OR substantive refresh (~+5 LoC with v3.7.13–v3.7.16 era summary clause). My read leans substantive — the existing prose ends on v3.7.12 and skipping 4 releases of era summary is noticeable.
3. Quick re-run: `python3 generate_user_guide.py --dry-run` — confirm exit 0.

### 2H — SUB_SKILL_DESCRIPTIONS + Section 24 PDF row

Depends on 2C (new sub-skill needs to exist on filesystem before its descriptor lands in the dict, or the dict-parity check fires).

Steps:
1. Edit `generate_user_guide.py:68–91` — add `higgsfield-gpt-image-2` entry to `SUB_SKILL_DESCRIPTIONS` dict (per §1A site #4). Verify against 71-char ceiling.
2. Run `python3 generate_user_guide.py --dry-run` — confirm dict-parity check passes (filesystem walk should now include the new sub-skill, and the dict now has its entry).
3. Section 24 row is auto-generated from the dict; no separate edit needed.

### 2I — Version cascade + CHANGELOG draft

Mechanical edits + prose composition.

Steps:
1. Root `SKILL.md` frontmatter: version `3.7.15` → `3.7.16`, updated date.
2. README.md badge: version cascade.
3. README.md footer: version + updated date cascade.
4. Insert new v3.7.16 entry above v3.7.15 entry in `CHANGELOG.md` (Phase 2I composes per §1A CHANGELOG sketch).
5. Run `python3 validate.py` — confirm clean.

### 2J — PDF regen + visual check

Mechanical. Depends on all upstream changes being in place.

Steps:
1. `python3 generate_user_guide.py --dry-run` — exit 0 expected (gates the regen).
2. `python3 generate_user_guide.py` — exit clean, ~29 pages expected (1 more than v3.7.15 due to new SUB_SKILL_DESCRIPTIONS entry).
3. Open `docs/user-guide/USER-GUIDE.pdf` in viewer:
   - Page 1 version header reads `v3.7.16`
   - Page 1 footer date matches root SKILL.md frontmatter
   - Section 24 includes `higgsfield-gpt-image-2` row
   - FAQ paragraph reflects v3.7.16 (count + version updated)
   - Code blocks render in DVSM (no Courier fallback)

**STOP if page count is anything other than ~29.** Drift outside ±1 from the expected count signals layout reflow that needs investigation. Per v3.7.14 / v3.7.15 substrate, the descope criterion remains: if 2J surfaces page-count drift attributable to DVSM (not to the SUB_SKILL_DESCRIPTIONS addition), descope the DVSM swap and ship v3.7.16 without it.

### 2K — Validator re-baseline

Mechanical.

Steps:
1. `cp docs/user-guide/USER-GUIDE.pdf docs/user-guide/USER-GUIDE.pdf.baseline-v3.7.16`.
2. Edit `validate_user_guide.py` `DEFAULT_BASELINE`: `USER-GUIDE.pdf.baseline-v3.7.15` → `USER-GUIDE.pdf.baseline-v3.7.16` (one-line edit at L98).
3. Run `python3 validate_user_guide.py` — confirm VALIDATION PASSED (candidate = baseline copy).

### 2L — Full validation pass

Mechanical. The gate before final review.

Steps:
1. `python3 validate.py` — ALL CHECKS PASSED (including new Phase 4 PDF-dry-run smoke).
2. `python3 generate_user_guide.py --dry-run` — exit 0.
3. `python3 validate_user_guide.py` — VALIDATION PASSED against new baseline.

**STOP for final review.**

### 2M — Final repo-wide diff review

Steps:
1. `git status` — confirm only expected files surfaced (~17 files modified/created per §1A total delta).
2. `git diff --stat` — confirm LoC delta roughly matches §1A's `+990 to +1250 lines` estimate (gpt-image-2/ subdirectory + cross-surface-workflow.md + CHANGELOG.md dominate).
3. Confirm no out-of-scope edits leaked (e.g., no accidental edits to other sub-skills, no PDF baseline files for older versions).
4. Confirm new files all present: 2 new skills/higgsfield-gpt-image-2/* files + 1 new asset (font) + 1 new PDF baseline + 1 new PHASE-1 inventory.
5. User approval before commit.

Commit format per project convention: `feat: v3.7.16 — MEGA: gpt-image-2-director sub-skill + static-ads satellite + ms_image §3 expansion + DVSM + exit-code matrix + validate.py subprocess + 3 cross-refs`.

After merge: git tag + GitHub release per the project convention surfaced in memory (`feedback_github_releases.md`, `feedback_release_workflow.md`).

---

## §1G — Decisions register

Numbered locks per the v3.7.13 → v3.7.14 → v3.7.15 convention. Each lock is one row. Phase-0 decisions D-PHASE-0-* carried forward.

| # | Decision | Source | Status |
|---|---|---|---|
| **D-PHASE-0-1** | Architectural Option β — consolidated `higgsfield-gpt-image-2/` sub-skill with `static-ads-workflow.md` satellite + ms_image as cross-surface-workflow.md §3 expansion. 1 new sub-skill, not 3 | Phase 0 §VERIFY 0.3d + closing | LOCKED |
| **D-PHASE-0-2** | DVSM ships — regular weight only (333 KB), new `Mono` font alias, 2-LoC swap site | Phase 0 §VERIFY 0.4 | LOCKED |
| **D-PHASE-0-3** | --dry-run exit-code matrix per Phase 0 §VERIFY 0.5 design D5-A — 5 named exception classes + 7 exit-code constants + argparse harness | Phase 0 §VERIFY 0.5 | LOCKED |
| **D-PHASE-0-4** | validate.py subprocess integration per Phase 0 §VERIFY 0.6 design 6-A + 6-i — append as Phase 4, binary returncode mapping, stderr first-line excerpt for diagnostic | Phase 0 §VERIFY 0.6 | LOCKED |
| **D-PHASE-0-5** | FAQ paragraph refresh — update count + version. Phase 2 §2G picks between minimum-viable (2 tokens) and substantive (+5 LoC era summary) | Phase 0 §VERIFY 0.7a | LOCKED with Phase-2 picks |
| **D-PHASE-0-6** | Item 12 ships 3 cross-reference sites (multi-character-anchor.md L80, worked-example L68, higgsfield-seedance L488). Other 6 descope to v3.7.17+ backlog | Phase 0 §VERIFY 0.7b | LOCKED |
| **D-PHASE-0-7** | Item 13 (DISCIPLINE.md boundary-condition framing pattern naming) descopes to v3.7.17. Re-eligible if Phase 1+ surfaces second instance | Phase 0 §VERIFY 0.7c | LOCKED |
| **D-PHASE-0-8** | Substrate inheritance unchanged — v3.7.14 DVC + --dry-run + .planning/<version>/ convention + v3.7.15 per-claim register-downgrade discipline | Phase 0 closing | LOCKED |
| D1 | Arc shape — minor release v3.7.16, MEGA scope, content-translation + infrastructure mix | Phase 0 closing | LOCKED |
| D2 | Disposition for items 1 + 3 — TRANSLATE-WITH-VERIFICATION (item 1 LOWER-FRICTION SUB-CLASS; item 3 LOWEST-FRICTION SUB-CLASS) | Phase 0 §VERIFY 0.1i + 0.2f | LOCKED |
| D3 | Disposition for item 2 (ms_image §3 expansion) — content within Probe 0.3-a + existing brief evidence boundary; no fabrication beyond evidence | Phase 1 §1C | LOCKED |
| D4 | gpt-image-2-director.md per-element translation rules per §1B-A. Capability framing ADOPT close to verbatim; format craft patterns ADOPT close to verbatim; downgrade only the "templateable slots are slot-required" reach to a heuristic. Worked examples: Phase 2 picks adopt-verbatim vs substitute | Phase 1 §1B-A | LOCKED with Phase-2 picks on worked-examples |
| D5 | static-ads.md per-element translation rules per §1B-B. Production-knowledge content (fractional coordinates / safe-zones / brand-vs-structure) ADOPT close to verbatim. Brand-folder execution layer TRANSLATE AS WORKFLOW RECIPE; script dependencies DOCUMENT PATTERN | Phase 1 §1B-B | LOCKED |
| D6 | ms_image §3 expansion structure — opens §3 / §3.a / §3.b.i–v sub-section structure within Path A / Path B framing. Source-evidence boundary explicit per §1C-c | Phase 1 §1C | LOCKED |
| D7 | DVSM Mono font alias — single new alias parallel to Body. Only `code_block` at L156 swaps from Courier. Bundle only regular weight (333 KB) | Phase 1 §1D-1 | LOCKED |
| D8 | Exit-code matrix design — D5-A from Phase 0 (5 named exception classes + 7 exit-code constants + 5 re-raise wrappers + argparse harness in `__main__`) | Phase 1 §1D-2 | LOCKED |
| D9 | validate.py integration — Phase 4 position; binary returncode mapping; subprocess timeout=60s; stderr first-line excerpt | Phase 1 §1D-3 | LOCKED |
| D10 | Cross-reference 3 sub-sites exact prose per §1E-1, §1E-2, §1E-3 | Phase 1 §1E | LOCKED |
| D11 | Phase 2 sub-phase ordering with STOPs — 13 sub-phases (2A–2M) with explicit STOP points at 2A (infrastructure review), 2B (validate gate review), 2C (largest content review), 2D (satellite review), 2E (descope trigger if §3.b drifts beyond evidence), 2J (page count drift descope trigger), 2L (final review), 2M (final diff review) | Phase 1 §1F | LOCKED |
| D12 | Phase 2 FAQ refresh judgment — Phase 2 §2G picks between minimum-viable and substantive. Recommend substantive (era summary noticeable to skip 4 releases) | Phase 1 §1A site #3 | LOCKED with Phase-2 picks |
| D13 | Phase 2 worked-example substitution judgment — Phase 2 §2C / §2D pick whether to preserve Adil's brand-name placeholders (AURA, etc.) or substitute. Recommend preserve verbatim (variety is the pedagogical value) | Phase 1 §1B-A-3, §1B-A-4, §1B-A-8 | LOCKED with Phase-2 picks |
| D14 | Source attribution per v3.7.13 / v3.7.15 attribution convention — Adil Aliyev credited in CHANGELOG (Source attribution section), at top of new SKILL.md + satellite (1-line citation each), and in PHASE-0 / PHASE-1 verification artifacts | Phase 1 §1A | LOCKED |
| D15 | Out-of-scope items surfaced — items 12.1, 12.2, 12.3, 12.5, 12.8, 12.9 (6 of 9 cross-reference sub-sites) and item 13 (DISCIPLINE.md pattern naming) deferred to v3.7.17+. Backlog entry: "Sub-skill cross-reference review arc — earns its own scope" | Phase 0 §VERIFY 0.7 + Phase 1 §1E-5 | LOCKED-AS-DEFERRED |
| D16 | Live-enumeration discipline reuse — §3.b.iv applies the existing v3.7.13 live-enumeration discipline pattern (already used for hooks + settings in marketing-studio SKILL.md §4) to ms_image's style_id + brand_kit_id parameters | Phase 1 §1C-d | LOCKED |
| D17 | Source-corpus reconciliation #12 preserved — ms_image expansion explicitly notes that Adil's source corpus doesn't document this surface. Reuses v3.7.13 reconciliation register | Phase 1 §1C-b §3.b.v | LOCKED |
| D18 | PDF page-count drift descope trigger — if Phase 2 §2J shows page count outside ±1 of expected ~29 (driven only by new SUB_SKILL_DESCRIPTIONS entry), surface as DVSM descope candidate before continuing | Phase 1 §1F sub-phase 2J | LOCKED |
| D19 | ms_image fabrication prohibition — explicit DO-NOT-WRITE list per §1C-c (no worked examples, no sample UUIDs, no pricing claims, no capability claims beyond schema, no specific style enumeration). Phase 2 §2E STOP point enforces | Phase 1 §1C-c | LOCKED |
| D20 | Mega-release commit format — single commit covering all sub-phases per project convention: `feat: v3.7.16 — MEGA: gpt-image-2-director sub-skill + static-ads satellite + ms_image §3 expansion + DVSM + exit-code matrix + validate.py subprocess + 3 cross-refs` | Phase 1 §1F sub-phase 2M | LOCKED |

---

## Phase 1 closing summary

**Scope verified:** 1 new sub-skill directory with 2 files (SKILL.md + static-ads-workflow.md satellite) + 1 cross-surface-workflow.md §3 expansion within source-evidence boundary + 1 font bundle + 3 infrastructure changes (DVSM swap + exit-code matrix + validate.py subprocess) + 1 PDF FAQ refresh + 3 cross-reference cite additions + standard version cascade + PDF regen + new validator baseline.

**Total markdown LoC delta:** ~+990 to +1250 lines. Mega-release-scale. Substantially larger than v3.7.15 (~+230–250) but smaller than v3.7.13's higgsfield-marketing-studio creation arc (~+1600).

**Architectural lock:** Option β confirmed throughout — items 1 + 3 consolidate under one `higgsfield-gpt-image-2/` umbrella with satellite, mirroring the proven marketing-studio + cross-surface-workflow.md pattern.

**Descope option remains open through Phase 1:** Phase 1 evidence has surfaced TWO additional descope candidates not surfaced in Phase 0:
1. **(potential) FAQ paragraph substantive refresh** — Phase 2 §2G may pick minimum-viable instead. Not really a descope; user-judgment call documented in D12.
2. **(potential) Worked-example substitution** — Phase 2 §2C / §2D may pick adopt-verbatim instead of substitute. Not a descope; user-judgment call documented in D13.

No Phase 1 evidence surfaces a scope-too-large descope signal beyond what Phase 0 already identified.

**Source-evidence discipline reaffirmed for §3 expansion:** D19's explicit DO-NOT-WRITE list (no worked examples, no sample UUIDs, no pricing claims, no capability claims beyond schema) operationalizes the plausibility-over-verification discipline at the highest-risk content-fabrication surface in the release. §1C-c is the contract; Phase 2 §2E STOP point enforces.

**Per-element translation rules:** locked in §1B-A (gpt-image-2-director) and §1B-B (static-ads). Phase 2 composes prose mechanically following the per-element ADOPT/DOWNGRADE tables. Two Phase-2 judgment-call points documented (D12 FAQ refresh shape, D13 worked-example substitution).

**Estimated total Phase 2 effort:** 2-3 sessions across 13 sub-phases. 2C (new SKILL.md content composition) is the largest single-session sub-phase. 2A/2B (infrastructure) are session-front-load to establish the substrate before content compounds.

**Open user decisions before Phase 2A:**
- Confirm or override D12 (FAQ refresh shape — minimum-viable vs substantive)
- Confirm or override D13 (worked-example substitution — preserve Adil's placeholders vs substitute our own)
- Any per-element translation-rule overrides in §1B-A or §1B-B
- Confirm D18 page-count descope trigger threshold (±1 from ~29)

---

**STOP. Awaiting user review before Phase 2A begins.**
