---
name: higgsfield-seedance
description: "Rewrites scene descriptions using professional cinematography language, structures prompts with a six-slot formula (camera + subject + action + setting + style + lighting), and diagnoses content filter rejections via a preflight linter. Use whenever the user asks for a Seedance 2.0 / Seedance Pro prompt, describes a scene for Seedance generation, mentions Seedance, reports a Seedance generation failure or flagged prompt, or is burning credits on Seedance regenerations."
user-invocable: true
metadata:
  tags: [higgsfield, seedance, seedance-2.0, seedance-pro, content-filter, prompt, director, flagged]
  version: 1.5.0
  updated: 2026-05-17
  parent: higgsfield
---

# Higgsfield Seedance Director

Use this skill whenever the user wants a Seedance 2.0 / Seedance Pro prompt, OR
whenever a Seedance generation has been blocked, flagged, or silently failed.
This skill's job is to stop credit waste on filter rejections.

---

## The Filter Model — Read This First

Seedance 2.0's content filter is **not** a keyword blacklist. It is a language
model that reads the full prompt as a single scene and judges intent and context.
Most users burn hours swapping individual words — that loop does not work.

The filter compares two things:

- **A prompt that reads like a filmmaker describing a shot** → tends to pass.
- **A prompt that reads like a note to a friend** → tends to fail.

A word that looks sensitive in isolation can sit inside a well-constructed
cinematic prompt without issue — the filter reads the full picture. A prompt
with no picture to read (no setting, no visual purpose, no narrative logic)
gives the filter nothing to work with, and it errs on the side of caution.

**Practical rule:** the prompt must describe a **scene**, not a **subject**.
Fix the voice first, then fix the words.

---

## Instant Fail vs. Delayed Fail — the Diagnostic

This single heuristic saves time on every failure:

| Failure timing | Meaning | What to do |
|----------------|---------|------------|
| **< 10 seconds** (instant) | Content filter rejection — prompt never reached the GPU | Rewrite for voice + remove risk tokens. Do not regenerate unchanged. |
| **> 30 seconds** (delayed) | Infrastructure, timeout, or complexity — prompt passed the filter but the render failed | Simplify action density, cut length, try again |

If the user is seeing **instant fails in a loop**, it is a filter issue — never
a GPU issue. Stop them from regenerating before the rewrite.

---

## The Seedance Prompt Formula

Every Seedance prompt should hit these six slots, in this order:

```
[Camera movement] + [Subject] + [Action] + [Setting] + [Style] + [Lighting]
```

All six are technically optional — but a prompt that includes all six almost
never gets flagged, because the filter has full context to interpret every
word. A prompt missing 3+ slots is where flags come from.

### Minimum viable Seedance prompt

> **Slow dolly-in on a figure in a dark overcoat standing alone at the end of
> a rain-slick alley. Cold teal shadows, single practical streetlamp, shallow
> depth of field.**

Camera ✓ Subject ✓ Action ✓ Setting ✓ Style ✓ Lighting ✓ — all six slots, ~30
words, passes the filter because the scene is fully legible.

---

## Seedance 2.0 Prompt Modes

Seedance 2.0 exposes five generation modes that each take the six-slot formula
but apply it to a different starting point. Picking the right mode is upstream of
prompt writing — the same sentence will produce different results in different
modes, because each mode reads the prompt as a different kind of instruction.

### Reference-Based

The prompt builds a scene around a source image that carries the visual identity —
character, wardrobe, palette, sometimes composition. The prompt's job is NOT to
re-describe what the image already shows; it's to place the subject into a new
action, setting, or motion context. This is the workhorse mode for any sequence
that needs a consistent character across varied shots.

```
[Source image role: "as the main character" / "as the starting frame"].
[Action the subject performs]. [Environment and atmosphere if not visible in source].
[Camera movement]. [Lighting cue if different from source].
```

### Continuation

The prompt extends a prior Seedance generation forward in time, picking up at the
final frame of the previous clip. Identity, wardrobe, environment, and emotional
state all carry over. The prompt should describe what happens NEXT — never what
just happened. For the full five-rule construction pattern, see the Continuation
Prompt Formula section directly below.

```
[Continuing from prior clip]. [New action that follows from the last frame].
[Camera direction for the continuation]. [Any state change — light shift, new beat].
```

### Expand Shot

