# v3.7.13 Phase 0 — Live MCP Probe Verified-Facts Log

**Date:** 2026-05-18
**Operator:** Claude Code session, Higgsfield MCP via `mcp__claude_ai_Higgsfield__*` tools
**Account:** team plan, baseline balance 2,771.67 credits
**Spend budget (per DECISION 6):** $25 ceiling (~2,500–5,000 credits at Team rate $0.005–$0.01/credit)
**Spend used:** **0 credits** — all verification closed via free probes; spend probes (0.3-spend, 0.4) deferred per discipline (see verdicts)
**Scope:** Probes 0.1, 0.2a/b/c, 0.3-a, 0.3-b per v3.7.13 plan Phase 0 spec, plus one supplementary free probe (mode normalization via `show_marketing_studio`)

---

## Pre-probe intel surfaced from tool schemas

Before running any live probe, the loaded MCP tool descriptions surfaced four findings — included here because they are verified-by-schema facts even though no live call was made:

| Pre-probe finding | Source (tool description) | Verdict | Correction flag |
|---|---|---|---|
| Hook/setting support limited to 5 presets: UGC, Tutorial, Unboxing, Product Review, UGC Virtual Try On | `generate_video` tool description | CONTRADICTS content-factory L193–L194 (which listed 6 — included `virtual_try_on` / Pro Virtual Try On in the family) | **Correction #10 candidate** |
| `get_cost: true` not supported for marketing studio models | `generate_video.params.get_cost` description | CONFIRMS our existing `higgsfield-stack` claim (no preflight for MS) | No correction — confirms existing skill |
| `avatars` accepts `type: 'custom' \| 'preset'` (max 1 item) | `show_marketing_studio.avatars` parameter description | CONFIRMS correction #3 (avatar types broader than content-factory's "preset only") AND correction #5 (one-avatar API limit) | No new correction — confirms §11 #3 + #5 |
| New entity types beyond source corpus: `ad_reference`, `brand_kit`, `image_style`/`ad_format`, plus `webproduct` vs `product` distinction | `show_marketing_studio.type` enum + description | NEW INTEL — beyond source-corpus scope | Documented as out-of-scope for v3.7.13 |

---

## Probe 0.1 — Preset enumeration

**Call:**
```
show_marketing_studio(action='presets')
```

**Response (verbatim):**
```json
{"presets":[
  {"mode":"UGC","description":"Realistic social media videos","type":"UGC","preset_type":"UGC","slug":"ugc"},
  {"mode":"Tutorial","description":"Step-by-step tutorials","type":"Tutorial","preset_type":"Tutorial","slug":"tutorial"},
  {"mode":"Unboxing","description":"High-quality unboxing","type":"Unboxing","preset_type":"Unboxing","slug":"ugc_unboxing"},
  {"mode":"Hyper Motion","description":"Highlight your product","type":"Hyper Motion","preset_type":"Hyper Motion","slug":"hyper_motion"},
  {"mode":"Product Review","description":"Authentic product reviews","type":"Product Review","preset_type":"Product Review","slug":"product_review"},
  {"mode":"TV Spot","description":"Authentic stories, amplified","type":"TV Spot","preset_type":"TV Spot","slug":"tv_spot"},
  {"mode":"Wild Card","description":"A unique and creative video mode for custom ideas","type":"Wild Card","preset_type":"Wild Card","slug":"wild_card"},
  {"mode":"UGC Virtual Try On","description":"Try before you buy","type":"UGC Virtual Try On","preset_type":"UGC Virtual Try On","slug":"ugc_virtual_try_on"},
  {"mode":"Pro Virtual Try On","description":"Advanced virtual try-on","type":"Pro Virtual Try On","preset_type":"Pro Virtual Try On","slug":"virtual_try_on"}
]}
```

**Verdict:** **CONFIRMS** content-factory L180–L191 9-preset list and all slug values exactly. Also surfaces the short `description` field for each preset (useful sub-skill content). **No `ugc_how_to` or `product_showcase` slugs appear** — partial refutation of content-factory's slug-mismatch table (full refutation in Probe 0.3-b + supplementary probe).

**Correction-candidate flag:** None at this probe — full slug-mismatch correction recorded under Probe 0.3-b.

---

## Probe 0.2a — Hook picklist

**Call:**
```
show_marketing_studio(action='list', type='hook', size=100)
```

