---
name: higgsfield-prompt
description: "Use when building, writing, refining, or structuring a Higgsfield AI prompt. Covers the MCSLA formula, prompt structure, narrative vs. timestamped formats, and how to write for both text-to-video and image-to-video workflows."
user-invocable: true
metadata:
  tags: [higgsfield, prompt, MCSLA, formula, text-to-video, image-to-video]
  version: 3.4.0
  updated: 2026-05-18
  parent: higgsfield
---

# Higgsfield Prompt Engineering

## The MCSLA Formula

Every high-performing Higgsfield prompt is built on five layers. Think of it as the
cinematographer's checklist — fill in each layer and the model has everything it needs.

| Letter | Element | Description | Example |
|--------|---------|-------------|---------|
| **M** | Model | Which generation engine | "Use Kling 2.6" |
| **C** | Camera | Named camera control | "FPV Drone shot weaving through the alley" |
| **S** | Subject | Who/what + appearance | "A woman in a sand-colored suit, sharp eyes" |
| **L** | Look | Style + color + lighting | "Cinematic, golden hour, anamorphic flare" |
| **A** | Action | What happens in the scene | "She turns slowly, wind lifting her coat" |

---

## Prompt Types

### Text-to-Video (T2V)
Start from nothing — describe the entire scene from scratch.
Best for: establishing scenes, abstract concepts, environments without a specific character.

```
[Subject + appearance].
[Environment — location, time, weather, atmosphere].
[Action — what happens and how].
[Camera — named control].
[Look — style + color grade].
```

**Example:**
```
A lone astronaut stands on the surface of a red desert planet, helmet visor reflecting
twin moons rising on the horizon. Dust spirals slowly in the thin atmosphere.
She turns to face the camera, gloved hand raised in a slow salute.
Camera: slow Crane Up revealing the vast emptiness behind her.
Style: Cinematic, desaturated orange and deep blue, 2.35:1 anamorphic.
```

---

### Image-to-Video (I2V)
Animate a provided still image. The image defines the starting frame.
Best for: character consistency, product shots, portrait animation, storyboard bring-to-life.

```
[Reference the input image as the first frame].
[Describe what should move, change, or animate — not what is already visible].
[Camera — named control].
[Style/atmosphere cues].
```

**Example:**
```
Starting from the provided image as the first frame.
The woman's hair lifts gently in the wind. She blinks slowly and turns her gaze
slightly to the left, a faint smile forming.
Camera: subtle Dolly In toward her face.
Style: Cinematic, warm afternoon light, shallow depth of field.
```

**Key rule for I2V:** Do NOT re-describe what is already in the image. Only describe
what should *change* or *animate*. Over-describing the static elements confuses the model.
This applies equally to @ Image references in Seedance/Cinema Studio 3.0 — describe
ONLY motion and camera movement, never what's already visible.

---

## Narrative Structure

### Fluid Narrative (preferred for most use cases)
Write the scene as continuous action. No timestamps. Most natural for Higgsfield.

```
A detective pushes open the door to the rain-soaked rooftop, coat whipping in the wind.
She steps to the edge and looks down at the city below — a thousand lights blurring
through the downpour. Camera dollies slowly behind her, then cranes up to reveal the
skyline. Cinematic style, cold blue tones, 16:9.
```

### Timestamped (use only for precise multi-beat sequences)
Only use when exact timing of separate actions matters — e.g., a transformation,
a multi-phase action sequence, or a beat-synced music video. Maps to Cinema Studio 3.0's
Custom multi-shot mode.

```
0–3s: Wide establishing shot. The fighter stands alone in the ring, chest heaving.
3–6s: Crash Zoom In on his face. Sweat on his brow, jaw clenched.
6–10s: 360 Orbit as he raises his fists. Crowd noise rises.
```

---

## High-Performing Prompt Patterns

> **The #1 mistake in video prompting**: over-describing appearance and under-describing
> behavior. Give your subject something to DO. Give them an internal state that creates
> visible behavior. A verb that describes motion or intention is more important than
> adjectives.

**Specificity beats generality:**
- ❌ "the camera moves dramatically"
- ✅ "camera Dolly Zoom In — subject stays the same size as the background rushes forward"

