---
name: higgsfield-soul
description: "Creates and manages reusable character profiles (Soul IDs) for consistent facial and stylistic identity across multiple image and video generations. Provides identity-vs-motion prompt separation, character sheet creation workflows, micro-expression direction, and Soul Cast AI actor configuration. Use when the user wants to maintain character consistency across multiple generations, asks about Soul ID, creating reusable characters, or generating consistent people across different scenes and shots."
user-invocable: true
metadata:
  tags: [higgsfield, soul, character, consistency, Soul ID, identity]
  version: 3.0.0
  updated: 2026-04-06
  parent: higgsfield
---

# Higgsfield Soul ID — Character Consistency

## What Is Soul ID?

Soul ID is Higgsfield's character consistency system. Create a character reference once,
then reuse it across unlimited generations — different scenes, angles, lighting, and
actions — while the face and core appearance remain consistent.

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

## Identity vs. Motion Separation — Hard Rule

When Soul ID is active, **every prompt MUST be split into two blocks**. This is the
single most important rule for preventing identity drift.

### Identity Block — Static descriptors only
Contains: face features, clothing, body type, distinguishing marks, color palette.
Does NOT contain: any motion, camera, speed, or temporal language.

### Motion Block — Temporal and camera only
Contains: camera movement, action choreography, speed, environmental changes.
Does NOT contain: any character appearance repetition.

### Before/After Examples

**Example 1 — Action scene:**

❌ **Mixed (bad) — causes identity drift:**
```
A tall woman with green eyes and freckles in a leather jacket sprints through
a warehouse while the camera tracks her and her green eyes flash with determination
and her freckles catch the fluorescent light as she vaults over a railing.
```
Face morphs mid-clip because the model re-reads face descriptors while processing motion.

✅ **Separated (good) — identity stays locked:**

**Identity Block:**
```
The Soul ID character — tall build, green eyes, light freckles across the nose
and cheeks, wearing a fitted black leather jacket, dark jeans.
```

**Motion Block:**
```
She sprints through a dimly lit warehouse, vaults over a metal railing
without breaking stride.
Camera: Action Run — low behind her, matching pace.
Fluorescent lights flicker overhead.
Style: Cinematic, cold industrial blue, high contrast. 16:9.
```

---

**Example 2 — Emotional close-up:**

❌ **Mixed (bad) — face warps during camera move:**
```
A weathered man with deep wrinkles and sad brown eyes wearing a grey wool coat
sits on a park bench as the camera slowly dollies in on his wrinkled face and
sad brown eyes while autumn leaves drift past his grey coat.
```

✅ **Separated (good) — face stays sharp:**

**Identity Block:**
```
The Soul ID character — man in his 60s, deep wrinkles, warm brown eyes,
wearing a heavy grey wool coat, brown leather gloves.
```

**Motion Block:**
```
He sits on a park bench, hands folded in his lap, staring at the ground.
A single autumn leaf drifts into frame and lands on the bench beside him.
Camera: slow Dolly In toward his face.
Style: Cinematic. Overcast diffused light, muted earth tones. 16:9.
```

---

**Example 3 — Cinema Studio (@ Elements):**

❌ **Mixed (bad) — identity in the prompt field:**
```
@Sarah with her dark curly hair and tattoo sleeve walks into the bar.
```

✅ **Separated (good) — identity in the Element, motion in the prompt:**

**@ Element definition (set in Cinema Studio UI):**
```
@Sarah: dark curly hair, tattoo sleeve on left arm, wearing a vintage band tee.
```

**Prompt field:**
```
@Sarah pushes open the door and steps inside. She scans the room, then walks
to the far end of the bar. The bartender nods.
```

### Which descriptors belong where

| Identity Block | Motion Block |
|---------------|-------------|
| Face shape, skin tone, eye color | Camera movement name |
| Hair style, color, length | Action verbs (runs, turns, sits) |
| Body type, height, build | Environmental motion (wind, rain, lights) |
| Clothing, accessories, jewelry | Speed and timing cues |
| Scars, tattoos, distinguishing marks | Atmospheric changes (light shifts, fog) |
| Color palette of the character | Style and color grade of the scene |

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
- **Nano Banana Pro** — best for maximum photorealistic sharpness
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

## Micro-Expressions — Nuanced Performance Direction

Use these facial performance directions to add emotional depth to Soul ID characters.
Combine with Soul Cast or character prompting for precise actor-level control.

### Core Set

| Name | Description | Best for |
|------|-------------|----------|
| **Deadpan Neutral** | Flat affect, no visible emotion, mask-like stillness | Thriller, interrogation, AI/android characters |
| **Fierce Focus** | Intense locked gaze, brow slightly lowered, total attention | Action, competition, confrontation |
| **Subtle Arrogance** | Chin slightly raised, half-lidded eyes, faint smirk | Villain intros, power dynamics, fashion |
| **Candid Profile** | Unposed side angle, natural and unaware of camera | Documentary, street photography, slice-of-life |
| **Post-Workout Fatigue** | Heavy lids, parted lips, light sheen of sweat, relaxed muscles | Fitness, aftermath, exhaustion scenes |
| **Predator Glare** | Unblinking stare, head slightly lowered, eyes locked forward | Horror, thriller, intimidation |
| **Sunblind Squint** | Eyes narrowed against bright light, slight grimace | Outdoor scenes, desert, beach, golden hour |
| **Total Dissociation** | Thousand-yard stare, eyes unfocused, emotionally absent | Trauma, shock, psychological drama |
| **Controlled Breath** | Lips slightly parted, nostrils flared, deliberate calm | Pre-action tension, meditation, recovery |

