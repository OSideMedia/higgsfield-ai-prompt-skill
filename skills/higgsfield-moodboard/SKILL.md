---
name: higgsfield-moodboard
description: >
  Use when the user asks about Moodboard, building a moodboard from reference images,
  curated moodboard presets, Soul Hex color transfer, applying a visual style direction
  to generations, or named moodboard styles like Y2K studio, Warm ambient, Theatrical
  light, Swag era, Flash editorial, Street photography, Asian nostalgia, Retro BW,
  Surreal solarization, etc.
user-invocable: true
metadata:
  tags: [higgsfield, moodboard, style, reference, soul-hex, color, presets, Y2K, editorial]
  version: 3.0.0
  updated: 2026-04-06
  parent: higgsfield
---

# Higgsfield Moodboard

## What Moodboard Does

Moodboard translates a collection of visual references into a **unified style direction**
that can be applied to any generation. Instead of describing a feeling in text and hoping
the model interprets it correctly, you show the platform exactly what you want.

**Location:** Moodboard tab (marked "New" in nav) → higgsfield.ai/moodboard

**Two tabs inside Moodboard:**
- **Curated** — Higgsfield's own named preset moodboards, ready to use
- **My Moodboards** — your custom moodboards built from uploaded references

---

## Curated Moodboard Presets

Named presets built by Higgsfield — apply any of these immediately without uploading
reference images. Each represents a complete visual world.

| Preset | Visual Character | Best for |
|--------|-----------------|---------|
| **General** | Neutral — no strong stylistic bias | Default when unsure, versatile |
| **Warm ambient** | Warm, soft, gently lit — cozy and lived-in | Lifestyle, home, intimate portrait |
| **Y2K studio** | Hypercolor studio backdrop, fairy wings, maximalist | Y2K aesthetic, fashion, fantasy editorial |
| **Swag era** | Early 2000s hip-hop and streetwear energy | Urban fashion, music culture content |
| **Theatrical light** | Dramatic stage lighting, strong contrast, silhouette | Artistic portrait, performance, dark editorial |
| **Y2K street** | Union Jack tees, street photography, 2000s pop culture | Street style, youth culture, nostalgia |
| **Flash editorial** | On-camera flash, oversaturated, candid — Cobrasnake era | Party, raw editorial, documentary fashion |
| **Old smartphone** | Low resolution, slightly washed, nostalgic phone camera | Authentic, lo-fi, personal content |
| **Street photography** | Urban candid, natural light, documentary | Street style, city life, authentic scenes |
| **Asian nostalgia** | Japanese/Korean city streetwear, warm neon, youth culture | Asian fashion, Tokyo/Seoul aesthetic |
| **Retro BW** | Black and white, classic tones, timeless | Artistic portrait, formal editorial, classic fashion |
| **Surreal solarization** | Otherworldly color shifts, solarization effect | Conceptual/avant-garde, fashion art |

**How to apply a curated preset:**
1. Go to Moodboard tab
2. Select **Curated**
3. Click any preset
4. It becomes available in My Moodboards or applies directly to generation

---

## Building a Custom Moodboard

### Upload Requirements

**Recommended:** 20+ photos, one cohesive style
**Avoid:** Mixed styles, inconsistent quality

**Two upload options in the Moodboard builder:**
- **Upload images** — upload from your device
- **Upload from assets** — pull from your existing Higgsfield generations/assets

**What "one cohesive style" means:**
All reference images should share the same visual world — similar lighting quality,
color temperature, tone, and aesthetic. If half your references are dark and moody
and half are bright and airy, the moodboard gets confused and produces a muddled output.

**Good reference set (cohesive):** Film stills from the same movie, a photographer's
series, a curated Pinterest board with a single strong aesthetic, a fashion brand's
lookbook.

**Bad reference set (mixed):** Random images from different genres, mixing a sunset
photo with a dark studio portrait with a colorful illustration.

### Building the Moodboard

1. Click **Build your moodboard ✦** (yellow button at top)
2. Upload 20+ reference images via "Upload images" or "Upload from assets"
3. Higgsfield analyzes the visual properties across all references
4. Synthesizes dominant: colors, tonal values, lighting character, stylistic patterns
5. Creates a named moodboard saved under **My Moodboards**

