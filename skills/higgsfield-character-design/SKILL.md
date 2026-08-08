---
name: higgsfield-character-design
description: "Pre-production story-and-character development for Higgsfield projects — the upstream layer that decides WHAT to prompt before any model runs. Use when the user wants to build a character, design a world, develop a story or premise, create a character sheet / character bible / story bible, lock a visual style or 'visual DNA', plan a multi-shot narrative with consistent characters, or says things like 'help me design a character', 'build the world', 'I need a backstory', 'make this character consistent across shots', 'develop my film/series concept', or 'I keep getting generic AI characters'. Routes the locked outputs into higgsfield-prompt + the right model. Adapted from Higgsfield's official character-design framework by @vavavinca."
user-invocable: true
metadata:
  tags: [higgsfield, character-design, story, worldbuilding, character-sheet, story-bible, visual-dna, pre-production, consistency, narrative]
  version: 1.1.0
  updated: 2026-07-05
  parent: higgsfield
---

# Higgsfield Character Design — Story Bible

The rest of this skill library answers *"how do I prompt this?"* This skill answers the question upstream of it: *"what am I prompting, and why this and not generic AI slop?"* It is the pre-production layer — premise, world, character, story, and a locked visual style — that you build **before** writing a single generation prompt, then hand off to `higgsfield-prompt` and the model guides.

> **Attribution.** The framework, worksheet structure, and the "world first" method are adapted from Higgsfield's official *Character Design* materials by **@vavavinca**. We reuse the *schemas and method*; all examples here are original. Credit Vinca when sharing.

