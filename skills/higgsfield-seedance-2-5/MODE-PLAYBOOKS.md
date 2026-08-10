# Seedance 2.5 — Mode Playbooks

The long-form templates for the modes and techniques that `SKILL.md` routes to. Every
template here is `[OFFICIAL — Dreamina]` (ByteDance's *Seedance 2.5 Prompt Guide* and
*User Guide*), normalized to this repo's house conventions: positive phrasing, no age
words, reference roles always paired with exclusions.

Read only the section the task needs.

| Task | Section |
|---|---|
| Change something inside an existing video | § Video editing |
| Add footage after (or before) an existing video | § Video extension |
| First/last frames, keyframe stages | `SKILL.md` § First-Last Frame and Multi-Keyframe Control |
| A storyboard grid drives shot order | § Storyboard grids |
| A 3D previz / white-model drives the shot | § Blockout references |
| A batch of stills becomes one edited video | § One-click video |
| Bridge content between two finished clips | § Seamless transitions |

---

## Auto-locked parameters

Three modes take parameters away from you. Know this before promising an aspect ratio or a
runtime.

| Task | Aspect ratio | Duration |
|---|---|---|
| Video editing | Locked to the input video's ratio | Locked to ~the input's duration (±~0.3s from frame processing) |
| First-frame / first-and-last-frame | Locked to the **first image's** ratio (first and last should match, or the last frame stretches) | Settable |
| Video extension | Locked to the input video's ratio | Settable |

On the Higgsfield surface, `video_edit` additionally **bills by the source video's
duration** and ignores the `duration` and `aspect_ratio` parameters entirely
(`../../specs/model-specs.json`, snapshot 2026-08-07).

---

## Video editing

> **Check the lane before writing an edit order.** `video_edit` is for a **scoped change
> inside a master whose timeline must survive untouched** — a wall's light colour from
> 4–7 s, one prop swapped, the music removed. It ignores `duration`, ignores
> `aspect_ratio`, and bills by the master's full length. A *footage-transformation* job —
> replace the subject, inherit the plate's performance frame for frame, keep every other
> pixel — is the **`omni_reference` v2v lane** instead, where duration is settable and must
> equal the source (which is why the source has to be ≥ 4 s): `VFX-PIPELINE.md` § Stage 4.

Define the source as the **sole editing master**, then state the edit target, the scope, the
target material, and what must not change.

```
[Edit Goal]
Edit @Video 1. Within <the entire video or a specific time range>, <add, remove, replace, or
adjust> <visual object, region, or audio category>.

[Source Video Role]
@Video 1 is the sole editing master. It defines <characters, scene, actions, composition,
camera movement, occlusion relationships, audio, and event order>.

[Target Material Role]
@Image 1 or @Audio 1 defines <specified attributes of the target object or sound>.

[Edit Scope]
Modify only <object, region, time range, or audio category>.

[Content to Preserve]
Keep <visual content, motion, audio, and timing relationships that must not change> from @Video 1.
```

**Worked example:**

```
[Edit Goal]
Edit @Video 1. Only from 4-7 seconds, change the cool blue light on the right wall to warm
orange light.

[Source Video Role]
@Video 1 is the sole editing master. It defines the character, room layout, actions,
composition, camera movement, audio, and event order.

[Edit Scope]
Change only the light color on the right wall and the area it illuminates. Allow the
character's skin tone to respond naturally to the environmental light.

[Content to Preserve]
Keep the character's identity, clothing, expression, position, motion, room structure, camera
movement, dialogue, and ambience from @Video 1.
```

### Subject replacement — the Timeline Inheritance clause

A replaced object must inherit the original's *timeline*, not just its look. Without this
clause the new object appears, moves, and exits on its own schedule.

```
[Edit Scope]
Modify only <specific object and area>. The entire video contains <number> target object(s).
Do not modify <content to preserve>.

[Timeline Inheritance]
<Target object> inherits every appearance, motion, occlusion, and exit of <original object>,
including timing, duration, path, and speed changes.
Except for the object or area explicitly modified above, keep all other people, props, scene
content, camera movements, cuts, and event order from @Video 1 unchanged.
```

