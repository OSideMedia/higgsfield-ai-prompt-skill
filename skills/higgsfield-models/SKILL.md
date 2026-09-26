---
name: higgsfield-models
description: >
  Use when the user asks which model to use, wants to compare models,
  or needs guidance on selecting between Kling, Sora 2, Wan (incl. Wan 3.0),
  Seedance (incl. 2.5), Veo 3, Minimax Hailuo / MiniMax H3, FLUX 3 Video,
  Gemini Omni Flash, Soul, Nano Banana, GPT Image 2.5, or other Higgsfield
  engines — including which lane edits existing footage (video_edit, Kling
  3.0 Omni Edit, FLUX 3 Video Edit, Genjutsu, Ad Multiplier) and which
  models make one clip longer than 15s.
user-invocable: true
metadata:
  references:
    - MODELS-DEEP-REFERENCE.md
  tags: [higgsfield, models, Kling, Sora, Wan, Seedance, Veo, Soul, NanoBanana, GPT-Image-2.5, FLUX-3, Genjutsu, edit-lanes, long-take]
  version: 3.3.0
  updated: 2026-09-26
  parent: higgsfield

---

# Higgsfield Model Selection Guide

Choosing the right model is the single biggest factor in output quality after the prompt.
This file handles most selection questions. For deep per-model documentation (prompting
specifics, parameters, edge cases, API details) → read `MODELS-DEEP-REFERENCE.md`.
The canonical comparison tables, the **Edit-Lane Chooser**, the **Long-Take Chooser**, and
the **Motion Transfer** table live in `../../model-guide.md` — this file agrees with them.

Star ratings are written only from real generations. A `—` in a star column means **not
yet field-rated**; platform facts for those rows are `[OFFICIAL — platform, snapshot 2026-09-26]`.

---

## Quick Decision Flowchart

Fast lookup — for detailed comparisons see the full tables below.

| Need | Recommended Model | Tier |
|------|-------------------|------|
| Top-tier cinematic video + audio | Kling 3.0 | Premium |
| Epic scale / spectacle | Seedance 2.0 or Minimax Hailuo 2.3 (Sora 2 is UI-only — verify live) | Premium |
| Nature / landscapes | Veo 3.1 | Premium |
| Artistic / stylized video | Wan 2.6 | Mid |
| One clip longer than 15s | Seedance 2.5 · Wan 3.0 / Prime · FLUX 3 Video (to 20s) → `model-guide.md` § Long-Take Chooser | — |
| Edit / extend / multiply existing footage | → `model-guide.md` § Edit-Lane Chooser | — |
| Motion transfer from a reference video | Kling 3.0 Motion Control or Genjutsu → `model-guide.md` § Motion Transfer | — |
| Fast video iteration | Seedance 2.0 Fast / Mini | Mid |
| VFX / fluid motion | Minimax Hailuo 2.3 | Mid |
| Budget-friendly video | Kling 2.5 Turbo / Higgsfield DoP Lite | Free–Low |
| Fashion / aesthetic images | Soul 2.0 | Free |
| Photorealistic sharp images | Nano Banana Pro | Low |
| AI actor generation | Soul Cast | Low |
| Native 4K images | Kling Image 3.0 | Mid |
| Transparent-background image | GPT Image 2.5 (`background: transparent`) | — |
| Photo style transformation | Photodump (29 presets) | Low |

**Pricing tiers:** Free (Soul 2.0, DoP Lite) · Low (0.1–2 credits) · Mid (2–10 credits) · Premium (10+ credits). See the Credit Cost Reference below for exact per-model costs.

---

## Video Models — Comparison

