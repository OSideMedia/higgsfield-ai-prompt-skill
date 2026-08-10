---
name: higgsfield-seedance
description: >
  Failure-mode reference for Seedance 2.0 / Seedance Pro. Catalog of
  named output failures (FPS drift, NSFW false-positive, keyframe-
  invention, physics-state drift, action-reversal fill, filler-babble on
  short dialogue lines, truncated action, mimed manipulation, orphan
  limbs in a group shot, multi-motion overload, spatial-awareness failures)
  with symptom + mechanism + counter for each. Consulted when a Seedance
  generation lands in a recognizable failure pattern.
user-invocable: false
metadata:
  tags: [higgsfield, seedance, seedance-2.0, seedance-pro, failure-modes, recovery, prompt]
  version: 1.3.0
  updated: 2026-08-09
  parent: higgsfield
---

# Seedance 2.0 — Failure Modes Reference

Named catalog of Seedance output failures, what causes each, and the
prompt-side fix. Consulted when a generation lands in a recognizable
pattern rather than a random miss.

---

## How to use this reference

Each entry below uses the same four fields:

- **Symptom** — what the user sees in the output.
- **Mechanism** — why Seedance produces that output.
- **Counter** — the prompt-side fix.
- **Worked example** — concrete before/after when the fix benefits
  from being shown rather than described.

When a generation fails, scan the section headers for the matching
symptom first. If nothing matches, the failure may belong in
`SKILL.md` § When the User Is Already in a Failure Loop instead —
that section covers filter rejections rather than render failures.

---

## FPS drift and frame-by-frame de-duplication

**Symptom.** The output plays back choppy. Inspecting it frame-by-frame
in an editor shows duplicate consecutive frames where motion should be
continuous. Requested 24 fps; actual cadence runs closer to 12-18 fps
with the dupes counted.

**Mechanism.** Seedance does not always honor a requested frame rate.
Under load or on dense action prompts it drops the effective frame
rate and pads the timeline with repeated frames to fit the requested
duration. The duplicates are the give-away.

**Counter.** Two layers, applied in order:

1. State the frame rate explicitly in the prompt body, not only in
   the meta header — `The video runs at 24 fps. No frame is
   repeated.` Anchoring the rate in the dynamic description raises
   the rate of correct output without making it deterministic.
2. When the output still drifts and the clip is needed as B-roll
   (not a hero shot), de-duplicate frame-by-frame in the editor:
   delete the repeated frames, re-interpolate, and use the result
   as connective footage. Save hero shots for re-generation.

The frame-by-frame de-dup is a fallback, not a fix. Hero shots that
land at 12 fps stay broken; re-generate them.

---

## Frame-level review is mandatory

**Symptom.** A Seedance clip looks fine at full speed but a single
bad frame inside it ruins the cut in playback — a flickered hand, a
warped face, a misplaced object that only the eye-on-pause catches.

**Mechanism.** Seedance output is generated, not captured. Unlike film
footage where lens optics constrain what each frame can contain, an
AI clip's per-frame state is independent and can drift in a single
frame without warning. A 24-frame clip is 24 independent generations
the model strung together.

**Counter.** Treat every Seedance clip as untrusted until reviewed
frame-by-frame in the editor. Step through with the J/K/L scrub or
arrow-key step; one bad frame is enough to reject the take. Plan the
frame-review time into the iteration budget — a 10-second clip is
roughly 30-60 seconds of careful scrub time per pass.

---

## Failed-generation salvage

**Symptom.** A generation comes back rejected at the take level — the
camera move is wrong, the action collapses, the composition broke
mid-shot. First instinct is to discard and regenerate.

**Mechanism.** A "failed" Seedance generation is rarely failed across
all 10 seconds of runtime. The model frequently produces 1-3 seconds
of usable footage inside an otherwise-discarded clip — a clean
opening before the camera drift, a clean middle before the action
collapse, a usable insert near the end.

**Counter.** Before discarding, scrub the rejected take and mark the
usable segment with in/out points. Cut it out and bank it. The
2-second insert that survives a "failed" generation often slots into
a different scene as connective footage, or holds for a reaction
beat in the original shot.

