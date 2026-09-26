---
name: higgsfield-stack
description: "Use when the user mentions the Higgsfield CLI (binaries `higgsfield` / `higgs` / `hf`, `higgsfield auth login`, `higgsfield generate create`, `higgsfield workflow`, the `@higgsfield/cli` npm package), the Higgsfield MCP custom connector (`mcp.higgsfield.ai/mcp`) or its bundled workflows (`get_workflow_instructions` — character-sheet, thumbnail-generation, ugc-* videos, faceless-video, narrator, subtitles, product-photoshoot, brand-asset-creation, ad-multiplier, video-editing / Higgsedit, website-builder-flow), Higgsfield's bundled skills repo (`higgsfield-ai/skills` — `higgsfield-generate`, `higgsfield-soul-id`, `higgsfield-product-photoshoot`, `higgsfield-brandkit`, `higgsfield-marketplace-cards`, `higgsfield-websites`, `higgsfield-video-explainer`, `higgsfield-youtube-thumbnail`, invoked as `/higgsfield:generate` etc.), or asks how this skill coexists with those tools (`do I need both`, `how does this work with the CLI/MCP/skills`, `should Higgsfield's workflow do this or you`)."
user-invocable: true
metadata:
  tags: [higgsfield, stack, cli, mcp, official-skills, bundled-workflows, coexistence, handoff, environment]
  version: 1.3.0
  updated: 2026-09-26
  parent: higgsfield
---

# Higgsfield Stack — Coexistence With Official Tooling

## What this sub-skill is for

"The Higgsfield stack" means Higgsfield's own official tooling: their command-line interface (CLI), their custom MCP connector for claude.ai and the Claude desktop app — which now ships its own **bundled workflows** — and their bundled-skills repo (`higgsfield-ai/skills`, v0.12.0). Any one of those tools — or any combination — may be present in the user's environment alongside this prompt skill. This sub-skill documents how the surfaces coexist, what each one owns, and how a clean handoff looks.

The core principle is a layer split. This skill is the prompt-construction + production-discipline layer: MCSLA structure, named platform vocabulary, model selection criteria, Seedance preflight, Cinema Studio depth, Soul Character Anchor Block, Two-Tool Refinement Pipeline guidance, anti-bombast register, shared negative constraints. Their stack is the execution layer: authentication, file uploads, job submission, polling, retries, returning a result URL. Our skill never invokes their CLI.

**What changed in 2026.** The execution layer is no longer prompt-free. Higgsfield's connector now carries 16 named workflows (character sheets, thumbnails, UGC videos, faceless video, ad multiplication, editing …) that bring their own prompt engines, and several of their bundled skills enhance prompts on the backend. The split still holds for direct generation; for requests that are squarely one of their workflows, § Higgsfield's bundled workflows says what this library adds and what it hands off.

---

## The three official surfaces

| Surface | What it is | Detection signals | Best fit |
|---|---|---|---|
| **Higgsfield CLI** | Binary distributed at https://github.com/higgsfield-ai/cli. Binary names: `higgsfield`, `higgs`, `hf`. Install via `curl -fsSL https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh \| sh` or `brew install higgsfield-ai/tap/higgsfield`. Auth via `higgsfield auth login` (device flow). As of 1.1.23 its commands include `generate`, `model`, `workflow`, `preset`, `voices`, `upload`, `soul-id`, `marketing-studio`, `product-photoshoot`, `marketplace-cards`, `website`, `workspace`, `account`. | User types `higgsfield`, `higgs`, or `hf` in conversation; user says "I have the CLI installed"; user pastes output from `higgsfield ... --json` | Claude Code, Codex, Cursor, or any terminal-native agent. Per Higgsfield's own guidance: if the user is in Claude Code or Codex, prefer the CLI over the MCP. |
| **Higgsfield MCP** | Custom connector at https://mcp.higgsfield.ai/mcp. Separate product from the CLI. Installed in claude.ai or the Claude desktop app via Settings → Connectors → Add custom connector. Ships **bundled workflows** loaded with `get_workflow_instructions` (§ Higgsfield's bundled workflows). | User is in claude.ai web or the Claude desktop app (not a terminal); user mentions "the connector" or "MCP" or `mcp.higgsfield.ai`; the current Claude session has tools whose names mention Higgsfield generation. | claude.ai web, Claude desktop app, environments without a terminal. |
| **Higgsfield bundled skills** | Skill repo at https://github.com/higgsfield-ai/skills — `VERSION` **0.12.0**, last commit 2026-09-11. Install via `npx skills add higgsfield-ai/skills`, `gh skill install higgsfield-ai/skills`, or the Claude Code marketplace (`/plugin marketplace add higgsfield-ai/skills`, then `/plugin install higgsfield@higgsfield`). Invoke as `/higgsfield:<skill>`. Skill list below. | Skill files matching those names visible in the agent's skill directory; user invokes one of those slash commands; user mentions installing `higgsfield-ai/skills`. | Agents that consume Markdown skill bundles (Claude Code, Cursor, Codex …). The skills drive the CLI under the hood; several add backend prompt enhancement. |