**Response (9 hooks, abbreviated to id/name/type/prompt — full thumbnail/video URLs omitted):**
```json
[
  {"id":"3d45fb46-254f-4c83-9685-8e3d28945a67","type":"stunt","name":"Product Hit","prompt":"Object flies into frame, hits subject. Brief reaction → pivot to product."},
  {"id":"75b6d501-be0e-4416-a7ed-52f04f180574","type":"subtle","name":"Spicy","prompt":"The shot starts with an extreme close-up of a collarbone, slowly tilts up to reveal a flawless makeup look, then pulls back into selfie framing before a silent pause leads into the product pitch."},
  {"id":"26cac2dd-99cb-4818-a678-509b0dab2c32","type":"subtle","name":"Interview","prompt":"Interviewer asks a second stranger a question based entirely on the first stranger's random answer; confusion builds until the second person naturally notices the product (Erewhon-style aspirational item) and pivots into a casual review."},
  {"id":"d50eb41c-fcfa-4f4d-93aa-473cdc6bc3b2","type":"stunt","name":"Random Object Mic","prompt":"During a casual vlog, a random absurd object falls into the person's hand from above, and they immediately use it as a microphone to continue a completely serious product review."},
  {"id":"8101cd3e-3cc9-4607-a171-3582daa2f6ee","type":"subtle","name":"Product Crash","prompt":"The product itself falls from above and destroyed, creating chaos; harsh sharpness leads to a perfectly clean and restored scene where a person calmly begins reviewing the product."},
  {"id":"31976cc7-e597-4be2-9753-4a80153b0cc7","type":"stunt","name":"Blizzard","prompt":"A cozy indoor scene is suddenly hit by a violent, impossible blizzard; chaos fills the room but the product remains intact and functioning, and once the storm stops, the product is still working."},
  {"id":"2db84ed8-7082-4981-9c9c-9d61b3c28668","type":"subtle","name":"Camera Bump","prompt":"The camera operator accidentally bumps into a person, hitting their forehead; they react briefly, recover, and naturally reveal the dress (or product on it) while transitioning into a casual explanation."},
  {"id":"5443eff1-d940-4ad3-9413-957bb048a6b0","type":"stunt","name":"Product Dodge","prompt":"Suddenly, a product flies into a person's face; he quickly bends down to avoid a collision, and in the next frame he stands up straight and already holds the product in his hands and begins to review as if nothing had happened."},
  {"id":"ec9fdf99-314d-480d-a656-10d9861341e7","type":"subtle","name":"Epic Fail","prompt":"A person performs an unsuccessful backflip, lands unsuccessfully, falls, and immediately, without pause, takes out the product and begins an unflappable review."}
]
// has_more: false, cursor: null — 9 hooks is the complete picklist
```

**Verdict:** **CONFIRMS** content-factory L229 hook list exactly (all 9 names match). **NEW INTEL** (beyond source corpus):
- Each hook has a `type` field classifying it as `stunt` or `subtle` (5 subtle + 4 stunt)
- Each hook has a descriptive `prompt` field with the visual concept — extractable as sub-skill content
- Each hook has `thumbnail_url` + `video_url` for visual preview
- `entity_type: "hook"`, `source: "preset"`

**Correction-candidate flag:** None — confirms content-factory.

---

## Probe 0.2b — Setting picklist

**Call:**
```
show_marketing_studio(action='list', type='setting', size=100)
```

