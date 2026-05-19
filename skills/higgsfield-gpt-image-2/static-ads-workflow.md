---
name: higgsfield-gpt-image-2
description: >
  Cross-surface satellite document for higgsfield-gpt-image-2. Covers the ad-recreation
  workflow that uses GPT Image 2.0 as its generation engine — taking an uploaded ad
  format reference plus the user's brand identity and product images, deriving layout
  zones, generating brand-grounded copy variations, and rendering static ads. Includes
  the fractional-coordinate zone notation, brand-neutral wireframe intermediation,
  safe-zone top/bottom-10% rule, brand-vs-structure separation rule, and three worked
  template patterns (iMessage conversation, scarcity countdown, ingredient spotlight).
  Consulted from parent SKILL.md § 3 footer plus § 10 cross-surface workflow context
  when the user wants to recreate a winning ad with their brand's products and copy.
user-invocable: false
metadata:
  tags: [higgsfield, gpt-image-2, static-ads, ad-recreation, layout-zones, safe-zone, brand-identity, workflow, satellite]
  version: 1.0.0
  updated: 2026-05-18
  parent: higgsfield-gpt-image-2
---

# Static Ads Workflow

Cross-surface satellite for the [Higgsfield GPT Image 2.0](SKILL.md) sub-skill. Documents the ad-recreation workflow Adil established: take an uploaded ad format reference image, derive its layout structure as a fractional-coordinate zone grid, generate a brand-neutral wireframe at the target aspect ratio, and render the user's brand identity plus products plus copy through GPT Image 2.0 using the wireframe as a structural template.

This is the production-knowledge layer beneath the parent SKILL.md's general-purpose prompt-craft. When the user wants to recreate a winning ad format with their brand, route here; when the user wants any other kind of GPT Image 2.0 prompt, the parent SKILL.md three-format taxonomy covers it.

Translated from Adil Aliyev's `static-ads.md` source corpus per the v3.7.13 / v3.7.15 / v3.7.16 translation precedent.

---

## 1. Workflow prerequisites

Adil's static-ads recipe assumes a brand-identity scaffold already exists on disk. The original source corpus pins this to a specific directory shape:

```
./brands/[brand-name]/brand-identity/
├── visual-guidelines.md    — brand voice, typography, accent colours
├── products.json           — product catalog with product_url per product
└── product-images/         — per-product reference images
```

Translation note for our skill: the specific path convention is Adil's; the substance is a brand-identity reference document plus a product images folder accessible to the workflow. Exact paths and file names depend on your project structure. The recipe doesn't depend on the directory shape; it depends on the artifacts being available.

### When brand-identity files don't exist yet

Adil's source corpus assumes a `/brand` slash command bootstraps the brand folder. Our skill does not ship `/brand`; if your brand-identity files don't exist yet, you'll need to create them before running this workflow.

### Product page fetching

Adil's recipe fetches the live product page (per `product_url` in the brand's product catalog) to ground the copy in the brand's actual claims, ingredient lists, certifications, and exact product language. The pattern is *fetch product page → extract benefits / claims / certifications / brand-voice substance → use as primary source of truth for copy variations*. Our skill documents the pattern; the specific fetch tool depends on the execution environment (Higgsfield CLI, MCP, web browser, manual paste, etc.).

`visual-guidelines.md` informs tone; the live product page informs substance. Don't substitute one for the other — the tone document describes how the brand speaks; the product page describes what the brand is actually saying about this specific product right now.

---

## 2. The spec.json pattern

Each ad-recreation run produces one spec.json describing the recipe inputs plus per-variation prompts. The artifact lives at `[output-folder]/static-ad-spec.json` and looks roughly like this:

```json
{
  "output_name": "iMessage-energy-gel",
  "brand": "puresport",
  "product_name": "Energy Gel",
  "reference_image": "brands/puresport/static-ads/ad-references/iMessage-format.jpg",
  "layout_zones": {
    "text_zone":       {"top": 0.10, "bottom": 0.35},
    "product_zone":    {"top": 0.40, "bottom": 0.77},
    "button_zone":     {"top": 0.81, "bottom": 0.91},
    "disclaimer_zone": {"top": 0.91, "bottom": 0.97}
  },
  "product_images": [
    "brands/puresport/brand-identity/product-images/energy-gel-berry.jpg",
    "brands/puresport/brand-identity/product-images/energy-gel-angle.jpg"
  ],
  "aspect_ratio": "3:4",
  "additional_aspect_ratios": ["9:16"],
  "variations": [
    {
      "slug": "var-1",
      "prompt": "[fully resolved zone-based prompt for variation 1]"
    },
    {
      "slug": "var-2",
      "prompt": "[fully resolved zone-based prompt for variation 2]"
    }
  ]
}
```

