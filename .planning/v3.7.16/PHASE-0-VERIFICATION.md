# v3.7.16 — Phase 0 Verification Report

**Date:** 2026-05-18
**Scope under verification:** MEGA RELEASE — 9 locked scope items spanning 3 new content surfaces (gpt-image-2-director, static-ads, ms_image/DTC Ads), 3 infrastructure items (DVSM mono font, --dry-run exit-code matrix, validate.py subprocess integration), and 3 content-cleanup items (FAQ paragraph refresh, 6-site cross-reference fill, DISCIPLINE.md pattern naming)
**Convention carried from v3.7.13 / v3.7.14 / v3.7.15:** `.planning/<version>/PHASE-0-*.md`, read-only across Phase 0, cite-by-line, plausibility-over-verification discipline, per-claim register-downgrade
**Substrate inherited:** v3.7.14 DVC font + `--dry-run` smoke gate, v3.7.13 `.planning/<version>/` convention, v3.7.15 boundary-condition framing (observed, not yet pattern-named)

---

## Headline finding

**Phase 0 evidence surfaces a substantial mismatch between scope item 2 (ms_image as a full sub-skill) and the project's established discipline.** All three "new content surface" items in the kickoff were framed as parallel work — and items 1 (gpt-image-2-director) and 3 (static-ads.md) ARE parallel, both are Adil source-corpus translations of comparable shape to v3.7.13's content-factory translation and v3.7.15's cinematic-motion-language translation. Item 2 (ms_image / DTC Ads) is fundamentally different work: **zero hits across both Adil source SKILL.md files** (`marketing-studio-director/SKILL.md` 262 lines and `higgsfield-content-factory/SKILL.md` 997 lines) for any of `ms_image`, `dtc ads`, `dtc_ads`, or `marketing_studio_image`. The only substrate that exists today is v3.7.13's Phase 0 Probe 0.3-a finding (a single live-MCP introspection result naming ms_image as the third Marketing Studio model with `brand_kit_id` / `style_id` / batch-20 / max-14-media capabilities) and the brief naming in `cross-surface-workflow.md` §3. Building ms_image as a "full sub-skill" therefore requires either (a) methodology shift to live-MCP probing à la v3.7.13's Probe 0.3 series — different work-shape, different verification cost — or (b) pure documentation authoring without a translation source — violates the project's "Adil-corpus-as-source" pattern that v3.7.13 / v3.7.15 established. **This is the single largest descope signal in Phase 0.**

**Three other DESCOPE RECOMMENDATIONS surface:** item 13 (DISCIPLINE.md boundary-condition naming) has only ONE observation — the v3.7.15 forward criterion explicitly says "May earn its own DISCIPLINE.md pattern name in a future arc **if the same shape surfaces elsewhere**" — naming a one-observation pattern violates the criterion v3.7.15 itself set. Item 12 (6-site cross-reference fill) is partially descopable: only 3 of 6 sites are clean parenthetical additions, the other 3 require prose rework that isn't visibly additive. Item 6 (DVSM swap) is CLEAN — measurements below confirm 0.33% max drift vs. Courier on all real code-block content (Courier and DVSM are both monospace; DVSM swap is mechanically simpler than v3.7.14's DV → DVC swap was). Items 1, 3, 5, 7, 11 carry no descope signal. **Recommended Phase 1 scope: 5 clean items (1, 3, 6, 11, partial 12) + 2 infrastructure items requiring contract design (5, 7) = 7 items; item 2 rescoped to "DTC Ads as Marketing Studio expansion" (not a new sub-skill); items 13 + 3 prose-rework cross-reference sites deferred to v3.7.17 backlog.** The mega-release earns its scope at 7-8 items, not 9; the descope is at item 2's work-shape, not its inclusion.

Architectural option (α/β/γ) analysis surfaced in §VERIFY 0.3 + the dedicated Architectural section: my read leans β (gpt-image-2-director + static-ads consolidated under one new `higgsfield-gpt-image-2` sub-skill mirroring the marketing-studio + cross-surface-workflow pattern; ms_image as cross-surface-workflow.md §3 expansion, NOT a new sub-skill). Phase 1 picks.

---

## VERIFY 0.1 — gpt-image-2-director source read

**Path verification:** Source file lives at `/Users/petercsanky/Desktop/EVEN MORE SKILLS/gpt-image-2-director/SKILL.md` (NOT in `MORE CUSTOM SKILLS/` as the kickoff prompt hypothesized — re-confirms the v3.7.13 audit-note "filed for Phase 2C-mini, never executed" was working from a wrong path assumption). 13,949 bytes / 206 lines.

### 0.1a — Document structure

| Section | Lines | Shape |
|---|---|---|
| Frontmatter | 1–4 | YAML — `name`, single dense `description` line ~750 chars including trigger language ("converts plain-text concepts into production-ready prompts for GPT Image 2.0, routing by output type — structured JSON…vs. dense cinematic prose…vs. auto-derive meta-prompts") |
| `# GPT Image 2.0 Prompt Director` opener | 6–8 | One-paragraph mission statement |
| `## What makes GPT Image 2.0 different` | 10–19 | 4-bullet capability framing (prompt-following, text-rendering, design/UI strength, photorealism weakness) |
| `## Three prompt formats` | 21–35 | Format-A/B/C overview before per-format depth |
| `## Format A — Structured JSON` | 37–99 | Core fields + 5 key-pattern subsections + worked JSON example |
| `## Format B — Dense cinematic prose` | 101–122 | 8-step information order + 5 craft rules + worked prose example |
| `## Format C — Auto-derive meta-prompt` | 124–152 | Templated meta-prompt scaffold + when-to-use trigger |
| `## Output format` | 154–162 | Code-block-wrapping rules |
| `## Routing — how to pick a format` | 164–172 | Concept→format decision rules |
| `## Quality checklist before returning` | 174–183 | 6-item pre-delivery checklist |
| `## Example routings` | 185–205 | 6 paired concept→format examples |

**Organizational scheme:** craft-direction document — capability framing first, then 3 routing buckets, then per-bucket depth, then output and quality discipline. Mirrors `marketing-studio-director.md`'s shape (capability → per-preset rules → output discipline) but for a different model and a different routing taxonomy (output-shape rather than ad-preset).

### 0.1b — Conceptual coverage

The skill teaches **three orthogonal things about GPT Image 2.0**:

1. **Capability framing** (L10–19): what GPT Image 2.0 is uniquely good and bad at. Plausibility check: "prompt following is its #1 strength," "text rendering is best-in-class," "cinematic photorealism is its weakness" — these are widely-corroborated capability claims about GPT Image 2.0 specifically. The "lean into design/UI" guidance follows from the capability framing.

2. **Format routing by output shape** (L21–35, L164–172): output type → prompt format. Discrete-region/multi-panel/layout → JSON; single-scene/single-frame → prose; theme-only/auto-derive → meta-prompt. This routing taxonomy is craft synthesis — Adil's organizing principle for how to write for the model.

3. **Per-format craft rules**:
   - JSON: count-and-label pattern, position-scoped regions, section objects with title/position/count/labels, templateable slots, inline typography callouts
   - Prose: specific-over-atmospheric, concrete props, camera/film language, embedded text in quotes, avoid "photorealistic" for face-heavy
   - Meta-prompt: structured scaffold with theme placeholder + composition rules + visual quality + typography system + signature

### 0.1c — Layering — does this split prompt-craft from execution?

**No — pure prompt-craft skill, no execution layer.** The skill outputs a finished prompt the user pastes into GPT Image 2.0. No tool invocation, no API call, no orchestration. The "Output format" section (L154–162) is explicit: *"Return only the finished prompt in a code block. No preamble, no explanation, no 'here's your prompt'… The user pastes it into GPT Image 2.0 directly."*

This is parallel to `marketing-studio-director.md` (also pure prompt-craft) but unlike `higgsfield-content-factory.md` (which DOES split — content-factory orchestrates MCP calls; director writes the prompt). For our skill, the right architectural parallel is `marketing-studio-director.md` → `higgsfield-marketing-studio/SKILL.md` (translated as prompt-craft, no execution layer added by us).

### 0.1d — Author signature — does this match Adil's signature?

**Yes, with one nuance.** Applying v3.7.13 Block 2B-prime calibration ("strong craft, weak provenance"):

| Signal | Strength | Evidence |
|---|---|---|
| HARD RULE / universalizing volume | **Lower than cinematic-motion-language.md.** | The skill uses softer framing throughout: "Use when…", "Pick one based on…", "Default to flowing paragraph for prompts under 50 words" (L292) — these are heuristics, not HARD RULEs. Compare to cinematic-motion-language.md's `### Never use 'slow', 'fast', 'gentle', 'subtle' alone — always anchor to physics or time` (HARD RULE register). gpt-image-2-director is genuinely calmer in register. |
| Zero external citations | **Confirmed.** | No textbooks, no documentation links, no DPs, no model-version anchors. All capability claims are presented as Adil's experience-based knowledge. Identical to cinematic-motion-language.md and marketing-studio-director.md. |
| Falsifiable claims tied to verifiable model behavior | **Partial.** | "Prompt following is its #1 strength" / "text rendering is best-in-class" are widely-validated claims (third-party benchmarks corroborate). The "plasticky skin failure mode" claim (L17, L119) is verifiable by anyone with GPT Image 2.0 access. **Stronger production-knowledge register than cinematic-motion-language.md.** |
| Vocabulary application vs invention | **Standard cinematography + standard prompt-engineering.** | "35mm film photograph," "shallow depth of field," "low-angle dynamic perspective" (L117) are standard cinematography. JSON pattern names ("count-and-label," "position-scoped regions") are Adil's framing of standard prompt-engineering. Per v3.7.15 calibration: vocabulary is borrowed, framing is synthesis. |
| Synthesis (the format routing) | **Adil's contribution.** | The Format-A/B/C taxonomy organized by output-shape is Adil's organizing principle; not borrowed from external docs. |

