---
name: higgsfield-workspaces
description: "Use when the user is unsure which Higgsfield workspace fits their task, needs to decide between Cinema Studio / Lipsync Studio / Draw-to-Video / Viral Hub presets / Click to Ad / Higgsfield Audio (Sora 2 Trends is built on the retired Sora 2), or is asking 'what should I use for X'. This sub-skill routes by production problem BEFORE model selection."
user-invocable: true
metadata:
  tags: [higgsfield, workspaces, routing, decision, cinema-studio, lipsync, draw-to-video, viral-hub, sora-trends, click-to-ad, higgsfield-audio]
  version: 1.3.0
  updated: 2026-09-26
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
| Fast short-form or viral-style content | Viral Hub presets (Sora 2 Trends is built on the retired Sora 2 — see its section) |
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

The workspace for taking a rough sketch, blocking diagram, or storyboard panel
and turning it into a generated video. It exists to bridge the gap between
paper-stage ideation and motion testing — the place to validate a shot idea
before it earns the credits and time of a full Cinema Studio build.

**When to use:**
- Early ideation, when you're still deciding what the shot wants to be.
- Shot blocking experiments — testing how a composition reads in motion.
- Pre-production validation before committing to Cinema Studio scene work.
- Fast iteration on framing, staging, and silhouette before the prompt or
  reference set is locked.

**Input characteristics:** the workspace is forgiving. Hand-drawn storyboards,
blocking diagrams with stick figures or geometric placeholders, even a crude
napkin sketch all work as input. Quality of line is not the point — clarity of
compositional intent is. A messy sketch with a clear staging idea outperforms
a polished sketch whose staging is muddled.

**The prompt's role:** the sketch carries composition and blocking; the prompt
carries everything else. Subject details, environment, lighting, mood, and
material qualities all live in the prompt. Think of the prompt as describing
the realized scene the sketch was hinting at — the sketch told the engine
*where* things sit and *how* they move; the prompt tells it *what* they are.

**Scope — this workspace, not a Seedance reference slot.** Here the sketch *is*
the input the workspace is built to realize, and a draft that inherits its
layout is the point. Attached to a Seedance generation it is a different
regime: a drawing in the first-frame role becomes frame one, drawing and all,
and a position diagram goes in **last** as a position reference only — one
incomplete-record house run found it does not reliably move blocking
(`../higgsfield-seedance/FAILURE-MODES.md` § A fight generated as separate
clips comes back choppy; `../../templates/seedance/staging-reference.md`;
`../shared/house-rulings.md` P2-11). Do not carry "the sketch carries
blocking" from here into a Seedance prompt.

**Output expectations:** test-quality, short. The output is a tool for shot
validation, not usually the final delivery. Treat the result as a draft, then
either refine the prompt (if blocking is right but the realized scene is off)
or re-block with a new sketch (if the staging itself needs to change).

**Two prompt patterns:**

- **Realization pattern** — describe the scene the sketch was pointing toward,
  including lighting and mood, and end with a camera direction that matches
  what the sketch implies. Use this when you want a faithful interpretation
  of the rough drawing.
- **Variation pattern** — keep the blocking implicit (the sketch handles it)
  and use the prompt to swap style, lighting, genre, or time-of-day across
  multiple generations. Same composition, different treatments. Useful for
  picking a visual direction before committing.

**Cross-reference:** when the test reads well and you want a longer, multi-shot
realization, move into Cinema Studio with the validated blocking in mind. If
you need higher fidelity earlier in the process — a pre-rendered hero frame
that subsequent shots can reference — the Hero Frame workflow inside Cinema
Studio is the alternative path. See `higgsfield-cinema` for that handoff.

### Viral Hub presets

`[OFFICIAL — Higgsfield MCP tool schema, get_presets, 2026-09-26]` Higgsfield's preset
galleries are browsed with `get_presets`; `source: 'viral'` lists the **Viral Hub** chain
presets (the gallery behind `/effects` requests). Browsing opens a preview and starts
nothing — a preset runs through `execute_preset` only when the user explicitly asks to
generate. This is where fast short-form / viral work starts now that Sora 2 Trends sits on
a retired model. Presets are the viral-effects / social product, not film grammar (the
scope caveat at the top of `../higgsfield-motion/SKILL.md`): a trend piece that needs
deliberate camera direction belongs in Cinema Studio.