**Response (14 settings, abbreviated to id/name/type/prompt):**
```json
[
  {"id":"b8368076-...","type":"realistic","name":"Bedroom","prompt":"On bed or propped against pillows, soft window light. Unmade bed, cozy textures. Relaxed morning or evening wind-down vibe — honest, low-effort feel."},
  {"id":"b03705e5-...","type":"unrealistic","name":"Airplane Wing","prompt":"Person sits on airplane wing mid-flight at altitude. Casual product review — powerful wind, clouds, engine roar."},
  {"id":"10f47b85-...","type":"realistic","name":"Nature","prompt":"Outdoors — trail, park, beach, or garden depending on product. Natural light, greenery or open sky. Active or peaceful mood — setting adapts to product."},
  {"id":"3cf2164e-...","type":"unrealistic","name":"Roofing","prompt":"Person on the edge of a skyscraper rooftop, city skyline stretched out behind, wind moving through hair, sun catching the buildings. Casual product review with the entire city below, character completely unbothered by the height — selfie camera, golden hour or dusk, urban scale visible in every direction."},
  {"id":"6bfbe372-...","type":"realistic","name":"Gym","prompt":"Gym floor, locker room, or post-workout bench. Bright overhead lighting, equipment in background. Sweaty or freshly finished energy — product tied to performance or recovery."},
  {"id":"e99c2ee8-...","type":"unrealistic","name":"Volcano Rim","prompt":"Person sits on active volcano rim, lava below. Casual product review — lava bubbles, smoke drifts through, zero reaction."},
  {"id":"189fa1ac-...","type":"realistic","name":"Bathroom","prompt":"Mirror selfie or front camera in bathroom. Ring light or vanity lighting, tiles visible. Intimate getting-ready energy — product shown mid-routine, close-up friendly."},
  {"id":"f495493f-...","type":"unrealistic","name":"Tiny Reviewer","prompt":"Person shrunk to 15cm next to a product their full height. Normal selfie review at impossible scale — leans on it."},
  {"id":"a0eb0be9-...","type":"realistic","name":"Kitchen","prompt":"Standing at counter or leaning on island, natural daylight. Clean surface, mug or fruit in background. Casual mid-day energy — product fits daily routine."},
  {"id":"d6992aea-...","type":"unrealistic","name":"Car Roof","prompt":"Person on roof of moving car, desert highway, golden hour. Product review while swaying with the road. Semi truck passes — no flinch."},
  {"id":"fdfa032c-...","type":"realistic","name":"In Car","prompt":"Selfie from passenger or driver seat, parked or cruising. Window light on face. Casual tone — talking to camera between errands."},
  {"id":"8c95f9ba-...","type":"realistic","name":"Street","prompt":"Walking on sidewalk or standing on urban street, handheld selfie. City backdrop — storefronts, traffic, pedestrians. Energetic pace, talking while moving. Spontaneous discovery feel."},
  {"id":"d39dda10-...","type":"realistic","name":"Office","prompt":"Desk setup, laptop open, coffee nearby. Clean modern space, soft overhead or monitor glow. Hushed mid-workday tone — quick product mention squeezed between tasks."},
  {"id":"71f61bb0-...","type":"unrealistic","name":"Train Surf","prompt":"Person hangs outside a moving train, filming selfie. Reviews product — wind pressing on them is the live demo."}
]
// has_more: false, cursor: null — 14 settings is the complete picklist
```

**Verdict:** **CONFIRMS** content-factory L233–L234 setting list exactly. 8 realistic (Bedroom, Bathroom, Kitchen, Office, In Car, Street, Gym, Nature) + 6 unrealistic (Airplane Wing, Roofing, Volcano Rim, Tiny Reviewer, Car Roof, Train Surf). **NEW INTEL:** `type` field confirms realistic/unrealistic classification at the API level; each setting has a descriptive `prompt` field extractable as sub-skill content; thumbnail + video preview URLs.

**Correction-candidate flag:** None — confirms content-factory.

---

## Probe 0.2c — Avatar picklist

**Call:**
```
show_marketing_studio(action='list', type='avatar', size=100)
```

**Response (40 preset avatars, abbreviated to id/name/gender/type):**

| # | Name | Gender | Type |
|---|---|---|---|
| 1 | Jayden | male | preset |
| 2 | Stefan | male | preset |
| 3 | Mei | female | preset |
| 4 | Yuna | female | preset |
| 5 | Adriana | female | preset |
| 6 | Clara | female | preset |
| 7 | Maria | female | preset |
| 8 | Sofia | female | preset |
| 9 | Valentina | female | preset |
| 10 | Jia | female | preset |
| 11 | Lily | female | preset |
| 12 | Tae | male | preset |
| 13 | Felix | male | preset |
| 14 | **Malik** | male | preset |
| 15 | Liam | male | preset |
| 16 | Joon | male | preset |
| 17 | Erik | male | preset |
| 18 | Nia | female | preset |
| 19 | Hana | female | preset |
| 20 | Ryu | male | preset |
| 21 | Priya | female | preset |
| 22 | Elena | female | preset |
| 23 | Kai | male | preset |
| 24 | Sora | female | preset |
| 25 | Minji | female | preset |
| 26 | Margot | female | preset |
| 27 | Niko | male | preset |
| 28 | Jin | male | preset |
| 29 | Yuki | female | preset |
| 30 | Marco | male | preset |
| 31 | Ren | male | preset |
| 32 | Lucas | male | preset |
| 33 | Zara | female | preset |
| 34 | Naomi | female | preset |
| 35 | Megan | female | preset |
| 36 | Omar | male | preset |
| 37 | Miso | female | preset |
| 38 | Scarlett | female | preset |
| 39 | Amara | female | preset |
| 40 | Audrey | female | preset |