### The bundled skills at 0.12.0

`[OFFICIAL — Higgsfield skills repo, README + VERSION, 2026-09-26 capture]`

| Skill | Invoke | What it owns (their README, condensed) |
|---|---|---|
| `higgsfield-generate` | `/higgsfield:generate` | Image, video, **3D** and audio generation across 30+ models, plus Marketing Studio branded ads and **Virality Predictor** scoring of finished videos |
| `higgsfield-soul-id` | `/higgsfield:soul-id` | Train a Soul Character; returns a `reference_id` |
| `higgsfield-product-photoshoot` | `/higgsfield:product-photoshoot` | 10 modes (studio, lifestyle, Pinterest pin, hero banner, carousel, ad pack, virtual try-on, conceptual, restyle, closeup-with-person) on `gpt_image_2`, backend prompt enhancement |
| `higgsfield-brandkit` | `/higgsfield:brandkit` | Visual identity: palettes, editable SVG marks, typography, mockups, packaging, decks, brandbooks |
| `higgsfield-marketplace-cards` | `/higgsfield:marketplace-cards` | Marketplace main / secondary images and A+ style modules, backend prompt enhancement |
| `higgsfield-websites` | `/higgsfield:websites` | Build, edit and deploy full-stack websites |
| `higgsfield-video-explainer` | `/higgsfield:video-explainer` | Narrated non-photoreal explainer as matched Seed Audio + Gemini Omni blocks, assembled with `explainer_video` |
| `higgsfield-youtube-thumbnail` | `/higgsfield:youtube-thumbnail` | Truthful, high-impact thumbnails and vertical covers, identity-preserving references |
| `higgsfield-game-generation` | `/higgsfield:game-generation` | Playable browser games, or game sprites, textures, **rigged 3D assets** and audio |

**Count discrepancy, unresolved:** the README's badge and table list **9** skills; the
top-level skill directories captured on 2026-09-26 were **8** — no `higgsfield-game-generation`
directory. Check the repo before telling a user that skill is installable.

---

## Preflight discipline — check cost and balance before generating

Every Higgsfield generation costs credits, and production-grade AI cinema runs at roughly 1.0% image and 1.5% video acceptance rates (`production-benchmarks.md`). On Veo, Kling, Sora-2, and Seedance-class video, a single un-checked job can swallow hours of budget. The preflight pattern is part of the Tier 1 *Lock-before-generate* discipline (`DISCIPLINE.md`) — lock the cost estimate alongside the prompt, before submission, on whichever surface the user is on.

This skill never invokes the preflight itself; it names the pattern. The execution layer owns the calls. Both MCP and CLI expose dedicated preflight surfaces — same underlying API, different invocation shapes.

### Two-step preflight

Preflight is two steps, not one. The v3.7.10 release named only the second step (cost estimate); dogfooding immediately surfaced why the first step matters.

