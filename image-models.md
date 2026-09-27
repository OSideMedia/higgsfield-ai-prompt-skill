# Higgsfield Image Models — Complete Reference

> **Specs snapshot: 2026-09-26** — machine-readable image-model facts (resolution
> enums, model_type/quality options, aspect ratios) are generated from a
> `type=image` `models_explore` snapshot into `specs/image-model-specs.yaml` /
> `.json` and `specs/IMAGE-MODEL-SPECS.md` (regenerate via `python3 scripts/sync_specs.py
> --type image`). Verify model **parameters/enums** against that specs layer
> first (HARD RULE #3); credits/pricing below remain hand-maintained UI claims —
> verify live before quoting exact prices.

All image models available in the Higgsfield Image tab.
⚠ = Third-party/external model (warning triangle shown in UI)
G = Google-powered model

**Catalog check (2026-09-26):** an entry marked *not in the API catalog* is absent from
`higgsfield model list` / `workflow list` (CLI 1.1.23) and from the 2026-09-26 `models_explore`
image snapshot. It may be UI-only — verify in the live UI before recommending it.

---

## Routing by Asset Class

`[FIELD — AI-vs-VFX, 2026-08-08]` There is no single best image model for a project —
there is a best model **per asset class**, and switching between them mid-project is the
normal case. This table is the routing; the per-model sections below are the reference.

| Asset class | Model | Why |
|---|---|---|
| Human character sheet, face matching | **Nano Banana 2** | Strongest face match on the platform |
| Small corrective edits to an existing asset | **Nano Banana 2** | Holds its input images best — switch *to* it for a one-line fix instead of re-prompting the whole sheet |
| Fantasy creature / non-human character sheet | **Seedream 5.0** (the build does not say Lite or Pro) | Best at fantasy creatures |
| Clothing, wardrobe changes, branded garments | **GPT Image 2** | Handles clothing best. (`[HOUSE]` note, not the build's words: for costume texture on a from-scratch sheet one other production picked Seedream 5.0 Pro — `skills/higgsfield-soul/SKILL.md` § Pick the Sheet Model per JOB; the edits-vs-from-scratch split is one reading, not a default — OPEN, `skills/shared/house-rulings.md` P3-2; compare 2–3 models per sheet) |
| Locations and environment stills | **Soul Cinema** | Most cinematic frames; GPT skews yellow, Nano Banana makes locations too clean and too symmetrical |

Two economics notes that follow from it:

- **Location work batches.** Seven credits (the build's figure — verify live) buys one GPT Image 2 generation or ~56 Soul
  Cinema variations — so on locations, batch wide and select rather than prompt-tuning.
  Select on **light**: bad light in the still is the most common cause of a slop video.
- **Fix, don't rebuild.** A warped logo or a colour cast on an otherwise-good sheet is a
  Nano Banana 2 one-liner (`change the logo to the one in image two`). Re-prompting the
  sheet re-rolls everything that was already right. On an **identity base**, mask the changed
  region back onto the untouched original afterwards (`skills/shared/house-rulings.md` P2-3).

**Routing by parameter** `[OFFICIAL — platform, snapshot 2026-09-26]` — these are catalog
capabilities, not field-rated quality calls:

| Need | Model | Parameter |
|---|---|---|
| Transparent-background cut-out | **GPT Image 2.5** | `background: transparent` (§ GPT Image 2.5) |
| Quality above `high` | **GPT Image 2.5** | `quality` xhigh / max |
| Masked inpaint of one region | **Nano Banana 2** / **Nano Banana 2 Lite** | `mask` role + `is_inpaint` (§ Inpaint, Mask & Background Parameters) |
| Inpaint/edit of a reference instead of a fresh image | **Seedream 5.0 Pro** | `is_inpaint` |
| Extend the canvas (or crop) side by side | **FLUX.2 Pro Outpaint** | `expand_top` / `expand_bottom` / `expand_left` / `expand_right` |
| Relight an existing image (CLI only) | **`nano_banana_2_relight`** | light source / quality / colour / brightness (§ Nano Banana relight) |

Sheet-construction laws (grey background, the two-close-up creature sheet, the face-lock
crop, the size-ref frame) live in `skills/higgsfield-character-design/SKILL.md`
§ Sheet Construction Laws; the grey-background and one-readable-face laws are canonical in
`templates/ad-asset-prep.md` § Design for win rate; the full production pipeline is
`skills/higgsfield-seedance-2-5/VFX-PIPELINE.md`.

---

## Higgsfield Native Models

### Soul 2.0
**Credits:** Free (5,000 free generations)
**UI:** Soul 2.0 · 3:4 · 2K · 1/4 · Color Transfer · Character slot · Moodboard
**Best for:** Fashion editorial · cultural/aesthetic portraits · trend-driven content
**Unique controls:** Style presets (10 named aesthetics) · Color Transfer palettes (6 named) · Soul ID character slot · Moodboard integration
**Strengths:** Built-in cultural fluency — understands subcultures, fashion aesthetics, contemporary visual trends
**Prompt tip:** Describe subject + scene + mood only. Apply style via presets, not text.
→ See `higgsfield-soul` skill for full detail on presets, Color Transfer, and Soul ID

**Platform constraint — style preset vs reference image** `[OFFICIAL — platform CLI, 2026-09-26]`:
`higgsfield model get text2image_soul_v2` carries two rules — **`style_id` cannot be combined with
`image_references`**, and at most **one** image reference is allowed. The same CLI schema has a
separate `custom_reference_id` param that the rule does not mention, and the MCP catalog's Soul 2.0
ids (`soul_2`, `soul_v2`) expose only `quality` and `soul_id`. Which UI control maps to which param
— Style preset → `style_id`? Character slot / Soul ID → `custom_reference_id`, `soul_id`, or
`image_references`? — is **unverified**. Until it is: if a style preset plus an uploaded reference
image is rejected or ignored, drop one of them; do not promise that a preset and a reference image
combine.

---

### Soul Cinema
**Model id:** `soul_cinematic` — named *Soul Cinema* in every image snapshot since 2026-06-22 (the CLI lists it as "Soul Cinematic"); `quality` 1.5k / 2k, `soul_id` `[OFFICIAL — platform, snapshot 2026-09-26]`. This entry was written in 2026-03 as *Soul Cinema Preview*.
**Credits:** Low (cheaper per generation than most models)
**Best for:** Cinematic-grade image generation — rich textures, natural compositions, "spontaneous look," deep depth of field, film grain aesthetics
**Excels at:** Close-up shots specifically
**Unique:** No preset selection panel — unlike Soul 2.0, it's **purely prompt-driven**
**Key workflow:** Generate cinematic keyframe with Soul Cinema → feed into video model (e.g., Kling 3.0 I2V) for best results
**Works with:** Soul ID (character consistency) and Soul HEX (precise color control)
**Status:** Out of preview — the catalog name is Soul Cinema (see Model id above)

**Soul HEX** — Extracts color palettes from reference photos for brand-consistent, color-matched visuals. Works across Soul 2.0, Soul Cinema, and Cinema Studio 2.5.

---

### Soul Cast
**Model id:** `soul_cast` · **Provider:** Higgsfield
**Best for:** Consistent cinematic character identity — the same face/character held across many generations
**Aspect ratio:** 16:9 only (per the specs snapshot, still true 2026-09-26)
**Unique control — `budget` (10–500, default 50):** generation budget dial — higher budget spends more compute on the identity
**Note:** Previously exposed only inside Cinema Studio (2.5/3.0 "Soul Cast AI actors"); now a standalone model in the image catalog. For per-shot character work at other aspect ratios, generate the identity here and carry it into other models via references.

---

### Soul Location
**Model id:** `soul_location` · **Provider:** Higgsfield
**Best for:** Environment and location generation — establishing plates, backdrops, location references for I2V and multi-shot pipelines
**Aspect ratios:** 1:1, 4:3, 3:4, 16:9, 9:16, 3:2, 2:3, 21:9, 9:21 — widest ratio spread of the Soul family (the only image model with 9:21 vertical ultrawide in the 2026-09-26 snapshot)
**Controls:** No extra parameters — purely prompt-driven
**Pairs with:** Soul Cast (character) + Soul Location (environment) as reference inputs for reference-driven video models

---

### Higgsfield Soul (Legacy)
**Catalog:** not in the API catalog as of the 2026-09-26 snapshot; may be UI-only — verify in the live UI before recommending (the catalog's Soul image models are Soul 2.0, Soul Cinema, Soul Cast and Soul Location).
**Credits:** 0.5 per generation
**UI:** Higgsfield Soul · 1:1 · 2K · Style On/Off · 1/4 · Unlimited · Character slot
**Prompt field:** "Upload image as a prompt or Describe the scene you imagine"
**Best for:** Lower-cost portrait generation · image-as-prompt workflows · when Soul 2.0 credit quota is exhausted
**vs Soul 2.0:** Older model, no Color Transfer or style presets. Accepts image uploads as prompt input. Half the cost.
**Unique feature:** Image-as-prompt — upload a reference image to guide generation style/composition instead of (or alongside) text

---

### Z-Image
**Credits:** 0.15 per generation — cheapest image model on the platform
**UI:** Z-Image · 16:9 · 1/4 · Unlimited
**Best for:** Rapid iteration · high-volume testing · when budget is the primary constraint
**Use when:** You need many variations fast and quality is secondary to speed and cost
**Note:** No resolution or quality controls visible — streamlined for volume

---

### Kling O1 Image
**Model id:** `kling_omni_image` — catalog name *Kling O1 Image* (`resolution` 1k / 2k) `[OFFICIAL — platform, snapshot 2026-09-26]`
**Credits:** 0.5 per generation
**UI:** Kling O1 · 1:1 · 2K · 1/4 · Unlimited
**Best for:** Clean, high-quality 2K images at low cost · square format social content
**vs Z-Image:** 3x the cost but 2K resolution and Kling model quality
**Default aspect:** 1:1 — native square. Good for Instagram/social.
**Note:** Image-only version of the Kling engine (same family as Kling 2.6/3.0 video)

---

### Kling Image 3.0
**Catalog:** not in the API catalog as of the 2026-09-26 snapshot; may be UI-only — verify in the live UI before recommending. Catalog pick for native 4K stills: Nano Banana Pro (`resolution` 1k / 2k / 4k — the `model-guide.md` decision tree's "maximum sharpness / 4K" pick). No catalog model is on record for Image Series Mode.
**Credits:** TBD
**UI:** Kling Image 3.0 · 16:9 · 4K
**Best for:** Native 4K stills (up to 3840×2160) · Image Series Mode for storyboarding · multi-reference workflows
**Key features:**
- **Native 4K** (up to 3840×2160) — no upscaling. Also supports 1K and 2K
- **Image Series Mode**: generate sequential frames with consistent characters, style, and tone across varied camera angles (storyboarding use case)
- **Up to 10 reference images** per generation
- **Visual Chain-of-Thought**: model reasons through composition before rendering
- **Style transfer + portrait reference + character reference + multi-image blending** all in one workflow
- **Local re-editing**: add/remove/modify elements without switching tools
- **Batch optimization**
- **Cinematic color grading** built in
- **Aspect ratios**: 1:1, 3:4, 4:3, 16:9, 9:16

---

### Kling Image 3.0 Omni
**Catalog:** not in the API catalog as of the 2026-09-26 snapshot; may be UI-only — verify in the live UI before recommending. Catalog pick for edits at up to 4K: Nano Banana 2 (§ Routing by Asset Class — small corrective edits; `resolution` 1k / 2k / 4k).
**Credits:** TBD
**UI:** Kling Image 3.0 Omni · 16:9 · 4K
**Best for:** Advanced editing · refining styles and subjects · strongest prompt fidelity
**What it adds over Image 3.0:** Enhanced editing capabilities, stronger prompt adherence, refining styles and subjects with greater precision
**Resolution:** Native 2K and 4K output

---

### Wan 2.2
**Catalog:** not in the API catalog as of the 2026-09-26 snapshot; may be UI-only — verify in the live UI before recommending (no Wan image model is listed). Catalog pick for stylized images: Seedream 5.0 Pro (§ Seedream 5.0 Pro — stylized-2D work).
**Credits:** 1 per generation
**UI:** Wan 2.2 · 3:4 · Style On/Off · 1 generation
**Best for:** Stylized / artistic image output · non-photorealistic aesthetics
**vs Wan video:** Same model family as Wan 2.5/2.6 video — painterly, artistic, non-photorealistic strengths carry over to image
**Style toggle:** On enables stylization mode

---

### Multi Reference
**Catalog:** not in the API catalog as of the 2026-09-26 snapshot; may be UI-only — verify in the live UI before recommending. Catalog pick for a multi-reference blend: Nano Banana Pro (14 references — `skills/higgsfield-models/SKILL.md` § Unique Feature Matrix).
**Credits:** 1.5 per generation
**UI:** Multi Reference · 3:4 · Style On/Off · 1/4 · Unlimited
**Best for:** Compositing elements from multiple reference images into one generation
**Use when:** You have several reference photos (character, location, prop, color) and want to blend them into a single coherent output
**How it works:** Upload multiple reference images, the model synthesizes a new image drawing from all references simultaneously
**Prompt tip:** Be explicit about which element comes from which reference

---

### Reve
**Catalog:** not in the API catalog as of the 2026-09-26 snapshot; may be UI-only — verify in the live UI before recommending.
**Credits:** 1 per generation
**UI:** Reve · 3:4 · Standard quality · 1/4 · Unlimited
**Best for:** General-purpose image generation
**Quality selector:** Standard (only option visible — may have additional tiers)
**Note:** Newer model in the lineup — less known quantity, worth testing for versatile generation

---

## Seedream Family

### Seedream 5.0 Pro
**Model id:** `seedream_v5_pro` — in the spec snapshot since 2026-08-01 (resolution `1k`/`1.5k`/`2k`, default 2k; aspect ratios incl. 21:9). `[FIELD provenance: first observed on 161 harvested community jobs, 2026-07-18]`
**Edit / background params** `[OFFICIAL — platform, snapshot 2026-09-26]`: `is_inpaint` (default false — "Treat the request as an inpaint/edit of the reference image(s) instead of a fresh generation") and `remove_bg` (default false — "Remove the background from the generated image"). No `mask` role.
**Best for:** Anime / manga / stylized-2D image work — character sheets with clean linework, flat cel color fills, multi-panel manga page layouts with screentones and readable panel geometry
**Field-proven dialects:** split-screen anime character sheets (full-body action pose left, chest-up portrait right, identical character, white seamless background, ~190w median) · black-and-white manga page spreads (panels laid out by position + size + content, refs as Image0/1/2, ink linework, screentones, no color)
**Style anchoring:** use an **art-era anchor** ("early 2000s retro anime, soft painted cel-shading, vintage proportions") — the stylized-image equivalent of the photoreal director/DP anchor
**vs 5.0 Lite / 4.5:** the pick when line + flat color + text/panel layout matter more than photoreal texture; photoreal sheet work stays on Soul / GPT Image 2 / Nano Banana Pro

---

### Seedream 5.0 Flash
**Model id:** `seedream_5_0_flash` · **Provider:** Bytedance · new in the 2026-09-26 snapshot — **not yet field-rated**
**Catalog description:** "Fast image generation and instruction-based editing, up to 2K" `[OFFICIAL — platform, snapshot 2026-09-26]`
**Resolution:** `1k` / `1.5k` / `2k` (default 2k) · **Aspect ratios:** auto, 1:1, 4:3, 3:4, 16:9, 9:16, 3:2, 2:3, 21:9 · **Reference input:** image references
**Note:** optional `width` / `height` are "stored in generation metadata; not sent to the provider" — they do not size the output.
**vs 5.0 Pro:** same resolution ladder; Flash has no `is_inpaint` or `remove_bg`. Prompting dialect not yet documented here. Credits: verify in the UI.

---

### Seedream 5.0 Lite
**Credits:** 1 per generation
**UI:** Seedream 5.0 lite · 2K · 16:9 · 1/4 · @ (Elements) · Unlimited
**Best for:** Fast, high-aesthetic image generation · versatile styles · rapid iteration
**@ Elements:** Supports @ syntax for referencing saved Elements
**Unlimited toggle:** Batch generation without credit cap
**vs 4.5:** 5.0 Lite = faster, 2K. 4.5 = slower, 4K. Same cost.

---

### Seedream 4.5
**Credits:** 1 per generation
**UI:** Seedream 4.5 · 4K · 16:9 · 1/4 · @ (Elements) · Unlimited
**Best for:** 4K output · when maximum resolution matters over speed
**Quality tiers — `quality`:** `basic` (default, renders up to 4K) / `high` (renders up to ~6K)
**Aspect ratios:** 1:1, 4:3, 16:9, 3:2, 21:9, 3:4, 9:16, 2:3
**@ Elements:** Supports @ syntax for referencing saved Elements
**vs 5.0 Lite:** Higher resolution (4K vs 2K), same cost, slower generation

---

### Seedream 4.0
**Catalog:** not in the API catalog as of the 2026-09-26 snapshot; may be UI-only — verify in the live UI before recommending (Seedream 4.5 and 5.0 Pro / Lite / Flash are in it).
**Credits:** 1 per generation
**UI:** Seedream 4.0 · Basic quality · 3:4 · 1/4 · Unlimited
**Best for:** Legacy/baseline generation · portrait orientation (3:4 default)
**Quality selector:** Basic (lowest tier shown)
**Note:** Older model tier — use 4.5 or 5.0 Lite for better results at the same cost

---

## Nano Banana Family (G = Google-powered)

All three models run on Google's Gemini image engine. Each is a distinct model tier.

---

### Nano Banana
**Google model:** Gemini 2.5 Flash Image
**Credits:** 1 per generation
**UI:** Nano Banana · 3:4 · 1/4 · Unlimited · **Draw**
**Best for:** Sketch-to-image prototyping · portrait format · fast, low-cost generation
**Draw feature:** Sketch a rough composition or shape — model generates from your drawing
**Strengths:** Speed and efficiency, optimized for high-volume, low-latency use
**Note:** Original model — Draw feature makes it still uniquely useful; most other surfaces now default to NB2

---

### Nano Banana Pro
**Google model:** Gemini 3 Pro Image Preview
**Credits:** 2 per generation
**UI:** Nano Banana Pro · 16:9 · 1K · @ (Elements) · Unlimited · **Draw**
**Best for:** Professional asset production · complex multi-element prompts · accurate text in images · brand mockups · sequential art/storyboards
**Draw feature:** Sketch-to-image, same as base
**@ Elements:** Supports @ syntax for Higgsfield saved Elements

**Unique capabilities (not in other Nano Banana tiers):**

**Thinking mode** — Before generating, model silently reasons through complex prompts, producing up to 2 interim "thought images" to test composition. Always on, cannot be disabled. Significantly better at complex, multi-instruction prompts.

**Up to 14 reference images** — Input up to 14 images simultaneously:
- Up to 6 object images (high-fidelity object inclusion)
- Up to 5 person images (character consistency)
Tip: Name each reference's role — "Use Image A for pose, Image B for style, Image C for background"

**Google Search grounding** — Pulls real-time web info for data-accurate visuals: weather forecasts, stock charts, news events. Ask "what's today's weather in Tokyo" and it generates an accurate graphic.

**Advanced text rendering** — Best text accuracy in the family. Multilingual text, infographics, menus, logos, diagrams. Also translates text inside an existing image while preserving layout.

**Resolution:** 1K (default), 2K, 4K
**Aspect ratios:** 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9

**What it excels at:**
- Text-heavy assets: posters, infographics, magazine covers, menus, diagrams
- Brand identity: logo mockups, pattern draping onto 3D objects/apparel/packaging
- Multi-character scenes: up to 5 consistent characters in a single image
- Sequential art: comic panels, storyboards with consistent characters across panels
- Data visualization with Search grounding: charts/graphs using real-world accuracy
- Product mockups: studio-quality commercial photography shots

**6-element prompt formula for best results:**
1. **Subject** — who/what: "a stoic robot barista with glowing blue optics"
2. **Composition** — framing: "extreme close-up", "low angle", "wide shot"
3. **Action** — what's happening: "brewing coffee, steam rising"
4. **Location** — setting: "a futuristic café on Mars, warm amber lighting"
5. **Style** — aesthetic: "photorealistic", "3D animation", "film noir", "watercolor"
6. **Camera/lighting** — "shallow depth of field (f/1.8)", "golden hour backlight", "muted teal color grading"

**When using multiple reference images:** explicitly name each reference's role in the prompt

**Known limitations (official):**
- Small text and fine details may not render perfectly every time
- Factual data in diagrams should be verified — model can hallucinate data
- Multilingual text may have grammar errors
- Complex edits and blending can produce artifacts
- Character consistency may drift across long multi-turn sessions

**Production-team observations (Higgsfield team disclosed):**

The following failure modes and counters come from the Hell Grind 90-min Cannes production team's documented in-pipeline use of Nano Banana Pro. They sit alongside the official limitations above — recurring patterns the team hit and the prompt-side fixes they shipped.

- **Plasticky-texture failure mode.** Surfaces are smooth and over-rendered; faces read as plastic in wide shots. Counter: append a trailing line `light atmospheric haze, film grain, crush blacks, shadow depth` at the end of the prompt. The single trailing line measurably shifts texture toward photographic without destabilizing the rest of the composition.
- **Spatial-awareness limit (location references).** Uploading a city or environment image as a reference results in indoor subjects placed outdoors, or interiors that fail to spatially align with the reference geometry. Counter: keep the location in the *prompt text* (described verbally), not as an *image reference*. NBP handles described locations better than image-referenced ones.
- **4-view default vs single composition.** NBP defaults to producing a 4-view reference sheet when asked for a character. Counter: explicitly request `one view image` (or `single composition`) when you want a single hero frame rather than a sheet.
- **Multi-image embedded prompt drift.** A single prompt requiring many embedded reference elements (e.g., a 12-Polaroid photo wall built from individual character sheets) produces severe drift — faces from the source sheets fail to read correctly in the composite. Counter: generate each element individually, then composite in Photoshop. The production-team workflow accepted this trade-off (longer post-production for higher per-element fidelity).

**Location-handling discipline (Group H):**

When NBP is generating location-anchored shots, three patterns recur in production-team practice:

- **Every location needs an anchor** — a named visual landmark (a tree, a specific architectural feature, a recurring prop) gives the prompt a fixed point for relative spatial placement (`Roco stands to the left of the tree`). Anchorless locations drift.
- **Never generate locations from the front.** Front-facing location renders confuse NBP's depth perception. Use a 3/4 angle or a ceiling-corner (CCTV) angle for location-establishing shots.
- **Split locations into views, don't combine.** When a location appears across multiple cuts at different angles, generate separate location images per angle and attach them as separate references (`for cut one use this view, for cut two use this view`). Production-team learning evolved this away from earlier combined-into-single-reference practice — separate references hold better.

**Workflow positioning:**

NBP is the strongest single image model on the platform for sharpness, multi-element composition, and text rendering. For **high-investment characters** that will appear across many shots, the two-tool pipeline outperforms NBP alone: Soul Cinema for initial character generation + GPT Image 2 for refinement editing. See `skills/higgsfield-soul/SKILL.md` § Two-Tool Refinement Pipeline for the split-by-task discipline and the ~600 + ~200 = ~800 generations anchor from the Hell Grind production.

---

### Nano Banana 2
**Google model:** Gemini 3.1 Flash Image
**Released:** February 26, 2026
**Credits:** 1.5 per generation
**UI:** Nano Banana 2 · 16:9 · 1K · 1/4
**Best for:** Pro-quality output at Flash speed · rapid iteration on complex prompts · character-consistent multi-image workflows · text rendering · storyboarding

**What it is:** Google's "best of both worlds" — Nano Banana Pro's intelligence at Nano Banana's speed. Now the default image model across most Google surfaces (Gemini app, Search, Flow, Google Ads). Also powers **Soul Cast** in Cinema Studio 2.5.

**Capabilities:**
- **Subject consistency**: maintains resemblance of up to **5 characters** and fidelity of up to **14 objects** in a single workflow — critical for storyboarding
- **Precision text rendering + translation**: accurate legible text in images, can translate/localize text within an image while preserving layout
- **Advanced world knowledge**: pulls from Gemini's knowledge base + real-time web search to accurately render specific subjects, places, landmarks
- **Resolution**: 512px to 4K native
- **Aspect ratios**: 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 4:5, 5:4, 21:9
- **Infographics, diagrams, data visualizations**: strong at generating from text prompts
- **Reference image editing**: edit/transform/combine existing images via text prompts
- **Style transfer**: combine multiple reference images into one output
- **Photorealistic quality**: vibrant lighting, richer textures, sharper details vs original Nano Banana

**Prompting patterns that work well:**
- **Structured JSON prompts** for complex scenes (subject → accessories → photography → background breakdown)
- **Short direct prompts** also work ("Create a realistic photo of this character")
- **Style transfer**: "Show me the animation style image version" / "Show me the real-life photo version"
- **Location + time**: coordinates or place name + "at sunset" generates accurate scenes
- **Blueprint/schematic**: "hand drawn isometric schematic diagram of [subject]"
- **Infographic overlays**: detailed annotation instructions on top of photos
- **Multi-panel comics**: single prompt with per-panel descriptions
- **Product ad recreation**: "Recreate this ad concept using my product instead" + reference image

**When to use NB2 vs Pro:**
- **NB2** = best for rapid generation, precise instruction following, speed, integrated image-search grounding
- **NB Pro** = best for high-fidelity tasks requiring maximum factual accuracy, complex compositions, Thinking mode reasoning, 14-ref compositing

**When to use NB2 vs base Nano Banana:**
- NB2 is dramatically better at everything — base is only worth using for its Draw feature

**No Draw yet** — Draw feature exists only in base Nano Banana and Nano Banana Pro

**SynthID + C2PA:** All Nano Banana family outputs include an invisible SynthID watermark and C2PA Content Credentials for AI provenance verification

**Masked inpaint** `[OFFICIAL — platform, snapshot 2026-09-26]`: `nano_banana_2` takes a `mask` media role plus `is_inpaint` (default false — "Whether to restrict the edit to the supplied mask"); resolution 1k / 2k / 4k. See § Inpaint, Mask & Background Parameters.

> **Same id, different model on the CLI** `[OFFICIAL — platform, checked 2026-09-26]`: the MCP's
> `nano_banana_2` ("Nano Banana 2": default 1k, `auto` aspect, `mask` + `is_inpaint`) matches the
> CLI's **`nano_banana_flash`** parameter for parameter, while `higgsfield model get nano_banana_2`
> answers as **Nano Banana Pro** (default 2k, no `auto` aspect, no mask). On the CLI, use
> `nano_banana_flash` for this model; `--model nano_banana_2` there most likely runs Nano Banana Pro.
> Recorded in `specs/crosscheck_allowlist.json`; re-check when either surface changes.

---

### Nano Banana 2 Lite
**Model id:** `nano_banana_2_lite` · **Google-powered**
**Best for:** Budget NB2-family generation — high volume, drafts, iteration passes before committing to NB2/Pro
**Resolution:** 1k only (single option — no 2K/4K on Lite)
**Unique control — `thinking` (MINIMAL / HIGH, default HIGH):** depth of internal reasoning before generation. Drop to MINIMAL for speed on simple prompts; keep HIGH for complex multi-instruction prompts
**Aspect ratios:** auto, 1:1, 3:2, 2:3, 4:3, 3:4, 4:5, 5:4, 9:16, 16:9, 21:9
**Reference input:** image references supported
**vs Nano Banana 2:** Lite trades the 2K/4K resolution ladder for a cheaper tier and an explicit thinking-depth dial; same aspect-ratio spread plus auto
**Masked inpaint** `[OFFICIAL — platform, snapshot 2026-09-26]`: the same `mask` role + `is_inpaint` pair as Nano Banana 2.

---

### Nano Banana relight (CLI only)
**Job type:** `nano_banana_2_relight` — listed by the `higgsfield` CLI (`model get`, 2026-09-26) but **not in the MCP `models_explore` list**; the CLI's display name for it is "Nano Banana Pro". `[OFFICIAL — platform CLI, 2026-09-26]`
**What it takes:** an existing image (`image_references`, required) — there is **no prompt param**. Required: `brightness` (integer; range not stated), `color` (string; format not stated), `light_quality` hard / sharp / soft, and `light_source` — one of 26 three-letter position codes (`fml`, `bur`, `mdm`, …). The schema does not define the codes; do not guess their meaning — read them off the UI control. Optional `remove_bg` (default false).
**Status:** not yet field-rated; credits not stated.

---

## GPT Image Family (OpenAI-powered)

### GPT Image
**Credits:** 2 per generation
**UI:** ChatGPT · 1:1 · Mid quality · 1/4 · Unlimited · Character slot
**Best for:** Instruction-following · complex multi-element prompts · character slot integration
**Quality selector:** Low / Mid / High
**Character slot:** Supports Soul ID character reference (GENERAL shown by default)
**Default aspect:** 1:1 square
**Note:** Model selector shows "ChatGPT" branding — OpenAI's GPT-Image model
**Status:** Not in the API catalog (2026-09-26) — verify in the UI before recommending; prefer GPT Image 2.5 / 2 or OpenAI Hazel. The catalog id that left, `gpt_image`, was named *GPT Image 1.5* in its only snapshot (§ GPT Image 1.5)

---

### GPT Image 1.5
**Catalog:** left the API catalog — its id `gpt_image` was named *GPT Image 1.5* in the 2026-06-22 image snapshot and has been absent since 2026-07-05 (`specs/retired-model-ids.json`). May be UI-only — verify in the live UI before recommending. Catalog pick for text in images: GPT Image 2 (§ GPT Image 2).
**Credits:** 2 per generation
**UI:** GPT Image 1.5 · 1:1 · Low quality · 1/4
**Best for:** Complex prompts · text-in-image · precise instruction following
**Quality selector:** Low / (implied Medium/High)
**vs GPT Image:** Newer version. Default shown at Low quality (faster/cheaper mode). No character slot visible.
**Text in image:** GPT Image 1.5 handles text rendering better than most models
**Note:** Same credit cost as original — upgrade when you need better prompt adherence

---

### GPT Image 2
**Credits:** Confirm in Higgsfield UI — premium tier expected given native 4K + O-series reasoning
**UI:** GPT Image 2 · 16:9 · 4K · 1/4 · Multi-reference (up to 16 images)
**Best for:** Photorealistic commercial imagery · text-heavy designs · multilingual campaigns · character consistency across multi-shot · CJK / Hindi / Bengali text rendering
**Higgsfield URL:** `higgsfield.ai/ai/image?model=imagegen_2_0`
**Higgsfield internal slug:** `imagegen_2_0`
**OpenAI model ID:** `gpt-image-2` (snapshot `gpt-image-2-2026-04-21`, released April 21, 2026, knowledge cutoff December 2025)
**Native resolution:** 4K (up from 1536×1024 in GPT Image 1.5)
**Reference images:** up to 16
**Multilingual text rendering:** >95% accuracy across Japanese, Korean, Chinese, Hindi, Bengali — first OpenAI image model to handle non-Latin scripts at production-grade fidelity
**vs GPT Image 1.5:** Photorealism leap, text-rendering leap, native 4K (up from 1536×1024), ~2× speed on standard mode, plus O-series reasoning capability for complex multi-element prompts that previously required Nano Banana Pro Thinking mode
**Note:** First image model with O-series reasoning capabilities — complex multi-element compositions resolve more reliably than on prior GPT Image generations. For full API specs, rate limits, and deep-reference comparison to siblings, see `skills/higgsfield-models/MODELS-DEEP-REFERENCE.md` § GPT Image 2.

**CLI ↔ MCP disagreement on `gpt_image_2` (2026-09-26) — recorded, not resolved.** The two
official Higgsfield surfaces describe different parameter sets for the same id:

| Field | MCP `models_explore` (image snapshot 2026-09-26) | CLI `higgsfield model get gpt_image_2` (2026-09-26) |
|---|---|---|
| Aspect ratios | 1:1, 4:3, 3:4, 16:9, 21:9, 9:16, 3:2, 2:3 | the same **plus auto, 4:5, 5:4** (default 1:1) |
| `resolution` default | 1k | **2k** |
| `quality` default | low | **high** |
| `background` | not listed | auto / opaque / transparent (default null) |
| `mask` / `is_inpaint` | not listed | `mask` (object) + `is_inpaint` (default false) |
| Media role | `image` | `image_references` |

Neither surface is declared the winner here. Until one is verified against a real generation:
set `quality` and `resolution` explicitly instead of relying on either default, and treat
`background`, `mask` / `is_inpaint`, and the auto / 4:5 / 5:4 ratios on `gpt_image_2` as
CLI-listed but MCP-unlisted. For a transparent background, GPT Image 2.5 is the route both
surfaces agree on.

---

### GPT Image 2.5
**Model id:** `gpt_image_2_5` · **Provider:** OpenAI · new in the 2026-09-26 snapshot — **not yet field-rated**
**Catalog description:** "GPT Image 2.5 generation and editing with Flare and Sunburst variants" `[OFFICIAL — platform, snapshot 2026-09-26]` (MCP and CLI agree on every field below)
**Params:**
- `variant` — `flare` (default) / `sunburst`
- `quality` — `low` (default) / `medium` / `high` / **`xhigh`** / **`max`**
- `resolution` — `1k` (default) / `2k` / `4k`
- **`background` — `auto` / `opaque` / `transparent`** (omit to keep the model default)
- Aspect ratios (15) — auto, 1:1, 3:2, 2:3, 4:3, 3:4, 16:9, 9:16, 21:9, 27:16, 16:27, 9:8, 8:9, 4:5, 5:4 (CLI default 1:1)
- `image_references` — generation and editing from reference images

**Transparent background — the first transparent-background route in the MCP catalog.** No other
image model in the 2026-09-26 MCP snapshot offers a transparent option (the CLI also lists
`background` on `gpt_image_2` — see § GPT Image 2). OpenAI's API needs PNG or WebP output for
transparency `[OFFICIAL — OpenAI docs]`; Higgsfield exposes no output-format parameter, so whether
the delivered file carries an alpha channel is **unverified** — check the first download before
building a cut-out pipeline on it.

**Variant choice** `[OFFICIAL — OpenAI docs]`: Sunburst "for workflows where editing precision
matters most"; Flare "for fast, high-quality everyday image generation". The Higgsfield `variant`
values are matched to OpenAI's `gpt-image-2.5-sunburst` / `gpt-image-2.5-flare` by name.

**Defaults are draft settings.** A bare call runs `flare` / `low` / `1k`. OpenAI: "Use
`quality: "low"` for quick drafts. For final assets, compare higher quality settings to find the
right balance of detail, latency, and cost." Set `quality` and `resolution` explicitly for finals.

**Credits:** not stated in the catalog — verify in the UI. (OpenAI's API bills 2.5 at the same
per-token rates as GPT Image 2, with token counts that differ by model and quality — that says
nothing about Higgsfield credits.)

Sources: [OpenAI image generation guide](https://platform.openai.com/docs/guides/image-generation),
[gpt-image-2.5-sunburst](https://platform.openai.com/docs/models/gpt-image-2.5-sunburst),
[gpt-image-2.5-flare](https://platform.openai.com/docs/models/gpt-image-2.5-flare) (fetched 2026-09-26).
Prompting and "when to prefer 2.5 vs 2": `skills/higgsfield-gpt-image-2/SKILL.md` § GPT Image 2.5.

---

### OpenAI Hazel
**Model id:** `openai_hazel` · **Provider:** OpenAI
**Best for:** Powerful reference-based editing · best-in-class text rendering
**Quality selector — `quality`:** low / medium / high (default medium)
**Aspect ratios:** 1:1, 3:2, 2:3, auto
**Reference input:** image references supported — feed the image you want edited/transformed
**vs GPT Image 2:** Hazel is the editing-and-text specialist with a compact aspect set (1:1/3:2/2:3/auto); GPT Image 2 is the native-4K, 16-reference generation flagship. Reach for Hazel when the job is "edit this image" or "get this text exactly right"

---

## FLUX Family (⚠ External/Third-party)

All FLUX models show a warning triangle (⚠) in the UI — third-party external models.

### FLUX.2 Flex
**Credits:** 5 per generation
**UI:** ⚠ FLUX.2 Flex · 16:9 · 2K · 1/4 · Settings ⚙
**Best for:** Flexible, high-quality FLUX generation
**Unique:** Settings ⚙ button — additional configuration options beyond standard controls
**Note:** No Unlimited toggle visible. Higher cost reflects external model pricing.

---

### FLUX.2 Pro
**Credits:** 1.5 per generation
**UI:** ⚠ FLUX.2 Pro · 16:9 · 2K · 1/4 · Unlimited
**Best for:** Professional-grade FLUX output at mid-tier cost
**vs Flex:** Same resolution, lower cost, Unlimited toggle available

---

### FLUX.2 Max
**Credits:** 6 per generation — most expensive image model on the platform
**UI:** ⚠ FLUX.2 Max · 16:9 · 2K · 1/4
**Best for:** Highest FLUX quality output — when cost is not a constraint
**Note:** No Unlimited toggle. Premium tier of the FLUX.2 family.

---

### FLUX.2 Pro Outpaint
**Model id:** `flux_2_pro_outpaint` · **Provider:** Black Forest Labs · new in the 2026-09-26 snapshot — **not yet field-rated**
**Catalog description:** "Expands an image beyond its borders with FLUX.2 [pro]: per-side pixel expansion painted as a coherent, seamless scene extension. Negative values crop that side instead; an all-crop request is served locally for free without the model." `[OFFICIAL — platform, snapshot 2026-09-26]`
**Params:** `expand_top` / `expand_bottom` / `expand_left` / `expand_right` — pixels, −8192 to 2048, default 0; a **negative value crops** that side. One image via `image_references`.
**Use when:** a still needs more canvas on specific sides (a 16:9 plate widened for 21:9, headroom for a title) — or an exact per-side crop, which the catalog says costs nothing when every side is negative.

---

### Flux Kontext
**Credits:** varies
**UI:** ⚠ Flux Kontext · (editing interface)
**Best for:** Targeted image editing · inpainting · modifying specific areas of an existing image
**Use when:** You have an image you want to change, not generate from scratch
**vs generation models:** This is an editing model — input is an existing image + instruction

---

### Flux Kontext Max
**Catalog:** the same id as Flux Kontext — `flux_kontext` was named *Flux Kontext Max* in the 2026-06-22 image snapshot and *Flux Kontext* since 2026-07-05. Recommend it as Flux Kontext; whether the UI still shows a separate Max tier is unverified.
**Credits:** 1.5 per generation
**UI:** ⚠ Flux Kontext Max · 3:4 · Style On/Off · 1/4 · Unlimited
**Best for:** Higher-quality version of Flux Kontext editing
**vs Kontext:** Same editing purpose, higher quality output, portrait default (3:4)
**Style toggle:** On enables stylization during edit

---

## Recraft Family (⚠ External/Third-party)

### Recraft 4.1
**Model id:** `recraft_v4_1` (renamed from `recraft-v4-1`, which remains a catalog alias) · **Provider:** Recraft
**UI:** Recraft V4.1 (and **Recraft V4.1 Utility**) · 1:1 · 1/4 · NEW
**Best for:** Photorealistic + expressive generation, brand assets, logos/icons, product mockups
**Resolution:** 1k (everyday) / 2k (larger assets) — see `specs/image-model-specs.yaml`
**Batch:** 1–4 images per job (`batch_size`)
**Unique control — `model_type` (4 variants):**
- `standard` — expressive, exploratory generation (the default; "Recraft V4.1" in the UI)
- `vector` — logos, typography, icons, SVG-like illustration
- `utility` — cleaner, flatter, front-facing, predictable product shots & mockups (the **"Recraft V4.1 Utility"** UI entry)
- `utility_vector` — utility simplicity with vector output (brand assets)

**Palette control:** `colors` (up to 10 `#RRGGBB` values) and `background_color` (single `#RRGGBB` or null) — strong fit for brand swatches, controlled flat backgrounds, icon/vector work. Hex only: no `#RGB` shorthand, no `#RRGGBBAA`, no `rgba()`, no color names.
**Prompt tip:** For logos/icons pick `vector`; for clean e-commerce product shots pick `utility`. Pass brand colors via `colors` rather than describing them in prose.

---

## Grok Family (xAI)

`[OFFICIAL — platform, snapshot 2026-09-26]` — both **not yet field-rated**. The xAI API
documentation mined in `skills/higgsfield-models/MODELS-DEEP-REFERENCE.md` § Grok Imagine describes
the vendor API, which is broader than these Higgsfield params.

### Grok Image
**Model id:** `grok_image` · live since at least the 2026-08-01 snapshot (the old "not available on Higgsfield" notice was wrong)
**Catalog description:** "Expressive, high-contrast generation and editing"
**Params:** `mode` std (default) / quality ("higher-fidelity"); `resolution` 1k / 2k · **Aspect ratios:** 1:1, auto, 1:2, 2:1, 3:2, 2:3, 4:3, 3:4, 16:9, 9:16 · image references

### Grok Image 2.0
**Model id:** `grok_image_2_0` · new in the 2026-09-26 snapshot
**Catalog description:** "Next-generation image creation and editing from xAI"
**Params:** `quality` low / medium (default medium); `resolution` 1k / 2k · same 10 aspect ratios as Grok Image · image references
Prompting dialect not yet documented here; credits: verify in the UI.

---

## Inpaint, Mask & Background Parameters

`[OFFICIAL — platform, snapshot 2026-09-26]` (MCP catalog) unless marked CLI.

| Model | Parameter | What the platform says |
|---|---|---|
| Nano Banana 2 (`nano_banana_2`) | `mask` media role + `is_inpaint` (default false) | "Whether to restrict the edit to the supplied mask." |
| Nano Banana 2 Lite (`nano_banana_2_lite`) | `mask` media role + `is_inpaint` (default false) | Same as Nano Banana 2 |
| Seedream 5.0 Pro (`seedream_v5_pro`) | `is_inpaint` (default false), no `mask` role | "Treat the request as an inpaint/edit of the reference image(s) instead of a fresh generation." |
| Seedream 5.0 Pro (`seedream_v5_pro`) | `remove_bg` (default false) | "Remove the background from the generated image." |
| Bytedance Image Upscale (`bytedance_image_upscale`) | `remove_bg` (default false); `resolution` 2k / 4k (default 4k) | "Remove the background from the upscaled image." |
| GPT Image 2.5 (`gpt_image_2_5`) | `background` auto / opaque / transparent | § GPT Image 2.5 |
| GPT Image 2 (`gpt_image_2`) — **CLI only** | `mask`, `is_inpaint`, `background` | Not in the MCP list — § GPT Image 2 disagreement table |
| Nano Banana relight (`nano_banana_2_relight`) — **CLI only** | `remove_bg` | § Nano Banana relight |
| FLUX.2 Pro Outpaint (`flux_2_pro_outpaint`) | `expand_*` (negative = crop) | § FLUX.2 Pro Outpaint |

`remove_bg` removes a background; the catalog does not say its output is a transparent PNG, so do
not treat it as the same thing as GPT Image 2.5's `background: transparent`.

---

## Swap Tools (Not Generation Models)

These are upload-based transformation tools, not text-to-image generators.

### Face Swap
**Credits:** Free (2 free generations, then paid)
**UI:** Face Swap · Your Photo (upload face to insert) · Target Image (photo with face to replace) · 3:4 · Unlimited
**How it works:** Upload the face you want → upload the target photo → face is composited in

### Character Swap
**Credits:** 2 per generation
**UI:** Character Swap · Your Photo (character to insert) · Target Image (character to replace) · 3:4
**How it works:** Full character body swap — replaces an entire person in a target image with your uploaded character
**vs Face Swap:** Face Swap = face only. Character Swap = full body/character replacement.

> The image catalog also carries utility/system entries — AutoSprite (animate a character image into a game-ready sprite sheet), MS Image (Marketing Studio ad images), image_auto (auto model selection), upscalers (Topaz, Bytedance), background remover, and the generic `outpaint` tool. These are pipeline tools rather than prompt-crafted generation models and are out of scope for this reference; FLUX.2 Pro Outpaint and the inpaint/background params are covered above because they change how an asset is planned.

---

## Complete Cost Reference

| Model | Credits | Resolution | Notes |
|-------|---------|-----------|-------|
| Z-Image | 0.15 | — | Cheapest |
| Higgsfield Soul | 0.5 | 2K | Legacy, image-as-prompt · not in API catalog |
| Kling O1 Image | 0.5 | 2K | Square default · `kling_omni_image` |
| Seedream 4.0 | 1 | Basic | Older tier · not in API catalog |
| Seedream 5.0 Lite | 1 | 2K | Fast |
| Seedream 4.5 | 1 | 4K | High-res, `quality` basic/high (~6K) |
| Nano Banana | 1 | — | Draw, portrait |
| Wan 2.2 | 1 | — | Artistic · not in API catalog |
| Reve | 1 | — | New (2026-03) · not in API catalog |
| Soul 2.0 | Free | 2K | 5K free gens |
| Soul Cinema | Low | — | Cinematic keyframes · `soul_cinematic` |
| Soul Cast | TBD | — | Character identity, 16:9, `budget` 10–500 |
| Soul Location | TBD | — | Environments, 9 aspect ratios |
| Kling Image 3.0 | TBD | 4K | Native 4K, series mode · not in API catalog |
| Kling Image 3.0 Omni | TBD | 4K | Advanced editing · not in API catalog |
| Nano Banana 2 | 1.5 | 1K | Pro quality at Flash speed |
| Nano Banana 2 Lite | TBD | 1K only | Budget NB2, `thinking` MINIMAL/HIGH |
| FLUX.2 Pro | 1.5 | 2K | ⚠ External |
| Flux Kontext Max | 1.5 | — | ⚠ Edit · now Flux Kontext (`flux_kontext`) |
| Multi Reference | 1.5 | — | Multi-image blend · not in API catalog |
| Recraft 4.1 | varies | 1K/2K | ⚠ External · standard/vector/utility/utility_vector · hex palettes |
| GPT Image | 2 | — | Character slot · not in API catalog |
| GPT Image 2.5 | TBD | 1K–4K | Transparent background, quality to `max` · not yet field-rated |
| Grok Image / Grok Image 2.0 | TBD | 1K / 2K | xAI · not yet field-rated |
| Seedream 5.0 Flash | TBD | up to 2K | Fast + instruction editing · not yet field-rated |
| FLUX.2 Pro Outpaint | TBD (all-crop requests free per the catalog) | — | ⚠ External · per-side expand/crop |
| GPT Image 1.5 | 2 | — | Text-in-image · left the catalog after 2026-06-22 |
| OpenAI Hazel | TBD | — | Editing, best text rendering |
| Character Swap | 2 | — | Body swap |
| Nano Banana Pro | 2 | 1K | Draw, landscape |
| FLUX.2 Flex | 5 | 2K | ⚠ External |
| FLUX.2 Max | 6 | 2K | ⚠ Most expensive |
| Face Swap | Free | — | 2 free then paid |