The spec is a portable artifact: anyone with the spec.json plus the referenced images can invoke GPT Image 2.0 to render the variations. The spec captures every input the generation step needs — `reference_image` (if Mode A; see § 4), `product_images`, `layout_zones`, target aspect ratios, and the fully-resolved prompt per variation.

### Adil's helper scripts (not adopted into our skill)

The static-ads source corpus ships two helper scripts — `generate-static-ad.py` and `generate-reformat.py` — that take the spec.json and call the GPT Image 2.0 API to render and reformat outputs. Our skill documents the spec.json pattern but does NOT bundle these scripts. Users can invoke their own generation pipeline (Higgsfield CLI, MCP, direct API client, web UI) using the spec.json as input. The pattern is what's transferable; the helper-script implementation is environment-specific.

---

## 3. Layout zones + safe-zone discipline

Three production-discipline patterns that distinguish ad recreation from general-purpose GPT Image 2.0 prompts: fractional-coordinate zone notation, wireframe intermediation, and the safe-zone rule. These are the highest-value content in the source corpus — specific, falsifiable, and transferable to non-GPT-image-2 platforms.

### Fractional-coordinate zone notation

Express each content zone as a fraction of total frame height (0.0 = top edge, 1.0 = bottom edge). Standard zone names used across Adil's recipe:

- `text_zone` — where headline and sub-headline sit
- `product_zone` — where the product is placed
- `button_zone` — where the CTA button sits
- `disclaimer_zone` — where the disclaimer text sits

Concrete example for a calling-screen format:

```json
"layout_zones": {
  "text_zone":       {"top": 0.10, "bottom": 0.35},
  "product_zone":    {"top": 0.40, "bottom": 0.77},
  "button_zone":     {"top": 0.81, "bottom": 0.91},
  "disclaimer_zone": {"top": 0.91, "bottom": 0.97}
}
```

The fractions are falsifiable production direction: a static ad with text below the 0.35 cutoff or a CTA outside the 0.81-0.91 band fails the convention. For the broader vocabulary of named regions in non-ad contexts, see [vocab.md](../../vocab.md) § Composition Vocabulary → Spatial Zoning.

### Wireframe intermediation

The zones aren't just descriptive — they generate a brand-neutral wireframe at the target aspect ratio. The wireframe is what gets passed to GPT Image 2.0 as Image 1, NOT the original reference ad. This eliminates colour, typeface, and style contamination from the reference, and there is no aspect ratio conflict regardless of source format.

This is the non-obvious workaround technique most worth preserving from Adil's corpus: the brand-neutral wireframe lets you inherit *layout structure* from a reference ad without inheriting its *visual identity* — exactly the separation § 4 operationalizes.

In practice: render a simple block layout at the target aspect ratio with each zone's bounding box drawn as a labeled rectangle (the zone name as a callout — "text_zone", "product_zone", etc.). That blocky reference image becomes Image 1 in the Mode A call below. GPT Image 2.0 reads the wireframe as a layout spec and produces an ad that honors the spatial grid without copying the reference ad's visual treatment.

### Safe-zone top/bottom-10% rule

Keep the top 10% and bottom 10% of the frame free from text, logos, icons, buttons, and UI elements — photographic content such as hands, arms, or product edges entering the frame is fine. This applies to every prompt in every mode — no exceptions.

The HARD-RULE volume here is justified by the platform UI reality the rule responds to: Instagram and TikTok's UI overlays consume the top and bottom ~10% of the frame. Text or buttons placed in those zones get obscured by the platform chrome at delivery time. The rule isn't craft opinion; it's verifiable surface fact about how social platforms render image ads in their feeds. Cross-reference [parent SKILL.md](SKILL.md) § 3 (Format A → JSON layout precision) for the general-purpose layout discipline this safe-zone rule specializes.

---

## 4. Brand-vs-structure separation

The core operational rule of the ad-recreation workflow. The reference ad belongs to another brand; treat it as a structural template only — never copy its visual identity.

### The two-list rule

