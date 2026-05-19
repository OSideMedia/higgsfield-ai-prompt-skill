---
name: higgsfield-gpt-image-2
description: "Use when the user mentions GPT Image 2.0, gpt-image-2, GPT-Image-2 prompts, or wants to generate an image with GPT Image 2.0. Covers the three-format prompt taxonomy (Format A structured JSON for UI mockups and layout-dense images; Format B dense cinematic prose for single-subject scenes; Format C auto-derive meta-prompt for theme-only concepts), per-format craft patterns, output conventions, the 6-item pre-delivery checklist, and cross-surface workflow context (companion static-ads-workflow.md for ad recreation; higgsfield-marketing-studio cross-surface-workflow.md §3 for ms_image / DTC Ads Higgsfield-native alternative)."
user-invocable: true
metadata:
  tags: [higgsfield, gpt-image-2, prompt-director, image, json, prose, meta-prompt, layout, mockup, infographic, character-sheet, ui-mockup, landing-page, static-ads, cross-surface]
  version: 1.0.0
  updated: 2026-05-18
  parent: higgsfield
---

# Higgsfield GPT Image 2.0

A prompt director for GPT Image 2.0. Converts plain-text concepts into production-ready prompts that route by output type: structured JSON for layout-dense images (UI mockups, infographics, character sheets, multi-panel posters), dense cinematic prose for single-subject scenes (portraits, photographs, landscapes), or auto-derive meta-prompts for theme-only concepts where the model self-generates the composition.

Translated from Adil Aliyev's `gpt-image-2-director` source corpus per the v3.7.13 / v3.7.15 translation precedent. The companion `static-ads-workflow.md` satellite covers the ad-recreation workflow that uses GPT Image 2.0 as its generation engine.

---

## 1. What GPT Image 2.0 is

GPT Image 2.0 is an image-generation model with a distinct capability profile that shapes how its prompts should be written. Four properties drive format choice across the three prompt taxonomies in §§ 2–5 below:

**Granular layout precision.** GPT Image 2.0 honors granular layout instructions — top-left panel shows X, mid-right shows Y, N icons in a row labeled A/B/C — in a way other models don't reliably match. This is testable: run the same multi-region brief against comparable image models and observe the difference. It's also why the Format A JSON taxonomy works as well as it does: the model reads JSON region keys as layout intent.

**Text rendering.** Multi-line paragraphs, mixed scripts (CJK + Latin), small UI labels, numeric data in tables — all sharp and legible. This is one of the model's distinctive strengths over comparable image generators. Same testability boundary: a user can verify by running prompts with mixed scripts and small UI labels against comparable models and observing the difference. The implication for prompts: embed real text in quotation marks exactly as it should render; do not paraphrase.

**Design and UI as sweet spot.** Website landing pages, social-feed mockups, magazine covers, infographics, exploded product diagrams, exam-paper layouts — anything with real information density. Lean prompts into the strengths.

**Cinematic photorealism is the weakness.** Human faces often go plasticky on realism-flagged prompts. Lean into stylized, illustrated, or editorial aesthetics rather than hyperreal skin. When realism is requested, frame it as film photography (grain, flash, 35mm) rather than as "photorealistic" — film-photography language tends to produce the look users want without triggering the plasticky-skin failure mode. Cross-reference: [vocab.md](../../vocab.md) § Visual Style Vocabulary → Film Stock Emulation for the broader film-photography language family.

---

## 2. Three prompt formats

Pick one based on the user's concept. If the concept fits multiple, pick the one best suited to the subject — don't hedge.

| Format | Use when | Output type |
|---|---|---|
| **A — Structured JSON** | Output has discrete regions, labeled parts, UI chrome, multi-panel grids, or information hierarchy | UI mockups, landing pages, infographics, exploded diagrams, character reference sheets, social-media post mockups, magazine layouts, editorial document renders, multi-panel posters, comic / manga pages, brand-identity boards, design-system boards, card grids |
| **B — Dense cinematic prose** | Output is one scene, one frame, one subject with no chrome or layout regions | portraits, cinematic scenes, concept art, illustrations, landscapes, fashion shots, character moments |
| **C — Auto-derive meta-prompt** | User gives a theme and wants the model to self-generate the whole composition | concept posters from a single topic, character relationship diagrams, encyclopedia-style infographics |

Each format has its own craft patterns in §§ 3–5 below. The routing decision is consolidated in § 6.

### Tie-break

When in genuine doubt between A and B (e.g., "a character with some labels around them") — default to A. Layout precision is GPT Image 2.0's primary differentiator and prompts should reach for it.

---

## 3. Format A — Structured JSON

Write a single JSON object describing every visible region. GPT Image 2.0 reads this as a layout spec.

### Core fields to reach for

