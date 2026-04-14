---
name: higgsfield-cinema
description: "Guides users through professional filmmaking workflows in Higgsfield Cinema Studio, including creating multi-shot sequences, configuring optical stacks, applying color grading, managing Soul Cast AI actors, and structuring per-scene prompts with Director Panel camera movements. Use when the user mentions Cinema Studio, Cinema Studio 2.5, Cinema Studio 3.0, Soul Cast, color grading, multi-shot video, shot sequences, storyboard workflow, Hero Frame, optical stack, keyframe interpolation, Elements system (@Characters/@Locations/@Props), Speed Ramp, Director Panel, Higgsfield Popcorn, Single Shot / Multi-Shot Auto / Multi-Shot Manual modes, Reference Anchor, Smart shot control, or any professional filmmaking workflow inside Higgsfield."
user-invocable: true
metadata:
  tags: [higgsfield, cinema-studio, multi-shot, storyboard, popcorn, hero-frame, optical, elements, director-panel, speed-ramp, soul-cast, color-grading]
  version: 3.0.0
  updated: 2026-04-06
  parent: higgsfield
---

# Higgsfield Cinema Studio 2.5

Cinema Studio is Higgsfield's professional filmmaking environment — a full production
workflow for multi-shot, character-consistent cinematic content. It's fundamentally
different from single-clip generation: you're building sequences, not individual videos.

---

## Cinema Studio vs Standard Generation

| | Standard Generation | Cinema Studio 2.5 | Cinema Studio 3.0 (Business/Team Plan) |
|--|--------------------|--------------------|----------------------------------------|
| Output | Single clip | Multi-shot sequence | Multi-shot sequence |
| Character consistency | Manual / Soul ID only | Reference Anchor system | @ reference system (up to 9 images) |
| AI actor generation | Not available | Soul Cast — generate actors from parameters (no photos) | Soul Cast — General (2K) / Character (4K) / Location (4K) modes, 0.125 credits |
| Camera control | Named presets | Director Panel (18 movements) | Director Panel + Smart (auto camera planning) |
| Optical physics | Not available | Full camera body + lens stack | Not available |
| Color grading | Not available | Built-in suite (temp, contrast, grain, bloom, etc.) | Not available |
| Shot structure | One prompt = one clip | Up to 6 scenes, 12s total max, per-scene config | Smart (auto) + Custom multi-shot (up to 6 scenes, 15s) |
| 3D exploration | Not available | Gaussian splatting — move inside any generated image | Not available |
| Batch generation | Not available | Grid generation — up to 16 variations per credit | Not available |
| Storyboard | Not available | Higgsfield Popcorn integration | Not available |
| Speed control | Not available | Speed Ramp (6 modes) | Speed Ramp (7 modes + Bullet Time, Hero Moment) |
| Genre | Style descriptions | 8 named genres | 7 genres (General, Action, Horror, Comedy, Noir, Drama, Epic) |
| Audio | Model-dependent | On/Off | On/Off (native dual-channel stereo) |
| Video resolution | Model-dependent | Up to 1080p | Up to 720p (may increase) |
| Image resolution | Model-dependent | Up to 4K | Up to 4K (Character/Location) · Up to 2K (General) |
| Max video duration | Model-dependent | 12s | 15s |
| Aspect ratios | Model-dependent | 6 options | 7 options (+ 21:9 ultrawide) |
| Plan requirement | All plans | All plans | **Business/Team plan only** |

**Use Cinema Studio when:**
- You need 2+ shots that must feel like the same film
- Character geometry must be locked across cuts
- You want professional optical physics (lens flare, depth of field, sensor grain) — 2.5 only
- You're building a short film, branded content, or any sequence longer than one clip

**Stick with standard generation when:**
- Single clip is sufficient
- Speed matters more than consistency
- Exploring ideas before committing to a full sequence

---

## ⚠ Version Detection — Ask First

**Before generating any Cinema Studio output, always ask the user:**

> Are you working in **Cinema Studio 2.5** or **Cinema Studio 3.0**?

If the user has already stated their version (e.g., "I'm using 3.0" or "Cinema Studio 3.0"), remember it and don't ask again. But never assume — 2.5 and 3.0 have fundamentally different feature sets.

**Why this matters:**
- 2.5 has optical physics (camera body + lens stack), color grading, 3D Mode, grid generation
- 3.0 has **none of those** — outputting them wastes the user's time and causes confusion
- 3.0 has features 2.5 doesn't: native audio, Smart shot control, 21:9 ultrawide, 15s duration
- Speed Ramp options differ between versions
- Genre lists differ between versions

**Once the version is known, use ONLY that version's output format and feature set.** Never mix features from one version into output for the other.

---

## The 10-Step Cinema Studio 2.5 Workflow

Cinema Studio 2.5 extends the pipeline in both directions: **pre-production** (Soul Cast +
location prompt) before generation, and **post-production** (color grading) after.

```
 1. SCRIPT        → Write or paste your scene description / shot list
 2. SOUL CAST     → (New in 2.5) Generate AI actors from parameters or use saved Elements
 3. REFERENCE     → Upload character photo → create Reference Anchor (or use Soul Cast actor)
 4. ELEMENTS      → (Optional) Define @Characters, @Locations, @Props if needed
 5. OPTICAL STACK → Select camera body + lens + focal length + aperture (image mode)
 6. HERO FRAME    → Generate a key image that defines the visual tone
 7. COLOR GRADE   → (New in 2.5) Apply color grading to keyframes before video generation
 8. CAMERA CONFIG → Set Director Panel movement + Speed Ramp + Duration in UI
 9. SHOT MODE     → Choose Single Shot / Multi-Shot Auto / Multi-Shot Manual
10. GENERATE → EXPORT → Chain into timeline or export to editing
```

---

## Elements System — Define Once, Call Everywhere

Elements are Cinema Studio's reusable asset library. Create a Character, Location, or Prop
once and reference it with `@` in any subsequent prompt.

**Three element types:**

| Type | What it stores | Call with |
|------|---------------|-----------|
| Character | Person, appearance, costume | `@CharacterName` |
| Location | Environment, setting, atmosphere | `@LocationName` |
| Prop | Object, vehicle, specific item | `@PropName` |

**Creation workflow:**
1. Open Elements panel → New Element → choose type
2. Upload reference image(s)
3. Name the element (this becomes the `@` tag)
4. Add description (appearance details, key features)
5. Save → now available across all shots in this project

**Per-Character Emotion:** In Multi-Shot mode, each character can have an **emotion setting
per scene**. The available emotions are:

| Emotion | Effect |
|---------|--------|
| Joy | Smiling, warm expression, positive energy |
| Fear | Wide eyes, tense posture, defensive body language |
| Surprise | Raised brows, open mouth, alert stance |
| Sadness | Downcast eyes, slumped posture, muted energy |

Set emotion per character per scene in the UI — this keeps expression changes out of the
prompt field and lets the model handle the subtlety of facial animation.

