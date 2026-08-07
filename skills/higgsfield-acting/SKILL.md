---
name: higgsfield-acting
description: "Writes the character-performance layer of a video prompt as behavior under pressure, not displayed emotion — objective, obstacle, tactics, beats, subtext, listening, body/status/proxemics, and mandatory eye life. Produces a reusable 150–220-word acting master profile per character plus a per-scene rewrite of it, and a locked voice prompt. Use whenever a prompt needs acting, performance, or emotion direction; whenever characters read wooden, dead-eyed, or 'AI'; whenever a character must stay themselves across many shots; or when the user asks for character behavior, mannerisms, tics, a gait, or how someone reacts. Pairs with higgsfield-facs (muscle-level AU codes) and higgsfield-seedance (the prompt the paragraph goes into)."
user-invocable: true
metadata:
  tags: [higgsfield, seedance, acting, performance, character, behavior, emotion, subtext, beats, eye-life, voice, ensemble, master-profile]
  version: 1.0.0
  updated: 2026-08-07
  parent: higgsfield
---

# Higgsfield Acting Director

`[OFFICIAL — Higgsfield "Hell Grind" open-source brief]` — the performance system behind
Higgsfield's 95-minute AI feature film, adapted to this repo's prompt surfaces.

**The core axiom of the entire system: acting is BEHAVIOR under pressure, not a display of
emotion.** A character wants something, something is in the way, and they act to get it.
Emotion is a byproduct of that struggle — never the thing you write directly.

This is a **layer on top of** `../higgsfield-seedance/SKILL.md`: the paragraph this skill
produces goes into the PERFORMANCE / CHARACTER ACTING block of an otherwise normal Seedance
prompt. It does not change camera, light, wardrobe, or grade.