The prompt grows the canvas or spatial extent of an existing frame — pulling the
frame boundaries outward to reveal what's beyond the original edges. This is NOT
a time extension (that's Continuation) and NOT a zoom-out camera move within the
original generation. It rewrites the frame itself to include more scene. Useful
for turning a tight composition into a wider establishing shot without
regenerating from scratch.

```
[Source frame reference]. Extend the scene [direction: outward / upward / leftward].
[What appears in the newly revealed area]. [Preserve the original subject/composition].
```

### Edit Shot

The prompt modifies specific elements of an existing generation while everything
else stays exactly as it was. Think of it as a targeted patch: change a jacket
color, remove a background figure, swap a prop, adjust a facial expression.
Identity, camera, composition, and lighting stay locked unless you explicitly
name them in the change list. The Keep Rule matters here: always state what to
preserve alongside what to change.

```
Change [specific element] to [new state]. Keep [everything else] unchanged.
[Preserve identity, composition, lighting, and camera behavior from the original.]
```

### Transformation

The prompt describes an explicit state change inside a single clip — the subject,
object, or environment visibly becomes something else within the shot's
duration. Distinct from Continuation (which extends time across two clips) and
from Edit Shot (which modifies a generated clip after the fact). Transformation
happens *during* the generation, in one continuous take. Use it when the shot's
core idea is the change itself: a character morphing, an object decaying, a
landscape shifting from one season to another. The skeleton below is written
for character → character; the same pattern applies to object → object and
environment → environment with the relevant noun substituted.

```
[Subject in starting state — full identity descriptors]. [Triggering moment or
cue]. [Subject mid-transformation — what visibly changes, in observable
physical terms]. [Subject in ending state — new identity descriptors].
[Camera behavior across the change]. [Lighting / palette shift if any].
```

The transformation must be one continuous arc, not a cut. Describe the
intermediate state explicitly — the model needs a midpoint anchor or it will
either snap from start to end (looks like a cut) or render an ambiguous blur.
Keep the duration short (5–8 seconds is the sweet spot for a single
transformation); longer clips drift.

### Mode Selection Rule

Reference-Based for new action with an existing character. Continuation for the
next beat in time. Expand Shot to widen the frame spatially. Edit Shot to patch
specific details. Transformation prompt mode when the shot's core idea is a
state change inside a single clip — the change is the content. If you find
yourself writing across multiple modes in one prompt — stop, pick one,
generate, then use the output as input to the next mode.

---

## Continuation Prompt Formula

When writing a Continuation mode prompt, apply these five rules. Skipping any of
them is the most common cause of continuation failures: identity drift across the
boundary, re-played actions, environment shifts, and broken emotional through-lines.

### The Five Rules

1. **Last-frame anchor.** Open the prompt with a short description of what the
   camera sees in the final frame of the prior clip — the pose, the position in
   frame, where the character is looking. This tells the model where to start
   rendering from. One sentence is enough.

2. **Identity anchor.** Paste the character's identity block (the same paragraph
   you used in the original prompt) verbatim into the continuation prompt. Do
   not paraphrase it. Do not shorten it. Continuation boundaries are where
   identity drifts — a verbatim re-paste gives the model no room to reinterpret.

3. **Prior clip as secondary memory.** Name what just happened in one line —
   "following the door opening," "after the punch lands," "continuing from her
   turn toward the window." Do not re-describe the action in detail. One
   referential phrase, then move on.

4. **Immediate continuation.** Start the new action on the frame that follows
   the prior clip's final frame. No time skip, no fade, no implied cut — unless
   the user has explicitly asked for one. If they want a skip, describe it as a
   new shot instead.

5. **No action repeat.** The new prompt must extend, not loop. If the prior clip
   ended on her drawing her weapon, the continuation does NOT describe her
   drawing her weapon — it describes what she does with it next. Repeating a
   described action is what causes the "previous beat replays" symptom.

### What Must Carry Over

Across the continuation boundary, preserve: character identity (face, build,
distinguishing marks), wardrobe (every garment and accessory), environment
(architecture, light quality, color treatment, ambient particulates), and
emotional carryover (the state the character was in at the last frame — tense,
exhausted, alert — should still read on their body in the opening of the
continuation).

> For the eight named substrate channels that "emotional carryover"
> decomposes into, see `../../vocab.md` § Emotion as Visible Behavior —
> Channels.

### Example

Prior clip ended on a detective standing in a doorway, rain behind her, glancing
over her shoulder. The continuation prompt:

```
Continuing from the prior clip — the detective framed in the doorway, head
turned, rain behind her. [Identity block verbatim: weathered woman, mid-40s,
short dark hair, charcoal trench coat, leather gloves, tired but alert.]
Following her glance back, she steps fully into the corridor, lets the door
swing shut behind her, and begins walking toward camera. Slow dolly-back
matching her pace. Same cool blue-grey palette, same overhead practical light.
Tense, controlled energy carrying over from the prior clip.
```

All five rules present: last-frame anchor (framed in the doorway, head turned,
rain behind her), identity anchor (bracketed block, verbatim), prior clip as
secondary memory ("following her glance back"), immediate continuation (steps
fully into the corridor — the next frame action), no action repeat (the glance
is referenced, not re-performed).

---

## Working Modes vs Prompt Modes — Two Taxonomies

The Seedance 2.0 Prompt Modes section above names five things the
platform exposes: Reference-Based / Continuation / Expand Shot / Edit
Shot / Transformation. These are platform mechanisms — different pathways
through which Seedance accepts a prompt. The Reference Roles and Working
Modes sections below name two adjacent concepts that the platform
vocabulary does not surface:

- **Working modes** — user intent. What you are trying to DO with the
  craft when you sit down to write the prompt.
- **Prompt modes** — platform mechanism. Which of the 5 input pathways
  Seedance accepts the prompt through.
- **Reference roles** — what each reference inside the prompt represents.
  A semantic-role layer, distinct from the input-modality use-case
  patterns catalogued in `../higgsfield-cinema/SKILL.md` § @ Reference
  Patterns for Cinema Studio 3.0 (which lists `@Image1` / `@Video1` /
  `@Audio1` patterns by scenario, not by semantic role).

These three taxonomies are peers, not hierarchical. A single Seedance
shot pulls from all three: a working-mode intent picks a prompt mode;
references inside the prompt play specific roles.

### The "Continuation" Word Collision

"Continuation" names something in both taxonomies:

- **Continuation working mode** = user intent — "I am picking up where
  the previous shot left off."
- **Continuation prompt mode** = platform mechanism — the specific
  Seedance input pathway that extends a prior generation forward in time
  (see the Seedance 2.0 Prompt Modes section above).

A user in Continuation working mode almost always uses Continuation
prompt mode — the intent and the mechanism line up. But Bridging working
mode can also reach for Continuation prompt mode (when the bridge
anchors on the last frame of the upstream shot), and Repair working mode
can reach for Continuation prompt mode (when the repair is a re-shoot
starting from the same last frame as the failed clip). The names
overlap; the meanings don't.