**@ tag rule — use exactly what the user provides, nothing more**
Only use @ tags for Elements the user has explicitly given you in this conversation.
If they give you `@Marcus` but no location or prop tags, write the location and props
as plain description. Never invent or assume @ tags for anything the user hasn't named.
Each @ tag the user gives you = they have that Element set up. Silence = they don't.

**No Elements provided — write everything as description:**
```
A woman with dark hair and a red coat walks through a narrow downtown alley at night.
She carries a worn leather briefcase. She stops under a streetlight, turns to camera.
```

**User provides @Sarah only — use it, describe the rest:**
```
@Sarah walks through a narrow downtown alley at night.
She carries a worn leather briefcase. She stops under a streetlight, turns to camera.
```

**User provides @Sarah, @DowntownAlley, @LeatherBriefcase — use all three:**
```
@Sarah walks through @DowntownAlley, carrying @LeatherBriefcase.
She stops under a streetlight, turns to camera.
```

**Key rule:** Match exactly what the user gives you. No more, no less.
Tags they give you = Element exists. Anything else = write it as description.

---

## Soul Cast — AI Actor Generation

Soul Cast is Cinema Studio 2.5's character generation system — create AI actors from
parameters instead of uploading photos. This is fundamentally different from Soul ID.

### Soul Cast vs Soul ID

| | Soul Cast | Soul ID |
|--|-----------|---------|
| Input | Parameter selection | 20+ photos of real person |
| Purpose | Generate AI actors from scratch | Maintain consistency of a known face |
| Photo required | No | Yes |
| Powered by | Nano Banana 2 | — |

### Soul Cast Parameter Categories (8 total)

| # | Category | Options |
|---|----------|---------|
| 1 | **Genre** | Action, Adventure, Comedy, Drama, Thriller, Horror, Detective, Romance, Sci-Fi, Fantasy, War, Western, Historical, Sitcom (14 options) |
| 2 | **Budget** | Production budget slider (in millions) — higher = refined blockbuster look, lower = raw/gritty |
| 3 | **Era** | Decade selection starting from 1900s — grounds character in correct time period |
| 4 | **Archetype** | Innocent, Everyman, Hero, Caregiver, Explorer, Rebel, Lover, Creator, Jester, Sage, Magician, Ruler (12 options) |
| 5 | **Identity** | Gender, race, age |
| 6 | **Physical Appearance** | Height, eye color, hair, facial hair, etc. |
| 7 | **Details** | Scars, tattoos, freckles, other imperfections |
| 8 | **Outfit** | Casual, Formal, High Fashion, Military, Sporty, Workwear, Vintage (7 styles) |

### Key Features

- Add up to **3 Soul Cast characters per keyframe** — choose from saved Elements or generate on the spot
- **"Save to elements"** button to reuse a specific Soul Cast actor across projects
- Every actor auto-generates a **backstory + character sheet** (personality traits, motivation, fear, flaw, strength)
- Designed to eliminate the "plastic/waxy" AI look — excels at **skin textures and emotions**
- Powered by the **Nano Banana 2** model under the hood

### Soul Cast Workflow

```
1. Open Cinema Studio → Navigate to Soul Cast panel
2. Set Genre + Era + Budget to establish the visual world
3. Select Archetype + Identity + Physical Appearance
4. Add Details (imperfections) + Outfit
5. Generate → Review backstory + character sheet
6. Save to Elements → Now available as @CharacterName across all shots
7. Repeat for additional characters (up to 3 per keyframe)
```

---

## Built-in Color Grading Suite

Cinema Studio 2.5 adds a post-production color grading suite applied to keyframes
**before** video generation — enabling unified visual cohesion across all clips.

### Controls

| Control | Effect |
|---------|--------|
| Color temperature | Warm ↔ cool shift |
| Contrast | Shadow/highlight separation |
| Saturation | Color intensity |
| Sharpness + effects | Detail enhancement |
| Highlights | Bright area control |
| Film grain | Analog texture overlay |
| Exposure | Overall brightness |
| Bloom | Highlight glow/diffusion |

### Workflow

1. Generate your keyframe image (Hero Frame or grid selection)
2. Click the keyframe → **"Colorgrade"** button
3. Adjust settings to taste
4. Apply — grade is baked into the keyframe before video generation
5. Repeat for each keyframe to maintain visual cohesion across the sequence

**Tip:** Grade your Hero Frame first, then match subsequent keyframes to it.
This is the post-production equivalent of a DIT (Digital Imaging Technician) on set.

---

## Optical Physics Engine

Cinema Studio's Image Mode gives you a full camera body + lens stack. These are the
**exact names from the UI** (previous versions had wrong names — these are corrected).

**Claude's job when building a Cinema Studio image prompt:** Always recommend a specific
optical stack — body + lens + focal length + aperture — with a one-line reason why.
Never leave the optical stack blank or say "choose based on preference." Make a call.

---

### Optical Stack Recommendations by Intent

Use the user's creative intent to select the stack. The most important signal is
**what the image needs to feel like** — not just the genre.

#### Portrait / Character Focus

| Feel | Body | Lens | Focal | Aperture | Why |
|------|------|------|-------|----------|-----|
| Warm, intimate, skin-flattering | Full-Frame Cine Digital | Warm Cinema Prime | 50mm | f/1.4 | Flattest most natural face rendering, creamy background separation |
| Artistic / swirling bokeh | Full-Frame Cine Digital | Swirl Bokeh Portrait | 50mm | f/1.4 | Distinctive background treatment isolates subject dramatically |
| Prestige / awards-film quality | Grand Format 70mm Film | Classic Anamorphic | 50mm | f/1.4 | Rich grain + horizontal bokeh = immediate cinematic credibility |
| Fashion / editorial sharp | Premium Large Format Digital | Clinical Sharp Prime | 50mm | f/4 | Maximum face detail, clinical modern look |
| Nostalgic / vintage character | Classic 16mm Film | 70s Cinema Prime | 50mm | f/1.4 | Grain + warmth + soft rendering = timeless feel |

#### Scene / Environment / Establishing

| Feel | Body | Lens | Focal | Aperture | Why |
|------|------|------|-------|----------|-----|
| Cinematic wide establishing | Studio Digital S35 | Compact Anamorphic | 14mm | f/4 | Industry-standard look, oval bokeh on background elements |
| Epic / spectacle | Grand Format 70mm Film | Classic Anamorphic | 14mm | f/4 | Scale + grain + strong lens character = instant epic quality |
| Documentary / real | Modular 8K Digital | Clinical Sharp Prime | 35mm | f/4 | Clean, high-DR, no optical character — feels captured not staged |
| Moody / atmospheric | Classic 16mm Film | Halation Diffusion | 35mm | f/4 | Grain + highlight glow creates organic atmosphere |
| Nature / landscape | Modular 8K Digital | Clinical Sharp Prime | 14mm | f/11 | Maximum depth, maximum detail, everything sharp |

#### Emotion / Tone-Driven

