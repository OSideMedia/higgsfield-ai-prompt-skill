# Template: Single-Character Position Prompt

Paste-ready Seedance 2.0 prompt template for shots with one character
in frame. Simpler companion to `multi-character-anchor.md` for cases
where there is no cross-character geometry to lock.

## When to use this template

Single-character shots where position, pose, and contact points still
matter — character-walks-into-frame, character-pulls-prop, character-
delivers-line. For shots with two or more characters, use
`multi-character-anchor.md` instead.

## Prompt template

```
[At/from N seconds] One character in frame.

[Identity, Soul ID handle].
  Screen position: [left third / center / right third],
  x-position [%], y-position [%], frame occupancy [%].
  Depth layer: [foreground / midground / background].
  Body orientation: [toward camera / away / profile-left /
    profile-right / three-quarter].
  Pose: [physical configuration].
  Gaze: [where they look — frame-position or off-screen direction].
  Contact points: [physical surfaces — feet planted, hand on doorframe].
  State lock: [emotional or physical state].

One dominant action: [single action — one motion verb at the spine
  of the shot per § Single-vs-multi-shot decision].
Motion: [secondary motion — hair, fabric, breath; eye motion].

Camera: [shot size], [angle], [lens], [movement — one dominant
  motion per § Multi-motion camera overload guidance].
Setting: [location, time, weather, atmosphere].
Aesthetic: [genre, lighting, color grade, texture].
Audio: [ambience, SFX, dialogue, music].
Final frame: [composition at last frame].
```

## What goes in each field

- **Identity + position + depth + orientation + pose + gaze + contact
  points + state lock + facial expression** are the 10 attributes of
  the Character Anchor Block — see
  `../../skills/higgsfield-soul/SKILL.md` § Character Anchor Block
  for the full attribute structure
- **One dominant action + Motion** separation prevents the multi-
  motion overload failure — see
  `../../skills/higgsfield-seedance/FAILURE-MODES.md` § Multi-motion
  camera overload

## See also

- `multi-character-anchor.md` (sibling template) — multi-character
  version with cross-character relationships
- `top-down-map.md` (sibling template) — meta-prompt to pre-visualize
  position before filling this template
- `../../skills/higgsfield-soul/SKILL.md` § Character Anchor Block —
  10-attribute per-character structure
- `../../skills/higgsfield-seedance/SKILL.md` § Frame Coordinate
  System — position vocabulary