- `type` — one-line description of what this image is ("infographic poster", "landing page mockup", "exploded view diagram", "anime character reference sheet", "social media app interface mockup")
- `style` — the visual style ("cute flat vector illustration, cozy, warm, soft shading", "clean high-tech 3D render, studio lighting, glowing accents", "GTA V cover art style, cel-shaded, thick black panel borders")
- `subject` or `character` — the main entity, with specific visual attributes
- `layout` — nested objects for regions: `header`, `centerpiece`, `sections`, `footer`, `left_side`, `right_side`, `grid_panels`, `top_header`, `bottom_bar`, etc. This is where precision matters most.
- `background` — color, texture, or scene
- Text content embedded in quoted strings. Keep real text if the user provided it — don't paraphrase. CJK and other non-Latin scripts stay in their original form.

### Key patterns that make JSON prompts work

**Count-and-label pattern.** When there are multiple similar items (buttons, icons, chat messages, panels, callouts), give a `count` and a parallel `labels` array:

```json
"messages": {
  "count": 7,
  "items": ["user1: hello", "user2: hi there", "..."]
}
```

**Position-scoped regions.** Explicitly name positions: `top-left`, `top-center`, `mid-right`, `bottom-center-right`. GPT Image 2.0 respects these.

**Section objects with title, position, count, labels.** For infographics with multiple zones:

```json
{
  "title": "衣装・装備詳細",
  "position": "bottom-left",
  "count": 9,
  "labels": ["胸当て", "肩当て", "腕甲", "..."]
}
```

**Templateable slots with `{argument name="x" default="y"}`.** When a user explicitly wants a reusable template, slot notation like `{argument name="city" default="Tokyo"}` works. As a heuristic, don't add slots by default on one-off prompts — keep the prompt concrete. When slots are used, the default value should be a realistic value, not a placeholder string.

**Inline typography callouts.** When typography matters, include it inline: `"title in large serif font"`, `"11px Inter Regular"`, `"Space Grotesk Bold Caps"`.

### Worked example — minimal shape

```json
{
  "type": "landing page mockup",
  "style": "clean modern e-commerce, soft pastel palette, generous whitespace",
  "layout": {
    "header": {
      "logo": "small black wordmark 'AURA'",
      "nav": ["Shop", "About", "Journal", "Contact"],
      "cart_icon": "top-right"
    },
    "hero": {
      "left_side": "large product photo of amber glass serum bottle on marble",
      "right_side": {
        "headline": "Skin, restored.",
        "subheadline": "A 7-day reset ritual. Clinically tested.",
        "cta_button": "black pill button 'Shop the ritual'"
      }
    },
    "below_hero": {
      "ingredient_grid": {"count": 4, "labels": ["Vitamin C", "Niacinamide", "Peptides", "Hyaluronic Acid"]}
    }
  }
}
```

For the ad-recreation variant of structured layout — fractional-coordinate zone notation, safe-zone discipline, brand-vs-structure separation, wireframe intermediation — see the companion [`static-ads-workflow.md`](static-ads-workflow.md) § 3 (Layout zones + safe zones) and § 4 (Brand-vs-structure separation).

---

## 4. Format B — Dense cinematic prose

Write one continuous paragraph. Order the information roughly as: image type / medium → main subject with specific visual details → pose or action → background / setting → environmental details → lighting → color palette / film stock / texture → mood descriptor.

*Roughly* because GPT Image 2.0 handles slight ordering deviation gracefully — the order is a scaffolding, not a HARD RULE. The point is to put the most concrete visual anchors (medium, subject, props) early enough that the model commits to them before downstream details modify.

### What makes prose prompts work

**Specific over atmospheric.** "White ribbed tank top and a loose beige knit cardigan slipping off one shoulder" beats "casual outfit". GPT Image 2.0 executes specificity better than it interprets mood.

**Concrete props and objects.** Reference exact things: "a white vintage Toyota Levin hatchback with red taillights", "an open notebook, a pen, and a pink flower on a desk". See [vocab.md](../../vocab.md) § Composition Vocabulary for the broader spatial-anchoring vocabulary that pairs with concrete-prop direction.

**Camera and film language.** "35mm film photograph", "direct camera flash", "low-angle dynamic perspective", "aerial drone shot", "shallow depth of field" — these actually steer the output toward the look named.

**Embedded text in quotation marks.** When text appears in the image, put it in quotes exactly as it should render: `elegant vertical Japanese text that reads "都会の夜に溶けていく"`. This pattern leans into the text-rendering capability documented in § 1.

**Avoid "photorealistic" when faces are in frame.** Use "cinematic", "film photograph", "35mm", "editorial portrait" instead — these bias toward a look GPT Image 2.0 actually nails, rather than triggering its plasticky-skin failure mode. Cross-reference: § 1 capability framing + [vocab.md](../../vocab.md) § Visual Style Vocabulary → Film Stock Emulation.

