# Reference — Dialogue & beat timing for footage transforms

A timed camera move (crash zoom, push-in, reveal pull-back) only pays off if it lands on the
right frame. Seedance's internal timing drifts, so you anchor the move **twice**: once by
meaning (the spoken line or a visible action) and once by number (a second mark). This file is
how you get the number and phrase both anchors. Referenced from
[`../SKILL.md`](../SKILL.md) § Timed camera moves synced to dialogue.

## Measure `T` from the source clip

You are reading `T` off the footage the user already has — not guessing.

1. **Inspect the clip.** Probe its duration / fps (extract a few frames if you can open it).
   You need the total runtime the prompt will match, and the moment the payoff should land.
2. **Find the trigger moment.** It is one of:
   - **A spoken word** — the frame where a specific word begins. Read it from the audio, or from
     the source captions/transcript if the user has them.
   - **A visible action beat** — a finger snap, a head turn, a step, a hand rising. Often easier
     to hit than a word because it's visible in the frames ("at about 2.2s, on his finger snap
     with his right hand up beside his head").
3. **Convert a timecode to seconds.** Prompts want seconds-from-clip-start, not `MM:SS:FF`.
   - `MM:SS` → `MM*60 + SS`. Example: `00:02` → `2` seconds.
   - With frames `MM:SS:FF` at `fps` → `MM*60 + SS + FF/fps`. Example: `00:02:05` at 24fps →
     `2 + 5/24 ≈ 2.2` seconds.
   - Round to one decimal (`~2.2s`); Seedance treats it as intent, not a frame-exact target.

## Phrase both anchors

Put both in the action, close together:

```
At about 2.2 seconds, on the line "transform myself right in front of you," the camera snaps
into a hard crash zoom on his right hand …
```

- **Semantic** — `On the line "<exact words>," …` (or `exactly as the man turns and looks back,
  …` for an action beat). Quote the line **verbatim**.
- **Numeric** — `At about <T> seconds, …`.

If the two ever disagree (the word actually lands at 3s but you wrote 2.2s), fix the number —
the semantic anchor is the ground truth; the numeric one is insurance.

## Requirements and edge cases

- **Keep the talk track.** Any move anchored to a spoken line needs `SFX and source dialogue
  only` in the specs line, or the dialogue won't survive to anchor against. `SFX only` is for
  moves anchored to a silent action beat.
- **Leave a tail.** The payoff needs room to play after the trigger — a creature slowly turning
  to camera needs ~2–3s. If the clip is too short, fire the move on the **first word** of the
  line instead of after it.
- **Recompute on every runtime change.** If the user changes the total duration, every numeric
  `T` shifts — recompute and tell them the new mark. A prepended intro pushes the whole source
  back; do the `total − intro = surviving window` subtraction (`../SKILL.md` § Duration
  discipline) before promising a line will land.
- **Lip-sync fit.** A line that runs ~6s cannot sit in a 5s surviving window. Check the line
  length against the window before delivering.

Dialogue generation, the `[AUDIO: Xs]` script block, lip-sync, and the first-15s audio
extraction trap are documented in [`../../higgsfield-audio/SKILL.md`](../../higgsfield-audio/SKILL.md)
§ Audio as a Conditioning Input.
