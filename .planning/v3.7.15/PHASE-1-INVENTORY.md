# v3.7.15 — Phase 1 Locked Inventory + Decisions Register

**Date:** 2026-05-18
**Carry-forward from Phase 0 (`PHASE-0-VERIFICATION.md`):** 4 full pillar gaps + 1 partial-coverage-with-additive-content (Negative Space). Disposition TRANSLATE-WITH-VERIFICATION. Content-translation-only arc, $0 probe budget. Substrate inherited: v3.7.14 DVC pipeline + `--dry-run` + `.planning/<version>/` convention.
**Convention:** `.planning/<version>/PHASE-1-INVENTORY.md` per v3.7.13 → v3.7.14 pattern.

---

## §1A — File-by-file change inventory

Every file touched by v3.7.15, ordered roughly by Phase 2 sequencing. LoC estimates are conservative ceilings.

### MODIFIED: `vocab.md` (371 lines → ~520-540 lines)

The substantive content work. Five surfaces across two existing top-level sections:

**Surface 1 — § Camera Movement Terminology (currently L3-92):** three new `###` subsections inserted after § Motion Hierarchy (L81-90), before the closing horizontal rule at L92.

- `### Camera Contract` — ~25-35 lines. Prompt-discipline pattern: state camera behavior as an explicit rule; reinforce in negative prompt. Includes 3-4 example camera-contract patterns (static locked-off, slow push-in, single handheld drift). Cross-references the existing § Cut & Continuity → "Camera character" entry at L62, which catalogs the mode-of-motion taxonomy this pillar's contracts choose from.
- `### Motion Physics Anchor` — ~30-40 lines. Speed-specification vocabulary: physical analogies + time-anchored measurements. 4-6 analogy examples + 4-6 time-anchor patterns. Explicit cross-reference to § Subject & Character → Movement Quality (L205-209) noting the orthogonal-vocabulary relationship (per D6).
- `### Lens Behavior Sequence` — ~30-40 lines. Cause-effect focus-event structure (trigger → shift → state → return → repeat). Vocabulary block: focus-breathing, bokeh silhouette, lens plane crossing, anamorphic rendering. Cross-references the existing Rack Focus entry at L26 (which is the bare-bones focus-shift vocabulary this pillar extends).

**Surface 2 — § Composition Vocabulary (currently L334-342, flat-bullet structure):** restructure from flat bullets to `###` subsections (per D7) to accommodate Spatial Zoning's multi-paragraph content and Negative-prompt reinforcement as a peer entry. Net structural change: existing 3 flat bullets become 3 `###` subsections, plus 2 new `###` subsections.

Post-restructure ordering:
- `### Negative-prompt reinforcement` — NEW. ~10-15 lines. Cross-cutting compositional discipline used by Camera Contract / Spatial Zoning / Negative space. Captures the pattern + 2-3 examples drawn from each context. (Per D10.)
- `### Spatial Zoning` — NEW. ~25-35 lines. Named-region system + per-region rule grammar + negative-prompt cross-reference. 3-4 region-naming conventions + 3-4 zone-rule examples. (Per D5 placement, D11 translation rule.)
- `### Negative space` — EXPANDED. Existing single bullet at L338 (~3 lines) becomes a `### Negative space` subsection (~10-12 lines) with added negative-prompt reinforcement note + binding to Spatial Zoning + optionally 1-2 quoted evocative naming examples. **Existing prose preserved verbatim; expansion is additive only.** (Per D7, D11.)
- `### Crossing rule` — UNCHANGED prose, restructured from flat bullet at L339 to `### Crossing rule` subsection. (Per D7 house-style alignment.)
- `### Coordinate notation` — UNCHANGED prose, restructured from flat bullet at L340 to `### Coordinate notation` subsection. (Per D7 house-style alignment.)

**Net vocab.md LoC delta:** +150 to +170 lines (4 new sections + 1 expansion + 3 structural-only changes that swap bullet markup for `###` headings).

**House-style notes:**
- All new sections follow the production-direction register used across vocab.md: name physical mechanisms, avoid metaphysical claims about the model, terse-to-medium register.
- Per-pillar translation rules from §1G applied mechanically during composition.
- Section divider conventions: existing `---` horizontal rules between top-level `##` sections preserved. No new top-level `##` sections introduced (per D5 Option-A lock).
- Cross-reference notation: `(see § <section name>)` for in-document refs, `(see [skills/.../SKILL.md](...) § <name>)` for cross-skill refs — matches existing vocab.md L78/L90/L323/L330/L340 patterns.

### MODIFIED: `skills/higgsfield-marketing-studio/cross-surface-workflow.md` (L417)

One-line update. Current text:

> `| Cinematic prompt-pattern vocabulary (Camera Contract, Motion Physics Anchor, etc.) | **Deferred** — \`cinematic-motion-language.md\` translation to \`vocab.md\` is a follow-up release; 4 of 5 pillars are partial-or-no-coverage gaps |`

Phase 2 replacement: change "Deferred — ... is a follow-up release" to closure language pointing at v3.7.15 with section cite. Proposed text (Phase 2 may refine):

> `| Cinematic prompt-pattern vocabulary (Camera Contract, Motion Physics Anchor, etc.) | **Shipped in v3.7.15** — translated to \`vocab.md\` § Camera Movement Terminology (Camera Contract, Motion Physics Anchor, Lens Behavior Sequence) + § Composition Vocabulary (Spatial Zoning, Negative space) |`

Net delta: 1 line edit, 0 lines net added.

### MODIFIED (OPTIONAL): `DISCIPLINE.md` § Anti-Bombast L176-180

OPTIONAL refinement. Existing "Demonstrated in" line cites `vocab.md § Scene-physics lighting` as the demonstration of the named-physical-mechanism translation discipline. Motion Physics Anchor is a sibling demonstration of the same discipline applied to motion-speed. Phase 2 can OPTIONALLY extend the "Demonstrated in" citation to read:

> `vocab.md § Scene-physics lighting (replaces stylistic adjectives with named physical mechanisms) + vocab.md § Motion Physics Anchor (extends the same discipline to motion-speed specification) + the seedance-2-pro-director skill's anti-empty-words discipline...`

