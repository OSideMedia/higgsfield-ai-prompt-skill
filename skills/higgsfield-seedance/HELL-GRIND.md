# Hell Grind — the Feature-Film Pipeline

`[OFFICIAL — Higgsfield "Hell Grind" open-source brief]` — Higgsfield open-sourced the
production system behind their **95-minute AI feature film**, including the CINEDANCE prompt
skill it ships with. This file is the part of that system the repo did not already have.

**What this file is not.** The CINEDANCE prompt doctrine — block scaffold, FOV degrees,
optics decision tree, positive locks, cut vocabulary, context isolation, tag naming — is
already the `[OFFICIAL]` doctrine in `SKILL.md` § Official Prompt Architecture, harvested
from the same source family. It is not restated here. Neither are the engine rules
(`ENGINE-RULES.md`) or the tutorial patterns (`PRODUCTION-PATTERNS.md`).

What *is* here is the layer above the prompt: how the assets are built before anything is
generated, how a scene's geography is locked across every shot in it, how dialogue is
constructed, and how the iteration loop is run so a shot converges instead of burning
credits. Every rule in the source brief exists because a shot failed without it.

> **Read with:** `SKILL.md` (the prompt grammar), `ENGINE-RULES.md` (the hard constraints),
> `../higgsfield-acting/SKILL.md` (the performance layer this pipeline assumes), and
> `../../templates/seedance/global-style-prefix.md` (the Style Prefix this pipeline glues to
> every prompt).

---

## The core problem: the model has no memory

A video model remembers nothing between generations. If a character is not fully described
in *every* prompt, the next shot gives them a different face and a different jacket. Every
technique below is a consequence of that single fact.

**Describe everything, every time.** The descriptor goes into every prompt **word for word,
never shortened.** Consistency is not a setting; it is repetition.

---

## Pre-production: assets

An **asset** is a pair: **text + image**. The text is a full description — the *descriptor* —
that is pasted verbatim into every prompt. The image is the reference the model anchors to.
Neither works alone.

References are **assets only**: characters and locations. Everything else is prompt text.

### The character sheet is three images — and one of them has no head

| Panel | Content |
|---|---|
| 1 | Close-up of the face |
| 2 | Full body, front — **headless** |
| 3 | Full body, back |

**Why the front figure loses its head.** On wide shots the model kept sourcing the face from
the small full-body figure on the sheet, where the face is tiny and blurry. Remove that head
and the model has exactly one place to take the face from: the close-up. This sounds absurd
and it fixed a whole class of broken shots.

**Keep the sheet deliberately boring.** Neutral grey background, flat light, real skin with
visible pores, no retouch. The cinema look lives in the locations and the video prompts — bake
film grain and a cinematic lens into the sheet and the character carries that look into every
scene and stops reacting to new light.

**Sheets read best with a large portrait in 3/4 view** — face turned slightly, not straight-on.

> Complements `../higgsfield-soul/SKILL.md` § Character Sheet Creation (the Soul-ID route to
> the same goal) and `../../templates/ad-asset-prep.md` (asset prep generally). The headless
> front panel and the boring-on-purpose rule are the Hell Grind additions.

### Point changes go on with masks, never with a second full pass

Clothes, scars, and blood are **point changes**. Make the change on the original sheet in Nano
Banana Pro or Seedream, then bring it back onto the original **by hand, with a mask** in any
graphics editor: the mask places only the changed part — the jacket, the scar, the blood — on
top of the original, and everything else stays untouched.

**The rule that protects quality: an image never runs through a model twice in full.** Every
extra pass destroys texture and drifts color. After two passes the face turns symmetrical,
plastic, and lifeless — and that dead texture later damages the character's *acting* in video.
The model makes the point edit; the final is always assembled with masks on top of the
original.

### The voice is not an asset — it is a locked descriptor

Seedance holds three or four voices per character inside one tonality. That is enough for a
feature film **only if the voice is managed**.

