---
name: higgsfield-soul
description: >
  Use when the user wants to maintain character consistency across multiple
  generations, asks about Soul ID, creating reusable characters, or generating
  consistent people across different scenes and shots.
user-invocable: true
metadata:
  tags: [higgsfield, soul, character, consistency, Soul ID, identity]
  version: 1.5.1
  updated: 2026-03-18
  parent: higgsfield
---

# Higgsfield Soul ID — Character Consistency

## What Is Soul ID?

Soul ID is Higgsfield's character consistency system. You create a character reference once,
then reuse that same character across unlimited generations — different scenes, angles,
lighting, and actions — while the face and core appearance remain consistent.

This is Higgsfield's equivalent of casting the same actor for an entire film.

---

## How It Works

1. **Create a Soul ID** — Upload a reference image or generate one using Soul 2.0
2. **The platform stores the character** — assigns it an ID
3. **Reference in future prompts** — "using Soul ID character [name/reference]"
4. **Character stays consistent** — face, skin tone, basic features carry across generations

---

## When to Use Soul ID

✅ You're building a multi-shot sequence with the same character
✅ You're creating a short film / story with a recurring protagonist
✅ You're making an AI influencer or brand mascot
✅ You want consistent faces across a product ad campaign
✅ You're doing a multi-scene action sequence and need the hero to look the same

❌ Don't use if you only need one shot — overkill for single generations
❌ Don't use if you want maximum creative variation — consistency limits style range

---

## Prompting With Soul ID

When a Soul ID character is active, your prompt should:

**1. Reference the character simply:**
```
The Soul ID character walks through a crowded Tokyo street at night.
```

**2. Describe what changes — not what the character looks like:**
```
The Soul ID character now wears a formal black suit. She stands at a podium,
addressing a conference room. Camera: Dolly In toward her face.
Style: Cinematic, cool corporate lighting, 16:9.
```

**3. You can change clothing, setting, expression:**
```
The Soul ID character is now in a red dress, dancing alone in a ballroom.
Camera: 360 Orbit.
Style: Cinematic, warm golden chandelier light.
```

**Key rule:** Don't re-describe the face or core features — the Soul ID handles that.
Only describe what is *different* from the base character.

---

## Creating a Strong Soul ID Reference

The quality of your Soul ID reference image determines consistency quality.

**For best results:**
- Use a **front-facing or 3/4 angle** portrait — full face visible
- **Even lighting** — avoid harsh shadows obscuring features
- **Neutral to slight expression** — smile is fine, extreme emotion limits flexibility
- **Clear image** — no blur, no obstruction, no glasses if avoidable
- **Solo subject** — no other people in the reference frame

**Image models to generate your Soul ID reference:**
- **Soul 2.0** — best for fashion-forward, high-aesthetic characters
- **Nano Banana Pro 2** — best for maximum photorealistic sharpness
- **Seedream 4.5** — good for a range of styles

---

## Character Sheet Creation

A **character sheet** is a multi-angle reference image showing the same character from
several viewpoints — typically front, 3/4, side profile, and back. It gives the model
comprehensive geometry to work from and dramatically improves consistency.

**How to create a character sheet:**
1. Generate your character in Cinema Studio using your preferred optical stack
2. Use **Grid Generation (2×2 or 4×4)** to produce multiple variations
3. Alternatively, use **3D Mode (Gaussian splatting)** to orbit a single generation and
   capture front, side, and 3/4 angles
4. Arrange the best angles into a single composite reference image
5. Upload as your Soul ID reference

**What to include on a character sheet:**
- **Front face** — neutral expression, even lighting
- **3/4 angle** — shows depth of facial features
- **Side profile** — nose, jaw, ear structure
- **Full body** (optional) — posture, costume, proportions

**Prompt pattern to generate character sheet content:**
```
Front-facing portrait of [character description], neutral expression, even studio lighting,
clean background. Head and shoulders visible.
```
Then use 3D Mode to orbit and capture additional angles from the same generation.

**Why it matters:** A multi-angle character sheet gives Soul ID far more geometry data
than a single photo. This translates directly into better consistency across extreme
angle changes, action shots, and profile views.

---

## Multi-Character Consistency

If you need multiple consistent characters in the same scene:

```
Shot 1 — establish both:
The Soul ID character [Character A] and a second character [Character B, describe
appearance] face each other across a table. Camera: Arc slowly around them.

Shot 2 — reference both:
The Soul ID character [A] slides a folder across the table.
[Character B] opens it, expression shifting from confusion to realization.
Camera: Dolly In toward [B's] face.
```

Note: Higgsfield can hold multiple Soul IDs. Reference each clearly in the prompt.

---

## AI Influencer Workflow

Soul ID is the foundation of Higgsfield's AI Influencer Studio feature.

**Workflow:**
1. Create Soul ID from a high-quality portrait (generated or uploaded)
2. Generate images of the character in different outfits/settings
3. Animate using image-to-video with motion presets
4. Use Lipsync Studio to add speech if needed
5. Chain shots together for a full content series

**Prompt pattern for influencer content:**
```
The Soul ID character [name] is in a modern kitchen at golden hour.
She holds a coffee mug, steam rising. She looks directly at camera with a warm smile.
Camera: slight Dolly In. Style: Lifestyle, warm tones, 9:16 vertical.
```
