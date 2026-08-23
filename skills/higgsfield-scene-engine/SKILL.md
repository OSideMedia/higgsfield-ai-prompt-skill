---
name: higgsfield-scene-engine
description: "Tests whether a scene is structurally worth generating before any shot is prompted — a five-element engine of Goal, Obstacle, Tactic, Reversal, and Value Shift. Use when the user has a scene, sequence, beat outline, or script and wants it audited or strengthened; when a sequence generates cleanly but lands flat and nobody can say why; when shots look good individually but the run of them does not build; or when the user asks 'is this scene working', 'what's weak here', or 'why doesn't this land'. Upstream of prompting — it decides WHICH shots deserve the credits, not how to write them. Pairs with higgsfield-character-design (who the characters are) and higgsfield-shotlist-director (turning the settled scene into shots)."
user-invocable: true
metadata:
  tags: [higgsfield, story, scene, structure, sequence, audit, dramaturgy, pre-production, reversal, value-shift]
  version: 1.0.0
  updated: 2026-08-22
  parent: higgsfield
---

# Higgsfield Scene Engine — is this scene worth generating?

`[DEMO — Tigran (tig-scene-engine), 2026-06-26]` `[UNPROVEN HERE]` **These definitions are
bespoke and deliberately not the textbook ones.** Apply them as written; do not substitute
standard screenwriting glosses, which are looser and will pass scenes this engine fails.

**Why a prompter carries this.** Every shot costs credits and iterations. A structurally
dead scene generates just as cleanly as a live one — the model has no opinion about whether
a beat earns its place — so the failure surfaces only after the footage exists and the cut
does not build. This skill is the cheapest pass in the repo: it runs on text, before any
generation, and its whole job is to stop you paying to render a scene that cannot work.

It decides **which** shots deserve the spend. `higgsfield-shotlist-director` turns the
settled scene into shots; `higgsfield-acting` writes the performance inside them.

---

## The five-element engine

### 1. Goal

The single, unchanging thing the hero is fighting for: to fix what has already been
established and reach, as fast as possible, the result that resolves it. "Already
established" means *anything* set up earlier — deep backstory, a few scenes ago, or one
minute ago.

- **The major goal never changes**, and the hero is never wrong about it. He can be wrong
  about **tactics**, never about the goal.
- **Every scene goal must be a causal link toward the story goal.** *Test:* if you can
  remove the scene and the chain still holds, the scene fails. No orphan scenes.
- "What he *ought* to do" is not a separate thing to test — the right move is dictated by
  **Obstacle + Stakes**. A hero taking a tactic the stakes would not justify (showering
  while the building burns) is a flaggable inconsistency: name it as bad writing or as
  deliberate self-sabotage.

### 2. Obstacle

A strong circumstance that **jeopardizes** either one stage of the path or the whole goal.
It *threatens*; it does not merely *cost*.

- It can be a **branching search space** (many places to look, limited time) or a **single
  hard wall** (a dead battery — you cannot search a dead machine). A wall typically spawns
  a fresh sub-goal with its own terrain.
- Name its **scale**: *local* (threatens the current stage) or *global* (threatens the whole
  goal).
- The obstacle is **what forces the hero to choose or change a tactic.** No jeopardy → no
  tactic needed → no scene.
- *Audit test:* name what is at risk, and at what scale. If nothing genuinely is, the
  obstacle is fake and the scene goes slack.

### 3. Tactic

The move the threat **forces** the hero to choose — a reasonable guess on his current,
often incomplete, knowledge. This is **search under uncertainty, not error-as-stupidity.**

- A "wrong" tactic is not dumbness; it is a plausible probe of a space he cannot fully see.
  The engine is a **knowledge gap**: the distance between what he believes and what is.
- **Each failed tactic must return information** that narrows the search and reshapes the
  next move. The drama is the narrowing, not the punishment.
- ✅ good: the tactic is a reasonable bet on current info, **and** its failure teaches
  something new.
- ❌ weak: a tactic he had no reason to try, or a failure that returns **zero information** —
  a wheel-spin. A failing tactic is only a weakness when the failure teaches nothing.

### 4. Reversal

A turn against expectation. Three forms:

1. **My own action flips on me** — what I did *for* something starts working *against* it
   (I shower to make the pitch; the shower makes me late and I miss it).
