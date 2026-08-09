---
name: higgsfield-shotlist-director
description: "Turns a brief, script, scene breakdown, treatment, or story idea into ONE connected director's shotlist for Seedance 2.0 — a single editable HTML artifact with a global Style Prefix, an @-asset glossary, and named per-scene prompts (1a, 1b, 2a…) each in Style → Characters → Scene → CUT 1..N form. Use whenever the user says 'make a shotlist', 'break this script into prompts', 'generate Seedance prompts for this ad/film', 'turn this brief into a shot list', 'director's shotlist', or wants many connected scene prompts rather than one. Also use to revise an existing shotlist (edit-once-propagates: 'change the style prefix everywhere', 'rewrite scene 4', 'split prompt 6'). Each prompt targets 15s; longer scenes split across 1a/1b/1c under one scene number."
user-invocable: true
metadata:
  tags: [higgsfield, seedance, seedance-2.0, shotlist, director, style-prefix, ad, commercial, artifact, html]
  version: 1.2.0
  updated: 2026-08-09
  parent: higgsfield
---

# Higgsfield Shotlist Director

Turn a brief into **one connected shotlist** — not a pile of separate prompts.
The deliverable is a single editable HTML artifact the user opens in a browser,
ticks scenes off as they shoot, and comes back to you to revise. This is the
artifact-shaped workflow a fully-AI commercial actually runs on: lock a global
look once, declare the cast/props/locations once, then emit named per-scene
prompts that all inherit both.

> **This skill is the connected layer on top of `higgsfield-seedance`.** It does
> not reinvent the prompt grammar — every per-scene prompt obeys the six-slot
> formula and the Prompt-Craft Laws in `../higgsfield-seedance/SKILL.md`, and
> every prompt is preflight-linted before delivery. What this skill adds is the
> *document*: the global Style Prefix, the `@`-glossary, the per-scene numbering,
> and the edit-once / per-scene-override semantics that keep 25 prompts in sync.