## QUICK FACTS
*Routing aids — read the linked sections for the actual method.*
- **World first, always.** Lock the world before you cast a character; the world is the gravity that shapes who they have to become [→](#the-method-world-first)
- Six steps, each locks an output you do not revisit: Premise → World → Character → Story Spine → Style Sheet → hand-off [→](#the-method-world-first)
- The flagship artifact is the **9-Question Character Sheet** — thematic role, external/internal goal, psychological/moral need, wound, spark, silhouette, contradiction [→](#step-3-character-9-questions-the-web)
- The strongest anti-slop tool is the **Forbidden List** in the Style Sheet — naming what the world is NOT is often more useful than the palette [→](#step-5-style-sheet-visual-dna-forbidden-list)
- Specificity beats adjectives: if *any* character could say it, it's a stereotype; keep asking **"why?"** until the answer surprises you [→](#anti-generic-drills)
- Fillable worksheets live in `../../templates/character-design/` — hand them to the user or fill them together [→](#templates)
- Construction laws for the sheet as an artifact: **plain grey background** · creature sheets get **two close-ups (mouth open + closed)** · the **face-lock crop** · a **size-ref frame** for scale between two subjects [FIELD] [→](#sheet-construction-laws)
- Once the character **looks** right, don't jump to scenes — run a **screen test**: casting read → role options → playable lines → voice triggers → one audition prompt [EMPIRICAL] [→](#screen-test-audition)
- This skill produces inputs; it does **not** generate. Hand the locked Visual DNA + character sheet to `higgsfield-prompt` [→](#step-6-hand-off-to-generation)

---

## The method: world first

A world is **a system of constraints**. Decide what the world will not let a character do, and you have decided who they have to become. So the order is not negotiable — each step locks an output the later steps depend on, and you don't loop back to relitigate it:

```
1. PREMISE      one arguable sentence, no characters yet
2. WORLD        six dimensions, filled before anyone is cast
3. CHARACTER    9 questions + a relationship web
4. STORY SPINE  10–20 beats, "therefore / but", never "and then"
5. STYLE SHEET  palette + lighting + materials + a FORBIDDEN list (the Visual DNA)
6. HAND OFF     feed the locked sheets into higgsfield-prompt + a model
```

The failure mode this prevents is the common one: open Higgsfield → generate a cool image → realize there's no story or consistency → quit. Build the bible first; the image is the *receipt*, not the recipe.

If the user arrives mid-stream ("I already have a character"), don't force them back to step 1 — locate where they are, check the upstream outputs exist (a character with no world is the usual gap), and fill the missing layer.

---

## Step 1 — Premise

One sentence, **no character names**. It states an arguable claim about people or the world, not a plot. Four fields, then a pressure test (worksheet: `../../templates/character-design/premise.md`).

1. **Theme statement** — a claim, not a logline. *"Belonging is something you build, not something you're owed."*
2. **What it argues** — the testable belief. *"People who wait to be chosen stay invisible."*
3. **The counter-argument** — the opposing truth the story must honor, *or the theme is propaganda.* *"Some people are kept out no matter what they build."*
4. **Emotional promise** — one word + one line. *"Defiance — the thrill of a door forced open."*

**Pressure test (all five):** compresses to ONE sentence (no "and", no semicolon) · contains NO character names · is arguable · has a real counter-argument · names a feeling, not just an event.

---

## Step 2 — World Sheet (six dimensions)

Fill **all six** before casting anyone (worksheet: `../../templates/character-design/world-sheet.md`). Each answer must be specific and must not change when characters arrive.

| Dimension | The question it answers | Original example |
|-----------|-------------------------|------------------|
| **Physical** | Look, sound, smell, climate, geography, architecture | "A tide-city built on stilts; the streets flood twice a day and everyone owns a boat before they own shoes." |
| **Social** | Who has power, how it passes | "Status is measured in dry land. The few who own ground above the tideline never have to row." |
| **Economic** | Currency, what's scarce, what people kill for | "Fresh water is the real currency; salt ruins everything, so sealed jars are inheritance." |
| **Ideological** | What's sacred, shameful, unspoken | "Drowning is shameful — it means you didn't read the water. Nobody says a drowned name aloud." |
| **Historical** | What everyone remembers or has forgotten | "The Great Surge took the old capital a century ago; half the city pretends it's coming back." |
| **Sensory** | The daily textures the body knows | "Rope-burned palms, the green smell of low tide, lantern oil, the constant give of a floor that moves." |

**Done check:** read it aloud — does it sound like *one* world (no contradictions)? Is every answer specific? Will it stay true once characters walk in? Lock it. See also [Hard vs soft worldbuilding](#hard-vs-soft-worldbuilding) for how knowable the rules should be.

---

## Step 3 — Character (9 questions + the web)

### The 9-Question Character Sheet
The framework's flagship artifact (worksheet: `../../templates/character-design/9-question-character-sheet.md`). Header: name, age, world, archetype. Then, in order — vague answers are the enemy; only *this* character should be able to give them:

1. **Thematic role** — what they prove or disprove about the premise. *"That belonging can be built — he builds a crew out of other discards."*
2. **External goal** — a specific, currently-impossible want. *"Buy the deed to a square meter of dry land before the next Surge season."*
3. **Internal goal** — what reaching it would mean about themselves. *"Proof he's worth keeping, not just useful to keep around."*
4. **Psychological need** — the flaw that hurts THEM. *"He treats every kindness as a debt he has to discharge before it's used against him."*
5. **Moral need** — the flaw that hurts OTHERS. *"He recruits people for their use, then can't admit when he's done using them."*
6. **Wound** — the specific past event that taught them the world hurts. *"At nine, watched his mother trade her water ration to a landlord who let her drown anyway."*
7. **Spark** — the specific past event that taught them what to become. *"A stranger pulled him out of the tide and asked his name — the first person who wanted it."*
8. **Silhouette** — what their shape says across a room. *"Always half-crouched at a doorway, weight on the back foot, ready to bolt or bargain."*
9. **Contradiction** — two things that don't match. *"Pretends he travels light. Keeps a waterlogged ledger of everyone who ever did him a favor."*

### The Character Web
Characters reveal themselves in friction, never alone (worksheet: `../../templates/character-design/character-web.md`). Map four spokes around the hero — **Opponent** (the primary opposite), **Ally** (who they lean on), **Mentor** (who taught them), **Foil** (the variation that exposes them). Characters can move *through* roles over the story (a mentor who becomes an opponent is a person; one stuck in a single bubble is a function). Diagnostic: if you can take one spoke away and the hero says the same line in every scene, the web is too thin.

---

## Step 4 — Story Spine

10–20 numbered beats (worksheet: `../../templates/character-design/story-spine.md`). **Beat format:**

```
Beat N: [character] [does / discovers / loses] [thing]. Result: [the next problem].
```

Connect beats with **"therefore"** or **"but"** — never "and then" (that's a list, not a story). Mark the **Midpoint Turn**: which beat flips the premise against the lead. Stop when the premise is proven — don't pad to hit 20.

---

## Step 5 — Style Sheet (Visual DNA + Forbidden List)

Lock the look once, then inject it verbatim into every prompt (worksheet: `../../templates/character-design/style-sheet.md`). Two ways to build it: **(A)** let the model draft it from the World Sheet (the worksheet carries a ready-to-paste prompt), or **(B)** fill it by hand. Six constants:

- **Palette** — 5–7 hex codes (`#1B3A4B`, `#6FA8A0`, …). Inject the hex, don't describe colors in prose.
- **Lighting** — the recurring light logic ("flat overcast noon, warm lantern pools after dark").
- **Materials** — what the world is made of ("wet rope, salt-bleached wood, hammered tin, oilcloth").
- **Juxtaposition** — one familiar + new pairing that fixes the world's identity ("a child's birthday party on a half-sunk rooftop").
- **Age & proportion** — the build/era language for characters.
- **Real-life refs** — 2–3 actors / paintings / films for the look (treat as *look* references, not identity to copy).

**The Forbidden List is the most valuable field** — name what the world is **NOT**. It's often more useful than the palette and it's your strongest anti-slop lever:

> *NO generic flooded-city teal-and-orange. NO neon. NO pristine surfaces — everything is salt-scarred. NO clear blue sky. NO photoreal celebrity faces. NO pure-black shadows; use deep indigo instead.*

This Visual DNA — hex palette + forbidden list — is what gets pasted into prompts to keep a series consistent. See `higgsfield-soul` (Soul HEX) and `higgsfield-style` for how the color lock is applied at generation time.

---

## Step 6 — Hand off to generation

This skill produces inputs; it does not generate. When the bible is locked, route forward:

- **The prompt** → `higgsfield-prompt` (MCSLA structure). Inject the Visual DNA (hex + forbidden list) verbatim, and pull the subject from the character's Silhouette + Contradiction, the action from the relevant Story Spine beat.
- **The model** → `model-guide.md` / `image-models.md`. For a character who recurs across many shots, train a **Soul ID / Soul Cast** identity (`higgsfield-soul`) rather than re-rolling one-offs; for a single hero image that won't reappear, a one-off generation is fine.
- **Multi-shot sequences** → `higgsfield-cinema` (Cinema Studio) for shot-by-shot continuity; the Story Spine beats become the shot list.
- **Generic prompts get generic characters.** A thin prompt ("a young man's portrait, cyberpunk") cannot recover what the sheet would have supplied — the locked sheet is the difference between a function and a person on screen.

---

## Sheet Construction Laws

`[FIELD — AI-vs-VFX, 2026-08-08]` The sections above decide **what** is on the sheet. These
are the construction laws for the sheet as an *artifact* — the flaws they prevent are the
ones you otherwise pay for in every downstream generation that references it.

**Plain grey background, always.** Not a set, not an environment, not a gradient. A sheet
built on a busy background makes the downstream model decide which pixels are the character
and which are the world, and that decision costs re-rolls. Grey is the credit-saver.

**Creature and non-human sheets carry two head close-ups: mouth open and mouth closed.**
A creature detailed enough to be interesting is detailed enough to glitch between
expressions — a jaw that reshapes the skull when it opens. Two close-ups at the same angle,
one closed and one in a full roar, pin both extremes. The canonical layout is three panels:
full body, head closed, head open.

**The face-lock crop.** A three-panel human sheet gives the model three faces to average —
front full-body, back full-body, close-up — and at full-body scale the face is only a few
dozen pixels, so averaging drags identity toward generic. **Crop the heads out of the
full-body panels.** The full-body frames keep doing their real job (build, silhouette,
wardrobe); the close-up becomes the single source of truth for the face.

**Scale between two subjects needs its own asset.** Relative size is the first thing to
drift and the last thing words can fix — "tiny compared to the enormous creature" returns a
different size every generation, and worst on wides. Build a **size-ref frame**: merge the
two character sheets plus a frame whose scale was right into one image showing them
together, write the proportion in human-height comparisons ("wingspan as wide as twenty
humans lying head to toe"), save it as its own named asset, and attach it to every shot
containing both. Add the asymmetry lock — *if scale is uncertain, render the smaller
subject smaller, never larger* — because an undersized subject reads as distance while an
oversized one reads as fake.

**Fix a flawed sheet; don't rebuild it.** A warped logo or a colour cast on an otherwise
good sheet is a one-line edit on the model that holds inputs best (Nano Banana 2), not a
re-prompt: `change the logo to the one in image two`. Re-prompting re-rolls everything that
was already right. Model routing per asset class: `../../image-models.md` § Routing by
Asset Class.

---

## Screen Test / Audition

> **[EMPIRICAL — community workflow]** Adapted from a community casting-director system prompt. It works in the field; it is not a platform guarantee.

The bible tells you who the character *is*; the generated stills tell you they *look* right. Neither tells you how they **move, speak, and react** — and that is what every scene generation you are about to pay for depends on. So before spending on real scenes, run one cheap audition video and watch the character *act*. This is the same thesis as `../../templates/ad-asset-prep.md`'s generate-many → **test-in-motion** → lock-the-winner loop, applied to a person instead of a product: consistent-looking is not the same as castable.

Six steps, in order — the user chooses at step 5; never skip ahead to the final prompt:

1. **Casting read.** Interpret the locked character sheet as casting material, not lore: presence, playable age range, status, inner wound, external mask, likely voice, likely movement. Pull straight from the 9 questions — Silhouette and Contradiction do most of the work here.
2. **Role options (3–6).** Offer contrasting role types the character could be cast as — lead, antagonist, mentor, tragic hero, villain-with-restraint, silent presence… Each option must state **what the audition has to prove** ("can he menace without raising his voice?"). An option with nothing to prove is not an option.
3. **Three audition lines.** Real scene dialogue with subtext, implying an off-camera reader, each playable more than one way. **Not trailer narration, not lore recitation** — if it sounds like a voice-over, it cannot be *acted*.
4. **Three voice triggers.** Each is **≤3 comma-separated qualities** ("authoritative, grief, controlled") — a *how*, never the spoken line itself. The three must contrast with each other, not be synonyms.
5. **The user picks** one role + one line + one trigger (blending is allowed — the blend still obeys ≤3 qualities).
6. **One final audition prompt, under 3500 characters.** Build a playable scene, not a showcase:
   - **Simple setting** — the audition room, not the movie: one location, no spectacle competing with the face.
   - **Camera:** MCU or locked-off eye-level, shallow depth of field. The frame holds still so the *performance* is what moves.
   - **Acting spine:** objective, obstacle, tactic, emotional shift, and the subtext under the line.
   - **Reaction beats and silence** — write the listening, not just the speaking.
   - **At least one expressive vocal moment** (a stutter, a vocal crack, a whispered threat, a controlled shout) and **subtle physical acting** (blinks, gaze shifts, jaw tension) — muscle, not emotion labels.
   - **Unresolved ending** — cut the take before the moment closes; resolution reads as trailer, open tension reads as acting.
   - Finish with film grain + realistic skin, so you judge a performance, not a render.

**Divergence rule:** if the user comes back and picks a *different role type*, rebuild the acting logic from scratch — new objective, new tactics, new beat pattern. A mentor read is not a villain read with softer adjectives; the same beats reworded is the audition-room version of slop.

### Worked mini-example (the tide-city fixer from Step 3)

- **Casting read:** late 20s reading older; low status wearing borrowed confidence; mask of the indispensable broker over a wound of being kept only while useful; voice quick and transactional, dropping register when cornered; moves like his Silhouette — half-crouched at doorways, weight on the back foot.
- **Role option — villain-with-restraint.** Must prove: he can threaten someone *while doing them a favor*, without ever raising his voice.
- **Audition line:** *"You've still got both your water jars. That's not luck — that's me. So sit down, and let me tell you the second half of the favor."* (Playable warm or menacing; the off-camera reader is whoever owes him.)
- **Voice trigger:** `quiet, transactional, barely controlled`.

### Direct the takes, then lock the winner

- **Facial direction:** for muscle-level control of the audition takes (the jaw tension, the asymmetric almost-smile), hand the beats to `../higgsfield-facs/SKILL.md` — AU codes, not emotion labels.
- **After the audition:** when a take proves the character is castable, lock that winner's identity with `../higgsfield-soul/SKILL.md` (Soul ID / Soul Cast) so every real scene starts from the version that can act — the lock-the-winner step of the `../../templates/ad-asset-prep.md` loop.

---

## Anti-generic drills

Three fast tests for killing slop, usable at any step:

- **Always Ask Why.** Repeat "why?" until the answer surprises *you*. "He's guarded." Why? "He was betrayed." Why does that still run him? "Because the one who betrayed him also taught him everything." A stereotype is any line *any* character could say; yours is the line only this one could.
- **One Wound, Two Characters.** The same wound produces opposite people. "Abandoned as a child" → one runs toward every relationship and clings; another refuses to need anyone. Pick the *less* obvious reaction.
- **Eyes Wide Shut / Silhouette test.** Can you recognize the character from shape alone, with no face? If the silhouette doesn't read (warrior / mystic / rogue), the design is generic — fix it before generating.

---

## Hard vs soft worldbuilding

How knowable should the world's rules be? Decide with three questions (worksheet note in `world-sheet.md`):

1. Does the story depend on the audience *mastering* the rules? Yes → **hard** (rules are explicit and consistent, e.g. heist/system stories).
2. Do you want the audience feeling smart or feeling *wonder*? Smart → hard; wonder → **soft**.
3. Are you willing to leave things unexplained? Yes → soft (mystery preserved, e.g. fable/dream logic).

Hard worlds reward consistency in your prompts (repeat the same physical rules); soft worlds reward atmosphere over explanation. This choice changes how literal your World Sheet's Physical/Historical dimensions should be at generation time.

---

## Templates

Fillable worksheets in `../../templates/character-design/` (hand them to the user or fill collaboratively):

| Worksheet | Step |
|-----------|------|
| `premise.md` | 1 — theme + counter-argument + pressure test |
| `world-sheet.md` | 2 — six dimensions + hard/soft check |
| `9-question-character-sheet.md` | 3 — the flagship character schema |
| `character-web.md` | 3 — Opponent / Ally / Mentor / Foil map |
| `story-spine.md` | 4 — beats + midpoint turn |
| `style-sheet.md` | 5 — Visual DNA + Forbidden List (+ AI-draft prompt) |

---

## Related skills
- `higgsfield-prompt` — turns the locked sheet into an MCSLA generation prompt (the primary hand-off)
- `higgsfield-soul` — Soul ID / Soul Cast for recurring-character consistency; Soul HEX for the palette lock
- `higgsfield-cinema` — Cinema Studio multi-shot sequences; Story Spine → shot list
- `higgsfield-style` — applying the Visual DNA / forbidden list at generation time
- `model-guide.md` · `image-models.md` — picking the model for the character/scene