| Feel | Body | Lens | Focal | Aperture | Why |
|------|------|------|-------|----------|-----|
| Romance / dreamlike | Full-Frame Cine Digital | Halation Diffusion | 50mm | f/1.4 | Highlight glow + shallow focus = soft emotional warmth |
| Tension / suspense | Studio Digital S35 | Compact Anamorphic | 35mm | f/4 | Neutral but cinematic — lets the subject and lighting carry the mood |
| Dread / horror | Classic 16mm Film | Vintage Prime | 35mm | f/4 | Distortion + grain + flat rendering = unsettling realism |
| Energy / action | Studio Digital S35 | Compact Anamorphic | 35mm | f/4 | S35 + anamorphic = kinetic, industry-standard action feel |
| Melancholy / memory | Classic 16mm Film | Halation Diffusion | 50mm | f/1.4 | Softness + grain reads immediately as memory or longing |
| Surreal / abstract | Full-Frame Cine Digital | Creative Tilt Lens | 14mm | f/1.4 | Selective focus plane makes real scenes feel dreamlike or miniature |

#### Commercial / Functional

| Feel | Body | Lens | Focal | Aperture | Why |
|------|------|------|-------|----------|-----|
| Product / packshot | Premium Large Format Digital | Clinical Sharp Prime | 50mm | f/11 | Everything sharp, no optical distraction from the product |
| Product with lifestyle feel | Full-Frame Cine Digital | Warm Cinema Prime | 50mm | f/4 | Warm, flattering, some background separation — not clinical |
| Food / texture detail | Premium Large Format Digital | Extreme Macro | 50mm | f/4 | Maximum detail rendering for close-up texture work |
| Architecture / interior | Modular 8K Digital | Clinical Sharp Prime | 14mm | f/11 | Wide + sharp = every detail of the space visible |
| Fashion editorial | Premium Large Format Digital | Classic Anamorphic | 50mm | f/1.4 | High-end magazine look — sharp subject, cinematic background |

---

### How Claude Should Deliver the Output

Cinema Studio has two separate inputs:
- **UI dropdowns** — Camera body, Lens, Focal length, Aperture, Genre, Director Panel, Speed Ramp
- **Prompt field** — Scene description only. No camera/lens/aperture text goes here.

Claude must always output these as two clearly separated blocks:

**Block 1 — UI Settings (select these in Higgsfield before pasting the prompt)**
```
Camera:   Full-Frame Cine Digital
Lens:     Warm Cinema Prime
Focal:    50mm
Aperture: f/1.4
Genre:    Intimate
↳ Why: Flattest, most natural face rendering. Creamy background separation
       keeps all attention on the character without any lens distortion.
```

**Block 2 — Prompt (paste this into the Cinema Studio prompt field)**
```
[Scene description only — no camera, lens, aperture, or genre language here]
```

**Rule:** Never put camera body names, lens names, focal lengths, apertures, or genre
names inside the prompt text. They live in the UI, not the prompt field.

---

### Camera Body Reference

| Body | Character | Best for |
|------|-----------|----------|
| Premium Large Format Digital | Ultra-sharp, clinical modern | Commercial, fashion, product |
| Classic 16mm Film | Grain, texture, organic warmth | Drama, indie, period, horror |
| Modular 8K Digital | High dynamic range, clean | Nature, documentary, landscape, architecture |
| Full-Frame Cine Digital | Cinematic standard, versatile | Narrative, character, romance, drama |
| Studio Digital S35 | Super 35, industry standard | Action, thriller, genre, suspense |
| Grand Format 70mm Film | Epic scale, rich grain | Spectacle, prestige cinema, blockbuster |

### Lens Reference

| Lens | Effect | Best for |
|------|--------|----------|
| Creative Tilt Lens | Selective focus plane, miniature effect | Surreal, abstract, stylized |
| Compact Anamorphic | Oval bokeh, subtle flare | Cinematic standard, action, thriller |
| Halation Diffusion | Glow around highlights, dreamy | Romance, memory, soft drama, horror atmosphere |
| Extreme Macro | Hyper close-up detail | Product texture, food, insects, fine detail |
| 70s Cinema Prime | Warm, slightly soft vintage character | Period pieces, nostalgia, retro |
| Warm Cinema Prime | Golden warmth, skin-flattering | Portraits, drama, lifestyle |
| Swirl Bokeh Portrait | Swirling background blur | Artistic portrait, fashion editorial |
| Vintage Prime | Classic rendering, subtle distortion | Retro, lo-fi, character, horror |
| Classic Anamorphic | Strong flare, wide horizontal bokeh | Prestige, blockbuster, fashion |
| Clinical Sharp Prime | No aberration, maximum resolution | Commercial, technical, product, documentary |

### Focal Length Reference
`8mm` · `14mm` · `35mm` · `50mm`

- **8mm** — Ultra-wide, immersive distortion. Action POV, environment, disorientation
- **14mm** — Wide, environmental, scale. Establishing shots, landscape, architecture
- **35mm** — Natural human field of view. Documentary, street, two-shots, candid
- **50mm** — Classic portrait compression. Character close-ups, product, single subject

### Aperture Reference
- **f/1.4** — Shallow depth of field. Subject sharp, background creamy bokeh. Intimacy, focus, emotion
- **f/4** — Balanced. Subject sharp, background slightly soft. Most versatile, natural look
- **f/11** — Deep depth of field. Everything sharp front to back. Product, landscape, architecture

---

## Director Panel — 18 Camera Movements

**⚠ Use ONLY these exact movement names in Cinema Studio output.** General cinematic terms like "Crane Down", "Whip Pan", "FPV Drone", "Crash Zoom" etc. (from `vocab.md`) are valid for standard video generation and image prompts **outside** Cinema Studio, but they are NOT Director Panel options. Inside Cinema Studio, map to the closest equivalent (e.g., Crane Down → **Jib Down**, Crane Up → **Jib Up**).

All movements available in Cinema Studio's Director Panel:

| Movement | Description | Best for |
|----------|-------------|----------|
| Static | Locked off, no movement | Dialogue, tension, composition |
| Handheld | Organic shake, documentary feel | Urgency, realism, action |
| Zoom Out | Focal length pulls back | Revelation, isolation |
| Zoom In | Focal length pushes in | Intensity, focus on subject |
| Camera Follows | Tracks subject movement | Chase, pursuit, accompaniment |
| Pan Left | Horizontal sweep left | Reveal, environment scan |
| Pan Right | Horizontal sweep right | Reveal, environment scan |
| Tilt Up | Vertical sweep up | Scale, aspiration, reveal |
| Tilt Down | Vertical sweep down | Weight, consequence, ground |
| Orbit Around | 360° around subject | Isolation, drama, examination |
| Dolly In | Physical push toward subject | Emotional intimacy |
| Dolly Out | Physical pull from subject | Distance, context reveal |
| Jib Up | Camera rises on arm | Scale, context, god's eye |
| Jib Down | Camera descends on arm | Grounding, arrival |
| Drone Shot | Aerial movement | Landscape, scale, geography |
| Dolly Left | Lateral push left | Parallel tracking, reveal |
| Dolly Right | Lateral push right | Parallel tracking, reveal |
| 360 Roll | Camera rolls on axis | Disorientation, stylized |
| Auto | Model selects best movement | When unsure |

