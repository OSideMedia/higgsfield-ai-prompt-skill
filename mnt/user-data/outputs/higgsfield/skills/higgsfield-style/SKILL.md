---
name: higgsfield-style
description: >
  Use when the user asks about visual styles, aesthetics, color grades, film looks,
  or how to set the tone and atmosphere of a Higgsfield generation.
user-invocable: true
metadata:
  tags: [higgsfield, style, VHS, cinematic, anamorphic, color, aesthetic]
  version: 3.0.0
  updated: 2026-04-06
  parent: higgsfield
---

# Higgsfield Visual Styles

## Core Platform Styles

These five styles are Higgsfield's named presets. Reference them by exact name.

### Cinematic
**Look:** Polished, high-contrast, vivid colors, balanced exposure — modern blockbuster
**Best for:** Drama, action, narrative films, commercials, any professional content
**Color tendency:** Rich, saturated, clean
**Prompt phrase:** "Style: Cinematic"
**Pair with:** Kling 2.6/3.0, Sora 2, Dolly In, Arc, Crane Up

```
Example: A detective walks through a night market.
Style: Cinematic. Cold blue shadows, warm amber market stall light.
Shallow depth of field. 16:9.
```

---

### VHS
**Look:** Retro videotape grain, color bleed, slight scanlines, analog imperfection
**Best for:** 80s/90s nostalgia, horror, thriller, retro music videos, flashbacks
**Color tendency:** Slightly washed out, warm yellows and reds, low contrast
**Prompt phrase:** "Style: VHS"
**Pair with:** Handheld camera, Wan 2.5, any horror preset

```
Example: Teenagers at a house party in 1987.
Style: VHS. Warm, grainy, slightly overexposed. 4:3 ratio.
```

---

### Super 8MM
**Look:** Warm film grain, soft vignette, muted colors, home-movie feel
**Best for:** Personal stories, romance, nostalgia, indie films, family moments
**Color tendency:** Warm, golden, slightly faded
**Prompt phrase:** "Style: Super 8MM"
**Pair with:** Handheld, natural light descriptions, intimate scenes

```
Example: A couple dancing in a sunlit backyard in the 1970s.
Style: Super 8MM. Warm grain, soft vignette edges. 4:3.
```

---

### Anamorphic
**Look:** Ultra-wide aspect ratio (2.35:1), horizontal lens flares, slight barrel distortion,
epic scale — classic Hollywood widescreen
**Best for:** Action, epic fantasy, war films, sweeping landscapes, high drama
**Color tendency:** High contrast, deep blacks, rich highlights
**Prompt phrase:** "Style: Anamorphic" or "Style: Anamorphic, 2.35:1 widescreen"
**Pair with:** Crane Up, 360 Orbit, Super Dolly Out, Sora 2

```
Example: An army marches across a frozen plain at dawn.
Style: Anamorphic, 2.35:1. Deep blue-grey tones. Lens flare on the rising sun.
```

---

### Abstract
**Look:** Non-representational, surreal color schemes, unconventional shapes, artistic
**Best for:** Music videos, conceptual art, dream sequences, experimental content
**Color tendency:** Vivid, unexpected, driven by concept not realism
**Prompt phrase:** "Style: Abstract"
**Pair with:** Wan 2.5, Portal, Multiverse, Glitch presets

```
Example: Fractured geometric shapes pulse to music in a void.
Style: Abstract. Electric blue and magenta on black. 1:1 ratio.
```

---

## Color Grade Vocabulary

Use these in any prompt regardless of style preset:

| Mood | Color grade description |
|------|------------------------|
| Cold thriller | "Teal and orange, desaturated, high contrast" |
| Warm nostalgia | "Golden hour amber, soft shadows, low contrast" |
| Cyberpunk | "Neon magenta and cyan, deep shadows, HDR" |
| Horror | "Sickly green-yellow, crushed blacks, desaturated" |
| Romance | "Soft warm pink-gold, lifted shadows, dreamy" |
| Documentary | "Neutral, natural light, no grade" |
| Epic fantasy | "Rich jewel tones, deep shadows, volumetric light" |
| Noir | "High contrast black and white, or near-monochrome" |
| Sci-fi cold | "Ice blue and silver, stark white light" |
| Post-apocalyptic | "Desaturated orange and brown, dust haze" |

---

## Lighting Vocabulary

| Type | Description | Best for |
|------|-------------|----------|
| Golden hour | Warm directional light just after sunrise or before sunset | Romantic, epic, beautiful |
| Overcast | Soft diffused light, no shadows | Documentary, emotional, grounded |
| Neon | Colored artificial light from signs/screens | Cyberpunk, night scenes, urban |
| Volumetric | Light rays visible through atmosphere (fog/dust) | Fantasy, cinematic, atmospheric |
| Practical only | All light comes from sources visible in frame (lamps, fire, screens) | Realism, noir, intimate |
| Side-lit | Single strong light from one side creating deep shadow | Drama, tension, portrait |
| Backlit | Subject silhouetted or rimlit from behind | Mystery, romance, epic reveal |
| Low key | Mostly dark with small pools of light | Horror, thriller, noir |
| High key | Bright, even, minimal shadows | Comedy, commercial, lifestyle |

---

## Cinematic Lighting Techniques

Specific lighting setups that AI models respond to well. Use these terms directly
in your prompts for precise control over how light shapes the scene.