Failed takes mined for usable seconds compound across a project —
the 90-min Cannes feature shipped meaningful runtime from salvage
cuts alone.

---

## NSFW false-positive (provider-side)

**Symptom.** A prompt with no NSFW content comes back rejected as
NSFW. The IP-check section passes; only the NSFW classifier fires.

**Mechanism.** Seedance's NSFW classifier runs on the prompt text and
on intermediate generation tokens. Body-anatomy specificity, certain
costume vocabulary, and some sensual-but-clean phrasings can trip
the classifier even on benign content. The classifier is probabilistic
and tuned conservative; false positives are part of its operating
profile.

**Counter.** Rephrase the prompt:

1. Remove or generalize body-anatomy specifics (`her bare shoulders`
   → `her shoulders`; `tight-fitting dress` → `fitted dress`).
2. Replace sensual-register adjectives with neutral equivalents
   (`sultry` → `composed`; `seductive` → `direct`).
3. Move the rephrased prompt through the preflight linter in
   `SKILL.md` § Pre-flight Linter to catch other risk tokens.

Do not regenerate the same prompt unchanged — same text trips the
same classifier. See `SKILL.md` § When the User Is Already in a
Failure Loop for the anti-loop discipline.

---

## Keyframe-consistency forces invention

**Symptom.** The prompt requires an element to appear or move (`the
character pulls a Polaroid off the fridge`) but the source keyframe
does not contain that element. Seedance produces the action anyway,
inventing the element's placement — often in a spot that contradicts
the rest of the scene geometry.

**Mechanism.** Seedance treats the source keyframe as a strong anchor
for what the world contains. When the prompt requires an element that
the keyframe does not show, the model has to manufacture both the
element AND its placement, and the placement often drifts to wherever
the model can fit it without overwriting other reference content.

**Counter.** State the absence explicitly so the model knows it is
being asked to add, not to match: `The Polaroid is not visible on the
fridge in image 5; it appears in this shot when the character lifts
their hand from below the frame.` The explicit-negative-reference
clause tells the model that the source keyframe and the target output
intentionally disagree on this element, which routes the model to
invent placement deliberately rather than as a fallback.

---

## Physics-state-anchor

**Symptom.** A physical object behaves wrong when an adjacent object
moves — the magnet flies away with the Polaroid when the character
pulls the Polaroid off the fridge; the cup tips when the character
lifts the saucer; the hat lifts when the character turns their head.
Adjacent-object physics violations.

**Mechanism.** Seedance has no enforced physics simulation. When two
objects are visually adjacent in the source frame, the model can
interpret a movement on one as a movement on both, especially under
fast camera work or dense action prompts.

**Counter.** State the invariant explicitly. Add a clause to the
prompt naming what stays put: `The magnet stays attached to the
fridge surface throughout. Only the Polaroid moves.` The physics
anchor reads as a soft constraint, not a hard guarantee — but
adjacent-object drift drops noticeably when the invariant is named.

---

## Action-reversal fill

**Symptom.** The prompted action completes in the first seconds and the
rest of the clip plays it back in reverse — the character walks forward
then steps back to the start mark, leans in then pulls away, reaches out
then withdraws the hand. Reads as an unmotivated there-and-back. The
camera version: a move with no stated destination drifts back the way it
came once it arrives.

**Mechanism.** A short action finishes before the clip does, and the
model still has seconds of timeline to fill. With no further instruction
in the prompt, the cheapest continuation consistent with the scene is to
run the motion it already rendered in reverse. `[EMPIRICAL — dramaclaw
production corpus, Seedance]`; model-agnostic i2v behavior, not a
Seedance spec.

**Counter.** Give the motion enough material to spend the whole clip in
one direction: chain 2–3 connected actions along the same vector (walks
to the window, pulls the curtain aside, leans into the glass). If the
story calls for a there-and-back, that is two shots, not one prompt. For
camera moves, name the endpoint — state what the frame shows when the
move finishes. Full treatment: `SKILL.md` § Prompt-Craft Laws →
Motion-prompt laws.