**Step 1 — Verify the model's param schema.** Models have bounded, enumerated params: aspect ratios are not free-form, durations have ranges, mode tags are model-specific. The schema is the ground truth; training-data knowledge of "what CLI flags usually look like" is not. Skip this step and you can produce a syntactically-valid preflight command that targets an invalid parameter value — the kind of mistake that hard-fails on submission and burns iteration time you thought you were saving.

**Step 2 — Estimate cost** against the now-verified schema.

| Step | MCP | CLI |
|---|---|---|
| 1. Schema verify | `models_explore(action="get", model_id="<model>")` | `higgsfield model get <model>` — or `higgsfield workflow get <name>` for a workflow job type (Cinema Studio 4.0, `voice_change`, `reframe` …) |
| 2. Cost estimate | `generate_image` / `generate_video` / `generate_audio` / `generate_3d` with `get_cost: true` | `higgsfield generate cost <model> [--param value]...` — or `higgsfield generate cost workflow <name> [--param value]...` |

**Failure mode this prevents — plausibility-over-verification.** The model knows enough about Higgsfield (and about CLIs generally, and about MCP schemas generally) to produce a *plausible* preflight call. Plausibility is not validity. Plausibility says `--aspect-ratio 2.35:1` because hyphenated flags and cinematic anamorphic ratios are both prevalent in training data. Verification says `--aspect_ratio 16:9` because that is what `higgsfield model get kling3_0` returns. The discipline is to run the verification command that is sitting right there, not to trust the plausible answer. This pattern recurs across surfaces — see `DISCIPLINE.md` Tier 1 § Plausibility-over-verification for the cross-cutting framing.

### Verified preflight surfaces

| Concern | MCP | CLI | Bundled skills |
|---|---|---|---|
| Schema verification (param enum, ranges, defaults) | `models_explore(action="get", model_id="<model>")` | `higgsfield model get <model>` | Drop to CLI for the verify |
| Cost estimate (no job submitted) | `generate_image` / `generate_video` / `generate_audio` / `generate_3d` with `get_cost: true` | `higgsfield generate cost <model> [--param value]...` | Drop to CLI for the check, then run the slash command |
| Cost estimate — a workflow job type | — | `higgsfield generate cost workflow <name> [--param value]...` works for some workflows (`reframe` verified 2026-09-26); `cinematic_studio_video_4_0` and `voice_change` are rejected there ("Unknown workflow") — estimate them by model id (`higgsfield generate cost cinematic_studio_video_4_0 …`; `voice_change` needs `--input_video` + `--voice_id`) | Drop to CLI |
| Cost estimate — Shorts Studio | `shorts_studio_create` with `get_cost: true` + `duration_seconds` (no preset or upload needed) | — | — |
| Surfaces whose schema states no cost and has no `get_cost` | `virality_predictor`, `video_analysis_create` — check `balance` before and after (`../higgsfield-repurpose/SKILL.md` § Paid or free) | — | — |
| Credit balance + plan + email | `balance` tool | `higgsfield account status` | Drop to CLI |
| Recent transactions (newest first) | `transactions` tool | `higgsfield account transactions --size N` | Drop to CLI |

**CLI naming gotcha.** The canonical subcommand for balance is `account status` (alias `acc status`). `account balance` and `account credits` both fall through to parent help — they are not valid subcommands. Tell the user `status` if they go looking for `balance`.

**CLI scripting note.** Append `--json` to any of the above for machine-readable output. Useful when Claude Code is parsing the response inside a longer workflow.

**Bundled skills note.** The bundled skills drive the CLI under the hood (`higgsfield-generate` wraps `generate create`; photoshoot, marketplace cards, Soul ID and websites have their own CLI command groups); they don't expose a parallel preflight slash command. Same auth, same workspace, so a one-line CLI cost check before the slash invocation is the cleanest pattern: `higgsfield generate cost <model> --prompt "..." [...flags]`, then `/higgsfield:generate`.