| Technique | Effect | Best for |
|-----------|--------|----------|
| Rembrandt lighting | Triangle of light on the shadowed cheek, one eye lit | Portrait drama, character intros, moody interviews |
| Butterfly / Paramount lighting | Overhead light casting a shadow under the nose | Glamour, fashion, beauty shots, classic Hollywood |
| Split lighting | Half the face lit, half in complete shadow | Duality, inner conflict, villain reveals |
| Rim lighting / backlit | Edge glow outlining the subject's silhouette | Mystery, epic reveal, separation from background |
| Motivated lighting | Light source visible or implied in the scene (lamp, window, fire) | Realism, narrative grounding, naturalistic drama |
| Practical lighting | In-scene light sources (neon signs, candles, screens) | Night scenes, cyberpunk, intimate realism |
| Chiaroscuro | Extreme contrast between light and dark areas | Renaissance feel, high drama, painterly compositions |
| High-key | Bright, minimal shadows, even illumination | Comedy, commercial, lifestyle, clean aesthetic |
| Low-key | Deep shadows dominate, small pools of light | Noir, thriller, horror, psychological tension |
| Golden hour / Magic hour | Warm amber directional light, long soft shadows | Romance, beauty, epic landscapes, emotional beats |
| Blue hour | Cool steel-blue ambient light just after sunset | Melancholy, transition, quiet tension, urban solitude |
| Harsh midday sun | Hard overhead light, strong defined shadows | Desert, confrontation, exposed vulnerability |
| Overcast diffused / softbox | Even soft light, no hard shadows | Portraits, documentary, grounded realism |

---

## Aspect Ratio Guide

| Ratio | Name | Best for |
|-------|------|----------|
| 16:9 | Widescreen | Standard video, YouTube, film |
| 9:16 | Vertical | TikTok, Instagram Reels, Shorts |
| 2.35:1 | Anamorphic | Epic cinema, maximum widescreen drama |
| 1:1 | Square | Instagram posts, artistic |
| 4:5 | Portrait | Instagram feed, social portrait |
| 4:3 | Classic TV | Retro, VHS feel, vintage |

---

> **Negative constraints:** For texture/lighting artifacts (flickering textures, style ignored,
> over-lit output, color grade inconsistency) and their prevention phrases, see
> `../shared/negative-constraints.md` — Texture/Lighting Artifacts section.

---

## Style Best Practices (Cinema Studio 3.0 / Seedance 2.0)

These principles apply to Cinema Studio 3.0's generation engine (Business/Team plan only) and complement the style vocabulary above.

### One Style Anchor Rule

ONE primary style anchor beats five adjectives. Beyond 2–3 style tokens, model attention dilutes and the output becomes generic.

**Wrong:** `Style: cinematic, anamorphic, moody, atmospheric, dramatic lighting, film grain, desaturated, noir-inspired, high contrast, vintage feel`

**Right:** `Style: anamorphic, subtle grain, muted palette`

Pick your anchor (the single most important style element), add 1–2 supporting tokens, stop.

### "Cinematic" Does Nothing

Every generated video is "cinematic" by default. The word adds zero information. Replace it with a specific lens or contrast description:

- ~~"cinematic"~~ → `shallow depth of field, warm highlights, cool shadows`
- ~~"cinematic look"~~ → `anamorphic, 2.35:1, horizontal lens flares`
- ~~"cinematic quality"~~ → `35mm film stock, natural grain, Kodak Portra palette`

### Style Transfer via @Reference

Visual style references beat descriptive text. One reference image/video carries more style information than 10 descriptor words:

```
Match the visual style, color grading, and film texture of @Video1.
A woman walks through autumn leaves in a park.
Camera: slow tracking alongside her.
```

Use style references for: color grading, film stock emulation, lighting mood, texture quality, era-specific looks.

### CGI Material Contract

When prompting CGI or product renders, specify 2–4 material properties per surface to avoid the default "plastic sheen":

| Property | Options | Example |
|----------|---------|---------|
| Base | metal, glass, fabric, ceramic, wood, leather | `brushed stainless steel` |
| Roughness | matte, satin, glossy, mirror | `satin finish` |
| Imperfection | scratches, dust, wear, fingerprints, patina | `fine scratches from use` |
| Edge | beveled, sharp, rounded, chamfered | `soft rounded edges` |

**Example:** `A matte ceramic vase with hairline cracks and a subtle patina, soft rounded rim, resting on rough-hewn oak.`

### Period Control

Don't just name the decade — specify the **materials and lighting** of the era:

- ~~"1970s style"~~ → `Kodachrome warm tones, wood paneling, orange shag carpet, tungsten bulbs casting amber light`
- ~~"1940s noir"~~ → `high-contrast black and white, Venetian blind shadows, fedora silhouettes, wet asphalt reflecting streetlamps`
- ~~"1990s home video"~~ → `Hi8 camcorder grain, autofocus hunting, timestamp overlay, oversaturated greens`

---

## Related skills
- `higgsfield-camera` — Camera controls to pair with styles
- `higgsfield-mixed-media` — Artistic style overlays (non-photorealistic)
- `higgsfield-moodboard` — Moodboard + Soul Hex for project-level style locking
- `higgsfield-cinema` — Cinema Studio built-in color grading suite
- `templates/` — Annotated genre-specific prompt templates with style examples