**Active verbs carry the scene:**
- ❌ "a woman is in an alley"
- ✅ "a woman darts through a rain-soaked alley, coat flapping, boots splashing"

**Name the camera control:**
Higgsfield understands its own preset names. Always use them explicitly.
- ❌ "the camera slowly circles"
- ✅ "360 Orbit around the subject"

**Lead with subject, end with style:**
Subject → Action → Camera → Style is the most reliable order.

**Keep it under 200 words:**
Focused prompts outperform exhaustive ones. One clear intention > ten vague details.

**Cinema Studio: Keep it under 512 characters:**
Cinema Studio has a hard 512-character limit on prompts (both 2.5 and 3.0).
- **2.5:** @ Element chips consume ~80–100 hidden characters each. With 2 @ tags, keep visible text under ~250 chars.
- **3.0:** @ references (images/video/audio) are media attachments, not inline metadata — they consume less hidden space. Keep visible text under ~350–400 chars with references, ~450–500 without.
See the Cinema Studio skill for full character budget details.

---

## The Pre-Prompt Checklist

Before writing any prompt, answer these five questions. Vague prompts like "give me
something cinematic" tell the AI nothing.

| Question | What to specify |
|----------|----------------|
| **Who?** | Subject + appearance (e.g. "a man in a leather jacket") |
| **Where?** | Environment + atmosphere (e.g. "in a narrow aircraft galley, cold blue light") |
| **What's happening?** | 1 primary action (e.g. "punches his opponent") |
| **Camera movement?** | Named preset (e.g. "Handheld") or Cinema Studio Director Panel |
| **Mood/Genre?** | Style + color grade, or Cinema Studio genre selection |

---

## One Action Per Scene

AI models can replicate real-life physics — but only so much at once. Asking for
multiple complex actions in one clip overwhelms the model.

**Rule:** 1 primary action per clip, with 1–2 secondary actions max.

Break complex sequences into separate shots and stitch them in a video editor, or
use Multi-Shot Manual mode to prompt each scene separately.

**Fast Motion Trick:** If fast motion keeps morphing or breaking, generate the scene
in Slow Mo first, then speed it up in post (CapCut, Premiere, DaVinci). The model
renders cleaner physics in slow motion.

---

## Generic-Emotion Decomposition — Which kind of X?

Never leave a generic emotion in a prompt. "Sad" / "angry" /
"surprised" / "scared" / "thoughtful" / "in love" — each is at least
three or four distinct physical realizations, and the model renders
a different version depending on which one your prompt invites. A
prompt that says only "she looks surprised" produces a different
shot every regeneration and degrades adherence across batches.

The rule: decompose the generic emotion into specific muscle
movements, breath, eyes, and skin. If you can't decompose
confidently, ask the user to choose a variant.

Clarification template — offer when the script or user supplies a
generic emotion you cannot decompose without inventing detail:

> Which kind of surprise?
> (a) Light positive — eyebrows lift, lips part softly, slow inhale
>     through the nose, no other movement.
> (b) Shock — sharp inhale through the mouth, eyes widen, body
>     freezes in place, hand involuntarily lifts to chest.
> (c) Disbelief — slow blink, head tilts a fraction, lips press
>     together, only one eyebrow lifts.
> (d) Surprise-with-joy — eye light shifts (catchlight reads),
>     smile builds gradually, shoulders relax.

Same shape applies to any generic adjective — "tense" / "sad" /
"angry" / "scared" / "thoughtful" / "in love" each decomposes into
3-5 distinct physical realizations. The decomposed prompt produces
a performance; the generic prompt produces AI-video.

> **Preset library alternative.** For named micro-expression presets
> that drop into a prompt without first-principles decomposition,
> see `../higgsfield-soul/SKILL.md` § Micro-Expressions. The catalog
> covers most common emotional registers with locked physical
> descriptors. Use the decompose-from-first-principles rule above
> when no preset matches; use the preset library when one does.

### Layered emotion states