## QUICK FACTS
*Generated-checked block (scripts/build_index.py verifies anchors). Routing aids — read the linked sections for the rules.*
- Write the **objective** (a verb aimed at a partner), never the state — "make him confess", never "be angry" [→](#the-five-pillars-of-every-scene)
- **2–4 beat changes** per scene, each one visible in behavior: a pause, a posture change, a tempo change, a shift of gaze. Unchanged behavior for the whole shot = played flat [→](#the-five-pillars-of-every-scene)
- **Listening beats speaking.** The reaction starts *before* the partner's line ends; a hard question earns a micro-pause before the answer [→](#listening-and-reaction)
- The body carries the biography: **center of gravity, tempo, openness, breath** — set all four before any psychology [→](#the-body)
- **Business** — a physical task the hands are doing — kills theatricality; the strongest accent in a scene is the moment the character **stops** it [→](#the-body)
- **Distance is drama**; a change of distance *is* a beat change. Status is what you DO, and status **breaks** are the most interesting thing in a performance [→](#the-body)
- The **master profile** is 150–220 words, one paragraph, fixed block order, written once per character and then rewritten per scene — never pasted [→](#the-acting-master-profile)
- Every tic carries a **trigger**; every mask carries a **crack** — at least one "However, when X…" clause per profile [→](#the-acting-master-profile)
- **Eye life is mandatory and never optional** — saccades, blink quality, live catchlights, eyes-lead-thought. Dead eyes are the number-one tell of AI acting [→](#eye-life)
- Scene adaptation **transforms, never deletes**: a behavior that can't physically happen is displaced into another outlet, not removed [→](#scene-adaptation)
- The **voice prompt is locked** — one per character, pasted verbatim into the audio field, never adapted per scene [→](#voice-fixed-identity-never-adapted)
- **States, not transitions.** Models fail process and nail state: "mid-throw, arm extended", not "reaches in, pulls out, winds up" [→](#states-not-transitions)
- Ensemble reactions travel in a **wave, never in sync**; the strong are still and quiet, the weak fidget and shout [→](#ensemble-and-space)
- 15 named bad-acting symptoms with prompt-level fixes, and a 0–5 self-check scale — **aim every hero shot at 4+** [→](#the-atlas-of-bad-acting)

---

## Where this sits among the repo's performance tools

| Layer | Skill | What it controls |
|---|---|---|
| **Craft** — why the character does anything | **this skill** | objective, obstacle, tactics, beats, subtext, status, business |
| Muscle | `../higgsfield-facs/SKILL.md` | facial Action Unit codes (AU12, AU6…) |
| Named expressions | `../higgsfield-soul/SKILL.md` § Micro-Expressions | expression vocabulary for identity work |
| Production form | `../higgsfield-seedance/HELL-GRIND.md` § Two extra blocks | the CHARACTER ACTING block this output fills |
| Backstory | `../higgsfield-character-design/SKILL.md` | who the character is before any scene exists |

Use this skill to decide **what the body does**; use FACS to specify **which muscles** do it
in a close-up. They compose — a FACS beat schedule inside a paragraph written by these rules
is the highest-resolution performance the platform supports.

---

# Part I — The craft

## What good acting is

Truthful behavior under imaginary circumstances. Not depicted emotions, not recited text,
not "expressive faces."

| Bad acting | Good acting |
|---|---|
| Shows the emotion ("I am angry") | Pursues the objective ("I will make you return the money") — anger arises on its own |
| Waits for their cue | Listens and reacts to the partner every second |
| Body illustrates the words (gesture = word) | Body lives its own life, sometimes contradicts the words |
| All lines in one tempo and tone | Rhythm changes with every change of tactic |
| Emotion switches on at the line and off after | State is continuous — there is a life before and a life after the line |
| The face "performs" — eyebrows, grimaces | The face thinks — the thought is readable in the eyes before the words |

## The five pillars of every scene

Every character in every scene decomposes into five elements. If one is missing, the
performance falls apart.

**1. Objective.** What the character wants IN THIS SCENE, RIGHT NOW, FROM A SPECIFIC PERSON.
Always a verb aimed at the partner: *make him confess* · *beg a week's extension* ·
*convince her I'm not afraid*. Never a state ("be angry", "feel guilty") — states cannot be
played. Behind the scene objective sits a **super-objective**: what the character wants
across the whole story, with every scene objective a step toward it.

**2. Obstacle and stakes.** What prevents them — external (another character wants the
opposite; witnesses in the room; two hours to deadline) or internal (pride won't let them
beg; they don't believe their own words). Always answer *what happens if I do NOT get what I
want?* — and the answer must frighten the character. The higher the cost of failure, the
more taut the scene.

**3. Tactics.** The concrete method of pursuing the objective right now, as an action verb:
*press · charm · shame · plead · provoke · bargain · threaten · stall*. When a tactic fails,
a living person **changes** it. One tactic for a whole scene is dead acting.

**4. Beats.** The smallest unit of action: the stretch during which the character wants one
thing and pursues it one way. A beat ends when the objective is achieved, the tactic fails,
new information arrives, or the balance of power shifts. **Every beat change must be VISIBLE
in behavior** — a pause, a change of posture, a change of speech tempo, a shift of gaze. A
good scene has **2–4 beat changes**.

**5. Subtext.** What the character actually thinks and wants, as opposed to what they say.
Subtext is **not performed** — it leaks out on its own when the character plays the true
objective while speaking the false text. Buildable markers: questions that aren't questions ·
repetitions (asking the same thing — they don't believe the answer) · abrupt topic changes ·
jokes at the wrong moment (a shield against vulnerability) · answers that are too short
("Fine." "Sure." — a closed door).

## Listening and reaction

Performance lives not in the lines but **between** them. Four observable markers to write in:

1. **The reaction starts before the partner's line ends.** A person grasps the point
   mid-phrase — the face and body already answer. A neutral face until the line ends, then
   "switching on", is dead acting.
2. **Thought before word.** Before a hard answer there is a micro-pause — the person visibly
   decides what to say. Instant answers at uniform speed read as memorized text.
3. **The assessment moment.** After news, a threat, or an insult, the character needs time to
   digest — from a fraction of a second to a long pause. Cinema lives on close-ups of these
   assessments: a face, a defocused gaze, the world swimming.
4. **Contagion from the partner.** Tempo, volume, and energy shift in response: a shout is
   answered either with a counter-shout or with pointed quiet — but *answered*, not continued
   over.

## The body

**Physical state before psychology.** Set four parameters for every character before any
inner life:

- **Center of gravity** — high (chest, chin: confidence, aggression, status) or low
  (shoulders, slouch: fatigue, fear, submission).
- **Tempo** — fast/ragged (nervousness, stimulant energy) or slow/economical (control,
  threat — the most dangerous people move least).
- **Openness** — squared shoulders and open palms, versus crossed arms, dropped head, closed
  poses.
- **Breath** — high and rapid (panic) versus low and slow (control). Breath is the most honest
  indicator of state, and sound must match physics: someone who just ran cannot speak on a
  steady voice.

**Business — the physical task.** A character almost always needs a DOING. They don't "have a
conversation" — they fix an engine, count money, cook, wipe a glass, and talk over the top of
it. Business kills fake theatricality (the hands are busy with truth), creates rhythm (pauses
fill with action), and generates subtext (*how* a person counts money says more than the
words).

> **The interrupted-action rule.** The strongest accent is when a character **stops** the
> business. If he was slicing bread and stopped at a phrase, the phrase became an event. Use
> the stop as punctuation.

**Proxemics — distance as drama.** The distance between characters is a visible graph of
their relationship:

| Zone | Distance | Reads as |
|---|---|---|
| Intimate | under 0.5 m | love or violence — entering uninvited is aggression |
| Personal | 0.5–1.2 m | trust |
| Social | 1.2–3.5 m | business, wariness |
| Public | 3.5 m+ | alienation, hierarchy |

A threat whispered 10 cm from a face is scarier than one shouted across a room. Scene drama is
often just the story of distance: who closes it, who breaks it, who freezes. **A change of
distance is a change of beat** — and it must be written in metres, per the measurable-language
rule in `../higgsfield-seedance/SKILL.md`.

**Status — the invisible hierarchy.** Status is what you DO, not who you are.

- **High status:** an immobile head, slow movements, long gazes, pauses before answering,
  taking up space, touching other people's things.
- **Low status:** fussing, frequent self-touching (face, hair), broken speech, filler-laughter,
  asking permission with the eyes.

The most interesting thing in a performance is a **status break**: the boss who shows fear for
one second; the underling who suddenly stops smiling. A powerful scene shape is *enter high and
collapse*, or *enter low and flip the room*.

## How good acting sounds

- Rhythm is written in the text — deliver it precisely; fast ≠ mushy.
- Overlaps are normal (lines stepping on each other's tails), but key words stay clean.
- **Volume contrast: the most frightening things are said the quietest.** Shouting is the
  currency of the weak; the character who owns the scene lowers the volume and everyone leans in.
- Pauses are events, not holes — a pause is legal only if something happens inside it: an
  assessment, a decision, a refusal to answer.
- Real speech has litter: interruptions, half-heard words, repetitions, unfinished phrases.
  Perfectly constructed sentences kill street truth.

---

# Part II — Writing the acting

## The acting master profile

Every recurring character gets **one** master profile — the permanent source of truth about
how they act. Written once, then adapted per scene. Target: **150–220 words, one flowing
paragraph**, fully observable and filmable.

**Block order is fixed:**

```
Character acting as [NAME]. [Build, physique, posture — the body as a document of their
biography]. [The psychological engine in one clause — the inner drive that explains the
physicality]. Vocal profile: [pitch/timbre, accent/origin, pace and delivery manner, and how
the voice breaks or shifts under emotion]. Key physical habits and tics: [signature tic with
its trigger; stress tic with its trigger; concealment behavior — what they do to hide what
they feel; the facial mask and the exact condition under which it cracks]. Eye life: [blink
quality and rate, scanning pattern, gaze-before-head, catchlights]. Walking style: [the gait
as characterization — named and specific, with weight, rhythm, and foot placement]. However,
when [emotional trigger], [the transformation — how the posture, gait, and face change].
[Optional: the softening target — the one person or thing that makes the face genuinely soften].
```

**Rules for each block:**

1. **Only observable behavior.** Every inner state needs a body marker. Never "he is nervous" —
   write the trembling lower lip, the heavy swallow, the long inhale through the mouth and
   sharp exhale through pursed lips.
2. **Every tic has a trigger.** Not "he cracks his knuckles" but "he cracks his knuckles during
   mundane conversations to fake confidence." Format: `[tic] + [when/why]`. Tics without
   triggers are decoration; tics with triggers are dramaturgy.
3. **Name the gait.** A coined name in quotes anchors the biomechanics — a "power-walk", a
   "peacock strut", a "gallery walk", a "battering-ram stride", a "dreadnought pace" — then
   unpack it: weight, step, what the torso and arms do, what the head does.
4. **Build in the mask AND the crack.** The single most cinematic device in a profile is the
   conditional transformation: the facade, plus the precise trigger that collapses it. A
   dominant swagger that crumbles into a childlike slouch when rejected; stern discipline that
   melts into a radiant smile at one specific person. **Every profile carries at least one
   "However, when X — …" clause.** A character playing two truths at once is the difference
   between a puppet and a person.
5. **One softening target.** Where it fits, give the face exactly one person, animal, or object
   it genuinely softens for. One — not two. This humanizes without diluting.
6. **No wardrobe.** Clothing lives in the scene/look block, never in the acting profile. The
   profile must survive any costume change.
7. **No camera, no color.** Acting drives performance, face, voice, and motion only.
8. **Physique carries biography.** Build and posture tell the backstory — a build "weathered
   from past struggles", shoulders "perpetually tense", a posture "over-corrected to project
   authority". Profession, past injuries, and self-image must be readable in the body.

> **Age is not a profile field.** Engine rule 1 (`../higgsfield-seedance/ENGINE-RULES.md`) is
> age-blind characters, and the content filter tightens sharply on age words. Carry the same
> information through **build, wear, posture, and voice** — "a body that has already been
> repaired twice", "a working-class rasp", "an old boxer's walk" — never a number and never
> *boy / girl / young / teen*.

## Eye life

**Dead eyes are the number-one tell of AI-generated acting.** Every character gets continuous,
naturalistic ocular life, in the profile *and* in every scene.

- **Micro-saccades and gaze targeting** on whatever they attend to; the gaze keeps moving —
  eyes drift, flick away in thought, scan to a detail and settle back. They never lock frozen.
- **Realistic blink rate and quality**, tied to state: rapid blink-bursts under stress; slow
  calm lids in control; a blink-and-glaze on a moment of dissociation.
- **Live catchlights** — the eyes must read as wet, lit, and alive.
- **Controlled stillness is chosen, never dead.** For a near-unblinking predator calm, keep
  blinks rare, slow, and deliberate — a decision, not a freeze — and let the gaze still shift
  slowly with intent.
- **Eyes lead the thought.** The eyes reach the target a touch before the head turns. The
  thought is readable in the eyes before the words come.
- **Eye life reacts to the beat.** Blink rate, gaze steadiness, and catchlight warmth all shift
  when the beat shifts.

The phased-blink shorthand from the film pipeline — *one lazy blink → a quick DOUBLE-BLINK →
one HARD reset-blink* — is the cheapest way to buy a living face in a static shot
(`../higgsfield-seedance/HELL-GRIND.md` § Physics, not adjectives).

## Scene adaptation

The master profile is who the character IS. For each scene, **rewrite it into the moment** —
never paste it.

1. **Present characters only.** An acting paragraph only for characters actually in the shot.
   No character in frame → no paragraph.
2. **Keep the constant core.** Identity, vocal profile, signature tics, eye life, and the
   emotional through-line stay the same in every scene — this is what holds the character
   together across cuts. Never contradict the master.
3. **Re-express for this scene.** Select, emphasize, modify, or drop specific behaviors to fit
   the scene's posture (seated / standing / running / hiding), action, beat, emotional state,
   and time of day.
4. **Transform, don't delete.** A behavior that physically cannot happen here is *converted*,
   not removed: a restless pacer slumped on a sofa keeps the same nervous engine, displaced
   into restless micro-sway, wrist-flicks, and paper-tearing. **The energy is constant; its
   outlet changes.**
5. **One flowing paragraph.** Fold the adaptation into prose in the character's register — no
   bullet lists, no headers, no "dial" lines inside the prompt.
6. **Lead with the character's reference tag** so the model binds the acting to the right
   person (`../higgsfield-seedance/SKILL.md` § Tag naming).

## Voice — fixed identity, never adapted

Acting is rewritten per scene; **voice is locked.** Each character gets one Voice prompt — a
permanent vocal identity pasted **verbatim** into the audio field every time they speak, and
never modified. If the character appears but says nothing, omit it.

```
"A [origin / accent descriptor]. [Timbre and register]; [pace and delivery manner];
[emotional character — and how it shifts under pressure]."
```

The vocal profile *inside* the acting paragraph describes how speech behaves dramatically
(tempo shifts, breaking registers, whispers); the Voice prompt in the audio field locks the
**sound** itself. Both must agree.

Seedance holds only three or four voices per character within one tonality, so drift is real —
stress-test the voice across generations exactly like the look, and lock it harder rather than
"keep shooting" (`../higgsfield-seedance/HELL-GRIND.md` § The voice is not an asset).

## States, not transitions

Video generation models fail transitions and nail states. Describe characters **already IN**
the action state — mid-throw, mid-punch, mid-pace, mid-argument — not the process of getting
there.

- ❌ "reaches into the bag, pulls out the knife, winds up" → collapses
- ✅ "mid-throw, arm extended" → lands

Chain states beat by beat instead of narrating continuous processes. The production form of
this rule: complex action **opens** the prompt, and the approach becomes a separate shot
(`../higgsfield-seedance/HELL-GRIND.md` § Solutions born under deadline).

## Ensemble and space

- **Group reactions travel in a wave, never in sync.** One person gets the joke first, the
  second half a beat later, the third not at all. Simultaneous identical reactions read as fake
  — unless a deliberately choreographed comic sync is the point.
- **The reaction is worth more than the action.** After every event, the most valuable frame is
  the face of the person who saw it.
- **Freeze at the threat.** Constant ensemble micro-movement — shifting weight, gesturing,
  leaning — and at the key threat everything STOPS. The contrast of bustle → stillness is
  punctuation.
- **Movement equals motivation.** Nobody crosses a room without an impulse: toward something or
  away from something. Strong motivated events — closing in (escalation) · turning one's back
  (dismissal, or hiding the face) · standing while the other sits (dominance grab) · sitting
  down mid-conflict (paradoxical power) · stopping in the doorway (the threshold is the decision
  point) · starting to pack (ultimatum by body).
- **The strong are still and quiet; the weak fidget and shout.** Danger is played not by the
  dangerous one but by the tension of everyone around them. Threat without wind-up: no menacing
  pauses, no slow-motion turns — in a truthful world violence arrives without an announcement.
- **Degradation accumulates.** If a character is worn down across a story, carry it in the body
  cumulatively — greyer, heavier, slower reactions — never resetting between scenes.

> **Engine ceiling:** only ≤3 characters track reliably across cuts
> (`../higgsfield-seedance/ENGINE-RULES.md` rule 5). Write the wave for the tracked pair or
> trio; everyone else is crowd, described as a mass.

---

# Part III — Quality control

## The atlas of bad acting

Recognize the symptom, apply the prompt-level fix.

| # | Symptom | How it looks | Prompt-level fix |
|---|---|---|---|
| 1 | Indication (mugging) | The face "depicts" the emotion: arched brows, grimaces | Remove the face from the task; write the objective and give the hands business |
| 2 | Playing the result | The character plays the scene's outcome from second one | Write only what the character knows NOW |
| 3 | Waiting for the cue | Empty face while the partner speaks | Write the reaction starting mid-line of the partner |
| 4 | Monotactics | One color for the whole scene (all shouting / all whining) | Mark the beats; a new tactic verb for each |
| 5 | Gesture illustration | Gesture duplicates the word ("big" — arms spread) | Gesture either precedes the thought, contradicts the words, or is absent |
| 6 | Free emotion | Tears or rage with no build-up and no trigger | Build the ladder: restraint → break; emotion must cost something |
| 7 | Body false to biography | A thug with a dancer's posture | Set the body profile: center of gravity, tempo, wear |
| 8 | Speech too clean for the class | A street character speaking in literary periods | Litter the speech: interruptions, dropped endings, repeats |
| 9 | Threat signaling | "Menacing" pauses, squints, slow turns before violence | Threat is mundane; violence without wind-up |
| 10 | Synchronized ensemble | Everyone reacts identically and at once | Stagger reactions in a wave, vary their strength |
| 11 | Dead pauses | Silence in which nothing happens | Fill with assessment or business — or cut |
| 12 | Emotional reset | The character instantly "recovers" after a strong event | States have inertia; the trail carries into the next beat |
| 13 | Commenting the role | The performance winks at the viewer | Full belief in the circumstances; comedy is played dead serious |
| 14 | Close-up overload | Active mimicry on a close-up | The tighter the shot, the less movement: only the eyes and the thought |
| 15 | Dead eyes | Frozen stare, no blinks, no saccades, glassy catchlights | Apply § Eye life in full — it is never optional |

## The performance scale

A self-check on the paragraph before it ships.

- **0 — Mannequin.** Text delivered, behavior absent.
- **1 — Declaimer.** "Expressive" text, indicated emotions, illustrating body.
- **2 — Diligent.** An objective can be guessed, but one tactic, late reactions, empty pauses.
- **3 — Craftsman.** Objective and beats present, listens to the partner, body makes sense.
  Missing: subtext, surprising tactics, inertia of states.
- **4 — Alive.** Continuous behavior, contrasting tactics, subtext diverging from text, status
  in the body, reactions ahead of lines, at least one unexpected-but-true choice.
- **5 — Magnet.** All of 4 plus paradox. **The two-truths rule: at level 5 the character always
  plays TWO truths simultaneously** — helps and hates it; apologizes and defends; loves and has
  already left. One clean emotion without contradiction reads as synthetic on a close-up.

**Aim every hero shot at 4+.** A paragraph that self-checks at 2 or below gets rewritten before
it ships.

## Pre-send checklist

- [ ] Objective as a verb aimed at a partner — for every character in frame
- [ ] Obstacle and stakes exist; the cost of failure is real
- [ ] 2–4 beat changes, each visible in behavior (pause / posture / tempo / gaze)
- [ ] Reactions begin before the partner's lines end; assessment moments present
- [ ] Every character has business; the interrupted-action accent used deliberately
- [ ] Distances change, the changes are motivated, and they are written in metres
- [ ] Status is in the body, not just the words
- [ ] All tics carry triggers; the mask has its crack ("However, when X…")
- [ ] Eye life written explicitly: saccades, blink quality, catchlights, eyes-lead-thought
- [ ] Voice prompt pasted verbatim if the character speaks; omitted if silent
- [ ] States, not transitions
- [ ] No wardrobe, camera, or color inside the acting paragraph
- [ ] No age words anywhere (engine rule 1)
- [ ] Ensemble reactions staggered; strong = still, weak = fidgety
- [ ] Scale check: would this paragraph score 4+?

---

# Part IV — Worked example

Invented character; use as a pattern, not as content.

## Master profile

```
Character acting as VIKTOR. A retired night-shift taxi driver and former amateur boxer; heavy,
thick-necked build gone soft at the middle, with a flat-nosed face and old scar tissue over
both eyebrows; sits and stands with a low, grounded center of gravity, weight always on the
whole foot. Runs on a single engine: decades of waiting — for fares, for rounds, for trouble —
have made patience his weapon. Vocal profile: low, hoarse, unhurried baritone with a
working-class rasp, short sentences delivered flat and economical, dropping to a slower,
quieter register the more serious things get — he never speeds up. Key physical habits and
tics: rolls an old coin across his knuckles when sizing a situation up; a slow, audible
nose-breath before he says no; when lying is happening in front of him, he goes completely
still and lets a long silence do the pressing; his default face is a heavy-lidded, bored mask
that conceals total attention. Eye life: sleepy, hooded eyes with slow deliberate blinks and
constant quiet scanning — mirrors, hands, exits — the gaze settling on a speaker a beat before
his head turns; catchlights low but alive. Walking style: a heavy, rolling "old boxer's walk",
short economical steps, shoulders level, hands loose and ready, never hurrying. However, when
someone raises a hand near him, the sleepy mask vanishes in a half-second: the chin drops, the
hands rise halfway, the feet find their old stance — then he catches himself and folds it away,
embarrassed. His face only truly softens for stray dogs, which he feeds from his coat pocket.
```

**Voice (pasted verbatim when VIKTOR speaks):**

```
"A working-class city accent, roughened by decades of night shifts. Low, hoarse, unhurried
baritone; short flat economical sentences with long comfortable pauses; calm and faintly
amused, going quieter — never louder — as things get serious."
```

## Scene adaptation

*Scene: VIKTOR sits in his parked cab at night; a nervous passenger in the back seat is lying
about having money for the fare.*

```
VIKTOR sits motionless in the driver's seat, heavy and grounded, watching the passenger in the
rear-view mirror instead of turning around — his hooded eyes flick between the mirror, the
passenger's hands, and the door lock in slow, quiet scans, blinks rare and deliberate, the gaze
settling on the mirror a beat before his head ever moves. The old coin walks across his
knuckles on the seat-rest, unhurried; as the passenger's story falls apart, the coin stops
mid-roll — he lets the silence sit, takes one slow, audible breath through the nose, and
answers in his low, hoarse baritone, flatter and quieter than before, never speeding up. Only
when the passenger's voice cracks does the sleepy mask ease a fraction: a long exhale, a slow
blink, the coin resuming its roll — patience choosing, for now, to be kind.
```

**What happened here:** the walk is irrelevant (seated) so its energy moved into stillness and
the coin; the signature tics kept their triggers (coin = sizing up · stopped coin = interrupted
action as punctuation · nose-breath = refusal · stillness plus silence = pressure on a liar);
the eye life obeys the master but is re-targeted to mirror, hands, lock; the beat changes are
visible (coin stops → silence → quieter voice → softening); and the voice stayed untouched —
it will be pasted verbatim into the audio field.

---

## Final axioms

1. Acting is behavior under pressure, not a demonstration of feelings.
2. Listening matters more than speaking; reacting matters more than declaiming.
3. Emotion is the consequence of a won or lost struggle, and it is expensive.
4. The body is smarter than the words: when text and body conflict, the viewer believes the body.
5. The strong are still and quiet; the weak fuss and shout. Exceptions are events.
6. Every tic needs a trigger; every mask needs a crack.
7. Every scene is somebody's defeat. If nobody lost, there was no scene.
8. Subtext is not shown — it fails to be hidden.
9. States, not transitions; the model films what is, not what becomes.
10. When in doubt — cut. Less acting equals more truth.

---

## Related Skills

- `../higgsfield-seedance/SKILL.md` — the Seedance prompt this paragraph goes into
- `../higgsfield-seedance/HELL-GRIND.md` — the CHARACTER ACTING block's production form,
  dialogue construction, and the micro-life rules
- `../higgsfield-seedance-2-5/SKILL.md` — 2.5's observable-cue emotional direction
- `../higgsfield-facs/SKILL.md` — muscle-level facial control by Action Unit code
- `../higgsfield-soul/SKILL.md` — identity consistency and micro-expression vocabulary
- `../higgsfield-character-design/SKILL.md` — the story bible upstream of any profile
- `../higgsfield-audio/SKILL.md` — where the locked voice prompt is delivered
