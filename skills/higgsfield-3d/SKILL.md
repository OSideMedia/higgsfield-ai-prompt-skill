---
name: higgsfield-3d
description: "Use when the user wants a 3D model, mesh or GLB out of Higgsfield — image-to-3D, multi-view-to-3D, text-to-3D, rigging or animating a mesh, remesh / retopology, retexture, or 3D Body (human shape + pose from one photo) — or mentions 3D Jutsu / Scene Builder 3D (private Blender scene projects built through Python). Also use for a 3D turnaround of a character or prop as a consistent multi-angle reference, or a physical 3D blockout rendered as a staging reference for a video shot. Names that trigger it: generate_3d, sam_3_3d, image_to_3d, multi_image_to_3d, meshy_v7_image_to_3d, tripo_h3_1_image_to_3d, tripo_h3_1_multiview_to_3d, hunyuan3d_v3_image_to_3d, meshy_v6_text_to_3d, hunyuan3d_v3_1_text_to_3d, tripo_3d, 3d_rigging, meshy_v5_remesh, meshy_v5_retexture, sam_3_3d_body, animation_actions, scene_builder_3d_*."
user-invocable: true
metadata:
  tags: [higgsfield, 3d, glb, mesh, image-to-3d, multi-view, text-to-3d, rigging, animation, remesh, retexture, 3d-body, 3d-jutsu, scene-builder, blender, turnaround, staging-reference]
  version: 1.0.0
  updated: 2026-09-26
  parent: higgsfield
---

# Higgsfield 3D — Meshes, Rigs, and 3D Jutsu Scenes

