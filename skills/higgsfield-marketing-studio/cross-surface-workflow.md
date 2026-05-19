---
name: higgsfield-marketing-studio
description: >
  Cross-surface production workflow reference for higgsfield-marketing-studio. Documents
  Adil's documented four-surface recipe (GPT Image 2.0 → Soul Cinema → Nano Banana Pro →
  Marketing Studio) plus the Higgsfield-native ms_image ("DTC Ads") image-generation
  surface as an alternative upstream. Consulted when the user asks how to build a
  full ad campaign across image and video surfaces, when they need brand-identity
  assets feeding into Marketing Studio video, or when they ask about ms_image / DTC Ads.
user-invocable: false
metadata:
  tags: [higgsfield, marketing-studio, dtc-ads, cross-surface, workflow, ms-image, gpt-image-2, soul-cinema, nano-banana]
  version: 1.0.0
  updated: 2026-05-18
  parent: higgsfield
---

# Marketing Studio — Cross-Surface Production Workflow

---

## 1. What this document is

This document is the connection layer between Marketing Studio and the image-side Higgsfield surfaces that feed it as reference assets. It exists because Marketing Studio doesn't operate alone in practice — Adil's documented production recipe across SRT-1 / SRT-2 / SRT-3 chains four Higgsfield surfaces together to build a full brand campaign, with each stage's output feeding the next as reference media.

This doc documents that recipe AND names the Higgsfield-native `ms_image` ("DTC Ads") surface as an alternative upstream that Adil didn't use in his demos but is available on the platform [Phase 0: Probe 0.3-a].

This is NOT standalone surface documentation. For Soul Cinema depth, see `../higgsfield-soul/SKILL.md`. For Marketing Studio depth, see this directory's `SKILL.md`. For GPT Image 2.0 and Nano Banana Pro depth, those are deferred to future arcs — see §8. This doc just describes how the surfaces fit together.

---

## 2. Adil's documented four-surface recipe

Four stages, each with a Higgsfield surface and a downstream feed:

| # | Stage | Higgsfield surface | What it produces | Feeds into |
|---|---|---|---|---|
| 1 | Brand-identity assets | GPT Image 2.0 in the Higgsfield UI [SRT-3:00:02:12] | Logos, brand kits, posters, billboards | Stage 3 (logos for refinement) + Stage 4 (banners as reference media) |
| 2 | Clothing items + locations | Soul Cinema [SRT-2:00:04:00 onward; SRT-3:00:12:00 onward] | Product mockups (clothing, accessories) AND custom location backdrops | Stage 4 (as reference media in `medias[]`) |
| 3 | Refinements + packaging | Nano Banana Pro [SRT-2:00:04:54, 00:06:00, 00:33:00] | Multi-view product sheets, logo color swaps, packaging design | Stage 4 (packaging in additional-asset slot) |
| 4 | Final video | Marketing Studio — this sub-skill [SRT-2:00:09:00 onward] | 4–15s ad videos in one of 9 presets | (output) |

The four-surface recipe is Adil's choice, not a Higgsfield requirement. The platform also exposes a native `ms_image` ("DTC Ads") surface that consolidates much of Stages 1–3 into a single brand-kit-aware image-generation tool. See §3 for the alternative.

---

## 3. Brand-identity assets stage (image-side surfaces)

Stage 1 of the recipe — brand-identity assets — has two valid paths through Higgsfield.

### 3.a — Path A (Adil's actual recipe)

GPT Image 2.0, Soul Cinema, and Nano Banana Pro used in combination. GPT Image 2.0 for logos and posters; Soul Cinema for clothing mockups; Nano Banana Pro for multi-view item sheets and logo refinements. Demonstrated end-to-end in SRT-2. See §§ 3.1–3.5 below for the verbatim production prompts Adil used.

