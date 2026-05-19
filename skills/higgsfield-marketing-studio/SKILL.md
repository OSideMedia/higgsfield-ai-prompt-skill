---
name: higgsfield-marketing-studio
description: "Use when the user mentions Marketing Studio, DTC Ads, ad video, UGC video, the marketing_studio_video MCP model, or wants to generate one of the 9 Marketing Studio ad presets (UGC, Tutorial, Unboxing, Hyper Motion, Product Review, TV Spot, Wild Card, UGC Virtual Try On, Pro Virtual Try On). Also triggers on hook+setting picklist questions, preset-avatar / custom-avatar / text-generated-avatar handling, 4–15s ad video questions, or any reference to Higgsfield's ad-video product surface. Cross-surface workflow handoffs (GPT Image 2.0 / Soul Cinema / Nano Banana Pro / ms_image image gen → Marketing Studio video) covered in the companion cross-surface-workflow.md."
user-invocable: true
metadata:
  tags: [higgsfield, marketing-studio, dtc-ads, marketing, ugc, ad, video, preset, hook, setting, avatar, cross-surface]
  version: 1.0.0
  updated: 2026-05-18
  parent: higgsfield
---

# Higgsfield Marketing Studio

Marketing Studio is Higgsfield's opinionated short-form ad-video product. Generations are bounded by a 4–15 second per-clip cap [Phase 0: Probe 0.3-b], routed through one of nine named presets that dictate camera language, register, and the available picklist of hooks and settings. It's distinct from Higgsfield's general video models (Soul, Seedance, Cinema Studio) — those let you write whatever you want; Marketing Studio enforces ad-format conventions per preset and ships with a built-in library of preset hooks, settings, and avatars.

This sub-skill covers Marketing Studio video. The two image-side Marketing Studio surfaces (`marketing_studio_image` and `ms_image` / "DTC Ads") are named in §2 but covered in the companion `cross-surface-workflow.md`.

---

## 1. What Marketing Studio is

Marketing Studio is a routing layer on top of `generate_video` for short-form ad creative. You provide a product image (required) plus optional avatar, location, and additional-asset references. You pick one of nine presets. You optionally write a prompt. Marketing Studio handles the rest — camera language, pacing, hook execution, setting context — per the preset's built-in conventions.

The opinionated thing about Marketing Studio is that the preset choice is load-bearing. Pick `Hyper Motion` and you get kinetic product hero shots with an auto pack-shot at the end [SRT-2:00:13:33]. Pick `TV Spot` and you get composed cinematic narrative — sometimes from a five-word prompt when the asset references carry the weight [SRT-3:00:18:30; PDF items 12, 13]. Pick `Wild Card` and you get permission to break ad-grammar conventions [director:L113–L117; PDF items 10, 11]. The presets aren't decoration; they choose the production rules.

When Marketing Studio isn't the right tool:

- If your video needs to run longer than 15 seconds — Cinema Studio (`higgsfield-cinema`) covers narrative length, or use one of the escape-hatch models in §9
- If you need character-consistent multi-shot video with lip-sync — Wan 2.7 or Veo 3.1 are designed for sync (per §9 escape hatches)
- If you want free-form video without ad framing — Seedance (`higgsfield-seedance`), Soul (`higgsfield-soul`), or Cinema Studio give you the open canvas Marketing Studio's preset routing closes off

---

## 2. Two access surfaces — and three MS models

You reach Marketing Studio two ways:

| Surface | How you reach it | What it exposes |
|---|---|---|
| Web UI at `higgsfield.ai` | Browser, direct | Per-generation controls for preset / aspect ratio / quality / duration / hook / setting / avatar / additional asset [SRT-3:00:09:00–00:10:00]. In-app custom avatar generation by text prompt [SRT-3:00:13:00]. In-app product registration by URL scan [SRT-2:00:08:50] |
| MCP via `mcp.higgsfield.ai/mcp` | Custom connector in Claude / Cowork / agent | `show_marketing_studio` for entity management (presets, hooks, settings, avatars, products, brand kits) + `generate_video` with `model: "marketing_studio_video"` for the actual render |

Both surfaces share the same preset / hook / setting / avatar taxonomy. The web UI is what's demonstrated in SRT-2 and SRT-3; the MCP is what `higgsfield-content-factory` orchestrates programmatically.

### Three Marketing Studio models exist — this sub-skill covers the video one

[Phase 0: Probe 0.3-a] surfaced that "Marketing Studio" is three models, not one — source-corpus reconciliation #11:

| Model ID | Display name | Output | Scope in v3.7.13 |
|---|---|---|---|
| `marketing_studio_video` | Marketing Studio | video | **This sub-skill** — 9 ad presets, 4–15s, hook + setting + avatar handling |
| `marketing_studio_image` | Marketing Studio Image | image | Basic product image ads — `resolution` param only (1k/2k/4k), 11 aspect ratios. Out of scope |
| `ms_image` | DTC Ads | image | Full DTC ad image generation — brand-kit-aware, ad-format styles, batch up to 20, max 14 reference media. Out of scope; named briefly in `cross-surface-workflow.md` §3 |

> **Naming note** [from `show_marketing_studio` MCP tool description]: when discussing `ms_image` with the user, refer to it as "DTC Ads" — that's the user-facing brand name. The model ID `ms_image` is internal nomenclature.

This sub-skill scopes to `marketing_studio_video`. References to "Marketing Studio" below mean the video model unless the surrounding text says otherwise.

---

## 3. The 9 presets

The nine presets are the routing layer. Pick one, and Marketing Studio applies its built-in production rules.