---

## Speed Ramp

Controls temporal feel of the shot. Set per-scene in Cinema Studio.

> **⚠ Speed Ramp options differ between versions. Use ONLY the table for the version the user specified. Never output a 2.5 ramp name in 3.0 output or vice versa.**

### Cinema Studio 2.5 Speed Ramps (6 modes)

| Mode | Effect | Best for |
|------|--------|----------|
| Linear | Consistent speed throughout | Standard, natural |
| Slow Mo | Reduced playback speed | Impact moments, emotion |
| Speed Up | Accelerated playback | Montage, energy, passage of time |
| Impact | Fast → sudden slow at key moment | Action, hits, reveals |
| Auto | Model selects based on content | When unsure |
| Custom | Draw your own speed curve | Precise creative control |

**Custom curve:** Blue line with draggable nodes. Pull up = slow down, pull down = speed up.
Left = beginning of clip, right = end.

**2.5-only values — NEVER use in 3.0 output:** Linear, Slow Mo, Speed Up, Impact, Custom

### Cinema Studio 3.0 Speed Ramps (7 modes)

| Mode | Effect | Best for |
|------|--------|----------|
| Auto | Model selects based on content | When unsure |
| Slow-mo | Reduced playback speed | Impact moments, emotion |
| Ramp Up | Gradual acceleration | Building energy, montage |
| Flash In | Fast start → ease to normal | Dramatic entrances, openings |
| Flash Out | Normal → sudden snap acceleration | Launches, exits, explosive action |
| Bullet Time | Ultra-slow at key moment, normal around it | Action hits, reveals, hero beats |
| Hero Moment | Slow build → dramatic pause → release | Character reveals, power moves |

**3.0-only values — NEVER use in 2.5 output:** Ramp Up, Flash In, Flash Out, Bullet Time, Hero Moment

---

## Genre Selection

> **⚠ Genre lists differ between versions. Use ONLY the genres for the version the user specified.**

### Cinema Studio 2.5 Genres (8)

`General` · `Action` · `Horror` · `Comedy` · `Western` · `Suspense` · `Intimate` · `Spectacle`

Genre affects lighting defaults, color grading baseline, and motion style suggestions.
You can always override with explicit prompt language — genre is a starting point.

| Genre | Lighting default | Color tendency | Motion style |
|-------|-----------------|----------------|--------------|
| General | Neutral | Balanced | Varies |
| Action | Hard, high contrast | Desaturated, cool | Dynamic |
| Horror | Low key, harsh shadows | Desaturated, teal/green tint | Slow or sudden |
| Comedy | Bright, even | Warm, saturated | Light, energetic |
| Western | Golden hour / dusty | Warm amber | Steady, wide |
| Suspense | Low key, motivated | Cold, muted | Slow build |
| Intimate | Soft, warm | Warm, skin-flattering | Gentle |
| Spectacle | Dramatic, high contrast | Bold, saturated | Epic, sweeping |

**2.5-only genres — NEVER use in 3.0 output:** Western, Suspense, Intimate, Spectacle

### Cinema Studio 3.0 Genres (7)

`General` · `Action` · `Horror` · `Comedy` · `Noir` · `Drama` · `Epic`

**3.0-only genres — NEVER use in 2.5 output:** Noir, Drama, Epic

---

## Shot Modes

### Single Shot
Standard generation — one prompt, one clip. Same as regular Higgsfield but with the
optical stack and Director Panel applied.

### Multi-Shot Auto
Describe the full sequence in one prompt. Cinema Studio breaks it into shots automatically.
Good for: rough sequences, exploration, when you don't need per-shot control.

```
Example: "A woman walks into a bar, sits down, orders a drink. Bartender slides it over.
She takes a sip and stares at her reflection in the mirror behind the bottles."
→ Cinema Studio Auto generates: Establishing shot / Walk to seat / Order / Drink delivery / Reflection closeup
```

### Multi-Shot Manual
Full per-scene control. Up to 6 scenes, each with its own:
- Prompt
- Camera movement (Director Panel)
- Speed Ramp
- Duration

**⚠ 12-Second Total Runtime Cap:** The combined duration of all scenes in a Multi-Shot
sequence cannot exceed **12 seconds total**. Plan your per-scene durations to stay within
this limit (e.g., 6 scenes × 2s each, or 4 scenes × 3s, or 3 scenes × 4s).

**Cost transparency:** Multi-Shot Manual with 4 variations = **24 generations total** (6 scenes × 4 variations). Plan credits accordingly.

**Multi-Shot Manual workflow:**
1. Scene 1: Establishing shot — wide, sets location
2. Scene 2: Character introduction — medium, shows protagonist
3. Scene 3: Action beat — closer, movement
4. Scene 4: Reaction — close-up, emotion
5. Scene 5: Consequence / turn — medium or wide
6. Scene 6: Resolution / button — varies

---

## Reference Anchor System

The Reference Anchor locks character geometry (facial structure, proportions, costume silhouette)
across all shots in a sequence — preventing the character drift that happens in standard generation.

**Setup:**
1. Upload a clear, well-lit reference photo of your character
2. Cinema Studio generates an anchor from it
3. Every subsequent shot in the project references this anchor
4. Combine with Soul ID for full face + geometry lock

**Best practices:**
- Use a front-facing, neutral expression photo for the anchor
- Avoid glasses, hats, or accessories in the anchor image if they won't always be present
- One Reference Anchor per character — add multiple if you have a cast
- The anchor persists across the whole Cinema Studio project

---

## Hero Frame

A Hero Frame is a key image you generate before committing to video — it defines the
visual tone, lighting, color, and composition of your sequence.

**Why it matters:** Generating a Hero Frame first costs ~1 credit. Adjusting the video
after generation costs full video credits. Get the look right on the image first.

**Hero Frame workflow:**
1. Describe your opening shot with full optical stack
2. Generate as image (Soul 2.0 or Nano Banana 2)
3. Review: Is the lighting right? Color? Character look?
4. Iterate on image until it's exactly right
5. Use as the first frame / style reference for video generation

**Hero Frame as style lock:**
Once you have a Hero Frame you love, use it as a reference upload for your first video
shot. Describe the match in the prompt as atmosphere and lighting language — not as
camera/genre instructions (those go in the UI settings):
```
The same overcast midday light as the reference image.
Muted, desaturated tones. The character enters from the left side of frame.
```

---

## Higgsfield Popcorn — Storyboard Integration

Popcorn is Higgsfield's storyboard tool. Use it to plan a sequence visually before
committing to Cinema Studio generation.

