---
name: higgsfield-marketing-studio
description: "Use when the user mentions Marketing Studio, DTC Ads, ad video, UGC video, the marketing_studio_video MCP model, or wants to generate one of the 9 Marketing Studio ad presets (UGC, Tutorial, Unboxing, Hyper Motion, Product Review, TV Spot, Wild Card, UGC Virtual Try On, Pro Virtual Try On). Also triggers on hook+setting picklist questions, preset-avatar / custom-avatar / text-generated-avatar handling, 4–15s ad video questions, or any reference to Higgsfield's ad-video product surface. Also use for Ad Multiplier (`ad_multiplier` — 'multiply my ad', many independently edited versions of one supplied 4–30s ad) and for Genjutsu one-off edits of a finished ad (swap one object / product / garment → `hf_mult_replace_object`; transfer motion → `hf_mult_motion_control`)."
user-invocable: true
metadata:
  tags: [higgsfield, marketing-studio, dtc-ads, marketing, ugc, ad, video, preset, hook, setting, avatar, ad-multiplier, genjutsu]
  version: 1.1.0
  updated: 2026-09-26
  parent: higgsfield
---

# Higgsfield Marketing Studio

## QUICK FACTS
*Generated-checked block (scripts/build_index.py verifies anchors). Read the linked sections for full context — these lines are routing aids, not the rules themselves.*
- Hard duration cap: 4–15s per clip; out-of-range values get clamped; longer narrative = multi-clip sequence edited externally [→](#7-generation-parameters)
- 9 presets: UGC, Tutorial, Unboxing (`ugc_unboxing`), Hyper Motion, Product Review, TV Spot, Wild Card, UGC Virtual Try On, Pro Virtual Try On [→](#3-the-9-presets)
- Pro Virtual Try On slug is `virtual_try_on`, NOT `pro_virtual_try_on` [→](#slug-naming-is-canonical-routing-mode-lives-on-a-different-mcp-call)
- Preset routing happens via `show_marketing_studio.mode` — `generate_video` has NO `mode` parameter at all [→](#slug-naming-is-canonical-routing-mode-lives-on-a-different-mcp-call)
- Hook + setting picklists on FIVE presets only: UGC, Tutorial, Unboxing, Product Review, UGC Virtual Try On (NOT Pro Virtual Try On) [→](#4-hook--setting-picklists)
- 9 hooks (4 stunt / 5 subtle) as of 2026-05-18 — picklists drift; enumerate live for current UUIDs [→](#hooks-9-entries-as-of-2026-05-18--visual-scene-templates-not-verbal-copy)
- 14 settings (8 realistic / 6 unrealistic) as of 2026-05-18, passed by UUID as `setting_id` [→](#settings-14-entries-as-of-2026-05-18--environment-templates)
- `avatars` array MUST contain exactly one entry; empty `avatars: []` substitutes a random face per render — always pass one [→](#avatar-field-constraints--consolidated)
- Two-person scenes: primary in `avatars`, secondary as a reference image in `medias` [→](#avatar-field-constraints--consolidated)
- `avatars` and `medias` are top-level siblings of `params` — NOT nested under `params`; wrong nesting rejects [→](#avatars-is-a-separate-top-level-media-slot--not-a-nested-parameter)
- `prompt` is optional; `aspect_ratio` enum: auto/21:9/16:9/4:3/1:1/3:4/9:16; `resolution`: 480p/720p/1080p (default 720p) [→](#7-generation-parameters)
- `get_cost` for MS: the 2026-05 schema said unsupported; the 2026-09-26 `generate_video` schema no longer states that exception — untested either way, so try `get_cost: true` and keep `transactions(limit=200)` as the post-hoc check [→](#what-is-not-in-the-schema)
- **Ad Multiplier** (`ad_multiplier`, "powered by Seedance 2.5"): many independently edited versions of ONE supplied 4–30s ad; same four modes as Seedance 2.5 incl. 1080p; Higgsfield's connector loads its `ad-multiplier` workflow FIRST [→](#14-ad-multiplier-and-genjutsu--editing-a-finished-ad)
- One object swapped in one clip is **Genjutsu** (`hf_mult_replace_object`), not Ad Multiplier [→](#genjutsu--one-edit-one-clip)
- Three MS models exist: `marketing_studio_video` (this skill), `marketing_studio_image`, `ms_image` — call `ms_image` "DTC Ads" with users [→](#three-marketing-studio-models-exist--this-sub-skill-covers-the-video-one)
- Three avatar types: preset (~40 in library), uploaded, text-generated [→](#three-avatar-types)
- Cannot do: >15s clips, non-human lip-sync, multi-character dialogue, multi-setting single output, free-form hook/setting IDs, >1 avatar [→](#9-what-marketing-studio-cannot-do)

Marketing Studio is Higgsfield's opinionated short-form ad-video product. Generations are bounded by a 4–15 second per-clip cap [Phase 0: Probe 0.3-b], routed through one of nine named presets that dictate camera language, register, and the available picklist of hooks and settings. It's distinct from Higgsfield's general video models (Soul, Seedance, Cinema Studio) — those let you write whatever you want; Marketing Studio enforces ad-format conventions per preset and ships with a built-in library of preset hooks, settings, and avatars.

This sub-skill covers Marketing Studio video. The two image-side Marketing Studio surfaces (`marketing_studio_image` and `ms_image` / "DTC Ads") are named in §2 but not covered here.

---

## 1. What Marketing Studio is

Marketing Studio is a routing layer on top of `generate_video` for short-form ad creative. You provide a product image (required) plus optional avatar, location, and additional-asset references. You pick one of nine presets. You optionally write a prompt. Marketing Studio handles the rest — camera language, pacing, hook execution, setting context — per the preset's built-in conventions.

When Marketing Studio isn't the right tool:

- If your video needs to run longer than 15 seconds — Cinema Studio (`higgsfield-cinema`) covers narrative length
- If you need character-consistent multi-shot video with lip-sync — Marketing Studio is not built for it; see `../../model-guide.md` for model selection
- If you want free-form video without ad framing — Seedance (`higgsfield-seedance`), Soul (`higgsfield-soul`), or Cinema Studio give you the open canvas Marketing Studio's preset routing closes off

---

## 2. Two access surfaces — and three MS models

You reach Marketing Studio two ways:

| Surface | How you reach it | What it exposes |
|---|---|---|
| Web UI at `higgsfield.ai` | Browser, direct | Per-generation controls for preset / aspect ratio / quality / duration / hook / setting / avatar / additional asset [SRT-3:00:09:00–00:10:00]. In-app custom avatar generation by text prompt [SRT-3:00:13:00]. In-app product registration by URL scan [SRT-2:00:08:50] |
| MCP via `mcp.higgsfield.ai/mcp` | Custom connector in Claude / Cowork / agent | `show_marketing_studio` for entity management (presets, hooks, settings, avatars, products, brand kits) + `generate_video` with `model: "marketing_studio_video"` for the actual render |

Both surfaces share the same preset / hook / setting / avatar taxonomy. The web UI is what's demonstrated in SRT-2 and SRT-3; the MCP is the programmatic route.

### Three Marketing Studio models exist — this sub-skill covers the video one

[Phase 0: Probe 0.3-a] surfaced that "Marketing Studio" is three models, not one — source-corpus reconciliation #11:

| Model ID | Display name | Output | Scope in v3.7.13 |
|---|---|---|---|
| `marketing_studio_video` | Marketing Studio | video | **This sub-skill** — 9 ad presets, 4–15s, hook + setting + avatar handling |
| `marketing_studio_image` | Marketing Studio Image | image | Basic product image ads — `resolution` param only (1k/2k/4k), 11 aspect ratios. Out of scope |
| `ms_image` | DTC Ads | image | Full DTC ad image generation — brand-kit-aware, ad-format styles, batch up to 20, max 14 reference media. Out of scope for this sub-skill |

> **Naming note** [from `show_marketing_studio` MCP tool description]: when discussing `ms_image` with the user, refer to it as "DTC Ads" — that's the user-facing brand name. The model ID `ms_image` is internal nomenclature.

This sub-skill scopes to `marketing_studio_video`. References to "Marketing Studio" below mean the video model unless the surrounding text says otherwise.

---

## 3. The 9 presets

The nine presets are the routing layer. Pick one, and Marketing Studio applies its built-in production rules.

| # | Display name | Slug | Hook + setting picklist? | What it's for |
|---|---|---|---|---|
| 1 | UGC | `ugc` | Yes | Realistic single-take social videos with a person + product [Phase 0: Probe 0.1] |
| 2 | Tutorial | `tutorial` | Yes | Step-by-step how-to / recipe [Phase 0: Probe 0.1] |
| 3 | Unboxing | `ugc_unboxing` | Yes | High-quality unboxing reveal from packaging |
| 4 | Hyper Motion | `hyper_motion` | **No** | — |
| 5 | Product Review | `product_review` | Yes | — |
| 6 | TV Spot | `tv_spot` | **No** | Cinematic narrative spots in polished commercial register |
| 7 | Wild Card | `wild_card` | **No** | Surreal one-shot creative concepts |
| 8 | UGC Virtual Try On | `ugc_virtual_try_on` | Yes | Try-before-buy, casual register |
| 9 | Pro Virtual Try On | `virtual_try_on` | **No** [Phase 0: pre-probe finding — see §4] | Editorial / lookbook-style virtual try-on |

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

> Picklist contents drift over time. The Phase 0 snapshot at the v3.7.13 Phase 0 probes notes (internal build notes) is correct as of 2026-05-18; for canonical current data, run the live enumeration calls below.

### Hooks (9 entries as of 2026-05-18) — visual scene templates, not verbal copy

```
show_marketing_studio(action='list', type='hook', size=100)
```

[Phase 0: Probe 0.2a] returned 9 hooks, classified by `type` field as either `stunt` (4) or `subtle` (5):

- **Stunt:** Product Hit, Random Object Mic, Blizzard, Product Dodge
- **Subtle:** Spicy, Interview, Product Crash, Camera Bump, Epic Fail

Each hook ships with a descriptive `prompt` field that explains the visual concept.

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
- **`get_cost: true` support — unresolved.** At Phase 0 (2026-05) the `generate_video.params.get_cost` MCP description said Marketing Studio models do not support preflight cost estimation. The **2026-09-26** `generate_video` schema no longer carries that exception — its `get_cost` field reads only "return the cost in credits for this generation without submitting any job" `[OFFICIAL — Higgsfield MCP tool schema, 2026-09-26]`. An absent caveat is not proof the preflight now works for `marketing_studio_video`, and it has not been tried. Try `get_cost: true` first; keep post-hoc verification via `transactions(limit=200)` (§12) as the check.
- **No multi-character avatar slot.** One avatar max — see §5 for the reference-image workaround.

---

## 8. Output prompt style — flowing OR sectioned (NOT a hard rule)

*[Third-party example material withdrawn — see `THIRD_PARTY_NOTICES.md`.]*

---

## 9. What Marketing Studio cannot do

Six things Marketing Studio is not designed for. Trying to force these typically produces broken output:

1. **Clips longer than 15 seconds.** Hard cap at the API level [Phase 0: Probe 0.3-b]. For longer narrative, design as a 2-clip or 5-clip sequence (each clip ≤15s) and edit externally.
2. **Lip-synced dialogue from non-human characters.** Talking fruit, talking products, etc. — the model doesn't reliably sync audio to non-face geometry.
3. **Multi-character coordinated dialogue with consistent identities across cuts.** The one-avatar API limit (§5) prevents this; even with the reference-image workaround, identity drift across multiple generations is high.
4. **Single output with multiple settings, split-screen, or day-X-vs-day-Y diary structure.** One setting per generation. For multi-setting narrative, split into separate clips per the multi-clip pattern.
5. **Free-form `hook_id` or `setting_id` not in the picklist.** Picklists are closed — you can only pass UUIDs returned by `show_marketing_studio(action='list', type='hook'|'setting')`. To skip the hook, omit `hook_id`.
6. **More than one avatar per generation.** One avatar slot, enforced. Workaround: primary in `avatars`, secondary as reference image in `medias` (§5).

### Escape-hatch models for what MS can't render

*[Third-party example material withdrawn — see `THIRD_PARTY_NOTICES.md`.]*

---

## 10. Worked examples — production reference library

The eight worked prompts that used to sit here were third-party production prompts. They were
withdrawn in November 2026 — see `THIRD_PARTY_NOTICES.md` at the repository root.

---

## 11. Cross-surface workflow context

The companion `cross-surface-workflow.md` documented a campaign workflow adapted from third-party
videos and example prompts. It has been withdrawn — see `THIRD_PARTY_NOTICES.md` at the repository root.

---

## 12. Pricing characteristics

Marketing Studio pricing is plan-dependent. At Phase 0 (2026-05) `get_cost: true` was explicitly unsupported for Marketing Studio models [Phase 0: pre-probe finding from `generate_video.params.get_cost` description]; the 2026-09-26 schema no longer states that exception, and nobody has tried it since (§7 → What is NOT in the schema). Until a preflight is seen to work for `marketing_studio_video`, verify spend post-hoc.

*[Third-party example material withdrawn — see `THIRD_PARTY_NOTICES.md`.]*

### Post-hoc verification

```
transactions(limit=200)
```

Pull recent transaction history after a campaign run. Filter by date range to isolate the campaign's actual spend. Sum credits per preset / per model. Even if a `get_cost` preflight turns out to work for MS, this is the only way to know what a campaign *actually* cost — an estimate is not a measurement.

For broader preflight discipline on non-MS models (Kling, Seedance, etc.), see `../higgsfield-stack/SKILL.md` § Preflight discipline.

---

## 13. Source acknowledgment

The withdrawn parts of this sub-skill — the per-preset creative direction, the worked prompts and the
companion workflow — were adapted from skill files, example prompts and videos by Adil Aliyev. What
remains are API facts read from the live MCP surface (`Phase 0` marks) and short observations of the
web UI cited to his published videos (`SRT-n` marks), with a few corrections of claims in his
`higgsfield-content-factory.md` skill file, cited by line (`content-factory L…`). The credit is
recorded here and in
`THIRD_PARTY_NOTICES.md` at the repository root; a credit is not a claim of permission to redistribute
that material.

### Verification pass

Per the v3.7.11 plausibility-over-verification discipline applied recursively to source material — every API claim in this sub-skill cites a Phase 0 live MCP probe verdict; every behavioral claim cites an SRT timestamp. Full verification trail at the v3.7.13 Phase 0 probes notes (internal build notes).

Twelve source-corpus reconciliations applied during translation (5 API-architecture / 4 capability / 2 calibration / 1 cross-surface), grouped and explained in the v3.7.13 CHANGELOG entry. Adil is credited as source throughout; the reconciliations are documentation of source-material truth at translation time, not critique of the source.

---

## 14. Ad Multiplier and Genjutsu — editing a finished ad

**Provenance differs from §§1–13:** this section is not from the Phase 0 probes or Adil's
corpus. It comes from the 2026-09-26 video catalog snapshot `[OFFICIAL — platform,
2026-09-26]` and the Higgsfield connector's own routing text `[OFFICIAL — Higgsfield MCP
server instructions / tool schema, 2026-09-26]`. Nothing here has been fired.

### Ad Multiplier — many versions of one ad

**Model `ad_multiplier`** — "Ad Multiplier video generation powered by Seedance 2.5". Its
parameter surface in the snapshot is the same as `seedance_2_5`'s:

| Param | Values | Default |
|---|---|---|
| `mode` | `t2v` · `omni_reference` · `video_edit` (edits one reference video, billed by that video's duration; `duration` and `aspect_ratio` ignored) · `video_extension` (`aspect_ratio` ignored) | `t2v` |
| `duration` | 4–30s | 5 |
| `resolution` | `480p` · `720p` · `1080p` | `720p` |
| `extension_mode` | `forward` · `backward` — required for `video_extension`, not allowed otherwise | — |
| `generate_audio` | bool | true |
| `bitrate_mode` | `standard` · `high` | `standard` |
| aspect ratios | `auto` · `21:9` · `16:9` · `4:3` · `1:1` · `3:4` · `9:16` | — |
| media roles | `start_image` · `end_image` · `image_references` · `video_references` · `audio_references` | — |

Because `ad_multiplier` is in `../../specs/model-specs.json`, a settings header can be
enum-checked before spending: `python3 scripts/seedance_lint.py --model ad_multiplier
--mode video_edit --resolution 1080p "<prompt>"` (a `4k` there FAILs).

- **Higgsfield routes this through its own workflow first.** The connector's instruction:
  load workflow `ad-multiplier` "when the user asks to 'multiply my video', 'multiply my
  ad', create multiple independently edited versions of one supplied 4-30 second video, or
  regenerate the same ad with different people or products. **Load this workflow before
  Marketing Studio, model browsing, or direct generation.**" The workflow (v1.4) covers
  replacing / adding / removing people, products, objects, clothing, backgrounds and
  targeted on-screen text while preserving motion, framing, cuts, timing, aspect and
  audio — and says it is **not** for simple video edits.
- **What this library adds, and what it hands off.** Hand off the orchestration — the
  `ad-multiplier` workflow owns the multi-version run (`../higgsfield-stack/SKILL.md`
  § Coexistence rules for Higgsfield's workflows). This library adds the per-version edit
  text, written in the Seedance 2.5 `video_edit` grammar — what to preserve, what to change
  (`../higgsfield-seedance-2-5/SKILL.md`) — and a version plan that changes **one variable
  per version** (person, product, background, on-screen line) so the versions can be
  compared; `../higgsfield-repurpose/SKILL.md` § Virality Predictor can then rank them.

### Genjutsu — one edit, one clip

**One object swapped in one clip — the tie-break:** a swap driven by a **reference image of the new object** (a product shot) → Genjutsu `hf_mult_replace_object`, the connector's own route for a single swap; a scoped change **described in words only** (no reference image of the replacement — relight, remove, recolour, change BGM or language) → Seedance 2.5 `video_edit`. Neither lane is field-rated. (`../../model-guide.md` § Edit-Lane Chooser)

- **Two catalog models, both named "Genjutsu"** (Higgsfield): `hf_mult_replace_object` —
  "Replace objects in a source video using reference images"; `hf_mult_motion_control` —
  "Transfer motion from a reference video to subjects in reference images". Each exposes
  only `resolution` (`480p` · `720p` · `1080p`, default `720p`); the edit is specified by
  the reference media.
- **The connector's routing, verbatim:** "Higgsfield Genjutsu routes through
  generate_video: motion transfer -> hf_mult_motion_control; object replacement ->
  hf_mult_replace_object; **never legacy motion_control or ad-multiplier for one Genjutsu
  edit**." And from `generate_video`: "reserve ad-multiplier for explicitly requested
  independent variants."
- **The split:** one object / product / garment / character swapped in one clip →
  `hf_mult_replace_object`. Many independent versions of the ad → Ad Multiplier.
- **Role-name mismatch:** `generate_video` says to pass images with role `image` and
  exactly one source or driving video with role `video`; the snapshot lists the roles as
  `image_references` / `video_references`. The server "may auto-coerce when unambiguous" —
  check `models_explore` for the model before trusting either spelling.
- The snapshot lists no prompt-related parameter for either Genjutsu model; whether a
  prompt is read at all is not stated.