Lock every character's voice in pre-production, before any dialogue is written, right in the
descriptor: **register, tempo, accent, manner.** It is pasted into the audio field as-is,
every time that character speaks, and it never changes.

```
Voice: deep, gravelly bass-baritone; slow, calculated pacing; London street accent;
menacing calm — he never raises his voice.
```

**Stress-test the voice between generations the same way you stress-test the look.** If it
drifts between shots, go back and lock it harder. Do not "keep shooting."

### The acting is locked the same way as the look and the voice

Every character gets one behavior paragraph written before any shooting — movement, hands,
habits, nervous gestures, eye behavior, and exactly how they break under pressure. That
paragraph is the source of truth; each scene adapts it to the moment's posture and action,
but the core never changes.

**A behavior that is physically impossible in a scene is transferred, not deleted.** A
character who paces the room, sat down on a sofa, does not calm down — the same energy moves
into swaying, finger-tapping, and jagged gestures.

Full system: `../higgsfield-acting/SKILL.md`.

### Location sheets

- **Shoot the location sheet in 3/4, not frontal.** A frontal "pretty picture" becomes flat
  wallpaper on wides, and past its edges the model invents new surroundings every time. A 3/4
  view gives the model depth to read — it places characters correctly and covers close to a
  full circle of angles.
- **Leave an anchor in every location** — a column, a lamp, a sofa — and tie the staging to it.
  "The character at the lamp, facing the door" works. "The character in the room" is a lottery.
- **Keep one light logic**: one source, one direction of shadows, never two suns. Otherwise
  every new angle re-invents the lighting.
- **Reverse angles, route 1:** generate a corner of the same room in GPT Image 2 or Nano
  Banana, matching the soft focus of the original.
- **Reverse angles, route 2** (found late in production): generate a **video of the empty
  location** where the camera slowly walks through the space — Seedance draws the other sides
  consistently with the sheet. Screenshot the angle you need, take it to Seedream or Nano
  Banana Pro, and prompt a texture/lighting improvement. A full location sheet out of a single
  image.

### Name the role of every reference — and ban location inheritance

The model decides for itself if you do not, and it decides wrong: it copies the composition
instead of the face, or the face instead of the color palette.

```
@roco for character reference
@jaxx for character reference
@loc_cave_front for location reference — take only the space and the texture: raw concrete,
black rock walls. Do not use as a starting frame, do not inherit the composition, the angle,
or the grade.
```

**Location references get an explicit ban on inheritance.** This is the Environment role in
`SKILL.md` § Reference Roles, stated in the model's own working vocabulary.

**One dictionary of names for the whole project.** All assets live under tags — `@roco`,
`@loc_cave_front` — and the same tags are used everywhere: in documents, in prompts, in the
interface.

---

## The GEO SPATIAL LAYOUT block

**The most expensive problem in early takes:** characters teleport, swap places, and the
camera jumps to the wrong side. The reason is simple — the model does not remember who stood
where in the previous shot.

The cure is a **floor plan of the place in a few lines**: landmark objects, what is on the
right, what is on the left, where the camera stands. **No characters, no action — only the
place itself.** Write it once per scene and paste it into every shot of that scene *without
changes*. The model gets the same room in every shot, and there is nowhere left to lose the
people.

```
GEO SPATIAL LAYOUT (locked across every shot — pure spatial map):
— PLATFORM = raised circular ritual stone disc at the edge of a cliff.
— ALTAR-MONOLITH: at the cliff edge, MID-RIGHT position relative to the platform.
— RITUAL CENTER: CENTER-LEFT, ~3 m from the altar.
— 180° AXIS: camera ALWAYS stays on the corpse-field side — it NEVER crosses the line.
— BACK-LIGHTING: crimson horizon glow comes from BEHIND the platform, rim-lighting
  silhouettes from camera's perspective.
```

Rules for reading and writing the map:

- **GEO is only the map.** The *look* of the place still comes from the location asset — its
  descriptor and reference go into the prompt next to the map.