**Popcorn → Cinema Studio workflow:**
1. Open Popcorn → describe your story / scene breakdown
2. Popcorn generates a visual storyboard with shot descriptions
3. Review shot order, camera angles, key moments
4. Export storyboard → import into Cinema Studio as shot list
5. Configure each shot: optical stack, Director Panel, Speed Ramp
6. Generate in Multi-Shot Manual mode using the storyboard as your script

**When to use Popcorn first:**
- Any sequence longer than 3 shots
- When you're not sure of the shot order
- Client or collaborator needs to approve the structure before generation
- Complex action sequences with many camera angles

---

## Keyframe Interpolation — Start/End Frames

Define exactly where a shot begins and ends. Eliminates morphing artifacts that happen
when the model guesses the transition.

**Setup:**
- **Start Frame**: Upload or generate the first frame of the shot
- **End Frame**: Upload or generate the last frame of the shot
- Cinema Studio interpolates the motion between them

**Best uses:**
- Precise character entrances / exits
- Object reveals with exact start and end position
- Match cuts between shots (end frame of shot A = start frame of shot B)
- Controlled camera moves where position must be exact

---

## 3D Mode — Gaussian Splatting

Cinema Studio can build a **3D version of any generated image** using Gaussian splatting.
Once active, you can move inside the frame — shift perspective, orbit the scene, and find
a composition that didn't exist in the original 2D generation.

**How it works:**
1. Generate an image in Cinema Studio (any model, any optical stack)
2. Activate 3D Mode on the generated image
3. Cinema Studio reconstructs the scene as a 3D Gaussian splat
4. Use the virtual camera to move freely — orbit, push in, shift angle
5. Capture your preferred composition as a new frame
6. Use that frame as a start frame for video generation

**When to use 3D Mode:**
- You love the generation but want a different camera angle
- You need a reverse shot or over-the-shoulder from the same scene
- You're building a virtual camera move through a static scene
- You want to explore parallax and depth before committing to video

**Workflow tip:** Generate a Hero Frame → enter 3D Mode → find 2–3 different angles →
use each as start frames for different shots in your Multi-Shot Manual sequence. One
generation becomes multiple shots.

---

## Grid Generation — Batch Variations

Instead of generating one image at a time, Cinema Studio can produce **2×2, 3×3, or 4×4
grids** — up to 16 variations from a single generation, charged as one credit.

**Grid sizes:**
| Grid | Variations | Cost |
|------|-----------|------|
| 2×2 | 4 images | 1 generation credit |
| 3×3 | 9 images | 1 generation credit |
| 4×4 | 16 images | 1 generation credit |

**When to use Grid Generation:**
- Exploring compositions — generate 16 options, pick the best one
- Character sheet creation — multiple poses/angles in one pass
- A/B testing visual direction before committing to video
- Cost-efficient iteration — spend 1 credit, get up to 16 options

**Workflow with grids:**
1. Write your prompt + configure optical stack
2. Select grid size (2×2 through 4×4)
3. Generate — all variations appear grouped together
4. Select the best variation(s)
5. Use as Hero Frame, start frame, or enter 3D Mode on any individual result

---

## Resolution Settings

Cinema Studio supports explicit resolution control for image generation:

| Setting | Resolution | Best for |
|---------|-----------|----------|
| 1K | 1024px | Fast iteration, concept exploration |
| 2K | 2048px | Standard quality, most workflows |
| 4K | 4096px | Final delivery, print, hero assets |

**Rule of thumb:** Start at 1K–2K for exploration and grid generation. Switch to 4K only
for your final selected composition. Higher resolution = longer generation time and more
credits.

---

## Frame Extraction Loop — Build, Animate, Extract, Repeat

One of Cinema Studio 2.5's most powerful workflows is the **frame extraction loop**. You
can extract the **start frame or end frame** from any generated video and feed it back into
the image workflow — creating an iterative creative cycle.

**The loop:**
```
1. GENERATE IMAGE → Hero Frame or grid selection
2. ANIMATE        → Turn image into video (any model)
3. EXTRACT FRAME  → Pull the start or end frame from the video
4. FEED BACK      → Use extracted frame as a new start image
5. REPEAT         → Animate again from the new starting point
```

**Why this matters:**
- The end frame of a video often produces compositions you'd never prompt directly
- Extracted frames carry the model's physics — natural motion blur, weight, momentum
- Chaining extract → animate creates organic visual evolution
- End frame of shot A becomes start frame of shot B — seamless continuity

**Best uses:**
- Building long sequences that feel connected without multi-shot mode
- Discovering unexpected compositions from model-generated endpoints
- Creating transformation sequences (character aging, day-to-night, etc.)
- Match-cutting between scenes using extracted frames as anchors

---

## Object & Person Insertion

Cinema Studio 2.5 can **insert characters and objects into a scene** that weren't present
in the original start frame. This was essentially impossible before — the model would
ignore new subjects or break the scene trying to add them.

**How it works:**
1. Generate or upload your base scene (the environment)
2. In the prompt, describe the character or object entering the scene
3. Cinema Studio composites the new subject into the existing environment
4. The insertion respects lighting, perspective, and scale of the original scene

**Best for:**
- Adding a character walking into an establishing shot
- Placing props or vehicles into an existing environment
- Building up scene complexity across multiple generations
- "What if" exploration — same scene with different subjects

**Prompt pattern for insertion:**
```
[Describe the existing scene briefly]. A man in a dark overcoat enters from the left
side of frame, walking toward the center. He carries a briefcase.
```

**Tip:** The more specific you are about the entry point (left, right, background,
foreground) and the action, the cleaner the insertion.

---

## Clustering — Automatic Generation Grouping

All generations from the same prompt are **automatically clustered** (grouped together) in
Cinema Studio's interface. This means:

- Every variation from a grid generation stays in one visual group
- Iterative re-generations of the same prompt are easy to compare
- Long projects stay organized without manual folder management
- You can quickly scan clusters to pick the best result from each prompt

**Tip:** Use clustering to your advantage — generate multiple variations of each key shot,
then pick winners from each cluster before assembling the final sequence.

---

## Cinema Studio Output Format

**Core rule:** Everything selectable in the Higgsfield UI stays out of the prompt.
The prompt field is for scene description only — pure visual storytelling language.

### What goes where

| Belongs in UI (dropdowns) | Belongs in Prompt field |
|--------------------------|------------------------|
| Camera body | Character appearance and action |
| Lens | Environment and atmosphere |
| Focal length | What happens in the scene |
| Aperture | Lighting and mood description |
| Genre | Emotion and tone |
| Director Panel movement | Everything the eye sees |
| Speed Ramp | |
| Duration | |

---

### IMAGE MODE Output Format (Cinema Studio 2.5 only)

```
━━━ UI SETTINGS (select in Higgsfield) ━━━━━━━━━━━━━━━━━━
Camera:   [body name]
Lens:     [lens name]
Focal:    [focal length]
Aperture: [aperture]
↳ Why: [one sentence — what this stack gives the image and why]

━━━ PROMPT (paste into Cinema Studio) ━━━━━━━━━━━━━━━━━━━
[Scene description only. No camera/lens/aperture language.]
```