**Marketing Studio caveat — now unresolved.** The 2026-05 MCP tool descriptions said `get_cost` is not supported for Marketing Studio models. The 2026-09-26 `generate_video` schema no longer states that exception (its `get_cost` field reads only "return the cost in credits for this generation without submitting any job"). An absent caveat is not proof it works, and it has not been tried: try `get_cost: true`, and keep `balance` before-and-after as the check. Detail: `../higgsfield-marketing-studio/SKILL.md` § 7.

**Adjustments block (MCP).** When `get_cost: true` is set on `generate_image` / `generate_video`, the response includes an `adjustments` object that surfaces which unset optional params the server defaulted (e.g. `mode=std`, `sound=on`). Surface these to the user alongside the credit cost — they are part of the preflight contract. The CLI's `generate cost --json` response does not currently include adjustments; if symmetry matters to the user, recommend the MCP path or pass each optional param explicitly on the CLI.

### Plan tier, not surface, controls queue priority

All four surfaces share one credit pool and one job queue. Queue priority is a function of the user's paid Higgsfield plan tier (Plus / Ultra / Business / Team), not the choice of MCP vs CLI vs bundled skills vs paste-into-website. Surface choice affects ergonomics and authentication shape, not queue position:

- **CLI** is preferred for headless / CI / long-running batches because it uses long-lived API tokens rather than interactive OAuth round-trips. Per Higgsfield's own guidance on `higgsfield.ai/mcp`: "If you are using Claude Code or Codex, it's better to use the CLI."
- **MCP** is preferred for conversational generation inside claude.ai web, the Claude desktop app, or Claude Code in interactive mode — single OAuth, no token management.
- **Bundled skills** sit on top of the CLI; they inherit its auth model and tier behavior.

When a free-tier user reports MCP timeouts or queue stalls, the answer is plan tier, not "switch surfaces." Recommend upgrading the plan if iteration volume justifies it; recommend the CLI only if the workload is headless or non-conversational.

### When to surface preflight in this skill's output

Add a preflight line to the output block whenever:

- The user has signaled they are about to execute (CLI / MCP / bundled skills mentioned).
- The model is video-class (Veo, Kling, Sora-2, Seedance, Hailuo, DoP) OR a high-cost image model (Nano Banana Pro at higher resolutions, GPT Image 2 at 4K).
- The user has named a budget constraint or credit-optimization concern.
- The work is iteration-heavy by structure (Cinema Studio multi-shot, Two-Tool Refinement Pipeline, multi-character anchor template).

Skip preflight surfacing for one-off image generation on a cheap model, or when the user is clearly just exploring vocabulary without intent to execute.

### Iteration-budget projection (production-benchmarks tie-in)

When surfacing preflight cost, contextualize it against the acceptance-rate anchors in `production-benchmarks.md`. A single Kling 3.0 8s generation at 16:9 std mode costs 16 credits; the 1.5% video-acceptance anchor implies roughly 67 attempts on average to land one keeper — at 16 credits per attempt, that's about 1,000 credits per finished shot. Multiply by shot count for multi-shot sequences. The discipline isn't to surface the multiplied number every time — it's to make sure the user is reading single-shot cost in the context of iteration cost, not as an absolute. This is the same anchor that justifies the preflight pattern in the first place: iteration burn is the work, not the failure, and preflight is how you keep the burn visible.

---

## How our skill fits in

```
USER REQUEST
   ↓
[ our skill — higgsfield-ai-prompt-skill ]
   • routes to the right sub-skill (prompt / camera / soul / cinema /
     seedance / etc.)
   • applies MCSLA (Model · Camera · Subject · Look · Action)
   • uses named platform vocabulary from `../../vocab.md`
   • appends shared negative constraints
   • runs `../../scripts/seedance_lint.py` preflight (Seedance prompts only)
   • produces a production-grade prompt
   ↓
[ hand-off to whatever execution surface the user has ]
   ↓
EXECUTION SURFACE (one of):
   • Higgsfield CLI — `higgsfield generate create <model_id> --prompt "..." --wait`
   • Higgsfield MCP — Claude calls the connector's generation tool
   • Higgsfield's bundled skills — `higgsfield-generate` takes the prompt
     and formats the underlying call
   • None — user copies the prompt into higgsfield.ai directly
   ↓
RESULT
```

