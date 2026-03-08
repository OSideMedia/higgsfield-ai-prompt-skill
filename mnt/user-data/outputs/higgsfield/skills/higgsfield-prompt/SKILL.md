---
name: higgsfield-prompt
description: >
  Use when building, writing, refining, or structuring a Higgsfield AI prompt.
  Covers the MCSLA formula, prompt structure, narrative vs. timestamped formats,
  and how to write for both text-to-video and image-to-video workflows.
user-invocable: true
tags: [higgsfield, prompt, MCSLA, formula, text-to-video, image-to-video]
metadata:
  version: 1.4.0
  updated: 2026-03-08
  parent: higgsfield
---

# Higgsfield Prompt Engineering

## The MCSLA Formula

Every high-performing Higgsfield prompt is built on five layers. Think of it as the
cinematographer's checklist — fill in each layer and the model has everything it needs.

| Letter | Element | Description | Example |
|--------|---------|-------------|---------|
| **M** | Model | Which generation engine | "Use Kling 2.6" |
| **C** | Camera | Named camera control | "FPV Drone shot weaving through the alley" |
| **S** | Subject | Who/what + appearance | "A woman in a sand-colored suit, sharp eyes" |
| **L** | Look | Style + color + lighting | "Cinematic, golden hour, anamorphic flare" |
| **A** | Action | What happens in the scene | "She turns slowly, wind lifting her coat" |

---

## Prompt Types

### Text-to-Video (T2V)
Start from nothing — describe the entire scene from scratch.
Best for: establishing scenes, abstract concepts, environments without a specific character.

```
[Subject + appearance].
[Environment — location, time, weather, atmosphere].
[Action — what happens and how].
[Camera — named control].
[Look — style + color grade].
```

**Example:**
```
A lone astronaut stands on the surface of a red desert planet, helmet visor reflecting
twin moons rising on the horizon. Dust spirals slowly in the thin atmosphere.
She turns to face the camera, gloved hand raised in a slow salute.
Camera: slow Crane Up revealing the vast emptiness behind her.
Style: Cinematic, desaturated orange and deep blue, 2.35:1 anamorphic.
```

---

### Image-to-Video (I2V)
Animate a provided still image. The image defines the starting frame.
Best for: character consistency, product shots, portrait animation, storyboard bring-to-life.

```
[Reference the input image as the first frame].
[Describe what should move, change, or animate — not what is already visible].
[Camera — named control].
[Style/atmosphere cues].
```

**Example:**
```
Starting from the provided image as the first frame.
The woman's hair lifts gently in the wind. She blinks slowly and turns her gaze
slightly to the left, a faint smile forming.
Camera: subtle Dolly In toward her face.
Style: Cinematic, warm afternoon light, shallow depth of field.
```

**Key rule for I2V:** Do NOT re-describe what is already in the image. Only describe
what should *change* or *animate*. Over-describing the static elements confuses the model.

---

## Narrative Structure

### Fluid Narrative (preferred for most use cases)
Write the scene as continuous action. No timestamps. Most natural for Higgsfield.

```
A detective pushes open the door to the rain-soaked rooftop, coat whipping in the wind.
She steps to the edge and looks down at the city below — a thousand lights blurring
through the downpour. Camera dollies slowly behind her, then cranes up to reveal the
skyline. Cinematic style, cold blue tones, 16:9.
```

### Timestamped (use only for precise multi-beat sequences)
Only use when exact timing of separate actions matters — e.g., a transformation,
a multi-phase action sequence, or a beat-synced music video.

```
0–3s: Wide establishing shot. The fighter stands alone in the ring, chest heaving.
3–6s: Crash Zoom In on his face. Sweat on his brow, jaw clenched.
6–10s: 360 Orbit as he raises his fists. Crowd noise rises.
```

---

## High-Performing Prompt Patterns

**Specificity beats generality:**
- ❌ "the camera moves dramatically"
- ✅ "camera Dolly Zoom In — subject stays the same size as the background rushes forward"

**Active verbs carry the scene:**
- ❌ "a woman is in an alley"
- ✅ "a woman darts through a rain-soaked alley, coat flapping, boots splashing"

**Name the camera control:**
Higgsfield understands its own preset names. Always use them explicitly.
- ❌ "the camera slowly circles"
- ✅ "360 Orbit around the subject"

**Lead with subject, end with style:**
Subject → Action → Camera → Style is the most reliable order.

**Keep it under 200 words:**
Focused prompts outperform exhaustive ones. One clear intention > ten vague details.

**Cinema Studio: Keep it under 512 characters:**
Cinema Studio has a hard 512-character limit on prompts. @ Element chips consume
~80–100 hidden characters each. With 2 @ tags, keep visible text under ~250 chars.
See the Cinema Studio skill for full character budget details.

---

## The Pre-Prompt Checklist

Before writing any prompt, answer these five questions. Vague prompts like "give me
something cinematic" tell the AI nothing.

| Question | What to specify |
|----------|----------------|
| **Who?** | Subject + appearance (e.g. "a man in a leather jacket") |
| **Where?** | Environment + atmosphere (e.g. "in a narrow aircraft galley, cold blue light") |
| **What's happening?** | 1 primary action (e.g. "punches his opponent") |
| **Camera movement?** | Named preset (e.g. "Handheld") or Cinema Studio Director Panel |
| **Mood/Genre?** | Style + color grade, or Cinema Studio genre selection |

---

## One Action Per Scene

AI models can replicate real-life physics — but only so much at once. Asking for
multiple complex actions in one clip overwhelms the model.

**Rule:** 1 primary action per clip, with 1–2 secondary actions max.

Break complex sequences into separate shots and stitch them in a video editor, or
use Multi-Shot Manual mode to prompt each scene separately.

**Fast Motion Trick:** If fast motion keeps morphing or breaking, generate the scene
in Slow Mo first, then speed it up in post (CapCut, Premiere, DaVinci). The model
renders cleaner physics in slow motion.

---

## Common Prompt Mistakes

| Mistake | Fix |
|---------|-----|
| Re-describing the image in I2V | Only describe what changes/moves |
| Generic camera language | Use exact preset names |
| No style specified | Always include visual style + color grade |
| Too many actions in one shot | Split into separate generations and chain them |
| Contradictory movements | Don't combine Dolly In + Dolly Out in same shot |
| Prompt over 512 chars (Cinema Studio) | Cut text, reduce @ tags, use pronouns |
| Describing impact before action | Just describe the action, let AI render the result |
| Specific martial arts moves | Use general fighting energy instead of named moves |
| Multiple @ Elements in action scenes | Use @ for static scenes, plain text for action |