| # | Display name | Slug | Hook + setting picklist? | What it's for | Per-preset notes |
|---|---|---|---|---|---|
| 1 | UGC | `ugc` | Yes | Realistic single-take social videos with a person + product [Phase 0: Probe 0.1] | Phone-native selfie framing, handheld, eye-level, single continuous take; casual conversational register [director:L52, L77–L81]. ASMR variant: same preset + `generate_audio: true` + intimate setting + no hook [content-factory L237–L243] |
| 2 | Tutorial | `tutorial` | Yes | Step-by-step how-to / recipe [Phase 0: Probe 0.1] | Stable camera (tripod, overhead rig, locked handheld); cuts allowed between steps; imperative-voice dialogue ("apply," "hold," "press") [director:L83–L87] |
| 3 | Unboxing | `ugc_unboxing` | Yes | High-quality unboxing reveal from packaging | Top-down or 3/4 angle; hands in frame; tactile close-ups on reveal moments [director:L89–L93]. Accepts custom packaging image in the additional-asset slot [SRT-2:00:23:50–00:25:00] |
| 4 | Hyper Motion | `hyper_motion` | **No** | Kinetic product hero shots — splash, pour, spin, drop | Works WITHOUT an avatar [SRT-2:00:13:00]. Default arc renders "element-by-element assembly" with auto pack-shot at the end [SRT-2:00:13:33]. Accepts logos as the hero subject, not just products [SRT-2:00:14:55–00:15:35; PDF item 8]. Whip pans, orbits, speed ramps [director:L95–L99] |
| 5 | Product Review | `product_review` | Yes | Authentic talking-head review with product in hand | Medium shot of presenter + B-roll inserts of product detail [director:L101–L105]. Measured, observational register; third-person |
| 6 | TV Spot | `tv_spot` | **No** | Cinematic narrative spots in polished commercial register | Composed dolly / crane / cinematic framing; structured arc (establishing → product → lifestyle → hero/logo) [director:L107–L111]. Can work with five-word prompts when assets carry the load [SRT-3:00:18:30]. Has a default packshot beat that must be explicitly negated when unwanted [PDF item 13: *"ABSOLUTELY NO PACKSHOT. NEVER SHOW ISOLATED PRODUCTS."*] |
| 7 | Wild Card | `wild_card` | **No** | Surreal one-shot creative concepts | Permission to break conventional ad grammar; impossible geometry, surreal juxtaposition, unexpected scale [director:L113–L117]. Adil's "favorite preset" [SRT-2:00:18:30] |
| 8 | UGC Virtual Try On | `ugc_virtual_try_on` | Yes | Try-before-buy, casual register | Selfie or mirror framing; casual environment; natural movement (turn, walk, gesture) [director:L119–L122]. Phone-native aesthetic, not overly produced |
| 9 | Pro Virtual Try On | `virtual_try_on` | **No** [Phase 0: pre-probe finding — see §4] | Editorial / lookbook-style virtual try-on | Studio-quality. Clean backdrop (cyc wall, studio seamless), controlled lighting, composed poses [director:L124–L128]. Orbit / push-in / static editorial framing |

### Slug naming is canonical; routing mode lives on a different MCP call

**The slug for Pro Virtual Try On is `virtual_try_on`, not `pro_virtual_try_on`** — non-obvious mapping, verified at [Phase 0: Probe 0.1]. The other eight slugs match their display names predictably.

**Preset routing happens via `show_marketing_studio.mode`, NOT via `generate_video.mode`.** The `generate_video` schema for `marketing_studio_video` has no `mode` parameter at all [Phase 0: Probe 0.3-b]. content-factory L681–L692 documented a "slug mismatch table" claiming `generate_video.mode` accepts `ugc_how_to` for Tutorial and `product_showcase` for Hyper Motion — neither slug exists in the live API [Phase 0: supplementary probe]; the entire premise of that table is wrong. Source-corpus reconciliation #7. The actual routing happens in the `show_marketing_studio` flow:

```
1. show_marketing_studio(action='fetch', url='<product URL>', mode='hyper_motion')
   # OR action='create' with uploaded medias[] + mode='hyper_motion'
   # This registers the product AND sets the next-step preset.

2. generate_video(params={
     model: 'marketing_studio_video',
     prompt: '<optional>',
     duration: 8,
     aspect_ratio: '9:16',
     resolution: '720p',
     generate_audio: false
   }, medias=[...], avatars=[...])
```

The preset chosen in step 1 routes the generation in step 2. No `mode` parameter on the `generate_video` call.

---

## 4. Hook + setting picklists

Hooks and settings are open-ended picklists you select by UUID. They're available for **five** of the nine presets, not six.

> **Key rule** [from `generate_video` MCP tool description — Phase 0 pre-probe finding]: hook + setting picklists are supported only for `UGC`, `Tutorial`, `Unboxing`, `Product Review`, and `UGC Virtual Try On`. Pro Virtual Try On is NOT in the family — contradicts content-factory L193–L194 which included it. Source-corpus reconciliation #10.

> Picklist contents drift over time. The Phase 0 snapshot at `../../.planning/v3.7.13/PHASE-0-PROBES.md` is correct as of 2026-05-18; for canonical current data, run the live enumeration calls below.

### Hooks (9 entries as of 2026-05-18) — visual scene templates, not verbal copy

```
show_marketing_studio(action='list', type='hook', size=100)
```

[Phase 0: Probe 0.2a] returned 9 hooks, classified by `type` field as either `stunt` (4) or `subtle` (5):

- **Stunt:** Product Hit, Random Object Mic, Blizzard, Product Dodge
- **Subtle:** Spicy, Interview, Product Crash, Camera Bump, Epic Fail

Each hook ships with a descriptive `prompt` field that explains the visual concept. Example — "Interview": *"Interviewer asks a second stranger a question based entirely on the first stranger's random answer; confusion builds until the second person naturally notices the product (Erewhon-style aspirational item) and pivots into a casual review."* You don't have to use that exact prompt — but the hook's preset structure is what gets baked into the generation.

Pass the hook's UUID as `params.hook_id`. To skip the hook entirely (still on a hook-eligible preset), omit `hook_id`.

### Settings (14 entries as of 2026-05-18) — environment templates

```
show_marketing_studio(action='list', type='setting', size=100)
```

[Phase 0: Probe 0.2b] returned 14 settings, classified by `type` field:

- **Realistic (8):** Bedroom, Bathroom, Kitchen, Office, In Car, Street, Gym, Nature
- **Unrealistic (6):** Airplane Wing, Roofing, Volcano Rim, Tiny Reviewer, Car Roof, Train Surf

