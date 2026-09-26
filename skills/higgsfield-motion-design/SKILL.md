---
name: higgsfield-motion-design
description: "End-to-end motion-design / animated-ad creation flow on Higgsfield via the MCP connector. Use when the user wants to create motion design, animate a logo, make a video from an image, build an animated ad or brand promo, turn a product into motion, or says 'make a motion', 'motion design', 'animate this', 'make a video from my logo', 'animated brand', 'motion graphics', 'brand motion', 'kinetic graphics', 'promo video', or 'ad video'. Drives a storyboard-first pipeline: brief → storyboard sheet (GPT Image 2) → video (Seedance 2.0) — an AI-generated pixel video clip. Distinct from higgsfield-motion (the named camera/motion preset library) and from higgsfield-vibe-motion (deterministic Remotion code with crisp text); use vibe-motion instead when the text/logo must stay perfectly crisp, editable, and deployable as code."
user-invocable: true
metadata:
  tags: [higgsfield, motion-design, animated-ad, logo-animation, brand, motion-graphics, storyboard, classicMD, highMD]
  version: 1.0.1
  updated: 2026-06-22
  parent: higgsfield
---

# Higgsfield Motion Design

A full motion-design creation flow run through the Higgsfield MCP connector. Follow the steps in order, be concise and direct, and **reply in the user's language**. This skill is the guided *ad/brand-motion* pipeline — for the named camera/motion preset library (Explosion, Werewolf, Air Bending, etc.) use `higgsfield-motion` instead.

