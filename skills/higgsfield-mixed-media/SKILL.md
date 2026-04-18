---
name: higgsfield-mixed-media
description: >
  Use when the user asks about Mixed Media, wants to apply artistic preset styles
  to an image (Noir, Sketch, Paper, Canvas, Particles, Neon, etc.), combine
  multiple artistic treatments, or create stylized non-photorealistic outputs.
user-invocable: true
metadata:
  tags: [higgsfield, mixed-media, presets, artistic, noir, sketch, particles, style]
  version: 3.0.0
  updated: 2026-04-06
  parent: higgsfield
---

# Higgsfield Mixed Media

## What Is Mixed Media?

Mixed Media is Higgsfield's artistic style overlay system — a library of curated
visual presets that transform your images and videos into stylized, non-photorealistic
art directions. Each preset is a complete aesthetic treatment, not just a filter.

**Location:** higgsfield.ai/mixed-media-intro

**Input:** Any image or video  
**Output:** Same content rendered through the chosen artistic style  
**Key difference from styles:** Mixed Media is about *artistic transformation*, 
not cinematic grading. You're moving from photo to art, not adjusting color grade.

---

## The Full Mixed Media Preset Library

### Textural / Surface Presets
| Preset | Look | Best for |
|--------|------|----------|
| **Sketch** | Hand-drawn pencil sketch, line weight variation | Concept art, storyboard, editorial |
| **Canvas** | Oil paint on canvas texture, brushwork visible | Fine art, dramatic portraiture |
| **Paper** | Subject looks cut and placed on paper | Collage, graphic, minimal |
| **Akrill** | Acrylic paint — thick, textured, vivid | Pop art, expressive portraiture |
| **Hand Paint** | Loose gestural watercolor brushwork | Soft, artistic, romantic |
| **Paint App** | Digital painting — smooth, stylized | Editorial, illustration |
| **Marble** | Subject rendered in marble texture | Sculpture aesthetic, luxury |
| **Origami** | Subject folded into paper geometry | Minimal, Japanese aesthetic |

### Light & Atmosphere
| Preset | Look | Best for |
|--------|------|----------|
| **Noir** | High-contrast black and white, deep shadows | Crime, drama, editorial |
| **Overexposed** | Blown highlights, washed out, dreamlike | Fashion, ethereal, editorial |
| **Ultraviolet** | UV-reactive palette, neon on dark | Club, night, music |
| **Glow Trace** | Luminous trails, subject leaves light path | Dance, movement art |
| **Random Glow** | Unpredictable glowing particles and light | Fantasy, magical, abstract |
| **Northern Lights** | Aurora borealis palette and flow | Nature, mystical, atmospheric |
| **Neon** | Vivid neon outlines on dark background | Cyberpunk, signage, night |
| **Cold Vision** | Ice-blue, clinical, cold atmospheric | Sci-fi, thriller, dystopian |
| **Burning Sunset** | Deep orange and crimson warmth | Drama, epic, emotional |
| **Innerlight** | Warm glow emanating from within subject | Spiritual, warm, emotional |

### Geometric & Digital
| Preset | Look | Best for |
|--------|------|----------|
| **Particles** | Subject dissolves into floating particles | Sci-fi, abstract, ethereal |
| **Point Cloud** | 3D point cloud representation | Technical, sci-fi, abstract |
| **Wireframe** | Geometric wireframe overlay | Tech, architectural, design |
| **Polygon** | Subject fragmented into flat polygons | Graphic, modern, digital art |
| **Fragments** | Subject broken into scattered pieces | Abstract, dramatic, impactful |
| **Multiverse** | Fractured parallel reality layers | Sci-fi, surreal, conceptual |
| **Collage** | Subject reassembled as cut-paper collage | Editorial, zine, artistic |
| **Comic** | Classic comic book halftone + lines | Pop art, superhero, nostalgia |
| **Flash Comic** | Modern bright comic style | Action, energetic, bold |
| **Pixel Game** | 8-bit retro pixelated aesthetic | Gaming, nostalgic, fun |
| **3D Rotation** | Subject appears as 3D rotating object | Product, logo, tech |

### Organic & Elemental
| Preset | Look | Best for |
|--------|------|----------|
| **Bubbles** | Transparent soap bubbles fill scene | Dreamy, playful, ethereal |
| **Ocean** | Underwater refraction and caustic light | Aquatic, dreamy, calm |
| **Lava** | Molten rock texture and glow | Dramatic, volcanic, intense |
| **Toxic** | Neon-green toxic atmosphere | Horror, sci-fi, danger |
| **Acid** | Psychedelic acid-wash color distortion | 1960s, surreal, experimental |
| **LSD** | Strong psychedelic visual distortion | Abstract, experimental |
| **Cannabis** | Soft dreamy haze and warmth | Chill, atmospheric, mellow |
| **Sand Worm** | Desert sand texture and movement | Sci-fi, epic, textural |