| Model | Realism | Character | Motion | Style | Duration | Audio | Best for |
|-------|---------|-----------|--------|-------|----------|-------|----------|
| Kling 3.0 | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★☆ | 3–15s | ✅ | Cinematic, long, audio, multi-shot |
| Kling 3.0 Omni | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★☆ | 3–15s | ✅ | Video clone, storyboard control |
| Kling 3.0 Omni Edit | ★★★★★ | ★★★★★ | — | ★★★★☆ | 3–10s in (UI doctrine) | ✅ | Edit footage at 3.0 quality — `kling_video_edit`, `mode` std / pro / 4k, source video + optional image refs |
| Kling O1 Video (legacy) | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★☆☆ | 5–10s | ❌ | Multi-ref (7), start/end frame |
| Kling O1 Video Edit (legacy) | ★★★★☆ | ★★★★★ | — | ★★★★★ | 3–10s | ❌ | Relight, restyle, swap, remove — UI-only, not in the API catalog |
| Kling 3.0 Motion Control | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★☆☆ | 3–30s | Optional | Motion transfer from reference video |
| Genjutsu — motion transfer | — | — | — | — | — | — | `hf_mult_motion_control`: motion from a reference video onto subjects in reference images; 480p–1080p. Not yet field-rated |
| Genjutsu — replace object | — | — | — | — | — | — | `hf_mult_replace_object`: replace objects in a source video from reference images; 480p–1080p. Not yet field-rated |
| Kling 2.6 (legacy) | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★☆☆ | 5/10s | ✅ | Character drama, realism; native audio via `sound` toggle (default on) |
| Kling 2.5 Turbo | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★☆☆ | 5–10s | ❌ | Fast Kling iteration |
| Sora 2 (UI-only) | ★★★★☆ | ★★★☆☆ | ★★★★★ | ★★★★☆ | 4–12s | ✅ | Epic scale, physics, action — UI generations only; not in the API catalog (2026-09-26) |
| Wan 3.0 | — | — | — | — | 2–30s or −1 smart (billed as 10s) | ✅ | T2V, first/last frame, multimodal reference (image/video/audio), `enable_thinking`; frames and references never combined. Not yet field-rated |
| Wan 3.0 Prime | — | — | — | — | 2–30s or −1 smart (billed as 10s) | ✅ | Same parameter surface as Wan 3.0; how Prime differs is not stated. Not yet field-rated |
| Wan 2.7 | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★★★ | 2–15s | ✅ | 60fps, T2V/I2V/R2V/edit, first+last frame |
| Wan 2.6 | ★★★★☆ | ★★★☆☆ | ★★★★☆ | ★★★★★ | 5/10/15s | ❌ | Artistic, stylized, improved physics |
| Wan 2.5 | ★★★★☆ | ★★★☆☆ | ★★★★☆ | ★★★★★ | 5–10s | ✅ | Native audio, artistic, fantasy |
| Seedance 2.5 | — | — | — | — | 4–30s | ✅ | Omni-reference (≤30 images incl. start/end, ≤50 items), `video_edit`, `video_extension`; 480p / 720p / **1080p**; start/end frames only in `omni_reference`; no 4K, no `genre`. Not yet field-rated |
| Ad Multiplier | — | — | — | — | 4–30s | ✅ | "Powered by Seedance 2.5" — many edited variants of one 4–30s ad via Higgsfield's `ad-multiplier` workflow. Not yet field-rated |
| Seedance 2.0 | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★☆ | 4–15s | ✅ | 12-asset multimodal, complex motion, native 4K (`mode=std`), `genre` |
| Seedance 2.0 Fast | ★★★★☆ | ★★★★☆ | ★★★★★ | ★★★★☆ | 4–15s | ✅ | `mode=fast` of 2.0 — no 1080p/4K |
| Seedance 2.0 Mini | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | 4–15s | ✅ | Budget tier, full reference roles + `genre`; no 1080p/4K |
| Seedance 1.5 Pro | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | 4/8/12s | ✅ | Best lip-sync, multilingual audio |
| Seedance Pro (legacy UI label) | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | 10s | ❌ | Not in the API catalog — use Seedance 2.0 Fast / Mini |
| Veo 3.1 | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★★☆ | 4/6/8s | ✅ | Ref images, first/last frame, 4K (Google API — the catalog's `veo3_1` shows only `start_image`; verify) |
| Veo 3.1 Lite | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | 4/6/8s | ✅ | Budget 3.1 quality, 1080p, start + end frame, volume |
| Veo 3 | ★★★★☆ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | 4–8s | ✅ | Nature, environment, stable model |
| Gemini Omni Flash | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | 4–10s | ✅ | Reference-driven video (image + video refs), native audio, 720p |
| Gemini Omni Flash 1.1 | — | — | — | — | 3–10s | ✅ | Required `mode` (t2v / i2v / reference / **edit** — source ≤30s); start/end frames; 360p–4K. Not yet field-rated |
| Grok Imagine Video | ★★★★☆ | ★★★☆☆ | ★★★★☆ | ★★★★☆ | 1–15s | ✅ | Animate images, social clips (the catalog exposes no source-video input — editing unverified on Higgsfield) |
| Minimax Hailuo 2.3 | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★★☆ | 6/10s | ❌ | VFX, fluid motion, anime, physics |
| Minimax Hailuo 02 | ★★★★☆ | ★★★☆☆ | ★★★★★ | ★★★☆☆ | 6/10s | ❌ | Dance, sports, fluid motion |
| MiniMax H3 | — | — | — | — | 4–15s | — | Keyframes or image/video/audio refs, 2K, `batch_size` 1–4. Not yet field-rated |
| MiniMax H3 Max | — | — | — | — | 5–15s | — | "Fast" variant, 480p / 768p, same roles, `batch_size` 1–4. Not yet field-rated |
| Happy Horse Video | — | — | — | — | 3–15s | — | T2V + single start frame, 720p / 1080p. Not yet field-rated |
| FLUX 3 Video | — | — | — | — | 5–20s | ✅ | T2V, multi-frame I2V, continuation; native 2:1. Not yet field-rated |
| FLUX 3 Video Edit | — | — | — | — | first 15s of source | — | Text edit of one video, 1 credit per processed second. Not yet field-rated |
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
│   ├── Text/logo in image? → GPT Image 2.5 or GPT Image 2 (see higgsfield-gpt-image-2)
│   ├── Transparent-background cut-out? → GPT Image 2.5
│   ├── Extend / crop the canvas per side? → FLUX.2 Pro Outpaint
│   ├── Masked inpaint? → Nano Banana 2 / 2 Lite (`mask` + `is_inpaint`)
│   └── Edit an existing image? → Flux Kontext
│
└── VIDEO
    ├── EXISTING footage to edit, extend, or multiply?
    │   └── → model-guide.md § Edit-Lane Chooser (one table, every lane)
    │
    ├── One clip longer than 15s?
    │   └── → model-guide.md § Long-Take Chooser
    │       (Seedance 2.5 · Wan 3.0 / Prime · FLUX 3 Video · Cinema Studio 4.0)
    │
    ├── Is a human character the focus?
    │   ├── Need audio, up to 15s, multi-shot → Kling 3.0
    │   ├── Need to clone from reference video → Kling 3.0 Omni
    │   ├── Best lip-sync + multilingual → Seedance 1.5 Pro
    │   ├── Legacy-tier great character (audio togglable via `sound`) → Kling 2.6
    │   └── Fast iteration → Kling 2.5 Turbo
    │
    ├── Need motion transfer from reference video?
    │   └── → Kling 3.0 Motion Control or Genjutsu (model-guide.md § Motion Transfer)
    │
    ├── Animate a still image with cinematic camera?
    │   └── → Higgsfield DoP (Lite/Standard/Turbo)
    │
    ├── Is the environment/phenomenon the hero?
    │   ├── Nature, documentary, stable → Veo 3
    │   ├── Need ref image consistency → Veo 3.1 (verify refs in the UI)
    │   ├── Budget Veo 3.1 quality / volume → Veo 3.1 Lite
    │   ├── 60fps, first+last frame, ref images → Wan 2.7
    │   └── Artistic, painterly, fantasy → Wan 2.5/2.6
    │
    ├── Is it action/spectacle?
    │   ├── Epic scale, crowds, physics → Seedance 2.0 (Sora 2 is UI-only — verify)
    │   ├── VFX, anime, fluid motion → Minimax Hailuo 2.3
    │   └── Dance, sports, budget motion → Minimax Hailuo 02
    │
    ├── Need maximum reference control?
    │   ├── Up to 30 images / 50 items (images + video + audio) → Seedance 2.5
    │   ├── Up to 12 assets with 4K or `genre` → Seedance 2.0
    │   ├── Up to 7 image refs → Kling O1 Video
    │   └── Image + video refs with native audio → Gemini Omni Flash / 1.1
    │
    └── Speed/cost priority?
        ├── Fastest Kling → Kling 2.5 Turbo
        ├── Seedance drafts → Seedance 2.0 Fast / Mini
        ├── Up to 4 takes per call → MiniMax H3 / H3 Max (`batch_size`)
        └── Fastest Veo → Veo 3.1 Fast or Veo 3 Fast
```

---

## Image Models — Quick Selection

| Need | Model | Credits |
|------|-------|---------|
| Fashion / cultural portrait | Soul 2.0 | Free |
| Cinematic keyframe for I2V | Soul Cinema Preview | Low |
| Consistent character identity (16:9) | Soul Cast | `budget` 10–500 |
| Environment / location plate | Soul Location | — |
| Cheapest generation | Z-Image | 0.15 |
| Low-cost portrait | Higgsfield Soul | 0.5 |
| Low-cost 2K square | Kling O1 | 0.5 |
| Native 4K / image series | Kling Image 3.0 | — |
| 4K + advanced editing | Kling Image 3.0 Omni | — |
| Fast versatile 2K | Seedream 5.0 Lite | 1 |
| Fast generation + instruction editing up to 2K | Seedream 5.0 Flash (not yet field-rated) | — |
| 4K versatile | Seedream 4.5 | 1 |
| Sketch-to-image (Draw) | Nano Banana | 1 |
| Artistic / stylized | Wan 2.2 | 1 |
| Blend multiple references | Multi Reference | 1.5 |
| Fast pro-quality + text rendering | Nano Banana 2 | 1.5 |
| Budget NB2 (1k only, `thinking` MINIMAL/HIGH) | Nano Banana 2 Lite | — |
| Transparent background · quality to `max` · 15 aspect ratios | GPT Image 2.5 (not yet field-rated) | — |
| Complex prompts / text in image | GPT Image 1.5 | 2 |
| Reference-based editing + best text rendering | OpenAI Hazel | — |
| Max fidelity / Thinking mode / 14 refs | Nano Banana Pro | 2 |
| xAI generation + editing | Grok Image / Grok Image 2.0 (not yet field-rated) | — |
| Image editing / inpainting | Flux Kontext | varies |
| Extend or crop the canvas per side | FLUX.2 Pro Outpaint (not yet field-rated) | — |
| Photo style transformation (29 cartoon/illustration presets) | Photodump | Low |

Full image model specs + UI controls → `../../image-models.md`
Full Photodump preset library (29 named styles) → `../../photodump-presets.md`

---

## Budget Tiers

**Image models — by credit cost:**
- **Free / near-free:** Soul 2.0 (5K gens) · Z-Image (0.15) · Face Swap (2 free)
- **Budget (0.5–1):** Higgsfield Soul · Kling O1 · Seedream family · Nano Banana · Wan 2.2 · Reve
- **Mid (1.5–2):** Nano Banana 2 · Multi Reference · FLUX.2 Pro · Flux Kontext Max · GPT Image · NB Pro · Character Swap
- **Premium (5–6):** FLUX.2 Flex · FLUX.2 Max

**General pricing tiers (video + image, approximate):**
- **Free:** Soul 2.0 · DoP Lite (limited)
- **Low:** 0.1–2 credits per generation
- **Mid:** 2–10 credits per generation
- **Premium:** 10+ credits per generation

For exact per-model video costs see the Credit Cost Reference in `../../model-guide.md`.

---

## Unique Feature Matrix

Catalog-backed rows cite `[OFFICIAL — platform, snapshot 2026-09-26]` (media roles and params in
`../../specs/MODEL-SPECS.md` / `IMAGE-MODEL-SPECS.md`); other entries are earlier doctrine.

| Feature | Available on |
|---------|-------------|
| Native audio (dialogue, SFX, ambient) | Kling 3.0/Omni/2.6 · Seedance 2.5/2.0/2.0 Mini/1.5 Pro · Ad Multiplier · Wan 3.0/Prime · FLUX 3 Video · Gemini Omni Flash / 1.1 · Veo 3/3.1/3.1 Lite · Wan 2.5/2.7 · Grok Video · Cinema Studio 3.0 / 4.0 |
| Soul ID character slot | Soul 2.0 · GPT Image · Higgsfield Soul |
| @ Elements syntax | Seedream 4.5/5.0 Lite · Nano Banana Pro · Cinema Studio |
| Draw (sketch-to-image) | Nano Banana · Nano Banana Pro |
| Video editing (existing footage) | Seedance 2.5 `video_edit` · Cinema Studio 4.0 `video_edit` · Kling 3.0 Omni Edit · FLUX 3 Video Edit · Gemini Omni Flash 1.1 `edit` · Genjutsu replace-object · Ad Multiplier (many variants) · Kling O1 Video Edit (UI-only legacy) → `../../model-guide.md` § Edit-Lane Chooser |
| Multi-image reference blend | Seedance 2.5 (≤30 images) · Multi Reference · Nano Banana Pro (14 refs) · Kling O1 Video (7 refs) |
| Start/end frame control | Seedance 2.5 (`omni_reference` only) / 2.0 / 2.0 Mini / 1.5 Pro · Kling 3.0 · Wan 3.0/Prime (not with references) · Wan 2.7 · FLUX 3 Video · Gemini Omni Flash 1.1 · MiniMax H3 / H3 Max · Minimax Hailuo · Veo 3.1 Lite · Cinema Studio 3.0 / 4.0 · Marketing Studio · Ad Multiplier · Kling O1 Video (UI legacy) |
| Video extension | Seedance 2.5 / Ad Multiplier / Cinema Studio 4.0 `video_extension` (forward / backward) · FLUX 3 Video (continuation) · Veo 3.1 (Google API chain to 148s — the catalog's `veo3_1` takes no video input; verify) |
| One clip longer than 15s | Seedance 2.5 (30s) · Wan 3.0/Prime (30s) · FLUX 3 Video (20s) → `../../model-guide.md` § Long-Take Chooser |
| Performance cloning from video | Kling 3.0 Omni |
| Motion transfer from a reference video | Kling 3.0 Motion Control (3–30s reference) · Genjutsu `hf_mult_motion_control` |
| Soul Cast AI actors | Cinema Studio 2.5 · standalone `soul_cast` image model (16:9, `budget` 10–500) |
| Soul Cast AI actors (General 2K / Character 4K / Location 4K) | Cinema Studio 3.0 (Business/Team) |
| Built-in color grading | Cinema Studio 2.5 (full grading suite) · Cinema Studio 3.5 (Color Palette axis in Style Settings — 8 named palettes) |
| Native dual-channel stereo audio | Cinema Studio 3.0 (Business/Team) · Kling 3.0/Omni · Seedance 2.0/1.5 Pro · Veo 3/3.1 · Wan 2.5/2.7 |
| Soul HEX color matching | Soul 2.0 · Soul Cinema Preview · Cinema Studio 2.5 |
| Native 4K image series | Kling Image 3.0 |
| Style presets + Color Transfer | Soul 2.0 (the CLI forbids `style_id` + image references in one Soul 2.0 call — see `../../image-models.md` § Soul 2.0) |
| Transparent-background image output | GPT Image 2.5 `background: transparent` (the CLI also lists `background` on GPT Image 2 — see `../../image-models.md` § GPT Image 2) |
| Masked inpaint | Nano Banana 2 / 2 Lite (`mask` + `is_inpaint`) · Seedream 5.0 Pro (`is_inpaint`) · GPT Image 2 (CLI only) |
| Google Search grounding | Nano Banana Pro |
| Negative prompts | Veo 3/3.1 · Wan 3.0 (Alibaba docs: an in-prompt "Negative prompt list" section, not a separate parameter) |
| Batch of up to 4 takes per call | MiniMax H3 / H3 Max (`batch_size`) |
| Smart auto-camera planning | Cinema Studio 3.0 (Business/Team) |

---

## Key Model Notes

**Kling 3.0 vs 2.6:** 3.0 is the current top Kling model — longer clips (15s vs 10s), native audio,
multi-shot AI direction, physics engine, 4K HDR, stylized output engine. 2.6 is now legacy —
use 3.0 for all new work unless cost is the primary constraint.

**Kling V3 vs O3:** Use V3 for prompt-driven cinematic work (text-to-video, image-to-video).
Use O3 when you have reference media (video or image+audio) to anchor character identity —
O3's reference-based consistency is its defining advantage.

**Kling 3.0 Motion Control:** Upload a 3–30s reference clip to transfer full-body motion,
hand gestures, facial expressions. Image Orientation for camera/talking head; Video
Orientation for complex motions (dancing, action, full-body movement). Genjutsu
(`hf_mult_motion_control`) is the other motion-transfer lane — see model-guide.md § Motion Transfer.

**Seedance 2.0:** Rule of 12 (up to 12 assets per
generation). Real person face uploads blocked — use synthetic character references. Best practices for Seedance 2.0 prompting are integrated into the sub-skills (see higgsfield-prompt, higgsfield-camera, higgsfield-motion).

**Seedance 2.5 (2026-09-26 surface):** 4–30s, 480p / 720p / **1080p**, four modes. `start_image` /
`end_image` are accepted **only in `omni_reference`**; `t2v` takes no media. 4K and the `genre`
param remain on the 2.0 family (2.0; `genre` also on 2.0 Mini). Dialect: `higgsfield-seedance-2-5`.

**Wan 3.0 / 3.0 Prime:** 2–30s (or `-1` smart duration, billed as 10s — offer it only when the
user asks the model to pick the length), 480p–1080p, native audio, `enable_thinking`. A call
carries either frames or references, never both. Vendor prompting dialect:
`MODELS-DEEP-REFERENCE.md` § Wan 3.0.

**Veo 3.1 vs 3.1 Lite vs 3:** 3.1 adds reference images (up to 3), first/last frame, video extension, 4K
at the Google API; the Higgsfield catalog's `veo3_1` exposes only a `start_image` role, so verify
those in the UI. 3.1 Lite is budget-priced 3.1 quality at 1080p — supports T2V and I2V with start +
end frames, costs less than half of 3.1 Fast. 3 is stable and proven. Use 3.1 for subject
consistency, 3.1 Lite for volume, 3 for pure environment/nature.

**Wan 2.7:** Major upgrade — native 60fps (vs 24fps in 2.6), up to 15s duration, first+last frame anchoring, up to 5 reference images, 4-model suite (T2V/I2V/R2V/video edit), Flow-Matching architecture. 40% better physics consistency over 2.6.

**Wan 2.5:** First Wan version with native audio — joint text/audio/video generation. Supports audio-driven video (upload audio to drive visuals). 1080p, 5–10s.

**Minimax Hailuo 2.3 vs 02:** 2.3 is a major upgrade — improved physics, anime/illustration styles, facial micro-expressions, better prompt adherence. Fast variant now at 1080p (02 Fast was 512p). 02 remains available for budget motion work.

**Grok Imagine:** Aurora architecture (autoregressive, not diffusion) — excels at text/logo
rendering and multi-image compositing. On Higgsfield: **Grok Image** (`grok_image`) and
**Grok Image 2.0** (`grok_image_2_0`) are live image models; Grok Video takes only a start image.

**Gemini Omni Flash / 1.1:** Google's reference-driven video models. 1.0 accepts image and video
references, native audio, 4–10s at 720p (16:9 or 9:16). 1.1 adds a required `mode`
(text-to-video / image-to-video / reference-to-video / edit), start/end frames, 3–10s, and
360p–4K; its edit mode uses the source duration capped at 30s. 1.1 is not yet field-rated.

For deep documentation on any specific model → read `MODELS-DEEP-REFERENCE.md`

---

## Cinema Studio 3.0 (Business/Team Plan)

Cinema Studio 3.0 is a separate generation engine available on Business and Team plans. Version toggle in the upper-right corner of the Cinema Studio UI switches between 2.5 and 3.0.

| Feature | Cinema Studio 2.5 | Cinema Studio 3.0 (Business/Team) | Cinema Studio 3.5 |
|---------|-------------------|-----------------------------------|--------------------|
| Video Resolution | Up to 1080p | Up to 720p (may increase) | 480p / 720p / 1080p (three-tier) |
| Image Resolution | Up to 4K | Up to 4K (Character/Location) · Up to 2K (General) | 1.5K / 2K (Soul Cinema, default image model) · 1K / 2K / 4K (Cinematic Cameras image model) |
| Max Duration | 12s | 15s | 15s |
| Aspect Ratios | 6 options | 7 options (+ 21:9 ultrawide) | Video: 7 options (Auto, 16:9, 9:16, 4:3, 3:4, 1:1, 21:9) · Image: 8 options (1:1, 3:4, 2:3, 9:16, 3:2, 4:3, 16:9, 21:9) |
| Audio | On/Off | On/Off (native dual-channel stereo) | On/Off (generated alongside video) |
| Shot Control | Manual multi-shot | Smart (auto) + Custom multi-shot | Video: 3-pill main UI (Genre / Style / Camera) · Image: Cinematic models picker (Soul Cinema default + Cinematic Characters / Locations / Cameras) — see `higgsfield-cinema` |
| Generation Cost | Varies | 48 credits | Varies — see Higgsfield plan documentation |

> For full Cinema Studio 3.0 documentation → see `higgsfield-cinema`

Cinema Studio 3.5 sits alongside 2.5 and 3.0 in the model selector — all three coexist on the platform, version is user-selected, and there is no auto-routing between them. 3.5 reframes the surface: the main UI collapses creative control into three pills (Genre / Style / Camera), each defaulting to Auto with manual override available. Optical physics is restored via a four-axis Camera Settings panel (Camera Body / Lens / Focal Length / Aperture, with 75mm added as a new focal length vs 2.5's 8/14/35/50mm set — vocabulary differs from 2.5; do not mix). The Style Settings panel exposes three preset axes (Color Palette / Lighting / Camera Moveset Style) plus a free-form Manual Style mode for natural-language style direction. An AI director toggle is visible in the bottom toolbar; function not yet documented. 3.5 supports both video and image generation; the image-mode picker exposes four Cinematic models (Soul Cinema default, plus Cinematic Characters, Cinematic Locations, and Cinematic Cameras with 2.5 vocabulary) — see `higgsfield-cinema` for the image-mode surface.

> For full Cinema Studio 3.5 documentation → see `higgsfield-cinema`

**Cinema Studio 4.0** (`cinematic_studio_video_4_0`) is live as a **CLI workflow** (not in the MCP
`models_explore` list, 2026-09-26): the same four modes as Seedance 2.5 (`t2v` / `omni_reference` /
`video_edit` / `video_extension`), 480p / 720p / 1080p, native audio, plus camera body / lens /
aperture / genre / era / pacing / light / color-palette params. The CLI schema states no duration
bounds — verify before promising a long take. Not yet field-rated; not yet documented in
`higgsfield-cinema`.

---

## Related skills
- `higgsfield-prompt` — MCSLA formula, prompt structure
- `higgsfield-cinema` — Cinema Studio model selection
- `higgsfield-assist` — Credit optimization and plan selection
- `higgsfield-audio` — Audio-capable model details
- `higgsfield-gpt-image-2` — GPT Image 2 / 2.5 prompting and when to prefer 2.5
- `templates/` — Annotated templates with per-genre model recommendations