**Image Mode example:**
```
━━━ UI SETTINGS (select in Higgsfield) ━━━━━━━━━━━━━━━━━━
Camera:   Grand Format 70mm Film
Lens:     Classic Anamorphic
Focal:    50mm
Aperture: f/1.4
↳ Why: 70mm grain + anamorphic flare gives instant prestige cinema quality.
       f/1.4 puts the harbour out of focus, keeping all weight on the detective.

━━━ PROMPT (paste into Cinema Studio) ━━━━━━━━━━━━━━━━━━━
A weathered detective stands at the edge of a rain-soaked harbour dock at night.
An old leather briefcase sits at his feet, open, papers scattered by the wind.
He stares at the horizon, collar turned up against the driving rain.
Harbour lights fracture on the black water below.
```

---

### SINGLE SHOT Video Output Format (Cinema Studio 2.5)

```
━━━ UI SETTINGS (select in Higgsfield) ━━━━━━━━━━━━━━━━━━
Genre:      [genre]
Movement:   [Director Panel movement]
Speed Ramp: [mode]
Duration:   [seconds]

━━━ PROMPT (paste into Cinema Studio) ━━━━━━━━━━━━━━━━━━━
[Scene description only. No movement, genre, speed ramp, or duration language.]
```

**Single Shot example:**
```
━━━ UI SETTINGS (select in Higgsfield) ━━━━━━━━━━━━━━━━━━
Genre:      Suspense
Movement:   Dolly Out
Speed Ramp: Slow Mo
Duration:   8s

━━━ PROMPT (paste into Cinema Studio) ━━━━━━━━━━━━━━━━━━━
A weathered detective stands at the edge of a rain-soaked harbour dock at night.
An old leather briefcase sits at his feet, open, papers scattered by the wind.
He stares at the horizon, collar turned up against the driving rain.
Harbour lights fracture on the black water below.
He reaches down and slowly closes the briefcase.
```

---

### MULTI-SHOT AUTO Video Output Format (Cinema Studio 2.5)

Same structure as Single Shot — one UI settings block, one prompt. The user describes
the full scene in the prompt and Cinema Studio breaks it into shots automatically.

```
━━━ UI SETTINGS (select in Higgsfield) ━━━━━━━━━━━━━━━━━━
Genre:      [genre]
Movement:   [Director Panel movement — or Auto if varied]
Speed Ramp: [mode]
Duration:   [total seconds]

━━━ PROMPT (paste into Cinema Studio) ━━━━━━━━━━━━━━━━━━━
[Full scene description. Let Cinema Studio break it into shots.
No movement, genre, speed ramp, or duration language in here.]
```

**Multi-Shot Auto example:**
```
━━━ UI SETTINGS (select in Higgsfield) ━━━━━━━━━━━━━━━━━━
Genre:      Suspense
Movement:   Auto
Speed Ramp: Linear
Duration:   15s

━━━ PROMPT (paste into Cinema Studio) ━━━━━━━━━━━━━━━━━━━
A weathered detective pushes open the door of a rain-soaked bar and steps inside.
He scans the room — empty except for a bartender polishing glasses at the far end.
He walks slowly to the bar and sits down. The bartender slides a drink without a word.
The detective picks it up, stares at his reflection in the mirror behind the bottles.
He sets it down without drinking.
```

---

### MULTI-SHOT MANUAL Video Output Format (Cinema Studio 2.5)

One UI settings block per scene. One prompt per scene. Six scenes = six pairs.
Each scene is fully self-contained — the user configures and pastes them one at a time.

```
━━━ SCENE 1 — [short scene title] ━━━━━━━━━━━━━━━━━━━━━━━
UI SETTINGS
  Genre:      [genre]
  Movement:   [movement]
  Speed Ramp: [mode]
  Duration:   [seconds]

PROMPT
[Scene 1 description only.]

━━━ SCENE 2 — [short scene title] ━━━━━━━━━━━━━━━━━━━━━━━
UI SETTINGS
  Genre:      [genre]
  Movement:   [movement]
  Speed Ramp: [mode]
  Duration:   [seconds]

PROMPT
[Scene 2 description only.]

[...continue for each scene]
```

**Multi-Shot Manual example — 3 scenes (same pattern scales to 6):**

```
━━━ SCENE 1 — Arrival ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UI SETTINGS
  Genre:      Suspense
  Movement:   Handheld
  Speed Ramp: Linear
  Duration:   5s

PROMPT
A weathered detective steps through the door of a dimly lit bar.
Rain drips from his coat. He pauses, eyes adjusting to the dark.
The bar is nearly empty. A jukebox plays quietly in the corner.

━━━ SCENE 2 — The Walk ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UI SETTINGS
  Genre:      Suspense
  Movement:   Camera Follows
  Speed Ramp: Linear
  Duration:   4s

PROMPT
He walks slowly down the length of the bar, boots on wet floorboards.
A bartender watches without expression. One other patron doesn't look up.
He reaches the end stool and sits down deliberately.

━━━ SCENE 3 — The Mirror ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UI SETTINGS
  Genre:      Suspense
  Movement:   Dolly In
  Speed Ramp: Slow Mo
  Duration:   6s

PROMPT
A glass of whiskey sits untouched on the bar in front of him.
He stares at his own reflection in the mirror behind the bottles.
His jaw tightens. He picks up the glass, holds it, sets it back down.
```

---

## Cinema Studio 3.0 Output Formats

**3.0 does NOT have:** Camera body, Lens, Focal length, Aperture, Color grading, 3D Mode, Grid generation. Never include these in 3.0 output.

**3.0 has:** Genre (7: General, Action, Horror, Comedy, Noir, Drama, Epic), Director Panel, Speed Ramp (7: Auto, Slow-mo, Ramp Up, Flash In, Flash Out, Bullet Time, Hero Moment), Duration (up to 15s), Audio (On/Off native stereo), Smart shot control, 21:9 ultrawide.

**Version guard — values that do NOT exist in 3.0 (never output these):**
- Speed Ramp: ~~Linear~~, ~~Slow Mo~~, ~~Speed Up~~, ~~Impact~~, ~~Custom~~
- Genre: ~~Western~~, ~~Suspense~~, ~~Intimate~~, ~~Spectacle~~
- UI fields: ~~Camera body~~, ~~Lens~~, ~~Focal length~~, ~~Aperture~~, ~~Color grading~~, ~~3D Mode~~, ~~Grid generation~~

---

### IMAGE MODE Output Format (Cinema Studio 3.0)

No optical stack in 3.0. Image output uses Soul Cast modes only.

```
━━━ UI SETTINGS (select in Higgsfield) ━━━━━━━━━━━━━━━━━━
Soul Cast Mode: [General / Character / Location]
Genre:          [genre]
↳ Why: [one sentence — what this combination gives the image and why]

━━━ PROMPT (paste into Cinema Studio) ━━━━━━━━━━━━━━━━━━━
[Scene description only. No camera/lens/aperture language — these don't exist in 3.0.]
```

