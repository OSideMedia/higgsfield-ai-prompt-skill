# House Rulings — Contested Questions and Where They Were Settled

This library's law for disagreements: **a real tension is recorded, not silently resolved.**
This file is the index. Each entry names the question, the ruling, the scope it holds in, both
sides with the file that carries each and its provenance, and the date. The fixes themselves
live in the source files — every file named below states its own scope and points back here,
so an agent reading either side gets the right answer for its regime.

Three kinds of ruling:

- **SCOPE** — both rules are right, in different regimes. Each file now states its regime and
  cites the other.
- **OPEN — unmeasured** — two sources disagree about the *same* regime and nothing in this repo
  measures it. No winner is picked. A default is given only where one side is clearly the
  cheaper failure, with the reason; the settling probe is named.
- **FIXED** — a plain error (a dangling reference, a wrong syntax, a count gone stale). Listed
  at the end with where it was fixed.

Label meanings (`[OFFICIAL]`, `[FIELD]`, `[EMPIRICAL]`, `[MEASURED]` …): `provenance.md` in this
directory. All entries dated **2026-09-26** unless marked.

---

## P1 — load-bearing

### P1-1 · How much character description goes into each prompt?

- **Ruling:** SCOPE for two regimes, **OPEN — unmeasured** for the third.
- **Scope:** (a) **start frame / I2V** — the image is frame one: motion and camera only, no
  appearance text. (b) **no reference image** carries identity — the full descriptor, word for
  word, in every prompt; it is the only identity the model gets. (c) a character **reference
  attached as identity**, multi-shot — contested.
- **Side A — full descriptor beside the reference, never shortened:**
  `../higgsfield-seedance/HELL-GRIND.md` § The core problem `[OFFICIAL — Hell Grind brief]`.
- **Side B — minimal text beside the reference:** `../higgsfield-seedance/SKILL.md` § Tag naming +
  minimal reference text `[OFFICIAL — Higgsfield prompt-writter.skill]`;
  `../higgsfield-soul/SKILL.md` § Prompt economy `[EMPIRICAL — Joey]`.
- **Not a side on volume:** the Higgsfield Studio breakdowns `[FIELD]` and `negative-constraints.md`
  § Face / Identity Artifacts ("copy-paste the exact character description") back **verbatim**
  wording — which both sides already agree on — not how much of it goes in.
  `../higgsfield-troubleshoot/SKILL.md` § Quick Diagnostic states all three regimes and takes no
  side on (c).
- **Default:** none on *volume* — neither failure is clearly cheaper. Settled on both sides and
  binding everywhere: the identity text is fixed wording from one source, never varied between
  shots, never contradicting the reference; when a character stops matching its reference,
  delete contradicting text first.
- **Settling probe:** one 480p pair, same reference, full descriptor vs `@TAG:` line only,
  three shots each, scored for identity drift.

### P1-2 · How many takes before a failing shot is rewritten, escalated or restructured?

- **Ruling:** SCOPE for most of the ladder; **OPEN** at two points where rungs count the same
  thing. Six numbers, ordered as one ladder in `../higgsfield-troubleshoot/SKILL.md`
  § Stop-Rule Ladder. The earliest tripwire wins; later numbers are ceilings, never quotas.
  (Was labelled SCOPE throughout — "they do not disagree". Relabelled: rungs 1 and 3 overlap in
  v2v, and rung 1's different-flaws escape meets the Retry Ladder's step 2.)
- **Rungs:** 2 same-flaw re-rolls of an unchanged prompt → rewrite (troubleshoot § Take Triage
  `[EMPIRICAL — Emily2040]`) · 3 paid attempts with no declared budget → named options
  (troubleshoot § Retry Ladder `[EMPIRICAL — MiniMax H3]`) · half a declared budget with no
  progress on the same flaw → change strategy (troubleshoot § Attempt budget `[heuristic]`, read
  as `[HOUSE]`) · 4 v2v batches, ceiling → prompt/source fault
  (`../higgsfield-seedance-2-5/VFX-PIPELINE.md` § Stage 5 `[FIELD — AI-vs-VFX]`) · 10–15
  surgical iterations inside a declared budget → simplify the shot
  (`../higgsfield-seedance/HELL-GRIND.md` § The iteration loop `[OFFICIAL — Hell Grind]`) ·
  65–100 generations per kept shot → a planning benchmark, never a stop rule
  (`../../production-benchmarks.md` `[FIELD — 13-project harvest]`).