## QUICK FACTS
- Output = **one self-contained HTML file** (inline CSS/JS, no deps), not loose prompts [→](#what-you-produce)
- Three structural layers, top to bottom: **Global Style Prefix → `@`-asset glossary → named per-scene prompts** [→](#the-three-layers)
- Per-scene prompt law: `Style → Characters → Scene → CUT 1..N`; each prompt targets **15s**; split long scenes as `3a/3b/3c` [→](#per-scene-prompt-law)
- [OFFICIAL] Density heuristic: group rows when ALL of {same cast, same location, one emotional unit, ≤15s, inside length limits}; split on ANY of {location cut, cast change, setup change, performance arc, insert} — **don't fragment grief**; complexity budget + auto-enrichment defaults for thin briefs [→](#prompt-density-grouping-shot-rows-into-15s-envelopes)
- Whole-sequence checks before delivery: **tempo budget** (cut durations sum exactly to runtime; one 6–8s hero hold) + **monotony audit** (no 3 consecutive cuts sharing shot size AND camera move) [→](#sequence-tempo-and-variety)
- Continuity carries exits too: an **Off-screen line** (exit side + last state) per just-departed character keeps re-entry direction legal [→](#per-scene-prompt-law)
- **Edit-once-propagates**: change the prefix once → it changes in every prompt; per-scene **override** lets one scene break the global look [→](#edit-once-and-per-scene-override)
- Differentiators over a bare shotlist generator: **preflight linter**, **reference-role lanes**, **Elements `@`-auto-attach**, **failure-mode awareness**, **acceptance-rate logging** [→](#what-makes-this-outclass-a-bare-generator)
- English prompt text only (Seedance expects English), even if the user writes in another language [→](#workflow)

---

## What you produce

A single `shotlist.html` (saved to the user's outputs and presented). It is
**self-contained** — inline CSS, inline JS, zero external dependencies — so the
user can open it offline and it just works. Structure:

1. **Title bar** — project name (infer from the brief; "Untitled" if unclear).
2. **Global Style Prefix** — collapsible block at top, applied to every prompt.
3. **`@`-asset glossary** — the cast/props/locations declared once.
4. **Scene list** — numbered scenes, each with a checkbox (progress saved in
   `localStorage`), a one-line scene description, and one or more copy-ready
   prompt blocks (`Prompt 3a · 15s`, `Prompt 3b · 15s`).
5. A short "how to use" note (checkboxes auto-save; ask Claude to revise).

The Style Prefix appears **once** in the collapsible block **and** is prepended
verbatim to every prompt's copy-block — so the user copies one prompt into
Seedance and it works standalone, no reassembly.

---

## The three layers

### 1. Global Style Prefix

A single style block glued to every prompt in the document — edit it once and it
changes everywhere. It locks the film's global look: format/resolution, lighting
doctrine, colour ratio, lens/shutter, skin realism, acting register, physics,
composition, continuity, frame rate, and audio convention.

Ship the reusable fill-in-the-blanks block from
[`../../templates/seedance/global-style-prefix.md`](../../templates/seedance/global-style-prefix.md).
**Always check the conversation first** — if the user pasted a custom prefix, use
that one verbatim. Otherwise use the template default.

### 2. `@`-asset glossary

Declare every recurring asset once, with a stable `@`-name, then register each
under **Elements** in Higgsfield with the **same name** so pasting a prompt
auto-attaches the right images:

```
@hero — main character          @boss — side character
@headphones — product           @sneakers · @bag · @skydancer — props
@kitchen · @stadium · @street — locations
@s_hero — athletic-look hero     @s_hero_wet — sweaty post-run hero
@music_track (audio_1.wav) — motion locks to this beat
@street_schematic (image_1.png) — top-down position map
```

The slot→role discipline (`@Image1` = character, `@Image2` = costume, `@Audio1`
= rhythm…) comes from `../higgsfield-seedance/SKILL.md` § Reference Roles →
Per-Image Role Convention. **Multi-state variants get their own locked entry**
(`@s_hero_wet`), built on purpose up front — asking the model to "sweat him up"
later makes it improvise and the face drifts.

**Each glossary entry also carries a fidelity grade** — a role says what job the
asset does, the grade says how much of it must survive into the pixels:
*full-preserve* / *partial-preserve (name the parts)* / *attribute-transfer (name
the target it lifts onto)* / *loose-guide*. One word per line is enough
(`@headphones — product, full-preserve`); the grades and their prompt phrasing
live in `../higgsfield-seedance-2-5/SKILL.md` § Reference Roles → Fidelity.
Without a grade, "use @image4 for the coat" silently means whatever the model
felt like keeping that day.

### 3. Named per-scene prompts

Every scene is numbered (`1`, `2`, `3`…) and split into named 15-second prompts
(`1a`, `1b`, `2a`). One checkbox per **scene**, even when split across `3a/3b/3c`.

---

## Per-scene prompt law

Every prompt follows this exact order, top to bottom. (This verbatim-prefix
shape is the **connected-shotlist regime** `[FIELD — 13-project harvest]`;
a standalone block-scaffold prompt instead distributes style into its home
blocks and opens on SCENE CONTEXT — `../higgsfield-seedance/SKILL.md`
§ Distributed style. Which shape ships is decided by the workflow: shotlist →
this law; single standalone brief → distributed.)

```
[STYLE PREFIX — full block, verbatim (or the per-scene override)]

Characters:
[Only the characters in this prompt. @names + locked physical descriptors +
carried state — wet hair from the prior scene, strap on one shoulder, same
wardrobe unless it changed on screen.]

Off-screen (only when someone just left):
[Anyone in the PREVIOUS prompt but absent here: exit side + last visible state —
"Bo — exited frame-left, still carrying the crate." Carry for one prompt, drop
after two consecutive absent prompts.]

Scene:
[1–2 sentences. Where, when, and the geo-spatial blocking — where each character
sits relative to the location and to each other. "Hero at the kitchen island,
back to camera; the moka pot is on the left burner."]

CUT 1 — [framing, lens/FOV, camera move]:
[Beat-accurate action: gesture, eye-line, breath, micro-pause; what the camera
does; what the light does; diegetic SFX if relevant.]

CUT 2 — …
```

Each prompt **targets 15s** (Seedance generates a fixed-length clip — design the
cuts to fill it, don't pad with dead air). Most 15s prompts hold 1–3 cuts —
that is the **live-action narrative norm**; stylized registers run denser by
design (3D-animated 6 shots/15s, product montage 8–10 sections with 0.3s macro
cuts — `../higgsfield-style/SKILL.md` § Style Recipes), and the flash-establish
/ insert durations in `../higgsfield-camera/SKILL.md` § Shot duration by type
are what make dense shapes fit. If a scene runs longer, split it across
`3a/3b/3c`, each its own 15s block with the full Style Prefix and Characters
block, continuity holding across them.

**Beat-by-beat choreography, not "he dances."** Generic motion verbs mean nothing
to Seedance — spell the move out: *"two crisp head nods on the beat, shoulders
rolling back one at a time, a soft knee-dip, a loose finger-snap, finishing on a
quarter-spin."* (Full pattern: `../../templates/10-dance-music-performance.md`.)

**The Off-screen line is what keeps re-entries legal.** Carried state covers who
is in frame; it says nothing about who just left, and re-entry from the wrong
side is a classic continuity break the viewer feels before they can name it.
One line per departed character buys the next prompt the correct entering side
and hand-state for free. `[EMPIRICAL — MiniMax H3 skill corpus; re-derived]`

**Match-cut via a repeated anchor action.** When independently-generated scenes
must cut together, end and begin neighboring scenes on the **same gesture** (the
ear-cup tap) — the reused motion lets them "cut on action" most of the time.
When those clips then sit on one timeline, plan the unifying finish pass and cut
placement per `../higgsfield-audio/SKILL.md` § Cutting to music.

---

## Prompt density — grouping shot rows into 15s envelopes

`[OFFICIAL — Higgsfield shotlist-builder + seedance-2-pro-director skills,
2026-07]` — the shotlist's hardest judgment call is how many script beats
share one 15s prompt. There is no fixed ratio (canonical productions ran
anywhere from 1.4 rows per prompt to 4.7); decide per scene with this
heuristic:

**Group shot rows into ONE prompt when ALL of these hold:**

1. Same character set in frame
2. Same location (or sub-area of it)
3. One continuous emotional/temporal unit — no time skip, no mood pivot
4. Stageable in ≤15 seconds of screen time
5. The combined prompt stays inside practical length limits (ZH: the
   1,800-char hard cap; EN block prompts run much longer — see
   `../higgsfield-seedance/SKILL.md` § Field calibration)

**Split into separate prompts when ANY of these fire:**

1. Hard cut between locations (apartment → flashback)
2. A major character entrance/exit changes the handle list
3. A lens/setup change that needs its own envelope (wide establish → tight
   insert)
4. A performance arc that deserves its own 15 seconds — a reaction that
   builds across 5–7 beats is never bundled with action. **Don't fragment
   grief**: one continuous emotional collapse is ONE prompt even if the
   script writes it as three rows.
5. An insert/cutaway to a prop or screen (those get their own ECU prompt)

**Complexity budget per prompt** (split triggers): more than 2 strong
actions · more than 2 camera moves · more than 3 important characters ·
more than 1 complex VFX event · more than 1 location change — any of these
means the scene wants another envelope. Duration ladder: 4–8s = one strong
action · 8–12s = one action + a reveal · 12–15s = 2–3 simple beats ·
complex fight/chase/transformation = multiple prompts. **Reconciling the
ladder with the 15s target:** 15s is the default envelope, not a
straitjacket — when a scene's beats genuinely fill only 4–8s of screen time,
generate a deliberately shorter clip (Seedance accepts 4–15s) rather than
padding dead air into 15; the prompt-law's "don't pad" rule wins.

**When in doubt, err toward more prompts and shorter envelopes** — Seedance
handles tight prompts better than overloaded ones, and the user can run them
in sequence.

**Auto-enrichment for thin briefs.** When a scene row is thin ("a guy in a
room, he's angry"), don't ask — fill in production detail with the default
cinematic choices, never details that change the meaning: 16:9 · one
clear physical action · slow controlled dolly-in or locked-off frame ·
a neutral-to-portrait lens (63°/47° FOV in Seedance block prompts — mm
vocabulary like "35–50mm" is for non-Seedance surfaces; 29° only if a
close-up needs it — `../higgsfield-seedance/SKILL.md` § FOV anchors) ·
motivated practical light · subtle ambience + one meaningful SFX · a clear
final frame. **Duration is never auto-defaulted** — inside a shotlist the
envelope law above governs (target 15s, shorter deliberate clips per the
ladder); for a standalone prompt, ask — the seedance rule "always ask the
user for runtime, never default" stands.

---

## Sequence tempo and variety

`[EMPIRICAL — third-party director-skill evaluations 2026-08-09; re-derived
heuristics, unmeasured here]` — two whole-sequence checks that no per-prompt
rule can catch, run once before delivery:

**Tempo budget — the arithmetic gate.** Budget the piece before writing it:
total runtime at ~4–6s average per cut gives the cut count the piece can carry,
with **one deliberately longer hero hold (6–8s)** reserved for the money moment.
Rough bands: ≤15s → ~3 cuts · ~20s → 4–5 · ~30s → ~6 · ~45s → 7–8 · ~60s →
9–11. Then check the sum: stated cut durations must **add up to the requested
runtime exactly**. A budget that doesn't add up ships dead air or an impossible
cut, and the error is invisible until the timeline.

**Monotony audit — read the column, not the prompt.** After drafting, read only
the framing + camera-move line of every cut, top to bottom, as one column. No
run of **three consecutive cuts** may share the same shot size *and* the same
camera move; when every cut reads "medium, slow push-in", vary the shot's
*function and scale* — not just its duration. Per-prompt review can't see this
failure at all; it only shows when the column is read as a sequence, and it is
the single most common tell of a generated shotlist.

---

## Edit-once and per-scene override

Talk to the user's revisions like an editor of one connected document, never 20
loose chats:

- **"Edit prompt 1a, do X"** → change only that prompt.
- **"Change the style prefix to Y, apply everywhere"** → propagate to every
  prompt's copy-block in one pass.
- **Per-scene override** → one scene can break the global look. Replace just that
  prompt's Style Prefix lighting line (e.g. Scene 2 stadium: *"bright, genuinely
  sunny midday, strong frontal sun, deep blue sky, hard-edged shadows"*) while
  every other scene keeps the soft global prefix. The override is a local edit to
  one prompt's prefix, not a change to the global block.

When revising, **re-render the same HTML file with the change applied** — don't
describe the change in chat. Preserve scene numbering where possible (don't
renumber everything for a one-prompt edit), preserve the Style Prefix unless told
to change it. The user's checkbox state survives via `localStorage` keyed by
scene number, so stable numbering = no lost progress.

---

## What makes this outclass a bare generator

A plain "script → prompts" generator stops at the document. This skill is wired
into the rest of the repo, which is the whole point:

1. **Preflight every prompt.** Before delivering the shotlist, run each prompt's
   copy-block through the linter — `python3 scripts/seedance_lint.py --preflight
   --regime block --model seedance_2_0 "<prompt>"`
   (`../higgsfield-seedance/SKILL.md` § Pre-flight Linter). Copy-blocks are
   block-scaffold regime: the linter usually auto-detects this, but pin
   `--regime block` so the short-form word caps can never fire on a
   full-density scene prompt. Real names, brand/IP, age markers, conflicting instructions, shot-
   count drift, and out-of-enum aspect/resolution/mode are caught **before** the
   user burns credits. A shotlist of 25 prompts is 25 chances to ship a flagged
   one. In the same pass run the § Sequence tempo and variety checks — the
   linter sees one prompt at a time; the sum check and monotony audit see the
   sequence.
2. **Reference-role lanes.** The `@`-glossary uses the stable slot→role
   convention so `@Image1` = character holds across all 25 prompts and nobody
   re-checks which face the model expects at shot 47.
3. **Failure-mode awareness.** Flag high-risk shots at authoring time (reflections,
   same-character doubles, crowds, compound camera moves, door-entry geometry) per
   `../higgsfield-seedance/ENGINE-RULES.md` and
   `../higgsfield-seedance/FAILURE-MODES.md`, rather than
   letting them silently break a scene.
4. **Acceptance-rate honesty.** The finished ad is the best few seconds out of
   many takes — keep candidates, test in motion, lock the winner, and log
   kept/rejected outcomes to the ledger (`higgsfield-recall`). The shotlist is the
   plan; iteration is still the skill.
5. **Audio as a driver.** When a `@music_track` locks the choreography, write the
   beat-sync mapping per `../higgsfield-audio/SKILL.md` § Audio as a Conditioning
   Input; keep the prompt body diegetic-only and layer score in post.

---

## Workflow

1. **Read the brief as a director, not a transcriber.** Find the dramatic shape —
   where each scene turns, lands, and breathes.
2. **Lock the Style Prefix.** Custom from the conversation, or the template
   default.
3. **Build the `@`-glossary.** One entry per recurring asset; multi-state variants
   get their own locked entry.
4. **Block the scenes.** Number them; decide how many 15s prompts each beat needs
   (honest assessment — a 40s confession is `5a/5b/5c`).
5. **Write each prompt** in the per-scene law (Style → Characters → Scene → CUT
   1..N), in **English** even if the user wrote in another language.
6. **Preflight every prompt** and flag high-risk shots.
7. **Generate the HTML** (skeleton below) and present it.
8. **On revisions**, re-render the file with edits applied; preserve numbering.

---

## HTML skeleton

Self-contained, dark directing-room aesthetic. Inline everything. Checkbox state
persists in `localStorage`; each prompt has a Copy button; the Style Prefix is in
a collapsible block at the top **and** prepended to every prompt's `<pre>`.

```html
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>{{PROJECT_TITLE}} — Director's Shotlist</title>
<style>
  :root{--bg:#0e0e10;--panel:#17171a;--panel-2:#1d1d21;--border:#2a2a30;
        --text:#e8e8ea;--dim:#9a9aa2;--accent:#d4a259;--done:#4ade80}
  *{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--text);
    font-family:-apple-system,system-ui,sans-serif;line-height:1.5;padding:32px 24px 80px}
  .container{max-width:980px;margin:0 auto} h1{font-size:28px;margin:0 0 4px}
  .howto,details.style-prefix,.scene{background:var(--panel);border:1px solid var(--border);
    border-radius:8px;padding:14px 18px;margin-bottom:18px}
  details.style-prefix summary{cursor:pointer;font-weight:600;color:var(--accent)}
  pre{white-space:pre-wrap;font-family:"SF Mono",Menlo,monospace;font-size:12.5px;margin:0}
  .scene-header{display:flex;gap:12px;align-items:flex-start;margin-bottom:14px}
  .scene-num{font-weight:700;color:var(--accent);min-width:48px}
  .scene.done .scene-desc{text-decoration:line-through;color:var(--dim)}
  .prompt-block{background:var(--panel-2);border:1px solid var(--border);
    border-radius:6px;margin-top:12px;overflow:hidden}
  .prompt-label{display:flex;justify-content:space-between;padding:8px 14px;
    border-bottom:1px solid var(--border);font-size:12px;color:var(--dim);text-transform:uppercase}
  .copy-btn{background:transparent;color:var(--accent);border:1px solid var(--border);
    border-radius:4px;padding:4px 10px;font-size:11px;cursor:pointer}
  .copy-btn.copied{color:var(--done);border-color:var(--done)}
  pre.prompt{padding:14px 16px}
</style></head><body><div class="container">
  <h1>{{PROJECT_TITLE}}</h1>
  <div class="howto">Tick scenes as you finish — progress saves automatically.
    Copy any prompt (Style Prefix + Characters + Scene + Cuts). Ask Claude to revise.</div>
  <details class="style-prefix"><summary>Global Style Prefix (applied to every prompt)</summary>
    <pre>{{STYLE_PREFIX_TEXT}}</pre></details>
  {{SCENES_HTML}}
</div><script>
  document.querySelectorAll('.scene input[type=checkbox]').forEach(cb=>{
    const k='shotlist-scene-'+cb.dataset.scene+'-done';
    if(localStorage.getItem(k)==='1'){cb.checked=true;cb.closest('.scene').classList.add('done')}
    cb.addEventListener('change',()=>{localStorage.setItem(k,cb.checked?'1':'0');
      cb.closest('.scene').classList.toggle('done',cb.checked)})});
  document.querySelectorAll('.copy-btn').forEach(b=>b.addEventListener('click',()=>{
    const p=b.closest('.prompt-block').querySelector('pre.prompt');
    navigator.clipboard.writeText(p.textContent).then(()=>{b.classList.add('copied');
      const t=b.textContent;b.textContent='Copied';
      setTimeout(()=>{b.classList.remove('copied');b.textContent=t},1500)})}));
</script></body></html>
```

Each scene block in `{{SCENES_HTML}}` (one checkbox per scene, `data-scene` =
scene number as a string):

```html
<div class="scene">
  <div class="scene-header">
    <input type="checkbox" data-scene="3">
    <div class="scene-num">3.</div>
    <div class="scene-desc">Hero grooves across the kitchen — the world goes quiet.</div>
  </div>
  <div class="prompt-block">
    <div class="prompt-label"><span>Prompt 3a · 15s</span><button class="copy-btn">Copy</button></div>
    <pre class="prompt">[FULL PROMPT — Style Prefix verbatim, then Characters, Scene, CUT 1, CUT 2…]</pre>
  </div>
  <div class="prompt-block">
    <div class="prompt-label"><span>Prompt 3b · 15s</span><button class="copy-btn">Copy</button></div>
    <pre class="prompt">[FULL PROMPT for the second 15s chunk of scene 3]</pre>
  </div>
</div>
```

---

## Related skills

- `higgsfield-seedance` — the prompt grammar this skill emits (six-slot formula,
  Prompt-Craft Laws, Reference Roles, preflight linter, engine + failure modes)
- `higgsfield-pipeline` — upstream multi-shot production planning the shotlist
  slots into
- `higgsfield-audio` — `@music_track` beat-sync + diegetic-only convention
- `higgsfield-soul` — locked character sheets the `@`-glossary points at
- `higgsfield-recall` — log kept/rejected take outcomes as you shoot the list
- `../../templates/seedance/global-style-prefix.md` — the reusable prefix block +
  a per-scene override example
