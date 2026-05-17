---
name: higgsfield-soul
description: "Creates and manages reusable character profiles (Soul IDs) for consistent facial and stylistic identity across multiple image and video generations. Provides identity-vs-motion prompt separation, character sheet creation workflows, micro-expression direction, and Soul Cast AI actor configuration. Use when the user wants to maintain character consistency across multiple generations, asks about Soul ID, creating reusable characters, or generating consistent people across different scenes and shots."
user-invocable: true
metadata:
  tags: [higgsfield, soul, character, consistency, Soul ID, identity]
  version: 3.3.0
  updated: 2026-05-17
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
- **Embedded prop sheets** (optional) — bake recurring character
  props directly into a character-sheet panel. Higgsfield image
  generation handles multi-element character images well, so prop
  continuity often holds without a separate prop sheet. For props
  that don't hold this way, see § Tricky-Prop Sheets below.

**Prompt pattern to generate character sheet content:**
```
Front-facing portrait of [character description], neutral expression, even studio lighting,
clean background. Head and shoulders visible.
```
Then use 3D Mode to orbit and capture additional angles from the same generation.

**Why it matters:** A multi-angle character sheet gives Soul ID far more geometry data
than a single photo. This translates directly into better consistency across extreme
angle changes, action shots, and profile views.

### Single-prompt 6-panel character sheet (3×2 grid)

An alternative to the multi-step assembly above is generating
the entire character sheet in **one prompt → one 16:9 image →
3×2 grid with six labeled panels**. Same character described
once; identity stays maximally locked across all six panels
because the generation pass is single. Prefer this for Soul ID
reference work when the image model supports a 16:9 grid layout
(Nano Banana Pro and similar grid-capable models).

The six panels in canonical order:

- **Panel 1 — Front body:** straight-on neutral stance, full
  styling visible head-to-toe
- **Panel 2 — 3/4 turn:** body angled ~30° from camera, weight
  on back hip
- **Panel 3 — Back body:** straight back view, hair fall and
  accessory details from behind
- **Panel 4 — Waist-up portrait:** head, shoulders, upper torso
- **Panel 5 — Hands detail close-up:** both hands forward, ring
  stack, nail finish, any held prop
- **Panel 6 — Face detail close-up:** tight crop from collarbone
  up, earrings, lips, skin texture, eyes

**Prompt pattern** — identity described once at the opening,
followed by panel position labels with what's different per
panel (stance, framing, focus). Close with: "Identical character
identity locked across all six panels. Uniform studio backdrop
and lighting across all six panels."

**Why single-prompt over multi-step:** the multi-step assembly
above (Grid Generation + 3D Mode + composite) produces a sheet
from multiple independent generations — identity can drift
panel-to-panel even with a strong reference. The single-prompt
3×2 grid keeps identity locked because all six panels render
together in one pass.

---

## Character Anchor Block

Where § Character Sheet Creation builds the multi-angle identity
reference that goes into Soul ID, the **Character Anchor Block**
is the per-shot prompt structure that locks how that character
appears IN a specific shot. The character sheet is build-time; the
anchor block is shot-time.

A complete anchor block names, per character in frame, ten
attributes:

1. **Identity** — which character this is (matches a Soul ID
   handle when references are present)
2. **Screen position** — qualitative anchor + percentage notation
   paired per `../higgsfield-seedance/SKILL.md` § Frame Coordinate
   System
3. **Depth layer** — foreground / midground / background
4. **Frame occupancy** — % of frame area the character fills
5. **Body orientation** — direction the character faces (toward
   camera, away, profile-left, profile-right, three-quarter)
6. **Pose** — current physical configuration (standing, seated,
   leaning, mid-stride)
7. **Gaze direction** — where the character is looking, named
   either by frame-position or by another subject (`looking at
   Character B`)
8. **Contact points** — what physical surface or object the
   character is grounded against
9. **State lock** — current emotional or physical state (calm,
   exhausted, injured, soaked, in motion) — see § Multi-Form State
   Tracking for state-across-scenes discipline
