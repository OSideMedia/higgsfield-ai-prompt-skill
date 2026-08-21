---
name: higgsfield-seedance-2-5
description: "Seedance 2.5 prompt director — the omni-reference dialect. Routes the four generation modes (t2v / omni_reference / video_edit / video_extension), writes explicit @Image/@Video/@Audio reference roles with exclusions, stages 30-second videos into end-state beats, and covers video editing, forward/backward extension, first-last-frame and multi-keyframe control, storyboard grids, blockout rendering, and seamless transitions. Use whenever the user asks for a Seedance 2.5 prompt, mentions Seedance 2.5 / Dreamina / Jimeng, wants a clip longer than 15s on Seedance, wants to EDIT or EXTEND an existing video rather than generate a new one, or supplies more than a handful of image/video/audio references. For Seedance 2.0 (4K, start/end frames, genre hint) use higgsfield-seedance instead."
user-invocable: true
metadata:
  tags: [higgsfield, seedance, seedance-2.5, dreamina, jimeng, omni-reference, video-edit, video-extension, multi-reference, long-video, keyframes, storyboard, blockout, transitions]
  version: 1.3.0
  updated: 2026-08-21
  parent: higgsfield
---

# Higgsfield Seedance 2.5 Director

Seedance 2.5 is a **different dialect from Seedance 2.0**, not a version bump you can
prompt through by habit. 2.0 is a reference-driven shot generator with start/end frames
and a 4K lane. 2.5 is an **omni-reference production model**: up to 50 reference
materials, 30-second native runtime, and three non-generation modes — it can edit a video
you already have, and extend one forward or backward from its boundary frame.

The prompt grammar changes with it. Reference roles are declared in prose (`@Image 1
defines …`), audio and text get bracket syntax, long videos are staged with explicit end
states, and first/last frames are announced **inside the prompt** rather than selected as
a mode.

> **Model split — read this before writing anything.** 2.5 caps at **720p** and has no
> `start_image` / `end_image` media role, no `genre` hint, and no 4K lane. If the job
> needs 4K, a genre hint, or platform-level start/end frame pinning, it is a
> **Seedance 2.0** job — `../higgsfield-seedance/SKILL.md`. See § Choosing 2.0 vs 2.5.

