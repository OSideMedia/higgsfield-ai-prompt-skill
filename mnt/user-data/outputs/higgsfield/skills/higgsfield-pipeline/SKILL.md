---
name: higgsfield-pipeline
description: >
  Use when the user wants to create a complete multi-shot video, asks how to chain
  Higgsfield tools together, wants to build a short film or branded content series,
  asks "what's the full workflow", needs to connect Popcorn → image → video → Recast
  → audio → assembly, or wants to understand how the platform works as a production
  system rather than isolated tools.
user-invocable: true
metadata:
  tags: [higgsfield, pipeline, workflow, chain, production, multi-shot, short-film, popcorn, recast]
  version: 3.1.0
  updated: 2026-04-10
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
[3] GENERATE IMAGE   → Soul 2.0 or Nano Banana 2 for each post
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

## Pipeline E: Multi-Style Short Film (Soul Cinema + Seedance 2.0 Chain)

**Goal:** A narrative short where every scene is a completely different animation style (paper cutout, French graphic novel, chibi, stop motion, manga, claymation, 2D-on-live-action, live action) but the hero character and key props stay consistent across all of them.

**Credits required:** Medium-High (Pro or Business plan). Soul Cinema is cheap (~0.5 credits per 4-image batch); Seedance 2.0 is where the credits go.
**Time:** 2–4 hours for an 8-scene short.

**The core trick:** feed the **previous scene's video + prompt** into the next scene's planning step. This is how style can change radically scene-to-scene while character, props, and story continuity hold.

```
[1] SOUL CINEMA      → Style-first keyframe for this scene (minimal prompt + enhancer)
[2] NANO BANANA PRO  → Targeted edits to match hero's appearance to previous scenes
[3] PROP SHEET       → (Once, at project start) multi-angle reference for recurring objects
[4] CLAUDE           → Write Seedance prompt given keyframe + PREVIOUS scene's prompt
[5] SEEDANCE 2.0     → Animate with keyframe (style ref) + previous video (continuity ref)
[6] REPEAT per scene → Each new scene feeds the previous video back into Claude
[7] ASSEMBLE         → Cut in DaVinci / Premiere / CapCut
```

### Stage 1 — Soul Cinema keyframe (style-first, enhancer ON)

For each new scene, generate a keyframe that defines the style. Prompts here should be **deliberately short** — 5–15 words — with the Soul Cinema enhancer toggle ON. Short prompts + enhancer explore styles you would never think to ask for explicitly.

```
Example per-scene keyframe prompts:
- "cartoon highly stylized man waking up in the bedroom"
- "2D French graphic novel style, man in a suit on a horse, cowboy chasing him in a futuristic environment"
- "chibi gladiator toy in a low poly arena"
- "stop motion style man in a black suit, futuristic helicopter behind him"
- "claymation style man in a suit over a black cauldron carried by a red demon"
```

**Style keyword locators:** Identify the 1–2 words that control the entire aesthetic — these are the only words you change between scene variants. In the examples above: `French graphic novel style` + `futuristic environment`, `chibi` + `low poly`, `stop motion` + `futuristic helicopter`, `claymation` + `red demon`. Swap those and the whole world changes.

Run 2–4 batches per scene, pick the strongest frame.

### Stage 2 — Nano Banana Pro: edit, don't regenerate

If Soul Cinema nails the style but the hero drifts (wrong hair color, wrong outfit, face too different from scene 1), **do not re-roll**. Take the image into Nano Banana Pro and swap only the mismatched elements:

```
Nano Banana Pro edit prompts:
- "swap hair to black"
- "put him in a black suit"
- "match this character to the reference image, keep the art style"
```

This is how you get cross-style character consistency — Soul Cinema owns the look, Nano Banana Pro owns the identity.

### Stage 3 — The prop sheet (one-time, up front)

Any object that appears in multiple scenes (watch, gun, pendant, briefcase) needs a prop sheet generated **once** at the start of the project. Seedance needs to know what the object looks like from every direction to keep it consistent across shots.

