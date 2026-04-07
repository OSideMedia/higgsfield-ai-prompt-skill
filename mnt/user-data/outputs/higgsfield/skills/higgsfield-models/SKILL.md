---
name: higgsfield-models
description: >
  Use when the user asks which model to use, wants to compare models,
  or needs guidance on selecting between Kling, Sora 2, Wan, Seedance,
  Veo 3, Minimax Hailuo, Soul, Nano Banana, or other Higgsfield engines.
user-invocable: true
metadata:
  references:
    - MODELS-DEEP-REFERENCE.md
  tags: [higgsfield, models, Kling, Sora, Wan, Seedance, Veo, Soul, NanoBanana]
  version: 3.0.0
  updated: 2026-04-06
  parent: higgsfield

---

# Higgsfield Model Selection Guide

Choosing the right model is the single biggest factor in output quality after the prompt.
This file handles most selection questions. For deep per-model documentation (prompting
specifics, parameters, edge cases, API details) → read `MODELS-DEEP-REFERENCE.md`.

---

## Video Models — Comparison

| Model | Realism | Character | Motion | Style | Duration | Audio | Best for |
|-------|---------|-----------|--------|-------|----------|-------|----------|
| Kling 3.0 | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★☆ | 3–15s | ✅ | Cinematic, long, audio, multi-shot |
| Kling 3.0 Omni | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★☆ | 3–15s | ✅ | Video clone, storyboard control |
| Kling 3.0 Omni Edit | ★★★★★ | ★★★★★ | — | ★★★★☆ | 3–10s | ✅ | Edit footage at 3.0 quality |
| Kling O1 Video (legacy) | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★☆☆ | 5–10s | ❌ | Multi-ref (7), start/end frame |
| Kling O1 Video Edit (legacy) | ★★★★☆ | ★★★★★ | — | ★★★★★ | 3–10s | ❌ | Relight, restyle, swap, remove |
| Kling 3.0 Motion Control | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★☆☆ | 3–30s | Optional | Motion transfer from reference video |
| Kling 2.6 (legacy) | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★☆☆ | 5–10s | ❌ | Character drama, realism (no audio) |
| Kling 2.5 Turbo | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★☆☆ | 5–10s | ❌ | Fast Kling iteration |
| Sora 2 | ★★★★☆ | ★★★☆☆ | ★★★★★ | ★★★★☆ | — | ❌ | Epic scale, physics, action |
| Wan 2.7 | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★★★ | 2–15s | ✅ | 60fps, T2V/I2V/R2V/edit, first+last frame |
| Wan 2.6 | ★★★★☆ | ★★★☆☆ | ★★★★☆ | ★★★★★ | 5–15s | ❌ | Artistic, stylized, improved physics |
| Wan 2.5 | ★★★★☆ | ★★★☆☆ | ★★★★☆ | ★★★★★ | 5–10s | ✅ | Native audio, artistic, fantasy |
| Seedance 2.0 | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★☆ | 10s | ✅ | 12-asset multimodal, complex motion |
| Seedance 1.5 Pro | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | 10s | ✅ | Best lip-sync, multilingual audio |
| Seedance Pro | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | 10s | ❌ | Fast iteration, no audio needed |
| Veo 3.1 | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★★☆ | 4–8s | ✅ | Ref images, first/last frame, 4K |
| Veo 3.1 Lite | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | 4–8s | ✅ | Budget 3.1 quality, 1080p, I2V, volume |
| Veo 3 | ★★★★☆ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | 4–8s | ✅ | Nature, environment, stable model |
| Grok Imagine Video | ★★★★☆ | ★★★☆☆ | ★★★★☆ | ★★★★☆ | 1–15s | ✅ | Video editing, animate images |
| Minimax Hailuo 2.3 | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★★☆ | 6–10s | ❌ | VFX, fluid motion, anime, physics |
| Minimax Hailuo 02 | ★★★★☆ | ★★★☆☆ | ★★★★★ | ★★★☆☆ | 6–10s | ❌ | Dance, sports, fluid motion |
| Higgsfield DoP (Lite/Standard/Turbo) | ★★★☆☆ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | 3–5s | ❌ | I2V specialist, 50+ presets, optical physics |

---

## Decision Flowchart

