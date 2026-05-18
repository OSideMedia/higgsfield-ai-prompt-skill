# Higgsfield Skill Library — Discipline Patterns

## What this is

Cross-cutting discipline patterns observed in the higgsfield skill library and in a single Higgsfield-team-adjacent author bundle that systematized AI-cinema practice during the 2026 Cannes production cycle. The author bundle (banana-pro-director, cinema-worldbuilder, screenwriter-skill, shotlist-builder, seedance-2-pro-director) is used inside the Higgsfield production team's actual pipeline. The patterns here proved out under real production pressure — five skills, fifteen people, fourteen days, one 90-minute AI feature shipped for Cannes — and recur in higgsfield's own codebase as independently-evolved practice.

Three tiers: workflow (how to author prompts), output (what to emit), architectural (how multi-step work composes). Each pattern points to a concrete demonstration in higgsfield's existing codebase — observed practice, not aspirational claims.

For a new sub-skill: check **Tier 1** if it involves multi-step
authoring, **Tier 2** if it produces output, **Tier 3** if it
composes multiple stages. Pick what applies.

## Tier 1 — Workflow Discipline

### Pre-Prompt Confirmation Gate

Confirm intent in short form before composing a long prompt;
when stuck, prefer one narrow question over three open-ended.

**When to apply:** Output longer than a few sentences, or any sub-skill triggering expensive downstream work.

**Demonstrated in:** root `SKILL.md` § Workflow → Full Path —
Production Requests (confirm-before-generating + anti-fragmentation
rule).

### Explicit-Stop Between Phases

Multi-phase workflows don't collapse into one response; each
phase produces an artifact the next phase consumes.

**When to apply:** Stateful loops where intermediate artifacts need user confirmation.

**Demonstrated in:** `skills/higgsfield-pipeline/SKILL.md` §
Pipelines A-E — stage-based artifact handoff; Pipeline Pitfall 1
encodes the don't-skip-ahead rule explicitly.

### Inventory-Extraction Checklist Before Composing

Silently catalog what the user provided — who / where / doing
what / with what camera / mood — before composing.

**When to apply:** Sub-skills authoring prompts from free-form briefs.

**Demonstrated in:** `skills/higgsfield-prompt/SKILL.md` § The
Pre-Prompt Checklist — 5-question inventory before writing.

### Iteration-is-craft

Iteration burn is the work, not the failure. Production-grade AI-cinema
runs at roughly 1% image-acceptance and 1.5% video-acceptance rates;
the iteration loop IS the craft, and treating each rejected take as a
failure ends the project on Day 7.

**When to apply:** Any sub-skill that produces generative output; any
budgeting or planning conversation; any post-clip diagnostic.

**Demonstrated in:** `production-benchmarks.md` § Acceptance-rate
anchors (quadruple-confirmed 1.0% / 1.5% rates) + `skills/higgsfield-
prompt/SKILL.md` § The Iteration Rule — Change One Variable at a Time.

### Lock-before-generate

Lock subject, scene, camera, lighting, and coverage decisions BEFORE
prompting — not during. Decisions made during the iteration loop drift
from the original intent; decisions made before lock as anchors that
the iteration loop tests against.

**When to apply:** Any multi-shot or multi-character output; any work
that needs to hold consistency across cuts.

**Demonstrated in:** `skills/higgsfield-soul/SKILL.md` § Character
Anchor Block (10-attribute pre-shot lock) + `skills/higgsfield-
seedance/SKILL.md` § Frame Coordinate System + § Per-Image Role
Convention.

### Falsifiable Success Criteria

Define what "good output" looks like in falsifiable terms BEFORE
prompting, so the iteration loop has a stopping criterion. The
discipline prevents the post-hoc rationalization failure mode —
claiming success regardless of outcome because no specific test was
committed to up front.

**When to apply:** Any project-level or scene-level work where
"finished" is not self-evident.

**Demonstrated in:** `production-benchmarks.md` § Falsifiable AI-
cinema success criteria (5-criterion rubric committed before
generation began).

## Tier 2 — Output Discipline

### Visual-Marker-Only Output Discipline

Describe characters and objects by visible markers (clothing,
build, posture, action, hair), not proper names, age labels, or
unobservable attributes. Visual markers carry across regenerations.

**When to apply:** Any prompt for image or video generation.

**Demonstrated in:** `skills/higgsfield-prompt/SKILL.md` §
Seedance 2.0 Engine Constraints → Age-blind character rule.

### Triple-Redundant Runtime

Runtime appears in title, meta header, and per-shot timing
labels — all three must agree, per-shot labels must sum to total.

**When to apply:** Multi-shot or time-anchored output.

**Demonstrated in:** `skills/higgsfield-seedance/SKILL.md` §
Runtime arithmetic for multi-shot prompts.

### Single-Variable Iteration

Change exactly one variable per regeneration. Multi-variable
iteration makes diagnosis impossible.

**When to apply:** Iteration on close-but-not-right generations.

**Demonstrated in:** `skills/higgsfield-prompt/SKILL.md` § The
Iteration Rule — Change One Variable at a Time + 6-Pass Diagnostic.

### BAD/GOOD/GREAT

Show output gradients explicitly — BAD, GOOD, GREAT examples
side-by-side — so the reader sees the difference, not just hears
about it. The contrast is what teaches; a single GOOD example without
a BAD comparison reads as one possibility rather than a chosen
direction.

