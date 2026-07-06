---
name: higgsfield-gpt-image-2
description: >
  Cross-surface satellite document for higgsfield-gpt-image-2. Covers the Automatic
  Product Reference Sheet workflow — turning one product image into a multi-view studio
  reference sheet (front/back/sides/top/macro-detail panels) for high-consistency image
  and video generation, plus the Automatic Prompt Creator meta-prompt that converts a
  set of product images into one identity-locked, product-specific generation prompt.
  Includes the verbatim GLOBAL IDENTITY LOCK copy/paste prompt, the prompt-conversion
  meta-prompt, and two worked examples (hat, golf dress). Best run with Nano Banana Pro,
  Nano Banana 2, or GPT Image 2.0. Consulted from parent SKILL.md when the user wants a
  product reference sheet, an identity-locked product prompt, or asset prep for static
  ads / Marketing Studio / Soul workflows.
user-invocable: false
metadata:
  tags: [higgsfield, gpt-image-2, reference-sheet, product-reference, identity-lock, nano-banana-pro, multi-view, asset-prep, workflow, satellite]
  version: 1.0.0
  updated: 2026-06-03
  parent: higgsfield
---

# Product Reference Sheet Workflow

A reference sheet is a single studio image that documents one real product
from many angles — front, back, sides, top, and macro close-ups of branding,
material, and construction. Feeding a reference sheet (instead of one
photo) into downstream generation gives the model far more identity geometry
to hold onto, which is what keeps a product consistent across image and video
generations.

This satellite covers two Higgsfield workflows that produce that asset:

1. **Automatic Product Reference Sheet** — one product image → a multi-view
   sheet, via a ready-to-paste prompt.
2. **Automatic Prompt Creator** — multiple product images → one
   product-specific, identity-locked prompt → final result.

Translated from Higgsfield's official Reference Workflow guide plus a
companion copy/paste prompt pack, per the v3.7.16 `static-ads-workflow.md`
satellite precedent. Best run with **Nano Banana Pro, Nano Banana 2, or GPT
Image 2.0** (see `../../image-models.md` for model selection).

---

## 1. Automatic Product Reference Sheet — the 3-step flow

Turn one product image into a professional reference sheet in three steps:

1. **Upload** a single clean product image.
2. **Paste the provided prompt** (the GLOBAL IDENTITY LOCK in § 2 below),
   keeping `@image1` pointed at the uploaded image.
3. **Generate** — the model returns a clinical multi-view studio sheet:
   front / back / sides / top / underside as relevant, plus macro close-ups
   of branding, key material, and a construction detail.

The whole point is *identity preservation, not redesign* — the output must
read as the same real physical product photographed in a studio, not a
re-imagined or vectorized version. One image in, a reusable
high-consistency generation asset out.

---

## 2. GLOBAL IDENTITY LOCK — paste-ready prompt

Works with any product. Keep the camera/capture and background blocks intact;
the model adapts the view list to the product type.

