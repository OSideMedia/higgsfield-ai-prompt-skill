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
[`../production-benchmarks.md`](../production-benchmarks.md) — same
idea, applied upstream at sheet-creation time instead of downstream at take-
selection time.

- **Grey background wins more often** — nothing in frame competes with the
  subject, so the model has less to get wrong. The Seedance-4K film tutorial
  states this as tested: "after tons of testing, grey performs way better than
  white or black" [DEMO — Seedance-4K film tutorial, 2026-07]. Any neutral
  grey works — light-grey cyclorama for people, medium grey for props,
  `#7f7f7f` for creature sheets. Field confirmation of the same practice,
  with a second pinned value: harvested production **human**-sheet prompts
  run "flat solid neutral grey background (#8a8a8a), seamless, no gradient,
  only a soft contact shadow" — with both views "matched in scale, lighting,
  and style for consistency" [FIELD — 13-project harvest, 2026-07-18]. Any
  mid-grey works; what matters is pinning ONE exact hex per project so every
  sheet matches (`#7f7f7f` creature / `#8a8a8a` human are both proven picks). (Anime/manga sheets are the exception:
  they run white seamless — see `../image-models.md` § Seedream 5.0 Pro.) This bullet is the canonical home of the
  grey rule; the sheet workflows in
  `../skills/higgsfield-gpt-image-2/reference-sheet-workflow.md` and
  `../skills/higgsfield-soul/SKILL.md` § Character Sheet Creation point here.
- **3/4-angle locations beat flat head-on** — they give the camera depth to move
  through, so motion tests survive more often. See § Location plates below for
  the empty-plate rule.
- **One clean subject per sheet** — a single, unambiguous thing to lock onto.
  (The one deliberate exception: crowd work, where you *want* a multi-character
  VARIETY lineup sheet — see `../skills/higgsfield-soul/SKILL.md`
  § Variety Sheets.)

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
texture. One clear face + one full body is the hard floor per character — never
ship a character on a single image ("so Seedance doesn't have to guess").
See `../skills/higgsfield-soul/SKILL.md` § Character Sheet Creation.

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

### 6b. Related characters — derive the face, don't describe it

[FIELD — 13-project harvest] For siblings/relatives, don't describe family
resemblance independently — **generate the relative from the same face**:
"the 13–14-year-old younger sister of the man in the reference, his spitting
image: take the exact face from the reference and translate it onto a
naturally younger teenage girl — same eyes, brows, nose, lips, same moles
and freckles in matching positions." Resemblance generated from one source
face holds across shots; two independently-described faces drift apart.