In this skill, section context disambiguates: if the surrounding content
is in the Working Modes section, "Continuation" means the intent; if in
the Seedance 2.0 Prompt Modes section or the Continuation Prompt Formula
section, "Continuation" means the mechanism. If still ambiguous, the
longer forms — "Continuation working mode" and "Continuation prompt
mode" — are always available.

### Working Mode → Prompt Mode Mapping

| Working mode  | Typical prompt mode(s)                | Reference roles in play                |
|---------------|---------------------------------------|----------------------------------------|
| Exploration   | Reference-Based, or pure T2V          | Character (optional)                   |
| Continuation  | Continuation                          | Character + Last-Frame                 |
| Bridging      | Reference-Based or Continuation       | Character + Last-Frame + Environment   |
| Repair        | Edit Shot, or fresh Reference-Based   | Character + (failed-shot reference)    |

Not a strict mapping. One working mode routes through one or more prompt
modes depending on what the shot needs; the table anchors the typical
case without claiming a 1:1 bijection.

---

## Reference Roles

Seedance prompts use references — `@Image`, `@Video`, and `@Audio` — to
lock specific properties across shots. Each reference plays one of four
roles depending on what it locks. This is a semantic-role taxonomy: what
the reference IS FOR in the prompt. It sits alongside (not on top of)
the input-modality use-case patterns in `../higgsfield-cinema/SKILL.md`
§ @ Reference Patterns for Cinema Studio 3.0, which catalogs concrete
prompt patterns by file type.

If a property has to read consistently across multiple shots, assign it
to a reference role. If it only matters for one shot, write it inline.

### Character

Locks main-character identity across shots — face, build, distinguishing
marks. Almost always an image reference; for highest consistency, use
the Soul ID character sheet documented in
`../higgsfield-soul/SKILL.md` § Character Sheet Creation.

Pattern in a Seedance prompt:

```
@Image1 as the main character. [Identity block verbatim.] [Action the
subject performs.] ...
```

### Last-Frame

Anchors the start of a new clip to a specific frame from the previous
one. The role tells the model where to begin rendering from. Used in
Continuation prompt mode and inside Bridging working mode. For the full
five-rule construction pattern, see the Continuation Prompt Formula
section above.

Pattern in a Seedance prompt:

```
Continuing from the prior clip — [short description of what the camera
sees in the final frame of the prior clip]. [New action that follows.]
```

### Environment

Locks the world and setting across shots — architecture, light quality,
ambient particulates, weather state. The role tells the model the
specific space the action takes place in, separate from any character
in that space. Pairs with `../higgsfield-cinema/SKILL.md` § Location
Reference Sheets when the same environment recurs across enough shots
to earn a sheet.

Pattern in a Seedance prompt:

```
@Image1 as the environment. [Subject + action.] [Lighting / atmospheric
cues consistent with the environment reference.]
```

### Prop

Locks specific recurring objects — a hero costume piece, a signature
weapon, a branded product, a vehicle that appears across multiple shots.
The role tells the model that this specific object — not a generic
instance of its category — must read identically across cuts.

Pattern in a Seedance prompt:

```
@Image1 as the prop. [Subject interacts with the prop.] [Camera
behavior.] [How the prop appears in the new shot — same geometry and
material as the reference.]
```

### Per-Image Role Convention

Reference handles (`@Image1`, `@Image2`, `@Video1`, `@Audio1`) are
assigned by upload order — the first image attached becomes
`@Image1`, the second becomes `@Image2`, and so on. Production
practice locks a stable role assignment per slot, kept identical
across every prompt in a shot list, so the team and the model both
know which reference carries which property without re-reading the
prompt body.

| Slot       | Role                          |
|------------|-------------------------------|
| `@Image1`  | Character identity            |
| `@Image2`  | Costume                       |
| `@Image3`  | Environment + lighting        |
| `@Image4`  | Composition                   |
| `@Video1`  | Motion only                   |
| `@Video2`  | Camera movement only          |
| `@Audio1`  | Rhythm + atmosphere           |

The slot order is not model-enforced — it is team-side discipline.
The payoff is reference-stability across long shot lists: once
`@Image1 = character` for the project, that holds for every prompt,
and nobody has to re-check which face the model expects at shot 47.

When a reference conflicts with the prompt text — costume reference
shows red, text says blue — resolve it explicitly in the prompt
body: `@Image2 as costume reference, but recoloured to blue for this
shot`. Don't let an unresolved conflict reach the model.

### Load-Bearing Rule

**References support memory, but text defines action.** The references
in a Seedance prompt carry the persistent properties that read
consistently across shots; the prompt text directs what happens in this
specific generation. References cannot drive new action; text cannot
replace what the references carry. Both layers stay in their lanes.

