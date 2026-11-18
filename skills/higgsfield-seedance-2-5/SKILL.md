---
name: higgsfield-seedance-2-5
description: "Seedance 2.5 prompt director — the omni-reference dialect. Routes the four generation modes (t2v / omni_reference / video_edit / video_extension), writes explicit @Image/@Video/@Audio reference roles with exclusions, stages 30-second videos into end-state beats, and covers video editing, forward/backward extension, first-last-frame and multi-keyframe control, storyboard grids, and seamless transitions. Parts of the prompt-method guidance and the mode templates were withdrawn in November 2026 — see THIRD_PARTY_NOTICES.md. Use whenever the user asks for a Seedance 2.5 prompt, mentions Seedance 2.5 / Dreamina / Jimeng, wants a clip longer than 15s on Seedance, wants to EDIT or EXTEND an existing video rather than generate a new one, or supplies more than a handful of image/video/audio references. For Seedance 2.0 (4K, `mode=fast`, or a genre hint) use higgsfield-seedance instead."
user-invocable: true
metadata:
  tags: [higgsfield, seedance, seedance-2.5, dreamina, jimeng, omni-reference, video-edit, video-extension, multi-reference, long-video, keyframes, storyboard, blockout, transitions]
  version: 1.6.0
  updated: 2026-09-26
  parent: higgsfield
---

# Higgsfield Seedance 2.5 Director

Seedance 2.5 is a **different dialect from Seedance 2.0**, not a version bump you can
prompt through by habit. 2.0 is a reference-driven shot generator with a 4K lane and a
genre hint. 2.5 is an **omni-reference production model**: up to 50 reference
materials, 30-second native runtime, and three non-generation modes — it can edit a video
you already have, and extend one forward or backward from its boundary frame.

The prompt grammar changes with it. Reference roles are declared in prose (`@Image 1
defines …`), audio and text get bracket syntax, long videos are staged with explicit end
states, and first/last frames live inside `omni_reference` — either as the platform's
`start_image` / `end_image` roles or announced **inside the prompt** — never as a separate
mode.

> **Model split — read this before writing anything.** 2.5 tops out at **1080p** (no 4K
> lane) and has no `genre` hint. Since the 2026-09-26 snapshot it **does** expose
> `start_image` / `end_image` roles — but only in `omni_reference` mode. If the job needs
> 4K or a genre hint, it is a **Seedance 2.0** job — `../higgsfield-seedance/SKILL.md`.
> See § Choosing 2.0 vs 2.5.