10. **Facial expression** — specific emotional register (composed,
    fearful, smiling small, gritted teeth)

The block sits before the Dynamic Description in the Seedance
output format and feeds a Spatial Layout Block when multiple
characters share frame (see `../higgsfield-seedance/SKILL.md`
§ Spatial Layout Block for the multi-character extension).

### Multi-Form State Tracking

When a character changes state across the project — wounds from a
fight scene that persist into the next scene, a costume change
midway through, a transformation across multiple stages — generate
a **separate anchor sheet per state**. Don't rely on the base
character sheet plus prompt-text descriptions to track the
difference; the model loses the state under iteration pressure.

The discipline is what film production calls **script supervising**:
every shot tracks which version of the character it should match. A
character with five stages (initial → fight-injuries → partially-
transformed → almost-fully → completely-transformed) gets five
distinct Soul ID sheets, one per stage. The shot list references
the matching sheet by name; the prompt names the stage in the
identity block.

The cost is one character-sheet generation pass per state; the
payoff is that no shot opens a continuity bug that has to be caught
at frame-review time (see `../higgsfield-seedance/FAILURE-MODES.md`
§ Frame-level review is mandatory).

### Face-from-Wide-Shot Workaround

In wide shots the face on a character-sheet panel often reads as
plasticky — the model deprioritizes facial detail when most of the
frame is body or environment. The workaround: render the wide shot,
then crop the **face** from a **closer shot** (medium-up, shoulders-
up, head-and-shoulders) and replace the wide-shot face with the
cropped one in post.

This is a character-sheet construction technique, not a generation
technique. Keep one closer-shot panel in the character sheet
specifically for this purpose — the face you'd cut and paste back
into wide shots that need it.

### Tricky-Prop Sheets

Some props don't generate consistently from a single reference panel
— a monster claw the model keeps rendering as a sword, a hand-prop
that defaults to a generic shape, an accessory that can't stay
continuous across shots. For these, build a **separate prop sheet**
alongside the character sheet:

- **Inside view** — interior structure or assembly detail
- **Outside view** — silhouette and surface
- **State variations** — open / closed / extended / grasped /
  combat-engaged, as the prop's narrative requires

The inverse pattern to the **Embedded prop sheets** bullet in
§ Character Sheet Creation above — embedded works for props that
generate cleanly; separate prop sheets are the fallback for props
that don't.

---

## Two-Tool Refinement Pipeline

For high-investment characters — leads who carry many shots in a
project — initial generation in **Soul Cinema** plus refinement
editing in **GPT Image 2** produces stronger anchor sheets than
either tool alone. Soul Cinema is the Higgsfield first-pass image
surface (high-volume batch generation against the character
description); GPT Image 2 is a third-party (OpenAI) edit surface
that preserves existing image details — particularly facial
geometry — when modifying outfits, accessories, lighting, or
background elements.

The split is by task:

- **Soul Cinema** — generate the initial character look across pose,
  expression, and lighting variations. Higher-volume; the model
  batches well.
- **GPT Image 2** — edit selected Soul Cinema outputs to refine
  costume, swap accessories, adjust lighting, or extend the sheet
  with state variations. Better preservation of the face under edit
  pressure.

When to reach for both tools: the character will appear in tens of
shots and is worth front-loading iteration cost into. A planning
anchor from a Higgsfield-team production — the lead character of
the 90-minute Cannes feature absorbed ~600 Soul Cinema generations
plus ~200 GPT Image 2 generations before any narrative shot
generation began (see `../../production-benchmarks.md` § Per-
character iteration anchor for the full breakdown).

When to stick with one tool: characters appearing in only a handful
of shots don't justify the two-tool overhead; a single Soul Cinema
pass suffices.

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

## Soul Cinema as the CS 3.0/3.5 Default Image Model

