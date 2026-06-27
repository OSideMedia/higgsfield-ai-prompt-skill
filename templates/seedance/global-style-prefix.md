# Template: Global Style Prefix (the edit-once block)

A single style block **glued verbatim to every prompt** in a connected Seedance
2.0 shotlist. Edit it once → it changes everywhere. It locks the film's global
look so 25 separately-generated scenes read as one piece.

## When to use this template

Any multi-scene Seedance production where every clip must share a look —
commercials, short films, branded content. It is the top layer of the
[`higgsfield-shotlist-director`](../../skills/higgsfield-shotlist-director/SKILL.md)
artifact: prepended to every per-scene prompt's copy-block, and shown once in a
collapsible block at the top of the shotlist HTML.

The prefix locks the **global** look. A single scene can break it with a
**per-scene override** (see below) — a local edit to just that prompt's prefix,
not a change to the global block.

## Default prefix block (fill in the blanks, then freeze)

Replace the bracketed fields; keep the labelled structure. Once set, do not edit
per-prompt — edit it once and re-render the whole shotlist.

```
Style: [8K IMAX commercial], [16:9] widescreen. Photorealistic — no 3D render, no game engine.
Lighting: [Natural light only — soft, even morning daylight, gentle atmospheric haze throughout. Key light from sky and windows only. No artificial light.]
Color: [60:30:10] — dominant / secondary / accent.
Camera: Physical cine lens. 180° shutter motion blur.
Skin: Pore-level realism — vellus hair, asymmetric moles, capillary flush, pore-shadow matching on-set light.
Acting: Hollywood — micro-pauses before reactions, precise eye-line, living eyes with catch-lights, chest rise from breathing. Characters never standing, always reacting.
Physics: Gravity and inertia respected — mass has real weight, correct contact shadows. No floating props.
Composition: Rule of thirds + golden ratio. Every person moving from frame one.
Continuity: Characters, props, environment identical across every cut. No identity drift.
Technical: 24fps smooth motion. 8K detail. No jitter.
Audio: Diegetic dialogue and environmental SFX only. No music. No subtitles.
```

Notes on the fields:

- **Format / resolution** — match the deliverable's aspect ratio. Seedance 2.0
  supports `auto/21:9/16:9/4:3/1:1/3:4/9:16` and `480p/720p/1080p/4k` (4K in
  `mode=std` only). Keep it inside the model enum — the preflight linter catches
  out-of-enum values.
- **Color `60:30:10`** — dominant / secondary / accent ratio; name the three
  colours in the per-scene Scene block, not here.
- **Audio: diegetic-only** — the prompt body names only real-world SFX; layer any
  score in post. See `../../skills/higgsfield-audio/SKILL.md` § Seedance 2.0 and
  the diegetic-only convention.
- **No negative phrasing** — every line is a *positive* declaration of what must
  be true (Seedance reads the body as positive instruction only). See
  `../../skills/higgsfield-seedance/SKILL.md` § Prompt-Craft Laws → No negative
  prompts in the prompt body.

## Per-scene override example (Scene 2 / sunny stadium)

One scene breaks the soft global look. Replace **only the Lighting line** in that
single prompt's prefix; every other field — and every other scene — stays on the
global block:

```
Lighting: Natural light only — bright, genuinely sunny midday, strong direct sunlight from high and frontal (sun in front of and above the subject, behind the camera), deep blue sky, crisp hard-edged shadows, vivid saturated colour, low haze.
```

The override is a local edit to one prompt, not an edit to the global Style
Prefix. If you find yourself overriding the same field in many scenes, that field
belongs in the global block instead — fold it up and re-render.

## Related

- `../../skills/higgsfield-shotlist-director/SKILL.md` — the connected shotlist
  this prefix sits at the top of
- `../../skills/higgsfield-seedance/SKILL.md` § Prompt-Craft Laws — the per-prompt
  grammar the prefix wraps
- `../../skills/higgsfield-cinema/SKILL.md` § Manual Style — project-level style
  control for Cinema Studio (sibling concept, different surface)
