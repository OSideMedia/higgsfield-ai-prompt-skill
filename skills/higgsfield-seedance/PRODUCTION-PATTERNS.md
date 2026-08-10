# Production Patterns — Tutorial-Demonstrated

`[DEMO — Seedance-4K film tutorial, 2026-07]` (plus a closing
`[FIELD]` section of harvest-sourced patterns — see § Field-Harvested
Patterns)

Patterns shown **working on screen** in Higgsfield's own Seedance-4K film
tutorial and its blog breakdown. Demonstrated, not spec-guaranteed: each one
produced the claimed result in the tutorial's footage, but none of them is a
model parameter. Read alongside `SKILL.md` § Official Prompt Architecture —
the Block Scaffold (the `[OFFICIAL]` doctrine these patterns are applied
inside) and § Reference Roles (the semantic-role taxonomy the vocabulary
below plugs into).

Model-parameter facts referenced here come from `../../specs/model-specs.json`
(seedance_2_0: duration 4–15s; 480p/720p/1080p/4k with 4k/1080p requiring
`mode=std`; media roles `start_image` / `end_image` / `image_references` /
`video_references` / `audio_references`).

---

## Reference-Role Vocabulary

Three in-prompt role phrases, each changing how the model reads a reference:

| Phrase | Role | Effect |
|---|---|---|
| `"100% matches the reference"` | Identity lock | The subject must render as the reference shows it — same phrase the official `@TAG:` line ends on. Use for characters and hero props. |
| `"STYLE REFERENCE ONLY, not a fixed keyframe; the model extends the world"` | Location style | The reference sets look and architecture, but the model may extend beyond the visible frame. Use for locations so the camera isn't chained to the reference's exact crop. |
| `"VARIETY reference"` | Crowd diversity | A multi-character lineup sheet read as a sampling pool, not an identity. |

**The clone-army failure and its fix:** a single-character reference used for
a crowd produces a crowd of that one character. The tutorial's fix: build a
lineup sheet with several distinct characters (a 4-elf lineup in the demo),
attach it once, and relabel it in-prompt as a `VARIETY reference` — the model
then samples a diverse crowd from the sheet instead of cloning one face.

These phrases map onto `SKILL.md` § Reference Roles: `100% matches` is the
Character/Prop role stated in the model's own working vocabulary;
`STYLE REFERENCE ONLY` is the Environment role; `VARIETY reference` is a
crowd-specific extension the four-role taxonomy doesn't otherwise name.

---

## Coordinate Blocking

Extends `SKILL.md` § Frame Coordinate System with two demonstrated notations:

- **Size as % of frame width** (alongside frame-area occupancy):
  `"@TRUCK a tiny speck under 4% of frame width at x38% y44%"` — position and
  size pinned in one clause.
- **Locked screen direction:** `"travel screen-left to screen-right, locked"`
  — the word `locked` is doing the work; without it, long moves drift or
  reverse. Pair with per-character body orientation (which way each subject
  faces) for multi-character blocking.

---

## Non-Empty Opening Frame

Describe the first frame with the subject **already in motion** and the
framing asymmetric. An opening frame described as empty or static invites the
model to spend the first seconds "arriving" — dead air at the head of a 4–15s
clip is expensive. Same discipline as the official FIRST FRAME / BLOCKING
block: everyone moving from frame one.

---

## Per-Segment LENS LOCK + Timed Cut Control

Demonstrated multishot control stack:

- Exact-count timed cuts: `"Exactly one HARD CUT, at 0:07; otherwise the
  camera holds still."` — count + timestamp + hold clause in one line.
- Multi-segment FORMAT MODE with a **LENS LOCK per segment** (explicit FOV
  phrase opening each segment), `SMASH CUT` into a slow-motion segment,
  `MATCH CUT` between graphically-rhymed frames.

This is the cut-format ladder and the 4-mechanism extreme-FOV stack
(`SKILL.md` § Official Prompt Architecture — the Block Scaffold) applied
together; per-segment timing must still sum to the declared duration
(`SKILL.md` § Output Format → Runtime arithmetic).

---

## Red-Arrow Prop Annotation

When a character keeps interacting with the wrong part of a prop (pressing
the wrong button, gripping the wrong handle): **draw a red arrow on the prop
reference sheet** pointing at the correct spot, then have the prompt-writing
model describe exactly where the arrow points, so the prompt encodes it in
words — e.g. `"The reference's red arrow points precisely to the CH-UP
chevron (^)."` The annotation lives on the sheet; the instruction lives in
the text. Same principle as the official rule to state critical details
(small text, logos, colors) in words even when visible in the reference.

---

## Video-Reference 1:1 Lock + SCREEN REALISM