Each setting ships with a descriptive `prompt` field describing the scene. Pass the setting's UUID as `params.setting_id`.

### Live-enumeration discipline

The picklist names listed above are a 2026-05-18 snapshot. New hooks and settings get added; existing ones can be revised. For production work — especially when documenting a campaign or building a multi-shot plan — call the live enumeration first and pull the current UUIDs. Hardcoding UUIDs from a stale snapshot is the failure mode this discipline prevents.

When the user describes a scene that matches a known hook or setting name, you can name the hook / setting in your routing without an upfront live enumeration — Marketing Studio's web UI lets users pick by name from the dropdown [SRT-3:00:09:00, 00:09:40]. The UUIDs only matter when you're hitting the MCP directly.

---

## 5. Avatar handling

Marketing Studio takes one avatar per generation. There are three avatar types, and one hard API limit you can't work around without a workaround.

### Three avatar types

| Type | How you create it | When to use |
|---|---|---|
| **preset** | Pick from the built-in library via `show_marketing_studio(action='list', type='avatar')`. Returns ~40 preset avatars as of 2026-05-18 [Phase 0: Probe 0.2c] | When you need a generic face fast and don't want to manage your own |
| **uploaded** | Click upload in the web UI, drop an image, give the avatar a name, click "Create avatar" [SRT-2:00:08:55] | When you have a specific person you want to feature (creator, brand ambassador) |
| **text-generated** | In the web UI, click "Create avatar" and type a description prompt — Marketing Studio generates the avatar on the fly. Example prompts: *"elegant 60-year-old woman"* [SRT-3:00:13:00]; *"Asian woman with pink hair, mid-20s, dressed in soft beige and lilac modern fashion"* [SRT-3:00:18:00] | When you want a specific look you don't have a real person for, or you want different demographics for different ad variants |

content-factory L630 documented preset-only avatars (`avatars: [{ id, type: "preset" }]`); Phase 0 confirms the API accepts `type: 'custom' | 'preset'` and SRT-2 / SRT-3 demonstrate all three creation paths. Source-corpus reconciliation #3.

