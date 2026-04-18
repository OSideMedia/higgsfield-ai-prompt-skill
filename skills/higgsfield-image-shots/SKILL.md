---
name: higgsfield-image-shots
description: >
  Use when the user wants to generate a cinematic still image on Higgsfield,
  asks about shot framing, camera angle, or composition for image prompts,
  needs a specific shot type (close-up, wide shot, cowboy shot, etc.),
  or is working with [img] reference-based image generation. Covers distance
  & size shots, camera angles, and camera movement keywords optimized for
  AI image models (Soul 2.0, Nano Banana, Seedream, GPT Image, Flux, etc.).
user-invocable: true
metadata:
  tags: [higgsfield, image, shots, framing, angle, composition, cinematic, portrait, close-up, wide-shot]
  version: 3.0.0
  updated: 2026-04-06
  parent: higgsfield
---

# Higgsfield Cinematic Image Prompting

This skill covers **still image** shot composition — framing, angles, and implied
camera movement for AI image generation. Use these keywords and patterns when
building prompts for any Higgsfield image model.

**Key difference from video camera controls:** These are composition directives
for a single frame. The `[img 1]` token references a Soul ID character or
uploaded reference image. Replace it with your character description or @ Element
when no reference image is used.

---

## How to Use This Reference

Every entry has:
- **Shot/Movement** — the cinematography term
- **AI Prompt Keyword** — the exact words to put in your image prompt
- **Purpose** — what emotional/compositional effect it creates
- **Prompt Example** — a ready-to-adapt prompt phrase

**Prompt pattern for image generation:**
```
[Shot keyword] of [img 1 or character description] + [pose/action] + [environment detail] + [lighting/atmosphere]
```

---

## Distance & Size — Shot Framing

These control how much of the subject fills the frame and how much
environment is visible. Choose based on whether the image is about
the world, the character, or a detail.

### Extreme Wide Shot (EWS)
**AI Prompt Keyword:** EWS, Vast, Landscape
**Definition:** The subject is barely visible; emphasizes the vast landscape or location.
**Purpose:** Establish vastness, show isolation, or emphasize scale.
**Prompt Example:**
```
Extreme wide shot of [img 1] standing alone in a vast, empty frozen tundra.
The subject is small in the distance, surrounded by massive snowy mountains.
Cinematic lighting
```

---

### Wide Shot (WS) / Long Shot
**AI Prompt Keyword:** Wide Shot, Full Body
**Definition:** Shows the full subject within their environment.
**Purpose:** Provide context and spatial awareness.
**Prompt Example:**
```
Wide shot of [img 1] standing full body in a snowstorm. She is wearing fur armor,
boots visible, centered in a snowy forest clearing. Environmental context.
```

---

### Full Shot
**AI Prompt Keyword:** Full Shot, Framed
**Definition:** Frames the subject from head to toe while filling more of the frame.
**Purpose:** Balance character detail with environment.
**Prompt Example:**
```
Full body shot of [img 1] from head to toe. She stands confidently in the snow,
holding a weapon at her side. Detailed costume design
```

---

### Medium Long Shot (MLS)
**AI Prompt Keyword:** Medium Long Shot
**Definition:** Frames the subject from knees up.
**Purpose:** Natural framing for movement or dialogue.
**Prompt Example:**
```
Medium long shot of [img 1] framed from the knees up. She is walking through
deep snow, looking towards the horizon. 3/4 angle view.
```

---

### Cowboy Shot
**AI Prompt Keyword:** Cowboy Shot
**Definition:** Frames subject from mid-thigh up.
**Purpose:** Emphasize posture, readiness, or action.
**Prompt Example:**
```
Cowboy shot of [img 1] framed from mid-thigh up. Focus on her hands resting
on her belt, confident stance, snowy background with soft bokeh.
```

---

### Medium Shot (MS)
**AI Prompt Keyword:** Medium Shot
**Definition:** Frames the subject from the waist up.
**Purpose:** Balanced emotional and physical framing.
**Prompt Example:**
```
Medium shot of [img 1] from the waist up. She is looking directly at the camera
with a serious expression. Snowflakes falling in the foreground.
```

---

### Medium Close-Up (MCU)
**AI Prompt Keyword:** MCU
**Definition:** Frames subject from chest or shoulders up.
**Purpose:** Emotional connection without intensity.
**Prompt Example:**
```
Medium close-up of [img 1] framed from chest up. Focus on her face and fur collar.
The wind is blowing her braided hair. Intimate and dramatic
```

---