### Applying to Generation

Once built, your moodboard appears in:
- Soul 2.0 → Moodboard selector in the prompt bar
- Any generation interface that supports moodboard input

The moodboard acts as a **style layer** applied on top of your text prompt —
you describe the scene, the moodboard handles the look.

---

## Soul Hex — Color Transfer

Soul Hex is Moodboard's dedicated color feature. It extracts and transfers the exact
color signature from a reference image.

**Location:** Soul 2.0 prompt bar → **Color Transfer** button

### Named Color Palettes

Pre-built palettes available directly in Color Transfer:

| Palette | Visual Character |
|---------|----------------|
| **Film colors** | Natural, organic, slightly desaturated film stock |
| **Lime Jam** | Cool greens, fresh tones, nature-adjacent |
| **Candy pink** | Warm pinks, peachy highlights |
| **Nostalgic blue** | Desaturated blues, faded, melancholic |
| **Soft palette** | Muted, airy, minimal contrast |
| **Black gloss** | High contrast, deep blacks, graphic |

### Custom Color Reference Upload

1. Click **Upload & Create ✦** in the Soul Hex section
2. Upload any reference image with the color world you want
3. Soul Hex extracts the color palette automatically — shows hex swatches
4. Apply to generations

**Good color references to upload:**
- Film still from a movie with the color grade you want
- Fashion editorial with a strong color world
- Your brand's visual assets to match brand colors
- Any image where the color palette is the dominant appeal

---

## Moodboard + Soul ID: The Power Combination

| What it controls | Tool |
|-----------------|------|
| **Who** — face and character consistency | Soul ID |
| **Color world** — palette and grade | Color Transfer / Soul Hex |
| **Overall aesthetic** — lighting, tone, visual language | Moodboard |
| **Specific visual treatment** — preset style | Soul 2.0 Style Preset |

**Workflow for a consistent content series:**

```
Step 1: Create Soul ID character (20+ photos, Character tab)
Step 2: Build Moodboard from style references (20+ cohesive images)
Step 3: Set Color Transfer palette (named or custom upload)
Step 4: Every generation uses:
         → Character slot: Soul ID active
         → Style: appropriate preset
         → Color Transfer: consistent palette
         → Moodboard: your custom moodboard active
Step 5: Only the scene description changes post to post
```

**Per-post prompt template (with all consistency tools active):**
```
[Soul ID character] is [action] at [specific location].
[One unique visual detail for this post.]
Camera: [movement]. Aspect: 9:16.
[No style description needed — moodboard + preset handle it.]
```

---

## Moodboard as a Prompt Modifier

When you want to write the moodboard's style into the prompt directly
(rather than using the UI), use this structure:

```
[MOODBOARD: Project Name]
Color palette: [2–3 dominant colors]
Tone: [warm/cool + emotional register]
Film look: [sensor/grain if applicable]
Lighting character: [quality of light]
Cultural reference: [specific aesthetic if using a curated preset]
```

**Example — Y2K Studio:**
```
[MOODBOARD: Summer Campaign]
Color palette: electric blue backdrop, metallic silver, iridescent highlights
Tone: hyper-energized, maximalist, unserious
Film look: early 2000s digital — slightly blown highlights, vivid saturation
Lighting character: hard studio flash, colorful gels
Cultural reference: Y2K maximalism, early internet fashion
```

**Example — Theatrical Light:**
```
[MOODBOARD: Dark Portrait Series]
Color palette: deep black, single amber key light, deep shadow fill
Tone: mysterious, composed, high-drama
Film look: medium format digital, razor-sharp
Lighting character: single hard source, theatrical — all else falls to black
Cultural reference: stage photography, Helmut Newton editorial
```

---

## Related skills
- `higgsfield-soul` — Soul ID character consistency (combine with Moodboard for full visual lock)
- `higgsfield-style` — Visual styles and color grades
- `higgsfield-mixed-media` — Artistic preset overlays
- `higgsfield-pipeline` — Pipeline B uses Moodboard as a core stage
- `templates/` — Annotated genre templates demonstrating style direction