```text
Use @image1 as a strict photographic reference of a real product.

Create a high-resolution studio reference sheet of the EXACT SAME product
shown in @image1. This is not a redesign or reinterpretation. It must look
like the same real physical product was placed in a studio and photographed
from multiple angles.

GLOBAL IDENTITY LOCK (CRITICAL):
Preserve the exact real-world identity of the product from @image1, including
all product-specific characteristics that apply:
- identical overall shape, proportions, silhouette, and structure
- identical dimensions and construction logic
- identical material behavior, thickness, softness, rigidity, and finish
- identical seams, folds, edges, contours, stitching, joins, closures,
  fasteners, hardware, trim, and surface transitions
- identical color relationships and tonal balance
- identical wear, subtle imperfections, manufacturing irregularities, and
  real-world material variation
- identical product-specific features visible in @image1, whatever they may be

BRANDING / GRAPHICS / LABEL LOCK (CRITICAL):
If the product in @image1 includes any logo, text, label, print, patch, tag,
embossing, engraving, packaging graphics, or branding element, preserve it
EXACTLY as it appears:
- preserve exact typography
- preserve exact stroke weight, spacing, alignment, and placement
- preserve exact print, embroidery, emboss, stamp, engraving, or label
  appearance
- preserve slight real-world irregularities
Treat all branding and graphic elements as photographed physical parts of the
product, not as digitally recreated text or artwork.

REFERENCE SHEET LAYOUT:
Photograph the product as a clean multi-view studio reference sheet. Show the
most useful angles based on the product type, including: front, back, left
side, right side, top, bottom/underside where relevant, 3/4 angle if helpful,
macro close-up of the main branding/logo/label area, macro close-up of a key
material or texture area, macro close-up of an important construction detail,
and macro close-up of an important feature specific to the product.
If the product type requires a different angle set, adapt intelligently while
still keeping it a clean, clinical product reference sheet.

BACKGROUND + LIGHTING:
- solid light gray background (#DCDCDC)
- perfectly even studio lighting
- shadowless or near-shadowless presentation
- no gradients
- no reflections
- clean, neutral commercial studio setup

REALISM REQUIREMENTS:
- must look like real product photography, not CGI
- preserve micro surface texture and real material character
- preserve stitching, molding, printing, machining, or assembly
  irregularities where applicable
- preserve realistic edge detail and true product finish
- maintain real-world asymmetry where the physical object naturally has it

CAMERA / CAPTURE:
Canon EOS R5
RF 100mm f/2.8L Macro IS USM
f/8
ISO 100
true-to-life color profile
macro-level material detail
edge-to-edge sharpness

FINAL RESULT:
A clinical, ultra-realistic product reference sheet of the exact product in
@image1, preserving its real-world identity, materials, branding,
construction, and imperfections with professional studio accuracy.
```

**Identity-lock discipline:** if a product has no visible branding, do not
invent any. If a detail is not visible in the source, do not hallucinate it —
be precise about what is actually present.

---

## 3. Automatic Prompt Creator — meta-prompt

When you have multiple images of one product, this meta-prompt converts the
global template above into a tightly product-specific prompt. Paste it into
the LLM of your choice *along with the product images*; it outputs one final
generation prompt.

```text
You are a prompt-conversion assistant. Your job is to take the global
product-sheet prompt and rewrite it into a product-specific final prompt
based on the reference image(s) attached to the conversation.

Automatically account for however many reference images are provided. Label
them sequentially as @image1, @image2, @image3, and so on. Your rewritten
prompt must correctly reference all provided images.

Do NOT keep the prompt generic. Analyze the reference image(s) and identify
exactly what the product is, how it is constructed, what materials it uses,
how its branding is applied, what textures are visible, what small details
matter, and which product-specific close-ups and angles are needed. Then
rewrite the global prompt so it is fully tailored to that specific product
while preserving the same studio-reference-sheet purpose, realism standard,
and camera/capture specifications.

Analyze from the image(s): (1) product type; (2) overall identity and
structure — shape, silhouette, proportions, construction logic, parts,
closures/seams/joints/hardware; (3) material and surface qualities —
fabric/metal/plastic/leather/glass/etc., softness or rigidity, thickness,
sheen, grain, finish; (4) branding/graphics/typography/labels — logos,
printed/stitched/embossed/engraved text, patches, tags, color blocking,
stripe placement, exact relative placement, and HOW the branding physically
exists on the object; (5) real-world imperfections — wear, stitching/print
irregularities, slight asymmetry; (6) product-specific shot planning — which
views and macro close-ups matter most for THIS product.

Rules: preserve the same studio-sheet intent, realism level, and capture
specs. Keep the camera/lens package and the background/lighting treatment
exactly consistent unless the user changes them. Convert all generic
statements into specific statements that match the actual product. If the
product has branding, describe it as part of the identity lock. If it has no
visible branding, do not invent any. If a detail is not visible, do not
hallucinate it. The final prompt should read like a refined expert
image-generation prompt, not analysis notes.

Output ONLY the final rewritten prompt — no reasoning, no commentary, no
summary of changes, no multiple versions. One best final prompt.
```