## QUICK FACTS
*Generated-checked block (scripts/build_index.py verifies anchors). Routing aids — read the linked sections for the rules themselves.*
- Four modes, picked **before** writing: `t2v` · `omni_reference` · `video_edit` · `video_extension`; the mode changes what the prompt *is* [→](#the-mode-router)
- Higgsfield surface: **480p/720p only**, duration **4–30s**, no start/end-frame role, no genre hint, `extension_mode` required for (and only for) `video_extension` [→](#the-higgsfield-parameter-surface)
- `video_edit` **ignores** `duration` and `aspect_ratio` and bills by the source video's length; `video_extension` inherits the source's aspect ratio [→](#the-higgsfield-parameter-surface)
- Every reference material gets an explicit role **and** an exclusion — "what to use" plus "what not to use"; never let the model infer the mapping [→](#reference-roles-say-what-to-use-and-what-not-to-use)
- Each material also declares a **fidelity grade** — full-preserve / partial-preserve / attribute-transfer (name the target) / loose-guide; beat lines name characters (name + one visible marker), never handles [→](#fidelity-say-how-much-of-each-material-must-survive)
- Material budget: 30 images / 10 videos ≤30s total / 10 audio ≤30s total, 50 materials max; stability ranges are 1–8 subjects (images), 1–5 subjects at 5–10s (video/audio) [→](#material-budget)
- Multi-reference is a 5-step workflow — map → group → profile → select-by-scene, one line per subject; `@Images 1 through 4 define four characters` is the canonical failure [→](#multi-reference-the-five-step-workflow)
- Long videos are **staged**, not paragraphed: one primary change per stage + an explicit **end state**; timestamps allocate a budget, they are not frame-accurate edit points [→](#long-video-stages-and-end-states)
- Staging fixes too many EVENTS; two incompatible JOBS in one generation (physics + performance) is a separate cut — split into two prompts and stitch [→](#split-by-job-not-only-by-length)
- Bracket syntax: `()` music · `<>` SFX · `{}` dialogue · `【】` subtitles; non-Chinese dialogue needs a language line before the line [→](#audio-and-text-bracket-syntax)
- First/last frames and multi-keyframes are declared **in the prompt** (`@Image 1 is the first frame`) — aspect ratio locks to the first image; never merge the two anchors into one sentence [→](#first-last-frame-and-multi-keyframe-control)
- Editing needs a **sole editing master** + edit scope + Timeline Inheritance; extension needs the **boundary frame aligned before** any new content: `MODE-PLAYBOOKS.md`
- Storyboard grids, coarse-vs-fine blockouts, one-click video, seamless transitions: `MODE-PLAYBOOKS.md`
- **AI-VFX production pipeline** — model-per-asset-class routing, the size-ref frame, location batching, the `omni_reference` v2v lane (source ≥4s, duration = source), the four-batch rule, the slop catalog: `VFX-PIPELINE.md`
- Emotion needs 2–4 **observable** cues, not adjectives; niche camera terms get translated into a visible result [→](#emotional-direction-and-camera-terms)
- The real-person formula is 7 slots — and slot 1 is **role, never age**: the age-blind engine rule outranks the source guide's `[Age/Race]` label [→](#the-real-person-character-formula)
- Hard limits that must not be over-promised (frame accuracy, locked parameters, pixel-identical transitions) [→](#hard-limits-do-not-over-promise-these)
- Dreamina-product features that are **not** on the Higgsfield surface — Ultra Long Video 180s, mark-based editing, Clay Renderer [→](#dreamina-only-what-higgsfield-does-not-expose)

---

## Provenance

Two independent sources, labelled throughout:

| Label | Source |
|---|---|
| `[OFFICIAL — Dreamina]` | ByteDance's *Dreamina Seedance 2.5 Prompt Guide* + *User Guide* — the model vendor's own prompt doctrine. Prompt grammar is model-side, so it carries across to Higgsfield's hosting. |
| `[OFFICIAL — platform]` | Higgsfield's live `models_explore` catalog, snapshot **2026-08-07** (`../../specs/model-specs.json`). Parameters, enums, and media roles come from here and nowhere else. |
| `[DREAMINA-ONLY]` | A Dreamina *product* feature with no Higgsfield parameter behind it. Never quote these as things the user can do here. |

Where the two disagree about what is *settable*, the platform snapshot wins — it is what
the API actually accepts.

---

## The Mode Router

Pick the mode first. The same sentence means different things in different modes, and two
of the four modes are not generation at all.

| The user wants | Mode | What the prompt is |
|---|---|---|
| A clip from a description, no materials | `t2v` | A scene brief — the core formula below |
| A clip built from images / videos / audio they supply | `omni_reference` | A **role map** plus a scene brief |
| To change something inside a video they already have | `video_edit` | An **edit order**: master + scope + preserve list |
| More footage before or after a video they already have | `video_extension` | A **boundary contract** plus new content |

Two rules that fall out of this:

1. **First/last frames, keyframes, storyboard grids, and blockouts are all `omni_reference`.**
   2.5 has no separate first/last-frame mode on this platform — the anchor images are
   ordinary references whose *role sentence* says they are the first and last frame.
   `[OFFICIAL — Dreamina: "no need to switch to a separate first/last-frame mode"]`
2. **Editing is not regeneration.** If the user wants the shot rebuilt, that is
   `omni_reference` with the old clip as a motion reference — not `video_edit`. `video_edit`
   preserves the master's timeline and changes one scoped thing inside it.

> **Video-to-video is not automatically `video_edit`.** The field VFX workflow — swap the
> person in this plate, keep every other pixel — runs in **`omni_reference` with the source
> attached as a video reference**, because that is the lane where `duration` is settable and
> must be **matched to the source** (and where the source therefore has to be **≥ 4 s**, the
> `duration` floor). `video_edit` is the lane for a scoped change inside a master whose
> timeline must survive untouched. Full routing table + the performance-inheritance clause:
> `VFX-PIPELINE.md` § Stage 4. `[FIELD — AI-vs-VFX, 2026-08-08]`

---

## The Higgsfield Parameter Surface

`[OFFICIAL — platform, snapshot 2026-08-07]` · verify against `../../specs/model-specs.json`
before quoting (HARD RULE 3).

| Parameter | Values | Notes |
|---|---|---|
| `mode` | `t2v` · `omni_reference` · `video_edit` · `video_extension` | default `t2v` |
| `duration` | 4–30 s | default 5 — **ignored in `video_edit`** |
| `resolution` | `480p` · `720p` | default 720p — **there is no 1080p or 4K on 2.5** |
| `generate_audio` | bool | default true |
| `extension_mode` | `backward` · `forward` | **required** for `video_extension`, **not allowed** otherwise |
| aspect ratio | `auto` · `21:9` · `16:9` · `4:3` · `1:1` · `3:4` · `9:16` | ignored in `video_edit`; follows the source in `video_extension` |
| media roles | `image_references` · `video_references` · `audio_references` | **no `start_image` / `end_image`** |

Three consequences worth stating to the user before they spend credits:

- **`video_edit` bills by the source video's duration**, and neither `duration` nor
  `aspect_ratio` is settable — a 20-second master costs a 20-second render no matter how
  small the edit.
- **`video_extension` inherits the source's aspect ratio**; only the extension's
  *duration* is yours to set.
- **No `genre` parameter.** 2.0's genre hint does not exist here — genre lives in the
  prompt's visual-style clause instead.

Preflight the same way as 2.0:

```
python3 scripts/seedance_lint.py --preflight --model seedance_2_5 "<prompt>"
```

The linter reads the enums out of `../../specs/model-specs.json`, so an out-of-range duration, a
1080p request, or a `video_extension` missing its `extension_mode` is caught before the
render.

---

## The Core Prompt Formula

`[OFFICIAL — Dreamina]` Combine only the parts the shot needs; omit the rest rather than
padding empty slots.

```
<Subject> performs <primary action or event> in <scene and environment>.
The visuals feature <visual style>.
Use <shot size, camera angle, camera movement, or cuts>.
Audio includes <dialogue, ambience, sound effects, or music>.
```

- **Subject + action** is load-bearing — make it concrete. "The man runs" → "the man
  accelerates into a sprint while his jacket reacts to the airflow."
- **Scene and environment** — location, time, weather, spatial relationships, background state.
- **Visual style** — lighting, color, materials, texture, mood. Only descriptors that add
  information; stacked buzzwords ("cinematic, 8K, masterpiece") sample nothing in particular.
  The named-substitute discipline in `../higgsfield-seedance/SKILL.md` § Prompt-Craft Laws
  applies unchanged.
- **Camera** — shot size, angle, movement, focus subject, transitions. Motion matches the
  action; it is not decoration.
- **Audio** — dialogue, voice characteristics, ambience, SFX, music, synchronized to the visuals.

**Generation parameters are not prompt text.** Resolution, duration, and aspect ratio are
set on the generation page or via the API — writing them into the prose does nothing except
in the modes that auto-lock them, where they are not settable at all.

---

## Reference Roles — Say What to Use *and* What Not to Use

The moment there is more than one material, or a material sitting next to a text
description, the prompt must state what each material contributes. `[OFFICIAL — Dreamina]`

```
@Image 1 defines <subject>'s <appearance, clothing, structure, or material>.
@Video 1 defines <motion, camera movement, or pacing>.
@Audio 1 defines <character or sound type>'s <voice, dialogue, ambience, or music>.
```

Every material that could leak something unwanted gets an explicit exclusion in the same
sentence:

```
@Image 2 defines the workbench and window light. Do not use the people in the image.
```

Rules:

- **Mappings live in the prompt.** Text labels drawn inside an image are not a mapping, and
  the model will not infer which person or prop a material represents.
- **Video-only references are motion/pacing references by default**, not identity — say so
  explicitly when you mean otherwise.
- **Several views of one subject must say they are one subject**: "All four images define
  one folding desk lamp. The output must contain only one lamp throughout." Without it the
  model duplicates the subject.
- **When a reference video already carries the motion accurately, state only which
  attributes to inherit.** Restating every action fights the reference. A blockout or motion
  video carries motion and spatial structure — not identity — so the prompt still has to
  define subjects, scene, action, and visual style.
- **Never place a reference handle in a shot where that subject is absent** — the same rule
  as 2.0's tag discipline; the model forces it into frame.
- **Character sheets leak their staging.** A sheet's neutral backdrop and multi-view panel
  layout are the most common character-material leak — the flat gray studio renders as the
  actual set. Pair every character-sheet role with its own exclusion: *"Do not take the
  gray backdrop, the panel borders, or the multi-view layout."*
- **Beat lines name characters, never handles.** In action/beat prose, a character appears
  as name + one visible marker at their first appearance in the beat — *"Mira — silver
  streak, rust-red jacket — crosses the stall line"* — not as `@Image 2`. The model binds
  by what it can see in the material, and a handle used as a sentence subject is the
  classic way one character comes back as two people. `[OFFICIAL — SD25-PE mapping
  priority: material content outranks upload order]`

### Fidelity — say how much of each material must survive

`[EMPIRICAL — MiniMax H3 skill corpus, re-derived; cross-model structure, unmeasured on
Seedance]` A role says what job a material does; it still doesn't say how much of the
material must reach the pixels. Declare one fidelity grade per material, in the same
sentence as its role:

- **full-preserve** — the subject appears as-is: face, build, wardrobe, all of it.
- **partial-preserve** — the named parts survive, the rest is free: *"the jacket and the
  scar; hairstyle may change."*
- **attribute-transfer** — named traits lift onto a **different, named target**: *"apply
  this fabric's weave and sheen to Mira's coat."* The target must be named — this is the
  one case a bare role line cannot express, and the one that goes wrong silently.
- **loose-guide** — mood, palette, or energy only; nothing is copied literally.

```
@Image 4 defines the brocade fabric — attribute-transfer onto Mira's coat only.
Do not carry the garment's cut, the mannequin, or the studio backdrop.
```

### Material budget

`[OFFICIAL — Dreamina]` Hard limits vs the ranges that actually stay stable:

| Type | Hard limit | Stable range |
|---|---|---|
| Images | 30, each ≤4K | 1–8 distinct subjects |
| Videos | 10, ≤30s combined | 1–5 subjects, 5–10s each |
| Audio | 10 clips, ≤30s combined | only clips directly relevant |
| Video-edit source | 1 video + reference images | source ≤20s, 1–5 reference images |

50 reference materials total. Above the stable ranges (9–12 subjects in images, 6–10 in
audio/video, 6–8 edit reference images) generation still works but stability drops and the
shot may need several attempts — budget for it, or split the scene.

**More than five subjects needing multiple views → one view per image.** Independent view
images beat a single collage of views; the collage is the less stable form.

---

## Multi-Reference — the Five-Step Workflow

`[OFFICIAL — Dreamina]` The goal is **not** to cram every reference into one sentence. It
is to define the relationships among characters, props, scenes, actions, and audio so the
model picks the right material for the right moment.

**Step 1 — name and map each subject individually.** One line per subject:

```
<Character A> corresponds to @Image 1. Use only the appearance, hairstyle, and clothing.
<Character B> corresponds to @Image 2. Use only the appearance, hairstyle, and clothing.
<Prop A> corresponds to @Image 3. Use only the structure, material, and color.
<Scene A> references @Image 4. Use only the spatial layout, architecture, and lighting.
Do not use the people in the image.
```

> **The canonical failure:** `@Images 1 through 4 define four characters respectively.`
> That sentence does not say which image is which character, and the model will guess.

**Step 2 — group by type** once several subjects are in play: `[Characters]` → `[Props]` →
`[Scenes]` → `[Motion and Audio]`. Add the non-interchange lock to the character group:
"Do not interchange these characters' appearances, clothing, actions, positions, or dialogue."

**Step 3 — profile any recurring subject.** A character crossing several scenes, or
carrying several materials, gets one consolidated block:

```
[Subject Profile: Conservator]
Appearance and clothing: @Image 1.
Fixed prop: <Sample Case> from @Image 5.
Locations: <Conservation Lab> and <Gallery>.
Motion references: the case-opening motion from @Video 1.
Do not use: other characters' clothing. Do not give this character other equipment.
```

**Step 4 — select references by scene.** Per scene, list only the subset actually used,
then the event and its end state:

```
Scene 1 | Inspection in the Conservation Lab
Use: <Conservator>, <Sample Case>, <Conservation Lab>, and the case-opening motion from @Video 1.
Event: <Conservator> opens <Sample Case> at the workbench and inspects the sample inside.
End state: <Conservator> remains on the inner side of the workbench. <Sample Case> stays
beside the conservator's right hand.
```

**Step 5 — check ownership.** Props belong to exactly one character ("belongs only to
<Conservator>"); character count, clothing, and spatial direction stay constant across scenes.

---

## Long Video — Stages and End States

`[OFFICIAL — Dreamina]` 2.5 generates up to 30 seconds natively. Anything with several
events gets **staged** — one flat paragraph is where dropped beats come from.

Each stage carries exactly **one primary state change** and closes on an **explicit,
directly visible end state**. Each new stage restates what carries over.

```
[Generation Goal]
Generate a <video type>. The central subject is <subject>, and the primary event is <story summary>.

[Stage 1]
Initial state: <initial state of characters, props, and scene>.
Primary event: <one primary action or event>.
End state: <character positions, prop ownership, or visible scene state>.

[Stage 2]
Continue from the previous stage: <state that must remain unchanged>.
Primary event: <one primary action or event>.
End state: <observable state>.

[Stage 3]
Primary event: <closing event>.
End state: <final visible state>.

[Maintain Consistency]
Keep <character identity, number of characters, clothing, prop ownership, spatial direction,
and audio relationships> consistent.
```

### Split by JOB, not only by length

Staging solves *too many events in one paragraph*. It does not solve **two
incompatible jobs in one generation**, and that is a separate cut worth making
[DEMO — Higgsfield "AI Love Stories" tutorial, 2026-08].

The reported case: an arena scene containing a fight (a giant throw, a sword
snatch, a takedown) and, in the same beat, the acting around it (a hidden
worry, a flirtatious exit, hope draining from a face). Run as one prompt it
held — badly, in both directions at once: *"the fight gets softer, the faces get
flatter."* The model spends its attention budget once. Asked to nail physics
and micro-performance in one generation, it half-does each.

Split into **two prompts, one job each, stitched in the edit**:

| Cut it here | Because |
|---|---|
| **physics ↔ performance** | mass, contact and follow-through vs. eyes, breath and micro-expression. Different attention, different optics, usually different shot sizes |
| **action ↔ dialogue** | the same split wearing other clothes |
| **the beat that needs room** | the second reported case: a 30s carnival scene *held* as one prompt, and was still split into 3×15s because the first-touch beat needed room — *"these beats felt completely rushed"*. Length was not the constraint; **pacing** was |

**How to tell which cut you need.** Length-driven splits are decided by
counting events. This one is decided by asking: *what is this shot's dominant
job?* If a prompt has two honest answers, it has two shots in it. That is the
same question the Feasibility Veto asks about a single frame, applied to a
whole generation.

Note the direction of the second case: it fit, and was split anyway. "It
generated" is not the bar — a scene that renders every beat but rushes the one
that matters has failed at the thing you were making it for.

Practical consequence, stated plainly by the same production: **a perfect 30s
render does not exist.** Generate raw footage per job, then assemble. Several
of the finished scenes in that film take the background from one take and the
foreground action from another.

### Timestamps and pacing

Stages are the default. Reach for one-second precision only when a specific handoff,
entrance/exit, transition, or beat must land on a moment.

| Pattern | Use for | Example |
|---|---|---|
| Time range | Allocating pacing to a segment | `0-3 seconds… 3-7 seconds… 7-12 seconds…` |
| Exact time point | One key event | `At 5 seconds, the camera whip-pans rapidly to the left and completes the transition.` |
| Relative timing | A delay between two events | `Three seconds after the character presses the button, the room lights gradually turn off.` |

- Ranges are **consecutive and non-overlapping**, and they are a **time budget**, not a
  frame-accurate edit point — actions may land slightly either side of a boundary.
- Too little content in a range hands the model freedom you did not intend; too much causes
  excessive cutting or dropped events.
- **Never demand a frequency inside one second** ("complete three actions in one second").
  Timestamps allocate time; they do not enforce cadence.
- Every timestamped segment still ends on an explicit end state, exactly like a stage.

> **Relationship to 2.0's beat arithmetic.** `../higgsfield-seedance/SKILL.md` § Output
> Format requires timed beats to sum to the declared duration. That still holds — but sum
> to 4–30s here, and remember that on 2.5 the sum is a budget the model approximates, not a
> cut list it honours to the frame.

---

## Audio and Text — Bracket Syntax

`[OFFICIAL — Dreamina]` Prompts can be written entirely in natural language. Use the
brackets when music, SFX, dialogue, and subtitles must be told apart explicitly:

| Content | Syntax | Example |
|---|---|---|
| Music | `()` | `(Soft, rhythmic piano music plays in the background)` |
| Sound effects | `<>` | `<A bell rings in the distance>` |
| Dialogue | `{}` | `{Hello, welcome back.}` |
| Subtitles | `【】` | `【Chapter One: Departure】` |

**Dialogue language reinforcement.** For non-Chinese dialogue — or when English text comes
back spoken in Chinese, or a specific regional variety is wanted — state it before the line:

```
Dialogue language + regional variety or accent + delivery style + speaker + {dialogue}
```

```
Dialogue language: authentic Los Angeles English. The young man says in natural Los Angeles
vernacular: {No way, you actually made it.}
```

Two house rules carry over from `../higgsfield-audio/SKILL.md` and the film pipeline in
`../higgsfield-seedance/HELL-GRIND.md`:

- **Speech lives in the audio clause only** — not a word of dialogue inside the action
  description, or the model narrates it as behavior. The trap is that writers do not think
  of *subtext* as speech: `they exchange a look that says "you too?"` is a line the script
  never wrote, and it comes back spoken. `[HOUSE — the failing take is timecoded in the
  nutllwhy/seedance-tvc-director evaluation, MIT, 2026-08-09.]` Anything readable is a
  voicing request — quoted subtext, a remembered line, a slogan, a sign read aloud. Write
  the visible behavior instead (*jaw sets, eyes hold*), and note that adding "no dialogue"
  does not undo it: the readable text is still there being asked for.
- **Diegetic-only is a project choice, and 2.5 finally obeys it.** Random subtitles and
  unrequested BGM were 2.0's most-reported nuisance; ByteDance calls suppression of both a
  headline 2.5 fix `[OFFICIAL — Dreamina]`. Still say it — `(no music)` and no `【】` block —
  rather than trusting the improvement.

---

## First-Last Frame and Multi-Keyframe Control

`[OFFICIAL — Dreamina]` On 2.5 these are **prompt statements, not a mode**, because the
platform surface has no start/end-frame media role.

```
@Image 1 is the first frame. It defines the opening composition, subject position, pose,
prop state, scene, and camera direction.
@Image 2 is the last frame. It defines the ending composition, subject position, pose,
prop state, scene, and camera direction.
@Image 3 defines <Subject A>'s <appearance, clothing, structure, or material>. Do not change
the first-frame composition defined by @Image 1 or the last-frame composition defined by @Image 2.

<Describe one continuous action or event>.
The video begins naturally from the first frame defined by @Image 1 and reaches the last
frame defined by @Image 2 after the continuous action.
Between the first and last frames, maintain continuity in <character identity, prop structure
and ownership, scene layout, and camera direction>.
```

Three failure sources, all avoidable:

1. **Never merge the anchors** — `@Images 1 and 2 are the first and last frames` is the
   documented wrong form. One role sentence per image.
2. **First and last images must share an aspect ratio**, or the last frame stretches. The
   output ratio locks to the **first** image; duration stays settable.
3. **Supplementary references supplement only their named attribute** — each one repeats the
   "do not change the first/last-frame composition" clause.

**Multi-keyframe sequences** (3+ ordered stage images) open with `Use @Image 1 through
@Image N as keyframes in this order`, then describe the key state each image represents.
Independent keyframe images align far more reliably than several frames combined into one
grid. Keyframes control **stage order and key states** — they do not reproduce every
intermediate frame.

Storyboard grids and blockout references (coarse vs fine) are the next rung up:
`MODE-PLAYBOOKS.md` § Storyboard grids and § Blockout references.

---

## Editing, Extension, and the Composite Modes

The long templates live in **`MODE-PLAYBOOKS.md`** in this directory. What you need to know
before opening it:

- **Video editing** — define the source as the **sole editing master**, then edit goal, edit
  scope, target material, and the preserve list. Subject replacement additionally needs a
  **Timeline Inheritance** clause so the new object inherits the old one's exact timing,
  path, occlusion, and exit. Background replacement scopes the edit to *outside the
  subject's silhouette*. Audio categories (dialogue, language, voice, BGM, SFX) edit
  independently.
- **Video extension** — the one rule that decides success: **align the boundary frame before
  describing new content.** Forward extension continues from the source's last frame;
  backward extension must land *on* the source's first frame as its explicit end state.
  "Then connect to the source video" is the documented failure phrasing — it leaks later
  elements in early and lets the image drift after it arrives.
- **One-click video** (images → one edited video) — `Material Roles → Image Order → Motion
  Amount → Editing Style → Visual Treatment → Audio`. "Turn these into a video" is never enough.
- **Seamless transitions** (bridge content between two clips) — `Before Video → After Video →
  Trigger Action → Camera Movement → Visual Transformation → Arrival State → Audio`.
- **Transition vocabulary** — natural shot switch · fade in/out · stacking · white/black flash ·
  erase · mask · similar-object · action · dynamic relay · zoom in/out · ink-wash. Each
  named with its own trigger and arrival composition.

---

## Emotional Direction and Camera Terms

`[OFFICIAL — Dreamina]`

**Emotion.** Abstract words ("tense", "warm", "oppressive") set a direction and leave the
rest to interpretation. Pair them with directly visible or audible cues — eye movement, brow
tension, mouth movement, breathing, gaze direction, hand movement. **Two to four cues is
enough for one transition**; listing every facial detail is counterproductive.

```
The overall emotion shifts from <starting emotion> to <ending emotion>.
After <triggering event>, <subject> first shows <immediate observable reaction>.
Then, <eyes, brows, mouth, breathing, gaze, or hand movement> gradually <changes>.
Finally, <subject> expresses <target emotion> through <restrained or explicit outward behavior>.
```

Use event-triggered multi-stage form only when the emotion genuinely changes several times.
For muscle-level control beyond this, `../higgsfield-facs/SKILL.md` (AU codes); for the
behavior-under-pressure layer that makes the cues *mean* something,
`../higgsfield-acting/SKILL.md`.

**Camera terms.** Basic language works directly — shot size (extreme wide / wide / medium /
close-up / extreme close-up), movement (push in, pull out, pan, lateral move, follow, orbit,
dive, dolly out, tilt up, handheld shake), position (low angle, overhead, first-person).

Popular techniques (one-take, dolly zoom, aerial, FPV, bullet time, handheld, bounce speed
ramp) also work directly — but with several subjects in frame, still say **which** subject
the camera follows or orbits, where the move starts, and where it ends.

For a **niche or ambiguous term**, keep the term and translate it into an observable result:

```
Cinematography term + target subject + visual change + foreground/background relationship + direction or speed
```

```
Rack focus: shift focus smoothly from the leaves in the foreground to the person in the
background. The leaves gradually blur while the person's face changes from soft to sharp.
```

For a precise transition moment, add the trigger time, the occluding object, the direction,
and what continues afterwards. Aperture/focal-length/shutter numbers are allowed but the
intended visible result is clearer than a raw value alone.

> **FOV degrees still beat millimetres.** The discrete-anchor FOV bank in
> `../higgsfield-seedance/SKILL.md` § FOV anchors is house doctrine across the Seedance
> family and applies here unchanged.

---

## The Real-Person Character Formula

`[OFFICIAL — Dreamina]` The vendor's answer to "my characters look AI, or look like twins"
is a seven-slot character block. It works for stylized characters too.

```
[Role]  [Skin color / skin texture]  [Facial details]  [Eyes / soul]
[Hairstyle / hair color]  [Clothing / clothing texture]  [Body type / mood / temperament]
[Other requirements, if any]
```

Slot notes:

- **Skin** — carry real texture: visible micro-pores, translucency, capillary flush. This is
  the single slot that most separates "photo of a person" from "AI render".
- **Facial details** — eye shape, brow line, nose bridge, lips, jawline. Specific beats pretty.
- **Eyes / soul** — what the gaze is *doing* and what it carries. Dead eyes are the number-one
  tell; see `../higgsfield-acting/SKILL.md` § Eye life.
- **Body type / mood / temperament** — the body as biography, not a compliment.

> **House override on slot 1.** The source guide labels the first slot `[Age/Race]`. **Do
> not write age.** Engine rule 1 in `../higgsfield-seedance/ENGINE-RULES.md` is age-blind
> characters, and Higgsfield's own feature-film brief gives the reason: the content filter
> tightens sharply the moment it reads a minor. Write **role, build, clothing, and action**
> instead — "a lean courier in a soaked parka", not "a 22-year-old". Ethnicity stays a normal
> descriptive slot; age does not.

---

## Choosing 2.0 vs 2.5

| The job needs | Model |
|---|---|
| 4K or 1080p output | **2.0** (`mode=std`) — 2.5 has no lane above 720p |
| Platform-pinned start / end frame media role | **2.0** |
| A `genre` hint parameter | **2.0** |
| A clip longer than 15 seconds in one generation | **2.5** (up to 30s) |
| Editing a video that already exists | **2.5** (`video_edit`) |
| Extending a clip forward *or backward* | **2.5** (`video_extension`) |
| More than 9 reference images, or >3 reference videos/audio clips | **2.5** (30 / 10 / 10 vs 2.0's 9 / 3 / 3) |
| Cheap 480p prompt validation | either — both cap the draft lane at 480p |

**The honest default:** draft and structure on 2.5 when the job is long, reference-heavy, or
edit-shaped; finish on 2.0 when the deliverable needs resolution. They are not
interchangeable takes — a 2.5 draft validates the *prompt*, not the 2.0 render, for the same
reason `../higgsfield-seedance/SKILL.md` § Drafts Validate the Prompt gives: there is no
seed to pin.

### What carries over from 2.0 unchanged

The engine rules are shared. `../higgsfield-seedance/ENGINE-RULES.md` applies in full —
age-blind characters, exit-frame = implicit cut, off-screen = nonexistent, avoid reflection
shots, ≤3 tracked characters, double-contrast cuts, micro-expressions as physics. So do the
positive-phrasing law (Seedance has no negative-embedding architecture in either version),
the homograph trap, and the block scaffold for production-scale briefs.

---

## Hard Limits — Do Not Over-Promise These

`[OFFICIAL — Dreamina]`

- **Timestamps allocate time; they are not frame-accurate edit points.** Never imply a beat
  will land on an exact frame.
- **Video-editing prompts raise the probability** that critical events align with the source —
  they cannot guarantee frame-by-frame overlap.
- **Multi-reference selects and combines** the right materials per scene; it does not make
  every material appear at once.
- **Frame-level text accuracy is not promised.** Subtitles, formulas, signs, and product
  specs need prepared reference materials plus post — the same conclusion as 2.0's text-rendering
  high-risk row.
- **Video editing locks the input's aspect ratio and approximate duration**; output may differ
  by up to ~0.3s from transition-frame handling.
- **First/last-frame generation locks aspect ratio to the first image**; mismatched ratios
  stretch the last frame.
- **Video extension locks aspect ratio to the source**; the extended segment's audio volume may
  differ slightly.
- **Boundary frames connect naturally, not identically** — review both sides of the seam plus
  the whole extended segment.
- **Seamless transitions aim for visual and audio continuity**, not pixel-identical preservation
  of either source clip.

---

## Dreamina-Only — What Higgsfield Does Not Expose

`[DREAMINA-ONLY]` These exist in ByteDance's own Dreamina/Jimeng product and appear in the
guides, but there is **no Higgsfield parameter behind them** on the 2026-08-07 snapshot. Do
not offer them here.

| Dreamina feature | Status on Higgsfield | Closest thing that does work |
|---|---|---|
| **Ultra Long Video** — 30–180s in one generation | Not exposed; `duration` caps at 30 | Stage a 30s generation, then chain `video_extension` |
| **Nested extension to 60s** via repeated UI operations | The *model* rule (source ≤30s → extend up to 30s) holds; the one-click nesting UI does not exist | Chain `video_extension` calls, re-checking the boundary each time |
| **Edit with marks / Advanced Edit** — box, arrow, brush, anchor annotations on a frame | Not exposed; there is no annotation channel | `video_edit` with a written scope: object + change + effective time range |
| **Clay Renderer plugin** — white-model rendering workflow | Not exposed as a plugin | Coarse/fine blockout prompting via `omni_reference` (`MODE-PLAYBOOKS.md` § Blockout references) |
| Native 180s / multi-minute deliverables | — | Generate in 30s pieces and assemble in post (`../higgsfield-pipeline/SKILL.md`) |

**Extension chain math.** The model-side rule is: a source **within 30 seconds** can be
extended by 4–30 seconds in one operation, so a 30s source plus a 30s extension is the
60-second ceiling for a single chain. Beyond that, re-anchor from the original references
rather than extending an extension — the same degradation curve as 2.0's chain cap in
`../higgsfield-seedance/SKILL.md` § Extension Prompting.

---

## Pre-Submission Checklist

`[OFFICIAL — Dreamina]`, plus the house preflight. Only the rows for techniques actually used:

- [ ] Subject and primary action or event stated plainly
- [ ] Every reference states what to use **and** what not to use
- [ ] Every character, product, and prop named and bound to a specific material
- [ ] References selected **per scene**, not all required at once
- [ ] Each long-video stage has one primary change and a clear end state
- [ ] Character count, clothing, prop ownership, and spatial relationships consistent throughout
- [ ] Editing prompts define the sole master, edit scope, target quantity, and preserve list
- [ ] Abstract emotions and niche camera terms paired with observable cues
- [ ] First/last frames: one role per image, matching aspect ratios, anchors not merged
- [ ] Storyboards state which structure to inherit, not literal panel reproduction
- [ ] Blockouts: coarse vs fine identified first, inheritance list stated
- [ ] Auto-locked parameters respected for edit / first-last / extension
- [ ] Extension: boundary frame, motion trend, and audio continuity all checked
- [ ] One-click video: roles, order, motion amount, editing style, audio all defined
- [ ] Transitions: both clips' roles, trigger, process, and arrival state defined
- [ ] No age words anywhere (engine rule 1)
- [ ] `seedance_lint.py --preflight --model seedance_2_5` run and clean

---

## Related Skills

- `../higgsfield-seedance/SKILL.md` — Seedance 2.0 director: the filter model, block scaffold,
  FOV anchors, prompt-craft laws, engine rules. **Everything model-agnostic lives there.**
- `../higgsfield-seedance/ENGINE-RULES.md` — the shared hard rendering constraints
- `../higgsfield-seedance/HELL-GRIND.md` — Higgsfield's open-sourced feature-film pipeline
  (assets, GEO spatial layout, dialogue construction, iteration discipline)
- `../higgsfield-acting/SKILL.md` — performance: objective, obstacle, tactics, beats, eye life
- `../higgsfield-facs/SKILL.md` — facial control by Action Unit code
- `../higgsfield-seedance-vfx/SKILL.md` — video-to-video footage transforms on 2.0
- `../higgsfield-models/SKILL.md` — model choice against the specs layer
- `../higgsfield-pipeline/SKILL.md` — assembling 30-second pieces into a longer deliverable
- `MODE-PLAYBOOKS.md` — the editing / extension / one-click / transition / blockout templates
- `VFX-PIPELINE.md` — the AI-VFX production pipeline: asset-class model routing, the size-ref
  frame, location batching, the `omni_reference` v2v lane, the four-batch rule, the slop catalog
