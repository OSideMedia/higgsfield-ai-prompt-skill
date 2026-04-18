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
    scripts: [higgsfield_memory.py]
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
python3 higgsfield_memory.py query-filter "<key terms from prompt>" 5

# Check for relevant quality failures:
python3 higgsfield_memory.py query-quality "<key terms from prompt>" 5
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

## Database Status Check

To see current knowledge base size:
```bash
python3 higgsfield_memory.py stats
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