```
Is this image or video?
├── IMAGE
│   ├── Person / portrait? → Soul 2.0
│   ├── Cinematic keyframe for I2V pipeline? → Soul Cinema Preview
│   ├── Native 4K / image series / storyboarding? → Kling Image 3.0
│   ├── Maximum sharpness / 4K? → Nano Banana Pro
│   ├── Fast pro-quality / text rendering? → Nano Banana 2
│   ├── Reference consistency or dense text? → Seedream 4.5
│   ├── Complex layout / multi-panel? → Seedream 5.0 Lite
│   ├── Text/logo in image? → GPT Image 1.5
│   └── Edit an existing image? → Flux Kontext
│
└── VIDEO
    ├── EDIT existing footage?
    │   ├── Relight, restyle, swap, remove → Kling O1 Video Edit
    │   └── Higher quality 3.0 edit → Kling 3.0 Omni Edit
    │
    ├── Is a human character the focus?
    │   ├── Need audio, long clip (15s), multi-shot → Kling 3.0
    │   ├── Need to clone from reference video → Kling 3.0 Omni
    │   ├── Best lip-sync + multilingual → Seedance 1.5 Pro
    │   ├── No audio needed, great character → Kling 2.6
    │   └── Fast iteration → Kling 2.5 Turbo
    │
    ├── Need motion transfer from reference video?
    │   └── → Kling 3.0 Motion Control
    │
    ├── Animate a still image with cinematic camera?
    │   └── → Higgsfield DoP (Lite/Standard/Turbo)
    │
    ├── Is the environment/phenomenon the hero?
    │   ├── Nature, documentary, stable → Veo 3
    │   ├── Need ref image consistency → Veo 3.1
    │   ├── Budget Veo 3.1 quality / volume → Veo 3.1 Lite
    │   ├── 60fps, first+last frame, ref images → Wan 2.7
    │   └── Artistic, painterly, fantasy → Wan 2.5/2.6
    │
    ├── Is it action/spectacle?
    │   ├── Epic scale, crowds, physics → Sora 2
    │   ├── VFX, anime, fluid motion → Minimax Hailuo 2.3
    │   └── Dance, sports, budget motion → Minimax Hailuo 02
    │
    ├── Need maximum reference control?
    │   ├── Up to 12 assets (images+video+audio) → Seedance 2.0
    │   ├── Up to 7 image refs → Kling O1 Video
    │   └── Up to 3 asset refs → Veo 3.1
    │
    └── Speed/cost priority?
        ├── Fastest Kling → Kling 2.5 Turbo
        ├── Fastest Seedance → Seedance Pro
        └── Fastest Veo → Veo 3.1 Fast or Veo 3 Fast
```

---

## Image Models — Quick Selection

| Need | Model | Credits |
|------|-------|---------|
| Fashion / cultural portrait | Soul 2.0 | Free |
| Cinematic keyframe for I2V | Soul Cinema Preview | Low |
| Cheapest generation | Z-Image | 0.15 |
| Low-cost portrait | Higgsfield Soul | 0.5 |
| Low-cost 2K square | Kling O1 | 0.5 |
| Native 4K / image series | Kling Image 3.0 | — |
| 4K + advanced editing | Kling Image 3.0 Omni | — |
| Fast versatile 2K | Seedream 5.0 Lite | 1 |
| 4K versatile | Seedream 4.5 | 1 |
| Sketch-to-image (Draw) | Nano Banana | 1 |
| Artistic / stylized | Wan 2.2 | 1 |
| Blend multiple references | Multi Reference | 1.5 |
| Fast pro-quality + text rendering | Nano Banana 2 | 1.5 |
| Complex prompts / text in image | GPT Image 1.5 | 2 |
| Max fidelity / Thinking mode / 14 refs | Nano Banana Pro | 2 |
| Image editing / inpainting | Flux Kontext | varies |

Full image model specs + UI controls → `../../../../../../image-models.md`

---

## Budget Tiers

**Free / near-free:** Soul 2.0 (5K gens) · Z-Image (0.15) · Face Swap (2 free)
**Budget (0.5–1):** Higgsfield Soul · Kling O1 · Seedream family · Nano Banana · Wan 2.2 · Reve
**Mid (1.5–2):** Nano Banana 2 · Multi Reference · FLUX.2 Pro · Flux Kontext Max · GPT Image · NB Pro · Character Swap
**Premium (5–6):** FLUX.2 Flex · FLUX.2 Max

---

## Unique Feature Matrix