Sibling formulation of the v3.7.1 camera-side rule ("Prompt wins on
action, reference wins on texture and world feel" — see
`../higgsfield-camera/SKILL.md` § Video Reference — What It Reads, and
What It Can't, § Load-Bearing Rule). Same underlying principle from
different surfaces. The camera-side rule names the WIN order in case of
conflict; the Seedance-side rule names the LANES each side covers.

The same distinction applies one level up — at the prompt-construction
workflow, not just inside the prompt. When a Seedance clip lands and
you want the next prompt to match its look, screenshot the working
frame and upload it **to Claude, not to Seedance**. Claude needs the
visual to write a prompt that matches the look; Seedance receives the
resulting text prompt and renders the next clip without the screenshot
attached. The screenshot is reference (for the prompt-building model);
the text prompt is action (for the generation model).

---

## Frame Coordinate System

**Frame Coordinate System** locks where subjects, props, and
compositional elements sit inside the frame.

### Qualitative anchors

Standard film-language position language, machine-readable because
it is widely-attested in the training data:

- **Horizontal:** `left third`, `center`, `right third`
- **Vertical:** `upper third`, `lower third` (centered vertically is
  the default and rarely needs naming)
- **Depth:** `foreground`, `midground`, `background`

### Percentage notation

Numeric coordinates for cases where the qualitative anchors are
not specific enough:

- **x-position:** `0%` (far left frame edge) to `100%` (far right
  frame edge)
- **y-position:** `0%` (top of frame) to `100%` (bottom of frame)
- **frame occupancy:** the percentage of the frame area the subject
  fills, useful for shot-size pinning (a tight close-up sits near
  `60-80%` occupancy; a wide establishing has the subject below
  `15%`)

Use percentages when qualitative anchors are under-specified —
e.g., two characters in the same half of frame.

### Pair the two notations

Ship the qualitative anchor and the percentage notation **together
in the same prompt**, not as alternatives. The qualitative term
gives the model the film-language hook; the percentage gives it the
precision target. Example:

```
Character A stands in the right third, x-position 70%, y-position
50%, frame occupancy 25%. Character B stands in the left third,
x-position 25%, y-position 55%, frame occupancy 22%.
```

### Not a mathematical guarantee

Frame coordinates are **a strong compositional anchor, not a
geometric guarantee**. The model treats them as directorial
intent — the same way a DP reads "right third" on a storyboard —
not as pixel-exact targets. Use them alongside the rest of the
standard composition vocabulary (`over-the-shoulder`, `eye line`,
`ground contact`, `headroom`, `nose room`, `crossing rule`) rather
than as a substitute for it.

When a coordinate drifts in the output, that is the expected behavior
class — the coordinate set the intent; the model rendered to its
best-fit interpretation. Adjust the prompt by tightening the
qualitative anchor or by adding a contact-point clause (`feet on
the marked floor mark`, `right hand resting on the table edge`)
that physically grounds the position rather than re-specifying the
percentage harder.

---

## Spatial Layout Block

A **Spatial Layout Block** is a named structural unit inside a
Seedance prompt that consolidates the spatial-vocabulary fields
from § Frame Coordinate System into a single block the model can
read as one coherent spatial brief. Where Frame Coordinate System
provides the *vocabulary*, the Spatial Layout Block provides the
*structure* for using it.

Scattered spatial directives force the model to reassemble scene
geometry from fragments — and it often picks the wrong reassembly.

### What goes in the block

A complete Spatial Layout Block names, per subject in frame:

- **Identity** — which character/prop/element this is (matches a
  Reference Role handle when references are present)
- **Screen position** — qualitative anchor + percentage notation
  paired per § Frame Coordinate System above
- **Depth layer** — foreground / midground / background
- **Frame occupancy** — % of frame area the subject fills
- **Body orientation** — direction the subject faces (toward
  camera, away, profile-left, profile-right, three-quarter to
  camera)
- **Contact points** — what physical surface or object the subject
  is grounded against (`feet on wet asphalt`, `back pressed against
  the wall`)

Multi-character blocks add the cross-subject relationships:
relative distance, eyeline direction between subjects, screen-left
vs screen-right consistency, whether subjects cross the central
vertical axis, what occludes what.

### When to use a Spatial Layout Block

Three triggers:

1. **More than one subject in frame.** Two-character work is where
   the model most often swaps screen positions or crosses the
   central axis without instruction. A block prevents that.
2. **A specific compositional intent that needs to read across
   shots.** When the same blocking must hold for several beats — a
   character anchored left, another anchored right — the block
   makes the anchor explicit and re-usable.
3. **A failure-mode-prone shot.** Door-entry shots, hallway-direction
   shots, and any shot where the model has been picking the wrong
   spatial reassembly historically all benefit from a block up
   front rather than inline spatial fragments.

Shots with a single subject in a clear position rarely need a full
block; a single qualitative-plus-percentage anchor inside the
Dynamic Description suffices.

### Block-and-prompt fit

The Spatial Layout Block sits **before** the Dynamic Description in
the output format (see § Output Format for Seedance Prompts below).
It primes the model with full geometry; the Dynamic Description
then describes the action that happens inside that geometry.

The block does not replace the six-slot formula — camera, lens,
lighting, and shot timing stay in their respective slots.

---

## Working Modes

Working modes is a user-intent layer above the platform mechanism. It
names what you are trying to DO when you sit down to write a Seedance
prompt — independent of which prompt mode you eventually route through.
See the disambiguation section above for the relationship between
working modes (intent) and prompt modes (mechanism). The mapping table
there shows the typical routes.

### Exploration

Open-ended discovery. No prior shot to anchor on; no constraint to
match. You're generating to find out what the shot wants to be. Short
prompts work here — the model has space to bring its own interpretation.
Typically routes through Reference-Based prompt mode (with a single
character anchor) or pure text-to-video (no references at all).

### Continuation

Picking up where a previous shot left off. The prior clip is the anchor;
the new clip continues from its final frame. Working mode and prompt
mode line up: Continuation working mode almost always routes through
Continuation prompt mode. See the Continuation Prompt Formula section
above for the five-rule construction.

### Bridging

Connecting two existing shots that don't currently flow. The shots
themselves work; the cut between them feels wrong — spatial geography
is unclear, or the emotional energy mismatches, or the camera character
jumps. Bridging uses references from both ends — the last frame of the
upstream shot and the first frame of the downstream shot — to navigate
the middle. Typically routes through Continuation prompt mode (when the
upstream last-frame is the dominant anchor) or Reference-Based (when
both ends carry equal weight). Common reference role configuration:
Character + Last-Frame + Environment.

### Repair

Fixing a failed shot. Distinct from regenerating with a tweaked prompt —
Repair acknowledges that the failed clip is data: it shows you what the
model interpreted wrong, and that interpretation needs to be addressed
directly. Typically routes through Edit Shot prompt mode (when the
failure is local — a wrong jacket color, a missing prop) or a fresh
Reference-Based generation with corrective prompt text (when the failure
is structural — wrong action beat, drifted identity). Pair with the
Iteration Rule in `../higgsfield-prompt/SKILL.md` § The Iteration Rule
when iterating on the corrective prompt.

### Decision Tree — Picking a Working Mode

The mode you reach for is downstream of what you're noticing in your
work. Diagnose by symptom, then pick the mode that fits:

| What you're seeing | Working mode | Why |
|---|---|---|
| Blank page, no anchors yet | Exploration | No prior shot to continue or bridge from; freeform discovery first. |
| Strong shot that needs a follow | Continuation | The shot earned a sequel; pick up where it left off. |
| Two strong shots that don't connect | Bridging | The shots work; the seam between them doesn't. |
| Strong shot but the feeling is weak | Continuation (with role swap) | Re-shoot the same beat with a different reference role carrying the weight — e.g. close-up where the original was wide. |
| Spatial logic feels off mid-sequence | Bridging (with geography clarification) | The sequence needs a beat that re-establishes who is where. |
| Failed shot you keep generating around | Repair | Stop iterating on the prompt. Target the failure directly. |

The decision tree is symptom-first, not mode-first. The mode is the
treatment; the symptom in your work is the diagnostic. If you find
yourself reaching for a mode without naming what symptom drove the
choice, that's a signal to step back.

---

## Two-Layer Prompt Authoring

A skeleton prompt is not meant to be copied blindly into Seedance and
expected to work on its own. A skeleton is a structure — the logic of
the prompt, not the finished prompt. That matters most for the
Bridging, Continuation, and Repair working modes (see § Working Modes
above), because those three tasks depend heavily on context: what
happened before, what must follow, and what exactly the shot is
supposed to solve.

Each practical skeleton in this workflow has two layers, each with a
different audience and a different job.

### The Two-Layer Distinction

- **Layer 1 — task definition / briefing block.** Written for yourself
  or pasted into a ChatGPT-style assistant before the production
  prompt is drafted. Explains the actual problem in plain prose: what
  scene already exists, what the next scene is, what is missing
  between them, what must remain the same, and what the bridge or
  repair must achieve. Layer 1 is the planning step — it forces the
  prompt author to define the problem cleanly before writing the
  model-facing prompt.

- **Layer 2 — production prompt for Seedance.** Shorter, cleaner, more
  execution-oriented. Translates the Layer 1 decision into a
  model-friendly structure: reference roles declared up front,
  preservation clauses, the one action, anti-repeat language, camera
  cue, audio cue. Layer 2 is what gets pasted into the generation
  field.

The distinction makes the workflow practical. Without Layer 1, bridges
fail because the prompt author hasn't decided what the bridge is
supposed to solve; continuations restage instead of continuing because
the prompt author hasn't named what to preserve; repairs over-shoot
because the prompt author hasn't isolated what to change. The two
layers exist to prevent those three failure modes by separating the
planning step from the execution step.

### Bridge Skeleton

The Bridging working mode (see § Working Modes / Bridging above) is
the problem-solving mode — the bridge is not generic cinematic filler.
Use this skeleton when two scene blocks both work but the connection
between them does not.

**Layer 1 — bridge briefing block.** Named fields:

```
Scene A ends with:
[final visible state of upstream scene]

Scene B begins with:
[opening visible state of downstream scene]

The missing thing between them is:
[reaction / movement into a new space / prop action /
emotional beat / spatial clarification]

The bridge must preserve:
[same character, same outfit, same location logic,
same emotional residue, same prop continuity]

The bridge must not do:
[no new subplot, no repeat of previous action,
no extra threat, no random spectacle]

The purpose of the bridge is:
[explain the transition / make the cut readable /
carry emotion / reposition the viewer in space]
```

**Layer 2 — bridge production prompt skeleton.** Reference roles
declared up front, then the bridging clauses:

```
[Reference roles]
@Image1 = character identity reference
@Image2 = continuity start or location anchor (omit if neither is needed)

This is a bridging shot between the previous beat and the next scene.
Its purpose is continuity, not spectacle.

Keep the same character, same outfit, same space logic, same emotional
carryover, and same prop continuity.
Show one readable action that explains the transition.
Do not repeat the previous action beat.
Do not introduce a new threat or subplot.

Scene: [where the character is in this transition moment]
Bridge action: [one small but meaningful movement or reaction]
Camera: [restrained and readable]
Audio: [live sound only if needed]
```

A good bridge often looks "small" compared to an action scene but
does major structural work. If the Layer 2 prompt produces something
that feels too eventful, the Layer 1 briefing's "must not do" clause
was probably too thin — revise the briefing, then re-derive the
production prompt.

### Continuation Skeleton

The Continuation working mode (see § Working Modes / Continuation
above) solves a temporal problem, not a connection problem: the next
clip must begin directly after the previous clip, not as a new
restaging. This skeleton operationalizes the five rules in the
Continuation Prompt Formula section above — specifically rule #5,
"No action repeat."

**Layer 1 — continuation briefing block.** Named fields:

```
The previous clip ends on:
[end pose / camera direction / emotional state /
visible props]

The next clip must begin immediately after that.

Keep:
[identity / body direction / location / emotional
carryover / props]

Change:
[the new beat that begins now]

Do not repeat:
[the previous action phase]
```

**Layer 2 — continuation production prompt skeleton.** Three reference
roles is the typical configuration:

```
[Reference roles]
@Image1 = exact last-frame continuity anchor
@Image2 = character identity reference
@Image3 = optional environment or prop continuity reference

Use @Image1 as the exact continuity start anchor.
Keep the same character, same lighting logic, same spatial continuity,
same emotional carryover.
Start immediately after the final frame.
Do not repeat the previous beat.

Scene: [what remains unchanged]
New action: [what starts now]
Camera: [how the viewer reads the continuation]
Audio: [live sound only if needed]
```

**If the result keeps replaying the previous beat,** the correction is
not "make the prompt longer." The correction is to strengthen the
temporal and anti-repeat language. Useful phrase variants:

- start immediately after the final frame
- do not repeat the previous fight
- do not restage the earlier beat
- continue forward into the new action
- preserve the same fatigue state and emotional carryover

These are interchangeable — pick the variant whose verbs match the
prior clip's content. A continuation following a fight scene wants
"do not repeat the previous fight"; a continuation following a quiet
moment wants "do not restage the earlier beat."

### Repair Skeleton

The Repair working mode (see § Working Modes / Repair above) does not
behave like "generate the scene again, but better." That breaks
continuity and changes too much. The real question is always: what
exactly am I trying to preserve, and what exactly am I trying to
change? A usable repair prompt has two parts that map directly onto
that question — a preservation block and a modification block.

**Layer 1 — repair briefing block.** Named fields:

```
Current clip / image state:
[what already works and must remain stable]

The exact problem:
[what is wrong]

Preserve:
[identity / framing / pacing / space / continuity /
lighting / emotion / prop logic]

Change only:
[one or two specific elements]

Do not damage:
[what tends to drift if the edit is too broad]
```

**Layer 2 — repair production prompt skeleton.** Tight, surgical, no
descriptive ornament:

```
Keep the original framing, pacing, environment, and character
identity.
Preserve the same outfit, same lighting logic, same scene layout,
same emotional state.
Change only [the exact element that needs fixing].
Do not alter the rest of the shot.
```

The "do not damage" field in Layer 1 is the field most often skipped
and most often the source of repair failures. Name the properties
that typically drift when an edit goes too broad — those are the
properties the model needs explicit protection on, even if they
aren't the properties the edit is targeting.

---

## Keyframe Workflow

The most useful official direction on fine-grained Seedance editing
comes from BytePlus VideoPilot — Seedance's official editing-style
interface from ByteDance / BytePlus. VideoPilot frames fine-grained
video editing not as one vague "fix this clip" prompt but as a
**reference + keyframe + local modification** workflow. Three named
ingredients, each with its own job.

This section names what VideoPilot's interface exposes (Capability
Surface), how to translate those primitives into prompt-only Seedance
work when the dedicated UI isn't in play (Translating to Seedance
Prompts), and the underlying mindset that makes the whole approach
work (The Editor-not-Regenerator Mindset).