- **SCOPE:** paid attempts, budget fractions, prompt versions and a project funnel are
  different units. A declared budget (troubleshoot § Attempt budget) replaces the three-attempt
  default with the half-budget tripwire and the 10–15 ceiling — whichever fires first.
- **OPEN — rung 1 vs rung 3 in v2v:** both count same-defect runs of one unchanged prompt +
  source; one says 2, the other stopped at 4. Unmeasured here. **Default:** stop at the first
  repeat — the cheaper failure: at worst one single-variable rewrite of a prompt that was fine
  (revertible, logged), against at worst two more batches bought on a defect that was already
  systematic.
- **OPEN — two failed takes with different flaws:** troubleshoot § Take Triage
  `[EMPIRICAL — Emily2040]` (with `../higgsfield-prompt/SKILL.md` § Before You Iterate) reads them
  as stochastic (batch-and-cull); troubleshoot § Retry Ladder step 2 `[EMPIRICAL — MiniMax H3]`
  reads a second failure as over-packing (split). At n = 2 the ledger verdict is `low-n`. No default on cost — a wasted batch and a needless split are comparable. Tie-break
  `[HOUSE]`, from Before You Iterate's own wording ("with the occasional near-hit"): a near-hit
  on the shot's primary job → batch-and-cull; no near-hit → split.
- **Settling probe:** for the first OPEN point, the ledger — log every v2v batch with its defect
  class, and read how often a same-defect pair at batch 2 recovered by batch 4.

---

## P2 — contradictions

### P2-1 · Chain actions, or start in the state?

- **Ruling:** SCOPE — by what the shot is for.
- **Scope:** a **result** reached through a reversing process (reaches in, pulls out, winds up)
  → start *in* the state; **simple same-direction motion** that must fill the clip → chain 2–3
  connected actions; an **object that must visibly change** → the five-step causal chain.
- **Sides:** `../higgsfield-acting/SKILL.md` § States, not transitions `[OFFICIAL — Hell Grind]`
  · `../higgsfield-seedance/SKILL.md` § Motion-prompt laws + `../higgsfield-seedance/FAILURE-MODES.md`
  § Action-reversal fill `[EMPIRICAL — dramaclaw]` · `../higgsfield-seedance/FAILURE-MODES.md`
  § Mimed manipulation `[EMPIRICAL — nutllwhy]`. Each of the three now states its scope and
  cites the other two.
- **Unmeasured edge:** how many same-direction steps a chain holds before it collapses.

### P2-2 · Voice: paste every time, or once?

- **Ruling:** SCOPE — by model — plus **OPEN** on what "once" means on 2.5, with a default.
- **Scope:** Seedance **2.0**, or any shot where no reused reference carries the voice → the
  voice-bible line verbatim in the audio field each time the character speaks. **2.5** with the
  same character-sheet reference reused → the sheet carries the voice; it goes in the role
  sentence, not the audio field, still copied from the voice bible.
- **Sides (by model):** `../higgsfield-acting/SKILL.md` § Voice + `../higgsfield-seedance/HELL-GRIND.md`
  § The voice is not an asset `[OFFICIAL — Hell Grind]` · `../higgsfield-seedance-2-5/VFX-PIPELINE.md`
  § Direction patterns from the build (the voice lock) `[FIELD — AI-vs-VFX]` +
  `[OFFICIAL — prompt-builder 2.5]`.
- **OPEN — "once" per project or per prompt (2.5):** the voice lock says describe it once
  "rather than re-specifying it in every prompt" — readable as once per *project*. Against
  that, the Dreamina core formula's Audio slot lists "voice characteristics" per prompt
  (`../higgsfield-seedance-2-5/SKILL.md` § The Core Prompt Formula `[OFFICIAL — Dreamina]`), and
  the same build's § Emotion with no video reference writes "how the voice sounds" into the
  prompt at hand. Nothing here measures it.
