---
name: higgsfield-recall
description: >
  Use this skill AUTOMATICALLY before writing any Higgsfield prompt. Query the memory
  databases for relevant past failures and pre-apply known fixes before the user even
  hits generate. Triggers include: any request to write a Higgsfield prompt, any use
  of the higgsfield-prompt skill, any mention of generating a video or image on
  Higgsfield, any MCSLA prompt construction. This skill should run SILENTLY in the
  background — don't announce it, just apply what's known. If the databases are empty,
  skip silently and proceed with normal prompt generation.
user-invocable: true
metadata:
  tags: [higgsfield, recall, memory, pre-check, filter, quality, prompt, generate]
  version: 3.0.0
  updated: 2026-04-06
  parent: higgsfield
  compatibility:
    tools: [bash]
    scripts: [scripts/higgsfield_memory.py]
    databases: [db/filter-memory.json, db/quality-memory.json]
---

# Higgsfield Recall — Pre-Generation Memory Check

## Purpose

Before writing any Higgsfield prompt, query both memory databases to find relevant
past failures. Apply known fixes silently — the user should never have to remember what
broke before. The system remembers for them.

**This skill runs automatically** as part of any Higgsfield prompt generation.
It does not interrupt the workflow unless it finds something relevant.

**Bootstrap status:** The databases ship with seed entries covering the most common
failure patterns (character drift, VHS style ignored, I2V static output, camera conflicts,
lip-sync desync, content filter blocks for real persons and IPs). These grow automatically
as the user logs new failures.

---

## When to Run

Run a recall check whenever:
- Writing or improving a Higgsfield prompt (any type)
- The user mentions a topic, character, action, or style that could match past failures
- The prompt contains terms that historically triggered content filters
- The model being selected has previously produced poor results for this type of shot

**Do NOT announce running the recall check.** Just run it, apply what's relevant,
and proceed. Only surface findings when they directly change the prompt.

---

## Recall Workflow

### Step 1: Extract search terms from the prompt intent

Before querying, pull the key semantic terms from what the user wants:

```
Extract:
- Subject/character (person type, appearance)
- Action (what they're doing)
- Location/environment
- Style (visual style, model, camera)
- Topic (the general category: "car chase", "product shot", "horror scene")
```

---

### Step 2: Query both databases

```bash
# Check for relevant filter blocks:
python3 scripts/higgsfield_memory.py query-filter "<key terms from prompt>" 5

# Check for relevant quality failures:
python3 scripts/higgsfield_memory.py query-quality "<key terms from prompt>" 5
```

**Query strategy:**
- Use 3–6 of the most specific nouns from the prompt
- Run separate queries for the subject, action, and style if needed
- Prioritize entries with `fix_confirmed: true` — these are proven solutions

---

### Step 3: Evaluate relevance

For each result returned, assess:

| Question | If yes → |
|----------|----------|
| Does this entry's topic/category directly overlap with this prompt? | Apply the known fix |
| Is a blocked term present in my draft prompt? | Remove/substitute it now |
| Did this model fail on this type of shot before? | Consider switching models |
| Is there a confirmed improved prompt for this scenario? | Use it as the base |

**Relevance threshold:** Only act on entries with a relevance score > 0 from the query.
Ignore entries that only match on generic words.

---

### Step 4: Apply findings silently

**For filter block matches:**
- Remove or substitute the blocked terms before presenting the prompt
- If a substitution was confirmed to work, use it directly
- Do not tell the user "I removed X because it was blocked before" unless they ask —
  just present the clean prompt

**For quality failure matches:**
- Use the confirmed improved prompt structure as the base
- Apply the specific fix that worked (e.g. explicit artifact description for VHS)
- Adjust the model if a better one was identified for this scenario

---

### Step 5: Surface findings only when material

Only mention the recall results if:
- A significant change was made to avoid a known filter block
- A model switch is recommended based on past failures
- The recall found a directly relevant confirmed fix that substantially changes the prompt

**How to surface findings (when needed):**

```
"⚠️ Filter note: Previous attempts with [term] were blocked on [date].
Using '[substitution]' instead — this was confirmed to pass."

"📋 Quality note: [Model] produced [failure type] for this scenario before.
Switching to [better model] based on past results."
```

If nothing relevant found: proceed silently, no mention of the recall check.

---

## Manual Recall (User-Initiated)

The user can also request a recall check directly:

```
"What do we know about [topic] failing?"
"Has [model] had issues with [scenario] before?"
"What got blocked when we tried [type of content]?"
"What's our substitution for [blocked term]?"
```

For these queries, surface the full relevant entries with:
- The original failure
- The substitution or fix that was tried
- Whether it was confirmed to work
- The date it was logged