In v3.7.16, the GPT Image 2.0 layer of Path A acquires its own sub-skill at [skills/higgsfield-gpt-image-2/](../higgsfield-gpt-image-2/SKILL.md) — three-format prompt taxonomy (Format A JSON / Format B prose / Format C meta-prompt) covering UI mockups, single-subject scenes, and theme-only auto-derive prompts. For ad-format recreation specifically (a specialization of GPT Image 2.0 use), see the companion [static-ads-workflow.md satellite](../higgsfield-gpt-image-2/static-ads-workflow.md). Soul Cinema (for items specifically) and Nano Banana Pro remain deferred to future arcs.

### 3.b — Path B (`ms_image` / "DTC Ads")

A dedicated Higgsfield-native image-generation surface for marketing image work, surfaced by [Phase 0: Probe 0.3-a] in v3.7.13 as the third Marketing Studio model alongside `marketing_studio_image` (basic) and `marketing_studio_video` (this sub-skill's primary surface). Adil's source corpus does not document `ms_image` — see § 3.b.v for the source-corpus reconciliation tally.

#### 3.b.i — Capability summary

`ms_image` distinguishes itself from GPT Image 2.0 through four capabilities not present in the general-purpose image model:

- **Brand-kit awareness:** accepts a `brand_kit_id` parameter that ties generation to a per-user brand kit (typography, colour palette, logo placement)
- **Ad-format style routing:** requires a `style_id` parameter selecting from a platform-curated library of ad-format styles
- **Batch generation:** generates up to 20 images per call via `batch_size`, vs. GPT Image 2.0's single-image-per-call default
- **Reference-media capacity:** accepts up to 14 image-role reference media per generation, vs. GPT Image 2.0's smaller reference budget

These capabilities position `ms_image` for the campaign-scale ad image generation use case where brand consistency across many images is the load-bearing constraint.

#### 3.b.ii — Parameter schema

Per [Phase 0: Probe 0.3-a] in v3.7.13 (`models_explore(action='search', query='marketing studio')` introspection):

| Parameter | Required | Type | Default | Options |
|---|---|---|---|---|
| `style_id` | required | string | — | platform-managed style enumeration |
| `brand_kit_id` | optional | string | — | user-specific brand kit |
| `resolution` | optional | string | `1k` | `1k`, `2k`, `4k` |
| `quality` | optional | string | `low` | `low`, `medium`, `high` |
| `batch_size` | optional | number | `1` | `1`–`20` |
| `folder_id` | optional | string | — | organizational metadata |

**Aspect ratios supported (15):** `1:1`, `3:2`, `2:3`, `16:9`, `9:16`, `4:3`, `3:4`, `21:9`, `27:16`, `16:27`, `9:8`, `8:9`, `4:9`, `9:4`, `auto`.

**Reference media:** up to 14 image-role items per generation.

**Pricing:** not separately documented for `ms_image` in Phase 0 evidence. For cost verification, use `transactions(limit=200)` post-hoc as documented in SKILL.md § 12.

#### 3.b.iii — When to recommend `ms_image` over GPT Image 2.0

`ms_image` is not part of Adil's demonstrated canonical recipe — his source corpus doesn't document it (see § 3.b.v). Treat GPT Image 2.0 as the default for image-side work, and reach for `ms_image` when its specific differentiators apply:

- **Brand-kit consistency across many images** — when the user is generating multiple ad creatives that all need consistent typography, colour palette, and logo placement. `ms_image`'s `brand_kit_id` parameter ties the generation to a stable brand kit; GPT Image 2.0 requires re-specifying brand identity in every prompt body.
- **Batch generation of 5–20 ads per call** — `batch_size: 5` through `batch_size: 20` is `ms_image`'s natural surface; GPT Image 2.0's single-image-per-call model doesn't batch.
- **Ad-format style selection from a curated library** — when the user wants to pick from Higgsfield's platform-managed ad-format library rather than describe the format in prose / JSON. `style_id` is the entry point; no GPT Image 2.0 equivalent.

For everything else — UI mockups, infographics, single-image cinematic scenes, theme-only meta-prompts, ad-format recreation from a reference image — GPT Image 2.0 (see [skills/higgsfield-gpt-image-2/](../higgsfield-gpt-image-2/SKILL.md)) is the better fit.

#### 3.b.iv — Naming reminder + live-enumeration discipline

**Naming:** when discussing `ms_image` with the user, refer to it as "DTC Ads." The model ID `ms_image` is internal nomenclature; the user-facing brand name is DTC Ads [from `show_marketing_studio` MCP tool description].

**Live-enumeration discipline:** `style_id` values are platform-managed (the curated ad-format library drifts as Higgsfield adds styles); `brand_kit_id` values are user-specific (each user's brand kits). Hardcoded UUIDs from this doc would mislead — the parameter schema is what's stable; the IDs are not. For canonical current values, call:

```
show_marketing_studio(action='list', type='brand_kit')
# and the equivalent for style enumeration
```

This reuses the v3.7.13 live-enumeration discipline pattern established in [SKILL.md](SKILL.md) § 4 for hooks + settings — same discipline applied wherever IDs drift over time and are not appropriate to hardcode in static documentation.

#### 3.b.v — Source-corpus reconciliation #12

Adil's source corpus — `marketing-studio-director.md` (262 lines, 9 video presets + prompt grammar), `higgsfield-content-factory.md` (997 lines, 5-stage MCP-orchestration pipeline), and the three SRT video demonstrations — does not document `ms_image` at all. Phase 0 search across both source SKILL.md files returned **zero hits** for `ms_image`, `dtc ads`, `dtc_ads`, or `marketing_studio_image`.

The `ms_image` coverage in §§ 3.b.i–3.b.iv is sourced entirely from [Phase 0: Probe 0.3-a] (v3.7.13 live-MCP introspection of the `models_explore` endpoint) plus this doc's prior brief at L51–59. Per v3.7.16 § 1C source-evidence discipline: content stays within the parameter schema + naming rule + capability summary derived from the schema; no worked examples (we have none — no source corpus, no demo evidence), no sample UUIDs (no observed instances), no pricing claims for `ms_image` specifically (no separate pricing signal), no specific ad-format style names (no style enumeration in Probe 0.3-a evidence — `style_id` is required but the enumeration is platform-managed; see § 3.b.iv live-enumeration discipline).

Verification trail: [.planning/v3.7.16/PHASE-0-VERIFICATION.md](../../.planning/v3.7.16/PHASE-0-VERIFICATION.md) § VERIFY 0.3 (ms_image source-corpus survey + architectural option β rationale) and [.planning/v3.7.16/PHASE-1-INVENTORY.md](../../.planning/v3.7.16/PHASE-1-INVENTORY.md) § 1C (source-evidence boundary + DO-NOT-WRITE list).

### Worked examples from PDF items 1–5 (Adil's recipe — Path A)

These are Adil's raw production prompts from the SRT-2 HIGGS clothing brand build. Items 1, 2, 4, 5 used Soul Cinema; item 3 used Nano Banana Pro (for the multi-view shoe sheet).

#### 3.1 — T-Shirt (Soul Cinema)
*Source: PDF item 1.*

```
Flat lay product mockup of an oversized short-sleeve soccer football jersey, ghost
mannequin style, isolated on pure white background #FFFFFF, sharp studio
lighting.

FABRIC & TEXTURE:
- 100% polyester performance mesh — visible fine diamond mesh weave texture
- Athletic synthetic sublimation print fabric, slightly structured

SILHOUETTE:
- Oversized boxy fit, very dropped shoulders
- Short sleeves
- Classic polo-style collar — black fabric, V-neck opening, structured collar flap
- Straight hem, side slits

BASE COLOR: crisp white

PANEL CONSTRUCTION:
- Large black raglan-style panel covering both shoulders completely — wraps from
collar across full shoulder and upper sleeve
- Black curved pointed panel on both sides of lower chest — sharp angular wings
pointing inward toward center
- Black vertical side panels on both sides from underarm to hem
- ONE single white stripe on outer edge of both sleeves (on the black shoulder
panel area) — one stripe only, not three
- Black polo collar

FRONT GRAPHIC — CENTER CHEST:
- Single word "AXIS" only — large elegant italic serif font, bold, black, condensed
- Classic football shirt sponsor typography, approx 8–9cm tall
- Centered on white chest area
- NO second line, NO additional text

BACK: completely clean — white body with black panels, no text no number

Colors: white + black only

Technical: flat lay top-down symmetrical view, ghost mannequin, ultra high
resolution, isolated on #FFFFFF, photorealistic synthetic mesh texture, apparel
product photography
```

What makes this example work: every visible element is enumerated with explicit constraints (panel placement, stripe count "one stripe only, not three," font weight, sponsor typography size in cm). The "NO second line, NO additional text" negative is specific — common when the model has been adding incidental text. Hex code `#FFFFFF` rather than "white" pins the background precisely.

#### 3.2 — Jacket (Soul Cinema)
*Source: PDF item 2.*

```
Two views of a full bomber jacket product shot side by side, front view on the left
and back view on the right, both entirely visible from top to bottom, nothing
cropped or cut off, full garments completely in frame, floating centered on a pure
white background. Clean and minimal design, casual ski-inspired bomber jacket in
bold lime yellow-green (#d1fe17) and deep black colorway, color-blocked panels
with sharp clean edges. Two side zip pockets with subtle stitching. No
drawstrings, no cords anywhere. Oversized slightly large hood with a relaxed
draped silhouette, fully visible, hood completely in frame. Front view: small
brushstroke-style hand-painted text logo reading "VALE" in raw ink calligraphy on
the right chest. Back view: clean solid back panel, no graphics, pure color-blocked
design. Smooth matte technical fabric with slight padding, quilted texture on
panels, casual après-ski streetwear feel. Ghost mannequin style, pure white studio
background, no shadows, no gradients, no clipping, no cropping, both jackets
visible from collar to hem, 8K detail, sharp fabric texture, fashion lookbook
photography, product catalog style, flat lay apparel reference sheet.
```

What makes this example work: the two-view brief is explicit ("front view on the left and back view on the right, both entirely visible"). Hex code `#d1fe17` for the brand lime keeps the color exact across regenerations. Negative constraints ("no shadows, no gradients, no clipping, no cropping") suppress common product-shot artifacts. The brushstroke logo specification handles the hard problem of legible-but-handpainted text rendering.

#### 3.3 — Shoes (Nano Banana Pro)
*Source: PDF item 3. Nano Banana Pro chosen here for its multi-view reference sheet capability.*

```
Technical footwear reference sheet showing ONE original trail sneaker in 4 views,
2x2 grid, pure white background #FFFFFF, sharp studio lighting, photorealistic
textures. Fully original design.

LOGO:
- 6-pointed organic star shape (curved pointed rays, small center circle)
- TWO placements:
 1. Lateral side panel: small ~2cm, glossy silver/chrome on dark panel — subtle
 2. Outsole center heel: same star molded in rubber, #d1fe17 lime yellow, ~3cm

SHOE DESIGN:

CONSTRUCTION STYLE:
- Multi-panel upper — technical mesh base with external structural cage overlay
- Open ventilation mesh windows on lateral and medial sides — visible through
cage
- Cage/exoskeleton overlay: organic curved structural frame — GLOSSY
LACQUERED medium gray / silver-gray — high shine patent/lacquer finish, reflects
light sharply, like glossy patent leather or lacquered plastic
- Cage lacing: bungee cord threads through cage eyelets

MATERIALS:
- Main mesh base: black/charcoal technical mesh
- Cage overlay panels: glossy lacquered silver-gray — high gloss, mirror-like
sheen, sharp light reflections visible on curved surfaces
- Toe cap: reinforced rubber bumper, matte black
- Heel counter: structured matte black with padded collar
- Pull tab: large loop at heel, black woven webbing with metal D-ring

LACING:
- Bungee/quick lace system through cage eyelets
- Laces: #d1fe17 acid lime yellow — sharp contrast against glossy gray and black

MIDSOLE:
- Medium height ~28mm
- Upper layer: light silver-gray matching cage tone
- Lower layer: thin #d1fe17 lime stripe running full length
- Slight rocker geometry

OUTSOLE:
- Aggressive lug pattern, black rubber
- Center heel: star logo molded, #d1fe17 lime
- Forefoot flex grooves

COLORWAY: black mesh + glossy lacquered silver-gray cage + #d1fe17 lime laces
and midsole stripe + matte black rubber

—— 4 VIEWS ——

TOP LEFT — LATERAL SIDE: full left profile, glossy gray cage with sharp light
reflections, black mesh windows, lime laces, midsole lime stripe, small star logo on
side panel
TOP RIGHT — OVERHEAD: top down, glossy cage panels catching light, bungee
lacing, padded collar
BOTTOM LEFT — HEEL REAR: heel counter, pull tab, lime midsole stripe at base
BOTTOM RIGHT — OUTSOLE: sole up, full lug tread, lime star logo at heel center

PRESENTATION:
- All 4 same shoe same colorway
- Pure white background, NO text, NO callouts, NO labels
- Thin gray lines between panels only
- Glossy lacquer finish must be clearly visible — sharp specular highlights on cage
panels
```

What makes this example work: structured sections (Construction Style / Materials / Lacing / Midsole / Outsole / Colorway / 4 Views / Presentation) — sectioned-prompt style is appropriate here because the brief has discrete categories of detail. Each view has a specific framing brief. The hex codes recur across sections to enforce color consistency. The "NO text, NO callouts, NO labels" negative prevents the model from adding annotation-style overlay text.

#### 3.4 — Pants (Soul Cinema)
*Source: PDF item 4.*

```
Flat lay product mockup of oversized wide-leg parachute track pants, ghost
mannequin style, isolated on pure white background #FFFFFF, sharp studio
lighting.

FABRIC & TEXTURE:
- Crinkled nylon parachute fabric — visible crinkle texture across entire surface
- Lightweight ripstop nylon, slightly shiny, crisp hand feel
- Natural crease/wrinkle texture throughout

SILHOUETTE:
- Extremely wide-leg, balloon/parachute silhouette — very voluminous from hip to
ankle
- High waist with elastic waistband + drawstring
- Loose gathered folds creating natural folds and volume
- Tapered slightly at ankle with adjustable toggle/drawstring hem
- Clean sides — no cargo pockets

BASE COLOR: deep matte black #0D0D0D

CONSTRUCTION DETAILS:
- Elastic waistband approximately 4cm, pull-on style
- Internal drawstring at waist with small metal aglets
- Single vertical piping stripe running down outer seam of each leg full length
- Piping stripe color: #d1fe17 acid lime yellow, double thin parallel lines approx
5mm total width
- Ankle hem: toggle drawstring in matching black

LOGO ON LEFT THIGH (small, embroidered or printed):
- Abstract geometric symbol only — NO letters, NO text, NO words
- Two intersecting diagonal lines forming an X shape with a small circle at the
center intersection
- Size: approximately 3–4cm
- Color: #d1fe17 acid lime

Colors: matte black base, #d1fe17 lime piping and logo only

Technical: flat lay top-down symmetrical view, ghost mannequin, full length pants,
ultra high resolution, isolated on #FFFFFF, photorealistic crinkle nylon fabric
texture, apparel product photography
```

What makes this example work: same sectioned-prompt template as the T-shirt (item 1) — Fabric & Texture / Silhouette / Base Color / Construction Details / Logo / Colors / Technical. Reusable scaffold per item. The "NO letters, NO text, NO words" negative on the logo block prevents text-rendering bleed. The dimensional specifications (waistband ~4cm, piping ~5mm, logo ~3–4cm) keep proportions consistent.

#### 3.5 — Sunglasses (Soul Cinema)
*Source: PDF item 5.*

```
A full product shot of sports sunglasses / athletic shield glasses, entirely visible,
nothing cropped or cut off, floating centered on a pure white background. Inspired
by high-performance sport shield sunglasses design, single lens wraparound
shield style, sleek and aerodynamic frame. Bold and angular frame shape,
lightweight matte finish. Small clean wings logo engraved or printed on the temple
arm of the frame. Lens options: dark tinted single shield lens, mirror finish. Sporty
aggressive silhouette, premium athletic eyewear aesthetic. Pure white studio
background, no shadows, no gradients, no clipping, no cropping, full glasses
visible from temple to temple, 8K detail, sharp product photography, eyewear
catalog style, front view and slight three-quarter angle view side by side.
```

What makes this example work: shorter than the clothing items because eyewear is structurally simpler — single lens, single frame, two temple arms. Two-view brief (front + three-quarter angle) handled in one prompt rather than separate generations. The "no shadows, no gradients, no clipping, no cropping" pattern recurs from items 2 and 3 — Adil's standard product-shot negative-constraint cluster.

---

## 4. Locations stage (Soul Cinema)

Soul Cinema doubles as a location-generation surface in Adil's recipe. Locations get pre-generated as image references and passed to Marketing Studio in the additional `medias[]` slot (see `SKILL.md` §6).

Demonstrated locations:
- Lip balm: desert sand with flowers bursting from sand [SRT-3:00:12:00 area, fed PDF item 6's Hyper Motion-style render in SRT-3:~00:11:30]
- Perfume: warm beige interior with silk panels [SRT-3:00:12:30 area]
- TV Spot: monochrome city street, train station backdrop [SRT-3:00:18:00 area]
- Urban pedestrian overpass + dark underground parking garage [PDF item 6 location parts 1 and 2 — Pro Virtual Try-On Liquid Scan Transition]

The PDF doesn't include the Soul Cinema location prompts themselves — only the Marketing Studio prompts that reference them. For Soul Cinema generation depth (Soul ID, Character Anchor Block, Two-Tool Refinement Pipeline), see `../higgsfield-soul/SKILL.md`.

In Marketing Studio, custom locations flow through the standard `medias[]` array alongside the product image:

```
medias=[
  {value: '<product uuid>', role: 'image'},
  {value: '<location image uuid or url>', role: 'image'},
]
```

Marketing Studio renders the location as the scene's environment rather than treating it as a separate UI-level field — the model honors the spatial / lighting characteristics of the location image as part of the generation.

---

## 5. Refinements + packaging stage (Nano Banana Pro)

Nano Banana Pro is Adil's go-to for two kinds of work:

**Refinements:** logo color swaps onto existing items, view-variant generation (the `front view` / `rear view` chain-prompt pattern visible in SRT-2:~00:06:00), multi-view technical sheets. Demonstrated throughout SRT-2: 00:04:54 logo refinement, 00:06:00 multi-view shoe sheet.

**Packaging:** premium packaging design with brand-kit awareness. Demonstrated in SRT-2:~00:33:00 for the Quantum Cosmos packaging concept.

Packaging output flows into Marketing Studio's Unboxing preset via the additional-asset slot (see `SKILL.md` §6):

```
medias=[
  {value: '<product uuid>', role: 'image'},
  {value: '<packaging image uuid or url>', role: 'image'},
]
```

### Worked example from PDF item 14 (Quantum Cosmos packaging)

*Source: PDF item 14.*

```
Use the provided logo to design a premium packaging concept for a clothing
collection called "Quantum Cosmos".

Create:
- A box and a shopping bag with a cohesive visual identity.

Concept direction:
Futuristic, minimal, inspired by physics / Higgs field / cosmic aesthetics.
Feels like a scientific object mixed with high-end fashion.

Design details:
- Clean typography, subtle markings (like lab labels or serial numbers)
- Strong, controlled layout with lots of empty space
- Avoid clutter, keep it refined and intentional

Bag:
- Matte black base
- Add cosmic visuals (stars, nebula, soft space textures) in a natural, expressive
way
- Keep it premium, not overly loud
- Minimal typography:
  "QUANTUM COSMOS — DROP 01"
  "QC_01"
- Text small and well-placed
- Logo integrated cleanly

Box:
- Solid #D1FE17 green color
- Ultra minimal design
- Only a very small logo or "QC_01"
- No large text
- Clean, premium surface

Presentation:
- Show both items clearly together
- Black background
- High-end product visualization style

Overall feel:
Luxury, experimental, clean, futuristic — strong contrast between expressive bag
and ultra minimal box.
```

What makes this example work: the "Use the provided logo" opening makes the reference-image dependency explicit. Two distinct items (bag and box) get separate design sections — the model treats them as paired but distinct objects. The "Overall feel" closing line ("Luxury, experimental, clean, futuristic — strong contrast between expressive bag and ultra minimal box") reinforces the design tension the prompt is asking for. Hex code `#D1FE17` matches the brand lime used across the clothing items, maintaining brand consistency across surfaces.

---

## 6. Final video stage (Marketing Studio)

Once you have brand-identity assets (Stage 1), locations (Stage 2 if needed), and refinements / packaging (Stage 3), Stage 4 pulls them together in Marketing Studio.

This satellite doc doesn't duplicate the Marketing Studio depth. For:

- The 9 presets and per-preset register notes — see `SKILL.md` §3
- The 4 reference-media slots and the call shape (`avatars` and `medias` are sibling top-level arrays, NOT nested in `params`) — see `SKILL.md` §6
- The full `marketing_studio_video` parameter schema — see `SKILL.md` §7
- 8 production-grade worked examples covering 5 of the 9 presets (Pro VTO ×2, UGC ×1, Hyper Motion ×1, Wild Card ×2, TV Spot ×2) — see `SKILL.md` §10

---

## 7. End-to-end worked example — Adil's HIGGS brand build

Adil's HIGGS clothing brand build (the SRT-2 demonstration) is the canonical end-to-end recipe. Trace through all four stages:

1. **Brand-identity (Stage 1, PDF items 1–5):** T-shirt, Jacket, Shoes, Pants, Sunglasses mockups generated via Soul Cinema (items 1, 2, 4, 5) + Nano Banana Pro (item 3, multi-view shoe sheet). Full prompts embedded in §3 above. Each item established as a registered product entity in Higgsfield's product library — see `SKILL.md` §6 for the registration paths.
2. **Locations (Stage 2, not in PDF):** Custom backdrops generated in Soul Cinema per scene needs. The urban pedestrian overpass + dark underground parking garage that PDF item 6 (Liquid Scan Transition) references were generated this way. Visible in SRT-2:~00:11:30 demo. Soul Cinema prompts not in the PDF; for Soul Cinema location-generation depth, see `higgsfield-soul`.
3. **Packaging (Stage 3, PDF item 14):** Quantum Cosmos branded packaging via Nano Banana Pro for the Unboxing preset. Full prompt embedded in §5 above.
4. **Final ad videos (Stage 4, PDF items 6–13):** 8 production videos across 5 Marketing Studio presets — Pro Virtual Try-On Liquid Scan (PDF 6), UGC Try-On 5 Clips (PDF 7), Logo Hyper Motion (PDF 8), Pro Virtual Try-On Skateboard (PDF 9), Wild Card Levitation (PDF 10), Wild Card Portal Cuts (PDF 11), TV Spot v1 (PDF 12), TV Spot v2 (PDF 13). Full prompts embedded in `SKILL.md` §10.

### What the recipe deferred (5 of 9 presets unused)

Adil's SRT-2 session demonstrated 5 of the 9 Marketing Studio presets. These 5 didn't get worked examples in this production session:

- **UGC (vanilla)** — preset 1
- **Tutorial** — preset 2
- **Unboxing** — preset 3 (PDF item 14 produces the packaging asset for Unboxing, but no Unboxing video prompt is in the PDF)
- **Product Review** — preset 5
- **UGC Virtual Try On** — preset 8 (PDF item 7 covers something close — "UGC Try-On 5 Clips" — but uses the basic UGC preset, not UGC VTO specifically)

For those preset registers, the source corpus's prose-craft layer (`marketing-studio-director.md` per-preset rules, summarized in `SKILL.md` §3) is the primary guidance. The lack of worked examples in this session isn't a gap in Marketing Studio — it's a scope choice in Adil's specific demo.

---

## 8. Surface coverage map (in-scope vs deferred)

Honest table of what's covered today vs. what's deferred:

| Surface | Coverage in our skill (as of v3.7.16) |
|---|---|
| Marketing Studio video (`marketing_studio_video`) | **In-scope** — covered in this directory's `SKILL.md` |
| Cross-surface workflow (this doc) | **In-scope** — connection layer between MS and image-side surfaces |
| Soul Cinema (image gen + locations) | **In-scope** — depth in `../higgsfield-soul/SKILL.md` (Soul ID + Character Anchor Block + Two-Tool Refinement Pipeline) |
| GPT Image 2.0 (image gen) | **Shipped in v3.7.16** — translated to `../higgsfield-gpt-image-2/SKILL.md` (three-format prompt taxonomy: Format A JSON / Format B prose / Format C meta-prompt). Translates `gpt-image-2-director` source corpus per the v3.7.13 marketing-studio precedent. |
| Nano Banana Pro (image gen) | **Referenced, not covered** — Nano Banana Pro sibling-director hunt deferred indefinitely |
| `ms_image` ("DTC Ads") | **Expanded in §3.b (v3.7.16)** — Phase 0 architectural option β rescope: full sub-skill deferred (Adil source corpus has zero coverage of `ms_image` — see § 3.b.v source-corpus reconciliation #12), §3 expanded into §3.a / §3.b.i–v structure with capability summary + parameter schema + recommendation heuristic + naming reminder + source-corpus reconciliation. |
| `marketing_studio_image` (basic MS image) | **Referenced (`SKILL.md` §2), not covered** — out of scope; lower-capability than `ms_image` |
| Static-image cross-surface (e.g., reference-swap ad recreation) | **Shipped in v3.7.16** — translated to `../higgsfield-gpt-image-2/static-ads-workflow.md` satellite (fractional-coordinate zones, brand-neutral wireframe intermediation, safe-zone top/bottom-10% rule, brand-vs-structure separation, three template patterns: iMessage / Scarcity Countdown / Ingredient Spotlight). |
| Cinematic prompt-pattern vocabulary (Camera Contract, Motion Physics Anchor, etc.) | **Shipped in v3.7.15** — translated to `vocab.md` § Camera Movement Terminology (Camera Contract, Motion Physics Anchor, Lens Behavior Sequence) + § Composition Vocabulary (Negative-prompt reinforcement, Spatial Zoning, Negative space expansion). 4 of 5 pillars added as new subsections; Negative Space extended from existing L338 coverage with negative-prompt reinforcement pattern + Spatial Zoning binding. |

The full deferral list with reasoning is in the v3.7.13 CHANGELOG's Scope acknowledgment subsection.

---

## 9. Source acknowledgment

Adil's documented production recipe is the substrate for this workflow doc; full attribution and source corpus citation in `SKILL.md` §13.

One addition specific to this doc: the `ms_image` ("DTC Ads") surface (correction #12) was surfaced by [Phase 0: Probe 0.3-a] as net-new intel beyond what Adil's source corpus documents. Verification trail in `../../.planning/v3.7.13/PHASE-0-PROBES.md`.