> **Sourcing:** The keyframe-editing capability surface below is from
> the BytePlus VideoPilot fine-tuning documentation
> (`docs.byteplus.com`) and ByteDance's official Seedance launch
> materials (`seed.bytedance.com`). Same official source set as the
> Rule of 12 citation at
> `../higgsfield-models/MODELS-DEEP-REFERENCE.md:274`.

### Capability Surface

VideoPilot exposes five named editing primitives. These are what the
official UI lets you do; the prompt-side translation in the next
section is the closest equivalent when working through prompts alone.

- **Continuous keyframe segmentation.** VideoPilot parses a reference
  video into continuous keyframe segments. The segmentation is
  done by the system, not assembled by hand. The unit of edit is the
  keyframe, not the whole clip.

- **Fine-grained keyframe edits.** Edits target a single keyframe at
  a time. Surgical at the temporal axis — change one frame's content
  without rewriting any other frame's instruction.

- **Custom keyframes.** The editor can add keyframes the system
  didn't auto-detect. Useful when an important beat falls between
  the auto-segmented keyframes.

- **Partial redraw of selected regions.** Spatial-local edits within
  a keyframe — mask the region, redraw only what is inside the mask.
  Surgical at the spatial axis (vs. the temporal-axis surgery of
  fine-grained keyframe edits).

