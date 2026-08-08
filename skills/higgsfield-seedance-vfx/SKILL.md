---
name: higgsfield-seedance-vfx
description: "Writes, improves, or rewrites Seedance 2.0 prompts that TRANSFORM footage the user already has (video-to-video), rather than building a scene from scratch. Use whenever a real clip is the starting point and they want to: add a VFX element (set a head or hair on fire, transform a hand, make a limb invisible), swap the environment around a preserved subject (desert, clouds, lava, a neon city), drop a giant photoreal creature behind or onto a subject/landmark, relight or regrade so subject and added elements read as one shot, sync a crash-zoom or push-in to a spoken line or timecode, or generate a matching transformed start frame to animate from. Also use when they paste such a prompt and ask to change its lighting, timing, creature, or runtime, or say 'make a Seedance prompt for this video' with a clip attached. This is the video-to-video specialization; for a brand-new scene from image references with no source clip to preserve, higgsfield-seedance applies instead."
user-invocable: true
metadata:
  tags: [higgsfield, seedance, seedance-2.0, video-to-video, v2v, vfx, footage-transformation, environment-swap, creature, relight, 4k]
  version: 1.0.0
  updated: 2026-06-30
  parent: higgsfield
---

# Higgsfield Seedance VFX — Footage Transformation

This skill is for **editing a clip the user already has**: keep a real subject and the
real camera move, change only what they ask for. It is the video-to-video sibling of
`../higgsfield-seedance/SKILL.md` (the general Seedance director). It **reuses that skill's
grammar verbatim** — the six-slot formula, the Prompt-Craft Laws, the preflight linter —
and adds the transformation layer below. Do not contradict the parent skill; when a shot
needs filter-safety, mode selection, or engine rules, defer to it.

> **This file is the Seedance 2.0 v2v lane.** It stays the right choice when the job needs
> **4K**, `mode=std`, a platform start/end frame, or a `genre` hint. If the plate job is
> running on **Seedance 2.5** — 720p ceiling, up to 30 s, many references — the lane is
> `omni_reference` with the clip attached as a video reference, and its production doctrine
> (source ≥ 4 s, duration = source, the four-batch rule, the performance-inheritance clause)
> lives in `../higgsfield-seedance-2-5/VFX-PIPELINE.md`.

> **This skill is a video-to-video layer on top of `../higgsfield-seedance/SKILL.md`.**
> Every VFX transform is still a Seedance prompt. This skill only changes the *starting
> point*: a real source clip whose subject, performance, and camera move must survive the
> edit. `higgsfield-seedance` § Seedance 2.0 Prompt Modes / Transformation covers the
> *in-clip morph* (a character visibly becoming something else in one take); **this** skill
> covers *preservation-VFX* — lock the real plate, layer the effect in.