Single-axis decomposition (above) names one register: angry / sad /
surprised. **Layered emotion** names a composite state where two
registers stack — *anxious determination*, *tired tenderness*,
*bitter amusement*, *cornered calculation*. Production-team practice
finds the model renders layered states better than single registers
when the layering is described as *one channel modulating another*:
the dominant state plus the underlying state plus the visible tell.

- **Anxious determination** — set jaw + locked gaze (determination)
  with shallow chest breath and a single hand at the side flexing
  open-closed (anxiety underneath).
- **Tired tenderness** — soft micro-smile + half-closed eyes
  (tenderness) with the body weight settled, slow blink interval
  (tiredness underneath).
- **Bitter amusement** — one-sided smirk + eye-shine (amusement)
  with no smile crinkles at the eye corners (bitterness underneath).

Compose layered states by stacking decomposed physical realizations
from the single-axis catalog. The dominant state goes in the face;
the underlying state goes in breath, posture, and hand-state; the
visible tell sits in the eyes.

For finer control, layer a **tiny detail** on top of an existing
emotional cue: `Roco is very upset, and his lower lip trembles`.
The base emotion gets the broad performance; the tiny detail gives
the model a specific physical cue to render. Production-team
discipline holds that the model renders the simple-emotion-plus-
tiny-detail compound better than either an over-decomposed prompt
or a too-generic one.

---

## Identity vs. Motion Separation Rule

When a prompt involves Soul ID or any character who must stay consistent across shots,
**always split the output into two clearly labeled blocks**:

### Identity Block — Static visual descriptors ONLY
- Face features, skin tone, body type, distinguishing marks
- Clothing, accessories, color palette
- NO motion, NO camera, NO temporal language

### Motion Block — Temporal and camera ONLY
- Camera movement, action choreography, speed
- Environmental motion, atmospheric changes
- NO character appearance repetition

**Bad (mixed) — identity drifts:**
```
A woman with sharp cheekbones and auburn hair in a blue trench coat runs through
a rain-soaked alley, her coat flapping, sharp cheekbones catching the neon light,
camera chasing her at full speed, her auburn hair streaming behind her.
```

**Good (separated) — identity stays locked:**

**Identity Block:**
```
The Soul ID character — sharp cheekbones, auburn hair shoulder-length,
wearing a blue trench coat with silver buttons, lean athletic build.
```

**Motion Block:**
```
She runs through a rain-soaked alley, coat flapping behind her.
Camera: Action Run — low behind, matching pace.
Neon reflections streak across wet concrete.
Style: Cinematic, cold blue shadows, warm neon accents. 16:9.
```

**When to apply this rule:**
- Always when Soul ID is active
- Always in multi-shot sequences where the same character appears
- Always when camera movement is involved alongside a character
- In Cinema Studio, identity goes in the @ Element definition; motion goes in the prompt

> **Camera matches emotion, not just identity.** The Motion Block describes WHAT
> the character does and HOW the camera moves. The *quality* of the camera motion
> — jittery handheld for anger, smooth handheld breathing for calm, static + slow
> push for revelation — should track the focal character's emotional state. See
> `../higgsfield-camera/SKILL.md` § Camera-Emotion Sync for the 6-emotion movement
> map and the emotional-arcs-within-a-shot pattern. For decomposing the underlying
> generic emotion before picking a camera prescription, see § Generic-Emotion
> Decomposition above.

---

## Common Prompt Mistakes

| Mistake | Fix |
|---------|-----|
| Re-describing the image in I2V | Only describe what changes/moves |
| Generic camera language | Use exact preset names |
| No style specified | Always include visual style + color grade |
| Too many actions in one shot | Split into separate generations and chain them |
| Contradictory movements | Don't combine Dolly In + Dolly Out in same shot |
| Prompt over 512 chars (Cinema Studio) | Cut text, reduce @ tags, use pronouns |
| Describing impact before action | Just describe the action, let AI render the result |
| Specific martial arts moves | Use general fighting energy instead of named moves |
| Multiple @ Elements in action scenes | Use @ for static scenes, plain text for action |
| Mixing identity + motion in one block | Separate into Identity Block + Motion Block (see above) |
| Aspect ratio inside the prompt body | Set aspect in the Higgsfield UI / output-format header. Describe framing in plain language ("full body" / "chest-up" / "wide establishing") not numerical ratios. |