---

## 4. Worked examples (verbatim production prompts)

### 4.1 — Hat reference sheet (single image)

```text
Use @image1 as a strict photographic reference of a real product.

Create a high-resolution studio reference sheet of the EXACT SAME white hat
from @image1. It must look like the same real hat was physically placed in a
studio and photographed from multiple angles.

IDENTITY LOCK (CRITICAL):
- identical hat shape, proportions, and structure
- identical front panel curvature and foam structure
- identical brim curvature, thickness, and stitching rows
- identical navy rope placement and thickness across the front
- identical panel seams and crown construction
- identical perforation pattern on the side panels (match exactly)
- identical wear, subtle fabric variation, and real-world imperfections

LOGO LOCK (CRITICAL):
Use the logo EXACTLY as it exists on the hat in @image1 — do not recreate
typography, re-type text, or "clean up" the logo. Preserve exact stroke
weight, spacing, alignment, and slight print/embroidery irregularities.
Treat the logo as a photographed element printed/stitched on fabric.

REFERENCE SHEET LAYOUT: front, back, left side, right side, top, underside
brim, macro close-up of logo, macro close-up of rope detail, macro close-up
of perforation texture, macro close-up of brim stitching.

BACKGROUND + LIGHTING: solid light gray (#DCDCDC), perfectly even studio
lighting, no shadows, no gradients, no reflections.

CAMERA / CAPTURE: Canon EOS R5, RF 100mm f/2.8L Macro IS USM, f/8, ISO 100,
true-to-life color, macro-level textile detail, edge-to-edge sharpness.

RESTRICTIONS: no redesign, no stylization, no brand reinterpretation, no
added elements, no smoothing or beautification.
```

### 4.2 — Apparel reference sheet (two reference roles)

Uses `<<<image_1>>>` as the garment identity reference and `<<<image_2>>>` as
the logo identity/placement reference:

```text
Use <<<image_1>>> as the strict garment identity reference. Use
<<<image_2>>> as the strict logo identity and placement reference.

This is a LOCKED apparel reference sheet. The garment and logo must be
identical to the references with zero redesign, reinterpretation, or
stylistic variation.

GARMENT LOCK: reproduce the exact same women's sleeveless golf dress from
<<<image_1>>> — same white athletic fabric tone and material response, navy
collar shape and thickness, V-placket geometry and depth, armhole trim,
double navy side stripe placement/spacing/taper, skirt length/flare/
silhouette, seam lines and stitch placement, fit proportions.

LOGO LOCK (CRITICAL): use the exact logo from <<<image_2>>> only — same
letterforms, overlap relationship, spacing, weight, proportions, embroidered
thread color, exact position on left chest, and scale. Do NOT recreate,
restyle, vectorize, or reinterpret the logo.

EMBROIDERY REALISM: the logo must appear physically stitched — raised thread
structure, tight embroidery density, visible thread direction, micro
shadowing, slight fabric compression, subtle curvature following the chest
contour.

REFERENCE SHEET LAYOUT on flat light gray (#DCDCDC), even omnidirectional
lighting, no shadows/gradients/reflections: full front (centered), full back,
left profile, right profile, close-up of chest logo, close-up of side-stripe
construction.

MODEL / POSE: neutral mannequin-style stance, arms relaxed, no fashion
posing.

PHOTOGRAPHY SPEC: Canon EOS R5, RF 85mm f/2 Macro IS STM, f/8, ISO 100,
true-to-life color science, no cinematic grading, no stylization LUTs.

RESTRICTIONS: no additional logos, no alternate branding, no text overlays,
no environment, no props, no lighting effects, no beauty retouching.
```

---

## 5. Views the video will need (front / side / back — and the bottom)

