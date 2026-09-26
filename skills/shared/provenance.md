# Provenance Labels — the Repo-Wide Legend

Every claim in this library that did not come from the repo's own reasoning carries a tag
saying where it came from. The tag tells an agent **how hard to lean on the claim** — and,
when two files disagree, which disagreement is real. Local tables (the Provenance blocks in
`../higgsfield-seedance-2-5/SKILL.md` and `../higgsfield-seedance-2-5/VFX-PIPELINE.md`) name
*sources*; this file defines the *labels* they use.

Contested questions — two tagged sources disagreeing about the same regime — are indexed in
`house-rulings.md` in this directory.

---

## The labels

| Label | What it means | Evidence the tag must carry | How to lean on it |
|---|---|---|---|
| `[OFFICIAL — <source>, <date>]` | The vendor or the platform said so: Higgsfield's own published skills, briefs and docs; ByteDance's Dreamina guides; the platform catalog (`models_explore` snapshot, CLI rules) | A named, dated, **vendor-authored** document or snapshot. Authorship must be recorded in the repo — a copy found in a community channel is not OFFICIAL on the strength of where it was found | Strongest prior. On what is **settable** (enums, durations, roles, caps) `[OFFICIAL — platform]` outranks every other label (HARD RULE 3). On what **works**, vendor prompt doctrine is a strong prior, not a measurement |
| `[DEMO — <source>, <date>]` | Shown working on screen in a vendor or studio tutorial — the output was visible | The tutorial named and dated; what was shown | One demonstrated instance, n ≈ 1. Numbers quoted on screen (pricing, rates, "after tons of testing") are the presenter's claim and carry "verify live" |
| `[FIELD — <source>, <date>]` | Observed in real productions: a studio's breakdown of its own film, a harvest of shipped production prompts or jobs | The production(s) or corpus named and dated; for a corpus, its scale (projects · creators · prompts or jobs) | Proves a practice was **used** in shipped work; does not by itself prove the practice caused the result. One studio is one production's practice |
| `[EMPIRICAL — <source>, re-derived <date>]` | **Third-party practitioner material** — a skill file, a prompt corpus, a guide — evaluated here, judged sound, re-written in house voice, and **not measured on our routes** | The source named (repo or skill, licence where known) and the date it was re-derived | A strong heuristic. "Unmeasured here" is part of the label's meaning — `[UNPROVEN HERE]` is implied and need not be repeated |
| `[HOUSE]` | This repo's own rule or inference — nobody else's | The argument, on the page | Exactly as strong as its argument. Unmeasured unless it also carries `[MEASURED]` |
| `[MEASURED — <route>, <model · mode · resolution>, n=<per arm>, <date>]` | **Our own run** | The route (the surface actually fired: Higgsfield MCP / CLI / web, or a direct provider such as Ark), the model with mode and resolution, the sample size per arm, the date, the result. The record should be citable — a ledger row, a CHANGELOG entry | The only label that is evidence *here*, and only for the route it names. One pair is a direction, not a rate |

### Modifiers

- **`[UNPROVEN HERE]`** — added to an OFFICIAL, DEMO or FIELD claim that nobody here has run.
  Redundant on EMPIRICAL.
- **`record incomplete: <missing fields>`** — inside a MEASURED tag when the record lacks a
  route, an n, a model or a date. Read the result as a **direction**, never as a rate, and never
  let it overrule a complete record.
- **`record held outside this repo`** — a measurement whose raw data is not in this repository.
  The repo can only vouch for what it wrote down; treat it as record-incomplete.
- **"verify live" / "confirm in the UI"** — any number that changes without a snapshot
  behind it: credit prices, plan limits, UI state.
- **`[DREAMINA-ONLY]`** — a Dreamina *product* feature with no Higgsfield parameter behind it
  (`../higgsfield-seedance-2-5/SKILL.md` § Dreamina-Only).

---

## Rules for applying them

1. **Tag the claim, not the file.** A header tag covers only the untagged text beneath it; a
   section that carries its own tag is governed by its own tag. A line such as *"every
   template here is OFFICIAL"* is false the moment one section below it carries another label.
2. **Third-party skill material is EMPIRICAL** — whatever the file is called, however
   production-shaped it looks. It becomes FIELD only when it reports productions it shipped,
   with the production named, and OFFICIAL only when the repo records that the vendor wrote it.
3. **Somebody else's measurement is not MEASURED here.** A third party's captured errors on
   another provider's lane stay EMPIRICAL; a measurement ported from outside this repository
   keeps its fields and gains `record held outside this repo`.
4. **Labels do not settle disagreements by rank**, with two exceptions: the platform snapshot
   wins on what is settable, and a complete MEASURED record wins on what works on the route it
   names. Everything else goes into `house-rulings.md` with both sides and "unmeasured here".
5. **A settling probe is named, not assumed.** When a ruling is OPEN, the cheapest probe that
   would settle it (usually one 480p pair) is written next to it — and nothing is promoted to
   MEASURED until that probe has actually run and been logged.

---

## Legacy labels — how to read them under this legend

Older text uses forms that predate this legend. They are read as follows; new text uses the
table above.

| As written | Read as |
|---|---|
| `[FIELD — community, <skill or repo>]` — e.g. `seedance-2.0 repo v6.6.0` | EMPIRICAL — third-party skill material |
| `[EMPIRICAL — community workflow]` · `[EMPIRICAL — community guides, NOT official docs]` | EMPIRICAL, source unnamed — the weakest form; prefer a named source |
| `[EMPIRICAL — third-party, China Ark lane, 2026-08]` | EMPIRICAL — a third party's measurement on a non-Higgsfield route (rule 3) |
| `[FIELD]` · `[OFFICIAL]` · `[DEMO]` alone | The same label, with the source named in the enclosing section's or file's header tag |
| `[FIELD provenance: first observed on N harvested jobs, <date>]` | FIELD |
| `[HOUSE — re-derived from <third-party skill>]` | EMPIRICAL (rule 2) |
| `[DEMO — <person> (<skill file>)]` + `[UNPROVEN HERE]` | EMPIRICAL (rule 2) |

---

## Related

- `house-rulings.md` — every contested question, its ruling or "OPEN — unmeasured", and the
  files that carry each side
- `negative-constraints.md` — the shared prevention reference (its Whole-Frame Degradation
  section is the worked example of an EMPIRICAL claim with its settling probe named)
- `../higgsfield-seedance-2-5/SKILL.md` § Provenance · `../higgsfield-seedance-2-5/VFX-PIPELINE.md`
  § Provenance — the local source tables
