---
name: higgsfield-stack
description: "Use when the user mentions the Higgsfield CLI (binaries `higgsfield` / `higgs` / `hf`, `higgsfield auth login`, `higgsfield generate create`, the `@higgsfield/cli` npm package), the Higgsfield MCP custom connector (`mcp.higgsfield.ai/mcp`), Higgsfield's bundled skills (`higgsfield-generate` / `higgsfield-soul` / `higgsfield-product-photoshoot` invoked as `/higgsfield:generate` etc.), or asks how this skill coexists with those tools (`do I need both`, `how does this work with the CLI/MCP/skills`)."
user-invocable: true
metadata:
  tags: [higgsfield, stack, cli, mcp, official-skills, coexistence, handoff, environment]
  version: 1.2.1
  updated: 2026-05-18
  parent: higgsfield
---

# Higgsfield Stack — Coexistence With Official Tooling

## What this sub-skill is for

"The Higgsfield stack" means Higgsfield's own official execution tooling: their command-line interface (CLI), their custom MCP connector for claude.ai and the Claude desktop app, and their three bundled skills (`higgsfield-generate`, `higgsfield-soul`, `higgsfield-product-photoshoot`). Any one of those tools — or any combination — may be present in the user's environment alongside this prompt skill. This sub-skill documents how the two surfaces coexist, what each one owns, and how a clean handoff looks.

The core principle is a layer split. This skill is the prompt-construction + production-discipline layer: MCSLA structure, named platform vocabulary, model selection criteria, Seedance preflight, Cinema Studio depth, Soul Character Anchor Block, Two-Tool Refinement Pipeline guidance, anti-bombast register, shared negative constraints. Their stack is the execution layer: authentication, file uploads, job submission, polling, retries, returning a result URL. Different jobs, no overlap. Our skill never invokes their CLI; their stack never invents prompt logic. The user gets one prompt from us and one execution path from them.

---

## The three official surfaces

| Surface | What it is | Detection signals | Best fit |
|---|---|---|---|
| **Higgsfield CLI** | Binary distributed at https://github.com/higgsfield-ai/cli. Binary names: `higgsfield`, `higgs`, `hf`. Install via `curl -fsSL https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh \| sh` or `brew install higgsfield-ai/tap/higgsfield`. Auth via `higgsfield auth login` (device flow). | User types `higgsfield`, `higgs`, or `hf` in conversation; user says "I have the CLI installed"; user pastes output from `higgsfield ... --json` | Claude Code, Codex, Cursor, or any terminal-native agent. Per Higgsfield's own guidance: if the user is in Claude Code or Codex, prefer the CLI over the MCP. |
| **Higgsfield MCP** | Custom connector at https://mcp.higgsfield.ai/mcp. Separate product from the CLI. Installed in claude.ai or the Claude desktop app via Settings → Connectors → Add custom connector. | User is in claude.ai web or the Claude desktop app (not a terminal); user mentions "the connector" or "MCP" or `mcp.higgsfield.ai`; the current Claude session has tools whose names mention Higgsfield generation. | claude.ai web, Claude desktop app, environments without a terminal. |
| **Higgsfield bundled skills** | Skill repo at https://github.com/higgsfield-ai/skills (v0.3.0). Three skills: `higgsfield-generate`, `higgsfield-soul`, `higgsfield-product-photoshoot`. Install via `npx skills add higgsfield-ai/skills`. Invoke as `/higgsfield:generate`, `/higgsfield:soul`, `/higgsfield:product-photoshoot`. | Skill files matching those names visible in the agent's skill directory; user invokes one of those slash commands; user mentions installing `higgsfield-ai/skills`. | Agents that consume Cowork-style skill bundles. All three skills drive the CLI under the hood — they are workflow/transport guidance, not prompt engineering. |

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
| 1. Schema verify | `models_explore(action="get", model_id="<model>")` | `higgsfield model get <model>` |
| 2. Cost estimate | `generate_image` / `generate_video` with `get_cost: true` | `higgsfield generate cost <model> [--param value]...` |

**Failure mode this prevents — plausibility-over-verification.** The model knows enough about Higgsfield (and about CLIs generally, and about MCP schemas generally) to produce a *plausible* preflight call. Plausibility is not validity. Plausibility says `--aspect-ratio 2.35:1` because hyphenated flags and cinematic anamorphic ratios are both prevalent in training data. Verification says `--aspect_ratio 16:9` because that is what `higgsfield model get kling3_0` returns. The discipline is to run the verification command that is sitting right there, not to trust the plausible answer. This pattern recurs across surfaces — see `DISCIPLINE.md` Tier 1 § Plausibility-over-verification for the cross-cutting framing.

