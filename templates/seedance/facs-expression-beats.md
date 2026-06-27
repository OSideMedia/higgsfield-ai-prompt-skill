# Template: FACS Expression-Beat Schedule

Paste-ready Seedance 2.0 prompt template for close-up facial acting driven by
**FACS Action Unit codes** — one AU set per beat. Full method, the AU reference
table, and the emotion→AU recipes live in
`../../skills/higgsfield-facs/SKILL.md`.

## When to use this template

Close-up shots where the *face* is the content — monologue, dialogue, a forced
smile, a mixed/uncanny expression, an emotion arc across a single continuous
take. Not for shots where blocking or whole-body action dominates (use
`single-character-position.md` for those).

> **Plan first.** Decide the 3–4 expressions the beat needs *before* writing —
> stacking more AUs degrades accuracy. See `higgsfield-facs` § The Plan-First
> Workflow.

## Prompt template

```
**Model:** Seedance 2.0
**Aspect ratio:** [1:1 / 16:9 / 9:16]   **Duration:** [Ns]

[Use the provided character @Image1 as the fixed identity reference. — optional,
 only for identity consistency; codes work without an image]

**Style & Mood:** [framing — tight close-up, face + shoulders], [lighting],
[background], shallow depth of field, [mood].

[Optional dialogue — generates speech + automatic lip-sync, see higgsfield-audio
 § Audio as a Conditioning Input:
 [AUDIO: 0s] "[the spoken line]"]

Beat 1 ([0-Xs]): [AU codes] ([optional short anatomical description]) [— delivers "<line>"]
Beat 2 ([X-Ys]): [AU codes] (...) [— delivers "<line>"]
Beat 3 ([Y-Zs]): [AU codes] (...) 
[3–4 beats max for reliable rendering]

[One-line mood / subtext — e.g. "the face never fully commits to either; the
 audience reads both at once."]

**Camera:** [one dominant move — slow push-in / static medium close-up]
```

## What goes in each field

- **AU codes** — from `../../skills/higgsfield-facs/SKILL.md` § AU Code Reference.
  Specify **codes-only** (`AU12`) for terse beat lists, or **codes + short
  anatomical description** for any unit the model keeps dropping — test both.
- **Emotion → AUs** — for "which code for anger/fear/sadness," see
  `higgsfield-facs` § Emotion → AU Recipes (Duchenne smile = AU6+AU12, sadness =
  AU1+AU4+AU15, etc.). Blend two emotions' AUs in one beat for mixed expressions.
- **Beats are expression changes within a continuous close-up, not cuts.** Keep
  the camera move singular so Seedance doesn't read the schedule as a shot list.
  Beat time ranges must sum to **Duration** (`higgsfield-seedance` § Runtime
  arithmetic).
- **Dialogue beats** — the `[AUDIO: Xs]` block drives lip/jaw phoneme shaping;
  reserve your explicit AU schedule for the expressive brow/eye/cheek muscles
  around the words.

## See also

- `../../skills/higgsfield-facs/SKILL.md` — full FACS method, AU table, emotion
  recipes, worked examples, the not-a-guarantee provenance rule
- `../../skills/higgsfield-audio/SKILL.md` § Audio as a Conditioning Input —
  `[AUDIO: Xs]` dialogue + lip-sync
- `../../skills/higgsfield-soul/SKILL.md` § Micro-Expressions — named expressions
  that decompose to AU combos
- `single-character-position.md` (sibling template) — when blocking, not the
  face, is the content
