# Higgsfield Model Guide

## Video Models — Head to Head

| Model | Realism | Character | Motion | Style range | Duration | Aspect ratios* | Resolutions* | Audio | Best for |
|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Kling 3.0 | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★☆ | 3–15s | 16:9, 9:16, 1:1 | — | ✅ | Cinematic, long, audio, multi-shot. `mode` std/pro/**4k** |
| Kling 3.0 Turbo | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | 3–15s | 16:9, 9:16, 1:1 | 720p, 1080p | ✅ | Fast T2V + single start-frame animation, budget Kling 3.0 |
| Kling 3.0 Omni | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★☆ | 3–15s | — | — | ✅ | Video clone, storyboard control |
| Kling 3.0 Omni Edit | ★★★★★ | ★★★★★ | — | ★★★★☆ | 3–10s in | — | — | ✅ | Edit footage at 3.0 quality |
| Kling O1 Video (legacy) | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★☆☆ | 5–10s | — | — | ❌ | Multi-ref (7), start/end frame |
| Kling O1 Video Edit (legacy) | ★★★★☆ | ★★★★★ | — | ★★★★★ | 3–10s in | — | — | ❌ | Relight, restyle, swap, remove |
| Kling 3.0 Motion Control | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★☆☆ | 3–30s | — | — | Optional | Motion transfer from reference video |
| Kling 2.6 (legacy) | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★☆☆ | 5/10s | 16:9, 9:16, 1:1 | — | ✅ | Character drama, realism; native audio via `sound` toggle (default on) |
| Kling 2.5 Turbo | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★☆☆ | 5–10s | — | — | ❌ | Fast Kling iteration |
| Kling 2.1 Master (deprecated) | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | 5–10s | — | — | ❌ | Deprecated — removed from platform. Use Kling 2.6 or 3.0 |
| Sora 2 (UI-only) | ★★★★☆ | ★★★☆☆ | ★★★★★ | ★★★★☆ | 4–12s | — | 720p (base), 1080p (Pro/Max tiers) | ✅ | Epic scale, physics, action, multi-shot + sound — **UI-only, confirmed present in the UI 2026-07-06** as a 4-variant family: Sora 2 (720p) / Sora 2 Pro (1080p) / Sora 2 Max / Sora 2 Pro Max (both 1080p, "BY HIGGSFIELD" enhanced tiers), all 4–12s. Not in the API/MCP catalog — UI generations only |
| Wan 2.7 | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★★★ | 2–15s | 16:9, 9:16, 1:1, 4:3, 3:4 | 720p, 1080p | ✅ | 60fps, T2V/I2V/R2V/edit, first+last frame |
| Wan 2.6 | ★★★★☆ | ★★★☆☆ | ★★★★☆ | ★★★★★ | 5/10/15s | 16:9, 9:16, 1:1 | — | ❌ | Artistic, stylized, improved physics |
| Wan 2.5 | ★★★★☆ | ★★★☆☆ | ★★★★☆ | ★★★★★ | 5–10s | — | — | ✅ | Native audio, artistic, fantasy |
| Wan 2.5 Fast | ★★★☆☆ | ★★★☆☆ | ★★★★☆ | ★★★★★ | 5–10s | — | — | ✅ | Fast Wan iteration with audio |
| Seedance 2.5 | — | — | — | — | 4–30s | auto, 21:9, 16:9, 4:3, 1:1, 3:4, 9:16 | 480p, 720p | ✅ | **Omni-reference**: 30 images / 10 videos / 10 audio refs, **30s in one generation**, plus `video_edit` and forward/backward `video_extension` modes. **No 1080p/4K, no start/end-frame role, no genre hint.** Not yet field-rated |
| Seedance 2.0 | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★☆ | 4–15s | auto, 21:9, 16:9, 4:3, 1:1, 3:4, 9:16 | 480p, 720p, 1080p, 4k | ✅ | 12-asset multimodal, complex motion, **native 4K** (`mode=std`), genre hints |
| Seedance 2.0 Fast | ★★★★☆ | ★★★★☆ | ★★★★★ | ★★★★☆ | 4–15s | auto, 21:9, 16:9, 4:3, 1:1, 3:4, 9:16 | 480p, 720p | ✅ | `mode=fast` of Seedance 2.0 — cheaper/faster, **no 1080p/4K**, lower plan tier |
| Seedance 2.0 Mini | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | 4–15s | auto, 16:9, 9:16, 4:3, 3:4, 1:1, 21:9 | 480p, 720p | ✅ | Distinct API id (`seedance_2_0_mini`, added ~2026-06): budget tier with the full reference-input surface (image/video/audio refs) + native audio; no 1080p/4K |
| Seedance 1.5 Pro | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | 4/8/12s | auto, 16:9, 9:16, 4:3, 3:4, 1:1, 21:9 | 480p, 720p, 1080p | ✅ | Multilingual audio, lip-sync, drama |
| Seedance Pro (legacy UI label) | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | 10s | — | — | ❌ | Legacy label — not in the API catalog (2026-07-05 snapshot); superseded by Seedance 1.5 Pro (`seedance1_5`) and Seedance 2.0 Fast/Mini |
| Veo 3.1 | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★★☆ | 4/6/8s | 16:9, 9:16 | — | ✅ | Ref images, first/last frame, extension, 4K |
| Veo 3.1 Fast | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | 4/6/8s | — | — | ✅ | Fast iteration, same caps as 3.1 |
| Veo 3 | ★★★★☆ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | 4–8s | 16:9, 9:16 | — | ✅ | Nature, environment, stable model |
| Veo 3.1 Lite | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | 4/6/8s | 16:9, 9:16, auto | — | ✅ | Budget 3.1 quality, 1080p, I2V, volume |
| Veo 3 Fast | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | 8s | — | — | ✅ | Fast, stable, volume content |
| Gemini Omni Flash | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | 4–10s | 16:9, 9:16 | 720p | ✅ | Reference-driven video (image + video refs), native audio, fast social clips |
| Grok Imagine Video | ★★★★☆ | ★★★☆☆ | ★★★★☆ | ★★★★☆ | 1–15s | 16:9, 9:16, 1:1 | — | ✅ | Video editing, animate images, social clips |
| Grok Imagine 1.5 | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | 2–15s | — | 480p, 720p | ✅ | I2V-only preview — animate one start image, native audio direction |
| Minimax Hailuo 2.3 | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★★☆ | 6/10s | — | 512, 768, 1080 | ❌ | VFX, fluid motion, anime, physics |
| Minimax Hailuo 2.3 Fast | ★★★★☆ | ★★★★☆ | ★★★★★ | ★★★★☆ | 6/10s | — | 512, 768, 1080 | ❌ | Fast iteration, batch creation |
| Minimax Hailuo 02 | ★★★★☆ | ★★★☆☆ | ★★★★★ | ★★★☆☆ | 6/10s | — | 512, 768, 1080 | ❌ | Dance, sports, fluid motion |
| Minimax Hailuo 02 Fast | ★★★☆☆ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | 6/10s | — | 512, 768, 1080 | ❌ | Budget motion, 512p |
| FLUX 3 Video | — | — | — | — | 5–20s | auto, 21:9, 2:1, 16:9, 4:3, 1:1, 3:4, 9:16 | 720p, 1080p | ✅ | T2V + multi-frame I2V + video continuation with synchronized audio; start/end frame + image/video reference roles; only model in the catalog with a native **2:1** ratio. Not yet field-rated |
| Higgsfield DoP (Lite/Standard/Turbo) | ★★★☆☆ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | 3–5s | — | — | ❌ | I2V specialist, 50+ camera presets, optical physics |

\* **Aspect ratios / Resolutions columns are sourced from the specs layer** (`specs/MODEL-SPECS.md`, `models_explore` snapshot 2026-08-07) — do not hand-edit them. A `—` means the model is legacy/unsnapshotted or the snapshot does not expose that field; verify live before promising values for those rows. Duration cells for snapshot-covered models are cross-checked against the specs by `scripts/validate.py`.

> The catalog also lists utility/system entries — AutoSprite (game sprite-sheet animation), MS Image (Marketing Studio ad images), LLM text, upscalers, background removers, outpaint, Sync Lipsync 3 (audio-driven lipsync retiming). These are pipeline tools, not prompt-crafted generation models, and are intentionally out of scope for these tables. (**Explainer Video left the catalog in the 2026-08-07 snapshot** — it had already dropped out of the CLI list at 2026-08-01. Verify in the UI before referencing it.)

> **New in the 2026-08-07 snapshot — not yet field-rated** (no star rows until real generations back them): **Seedance 2.5** (`seedance_2_5` — see the dedicated row above and `skills/higgsfield-seedance-2-5/SKILL.md`) and **FLUX 3 Video** (`flux_3_video`, Black Forest Labs — T2V / multi-frame I2V / continuation, 5–20s, 720p–1080p). Also changed: **Grok Video 1.5** gained image + audio reference roles (it is no longer I2V-only), and the live CLI reports three mutual-exclusion rules on it — references cannot be combined with `start_image`, audio references require at least one image reference, and 1080p is unavailable once references are attached. **MiniMax H3** gained a `batch_size` parameter (1–4). Enums per `specs/MODEL-SPECS.md`; verify credits in the UI before recommending.

> **New in the 2026-08-01 snapshot — not yet field-rated**: **MiniMax H3** (`minimax_h3` — multimodal keyframes + image/video/audio references, 5–15s, 2K, incl. 21:9) and **Happy Horse Video** (`happy_horse_video` — T2V / single start-frame, 3–15s, 720p/1080p).

## Image Models — Head to Head

| Model | Quality | Faces | Style range | Speed | Best for |
|-------|---------|-------|-------------|-------|----------|
| Soul 2.0 | ★★★★★ | ★★★★★ | ★★★☆☆ | ★★★★☆ | Fashion, portrait, aesthetic |
| Soul Cinema Preview | ★★★★★ | ★★★★★ | ★★★☆☆ | ★★★★☆ | Cinematic keyframes, close-ups, film grain |
| Soul Cast | ★★★★☆ | ★★★★★ | ★★★☆☆ | ★★★☆☆ | Consistent cinematic character identity (16:9, `budget` 10–500) |
| Soul Location | ★★★★☆ | — | ★★★☆☆ | ★★★★☆ | Environment / location generation, 9 aspect ratios incl. 21:9 + 9:21 |
| Kling Image 3.0 | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★★☆ | Native 4K, series mode, storyboarding |
| Kling Image 3.0 Omni | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★★☆ | Advanced editing, strongest prompt fidelity |
| Nano Banana Pro | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★☆☆ | Max fidelity, Thinking mode, 14 refs |
| Nano Banana 2 | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★★☆ | Fast pro-quality, text rendering, consistency |
| Nano Banana 2 Lite | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★★ | Budget NB2 — 1k only, `thinking` MINIMAL/HIGH |
| Seedream 4.5 | ★★★★☆ | ★★★★★ | ★★★★★ | ★★★★☆ | Reference consistency, dense text, 4K |
| Seedream 5.0 Lite | ★★★★☆ | ★★★★☆ | ★★★★★ | ★★★★★ | Reasoning, search, multi-output, layouts |
| GPT Image 2 | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★★☆ | Native 4K, best text/typography, reasoning compositions |
| GPT Image 1.5 | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | Text-in-image, instruction following |
| OpenAI Hazel | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | Reference-based editing, best text rendering (`quality` low/medium/high) |
| Recraft 4.1 | ★★★★☆ | ★★★☆☆ | ★★★★★ | ★★★★☆ | Logos/icons/vector, product mockups, hex brand palettes |
| Flux 2 | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | High-quality FLUX generation (pro/flex/max) |
| Flux Kontext | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★★☆ | Editing existing images |

---

## Decision Flowchart

```
Is this image or video?
├── IMAGE
│   ├── Is it a person / portrait? → Soul 2.0
│   ├── Need cinematic keyframe for I2V pipeline? → Soul Cinema Preview
│   ├── Same character identity across many shots? → Soul Cast
│   ├── Environment / location plate? → Soul Location
│   ├── Need native 4K / image series / storyboarding? → Kling Image 3.0
│   ├── Need maximum sharpness / 4K? → Nano Banana Pro
│   ├── Fast pro-quality / text rendering / consistency? → Nano Banana 2
│   ├── Need reference consistency or dense text? → Seedream 4.5
│   ├── Complex layout / real-time data / multi-panel output? → Seedream 5.0 Lite
│   └── Need to edit an existing image? → Flux Kontext
│
└── VIDEO
    ├── Do you want to EDIT existing footage?
    │   ├── Relight, restyle, swap, remove, transform? → Kling O1 Video Edit (Edit Video tab)
    │   └── Higher quality edit with 3.0 architecture? → Kling 3.0 Omni Edit
    │
    ├── Is a human character the focus?
    │   ├── Need audio, long clip (up to 15s), or multi-shot? → Kling 3.0
    │   ├── Need to clone from a reference video? → Kling 3.0 Omni
    │   ├── Need per-shot storyboard control? → Kling 3.0 Omni
    │   ├── Need multi-reference inputs (up to 7) or start/end frame? → Kling O1 Video
    │   ├── Fast iteration on Kling quality? → Kling 2.5 Turbo
    │   └── Standard length, audio optional (`sound` toggle)? → Kling 2.6
    │
    ├── Need motion transfer from reference video?
    │   └── → Kling 3.0 Motion Control
    │
    ├── Animate a still image with cinematic camera?
    │   └── → Higgsfield DoP (Lite/Standard/Turbo)
    │
    ├── Need very long camera motion (up to 30s)?
    │   └── → Kling 3.0 Motion Control
    │
    ├── Is the source an EXISTING video the user wants changed or continued?
    │   ├── Change one thing inside it (object, background, BGM, spoken
    │   │   language)? → Seedance 2.5 `video_edit`
    │   ├── Add footage after — or before — it? → Seedance 2.5
    │   │   `video_extension` (forward / backward)
    │   └── Restyle / VFX-transform the whole plate? → Seedance 2.0
    │       (skills/higgsfield-seedance-vfx) or Grok Imagine Video
    │
    ├── One clip longer than 15s, or more than 9 image refs?
    │   └── → Seedance 2.5 (4–30s, 30 image / 10 video / 10 audio refs) —
    │       accepting the 720p ceiling; finish on Seedance 2.0 if the
    │       deliverable needs 1080p/4K
    │
    ├── Is scale / spectacle the focus?
    │   └── Explosions, crowds, physics, epic landscapes? → Seedance 2.0 or
    │       Minimax Hailuo 2.3 (Sora 2 is UI-only — not in the API catalog
    │       as of 2026-07-05; verify in the live UI before using it)
    │
    ├── Is artistic style the priority?
    │   ├── 60fps, first+last frame, reference images? → Wan 2.7
    │   └── Fantasy, stylized, painterly, surreal? → Wan 2.5 / 2.6
    │
    ├── Is fluid motion / physical performance the focus?
    │   └── VFX, anime, fluid motion, physics? → Minimax Hailuo 2.3
    │   └── Dance, sports, martial arts? → Minimax Hailuo 02
    │   └── Video editing / restyle existing footage? → Grok Imagine Video
    │   └── Animate a still image (10s, audio)? → Grok Imagine Video
    │
    ├── Is the environment / nature the hero?
    │   ├── Subject consistency / reference images? → Veo 3.1
    │   ├── Define start + end frame? → Veo 3.1
    │   ├── Extend existing Veo video? → Veo 3.1
    │   ├── Fast iteration (Veo quality)? → Veo 3.1 Fast
    │   ├── Budget Veo 3.1 quality / volume? → Veo 3.1 Lite
    │   └── Weather, wildlife, landscape (stable)? → Veo 3
    │
    └── Need fast iteration / social content?
        ├── Audio required? → Seedance 1.5 Pro
        ├── 12-asset multimodal reference? → Seedance 2.0
        ├── Image + video refs with native audio (720p)? → Gemini Omni Flash
        └── No audio, speed first? → Seedance 2.0 Fast / Mini with
            generate_audio off ("Seedance Pro" is a legacy UI label —
            not in the API catalog)
```

---

## Kling Generation vs Edit Mode

The Kling lineup has two distinct interfaces in Higgsfield:

**Create Video tab** — Generate new video from text, image, or references
- Kling 3.0, 3.0 Omni, O1 Video, Motion Control, 2.6, 2.5 Turbo

**Edit Video tab** — Transform existing footage (video-to-video)
- Kling O1 Video Edit: natural language edits, no masking, 720p output
- Kling 3.0 Omni Edit: same concept at 3.0 quality tier

Key distinction: Edit mode preserves the original motion structure, camera path, and spatial relationships of your source footage. You're transforming the look/content, not the movement.

### Edit Prompt Formula
`Change [Target] to [New State], keep [everything else] unchanged`

Examples:
- "Change the lighting to golden hour dusk, keep character and motion unchanged"
- "Restyle as 1970s film grain, keep all composition"
- "Remove the background person, keep everything else exactly as is"

---

## Model + Camera Control Compatibility

Some camera controls perform better on certain models:

| Camera Control | Best model |
|----------------|-----------|
| Dolly In (emotional close-up) | Kling 2.6 / 3.0 |
| FPV Drone (kinetic chase) | Kling 2.6, Sora 2† |
| 360 Orbit (character isolation) | Kling 2.6 / 3.0 |
| Crane Up (epic reveal) | Sora 2† |
| Timelapse Landscape | Veo 3 |
| Hyperlapse | Veo 3, Sora 2† |
| Handheld (documentary feel) | Kling 2.6, Veo 3 |
| Action Run (physical chase) | Minimax Hailuo 2.3, Kling 2.6 |
| Super Dolly Out (scale reveal) | Sora 2† |
| Dutch Angle (horror/tension) | Wan 2.5, Kling 2.6 |
| Long camera motion path | Kling 3.0 Motion Control |
| Motion transfer from reference | Kling 3.0 Motion Control |

† Sora 2 is UI-only — not in the API catalog as of 2026-07-05; verify in the live UI before recommending. Catalog-verified fallbacks for scale/physics shots: Seedance 2.0, Minimax Hailuo 2.3.

---

## Model + Motion Preset Compatibility

| Preset type | Best model |
|-------------|-----------|
| Transformation (Werewolf, Cyborg, Animalization) | Wan 2.5, Kling 2.6 |
| Elemental (Fire, Water, Earth, Air) | Wan 2.5, Sora 2† |
| Explosion / Destruction | Sora 2†, Seedance 2.0 |
| Surreal / Glitch / Multiverse | Wan 2.5 |
| Horror presets | Kling 2.6, Wan 2.5 |
| Dance / Motion glow | Minimax Hailuo 2.3 |
| Nature effects (Sakura, Bloom, Northern Lights) | Veo 3, Wan 2.5 |
| Bullet Time / Slow motion | Kling 2.6, Sora 2† |
| Stylized (Anime, Pixar, Claymation) | Kling 3.0, Wan 2.5 |

† Sora 2 is UI-only — not in the API catalog as of 2026-07-05; verify in the live UI before recommending (see the Camera Control note above).

---

## Credit Cost Reference (approximate)

| Model | Credit cost per generation |
|-------|-----------------------------|
| Seedance Pro (legacy UI label — see video table) | Low |
| Kling 2.5 Turbo | Low–Medium |
| Wan 2.5 | Low–Medium |
| Minimax Hailuo 2.3 | Medium |
| Minimax Hailuo 02 | Medium |
| Kling 2.6 | Medium |
| Sora 2 (UI-only — verify live) | Medium–High |
| Kling O1 Video Edit | ~9 credits |
| Kling 3.0 | ~10 credits |
| Kling 3.0 Motion Control | Medium–High |
| Veo 3.1 Lite | Medium |
| Veo 3 | High |
| Wan 2.7 | Low–Medium |
| Wan 2.5 | Low–Medium |

Plans: Free (25 credits/mo) · Basic $6/mo (150) · Pro $27/mo (700) · Ultimate $55/mo (1500)

---

## Higgsfield DoP — Image-to-Video Specialist

Higgsfield DoP is Higgsfield's native Image-to-Video (I2V) system with three quality tiers:
- **Higgsfield Lite** — 720p, 3–5s, fastest
- **Higgsfield Standard** — 720p, 3–5s, balanced
- **Higgsfield Turbo** — 720p, 3–5s, highest quality

**What makes DoP unique:**
- Specialized I2V generative model — designed for animating static images
- 50+ cinematic camera presets (Bullet Time, Crash Zoom, 360 Orbit, Robo Arm, FPV Drone, etc.)
- Simulates real-world optical physics: bokeh, parallax, natural lighting shifts as camera moves through 3D-mapped environment
- Multi-Frame Guidance: starting image + "last frame" reference for seamless transitions
- Preset categories: All, New, Trending, Effects, Basic Camera Control, Epic Camera Control, Catch the Pulse, Mix

**Best for:** Social media ads, product showcases, film pre-visualization, animating hero images with cinematic camera movement