### Close-Up (CU)
**AI Prompt Keyword:** Close-Up
**Definition:** Tight framing on the face or a key detail.
**Purpose:** Highlight emotion or detail.
**Prompt Example:**
```
Close-up of [img 1], framing only her head and neck. Her piercing eyes looking
into the lens. Frosty breath visible in the cold air.
```

---

### Extreme Close-Up (ECU)
**AI Prompt Keyword:** ECU
**Definition:** Focuses on a very small detail.
**Purpose:** Heighten tension or intimacy.
**Prompt Example:**
```
Extreme close-up on the eyes of [img 1]. Macro detail of the iris, snowflakes
caught in her eyelashes, war paint texture. Intense gaze
```

---

### Macro Shot
**AI Prompt Keyword:** Macro
**Definition:** Ultra-close shot showing fine texture.
**Purpose:** Emphasize detail and texture.
**Prompt Example:**
```
Macro shot of the texture of [img 1]'s fur armor and the frost on her skin.
Microscopic details of snow crystals and leather grain
```

---

## Distance & Size — Quick Reference

| Shot | Frame content | AI Keyword | Best for |
|------|--------------|------------|----------|
| EWS | Subject tiny in vast landscape | EWS, Vast, Landscape | Scale, isolation, world-building |
| Wide / Long | Full body + full environment | Wide Shot, Full Body | Context, establishing |
| Full Shot | Head to toe, subject fills frame | Full Shot, Framed | Costume, character intro |
| Medium Long | Knees up | Medium Long Shot | Movement, dialogue |
| Cowboy | Mid-thigh up | Cowboy Shot | Posture, readiness, action |
| Medium | Waist up | Medium Shot | Balanced emotion + body |
| MCU | Chest/shoulders up | MCU | Connection, intimacy |
| Close-Up | Face | Close-Up | Emotion, expression |
| ECU | Single detail (eyes, hands) | ECU | Tension, intimacy, texture |
| Macro | Ultra-close texture | Macro | Detail, material, surface |

---

## Angles

These control the camera's vertical and spatial relationship to the subject.
Angle choice dramatically changes the emotional read of an image.

### Eye-Level
**AI Prompt Keyword:** Eye-Level
**Definition:** Camera is level with the subject's eyes.
**Purpose:** Neutral, realistic perspective.
**Prompt Example:**
```
Eye-level shot of [img 1] facing the camera. Neutral perspective, realistic
documentary style portrait in the snow.
```

---

### Low Angle
**AI Prompt Keyword:** Low Angle
**Definition:** Camera looks up at the subject.
**Purpose:** Convey power or dominance.
**Prompt Example:**
```
Low angle shot looking up at [img 1]. She towers over the camera, looking powerful
and dominant against a stormy sky.
```

---

### High Angle
**AI Prompt Keyword:** High Angle
**Definition:** Camera looks down at the subject.
**Purpose:** Convey vulnerability or insignificance.
**Prompt Example:**
```
High angle shot looking down at [img 1]. She is looking up towards the camera,
snow falling onto her face. Vulnerable perspective.
```

---

### Overhead / Bird's Eye View
**AI Prompt Keyword:** Overhead
**Definition:** Shot from directly above.
**Purpose:** Abstract or strategic perspective.
**Prompt Example:**
```
Direct overhead bird's eye view of [img 1] standing in the snow. Top-down angle
showing her shadow stretching on the white ground.
```

---

### Worm's Eye View
**AI Prompt Keyword:** Worm's Eye
**Definition:** Shot from ground level looking straight up.
**Purpose:** Extreme power or surreal scale.
**Prompt Example:**
```
Worm's eye view from the ground looking up at [img 1]'s boots and legs, with
her face distant in the sky. Ant-man perspective
```

---

### Dutch Angle / Canted Angle
**AI Prompt Keyword:** Dutch Angle, Canted Angle
**Definition:** The camera is tilted sideways (tilted horizon).
**Purpose:** Creates unease, disorientation, or chaos.
**Prompt Example:**
```
Dutch angle shot of [img 1], tilted horizon line. Disorienting and chaotic
atmosphere, battle ready pose, dynamic composition
```

---

### Over-the-Shoulder (OTS)
**AI Prompt Keyword:** Over-the-Shoulder, OTS
**Definition:** Looking past one person's shoulder at another.
**Purpose:** Essential for dialogue, grounds the conversation.
**Prompt Example:**
```
Over-the-shoulder shot looking past a blurry Viking warrior in the foreground,
focusing on [img 1] who is staring back at them.
```

---