### Sora 2 Trends

> **Built on Sora 2 — likely affected by its shutdown (unconfirmed in the UI).**
> OpenAI shut the Sora 2 API down on 2026-09-24 `[OFFICIAL — OpenAI deprecations page, read
> 2026-09-26]`. Whether this workspace still works in Higgsfield's web UI after that date
> is unconfirmed — on 2026-09-26 higgsfield.ai/sora-2 was still up with no shutdown
> notice. Don't route new work here; fast short-form / viral work starts from the Viral
> Hub presets above. The description below is kept as reference.

A templated workspace built on top of the Sora 2 model, tuned for trend-led
short-form content. The distinction worth holding onto: this is *not* the same
as selecting Sora 2 as a raw model elsewhere on the platform. Trends wraps the
model in pre-tuned templates optimized for viral pacing, vertical framing,
and quick iteration cycles. The templating is the point — it does work that
would otherwise have to be re-invented every shot.

**When to use:**
- TikTok, Reels, and Shorts deliverables — anywhere the format itself is more
  important than full cinematic control.
- Trend-jacking, where speed of iteration and platform fluency beat per-shot
  polish.
- Content where the audience expects a specific format-native rhythm rather
  than a deliberate director's hand.

**Distinguishing features:**
- **Vertical-first composition.** 9:16 is the default, with 1:1 and 4:5 also
  common. Compositions are framed for phones, not for film.
- **Pacing optimized for short-attention spans.** Fast cuts, hook-driven
  openings, and a "payoff by second three" structure are baked into the
  templates rather than something the prompt has to enforce.
- **Templated patterns for common trend formats.** POV reveals,
  before-and-after flips, "tell me without telling me" setups, day-in-the-life
  loops, and similar recurring structures each have a starting template.
  Picking the template is most of the structural work.

**Input characteristics:** usually a hook idea or a trend reference. Characters
and locations can be specified, but the templating handles a lot of structure
that you'd otherwise have to direct manually. The lift on input is light.

**The prompt's role:** provide the specific subject and beat for the chosen
trend template. The template handles pacing and format; the prompt handles
*what* the shot is about within that format. Think of the prompt as content
slotted into a structure that's already running.

**Trade-offs vs. Cinema Studio:** Trends sacrifices fine-grained control in
exchange for speed and platform-native output. If the deliverable needs
deliberate camera direction, character continuity across shots, or genre
framing that the trend templates don't carry, Cinema Studio is the right
workspace and the wrong question to ask in Trends.

**Cross-reference:** for one-click trend-flavored workflows that overlap with
this workspace (Vibe Motion, the various style apps), see `higgsfield-apps`.
When full cinematic control is needed instead of templated trend pacing,
escalate to `higgsfield-cinema`.

### Click to Ad

The product-focused ad workspace. Paste a product URL or upload an image and
Click to Ad produces a video ad variation tuned for ecommerce use. It's the
fastest way to produce packshot-adjacent content without writing a cinematic
prompt. Use it for product ads, ecommerce variations, and quick-turn commercial
content. For the full Click to Ad decision tree, companion product-ad apps
(Packshot, Giant Product, Macro Scene, Billboard Ad, and the rest of the ad
family), see `higgsfield-apps`.

### Higgsfield Audio

The standalone voice workspace — and the most commonly misplaced one on the
platform, because Higgsfield has three distinct audio surfaces that all sound
similar by name. This workspace is the one where audio is the deliverable
itself, not a layer baked into a video and not a sync target for a generated
face.

**When to use:**
- Voiceover work where the final output is an audio file (narration, podcast
  inserts, ad reads, e-learning tracks).
- Voice swap on an existing audio track — change who says it without changing
  the timing or the emotional shape of the performance.
- Translation of an existing audio track into another language, ideally
  preserving as much of the original speaker's character as the engine
  supports.
- Any time you need a voice *asset* that will be fed into a downstream
  workspace (a finished track to feed into Lipsync Studio, an ad read to drop
  under a Click to Ad video, narration to underlay a Cinema Studio sequence).