Phase 2 call. Cost: 1 line edit. Value: makes the cross-section discipline visible. Neutral on whether to ship — Phase 2 can defer to a future DISCIPLINE.md refresh if scope feels tight.

### MODIFIED: Root `SKILL.md` (L15-16)

Standard version-cascade pattern matching v3.7.10 → v3.7.11 → v3.7.12 → v3.7.13 → v3.7.14:

- L15: `  version: 3.7.14` → `  version: 3.7.15`
- L16: `  updated: 2026-05-18` → `  updated: <ship date>` (same-day cascade if shipped today; otherwise the actual ship date)

Net delta: 2 lines edited, 0 lines added/removed.

### MODIFIED: `README.md` (L1 + L262)

Same version-cascade pattern:

- L1: `[![Version](https://img.shields.io/badge/version-3.7.14-blue)](...)` → `version-3.7.15`
- L262: `Built February 2026 · v3.7.14 (updated 2026-05-18)` → `v3.7.15 (updated <ship date>)`

Net delta: 2 lines edited.

### MODIFIED: `CHANGELOG.md`

New v3.7.15 entry inserted above existing v3.7.14 entry at line 3. Following v3.7.14's prose-style template (lead paragraph + Added + Changed + Verification + Scope acknowledgment + Backlog updates).

Sketch entry — Phase 2 §2E composes the final prose:

```markdown
## v3.7.15 — <ship-date>

Content-translation patch release closing the cinematic-motion-language.md → vocab.md
gap-fill arc carried since v3.7.13. Adds 4 new vocabulary sections to vocab.md (Camera
Contract, Motion Physics Anchor, Lens Behavior Sequence, Spatial Zoning) and expands
the existing Negative space entry with negative-prompt reinforcement pattern + zone-
binding to Spatial Zoning. Translates Adil Aliyev's 5-pillar cinematic-motion-language
framework to our skill's voice and register per the TRANSLATE-WITH-VERIFICATION
disposition established in v3.7.13. No infrastructure changes; substrate carries from
v3.7.14 (DVC font + --dry-run smoke gate + .planning/<version>/ artifact convention).

### Source attribution

Adil Aliyev's cinematic-motion-language.md (~8 KB, sibling to marketing-studio-director
and content-factory translated in v3.7.13). 5-pillar system: Camera Contract / Motion
Physics Anchor / Spatial Zoning / Lens Behavior Sequence / Negative Space as
Compositional Tool. Per the v3.7.13 author-signature calibration ("strong craft, weak
provenance"), per-pillar register classification applied during translation: pillar
names + grouping treated as craft synthesis (translated freely to our voice); pillar
vocabulary treated as standard cinematography (adopted close to verbatim); universalizing
claims about model behavior treated as craft opinion at HARD RULE volume (register-
downgraded to "useful pattern" / "common technique" framing).

### Added

- **vocab.md § Camera Movement Terminology → 3 new ### subsections:** Camera Contract,
  Motion Physics Anchor, Lens Behavior Sequence. Placed after § Motion Hierarchy.
- **vocab.md § Composition Vocabulary → 2 new ### subsections:** Negative-prompt
  reinforcement (cross-cutting compositional discipline), Spatial Zoning (named-region
  system).
- **NEW `.planning/v3.7.15/` verification + inventory artifacts:**
  `PHASE-0-VERIFICATION.md` (gap-check + register classification per pillar +
  architectural options) and `PHASE-1-INVENTORY.md` (file-by-file inventory + sub-phase
  ordering + decisions register).

### Changed

- **vocab.md § Composition Vocabulary restructure** — converted from flat bullets to
  ### subsections for house-style alignment with Camera Movement / Visual Style /
  Lighting / Subject & Character (all use ### subsections internally). Negative space
  expanded in-place with negative-prompt reinforcement note + binding to Spatial Zoning.
  Crossing rule and Coordinate notation prose unchanged; markup-only conversion.
- **skills/higgsfield-marketing-studio/cross-surface-workflow.md L417** — "Deferred —
  cinematic-motion-language.md translation" callout updated to closure language pointing
  at the new vocab.md sections.
- **Root SKILL.md** — frontmatter `version: 3.7.14` → `3.7.15`; `updated: 2026-05-18` →
  `<ship date>`.
- **README.md** — version badge (L1) and footer (L262) cascade `3.7.14` → `3.7.15`.
- **docs/user-guide/USER-GUIDE.pdf** — regenerated with v3.7.15 metadata cascade
  (version + updated date appear at header L109, page-1 footer L240, last-page footer
  L1258 per generate_user_guide.py). Page count unchanged from v3.7.14 baseline; vocab.md
  content is not embedded in the PDF (only the filename appears in Section 24 Root Files
  table at L1186), so no content cascade.
- **validate_user_guide.py** — `DEFAULT_BASELINE` retargeted from
  `USER-GUIDE.pdf.baseline-v3.7.14` to `USER-GUIDE.pdf.baseline-v3.7.15`. One-line edit.

### Verification

- `python3 validate.py` — ALL CHECKS PASSED.
- `python3 generate_user_guide.py --dry-run` — exit 0.
- `python3 generate_user_guide.py` — exit clean. Page count unchanged.
- `python3 validate_user_guide.py` against new v3.7.15 baseline — VALIDATION PASSED.

### Scope acknowledgment

Content-translation-only patch release. Out of v3.7.15 scope (deferred to future arcs):

- `gpt-image-2-director` sub-skill — carried from v3.7.13/14 backlog
- `ms_image` ("DTC Ads") full sub-skill — carried from v3.7.13/14 backlog
- `static-ads.md` translation — carried from v3.7.13/14 backlog
- Soul Cinema / Nano Banana Pro sibling director skills — carried (deferred indefinitely)
- `validate.py` subprocess integration of `--dry-run` — carried from v3.7.14
- Courier → DejaVu Sans Mono swap — carried from v3.7.14
- Adil's integrated Prompt Template (source L114-149) — cited as pedagogical artifact, not imported (per Phase 1 D8)
- Adil's Dervish Shot worked example (source L186-209) — cited as pedagogical artifact, not imported (per Phase 1 D9)
- FAQ paragraph at generate_user_guide.py L1236 ("Seventeen platform releases ... this guide (v3.7.12)") — out of scope; stale across v3.7.13/14/15 but historically-versioned content per established practice

### Backlog — updated

- **CLOSED: cinematic-motion-language.md vocab.md gap-fill** (carried from v3.7.13) — 4 new vocab.md subsections + 1 in-place expansion ship in v3.7.15 per the TRANSLATE-WITH-VERIFICATION disposition.
- All other v3.7.14 backlog items unchanged — carry-forward to future releases.
```

