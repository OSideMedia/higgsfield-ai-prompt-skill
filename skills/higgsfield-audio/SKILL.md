---
name: higgsfield-audio
description: >
  Use when the user asks about audio in Higgsfield videos, needs to add dialogue
  or lip-sync, wants sound effects or ambient sound in generated video, asks about
  music or BGM in output, or is using any audio-capable model (Kling 3.0, Seedance
  1.5 Pro, Seedance 2.0, Veo 3/3.1, Grok Imagine Video). Also use when the user's
  prompt would benefit from audio direction but they haven't mentioned it.
user-invocable: true
metadata:
  tags: [higgsfield, audio, dialogue, lip-sync, SFX, ambient, sound, BGM, music, voice]
  version: 3.0.0
  updated: 2026-04-06
  parent: higgsfield
---

# Higgsfield Audio Prompting Guide

## Which Models Support Audio?

| Model | Audio type | Dialogue | SFX | Ambient | BGM | Lip-sync |
|-------|-----------|----------|-----|---------|-----|----------|
| Kling 3.0 / Omni | Native joint | ✅ | ✅ | ✅ | ✅ | ✅ Multi-language |
| Seedance 2.0 | Native joint | ✅ | ✅ | ✅ | ✅ | ✅ Multi-language |
| Seedance 1.5 Pro | Native joint | ✅ | ✅ | ✅ | ✅ | ✅ Best lip-sync |
| Veo 3 / 3.1 | Native joint | ✅ | ✅ | ✅ | ✅ | ✅ English best |
| Grok Imagine Video | Native joint | ✅ | ✅ | ✅ | ✅ | ✅ |
| All other models | ❌ | — | — | — | — | — |

**"Native joint"** means audio and video are generated simultaneously in one pass —
not layered on after. This produces natural synchronization without post-production.

Models without native audio: add audio in post with Lipsync Studio or external tools.

---

## The Four Audio Layers

Every audio-capable prompt should consider four layers. You don't need all four
in every prompt, but knowing which to include gives the model clear direction.

### 1. Dialogue — What characters say

Put dialogue in quotes. Be explicit about who speaks, their tone, and language.

```
She says: "We need to leave. Now."
He whispers: "Not yet."
```

**Best practices:**
- Keep dialogue short — 1-2 sentences per character per shot
- Specify emotional tone: "says urgently", "whispers", "shouts across the room"
- For non-English: specify language and dialect → `She speaks in Cantonese: "走啦"`
- For Seedance 1.5 Pro: supports English, Chinese (incl. Sichuanese, Cantonese,
  Taiwanese Mandarin, Shanghainese), Japanese, Korean, Spanish, Indonesian

### 2. SFX — Specific sound events tied to action

Describe SFX at the point they happen. Tie them to visible actions.

```
The glass shatters on the floor — sharp crack, then settling tinkle.
Footsteps on wet concrete — splashing, rhythmic.
A door slams shut — heavy metal, echoing.
```

**Best practices:**
- One SFX description per action beat
- Use onomatopoeia sparingly — descriptive phrases work better than "BANG" or "CRASH"
- Tie timing to action: "as she sets the cup down" not "cup sound at 4 seconds"

### 3. Ambient — Background soundscape

Set the acoustic environment. This is the continuous sound bed.

```
Ambient: quiet café murmur, espresso machine, rain against windows.
Ambient: forest at night — crickets, distant owl, gentle wind through leaves.
Ambient: busy intersection — traffic, horns, construction in the distance.
```

**Best practices:**
- 2-3 ambient elements maximum — more gets muddy
- Describe the *space* acoustics: "reverberant church hall", "tight car interior"
- Contrast silence with sound for impact: "Dead silence. Then — a single footstep."

### 4. BGM — Background music mood

Don't name songs or artists (content filter). Describe the musical texture.

```
BGM: slow piano, minor key, melancholic.
BGM: tense orchestral build — low strings, rising.
BGM: lo-fi hip-hop beat, warm vinyl crackle, relaxed.
```

**Best practices:**
- Describe instrumentation, tempo, mood — not genre labels alone
- "Tense strings, building" works better than "suspenseful music"
- Specify when music enters/exits: "Piano enters at the midpoint, builds to the end"
- For beat-sync content: "Cuts match the downbeat" or "Movement peaks on the drop"

---

## Audio Prompt Structure