Counts: 24 female / 16 male. Multicultural casting (East Asian, South Asian, Black/African, Hispanic/Latin, European/White). `has_more: false` — 40 preset avatars is the complete library.

**Verdict:** **CONFIRMS** "Malik" (used in SRT-2:00:14:00 verbatim demo). **CONTRADICTS** content-factory L612 minor: API returns `type: "preset"` field, NOT `source: "preset"` as content-factory said. Calibration delta only — content-factory's filter recommendation works with field renamed.

**Correction-candidate flag: Correction #9** — minor field-name calibration (`source` → `type`).

---

## Probe 0.3-a — Marketing Studio model discovery

**Call:**
```
models_explore(action='search', query='marketing studio', limit=20)
```

**Response (3 models found):**

### Model 1: `marketing_studio_image`
```json
{
  "id": "marketing_studio_image",
  "name": "Marketing Studio Image",
  "description": "One-click product image ads for social campaigns",
  "output_type": "image",
  "parameters": [
    {"name":"resolution","required":"optional","type":"string","default":"1k","options":["1k","2k","4k"]}
  ],
  "medias": [{"name":"medias","type":"image","roles":["image"]}],
  "aspect_ratios": ["auto","1:1","3:2","2:3","4:3","3:4","4:5","5:4","9:16","16:9","21:9"]
}
```

### Model 2: `ms_image` (display name "DTC Ads")
```json
{
  "id": "ms_image",
  "name": "DTC Ads",
  "description": "DTC ad image generation with brand-kit-aware prompts, avatars, products, and curated ad formats",
  "output_type": "image",
  "parameters": [
    {"name":"style_id","required":"required","type":"string"},
    {"name":"brand_kit_id","required":"optional","type":"string"},
    {"name":"resolution","required":"optional","type":"string","default":"1k","options":["1k","2k","4k"]},
    {"name":"quality","required":"optional","type":"string","default":"low","options":["low","medium","high"]},
    {"name":"batch_size","required":"optional","type":"number","default":1,"min":1,"max":20},
    {"name":"folder_id","required":"optional","type":"string"}
  ],
  "medias": [{"name":"medias","type":"image","max":14,"roles":["image"]}],
  "aspect_ratios": ["1:1","3:2","2:3","16:9","9:16","4:3","3:4","21:9","27:16","16:27","9:8","8:9","4:9","9:4","auto"],
  "tags": ["marketing","ads","product","brand-kit","ad-format","avatar","dtc"]
}
```

### Model 3: `marketing_studio_video` (the main one)
```json
{
  "id": "marketing_studio_video",
  "name": "Marketing Studio",
  "description": "One-click product ads, TikTok/Reels ready",
  "output_type": "video",
  "tags": ["marketing","ugc","ads","tiktok","reels","product","social-media"],
  // Full schema captured under Probe 0.3-b below
}
```

**Verdict:** **CONFIRMS** content-factory's reference to `marketing_studio_video` [CF:L476]. **NEW INTEL:** Marketing Studio is **three models, not one**:
- `marketing_studio_image` — basic product image gen
- `ms_image` (display: "DTC Ads") — full DTC ad image gen with brand kits, ad-format styles, batch generation up to 20
- `marketing_studio_video` — the video model that director.md and content-factory document

The naming surprise: `ms_image` has display name "DTC Ads." This is the "Marketing Studio" image surface internally; per `show_marketing_studio` tool description ("do not say `ms_image` — refer to it as 'DTC Ads'"), the user-facing brand name is DTC Ads, not Marketing Studio Image. Out of scope for v3.7.13 (image-side adjacent), but worth flagging for the cross-surface workflow doc.

**Correction-candidate flag:** None at this probe — three-model discovery is new intel beyond source corpus, not a correction to a wrong claim.

---

