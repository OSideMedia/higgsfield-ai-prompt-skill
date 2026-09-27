---
name: higgsfield-repurpose
description: "Use when the user already has a FINISHED video and wants Higgsfield to repurpose, restyle, clip or analyze it: Shorts Studio (restyle one 4–120s source video into a set of short-form clips from a style preset), Clipify (turn one YouTube video into subtitled clips), Virality Predictor (predict virality, hook strength, attention, retention risk with a dashboard), or Video Analysis (scene-by-scene breakdown of an uploaded video or a YouTube link). Also use when the user asks which of these cost credits and which are free, 'turn my video into shorts', 'will this go viral', 'score my ad', 'break this video down scene by scene'. Names: shorts_studio_create, shorts_studio_create_preset, shorts_studio_list_presets, shorts_studio_status, clipify, virality_predictor, brain_activity, video_analysis_create, video_analysis_status."
user-invocable: true
metadata:
  tags: [higgsfield, repurpose, post-production, shorts-studio, clipify, virality-predictor, video-analysis, short-form, reels, youtube, analysis]
  version: 1.0.0
  updated: 2026-09-26
  parent: higgsfield
---

# Higgsfield Repurpose — Shorts, Clips, and Analysis of Finished Video

## QUICK FACTS
*Routing aids — read the linked sections for the full rules. Nothing in this sub-skill is field-tested.*
- Four surfaces take a video that already exists: Shorts Studio (restyle → shorts), Clipify (YouTube → subtitled clips), Virality Predictor (a score), Video Analysis (a scene breakdown) [→](#what-this-sub-skill-is-for)
- Paid vs free is per tool — `shorts_studio_create` is **PAID**; its `get_cost` estimate and preset creation state they are free; list / status calls state no cost [→](#paid-or-free-read-this-before-calling-anything)
- Shorts Studio: source 4–120s, output **720p only**, 9:16 default (16:9 optional); preflight with `get_cost: true` + `duration_seconds` — no preset or upload needed for the estimate [→](#shorts-studio)
- Shorts Studio presets store a STYLE (≤10 media, videos ≤30s, public https URLs) — write the preset prompt as laws, not adjectives [→](#style-presets-free)
- Clipify: exactly ONE YouTube URL per job; 1–20 clips; 9:16 / 1:1 / 16:9; subtitle font, case, position and highlight colour are parameters [→](#clipify)
- Virality Predictor: input is a confirmed uploaded video or a completed generated video; it is a PREDICTION — compare variants with it, don't treat it as audience data [→](#virality-predictor)
- Video Analysis: exactly one of uploaded video / YouTube URL; ~3–5 min; **warn up front: the longer the video, the less accurate the breakdown** [→](#video-analysis)
- Burned-in captions, cuts, soundtrack, voice swaps are other surfaces — hand-off map [→](#where-the-neighbouring-jobs-live)

---

## What this sub-skill is for

Every surface here starts from a **video that already exists** — a finished ad, a long
YouTube video, a generated clip — and produces something derived from it: restyled
shorts, cut-down clips, a performance prediction, or a scene list. None of them writes a
generation prompt from scratch; that is the rest of this library.

| Surface | Input | Output | Tool / model |
|---|---|---|---|
| **Shorts Studio** | One uploaded video, 4–120s + a style preset | A set of AI-restyled short-form clips | `shorts_studio_*` (MCP) |
| **Clipify** | One YouTube URL | Ready-to-share clips with subtitles | `clipify` (video catalog model) |
| **Virality Predictor** | An uploaded or generated video | Virality / engagement / attention / hook / retention-risk prediction + dashboard | `virality_predictor` (MCP) |
| **Video Analysis** | An uploaded video or a YouTube URL | Scene-by-scene analysis | `video_analysis_*` (MCP) |

**Not this sub-skill:** changing what is *inside* a clip (swap an object, re-light, extend
it) — that is `../higgsfield-seedance-2-5/SKILL.md` (video_edit / video_extension),
`../higgsfield-seedance-vfx/SKILL.md`, or Genjutsu (`../higgsfield-marketing-studio/SKILL.md`
§ 14). Many edited versions of one ad → Ad Multiplier, same § 14.

---

## Paid or free — read this before calling anything

`[OFFICIAL — Higgsfield MCP tool schema, 2026-09-26]` unless marked.

| Tool | Spends credits? | Evidence |
|---|---|---|
| `shorts_studio_create` | **PAID** — "reserves credits" | Tool description |
| `shorts_studio_create` with `get_cost: true` + `duration_seconds` | **Free** — "estimate the credit cost without submitting a job"; no preset or source video needed | Tool description |
| `shorts_studio_create_preset` | **Free** — "just stores a STYLE — no generation, no credits" | Tool description |
| `shorts_studio_list_presets` · `shorts_studio_list_sessions` · `shorts_studio_status` | **Not stated** — list / status calls that submit nothing; not called free here | Tool descriptions (silent on cost) |
| `clipify` | **Not stated.** It is a video-catalog model, so it runs through `generate_video` / the CLI and can be preflighted with `get_cost: true` (MCP) or `higgsfield generate cost clipify …` (CLI — confirm the flag form with `higgsfield model get clipify` first) | `[OFFICIAL — platform, 2026-09-26]` snapshot has no price field |
| `virality_predictor` | **Not stated**, and the tool has no `get_cost` field | Tool schema |
| `video_analysis_create` | **Not stated**, and the tool has no `get_cost` field | Tool schema |
| `video_analysis_status` · `video_analysis_jobs` | **Not stated** — status / list calls that submit nothing; not called free here | Tool descriptions (silent on cost) |

**Where the schema is silent, do not call it free.** Check the balance before and after
(`balance` / `transactions` on MCP, `higgsfield account status` on the CLI) the first time
a surface is used, and record what it actually cost. No prices appear in this file because
none were measured.

---

## Shorts Studio

`[OFFICIAL — Higgsfield MCP tool schema, shorts_studio_*, 2026-09-26]`

> "Start a Shorts Studio short: restyle one uploaded source video (4s–120s) into a set of
> AI-generated short-form clips using a style preset. PAID — reserves credits."

| Param | Values | Notes |
|---|---|---|
| `source_video_id` | uuid | The uploaded video's `video_input` id (`media_upload_widget`, type=video). Required unless `get_cost` |
| `preset_id` | uuid | From `shorts_studio_list_presets` or `shorts_studio_create_preset`. Required unless `get_cost` |
| `preset_source` | `user` · `cms` | The preset item's own `preset_source`. Required unless `get_cost` |
| `aspect_ratio` | `9:16` (default) · `16:9` | Output orientation |
| `resolution` | `720p` | **The only value** — the schema pins it as a constant |
| `get_cost` | bool | With `duration_seconds`, returns the estimate and submits nothing |
| `duration_seconds` | > 0, ≤ 120 | Source length; required when `get_cost` is true |

**The run, in order:**

1. **Estimate first** — `get_cost: true` + `duration_seconds` (free; no preset, no upload).
2. **Pick or make a style** — `shorts_studio_list_presets` returns the user's own presets
   first, then the CMS library (paginated via `next_cursor`); or make one (below).
3. **Upload the source** — the user uploads through `media_upload_widget` (type=video);
   the tool asks for an upload before it is called, never a chat attachment.
4. **Create** — PAID. Returns a session with **empty** `job_ids`.
5. **Poll** `shorts_studio_status` until clips appear. `status='completed'` means every
   clip job is *terminal*, **not necessarily successful** — check each clip.

> **Schema mismatch to know about:** `shorts_studio_status` says to poll each clip's
> `job_id` "via job_status", but no `job_status` tool is in the connector's 2026-09-26 tool
> list — the listed job tools are `jobs_wait`, `job_display` and `show_generation_by_ids`.
> Which one the status tool means is unverified.

**Not published:** how many clips a session produces, how long each is, and what the
restyle keeps from the source (timing, audio, framing). Look at one real session before
promising any of them.

### Style presets (free)

`shorts_studio_create_preset` stores a style from reference media — no generation, no
credits.

- **Limits:** ≤ 10 media total; each video ≤ 30s (send `duration` so the cap applies);
  every media item a **public https URL** (use an uploaded media's URL, or
  `media_import_url` first).
- **Fields:** `name` (required), `prompt` (optional style direction), `image_medias`,
  `video_medias`, `thumbnail`.
- **Naming:** Higgsfield's own tool instruction is to give an unnamed preset a random
  friendly two-word name rather than ask — follow it.
- **What this library adds** `[INFERENCE — untested]`: a style preset is a *saved style
  block*, the same job as Cinema Studio's Manual Style — so write its `prompt` the same
  way: **laws, not descriptions** (grade behaviour, lighting law, texture, camera register),
  no vague labels, no director name-drops. See `../higgsfield-cinema/SKILL.md` § Manual
  Style — Authoring Guide.

---

## Clipify

`[OFFICIAL — platform, 2026-09-26]` — model `clipify`, "Turn one YouTube video into
ready-to-share clips with subtitles" (video catalog, `../../specs/models_explore_snapshot_2026-09-26.json`).

| Param | Values | Default |
|---|---|---|
| `urls` | YouTube URL array — "Provide **exactly one** URL; submit one Clipify job per source video" | required |
| `clips_num` | 1–20 | 10 |
| `clip_aspect` | `9:16` · `1:1` · `16:9` | `9:16` |
| `subtitle_font` | `notosans` · `notoserif` · `notosansdisplay` · `ibmplexsans` · `mplusrounded1c` · `bebasneue` · `archivoblack` · `unbounded` · `inter` · `montserrat` · `bangers` · `permanentmarker` · `playfairdisplay` · `caveat` | `notosans` |
| `subtitle_case` | `upper` · `lower` · `as-is` | `as-is` |
| `subtitle_position` | `bottom` · `center` · `top` | `bottom` |
| `subtitle_highlight_hex` | `#RRGGBB` | `#FFE84D` |
| `track_face_crop` | bool — "Track faces when cropping clips" | true |
| `max_height` | 144–2160 — "Maximum source processing height" | 1080 |
| `segment_seconds` | 2–60 — "Segment duration in seconds" | 10 |

**Clipify vs Shorts Studio.** Clipify **cuts** one YouTube video into subtitled clips; it
has no style or restyle parameter. Shorts Studio **restyles** one uploaded video into
AI-generated clips from a preset. Long talk / podcast / tutorial → clips: Clipify. A
short piece whose look should change: Shorts Studio.

The source is fetched from YouTube — clip only videos the user owns or has the rights to.
What `segment_seconds` controls beyond its one-line description is not documented.

---

## Virality Predictor

`[OFFICIAL — Higgsfield MCP tool schema, virality_predictor, 2026-09-26]`

> "predicts a video's virality potential, engagement, attention, audience response,
> retention risk, hook strength, and creative performance with an interactive dashboard."

- `action: "create"` with `params.medias: [{role: "video", id: <uuid>}]` — the id is a
  **confirmed uploaded video `media_id`** or a **completed generated video `job_id`**;
  `params.model` is the constant `"virality_predictor"`.
- `action: "preview"` with `params.job_id` re-opens an existing dashboard.
- **CLI face:** Higgsfield's own skills repo says its Virality Predictor path "Uses
  Virality Predictor (`brain_activity`) with `--video`" `[OFFICIAL — Higgsfield skills repo
  README, v0.12.0]`; CLI 1.1.23 `model get brain_activity` shows a text-output model named
  "Brain Activity" that requires `medias`. That the two are the same product rests on that
  README line — not verified here.

**How this library uses it** `[INFERENCE — untested]`:

- **It is a prediction, not audience data.** This repo has never compared its scores with
  real performance. Report it as "the predictor says", never as "this will go viral".
- **Compare variants, don't chase a number.** The useful question is relative: hook A vs
  hook B on the *same* ad, cut 1 vs cut 2. Rewriting a creative only to move one score is
  optimizing the instrument.
- Natural pairings: hook variants from `../higgsfield-marketing-studio/SKILL.md`, Ad
  Multiplier versions (same skill, § 14), campaign batches in
  `../higgsfield-content-factory/SKILL.md`.

---

## Video Analysis

`[OFFICIAL — Higgsfield MCP tool schema, video_analysis_*, 2026-09-26]`

- **Input — exactly one of:** `video_input_id` (an uploaded video's media id) **or**
  `youtube_url` (https on `youtube.com`, `www.youtube.com`, `m.youtube.com` or `youtu.be`
  only).
- **Queued:** returns `status='queued'`; poll `video_analysis_status` every 30–60 seconds
  until `completed` (scenes populated) or `failed` (`fail_reason` populated). "Processing
  typically takes 3-5 minutes on average." Past jobs: `video_analysis_jobs`.
- **The warning the tool requires, verbatim:** *"warn the user up front that the longer
  the video, the less accurate the scene-by-scene analysis becomes — short clips give the
  most reliable results."* Say it **before** submitting, every time.
- Practical consequence: trim to the sequence you actually care about before uploading.

**Uses in this repo** `[HYPOTHESIS — UNMEASURED]`:

- **Reference breakdown** — a short reference sequence → a scene list to seed
  `../higgsfield-shotlist-director/SKILL.md` or to audit with
  `../higgsfield-scene-engine/SKILL.md`. Analyze a reference for its *structure*; the
  shotlist still gets written, not copied.
- **Cut check** — did a generated multi-shot clip actually cut where the prompt declared
  ("strictly N shots")? The analysis is a second pair of eyes, not a verdict.
- The output's shape beyond "scenes" is not documented. Treat what comes back as notes to
  verify against the video, never as ground truth.

---

## Where the neighbouring jobs live

| The user wants | Surface | Where it is covered |
|---|---|---|
| Captions burned into the pixels | Higgsfield's `subtitles` workflow | `../higgsfield-stack/SKILL.md` § Higgsfield's bundled workflows |
| Cuts, trims, soundtrack, layouts, animated text, title cards on footage | Higgsfield's `video-editing` workflow (Higgsedit) | same |
| The same video at another aspect ratio | `reframe` (MCP tool; also a CLI workflow — verify params with `higgsfield workflow get reframe --json`) | — |
| A different voice on the same video | `voice_change` | `../higgsfield-audio/SKILL.md` § Voice change and voice cloning |
| One object swapped, or motion transferred | Genjutsu | `../higgsfield-marketing-studio/SKILL.md` § 14 |
| Many independently edited versions of one ad | Ad Multiplier | same |

---

## Provenance

- Shorts Studio, Virality Predictor, Video Analysis: `[OFFICIAL — Higgsfield MCP tool
  schema, 2026-09-26]` — read from the connector's tool definitions; no tool was called.
- Clipify: `[OFFICIAL — platform, 2026-09-26]` — the video `models_explore` snapshot.
- `brain_activity`: CLI 1.1.23 `model get` (a free schema read) plus Higgsfield's skills
  repo README v0.12.0.
- Nothing here has been run; costs, clip counts, clip lengths and the accuracy of any
  analysis are unmeasured.

## Related skills

- `../higgsfield-stack/SKILL.md` — execution surfaces, preflight, Higgsfield's bundled workflows
- `../higgsfield-audio/SKILL.md` — voice change and cloned voices
- `../higgsfield-marketing-studio/SKILL.md` — ad creative, Ad Multiplier, Genjutsu
- `../higgsfield-content-factory/SKILL.md` — campaign batches that virality scores can rank
- `../higgsfield-shotlist-director/SKILL.md` · `../higgsfield-scene-engine/SKILL.md` — where a scene breakdown goes next