> **Negative constraints:** For a comprehensive list of artifacts to avoid (floating limbs,
> face warping, flickering textures, etc.) and the prompt phrasing to prevent them, see
> `../shared/negative-constraints.md`. Always check the relevant categories for your prompt type.

---

## The Iteration Rule — Change One Variable at a Time

When a prompt is close-but-not-right and you're about to regenerate, change
**exactly one variable** per attempt. Subject detail, composition, motion
behavior, lighting, or style — pick the one that's wrong, change only that,
regenerate.

**Why it matters:** if you change two variables and the result improves, you
don't know which change drove the improvement. If the result regresses, you
don't know which change broke it. Either way you've spent a generation and
learned nothing about the prompt. Single-variable iteration gives every
regeneration a clean cause-and-effect signal — you keep what works, drop what
doesn't, and converge on the right prompt fast.

**The exception:** once the prompt is locked and you're varying purely for
stylistic exploration (e.g., five lighting variants of an already-approved
scene), batching changes is fine. The rule applies during *refinement*, not
during fan-out.

**Workflow:**

1. Generate the baseline.
2. Identify what's wrong — pick **one** specific thing.
3. Change only that variable in the prompt; leave everything else untouched.
4. Regenerate.
5. Compare against the baseline — did the targeted change move the result the
   way you expected?
6. Lock that change. Identify the next problem. Repeat.

If you find yourself wanting to "fix everything at once," stop and ask which
fix matters most. That one goes in this regeneration; the rest wait their turn.

### Prompt-window hygiene

Iteration also accumulates clutter — old prompt edits that no longer apply,
stale reference images attached from earlier shots, contradictory clauses
layered atop one another, prompts that have grown so long the model loses
the load-bearing pieces inside the noise. Four hygiene patterns from
production practice:

- **Delete obsolete prompt blocks.** When a previous prompt section was about
  the sticky-note prop but you've moved to character generation, delete the
  sticky-note block. Otherwise the model occasionally pulls the stale prop
  into the new generation.
- **Editor-adds-atop-existing-prompt creates contradictions.** When edits
  accumulate by appending rather than replacing, the prompt collects
  contradictory clauses (`tight close-up` from the old version, `wide
  establishing` from the new one). Symptom: output degrades into model-confusion
  artifacts. Counter: when iterating, replace the relevant clause in place
  rather than appending a new one.
- **Remove stale reference images.** When assets change between shots (the
  Polaroid was on the fridge in shot 1 but pulled off in shot 2), remove the
  now-stale reference from the prompt window so the model is not still
  trying to place it.
- **Prompt-overload sanitize pass.** When the prompt has grown beyond ~2-3k
  characters from accumulated detail, ask Claude (or whatever prompt-
  construction surface you use) to **optimize / study the context / sanitize
  the prompt** — consolidate redundant clauses, drop now-obsolete
  qualifiers, preserve the load-bearing structure. The sanitize pass keeps
  the prompt inside the cap and inside the model's effective attention
  window.

### When You Don't Know What's Wrong Yet — the 6-Pass Diagnostic Sequence

The Iteration Rule above assumes you can identify which one variable to change.
When you can't — the prompt produces output that's vaguely off and you can't
name why — run the 6-Pass Diagnostic Sequence to find it. Each pass isolates
one variable, in order, and tests it before moving on.

The order is not arbitrary. Subject and action carry the heaviest token weight
(early-prompt positioning); camera and style come next; audio and output
controls sit at the periphery. Diagnosing in this order surfaces the highest-
leverage problem first and stops you from chasing a style-pass fix when the
real issue was the subject description three layers up.

| Pass | Variable | Question |
|------|----------|----------|
| 1 | Subject | Is the character / object / focal element described unambiguously? |
| 2 | Action | Is the action concrete (physics-based) and singular for the shot? |
| 3 | Camera | Is the camera move named (Director Panel preset or specific verb), not implied? |
| 4 | Style | Is the look anchored (palette, grade, lens, lighting), not adjective-only? |
| 5 | Audio | If audio is part of the output, is it described as a parallel track with concrete sounds? |
| 6 | Output | Are aspect ratio, duration, and resolution set deliberately for the shot's needs? |

