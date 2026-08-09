---
name: higgsfield-seedance
description: "Rewrites scene descriptions using professional cinematography language, structures prompts with a six-slot formula (camera + subject + action + setting + style + lighting), and diagnoses content filter rejections via a preflight linter. Use whenever the user asks for a Seedance 2.0 / Seedance Pro prompt, describes a scene for Seedance generation, mentions Seedance, reports a Seedance generation failure or flagged prompt, or is burning credits on Seedance regenerations."
user-invocable: true
metadata:
  tags: [higgsfield, seedance, seedance-2.0, seedance-pro, content-filter, prompt, director, flagged]
  version: 1.12.0
  updated: 2026-08-09
  parent: higgsfield
---

# Higgsfield Seedance Director

## QUICK FACTS
*Generated-checked block (scripts/build_index.py verifies anchors). Read the linked sections for full context — these lines are routing aids, not the rules themselves.*
- The filter is an LLM reading full-scene intent, not a keyword blacklist — describe a SCENE, not a subject; fix the voice first [→](#the-filter-model-read-this-first)
- Instant fail (<10s) = filter rejection; delayed fail (>30s) = infra/complexity — never regenerate an instant fail unchanged [→](#instant-fail-vs-delayed-fail-the-diagnostic)
- Six slots, in order: Camera + Subject + Action + Setting + Style + Lighting; missing 3+ slots is where flags come from [→](#the-seedance-prompt-formula)
- Empirical prompt-craft laws: 50–80-word attention sweet spot (front-load the load-bearing element), name a director/lens not "cinematic", "fast" degrades motion, no negative prompts in the body, unidirectional motion chains + named camera endpoint + detail scale follows shot size [→](#prompt-craft-laws)
- Five prompt modes: Reference-Based / Continuation / Expand Shot / Edit Shot / Transformation — pick the mode before writing [→](#seedance-20-prompt-modes)
- [OFFICIAL] block scaffold for production prompts: SCENE CONTEXT → … → POSITIVE LOCKS, distributed style on standalone briefs (connected shotlists glue the compiled Style Prefix verbatim instead), FOV in degrees only, CAMERA block 3rd, cut ladder oner / CUT n / timed / freestyle [→](#official-prompt-architecture-the-block-scaffold)
- [FIELD] 13-project corpus calibration: word length scales with register (218w → 2,059w medians — the 50–80w sweet spot is single-shot-only), video briefs hand-authored (`enhance_prompt` off), Style Prefix = per-project constant compiled into home blocks [→](#field-calibration-the-13-project-production-corpus)
- [FIELD] Three "helpful-instinct" drift sources, each with a standing lock: environment invention (#1, above character drift), character-height equalization, scale drift on wides [→](#positive-locks)
- Build-safe construction for crowds/destruction/creatures: evacuated cities, contained fights ("stays at the sea surface"), the safe benchmark scene [→](#build-safe-construction-crowds-destruction-creatures)
- Extend an existing clip: attach it as a video reference + open with "The scene continues." — match source resolution AND duration; chain cap ~2 (hard 3), then re-anchor from ORIGINAL references [→](#extension-prompting-video-reference-continuation)
- **This file is Seedance 2.0.** For **2.5** — four modes incl. `video_edit` / `video_extension`, 4–30s, 30/10/10 references, in-prompt first-last frames, 720p ceiling — use `../higgsfield-seedance-2-5/SKILL.md`
- Tutorial-demonstrated patterns (reference-role vocabulary incl. VARIETY reference, SCREEN REALISM + duration-match composites, 60:30:10 grade, red-arrow prop annotation): `PRODUCTION-PATTERNS.md` in this directory
- [OFFICIAL] Feature-film pipeline (asset construction, per-scene GEO SPATIAL LAYOUT, the position-fixing first second, dialogue construction, ban dictionary, the 10–15 iteration rule, crowds / giants / thresholds): `HELL-GRIND.md` in this directory
- Performance — objective, obstacle, tactics, beats, subtext, eye life, the acting master profile: `../higgsfield-acting/SKILL.md`
- Hard engine rules (age-blind, exit-frame = cut, off-screen = nonexistent, no reflections, ≤3 tracked characters, double-contrast cuts) + high-risk shot table: `ENGINE-RULES.md` in this directory
- Reference roles: Character / Last-Frame / Environment / Prop — role determines what the prompt may re-describe [→](#reference-roles)
- Working modes: Exploration / Continuation / Bridging / Repair (distinct from prompt modes) [→](#working-modes-vs-prompt-modes-two-taxonomies)
- Layer 1 briefing vs Layer 2 production prompt — never paste Layer 1 into the prompt box [→](#two-layer-prompt-authoring)
- Native **4K** is available in `mode=std` only; `mode=fast` (Seedance 2.0 Fast) caps at 480p/720p — in Cinema Studio the model is still capped at 1080p [→](#pre-flight-linter)
- Always preflight: `python3 scripts/seedance_lint.py --preflight --model seedance_2_0 "<prompt>"` — enums come from `../../specs/model-specs.json` (fast+1080p/4K and Kling 21:9 are auto-caught) [→](#pre-flight-linter)
- 480p drafts validate the prompt, NOT the take — no seed param; pin Hero Frame + start/end frames to carry a look [→](#drafts-validate-the-prompt-not-the-take)
- ZH prompts: hard 1,800-char cap; ZH antislop list enforced by the linter [→](#multi-language-prompt-workarounds)
- Flagged prompt → rewrite playbook per linter rule, then voice pass [→](#the-rewrite-playbook)
- Repeated flags → full loop-breaker procedure + LOG THE OUTCOME (`--confirmed` / `add-quality`) [→](#when-the-user-is-already-in-a-failure-loop)


Use this skill whenever the user wants a Seedance 2.0 / Seedance Pro prompt, OR
whenever a Seedance generation has been blocked, flagged, or silently failed.
This skill's job is to stop credit waste on filter rejections.

> **Engine rules (read with this file):** the hard rendering constraints of the
> Seedance 2.0 engine — age-blind characters, exit-frame = implicit cut,
> off-screen = nonexistent, no reflection shots, ≤3 tracked characters, the
> double-contrast cut rule — live in `ENGINE-RULES.md` in this directory,
> together with the high-risk shot table (reflections, same-character doubles,
> crowds, text rendering) and its mitigations. This SKILL.md is the
> `EN-director` *profile* of that rule core; the `ZH-house` and
> `bilingual-JSON` profiles (`../../docs/Seedance 2 Skill.md`) obey the same
> core. Flag high-risk shot types at authoring time — never silently break a
> rule the project's hero image happens to conflict with.

> **Production patterns (sibling reference):** patterns demonstrated working
> in Higgsfield's own Seedance-4K film tutorial — reference-role vocabulary,
> coordinate blocking, video-reference screen composites, prompted
> imperfection, 60:30:10 grade — live in `PRODUCTION-PATTERNS.md` in this
> directory, labeled `[DEMO]`.

---

## The Filter Model — Read This First

Seedance 2.0's content filter is **not** a keyword blacklist. It is a language
model that reads the full prompt as a single scene and judges intent and context.
Most users burn hours swapping individual words — that loop does not work.

The filter compares two things:

- **A prompt that reads like a filmmaker describing a shot** → tends to pass.
- **A prompt that reads like a note to a friend** → tends to fail.

A word that looks sensitive in isolation can sit inside a well-constructed
cinematic prompt without issue — the filter reads the full picture. A prompt
with no picture to read (no setting, no visual purpose, no narrative logic)
gives the filter nothing to work with, and it errs on the side of caution.

**Practical rule:** the prompt must describe a **scene**, not a **subject**.
Fix the voice first, then fix the words.

---

## Instant Fail vs. Delayed Fail — the Diagnostic

This single heuristic saves time on every failure:

| Failure timing | Meaning | What to do |
|----------------|---------|------------|
| **< 10 seconds** (instant) | Content filter rejection — prompt never reached the GPU | Rewrite for voice + remove risk tokens. Do not regenerate unchanged. |
| **> 30 seconds** (delayed) | Infrastructure, timeout, or complexity — prompt passed the filter but the render failed | Simplify action density, cut length, try again |

If the user is seeing **instant fails in a loop**, it is a filter issue — never
a GPU issue. Stop them from regenerating before the rewrite.

---

## The Seedance Prompt Formula

Every Seedance prompt should hit these six slots, in this order:

```
[Camera movement] + [Subject] + [Action] + [Setting] + [Style] + [Lighting]
```

All six are technically optional — but a prompt that includes all six almost
never gets flagged, because the filter has full context to interpret every
word. A prompt missing 3+ slots is where flags come from.

### Minimum viable Seedance prompt

> **Slow dolly-in on a figure in a dark overcoat standing alone at the end of
> a rain-slick alley. Cold teal shadows, single practical streetlamp, shallow
> depth of field.**

Camera ✓ Subject ✓ Action ✓ Setting ✓ Style ✓ Lighting ✓ — all six slots, ~30
words, passes the filter because the scene is fully legible.

---

## Prompt-Craft Laws

A set of Seedance-2.0-specific prompt rules. These are **empirical** —
practitioner A/B findings that are plausible given the architecture but are
**not** in the official model spec. Treat them as strong heuristics and let the
repo's iteration discipline (`../higgsfield-prompt/SKILL.md` § The Iteration
Rule) confirm them on your own material, rather than as guaranteed model
behavior.

### Length and order — the attention model

Seedance reads the prompt **left-to-right with diminishing attention weight**.
The first sentence carries the most influence; by the third sentence you are in
"detail territory," where the model stops treating elements as primary
instructions and starts sampling them diffusely.

- **Sweet spot: 50–80 words (short-form regime).** A 70-word prompt reliably
  outperforms a structurally identical 200-word version of the same scene —
  more words past ~3 sentences buys diffusion, not control. (Block-scaffold
  production prompts are the other regime: § Official Prompt Architecture.)
- **Structure in three sentences:** ① subject + action, ② camera + style,
  ③ constraints / positive locks.
- **Lead with the single most load-bearing element.** When a shot lives on its
  subject, the subject opens the prompt; when it lives on a camera move, the
  move opens it.

**Relationship to the two length numbers.** This 50–80-word figure is the
*coherence optimum*. The >180-word figure in § Pre-flight Linter is a *different
axis* — the filter/encoder risk ceiling (>220 often hard-fails the text
encoder). 50–80 is where to sit; ~180 is where it starts to break. They don't
conflict.

**Relationship to the six-slot formula.** The six slots guarantee the filter
sees a *complete* scene (presence). The attention model governs *weight* (order
+ length). Keep all six slots present, but the slot list's camera-first ordering
is a completeness checklist, not a mandate to open with the camera word when the
shot's identity is the subject.

### Name the thing — kill empty adjectives

`cinematic`, `epic`, `beautiful`, `high quality`, `amazing` are high-frequency
labels attached to an enormous range of training footage — dark thrillers,
bright rom-coms, nature docs all read as "cinematic" — so the model samples a
broad, diffuse distribution and they move the output toward nothing in
particular. Don't just delete the slop word (Voice Rewrite §6) — **substitute a
named, narrowly-trained referent**:

| Empty adjective | Named substitute (samples a narrow distribution) |
|---|---|
| "cinematic" / "epic look" | a **director**: "Wes Anderson symmetry" (centered framing, pastel) · "Kubrick one-point perspective" (geometric corridors) |
| "cinematic lighting" | a **lighting setup**: "golden-hour backlight, long shadows stretching forward" |
| "beautiful" / "high quality" | a **lens spec**: "anamorphic 2.39:1, lens flare from a practical light source" |

Positive form of `../higgsfield-prompt/SKILL.md` § Anti-Slop Vocabulary.

> **Official override on director names.** Higgsfield's own prompt-writing
> skill forbids director names, signature-work references, and equipment
> model names outright (see § Official Prompt Architecture — the Block
> Scaffold → Measurable-language rules). The director-substitute trick above
> is an empirical short-form fallback; in block-scaffold prompts, describe
> the look in observable terms instead — "centered symmetrical framing,
> pastel palette", not "Wes Anderson symmetry".

### "fast" is the highest-degradation keyword

Combined with complex action or camera movement, `fast` is the single
worst-degrading keyword. The temporal branch already runs multiple high-velocity
calculations when motion is layered; `fast` asks all of them to run at maximum
velocity at once. Two competing fast elements jitter; three compound into error
that's hard to salvage.

**Fix: describe the physics, not the speed.** `feet striking hard, each stride
at full extension, arms pumping at 90 degrees` produces the perception of speed
with no degradation. One element can carry speed — just not all of them
simultaneously. (Same family as Voice Rewrite §3 — describe physics, not
emotion.)

### No negative prompts in the prompt body

Seedance has **no negative-embedding architecture** for the prompt text — every
token is read as a *positive* instruction. `negative: jitter, bent limbs` gets
parsed as scene description the model tries to render (noise), not as a
constraint, and makes the output worse.

Use **positive constraint statements** — direct declarations of what must be
true:

```
Face stable. Limbs anatomically natural. Consistent lighting, no flicker.
Body proportions consistent throughout.
```

**Scope:** this is about the Seedance prompt **body**, and the target is
`negative:` list syntax / bare negation lists — not every "no" token. A short
lock tail inside a positive declaration ("Consistent lighting, no flicker";
the Style Prefix's "Photorealistic — no 3D render") is fine and field-proven
across the harvest corpus. It does **not** override the Higgsfield UI's
dedicated negative-prompt field (which some image models expose and
`../../vocab.md` § Composition Vocabulary uses). The same positive-only
requirement is already documented for Cinema Studio 3.0 in
`../shared/negative-constraints.md`.

### Ambiguous verbs — the homograph trap (v1.10, Peter's find 2026-07-14)

If a word has a plausible second reading, Seedance may take it. The observed
case: *"wind tearing at her coat"* — meant as fabric pulled violently; the
model sometimes reads *tearing* as ripping (fabric shredding) or tearing up
(crying), and the shot changes accordingly. This is not covered by any known
prompt guide — treat it as a first-class law:

**Before a verb ships, ask: is there a second physical thing this word can
look like? If yes, replace it with the phrasing only ONE thing can look like.**

- `wind tearing at her coat` → `wind whipping violently at her coat` /
  `her coat flutters violently in the wind`
- Seed homograph list (grow it whenever a generation misreads a word):
  **tearing** (rip / cry) · **shoot** (fire / film) · **duck** (crouch / bird) ·
  **bolt** (run / lightning / hardware) · **draw** (pull / sketch / weapon) ·
  **wave** (hand / ocean) · **charge** (run at / electricity) · **rock**
  (sway / stone) · **drop** (fall / droplet) · **fire** (flame / shoot /
  dismiss) · **strike** (hit / match / lightning) · **break** (shatter /
  pause / dawn) · **pound** (hammer / heartbeat) · **snap** (break / photo /
  fingers).
- The list is a seed, not the rule — the rule is the self-check, which
  generalizes to any word forever.

### Community v3 cherry-picks (Joey drop, audited 2026-07-14)

Adopted (genuinely absent from this skill until now):

- **Camera on the shadow side, with a stated operator axis.** Place the
  camera on the shadow side of the key light and say where the operator
  stands/moves — light wraps toward the lens and faces keep dimension.
- **Detail-on-wide ("snake cam").** 84° low-angle placed hard against a small
  foreground object — detail-shot intimacy without losing the wide's context.
- **Intimate wide.** 63–84° on a close face instead of a long lens — presence
  without compression; the room stays in the frame.
- **Prompt-reset heuristic.** When iterations are getting *worse*, stop
  stacking fixes: strip the prompt back to subject + action + camera and
  re-add only what's necessary. Density is a bell curve; past the peak you
  can't tell which element the model dropped.
- **Canonical-over-plate.** Every subject keeps its own identity reference
  even when it is visible in the environment plate — the plate carries the
  world, the canonical ref carries identity; never let a plate double as an
  identity source.
- **Contrast curve stated three ways.** When the grade matters, state it as
  tonal curve + specular removal + named grade — one phrasing alone drifts.

Rejected (was: flagged, test day pending): their worldbuilder puts the camera
block at the BOTTOM ("at the top FOV fights identity data") — this contradicts
both this skill's CAMERA-3rd-position rule and their own seedance skill.
**Resolved 2026-07-26 by field evidence instead of a test day** `[FIELD — 13-project
community harvest]`: across ~4,000 harvested production prompts from 9 creators,
the CAMERA block sits mid-document in every final prompt — never at the bottom.
CAMERA-3rd stands; the bottom-position claim is dropped.

### Motion-prompt laws (dramaclaw production corpus, audited 2026-08-09)

`[EMPIRICAL — dramaclaw production corpus, Seedance]` — practitioner findings
earned in dramaclaw's Seedance production work. The craft is model-agnostic
i2v motion-writing rather than a Seedance spec; same epistemic status as the
rest of this section (strong heuristics — confirm on your own material).

- **Unidirectional motion only.** A short action that finishes early leaves
  the model with seconds of clip to fill, and it fills them by **reversing**
  the action — the character walks forward then steps back, leans in then
  pulls away. Chain **2–3 connected actions in the same direction** so the
  motion spends the whole clip; a deliberate there-and-back is **two shots**,
  never one prompt. (Failure face: `FAILURE-MODES.md` § Action-reversal
  fill.)
- **Name the camera endpoint.** A camera move needs a destination, not just
  a name — say **what the frame shows when the move finishes** ("slow
  dolly-in, ending on her hands wrapped around the cup"), not only the
  move's name. A move that runs out of instruction before it runs out of
  clip drifts or reverses — the camera face of the unidirectional law.
- **Detail scale follows shot size.** Close-ups earn micro-detail (fingers
  tightening, a jaw flex); wides earn broad arcs (crossing the courtyard,
  the crowd parting). Cross-matching — micro-detail written into a wide, or
  a broad traversal written into a close-up — is unrenderable at that shot
  size and degrades the whole clip. (Detail *inside* a wide is a
  composition problem, not a prompt-detail problem — see the snake-cam
  cherry-pick above.)

### Already-covered siblings (cross-links, not new rules)

- **Compound camera move** (`dolly in while panning left`) → jitter at the
  transition because the model executes the two vectors in sequence. Use one
  primary move + one texture modifier (`slow dolly in, slightly handheld`). Full
  treatment: `FAILURE-MODES.md` § Multi-motion camera overload.
- **Image-to-video subject drift** → re-describing what's already in the source
  image gives the model two competing inputs for one subject; reconciliation
  introduces drift. Keep an I2V prompt to **motion + camera only**. See
  § Seedance 2.0 Prompt Modes / Reference-Based and
  `../higgsfield-prompt/SKILL.md` (I2V key rule).

---

## Official Prompt Architecture — the Block Scaffold

`[OFFICIAL — Higgsfield prompt-writter.skill, 2026-07]` — Higgsfield ships
its own Seedance 2.0 prompt-writing skill with the Seedance-4K release. This
section is that doctrine, reconciled with the rest of this file. Where the
two disagree, the official rule wins inside block-scaffold prompts; the
empirical rules elsewhere in this skill remain the short-form regime.

**Two regimes, not a contradiction.** The six-slot formula and the
50–80-word sweet spot (§ Prompt-Craft Laws) govern short-form single shots.
The block scaffold is the production regime — multi-shot, reference-heavy,
high-control work — where *structure replaces the word cap*: write densely
where control matters, sparsely where it does not, and say each important
thing once. The pre-flight linter detects this regime automatically (canonical
block labels / shot markers) and suspends the short-form word caps — force it
with `--regime block` if detection misses — while every structural lint rule
(shot counts, beat sums, handle declarations, enum checks) still applies in
full. Likewise, the Voice Rewrite instruction
to put a Style & Mood clause up front is the short-form filter pass — in a
block prompt the filter gets its full scene from SCENE CONTEXT, LOCATION MAP,
and LIGHTING instead, and style is distributed (below).

### Block order

Write blocks in this order, using **only the blocks the shot needs**:

```
SCENE CONTEXT
ACTIVE REFERENCES
LOCATION MAP
FIRST FRAME / BLOCKING
FORMAT MODE
OPTICS
CAMERA
ACTION
PERFORMANCE      (when acting matters)
PHYSICS
LIGHTING
COLOR GRADE      (when the grade is strong / stylized)
WARDROBE         (when costume matters)
AUDIO
STYLE            (technical-style suffix)
OUTPUT SETTINGS  (when format must be pinned)
POSITIVE LOCKS
```

Logic: context and references first, then space and timing, then action and
physics, then descriptive style in its home positions, then a technical
suffix, locks last. A naturalistic single take may drop COLOR GRADE,
WARDROBE, and OUTPUT SETTINGS entirely and fold those notes into LOCATION
MAP / LIGHTING.

### Distributed style — the standalone-block rule

In a **standalone block-scaffold prompt** there is no style-prefix block at
the top; the prompt always opens on SCENE CONTEXT. Each style aspect lives
in the block that governs it: light → LIGHTING; color → COLOR GRADE, or
folded into LOCATION MAP + LIGHTING for a naturalistic look; lens / optical
character → OPTICS; skin realism and acting → PERFORMANCE; format / grain /
fps → the STYLE + OUTPUT SETTINGS suffix just before POSITIVE LOCKS.
Descriptive style sits in the body next to what it describes; technical
style sits as the end suffix; nothing style-related opens the prompt.

**Connected-shotlist carve-out** `[FIELD — 13-project harvest]`: in a
multi-scene shotlist project, the field-proven shape is the opposite — a
per-project compiled **Style Prefix glued verbatim to the top of every scene
prompt** (edit once → changes everywhere), then the scene body. Consistency
across 25 separately-generated scenes outweighs distributed elegance there.
That regime is owned by `../higgsfield-shotlist-director/SKILL.md` § Per-scene
prompt law and `../../templates/seedance/global-style-prefix.md`; this
section governs standalone prompts only.

### FOV anchors + the CAMERA-3rd-position rule

In prompt text, state field of view in **degrees from these discrete
anchors only** — never millimeters, never in-between values (not "23°" —
use 18° or 29°):

| FOV | mm equiv | Use |
|-----|----------|-----|
| 180° | fisheye | spherical distortion — POV, dream-state |
| 107° | 14–16mm | architectural ultra-wide, epic establish |
| 84° | 20–24mm | wide — establish, group blocking |
| 63° | 28–35mm | observational, reportage |
| 47° | 40–50mm | neutral human perspective |
| 29° | 75–85mm | portrait compression, dialogue bust |
| 18° | 100–135mm | close portrait, identity-preserving |
| 12° | 180–200mm | tele-detail — hands, objects |
| 8° | 300–400mm | extreme compression, observation, broadcast |

In a multishot, set FOV per segment and add `"no drift mid-segment"`.

Place the CAMERA block in the **3rd position** of the prompt's core layers
(subject → action → camera → style → constraints). Moved to the end, FOV
gets ignored; moved to the front, it conflicts with identity.

### Measurable-language rules

- **Positive phrasing only** — official confirmation of the empirical
  no-negative-prompts law (§ Prompt-Craft Laws).
- **Speeds in km/h** — "moves at 40 km/h", not "fast" (which is also the
  highest-degradation keyword, § Prompt-Craft Laws).
- **Atmosphere in % / meters** — "fog density 40%", "haze visible at 15
  meters"; build it in steps across shots (20% → 40% → 60%).
- **Giant scale via human-height comparison** — "as tall as four humans
  stacked head to toe", not "huge" or "three meters".
- **Left/right is always from the camera.**
- **Emotion through muscle movement, not labels** — same rule as Voice
  Rewrite §3; the muscle-level extreme is `../higgsfield-facs/SKILL.md`.
- **White balance in Kelvin**, fixed within a scene: 3200K / 4000K / 5600K /
  8500K.
- **Masses and sizes in real units for physics** `[FIELD]` — the PHYSICS
  block writes weights in so gravity reads correctly: `"the spider is 10–12
  centimeters, 50–70 grams — it falls gently; the man is 70–80 kg — the
  drop lands hard."` Material behavior gets the same treatment (`"the liana
  stretches slightly under load and creaks like fibrous wood"`).
- **Causal prop interaction** `[FIELD]` — objects never move on their own;
  every prop event needs a visible physical cause with event order:
  `"the cup tips only from visible sleeve contact"` · `"a button press is a
  full mechanical event — contact, 2–3 mm of travel, click, spring-back;
  the screen lights only AFTER the click."`
- **No director names, signature works, or equipment model names** — they
  get ignored or break complex moves; describe the look instead. (Overrides
  the empirical director-substitute in § Prompt-Craft Laws for this regime.)
- **English prompts only** (for the historical ZH exception, see
  § Multi-Language Prompt Workarounds).

### POSITIVE LOCKS

A **lock** is a short hard fixer placed next to what it protects —
`"headlights stay glowing in every shot"`. The POSITIVE LOCKS block closes
the prompt: continuity (characters, props, environment identical across
cuts) plus a single positive restatement of critical info. This is where the
positive constraint statements from § Prompt-Craft Laws live in a block
prompt.

**Three named "helpful-instinct" drift sources** `[FIELD — 13-project
harvest]` — the model's own instincts, each needing a standing lock:

1. **Environment invention — the #1 drift source, above character drift.**
   Whenever a location reference is attached, the model "helpfully" widens
   rooms and adds furniture it wasn't shown; multiple creators called this
   the single largest source of drift between clips. Standing lock: `"the
   set contains only what the reference shows — no added furniture, rooms,
   or geography beyond the reference"`, plus explicit absences where they
   matter (`"nothing on the floor, nothing on the bed"`).
2. **Character-height equalization.** With two people in frame the model
   drifts toward equal heights. Write real heights into **every** prompt
   with 2+ characters (`"she is 165 cm, he is 178 cm"`) so relative scale
   never floats.
3. **Scale drift on wide shots.** A human anchor shrinks to a speck across
   cuts. Lock it: `"the girl stays the calm human-sized anchor — never
   shrunk to a tiny distant dot."`

### Cut-format ladder

Four precision levels — points on a scale, pick the one the shot needs:

1. **Oner** — `"one continuous shot, the camera does not cut on its own."`
2. **Sequential cuts, no timecodes** — `CUT 1 … CUT 2 … CUT 3`, described in
   order, when cuts matter but exact timing doesn't.
3. **Timed multishot** — explicit cuts at stated seconds
   (`1.0s HARD CUT`), when beats must land on a clock.
4. **Freestyle b-roll** — don't lock cuts; let the model find angles.

Whenever cuts are specified (timed or not), add: `"cuts only at the
specified points, the camera does not cut on its own."` Cut vocabulary:
`HARD CUT`, `SMASH CUT`, `MATCH CUT`, `INSERT CUT`, `REVERSE CUT`,
`WHIP CUT`; fades/crossfades only if explicitly requested. This ladder is
the resolution of the pick-a-side anti-pattern in § Output Format
(per-second labels inside an intended oner read as cut instructions), and
timed beats must still sum to the declared duration (4–15s) per the runtime
arithmetic there.

### Tag naming + minimal reference text

- User-specified tags verbatim; otherwise load-order `@image1 @video1
  @audio1` — consistent with § Reference Roles → Per-Image Role Convention.
- The `@TAG:` reference line = role/build + current state + unique visible
  features + action-critical details + voice (only if it has a line) +
  `"100% matches the reference"`. **No age.** The official skill's own template
  opened this line with an age token; engine rule 1 (`ENGINE-RULES.md`) forbids
  it in either language, and Higgsfield's feature-film brief gives the reason —
  the content filter tightens sharply the moment it reads a minor
  (`HELL-GRIND.md` § Wording rules). Carry the same information through build,
  wear, and posture.
- **Keep reference character text minimal** — long appearance text fights
  the image and degrades it (same mechanism as the I2V subject-drift rule in
  § Prompt-Craft Laws).
- **State critical details in words anyway** — small text, logos, colors —
  even when visible in the reference; the model can drop them.
- **Never place an `@tag` in a shot where that object is not present** — the
  model will force it into frame.

### Context isolation

Every generation is a blank slate with no memory of previous shots. Never
carry in scene numbers, script headings, prior-scene summaries, unused tags
or characters, or "as above / continues" phrasing. This is *why* the
Continuation Prompt Formula (below) demands a verbatim identity re-paste
rather than a reference back to the earlier prompt.

### Special protocols

- **4-mechanism extreme-FOV multishot stack** (8° / 107°): ① sequence-wide
  identity lock (single location reference across all beats), ② LENS LOCK
  opener — explicit FOV phrase starting each beat, ③ LENS CHECK closer
  confirming FOV at the end of each beat, ④ color via material + light, not
  a list. **All four or extreme-FOV multishots break down after 2–3 beats.**
- **Whip-pan needs ≥0.8s of blur travel** — under 0.8s it renders as a hard
  cut without blur (settled → 0.8s WHIP → settled).
- **Mixed real-time / slow-mo:** hard cuts only between speed modes; each
  shot is one speed start to finish.
- **Anti-impact locks** for cracks/breaks: `"crowd PRESSES, not strikes"` ·
  `"fracture originates from edge stress, not center impact"` · `"no impact
  point — pressure-based crack"` · sequential timing edge-to-center, not
  radial from a point.
- **Observation pattern** (hidden-camera effect), all three at once:
  foreground occlusion over 20–30% of frame + atmospheric haze between
  camera and subject + distance vantage at 8–12°. Change the occlusion type
  between beats; keep the vantage single.

For these protocols applied on real footage — per-segment LENS LOCKs, timed
SMASH/MATCH cuts, screen composites — see `PRODUCTION-PATTERNS.md` in this
directory.

### Field calibration — the 13-project production corpus

`[FIELD — community harvest 2026-07-18: 13 shared Higgsfield projects, 9
creators, ~4,000 production prompts pulled via API with full params]`. What
the corpus confirms and calibrates about the block scaffold:

- **The scaffold holds platform-wide.** Every project — photoreal adventure,
  K-drama romance, broadcast-TV drama, anime, stop-motion folklore — runs the
  same Style-Prefix-plus-Constraints-plus-variable-SHOT structure with the
  same block anatomy. "SHOT" markers appear in 95% of the flagship project's
  1,240 Seedance prompts; 15s is the dominant duration (they generate long
  multi-shot clips and cut the best seconds).
- **Word-length ladder by register.** Median Seedance prompt length tracks
  register and ambition, not a fixed cap: tech-demo 218w → broadcast-TV drama
  538w → commercial 779w → genre anthology 955w → adventure film 1,433w
  (p90 2,648) → stop-motion emotional drama 2,059w. The 50–80-word sweet spot
  (§ Prompt-Craft Laws) is *single-shot* doctrine; production multishot briefs
  live an order of magnitude above it. Length scales with performance
  complexity — never truncate a reaction arc to be neat.
- **Register contracts the template.** Photoreal keeps every block (PHYSICS
  with real masses, pore-level PERFORMANCE); stylized work (anime,
  stop-motion) drops PHYSICS/skin realism and keeps SHOT beats + continuity +
  a hard medium lock. See `../higgsfield-style/SKILL.md` § Register Poles.
- **The Style Prefix is a per-project compiled constant.** In connected
  shotlist projects the corpus ships it **verbatim at the top of every scene
  prompt** (the Style-Prefix-plus-Constraints-plus-SHOT structure in the
  first bullet — that is the delivered form, not just an authoring note).
  Standalone block prompts instead *distribute* those aspects into their
  home blocks (§ Distributed style — the standalone-block rule). Which form
  ships is decided by the workflow, not by taste — see
  `../higgsfield-shotlist-director/SKILL.md` § Per-scene prompt law.
- **Video prompts are hand-authored.** `enhance_prompt` was absent/off on
  every harvested Seedance job but ON for 1,022 image jobs — let the enhancer
  expand image prompts, never the video brief.
- **Platform-layer params observed on Seedance jobs** (Higgsfield surface,
  not necessarily the raw model API): `multi_shot_mode: "custom"` (the timed
  multishot mode), `genre: "auto"`, `speedramp: "auto"`, `mode: "std"`,
  `bitrate_mode: "high"`, `generate_audio: true`, 21:9 at 4K.
- **Iteration economics** (TESTS-first culture, 65–100 generations per kept
  shot, five-bucket folder discipline): `../../production-benchmarks.md`
  § Community-corpus anchors.

---

## Seedance 2.0 Prompt Modes

Seedance 2.0 exposes five generation modes that each take the six-slot formula
but apply it to a different starting point. Picking the right mode is upstream of
prompt writing — the same sentence will produce different results in different
modes, because each mode reads the prompt as a different kind of instruction.

### Reference-Based

The prompt builds a scene around a source image that carries the visual identity —
character, wardrobe, palette, sometimes composition. The prompt's job is NOT to
re-describe what the image already shows; it's to place the subject into a new
action, setting, or motion context. This is the workhorse mode for any sequence
that needs a consistent character across varied shots.

```
[Source image role: "as the main character" / "as the starting frame"].
[Action the subject performs]. [Environment and atmosphere if not visible in source].
[Camera movement]. [Lighting cue if different from source].
```

### Continuation

The prompt extends a prior Seedance generation forward in time, picking up at the
final frame of the previous clip. Identity, wardrobe, environment, and emotional
state all carry over. The prompt should describe what happens NEXT — never what
just happened. For the full five-rule construction pattern, see the Continuation
Prompt Formula section directly below.

```
[Continuing from prior clip]. [New action that follows from the last frame].
[Camera direction for the continuation]. [Any state change — light shift, new beat].
```

### Expand Shot

The prompt grows the canvas or spatial extent of an existing frame — pulling the
frame boundaries outward to reveal what's beyond the original edges. This is NOT
a time extension (that's Continuation) and NOT a zoom-out camera move within the
original generation. It rewrites the frame itself to include more scene. Useful
for turning a tight composition into a wider establishing shot without
regenerating from scratch.

```
[Source frame reference]. Extend the scene [direction: outward / upward / leftward].
[What appears in the newly revealed area]. [Preserve the original subject/composition].
```

### Edit Shot

The prompt modifies specific elements of an existing generation while everything
else stays exactly as it was. Think of it as a targeted patch: change a jacket
color, remove a background figure, swap a prop, adjust a facial expression.
Identity, camera, composition, and lighting stay locked unless you explicitly
name them in the change list. The Keep Rule matters here: always state what to
preserve alongside what to change.

```
Change [specific element] to [new state]. Keep [everything else] unchanged.
[Preserve identity, composition, lighting, and camera behavior from the original.]
```

### Transformation

The prompt describes an explicit state change inside a single clip — the subject,
object, or environment visibly becomes something else within the shot's
duration. Distinct from Continuation (which extends time across two clips) and
from Edit Shot (which modifies a generated clip after the fact). Transformation
happens *during* the generation, in one continuous take.

> **Not to be confused with footage transformation (video-to-video).** This
> Transformation *prompt mode* is an in-clip morph generated from scratch. When
> the user starts from a **real clip they already shot** and wants to preserve
> the subject + camera move while adding a VFX element, swapping the world, or
> dropping in a creature, that is the video-to-video workflow in
> `../higgsfield-seedance-vfx/SKILL.md` (`@source` grammar, lock-down clauses,
> lighting integration, std-4K). Use it when the shot's
core idea is the change itself: a character morphing, an object decaying, a
landscape shifting from one season to another. The skeleton below is written
for character → character; the same pattern applies to object → object and
environment → environment with the relevant noun substituted.

```
[Subject in starting state — full identity descriptors]. [Triggering moment or
cue]. [Subject mid-transformation — what visibly changes, in observable
physical terms]. [Subject in ending state — new identity descriptors].
[Camera behavior across the change]. [Lighting / palette shift if any].
```

The transformation must be one continuous arc, not a cut. Describe the
intermediate state explicitly — the model needs a midpoint anchor or it will
either snap from start to end (looks like a cut) or render an ambiguous blur.
Keep the duration short (5–8 seconds is the sweet spot for a single
transformation); longer clips drift.

### Mode Selection Rule

Reference-Based for new action with an existing character. Continuation for the
next beat in time. Expand Shot to widen the frame spatially. Edit Shot to patch
specific details. Transformation prompt mode when the shot's core idea is a
state change inside a single clip — the change is the content. If you find
yourself writing across multiple modes in one prompt — stop, pick one,
generate, then use the output as input to the next mode.

---

## Continuation Prompt Formula

When writing a Continuation mode prompt, apply these five rules. Skipping any of
them is the most common cause of continuation failures: identity drift across the
boundary, re-played actions, environment shifts, and broken emotional through-lines.

### The Five Rules

1. **Last-frame anchor.** Open the prompt with a short description of what the
   camera sees in the final frame of the prior clip — the pose, the position in
   frame, where the character is looking. This tells the model where to start
   rendering from. One sentence is enough.

2. **Identity anchor.** Paste the character's identity block (the same paragraph
   you used in the original prompt) verbatim into the continuation prompt. Do
   not paraphrase it. Do not shorten it. Continuation boundaries are where
   identity drifts — a verbatim re-paste gives the model no room to reinterpret.

3. **Prior clip as secondary memory.** Name what just happened in one line —
   "following the door opening," "after the punch lands," "continuing from her
   turn toward the window." Do not re-describe the action in detail. One
   referential phrase, then move on.

4. **Immediate continuation.** Start the new action on the frame that follows
   the prior clip's final frame. No time skip, no fade, no implied cut — unless
   the user has explicitly asked for one. If they want a skip, describe it as a
   new shot instead.

5. **No action repeat.** The new prompt must extend, not loop. If the prior clip
   ended on her drawing her weapon, the continuation does NOT describe her
   drawing her weapon — it describes what she does with it next. Repeating a
   described action is what causes the "previous beat replays" symptom.

### What Must Carry Over

Across the continuation boundary, preserve: character identity (face, build,
distinguishing marks), wardrobe (every garment and accessory), environment
(architecture, light quality, color treatment, ambient particulates), and
emotional carryover (the state the character was in at the last frame — tense,
exhausted, alert — should still read on their body in the opening of the
continuation).

> For the eight named substrate channels that "emotional carryover"
> decomposes into, see `../../vocab.md` § Emotion as Visible Behavior —
> Channels.

### Example

Prior clip ended on a detective standing in a doorway, rain behind her, glancing
over her shoulder. The continuation prompt:

```
Continuing from the prior clip — the detective framed in the doorway, head
turned, rain behind her. [Identity block verbatim: weathered woman, mid-40s,
short dark hair, charcoal trench coat, leather gloves, tired but alert.]
Following her glance back, she steps fully into the corridor, lets the door
swing shut behind her, and begins walking toward camera. Slow dolly-back
matching her pace. Same cool blue-grey palette, same overhead practical light.
Tense, controlled energy carrying over from the prior clip.
```

All five rules present: last-frame anchor (framed in the doorway, head turned,
rain behind her), identity anchor (bracketed block, verbatim), prior clip as
secondary memory ("following her glance back"), immediate continuation (steps
fully into the corridor — the next frame action), no action repeat (the glance
is referenced, not re-performed).

### Extension Prompting — Video-Reference Continuation

`[EMPIRICAL — cross-surface, verified on Dreamina]` — no Seedance surface
exposes a dedicated "extend" button. The working extension path: attach the
existing clip as a **video reference** (the `video_references` media role)
and open the prompt with **"The scene continues."** The model picks up from
the clip's end and carries motion, characters, environment, even voices. The
five rules above still apply — the attached clip simply replaces the prose
last-frame anchor with the real thing.

- **Prequels:** open with **"Show me what happens before"** instead — the
  model generates the clip leading *into* the source. Past / current /
  future can all be chained around one anchor clip.
- **Match the source clip's resolution AND duration** — 1080p source →
  1080p extension, 15s source → 15s extension (both inside the model's
  4–15s range; 1080p/4k require `mode=std`). A 720p extension of a 1080p
  source shows a visible quality jump at the join. Same family as the
  duration-match rule for screen composites
  (`PRODUCTION-PATTERNS.md` § Video-Reference 1:1 Lock + SCREEN REALISM).
- **Feed the tail, not just the frame** `[FIELD — 13-project harvest]`:
  production practice feeds **the final 3–4 seconds** of the finished take
  back as the `@video` reference rather than a last-frame still — the clip
  carries *motion* into the join, so the next shot picks up the exact pose,
  framing, light, and movement where the previous one left off instead of
  restarting from a frozen pose.
- **Occluded-identity binding:** if an identity feature is hidden at the
  source clip's end (a mole behind a hand), add the character image as a
  second reference and bind it explicitly: `"The woman's identity is
  @Image1."`
- **Chains degrade.** Each extension re-feeds a generation of a generation
  and compounds artifacts. `[FIELD — community, seedance-2.0 repo v6.6.0]`:
  expect visible drift by the 4th–5th chained generation; **cap seamless
  chains at ~2 (hard ceiling 3), then re-anchor from the ORIGINAL canonical
  references** — a scene boundary is an intentional cut re-opened from
  canonical refs, not extension #4. A sequence that must run longer: break
  the chain with a B-roll cutaway between extensions, or upscale before
  re-feeding.
- **Prompt-engineered cut points:** end the extension prompt on a
  camera-angle change (`"the scene from the character's perspective"`) so
  the next join reads as intentional coverage rather than a seam.
- **Source carries state:** the attached clip carries the state; the
  extension text carries only the delta — see the `[FIELD]` addendum under
  § Reference Roles → Load-Bearing Rule before writing the opening line.
- **Extending dialogue:** check the per-language dialogue-sync budget table
  in `../higgsfield-audio/SKILL.md` before writing the next line — reliable
  lip-sync word counts differ sharply by language.

---

## Working Modes vs Prompt Modes — Two Taxonomies

The Seedance 2.0 Prompt Modes section above names five things the
platform exposes: Reference-Based / Continuation / Expand Shot / Edit
Shot / Transformation. These are platform mechanisms — different pathways
through which Seedance accepts a prompt. The Reference Roles and Working
Modes sections below name two adjacent concepts that the platform
vocabulary does not surface:

- **Working modes** — user intent. What you are trying to DO with the
  craft when you sit down to write the prompt.
- **Prompt modes** — platform mechanism. Which of the 5 input pathways
  Seedance accepts the prompt through.
- **Reference roles** — what each reference inside the prompt represents.
  A semantic-role layer, distinct from the input-modality use-case
  patterns catalogued in `../higgsfield-cinema/SKILL.md` § @ Reference
  Patterns for Cinema Studio 3.0 (which lists `@Image1` / `@Video1` /
  `@Audio1` patterns by scenario, not by semantic role).

These three taxonomies are peers, not hierarchical. A single Seedance
shot pulls from all three: a working-mode intent picks a prompt mode;
references inside the prompt play specific roles.

### The "Continuation" Word Collision

"Continuation" names something in both taxonomies:

- **Continuation working mode** = user intent — "I am picking up where
  the previous shot left off."
- **Continuation prompt mode** = platform mechanism — the specific
  Seedance input pathway that extends a prior generation forward in time
  (see the Seedance 2.0 Prompt Modes section above).

A user in Continuation working mode almost always uses Continuation
prompt mode — the intent and the mechanism line up. But Bridging working
mode can also reach for Continuation prompt mode (when the bridge
anchors on the last frame of the upstream shot), and Repair working mode
can reach for Continuation prompt mode (when the repair is a re-shoot
starting from the same last frame as the failed clip). The names
overlap; the meanings don't.

In this skill, section context disambiguates: if the surrounding content
is in the Working Modes section, "Continuation" means the intent; if in
the Seedance 2.0 Prompt Modes section or the Continuation Prompt Formula
section, "Continuation" means the mechanism. If still ambiguous, the
longer forms — "Continuation working mode" and "Continuation prompt
mode" — are always available.

### Working Mode → Prompt Mode Mapping

| Working mode  | Typical prompt mode(s)                | Reference roles in play                |
|---------------|---------------------------------------|----------------------------------------|
| Exploration   | Reference-Based, or pure T2V          | Character (optional)                   |
| Continuation  | Continuation                          | Character + Last-Frame                 |
| Bridging      | Reference-Based or Continuation       | Character + Last-Frame + Environment   |
| Repair        | Edit Shot, or fresh Reference-Based   | Character + (failed-shot reference)    |

Not a strict mapping. One working mode routes through one or more prompt
modes depending on what the shot needs; the table anchors the typical
case without claiming a 1:1 bijection.

---

## Reference Roles

Seedance prompts use references — `@Image`, `@Video`, and `@Audio` — to
lock specific properties across shots. Each reference plays one of four
roles depending on what it locks. This is a semantic-role taxonomy: what
the reference IS FOR in the prompt. It sits alongside (not on top of)
the input-modality use-case patterns in `../higgsfield-cinema/SKILL.md`
§ @ Reference Patterns for Cinema Studio 3.0, which catalogs concrete
prompt patterns by file type.

If a property has to read consistently across multiple shots, assign it
to a reference role. If it only matters for one shot, write it inline.

Three in-prompt role *phrases* demonstrated in Higgsfield's Seedance-4K
tutorial — `"100% matches the reference"` (identity lock), `"STYLE
REFERENCE ONLY"` (environment that the model may extend), and `"VARIETY
reference"` (crowd lineup sheet, the clone-army fix) — are catalogued in
`PRODUCTION-PATTERNS.md` § Reference-Role Vocabulary.

### Character

Locks main-character identity across shots — face, build, distinguishing
marks. Almost always an image reference; for highest consistency, use
the Soul ID character sheet documented in
`../higgsfield-soul/SKILL.md` § Character Sheet Creation.

Pattern in a Seedance prompt:

```
@Image1 as the main character. [Identity block verbatim.] [Action the
subject performs.] ...
```

### Last-Frame

Anchors the start of a new clip to a specific frame from the previous
one. The role tells the model where to begin rendering from. Used in
Continuation prompt mode and inside Bridging working mode. For the full
five-rule construction pattern, see the Continuation Prompt Formula
section above.

Pattern in a Seedance prompt:

```
Continuing from the prior clip — [short description of what the camera
sees in the final frame of the prior clip]. [New action that follows.]
```

### Environment

Locks the world and setting across shots — architecture, light quality,
ambient particulates, weather state. The role tells the model the
specific space the action takes place in, separate from any character
in that space. Pairs with `../higgsfield-cinema/SKILL.md` § Location
Reference Sheets when the same environment recurs across enough shots
to earn a sheet.

Pattern in a Seedance prompt:

```
@Image1 as the environment. [Subject + action.] [Lighting / atmospheric
cues consistent with the environment reference.]
```

### Prop

Locks specific recurring objects — a hero costume piece, a signature
weapon, a branded product, a vehicle that appears across multiple shots.
The role tells the model that this specific object — not a generic
instance of its category — must read identically across cuts.

Pattern in a Seedance prompt:

```
@Image1 as the prop. [Subject interacts with the prop.] [Camera
behavior.] [How the prop appears in the new shot — same geometry and
material as the reference.]
```

### Per-Image Role Convention

Reference handles (`@Image1`, `@Image2`, `@Video1`, `@Audio1`) are
assigned by upload order — the first image attached becomes
`@Image1`, the second becomes `@Image2`, and so on. Production
practice locks a stable role assignment per slot, kept identical
across every prompt in a shot list, so the team and the model both
know which reference carries which property without re-reading the
prompt body.

| Slot       | Role                          |
|------------|-------------------------------|
| `@Image1`  | Character identity            |
| `@Image2`  | Costume                       |
| `@Image3`  | Environment + lighting        |
| `@Image4`  | Composition                   |
| `@Video1`  | Motion only                   |
| `@Video2`  | Camera movement only          |
| `@Audio1`  | Rhythm + atmosphere           |

`@Audio1` is **load-bearing on timing**, not just atmosphere: an uploaded
audio file is a conditioning input that drives cut timing, camera
acceleration, and action pace (beat sync), and a `[AUDIO: Xs]` script block
in the prompt body generates dialogue + SFX + lip-sync. Both, plus the
first-15s extraction trap, are documented in
`../higgsfield-audio/SKILL.md` § Audio as a Conditioning Input. The
temporal-compatibility constraint below (a `@Video1` camera style must not
fight the `@Audio1` rhythm) is the audio case of the Load-Bearing Rule.

The slot order is not model-enforced — it is team-side discipline.
The payoff is reference-stability across long shot lists: once
`@Image1 = character` for the project, that holds for every prompt,
and nobody has to re-check which face the model expects at shot 47.

When a reference conflicts with the prompt text — costume reference
shows red, text says blue — resolve it explicitly in the prompt
body: `@Image2 as costume reference, but recoloured to blue for this
shot`. Don't let an unresolved conflict reach the model.

### Load-Bearing Rule

**References support memory, but text defines action.** The references
in a Seedance prompt carry the persistent properties that read
consistently across shots; the prompt text directs what happens in this
specific generation. References cannot drive new action; text cannot
replace what the references carry. Both layers stay in their lanes.

Sibling formulation of the v3.7.1 camera-side rule ("Prompt wins on
action, reference wins on texture and world feel" — see
`../higgsfield-camera/SKILL.md` § Video Reference — What It Reads, and
What It Can't, § Load-Bearing Rule). Same underlying principle from
different surfaces. The camera-side rule names the WIN order in case of
conflict; the Seedance-side rule names the LANES each side covers.

> `[FIELD — community, seedance-2.0 repo v6.6.0]` **Source carries state.**
> When an accepted clip or final frame is attached as a reference, the
> source carries the state — the prompt text carries only the *delta*.
> Delete opening-state prose that repeats what the attached source already
> shows; when a reference and the text conflict, **references outrank
> text**. One class of state stays in prose regardless: a still frame
> cannot carry open motion vectors, camera-movement phase, or audio phase —
> in-flight motion and timing must be restated in words even when the frame
> is attached. Applied to extensions in § Continuation Prompt Formula →
> Extension Prompting.

The same distinction applies one level up — at the prompt-construction
workflow, not just inside the prompt. When a Seedance clip lands and
you want the next prompt to match its look, screenshot the working
frame and upload it **to Claude, not to Seedance**. Claude needs the
visual to write a prompt that matches the look; Seedance receives the
resulting text prompt and renders the next clip without the screenshot
attached. The screenshot is reference (for the prompt-building model);
the text prompt is action (for the generation model).

---

## Frame Coordinate System

**Frame Coordinate System** locks where subjects, props, and
compositional elements sit inside the frame.

### Qualitative anchors

Standard film-language position language, machine-readable because
it is widely-attested in the training data:

- **Horizontal:** `left third`, `center`, `right third`
- **Vertical:** `upper third`, `lower third` (centered vertically is
  the default and rarely needs naming)
- **Depth:** `foreground`, `midground`, `background`

### Percentage notation

Numeric coordinates for cases where the qualitative anchors are
not specific enough:

- **x-position:** `0%` (far left frame edge) to `100%` (far right
  frame edge)
- **y-position:** `0%` (top of frame) to `100%` (bottom of frame)
- **frame occupancy:** the percentage of the frame area the subject
  fills, useful for shot-size pinning (a tight close-up sits near
  `60-80%` occupancy; a wide establishing has the subject below
  `15%`)

Use percentages when qualitative anchors are under-specified —
e.g., two characters in the same half of frame.

### Pair the two notations

Ship the qualitative anchor and the percentage notation **together
in the same prompt**, not as alternatives. The qualitative term
gives the model the film-language hook; the percentage gives it the
precision target. Example:

```
Character A stands in the right third, x-position 70%, y-position
50%, frame occupancy 25%. Character B stands in the left third,
x-position 25%, y-position 55%, frame occupancy 22%.
```

### Not a mathematical guarantee

Frame coordinates are **a strong compositional anchor, not a
geometric guarantee**. The model treats them as directorial
intent — the same way a DP reads "right third" on a storyboard —
not as pixel-exact targets. Use them alongside the rest of the
standard composition vocabulary (`over-the-shoulder`, `eye line`,
`ground contact`, `headroom`, `nose room`, `crossing rule` — the last
formalized at [vocab.md](../../vocab.md) § Composition Vocabulary →
Crossing rule) rather than as a substitute for it.

When a coordinate drifts in the output, that is the expected behavior
class — the coordinate set the intent; the model rendered to its
best-fit interpretation. Adjust the prompt by tightening the
qualitative anchor or by adding a contact-point clause (`feet on
the marked floor mark`, `right hand resting on the table edge`)
that physically grounds the position rather than re-specifying the
percentage harder.

---

## Spatial Layout Block

A **Spatial Layout Block** is a named structural unit inside a
Seedance prompt that consolidates the spatial-vocabulary fields
from § Frame Coordinate System into a single block the model can
read as one coherent spatial brief. Where Frame Coordinate System
provides the *vocabulary*, the Spatial Layout Block provides the
*structure* for using it.

Scattered spatial directives force the model to reassemble scene
geometry from fragments — and it often picks the wrong reassembly.

### What goes in the block

A complete Spatial Layout Block names, per subject in frame:

- **Identity** — which character/prop/element this is (matches a
  Reference Role handle when references are present)
- **Screen position** — qualitative anchor + percentage notation
  paired per § Frame Coordinate System above
- **Depth layer** — foreground / midground / background
- **Frame occupancy** — % of frame area the subject fills
- **Body orientation** — direction the subject faces (toward
  camera, away, profile-left, profile-right, three-quarter to
  camera)
- **Contact points** — what physical surface or object the subject
  is grounded against (`feet on wet asphalt`, `back pressed against
  the wall`)

Multi-character blocks add the cross-subject relationships:
relative distance, eyeline direction between subjects, screen-left
vs screen-right consistency, whether subjects cross the central
vertical axis, what occludes what.

### When to use a Spatial Layout Block

Three triggers:

1. **More than one subject in frame.** Two-character work is where
   the model most often swaps screen positions or crosses the
   central axis without instruction. A block prevents that.
2. **A specific compositional intent that needs to read across
   shots.** When the same blocking must hold for several beats — a
   character anchored left, another anchored right — the block
   makes the anchor explicit and re-usable.
3. **A failure-mode-prone shot.** Door-entry shots, hallway-direction
   shots, and any shot where the model has been picking the wrong
   spatial reassembly historically all benefit from a block up
   front rather than inline spatial fragments.

Shots with a single subject in a clear position rarely need a full
block; a single qualitative-plus-percentage anchor inside the
Dynamic Description suffices.

### Block-and-prompt fit

The Spatial Layout Block sits **before** the Dynamic Description in
the output format (see § Output Format for Seedance Prompts below).
It primes the model with full geometry; the Dynamic Description
then describes the action that happens inside that geometry.

The block does not replace the six-slot formula — camera, lens,
lighting, and shot timing stay in their respective slots.

---

## Working Modes

Working modes is a user-intent layer above the platform mechanism. It
names what you are trying to DO when you sit down to write a Seedance
prompt — independent of which prompt mode you eventually route through.
See the disambiguation section above for the relationship between
working modes (intent) and prompt modes (mechanism). The mapping table
there shows the typical routes.

### Exploration

Open-ended discovery. No prior shot to anchor on; no constraint to
match. You're generating to find out what the shot wants to be. Short
prompts work here — the model has space to bring its own interpretation.
Typically routes through Reference-Based prompt mode (with a single
character anchor) or pure text-to-video (no references at all).

### Continuation

Picking up where a previous shot left off. The prior clip is the anchor;
the new clip continues from its final frame. Working mode and prompt
mode line up: Continuation working mode almost always routes through
Continuation prompt mode. See the Continuation Prompt Formula section
above for the five-rule construction.

### Bridging

Connecting two existing shots that don't currently flow. The shots
themselves work; the cut between them feels wrong — spatial geography
is unclear, or the emotional energy mismatches, or the camera character
jumps. Bridging uses references from both ends — the last frame of the
upstream shot and the first frame of the downstream shot — to navigate
the middle. Typically routes through Continuation prompt mode (when the
upstream last-frame is the dominant anchor) or Reference-Based (when
both ends carry equal weight). Common reference role configuration:
Character + Last-Frame + Environment.

### Repair

Fixing a failed shot. Distinct from regenerating with a tweaked prompt —
Repair acknowledges that the failed clip is data: it shows you what the
model interpreted wrong, and that interpretation needs to be addressed
directly. Typically routes through Edit Shot prompt mode (when the
failure is local — a wrong jacket color, a missing prop) or a fresh
Reference-Based generation with corrective prompt text (when the failure
is structural — wrong action beat, drifted identity). Pair with the
Iteration Rule in `../higgsfield-prompt/SKILL.md` § The Iteration Rule
when iterating on the corrective prompt.

### Decision Tree — Picking a Working Mode

The mode you reach for is downstream of what you're noticing in your
work. Diagnose by symptom, then pick the mode that fits:

| What you're seeing | Working mode | Why |
|---|---|---|
| Blank page, no anchors yet | Exploration | No prior shot to continue or bridge from; freeform discovery first. |
| Strong shot that needs a follow | Continuation | The shot earned a sequel; pick up where it left off. |
| Two strong shots that don't connect | Bridging | The shots work; the seam between them doesn't. |
| Strong shot but the feeling is weak | Continuation (with role swap) | Re-shoot the same beat with a different reference role carrying the weight — e.g. close-up where the original was wide. |
| Spatial logic feels off mid-sequence | Bridging (with geography clarification) | The sequence needs a beat that re-establishes who is where. |
| Failed shot you keep generating around | Repair | Stop iterating on the prompt. Target the failure directly. |

The decision tree is symptom-first, not mode-first. The mode is the
treatment; the symptom in your work is the diagnostic. If you find
yourself reaching for a mode without naming what symptom drove the
choice, that's a signal to step back.

---

## Two-Layer Prompt Authoring

A skeleton prompt is not meant to be copied blindly into Seedance and
expected to work on its own. A skeleton is a structure — the logic of
the prompt, not the finished prompt. That matters most for the
Bridging, Continuation, and Repair working modes (see § Working Modes
above), because those three tasks depend heavily on context: what
happened before, what must follow, and what exactly the shot is
supposed to solve.

Each practical skeleton in this workflow has two layers, each with a
different audience and a different job.

### The Two-Layer Distinction

- **Layer 1 — task definition / briefing block.** Written for yourself
  or pasted into a ChatGPT-style assistant before the production
  prompt is drafted. Explains the actual problem in plain prose: what
  scene already exists, what the next scene is, what is missing
  between them, what must remain the same, and what the bridge or
  repair must achieve. Layer 1 is the planning step — it forces the
  prompt author to define the problem cleanly before writing the
  model-facing prompt.

- **Layer 2 — production prompt for Seedance.** Shorter, cleaner, more
  execution-oriented. Translates the Layer 1 decision into a
  model-friendly structure: reference roles declared up front,
  preservation clauses, the one action, anti-repeat language, camera
  cue, audio cue. Layer 2 is what gets pasted into the generation
  field.

The distinction makes the workflow practical. Without Layer 1, bridges
fail because the prompt author hasn't decided what the bridge is
supposed to solve; continuations restage instead of continuing because
the prompt author hasn't named what to preserve; repairs over-shoot
because the prompt author hasn't isolated what to change. The two
layers exist to prevent those three failure modes by separating the
planning step from the execution step.

### Bridge Skeleton

The Bridging working mode (see § Working Modes / Bridging above) is
the problem-solving mode — the bridge is not generic cinematic filler.
Use this skeleton when two scene blocks both work but the connection
between them does not.

**Layer 1 — bridge briefing block.** Named fields:

```
Scene A ends with:
[final visible state of upstream scene]

Scene B begins with:
[opening visible state of downstream scene]

The missing thing between them is:
[reaction / movement into a new space / prop action /
emotional beat / spatial clarification]

The bridge must preserve:
[same character, same outfit, same location logic,
same emotional residue, same prop continuity]

The bridge must not do:
[no new subplot, no repeat of previous action,
no extra threat, no random spectacle]

The purpose of the bridge is:
[explain the transition / make the cut readable /
carry emotion / reposition the viewer in space]
```

**Layer 2 — bridge production prompt skeleton.** Reference roles
declared up front, then the bridging clauses:

```
[Reference roles]
@Image1 = character identity reference
@Image2 = continuity start or location anchor (omit if neither is needed)

This is a bridging shot between the previous beat and the next scene.
Its purpose is continuity, not spectacle.

Keep the same character, same outfit, same space logic, same emotional
carryover, and same prop continuity.
Show one readable action that explains the transition.
Do not repeat the previous action beat.
Do not introduce a new threat or subplot.

Scene: [where the character is in this transition moment]
Bridge action: [one small but meaningful movement or reaction]
Camera: [restrained and readable]
Audio: [live sound only if needed]
```

A good bridge often looks "small" compared to an action scene but
does major structural work. If the Layer 2 prompt produces something
that feels too eventful, the Layer 1 briefing's "must not do" clause
was probably too thin — revise the briefing, then re-derive the
production prompt.

### Continuation Skeleton

The Continuation working mode (see § Working Modes / Continuation
above) solves a temporal problem, not a connection problem: the next
clip must begin directly after the previous clip, not as a new
restaging. This skeleton operationalizes the five rules in the
Continuation Prompt Formula section above — specifically rule #5,
"No action repeat."

**Layer 1 — continuation briefing block.** Named fields:

```
The previous clip ends on:
[end pose / camera direction / emotional state /
visible props]

The next clip must begin immediately after that.

Keep:
[identity / body direction / location / emotional
carryover / props]

Change:
[the new beat that begins now]

Do not repeat:
[the previous action phase]
```

**Layer 2 — continuation production prompt skeleton.** Three reference
roles is the typical configuration:

```
[Reference roles]
@Image1 = exact last-frame continuity anchor
@Image2 = character identity reference
@Image3 = optional environment or prop continuity reference

Use @Image1 as the exact continuity start anchor.
Keep the same character, same lighting logic, same spatial continuity,
same emotional carryover.
Start immediately after the final frame.
Do not repeat the previous beat.

Scene: [what remains unchanged]
New action: [what starts now]
Camera: [how the viewer reads the continuation]
Audio: [live sound only if needed]
```

**If the result keeps replaying the previous beat,** the correction is
not "make the prompt longer." The correction is to strengthen the
temporal and anti-repeat language. Useful phrase variants:

- start immediately after the final frame
- do not repeat the previous fight
- do not restage the earlier beat
- continue forward into the new action
- preserve the same fatigue state and emotional carryover

These are interchangeable — pick the variant whose verbs match the
prior clip's content. A continuation following a fight scene wants
"do not repeat the previous fight"; a continuation following a quiet
moment wants "do not restage the earlier beat."

### Repair Skeleton

The Repair working mode (see § Working Modes / Repair above) does not
behave like "generate the scene again, but better." That breaks
continuity and changes too much. The real question is always: what
exactly am I trying to preserve, and what exactly am I trying to
change? A usable repair prompt has two parts that map directly onto
that question — a preservation block and a modification block.

**Layer 1 — repair briefing block.** Named fields:

```
Current clip / image state:
[what already works and must remain stable]

The exact problem:
[what is wrong]

Preserve:
[identity / framing / pacing / space / continuity /
lighting / emotion / prop logic]

Change only:
[one or two specific elements]

Do not damage:
[what tends to drift if the edit is too broad]
```

**Layer 2 — repair production prompt skeleton.** Tight, surgical, no
descriptive ornament:

```
Keep the original framing, pacing, environment, and character
identity.
Preserve the same outfit, same lighting logic, same scene layout,
same emotional state.
Change only [the exact element that needs fixing].
Do not alter the rest of the shot.
```

The "do not damage" field in Layer 1 is the field most often skipped
and most often the source of repair failures. Name the properties
that typically drift when an edit goes too broad — those are the
properties the model needs explicit protection on, even if they
aren't the properties the edit is targeting.

---

## Keyframe Workflow

The most useful official direction on fine-grained Seedance editing
comes from BytePlus VideoPilot — Seedance's official editing-style
interface from ByteDance / BytePlus. VideoPilot frames fine-grained
video editing not as one vague "fix this clip" prompt but as a
**reference + keyframe + local modification** workflow. Three named
ingredients, each with its own job.

This section names what VideoPilot's interface exposes (Capability
Surface), how to translate those primitives into prompt-only Seedance
work when the dedicated UI isn't in play (Translating to Seedance
Prompts), and the underlying mindset that makes the whole approach
work (The Editor-not-Regenerator Mindset).

> **Sourcing:** The keyframe-editing capability surface below is from
> the BytePlus VideoPilot fine-tuning documentation
> (`docs.byteplus.com`) and ByteDance's official Seedance launch
> materials (`seed.bytedance.com`). Same official source set as the
> Rule of 12 citation at
> `../higgsfield-models/MODELS-DEEP-REFERENCE.md:274`.

### Capability Surface

VideoPilot exposes five named editing primitives. These are what the
official UI lets you do; the prompt-side translation in the next
section is the closest equivalent when working through prompts alone.

- **Continuous keyframe segmentation.** VideoPilot parses a reference
  video into continuous keyframe segments. The segmentation is
  done by the system, not assembled by hand. The unit of edit is the
  keyframe, not the whole clip.

- **Fine-grained keyframe edits.** Edits target a single keyframe at
  a time. Surgical at the temporal axis — change one frame's content
  without rewriting any other frame's instruction.

- **Custom keyframes.** The editor can add keyframes the system
  didn't auto-detect. Useful when an important beat falls between
  the auto-segmented keyframes.

- **Partial redraw of selected regions.** Spatial-local edits within
  a keyframe — mask the region, redraw only what is inside the mask.
  Surgical at the spatial axis (vs. the temporal-axis surgery of
  fine-grained keyframe edits).

- **Keyframe description rewrite.** Rewriting the description of one
  keyframe causes the system to regenerate that frame AND its
  transition logic to neighboring keyframes accordingly. This is the
  closest official primitive to Seedance's Edit Shot prompt mode (see
  § Seedance 2.0 Prompt Modes / Edit Shot above).

### Translating to Seedance Prompts

When working through prompts and references rather than the dedicated
VideoPilot keyframe UI, the closest practical equivalent is six
operational rules. None of them guarantee perfect surgical editing
in every interface — they translate the official editing workflow
into prompt-based use.

1. **Use a screenshot or final frame as your stability anchor.**
2. **Keep the identity reference separate from the continuity anchor.**
3. **State exactly what must remain unchanged.**
4. **State exactly what is changing.**
5. **Forbid repetition of the previous beat if this is a continuation.**
6. **If the edit is local, describe only the local change and
   explicitly protect the rest.**

These map onto existing repo surfaces: rules 3, 4, and 6 onto the
Repair Skeleton's preserve / change blocks (see § Two-Layer Prompt
Authoring / Repair Skeleton above); rules 1 and 2 onto the Reference
Roles taxonomy (see § Reference Roles / Last-Frame and § Reference
Roles / Character above); rule 5 onto the Continuation Skeleton's
anti-repeat phrase library (see § Two-Layer Prompt Authoring /
Continuation Skeleton above).

### The Editor-not-Regenerator Mindset

The conceptual root of the whole keyframe workflow surface: if the
goal is surgical edits, think like an editor, not a full
regenerator. Freeze the parts that must remain stable. Isolate the
parts that must change. Then make the instruction local and explicit.

This is also the conceptual root of the Repair Skeleton: the
preserve / change split is the prompt-side enactment of the
editor-not-regenerator stance, the same discipline VideoPilot's UI
primitives express at the interface level.

---

## Pre-flight Linter

Before the user generates, run the prompt through the full preflight:

```
python3 scripts/seedance_lint.py --preflight --model seedance_2_0 "<prompt text>"
```

The linter is in the repo's scripts/ directory (`../../scripts/seedance_lint.py`). `--preflight` chains
three passes into one PASS/WARN/FAIL report:

**1. Filter lint** (always on):

- **Real names** of public figures / celebrities / politicians
- **Brand, IP, franchise names** (Nike, Marvel, Spider-Man, Pokémon, etc.)
- **Raw violence verbs** (fight, attack, kill, shoot, blood, gore, stab)
- **Age markers** (child, kid, young, teen, boy, girl — Seedance is age-blind)
- **Note-to-friend voice** (no Style/Mood, no Camera, no Lighting sections)
- **Overlength** (>180 words is risk territory; >220 words often hard-fails
  on the text encoder, not the filter)
- **Conflicting instructions** (moving + frozen, bright + dark, etc.)

**2. Structural lint** (with `--model <id>`; driven by `../../specs/model-specs.json`,
never guessed) — the expensive failure class:

- Declared shot count ("strictly N shots" / 严格N个镜头) vs actual
  `【镜头N】`/`[Shot N]` block count
- Timed beats (`[0-4s]`) summing past the declared duration / model max
- ZH prompts over the 1,800-character hard cap; ZH antislop phrases
- `@handle` used before its declaration line
- Aspect ratio / resolution / mode / duration outside the model's enum —
  catches Seedance `fast`+1080p (fast cannot output 1080p) and Kling 3.0
  + 21:9 (no native 21:9)

Settings are read from the prompt's own header lines (`**Aspect ratio**: …`,
`Resolution: …`, `mode: …`, `Duration: Ns`); override per-field with
`--ar / --resolution / --mode / --duration`.

**3. Memory recall**: the most relevant past failures from
`../../db/filter-memory.json` / `../../db/quality-memory.json` surface as INFO notes.

Output is `PASS`, `WARN`, or `FAIL` with the specific fix for each rule hit.
Treat `FAIL` as "do not hit generate." Treat `WARN` as "likely to pass, but
here is what to harden." Exit codes: 0 pass/warn, 1 fail, 2 usage — safe to
script.

---

## Drafts Validate the Prompt, Not the Take

The 480p tier is for **prompt iteration**, not take approval. Seedance 2.0
exposes **no seed parameter** (verified — `../../specs/model-specs.yaml`
lists `resolution`, `mode`, `genre` and nothing else), so re-running an
approved 480p draft at 1080p is a **fresh roll**: a new performance, a new
camera micro-trajectory, new timing. "Approve cheap, re-render at quality"
is not a workflow Seedance supports.

| Persists across rolls (prompt-driven — a draft CAN validate it) | Re-rolled fresh every generation (a draft CANNOT validate it) |
|---|---|
| Shot count and structure obedience | Performance — expression, gesture nuance, micro-timing |
| Blocking obedience (positions, directions, entrances/exits) | Camera micro-trajectory within the named move |
| @handle / identity contamination | Beat timing inside the clip |
| Dialogue placement | Fine detail (smoke threads, inscription legibility, reflections) |
| Content-filter pass/fail | |

To carry a look you approved into the final render, use the documented
transfer mechanism: the **Hero Frame** (`../higgsfield-assist/SKILL.md`)
plus **start/end-frame pinning** (start_image / end_image reference roles —
see § Reference Roles above). Pin the frame, not the roll. Fine-detail
judgments must be **re-checked at final resolution** — 480p hides exactly
the detail they're about.

---

## The Rewrite Playbook

When the linter fires, apply the substitutions below. These are drawn from
`../../db/filter-memory.json` — every pattern here has been confirmed
to work on past flagged prompts.

### Real names → archetype description

❌ "Keanu Reeves walking into a boardroom"
✅ "A lean man in his late 50s, dark shoulder-length hair, stubble, intense
  calm expression, in a dark suit, walking into a modern glass boardroom"

### Brand / IP → visual attributes only

❌ "Spider-Man swinging through New York"
✅ "A figure in a red and blue form-fitting suit, masked, swinging between
  skyscrapers on a tensile white line"

❌ "Nike shoes on a running track"
✅ "White athletic shoes with a dark swoosh-free silhouette on a red rubber
  running track"

### Violence → aftermath / tension / physics

❌ "Two people fighting in an alley"
✅ "Two figures locked in a tense physical confrontation, rain-slick alley,
  dramatic low-key lighting, camera shuddering on each impact"

❌ "An explosion destroys the car"
✅ "A burst of orange light and smoke billowing out from the car, metal
  buckling outward, glass fragments catching the light"

❌ "Blood drips from his hands"
✅ "His hands tremble at his sides, something dark staining his cuffs"

### Weapon → prop + purpose

❌ "A man holds a gun to another man's head"
✅ "A standoff in a concrete stairwell — one figure's arm extended, the other
  perfectly still, both silhouettes hard-edged against a single overhead
  fluorescent"

### Horror / dark → atmosphere, not acts

❌ "A monster tears a victim apart"
✅ "The aftermath of something wrong — an empty room, overturned furniture,
  a single smear trailing toward the door, ambient dread, flickering practical
  lamp"

### Build-safe construction — crowds, destruction, creatures

`[OFFICIAL — Higgsfield cinematic-prompt-builder skill, 2026-07]` — don't
describe something risky and hope it passes; build the scene safe from the
start. The substitutions usually read as *more* cinematic, not less: a
standoff is tenser than a massacre, an evacuated city eerier than a crowd in
panic, a roar more powerful than a kill.

| Avoid | Build instead |
|---|---|
| Civilians in panic, crowds fleeing under debris | An **evacuated / empty** city; abandoned streets; one lone figure for scale |
| Weapons firing into buildings / at people | Energy-discharge standoffs, sweeping searchlights, charged auras, shockwaves with no muzzle fire |
| Creatures tearing into each other / gore | A grapple / standoff / near-miss / circling / energy clash — combat **contained** |
| Destruction with people in harm's way | Destruction in **uninhabited terrain** — glaciers, deserts, ruins, open sea, evacuated zones; figures *reacting* to collapsing terrain, never victims |

**Containment doubles as physics.** Give every creature fight a containment
rule — `"the fight stays at the sea surface — breach, dive, grapple,
submerge, never airborne"` · `"boss scale locked at ~2.5 human-heights, not
kaiju-giant"`. The same clause that keeps the scene safe also grounds the
physics and stops scale escalation.

**The safe benchmark scene** — when a scene drifts risky, pull it back
toward this confirmed-passing shape: one original creature (no franchise),
in a generalized monument/amphitheatre location, in daylight, no weapons
present, performing expressive action (rising, roaring, spreading wings) —
expressive rather than violent.

---

## Voice Rewrite — the "Filmmaker not Friend" Pass

Even with every risk token removed, prompts still get flagged if the voice is
wrong. Do this pass on every Seedance prompt:

1. **Add a Style & Mood clause up front.** Palette, lens, lighting, atmosphere.
   Never skip this. It tells the filter "this is a shot."
2. **Name the camera move.** "Slow dolly-in," "low-angle tracking," "static
   medium." Not "the camera moves forward."
3. **Describe physics, not emotion.** "Jaw clenches, nostrils flare" not
   "looks angry." The filter reads physics as cinematic; emotion language as
   ambiguous intent. For the muscle-level extreme of this rule — facial
   expressions as FACS Action Unit codes (AU4+AU5+AU7 for anger) in close-up and
   dialogue — see `../higgsfield-facs/SKILL.md`.
4. **Describe force and direction, not destruction sequence.** "Driven into
   the car, metal buckling" not "thrown into side door, glass shatters, uses
   rebound to sweep leg."
5. **Present tense, active voice.** "She turns" not "she is turning."
6. **Cut the antislop words.** Breathtaking, stunning, epic, masterfully,
   cinematic masterpiece — these signal marketing copy, not a shot description,
   and correlate with flags.

> For the eight named substrate channels that "describe physics, not
> emotion" decomposes into, see `../../vocab.md` § Emotion as Visible
> Behavior — Channels.

---

## Output Format for Seedance Prompts

When generating a Seedance prompt for the user, use this structure. It
mirrors what Seedance's filter reads most cleanly:

```
**Model:** Seedance 2.0
**Aspect ratio:** 16:9   **Duration:** 10s

**Style & Mood:** [palette, lens, lighting, atmosphere — 1 sentence]

**Dynamic Description:** [camera move + subject + action, present tense,
shot-by-shot if multi-cut. This is the main block.]

**Static Description:** [location, props, ambient details — 1-2 sentences]

**Camera:** [exact movement name]
```

For the full bilingual EN+ZH director output format (used in Seedance's
web UI), see the extended reference at `../../docs/Seedance 2 Skill.md`.

### Runtime arithmetic for multi-shot prompts

Runtime appears in three places in a delivered Seedance prompt —
the title line, the meta header (`**Duration:** Xs`), and any
per-shot timing labels in the Dynamic Description. All three must
agree.

For multi-shot prompts, label each shot inline with its time range
(e.g. `Shot 1 (0-3s): ... hard cut to Shot 2 (3-8s): ... hard cut
to Shot 3 (8-15s): ...`). The per-shot labels must *sum* to the
total duration stated in the title and meta header; a drift between
the two surfaces is the most common source of "my multi-shot prompt
rendered as a single shot" failures.

Always ask the user for runtime — never default. A 5s, 10s, or 15s
assumption silently degrades adherence on prompts that needed a
different cap.

### Shot density for multi-scene prompts

When grouping multiple shot rows into a single Seedance prompt
(rather than splitting into separate prompts), use this starting
heuristic: roughly one prompt per 4-5 shot rows. The heuristic is
project-derived empirical observation, not platform-enforced, and
varies wildly by scene type.

Group shot rows into one prompt when ALL of these hold:

- Same character set in frame
- Same location or contiguous subset of a location
- Continuous emotional / temporal unit (no time skip, no major mood
  pivot)
- Combined runtime fits within the 15s Seedance cap
- The grouped prompt text stays within practical generation limits —
  for ZH prompts the 1,800-character hard cap; for EN block prompts
  there is no character analogue (production medians run far longer —
  § Field calibration). The once-circulating "~2,500 characters"
  budget is ZH-derived doctrine, not an EN limit.

Split into separate prompts when any of these fire: hard cut
between locations (e.g. apartment → flashback), major character
entrance or exit changes the handle list, or the combined runtime
exceeds 15s. The fuller production heuristic — five group criteria,
five split triggers, the complexity budget, and the "don't fragment
grief" rule — lives in `../higgsfield-shotlist-director/SKILL.md`
§ Prompt density.

The heuristic is a starting state, not a target. Adjust per project
as you learn how Seedance handles your particular scene-type
density — dense action sequences may want 1 prompt per 2-3 shot
rows; quiet emotional scenes may collapse to 1 prompt per 8+ rows.

### Single-vs-multi-shot decision

Default is single-shot. Reach for multi-shot when the content is
action, dynamic dialogue, or anywhere a cut is itself doing work a
single shot cannot deliver. Everything else holds tighter as a single
continuous shot.

For single-shot continuous motion, per-second beats give fine-grained
control without provoking cuts — `[0-3s] subject enters frame,
[3-7s] camera pushes in`. The bracket-notation reference lives in
`../../vocab.md` § Editing Syntax (shipping in v3.7.7 sub-phase 2f).

For multi-shot, use the Runtime arithmetic above — each cut labeled
with its time range, sum equals total duration. Action scenes earn an
extra layer: per cut, name the participants, location, implements,
and beat-by-beat choreography.

Anti-pattern: per-3-second time labels written inside what was meant
as a single continuous shot. Seedance reads any per-segment timing
block as cut instructions and inserts cuts. Pick a side — if you
want continuity, drop the time markers; if you want cuts, label them
with `Shot 1 / Shot 2 / Shot 3` and the multi-shot arithmetic above.

---

## Post-Clip Decisions

When a generated clip raises questions around itself, testing
becomes narrative work — not "is it good?" but "what does it do?"
and "what comes after?" The diagnostic below asks four scene-function
questions; the decision tree maps the answers to next-shot types.

### The Four Questions

After any strong clip, ask these four in order. They surface what
the clip is doing in the episode and what should come next.

1. What function does this scene have?
2. What is missing for it to feel connected?
3. What shot would make the connection readable?
4. Is the next step continuation, bridge, contrast, or reset?

These questions are scoped to the next move, not to "solving the
whole episode." The narrower scope is what keeps them practical.

### Next-Shot Decision Tree

The right question is not "what is the coolest next shot?" but "what
problem does the episode have right now?" Map the problem to a shot
type:

- **Strong but isolated** → continuation or before/after
- **Two scenes do not connect** → bridge
- **Spatial logic unclear** → geography clarification
- **Structure works but feeling weak** → close-up or reaction insert
- **Something broken** → targeted repair

The next shot is chosen by function, not by excitement.

> Note: "continuation," "bridge," and "targeted repair" here name
> next-shot types decided post-generation. "Continuation," "Bridging,"
> and "Repair" in § Working Modes above name per-clip intent during
> composition — different lifecycle phase, different decision.

---

## When the User Is Already in a Failure Loop

This section handles **filter rejections** — prompts the Seedance
filter blocks before generation. For **render failures** (FPS drift,
NSFW false-positive, keyframe-invention, physics-state drift, spatial-
awareness failures, multi-motion overload), see `FAILURE-MODES.md` in
this directory — sibling catalog with symptom + mechanism + counter
per named failure.

If the user tells you Seedance has flagged them multiple times in a row:

1. **Ask for the exact prompt text that got flagged.** Don't guess.
2. **Run the preflight linter** on that exact text.
3. **Apply the rewrite playbook** for every rule the linter hit.
4. **Do a voice pass** (add Style & Mood, name the camera, present-tense physics).
5. **Log the outcome** to the learning memory so future sessions benefit. These
   are concrete steps, not optional polish — the memory system only learns if
   outcomes actually get written:
   - After a rewrite **passes Seedance's filter in a real generation**, log it
     as a confirmed workaround:
     `python3 scripts/seedance_lint.py --confirmed "<the prompt that passed>"`
   - If you logged a predicted rejection earlier (`--log`) and later learn the
     outcome: `python3 scripts/higgsfield_memory.py update-filter <id> <fixed|workaround|still-blocked>`
   - After a **quality fix** is confirmed (motion, identity, blocking — not a
     filter issue): `python3 scripts/higgsfield_memory.py add-quality '<json entry>'`
     with the original prompt, the failure description, and the improved prompt.
   - For production-specific lessons that shouldn't pollute global memory, add
     `--project <name>` (entries land in `../../db/projects/`).

Do not let the user regenerate the same prompt with one word changed. That
is the loop that wastes hours.

---

## Multi-Language Prompt Workarounds

Seedance prompts default to English. This section documents historical
language-level workarounds for specific Seedance platform states.

### Chinese (as of 2026-05-17)

At Seedance 2.0's launch the model performed better against Chinese
prompts and enforced a hard 3,000-character cap per prompt. English
runs roughly 5-10 characters per word; Chinese runs 1-2. Production
teams used Chinese prompts to compress ~5× more directive content
into the same character budget — the decisive workaround on long
multi-shot prompts that otherwise hit the cap.

The workaround was a launch-window optimization, not a permanent
convention. If a long Seedance prompt keeps hitting the cap and
English compression has been exhausted, the Chinese-density path has
shipped before — verify the cap state in the current Seedance UI
before reaching for it.

---

## Related Skills

- `../higgsfield-seedance-2-5/SKILL.md` — **Seedance 2.5**, the omni-reference
  dialect: four modes (`t2v` / `omni_reference` / `video_edit` /
  `video_extension`), 4–30s, 30/10/10 reference materials, in-prompt first-last
  frames, video editing and forward/backward extension. Caps at 720p — route
  there when the job is long, edit-shaped, or reference-heavy; stay here when it
  needs 4K, a start/end-frame role, or a genre hint
- `../higgsfield-acting/SKILL.md` — the performance layer that fills the
  PERFORMANCE / CHARACTER ACTING block: objective, obstacle, tactics, beats,
  subtext, status, mandatory eye life, the acting master profile
- `HELL-GRIND.md` (this directory) — Higgsfield's open-sourced feature-film
  pipeline: asset construction, the per-scene GEO SPATIAL LAYOUT block, the
  position-fixing first second, dialogue construction, iteration discipline
- `higgsfield-seedance-vfx` — the video-to-video sibling: transform footage the
  user already shot (preserve subject + camera, add a VFX element / swap the
  world / drop a creature / relight to match / sync a timed zoom), std-4K
- `higgsfield-prompt` — MCSLA formula, archetype router, general prompt structure;
  the Iteration Rule and 6-Pass Diagnostic Sequence for when generations are
  off-target and you can't name why
- `higgsfield-troubleshoot` — diagnosis for non-filter failures (render quality, etc.)
- `higgsfield-recall` — pre-generation memory check against past failures
- `../shared/negative-constraints.md` — full negative-constraint reference,
  including the Content Filter / Safety section
- `../../docs/Seedance 2 Skill.md` — extended bilingual director reference
  (archetypes, cut rules, camera language appendix)