### Point of View (POV)
**AI Prompt Keyword:** POV, First Person Perspective
**Definition:** The camera *is* the character's eyes.
**Purpose:** Viewer experiences what the character sees, high immersion.
**Prompt Example:**
```
First person POV shot of someone approaching [img 1]. She is looking directly
at the viewer, hand extended as if greeting the camera.
```

---

### Selfie Angle
**AI Prompt Keyword:** Selfie Angle, Arm's Length
**Definition:** High angle, arm's length, facing the subject.
**Purpose:** Common in social media aesthetics, informal, close.
**Prompt Example:**
```
Handheld selfie angle of [img 1] looking into the lens, arm extended.
Casual vlog style, snowy mountains in the immediate background.
```

---

### Ground Level
**AI Prompt Keyword:** Ground Level, Surface View
**Definition:** Camera sits directly on the floor/surface, often with shallow depth of field.
**Purpose:** Immersive close-up of the ground or environment.
**Prompt Example:**
```
Ground level shot, camera resting on the snow. Shallow depth of field with snow
crystals in foreground, [img 1] walking in the background.
```

---

## Angles — Quick Reference

| Angle | Camera position | AI Keyword | Emotional effect |
|-------|----------------|------------|-----------------|
| Eye-Level | Level with eyes | Eye-Level | Neutral, realistic |
| Low Angle | Below, looking up | Low Angle | Power, dominance |
| High Angle | Above, looking down | High Angle | Vulnerability, insignificance |
| Overhead | Directly above | Overhead | Abstract, strategic |
| Worm's Eye | Ground, looking straight up | Worm's Eye | Extreme power, surreal |
| Dutch Angle | Tilted horizon | Dutch Angle, Canted Angle | Unease, chaos, tension |
| OTS | Past shoulder | Over-the-Shoulder, OTS | Dialogue, confrontation |
| POV | Character's eyes | POV, First Person Perspective | Immersion |
| Selfie | Arm's length, high | Selfie Angle, Arm's Length | Social media, casual |
| Ground Level | On the surface | Ground Level, Surface View | Environmental immersion |

---

## Camera Movements (Implied in Still Images)

For image generation, camera movement keywords create the *feeling* of motion
in a single frame — motion blur, composition that implies movement, or a
frozen moment mid-movement.

### Static / Basic

| Movement | AI Keyword | Definition | Purpose | Prompt Example |
|----------|-----------|------------|---------|----------------|
| Static Shot | Static | Camera does not move | Stability and focus | "Static camera shot of [img 1]. She stands perfectly still while snow falls heavily around her and the wind moves her hair. Tripod shot." |
| Pan Left/Right | Pan | Camera rotates horizontally | Reveal or follow action | "Camera pans slowly from left to right, starting on a snowy tree and revealing [img 1] standing in the distance." |
| Tilt Up/Down | Tilt | Camera tilts vertically | Reveal height or depth | "Camera tilts up, starting at [img 1]'s boots in the snow and moving up to reveal her face and the mountain peak behind her." |
| Zoom In | Zoom In, Lens Zoom | Camera slowly moves toward subject | Increase emotional intensity | "Slow zoom in on [img 1]'s face. The background compresses as the camera gets tighter on her expression." |
| Zoom Out | Zoom Out, Wide Reveal | Camera moves away from subject | Reveal environment or isolation | "Zoom out from [img 1]'s eye to reveal she is standing on the edge of a massive cliff. Establishing the environment." |
| Pedestal Up/Down | Pedestal Up, Pedestal Down | Entire camera physically moves up or down (elevator motion) | Change subject's relationship to ground | "Camera pedestals up, rising from the snow level to eye-level with [img 1], revealing her stature against the mountains." |

---

### Advanced Physical

| Movement | AI Keyword | Definition | Purpose | Prompt Example |
|----------|-----------|------------|---------|----------------|
| Dolly In | Dolly In | Camera moves forward on a track | Controlled cinematic intimacy | "Smooth cinematic dolly in towards [img 1]. The camera physically pushes forward through the snow, getting closer to her." |
| Dolly Out | Dolly Out | Camera moves backward on a track | Reveal scale or emotional distance | "Cinematic dolly out from [img 1]. The camera physically moves backward, starting close to her face and retreating to show her alone." |
| Truck Left/Right | Truck Left | Camera moves horizontally left or right | Add parallax and motion | "Truck right camera movement. The camera slides sideways parallel to [img 1] as she stands in profile, revealing the army behind her." |
| Orbit Shot | Orbit | Camera circles the subject | Dramatic emphasis and energy | "Camera orbits 360 degrees around [img 1]. She stands still in the center while the snowy background spins slowly behind her." |
| Crane Shot | Crane | Camera moves vertically on a crane | Grand reveal or epic scale | "Crane shot starting low on [img 1] and sweeping high up into the air, looking down at the snowy valley below." |