---

### SINGLE SHOT / SMART Video Output Format (Cinema Studio 3.0)

```
━━━ UI SETTINGS (select in Higgsfield) ━━━━━━━━━━━━━━━━━━
Genre:      [genre — General, Action, Horror, Comedy, Noir, Drama, or Epic]
Shot Mode:  [Smart / Custom]
Movement:   [Director Panel movement — or Smart for auto camera planning]
Speed Ramp: [Auto / Slow-mo / Ramp Up / Flash In / Flash Out / Bullet Time / Hero Moment]
Duration:   [up to 15s]
Audio:      [On / Off]

━━━ PROMPT (paste into Cinema Studio) ━━━━━━━━━━━━━━━━━━━
[Scene description only. Use @ to reference uploaded images/video/audio.
No movement, genre, speed ramp, or duration language in here.]
```

**Single Shot 3.0 example:**
```
━━━ UI SETTINGS (select in Higgsfield) ━━━━━━━━━━━━━━━━━━
Genre:      Action
Shot Mode:  Smart
Movement:   Jib Down
Speed Ramp: Slow-mo
Duration:   5s
Audio:      On

━━━ PROMPT (paste into Cinema Studio) ━━━━━━━━━━━━━━━━━━━
@CypressLookout packed with cars and people at night. @R34GTR parked
prominently in the center, @240SX and @AE86 visible nearby. Crowd
gathered between the cars, neon underglow reflecting on wet pavement.
City skyline glowing across the water in the distance. Engine noise,
crowd murmur, tension in the air.
```

---

### MULTI-SHOT MANUAL Video Output Format (Cinema Studio 3.0)

Same per-scene structure as 2.5 but with 3.0 options. Up to 6 scenes, 15s max total.

```
━━━ SCENE 1 — [short scene title] ━━━━━━━━━━━━━━━━━━━━━━━
UI SETTINGS
  Genre:      [genre]
  Movement:   [movement]
  Speed Ramp: [Auto / Slow-mo / Ramp Up / Flash In / Flash Out / Bullet Time / Hero Moment]
  Duration:   [seconds]
  Audio:      [On / Off]

PROMPT
[Scene 1 description only. Use @ for references.]
```

---

## ⚠ Prompt Character Limit — 512 Characters

Cinema Studio has a **hard 512-character limit** on the prompt field in **both 2.5 and 3.0**. However, how those characters are consumed differs by version.

### Cinema Studio 2.5 Character Budget

2.5 uses **@ Element chips** (Characters, Locations, Props). Each chip consumes roughly **80–100 hidden characters** for its internal ID and reference metadata.

- Max **2 @ Element tags per prompt** — each tag eats ~80–100 hidden chars
- Keep visible text under **~250 characters** when using 2 @ tags
- Keep visible text under **~350 characters** when using 1 @ tag
- Keep visible text under **~450 characters** when using 0 @ tags
- If a prompt is rejected, remove words — never assume it's a bug

### Cinema Studio 3.0 Character Budget

3.0 uses **@ references** (uploaded images, video clips, audio clips — up to 12 total). The @ reference system is structurally different from 2.5's Element chips. References are attached as media inputs rather than inline metadata, so they may consume **less hidden character space** than 2.5's Element chips.

- The 512-character hard limit still applies
- With @ references attached, keep visible text under **~350–400 characters** as a safe starting point
- With no @ references, you can use closer to the full **~450–500 characters**
- If a prompt is rejected for length, trim visible text first — do not assume it's a bug
- 3.0 prompts can be **more descriptive** than 2.5 prompts since @ references leave more room for text

---

## @ Element Persistence Across Scenes

@ Elements added in **Scene 1 persist across all subsequent scenes** in Multi-Shot Manual.
You do NOT need to re-add @ tags in every scene prompt.