**Take from the reference:**
- Layout format
- Zone positions and proportions
- UI element types (toggle switches, countdown blocks, iMessage bubbles, etc.)
- Element placement and spacing logic

**Take from `visual-guidelines.md`:**
- Background colour
- Typeface and weights
- Accent colours (CTA colour, icon colour, badge colour, toggle colours)

The visual-side list **always overrides** whatever appears in the reference. Before writing any prompt, read `visual-guidelines.md` and explicitly name the brand's background colour, headline typeface, body typeface, and relevant accent colours. Never leave these to be inherited from Image 1 — the override needs to be explicit in the prompt body, not implicit in image-reference context.

### Mode A — Reference swap (when reference_image is present)

Image 1 is either the original reference ad OR (preferred per § 3) the brand-neutral wireframe generated from the reference's layout zones. The prompt explicitly overrides all visual brand elements from the user's `visual-guidelines.md` and keeps only the structural template:

```
Image 1 shows the reference ad layout. Use it as a structural template only — keep
the layout format, zone positions, element placement, and spacing. Replace everything
visual with the target brand's identity: background colour [BRAND BG from
visual-guidelines], typography [BRAND TYPEFACE + WEIGHT], accent colours
[BRAND ACCENT COLOURS]. Replace the product with the exact [BRAND PRODUCT] from
images 2+. Replace all copy with [VARIATION COPY]. Replace any third-party trust
badge with [BRAND TRUST SIGNAL]. Do not carry over any colour, typeface, or visual
treatment from the reference — those belong to another brand. [ASPECT RATIO] aspect
ratio. Safe zones: keep the top 10% and bottom 10% of the frame free from text,
logos, icons, buttons, and UI elements — photographic content such as hands, arms,
or product edges entering the frame is fine.
```

### Mode B — Text-driven layout (no reference_image)

Product images are Image 1+. The prompt carries all layout, brand, and copy instructions from scratch (no wireframe intermediation). The brand-vs-structure separation still applies: the prompt names the layout explicitly rather than inheriting it from a reference.

```
Create: [AD FORMAT DESCRIPTION]. Background: [BRAND BG COLOR]. [ZONE-BY-ZONE
DESCRIPTION using brand typefaces, colours, and copy]. Product: exact
[BRAND PRODUCT] from images 1+. [ASPECT RATIO] aspect ratio. Safe zones: keep the
top 10% and bottom 10% of the frame free from text, logos, icons, buttons, and UI
elements — photographic content such as hands, arms, or product edges entering the
frame is fine.
```

Safe zones apply to every prompt in every mode — no exceptions, per § 3.

For the general-purpose JSON layout discipline underlying both modes, see [parent SKILL.md](SKILL.md) § 3 Format A craft patterns. The ad-recreation specialization here is the brand-vs-structure separation, which Adil's general-purpose director doesn't apply at this level of explicit rule.

---

## 5. Template patterns

Three production-grade template patterns from Adil's static-ads corpus. Each template is a single-paragraph prompt with bracketed placeholders for copy plus brand-specific values. When constructing the internal prompt template from an uploaded ad, match the style and specificity of these examples — every layout element, colour, typographic treatment, and structural detail should be specified.

For the simpler JSON shape (non-ad-recreation contexts), see [parent SKILL.md](SKILL.md) § 3 Worked example. These three templates are the ad-recreation specialization.

### 5.1 — iMessage / DM Conversation

```
Use the attached images as brand reference for product design ONLY. Do NOT use polished
ad layouts. This must look like a real screenshot. Create: a static ad designed to look
like a genuine iMessage conversation screenshot. White background. Top: realistic iOS
header bar — centered contact name "[FIRST NAME]" in bold black with a gray circular
avatar initials icon, small gray "iMessage" label below the name, small blue "<" back
arrow left, blue "ⓘ" info button right. Below: a realistic iMessage thread. Three to
five message bubbles, alternating sides. Messages from the friend [gray bubbles,
left-aligned]: first bubble "[OPENING LINE — casual and natural, e.g. 'wait have you
tried [product category] yet?']". Second bubble "[FOLLOW-UP — a specific reason or
personal result, conversational, with an emoji]". Messages from the recipient
[blue bubbles, right-aligned]: one or two short skeptical or curious replies, e.g.
"[REPLY 1]" and "[REPLY 2]". Final gray bubble from the friend: "[CLOSING LINE —
product or brand mentioned naturally, recommendation energy, e.g. 'it's called
[BRAND], they have a deal rn']". Below the last bubble: a realistic iMessage link
preview card — rounded rectangle with [BRAND COLOR] header strip, small product
thumbnail left, bold black title "[PRODUCT NAME]" right, gray subtitle "[BRAND] ·
[TAGLINE or URL]". Timestamp "[TIME]" and blue "Delivered" in small text below.
iPhone bottom bar: white background, gray rounded text input field reading "iMessage",
camera and audio icons either side. No brand logo overlay. Should look exactly like a
screenshot a friend would text you. [ASPECT RATIO] aspect ratio.
```