Add audio cues naturally within your prompt or as a dedicated block at the end.

### Inline method (preferred for short prompts):

```
A woman walks into a quiet library. Her heels click on the marble floor — each step
echoing. She whispers to the librarian: "Do you have the Collected Letters?"
Distant page turns. A clock ticks somewhere above.
```

### Dedicated block method (better for complex audio):

```
[Scene description — visual content, action, camera]

Audio:
  Dialogue: She says "We leave at dawn." He replies: "I'll be ready."
  SFX: coffee cup set down, chair scraping back
  Ambient: early morning kitchen — birds outside, kettle just boiled
  BGM: none — silence emphasizes the tension
```

---

## Lip-Sync Rules

Lip-sync is the most failure-prone audio feature. Follow these rules strictly:

### Do:
- Keep dialogue clips 3–8 seconds (sweet spot for accuracy)
- Use medium close-up or closer framing — model needs to see the mouth clearly
- One speaking face per shot — multiple faces break audio routing
- Lock the camera: `locked-off static camera` or `slow Dolly In` only
- Remove all head/face motion tokens: `nodding`, `turning head`, `looking around`
  compete with the lip engine and cause desync

### Don't:
- Don't combine dialogue with vigorous head movement in the same prompt
- Don't use 15s clips for lip-sync — technical max but accuracy degrades past 8s
- Don't include ambient or music tokens if lip-sync is the priority — they invite
  the generative audio engine to override your dialogue
- Don't use non-MP3 audio for Seedance 2.0 (when available) — WAV/AAC/OGG fail silently

### Multi-character dialogue workaround:
Multi-person lip-sync matching is an unresolved limitation across all models.
The production workaround:
1. Generate each character separately with their own audio segment
2. Composite in CapCut/Premiere using picture-in-picture + linear mask (15% feather)
3. Static image for the listening character; generated video for the speaking character

---

## Audio by Model — What Works Best Where

### Kling 3.0 (V3) / 3.0 Omni (O3)
- Best overall audio-visual integration
- Multi-language dialogue (English, Chinese, Japanese, Korean, Spanish + regional accents: American English, British English, Indian English)
- Multi-character dialogue: 3+ characters with correct speaker attribution and lip-sync per character
- Voice Binding: lock specific voice profiles to specific characters across shots
- O3 adds Voice Extraction from static images: upload audio clip (min 3s) + image to build a voice profile
- O3 adds Performance Cloning: act out a scene on camera → AI re-renders preserving likeness and voice
- Include dialogue, ambient, and SFX naturally in the prompt
- Prompt like a script: action + camera + mood + dialogue cues together

**Audio Speaker Attribution Format (V3/O3):**
```
[Speaker: Character Name] "dialogue" in a [warm/confident/excited] [male/female] voice with [accent].
Add [sound: footsteps / rain / door closing] when [action].
Background ambient: [environment description].
```

### Seedance 1.5 Pro
- Best lip-sync accuracy of all models
- Class-leading multilingual support including Chinese dialects
- Most stable emotional tone control
- Use for: professional dialogue scenes, multilingual content

### Seedance 2.0
- Upload MP3 audio as @Audio reference (part of Rule of 12)
- **MP3 only** — WAV/AAC/OGG/FLAC fail silently with no error
- Max 15s per clip, 3 audio files, 10MB each
- Timestamp anchoring: `"Audio @Audio1 plays exactly as uploaded from 0s to end. Do not modify."`
  Then remove all ambient/SFX/music tokens to prevent the generative engine from overriding.

### Veo 3 / 3.1
- Strong native audio for English dialogue and environmental sounds
- Dialogue in quotes: `"This must be it," he murmured.`
- SFX explicitly: `tires screeching loudly`
- Ambient as environment soundscape descriptions

### Grok Imagine Video
- Improved audio as of Video Imagine 1.0 (Feb 2026)
- Include audio intent directly in prompt — same inline style as other models
- Best for: social clips where audio adds polish but isn't the hero

---

## Common Audio Failures and Fixes