### Extended Set

| Name | Description | Best for |
|------|-------------|----------|
| **Suppressed Smile** | Fighting back a grin, corner of mouth twitching | Comedy, secret joy, romantic tension |
| **Quiet Devastation** | Eyes glassy, jaw tight, holding it together | Drama, grief, emotional climax |
| **Wary Recognition** | Eyes widen slightly, head tilts back a fraction | Reunion, suspicion, plot twist reaction |
| **Nervous Composure** | Calm face but swallowing, micro-tension in jaw | Interviews, lies, high-stakes poker |
| **Cold Calculation** | Eyes scanning, no emotional leakage, clinical | Villain strategy, heist planning, espionage |
| **Bitter Amusement** | One-sided smirk, eyes not smiling | Cynicism, dark humor, betrayal aftermath |
| **Exhausted Relief** | Eyes closing, shoulders dropping, breath release | Survival, rescue, end of ordeal |
| **Frozen Shock** | Mouth slightly open, eyes fixed, body still | Jump scares, bad news, sudden revelation |
| **Simmering Rage** | Clenched jaw, flared nostrils, steady stare | Confrontation, injustice, slow burn tension |
| **Vulnerable Openness** | Soft eyes, slightly parted lips, unguarded | Romance, confession, emotional honesty |

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

---

> **Negative constraints:** For face/identity artifacts (face morphing, identity drift,
> character swap, plastic skin) and their prevention phrases, see
> `../shared/negative-constraints.md` — Face/Identity Artifacts section.

---

## Cinema Studio 3.0 Soul Cast (Business/Team Plan)

> **Plan requirement:** Cinema Studio 3.0 Soul Cast is available exclusively on **Business and Team plans**.

Cinema Studio 3.0 carries over Soul Cast's 8 parameter categories from 2.5:

| Category | Options |
|----------|---------|
| Genre | General, Action, Horror, Comedy, Noir, Drama, Epic |
| Budget | $10M – $500M (affects production value aesthetic) |
| Era | 1900s – 2020s (decade increments) |
| Archetype | Innocent, Everyman, Hero, Caregiver, Explorer, Rebel, Lover, Creator, Jester, Sage, Magician, Ruler (12 options) |
| Identity | Gender, race, age |
| Physical Appearance | Build, height, eye color, hair style, hair texture, hair color, facial hair |
| Details | Scars, tattoos, accessories, distinguishing marks |
| Outfit | Clothing, materials, colors |

### 3.0 Soul Cast Modes

| Mode | Purpose | Output |
|------|---------|--------|
| General | Open-ended character generation | Character image |
| Character | Focused character creation with detailed parameters | Character image |
| Location | Environment/setting generation | Location image |

### 3.0 Soul Cast Specs

- Image resolution: up to 4K (Character/Location modes) · up to 2K (General mode)
- Batch size: 1 or 10
- Generation cost: 0.125 credits per image

### Character Consistency Best Practices

**Use 2–3 clear, well-lit reference shots:**
- Frontal view (primary identity anchor)
- 3/4-angle view (dimensional understanding)
- Side profile (silhouette + hair/ear/jawline)

**Outfit descriptions must be specific:**
- ~~"casual clothes"~~ → `fitted olive-green cotton t-shirt, dark indigo slim jeans, white leather sneakers with red accents`
- Include materials, colors, and distinctive details that the model can anchor to

**In I2V workflows — describe action, not appearance:**
The reference image already carries the character's visual identity. Re-describing their appearance creates conflict.

- **Wrong:** `@Image1 — A woman with curly brown hair and green eyes wearing a red jacket walks through the park.`
- **Right:** `@Image1 — She walks through the park, pausing to look up at the falling leaves. Camera: slow tracking alongside.`

**If features drift between shots:**
Use the character sheet image directly as @Image1 for tighter identity anchoring. A clean, well-lit character sheet outperforms multiple casual photos.

**Multi-character scenes:**
Reference each character separately with distinct @Image tags:

```
@Image1 as Character A (the detective). @Image2 as Character B (the witness).
Character A leans across the table, speaking firmly. Character B looks away, fidgeting.
Camera: slow push-in on Character B's face.
```

---

## Related skills
- `higgsfield-prompt` — MCSLA formula, Identity vs. Motion separation rule
- `higgsfield-cinema` — Cinema Studio Reference Anchor, Soul Cast, @ Elements
- `higgsfield-moodboard` — Soul Hex color palette for character consistency
- `higgsfield-pipeline` — Multi-shot workflow with Soul ID
- `higgsfield-recall` — Pre-generation memory check for character drift history
- `templates/` — Templates 03, 04, 05, 06, 08, 09, 10 include Identity/Motion Block examples
