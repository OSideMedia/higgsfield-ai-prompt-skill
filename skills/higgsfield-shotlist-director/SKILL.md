---
name: higgsfield-shotlist-director
description: "Turns a brief, script, scene breakdown, treatment, or story idea into ONE connected director's shotlist for Seedance 2.0 — a single editable HTML artifact with a global Style Prefix, an @-asset glossary, and named per-scene prompts (1a, 1b, 2a…) each in Style → Characters → Scene → CUT 1..N form. Use whenever the user says 'make a shotlist', 'break this script into prompts', 'generate Seedance prompts for this ad/film', 'turn this brief into a shot list', 'director's shotlist', or wants many connected scene prompts rather than one. Also use to revise an existing shotlist (edit-once-propagates: 'change the style prefix everywhere', 'rewrite scene 4', 'split prompt 6'). Each prompt targets 15s; longer scenes split across 1a/1b/1c under one scene number."
user-invocable: true
metadata:
  tags: [higgsfield, seedance, seedance-2.0, shotlist, director, style-prefix, ad, commercial, artifact, html]
  version: 1.0.0
  updated: 2026-06-27
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

### 3. Named per-scene prompts

Every scene is numbered (`1`, `2`, `3`…) and split into named 15-second prompts
(`1a`, `1b`, `2a`). One checkbox per **scene**, even when split across `3a/3b/3c`.

---

## Per-scene prompt law

Every prompt follows this exact order, top to bottom:

```
[STYLE PREFIX — full block, verbatim (or the per-scene override)]

Characters:
[Only the characters in this prompt. @names + locked physical descriptors +
carried state — wet hair from the prior scene, strap on one shoulder, same
wardrobe unless it changed on screen.]

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
cuts to fill it, don't pad with dead air). Most 15s prompts hold 1–3 cuts. If a
scene runs longer, split it across `3a/3b/3c`, each its own 15s block with the
full Style Prefix and Characters block, continuity holding across them.

**Beat-by-beat choreography, not "he dances."** Generic motion verbs mean nothing
to Seedance — spell the move out: *"two crisp head nods on the beat, shoulders
rolling back one at a time, a soft knee-dip, a loose finger-snap, finishing on a
quarter-spin."* (Full pattern: `../../templates/10-dance-music-performance.md`.)

**Match-cut via a repeated anchor action.** When independently-generated scenes
must cut together, end and begin neighboring scenes on the **same gesture** (the
ear-cup tap) — the reused motion lets them "cut on action" most of the time.

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
   copy-block through the linter — `python3 seedance_lint.py --preflight --model
   seedance_2_0 "<prompt>"` (`../higgsfield-seedance/SKILL.md` § Pre-flight
   Linter). Real names, brand/IP, age markers, conflicting instructions, shot-
   count drift, and out-of-enum aspect/resolution/mode are caught **before** the
   user burns credits. A shotlist of 25 prompts is 25 chances to ship a flagged
   one.
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