For **direct generation**, the prompt comes from us and the execution from one of the four surfaces above. The exception is a request that is squarely one of Higgsfield's own workflows — there the workflow owns its prompt engine and this library supplies inputs and checks instead (§ Higgsfield's bundled workflows).

---

## Coexistence rules

1. **Our skill produces the prompt for direct generation.** Regardless of which execution surface the user has installed, prompt construction for a direct `generate_*` / `generate create` call is this skill's job. MCSLA structure, named-vocabulary discipline, anti-bombast register, and the negative-constraints appendage all stay in our lane. If their bundled skill or their MCP tool wants a `--prompt` string for a direct generation, that string is our output, not theirs.

2. **Outside their own workflows, their tools don't produce the prompt logic.** Do not let `higgsfield-generate` or a bare MCP generation tool invent prompts on its own; if it offers to generate prompt text from a brief, route the brief through our skill first, then pass the resulting prompt down. **The exception is explicit:** their bundled workflows and backend-enhanced skills (product photoshoot, marketplace cards, thumbnails, character sheets …) *are* prompt engines by design. When a request is squarely one of those, follow § Higgsfield's bundled workflows — contribute inputs, don't build a competing pipeline.

3. **Do not duplicate their model-list call.** Their CLI exposes `higgsfield model list --json`. This skill maintains its own curated model-selection criteria in `../../model-guide.md` and `../../image-models.md`. Do not shell out to `model list` from this skill — the curation is the value. If the user needs ground-truth current model IDs (e.g., a new model just shipped), point them to their CLI; do not try to keep our files in sync at runtime.

4. **Do not bypass their CLI by calling `api.higgsfield.ai` directly.** This is a hard rule. Auth, uploads, retries, polling, and rate-limit handling are non-trivial and live inside their CLI. This skill never shell-curls the API or writes code that calls the API directly. If the user has the CLI, route through it; if not, the user pastes into higgsfield.ai by hand.

5. **Defer to their skill on execution flags.** If the user has `higgsfield-generate` loaded and asks for, say, a Marketing Studio ad, construct the prompt body here, then hand the prompt text off. Do not try to remember their `--avatars`, `--product_ids`, `--hook_id`, `--mode`, or `--format-id` syntax — that is their domain and their version-to-version churn. We do the prompt; they do the invocation.

---

## Higgsfield's bundled workflows

`[OFFICIAL — Higgsfield MCP tool schema + server instructions, 2026-09-26]` The connector
ships multi-step workflows, loaded with `get_workflow_instructions` (no argument lists the
catalog; `{ workflow: "<name>" }` loads one) and their files with
`get_workflow_bundle_file`. The captured catalog names **16** workflows:

| Workflow | Version | Scope (condensed from the catalog) |
|---|---|---|
| `ad-multiplier` | 1.4 | Many independently edited versions of ONE supplied 4–30s video — replace / add / remove people, products, objects, clothing, backgrounds, targeted on-screen text — preserving motion, framing, cuts, timing, aspect, audio. Not for simple edits |
| `brand-asset-creation` | 1.1 | Logos, identities, brand kits, mockups, merch, packaging, decks, social graphics; deterministic logo recolor / export |
| `character-sheet` | 1.0 | Character reference / model sheets / turnarounds / expression sheets; slot-based prompt with an "anti-AI / unretouched" realism engine; styles photoreal-unretouched / editorial / anime-2D / 3D-stylized / game-concept |
| `faceless-video` | 2.4 | Finished multi-scene narrator-led channel video (Explainer, History, Kids, Picture Story, Fairy Tale & Myth) |
| `narrator` | 1.1 | Takes fitted to video windows, long-form locked-voice reads, "put me in this video" presenter compositing |
| `product-photoshoot` | 1.0 | Packshots, lifestyle, hero banners, carousels, static ad packs, virtual try-on, CGI-style product stills |
| `subtitles` | 1.0 | Burn captions into the pixels only |
| `thumbnail-generation` | 1.3 | YouTube / Instagram thumbnails; 16 frameworks; 4K routing across `nano_banana_pro` / `gpt_image_2` / seedream |
| `ugc-product-video` · `ugc-review-video` · `ugc-try-on-video` · `ugc-tutorial-video` · `ugc-unboxing-video` · `ugc-website-video` | 1.0–1.1 | UGC / creator-style short videos by format |
| `video-editing` | 1.0 | **Higgsedit** — cuts, trims, soundtrack, layouts, animated text, shaders, overlays, title cards on supplied footage |
| `website-builder-flow` | — | Websites, web apps, browser games on Higgsfield |