- **Sides exist only from the camera.** "frame-left" and "frame-right" — the model does not
  understand "to the left of the character."
- **Positions are set from landmarks and in metres** — "at the altar", "three metres away".
- **State which side the camera stands on and which line it never crosses.** This keeps every
  cut on one axis.
- **After every cut, name again who stands where and where they look.** The model does not
  remember the previous shot.
- **Give a static dialogue a corner of the room, not the whole room.** The less space the
  model has, the less choice it has about where to put the characters.

> **Relationship to the Spatial Layout Block** (`SKILL.md` § Spatial Layout Block): that block
> is per-shot and *includes the people* — screen position, occupancy, orientation, contact
> points. GEO is per-**scene**, excludes the people, and is pasted unchanged across every shot
> in the scene. Use both: GEO fixes the room, the Spatial Layout Block fixes who is standing
> in it this shot.

---

## The first second is always a wide

One second at the start of a scene, **no lines and no action**: the model "photographs" the
arrangement — who stands where, what lies where, where the light comes from — and holds it
through every following shot. Remove that second and characters start swapping places.

Two refinements from production:

- **The "hm" trick.** Have someone say one short word — "hm" — during that second. It makes it
  easier for Seedance to treat the wide as a separate shot.
- **The wide does not have to be silent.** If the shot answers the previous one, feed the
  **tail of the previous clip's line** into that first second — the actor then answers the
  right thing in the right tone, and the two clips glue at the seam.

```
FIRST FRAME AND SPATIAL BLOCKING
SHOT 1 (~1.0s) — a wide that FIXES THE POSITIONS and does nothing else: ROCO planted at the
center of the mat, five smashed mannequins at CENTER-RIGHT, the door open at frame-LEFT with
JAX and REIN one step inside it, trays in hand. No camera move, no action beat.

AUDIO
Over that first second, the tail of the previous clip's line arrives on REIN's lips as she
walks in: "...I've got the coordinates." ROCO's eyes find her before his head turns.

ACTION TIMING
1.0s onward — ROCO answers into the same rhythm, dry and worn: "You're late."
```

> This is a *deliberate exception* to the Non-Empty Opening Frame pattern in
> `PRODUCTION-PATTERNS.md`, not a contradiction of it. That rule bans an **empty** opening
> frame — a frame with nobody in it while the model "arrives". The Hell Grind wide is
> **fully populated from frame one**; what it withholds is *action*, for exactly one second,
> to buy positional lock across the whole scene.

---

## The character-count header

The SCENE CONTEXT block opens with a count header, not a description:

```
EXACT 3 CHARACTERS — NO DUPLICATES: ROCO, JAX, REIN.
```

**This is not a formality.** The model loves to add extra people and to clone furniture. Only
those whose references are in the prompt exist in the frame — and repeated set dressing gets a
direct ban with a count:

```
Exactly ONE mannequin, NEVER render a second one.
FIVE smashed mannequins, never re-rendered as intact, never multiplied. Two trays, never more.
```

Counted objects belong in POSITIVE LOCKS, phrased as what **is** in the frame.

---

## Two extra blocks in the skeleton

The Hell Grind skeleton is `SKILL.md` § Block order plus three blocks it names explicitly:

| Block | Contents |
|---|---|
| **CHARACTER ACTING** | Per character: emotional state · what they want in this moment · what they are hiding · dominant body rhythm · visible habits in this beat · what changes across the shot |
| **STYLE** | The Style Prefix, pasted word for word (`../../templates/seedance/global-style-prefix.md`) |
| **QUALITY** | Detail and stability requirements — "8K detail, pore-level skin, no jitter, no flicker; the faces stay exactly their references at every distance" |

CHARACTER ACTING is the PERFORMANCE block's production form. Worked example:

