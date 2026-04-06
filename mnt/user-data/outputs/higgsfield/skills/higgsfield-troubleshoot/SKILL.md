---
name: higgsfield-troubleshoot
description: >
  Use when a Higgsfield generation fails, produces poor quality, looks wrong,
  doesn't match the prompt, or the user needs to fix or improve an output.
user-invocable: true
metadata:
  tags: [higgsfield, troubleshoot, fix, quality, failure, improve]
  version: 3.0.0
  updated: 2026-04-06
  parent: higgsfield
---

# Higgsfield Troubleshooting Guide

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
- Cut prompt to under 200 words — trim the least essential details
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
- [ ] Prompt is under 200 words
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
| Output blurry, jittery, or morphing | Overspecification — prompt too long or too detailed | Cut prompt to 30–100 words. Use @reference images/videos instead of 50+ words of description |
| Camera chaotic, spinning, or jittering | Violated the One-Move Rule — multiple camera moves in one shot | Rewrite to ONE primary camera move per shot. Use Cinema Studio 3.0's Smart mode, or split into multi-shot |
| Character doesn't match reference | Prompt is re-describing the character's appearance | Delete ALL physical descriptions. Describe ONLY action and emotion. The @reference carries identity |
| Action stiff or lacking impact | Missing intent/physics language | Add degree adverbs (`violently`, `gently`, `explosively`) and physics consequences (`dust erupts`, `sparks fly`, `fabric tears`) |
| Output "not what I wanted" (vague) | Ambiguous prompt with subjective language | Run Anti-Slop Check: replace `beautiful`, `stunning`, `epic`, `amazing`, `dynamic` with observable, measurable details |
| Audio not matching video | Audio description conflicting with visual description, or uploaded audio being overridden | Use timestamp anchoring for uploaded audio. Remove ambient/SFX tokens when using @Audio references |

### Diagnostic Flowchart

```
Output bad?
├── Blurry/morphing → Is prompt > 100 words?
│   ├── Yes → Cut to 30–100 words, use @reference
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

## Related skills
- `higgsfield-prompt` — MCSLA formula, prompt structure, Identity/Motion separation
- `higgsfield-recall` — Pre-generation memory check for past failures
- `higgsfield-models` — Model selection (wrong model = many quality issues)
- `higgsfield-audio` — Audio-specific failures and fixes
- `higgsfield-cinema` — Cinema Studio–specific issues (512 char limit, @ Element bugs)
- `../shared/negative-constraints.md` — Prevention-focused constraint reference