What this template demonstrates: realistic-screenshot framing as the ad delivery vehicle (the format hides the ad-ness by mimicking a familiar UI). The negative direction "Do NOT use polished ad layouts" cuts against GPT Image 2.0's default tendency toward composed commercial framing. Note the dense per-element specification — every UI chrome element (back arrow, info button, "iMessage" label, "Delivered" indicator, camera + audio icons) is named explicitly, leaning into the parent SKILL.md § 1 layout-precision capability.

### 5.2 — Scarcity / Countdown Urgency

```
Use the attached images as brand reference. Match the exact product design, colors,
and typography style precisely. Create: a high-urgency limited-stock ad on a
[BACKGROUND COLOR] background. Top: small [ACCENT COLOR] all-caps label
"[URGENCY TAG]" in a rounded pill shape. Below: large bold white uppercase
sans-serif headline "[OFFER HEADLINE]". Second line in [ACCENT COLOR]:
"[SECONDARY HOOK — e.g. 'Only [N] left at this price.']". Center: product hero
shot on the dark background, clean studio lighting with dramatic rim light on one
edge. Below the product: a horizontal stock progress bar — [BRAND COLOR] fill
approximately [FILL %] full on the left, gray empty track on the right. Left label:
"[SOLD COUNT]" in small white text. Right label: "[REMAINING]" in small
[ACCENT COLOR] text. Below the bar: a realistic digital countdown timer with four
colon-separated blocks — days, hours, minutes, seconds — each in a dark
rounded-rectangle tile with white bold monospace digits and small gray labels. Below
timer: a large [ACCENT COLOR] rounded-rectangle CTA button spanning most of the
width, bold white text "[CTA TEXT]". Very bottom: small gray disclaimer text
"[DISCLAIMER]". Brand logo top-right corner in white. [ASPECT RATIO] aspect ratio.
```

What this template demonstrates: limited-stock urgency mechanics (progress bar + countdown timer) rendered as concrete UI elements rather than as adjectives. The stock progress bar specification ("[FILL %] full on the left, gray empty track on the right") plus the countdown timer specification ("four colon-separated blocks — days, hours, minutes, seconds — each in a dark rounded-rectangle tile") are exactly the kind of precise UI direction GPT Image 2.0's layout precision (parent § 1) honors. Note that the urgency tone lives entirely in the bracketed copy slots; the visual structure is calm and grid-disciplined — the format doesn't sell the urgency, the copy does.

### 5.3 — Ingredient Spotlight / Clean Label

```
Use the attached images as brand reference. Match the exact product design and brand
colors precisely. Create: an educational ingredient-spotlight ad on a
[BACKGROUND COLOR] background. Top: small [BRAND COLOR] uppercase pill label
"[CATEGORY TAG — e.g. 'KEY INGREDIENT' / 'THE SCIENCE']". Below: large bold
[BRAND COLOR or dark] serif or heavy sans-serif headline: "[INGREDIENT NAME]." —
just the ingredient name with a period, confident and clinical. Below headline: a
dominant close-up photorealistic image of [THE INGREDIENT in natural form], macro
shot, sharp focus, soft diffused studio lighting — ingredient fills approximately 40%
of the total frame. To the right of or below the ingredient image: three stacked fact
rows, each with a [BRAND COLOR] filled bullet or thin left-border line: Row 1: bold
"[FACT LABEL 1:]" followed by one sentence on what the ingredient is. Row 2: bold
"[FACT LABEL 2:]" followed by one sentence on what it does. Row 3: bold
"[FACT LABEL 3:]" followed by one sentence on sourcing, dose, or form superiority.
Below the fact rows: product at a slight angle, clean studio lighting, partial crop
acceptable. To the left of the product: a small circular trust badge
"[TRUST BADGE TEXT]" in [BRAND COLOR] with white text. Brand logo bottom right,
small. No stars, no reviews, no CTA button. [ASPECT RATIO] aspect ratio.
```