**When to apply:** Any template, vocabulary, or pattern entry where
quality has a recognizable gradient.

**Demonstrated in:** `templates/seedance/top-down-map.md` BAD/GOOD/
GREAT section (pre-visualization gradient) + `templates/seedance/
multi-character-anchor.md` BAD/GOOD/GREAT section (multi-character
anchor block gradient).

### Skill-with-baked-context

Skills should bake the context they need (named tools, decision
criteria, anti-pattern catalog, worked examples) rather than asking
the user to provide context the skill could have. The user supplies
the request; the skill supplies the production knowledge.

**When to apply:** Any sub-skill design that has a recurring
operational context (tool selection, failure modes, workflow
positioning).

**Demonstrated in:** `image-models.md` § Nano Banana Pro Workflow
positioning (two-tool pipeline routing baked in) + `skills/
higgsfield-soul/SKILL.md` § Two-Tool Refinement Pipeline (~600 + ~200
generations anchor baked into pipeline framing).

### Anti-Bombast

Production-direction register. Avoid marketing voice, performative
urgency, fake confidence, and adjective stacks that describe what the
output should *be* rather than what the prompt should *do*. Replace
`epic`, `beautiful`, `cinematic masterpiece`, `ultra realistic`,
`dramatic` with named physical mechanisms (`low-angle 35mm anamorphic
medium shot`, `warm practical key light from screen-left`).

**When to apply:** Any prompt-construction surface; any documentation
the model or the user reads.

**Demonstrated in:** `vocab.md` § Scene-physics lighting (replaces
stylistic adjectives with named physical mechanisms) + the
seedance-2-pro-director skill's anti-empty-words discipline
(`Avoid: epic, beautiful, cinematic masterpiece, ultra realistic,
dramatic`).

#### Anti-Bombast Paradox

The anti-bombast discipline can itself slide into bombast about
restraint — the documentation that explains avoiding marketing voice
can become its own marketing voice (`our rigorous discipline of
production-direction register`, `the only honest approach to
prompt-engineering`). The paradox surfaces when the rule is described
in the register the rule prohibits. The discipline applies to itself
recursively: describe the rule in the same plain register it asks for
elsewhere. The fix is to demonstrate the rule (show a BAD-bombastic
vs GOOD-plain rewrite) rather than to praise the rule.

## Tier 3 — Architectural Discipline

### 3-Stage Chain / 4-Phase Loop Architectural Pattern

Multi-step production decomposes into named stages where each
stage produces an artifact the next stage consumes. Common shapes:
3-stage chain (character → image → video) or 4-phase loop
(script → assets → blocking → prompts).

**When to apply:** Orchestrating multiple generation stages.

**Demonstrated in:** `skills/higgsfield-pipeline/SKILL.md` § The
Master Production Chain + § Pipelines A-E.

### Closing-Block-Baked-Into-Every-Prompt

A shared text fragment appended to every prompt ensures
cross-prompt consistency. Defined once, applied without
redrafting.

**When to apply:** Multiple prompts share a common closing concern.

**Demonstrated in:** root `SKILL.md` § MANDATORY WORKFLOW step 4
("Append shared negative constraints from
`skills/shared/negative-constraints.md` before delivering any
prompt") + the shared constraints file.

### Strict-Order Workflow with Refusal-to-Skip Phases

Sequential workflows enforce order — Step N+1 can't start until
Step N is approved. Skipping surfaces drift downstream.

**When to apply:** Numbered sequence where each step depends on the prior step's artifact.

**Demonstrated in:** `skills/higgsfield-cinema/SKILL.md` § The
10-Step Cinema Studio 2.5 Workflow.

### Pre-Delivery Discipline

Before delivering output to the user, run a self-repair pass against
a checklist of common failure modes — catch preventable issues at
construction time rather than after credit burn. The pass takes
60-90 seconds; the savings compound across iteration loops.

**When to apply:** Any sub-skill that produces a long-form artifact
(prompt, plan, template fill) where issues are easier to fix
pre-delivery than post-generation.

**Demonstrated in:** `skills/higgsfield-seedance/FAILURE-MODES.md`
§ Self-repair before delivery (7-item pre-delivery prevention
checklist consolidated from named failure-mode counters).

## Author-bundle systematization finding

The v3.7.5+v3.7.7 audit corpus surfaces a single Higgsfield-team-adjacent author bundle that documented its AI-cinema practice systematically. Five skills in the bundle. The patterns DISCIPLINE.md captures (pre-prompt confirmation gate, strict-order workflow, explicit-stop between phases, closing-block-baked-into-every-prompt, triple-redundant runtime, visual-marker-only output, inventory-extraction checklist, 3-stage/4-phase architectural pattern, single-variable iteration) are documented in the bundle's skills AND demonstrated in higgsfield's own codebase. Both surfaces — the bundle's documentation and higgsfield's demonstrated practice — surface independently the same set of disciplines. The patterns are the audit contribution; the higgsfield demonstration is observed practice; both surfaces converge because production-grade AI-cinema work has structural constraints that surface similar disciplines wherever it is practiced.

## Source attribution

Pattern *form* is the v3.7.5 audit contribution, IP-safe per the
audit's pattern-not-text classification. Pattern *demonstration*
is higgsfield's own existing practice.