---

## Filler-babble on a short dialogue line

**Symptom.** A short scripted line in a solo shot comes back wrapped in
invented mumble — garbled pseudo-speech before or after the words, or
the scripted line delivered twice. Graded from transcripts, so this is
an AUDIO symptom; whether the mouth also keeps moving was not graded by
the rig below and is not claimed here.

**Mechanism.** The audio branch fills dead air, the same way § Action-
reversal fill spends leftover motion time. A line that ends well before
the clip does leaves a silent window, and the cheapest continuation
consistent with the shot is more speech-shaped sound in the same voice.
`[MEASURED — sync-budget ladder, 2026-08-09, EN × 4s × 480p × Seedance
2.0]`: every take at ≤6 words carried it; 8- and 12-word lines came back
4/4 clean. The risk direction is the **short** line, not the long one —
no truncation was observed up to 12 words (≈3 words per second).

**Counter.** Give the dead air a job instead of leaving the choice to
the model, and state the mouth state of every face that is visible:

1. **Fill the window.** Extend the line to roughly 8+ words in a
   4-second shot, or cut the shot down to the line.
2. **Script the silence.** If the line has to stay short, write what
   occupies the rest of the window — a named pause beat, an ambient or
   SFX event, action prose covering the gap before and after the line.
3. **One speaker, one line, once.** The speaking character says the
   line and nothing else; `HELL-GRIND.md` § Dialogue construction
   carries the full audio-block phrasing. A beat that carries a thought
   rather than a line is typed `INNER (unspoken)` there, which keeps it
   out of the mouth entirely.
4. **Every other visible face gets a positive at-rest mouth fact.** An
   unmarked mouth in frame is a mouth the model may decide is talking.
   State the rest state as something that *is* true — "lips at rest",
   "jaw closed, breath lifting the chest", "eyes on the speaker, mouth
   still" — never as a negation (`SKILL.md` § Prompt-Craft Laws → No
   negative prompts in the prompt body). Note that "listens without
   speaking" reads positive but carries *without*, so it trips the same
   law; prefer the forms above.

**Worked example.** A 4-second two-shot carrying one scripted line:

❌ `AUDIO — MIRA (dry, clipped): "It's gone."` Most of the window is
left unwritten, and the second face in frame has no mouth state at all.

✅ `AUDIO — Diegetic only: rain on the skylight, one door latch at 3.4s.
MIRA (dry, clipped) says her line once and nothing else: "It's gone, and
it took the ledger with it." DEV keeps his eyes on her — lips at rest,
jaw closed, his breath lifting his chest.`

The line rewrite is the measured half: it fills the window. The at-rest
mouth fact on the second character is the **unmeasured** half — it is
the prompt-side handling for when a second face cannot be kept out of
the shot, and it is not yet live-fired here. A one-shot 480p A/B (two
characters, one short line, mouth fact present vs. absent) would settle
it.

---

## Truncated action — the cut lands before the result

**Symptom.** The shot list reads as full coverage and the film shows
nothing landing. The lid is still closing when the cut comes, the hand
is still reaching, the door is half shut. Every action in the sequence
is an attempt; none of them is a result. Fast-cut sequences carry this
most, and it survives review because each individual shot looks correct.

**Mechanism.** Shots get priced by what they *contain*, not by what has
to *finish* inside them, so the model spends the runtime on the approach
and the completion falls past the boundary. Nothing in the prompt says
which state must be visible before the shot may end, so any frame is as
good a stopping point as any other. `[HOUSE — technique re-derived from
the nutllwhy/seedance-tvc-director evaluation, MIT, 2026-08-09.
UNPROVEN HERE: not A/B'd on our material.]`

**Counter.** Name the completion state as a visible fact and let it
settle before anything else happens — *the lid seats flush and stays
there*, *the glass comes to rest on the wood*, *her hand closes fully
around the handle*. Where the pace genuinely needs the cut sooner, open
the **next** shot on the result already true (the laptop shut, the room
already dark) so the sequence inherits what the cut skipped. The source
holds the completion for roughly 0.15–0.35s before cutting; treat that
as the direction to lean, not as a measured figure.