## QUICK FACTS
*Routing aids — read the linked sections for the actual rules.*
- The one job: **preserve** everything that makes the source recognizable, **change** only the named element; repeat the fragile guardrail ("face and identity unchanged") at the end [→](#the-core-idea-preserve-then-change-one-thing)
- Run it in **Seedance 2.0, mode std, 4K** — faces, lip-sync and fine detail hold at 4K where they warp at 1080p (`fast` can't do 4K; Cinema Studio caps at 1080p) [→](#resolution-run-it-in-4k)
- `@source` declares the clip as the base (not a style ref); add `@creature`/`@element` only when a real texture keeps getting faked [→](#prompt-anatomy-transform-variant)
- **Three levels** of difficulty: L1 swap the world · L2 change an element in-frame · L3 full handheld cinematic [→](#three-levels)
- Two modes: **add an element** to the plate, or **replace the environment** around a preserved subject [→](#two-transformation-modes)
- **Color matching alone looks pasted-in** — match key direction, bounce, optics/haze, edges/grounding [→](#lighting-integration-the-part-that-makes-or-breaks-it)
- Photoreal creatures need **biological accuracy** (wrinkled, cracked, asymmetric, matte — never smooth/glossy/inflated) + a real contact shadow; a reference image beats a description [→](#photoreal-creature-element-integration)
- Timed zoom synced to a line: anchor it **twice** — semantic (`On the line "…"`) + numeric (`At about Ts`); see `references/dialogue-timing.md` [→](#timed-camera-moves-synced-to-dialogue)
- Prepended-intro budget: `total − intro = surviving window` for the source performance; recompute on every change [→](#duration-discipline)
- Generate the transformed **start frame** first to lock the look before spending video credits; see `references/first-frame.md` [→](#first-start-frame-workflow)
- Output is **plain-text English**, no markdown inside the prompt, easy to copy [→](#output-format)

---

## The core idea: preserve, then change one thing

A transformation prompt has two jobs that pull against each other: **lock** everything that
makes the source recognizable (the person's identity, face, wardrobe, performance, framing,
lens, and camera motion), and **change** only the named element. If you under-specify the
lock, Seedance re-rolls the face or the camera and the edit stops matching the original. So
every prompt states both halves explicitly, and repeats the most fragile guardrail — usually
**"face and identity unchanged"** — at the end of the action.

This is the whole blueprint: real footage goes in, the exact same shot comes back — same
subject, same movement — with only the one requested change applied.

---

## Resolution: run it in 4K

Run everything in **Seedance 2.0, `mode=std`, 4K**. The 4K matters: faces, lip-sync and fine
detail hold at 4K where they warp and fall apart at 1080p — and a footage transform lives or
dies on the preserved face reading as the *same* face. The `4k` resolution enum is
model-verified (`../../specs/model-specs.json` → `seedance_2_0`); the "detail holds at 4K"
observation is a **practitioner claim**, strong but not a spec guarantee.

Two model constraints to respect (from `../higgsfield-seedance/SKILL.md` § Pre-flight Linter):
native 4K is available in **`mode=std` only** — `mode=fast` (Seedance 2.0 Fast) caps at
480p/720p, and inside **Cinema Studio** the model is still capped at 1080p. So a 4K footage
transform must run in std mode, on the standard Seedance 2.0 surface. If the user is on fast
mode or in Cinema Studio and asks for 4K, flag the cap before they generate.

---

## Prompt anatomy (transform variant)

### 1. The `@source` declaration

The source clip is the base, not a style reference. One line:

```
@source: Original <clip name> — <who/what is in it: subject, wardrobe, setting, action>. Preserve
<identity, face, wardrobe, performance, framing, camera and motion> exactly; <what to change —
e.g. enhance only the environment / add the creature on the tower / transform only the right arm>.
```

If a transformation needs a real texture the model keeps faking (an animal's fur, a specific
face), add a **second input** as a texture reference and declare it:

```
@creature: Reference photo of a real <animal> — <fur / face / anatomy notes>. Appearance and
fur/skin texture reference only; ignore the photo's background and lighting, do not use it for the
environment.
```

The user supplies their own descriptions of what is in their files — use the tags correctly,
don't invent what the clip contains. But before writing `@source` for a clip you can open,
**inspect it**: read its duration / fps / aspect and extract a few frames. Build `@source` and
the specs runtime from what the footage actually shows — subject, wardrobe, framing, camera
move, time of day, key direction — not from the user's one-line summary. Set the specs duration
to the probed runtime by default. If no source clip is described, ask what footage they're
starting from before writing.

> Seedance reads an uploaded video as a set of frames, not as a watched clip — so the frame
> content (subject, walk, light) is the context it has. Same principle as the screenshot →
> Claude workflow in `../higgsfield-seedance/SKILL.md` § Load-Bearing Rule.

### 2. Specs line

One compact line. Always include the source-matching constraints:

```
Photoreal. <aspect, default 16:9>. <duration — match the source clip>s. 4K. <look / grade>.
NON-IP — generic <creature/design>, not based on any brand or character. <SFX only | SFX and
source dialogue only>.
```

- **Match the source runtime by default.** If the clip is 6s, the prompt is 6s. Extend only
  when a payoff needs room (a slow creature turning to camera), and say why.
- **NON-IP guardrail** belongs in the specs line whenever a creature, armor, vehicle, or
  character design is added — generic, never a branded character. Keeps outputs clean and tends
  to generate more reliably than a trademarked design. (Same filter logic as
  `../higgsfield-seedance/SKILL.md` § The Rewrite Playbook / Brand · IP.)
- **Audio:** `SFX only` for added effects; `SFX and source dialogue only` when the source talk
  track must survive (e.g. a zoom synced to a spoken line — see
  `references/dialogue-timing.md`).

### 3. Scene action — one continuous shot

The source is a single take, so describe **continuous camera movement**, not cuts. Lead with the
shot/lens and "same framing as the source," then the preserved performance, then the
transformation, then any timed camera move. Close with the lock-down clause.

### 4. SFX line

End with a specific, ordered SFX note, exactly as the parent grammar requires. For added effects
be behavioral: not "fire" but "a soft whoomph as it catches, then a low steady flame roar and
crackle, occasional ember pop." Sync every effect (footsteps, impacts, wind, creature calls,
servo whirs) to the visible action.

---

## Three levels

The workflow scales in difficulty. The steps are identical at every level — inspect the clip,
name the one change, lock the rest — but the harder the camera moves, the harder the effect has
to track:

- **Level 1 — swap the world around you.** Keep the subject exactly as shot; replace the
  environment. Easiest on slow/steady moves; a driving shot raises the bar because the new world
  has to stream past at the right speed and relight the subject as it goes (§ Two transformation
  modes / B).
- **Level 2 — change an element in the frame.** Add or morph one specific thing: set a head of
  hair on fire, morph a hand into something unexpected, add a creature climbing a building. The
  plate stays; the effect is layered in and lit into it (§ Two transformation modes / A).
- **Level 3 — full handheld cinematic.** The camera is in-hand and moving the whole time — angle,
  parallax and shake all changing — and the effect (creature, environment, weather) must track to
  all of it without falling apart. This is the hardest case; preserve the handheld move
  frame-for-frame and lean on § Photoreal creature / element integration and § Lighting
  integration hardest here.

Locked-off shots are easy — the frame barely changes, so the model just paints the effect in.
The difficulty is entirely in how much the camera moves.

---

## Two transformation modes

### A. Add an element to the footage

Set a head on fire, transform a hand, make a limb invisible, perch a creature on a landmark. Keep
the whole plate; layer the effect in.

- Describe the effect's **physics and behavior over time**, not just its presence: where it
  starts, how it spreads, how it moves, what light it throws. Use directional "creep" for
  transformations ("starts at the tattoo, fine seams split one at a time and peel back, a servo
  seats, a cable plugs in, the next plate locks…") and ignition-then-build for fire.
- Make the effect **interact with the plate**: firelight flickering on a face and spilling onto a
  car's paint; a glassy invisible arm refracting the background; a giant creature casting a real
  soft-edged contact shadow on the structure it grips. (The model spills an added fire's orange
  glow onto skin, shirt and car on its own — but naming the interaction makes it reliable.)
- **Scale must be explicit** for giant creatures, or the model renders them life-size. Say
  "enormous, its massive body dwarfing the structure, clearly colossal relative to the mast."
- The subject usually stays **oblivious / unfazed**, mid-delivery — that contrast is the joke.
  State it.

### B. Replace the environment around a preserved subject

Keep the person, their vehicle, the seatbelt, the camera rig and its move; swap the whole world.

- The new world must **stream past with parallax** consistent with the original motion. If the car
  was driving, the replacement must give it a surface to drive on and things that rush past at
  speed. On a fast move the environment can't just sit behind the subject — it has to move with the
  subject at the right speed and change the lighting as it goes.
- The bigger the move, the **longer the lock list**: it's not just the face anymore — it's the car,
  the seatbelt, the rig framing, the whole driving motion, all held while only the environment
  changes.
- **Warm, directional daylight worlds are safer** for face/identity consistency than night or neon
  — those force a full relight of the subject and raise drift risk. Flag this tradeoff and bake the
  relight instruction in when the user wants night/neon anyway. (Seedance will pull light from the
  generated world and bounce it onto the subject — neon sliding across a car, lava glowing under a
  chin — without being asked; naming it makes it dependable.)

---

## Lighting integration (the part that makes or breaks it)

First decide the fork with the user — it changes everything:

- **Preserve the subject's lighting, grade only the new elements.** Lock the subject's original
  light; light and grade the added creature/environment to match the existing key on the subject so
  they integrate. Lowest identity risk.
- **Relight the whole frame under one look.** Subject included. Use this for a unified cinematic /
  commercial grade. Higher risk to the face, so keep identity/expression/wardrobe explicitly locked
  while only lighting and grade change.

Color matching alone is **not enough** to make a preserved subject sit in a new world — that's the
most common "looks pasted in" failure. When integrating a subject (or a creature) into a plate, go
beyond color with this recipe:

- **Light:** same key direction (name it — screen-left or screen-right), same softness, same shadow
  density and direction across the subject. ("Keep the sun as the key from screen-left exactly as
  before so the face and the light on it barely change.")
- **Environmental bounce:** let the world spill onto the subject — cool skylight from above, a warm
  bounce from sunlit ground/foliage, subtle ambient occlusion where forms meet.
- **Optics & atmosphere:** match lens character and micro-contrast; add a touch of the scene's
  atmospheric haze and aerial perspective over the subject so they aren't unnaturally crisp against
  a hazy background; match depth of field, focus falloff and film grain to the rest of the frame.
- **Edges & grounding:** remove hard cut-out edges, halos and mismatched rims; ground the subject
  with believable depth so they occupy the same space.

State the time of day and key direction concretely ("soft, diffused midday daylight with the key
coming from screen-right"). "Softer" means a larger, more diffuse source: gentle soft-edged
shadows, low contrast, smooth highlight rolloff, light haze. Full cinematic-lighting vocabulary is
in `../../vocab.md` § Lighting.

---

## Photoreal creature / element integration

When a creature or hard-surface element is added and must read as real:

- Demand wildlife-documentary / practical realism explicitly: "fully photoreal, real fur with depth
  and individual strands (or true scale detail / brushed metal), true anatomy, **never CG, plastic
  or cartoonish**."
- **Biological accuracy** is what separates a living thing from a cheap render. Specify real
  anatomical detail — "pebbled scaly skin, long claws, heavy tail, true reptile anatomy" — and
  demand **imperfection**: deeply wrinkled, cracked, sagging, **asymmetric**, mud-caked and matte.
  Avoid smooth, glossy or inflated surfaces; real animals are uneven. Match behavior to the species
  (a sloth shifts slow heavy weight; a chimp is alert and twitchy; a snake's coils tighten and a
  forked tongue tastes the air — and snakes don't blink, so use an unblinking stare, not a blink,
  for a reptile payoff).
- **Sell the scale.** Use on-screen reference objects (trees, buildings, crew, the subject) to
  establish true size, and use a **telephoto-lens illusion** with shallow depth of field to veil a
  giant creature partly behind foreground elements — plus a little motion blur and handheld softness
  so it integrates rather than floats.
- Tie it into the plate: same sun direction and color temperature as the subject, a real
  soft-edged contact shadow on what it touches, the same hazy atmosphere and depth as the far
  background.
- If it still reads as CG after a take, the reliable fix is a **second input** — a reference photo
  of the real animal/material, declared as a texture-only reference (see `@creature` above). When
  you already know exactly what you want, it's better to *show* the model than to describe it;
  generate the reference in `../higgsfield-gpt-image-2/SKILL.md` (GPT Image 2) or Nano Banana Pro,
  then point the prompt at it.

---

## Timed camera moves synced to dialogue

A crash zoom or smooth push-in landing on a beat is a recurring payoff. Anchor it **two ways at
once** so it lands even if Seedance's internal timing drifts: a semantic cue and a numeric cue.
The full measurement procedure — how to read `T` off the source audio and convert a timecode —
is in **`references/dialogue-timing.md`**.

- Semantic: `On the line "<exact words>," the camera <snaps into a hard crash zoom | begins a
  smooth, steady push-in> …`. Requires `SFX and source dialogue only` in the specs so the talk
  track survives.
- Numeric: `At about <T> seconds … the camera …`. Get `T` from the source audio (or a visible
  action beat — "at about 2.2s, on his finger snap").
- **Crash zoom** = fast hard punch-in; **smooth push-in** = slow steady glide, no snap. Match the
  user's word.
- If a landmark or subject must stay visible **through** the move, say so explicitly ("the tower
  stays in frame throughout, never cropped").
- Leave enough tail after the trigger for the payoff to play (a creature slowly turning to camera
  needs ~2–3s). If the clip is short, fire the zoom on the first word of the line rather than
  after it.

### Reveal pull-back (the outward move)

The mirror of the push-in: open tight on the *added* element in isolation — a long-telephoto,
compressed framing of the creature/effect with the subject out of frame — then move outward to
land on the real plate. Two flavors, match the user's word:

- **Hard / snap zoom-out** = a fast punch outward, abrupt.
- **Smooth pull-back** = a slow steady decompression, no snap.

Anchor the landing the same two ways as a timed zoom, and demand a **100% match of the source
composition** at the landing: name the matched attributes — same angle, headroom, horizon, lens
character — or the model lands on a near-miss framing that no longer cuts against the original.
After the landing, hand off to the preserved take and keep the source's own camera motion running.

### Preserving lip-sync to a known line

When the payoff is the subject's mouth matching a specific line, quote it **verbatim** and anchor
it twice: once inside the action ("…lips matching the source exactly, saying clearly: '<line>'…")
and once in the SFX/dialogue line. Require `SFX and source dialogue only` in the specs so the talk
track survives, and add "lips matching the source exactly" to the lock-down clause. Then check the
line against the surviving dialogue window (see § Duration discipline / Prepended-intro budget) —
a line that runs ~6s cannot sit in a 5s tail. If it doesn't fit, resolve the runtime before
delivering; don't ship a prompt that can't lip-sync. Dialogue + `[AUDIO: Xs]` mechanics live in
`../higgsfield-audio/SKILL.md`.

---

## Duration discipline

Default to the source clip's exact runtime. When the user changes the runtime, **recompute** any
numeric zoom timing and tell them the new mark. When a long hold lands on a static creature, add
small "living" micro-movements (a slow blink, jaw shift, steady breath) so it doesn't look frozen.

### Prepended-intro budget: intro + remaining = total

When you prepend a beat (a reveal, a telephoto hold, an establishing creature shot) to footage you
must preserve, the preserved take does not get longer — it gets *pushed back*. State the arithmetic
every time and flag what falls off:

`total runtime − intro length = surviving window for the source performance`

If the source take is longer than that surviving window, some of it cannot play. Say so explicitly
and offer the three resolutions, in order of fidelity:

1. **Extend the total** so the full source fits (intro + full source). Highest fidelity, longest
   clip.
2. **Start the source earlier** — sacrifice the clip's own quiet lead-in so the dialogue still
   lands in the window. Keeps total fixed, keeps the words, loses pre-roll.
3. **Accept truncation** — the first N seconds of the source won't appear. Only safe if the dropped
   head has no dialogue.

Never promise "100% lip-sync" and a prepended intro on a fixed total without doing this subtraction
first. Recompute and re-flag it on *every* change to either number.

---

## First / start-frame workflow

Before spending video credits, it's often worth generating the **transformed opening still** as an
image, locking the look, then animating from it. **See `references/first-frame.md`** for the full
procedure (model, settings, inputs, upload mechanics, and how to hand the still back to Seedance
as a `start_image`). This pairs with `../higgsfield-seedance/SKILL.md` § Drafts Validate the Prompt
— pin the frame, not the roll.

---

## Iterating

The user iterates fast and in small steps ("softer light," "from the right," "bigger snowier
mountains," "make the chimp huge," "a beat before the zoom," "keep the original runtime"). Change
**only the named thing** and keep the rest of the prompt stable — re-rolling the whole prompt loses
what already worked. When refining a generated still, edit the chosen result (pass it back as the
base) and fix only what's off rather than starting over. This is the footage-transform case of
`../higgsfield-prompt/SKILL.md` § The Iteration Rule.

---

## Output format

Output in **English first**, plain text — no bold, no headers, no bullets inside the prompt, not in
a code block. Easy to copy as-is. Chinese translation only if asked, after the English, same
format.

A short label above each prompt (e.g. `Hook_2 · Variant 1 — Through the clouds`) is fine and helps
when you deliver several variants; the prompt body itself stays plain text.

Skeleton:

```
@source: ...
@creature: ...            (only if a texture reference is used)

Photoreal. 16:9. <N>s. 4K. <look/grade>. NON-IP — generic <X>. SFX [and source dialogue] only.

<Continuous shot, same framing as source. Preserved performance. The transformation, with physics
and plate interaction. Any timed camera move with semantic + numeric anchor. Lock-down clause: face
and identity unchanged; everything else identical to the source.>

SFX [and source dialogue] only: <specific, ordered sounds>.
```

## Voice (match the user)

Terse and kinetic; physically precise (exact materials, behaviors, scale); director-minded (lenses,
angles, moves); non-generic (no "beautiful / stunning / amazing" — texture words instead);
emotionally controlled. Don't inflate, don't soften, don't explain what things "represent." Same
anti-slop discipline as `../higgsfield-seedance/SKILL.md` § Voice Rewrite.

## Seedance 2.0 input limits (reference)

Images ≤ 9; videos ≤ 3 items, total ≤ 15s; audio ≤ 3 MP3s, total ≤ 15s; total mixed inputs ≤ 12;
generation duration 4–15s. A source clip plus a texture-reference photo fits easily. If a request
needs more inputs than allowed, flag it and say what to prioritize. (Verified against
`../../specs/model-specs.json` → `seedance_2_0`: `media_roles` include `video`, `image`, `audio`,
`start_image`, `end_image`; `4k` is a legal resolution in `mode=std`.)

## Structure patterns to internalize (style reference only — do not reproduce)

- **Add-element:** `@source (preserve all, add effect)` → `specs + 4K + NON-IP + SFX only` →
  `continuous shot, preserved performance, effect igniting/creeping with plate interaction, subject
  unfazed` → `lock-down clause` → `SFX`.
- **Environment-swap:** `@source (preserve subject + vehicle + rig + motion, replace world)` →
  `specs + 4K + grade for the new world` → `continuous shot from the same rig, new world streaming
  past with parallax, relight to match or relight-all` → `lock-down` → `SFX`.
- **Creature-on-landmark with timed zoom:** `@source` + `@creature (texture ref)` → `specs + 4K +
  NON-IP + SFX and source dialogue only` → `continuous locked shot, giant photoreal creature
  integrated on the landmark, subject delivering to camera` → `at ~T / on the line "…", smooth
  push-in keeping the landmark in frame, creature turns to camera` → `lock-down` → `SFX and
  dialogue`.
- **Prepended reveal intro (transform + outward move + preserved performance):** `@source (preserve
  subject + performance + lip-sync + framing, add element, prepend a telephoto intro)` + `@creature
  (texture ref)` → `specs + 4K + NON-IP + SFX and source dialogue only` → `open tight/telephoto on
  the added element in isolation for the intro beat, hard or smooth zoom-out at ~T landing on a 100%
  match of the source composition, then the preserved take plays with exact lip-sync to the quoted
  line while the added element continues behind` → `budget check (intro + remaining = total)` →
  `lock-down` → `SFX and dialogue`.

A ready-to-fill skeleton plus worked variants live in
`../../templates/seedance/footage-vfx-transform.md`.

---

## Related Skills

- `../higgsfield-seedance/SKILL.md` — the parent Seedance director: six-slot formula, Prompt-Craft
  Laws, engine rules, content-filter preflight linter, and the in-clip Transformation prompt mode
- `../higgsfield-audio/SKILL.md` — audio-as-conditioning, `[AUDIO: Xs]` dialogue/SFX, lip-sync (the
  timed-zoom-to-dialogue and source-dialogue-preservation cases)
- `../higgsfield-camera/SKILL.md` — video reference, the Load-Bearing Rule, camera-move vocabulary
  (handheld preservation + moves you never filmed)
- `../higgsfield-gpt-image-2/SKILL.md` — generate the creature/texture reference image and the
  transformed start frame
- `../higgsfield-facs/SKILL.md` — muscle-level facial control when a dialogue-preserving transform
  also needs an exact expression
- `references/dialogue-timing.md` · `references/first-frame.md` — the two procedures this skill leans on