### Worked example

> A cinematic, moody photograph of a young Asian woman looking back over her shoulder at the viewer on a rainy night in a bustling street. She has wet, stringy black hair plastered to her face and a melancholic expression, wearing a loose, oversized greyish-green jacket. The street is wet, reflecting the blurred, glowing neon signs and traffic lights of the city. Parked on the wet asphalt to her left is a white vintage Toyota Levin hatchback with its red taillights illuminated. On the top left side of the image, elegant vertical Japanese text reads "都会の夜に溶けていく" in a large serif font. The overall aesthetic is atmospheric and cinematic, 35mm film texture, muted warm palette, capturing a quiet introspective moment amidst urban chaos.

What this example demonstrates: cinematic-medium opening ("A cinematic, moody photograph"), specific subject detail (wet stringy hair, oversized jacket), concrete prop (white vintage Toyota Levin hatchback with red taillights), embedded text in original CJK script with size + font direction ("elegant vertical Japanese text reads … in a large serif font"), film-stock language ("35mm film texture"), mood closing line. The CJK text rendering is the simplest demonstration of § 1's text-rendering capability — preserve or substitute embedded text as appropriate to the user's concept.

---

## 5. Format C — Auto-derive meta-prompt

The user gives a theme. You write instructions for the model to self-generate the full composition.

### Structure

```
Please automatically generate a [output type] centered around [THEME].

Require the AI to automatically derive and uniformly design the entire following visual system based on this theme, without my extra specification:
- [list of derivations the model should make — core subject, supporting structure, hovering elements, color hierarchy, material contrast, lighting, typography, etc.]

[Overall Style]
[specific style direction — "cel-shaded illustration", "ultra-realistic 3D commercial CGI rendering", "watercolor and ink hand-drawn illustration", etc.]

[Composition Rules]
- [rules about premium quality, central order, negative space, hierarchy]

[Visual Quality]
- [rules about detail level, lighting, materials]

[Typography System]
- [ratio of visual to text, title/subtitle generation, font temperament]

[Signature]
Naturally add the signature "[NAME]" in the [position].
```

### When to use

The user gives only a theme ("Chinese emperors", "Demon Slayer character map", "the psychology of procrastination") and wants a rich, self-derived output. If they give specific layout details, use Format A instead — the auto-derive meta-prompt cedes layout control to the model, which is the wrong choice when layout precision was specified.

---

## 6. Routing decision

Scan the user's concept and pick based on what they describe:

- **Mockup, UI, landing page, infographic, poster with panels, character sheet, magazine layout, grid, dashboard, diagram, social feed, exam paper, technical document** → **Format A (JSON)**.
- **One scene, one subject, one frame** with no discrete regions — a portrait, a cinematic shot, a landscape, a character moment, an illustration, a photograph → **Format B (prose)**.
- **A theme only** with the user asking you to design the whole thing — "make a poster about X", "relationship diagram of X", "encyclopedia page for X" without specifying the layout → **Format C (meta-prompt)**.

When in genuine doubt between A and B (e.g., "a character with some labels around them"), default to A per § 2 tie-break. The cost of routing to A when B was acceptable is small (extra layout precision); the cost of routing to B when A was needed is larger (lost layout anchoring).

---

## 7. Output format conventions

Return only the finished prompt in a code block. No preamble, no explanation, no "here's your prompt:", no format-choice justification. The user pastes it into GPT Image 2.0 directly.

This matches root [SKILL.md](../../SKILL.md) HARD RULES item 7 (output the prompt; no preamble) — same production discipline applied at this surface.

**Code-block conventions:**

