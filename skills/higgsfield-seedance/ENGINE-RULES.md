# Seedance 2.0 — Engine Rules (shared core)

This file is the **single home** for Seedance 2.0's hard rendering constraints.
Every Seedance prompt dialect cites this core instead of restating it — the
rules used to live only inside the bilingual-JSON profile doc, where the other
dialects couldn't see them.

**The dialects are output *profiles* of this one rule core:**

| Profile | Format | Where |
|---------|--------|-------|
| `EN-director` | English prose prompt, six-slot formula, MCSLA-compatible | `SKILL.md` (this skill) |
| `ZH-house` | Chinese house format (镜头-block shotlists, ≤1,800 chars) | team `shotlist-builder` (external corpus); ZH rules enforced by `../../scripts/seedance_lint.py` |
| `bilingual-JSON` | JSON API persona emitting paired `{"lang":"en"}` + `{"lang":"zh"}` prompts | `../../docs/Seedance 2 Skill.md` |

Pick the profile by delivery target; the rules below apply to **all of them**.

---

## Hard rendering constraints

Source: production-validated rules from the bilingual-JSON director doc
(`../../docs/Seedance 2 Skill.md` § Engine Rules), consolidated 2026-06-11.

1. **Age-blind characters (CRITICAL).** Never describe characters by age — in
   either language. Trigger words: *boy, girl, child, kid, young, teen, little,
   男孩, 女孩, 孩子, 少年, 少女, 小孩, 年轻*. Describe by **role** (rider,
   figure, traveler), **clothing**, and **action** — label what they do, never
   who they are.
2. **Action beats = intent + named technique, not biomechanics.**
   ✅ "spinning back kick connects." ❌ "left forearm rotates 45° to deflect."
   If the user names a move, preserve it; if they describe joint mechanics,
   compress to the move's name or intent.
3. **Describe force and direction, not destruction sequence.**
   ✅ "driven into the car, metal buckling." ❌ "thrown into side door, glass
   shatters, uses rebound to sweep leg."
4. **Spatial continuity breaks on cuts.** Re-anchor positions and facing
   direction after any cut.
5. **≤ 3 characters tracked across cuts.** Name the acting pair and the
   interaction vector per shot.
6. **Exit-frame = implicit cut.** A character who leaves frame is gone for the
   remainder of that shot. Never choreograph exit + re-entry in one continuous
   shot.
7. **Off-screen = nonexistent.** State changes must be shown on camera before
   being referenced.
8. **Avoid reflection shots** (blades, puddles, mirrors) — Seedance breaks
   scene geography when rendering reflections. See the high-risk table below
   for the workaround when the project *requires* one.
9. **Only describe what can be seen or heard.** ❌ "the air smells of pine."
   ✅ "pine needles covering the ground, wind moving through branches."
10. **Micro-expressions as physics.** ✅ "jaw clenches, nostrils flare."
    ❌ "looks angry."
11. **Double-contrast cut (mandatory).** Every cut changes **both** shot size
    (extreme wide → wide → medium → MCU → CU → ECU) **and** camera character
    (handheld | static | stabilized tracking | crane | aerial) — never repeat
    either across a cut.

---

## High-risk shot types — flag at authoring time

These shot types conflict with the engine rules above. **Flag the conflict
when the request comes in** — a project whose hero image is a mirror or water
reflection needs the documented workaround applied deliberately, not the rule
silently broken. Mitigations are house technique derived from the engine
rules; they are not platform-documented features.

| High-risk shot | Why it breaks | Mitigation |
|----------------|---------------|------------|
| **Reflections** (mirrors, water, blades) | Engine breaks scene geography rendering reflector + reflected together (rule 8) | Never show the reflective surface and the subject in one continuous shot. Shoot the reflection **as** the scene: a dedicated shot where the mirror/water image is the primary subject, then cut (double-contrast, rule 11) to the physical subject. For a reflection hero image, pin it as the start frame of its own shot rather than asking the engine to construct the reflection. |
| **Two instances of the same character** (clones, mirror selves, time doubles) | Identity tracking assumes one body per identity; instances contaminate each other | Treat each instance as a **separate named role** with its own wardrobe/feature anchors ("@Hero-present: rain-soaked coat; @Hero-memory: pressed suit"). Pin each with its own reference image where possible. Prefer cutting between instances over continuous two-instance frames. |
| **Crowds** | Only ≤3 characters track across cuts (rule 5) | Describe the crowd as **environment, not characters**: a single mass with collective motion ("the crowd surges left as one"). Never name or track more than 3 individuals; foreground your tracked pair against the mass. |
| **Text rendering** (signs, inscriptions, screens) | Glyph fidelity is unreliable, and per § Drafts Validate the Prompt, fine-detail legibility re-rolls every generation | Keep story-critical text out of the generation: use the text-overlay templates (`../../templates/text-overlays/`) or post overlays. If in-scene text is unavoidable, keep it short, large, and verify legibility **at final resolution** — never approve it from a 480p draft. |

---

## Enforcement

- `../../scripts/seedance_lint.py --preflight --model seedance_2_0` checks the
  mechanical subset (age markers, shot-count declarations, ZH caps, enum
  legality per `../../specs/model-specs.json`).
- The judgment subset (reflections, instance handling, crowd phrasing,
  double-contrast) is reviewed against this file — cite the rule number when
  flagging a conflict to the user.