```
CHARACTER ACTING
ROCO — emotional state: burnt out and still going. What he wants in this moment: one more
clean hit before anyone walks in on him failing. What he is hiding: that the arm is winning,
and that it frightens him. Dominant body rhythm: heavy, planted, slow recovery between bursts.
Visible habits in this beat: the jaw set-and-release, the right shoulder pulled low by the
crystal, the blood he does not wipe, the gaze that finds the broken mannequins first and
people second. What changes across the shot: the second the door opens he re-arms his face —
the exhaustion folds back behind a dry half-smile before he says a word.
```

**The closing technical tag tail.** Production prompts end on a short tag row after the Style
Prefix:

```
Photoreal. NON-IP. 16:9. 12s. SFX only. NO CGI. Cinematic.
```

`SFX only. No music.` is treated as mandatory in this pipeline — music belongs to
post-production, and a generated soundtrack only gets in the way of the edit. (A *project*
choice, consistent with the harvest corpus's 12-of-13 music ban; see
`../../templates/seedance/global-style-prefix.md` § Field specimens.)

---

## Wording rules

- **Present tense. Short sentences.**
- **The camera is written inside the action**, not as a separate aesthetic paragraph.
- **Keep each beat light: up to three sentences per beat.** Overload a beat and the model
  smears it.
- **Length is not the enemy — an overloaded beat is.** Hell Grind's prompts ran **3,000–4,000
  words**. This sits at the top of the harvest corpus's register ladder (`SKILL.md` § Field
  calibration) and confirms it: structure replaces the word cap in the block-scaffold regime.
- **Actions only in positive form.** The model ignores "does NOT fall on his back" — or does
  the opposite. Write "falls on his stomach."
- **The character is in frame from the first frame, and never looks into the camera** unless
  you ask for it.
- **Never write age, in any language.** The content filter becomes markedly stricter the
  moment it reads a minor. Give the **role, the clothes, the action** instead. This is the
  production reason behind engine rule 1 (`ENGINE-RULES.md`) — and it **overrides** the
  `@TAG:` line's `age + role/build` form in `SKILL.md` § Tag naming: write role and build,
  drop the age.
- **Keep a ban dictionary** of words the model punishes, and grow it as you find them:

| Instead of | Write |
|---|---|
| dark | low key |
| jolting | rapid motion |

  Same mechanism as the homograph trap in `SKILL.md` § Ambiguous verbs — a word the model
  reads as something other than what you meant. Log the substitution when you find one, the
  same way you log a homograph.

---

## Dialogue construction

**A dialogue line in the prompt is always built the same way:**

```
The voice and its emotion → the line in quotes → the physical action → the facial reaction
```

- **Lines live only in the audio section.** Not one word of speech inside the action block.
- **Seedance adds its own "uhms", chuckles, and whole phrases**, so the prompt carries a hard
  block: everyone speaks **only** the line in quotes; whoever has no line stays completely
  silent; a "half-laugh" written in the action is a facial expression, **with no sound**.
  `[HOUSE — the rest of this bullet is ours, not the brief's]` "Stays silent" settles the
  *sound*; the **picture** needs its own fact, so every other visible face also carries a
  positive at-rest mouth state — "lips at rest", "jaw closed, listening" — an unmarked mouth
  in frame being one the model may decide is talking. The risk direction is the **short**
  line: one that ends well before the shot does leaves audio air the model fills with
  invented mumble (`FAILURE-MODES.md` § Filler-babble on a short dialogue line — measured at
  ≤6 words on a 4-second shot; the at-rest mouth fact itself is not yet live-fired here).
- **Write the mix too**: voices clean and close to the microphone, ambience under them,
  ambience dips when someone speaks.
- **Rare names get a transcription**, or the model breaks them.
- **Two seam tricks:** on the wide shots of a dialogue, feed the tail of the previous line into
  the prompt — it helps the lips and the rhythm; and **open every new generation with the line
  that closed the previous one**, so the emotion crosses the seam together with the text.

Worked example — the action lives in the timing block, the speech lives in the audio block,
and the two never mix:

```
ACTION TIMING
0.0–3.0s — JAX and REIN walk the corridor toward the lens, in step. JAX talks with his eyes up
on the ceiling lights, one hand patting his stomach; REIN's thumb keeps scrolling the tablet,
her pace unchanged, she never looks up at him.
3.0–4.0s — the distant THUD from the training room lands: REIN's thumb STOPS on the glass, and
only then her head turns to the door — the interrupted work is the accent of the beat. JAX's
grin drops half a second later.

AUDIO
Diegetic only — corridor air, two sets of footsteps on concrete, soft taps on the tablet, the
distant THUD and a hiss of crystal behind the door. JAX voice (verbatim): "A London street
voice, loose and hungry, always half-joking, sentences thrown out mid-stride." His line, and
nothing else: "Man, some cereal and a milkshake would hit the spot right now." REIN voice
(verbatim): "A technical voice — flat, fast, precise, no wasted air." Her line, and nothing
else: "I think I've got the coordinates." Nobody else speaks; JAX's amused breath is a facial
expression, with no sound. No music.
```

---

## Physics, not adjectives

On emotion words — "sad", "angry", "shocked" — the model improvises and returns something
shallow. For deeper emotion, describe the **work of muscles and body**: a tremble, a jaw
clenched with rage and flexing, cheekbones drawn tight, a light exhale through the nose.

Four additions that live in the timing block:

- **INNER (unspoken).** One line of inner monologue per stretch of action — what the character
  thinks and wants — marked `INNER (unspoken)` so it is never voiced.
- **Phased blinking.** "one lazy blink → a quick DOUBLE-BLINK → one HARD reset-blink" — the
  cheapest sign of a living face.
- **A clear gaze direction, or darting eyes.** Constantly working micro-expressions give the
  face life; a fixed stare reads dead.
- **The micro-life rule.** Against frozen faces in static shots: **one visible micro-event
  every one or two seconds** — the breath lifts the chest, a nostril moves, a brow tenses and
  relaxes.

**Describe stillness as held tension, never as a freeze.** Calming phrases like "nobody moves"
freeze the frame themselves.

Worked example — the words "exhausted" and "angry" appear nowhere; the state is built out of
muscle in the timing and out of intention in the acting block:

```
ACTION TIMING
0.0–2.0s — ROCO holds the center of the mat, feet planted wide, chest pumping in short shallow
pulls; the crystal arm hangs heavy at his side and drags his right shoulder a finger lower
than the left.
2.0–4.5s — the jaw sets and releases twice; a thread of blood runs from his nose to his upper
lip and he lets it run; one lazy blink, a quick DOUBLE-BLINK, one HARD reset-blink.
4.5–6.0s — the gaze drops to the smashed mannequins at CENTER-RIGHT, holds one beat, then
lifts to the door as it opens — the eyes reach the door before the head turns.
```

Three more that separate a living shot from a dead one:

1. **The reaction starts before the other line ends.** A listener gets the point mid-sentence
   and their face already answers. After an important event, give the character a fraction of a
   second to take it in before speaking.
2. **Emotion does not switch off instantly.** After a heavy moment the breath is still uneven,
   the hands still unsteady — that tail carries into the next clip and stitches the cuts.
3. **Keep the hands busy.** A character does not "have a conversation" — they fix, count, pour,
   and talk over it. **The strongest accent of a scene is the moment they stop that work**
   because of what they just heard.

Muscle-level control beyond this: `../higgsfield-facs/SKILL.md`. The craft layer:
`../higgsfield-acting/SKILL.md`.

---

## The iteration loop

Generate in **batches, scene by scene**.

- **Every iteration is surgical: one line changes, everything else stays word for word.** A
  prompt is a working mechanism — rewrite it fully and you lose the parts that worked.
- **Everything goes into the log**: prompt version, what changed, verdict. Without the log you
  cannot repeat a good shot. (`../higgsfield-recall/SKILL.md` is this repo's ledger; log the
  outcome there.)
