# Reference Sheet Types — Motion / Camera, Outfit / Material, Palette / Mood, Product

Companion reference for `../SKILL.md` § Reference Sheet Types — Beyond Characters and
Locations. Moved out of the SKILL.md body verbatim in v3.36.0 so the main file stays
readable end-to-end in one pass; the principle ("a sheet locks one property; it pays
for itself at three or more shots") and the family table stay in `../SKILL.md`.
Relative paths below resolve from this `references/` folder.

### Motion / Camera Sheet

A short reference clip — 3–10 seconds is plenty — that captures a camera path
or motion rhythm you want repeated across multiple shots. The sheet locks the
movement signature, not the content of any single shot. Treat it as a
project-wide style anchor pulled into a generation as an @Video reference, the
way a DP would carry a "look" across an entire film.

Use cases: a music video where the same dolly-in arc punctuates every chorus;
a fight sequence where a signature whip-pan recurs at every climax beat; a
brand piece where every product shot starts on the same slow orbit. Distinct
from a Kling 3.0 Motion Control reference clip — that drives a single
generation's motion transfer. The Motion / Camera Sheet is reusable across the
whole project.

### Outfit / Material Sheet

Dedicated wardrobe reference. Locks fabric texture, color values, garment fit,
fastenings, and how the material moves and folds. Generate it once with even
lighting and multiple angles, then reuse it any time the costume needs to read
identically across cuts.

Use cases: a hero costume that appears across 12 scenes; a specific jacket that
must look the same in close-up and wide shot; a uniform that recurs across an
ensemble cast. The outfit sheet is **not** the same as a character sheet — the
character sheet locks identity (face, build, hair, distinguishing marks), while
the outfit sheet locks what the character is wearing AND how that wardrobe
behaves in motion. Build both when you have a hero costume on a hero character.

**The piano test — wardrobe complexity has a generation cost.** Every detail of
wardrobe complexity — buttons, ties, jewelry, scarves, layered garments,
intricate prints, fastening hardware — costs the model rendering budget. The
piano test (adapted from the Mr. Core methodology) is the rule: if a wardrobe
element is as visually demanding for the model to render as a piano in the
frame, the model will spend its budget rendering that element instead of the
action. Strip the wardrobe to the simplest silhouette that still reads as the
character. A trench coat reads as a trench coat without the buttons rendering
correctly. A uniform reads as a uniform without the rank insignia drifting
across frames. Design the costume's *signature* — the silhouette and one
identifying feature — and let the rest go simple. Hero costumes that must
render under close-up scrutiny earn their complexity; background costumes do
not.

### Palette / Mood Sheet

A color and tonal anchor for the project. Lock the visual mood across an entire
sequence: shadow density, key/fill ratio, saturation level, signature accent
colors, grade direction. Use a single curated still or a small grid of grade
references — the goal is to give every subsequent generation a consistent
palette to reach for.

Use cases: a noir piece where every scene shares the same shadow density and
warm-amber-on-cool-blue grade; a cyberpunk sequence where neon-to-base-light
ratio stays fixed across 15 cuts; a brand campaign where a signature accent
color appears in every shot regardless of subject. Pairs naturally with the
Soul Hex color system and curated moodboards in
`../../higgsfield-moodboard/SKILL.md`.

### Product Reference Sheet

When a product reappears across multiple shots — a hero SKU in a brand
campaign, a recurring prop in a narrative piece, a single item shot from a
dozen angles for ecommerce — give it the same asset-first treatment as a
character or location. Generate the product once as a multi-view reference
sheet, then call it in subsequent shots. Re-describing the product inside
each scene prompt is the root cause of "every shot reinterprets the
product": branding shifts, materials drift, geometry rearranges, and the
hero stops feeling like a single object.

The Product Reference Sheet uses a 7-part prompt scaffold. Each part fixes
one axis of the product's identity. Build the parts in order — the locks
come first, then composition, then surface treatment, then capture
parameters, then negative space.

**1. Identity Lock** — what the product *is*. Geometry, scale, color
values, defining proportions, distinguishing physical features. The same
discipline as a character sheet's identity block, applied to an object.

**2. Branding Lock** — placement, scale, color, and treatment of every
brand element on the product: logos, wordmarks, tags, stitched labels,
embossed marks. Specify position relative to product geometry (centered
front panel, left sleeve, lower right corner) and rendering style
(embroidered, screen-printed, embossed, foil-stamped).

**3. Layout** — the multi-view grid. Standard Product Reference Sheet
layout covers eight orthographic views plus macro close-ups:

| View | What it locks |
|------|---------------|
| Front | Primary read — branding placement, overall silhouette |
| Back | Reverse details, secondary branding, construction seams |
| Left side | Profile geometry, depth on the left |
| Right side | Profile geometry, depth on the right |
| Top | Top-down silhouette, crown / lid / opening geometry |
| Bottom | Underside details, base / sole / footprint |
| 3-quarter | Hero angle — combines front and side reads |
| Macro close-ups | Branding detail / material weave / construction join / any product-specific detail that earns its own frame |

Eight views vs. the Five-View Location Sheet's five — products need more
orthographic angles than locations because the camera is closer and the
geometry is the subject, not the environment. Macro close-ups are the
product analogue of the location sheet's close-up environmental-details
view, scaled up to one per product-specific concern.

**4. Background** — `#DCDCDC` light gray, shadowless lighting, no
gradients, no reflections. Studio product-photo convention: the
background contributes zero visual information so the product reads as
the only subject. Specify all four constraints — `#DCDCDC` alone without
the shadowless + no-gradients + no-reflections trio still leaves the
model room to add atmospheric noise. `#DCDCDC` is one shade inside the repo's
grey law (light-to-mid neutral grey, one pinned hex per project), stated once
in `../../../templates/ad-asset-prep.md` § Design for win rate.

**5. Realism** — the Material Realism block. Reusable template populated
per material; six axes that together make a surface read tactile and
physically grounded rather than rendered-flat:

- **Raised structure** — what stands proud of the base surface and by
  how much
- **Tight density** — how packed the surface elements are per unit area
- **Visible direction** — the directionality of grain, weave, thread, or
  flow across the surface
- **Micro shadowing** — the small shadows cast by raised elements into
  the surface valleys
- **Surface compression following form** — how the material deforms where
  it meets seams, edges, or attached elements
- **Curvature integration** — how the surface and its texture follow the
  product's overall geometry rather than sitting on top of it

Populate the six axes with material-specific vocabulary. Embroidery,
leather, knit, satin, brushed metal, and suede each have their own value
set; the six axes stay constant.

**6. Camera** — default product reference package: **Canon EOS R5 +
RF 100mm f/2.8L Macro IS USM, f/8, ISO 100**. The 100mm macro lens at
f/8 holds the whole product in sharp focus from front-most edge to
back-most edge across all eight views; ISO 100 keeps sensor noise out
of the gray background. Substitute only when a specific shot needs a
different read — e.g. shallow depth of field for a hero brand-detail
macro (f/4), or a wider focal length for an oversized product
(RF 50mm).

**7. Restrictions** — the content-fidelity block. The Product Reference
Sheet's job is to capture the actual product, not a stylized or
reinterpreted version. This block tells the model what NOT to do with
the source: don't redesign, don't reinterpret branding, don't beautify,
don't add styling. Frame composition discipline (no environmental
context, no props) is enforced here as part of the same content-fidelity
intent; the background/lighting constraints from Section 4 handle their
own scope and don't repeat here.

