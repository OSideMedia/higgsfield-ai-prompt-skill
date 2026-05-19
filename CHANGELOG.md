# Changelog

## v3.7.16 — 2026-05-18

Mega release. Three new content surfaces (`skills/higgsfield-gpt-image-2/SKILL.md` translating Adil Aliyev's `gpt-image-2-director.md` source corpus; `skills/higgsfield-gpt-image-2/static-ads-workflow.md` satellite translating Adil's `static-ads.md`; `skills/higgsfield-marketing-studio/cross-surface-workflow.md` §3 restructure with ms_image / "DTC Ads" coverage expanded within source-evidence boundary), three infrastructure changes (DejaVu Sans Mono code-block font swap + `--dry-run` 7-class exit-code matrix + `validate.py` Phase 4 subprocess integration), one PDF FAQ paragraph refresh (v3.7.13–v3.7.16 era summary), and three cross-reference cite additions in templates + seedance sub-skill. Substrate carries from v3.7.14/15 (DVC font + `--dry-run` + `.planning/<version>/` convention + per-claim register-downgrade discipline).

Original kickoff scope was 9 items targeting 3 new sub-skills (gpt-image-2 + static-ads + ms_image as separate sub-skills). Phase 0 evidence rescoped to architectural option β — items 1 (gpt-image-2-director translation) and 3 (static-ads translation) consolidated under a single `higgsfield-gpt-image-2/` sub-skill with `static-ads-workflow.md` as a satellite (mirroring the proven `higgsfield-marketing-studio/` + `cross-surface-workflow.md` pattern from v3.7.13). Item 2 (ms_image as full sub-skill) rescoped to a `cross-surface-workflow.md` §3 expansion because Phase 0 § VERIFY 0.3 surfaced **zero hits** across both Adil source SKILL.md files for `ms_image | dtc ads | dtc_ads | marketing_studio_image` — building a full sub-skill would have required either methodology shift to live-MCP probing or pure documentation authoring beyond the project's established Adil-corpus-as-source translation pattern. Net: 1 new sub-skill (with satellite) instead of 3.

### Architectural decision: Option β LOCKED

Phase 0 § VERIFY 0.3 surfaced the architectural choice between α (three separate sub-skills), β (consolidated `higgsfield-gpt-image-2/` with satellite + ms_image as §3 expansion), and γ (gpt-image-2 standalone + everything else into existing `higgsfield-marketing-studio/`). Phase 1 § 1A locked β based on three considerations:

1. Items 1 (gpt-image-2-director) and 3 (static-ads.md) cover **the same model** (GPT Image 2.0) at different routing taxonomies — prompt-craft vs. ad-recreation-workflow. Consolidating under one sub-skill with the workflow as satellite matches Adil's own source structure (he has two skills covering the same model).
2. The marketing-studio + cross-surface-workflow.md pattern established in v3.7.13 is **proven precedent** for the parent SKILL.md + satellite shape. Replicating it for gpt-image-2 maintains house-style consistency.
3. ms_image's source-corpus gap (zero hits in Adil corpus) **forces** the §3-expansion vs. new-sub-skill choice. β honors the source-evidence boundary by keeping ms_image at expansion-of-existing-doc shape, not at new-doc-built-from-thin-air shape.

### Source-evidence discipline applied to ms_image §3 expansion

Phase 1 § 1C established an explicit **DO-NOT-WRITE list** for the §3.b expansion, enforced at Phase 2E composition:

- No worked examples of ms_image generations (no source corpus, no demo evidence)
- No sample `brand_kit_id` or `style_id` UUIDs (no observed instances; placeholder UUIDs would mislead)
- No pricing claims for `ms_image` specifically (no separate pricing signal in Phase 0 evidence — surfaced explicitly in §3.b.ii)
- No capability claims beyond the parameter schema (the four ms_image differentiators derive 1:1 from the four distinguishing parameters: `brand_kit_id`, `style_id`, `batch_size`, `medias.max=14`)
- No specific ad-format style names (`style_id` is required but enumeration is platform-managed — surfaced via § 3.b.iv live-enumeration discipline callout reusing v3.7.13 hooks/settings pattern)

This is the v3.7.13 recursive-plausibility-over-verification discipline applied to a NEW failure-mode class: not "source got the API wrong" (v3.7.13's 12 reconciliations) but "no source at all — temptation to invent." Phase 1 § 1C-c codified the DO-NOT-WRITE list; Phase 2E STOP report audit confirmed all 5 items honored.

### Added

- **NEW `skills/higgsfield-gpt-image-2/SKILL.md`** (266 lines, 11 sections per Phase 1 § 1A locked structure). Translates Adil's `gpt-image-2-director.md` source corpus (~14 KB, 206 lines) per v3.7.13/15 translation precedent. Three-format prompt taxonomy: Format A structured JSON (UI mockups, layout-dense images) / Format B dense cinematic prose (single-subject scenes) / Format C auto-derive meta-prompt (theme-only concepts). Section coverage: §1 What GPT Image 2.0 is (capability framing applying v3.7.15 Spatial Zoning testability exception to prompt-following + text-rendering claims — Phase 1 Revision 1) · §2 Three prompt formats · §3 Format A · §4 Format B (CJK worked example preserved verbatim per Phase 1 D13) · §5 Format C · §6 Routing decision · §7 Output format conventions · §8 Pre-delivery checklist (cross-ref to DISCIPLINE.md § Pre-Delivery Discipline) · §9 Example routings (6 paired examples) · §10 Cross-surface workflow context · §11 Source acknowledgment.

- **NEW `skills/higgsfield-gpt-image-2/static-ads-workflow.md` satellite** (310 lines, 7 sections per Phase 1 § 1A locked structure). Translates Adil's `static-ads.md` source corpus (~20 KB, 316 lines). Production-knowledge workflow doc with the highest-falsifiable content from the source corpus: §3 fractional-coordinate zone notation (`text_zone`, `product_zone`, `button_zone`, `disclaimer_zone`) + brand-neutral wireframe intermediation + safe-zone top/bottom-10% rule (the only HARD-RULE volume claim in static-ads.md, adopted close to verbatim because the underlying premise — Instagram and TikTok UI overlays consume top/bottom ~10% of frame — is verifiable surface fact about platform UI behavior, not craft opinion; Phase 1 Revision 2 framing); §4 brand-vs-structure separation (two-list rule + Mode A reference swap / Mode B text-driven layout); §5 three worked template patterns (iMessage / DM Conversation, Scarcity / Countdown Urgency, Ingredient Spotlight / Clean Label) preserved verbatim with bracketed placeholders.

- **NEW `assets/fonts/DejaVuSansMono.ttf`** (333 KB, regular weight only). Bundle-symmetry inheritance from the v3.7.14 DVC swap — but for code blocks. `code_block` method at `generate_user_guide.py:210` swaps from `set_font("Courier", "", 9)` to `set_font("Mono", "", 9)`. Phase 0 § VERIFY 0.4 measured 0.33% max glyph-width drift on real code-block samples (well under the 5% threshold inherited from v3.7.14). Bundled with new `Mono` font alias alongside existing `Body` alias for DVC family — single `add_font("Mono", ...)` line at `generate_user_guide.py:155`. Updated `assets/fonts/README.md` with DVSM rationale section + four-TTF table.

- **NEW `.planning/v3.7.16/`** verification + inventory + execution artifacts following the v3.7.13/14/15-established convention. `PHASE-0-VERIFICATION.md` (7-VERIFY report at 836 lines: source-corpus reads for gpt-image-2-director + static-ads, ms_image source-evidence boundary survey, DVSM drift measurement, exit-code matrix design, validate.py subprocess integration design, content cleanup scope verification, architectural option α/β/γ enumeration). `PHASE-1-INVENTORY.md` (file-by-file inventory + § 1B-A / § 1B-B per-element translation rule tables + § 1C source-evidence boundary + § 1D infrastructure design specifics + § 1E cross-reference 3-site disposition + § 1F 13-sub-phase Phase 2 ordering with 8 STOPs + § 1G 28-row decisions register).

- **NEW exit-code matrix in `generate_user_guide.py`** — 7 enumerated exit codes (0 OK, 1 unknown catch-all, 2 frontmatter, 3 dict-parity, 4 font, 5 render, 6 output) backed by 5 named exception classes (`FrontmatterError`, `DictParityError`, `FontError`, `RenderError`, `OutputWriteError`) extending `BuildError(RuntimeError)`. argparse harness in `__main__` routes each exception class to its exit code with a stderr message labeled by failure class. Per Phase 1 § 1D-2 design D5-A; symmetric raise-site semantics enforced at Phase 2A Refinement 4 (every named class fires from at least one explicit `raise` site, including the body-wrap `try/except FPDFException → RenderError` re-raise inside `build_pdf`).

- **NEW `[ PDF DRY-RUN SMOKE ]` Phase 4 in `validate.py`** — subprocess invocation of `python3 generate_user_guide.py --dry-run` as an unconditional pre-release gate. Binary returncode mapping (0 = PASS, non-zero = FAIL) with stderr first-line excerpt surfaced for diagnostic context. `subprocess.TimeoutExpired` handler routes timeout to a standard `check(False, ...)` failure with 60-second ceiling. Per Phase 1 § 1D-3 design 6-A + 6-i; Phase 2B controlled failure verification confirmed end-to-end roundtrip (font removed → FontError → exit 4 → validate.py captures + reports → exit 1).

- **NEW v3.7.13–v3.7.16 era clause in PDF FAQ § 25** — Section 25 "What changed since v3.0.0?" answer extended with the cross-surface mega-arc summary (higgsfield-marketing-studio sub-skill, USER-GUIDE rendering pipeline hardening, cinematic-motion-language 5-pillar translation, higgsfield-gpt-image-2 sub-skill). Count corrected from inaccurate "Seventeen" to accurate "Thirty" (v3.0.0 → v3.7.16 inclusive). The "Seventeen" was stale predating v3.7.13; v3.7.16 corrects 4+ releases of count drift plus the original inaccuracy.

### Changed

- **`generate_user_guide.py`** — major structural change. Top-of-file gains 5 named exception classes + 7 exit-code constants + module docstring exit-code summary section (~+51 LoC). `UserGuidePDF.__init__` wraps the four `add_font` calls in try/except → `FontError` and adds the new `Mono` alias registration. `code_block` swaps Courier → Mono (single token). `read_root_metadata` converts two `raise RuntimeError` to `raise FrontmatterError`. `build_pdf` body wrapped in `try/except FPDFException → raise RenderError` (Phase 2A Refinement 4 — 1048 body lines re-indented +4 spaces under the wrap). Dict-parity check converts `raise RuntimeError` to `raise DictParityError`. `pdf.output(...)` wrapped in `try/except → OutputWriteError`. `__main__` block replaces the bare `build_pdf(...)` call with a full argparse + exception-class-routing harness mapping each failure class to its exit code. `SUB_SKILL_DESCRIPTIONS` dict gains `"higgsfield-gpt-image-2": "GPT Image 2.0 prompt director + static-ads workflow satellite"` entry (61 chars, 10 chars under the 71-char ceiling) inserted alphabetically between `higgsfield-cinema` and `higgsfield-marketing-studio`. Section 25 FAQ paragraph at L1290 refreshed per above. Net delta: ~+150 LoC across infrastructure + content edits.
- **`validate.py`** — gains Phase 4 PDF dry-run smoke check at L144 (+24 LoC) per above.
- **`validate_user_guide.py`** — `DEFAULT_BASELINE` retarget: `USER-GUIDE.pdf.baseline-v3.7.15` → `USER-GUIDE.pdf.baseline-v3.7.16` (one-token edit at L98).
- **`skills/higgsfield-marketing-studio/cross-surface-workflow.md`** — §3 restructured into §3 opening / §3.a Path A (Adil's actual recipe with pointer to new `higgsfield-gpt-image-2/` sub-skill and satellite) / §3.b Path B (`ms_image` / "DTC Ads") with five sub-sections: §3.b.i Capability summary · §3.b.ii Parameter schema (verbatim from Phase 0 Probe 0.3-a) · §3.b.iii When to recommend ms_image over GPT Image 2.0 (POLISH 2 framing — Adil's non-use treated as informational, not directive) · §3.b.iv Naming reminder + live-enumeration discipline callout (reuses v3.7.13 hooks/settings pattern for brand_kit_id + style_id) · §3.b.v Source-corpus reconciliation #12 (zero-hit grep + verification trail). §8 surface coverage map header refreshed to "(as of v3.7.16)"; three rows updated (GPT Image 2.0 shipped, ms_image expanded §3.b, Static-image cross-surface shipped via satellite). Net delta: +60 lines.
- **`templates/seedance/multi-character-anchor.md` L80** — GREAT exposition prose gains parenthetical cross-reference: `(distance + eyeline + crossing rule + negative space — see vocab.md § Composition Vocabulary → Crossing rule + § Negative space)`. +2 lines.
- **`templates/seedance/worked-example-two-character.md` L68** — "What this demonstrates" prose gains companion vocab.md citation alongside existing `§ Spatial Layout Block` reference. +2 lines.
- **`skills/higgsfield-seedance/SKILL.md` L488** — "Not a mathematical guarantee" subsection's inline vocabulary list gains parenthetical citation: `(`crossing rule` — the last formalized at vocab.md § Composition Vocabulary → Crossing rule)`. +1 line.
- **Root `SKILL.md`** — frontmatter version `3.7.15` → `3.7.16`; `updated:` `2026-05-18` (same-day cascade per v3.7.10/11/12/13/14/15 pattern).
- **`README.md`** — version badge (L1) + footer (L262) `3.7.15` → `3.7.16`.
- **`assets/fonts/README.md`** — updated title to include DVSM; new "Why DejaVu Sans Mono (v3.7.16)" rationale section + four-TTF table + corrected "three styles" sentence to handle Body (3 styles) + Mono (1 style regular) split.

### Verification

- `python3 validate.py` — ALL CHECKS PASSED. 24 SKILL.md files discovered (1 root + 23 sub-skills, up from 22). All frontmatter required fields present including the two new files (`skills/higgsfield-gpt-image-2/SKILL.md` + `skills/higgsfield-gpt-image-2/static-ads-workflow.md`). All cross-skill references resolve including the new `../higgsfield-gpt-image-2/SKILL.md` ref from cross-surface-workflow.md §3.a + §3.b.iii + §8 and the three new `../../vocab.md` refs at the cross-reference cite sites. New `[ PDF DRY-RUN SMOKE ]` Phase 4 reports exit 0; controlled failure verification (DVSM font removed) confirmed end-to-end roundtrip (FontError → exit 4 → validate.py captures + reports → exit 1) at Phase 2B STOP.
- `python3 generate_user_guide.py --dry-run` — exit 0 confirmed after Phase 2H resolves dict-parity. Pre-2H dry-runs exit 3 (DICT-PARITY ERROR) as designed — the dry-run gate caught the new sub-skill directory before its `SUB_SKILL_DESCRIPTIONS` entry landed. Phase 2A controlled failure tests (Phase 2A smoke + Phase 2B controlled-failure verification) confirmed the 7-class exit-code matrix routes each failure-class correctly to its labeled stderr + exit code.
- Phase 0 § VERIFY 0.4 measurement script (`/tmp/dvsm_drift.py`) confirmed DVSM glyph-width drift = 0.33% on real code-block samples (12 samples including CLI commands, MCP calls, paths, dict-key shapes, synthetic 71×'x' worst case). Page count post-DVSM swap at Phase 2A baseline = 28 (unchanged from v3.7.15); content-driven drift to 30 pages surfaced at Phase 2H after the new SUB_SKILL_DESCRIPTIONS row + Option B FAQ era summary expansion. Descope-trigger attribution test passed: 2-page drift fully explained by content additions, zero attributable to DVSM.
- Per-section verification tables produced at Phase 2C STOP (§ 1B-A 32-row table for gpt-image-2 SKILL.md composition), Phase 2D STOP (§ 1B-B 21-row table for static-ads-workflow.md), Phase 2E STOP (§ 1C 8-row structure table + 5-row DO-NOT-WRITE compliance audit for ms_image §3.b expansion). All rows verified ✓ at composition time; zero discipline-label drift; zero fabrication beyond source-evidence.

### Scope acknowledgment

Mega scope per Phase 0 evidence rescope:

- **Item 2 RESCOPED** — ms_image / "DTC Ads" full sub-skill → `cross-surface-workflow.md` §3 expansion (~60 net lines vs. ~400 lines for a full sub-skill). Phase 0 § VERIFY 0.3 zero-hit-grep evidence overrode kickoff scope ambition.
- **Items 12 + 13 DESCOPED to v3.7.17+ backlog:**
  - Item 12 PARTIAL — ship 3 of 9 cross-reference sub-sites (`multi-character-anchor.md` L80, `worked-example-two-character.md` L68, `higgsfield-seedance/SKILL.md` L488). Defer 6: 12.1 (table-cell at `templates/10-dance-music-performance.md` L32, awkward cite shape), 12.2/12.3 (fenced-code-block locations inside `multi-character-anchor.md` template scaffolding), 12.5 (fenced-code-block inside worked-example prompt body), 12.8 (`higgsfield-camera/SKILL.md` Camera Contract authoring — prose rework, not citation), 12.9 (`higgsfield-prompt/SKILL.md` MCSLA Action layer authoring — prose rework, not citation). Earns its own scope as a future "sub-skill cross-reference review" arc.
  - Item 13 FULL — DISCIPLINE.md boundary-condition framing pattern naming. v3.7.15 set the criterion ("if the same shape surfaces elsewhere"); only one observation to date. Re-eligible if a second observation surfaces in future translation work.
- **Phase 1 Revision 7 inventory correction** — PHASE-1-INVENTORY.md § 1E-2 drafted prose had a single-character path typo (`../../../vocab.md`, 3 levels up — out-of-project-root from `templates/seedance/`). Phase 2F apply-verbatim discipline caught + corrected to `../../vocab.md` (2 levels up); Phase 2G applied Refinement 7 to update the inventory document so the locked record matches what shipped.
- **Original kickoff 9-item scope → 7.5-item effective scope** — three content surfaces (β consolidation = 1 sub-skill + 1 satellite + 1 §3 expansion), three infrastructure changes, one FAQ refresh, partial cross-reference cleanup (3 of 9), descoped DISCIPLINE.md naming. Proportionate to Phase 0 evidence; the mega-release earns its scope at 7.5 items, not 9.

### Source corpus + attribution

Adil Aliyev source corpus translated:

- `gpt-image-2-director` source skill (~14 KB, 206 lines) → `skills/higgsfield-gpt-image-2/SKILL.md` per § 1B-A locked translation rules
- `static-ads.md` source corpus (~20 KB, 316 lines) → `skills/higgsfield-gpt-image-2/static-ads-workflow.md` satellite per § 1B-B locked translation rules

Adil's source corpus sibling to v3.7.13's `marketing-studio-director.md` + `higgsfield-content-factory.md` (translated v3.7.13) and v3.7.15's `cinematic-motion-language.md` (translated v3.7.15). Three releases, three source files, one author. The v3.7.13 author-signature calibration ("strong craft, weak provenance") holds across the corpus; per-claim register-downgrade applied per § 1B-A / § 1B-B tables. ms_image surface has **zero hits** across both v3.7.13-translated source SKILL.md files (`marketing-studio-director/SKILL.md` 262 lines + `higgsfield-content-factory/SKILL.md` 997 lines) — source-corpus reconciliation #12 preserved verbatim in `cross-surface-workflow.md` §3.b.v.

Attribution lands per Phase 1 D14 convention:

- This CHANGELOG entry (corpus citation + architectural rationale)
- `skills/higgsfield-gpt-image-2/SKILL.md` §11 + `static-ads-workflow.md` §7 (per-sub-skill source acknowledgment with per-claim translation calibration + verification trail to PHASE-0/PHASE-1 artifacts)
- `cross-surface-workflow.md` §3.b.v (ms_image zero-hit reconciliation with verification trail)

### Backlog — updated

- G1 Soul Cinema two-step compositing — UI testing remains pending (carried from v3.7.5)
- G13 Seedance `【镜头N】` syntax — Seedance product-team confirmation pending (carried from v3.7.5)
- **NEW: 6 of 9 cross-reference sub-sites deferred** (per Item 12 partial descope above) — earns its own scope as future "sub-skill cross-reference review" arc
- **NEW: DISCIPLINE.md boundary-condition framing pattern naming** (per Item 13 descope) — re-eligible if a second observation surfaces in future translation work
- **NEW: validate.py `check_relative_paths` regex tightening** — current regex matches backtick-quoted display text in markdown links, producing false-positives that 2C composition caught + worked around. Tightening to distinguish backtick-code-formatting from actual link references would eliminate the false-positive class.
- **NEW: cross-surface-workflow.md §8 surface coverage map maintenance** — current state refreshed at v3.7.16 Refinement 6; future content sub-skill additions should update §8 in the same release that creates them.
- **NEW: FAQ paragraph release-count maintenance discipline** — original "Seventeen" was inaccurate predating v3.7.13; v3.7.16 corrects to "Thirty". Structural fix candidate: either automate the count from CHANGELOG.md or convert to relative phrasing that doesn't require updating per release.
- **NEW: Phase 1 § 1A page-count projection methodology** — v3.7.16's actual 30-page count exceeded the § 1A-projected ~29 by +1 because the projection only modeled the dict-row addition, not the FAQ era summary expansion. Future Phase 1 work would benefit from per-content-addition page-count estimate columns rather than aggregate projection.
- **NEW: Soul Cinema (for items specifically) sibling-director sub-skill** — remains deferred (carried from v3.7.13)
- **NEW: Nano Banana Pro sibling-director sub-skill** — remains deferred indefinitely (carried from v3.7.13)

## v3.7.15 — 2026-05-18

Content-translation patch release closing the cinematic-motion-language.md → vocab.md gap-fill arc carried since v3.7.13. Adds 4 new `###` subsections to vocab.md (Camera Contract, Motion Physics Anchor, Lens Behavior Sequence, Spatial Zoning) and 1 new cross-cutting `###` subsection (Negative-prompt reinforcement, extracted because 3 of 5 pillars share the technique). Expands the existing Negative space entry from a single bullet (L338 in v3.7.14) to a multi-paragraph `### Negative space` subsection covering the negative-prompt reinforcement pattern + Spatial Zoning binding + a teaching frame on evocative naming. Restructures § Composition Vocabulary from flat bullets to `###` subsections for house-style alignment with Camera Movement / Visual Style / Lighting. Translates Adil Aliyev's 5-pillar cinematic-motion-language framework to our skill's voice and register per the TRANSLATE-WITH-VERIFICATION disposition established in v3.7.13. No infrastructure changes; substrate carries from v3.7.14 (DVC font + `--dry-run` smoke gate + `.planning/<version>/` artifact convention).

### Per-claim register downgrade — the principled boundary applied per pillar

Phase 0 verification (`.planning/v3.7.15/PHASE-0-VERIFICATION.md`) surfaced the author-signature calibration carried from v3.7.13: **pillar names + grouping = Adil's craft synthesis** (translated freely to our voice); **pillar vocabulary = standard cinematography** (adopted close to verbatim); **universalizing claims about model behavior = craft opinion at HARD RULE volume** (downgraded to "useful pattern" / "common technique" framing).

The locked §1G translation table operationalized this as a per-element ADOPT/DOWNGRADE classification across 5 pillars and 24 individual elements. The principled boundary between adopt-and-downgrade is **per-claim testability**:

- Camera Contract source L26 — *"The model treats the camera as a character — define it or it will improvise."* Metaphysical, untestable claim about model cognition → **DOWNGRADED** to *"When camera behavior is left implicit, the model defaults to its training-prior interpretation, which may not match the intended shot."*
- Spatial Zoning source L59 — *"This prevents the model from filling empty space with invented content."* Falsifiable, directionally correct → **ADOPTED** with explicit framing as *"a falsifiable production claim, well-aligned with how transformer-based video models respond to explicit constraints."*
- Motion Physics Anchor source L53 — *"Never use 'slow', 'fast', 'gentle', 'subtle' alone."* Universalizing HARD-RULE prohibition → **DOWNGRADED** to *"When motion-speed precision matters, anchor to physics analogies or time measurements rather than adjectives. Adjectives like `slow` or `fast` work as quick-spec for casual prompts but are less reliably interpreted than physical analogies or time anchors."*
- Lens Behavior Sequence source L79-80 — *"…but only when the sequence is described explicitly as cause and effect."* Universalizing "only when" → **DOWNGRADED** to *"Models tend to produce cleaner / more reliable focus events when the sequence is described as cause and effect…"*

The boundary is the discipline. Falsifiable directional claims about prompt-side effects keep; metaphysical universalizing claims about model cognition downgrade. DISCIPLINE.md § Anti-Bombast gains a one-sentence citation pointing at `vocab.md` § Motion Physics Anchor as the canonical example of the discipline applied to source material with HARD-RULE-volume craft opinion.

### Movement Quality conflict — narrower than Phase 0 framed it

Phase 0 surfaced Adil's Motion Physics Anchor as appearing to contradict our existing § Subject & Character → Movement Quality (vocab.md L264 in v3.7.15; was L205 in v3.7.14). Phase 1 §1C re-evaluation found the conflict was illusory: Movement Quality vocabulary (fluid / jerky / hesitant / confident / stumbling) describes the **character** of motion (performance direction); Motion Physics Anchor describes the **speed** of motion (rate specification). Orthogonal vocabularies. Adil's HARD-RULE prohibition on "slow"/"fast"/"gentle"/"subtle" applies to speed-descriptor adjectives, not to motion-character adjectives — the two lists do not overlap. Movement Quality at L264 ships **unchanged**. Motion Physics Anchor opens with explicit orthogonality framing: *"a character can move with `stumbling` quality (Movement Quality) at `the pace of a clock's hour hand` (Motion Physics Anchor). Different axes of motion description."*

### Source attribution

Adil Aliyev's `cinematic-motion-language.md` (~8 KB at `~/Desktop/EVEN MORE SKILLS/MORE CUSTOM SKILLS/`; sibling to `marketing-studio-director.md` and `higgsfield-content-factory.md` translated in v3.7.13). 5-pillar system: Camera Contract / Motion Physics Anchor / Spatial Zoning / Lens Behavior Sequence / Negative Space as Compositional Tool. Per-pillar attribution lives inside each new `vocab.md` subsection (closing blockquote callout: *"Translated from Adil Aliyev's `cinematic-motion-language.md` source corpus"*); per-claim translation rationale lives in `.planning/v3.7.15/PHASE-1-INVENTORY.md` §1G.

### Added

- **`vocab.md` § Camera Movement Terminology → 3 new `###` subsections** (`### Camera Contract`, `### Motion Physics Anchor`, `### Lens Behavior Sequence`). Inserted after § Motion Hierarchy at the tail of the Camera Movement Terminology section per the Option-A distributed-insertion architectural choice locked at Phase 1 §1B D5. Camera Contract = 14 lines / 186 words. Motion Physics Anchor = 26 lines / 305 words (includes orthogonality framing vs. § Movement Quality and 6 physical-analogy speed references + 4 time-anchored measurement examples). Lens Behavior Sequence = 20 lines / 259 words (includes trigger → shift → state → return → repeat structure + worked focus-event example + 6-term vocabulary list with cross-links to existing § Rack Focus + § Anamorphic entries).
- **`vocab.md` § Composition Vocabulary → 2 new `###` subsections** (`### Negative-prompt reinforcement`, `### Spatial Zoning`). Negative-prompt reinforcement = 15 lines / 146 words, placed first because the technique is cross-cutting (3 of 5 pillars share it per source-text grep verified in Phase 1 §1F). Spatial Zoning = 22 lines / 190 words (includes region-naming conventions + zone-rule examples + ADOPT-not-DOWNGRADE framing for the falsifiable "prevents model from filling empty space" claim per the testability-boundary discipline above).
- **`DISCIPLINE.md` § Anti-Bombast `**Demonstrated in:**` block** extended with one citation sentence (D14 PULL-IN per Phase 1 §1A) wrapped to 7 visual lines following DISCIPLINE.md's ~62-char line convention. Names cinematic-motion-language.md as the canonical example of source material with HARD-RULE-volume craft opinion and points at `vocab.md` § Motion Physics Anchor as the canonical example of per-claim register downgrade.
- **NEW `.planning/v3.7.15/`** verification + inventory artifacts following the v3.7.13/v3.7.14-established convention. `PHASE-0-VERIFICATION.md` (5-VERIFY report: gap-check + lexical-variant grep + architectural insertion options + per-pillar register classification + probe-scope decision) and `PHASE-1-INVENTORY.md` (file-by-file inventory + per-pillar §1G translation-rule ADOPT/DOWNGRADE table + 7-sub-phase ordering with STOPs + 17-row decisions register).

### Changed

- **`vocab.md` § Composition Vocabulary restructure** — converted from flat bullets to `###` subsections for house-style alignment with Camera Movement / Visual Style / Lighting / Subject & Character (all use `###` subsections internally). The existing 3 entries (Negative space, Crossing rule, Coordinate notation) become `### Negative space`, `### Crossing rule`, `### Coordinate notation` subsections. Crossing rule and Coordinate notation prose **unchanged** — markup-only conversion.
- **`vocab.md` § Composition Vocabulary → `### Negative space`** expansion (D4 partial-coverage-with-additive-content disposition). Existing v3.7.14 L338 prose preserved **verbatim** as the opening paragraph of the new subsection. Three additive paragraphs: (1) negative-prompt reinforcement cross-reference to the new sibling section, (2) binding to § Spatial Zoning naming negative space as one named zone type within a Spatial Zoning system ("the two compose"), (3) teaching frame on evocative naming with the boundary-condition formulation: *"Production-direction register tolerates evocative naming when the evocation is grounded in a compositional rule…Without the underlying rule, evocative naming reads as adjective-stacking; the rule is what makes the evocation operative."* Net 10 lines / 194 words; +9 lines / +129 words over the v3.7.14 single-bullet entry. Evocative naming examples (`sacred emptiness`, `active darkness, not background`, `deliberate compositional weight`) source-attributed inline to Adil's `cinematic-motion-language.md`.
- **`skills/higgsfield-marketing-studio/cross-surface-workflow.md` L417** — "Deferred — `cinematic-motion-language.md` translation to `vocab.md` is a follow-up release" callout closed with shipping language: *"Shipped in v3.7.15 — translated to `vocab.md` § Camera Movement Terminology (Camera Contract, Motion Physics Anchor, Lens Behavior Sequence) + § Composition Vocabulary (Negative-prompt reinforcement, Spatial Zoning, Negative space expansion)…"* One-line edit, +1 / -1 net delta.
- **Root `SKILL.md`** — frontmatter `version: 3.7.14` → `3.7.15`; `updated: 2026-05-18` (same-day cascade per the v3.7.10/11/12/13/14 pattern).
- **`README.md`** — version badge (L1) and footer (L262) cascade `3.7.14` → `3.7.15`.
- **`docs/user-guide/USER-GUIDE.pdf`** — regenerated with v3.7.15 metadata cascade. vocab.md content does NOT surface in the PDF (only the filename appears in Section 24 Root Files at `generate_user_guide.py` L1186); the regeneration is metadata-cascade-only (version + updated date at PDF header L109, page-1 footer L240, last-page footer L1258 via `META['version']`/`META['updated']`). Page count expected unchanged from v3.7.14 baseline (28 pages).
- **`docs/user-guide/USER-GUIDE.pdf.baseline-v3.7.15`** — NEW baseline file, byte-for-byte copy of the regenerated PDF; new validator target replacing v3.7.14 baseline.
- **`validate_user_guide.py`** — `DEFAULT_BASELINE` retargeted from `USER-GUIDE.pdf.baseline-v3.7.14` to `USER-GUIDE.pdf.baseline-v3.7.15`. One-line edit at L98.

### Verification

- `python3 validate.py` — ALL CHECKS PASSED. 23 SKILL.md files discovered. All cross-skill references resolve including the new `.planning/v3.7.15/` artifact references. All JSON databases pass schema. All 13 declared root files present.
- `python3 generate_user_guide.py --dry-run` — exit 0. The em-dash/Unicode class of bugs gated by the v3.7.14 `--dry-run` flag continues to surface here before ship time.
- `python3 generate_user_guide.py` — exit clean. Generated `docs/user-guide/USER-GUIDE.pdf` (28 pages, ≈90 KB). Page count unchanged from v3.7.14 baseline; no layout reflow.
- `python3 validate_user_guide.py` against new v3.7.15 baseline — VALIDATION PASSED. Layer 0 (`SUB_SKILL_DESCRIPTIONS` ceiling check) PASS: 22 entries ≤ 71 chars. Layer 1 (text-extract diff) PASS. Layer 2 (binary diff) PASS: byte-for-byte identical (candidate = baseline copy).
- `git diff --stat` content summary: `vocab.md` +109 / -4 net; `DISCIPLINE.md` +6 / 0 net; `skills/higgsfield-marketing-studio/cross-surface-workflow.md` +1 / -1 net; `SKILL.md` +1 / -1; `README.md` +2 / -2; `validate_user_guide.py` +1 / -1; `docs/user-guide/USER-GUIDE.pdf` regenerated (binary); new file `docs/user-guide/USER-GUIDE.pdf.baseline-v3.7.15` (binary); new files `.planning/v3.7.15/PHASE-0-VERIFICATION.md` + `PHASE-1-INVENTORY.md`.

### Cross-reference verification

Phase 2B `§`-prefixed cross-reference grep confirmed **ZERO blast radius** under Option A distributed-insertion architectural choice. All existing cross-references from sub-skills (`higgsfield-prompt`, `higgsfield-seedance`, `higgsfield-pipeline`, `higgsfield-cinema`, `higgsfield-stack`), DISCIPLINE.md, root SKILL.md, and `templates/seedance/multi-character-anchor.md` to vocab.md target sections that remain unchanged (`§ Emotion as Visible Behavior`, `§ World Through Recurrence`, `§ Editing Syntax`, `§ Scene-physics lighting`, `§ Aspect Ratio`). Six inline-mention enhancement opportunities surfaced for future release (templates referencing "negative space" / "crossing rule" inline could be enhanced with `§` cross-references; sub-skills referencing camera-discipline / MCSLA Action layer / Spatial Layout Block could cite the new pillar subsections). Flag-only; no v3.7.15 scope.

### Scope acknowledgment

Content-translation patch release. The descope path preserved in Phase 0 (probe budget allocation) was not triggered: content-translation evidence retired probe budget legitimately, mirroring v3.7.13's schema-level-evidence-retired-spend-probes pattern. The architectural insertion question (Phase 0 Options A/B/C) re-evaluated at Phase 1 §1B against actual `vocab.md` structure — Option A locked over the user's preliminary Option C lean because vocab.md has no precedent for system-level index sections (Cut & Continuity, Motion Hierarchy, 8-channel Emotion, 8-axis World Through Recurrence all live as `###` subsections without dedicated indices); importing one for Adil's 5-pillar framework would have treated his grouping as more architecturally privileged than our own existing frameworks. System-coherence preserved instead via per-pillar single-sentence callouts inside each new subsection (~5 callouts × ~2.4 visual lines = ~12 lines total).

Out of v3.7.15 scope (deferred to future arcs):

- `gpt-image-2-director` sub-skill — carried from v3.7.13/14 backlog
- `ms_image` ("DTC Ads") full sub-skill — carried from v3.7.13/14 backlog
- `static-ads.md` translation — carried from v3.7.13/14 backlog
- Soul Cinema / Nano Banana Pro sibling director skills — carried (deferred indefinitely)
- `validate.py` subprocess integration of `--dry-run` — carried from v3.7.14
- Courier → DejaVu Sans Mono swap — carried from v3.7.14
- Adil's integrated Prompt Template (source L114-149) — cited as pedagogical artifact, not imported per Phase 1 D8. MCSLA remains the single primary prompt structure
- Adil's Dervish Shot worked example (source L186-209) — cited as pedagogical artifact, not imported per Phase 1 D9. Per-pillar integrated examples in each new vocab.md subsection serve the same purpose at smaller scale
- FAQ paragraph at `generate_user_guide.py` L1236 ("Seventeen platform releases shipped between v3.0.0 (April 2026) and this guide (v3.7.12)") — stale across v3.7.13/14/15 but explicitly deferred per established practice (historically-versioned content); not touched
- Forward-looking content authoring: sub-skills could cite the new pillar subsections (camera-discipline → Camera Contract; MCSLA Action → Motion Physics Anchor; Spatial Layout Block → Spatial Zoning; product photography → Lens Behavior Sequence). Flagged in Phase 2B; not v3.7.15 scope
- Generalizable boundary-condition framing pattern ("grounded → operative; ungrounded → adjective-stacking") observed in Negative space evocative-naming treatment — may earn its own DISCIPLINE.md pattern name in a future arc if the same shape surfaces elsewhere

### Backlog — updated

- **CLOSED: `cinematic-motion-language.md` vocab.md gap-fill** (carried from v3.7.13/14) — 4 new vocab.md subsections + 1 new cross-cutting subsection + 1 in-place expansion + § Composition Vocabulary house-style restructure ship in v3.7.15 per the TRANSLATE-WITH-VERIFICATION disposition. The amended Phase 0 finding ("4 full pillar gaps + 1 partial-coverage-with-additive-content for Negative Space") replaces v3.7.13/14's CHANGELOG framing of "4 of 5 pillars need translation; Negative Space already covered" — Negative Space partial coverage at v3.7.14 L338 was real but missed Adil's negative-prompt-reinforcement pattern + zone-binding to Spatial Zoning, both shipped as additive content in v3.7.15.
- All other v3.7.14 backlog items unchanged — carry-forward to future releases. G1 Soul Cinema two-step compositing UI testing pending; G13 Seedance `【镜头N】` syntax product-team confirmation pending.
- **NEW: Boundary-condition framing pattern** — the "grounded → operative; ungrounded → adjective-stacking" framing applied to Negative space evocative-naming treatment is a more sophisticated application of the per-claim register-downgrade discipline. May earn its own DISCIPLINE.md pattern name in a future arc if the same shape surfaces elsewhere. Observed but not pattern-named in v3.7.15.

## v3.7.14 — 2026-05-18

Infrastructure-hardening patch release. Option B scope per `.planning/v3.7.14/PHASE-0-VERIFICATION.md` and locked Phase 1 inventory: three coupled items plus natural fallout. (1) `--dry-run` flag on `generate_user_guide.py` that runs the dict-parity check and full `build_pdf()` rendering pipeline in-memory without writing the output file. (2) FPDF Unicode font swap from helvetica (latin-1 core) to DejaVu Sans Condensed (DVC, bundled in `assets/fonts/`). (3) Section 24 sub-skill row for `higgsfield-marketing-studio` — deferred from v3.7.13 per its Phase 1 scope, surfaces in v3.7.14's regeneration via the existing auto-generated table. Natural fallout: USER-GUIDE.pdf regenerated under DVC + new `docs/user-guide/USER-GUIDE.pdf.baseline-v3.7.14` replacing v3.7.12 as `validate_user_guide.py`'s diff target. Phase 0 verification surfaced one substitution — DejaVu Sans **regular** measured 11–18% glyph-width drift versus helvetica and would overflow one existing `SUB_SKILL_DESCRIPTIONS` entry (`higgsfield-cinema` at the 71-char column ceiling); DejaVu Sans **Condensed** holds drift at 0.6–2.8% on real text with zero overflows. The substitution is Phase 0's evidence overriding the original assumption, not scope change — same family, same Unicode coverage, same goal.

### Closing the verification gap

Two prior releases ran latent rendering bugs into PDF generation that `validate.py` had no way to catch:

- **v3.7.12** — frontmatter parser raised `RuntimeError` at PDF render time when a required field was missing, AFTER `validate.py` passed clean. `validate.py` was checking structural integrity of inputs; the renderer was the only thing exercising the cross-input contract.
- **v3.7.13** — `SUB_SKILL_DESCRIPTIONS` accepted a Unicode em-dash that `build_pdf()` then crashed on at L1204 (`FPDFUnicodeEncodingException` from helvetica latin-1). `validate.py` passed clean; `validate_user_guide.py` passed clean; the rendering pipeline crashed only when actually run.

Both bugs surfaced post-merge during the ship-time regeneration cascade, forcing same-day fix commits inside the same release that named the bug. The two-step `validate.py` + `generate_user_guide.py` sequence was doing real verification work, but the rendering pipeline invocation was outside `validate.py`'s scope.

v3.7.14's `--dry-run` flag formalizes the rendering pipeline as a verification surface. Invocable as `python3 generate_user_guide.py --dry-run`, it runs the full pipeline — frontmatter parse, dict-parity check, `build_pdf()` rendering, font subsetting, layout pass — without writing the output file. The em-dash class of bug now crashes at the dry-run step, not at ship time. Eligible for `validate.py` subprocess integration in a future release (split off from v3.7.14 scope per Phase 1 §1A item 5 to keep this release tight).

v3.7.14 is the first release shipped under the hardened pipeline. Every release after this one inherits the protection — Unicode characters in dict entries are safe to use, and the `--dry-run` flag catches the next class of latent rendering bugs before they reach validation time.

### Added

- **NEW `assets/fonts/`** directory bundling DejaVu Sans Condensed (regular, Bold, Oblique TTFs). Total ~1.9 MB. Source: DejaVu Fonts v2.37 official GitHub release. License: Bitstream Vera + DejaVu Free (redistributable). Bundled in-repo for deterministic PDF regeneration across environments without a system-install dependency.
- **NEW `assets/fonts/README.md`** documenting source, license, the DVC-over-DV-regular rationale, and update procedure. Points at `../../.planning/v3.7.14/PHASE-0-VERIFICATION.md` for the measurement trail.
- **NEW `--dry-run` flag** on `generate_user_guide.py`. Invocation: `python3 generate_user_guide.py --dry-run`. Exit 0 on clean pipeline; non-zero on any pipeline-level failure (frontmatter parse, dict-parity, font registration, rendering).
- **NEW `docs/user-guide/USER-GUIDE.pdf.baseline-v3.7.14`** baseline file. Byte-for-byte copy of the regenerated PDF; new validator target replacing v3.7.12.
- **Section 24 marketing-studio row** in regenerated USER-GUIDE.pdf — closes the v3.7.13 deferral. Surfaces via the existing auto-generated Sub-Skills table from the dict entry added at v3.7.13 (`generate_user_guide.py:85`). No code edit required for the row itself.
- **NEW `.planning/v3.7.14/`** verification + inventory artifacts following the v3.7.13-established convention. `PHASE-0-VERIFICATION.md` (five-check probe report — font availability, FPDF API, glyph drift, validator normalization, dry-run scope) and `PHASE-1-INVENTORY.md` (file-by-file change inventory, sub-phase ordering with STOPs, decisions register).

### Changed

- **`generate_user_guide.py`** — DejaVu Sans Condensed registered in `UserGuidePDF.__init__` under the family alias `"Body"` so the 20 existing `set_font("Helvetica", ...)` call sites swap via a single family-name change to `set_font("Body", ...)`. `Courier` retained at `L149` for code blocks (ASCII-only content; no Unicode pressure observed in practice). `multi_cell(..., align="L")` applied to `body_text` / `bold_text` / `bullet` / `callout` methods (4 sites) to eliminate justified-text rivers in borderline-wrapping paragraphs that surfaced during 2D visual spot-check — DVC's slight extra width causes some helvetica-fit paragraphs to wrap to two lines under DVC, and fpdf2's `multi_cell` default `align="J"` produced loose word spacing on the first wrapped line. Refinement 3 landed alongside the DVC swap in the same edit cluster; PDF rendered ~4.7% smaller as a side effect (less stream commands per wrapped paragraph). `build_pdf()` gains optional `dry_run: bool = False` parameter; the single `pdf.output(...)` call site is gated behind the flag without further refactor. `__main__` block gains argparse. Net diff: +46 / -27 lines.
- **`generate_user_guide.py:1182`** — Root Files table entry for `USER-GUIDE.pdf` updated to `docs/user-guide/USER-GUIDE.pdf` to reflect the PR #36 (`docs/user-guide/` directory move from v3.7.7) location. One-line fix; closes the path staleness flagged in `.planning/v3.7.14/PHASE-1-INVENTORY.md` §1B D11.
- **`validate_user_guide.py`** — `DEFAULT_BASELINE` retargeted from `USER-GUIDE.pdf.baseline-v3.7.12` to `USER-GUIDE.pdf.baseline-v3.7.14`. Docstring `Defaults:` block updated to match. Layer 0 (`SUB_SKILL_DESCRIPTION_CEILING = 71`) unchanged — DVC drift on real content stays inside the ceiling per Phase 0 §VERIFY 0.3. Layer 1 normalization patterns unchanged — re-baseline is the natural transition (font rendering changes binary structure, not extracted text content).
- **`docs/user-guide/USER-GUIDE.pdf`** — regenerated with DVC + the marketing-studio Sub-Skills row + v3.7.14 metadata cascade. Page count unchanged from v3.7.13 baseline (28 pages) — DVC swap did not cascade to layout reflow.
- **Root `SKILL.md`** — frontmatter `version: 3.7.13` → `3.7.14`; `updated: 2026-05-18` (same-day cascade per the v3.7.10/11/12/13 pattern).
- **`README.md`** — version badge (L1) and footer (L262) cascade `3.7.13` → `3.7.14`.

### Verification

- `python3 validate.py` — ALL CHECKS PASSED. 23 SKILL.md files discovered (1 root + 22 sub-skills). All cross-skill references resolve (including the `../../.planning/v3.7.13/PHASE-0-PROBES.md` refs introduced in v3.7.13's marketing-studio sub-skill). All JSON databases pass schema (filter-memory: 4 entries; quality-memory: 5 entries). All 13 declared root files present. The new `assets/fonts/` and `.planning/v3.7.14/` directories are correctly outside `validate.py`'s iteration scope (it walks `skills/*/SKILL.md` and the explicit root-file list).
- `python3 generate_user_guide.py --dry-run` — exit 0, `DRY-RUN: pipeline OK (28 pages). Output NOT written.` Validates the new infrastructure flag end-to-end: frontmatter parse → dict-parity check → font registration → full `build_pdf()` rendering → output gate. The em-dash class of bug that crashed v3.7.13's render would now surface here, before ship time.
- `python3 generate_user_guide.py` — exit clean. Generated `docs/user-guide/USER-GUIDE.pdf` (28 pages, 90,417 bytes). Page count unchanged from v3.7.13 baseline.
- `python3 validate_user_guide.py` against new v3.7.14 baseline — VALIDATION PASSED. Layer 0 (`SUB_SKILL_DESCRIPTIONS` ceiling check) PASS: all 22 entries ≤ 71 chars (longest: 71, `higgsfield-cinema`; ceiling preserved under DVC per Phase 0 §VERIFY 0.3). Layer 1 (text-extract diff) PASS: no substantive differences after version/date/count normalization. Layer 2 (binary diff) PASS: byte-for-byte identical (candidate = baseline copy).

### Scope acknowledgment

Option B scope (rendering pipeline hardening + PDF refresh, coupled release). The descope path preserved in Phase 0 (Option A — `--dry-run` alone with font + Section 24 row deferred to v3.7.15) was not triggered: Phase 0 §VERIFY 0.3 surfaced that DV regular would overflow the 115mm column, but DVC's measured drift on real `SUB_SKILL_DESCRIPTIONS` content sits inside the 5% threshold the descope criterion gates on. The mixed-font fallback (DVC for tables + DV regular for body text) was considered in Phase 0 §VERIFY 0.3 and is not pursued — visual spot-check during 2D confirmed DVC reads acceptably across body prose.

Out of v3.7.14 scope (deferred to future arcs):

- `cinematic-motion-language.md` translation to `vocab.md` — carried from v3.7.13 backlog
- `gpt-image-2-director` sub-skill — carried from v3.7.13 backlog (sibling director-pattern adoption opportunity)
- `ms_image` ("DTC Ads") full sub-skill — carried from v3.7.13 backlog
- `static-ads.md` translation — carried from v3.7.13 backlog
- Soul Cinema / Nano Banana Pro sibling director skills — carried from v3.7.13 backlog (deferred indefinitely)
- `validate.py` subprocess integration of `--dry-run` — split off from v3.7.14 to keep release tight (this release adds the flag; a future release wires it into the standard pre-release check)
- Courier → DejaVu Sans Mono swap — code blocks remain ASCII-only by existing convention (Phase 1 D8)

### Source corpus + attribution

DejaVu Fonts v2.37 from <https://github.com/dejavu-fonts/dejavu-fonts/releases/tag/version_2_37>. License: Bitstream Vera + DejaVu Free (redistribution permitted including embedding in PDFs and shipping inside Git repositories). Full bundling rationale, license citation, and update procedure at `assets/fonts/README.md`.

### Backlog — updated

- **CLOSED: USER-GUIDE.pdf Unicode font upgrade** (carried from v3.7.13) — DVC swap replaces helvetica latin-1. Em-dashes, en-dashes, curly quotes, ellipsis, and arbitrary Unicode body content render natively. The "dict descriptions and PDF body content must be ASCII-only" workaround constraint lifts.
- **CLOSED: `validate.py` → `generate_user_guide.py` pre-ship sequence formalization** (carried from v3.7.13) — `--dry-run` flag delivers the runnable rendering-pipeline smoke test. `validate.py` subprocess integration deferred to a future release where it earns its own scope (see above).
- **CLOSED: USER-GUIDE.pdf Section 24 row for `skills/higgsfield-marketing-studio/`** (carried from v3.7.13) — surfaces in regenerated PDF as the natural byproduct of the v3.7.13 dict entry meeting v3.7.14's regeneration cascade.
- **CLOSED: USER-GUIDE.pdf Section 24 Root Files row staleness** (Phase 1 D11, pulled in via Refinement 1) — `USER-GUIDE.pdf` Root Files entry updated to `docs/user-guide/USER-GUIDE.pdf` reflecting PR #36's directory move.
- G1 Soul Cinema two-step compositing — UI testing remains pending (carried from v3.7.5)
- G13 Seedance `【镜头N】` syntax — Seedance product-team confirmation pending (carried from v3.7.5)
- `gpt-image-2-director` sub-skill — carried from v3.7.13
- `ms_image` ("DTC Ads") full sub-skill — carried from v3.7.13
- `cinematic-motion-language.md` vocab.md gap-fill — carried from v3.7.13 (4 of 5 pillars need translation; Negative Space already covered)
- `static-ads.md` translation — carried from v3.7.13
- Soul Cinema / Nano Banana Pro sibling director skills — carried from v3.7.13 (deferred indefinitely)
- Phase 0 Probe 0.3-spend + Probe 0.4 — carried from v3.7.13 (schema-level evidence already resolved target claims)
- **NEW: `validate.py` subprocess integration of `generate_user_guide.py --dry-run`** — split-off from v3.7.14's `--dry-run` scope. ~10 LoC addition: a `check_user_guide_renders()` function that subprocesses the dry-run invocation and asserts return code 0; folds into `validate.py`'s standard pre-release health check. Deferred to a release where it earns its own scope rather than ride coattails.
- **NEW: Courier → DejaVu Sans Mono swap** — `generate_user_guide.py:149` still uses Courier (latin-1 core) for code blocks. Same Unicode constraint applies in principle; not exercised in practice (code blocks are CLI commands, paths, dict keys — all ASCII by convention). Defer until a code block ever needs a non-ASCII glyph.
- **NEW: `--dry-run` exit-code matrix documentation** — `--dry-run` is binary (exit 0 / non-zero) in v3.7.14. A future release could distinguish frontmatter errors (exit 2), dict-parity errors (exit 3), rendering errors (exit 4) for finer-grained CI integration. Current binary contract is sufficient for the `validate.py` integration target.

## v3.7.13 — 2026-05-18

Multi-arc patch release adding Marketing Studio coverage. New `skills/higgsfield-marketing-studio/` sub-skill plus a companion `cross-surface-workflow.md` satellite doc, translating Adil's documented director-pattern source corpus (`marketing-studio-director.md` + `higgsfield-content-factory.md`) and SRT/PDF demonstration evidence into our skill's conventions. Phase 3.3 Option B scope: foundational Marketing Studio reference now, cross-surface workflow as a shallow connection layer, gpt-image-2-director / `ms_image` ("DTC Ads") full sub-skill / static-ads / cinematic-motion-language vocab gap-fill all deferred. Live MCP probes preceded all sub-skill prose per Phase 0 discipline — 12 source-corpus reconciliations applied during translation; 0 credits of authorized 2,500-credit budget spent because schema-level evidence retired the spend probes legitimately.

### Recursive plausibility-over-verification — the v3.7.11 discipline applied to source material

v3.7.11 named **plausibility-over-verification** as the failure mode where prose looks right because training-data pattern-matching knows the rough shape of the answer rather than because the author actually read the source files. v3.7.12 applied the discipline recursively to our own prior writing — composing Section 9 of the USER-GUIDE surfaced two inherited content errors in v3.7.11's own `skills/higgsfield-stack/SKILL.md`, both fixed in the same release that named the discipline. The author was the one who tripped it; the author was the one who caught it.

v3.7.13 applies the discipline a third level out: **to source material we ingest.** The Marketing Studio source corpus by Adil is high-craft, production-grade prose — but it carries the same calibration weakness our own prior releases did. Twelve corrections surfaced when we verified content-factory's documented intent against (a) the actual MCP API schema via live probes and (b) Adil's own demonstrated production behavior in the SRT-1/2/3 demos and the PDF prompt export. The same discipline that caught our v3.7.11 math error catches Adil's slug-mismatch table architectural misframing — and the fact that Adil and our v3.7.11 author both tripped the same pattern is the point. Source-material ingestion is now a verification surface, not a translation surface. Every API claim in the new sub-skill cites a Phase 0 live MCP probe verdict; every behavioral claim cites an SRT timestamp or PDF item number.

Three releases, three levels of the same discipline — and v3.7.13's own validation pass caught a fourth instance mid-release: an em-dash in the new `SUB_SKILL_DESCRIPTIONS` dict entry crashed `generate_user_guide.py`'s PDF render. The pattern catches itself. v3.7.13's CHANGELOG documents 12 reconciliations not to critique Adil — he is credited as source throughout — but because honest translation discipline requires naming where documented intent diverged from demonstrated behavior and live API. Adil's source corpus is the substrate; the reconciliations are notes on the substrate's truth at translation time.

### Source-corpus reconciliations (12 corrections + 1 calibration note)

Adil's documented intent in the markdown corpus differed from his demonstrated production behavior in the SRT and PDF evidence in twelve places. Per our verification discipline, live API wins over demonstrated behavior wins over documented intent. Corrections applied during translation. Adil is credited as source throughout (CHANGELOG, sub-skill top-of-file, in-text citations for adopted material); these reconciliations are documentation of source-material truth at translation time, not critique of the source.

The twelve corrections group into four buckets by which layer of the source-corpus the error lives at:

**API-architecture corrections (5)** — the source corpus got the call shape wrong; live MCP probes are the source of truth.

- **#7** `mode` parameter is on `show_marketing_studio`, NOT on `generate_video`. content-factory L681–L692 entire slug-mismatch table is premised on `generate_video.mode` being the routing key — it isn't. Specific claimed mismatches (`ugc_how_to` for Tutorial, `product_showcase` for Hyper Motion) don't exist in the API at all. The actual routing flow uses `show_marketing_studio.mode` on fetch/create actions to set the next-step preset; `generate_video` then renders against the registered routing. Sub-skill §3 documents the actual flow. **Strongest evidence of the recursive plausibility-over-verification pattern.** The slug-mismatch table reads like careful API documentation (specific values you wouldn't guess) but was assembled from training-data plausibility about what API-architecture gotchas usually look like, not from reading the live MCP schema. Same failure mode as v3.7.11's `--soul-id abc123` flag and `--aspect-ratio` hyphen form — confident-sounding output, never verified.
- **#8** `avatars` is a separate top-level media slot from `medias`, NOT a nested parameter. content-factory L630 wrote `avatars: [{ id, type: "preset" }]` inside `params`; the live schema declares `avatars` and `medias` as two distinct top-level media arrays. Call shape is `generate_video(params={...}, avatars=[...], medias=[...])`. Sub-skill §6 documents the correct shape with explicit call example.
- **#9** Avatar `type` field, not `source` field. content-factory L612 said filter the avatar list by `source: "preset"`; the live API returns the field as `type: "preset"`. Minor field-name calibration; CF's filter recommendation works with field renamed.
- **#10** Hook+setting picklist family is 5 presets, not 6. content-factory L193–L194 included `virtual_try_on` (Pro Virtual Try On) in the family; the `generate_video` tool description excludes it (*"supported only for presets UGC, Tutorial, Unboxing, Product Review, UGC Virtual Try On"*). Sub-skill §3 row 9 and §4 opening callout reflect the 5-preset family.
- **#11** Three Marketing Studio models exist: `marketing_studio_video` (video — what CF documented), `marketing_studio_image` (basic image), `ms_image` (display name "DTC Ads" — full DTC ad image gen with brand kits, ad formats, batch up to 20). CF only documented one. Sub-skill §2 names all three with scope-in-this-release noted; `ms_image` ("DTC Ads") additionally covered in `cross-surface-workflow.md` §3 as a Higgsfield-native alternative to GPT Image 2.0 (correction #12).

**Capability corrections (4)** — the source corpus undercounts what the platform can do; SRT/PDF demonstration evidence is the source of truth.

- **#2** Prompt is OPTIONAL. content-factory L469–L485 implies required ("Scene prompt" is a required field in every idea card); SRT-2 [00:09:15] verbatim (*"I don't even need a prompt. I'm just going to hit generate"*) + PDF item 8 (Hyper Motion logo prompt = five words total) demonstrate Marketing Studio generates from preset + product + avatar alone. Sub-skill §7 documents `prompt` as optional.
- **#3** Avatar types broader than CF documents. content-factory L630 documents preset only; SRT-2 [00:08:55] and SRT-3 [00:13:00, 00:18:00] demonstrate preset OR uploaded OR text-generated-in-UI types. Phase 0 schema confirmation: `show_marketing_studio.avatars.type` accepts `'custom' | 'preset'`. Sub-skill §5 documents all three avatar types.
- **#4** Reference media is 4 slots, not 2. content-factory L177 documents product + avatar; SRT-3 [00:11:30] adds custom location image (pre-generated in Soul Cinema); SRT-2 [00:24:00] adds additional-asset image (custom packaging for Unboxing). Sub-skill §6 documents all four slots with the call shape.
- **#5** One-avatar API hard limit, with reference-image workaround. director L143 framed as `≤ 2 humans tracked` (humans, not avatars); SRT-3 [00:19:00] verbatim (*"technically you can't use two avatars"*) + `show_marketing_studio.avatars` parameter documented as `max 1 item` confirm the hard API limit. Workaround: primary avatar in `avatars`, second person passed as reference image in `medias`. Sub-skill §5 documents the constraint + workaround.

**Calibration corrections (2)** — the source corpus over-asserts what's actually flexible; production behavior shows looser rules.

- **#1** Stage 3 batch order is suggested-not-enforced. content-factory L640–L648 documents one order (Entertainment → Street Interview → Unboxing → Product Review → ASMR); SRT-1 [00:06:53–00:15:30] demonstrates a different order in production (Street Interview → Unboxing → Product Review → Entertainment → ASMR). Not a wrong order vs right order — order is flexible. CHANGELOG-only reconciliation; the 5-stage pipeline scaffolding isn't adopted into our sub-skill, so the correction doesn't surface in sub-skill prose.
- **#6** Output prompt format is craft-not-rule. director L213 declares *"one continuous flowing paragraph — no section labels, no tags, no headers"* as a hard output rule; PDF item 10 (Wild Card — Levitation in Clouds), authored by the same person, uses an explicitly sectioned structure with `Style & Mood:`, `Dynamic Description:`, `Static Description:` headers plus quality suffixes and negative inclusions appended. Sub-skill §8 reframes as two valid output styles with guidance on when each fits.

**Cross-surface correction (1)** — the source corpus is missing a whole surface; Phase 0 schema probe surfaced it. Lives in `cross-surface-workflow.md` (correct home), not the sub-skill.

- **#12** Higgsfield platform exposes a native `ms_image` ("DTC Ads") image-generation surface that content-factory and director don't document at all. Brand-kit-aware (accepts `brand_kit_id`), ad-format curated (accepts `style_id`), batch generation up to 20, max 14 reference media per generation. Adil's recipe uses GPT Image 2.0 for the equivalent stage (Stage 1 brand-identity assets in `cross-surface-workflow.md`), but `ms_image` is the more integrated option for users who want brand-kit awareness across many generated images. Workflow doc §3 names both paths.

**Calibration note** (not a correction — two plan-dependent samples disagreeing, neither canonical):

- **Credit cost rate** — content-factory cites Creator plan ≈ $0.02/credit (tagged "approximate," "common"); SRT-1 [00:21:35] + SRT-3 [00:16:00] imply ~$0.06/credit in lived production (consistent across two independent SRT data points: 15,000 credits ≈ $900 for 100 videos = ~150 credits/video; ~$9 for one Wild Card generation). Sub-skill §12 frames as plan-dependent, recommends `transactions()` post-hoc, names ~$0.06/credit as the more credible planning anchor for user budgeting.

### Added

- **NEW `skills/higgsfield-marketing-studio/SKILL.md`** (671 lines, 13 sections per Phase 1 §1A locked inventory). Translates `marketing-studio-director.md` + `higgsfield-content-factory.md` per Phase 3.1 knowledge model with Phase 0 live-MCP findings ingested. Section coverage: §1 What MS is · §2 Two access surfaces + three MS models · §3 The 9 presets · §4 Hook + setting picklists · §5 Avatar handling (3 types, abstract treatment) · §6 Reference media (4 slots) · §7 Generation parameters · §8 Output prompt style (flowing OR sectioned — NOT a hard rule) · §9 What MS cannot do · §10 Worked examples (8 PDF items embedded verbatim) · §11 Cross-surface workflow context · §12 Pricing characteristics · §13 Source acknowledgment.
- **NEW `skills/higgsfield-marketing-studio/cross-surface-workflow.md`** (427 lines, 9 sections per Phase 1 §1B locked inventory). Satellite doc following the `skills/higgsfield-seedance/FAILURE-MODES.md` pattern. Connection layer documenting Adil's four-surface recipe (GPT Image 2.0 → Soul Cinema → Nano Banana Pro → Marketing Studio) plus the Higgsfield-native `ms_image` ("DTC Ads") alternative (correction #12). Embeds PDF items 1–5 verbatim in §3 (clothing mockups + multi-view shoe sheet) and PDF item 14 verbatim in §5 (Quantum Cosmos packaging).
- **NEW `.planning/` directory** introduced for per-release verification artifacts. v3.7.13's verified-facts log at `.planning/v3.7.13/PHASE-0-PROBES.md` sets the pattern for future releases — every API claim in any future sub-skill should cite back to a `.planning/<version>/` probe verdict the way v3.7.13's sub-skill does. Path convention from sub-skill files: `../../.planning/<version>/<filename>` (matches the established `../../vocab.md` repo-root-reference pattern; required by validate.py's relative-from-current-file resolver).
- **NEW `.planning/v3.7.13/PHASE-0-PROBES.md`** verified-facts log. Captures 10 Phase 0 probes (8 free, 2 deferred per discipline), full picklist snapshots (9 hooks, 14 settings, 40 preset avatars), full `marketing_studio_video` parameter schema, and the discovery trail for 12 source-corpus reconciliations.
- **9 Marketing Studio presets** (UGC, Tutorial, Unboxing, Hyper Motion, Product Review, TV Spot, Wild Card, UGC Virtual Try On, Pro Virtual Try On) — display names + slugs + per-preset register notes (Hyper Motion auto pack-shot + accepts logos; TV Spot 5-word-prompt viable; UGC family supports hook+setting picklists; cinematic-secondary presets do not).
- **8 production-grade worked examples** embedded in sub-skill §10, sourced from `PRODUCT GENERATION PROMPTS EXAMPLES.pdf` items 6–13 (Adil's verified SRT-2 production session). Cited by PDF item number + paired SRT timestamp.
- **5 cross-surface workflow examples + 1 packaging example** in workflow doc, sourced from PDF items 1–5 (Soul Cinema clothing + Nano Banana Pro shoes) and PDF item 14 (Nano Banana Pro Quantum Cosmos packaging).
- **3-type abstract avatar handling spec** (preset / uploaded / text-generated-in-UI) per DECISION 7 — names types and field constraints, does NOT enumerate individual preset avatars by name (live-enumeration instruction provided instead).
- **4-slot reference media spec** (product / avatar / location / additional-asset) with explicit call-shape documentation per correction #8.
- **Cross-surface workflow doc** documenting Adil's GPT Image 2.0 → Soul Cinema → Nano Banana Pro → Marketing Studio production recipe as a connection layer between existing sub-skills (`higgsfield-soul` for Soul Cinema depth) plus the Higgsfield-native `ms_image` ("DTC Ads") alternative.

### Changed

- **Root `SKILL.md`** — dispatcher per-trigger routing table gains 3 rows for `higgsfield-marketing-studio` (between Cinema Studio 3.5 row and Multi-shot pipeline row); auto-loaded "Sub-Skills" table gains 1 row (between `higgsfield-cinema` row and `higgsfield-pipeline` row). Both insertions group Marketing Studio adjacent to Cinema Studio — Higgsfield-native video products clustered before cross-cutting pipeline/utility skills. Frontmatter version 3.7.12 → 3.7.13; `updated:` 2026-05-18 (same-day cascade per v3.7.10/11/12 pattern).
- **`generate_user_guide.py`** — `SUB_SKILL_DESCRIPTIONS` dict gains `"higgsfield-marketing-studio": "Marketing Studio - 9 ad presets + 4-15s video + cross-surface"` entry (60 chars, well under the 71-char ceiling). Inserted between `higgsfield-cinema` and `higgsfield-recall` (topical-insertion convention, not alphabetical — corrects DECISION 5's pre-Phase-0 alphabetical assumption per Phase 1 §1F verification). Dict-vs-filesystem parity check passes 22 entries both sides.
- **`README.md`** — version badge (L1) + footer (L262) 3.7.12 → 3.7.13.

### Verification

- **Phase 0 live MCP probes complete.** 10 probes total (8 free, 2 deferred per discipline). **Total spend: 0 credits of authorized 2,500-credit (~$25) budget.** Discipline executed correctly — schema-level evidence retired the spend probes (0.3-spend and 0.4) legitimately, not because the budget wasn't there. Specifically: Probe 0.3-spend was to test slug normalization, but Probe 0.3-b's schema check showed `marketing_studio_video` has no `mode` parameter at all — the spend probe would have tested a hypothesis that schema-level evidence already refuted. Probe 0.4 was to test the random-face-fallback claim, but single-generation can't prove randomness (would require ≥2 generations to compare) and sub-skill practical guidance ("always pass an avatar") doesn't depend on the answer. Saved spend is preserved for a future arc that actually needs it.
- **12 source-corpus reconciliations** surfaced and applied during translation (5 API-architecture / 4 capability / 2 calibration / 1 cross-surface) + 1 calibration note. Full discovery trail at `.planning/v3.7.13/PHASE-0-PROBES.md`.
- `python3 validate.py` — ALL CHECKS PASSED. 23 SKILL.md files discovered (1 root + 22 sub-skills). All frontmatter required fields present on both new files (`SKILL.md` and `cross-surface-workflow.md`). All cross-skill references resolve including the new `../higgsfield-stack/SKILL.md` ref and the new `../../.planning/v3.7.13/PHASE-0-PROBES.md` refs (v3.7.13-established convention — see Added subsection).
- `python3 generate_user_guide.py` — exit clean (exit 0); printed `Generated docs/user-guide/USER-GUIDE.pdf (28 pages)`. Dict-vs-filesystem parity check passes 22 entries both sides. PDF regenerated as script side effect, then reverted to v3.7.12 baseline via `git checkout docs/user-guide/USER-GUIDE.pdf` per Phase 1 deferred-regeneration scope. **PDF not regenerated this release** — content-affecting changes are sub-skill-scoped, not user-guide-scoped (Section 24 row update for `skills/higgsfield-marketing-studio/` deferred to next PDF-touching release per Phase 1 scope decision).
- `python3 validate_user_guide.py` against existing v3.7.12 baseline — VALIDATION PASSED. Layer 0 (`SUB_SKILL_DESCRIPTIONS` ceiling check) PASS: all 22 entries ≤ 71 chars (longest: 71). Layer 1 (text-extract diff) PASS: no substantive differences after version/date/count normalization. Layer 2 (binary diff) PASS: byte-for-byte identical (candidate = baseline copy after revert).
- All 9 preset slugs, hook+setting picklist sample names, avatar handling claims, `marketing_studio_video` parameter spec cross-referenced against Phase 0 probe responses — no invented strings.
- 8 PDF Marketing Studio worked examples cited by exact PDF item number; 5 cross-surface PDF examples + 1 packaging example cited similarly; SRT-sourced claims cited by exact timestamp throughout both files.

### Scope acknowledgment

Phase 3.3 Option B scope. Marketing Studio sub-skill + cross-surface workflow doc shipped as a coupled multi-arc patch in a single release. Highest-credibility material in the source corpus — Adil's verified SRT-2 production session via PDF items 6–13 — captured as a foundational reference library in sub-skill §10. Workflow doc ships shallow — links to existing sub-skills (`higgsfield-soul` for Soul Cinema depth) rather than duplicating surface depth.

Deferred per Option B (and documented in workflow doc §8 surface coverage map for transparency):

- `gpt-image-2-director.md` translation — future arc; sibling director-pattern adoption opportunity that mirrors `marketing-studio-director.md`'s shape
- `ms_image` ("DTC Ads") full sub-skill — named in workflow doc §3 as the Higgsfield-native image-generation alternative to GPT Image 2.0; dedicated coverage deferred to future arc
- `static-ads.md` translation — deferred to future static-image arc (gpt-image-2 static-ad workflow, adjacent but separate from MS video workflow)
- `cinematic-motion-language.md` translation to `vocab.md` — deferred to follow-up release; narrowed scope to 4 of 5 pillars per Block 2B-prime-supplement gap-check (Negative Space pillar already covered in current `vocab.md` L338)
- Soul Cinema / Nano Banana Pro standalone director skills — deferred indefinitely; sibling-director hunt would require investigation work
- `PRODUCT GENERATION PROMPTS EXAMPLES.pdf` items 15–16 — discarded (chain-prompt fragments with no standalone instructional value)
- USER-GUIDE.pdf Section 24 row addition for `skills/higgsfield-marketing-studio/` — deferred to next PDF-touching release (no PDF regen this release)
- Phase 0 Probe 0.3-spend + Probe 0.4 — schema-level evidence already resolved their target claims; spend probes deferred per discipline (not budget constraint)

### Source corpus + attribution

Marketing Studio material translated from source corpus by Adil — `marketing-studio-director.md`, `higgsfield-content-factory.md`, YouTube demonstration series (3 videos: *"Higgsfield MCP + Claude Just Changed Marketing Forever"*, *"I Created a $1,000,000 Brand Using AI"*, *"I Launched a Beauty Brand From Scratch Using AI"*), and `PRODUCT GENERATION PROMPTS EXAMPLES.pdf`. Source-corpus reconciliations documented above are translation-time notes on source-material truth, not critique of the source.

Attribution lands in three places per Phase 1 §10 requirement:

- This CHANGELOG entry (source corpus named, recursive plausibility-over-verification framing applied)
- `skills/higgsfield-marketing-studio/SKILL.md` §13 (Source acknowledgment) — corpus citation + verification-pass framing + cross-reference to Phase 0 log
- In-text PDF item references and SRT timestamps throughout both new files mark every verbatim-or-near-verbatim adopted claim

### Backlog — updated

- G1 Soul Cinema two-step compositing — UI testing remains pending (carried from v3.7.5)
- G13 Seedance `【镜头N】` syntax — Seedance product-team confirmation pending (carried from v3.7.5)
- USER-GUIDE.pdf modernization — CLOSED in v3.7.12 (no v3.7.13 PDF regen)
- **NEW: `gpt-image-2-director` sub-skill** — deferred per Phase 3.3 Option B; sibling director-pattern adoption opportunity
- **NEW: `ms_image` ("DTC Ads") full sub-skill** — named in workflow doc §3, deferred for dedicated coverage
- **NEW: `cinematic-motion-language.md` vocab.md gap-fill** — deferred to follow-up release; 4 of 5 pillars need translation (Negative Space already covered)
- **NEW: `static-ads.md` translation** — deferred to future static-image arc
- **NEW: Soul Cinema / Nano Banana Pro sibling director skills** — deferred indefinitely
- **NEW: USER-GUIDE.pdf Section 24 row** for `skills/higgsfield-marketing-studio/` — deferred to next PDF-touching release
- **NEW: Phase 0 Probe 0.3-spend + Probe 0.4** — schema-level evidence already resolved target claims; spend probes deferred per discipline
- **NEW: USER-GUIDE.pdf Unicode font upgrade** — FPDF defaults to helvetica (latin-1, no em-dash/en-dash/most non-ASCII). v3.7.13 caught this when a Unicode em-dash in the new `SUB_SKILL_DESCRIPTIONS` entry crashed `generate_user_guide.py` at render time (line 1204 in `build_pdf()`). Workaround: keep dict entries ASCII-only. Long-term fix: upgrade `generate_user_guide.py` to a Unicode font like DejaVu Sans (FPDF supports it via `add_font` + `set_font`). Until upgraded, all dict descriptions and any new PDF body content must be ASCII-only — emoji, em-dashes, en-dashes, curly quotes, and most non-ASCII glyphs will crash the script.
- **NEW: `validate.py` → `generate_user_guide.py` pre-ship sequence formalization** — v3.7.12 and v3.7.13 both surfaced latent bugs (RuntimeError; Unicode rendering crash) only when `generate_user_guide.py` ran, after `validate.py` passed clean. The two-step sequence is doing real verification work — `validate.py` checks structure, `generate_user_guide.py` exercises the rendering pipeline. Consider adding a `--dry-run` flag to `generate_user_guide.py` that runs the dict-parity check + PDF build attempt without writing the output file. `validate.py` could then invoke it as part of the standard pre-ship check. Sets up automated catch of font/Unicode/dict-parity issues without manual sequencing.

## v3.7.12 — 2026-05-18

Single-arc release closing the v3.7.7-deferred USER-GUIDE.pdf modernization arc. Brings the user-facing PDF current with five releases of skill content (v3.7.7 production-benchmarks + Seedance depth + Soul depth + new template subdirectories; v3.7.8 higgsfield-stack sub-skill; v3.7.9 worked end-to-end example; v3.7.10 preflight discipline; v3.7.11 plausibility-over-verification + two-step preflight + aspect-ratio enum/style separation + dispatcher pre-delivery checklist). Net change: two NEW PDF sections (Section 4 execution-surface choice + preflight; Section 9 production-quality iteration anchors), six EXTEND sections (3 forward-ref, 12 +3 subsections, 14 +2 subsections, 17 +2 subsections, 20 +1 subsection, 24 row deltas, 25 FAQ rewrite + new Q&A), 20-section renumbering (4→5 through 23→25), full SUB_SKILL_DESCRIPTIONS dict refresh, RuntimeError blocker resolved, two inherited v3.7.11 content errors corrected.

Returns to single-arc cadence per v3.7.11 closeout commitment.

### Pre-existing RuntimeError resolved

`generate_user_guide.py` would have failed at line 798 (out-of-sync dict-vs-filesystem check) since v3.7.8 shipped — `discover_sub_skills()` returns 21 entries (includes higgsfield-stack added v3.7.8), `SUB_SKILL_DESCRIPTIONS` declared only 20. Not noticed across v3.7.8 / v3.7.9 / v3.7.10 / v3.7.11 because none of those releases regenerated the PDF. The Phase 1 inventory caught the latent bug; v3.7.12 fixes it as sub-phase 2A.

### Added

- **NEW Section 4 — "Running the Prompt — CLI / MCP / Bundled Skills / Paste"** (~58 PDF lines). Opens with the layer split ("This skill writes prompts. Higgsfield runs them."). Subsection "The four execution surfaces" names each surface verbatim — Higgsfield CLI (with `higgsfield auth login` and the long-lived-API-tokens-vs-OAuth mechanism that earns the Claude Code / Codex recommendation), Higgsfield MCP custom connector (`mcp.higgsfield.ai/mcp`), Higgsfield bundled skills (`npx skills add higgsfield-ai/skills`, `/higgsfield:generate`), paste-into-higgsfield.ai (always-works fallback). Coexistence callout names the shared-credit-pool + plan-tier-not-surface framing for all four surfaces. Subsection "Pre-Flight: check cost before you generate" presents the two-step pattern (schema verify then cost estimate) with the editorial framing of plausibility-over-verification ("Claude knows enough about Higgsfield to sound right without actually being right") and a 3-column table showing the verbatim MCP and CLI commands for each step. Adjustments-block note + Marketing Studio caveat callout close the section.

- **NEW Section 9 — "What 'Production Quality' Costs — Iteration Anchors"** (~95 PDF lines, two pages of body). Opens with "Production-grade AI cinema runs on iteration." Subsections: headline numbers (108,859 generations / 14 days / 15-person team / ~$400K generation cost / ~$500K total / ~$50M traditional-VFX equivalent ≈ 1% of baseline); acceptance-rate anchors table (5 rows, quadruple-confirmed at 1.0% image / 1.5% video) + callout summarizing the planning rule; per-character iteration anchor (~600 Soul Cinema + ~200 GPT Image 2 = ~800 generations for the Hell Grind lead); per-shot iteration anchor (Prompt 21C: 72 generations for one 10-second establishing shot); iteration-budget projection (a single Kling 3.0 8s 16:9 std generation costs 16 credits; at 1.5% acceptance, 67 attempts × 16 credits ≈ 1,000 credits per finished shot); AI-vs-traditional anchors table (Chuck Russell / Patrick Kalin / Jamafe, 3 rows); 5-criterion falsifiable success rubric; closing callout (preflight by credit-per-keeper, not credit-per-attempt).

- **Section 3 (How to Install) forward-reference** — closing paragraph pointing readers at Section 4 for the four execution paths.

- **Section 12 (Prompting Best Practices) three new subsections** — "Aspect Ratio Is an Enum (Anamorphic is NOT Output Ratio)" (paragraph + 2-row Concern/Where it belongs/Bound by table); "Frame Coordinate System (Seedance)" (qualitative + percentage notation paragraphs, code_block example, directorial-intent-not-guarantee closing); "Spatial Layout Block (multi-character)" (block-structure paragraph + 6-bullet field list + when-to-use closing).

- **Section 14 (Character Sheet Creation) two new subsections + sub-bullet** — "Character Anchor Block (per-shot, 10 attributes)" (build-time-vs-shot-time framing + 10-attribute bullet list verbatim from skills/higgsfield-soul/SKILL.md, closing paragraph naming Spatial Layout Block in Section 12); "Two-Tool Refinement — Soul Cinema + GPT Image 2" (two paragraphs cross-referencing Section 9's per-character iteration anchor); Multi-Form State Tracking sub-bullet pointing at the higgsfield-soul sub-skill.

- **Section 17 (Genre Templates) two new subsections** — "Technique templates (Seedance multi-character coordination)" (4-row table for `top-down-map.md` / `multi-character-anchor.md` / `single-character-position.md` / `worked-example-two-character.md`); "Text-overlay templates" (3-row table for `slogan.md` / `subtitle.md` / `speech-bubble.md`).

- **Section 20 (Troubleshooting) new subsection** — "Seedance Failure Modes — Named Catalog" (8-row Failure mode / What you see / Counter table covering FPS drift, frame-level review, failed-generation salvage, NSFW false-positive, keyframe-forces-invention, physics-state-anchor, multi-motion overload, spatial-awareness failure; counter for spatial-awareness references Section 12's Spatial Layout Block). Closing callout points at sub-skill file for full worked-example deep dives.

- **Section 24 (Repository Contents) four Root Files row deltas** — SKILL.md description CORRECTED from "Model selection guide (routes model questions)" to "Main dispatcher -- routes requests to the right sub-skill" (the prior text was a content error, mistaking root SKILL.md for skills/higgsfield-models/SKILL.md). Three new rows added: DISCIPLINE.md ("Cross-cutting discipline patterns (workflow / output / architectural)"), production-benchmarks.md ("Iteration anchors + Hollywood-validator cost comparisons"), photodump-presets.md ("29 Photodump style presets"). CLAUDE.md and CONTRIBUTING.md deliberately not added (engineering-facing, not end-user content).

- **Section 25 (FAQ) rewrite + new Q&A** — "What changed since v3.0.0?" answer rewritten to span v3.0.0 → v3.7.12 with named themes per era (install-path simplification → metadata refactor → audit-corpus mega-releases → stack-integration arc → this USER-GUIDE refresh). New Q&A inserted: "Do I need the Higgsfield CLI installed?" — answers No, names the four execution paths, cross-references Section 4. Existing FAQ entries unchanged.

- **`docs/user-guide/USER-GUIDE.pdf.baseline-v3.7.12`** (52,711 bytes, 28 pages) added alongside the retained `USER-GUIDE.pdf.baseline-v3.7.7` (19 pages) — baselines accumulate per repo convention.

### Corrections — inherited v3.7.11 content errors

The dogfooding-discipline-as-method that justified the v3.7.11 mega-release applies recursively. Composing v3.7.12's Section 9 (iteration-budget projection) surfaced two inherited content errors in v3.7.11's `skills/higgsfield-stack/SKILL.md`, both fixed in v3.7.12 by the same plausibility-over-verification discipline v3.7.11 introduced. Same release that named the discipline is the one whose author tripped it; v3.7.12 catches both by following the discipline.

- **Math error in § Iteration-budget projection.** v3.7.11 wrote "roughly 67 credits of preflighted spend on average to land one keeper." The math is wrong — 1/0.015 ≈ 67 is the number of attempts, not credits. At 16 credits per attempt on Kling 3.0 8s 16:9 std, per-keeper cost is roughly 1,000 credits. v3.7.12 corrects to "roughly 67 attempts on average to land one keeper — at 16 credits per attempt, that's about 1,000 credits per finished shot." Plausibility-over-verification surface: "67" was the right number in the calculation chain, just attached to the wrong unit. The arithmetic chain was never run end-to-end.

- **Surface-count inconsistency in § Plan tier, not surface.** v3.7.11 wrote "All three surfaces share one credit pool and one job queue" — a holdover from when paste-into-higgsfield.ai wasn't treated as a peer of CLI / MCP / bundled-skills. All four surfaces share the credit pool and queue in fact; v3.7.12 corrects to "All four surfaces share one credit pool and one job queue" and lists all four explicitly.

`skills/higgsfield-stack/SKILL.md` frontmatter version bumped 1.2.0 → 1.2.1 (patch — content corrections, no API change).

### Changed

- **`generate_user_guide.py`** — 20-section renumbering 4→5 through 23→25 across the TOC list, section_title() calls, comment markers, and one body cross-reference ("See I2V Gate rule in Section 10" → "Section 12"). Module docstring "Section 22" reference → "Section 24"; module docstring "v3.6.5" provenance reference refreshed to acknowledge the v3.7.12 dict refresh. TOC rendering switched from `pdf.v3_tag()` to `pdf.new_tag()` — corrects v3.7.12 NEW markers from rendering as " v3.0 " green badges (a v3.0-era artifact) to generic blue " NEW " badges. Body-level `pdf.v3_tag()` calls inside Sections 11 (CS 3.0), 12 (Seedance Best Practices), 13 (Soul ID), 20 (CS 3.0 Diagnostic Tree) retained — those correctly tag v3.0-era platform features being described.

- **`SUB_SKILL_DESCRIPTIONS` dict** — three entries: ADD `higgsfield-stack` ("CLI / MCP / bundled-skills coexistence + two-step preflight", 57 chars, inserted between `higgsfield-soul` and `higgsfield-audio` to preserve existing dict order); REFRESH `higgsfield-soul` ("Soul ID + Character Anchor Block + Two-Tool Refinement Pipeline", 63 chars — gains v3.7.7 Anchor Block + Two-Tool Pipeline, loses Soul Cast 3.0 + Soul Cinema CS-default phrasing); REFRESH `higgsfield-seedance` ("Seedance 2.0 + frame coords + spatial layout + named failure modes", 66 chars — gains v3.7.7 Frame Coordinate System + Spatial Layout + FAILURE-MODES, loses "working modes" + "content-filter preflight" phrasing). All 18 other entries unchanged. All 21 entries verified at or under the 71-char column ceiling.

- **`skills/higgsfield-stack/SKILL.md`** — frontmatter version 1.2.0 → 1.2.1; § Iteration-budget projection math corrected; § Plan tier, not surface surface count corrected (see Corrections above).

- **`validate_user_guide.py`** — `DEFAULT_BASELINE` retargeted from `USER-GUIDE.pdf.baseline-v3.7.7` to `USER-GUIDE.pdf.baseline-v3.7.12`; docstring Defaults example updated to match. v3.7.7 baseline file retained per accumulation convention.

- **Root `SKILL.md` frontmatter** — version 3.7.11 → 3.7.12. `updated:` 2026-05-18 (same-day cascade).

- **`README.md`** — version badge 3.7.11 → 3.7.12, footer 3.7.11 → 3.7.12.

- **`docs/user-guide/USER-GUIDE.pdf`** — regenerated. 19 pages → 28 pages (+9 pages). 33,679 bytes → 52,711 bytes (+56% file size).

### Verification

- `python3 generate_user_guide.py` — exit clean, prints `Generated docs/user-guide/USER-GUIDE.pdf (28 pages)`. No RuntimeError, no warnings.
- `python3 validate_user_guide.py` against new v3.7.12 baseline — Layer 0 (`SUB_SKILL_DESCRIPTIONS` ceiling check) PASS: all 21 entries ≤ 71 chars (longest: 71). Layer 1 (text-extract diff) PASS: no substantive differences after version/date/count normalization. Layer 2 (binary diff) PASS: byte-for-byte match (candidate = baseline copy).
- `python3 validate.py` — ALL CHECKS PASSED. No broken refs introduced by the dict edit, the Section 24 row updates, or the v3.7.12 frontmatter cascade.
- TOC text-extract from regenerated PDF — 25 items, NEW markers exactly on Section 4 and Section 9, prior NEW markers on Sections 11 (CS 3.0) and 12 (Seedance Best Practices) stripped as expected.
- `SUB_SKILL_DESCRIPTIONS` dict-vs-filesystem parity check — both sides 21 entries, no missing or extra.
- Page count delta vs baseline v3.7.7: 19 → 28 (+9 pages), consistent with two NEW sections + six EXTEND deltas. Came in under the inventory's optimistic 32–36-page estimate because FPDF packs content denser than the estimate assumed; net content gain matches scope.
- All CLI commands, MCP tool shapes, model IDs, and platform vocabulary in Section 4 cross-referenced against v3.7.10 / v3.7.11 live-verified syntax logs (no invented strings).

### Scope acknowledgment

Arc A scope (hand-edit hardcoded content to bring current; preserve editorial voice; no generator architectural change). Arc B (extract content from skill files into markdown-rendered PDF) and Arc C (extract structural data into config) considered and deliberately not pursued — the PDF's editorial voice is intentionally distinct from the skill files' technical voice, and an automated content-extraction pipeline would lose that distinction. v3.7.12 closes the "PDF modernization is the deferred dedicated arc" framing that v3.7.7 / v3.7.8 / v3.7.9 / v3.7.10 / v3.7.11 all cited. Future content drift addressed per release cadence (touch the PDF only when content-affecting changes ship in the same release).

In-release skill-file edits beyond root SKILL.md frontmatter (Phase 2 DO-NOT list override): the math-error and surface-count corrections in `skills/higgsfield-stack/SKILL.md` were discovered while composing Section 9, and fixing only the PDF would have left Claude producing wrong math at runtime while the human reads right math in the guide. Path 3 (fix both) chosen over Path 1 (PDF only) — keeping the agent and the documentation consistent. Both corrections cited in Corrections subsection above.

### Backlog — updated

- G1 Soul Cinema two-step compositing — UI testing remains pending (carried from v3.7.5)
- G13 Seedance `【镜头N】` syntax — Seedance product-team confirmation pending (carried from v3.7.5)
- USER-GUIDE.pdf modernization — CLOSED in v3.7.12

## v3.7.11 — 2026-05-18

Mega-release. Fourth one-time exception to the v3.7.7 closeout single-arc commitment, justified by dogfood-corpus continuity from same-day v3.7.10 release-night testing. Five co-headlined sub-phases (CH-1 README correction / CH-2 higgsfield-stack two-step preflight expansion / CH-3 higgsfield-prompt conflict-resolution / CH-4 aspect-ratio reality vs style vocab / CH-5 dispatcher pre-delivery checklist restructure) plus CH-6 DISCIPLINE.md framework-innovation pattern. Single named failure mode unifies the corpus: **plausibility-over-verification**.

### Fourth one-time exception mega-release

The v3.7.5 / v3.7.6 / v3.7.7 sequence framed itself as three one-time exceptions. v3.7.8 introduced single-arc cadence "unless audit-corpus continuity creates a comparable case." v3.7.11 is that comparable case — but the audit input is dogfood corpus, not discovery corpus. Same-day v3.7.10 release-night testing across two surfaces (CLI on Mac terminal, MCP via Cowork) produced six distinct findings whose remediation benefits from being shipped coherently rather than fragmented across five patch releases.

### Dogfood corpus — what was actually observed

CLI pass (2026-05-18, higgsfield 0.1.40 built 2026-05-12, Claude Code in real time):

- Attempt 1: dispatcher discipline skipped (no routing line, never read root SKILL.md or higgsfield-prompt before answering, never appended shared negative constraints). Output was plausible cinematography from training pattern-matching off vocab.md / model-guide.md grep snippets.
- Attempt 2 (after diagnostic): dispatcher discipline followed correctly, but produced `2.35:1` aspect ratio in the header and `--aspect-ratio` (hyphen) flag form in the preflight call — both invented from training plausibility. CLI rejected on first cost call: `Error: Invalid values: aspect_ratio=2.35:1 (allowed: 16:9,9:16,1:1)`. Underscore form `--aspect_ratio` verified working; returned 16 credits for the corrected 16:9 invocation.

MCP pass (2026-05-18, Cowork workspace with higgsfield-ai-prompt-skill repo mounted, Higgsfield MCP at mcp.higgsfield.ai/mcp, paid plan):

- Routing line present and well-specified (named four sub-skills with rationale).
- Schema verification fired without being asked: `models_explore(action="get", model_id="kling3_0")` called before any cost call.
- Preflight invocation correct: `generate_video(..., get_cost: true)` with no job submission; respected user-stated guardrail.
- Adjustments block surfaced from the MCP response (`mode=std`, `sound=on` defaults) — net-new intel for v3.7.11.
- Iteration-budget tie-in to production-benchmarks.md 1.5% acceptance rate produced unprompted ("~67 credits of preflighted spend on average to land one keeper").
- But: "16:9 anamorphic" written into the prompt body — incoherent (anamorphic is a >2:1 ratio register, not a 16:9 modifier). Negation-form constraints used instead of the canonical positive phrasing in negative-constraints.md. Prompt exceeded 200-word soft cap.

The contrast is informative: CLI failed at the workflow level (skipped the dispatcher), MCP succeeded at workflow but failed at vocabulary fidelity (paraphrased style register from training instead of from vocab.md). Both failures share the same mechanism — plausibility-over-verification — and v3.7.11 ships the structural fixes for both modes.

### CH-1 — README v3.7.10 correction (Bundle A)

The PRE-FLIGHT block in the README end-to-end example, added in v3.7.10, did not surface the schema-verification step and included an unverified `--soul-id abc123` flag whose hyphen-vs-underscore form was never confirmed against the live CLI. Both gaps surfaced during CLI dogfood. Correction: NEW first sub-step "SCHEMA VERIFY" added above the existing CLI cost call (`higgsfield model get kling3_0` / MCP `models_explore`); `--aspect_ratio` underscore form re-confirmed against the live CLI and left in place; the unverified `--soul-id abc123` line dropped from BOTH the PRE-FLIGHT block AND the post-PRE-FLIGHT `generate create` block, replaced with a placeholder comment pointing at `higgsfield model get <model>` for supported media roles (cleaner than silently picking a flag form that may be wrong). A closing note added separating output-ratio enum (16:9 / 9:16 / 1:1 for Kling 3.0) from anamorphic style vocabulary. Honest correction to a prior release — and a same-release application of the CH-6 plausibility-over-verification discipline: the v3.7.10 author typed `--soul-id abc123` because it looked right, not because it had been verified, which is exactly the failure mode v3.7.11 names.

### CH-2 — higgsfield-stack two-step preflight (Bundle B)

`skills/higgsfield-stack/SKILL.md` frontmatter version 1.1.0 → 1.2.0. New H3 § Two-step preflight inserted before § Verified preflight surfaces — names step 1 (schema verify) and step 2 (cost estimate) as the canonical pattern, with the failure mode this prevents (plausibility-over-verification) called out by name and cross-referenced to DISCIPLINE.md Tier 1. The three-column verified preflight surfaces table extended with a new top row for schema verification (`models_explore` / `higgsfield model get`). New paragraph on the MCP `adjustments` block — net-new intel from MCP dogfood, documents the asymmetry with CLI `--json` output. New H3 § Iteration-budget projection ties single-shot cost to production-benchmarks.md acceptance rates, formalizing the unprompted MCP-pass behavior as a discipline rule.

### CH-3 — higgsfield-prompt conflict resolution (Bundle C part 1)

`skills/higgsfield-prompt/SKILL.md` frontmatter version 3.4.0 → 3.5.0 (minor — additive H2 + § Common Prompt Mistakes update). New § Conflict resolution between sub-skills inserted after § Identity vs. Motion Separation Rule (cross-cutting discipline zone, not Seedance-scoped). Three-step hierarchy: explicit user direction > scene archetype > emotion-sync register. Closing rule: surface the resolution when non-obvious — transparent picking is the discipline, silent picking is the failure mode. MCP-pass dogfood demonstrated this discipline already; v3.7.11 promotes it from emergent behavior to documented rule.

### CH-4 — Aspect-ratio reality vs. style vocabulary (Bundle C part 2)

Two-file edit. (A) `skills/higgsfield-prompt/SKILL.md` § Common Prompt Mistakes — existing "Aspect ratio inside the prompt body" table row Fix column updated with per-model enum reference (Kling 3.0: 16:9 / 9:16 / 1:1 only — check `higgsfield model get <model>` / MCP `models_explore`); new disambiguation callout blockquote added immediately below the table (before the existing negative-constraints blockquote), naming the "16:9 anamorphic" incoherence and separating output ratio (header, enum-bounded) from anamorphic style cues (Look line, stylistic). (B) `vocab.md` — new H3 § Aspect Ratio: output spec vs. style register added inside the existing § Visual Style Vocabulary, immediately after § Named Platform Styles (placed next to the source of the confusion — the existing Anamorphic entry in Named Platform Styles). Two-row table distinguishes output spec from style register. Triggered by MCP-pass dogfood — even with full skill discipline, "16:9 anamorphic" bled across the boundary because the skill itself had not drawn the boundary explicitly.

### CH-5 — Dispatcher pre-delivery checklist (Bundle D)

Root `SKILL.md` — the prior `## MANDATORY WORKFLOW` and `## HARD RULES` sections folded into a single `## HARD RULES — pre-delivery checklist`. Previous structure stated rules as prohibitions at the top of the file ("NEVER write a prompt without reading X") — depends on the agent choosing to obey before it writes, and v3.7.10 dogfood proved that mechanism skippable when output looks plausible. New structure expresses the rules as a pre-delivery checklist: 8 items the agent confirms BEFORE sending the response, with explicit framing that any unconfirmed item means the response is incomplete. Items cover routing line presence, routed sub-skills opened and READ (grepped snippets do not satisfy), named vocabulary verified not invented, MCSLA structure, shared negative constraints with positive phrasing, preflight surfacing when applicable, aspect-ratio-as-enum-not-free-form, and the 200-word soft cap. The plausibility-over-verification failure mode is named explicitly in the section opener and tied to items 2, 3, 7. Verified during edit that no prior MANDATORY WORKFLOW or HARD RULES item was silently dropped in the merge — all 10 prior items mapped to a new home or absorbed into the opening framing.

### CH-6 — DISCIPLINE.md plausibility-over-verification pattern (framework innovation)

`DISCIPLINE.md` Tier 1 — Workflow Discipline gains a new pattern: § Plausibility-over-verification, inserted between § Lock-before-generate and § Falsifiable Success Criteria. Pattern body names the recurring trap (training-data plausibility producing output that looks correct without verifying against platform ground truth), names the demonstrated dogfood corpus (CLI invented flag forms + invalid aspect ratio; MCP paraphrased style register across boundary), and points to the CH-5 pre-delivery checklist as the operationalization. This is the unifying mechanism across both dogfood passes — same failure mode, different surfaces, same counter.

### Framework innovation candidate

| FI | Source | Insight |
|---|---|---|
| **FI10 (NEW)** | v3.7.10 dogfood corpus (CLI + MCP, same day) | Plausibility-over-verification is a cross-platform recurring trap; pre-delivery checklists catch what top-of-file prohibitions miss; dogfooding a release the same day surfaces failure modes that discovery corpus cannot |

### Changed

- **Root `SKILL.md` frontmatter** — version 3.7.10 → 3.7.11. `updated:` 2026-05-18.
- **Root `SKILL.md` body** — prior `## MANDATORY WORKFLOW` and `## HARD RULES` sections folded into a single `## HARD RULES — pre-delivery checklist` per CH-5.
- **`skills/higgsfield-stack/SKILL.md` frontmatter** — version 1.1.0 → 1.2.0. `updated:` 2026-05-18.
- **`skills/higgsfield-stack/SKILL.md` body** — § Preflight discipline expanded per CH-2 (new H3 Two-step preflight, new schema-verification row in surfaces table, new Adjustments-block paragraph, new H3 Iteration-budget projection).
- **`skills/higgsfield-prompt/SKILL.md` frontmatter** — version 3.4.0 → 3.5.0. `updated:` 2026-05-18.
- **`skills/higgsfield-prompt/SKILL.md` body** — new H2 § Conflict resolution between sub-skills (CH-3) + § Common Prompt Mistakes table row updated + new disambiguation callout blockquote below table (CH-4 A).
- **`vocab.md`** — new H3 § Aspect Ratio: output spec vs. style register added inside § Visual Style Vocabulary per CH-4(B).
- **`DISCIPLINE.md`** — new Tier 1 § Plausibility-over-verification per CH-6, inserted between § Lock-before-generate and § Falsifiable Success Criteria.
- **`README.md`** — version badge 3.7.10 → 3.7.11, footer 3.7.10 → 3.7.11, PRE-FLIGHT block in end-to-end example corrected per CH-1 (SCHEMA VERIFY sub-step added, unverified `--soul-id abc123` dropped from both PRE-FLIGHT and post-PRE-FLIGHT `generate create` blocks with placeholder comments, anamorphic-vs-output-ratio closing note added).

### Verification

All CLI syntax and behavior in this release was verified live on 2026-05-18 against `higgsfield 0.1.40 (built 2026-05-12)`. CLI calls run: `higgsfield model get kling3_0`, `higgsfield generate cost kling3_0 --prompt "test" --aspect_ratio 16:9 --duration 8 --json` (returned 16 credits), `higgsfield generate cost kling3_0 --prompt "test" --aspect_ratio 2.35:1 --duration 8` (returned `Error: Invalid values: aspect_ratio=2.35:1 (allowed: 16:9,9:16,1:1)`). MCP behavior verified via Cowork workspace using mcp.higgsfield.ai/mcp connector — `models_explore` returned same schema as CLI, `generate_video` with `get_cost: true` returned cost + adjustments block. No invented flag names, no invented param values, no invented preset names in this release. The previously-shipped `--soul-id abc123` in v3.7.10's README PRE-FLIGHT block was an exception — never verified against the CLI — and is dropped in CH-1 rather than silently kept.

### Scope acknowledgment

v3.7.11 is the largest release since v3.7.7 by content surface (5 sub-phases + framework-innovation pattern across 7 files). Justified as the fourth one-time exception per v3.7.8 commitment language. v3.7.12+ returns to single-arc cadence unless audit-corpus continuity creates another comparable case. Same-day release per Peter decision at v3.7.11 planning handoff. USER-GUIDE.pdf modernization remains the deferred dedicated arc (same as v3.7.8, v3.7.9, v3.7.10) — PDF not regenerated for v3.7.11.

### Backlog — unchanged

- G1 Soul Cinema two-step compositing — UI testing remains pending (carried from v3.7.5)
- G13 Seedance `【镜头N】` syntax — Seedance product-team confirmation pending (carried from v3.7.5)
- USER-GUIDE.pdf modernization — deferred dedicated arc

## v3.7.10 — 2026-05-18

Patch release: surfaces the pre-flight cost-check pattern that already exists on both the MCP (`get_cost: true` parameter on `generate_image`/`generate_video`, plus `balance` and `transactions` tools) and the CLI (`higgsfield generate cost`, `higgsfield account status`, `higgsfield account transactions`). Names preflight as part of Tier 1 *Lock-before-generate* discipline tied to production-benchmarks.md 1% / 1.5% acceptance rates. Replaces vague "MCP priority queue" mental model with verified "one credit pool, one job queue, queue priority is plan-tier-dependent" framing. Same-day follow-up to v3.7.9, completing the v3.7.8/v3.7.9/v3.7.10 stack-integration arc.

Single-arc, two files changed (plus version cascade).

### Added

- **`skills/higgsfield-stack/SKILL.md` § Preflight discipline** (NEW H2 section, ~60 lines). Three-column verified preflight-surface table (MCP / CLI / bundled skills) covering cost estimate, credit balance + plan, and recent transactions. Documents CLI naming gotcha (`account status` is canonical; `account balance` / `account credits` are NOT valid subcommands and fall through to parent help). Includes `--json` scripting note for CI/Claude Code parsing, marketing-studio `get_cost` exclusion caveat per official MCP tool description, bundled-skills "drop to CLI for the check" pattern (same auth, same workspace). New H3 § Plan tier, not surface, controls queue priority replaces any priority-queue surface-routing mental model with verified shared-queue + plan-tier framing. New H3 § When to surface preflight in this skill's output gives the trigger criteria (executing intent + video-class model OR named budget constraint OR iteration-heavy structure) for adding preflight lines to skill output.

- **README.md PRE-FLIGHT block in end-to-end example.** New block inserted between this skill's prompt output and the three-surface fan-out, showing all three preflight invocations side-by-side with the same Kling 3.0 + Soul ID worked example. Optional account-check sub-block (MCP balance/transactions vs CLI `account status` / `account transactions`) appended for completeness. Plus a one-line forward reference from the README to the new `higgsfield-stack` § Preflight discipline section.

### Changed

- **Root `SKILL.md` frontmatter** — version 3.7.9 → 3.7.10, `updated:` 2026-05-18 (same-day cascade).
- **`skills/higgsfield-stack/SKILL.md` frontmatter** — version 1.0.0 → 1.1.0 (minor bump, new H2 section added), `updated:` 2026-05-18.
- **`README.md`** — version badge 3.7.9 → 3.7.10, footer 3.7.9 → 3.7.10.

### Verification

All CLI syntax in this release was verified live against `higgsfield 0.1.40 (built 2026-05-12)` via `higgsfield generate cost --help`, `higgsfield account --help`, `higgsfield account status --help`, plus failed-falls-through-to-parent test of `higgsfield account balance --help` and `higgsfield account credits --help` (both confirmed as NOT valid subcommands — canonical name is `status`). MCP tool shapes (`get_cost: true`, `balance`, `transactions`) verified against current Higgsfield MCP tool descriptions at `mcp.higgsfield.ai/mcp`. No invented flag names, subcommand names, or parameter names in this release.

### Scope acknowledgment

v3.7.10 is intentionally narrow: one new section in one sub-skill + one block in README + version cascade. No sub-skills beyond higgsfield-stack modified, no new framework-innovation candidates, no PDF regenerated (USER-GUIDE.pdf modernization remains the deferred dedicated arc, same as v3.7.8 and v3.7.9). Closes the v3.7.8 → v3.7.9 → v3.7.10 stack-integration micro-arc: 3.7.8 introduced higgsfield-stack, 3.7.9 anchored it with a worked example, 3.7.10 adds preflight discipline. Returns to single-arc cadence per the v3.7.7 closeout commitment.

## v3.7.9 — 2026-05-18

Patch release: adds a worked end-to-end example to the README's "Higgsfield Stack Integration" section, showing how this skill's prompt output flows into all three Higgsfield execution surfaces (CLI, bundled skills, MCP) for a real request. Same-day follow-up to v3.7.8 — the v3.7.8 prose was abstract; v3.7.9 anchors the abstraction with a copy-pasteable concrete example.

Single-arc, README-only.

### Added

- **README.md "End-to-end example" subsection.** New H3 inside the Higgsfield Stack Integration section, positioned between the bundled-skills subsection and the coexistence-rules pointer. Worked example uses a "cinematic chase scene with Soul character" request, routed through `kling3_0` with a `--soul-id` flag, showing all three execution paths (CLI, bundled skills, MCP) and the layer-split principle reinforced in the closing paragraph.

### Changed

- **README.md** — version badge 3.7.8 → 3.7.9, footer 3.7.8 → 3.7.9.
- **Root `SKILL.md` frontmatter** — version 3.7.8 → 3.7.9, same-day `updated:` date.

### Scope acknowledgment

v3.7.9 is intentionally narrow: one file changed (README.md), plus the version-bump cascade. No sub-skills modified, no new framework-innovation candidates, no PDF regenerated (USER-GUIDE.pdf modernization remains the deferred dedicated arc, same as v3.7.8).

## v3.7.8 — 2026-05-18

Single-arc release: adds the `higgsfield-stack` sub-skill, which documents how this prompt-construction skill coexists with Higgsfield's own official tooling (their CLI, MCP custom connector, and bundled `higgsfield-ai/skills`). The two surfaces complement each other cleanly — our skill stays in its lane as the prompt-construction + production-discipline layer, theirs handles auth, upload, job submission, polling, and result delivery. No merge, no absorption, no dependency on their stack being present.

Returns to single-arc scope per the v3.7.7 closeout commitment, after the v3.7.5 / v3.7.6 / v3.7.7 mega-release sequence.

### Added

- **`skills/higgsfield-stack/SKILL.md`** (NEW sub-skill, 154 lines, v1.0.0). Documents the three official execution surfaces (CLI binary `higgsfield` / `higgs` / `hf`, MCP custom connector at `mcp.higgsfield.ai/mcp`, bundled skills repo at `higgsfield-ai/skills` v0.3.0 with `higgsfield-generate` / `higgsfield-soul` / `higgsfield-product-photoshoot`). Includes a layer-split principle, detection signals per surface, five coexistence rules, the `higgsfield-soul` naming collision callout (theirs trains the Soul Character; ours constructs the prompts that use the trained identity), handoff templates for each surface, Seedance preflight recommendation when CLI is present, and explicit non-goals.

- **README.md Higgsfield Stack Integration section.** New section between "Install" and "Structure" linking users to the three official Higgsfield surfaces (CLI, MCP, bundled skills) with the account requirement noted up front. Points to `skills/higgsfield-stack/SKILL.md` for the full coexistence rules.

### Changed

- **Root `SKILL.md` routing table** — three new rows added in the env/meta zone after the seedance row, routing CLI/MCP/bundled-skills triggers and handoff questions to `higgsfield-stack`.
- **Root `SKILL.md` sub-skills table** — one new row for `higgsfield-stack` after the seedance row.
- **Root `SKILL.md` frontmatter** — `version: 3.7.7 → 3.7.8`, `updated: 2026-05-18` (unchanged date — same-day release).
- **`README.md` version badge** — `version-3.7.7-blue → version-3.7.8-blue`.
- **`README.md` footer** — `v3.7.7 (updated 2026-05-18) → v3.7.8 (updated 2026-05-18)`.
- **`CLAUDE.md`** — sub-skill directory count corrected from `19` to `21`. The original `19` count was already stale on `main` before this release (current `main` had 20 sub-skills); this release adds the 21st, and the count is brought current in the same edit.

### Deferred to v3.7.9+

- **USER-GUIDE.pdf Section 22 "Root Files" update.** PR #36 (post-v3.7.7 housekeeping) deferred a Section 22 row update to the first content release. v3.7.8 is that release, but the PDF generator (`generate_user_guide.py`) has hardcoded content sections, so registering `higgsfield-stack` in the PDF is its own dedicated arc. The deferred Section 22 update from PR #36 plus `higgsfield-stack` registration now both ride into the PDF modernization arc. USER-GUIDE.pdf for v3.7.8 was not regenerated.

- **No new framework-innovation candidates.** v3.7.8 is intentionally small-scope; no FI logging.

### Scope acknowledgment

v3.7.5, v3.7.6, and v3.7.7 were mega-releases. v3.7.7's release notes committed to "single-arc scope unless audit-corpus continuity creates a comparable case." v3.7.8 is the first release under that commitment — one sub-skill, two file edits, no co-headline.

## v3.7.7 — 2026-05-18

Mega-release. Co-headlined: CH-1 production-benchmarks.md (Hell Grind 90-min Cannes feature anchors) + CH-2 Seedance depth (Frame Coordinate System + Spatial Layout Block + FAILURE-MODES.md new file + Character Anchor Block + Group F/P/G13b/Group H consolidation) + CH-3 templates library bootstrap (7 NEW template files in 2 new sub-directories) + CH-4 image-models expansion (G18 Nano Banana Pro production-team observations + Group H location-handling) + CH-5 DISCIPLINE.md SC1 reframe + SC2 anti-bombast paradox + 7 new patterns. **Third one-time exception to the harder-single-arc commitment**, after v3.7.5 backlog closeout and v3.7.6 — co-headlined by explicit Peter decision at Phase 0 → Phase 1 handoff. Largest release in repo history by sub-phase count (9 content sub-phases + 1 release ceremony sub-phase).

### Third one-time exception mega-release

Explicit framing acknowledgment. The v3.7.5 / v3.7.6 / v3.7.7 sequence is three mega-releases in succession. The harder-single-arc commitment from v3.7.5's closeout was the intent; mega-release scope kept making sense because v3.7.5+v3.7.7 audit corpus yielded cross-corpus continuity findings that benefited from being shipped as a coherent set rather than fragmented across multiple single-arc releases. The exception sequence does not establish a new pattern: v3.7.8+ returns to single-arc scope unless audit-corpus continuity creates a comparable case.

### CH-1 — Production-benchmarks.md (NEW file)

New `production-benchmarks.md` at repo root (~159 lines). Hell Grind 90-min Cannes feature anchors documented from the Higgsfield team's "Road to Cannes" three-episode documentary: 108,859 generations across 14 days; 9,540,047 credits; ~$400K generation cost / ~$500K total; 15-person team. Quadruple-confirmed 1.0% image acceptance + 1.5% video acceptance rates. ~600 + ~200 = ~800 generations per-character iteration anchor (Jack lead character). 72 generations for one 10-second establishing shot (per-shot iteration anchor). Three Hollywood-validator cost anchors (Chuck Russell $5M / Patrick Kalin $15-20M / Jamafe qualitative). Falsifiable AI-cinema success-criteria 5-rubric (committed before generation began). Plus § Source methodology documenting **Catch #15 instance #1** (credit-rate-per-dollar divergence finding — Ep. 1 $0.060/credit vs Ep. 3 $0.042/credit; resolved per LOCK 19 protocol with ship-both-anchors + caveat decision).

`validate.py` single-line addition registers production-benchmarks.md in `expected_root_files` (LOCK 20).

+159 lines new file + 1 line validate.py update in PR #26 (sub-phase 2a).

### CH-2 — Seedance depth across sub-phases 2b-i / 2b-ii / 2c-i / 2c-ii

Largest CH cluster by sub-phase count. Four sub-phases compose the Seedance-cluster expansion.

- **2b-i — G21 Frame Coordinate System + G19 Spatial Layout Block** in `skills/higgsfield-seedance/SKILL.md`. New H2 § Frame Coordinate System with 4 H3 sub-sections (Qualitative anchors / Percentage notation / Pair the two notations / Not a mathematical guarantee). New H2 § Spatial Layout Block with 3 H3 sub-sections (What goes in the block / When to use / Block-and-prompt fit). Tightened per Decision B self-review (159 → 130 lines after honest load-bearing-vs-padding classification). **Catch #14 instance #1** documented (vocabulary-introducing orientation budget overrun). +130 lines in PR #27.

- **2b-ii — Group F single-vs-multi-shot decision + Group P reference-handling + G13b multi-language workaround** in same file. NEW H3 § Per-Image Role Convention under § Reference Roles (per-slot @Image1/@Image2/@Image3/@Image4 + @Video1/@Video2 + @Audio1 role table). § Load-Bearing Rule extended with modality-routing paragraph (P142 upload-to-Claude-not-Seedance discipline). NEW H3 § Single-vs-multi-shot decision under § Output Format (consolidates P54+P59+P111+P112+P126). NEW H2 § Multi-Language Prompt Workarounds + H3 § Chinese (as of 2026-05-17) per LOCK 16 (historical-context framing per Rx-3 mitigation). Pre-commit Decision B tightening applied. +84 lines in PR #28.

- **2c-i — FAILURE-MODES.md (NEW file)** in `skills/higgsfield-seedance/`. New sibling reference (293 lines post-tightening) cataloging 8 Seedance render-failure modes with 4-field structure (Symptom / Mechanism / Counter / Worked example): FPS drift + frame-by-frame de-duplication / Frame-level review is mandatory / Failed-generation salvage / NSFW false-positive (provider-side) / Keyframe-consistency forces invention / Physics-state-anchor / Multi-motion camera overload / Spatial-awareness failures. Plus § Self-repair before delivery (7-item pre-delivery prevention checklist — anchors 2g Pre-delivery discipline cross-ref per content-map line 417) + § Cross-references (8 back-links to SKILL.md sections + sibling skills). Frontmatter matches MODELS-DEEP-REFERENCE.md sibling-file precedent. **Catch #14 instance #2** documented (catalog-format structural floor overrun, 312 → 293 lines after Decision B tightening per Decision A-tightened approval). **FI6 framework innovation candidate** logged (catalog-format sub-phases have higher structural floor). +293 lines new file + 7 lines SKILL.md forward-link in PR #29.

- **2c-ii — Group I Character Anchor Block + G17 Two-Tool Refinement Pipeline** in `skills/higgsfield-soul/SKILL.md`. Six insertions per LOCK 5 + LOCK 18: NEW H2 § Character Anchor Block (P157 10-attribute per-shot prompt structure) + 3 NEW H3 sub-sections (Multi-Form State Tracking via P17+P129 / Face-from-Wide-Shot Workaround via P127 / Tricky-Prop Sheets via P128) + P19 embedded prop sheets sub-bullet in existing § Character Sheet Creation; NEW H2 § Two-Tool Refinement Pipeline (G17 Soul Cinema → GPT Image 2 pipeline; ~600 + ~200 = ~800 generations Jack-character anchor citation). **First v3.7.7 sub-phase to hold LOCK 1 estimate without tightening** (135 lines actual, 96% of LOCK 1 upper bound 140). **FI7 framework innovation candidate** logged (content-map per-item baselines beat abstract sub-phase estimates). +135 lines in PR #30.

### CH-3 — Templates library bootstrap (7 NEW files, sub-phase 2d)

Two new sub-directories with seven new template files. Heaviest sub-phase by file count.

- `templates/seedance/top-down-map.md` (NF3, G23 Hack 17) — Claude meta-prompt template for top-down spatial map pre-visualization. With LOCK 15 BAD/GOOD/GREAT inline examples.
- `templates/seedance/multi-character-anchor.md` (NF4, G24) — Paste-ready Seedance multi-character anchor block template. With LOCK 15 BAD/GOOD/GREAT inline examples.
- `templates/seedance/single-character-position.md` (NF5, G25) — Simpler companion for single-character shots.
- `templates/seedance/worked-example-two-character.md` (NF6, G26) — Concrete end-to-end NF4 fill with Roco + Lulu neo-noir alley scene.
- `templates/text-overlays/slogan.md` (NF7, P153a) — Display text + entrance animation template.
- `templates/text-overlays/subtitle.md` (NF8, P153b) — Dialogue-synchronized subtitles.
- `templates/text-overlays/speech-bubble.md` (NF9, P153c) — Character-attributed in-frame dialogue.

Root SKILL.md cross-link infrastructure updated with 3 new tables (technique templates + text-overlay templates + new sub-directory rows in § Shared Resources).

**Catch #14 instance #3** documented (per-file usable-template floor overrun: 465 → 457 lines after Decision B tightening per Path B approval; FI7-adjusted projection 335-340 vs LOCK 1 estimate 255-275). **FI7-A framework innovation candidate** logged (Gate 1 structural-assumption verification required — verified existing templates have no frontmatter; LOCK 9 cascade count reduced from 12-19 range to fixed 12). **FI7-B framework innovation candidate** logged (per-file usable-template structural floor ~40-50 lines minimum independent of template body size).

+457 lines (444 template files + 21 root SKILL.md updates − 8 padding cuts) in PR #31.

### CH-4 — image-models + MODELS-DEEP-REFERENCE expansion (sub-phase 2e)

Rule-extending into existing image-models.md + MODELS-DEEP-REFERENCE.md files. G18 Nano Banana Pro production-team observations sub-section appended to existing § Nano Banana Pro "Known limitations (official)": Plasticky-texture failure mode + counter (atmospheric haze closing line) — P35; Spatial-awareness limit + counter (text-only location, not image reference) — P33; 4-view default + counter (explicit "one view image") — P34; Multi-image embedded prompt drift + counter (generate individually + Photoshop composite) — P43. Group H location-handling sub-section: every-location-needs-anchor (P122) / never-front-on (P123) / split-into-views not combine (P124). Workflow positioning paragraph cross-refs to 2c-ii § Two-Tool Refinement Pipeline. MODELS-DEEP-REFERENCE.md NBP entry gets 1-line failure-modes cross-ref. Quick Decision Table updated (GPT Image 1.5 → GPT Image 2 v3.7.6 carry-over per content-map line 46; new row for Soul Cinema → GPT Image 2 Two-Tool Refinement Pipeline routing).

Also bundled `chore:` markdownlint MD040 fix for two 2d template body code blocks (Path i precedent from 2d→2e cleanup).

**First v3.7.7 sub-phase to land significantly under LOCK 1 lower bound** (24 lines actual vs 50-70 LOCK 1 — 34%; FI5/FI7-adjusted 70-100, 24% of upper). **FI5-C framework innovation candidate** logged (anchor-reuse percentage inversely correlates with scope overrun — slotting into existing section anchors needs less orientation budget than new section creation).

+24 net lines (21 image-models + 3 MODELS-DEEP-REFERENCE + 2 chore lint fix) in PR #32.

### CH-2 cross-cutting + CH-5 prep — vocab.md consolidation + camera + prompt extensions (sub-phase 2f)

13 vocab.md entries shipped (Path C-tightened resolving **Catch #14 instance #4** — planning-doc drift between LOCK 14 list and 2f kickoff list, silent substitution mechanism documented per FI8 discipline). 5 entries slot into existing sections (P107 scene-physics lighting in § Lighting Vocabulary / P119 60/30/10 color rule in § Color Grade Language new sub-header / P55 L-cut audio bridge extends existing § Cut & Continuity entry / P57 camera-relative-to-previous-shot in § Cut & Continuity / Reference roles @Image1/@Image2 convention in § Image Reference Notations). 8 entries across 4 NEW H2/H3 sections (§ Editing Syntax under § Camera Movement: P140 bracket notation + P141 arrow notation; § Composition Vocabulary new H2: P161 negative space + P162 crossing rule + Coordinate notation; § Motion Hierarchy under § Camera Movement: P160 4-layer motion hierarchy; § Production Vocabulary new H2: P129 script supervising + State lock). All 6 forward-declared cross-refs from 2d templates RESOLVE at this PR (bracket / arrow / crossing rule / coordinate / reference roles / state lock).

Camera SKILL.md extensions: P64 sequenced camera moves + P65 static-pan-vs-glide distinction in § Combining Camera Controls; P98/P99 pull-back-from-emotional-moment row in § Camera-Emotion Sync table.

Prompt SKILL.md extensions: Group A layered emotion states sub-section in § Generic-Emotion Decomposition (P67 + P96 consolidated as "anxious determination" / "tired tenderness" / "bitter amusement" + tiny-detail layering); Group E prompt-window hygiene sub-section in § Iteration Rule (P46 delete-obsolete + P70 editor-adds-atop-existing + P91 stale-reference-image + P117 prompt-overload-sanitize-pass).

**FI8 framework innovation candidate** logged (Phase 2 directives that supersede Phase 1c locks must explicitly acknowledge the supersession; silent substitution constitutes Catch #14 surface). Deferred to v3.7.8+: modality routing vocab entry + compound camera moves vocab entry (both already routed via image-models.md + skills/higgsfield-camera/SKILL.md respectively; vocab.md reinforcement optional).

+123 lines (56 vocab.md + 5 camera + 62 prompt) in PR #33.

### CH-5 — DISCIPLINE.md cross-cutting expansion (sub-phase 2g)

Most procedure-locked sub-phase: LOCK 4 verbatim paste + LOCK 10 no-redraft + LOCK 12 7-pattern specification all held character-by-character. DISCIPLINE.md expanded 126 → 246 lines (+120 net).

LOCK 4 Replacement #1 (intro replace) pasted verbatim from discovery ledger Section 11 — two paragraphs naming the author-bundle systematization framing + 5-skills-15-people-14-days-Cannes production anchor.

LOCK 4 Replacement #2 added as NEW H2 § Author-bundle systematization finding between patterns and § Source attribution. **Minor interpretive note** logged for documentation: LOCK 4 spec said "Replaces current Convergent-evolution finding section" but current DISCIPLINE.md has no such section (Phase 1c-era version likely had it); applied LOCK 10 spirit by adding the locked language as additive H2 in functionally-equivalent location. Not Catch #14 #5 — interpretive resolution within LOCK 10 spirit.

7 new patterns per LOCK 12 distributed across existing 3 tiers (3 Tier 1 + 3 Tier 2 + 1 Tier 3):

- Tier 1 (+3): Iteration-is-craft / Lock-before-generate / Falsifiable Success Criteria
- Tier 2 (+3): BAD/GOOD/GREAT (per LOCK 15 — cites 2d NF3+NF4 templates) / Skill-with-baked-context / Anti-Bombast + SC2 Anti-Bombast Paradox H4 sub-section
- Tier 3 (+1): Pre-Delivery Discipline (cites 2c-i FAILURE-MODES.md § Self-repair before delivery)

All 8 cross-ref targets RESOLVE: 2a / 2b-i / 2b-ii / 2c-i / 2c-ii / 2d (NF3+NF4) / 2e / 2f. **R6 risk (aspirational content / cross-ref resolution) fully mitigated across v3.7.7 Phase 2.**

**FI7-B-revised framework innovation candidate** logged (per-file structural floor varies by file convention, not just file type — FAILURE-MODES.md catalog convention 4-field ~24 lines/entry vs DISCIPLINE.md pattern convention 3-field ~11 lines/entry; Gate 1 must read target file's existing patterns before applying FI7-B forward-estimation).

+120 net lines in PR #34.

### Framework innovations (FI5 → FI9, 9 total — FI5-C as unifying mechanism)

v3.7.7 execution surfaced nine framework innovations across the FI5-FI9 family. Per the 8-sub-phase data pattern, FI5-C (anchor-reuse correlation) is the underlying mechanism that FI5 / FI6 / FI7-B / FI7-B-revised express as surface manifestations within specific content-type contexts. FI7 + FI7-A are methodological. FI8 is content-planning. FI9 (NEW at 2h) is cumulative-scope discipline.

| FI | Source | Insight |
|---|---|---|
| **FI5-C** (primary) | 2e (24% LOCK) — confirmed across 8 sub-phases | Anchor-reuse percentage inversely correlates with scope overrun |
| FI7 (methodological) | 2c-ii (96% LOCK) | Content-map per-item baselines beat abstract sub-phase estimates |
| FI7-A (methodological) | 2d Gate 1 | Gate 1 must verify structural assumptions before per-item math is trusted |
| FI8 (content-planning) | 2f Gate 1 | Phase 2 directives that supersede Phase 1c locks must explicitly acknowledge supersession |
| **FI9 (NEW)** | 2h kickoff acknowledgment | Cumulative scope discipline requires periodic check against project-level locks during Phase 2 execution, not just per-sub-phase locks at Gate 4 |
| FI5 (case study) | 2b-i + 2b-ii | Vocabulary-introducing sub-phases need more orientation budget than rule-extending |
| FI6 (case study) | 2c-i | Catalog-format sub-phases have higher structural floor than rule-extension or vocabulary-intro |
| FI7-B (case study) | 2d | Per-file usable-template structural floor |
| FI7-B-revised (refinement) | 2g | Per-file structural floor varies by file convention, not just file type |

Anchor-reuse correlation across 8 sub-phases:

| Sub-phase | LOCK actual | Anchor reuse |
|---|---|---|
| 2b-i | 200% | New sections |
| 2d | 166% | All new files (7) |
| 2c-i | 133% | New file (FAILURE-MODES.md) |
| 2b-ii | 129% | Existing taxonomy extension |
| 2c-ii | 96% | Mostly existing + 1 NEW H2 |
| 2f | 95% | Mixed: 5 existing + 8 new across 4 sections |
| 2g | 67% | All 7 patterns under existing Tier H2s |
| 2e | 34% | All existing anchors |

### Catch #14 instances (6 distinct mechanisms — framework operating as designed)

Six Catch #14 instances surfaced across v3.7.7 Phase 2. Same catch class (planning-doc drift), six distinct mechanisms. Each instance surfaced at the appropriate Gate, handled per Decision A/B/C protocol where applicable, documented forward. Framework operating correctly produces catches; catches are forward learning, not retroactive failures.

| # | Sub-phase | Mechanism | Resolution |
|---|---|---|---|
| #1 | 2b-i | Vocabulary-introducing orientation budget overrun | Decision B retroactive tightening (159 → 130) |
| #2 | 2c-i | Catalog-format structural floor overrun | Decision A-tightened (312 → 293 with Path B approval) |
| #3 | 2d | Per-file usable-template floor overrun | Path B + Decision B preemptive tightening (465 → 457) |
| #4 | 2f Gate 1 | Silent substitution (Phase 2 directive vs Phase 1c lock) | Path C-tightened (13 entries union of both lists) |
| #5 | (cumulative 2a-2g) | LOCK 3 cumulative scope drift | Acknowledged at 2h kickoff; FI9 logged |
| #6 | 2h Gate 1 | Cascade-scope misalignment (LOCK 9 vs verified 8-file list) | Reconciled per Decision 2 (surface + document) |

### Backlog deferred to v3.7.8+

- **G1 Soul Cinema two-step compositing** — UI testing remains pending (carried over from v3.7.5; narrowed at v3.7.7 per discovery findings)
- **G13 Seedance `【镜头N】` syntax** — Seedance product-team confirmation pending (carried over from v3.7.5)
- **Modality routing vocab entry** — already routed via image-models.md + MODELS-DEEP-REFERENCE.md; vocab.md reinforcement optional
- **Compound camera moves vocab entry** — already covered in `skills/higgsfield-camera/SKILL.md` § Combining Camera Controls (P64 paragraph); vocab.md reinforcement optional
- **LOCK 4 Replacement #2 interpretive note** — Convergent-evolution section absent on current main; resolved per LOCK 10 spirit at 2g (additive placement); planning-doc currency observation only
- **LOCK 9 DISCIPLINE.md frontmatter item** — reconciled at 2h Gate 1 per Option (b) — DISCIPLINE.md retains existing root-level no-frontmatter convention
- **Table-style harmonization decision** (MD060 across ~50+ repo tables) — repo-wide style decision deferred; apply uniform markdownlint style OR add config disable OR leave as known stylistic preference

### Changed

- **Frontmatter version bumps (8 files, mixed minor + patch)** — root `SKILL.md` 3.7.6 → 3.7.7; `skills/higgsfield-seedance/SKILL.md` 1.5.0 → 1.6.0; `skills/higgsfield-seedance/FAILURE-MODES.md` 1.0.0 (new file, no bump); `skills/higgsfield-prompt/SKILL.md` 3.3.0 → 3.4.0; `skills/higgsfield-soul/SKILL.md` 3.3.0 → 3.4.0; `skills/higgsfield-camera/SKILL.md` 3.2.0 → 3.3.0; `skills/higgsfield-models/MODELS-DEEP-REFERENCE.md` 3.0.0 → 3.1.0; `skills/higgsfield-models/SKILL.md` 3.1.0 → 3.1.1 (patch — cross-link only). All `updated:` dates → 2026-05-18. `DISCIPLINE.md` / `vocab.md` / `production-benchmarks.md` / `image-models.md` retain root-level no-frontmatter convention. **R1 cascade mitigation per Phase 1c: single-file Edit + `python3 validate.py` per file** (not bulk Write per v3.7.5 catch #11 lesson). 8 ops vs LOCK 9's estimated 12 — see Catch #14 #6 above.

- **`USER-GUIDE.pdf` regenerated** — content-equivalent to v3.7.6 baseline (Layer 1 text-extract diff PASS with version/date pattern normalization) but byte-divergent at 29030 byte positions (parameterized version + /CreationDate metadata cascade through deflate compression). None of v3.7.7's net-new surfaces propagate into USER-GUIDE.pdf because `generate_user_guide.py` content sections are hardcoded — same constraint as v3.7.6. USER-GUIDE.pdf modernization remains the deferred dedicated arc.

- **`validate_user_guide.py` DEFAULT_BASELINE re-pointed** — `USER-GUIDE.pdf.baseline-v3.7.6` → `USER-GUIDE.pdf.baseline-v3.7.7`. New baseline `USER-GUIDE.pdf.baseline-v3.7.7` committed alongside this release (baselines accumulate, not rotate — v3.7.0 through v3.7.7 all retained for historical comparison).

- **Markdownlint repo hygiene (Path i-bundle-2h queue partial)** — 10 MD040 fenced-code-language fixes in `MODELS-DEEP-REFERENCE.md` (added `text` language hint to bare opening fences containing template/example prose); 1 MD058 blanks-around-tables fix in `vocab.md` (added blank line between `### Color Grade Language` H3 and immediately-following table). MD060 table-column-style warnings (~9 across vocab.md + MODELS-DEEP-REFERENCE.md + image-models.md) deferred per table-style harmonization decision — out of 2h scope (would require repo-wide reformatting of ~50+ tables).

- **`feedback_release_workflow.md` updated** — appended v3.7.7 execution facts: 9 framework innovations (FI5-FI9 family) + 6 Catch #14 instances with mechanisms + Decision B precedent (5 applied + 4 NOT-NEEDED) + forward operating rules for v3.7.8+ (FI5-C + FI7-A + FI8 + FI9 applied preemptively at Gate 1).

- **`backlog_audit_findings.md` updated** — v3.7.7 ship status recorded across all 9 sub-phases; v3.7.8+ deferred items expanded with full rationale per Path C-tightened + Decision 1 (Option b) decisions; framework-innovations + Catch #14-instances queue appended for forward reference.

### Sourcing

- **v3.7.7+ audit corpus** — Higgsfield-team-adjacent author bundle (banana-pro-director, cinema-worldbuilder, screenwriter-skill, shotlist-builder, seedance-2-pro-director) used inside Higgsfield production team's actual pipeline. Patterns proved out during the 2026 Cannes production cycle — five skills, fifteen people, fourteen days, one 90-minute AI feature shipped for Cannes. Source corpus: 3h 47m SRT (3 episodes of "Road to Cannes") + 16 Hack screenshot slides + 604-line seedance-2-pro-director skill body. Total: 358 items extracted across 40 topics; 22 discoveries surfaced; 11 G-candidates; ~150 P-candidates; 5 SC items.

- **IP discipline:** Pattern *form* + *discipline names* + cross-references = audit contribution (IP-safe per pattern-not-text classification). Specific authored content (template bodies, P153 text overlays, prompt formulas) stays at source; what higgsfield ships is re-documented in higgsfield voice with paraphrase per threshold rule (short fragments under 3-9 words quoted verbatim if load-bearing factual; everything else paraphrased). Verified across 9 sub-phases — zero verbatim-quote failures.

- **DISCIPLINE.md SC1 reframe** — LOCK 4 Replacement #1 + Replacement #2 verbatim language pre-locked from `/tmp/higgsfield-audit-v3.7.7-discovery/07-discovery-triage-ledger.md` Section 11 per Phase 1c Rx-4 (HIGH-severity risk) mitigation. Character-by-character paste verified at 2g Gate 4; LOCK 10 no-redraft discipline held.

- **Cross-corpus continuity** — Adil explicitly names screenwriter-skill at Ep. 1 SRT 623-627 and shotlist-builder at Ep. 2 SRT 391-395 (both are v3.7.5 audit subjects, confirming Higgsfield team uses v3.7.5 audit corpus skills inside their pipeline). Seedance-2-pro-director skill frontmatter explicitly defers multi-scene work to shotlist-builder. Stage 3 skill body verbatim-matches Adil's Ep. 3 Hack 3 description of the system-prompt-skill, confirming same author bundle. Cross-episode bidirectional callbacks (Ep. 2 → Ep. 1 P15 iteration-is-craft; Ep. 3 Hack 26 → Ep. 2 P80+P81 FPS-drift). Single-author-bundle systematization framing supersedes v3.7.5's "independent authors converging" framing.

### Cumulative scope acknowledgment

LOCK 3 ceiling was 1005-1335 lines (v3.7.7 scope estimate at Phase 1c). Actual cumulative content shipped: **1534 lines net** across 9 content sub-phases (15% above LOCK 3 upper bound). Each sub-phase honored its individual LOCK 1 estimate with Decision B tightening where needed and Path A/B/C surfacing where the 1.25× threshold was crossed — no defensive shipping at any sub-phase. The Catch #14 #5 (cumulative drift) is the absence of a cumulative scope check across sub-phases, not a failure of per-sub-phase discipline. **FI9 logged** for v3.7.8+ forward operational application: cumulative scope check at each 25% sub-phase milestone (not just per-sub-phase Gate 4 check).

## v3.7.6 — 2026-05-17

Mega-release. Co-headlined: C-arc (Building Complete AI Projects 10-Step Methodology) + G2 (GPT Image 2 flagship integration) + DISCIPLINE.md (cross-cutting discipline patterns meta-arc) + v3.7.5-audit-gap closeout (9 gaps shipped; 2 dropped; 2 deferred). Largest release in repo history by line count and surface count. Second exception to harder-single-arc commitment after v3.7.5 backlog closeout — co-headlined by explicit Peter decision at Phase 1 planning stage, not single-arc by accident.

### Building Complete AI Projects — The 10-Step Methodology (Steps 01-05)

New H2 `## Building Complete AI Projects — The 10-Step Methodology` in `skills/higgsfield-pipeline/SKILL.md`, placed between § The Core Insight and § The Master Production Chain. Five H3 sub-sections for Steps 01-05:

- **Step 01 — Start With the Project, Not the Prompt** — 9-field project basics list (Project type / Main subject / Visual style / Scene goal / Audience / Mood / Length / Setting / What must stay consistent) verbatim
- **Step 02 — Build a Master Script** — 9-item contents list verbatim + disambiguation blockquote per v3.7.5 § Post-Clip Decisions precedent ("Master Script" = structured project document, not Hollywood screenplay; source quote "it does not have to be a Hollywood screenplay; it just needs to explain the full idea clearly" shipped verbatim)
- **Step 03 — Use GPT as Your Creative Assistant** — 5 named GPT tile roles verbatim (Concept Builder / Script Writer / Shot List Planner / Prompt Refiner / Problem Solver) + GPT-in-stages framing + cross-link to `higgsfield-assist` for in-platform GPT-5 copilot alternative
- **Step 04 — Separate the Script From the Prompt** — 4 production-instruction categories verbatim (Camera Notes / Lighting Direction / Subject Movement / Environment Detail) + cross-link to `higgsfield-prompt` and `higgsfield-soul` § Identity vs Motion Separation as different-axis separation rule
- **Step 05 — Create a Project Bible** — 11-item lock-in list verbatim (Character appearance / Wardrobe / Hair / Color palette / Location / Lighting style / Camera style / Tone / Props / Negative rules / Continuity rules) + 3 rules of thumb verbatim + forward cross-link to `higgsfield-soul` § Character Sheet Creation and `higgsfield-cinema` § Elements System as downstream realizations of the upstream Bible artifact

+198 lines in PR #18.

### Building Complete AI Projects — The 10-Step Methodology (Steps 06-10 + Simple Workflow)

Continuation of the new H2 from 2a. Six new H3 sub-sections completing the 10-step methodology:

- **Step 06 — Give Every Scene One Job** — 6 scene purposes verbatim (Introduce the character / Show the location / Build tension / Reveal the product / Create emotion / Deliver the action — union-deduped across deck visual + bullet list + prose surfaces per cleaner-phrasing-wins precedent) + 6-question scene-prompt checklist verbatim + cross-link to `higgsfield-prompt` § One Action Per Scene as different unit of decomposition
- **Step 07 — Use Prompt Modules** — 7-module prose taxonomy verbatim (Character identity / Camera / Lighting / Style / Motion / Negative prompt / Continuity blocks) + worked camera-block example verbatim + cross-link with alias note to `higgsfield-soul` / `higgsfield-prompt` Identity-Motion blocks (finer-grained sibling framing — Identity Block ≡ Character identity block)
- **Step 08+09 — Fix Failures + Protect What Worked** — consolidated section per Phase 1b resolution (Iteration Rule + 6-Pass Diagnostic in `higgsfield-prompt` provides full discipline; 2b ships compact section naming the three rhetorical handles: "make it better" anti-pattern, 80% rule, "every failure should become a new rule" framing)
- **Step 10 — Build the Project in Passes** — 8 named passes verbatim (Concept / Project script / Scene breakdown / Shot list / Image prompts / Video prompts / Review results / Fix and finalize) + cross-link forward to § Master Production Chain + § Pipeline Decision Guide
- **Simple Workflow — Execution Recipe** — 10 imperative steps verbatim from both sources + cross-link at step 7 ("Generate inside Higgsfield") to § Pipeline Decision Guide for chain choice
- **Build With Purpose** — closing prose verbatim, paragraph form ("The power is not in one perfect prompt. The power is in the workflow.")

+155 lines in PR #19.

### Seedance audio + runtime + density coverage

Three audit-gap closeouts (G4 + G6 + G12) — Seedance-side discipline content across `higgsfield-audio` and `higgsfield-seedance`. All three are independent-re-document gaps from v3.7.5 Joey-bundle / shotlist-bundle audit; no source-verbatim items.

- **G4 — Diegetic-only audio convention for Seedance prompt body** in `skills/higgsfield-audio/SKILL.md` § Seedance 2.0 — callout distinguishes "BGM is a valid audio LAYER (model capability)" from "diegetic-only is a prompt-body authoring DISCIPLINE" with cross-link to existing § The Four Audio Layers. Two reasons the discipline matters even when BGM is supported (score descriptors underdetermine generation; timestamp-anchoring + remove-all-music-tokens pattern generalized to all Seedance prompts).
- **G6 — Runtime arithmetic discipline for multi-shot Seedance prompts** in `skills/higgsfield-seedance/SKILL.md` § Output Format — new H3 documenting triple-redundant runtime (title + meta header + per-shot timing labels) with arithmetic-must-equal-total rule and "always ask user for runtime, never default" hard rule.
- **G12 — Shot density heuristic for multi-scene Seedance prompts** in `skills/higgsfield-seedance/SKILL.md` § Output Format — new H3 documenting "~1 prompt per 4-5 shot rows" project-derived empirical starting heuristic, 5 group-rows conditions, 3 split-row triggers, plus explicit derivation caveat ("project-derived empirical observation, not platform-enforced").

+68 lines in PR #20 (+22 audio, +46 seedance).

### Prompt + Camera output rules + emotion discipline

Three audit-gap closeouts (G7 + G9 + G10) — prompt-authoring discipline across `higgsfield-prompt` and `higgsfield-camera`. Four Edit operations (G9 ships with paired cross-link callout in `higgsfield-prompt` § Identity vs Motion).

- **G7 — No-aspect-ratio-in-prompt-body universal rule** in `skills/higgsfield-prompt/SKILL.md` § Common Prompt Mistakes — new table row codifying the existing pattern (aspect ratio belongs in the UI / output-format header, not in the prompt body; describe framing in plain language like "full body" / "chest-up" / "wide establishing" not numerical ratios).
- **G9 — Camera-Emotion Sync hard rule** in `skills/higgsfield-camera/SKILL.md` — new H2 § Camera-Emotion Sync — Movement per Focal Character Emotion placed after § Combining Camera Controls. 6-emotion movement-to-camera-prescription map (Anger / Calm / Sadness / Shock / Action / Final beat) + § Emotional arcs within a single shot H3 (opening / transition / closing phase pattern) + back-cross-link to G10 for emotion-naming discipline. Mapping pairs are real-world cinematography practice re-documented in higgsfield voice.
- **G10 — Generic-Emotion Decomposition + "which kind of X?" template** in `skills/higgsfield-prompt/SKILL.md` — new H2 (not H3 per Phase 1c spec; see catch #14 instance 4 below). "Never leave a generic emotion in a prompt" rule + decompose-by-muscle / breath / eyes / skin pattern + worked "which kind of surprise?" 4-variant clarification template (Light positive / Shock / Disbelief / Surprise-with-joy) + cross-link to `higgsfield-soul` § Micro-Expressions for preset library alternative.
- **G9 paired cross-link callout** in `skills/higgsfield-prompt/SKILL.md` § Identity vs Motion Separation Rule — forward link to G9 ("the *quality* of camera motion tracks emotion") + back-link to G10.

Bidirectional cross-link chain established: `higgsfield-prompt` § Generic-Emotion Decomposition ↔ `higgsfield-camera` § Camera-Emotion Sync ↔ `higgsfield-prompt` § Identity vs Motion ↔ `higgsfield-soul` § Micro-Expressions.

+95 lines in PR #21 (+50 prompt, +45 camera).

### Soul character sheet single-prompt + Pipeline spatial blocking

Two audit-gap closeouts (G3 + G11) — Soul + Pipeline discipline. Two Edit operations across two files.

- **G3 — Single-prompt 6-panel character sheet (3×2 grid)** in `skills/higgsfield-soul/SKILL.md` — new H3 under existing § Character Sheet Creation. Alternative to multi-step assembly: one prompt → one 16:9 image → 3×2 grid with 6 labeled panels (Front body / 3/4 turn / Back body / Waist-up portrait / Hands detail close-up / Face detail close-up). Identity-locking rationale: single-pass generation prevents panel-to-panel drift.
- **G11 — Top-down spatial-blocking schema for multi-character scenes** in `skills/higgsfield-pipeline/SKILL.md` — new H2 § Spatial Blocking — Top-Down Schema for Multi-Character Scenes between § Working Practices and § Pipeline Decision Guide. 3 when-to-draw triggers verbatim (2+ characters / key prop on specific surface / complex camera geometry) + 6 what-goes-on-schema items verbatim (room outline / character positions / eyelines / props / distances / surface labels) + ASCII top-down schema example (R8 mitigation: runtime-portable, no `visualize:show_widget` claude.ai-runtime dependency) + absolute-spatial-declaration translation rule + cross-link forward to `higgsfield-seedance` § Output Format for Static Description slot integration.

+97 lines in PR #22 (+37 soul, +60 pipeline).

### GPT Image 2 — flagship integration

Adds GPT Image 2 to two surfaces — `image-models.md` catalog entry and `skills/higgsfield-models/MODELS-DEEP-REFERENCE.md` deep-reference entry. Closes the documentation gap identified at v3.7.5 audit (GPT Image 2 was previously only mentioned in passing at `higgsfield-cinema/SKILL.md:1804` as a Featured model with no dedicated entry; existing line 1804 mention now resolves to real destination).

14 strict-verbatim factual items shipped per Phase 2d spec: model ID `gpt-image-2`, snapshot `gpt-image-2-2026-04-21`, released April 21, 2026, knowledge cutoff December 2025, pricing $8 / $2 / $30 per 1M tokens (input / cached / output), rate limits Tier 1 5 IPM → Tier 5 250 IPM, 4 endpoints (`v1/images/generations`, `v1/images/edits`, `v1/responses`, `v1/chat/completions`), 4 not-supported features (streaming, function calling, structured outputs, fine-tuning), Higgsfield URL `higgsfield.ai/ai/image?model=imagegen_2_0`, internal slug `imagegen_2_0`, native 4K resolution (up from 1536×1024), up to 16 reference images, multilingual text rendering >95% accuracy, scripts list (Japanese / Korean / Chinese / Hindi / Bengali). Comparative prose (vs GPT Image 1.5 / Nano Banana Pro / Seedream 4.5) paraphrased per IP-safe re-document discipline.

+55 lines in PR #23 (+15 catalog, +40 deep-reference).

### DISCIPLINE.md — cross-cutting discipline patterns

New `DISCIPLINE.md` at repo root indexing 9 cross-cutting discipline patterns in 3-3-3 tier symmetry. Plus 1-line `validate.py` registration update so the new file is enforced by the validator going forward.

3-3-3 tier breakdown:

- **Tier 1 — Workflow Discipline:** Pre-Prompt Confirmation Gate (with P10 "one question over many" folded inline) / Explicit-Stop Between Phases / Inventory-Extraction Checklist Before Composing
- **Tier 2 — Output Discipline:** Visual-Marker-Only Output Discipline / Triple-Redundant Runtime / Single-Variable Iteration
- **Tier 3 — Architectural Discipline:** 3-Stage Chain / 4-Phase Loop Architectural Pattern / Closing-Block-Baked-Into-Every-Prompt / Strict-Order Workflow with Refusal-to-Skip Phases

Each pattern lists a concrete demonstration in the existing higgsfield codebase with file-and-section pointer (R6 mitigation: no aspirational content; all 9 cross-references verified resolving to real content at Gate 1 of sub-phase 2e). Two patterns use honest "weaker" framing rather than aspirational literal-source language: **P2 (Explicit-Stop Between Phases)** cites `higgsfield-pipeline` § Pipelines A-E artifact-handoff structure + Pipeline Pitfall 1 ("Never animate a 'good enough' image" — explicit don't-skip-ahead rule); **P8 (Closing-Block-Baked-Into-Every-Prompt)** cites root SKILL.md § MANDATORY WORKFLOW step 4 + `skills/shared/negative-constraints.md` as the single-source closing block applied across every higgsfield prompt. Both verified accurate by Peter at PR #24 review.

Tightening pass applied per review directive: 194 lines → 126 lines (-68, -35%). Cuts: folded "How to apply" H2 into "What this is" intro; compressed pattern descriptions from 2-3 sentence multi-line to 1-sentence single-line; tightened "Demonstrated in" cross-refs; compressed Source attribution. Preserved: 9 patterns, 3-3-3 tier symmetry, all 9 cross-references, P2/P8 honest framing, v3.7.5 audit attribution.

+126 lines new file + 4-line `validate.py` registration update in PR #24.

### Changed

- **Frontmatter version bumps (8 files + root + new file)** — root `SKILL.md` 3.7.5 → 3.7.6 / updated 2026-05-16 → 2026-05-17; `skills/higgsfield-pipeline/SKILL.md` 3.2.0 → 3.3.0 (minor bump for new H2 § Building Complete AI Projects + new H2 § Spatial Blocking); `skills/higgsfield-soul/SKILL.md` 3.2.0 → 3.3.0 (minor bump for new H3 § Single-prompt 6-panel character sheet); `skills/higgsfield-audio/SKILL.md` 3.0.0 → 3.1.0 (minor bump for G4 diegetic-audio addendum); `skills/higgsfield-seedance/SKILL.md` 1.4.0 → 1.5.0 (minor bump for G6 + G12 H3s); `skills/higgsfield-prompt/SKILL.md` 3.2.0 → 3.3.0 (minor bump for G7 mistake row + G10 H2 + G9 cross-link callout); `skills/higgsfield-camera/SKILL.md` 3.1.0 → 3.2.0 (minor bump for G9 H2); `skills/higgsfield-models/SKILL.md` 3.0.2 → 3.1.0 (minor bump for G2 MODELS-DEEP-REFERENCE entry). All `updated:` dates → 2026-05-17. New `DISCIPLINE.md` ships at initial 1.0.0 (not a bump; new-file value). `image-models.md` has no frontmatter, no bump applicable. **Largest frontmatter cascade in repo history (v3.7.5 was 2 sub-skills + root; v3.7.6 is 7 sub-skills + root + new file).** R1 cascade mitigation per Phase 1c: bumps applied one-Edit-at-a-time with `python3 validate.py` after each, no bulk Write per v3.7.5 catch #11 (markdown-fence-nesting failure) lesson.

- **`validate_user_guide.py` DEFAULT_BASELINE re-pointed** — `USER-GUIDE.pdf.baseline-v3.7.5` → `USER-GUIDE.pdf.baseline-v3.7.6` per v3.7.5 line 27 baseline-management discipline. New v3.7.6 baseline committed to git alongside this release (baselines accumulate, not rotate; v3.7.0 through v3.7.6 baselines all retained for historical comparison).

- **`USER-GUIDE.pdf` regenerated** — content-equivalent to v3.7.5 baseline (Layer 1 text-extract diff PASS with version/date pattern normalization) but byte-divergent at 32055 byte positions (~95% of file) — deflate compression cascades the parameterized input deltas (version string v3.7.5 → v3.7.6, updated date 2026-05-16 → 2026-05-17, /CreationDate metadata) through the entire compressed object stream. **None of the v3.7.6 net-new surfaces (C-arc methodology, G2 GPT Image 2, audit-gap closeouts, DISCIPLINE.md) propagate into USER-GUIDE.pdf** because `generate_user_guide.py` content sections are hardcoded — see Drift catalog status below. USER-GUIDE.pdf modernization remains the deferred dedicated arc per v3.7.5 v3.7.6+ candidates list.

- **`validate.py` updated** — `DISCIPLINE.md` added to `expected_root_files` list (line 134-140). Single-line registration ensures the new root-level doc is enforced by the validator going forward. Structural-integrity addition; Phase 1c spec did not list `validate.py` update but DISCIPLINE.md without validator registration would be inconsistent with the rest of root-doc enforcement pattern. Same class as catch #14 (structure wins over Phase 1c spec).

### Sourcing

- **C-arc source (Phase 1a triage)** — Higgsfield Discord, May 2026 — *Building Complete AI Projects: From Script to System* 14-page Canva slide deck + *How To Work With Scripts and GPTs to Build a Complete Project* (`How To 2.pdf`) 11-page Apple Pages prose companion. Both files in LEARNING HUB consolidated audit corpus. Cleaner-phrasing-wins precedent applied per v3.7.4 §5 / v3.7.5 §3 where the two sources diverge: prose canonical for body text (richer fields including "Hair" as separate Project Bible item + "Motion block" split from Negative/Continuity in Prompt Modules + "Deliver the action" as 6th scene purpose + "does not have to be a Hollywood screenplay" disclaimer + 80% rule + GPT-in-stages framing); deck canonical for visual / structural taxonomies (5-tile GPT roles + 4 production-instruction labels + 5 scene-purpose cards). 10-step numbering, step titles, and structural conclusions identical between sources — differences are expansion-density only.

- **C-arc methodology lineage** — no external citations in source (unlike v3.7.5 screenwriter-skill audit which cited McKee / Campbell / Aristotle). Higgsfield first-party reference is explicit at Simple Workflow step 7 ("Generate inside Higgsfield") and closing line ("Higgsfield brings the visuals to life"). Classification: Higgsfield-affiliated official-or-semi-official educational content. IP discipline: factual prescriptions (9-item Project basics, 9-item Master Script contents, 5 GPT tile names, 11-item Project Bible + 3 rules of thumb, 6 scene purposes + 6-question scene-prompt checklist, 7 prompt module names + worked camera-block example, 8 named passes, 10 Simple Workflow steps, 4 production-instruction categories, disambiguation blockquote language) shipped verbatim per audit's factual-prescription classification; all body prose paraphrased.

- **v3.7.5 audit findings closeout (Phase 1b resolution):**
  - **G2 GPT Image 2** — flagship integration, shipped this release (sub-phase 2d)
  - **G3 Single-prompt 6-panel character sheet** — shipped in `higgsfield-soul` § Character Sheet Creation (sub-phase 2c-iii)
  - **G4 Diegetic-only audio for Seedance** — shipped in `higgsfield-audio` § Seedance 2.0 (sub-phase 2c-i)
  - **G5 Scene-type-to-camera-grammar table** — **DROPPED** from v3.7.6 with backlog note. `higgsfield-prompt` § Scene Archetype Router (lines 416-453) already provides partial coverage via Action / General / Dialogue archetype maps. Reconsider only if richer scene-type taxonomy is warranted; current Router likely sufficient.
  - **G6 Runtime arithmetic discipline** — shipped in `higgsfield-seedance` § Output Format (sub-phase 2c-i)
  - **G7 No-aspect-ratio-in-prompt-body rule** — shipped in `higgsfield-prompt` § Common Prompt Mistakes (sub-phase 2c-ii)
  - **G8 Age-blind output rule** — **DROPPED** from v3.7.6 (already covered in `higgsfield-prompt` § Seedance 2.0 Engine Constraints → Age-blind character rule, lines 496-500). Phase 1b collision audit discovery — no work needed.
  - **G9 Camera-Emotion Sync hard rule** — shipped in `higgsfield-camera` § Camera-Emotion Sync (sub-phase 2c-ii)
  - **G10 Generic-Emotion Decomposition** — shipped in `higgsfield-prompt` § Generic-Emotion Decomposition (sub-phase 2c-ii)
  - **G11 Top-down spatial-blocking schema** — shipped in `higgsfield-pipeline` § Spatial Blocking (sub-phase 2c-iii)
  - **G12 15s-prompt density heuristic** — shipped in `higgsfield-seedance` § Output Format (sub-phase 2c-i)
  - **G1 Soul Cinema two-step compositing** — **DEFERRED** to v3.7.7+ pending Peter's hands-on Higgsfield UI testing
  - **G13 Multi-shot `【镜头N】` syntax** — **DEFERRED** to v3.7.7+ pending Seedance product-team confirmation of platform-native vs community convention

- **DISCIPLINE.md source (v3.7.5 audit pattern findings)** — 9 cross-cutting discipline patterns named from v3.7.5 ecosystem audit (Joey banana-pro-director + cinema-worldbuilder; screenwriter-skill; shotlist-builder). IP discipline: pattern *form* (structural shape + discipline name) is the audit contribution, IP-safe per pattern-not-text classification; pattern *demonstration* is higgsfield's own existing practice — file / section pointers are observed, not aspirational (R6 mitigation, verified at Gate 1 of sub-phase 2e).

### Deferred to future releases

- **G1 Soul Cinema two-step compositing flow** — Joey banana-pro-director Mode 1B (outfit-on-neutral-model Step 1B.1 → composite-onto-character Step 1B.2). Requires Peter's hands-on Higgsfield UI testing to verify the two-step flow works as documented before higgsfield ships re-documented guidance. Re-eligible for v3.7.7+ once UI testing completes.
- **G13 Multi-shot `【镜头N】` block syntax for Seedance prompts** — from shotlist-builder source. Requires Seedance product-team confirmation of whether `【镜头N】` is a Seedance-supported native convention or external community convention. If native: high-value documentation gap. If community: only worth a one-line reference, if anything. Re-eligible for v3.7.7+ once product-team confirmation arrives.

### Notes

- **Mega-release exception to harder-single-arc commitment.** v3.7.5 committed harder to single-arc discipline. v3.7.6 is the second exception after v3.7.5's own backlog closeout — co-headlined by explicit Peter decision at Phase 1 planning stage, not single-arc by accident. Rationale: closing the v3.7.5 audit-findings backlog + C-arc integration + DISCIPLINE.md cross-cutting work landed cleaner as a single co-headlined release than as a sequence of smaller releases. Future releases return to harder-single-arc discipline.

- **Catch #14 — planning-doc drift (new catch class, 6 instances).** New catch class opened this release. Cumulative numbering continues from v3.7.5 inheritance-pattern taxonomy which closed at #13. **Root cause:** Phase 1c specifications are estimates and structural placeholders, not authoritative on item counts, H-levels, scope line counts, or implementation step ordering. Phase 2 verifies against current file structure, source extracts, and tooling realities. Six instances surfaced across sub-phases:
  1. **Step 02 contents count** — Phase 1c said 8, source has 9 (Phase 2a discovery)
  2. **Step 05 Project Bible count** — Phase 1c said 10, source has 11 (Phase 2a discovery; Hair preserved as separate item per prose-canonical-for-body precedent)
  3. **Step 06 scene purposes count** — Phase 1c said 5, source has 6 (Phase 2b discovery; union-deduped across deck visual + bullet list + prose)
  4. **G10 H-level** — Phase 1c said H3 before § Identity vs. Motion, structural integrity requires H2 (H3 between two H2s would be orphaned per Markdown structure; Phase 2c-ii discovery)
  5. **DISCIPLINE.md scope** — Phase 1c estimated 50-80 lines, realized 194 then tightened to 126 (Phase 2e + tightening pass; trade-off accepted for demonstration-link specificity)
  6. **Phase 2f USER-GUIDE.pdf regen step ordering** — Phase 1c said regen before frontmatter bumps, but `generate_user_guide.py` reads version from root `SKILL.md` frontmatter as single source of truth; root frontmatter must bump first so regenerated PDF embeds v3.7.6 (Phase 2f discovery)

  **Mitigation discipline going forward:** when Phase 1c spec disagrees with source / structure / tooling reality, source / structure / tooling wins; document the disagreement as a catch class instance.

- **Frontmatter bump cascade scale.** 7 sub-skill files + root SKILL.md + new DISCIPLINE.md = 9 file frontmatters touched in single 2f batch. Largest cascade in repo history. R1 mitigation applied: single-file Edits with `python3 validate.py` after each, no bulk Write per v3.7.5 catch #11 (markdown-fence-nesting failure) lesson.

- **Drift catalog status update.** v3.7.6 net-new surfaces compound D-items 3-8 further per v3.7.5 line 75 precedent. New surfaces that don't propagate into USER-GUIDE.pdf because `generate_user_guide.py` content sections are hardcoded: C-arc 10-Step Methodology H2 (compounds D-item for pipeline overview), G2 GPT Image 2 catalog + deep-reference (compounds D-item for image-models section), G9 Camera-Emotion Sync H2 (compounds D-item for camera section), DISCIPLINE.md root doc (no current USER-GUIDE.pdf surface). D-item count unchanged at 6 (D3-D8); compound events increased substantially. USER-GUIDE.pdf modernization remains the deferred dedicated arc.

- **Future maintenance follow-ups (small-PR targets, not 2f scope):**
  - `MODELS-DEEP-REFERENCE.md` Quick Decision Table at line 1136 still routes "Photorealistic image with precise text/logo rendering" to GPT Image 1.5. With GPT Image 2 now documented as the premium-tier text-rendering option, this row would more accurately route to GPT Image 2. Single-row update; ship in future maintenance PR.
  - Pre-existing markdownlint warnings (MD060/table-column-style + MD040/fenced-code-language) in `image-models.md` line 363 and `MODELS-DEEP-REFERENCE.md` lines 60-307 surfaced by IDE re-scan during sub-phase 2d but not in 2d edit zones — additive-only release discipline. Address in future cleanup PR if desired.
  - DISCIPLINE.md scope review at 6 months: if patterns prove unused by new sub-skills, trim from 126 lines toward 100-line floor; if patterns drive new sub-skill design, keep or expand.

- **Phase 2 sub-phase shipping cadence.** 8 sub-phases shipped as 7 separate PRs before this release-ceremony PR (#18 / #19 / #20 / #21 / #22 / #23 / #24). Per-sub-phase merge cadence kept PR review surface manageable. Phase 1c estimated 8-13 sessions; actual landed near the lower bound. R1 / R6 / R8 risk mitigations all held; no Gate 4 self-audits surfaced regressions; one catch class (#14, six instances) opened across sub-phases.

Commit prefix: `feat: v3.7.6 — mega release: C-arc (Building Complete AI Projects 10-Step) + G2 (GPT Image 2 flagship) + DISCIPLINE.md + audit-gap closeout`

## v3.7.5 — 2026-05-16

### Added

- **`## Post-Clip Decisions` new H2 in `skills/higgsfield-seedance/SKILL.md`** (File 08 §3 four-question diagnostic + §12 Next-Shot Decision Tree, layer (e) from File 08 row 5 backlog) — placed adjacent to `## When the User Is Already in a Failure Loop` to form a paired post-generation cluster (post-clip diagnostic ↔ post-clip failure-handling). Two H3 sub-sections: `### The Four Questions` (4-question post-strong-clip diagnostic verbatim from File 08 §3 / Scene-First slide deck "WHEN TESTING BECOMES NARRATIVE"), `### Next-Shot Decision Tree` (5 problem→solution mappings verbatim from Scene-First slide deck "HOW TO CHOOSE THE NEXT SHOT"). Closing disambiguation blockquote in § Next-Shot Decision Tree differentiates the post-generation "continuation / bridge / targeted repair" next-shot types from the per-clip "Continuation / Bridging / Repair" Working Modes (different lifecycle phase, different decision) — anti-collision against the v3.7.3 Working Modes taxonomy.

- **`## Working Practices` new H2 in `skills/higgsfield-pipeline/SKILL.md`** (File 08 §7 parallel-tasks + §8 screenshots-as-working-memory, layer (e) from File 08 row 5 backlog) — placed between § Pipeline E Pitfalls close and § Pipeline Decision Guide. Two H3 sub-sections: `### Working in Parallel` (4 parallel-task categories from File 08 §7 — `Depends on a final frame` / `Writable in parallel` / `Backbone building` / `Waits for later refinement` — bullet leads normalized to noun-phrase form per the bullet-lead normalization rule established this release, see Notes below); `### Screenshots as Working Memory` (5 use-case bullets verbatim from File 08 §8 — `Scene already has a strong identity you do not want to lose` / `Prop or object must remain consistent` / `Body direction matters` / `Emotional carryover is very precise` / `Space is complex enough that text alone may blur it` — strict-verbatim application-gate fix applied at 2h on bullets 1 and 4). Anti-collision in §8 opening prose: explicit "distinct from screenshots as Seedance reference anchors (see `higgsfield-seedance` § Reference Roles)" against seedance line 743 ("Use a screenshot or final frame as your stability anchor") — GPT-side working memory vs prompt-time model reference, different lifecycle phases.

- **`### World Through Recurrence` new H3 in `vocab.md` § Environment & Atmosphere Vocabulary** (File 08 §5, layer (e) from File 08 row 5 backlog) — placed after the Environment Types H3, before the Audio / Sound Vocabulary H2. Eight named substrate axes (recurring spaces / light behavior / silence / materials / architecture / props / emotional conditions / camera distance / rhythm) with one-phrase definitions in `**name** — definition` form mirroring the v3.7.4 § Emotion as Visible Behavior — Channels H3 layout. Ships without a closing forward-link to an endpoint-inventory analog — see structural-asymmetry-by-design note below. Axis names verbatim from the Scene-First slide deck "WORLD THROUGH RECURRENCE" slide (cleaner-phrasing-wins precedent applied — File 08 §5 prose only enumerates 7 axes rhetorically; slide deck names 8 explicitly with "silence" surfaced as a separate bullet).

- **Two cross-link callout blockquotes in `skills/higgsfield-pipeline/SKILL.md` § Working Practices closing cluster** — placed between the H2 closing `---` and § Pipeline Decision Guide, bookended by `---` separators per the existing pipeline house pattern at lines 515-521. (i) `> **Recurrence as continuity substrate:** ...See ../../vocab.md § World Through Recurrence for the eight named substrate axes.` (ii) `> **Post-clip next-shot decisions:** ...See higgsfield-seedance § Post-Clip Decisions.` No inline enumeration of the 8 axes / 4 questions / 5 mappings in callouts — single-source-of-truth pattern; canonical enumeration lives in the target sections only.

- **Substrate→endpoint backlink in `vocab.md` Micro-Expression Vocabulary** (closes v3.7.4 sub-phase 2f Finding 2 — the asymmetric backlink gap). Three-line prose addition at § Micro-Expression Vocabulary intro: "The Emotion as Visible Behavior — Channels section above catalogs the eight substrate channels these endpoint expressions decompose into." Prose form (no `>` blockquote) chosen over § anchor form to mirror the v3.7.4 layer-(d) Channels closing forward-link cadence at vocab.md:191. Closes the substrate↔endpoint asymmetry at both ends of the relationship.

- **`### What Must Carry Over` → Channels cross-link blockquote in `skills/higgsfield-seedance/SKILL.md` § Continuation Prompt Formula** (closes v3.7.4 sub-phase 2b note (d) deferred). Multi-line `>` blockquote inserted between the "What Must Carry Over" subsection close (line 216) and § Example: "For the eight named substrate channels that 'emotional carryover' decomposes into, see `../../vocab.md` § Emotion as Visible Behavior — Channels." Single-source-of-truth pattern: no inline enumeration of the 8 channels in the blockquote, canonical list lives in vocab.md only. v3.7.4 layer-(d) cross-link house-style match.

- **Layer 0 validator in `validate_user_guide.py`** (closes v3.7.4 sub-phase 2e tooling flag — the v3.7.5+ programmatic char-count validator candidate). New `validate_sub_skill_descriptions()` function (+44 lines) imports `SUB_SKILL_DESCRIPTIONS` from `generate_user_guide.py`, asserts every entry ≤ 71 chars (empirical column ceiling verified at v3.7.4), exits with code 1 on overflow with per-entry overflow report, code 2 on environment-setup failure (import error), code 0 on pass. Runs before baseline/candidate comparison (Layer 1 / Layer 2) so source-data overflow fails fast rather than silently rendering as wrapped or clipped text in the regenerated PDF. Closes the v3.7.3 → v3.7.4 inherited-error class at the tooling level — see Notes below for the tooling-fix-closes-error-class observation.

### Changed

- **Frontmatter version bumps** — root `SKILL.md` 3.7.4 → 3.7.5 / updated 2026-05-15 → 2026-05-16; `skills/higgsfield-seedance/SKILL.md` 1.3.0 → 1.4.0 (minor bump for new `## Post-Clip Decisions` H2 — content-arc precedent from v3.7.1 / v3.7.2 / v3.7.3 / v3.7.4) / updated 2026-05-15 → 2026-05-16; `skills/higgsfield-pipeline/SKILL.md` 3.1.0 → 3.2.0 (minor bump for new `## Working Practices` H2) / updated 2026-05-03 → 2026-05-16; `vocab.md` no frontmatter to bump.

- **Closing-paragraph anchor drop in `skills/higgsfield-seedance/SKILL.md` § The Editor-not-Regenerator Mindset** (sharpens v3.7.4 sub-phase 2f Finding 1 — the Repair Skeleton cross-link doubling). Dropped clause: `in § Two-Layer Prompt Authoring above`. Target-flip from the v3.7.4 self-flag suggestion: the v3.7.4 candidate proposed sharpening the *mapping* paragraph cross-link in Translating to Seedance Prompts; v3.7.5 sharpened the *closing* paragraph anchor instead. Rationale: the closing-paragraph anchor was the more redundant of the two (the mapping paragraph's cross-link is operational and earns its slot; the closing paragraph's was a duplicate conceptual pointer 13 lines after the mapping). Mapping paragraph cross-link kept intact. Net: 4 lines deleted, 4 lines re-wrapped; the conceptual claim ("Repair Skeleton = preserve/change split = editor-not-regenerator stance") stands without the explicit § anchor. Catches the v3.7.4 sub-phase 2f self-flag directional error — Self-flag inheritance class catch #4 in the inheritance-pattern taxonomy.

- **`validate_user_guide.py` DEFAULT_BASELINE re-baselined** — `USER-GUIDE.pdf.baseline-v3.7.4` → `USER-GUIDE.pdf.baseline-v3.7.5`. Baseline-management discipline from v3.7.1: new baseline committed to git alongside this release. `USER-GUIDE.pdf` regenerated at 3e is content-equivalent to the v3.7.4 baseline (Layer 1 text-extract diff PASS with version/date pattern normalization) but byte-divergent at ~95% of positions — deflate compression cascades the parameterized input deltas (version string v3.7.4 → v3.7.5, updated date, /CreationDate metadata) through the entire compressed object stream. No substantive content change; rotation reflects version-tracking discipline, not content evolution. None of the v3.7.5 surfaces (pipeline §7/§8, vocab World Through Recurrence, seedance Post-Clip Decisions) propagate into `USER-GUIDE.pdf` because `generate_user_guide.py` content sections are hardcoded — see Drift catalog status below.

- **Bullet-lead normalization rule** (established v3.7.5): when source phrasing is bullet-ready (clausal or noun-phrase form), bullets ship strict verbatim per IP discipline; when source phrasing is rhetorical-question-stem ("what X" or similar), bullet leads normalize to noun-phrase form because the question stem isn't bullet-shaped without reworking. The normalization preserves source content; only the bullet-lead surface form differs. §7 parallel-task categories applied this rule (File 08 "what truly depends on a final frame" / "what can already be written in parallel" / "what belongs to backbone building" / "what should wait for later refinement" → noun-phrase leads `Depends on a final frame` / `Writable in parallel` / `Backbone building` / `Waits for later refinement`); §8 screenshot use-cases shipped strict verbatim (File 08 clausal form was already bullet-ready). Future releases inherit the rule explicitly when source form doesn't lend to verbatim bullet-lead use.

- **In-flight v3.7.5 prose refinements applied during sub-phase review:**
  - **Sub-phase 2b refinements:** A1 vocab backlink form-swap from `>` blockquote form to prose form (no `>`) — mirrors the v3.7.4 layer-(d) Channels closing forward-link at vocab.md:191, preserves substrate↔endpoint cadence symmetry across both ends of the relationship.
  - **Sub-phase 2d refinements:** local-wrap consistency (Option A) applied throughout new pipeline §7/§8 prose at ~70 cols, matching the existing pipeline hard-wrap convention; bullet lines on single rows matching pipeline existing bullet format.
  - **Sub-phase 2e refinements:** `vocab.md` World Through Recurrence H3 ships without closing synthesis prose — applying v3.7.4 layer-(c) Q3 discipline (no padding around a load-bearing claim that doesn't exist); bullet definitions in bare-style matching the existing vocab.md house-style precedent (Body Language / Movement Quality / Channels).
  - **Sub-phase 2f refinements:** seedance § Post-Clip Decisions H2 title plural ("Decisions" not "Decision"); H2 opening cadence tightened (dash-clause reduction); H3-1 closing verb "keeps" over "makes"; dropped unsourced "most common failure point"-style superlative pattern (continued from v3.7.4 sub-phase 2c discipline); 2-sentence disambiguation blockquote restructured (dropped non-canonical "Working-Mode" form discovered at R4 verification — the canonical phrasing is "Working Modes" without hyphen).
  - **Sub-phase 2g refinements:** pipeline §7 bullet 4 source-register refinement — `polish-only work` → `shot-level refinement (inserts, micro-prompts, beat adjustments)` to match File 08 §7's source register ("refinement" is more neutral than "polish-only" which reads as diminutive).
  - **Sub-phase 2h application-gate refinements:** pipeline §8 bullet 1 and bullet 4 strict-verbatim fix — `Scene has a strong identity to preserve` → `Scene already has a strong identity you do not want to lose`; `Emotional carryover is precise` → `Emotional carryover is very precise`. Bullets 1 and 4 had drifted to paraphrased forms in the initial 2h draft; application-gate compare-to-source caught the deviation pre-commit. The "very" qualifier preserved per source modesty. pipeline §8 vocab callout: dropped inline enumeration of 8 axes (single-source-of-truth pattern; canonical list lives in vocab.md only).

### Sourcing

- **Layer (e) — File 08 backlog completion.** All four layer-(e) net-new items per v3.7.4 CHANGELOG line 31 backlog disclosure integrated this release: File 08 §3 four-question post-clip diagnostic, §5 world-through-recurrence framing, §7 parallel-tasks speed principle, §8 screenshots-as-working-memory. With this release, File 08 row 5 layers (a) v3.7.3 + (b) v3.7.3 + (c) v3.7.4 + (d) v3.7.4 + (e) v3.7.5 + (f) v3.7.4 are all integrated; the File 08 audit row is fully consumed.

- **§12 paired complement to §3 (scope-creep disclosure).** File 08 §12 "How to choose the next shot" is the natural production-side complement to §3 "the four-question diagnostic" — §3 asks the questions, §12 maps answers to next-shot types. The pairing was identified during v3.7.5 Phase 1b+1c re-extraction; not pre-committed in v3.7.4 layer (e) backlog list. Both ship together as the paired post-generation cluster in seedance § Post-Clip Decisions (`### The Four Questions` + `### Next-Shot Decision Tree`). Honest scope-creep disclosure per v3.7.4 inheritance-pattern transparency precedent.

- **Scene-First slide deck (companion of File 08, same author).** Confirmed cleaner-phrasing-wins precedent applies for File 08 §3 four questions (slide deck tightens "What is missing for it to feel connected rather than isolated?" → "What is missing for it to feel connected?" and "What kind of shot would make that connection readable?" → "What shot would make the connection readable?" — shipped form matches slide deck) and §5 eight axes (slide deck names 8 verbatim with "silence" surfaced as a separate bullet; File 08 prose rhetorically lists 7 — shipped form matches slide deck). New finding for §8: AXIS PIVOT, not just sharper phrasing — slide deck "Screenshots help preserve" 6-element list (emotional state / body angle / prop placement / camera direction / spatial logic / continuity state) vs File 08 §8 "Screenshots are especially useful when" 5-item use-case list. Different editorial choice, not different phrasing. File 08 use-case form shipped per anti-collision with seedance § Reference Roles (which already enumerates preserve-elements as named reference types — Character / Last-Frame / Environment / Prop); use-case form names a different question Reference Roles doesn't answer.

- **Phase 1c triage ledger** for all 7 source files in `~/Desktop/NEW DOCS_5_3_2026/` audit set:
  - `Workflow Practical Guide English Full.pdf` (File 08) — INTEGRATE row 5 layer (e), shipped this release
  - `A Scene-First Continuity Workflow_ Building Episode One in Seedance.pdf` — DUPLICATE of File 08 (companion slide deck, same author, confirmed cleaner-phrasing-wins on §3 / §5 and AXIS PIVOT discovery on §8)
  - `Building Complete AI Projects from Script to System.pdf` — INTEGRATE deferred to v3.7.6 (C-arc; highest-priority next single-arc release; covers Project Bible / Master Script / GPT Creative Assistant / Prompt Modules / Passes / 10-step end-to-end workflow)
  - `How To 2.pdf` — DUPLICATE of Building Complete AI Projects (text companion of slide deck; will be cross-referenced at C-arc integration)
  - `Nano Banana Pro and Nano Banana 2_ A Creative-Tech Guide.pdf` — SKIP (no Higgsfield-side actionable content; Featured-model routing already exists in `skills/higgsfield-models/` for both models)
  - `PRODUCT REFERENCE SHEET PROMPTS.txt` — DUPLICATE of v3.7.2 Product Reference Sheet integration
  - `Reference Workflow_.pdf` — DUPLICATE of v3.7.1 Video Reference Capability Surface + v3.7.2 Product Reference Sheet
  - `article nano (2).pdf` — SKIP (marketing copy)

- **B1 Cinema Studio 3.5: TRIAGE FINDING, not deferred.** Scoped for assessment at Phase 1, found UNACTIONABLE — no source PDF in the audit set contained material to close any of the 7 Cinema Studio 3.5 deferrals tracked in `higgsfield-cinema/SKILL.md` (AI Director Toggle behavioral documentation still requires Peter's hands-on UI testing; per-Cinematic-model video-mode picker structure still requires additional UI screenshots). Removed from v3.7.5 release scope prior to Phase 2. Not a deferral — a triage finding that the deferral pile is awaiting external input (UI testing + screenshot capture by Peter), not audit-source identification by Claude Code.

- **IP discipline held throughout.** Paraphrased prose per File 08 source discipline; named factual prescriptions verbatim: 8 substrate axes (vocab.md World Through Recurrence), 4 questions (seedance Post-Clip Decisions / Four Questions), 5 problem→solution mappings (seedance Next-Shot Decision Tree), 4 parallel-task categories (pipeline Working in Parallel — bullet leads normalized to noun-phrase form per the bullet-lead normalization rule, see Notes below), 5 screenshot use-cases (pipeline Screenshots as Working Memory — strict verbatim post-application-gate fix). No verbatim long-prose extracts; no verbatim worked-example prompts.

### Notes

- **Backlog closeout exception.** v3.7.5 ships 9 deliverables in one release counted at the granular level — A1 (vocab backlink) + A2 (seedance Editor-not-Regenerator anchor drop) + A3 (Layer 0 validator) + A4 (seedance What Must Carry Over cross-link) + B2 §3+§12 (Post-Clip Decisions H2) + B2 §5 (World Through Recurrence H3) + B2 §7 (Working in Parallel H3) + B2 §8 (Screenshots as Working Memory H3) + 2 pipeline callouts. Second exception to single-arc-scope discipline after v3.7.4 (the layer (c)+(d)+(f) one-time exception). Rationale: closing out the audit-set backlog before context switch. All 9 deliverables source from a single audit (2026-05-11) and integrate net-new content with low anti-collision risk after Phase 1c triage cut B1 and deferred C-arc. **HARDER single-arc discipline commitment for v3.7.6+:** the audit-set is now fully consumed (5 DUPLICATE + 2 SKIP + 1 INTEGRATE-deferred at C-arc; File 08 layer (e) integrated this release). Future arcs require fresh source identification, not backlog mining. C-arc Building Complete AI Projects is the single highest-priority v3.7.6 arc; commit to single-arc shape.

- **Inheritance-pattern meta-observation — 13 caught errors at verification gates across v3.7.4 + v3.7.5, spanning 7 distinct error classes.** (1) **Factual inheritance** (#1-3 v3.7.4): claims from prior CHANGELOGs that didn't match current repo state. (2) **Self-flag inheritance** (#4): directionally-wrong v3.7.4 2f self-flag — v3.7.5 A2 target-flip caught the divergence between flag direction (mapping paragraph) and actual sharpening (closing paragraph). (3) **Source-conflation** (#5 + #8 + #13): orchestrator-side Phase 1 prompt condensation errors; #13 specifically the single-source assumption when two sources existed (Phase 1c described File 08 §8 only, missed Scene-First slide deck's AXIS PIVOT to preserve-list form). (4) **Reference-class mismatch** (#6 + #12): cross-skill precedent misapplied to wrong file or wrong context; #12 specifically pipeline house-style verification missed at first attempt (seedance inline-blockquote pattern proposed for pipeline before re-reading pipeline's actual 515-521 callout-cluster precedent). (5) **Reference-locator drift** (#7): line-number citation from stale memory. (6) **Non-canonical-form invention** (#9): syntax form suggested that doesn't appear in target file. (7) **Infrastructure failure** (#10 + #11, NEW CLASS for v3.7.5): orchestration-layer failures — session-boundary context loss (2g/2h pre-edit drafts didn't persist across turn boundaries), markdown code-fence nesting failure (triple-backtick inside triple-backtick stripped inner content). Gate mechanism generalizes bidirectionally: catches both Claude Code's prior CHANGELOG inheritance and orchestrator-side condensation errors. **Application gate distinct from pre-edit verification gate:** pre-edit gates catch inherited claims before authoring; application gates catch in-flight deviations at edit time (e.g., the §8 bullet 1 + 4 strict-verbatim fix at 2h). Two different mechanisms, both contribute to discipline.

- **Layer 0 validator tooling closure.** `validate_user_guide.py` Layer 0 `SUB_SKILL_DESCRIPTIONS` check now formally enforces the empirical 71-char column ceiling — replacing the v3.7.4 informal CHANGELOG-note discipline (per v3.7.4 CHANGELOG line 45: "v3.7.5+ description updates should either re-evaluate the empirical ceiling against the actual 115mm Helvetica 9pt column rendering, or route new content through CHANGELOG / cross-links") with programmatic enforcement. Future releases inherit programmatic prevention of the silent-overflow risk rather than depending on Claude Code re-reading the prior CHANGELOG self-claim. **Tooling-fix-closes-error-class precedent worth carrying forward:** when an inherited-error class is caught at gate across multiple releases, the structural close is a tooling addition that makes the discipline programmatic rather than narrative.

- **§8 source-pivot discovery.** Phase 1c summary described File 08 §8 as "5-bullet use-case list" but missed that the Scene-First slide deck pivoted the bullet axis to a 6-element "what screenshots preserve" list — not just sharper phrasing but a different editorial choice. File 08 form shipped per anti-collision with seedance § Reference Roles (which already enumerates preserve-elements as named reference types — Character / Last-Frame / Environment / Prop); use-case form names a different question Reference Roles doesn't answer. Phase 1c summary-style audit assumptions should compare both source forms when both exist, not assume one mirrors the other. Logged as catch #13 in the inheritance-pattern taxonomy (source-conflation class).

- **`vocab.md` World Through Recurrence structural-asymmetry-by-design.** The new H3 ships without a closing forward-link, unlike v3.7.4 layer (d) Emotion as Visible Behavior — Channels H3 which forward-links to Micro-Expression Vocabulary as substrate→endpoint relationship. Asymmetry is structural: §5 substrate (world-cohesion axes) has no endpoint-inventory analog in vocab.md to forward-link to (the endpoint would be a "named worlds" or "world-typing" inventory; vocab.md doesn't have one). Closing prose would be synthesis padding without a load-bearing claim. v3.7.4 layer (c) Q3 discipline applied (no padding around a load-bearing claim that doesn't exist). Backlink completeness preserved at the other relationship — Channels↔Micro-Expression Vocabulary now backlinks symmetrically via A1.

- **Bullet-lead normalization rule (established v3.7.5).** See Changed subsection above for the full rule. Documented here in Notes for future-release inheritance: when source phrasing is bullet-ready, bullets ship strict verbatim; when source is rhetorical-question-stem, bullet leads normalize to noun-phrase form, preserving source content with only the surface form differing. §7 and §8 in this release apply the rule asymmetrically per source form (§7 normalized, §8 strict verbatim).

- **Drift catalog status** (verified at Phase 3c per per-release verification gate; not inherited from v3.7.4 CHANGELOG self-claims). 6 D-items at v3.7.5 start (D3-D8 inline at `docs/pdf-audit/AUDIT-REPORT-v3.6.0.md:313`). **0 closed.** **1 partially addressed:** D8 — Layer 0 validator formally enforces the 71-char column ceiling (enforcement gap closed by tooling); `SUB_SKILL_DESCRIPTIONS` data entries remain stale relative to v3.6.4 content additions (data still byte-identical to v3.7.4 baseline). **5 unchanged at USER-GUIDE.pdf surface:** D3 / D4 / D5 / D6 / D7 (`generate_user_guide.py` not touched this release; last touch v3.7.3). **5 compound events with surface overlap:** D4 (Section 10 — Seedance prompt modes) compounds with 3 new v3.7.5 surfaces (pipeline § Working in Parallel, pipeline § Screenshots as Working Memory, seedance § Post-Clip Decisions); D6 (Section 18 — Iteration Rule + 6-Pass Diagnostic) compounds with 2 new v3.7.5 surfaces (seedance § The Four Questions, seedance § Next-Shot Decision Tree — both iteration-and-diagnostic frameworks; sub-components of the same Post-Clip Decisions H2 that D4 also counts, hence "surface overlap"). Weak adjacency, not counted as drift compound: vocab.md World Through Recurrence conceptually connects to higgsfield-cinema Reference Sheet Types (both deal with what-must-recur-across-shots logic) but lives in a different file in a different category. **Net trend:** drift visibly compounding; D4 and D6 USER-GUIDE staleness now spans the v3.6.4 additions + 5 v3.7.5 net-new surfaces.

#### v3.7.6+ candidates

Tracked inline in this release-notes context for visibility; convert to a separate `BACKLOG.md` if the list grows beyond ~6 items.

- **C-arc Building Complete AI Projects** (Phase 1c Category C INTEGRATE-deferred — highest priority for v3.7.6). Substantial standalone arc covering Project Bible / Master Script / GPT Creative Assistant / Prompt Modules / Passes / 10-step end-to-end workflow. Target sub-skill: `higgsfield-pipeline` (likely a new ## H2 cluster). Deserves dedicated single-arc release. Source: `Building Complete AI Projects from Script to System.pdf` (plus `How To 2.pdf` companion).

- **USER-GUIDE.pdf modernization arc.** Dedicated single-arc release updating Section 10 (Seedance prompt modes — D4), Section 11 (Soul Cinema + Studio Look — D5), Section 18 (Iteration Rule + 6-Pass Diagnostic — D6), Section 21 (Reference Sheet Types + v3.6.4 piano test / Action Design / Morph-Cut — D7), Section 22 (sub-skill row descriptions via `SUB_SKILL_DESCRIPTIONS` dict updates — D8 data refresh). Would close D4, D5, D6, D7, D8 simultaneously. Scope likely substantial (5 sections × content drift accumulated over 3 releases since v3.6.0); deserves dedicated treatment. The Layer 0 validator added this release will enforce the column ceiling on any `SUB_SKILL_DESCRIPTIONS` updates.

- **Mr. Core methodology additional work.** Deferred from v3.7.5 backlog clarification at Phase 1b — Mr. Core was already integrated v3.6.4 from "Building a Cinematic Universe", a different source than File 08. If additional Mr. Core work is wanted, source PDF needs separate identification by Peter. Lower priority than C-arc and USER-GUIDE modernization.

Commit prefix: `feat: v3.7.5 — backlog closeout: A-arcs + File 08 layer (e) + Layer 0 validator + 2 cross-link callouts`

## v3.7.4 — 2026-05-15

### Added

- **Two-Layer Prompt Authoring** new H2 section in `skills/higgsfield-seedance/SKILL.md` (layer (c) from File 08 row 5) — placed between § Working Modes and § Pre-flight Linter. Four H3 sub-sections: `### The Two-Layer Distinction` (Layer 1 task definition / briefing block ↔ Layer 2 production prompt), `### Bridge Skeleton` (Layer 1 briefing block with 6 named fields + Layer 2 production skeleton), `### Continuation Skeleton` (Layer 1 briefing + Layer 2 skeleton + 5-variant anti-repeat phrase library), `### Repair Skeleton` (Layer 1 briefing + Layer 2 skeleton + closing observation on the under-used "do not damage" field). No closing-synthesis H3 — load-bearing claim ("the distinction makes the workflow practical") lands in the opening Two-Layer Distinction H3 rather than after the skeletons, per goal-backward analysis at 2a Q3.

- **Keyframe Workflow** new H2 section in `skills/higgsfield-seedance/SKILL.md` (layer (f) from File 08 row 5) — placed between § Two-Layer Prompt Authoring and § Pre-flight Linter. Three H3 sub-sections: `### Capability Surface` (5 named BytePlus VideoPilot editing primitives — continuous keyframe segmentation / fine-grained keyframe edits / custom keyframes / partial redraw of selected regions / keyframe description rewrite), `### Translating to Seedance Prompts` (6 operational rules + mapping paragraph cross-linking to Repair Skeleton + Reference Roles / Last-Frame + Reference Roles / Character + Continuation Skeleton), `### The Editor-not-Regenerator Mindset` (closing synthesis cross-linking to Repair Skeleton as the same discipline at the prompt-only level). H2 name follows the Rule-of-12 precedent at `skills/higgsfield-models/MODELS-DEEP-REFERENCE.md:274` (canonical concept in heading; BytePlus VideoPilot product attribution in opening paragraph + sourcing block).

- **Emotion as Visible Behavior — Channels** new H3 in `vocab.md` § Subject & Character Vocabulary (layer (d) from File 08 row 5) — placed after the existing Emotion Cues H3. Eight named substrate channels (breath / eye behavior / jaw tension / loss of focus / scanning pattern / delayed recovery / control attempt / emotional residue after the peak) with one-phrase definitions in bare comma-list / fragment form matching the surrounding vocab.md house style (Body Language / Movement Quality). Closing prose forward-links to the Micro-Expression Vocabulary section below as substrate→endpoint relationship. Net-new vs the existing repo content: the principle ("describe physics, not emotion" / "micro-expressions work as physics") is restated in four places already, but the channels themselves — the substrate that PRODUCES the visible behavior — are not named anywhere prior to this release.

- **Two cross-link blockquotes pointing at the new vocab.md channels H3** — (i) `skills/higgsfield-seedance/SKILL.md` § Voice Rewrite, multi-line blockquote after rule 6, before separator: "For the eight named substrate channels that 'describe physics, not emotion' decomposes into, see `../../vocab.md` § Emotion as Visible Behavior — Channels." (ii) `skills/higgsfield-prompt/SKILL.md` § Seedance 2.0 Engine Constraints / Sensory rules, multi-line blockquote after the "Micro-expressions work as physics" bullet, before § Action rules: same target, slightly different framing ("that micro-expressions decompose into"). Style matches v3.7.3 cross-link house pattern (multi-line `>` with prose framing wrapped at ~65 chars). No inline enumeration of channel names in blockquotes — single-source-of-truth pattern, channels live canonically in vocab.md only.

### Changed

- **Frontmatter version bumps** — root `SKILL.md` 3.7.3 → 3.7.4 / updated 2026-05-15; `skills/higgsfield-seedance/SKILL.md` 1.2.0 → 1.3.0 (minor bump for two new H2 sections — content-arc precedent from v3.7.1 camera + v3.7.2 cinema + v3.7.3 seedance) / updated 2026-05-15; `skills/higgsfield-prompt/SKILL.md` updated 2026-05-11 → 2026-05-15 only, no version bump (per v3.7.3 precedent at CHANGELOG.md:16 for one-line cross-link additions); `vocab.md` no frontmatter to bump.

- **`SUB_SKILL_DESCRIPTIONS["higgsfield-seedance"]` intentionally NOT updated** in `generate_user_guide.py:85`. Char-count math verified at authoring time via grep + `len()` against the dict: current entry is 71 chars at the empirical column ceiling (tied with `higgsfield-cinema` at 71); adding `+ two-layer authoring` → 93 chars (overflow 22), adding `+ keyframe workflow` → 91 chars (overflow 20), trimming the `Seedance 2.0 ` prefix still overflows at 80 / 78 chars (overflow 9 / 7). Per v3.7.3 precedent (CHANGELOG line 15: "Reference Roles intentionally not listed in the entry to stay within column width"), the existing "working modes" reference implicitly covers layer (c) via shared Bridge / Continuation / Repair skeleton naming; layer (f) keyframe workflow gets no column mention and is discovered via seedance routing in the root `SKILL.md` table.

- **`validate_user_guide.py` DEFAULT_BASELINE re-baselined** — `USER-GUIDE.pdf.baseline-v3.7.3` → `USER-GUIDE.pdf.baseline-v3.7.4`. Baseline-management discipline from v3.7.1: new baseline committed to git alongside this release.

- **In-flight v3.7.4 prose refinements applied during sub-phase review:**
  - **Sub-phase 2b refinements:** dropped editorial superlative "which is the most common failure point" from the layer-(c) Continuation Skeleton intro (unsourced — not supported by either v3.7.3 § Continuation Prompt Formula or File 08 §11.B); refined `@Image2 = optional continuity start or location anchor` → `@Image2 = continuity start or location anchor (omit if neither is needed)` for dual-function clarity; softened "Every practical skeleton in this workflow has two layers" → "Each practical skeleton in this workflow has two layers, each with a different audience and a different job" (the Exploration mode's Layer 1 collapses to one sentence per File 08 §6, so "Every" was factually wrong, not just over-broad).
  - **Sub-phase 2b cross-link form swap:** switched layer-(d) cross-link blockquotes from inline-enumeration form to canonical-pointer form after pre-edit-style verification against v3.6.5 marketing-strip discipline (single-source-of-truth pattern; channels enumerated only in vocab.md).
  - **Sub-phase 2b vocab.md normalization:** normalized 8 channel definitions to bare comma-list / fragment form matching surrounding house style (File 08 source had zero definitions; all definitions are editorial paraphrasing, and uniformity matters more than the abstract-vs-concrete density variance initially introduced).
  - **Sub-phase 2d refinements:** subject-verb agreement fix ("None of them guarantees" → "None of them guarantee") in layer-(f) Translating to Seedance Prompts intro; compressed the Editor-not-Regenerator H3 closing paragraph from two sentences to one (one-sentence form preserves both surfaces named + "different levels" framing without the doubling-restates-then-elaborates pattern).

### Sourcing

- **Layers (c) + (d) + (f)** — sourced from File 08 (`Workflow Practical Guide English Full.pdf`, 15pp, the deepest source in the 2026-05-11 audit set) per `/tmp/higgsfield-audit-2026-05-11/AUDIT.md` row 5, recommendation INTEGRATE (high-impact). Layers (a) Reference Roles taxonomy + load-bearing rule and (b) Four Working Modes + decision tree integrated v3.7.3; layers (c) Two-Layer Prompt Authoring (briefing block + Bridge / Continuation / Repair skeletons), (d) emotion-as-visible-behavior channels vocabulary, and (f) BytePlus VideoPilot keyframe workflow integrated this release. Layer (e) net-new backlog items (four-question post-clip diagnostic from File 08 §3, world-through-recurrence framing from §5, parallel-tasks speed principle from §7, screenshots as working memory from §8) remain in backlog for future single-arc releases.

- **Layer (f) additional sourcing** — `seed.bytedance.com` (ByteDance's official Seedance launch materials) and `docs.byteplus.com` (BytePlus VideoPilot fine-tuning documentation), as cited in File 08 §11.D-E. Same official source set as the Rule of 12 citation at `skills/higgsfield-models/MODELS-DEEP-REFERENCE.md:274`; the new H2's Sourcing block cross-links to that earlier citation rather than restating provenance.

- **IP discipline** — paraphrased content only per File 08 source discipline. Short technical phrases (named blocks, skeleton field names, the Two-Layer distinction terms, the eight emotion channel names, the five VideoPilot capability names, the six VideoPilot-to-Seedance translation rules, the "freeze / isolate / local and explicit" mindset framing, the BytePlus VideoPilot product name) are factual prescriptions and land as-is. No verbatim long-prose extracts. No verbatim worked-example prompts from File 08 — the bridge / continuation / repair worked examples in File 08 §11.A-C are referenced by paraphrase only; repo content downstream of this audit produces repo-native explanations rather than File-08-native ones.

- **AUDIT.md re-extract** — the original `/tmp/higgsfield-audit-2026-05-11/AUDIT.md` was lost when `/tmp` cleared between releases. A partial re-extract scoped to row 5 layers (c) / (d) / (f) was performed at v3.7.4 Phase 1 via direct re-read of File 08 PDF; the re-extract lives at `/tmp/higgsfield-audit-2026-05-11/AUDIT.md` (not committed to repo per the audit-file IP discipline). Rows 1–4 + row 5 layers (a) + (b) are not re-extracted; the integrated content in repo (v3.7.1 / v3.7.2 / v3.7.3) is the canonical record for those.

### Notes

- **Combined-release exception.** This release combines three layers (c) + (d) + (f) from a single audit-row source — an explicit one-time exception to the single-arc-scope discipline held since v3.6.x. Rationale: all three layers source from the same File 08 audit row 5, all are small additive insertions, and shipping together collapses three baseline-rotation cycles into one. Return to single-arc discipline for v3.7.5+.

- **Inheritance-pattern meta-observation.** v3.7.4 verification gates caught three inherited errors during sub-phase execution: (1) 2b cross-link target audit error — Phase 1 audit asserted both physics/emotion principle restatements lived in `higgsfield-seedance`, pre-edit verification caught one is actually in `higgsfield-prompt`; (2) 2c "most common failure point" unsourced editorial superlative in layer-(c) Continuation Skeleton intro, caught at post-2a verification; (3) 2e char-count math inherited from v3.7.3 CHANGELOG miscount (67 / 70 / ~3 figures cited, actual is 71 / 71 / 0). Catch mechanism in all three: per-sub-phase verification gates re-reading current file state rather than trusting prior-release self-claims. Forward instruction: continue per-sub-phase verification gates for v3.7.5+; programmatic char-count validator in `validate_user_guide.py` (deferred to v3.7.5+ tooling candidate) would prevent the third error class from recurring.

- **Inheritance disclosure + forward note for `SUB_SKILL_DESCRIPTIONS` ceiling.** v3.7.3 CHANGELOG line 15 cited 67 / 70 / ~3 figures; v3.7.4 verification found these to be a miscount — the entry has always been 71 chars since the v3.7.3 update, and the empirical ceiling is 71 chars set by the two longest shipped entries. Defer decision survives regardless of which figures are used; this note corrects the record, not the action. The corrected ceiling reframes the threshold for future releases — any further entry-extending arc is now overflow territory, not just "two-in-a-row." v3.7.5+ description updates should either re-evaluate the empirical ceiling against the actual 115mm Helvetica 9pt column rendering, or route new content through CHANGELOG / cross-links instead of the description string.

- **Additive-only release; no restructuring of pre-v3.7.4 content.** 339 insertions / 5 deletions across 4 touched files; all 5 deletions are frontmatter scalar replacements (root version + updated; seedance version + updated; prompt updated). Primary sub-skill touched: `higgsfield-seedance` (two new H2 sections inserted as a contiguous block between existing § Working Modes and § Pre-flight Linter; one in-flight blockquote cross-link added at § Voice Rewrite). Secondary touch: `higgsfield-prompt` (one in-flight blockquote cross-link at § Seedance 2.0 Engine Constraints / Sensory rules). Tertiary touch: `vocab.md` (one new H3 in § Subject & Character Vocabulary). No edits to other sub-skill files; no routing changes; no new sub-skills.

- **Drift catalog status.** D4 (5 Seedance prompt modes unreflected in USER-GUIDE Section 10) — v3.7.4 layer-(c) Two-Layer Prompt Authoring adds another adjacent surface (skeletons operationalizing the Bridging / Continuation / Repair working modes), but USER-GUIDE Section 10 still doesn't enumerate the prompt modes or the working modes or the skeletons. D4 NOT closed; drift accumulates. D6 (Iteration Rule + 6-Pass Diagnostic) — v3.7.4 layer-(c) skeletons reinforce the iteration/diagnostic framework adjacently, but USER-GUIDE Section 18 hasn't been updated. D6 NOT closed. D8 (sub-skill row descriptions unreflected) — v3.7.4's 2e snippet formally documents the 70-char-ceiling deferral that PREVENTS the higgsfield-seedance row description from being refreshed. D8 NOT closed; reason now formally documented. D3 / D5 / D7 status unchanged (v3.7.4 didn't touch their surfaces). Drift catalog source: `docs/pdf-audit/AUDIT-REPORT-v3.6.0.md:313` (USER-GUIDE expansion row, inline D3-D8 list). Verified at v3.7.4 Phase 3c rather than inherited from v3.7.3 CHANGELOG self-claim.

- **`USER-GUIDE.pdf` regenerated** by `generate_user_guide.py`. Build-time invariant passes trivially (`SUB_SKILL_DESCRIPTIONS` keys unchanged — no Section 22 sub-skill list change). Validator baseline rotated: v3.7.3 → v3.7.4. Layer 1 text-extract diff prediction: zero substantive content diffs (the `SUB_SKILL_DESCRIPTIONS` deferral means no Section 22 row text change); version-string deltas (v3.7.3 → v3.7.4) pattern-normalized to zero; date string deltas (v3.7.3 was same-day-as-v3.7.1/2 on 2026-05-11; v3.7.4 ships 2026-05-15, +4 days). Layer 2 binary diff: expected to cascade through deflate-compressed PDF object streams.

#### v3.7.5+ candidates

Tracked inline in this release-notes context for visibility; convert to a separate `BACKLOG.md` if the list grows beyond ~6 items.

- **Repair Skeleton cross-link doubling sharpening** (layer (c) Finding 1 at v3.7.4 sub-phase 2f). The cross-link to Repair Skeleton appears twice within 13 lines of layer (f) — once in Translating to Seedance Prompts mapping paragraph (operational), once in Editor-not-Regenerator Mindset closing (conceptual). Both earn their slots in their respective paragraphs; the doubling effect on full-section scan is real but mild. Optional v3.7.5+ wordsmithing pass could substitute the mapping reference with a lighter "preserve / change blocks above" (no explicit § anchor).
- **Substrate→endpoint backlink in vocab.md** (layer (d) Finding 2 at v3.7.4 sub-phase 2f). The new H3 closes with a forward cross-link to the existing Micro-Expression Vocabulary H2 — but Micro-Expression Vocabulary's own intro doesn't backlink to the channels. A v3.7.5+ one-line intro edit to Micro-Expression Vocabulary would close the asymmetry. Deferred this release per additive-only discipline (the edit would touch pre-v3.7.4 content).
- **Programmatic char-count validator** (v3.7.4 sub-phase 2e tooling flag). Add a `validate_user_guide.py` check that re-asserts each `SUB_SKILL_DESCRIPTIONS` entry against the empirical column ceiling at every validation pass. Would prevent the v3.7.3 → v3.7.4 inheritance-error class from recurring.
- **"What Must Carry Over" cross-link backfill target** (v3.7.4 sub-phase 2b note (d) deferred). The layer-(c) skeletons mention "emotional carryover" / "emotional residue" / "emotional state" 7+ times across Bridge / Continuation / Repair. A higher-leverage backfill location than the skeletons themselves is § Continuation Prompt Formula's "What Must Carry Over" subsection (lines 209–216 of seedance, pre-v3.7.4 content), which lists "emotional carryover" with elaboration. v3.7.5+ could add a one-line cross-link there to the new channels vocab.

Commit prefix: `feat: v3.7.4 — File 08 layers (c)+(d)+(f) combined (one-time exception)`

## v3.7.3 — 2026-05-11

### Added

- **Working Modes vs Prompt Modes — Two Taxonomies** disambiguation section in `skills/higgsfield-seedance/SKILL.md` — new H2 placed after the Continuation Prompt Formula and before the Pre-flight Linter. Names Working modes (user intent), Prompt modes (platform mechanism), and Reference roles (what references represent) as three peer concepts; explicitly addresses the "Continuation" word collision (same word names a working mode AND a prompt mode — different layers, different meanings, but they often co-occur). Includes a 4-row mapping table showing typical prompt-mode routes per working mode + which reference roles tend to come along.
- **Reference Roles** taxonomy in `skills/higgsfield-seedance/SKILL.md` — new H2 with four named roles (Character / Last-Frame / Environment / Prop) as H3 sub-sections, each with definition + Seedance prompt pattern. Semantic-role layer, distinct from `skills/higgsfield-cinema/SKILL.md` § @ Reference Patterns for Cinema Studio 3.0 (line 1568, input-modality × scenario use-case patterns). Character role cross-links to `../higgsfield-soul/SKILL.md` § Character Sheet Creation; Last-Frame cross-links to the existing Continuation Prompt Formula above; Environment cross-links to cinema's Location Reference Sheets; Prop is net-new as a named role category. Closes with the synthesis Load-Bearing Rule sub-section (intentionally a synthesis block, not a fifth role entry).
- **References Support Memory, Text Defines Action** load-bearing rule callout closing the Reference Roles section. Heading `### Load-Bearing Rule` (section TYPE per v3.7.1 camera precedent at `skills/higgsfield-camera/SKILL.md:326`); body opens with the bold rule statement, then 4-sentence supporting prose, then a cross-link paragraph naming the sibling v3.7.1 camera-side rule ("Prompt wins on action, reference wins on texture and world feel"). The camera-side rule names the WIN order in case of conflict; the Seedance-side rule names the LANES each side covers — both rules now appear in the repo as peer formulations of the same underlying principle.
- **Working Modes** taxonomy in `skills/higgsfield-seedance/SKILL.md` — new H2 with four named modes (Exploration / Continuation / Bridging / Repair) as H3 sub-sections, each with definition + which prompt mode it typically routes through. User-intent layer on top of the existing 5 Seedance prompt modes. Closes with the synthesis Decision Tree sub-section (intentionally a synthesis block, not a fifth mode entry) — a 6-row symptom → working-mode diagnostic table with closing prose framing the decision tree as symptom-first, not mode-first ("the mode is the treatment; the symptom in your work is the diagnostic").
- **One-line cross-link** in `skills/higgsfield-prompt/SKILL.md` § Seedance 2.0 Prompting Best Practices (after line 307) pointing at the new Working Modes section in `higgsfield-seedance`. Style matches v3.7.1's `higgsfield-motion` blockquote cross-link to `higgsfield-camera` (multi-line blockquote with prose framing).

### Changed

- **`SUB_SKILL_DESCRIPTIONS["higgsfield-seedance"]` updated** in `generate_user_guide.py:85` — `"Seedance 2.0 prompt director + content-filter preflight"` → `"Seedance 2.0 prompt director + working modes + content-filter preflight"` (67 chars, under the existing 70-char column ceiling — no Section 22 column-width recalibration needed). Reflects the new user-intent layer. Reference Roles intentionally not listed in the entry to stay within column width; readers discover roles via the working-modes section.
- **Frontmatter version bumps** — root `SKILL.md` 3.7.2 → 3.7.3; `skills/higgsfield-seedance/SKILL.md` 1.1.0 → 1.2.0 (minor bump for three new H2 sections in the primary sub-skill, matching v3.7.1 camera + v3.7.2 cinema content-arc precedents). `skills/higgsfield-prompt/SKILL.md` `updated`-date refresh only (2026-05-03 → 2026-05-11), no version bump — single one-line cross-link, per v3.7.1 `higgsfield-motion` precedent at CHANGELOG.md:107. All `updated` fields set to 2026-05-11.
- **`validate_user_guide.py` DEFAULT_BASELINE re-baselined** — `USER-GUIDE.pdf.baseline-v3.7.2` → `USER-GUIDE.pdf.baseline-v3.7.3`. Baseline-management discipline from v3.7.1: new baseline committed to git alongside this release.

### Sourcing

- **Working Modes + Reference Roles + load-bearing rule** — sourced from File 08 (`Workflow Practical Guide English Full.pdf`, 15pp, the deepest source in the 2026-05-11 audit set) per `/tmp/higgsfield-audit-2026-05-11/AUDIT.md` row 5, recommendation INTEGRATE (high-impact). Layers (a) Reference Roles taxonomy + load-bearing rule and (b) Four Working Modes + decision tree integrated in this release. Layers (c) briefing block + skeleton templates, (d) emotion-as-visible-behavior vocab.md additions, and (f) BytePlus VideoPilot keyframe workflow deferred to later releases per single-arc scope discipline. Paraphrased content only per File 08 IP discipline — short technical phrases (role names, mode names, the load-bearing rule statement) are factual prescriptions and land as-is.
- **Anti-collision finding — v3.6.0 AUDIT-REPORT.md item 11 misclassification.** The v3.6.0 audit classified an input-modality reference-roles framing ("image = identity/wardrobe/palette/composition; video = motion rhythm/camera behavior/blocking; audio = timing/speech/ambience") as DUPLICATE against `higgsfield-cinema/SKILL.md` § @ Reference Patterns. Verified during Phase 2A: cinema's @ Reference Patterns for Cinema Studio 3.0 section (line 1568) lists 9 concrete use-case patterns keyed off `@Image1` / `@Video1` / `@Audio1` but does NOT name a "Reference Roles" taxonomy. File 08's framing (character / last-frame / environment / prop) is a semantic-role layer, orthogonal to cinema's input-modality patterns. The two coexist; the new Reference Roles H2 cross-links to cinema's pattern catalog for concrete examples. The v3.6.0 DUPLICATE classification was an over-aggressive dedup based on the auditor's reading of cinema content, not an actually-named existing taxonomy. Future maintenance pass could amend the AUDIT-REPORT.md item 11 entry to note the correction; out of v3.7.3 scope.

### Notes

- **Deferred from File 08 to later releases.** (c) Briefing block + Bridge/Continuation/Repair prompt skeletons → candidate for v3.7.4 as a new "Two-Layer Prompt Authoring" section. (d) Emotion-as-visible-behavior vocabulary → candidate for vocab.md addition under a future release. (f) BytePlus VideoPilot keyframe workflow → candidate for `higgsfield-seedance` sub-section. Other File 08 net-new items (five anchor types, anti-repeat phrase library, weak-vs-better worked examples, world-through-recurrence framing) tracked as backlog under the same File-08-integration arc.
- **Additive-only release.** No restructuring of pre-v3.7.3 content. Primary sub-skill touched: `higgsfield-seedance` (three new H2 sections inserted as a pure block between the existing Continuation Prompt Formula section and Pre-flight Linter section). Secondary touch: one-line blockquote cross-link in `higgsfield-prompt`. Tertiary touch: one-line `SUB_SKILL_DESCRIPTIONS` value update in `generate_user_guide.py`. `vocab.md` untouched — Reference Roles is seedance-internal vocabulary (per v3.7.2 precedent for reference-sheet types).
- **"Continuation" word collision explicitly addressed.** Same word names a working mode AND a prompt mode. The disambiguation section's `### The "Continuation" Word Collision` H3 defines both senses, names the common-case overlap (Continuation working mode + Continuation prompt mode), names the edge cases (Bridging and Repair working modes also reach for Continuation prompt mode), and gives a disambiguation rule for ambiguous usage: section context disambiguates, longer forms "Continuation working mode" / "Continuation prompt mode" available if context isn't enough.
- **Closing synthesis sub-sections, not parallel entries.** The Reference Roles section closes with `### Load-Bearing Rule` (synthesis: WHY the role taxonomy matters, plus the cross-link to the sibling camera-side rule); the Working Modes section closes with `### Decision Tree — Picking a Working Mode` (synthesis: HOW to use the working modes, with a symptom-first diagnostic table). Intentional pattern, matching the repo's existing synthesis-closer style (e.g. the piano test at `skills/higgsfield-cinema/SKILL.md:663` is a closing synthesis under Outfit / Material Sheet, not a parallel entry).
- **Drift catalog status.** D4 (5 Seedance prompt modes unreflected in USER-GUIDE Section 10) — File 08's parallel 4-mode working-modes taxonomy added alongside the existing 5 prompt modes; both layers now in repo with explicit disambiguation. D4 NOT closed (the existing 5 modes already in repo at v3.7.1 time are still not enumerated in USER-GUIDE Section 10 — that's a separate USER-GUIDE-expansion concern). D6 (Iteration Rule + 6-Pass Diagnostic) — File 08's Repair working mode + decision tree adds an adjacent framing but uses a different mental model; D6 NOT closed. D3 / D5 / D7 (Product axis added v3.7.2) / D8 status unchanged.
- **`USER-GUIDE.pdf` regenerated** by `generate_user_guide.py`. Build-time invariant passes trivially (`SUB_SKILL_DESCRIPTIONS` keys unchanged — only the value for `higgsfield-seedance` changes). Validator baseline rotated: v3.7.2 → v3.7.3. **Layer 1 text-extract diff prediction:** ONE substantive content diff (Section 22 seedance row text update from the `SUB_SKILL_DESCRIPTIONS` edit — same pattern as v3.7.1's camera row update); version-string deltas (v3.7.2 → v3.7.3) pattern-normalized to zero substantive diff; date string deltas zero (same-day release as v3.7.1 / v3.7.2). Layer 2 binary diff: expected to cascade through deflate-compressed object streams.
- **No sub-skill content moved or removed. No routing changes. No new sub-skills.**

Commit prefix: `feat: v3.7.3 — Working Modes + Reference Roles + Two-Taxonomies disambiguation (File 08 layers a+b)`

## v3.7.2 — 2026-05-11

### Added

- **Product Reference Sheet** as the 6th reference-sheet type in `skills/higgsfield-cinema/SKILL.md` § Reference Sheet Types. New H3 sub-section `### Product Reference Sheet` placed between the existing `### Palette / Mood Sheet` block and the `### The Reference Sheet Family` summary table — the structural parallel slot, since prose order now matches table order. Section content:
  - Sub-bullet: 7-part prompt scaffold — Identity Lock + Branding Lock + Layout + Background + Realism + Camera + Restrictions. Parallel to existing reference-sheet templates but adapted for products (no character, no location-as-architecture; the product itself is the locked subject). Section ordering inside the H3 follows the source material's order: locks → composition → surface → capture → negative space.
  - Sub-bullet: Multi-view product layout — eight orthographic views (front / back / left / right / top / bottom / 3-quarter) plus macro close-ups. Parallel to the Five-View Location Sheet at `skills/higgsfield-cinema/SKILL.md:575` but adapted for product geometry — eight views vs. five because the camera is closer and the geometry IS the subject.
  - Sub-bullet: **Material Realism** block — reusable six-axis template (raised structure, tight density, visible direction, micro shadowing, surface compression following form, curvature integration) populated per material. Generalized so the same scaffold carries to leather / knit / satin / brushed metal / suede; embroidery populates the six axes for the hat worked example below as one instance of the template.
  - Sub-bullet: `#DCDCDC` light gray background + shadowless lighting + no gradients + no reflections — product-photo studio convention. Specified as a four-constraint package because the `#DCDCDC` value alone still leaves the model room for atmospheric noise. Factual prescription, lands as-is.
  - Sub-bullet: Canon EOS R5 + RF 100mm f/2.8L Macro IS USM (f/8, ISO 100) — default camera package for Product Reference Sheets. Utilitarian technical spec, not promotional positioning (consistent with v3.6.5 marketing-strip discipline, which targeted "class-leading" / "best-in-class" language, not concrete instrument specs). Substitution guidance included for shallow-DoF macro (f/4) and oversized-product (RF 50mm) cases.
  - Sub-bullet: **Hat worked example** — black baseball cap with embroidered wordmark, demonstrating the full 7-part scaffold with the Material Realism block populated by embroidery vocabulary (raised thread structure, tight stitch density, visible thread direction, micro shadowing in stitch valleys, fabric compression around stitching, curvature integration following the pre-curved crown). Formatted as `#### Hat — Worked Example` per the existing H4 sub-category pattern at `skills/higgsfield-cinema/SKILL.md:282-313`.
  - Sub-bullet: One row appended to the Reference Sheet Family summary table at `skills/higgsfield-cinema/SKILL.md:700` — `| Product | Product geometry, branding placement, material/surface, multi-view layout | This section |`. Five other table rows unchanged.
  - Sub-bullet: One-phrase additive amendment to the section intro's axis enumeration at `skills/higgsfield-cinema/SKILL.md:622` — append `, or product` to the existing `identity, architecture, motion behavior, wardrobe, or palette` list. Same kind of edit as v3.7.1's `SUB_SKILL_DESCRIPTIONS` line refresh: enumeration update to reflect new content, not a re-wording of an existing claim. Bare axis name to match the pattern of the other five entries.

### Changed

- **Frontmatter version bumps** — root `SKILL.md` 3.7.1 → 3.7.2; `skills/higgsfield-cinema/SKILL.md` 3.2.0 → 3.3.0 (minor bump for new H3 sub-section + new table row, matching v3.7.1 `higgsfield-camera` 3.0.0 → 3.1.0 precedent for content additions). `updated` fields set to 2026-05-11 (root SKILL.md `updated` unchanged at 2026-05-11 — same day as v3.7.1).
- **`validate_user_guide.py` DEFAULT_BASELINE re-baselined** — `USER-GUIDE.pdf.baseline-v3.7.1` → `USER-GUIDE.pdf.baseline-v3.7.2`. Re-baseline required because of the version-string delta cascade through deflate-compressed PDF object streams (Layer 1 text-extract content is byte-identical after pattern normalization — see Notes). Baseline-management discipline from v3.7.1: the new `USER-GUIDE.pdf.baseline-v3.7.2` is committed to git alongside this release.

### Sourcing

- **Product Reference Sheet** — sourced from File 06 (`PRODUCT REFERENCE SHEET PROMPTS.txt`, ~395 lines) and File 07 Part 1 (slides 1–6 of `Reference Workflow_.pdf`) of the 2026-05-11 `NEW DOCS_5_3_2026` audit (`/tmp/higgsfield-audit-2026-05-11/AUDIT.md` row 3, recommendation INTEGRATE — strong fit with drift catalog item D7's Reference Sheet Types surface, extending it with a Product axis). D7's other items (v3.6.0 Reference Sheet Types expansion + v3.6.4 piano test / Action Design / Morph-Cut breathing room) were already reflected in the live cinema SKILL.md at v3.7.1 release time and are unaffected. Paraphrased content only per File 06 IP discipline — short technical phrases (camera spec, hex color, sheet type name, the six Material Realism axis labels, embroidery realism vocabulary) are factual prescriptions, not paraphrasable, and land as-is.

### Notes

- **Deferred from File 06 to a later release.** (a) The "Automatic Prompt Creator" meta-prompt — a reusable LLM-side prompt-conversion assistant that takes the global template + N images and outputs a product-specific final prompt — is qualitatively a new repo pattern (meta-prompts that build other prompts) and its right home is not yet decided (candidates: `higgsfield-prompt`, `higgsfield-assist`, or a dedicated sub-section of `higgsfield-cinema`). Deferring lets v3.7.2 stay single-arc. (b) The dress worked example from File 06 — hat alone demonstrates the full 7-part scaffold with the Material Realism block populated for embroidery; a second example would be additive density without semantic gain. Both candidates for a future content release.
- **Additive-only release.** No restructuring of pre-v3.7.2 content. No re-wording beyond the one-phrase axis-enumeration append at `skills/higgsfield-cinema/SKILL.md:622` (treated same as v3.7.1's `SUB_SKILL_DESCRIPTIONS` refresh — enumeration extension, not a reword of any existing claim). Single sub-skill touched: `higgsfield-cinema`. No new sub-skills, no routing changes, no edits to other skill files. `vocab.md` untouched — it does not enumerate reference sheet types, so the new Product type doesn't surface there.
- **Drift catalog status.** D7 extended with the Product axis (Product Reference Sheet content now in repo). D3 / D4 / D5 / D6 / D8 remain open.
- **`USER-GUIDE.pdf` regenerated** by `generate_user_guide.py`. Build-time invariant passes trivially (`SUB_SKILL_DESCRIPTIONS` keys unchanged — cinema's editorial summary doesn't enumerate sheet types, so adding a 6th sheet doesn't tip the entry, so no edit needed). Validator baseline rotated: v3.7.1 → v3.7.2. Layer 1 text-extract diff prediction: zero substantive content diffs (Section 22 cinema row text stays byte-identical because no `SUB_SKILL_DESCRIPTIONS` change); only version-string deltas (v3.7.1 → v3.7.2) which the validator's normalization patterns absorb. Date string deltas: zero (same-day release as v3.7.1). Layer 2 binary diff: expected to cascade through deflate-compressed object streams as it did v3.7.0 → v3.7.1.
- **No sub-skill content moved or removed. No routing changes. No new sub-skills.**

Commit prefix: `feat: v3.7.2 — Product Reference Sheet as 6th reference-sheet type (D7 net-new Product axis)`

## v3.7.1 — 2026-05-11

### Added

- **Video Reference Capability Surface** section in `skills/higgsfield-camera/SKILL.md` — new top-level H2 "Video Reference — What It Reads, and What It Can't" documenting what a `@Video` reference reads reliably vs. less reliably, the four tagging patterns by purpose (world / action energy / camera+production / voice+performance), the three hard limits, and the load-bearing rule "prompt wins on action, reference wins on texture and world feel." Pair-with-image rule for character identity added. Repo previously documented `@Video` usage in 8+ places but never the capability/limit boundary.
  - Sub-bullet: one-line cross-link added in `skills/higgsfield-motion/SKILL.md` § @Video Reference as Primary Method pointing at the new capability surface.
  - Sub-bullet: `SUB_SKILL_DESCRIPTIONS["higgsfield-camera"]` in `generate_user_guide.py` updated from `"Camera controls + One-Move Rule + Smart Mode"` → `"Camera controls + One-Move Rule + Smart Mode + @Video reference"` to reflect the new H2 in Section 22's sub-skill table. Length stays inside the existing column width (65 chars vs. longest existing entry at 70 chars — no PDF row wrap).
- **Image Reference Notations disambig block** in `vocab.md` — new H3 "Image Reference Notations — `@Image1` vs `<<<image_1>>>`" under Platform Feature Vocabulary explaining `@Image1` as the platform-side reference syntax used in actual prompts vs. `<<<image_1>>>` as the Seedance 2 Skill's internal explicit-reference notation (per `docs/Seedance 2 Skill.md:178`). Both refer to the same underlying @-reference mechanic; bracket style is contextual to which surface is being addressed.

### Changed

- **`validate_user_guide.py` DEFAULT_BASELINE re-baselined** — `USER-GUIDE.pdf.baseline-v3.7.0` → `USER-GUIDE.pdf.baseline-v3.7.1`. (Note: the previous `DEFAULT_BASELINE` path at v3.7.0 time pointed at `USER-GUIDE.pdf.baseline-v3.6.5`, but that file was never committed and not present on disk at v3.7.1 release time. Phase 2D reconstructed the v3.7.0 PDF deterministically from the `v3.7.0` tag and used it as the rotation baseline.) Re-baseline is required because the `SUB_SKILL_DESCRIPTIONS` update changes the Section 22 `higgsfield-camera` row text — a substantive content diff per `validate_user_guide.py:48` ("Sub-skill row description changes (Section 22 second column)"). The re-baseline workflow is exactly the one anticipated in the v3.7.0 validator docstring lines 54-59 for intentional content updates.
- **Frontmatter version bumps** — root `SKILL.md` 3.7.0 → 3.7.1; `skills/higgsfield-camera/SKILL.md` 3.0.0 → 3.1.0 (minor bump for new H2); `skills/higgsfield-models/SKILL.md` 3.0.1 → 3.0.2 (patch — child-doc `MODELS-DEEP-REFERENCE.md` Rule-of-12 citation, per v3.6.5 parent-tracks-child precedent at CHANGELOG L61). `skills/higgsfield-motion/SKILL.md` — `updated` field refreshed only, no version bump (one-line cross-link, per v3.6.4 pipeline precedent at CHANGELOG L107). All `updated` fields set to 2026-05-11.

### Sourcing

- **Video Reference Capability Surface** — sourced from File 07 part 2 of the 2026-05-11 `NEW DOCS_5_3_2026` audit (`/tmp/higgsfield-audit-2026-05-11/AUDIT.md` row 4, recommendation INTEGRATE — high value, low cost).
- **Rule of 12 — ByteDance / BytePlus citation** added at the canonical Rule of 12 definition (`skills/higgsfield-models/MODELS-DEEP-REFERENCE.md` § The Rule of 12 — Asset Budget, line 274). Sources the 9-image / 3-video / 3-audio limit to official Seedance launch materials at `seed.bytedance.com`. Canonical-only placement: the 4 other repo mentions of "Rule of 12" are brief uses of a now-sourced term, not independent claims, and adding inline citations at each would partially reverse the v3.6.5 marketing-copy strip discipline. Forward compatibility: future limit updates have one source of truth to drift.
- **Image Reference Notations disambig** — sourced from AUDIT.md topline observation 9 and Row 3 net-new content note.

### Notes

- **Additive-only release.** No restructuring of existing sections. No re-wording of pre-v3.7.1 content beyond the citation lines and the `SUB_SKILL_DESCRIPTIONS` entry refresh.
- **No drift catalog items closed.** D3-D8 from the v3.7.0 deferred-content track remain open — File 07 part 2 is fresh scope not covered by D3-D8.
- **`USER-GUIDE.pdf` regenerated** by `generate_user_guide.py` after the `SUB_SKILL_DESCRIPTIONS` update. Validator baseline rotated: v3.7.0 reconstructed in a worktree at the `v3.7.0` tag (deterministic regen per Path B refactor; `pdf.set_creation_date` pinned via `META['updated']` produces byte-equivalent output) and used as the rotation baseline. Layer 1 text-extract diff v3.7.0 → v3.7.1 produced one intentional substantive diff (Section 22 `higgsfield-camera` row text update); version/date deltas pattern-normalized. New baseline `USER-GUIDE.pdf.baseline-v3.7.1` and reconstructed `USER-GUIDE.pdf.baseline-v3.7.0` (kept as historical reference) committed to git this release — closing a v3.7.0 baseline-management gap surfaced during Phase 2D (the v3.6.5 baseline file referenced by `validate_user_guide.py:93` at v3.7.0 time was never committed and not present on disk at v3.7.1 release time).
- **Baseline-management discipline closed.** Baseline files are now committed to git alongside the release that produced them, matching the existing tracking pattern for `USER-GUIDE.pdf` (tracked since v3.0.0). `validate_user_guide.py` docstring updated to note this. The "PDF tracks version" invariant from v3.7.0's Path B refactor now has a corresponding "baseline is tracked" invariant. This surprise cannot recur.
- **`higgsfield-motion` `updated`-only refresh rationale.** The one-line cross-link pointing at the new capability surface in `higgsfield-camera` does not change what the `higgsfield-motion` sub-skill teaches — the @Video Reference section there remains the action-specific primary method, with a pointer to the capability surface for broader context. Per the v3.6.4 pipeline precedent (CHANGELOG L107), single one-line cross-links are tracked via `updated`-date refresh without a version bump.
- **No sub-skill content moved or removed. No routing changes. No new sub-skills.**

Commit prefix: `feat: v3.7.1 — Video Reference Capability Surface + Rule-of-12 ByteDance citation + @image syntax disambig`

## v3.7.0 — 2026-05-04

### Changed

- **`generate_user_guide.py` Path B refactor (Option D scope)** — version metadata + sub-skill list parameterization. Eliminates the manual sync burden that left the PDF six releases stale by v3.6.1. Specifically:
  - Sub-bullet: New `read_root_metadata()` helper parses root `SKILL.md` frontmatter for `version`, `updated`, `author`. Custom 30-line stdlib-only parser; no new dependencies (script remains `fpdf`-only on the third-party side).
  - Sub-bullet: New `discover_sub_skills()` helper walks `skills/*/` for SKILL.md presence; excludes `shared/` utility directory.
  - Sub-bullet: New `SUB_SKILL_DESCRIPTIONS` dict at top of script holds the editorial summaries for the Section 22 sub-skill table — preserves v3.6.5 byte-for-byte equivalence (frontmatter `description:` fields are routing-trigger language, not editorial summaries; using them would be a content regression).
  - Sub-bullet: Build-time invariant check: filesystem-discovered sub-skill set must equal `SUB_SKILL_DESCRIPTIONS.keys()`; mismatch raises with a clear "update the dict" error message. **Catches the staleness scenario** (a new sub-skill was added without updating the PDF) at build time instead of letting the PDF silently drift.
  - Sub-bullet: 5 hardcoded version strings replaced with `META['version']` references (line 16 header, line 139 cover, line 743 FAQ Q5, line 763 footer; module docstring rewritten without inline version).
  - Sub-bullet: Hardcoded date strings (line 139 cover, line 763 footer) replaced with `META['updated']`.
  - Sub-bullet: Hardcoded author string ("O-Side Media", lines 139 + 763) replaced with `META['author']`.
  - Sub-bullet: PDF creation date pinned via `pdf.set_creation_date(datetime.fromisoformat(META['updated']))` for reproducible binary builds (FPDF2's default embeds wall-clock time in `/CreationDate`, breaking binary diff).
  - Sub-bullet: Section 22 "Sub-Skills (20 total)" count is now `f"Sub-Skills ({len(SUB_SKILL_DESCRIPTIONS)} total)"` — auto-updates when a new sub-skill is added.
  - Sub-bullet: **Root-files table at Section 22 kept hardcoded.** Set is small, stable, descriptions are editorial; dynamic walk would either break byte-for-byte (by including all root .md/.py/.pdf files) or require an allowlist (defeating the purpose). Cost-of-hardcoded ≈ zero, value-of-dynamic ≈ near-zero for this case.
- **FAQ Q5 staleness bug fix** — line 743 said "currently v3.0.0" since pre-v3.6.2 (wrong even within the v3.6.2 build). Now parameterized via `META['version']`, reads "currently v3.7.0" in this build and tracks every future release.
- **New repo file: `validate_user_guide.py`** — lightweight (~190 lines including methodology docstring) validation script. Three-layer validation: build-time invariants (in-script raises), text-extract diff (`pdftotext -layout` or `pdfplumber` fallback) against a frozen baseline PDF with version/date/count patterns normalized away, and binary diff (post-timestamp-pinning, informational). Run before any future PDF regeneration to catch unintended drift. Opens with a methodology docstring documenting what counts as an allowed change vs a regression so future maintainers can read the script's purpose without reverse-engineering the regex patterns.
- **`USER-GUIDE.pdf` regenerated** by the refactored script. Layer 1 text-extract diff against frozen v3.6.5 baseline: PASS (zero substantive content regressions after normalizing version/date/count patterns). Layer 2 binary diff: bytes differ throughout the PDF's compressed object streams — expected behavior, since small text changes (v3.6.5 → v3.7.0, 2026-04-25 → 2026-05-04) cascade through deflate-compressed streams shifting many byte positions. Page count unchanged at 19 pages.
- **Backlog cleanup in `docs/pdf-audit/AUDIT-REPORT-v3.6.0.md`** — section header re-labeled "v3.6.5+ planning" → "v3.7.0+ planning". Path B refactor row struck with closure annotation. USER-GUIDE comprehensive expansion row stays open with a v3.7.1+ note that explicitly enumerates the drift catalog (D3-D8) as the v3.7.1+ content scope. AI director toggle row remains open (BLOCKED — function unverified).
- **Frontmatter version bump** — root `SKILL.md` 3.6.5 → 3.7.0. `updated` field unchanged at 2026-05-04 (same-day release). No sub-skill frontmatter bumps — refactor is build-tooling only, no sub-skill content changed.

### Sourcing

- Path B refactor — sourced from the original 2026-04-25 v3.6.0 audit observation that the PDF was 6 releases stale; tracked as MEDIUM-priority backlog row across v3.6.x. Scope locked to Option D after structural read of the existing 770-line generator surfaced architectural cost asymmetries between options.

### Notes

- **Option D scope rationale (why not Option B).** The structural read of `generate_user_guide.py` recalibrated the audit's "~3-4 hours" estimate against four viable refactor shapes: Option A (metadata-only, ~2h), Option D (Option A + sub-skill enumeration, ~1.5-2h), Option C (hybrid with content-in-YAML, ~3-4h), and Option B (full SKILL.md parsing with custom markdown→FPDF renderer, ~10-15h). The audit's estimate was calibrated for Option C scope but described Option B language. Option B's true cost (markdown parser + table-width pinning + 5 synthesized sections without SKILL.md homes + heading-anchor stability + ongoing maintenance burden) significantly exceeds the value delivered by Option D for the *concrete* staleness problem (version metadata + sub-skill count). Option D ships the cheapest refactor that solves the staleness pain that motivated the row.
- **What's deferred to v3.7.1+ (drift catalog).** v3.7.0 ships v3.6.5-equivalent PDF content (byte-for-byte except metadata bytes after pattern normalization). Content drift between the PDF and current SKILL.md content remains, catalogued during scoping as items D3 through D8: Cinema Studio 3.5 selection guide unreflected; the 5 Seedance prompt modes (incl. v3.6.4 Transformation prompt mode) unreflected in Section 10; v3.6.3 Soul Cinema and v3.6.4 Studio Look re-pass unreflected in Section 11; v3.6.4 Iteration Rule + 6-Pass Diagnostic Sequence unreflected in Section 18; v3.6.0 Reference Sheet Types and v3.6.4 piano test / Action Design / Morph-Cut breathing room unreflected in Section 21; sub-skill row descriptions unreflected for v3.6.4 additions in Section 22. **All deferred to v3.7.1+** as content-expansion work, not refactor scope.
- **`refactor:` introduced as fourth Conventional Commits prefix** in repo history. Prior prefixes: `feat:` (v3.4.0–v3.6.0, v3.6.3, v3.6.4 — new content arcs), `chore:` (v3.6.1 — config), `docs:` (v3.6.2, v3.6.5 — content polish). `refactor:` semantics: code reorganization that does not change observable behavior or content. v3.7.0 fits — the generated PDF's content is byte-equivalent to v3.6.5 (per Layer 1 text-extract diff after pattern normalization) except for metadata bytes (which the refactor itself fixes as a deliberate change, not a regression).
- **Validation results.** Layer 1 text-extract diff against frozen v3.6.5 baseline: PASS — zero substantive differences flagged after normalizing version/date/count patterns. Layer 2 binary diff: 28247 byte positions differ in a 33648-byte file — expected behavior because PDF deflate-compressed object streams cascade-shift on small text changes; Layer 1 is the authoritative content check. No content regressions. No layout shifts (page count unchanged at 19).
- **Build-time staleness protection.** Future releases that add a new sub-skill will trigger the filesystem-vs-`SUB_SKILL_DESCRIPTIONS` invariant check at build time, raising with a clear error message. The PDF cannot silently drift on the sub-skill list anymore.
- **No sub-skill content changed. No new sub-skills, no routing changes, no SKILL.md edits beyond the root frontmatter version bump.**

Commit prefix: `refactor: v3.7.0 — generate_user_guide.py Path B refactor (Option D — metadata + sub-skill list parameterization)`

## v3.6.5 — 2026-05-04

### Changed

- **Marketing-copy strip on `skills/higgsfield-models/MODELS-DEEP-REFERENCE.md`** — file-wide style normalization removing product-marketing language while preserving all capability and routing information. Nine surgical edits:
  - Sub-bullet: `### Kling 3.0 ⭐ EXCLUSIVE — Current Top Model` → `### Kling 3.0` (plan-availability badge + promotional positioning stripped; `Best for:` and `Strengths:` lines below carry the routing info)
  - Sub-bullet: `### Kling 3.0 Omni ⭐ EXCLUSIVE` → `### Kling 3.0 Omni`
  - Sub-bullet: `### Kling 3.0 Omni Edit ⭐ EXCLUSIVE` → `### Kling 3.0 Omni Edit`
  - Sub-bullet: `### Kling 3.0 Motion Control ⭐ NEW (March 25, 2026)` → `### Kling 3.0 Motion Control (added March 25, 2026)` (`⭐ NEW` temporal marketing stripped; date reframed as factual provenance)
  - Sub-bullet: Sora 2 Strengths line — `Best-in-class for large-scale events` → `Strongest at large-scale events` (canonical kept-form per the strip rule: "Strongest at X" preserves capability claim without superlative positioning)
  - Sub-bullet: Kling 2.6 audio capabilities header — `**Audio capabilities (class-leading at this tier):**` → `**Audio capabilities:**` (parenthetical superlative stripped; bulleted capability list below carries the routing info)
  - Sub-bullet: Aurora text/logos strength row — `One of Aurora's top differentiators — most models fail here` → `Where Aurora outperforms most models — most models fail here` (positioning language stripped; capability claim preserved verbatim)
  - Sub-bullet: Video Imagine 1.0 — vendor-quoted `"best-in-class instruction following for video generation"` bullet removed entirely (quoted vendor marketing carries no routing info; adjacent bullets carry capability content)
  - Sub-bullet: Nano Banana Pro Strengths line — `Best image quality on the platform` → `Strongest image quality on the platform`
- **Cross-file marketing-copy strip in `skills/higgsfield-apps/SKILL.md`** — line 117 `Cinema Studio is Higgsfield's premium filmmaking environment` → `Cinema Studio is Higgsfield's professional filmmaking environment`. Matches the precedent in `skills/higgsfield-cinema/SKILL.md` (which already uses "professional filmmaking environment" in the equivalent slot).
- **Audio-block diversity pass on the five Seedance 2.0 worked examples in `prompt-examples.md`** — v3.6.4 shipped all five examples with the same audio-block compositional shape (primary action + environmental texture + distant element + low/no music indicator). v3.6.5 varies the shapes one-to-one across the five examples:
  - Sub-bullet: Underground Parking Pursuit (Action) — **foreground-heavy** shape (close-mic'd breath and stride detail leading; environmental sound demoted with attenuation cues)
  - Sub-bullet: Hospital Vigil II (Drama) — **music-foregrounded** shape (single sustained low cello note as structural element, swelling through the emotional break; diegetic sound recedes beneath it; no spoken dialog added)
  - Sub-bullet: Derelict Station Approach (Sci-Fi) — **sound-design-anchored** shape (audio framed as designed/constructed/treated rather than captured; SFX-design vocabulary throughout: treated drone, constructed hull groans, EQ'd helmet breath)
  - Sub-bullet: Coffee Beans — Label Iteration (Product) — **ambient-heavy** shape ("same as source" Edit Shot framing preserved; kitchen ambience layered as primary content with refrigerator hum, traffic, air; foreground sounds placed *inside* the ambience)
  - Sub-bullet: Awakening II (Transformation) — **dialog-anchored as wordless vocal performance** shape (her hum anchors the scene with timbre/dynamic/transformation-arc detail; surrounding sound recedes; no spoken-word content — the vocal performance is wordless throughout)
- **Backlog cleanup in `docs/pdf-audit/AUDIT-REPORT-v3.6.0.md`** — section header re-labeled "v3.6.4+ planning" → "v3.6.5+ planning"; two rows struck with closure annotations (marketing-copy strip closed by Item A above; audio-block diversity closed by Item B above). Three rows remain open: AI director toggle behavioral documentation (BLOCKED — function unverified), Path B generator refactor (v3.7.x+), USER-GUIDE comprehensive expansion (v3.7.x+).
- **Frontmatter version bumps** — root `SKILL.md` 3.6.4 → 3.6.5; `skills/higgsfield-models/SKILL.md` 3.0.0 → 3.0.1; `skills/higgsfield-apps/SKILL.md` 3.0.0 → 3.0.1. All `updated` fields set to 2026-05-04. Patch-level bumps on the two sub-skills because the changes are content-polish style normalization, not feature additions.

### Sourcing

- Marketing-copy strip — sourced from the original 2026-04-25 v3.6.0 review observation, tracked as a backlog row (LOW priority) since v3.6.0. Strip rule applied per Peter's clarification: strip product-marketing modifiers (plan-availability badges like ⭐ EXCLUSIVE, promotional positioning like Current Top Model, superlative claims like best-in-class / class-leading / top differentiators); keep capability and routing language ("Strongest at X" claims, technical specs, concrete capability descriptors).
- Audio-block diversity pass — sourced from the 2026-05-03 v3.6.4 release review note, tracked as a v3.6.5+ backlog row added during v3.6.4 cleanup. Five-shape taxonomy applied: foreground-heavy / music-foregrounded / sound-design-anchored / ambient-heavy / dialog-anchored.

### Notes

- **Close-out cleanup release.** v3.6.5 closes the two remaining LOW-priority backlog rows from the v3.6.0 audit + v3.6.4 cleanup. After this release, the only open items in `docs/pdf-audit/AUDIT-REPORT-v3.6.0.md` are the BLOCKED AI director toggle row and two v3.7.x+ planned items (Path B refactor + USER-GUIDE expansion). The v3.6.x cycle is content-complete.
- **Strip rule sharpened during scoping** — "premium" stripped when it's a plan-tier marketing modifier on the platform itself (one cross-file hit in `higgsfield-apps/SKILL.md`); kept when it's workflow vocabulary describing model cost tiers within a routing pipeline (e.g., `higgsfield-pipeline/SKILL.md` Stage 8 routing pseudocode, `higgsfield-assist/SKILL.md` cost-tier guidance). Both retained-context hits preserved verbatim.
- **No cross-file false positives.** Wider repo scan surfaced one anti-pattern *example* in `templates/02-product-ugc-showcase.md` (`"Measurable lighting — not 'looks premium'"`) and one anti-slop vocabulary list in `docs/Seedance 2 Skill.md` — both are documentation *against* marketing language and were preserved.
- **Audio-block stylistic discipline.** Each new audio block demonstrates its named shape through composition rather than enumeration — a reader can read the shape off the prose without needing the label. Foreground/background mix structure made explicit via attenuation cues; designed audio flagged with SFX-design vocabulary; musical structure tied to scene emotional read.
- **B2 wordless preserved.** Hospital Vigil II remains wordless after the diversity pass — the v3.6.4 example's narrative content (a wordless emotional beat between husband and unconscious wife) is preserved; the diversification works at the audio-mix level only, with a sustained cello carrying what dialog would otherwise carry.
- **No new sub-skills, no new content arcs, no routing changes.** Surgical content polish only.

Commit prefix: `docs: v3.6.5 — marketing-copy strip on MODELS-DEEP-REFERENCE.md + audio-block diversity pass on Seedance worked examples`

## v3.6.4 — 2026-05-03

### Added

- **6-Pass Diagnostic Sequence subsection** in `skills/higgsfield-prompt/SKILL.md` — new `### When You Don't Know What's Wrong Yet — the 6-Pass Diagnostic Sequence` h3 inserted into the existing Iteration Rule section. Six-variable diagnostic sequence (subject → action → camera → style → audio → output) for finding which variable to change when the Iteration Rule's "pick the one that's wrong" can't be answered yet. Frames the 6-Pass as a finder, not a refinement loop — once the variable is identified, the Iteration Rule takes over.
  - Sub-bullet: PDF order preserved verbatim (subject / action / camera / style / audio / output).
  - Sub-bullet: cross-link added in `skills/higgsfield-seedance/SKILL.md` Related Skills section pointing back at the new subsection.
- **Transformation prompt mode** added to `skills/higgsfield-seedance/SKILL.md` — fifth mode in the Seedance 2.0 Prompt Modes catalog, alongside Reference-Based, Continuation, Expand Shot, and Edit Shot. Describes a state change inside a single clip (distinct from Continuation, which extends time across two clips, and Edit Shot, which patches a generated clip after the fact).
  - Sub-bullet: section opener at L80 updated from "four generation modes" → "five generation modes".
  - Sub-bullet: Mode Selection Rule paragraph extended with Transformation routing logic.
  - Sub-bullet: full prose phrase "Transformation prompt mode" used wherever ambiguity with the existing Transformation genre in `prompt-examples.md` is possible. One-line disambiguation gloss added to the top of the `prompt-examples.md` Transformation genre section.
- **Action Design Rules subsection** in `skills/higgsfield-cinema/SKILL.md` — new `### Action Design Around AI Strengths` h3 appended to the (renamed) Fight Scene & Action Design Rules section. Adapted from the Mr. Core methodology — covers location selection (forgiving vs. punishing spaces), choreography around model strengths, the one-transformation-per-shot rule, and single-generation strategy.
- **Morph-Cut breathing room** in `skills/higgsfield-cinema/SKILL.md` Multi-Shot Manual subsection — explicit 2-second still-or-near-still moments at the start and end of every shot to give editors morph-cut and smooth-cut landing points. Adapted from the Mr. Core methodology.
- **The piano test** in `skills/higgsfield-cinema/SKILL.md` Outfit/Material Sheet subsection — wardrobe complexity has a generation cost; if a wardrobe element is as visually demanding as a piano in the frame, the model spends its budget rendering it instead of the action. Strip wardrobe to the simplest silhouette that reads as the character. Adapted from the Mr. Core methodology.
- **Studio Look vs. Cinematic Look — Soul Cinema as the Re-Pass** subsection in `skills/higgsfield-soul/SKILL.md` — new h3 inside the existing Soul Cinema as the CS 3.0/3.5 Default Image Model section. Diagnoses the studio look (clean / evenly lit / glossy / plastic-feeling), prescribes the re-pass workflow through Soul Cinema with explicit grade / lighting / lens / palette direction. Adapted from the Mr. Core methodology. Includes explicit gloss disambiguating "studio look" (visual quality of output) from "Cinema Studio" (the product).
- **Five Seedance 2.0 worked examples** added to `prompt-examples.md` — one per chosen genre, each with full audio block as a first-class element:
  - Sub-bullet: Action → Underground Parking Pursuit (Reference-Based mode)
  - Sub-bullet: Drama → Hospital Vigil II (Continuation mode)
  - Sub-bullet: Sci-Fi → Derelict Station Approach (Reference-Based mode)
  - Sub-bullet: Product/Commercial → Coffee Beans — Label Iteration (Edit Shot mode)
  - Sub-bullet: Transformation → Awakening II (Transformation prompt mode)
- **Three template cross-links** in `templates/01-cinematic-action-chase.md`, `templates/02-product-ugc-showcase.md`, `templates/05-sci-fi-vfx.md` pointing at the new Seedance worked examples in `prompt-examples.md`.

### Changed

- **Section rename in `skills/higgsfield-cinema/SKILL.md`** — "Fight Scene Rules (Tested)" → "Fight Scene & Action Design Rules (Tested)" to accommodate the new Action Design subsection.
- **One-line cross-link in `skills/higgsfield-pipeline/SKILL.md` Stage 8 — Assembly** pointing at the Morph-Cut breathing room rule for cut-friendly source-material generation.
- **Backlog cleanup in `docs/pdf-audit/AUDIT-REPORT-v3.6.0.md`** — section header re-labeled "v3.6.3+ planning" → "v3.6.4+ planning"; eight rows struck (the four Mr. Core sub-concepts shipped here, the 6-Pass Testing Protocol gap-check, the Transformation prompt mode, the Seedance worked-example library, and the stale Per-Cinematic-model deep workflow guidance row that v3.6.3 already closed). Three rows remain open (AI director toggle BLOCKED, product-marketing language strip LOW, Path B refactor + USER-GUIDE expansion v3.7.x+); one new row added (audio-block diversity pass — see Notes).
- **Frontmatter version bumps** — root `SKILL.md` 3.6.3 → 3.6.4; `skills/higgsfield-prompt/SKILL.md` 3.1.0 → 3.2.0; `skills/higgsfield-seedance/SKILL.md` 1.0.0 → 1.1.0; `skills/higgsfield-cinema/SKILL.md` 3.1.0 → 3.2.0; `skills/higgsfield-soul/SKILL.md` 3.1.0 → 3.2.0. `skills/higgsfield-pipeline/SKILL.md` updated-date refreshed only (single one-line cross-link, no version bump). All `updated` fields set to 2026-05-03.

### Sourcing

All four content arcs are sourced from `docs/pdf-audit/AUDIT-REPORT-v3.6.0.md` — the GAP candidates flagged for v3.6.1+ deferral during the v3.6.0 audit. No new external source material this release; this is the deferred-backlog payoff release.

- 6-Pass Diagnostic Sequence — Seedance 2.0 Prompt Modes slide deck item 8 + Seedance Promt modes prose handbook (sibling pair, GAP/PENDING-CHECK in v3.6.0 audit).
- Transformation prompt mode — Seedance 2 Serious Examples Supplement item 9 (GAP/deferred in v3.6.0 audit).
- Seedance 2.0 worked-example library — Seedance 2 Serious Examples Supplement (REINFORCE-only in v3.6.0 audit, integrated as worked illustrations of existing patterns).
- Mr. Core methodology (4 sub-concepts) — Building a Cinematic Universe Mr. Core long-form items 3, 4–6 (collapsed to "Action choreography"), 7, 8 (GAPs in v3.6.0 audit).

The v3.6.0 audit flagged the 6-Pass as PENDING-CHECK — the gap-check verdict is recorded above as PARTIAL GAP: the Iteration Rule covers the single-variable principle; the 6-Pass adds a prescribed diagnostic order and includes audio + output axes the Iteration Rule does not name. The 6-Pass therefore ships as a subordinate diagnostic tool inside the Iteration Rule section, not as a competing rule.

### Notes

- **Largest release in repo history.** Bundles four unrelated arcs into one merge — a 6-pass diagnostic, a fifth Seedance prompt mode, a Mr. Core methodology pass distributed across cinema and soul, and a Seedance worked-example library expansion. Total ~5–6 hours of content work; release process overhead handled separately.
- **Distributed Mr. Core placement.** Methodology integrated where each piece lands most naturally — Action Design + Morph-Cut breathing room + piano test in `higgsfield-cinema`, Studio→Cinematic re-pass in `higgsfield-soul`, lightweight cross-link from `higgsfield-pipeline` Stage 8. No "Mr. Core" in any section header; attribution lives in body text only ("adapted from the Mr. Core methodology").
- **"Studio look" disambiguation.** First appearance of the term in `higgsfield-soul` includes an explicit gloss distinguishing the visual-quality sense ("studio-feeling output") from the Cinema Studio product. Full phrasing — "studio look," "studio-feeling" — used throughout the new content; bare "studio" avoided where it could be confused.
- **Templates cross-link gap.** Only 3 of the 5 chosen Item 3 genres (Action, Product/Commercial, Sci-Fi) have corresponding files in `templates/`. Drama and Transformation templates do not exist; Item 3 cross-links those two genres only inside `prompt-examples.md`, not in `templates/`. New Drama / Transformation templates deferred — earn their own future release if the gap stays felt.
- **No v3.6.0 Cinema Studio framing changes.** Studio-look disambiguation lives entirely in new content; no concurrent edits to existing Cinema Studio 3.5 sections.
- **No new sub-skills, no routing changes, no Featured-models documentation drift.**
- **Audio-block diversity pass deferred** — all five Seedance worked examples use the same compositional shape (primary action + environmental texture + distant element + low/no music indicator). A future release could vary this with foreground-heavy, ambient-heavy, music-foregrounded, dialog-anchored, or sound-design-anchored audio shapes. Tracked as v3.6.5+ backlog.

Commit prefix: `feat: v3.6.4 — Mr. Core methodology + Seedance 5th prompt mode + 6-Pass + Seedance worked examples`

## v3.6.3 — 2026-04-25

### Added

- **Per-Cinematic-model selection guide subsection** in `higgsfield-cinema/SKILL.md` — new `#### Per-Cinematic-model selection guide` h4 inserted between the resolution table and the existing Cinematic Cameras h4. Covers Soul Cinema (the default), Cinematic Characters (expressive faces and styling), and Cinematic Locations (environments and atmosphere) with 1–2 paragraphs each on when to pick the model, what intent it serves, and what to use it for vs avoid. The existing Cinematic Cameras h4 remains in place as the fourth per-model dive.
- **Soul Cinema subsection in `higgsfield-soul/SKILL.md`** — new `## Soul Cinema as the CS 3.0/3.5 Default Image Model` subsection with Soul ID identity-anchor prompting pattern adapted for image mode (Identity Block + Scene/Style Block, since image generation has no temporal axis). Closes the v3.6.2 USER-GUIDE row description promise that previously cross-referenced Soul Cinema content the sub-skill did not have, and pays off the existing route-out from `higgsfield-cinema` line 1589.

### Changed

- **Cleanup of "deferred to a future release" hooks in `higgsfield-cinema/SKILL.md`** — picker-table h4 hook and Cinematic Cameras h4 blockquote updated to reflect that selection guidance now ships in this release. Sample prompts, Featured-models-in-image-mode framing, the Save Setup workflow, and video-mode's parallel Cinematic/Featured picker remain explicitly deferred.
- **Frontmatter version bumps** — root `SKILL.md` 3.6.2 → 3.6.3; `skills/higgsfield-soul/SKILL.md` 3.0.0 → 3.1.0 with `updated` field set to 2026-04-25; `skills/higgsfield-cinema/SKILL.md` `updated` field unchanged at 2026-04-25.

### Sourcing

No new UI verification this release. Per-Cinematic-model selection-guide content is derived from the v3.6.0 UI-verification pass (2026-04-25) that produced the original four-row picker table, plus the v3.6.2 USER-GUIDE refresh contract that promised Soul Cinema coverage in `higgsfield-soul`. The `docs/pdf-audit/AUDIT-REPORT-v3.6.0.md` gap analysis remains the source of record for the picker structure. Pipeline E references to "Soul Cinema" in `higgsfield-pipeline/SKILL.md` were verified as picker-context (post-v3.6.0 default Cinematic model), not Preview-context — the Part 1 cross-link from the Soul Cinema selection-guide entry into Pipeline E is correct.

### Notes

Selection-guide-only depth: each model gets 1–2 paragraphs covering pick / intent / use / avoid. Sample prompts specific to each Cinematic model are deferred to v3.6.4+ if the gap stays felt — `templates/` and `prompt-examples.md` already cover prompting at the genre level, and per-Cinematic-model sample prompts would partially overlap with both. Closes the v3.6.2 USER-GUIDE row description promise. Vocabulary discipline preserved: Soul Cinema / Cinematic Characters / Cinematic Locations are described without 2.5 optical vocabulary; only Cinematic Cameras inherits 2.5's Camera Body / Lens / Focal Length / Aperture stack. `model-guide.md`, `image-models.md`, `vocab.md`, and `higgsfield-pipeline/SKILL.md` left untouched — their "Soul Cinema Preview" mentions refer to the older standalone model, not the picker-context Soul Cinema. `MODELS-DEEP-REFERENCE.md` verified as exclusively Featured-model documentation in its Image Models section (Soul 2.0, Nano Banana Pro, Seedream 4.5, Flux Kontext) — left untouched.

Two LIMITED MODIFICATIONs to pre-existing skill content:

1. The deferred-hook in the picker-table h4 of `higgsfield-cinema/SKILL.md` (previously: "Per-model deep workflow guidance ... is deferred to a future release") updated to point at the new `§ Per-Cinematic-model selection guide`, with the deferral language narrowed to "sample prompts specific to each Cinematic model."
2. The deferred-hook blockquote in the Cinematic Cameras h4 of `higgsfield-cinema/SKILL.md` (previously: "Per-Cinematic-model deep workflow guidance is deferred to a future release") updated to reflect that selection guidance now ships, with the still-deferred items explicitly enumerated (sample prompts, Featured-models-in-image-mode framing, Save Setup workflow, video-mode picker coverage).

Commit prefix: `feat: v3.6.3 — per-Cinematic-model selection guide + Soul Cinema in higgsfield-soul`

## v3.6.2 — 2026-04-25

### Changed
- **README.md** updated for v3.4–v3.6 platform additions:
  - Cinema Studio 3.5 line added alongside 2.5 and 3.0
  - Cinema Studio 2.5 features list extended (Five-View Location Reference Sheet, Reference Sheet Types, Elements System library surface)
  - Seedance 2.0 best practices list extended (prompt modes, Continuation Prompt Formula, Iteration Rule)
  - Shared negative constraints line extended (Motion Control failure diagnostic, Physics Rendering Decision Matrix)
  - Model list updated with Kling 3.0 Motion Control
  - File tree updated: `higgsfield-workspaces` added (sub-skill count 19 → 20), plus `.markdownlint.json` and `docs/pdf-audit/`
  - `higgsfield-cinema` row updated with 3.5
  - Version badge bumped 3.3.0 → 3.6.2; footer date refreshed
- **USER-GUIDE.pdf** regenerated with light refresh:
  - Version metadata refreshed (`v3.0.0` → `v3.6.2`) across cover page, header, footer, and module docstring
  - Section 6 model table extended with Kling 3.0 Motion Control / Wan 2.7 / Veo 3.1 Lite
  - Section 9 Cinema Studio 3.0 closed with a brief Cinema Studio 3.5 acknowledgment paragraph + callout pointing to `higgsfield-cinema` for full coverage
  - Section 22 sub-skill table corrected from 18 → 20 (added `higgsfield-seedance` from v3.2.0 + `higgsfield-workspaces` from v3.4.0; refreshed `higgsfield-soul` and `higgsfield-cinema` row descriptions)
  - FAQ "what changed?" answer updated to summarize v3.3.0 → v3.6.2 themes and delegate full detail to CHANGELOG
- **`docs/pdf-audit/AUDIT-REPORT-v3.6.0.md`** backlog table re-labeled and re-prioritized: section header now reads v3.6.3+; "Per-Cinematic-model deep workflow guidance" priority bumped MEDIUM → HIGH (natural follow-on to v3.6.0 Image Mode subsection); two new entries added for v3.7.x+ planning (Path B generator refactor; comprehensive USER-GUIDE expansion bundled with that refactor).
- **Root `SKILL.md`** frontmatter version bumped 3.6.1 → 3.6.2 / 2026-04-25.

### Notes
- **Light refresh, not full refresh.** Deep feature documentation lives in `SKILL.md` files; the USER-GUIDE PDF is an overview artifact. Comprehensive new PDF sections for Cinema Studio 3.5 / Image Mode / Elements / Physics Matrix / Motion Control / workspace-first / Reference Sheet Types are deferred to v3.7.x+ as part of the Path B generator refactor.
- **Path B generator refactor deferred to v3.7.x+** — `generate_user_guide.py` currently hardcodes all content as Python string literals (no `SKILL.md` parsing). By v3.6.1 the PDF was 6 releases stale precisely because every release requires manual script edits. Refactoring the generator to parse `SKILL.md` files dynamically would eliminate the manual sync burden but is a substantial standalone release (~3–4 hours of refactor + validation) and should not mix with content writing.
- Pure documentation refresh. No skill content changes. No new sub-skills. No routing changes. No LIMITED MODIFICATIONs.
- Third Conventional Commits prefix in repo history (`docs:`) following `feat:` (v3.4.0–v3.6.0) and `chore:` (v3.6.1).

## v3.6.1 — 2026-04-25

### Added
- `.markdownlint.json` at repo root — config to silence intentional CHANGELOG conventions. MD022 (blanks around headings) and MD032 (blanks around lists) disabled file-wide. MD024 (no duplicate headings) refined to `siblings_only`, which allows repeated `### Added` / `### Changed` / `### Sourcing` / `### Notes` subheadings under different `## vX.Y.Z` parents — the Keep-A-Changelog pattern. MD013 (line length) also disabled for long-form bullets.

### Changed
- Root `SKILL.md` frontmatter version bumped to 3.6.1 / 2026-04-25.

### Notes
- Pure infrastructure change — no skill content, no model documentation, no behavioral change to any sub-skill. Resolves 241 pre-existing markdownlint warnings on `CHANGELOG.md` that flagged intentional repo conventions across v3.2.0 through v3.6.0.
- No new sub-skills, no routing changes, no LIMITED MODIFICATIONs.

## v3.6.0 — 2026-04-25

### Added
- **Cinema Studio 3.5 section** in `higgsfield-cinema` — three-pill main UI surface (Genre / Style / Camera), Style Settings panel three-axis preset stacking (8 Color Palette / 6 Lighting / 9 Camera Moveset Style), Manual Style free-form mode, Camera Settings four-axis panel (3 Camera Body / 5 Lens / 5 Focal Length including new 75mm / 3 Aperture), five recommended stacks, output controls (480p draft tier added, 21:9 ultrawide preserved), AI director toggle acknowledged with function deferred.
- **Image Mode subsection** in `higgsfield-cinema` — Cinema Studio 3.5 image mode coverage including the four Cinematic models picker (Soul Cinema default, Cinematic Characters, Cinematic Locations, Cinematic Cameras), Featured models acknowledgment, image-mode aspect ratios (8 options), resolution table by selected model, and disambiguation between Soul Cinema (Cinematic model) and Higgsfield Soul Cinema (Featured model).
- **Elements System extension** in `higgsfield-cinema` — five source tabs (Uploads / Image Generations / Video Generations / Elements / Liked) and six element categories (All / Pinned / Shared / Characters / Locations / Props), library-first workflow guidance, cross-shot continuity tip via Image/Video Generations tabs.
- **Physics Rendering — Resolution Decision Matrix** (cross-model section) in `higgsfield-cinema` — applies to Seedance 2.0 and Cinema Studio 3.x; routing rule for fast/chaotic motion (720p), fine-detail physics (1080p), grounded weight (1080p), and draft/exploration (480p).
- **Cinema Studio 3.5 row** added to the comparison table in `higgsfield-models/SKILL.md` (Cinema Studio version comparison) plus framing paragraph and cross-link blockquote — routing-level coverage that defers full surface documentation to `higgsfield-cinema`.
- **Built-in color grading row** in `higgsfield-models/SKILL.md` Unique Feature Matrix — Cinema Studio 3.5 added alongside Cinema Studio 2.5 with Color Palette axis (8 named palettes) callout.
- **PDF integration audit** at `docs/pdf-audit/AUDIT-REPORT-v3.6.0.md` covering eight community/creator PDFs reviewed externally on 2026-04-24/25 plus hands-on UI verification of Cinema Studio 3.5 conducted on 2026-04-25.

### Changed
- **Cinema Studio version comparison table** in `higgsfield-cinema/SKILL.md` — fourth column added for Cinema Studio 3.5 (existing 2.5 and 3.0 columns unchanged).
- **Cinema Studio version comparison table** in `higgsfield-models/SKILL.md` — fourth column added for Cinema Studio 3.5 (existing 2.5 and 3.0 columns unchanged).
- **Kling 3.0 resolution line** in `MODELS-DEEP-REFERENCE.md` — refined from `1080p + 4K HDR` to `720p / 1080p / 4K HDR` reflecting the current quality dropdown (4K was already documented; 720p added).
- **Cinema Studio 3.0 section** in `higgsfield-cinema/SKILL.md` — one-bullet Soul Cinema acknowledgment appended to the Quick Specs subsection (forward-link to the new 3.5 Image Mode subsection, since Soul Cinema is the shared default image model across 3.0 and 3.5).
- **Routing entries and sub-skill triggers** in root `SKILL.md` updated to surface Cinema Studio 3.5 (routing table first row expanded, new dedicated 3.5 routing row added, sub-skills triggers row expanded with Style Settings / Camera Settings / Manual Style keywords).
- **Root `SKILL.md` "What Is Higgsfield?" paragraph** — `Cinema Studio 2.5 and Cinema Studio 3.0` expanded to `Cinema Studio 2.5, Cinema Studio 3.0 (Business/Team plan), and Cinema Studio 3.5`.
- **Root `SKILL.md` frontmatter** version bumped to 3.6.0 / 2026-04-25.
- **`higgsfield-cinema/SKILL.md` frontmatter** version bumped from 3.0.0 to 3.1.0 / 2026-04-25 (mirrors the v3.5.0 sub-skill bump pattern).

### Sourcing
Additions informed by hands-on UI verification of Cinema Studio 3.5 conducted on 2026-04-25 plus eight community/creator PDFs reviewed externally. Full gap analysis preserved in `docs/pdf-audit/AUDIT-REPORT-v3.6.0.md`. The v3.4.0 audit report at `docs/pdf-audit/AUDIT-REPORT.md` remains the methodology template. Cinema Studio 3.5 image-mode and Cinematic models picker findings sourced from a 2026-04-25 hands-on UI verification pass that surfaced beyond the CinemaStudioRecap PDF coverage. The vocabulary-routing rule ("vocabulary follows the model you have selected") replaces an earlier draft framing that incorrectly described Cinematic Cameras as a toggle.

### Notes
- ADDITIVE-ONLY discipline preserved with **four explicit LIMITED MODIFICATIONs**:
  1. Cinema Studio version comparison table in `higgsfield-cinema/SKILL.md` extended with a 3.5 column (existing 2.5/3.0 columns untouched).
  2. Cinema Studio version comparison table in `higgsfield-models/SKILL.md` extended with a 3.5 column (existing 2.5/3.0 columns untouched).
  3. Kling 3.0 resolution line in `MODELS-DEEP-REFERENCE.md` refined from `1080p + 4K HDR` to `720p / 1080p / 4K HDR`.
  4. Cinema Studio 3.0 section in `higgsfield-cinema/SKILL.md` — one-bullet Soul Cinema acknowledgment appended to the Quick Specs subsection.
- Root `SKILL.md` frontmatter, dispatcher entries, and "What Is Higgsfield?" line updated to surface 3.5 (in-scope routine bookkeeping for a new sub-skill version, not counted as a LIMITED MODIFICATION).
- AI director toggle acknowledged but function deferred to a future release.
- Backlog items deferred to v3.6.1+: Mr. Core methodology integration (piano test, Morph Cut breathing room, action choreography, studio-vs-cinematic re-pass); 6-Pass Testing Protocol gap-check against the existing Iteration Rule; Transformation prompt mode addition; Seedance 2.0 worked-example library expansion; per-Cinematic-model deep workflow guidance (image and video) — when to pick each Cinematic model for which intent, prompting patterns specific to each, video-mode picker structure; strip product-marketing language from skill content (file-wide pass on `MODELS-DEEP-REFERENCE.md`).
- MANDATORY WORKFLOW and HARD RULES blocks in root `SKILL.md` (lines 27–43) verified byte-for-byte unchanged.
- No new sub-skills created in this release — Elements System extension and Cinema Studio 3.5 documentation both live in the existing `higgsfield-cinema` sub-skill per the established dispatcher routing.
- `higgsfield-cinema/SKILL.md` frontmatter bumped 3.0.0 → 3.1.0 / 2026-04-25 to reflect the additive content scope (mirrors the v3.5.0 sub-skill bump pattern for `higgsfield-workspaces`).

## v3.5.0 — 2026-04-24

### Added
- **Sketch-to-Video / Draw-to-Video workspace** expansion in `higgsfield-workspaces` — full coverage of input characteristics, prompt role, two prompt patterns (Realization and Variation), and use cases for ideation-phase work.
- **Sora 2 Trends workspace** expansion in `higgsfield-workspaces` — distinguishes the templated workspace from raw Sora 2 model use, documents the vertical-first / pacing-optimized characteristics and trade-offs vs. Cinema Studio.
- **Higgsfield Audio standalone workspace** expansion in `higgsfield-workspaces` — three core capabilities (voiceover, voice swap, translation), distinct from Lipsync Studio (audio-to-video sync) and from in-video audio layering (SCELA in `higgsfield-audio`).

### Changed
- `higgsfield-workspaces/SKILL.md` minor version bumped from 1.0.0 to 1.1.0 (additive expansions to existing workspace descriptions; no breaking changes).
- Root `SKILL.md` frontmatter bumped to version 3.5.0.

### Sourcing
Additions informed by the v3.4.0 PDF audit (Higgsfield Tools Guide items 5, 6, 8) and the broader workspace-first framing established in v3.4.0. Full gap analysis preserved in `docs/pdf-audit/AUDIT-REPORT.md`.

### Notes
- All three additions live in the `higgsfield-workspaces` sub-skill — single-file scope.
- No new sub-skills, no routing changes in root `SKILL.md` (only frontmatter version bumped).
- This release closes out the workspace-related MEDIUM backlog from the v3.4.0 audit.
- REINFORCE polish items remain deferred indefinitely.

## v3.4.1 — 2026-04-24

### Added
- **Motion Control failure diagnostic** in `higgsfield-troubleshoot` — symptom → root cause → fix mapping for common Kling 3.0 Motion Control failures, cross-referenced to the workflow added in v3.4.0.
- **Reference Sheet Types** section in `higgsfield-cinema` — extends the Location Reference Sheets pattern from v3.4.0 with three additional reference-sheet categories: Motion/Camera, Outfit/Material, and Palette/Mood.
- **The Iteration Rule** in `higgsfield-prompt` — named methodology for single-variable iteration when refining prompts.

### Sourcing
Additions informed by the PDF audit captured in v3.4.0. Specifically: Kling Motion Control handbook (failure diagnostic), Seedance 2.0 handbook (reference-sheet types), AI Prompting Handbook + Higgsfield Tools Guide (iterate-one-variable rule). Full gap analysis preserved in `docs/pdf-audit/AUDIT-REPORT.md`.

### Notes
- No existing content modified. This release is purely additive.
- Root `SKILL.md` not modified — no new sub-skill, no routing changes.
- Three MEDIUM-priority items shipped from the audit backlog. Remaining workspace-expansion MEDIUMs (Sketch-to-Video, Sora 2 Trends, Higgsfield Audio standalone) deferred to v3.5.0.

## v3.4.0 — 2026-04-18

### Added
- **Location Reference Sheets** pattern in `higgsfield-cinema` — five-view spec for treating locations as first-class assets parallel to character sheets.
- **Seedance 2.0 Prompt Modes** section in `higgsfield-seedance` — documents Reference-Based, Continuation, Expand Shot, and Edit Shot as distinct generation modes with prompt-construction patterns.
- **Continuation Prompt Formula** section in `higgsfield-seedance` — five-rule named pattern for writing continuation prompts (last-frame anchor, identity anchor, prior clip as secondary memory, immediate continuation, no action repeat).
- **Kling 3.0 Motion Control workflow** in `higgsfield-motion` — 8-step Higgsfield UI walkthrough for invoking Motion Control, plus a motion-reference input quality checklist. Cross-referenced from `MODELS-DEEP-REFERENCE.md`.
- **New sub-skill `higgsfield-workspaces`** — workspace-first decision layer that routes users to the right Higgsfield workspace (Cinema Studio / Lipsync Studio / Draw-to-Video / Sora 2 Trends / Click to Ad / Higgsfield Audio) based on the production problem, before model selection.

### Sourcing
Additions informed by review of official Higgsfield documentation (Cinema Studio 3.0 handbook, Seedance 2.0 handbook, Kling Motion Control handbook, Higgsfield Tools Guide) and third-party AI prompting reference material. Source PDFs are not committed to this repo; analysis preserved in `docs/pdf-audit/AUDIT-REPORT.md`.

### Notes
- No existing content modified. This release is purely additive.
- Root `SKILL.md` routing tables updated with two new rows only — MANDATORY WORKFLOW and HARD RULES unchanged.
- MEDIUM and REINFORCE items from the audit deferred to future releases.

## v3.3.0 — 2026-04-17

### Changed
- **BREAKING (install paths):** Flattened skill structure. The dispatcher `SKILL.md` now lives at the repo root. Sub-skills moved from `mnt/user-data/outputs/higgsfield/skills/` to `./skills/`. Templates moved from `mnt/user-data/outputs/higgsfield/templates/` to `./templates/`. The `mnt/user-data/outputs/` directory has been removed — it was a Claude runtime artifact path, not a canonical skill install location.
- The old root `SKILL.md` (scoped to model-guide only) has been merged into `skills/higgsfield-models/SKILL.md`. Users should now point to the new unified dispatcher.

### Added
- Explicit **MANDATORY WORKFLOW** and **HARD RULES** blocks at the top of the root `SKILL.md`, hardened for Claude Opus 4.7's literal instruction-following behavior. The model will now route requests through sub-skills and apply MCSLA without needing to be told manually.
- First-response one-line sub-skill confirmation rule so users see the skill engaged.

### Fixed
- Broadened skill `description` frontmatter so the skill triggers on generic video-prompt requests, not just model-selection queries.
- Fixed all relative path references after the flatten.

### Migration
- If you installed via `cp -r` to `~/.claude/skills/`, re-clone from `main` — the install path changed.
- If you use Claude.ai Projects, re-upload the root `SKILL.md` as your project instruction base.

## v3.2.0 — 2026-04-10

### Added
- **`higgsfield-seedance` sub-skill** — dedicated Seedance 2.0 / Pro prompt director
  that enforces the filmmaker-voice discipline required to pass Seedance's LLM-based
  content filter on the first try. Routes from the parent skill on any Seedance
  prompt request, flagged-prompt report, or Seedance credit-waste complaint.
  - Filter model explainer (LLM reads full-scene intent, not a keyword blacklist)
  - Instant-fail vs. delayed-fail diagnostic heuristic
  - Six-slot Seedance prompt formula (Camera + Subject + Action + Setting + Style + Lighting)
  - Rewrite playbook for real names, brands/IP, violence, weapons, horror
  - "Filmmaker not Friend" voice rewrite pass (6 rules)
  - Failure-loop recovery protocol with filter-memory logging
- **`seedance_lint.py` — pre-flight linter** at the project root. Pure stdlib,
  no dependencies. Scans a drafted prompt for 11 filter-risk patterns before
  the user burns credits on an instant-fail rejection.
  - FAIL rules: real-person names, brand/IP, violence verbs, weapon nouns,
    age markers, overlength (>220 words)
  - WARN rules: antislop adjectives, long prompts (>180 words), too-short
    prompts (<15 words), missing Style/Mood clause, missing camera move,
    missing setting, contradictory instructions
  - Output: PASS / WARN / FAIL verdict with per-rule fix suggestions
  - Usage: `python3 seedance_lint.py "<prompt>"` or pipe via stdin or `--file`
  - Exit code 1 on FAIL for CI / script integration
  - **Filter-memory loopback:** `--log` appends FAIL verdicts to
    `db/filter-memory.json` with rule hits as `blocked_terms` + `tags` and
    fix suggestions as `substitution`. `--confirmed` logs a rewrite that
    passed Seedance's filter in a real generation (outcome=workaround,
    substitution_worked=True). Update outcomes later with
    `python3 higgsfield_memory.py update-filter <id> <outcome>`.
- Parent skill routing table + sub-skills list updated to surface
  `higgsfield-seedance` for Seedance / flagged-prompt triggers.

## v3.1.0 — 2026-04-10

### Added
- **Seedance 2.0 Scene Archetype Router** (`higgsfield-prompt`) — planning layer on top of MCSLA
  - Action archetypes: Pursuit / Duel / Impact with decision tree
  - General archetypes: Journey / Atmosphere / Reveal with decision tree
  - Dialogue archetypes: Confrontation / Interrogation / Negotiation with decision tree
  - Dialogue word-limit rule (~25–30 spoken words per 15s)
- **Seedance 2.0 Engine Constraints** (`higgsfield-prompt`) — hard rendering rules
  - ≤3 characters tracked across cuts
  - Exit-frame = implicit cut (never choreograph exit + re-entry)
  - Off-screen = nonexistent (state changes must be shown before referenced)
  - Avoid reflection shots (breaks scene geography)
  - Only see-or-hear (no smell/taste/internal thoughts)
  - Action beats = intent + named technique, not joint mechanics
  - Double-contrast cut rule (shot size AND camera character both change)
  - Causally-motivated inserts with named subject
  - Age-blind character rule (describe by role/clothing/action)
  - Default in medias res
- **Pipeline E: Multi-Style Short Film** (`higgsfield-pipeline`) — Soul Cinema + Nano Banana Pro + Seedance 2.0 chain
  - Style-first keyframe generation with Soul Cinema enhancer ON + minimal prompts
  - Style keyword locators (swap 1–2 words to change whole aesthetic)
  - Edit-don't-regenerate workflow via Nano Banana Pro
  - Prop sheet technique (one-time, multi-angle, material breakdown)
  - Previous-video-as-continuity-reference feedback loop (the key consistency trick)
  - 15-second-per-scene cap rationale
  - 6 pipeline-specific pitfalls
- **Cut & Continuity Vocabulary** section in `vocab.md`
  - Double contrast, camera character, re-anchoring, 180° rule
  - Exit-frame = implicit cut, causally-motivated insert
  - Match cut, smash cut, hard cut, L-cut / J-cut, whip-pan transition
- `docs/Seedance 2 Skill.md` — reference file for the full bilingual EN+ZH Seedance director mode (standalone JSON API pattern)

### Changed
- `higgsfield-prompt` bumped to v3.1.0 (Seedance archetype router + engine constraints added)
- `higgsfield-pipeline` bumped to v3.1.0 (Pipeline E added, decision guide updated)

## v3.0.0 — 2026-04-06

### Added
- Cinema Studio 3.0 support (Business/Team plan only) across all sub-skills
  - Full specs: 15s max duration, 720p video, 2K image, 48 credits, 7 genres, 7 aspect ratios (+ 21:9 ultrawide)
  - Smart shot control (auto camera planning) + Custom multi-shot (up to 6 scenes, 12s)
  - Native dual-channel stereo audio (unified multimodal architecture)
  - Soul Cast 3.0: General (2K) / Character (4K) / Location (4K) modes, 0.125 credits
  - @ reference patterns: up to 9 images, 3 video clips, 3 audio clips (≤12 total)
  - Resolution Comparison Table (Cinema Studio 2.5 vs 3.0) in higgsfield-cinema and higgsfield-models
  - "When to Use 3.0 vs 2.5" decision table
- Seedance 2.0 prompting best practices integrated into MCSLA framework
  - Intent over Precision (30–100 word sweet spot)
  - Director's Formula → MCSLA mapping with early-token priority
  - Genre Router with 7 genre-specific prompt length and lead-with targets
  - I2V Gate rule for image-to-video workflows
  - Anti-Slop vocabulary check (kill: beautiful, stunning, epic, amazing, dynamic, energetic)
  - Physics Language — concrete consequences instead of mood words
  - Degree Adverbs for intensity guidance
  - Narrative Structure Options (fluid vs timestamp storyboard)
  - Three-Act Rhythm for action prompts (Charge-up → Burst → Aftermath)
  - No Negative Prompts guidance (positive constraints only)
- One-Move Rule for camera control (one primary camera move per shot)
- Genre-Based Camera Presets table (8 genres with primary/secondary/avoid)
- Reliable Camera Phrasing Library (7 tested phrases)
- Camera Transfer via @Video reference + Dual Video Reference patterns
- Smart Mode documentation for Cinema Studio 3.0 auto-camera
- Intent-First choreography for motion (describe intent, not timestamps)
- @Video Reference as primary method for action/fight scenes
- Beat Density Diagnostic (1–2 beats per 5 seconds)
- One Style Anchor Rule + "Cinematic Does Nothing" guidance
- CGI Material Contract (4 properties per surface)
- Period Control (materials + lighting, not decade labels)
- Style Transfer via @Reference
- Audio elevated to first-class prompt element (SCELA integration)
  - Native audio-video joint generation documentation
  - Input constraints (MP3/WAV, 3 clips, ≤15s, <15MB)
  - Lip-sync (experimental, single face)
  - Tone/Voice cloning via @Reference
  - Dialect support and timestamp anchoring
  - Sound design specificity guidance
- Character consistency best practices for Soul Cast 3.0
- 6-symptom diagnostic tree for Cinema Studio 3.0 troubleshooting
- Cinema Studio 3.0 genre mappings + prompt length targets in all 10 genre templates
- @reference workflow examples in all 10 genre templates
- Cinema Studio 3.0 Notes in shared negative constraints (positive alternatives table)
- Cinema Studio 3.0 comparison section in higgsfield-models

### Changed
- Seedance 2.0 status: removed all "(upcoming)" labels — now documented as active
- Negative constraints updated: Cinema Studio 3.0 does not support negative prompt syntax — positive alternatives provided
- Genre templates updated with Cinema Studio 3.0 genre mappings and Speed Ramp recommendations
- Dispatcher routing table updated with Cinema Studio 3.0 entries
- Unique Feature Matrix expanded with Cinema Studio 3.0 capabilities

### Preserved
- All Cinema Studio 2.5 documentation remains intact and fully supported
- MCSLA formula retained as primary framework throughout
- All v2.0.2 content preserved — this update is purely additive

---

## v2.0.2 — 2026-03-26

### Fixed: Higgsfield DoP documented as model family
- "Higgsfield DOP" was treated as a single model. DoP is actually the family/brand name for Higgsfield's I2V system with three quality tiers: Higgsfield Lite, Standard, and Turbo (all 720p, 3–5s).
- Added DoP family section to model-guide.md with tier breakdown, 50+ preset categories, and optical physics capabilities.
- Added DoP row to video model comparison tables and decision flowcharts in model-guide.md and higgsfield-models/SKILL.md.
- Updated root SKILL.md, dispatcher SKILL.md, README.md, and CHANGELOG.md references from "Higgsfield DOP" to "Higgsfield DoP (Lite/Standard/Turbo)".

### Fixed: Kling 2.1 Master marked as deprecated
- Kling 2.1 Master is no longer on the platform. Marked as "(deprecated)" in model-guide.md and MODELS-DEEP-REFERENCE.md with notice to use Kling 2.6 or 3.0.
- Removed from Create Video tab model list in model-guide.md.

### Fixed: Grok Imagine Image removed from image model listings
- "Grok Imagine Image" does not exist on the Higgsfield platform — Grok Imagine is a video-only model family.
- Removed from image model quick selection table and decision flowchart in higgsfield-models/SKILL.md.
- Removed from cost table in image-models.md.
- Added "NOT available on Higgsfield" notice to the xAI API documentation section in MODELS-DEEP-REFERENCE.md (documentation preserved for reference).
- Updated Quick Decision Table to redirect former Grok Imagine Image recommendations to GPT Image 1.5, Multi Reference, and Flux Kontext.

### Fixed: Seedance 2.0 labeled as upcoming
- Seedance 2.0 is pre-documented but not yet live on the platform. Added "(upcoming)" labels across model-guide.md, higgsfield-models/SKILL.md, MODELS-DEEP-REFERENCE.md, higgsfield-audio/SKILL.md, higgsfield-troubleshoot/SKILL.md, and shared/negative-constraints.md.
- Decision flowcharts now note "use Seedance 1.5 Pro until launch" as fallback.

### Updated: Version bumped to 2.0.2
- All 21 SKILL.md files, MODELS-DEEP-REFERENCE.md, and README.md bumped from 2.0.1 to 2.0.2.

---

## v2.0.1 — 2026-03-26

### Fixed: Broken shared/negative-constraints.md paths (14 instances)
- 13 sub-skill SKILL.md files referenced `shared/negative-constraints.md` using paths relative to their own directory, which didn't resolve. Fixed to `../shared/negative-constraints.md` in all sub-skills.

### Fixed: Model name accuracy
- **"Nano Banana Pro 2" does not exist.** Corrected to "Nano Banana Pro" across 5 files (13 instances). "Nano Banana", "Nano Banana 2", and "Nano Banana Pro" are three separate models — they were previously conflated.
- **"MiniMax" → "Minimax"** — platform spells it "Minimax Hailuo" (lowercase 'imax'). Fixed across 13 files (26 instances).

### Fixed: Templates missing Identity/Motion guidance
- Templates 01 (action chase), 02 (product UGC), and 07 (landscape) now include Identity/Motion Block callouts referencing template 06 and `higgsfield-soul`.
- Template 03 (horror) restructured: Identity/Motion Block sections moved before Variations to match the format used by the other 9 templates.

### Fixed: MODELS-DEEP-REFERENCE.md frontmatter regression
- `tags` was at the top level instead of inside `metadata` — the exact bug v1.5.1 fixed. Moved back inside `metadata`.

### Fixed: Memory system bugs (higgsfield_memory.py + JSON DBs)
- **ID prefix mismatch:** Seeded entries used `filt-`/`qual-` prefixes but code generates `F-`/`Q-`. Aligned seeded data to match code (`F-001`–`F-004`, `Q-001`–`Q-005`).
- **Date field mismatch:** Seeded entries used `"date"` but code reads `"date_added"`. Renamed in all 9 seeded entries.
- **Missing `outcome` field:** Added `"outcome": "workaround"` to all 4 filter entries.
- **Docstring:** Added `update-quality` to usage docstring (command was wired but undocumented).

### Fixed: README.md structure tree
- Added `validate.py`, `CONTRIBUTING.md`, and `USER-GUIDE.pdf` to the project tree.

### Fixed: validate.py
- Added check for `tags` at top level of frontmatter (the regression it was created to prevent).
- Removed unused `SKILL_DIRS` variable.

### Fixed: Minor consistency
- `higgsfield-recall/SKILL.md`: moved non-standard `compatibility` block inside `metadata`.

### Updated: Version bumped to 2.0.1
- All 21 SKILL.md files, MODELS-DEEP-REFERENCE.md, and README.md bumped from 2.0.0 to 2.0.1.

---

## v2.0.0 — 2026-03-26

### New: Shared Negative Constraints Reference
- Created `skills/shared/negative-constraints.md` — a consolidated, categorized reference of all AI video/image generation artifacts and the prompt phrasing to prevent them.
- Six categories: Body/Motion Artifacts, Face/Identity Artifacts, Texture/Lighting Artifacts, Temporal/Consistency Artifacts, Content Filter/Safety Artifacts, Cinema Studio–Specific Artifacts.
- Each entry includes: the artifact, why it happens in AI video, and the recommended prevention phrase.
- All 18 sub-skills updated to reference this shared file for their relevant artifact categories.
- Domain-specific constraints that only apply to one sub-skill remain in that sub-skill — the shared file supplements, not replaces.

### New: Identity vs. Motion Separation Rule
- Added hard rule to `higgsfield-prompt` and `higgsfield-soul`: when Soul ID or character consistency is involved, prompts must be split into two blocks:
  - **Identity Block** — static visual descriptors only (face, clothing, body, marks). No motion, no camera, no temporal language.
  - **Motion Block** — camera movement, action, speed, environmental changes. No character description repetition.
- Includes 3 before/after examples showing mixed (bad) vs. separated (good) prompts with explanations.
- Added "which descriptors belong where" reference table.
- Updated `higgsfield-recipes`, `higgsfield-pipeline`, `higgsfield-cinema`, and `higgsfield-recall` to reference this separation rule.
- All 10 genre templates include Identity Block + Motion Block sections for character-involved prompts.

### New: Templates Folder (10 annotated genre templates)
- Created `templates/` directory with 10 production-quality annotated prompt templates:
  1. `01-cinematic-action-chase.md` — Chase/pursuit sequences
  2. `02-product-ugc-showcase.md` — Product ads and UGC content
  3. `03-horror-atmosphere.md` — Horror and atmospheric dread
  4. `04-fashion-editorial.md` — Fashion/editorial portraits
  5. `05-sci-fi-vfx.md` — Sci-fi and VFX spectacle
  6. `06-portrait-character-intro.md` — Character introductions
  7. `07-landscape-establishing-shot.md` — Landscape/establishing shots
  8. `08-comedy-social-media.md` — Comedy and social media content
  9. `09-romantic-intimate.md` — Romance and intimate moments
  10. `10-dance-music-performance.md` — Dance/music performances
- Each template includes: genre header, trigger conditions, recommended model, full example prompt, line-by-line annotation, negative constraints reference, common mistakes, and 3-4 variations.
- Templates based on and expanded from proven `prompt-examples.md` prompts.
- Main dispatcher SKILL.md updated with genre-matching routing table for templates.

### New: Sub-Skill Cross-References
- Added "Related skills" footer to all 18 sub-skills pointing to relevant sibling skills.
- Added `shared/` and `templates/` paths to the main dispatcher routing table.
- Updated dispatcher with new "Shared Resources" section.

### Updated: Main Dispatcher
- Version bumped to 2.0.0.
- Added template genre-matching routing table ("Check Templates for Genre Match").
- Added Shared Resources section with paths to `shared/negative-constraints.md` and `templates/`.
- Added template and shared constraint references to the footer resource list.

### Updated: All sub-skills version bumped to 2.0.0
- All 18 sub-skill SKILL.md files + MODELS-DEEP-REFERENCE.md bumped from 1.6.0 to 2.0.0.
- Root SKILL.md and dispatcher SKILL.md both at 2.0.0.

---

## v1.6.0 — 2026-03-26

### New: Kling 3.0 Model Family
- **Kling Video 3.0 (V3)**: 15s max duration, multi-shot generation (up to 6 camera cuts), native audio-visual co-generation with multilingual support (EN, ZH, JA, KO, ES + regional accents), Voice Binding, multi-character dialogue (3+ speakers), physics engine, 4K HDR output, professional export (16-bit HDR, EXR sequences), text rendering, Elements 3.0 tagging, sequential action syntax, motion endpoint pattern.
- **Kling Video 3.0 Omni (O3)**: Same quality as V3 plus Video Element referencing, Performance Cloning, Voice Extraction from static images, custom storyboard, multi-character coreference, video-to-video, natural language editing, 4K/60fps.
- **Kling 3.0 Motion Control**: Reference video → motion transfer (3–30s), Image/Video Orientation modes, Element Binding for face stability, camera sync, audio passthrough.
- **Kling Image 3.0**: Native 4K (up to 3840×2160), Image Series Mode, up to 10 reference images, Visual Chain-of-Thought, style transfer + portrait + character reference + multi-image blending, local re-editing, cinematic color grading.
- **Kling Image 3.0 Omni**: Same as Image 3.0 plus advanced editing with stronger prompt fidelity. Native 2K and 4K output.
- Added V3 vs O3 selection guidance, Audio Speaker Attribution Format, Multi-Shot Storyboard Format.
- Marked Kling 2.6 and O1 as legacy (still documented).
- Updated model comparison tables, decision flowcharts, and unique feature matrix across all model reference files.

### New: Cinema Studio 2.5
- Updated Cinema Studio from 2.0 to 2.5 across all files.
- **Soul Cast integration**: Character-and-location-first workflow with up to 3 AI actors per keyframe. 8 parameter categories (Genre, Budget, Era, Archetype, Identity, Physical Appearance, Details, Outfit). Auto-generated backstory + character sheet. Powered by Nano Banana 2.
- **Soul Cast vs Soul ID** distinction documented: Soul Cast = generate AI actors from parameters (no photos needed); Soul ID = upload 20+ photos to train identity consistency.
- **Built-in Color Grading Suite**: Color temperature, contrast, saturation, sharpness, film grain, exposure, bloom. Applied to keyframes before video generation.
- Extended workflow: pre-production (Soul Cast + location) → generation → post-production (color grade).

### New: Nano Banana 2 expanded documentation
- Expanded prompting-relevant capabilities: subject consistency (5 characters, 14 objects), precision text rendering + translation, advanced world knowledge, 512px to 4K, full aspect ratio list, infographic/diagram generation, reference image editing, style transfer.
- Added prompting patterns: structured JSON, short direct, style transfer, location+time, blueprint/schematic, infographic overlays, multi-panel comics, product ad recreation.
- Added NB2 vs NB Pro comparison note.

### New: Soul Cinema Preview (image model)
- Higgsfield proprietary cinematic-grade image model (launched March 4, 2026).
- Prompt-driven only (no preset panel). Excels at close-up shots. Works with Soul ID + Soul HEX.
- Key workflow: generate cinematic keyframe → feed into Kling 3.0 I2V.
- Documented Soul HEX color palette system.

### New: Expanded cinematic vocabulary (UPDATE 5)
- **Camera angles**: Low Angle, High Angle, Eye Level, Bird's-Eye View, Worm's-Eye View, Ground Level, Canted Angle Left/Right, Static Oblique, OTS, POV, Two-Shot, Cowboy Shot added to `higgsfield-camera`.
- **Shot sizes**: Full standard ladder (ELS through Insert Shot) added to `higgsfield-camera`.
- **Micro-expressions**: 19 nuanced facial performance directions (Core set + Extended set) added to `higgsfield-soul`.
- **Cinematic lighting techniques**: 13 named lighting techniques (Rembrandt, Butterfly, Split, Rim, Motivated, Practical, Chiaroscuro, High-key, Low-key, Golden hour, Blue hour, Harsh midday, Overcast diffused) added to `higgsfield-style`.
- **Key prompting principle**: "#1 mistake in video prompting" callout added to `higgsfield-prompt`.

### Updated: Platform model lineup
- Video: Kling 3.0, Kling O1, Kling 2.6, Kling 2.5 Turbo, Kling 3.0 Motion Control, Sora 2, Google Veo 3.1, Wan 2.5/2.6, Seedance Pro, Minimax Hailuo 02, Higgsfield DoP (Lite/Standard/Turbo).
- Image: Nano Banana Pro, Nano Banana 2, Soul 2.0, Soul Cinema Preview, Soul Cast, Flux 2, Flux Kontext, GPT Image 1.5, Seedream 4.0.
- Updated root SKILL.md, dispatcher, model-guide.md, and higgsfield-models sub-skill.

### Updated: Audio skill for Kling 3.0
- Multi-character dialogue (3+ speakers with correct attribution).
- Voice Binding and Voice Extraction (O3).
- Performance Cloning (O3).
- Audio Speaker Attribution Format template.

### All sub-skills version bumped to 1.6.0

---

## v1.5.2 — 2026-03-18

### Fixed: higgsfield_memory.py — Robustness
- Added `ValueError` handling around `int(sys.argv[3])` in `query-filter` and `query-quality` — passing a non-integer `top_n` argument now returns a clean JSON error instead of an unhandled crash.
- Made `export_summary()` atomic — writes to `.tmp` then renames, consistent with `save_db()`. Prevents partial/corrupted output on interrupted writes.

### Fixed: higgsfield-recall/SKILL.md — Broken command references
- Changed `python higgsfield_memory.py ...` → `python3` in all three code blocks. `python` is not in PATH on modern macOS/Linux.
- Replaced reference to non-existent `higgsfield-learn` skill with the correct `higgsfield-troubleshoot`.

### Fixed: validate.py — Typo
- Corrected "Highsfield" → "Higgsfield" in the validation report header.

## v1.5.1 — 2026-03-18

### Fixed: higgsfield_memory.py — Critical error handling
- Added try-except around `json.loads()` in `add_filter()` and `add_quality()` — malformed JSON no longer crashes the script; returns a structured error response instead.
- Made `save_db()` atomic — writes to a `.tmp` file then renames it, preventing database corruption if the process is interrupted mid-write.
- Added try-except to `load_db()` covering missing file and corrupted JSON cases.
- Added deterministic secondary sort key (`date_added`) to `query_filter()` and `query_quality()` — equal-scored results now return in consistent order.
- Improved tokenizer — hyphenated terms (e.g. `real-person`) now match as a whole phrase AND as individual component words, improving filter memory accuracy.
- Removed unused `import os`.

### Fixed: higgsfield_memory.py — New `health` command
- Added `python3 higgsfield_memory.py health` — runs a quick integrity check on both database files (validates JSON, verifies entry counts match `_total_entries`).

### Fixed: db/filter-memory.json — Schema completeness
- Added missing `substitution_worked` field (was `null`-defaulted in code but absent from all 4 seeded entries).

### Fixed: db/quality-memory.json — Field naming consistency
- Renamed `model` → `model_used` and `category` → `failure_type` in all 5 entries to match what `add_quality()` writes.
- Added missing `outcome` and `improvement_confirmed` fields to all 5 entries.

### Fixed: SKILL.md frontmatter — Invalid top-level attributes
- Moved `tags` from top-level into `metadata` block across all 20 SKILL.md files (`tags` is not a supported top-level skill attribute).
- Moved `references` from top-level into `metadata` block in `SKILL.md` and `higgsfield-models/SKILL.md`.

### Fixed: Broken relative paths
- Main dispatcher (`mnt/user-data/outputs/higgsfield/SKILL.md`): corrected bare filenames `vocab.md`, `model-guide.md`, `prompt-examples.md` to proper relative paths (`../../../../`).
- `higgsfield-models/SKILL.md`: corrected `image-models.md` reference to `../../../../../../image-models.md`.

### Fixed: README — Incorrect install command
- Changed `cp -r higgsfield_v140` to `git clone … && cp -r higgsfield_v150` with correct repo path.
- Corrected directory diagram label from `higgsfield_v150/` to `higgsfield/ (repo root)`.
- Corrected Cowork install instruction (was referencing a non-existent `higgsfield_v150/` subfolder).

### New: validate.py — Pre-release health checker
- Added `validate.py` at repo root: verifies all SKILL.md files have valid frontmatter, all relative path references resolve to real files, both JSON databases are valid and schema-complete, and all expected root files are present.
- Run with `python3 validate.py` before any release. Exits 0 on pass, 1 on failure with itemised report.

## v1.5.0 — 2026-03-13

### New: Cinema Studio 2.0 — 3D Mode (Gaussian Splatting)
- Documented the 3D exploration feature that builds a 3D Gaussian splat from any generated image.
- Virtual camera orbit around generated scenes — front, side, back, above.
- Creative workflow: generate image → enter 3D Mode → orbit to new angle → capture as new start frame → animate.
- Best practices for source images (single subjects, clear geometry, even lighting).

### New: Cinema Studio 2.0 — Grid Generation (Batch Variations)
- Documented 2×2 and 4×4 grid generation modes for producing multiple variations from a single prompt.
- 2×2 = 4 variations per credit; 4×4 = 16 variations per credit.
- Use cases: A/B testing compositions, character sheet creation, finding the best start frame.

### New: Cinema Studio 2.0 — Resolution Settings
- Documented explicit resolution control: 1K (fast drafts), 2K (default production), 4K (final delivery).
- Higher resolution = longer generation time, same credit cost.

### New: Cinema Studio 2.0 — Frame Extraction Loop
- Documented the iterative Build → Animate → Extract → Feed Back → Repeat workflow.
- Extract any frame from a generated video as a new start image for the next generation.
- Key technique for extending sequences beyond single-clip duration limits.

### New: Cinema Studio 2.0 — Object & Person Insertion
- Documented the ability to insert characters or objects not present in the original start frame.
- Describe the new element in the prompt; the model composites it into the scene.
- Best practices: match lighting, keep scale plausible, one insertion per generation.

### New: Cinema Studio 2.0 — 12-Second Total Runtime Cap
- Added critical warning to Multi-Shot Manual section: total runtime across all scenes is capped at 12 seconds.
- Duration allocation strategy: plan scene durations before building to avoid hitting the cap.

### New: Cinema Studio 2.0 — Per-Character Emotion Controls
- Documented per-character emotion settings in the Elements system: Joy, Fear, Surprise, Sadness.
- Applied per character per scene in Multi-Shot Manual mode.

### New: Cinema Studio 2.0 — Clustering (Automatic Generation Grouping)
- Documented the automatic grouping feature that clusters generations from the same prompt.
- Expand/collapse cluster groups for project organization.

### New: Soul ID — Character Sheet Creation
- Added Character Sheet workflow to the Soul ID skill.
- Multi-angle reference images (front, 3/4, side, full body) for improved consistency.
- How to create character sheets using Grid Generation and 3D Mode.
- Why multi-angle references improve Soul ID consistency across extreme angle changes.

### Updated: Cinema Studio comparison table
- Added rows for 3D exploration and batch generation to the Cinema Studio vs Standard comparison.

### Updated: All sub-skills version bumped to 1.5.0

---

## v1.4.0 — 2026-03-05

### Fixed: MODELS-DEEP-REFERENCE.md — Duplicate YAML key
- Removed duplicate `user-invokable: true` key from frontmatter (kept correct `user-invocable: true`).

### New: Cinematic Still Images section in prompt-examples.md
- Added 3 fully worked cinematic still image examples using the v1.3.9 Image Prompt Formula (`[Shot size] + [Angle] + [Movement keyword] of [character]. [Pose]. [Environment]. [Lighting]. [Style].`).
- **Example 8 — Sci-Fi Character Tension** (Nano Banana Pro, 16:9): MCU + Low Angle + Dolly Zoom. Cyber-enhanced operative in neon rain.
- **Example 9 — Epic Fantasy Scale** (Seedream 4.5, 16:9): EWS + Overhead + Crane Up. Lone warrior on a shattered bridge over a lava chasm.
- **Example 10 — Psychological Thriller Detail** (Nano Banana Pro, 3:4): ECU + Dutch Angle + Rack Focus. Lipstick-smeared mirror reflection in a dim bathroom.
- Covers a mix of models, aspect ratios, and genres.

### Fixed: higgsfield_memory.py — Directory fallback bug
- Replaced fragile `if not DB_DIR.exists(): DB_DIR = SCRIPT_DIR` fallback with `DB_DIR.mkdir(parents=True, exist_ok=True)`.
- Ensures the `db/` directory is always created rather than silently falling back to the script directory (which would misplace database files).

### Fixed: prompt-examples.md — Audio duration correction
- Example 5 (Audio-Driven Scene): changed duration from `10s` to `8s` to match Seedance 1.5 Pro's recommended lip-sync sweet spot (3–8s).

### New: Memory summary for cold-start resolution
- Generated `db/memory-summary.md` via `python3 higgsfield_memory.py export-summary`.
- Human-readable snapshot of all 4 filter memory entries and 5 quality memory entries.
- Added to project knowledge base for automatic context loading — eliminates cold-start gap where Claude previously had no recall of past generation failures.

---

## v1.3.9 — 2026-03-04

### New: higgsfield-image-shots sub-skill — Cinematic Image Prompting
- New dedicated sub-skill for **still image** prompt composition, separate from video camera controls.
- **10 Distance & Size shots** with AI prompt keywords and examples: Extreme Wide Shot (EWS), Wide Shot / Long Shot, Full Shot, Medium Long Shot (MLS), Cowboy Shot, Medium Shot (MS), Medium Close-Up (MCU), Close-Up (CU), Extreme Close-Up (ECU), Macro Shot.
- **10 Camera Angles** with emotional purpose and prompt patterns: Eye-Level, Low Angle, High Angle, Overhead / Bird's Eye, Worm's Eye, Dutch Angle / Canted Angle, Over-the-Shoulder (OTS), Point of View (POV), Selfie Angle, Ground Level.
- **17 Camera Movements for stills** across three tiers — Static/Basic (Static, Pan, Tilt, Zoom In/Out, Pedestal), Advanced Physical (Dolly In/Out, Truck, Orbit, Crane), Cinematic & AI (Dolly Zoom/Vertigo, Crash Zoom, FPV, Bullet Time, Handheld Follow, Camera Roll, Rack Focus, Pull Back Reveal, Fly-Through).
- Every entry includes: AI Prompt Keyword, definition, primary purpose/effect, and a ready-to-paste prompt example using the `[img 1]` reference pattern.
- **Quick reference tables** for Distance & Size and Angles for fast lookup.
- **Combination formula** — how to layer shot size + angle + movement keyword into a single image prompt with 4 worked examples.
- **Image Prompt Formula** — structured pattern: `[Shot size] + [Angle] + [Movement keyword] of [character]. [Pose]. [Environment]. [Lighting]. [Style].`

### Updated: Dispatcher SKILL.md
- Added `higgsfield-image-shots` to routing table and sub-skills index.
- Clarified `higgsfield-camera` label as video-specific to distinguish from the new image shots skill.
- Version bumped to 1.3.9.

### Updated: README.md
- Added `higgsfield-image-shots/SKILL.md` to the directory structure listing.

---

## v1.3.8 — 2026-03-04

### New: Cinema Studio 2.0 — Prompt Character Limit (512 chars)
- Documented the **hard 512-character limit** on Cinema Studio prompt fields.
- @ Element chips consume ~80–100 hidden characters each for internal metadata.
- Added character budget guidelines: ~250 visible chars with 2 tags, ~350 with 1, ~450 with 0.

### New: @ Element Persistence Rule
- Discovered that @ Elements added in **Scene 1 persist across all scenes** in Multi-Shot Manual.
- No need to re-add @ tags in Scenes 2–6. Characters carry through via Reference Anchor.
- Recommended pattern: @ Elements in Scene 1, visual descriptions in subsequent scenes.

### New: Fight Scene Rules (Tested)
- Documented what Cinema Studio CAN and CANNOT render in two-character fight sequences.
- CAN: facing each other, general fighting energy, pinned against wall, falling, walking away.
- CANNOT: specific punch contact, kicks, martial arts, cause-and-effect choreography, prop weapons, grappling.
- Documented **character swap problem**: two @ tags in action scenes causes the AI to confuse hero/villain roles.
- Added fight sequence template alternating @ Element scenes (character) with plain text scenes (action).

### New: Prompting Best Practices (from Higgsfield official)
- Added **pre-prompt checklist**: Who, Where, What's happening, Camera, Mood/Genre.
- Added **one action per scene rule** with breakdown strategy.
- Added **fast motion trick**: generate in Slow Mo, speed up in post.

### Updated: Common Prompt Mistakes table
- Added 4 new entries: over 512 chars, impact before action, specific martial arts, multiple @ tags in action.

## v1.3.7 — 2026-02-28

### Architecture: De-duplication pass
- **Root SKILL.md** stripped from 146 to 42 lines — removed full model tables and quick reference that duplicated `model-guide.md`. Now a lean index with cross-references only.
- **Dispatcher SKILL.md** stripped from 219 to ~170 lines — removed duplicated MCSLA definition (lives in `higgsfield-prompt`), model selection table (lives in `higgsfield-models`), and platform quick reference. Keeps only workflow, routing table, output format.
- Net token savings: ~300 lines of duplicated content removed from default context window load.

### New: Fast Path for simple requests
- Dispatcher now distinguishes between **fast path** (clear creative intent, no constraints → generate immediately with sensible defaults) and **full path** (production-grade → confirm parameters first).
- Defaults: 16:9, 8s, Cinematic, Kling 3.0 (character) or Sora 2 (action), Soul 2.0 (portrait) or Nano Banana Pro (other images).

### Fixed: Recall system paths
- `higgsfield_memory.py` path changed from `SCRIPT_DIR.parent / "db"` to `SCRIPT_DIR / "db"` with fallback to same-directory. Matches actual directory layout.
- Created `db/` directory and moved `filter-memory.json` into it.
- Created `quality-memory.json` (was missing entirely).
- Updated all `higgsfield-recall/SKILL.md` bash commands from `scripts/higgsfield_memory.py` to `higgsfield_memory.py`.

### New: Seeded memory databases
- `filter-memory.json` seeded with 4 entries: real-person blocks, brand/IP blocks, violence filter, Seedance 2.0 face upload restriction.
- `quality-memory.json` seeded with 5 entries: character drift (Sora 2), VHS style ignored (Kling 2.6), I2V static output, camera conflict, lip-sync desync (Seedance 1.5 Pro).

### Slimmed: higgsfield-models
- Split into compact `SKILL.md` (~200 lines, handles 90% of model selection) and `MODELS-DEEP-REFERENCE.md` (full 1021-line per-model documentation, loaded on-demand).
- SKILL.md contains: comparison table, decision flowchart, image quick selection, budget tiers, unique feature matrix, key model notes.

### New: higgsfield-audio sub-skill
- Full audio prompting guide covering all audio-capable models (Kling 3.0, Seedance 1.5 Pro/2.0, Veo 3/3.1, Grok Imagine Video).
- Four audio layers: Dialogue, SFX, Ambient, BGM — with prompt structure and best practices.
- Lip-sync rules: timing, framing, token conflicts, multi-character workaround.
- Per-model audio notes and common failure/fix table.

### New: Before → After prompt examples
- 5 transformation examples added to `prompt-examples.md` showing weak → strong prompt improvement.
- Covers: vague→specific, over-described I2V, slop words, camera conflicts, missing audio direction.

### Consistency pass
- All sub-skills bumped to version 1.3.7.
- `higgsfield-troubleshoot` updated: character consistency recommendation changed from "Kling 2.6" to "Kling 3.0 (or 2.6 if no audio needed)". VFX recommendation updated. Audio troubleshooting sections added.
- Removed duplicate `user-invokable: true` typo key from all frontmatter blocks.
- Dispatcher routing table updated with `higgsfield-audio` entry.

---

## v1.3.6 — 2026-02-28

### higgsfield-models/SKILL.md — Grok Imagine family added (was completely absent)

Grok Imagine (`grok-imagine-image` and `grok-imagine-video`) had zero entries anywhere in the library despite being live on the platform. Both models documented from scratch using the official xAI API docs (docs.x.ai/developers/model-capabilities/images/generation and video/generation).

**Architecture context documented:**
Aurora is an autoregressive mixture-of-experts network — architecturally distinct from diffusion models. Predicts next token from interleaved text+image data. This gives it tighter compositional control, stronger multi-element scene understanding, and reliable text/logo rendering where diffusion models fail.

**`grok-imagine-image` — new complete entry:**
- Text-to-image with full aspect ratio table (10 ratios including `auto`, `19.5:9`, `20:9`)
- Resolution: 1k / 2k
- Image editing (single image): source image + prompt, output follows input ratio. Critical note: OpenAI SDK `images.edit()` uses `multipart/form-data` which is NOT supported — must use xAI SDK or `application/json` directly
- Multi-image editing (up to 3 source images): ordered input, cross-image compositing, aspect ratio override
- Multi-turn iterative editing chain: use each output URL as next input — primary recommended workflow for complex compositions
- Style transfer: photorealistic → anime → oil painting → pencil sketch → watercolor → pop art
- Batch generation: up to 10 images per request via `n` parameter
- Aurora differentiators table: text/logo rendering, multi-person scenes, precise prompt adherence, photorealism, iterative chains, batch A/B testing
- Content moderation: `response.respect_moderation` flag documented

**`grok-imagine-video` — new complete entry:**
- Duration: 1–15s (generation); editing preserves source duration (not user-configurable)
- Resolution: 720p (cap for both generation and editing; 1080p input downsized)
- Audio: ✅ native — dialogue, SFX, ambient, music
- Generation modes: T2V, I2V, video editing/restyling
- Async workflow: `request_id` → poll until `status: "done"` → download from temporary URL
- Video editing constraints: input must be publicly accessible URL; output capped at 720p; duration not configurable
- Imagine 1.0 (Feb 1, 2026): duration extended to 10s, improved audio quality, video editing (add/remove objects, restyle, motion control)
- Grok Imagine internal decision table (8 rows, image vs video routing)

**model-guide.md:**
- Grok Imagine Video added to video table
- Grok Imagine Video added to decision flowchart

**image-models.md:**
- Grok Imagine Image added to pricing/capability table

**Quick Decision Table (higgsfield-models SKILL.md):**
- 7 new Grok Imagine rows added (5 image, 2 video)

---

## v1.3.5 — 2026-02-28


### higgsfield-models/SKILL.md — Google Veo family complete rewrite

The library had one thin "Veo 3 (Google)" entry (6 lines). The UI shows 4 Veo models on platform. Google's official API docs (ai.google.dev/gemini-api/docs/video) confirm Veo 3.1 has significant exclusive capabilities missing from all previous documentation.

**New entries: Veo 3.1, Veo 3.1 Fast, Veo 3 Fast** (in addition to expanded Veo 3)

**Veo 3.1 — new capabilities documented (3.1-exclusive features):**
- Reference images (up to 3): `reference_type: "asset"` — preserves subject appearance (character face, outfit, prop) consistently throughout video. Veo 3.1 and 3.1 Fast only, not available in Veo 3/3 Fast.
- First + last frame interpolation: specify opening and closing frame images; model generates the motion between them. Duration must be 8s when using this feature.
- Video extension: extend any Veo-generated video by 7s, up to 20 times (max 148s total). Input must be 720p. Videos stored 2 days (timer resets on each reference). Voice extension requires audio in last 1s of source.
- 4K output: 8s only, higher latency/cost. 1080p also 8s only. 720p supports all durations (4/6/8s).
- Portrait mode (9:16): available across all Veo 3/3.1 models.

**Duration constraints documented:**
- Reference images / first+last frame / 1080p / 4K → duration must be 8s
- Extension → input must be 720p; output combines original + extension up to 148s

**Audio generation guidance added:**
- Dialogue: use quotes for specific speech
- SFX: describe sounds explicitly (tires screeching, not just "loud sounds")
- Ambient: describe environment soundscape
- Negative prompts: supported (describe what you don't want, no "no X" language)

**Full Veo prompt element framework documented:**
Subject / Action / Style / Camera / Composition / Focus+Lens / Ambiance / Audio

**Veo 3.1 vs Veo 3 comparison table** — 8 capabilities across all 4 models (audio, reference images, first/last frame, extension, 4K, portrait, negative prompts, stable/preview status)

**Veo 3.1 Fast, Veo 3 Fast** — new entries clarifying speed/quality/cost tradeoffs and use cases

**Quick Decision Table** — Veo row expanded from 1 to 5 rows

### model-guide.md
- Video table: Veo row expanded from 1 to 4, audio column corrected to ✅ for all Veo 3/3.1 (was incorrectly ❌), durations added
- Decision flowchart: Veo branch expanded to 5 decision points

---

## v1.3.4 — 2026-02-28


### higgsfield-models/SKILL.md — Seedance 2.0 full production documentation

Seedance 2.0 has not yet shipped on Higgsfield but is incoming. This version replaces the thin v1.3.3 stub with a complete, production-ready reference document built from two third-party Seedance 2.0 skill libraries (Emily/@iamemily2050's seedance-2.0 v3.8.0 and seedance-bot-1), both containing validated practitioner knowledge from 10,000+ generation testing on the Jimeng/Dreamina platform.

**New sections added to the Seedance 2.0 entry:**

- **Rule of 12** — Full asset budget table with the critical correction that video clips share a 15s combined limit (not 15s per clip). Audio 15s combined limit also documented.
- **Generation Modes (T2V / I2V / V2V / R2V)** — All four modes documented with the critical V2V distinction: reference technique vs. direct edit trigger different model pathways
- **Five-Layer Prompt Stack** — Subject/Action/Camera/Style/Sound architecture with Delegation Levels 1–4, word count ranges, decision rule, and complete examples at each level including Level 4 fight choreography
- **6-Part Field Formula** — `[SHOT TYPE] + [SUBJECT] + [ACTION] + [STYLE] + [CAMERA MOVEMENT] + [AUDIO CUES]`, cross-validated on 10,000+ generations
- **Anti-Slop / Prompt Hygiene** — Instant-delete word list and measurable replacement table; the one test: "can a camera, light meter, or stopwatch measure this word?"
- **Camera Control** — Full camera contract (framing/move/speed/angle), reliable phrasing library, anti-drift rules, One-Take technique (一镜到底) with image waypoints, Nine-Grid storyboard method (九宫格)
- **Audio Rules and Failure Modes** — Platform hard limits (MP3 only — WAV/AAC fail silently), sweet spot 3–8s, timestamp anchoring phrase for audio rewrite bug, multi-character compositing workaround, critical Jimeng platform distinction (Seedance 2.0 video generation vs. OmniHuman-1 Digital Human tool — Master/Quick/Standard modes do NOT exist in Seedance 2.0)
- **Character Identity** — Character card format, identity anchoring syntax, multi-character @Tag patterns, 360° consistency test, hand safety rules
- **Beat Density** — Max changes per duration table, Level 4 fight density guidance
- **Genre Templates** — 5 ready-to-use starters: product ad, fight scene, short drama dialogue, music beat sync, architecture walkthrough
- **Compliance / Copyright** — 6-gate pre-generation checklist, substitution table (Iron Man → descriptor, Spider-Man → descriptor, Eiffel Tower → descriptor, Bohemian Rhapsody → descriptor)
- **Emergency Fixes** — 8-row quick-fix table for all common failure modes
- **Platform Parameters** — Confirmed aspect ratios (16:9 · 9:16 · 4:3 · 3:4 · 21:9 · 1:1), resolution tiers, duration range
- **Feb 2026 status note** — Real person face uploads blocked, API delayed, Higgsfield integration incoming

**Quick Decision Table** — Seedance 2.0 expanded from 1 row to 3 rows (R2V / V2V / complex motion routing)

**Key accuracy corrections from practitioner data (vs. earlier documentation):**
- Video clip limit is 15s COMBINED total, not 15s per clip
- Negative prompts (--no syntax) are NOT supported — positive constraints only
- Lip-sync sweet spot is 3–8s, not the 15s technical maximum
- Master/Quick/Standard modes belong to OmniHuman-1 Digital Human, NOT Seedance 2.0
- API is delayed (was planned Feb 24) due to copyright enforcement actions

---

## v1.3.3 — 2026-02-28


### higgsfield-models/SKILL.md — Seedance Family Complete Rewrite

The library previously had a single thin "Seedance Pro" entry. Three properly documented tiers now replace it:

**Seedance 2.0** — new entry (most advanced tier, was completely missing):
- Architecture: unified multimodal audio-video joint generation (text + image + audio + video inputs)
- 12 simultaneous asset inputs: 9 images + 3 video clips (15s each) + 3 audio files + text
- Model auto-interprets each asset's role; use natural language to specify references
- Motion realism: industry-leading complex multi-person interaction (synchronized sports, fight choreography)
- Acoustic physics: audio calculated from visual environment geometry (not just layered on)
- Frame-level precision: control fonts, transitions, screen rhythm per frame
- Video extension + scene merging with maintained continuity
- ~30% faster generation than comparable 2K models
- Use case: reference choreography video + character images + audio clip → synchronized scene

**Seedance 1.5 Pro** — new entry (was missing — different model from Pro):
- Architecture: dual-branch Diffusion Transformer, simultaneous audio-video single-pass generation
- Multilingual lip-sync: English, Chinese (Sichuanese, Cantonese, Taiwanese Mandarin, Shanghainese), Japanese, Korean, Spanish, Indonesian
- Multi-character dialogue with correct lip-motion assignment per character
- Audio types: speech, singing, non-verbal vocalizations, SFX, BGM — all native
- Beats Kling 2.6 and Veo 3.1 on audio-visual synchronization (SeedVideoBench 1.5)
- Cinematic camera: dolly zoom (Hitchcock zoom), long takes, orbital/arc/tracking shots
- Strong in stylized content: comedy timing, theatrical/opera performance, short dramas
- Architecture note: simultaneous generation (not post-production layering) is the key distinction vs competitors

**Seedance Pro** — existing entry expanded:
- Clarified as fast iteration tier, NO native audio
- Pro (1080p) vs Lite (720p) distinction documented
- Correct positioning: use when audio not required; iterate before committing to 1.5 Pro/2.0

**Quick Decision Table** — Seedance row expanded from 1 to 3 rows

### model-guide.md
- Video table: Seedance row expanded from 1 to 3 with audio column correctly marked
- Decision flowchart: Seedance branch updated with audio/no-audio split and Seedance 2.0 option

---

## v1.3.2 — 2026-02-28


### higgsfield-models/SKILL.md — Kling Family Complete Rewrite

**Kling 3.0** — fully documented (was a thin stub): duration 3–15s, native multilingual audio (6 languages + accents), AI Director multi-shot mode, physics-aware engine, stylized output (anime/Pixar/claymation), EXCLUSIVE badge.

**Kling 3.0 Omni** — new entry: Performance Cloning (clone character appearance + voice from 3–8s video), Voice Extraction (static image + audio = voice profile), custom per-shot storyboard, Elements 3.0 (video-clip-based identity locking).

**Kling 3.0 Omni Edit** — new entry: reference-guided video transformation at 3.0 quality tier.

**Kling O1 Video** — new dedicated entry: Chain-of-Thought (CoT) reasoning pre-render, up to 7 simultaneous reference inputs, start/end frame mode, motion transfer from reference video.

**Kling O1 Video Edit (Edit Video tab)** — new entry (entire tab was undocumented):
- Relight & Atmosphere: 3D geometry-aware lighting transformation (featured UI capability)
- Full edit type catalog: Restyle, Object swap, Add elements, Delete/remove, Scene transformation, Angle change, Character replacement
- The Keep Rule prompt formula: `Change [Target] to [New State], keep [everything else] unchanged`
- 5 example edit prompts. Auto settings toggle. Input: 3–10s video + up to 4 image refs, output: 720p.

**Kling Motion Control** — new entry: up to 30s duration (longest in lineup), camera path control.

**Kling 2.5 Turbo, 2.1, 2.1 Master** — new entries: fast iteration tier and legacy tier context.

**Quick Decision Table** — expanded from 10 to 20 rows covering full Kling family + edit mode.

### model-guide.md — Full Rewrite
- Video table: 8 → 15 models, added Duration and Audio columns
- Image table: updated Seedream entries with correct capability notes
- Decision flowchart: added Edit Video branch, full Kling sub-tree, Seedream image sub-tree
- New section: Kling Generation vs Edit Mode with two-tab distinction and edit prompt formula
- Camera/preset compatibility tables updated with Kling 3.0 and Motion Control

---

## v1.3.1 — 2026-02-28

### image-models.md — Seedream Family Expansion

**Seedream 5.0 Lite** — full capability documentation: online search/real-time data grounding, deep reasoning for long complex prompts (1,000+ chars), native multi-image output, complex layout generation. Prompt tips for each.

**Seedream 4.5** — full capability documentation: enhanced reference consistency (face/lighting/identity), accurate multi-image editing (stable with 10+ refs), dense text/typographic rendering, specific editing capabilities (selective deletion, material swap, in-image translation, font/color edits).

**Seedream family** — architecture context note added (DiT + high-compression VAE, bilingual training, RLHF pipeline).

### higgsfield-models/SKILL.md — Seedream Section Expansion
- Added Seedream 5.0 Lite entry. Expanded Seedream 4.5 entry. Quick decision table: 2 new rows.

---

## v1.3.0 — 2026-02-28


### higgsfield-cinema — Complete Rewrite

Major corrections and additions based on actual Cinema Studio 2.0 UI review:

**Elements system (new — was completely missing):**
Characters, Locations, Props — create once, call via `@` in any prompt.
Full creation workflow. Multi-element prompt examples. `@` + Soul ID combination rules.

**Image Mode cameras — corrected (all previous names were wrong):**
Correct camera bodies: Premium Large Format Digital, Classic 16mm Film, Modular 8K Digital,
Full-Frame Cine Digital, Studio Digital S35, Grand Format 70mm Film.
Correct lenses: Creative Tilt Lens, Compact Anamorphic, Halation Diffusion, Extreme Macro,
70s Cinema Prime, Warm Cinema Prime, Swirl Bokeh Portrait, Vintage Prime,
Classic Anamorphic, Clinical Sharp Prime.
Focal lengths corrected: 8mm, 14mm, 35mm, 50mm.
Aperture options: f/1.4, f/4, f/11.

**Genre list — corrected:**
Previous (wrong): Action/Horror/Comedy/Suspense/Drama/Romance.
Correct: General/Action/Horror/Comedy/Western/Suspense/Intimate/Spectacle.

**Director Panel — all 18 camera movements documented:**
Static, Handheld, Zoom Out, Zoom In, Camera Follows, Pan Left, Pan Right,
Tilt Up, Tilt Down, Orbit Around, Dolly In, Dolly Out, Jib Up, Jib Down,
Drone Shot, Dolly Left, Dolly Right, 360 Roll (+ Auto).

**Speed Ramp — new (was missing):**
Linear, Slow Mo, Speed Up, Impact, Auto, Custom. Custom curve via blue line nodes.

**Shot modes — fully documented:**
Single Shot, Multi-Shot Auto, Multi-Shot Manual (6 scenes, full per-scene config).
Cost transparency: Multi-Shot Manual × 4 variations = 24 generations.

---

## v1.2.0 — 2026-02-28

### New Sub-Skills

**higgsfield-vibe-motion** — Complete Vibe Motion guide
- Core concept: Vibe Motion generates Remotion code, not pixel sequences — deterministic,
  not predictive. Text is always crisp. Edits are non-destructive.
- Powered by Claude (Anthropic) + Remotion open-source framework
- Full chat-based workflow: describe → upload assets → apply template → refine
- Color palette presets (Mosaic, Prism, Candy, Minimal, Dark, Brand)
- Animation Speed / Physics slider documentation
- Real-time editing controls (Font Family, Text Color, Font Size, Background, Speed)
- Template categories: Text Animation, Infographics, Posters, Brand, Social, Product
- Prompting patterns for: typography, logo animation, infographics/stats, social motion
  graphics, product feature animation — all with fill-in-the-blank examples
- Vibe Motion vs other Higgsfield tools decision guide
- Combining Vibe Motion with video generation: 3 practical patterns (titles + cinematic,
  product ad intro/outro, full social ad chain)
- Technical notes: 4K output, Remotion code export, data-driven animation capabilities

**higgsfield-pipeline** — End-to-end production chain skill
- Master production chain documented: Popcorn → Seedream → Animate → Recast →
  Lipsync → Vibe Motion → Upscale → Assembly (all 8 stages)
- Pipeline A: Cinematic Short Film (full chain, character-consistent narrative)
  - Stage-by-stage prompting templates with full example short film sequence
  - Model selection matrix by scene type
  - I2V animation prompt structure for multi-scene consistency
- Pipeline B: Social Content Series (Soul ID + Moodboard locked, batch generation)
  - Per-post prompt template
  - Example 3-post series with consistent character and style
- Pipeline C: Product Campaign (hero video + variants + social cuts)
  - Product hero prompt structure
  - App integration (Click to Ad, Packshot, Giant Product)
- Pipeline D: Fast Iteration / Speed Run (5 creative directions in under an hour)
- Pipeline decision guide (which pipeline for which goal)
- 5 named pipeline pitfalls with specific fixes

### Root SKILL.md Updates
- Version bumped to 1.2.0
- Routing table: 8 new rows for `higgsfield-vibe-motion` and `higgsfield-pipeline`
- Sub-skills index: 2 new entries

---

## v1.1.0 — 2026-02-28


### New Sub-Skills

**higgsfield-cinema** — Cinema Studio 2.0 complete workflow
- Full 8-step production workflow (Script → Reference → Optical Stack → Hero Frame →
  Camera Config → Start/End Frames → Generate → Export)
- Optical physics engine documentation: camera bodies (ARRI ALEXA, Panavision, Sony VENICE,
  RED, 16mm, Super 8), lens types (16mm–135mm + Anamorphic), aperture/depth of field
- Reference Anchor system — how to lock character geometry across shots
- Manual Multi-Shot mode — 12-second sequences broken into up to 6 segments
- Cinema Studio vs standard generation decision guide
- Higgsfield Popcorn (storyboard tool) integration and workflow
- Cinema Studio prompting format (adds optical stack + Reference Anchor)
- Genre selection (Action, Horror, Comedy, Suspense, Drama, Romance)
- Keyframe Interpolation — Start/End Frame for morph-free transitions
- Model selection matrix for Cinema Studio specifically

**higgsfield-moodboard** — Style definition and visual consistency
- Soul Moodboard workflow (collect → upload → synthesize → export as modifier)
- Soul Hex color transfer — extract palette from any reference image
- Project-level style modifier template
- Moodboard + Soul ID integration for complete character + aesthetic consistency
- AI Influencer campaign moodboard workflow
- When to use moodboard vs inline style descriptions

**higgsfield-mixed-media** — Complete preset library
- Full 50+ Mixed Media preset catalogue organized by category
  (Textural, Light & Atmosphere, Geometric & Digital, Organic & Elemental,
  Vintage & Film, Social / Trend, Surreal / Dark)
- Each preset: name, visual look, best use cases
- Layer Mixed Media feature — stacking presets
- Effective preset combination table
- Mixed Media vs Visual Styles decision guide
- Social content series strategy using presets

**higgsfield-assist** — GPT-5 copilot + credit optimization
- Higgsfield Assist feature (GPT-5 powered, at higgsfield.ai/chat)
- What Assist can do + how to use it
- Claude skill vs Assist — when to use each
- Coming features in Assist
- Complete credit optimization guide:
  - Plan comparison table with credit counts and costs
  - Credit cost tiers by model
  - 5 most common credit waste patterns + fixes
  - Hero Frame Efficiency Method (the single highest-leverage technique)
  - Model selection by budget scenario (tight/mid/high)
  - Platform efficiency tips (presets, community gallery, batching, etc.)
  - 4-week platform learning path

### Additions to Existing Skills

- `higgsfield-models` — Added Kling O1, Veo 3.1, Seedance 2.0 to video model list
- `higgsfield-apps` — Added Nano Strike, Nano Theft, Vibe Motion, UGC Factory,
  Draw to Video, Photodump Studio
- `SKILL.md` — Updated routing table to include new v1.1 sub-skills
- `references/model-guide.md` — Updated decision flowchart with Wan 2.6, Kling 3.0

### Known Gaps (v1.2 targets)
- Vibe Motion workflow (chat-based video generation)
- UGC Factory deep-dive workflow
- Contest / challenge strategy prompts
- Draw to Video and Sketch to Video workflows
- Kling O1 (reasoning-based video) specific prompting
- Multi-reference image generation workflow
- Upscale / Topaz post-processing workflow
- Community strategy and sharing best practices

---

## v1.0.0 — 2026-02-28

### Initial Release

**Core files:**
- `SKILL.md` — Root entry point with MCSLA formula and full workflow
- `README.md` — Installation and usage guide

**Sub-skills:**
- `higgsfield-prompt` — MCSLA formula, T2V vs I2V, narrative structure
- `higgsfield-models` — All video + image models with decision flowchart
- `higgsfield-camera` — Complete camera control library (40+ controls)
- `higgsfield-motion` — 100+ named motion presets organized by category
- `higgsfield-style` — Five named styles + color grades + lighting vocabulary
- `higgsfield-soul` — Soul ID character consistency + AI Influencer workflow
- `higgsfield-apps` — 80+ one-click Apps organized by use case
- `higgsfield-recipes` — 9 genre templates
- `higgsfield-troubleshoot` — 10 failure patterns + pre-generation checklist

**References:**
- `vocab.md` — Full vocabulary for camera, shot size, style, lighting, atmosphere
- `model-guide.md` — Head-to-head comparison tables + decision flowchart
- `prompt-examples.md` — 18 original example prompts