Net CHANGELOG.md delta: +~80 lines (one new versioned entry).

### REGENERATED: `docs/user-guide/USER-GUIDE.pdf`

Triggered by version + updated-date metadata cascade (per `generate_user_guide.py` L109/240/1258). vocab.md content does NOT surface in the PDF (verified: L1186 only names vocab.md as a Root Files entry; full vocab content is not embedded). Page count expected to remain unchanged (28 pages per v3.7.14 baseline). No layout reflow expected.

Phase 2 §2D handles regeneration + visual spot-check + new baseline creation.

### NEW: `docs/user-guide/USER-GUIDE.pdf.baseline-v3.7.15`

Byte-for-byte copy of the regenerated PDF; new validator target replacing v3.7.14 baseline. Created by Phase 2 §2D after `generate_user_guide.py` runs clean.

### RETAINED (no edit): `docs/user-guide/USER-GUIDE.pdf.baseline-v3.7.14`

Previous baseline kept in place per the v3.7.12 → v3.7.14 retention pattern. No automatic deletion.

### NOT MODIFIED — explicit non-changes (carry-forward checks)

The following surfaces were audited for cross-reference impact and need NO edit:

- **`generate_user_guide.py`** — no source code change. vocab.md content is not embedded; only the filename appears at L1186 in the Root Files table. Metadata cascade flows automatically via `META['version']` and `META['updated']` from root SKILL.md frontmatter.
- **`validate.py`** — no source code change. The new vocab.md sections are content within an already-tracked file; validate.py's structural checks (frontmatter, paths, JSON schemas) are not affected by vocab.md content additions.
- **`skills/higgsfield-prompt/SKILL.md`** L599 — references `vocab.md § Emotion as Visible Behavior — Channels`. UNCHANGED section. No edit needed.
- **`skills/higgsfield-stack/SKILL.md`** L108 — references `vocab.md` (no specific section). UNCHANGED. No edit needed.
- **`skills/higgsfield-pipeline/SKILL.md`** L853 — references `vocab.md § World Through Recurrence`. UNCHANGED section. No edit needed.
- **`skills/higgsfield-seedance/SKILL.md`** L219, L1039, L1122 — reference `vocab.md § Emotion as Visible Behavior` (L219, L1039) and `vocab.md § Editing Syntax` (L1122). UNCHANGED sections. No edit needed.
- **`skills/higgsfield-cinema/SKILL.md`** L397, L611 — reference `vocab.md` (no specific section / general crane-pan-etc. vocabulary). UNCHANGED. No edit needed.
- **`templates/seedance/multi-character-anchor.md`** L57 — references `vocab.md § Editing Syntax`. UNCHANGED section. No edit needed.
- **`DISCIPLINE.md`** L82 — references `vocab.md § Aspect Ratio`. UNCHANGED section. No edit needed.

**Cross-reference blast-radius verdict:** Zero existing cross-references to vocab.md break under v3.7.15's architectural insertion. All target sections remain at their existing names. New sections are additive only.

### TOTAL DELTA SUMMARY

| Surface | Disposition | Net lines |
|---|---|---|
| vocab.md | content additions + minor restructure | +150 to +170 |
| skills/higgsfield-marketing-studio/cross-surface-workflow.md | 1-line callout closure | ~0 |
| DISCIPLINE.md § Anti-Bombast (OPTIONAL) | 1-line citation extension | ~0 |
| Root SKILL.md frontmatter | version + date cascade | 0 |
| README.md badge + footer | version cascade | 0 |
| CHANGELOG.md | new v3.7.15 entry | +~80 |
| docs/user-guide/USER-GUIDE.pdf | regenerated (metadata-only) | binary refresh |
| docs/user-guide/USER-GUIDE.pdf.baseline-v3.7.15 | NEW baseline | binary |
| validate_user_guide.py DEFAULT_BASELINE | 1-line retarget | 0 |
| `.planning/v3.7.15/PHASE-0-VERIFICATION.md` | already shipped | n/a |
| `.planning/v3.7.15/PHASE-1-INVENTORY.md` | this file | n/a |

Total markdown LoC delta: ~+230 to +250 lines. PDF binary refreshed (no LoC). All other surfaces version-cascade only.

---

## §1B — Architectural insertion decision LOCKED

**LOCKED: Option A — distributed insertion, NO system-level index in vocab.md.**

This diverges from the user's preliminary lean toward Option C. The brief was explicit about re-evaluating with vocab.md structure visible. Re-evaluation reasoning below.

### Re-evaluation against actual vocab.md structure

vocab.md is 371 lines, organized thematic-by-craft-domain across 11 top-level `##` sections. The relevant existing sections for our 4 new pillars are:

- **§ Camera Movement Terminology** (L3-92) — the largest section, 11 internal `###` subsections including Motion Hierarchy and Cut & Continuity Vocabulary. Treats camera-as-craft-domain broadly: vocabulary, movement taxonomy, cut/continuity discipline, motion-layer decomposition. Houses 3 of our 4 pillars naturally (Camera Contract, Motion Physics Anchor, Lens Behavior Sequence).
- **§ Composition Vocabulary** (L334-342) — smallest section, currently 3 flat bullets (Negative space, Crossing rule, Coordinate notation). Houses our remaining pillar (Spatial Zoning) and the in-place Negative Space expansion. Per D7, restructures from flat-bullets to `###` subsections to accommodate.

### Why Option A holds over the user's preliminary Option C lean

The user's Option-C reasoning was "preserves system-level coherence of the 5-pillar framework." Re-evaluating that claim against the actual file:

1. **System-level coherence is preserved by `###` subheadings under Option A, not lost.** A reader scrolling vocab.md sees five new named entities — Camera Contract, Motion Physics Anchor, Lens Behavior Sequence, Spatial Zoning, Negative space — all visible in the table-of-contents at their level. The 5-pillar grouping is Adil's pedagogical scaffolding; our vocab.md doesn't need to import that grouping as a structural element. The pillars are discoverable as named techniques regardless of whether they're listed as "the 5 pillars" anywhere.

2. **vocab.md has no existing precedent for system-level index sections.** Other multi-bullet frameworks in vocab.md — Cut & Continuity Vocabulary (L60-72), Motion Hierarchy (L81-90), Emotion as Visible Behavior — Channels (L219-238), World Through Recurrence (L268-283) — all live as ### subsections within their parent thematic section. None has a dedicated index. Importing one for the 5-pillar framework specifically would treat Adil's grouping as more architecturally privileged than e.g. our own 4-layer Motion Hierarchy or 8-channel Emotion framework — that's not the disposition we want.

3. **Option C's index introduces an indirection layer that costs more than it pays.** Cross-references from sub-skills currently point at exact sections: `vocab.md § Emotion as Visible Behavior`, `vocab.md § World Through Recurrence`, `vocab.md § Scene-physics lighting`. Under Option A, new cross-refs follow the same pattern: `vocab.md § Camera Contract`, `vocab.md § Motion Physics Anchor`. Under Option C, refs would either point at the index ("see § Cinematic Motion Language → Camera Contract" — extra hop) or duplicate at both index and section. Both options add complexity.

4. **The "system" framing is Adil's value-add, not vocabulary-reference value-add.** Adil's contribution is naming + grouping a set of related craft techniques. We adopt the techniques (the vocabulary inside each pillar) per TRANSLATE-WITH-VERIFICATION. We preserve the names. We do NOT need to import the meta-structural framing — that's pedagogical packaging suited to his SKILL.md, not to a vocabulary-reference document.

5. **System-coherence cross-references CAN live INSIDE each pillar section without requiring a separate index.** Each new section can include a single-line callout like `> Part of the 5-pillar cinematic-motion-language framework (see also § Motion Physics Anchor, § Lens Behavior Sequence, § Spatial Zoning, § Composition Vocabulary → Negative space).` That preserves system discoverability without scaffolding a separate index section. Per-pillar callouts cost ~5 lines total across 4 sections; an index section would cost ~15 lines as its own entity.

### Option-A placement under §1A LOCKED:

- Camera Contract → § Camera Movement Terminology → new `### Camera Contract` after Motion Hierarchy (insertion point: after L90, before L92 horizontal rule)
- Motion Physics Anchor → § Camera Movement Terminology → new `### Motion Physics Anchor` after Camera Contract
- Lens Behavior Sequence → § Camera Movement Terminology → new `### Lens Behavior Sequence` after Motion Physics Anchor
- Spatial Zoning → § Composition Vocabulary → new `### Spatial Zoning` (after the new Negative-prompt reinforcement bullet, before Negative space)
- Negative space (EXPANDED) → § Composition Vocabulary → existing entry restructured to `### Negative space` + content expansion