The connector's own routing, verbatim where it binds: *"Unless an explicit preset selected
its recipe, for multi-step videos call get_workflow_instructions first (with no
argument)."* · *"For multiple edits of one clip call get_workflow_instructions with {
workflow: "ad-multiplier" } first."* · *"For character sheets call get_workflow_instructions
with { workflow: "character-sheet" }"* · *"Generate a character sheet only on an explicit
request."* Workflow versions move independently — list the catalog live before quoting a
workflow's scope.

### Coexistence rules for Higgsfield's workflows

1. **When the request is squarely a workflow's job and the user is on the connector, the
   workflow runs it.** The connector routes those requests to its workflow before model
   browsing or direct generation. Do not build a competing prompt pipeline beside it.
2. **This library contributes what the workflow does not own** — the thinking upstream of
   the run (who the character is, what the scene is for, the hook, the style laws, the audio
   plan) and the checks downstream of it (scoring, analysis, cut review). It also still
   writes direct-generation prompts when the user wants control outside the workflow, or is
   not on the connector.
3. **Hand-offs stay inside Higgsfield and this library.** Every route below ends at one of
   Higgsfield's own workflows / skills or at one of this library's sub-skills. Never route the
   work to an outside product.
4. **Respect the connector's gates** — a character sheet only on an explicit request; the
   `ad-multiplier` workflow only for independent variants (a single object swap is Genjutsu —
   `../higgsfield-marketing-studio/SKILL.md` § 14).

| Request is squarely… | Higgsfield's workflow owns | This library adds | Our sub-skill |
|---|---|---|---|
| "Multiply my ad" / many versions of one ad | `ad-multiplier` — the multi-version run | Per-version edit text in the Seedance 2.5 `video_edit` grammar; a one-variable-per-version plan; ranking the versions | `higgsfield-marketing-studio` § 14 · `higgsfield-repurpose` |
| A character sheet / turnaround / expression sheet | `character-sheet` — the sheet prompt and its realism engine | Who the character is (9-question sheet, visual DNA), then the identity lock and performance for the shots that follow | `higgsfield-character-design` · `higgsfield-soul` · `higgsfield-acting` |
| A thumbnail or video cover | `thumbnail-generation` — frameworks, model routing | Composition vocabulary if the user wants to direct the frame by hand | `higgsfield-image-shots` |
| A UGC-style product / review / try-on / tutorial / unboxing / website video | the matching `ugc-*` workflow | Marketing Studio preset register, hook + setting choice, avatar constraints — when the user wants to write it through Marketing Studio instead | `higgsfield-marketing-studio` · `higgsfield-content-factory` |
| A finished faceless channel video | `faceless-video` — the end-to-end build | A structural audit of the script's scenes before the run spends credits | `higgsfield-scene-engine` |
| A narrator take, a locked-voice read, a presenter composite | `narrator` | Voice choice, cloned voices, voice change | `higgsfield-audio` § Voice change and voice cloning |
| Product photography / packshots / static ad packs | `product-photoshoot` | A product reference sheet; static-ad recreation when the user wants to author the prompt | `higgsfield-gpt-image-2` · `higgsfield-cinema` (`../higgsfield-cinema/references/reference-sheet-types.md`) |
| A logo, brand kit, brandbook, deck, merch | `brand-asset-creation` | A style anchor or moodboard if the brand look needs directing | `higgsfield-moodboard` |
| Burned-in captions | `subtitles` | Nothing — in-generation text is a different job | (`templates/text-overlays/` covers text rendered *by* the model) |
| Cuts, trims, soundtrack, titles on supplied footage | `video-editing` (Higgsedit) | Where the cuts land on the music | `higgsfield-audio` § Cutting to music |
| A website, web app or browser game | `website-builder-flow` | Nothing | — |