What this template demonstrates: educational / clean-label register (confident, clinical headline plus 3-row fact structure) as an explicit ad pattern that contrasts with both the iMessage realistic-screenshot pattern and the Scarcity urgency-mechanics pattern. The negative direction "No stars, no reviews, no CTA button" suppresses ad-pattern bleed into the clean-label register — without that suppression, GPT Image 2.0 tends to add review stars and a CTA by default, both of which break the educational frame.

---

## 6. Forward-pointers

When this satellite's workflow doesn't apply, route to:

- **General-purpose GPT Image 2.0 prompts** → [parent SKILL.md](SKILL.md). The three-format taxonomy (Format A JSON / Format B prose / Format C meta-prompt) covers everything that isn't ad-format recreation.
- **Marketing Studio video ad workflows** → [higgsfield-marketing-studio](../higgsfield-marketing-studio/SKILL.md). When the user wants a 4-15s ad video rather than a static image ad.
- **Brand-kit-aware DTC ad image generation (Higgsfield-native)** → [the Marketing Studio cross-surface-workflow.md](../higgsfield-marketing-studio/cross-surface-workflow.md) § 3 covers `ms_image` / "DTC Ads" — Higgsfield's native image-generation surface for ad work. When brand-kit consistency across many images matters more than the reference-ad-recreation pattern this satellite documents.
- **The broader cross-surface workflow for end-to-end ad campaigns** → [the Marketing Studio cross-surface-workflow.md](../higgsfield-marketing-studio/cross-surface-workflow.md) § 2 documents Adil's full four-surface recipe (GPT Image 2.0 → Soul Cinema → Nano Banana Pro → Marketing Studio) for end-to-end campaign production. The brand-identity reuse pattern there is the parallel to the brand-vs-structure separation rule documented in this satellite's § 4.

---

## 7. Source acknowledgment

Coverage in this satellite is translated from source material by Adil Aliyev — author of `static-ads.md` (sibling source to `gpt-image-2-director.md` translated into the parent SKILL.md). Source: `static-ads.md` (~20 KB, 316 lines).

### Per-claim translation calibration

Per the v3.7.13 author-signature calibration carried through v3.7.15 / v3.7.16:

- **Workflow shape (10-step sequential structure) is Adil's pedagogical scaffolding** — translated to our skill's voice and condensed where execution-layer assumptions don't carry over (the source's `./brands/` directory convention, `/brand` slash command, and helper scripts are documented as patterns the recipe expects, not as functional infrastructure our skill provides).
- **Production-knowledge claims adopted close to verbatim** — fractional coordinates, safe-zone rule, brand-vs-structure separation, wireframe intermediation. These are the highest-falsifiable content in the source corpus and translate cleanly without register-downgrade.
- **Brand-folder execution layer documented as workflow recipe, not as literal execution layer** — our skill does not ship `/brand` or the helper scripts (`generate-static-ad.py`, `generate-reformat.py`). The patterns are transferable to any execution environment; the specific tooling is environment-specific.

The safe-zone top/bottom-10% rule is adopted at full HARD-RULE volume — the only HARD-RULE volume claim in the source corpus — because the underlying premise (Instagram and TikTok's UI overlays consume the top/bottom ~10% of the frame) is verifiable surface fact about platform UI behavior, not craft opinion. The HARD-RULE volume is justified by the platform UI reality the rule responds to.

### Verification trail

Per-source disposition: [.planning/v3.7.16/PHASE-0-VERIFICATION.md](../../.planning/v3.7.16/PHASE-0-VERIFICATION.md) § VERIFY 0.2 (static-ads.md source read + disposition class TRANSLATE-WITH-VERIFICATION LOWEST-FRICTION SUB-CLASS).

Per-element translation rules: [.planning/v3.7.16/PHASE-1-INVENTORY.md](../../.planning/v3.7.16/PHASE-1-INVENTORY.md) § 1B-B (per-element ADOPT / DOWNGRADE table).

Parent sub-skill: [SKILL.md](SKILL.md) covers `gpt-image-2-director` source corpus translation per § 1B-A — read that for the general-purpose three-format prompt taxonomy that this satellite specializes for ad recreation.
