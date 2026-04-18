---
name: higgsfield-seedance
description: "Rewrites scene descriptions using professional cinematography language, structures prompts with a six-slot formula (camera + subject + action + setting + style + lighting), and diagnoses content filter rejections via a preflight linter. Use whenever the user asks for a Seedance 2.0 / Seedance Pro prompt, describes a scene for Seedance generation, mentions Seedance, reports a Seedance generation failure or flagged prompt, or is burning credits on Seedance regenerations."
user-invocable: true
metadata:
  tags: [higgsfield, seedance, seedance-2.0, seedance-pro, content-filter, prompt, director, flagged]
  version: 1.0.0
  updated: 2026-04-10
  parent: higgsfield
---

# Higgsfield Seedance Director

Use this skill whenever the user wants a Seedance 2.0 / Seedance Pro prompt, OR
whenever a Seedance generation has been blocked, flagged, or silently failed.
This skill's job is to stop credit waste on filter rejections.

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

## Seedance 2.0 Prompt Modes

Seedance 2.0 exposes four generation modes that each take the six-slot formula
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

### Mode Selection Rule

Reference-Based for new action with an existing character. Continuation for the
next beat in time. Expand Shot to widen the frame spatially. Edit Shot to patch
specific details. If you find yourself writing across multiple modes in one
prompt — stop, pick one, generate, then use the output as input to the next mode.

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

---

## Pre-flight Linter

Before the user generates, run the prompt through the preflight linter:

```
python3 seedance_lint.py "<prompt text>"
```

The linter is at the project root (`seedance_lint.py`). It flags:

- **Real names** of public figures / celebrities / politicians
- **Brand, IP, franchise names** (Nike, Marvel, Spider-Man, Pokémon, etc.)
- **Raw violence verbs** (fight, attack, kill, shoot, blood, gore, stab)
- **Age markers** (child, kid, young, teen, boy, girl — Seedance is age-blind)
- **Note-to-friend voice** (no Style/Mood, no Camera, no Lighting sections)
- **Overlength** (>180 words is risk territory; >220 words often hard-fails
  on the text encoder, not the filter)
- **Conflicting instructions** (moving + frozen, bright + dark, etc.)

Output is `PASS`, `WARN`, or `FAIL` with the specific fix for each rule hit.
Treat `FAIL` as "do not hit generate." Treat `WARN` as "likely to pass, but
here is what to harden."

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
   ambiguous intent.
4. **Describe force and direction, not destruction sequence.** "Driven into
   the car, metal buckling" not "thrown into side door, glass shatters, uses
   rebound to sweep leg."
5. **Present tense, active voice.** "She turns" not "she is turning."
6. **Cut the antislop words.** Breathtaking, stunning, epic, masterfully,
   cinematic masterpiece — these signal marketing copy, not a shot description,
   and correlate with flags.

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

---

## When the User Is Already in a Failure Loop

If the user tells you Seedance has flagged them multiple times in a row:

1. **Ask for the exact prompt text that got flagged.** Don't guess.
2. **Run the preflight linter** on that exact text.
3. **Apply the rewrite playbook** for every rule the linter hit.
4. **Do a voice pass** (add Style & Mood, name the camera, present-tense physics).
5. **Log the fix** to the filter-memory database at the project root so future
   sessions benefit — use `higgsfield_memory.py` (at the project root) to append
   an entry describing the blocked prompt, the substitution, and whether it worked.

Do not let the user regenerate the same prompt with one word changed. That
is the loop that wastes hours.

---

## Related Skills

- `higgsfield-prompt` — MCSLA formula, archetype router, general prompt structure
- `higgsfield-troubleshoot` — diagnosis for non-filter failures (render quality, etc.)
- `higgsfield-recall` — pre-generation memory check against past failures
- `../shared/negative-constraints.md` — full negative-constraint reference,
  including the Content Filter / Safety section
- `../../docs/Seedance 2 Skill.md` — extended bilingual director reference
  (archetypes, cut rules, camera language appendix)