## Probe 0.3-b — Full schema for `marketing_studio_video`

**Call:**
```
models_explore(action='get', model_id='marketing_studio_video')
```

**Response (verbatim):**
```json
{
  "id": "marketing_studio_video",
  "name": "Marketing Studio",
  "provider_name": "Higgsfield",
  "description": "One-click product ads, TikTok/Reels ready",
  "output_type": "video",
  "parameters": [
    {"name":"resolution","required":"optional","type":"string","default":"720p","options":["480p","720p","1080p"]},
    {"name":"generate_audio","required":"optional","type":"bool","default":false},
    {"name":"folder_id","required":"optional","type":"string"},
    {"name":"width","required":"optional","type":"number"},
    {"name":"height","required":"optional","type":"number"},
    {"name":"hook_id","required":"optional","type":"string"},
    {"name":"setting_id","required":"optional","type":"string"},
    {"name":"ad_reference_id","required":"optional","type":"string"}
  ],
  "medias": [
    {"name":"avatars","type":"image"},
    {"name":"medias","type":"image","roles":["image","start_image","end_image"]}
  ],
  "aspect_ratios": ["auto","21:9","16:9","4:3","1:1","3:4","9:16"],
  "tags": ["marketing","ugc","ads","tiktok","reels","product","social-media"],
  "duration_range": {"min":4,"max":15}
}
```

**Verdict — multiple findings:**

✅ **CONFIRMS** content-factory:
- `aspect_ratios` list matches L174 exactly (7 values: auto/21:9/16:9/4:3/1:1/3:4/9:16)
- `resolution` options match L175 exactly (480p/720p/1080p); **adds default = 720p**
- `generate_audio` is a declared bool parameter, default false (L176)
- `duration_range` 4–15s matches L171 exactly
- `hook_id` and `setting_id` are declared optional string parameters (L499–L500)

