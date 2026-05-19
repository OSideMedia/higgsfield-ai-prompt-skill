# Template: Multi-Character Anchor Prompt

Paste-ready Seedance 2.0 prompt template for shots with two or more
characters in frame. Locks per-character identity, position, depth,
pose, gaze, and contact points before the action description.

## When to use this template

Any Seedance prompt with two or more characters where placement,
orientation, and inter-character relationship matter — character
swaps, axis crossings, eyeline mismatches all drop noticeably when
this template is used instead of inline spatial fragments.

## Prompt template

```text
[At/from N seconds] N characters in frame.

Character A — [identity, Soul ID handle].
  Screen position: [left third / center / right third],
  x-position [%], y-position [%], frame occupancy [%].
  Depth layer: [foreground / midground / background].
  Body orientation: [toward camera / away / profile-left /
    profile-right / three-quarter].
  Pose: [physical configuration — standing, seated, mid-stride].
  Gaze: [where they look — frame-position OR "looking at Character B"].
  Contact points: [physical surfaces they touch — feet on wet
    asphalt, left hand on the railing].
  State lock: [emotional or physical state — calm, exhausted,
    injured, soaked].

Character B — [identity, Soul ID handle].
  [...same fields...]

Cross-character relationships:
  Distance between A and B: [approximate].
  Eyeline: [A → B, B → A, both → off-screen, mutual avoidance].
  Crossing rule: [neither crosses the central vertical axis /
    A may cross right-to-left at N seconds].
  Negative space: [where the empty area sits in frame].

Camera: [shot size], [angle], [lens], [movement].
Setting: [location, time, weather, atmosphere, production design].
Aesthetic: [genre, lighting, color grade, texture, VFX].
Audio: [ambience, SFX, dialogue, music].
Continuity locks: [costume / state / prop invariants].
Final frame: [composition at last frame].
```

## What goes in each field

- **Identity** matches a Soul ID character handle (see
  `../../skills/higgsfield-soul/SKILL.md` § Character Anchor Block
  for the 10-attribute per-character structure this template consumes)
- **Screen position** pairs qualitative anchor + percentage notation
  per `../../skills/higgsfield-seedance/SKILL.md` § Frame Coordinate
  System (vocab.md § Editing Syntax bracket notation ships in v3.7.7
  sub-phase 2f)
- **Contact points** prevent the character-floating failure mode
  catalogued in `../../skills/higgsfield-seedance/FAILURE-MODES.md`
- **Cross-character relationships** prevent character-swap and
  axis-crossing failures — see § Spatial Layout Block in the seedance
  SKILL.md for the structural rationale

## BAD / GOOD / GREAT

**BAD:** Inline spatial fragments scattered through the Dynamic
Description. `Character A walks in. Character B is by the window.`
Result: Seedance picks default positions; A and B swap across cuts;
eyelines drift.

**GOOD:** Use the template, fill in per-character anchor block,
specify qualitative position only (`left third` / `right third`).
Spatial accuracy improves; cross-character relationships hold
better. Coordinate precision is still under-specified for tight
shots.

**GREAT:** Use the template, fill every field including percentage
notation paired with qualitative anchors, specify cross-character
relationships (distance + eyeline + crossing rule + negative space —
see [vocab.md](../../vocab.md) § Composition Vocabulary → Crossing rule
+ § Negative space). Pre-visualize the scene with `top-down-map.md` first
and paste the
blocking note Claude generates into the Character A / Character B
fields. Block is reusable across cuts with the same characters —
copy and adjust per cut rather than re-specifying.

## See also

- `top-down-map.md` (sibling) — meta-prompt that generates the
  blocking note this template consumes
- `worked-example-two-character.md` (sibling) — concrete end-to-end
  fill of this template structure
- `../../skills/higgsfield-soul/SKILL.md` § Character Anchor Block —
  the 10-attribute per-character structure
- `../../skills/higgsfield-seedance/SKILL.md` § Frame Coordinate
  System + § Spatial Layout Block — the vocabulary + block this
  template uses