The audio twin of this law is already in this repo — a spoken line pinned
early so the cut inherits a tail (§ Filler-babble, and OSIDE's
`dialogue-no-handle`). This is the same law for picture.

---

## Mimed manipulation — hands move, the object does not

**Symptom.** A character opens, tears, pours, presses or spreads
something and the object never changes: fingers work convincingly over a
pack that stays sealed, a cap that never breaks its seal, a surface that
never creases. Reads as an actor rehearsing without a prop.

**Mechanism.** The manipulation was written as its verb — *tears it open
cleanly*, *twists the cap off* — which gives the model a gesture and no
mechanism. With no structure, no anchor and no material response stated,
the gesture is the only part it can render. `[HOUSE — re-derived from the
same evaluation. UNPROVEN HERE.]`

**Counter.** Write the causal chain, in order:

1. **Initial structure** — what the object is before contact (sealed
   along the top edge, capped, full).
2. **Anchor** — what holds it steady and how (the other hand gripping
   the body of the pack, the base flat on the counter).
3. **Force** — where the force is applied and which way it travels
   (thumb and forefinger at the notch, pulling across).
4. **Material feedback** — what the material visibly does (the film
   parts from the notch, the pack creases where it is held).
5. **Finished state** — what is true when it is done (a continuous
   opening with the contents visible, the torn strip clear of the pack).

Two routing rules travel with it. If the manipulation only *gets us to*
the next state rather than being the point of the shot, use two states
and a sound instead — sealed pack, a tear heard off screen, hands
already inside it; it is cheaper and it cannot fail this way. And never
invent a structure the reference cannot show: if the notch, the seal or
the catch is not visible in the material you hold, open it off screen,
cut around it, or shoot it for real.

Do not stack a legible brand face, a two-handed manipulation and a
strong effect in one shot — the manipulation shot proves the mechanism,
a separate shot proves the label.

---

## Orphan limbs in a group shot

**Symptom.** Three or more characters, and a hand enters the action with
no body behind it: a sleeve crossing another character's chest, a
forearm from off screen with no shoulder, an extra hand nobody owns.
Adjacent to it: the headcount changes across a cut, or two neighbours
trade places between the wide and the close-up.

**Mechanism.** With no order lock, the model re-derives the group on
every cut rather than carrying one forward. Reaching is the moment it
shows, because a hand is the smallest thing in frame that has to belong
to somebody. `[HOUSE — re-derived from the same evaluation. UNPROVEN
HERE.]`

**Counter.** Lock the group before the action: the exact headcount, the
left-to-right screen order, who sits next to whom — held in every
framing. Then give each hand entering the action an owner: whose hand,
which hand, what sleeve, which side of frame it enters from, where it
returns to. Cap hand action at two characters per shot; the rest watch.

When the shot wants a detail, two faces and a group recap at once, that
is three shots — a fixed insert on the object with at most two
attributable hands, a two-shot on the neighbours who react, then a
static group frame with hands already clear of the object. One
continuous push-out cannot deliver all three.

---

## Multi-motion camera overload

**Symptom.** A camera move with multiple stacked motions
(handheld + rise + push-in + rack focus) produces an unreadable
result. The viewer cannot track any one motion because all three are
happening simultaneously; the shot reads as instability, not as
choreography.

**Mechanism.** Seedance can render any individual camera motion well;
combining motions stresses the model's ability to keep the subject
inside the frame while all axes are changing at once. The audience-
side problem is independent: human attention does not parse three
simultaneous camera motions even when they render cleanly.

**Counter.** One dominant motion per shot. If two motions are
required, split the shot into two cuts and apply each motion to one
cut. If the script demands a compound move (`rise into a push-in`),
state the motions in clear sequence with timing — `Camera rises from
0-3s, holds, then pushes in from 4-8s` — so the model can render
them as discrete phases rather than simultaneous axes.

See `SKILL.md` § Single-vs-multi-shot decision for the multi-shot
split mechanics.

---