**Soul Cinema** is the default Cinematic model in the Cinema Studio 3.0 and 3.5 image-mode picker — the model that runs when you toggle Cinema Studio into image mode and do not change the model selection. It is shared across both Cinema Studio versions and is distinct from the older standalone "Soul Cinema Preview" model and from the separately-named Featured-list "Higgsfield Soul Cinema" (see `../higgsfield-cinema/SKILL.md` § Image Mode for the disambiguation).

### Soul ID identity prompting in Soul Cinema

When a Soul ID is active and Soul Cinema is the selected image model, the same **Identity vs. Motion separation** rule documented above applies — but Soul Cinema's general-purpose cinematic weighting means the Identity Block does most of the work and the "Motion Block" is replaced by a **Scene/Style Block** (since image generation has no temporal dimension).

**Identity Block** — Soul ID reference + static descriptors only:
```
The Soul ID character — [face/body/wardrobe descriptors only, no camera or motion language].
```

**Scene/Style Block** — environment + lighting + style direction:
```
[Setting], [time of day], [lighting quality], [color palette].
Style: Cinematic, [grade], [aspect ratio].
```

Keep the two blocks textually separate in the prompt. Do not re-describe identity inside the Scene/Style block — Soul Cinema is sensitive to identity drift if face/wardrobe descriptors leak into environmental phrasing. For broader picker context (when to pick Soul Cinema vs Cinematic Characters vs Cinematic Locations vs Cinematic Cameras), see `../higgsfield-cinema/SKILL.md` § Per-Cinematic-model selection guide.

### Studio Look vs. Cinematic Look — Soul Cinema as the Re-Pass

When a model returns a character that reads as **studio-feeling** — clean,
evenly lit, glossy, slightly plastic — the result is not a final. It's an
intermediate. The studio look is what the model defaults to when no atmosphere
or grade is doing work in the prompt; it's competently rendered but reads as
"AI-generated" rather than "filmed." (Distinct from **Cinema Studio**, the
product — here "studio" describes a visual quality of the output, not the
generation environment that produced it.) The fix is to treat the studio-feeling
output as a starting frame and re-pass it through Soul Cinema with explicit
cinematic direction — palette, grade, lens character, lighting language — until
the look lands.

These rules are adapted from the Mr. Core methodology.

**Diagnose the studio look.** Symptoms: skin reads as smooth/even rather than
specular; lighting feels evenly distributed (no key/fill ratio, no directional
shadow); palette is wide and accurate rather than graded; clothing fabric
reads as new and clean rather than worn or weighted; the frame as a whole
looks like a product photograph rather than a film still.

**The re-pass workflow.** Take the studio-feeling output and:

1. Use it as a reference upload into Soul Cinema (or use Edit Shot in Seedance
   if you want to preserve identity exactly and modify only the look).
2. Add an explicit grade direction — "Bleach Bypass," "Teal Orange Epic,"
   "Sodium Decay," "Bleached Warm" — pick from the Cinema Studio 3.5 Color
   Palette presets in `../higgsfield-cinema/SKILL.md` § Style Settings, or
   describe one in Manual Style.
3. Add directional lighting language — single key source, side rim, contre-jour,
   silhouette — not "well-lit" or "evenly lit."
4. Add lens character — Vintage Haze, Warm Halation, Anamorphic — to break the
   default clinical sharpness.
5. Add a palette compression — "muted," "desaturated," "crushed blacks" — to
   pull the wide accurate palette into a graded one.

The studio look is a stop on the path, not the destination. Plan for the
re-pass as part of the workflow; don't treat the first generation as the
final.

---

## Related skills
- `higgsfield-prompt` — MCSLA formula, Identity vs. Motion separation rule
- `higgsfield-cinema` — Cinema Studio Reference Anchor, Soul Cast, @ Elements
- `higgsfield-moodboard` — Soul Hex color palette for character consistency
- `higgsfield-pipeline` — Multi-shot workflow with Soul ID
- `higgsfield-recall` — Pre-generation memory check for character drift history
- `templates/` — Templates 03, 04, 05, 06, 08, 09, 10 include Identity/Motion Block examples