**Three core capabilities:**

- **Voiceover generation.** Text in, spoken audio out. Voice characteristics
  — gender, age range, tone, pacing, energy level — are directable. Use this
  for greenfield voice work where there is no source audio.
- **Voice swap.** Source audio in, same audio in a different voice out. The
  timing, prosody, and emotional inflection of the original performance carry
  over; only the speaker identity changes. This is the right tool when an
  existing performance is structurally good but the voice is wrong (a bad
  scratch track, a placeholder read, an unlicensable original).
- **Translation.** Source audio in, the same content rendered in another
  language out. Where the engine supports it, the original speaker's voice
  characteristics are preserved across the translation, so the localized
  version still sounds like the same person.

**Input characteristics:**
- For voiceover: clean text or a script. Stage directions and tone notes
  belong in the prompt, not in the script body.
- For voice swap: source audio plus a target voice reference. The cleaner the
  source, the cleaner the swap.
- For translation: source audio plus the target language. Optionally a voice
  match preference if the engine offers it.

**The prompt's role:** voice descriptors and direction notes. Tone
(calm/urgent/conversational/authoritative), age range, accent, energy, and
pacing are all directable through the prompt. The synthesis itself is handled
by the audio engine — the prompt steers performance, not synthesis.

**Distinction from Lipsync Studio:** Lipsync Studio puts a voice (often
generated here) onto a video character. The sync direction there is
audio-to-video — the face follows the audio. Higgsfield Audio standalone
produces voice as a deliverable in its own right, with no video involvement
required. If the user wants a talking character on screen, route to Lipsync
Studio; if they want a voice file, this is the workspace.

**Distinction from in-video audio:** the SCELA layer of a Cinema Studio
generation (dialogue, SFX, ambient, BGM) is *baked into* the video at
generation time. That work lives in `higgsfield-audio`. Standalone Higgsfield
Audio is voice-as-asset — a separate deliverable, not a layer.

**Cross-reference:** for the in-video audio layer design (SCELA, dialogue
blocking, ambient sound design, BGM direction), see `higgsfield-audio`. For
AI actor voices that pair with avatars and Soul Cast characters, see
`higgsfield-soul`. For when the voice asset produced here gets dropped onto a
generated face, see Lipsync Studio above.

---

### Higgsfield Collab

Collab is Higgsfield's built-in collaboration space — the team-and-community
layer that sits across the workspaces above. It is where a campaign or scene
stops being a solo job and becomes a shared one. Use it when more than one
person needs to generate, review, or talk through work together.

**Shared projects.** A project is a shared space where members generate
together, chat, share assets, and hop on calls. Projects have three access
levels:

- **Private** — invited members only.
- **Public** — discoverable, view-only for non-members.
- **Open** — anyone can join with owner approval.

**Real-time communication.** Chat is built into every project. Any project
with two or more members supports audio and video calls — join, leave, and
mute from inside the project, with a persistent call bar that stays visible as
you navigate so you never lose the call.

**Share to Collab.** Send any generation straight into the project chat with
one tap using the **Share to Collab** toggle. Teammates see the output along
with its prompt, model, and progress, so they can react, give feedback, or
build on it immediately.

**Community feed.** A recommended-and-trending feed of published work across
the platform, for discovery and inspiration.

**Orgs & Team Plans.** Free Orgs enable collaborative identity sharing; paid
Team Plans unlock shared credits, shared elements, admin controls, and SSO.
Users also earn karma by liking, commenting, generating, and inviting friends,
and can exchange karma for credits.

> **Collab vs Shared Canvas.** Collab is project-level collaboration —
> shared spaces, chat, calls, and a community feed. **Shared Canvas** (see
> `../higgsfield-canvas/SKILL.md` § Shared Canvas) is board-level live
> co-editing of a single node graph. Reach for Collab to organize a team and
> a campaign; reach for Shared Canvas to build one pipeline together in real
> time.

This sub-skill documents only the collaboration features Higgsfield publishes;
it does not assert limits beyond those.

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
prompt, a Draw to Video prompt, and a Click to Ad prompt all benefit from MCSLA
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