## Spatial-awareness failures

**Symptom.** Door-entry shots have higher failure rate than static
shots. Hallway-direction shots end up pointing the wrong way.
Characters walk through furniture instead of around it. The model
picks the spatially-wrong placement when one was under-specified.

**Mechanism.** Seedance reconstructs scene geometry from references
plus prompt text. When references don't show the exact geometry the
prompt requires — the camera position before a door, the direction
of a hallway, the path around a couch — the model picks a plausible
default that often disagrees with what the user expected.

**Counter.** Lock the geometry with a spatial layout block before
the action description. State explicitly:

- Where the camera sits at the start of the shot (`Camera inside
  the room, facing the closed door`).
- The relevant geometric features (`The couch sits between the
  character and the camera`).
- The direction-of-travel for any motion (`The character walks
  around the couch from screen-left to screen-right`).

See `SKILL.md` § Spatial Layout Block for the full block structure
and § Frame Coordinate System for the per-subject coordinate
vocabulary.

---

## Self-repair before delivery

Before the prompt goes to Seedance, run this pre-delivery checklist.
It consolidates the Counters above into a prevention pass so common
failures get caught at prompt-construction time rather than after a
burned generation.

- **Frame rate stated in prompt body** (not only meta header)?
  Cross-ref: § FPS drift.
- **Body-anatomy / sensual-register tokens scrubbed**? Cross-ref:
  § NSFW false-positive.
- **Elements appearing for the first time marked as absent from
  source keyframe**? Cross-ref: § Keyframe-consistency forces
  invention.
- **Adjacent-object invariants named** where applicable (`X stays
  attached`, `Y does not move`)? Cross-ref: § Physics-state-anchor.
- **Motion spends the whole clip in one direction**? Short actions
  chained into 2–3 same-direction beats; camera move has a named
  endpoint? Cross-ref: § Action-reversal fill.
- **Dialogue window fully written**? A short line extended (~8+ words in
  a 4-second shot) or its silence scripted, and every visible face
  carrying a mouth state? Cross-ref: § Filler-babble on a short dialogue
  line.
- **One dominant camera motion per shot**? Compound moves split into
  sequenced phases or separate cuts? Cross-ref: § Multi-motion
  camera overload.
- **Geometry locked with a spatial layout block** when more than one
  subject, or any shot historically prone to spatial failures
  (door-entry, hallway-direction, around-furniture)? Cross-ref:
  § Spatial-awareness failures.
- **Frame-level review time budgeted** for the resulting take?
  Cross-ref: § Frame-level review is mandatory.

The checklist takes 60-90 seconds per prompt and catches the
majority of preventable failures before credit burn.

---

## Cross-references

- `SKILL.md` § Filter Model — read-this-first for filter rejection
  vs render failure distinction
- `SKILL.md` § Voice Rewrite — language-level rewriting for filter
  passes (adjacent to § NSFW false-positive in this file)
- `SKILL.md` § When the User Is Already in a Failure Loop —
  filter-loop recovery (sibling to this catalog for the
  render-failure side)
- `SKILL.md` § Spatial Layout Block — block structure that prevents
  spatial-awareness failures
- `SKILL.md` § Frame Coordinate System — coordinate vocabulary that
  the spatial layout block uses
- `SKILL.md` § Single-vs-multi-shot decision — multi-shot split
  mechanics referenced from § Multi-motion camera overload
- `HELL-GRIND.md` § Dialogue construction — the audio-block phrasing
  and the `INNER (unspoken)` marker that § Filler-babble on a short
  dialogue line depends on
- `../higgsfield-troubleshoot/SKILL.md` § Sequence & Continuation
  Failure Atlas — symptom → single-repair-variable table for
  chained/continuation defects (this catalog covers single-clip
  render failures; the atlas covers the joins)
- `../higgsfield-soul/SKILL.md` § Character Sheet Creation —
  upstream character-anchoring discipline that prevents character-
  drift failures
- `../higgsfield-pipeline/SKILL.md` § Master Production Chain —
  upstream production workflow that establishes the frame-level
  review discipline named in this catalog