---

### Cinematic & AI

| Movement | AI Keyword | Definition | Purpose | Prompt Example |
|----------|-----------|------------|---------|----------------|
| Dolly Zoom | Dolly Zoom, Vertigo Effect | Camera moves backward while zooming in (or vice versa) | Background warps while subject stays the same size — disorientation | "Dolly zoom effect on [img 1]. The background mountains appear to warp and grow larger while she stays the same size. Vertigo effect." |
| Crash Zoom | Crash Zoom | Fast aggressive zoom | Shock or sudden emphasis | "Sudden crash zoom into [img 1]'s face. The camera snaps from a wide shot to an extreme close-up instantly. Dramatic impact." |
| FPV Drone Shot | FPV | Fast, immersive flying camera movement | High energy and immersion | "Fast FPV drone shot flying through a snowy canyon and swooping past [img 1]. High speed, dynamic motion blur." |
| Bullet Time | Bullet Time | Time appears frozen while camera moves | Stylized dramatic emphasis | "Bullet time effect. Time is frozen with snowflakes suspended in mid-air, while the camera smoothly rotates 180 degrees around [img 1]." |
| Handheld Follow | Handheld Follow | Handheld camera follows subject | Urgency and realism | "Handheld camera movement following [img 1]. The image has slight shake and organic motion, documentary war reporter style." |
| Camera Roll | Camera Roll | Camera rotates on its axis | Disorientation or intensity | "Camera roll. The horizon line spins 360 degrees while focused on [img 1], turning the snowy world upside down and back again." |
| Rack Focus | Rack Focus | Focus shifts between subjects | Guide viewer attention | "Rack focus shot. Starts focused on a sword in the foreground, then shifts focus to [img 1]'s face in the background." |
| Pull Back Reveal | Reveal | Camera pulls back to reveal new context | Surprise or scale reveal | "Pull back reveal. Camera starts on the detail of [img 1]'s eye, then pulls back rapidly to show she is standing on top of a burning village." |
| Fly-Through | Fly-Through | Camera moves through environment elements | Immersion and momentum | "Camera flies through a gap in the trees and past falling snow to land on a medium shot of [img 1]." |

---

## Combining Shot + Angle + Movement

The strongest image prompts layer all three:

**Pattern:** `[Distance/Size] + [Angle] + [Movement hint] + [Subject] + [Environment] + [Lighting]`

**Examples:**

```
Low angle medium close-up of [img 1], camera dolly zooming in slowly.
She towers over the frame against a blood-red sunset, wind whipping her cloak.
Cinematic lighting, high contrast.
```

```
Overhead extreme wide shot, static camera. [img 1] is a tiny figure at the center
of a vast frozen lake, her shadow stretching long. Blue hour lighting, desolate.
```

```
Ground level close-up, rack focus. Snow crystals sharp in the foreground,
[img 1]'s boots blurred behind them, then focus shifts to her face looking down.
Shallow depth of field, cold blue tones.
```

```
Dutch angle cowboy shot, handheld feel. [img 1] stands mid-thigh up in a
burning village, tilted horizon, smoke swirling. War paint on her face,
weapon drawn. Chaotic, urgent composition.
```

---

## Image Prompt Formula (for Cinematic Stills)

```
[Shot size] + [Angle] + [Movement keyword] of [img 1 / character description].
[Pose, expression, or action].
[Environment — location, weather, atmosphere].
[Lighting — time of day, source, quality].
[Style — cinematic, film stock, color grade].
```

**Full example:**
```
Medium close-up, low angle, slow dolly in toward [img 1].
She stares past the camera with narrowed eyes, jaw set, braids falling over
one shoulder. A frozen battlefield stretches behind her, smoke rising from
distant fires. Golden hour backlight rims her silhouette.
Style: Cinematic, Kodak Vision3 500T, desaturated teal shadows, warm highlights.
```

---

> **Negative constraints:** For face/identity and texture/lighting artifacts in image generation,
> see `../shared/negative-constraints.md`.

---

## Related skills
- `higgsfield-camera` — Video camera controls (this skill covers still-image composition)
- `higgsfield-style` — Visual styles and lighting techniques
- `higgsfield-soul` — Soul ID for character-consistent image series
- `higgsfield-cinema` — Cinema Studio optical physics engine for image generation
- `higgsfield-models` — Image model selection (Soul 2.0, Nano Banana, Seedream, etc.)
- `templates/` — Annotated genre-specific prompt templates