| Feature | Available on |
|---------|-------------|
| Native audio (dialogue, SFX, ambient) | Kling 3.0/Omni · Seedance 1.5 Pro/2.0 · Veo 3/3.1 · Grok Video |
| Soul ID character slot | Soul 2.0 · GPT Image · Higgsfield Soul |
| @ Elements syntax | Seedream 4.5/5.0 Lite · Nano Banana Pro · Cinema Studio |
| Draw (sketch-to-image) | Nano Banana · Nano Banana Pro |
| Video editing (relight/restyle/swap) | Kling O1 Video Edit · Kling 3.0 Omni Edit · Grok Video |
| Multi-image reference blend | Multi Reference · Nano Banana Pro (14 refs) · Kling O1 Video (7 refs) |
| Start/end frame control | Kling O1 Video · Veo 3.1 · Wan 2.7 |
| Video extension (up to 148s) | Veo 3.1 |
| Performance cloning from video | Kling 3.0 Omni |
| Up to 30s camera/motion transfer | Kling 3.0 Motion Control |
| Soul Cast AI actors | Cinema Studio 2.5 |
| Soul Cast AI actors (General 2K / Character 4K / Location 4K) | Cinema Studio 3.0 (Business/Team) |
| Built-in color grading | Cinema Studio 2.5 |
| Native dual-channel stereo audio | Cinema Studio 3.0 (Business/Team) · Kling 3.0/Omni · Seedance 2.0/1.5 Pro · Veo 3/3.1 · Wan 2.5/2.7 |
| Soul HEX color matching | Soul 2.0 · Soul Cinema Preview · Cinema Studio 2.5 |
| Native 4K image series | Kling Image 3.0 |
| Style presets + Color Transfer | Soul 2.0 |
| Google Search grounding | Nano Banana Pro |
| Negative prompts supported | Veo 3/3.1 only |
| Smart auto-camera planning | Cinema Studio 3.0 (Business/Team) |

---

## Key Model Notes

**Kling 3.0 vs 2.6:** 3.0 is the current top model — longer clips (15s vs 10s), native audio,
multi-shot AI direction, physics engine, 4K HDR, stylized output engine. 2.6 is now legacy —
use 3.0 for all new work unless cost is the primary constraint.

**Kling V3 vs O3:** Use V3 for prompt-driven cinematic work (text-to-video, image-to-video).
Use O3 when you have reference media (video or image+audio) to anchor character identity —
O3's reference-based consistency is its defining advantage.

**Kling 3.0 Motion Control:** Upload a 3–30s reference clip to transfer full-body motion,
hand gestures, facial expressions. Image Orientation for camera/talking head; Video
Orientation for complex motions (dancing, action, full-body movement).

**Seedance 2.0:** Rule of 12 (up to 12 assets per
generation). Real person face uploads blocked — use synthetic character references. Best practices for Seedance 2.0 prompting are integrated into the sub-skills (see higgsfield-prompt, higgsfield-camera, higgsfield-motion).

**Veo 3.1 vs 3.1 Lite vs 3:** 3.1 adds reference images (up to 3), first/last frame, video extension, 4K.
3.1 Lite is budget-priced 3.1 quality at 1080p — supports T2V and I2V, costs less than half of 3.1 Fast.
3 is stable and proven. Use 3.1 for subject consistency, 3.1 Lite for volume, 3 for pure environment/nature.

**Wan 2.7:** Major upgrade — native 60fps (vs 24fps in 2.6), up to 15s duration, first+last frame anchoring, up to 5 reference images, 4-model suite (T2V/I2V/R2V/video edit), Flow-Matching architecture. 40% better physics consistency over 2.6.

**Wan 2.5:** First Wan version with native audio — joint text/audio/video generation. Supports audio-driven video (upload audio to drive visuals). 1080p, 5–10s.

**Minimax Hailuo 2.3 vs 02:** 2.3 is a major upgrade — improved physics, anime/illustration styles, facial micro-expressions, better prompt adherence. Fast variant now at 1080p (02 Fast was 512p). 02 remains available for budget motion work.

**Grok Imagine:** Aurora architecture (autoregressive, not diffusion) — excels at text/logo
rendering and multi-image compositing. Image editing supports multi-turn iterative chains.

For deep documentation on any specific model → read `MODELS-DEEP-REFERENCE.md`

---

## Cinema Studio 3.0 (Business/Team Plan)

Cinema Studio 3.0 is a separate generation engine available on Business and Team plans. Version toggle in the upper-right corner of the Cinema Studio UI switches between 2.5 and 3.0.

| Feature | Cinema Studio 2.5 | Cinema Studio 3.0 (Business/Team) |
|---------|-------------------|-----------------------------------|
| Video Resolution | Up to 1080p | Up to 720p (may increase) |
| Image Resolution | Up to 4K | Up to 4K (Character/Location) · Up to 2K (General) |
| Max Duration | 12s | 15s |
| Aspect Ratios | 6 options | 7 options (+ 21:9 ultrawide) |
| Audio | On/Off | On/Off (native dual-channel stereo) |
| Shot Control | Manual multi-shot | Smart (auto) + Custom multi-shot |
| Generation Cost | Varies | 48 credits |

> For full Cinema Studio 3.0 documentation → see `higgsfield-cinema`

---

## Related skills
- `higgsfield-prompt` — MCSLA formula, prompt structure
- `higgsfield-cinema` — Cinema Studio model selection
- `higgsfield-assist` — Credit optimization and plan selection
- `higgsfield-audio` — Audio-capable model details
- `templates/` — Annotated templates with per-genre model recommendations
