# Template: Staging Reference (front-on blocking map)

`[DEMO — Tigran (tig-blocking-map v2), 2026-07-24]` A **staging reference** is a
deliberately schematic, colour-coded outline drawing attached to the generation alongside
the real location and character references. It tells the model **who is where** — nothing
else.

This is the companion to `top-down-map.md` and the opposite half of it. That template is
for **reasoning** about a space and its floor plan is never attached to anything; this one
is the reference a video model actually sees, and it is drawn **front-on from the camera's
side**, because video models think in frames, not floor plans.

> ## Read this before reaching for it — what it is measured to do
>
> - **It does NOT reliably move the blocking.** Measured across 24 cells: a first pass
>   came back inconclusive because the model's own compositional prior dominated 11 of 12
>   cells regardless of arm; a second, **counterbalanced** pass — two mirrored maps, so the
>   prior is identical in both arms and cancels — had renders tracking the map's
>   orientation **6/12, which is chance**. Do not promise a user that this pins positions.
> - **It IS safe.** **0/18 bleed** across both passes: with the three-layer architecture
>   below in place, the map's graphic look did not enter the shot.
>
> So: the anti-bleed architecture is settled and reusable, and the blocking claim is not.
> Reach for this when you want a shared, unambiguous *authoring* artifact for a complex
> multi-character frame — and when a position genuinely must hold, back it with the prose
> blocking locks in `../../skills/higgsfield-seedance/SKILL.md`, not with the map alone.

## The three-layer anti-bleed architecture

Bleed has exactly three feeds. This is the half that measured clean, and it only measures
clean because all three are closed at once.

1. **IMAGE — outlines, never fills.** Figures are thin, muted-colour outlines: no fills, no
   solid colour blocks, no shading, no texture. Line-work reads as *plan*; large flat colour
   fields read as *aesthetic* and get voted into the shot. Any grid stays very faint.
2. **TEXT — positive form only.** The block you paste into the video prompt **never names
   the map's graphic style at all** — not `flat`, `vector`, `schematic`, `grid`,
   `diagram`, `illustration`, and **not even as negations**. Models are weak at negation,
   so "no flat vector schematic look" still ships the tokens *flat*, *vector*, *schematic*
   into the prompt and primes the very style being banned. Instead, assert positively where
   style **does** come from — the location and character references. Graphic vocabulary
   lives in exactly one place: the diagram-*generation* prompt, which never touches the
   video prompt.
3. **STRUCTURE — attach it LAST.** Location and character references first, staging
   reference last, so the photographic references dominate the style vote.

**Never trade signal for stealth.** An ultra-faint map removes bleed *and* blocking — the
model reads geometry through the same pixels that could bleed. Reduce style **mass**
(outlines, muted colour, faint grid); never reduce signal **contrast**.

## Letters live in prompt-space, colours live in image-space

The drawing carries **only** coloured outline figures — no letters, no labels, no
typography. Rendered text is unreliable and a rendered letter can bleed into the shot.
Letters `A`, `B`, `C` exist only in the prompt text, bound to figures through colour
(*"@A = the BLUE figure"*). This keeps the full value of letters — stable, non-visual
handles you can use throughout the prompt (*"@A jerks his head"*) — at zero render risk.

One muted, maximally distinct colour per figure — muted blue, orange, yellow, purple, red,
green. **Colour is the identity of the letter only, never wardrobe.**

## Step 1 — the diagram-generation prompt

The source frame is attached to *this* generation as the composition guide, but it must be
scoped, and the assistant still translates every position, pose and facing direction into
explicit words: **the words carry the staging, the image pins the outline.**

```
@[Image 1](image_1) — use the attached image ONLY as the compositional guide: copy its
exact framing, camera angle, crop, and the positions, poses and scale of every person —
but do NOT copy its photographic look: no photo textures, no realistic lighting, no
realistic faces, no colors from the image. Do NOT add anything that is not in the attached
image. Do NOT complete cropped bodies — if a body part is cut off by the frame edge in the
image, cut it off in the drawing. The OUTPUT is a flat schematic:

Flat minimalist technical LINE DRAWING, a staging plan for a film scene — an obviously
schematic, non-photographic drawing on a white background with a very faint, thin,
light-grey graph-paper grid. Figures are drawn as clean THIN OUTLINES in muted colors —
NO fills, NO solid color blocks, NO shading, NO texture, NO realism, NO text, NO letters,
NO labels anywhere.

Front view matching the attached image's framing exactly: [N] outline figures.
[Per figure: POSITION IN FRAME — a MUTED-COLOR outline figure, what is visible (full body /
head and shoulders only / torso and arms only), pose exactly as in the image, facing
direction, any signature prop as a simple outlined shape and exactly where it sits relative
to the body.]
[Anchoring furniture/architecture as simple thin-outline shapes and where — or "no
furniture, open background."]

Nothing else — no ground line, no extra props, no extra figures. Simple, readable,
diagrammatic — flat 2D line drawing, minimal detail, only who is where.
--ar [match source frame] --style raw --stylize 30
--no photorealism, photo texture, realistic lighting, realistic faces, shading, solid color
fills, color blocks, text, letters, labels, typography
```

Deliver with it: the `@staging_` tag to assign to the **result**, the `@loc_` tag for the
source frame, and a one-line colour key (*"BLUE = the captive soldier, centre-foreground"*).