2. **Hidden agency revealed** — the thing or person I thought I was acting *on* was acting
   *on me* all along. The thriller move; it often fires exactly when the knowledge gap closes.
3. The general case: the situation turns opposite to what the tactic intended.

**Placement:** at least one reversal **per sequence**. A single scene may be pure
escalation, but a *resolved sequence* with zero reversals **fails**.

A **sequence** is the run of scenes from when a specific jeopardy opens to when it resolves —
overcome, or it defeats him and forces a new path. Sequences **nest**, and each resolving
unit needs its own reversal. Flag which scale you are auditing.

### 5. Value Shift

**The change in the AUDIENCE'S read of a character, triggered by a reversal.** The keystone,
and the most misunderstood element: it does not happen on the page, it happens in the
viewer's mind. Each reversal forces the audience to **re-judge** the character — a moving
verdict they keep revising (*nice → experienced → cunning → no, he's desperate → devoted son
→ what a man*).

> **THE CORE RULE: a reversal with no value shift is inert.** A structural turn is not a
> reversal unless it moves the audience's verdict. If you cannot name a **before-verdict**
> and an **after-verdict** the audience would hold, the turn is dead weight no matter how
> much plot flipped.

Audit the **trajectory**, not just presence: are the revaluations building a deepening
portrait, or just oscillating?

---

## The causal chain

> **Goal** (fixed; every scene a causal link toward it)
> → **Obstacle** (jeopardizes a stage or the whole goal; name what is at risk + scale)
> → **Tactic** (forced by the threat; a reasonable guess; its outcome must return information)
> → **Reversal** (turn against expectation; ≥1 per resolved sequence)
> → **Value Shift** (the audience re-judges the character; no shift → the reversal is useless)

---

## Audit procedure

Work the chain in order. Reversal and Value Shift are judged at the **sequence** level, not
the scene.

1. **Goal** — state the scene goal in one line. Is it a causal link to the story goal? Apply
   the removal test. If you do not know the story goal, ask — you cannot fully audit Goal
   without it.
2. **Obstacle** — name the circumstance, exactly what it jeopardizes, and the scale.
3. **Tactic** — is each forced by the jeopardy, reasonable on current knowledge, and does
   each outcome return information? Flag wheel-spins and unmotivated tactics.
4. **Reversal** — locate them, name the form, confirm ≥1 per resolved sequence.
5. **Value Shift** — for **each** reversal, name before-verdict → after-verdict. If you
   cannot, mark it **INERT** and make it the priority fix. Then assess the trajectory.

### Audit output

```
SCENE/SEQUENCE: <one-line identification>

CHAIN CHECK
• Goal — <verdict + one line>
• Obstacle — <what's jeopardized + scale + verdict>
• Tactic — <forced? reasonable? returns info? verdict>
• Reversal — <form + present? ≥1 in sequence? verdict>
• Value Shift — <before-verdict → after-verdict per reversal, or INERT; trajectory note>

WEAKEST POINT: <the single element that, if fixed, recovers the most>

WHAT IF…
1. (Minimal) <change ONLY the weakest point so the rest of their scene still works>
2. (Clean) <a version that fully works, even if it departs further from the original>
3. (Optional) <only if it genuinely adds something>
```

The three tiers matter in that order: **minimal preserves the user's version**, clean is
yours, and the third is optional. Do not collapse them into one rewrite.

---

## Where this sits before prompting

Once the chain holds, the scene is worth spending on — and only then:

| Next | Skill |
|---|---|
| Who these people are, and their bible | `../higgsfield-character-design/SKILL.md` |
| The shared scene direction and each character's fuel | `../higgsfield-acting/SKILL.md` § The layer above the pillars |
| Breaking the settled scene into shots | `../higgsfield-shotlist-director/SKILL.md` |
| Writing the shot itself | `../higgsfield-seedance/SKILL.md` · `../higgsfield-seedance-2-5/SKILL.md` |

**The most common real failure to hunt for first:** a reversal that turns the plot but does
not move the audience's verdict. Surface it before anything else — it is the one that
survives a read-through, generates beautifully, and still lands flat in the cut.

## Related Skills

- `../higgsfield-character-design/SKILL.md` — premise, world, character, story bible
- `../higgsfield-acting/SKILL.md` — the performance layer inside a settled scene
- `../higgsfield-shotlist-director/SKILL.md` — scene → shot list
