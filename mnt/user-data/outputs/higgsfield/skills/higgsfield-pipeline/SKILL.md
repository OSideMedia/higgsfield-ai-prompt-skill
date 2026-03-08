---
name: higgsfield-pipeline
description: >
  Use when the user wants to create a complete multi-shot video, asks how to chain
  Higgsfield tools together, wants to build a short film or branded content series,
  asks "what's the full workflow", needs to connect Popcorn → image → video → Recast
  → audio → assembly, or wants to understand how the platform works as a production
  system rather than isolated tools.
user-invocable: true
tags: [higgsfield, pipeline, workflow, chain, production, multi-shot, short-film, popcorn, recast]
metadata:
  version: 1.4.0
  updated: 2026-03-08
  parent: higgsfield
---

# Higgsfield Production Pipeline

## The Core Insight

Every Higgsfield tool is strong individually. The real power is when you chain them.
A professional result almost always involves at least 3 tools in sequence.
This skill documents the key chains and how to prompt for each stage.

---

## The Master Production Chain

This is Higgsfield's complete cinematic workflow — the chain used for short films,
branded content, and any multi-shot sequence that needs character continuity:

```
[1] POPCORN          → Storyboard / key frame images (consistent character + framing)
[2] SEEDREAM / SOUL  → Edit / style the image (transform appearance, fix details)
[3] ANIMATE          → Bring the image to motion (Veo 3.1 / Seedance / Sora 2 / Kling)
[4] RECAST           → Swap character if needed (maintain motion, change identity)
[5] LIPSYNC          → Add audio performance (speech, sound, emotion)
[6] VIBE MOTION      → Add motion graphic layers (titles, captions, CTAs)
[7] UPSCALE          → Final quality pass (Topaz upscale for delivery)
[8] ASSEMBLE         → Edit together in your video editor of choice
```

Not every project uses all 8 stages. Most good short-form content uses 3–5.

---

## Pipeline A: Cinematic Short Film (Full Chain)

**Goal:** A multi-scene narrative short — character-consistent, story-driven
**Credits required:** High (Pro or Ultimate plan recommended)
**Time:** 2–4 hours for a 30-second sequence

### Stage 1 — Storyboard with Popcorn

Generate consistent key frames for every scene before animating anything.
This is the planning stage — it's cheap and sets the foundation for everything.

```
Popcorn prompt structure:
"[Character description — be specific and consistent across all Popcorn prompts].
[Scene — location, time, atmosphere].
[Framing — camera angle, shot size, composition].
[Lighting — source, quality, direction].
[Style — film look, color grade, specific cinematographer reference]."
```

**Key rule:** Use the **exact same character description** in every Popcorn prompt.
This is how you get visual continuity across scenes without Soul ID.

**Example scene prompts for a single short:**

```
Scene 1 — Establishing:
"A middle-aged woman, dark hair pulled back, wearing a grey wool coat,
sitting behind the wheel of a moving car. Camera through windshield —
focused and tense expression. Sunlight flickering across her face.
35mm film, shallow depth of field, muted color tones, Roger Deakins style."

Scene 2 — Passenger reaction:
"An elderly man in a thick knit sweater, seated in the passenger seat,
gazing out the window with a calm but distant expression.
Camera slightly off-center, interior car shot.
Same 35mm film look, muted tones, soft natural light."

Scene 3 — Object insert:
"Close-up of a weathered wooden photo frame on a kitchen counter.
Inside: a faded photograph of a young woman and elderly man smiling.
Warm afternoon light through lace curtains, dust motes in air.
50mm lens, shallow focus, nostalgic atmosphere, yellow-green tones."
```

---

### Stage 2 — Image Editing with Seedream

After Popcorn generates your key frames, use Seedream to make targeted edits
that prompt engineering alone can't achieve:

**Common Seedream transformations:**
- Changing the character's appearance ("make the man look like a zombie")
- Fixing a detail that didn't render correctly
- Adjusting clothing or props
- Adding or removing an element from the frame
- Age progression or style transformation

```
Seedream edit prompt structure:
"[What to change, specifically]. [What to keep the same]."

Example:
"Make the elderly man look like a zombie — rotten flesh, white milky eyes,
grey skin tone. Keep all other elements of the image identical."
```

**Note:** Seedream edits the image, not the video. Always edit your Hero Frame
before animating — never after.

---

### Stage 3 — Animate by Scene Type

Choose the animation model based on what the scene requires:

| Scene type | Best model | Key prompt note |
|------------|-----------|----------------|
| Character emotional reaction | Veo 3.1 / Kling 2.6 | Lead with camera mount position |
| Car/vehicle action | Veo 3.1 / Sora 2 | Specify camera mount explicitly |
| Physical stunt / crash | Sora 2 | "One continuous shot, no cuts" |
| Quiet interior moment | Seedance / Kling 2.6 | Minimal motion, camera Dolly In |
| Epic reveal / scale | Sora 2 | Crane Up or Super Dolly Out |
| Portrait / reaction close-up | Kling 2.6 | Head Tracking or Dolly In |

**I2V animation prompt structure:**
```
"[Starting from the provided image as the first frame.]
[Describe only what MOVES or CHANGES — not what is already visible.]
[Camera — named control.]
[Atmosphere cues — sound, light changes, environmental motion.]
[Style consistency note if needed.]"
```

**Example chain of animation prompts (same short film):**

```
Scene 1 animation (Veo 3.1):
"Camera mounted on the dashboard, focused on the woman driving.
She drives calmly for 2 seconds — then her head turns left sharply.
Her eyes widen in silent horror, lips trembling, color drains from her face.
She doesn't speak — only stares, frozen. Warm sunlight flickers across her face.
Handheld realism, shallow depth of field, cinematic natural lighting."

Scene 2 animation (Veo 3.1):
"Camera fixed behind the car through the rear window.
The man turns his head slowly to the left — confusion spreading.
Expression twists from curiosity to fear. Eyes dart wildly.
He begins trembling and jerking his head, as if losing control.
Claustrophobic tension. Handheld realism, shallow DOF, eerie silence."

Scene 3 animation (Sora 2):
"A speeding sedan on an empty highway — camera tracking rig, low to ground.
Air shimmers with heat. Car veers — front tire catches rough asphalt.
The car lurches, tilts, flips violently through the air.
Dust, glass, metal fragments scatter. Sun flares in the lens.
Car rotates midair, skids upside down to a stop.
One continuous shot, no cuts. 24mm wide lens, midday, high shutter speed."

Scene 4 animation (Seedance):
"Camera dolly in slowly toward the woman at the kitchen window.
She doesn't move — just stands, looking out. Stillness."
```

---

### Stage 4 — Recast (Character Swap)

If you need to change a character's identity while keeping the motion exactly:

1. Take your animated video clip from Stage 3
2. Feed it into the **Recast** app
3. Upload your target character reference image
4. Recast replaces the character while preserving every motion, camera move, and
   lighting condition from the original clip

**Use Recast when:**
- You edited the character in Seedream (zombie example) but want to apply that
  transformation to the already-animated video
- You want the same scene with a completely different character (A/B test)
- You're building an AI Influencer series and need the Soul ID face in motion
- You need to de-identify or replace a character in existing footage

**Recast prompt note:** Recast is mostly UI-driven — the "prompt" is the reference
image you upload. The more cleanly shot the reference face, the better the swap.

---

### Stage 5 — Lipsync / Audio

Add speech or audio performance to any video clip:

**Lipsync Studio:** Upload video + audio → lips sync to the audio
**Kling 3.0:** Generate video with native audio already embedded (most seamless)
**Kling Avatars 2.0:** Create a talking avatar from a single image

```
When to use each:
- You have existing video + want to add speech → Lipsync Studio
- You're generating new content + need audio → Kling 3.0 (generate with audio from start)
- You want a consistent talking head character → Kling Avatars 2.0
```

**Lipsync prompt:** Not really a text prompt — upload the video clip and the audio.
The system handles sync automatically.

---

### Stage 6 — Vibe Motion Overlay (Optional)

Add motion graphic layers — titles, captions, lower thirds, CTAs — on top of
your generated video clips. See `higgsfield-vibe-motion` skill for full detail.

**Common additions at this stage:**
- Scene title cards (can be cut in before each scene)
- Character name lower thirds
- Location/time stamp
- End card with CTA, handle, or credit

---

### Stage 7 — Upscale

Run finished clips through Higgsfield's Topaz-integrated upscale before delivery:
- Upscale from 720p to 1080p or 4K
- Sharpens detail lost in generation
- Reduces generation artifacts
- Use Sora 2 Upscale specifically for Sora 2 outputs

---

### Stage 8 — Assembly

Higgsfield doesn't have a native timeline editor — assemble in your editing tool.

**Recommended assembly workflow:**
```
1. Export all clips from Higgsfield
2. Bring into DaVinci Resolve / Premiere / CapCut
3. Import Vibe Motion title cards/overlays
4. Add music (Kling 3.0 clips already have audio — other models need music added)
5. Color grade if needed (minimal — Higgsfield output is already color-intentional)
6. Export for platform
```