- No redesign
- No stylization
- No brand reinterpretation
- No added elements
- No alternate branding
- No additional logos
- No text overlays
- No props
- No environment
- No lighting effects
- No smoothing or beautification
- No beauty retouching

The Product Reference Sheet locks the product; narrative use of the
product happens in downstream scene prompts that call this sheet as a
reference.

#### Hat — Worked Example

A black baseball cap with an embroidered logo, set up as a Product
Reference Sheet:

- **Identity Lock** — six-panel baseball cap, black cotton twill, curved
  brim, adjustable strap closure, pre-curved crown, eyelets on each
  panel
- **Branding Lock** — embroidered wordmark centered on the front panel,
  white thread, 4cm wide, positioned 3cm above the brim seam
- **Layout** — front / back / left / right / top / bottom / 3-quarter,
  plus macro close-ups of the embroidered wordmark, the panel seams,
  and the strap closure
- **Background** — `#DCDCDC` light gray, shadowless lighting, no
  gradients, no reflections
- **Realism (Material Realism populated for embroidery):**
  - Raised structure — raised thread structure, thread sitting proud of
    the cotton twill base
  - Tight density — tight stitch density across each letterform
  - Visible direction — visible thread direction following each letter's
    stroke path
  - Micro shadowing — micro shadowing in the stitch valleys between
    thread rows
  - Surface compression following form — fabric compression around the
    stitching where the thread tension pulls the twill in
  - Curvature integration — embroidery curvature following the
    pre-curved front panel rather than sitting flat
- **Camera** — Canon EOS R5, RF 100mm f/2.8L Macro IS USM, f/8, ISO 100
- **Restrictions** — no redesign, no stylization, no brand
  reinterpretation, no added elements, no smoothing or beautification

For leather / knit / satin / brushed metal / suede hero products, swap
the Material Realism block's embroidery vocabulary for the material's
own value set on each of the six axes — the scaffold is identical.
