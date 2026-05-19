# Template: Worked Example — Two-Character Anchoring (Neo-Noir Alley)

Concrete end-to-end demonstration of `multi-character-anchor.md`
applied to a real scene. Shows what the template fields actually fill
with when the scene is named.

## The scene

Two characters on a rain-soaked alleyway at night. A detective
("Roco") confronts a suspect ("Lulu") who is backing toward a chain-
link fence. Tension; no contact yet. Cinematic neo-noir register.

## The filled prompt

```text
At 0 seconds, two characters in frame.

Character A — Roco (Soul ID @Image1).
  Screen position: left third, x-position 30%, y-position 55%,
    frame occupancy 28%.
  Depth layer: midground.
  Body orientation: three-quarter toward Lulu, screen-right.
  Pose: standing, weight on back foot, right hand resting on coat
    pocket.
  Gaze: locked on Lulu's eyes.
  Contact points: boots planted on wet asphalt, shoulders square.
  State lock: composed, alert, controlled aggression.

Character B — Lulu (Soul ID @Image2).
  Screen position: right third, x-position 70%, y-position 60%,
    frame occupancy 24%.
  Depth layer: midground (1 meter behind Roco's depth plane).
  Body orientation: three-quarter toward Roco, screen-left.
  Pose: backing one step at a time, hands raised at chest height,
    palms out.
  Gaze: darting between Roco's eyes and the alley behind her.
  Contact points: back nearly touching chain-link fence, boots
    sliding on wet asphalt.
  State lock: cornered, calculating, afraid but controlled.

Cross-character relationships:
  Distance between Roco and Lulu: ~3 meters, closing.
  Eyeline: Roco → Lulu sustained; Lulu → Roco intermittent.
  Crossing rule: neither crosses the central vertical axis of the
    frame in this shot.
  Negative space: centered between them, narrowing as Roco advances.

Camera: medium-two-shot, low angle (camera at chest height), 35mm
  anamorphic lens, slow dolly-in 0.5m over the shot duration.
Setting: rain-soaked alleyway, 2am, light rain, sodium-vapor street
  lamp from screen-right above, steam from a manhole behind Lulu,
  garbage bags + chain-link fence + brick walls.
Aesthetic: neo-noir, high-contrast key-and-fill with deep shadows,
  desaturated palette with sodium-orange highlights, film grain
  visible, no VFX.
Audio: light rain continuous, distant traffic, Roco's footstep on
  wet asphalt at 2s, Lulu's breath audible, no music.
Continuity locks: Lulu's hands stay raised throughout; Roco's right
  hand stays on coat pocket; neither character changes position by
  more than ~1m.
Final frame: Roco one step closer, Lulu's back touching the fence,
  eyeline locked, negative space narrowed to half the original.
```

## What this demonstrates

- Every `multi-character-anchor.md` field filled — including cross-
  character relationships (distance + eyeline + crossing rule +
  negative space) per § Spatial Layout Block in the seedance SKILL.md
  + [vocab.md](../../vocab.md) § Composition Vocabulary → Crossing
  rule + § Negative space
- One dominant camera motion (slow dolly-in) — no compound moves per
  § Multi-motion camera overload in FAILURE-MODES.md
- Continuity locks explicit + Soul ID handles (`@Image1`, `@Image2`)
  match upload-order convention — see § Per-Image Role Convention +
  § Multi-Form State Tracking + § Physics-state-anchor for the
  discipline behind state + handle locks

## See also

- `multi-character-anchor.md` — the template this example fills
- `top-down-map.md` — pre-visualize before filling the template
- `../../skills/higgsfield-soul/SKILL.md` § Character Anchor Block —
  per-character 10-attribute structure
- `../../skills/higgsfield-seedance/SKILL.md` § Spatial Layout Block —
  the prompt-body block this example assembles
- `../../production-benchmarks.md` § Per-character iteration anchor —
  budget anchors for the Soul ID generation pass that built Roco and
  Lulu's character sheets