- **The ten-to-fifteen rule.** If a shot has not come together in 10–15 iterations, **the
  problem is not the wording.** Simplify the *shot*: split it in two, remove an action, change
  the angle.

> Consistent with the iteration economics in `../../production-benchmarks.md` (65–100
> generations per kept shot across a project) — the 10–15 rule governs a *single prompt's*
> convergence before it must be restructured, not the project's total take count.

---

## Solutions born under deadline

- **Complex action never sits in the middle of the timing.** A door that would not break — the
  character shuffled next to it and froze. The fix: **the action opens the prompt** — "he is
  ALREADY mid-swing, the door ALREADY cracking" — and the approach to the door becomes a
  separate shot. (The production form of the states-not-transitions rule; see
  `../higgsfield-acting/SKILL.md` § States, not transitions.)
- **A crowd is one "character" asset** with a range of heights and clothes. One or two lead
  extras get their own assets for close-ups. On medium shots, **state the number directly** —
  "20+" — otherwise the model gives you three people in one take and a hundred in the next.
  (Pairs with the VARIETY reference pattern in `PRODUCTION-PATTERNS.md` and the ≤3-tracked-
  characters engine rule.)
- **Transitions between two spaces hold on a threshold.** Both location assets in one prompt,
  and the seam is a doorway with a **light contrast across it** — "a warm amber room, a cold
  blue corridor beyond the arch." The contrast explains the palette change and forgives small
  geometry mistakes.
- **Giants live on scale anchors.** A size comparison in every prompt, **plus a human figure in
  frame to measure against**. Without both, the model quietly shrinks the giant back toward
  human height. State the failure condition too:

```
POSITIVE CONSTRAINTS
THE SCALE LAW — VISIBLE PROOF IN THE PICTURE: the stone guardian stands THIRTY METRES tall —
his head is lost in the darkness of the dome, his open palm is as wide as a family car, and
ROCO at his foot reaches just above the ankle. In every frame the guardian's silhouette is at
least FIVE TIMES the height of the human figure beside him, and the frame cannot hold both his
feet and his head at once. A guardian that reads as a large man, or fits comfortably in frame
next to a standing human = failed shot.
```

  This is the concrete form of the human-height-comparison rule in `SKILL.md` § Measurable-
  language rules — with two additions: the human anchor must be **in the frame**, and the
  prompt names what a **failed** shot looks like.

---

## The five rules, compressed

1. **Assets first.** Do not generate a single shot until every character, location, and prop is
   locked and stress-tested. This one rule saves more money than everything else combined.
2. **Describe everything, every time.** The model has no memory. The descriptor goes into every
   prompt, word for word, never shortened.
3. **Change one thing at a time.** Rewrite a prompt fully and you lose the parts that worked.
   One line per iteration, everything into the log.
4. **Give the model less freedom.** A corner instead of a room, an anchor instead of an open
   space, a map instead of guesswork, one action per shot.
5. **If a shot will not come together — simplify the shot, not the words.** Split it in two,
   remove an action, change the angle.

The pipeline does not need fifteen people to work — it needs the rules followed. It scales
down to a team of one.

---

## Related

- `SKILL.md` — the prompt grammar this pipeline fills in
- `ENGINE-RULES.md` — the hard rendering constraints
- `PRODUCTION-PATTERNS.md` — tutorial-demonstrated patterns from the same source family
- `../higgsfield-acting/SKILL.md` — the performance system the CHARACTER ACTING block encodes
- `../higgsfield-soul/SKILL.md` — Soul ID character sheets and multi-character consistency
- `../higgsfield-shotlist-director/SKILL.md` — the connected-shotlist form of "one dictionary
  of names for the whole project"
- `../higgsfield-recall/SKILL.md` — the iteration log
- `../../templates/seedance/global-style-prefix.md` — the Style Prefix pasted into every prompt
