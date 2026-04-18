---
name: higgsfield-workspaces
description: "Use when the user is unsure which Higgsfield workspace fits their task, needs to decide between Cinema Studio / Lipsync Studio / Draw-to-Video / Sora 2 Trends / Click to Ad / Higgsfield Audio, or is asking 'what should I use for X'. This sub-skill routes by production problem BEFORE model selection."
user-invocable: true
metadata:
  tags: [higgsfield, workspaces, routing, decision, cinema-studio, lipsync, draw-to-video, sora-trends, click-to-ad, higgsfield-audio]
  version: 1.0.0
  updated: 2026-04-18
  parent: higgsfield
---

# Higgsfield Workspaces — Task-First Decision Layer

## Introduction

Higgsfield is organized around workspaces, each one tuned for a specific kind of
production work. The right starting question is not "which model should I use?"
but "what am I actually trying to make?" Inside a workspace, model choice still
matters — it shapes quality, speed, and cost — but a workspace mismatch costs
more time than a suboptimal model. Pick the workspace by the task, then pick the
model by the result you want.

---

## The Decision Matrix

| Your production problem | Start with workspace |
|-------------------------|----------------------|
| Cinematic scene with deliberate camera direction | Cinema Studio |
| Speaking character, dubbing, or avatar video | Lipsync Studio |
| Rough idea, sketch, or storyboard test | Draw to Video / Sketch to Video |
| Fast short-form or viral-style content | Sora 2 Trends |
| Product ad or ecommerce variation | Click to Ad |
| Narration, voice swap, or translation | Higgsfield Audio |

If the user's task matches more than one row, pick the workspace whose output
most closely resembles the final deliverable — you can always chain into another
workspace for polish or audio later.

---

## Workspace Descriptions

### Cinema Studio

The professional filmmaking environment on Higgsfield. Built for multi-shot,
character-consistent sequences where camera direction, genre framing, and visual
cohesion matter. Cinema Studio 2.5 offers optical physics (camera body + lens
stack) and built-in color grading; Cinema Studio 3.0 (Business/Team plan) adds
native audio, Smart camera planning, and longer durations. Choose this workspace
when the work needs to feel like a film. For prompt construction, Director Panel
use, optical stack selection, and multi-shot planning, see `higgsfield-cinema`.

### Lipsync Studio

The workspace for putting words into a character's mouth. It pairs an image,
video, or generated face with an audio track and synchronizes the lip movement
to the speech. Use it for dubbed performances, talking-head avatars, character
dialogue, and lipsync work layered on top of existing video generations. For
audio layer design (dialogue, SFX, ambient, BGM) that feeds into Lipsync Studio,
see `higgsfield-audio`. For character reference management and Soul Cast avatar
generation that commonly sits upstream, see `higgsfield-soul`.

### Draw to Video / Sketch to Video

The workspace for turning a rough drawing — a napkin sketch, blocking diagram,
storyboard panel — into a generated video. It's the fastest path from "here's
the idea on paper" to a moving test. Use it for early ideation, shot-blocking
experiments, and pre-production tests before committing credits to a full Cinema
Studio build. This workspace is thinly documented in the current skill; for
available one-click workflows related to sketch-based generation, see
`higgsfield-apps` (Sketch-to-Real and related app listings).

### Sora 2 Trends

A templated workspace built on top of the Sora 2 model, tuned for fast,
trend-led short-form content. Distinct from picking Sora 2 as a raw model —
Trends wraps the model in a workflow optimized for viral pacing, vertical
framing, and quick iteration. Use it when the deliverable is TikTok/Reels/Shorts
style content and you want the templating rather than full Cinema Studio
control. This workspace is thinly documented in the current skill; for
Sora 2 model capabilities and for app-level workflow entry points, see
`higgsfield-apps`.

### Click to Ad

The product-focused ad workspace. Paste a product URL or upload an image and
Click to Ad produces a video ad variation tuned for ecommerce use. It's the
fastest way to produce packshot-adjacent content without writing a cinematic
prompt. Use it for product ads, ecommerce variations, and quick-turn commercial
content. For the full Click to Ad decision tree, companion product-ad apps
(Packshot, Giant Product, Macro Scene, Billboard Ad, and the rest of the ad
family), see `higgsfield-apps`.

### Higgsfield Audio

The standalone voice workspace — distinct from Lipsync Studio and from in-video
audio generation. It handles voiceovers, voice swaps across existing tracks, and
translation workflows where audio is the primary deliverable rather than a
layer inside a video. Use it when the output is audio, or when you need a voice
asset to feed into a downstream workspace. For audio layer design principles
that apply to both standalone and in-video audio work, see `higgsfield-audio`.

---

## The Six-Step Project Logic

Every workspace follows the same high-level project flow. Memorizing this
sequence means you can navigate any new workspace without re-learning it.

1. **Open the right workspace** — the one matching your production problem.
2. **Choose the right feature** inside it — mode, preset, or tool that fits the
   specific shot or asset you're producing.
3. **Select the model** that fits the job — quality, speed, and cost tradeoffs
   live here, inside the workspace you already chose.
4. **Prepare the input** — hero frame, reference image, source video, audio
   clip, or any starting asset the workspace expects.
5. **Add the prompt, script, or controls** — MCSLA for scene prompts, UI
   settings for Cinema Studio, motion reference for Motion Control, and so on.
6. **Generate, review, iterate** — expect multiple passes. Change one variable
   per iteration so you can tell what drove the improvement.

---

## Relationship to MCSLA

Workspace-first is a routing layer that sits ABOVE the MCSLA prompt formula.
Once you're inside the right workspace, MCSLA (Model · Camera · Subject · Look ·
Action) still governs how the prompt itself is built. Workspaces don't replace
MCSLA — they decide which environment you'll apply MCSLA inside. A Cinema Studio
prompt, a Sora 2 Trends prompt, and a Click to Ad prompt all benefit from MCSLA
discipline, but the UI controls, defaults, and model options around each prompt
are different. Choose the workspace first; then apply MCSLA cleanly inside it.

---

## Related skills

- `higgsfield-cinema` — prompt patterns for Cinema Studio (all modes)
- `higgsfield-audio` — audio layer design for Lipsync Studio and in-video audio
- `higgsfield-soul` — character references and Soul Cast avatars, often upstream of Lipsync
- `higgsfield-apps` — one-click workflows, including sketch-based and trend-based entry points
- `higgsfield-models` — model selection once a workspace is chosen
- `higgsfield-prompt` — MCSLA formula applied inside any workspace