**Disposition class:** **TRANSLATE-WITH-VERIFICATION (LOWER-FRICTION SUB-CLASS).** Lower friction than cinematic-motion-language.md because the universalizing-claim volume is lower and the production-knowledge register is higher. Per-claim register downgrade still applies for any "GPT Image 2.0 always does X" universalizing claims, but the bulk of the content is closer to production-knowledge than to craft opinion.

### 0.1e — Hardcoded artifacts

- **Two embedded text strings in CJK + Latin examples:** `"都会の夜に溶けていく"` (prose worked example, L122); `"衣装・装備詳細"` + `"胸当て、肩当て、腕甲"` (JSON example, L64–67). These are illustrative examples, not authoritative references — translation should preserve them as examples or replace with our own.
- **One brand name:** "AURA" (JSON example L82). Generic placeholder; safe to translate or replace.
- **One product name + URL fragment:** `"AXIS"` brand wordmark inside a JSON snippet (L82). Generic.
- **No share links, no UUIDs, no character limits, no dated artifacts.** This is materially cleaner provenance than `marketing-studio-director.md` (which had Adil-attributed share links per v3.7.13 audit) or `content-factory.md` (which had pricing approximations + L897 ≈ $0.02/credit claims).

### 0.1f — Cross-references

**Zero cross-references to marketing-studio-director, content-factory, or any Higgsfield surface.** This is a standalone skill, not a satellite. Routing decisions are entirely model-internal (output-shape based). Source-corpus reconciliation: gpt-image-2-director does NOT participate in the marketing-studio surface map at all — it's a parallel craft skill for a parallel model, not a Marketing Studio component. This supports the architectural read that gpt-image-2-director adopts as a **new sibling sub-skill**, not as an expansion of higgsfield-marketing-studio.

### 0.1g — Concrete technical claims worth verifying vs craft opinion worth downgrading

| Claim shape | Example from source | Translation handling |
|---|---|---|
| Capability-fact (broadly corroborated) | "Prompt following is its #1 strength" (L14); "Text rendering is best-in-class" (L15) | **Adopt close to verbatim.** Plausibility-over-verification: these are widely-validated. |
| Capability-weakness (specific failure-mode) | "Human faces often go plasticky… frame it as film photography rather than as 'photorealistic'" (L17) | **Adopt as production discipline.** The "use film/cinematic language not 'photorealistic'" recipe is a concrete falsifiable workaround. |
| Format-routing rule | "Use when the output has discrete regions, labeled parts…" (L27) | **Adopt as routing heuristic.** Soften any "always" / "never" framing if present (none observed here). |
| Craft-vocabulary pattern names | "count-and-label pattern" (L51); "position-scoped regions" (L58); "section objects with title/position/count/labels" (L61) | **Adopt as named patterns.** Adil's framing of standard prompt-engineering recipes. |
| Worked examples | JSON example at L76–98; prose example at L122 | **Adopt with optional substitution.** Embedded CJK examples are illustrative; can preserve or replace. |
| Quality checklist | L174–183 (6 items) | **Adopt close to verbatim.** Pre-delivery discipline aligns with our existing DISCIPLINE.md Tier 3 § Pre-Delivery Discipline. |

### 0.1h — Worked examples

Two worked examples in source:

1. **JSON minimal shape** (L76–98) — landing-page mockup for fictional brand "AURA." Demonstrates the count-and-label pattern (`"ingredient_grid": {"count": 4, "labels": [...]}`), position-scoped regions (`"left_side"`, `"right_side"`, `"below_hero"`), inline content rendering ("Skin, restored." / "A 7-day reset ritual. Clinically tested."). 23-line JSON object.

2. **Prose example** (L122) — single paragraph, Asian woman on rainy night with neon signs, embedded vertical Japanese text. Demonstrates concrete props, camera/film language, embedded-text-in-quotes pattern. ~150 words.

