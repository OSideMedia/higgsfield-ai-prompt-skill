# Template: Ad-Asset Prep (lock everything before the camera moves)

A checklist for prepping a commercial's assets **before** any video generation.
Assets recur in every scene, so locking the product, characters, locations, and
props up front is what keeps a fully-AI ad consistent once motion starts. The
thesis from the cinematic-commercial workflow: *generate many, test in motion,
lock the winner* — and design each asset so more outputs come back usable.

## Design for win rate

A quiet multiplier behind the whole workflow: shape each asset so a **higher
fraction of generations come back usable** (the "win rate"). It is the
asset-design face of the acceptance-rate discipline in
[`../DISCIPLINE.md`](../DISCIPLINE.md) and
[`../docs/production-benchmarks.md`](../docs/production-benchmarks.md) — same
idea, applied upstream at sheet-creation time instead of downstream at take-
selection time.

- **Grey background wins more often** — nothing in frame competes with the
  subject, so the model has less to get wrong.
- **3/4-angle locations beat flat head-on** — they give the camera depth to move
  through, so motion tests survive more often.
- **One clean subject per sheet** — a single, unambiguous thing to lock onto.

Higher win rate compounds: cheaper iteration, fewer regenerations, more keeper
seconds per credit.

## The checklist

### 1. Product sheet from a single image

Drop one product photo into GPT Image 2 and ask for **front and 3/4 views** so
the model knows the product from every side and won't hallucinate it mid-scene.
See `../skills/higgsfield-gpt-image-2/reference-sheet-workflow.md`.

### 2. Hero character sheet (Soul Cinema, grey background)

Close-up (locks the face) **+** full-body front/back (locks the build), on a
**grey background**, generated in **Soul Cinema** for the best photoreal skin
texture. See `../skills/higgsfield-soul/SKILL.md` § Character Sheet Creation.

### 3. Lock one face — erase the duplicate

A character sheet with **multiple faces** makes the video model "not know which
face to grab," so it drifts. Bring the sheet into GPT Image 2 and erase the
extras, leaving one face to lock onto:

```
(in GPT Image 2, on the character sheet)
Erase the face from the full-body shot on the right panel.
```

One face left → the video model stops drifting between faces.

### 4. Outfit design loop — 10 ideas → mix and recolor

Ask Claude for the ideas, generate them, then combine:

```
Give me 10 casual outfit ideas for this character. Write each one as an image prompt.
```

Generate all 10, then **mix and recolor** in GPT Image 2:

```
Take the shirt from look 2, make it pink, keep the jeans from look 1,
combine into one prompt. Keep the face, skin, and background unchanged.
```

### 5. Preserve realism after an edit — the anti-"slop" composite

Every GPT Image edit softens Soul-grade skin toward flat "AI slop." The fast
manual fix is a layer-mask composite — see
`../skills/higgsfield-soul/SKILL.md` § Two-Tool Refinement Pipeline (the
layer-mask composite worked example).

### 6. Multi-state variants — bake the state in on purpose

Build separate locked sheets for each state the ad needs — final look (`@hero`),
athletic look (`@s_hero`), **soaked/sweaty** look (`@s_hero_wet`). Build the wet
version **now**, on purpose: asking GPT Image to "sweat him up with words" later
makes it improvise and "the face drips off of him."

### 7. Prop sheets (objects skip the motion test)

Clean studio prop sheets (shoes, bag, moka pot, mug) into GPT Image 2. **No
motion tests** — props are objects, they don't perform; the prop sheet is enough.
Generate-many / test-in-motion / lock applies to *performers*, not props.

### 8. Register the `@`-glossary

Declare every asset once with a stable `@`-name and register each under
**Elements** with the same name so prompts auto-attach the right images:

```
@hero — main character          @boss — side character
@headphones — product           @sneakers · @bag · @skydancer — props
@kitchen · @stadium · @street — locations
@s_hero — athletic-look hero     @s_hero_wet — sweaty post-run hero
@music_track (audio_1.wav) — motion locks to this beat
```

Full slot→role discipline:
`../skills/higgsfield-seedance/SKILL.md` § Reference Roles. This glossary is the
second layer of the connected shotlist —
`../skills/higgsfield-shotlist-director/SKILL.md`.

## Related

- `../skills/higgsfield-soul/SKILL.md` — character sheets + the anti-slop composite
- `../skills/higgsfield-gpt-image-2/SKILL.md` + `…/reference-sheet-workflow.md` +
  `…/static-ads-workflow.md` — product/prop sheets, location editing
- `../skills/higgsfield-shotlist-director/SKILL.md` — where these locked assets
  feed the connected shotlist
- `../DISCIPLINE.md` — the acceptance-rate philosophy "win rate" is the upstream
  face of