**Recommended pattern for multi-character sequences:**
1. **Scene 1:** Use @ Elements to establish all characters (e.g. `@HERO and @badguy3`)
2. **Scenes 2–6:** Reference characters by **visual description only** (e.g. "the man in
   the leather jacket") — the Reference Anchor keeps their appearance locked

**Why this works:** The @ Elements in Scene 1 lock character geometry into the Reference
Anchor. Subsequent scenes inherit that lock automatically. Using @ tags again in later
scenes forces the model to re-process the reference data, which competes with action
prompts and causes issues like character swaps, broken choreography, and missed actions.

---

## Prompting Best Practices

For the full Pre-Prompt Checklist, one-action-per-scene rule, and fast motion trick, see `higgsfield-prompt`. Cinema Studio–specific additions:

- Select camera movement from Director Panel presets (not prompt text)
- Select genre from Cinema Studio genre options (not prompt text)
- Use @ Elements for character identity; keep prompts to action and scene description only

---

## Fight Scene Rules (Tested)

Two-character fight sequences are among the hardest things to generate in Cinema Studio.
These rules come from extensive real-world testing.

### What the AI CAN render in fight scenes
- Two people standing/facing each other ✓
- General fighting/struggling energy ✓
- One person pinned against a wall ✓
- One person falling to the ground ✓
- Someone walking away ✓
- Sound effects matching the action ✓

### What the AI CANNOT reliably render
- A specific punch connecting with a face ✗
- Kicks (roundhouse, front kick, etc.) ✗
- Complex martial arts choreography ✗
- Precise cause-and-effect sequences (hit → stumble) ✗
- Prop-based combat (trays, carts, objects as weapons) ✗
- Grappling at close range (often renders as embracing) ✗

### Character Swap Problem

When two @ Elements are used in the same action prompt, the AI frequently **swaps
which character is the hero and which is the villain.** The first character mentioned
tends to get assigned the "protagonist" role regardless of the prompt's intent.

**Fixes:**
- Use @ Elements only in **static/slow scenes** (standoff, pinned, walk away)
- Use **plain text** for **action scenes** where choreography matters
- If using @ tags, always put the hero character **first** in the prompt
- End each scene by stating who is where, to anchor positions

### Fight Sequence Template (Multi-Shot Manual)

```
Scene 1 (@ Elements) — Standoff: Lock in characters, tension build
Scene 2 (Plain text) — First exchange: Describe fighting energy, not specific moves
Scene 3 (Plain text) — Escalation: Bodies slamming, intensity rising
Scene 4 (@ Elements) — Close-up moment: Pin against wall, intense stare
Scene 5 (Plain text) — The finish: Someone goes down
Scene 6 (@ Elements) — Resolution: Hero walks away from camera
```

Alternate @ Element scenes (for character faces) with plain text scenes (for action).
The viewer's brain fills in character continuity between cuts — that's how real film
editing works.

---

## Model Selection for Cinema Studio

Different models perform differently inside Cinema Studio's environment:

| Use case | Recommended model |
|----------|------------------|
| Character-driven drama sequence | Kling 3.0 |
| Clone character from reference footage | Kling 3.0 Omni |
| Epic scale / action multi-shot | Sora 2 |
| Artistic / stylized sequence | Wan 2.6 |
| Nature / environment sequence | Veo 3 / Veo 3.1 |
| Fast iteration on sequence | Kling 2.5 Turbo |
| Hero Frame image generation | Soul 2.0 / Nano Banana 2 |

---

## Quick Decision — Cinema Studio vs Other Tools

| Need | Use |
|------|-----|
| Single clip, no sequence | Standard generation |
| 2–6 shot sequence, character consistent | Cinema Studio — Multi-Shot Manual |
| Sequence but don't need per-shot control | Cinema Studio — Multi-Shot Auto |
| Don't know shot order yet | Popcorn first → Cinema Studio |
| Need motion graphics / text animation | Vibe Motion (not Cinema Studio) |
| Edit existing footage | Kling O1 Video Edit (not Cinema Studio) |
| Just need audio added to a clip | Lipsync Studio / Kling 3.0 |

---

> **Identity vs. Motion:** In Cinema Studio, identity goes in the @ Element definition (or
> Soul Cast parameters); motion goes in the prompt field. Never put face/clothing descriptors
> in the prompt when @ Elements are active. See `higgsfield-prompt` and `higgsfield-soul`
> for the full separation rule.

> **Negative constraints:** For Cinema Studio–specific artifacts (prompt rejected, @ Element
> character swap, 3D Mode holes, optical stack mismatch) and all general artifacts, see
> `../shared/negative-constraints.md`.

---

## Cinema Studio 3.0 (Business/Team Plan)

> **Plan requirement:** Cinema Studio 3.0 is available exclusively on **Business and Team plans**. Free and individual plan users should use Cinema Studio 2.5, which remains fully supported.

> **Version toggle:** Cinema Studio 2.5 and 3.0 coexist on the platform. Switch between them using the version selector in the upper-right corner of the Cinema Studio UI.

### What's Different in 3.0

Cinema Studio 3.0 is a separate generation engine from 2.5. Key differences:

- **Higher max duration:** 15s (vs 2.5's 12s)
- **Lower video resolution (for now):** Video capped at 720p (vs 2.5's 1080p); Image up to 4K in Character/Location modes (General mode capped at 2K)
- **Native audio:** Audio generated simultaneously with video via unified multimodal architecture — dual-channel stereo, not post-processed
- **Smart shot control:** Model auto-plans camera language based on genre and scene description
- **Ultrawide aspect ratio:** 21:9 added (not available in 2.5)
- **No optical physics engine:** 2.5's camera body + lens stack is not available in 3.0
- **No color grading suite:** 2.5's built-in grading is not available in 3.0
- **No 3D Mode / Grid Generation:** These 2.5 features are not available in 3.0

> **Resolution note:** Cinema Studio 3.0 video resolution (720p) may increase. For 1080p video, use Cinema Studio 2.5. Image resolution in 3.0 varies by mode: Character/Location support 4K, General is capped at 2K.

### Cinema Studio 3.0 Quick Specs

See the comparison table at the top for full 2.5 vs 3.0 differences. Key 3.0-specific details:

- **Video:** up to 15s, 720p (may increase), 48 credits/generation
- **Image (Soul Cast 3.0):** up to 4K (Character/Location) · 2K (General), 0.125 credits
- **Genres (7):** General, Action, Horror, Comedy, Noir, Drama, Epic
- **Speed Ramp (7):** Auto, Slow-mo, Ramp Up, Flash In, Flash Out, Bullet Time, Hero Moment
- **Aspect Ratios (7):** Auto, 1:1, 3:4, 9:16, 4:3, 16:9, 21:9
- **Audio:** On/Off — natively generated alongside video (dual-channel stereo)
- **Shot Control:** Smart (auto camera planning) or Custom multi-shot (up to 6 scenes, 15s total)

### Input Limits (@ References)

| Type | Max Count | Formats | Size/Duration Limit |
|------|-----------|---------|---------------------|
| Images | 9 | jpeg, png, webp, bmp | — |
| Video clips | 3 | mp4, mov | Combined ≤15s total |
| Audio clips | 3 | mp3, wav | Combined ≤15s total |
| **Total files** | **≤12** | | |

### @ Reference Patterns for Cinema Studio 3.0

**Character identity (first frame):**
@Image1 as the main character. She walks through the market, picking up fruit and examining it closely.

**Environment / last frame:**
@Image1 as the starting environment. @Image2 as the destination. Camera tracks through a doorway transitioning from the first space to the second.

**Motion reference / camera cloning:**
Match the camera movement from @Video1. A dancer performs on a rooftop at sunset, wind catching her dress.

**Audio reference (BGM / dialogue / tone):**
Audio @Audio1 plays exactly as uploaded from 0s to end. Do not modify or replace the audio content. Voiceover tone references @Video1.

**Multi-image spatial mapping:**
@Image1 as first frame, @Image2 as top of frame, @Image3 as left side. Camera slowly pans right, revealing the full scene.

**Video extension:**
Extend @Video1 by 5s. The character continues walking, reaching the edge of the cliff and looking out over the valley.

**Ad recreation:**
Mimic @Video1's shot design, pacing, and transitions. Replace all products with @Image1. Match the lighting and camera angles.

**Outfit transformation:**
@Image1 as the character in casual clothes. @Image2 as the same character in formal attire. A quick-cut transformation sequence with fabric particles.

**One-shot continuity:**
@Image1 first frame, @Image2 midpoint, @Image3 final frame. No cuts throughout, one continuous shot tracking the subject across all three compositions.

### When to Use 3.0 vs 2.5

| Need | Recommendation |
|------|---------------|
| Highest video resolution (1080p) | Cinema Studio 2.5 |
| 4K images (Character/Location) | Cinema Studio 3.0 (Business/Team) |
| Longer duration (up to 15s) | Cinema Studio 3.0 (Business/Team) |
| Native audio with video | Cinema Studio 3.0 (Business/Team) |
| Optical physics (lens, sensor) | Cinema Studio 2.5 |
| Color grading suite | Cinema Studio 2.5 |
| 3D Mode / Grid Generation | Cinema Studio 2.5 |
| Ultrawide 21:9 aspect ratio | Cinema Studio 3.0 (Business/Team) |
| Smart auto-camera planning | Cinema Studio 3.0 (Business/Team) |
| Free/Individual plan | Cinema Studio 2.5 |

## Related skills
- `higgsfield-prompt` — MCSLA formula, Identity/Motion separation, 512-char awareness
- `higgsfield-soul` — Soul ID + Soul Cast character consistency
- `higgsfield-pipeline` — Full production pipeline (Cinema Studio is one stage)
- `higgsfield-camera` — Standard camera presets (Cinema Studio uses Director Panel instead)
- `higgsfield-style` — Visual styles (Cinema Studio has built-in color grading)
- `higgsfield-models` — Model selection within Cinema Studio
- `higgsfield-audio` — Audio design for Kling 3.0 sequences
- `templates/` — Genre-specific annotated templates