## QUICK FACTS
*Generated-checked block (scripts/build_index.py verifies anchors). Routing aids — read the linked sections for the rules themselves.*
- Four modes, picked **before** writing: `t2v` · `omni_reference` · `video_edit` · `video_extension`; the mode changes what the prompt *is* [→](#the-mode-router)
- Higgsfield surface: **480p/720p/1080p** (no 4K), duration **4–30s**, `start_image`/`end_image` **only in `omni_reference`**, `t2v` takes zero references, no genre hint, `extension_mode` required for (and only for) `video_extension` [→](#the-higgsfield-parameter-surface)
- `video_edit` **ignores** `duration` and `aspect_ratio` and bills by the source video's length; `video_extension` inherits the source's aspect ratio [→](#the-higgsfield-parameter-surface)
- Each material also declares a **fidelity grade** — full-preserve / partial-preserve / attribute-transfer (name the target) / loose-guide; beat lines name characters (name + one visible marker), never handles [→](#fidelity--say-how-much-of-each-material-must-survive)
- Material budget: 30 images / 10 videos ≤30s total / 10 audio ≤30s total, 50 materials max (Dreamina's figures — the platform enforces only the 30-image and 50-material caps) — a platform `start_image`/`end_image` counts against both; stability ranges are 1–8 subjects (images), 1–5 subjects at 5–10s (video/audio) [→](#material-budget)
- Staging fixes too many EVENTS; two incompatible JOBS in one generation (physics + performance) is a separate cut — split into two prompts and stitch [→](#split-by-job-not-only-by-length)
- Bracket syntax: `()` music · `<>` SFX · `{}` dialogue · `【】` subtitles; non-Chinese dialogue needs a language line before the line; a music suppression never goes inside `()` — `(no music)` there reads as a music cue (house inference, the default) [→](#audio-and-text--bracket-syntax)
- First/last frames are `omni_reference` work: the platform `start_image`/`end_image` roles **or** an in-prompt declaration (`@Image 1 is the first frame`) — which holds better is unmeasured; keyframes 3+ are always in the prompt; never merge two anchors into one sentence [→](#first-last-frame-and-multi-keyframe-control)
- **AI-VFX production pipeline** — model-per-asset-class routing, the size-ref frame, location batching, the `omni_reference` v2v lane (source ≥4s, duration = source), the four-batch rule, the slop catalog: `VFX-PIPELINE.md`
- Hard limits that must not be over-promised (frame accuracy, locked parameters, pixel-identical transitions) [→](#hard-limits--do-not-over-promise-these)
- Dreamina-product features that are **not** on the Higgsfield surface — Ultra Long Video 180s, mark-based editing, Clay Renderer [→](#dreamina-only--what-higgsfield-does-not-expose)

---

## Provenance

Two primary sources, labelled throughout, plus the secondary sources below. What each
label *means* — and the evidence it requires — is the repo-wide legend in
`../shared/provenance.md`.

| Label | Source |
|---|---|
| `[OFFICIAL — Dreamina]` | ByteDance's *Dreamina Seedance 2.5 Prompt Guide* + *User Guide* — the model vendor's own prompt doctrine. Prompt grammar is model-side, so it carries across to Higgsfield's hosting. |
| `[OFFICIAL — platform]` | Higgsfield's live `models_explore` catalog, snapshot **2026-09-26** (`../../specs/model-specs.json`). Parameters, enums, and media roles come from here and nowhere else. |
| `[DREAMINA-ONLY]` | A Dreamina *product* feature with no Higgsfield parameter behind it. Never quote these as things the user can do here. |
| `[EMPIRICAL — sd25-pe]` | `sd25-pe`, a Seedance 2.5 skill file. The repo records only a Discord copy (v0.1.0, noted in the v3.33.0 changelog) and **not who wrote it**, so it is not labelled OFFICIAL. Its mapping-priority claim — material content outranks upload order — is recorded as that file's claim, not as a platform fact. |
| Secondary labels | `[OFFICIAL — Higgsfield Seedance 2.5 deck]` · `[DEMO — Higgsfield "AI Love Stories" tutorial]` · `[FIELD — AI-vs-VFX]` (the build in `VFX-PIPELINE.md`) · `[EMPIRICAL — MiniMax H3 skill corpus]` · `[EMPIRICAL — nutllwhy/seedance-tvc-director skill]` — each named where it is used. |

Where the two disagree about what is *settable*, the platform snapshot wins — it is what
the API actually accepts.

---

## The Mode Router

Pick the mode first. The same sentence means different things in different modes, and two
of the four modes are not generation at all.

| The user wants | Mode | What the prompt is |
|---|---|---|
| A clip from a description, no materials | `t2v` | A scene brief — the core formula below |
| A clip built from images / videos / audio they supply | `omni_reference` | A **role map** plus a scene brief |
| To change something inside a video they already have | `video_edit` | An **edit order**: master + scope + preserve list |
| More footage before or after a video they already have | `video_extension` | A **boundary contract** plus new content |

Two rules that fall out of this:

1. **First/last frames, keyframes, storyboard grids, and blockouts are all `omni_reference`.**
   2.5 has no separate first/last-frame mode on this platform. The first and last frame
   can go in two ways: the platform `start_image` / `end_image` roles (allowed **only** in
   `omni_reference` — the catalog rejects them in `t2v`, `video_edit` and
   `video_extension`), or ordinary references whose *role sentence* says they are the first
   and last frame. Which of the two holds the boundary better is **unmeasured**; keyframes
   3+ exist only in the prompt form. `[OFFICIAL — Dreamina: "no need to switch to a separate
   first/last-frame mode"]` · `[OFFICIAL — platform, snapshot 2026-09-26]`
2. **Editing is not regeneration.** If the user wants the shot rebuilt, that is
   `omni_reference` with the old clip as a motion reference — not `video_edit`. `video_edit`
   preserves the master's timeline and changes one scoped thing inside it.

> **Video-to-video is not automatically `video_edit`.** The field VFX workflow — swap the
> person in this plate, keep every other pixel — runs in **`omni_reference` with the source
> attached as a video reference**, because that is the lane where `duration` is settable and
> must be **matched to the source** (and where the source therefore has to be **≥ 4 s**, the
> `duration` floor). `video_edit` is the lane for a scoped change inside a master whose
> timeline must survive untouched. Full routing table + the performance-inheritance clause:
> `VFX-PIPELINE.md` § Stage 4. `[FIELD — AI-vs-VFX, 2026-08-08]`

---

## The Higgsfield Parameter Surface

`[OFFICIAL — platform, snapshot 2026-09-26]` · verify against `../../specs/model-specs.json`
before quoting (HARD RULE 3).

| Parameter | Values | Notes |
|---|---|---|
| `mode` | `t2v` · `omni_reference` · `video_edit` · `video_extension` | default `t2v` |
| `duration` | 4–30 s | default 5 — **ignored in `video_edit`** |
| `resolution` | `480p` · `720p` · `1080p` | default 720p — **no 4K on 2.5** (1080p added by the 2026-09-26 snapshot; not yet field-rated) |
| `generate_audio` | bool | default true |
| `bitrate_mode` | `standard` · `high` | default standard |
| `extension_mode` | `backward` · `forward` | **required** for `video_extension`, **not allowed** otherwise |
| aspect ratio | `auto` · `21:9` · `16:9` · `4:3` · `1:1` · `3:4` · `9:16` | ignored in `video_edit`; follows the source in `video_extension` |
| media roles | `start_image` · `end_image` · `image_references` · `video_references` · `audio_references` | `start_image` / `end_image` **only in `omni_reference`** |

The catalog also carries **reference-count rules** that the table cannot show
`[OFFICIAL — platform, CLI rules 2026-09-26]`:

- `t2v` takes **zero** references — no image/video/audio references and no start/end frame.
- `omni_reference` needs **at least one** reference (a start or end frame counts).
- `start_image` / `end_image` are accepted **only** in `omni_reference`.
- image references + start frame + end frame **≤ 30**; all references + start + end **≤ 50**.

Three consequences worth stating to the user before they spend credits:

- **`video_edit` bills by the source video's duration**, and neither `duration` nor
  `aspect_ratio` is settable — a 20-second master costs a 20-second render no matter how
  small the edit.
- **`video_extension` inherits the source's aspect ratio**; only the extension's
  *duration* is yours to set.
- **No `genre` parameter.** 2.0's genre hint does not exist here — genre lives in the
  prompt's visual-style clause instead.

Preflight the same way as 2.0:

```
python3 scripts/seedance_lint.py --preflight --model seedance_2_5 "<prompt>"
```

The linter reads the enums out of `../../specs/model-specs.json`, so an out-of-range duration, a
4K request, or a `video_extension` missing its `extension_mode` is caught before the
render.

---

## The Core Prompt Formula

*[Vendor-derived guidance withdrawn — see `THIRD_PARTY_NOTICES.md`.]*

---

## Reference Roles — Say What to Use *and* What Not to Use

*[Vendor-derived guidance withdrawn — see `THIRD_PARTY_NOTICES.md`.]*

### Fidelity — say how much of each material must survive

`[EMPIRICAL — MiniMax H3 skill corpus, re-derived 2026-08-09; cross-model structure,
unmeasured on Seedance]` A role says what job a material does; it still doesn't say how much of the
material must reach the pixels. Declare one fidelity grade per material, in the same
sentence as its role:

- **full-preserve** — the subject appears as-is: face, build, wardrobe, all of it.
- **partial-preserve** — the named parts survive, the rest is free: *"the jacket and the
  scar; hairstyle may change."*
- **attribute-transfer** — named traits lift onto a **different, named target**: *"apply
  this fabric's weave and sheen to Mira's coat."* The target must be named — this is the
  one case a bare role line cannot express, and the one that goes wrong silently.
- **loose-guide** — mood, palette, or energy only; nothing is copied literally.

```
@Image 4 defines the brocade fabric — attribute-transfer onto Mira's coat only.
Do not carry the garment's cut, the mannequin, or the studio backdrop.
```

### Material budget

`[OFFICIAL — Dreamina]` Hard limits vs the ranges that actually stay stable:

| Type | Hard limit | Stable range |
|---|---|---|
| Images | 30, each ≤4K | 1–8 distinct subjects |
| Videos | 10, ≤30s combined | 1–5 subjects, 5–10s each |
| Audio | 10 clips, ≤30s combined | only clips directly relevant |
| Video-edit source | 1 video + reference images | source ≤20s, 1–5 reference images |

50 reference materials total. On Higgsfield the platform enforces **two** of these caps and
counts a `start_image` / `end_image` against both: image refs + start + end ≤ 30, all
materials + start + end ≤ 50 `[OFFICIAL — platform, CLI rules 2026-09-26]`. The 10-video,
10-audio and ≤30 s-combined figures are Dreamina's; no platform rule states them — treat
them as the vendor's model limits, unverified on Higgsfield. Above the stable ranges (9–12 subjects in images, 6–10 in
audio/video, 6–8 edit reference images) generation still works but stability drops and the
shot may need several attempts — budget for it, or split the scene.

**More than five subjects needing multiple views → one view per image.** Independent view
images beat a single collage of views; the collage is the less stable form.

**Spend one view on a strong expression, not four resting faces.** `[OFFICIAL — Higgsfield
Seedance 2.5 deck, PART 2]` A set of neutral views teaches the model the face at rest and
nothing else, so the first line of dialogue invents a mouth. Generate the views on a neutral
light-grey ground (shade and mechanism: `../../templates/ad-asset-prep.md` § Design for win
rate) and make **one of them a strong expression** — anger, or a wide smile —
so the model learns the character's **facial dynamics and teeth structure**, not only the
resting face. The canonical four: front view · back view · facial details at neutral ·
facial dynamics and teeth under strong emotion.

---

## Multi-Reference — the Five-Step Workflow

*[Vendor-derived guidance withdrawn — see `THIRD_PARTY_NOTICES.md`.]*

---

## Long Video — Stages and End States

*[Vendor-derived guidance withdrawn — see `THIRD_PARTY_NOTICES.md`.]*

### Split by JOB, not only by length

Staging solves *too many events in one paragraph*. It does not solve **two
incompatible jobs in one generation**, and that is a separate cut worth making
[DEMO — Higgsfield "AI Love Stories" tutorial, 2026-08].

The reported case: an arena scene containing a fight (a giant throw, a sword
snatch, a takedown) and, in the same beat, the acting around it (a hidden
worry, a flirtatious exit, hope draining from a face). Run as one prompt it
held — badly, in both directions at once: *"the fight gets softer, the faces get
flatter."* The model spends its attention budget once. Asked to nail physics
and micro-performance in one generation, it half-does each.

Split into **two prompts, one job each, stitched in the edit**:

| Cut it here | Because |
|---|---|
| **physics ↔ performance** | mass, contact and follow-through vs. eyes, breath and micro-expression. Different attention, different optics, usually different shot sizes |
| **action ↔ dialogue** | the same split wearing other clothes |
| **the beat that needs room** | the second reported case: a 30s carnival scene *held* as one prompt, and was still split into 3×15s because the first-touch beat needed room — *"these beats felt completely rushed"*. Length was not the constraint; **pacing** was |

**How to tell which cut you need.** Length-driven splits are decided by
counting events. This one is decided by asking: *what is this shot's dominant
job?* If a prompt has two honest answers, it has two shots in it. That is the
same question the Feasibility Veto asks about a single frame, applied to a
whole generation.

Note the direction of the second case: it fit, and was split anyway. "It
generated" is not the bar — a scene that renders every beat but rushes the one
that matters has failed at the thing you were making it for.

Practical consequence, stated plainly by the same production: **a perfect 30s
render does not exist.** Generate raw footage per job, then assemble. Several
of the finished scenes in that film take the background from one take and the
foreground action from another.

### Timestamps and pacing

*[Vendor-derived guidance withdrawn — see `THIRD_PARTY_NOTICES.md`.]*

---

## Audio and Text — Bracket Syntax

`[OFFICIAL — Dreamina]` Prompts can be written entirely in natural language. Use the
brackets when music, SFX, dialogue, and subtitles must be told apart explicitly:

*[Third-party example material withdrawn — see `THIRD_PARTY_NOTICES.md`.]*

**Dialogue language reinforcement.** For non-Chinese dialogue — or when English text comes
back spoken in Chinese, or a specific regional variety is wanted — state it before the line.

Two house rules carry over from `../higgsfield-audio/SKILL.md` and the film-pipeline notes
that `../higgsfield-seedance/HELL-GRIND.md` used to carry (withdrawn):

- **Speech lives in the audio clause only** — not a word of dialogue inside the action
  description, or the model narrates it as behavior. The trap is that writers do not think
  of *subtext* as speech: `they exchange a look that says "you too?"` is a line the script
  never wrote, and it comes back spoken. `[EMPIRICAL — nutllwhy/seedance-tvc-director skill
  (MIT), re-derived 2026-08-09; the failing take is timecoded in that evaluation]` Anything readable is a
  voicing request — quoted subtext, a remembered line, a slogan, a sign read aloud. Write
  the visible behavior instead (*jaw sets, eyes hold*), and note that adding "no dialogue"
  does not undo it: the readable text is still there being asked for.
- **Diegetic-only is a project choice, and 2.5 finally obeys it.** Random subtitles and
  unrequested BGM were 2.0's most-reported nuisance; ByteDance calls suppression of both a
  headline 2.5 fix `[OFFICIAL — Dreamina]`. Still say it — and no `【】` block — rather
  than trusting the improvement. One part is settled: **lead with the positive diegetic
  list** (the sources and room tone the audio *is*). One is a default: **never put the
  suppression inside the `()` bracket** — `()` is the music channel, so `(no music)` there
  is most likely read as a music cue. That is a `[HOUSE]` inference, not a measurement; it
  stands as the default because writing the suppression as plain audio text after the list
  costs nothing (`../shared/house-rulings.md` P2-7). Which token to write —
  **`NO BGM`** (one third-party skill: a production term reads as a hard spec,
  `../higgsfield-audio/SKILL.md` § Suppressing music `[EMPIRICAL]`) or **`No music.`** (the
  form 12 of 13 harvested projects shipped, `../../templates/seedance/global-style-prefix.md`
  `[FIELD]`) — is **OPEN, unmeasured here** (`../shared/house-rulings.md` P2-7).

---

## First-Last Frame and Multi-Keyframe Control

`[OFFICIAL — Dreamina]` On 2.5 these are **not a mode** — they are `omni_reference` work.
Since the 2026-09-26 snapshot the platform also exposes `start_image` / `end_image` roles
(`omni_reference` only), so the first and last frame have **two routes**:

- **Platform roles** — attach the anchors as `start_image` / `end_image`. Keep a short role
  sentence in the prompt anyway (what the frame fixes, what may change) so the prose and the
  attachment agree. `[OFFICIAL — platform, snapshot 2026-09-26]`
- **In-prompt declaration** — attach the anchors as ordinary `image_references` and name
  their roles in prose. This is the form ByteDance's guide documents, and
  the only form for keyframes 3+.

Which route holds the boundary better is **unmeasured** — no O-Side generation compares
them. Don't do both for the same image (one image, one role).

*[Third-party example material withdrawn — see `THIRD_PARTY_NOTICES.md`.]*

1. **First and last images must share an aspect ratio**, or the last frame stretches. The
   output ratio locks to the **first** image; duration stays settable. (Dreamina doctrine for
   the in-prompt form; unverified for the platform `start_image` role.)
2. **Supplementary references supplement only their named attribute** — each one repeats the
   "do not change the first/last-frame composition" clause.

Storyboard grids are the next rung up: `MODE-PLAYBOOKS.md` § Storyboard grids. (The
blockout-reference templates were withdrawn in November 2026.)

---

## Editing, Extension, and the Composite Modes

The mode templates this section summarised were vendor-derived and have been withdrawn — see
`MODE-PLAYBOOKS.md` and `THIRD_PARTY_NOTICES.md` at the repository root.

---

## Emotional Direction and Camera Terms

*[Vendor-derived guidance withdrawn — see `THIRD_PARTY_NOTICES.md`.]*

---

## The Real-Person Character Formula

*[Vendor-derived guidance withdrawn — see `THIRD_PARTY_NOTICES.md`.]*

---

## Choosing 2.0 vs 2.5

| The job needs | Model |
|---|---|
| 4K output | **2.0** (`mode=std`) — 2.5 stops at 1080p |
| A `genre` hint parameter, or `mode=fast` | **2.0** |
| 1080p output | either — 2.0 needs `mode=std`; 2.5's 1080p is not yet field-rated |
| Platform start / end frame | either — 2.0 in any reference setup; 2.5 **only in `omni_reference`** |
| A clip longer than 15 seconds in one generation | **2.5** (up to 30s) |
| Editing a video that already exists | **2.5** (`video_edit`) |
| Extending a clip forward *or backward* | **2.5** (`video_extension`) |
| More than 9 reference images, or >3 reference videos/audio clips | **2.5** (30 / 10 / 10 vs 2.0's 9 / 3 / 3) |
| Cheap 480p prompt validation | either — both cap the draft lane at 480p |

**The honest default:** draft and structure on 2.5 when the job is long, reference-heavy, or
edit-shaped; finish on 2.0 when the deliverable needs 4K. They are not
interchangeable takes — a 2.5 draft validates the *prompt*, not the 2.0 render, for the same
reason `../higgsfield-seedance/SKILL.md` § Drafts Validate the Prompt gives: there is no
seed to pin.

### What carries over from 2.0 unchanged

The 2.0 engine rules carry over. Their numbered list was withdrawn from
`../higgsfield-seedance/ENGINE-RULES.md` in November 2026 (see `THIRD_PARTY_NOTICES.md`); that file
now keeps the high-risk shot table and its mitigations. Also carried over: the
positive-phrasing law (stated for 2.0 as an empirical law — Seedance parses negative-list
syntax as scene description; for 2.5 it is carried over by house assumption, unmeasured),
the homograph trap, and the block scaffold for production-scale briefs.

---

## Hard Limits — Do Not Over-Promise These

`[OFFICIAL — Dreamina]`

- **Timestamps allocate time; they are not frame-accurate edit points.** Never imply a beat
  will land on an exact frame.
- **Video-editing prompts raise the probability** that critical events align with the source —
  they cannot guarantee frame-by-frame overlap.
- **Multi-reference selects and combines** the right materials per scene; it does not make
  every material appear at once.
- **Frame-level text accuracy is not promised.** Subtitles, formulas, signs, and product
  specs need prepared reference materials plus post — the same conclusion as 2.0's text-rendering
  high-risk row.
- **Video editing locks the input's aspect ratio and approximate duration**; output may differ
  by up to ~0.3s from transition-frame handling.
- **First/last-frame generation locks aspect ratio to the first image**; mismatched ratios
  stretch the last frame.
- **Video extension locks aspect ratio to the source**; the extended segment's audio volume may
  differ slightly.
- **Boundary frames connect naturally, not identically** — review both sides of the seam plus
  the whole extended segment.
- **Seamless transitions aim for visual and audio continuity**, not pixel-identical preservation
  of either source clip.

---

## Dreamina-Only — What Higgsfield Does Not Expose

`[DREAMINA-ONLY]` These exist in ByteDance's own Dreamina/Jimeng product and appear in the
guides, but there is **no Higgsfield parameter behind them** on the 2026-09-26 snapshot. Do
not offer them here.

| Dreamina feature | Status on Higgsfield | Closest thing that does work |
|---|---|---|
| **Ultra Long Video** — 30–180s in one generation | Not exposed; `duration` caps at 30 | Stage a 30s generation and extend it once, to the 60 s single-chain ceiling (§ Extension chain math below); past that, re-anchor from the original references and assemble in post |
| **Nested extension to 60s** via repeated UI operations | The *model* rule (source ≤30s → extend up to 30s) holds; the one-click nesting UI does not exist | Chain `video_extension` calls, re-checking the boundary each time |
| **Edit with marks / Advanced Edit** — box, arrow, brush, anchor annotations on a frame | Not exposed; there is no annotation channel | `video_edit` with a written scope: object + change + effective time range |
| **Clay Renderer plugin** — white-model rendering workflow | Not exposed as a plugin | Blockout prompting via `omni_reference` (the `MODE-PLAYBOOKS.md` templates for it were withdrawn in November 2026) |
| Native 180s / multi-minute deliverables | — | Generate in 30s pieces and assemble in post (`../higgsfield-pipeline/SKILL.md`) |

**Extension chain math.** The model-side rule is: a source **within 30 seconds** can be
extended by 4–30 seconds in one operation, so a 30s source plus a 30s extension is the
60-second ceiling for a single chain. Beyond that, re-anchor from the original references
rather than extending an extension — the same degradation curve as 2.0's chain cap in
`../higgsfield-seedance/SKILL.md` § Extension Prompting.

---

## Pre-Submission Checklist

*[Vendor-derived guidance withdrawn — see `THIRD_PARTY_NOTICES.md`.]*

---

## Related Skills

- `../higgsfield-seedance/SKILL.md` — Seedance 2.0 director: the filter model, block scaffold,
  FOV anchors, prompt-craft laws, engine rules. **Everything model-agnostic lives there.**
- `../higgsfield-seedance/ENGINE-RULES.md` — the shared high-risk shot table and enforcement notes
- `../higgsfield-facs/SKILL.md` — facial control by Action Unit code
- `../higgsfield-seedance-vfx/SKILL.md` — video-to-video footage transforms on 2.0
- `../higgsfield-models/SKILL.md` — model choice against the specs layer
- `../higgsfield-pipeline/SKILL.md` — assembling 30-second pieces into a longer deliverable
- `MODE-PLAYBOOKS.md` — notes on editing, extension, storyboard grids and transitions (the long-form templates were withdrawn)
- `VFX-PIPELINE.md` — the AI-VFX production pipeline: asset-class model routing, the size-ref
  frame, location batching, the `omni_reference` v2v lane, the four-batch rule, the slop catalog
