# Higgsfield Model Guide

## Video Models — Head to Head

| Model | Realism | Character | Motion | Style range | Duration | Aspect ratios* | Resolutions* | Audio | Best for |
|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Kling 3.0 | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★☆ | 3–15s | 16:9, 9:16, 1:1 | — | ✅ | Cinematic, long, audio, multi-shot. `mode` std/pro/**4k** |
| Kling 3.0 Turbo | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | 3–15s | 16:9, 9:16, 1:1 | 720p, 1080p | ✅ | Fast T2V + single start-frame animation, budget Kling 3.0 |
| Kling 3.0 Omni | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★☆ | 3–15s | — | — | ✅ | Video clone, storyboard control |
| Kling 3.0 Omni Edit | ★★★★★ | ★★★★★ | — | ★★★★☆ | 3–10s in | — | — | ✅ | Edit footage at 3.0 quality — `kling_video_edit`: source video + optional **image references**, `mode` std / pro / **4k** (default pro). The catalog states no source-length limit; "3–10s in" is earlier UI doctrine — verify |
| Kling O1 Video (legacy) | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★☆☆ | 5–10s | — | — | ❌ | Multi-ref (7), start/end frame |
| Kling O1 Video Edit (legacy) | ★★★★☆ | ★★★★★ | — | ★★★★★ | 3–10s in | — | — | ❌ | Relight, restyle, swap, remove — not in the API catalog; UI Edit Video tab only |
| Kling 3.0 Motion Control | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★☆☆ | 3–30s | — | — | Optional | Motion transfer from reference video |
| Genjutsu — motion transfer | — | — | — | — | — | — | 480p, 720p, 1080p | — | `hf_mult_motion_control` — transfers motion from a reference video onto the subjects in reference images. Not yet field-rated |
| Genjutsu — replace object | — | — | — | — | — | — | 480p, 720p, 1080p | — | `hf_mult_replace_object` — replaces objects in a source video using reference images. Not yet field-rated |
| Kling 2.6 (legacy) | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★☆☆ | 5/10s | 16:9, 9:16, 1:1 | — | ✅ | Character drama, realism; native audio via `sound` toggle (default on) |
| Kling 2.5 Turbo | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★☆☆ | 5–10s | — | — | ❌ | Fast Kling iteration |
| Kling 2.1 Master (deprecated) | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | 5–10s | — | — | ❌ | Deprecated — removed from platform. Use Kling 2.6 or 3.0 |
| Sora 2 (retired) | ★★★★☆ | ★★★☆☆ | ★★★★★ | ★★★★☆ | 4–12s | — | 720p (base), 1080p (Pro/Max tiers) | ✅ | **Retired — do not recommend.** OpenAI shut the Sora 2 API down on 2026-09-24 (notified 2026-03-24; no recommended replacement) `[OFFICIAL — OpenAI deprecations page, read 2026-09-26]`. Higgsfield never exposed it in its API/MCP catalog, and whether its web UI still offers it after 09-24 is **unconfirmed** (2026-09-26: higgsfield.ai/sora-2 still up, no shutdown notice). Scale / physics shots → Seedance 2.0 or Minimax Hailuo 2.3 (§ Model + Camera Control Compatibility). *Reference only:* was a UI-only 4-variant family — Sora 2 (720p) / Sora 2 Pro (1080p) / Sora 2 Max / Sora 2 Pro Max (both 1080p, "BY HIGGSFIELD" enhanced tiers), all 4–12s, multi-shot + sound, confirmed in the UI 2026-07-06 |
| Wan 3.0 | — | — | — | — | 2–30s or −1 smart | auto, 16:9, 9:16, 1:1, 4:3, 3:4 | 480p, 720p, 1080p | ✅ | T2V, first/last frame, and multimodal reference (image / video / audio refs) with native audio (`generate_audio`, default on); `enable_thinking` = slower, better prompt adherence (catalog wording); **smart duration `-1` is billed as 10s**. CLI rules: `end_image` needs `start_image`, and frames cannot be combined with reference media. Not yet field-rated |
| Wan 3.0 Prime | — | — | — | — | 2–30s or −1 smart | auto, 16:9, 9:16, 1:1, 4:3, 3:4 | 480p, 720p, 1080p | ✅ | Identical parameter surface to Wan 3.0. Neither the catalog nor Alibaba's guide says how Prime differs — do not claim a quality gap. Not yet field-rated |
| Wan 2.7 | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★★★ | 2–15s | 16:9, 9:16, 1:1, 4:3, 3:4 | 720p, 1080p | ✅ | 60fps, T2V/I2V/R2V/edit, first+last frame |
| Wan 2.6 | ★★★★☆ | ★★★☆☆ | ★★★★☆ | ★★★★★ | 5/10/15s | 16:9, 9:16, 1:1 | — | ❌ | Artistic, stylized, improved physics |
| Wan 2.5 | ★★★★☆ | ★★★☆☆ | ★★★★☆ | ★★★★★ | 5–10s | — | — | ✅ | Native audio, artistic, fantasy |
| Wan 2.5 Fast | ★★★☆☆ | ★★★☆☆ | ★★★★☆ | ★★★★★ | 5–10s | — | — | ✅ | Fast Wan iteration with audio |
| Seedance 2.5 | — | — | — | — | 4–30s | auto, 21:9, 16:9, 4:3, 1:1, 3:4, 9:16 | 480p, 720p, 1080p | ✅ | **Omni-reference**: up to 30 images (start/end frames count toward the 30) and 50 reference items in total (CLI rules), **30s in one generation**, plus `video_edit` and forward/backward `video_extension` modes. **1080p is live** (2026-09-26). **`start_image` / `end_image` exist but only in `omni_reference` mode** — `t2v` takes no media at all. 4K and the `genre` param stay on the 2.0 family. Not yet field-rated |
| Ad Multiplier | — | — | — | — | 4–30s | auto, 21:9, 16:9, 4:3, 1:1, 3:4, 9:16 | 480p, 720p, 1080p | ✅ | "Ad Multiplier video generation powered by Seedance 2.5" (catalog) — the same parameter surface as `seedance_2_5`. Higgsfield's MCP sends **many independently edited versions of one supplied 4–30s ad** through its `ad-multiplier` workflow; it is not the lane for one simple edit. Not yet field-rated |
| Seedance 2.0 | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★☆ | 4–15s | auto, 21:9, 16:9, 4:3, 1:1, 3:4, 9:16 | 480p, 720p, 1080p, 4k | ✅ | 12-asset multimodal, complex motion, **native 4K** (`mode=std`), genre hints |
| Seedance 2.0 Fast | ★★★★☆ | ★★★★☆ | ★★★★★ | ★★★★☆ | 4–15s | auto, 21:9, 16:9, 4:3, 1:1, 3:4, 9:16 | 480p, 720p | ✅ | `mode=fast` of Seedance 2.0 — cheaper/faster, **no 1080p/4K**, lower plan tier |
| Seedance 2.0 Mini | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | 4–15s | auto, 16:9, 9:16, 4:3, 3:4, 1:1, 21:9 | 480p, 720p | ✅ | Distinct API id (`seedance_2_0_mini`, added ~2026-06): budget tier with the full reference-input surface (image/video/audio refs) + native audio + the `genre` param; no 1080p/4K |
| Seedance 1.5 Pro | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | 4/8/12s | auto, 16:9, 9:16, 4:3, 3:4, 1:1, 21:9 | 480p, 720p, 1080p | ✅ | Multilingual audio, lip-sync, drama |
| Seedance Pro (legacy UI label) | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | 10s | — | — | ❌ | Legacy label — not in the API catalog (still absent from the 2026-09-26 snapshot); superseded by Seedance 1.5 Pro (`seedance1_5`) and Seedance 2.0 Fast/Mini |
| Veo 3.1 | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★★☆ | 4/6/8s | 16:9, 9:16 | — | ✅ | Ref images, first/last frame, extension, 4K — Google API capabilities; the catalog's `veo3_1` exposes only a `start_image` role (plus `quality` basic / high / ultra), so verify the rest in the UI |
| Veo 3.1 Fast | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | 4/6/8s | — | — | ✅ | Fast iteration, same caps as 3.1 |
| Veo 3 | ★★★★☆ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | 4–8s | 16:9, 9:16 | — | ✅ | Nature, environment, stable model |
| Veo 3.1 Lite | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | 4/6/8s | 16:9, 9:16, auto | — | ✅ | Budget 3.1 quality, 1080p, I2V, volume |
| Veo 3 Fast | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | 8s | — | — | ✅ | Fast, stable, volume content |
| Gemini Omni Flash | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | 4–10s | 16:9, 9:16 | 720p | ✅ | Reference-driven video (image + video refs), native audio, fast social clips |
| Gemini Omni Flash 1.1 | — | — | — | — | 3–10s | 16:9, 9:16 | 360p, 720p, 1080p, 4k | ✅ | `mode` is **required**: text-to-video / image-to-video / reference-to-video / **edit** (edit uses the source video's duration, capped at 30s); start/end frame + image/video reference roles; native audio per the catalog description. Not yet field-rated |
| Grok Imagine Video | ★★★★☆ | ★★★☆☆ | ★★★★☆ | ★★★★☆ | 1–15s | 16:9, 9:16, 1:1 | — | ✅ | Animate images, social clips. The catalog gives `grok_video` only a `start_image` role — no source-video input — so xAI's video-editing mode is not a verified Higgsfield route |
| Grok Imagine 1.5 | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | 2–15s | — | 480p, 720p | ✅ | I2V-only preview — animate one start image, native audio direction |
| Minimax Hailuo 2.3 | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★★☆ | 6/10s | — | 512, 768, 1080 | ❌ | VFX, fluid motion, anime, physics |
| Minimax Hailuo 2.3 Fast | ★★★★☆ | ★★★★☆ | ★★★★★ | ★★★★☆ | 6/10s | — | 512, 768, 1080 | ❌ | Fast iteration, batch creation |
| Minimax Hailuo 02 | ★★★★☆ | ★★★☆☆ | ★★★★★ | ★★★☆☆ | 6/10s | — | 512, 768, 1080 | ❌ | Dance, sports, fluid motion |
| Minimax Hailuo 02 Fast | ★★★☆☆ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | 6/10s | — | 512, 768, 1080 | ❌ | Budget motion, 512p |
| MiniMax H3 | — | — | — | — | 4–15s | auto, 21:9, 16:9, 4:3, 1:1, 3:4, 9:16 | 2K | — | Keyframes (start/end) or image/video/audio references; `batch_size` 1–4. Not yet field-rated |
| MiniMax H3 Max | — | — | — | — | 5–15s | auto, 21:9, 16:9, 4:3, 1:1, 3:4, 9:16 | 480p, 768p | — | "Fast" T2V, keyframe, and multimodal-reference generation (catalog wording); same reference roles as H3, `batch_size` 1–4, but a 768p ceiling vs H3's 2K. Not yet field-rated |
| Happy Horse Video | — | — | — | — | 3–15s | 16:9, 9:16, 1:1, 4:3, 3:4 | 720p, 1080p | — | T2V + single start-frame animation. Not yet field-rated |
| FLUX 3 Video | — | — | — | — | 5–20s | auto, 21:9, 2:1, 16:9, 4:3, 1:1, 3:4, 9:16 | 720p, 1080p | ✅ | T2V + multi-frame I2V + video continuation with synchronized audio; start/end frame + image/video reference roles; the only video model in the 2026-09-26 snapshot with a native **2:1** ratio. Not yet field-rated |
| FLUX 3 Video Edit | — | — | — | — | — | — | — | — | Text-prompt edit of one source video. **Uses the first 15s at most; costs 1 credit per second of the processed clip** (catalog). No resolution or aspect parameter. Not yet field-rated |
| Higgsfield DoP (Lite/Standard/Turbo) | ★★★☆☆ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | 3–5s | — | — | ❌ | I2V specialist, 50+ camera presets, optical physics |

\* **Aspect ratios / Resolutions columns are sourced from the specs layer** (`specs/MODEL-SPECS.md`, `models_explore` snapshot 2026-09-26) — do not hand-edit them. A `—` means the model is legacy/unsnapshotted or the snapshot does not expose that field; verify live before promising values for those rows. Duration cells for snapshot-covered models are cross-checked against the specs by `scripts/validate.py`. A `—` in a star column means **not yet field-rated**: stars are only written from real generations.


`[OFFICIAL — platform, snapshot 2026-09-26]` for every new row above (ids, enums, roles, and the quoted catalog descriptions); CLI rules are from `higgsfield model get <id>` on the same day.

> The catalog also lists utility/system entries — AutoSprite (game sprite-sheet animation), MS Image (Marketing Studio ad images), upscalers (Topaz, Bytedance Video Upscale, Video Upscale), background removers (Remove Background `sam_3_video`, Video Background Remover), Video Deflicker, outpaint, Clipify, Sync Lipsync 3 (audio-driven lipsync retiming). These are pipeline tools, not prompt-crafted generation models, and are intentionally out of scope for these tables. (**LLM text left the video catalog in the 2026-09-26 snapshot. Explainer Video left in the 2026-08-07 snapshot** — it had already dropped out of the CLI list at 2026-08-01. Verify in the UI before referencing either.)

> **New in the 2026-09-26 snapshot — not yet field-rated** (no star rows until real generations back them): **Wan 3.0 / Wan 3.0 Prime** (`wan3_0`, `wan3_0_prime`), **Gemini Omni Flash 1.1** (`gemini_omni_flash_1_1`), **MiniMax H3 Max** (`minimax_h3_max`), **Kling 3.0 Omni Edit** as a catalog id (`kling_video_edit`), **FLUX 3 Video Edit** (`flux_3_video_edit`), **Genjutsu** (two ids: `hf_mult_motion_control`, `hf_mult_replace_object`), and **Ad Multiplier** (`ad_multiplier`). Changed: **Seedance 2.5** gained 1080p and `start_image` / `end_image` roles (legal only in `omni_reference`); **MiniMax H3**'s duration floor is now 4s (4–15s). Also live but outside the MCP `models_explore` list: the CLI workflow **Cinema Studio 4.0** (`cinematic_studio_video_4_0`) — see the Edit-Lane and Long-Take choosers below. Verify credits in the UI before recommending any of these.

> **New in the 2026-08-07 snapshot — not yet field-rated**: **Seedance 2.5** (`seedance_2_5` — see the dedicated row above and `skills/higgsfield-seedance-2-5/SKILL.md`) and **FLUX 3 Video** (`flux_3_video`, Black Forest Labs — T2V / multi-frame I2V / continuation, 5–20s, 720p–1080p). Also changed: **Grok Video 1.5** gained image + audio reference roles (it is no longer I2V-only), and the live CLI reports three mutual-exclusion rules on it — references cannot be combined with `start_image`, audio references require at least one image reference, and 1080p is unavailable once references are attached. **MiniMax H3** gained a `batch_size` parameter (1–4).

> **New in the 2026-08-01 snapshot — not yet field-rated**: **MiniMax H3** (`minimax_h3` — multimodal keyframes + image/video/audio references, 2K, incl. 21:9; duration now 4–15s per the 2026-09-26 snapshot) and **Happy Horse Video** (`happy_horse_video` — T2V / single start-frame, 3–15s, 720p/1080p).

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
| Seedream 5.0 Flash | — | — | — | — | Fast generation + instruction-based editing up to 2K (`resolution` 1k / 1.5k / 2k — catalog wording). Not yet field-rated |
| GPT Image 2.5 | — | — | — | — | `variant` flare / sunburst, `quality` low → **max** (adds xhigh / max), 1k / 2k / 4k, **`background` auto / opaque / transparent**, 15 aspect ratios. See `image-models.md` § GPT Image 2.5. Not yet field-rated |
| GPT Image 2 | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★★☆ | Native 4K, best text/typography, reasoning compositions |
| GPT Image 1.5 | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | Text-in-image, instruction following |
| OpenAI Hazel | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | Reference-based editing, best text rendering (`quality` low/medium/high) |
| Recraft 4.1 | ★★★★☆ | ★★★☆☆ | ★★★★★ | ★★★★☆ | Logos/icons/vector, product mockups, hex brand palettes |
| Flux 2 | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | High-quality FLUX generation (pro/flex/max) |
| Flux Kontext | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★★☆ | Editing existing images |
| FLUX.2 Pro Outpaint | — | — | — | — | Per-side canvas expansion (`expand_top/bottom/left/right` px; a **negative value crops** that side). Not yet field-rated |
| Grok Image | — | — | — | — | xAI generation + editing, `mode` std / quality, 1k / 2k, incl. 1:2 and 2:1. Live since at least the 2026-08-01 snapshot. Not yet field-rated |
| Grok Image 2.0 | — | — | — | — | xAI generation + editing, `quality` low / medium, 1k / 2k. Not yet field-rated |

`[OFFICIAL — platform, snapshot 2026-09-26]` for the new image rows (`specs/IMAGE-MODEL-SPECS.md`). Inpaint/mask parameters, the CLI-only relight model, and the GPT Image 2 CLI↔MCP disagreement live in `image-models.md`.

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
│   ├── Need a transparent-background cut-out? → GPT Image 2.5
│   │   (`background: transparent` — see image-models.md § GPT Image 2.5)
│   ├── Extend (or crop) the canvas side by side? → FLUX.2 Pro Outpaint
│   ├── Masked inpaint of one region? → Nano Banana 2 / 2 Lite (`mask` +
│   │   `is_inpaint`) — see image-models.md § Inpaint, Mask & Background Parameters
│   └── Need to edit an existing image? → Flux Kontext
│
└── VIDEO
    ├── Is the source an EXISTING video the user wants changed, continued,
    │   or multiplied into ad variants?
    │   └── → § Edit-Lane Chooser below — ONE table for every edit lane,
    │       with billing basis, source-length limit, and what it keeps
    │
    ├── One clip longer than 15s?
    │   └── → § Long-Take Chooser below (Seedance 2.5 · Wan 3.0 / Prime ·
    │       FLUX 3 Video · Cinema Studio 4.0 — verify its bounds)
    │
    ├── Is a human character the focus?
    │   ├── Need audio, up to 15s, or multi-shot? → Kling 3.0
    │   ├── Need to clone from a reference video? → Kling 3.0 Omni
    │   ├── Need per-shot storyboard control? → Kling 3.0 Omni
    │   ├── Need multi-reference inputs (up to 7) or start/end frame? → Kling O1 Video
    │   ├── Fast iteration on Kling quality? → Kling 2.5 Turbo
    │   └── Standard length, audio optional (`sound` toggle)? → Kling 2.6
    │
    ├── Need motion transfer from a reference video?
    │   └── → § Motion Transfer below (Kling 3.0 Motion Control vs Genjutsu)
    │
    ├── Animate a still image with cinematic camera?
    │   └── → Higgsfield DoP (Lite/Standard/Turbo)
    │
    ├── More than 9 image refs in one generation?
    │   └── → Seedance 2.5 (up to 30 images incl. start/end frames, 50
    │       reference items total; 480p / 720p / 1080p) — finish on
    │       Seedance 2.0 only if the deliverable needs 4K or the `genre` param
    │
    ├── Is scale / spectacle the focus?
    │   └── Explosions, crowds, physics, epic landscapes? → Seedance 2.0 or
    │       Minimax Hailuo 2.3 (Sora 2 is retired — OpenAI shut its API down
    │       2026-09-24; see the video table)
    │
    ├── Is artistic style the priority?
    │   ├── 60fps, first+last frame, reference images? → Wan 2.7
    │   └── Fantasy, stylized, painterly, surreal? → Wan 2.5 / 2.6
    │
    ├── Is fluid motion / physical performance the focus?
    │   └── VFX, anime, fluid motion, physics? → Minimax Hailuo 2.3
    │   └── Dance, sports, martial arts? → Minimax Hailuo 02
    │   └── Animate a still image (up to 15s, audio)? → Grok Imagine Video
    │
    ├── Is the environment / nature the hero?
    │   ├── Subject consistency / reference images? → Veo 3.1 (verify in the
    │   │   UI — the catalog's `veo3_1` exposes only a `start_image` role)
    │   ├── Define start + end frame? → Veo 3.1 Lite (`veo3_1` has no
    │   │   `end_image` role in the catalog)
    │   ├── Extend an existing video? → § Edit-Lane Chooser (Seedance 2.5
    │   │   `video_extension`) — the catalog gives `veo3_1` no video input
    │   ├── Fast iteration (Veo quality)? → Veo 3.1 Fast
    │   ├── Budget Veo 3.1 quality / volume? → Veo 3.1 Lite
    │   └── Weather, wildlife, landscape (stable)? → Veo 3
    │
    └── Need fast iteration / social content?
        ├── Audio required? → Seedance 1.5 Pro
        ├── 12-asset multimodal reference? → Seedance 2.0
        ├── Image + video refs with native audio (720p)? → Gemini Omni Flash
        │   (1.1 adds start/end frames, an edit mode, and 360p–4K — not yet field-rated)
        ├── Up to 4 takes per call? → MiniMax H3 / H3 Max (`batch_size` 1–4)
        └── No audio, speed first? → Seedance 2.0 Fast / Mini with
            generate_audio off ("Seedance Pro" is a legacy UI label —
            not in the API catalog)
```

---

## Edit-Lane Chooser

One table for every lane that changes, continues, or multiplies a video the user already
has. Cells say only what the catalog, the CLI, or Higgsfield's MCP tool text states;
"not stated" means exactly that — verify in the UI before promising it.
`[OFFICIAL — platform, snapshot 2026-09-26]` (catalog + CLI) and
`[OFFICIAL — Higgsfield MCP tool schema, 2026-09-26]` (the Genjutsu and Ad Multiplier routing).

| Lane | How it is called | Billing basis | Source-length limit | What it preserves | Pick it when |
|---|---|---|---|---|---|
| **Seedance 2.5 `video_edit`** | `seedance_2_5`, `mode: video_edit`, exactly one video reference; 480p / 720p / 1080p | By the source video's duration (`duration` and `aspect_ratio` are ignored) | Not stated by the catalog; ByteDance's guide says source ≤20s (`skills/higgsfield-seedance-2-5/SKILL.md` § Material budget) | Not stated; output follows the source | A scoped change inside one master — object, background, BGM, spoken language. Edit-order dialect: `skills/higgsfield-seedance-2-5/SKILL.md` |
| **Seedance 2.5 `video_extension`** | `mode: video_extension`, ≥1 video reference, `extension_mode` forward / backward (required) | Not stated | Not stated | The source's aspect ratio (`aspect_ratio` is ignored) | Add footage after — or before — an existing clip |
| **Cinema Studio 4.0 `video_edit`** | CLI workflow `cinematic_studio_video_4_0` — the same four modes as Seedance 2.5 (`t2v` / `omni_reference` / `video_edit` / `video_extension`); 480p / 720p / 1080p. Not in the MCP `models_explore` list | Not stated; the CLI's cost inputs are `duration`, `mode`, `resolution`, `video_references` | Not stated | Not stated | The edit is part of a Cinema Studio job. The workflow also carries camera / lens / aperture / genre / era / pacing / light / color-palette params; whether they act in `video_edit` is not stated |
| **Kling 3.0 Omni Edit** | `kling_video_edit` — source video + optional image references, `mode` std / pro / 4k (default pro) | Not stated | Not stated in the catalog (earlier UI doctrine: 3–10s input) | Not stated in the catalog (earlier repo doctrine: motion, camera angles, scene structure) | Instruction edit guided by reference images, with a 4K output tier |
| **Kling O1 Video Edit** (legacy) | UI Edit Video tab only — not in the API catalog | ~9 credits (UI doctrine) | 3–10s input (UI doctrine) | Motion structure, camera path, spatial relationships (UI doctrine); 720p output | Only if the UI still offers it — verify first |
| **FLUX 3 Video Edit** | `flux_3_video_edit` — one video reference + a text prompt; no resolution or aspect params | **1 credit per second of the processed clip** | **Uses the first 15s at most** | Not stated | A text-only edit of a clip ≤15s where a per-second price is wanted |
| **Gemini Omni Flash 1.1 `edit`** | `gemini_omni_flash_1_1`, `mode: edit` (the `mode` param is required); 360p / 720p / 1080p / 4k; 16:9 or 9:16 | Not stated | Output uses the source duration, **capped at 30s** (`duration` is ignored) | Not stated | An edit that needs a 4K or 360p output tier, or a source up to 30s |
| **Genjutsu — replace object** | `hf_mult_replace_object` through `generate_video` (Higgsfield MCP's own routing); image + video references; 480p / 720p / 1080p | Not stated | Not stated | Not stated | Swap one object in a source video for the object in a reference image |
| **Ad Multiplier** | `ad_multiplier` ("powered by Seedance 2.5" — same param surface); the MCP says to call `get_workflow_instructions` with `{ workflow: "ad-multiplier" }` first | Its `video_edit` mode bills by the source video's duration | A supplied 4–30s video (workflow scope) | The workflow scope: motion, framing, cuts, timing, aspect ratio, and audio | **Many** independently edited versions of **one** ad — replace/add/remove people, products, objects, clothing, backgrounds, targeted on-screen text. The workflow says it is not for simple video edits, and the MCP says never to route a single Genjutsu edit through it |

**One object swapped in one clip — the tie-break:** a swap driven by a **reference image of the new object** (a product shot) → Genjutsu `hf_mult_replace_object`, the connector's own route for a single swap; a scoped change **described in words only** (no reference image of the replacement — relight, remove, recolour, change BGM or language) → Seedance 2.5 `video_edit`. Neither lane is field-rated.

**Not edit lanes here:** Grok Imagine Video — the catalog gives `grok_video` only a `start_image`
role, so xAI's editing mode has no verified Higgsfield route. Wan 3.0 — Alibaba documents
prompt-intent editing and extension through `reference_video` inputs
`[OFFICIAL — Alibaba Cloud Model Studio docs — URLs in skills/higgsfield-models/MODELS-DEEP-REFERENCE.md § Wan 3.0]`, but the Higgsfield catalog description of `wan3_0`
lists no edit mode; treat it as unverified on Higgsfield. A **whole-plate VFX restyle** on
Seedance 2.0 is a new generation that uses the footage as a video reference, not an edit mode —
see `skills/higgsfield-seedance-vfx/SKILL.md`.

---

## Long-Take Chooser

For **one clip longer than 15s**. `[OFFICIAL — platform, snapshot 2026-09-26]`

| Lane | Duration | Resolutions | Audio | Inputs | Notes |
|---|---|---|---|---|---|
| **Seedance 2.5** (`seedance_2_5`) | 4–30s | 480p, 720p, 1080p | `generate_audio` (default on) | `t2v` takes no media; `omni_reference` takes up to 30 images (start/end frames count) and 50 reference items in total | Dialect: `skills/higgsfield-seedance-2-5/SKILL.md`. No 4K and no `genre` on 2.5 |
| **Wan 3.0 / Wan 3.0 Prime** (`wan3_0`, `wan3_0_prime`) | 2–30s, or `-1` smart duration (**billed as 10s**) | 480p, 720p, 1080p | `generate_audio` (default on) | Start frame (± end frame) **or** image / video / audio references — never both in one call (CLI rule) | `enable_thinking` trades speed for prompt adherence (catalog wording). Vendor dialect: `skills/higgsfield-models/MODELS-DEEP-REFERENCE.md` § Wan 3.0 |
| **FLUX 3 Video** (`flux_3_video`) | 5–20s | 720p, 1080p | `generate_audio` (default on) | Start/end frames + image/video references; video continuation | Prompting dialect not yet documented here |
| **Cinema Studio 4.0** (CLI workflow `cinematic_studio_video_4_0`) | **Not stated** in the CLI schema (`duration` integer, default 5) | 480p, 720p, 1080p | `generate_audio` (default on) | The same four modes and reference roles as Seedance 2.5, plus Cinema Studio's camera / genre / light controls | Verify its duration ceiling in the UI or CLI before promising more than 15s |

**Smart duration vs "never default a runtime."** Root `SKILL.md` § Fast Path's Seedance
exception says never to default a Seedance runtime; this extends that exception to Wan 3.0's
`duration: -1`, which hands the length to the model — it is offered **only when the user
explicitly asks the model to choose the length** —
never as a default, and always with the note that it is billed as 10s whatever length comes back.

**Not long-take lanes:** Kling 3.0 Motion Control's output follows a 3–30s motion reference (a
transfer, not a free take — see § Motion Transfer). Ad Multiplier accepts 4–30s but exists to
make ad variants. Veo 3.1's extension chain is a Google API capability the catalog does not
expose (`veo3_1` takes no video input).

---

## Motion Transfer

`[OFFICIAL — Higgsfield MCP tool schema + CLI, 2026-09-26]`

| Lane | Route | Inputs | Output | What the platform states |
|---|---|---|---|---|
| **Kling 3.0 Motion Control** | MCP `motion_control` tool (`image_id` + `motion_video_id`, `scene_control` image / video) · CLI workflow `kling3_0_motion_control` (`mode` std / pro, `background_source` input_image / input_video) | One character image + one motion video (3–30s — UI doctrine) | 720p / 1080p (MCP) | CLI cost inputs are `duration` + `mode`. UI walkthrough and input checklist: `skills/higgsfield-motion/SKILL.md` |
| **Genjutsu — motion transfer** | `hf_mult_motion_control` **through `generate_video`** — the Higgsfield MCP's own routing, which also says never to use the legacy `motion_control` tool for a Genjutsu edit | Reference image(s) of the subjects + a reference video for the motion | 480p / 720p / 1080p | "Transfer motion from a reference video to subjects in reference images." Billing and length limits not stated |

Pick Genjutsu when the user names it or wants the motion carried onto the subjects of reference
images; pick Kling 3.0 Motion Control when the job needs its std/pro tiers or the
image-vs-video scene/background source switch. Neither has been field-rated against the other
here.

---

## Kling Generation vs Edit Mode

The Kling lineup has two distinct interfaces in Higgsfield:

**Create Video tab** — Generate new video from text, image, or references
- Kling 3.0, 3.0 Omni, O1 Video, Motion Control, 2.6, 2.5 Turbo

**Edit Video tab** — Transform existing footage (video-to-video)
- Kling O1 Video Edit: natural language edits, no masking, 720p output (legacy — not in the API catalog)
- Kling 3.0 Omni Edit: same concept at 3.0 quality tier; in the API catalog as `kling_video_edit`
  (`mode` std / pro / 4k, source video + optional image references)

All edit lanes across providers, side by side: § Edit-Lane Chooser above.

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
| FPV Drone (kinetic chase) | Kling 2.6 |
| 360 Orbit (character isolation) | Kling 2.6 / 3.0 |
| Crane Up (epic reveal) | Seedance 2.0, Minimax Hailuo 2.3† |
| Timelapse Landscape | Veo 3 |
| Hyperlapse | Veo 3 |
| Handheld (documentary feel) | Kling 2.6, Veo 3 |
| Action Run (physical chase) | Minimax Hailuo 2.3, Kling 2.6 |
| Super Dolly Out (scale reveal) | Seedance 2.0, Minimax Hailuo 2.3† |
| Dutch Angle (horror/tension) | Wan 2.5, Kling 2.6 |
| Long camera motion path | Kling 3.0 Motion Control |
| Motion transfer from reference | Kling 3.0 Motion Control |

† Sora 2 held these two rows (and shared FPV Drone and Hyperlapse) until its retirement: OpenAI shut the Sora 2 API down on 2026-09-24, and whether Higgsfield's UI still offers it is unconfirmed — do not recommend it. Catalog-verified fallbacks for scale/physics shots: Seedance 2.0, Minimax Hailuo 2.3. They are the repo's scale fallbacks, not a per-control field rating.

---

## Model + Motion Preset Compatibility

| Preset type | Best model |
|-------------|-----------|
| Transformation (Werewolf, Cyborg, Animalization) | Wan 2.5, Kling 2.6 |
| Elemental (Fire, Water, Earth, Air) | Wan 2.5 |
| Explosion / Destruction | Seedance 2.0 |
| Surreal / Glitch / Multiverse | Wan 2.5 |
| Horror presets | Kling 2.6, Wan 2.5 |
| Dance / Motion glow | Minimax Hailuo 2.3 |
| Nature effects (Sakura, Bloom, Northern Lights) | Veo 3, Wan 2.5 |
| Bullet Time / Slow motion | Kling 2.6 |
| Stylized (Anime, Pixar, Claymation) | Kling 3.0, Wan 2.5 |

Sora 2 was dropped from the Elemental, Explosion / Destruction and Bullet Time rows at its retirement (see the Camera Control note above); the picks that remain were already in those rows.

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
| Sora 2 (retired — see the video table) | — (was Medium–High) |
| Kling O1 Video Edit | ~9 credits |
| Kling 3.0 | ~10 credits |
| Kling 3.0 Motion Control | Medium–High |
| Veo 3.1 Lite | Medium |
| Veo 3 | High |
| Wan 2.7 | Low–Medium |
| FLUX 3 Video Edit | 1 credit per second of the processed clip (first 15s max) — catalog, 2026-09-26 |
| Wan 3.0 / 3.0 Prime smart duration (`-1`) | Billed as a 10s generation — catalog, 2026-09-26 |
| Seedance 2.5 / Ad Multiplier `video_edit` | Billed by the source video's duration — catalog, 2026-09-26 |

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