- **JSON prompts:** wrap in a ` ```json ` code block.
- **Prose prompts:** wrap in a plain ` ``` ` code block.
- **Meta-prompts:** wrap in a plain ` ``` ` code block.

**Multiple variations:** when the user asks for multiple variations, return them as separate code blocks with a one-line label before each (e.g., `**Variant A — magazine layout:**`).

---

## 8. Pre-delivery checklist

Before outputting the prompt, scan it against this 6-item check. The pass takes 30–60 seconds; the savings compound across iteration loops.

1. **Region coverage** — does every distinct visible region have a named location or field?
2. **Counts and labels** — are counts and labels explicit where there are multiple similar items?
3. **Real text preserved** — is real text kept in its original language and in quotes, ready to render?
4. **Realism framing** — for face-heavy prompts, have you avoided "photorealistic" in favor of film / cinematic language (per § 1, § 4)?
5. **Style specificity** — is the style line specific enough to produce a recognizable aesthetic, or is it generic adjective stacking?
6. **JSON validity (Format A only)** — is the JSON valid (check braces, commas, escaping of quotes inside strings)?

This is the surface-specific operationalization of the cross-cutting pre-delivery discipline. See [DISCIPLINE.md](../../DISCIPLINE.md) § Pre-Delivery Discipline for the underlying pattern (the v3.7.5 + v3.7.7 audit-corpus discipline applied across multiple sub-skills).

---

## 9. Example routings

Six paired examples showing the routing decision in practice.

| User concept | Format | Reasoning |
|---|---|---|
| "make me a landing page for a matcha tea startup called Kori, emphasis on clean Japanese minimalism" | **A (JSON)** | Landing page has discrete regions (header, hero, product grid, footer) — Format A's primary use case. |
| "a teenage girl sitting alone at a bus stop at dusk, 90s vibe" | **B (prose)** | Single scene, no layout. |
| "make a poster about the history of the samurai" | **C (meta-prompt)** | Theme only; no specifics on layout. |
| "a character reference sheet for a cyberpunk bounty hunter named Iris, show front/side/back views and 4 expressions" | **A (JSON)** | Explicit layout regions ("front/side/back views and 4 expressions"). The 'character sheet' label is a strong Format A signal. |
| "photo of an old man fixing a vintage arcade machine, lit by the machine's screen" | **B (prose)** | One framed photograph. |
| "infographic about the types of clouds, make it look like a vintage encyclopedia page" | **A or C** | If the user lists the cloud types and what to show for each → A. If they just say "types of clouds" and expect you to fill it in → C. |

---

## 10. Cross-surface workflow context

GPT Image 2.0 is one image-side surface in the Higgsfield platform ecosystem. Two cross-surface paths are worth naming:

**Companion: ad-recreation workflow.** When the user uploads a winning ad format and wants to recreate it with their brand's products and copy, route to the companion [`static-ads-workflow.md`](static-ads-workflow.md). That doc covers the 10-step workflow that uses GPT Image 2.0 as its generation engine plus the production discipline (fractional-coordinate zone notation, safe-zone top/bottom-10% rule, brand-vs-structure separation, wireframe intermediation) that Adil's source corpus documented.

**Higgsfield-native alternative: ms_image / "DTC Ads".** Higgsfield's platform exposes a native image-generation surface for ad work — `ms_image` (display name "DTC Ads") — that is brand-kit-aware (accepts `brand_kit_id`), ad-format curated (accepts required `style_id`), supports batch generation up to 20 images per call, and accepts up to 14 reference media. For brand-kit-consistency-across-many-images use cases or batch generation of 5–20 ads per call, ms_image is the more integrated option. Adil's source corpus doesn't document ms_image (source-corpus reconciliation #12) — treat GPT Image 2.0 as the default for image-side work, and reach for ms_image when its specific differentiators apply. See [the Marketing Studio cross-surface-workflow.md](../higgsfield-marketing-studio/cross-surface-workflow.md) § 3 for the full ms_image coverage.

---

## 11. Source acknowledgment

GPT Image 2.0 coverage in this sub-skill is translated from source material by Adil Aliyev — Higgsfield-team-adjacent author of `gpt-image-2-director.md` (sibling to `marketing-studio-director.md` + `higgsfield-content-factory.md` translated in v3.7.13, and `cinematic-motion-language.md` translated in v3.7.15). Source corpus: `gpt-image-2-director` source skill (`SKILL.md`, ~14 KB, 206 lines).

### Per-claim translation calibration

Per the v3.7.13 author-signature calibration carried through v3.7.15: **format-routing taxonomy (Format A / B / C) is Adil's craft synthesis** (translated freely to our voice); **per-format vocabulary and craft patterns are standard prompt-engineering and cinematography** (adopted close to verbatim); **capability claims about GPT Image 2.0's prompt-following and text-rendering strengths** (translated under the v3.7.15 Spatial Zoning testability exception — testable directional claims about prompt-side effects pass the testability boundary; universalizing metaphysical claims about model cognition would not).

### Verification trail

Per-source disposition: [.planning/v3.7.16/PHASE-0-VERIFICATION.md](../../.planning/v3.7.16/PHASE-0-VERIFICATION.md) § VERIFY 0.1 (gpt-image-2-director source read + disposition class TRANSLATE-WITH-VERIFICATION LOWER-FRICTION SUB-CLASS).

Per-element translation rules: [.planning/v3.7.16/PHASE-1-INVENTORY.md](../../.planning/v3.7.16/PHASE-1-INVENTORY.md) § 1B-A (per-element ADOPT / DOWNGRADE table).

Companion satellite: [`static-ads-workflow.md`](static-ads-workflow.md) covers the static-ads.md source corpus translation per § 1B-B.