State the **target count** explicitly ("Keep exactly one white folding desk lamp throughout
the video") — this is the 2.5 form of the duplicate-object lock.

### Background replacement — scope by silhouette

```
[Target Reference Role]
@Image 1 defines only <target environment>'s spatial layout, materials, depth of field,
ambient color, and lighting direction. Do not use the people or foreground objects in the image.

[Edit Scope]
Modify only <background outside the subject's silhouette>. Do not modify <subject identity,
facial features, hairstyle, clothing, expression, position, size, or motion>.

[Timeline Inheritance]
Keep the character actions and occlusion relationships from @Video 1.
```

### Audio editing

Dialogue, spoken language, voice, background music, and sound effects edit independently.
Name the category, the change, and what stays untouched.

```
Edit @Video 1. Remove only the original background music. Keep the character dialogue, lip
sync, ambience, and action sound effects; preserve the visuals, camera treatment, and editing
rhythm from @Video 1.
```

```
Edit @Video 1. Change <Presenter>'s spoken language to natural American English while
preserving the dialogue content and speaking times. Keep all other character voices,
background music, ambience, and visuals from @Video 1.
```

### Written-scope editing (the annotation substitute)

Dreamina's mark-based editor is not on the Higgsfield surface (`SKILL.md` § Dreamina-Only),
so precision comes from the sentence instead. The vendor's own written form is:

```
[Specific modification object / what] + [action and change description] + [effective time range]
```

```
In the first 8 seconds of the video, replace the courier's jeans with dark black suit
trousers, and keep that change consistent for the rest of the clip.
```

Say whether the change exists for the **whole clip** or only inside a stated window — an
unscoped edit is where mid-clip reversions come from.

---

## Video extension

**Align the boundary frame before describing any new content.** This is the rule the mode
lives or dies on. A forward extension's first frame continues from the source's last frame;
a backward extension's last frame lands *on* the source's first frame.

On the Higgsfield surface this mode requires `extension_mode: forward | backward`, and the
aspect ratio follows the source.

### Forward extension (after the source)

```
@Video 1 is the source video to extend forward.

Extend @Video 1 forward. The first frame of the extended segment directly continues from the
last frame of @Video 1. Maintain continuity in <subject pose and orientation>, <prop
position>, <background and spatial relationships>, <camera position and composition>,
<lighting>, and <motion direction>.

Then, <describe the new action, event, camera treatment, or audio to add>.

Throughout the extension, maintain continuity in <character identity and clothing>, <key
props>, <background layout>, and <axis of action>.
Keep each subject as the same continuous instance throughout: do not duplicate or split it,
and keep the person's appearance or the object's number of parts stable.
```

### Backward extension (before the source)

The trap: writing "then connect to the source video". That phrasing lets later elements leak
into the preceding footage, and lets the image keep drifting after it has already reached the
target state. Land the source's first frame explicitly, as the extension's end state.

```
@Video 1 is the source video to extend backward.

Extend @Video 1 backward. Before the source video begins, <describe the preceding action,
event, camera treatment, or audio>.

The last frame of the extended segment naturally connects to the first frame of @Video 1:
<subject pose and orientation>, <prop position>, and <background and spatial relationships>.
Match the <camera position and composition>, <lighting>, and <motion direction> of @Video 1's
first frame.

Throughout the extension, maintain continuity in <character identity and clothing>, <key
props>, <background layout>, and <axis of action>.
```

### With additional reference materials

Define every new material's role **first**, then state that the source video still controls
the boundary image. New materials supplement; they never override the boundary.

For a backward extension, additionally say which materials belong to the preceding segment
and which must appear **only after** the source begins — otherwise later characters, props,
and effects show up early.

```
<Materials that should appear only after the source video begins> must not appear early in
the backward extension.
```

### Extension house rules

- **Boundary frames connect naturally, not identically.** Review both sides of the seam plus
  the full extended segment before accepting the take.
- **A cut extension is a different order than a continuous one.** For a continuous extension,
  ask for natural extension and smooth movement connection with no rigid cut and no objects
  appearing out of thin air. For a deliberate transition, use the cut-setting formula:
  `[transition type guide] + [basic constraint requirements] + [cut logic requirements]`,
  naming shot A, the transition, and shot B.
- **Extended-segment audio volume may differ slightly** from the source.
- **Chain economics:** a source within 30s extends by 4–30s per operation — 60 seconds is a
  single chain's ceiling. Past that, re-anchor from the original references rather than
  extending an extension.

---

## Storyboard grids

A grid communicates **story, shot order, and approximate composition** — not strict per-panel
reproduction. Prefer ≤15 panels, clean line art or simple diagrams, minimal text labels.

```
@Image 1 provides an <N-panel storyboard grid> for shot order and approximate composition.
Read it <left to right, top to bottom>. Do not use the grid's <line-art style, text labels,
or placeholder characters>.
@Image 2 defines <Subject A>'s <appearance and clothing>.
@Image 3 defines <key prop or scene>'s <structure, material, or lighting>.

Shot 1: <shot size, subject action, and scene state>.
Shot 2: <shot size, subject action, camera movement, or transition>.
...
Shot N: <closing action and final visible state>.

The final video uses <visual style>. Audio includes <dialogue, ambience, action sound effects,
or music>.
```

State the reading order explicitly, and state what to **ignore** from the grid itself — the
line-art style and placeholder figures are the two things that leak.

When the board is monochrome and the film is not, say so in its own sentence: *"Do not
render in pencil, ink, or monochrome — the board's drawing style is not the film's
style."* The generic exclusion covers borders and labels; it does not stop the board's
*medium* from being read as the film's look, and the failure is unmistakable — the render
comes back gray and sketchy. `[EMPIRICAL — third-party Seedance 2.5 field skill,
2026-08-09 evaluation; vendor-consistent]`

### Panel-to-timestamp mapping — the optional adherence raiser

`[MEASURED — 2026-08-09 A/B, (2.5, Ark), 480p, one pair]` Adding an explicit
panel→time mapping to the grid's role line changes *when* the cuts land, not whether
the shots come in order:

```
Panel 1 (left) is 0-1.5s, panel 2 (middle) is 1.5-2.5s, panel 3 (right) is 2.5-4s.
Do not reorder the shots. Do not invent shots that are not on the board.
```

What the A/B showed on a clean 3-panel board: **order was followed in both arms** —
order alone doesn't need the mapping. The mapping arm's cuts landed on the declared
stamps and each panel's contents stayed in its own shot; the unmapped arm chose its own
pacing (the middle shot swallowed half the runtime) and let a shot-3 prop leak into
shot 1. Use the mapping when the *time budget* per panel matters or when props/actors
must not bleed across panels.

Two boundaries hold: the vendor disclaims strict storyboard alignment — the grid stays
a "high-level plot reference", and the mapping raises adherence rather than
guaranteeing it (timestamps allocate a budget; they are not frame-accurate edit
points). When true per-panel strictness is required, that is the **multi-keyframe
channel** (`SKILL.md` § First/last frame and multi-keyframe control), not a grid.
Slot position, by contrast, is not worth fighting over: the same A/B day measured
board-first vs board-last with identical order adherence — upload order is a
tie-breaker, not semantics (SD25-PE confirmed).

---

## Blockout references

Decide **coarse vs fine first** — it changes the whole prompt structure.

| Type | Best for | Material needs | Prompt focus |
|---|---|---|---|
| **Coarse** | Simple geometry previewing action, paths, blocking, camera movement, cuts | Clear shape relationships + a complete action sequence; character/prop/scene images added separately | Map every blockout subject; state which temporal and spatial information to inherit |
| **Fine** | A complete model needing new materials, colors, characters, scene, or style | Complete, clean model — no path lines, coordinate axes, controllers, or camera frustums | Preserve structure, action, and camera; define what to re-render |

### Coarse blockout

What a coarse blockout can carry, and what the prompt must say about each:

| Blockout information | State in the prompt |
|---|---|
| Path | Action trajectory, motion direction, subject blocking, entrance/exit order |
| Camera movement | Camera position, path, direction, speed changes |
| Lighting | Light direction, brightness changes, and when they occur |
| Cuts | Cut positions, and the subject/composition before and after each |
| Audio | Whether to inherit dialogue, music, ambience, or action SFX |

```
@Video 1 is a coarse blockout reference. It provides only <motion paths, subject blocking,
camera position, camera movement, cuts, lighting changes, sound rhythm, or spatial
relationships>. Do not use its blockout appearance, materials, or scene.
<Blockout Subject A> in @Video 1 corresponds to <Subject A>.
<Blockout Subject B or geometric prop> in @Video 1 corresponds to <Subject B or key prop>.
@Image 1 defines <Subject A>'s <appearance, clothing, or structure>.
@Image 2 defines <specified attributes> of <Subject B, key prop, or scene>.

<Subject> completes <primary action or event> in <scene>.
Keep <motion path, blocking, camera movement, cuts, lighting, or sound rhythm> from @Video 1.
The final video uses <characters, scene, materials, and visual style>. Audio includes
<dialogue, ambience, or action sound effects>.
```

**Appendage warning.** Arms, wings, and similar appendages should appear in a coarse blockout
only when their action sequence is *complete*; a partial appendage sequence renders stiff or
gets misread structurally. The vendor's own best practice is to leave limbs and wings out of
the coarse model entirely.

### Fine blockout

```
@Video 1 is a fine blockout reference. Preserve <subject structure, action, spatial layout,
camera position, camera movement, and cuts>. Do not use its original gray materials or empty
background.
@Image 1 defines <subject>'s <character appearance, material, color, or surface details>.
@Image 2 defines <scene>'s <space, materials, lighting, or visual style>.

Re-render <subject> from @Video 1 as <final subject>, and re-render the scene as <final scene>.
Keep <structure, action, camera treatment, and spatial relationships> from @Video 1.
Use <materials, colors, and style>. Audio includes <ambience, sound effects, or music>.
```

Clean the source first: remove trajectory lines, coordinate axes, controllers, and camera
frustums, or they render as scene content.

**Segmented render form** — when the render treatment changes partway through:

```
Render the blockout animation of @Video 1 into the final film.
0-<N>s: <background environment, tone, character material, light and shadow>.
At <N>s, <transition trigger point and method>: <rendering description of the new scene>.
Character rendering <remains unchanged / changes with the scene>.
```

**Partial-reference discipline.** A blockout used for only part of a clip must say so, or it
expands into a whole-film reference: "@Video 2 is the action reference for the 20-25 second
counterattack only; do not use it for other segments, and do not bring its gray scene or
original texture into the final footage."

---

## One-click video

Turning a batch of images — optionally plus a style-reference video — into one video with
consistent pacing. **"Turn these materials into a video" is never enough.**

Order: `Material Roles → Image Order → Motion Amount → Editing Style → Visual Treatment → Audio`

```
[Material Roles]
@Image 1 is used for <character, product, scene, or opening image>.
@Image 2 is used for <character, product, scene, or process image>.
@Image 3 is used for <character, product, scene, or ending image>.
@Video 1 is used only for <editing rhythm, transitions, subtitle treatment, or music style>.
Do not use its character identities or scene.

[Arrangement]
Show the images in <upload order, a specified order, or a model-selected thematic order>.
<State the character, product, location, and event relationships that must remain consistent>.

[Image Motion]
Apply <subtle live motion, parallax, push-in/pull-out, lateral movement, or local action> to
each image.
Keep <subject appearance, product structure, text, or background relationships> stable.

[Final Style]
Use <editing rhythm, transition style, subtitle or graphic treatment, and color style>.

[Audio]
Include <dialogue, ambience, sound effects, or music>.
```

If image order matters, state the exact sequence — the model will not infer it. If it does
not, say the model may arrange by theme. With several characters or products, keep naming and
binding each one separately.

---

## Seamless transitions

Generates continuous **bridge content** between two videos.

Order: `Before Video → After Video → Trigger Action → Camera Movement → Visual Transformation
→ Arrival State → Audio`

```
@Video 1 is the before-transition clip. Use its <ending subject, action, composition, camera
direction, and audio>.
@Video 2 is the after-transition clip. Use its <opening subject, composition, camera direction,
and audio>.
Keep <character identity, product structure, scene, and primary action> stable in the original
portions of @Video 1 and @Video 2.

At the end of @Video 1, <subject or foreground object> triggers the transition through <action>.
The camera <movement direction and speed change>, while <shape, material, light, or space>
gradually transforms into <corresponding element> at the start of @Video 2.
The transition ends naturally at @Video 2's opening composition, preserving continuity in
<subject position, camera direction, and motion trend>.
Audio transitions smoothly from <before audio> to <after audio>.
```

### Transition methods and what each one needs

| Method | Specify |
|---|---|
| Dive / reverse movement | Camera direction, speed change, when the next scene begins |
| Character rotation | Pose, rotation direction, how clothing and background change continuously |
| Foreground occlusion | When the foreground object fills the frame, and the composition that follows |
| Object morph | Corresponding shapes and materials, and the transformation process |
| Push / pull or focus change | Camera movement, focus target, continuous spatial relationship |

### Named transition vocabulary

`[OFFICIAL — Dreamina]` Each is written as `[transition type guide] + [basic constraint
requirements] + [cut logic requirements]`, and each guide clause carries the same two
prohibitions: no rigid cut, and no objects appearing out of thin air.

| Transition | What it does |
|---|---|
| **Natural shot switching** | Hard-cut-like with no effect — but named explicitly so the seam reads as a shot change, not a glitch |
| **Fade in / fade out** | Shot A darkens to black, shot B lifts out of it |
| **Stacking** | Shot A becomes transparent while shot B emerges; the two overlap for a stated duration |
| **White flash / black flash** | An impact beat erupts into a flash, then cuts straight to the next scene |
| **Erase** | The frame wipes like a sliding door in a stated direction, uncovering shot B |
| **Mask transition** | An object or wall fills the frame to black; the camera pulls through into shot B |
| **Similar-object transition** | Shape similarity carries the cut — a coin becomes a ruler's end |
| **Action transition** | The camera follows a violent movement into blur; shot B enters from the same blur direction |
| **Dynamic relay** | A subject exits the frame in one scene and enters the next holding the same posture, against a new background |
| **Zoom in / zoom out** | Magnify into a detail (a pupil) until the next scene unfolds inside it |
| **Ink-wash** | Shot A diffuses like ink in water while shot B emerges from the dispersal |

You may also hand the model a shortlist and let it choose: "From natural shot switching, mask
transition, ink-wash transition, or similar-object transition, use the one that suits this
film's style."

**The ceiling:** a transition targets visual and audio continuity. It is a generated bridge,
not a pixel-identical edit splice of both sources.

### Give the bridge a deadline

`[HOUSE — re-derived from the nutllwhy/seedance-tvc-director evaluation, MIT, 2026-08-09.
UNPROVEN HERE: the durations below are that source's practitioner figures, not measured on
our material.]`

A transition written without an arrival keeps going. The vocabulary above is safe because
every entry names a finish; the failure is in the freehand wording around it — **"drifts
through", "floats across", "travels into", "gradually becomes"** name a passage and no
endpoint, so the bridge eats the segment after it and the next scene arrives late.

Write every bridge as three states with a stated clock:

```
Last state of the outgoing scene → one bridging action → target scene fully established at <time>.
```

Four guardrails, in the source's numbers — lean this way rather than treating them as
measured:

- **An ordinary bridge is short** — roughly 0.2–0.8s. It is a seam, not a shot.
- **One hero transition per piece** may run longer, ~1.2s, and only one.
- **No empty frame inside it.** A bridge that passes through a near-solid or subject-less
  frame for more than a beat reads as a dropout; the target scene should be establishing
  itself before the bridging element clears.
- **Say when the target is established**, not just that it arrives: *"the whip begins at
  9.0s; the living room is fully readable by 9.5s"*. A named arrival time is what stops the
  passage from expanding into the next segment's runtime.

Total transition time across a 30s piece stays small — the source budgets ~2.5s for all of
them combined. Everything else belongs to the scenes.

Reach for a morph only when the concept itself is the transformation. Otherwise a hard cut,
an action match or a short whip is both cheaper and more reliable — and each one has a
finish written into its own name.

---

## Related

- `SKILL.md` — the mode router, reference-role grammar, staging, limits
- `../higgsfield-seedance/SKILL.md` — Seedance 2.0 director and the shared prompt-craft laws
- `../higgsfield-seedance/ENGINE-RULES.md` — hard rendering constraints shared across the family
- `../higgsfield-pipeline/SKILL.md` — assembling generated pieces into a longer cut