The REFERENCE SHEET LAYOUT block above says "bottom/underside where relevant."
The Seedance-4K film tutorial shows exactly when it's relevant, and it is not
optional there [DEMO — Seedance-4K film tutorial, 2026-07]:

- **Front / side / back is the working minimum** for any prop the camera will
  move around — the tutorial's TV-remote sheet is three identical remotes on
  one baseline (front face, true side profile, back shell).
- **Add a BOTTOM / undercarriage view whenever the object will be flipped,
  tumbled, or rolled in the video.** The tutorial's snow-truck sheet is a 2×2
  grid — FRONT / SIDE / REAR / BOTTOM-UNDERCARRIAGE — built specifically
  because the truck gets flipped onto its roof in the scene. A model cannot
  invent an underside it has never seen; it will hallucinate one mid-tumble.

Plan the views from the shot list, not from the object: whatever face of the
prop the video will expose, the sheet must have already photographed.

On background: the GLOBAL IDENTITY LOCK's solid light gray (`#DCDCDC`) sits
inside the tutorial's tested neutral-grey rule (light-to-medium grey beats
white or black; `#7f7f7f` for creature sheets) — the canonical statement lives
in `../../templates/ad-asset-prep.md` § Design for win rate.

If a GPT Image 2 sheet comes back reading flat or 2D, rerun the **same prompt,
unchanged, in Nano Banana Pro** before rewriting anything — the tutorial
recovered its remote sheet exactly this way. The full sheet-model ladder
(GPT Image 2 at 4K default → Nano Banana Pro on flatness → Soul Cinema for
locations/characters-from-scratch) is in `../../templates/ad-asset-prep.md`
§ Which model makes the sheet.

---

## 6. Red-arrow annotation — aim the actor at the right control

A fix for a stubborn failure mode: the video actor keeps interacting with the
**wrong part of the prop** — pressing the wrong button, gripping the wrong
handle — no matter how the action is re-phrased
[DEMO — Seedance-4K film tutorial, 2026-07].

The trick encodes the instruction into the reference image itself:

1. **Draw a red arrow on the sheet image** pointing at the exact control or
   region the action targets (any image editor; the arrow becomes part of the
   reference).
2. **Have the prompt read the arrow back in words.** Tutorial verbatim, from
   the remote-press scene: *"The reference's red arrow points precisely to the
   CH-UP chevron (˄) directly above the 'CH' label"* — and the ACTION block
   then places the thumb "where the red arrow points."

The annotated sheet and the prompt now agree on one unambiguous target, so the
model stops improvising the contact point. Use a copy of the sheet for this —
keep the clean, arrow-free sheet as the identity reference for every shot that
doesn't need the pointer.

---

## 7. Where reference sheets feed downstream

The reference sheet is a reusable identity asset, not an end product. Feed it
into:

- **Static ads** — as the product reference in `static-ads-workflow.md`
  (Mode A reference swap).
- **Marketing Studio video** — register it as a product so generations hold
  product fidelity (see `../higgsfield-marketing-studio/SKILL.md` § 6).
- **Soul / character work** — the same identity-lock discipline applies to
  character turnaround sheets (see `../higgsfield-soul/SKILL.md`
  § Character Sheet Creation).

## 8. Source acknowledgment

Translated from Higgsfield's official **Product References & Video
References** reference-workflow guide (Automatic Product Reference Sheet +
Automatic Prompt Creator) plus a companion copy/paste prompt pack. The
GLOBAL IDENTITY LOCK prompt, the Automatic Prompt Creator meta-prompt, and
the two worked examples are preserved close to verbatim as reusable
copy/paste assets; surrounding guidance re-expressed in house voice. Model
compatibility (Nano Banana Pro / Nano Banana 2 / GPT Image 2.0) stated per
the source. §§ 5–6 (view coverage for motion, red-arrow annotation) are
tutorial-demonstrated conventions from the Seedance-4K film breakdown
[DEMO — Seedance-4K film tutorial, 2026-07].
