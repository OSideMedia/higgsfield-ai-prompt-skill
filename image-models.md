# Higgsfield Image Models — Complete Reference

All image models available in the Higgsfield Image tab.
⚠ = Third-party/external model (warning triangle shown in UI)
G = Google-powered model

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

---

### Higgsfield Soul (Legacy)
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

### Kling O1
**Credits:** 0.5 per generation
**UI:** Kling O1 · 1:1 · 2K · 1/4 · Unlimited
**Best for:** Clean, high-quality 2K images at low cost · square format social content
**vs Z-Image:** 3x the cost but 2K resolution and Kling model quality
**Default aspect:** 1:1 — native square. Good for Instagram/social.
**Note:** Image-only version of the Kling engine (same family as Kling 2.6/3.0 video)

---

### WAN 2.2
**Credits:** 1 per generation
**UI:** WAN 2.2 · 3:4 · Style On/Off · 1 generation
**Best for:** Stylized / artistic image output · non-photorealistic aesthetics
**vs WAN video:** Same model family as Wan 2.5/2.6 video — painterly, artistic, non-photorealistic strengths carry over to image
**Style toggle:** On enables stylization mode

---

### Multi Reference
**Credits:** 1.5 per generation
**UI:** Multi Reference · 3:4 · Style On/Off · 1/4 · Unlimited
**Best for:** Compositing elements from multiple reference images into one generation
**Use when:** You have several reference photos (character, location, prop, color) and want to blend them into a single coherent output
**How it works:** Upload multiple reference images, the model synthesizes a new image drawing from all references simultaneously
**Prompt tip:** Be explicit about which element comes from which reference

---

### Reve
**Credits:** 1 per generation
**UI:** Reve · 3:4 · Standard quality · 1/4 · Unlimited
**Best for:** General-purpose image generation
**Quality selector:** Standard (only option visible — may have additional tiers)
**Note:** Newer model in the lineup — less known quantity, worth testing for versatile generation

---

## Seedream Family

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
**@ Elements:** Supports @ syntax for referencing saved Elements
**vs 5.0 Lite:** Higher resolution (4K vs 2K), same cost, slower generation

---

### Seedream 4.0
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

---

### Nano Banana 2
**Google model:** Gemini 3.1 Flash Image
**Released:** February 26, 2026 — brand new (2 days old at time of writing)
**Credits:** 1.5 per generation
**UI:** Nano Banana 2 · 16:9 · 1K · 1/4
**Best for:** Pro-quality output at Flash speed · rapid iteration on complex prompts · character-consistent multi-image workflows

**What it is:** Google's "best of both worlds" — Nano Banana Pro's intelligence at Nano Banana's speed. Now the default image model across most Google surfaces (Gemini app, Search, Flow, Google Ads). Pro remains available for maximum-fidelity specialized tasks.

**Capabilities (inherited from Pro, delivered at Flash speed):**
- Advanced world knowledge and real-time Search grounding
- Precision text rendering and in-image translation
- Subject consistency: up to 5 characters and 14 objects in one workflow
- Precise instruction following for complex, multi-part prompts
- Production-ready specs: 512px to 4K, all major aspect ratios

**When to use NB2 vs Pro:**
- NB2: rapid iteration, strong results fast, character consistency, text accuracy
- Pro: absolute maximum fidelity, Thinking mode reasoning, 14-ref-image compositing, when quality matters more than speed

**When to use NB2 vs base Nano Banana:**
- NB2 is dramatically better at everything — base is only worth using for its Draw feature

**Status:** Rolling out — processing slower than usual during initial deployment
**No Draw yet** — Draw feature exists only in base Nano Banana and Nano Banana Pro

**SynthID + C2PA:** All Nano Banana family outputs include an invisible SynthID watermark and C2PA Content Credentials for AI provenance verification

## GPT Image Family (OpenAI-powered)

### GPT Image
**Credits:** 2 per generation
**UI:** ChatGPT · 1:1 · Mid quality · 1/4 · Unlimited · Character slot
**Best for:** Instruction-following · complex multi-element prompts · character slot integration
**Quality selector:** Low / Mid / High
**Character slot:** Supports Soul ID character reference (GENERAL shown by default)
**Default aspect:** 1:1 square
**Note:** Model selector shows "ChatGPT" branding — OpenAI's GPT-Image model

---

### GPT Image 1.5
**Credits:** 2 per generation
**UI:** GPT Image 1.5 · 1:1 · Low quality · 1/4
**Best for:** Complex prompts · text-in-image · precise instruction following
**Quality selector:** Low / (implied Medium/High)
**vs GPT Image:** Newer version. Default shown at Low quality (faster/cheaper mode). No character slot visible.
**Text in image:** GPT Image 1.5 handles text rendering better than most models
**Note:** Same credit cost as original — upgrade when you need better prompt adherence

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

### Flux Kontext
**Credits:** varies
**UI:** ⚠ Flux Kontext · (editing interface)
**Best for:** Targeted image editing · inpainting · modifying specific areas of an existing image
**Use when:** You have an image you want to change, not generate from scratch
**vs generation models:** This is an editing model — input is an existing image + instruction

---

### Flux Kontext Max
**Credits:** 1.5 per generation
**UI:** ⚠ Flux Kontext Max · 3:4 · Style On/Off · 1/4 · Unlimited
**Best for:** Higher-quality version of Flux Kontext editing
**vs Kontext:** Same editing purpose, higher quality output, portrait default (3:4)
**Style toggle:** On enables stylization during edit

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

---

## Complete Cost Reference

| Model | Credits | Resolution | Notes |
|-------|---------|-----------|-------|
| Z-Image | 0.15 | — | Cheapest |
| Higgsfield Soul | 0.5 | 2K | Legacy, image-as-prompt |
| Kling O1 | 0.5 | 2K | Square default |
| Seedream 4.0 | 1 | Basic | Older tier |
| Seedream 5.0 Lite | 1 | 2K | Fast |
| Seedream 4.5 | 1 | 4K | High-res |
| Nano Banana | 1 | — | Draw, portrait |
| WAN 2.2 | 1 | — | Artistic |
| Reve | 1 | — | New |
| Soul 2.0 | Free | 2K | 5K free gens |
| Nano Banana 2 | 1.5 | 1K | New, slow rollout |
| FLUX.2 Pro | 1.5 | 2K | ⚠ External |
| Flux Kontext Max | 1.5 | — | ⚠ Edit |
| Multi Reference | 1.5 | — | Multi-image blend |
| GPT Image | 2 | — | Character slot |
| GPT Image 1.5 | 2 | — | Text-in-image |
| Character Swap | 2 | — | Body swap |
| Nano Banana Pro | 2 | 1K | Draw, landscape |
| FLUX.2 Flex | 5 | 2K | ⚠ External |
| FLUX.2 Max | 6 | 2K | ⚠ Most expensive |
| Face Swap | Free | — | 2 free then paid |
| Grok Imagine Image | — | 1K / 2K | Photorealistic, text/logo, multi-image editing |