- **Keyframe description rewrite.** Rewriting the description of one
  keyframe causes the system to regenerate that frame AND its
  transition logic to neighboring keyframes accordingly. This is the
  closest official primitive to Seedance's Edit Shot prompt mode (see
  § Seedance 2.0 Prompt Modes / Edit Shot above).

### Translating to Seedance Prompts

When working through prompts and references rather than the dedicated
VideoPilot keyframe UI, the closest practical equivalent is six
operational rules. None of them guarantee perfect surgical editing
in every interface — they translate the official editing workflow
into prompt-based use.

1. **Use a screenshot or final frame as your stability anchor.**
2. **Keep the identity reference separate from the continuity anchor.**
3. **State exactly what must remain unchanged.**
4. **State exactly what is changing.**
5. **Forbid repetition of the previous beat if this is a continuation.**
6. **If the edit is local, describe only the local change and
   explicitly protect the rest.**

These map onto existing repo surfaces: rules 3, 4, and 6 onto the
Repair Skeleton's preserve / change blocks (see § Two-Layer Prompt
Authoring / Repair Skeleton above); rules 1 and 2 onto the Reference
Roles taxonomy (see § Reference Roles / Last-Frame and § Reference
Roles / Character above); rule 5 onto the Continuation Skeleton's
anti-repeat phrase library (see § Two-Layer Prompt Authoring /
Continuation Skeleton above).

### The Editor-not-Regenerator Mindset