### Vintage & Film
| Preset | Look | Best for |
|--------|------|----------|
| **Vintage** | Aged, faded, yellowed film stock | Nostalgic, retro, warm |
| **VHS** | Scanlines, color bleed, static | 80s/90s, horror, retro |
| **J-Magazine** | Japanese fashion magazine aesthetic | Editorial, street, stylized |
| **60s Cafe** | Mid-century modern warm palette | Retro, lifestyle, warm |
| **Renaissance** | Classical painting light and composition | Fine art, portrait, dramatic |

### Social / Trend
| Preset | Look | Best for |
|--------|------|----------|
| **Two Color** | Bold two-tone duotone treatment | Graphic, poster, editorial |
| **Palette** | Restricted color palette, graphic | Illustration, brand, poster |
| **Modern** | Clean contemporary minimal style | Commercial, brand, lifestyle |
| **Windows** | Windows/panes frame the subject | Architectural, mystery, framing |
| **Magazine** | High-gloss editorial magazine spread | Fashion, commercial, portrait |
| **Tracking** | Motion tracking lines/paths visible | Sports, movement, tech |

### Surreal / Dark
| Preset | Look | Best for |
|--------|------|----------|
| **Broken Mirror** | Subject reflected in shattered fragments | Drama, psychological, horror |
| **Glitch** | Digital glitch artifacts, corruption | Cyberpunk, horror, avant-garde |
| **Melting Doodle** | Subject melts into doodle strokes | Surreal, fun, artistic |
| **Brick Cube** | Subject rendered as 3D brick structure | Abstract, architectural |

---

## How to Use Mixed Media in Prompts

Mixed Media presets are applied **on top of** your base generation, so your prompt
describes the scene and you specify the Mixed Media treatment separately.

**Standard application:**
```
[Scene description as normal prompt.]
Mixed Media preset: [Preset Name]
```

**Example:**
```
A woman in a red coat stands alone on a cobblestone bridge in winter rain.
Camera: Dolly In toward her face.
Style: Cinematic, cold tones, 16:9.
Mixed Media preset: Noir
```

**Combining base style + Mixed Media treatment:**
```
A fashion model in structured black tailoring, direct gaze to camera.
Style: High-contrast editorial. Studio white background.
Mixed Media preset: Two Color — black and vermillion.
```

---

## Stacking Presets (Layer Mixed Media)

Higgsfield allows stacking multiple Mixed Media presets via the **Layer Mixed Media**
feature — shown as the first item in the community gallery.

**What it does:** Applies two presets simultaneously, blending their treatments.

**Effective combinations:**
| Stack | Combined effect |
|-------|----------------|
| Sketch + Particles | Drawing dissolving into dust |
| Noir + Broken Mirror | Psychological thriller fragment |
| Neon + Glitch | Cyberpunk disruption |
| Canvas + Vintage | Aged oil painting aesthetic |
| Wireframe + Cold Vision | Sci-fi diagnostic overlay |
| Watercolor + Overexposed | Soft bleached painterly |

**Prompt phrase for stacking:**
```
Mixed Media presets: [Preset A] + [Preset B] (layered)
```

---

## Mixed Media vs Visual Styles

| Feature | When to use |
|---------|-------------|
| **Visual Styles** (Cinematic/VHS/etc.) | Cinematic grading — realistic film looks, color grades. Staying in photorealistic territory. |
| **Mixed Media** | Artistic transformation — moving to illustration, painting, abstract, or non-photorealistic territory. |

They are **not mutually exclusive** — you can specify a base visual style AND a
Mixed Media treatment in the same prompt for layered results.

---

## Mixed Media for Social Content

Mixed Media presets are particularly effective for creating **series-ready social content**
where visual consistency comes from the preset rather than a complex Moodboard setup.

**One preset → entire series:**
```
Post 1: [Street photography scene]. Mixed Media: J-Magazine
Post 2: [Portrait scene]. Mixed Media: J-Magazine  
Post 3: [Architecture scene]. Mixed Media: J-Magazine
```

Result: Diverse content, unified by a consistent artistic treatment.

---

> **Negative constraints:** For texture/lighting artifacts when using Mixed Media overlays,
> see `../shared/negative-constraints.md` — Texture/Lighting Artifacts section.

---

## Related skills
- `higgsfield-style` — Cinematic styles (photorealistic territory; Mixed Media is artistic territory)
- `higgsfield-motion` — Motion presets (different from Mixed Media presets)
- `higgsfield-moodboard` — Moodboard for project-level style consistency
- `templates/` — Annotated genre templates