---

## Pipeline B: Social Content Series (Streamlined Chain)

**Goal:** Consistent weekly social posts with same character and aesthetic
**Credits required:** Medium (Pro plan)
**Time:** 30–60 minutes per post once Soul ID + Moodboard are set up

```
[1] SOUL ID          → Character locked once, reused forever
[2] MOODBOARD        → Aesthetic locked once, appended to every prompt
[3] GENERATE IMAGE   → Soul 2.0 or Nano Banana Pro 2 for each post
[4] ANIMATE          → Kling 2.6 I2V, simple motion per post
[5] VIBE MOTION      → Caption/CTA overlay per post format
```

**Per-post prompt template (after Soul ID + Moodboard are established):**

```
[Soul ID character] is [specific action] at [specific location].
[One specific visual detail that changes this post from the last.]
Camera: [simple control — Dolly In / Arc / Overhead].
Aspect: 9:16. Duration: 5s.
[Moodboard style modifier — same every post.]
```

**Example series (3 posts, same character):**
```
Post 1: [Soul ID] sips coffee at a sun-drenched café terrace. Reading a book.
         Camera: Dolly In. Aspect: 9:16.
         Style: warm amber, shallow DOF, golden hour.

Post 2: [Soul ID] walks through a quiet morning market, tote bag on shoulder.
         Camera: slight Arc. Aspect: 9:16.
         Style: warm amber, shallow DOF, golden hour.

Post 3: [Soul ID] sits at a desk by a tall window, writing in a journal.
         Camera: Dolly In. Aspect: 9:16.
         Style: warm amber, shallow DOF, golden hour.
```

The style modifier is identical every time. Only the scene changes.

---

## Pipeline C: Product Campaign (Commercial Chain)

**Goal:** Multi-asset product ad campaign — hero video + variants + social cuts
**Credits required:** Medium-High

```
[1] NANO BANANA PRO  → Perfect product hero image (4K sharp)
[2] MOODBOARD        → Brand visual direction locked
[3] I2V ANIMATION    → Product comes alive (Kling 2.6)
[4] APPS             → Variant generation (Click to Ad, Packshot, Giant Product)
[5] VIBE MOTION      → Feature callouts, lower thirds, price/CTA cards
[6] ASSEMBLE         → Hero cut + 3–5 social cuts
```

**Product hero prompt:**
```
[Product — describe precisely: material, color, form, no brand name].
[Surface/setting — clean, brand-appropriate].
Camera: [Robo Arm / Lazy Susan / Dolly In].
Lighting: [soft diffused / dramatic side-light / macro backlit].
Style: Commercial quality, [clean/warm/dramatic]. [Ratio].
```

---

## Pipeline D: Fast Iteration / Social Speed Run

**Goal:** Test 5 creative directions in under an hour
**Credits required:** Low (Basic/Pro)

```
[1] SEEDANCE PRO     → Generate 5 fast test clips (one prompt each)
[2] PICK BEST        → Select 1–2 that work
[3] KLING 2.6        → Upgrade the winners to premium quality
[4] VIBE MOTION      → Add captions/CTAs
[5] POST             → Skip the assembly step — single clips, direct export
```

---

## Pipeline Decision Guide

| You want to make | Use this pipeline |
|-----------------|-------------------|
| Short film / narrative | Pipeline A (Full Chain) |
| AI influencer series | Pipeline B (Social Series) |
| Product campaign | Pipeline C (Commercial) |
| Quick social content | Pipeline D (Speed Run) |
| Motion graphics only | Vibe Motion standalone |
| Single cinematic shot | Standard video generation (no pipeline) |

---

## Pipeline Pitfalls

**Pitfall 1: Animating before the image is right**
Fix your Hero Frame at Stage 1 before any animation. Never animate a "good enough" image.

**Pitfall 2: Different character descriptions across Popcorn prompts**
Use copy-paste for the character description in every Popcorn prompt. Even small
wording differences cause the character to drift between scenes.

**Pitfall 3: Trying to fix character issues in animation (Stage 3)**
If the character looks wrong in the Hero Frame, Recast is the fix — not the animation
prompt. Animation prompts can't fix appearance problems in the source image.

**Pitfall 4: Skipping Recast when you should use it**
If you've transformed a character with Seedream (e.g., zombie edit) and animated
the original, you need Recast to apply the transformation to the final animated clip.
The Seedream edit only affects the still — not the video.

**Pitfall 5: Over-engineering a single shot**
Save the full pipeline for multi-shot sequences. A single 5-second clip doesn't
need 8 stages. Run it through standard generation → upscale → post.