### Verified preflight surfaces

| Concern | MCP | CLI | Bundled skills |
|---|---|---|---|
| Schema verification (param enum, ranges, defaults) | `models_explore(action="get", model_id="<model>")` | `higgsfield model get <model>` | Drop to CLI for the verify |
| Cost estimate (no job submitted) | `generate_image` / `generate_video` with `get_cost: true` | `higgsfield generate cost <model> [--param value]...` | Drop to CLI for the check, then run the slash command |
| Credit balance + plan + email | `balance` tool | `higgsfield account status` | Drop to CLI |
| Recent transactions (newest first) | `transactions` tool | `higgsfield account transactions --size N` | Drop to CLI |

**CLI naming gotcha.** The canonical subcommand for balance is `account status` (alias `acc status`). `account balance` and `account credits` both fall through to parent help — they are not valid subcommands. Tell the user `status` if they go looking for `balance`.

**CLI scripting note.** Append `--json` to any of the above for machine-readable output. Useful when Claude Code is parsing the response inside a longer workflow.

**Bundled skills note.** The bundled skills (`higgsfield-generate`, `higgsfield-soul`, `higgsfield-product-photoshoot`) wrap `generate create` under the hood; they don't expose a parallel preflight slash command. Same auth, same workspace, so a one-line CLI cost check before the slash invocation is the cleanest pattern: `higgsfield generate cost <model> --prompt "..." [...flags]`, then `/higgsfield:generate`.

**Marketing Studio caveat.** Per Higgsfield MCP tool descriptions, `get_cost` is not supported for marketing studio models. For those, run the job and read cost from the result, or check `balance` before and after.

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
   • runs `../../seedance_lint.py` preflight (Seedance prompts only)
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

The prompt always comes from us. The execution always comes from one of the four surfaces above. Nothing crosses the boundary in either direction.

---

## Coexistence rules

1. **Our skill always produces the prompt.** Regardless of which execution surface the user has installed, prompt construction is this skill's job. MCSLA structure, named-vocabulary discipline, anti-bombast register, and the negative-constraints appendage all stay in our lane. If their bundled skill or their MCP tool wants a `--prompt` string, that string is our output, not theirs.

2. **Their skills, CLI, and MCP never produce the prompt logic.** Do not let `higgsfield-generate` or any MCP tool invent prompts on its own. If it offers to generate prompt text from a brief, route the brief through our skill first, then pass the resulting prompt down.

3. **Do not duplicate their model-list call.** Their CLI exposes `higgsfield model list --json`. This skill maintains its own curated model-selection criteria in `../../model-guide.md` and `../../image-models.md`. Do not shell out to `model list` from this skill — the curation is the value. If the user needs ground-truth current model IDs (e.g., a new model just shipped), point them to their CLI; do not try to keep our files in sync at runtime.

4. **Do not bypass their CLI by calling `api.higgsfield.ai` directly.** This is a hard rule. Auth, uploads, retries, polling, and rate-limit handling are non-trivial and live inside their CLI. This skill never shell-curls the API or writes code that calls the API directly. If the user has the CLI, route through it; if not, the user pastes into higgsfield.ai by hand.

5. **Defer to their skill on execution flags.** If the user has `higgsfield-generate` loaded and asks for, say, a Marketing Studio ad, construct the prompt body here, then hand the prompt text off. Do not try to remember their `--avatars`, `--product_ids`, `--hook_id`, `--mode`, or `--format-id` syntax — that is their domain and their version-to-version churn. We do the prompt; they do the invocation.

---

## Naming collision — `higgsfield-soul` (theirs) vs `higgsfield-soul` (ours)

Higgsfield's bundled-skills repo includes a skill named `higgsfield-soul` (renamed from `higgsfield-soul-id` in their v0.3.0). This sub-skill library also has a sub-skill named `higgsfield-soul` at `../higgsfield-soul/SKILL.md`. Same name, different jobs. The collision is real and worth disambiguating up front because both will trigger on user phrases like "Soul" or "Soul ID".