> **Field-name calibration** [source-corpus reconciliation #9]: content-factory L612 said filter the avatar list by `source: "preset"`; the live API returns the field as `type: "preset"`. Adjust the filter recommendation accordingly.

### Avatar field constraints — consolidated

Three constraints, all enforced at the API or UI level:

1. **The `avatars` array MUST contain exactly one entry.** Marketing Studio rejects two simultaneous avatars at the UI level [SRT-3:00:19:00, verbatim: *"technically you can't use two avatars"*]. `show_marketing_studio.avatars` parameter is explicitly documented as `max 1 item` [Phase 0: pre-probe finding]. Source-corpus reconciliation #5.

2. **Empty `avatars: []` substitutes a random face per render.** content-factory L632–L636 documents this as a silent fallback that kills campaign visual consistency — the same prompt run twice with empty avatars produces two different faces. This claim is source-corpus only; not directly verified in Phase 0 (a multi-generation comparison would be needed to prove randomness). Practical guidance: **always pass an avatar.**

3. **Two-person scenes use the reference-image workaround.** When you need a primary character plus a second person, pass the primary in `avatars` and the secondary as a reference image in `medias` [SRT-3:00:19:00 demonstrated workaround]. Consistent with director L143's `≤ 2 humans tracked` rule.

### What this sub-skill does NOT do

This sub-skill names the three avatar types and the field constraints. It does NOT enumerate individual preset avatars by name. Reasons:

- The preset library drifts over time (avatars added / removed by Higgsfield)
- The live enumeration call is the canonical source — `show_marketing_studio(action='list', type='avatar', size=100)` returns the current list with names, genders, and preview URLs
- Picking by name from the live list is the right pattern for any production work

For reference: the 2026-05-18 snapshot in the Phase 0 log shows 40 preset avatars with a ~24F / ~16M gender ratio. Pick by name from the live list, not from any hardcoded table in this sub-skill.

---

## 6. Reference media — 4 slots

Marketing Studio accepts up to four kinds of reference media. The web UI exposes them as four upload slots; the MCP exposes them across two top-level arrays.

| Slot | Required? | What it carries | How it enters the call |
|---|---|---|---|
| **Product image** | Yes | The thing being advertised — packaging, hangtag, color, label detail must be preserved exactly | `medias[]` array with role `image` (or `start_image` / `end_image` for frame-anchored), OR registered via `show_marketing_studio(action='create' / 'fetch')` first and referenced by UUID |
| **Avatar image** | No (for UGC-family presets it's strongly recommended — see §5) | The person presenting the product | Separate `avatars[]` top-level array — NOT nested in `params` |
| **Custom location image** | No | Pre-generated backdrop or scene (e.g., from Soul Cinema) | Additional entry in `medias[]` array [SRT-3:00:11:30, 00:12:30, 00:14:00] |
| **Additional asset image** | No | Brand asset like custom packaging (e.g., for Unboxing preset) | Additional entry in `medias[]` array [SRT-2:00:24:00] |

### `avatars` is a SEPARATE top-level media slot — not a nested parameter

> **Critical correction** [source-corpus reconciliation #8, Phase 0: Probe 0.3-b]: content-factory L630 documented avatars as `params: { avatars: [...] }` — nested inside `params`. The schema shows `avatars` and `medias` are TWO DISTINCT top-level media arrays declared under the model's `medias` schema entry.

The actual call shape is:

```
generate_video(
  params={
    model: 'marketing_studio_video',
    prompt: '<optional>',
    duration: 8,
    aspect_ratio: '9:16',
    resolution: '720p',
    generate_audio: false,
    hook_id: '<uuid>',         # UGC family only
    setting_id: '<uuid>',      # UGC family only
  },
  avatars=[{id: '<uuid>', type: 'preset'}],   # max 1 — see §5
  medias=[
    {value: '<product uuid or url>', role: 'image'},
    {value: '<location image>', role: 'image'},    # optional
    {value: '<packaging asset>', role: 'image'},   # optional
  ]
)
```

`avatars` and `medias` are sibling parameters at the top level of `generate_video`, NOT nested under `params`. Get this wrong and the call shape rejects.

### Product registration — two paths

Both register the product as a reusable entity you can pass by UUID:

- **From URL scan:** `show_marketing_studio(action='fetch', url='<product page URL>')` — server scans the URL, extracts images, registers the product. Demonstrated live at [SRT-2:00:08:50, verbatim: *"paste in the link and create the product automatically"*]
- **From uploaded media:** `show_marketing_studio(action='create', type='product', medias=[...])` — pass uploaded image media; server registers the product with auto-derived title

After registration, the product UUID is what you pass in subsequent `generate_video` calls. The user's library is enumerable via `show_marketing_studio(action='list', type='product')`.

---

## 7. Generation parameters

Full schema for `marketing_studio_video` from [Phase 0: Probe 0.3-b]:

| Parameter | Type | Required? | Default | Notes |
|---|---|---|---|---|
| `model` | string | required | — | Must be `"marketing_studio_video"` |
| `prompt` | string | **optional** | — | Preset + product + avatar generates without a prompt [SRT-2:00:09:15, verbatim: *"I don't even need a prompt. I'm just going to hit generate"*]. Source-corpus reconciliation #2 — content-factory L469–L485 implied prompt was required; it's not |
| `duration` | integer (seconds) | optional | — | **Range: 4–15s.** Hard cap [Phase 0: Probe 0.3-b]. Outside range gets clamped to nearest allowed |
| `aspect_ratio` | string | optional | — | One of: `auto`, `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, `9:16` [Phase 0: Probe 0.3-b]. UI demos: `9:16` for vertical UGC [SRT-3:00:09:55]; `16:9` for TV-broadcast format [SRT-3:00:19:20] |
| `resolution` | string | optional | `"720p"` | One of: `480p`, `720p`, `1080p`. Default is `720p`; UI exposes `1080p` as "highest" [SRT-3:00:09:55] |
| `generate_audio` | bool | optional | `false` | Set `true` for audio. Output is **auto-scored music**, not just ambient sound [SRT-2:00:12:50, verbatim: *"the music is built in. I didn't have to upload this"*] |
| `hook_id` | string (UUID) | optional | — | UGC family only (see §4). Enumerate via `show_marketing_studio(action='list', type='hook')` |
| `setting_id` | string (UUID) | optional | — | UGC family only (see §4). Enumerate via `show_marketing_studio(action='list', type='setting')` |
| `ad_reference_id` | string (UUID) | optional | — | Reference to a previously-completed ad concept entity (`show_marketing_studio` `type='ad_reference'`). Out of scope for v3.7.13 |
| `folder_id` | string | optional | — | Organizational metadata |
| `width` | number | optional | — | Custom pixel width beyond `aspect_ratio` enum |
| `height` | number | optional | — | Custom pixel height beyond `aspect_ratio` enum |

Top-level media arrays (separate from `params` — see §6):

| Slot | Type | Notes |
|---|---|---|
| `avatars` | array of `{id, type}` | Max 1 entry. `type` is `"preset"` or `"custom"` |
| `medias` | array of `{value, role}` | Roles: `image`, `start_image`, `end_image`. Product image is the primary entry |

### What is NOT in the schema

Three notable absences:

- **No `mode` parameter.** Preset routing happens via `show_marketing_studio.mode` (§3), not via `generate_video.mode`.
- **No `get_cost: true` support.** Marketing Studio models do not support preflight cost estimation [from `generate_video.params.get_cost` MCP tool description — Phase 0 pre-probe finding]. Consistent with the existing `higgsfield-stack` documentation. Verify spend post-hoc via `transactions(limit=200)` (§12).
- **No multi-character avatar slot.** One avatar max — see §5 for the reference-image workaround.

---

## 8. Output prompt style — flowing OR sectioned (NOT a hard rule)

Marketing Studio accepts both prompt styles. Pick the one that fits your concept; don't enforce either as a universal rule.

> **Source-corpus reconciliation #6:** director L213 declared "One continuous flowing paragraph — no section labels, no tags, no headers" as a hard output rule. PDF item 10 (Wild Card — Levitation in Clouds), authored by the same person, uses an explicitly sectioned structure with `Style & Mood:`, `Dynamic Description:`, `Static Description:` headers plus quality suffixes and negative inclusions appended. **The "no section labels" rule is craft opinion about elegant output, NOT an MS engine constraint.** Both styles render correctly.

### When flowing paragraph fits

- Short, concept-driven prompts where the asset references carry the weight. PDF item 8's Hyper Motion logo treatment is literally five words: *"logo creating with comet tail."* No sections needed.
- Five-word TV Spot prompts when the avatar and location assets supply the rest [SRT-3:00:18:30].
- Vanilla UGC where the hook + setting picklist values already structure the generation and the prompt just adds tone.

Flowing paragraph reads like production prose — easier to skim, harder to over-engineer.

### When sectioned structure fits

- Narrative-arc prompts with multiple beats. PDF item 6 (Pro Virtual Try-On — Liquid Scan Transition) uses time-coded segments: `0–3s: FULL BODY SHOT…`, `4–7s: The glasses reach maximum size…`, `8–10s: THE MOMENT the glasses touch her face — LIQUID SCAN TRANSITION…`, `11–15s: MEDIUM CLOSE-UP…`. The time-coding makes the beat structure legible to the model.
- Hyper-detailed Wild Card concepts where you want explicit Style / Dynamic / Static separation. PDF item 10's Levitation in Clouds is the canonical example: `Style & Mood:` (dreamlike high-fashion film, Hollywood wire-work VFX, anamorphic 28mm), `Dynamic Description:` (multi-paragraph action narrative), `Static Description:` (single-frame pose), then quality suffixes ("4K, Ultra HD, Rich details, Sharp clarity, Cinematic texture") and negative inclusions ("No ghosting, No flickering, No text overlays").
- Multi-clip campaigns where one prompt has to render coherently across 5 separate generations. PDF item 7 (UGC Try-On — 5 Clips Indoor Room) uses `## CLIP 1 — 4s`, `## CLIP 2 — 4s — JACKET`, etc.

### Picking between them

Default to flowing paragraph for prompts under 50 words. Use sectioned structure when the prompt has discrete beats (time-coded narrative, multi-clip campaign, explicit Style / Dynamic / Static separation). Don't impose section labels on a prompt that doesn't need them — but don't refuse to use them on a prompt where the structure actually helps.

---

## 9. What Marketing Studio cannot do

Six things Marketing Studio is not designed for. Trying to force these typically produces broken output:

1. **Clips longer than 15 seconds.** Hard cap at the API level [Phase 0: Probe 0.3-b]. For longer narrative, design as a 2-clip or 5-clip sequence (each clip ≤15s) and edit externally — PDF item 7 demonstrates the 5-clip pattern.
2. **Lip-synced dialogue from non-human characters.** Talking fruit, talking products, etc. — the model doesn't reliably sync audio to non-face geometry.
3. **Multi-character coordinated dialogue with consistent identities across cuts.** The one-avatar API limit (§5) prevents this; even with the reference-image workaround, identity drift across multiple generations is high.
4. **Single output with multiple settings, split-screen, or day-X-vs-day-Y diary structure.** One setting per generation. For multi-setting narrative, split into separate clips per the multi-clip pattern. PDF item 11 (Wild Card — Jacket Portal Cuts) is the workaround when six locations must appear in one 15s clip — uses portal-cut transitions instead of a multi-setting parameter.
5. **Free-form `hook_id` or `setting_id` not in the picklist.** Picklists are closed — you can only pass UUIDs returned by `show_marketing_studio(action='list', type='hook'|'setting')`. To skip the hook, omit `hook_id`.
6. **More than one avatar per generation.** One avatar slot, enforced. Workaround: primary in `avatars`, secondary as reference image in `medias` (§5).

### Escape-hatch models for what MS can't render

When an idea genuinely needs lip-sync, longer narrative, or multi-shot continuity, route to one of these instead of forcing MS [content-factory L260–L264]:

- **Wan 2.7** — synchronized audio + character-consistent video
- **Veo 3.1** — ultra-realistic cinematic, audio-friendly
- **Cinema Studio Video 3.0** — most advanced cinema-grade
- **Seedance 2.0** — reference-driven, multi-SKU, consistent identity
- **Kling 3.0** — multi-shot, audio sync, motion transfer

Use the escape hatch sparingly — Marketing Studio's opinionated structure is the value, and reaching for an escape model means losing the preset routing.

---

## 10. Worked examples — production reference library

Eight production-grade Marketing Studio prompts, sourced from `PRODUCT GENERATION PROMPTS EXAMPLES.pdf` items 6–13. These are the raw prompts Adil used to generate the HIGGS fictional clothing brand demonstrated in the SRT-2 video. Maximum credibility — paired prompt + video evidence for each.

Each example is cited by PDF item number plus the SRT-2 timestamp where the resulting video appears on camera.

### 10.1 — Pro Virtual Try-On — Liquid Scan Transition
*Source: PDF item 6, paired SRT-2 demo at ~00:11:30. Sectioned time-coded structure across 4 beats within a single 15s clip.*

```
all HIGGS items including: white jersey t-shirt, neon yellow puffer jacket, black
track pants with neon green stripe, grey sneakers with neon yellow laces, and
black-to-neon-yellow gradient sunglasses. the female model — use her exact face,
hair, and body throughout the entire video without any changes.

CAMERA: COMPLETELY STATIC throughout the entire video. Fixed position, fixed
angle, zero movement. Only subjects and objects move within the frame.

Location part 1: Urban pedestrian overpass bridge. Glass-panel ceiling above
letting in diffused grey daylight. Metal railings on both sides, concrete floor,
city street with traffic visible far below. Overcast natural lighting.

Location part 2: Dark underground parking garage. Single harsh overhead lamp,
tight pool of light on concrete floor, deep shadows, concrete pillars in background.

0–3s: FULL BODY SHOT — static camera, low angle pointing upward. Female
model stands centered on the overpass in her own clothes, relaxed stance. She
raises the HIGGS sunglasses pinched between two fingers, cocks her wrist back,
then THROWS the glasses forward toward the camera with a sharp snap. The
sunglasses fly directly at the static lens in full 3D — tumbling and spinning in slow
motion, growing larger frame by frame until they nearly fill the screen. Glasses
stay fully intact. Neon yellow frame catches daylight. Model stands still in the
blurred background. CAMERA DOES NOT MOVE.

4–7s: The glasses reach maximum size, SLOW DOWN, STOP mid-air, then
REVERSE on their own — flying back toward the model spinning. As they travel
back the model shifts her pose dynamically — she leans her head slightly forward
to meet the glasses, lifts her chin, squares her shoulders with attitude. The
glasses arc back and land perfectly onto her face. CAMERA STATIC.

8–10s: THE MOMENT the glasses touch her face — LIQUID SCAN TRANSITION: a
wave of liquid mercury ripples outward from her face across the entire frame, like
a 3D scan pulse sweeping through space. The overpass environment MELTS and
DISSOLVES in 3D depth — the bridge, railings, ceiling peel away in layers like
liquid geometry dissolving into the scan wave. The dark parking garage
MATERIALIZES through the liquid scan, environment rebuilding itself in 3D layers
from background to foreground as the wave passes. Simultaneously the full
HIGGS outfit liquifies onto her body: white jersey t-shirt, neon yellow puffer jacket,
black track pants with neon green stripe, grey sneakers with neon yellow laces —
all five items flow onto her in one fluid wave synced with the environmental scan.
The model strikes a new powerful pose as the outfit locks in — weight shifted to
one leg, one hand at side, chin up. CAMERA STATIC.

11–15s: MEDIUM CLOSE-UP — static camera at chest-to-head height. She stands
fully dressed in all HIGGS items in the parking garage. Hard overhead lamp light,
sharp shadows. She adjusts sunglasses with one finger, holds the pose, stares
directly into camera with cold confident expression. No glow, no outlines on body.
Cinematic grade — deep blacks, punchy contrast, neon yellow only as real material
color on clothing. 9:16 vertical.
```

What makes this example work: the time-coded segments give the model discrete beats to render. The Camera Contract opens with a hard rule (`COMPLETELY STATIC`, `CAMERA DOES NOT MOVE`) and reinforces it at every segment boundary. The avatar-fidelity directive (*"use her exact face, hair, and body throughout the entire video without any changes"*) is the explicit identity lock content-factory describes.

### 10.2 — UGC Try-On — 5 Clips Indoor Room
*Source: PDF item 7. Multi-clip campaign pattern — five separate generations of 3–4s each, sharing one location + camera contract.*

```
# HIGGS — 5 CLIPS

LOCATION: Indoor room. Large white-framed floor-to-ceiling glass door centered
in background. Dark night outside. Grey linen curtains floor-length on both sides.
Warm hardwood parquet floor. Cool blue backlight from behind the door, soft
frontal key light on face. Cold blue-teal cinematic color grade.
CAMERA: STATIC, FULL BODY SHOT, eye level. Same angle all 5 clips, never moves.
IMPORTANT: Female model has NO bag, NO backpack, NO purse on her at any
point in any clip. Hands are empty unless specified.

---

## CLIP 1 — 4s
Female model stands centered in her own clothes. No bag, no backpack. She
reaches off-frame, grabs the white HIGGS jersey t-shirt, pulls it over her head and
on — adjusts it, smooths it down. Looks into camera. No effects. 9:16 vertical.

---

## CLIP 2 — 4s — JACKET
Female model stands centered, already wearing the white HIGGS t-shirt. No bag,
no backpack. She reaches off-frame, grabs the HIGGS puffer jacket, shrugs it on
— one arm then the other — adjusts collar with both hands. Looks into camera.
No effects. 9:16 vertical.

---

## CLIP 3 — 4s — PANTS + SNEAKERS

Female model stands centered, already wearing HIGGS t-shirt and jacket. No bag,
no backpack. Already wearing HIGGS track pants with neon green side stripe and
grey HIGGS sneakers — changed off-screen. She runs one hand down the side
stripe, lifts one foot and stomps on the parquet once. Looks into camera. No
effects. 9:16 vertical.

---

## CLIP 4 — 3s — SUNGLASSES
Female model stands centered, fully dressed in HIGGS outfit. No bag, no
backpack. She holds the HIGGS sunglasses between two fingers, slides them onto
her face in one smooth motion. Looks into camera — cold confident expression.
No effects. 9:16 vertical.

---

## CLIP 5 — 3s — FINAL
Female model from stands centered, complete HIGGS outfit, sunglasses on. No
bag, no backpack. Arms relaxed at sides. She squares her shoulders, looks
directly into camera. Says: "That's it." Holds the pose cold and still. 9:16 vertical.
```

What makes this example work: the shared `LOCATION` and `CAMERA` blocks at the top apply to all 5 clips — the model gets a consistent rendering context. Each clip is named (`CLIP N — Xs — DESCRIPTOR`) so the editor can sequence them. The "no bag, no backpack" line is a negative constraint repeated in every clip — common pattern when the model has been adding incidental props.

### 10.3 — Logo — Hyper Motion
*Source: PDF item 8. Verbatim Adil prompt from SRT-2:00:15:10. The five-word minimum.*

```
logo creating with comet tail.
```

What makes this example work: Hyper Motion runs on extremely short prompts when an asset reference carries the load — the preset supplies the kinetic structure, so the prompt only has to name the concept. Output (per SRT-2:00:15:35): outer space scene, comet trail, logo materializes at the end with the brand name. No section labels, no quality suffixes, no negative inclusions — and it works.

### 10.4 — Pro Virtual Try-On — Skateboard Outfit Change
*Source: PDF item 9, paired SRT-2 demo at 00:18:00–00:19:00. Long continuous-take prompt with items appearing in air.*

```
The character — dark hair, grey tank top, oversized dark red baggy jeans,
crossbody tactical bag, red bandana on wrist, red paint mark on nose — rides a
skateboard continuously from left to right across the frame. Smooth push, steady
cruise, never stopping. Camera stays strictly side-on the entire time, drifting
smoothly alongside him at constant speed and height, never ahead, never behind,
never rotating. One continuous uncut shot.

As he skates, individual clothing items from the HIGGS collection levitate in the air
ahead of him — floating still, at body height, positioned exactly where they would
sit on a person — waiting. He skates straight through each one without slowing.
The moment he passes through a levitating item it is instantly on his body,
perfectly fitted, as if it was always there. No animation, no effect, no flash — it
simply appears on him as he exits the other side.

Item 1 — white and black HIGGS football jersey: floating at chest height in open air,
he skates through it, it is on him.
Item 2 — black cargo pants with neon green stripe: floating at waist height, legs
hanging naturally, he skates through it, it is on him.
Item 3 — neon yellow-black puffer jacket: floating with sleeves open wide, he
skates through it, it is on him.
Item 4 — grey and neon yellow chunky sneakers: floating at board level, pair side
by side, he skates through them, they are on his feet.
Item 5 — black wraparound sunglasses with neon yellow frame: floating at face
height, he skates through them, they are on his face.

After the last item he is fully dressed in the complete HIGGS collection. He does
not slow down. He pushes once more and keeps skating. Camera drifts to a halt.
He disappears into the distance still rolling. Frame holds on the empty space
where he just was. Silence.

Background: a single continuous urban environment scrolling — raw concrete wall,
cracked asphalt ground with skate marks, hard midday sun casting a sharp
shadow alongside him the entire time. Neon yellow-green appears on wall
markings and signage as he passes.

Sound: continuous skateboard wheel roll on asphalt throughout, occasional push
foot scrape. Each item landing produces no sound. No music. City ambience, wind,
distant traffic. Style: photorealistic cinematic, 2.39:1 Cinemascope, desaturated
warm daylight, neon yellow-green as the only saturated color, streetwear editorial,
identical grain throughout, strict side-on camera drift, one unbroken take.
```

What makes this example work: the Camera Contract is precise — *"strictly side-on… drifting smoothly alongside him at constant speed and height, never ahead, never behind, never rotating."* The five items are enumerated separately with location specifications. The Style block at the end ties it together (2.39:1 Cinemascope, desaturated warm daylight). Continuous-take discipline runs through every sentence.

### 10.5 — Wild Card — Levitation in Clouds
*Source: PDF item 10. Canonical example of sectioned-prompt structure (Style & Mood / Dynamic Description / Static Description).*

```
# LEVITATION IN CLOUDS — ONE SHOT HANDHELD

Style & Mood: Dreamlike high-fashion film. Practical Hollywood VFX — wire-work
levitation with camera operator also suspended on rig. Handheld shaky camera,
real operator breathing and body sway, no stabilization. Golden hour light breaking
through massive cloud formations. Anamorphic 28mm wide, natural film grain,
deep focus. One continuous unbroken shot, no cuts.

Dynamic Description: The camera is already mid-air, shaking with real handheld
weight, chasing the character from @image_1 who flies upright through a vast
open sky between towering cumulus clouds. The character glides ahead of the
camera in a natural standing pose — body vertical, arms slightly away from sides,
head tilted up, the outfit fabric pulling and fluttering backward from wind
resistance. The camera operator struggles to keep up, the framing loose and
imperfect, the character drifting in and out of center frame — the imperfection
sells the reality. The character banks left gently, leaning the whole body into the
turn like a bird, and glides through a narrow canyon between two massive cloud
walls — the camera follows, shaking harder from the turbulence, white vapor
streaking past the lens, momentarily obscuring the shot, then clearing. Golden
sunlight flashes in and out as the character weaves between cloud shadows and
sun pockets — the exposure shifts naturally, bright to dark to bright. The character
reaches one arm forward, fingers spread, dragging through a wisp of cloud, the
vapor splitting around the hand and trailing off the fingertips. The other arm stays
relaxed at the side. The character punches through a thin cloud layer — vapor
exploding around the body — and emerges into open golden sky above the cloud
floor, the sun massive and low on the horizon. The character slows, arms
dropping, floating upright, decelerating gently. The camera catches up and drifts
to face them frontally. The shaking calms. The character hangs still in the golden
light, the infinite cloud ocean below, breathing, fabric settling. The camera holds,
still swaying gently.

Static Description: Vast open sky between massive cumulus cloud formations.
Golden hour sun low on horizon. Single character flying upright in a natural vertical
pose — no flips, no spins, no unnatural body contortion. Handheld camera on wire
rig — real operator shake, no stabilization. Practical wire-work VFX. Real wind, real
cloth physics, real exposure shifts. One continuous unbroken shot. Stylized 3D
animation. 4K, Ultra HD, Rich details, Sharp clarity, Cinematic texture, No
ghosting, No flickering, No text overlays, No watermarks, No subtitles, Stable
picture, Realistic cloth physics.
```

What makes this example work: the `Style & Mood:` block establishes the aesthetic frame (dreamlike, anamorphic, golden hour, one continuous shot). The `Dynamic Description:` block is the narrative action — what happens. The `Static Description:` block describes the held final frame. Quality suffixes and negative inclusions appended at the end ensure the model doesn't fill with unwanted artifacts. This is the example that refutes director L213's "no section labels" rule — sectioned structure works when the prompt is genuinely multi-beat.

### 10.6 — Wild Card — Jacket (Portal Cuts Between Locations)
*Source: PDF item 11. Multi-location single-take using portal-cut transitions.*

```
As Roko moves through the frame, vertical floor-to-ceiling rectangular cuts appear
ahead of him in open air — no border, no frame, no door, no arch, just a hard
straight-edged cut where one world ends and another begins. He walks and then
runs straight through each one without slowing.

Location 1 — rooftop of a housing block, midday: raw concrete underfoot, AC units
and satellite dishes, laundry lines overhead, harsh flat sun, city sprawl visible
beyond the edge, pigeons scatter as he passes.
Location 2 — outdoor basketball court, afternoon: cracked asphalt, faded court
markings, chain-link fence casting grid shadows across everything, a ball rolling
slowly across his path.
Location 3 — underpass, bright midday: concrete pillars, graffiti walls, skate marks
on the ground, a lone skater frozen mid-trick in the background, sun cutting in
hard from both ends.
Location 4 — street market, midday: folding tables with bootleg merch, tarpaulin
roofs, people parting as he moves through, cardboard boxes stacked high, sun
bleaching everything pale.
Location 5 — empty parking lot, late afternoon: flat open asphalt, faded yellow
lines, long hard shadows, a shopping cart on its side, heat shimmer off the ground.
Location 6 — rooftop again at golden hour, different building: wider, emptier, just
open sky and city behind him. He slows to a walk. Then stops facing right. Stands
still. Wind moves his clothes. Silence.

The background of each location scrolls naturally as he moves through it. Each
rectangular cut between worlds is pixel-sharp, hard edge, no blending, no
transition effect — just a seam in space. Sound: footsteps on concrete throughout,
texture shifts slightly each location. No music. Wind, city noise, distant traffic.
Style: photorealistic cinematic, 2.39:1 Cinemascope, desaturated warm daylight,
streetwear editorial, identical grain across all six spaces, static side-on camera,
one unbroken take.
```

What makes this example work: six distinct locations in one 15s clip — Marketing Studio's "one setting per generation" guidance gets explicitly worked around via the portal-cut device. The locations are described concretely (specific props, lighting, time of day, ambient sound). Style block at end maintains visual consistency across the six environments.

### 10.7 — TV Spot — Version 1
*Source: PDF item 12. Short prompt with explicit camera + cut direction.*

```
Monochrome city street. Crowds blur past in long exposure. One guy walks toward
camera, wearing acid green and black streetwear. No green elements in the
environment — no lines, no glow. Only the clothing fabric is colored, everything
else is strictly black and white. Cut with fast negative invert flashes — full frame
color inversion, 2-3 frames each through the clip. Quick, cold, confident. Dynamic
streetwear commercial. No VFX. No box unpacking.
```

What makes this example work: the look is specified with a single inversion device (monochrome environment + colored clothing fabric only). The cut pattern (fast negative invert flashes, 2–3 frames each) is concrete. Negative constraints at the end (*"No VFX. No box unpacking."*) cut against TV Spot's default packshot tendency.

### 10.8 — TV Spot — Version 2
*Source: PDF item 13. Same monochrome concept as 10.7 but with explicit packshot suppression.*

```
Monochrome city street, empty and cold. Blurred ghostly figures drift past in long
exposure — faceless, weightless, grey. A single figure walks through the street —
full natural color, acid green and black streetwear, face visible, natural confident
walk. Quick cuts between different camera angles — medium front, medium side,
medium close face level. He just walks, no dancing, no posing, no gestures.
Camera orbits around him 180 degrees on one shot. Invert flash on every cut —
full frame color inversion, nothing else. Cut to black. NO visual effects, NO
lightning, NO energy beams, NO particles, NO light trails on the character. Only
full-frame invert flashes on cuts. ABSOLUTELY NO PACKSHOT. NEVER SHOW
ISOLATED PRODUCTS.
```

What makes this example work: the negative constraint at the end (`ABSOLUTELY NO PACKSHOT. NEVER SHOW ISOLATED PRODUCTS.`) tells you something about Marketing Studio's TV Spot default — it likes to end on a packshot beat, and you have to negate that explicitly if you want a different ending. The repeated "NO X" pattern (lightning, energy beams, particles, light trails) is the canonical way to suppress visual artifacts the model adds without prompting.

---

## 11. Cross-surface workflow context

Marketing Studio doesn't operate alone in practice. Adil's documented production recipe across SRT-1 / SRT-2 / SRT-3 routes brand-identity assets through GPT Image 2.0, locations through Soul Cinema, refinements and packaging through Nano Banana Pro — then feeds the outputs into Marketing Studio as reference media for the final video. The Higgsfield platform also exposes its own native `ms_image` ("DTC Ads") surface for image generation that Adil didn't use but is available [Phase 0: Probe 0.3-a].

When the user asks about building a full ad campaign (brand identity → product mockups → packaging → ad videos), route to the companion `cross-surface-workflow.md`. It documents the four-surface recipe, names the `ms_image` alternative, and pairs PDF items 1–5 + 14 (the image-side prompts from the same SRT-2 production session) with the SRT timestamps where each appears on camera.

---

## 12. Pricing characteristics

Marketing Studio pricing is plan-dependent. There's no preflight cost estimation available — `get_cost: true` is explicitly unsupported for Marketing Studio models [Phase 0: pre-probe finding from `generate_video.params.get_cost` description]. You verify spend post-hoc.

### Two rate samples — neither canonical

| Source | Implied rate | Context |
|---|---|---|
| `higgsfield-content-factory` L897–L899 | Creator plan ≈ $0.02/credit; Team/Pro ≈ $0.01–$0.005/credit | Tagged "approximate" and "common"; flagged as plan-dependent |
| Adil's lived production (SRT-1:00:21:35) | ~$0.06/credit implied (15,000 credits ≈ $900 for 100 videos = ~150 credits per video) | Specific plan tier not stated; consistent with SRT-3:00:16:00's "~$9 for one Wild Card generation" data point |

The two rates disagree because they reflect different plan tiers and different time points. Neither is canonical Higgsfield pricing.

### Use the higher anchor for budget planning

For budget planning conversations, lean on **~$0.06/credit ≈ ~$9 per video** as the more credible anchor. It's Adil's lived experience and is internally consistent across two independent SRT data points. The lower "common Creator plan" rate from content-factory is tagged-approximate and may reflect an older pricing tier.

### Post-hoc verification

```
transactions(limit=200)
```

Pull recent transaction history after a campaign run. Filter by date range to isolate the campaign's actual spend. Sum credits per preset / per model. This is the only verifiable way to know what a Marketing Studio campaign actually cost — there is no preflight path for MS.

For broader preflight discipline on non-MS models (Kling, Seedance, etc.), see `../higgsfield-stack/SKILL.md` § Preflight discipline. MS is the exception, not the rule.

---

## 13. Source acknowledgment

Marketing Studio coverage in this sub-skill is translated from source material by Adil — Higgsfield's marketing-tools creator. Source corpus:

- **`marketing-studio-director.md`** — single-purpose prompt-director skill for Marketing Studio. Source for the per-preset register rules (§3), engine constraints, and output-format conventions (reframed in §8).
- **`higgsfield-content-factory.md`** — 5-stage MCP-orchestration skill for full-pipeline campaign production. Source for API-level capability claims (most superseded by Phase 0 live MCP probes; see source-corpus reconciliations in the v3.7.13 CHANGELOG).
- **YouTube demonstration series** (3 videos):
  - *"Higgsfield MCP + Claude Just Changed Marketing Forever"* (SRT-1) — content-factory pipeline walkthrough
  - *"I Created a $1,000,000 Brand Using AI"* (SRT-2) — HIGGS clothing brand build via Marketing Studio web UI
  - *"I Launched a Beauty Brand From Scratch Using AI"* (SRT-3) — HIGGS Beauty brand build via Marketing Studio web UI
- **`PRODUCT GENERATION PROMPTS EXAMPLES.pdf`** — raw production-prompt export from the SRT-2 build. Items 6–13 embedded in §10 of this sub-skill; items 1–5 + 14 embedded in `cross-surface-workflow.md`.

### Verification pass

Per the v3.7.11 plausibility-over-verification discipline applied recursively to source material — every API claim in this sub-skill cites a Phase 0 live MCP probe verdict; every behavioral claim cites an SRT timestamp or PDF item number. Full verification trail at `../../.planning/v3.7.13/PHASE-0-PROBES.md`.

Twelve source-corpus reconciliations applied during translation (5 API-architecture / 4 capability / 2 calibration / 1 cross-surface), grouped and explained in the v3.7.13 CHANGELOG entry. Adil is credited as source throughout; the reconciliations are documentation of source-material truth at translation time, not critique of the source.