**How to build the prop sheet:**
1. Upload the hero keyframe (Scene 1) to Claude
2. Ask Claude: *"Give me a prop sheet prompt for [object] that matches this exact style"*
3. Take Claude's prompt into Nano Banana Pro
4. The prop sheet should include:
   - **Material breakdown** (what it's made of, surface detail)
   - **Internals** (if relevant — watch face, gun mechanism)
   - **Multiple angles** — front, side, back, 3/4, top. This is the critical part.

Keep the prop sheet image on hand. It gets fed into Seedance alongside the keyframe any time the object appears.

### Stage 4 — Claude writes the Seedance prompt (with previous-video memory)

This is the stage most people skip and it's where the consistency comes from. For each new scene:

1. Upload the scene's keyframe (from Stage 1–2)
2. **Also upload the previous scene's video prompt** so Claude knows what just happened, what style was established, and what effects need to carry through (portal, teleport, wardrobe state)
3. Describe the scene in plain language — what the hero does, what the environment does, how the scene ends
4. Claude outputs a full Seedance-ready prompt, shot by shot, 15-second cap

```
Example plain-language brief to Claude (scene 3, chibi arena):
"He lands in the arena, realizes he's gone chibi, tries to pick up a weapon but
can't figure out his blocky hands, dodges a knight, fumbles the watch, finally
catches it on the last try, and teleports out. 15 seconds."
```

Claude, given the previous prompt + keyframe, will preserve the teleport effect, the watch behavior, and the hero's core identity — while writing the new scene in the new style.

### Stage 5 — Seedance 2.0 with keyframe + previous video

Feed Seedance **three** inputs per scene:
1. **The Claude-written prompt** (from Stage 4)
2. **The keyframe** as style reference
3. **The previous scene's video** as continuity reference — this is the highest-leverage input. It's how the portal effect, character details, and story beats carry between radically different styles.

**Hard rules:** 15-second cap per scene (easier editing downstream), one generation per style (commit to the choice), multiple camera angles + movements within the 15s — Seedance 2.0 can handle a full multi-shot scene in a single generation.

### Stage 6 — Repeat with feedback loop

For every subsequent scene, the workflow is identical except the "previous video" you feed in is the scene you just generated. The chain self-reinforces: scene 3 knows about scene 2's ending state, scene 4 knows about scene 3's, and so on.

### Stage 7 — Assembly

Export all 8 clips, drop into your NLE, crossfade on the teleport flashes, add music under. Because each scene is already 15s with internal cuts baked in, assembly is mostly trimming and audio.

### Pipeline E pitfalls

**Pitfall 1: Skipping the previous-video feed.** If you only feed Seedance the keyframe, the story fragments. The previous video is what keeps the hero recognizable across styles.

**Pitfall 2: Re-rolling Soul Cinema when Nano Banana Pro can fix it.** Character wrong but style right? Edit, don't regenerate. Saves credits and preserves the style you already liked.

**Pitfall 3: Long Soul Cinema prompts with enhancer on.** Enhancer works best on short prompts. If you write 80 words, the enhancer has nothing to improvise with.

**Pitfall 4: No prop sheet for recurring objects.** A watch that appears in 8 scenes will drift into 8 different watches without a multi-angle reference image generated up front.

**Pitfall 5: Describing character age in prompts.** Seedance age inference is unreliable. Describe by role, clothing, and action — never by age. See the age-blind rule in `higgsfield-prompt`.

**Pitfall 6: >15 seconds per scene.** Seedance 2.0 caps at 15s, and beyond that prompt adherence degrades. Split longer scenes in two if needed.

---

## Pipeline Decision Guide

| You want to make | Use this pipeline |
|-----------------|-------------------|
| Short film / narrative (consistent style) | Pipeline A (Full Chain) |
| AI influencer series | Pipeline B (Social Series) |
| Product campaign | Pipeline C (Commercial) |
| Quick social content | Pipeline D (Speed Run) |
| Short film / narrative (style changes per scene) | Pipeline E (Multi-Style Soul Cinema + Seedance) |
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

---

> **Identity vs. Motion:** In all pipeline stages involving Soul ID characters, split prompts
> into Identity Block + Motion Block. The Identity Block stays identical across all stages;
> only the Motion Block changes per shot. See `higgsfield-prompt` and `higgsfield-soul`.

> **Negative constraints:** For artifacts specific to multi-shot workflows (identity drift,
> scene continuity breaking, camera contradictions), see `../shared/negative-constraints.md` —
> Temporal/Consistency and Face/Identity sections.

---

## Related skills
- `higgsfield-prompt` — MCSLA formula, Identity/Motion separation
- `higgsfield-soul` — Soul ID character consistency
- `higgsfield-cinema` — Cinema Studio workflow (alternative to manual pipeline)
- `higgsfield-models` — Model selection per pipeline stage
- `higgsfield-vibe-motion` — Motion graphics for overlay stages
- `higgsfield-recall` — Pre-generation memory check before each stage
- `templates/` — Annotated genre-specific templates for pipeline starting points