For compositing a finished clip onto an in-frame screen (TV, phone, monitor):
attach the finished clip via the `video_references` role and lock it hard:

```
@video1 matches the source 1:1 — never reinterpreted, re-edited, cropped,
looped early, or replaced.

SCREEN REALISM
Glass sheen and room reflections on the screen surface, faint sub-pixel
grid, slight moiré, highlight bloom, screen seen at a slightly off-axis
angle.
```

The 1:1 clause stops the model from "improving" the footage; the SCREEN
REALISM block makes the composite read as a physical screen instead of a
pasted rectangle.

**Duration-match rule:** the new generation's duration must **exactly match
the reference clip's duration** — otherwise Seedance starts making things up
past the reference's end. The tutorial cut a scene to its first 6 seconds to
feed a 6-second composite. (Both durations must sit inside the model's 4–15s
range.)

---

## Prompted Imperfection as Realism

Perfect renders read as synthetic. The tutorial prompts optical flaws in as
content: heat-haze swim, telephoto micro-tremor, a digital-zoom "mushy"
smear, a brief focus hunt before lock. Quantify atmosphere per the official
%-rule — the demo ran a haze ramp from 20% to 70% across the shot.

The word **content** is load-bearing: each flaw above is attached to something —
a named element at a named moment, or, for the atmospheric ones, a quantified
ramp with a stated extent. The same vocabulary written as a bare quality plea
trailing the prompt is the degradation case, not this one — see
`../shared/negative-constraints.md` § Whole-Frame Degradation, which also covers
the § Field-Harvested Patterns motion-blur bullet below.

---

## 60:30:10 Color Grade

State the grade as proportions — **60% dominant / 30% secondary / 10%
accent** — with each color tied to a source and a surface, never a flat
color list. This is the official color-via-material-plus-light rule with
proportions attached; it lives in the COLOR GRADE block of a block-scaffold
prompt.

---

## Offscreen Voice-Only Characters

Declare a character who speaks but must never appear:

```
(Mother is an offscreen English voice only — no in-frame reference, never
enters the shot.)
```

This reconciles with the engine rule that off-screen = nonexistent
(`ENGINE-RULES.md`): the parenthetical tells the model the voice has no
body to frame, so it neither invents one nor pulls the speaker into shot.

---

## Specify What Plays on Screens

Never leave an in-frame screen's content to the model — unspecified screens
fill with text-slop. Name every item in sequence: `"the TV plays a news
broadcast, then a perfume ad, then a car ad, then @Image4."` A reference
tag is valid screen content (see § Video-Reference 1:1 Lock above for
full-clip composites).

---

## In-Prompt Scene Transitions

Two demonstrated ways to move between scenes without an editing cut:

- **The TV hand-off:** build the *next* scene's location early and put it on
  an in-scene TV as the last channel — the clip's final frame (the screen
  filling with the new location) becomes the next scene's opening frame.
- **Scale transitions in-prompt:** a continuous move from an army-wide shot
  down to a palm-sized duel, written as one camera journey rather than a cut.

---

## Field-Harvested Patterns

`[FIELD — 13-project community harvest, 2026-07-18]` — patterns pulled from
harvested production prompts rather than the tutorial. Same status as [DEMO]:
worked in production, not spec-guaranteed.

- **Selective motion blur as artifact concealment.** Most projects ban motion
  blur; one 4K tech-demo *inverts the ban on purpose*: "water-covered faces,
  hands, and foreground figures crossing the lens get motion blur to hide
  artifacts." Where the model is weakest (lens-crossing limbs, water-occluded
  faces), prompt blur onto exactly those elements to mask it.
- **HEX-array color lock (image prompts).** Beyond the 60:30:10 prose grade,
  a still prompt can end with a machine-readable palette — `HEX VALUES:
  ["#9d6e5f","#a87e72","#3f4591","#30317f", …]` — locking the color world as
  a list, not a description.
- **Generate forward, reverse in the edit.** A rewind/time-reversal effect is
  never generated — forward plates are reversed manually in post. The model
  only ever renders forward-time physics.
- **Populated-plate reuse.** For a recurring crowded set (a restaurant),
  composite the cast + background diners onto the location plate ONCE, then
  reuse that populated plate as the reference for every seated scene — the
  seating, eyelines, and crowd inherit from one source instead of re-rolling
  per shot. (Complementary to the empty-plate rule in
  `../../templates/ad-asset-prep.md`: empty when the model should own the
  crowd, populated-once when the crowd must repeat.)
- **Transformation staged off-screen.** A character-to-creature (or
  creature-to-character) transformation is "never shown mid-morph unless
  staged as a shadow silhouette — otherwise it happens off-screen, only
  before/after shown." Avoids the model's morph failure mode by design.
