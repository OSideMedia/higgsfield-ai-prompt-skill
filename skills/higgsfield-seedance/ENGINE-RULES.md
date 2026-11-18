# Seedance 2.0 — Engine Rules (shared core)

This file was the shared home for Seedance 2.0's hard rendering constraints. The
numbered rule list has been withdrawn (see below); what remains is house technique:
the high-risk shot table and the enforcement notes.

**The dialects are output *profiles* of this one rule core:**

| Profile | Format | Where |
|---------|--------|-------|
| `EN-director` | English prose prompt, six-slot formula, MCSLA-compatible | `SKILL.md` (this skill) |
| `ZH-house` | Chinese house format (镜头-block shotlists, ≤1,800 chars) | team `shotlist-builder` (external corpus); ZH rules enforced by `../../scripts/seedance_lint.py` |
| `bilingual-JSON` | JSON API persona emitting paired EN + ZH prompts | a third-party reference document, withdrawn from this repository |

Pick the profile by delivery target.

---

## Hard rendering constraints

The numbered rule list that used to sit here was consolidated from a third-party reference
document and has been withdrawn — see `THIRD_PARTY_NOTICES.md` at the repository root. Other files still
cite those rules by number ("rule 1", "rule 8"); the citing sentence normally states the rule it
relies on. The mechanical subset is still enforced by the linter (§ Enforcement).

---

## High-risk shot types — flag at authoring time

These shot types conflict with the engine rules above. **Flag the conflict
when the request comes in** — a project whose hero image is a mirror or water
reflection needs the documented workaround applied deliberately, not the rule
silently broken. Mitigations are house technique derived from the engine
rules; they are not platform-documented features.

| High-risk shot | Why it breaks | Mitigation |
|----------------|---------------|------------|
| **Reflections** (mirrors, water, blades) | Engine breaks scene geography rendering reflector + reflected together (rule 8) | Never show the reflective surface and the subject in one continuous shot. Shoot the reflection **as** the scene: a dedicated shot where the mirror/water image is the primary subject, then cut (double-contrast — `../../vocab.md` § Cut & Continuity Vocabulary) to the physical subject. For a reflection hero image, pin it as the start frame of its own shot rather than asking the engine to construct the reflection. |
| **Two instances of the same character** (clones, mirror selves, time doubles) | Identity tracking assumes one body per identity; instances contaminate each other | Treat each instance as a **separate named role** with its own wardrobe/feature anchors ("@Hero-present: rain-soaked coat; @Hero-memory: pressed suit"). Pin each with its own reference image where possible. Prefer cutting between instances over continuous two-instance frames. |
| **Crowds** | Only ≤3 characters track across cuts (rule 5) | Describe the crowd as **environment, not characters**: a single mass with collective motion ("the crowd surges left as one"). Never name or track more than 3 individuals; foreground your tracked pair against the mass. |
| **Text rendering** (signs, inscriptions, screens) | Glyph fidelity is unreliable, and per § Drafts Validate the Prompt, fine-detail legibility re-rolls every generation | Keep story-critical text out of the generation: use the text-overlay templates (`../../templates/text-overlays/`) or post overlays. If in-scene text is unavoidable, keep it short, large, and verify legibility **at final resolution** — never approve it from a 480p draft. |

---

## Enforcement

- `../../scripts/seedance_lint.py --preflight --model seedance_2_0` checks the
  mechanical subset (age markers, shot-count declarations, ZH caps, enum
  legality per `../../specs/model-specs.json`).
- The judgment subset (reflections, instance handling, crowd phrasing,
  double-contrast) is a judgment call — name the conflict plainly when flagging
  it to the user.