System-coherence preserved via single-line callouts inside each pillar section (per #5 above). No separate index section.

---

## §1C — Motion Physics Anchor ↔ Movement Quality reconciliation LOCKED

**LOCKED: D6 — keep both with explicit framing. No deletion of Movement Quality.**

### Re-evaluation against actual file content

Phase 0 framed this as a contradiction at HARD-RULE volume. Reading the actual texts more carefully, the conflict is narrower than Phase 0 surfaced:

**vocab.md § Subject & Character Vocabulary → Movement Quality (L205-209):**
```
### Movement Quality
- Fluid, jerky, precise, hesitant, confident, stumbling
- Slow-motion, overcranked (high fps = slow playback)
- Undercranked (low fps = fast playback)
- Natural, stilted, mechanical, animal-like
```

**Adil's Motion Physics Anchor (source L37-54):**
```
Give every moving element a speed reference from the physical world, not an adjective.
...
Never use "slow", "fast", "gentle", "subtle" alone — always anchor to physics or time.
```

**The actual scope distinction:**

Movement Quality vocabulary (Fluid / jerky / precise / hesitant / confident / stumbling / Natural / stilted / mechanical / animal-like) describes the **character/quality** of motion — how the motion reads, what it communicates. These are *performance-direction* descriptors. The slow-motion/overcranked/undercranked entries describe **playback rate** (a different concept again — temporal manipulation, not motion-speed).

Motion Physics Anchor (Adil's pillar) addresses **motion speed** — how fast something moves through the frame. The prohibited adjectives in Adil's framing are "slow", "fast", "gentle", "subtle" — adjectives that describe speed, not motion quality.

These are **orthogonal vocabularies**:
- Movement Quality answers: "how does the character move?"
- Motion Physics Anchor answers: "how fast does anything move?"

There is no actual conflict at the vocabulary level. The conflict Phase 0 framed was based on Adil's HARD-RULE volume, not on the substantive content.

### Reconciliation LOCKED:

1. Movement Quality at L205-209 — **UNCHANGED.** Performance-direction vocabulary stays. No deletion. No reframing.

2. Motion Physics Anchor new section — opens with a 1-2 sentence framing that names the orthogonality:

   > Motion Physics Anchor specifies *how fast* a moving element moves through the frame, anchored to physical analogies or time measurements. Distinct from § Subject & Character → Movement Quality (above), which describes the *character* of motion (fluid / jerky / hesitant / confident etc.) — performance direction rather than speed specification. The two vocabularies compose: a character can move with "stumbling" quality (Movement Quality) at "the pace of a clock's hour hand" (Motion Physics Anchor speed).

3. Adil's HARD-RULE prohibition on "slow"/"fast"/"gentle"/"subtle" — register-downgraded per D11 translation rule. Translated as:

   > When motion-speed precision matters, anchor to physics analogies or time measurements rather than adjectives. Adjectives like "slow" or "fast" work as quick-spec for casual prompts but are less reliably interpreted than physical analogies ("like dust suspended in honey") or time anchors ("one full revolution per 10 seconds"). The directional pattern: more specific anchor → more controlled output.

This preserves Movement Quality (no deletion, no contradiction); adds Motion Physics Anchor as a complementary vocabulary; explicitly frames the orthogonality; and translates Adil's HARD-RULE volume into our skill's terse production-direction register.

---

## §1D — Negative Space expansion scope LOCKED

**LOCKED: D7 — Negative Space restructured from flat bullet to `### Negative space` subsection. Existing prose preserved verbatim. Expansion is additive only.**

### Concrete additions to existing L338 content

Existing prose (preserved verbatim as opening sentences of the new subsection):

> Negative space — the deliberately-empty area of the frame that isolates or weighs the subject. Production-direction language: `negative space sits center-left of frame, narrowing as the character advances`. Naming negative space as a compositional element prevents the model from filling it with incidental detail.

Additions (Phase 2 composes final prose):

1. **Negative-prompt reinforcement pattern** — cross-reference to the new `### Negative-prompt reinforcement` subsection (above). Sentence-level: "When negative space is named in the prompt, mirror the exclusion in the negative prompt — see § Negative-prompt reinforcement above."

2. **Binding to Spatial Zoning** — sentence-level cross-reference noting the reciprocal relationship: "Negative space is one named zone type within a Spatial Zoning system (see § Spatial Zoning) — Spatial Zoning declares region rules; Negative space names which regions are deliberately empty."

3. **OPTIONAL: Adil's evocative naming examples** — quoted ONLY if Phase 2 judges that the production-direction register tolerates them. Candidates: "sacred emptiness," "the darkness is active, not background." If included, framed as: 'Production-direction register tolerates evocative naming when the evocation is grounded in a compositional rule — e.g., naming a zone "sacred emptiness" only after the zone has been declared as no-light, no-motion, no-particles.' If Phase 2 judges this register-shift too far from house style, omit; the negative-prompt reinforcement + Spatial Zoning binding alone carry the additive content.

### Estimated LoC

Existing entry: ~3 lines. After expansion + `###` subheading: ~10-12 lines. Net add: ~7-9 lines.

### What is NOT changed

- The original prose is preserved verbatim. Phase 2 must not rewrite the existing sentences.
- The opening definition stays at the top of the subsection.
- No change to neighboring entries (Crossing rule, Coordinate notation) beyond the markup-only flat-bullet → `###` conversion (per D7).

---

## §1E — Source content disposition for Prompt Template (Q4) and Dervish Shot (Q5) LOCKED

### Q4 — Adil's integrated Prompt Template (source L114-149)

**LOCKED: D8 — cite as pedagogical artifact; do NOT import into vocab.md or prompt-examples.md.**

The Prompt Template is a structured brief format integrating all 5 pillars: CAMERA / ASPECT RATIO / DURATION / Style&Mood / Narrative / Action / Lens / Lighting / Spatial Zones / Audio / Quality / Negative Prompt. It is pedagogical scaffolding suited to Adil's standalone skill.

Why not adopted:

1. **MCSLA conflict risk.** Our skill's primary prompt structure is MCSLA (Model · Camera · Subject · Look · Action), documented in `skills/higgsfield-prompt/SKILL.md` and enforced via root SKILL.md HARD RULES item 4. MCSLA + Adil's template are not strictly contradictory — Adil's template can be read as a more granular MCSLA expansion — but introducing a second primary template would crowd. Users would face "which template do I use?" decision overhead.

2. **5-pillar vocabulary stands without the template.** The pillars are USEFUL techniques inside MCSLA layers (Camera Contract within MCSLA's C; Motion Physics Anchor within MCSLA's A; Spatial Zoning within MCSLA's L/C; Lens Behavior Sequence within MCSLA's C/L; Negative Space within MCSLA's S/L). Users get the value of the pillars without needing Adil's specific brief format.

3. **Source remains accessible.** Adil's source file lives in his standalone skill. Users who want the integrated template can read it there. Our skill cites the source corpus (CHANGELOG, sub-skill attribution) so users know where to look for the full pedagogical packaging.

### Q5 — Adil's Dervish Shot worked example (source L186-209)

**LOCKED: D9 — cite as pedagogical artifact; do NOT import into vocab.md, prompt-examples.md, or templates/.**

The Dervish Shot is a single concrete brief demonstrating all 5 pillars together (whirling dervish, hand close-up, golden dust particles, pure black left third, sacred Sufi atmosphere).

Why not adopted:

1. **prompt-examples.md is curated for diverse genres.** Existing examples cover action, horror, romance, sci-fi, etc. Adding a sacred-Sufi-atmosphere example would be a strong genre addition but it would not pedagogically demonstrate the pillars MORE clearly than smaller, more focused examples embedded inside each new vocab.md section.

2. **Per-pillar integrated examples serve the same purpose at smaller scale.** Each new vocab.md section (Camera Contract, Motion Physics Anchor, etc.) can include a 2-3 line worked example demonstrating that pillar's vocabulary in action. These shorter examples sit closer to the vocabulary they illustrate, are easier to scan, and don't require a reader to parse a full 23-line brief to extract the pillar-specific lesson.

3. **The Dervish Shot is recognizable enough that direct adoption would feel like uncredited copying.** Even with attribution, lifting Adil's signature worked example verbatim into our skill would be a register-shift away from "translate to our voice." Per the TRANSLATE-WITH-VERIFICATION disposition, we adopt vocabulary and translate framing; we don't lift complete pedagogical artifacts.

### Optional Phase 2 enhancement

If Phase 2 judges that ONE integrated worked example would help users see the pillars composing together (rather than as isolated techniques), the right approach is to compose a NEW worked example in our skill's voice and genre — not to import the Dervish Shot. This is a Phase 2 judgment call, not a Phase 1 lock.

---

## §1F — Cross-pillar negative-prompt-reinforcement extraction LOCKED

**LOCKED: D10 — extract-once as a new `### Negative-prompt reinforcement` subsection at the top of § Composition Vocabulary. Camera Contract / Spatial Zoning / Negative space all reference back to it.**

### Pattern occurrence across pillars (verified from source read)

| Pillar | Uses negative-prompt reinforcement? | How |
|---|---|---|
| Camera Contract | YES (source L33) | "Always reinforce camera rules in the negative prompt as well." |
| Motion Physics Anchor | NO | Negative-prompt tactic not invoked in the pillar's framing. |
| Spatial Zoning | YES (source L73) | "Always cross-reference spatial zones in the negative prompt." |
| Lens Behavior Sequence | NO | Negative-prompt tactic not invoked in the pillar's framing. |
| Negative Space | YES (source L109-110) | "particles on the left side, light on the left side, movement on the left side" as explicit negative-prompt entries. |

3 of 5 pillars share the technique. Different surface examples; same underlying mechanism.

### Why extract-once over keep-embedded

1. **Single source of truth.** The pattern is the same across all three contexts: name the exclusion in the negative prompt mirror to the positive declaration. Repeating the same explanation in three places creates drift risk over time.

2. **First-class compositional discipline.** The technique is itself a compositional tactic — it's about how prompts compose positive declarations with negative exclusions. That makes § Composition Vocabulary the natural home, alongside Negative space, Crossing rule, Coordinate notation.

3. **Cross-references are cheap; duplication is expensive.** Each pillar that uses the technique adds a 1-line reference: "Reinforce in the negative prompt — see § Composition Vocabulary → Negative-prompt reinforcement." Adding 3 such lines is cheaper than maintaining 3 copies of the pattern's explanation.

### Placement under § Composition Vocabulary

Top of the section (first `###` subsection after the section heading). Reasoning: it's a CROSS-CUTTING discipline that applies across multiple pillars; surfacing it first makes the discipline visible before the specific applications.

Proposed structure:
```
## Composition Vocabulary

(existing intro paragraph)

### Negative-prompt reinforcement      [NEW, cross-cutting]
### Spatial Zoning                       [NEW]
### Negative space                       [EXPANDED]
### Crossing rule                        [UNCHANGED prose, markup converted]
### Coordinate notation                  [UNCHANGED prose, markup converted]
```

### Estimated LoC for new subsection

~10-15 lines. Includes: pattern statement (1-2 sentences), 2-3 example pairs (positive-side declaration + negative-side mirror), cross-references to the pillars that use it (Camera Contract, Spatial Zoning, Negative space).

---

## §1G — Per-pillar translation rule LOCKED

The author-signature calibration from Phase 0 applied per-pillar. Phase 2 composes prose using these rules mechanically.

### Camera Contract

| Element | Disposition |
|---|---|
| State-as-hard-rule discipline (source L24-25) | **ADOPT close to verbatim.** Translate to our voice: "State camera behavior explicitly in the prompt before describing subject or action — the model defaults to its training-prior behavior when camera intent is implicit." |
| "Static locked-off camera. Zero movement. No pan, no zoom, no dolly, no shake." (source L29) | **ADOPT as a quoted example.** Standard cinematography pattern; our skill already uses similar locked-off framing in templates. |
| "Slow push-in only — 10% scale change over the full duration." (source L30) | **ADOPT as a quoted example.** Time-anchored measurement is good craft. |
| "Single handheld drift, slight organic sway, no cuts." (source L31) | **ADOPT as a quoted example.** |
| "The model treats the camera as a character — define it or it will improvise." (source L26) | **DOWNGRADE.** Translate: "When camera behavior is left implicit, the model defaults to its training-prior interpretation, which may not match the intended shot." Strip the metaphysical "treats camera as a character" framing — that's craft-opinion at HARD RULE volume; the production claim sits one level beneath. |
| "Always reinforce camera rules in the negative prompt as well." (source L33) | **ADOPT.** Cross-reference to § Composition Vocabulary → Negative-prompt reinforcement per D10. |

### Motion Physics Anchor

| Element | Disposition |
|---|---|
| Speed analogies (source L42-45): dust/honey, embers/still-air, smoke/cathedral, lake-disturbed-by-drop | **ADOPT close to verbatim.** Useful production-direction examples. May add 1-2 of our own (e.g., from existing prompt-examples.md context) to demonstrate the pattern is extensible. |
| Time-anchored measurements (source L48-51): "one full revolution across the entire 10-second clip" / "roughly 6 degrees per second" / "the pace of a clock's hour hand — imperceptibly slow" / "travels the full arc in 8 seconds with no pause" | **ADOPT close to verbatim.** Highly specific, transferable. |
| "Never use 'slow', 'fast', 'gentle', 'subtle' alone — always anchor to physics or time." (source L53) | **DOWNGRADE per §1C.** Translate to: "When motion-speed precision matters, anchor to physics analogies or time measurements rather than adjectives. Adjectives like 'slow' or 'fast' work as quick-spec for casual prompts but are less reliably interpreted than physical analogies or time anchors." |
| Orthogonality framing vs. § Movement Quality | **NEW (per §1C).** 1-2 sentence framing at top of section explicitly naming the orthogonal-vocabulary relationship. |

### Lens Behavior Sequence

| Element | Disposition |
|---|---|
| Cause-effect structure (source L78-82): "trigger → shift → state → return → repeat" | **ADOPT close to verbatim.** Translatable scaffolding. |
| Worked focus-event example (source L85-87): foreground crossing → focus shift → bokeh → focus return → cycle | **ADOPT close to verbatim** as a quoted example. |
| Vocabulary list (source L90-95): focus-breathing, rack focus, bokeh silhouette, lens plane crossing, anamorphic lens rendering | **ADOPT close to verbatim.** Standard cinematography. Cross-link Rack Focus to its existing entry at vocab.md L26 (avoid duplication — Rack Focus lives in Camera Movement → Zoom; reference back from Lens Behavior Sequence rather than re-defining). |
| "Models can simulate focus-breathing, rack focus, and lens diffusion — but only when the sequence is described explicitly as cause and effect." (source L79-80) | **DOWNGRADE.** Translate: "Models tend to produce cleaner / more reliable focus events when the sequence is described as cause and effect rather than as a single static depth-of-field state." Soften "only when" to "tend to" — the universalizing claim isn't strictly true. |

### Spatial Zoning

| Element | Disposition |
|---|---|
| Region naming conventions (source L62-65): "Left third / center third / right third", "Foreground / midground / background", "Upper half / lower half", "Right two-thirds / left void" | **ADOPT close to verbatim.** Standard cinematography vocabulary. |
| Zone-rule examples (source L68-71): "Left third: pure black, no light, no particles, no movement." etc. | **ADOPT close to verbatim** as quoted examples. |
| "This prevents the model from filling empty space with invented content." (source L59) | **ADOPT.** Falsifiable production claim, directionally correct, defensible. No downgrade needed. |
| "Always cross-reference spatial zones in the negative prompt." (source L73) | **ADOPT.** Cross-reference to § Composition Vocabulary → Negative-prompt reinforcement per D10. |

This is the pillar with the lightest translation needed — Adil's production-direction register sits closest to our house style here.

### Negative space (expansion, not new section)

| Element | Disposition |
|---|---|
| Existing vocab.md L338 prose | **PRESERVE VERBATIM.** No rewrite. |
| Negative-prompt reinforcement pattern (source L109-110) | **ADD as cross-reference** to § Negative-prompt reinforcement (per D10). Sentence-level addition. |
| Binding to Spatial Zoning | **ADD as cross-reference.** Sentence-level. |
| Evocative naming ("sacred emptiness," "active darkness, not background") (source L100, L106-107) | **OPTIONAL.** Phase 2 judgment call. If adopted, frame as 1-2 quoted examples, not as house vocabulary. If omitted, no loss — the negative-prompt reinforcement + Spatial Zoning binding carry the additive content. |

---

## §1H — Sub-phase 2 ordering with STOPs

Seven sub-phases. Estimated total Phase 2 effort: 1-2 sessions depending on prose composition pace.

### 2A. vocab.md content edits (the substantive work)

Largest sub-phase. All 5 surfaces (3 new sections in Camera Movement Terminology, 1 new section + 1 expansion + 1 cross-cutting bullet + 2 markup-only conversions in Composition Vocabulary).

Steps:
1. Add `### Camera Contract` after Motion Hierarchy (before L92 horizontal rule). Apply D11/§1G translation rule.
2. Add `### Motion Physics Anchor` after Camera Contract. Include orthogonality framing per §1C.
3. Add `### Lens Behavior Sequence` after Motion Physics Anchor. Cross-link Rack Focus at L26.
4. Restructure § Composition Vocabulary heading area (L334+): swap flat-bullet markup for `###` subsections.
5. Add `### Negative-prompt reinforcement` as the first subsection.
6. Add `### Spatial Zoning` as the second subsection.
7. Expand existing Negative space bullet into `### Negative space` subsection. PRESERVE existing prose verbatim; add cross-references per §1D.
8. Convert Crossing rule + Coordinate notation flat bullets to `### Crossing rule` and `### Coordinate notation` subsections (prose unchanged).
9. Run `python3 validate.py` — confirm no structural drift introduced.

**STOP for content review.** User reviews the new vocab.md sections before Phase 2 continues. This is the highest-judgment sub-phase; review catches drift from §1G translation rules before downstream work compounds.

### 2B. Cross-reference updates

Steps:
1. Update `skills/higgsfield-marketing-studio/cross-surface-workflow.md` L417: replace "Deferred — ..." with closure language per §1A entry above.
2. OPTIONAL: Update DISCIPLINE.md § Anti-Bombast L176-180 "Demonstrated in" citation per §1A optional entry. Phase 2 call.
3. Run `python3 validate.py`.

**STOP if any cross-reference work surfaces beyond these two.** Phase 1 §1A audited the cross-reference blast radius (all existing vocab.md cross-refs point at unchanged sections) so this sub-phase should be small. If Phase 2 finds additional cross-refs that need updating, surface them before continuing.

### 2C. Version cascade

Mechanical edits:
1. Root SKILL.md frontmatter: version `3.7.14` → `3.7.15`, updated date.
2. README.md L1 badge: version cascade.
3. README.md L262 footer: version + updated date cascade.
4. Run `python3 validate.py` — confirm clean.

### 2D. USER-GUIDE.pdf regeneration (metadata-cascade only)

Mechanical regen:
1. Pre-flight: `python3 generate_user_guide.py --dry-run`. Expect exit 0.
2. Full regen: `python3 generate_user_guide.py`. Expect exit clean, 28 pages (unchanged from v3.7.14).
3. Visual spot-check: open `docs/user-guide/USER-GUIDE.pdf` and verify version-on-page-1 reads `v3.7.15` + updated date matches root SKILL.md frontmatter.
4. Create new baseline: `cp docs/user-guide/USER-GUIDE.pdf docs/user-guide/USER-GUIDE.pdf.baseline-v3.7.15`.
5. Update `validate_user_guide.py` `DEFAULT_BASELINE` constant: `USER-GUIDE.pdf.baseline-v3.7.14` → `USER-GUIDE.pdf.baseline-v3.7.15` (one-line edit at L98).
6. Run `python3 validate_user_guide.py` — confirm pass against new baseline.

**STOP if page count drifts from 28** — would indicate unintended layout reflow that needs investigation before continuing.

### 2E. CHANGELOG.md entry

Prose composition. Insert new v3.7.15 entry above v3.7.14 entry. Follow v3.7.14 prose-style template per §1A sketch. Sections: lead paragraph, Source attribution, Added, Changed, Verification, Scope acknowledgment, Backlog — updated.

### 2F. Full validation pass

Mechanical:
1. `python3 validate.py` — ALL CHECKS PASSED.
2. `python3 generate_user_guide.py --dry-run` — exit 0.
3. `python3 validate_user_guide.py` — VALIDATION PASSED against new baseline.

**STOP for final repo-wide review** before commit. This is the last gate before changes become part of the repo's history.

### 2G. Final repo-wide diff review

Steps:
1. `git status` — confirm only expected files surfaced.
2. `git diff --stat` — confirm LoC delta roughly matches §1A's `+230 to +250` markdown estimate (vocab.md + CHANGELOG.md dominate; everything else cascade-only).
3. Confirm no out-of-scope edits leaked.
4. User approval before commit.

Commit format per project convention: `feat: v3.7.15 — cinematic-motion-language vocab.md gap-fill (4 pillars + Negative Space expansion)`.

After merge: git tag + GitHub release per the project convention surfaced in memory (`feedback_github_releases.md`, `feedback_release_workflow.md`).

---

## §1I — Decisions register

Numbered locks per the v3.7.13 → v3.7.14 convention. Each lock is one row.

| # | Decision | Source | Status |
|---|---|---|---|
| D1 | Arc shape — patch release v3.7.15, content-translation-only, $0 probe budget | Phase 0 §VERIFY 0.5 | LOCKED |
| D2 | Substrate inheritance — v3.7.14 DVC + --dry-run + .planning/<version>/ convention, no changes | Phase 0 closing | LOCKED |
| D3 | Disposition — TRANSLATE-WITH-VERIFICATION carried from v3.7.13 | Phase 0 closing | LOCKED |
| D4 | Negative Space disposition — partial-coverage-with-additive-content (EXTEND, not skip). Net surfaces: 4 new pillar additions + 1 in-place expansion | Phase 0 §0.2b | LOCKED |
| D5 | Architectural insertion — Option A (distributed insertion, NO system-level index). Diverges from user's preliminary Option C lean. Reasoning at §1B above | Phase 1 §1B | LOCKED |
| D6 | Movement Quality reconciliation — keep both with explicit orthogonality framing. No deletion of Movement Quality at vocab.md L205-209 | Phase 1 §1C | LOCKED |
| D7 | Composition Vocabulary restructure — convert from flat bullets to ### subsections for house-style alignment. All 5 entries (3 existing + 2 new) become ### subsections of equal weight | Phase 1 §1D | LOCKED |
| D8 | Prompt Template (source L114-149) disposition — cite as pedagogical artifact; do NOT import. MCSLA remains single primary prompt structure | Phase 1 §1E | LOCKED |
| D9 | Dervish Shot worked example (source L186-209) disposition — cite as pedagogical artifact; do NOT import. Per-pillar integrated examples serve same purpose at smaller scale | Phase 1 §1E | LOCKED |
| D10 | Negative-prompt reinforcement extraction — extract-once as new `### Negative-prompt reinforcement` subsection at top of § Composition Vocabulary. Camera Contract / Spatial Zoning / Negative space cross-reference back | Phase 1 §1F | LOCKED |
| D11 | Per-pillar translation rules — per §1G table. Camera Contract: adopt patterns, downgrade "treats camera as a character" metaphysics. Motion Physics Anchor: adopt analogies/time-anchors, downgrade HARD-RULE prohibition. Lens Behavior Sequence: adopt structure + vocabulary, soften "only when" to "tend to." Spatial Zoning: adopt close to verbatim (lightest translation). Negative space: preserve existing prose verbatim + add cross-refs | Phase 1 §1G | LOCKED |
| D12 | PDF regeneration — triggered by metadata cascade only (vocab.md content does NOT surface in PDF; only filename appears at generate_user_guide.py L1186). Standard regen pattern + new baseline + validator retarget | Phase 1 §1A | LOCKED |
| D13 | cross-surface-workflow.md L417 closure — update "Deferred — ..." callout to closure language pointing at the new vocab.md sections | Phase 1 §1A | LOCKED |
| D14 | DISCIPLINE.md § Anti-Bombast extension — OPTIONAL. Phase 2 may extend "Demonstrated in" citation to include vocab.md § Motion Physics Anchor. Neutral on whether to ship | Phase 1 §1A | OPTIONAL — Phase 2 call |
| D15 | Out-of-scope items surfaced — FAQ paragraph at generate_user_guide.py L1236 ("Seventeen platform releases ... this guide (v3.7.12)") is stale across v3.7.13/14/15. Explicitly deferred per established practice. Not touched in v3.7.15 | Phase 1 §1A | LOCKED-AS-DEFERRED |
| D16 | System-coherence preservation under Option A — single-line callouts inside each pillar section ("Part of the 5-pillar cinematic-motion-language framework, see also § X, § Y, § Z") rather than a dedicated index section. Cost: ~5 lines total across 4 pillars vs. ~15 lines for a separate index | Phase 1 §1B | LOCKED |
| D17 | Source attribution — Adil Aliyev credited in CHANGELOG (Source attribution section), at top of each new vocab.md pillar section (1-line citation), and in PHASE-0/PHASE-1 verification artifacts. Per v3.7.13 attribution convention | Phase 1 §1A CHANGELOG sketch | LOCKED |

---

## Phase 1 closing summary

**Scope verified:** 4 new vocab.md sections + 1 in-place expansion + § Composition Vocabulary markup-only restructure + 1 cross-surface-workflow.md callout closure + OPTIONAL DISCIPLINE.md extension + standard version cascade + PDF regen + new baseline.

**Cross-reference blast radius:** ZERO. All existing vocab.md cross-references from sub-skills, templates, and DISCIPLINE.md point at sections that remain unchanged.

**Architectural lock:** Option A (distributed insertion) — diverges from user's preliminary Option C lean. Reasoning documented at §1B; user can override before Phase 2A begins.

**Movement Quality conflict:** narrower than Phase 0 framed it. Movement Quality covers character motion CHARACTER; Motion Physics Anchor covers motion SPEED. Orthogonal vocabularies. No deletion needed.

**Per-pillar translation rules:** locked in §1G. Phase 2 composes prose mechanically following the per-element ADOPT/DOWNGRADE table.

**Estimated total Phase 2 effort:** 1-2 sessions. Largest sub-phase is 2A (content composition). All other sub-phases are mechanical.

**Open user decisions before Phase 2A:**
- Confirm or override D5 (Option A architectural insertion vs. preliminary Option C lean)
- Confirm D14 disposition (extend DISCIPLINE.md § Anti-Bombast or defer)
- Any per-pillar translation-rule overrides in §1G

---

**STOP. Awaiting user review before Phase 2A begins.**