| | Theirs (`higgsfield-soul`) | Ours (`../higgsfield-soul/SKILL.md`) |
|---|---|---|
| Job | Train a Soul Character (face-faithful identity model) | Prompt-side character consistency discipline |
| Input | 5–20 face photos plus a name | Free-form user request |
| Output | A `reference_id` consumable by Soul-aware generation models | Production-grade prompt with Character Anchor Block, Identity/Motion separation, Two-Tool Refinement Pipeline guidance |
| Invocation | `/higgsfield:soul` slash command, or `higgsfield soul-id create ...` from the CLI | Auto-loaded by our root dispatcher when character consistency is the topic |
| Owns | Training run, polling, returning the `reference_id` | MCSLA structure for Soul prompts, Character Sheet creation, the 10-attribute pre-shot lock, multi-form state tracking |

The rule is sequential, not overlapping. Theirs trains the identity. Ours constructs the prompt that uses the trained identity.

- When the user says "create my Soul" or "train a Soul ID from these photos" — that is **their** `higgsfield-soul`'s job. Hand off; do not try to do it here.
- When the user says "write me three Soul prompts for scenes A / B / C using my `reference_id`" — that is **our** `../higgsfield-soul/SKILL.md`'s job. Construct the prompts; do not try to run training.

If the user is ambiguous ("help me with Soul"), ask which step they're on: training the identity, or prompting with an already-trained identity. One short question; do not split across multiple rounds.

---

## Detection guidance

Before deciding whether to attach a handoff line, look for these signals that the Higgsfield stack is present in the current environment:

- **Direct user statement** — "I have the CLI installed", "I'm using their MCP", "I ran `npx skills add higgsfield-ai/skills`".
- **Available MCP tools** — the current Claude session exposes tools whose names mention Higgsfield generation. Suggests the MCP connector is attached.
- **Skill files on disk** — a `SKILL.md` for `higgsfield-generate`, `higgsfield-soul` (theirs, not ours), or `higgsfield-product-photoshoot` visible in the agent's skill directory. Suggests their bundled skills are installed.
- **Command output or slash invocations** — user pastes output from `higgsfield ...` or uses `/higgsfield:generate`, `/higgsfield:soul`, `/higgsfield:product-photoshoot`.
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

If multiple surfaces are present, pick the one that fits the user's stated workflow. Do not list all three. If none are present, do not append a handoff line at all.

---

## Seedance preflight integration

The one place where this skill's tooling earns its keep inside the integrated flow is `../../seedance_lint.py`. Seedance 2.0's content filter rejects instant-fail prompts before they reach the GPU, and the user gets charged credits regardless of whether the rewrite was the issue. The linter catches the predictable rejection patterns at prompt-construction time, before submission.

When the CLI is present AND the prompt being constructed is for Seedance 2.0 or Seedance Pro, append a recommendation:

> `Run python3 seedance_lint.py "<prompt>" before submitting to catch content-filter rejections. The filter is voice-based, not a keyword blacklist — see ../higgsfield-seedance/SKILL.md for the full diagnostic.`

This is a recommendation to the user. This skill does not run the linter on the user's behalf and does not require the linter to have run before delivering the prompt.

---

## What this sub-skill does NOT do

- Does not install, configure, or troubleshoot the Higgsfield CLI, MCP connector, or bundled skills. Point users to the upstream repos linked above for any of that.
- Does not replicate their model catalog — no equivalent of `higgsfield model list` runs from this skill.
- Does not run their CLI commands on the user's behalf. No `Bash` calls into `higgsfield generate create`, `higgsfield soul-id create`, or any other binary invocation.
- Does not absorb their skills' logic. `higgsfield-generate` knows how to format Marketing Studio invocations; this skill does not.
- Does not create a dependency on their stack being present. The full prompt-skill library remains functional standalone — the four execution surfaces (CLI, MCP, bundled skills, paste-into-website) are all valid, including the last one.

---

## Related sub-skills

- `../higgsfield-prompt/SKILL.md` — produces the prompt text that gets handed off to any execution surface.
- `../higgsfield-workspaces/SKILL.md` — handles the upstream "which Higgsfield workspace fits my task" question, which is settled before any execution surface comes into play.
- `../higgsfield-seedance/SKILL.md` — pairs with the `../../seedance_lint.py` preflight recommendation above; covers the full filter diagnostic and prompt-mode router.
- `../higgsfield-assist/SKILL.md` — credit-optimization questions apply regardless of execution surface; route credit/plan questions there.
- `../higgsfield-soul/SKILL.md` — our Soul prompt-construction sub-skill. Read the Naming collision section above before routing — theirs trains, ours prompts.