- **Default `[HOUSE]`:** once per **prompt**, in the role sentence. Each generation reads only its
  own prompt (`../higgsfield-seedance/SKILL.md` § Context isolation); a line pasted from the
  voice bible is the same words the sheet was built to, so it can only fight the sheet if the
  bible and the sheet already disagree — a failure the wording discipline forbids anyway —
  while an omitted line leaves a dialogue shot with no protection if the sheet under-carries
  the voice, and that costs a re-render.
- **Unmeasured edge:** whether also repeating the voice in the 2.5 audio field helps or fights.
- **Settling probe:** one 480p pair on 2.5, same sheet reference, second prompt with vs without
  the role-sentence voice line, voice match scored against the first.

### P2-3 · May an identity asset go through a model a second time?

- **Ruling:** SCOPE + **OPEN** on one point, with a default.
- **Scope:** the **identity base** (the close-up face plate) never takes another full pass —
  changes are masked onto the untouched original. A **derived look frame** (a final still, a
  start frame, a look variant with its own name) may be re-passed (the Studio Look re-pass),
  and is never used as the identity base or as a reference plate.
- **Sides:** `../higgsfield-seedance/HELL-GRIND.md` § Point changes `[OFFICIAL]` +
  `../higgsfield-soul/SKILL.md` § The Untouched Base `[FIELD — ONEIRIC + ADILIADA]` · the one-line
  Nano Banana 2 fix, `../higgsfield-seedance-2-5/VFX-PIPELINE.md` § Stage 1 and
  `../higgsfield-character-design/SKILL.md` § Sheet Construction Laws `[FIELD — AI-vs-VFX]` ·
  `../higgsfield-soul/SKILL.md` § Studio Look re-pass (Mr. Core methodology).
- **OPEN:** whether one full Nano Banana 2 pass alone measurably softens a sheet.
- **Default:** make the point edit with the one-liner, then **mask the changed region back onto
  the original**. The mask costs minutes; a softened base is paid for in every shot that reads it.
- **Siblings pointed at the default:** `../higgsfield-soul/SKILL.md` § Two-Tool Refinement
  Pipeline (GPT Image 2 edits on the anchor sheet — a whole-frame *adjust lighting* has no region
  to mask back, so it belongs on a derived look frame) and `../../templates/ad-asset-prep.md`
  § 3 (erasing the duplicate face in GPT Image 2).

### P2-4 · Film grain on a character sheet?

