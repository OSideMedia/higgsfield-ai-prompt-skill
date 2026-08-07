# Template: Seedance 2.5 Omni-Reference Brief

The paste-ready skeleton for a **Seedance 2.5 `omni_reference`** generation — several
characters, props, scenes, motion, and audio references combined into one staged clip.

Doctrine: `../../skills/higgsfield-seedance-2-5/SKILL.md`. Long-form mode templates
(editing, extension, one-click, transitions, blockouts): the same directory's
`MODE-PLAYBOOKS.md`.

## When to use this template

- The user supplies **more than one** reference material, or one reference plus a description
- Two or more named subjects must not swap appearance, clothing, or props
- The clip runs longer than a single continuous beat (stage it)
- Any 2.5 job that is *not* plain `t2v` and *not* an edit/extension order

For a single-subject clip with one reference and one continuous action, skip the structure and
use the core formula in `SKILL.md` § The Core Prompt Formula — this template is for the case
where material mapping is the risk.

## Platform settings (not prompt text)

`[OFFICIAL — platform, snapshot 2026-08-07]` Set these in the UI / API, never in the prose:

| Setting | Value |
|---|---|
| `mode` | `omni_reference` |
| `duration` | 4–30 s |
| `resolution` | `480p` (drafts) or `720p` (2.5 has no 1080p/4K lane) |
| aspect ratio | `auto` · `21:9` · `16:9` · `4:3` · `1:1` · `3:4` · `9:16` |
| `generate_audio` | `true` unless the deliverable is silent |

Preflight before spending: `python3 scripts/seedance_lint.py --preflight --model seedance_2_5 "<prompt>"`

---

## The skeleton

Fill the bracketed fields. **Delete any block the shot does not need** — an empty block is
noise, not structure.

```
[Characters]
<Character A> corresponds to @Image 1. Use only the appearance, hairstyle, and clothing.
<Character B> corresponds to @Image 2. Use only the appearance, hairstyle, and clothing.
Do not interchange these characters' appearances, clothing, actions, positions, or dialogue.

[Props]
<Prop A> corresponds to @Image 3 and belongs only to <Character A>. Use only the structure,
material, and color.

[Scenes]
<Scene A> references @Image 4. Use only the spatial layout, architecture, and lighting.
Do not use the people in the image.

[Motion and Audio]
@Video 1 defines the pacing of <specific action>. Do not use the person's identity, clothing,
or scene from the video.
@Audio 1 defines <Character A>'s voice and specified dialogue.

[Subject Profile: <Character A>]          ← only for a subject recurring across scenes
Appearance and clothing: @Image 1.
Fixed prop: <Prop A> from @Image 3.
Locations: <Scene A>.
Motion references: the <action> motion from @Video 1.
Do not use: other characters' clothing. Do not give this character other equipment.

[Generation Goal]
Generate a <video type>. The central subject is <subject>, and the primary event is
<one-sentence story summary>.

[Stage 1]
Initial state: <initial state of characters, props, and scene>.
Primary event: <ONE primary action or event>.
End state: <character positions, prop ownership, or visible scene state>.

[Stage 2]
Continue from the previous stage: <state that must remain unchanged>.
Primary event: <ONE primary action or event>.
End state: <observable state>.

[Stage 3]
Primary event: <closing event>.
End state: <final visible state>.

[Visual Style]
<Lighting, color, materials, texture, mood — named specifics, not stacked adjectives>.

[Camera]
<Shot size, angle, movement, focus subject, cuts — matched to the action, not decorative>.

[Audio]
<Ambience and action SFX>. (music, only if the project wants it) <specific sound effect>
Dialogue language: <language and regional variety>. <Character A> says: {the line}

[Maintain Consistency]
Keep <character identity, number of characters, clothing, prop ownership, spatial direction,
and audio relationships> consistent throughout.
```

---

## Filled example

Two characters, one prop, one location, one motion reference, three stages.

```
[Characters]
<Florist> corresponds to @Image 1. Use only the appearance, hairstyle, and dark green apron.
<Assistant> corresponds to @Image 2. Use only the appearance, hairstyle, and clothing.
Do not interchange these characters' appearances, clothing, actions, positions, or dialogue.

[Props]
<Wrapped Bouquet> corresponds to @Image 3 and belongs only to <Florist> until Stage 3.
Use only the structure, flower types, and ribbon color.

[Scenes]
<Shop Workbench> references @Image 4. Use only the spatial layout, timber surfaces, and
window light. Do not use the people in the image.

[Motion and Audio]
@Video 1 defines the pacing of trimming stems and tying a ribbon. Do not use the person's
identity, clothing, or scene from the video.

[Generation Goal]
Generate an observational documentary clip. The central subject is <Florist>, and the primary
event is packing a single order from loose stems to a finished bouquet on the pickup shelf.

[Stage 1]
Initial state: <Florist> stands behind <Shop Workbench>. Loose stems, scissors, and wrapping
paper lie on the tabletop.
Primary event: <Florist> arranges the stems and trims them to length.
End state: <Florist> holds the bouquet in the left hand; the scissors are back on the right
side of the workbench.

[Stage 2]
Continue from the previous stage: both characters keep the same identities and clothing, and
<Florist> still holds the bouquet.
Primary event: <Assistant> unfolds the wrapping paper; <Florist> places the bouquet inside and
ties it with the ribbon.
End state: <Wrapped Bouquet> lies flat in the center of the workbench, ribbon bow facing camera.

[Stage 3]
Primary event: <Assistant> lifts <Wrapped Bouquet> and sets it on the pickup shelf.
End state: the bouquet is centered on the pickup shelf; both characters stand behind the
workbench looking at the finished order.

[Visual Style]
Overcast morning window light from frame-left, no fill from the camera side. Muted greens and
raw timber, one saturated accent in the ribbon. Real skin texture, visible paper grain.

[Camera]
Open on a medium shot of the workbench at chest height, hold through Stage 1, push in slowly
to the ribbon knot across Stage 2, then a single lateral move to follow the bouquet to the
shelf in Stage 3. 47° diagonal field of view throughout, no drift mid-segment.

[Audio]
Room tone, scissor snips, paper rustle, the ribbon pulling tight. <A shop bell rings once,
distant> (no music)

[Maintain Consistency]
Keep <Florist> and <Assistant>'s identities and clothing, the workbench orientation, the
scissors' position, and bouquet ownership consistent throughout.
```

---

## Checks before sending

- [ ] Every material has a role **and** an exclusion
- [ ] No `@Images 1 through N define N characters` — one line per subject
- [ ] Every prop belongs to exactly one character
- [ ] Each stage has **one** primary change and an explicit end state
- [ ] Stage count matches the runtime you set (three stages do not fit in 5 seconds)
- [ ] No age words anywhere (`../../skills/higgsfield-seedance/ENGINE-RULES.md` rule 1)
- [ ] Positive phrasing only — no `negative:` list, no bare negation stack
- [ ] Dialogue lives in the `[Audio]` block, in `{}`, and nowhere else
- [ ] Resolution is 480p or 720p — 2.5 has no higher lane
- [ ] `seedance_lint.py --preflight --model seedance_2_5` clean

## Related

- `../../skills/higgsfield-seedance-2-5/SKILL.md` — the dialect this template implements
- `../../skills/higgsfield-seedance-2-5/MODE-PLAYBOOKS.md` — edit / extend / one-click / transitions
- `multi-character-anchor.md` — the 2.0 form of cross-character anchoring
- `global-style-prefix.md` — the connected-shotlist style prefix
- `../../skills/higgsfield-acting/SKILL.md` — what to write when a stage needs performance