The same production's 3-frame character sheet is a strong human-sheet shape:
Frame 1 face portrait · Frame 2 **ghost-mannequin outfit display** ("garments
hold the natural shape of an invisible body — no head, no hands, no skin
visible") so wardrobe is its own decoupled panel · Frame 3 back view — thin
white dividers, equal frames. (The repo's canonical ghost-mannequin recipe:
`../skills/higgsfield-soul/SKILL.md` § Split-Panel Outfit-Change Sheet.)

### 7. Prop sheets (objects skip the motion test)

Clean studio prop sheets (shoes, bag, moka pot, mug) into GPT Image 2. **No
motion tests** — props are objects, they don't perform; the prop sheet is enough.
Generate-many / test-in-motion / lock applies to *performers*, not props.

Give the prop **multiple views** — front / side / back at minimum, and add a
**BOTTOM / undercarriage view whenever the object will be flipped, tumbled, or
rolled** in the video; the model can't invent an underside it has never seen
[DEMO — Seedance-4K film tutorial, 2026-07]. View-coverage details, plus the
red-arrow annotation trick for props the actor keeps mishandling:
`../skills/higgsfield-gpt-image-2/reference-sheet-workflow.md` § Views the
video will need + § Red-arrow annotation.

### 8. Location plates (3/4 angle, empty by default)

Locations are the third recurring asset next to characters and props — the
tutorial's rule is that **every scene needs all three built before any video
generation** [DEMO]. Two plate disciplines:

- **Ask for a 3/4 angle** — more visible room reads as more depth, which gives
  camera moves somewhere to go (the win-rate bullet above, applied).
- **Generate the plate empty** — no people — whenever the video model should
  own the crowd. A populated plate freezes extras into wallpaper; an empty
  plate lets the model cast and move them. (Two deliberate exceptions: when a
  crowded set must **repeat identically** across many shots, composite the
  crowd once and reuse that populated plate — see
  `../skills/higgsfield-seedance/PRODUCTION-PATTERNS.md` § Field-Harvested
  Patterns → populated-plate reuse; and when the crowd **is** the location
  — a festival, a packed arena — where an empty plate makes every shot prompt
  re-invent the throng. The full test is in
  `../skills/higgsfield-soul/SKILL.md` § Variety Sheets.)
- **Pin the sun before you pick.** A master plate should fix the light — its
  direction, height and quality — so it cannot jump between generations.
  Everything else in the scene inherits from it; a plate with ambiguous light
  hands you a different time of day per take.

**Choosing between plates: judge AFFORDANCE, not beauty.** Generate several
(location batches are the cheapest asset you will make) and reject on staging
grounds first [DEMO — Higgsfield "AI Love Stories" tutorial, 2026-08]. The
reported claim is that **~70% of the final video's quality comes from the
location** — [UNPROVEN HERE] as a number, but the selection discipline behind
it stands on its own, and the rejections are more instructive than the pick:

| Rejected | The actual reason |
|---|---|
| "gorgeous ship, but no room for a crowd and no room for a run" | **the blocking does not fit.** The scene needs a packed pier, a collision and a long sprint; the geometry has to hold all three |
| "no room between the cranes, way too much clutter" | **clutter turns to mush** under generation — busy detail at mid-depth degrades into noise once the frame moves |
| "good layout, but that heavy yellow tint would leak onto every scene" | **the plate's grade is contagious.** A tinted plate is a colour decision applied to the whole sequence, made by accident |
| *the pick:* "long pier — room for the crowd, the crash and the sprint; the sides hold all the mess, leaving the middle clean for the action" | **it has a clean action corridor**, and the clutter is pushed to the edges where it belongs |

Run the scene's beats against the plate before locking it. If a beat has
nowhere to happen, the plate is wrong no matter how good the still looks —
and you will not discover it until you are paying for shots.

Generate location plates in **Soul Cinema** (see § Which model makes the
sheet below); in video prompts a location plate is typically declared
"STYLE REFERENCE ONLY, not a fixed keyframe" —
`../skills/higgsfield-seedance/SKILL.md` § Reference Roles.

### 8b. Reverse-angle plates + master-plate exposure normalization

[FIELD — 13-project harvest] Two location-plate disciplines from production:

- **Reverse-angle plates are first-class elements.** Dialogue coverage that
  holds the 180° line is done with **paired per-angle location elements** —
  one plate per side (`loc_room_v2` + `loc_room_v2_reverse`), each saved and
  `@`-registered separately. The screen-direction lock comes from the plates,
  not from prose.
- **Normalize every plate against a master plate before use.** When a set
  needs multiple plates (desk wall, window wall, reverse), run each through a
  fast image edit against the chosen master: "match the exposure of this
  plate to the master plate — the second reference, same room — keeping
  everything else identical. CHANGE — exposure and light level only."
  Mismatched plate exposure otherwise reads as a lighting change between
  cuts.

### 9. Register the `@`-glossary

**Save every sheet as a Higgsfield Element** — this is what makes the sheet
`@`-referenceable from video prompts at all. Declare every asset once with a
stable `@`-name and register each under **Elements** with the same name so
prompts auto-attach the right images:

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

## Which model makes the sheet

The tutorial's model-hopping ladder [DEMO — Seedance-4K film tutorial,
2026-07], consistent with `../specs/image-model-specs.json`:

1. **GPT Image 2 at 4K resolution** — the default for character and prop
   sheets (resolution `4k`, quality `high` for hero assets).
2. **If the result reads flat / 2D** — rerun the **same prompt, unchanged, in
   Nano Banana Pro** (also up to `4k`). Demonstrated on the tutorial's TV-remote
   prop sheet: GPT Image 2's version looked flat, the identical prompt in Nano
   Banana Pro brought depth and highlights.
3. **Soul Cinema for locations and characters-from-scratch** — the cheapest
   first pass at ~0.125 credits per image; the tutorial's on-screen pricing
   showed **1 credit = 8 images** [DEMO — pricing shown on-screen; verify
   against the current UI before promising it]. Note Soul Cinema tops out at
   `2k` quality — when a sheet must be 4K, finish in GPT Image 2 or Nano
   Banana Pro.

The reason to spend here at all, in the tutorial's words: **"the better the
input image, the sharper the final video."**

## Related

- `../skills/higgsfield-soul/SKILL.md` — character sheets + the anti-slop composite
- `../skills/higgsfield-gpt-image-2/SKILL.md` + `…/reference-sheet-workflow.md` +
  `…/static-ads-workflow.md` — product/prop sheets, location editing
- `../skills/higgsfield-shotlist-director/SKILL.md` — where these locked assets
  feed the connected shotlist
- `../DISCIPLINE.md` — the acceptance-rate philosophy "win rate" is the upstream
  face of
