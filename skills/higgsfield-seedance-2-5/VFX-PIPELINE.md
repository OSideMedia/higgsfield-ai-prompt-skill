# Seedance 2.5 — The AI-VFX Pipeline

`SKILL.md` in this directory is the **dialect** — modes, reference-role grammar, staging,
bracket syntax. This file is the **pipeline**: how a whole VFX shot actually gets built
when the job is "replace a 3D/compositing pipeline with generation", and what the failures
look like on the way.

It is the answer to a specific brief — put a real person into real plate footage, put them
on a creature that does not exist, and fly them through a waterfall, frame for frame —
followed by the same shots built with no plate at all. The doctrine below is what survived
that build.

> **This is a production layer, not a second dialect.** Everything here is written *in*
> the grammar of `SKILL.md`. The block scaffold (`SCENE CONTEXT → … → POSITIVE LOCKS`),
> FOV-in-degrees, distributed style, the CAMERA-3rd-position rule and the prompt-craft
> laws are house doctrine in `../higgsfield-seedance/SKILL.md` and carry across to 2.5
> unchanged. Do not restate them here — read them there.

## QUICK FACTS
*Generated-checked block (scripts/build_index.py verifies anchors). Routing aids — read the linked sections for the rules themselves.*
- The pipeline is **images first, then video**, always — a shot is only as good as the still it was built from [→](#the-pipeline-images-first-then-video)
- One model per **asset class**, not one model for the project: faces + fixes → Nano Banana 2 · creatures → Seedream 5.0 · clothing → GPT Image 2 · locations → Soul Cinema [→](#stage-1--assets-one-model-per-asset-class)
- Character sheets go on a **plain grey background**; creature sheets carry **two close-ups, mouth open and mouth closed** [→](#stage-1--assets-one-model-per-asset-class)
- The **face-lock crop**: crop the head out of the full-body frames so the model has exactly one place to pull the face from [→](#the-face-lock-crop)
- Scale does not survive on words — build a **size-ref frame**, save it as its own asset, attach it to every scene, and lock "if scale is uncertain, render smaller" [→](#stage-2--the-scale-law-a-size-ref-frame)
- Locations are **batched cheap and selected by light** — bad light in the still is why the video comes out as slop [→](#stage-3--locations-batch-cheap-select-by-light)
- Field v2v runs in **`omni_reference` with a video reference, not `video_edit`** — which is why duration is settable, and must equal the source [→](#stage-4--footage-transformation-the-omni_reference-v2v-lane)
- Source clip **≥ 4 s** (the model's own duration floor); pad a shorter one by freeze-framing its last frame [→](#stage-4--footage-transformation-the-omni_reference-v2v-lane)
- **The four-batch rule**: the same defect in all four batches is a prompt or source fault — more batching only burns credits [→](#stage-5--when-v2v-fails-the-four-batch-rule)
- v2v cannot invent an action the plate has no anchor for; fall back to **i2v from a location screenshot** and write a deliberate **empty-frame pause** as the stitch point [→](#stage-5--when-v2v-fails-the-four-batch-rule)
- "Make it more natural" does nothing — the fix is a **physical picture** of the movement [→](#the-slop-catalog)
- The tells that give a shot away — the CG-double fall, the origami wing, the warped logo — and what each one is asking you to write [→](#the-slop-catalog)
- Direction patterns from the build: open mid-action, the cloud-punch opener, the high-speed kit, emotion with no video reference, the voice lock [→](#direction-patterns-from-the-build)

---

## Provenance

| Label | Source |
|---|---|
| `[FIELD — AI-vs-VFX, 2026-08-08]` | Higgsfield's *AI vs VFX: Can Seedance 2.5 Beat VFX?* build — blog write-up + the 25-minute production video, host Adil, plate footage by VFX artist Erik. Every shot in it was generated on Seedance 2.5. |
| `[OFFICIAL — prompt-builder 2.5]` | `prompt-builder-2-5.skill`, the prompt skill Higgsfield published alongside that build. |
| `[OFFICIAL — platform]` | Higgsfield's live `models_explore` catalog, snapshot **2026-08-07** (`../../specs/model-specs.json`). |

Where the field build and the platform snapshot disagree about what is *settable*, the
snapshot wins (HARD RULE 3). The field build is authoritative about what **works**, not
about what the API accepts.

---

## The pipeline: images first, then video

`[FIELD — AI-vs-VFX, 2026-08-08]` Every shot in the build — plate-based and fully
generated alike — went through the same two stages, in the same order:

```
1. ASSETS      character sheet · creature sheet · size-ref frame · location stills
2. VIDEO       one Seedance 2.5 generation per shot, every asset attached by role
```

The consequence worth saying out loud to a user before they spend a credit: **a bad still
cannot be rescued by the video prompt.** A location plate with wrong light produces a slop
video no matter how well the motion is written, and the cheap fix is upstream — regenerate
the still, not the shot.

The second-order consequence is the reason the asset stage is worth its own discipline: an
asset is generated once and referenced in every shot that needs it. A flaw you accept at
the sheet stage — a warped logo, a face that drifts, an ambiguous scale — is a flaw you
then pay for in every generation downstream.

---

## Stage 1 — Assets: one model per asset class

`[FIELD — AI-vs-VFX, 2026-08-08]` The single most repeated correction in the build is that
there is no "best image model" for a project — there is a best model **per asset class**,
and switching between them mid-project is the normal case, not a fallback.

| Asset class | Model | Why this one |
|---|---|---|
| Human character sheet, face matching | **Nano Banana 2** | Strongest face match on the platform |
| Small corrective edits to an existing sheet | **Nano Banana 2** | Holds its input images best — the model to switch *to* when something needs fixing rather than rebuilding |
| Fantasy creature / non-human character sheet | **Seedream 5.0** | Best at fantasy creatures |
| Clothing, wardrobe changes, branded garments | **GPT Image 2** | Handles clothing best |
| Locations and environment stills | **Soul Cinema** | Most cinematic frames; GPT skews yellow, Nano Banana makes locations too clean and too symmetrical |

Full specs, pricing and UI controls for each of these live in `../../image-models.md`;
this table is the *routing*, not the reference.

Three construction laws come with the table:

**Character sheets go on a plain grey background.** Not a set, not an environment, not a
gradient — plain grey. Sheets built on a busy background cost credits in re-rolls
downstream, because the video model has to decide which parts of the sheet are the
character and which are the world. `[FIELD — AI-vs-VFX, 2026-08-08]`

**Creature sheets carry two close-ups: mouth open and mouth closed.** A creature detailed
enough to be interesting is detailed enough to glitch between expressions — a jaw that
reshapes the skull when it opens. Two head close-ups at the same angle, one closed and one
in a full roar, pin both extremes and stop the face reorganizing itself mid-shot. The
canonical sheet is three panels: full body in flight, head closed, head open.
`[FIELD — AI-vs-VFX, 2026-08-08]`

**Small fixes are a model switch and one line, not a bigger prompt.** When a sheet comes
back with a warped logo or a color cast, do not rewrite the generation prompt — attach the
flawed sheet plus the correct asset to Nano Banana 2 and write the single sentence:
`change the logo to the one in image two`. Re-prompting the whole sheet re-rolls
everything that was already right. `[FIELD — AI-vs-VFX, 2026-08-08]`

### The face-lock crop

`[FIELD — AI-vs-VFX, 2026-08-08]` A three-panel sheet gives the model three faces to
average: a front full-body, a back full-body, and a close-up. At full-body scale the face
is a few dozen pixels, so averaging it in drags the identity toward generic.

**Crop the heads out of the full-body frames.** The sheet keeps its full-body panels for
build, silhouette and wardrobe; the close-up becomes the only place a face can be read
from. One source of truth for identity, at the only resolution where identity is actually
resolved.

This composes with, and does not replace, the reference-role discipline in `SKILL.md` —
the crop reduces what the model *can* misread; the role sentence tells it what to read.

---

## Stage 2 — The scale law: a size-ref frame

`[FIELD — AI-vs-VFX, 2026-08-08]` Relative scale between two subjects is the first thing
to drift and the last thing words can fix. A rider written as "tiny compared to the
enormous dragon" comes back a different size in every generation, and the drift is worst
on wides — which is exactly where scale is the whole point of the shot.

The fix is an image, not a sentence. **Build a size-ref frame:**

1. Take the creature sheet, the character sheet, and a screenshot from a generation whose
   scale was right.
2. Merge them into **one** reference image showing the pair mounted/positioned together —
   the field build used a three-panel version (wide side profile, three-quarter front,
   close-up of the mounting point).
3. Write the proportion into that image's own prompt in **human-height comparisons**, not
   metres: *"wingspan as wide as twenty humans lying head to toe; the dragon's head alone
   is longer than the rider's entire body."*
4. Save it as its **own named asset** and attach it to every shot that contains both
   subjects, with a role sentence that makes it proportion-only:

```
@size-ref: single image of the same rider mounted on the same dragon in flight — this is
the exact rider-to-dragon proportion to reproduce: body length about 12x and wingspan
about 14x the rider's height, the rider a tiny figure mounted low on the shoulders at the
base of the neck. Match this proportion in every frame. Ignore this image's background,
lighting and grade.
```

Two locks earn their place next to it:

- **The asymmetry lock.** `If scale is uncertain, render the rider SMALLER, never larger.`
  Scale errors are not symmetrical in how they read — an undersized rider reads as
  distance, an oversized one reads as fake.
- **The no-resize lock.** When the size-ref is built by *editing* a creature frame, say
  `do not shrink, resize or move the dragon` — otherwise the model solves the proportion
  by shrinking the wrong subject.

> This is the 2.5 form of the scale-drift lock in `../higgsfield-seedance/SKILL.md`
> § Positive Locks. There the counter is a standing sentence; here, with 30 image
> references available, it is a dedicated asset — which is stronger, because a proportion
> shown cannot be paraphrased.

---

## Stage 3 — Locations: batch cheap, select by light

`[FIELD — AI-vs-VFX, 2026-08-08]` Location stills are the cheapest place in the whole
pipeline to iterate and the most expensive place to get wrong.

**The economics drive the method.** Seven credits buys one GPT Image 2 generation, or
**56 Soul Cinema variations**. At that ratio the correct behaviour is not to write a
better prompt — it is to batch wide, then judge.

**Judge on light, before anything else.** The rejection reasons from the build, in the
order they came up:

| Rejected because | What it looked like |
|---|---|
| Plasticky, sun rays breaking through unnaturally | The scene is overcast — the light should be soft, and a hard sun contradicts the plate |
| Clouds badly placed, image too dark | Composition is fine, exposure kills it |
| Light falls nicely on the plain but not on the waterfall | The subject of the shot reads as a hole |
| **Accepted** | Focus on the waterfall, water reads blue, overcast but not dark |

**Bad light in the still is why video generations come out as slop.** That is the whole
rule. A location whose key is wrong will fight every lighting clause in the video prompt,
because the video model is matching the reference, not the paragraph.

**Test the finalists in video before locking one.** A still that reads well can still
animate badly. Spending one short generation on each finalist is cheaper than discovering
it in the hero shot.

### Reverse-angle locations

A scene almost always needs the same place seen from the other direction — the inside of
the cave you were just looking into, the far end of the room, the street from the opposite
kerb. Generate it as a *matched* location, not a new one: attach the locked location asset
and write an explicit carry-over list.

```
Reverse angle of the exact same basalt cave as in the reference image — same location,
same materials, same color grade, now facing the opposite direction: the dead-end back of
the cave.
MATCH TO REFERENCE — carry over exactly:
— the same rough black basalt of the ceiling and walls: layered, horizontally streaked,
  wet sheen, identical texture scale;
— the same floor: dark grey-brown fine volcanic gravel, matte and slightly damp,
  identical grain size and tone;
— the same cold overcast palette: graphite black, wet slate grey, muted earth-brown;
  fine film grain and soft naturalistic contrast identical to the reference frame.
```

Name the **materials, the grain size, the palette and the grade** — the four things that
give away two shots as different places. State what the new angle does *not* contain
("this side is completely sealed solid rock: no second opening, no daylight gap, no
waterfall anywhere in frame"), because the model will happily invent a second exit rather
than commit to a dead end. That instinct is environment invention, drift source #1 in
`../higgsfield-seedance/SKILL.md` § Positive Locks.

---

## Stage 4 — Footage transformation: the `omni_reference` v2v lane

This is the section that changes how a plate job gets routed.

`[FIELD — AI-vs-VFX, 2026-08-08]` The build's video-to-video shots — replace the man in
this clip with my character, keep every other pixel — were **not** run as `video_edit`.
They were run as **`omni_reference` with the source clip attached as a video reference**,
in the ordinary block scaffold, with `@video1` declared master in prose:

```
@video1 — source footage: master for camera, framing, focus, motion, expression timing,
background, lighting, grain and duration.
@adil-hiking — replacement character: <minimal identity anchor>. 100% matches the reference.
```

Three operating facts fall out of that routing, and none of them are true of `video_edit`:

**1. Duration is settable — and must equal the source.** `[FIELD]` *"Set the duration to
four seconds to match the reference. Anything longer and the AI starts guessing."* In
`omni_reference` the duration is a real parameter, so an over-long setting is an
instruction to invent footage past the end of the plate. `video_edit`, by contrast,
ignores `duration` entirely and bills by the master's length (`SKILL.md` § The Higgsfield
Parameter Surface).

**2. The source clip must be at least 4 seconds long.** `[FIELD]` This is not an arbitrary
threshold — `duration` has a hard **minimum of 4 s** `[OFFICIAL — platform]`, so a 2-second
plate cannot be duration-matched at all. **Pad a short clip by freeze-framing its last
frame** out to 4 s, then match. Cutting a long plate into segments and padding the short
ones is the normal prep step, not a hack.

**3. The preserve half is written as prose locks, not an `[Edit Scope]` block.** The
scaffold's `POSITIVE LOCKS` carries it: *"every pixel outside the replaced man remains
exactly as in @video1, including the empty-wall ending. Duration and all action timing
unchanged."*

### Which lane for which job

| The job | Lane |
|---|---|
| Swap a subject / add an element while inheriting the plate's performance frame-for-frame, plate ≥ 4 s | `omni_reference` + video reference, duration = source |
| Change one scoped thing inside a master whose timeline must survive untouched (a wall's light colour from 4–7 s, remove the music) | `video_edit` — `MODE-PLAYBOOKS.md` § Video editing |
| Rebuild the shot from the ground up, old clip as motion guidance only | `omni_reference` — `SKILL.md` § The Mode Router, rule 2 |
| Plate is Seedance **2.0** work (4K needed, platform start/end frame, genre hint) | `../higgsfield-seedance-vfx/SKILL.md` |

### The performance-inheritance clause

The clause that makes a swap read as a swap rather than a re-shoot is an explicit
frame-by-frame inheritance sentence — the `omni_reference` twin of the Timeline
Inheritance clause in `MODE-PLAYBOOKS.md`:

```
The man from @adil-hiking takes the original man's place and inherits his exact performance
frame by frame: same body position and posture, same head angle, same wide-eyed stare and
open-mouth shock expression with identical mouth aperture and blink timing, same stillness
during the hold, and the same fast straight-down drop out of frame at the exact same frames
with matching motion blur. Silhouette scale and screen position match the original at every
frame.
```

Then a `STYLE` clause whose job is integration, not look: *"grain, motion blur, focus
falloff, compression character and color match @video1 so the replaced man is
indistinguishable from originally shot footage."* This is what replaces keying, despilling
and grain-matching — say it, or the model composites cleanly and the shot reads pasted-in.

---

## Stage 5 — When v2v fails: the four-batch rule

`[FIELD — AI-vs-VFX, 2026-08-08]` The dragon-catch shot failed across **all four batches**.
The lesson generalises into the most credit-saving rule in the build:

> **If the same defect shows up across all four batches, the fault is the prompt or the
> source. Batching further is burning credits for nothing.**

The diagnostic that follows is about **anchors**: v2v inherits motion from the plate, so it
can only render an action the plate has an anchor for. There was no jump moment in the
source footage — so a prompt asking for a jump had nothing to inherit and turned to slop
every time. No amount of re-rolling creates an anchor that was never filmed.

**The fallback is image-to-video, and it is a downgrade in continuity, not in quality:**

1. Screenshot a frame of the location out of the plate.
2. Use it as the **starting frame** — declared in the prompt, not as a mode
   (`SKILL.md` § First-Last Frame and Multi-Keyframe Control).
3. Write the action from scratch, since nothing is being inherited any more.
4. Stitch the i2v shot to the v2v shot in the edit.

### The empty-frame pause

Step 4 is where the pattern earns its keep. **Write a deliberate empty beat into the prompt
at the point you intend to cut** — 1 to 1.5 seconds of location and nothing else:

```
… falling fast with real gravity, disappearing below the ledge. Then a pause: for about
1.5 seconds the frame stays completely empty, only the waterfall and drifting mist.
Suddenly @dragon-v3 bursts up from the abyss …
```

An empty frame is a clean cut point: no subject to match across the join, no continuity to
hold. Planning it into the generation is cheaper than hunting for one in the timeline
afterwards — and it doubles as a tension beat, which is why the same device appears
deliberately in the fully-generated half of the build (a one-second hold on an empty cliff
lip before the creature erupts into frame).

---

## The slop catalog

`[FIELD — AI-vs-VFX, 2026-08-08]` Each tell below is a rejection criterion *and* a
prompt-side instruction. Learning to name them is what converts "this looks fake" into a
line you can write.

**"Make it more natural" does nothing.** It is the archetypal non-instruction: no observable
target, nothing to render. Replace it with a **physical picture** of the movement — what
travels through the body, in what direction, at what rate:

> *"the body undulates like a worm swimming through the air: with every wingbeat a wave of
> motion travels along its spine — the chest lifts, then the wave rolls through the belly,
> hips and down the tail"*
>
> *"its head rapidly rotates back and forth around its own axis — a twisting rotational
> shake, like a dog shaking water off — and the twist travels down the neck as a spiral
> wave, the loose skin and neck spikes wobbling with the rotation, flinging spray outward
> in a spinning radial cloud"*

This is the same law as `../higgsfield-seedance/SKILL.md` § Prompt-Craft Laws — write the
visible — applied to motion specifically. **Motion physics is the load-bearing clause in a
VFX shot**: always specify the physical movement rather than the adjective for it.

**The origami wing.** A generated creature limb comes back reading low-poly: flat facets,
sharp corners, straight folds where there should be a curve. The counter is written as
surface behaviour — *high-poly, smooth organic muscle curves, no sharp corners, no flat
planes* — plus what the material does under load (spars bending under each downstroke,
membranes bellying then snapping flat with tension wrinkles).

**The CG-double fall.** The single most reliable giveaway in traditional VFX, and it
transfers straight to generation. There are **only two ways a person goes off a cliff**:
step off vertically, feet first, or push off and dive. Anything else — tipping over into a
stiff soldier pose, descending at one constant speed, with nothing moving in the clothes —
reads as an asset dragged from A to B, and a viewer catches it without being able to name
it. Write the fall as one of the two real options, with **acceleration** and with the
clothes doing something.

**Bad light in the still.** Covered in Stage 3, listed here because it belongs in the same
mental checklist: the most common cause of a slop video is a location plate that was
already wrong.

**Image-stage tells.** Warped logos and blue-ish colour shifts are the two that recur.
Both are Nano Banana 2 one-line fixes (Stage 1) — but only if you *look* for them before
the sheet is locked and referenced by forty downstream shots.

**Take-selection tells.** When several takes of a performance come back usable, the field
rejections were: overacting on the closing beat, a run that is too aggressive for the
emotion, an unnecessary head movement, and a smile that contradicts the mood of the scene.
All four are performance notes, not technical faults — which is the point. Judge a take
the way you would judge an actor.

---

## Direction patterns from the build

`[FIELD — AI-vs-VFX, 2026-08-08]`

**Open mid-action.** A generated opening frame wants to be an establishing beat, and an
establishing beat is dead air. For a shot that starts on an event, put the event in the
first second and say so: *"the veil is already bulging in frame one and the dragon breaks
through within the first second — no long empty establishing beat, no cave interior, no
approach shot."* The first frame carries state, not setup.

**The cloud-punch opener.** The counterpart for a shot that genuinely is an establisher: a
beautiful static frame is not a scene one. Give the camera something to break *through* —
open inside a cloud deck in full whiteout, push forward and down, tear out of the cloud
base, and let the vista resolve in one continuous reveal. The reveal is the shot; the
location is what it reveals.

**Emotion with no video reference.** When there is no plate to inherit a performance from,
describe the face at the level of what the body is actually doing — what the character is
going through, **what he says**, **how the voice sounds**, and **what his hands are doing**.
The build's cave monologue works because it specifies the swallow, the twitching fingers,
the aborted false start, the shaken-out hands, the trembling exhale, and only then the
sprint. Beat-level acting direction lives in `../higgsfield-acting/SKILL.md`; this is the
2.5 note that it must be written *out*, because there is no reference doing it for you.

**The voice lock.** `[FIELD]` 2.5 locks the **voice** together with the appearance in the
character sheet. Reuse the same sheet reference across generations and the voice stays
consistent — so describe the voice once, in the character's role sentence, rather than
re-specifying it in every prompt. `[OFFICIAL — prompt-builder 2.5]` states the same rule.

**The high-speed kit.** For chase and fly-by shots, three clauses do most of the work:
a **180° camera orbit** around the subject, **speed shake** (a constant fine vibration with
discrete jolts on top), and **lens droplets** that land, stay, tremble and streak like a
hard-mounted action camera. Two locks keep the kit from eating the shot: the orbit path
itself stays smooth and machine-driven with the shake living on top of it, and the
droplets must refract without hiding the action.

**Let the model improvise the background — deliberately.** On high-speed shots, background
detail can be left unspecified as long as improvisation cannot break the story. This is a
budget decision, not laziness: the words you save go into the subject, the physics and the
performance, which are the parts a viewer is actually looking at.

---

## Cost and effort anchors

`[FIELD — AI-vs-VFX, 2026-08-08]` Useful when a user asks what this replaces. Quote as
comparisons from the build, not as a quote for their job.

| Step | Traditional pipeline | This pipeline |
|---|---|---|
| Creature asset | Sculpt → retopology → UV unwrap → rig before you can animate; buying a model still leaves you animating it | Character sheet generated in about a minute for roughly 40 cents |
| Character into a plate | Key (curly hair by hand) → despill → composite → match light, shadows, grain | One reference sheet + one prompt; the model matches light and contrast to the plate |
| A person going off a cliff | CG double: cloth sim, physics, body-mass and trajectory, plus rotoscoping the midground — for a two-second shot | One prompt, written with a real fall |
| Creature animation | Build the 3D scene, match lighting, animate every part of the rig; the standard software alone runs to ~$3,000/year | A rewrite and a generation |
| Volumetric clouds reacting to a creature | Millions of particles, hundreds of gigabytes, render farms per second of footage | In the prompt |

The build's own framing for the second half — a fully generated cinematic with no plate at
all — is that a studio would quote **at least $50,000** for it.

---

## Related

- `SKILL.md` — the 2.5 dialect: modes, reference roles, staging, bracket syntax, limits
- `MODE-PLAYBOOKS.md` — `video_edit` and `video_extension` order forms, storyboards, blockouts, transitions
- `../higgsfield-seedance/SKILL.md` — house prompt doctrine: block scaffold, FOV anchors, distributed style, prompt-craft laws, positive locks
- `../higgsfield-seedance/HELL-GRIND.md` — the feature-film pipeline (asset construction at film scale, iteration discipline)
- `../higgsfield-seedance-vfx/SKILL.md` — the **2.0** video-to-video lane (4K, `mode=std`)
- `../higgsfield-character-design/SKILL.md` — what goes on the sheet before any model runs
- `../higgsfield-acting/SKILL.md` — performance construction for the emotion beats
- `../../image-models.md` — full specs for Nano Banana 2, Seedream 5.0, GPT Image 2, Soul Cinema
