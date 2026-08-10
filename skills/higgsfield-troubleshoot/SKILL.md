---
name: higgsfield-troubleshoot
description: >
  Use when a Higgsfield generation fails, produces poor quality, looks wrong,
  doesn't match the prompt, or the user needs to fix or improve an output.
user-invocable: true
metadata:
  tags: [higgsfield, troubleshoot, fix, quality, failure, improve]
  version: 3.2.0
  updated: 2026-08-09
  parent: higgsfield
---

# Higgsfield Troubleshooting Guide

## QUICK FACTS
*Generated-checked block (scripts/build_index.py verifies anchors). Read the linked sections for full context — these lines are routing aids, not the rules themselves.*
- Face inconsistency, dead camera moves, ignored prompts, static i2v, blocked dark content — the per-problem fix list [→](#common-problems-fixes)
- Kling 3.0 Motion Control failures are almost always upstream of the prompt: reference clip, character image, or orientation/scene-source settings [→](#motion-control-failures-kling-30)
- Pre-generation checklist: subject, action, named camera preset, style, grade, aspect, <200 words (short-form regime) [→](#pre-generation-checklist)
- Seedance/Cinema Studio symptom table + diagnostic flowchart: blurry = overspecified; chaotic camera = One-Move Rule violated; wrong character = prompt re-describes the reference [→](#cinema-studio-30-seedance-20-diagnostic-tree)
- Every delivered take gets ONE of five verdicts before anything re-fires: keep / fix-in-post / edit / re-roll / rewrite [→](#take-triage-five-verdicts-for-a-delivered-take)
- Two takes with the same flaw = rewrite, by rule; different flaws per roll = stochastic → batch-and-cull, not rewrite [→](#take-triage-five-verdicts-for-a-delivered-take)
- Re-roll = same prompt again, unchanged — no seed parameter on this surface; every roll is a fresh sample [→](#take-triage-five-verdicts-for-a-delivered-take)
- Change exactly one variable between takes so causality stays readable [→](#one-variable-per-retake)
- Declare the take budget AND a written "good enough" bar before take one; half-budget with no progress forces a strategy change [→](#attempt-budget-declared-before-take-one-heuristic)
- The shot log is the ledger row — one line per take, changed variable in `notes` [→](#the-shot-log-is-the-ledger-row)
- Continuation/extension defects: 12-row symptom → cause → single-repair-variable atlas (planned-vs-observed opening, motion-vector drop, prop contradictions, chain-depth drift…) [→](#sequence-continuation-failure-atlas)
- Retry Ladder: 4 terminating rungs — re-run once verbatim → treat 2nd failure as over-packing → switch model for that shot → stop after 3 paid attempts with named options [→](#retry-ladder-a-failed-take-edits-the-plan-not-just-the-dice)
- Log EVERY confirmed fix to learning memory, and check memory first before troubleshooting [→](#log-the-outcome-always)
- Vision-grounded diagnosis (stills only): vision proposes the `reject_reason`, the human confirms — advisory until a class clears the agreement gate [→](#vision-grounded-diagnosis-classify-the-rejected-still-dont-guess)

## Common Problems & Fixes

### Problem: Character face is inconsistent or morphing
**Cause:** No Soul ID reference; prompt has conflicting appearance descriptions
**Fix:**
- Create a Soul ID reference and use it in subsequent generations
- Remove any appearance descriptions that contradict each other
- For image-to-video: don't re-describe the face — let the input image carry it
- Use Kling 3.0 for best character consistency (or Kling 2.6 if no audio needed)

---

### Problem: Camera movement isn't working / is generic
**Cause:** Camera described vaguely, not using exact preset names
**Fix:**
- Replace generic descriptions with exact preset names: "Dolly In", "FPV Drone", "360 Orbit"
- Put the camera instruction on its own line or clearly labeled: "Camera: [name]"
- Don't describe what the camera is doing in prose — name the control directly

---

### Problem: Prompt is ignored / output doesn't match
**Cause:** Prompt too long, conflicting instructions, over-specified
**Fix:**
- Cut prompt to under 200 words — trim the least essential details (short-form prompts only; block-scaffold production briefs are a different regime — root `SKILL.md` HARD RULE 8)
- Remove any contradictory elements (don't say both "moving fast" and "frozen in place")
- Lead with the most important element: Subject → Action → Camera → Style
- Split complex scenes into multiple separate generations

---

### Problem: Visual style looks wrong / generic
**Cause:** No style specified, or style description too vague
**Fix:**
- Add one of the named styles: Cinematic / VHS / Super 8MM / Anamorphic / Abstract
- Add a specific color grade description: "cold teal and orange", "warm golden amber"
- Specify aspect ratio: 16:9 / 9:16 / 2.35:1
- Add lighting: "golden hour", "neon", "practical only", "overcast"

---

### Problem: Motion preset effect isn't visible
**Cause:** Preset not explicitly named, or scene context doesn't support the effect
**Fix:**
- Name the preset exactly as it appears in the library: "Apply Explosion preset"
- Place the preset instruction at the end of the prompt, clearly labeled
- Make sure the scene context supports the preset — e.g., Animalization needs a subject
  who can logically transform

---

### Problem: Image-to-video barely moves / is static
**Cause:** Prompt re-describes the static elements instead of what should animate
**Fix:**
- Only describe what **changes or moves** — not what is already visible in the image
- Add an explicit camera movement: "Camera: Dolly In" or "Camera: slow Arc"
- Specify the motion type: "hair gently lifts", "eyes blink", "she turns slowly left"
- Add atmospheric motion: "dust floats upward", "light flickers", "steam rises"

---

### Problem: VFX preset looks too artificial / cartoonish
**Cause:** Wrong model for the preset, or prompt style conflicts with effect
**Fix:**
- For grounded presets (Explosion, Freezing): use Kling 3.0 or 2.6 for realism
- For stylized presets (Animalization, Multiverse): use Wan 2.5 — leans into the style
- Add "photorealistic", "physically accurate", "cinematic quality" to the prompt

---

### Problem: Product shots look cheap or over-lit
**Cause:** No lighting specification, background too plain
**Fix:**
- Specify the background surface: "raw concrete", "warm wood grain", "black velvet"
- Add specific lighting: "soft side-light", "overhead product lighting", "practical only"
- Add texture cues: "camera reveals material grain", "surface catches light on edges"
- Use Nano Banana Pro for maximum image sharpness on product images

---

### Problem: Horror/dark content getting blocked
**Cause:** Platform safety filters triggering on explicit content
**Fix:**
- Describe outcomes rather than explicit acts: "aftermath", "tension", "dread"
- Use atmosphere language: "unsettling", "wrong", "something is off"
- Use the motion presets for horror effects rather than explicit descriptions
- Avoid direct descriptions of injury, gore, or explicit threat

---

## Motion Control Failures (Kling 3.0)

When a Kling 3.0 Motion Control generation comes back wrong, the cause is almost
always upstream of the prompt — the motion reference clip, the character image,
or the orientation/scene-source settings. Walk this list before you regenerate.

| Symptom | Root cause | Fix |
|---------|-----------|-----|
| Output suddenly jumps or snaps mid-clip | The motion reference contains a hidden cut, dissolve, or hard transition | Re-trim the reference to a single continuous shot. If the source clip can't be cleaned up, reshoot or pick a different reference |
| Output is shorter than the reference clip | The source motion is too fast or too dense for clean transfer | Slow the source (50–75% playback baked in), reshoot at a calmer pace, or pick a reference with simpler motion |
| Character face drifts or warps across the clip | The character image doesn't have a clearly readable face — bad framing, low light, or the face is too small in frame | Re-shoot or re-generate the character image with closer framing, even lighting, and a neutral or slight expression |
| Body motion looks correct but the face is dead or frozen | Wrong orientation mode for the shot — Image Orientation when you needed Video Orientation, or vice versa | Switch modes: Video Orientation for full-body movement (dance, action); Image Orientation for camera-driven shots with a mostly static body. Regenerate |
| Generated character feels detached from the environment | Scene source is set incorrectly — pulling the wrong background | Decide whether the environment should come from the motion video or the character image, then set Scene source accordingly |
| Motion transfers but identity drifts across the clip | The character image isn't full enough — head or body is cut off, or framing is too tight to anchor identity | Re-upload a character image that shows both head AND body fully; this is what Element Binding needs to keep the face stable through movement |

> For the full Motion Control workflow and pre-flight input checklist, see `../higgsfield-motion/SKILL.md` → "Kling 3.0 Motion Control — When and How to Run It" and "Motion Reference Input Checklist".

---

### Problem: Audio/lip-sync not working or out of sync
**Cause:** Head motion tokens competing with lip engine, non-MP3 format, clip too long
**Fix:**
- Remove all head/face motion tokens (nodding, turning head, looking around)
- Keep dialogue clips 3–8s (not 15s — accuracy degrades)
- Use MP3 format only for Seedance 2.0 (when available) (WAV/AAC fail silently)
- Lock camera: medium close-up, static or slow Dolly In only
- One face per shot — multiple faces break audio routing
- For detailed audio guidance → `higgsfield-audio` skill

---

### Problem: Background music overrides uploaded dialogue
**Cause:** Ambient/music tokens in prompt invite generative audio engine to replace your audio
**Fix:**
- Add timestamp anchoring: "Audio @Audio1 plays exactly as uploaded from 0s to end"
- Remove ALL ambient/SFX/music tokens from the prompt
- Keep the prompt focused on visual description + dialogue only

---

## Pre-Generation Checklist

Before generating, verify:

- [ ] Subject described clearly (who/what)
- [ ] Action described specifically (what happens)
- [ ] Camera named with exact preset name
- [ ] Visual style specified (Cinematic / VHS / etc.)
- [ ] Color grade or lighting mentioned
- [ ] Aspect ratio included
- [ ] Model selected (or let Higgsfield default)
- [ ] Prompt is under 200 words (short-form regime — skip for block-scaffold briefs)
- [ ] No conflicting instructions
- [ ] Soul ID referenced if character consistency needed
- [ ] Motion preset named at end if using one
- [ ] Identity Block separated from Motion Block (if Soul ID active)

---

> **Full negative constraints reference:** For a comprehensive, categorized list of all
> generation artifacts and the prompt phrasing to prevent them, see
> `../shared/negative-constraints.md`. This troubleshooting guide covers diagnosis and fixes;
> the shared constraints file covers prevention.

---

## Cinema Studio 3.0 / Seedance 2.0 Diagnostic Tree

> These diagnostics apply to Cinema Studio 3.0's generation engine (Business/Team plan only). For Cinema Studio 2.5 issues, see the general troubleshooting section above.

### Quick Diagnostic

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Output blurry, jittery, or morphing | Overspecification — prompt too long or too detailed | Short-form: cut to 30–100 words; use @reference images/videos instead of 50+ words of description. Block-scaffold briefs: don't shorten — tighten structure instead (one axis per clause, HARD RULE 8 regime) |
| Camera chaotic, spinning, or jittering | Violated the One-Move Rule — multiple camera moves in one shot | Rewrite to ONE primary camera move per shot. Use Cinema Studio 3.0's Smart mode, or split into multi-shot |
| Character doesn't match reference | Prompt is re-describing the character's appearance | Delete ALL physical descriptions. Describe ONLY action and emotion. The @reference carries identity |
| Action stiff or lacking impact | Missing intent/physics language | Add degree adverbs (`violently`, `gently`, `explosively`) and physics consequences (`dust erupts`, `sparks fly`, `fabric tears`) |
| Output "not what I wanted" (vague) | Ambiguous prompt with subjective language | Run Anti-Slop Check: replace `beautiful`, `stunning`, `epic`, `amazing`, `dynamic` with observable, measurable details |
| Audio not matching video | Audio description conflicting with visual description, or uploaded audio being overridden | Use timestamp anchoring for uploaded audio. Remove ambient/SFX tokens when using @Audio references |

### Diagnostic Flowchart

```
Output bad?
├── Blurry/morphing → Is it a short-form prompt > 100 words?
│   ├── Yes → Cut to 30–100 words, use @reference
│   │        (block-scaffold briefs: tighten structure, never truncate)
│   └── No → Too many action beats? (>2 per 5s) → Split into multi-shot
├── Camera wrong → How many camera moves specified?
│   ├── Multiple → Reduce to ONE move (One-Move Rule)
│   └── One → Try Smart mode instead, or use @Video camera transfer
├── Character wrong → Does prompt describe character appearance?
│   ├── Yes → Delete appearance, keep only action/emotion
│   └── No → Use better reference (frontal + 3/4 + profile shots)
├── Action weak → Does prompt have physics language?
│   ├── No → Add degree adverbs + physical consequences
│   └── Yes → Reduce beat density (1–2 beats per 5s)
└── Just bad → Run Anti-Slop Check
    ├── Found slop words → Replace with specific observables
    └── Clean → Try different genre setting, or use @reference
```

### Success Rate Note

Cinema Studio 3.0's generation engine produces ~90% usable output. If outputs are **consistently** bad across multiple attempts, the prompt is almost certainly the problem — not the model. Apply the diagnostic tree systematically before regenerating.

---

## Take Triage — Five Verdicts for a Delivered Take

`[FIELD — community, Emily2040/seedance-2.0 skill (MIT), re-derived 2026-08-09]`
The sections above repair outright failure. Most real takes land in between —
partially good — and the expensive habit is treating every flaw as a
regeneration. Before anything re-fires, every delivered take gets exactly one
of five verdicts:

| Verdict | When | Next move |
|---------|------|-----------|
| **Keep** | The thing this shot is FOR is delivered and nothing is fatal | Lock it, log it, move on. Perfection in secondary details is post's job |
| **Fix in post** | The flaw lives in the editor's domain: color, on-screen text, sound mix, trim, a few unstable frames at the ends | Never burn takes on what an edit fixes in minutes |
| **Edit, don't regenerate** | Composition and timing are right; exactly one layer is wrong and an edit surface supports it | Repair only the failing layer — the editor-not-regenerator mindset (`../higgsfield-seedance/SKILL.md` § Keyframe Workflow; `../higgsfield-pipeline/SKILL.md` Pipeline E Stage 2) |
| **Re-roll** | The prompt is right; the sample was unlucky | Same prompt again, unchanged — every roll is fresh on this surface (no seed parameter; `../higgsfield-seedance/SKILL.md` § Drafts Validate the Prompt, Not the Take). With enough ledger history, let the fork verdict decide iterate-vs-batch instead of eyeballing (`higgsfield-recall` § Read the verdict) |
| **Rewrite** | The same flaw appears in two takes | Systematic, not luck — **two takes with the same flaw = rewrite, by rule**. Diagnose (tables above; `../higgsfield-seedance/FAILURE-MODES.md`), change the prompt |

The rewrite tripwire cuts both ways: the same flaw twice means stop re-rolling
into the same wall, but *different* flaws on every roll mean the miss is
stochastic — that's batch-and-cull territory, not a rewrite
(`../higgsfield-prompt/SKILL.md` § Before You Iterate). When the verdict is
re-roll or rewrite and the failure keeps recurring, escalation is governed by
the Retry Ladder below.

### One variable per retake

Whatever the verdict changes — one prompt clause, OR the mode, OR one
reference — change exactly one thing between takes so causality stays
readable. Full mechanics: `../higgsfield-prompt/SKILL.md` § The Iteration
Rule — Change One Variable at a Time (and `DISCIPLINE.md` § Single-Variable
Iteration). The shot log below records *which* variable, per take.

### Attempt budget — declared before take one [heuristic]

Write two things down before the first fire:

- **A take budget** — a number, sized against the acceptance-rate reality in
  `../../production-benchmarks.md` (draft-tier exploration stretches it —
  § Drafts Validate the Prompt, Not the Take).
- **A written "good enough" bar** — the primary thing delivered, secondary
  flaws postable. Without it written down, the bar silently becomes
  "perfect," and no budget survives that.

At half the budget with no progress on the same flaw, stop iterating and
change strategy: a different mode, a shot split, or the Retry Ladder's rung-4
named options. Iteration without a stop condition is how a cheap shot becomes
an expensive one. The budget is not a promise of success — it is the tripwire
that forces the strategy change.

### The shot log is the ledger row

One line per take — what changed, what resulted — and the repo already has
the surface for it: the generation ledger (`../../db/ledger/`, § Log the
Outcome below, 5-second rule). Put the one changed variable in `notes`
("changed: lens lock line"); `prompt_hash` already dedupes identical
re-rolls. Two rows sharing a flaw is the rewrite tripwire made auditable —
re-reading the log beats re-living it.

---

## Sequence & Continuation Failure Atlas

`[FIELD — community, Emily2040/seedance-2.0 skill (MIT), re-derived 2026-08-09]`
Symptom → likely cause → single repair variable for chained work:
continuations, extensions, and start-frame-pinned handoffs. One repair
variable per retake — the one-variable rule applied to sequences. Handoff
mechanics live in `../higgsfield-pipeline/SKILL.md` § Continuation & Extension
Handoff; prompt templates in `../higgsfield-seedance/SKILL.md` § Continuation
Prompt Formula. This table is the symptom-side index into both.

| Symptom | Likely cause | Repair variable (change this one thing) |
|---------|-------------|------------------------------------------|
| Continuation opens from the *planned* ending, not the delivered one | Prompt written from the shot plan; the accepted take's actual end state was never reviewed | Rewrite the opening from what the parent clip actually shows — the source carries state, the prompt carries only the delta (`higgsfield-pipeline` § Source-carries-state rule) |
| Action restarts from the top | Completed beat never marked as already done | State the beat as completed ("the door already stands open") and prompt only what happens next |
| A later beat shows up early | Future-beat material leaked into this clip's prompt | Strip every future beat from prompt and endpoint — one clip owns one beat |
| Identity drifts across extensions | The chain tail displaced the canonical identity reference | Re-anchor from the ORIGINAL character refs, never a frame from the drifted tail (`higgsfield-pipeline` § Chain management) |
| Screen direction flips at the join | Axis never locked, or reset unintentionally | State the direction ("walks screen-left to screen-right") or declare the axis change as intentional coverage |
| Mid-flight motion stops dead | Open motion vector not carried across a still-frame handoff | Carry subject/camera speed and direction in prose — one of the three things a frame cannot carry (`higgsfield-pipeline` § Source-carries-state rule) |
| Camera move restarts from rest | Parent's camera-move phase missing from the prompt | Open from the observed camera phase ("mid-dolly, continuing in") |
| Prop contradicts the prior clip | Prop owner / position / condition not tracked across the handoff | Add a prop-state line (who holds it, where it sits, what condition); prop sheet for recurring props (`higgsfield-pipeline` Pipeline E Stage 3) |
| Dialogue repeats a delivered line | Audio phase not carried at the cut point | Mark the line as delivered and continue from the audio phase — a frame cannot carry it |
| Each extension looks worse than the last | Expected chain-depth drift — each generation re-ingests the previous one's artifacts | Re-anchor from canonical refs or cut intentionally; cap chains at 2 extensions, hard ceiling 3 (`higgsfield-pipeline` § Chain management) |
| A reference bleeds into the wrong role | Transfer / ignore clauses absent | Split the roles: per-image role line plus explicit exclusions (`higgsfield-seedance` § Reference Roles) |
| Too much happens; nothing lands | Several beats compiled into one prompt | Reassign future beats to later clips (`higgsfield-seedance` § Single-vs-multi-shot decision) |

A repair that works gets logged (§ Log the Outcome). Two takes failing on the
SAME row is the rewrite tripwire in § Take Triage — stop re-rolling into the
same wall.

---

## Retry Ladder — a failed take edits the plan, not just the dice

`[EMPIRICAL — MiniMax H3 skill corpus, re-derived]` When a take fails or drifts and the
diagnostic tree confirms the references and mappings were right, escalate in this order.
Each rung terminates — never loop on one rung:

1. **Re-run once, quoting the reference map verbatim.** The original role + exclusion
   lines, unedited. If the mapping was right, one clean re-roll is legitimate variance.
2. **Treat the second failure as evidence the shot is over-packed.** Shorten the
   envelope and/or split the surplus beats into a new adjacent prompt (the shotlist
   density split triggers apply), then re-run the preflight linter on **both** halves
   before firing either. A second identical re-roll pays twice for the same overload.
3. **Switch models for that one shot.** One shot on a different engine beats bending
   the whole piece around a shot the current engine won't hold.
4. **Stop after three paid attempts and present named options** — accept the best
   take, re-scope the shot, defer it, or ship with an explicit `placeholder: missing
   clip` note in the deliverable. Silent omission is never one of the options.

Log the rung that resolved it (§ Log the Outcome) — rung-2 resolutions are shotlist
authoring lessons, not generation luck.

---

## Log the Outcome — Always

Troubleshooting that isn't logged is troubleshooting the next session repeats.
After ANY confirmed fix from this skill, write it to the learning memory
(`../../scripts/higgsfield_memory.py`, databases in `../../db/`):

- **Filter workaround confirmed** (the rewritten prompt passed in a real
  generation): `python3 scripts/seedance_lint.py --confirmed "<prompt that passed>"`
- **Quality fix confirmed** (the improved prompt fixed motion / identity /
  blocking / audio): `python3 scripts/higgsfield_memory.py add-quality '<json>'` with
  `original_prompt`, `failure_description`, `improved_prompt`, `model_used` —
  then `update-quality <id> improved` once verified.
- **Outcome learned later** for an entry that already exists:
  `python3 scripts/higgsfield_memory.py update-filter <id> <fixed|workaround|still-blocked>`
- **Project-specific lessons**: add `--project <name>` to keep them scoped
  under `../../db/projects/` instead of global memory.

Before troubleshooting, also CHECK memory first — that's `higgsfield-recall`'s
job (`query-filter` / `query-quality`); the preflight's MEMORY RECALL section
does it automatically.

---

## Vision-Grounded Diagnosis — Classify the Rejected Still, Don't Guess

The `reject_reason` you log feeds the iterate-vs-batch fork (`higgsfield-recall`
§ Read the verdict). Logged from memory it's hearsay — "I think the face
drifted." When you can actually **see** the rejected output, classify it from the
frame instead of from recall. **This is an opt-in assist** ("diagnose this
rejected shot"), and it is **advisory**: vision *proposes*, the human *confirms*.

**Scope (v1): stills only** — an image, or a single representative frame the user
picks from a video. Full-clip motion failures (FPS drift, temporal de-dup,
multi-motion) are out of scope here; they need frame-by-frame review
(`../higgsfield-seedance/FAILURE-MODES.md`), not a single-frame classify.

**The chain:**

1. **Capture.** Get the still in hand. Local image → read it directly. Web URL →
   `media_import_url` (never pass a raw URL). Cowork local file → the upload
   widget. Outputs are not auto-saved, so capture is an explicit step.
2. **Classify against the `reject_reason` enum** (the table below). Note what you
   see in one line (the `vision_evidence`).
3. **No clean home → `other` + note.** Some visible failures (warped hand, FPS
   drift) have no exact enum value. Route to `other` with the evidence note;
   **never force-fit** a near-miss. If the `other` pile grows, that's the data
   that justifies a future enum-extension PR.
4. **Confirm, then log.** Surface the proposal — *"vision says `physics` (warped
   left hand, center frame); confirm or correct?"* — then:
   ```bash
   python3 ../../scripts/higgsfield_memory.py log-gen <project> --model <id> \
     --tags <shot_tags> --outcome rejected --reason <confirmed> \
     --vision-reason <proposed> --vision-evidence "<one line>"
   ```
   `--reason` is the human verdict (drives the fork); `--vision-reason` is the
   proposal (feeds the agreement gate). Logging both is what lets the tool learn.

**Mapping table — what vision sees → `reject_reason`:**

| Vision observes | reject_reason |
|---|---|
| face / identity changed vs reference | `identity-drift` |
| wardrobe or colour shifted vs reference | `wardrobe-contamination` |
| extra cuts / unwanted scene breaks | `extra-cuts` |
| staging or blocking broken | `blocking-broken` |
| flat / wrong performance | `performance` |
| wrong camera move | `camera-wrong` |
| physics or anatomy violation (incl. warped hand) | `physics` |
| garbled on-screen text | `text-render` |
| provider content-filter block | `filter-flagged` |
| bad framing / composition | `composition` |
| FPS drift, temporal de-dup, or **no clean home** | `other` + evidence note |

**Measure before trusting.** Vision is the fork's accuracy backstop only once
proven. `python3 ../../scripts/higgsfield_memory.py agreement <project>` reports, per
`reject_reason` class, how often the proposal matched the confirmed verdict. A
class is `trusted` (vision may be logged without confirmation) only above the
agreement gate over enough confirmed diagnoses; until then, confirm every one.

---

## Related skills
- `higgsfield-prompt` — MCSLA formula, prompt structure, Identity/Motion separation
- `higgsfield-recall` — Pre-generation memory check for past failures
- `higgsfield-models` — Model selection (wrong model = many quality issues)
- `higgsfield-audio` — Audio-specific failures and fixes
- `higgsfield-cinema` — Cinema Studio–specific issues (512 char limit, @ Element bugs)
- `higgsfield-pipeline` — Continuation & Extension Handoff mechanics (workflow side of the Sequence & Continuation Failure Atlas)
- `../shared/negative-constraints.md` — Prevention-focused constraint reference
