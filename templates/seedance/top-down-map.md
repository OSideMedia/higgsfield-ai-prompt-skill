# Template: Top-Down Floor Plan Pre-Visualization

Meta-prompt template for **Claude** (not Seedance). Generates a top-down
floor plan + paste-ready Seedance blocking note in one pass — locks
spatial geometry before any Seedance generation begins.

## When to use this template

Any multi-character or geometrically-complex shot where Seedance has
historically picked the wrong spatial reassembly — door-entry shots,
hallway-direction shots, two-character blocking that needs to hold
across cuts. See `../../skills/higgsfield-seedance/FAILURE-MODES.md`
§ Spatial-awareness failures for the failure class this template
prevents.

## Claude prompt template (paste-ready)

```
Build a top-down floor plan for [SCENE]. Mark every character with
their position, which direction they're facing, and who they're
looking at. Include distance between characters and a scale.

Below the diagram, write a paste-ready blocking note for Seedance —
one short paragraph per character covering: where they are, which way
they face, gaze line, pose, what they're touching.

Render as an HTML artifact.

Scene: [DESCRIPTION]
```

Fill `[SCENE]` with the one-line scene title (e.g., "diner standoff").
Fill `[DESCRIPTION]` with the full scene description — characters,
location, action, mood. The richer the description, the better the
spatial reassembly.

## What you get back

- An HTML artifact rendering the top-down floor plan visually
- A paste-ready blocking note formatted for direct copy into the
  Seedance prompt body's Spatial Layout Block (see
  `../../skills/higgsfield-seedance/SKILL.md` § Spatial Layout Block
  for the block structure that consumes this output)

## BAD / GOOD / GREAT

**BAD:** Skipping pre-visualization. Write the Seedance prompt
directly from the scene description; let Seedance pick the spatial
reassembly. Result on multi-character shots: characters end up on the
wrong sides of frame, walk through furniture, face the wrong direction.

**GOOD:** Use this template, get the top-down map, eyeball the
geometry, transcribe the relevant placement into the Seedance prompt
manually. Spatial accuracy improves significantly. The transcription
step introduces errors when geometry is complex.

**GREAT:** Use this template AND paste the blocking note Claude
generates directly into the Seedance prompt's Spatial Layout Block.
Zero transcription. The geometry Claude reasoned about and the
geometry Seedance receives are identical. Iterate the floor plan in
the Claude chat before locking — adjust positions, gaze lines, contact
points until the map matches intent, then copy the blocking note over.

## See also

- `../../skills/higgsfield-seedance/SKILL.md` § Frame Coordinate System
  — coordinate vocabulary the blocking note uses
- `../../skills/higgsfield-seedance/SKILL.md` § Spatial Layout Block —
  the prompt-body block that consumes the blocking note
- `../../skills/higgsfield-seedance/FAILURE-MODES.md` § Spatial-
  awareness failures — failure class this template prevents
- `multi-character-anchor.md` (sibling template) — paste-ready
  multi-character Seedance prompt that consumes the blocking note
