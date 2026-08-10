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
  version: 3.4.1
  updated: 2026-08-09
  parent: higgsfield
---

# Higgsfield Production Pipeline

## QUICK FACTS
*Generated-checked block (scripts/build_index.py verifies anchors). Read the linked sections for full context — these lines are routing aids, not the rules themselves.*
- 8-stage Master Chain: Popcorn → Seedream/Soul → Animate → Recast → Lipsync → Vibe Motion → Upscale → Assemble; most good short-form uses 3–5 stages [→](#the-master-production-chain)
- Lock 9 project fields before touching any tool; "what must stay consistent" is the load-bearing one [→](#step-01-start-with-the-project-not-the-prompt)
- One job per scene — six scene purposes; a good scene prompt answers six questions [→](#step-06-give-every-scene-one-job)
- 7 reusable prompt-module types: character identity, camera, lighting, style, motion, negative prompt, continuity [→](#step-07-use-prompt-modules)
- 80% rule: keep what worked, fix only the mistake; every diagnosed failure becomes a new negative rule [→](#step-0809-fix-failures-protect-what-worked)
- Build in 8 passes: Concept → Project script → Scene breakdown → Shot list → Image prompts → Video prompts → Review → Fix [→](#step-10-build-the-project-in-passes)
- Use the EXACT same character description (copy-paste) in every Popcorn prompt — continuity without Soul ID [→](#stage-1-storyboard-with-popcorn)
- Seedream edits the image, not the video — always edit the Hero Frame before animating, never after [→](#stage-2-image-editing-with-seedream)
- Model by scene type: Sora 2 for stunts/epic ("one continuous shot, no cuts"), Kling 2.6 portraits, Seedance quiet interiors [→](#stage-3-animate-by-scene-type)
- Recast swaps identity while preserving motion, camera, and lighting; the "prompt" is the reference image you upload [→](#stage-4-recast-character-swap)
- Audio routing: existing video + speech → Lipsync Studio; new content with audio → Kling 3.0; talking head → Kling Avatars 2.0 [→](#stage-5-lipsync-audio)
- Higgsfield has no native timeline editor — assemble in DaVinci Resolve / Premiere / CapCut [→](#stage-8-assembly)
- Pipeline E hard rules: 15-second cap per scene, one generation per style, feed the previous scene's video as continuity reference [→](#stage-5-seedance-20-with-keyframe-previous-video)
- Soul Cinema keyframes: deliberately short 5–15 word prompts with enhancer ON — long prompts starve the enhancer [→](#stage-1-soul-cinema-keyframe-style-first-enhancer-on)
- Never describe character age in Seedance prompts; >15s per scene degrades prompt adherence — split the scene [→](#pipeline-e-pitfalls)
- No extend button: attach the accepted clip as a video reference + open with "The scene continues." — and match the source's resolution AND duration [→](#the-extend-a-clip-workflow)
- Cap seamless extension chains at 2 (hard ceiling 3); re-anchor from ORIGINAL canonical refs, break chains with B-roll [→](#chain-management-depth-caps-and-re-anchoring)
- An attached source clip carries the state — prompt only the delta; motion vectors, camera-move phase, audio phase stay in prose when handing off from a still frame [→](#source-carries-state-rule)
- End extension prompts on a camera-angle change so the join reads as coverage; plan transitions ahead (last-channel-on-TV trick) [→](#clean-join-planning)
- Draw a top-down schema when 2+ characters, a key prop placement, or complex camera geometry — prompt in absolute terms ("A 2m from B") [→](#spatial-blocking-top-down-schema-for-multi-character-scenes)
- Never animate a "good enough" image; if the character looks wrong in the Hero Frame, Recast is the fix — not the animation prompt [→](#pipeline-pitfalls)


## The Core Insight

Every Higgsfield tool is strong individually. The real power is when you chain them.
A professional result almost always involves at least 3 tools in sequence.
This skill documents the key chains and how to prompt for each stage.

---

## Building Complete AI Projects — The 10-Step Methodology

The Core Insight above answers *why* you chain tools. The next
question is *how to plan the project* before any tool is touched.
Most people skip planning and start prompting straight from a
creative impulse — a generation here, a clip there, hoping the
pieces will connect. They don't. A project that's planned at the
script and bible level lands consistently; a project assembled
prompt-by-prompt drifts on character, style, and continuity within
three or four generations.

This section documents a 10-step methodology for building complete
AI projects — from idea through finished sequence — that sits
upstream of the Master Production Chain below. Use these 10 Steps
as a planning discipline; use Pipelines A-E to execute the
tool-level chain once your project plan is locked. The closing §
Simple Workflow gives the imperative-action version of the same 10
Steps if you want the execution recipe before the principles.

### Step 01 — Start With the Project, Not the Prompt

Before writing a single prompt, define what you are building. The
AI cannot read your intent; if you skip this step the model fills
in the gaps with whatever the prompt happens to suggest, and the
project drifts within the first few generations.

Lock these nine fields before any tool is touched:

- Project type
- Main subject
- Visual style
- Scene goal
- Audience
- Mood
- Length
- Setting
- What must stay consistent

The last field is the load-bearing one. If you don't know what
must stay consistent across the project, every other field can be
locked and the result will still feel disjointed.

### Step 02 — Build a Master Script

A Master Script is the project blueprint — the single document
that keeps every scene connected to the same goal. It does not
have to be a Hollywood screenplay; it just needs to explain the
full idea clearly.

> **Master Script disambiguation.** "Master Script" in this
> context means the structured project document, not a screenplay.
> The source explicitly notes "it does not have to be a Hollywood
> screenplay; it just needs to explain the full idea clearly."
> This is distinct from Hollywood screenplay craft (slug lines,
> action lines, character cues, transitions) — that's a different
> discipline and is not in this skill's scope.

The Master Script should include:

- The story or concept
- The scene order
- The main characters or products
- The visual style
- The camera rules
- The setting
- The emotional tone
- The continuity rules
- What should never happen

Without a Master Script, each prompt becomes its own random
island. With one, every prompt belongs to the same project —
characters carry between scenes, the visual style holds, and the
negative rules ("what should never happen") stay out of the
output.

### Step 03 — Use GPT as Your Creative Assistant

Do not use GPT like a magic button. Use it like a creative team
member. GPT plays five distinct roles in the project pipeline:

- **Concept Builder** — turns a rough idea into a structured
  concept
- **Script Writer** — drafts the Master Script from the concept
- **Shot List Planner** — breaks the script into scene-by-scene
  shot lists
- **Prompt Refiner** — turns each shot into image or video prompt
  text
- **Problem Solver** — diagnoses failed generations and rewrites
  the offending prompt

The key is **staging**. Do not ask GPT to do everything at once.
Ask for the project structure first. Then the scenes. Then the
prompts. Then the revisions. The output quality at every stage
depends on the input quality of the prior stage; cascading the
work in order gives you control over each handoff.

> **In-platform alternative.** Higgsfield has an in-platform GPT-5
> copilot (Higgsfield Assist at higgsfield.ai/chat) trained
> specifically on Higgsfield's tools and workflows. For quick
> in-platform prompt generation and platform-navigation questions,
> see `../higgsfield-assist/SKILL.md`. For upstream project
> staging across multiple sessions, an external GPT (Claude,
> ChatGPT) running this 10-step methodology is the better fit
> because state carries across the full project, not just the
> current platform session.

### Step 04 — Separate the Script From the Prompt

The script is what happens. The prompt is how the AI shows it.
These are two different artifacts that serve two different
purposes — keep them in separate documents, and don't let
prompt-shaped instructions leak into the script.

A script line might read:

> "She walks into the room and realizes something is wrong."

The same beat, as a prompt, reads:

> "A woman slowly enters a dim apartment from the hallway. Camera
> stays in front of her at chest height, tracking backward as she
> steps forward. Her eyes move toward an overturned chair and
> broken lamp. Warm hallway light behind her, cold blue window
> light across the room. Her face tightens as she realizes
> something is wrong."

The prompt decomposes the beat into four production-instruction
categories:

- **Camera Notes** — wide shot, eye-level, shallow depth of field,
  focus on subject's expression
- **Lighting Direction** — dim, cinematic, cool blue ambient from
  window, single warm lamp in corner
- **Subject Movement** — slow, hesitant walk, pauses mid-step,
  tense posture, hand to mouth
- **Environment Detail** — cluttered, atmospheric, dust motes,
  shadows in corners, sense of foreboding

The script gives story. The prompt gives visual instructions. You
need both, in separate documents, with the script feeding the
prompt rather than collapsing into it.

> **Separation rule axis distinction.** This is the project-level
> separation — script (story) from prompt (AI instruction). For
> the prompt-level separation within a single shot — Identity (who
> is in frame) from Motion (what they do and how the camera moves)
> — see `../higgsfield-prompt/SKILL.md` § Identity vs. Motion
> Separation Rule and `../higgsfield-soul/SKILL.md` § Identity vs.
> Motion Separation. Different axes of the same overall
> composition problem; both apply.

### Step 05 — Create a Project Bible

A Project Bible is a single document that locks in the rules of
the project — character appearance, environment, style, what must
stay consistent, what must never appear. It is especially
important for any project with multiple scenes, because
consistency comes from repetition and clear rules, not from the AI
inferring intent.

The Project Bible should lock in:

- Character appearance
- Wardrobe
- Hair
- Color palette
- Location
- Lighting style
- Camera style
- Tone
- Props
- Negative rules
- Continuity rules

Three rules of thumb make a Project Bible work in practice:

- If your character is supposed to look the same every time,
  describe them the same way every time.
- If your product is the focus, make sure the product stays the
  focus.
- If your scene takes place in one location, do not let the AI
  redesign the room every shot.

> **Project Bible as upstream source-of-truth.** The Project Bible
> lives in your own files alongside the Master Script — it's the
> document you maintain across the project. Two common downstream
> realizations of the Bible inside Higgsfield: (i) the Character
> section feeds into a Soul ID character sheet, see
> `../higgsfield-soul/SKILL.md` § Character Sheet Creation for the
> multi-angle reference approach; (ii) Characters, Locations, and
> Props feed into Cinema Studio's @ Elements system, see
> `../higgsfield-cinema/SKILL.md` § Elements System for the
> `@CharacterName` / `@LocationName` / `@PropName` workflow. The
> Bible is the upstream artifact; the Soul ID sheet and Cinema
> Studio Elements are tool-side realizations of it.

### Step 06 — Give Every Scene One Job

Every scene should have one clear purpose. When you try to make
one scene do too much, the AI starts blending details — messy
motion, wrong angles, extra people, broken hands, missing
objects, confusing results. Six scene purposes cover most
project work:

- Introduce the character
- Show the location
- Build tension
- Reveal the product
- Create emotion
- Deliver the action

A good scene prompt answers six questions:

- Who is in the shot?
- Where is the camera?
- What is the subject doing?
- What should the viewer notice first?
- What must stay visible?
- What should not happen?

Clarity wins.

> **Per-shot action-count rule.** Step 06 addresses the
> *narrative purpose* of a scene (which may span multiple shots).
> For the per-shot *action-count* rule — one primary action per
> clip, with one or two secondary actions max — see
> `../higgsfield-prompt/SKILL.md` § One Action Per Scene. Both
> useful, at different units of decomposition.

### Step 07 — Use Prompt Modules

A prompt module is a reusable block of instruction. Instead of
rewriting the same camera or lighting notes every time, build
modules you can copy and paste. Seven module types cover most
project work:

- Character identity block
- Camera block
- Lighting block
- Style block
- Motion block
- Negative prompt block
- Continuity block

Example camera block:

> "Camera stays in front of the main subject, facing them
> directly while tracking backward. The subject moves toward
> camera. Background movement stays behind the subject. Do not
> reverse the direction."

That one block can save multiple generations. Build your own
library of modules — it saves time and keeps your project
stable.

> **Prompt Modules as finer-grained sibling of Identity/Motion.**
> The 7-module taxonomy is a finer-grained sibling of the
> Identity-vs-Motion separation rule used in single-shot prompts.
> For Soul ID single-shot work, the 2-block separation in
> `../higgsfield-soul/SKILL.md` § Identity vs. Motion Separation
> (also `../higgsfield-prompt/SKILL.md` § Identity vs. Motion
> Separation Rule) is sufficient — "Character identity block"
> here aliases their "Identity Block." The 7-module taxonomy adds
> a layer for multi-shot projects where camera, lighting, and
> style each warrant their own reusable block.

### Step 08+09 — Fix Failures + Protect What Worked

When a generation fails, do not just say "make it better" —
that's not actionable. Tell GPT exactly what went wrong: which
specific element is off, what to keep, what to change. Every
failure should become a new rule: each diagnosed mistake gets
locked into the project's negative-rules list so it doesn't
recur.

When fixing, protect what already worked. If 80% of the
generation was right, keep that 80%. Only fix the broken part.
A lot of people destroy good prompts by changing too much — keep
the subject, keep the style, keep the camera if it worked, keep
the lighting if it worked. Fix only the mistake.

> **Full iteration discipline lives elsewhere.** The full
> Change-One-Variable-at-a-Time discipline and the 6-Pass
> Diagnostic Sequence (Subject / Action / Camera / Style / Audio
> / Output) for when you don't yet know what's wrong are
> documented in `../higgsfield-prompt/SKILL.md` § The Iteration
> Rule — Change One Variable at a Time. Step 08+09 here names the
> three rhetorical handles ("make it better" anti-pattern, 80%
> rule, "every failure should become a new rule" framing); the
> mechanics live there. Whether a take is even a regeneration
> candidate — versus keep, fix-in-post, or edit — is decided by the
> five-verdict triage in `../higgsfield-troubleshoot/SKILL.md`
> § Take Triage — Five Verdicts for a Delivered Take.

### Step 10 — Build the Project in Passes

Do not try to do everything at once. Build the project in clear
passes:

- Pass 1: Concept
- Pass 2: Project script
- Pass 3: Scene breakdown
- Pass 4: Shot list
- Pass 5: Image prompts
- Pass 6: Video prompts
- Pass 7: Review results
- Pass 8: Fix and finalize

Each pass produces an artifact the next pass consumes. Pass 1
gives Pass 2 a concept to script; Pass 2 gives Pass 3 a script
to break into scenes; and so on. AI moves fast, but fast without
structure creates chaos — a workflow keeps it clean.

> **Tool-level instantiation.** Passes 5-7 (image prompts / video
> prompts / generate) are where the Higgsfield tool chain enters
> the workflow — see § The Master Production Chain below for the
> 8-stage tool-level chain (Popcorn → Seedream/Soul → Animate →
> Recast → Lipsync → Vibe Motion → Upscale → Assemble), and §
> Pipeline Decision Guide below for the chain choice by project
> type (Cinematic Short Film, Social Series, Product Campaign,
> Fast Iteration, Multi-Style Short Film).

### Simple Workflow — Execution Recipe

The 10 Steps above are the methodology. The Simple Workflow
below is the imperative-action recipe — the same workflow
expressed as steps you take in order:

1. Write the project idea.
2. Ask GPT to turn it into a project brief.
3. Ask GPT to break it into scenes.
4. Ask GPT to write a clean script.
5. Ask GPT to turn each scene into image prompts.
6. Ask GPT to turn each scene into video prompts.
7. Generate inside Higgsfield.
8. Review what worked and what failed.
9. Give GPT specific correction notes.
10. Regenerate only what needs fixing.

That is how you move from idea to finished project. At step 7
("Generate inside Higgsfield"), you choose which tool-chain to
run — see § Pipeline Decision Guide below for the chain choice
by project type.

### Build With Purpose

The power is not in one perfect prompt. The power is in the
workflow.

Scripts give the project direction. GPTs help organize and
refine the work. Higgsfield brings the visuals to life. When you
use all three together, you stop hoping for random good results.
You start building with purpose.

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

**Cut-friendly source material:** if you're landing morph cuts or smooth cuts
in the editor, generate the source clips with explicit 2-second still-or-near-
still moments at start and end. See `../higgsfield-cinema/SKILL.md` §
Multi-Shot Manual → Morph-Cut and Smooth-Cut breathing room.

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

## Working Practices

### Working in Parallel

The workflow becomes inefficient if every generation is treated as a
complete stop. While one generation runs, adjacent tasks can already
proceed: reviewing earlier blocks, drafting the next prompt, preparing
a continuation screenshot, deciding whether a scene needs a bridge.
The speed comes from separating tasks by what they actually depend on.

- **Depends on a final frame** — tasks that genuinely need the previous generation's output (continuation anchors, edits to a specific rendered frame)
- **Writable in parallel** — prompt drafts, screenshot prep, GPT review of earlier blocks; no rendering dependency
- **Backbone building** — episode-structural work: scene order, bridge identification, continuity-arc mapping
- **Waits for later refinement** — shot-level refinement (inserts, micro-prompts, beat adjustments) that should wait until the episode structure is locked

This separation produces speed without sacrificing structural control.

### Screenshots as Working Memory

Between generations, the project state lives in GPT-side conversation
memory — what's been established, what's the current beat, what the
next scene needs to anchor against. Screenshots make that working
memory durable: they preserve what would otherwise drift between
exchanges, and they keep the project visible at each decision point.
This is the working anchor in GPT — distinct from screenshots as
Seedance reference anchors (see `higgsfield-seedance` § Reference
Roles). The mechanism is concrete: "continue from this actual visible
state" is a stronger prompt instruction than "continue the last scene."

A screenshot helps in five recurring situations:

- **Scene already has a strong identity you do not want to lose** — the established look, framing, or staging would be costly to lose to drift
- **Prop or object must remain consistent** — a specific thing has to appear in the same form across shots
- **Body direction matters** — the character's facing, posture, or gesture is load-bearing for the next beat
- **Emotional carryover is very precise** — the state at the previous clip's end is specific enough that "tense" or "alert" won't carry it
- **Space is complex enough that text alone may blur it** — geometry, layout, or spatial logic resists prose description

Screenshots reduce ambiguity, and reduced ambiguity usually means
better continuity.

---

> **Recurrence as continuity substrate:** The backbone-building work above (scene order, bridge identification, continuity-arc mapping) operates on a substrate — what should recur across shots for a world to cohere. See `../../vocab.md` § World Through Recurrence for the eight named substrate axes.

> **Post-clip next-shot decisions:** Deciding whether a scene needs a bridge (or a continuation, contrast, or reset) is a post-generation question, not a pre-generation one. The four-question diagnostic and the next-shot decision tree formalize the call. See `higgsfield-seedance` § Post-Clip Decisions.

---

## Continuation & Extension Handoff

Extending an accepted clip — a sequel, a prequel, or a chained
continuation — is a workflow problem before it is a prompt problem.
This section owns the handoff mechanics: what to attach, what the
prompt text still has to carry, how deep a chain can safely go, and
how to plan the joins. The prompt-pattern side (continuation anchor
phrasing, reference-role wording) lives in
`../higgsfield-seedance/SKILL.md` — this section does not restate
those templates. It extends § Working Practices above: the post-clip
decision tree decides *whether* to continue; this section is *how*.
When a continuation comes back wrong, the symptom-level repair table
lives in `../higgsfield-troubleshoot/SKILL.md` § Sequence &
Continuation Failure Atlas — one repair variable per symptom.

### The extend-a-clip workflow

[EMPIRICAL — cross-surface] There is no dedicated extend button.
The extension workflow:

1. **Attach the accepted clip as a video reference.**
2. **Open the prompt with "The scene continues."** The model
   continues from the clip's end, carrying motion, characters,
   environment, even voices. For a prequel clip, open with **"Show
   me what happens before"** instead — the same mechanism chains
   past/current/future segments.
3. **Match the source clip's resolution AND duration** in the new
   generation (1080p→1080p, 15s→15s). A 720p extension against a
   1080p source shows a visible quality jump at the join.
4. **Occluded-identity binding:** if an identity feature is hidden
   at the source's end (a mole behind a hand, a face turned away),
   add the character image as a second reference and bind it
   explicitly — "The woman's identity is @Image1."

### Chain management — depth caps and re-anchoring

[FIELD — community, seedance-2.0 repo v6.6.0] Quality degrades over
chained extensions: each generation re-ingests the previous
generation's artifacts, and drift is expected by the ~4th–5th
generation in a chain. Manage the chain, don't ride it:

- **Cap seamless continuation chains at 2 extensions** — hard
  ceiling 3.
- **Re-anchor from the ORIGINAL canonical references** — the
  character sheets and location refs the project started with,
  never a frame from the drifted chain tail.
- **Break chains with B-roll** — a cutaway between extensions
  resets the degradation clock without breaking story flow.
- **Treat a scene boundary as an intentional cut** re-opened from
  canonical refs — don't try to seamlessly extend across it.

### Source-carries-state rule

[FIELD] An attached accepted clip carries its own state — static
(who is in frame, wardrobe, layout) and dynamic (motion in
progress, camera move, sound). The prompt text carries **only the
delta** — what changes next. Delete opening-state prose that
repeats what the attached source already shows: references outrank
text when they conflict, so the repetition is wasted budget at
best and a conflict source at worst.

A still frame is the weaker handoff — it carries static state
only. Three things a frame cannot carry, which must stay in prose
when handing off from a screenshot instead of a clip:

- **Open motion vectors** — who is moving, in which direction, how fast
- **Camera-move phase** — where mid-move the camera is (mid-dolly, mid-arc)
- **Audio phase** — what sound or dialogue is in progress at the cut point

### Clean-join planning

[EMPIRICAL] Plan the join before generating the extension, not in
the edit:

- **End extension prompts on a camera-angle change** ("the scene
  from the character's perspective") so the cut reads as
  intentional coverage rather than a seam.
- **Plan scene-to-scene transitions ahead.** The tutorial trick
  [DEMO]: build the NEXT scene's location early and put it on an
  in-scene TV as the last channel playing — the last frame becomes
  the next scene's opening frame.
- A truly seamless butt-join is a post-editing job — overlap the
  clips, opacity-ghost align (~5 frames), short audio crossfade —
  and is out of prompt scope.

---

## Spatial Blocking — Top-Down Schema for Multi-Character Scenes

When a scene has multiple characters or geometry that matters,
AI video models hallucinate spatial relationships unless they're
declared in absolute terms. The fix is a top-down schema —
bird's-eye sketch of the scene that you draft, the user
approves, and the prompt then describes in absolute terms
("character A 2m from character B, character C 1.5m behind A,
partially occluded by the corner pillar"). Skip this step and
the model resolves blocking on its own — usually wrong, often
worse cut-to-cut as the geometry drifts.

**When to draw a schema:**

- 2+ characters in the same scene
- Key prop on a specific surface (device, artifact, weapon,
  photo)
- Complex camera geometry (which shot from where, arcs, eyeline
  changes per cut)

**What goes on the schema:**

- Room outline (walls, tables, screens, doorways)
- Character positions (one initial per character, placed at the
  starting position)
- Eyelines (arrow showing where each character is looking)
- Props (icons or short labels at exact placement)
- Distances (~Xm between key objects)
- Surface labels (FL / FR / BL / BR for front-left / front-right
  / back-left / back-right, relative to a stated main view)

ASCII form for the schema — runtime-portable, copy-paste-able
into chat or any document:

```
                      [WINDOW]
                          |
  [TABLE]    G(↓east)     |
    ┌─┐                   |        R(↑north)
    │ │       ~2m         |          @
    └─┘                  ~1.5m
                          |
                       [DOOR]
                          |
                  (camera mount, west wall)
```

Translate the schema into the prompt as absolute spatial
declarations — "Gandelfina stands behind the table, facing east
at the window; Roko stands 2m from her, facing north toward the
door" beats "Gandelfina near the table, Roko nearby" by a wide
margin for AI-video adherence.

> **Workflow handoff to Seedance.** Once the schema is approved,
> the prompt declares character positions in absolute terms
> inside the Static Description slot of the Seedance prompt.
> See `../higgsfield-seedance/SKILL.md` § Output Format.

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