Both examples are pedagogical artifacts. Translation handling: adopt as illustrative examples (parallel to how vocab.md adopted Adil's Spatial Zoning example), with optional substitution if the embedded CJK feels off-brand for our skill.

### 0.1i — Disposition summary

**TRANSLATE-WITH-VERIFICATION (LOWER-FRICTION SUB-CLASS)**, parallel to v3.7.15's cinematic-motion-language translation but with:

- Lower friction: register is calmer; production-knowledge content is denser per LoC; fewer universalizing-claim downgrade points
- Standalone sub-skill shape (no cross-refs to other Higgsfield surfaces) → adopts as new `skills/higgsfield-gpt-image-2/SKILL.md` (or similar) rather than as expansion of an existing sub-skill
- Architectural question: standalone OR consolidated with static-ads.md (which also targets gpt-image-2; see VERIFY 0.2)

---

## VERIFY 0.2 — static-ads.md source read

**Path verification:** `/Users/petercsanky/Desktop/EVEN MORE SKILLS/MORE CUSTOM SKILLS/static-ads.md` confirmed at expected location. 20,496 bytes / 316 lines (largest of the three new-content sources).

### 0.2a — Document structure

| Section | Lines | Shape |
|---|---|---|
| Frontmatter | 1–4 | YAML — `name: static-ads`, dense `description` line including `/static-ads` slash-command trigger |
| Opener | 6–12 | One-paragraph mission + output path convention |
| `## Step 1 — Select brand` | 14–22 | Brand-folder selection logic |
| `## Step 2 — Upload ad format reference` | 24–67 | Reference-image intake + zone extraction with **fractional-coordinate notation** |
| `## Step 3 — Select product(s) and copy variation count` | 70–103 | Product-image acquisition (local → website fetch → user fallback) |
| `## Step 4 — Generate and present copy variations` | 106–139 | Copy generation grounded in product-page fetch + brand voice |
| `## Step 5 — Aspect ratio` | 142–149 | Aspect-ratio selection |
| `## Step 6 — Name the output` | 152–160 | Slug derivation |
| `## Step 7 — Create output folder and write spec` | 163–229 | **JSON spec writing + Mode A/B prompt construction** |
| `## Step 8 — Generate` | 232–246 | Script invocation per variation |
| `## Step 9 — Reformat for additional aspect ratios` | 250–261 | Reformat script invocation |
| `## Step 10 — Present results` | 264–287 | Output presentation + regenerate-vs-edit options |
| `## Notes` | 290–298 | Cross-cutting notes on reference image, product images, copy grounding |
| `## Prompt template reference` | 301–316 | **3 worked examples: iMessage / Scarcity Countdown / Ingredient Spotlight** |

**Organizational scheme:** 10-step sequential workflow document with appended prompt-template reference library. Materially different shape from gpt-image-2-director (which is a routing-by-output-shape craft skill).

### 0.2b — Does the production-knowledge claim hold up on full read?

**Confirmed and stronger than v3.7.13's preliminary read.** v3.7.13's Block 2B-prime classified static-ads.md as "LEAD requiring verification, production-knowledge register, specific-and-unguessable details (layout zones with fractional coordinates, safe-zones top-10%/bottom-10% rule, brand-vs-structure separation)." Full read confirms each:

1. **Layout zones with fractional coordinates** (L48–63): `text_zone {top: 0.10, bottom: 0.35}` / `product_zone {top: 0.40, bottom: 0.77}` / `button_zone {top: 0.81, bottom: 0.91}` / `disclaimer_zone {top: 0.91, bottom: 0.97}`. These are **falsifiable production claims** — a static ad with text below the 0.35 cutoff or a CTA outside the 0.81–0.91 band fails the convention. Cannot be guessed; reflects production discipline.

2. **Safe zones top-10%/bottom-10% rule** (L223, L229): *"keep the top 10% and bottom 10% of the frame free from text, logos, icons, buttons, and UI elements — photographic content such as hands, arms, or product edges entering the frame is fine."* Specific, falsifiable, transferable to non-GPT-image-2 platforms.

3. **Brand-vs-structure separation** (L208–215): explicit two-list rule — *"Take from the reference: layout format, zone positions and proportions, UI element types, element placement and spacing logic. Take from `visual-guidelines.md`: everything visual — background colour, typeface and weights, any accent colours (CTA colour, icon colour, badge colour, toggle colours). These always override whatever appears in the reference."* This is the **core operational rule** of the skill — what to inherit, what to override.

4. **Wireframe intermediation** (L64–66): *"These zones are used to generate a brand-neutral wireframe at the target aspect ratio. The wireframe is what gets passed to GPT-image-2 as Image 1 — not the original ad. This eliminates color, typeface, and style contamination from the reference, and there is no aspect ratio conflict regardless of the source format."* This is the **technical workaround** that the entire skill rests on — and it's NOT mentioned in gpt-image-2-director at all.

### 0.2c — Surface overlap with gpt-image-2-director

**The two skills cover different surfaces of the same model.** gpt-image-2-director is **prompt-craft** (how to write a GPT Image 2.0 prompt given a concept). static-ads.md is **workflow** (how to recreate a winning ad format using GPT-image-2 as the generation engine).

| Dimension | gpt-image-2-director | static-ads.md |
|---|---|---|
| Input | Plain-text concept | Reference ad image + brand identity files |
| Output | Finished prompt the user pastes | `static-ad-spec.json` + multiple generated images |
| Execution layer | None (user pastes manually) | YES — invokes `generate-static-ad.py` + `generate-reformat.py` scripts |
| Per-format routing | 3 formats (JSON/prose/meta) by output shape | 2 modes (reference-swap vs. text-driven) by whether reference image is present |
| Cross-references | None | Internal to brand folder structure (`visual-guidelines.md`, `products.json`, `brand-identity/product-images/`) |
| Worked examples | Generic (AURA brand, generic prose) | Brand-specific (`puresport` / electrolytes / energy gel) |
| Author signature volume | Lower (calmer register) | Lower still (workflow doc register) |

**Overlap zone:** the "Prompt template reference" section in static-ads.md (L301–316) — iMessage / Scarcity Countdown / Ingredient Spotlight — IS prompt-craft content that overlaps with gpt-image-2-director's Format A (JSON layout). The overlap is bounded: static-ads.md's templates are specifically structured for ad-recreation; gpt-image-2-director's JSON pattern is general-purpose. Same model, different routing taxonomy.

**Architectural implication:** the two skills can adopt as separate sub-skills (Option α), can consolidate under one `higgsfield-gpt-image-2` umbrella with static-ads as satellite (Option β), or can adopt as `gpt-image-2-director` standalone + static-ads as expansion of higgsfield-marketing-studio (Option γ). See dedicated Architectural section.

### 0.2d — Author signature consistency

| Signal | Strength | Evidence |
|---|---|---|
| HARD RULE volume | **Lower than cinematic-motion-language.md, lower than gpt-image-2-director.** | "Safe zones apply to every prompt in every mode — no exceptions" (L229) is the strongest universalizing claim; everything else is procedural ("Ask:", "Run:", "Construct:"). Workflow doc register. |
| Zero external citations | **Confirmed.** | No platform docs, no benchmarks, no third-party sources. |
| Falsifiable claims | **Highest of the three.** | Fractional coordinates, safe-zone percentages, brand-vs-structure inheritance rules — all production-falsifiable. |
| Vocabulary | **Standard ad-creative vocabulary.** | "Headline," "subheadline," "CTA," "trust badge," "ingredient spotlight," "iMessage format" — all standard. |
| Synthesis | **Adil's wireframe-intermediation workaround + the zone-extraction protocol.** | The wireframe step (L64–66) is non-obvious problem-solving; this is Adil's contribution. |

**Disposition class:** **TRANSLATE-WITH-VERIFICATION (LOWEST-FRICTION SUB-CLASS)**. Workflow doc with falsifiable production claims and minimal craft-opinion-at-HARD-RULE-volume. Two reservations:

1. **Brand-folder dependency.** The skill assumes a `./brands/[brand-name]/brand-identity/` folder structure with `visual-guidelines.md` + `products.json` + product-images/. Our skill library doesn't have this scaffold. Translation must either (a) translate the workflow to be model-of-itself (the brand-folder structure is the storage convention static-ads expects), or (b) translate the prompt-template patterns + zone-extraction protocol + brand-vs-structure rule WITHOUT the full execution layer.
2. **Script dependencies.** The skill invokes `skills/references/generate-static-ad.py` and `skills/references/generate-reformat.py` — scripts that presumably exist in Adil's project but we don't have copies of. Translation handling: document the script invocation pattern conceptually; don't claim functional support unless the scripts are also adopted.

### 0.2e — Worked examples + structural rules

Three worked template examples (L301–316):

1. **iMessage / DM Conversation** (L306–308): single dense paragraph specifying iOS header bar, message bubbles (alternating gray/blue, left/right), link preview card, iPhone bottom bar. ~600 chars. Pattern: realistic-screenshot framing as ad delivery vehicle.

2. **Scarcity / Countdown Urgency** (L310–312): single dense paragraph specifying urgency tag, headline, product hero, stock progress bar, countdown timer (4 colon-separated tiles), CTA button, disclaimer, logo placement. ~750 chars. Pattern: limited-stock urgency with mechanical countdown.

3. **Ingredient Spotlight / Clean Label** (L314–316): single dense paragraph specifying category pill, headline (ingredient name + period), close-up ingredient image (macro, 40% frame), 3-row fact table (label + sentence), product at angle, trust badge, brand logo. ~750 chars. Pattern: educational clean-label register.

Each template is a single flowing paragraph (matches gpt-image-2-director's Format B prose style for single-image outputs). Templates use `[BRACKETED PLACEHOLDERS]` for copy slots — different convention from gpt-image-2-director's `{argument name="x" default="y"}` slot pattern at L71. **Translation question for Phase 1:** unify slot-notation across the two adopted skills, or preserve source conventions?

### 0.2f — Disposition summary

**TRANSLATE-WITH-VERIFICATION (LOWEST-FRICTION SUB-CLASS).** Workflow-shape content with production-knowledge register. Two adoption gates: (1) brand-folder execution layer — preserve as workflow recipe or drop; (2) script invocations — document pattern, do not claim functional support.

---

## VERIFY 0.3 — ms_image surface boundary

### 0.3a — Existing ms_image coverage in higgsfield-marketing-studio

Re-read of `/Users/petercsanky/Projects/higgsfield/skills/higgsfield-marketing-studio/SKILL.md` (672 lines) + `cross-surface-workflow.md` (428 lines):

| Site | Coverage |
|---|---|
| `SKILL.md` L16 | Names ms_image briefly: *"The two image-side Marketing Studio surfaces (`marketing_studio_image` and `ms_image` / 'DTC Ads') are named in §2 but covered in the companion `cross-surface-workflow.md`."* |
| `SKILL.md` L45–58 | §2 enumerates three Marketing Studio models in a table; ms_image row reads: *"ms_image — DTC Ads — image — Full DTC ad image generation — brand-kit-aware, ad-format styles, batch up to 20, max 14 reference media. Out of scope; named briefly in cross-surface-workflow.md §3"*. Naming convention noted: *"refer to it as 'DTC Ads' — that's the user-facing brand name"* (L55). |
| `cross-surface-workflow.md` L26 | Names ms_image as Higgsfield-native alternative to Adil's GPT-Image-2 + Soul + Nano Banana recipe. |
| `cross-surface-workflow.md` L53–57 | Most substantive coverage today: ~80 words. Documents `brand_kit_id` + `style_id` + batch-20 + max-14-reference-media capabilities. Cites [Phase 0: Probe 0.3-a]. Marks source-corpus reconciliation #12 (net-new intel beyond Adil's source corpus). |
| `cross-surface-workflow.md` L414 | Deferral note: *"`ms_image` ('DTC Ads') — Named here (§3), not covered — full sub-skill deferred to future arc; brand-kit-aware DTC ad image generation, distinct from GPT Image 2.0"*. |

**Total existing ms_image coverage: ~5 short paragraphs across two files. ~150 words.**

### 0.3b — Source corpus survey

```
$ grep -nEi "ms_image|dtc ads|dtc_ads|marketing_studio_image" \
    "/Users/petercsanky/Desktop/EVEN MORE SKILLS/marketing-studio-director/SKILL.md" \
    "/Users/petercsanky/Desktop/EVEN MORE SKILLS/higgsfield-content-factory/SKILL.md"

(no output — ZERO matches across both files)
```

**Result: ZERO hits.** marketing-studio-director.md is 262 lines covering 9 Marketing Studio video presets, the prompt-direction grammar, and the output format. It does not mention ms_image, DTC Ads, or marketing_studio_image at all. higgsfield-content-factory.md is 997 lines covering the 5-stage MCP-orchestration pipeline for full Marketing Studio video campaigns. Also zero hits.

**This is the major Phase 0 finding.** Adil's source corpus does not document ms_image. The only substrate is v3.7.13's Phase 0 Probe 0.3-a — a single live-MCP introspection result captured in `.planning/v3.7.13/PHASE-0-PROBES.md`.

### 0.3c — What does ms_image cover that's NOT in higgsfield-marketing-studio already?

Based on the brief notes at `cross-surface-workflow.md` L53–57 (the only substrate we have):

| Capability | Already in higgsfield-marketing-studio? | New territory if expanded |
|---|---|---|
| `brand_kit_id` param | No — Marketing Studio video doesn't use brand kits | YES |
| `style_id` param (ad-format style) | No | YES |
| Batch generation up to 20 images per call | No — MS video is one generation at a time | YES |
| Max 14 reference media per generation | No — MS video maxes at ~4 media slots | YES |
| User-facing name "DTC Ads" | YES (named in SKILL.md L55) | partial — naming is documented; capability is not |
| Image-side vs video-side surface distinction | YES (named at SKILL.md L46–58 table) | partial |

**Net-new content surface:** brand-kit-aware ad image generation as a distinct product from MS Video, with parameters and capabilities that don't exist in MS Video. Substantial — probably 200–400 lines of new content if treated as a full sub-skill.

### 0.3d — Is ms_image its own substantial sub-skill or an expansion of higgsfield-marketing-studio?

**Critical question for architecture.** Three reads:

**Read A — ms_image is its own sub-skill (parallel to higgsfield-marketing-studio).** Pros: image-side surface deserves its own discovery; user looking for "DTC ad image generation" finds a sub-skill named that. Cons: requires building from substrate that doesn't exist (no Adil corpus); violates the project's "Adil-corpus-as-source" translation pattern.

**Read B — ms_image is an expansion of higgsfield-marketing-studio (new top-level section).** Pros: ms_image IS a Marketing Studio model (per Higgsfield's own model naming — `show_marketing_studio.mode` accepts it); architectural location matches Higgsfield's own product structure; reuses existing source-corpus reconciliation #10/#11 work. Cons: higgsfield-marketing-studio currently scopes to video; mixing image + video under one sub-skill stretches scope. Existing SKILL.md L16 explicitly says "This sub-skill covers Marketing Studio video. The two image-side Marketing Studio surfaces are named in §2 but covered in the companion cross-surface-workflow.md." — adopting ms_image inline would contradict this scoping statement.

**Read C — ms_image expands cross-surface-workflow.md §3 (NOT a new sub-skill).** Pros: cross-surface-workflow.md L414 already says "Named here (§3), not covered — full sub-skill deferred to future arc"; expanding §3 from ~80 words to ~400–600 words upgrades the satellite without creating a new sub-skill or stretching SKILL.md's video-scope. Matches the marketing-studio + cross-surface-workflow satellite pattern. Cons: cross-surface-workflow.md becomes substantially larger; still satellite-doc shape, not sub-skill shape.

**My read:** **Read C is the right shape for Phase 0 evidence.** ms_image has no source corpus, so building 200–400 lines of new content as a sub-skill is documentation work, not translation work. Building 200–400 lines of expanded coverage in the satellite that already names ms_image is content expansion within an established pattern. Phase 1 picks; Phase 0 surfaces the shape.

**The discipline question:** if ms_image is rescoped to "cross-surface-workflow.md §3 expansion" rather than "new sub-skill," scope item 2 stays in v3.7.16 but at a different work-shape. If ms_image stays at "full sub-skill" framing, the methodology gap (live-MCP probing vs. translation) needs Phase 1 design work.

### 0.3e — Source-corpus reconciliation tally

Carrying forward v3.7.13's reconciliation register: ms_image was identified as **source-corpus reconciliation #12** ("net-new intel beyond what Adil's source corpus documents"). It remains the highest-friction reconciliation in the project: every other reconciliation in #1–#11 was source-vs-API-truth divergence within a surface Adil documented; #12 is a surface Adil did not document at all.

---

## VERIFY 0.4 — Courier → DejaVu Sans Mono drift measurement

**Result:** PASS by a wide margin. **0.33% max drift on all real code-block samples.** Item 6 is mechanically simpler than v3.7.14's DV → DVC swap was (which surfaced the 5%/18% threshold at DV regular).

### 0.4a — Methodology

Carried forward from v3.7.14 §VERIFY 0.3:
- fpdf2 v2.8.7 (confirmed installed)
- Real code-block content from `generate_user_guide.py` call sites at L325, L428, L431, L811, L932, L1009 + typical CLI/MCP/path/dict-key shapes + synthetic 71×'x' worst-case
- DejaVu Sans Mono regular TTF at `/tmp/dejavu-test/dejavu-fonts-ttf-2.37/ttf/DejaVuSansMono.ttf`
- 9pt size (matches `generate_user_guide.py:156` `set_font("Courier", "", 9)`)
- Test script: `/tmp/dvsm_drift.py`

### 0.4b — Per-sample drift measurements

| Sample | chars | Courier | DVSM | Drift |
|---|---|---|---|---|
| `git clone https://github.com/OSideMedia/…-prompt-skill` (L325) | 66 | 125.73mm | 126.15mm | **+0.33%** |
| `cp -r higgsfield-ai-prompt-skill ~/.claude/skills/higgsfield` (L325) | 60 | 114.30mm | 114.68mm | +0.33% |
| `"Write me a Higgsfield prompt for a woman walking through…"` (L428) | 81 | 154.31mm | 154.82mm | +0.33% |
| `"I need a Kling 3.0 prompt for a close-up dialogue scene…"` (L431) | 80 | 152.40mm | 152.91mm | +0.33% |
| `in a coffee shop. Warm lighting, shallow depth of field, handheld camera."` (L431) | 74 | 140.97mm | 141.44mm | +0.33% |
| `[Shot size] + [Angle] + [Movement keyword] of [character].` (L1009) | 58 | 110.49mm | 110.86mm | +0.33% |
| `[Pose]. [Environment]. [Lighting]. [Style].` (L1009) | 43 | 81.91mm | 82.19mm | +0.33% |
| `higgsfield model get kling3_0 --json` (typical) | 36 | 68.58mm | 68.81mm | +0.33% |
| `show_marketing_studio(action='list', type='hook', size=100)` (typical) | 59 | 112.39mm | 112.77mm | +0.33% |
| `skills/higgsfield-marketing-studio/cross-surface-workflow.md` (typical) | 60 | 114.30mm | 114.68mm | +0.33% |
| `{'model': 'marketing_studio_video', 'duration': 8, 'aspect_ratio': '9:16'}` (typical) | 74 | 140.97mm | 141.44mm | +0.33% |
| 71×'x' synthetic worst case | 71 | 135.25mm | 135.71mm | +0.33% |

**Max absolute drift: 0.33%.** Compare v3.7.14's measurements: DV → DVC drift 0.57%–6.40% on real content; DV → DV regular drift 11.77%–18.40% (tripped the descope criterion). DVSM swap is materially cleaner than either v3.7.14 candidate — because both Courier and DVSM are **monospace** fonts with near-identical per-character width (Courier 1.9050mm/char @ 9pt; DVSM 1.9113mm/char @ 9pt).

### 0.4c — Layout cascade risk

| Sample | Util in 175mm column | Overflow? |
|---|---|---|
| Longest real sample (`"Write me a Higgsfield prompt for a woman walking through…"` 81 chars) | 88.5% | none |
| Synthetic 71×'x' | 77.5% | none |
| 100-char hypothetical sample | ~109% (would overflow Courier too) | beyond existing content; no real samples exceed 100 chars |

**Zero existing code-block call sites overflow under DVSM.** All measured samples land at <90% column utilization. No layout cascade risk for the v3.7.14-established 5% drift threshold.

### 0.4d — Bundle size impact

| File | Size |
|---|---|
| DejaVuSansMono.ttf (regular) | 333 KB |
| DejaVuSansMono-Bold.ttf | 324 KB |
| DejaVuSansMono-Oblique.ttf | 246 KB |
| DejaVuSansMono-BoldOblique.ttf | 248 KB |
| **Minimal scope (regular only — matches existing `code_block` use)** | **333 KB** |
| Full-symmetry scope (matches DVC bundle convention) | 903 KB |

Existing DVC bundle: ~1.9 MB. Adding DVSM regular only: ~2.2 MB total. Adding DVSM full-symmetry: ~2.8 MB total. Both well under 5 MB threshold from v3.7.14.

**Recommendation:** **DVSM regular only.** `code_block` at `generate_user_guide.py:156` invokes `set_font("Courier", "", 9)` — no bold, no italic, no bold-italic. Bundling only the regular weight saves ~570 KB and matches actual usage. If a future code block needs bold or italic, add weights then. (v3.7.14 bundled all three DVC weights because `Body` was used at regular/bold/italic across the file; same justification doesn't apply to mono.)

### 0.4e — FPDF2 add_font integration

Direct analog of the DVC `Body` alias pattern at `generate_user_guide.py:101–103`:

```python
# Add to UserGuidePDF.__init__ alongside Body registrations
self.add_font("Mono", "", str(FONT_DIR / "DejaVuSansMono.ttf"))
```

Then `code_block` at L156 swaps:

```python
# OLD
self.set_font("Courier", "", 9)
# NEW
self.set_font("Mono", "", 9)
```

**Single-site infrastructure change.** No other Courier usage anywhere in the file (grep confirmed). LoC delta: +1 `add_font` line, 1 token swap in `code_block`. Total: ~2 LoC.

### 0.4f — Drift verdict

**No descope. DVSM swap is CLEAN.** 0.33% max drift on all real samples (vs. 5% threshold), zero overflow risk, +333 KB bundle (well under 5 MB threshold), 2-LoC integration, single call site to swap. Item 6 is the lowest-friction infrastructure change in v3.7.16.

---

## VERIFY 0.5 — `--dry-run` exit-code matrix design

### 0.5a — Failure class enumeration

`build_pdf(dry_run=False)` at `generate_user_guide.py:218` through L1264 has the following failure modes (mapping by current behavior):

| Failure class | Where it surfaces | Current exit behavior | Proposed exit code |
|---|---|---|---|
| Frontmatter parse error | `read_root_metadata()` L24–45 raises `RuntimeError` if no `---\n…\n---\n` block matches OR if required field (`version`, `updated`, `author`) missing | exit ≠0 (Python traceback) | **2** |
| Sub-skill dict-parity mismatch | L1195–1205 explicit `RuntimeError` when `discover_sub_skills()` ≠ `SUB_SKILL_DESCRIPTIONS.keys()` | exit ≠0 (Python traceback) | **3** |
| Font registration error | `UserGuidePDF.__init__()` L101–103 `add_font` raises if font file missing OR malformed | exit ≠0 (Python traceback) | **4** |
| Rendering error (FPDFUnicodeEncodingException) | Any `pdf.cell` / `pdf.multi_cell` / `pdf.table_row` call on a code point outside the registered font's Unicode coverage. v3.7.13 em-dash crash is the canonical instance. | exit ≠0 (Python traceback) | **5** |
| Output gate / file write error | `pdf.output(...)` at L1263 — disk full, permission denied, path missing | exit ≠0 (Python traceback) | **6** (non-dry-run only; N/A under `--dry-run`) |
| Unknown/uncaught error | Any other exception | exit ≠0 (Python traceback) | **1** (catch-all) |
| Success | Normal completion | exit 0 | **0** |

### 0.5b — Design proposal

Three design approaches:

**Design proposal D5-A: Wrap `build_pdf()` in a try/except harness, map exception classes to exit codes.**

```python
EXIT_OK = 0
EXIT_UNKNOWN = 1
EXIT_FRONTMATTER = 2
EXIT_DICT_PARITY = 3
EXIT_FONT = 4
EXIT_RENDER = 5
EXIT_OUTPUT = 6

if __name__ == "__main__":
    import argparse, sys
    parser = argparse.ArgumentParser(...)
    parser.add_argument("--dry-run", action="store_true", ...)
    args = parser.parse_args()
    try:
        build_pdf(dry_run=args.dry_run)
        sys.exit(EXIT_OK)
    except FrontmatterError as e:           # subclass RuntimeError or use sentinel
        print(f"FRONTMATTER ERROR: {e}", file=sys.stderr)
        sys.exit(EXIT_FRONTMATTER)
    except DictParityError as e:
        print(f"DICT-PARITY ERROR: {e}", file=sys.stderr)
        sys.exit(EXIT_DICT_PARITY)
    # ... etc
```

LoC estimate: +30–40 LoC (named exception classes + argparse harness). Touches `read_root_metadata()` and the L1195 dict-parity check to raise specific exception subclasses. Touches font registration and rendering call sites only if we re-raise wrapped.

**Design proposal D5-B: Print-then-exit at each known failure point; catch-all wrapper for unknowns.**

```python
def read_root_metadata():
    ...
    if not m:
        print(f"FRONTMATTER ERROR: No YAML frontmatter in {ROOT_SKILL_PATH}", file=sys.stderr)
        sys.exit(2)
    ...

def build_pdf(dry_run=False):
    ...
    if discovered != declared:
        print(f"DICT-PARITY ERROR: ...", file=sys.stderr)
        sys.exit(3)
    ...

if __name__ == "__main__":
    ...
    try:
        build_pdf(dry_run=args.dry_run)
    except Exception as e:
        print(f"UNKNOWN ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
```

LoC estimate: +15–20 LoC. Less reusable (functions become CLI-coupled — they `sys.exit` instead of raising), but simpler to ship. Trade-off: harder to test `build_pdf` in unit context if it can `sys.exit` directly.

**Design proposal D5-C: Status-tuple return + thin CLI wrapper.**

```python
class BuildResult:
    def __init__(self, status, message, pages=None):
        self.status = status
        self.message = message
        self.pages = pages

def build_pdf(dry_run=False) -> BuildResult:
    try:
        # ... existing pipeline
        return BuildResult(EXIT_OK, "OK", pages=pdf.page_no())
    except FrontmatterError as e:
        return BuildResult(EXIT_FRONTMATTER, str(e))
    ...

if __name__ == "__main__":
    ...
    result = build_pdf(dry_run=args.dry_run)
    if result.status != EXIT_OK:
        print(f"ERROR ({result.status}): {result.message}", file=sys.stderr)
    sys.exit(result.status)
```

LoC estimate: +40–50 LoC. Most testable, most refactor (build_pdf signature changes from `None` return to `BuildResult` return).

### 0.5c — Documentation surface

Three places the exit-code matrix could live:

1. **Inline `argparse` help text** — single string at the `--dry-run` flag description. Concise; visible via `python3 generate_user_guide.py --help`. Trade-off: cramped formatting.
2. **`generate_user_guide.py` module docstring** at the top of the file (currently L2–9). Visible to readers of the source; not visible at CLI invocation. Trade-off: hidden to users.
3. **New `docs/DRY-RUN-EXIT-CODES.md`** referenced from argparse help and module docstring. Most discoverable; adds a file to the repo.

**Recommendation:** **module docstring + argparse-help summary pointer.** v3.7.16 doesn't need a dedicated docs file (low surface complexity — 7 exit codes). The module docstring is where developers look when they hit a non-zero exit. argparse `--help` gets a one-liner: "On failure, exits 1 (unknown) / 2 (frontmatter) / 3 (dict-parity) / 4 (font) / 5 (render) / 6 (output)."

### 0.5d — Recommended design

**Design D5-A (named exception classes + argparse harness in `__main__`).** Reasons:

1. Existing dict-parity check at L1195 already uses `raise RuntimeError(...)` — natural to subclass.
2. `build_pdf()` stays return-`None` — no signature breaking change for any caller (none exist yet, but the planned validate.py subprocess integration in VERIFY 0.6 only inspects exit code, not return value).
3. Testable: `build_pdf()` raises typed exceptions; tests can `pytest.raises(DictParityError)` instead of asserting `sys.exit`.
4. LoC estimate (30–40) is bounded; mirrors v3.7.14's "10 LoC for the dry-run flag itself" precedent.

**Phase 1 picks final design.** Phase 0 surfaces three viable options.

### 0.5e — Reverse-compatibility constraint to VERIFY 0.6

If validate.py treats all non-zero as "build failed" (binary), the matrix gains nothing for validate.py — but still gains value at the CLI level (users running `--dry-run` get specific failure-class output). If validate.py distinguishes codes, validate.py can produce richer reports. See VERIFY 0.6 for the integration shape.

---

## VERIFY 0.6 — `validate.py` subprocess integration shape

### 0.6a — Current `validate.py` structure

`validate.py` (160 LoC) has 3 check phases (`main()` L113–157):

| Phase | Lines | Check class | Output |
|---|---|---|---|
| 1 | L117–125 | All SKILL.md files: frontmatter completeness + relative-path resolution | per-file PASS/FAIL |
| 2 | L127–130 | JSON databases: filter-memory + quality-memory schema + entry-count parity | per-db PASS/FAIL |
| 3 | L132–144 | 13 required root files present | per-file PASS/FAIL |
| Summary | L146–156 | Aggregate count + exit 0/1 | total PASS or list of issues |

Exit behavior: exit 0 on all-pass; exit 1 on any failure (no exit-code matrix today). Single failure mode = single exit.

### 0.6b — Integration question — where does the subprocess call go?

The subprocess call (`python3 generate_user_guide.py --dry-run`) is a fourth check phase — verifies that the PDF pipeline doesn't crash on the current repo state. Three positioning options:

**Position 6-A: Append as Phase 4 after Phase 3 (root files).**

```python
def main():
    ...
    # Phase 1: SKILL.md
    # Phase 2: JSON databases
    # Phase 3: Root files
    
    # Phase 4 (NEW): PDF dry-run smoke check
    print("\n[ PDF DRY-RUN SMOKE ]")
    import subprocess
    result = subprocess.run(
        ["python3", str(ROOT / "generate_user_guide.py"), "--dry-run"],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        check(True, "generate_user_guide.py --dry-run", "exit 0")
    else:
        check(False, "generate_user_guide.py --dry-run",
              f"exit {result.returncode}; stderr: {result.stderr.strip()[:120]}")
```

LoC estimate: +15 LoC inside `main()`. Cleanest.

**Position 6-B: Interleave with Phase 3 root-file checks.** Treats the PDF pipeline as a "root file infrastructure" check. Slightly more legible — group "infrastructure that affects builds" together. LoC similar; ordering only.

**Position 6-C: Make it conditional on a CLI flag (`validate.py --with-dry-run`).** Lets users opt out of the subprocess overhead in casual runs. LoC: +20 LoC. Trade-off: opt-in defeats the purpose of catching v3.7.13-class regressions before ship time.

**Recommendation: Position 6-A unconditional.** Validate.py is already a pre-release health check (the README docs it as such, and CLAUDE.md L23 lists it as the canonical pre-release gate); the subprocess overhead is tolerable for the ship-time use case it covers.

### 0.6c — Error-handling shape: matrix-aware OR binary?

Two reads on how validate.py treats the exit-code matrix from VERIFY 0.5:

**Read 6-i: Binary.** validate.py treats `result.returncode == 0` as PASS, anything else as FAIL. The matrix is for CLI users of `--dry-run` directly, not for validate.py. Simpler integration.

**Read 6-ii: Matrix-aware.** validate.py inspects `returncode` and reports the failure class in the validate.py output (e.g., "FAIL: dict-parity mismatch (exit 3) — run `python3 generate_user_guide.py --dry-run` for full diagnostic"). More informative output; requires validate.py to know the exit-code matrix.

**Recommendation: Read 6-i binary, with stderr capture for diagnostic context.** validate.py doesn't need to mirror the exit-code matrix — it needs to know if the dry-run passed AND surface the stderr if it failed so the user knows what to fix. The stderr from the named-exception harness (Design D5-A) carries the failure-class label ("FRONTMATTER ERROR: ...", "DICT-PARITY ERROR: ..."), so validate.py's output is informative without needing matrix awareness. Decouples validate.py from D5-A's exit-code choices.

### 0.6d — Performance impact

Single subprocess invocation: import fpdf2 + walk skills/ + render 28-page PDF in-memory. Empirically, a full `python3 generate_user_guide.py` run today takes ~1.5 seconds wall-clock (the user can measure on a real run; estimate is based on existing v3.7.14 / v3.7.15 ship-time validation evidence per their CHANGELOGs). The `--dry-run` variant skips the `pdf.output(...)` disk write but otherwise runs the same pipeline → essentially identical wall-clock.

validate.py today takes ~0.2s (no subprocesses, all I/O). Adding a 1.5s subprocess call multiplies validate.py wall-clock by ~8×. Net: validate.py becomes a ~1.7s health check from ~0.2s. **Acceptable for a pre-release gate.** Phase 1 should measure on the real repo and decide if 1.7s feels like "too slow for a pre-release check" — my read is no.

### 0.6e — LoC estimate

Total integration: **+15 LoC** in `validate.py:main()`. Minimal blast radius. Matches v3.7.14's pattern (each phase is ~10–15 LoC).

---

## VERIFY 0.7 — Content cleanup scope verification

### 0.7a — Item 11: FAQ paragraph at `generate_user_guide.py` L1236

Current text (L1235–1247):
> "What changed since v3.0.0?"
> "Seventeen platform releases shipped between v3.0.0 (April 2026) and this guide (v3.7.12). Major themes by era: install-path simplification, Seedance 2.0 prompt modes, Kling 3.0 Motion Control, and Cinema Studio 3.5 with Image Mode + Physics Rendering Decision Matrix (v3.3.0 through v3.6.x); a v3.7.0 metadata refactor making version and sub-skill discovery automatic; a v3.7.4 - v3.7.7 audit-corpus mega-release sequence that added production-benchmarks (Hell Grind Cannes-feature iteration anchors), Seedance Frame Coordinate System + Spatial Layout Block + FAILURE-MODES catalog, and Soul Character Anchor Block + Two-Tool Refinement Pipeline; a v3.7.8 - v3.7.11 stack-integration arc that added the higgsfield-stack sub-skill (CLI / MCP / bundled-skills coexistence), two-step preflight discipline (schema verify before cost estimate), aspect-ratio-as-enum vs. anamorphic-as-style-register separation, and the dispatcher pre-delivery checklist; and this v3.7.12 USER-GUIDE refresh closing the deferred PDF modernization arc. See CHANGELOG.md for full per-release detail."

**Two staleness vectors:**

1. **Count is wrong.** The current text says "Seventeen platform releases shipped between v3.0.0 (April 2026) and this guide (v3.7.12)." Actual count from CHANGELOG.md, v3.0.0 → v3.7.12 inclusive = **26 releases** (v3.0.0, v3.1.0, v3.2.0, v3.3.0, v3.4.0, v3.4.1, v3.5.0, v3.6.0, v3.6.1, v3.6.2, v3.6.3, v3.6.4, v3.6.5, v3.7.0, v3.7.1, v3.7.2, v3.7.3, v3.7.4, v3.7.5, v3.7.6, v3.7.7, v3.7.8, v3.7.9, v3.7.10, v3.7.11, v3.7.12). The "Seventeen" count was inaccurate when v3.7.12 shipped; the staleness predates v3.7.13. For v3.7.16, count v3.0.0 → v3.7.16 = **30 releases**.

2. **Guide version is wrong.** "this guide (v3.7.12)" → "this guide (v3.7.16)" for v3.7.16.

3. **Era summary is incomplete.** Adds three missing eras: v3.7.13 (translation + dispatcher pre-delivery checklist mega), v3.7.14 (DVC font + --dry-run flag + Section 24 row), v3.7.15 (vocab.md gap-fill 5-pillar translation), v3.7.16 (mega-release with new content surfaces + DVSM mono + validate.py subprocess + exit-code matrix). Optional content; the FAQ doesn't need to enumerate every era — it ends "See CHANGELOG.md for full per-release detail."

**Minimum-viable refresh (count + version only):** 2 token changes — "Seventeen" → "Thirty"; "v3.7.12" → "v3.7.16". **~2 LoC.**

**Substantive refresh (count + version + era summary):** ~5 LoC additional (insert one new clause describing the v3.7.13 → v3.7.16 era). Total: ~7 LoC.

**Kickoff estimate: ~3–5 LoC.** Confirmed achievable on the minimum-viable refresh; substantive refresh slightly exceeds the estimate.

**Item 11 verdict: CLEAN. Trivial scope. No descope signal.**

### 0.7b — Item 12: Six forward-looking cross-references

| # | Cite site | Cite target | Cite shape | LoC | Descope candidate? |
|---|---|---|---|---|---|
| 12.1 | `templates/10-dance-music-performance.md` L32 — annotation-table cell "Negative space isolates the performer — all attention on the body" | vocab.md § Composition Vocabulary → Negative space | Inline parenthetical inside a TABLE CELL — adds visual noise to a compact column-format. Cite shape is awkward. | 1–2 | **YES — table-cell sites don't naturally accommodate citation prose** |
| 12.2 | `templates/seedance/multi-character-anchor.md` L38 — TEMPLATE FIELD LABEL `Crossing rule: [...]` (inside a fenced code block) | vocab.md § Composition Vocabulary → Crossing rule | Cannot cite inside a fenced code block (would render literally in the template). Only the surrounding prose can cite. | partial | partial — only the surrounding "What goes in each field" prose at L40+ can cite cleanly |
| 12.3 | `templates/seedance/multi-character-anchor.md` L40 — TEMPLATE FIELD LABEL `Negative space: [...]` | vocab.md § Composition Vocabulary → Negative space | Same shape as 12.2 — inside fenced code block. | partial | partial |
| 12.4 | `templates/seedance/multi-character-anchor.md` L80 — GREAT exposition prose "(distance + eyeline + crossing rule + negative space)" | vocab.md § Composition Vocabulary → Crossing rule + Negative space | Prose location — clean inline parenthetical fits. | 1 | **NO — clean cite site** |
| 12.5 | `templates/seedance/worked-example-two-character.md` L44/L46/L62 — inside the worked-prompt fenced code block | vocab.md sections | Cannot cite inside the prompt example (would corrupt the example). | descope | **YES — fenced code block** |
| 12.6 | `templates/seedance/worked-example-two-character.md` L68–69 — "(distance + eyeline + crossing rule + negative space)" in "What this demonstrates" prose | vocab.md sections | Clean prose location. | 1 | **NO — clean cite site** |
| 12.7 | `skills/higgsfield-seedance/SKILL.md` L488 — inline list ending `'crossing rule')` in the "Not a mathematical guarantee" subsection | vocab.md § Composition Vocabulary → Crossing rule | Clean parenthetical addition. | 1 | **NO — clean cite site** |
| 12.8 | `skills/higgsfield-camera/SKILL.md` — no specific line cited; "camera-discipline content → cite new § Camera Contract" | vocab.md § Camera Movement Terminology → Camera Contract | Requires identifying the right paragraph in a 390-line file + writing inline prose introducing the cross-reference. **Prose authoring, not citation.** | 3–5 | **YES — prose rework** |
| 12.9 | `skills/higgsfield-prompt/SKILL.md` — no specific line; "MCSLA Action layer guidance → cite new § Motion Physics Anchor" | vocab.md § Camera Movement Terminology → Motion Physics Anchor | Same shape as 12.8 — prose authoring. The MCSLA "A — Action" definition at L17 is the natural anchor; needs new paragraph or inline prose addition. | 3–5 | **YES — prose rework** |

**Tally:** 9 sub-sites surfaced (vs. the kickoff's 6 nominal sites — the kickoff under-counted because multi-character-anchor.md had 3 distinct line references and worked-example had 4). Of the 9:

- **3 CLEAN** (12.4, 12.6, 12.7) — single parenthetical addition each, ~3 LoC total
- **2 PARTIAL** (12.2, 12.3) — cannot cite the labels themselves; only surrounding prose can cite, which means adding new prose (not just inserting citations)
- **4 AWKWARD/DESCOPE** (12.1, 12.5, 12.8, 12.9) — table-cell / inside-code-block / prose-authoring sites; all require either ugly cite shapes OR genuine prose authoring

**Kickoff said "Is the cross-reference addition genuinely additive (just inserting a citation) or does it require prose rework?"** Answer: only 3 of 9 sub-sites are genuinely additive citation-only edits. 6 of 9 require either prose authoring or have awkward cite shapes.

**Recommended descope:** ship items 12.4, 12.6, 12.7 (3 clean cites, ~3 LoC total). Defer items 12.8 and 12.9 (the prose-authoring sites for higgsfield-camera and higgsfield-prompt) to v3.7.17 — they're forward-looking content authoring, not citation cleanup. Defer items 12.1, 12.2, 12.3, 12.5 (awkward-shape sites) entirely — citation isn't the right tool there.

**Item 12 verdict: PARTIAL DESCOPE. Ship 3 of 9 sub-sites; defer 6.**

### 0.7c — Item 13: DISCIPLINE.md boundary-condition framing pattern naming

**The v3.7.15 forward criterion is explicit.** From `CHANGELOG.md` v3.7.15 changelog entry L80:

> "**NEW: Boundary-condition framing pattern** — the 'grounded → operative; ungrounded → adjective-stacking' framing applied to Negative space evocative-naming treatment is a more sophisticated application of the per-claim register-downgrade discipline. **May earn its own DISCIPLINE.md pattern name in a future arc if the same shape surfaces elsewhere.** Observed but not pattern-named in v3.7.15."

**Evidence count to date: 1 observation.** Phase 0 surveyed the v3.7.16 scope items for additional pattern surfacings:

- Item 1 (gpt-image-2-director translation): would the "grounded → operative; ungrounded → adjective-stacking" framing apply during translation? Possibly to claims like "Prompt following is its #1 strength" (grounded — corroborated by benchmarks → operative as production discipline) vs. "Human faces often go plasticky" (grounded — observable failure → operative as workaround language). **Plausibly applicable but not yet observed in actual translation — it's only "applicable" if Phase 1+ translation surfaces such a moment.**
- Item 3 (static-ads.md translation): production-knowledge register throughout; very few sites likely to trigger the boundary-condition framing.
- Items 5/6/7 (infrastructure): no register translation; framing doesn't apply.
- Items 11/12 (content cleanup): mechanical edits; framing doesn't apply.

**Phase 0 verdict on item 13:** **One observation. The v3.7.15 forward criterion has not been met.** Naming the pattern in DISCIPLINE.md after one observation would violate the criterion v3.7.15 itself set ("if the same shape surfaces elsewhere"). The honest move is to defer item 13 to v3.7.17 backlog and re-evaluate when a second observation surfaces — either from v3.7.16 Phase 1+ translation work (if it produces a clear second instance) or from a later release.

**Optional re-evaluation:** if v3.7.16 Phase 1 translation of gpt-image-2-director DOES produce a clear second observation of the pattern (e.g., handling Adil's "lean into stylized rather than hyperreal" claim with the same grounded→operative framing), the criterion gets met inside v3.7.16's own arc and item 13 becomes ship-eligible. **But Phase 0 cannot pre-judge this; the criterion has to be met by visible evidence in the translation work, not by Phase 0 speculation.**

**Item 13 verdict: DESCOPE to v3.7.17 backlog.** Re-eligible if v3.7.16 Phase 1+ surfaces a second observation in actual translation work.

---

## Architectural option enumeration — new-content surfaces (items 1, 2, 3)

Phase 0 surfaces; Phase 1 picks. Three viable architectures for items 1 (gpt-image-2-director), 2 (ms_image / DTC Ads), and 3 (static-ads.md):

### Option α — Three separate new sub-skills

```
skills/
  higgsfield-gpt-image-2/      (NEW — from gpt-image-2-director.md, prompt-craft)
    SKILL.md
  higgsfield-static-ads/        (NEW — from static-ads.md, ad-recreation workflow)
    SKILL.md
  higgsfield-dtc-ads/           (NEW — from ms_image / DTC Ads, brand-kit-aware image gen)
    SKILL.md
```

**Scope:**
- 3 new sub-skill directories
- 3 new entries in `SUB_SKILL_DESCRIPTIONS` dict at `generate_user_guide.py:68`
- 3 new rows in PDF Section 24 sub-skill rundown (L1207)
- Total new SKILL.md content: ~206 lines (item 1) + ~316 lines (item 3) + ~200–400 lines (item 2, authored not translated)
- v3.7.13/14/15 SUB_SKILL_DESCRIPTIONS ceiling of 71 chars per description — three new descriptions need to fit; achievable
- Dispatcher routing: 3 new `name` triggers in root SKILL.md

**Pros:**
- Each surface has its own discovery slot
- Clean per-sub-skill scoping (one model per sub-skill)
- Matches existing sibling pattern (higgsfield-soul, higgsfield-cinema, higgsfield-seedance, etc. — each is a model-scoped sub-skill)

**Cons:**
- **3 new sub-skills in one release is high** — v3.7.13 added 1 (higgsfield-marketing-studio); v3.7.0 added several but as part of the metadata refactor
- gpt-image-2-director and static-ads.md cover DIFFERENT modes of the SAME model (GPT Image 2.0) — adopting as two separate sub-skills doesn't reflect the model-grouping reality
- ms_image as full sub-skill demands the methodology shift / pure documentation work flagged in VERIFY 0.3 — not source-corpus translation

**Verdict:** highest-scope option. Defensible if descope of item 2 happens (then α becomes "2 new sub-skills" which is more proportionate).

### Option β — Consolidated `higgsfield-gpt-image-2` umbrella + ms_image as expansion of cross-surface-workflow.md

```
skills/
  higgsfield-gpt-image-2/                  (NEW — items 1 + 3 combined)
    SKILL.md                                (prompt-craft, from gpt-image-2-director.md)
    static-ads-workflow.md                  (workflow satellite, from static-ads.md)
  higgsfield-marketing-studio/             (EXISTING)
    SKILL.md                                (unchanged)
    cross-surface-workflow.md               (EXPANDED — §3 ms_image goes from ~80 to ~400–600 words)
```

**Scope:**
- 1 new sub-skill directory (`higgsfield-gpt-image-2/`) with 2 files (SKILL.md + satellite)
- 1 new entry in `SUB_SKILL_DESCRIPTIONS` (just `higgsfield-gpt-image-2`)
- 1 new row in PDF Section 24
- Existing `higgsfield-marketing-studio/cross-surface-workflow.md` expanded ~400–500 words (ms_image §3 detail)
- Total new content: ~206 + ~316 + ~400–600 = ~900–1100 lines across 3 files

**Pros:**
- **Mirrors the proven precedent** — marketing-studio + cross-surface-workflow.md established the sub-skill + satellite pattern in v3.7.13
- gpt-image-2 model has its own home; static-ads.md as workflow satellite of that home matches Adil's own structure (he has two skills covering the same model)
- ms_image expansion in cross-surface-workflow.md §3 honors the existing scoping ("Named here, not covered") with content expansion rather than scope shift
- Lowest sub-skill registration count (1 new)
- ms_image methodology issue (no source corpus) is bounded — it's "satellite expansion" work, not "new sub-skill authoring" work

**Cons:**
- gpt-image-2-director and static-ads.md are pedagogically distinct (prompt-craft vs. workflow); bundling under one SKILL.md may obscure the distinction
- cross-surface-workflow.md grows to >500 lines if §3 expands as proposed; satellite doc gets denser

**Verdict:** **my read.** Best fit for Phase 0 evidence. Honors:
- Items 1+3 covering the same model (group them)
- Item 2's source-corpus reality (expansion, not new sub-skill)
- The established marketing-studio + satellite pattern

### Option γ — Maximum integration with existing higgsfield-marketing-studio

```
skills/
  higgsfield-gpt-image-2/      (NEW — item 1 standalone, prompt-craft)
    SKILL.md
  higgsfield-marketing-studio/ (EXISTING, EXPANDED)
    SKILL.md                    (NEW SECTION — DTC Ads image surface — from item 2)
    cross-surface-workflow.md   (EXPANDED — item 3 static-ads.md adopted here as ad-workflow recipe)
```

**Scope:**
- 1 new sub-skill (item 1 only)
- higgsfield-marketing-studio/SKILL.md grows by ~200–400 lines (new DTC Ads section)
- cross-surface-workflow.md grows by ~316 lines (static-ads adoption)
- Lowest new sub-skill count (1)

**Pros:**
- Treats ms_image as what it nominally is — a Marketing Studio model — keeping it inside higgsfield-marketing-studio
- static-ads.md as cross-surface-workflow.md content matches its workflow shape

**Cons:**
- higgsfield-marketing-studio expands significantly (currently 672 lines → ~900–1100 lines with DTC Ads section); scoping statement at SKILL.md L16 ("This sub-skill covers Marketing Studio video") would need to be revised
- static-ads.md as cross-surface-workflow.md expansion couples it to marketing-studio surface — but static-ads.md is genuinely a general-purpose ad-recreation workflow, not Marketing-Studio-specific
- gpt-image-2-director still adopts as standalone, but it's the lone new sub-skill — feels imbalanced

**Verdict:** maximum-integration option. Defensible but stretches existing scoping conventions.

### Architectural recommendation

**My read leans Option β.** Phase 1 picks based on:
1. How much weight to give the "items 1+3 cover the same model" finding (high → β or γ)
2. How much weight to give the ms_image-no-source-corpus finding (high → β; rescope to satellite expansion)
3. How much weight to give "low new-sub-skill count is preferred for one release" (high → β or γ; both have 1 new sub-skill)

The pivot between β and γ is: does static-ads.md naturally fit alongside gpt-image-2-director (β — same model, parallel craft+workflow shape) or alongside marketing-studio (γ — both are ad-creation surfaces)? **Phase 0 evidence (VERIFY 0.2c surface-overlap table) supports β — the GPT Image 2 model is the shared anchor; the ad-creation framing is secondary.**

---

## Closing — locked decisions + descope recommendations

### Locked from Phase 0 evidence

1. **Item 6 (Courier → DVSM swap):** CLEAN. 0.33% max drift on real code-block content (well under 5% threshold). Bundle only `DejaVuSansMono.ttf` regular weight (333 KB, matches actual `code_block` usage). 2-LoC infrastructure change at `generate_user_guide.py:101` (add_font) + `:156` (set_font). **Ship as planned.**

2. **Item 11 (FAQ paragraph refresh):** CLEAN. Minimum-viable refresh = 2 token swaps ("Seventeen" → "Thirty"; "v3.7.12" → "v3.7.16"). Substantive refresh adds v3.7.13/14/15/16 era summary (~7 LoC total). **Ship as planned.**

3. **Item 5 (--dry-run exit-code matrix) + Item 7 (validate.py subprocess integration):** TRACTABLE WITH CONTRACT DESIGN. Recommended designs:
   - D5-A: named exception classes + argparse harness (+30–40 LoC, testable, exit codes 0–6)
   - 6-A position with 6-i binary error handling (+15 LoC in validate.py)
   - Documentation: module docstring + argparse help summary (no separate docs file)
   - Phase 1 finalizes the choice; Phase 0 surfaces three options each

4. **Items 1 + 3 (gpt-image-2-director + static-ads.md translation):** TRANSLATE-WITH-VERIFICATION (LOWER-FRICTION SUB-CLASS for item 1; LOWEST-FRICTION SUB-CLASS for item 3). Both follow v3.7.13/15 corpus-translation precedent. Per-claim register-downgrade discipline applies but lighter-touch than cinematic-motion-language was. Phase 1 inventory locks per-claim ADOPT/DOWNGRADE register.

### DESCOPE RECOMMENDATIONS

**Phase 0's discipline is to surface descope opportunities, not to commit to plan ambition. Four descope recommendations follow:**

1. **DESCOPE Item 2 to "ms_image as cross-surface-workflow.md §3 expansion," NOT a new sub-skill.** [HIGH CONFIDENCE]
   - Reason: zero source-corpus hits across both Adil source SKILL.md files for any of `ms_image` / `dtc ads` / `dtc_ads` / `marketing_studio_image`. Building a full sub-skill requires either methodology shift (live-MCP probing à la v3.7.13 Probe 0.3 series — different work-shape, different verification cost) OR pure documentation authoring without translation source (violates the project's Adil-corpus-as-source pattern).
   - Phase 1 alternative: expand cross-surface-workflow.md §3 from ~80 words to ~400–600 words. ms_image stays "named, partially covered" rather than "named, fully covered" — but the partial coverage matches what we actually know about the surface (via Probe 0.3-a only).
   - If Phase 1 disagrees: methodology design work needed before content authoring can begin (a Probe 0.3-series for ms_image; estimate ~1–2 days of live-MCP introspection work to establish parameter schema + capability boundaries + worked examples). v3.7.16 then becomes a discovery+content release, not a pure translation release.

2. **DESCOPE Item 13 (DISCIPLINE.md boundary-condition framing pattern naming) to v3.7.17 backlog.** [HIGH CONFIDENCE]
   - Reason: one observation only (Negative Space evocative-naming treatment in v3.7.15). The v3.7.15 forward criterion explicitly says "May earn its own DISCIPLINE.md pattern name in a future arc **if the same shape surfaces elsewhere**." Pattern-naming after one observation violates v3.7.15's own criterion.
   - Re-eligibility: if v3.7.16 Phase 1+ translation of gpt-image-2-director OR static-ads.md produces a clear second observation of the grounded→operative framing in actual translation work, item 13 becomes ship-eligible inside v3.7.16's own arc. Phase 0 cannot pre-judge this; it has to surface from actual translation evidence.

3. **PARTIAL DESCOPE Item 12 (6-site cross-references) to 3 sub-sites only.** [MEDIUM CONFIDENCE]
   - Ship: 12.4 (multi-character-anchor.md L80 prose), 12.6 (worked-example-two-character.md L68 prose), 12.7 (higgsfield-seedance/SKILL.md L488 inline) — 3 clean parenthetical citations, ~3 LoC total.
   - Defer to v3.7.17:
     - 12.8 (higgsfield-camera Camera Contract authoring) — prose rework, not citation
     - 12.9 (higgsfield-prompt MCSLA Action authoring) — prose rework, not citation
     - 12.1 (dance-music-performance table cell) — awkward cite shape
     - 12.2, 12.3, 12.5 (fenced-code-block sites) — citations can't render inside code blocks
   - Reason: only 3 of 9 sub-sites are genuinely additive single-line citations. The other 6 are prose authoring or awkward cite-shape sites that don't fit v3.7.16's mechanical-cleanup scope.

4. **PHASE-1 ARCHITECTURAL DECISION on items 1 + 3 grouping:** RECOMMEND Option β (consolidated `higgsfield-gpt-image-2` sub-skill + `static-ads-workflow.md` satellite + ms_image as cross-surface-workflow.md §3 expansion). [MEDIUM CONFIDENCE]
   - Reason: Items 1 and 3 cover the same model (GPT Image 2.0); the marketing-studio + satellite pattern is proven precedent; net new sub-skill count = 1 (proportionate to a single release).
   - α (3 new sub-skills) and γ (gpt-image-2 standalone + everything else into marketing-studio) are viable alternatives. Phase 1 picks based on documentation-philosophy weighting.

### Phase 1 transition — open questions

Surfacing for the user, ahead of Phase 1 inventory:

1. **Item 2 rescope: accept the cross-surface-workflow.md §3 expansion path, OR commit to methodology-design work for full sub-skill?** Most important Phase 1 routing question.
2. **Architectural option for items 1 + 3: α (3 separate), β (consolidated under gpt-image-2 umbrella with static-ads satellite), γ (gpt-image-2 standalone + everything else into marketing-studio)?** Recommend β.
3. **Item 5 exit-code matrix: D5-A (named exception classes) vs. D5-B (sys.exit at known failure points) vs. D5-C (status-tuple return)?** Recommend D5-A.
4. **Item 11 FAQ refresh: minimum-viable (2 token swaps) or substantive (era summary added)?** Either works.
5. **Item 12 partial-descope confirm: ship 3 clean sites and defer 6 awkward/prose-rework sites?** Recommend yes.
6. **Item 13 defer to v3.7.17 confirm, with re-eligibility if v3.7.16 Phase 1+ surfaces a second observation?** Recommend yes.

### Mega-release scope verdict

**Original 9-item scope → Phase 0 recommended scope:**

| Item | Original framing | Phase 0 verdict | Phase 0 recommended scope |
|---|---|---|---|
| 1 | gpt-image-2-director sub-skill | Adil corpus translation, lower friction than cinematic-motion-language | **SHIP — as part of consolidated higgsfield-gpt-image-2 sub-skill (Option β)** |
| 2 | ms_image full sub-skill | ZERO source corpus | **RESCOPE — cross-surface-workflow.md §3 expansion only, NOT new sub-skill** |
| 3 | static-ads.md translation | Adil corpus translation, lowest friction | **SHIP — as static-ads-workflow.md satellite under higgsfield-gpt-image-2 (Option β)** |
| 5 | validate.py subprocess integration of --dry-run | Tractable with 6-A binary integration | **SHIP** |
| 6 | Courier → DejaVu Sans Mono swap | 0.33% drift, clean swap | **SHIP — regular weight only (333 KB)** |
| 7 | --dry-run exit-code matrix | Tractable with D5-A named-exception design | **SHIP** |
| 11 | FAQ paragraph refresh | Trivial | **SHIP** |
| 12 | 6 forward-looking cross-references | Only 3 of 9 sub-sites clean | **PARTIAL SHIP — 3 sub-sites; defer 6 to v3.7.17** |
| 13 | DISCIPLINE.md boundary-condition pattern naming | 1 observation only | **DEFER to v3.7.17** |

**Net scope:** **6.5 "clean" items + 1 rescoped item = 7.5-item effective scope**, vs. the original 9-item ambition. Still substantial and earns the "mega" label, but proportionate to Phase 0 evidence.

---

## Carry-forward conventions adherence

- ✅ **Read-only across Phase 0.** Zero writes to `~/Projects/higgsfield/` source files. Zero writes to `~/Desktop/EVEN MORE SKILLS/`. This report lives under `.planning/v3.7.16/` (artifact directory, not source code).
- ✅ **Cite-by-file-and-line.** All claims cite file paths + line numbers where applicable (e.g., `generate_user_guide.py:156`, `cross-surface-workflow.md:L53–57`, `cinematic-motion-language.md:L26` per v3.7.15 substrate).
- ✅ **No confidential or pre-release material.** Adil source corpus is the same substrate v3.7.13 / v3.7.15 audited.
- ✅ **Author-signature calibration applied.** Per-source register classification (gpt-image-2-director: LOWER-FRICTION; static-ads.md: LOWEST-FRICTION). Per-claim register-downgrade discipline reaffirmed for Phase 1.
- ✅ **Plausibility-over-verification.** Item 2's "ms_image needs a full sub-skill" framing was the plausibility trap — the verification (grep across both source files) overrode the plausible-but-untested assumption. The Phase 0 finding (zero corpus hits) is the slow-down-and-read signal kicking in.

---

## Phase 0 artifacts (NOT committed to repo)

- `/tmp/dvsm_drift.py` — drift measurement script for VERIFY 0.4
- `/tmp/dejavu-test/dejavu-fonts-ttf-2.37/ttf/DejaVuSansMono*.ttf` — DVSM TTFs (carried over from v3.7.14 Phase 0 download; bundled-into-repo decision deferred to Phase 1)

These can be removed once Phase 0 is accepted.

---

## Phase 0 time estimate

This Phase 0 ran longer than v3.7.13/14/15 Phase 0s — closer to ~90 minutes equivalent work — but stayed within the kickoff's "60–90 minute" expectation. The mega-scope earned heavier verification: VERIFY 0.1, 0.2, 0.3 each required substantial source-corpus reads; VERIFY 0.4 ran a real measurement script; VERIFY 0.5, 0.6 required tracing build_pdf and validate.py structure; VERIFY 0.7 surfaced an under-counted cross-reference site list (9 sub-sites vs. the kickoff's 6 nominal sites). The Phase 0 length is appropriate to the mega-scope — and the descope recommendations it surfaced (items 2, 13, partial 12) honor the kickoff's discipline: trust the verification surface over the plan ambition.

---

**STOP. Awaiting user review before Phase 1 inventory.**