The conceptual root of the whole keyframe workflow surface: if the
goal is surgical edits, think like an editor, not a full
regenerator. Freeze the parts that must remain stable. Isolate the
parts that must change. Then make the instruction local and explicit.

This is also the conceptual root of the Repair Skeleton: the
preserve / change split is the prompt-side enactment of the
editor-not-regenerator stance, the same discipline VideoPilot's UI
primitives express at the interface level.

---

## Pre-flight Linter

Before the user generates, run the prompt through the preflight linter:

```
python3 seedance_lint.py "<prompt text>"
```

The linter is at the project root (`seedance_lint.py`). It flags:

- **Real names** of public figures / celebrities / politicians
- **Brand, IP, franchise names** (Nike, Marvel, Spider-Man, Pokémon, etc.)
- **Raw violence verbs** (fight, attack, kill, shoot, blood, gore, stab)
- **Age markers** (child, kid, young, teen, boy, girl — Seedance is age-blind)
- **Note-to-friend voice** (no Style/Mood, no Camera, no Lighting sections)
- **Overlength** (>180 words is risk territory; >220 words often hard-fails
  on the text encoder, not the filter)
- **Conflicting instructions** (moving + frozen, bright + dark, etc.)

Output is `PASS`, `WARN`, or `FAIL` with the specific fix for each rule hit.
Treat `FAIL` as "do not hit generate." Treat `WARN` as "likely to pass, but
here is what to harden."

---

## The Rewrite Playbook

When the linter fires, apply the substitutions below. These are drawn from
`../../db/filter-memory.json` — every pattern here has been confirmed
to work on past flagged prompts.

### Real names → archetype description

❌ "Keanu Reeves walking into a boardroom"
✅ "A lean man in his late 50s, dark shoulder-length hair, stubble, intense
  calm expression, in a dark suit, walking into a modern glass boardroom"

### Brand / IP → visual attributes only

❌ "Spider-Man swinging through New York"
✅ "A figure in a red and blue form-fitting suit, masked, swinging between
  skyscrapers on a tensile white line"

❌ "Nike shoes on a running track"
✅ "White athletic shoes with a dark swoosh-free silhouette on a red rubber
  running track"

### Violence → aftermath / tension / physics

❌ "Two people fighting in an alley"
✅ "Two figures locked in a tense physical confrontation, rain-slick alley,
  dramatic low-key lighting, camera shuddering on each impact"

❌ "An explosion destroys the car"
✅ "A burst of orange light and smoke billowing out from the car, metal
  buckling outward, glass fragments catching the light"

❌ "Blood drips from his hands"
✅ "His hands tremble at his sides, something dark staining his cuffs"

### Weapon → prop + purpose

❌ "A man holds a gun to another man's head"
✅ "A standoff in a concrete stairwell — one figure's arm extended, the other
  perfectly still, both silhouettes hard-edged against a single overhead
  fluorescent"

### Horror / dark → atmosphere, not acts

❌ "A monster tears a victim apart"
✅ "The aftermath of something wrong — an empty room, overturned furniture,
  a single smear trailing toward the door, ambient dread, flickering practical
  lamp"

---

## Voice Rewrite — the "Filmmaker not Friend" Pass

Even with every risk token removed, prompts still get flagged if the voice is
wrong. Do this pass on every Seedance prompt:

1. **Add a Style & Mood clause up front.** Palette, lens, lighting, atmosphere.
   Never skip this. It tells the filter "this is a shot."
2. **Name the camera move.** "Slow dolly-in," "low-angle tracking," "static
   medium." Not "the camera moves forward."
3. **Describe physics, not emotion.** "Jaw clenches, nostrils flare" not
   "looks angry." The filter reads physics as cinematic; emotion language as
   ambiguous intent.
4. **Describe force and direction, not destruction sequence.** "Driven into
   the car, metal buckling" not "thrown into side door, glass shatters, uses
   rebound to sweep leg."
5. **Present tense, active voice.** "She turns" not "she is turning."
6. **Cut the antislop words.** Breathtaking, stunning, epic, masterfully,
   cinematic masterpiece — these signal marketing copy, not a shot description,
   and correlate with flags.

> For the eight named substrate channels that "describe physics, not
> emotion" decomposes into, see `../../vocab.md` § Emotion as Visible
> Behavior — Channels.

---

## Output Format for Seedance Prompts

When generating a Seedance prompt for the user, use this structure. It
mirrors what Seedance's filter reads most cleanly:

```
**Model:** Seedance 2.0
**Aspect ratio:** 16:9   **Duration:** 10s

**Style & Mood:** [palette, lens, lighting, atmosphere — 1 sentence]

**Dynamic Description:** [camera move + subject + action, present tense,
shot-by-shot if multi-cut. This is the main block.]

**Static Description:** [location, props, ambient details — 1-2 sentences]

**Camera:** [exact movement name]
```

For the full bilingual EN+ZH director output format (used in Seedance's
web UI), see the extended reference at `../../docs/Seedance 2 Skill.md`.

### Runtime arithmetic for multi-shot prompts

Runtime appears in three places in a delivered Seedance prompt —
the title line, the meta header (`**Duration:** Xs`), and any
per-shot timing labels in the Dynamic Description. All three must
agree.

For multi-shot prompts, label each shot inline with its time range
(e.g. `Shot 1 (0-3s): ... hard cut to Shot 2 (3-8s): ... hard cut
to Shot 3 (8-15s): ...`). The per-shot labels must *sum* to the
total duration stated in the title and meta header; a drift between
the two surfaces is the most common source of "my multi-shot prompt
rendered as a single shot" failures.

Always ask the user for runtime — never default. A 5s, 10s, or 15s
assumption silently degrades adherence on prompts that needed a
different cap.

### Shot density for multi-scene prompts

