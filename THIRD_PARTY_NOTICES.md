# Third-party notices

O-Side Media licenses its own contributions to this repository — those it is entitled to
license — under the MIT licence in `LICENSE`. It does not purport to grant rights it does not
hold. Some material in this repository comes from, or is adapted from, other sources, and the
MIT licence text should not be read as a grant of rights in that material.

A credit below acknowledges a source. It is not a statement that the source's owner has approved
the use of their material here.

This is an independent project. It is not affiliated with, endorsed by or sponsored by
Higgsfield, ByteDance, OpenAI or any other vendor it mentions. Product and model names are the
trademarks of their owners and are used only to identify the products.

## 1. Withdrawn from the current tree (November 2026)

The following material reproduced or closely adapted third-party text. O-Side Media could not
confirm a right to redistribute it, so it was removed. Where other files still point at a removed
section, a short notice marks the place.

This section describes the current tree only. Earlier commits, tags and releases of this
repository were not changed and still contain the withdrawn material.

| What was withdrawn | Source |
|---|---|
| `docs/Seedance 2 Skill.md` (the whole file), two sections of `skills/higgsfield-prompt/SKILL.md` and the numbered rule list in `skills/higgsfield-seedance/ENGINE-RULES.md` | A third-party bilingual Seedance prompt-director document. Its author was not identified. |
| `skills/higgsfield-seedance/HELL-GRIND.md` (the whole file) and the default prefix block in `templates/seedance/global-style-prefix.md` | The production brief for the AI feature film "Hell Grind". The withdrawn file credited it to Higgsfield as an open-source brief; O-Side Media has not confirmed the terms it was published under. |
| `skills/higgsfield-acting/SKILL.md` (the whole sub-skill) | Acting-direction skill files that the withdrawn file credited to the "Hell Grind" brief (row above); their individual author was not confirmed. Individual passages also credited "Tigran's tig-acting-task skill", a "prompt-builder 2.5" document and a Higgsfield Studio production breakdown. |
| Sections 1–9 of `skills/higgsfield-gpt-image-2/SKILL.md`; `skills/higgsfield-gpt-image-2/static-ads-workflow.md`; the `skills/higgsfield-content-factory/` sub-skill; `skills/higgsfield-marketing-studio/cross-surface-workflow.md` (the whole file); the per-preset creative direction, the prompt-style section, the worked prompts, the escape-hatch model list and the rate samples in `skills/higgsfield-marketing-studio/SKILL.md`; and five sections of `vocab.md` (Camera Contract, Motion Physics Anchor, Lens Behavior Sequence, Spatial Zoning, Negative space) | Skill files, example prompts and videos by Adil Aliyev. |
| The prompt-method sections and example blocks of `skills/higgsfield-seedance-2-5/SKILL.md`, the mode templates of `skills/higgsfield-seedance-2-5/MODE-PLAYBOOKS.md`, and the skeleton and example blocks in `templates/seedance/omni-reference-2-5.md` | Dreamina / Seedance 2.5 prompt documentation (ByteDance), and related Seedance 2.5 prompt material whose author was not confirmed. |
| The method sections of `templates/seedance/staging-reference.md`, including its diagram prompt and connector block | A third-party blocking-map skill credited in that file. |
| The copy-and-paste prompts and worked examples in `skills/higgsfield-gpt-image-2/reference-sheet-workflow.md`, and the tutorial prompt excerpts in `prompt-examples.md` § Seedance-4K Film Tutorial | A reference-workflow guide, a companion prompt pack and a film tutorial published by Higgsfield. |
| The Screen Test / Audition section of `skills/higgsfield-character-design/SKILL.md` | A community casting-director prompt. Its author was not identified. |
| `templates/seedance/anime-animation.md` (the whole template) | An anime-animation guide by Fotachu ("AR GUY"), a Higgsfield Creator Partner Program creator. |

Shorter excerpts from the same sources were also removed from `skills/higgsfield-seedance/SKILL.md`
and the example answers under `evals/cases/`.

## 2. Third-party material still present

To O-Side Media's knowledge, the current tree still contains the following. O-Side Media does not
purport to license any of it, and has not confirmed its redistribution status.

- **Vendor catalog data — `specs/`.** The `models_explore_snapshot*.json` files and
  `cli_baseline.json` are output of Higgsfield's own catalog tools, saved as dated snapshots; the
  `model-specs.*`, `*-model-specs.*` and `*MODEL-SPECS.md` files are generated from them. The underlying data is Higgsfield's. O-Side Media
  has not obtained Higgsfield's permission to redistribute it and has not resolved whether
  Higgsfield's terms of use allow that. It is kept as a dated factual reference only, and the MIT
  licence does not cover it.
- **Guidance drawn from vendor documentation.** Passages labelled `[OFFICIAL — …]` restate, and
  in places briefly quote, documentation published by Higgsfield, ByteDance (Dreamina / Seedance)
  and OpenAI. That includes the parameter and limit descriptions left in
  `skills/higgsfield-seedance-2-5/`, the description of the Canvas workspace in
  `skills/higgsfield-canvas/SKILL.md`, and the guidance left in
  `skills/higgsfield-gpt-image-2/reference-sheet-workflow.md`. The label legend is
  `skills/shared/provenance.md`.
- **Guidance drawn from other authors' skills, guides and videos.** Passages labelled
  `[EMPIRICAL — …]`, `[DEMO — …]` or `[FIELD — …]` name the third-party skill, guide or video they
  draw on. Some places credit their source in their own text instead of a label: the API notes left
  in `skills/higgsfield-marketing-studio/SKILL.md`, which cite a skill file and videos by Adil
  Aliyev; the character-design framework in `skills/higgsfield-character-design/` and
  `templates/character-design/`; the passages in `skills/higgsfield-cinema/` and
  `skills/higgsfield-soul/SKILL.md` that credit a third-party methodology; and
  `production-benchmarks.md`, which reports figures from the "Hell Grind" production.
- **A Chinese filler-term list and length cap in `scripts/seedance_lint.py`.** The `ANTISLOP_ZH`
  terms and the Chinese prompt length cap that the linter enforces were taken from the bilingual
  Seedance prompt-director document named in section 1.
- **Fonts — `assets/fonts/`.** DejaVu fonts, under their own licence; see
  `assets/fonts/README.md`.

## 3. Rights holders

If you hold rights in material in this repository and want it removed or credited differently,
contact O-Side Media through its GitHub organisation page, <https://github.com/OSideMedia>.