---

## Pre-Generation Checklist (run mentally before every prompt)

Before finalizing any prompt, check:

- [ ] Named real person in prompt? → Check filter-memory for real-person blocks
- [ ] Weapon, drug, or violence language? → Check filter-memory for violence/substance blocks
- [ ] Brand or IP name? → Check filter-memory for brand-ip blocks
- [ ] Using a model that has failed for this scenario type? → Check quality-memory
- [ ] Using VFX/style keywords that were previously ignored? → Check quality-memory
- [ ] Character consistency required? → Check quality-memory for character-drift entries

---

## Log the Generation Result — One Question, One Command

Every generation attempt belongs in the **generation ledger**
(`../../db/ledger/` — kept AND rejected; the denominator is what makes
takes-per-kept ratios possible). The write path is agent-side and obeys the
**5-second rule**: at most one short question, then the agent runs one
command. The human never formats JSON, never fills a form.

**When the user reports a generation result** (pastes a link, says "that one
worked", "trash", "the face drifted again"):

1. If the verdict and reason are already clear from what they said, **ask
   nothing** — log it directly.
2. Otherwise ask **exactly one question**: *"keep or reject — what failed?"*
   If they don't answer, drop it. **Never ask twice, never nag.**
3. Write the row yourself:

```bash
python3 ../../scripts/higgsfield_memory.py log-gen <project> \
  --model seedance_2_0 --tags dialogue-cu,two-char \
  --outcome rejected --reason extra-cuts --credits 160
```

- `--tags` and `--reason` come from the controlled vocabularies in
  `../../db/ledger/README.md` — map the user's words to the nearest vocab
  value (`"face drifted"` → `identity-drift`); never invent new values.
- Add `--draft` for 480p exploration rolls (excluded from headline ratios).
- Wrong verdict logged? `python3 ../../scripts/higgsfield_memory.py amend-gen
  <id> outcome=kept` — corrections are superseding rows, history stays.
- Project name: the user's production name if one is established in the
  conversation, else `default`.
- Logging `--method quick|mcsla` tags the row for the framework-lift A/B
  (`ab <project> --tag <shot_tag>`); omit it to leave the row unlabeled and
  out of the comparison — never guess a method.

### Optional: log the routing (usage telemetry)

HARD RULE #1 already makes you name the sub-skills you routed to on the first
line of every response. When a production is tracking which skills actually earn
their keep, persist that declaration:

```bash
python3 ../../scripts/higgsfield_memory.py log-route --skills higgsfield-prompt,higgsfield-camera
```

`python3 ../../scripts/higgsfield_memory.py routing` then ranks sub-skills by opens and
lists the never-opened long tail. This is **instrumentation, not a verdict** —
it makes "which skills are load-bearing, which to prune" answerable from data
once enough requests accumulate; a small sample is not evidence a skill is dead.

### Read the verdict before re-rolling

After a few logged rows, `python3 ../../scripts/higgsfield_memory.py ratio <project>`
prints a per-shot-tag **verdict** that decides iterate-vs-batch:

- `iterate` (structural-dominant) → the prompt is wrong; hand off to
  `higgsfield-prompt` § The Iteration Rule (one variable at a time).
- `batch+sel` (stochastic-dominant) → the prompt is right; **stop re-rolling
  one at a time** — lock it, roll a batch, cull (see `higgsfield-prompt` §
  Batch-and-Select).
- `low-n` → fewer than five rows; don't trust the split, call it by eye.

A ⚠ plausibility line means a tag is beating its planning default by a wide
margin — *either* real lift *or* under-logged failures; surface it, let the
user decide. The verdict is only as good as the `reject_reason` labels, so map
the user's words to vocab honestly — and when the rejected output is in hand,
classify it from the frame instead of from memory (`higgsfield-troubleshoot` §
Vision-Grounded Diagnosis logs a `--vision-reason` alongside the human verdict,
advisory until the `agreement` command proves it).

---

## Database Status Check

To see current knowledge base size:
```bash
python3 scripts/higgsfield_memory.py stats
```

Empty databases = no recall benefit yet. Start logging failures with `higgsfield-troubleshoot`
and the recall system gets smarter with every entry.

---

> **Negative constraints:** The recall system complements `../shared/negative-constraints.md`.
> The shared file covers universal prevention rules; this recall system covers
> user-specific past failures and confirmed fixes.

---

## Related skills
- `higgsfield-troubleshoot` — Diagnose and fix specific failures (feeds recall DB)
- `higgsfield-prompt` — MCSLA formula, Identity/Motion separation
- `higgsfield-soul` — Character drift prevention (common recall topic)
- `higgsfield-models` — Model-specific failure patterns