When grouping multiple shot rows into a single Seedance prompt
(rather than splitting into separate prompts), use this starting
heuristic: roughly one prompt per 4-5 shot rows. The heuristic is
project-derived empirical observation, not platform-enforced, and
varies wildly by scene type.

Group shot rows into one prompt when ALL of these hold:

- Same character set in frame
- Same location or contiguous subset of a location
- Continuous emotional / temporal unit (no time skip, no major mood
  pivot)
- Combined runtime fits within the 15s Seedance cap
- The grouped prompt text stays within practical generation limits
  (~2500 characters)

Split into separate prompts when any of these fire: hard cut
between locations (e.g. apartment → flashback), major character
entrance or exit changes the handle list, or the combined runtime
exceeds 15s.

The heuristic is a starting state, not a target. Adjust per project
as you learn how Seedance handles your particular scene-type
density — dense action sequences may want 1 prompt per 2-3 shot
rows; quiet emotional scenes may collapse to 1 prompt per 8+ rows.

### Single-vs-multi-shot decision

Default is single-shot. Reach for multi-shot when the content is
action, dynamic dialogue, or anywhere a cut is itself doing work a
single shot cannot deliver. Everything else holds tighter as a single
continuous shot.

For single-shot continuous motion, per-second beats give fine-grained
control without provoking cuts — `[0-3s] subject enters frame,
[3-7s] camera pushes in`. The bracket-notation reference lives in
`../../vocab.md` § Editing Syntax (shipping in v3.7.7 sub-phase 2f).

For multi-shot, use the Runtime arithmetic above — each cut labeled
with its time range, sum equals total duration. Action scenes earn an
extra layer: per cut, name the participants, location, implements,
and beat-by-beat choreography.

Anti-pattern: per-3-second time labels written inside what was meant
as a single continuous shot. Seedance reads any per-segment timing
block as cut instructions and inserts cuts. Pick a side — if you
want continuity, drop the time markers; if you want cuts, label them
with `Shot 1 / Shot 2 / Shot 3` and the multi-shot arithmetic above.

---

## Post-Clip Decisions

When a generated clip raises questions around itself, testing
becomes narrative work — not "is it good?" but "what does it do?"
and "what comes after?" The diagnostic below asks four scene-function
questions; the decision tree maps the answers to next-shot types.

### The Four Questions

After any strong clip, ask these four in order. They surface what
the clip is doing in the episode and what should come next.

1. What function does this scene have?
2. What is missing for it to feel connected?
3. What shot would make the connection readable?
4. Is the next step continuation, bridge, contrast, or reset?

These questions are scoped to the next move, not to "solving the
whole episode." The narrower scope is what keeps them practical.

### Next-Shot Decision Tree

The right question is not "what is the coolest next shot?" but "what
problem does the episode have right now?" Map the problem to a shot
type:

- **Strong but isolated** → continuation or before/after
- **Two scenes do not connect** → bridge
- **Spatial logic unclear** → geography clarification
- **Structure works but feeling weak** → close-up or reaction insert
- **Something broken** → targeted repair

The next shot is chosen by function, not by excitement.

> Note: "continuation," "bridge," and "targeted repair" here name
> next-shot types decided post-generation. "Continuation," "Bridging,"
> and "Repair" in § Working Modes above name per-clip intent during
> composition — different lifecycle phase, different decision.

---

## When the User Is Already in a Failure Loop

This section handles **filter rejections** — prompts the Seedance
filter blocks before generation. For **render failures** (FPS drift,
NSFW false-positive, keyframe-invention, physics-state drift, spatial-
awareness failures, multi-motion overload), see `FAILURE-MODES.md` in
this directory — sibling catalog with symptom + mechanism + counter
per named failure.

If the user tells you Seedance has flagged them multiple times in a row:

1. **Ask for the exact prompt text that got flagged.** Don't guess.
2. **Run the preflight linter** on that exact text.
3. **Apply the rewrite playbook** for every rule the linter hit.
4. **Do a voice pass** (add Style & Mood, name the camera, present-tense physics).
5. **Log the fix** to the filter-memory database at the project root so future
   sessions benefit — use `higgsfield_memory.py` (at the project root) to append
   an entry describing the blocked prompt, the substitution, and whether it worked.

Do not let the user regenerate the same prompt with one word changed. That
is the loop that wastes hours.

---

## Multi-Language Prompt Workarounds

Seedance prompts default to English. This section documents historical
language-level workarounds for specific Seedance platform states.

### Chinese (as of 2026-05-17)

At Seedance 2.0's launch the model performed better against Chinese
prompts and enforced a hard 3,000-character cap per prompt. English
runs roughly 5-10 characters per word; Chinese runs 1-2. Production
teams used Chinese prompts to compress ~5× more directive content
into the same character budget — the decisive workaround on long
multi-shot prompts that otherwise hit the cap.

The workaround was a launch-window optimization, not a permanent
convention. If a long Seedance prompt keeps hitting the cap and
English compression has been exhausted, the Chinese-density path has
shipped before — verify the cap state in the current Seedance UI
before reaching for it.

---

## Related Skills

- `higgsfield-prompt` — MCSLA formula, archetype router, general prompt structure;
  the Iteration Rule and 6-Pass Diagnostic Sequence for when generations are
  off-target and you can't name why
- `higgsfield-troubleshoot` — diagnosis for non-filter failures (render quality, etc.)
- `higgsfield-recall` — pre-generation memory check against past failures
- `../shared/negative-constraints.md` — full negative-constraint reference,
  including the Content Filter / Safety section
- `../../docs/Seedance 2 Skill.md` — extended bilingual director reference
  (archetypes, cut rules, camera language appendix)