## QUICK FACTS
*Routing aids — read the linked sections for the full rules. Nothing in this sub-skill is field-tested.*
- 17 3D models in the 2026-09-26 snapshot, six jobs: single image→3D, multi-view→3D, text→3D, rig, remesh / retexture, 3D Body [→](#the-catalog-17-models-six-jobs)
- **THE law:** the mesh reproduces only what is in the source image — to add or change props, clothing or held objects, edit the IMAGE first, then convert the edited result [→](#the-source-image-law)
- Multi-view beats single-view for geometry: 2–4 views of the same subject → `multi_image_to_3d` / `tripo_h3_1_multiview_to_3d` [→](#multi-view-beats-single-view)
- The `prompt` field: the MCP schema says only `sam_3_3d` accepts one; the CLI marks it REQUIRED on the three text→3D models — send it there, confirm with `get_cost` [→](#the-prompt-field-two-surfaces-disagree)
- Server-enforced rules: animation needs rigging; texture options need texturing ON; Hunyuan std caps the prompt at 200 characters and has no PBR [→](#parameter-rules-the-server-enforces)
- Rig + animate: humanoids rig best; `animation_action_id` comes from a 678-action library (ids 0–696, not contiguous — look up, never guess) [→](#rigging-and-animation)
- `get_cost: true` preflights for free; never auto-resubmit after a transport timeout [→](#cost-and-submission-discipline)
- 3D Jutsu = private Blender 5.2 scene projects: inspect (query) → guarded edit (run) → `show_scene` LAST [→](#3d-jutsu-scene-builder-3d)
- A generated GLB cannot enter a 3D Jutsu scene — imports are curated-catalog assets only in this version [→](#what-3d-jutsu-cannot-take-in)
- Film use 1: a mesh turnaround as a multi-angle reference — UNMEASURED [→](#film-use-1-a-3d-turnaround-as-a-multi-angle-reference)
- Film use 2: a 3D blockout rendered front-on from the camera's side becomes the SOURCE FRAME for the staging template — UNMEASURED [→](#film-use-2-a-3d-blockout-as-a-staging-reference)

---

## What this sub-skill is for

Higgsfield now generates **3D assets** (GLB meshes, optionally textured, PBR-mapped, rigged
and animated) and hosts **3D Jutsu**, a private Blender scene editor driven through Python.
This sub-skill documents what each surface is for, what its parameters are, the rules the
server enforces, and the two uses that matter to this repo's film work: a consistent
multi-angle reference, and a physical staging reference.

It is a **routing and discipline layer**, the same as the rest of this library: it picks
the model and writes the inputs; the execution surface (MCP connector, CLI, web UI) runs
the job — see `../higgsfield-stack/SKILL.md`.

**Everything here comes from the platform's own schemas** (provenance at the end). No 3D
job and no 3D Jutsu edit has been run from this repo. There are no quality rankings, speed
claims or prices in this file — none were measured, so none are stated.

**Not this sub-skill:** Cinema Studio 2.5's *3D Mode* (Gaussian splatting inside a
generated image) — that is `../higgsfield-cinema/SKILL.md` § 3D Mode. And not a Blender
tutorial: 3D Jutsu's Python surface is documented only as far as its tool contracts go.

---

## The catalog — 17 models, six jobs

`[OFFICIAL — platform, 2026-09-26]` — `../../specs/models_explore_snapshot_3d_2026-09-26.json`.
`../../scripts/sync_specs.py` has no 3D type yet, so there is no generated 3D spec table: this
table is read straight from the snapshot. Names and providers are as the snapshot states
them.

| Job | Model id | Snapshot name · provider | Input |
|---|---|---|---|
| Single image → 3D | `sam_3_3d` | SAM 3 3D Objects · Meta | 1 image (role `image`) |
| Single image → 3D | `image_to_3d` | Image to 3D · Meshy | 1 image (role `image`) |
| Single image → 3D | `meshy_image_to_3d` | Image to 3D · Meshy | 1 image (role `image`) |
| Single image → 3D | `meshy_v7_image_to_3d` | Meshy 7 Image to 3D · Meshy | image (role `image_references`) |
| Single image → 3D | `tripo_h3_1_image_to_3d` | Tripo H3.1 Image to 3D · Tripo | image (role `image_references`) |
| Single OR multi-view → 3D | `hunyuan3d_v3_image_to_3d` | Hunyuan3D v3 Image to 3D · Tencent | "one image or multiple views" (role `image_references`) |
| Multi-view → 3D | `multi_image_to_3d` | Multi-Image to 3D · Meshy | 1–4 images of the same subject (role `image`) |
| Multi-view → 3D | `meshy_multi_image_to_3d` | Multi-Image to 3D · Meshy | 1–4 images of the same subject (role `image`) |
| Multi-view → 3D | `tripo_h3_1_multiview_to_3d` | Tripo H3.1 Multiview to 3D · Tripo | 2–4 **ordered** views (role `image_references`) |
| Text → 3D | `meshy_v6_text_to_3d` | Meshy 6 Text to 3D · Meshy | prompt |
| Text → 3D | `hunyuan3d_v3_1_text_to_3d` | Hunyuan 3D v3.1 Text to 3D · Tencent | prompt |
| Text → 3D | `tripo_3d` | Text to 3D · *(provider, description and tags blank in the snapshot)* | prompt |
| Rig an existing mesh | `3d_rigging` | 3D Rigging · Meshy | `model_url` (a GLB) |
| Rig an existing mesh | `meshy_rigging` | 3D Rigging · Meshy | `model_url` (a GLB) |
| Remesh | `meshy_v5_remesh` | Meshy 5 Remesh · Meshy | `model_url` |
| Retexture | `meshy_v5_retexture` | Meshy 5 Retexture · Meshy | `model_url` + text or image style |
| Human body → 3D | `sam_3_3d_body` | 3D Body · Meta | 1 photo of people (role `image_references`) |

**Three duplicate pairs.** `image_to_3d` / `meshy_image_to_3d`, `multi_image_to_3d` /
`meshy_multi_image_to_3d` and `3d_rigging` / `meshy_rigging` carry the same name, provider
and parameter list in the snapshot. The MCP `generate_3d` schema names the **unprefixed**
ids as its defaults, and CLI 1.1.23 `model get` knows only the unprefixed ids (the
`meshy_`-prefixed three return `No model with job_type`). Use the unprefixed ids. Whether
the pairs share a backend is not stated anywhere — do not claim it.

### Picking a model

| You have / want | Use | The schema's reason |
|---|---|---|
| One image, **one object in a busy frame** — lift just that object | `sam_3_3d` | "Lift a single image of an object"; the only image→3D model that takes a `prompt` — "to disambiguate which object to lift"; `detection_threshold` 0–1; `export_textured_glb:false` for a white mesh |
| One image, texture + PBR + rig + animation in one job | `image_to_3d` | Optional texturing, PBR, rigging, animation. **`should_texture` defaults OFF** |
| Same, with a low-poly geometry mode or higher-fidelity geometry | `meshy_v7_image_to_3d` | `model_type` standard / lowpoly; `ultra_mode` ("higher-fidelity geometry and finer surface detail"); **`should_texture` defaults ON** |
| Face-count control, quads, real-world scale, orientation matched to the photo | `tripo_h3_1_image_to_3d` | `face_limit` 1,000–2,000,000; `quad`; `auto_size`; `orientation: align_image`; `texture_alignment` |
| Geometry-only or low-poly output | `hunyuan3d_v3_image_to_3d` | `generate_type` Normal / LowPoly / Geometry; `face_count` 40,000–1,500,000 (default 500,000). The densest ceiling in the catalog is Tripo H3.1's `face_limit` (up to 2,000,000) |
| **2–4 views** of the same subject | `multi_image_to_3d` | "More views = better geometric accuracy"; same feature set as `image_to_3d` |
| 2–4 views, Tripo controls | `tripo_h3_1_multiview_to_3d` | "2 to 4 ordered views" — the order convention is **not** in the schema; check the model page before relying on it |
| Only a description | `meshy_v6_text_to_3d` | `mode` preview (geometry only) / full (textures); lowpoly; can rig + animate |
| Only a description, Tencent | `hunyuan3d_v3_1_text_to_3d` | `mode` std ("rapid") / pro ("higher-quality"); PBR, `generate_type`, `face_count` are **pro-only** |
| Only a description, with a negative prompt | `tripo_3d` | `negative_prompt`; texture + PBR default ON; `texture_quality` / `geometry_quality` standard / detailed |
| A mesh that needs a skeleton | `3d_rigging` | Takes `model_url`, not images |
| A mesh with bad topology or the wrong size / pivot | `meshy_v5_remesh` | `topology` triangle / quad; `target_polycount` 100–300,000; `resize_height`; `origin_at` bottom / center |
| A mesh that needs a new surface | `meshy_v5_retexture` | `text_style_prompt` or `image_style_url` (image wins when both are set); `enable_original_uv` default ON |
| A photo of a person — body shape + pose | `sam_3_3d_body` | "Reconstruct human body shape and pose as a GLB"; per-person PLY meshes, 3D keypoints, Meta Human Representation (MHR) metadata |

When unsure, the connector's own instruction is to call `models_explore(action:'recommend')`
before any `generate_*` tool `[OFFICIAL — Higgsfield MCP server instructions, 2026-09-26]`.

---

## The source-image law

`[OFFICIAL — Higgsfield MCP tool schema, generate_3d, 2026-09-26]` verbatim:

> "The mesh reproduces only what is in the source image — to add or change props,
> clothing, or held objects, edit the image first with `generate_image`, then convert the
> edited result."

What that means in practice (the first three lines restate the schema; the rest is labeled):

- **Fix it in 2D, then lift it.** A missing prop, the wrong jacket, an empty hand — all
  of it is an image edit before it is a 3D job. There is no mesh-side "add a sword".
- **Retexturing is the one post-hoc surface change** the catalog offers
  (`meshy_v5_retexture`); geometry changes go back to the image.
- The image-side tools for that edit are the image sub-skills this library already has —
  `../higgsfield-gpt-image-2/SKILL.md` (reference sheets, edits) and
  `../../templates/ad-asset-prep.md` (prop three-views, product sheets).
- `[INFERENCE — untested]` A single-view source shows one side of the subject; the model
  has to supply the rest. That is the problem multi-view input exists to reduce (next
  section) — plan the source images for the angles you will need, not just the pretty one.

---

## Multi-view beats single-view

`[OFFICIAL — platform, 2026-09-26]` `multi_image_to_3d`: *"1-4 images of the same subject
from different angles … More images improve geometric accuracy."* The MCP schema says the
same: use it "when 2-4 views of the same subject are available (better geometric
accuracy)".

- **Same subject is the whole condition.** Four images of four slightly different
  characters are not four views. `[INFERENCE — untested]` Views cut from one generated
  sheet are more likely to agree than four separate generations — the same reasoning the
  cinema sub-skill applies to location sheets (`../higgsfield-cinema/SKILL.md` § Location
  Reference Sheets: alt angles "from a single seed" keep light and material consistent).
- **Role names differ by model**: Meshy multi-image takes role `image` (max 4); Tripo
  multiview and Hunyuan take `image_references`. The server "may auto-coerce when
  unambiguous" — still pass the declared role.
- **Tripo wants its views ordered**, and the order is not published in the schema. Do not
  guess a front / left / back / right convention into a delivery.

---

## The prompt field — two surfaces disagree

- `[OFFICIAL — Higgsfield MCP tool schema, generate_3d, 2026-09-26]`: *"Optional text
  guidance. Only sam_3_3d accepts a prompt (to disambiguate which object to lift). Other 3D
  models ignore it."*
- `[OFFICIAL — platform CLI 1.1.23, higgsfield model get <id> --json, 2026-09-26]`: `prompt`
  is **required** on `meshy_v6_text_to_3d`, `hunyuan3d_v3_1_text_to_3d` and `tripo_3d`;
  optional (default empty) on `sam_3_3d`; absent from every image-input, rig, remesh,
  retexture and body model.

The MCP sentence is accurate for the image-input models and cannot be literally true for
text→3D (a text→3D job with its prompt ignored has no input). **Do not settle it by
guessing:** for text→3D, send the prompt, and run `get_cost: true` first — the server
returns `adjustments` showing what it did with the request before anything is spent. For
texture direction on the image-input models, the fields are `texture_prompt` /
`texture_image_url` (Meshy) — not `prompt`.

---

## Parameter rules the server enforces

`[OFFICIAL — platform CLI 1.1.23, model get rules, 2026-09-26]` — each is a server-side
constraint; breaking one rejects the job.

| Model(s) | Rule |
|---|---|
| `image_to_3d`, `multi_image_to_3d`, `meshy_v7_image_to_3d`, `meshy_v6_text_to_3d` | `enable_animation` requires `enable_rigging=true` |
| `image_to_3d`, `multi_image_to_3d`, `meshy_v6_text_to_3d` | `animation_action_id` is required when `enable_animation=true` (`meshy_v7` defaults it to `92`) |
| `image_to_3d`, `multi_image_to_3d`, `meshy_v7_image_to_3d` | `texture_prompt`, `texture_image_url` and `enable_pbr` each require `should_texture=true` |
| `meshy_v6_text_to_3d` | texture options (`texture_prompt`, `texture_image_url`, `enable_pbr`) require `mode=full`; `rigging_height_meters` requires `enable_rigging=true` |
| `hunyuan3d_v3_1_text_to_3d` | in `mode=std`: prompt ≤ 200 characters, no `generate_type`, no `face_count`, no `enable_pbr` (PBR needs `pro`); `enable_pbr` is ignored with `generate_type=Geometry` |
| `hunyuan3d_v3_image_to_3d` | `enable_pbr` unsupported with `generate_type=Geometry`; `polygon_type=quadrilateral` requires `generate_type=LowPoly` |
| `meshy_v5_retexture` | `text_style_prompt` or `image_style_url` is required |
| `tripo_h3_1_*` | "Enabling PBR also enables textures" (schema description) |

**Two defaults that bite:** `image_to_3d` / `multi_image_to_3d` return an **untextured**
mesh unless `should_texture: true` is set; `meshy_v7_image_to_3d` textures by default.
Meshy `target_polycount` defaults to 30,000 (range 100–300,000); Meshy `should_remesh`
defaults on, and when off, "returns the raw triangular mesh and topology/target_polycount
are ignored".

---

## Rigging and animation

`[OFFICIAL — platform, 2026-09-26]` + `[OFFICIAL — Higgsfield MCP tool schema, 2026-09-26]`

- **Two routes to a rig:** `enable_rigging: true` on a generating model (Meshy image,
  multi-image, 6 text, 7 image), or `3d_rigging` on a mesh you already have. `3d_rigging`
  takes `model_url` — a public HTTPS GLB without embedded credentials, or (per the MCP
  schema) a prior 3D `job_id`.
- **Humanoids rig best.** The schema's own caveat: "Works best on humanoid/character
  subjects; non-bipeds (animals, objects) may rig poorly."
- **Pose:** `pose_mode` `a-pose` / `t-pose` — "Recommended with enable_rigging for cleaner
  skeletons." `rigging_height_meters` (default 1.7) scales the skeleton.
- **Animation:** `enable_animation: true` + `animation_action_id`. The library holds **678
  actions** with ids in **0–696** — the ids are not contiguous, so never compute or guess
  one. The schema's named picks: idle `0`, walk `30` (Casual_Walk), run `16` (RunFast),
  jump `466` (Regular_Jump), wave `28` (Big_Wave_Hello), dance `64` (All_Night_Dance).
- **Look it up:** MCP `animation_actions` (read-only, no job; groups WalkAndRun,
  BodyMovements, DailyActions, Dancing, Fighting; each result carries a preview GIF — when
  several fit, show the previews and let the user pick) or CLI
  `higgsfield preset list animation-action --query walk`.
- Rigging and animation each **add cost** (schema wording) — preflight.

---

## Cost and submission discipline

- **Preflight is free:** MCP `generate_3d` with `get_cost: true` "preflights credits
  without submitting"; CLI `higgsfield generate cost <model_id> [--param value]…`. Apply the
  `adjustments` the server returns. This file lists no prices — they were not measured.
- **Cost drivers the schema names:** texturing ("Costs more credits"), rigging and
  animation ("Adds cost"). `count` 1–4 multiplies the job.
- **Timeouts:** "On a transport timeout the submission outcome may be unknown: do not
  automatically resubmit. Reuse returned job IDs and retry only after the original outcome
  is known."
- **Inputs:** `medias[].value` is a `media_id` or a prior `job_id`, never a URL (web media
  goes through `media_import_url`; local files through `media_upload_widget`). The
  exception is the `model_url` field on rig / remesh / retexture, which is a URL — for
  remesh and retexture the snapshot says to upload the GLB through the media API with
  `type=file` and pass the returned URL.
- Surface choice and the general two-step preflight: `../higgsfield-stack/SKILL.md`
  § Preflight discipline.

---

## 3D Jutsu (Scene Builder 3D)

`[OFFICIAL — Higgsfield MCP tool schema, scene_builder_3d_*, 2026-09-26]`

A **private project** holding a Blender scene that an agent edits by running Python
against it; results deliver as a GLB (portable) or a `.blend` (editable source).

| Step | Tool | Contract |
|---|---|---|
| Find or make a project | `scene_builder_3d_list_projects` / `scene_builder_3d_create_project` | Creation is **not idempotent** — on an interrupted or uncertain create, list projects before retrying, or you make a duplicate |
| Read state | `scene_builder_3d_get_project` | Revision, scene sequence, active operation, committed artifacts. An empty project is a valid empty scene at revision 0 |
| Inspect | `scene_builder_3d_query_python` | `bpy` + `artifacts`; temporary changes are discarded; can **render and publish preview images** without committing; returns the guards `revisionBefore` + `sceneSequenceAfter` |
| Edit | `scene_builder_3d_run_python` | One coherent edit against the exact inspected `revision` + `expectedSceneSequence`, with a stable `operationId`; advances `revisionAfter`. One mutation per project at a time; on a stale-state conflict, inspect again and regenerate with fresh guards and a new operation id |
| Add a model | `scene_builder_3d_search_assets` → `scene_builder_3d_import_asset` | Curated catalog GLBs only; copy the search result's `importArguments` (incl. `catalogSearch`); never repeat an import to poll it |
| Wait | `scene_builder_3d_get_operation` | Poll an active operation (`waitSeconds` max 8) |
| Deliver | `scene_builder_3d_show_scene` | **The final 3D Jutsu call**, with the exact committed revision. The widget is for the user — it is not visual evidence for the agent |
| Verify | `scene_builder_3d_get_artifact` | Fetch a render a query or edit published; inspect it before judging framing, light or geometry |
| Export | `scene_builder_3d_get_glb` / `scene_builder_3d_get_blend` | Short-lived downloads of an existing export; "a successful download does not establish that the exported scene looks correct" |

**Engine facts the schema pins:**

- Blender **5.2**; engines `BLENDER_EEVEE`, `BLENDER_WORKBENCH`, `CYCLES` (not
  `BLENDER_EEVEE_NEXT`). Query RNA rather than assuming older APIs exist.
- Build at **metre scale** with descriptive object names. For a new multi-object scene,
  establish the delivery camera, a motivated key light, fill and ambient light in the first
  blockout.
- Committed scenes are finalized with **Eevee and Khronos PBR Neutral**. Procedural
  shaders and world lighting "do not reliably carry into GLB" — use Principled materials and
  Point / Sun / Spot lights when GLB delivery matters.
- Published files: at most **8** PNG / JPEG / MP4 per operation, 512 MiB each, 1 GiB total,
  images ≤ 16,384 px per side and ≤ 64 MP. Python code ≤ 256 KiB.
- Coordinates: the editor / glTF side is **Y-up**; `bpy` is **Z-up** — account for it when
  comparing transforms.

### What 3D Jutsu cannot take in

- `scene_builder_3d_import_asset`: "This version accepts catalog assets only." and
  "Attachment IDs are not supported by this tool."
- `run_python` / `query_python`: "No network fetches or embedded model bytes; use
  scene_builder_3d_import_asset."

So **a GLB from `generate_3d` — or the user's own model — has no documented way into a 3D
Jutsu scene** in this version. A Jutsu scene is built from catalog assets plus geometry
made in `bpy`. Say this before anyone promises "put my generated character in the scene".

---

## Film use 1 — a 3D turnaround as a multi-angle reference

`[HYPOTHESIS — UNMEASURED; nothing below has been fired]`

**The idea.** Image-generated turnarounds draw every angle separately, and each angle can
drift. A mesh has one geometry: render it from any angle and the angles agree by
construction. That is the property worth testing.

**The chain.**

1. Build the source images — ideally 2–4 views of the subject as one sheet — and fix
   every prop, garment and held object **in the image** first (§ The source-image law).
2. `multi_image_to_3d` (or `tripo_h3_1_multiview_to_3d`) with `should_texture: true`;
   `get_cost: true` first.
3. Render the GLB from the angles the production needs. **Where:** 3D Jutsu cannot import
   it (§ What 3D Jutsu cannot take in), so the renders happen in any GLB viewer or the
   user's own Blender, outside Higgsfield.
4. Use the renders as image references — character-sheet panels, `@` Elements, Seedance
   image references.

**What is not known — say it, don't paper over it:**

- Whether a textured mesh holds a **face's** identity. For faces this library's route is
  Soul ID and character sheets (`../higgsfield-soul/SKILL.md`); a mesh render is not a
  substitute until someone measures it.
- Whether a rendered-CG reference **bleeds its render look** into a photoreal video. The
  staging-reference work measured that a graphic-looking reference *can* bleed, and closed
  it with a three-layer architecture (`../../templates/seedance/staging-reference.md`); the
  same risk plausibly applies to mesh renders and is untested.
- A reasonable first probe: a **rigid prop** — no face, no cloth, nothing that deforms — is
  the case with the least to lose.

Higgsfield's own image-side turnaround path is its `character-sheet` workflow — see
`../higgsfield-stack/SKILL.md` § Higgsfield's bundled workflows for when to hand off to it.

---

## Film use 2 — a 3D blockout as a staging reference

`[HYPOTHESIS — UNMEASURED; nothing below has been fired]`

This library already names the right shape for a reference a video model sees:
`../../templates/seedance/staging-reference.md` — **front-on, from the camera's side**,
thin muted-colour outlines, attached **last**, described in positive form only. And
`../../templates/seedance/top-down-map.md` — a floor plan is for **reasoning**, never
attached. A 3D scene can serve both, because a camera placed in a scene renders exactly
the shape the doctrine asks for.

**What 3D adds.** Real perspective, relative scale in metres, and a camera you can put
where the shot's camera actually is — the geometry a hand sketch only approximates.

**The chain.**

1. **Block it in 3D Jutsu at metre scale.** Stand-in figures (`bpy` primitives or catalog
   assets from `scene_builder_3d_search_assets`) with descriptive names, the anchoring
   furniture, and **one delivery camera** at the shot's position, height and lens.
2. **Render front-on through that camera** with `scene_builder_3d_query_python` (a query
   render publishes a PNG without committing a revision) and fetch it with
   `scene_builder_3d_get_artifact`.
3. **That render is not the staging reference — it is the source frame.** A Blender render
   has shaded, solid figures; layer 1 of the anti-bleed architecture is *outlines, never
   fills*. Feed the render to **Step 1** of `staging-reference.md` (the diagram-generation
   prompt) exactly as the template feeds a real frame: it converts the frame into the thin
   muted outline drawing, with the same colour legend, tag naming and QA checklist.
4. **Write the words from the scene data.** The template requires every figure's
   position, pose and facing to be spelled out in words ("the words carry the staging").
   `query_python` returns exact object names, positions in metres and transforms — the
   per-figure lines can be read off the scene instead of eyeballed.
5. **Optional floor plan:** a render from an overhead camera of the same scene is a
   top-down map — reasoning only, per `top-down-map.md`; never attached.
6. **Coverage:** move the camera, render again, run Step 1 again. The template's rule —
   *regenerate from the original frame, never from the previous diagram* — holds
   automatically, because every diagram is drawn from a fresh render of the same geometry.

**The measured caveat still governs.** The staging reference tracked the map's
orientation **6/12 — chance** (`staging-reference.md`). A more accurate source geometry
does not change what the video model does with the map. Offer this as a sharper shared
*authoring* artifact; when a position must hold, back it with the prose blocking locks the
template points to.

A third, smaller possibility — `sam_3_3d_body` turns a photo of a person into body shape,
pose and 3D keypoints — could supply a pose from a reference photo. Its GLB cannot enter
3D Jutsu either; unmeasured.

---

## Provenance and what is not known

- **Catalog:** `../../specs/models_explore_snapshot_3d_2026-09-26.json`
  `[OFFICIAL — platform, 2026-09-26]` (17 models, `has_more: false`). The snapshot ages out
  of the 30-day trust window on 2026-10-26 — after that, verify live (HARD RULE 3):
  `models_explore(type:'3d')` or `higgsfield model get <id>`.
- **Tool contracts:** `generate_3d`, `animation_actions`, `scene_builder_3d_*`
  `[OFFICIAL — Higgsfield MCP tool schema, 2026-09-26]` — read from the connector's tool
  definitions; no tool was called.
- **Prompt requirements and CEL rules:** `[OFFICIAL — platform CLI 1.1.23, higgsfield model
  get <id> --json, 2026-09-26]` — free schema reads, no job created.
- **Not known:** output quality, speed, price, how any 3D model handles faces, how a
  mesh-derived reference behaves in a video model, the Tripo view order, whether the
  duplicate Meshy ids share a backend. Nothing here was fired.

## Related skills

- `../higgsfield-stack/SKILL.md` — execution surfaces, preflight, and Higgsfield's own `character-sheet` workflow
- `../higgsfield-gpt-image-2/SKILL.md` — reference sheets and image edits (the "edit the image first" step)
- `../higgsfield-soul/SKILL.md` — face identity (the route a mesh does not replace)
- `../higgsfield-cinema/SKILL.md` — Cinema Studio 2.5 3D Mode (Gaussian splats — a different "3D")
- `../../templates/seedance/staging-reference.md` · `../../templates/seedance/top-down-map.md` — the staging doctrine Film use 2 plugs into