---

## Naming overlap — `higgsfield-soul-id` (theirs) vs `higgsfield-soul` (ours)

Higgsfield's bundled-skills repo has a Soul training skill, and this library has a sub-skill named `higgsfield-soul` at `../higgsfield-soul/SKILL.md`. Their skill was named `higgsfield-soul` at v0.3.0 — an exact name collision — and is **`higgsfield-soul-id`** (`/higgsfield:soul-id`) in the 0.12.0 README. The directory names no longer collide, but both still trigger on user phrases like "Soul" or "Soul ID", so the disambiguation still matters.

| | Theirs (`higgsfield-soul-id`) | Ours (`../higgsfield-soul/SKILL.md`) |
|---|---|---|
| Job | Train a Soul Character (face-faithful identity model) | Prompt-side character consistency discipline |
| Input | 5–20 face photos plus a name | Free-form user request |
| Output | A `reference_id` consumable by Soul-aware generation models | Production-grade prompt with Character Anchor Block, Identity/Motion separation, Two-Tool Refinement Pipeline guidance |
| Invocation | `/higgsfield:soul-id` slash command (`/higgsfield:soul` on installs older than the rename back), or `higgsfield soul-id create ...` from the CLI | Auto-loaded by our root dispatcher when character consistency is the topic |
| Owns | Training run, polling, returning the `reference_id` | MCSLA structure for Soul prompts, Character Sheet creation, the 10-attribute pre-shot lock, multi-form state tracking |

The rule is sequential, not overlapping. Theirs trains the identity. Ours constructs the prompt that uses the trained identity.

- When the user says "create my Soul" or "train a Soul ID from these photos" — that is **their** `higgsfield-soul-id`'s job. Hand off; do not try to do it here.
- When the user says "write me three Soul prompts for scenes A / B / C using my `reference_id`" — that is **our** `../higgsfield-soul/SKILL.md`'s job. Construct the prompts; do not try to run training.

If the user is ambiguous ("help me with Soul"), ask which step they're on: training the identity, or prompting with an already-trained identity. One short question; do not split across multiple rounds.

---

## Detection guidance

Before deciding whether to attach a handoff line, look for these signals that the Higgsfield stack is present in the current environment:

- **Direct user statement** — "I have the CLI installed", "I'm using their MCP", "I ran `npx skills add higgsfield-ai/skills`".
- **Available MCP tools** — the current Claude session exposes tools whose names mention Higgsfield generation. Suggests the MCP connector is attached.
- **Skill files on disk** — a `SKILL.md` for any of their skills in § The bundled skills at 0.12.0 (`higgsfield-generate`, `higgsfield-soul-id`, `higgsfield-product-photoshoot`, `higgsfield-brandkit` …) visible in the agent's skill directory. Suggests their bundled skills are installed. (A `higgsfield-soul` directory could be theirs from an older install or ours — ours carries `metadata.parent: higgsfield` in its frontmatter.)
- **Command output or slash invocations** — user pastes output from `higgsfield ...` or uses `/higgsfield:<skill>` (`/higgsfield:generate`, `/higgsfield:soul-id`, `/higgsfield:product-photoshoot` …).
- **Connector workflow tools** — the session exposes `get_workflow_instructions` / `get_workflow_bundle_file`. Suggests the MCP connector with its bundled workflows.
- **In Claude Code specifically** — `which higgsfield` returning a path, or `higgsfield --version` returning a version string.