| Problem | Cause | Fix |
|---------|-------|-----|
| Lip-sync completely off | Audio > 8s, or head motion tokens present | Trim to 5s, remove nodding/turning tokens |
| Model replaces uploaded audio | Ambient/music tokens in prompt invite generative override | Add timestamp anchoring phrase, remove all ambient/music tokens |
| Dialogue missing entirely | Non-MP3 format used (Seedance 2.0) | Convert to MP3 128-320kbps |
| SFX drowns out dialogue | Too many SFX cues competing | Reduce to 1-2 SFX per shot, prioritize dialogue |
| Audio sounds robotic | Flat emotional cues | Add emotional direction: "says warmly", "whispers with urgency" |
| Background music too loud | BGM description too prominent in prompt | Move BGM to end of prompt, reduce detail, or say "subtle BGM" |

---

## When to Skip Audio

Not every prompt needs audio direction. Skip audio cues when:
- Using a model without native audio (Kling 2.6, Wan 2.6, Seedance Pro, Minimax Hailuo 2.3/02)
- The content is purely visual (product beauty shots, abstract motion, landscape)
- Audio will be added entirely in post-production
- The prompt is already at the 200-word limit and visual direction is more important

---

> **Negative constraints:** For audio-specific artifacts (lip-sync desync, background music
> overriding dialogue, SFX drowning dialogue) and their prevention phrases, see
> `../shared/negative-constraints.md` — Temporal/Consistency Artifacts section.

---

## Cinema Studio 3.0 Audio (Business/Team Plan)

Cinema Studio 3.0 introduces native audio-video joint generation — a fundamental shift from models that treat audio as a post-processing step.

### Native Audio-Video Joint Generation

Audio is generated **simultaneously** with video via a unified multimodal architecture. This means:
- Audio and video are temporally aligned by default — no manual sync needed
- Dual-channel stereo output
- Sound design prompts directly influence both audio AND visual generation
- Audio is not "added on" — it's part of the same generation pass

### Audio as Prompt Element (SCELA)

Always describe audio as a **separate section** in your prompts. The generation engine handles three parallel audio tracks:

1. **BGM** — background music, score
2. **Ambient SFX** — environmental sounds, foley
3. **Dialogue** — character speech, voiceover

```
A chef slices vegetables rapidly on a wooden cutting board.
Camera: tight close-up tracking the knife.
Style: warm kitchen lighting, shallow depth of field.

Audio: rhythmic chopping on wood, oil sizzling in a nearby pan,
soft clinking of ceramic bowls. Light acoustic guitar BGM.
```

### Input Constraints

| Parameter | Limit |
|-----------|-------|
| Accepted formats | MP3, WAV |
| Max audio clips | 3 per generation |
| Combined duration | ≤15s total |
| Single file size | <15MB |
| MP3 bitrate | 128–320 kbps |

### Lip-Sync

Available but experimental in Cinema Studio 3.0:
- Focus on **emotion and general mouth movement**, not perfect phoneme sync
- **Single face per generation only** — multi-face lip-sync is not supported
- For best results, keep dialogue segments under 8 seconds
- Pair with clear frontal or 3/4 face angle reference images

### Tone / Voice Cloning via @Reference

Control speaking style, accent, and language by referencing a video with the desired voice:

```
Voiceover tone references @Video1. The narrator describes the product
in a warm, conversational tone. "This changes everything."
Audio @Audio1 plays exactly as uploaded from 0s to end.
Do not modify or replace the audio content.
```

### Dialect Support

Dialects written directly in the prompt work — the model understands regional speech patterns. Write dialogue in the target dialect for authentic delivery.

### Timestamp Anchoring

When uploading reference audio that must play unmodified:

```
Audio @Audio1 plays exactly as uploaded from 0s to end.
Do not modify or replace the audio content.
```

Then **remove all ambient/SFX/music tokens** from the prompt to prevent the generation engine from overriding the uploaded audio with generated sound.

### Sound Design Specificity

Describe **specific foley**, not generic moods:

**Wrong:** `nice ambient sounds, pleasant background noise`

**Right:** `the scratch of frosted glass, rustling of plush fabric, gentle tapping on acrylic, popping of bubble wrap, wooden floor creaking under bare feet`

Specific sound descriptions directly influence the generated audio output. The more precise the foley description, the more accurate the result.

---

## Related skills
- `higgsfield-models` — Which models support native audio
- `higgsfield-troubleshoot` — Audio failure diagnosis
- `higgsfield-cinema` — Cinema Studio audio workflow with Kling 3.0
- `higgsfield-vibe-motion` — Motion graphics with audio (different from AI-generated audio)
