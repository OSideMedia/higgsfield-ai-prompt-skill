# Field-Test Queue

The models and doctrine claims this library states **without a single O-Side generation behind
them**, ordered by what each test would change. Nothing here has been fired. It is the plan for
the day credits are available — not a record of results.

**Costs** are `higgsfield generate cost` estimates taken **2026-09-26** on the CLI's API account
(prompt-only, no media attached). `generate cost` creates no job (checked: the job list was
identical before and after every estimate). Subscription credit pricing can differ from the API
account, and attaching media can change a price — **re-run the estimate** (CLI `generate cost`,
or `get_cost: true` on the MCP `generate_*` tools) immediately before firing, and log the real
spend. Costs are itemised per model; never quote the total alone.

**Protocol for every row:** fire the cheapest config that answers the question, same prompt
across arms, one variable changed. Log each generation to the ledger (`db/ledger/`, one row per
attempt — `SKILL.md` § HARD RULES). A single generation is an observation, not a rating: a model
gets star rows in `model-guide.md` only after enough runs to judge it, and the verdict names
route, model id, resolution, n, and date (tag `[MEASURED]`).

## Priority 1 — claims the 2026-09-26 refresh just changed

| # | Question | Arms (model · settings) | Credits per arm | What changes on the answer |
|---|---|---|---|---|
| 1 | Does Seedance 2.5's new **1080p** lane hold detail the 720p lane loses? | `seedance_2_5` t2v 5s @ 720p · same @ 1080p | 35 · 60 | `higgsfield-seedance-2-5` § Choosing 2.0 vs 2.5 (the 1080p row says "not yet field-rated") |
| 2 | Which first-frame route holds the boundary better on 2.5 — the platform `start_image` role or the in-prompt `@Image 1 is the first frame` declaration? | `seedance_2_5` omni_reference 5s @ 480p, same anchor image, route A vs route B | 15 + media (preflight with the image attached — omni_reference refuses a cost estimate with no reference) | `higgsfield-seedance-2-5` § First-Last Frame (currently "unmeasured") |
| 3 | For a 20s single take, does Wan 3.0 match Seedance 2.5 at a third of the price? | `wan3_0` 20s @ 480p · `wan3_0_prime` 20s @ 480p · `seedance_2_5` 20s @ 480p | 20 · 30 · 60 | `model-guide.md` long-take chooser |
| 4 | Is Wan 3.0's smart duration (`-1`, billed as 10s) usable, or does it pick lengths that break the cut? | `wan3_0` duration −1 @ 480p, 3 prompts of different natural length | 10 each | long-take chooser — smart duration stays "only on explicit request" until this runs |
| 5 | Does `enable_thinking` change prompt adherence? (It does not change the price: 5 = 5.) | `wan3_0` 5s @ 480p, thinking off · on, same dense prompt | 5 · 5 | long-take chooser |

## Priority 2 — new models with no rating

| # | Question | Arms | Credits per arm | Owner doc |
|---|---|---|---|---|
| 6 | GPT Image 2.5: `flare` vs `sunburst`, and does `background: transparent` produce a clean alpha? | `gpt_image_2_5` low 1k flare · sunburst · flare + transparent | 0.25 · 0.25 · 0.25 | `higgsfield-gpt-image-2` |
| 7 | GPT Image 2.5 vs GPT Image 2 on the repo's text-rendering and clothing tasks | `gpt_image_2_5` medium 1k · `gpt_image_2` low 1k (same price class) | 0.5 · 0.5 | `image-models.md` |
| 8 | Grok Image 2.0 first look | `grok_image_2_0` low 1k | 1.25 | `image-models.md` |
| 9 | Seedream 5.0 Flash vs Lite/Pro on instruction edits | `seedream_5_0_flash` 1k | 0.5 | `image-models.md` |
| 10 | MiniMax H3 Max first look | `minimax_h3_max` 5s @ 480p | 7.5 | `model-guide.md` |
| 11 | Gemini Omni Flash 1.1 first look (cheapest possible) | `gemini_omni_flash_1_1` text-to-video 3s @ 360p | 3 | `model-guide.md` |
| 12 | FLUX 3 Video first look (still unrated since 2026-08-07) | `flux_3_video` 5s @ 720p | 27.5 | `model-guide.md` |
| 13 | Cinema Studio 4.0: does the optical stack (camera body / lens / aperture / era / light) change the render the way the 3.5 stack does? | `cinematic_studio_video_4_0` 5s @ 480p, stack off · on | 15 · 15 | `higgsfield-cinema` |
| 14 | 3D — does a text-to-3D mesh give a usable staging/turnaround reference? | `tripo_3d` (text) | 5 | `higgsfield-3d` |

## Priority 3 — edit lanes (need a source clip; price depends on it)

Seedance 2.5 `video_edit` and Cinema Studio 4.0 `video_edit` bill by the source duration;
FLUX 3 Video Edit states 1 credit per second of the processed clip (first 15s at most). Kling 3.0
Omni Edit, Gemini Omni Flash 1.1 `edit`, Genjutsu (`hf_mult_motion_control`,
`hf_mult_replace_object`) and Ad Multiplier need the source attached for an estimate. Use one
short (4–5s) source clip for every arm so the lanes compare on the same plate — the question is
which lane preserves what `model-guide.md`'s edit-lane chooser says it preserves.

## Things the estimates themselves revealed (2026-09-26)

- The CLI's own validator rejects `omni_reference` with no reference: "mode 'omni_reference'
  requires at least one reference media item" — the platform rule the 2.5 doctrine now states.
- `meshy_v6_text_to_3d` and `hunyuan3d_v3_1_text_to_3d` could not be estimated: the CLI reported
  "Unsupported validation rule" for their constraint rules (they use `type(…)` checks). Estimate
  those through the MCP `generate_3d` `get_cost` preflight instead.
- `generate cost workflow cinematic_studio_video_4_0` fails ("Unknown workflow") although
  `workflow list` shows it; estimating it as a model id works.