**How to use it:** start at Pass 1. If the result improves when you sharpen the
subject, you've found your variable — return to the Iteration Rule loop and
keep going. If Pass 1 doesn't move the result, lock the subject, advance to
Pass 2, and so on. The sequence is a finder, not a refinement loop. Once you
know which variable is wrong, the Iteration Rule takes over.

**Don't run all six passes blindly.** Six regenerations cost six credits. The
sequence's value is the *order* — most prompt failures land on Pass 1 or Pass 2
because early-prompt tokens dominate. If you reach Pass 4 without moving the
result, the prompt may need a structural rewrite, not iteration.

---

## Seedance 2.0 Prompting Best Practices

These best practices apply to Cinema Studio 3.0's generation engine (Business/Team plan) and complement the MCSLA formula above. They are not a replacement — use MCSLA as the primary framework, then apply these refinements.

> For the user-intent layer that sits above MCSLA — what working mode
> you're in (Exploration / Continuation / Bridging / Repair) and how each
> routes through Seedance's prompt modes — see
> `../higgsfield-seedance/SKILL.md` § Working Modes. The disambiguation
> between working modes and prompt modes lives in the same file,
> immediately above.

### Intent over Precision

Tell the model WHAT you want and HOW it should FEEL, not every micro-detail. Short prompts (30–100 words) consistently outperform long ones. The model is an AI director you collaborate with, not a render engine you command.

### The Director's Formula → MCSLA Mapping

The Director's Formula maps directly to MCSLA:

| Director's Formula | MCSLA Layer | Priority |
|-------------------|-------------|----------|
| Subject | S (Subject) | First 20–30 words (early tokens carry heavy weight) |
| Action | A (Action) | First 20–30 words |
| Scene | — (Context) | Supporting detail |
| Camera | C (Camera) | After subject + action |
| Style | L (Look) | After camera |
| Constraints | — (Guardrails) | End of prompt |

**Key insight:** Subject + Action should appear in the first 20–30 words of every prompt. Early tokens carry disproportionate weight in the generation engine.

### Genre Router — Prompt Length & Lead-With Targets

Different genres perform best with different prompt lengths and lead elements:

| Genre | Lead With | Target Length | Example Lead |
|-------|-----------|---------------|-------------|
| Product / E-commerce | Subject | 30–50 words | "A matte-black wireless earbud case rotates slowly on a marble pedestal..." |
| Lifestyle / Social | Action | 40–60 words | "She reaches for the coffee mug, steam curling upward..." |
| Drama / Narrative | Scene | 60–100 words | "Rain hammers a narrow Tokyo alley at 2 AM, neon signs reflecting in puddles..." |
| Music Video | Style | 50–80 words | "Anamorphic flares, crushed blacks, 16mm grain..." |
| Landscape / Travel | Scene | 30–60 words | "Dawn breaks over a volcanic ridge, mist pouring through the caldera..." |
| Commercial / Brand | Style | 40–70 words | "Clean white studio, soft even lighting, product hero moment..." |
| Anime / Artistic | Style | 50–90 words | "Cel-shaded lines, saturated palette, Studio Ghibli cloud physics..." |

### Anti-Slop Vocabulary

Kill these words — they add zero information and waste tokens:

| Slop Word | Replace With |
|-----------|-------------|
| beautiful | (delete — describe the specific visual instead) |
| stunning | (delete — describe what makes it striking) |
| epic | large-scale, sweeping, towering |
| amazing | (delete — show, don't tell) |
| dynamic | fast-tracking, whip-pan, handheld |
| energetic | sprinting, jumping, arms pumping |
| cinematic camera movement | slow dolly push / crane up / tracking shot |
| cool transition | match-cut / whip pan / smash cut |

### Physics Language

Use concrete physics consequences instead of mood words. The model responds to observable, physical details:

- ~~"powerful punch"~~ → `fist connects, sweat flies off in slow motion, opponent's head snaps back`
- ~~"dramatic entrance"~~ → `door slams open, dust erupts from the frame, light floods the dark room`
- ~~"fast car"~~ → `tires spin, gravel sprays backward, chassis drops as acceleration kicks in`

### Degree Adverbs

The model cannot infer intensity from images alone. Use adverbs to guide interpretation:

`slowly`, `dramatically`, `violently`, `gently`, `frantically`, `deliberately`, `cautiously`, `explosively`

**Example:** "She turns **slowly**, eyes narrowing **deliberately**, then **explosively** lunges forward."

### Three-Act Rhythm for Action

Every action prompt should follow this arc:

1. **Charge-up** — tension builds, energy gathers
2. **Burst** — the action explodes
3. **Aftermath** — physics consequences play out

**Example:** "The fighter plants her feet, fists clenching (charge-up). She throws a spinning kick that connects with the sandbag (burst). The bag swings violently, chain rattling, sand dust puffing from the seams (aftermath)."

### No Negative Prompts

Cinema Studio 3.0's generation engine does not support negative prompt syntax. Do not write "no blur" or "avoid shaky camera." Instead, use positive constraints — describe what you WANT:

- ~~"no shaky camera"~~ → `locked-off static camera, no movement`
- ~~"no blur"~~ → `sharp focus throughout, deep depth of field`
- ~~"don't make it dark"~~ → `bright, evenly lit, overcast daylight`

### Audio as First-Class Element

Describe audio separately in prompts. BGM, ambient SFX, and dialogue are handled as parallel tracks via dual-channel stereo generation:

```
A barista grinds coffee beans, pours steaming water over the filter.
Camera: tight close-up, slow dolly across the counter.
Style: warm tones, shallow depth of field.

Audio: the whir of the grinder, water bubbling through the filter,
ceramic mug placed on a wooden counter with a soft clink.
Soft jazz piano in the background, barely audible.
```

Sound design descriptions like "the scratch of frosted glass, rustling plush fabric, gentle tapping on acrylic" directly influence the generated audio output.

---

## Seedance 2.0 Scene Archetype Router

Before writing a Seedance prompt, identify which archetype the scene fits. The archetype dictates camera behavior, spatial logic, and what changes across time. This is a planning layer **on top of** MCSLA — pick the archetype first, then fill in MCSLA.

### Action Archetypes

| Archetype | Camera focus | Space dynamic |
|-----------|-------------|---------------|
| **Pursuit** | Distance closing/opening. Pursued ahead in frame, pursuer behind | Path narrows/opens |
| **Duel** | Camera lower on dominant side; dominance MUST alternate | Fighters trade position |
| **Impact** | Build-up slow → hit fast → aftermath slow | Point of contact = center |

**Decision tree:** Chase? → Pursuit. Two opponents trading advantage? → Duel. Single decisive contact moment? → Impact. None → default Duel.

**Duel rule:** neither side dominates more than one consecutive beat. If one fighter dominates the whole scene, describe it as a one-sided assault, not a duel.

### General Archetypes

| Archetype | What changes | Camera signature |
|-----------|-------------|-----------------|
| **Journey** | Position in space — road, flight, walking | Tracking, aerial, traveling alongside. Landscapes pass. |
| **Atmosphere** | Nothing — mood IS the content. Rain on glass, empty street. | Minimal movement. Slow push-in or static hold. Micro-changes carry all drama. |
| **Reveal** | Hidden → visible. Door opens, fog lifts, camera rounds corner. | Pan, crane, dolly reveal. Camera controls WHEN viewer sees the subject. |

**Decision tree:** Subject moves through space? → Journey. Something hidden becomes visible? → Reveal. Nothing changes, mood is the content? → Atmosphere. None → default Atmosphere.

### Dialogue Archetypes

| Archetype | Power dynamic | Camera signature |
|-----------|--------------|-----------------|
| **Confrontation** | Shifting — both push. Dominance trades per exchange. | Tight OTS, camera crosses axis on power shift. |
| **Interrogation** | Asymmetric — one extracts, one resists. | Low-angle on questioner, push-in on silence. |
| **Negotiation** | Balanced — both need something. | Symmetrical framing, matching shot sizes. |

**Decision tree:** Both pushing, dominance trading? → Confrontation. One extracting, one resisting? → Interrogation. Both need something, balanced? → Negotiation. None → default Confrontation.

**Dialogue word limit:** ~25–30 spoken words fit into 15 seconds. If the user provides more, keep the line where dominance flips (the power-shift exchange), 1 line before (setup), 1 line after (reaction). Convert the rest to physical behavior.

---

## Seedance 2.0 Engine Constraints

These are hard rendering constraints of the Seedance 2.0 engine — violating them causes broken output regardless of prompt quality.

### Character & spatial rules
- **≤ 3 characters tracked across cuts.** Name the acting pair and interaction vector per shot. More than 3 and Seedance loses track of identities.
- **Exit-frame = implicit cut.** Once a character leaves frame, they are gone for the remainder of that shot. Never choreograph exit + re-entry in the same continuous shot.
- **Off-screen = nonexistent.** State changes must be shown on camera before being referenced. Don't reference injuries, prop changes, or position shifts that happened off-screen.
- **Spatial continuity breaks on cuts.** Re-anchor positions and facing direction after any cut. State movement direction explicitly ("moving left-to-right").
- **Avoid reflection shots** (blades, puddles, mirrors) — Seedance breaks scene geography when rendering reflections.

### Sensory rules
- **Only describe what can be seen or heard.** No smell, taste, or internal thoughts.
  - ❌ "The air smells of pine." ✅ "Pine needles covering the ground, wind moving through branches."
- **Micro-expressions work as physics.** ✅ "jaw clenches, nostrils flare." ❌ "looks angry."

> For the eight named substrate channels that micro-expressions
> decompose into, see `../../vocab.md` § Emotion as Visible Behavior —
> Channels.

### Action rules
- **Intent + named technique, not biomechanics.** ✅ "spinning back kick connects." ❌ "left forearm rotates 45° to deflect the incoming hook at wrist level." If the user names a move, preserve it. If they describe joint mechanics, compress to the move's intent.
- **Force and direction, not destruction sequence.** ✅ "driven into the car, metal buckling." ❌ "thrown into side door, glass shatters, uses rebound to sweep leg."

### Double-contrast cut rule (mandatory)

Every cut must change **both** shot size AND camera character. The scale runs `extreme wide → wide → medium → MCU → close-up → ECU`. Camera character: `Handheld | Static | Stabilized tracking | Crane | Aerial` — never repeat across a cut.

**Bad (same camera character):** MS handheld → CU handheld
**Good (both change):** MS handheld → ECU static-locked

### Inserts — causally motivated, named subject

Inserts are sub-second (0.3–0.5s) dramatic punctuation at any shot size. Rules:
- **No story beats** — inserts are static moments only
- **Causally motivated** — the viewer must understand WHY they see this detail. Hero slammed onto hood → HIS hand gripping metal. Not: generic boot in a puddle.
- **Name the subject** — specify WHOSE body part or detail. Without attribution, Seedance renders wrong content.
- **Obey double contrast** — inserts still follow the cut rule.

### Age-blind character rule

Never describe characters by age in Seedance prompts. Trigger words to avoid: *boy, girl, child, kid, young, teen, little*. Seedance age inference is unreliable and drifts across shots.

- **With image input:** describe by **role** (rider, figure, traveler, speaker), **clothing**, and **action**. Never label who they are — label what they do.
- **Without image input:** use functional labels: "a figure in a wool cloak," "a silhouette against the horizon."

### Default: in medias res

Scenes start already in progress unless the user explicitly says "starts with…" or "ends with…". Don't waste the first 2 seconds on setup beats.

> Full Seedance director reference including bilingual EN+ZH JSON output format is dropped in the project `docs/` folder as `Seedance 2 Skill.md` — use it when you need the standalone director-mode prompt with scene-archetype routing and age-blind rules baked in.

---

## Related skills
- `higgsfield-soul` — Character consistency, Soul ID, micro-expressions
- `higgsfield-camera` — All named camera controls
- `higgsfield-style` — Visual styles, color grades, lighting
- `higgsfield-models` — Model selection
- `higgsfield-troubleshoot` — Fix failing generations
- `templates/` — Annotated genre-specific prompt templates