> **Not a spec sheet.** Model parameter enums (resolutions, modes, durations) come from the specs layer / `models_explore` — verify there (HARD RULE #3), don't hardcode them here.

## QUICK FACTS
- Two flows: **classicMD** (smooth, elegant, cinematic) vs **highMD** (fast cuts, extreme dynamics, CGI energy) — pick before anything else [→](#step-0--determine-the-flow-type)
- Ask **all** brief questions in ONE message — never split intake into rounds [→](#step-1--brief-intake-one-message)
- Storyboard = **one** image: a single grid sheet with all N panels via GPT Image 2 — never N separate images [→](#step-3--generate-the-storyboard)
- Final video = **Seedance 2.0** (`seedance_2_0`); confirm the model id with `models_explore` if unsure [→](#step-4--generate-the-video)
- highMD rule: no realistic humans — silhouettes, chrome figures, or 3D abstract shapes only [→](#notes--rules)
- highMD rule: the logo lock is a static hold proportional to clip length (~1s / ~2s / ~2–3s for 5 / 10 / 15s) [→](#step-4--generate-the-video)

---

## STEP 0 — Determine the flow type

Identify which workflow applies before anything else:

- **classicMD** — standard ads, brand promos, service presentations, logo reveals, general atmospheric content. Smooth transitions, elegant typography, cinematic feel.
- **highMD** — sports promos, tech launches, music teasers, AI-capability demos, fashion drops. Extreme camera speed, aggressive cuts, peak dynamics; realistic people are replaced by silhouettes, chrome elements, or 3D abstract figures.

If the request makes the flow obvious, proceed silently. If ambiguous, ask once:
> "Which style fits your project better — **Classic Motion** (smooth, elegant, cinematic) or **Hyper / Kinetic** (fast cuts, extreme dynamics, CGI energy)?"

---

## STEP 1 — Brief intake (one message)

Ask all of these in a **single** message (never split into rounds). Save every answer before proceeding:

1. **Existing assets?** — Yes (upload logo / product photo / reference) · No (help me create the visual)
2. **Duration** — 5s (teaser / logo sting) · 10s (standard post / stories) · 15s (promo / product video)
3. **Frame format** — 16:9 (horizontal) · 9:16 (vertical Reels/TikTok/Stories) · 1:1 (square feed)
4. **Mood / style** *(free input)* — e.g. energetic, minimalist, luxury, technological, atmospheric, aggressive, cinematic
5. **Brand / product name and tagline** *(if any)*
6. **Storyboard frames** — 6 (standard) · 8 (detailed) · 9 (maximum coverage)

---

## STEP 2 — Asset handling

**If the user HAS assets:** when the client is an Apps UI-capable surface, call `media_upload_widget` immediately so they can attach the local file (remote MCP cannot read chat attachments). For a web media URL, call `media_import_url` first and pass the returned `media_id`. Then proceed to Step 3.

**If the user has NO assets:** generate a base visual with **GPT Image 2** (`generate_image`, model `gpt_image_2`) — construct the prompt from brand name, mood, style, palette, aspect ratio. Display the result with `job_display`, ask "Does this work or want changes?", regenerate if needed, then proceed once approved.

---

## STEP 3 — Generate the storyboard

The core creative step. Generate **one** storyboard sheet — a single image with all N panels in a grid (N = the count from Step 1: 6, 8, or 9). Do **not** generate N separate images.

Call `generate_image` **once** with **GPT Image 2**, passing the approved asset / base visual as a reference. Each panel must: stay visually consistent with the approved asset · represent a distinct moment (opening → build → climax → resolution → logo lock) · show camera position, subject state, motion blur/freeze where relevant · carry a 2–4 word burned-in caption (scene label, not subtitle).

- **classicMD panels:** smooth compositions, elegant typography zones, cinematic lighting.
- **highMD panels:** peak-action freeze frames — frozen splashes, shattered elements, material stretch, aggressive angles, neon contrast.

Prompt skeleton:
```
Storyboard sheet, [N] sequential panels in a grid, each labeled "Frame 1"…"Frame N".
Panel 1: [scene]. Panel 2: [scene]. … Panel N: [logo lock / brand name].
Each panel: [camera angle], [motion state], [mood/lighting]. Style: [cinematic / kinetic].
Consistent color palette throughout. Clean storyboard design, thin borders between panels.
```

Display with `job_display`, then present a short storyboard summary (Frame 1…N one-liners + Mood + Motion + Ending) and ask: **Approve ✅** or **Changes needed** (regenerate the sheet, repeat approval).

---

## STEP 4 — Generate the video

Once the storyboard is approved, generate the final video with **Seedance 2.0** (`generate_video`, model `seedance_2_0` — confirm the id via `models_explore` if unsure). Build the prompt from: the approved scene sequence, the flow type, duration + aspect ratio (Step 1), mood/style, and the brand name/slogan for the logo lock.

- **classicMD:** `smooth motion design, [scene flow], elegant transitions, [mood] atmosphere, cinematic camera movement, [duration]s, brand reveal at end: [brand], [aspect ratio]`
- **highMD:** `high-intensity kinetic motion, [scene flow], extreme camera speed, aggressive match-cuts, peak-action freeze frames, [mood] CGI aesthetic, neon contrast, [duration]s, hard-stop logo lock: [brand], [aspect ratio]`

For highMD, the final seconds must be a **static hold** on the brand/logo — build it into the prompt explicitly, scaled to clip length (~1s for 5s, ~2s for 10s, ~2–3s for 15s).

Pass as the start frame: the original uploaded asset if the user had one, otherwise the first approved storyboard frame's job id. Seedance 2.0 carries native audio by default and a `genre` hint — set `genre` to match the mood when useful (action/horror/comedy/noir/drama/epic). Display with `job_display`.

> **Resolution note:** Seedance 2.0 reaches 4K only in `mode=std`; `mode=fast` caps at 720p. See `higgsfield-seedance` / the specs layer.

---

## STEP 5 — Review & iterate

Present the render and ask: **Love it ✅** (done) · **Different edit** (regenerate, same storyboard) · **Different style** (back to Step 1) · **Another version** (a second variation with a slight prompt change).

---

## Notes & rules

- Ask **all** Step 1 questions at once; never split intake.
- **Storyboard = one grid image** via GPT Image 2; never N separate images. No separate moodboard step — go brief → storyboard.
- **Image model:** GPT Image 2 (`gpt_image_2`). **Video model:** Seedance 2.0 (`seedance_2_0`).
- **highMD:** no realistic humans — silhouettes, chrome figures, 3D abstract shapes only; logo-lock duration is proportional to clip length.
- **classicMD logo** can appear as opener, closer, or both — ask if unspecified.
- Tool names: `generate_image`, `generate_video`, `job_display`, `media_upload_widget`, `media_import_url`, `media_upload` / `media_confirm`, `models_explore`, `balance` — confirm exact ids with tool search if unsure. Check credits with `balance` if the user seems concerned about usage.
- Match the user's language throughout. If a generation fails, explain briefly and offer a retry with adjusted parameters.

## Related skills
- `higgsfield-motion` — the named camera/motion preset library (different skill)
- `higgsfield-vibe-motion` — deterministic Remotion **code** motion graphics (crisp text, exact colors, deployable). Use it instead of this skill when the text/logo must stay perfectly crisp and editable rather than be a rendered video clip.
- `higgsfield-gpt-image-2` — GPT Image 2 prompt craft for the storyboard sheet
- `higgsfield-seedance` — Seedance 2.0 prompt formula, modes, and preflight linter
- `higgsfield-marketing-studio` — one-click product-ad surface (alternative to this manual flow)
- `higgsfield-apps` — MCP connector tooling (media upload, job display, balance)