If none of these signals are present, the user is on the paste-into-higgsfield.ai path. That is the default behavior of this skill — deliver the prompt, no handoff line needed.

---

## Handoff templates

When one or more surfaces are detected, append one short line after the prompt. Keep the register plain — these are pointers, not promotions.

- **CLI present:**
  `If you want, you can run this directly with: higgsfield generate create <model_id> --prompt "<prompt above>" --wait`
- **MCP present:**
  `You can invoke this via the Higgsfield connector — pass the prompt above as the prompt argument.`
- **Bundled skills present:**
  `If you want to run this, their higgsfield-generate skill can take this prompt as its --prompt argument.`
- **The request is squarely one of the connector's workflows:**
  `This is what Higgsfield's <workflow> workflow is built for — load it through the connector (get_workflow_instructions) and follow it; here is what to give it: <the inputs this library produced>.`

If multiple surfaces are present, pick the one that fits the user's stated workflow. Do not list them all. If none are present, do not append a handoff line at all.

---

## Seedance preflight integration

The one place where this skill's tooling earns its keep inside the integrated flow is `../../scripts/seedance_lint.py`. Seedance 2.0's content filter rejects instant-fail prompts before they reach the GPU, and the user gets charged credits regardless of whether the rewrite was the issue. The linter catches the predictable rejection patterns at prompt-construction time, before submission.

When the CLI is present AND the prompt being constructed is for Seedance 2.0 or Seedance Pro, append a recommendation:

> `Run python3 scripts/seedance_lint.py "<prompt>" before submitting to catch content-filter rejections. The filter is voice-based, not a keyword blacklist — see ../higgsfield-seedance/SKILL.md for the full diagnostic.`

This is a recommendation to the user. This skill does not run the linter on the user's behalf and does not require the linter to have run before delivering the prompt.

---

## What this sub-skill does NOT do

- Does not install, configure, or troubleshoot the Higgsfield CLI, MCP connector, or bundled skills. Point users to the upstream repos linked above for any of that.
- Does not replicate their model catalog — no equivalent of `higgsfield model list` runs from this skill.
- Does not run their CLI commands on the user's behalf. No `Bash` calls into `higgsfield generate create`, `higgsfield soul-id create`, or any other binary invocation.
- Does not absorb their skills' logic. `higgsfield-generate` knows how to format Marketing Studio invocations; this skill does not.
- Does not re-implement their workflows. When the connector's routing says a request belongs to one of its workflows, the agent in the session loads it with `get_workflow_instructions` and follows it — this library never restates a workflow's recipe; it supplies the inputs. The workflow's own file is the authority, and it versions independently.
- Does not create a dependency on their stack being present. The full prompt-skill library remains functional standalone — the four execution surfaces (CLI, MCP, bundled skills, paste-into-website) are all valid, including the last one.

---

## Related sub-skills

- `../higgsfield-prompt/SKILL.md` — produces the prompt text that gets handed off to any execution surface.
- `../higgsfield-workspaces/SKILL.md` — handles the upstream "which Higgsfield workspace fits my task" question, which is settled before any execution surface comes into play.
- `../higgsfield-seedance/SKILL.md` — pairs with the `../../scripts/seedance_lint.py` preflight recommendation above; covers the full filter diagnostic and prompt-mode router.
- `../higgsfield-assist/SKILL.md` — credit-optimization questions apply regardless of execution surface; route credit/plan questions there.
- `../higgsfield-soul/SKILL.md` — our Soul prompt-construction sub-skill. Read the Naming overlap section above before routing — theirs trains, ours prompts.
- `../higgsfield-3d/SKILL.md` — `generate_3d` models and 3D Jutsu scenes (their `higgsfield-generate` also covers 3D execution).
- `../higgsfield-repurpose/SKILL.md` — Shorts Studio, Clipify, Virality Predictor, Video Analysis, with the paid / free split.