🆕 **NEW INTEL** beyond content-factory:
- `width` and `height` parameters (custom dimensions beyond `aspect_ratio` enum)
- `ad_reference_id` parameter — connects to the `ad_reference` entity type surfaced earlier in show_marketing_studio
- `folder_id` parameter — organizational metadata
- `default: 720p` for resolution (CF didn't specify default)
- `medias` slot accepts roles `image` / `start_image` / `end_image` — frame-role support consistent with other video models
- Tag set: `marketing, ugc, ads, tiktok, reels, product, social-media`

⚠️ **STRUCTURAL CONTRADICTION with content-factory:**
- **The schema has NO `mode` parameter** — content-factory L681–L692 entire slug-mismatch table is premised on `generate_video.mode` being the routing key. **It is not.** `mode` lives on `show_marketing_studio` ("Optional Marketing Studio preset label/slug for next_step video generation"), not on `generate_video`.
- **`avatars` is a separate top-level media slot from `medias`** — content-factory wrote `avatars: [{ id, type: "preset" }]` as part of `params`; schema shows `avatars` and `medias` are two distinct top-level media arrays declared under `medias` schema entry. Call shape is `generate_video(params={...}, avatars=[...], medias=[...])` not `generate_video(params={..., avatars: [...]})`.

**Correction-candidate flags:**
- **Correction #7:** Slug-mismatch table is architecturally wrong. The `mode` parameter is on `show_marketing_studio`, not `generate_video`. The specific claimed mismatches (`ugc_how_to`, `product_showcase`) don't appear in the API at all.
- **Correction #8:** `avatars` is a separate top-level media slot from `medias` — content-factory's call-shape documentation is wrong.

---

## Supplementary probe — `show_marketing_studio.mode` normalization

Free probe to test whether the `mode` parameter on `show_marketing_studio(action='presets')` validates input or accepts arbitrary strings. Tested 5 mode values against `action='presets'`:

| Call | Response |
|---|---|
| `show_marketing_studio(action='presets', mode='Hyper Motion')` | Identical 9-preset list, no `next_step` field, no echo of `mode` |
| `show_marketing_studio(action='presets', mode='hyper_motion')` | Identical 9-preset list, no `next_step` field, no echo of `mode` |
| `show_marketing_studio(action='presets', mode='product_showcase')` | Identical 9-preset list, no `next_step` field, no echo of `mode` |
| `show_marketing_studio(action='presets', mode='Tutorial')` | Identical 9-preset list, no `next_step` field, no echo of `mode` |
| `show_marketing_studio(action='presets', mode='ugc_how_to')` | Identical 9-preset list, no `next_step` field, no echo of `mode` |

**Verdict:** `mode` parameter is silently accepted in all forms — including the content-factory-claimed slugs `product_showcase` and `ugc_how_to` — but the `presets` action doesn't surface a `next_step` or echo the mode back. Mode normalization probably happens in `fetch` / `create` actions (where `next_step` is meaningful per the tool description). Cannot determine canonical mode form from `presets` action alone.

For sub-skill documentation: the safe path is to pass the `slug` value as `mode` on `show_marketing_studio` (`'hyper_motion'`, `'tutorial'`, etc.) since those are the values the API returns and uses internally. The slug-mismatch table from content-factory is refuted regardless of mode-normalization specifics.

**Correction-candidate flag:** Strengthens **Correction #7** (slug-mismatch table refuted) — the specific `ugc_how_to` and `product_showcase` slugs don't trigger any error path either, but they also don't surface as canonical anywhere. They are not real Marketing Studio slugs.

---

## Probe 0.3-spend — DEFERRED (NOT NEEDED)

**Original purpose:** Test whether `generate_video.mode` accepts both title-case ("Hyper Motion") and slug ("hyper_motion") forms, and whether the content-factory-claimed alternative slugs (`product_showcase`, `ugc_how_to`) are accepted.

**Reason for deferral:** The slug-mismatch claim was refuted by:
1. Schema-level evidence (Probe 0.3-b): `marketing_studio_video` has no `mode` parameter at all
2. Picklist enumeration (Probe 0.1): the 9 presets return only the canonical slugs; `ugc_how_to`/`product_showcase` are absent
3. Supplementary probe: `show_marketing_studio.mode` silently accepts any string on `action='presets'` — testing arbitrary modes via spend probes would not produce additional clarifying evidence

Spending ~$5–$9 on a spend probe would not improve the verification picture. The slug-mismatch table is refuted at the schema level.

**Spend saved:** ~450 credits / ~$4.50

---

## Probe 0.4 — DEFERRED (NOT NEEDED FOR SUB-SKILL DISCIPLINE)

**Original purpose:** Test the random-face-fallback claim from content-factory L632–L636 ("leaving `avatars: []` causes Higgsfield to cast a fresh random face per render") by running ≥2 `generate_video` calls with empty avatars and comparing whether the generated face is identical or different.

**Reason for deferral:** Discipline reasoning, not budget reasoning:
1. **User library is empty** — `show_marketing_studio(action='list', type='product')` returned `{items:[], total_count:0}`. Probe would require registering a sample product first (free fetch, but adds setup steps).
2. **Single-generation cannot prove randomness** — verifying "random per render" requires ≥2 generations to compare, doubling the spend to ~$3.
3. **Sub-skill practical guidance does not depend on the random-face specifics.** The schema-level + SRT-3:00:19:00 + tool-description evidence already establishes: (a) `avatars` accepts max 1 entry, (b) types are preset/custom, (c) the UI rejects two avatars with a known workaround. Whether empty arrays produce random faces vs default faces vs rejection is a corner case; the sub-skill's recommendation is "always pass an avatar" regardless.
4. **Discipline over budget.** Approved spend is not a mandate to spend; it's headroom for verifications that close load-bearing questions. This one doesn't.

**Spend saved:** ~150–300 credits / ~$1.50–$3.00

**Sub-skill treatment:** Document the random-face-fallback claim as "source-corpus claim, not directly verified — practical guidance: always pass an avatar from preset or custom library to maintain campaign visual consistency."

---

## Running list of correction #7+ candidates (for CHANGELOG)

Five new corrections surfaced by Phase 0 (added to the 6 carried from §11 of Phase 3.1 knowledge model):

| # | Topic | Source-corpus claim | Live MCP reality | Implication |
|---|---|---|---|---|
| 7 | Slug-mismatch table architecturally wrong | content-factory L681–L692: `generate_video.mode` accepts `ugc_how_to` for Tutorial and `product_showcase` for Hyper Motion; recommends title-case as safe path | `marketing_studio_video` schema has **no `mode` parameter at all**. The `mode` parameter lives on `show_marketing_studio` (preset routing for next_step). Specific slugs `ugc_how_to` and `product_showcase` appear nowhere in the API. | Sub-skill documents preset routing via `show_marketing_studio.mode` flow (fetch/create with mode → next_step → generate_video). content-factory's slug-mismatch gotcha is removed. |
| 8 | `avatars` is a separate top-level media slot | content-factory L630: `avatars: [{ id, type: "preset" }]` as part of generate_video params | Schema declares `avatars` and `medias` as **two distinct top-level media arrays** under the `medias` schema entry. Call shape: `generate_video(params={...}, avatars=[...], medias=[...])`. | Sub-skill documents the actual call shape — two separate arrays, not nested in params. |
| 9 | Avatar `type` field, not `source` | content-factory L612: filter to `source: "preset"` | API returns `type: "preset"` field on each avatar item | Minor field-name calibration — adjust the picklist-filter recommendation. |
| 10 | 5-preset hook/setting family, not 6 | content-factory L193–L194 lists 6 UGC-family presets that get hook+setting: `ugc · tutorial · ugc_unboxing · product_review · ugc_virtual_try_on · virtual_try_on` | `generate_video` tool description: "supported only for presets UGC, Tutorial, Unboxing, Product Review, UGC Virtual Try On" — **5 presets, no `virtual_try_on` (Pro Virtual Try On)** | Sub-skill documents 5-preset family; Pro Virtual Try On does NOT get hook+setting picklist support. |
| 11 | Three Marketing Studio models exist | content-factory only documents `marketing_studio_video` [L476] | Three models: `marketing_studio_video` (video), `marketing_studio_image` (basic image), `ms_image` (display name "DTC Ads" — full DTC ad image gen with brand kits, ad formats, batch up to 20) | Sub-skill scopes to `marketing_studio_video` (the video model). Image-side models flagged in cross-surface-workflow.md as adjacent + deferred. |

**Combined corrections count for CHANGELOG: 11 corrections (6 from §11 + 5 from Phase 0) + 1 calibration note (credit cost rate).**

---

## Updated live picklist snapshots — ready for ingestion into Phase 2 sub-skill content

### 9 video presets (canonical, complete)
| # | mode (display) | slug | description |
|---|---|---|---|
| 1 | UGC | ugc | Realistic social media videos |
| 2 | Tutorial | tutorial | Step-by-step tutorials |
| 3 | Unboxing | ugc_unboxing | High-quality unboxing |
| 4 | Hyper Motion | hyper_motion | Highlight your product |
| 5 | Product Review | product_review | Authentic product reviews |
| 6 | TV Spot | tv_spot | Authentic stories, amplified |
| 7 | Wild Card | wild_card | A unique and creative video mode for custom ideas |
| 8 | UGC Virtual Try On | ugc_virtual_try_on | Try before you buy |
| 9 | Pro Virtual Try On | virtual_try_on | Advanced virtual try-on |

### Hook+setting family (5 presets per `generate_video` tool description)
UGC, Tutorial, Unboxing, Product Review, UGC Virtual Try On.
**Not in family:** Hyper Motion, TV Spot, Wild Card (cinematic secondaries), **Pro Virtual Try On** (per tool description — contradicts content-factory).

### 9 hooks (canonical, complete) — `id` UUIDs available in raw response section above
| Name | Type | Visual concept (short) |
|---|---|---|
| Product Hit | stunt | Object flies into frame, hits subject |
| Spicy | subtle | Close-up collarbone → flawless makeup → selfie → product pitch |
| Interview | subtle | Erewhon-style sidewalk interviewer + stranger discovers product |
| Random Object Mic | stunt | Absurd object falls into hand, used as mic for serious review |
| Product Crash | subtle | Product falls + destroyed → cuts to clean restored review |
| Blizzard | stunt | Cozy indoor scene hit by impossible blizzard, product survives |
| Camera Bump | subtle | Operator bumps into person → recover → product reveal |
| Product Dodge | stunt | Product flies at face → dodge → already-holding-product review |
| Epic Fail | subtle | Failed backflip → recover → unflappable product review |

### 14 settings (canonical, complete)
| Name | Type | Scene (short) |
|---|---|---|
| Bedroom | realistic | On bed, soft window light, cozy textures |
| Bathroom | realistic | Mirror selfie, ring/vanity lighting, intimate getting-ready |
| Kitchen | realistic | Counter, natural daylight, daily-routine fit |
| Office | realistic | Desk, laptop, soft overhead, hushed mid-workday |
| In Car | realistic | Selfie from passenger/driver seat, casual between-errands |
| Street | realistic | Walking sidewalk, urban backdrop, spontaneous discovery |
| Gym | realistic | Locker room/post-workout, bright overhead, performance/recovery |
| Nature | realistic | Trail/park/beach/garden, natural light, active or peaceful |
| Airplane Wing | unrealistic | Person on airplane wing at altitude, wind/clouds/engine |
| Roofing | unrealistic | Skyscraper rooftop edge, city below, golden hour |
| Volcano Rim | unrealistic | Active volcano rim, lava below, zero reaction |
| Tiny Reviewer | unrealistic | Person shrunk to 15cm next to full-height product |
| Car Roof | unrealistic | Person on roof of moving car, desert highway, semi truck passes |
| Train Surf | unrealistic | Person hangs outside moving train, wind as live demo |

### 40 preset avatars (full table in Probe 0.2c above)
24 female / 16 male. Multicultural cast. Notable name confirmed: **Malik** (Adil used in SRT-2:00:14:00 demo verbatim).

### `marketing_studio_video` full parameter spec (from Probe 0.3-b)
- `params` accepts: `resolution` (default 720p, options 480p/720p/1080p), `generate_audio` (bool default false), `folder_id` (string), `width` (number), `height` (number), `hook_id` (string), `setting_id` (string), `ad_reference_id` (string)
- Top-level media slots: `avatars` (image type, max 1 per show_marketing_studio.avatars description) and `medias` (image type, roles: image/start_image/end_image)
- `aspect_ratios`: auto / 21:9 / 16:9 / 4:3 / 1:1 / 3:4 / 9:16
- `duration_range`: 4–15s
- **No `mode` parameter** — preset routing via `show_marketing_studio.mode` flow
- `get_cost: true` NOT supported

---

## Phase 0 Summary Table

| Probe | Action | Cost | Verdict | Correction-flag |
|---|---|---|---|---|
| **Pre-probe schema scan** | Read tool descriptions before any live call | $0 | Surfaced 4 findings (1 contradicts CF — #10 candidate; 3 confirm existing claims) | #10 |
| **0.1** | `show_marketing_studio(action='presets')` | $0 | CONFIRMS 9-preset list + slugs | — |
| **0.2a** | `show_marketing_studio(action='list', type='hook')` | $0 | CONFIRMS 9 hooks; +NEW INTEL (type field, descriptive prompts) | — |
| **0.2b** | `show_marketing_studio(action='list', type='setting')` | $0 | CONFIRMS 14 settings; +NEW INTEL (type field) | — |
| **0.2c** | `show_marketing_studio(action='list', type='avatar')` | $0 | Confirms 40 preset avatars + Malik usage; minor field-name delta (`type` not `source`) | #9 |
| **0.3-a** | `models_explore(action='search', query='marketing studio')` | $0 | NEW INTEL: 3 MS models exist, not 1 | #11 |
| **0.3-b** | `models_explore(action='get', model_id='marketing_studio_video')` | $0 | CONFIRMS duration/aspect/resolution/audio specs; CONTRADICTS slug-mismatch (no `mode` param) + avatars-as-param claim | #7, #8 |
| **Supplementary** | `show_marketing_studio.mode` normalization on `action='presets'` × 5 forms | $0 | Strengthens #7 — slugs `ugc_how_to`/`product_showcase` don't appear anywhere | (strengthens #7) |
| **0.3-spend** | DEFERRED — slug-mismatch already refuted at schema level | $0 (saved ~$5) | NOT NEEDED | — |
| **0.4** | DEFERRED — single-generation can't verify randomness; sub-skill guidance unchanged regardless | $0 (saved ~$3) | NOT NEEDED FOR SHIP | — |

**Total spend:** 0 credits of 2,500-credit ($25) budget. All verification closed via free probes.

**Net correction count for sub-skill + CHANGELOG:** **11 corrections + 1 calibration note** (6 from §11 of Phase 3.1 + 5 new from Phase 0).

**Phase 0 outcome:** Sub-skill content substrate is now anchored on live API truth. Every API claim in the sub-skill will cite either a Phase 0 probe verdict or a `[CF:Lxxx]` source-corpus reference where they agree. Where they disagree, this log is the authoritative source.