- **Ruling:** **OPEN — unmeasured**, no default. (A default — drop the grain — was given earlier
  in this release and withdrawn: it rested on "a grain-free plate costs at most some
  uniformity", which weighs one side's risk only.)
- **Sides:** `../higgsfield-soul/SKILL.md` § The Reference Plate — the capture phrase keeps *soft
  natural film grain* as the anti-AI-uniformity signal `[EMPIRICAL — Joey]` ·
  `../higgsfield-seedance/HELL-GRIND.md` § The character sheet — grain baked into the sheet
  travels into every scene and the character stops reacting to new light `[OFFICIAL — Hell
  Grind]`.
- **Why no default:** both failures are inherited by every shot that reads the plate — baked
  grain cannot be removed per shot; an AI-uniform plate (plastic skin) softens every shot alike
  (`../higgsfield-soul/SKILL.md` § The Untouched Base guards that texture). Neither is clearly
  cheaper. Shared by both sides: Axis-1 skin detail fully on ("real skin with visible pores, no
  retouch"). Decide per project, pin it once, never vary it across one character's plates.
- **Settling probe:** one sheet with and without the clause, same scene prompt, grain read on the
  video.

### P2-5 · Scale: a sentence or a size-ref image?

- **Ruling:** SCOPE + **OPEN** at the boundary, with a default.
- **Scope:** vague comparatives ("tiny next to the enormous dragon") hold nowhere. A **true,
  visible body landmark** holds near-human props (`../higgsfield-seedance-2-5/VFX-PIPELINE.md`
  § Stage 2 `[FIELD — RED FLAG]`) and is Hell Grind's stated solution for a thirty-metre giant
  (about 16× a human; "at least five times" is the floor the prompt writes) with the human in
  frame (`../higgsfield-seedance/HELL-GRIND.md` § Solutions born under deadline `[OFFICIAL]` —
  the brief does not say whether a size-ref image was also attached). An extreme ratio **no
  landmark can express** takes the size-ref image
  (`../higgsfield-seedance-2-5/VFX-PIPELINE.md` § Stage 2 `[FIELD — AI-vs-VFX]`).
- **OPEN:** which instrument holds better where both are possible.
- **Default:** stack them when a reference slot is free — the sentence costs nothing, the image
  costs one generation, lost scale costs every wide. The landmark must be arithmetically true.
- **Also fixed:** the absolutes "scale does not survive on words" / "the last thing words can
  fix" / "the fix is an image, not a sentence" (`../higgsfield-seedance-2-5/VFX-PIPELINE.md`
  QUICK FACTS + § Stage 2, `../higgsfield-character-design/SKILL.md` § Sheet Construction Laws)
  now say *vague* words, and the image is scoped to an extreme ratio with no true, visible
  landmark.

### P2-6 · Anamorphic in the video prompt vs baking it into the asset

- **Ruling:** SCOPE — by whether a baked plate exists. (Was recorded OPEN at the Style Prefix;
  relabelled: the bake rule already decides that case and nothing argues the other way.)
- **Scope:** a standalone shot, a t2v shot or a genre recipe has nothing to bake into — the lens
  words in the Look line are the only route (`../higgsfield-recipes/SKILL.md`,
  `../higgsfield-seedance/SKILL.md` § Name the thing, `../../SKILL.md` HARD RULE 7). A sequence
  whose baked plate is attached to **every** shot → the optics words leave the video prompt
  (`../higgsfield-seedance/SKILL.md` § Bake it into the asset `[FIELD — ONEIRIC]`, one studio,
  not measured here) — **including the Style Prefix**, which is pasted verbatim into every
  scene prompt and so *is* the video prompt
  (`../../templates/seedance/global-style-prefix.md`).
- **Why not OPEN:** the harvest prefixes that name a lens
  (`../../templates/seedance/global-style-prefix.md` § Field specimens `[FIELD — 13-project
  harvest]`) never report baked plates — they sit in the first regime and are no second source
  for the second. If a production is found that names the lens over a baked plate *and* reports
  the result, this reopens.

### P2-7 · `NO BGM` or `No music.`?

- **Ruling:** **OPEN — unmeasured** on the token. Settled around it.
- **Settled:** lead with the positive diegetic list. **Default** `[HOUSE]` inference, unmeasured:
  never put the suppression inside the 2.5 `()` music bracket — `()` is the music channel, so
  `(no music)` there is most likely read as a music cue; plain text after the list costs nothing
  (fixed in `../../templates/seedance/omni-reference-2-5.md`).
- **Sides:** `NO BGM` reads as a hard spec — `../higgsfield-audio/SKILL.md` § Suppressing music
  `[EMPIRICAL — Joey cinema-director-v3]` · `No music.` — the form 12 of 13 harvested projects
  shipped, `../../templates/seedance/global-style-prefix.md` `[FIELD]` and
  `../higgsfield-seedance/HELL-GRIND.md`. Both forms are legal; `../higgsfield-seedance-2-5/SKILL.md`
  § Audio and Text now states both.
- **Settling probe:** one 480p pair on a scene that must land silent, scored on whether a bed
  appears.

### P2-8 · Which bans are legitimate under "the words you write are the words you summon"?

- **Ruling:** SCOPE — a test, not a list: **is the model's untouched default already the
  failure?** Lock tails, slow motion in a fight, a music bed, duplicates, copying an audio
  reference's voice, resizing the wrong subject, and the garbage of a baked property all pass.
- **Where:** `negative-constraints.md` § Where a ban is still correct (the table), which now
  covers the bans the old two-item list omitted. `../higgsfield-seedance/FAILURE-MODES.md`
  § Filler-babble on a short dialogue line no longer bans the word *without* — it is a preference inside the law, which
  targets negative lists and bare negations, not every "no" token
  (`../higgsfield-seedance/SKILL.md` § No negative prompts).

### P2-9 · The Style Prefix's "moving from frame one" vs the still first-second wide

- **Ruling:** SCOPE, resting on a `[HOUSE]` reading (unmeasured): "moving" and "always
  reacting" mean **life** (breath, eyes, weight, micro-reactions), not an action beat. The Hell
  Grind wide withholds a scripted action beat and a camera move ("No camera move, no action
  beat"), not life — and not movement already in progress: the brief's own example has REIN
  walking in during that second. "Open mid-action" governs a shot whose job is an **event**;
  the wide's job is **positional lock**. If the model reads the prefix line as action, the
  reading fails and the escape hatch below applies.
- **Sides:** `../../templates/seedance/global-style-prefix.md` `[FIELD]` ·
  `../higgsfield-seedance/HELL-GRIND.md` § The first second is always a wide `[OFFICIAL]` ·
  `../higgsfield-seedance-2-5/VFX-PIPELINE.md` § Direction patterns `[FIELD — AI-vs-VFX]`.
- **Escape hatch:** override the prefix's Composition line for the one prompt that needs the wide.

### P2-10 · Matching camera speed across two shots of one walk — FIXED

The fix wrote a relation ("shot 9 equals shot 10"), which neither separately generated prompt
can see and which § Context isolation forbids. Now: the **same absolute speed, word for word, in
both prompts** — `../higgsfield-seedance/FAILURE-MODES.md` § Walking is the hardest stunt.

### P2-11 · Staging reference — does it move blocking, and can it be a first frame? — FIXED + recorded

- **Recorded:** the Higgsfield Studio breakdowns claim the diagram raises staging-accurate win
  rate "dramatically" `[FIELD]`; the house A/B found orientation tracking at chance (6/12) and no
  bleed (0/18) `[MEASURED — record incomplete]`. What a user is promised follows the measurement
  (`../../templates/seedance/staging-reference.md`, top box).
- **Fixed:** `../higgsfield-seedance/FAILURE-MODES.md` § A fight generated as separate clips
  comes back choppy called it "first-frame geometry"; it is attached **last**, position only — a
  drawing in the first-frame role becomes frame one. `../higgsfield-workspaces/SKILL.md` § Draw
  to Video / Sketch to Video ("the sketch carries composition and blocking") is now scoped to
  that workspace and points here. The house A/B's record is incomplete, so `../../SKILL.md`,
  `../higgsfield-seedance/SKILL.md` and the staging eval now say "one incomplete-record run",
  not "measured safe".

### P2-12 · A top-down map in the shotlist glossary — FIXED

`../higgsfield-shotlist-director/SKILL.md` § The three layers registered a top-down map as an
attachable asset, against `../../templates/seedance/top-down-map.md` (never attach the floor
plan). The glossary entry is now a front-on staging reference, attached last, named by the
staging template's convention (`@staging_[PROJECT]_[scene]_[version]`) with no slot filename
beside it — a file named `image_1` would sit in the character's slot.

### P2-13 · Handles as sentence subjects

- **Ruling:** SCOPE — by model.
- **Scope:** on **2.5** beat prose names the character plus one visible marker, never a handle
  (`../higgsfield-seedance-2-5/SKILL.md` § Reference Roles `[EMPIRICAL — sd25-pe]`); handles live
  in the role map and legends. On **2.0** the house convention leads the acting line with the tag
  (`../higgsfield-acting/SKILL.md` § Scene adaptation, rule 6 — which now states both models).
- **Fixed:** the 2.5 prompt in `../higgsfield-seedance-2-5/VFX-PIPELINE.md` § The empty-frame pause
  and the letter example in `../../templates/seedance/staging-reference.md` now follow the scope.
  Handle *spelling* (`@Image 1` vs named tags): one form per project, never mixed in a prompt.

### P2-14 · Midjourney flags in the staging template — FIXED

`--ar / --style / --stylize / --no` are not parameters of any cataloged image model and ship
`--no` terms as positive tokens (HARD RULE 3). Removed from
`../../templates/seedance/staging-reference.md`; aspect ratio moves to the model's setting.

---

## P3 — smaller contested questions

### P3-1 · Sheet background shade, contact shadow, and the headless figure

- **Ruling:** SCOPE on the shade and the face law; **OPEN** on the contact shadow, with a default.
- **Canonical home:** `../../templates/ad-asset-prep.md` § Design for win rate. The sheet
  surfaces that name a background shade point to it — including, since the v3.38.0 review,
  `../higgsfield-soul/SKILL.md` § Split-Panel Outfit-Change Sheet, `../higgsfield-gpt-image-2/reference-sheet-workflow.md`
  (`#DCDCDC`) and `../higgsfield-cinema/references/reference-sheet-types.md`.
- **Shade:** light to mid neutral grey, one pinned hex per project; three stated mechanisms
  (nothing competes · low edge contrast · a boring sheet keeps reacting to scene light) are
  compatible.
- **OPEN:** "only a soft contact shadow" `[FIELD — harvest]` vs a flat field with no contact
  shadow (`../higgsfield-soul/SKILL.md` § The Reference Plate `[EMPIRICAL]`). Default for a plate
  read as a reference: the flat field — a contact shadow is baked light every shot inherits.
- **Headless figure:** remove every visible full-body face; Hell Grind removes the front head
  only, AI-vs-VFX crops all — both leave one readable face.

### P3-2 · Clothing: GPT Image 2 or Seedream 5.0 Pro?

- **Ruling:** **OPEN — unmeasured**, with a `[HOUSE]` job split as the working reading. The
  AI-vs-VFX build routes "clothing, wardrobe changes, branded garments" to GPT Image 2
  (`../higgsfield-seedance-2-5/VFX-PIPELINE.md` § Stage 1 `[FIELD — AI-vs-VFX]`); one tutorial
  comparison picked Seedream 5.0 Pro for costume **texture and wear** on a from-scratch sheet
  (`../higgsfield-soul/SKILL.md` § Pick the Sheet Model per JOB `[DEMO]`). Neither source splits
  by job. The house reading — **edits** on an existing sheet → GPT Image 2, **texture from
  scratch** → Seedream 5.0 Pro — makes both true but is an inference, and it is labelled as one
  in the source rows (`../higgsfield-seedance-2-5/VFX-PIPELINE.md`, `../../image-models.md`).
  Two productions, no measurement; the method (run the sheet through 2–3 models) stands.

### P3-3 · Tag versioning

- **Ruling:** SCOPE — bump the version of the tag whose **image changed**: a character's state, a
  regenerated plate, a re-drawn diagram. `../higgsfield-seedance/SKILL.md` § Tag naming ·
  `../../templates/seedance/staging-reference.md` § Tag naming.

### P3-4 · The story bible's movement lock vs "rewrite per scene, never paste"

- **Ruling:** SCOPE — the lock fixes the *words* of the signature and is pasted where the
  movement can happen; where it cannot, acting's transform-not-delete rule applies.
  `../higgsfield-character-design/SKILL.md` § Ship the bible · `../higgsfield-acting/SKILL.md`
  § Scene adaptation.

### P3-5 · Scene-engine's Goal / Obstacle / Tactic vs acting's

- **Ruling:** SCOPE — same words, different layer (structure vs playable behaviour). Term map in
  `../higgsfield-scene-engine/SKILL.md` § Same words, different layer; acting's layer table points
  to it.

### P3-6 · Filler-babble's 8+-word floor vs the ~16–20-words-per-15 s sync budget

- **Ruling:** SCOPE — a floor against dead air in one short shot vs a ceiling for reliable
  lip-sync across a clip. The meeting point depends on how the budget is read: `[HOUSE]` reads
  "~16–20 words per ~15 s clip (5–10 per line)" as a **per-clip total with a per-line cap**, and
  on that reading they meet at one 8–10-word line in a 4 s shot. As a **rate** (~1.1–1.3 w/s)
  that line (2–2.5 w/s) would be over budget; the one house run (record incomplete) found 8-
  and 12-word 4 s lines clean — a direction against the rate reading, not proof. When the line
  cannot grow inside the budget, script the silence. `../higgsfield-seedance/FAILURE-MODES.md`
  § Filler-babble (its `[MEASURED]` tag is now marked record-incomplete: no route, no n at ≤6
  words, record held outside this repo) · `../higgsfield-audio/SKILL.md` § Per-language
  dialogue-sync budgets `[EMPIRICAL — community seedance-2.0 repo v6.6.0]` (relabelled from FIELD in audio, seedance and pipeline alike).

---

## FIXED — plain errors

| Error | Fixed in |
|---|---|
| "Two hands … entering from the same sleeve" (anatomically impossible) | `../higgsfield-seedance/FAILURE-MODES.md` § Orphan limbs |
| Unresolvable citation of an outside product's registry entry (`dialogue-no-handle`) | `../higgsfield-seedance/FAILURE-MODES.md` § Truncated action — now cites HELL-GRIND's seam tricks |
| `16:9. 12s.` quoted as prompt text without saying they are parameters | `../higgsfield-seedance/HELL-GRIND.md` § Two extra blocks |
| HELL-GRIND "overrides the `@TAG:` age form" — the form was already removed | `../higgsfield-seedance/HELL-GRIND.md` § Wording rules |
| 3,000–4,000 words called "the top of the register ladder" — it is above it | `../higgsfield-seedance/HELL-GRIND.md` § Wording rules |
| "References are assets only: characters and locations" — props and geometry inputs omitted | `../higgsfield-seedance/HELL-GRIND.md` § Pre-production |
| 2.5 Stage 2 example packs two characters' actions into one stage | `../../templates/seedance/omni-reference-2-5.md` |
| Ultra-long row "chain `video_extension`" vs the 60 s single-chain ceiling | `../higgsfield-seedance-2-5/SKILL.md` § Dreamina-Only |
| "Enforces the same caps" — the platform enforces only 30 images / 50 total | `../higgsfield-seedance-2-5/SKILL.md` § Material budget |
| "No negative-embedding architecture in either version" — unsourced for 2.5 | `../higgsfield-seedance-2-5/SKILL.md` § What carries over |
| "Seven credits buys …" with no verify-live note | `../higgsfield-seedance-2-5/VFX-PIPELINE.md` § Stage 3 |
| VFX-PIPELINE claimed `build_index.py` checks its QUICK FACTS | `../higgsfield-seedance-2-5/VFX-PIPELINE.md` § QUICK FACTS |
| Catchlights listed as the eye-life item after the section said they are not the cure | `../higgsfield-acting/SKILL.md` (QUICK FACTS, profile template, checklist) · `../../templates/seedance/global-style-prefix.md` |
| Dangling § refs: "§ Workspace", a § with no file, a bare `SKILL.md` in a template | `../higgsfield-character-design/SKILL.md` · `../higgsfield-troubleshoot/SKILL.md` § Attempt budget · `../../templates/seedance/omni-reference-2-5.md` |
| Provenance overclaims: "every template here is OFFICIAL", acting's file-wide OFFICIAL header, `[OFFICIAL — SD25-PE]` with no authorship record, six labels for third-party skill material | `provenance.md` + the files it names (MODE-PLAYBOOKS, acting, seedance-2-5 § Provenance, troubleshoot, FAILURE-MODES, soul, scene-engine, character-design, vocab, staging-reference) |
| `FAILURE-MODES.md` barely routed; `staging-reference.md` unreachable from the Seedance skill | `../higgsfield-seedance/SKILL.md` QUICK FACTS, § When the User Is Already in a Failure Loop, § Spatial Layout Block; FAILURE-MODES frontmatter |