**Four frame-mismatch traps to check every time:** bodies cropped by the frame edge must be
described as cropped *and* forbidden from completion · head angle and gaze spelled out
· prop height pinned to anatomy (*"across the throat, under the chin — not the chest"*) ·
nothing added that is not in the frame.

## Step 2 — the connector block

Self-contained, positive form only, pasted as one block into the video prompt's references.

```
@staging_[PROJECT]_[scene]_[version] — POSITION REFERENCE ONLY
Use this reference solely to read where each figure is placed, its pose, and its facing
direction inside @loc_[PROJECT]_[name]_[scene]_[version]. Every visual quality of the shot
— style, light, color grade, faces, wardrobe, environment, props — comes exclusively from
@loc_[PROJECT]_[name]_[scene]_[version] and the character references. The shot is a fully
photoreal live-action frame.

LETTER LEGEND (letters exist only in this prompt; they do not appear on the reference)
@A = the BLUE figure on the staging reference = [character tag] → [position, pose, facing].
@B = the ORANGE figure on the staging reference = [character tag] → [position].

RENDER RULE: place the real, photoreal characters (from their own references) into the real
location @loc_[PROJECT]_[name]_[scene]_[version] at the positions this reference defines,
and take nothing else from it.

LOCKS: All style, light, and texture come exclusively from
@loc_[PROJECT]_[name]_[scene]_[version] and the character references;
@staging_[PROJECT]_[scene]_[version] defines positions only. The colors on the staging
reference identify WHO IS WHO on that reference only — wardrobe and grading come from the
character and location references. Everyone stays in their staging-locked position until
their scripted action.
```

**Attachment order: location and character references FIRST, staging reference LAST.**

## Tag naming

`@loc_[PROJECT]_[name]_[scene]_[version]` and `@staging_[PROJECT]_[scene]_[version]`.
`[PROJECT]` in caps. Pair the staging name with its location name visibly so the two read
as belonging together. Bump `_v2`, `_v3` on every retake and reference only the active
version per shot — a stale tag causes ghost blocking.

## Revising a diagram

`[FIELD — Higgsfield Studio, ONEIRIC breakdown, 2026-08-13]` Two rules, and the second is
the one that quietly ruins a sequence:

1. **Name every element by its assigned colour, never by the object or person.** *"Move the
   BLUE figure to the couch's left edge"*, not *"move Rudy"*. Colour is the diagram's
   language; character names belong to the video prompt. Ask for the revision in the same
   place the original diagram prompt was written, so the full colour key and geometry are
   still in play.
2. **Regenerate from the ORIGINAL FRAME, never from the previous diagram.** A diagram is
   always drawn from the real shot. Feed a drawing back into the image model and it starts
   copying **the drawing's flaws** instead of the frame's geometry — every pass compounds
   the last one's errors.

**Coverage becomes a conversation.** Once a scene has a diagram, new setups are cheap to
ask for: *"give me the MCU on the blue"*, *"now the POV of the green"* — and you get a
re-staged diagram for the new shot size or angle, with the same colour bindings intact.

**Keep the drawing out of the writing loop.** The prompt is written from the *text*
description of the frame, not by looking at the diagram image — which is why every figure's
position, pose and facing has to be spelled out in words at step 1. The words are what the
video prompt is built from; the drawing only has to agree with them.

> **Talk about it as spatial data, not as a picture.** The framing that makes this work is
> treating the reference as a system of lines, colours, coordinates and directions rather
> than an image to copy — which is why it is worth avoiding the words "image" and
> "reference" when instructing around it, and saying *positions, poses, facing directions*
> instead.

## Known failures

| Failure | Cause | Fix |
|---|---|---|
| Map look enters the shot | Any of the three feeds — colour-block fills, graphic vocabulary in the video prompt (**including as negations**), or the map attached before the photo references | Fix at all three layers, then bump the version tag |
| Colour → wardrobe bleed (blue figure → blue tunic) | Filled figures, saturated palette, identity not routed to a character reference | Outlines not fills, muted palette, legend routes identity to the character tag whose own reference owns wardrobe |
| Model invents what isn't in the frame | Missing guard lines | "Do NOT add anything that is not in the attached image" + "do NOT complete cropped bodies"; put the invented item in `--no` once it has appeared |
| Prop drifts (sword throat → chest) | Prop not pinned to anatomy | Pin with a positive **and** a contrast |

## QA checklist

**On the diagram, before assigning the tag:** thin outlines only · no text or labels
anywhere · cropped bodies stay cropped · props at the exact anatomical height · poses match
the frame (head angle, gaze, mouth) · framing and aspect match the source.

**On the video result:** fully photoreal, no graphic look · no white/grid background
artifacts or drawn-line edges · no staging colours in wardrobe or grade · no typography ·
positions held until the scripted action. If any check fails, fix at the layer that fed it.

## Extensions

Same convention, one distinct muted colour per path, each bound in the legend:

- **Trajectory maps** — a bullet, a bird, a thrown object. Design the curve on the faint
  grid (the grid is for **you**; the model reads the drawn path, not grid cells) and deliver
  it as a dashed line. Bind four facts: START, PATH shape, END, TRIGGER beat.
- **Camera path maps** — arrows for dolly/pan, declared in the legend as *"arrows = camera
  path only."*
- **Movement maps** — a dashed line for a character's cross, with start, path, end mark,
  and **when** the move happens, tied to a beat.
