---
name: higgsfield-models
description: >
  Use when the user asks which model to use, wants to compare models,
  or needs guidance on selecting between Kling, Sora 2, Wan, Seedance,
  Veo 3, Minimax Hailuo, Soul, Nano Banana, or other Higgsfield engines.
user-invocable: true
metadata:
  tags: [higgsfield, models, Kling, Sora, Wan, Seedance, Veo, Soul, NanoBanana, v2.0.2]
  version: 3.0.0
  updated: 2026-04-06
  parent: higgsfield
---

# Higgsfield Model Selection Guide

Higgsfield hosts multiple generation engines. Choosing the right one is the single
biggest factor in output quality after the prompt itself.

---

## Video Models

The Kling lineup in Higgsfield spans two generations (2.x and 3.0) plus the O1 reasoning tier, and includes a dedicated **Edit Video** tab for video-to-video transformation. Understanding which tier and which mode (Create vs Edit) to use is critical.

---

### Kling 3.0 ⭐ EXCLUSIVE — Current Top Model
**Duration:** 3s–15s · **Resolution:** 1080p + 4K HDR · **FPS:** 30fps (60fps in some configurations) · **Audio:** Native
**Best for:** Cinematic realism · character drama · long sequences · multi-shot storytelling · native audio dialogue
**Strengths:** Longest clip duration on the platform (up to 15s) · native multilingual audio (English, Chinese, Japanese, Korean, Spanish + accents) · superior subject consistency · precise text rendering in video · physics-aware motion (object interactions, hugging, fighting, complex machinery) · AI Director mode understands shot-reverse-shot, cross-cutting, camera blocking from a prompt alone · stylized output engine for anime, Pixar/claymation, felt/fabric textures
**Use when:** You need a long cinematic clip with audio, multi-shot narrative, or high-consistency character performance

**Multi-shot generation:** Up to 6 camera cuts in a single generation. Per-shot control over duration, shot size, perspective, narrative content, and camera movement. Describe an entire sequence in one prompt — model generates a coherent multi-shot video with edited camera cuts, not just a single clip.

**Audio:** Native audio-visual co-generation — dialogue, SFX, and ambient sound are generated WITH the video in a single pass, not layered after. Specify dialogue in quotes, ambient sound, and SFX — all generated natively alongside the video.

**Voice Binding:** Lock specific voice profiles to specific characters for consistent vocal identity across shots.

**Multilingual audio:** English, Chinese, Japanese, Korean, Spanish — including regional accents (American English, British English, Indian English).

**Multi-character dialogue:** 3+ characters with correct speaker attribution and lip-sync per character.

**Physics engine:** Gravity, inertia, weight transfer, collision detection, cloth dynamics, hair movement, fluid behavior — all simulated for realistic motion.

**Output:** 1080p standard + 4K HDR, 30fps (60fps in some configurations).

**Professional export:** 16-bit HDR, linear EXR sequences (compatible with Nuke, After Effects, DaVinci Resolve).

**Text rendering:** Legible signage, logos, CTAs preserved throughout motion sequences.

**Elements system:** Upload reference images to lock character identity across shots. Use `@element_name` syntax (Elements 3.0 tagging) for cross-shot subject consistency.

**Prompt note:** Treat the prompt like a script: describe action, camera, mood, and dialogue cues together. Optimal prompt length: 100–200 words.

**Sequential action syntax (3.0-specific):** Use "first / then / finally" structure for multi-step scenes.

**Motion endpoint pattern:** Append "returns to starting position" or "then settles" to prevent stuck-at-99% generation hang.

```
Example use case: A 12-second scene — a detective enters a rain-soaked alley, hears a
noise, turns to camera. Two cuts. Footsteps, rain ambiance, tense score.
→ Kling 3.0
```

---

### Kling 3.0 Omni ⭐ EXCLUSIVE
**Duration:** 3s–15s · **Resolution:** 4K · **FPS:** 60fps · **Audio:** Native
**Best for:** Reference-driven generation · video-based character cloning · custom multi-shot storyboards · maximum consistency workflows
**vs Kling 3.0:** Same generation quality. Omni = more control knobs. 3.0 = AI auto-directs from prompt alone. Omni = you control per-shot.
**Key features:**
- **Performance Cloning** — Upload a 3–8s reference video. Model extracts the character's visual traits AND voice. Re-renders them in new scenes with full identity and audio fidelity. Act out a scene on camera → AI re-renders with your character in a new setting, preserving likeness and voice.
- **Video Element referencing** — Upload a 3–8s reference video to extract visual traits AND voice simultaneously. Goes beyond static image references.
- **Voice Extraction from static images** — Upload a character image + 3s audio clip → builds a voice profile for that character
- **Custom storyboard** — Specify duration, shot size, perspective, narrative content, and camera movement per shot. Director-level granular control across a full multi-shot sequence.
- **Multi-character coreference** — 3+ characters maintained across shots with consistent identity.
- **Elements 3.0** — Most advanced version of the character/object reference system. References video clips, not just static images, for deeper identity lock.
- **Video-to-video** — Reshaping existing footage as a primary mode. Upload source footage and transform it while preserving motion structure.
- **Natural language editing** — Add, remove, or transform elements without leaving the generation flow.

**V3 vs O3 selection guidance:** Use V3 (Kling 3.0) for prompt-driven cinematic work — text-to-video, image-to-video where the prompt is the primary creative driver. Use O3 (Kling 3.0 Omni) when you have reference media (video or image+audio) to anchor character identity.

**Use when:** You need to clone a character's appearance and voice from reference footage, or you want per-shot storyboard control rather than AI auto-direction

```
Example use case: Upload a 5s selfie video of yourself speaking → clone your likeness
and voice → generate a 15s branded ad campaign with your AI double in a studio setting.
→ Kling 3.0 Omni
```

---

### Kling 3.0 Omni Edit ⭐ EXCLUSIVE
**Duration:** 3s–10s input · **Resolution:** 1080p
**Best for:** Transforming existing video with reference-guided edits at 3.0 quality
**What it does:** Upload existing footage → describe or show the change → model applies it while preserving original motion, camera angles, and scene structure. 3D spatial awareness means edits respect lighting geometry and don't break scene coherence.
**Use when:** You have footage you want to restyle, relight, or transform with the power of the 3.0 Omni architecture

---

### Kling 3.0 Motion Control ⭐ NEW (March 25, 2026)
**Duration:** 3s–30s · **Resolution:** 1080p
**Best for:** Reference-video motion transfer · full-body choreography · complex dance/action sequences · talking head with precise gestures

**Core capability:** Upload a 3–30s reference clip → model transfers full-body motion capture, hand gestures, facial expressions, and complex choreography to a new character or scene.

**Two orientation modes:**
- **Image Orientation** — Camera movements, talking head, static body. Best for dialogue, presentations, upper-body content.
- **Video Orientation** — Complex motions like dancing, action sequences, full-body movement. Best for choreography, sports, physical performance.

**Element Binding:** Connects facial identity to motion data for stable face during movement. Prevents face drift that normally occurs during fast or complex motion.

**Camera sync:** Pans, tracking shots, and zoom are synced from the reference clip — the output inherits the reference video's camera work.

**Audio passthrough:** Option to preserve the reference video's audio in the output.

**Prompt note:** Describe camera direction + scene context in the prompt — the reference video handles the movement. Don't describe the motion itself; let the reference clip drive it.

**Use when:** You need camera motion control over a longer duration than standard models allow, or you need to transfer specific human motion from a reference performance

```
Example use case: Upload a 15s dance clip → transfer the choreography to an anime
character in a neon-lit cityscape. Reference video drives all motion; prompt sets the scene.
→ Kling 3.0 Motion Control
```

---

### Kling O1 Video (Legacy)
**Duration:** 5s–10s · **Resolution:** 1080p
**Best for:** Reference-based generation · character-consistent multi-shot sequences · start/end frame controlled motion · up to 7 simultaneous reference inputs
**Strengths:** Chain-of-Thought (CoT) reasoning — model "thinks" before rendering, breaking the prompt into scene elements, motion paths, lighting plan, then executing. Handles complex multi-element prompts reliably. Up to 7 reference inputs simultaneously (characters, props, environments).
**Start/End Frame mode:** Upload a start image + end image → model generates the precise motion between them. Perfect for morphs, transitions, connecting two distinct scenes.
**Motion transfer:** Upload a reference video → model extracts the exact motion path and applies it to a new character or scene
**Use when:** You need complex multi-reference generation, or you want deterministic control over how a clip starts and ends

```
Example use case: 5 reference images (2 characters, 1 outfit, 1 location, 1 prop) →
a single coherent scene where all elements appear correctly.
→ Kling O1 Video
```

---

### Kling O1 Video Edit (Legacy — Edit Video tab)
**Input video:** 3–10s · **Resolution:** 720p output · **Cost:** ~9 credits
**Interface:** Separate "Edit Video" tab (not in the main model list) — upload existing video + optional up to 4 image/element references + text prompt
**Auto settings toggle:** On = model determines best edit parameters automatically

**What it does:** Transforms existing footage using natural language instructions. No masking, no tracking, no rotoscoping — describe the change and the model applies it across all frames while preserving original motion structure, camera angles, and spatial relationships.

**Edit types:**
- **Relight & Atmosphere** — Change daytime to dusk, add cinematic lighting. Model understands 3D geometry to adjust light and shadow realistically across the scene. (This is the featured capability shown in the UI — carousel of lighting presets)
- **Restyle** — Full aesthetic transformation: realistic → anime → cyberpunk → vintage → watercolor. Preserves faces, objects, composition, and motion.
- **Object swap** — Replace any element: turn a cat into a wolf, change an outfit, swap a prop. Handles substitution naturally across all frames.
- **Add elements** — Insert new objects, effects, or environmental details (flames, rain, crowds, weather)
- **Delete / remove** — Remove background distractions, bystanders, logos, objects — no manual masking
- **Scene transformation** — Change environment entirely (location, time of day, weather, era) while keeping character identity and camera motion intact
- **Angle change** — Fix shots filmed at the wrong angle by generating the same scene from a new perspective
- **Character/head replacement** — Swap characters or transform them (human → robot, alien, monster)

**The Keep Rule (critical for edit prompts):** Always specify what to preserve. Formula: `Change [Target] to [New State], keep [everything else] unchanged`

**Example edit prompts:**
- "Change the lighting to golden hour dusk, keep the character and camera motion unchanged"
- "Restyle the footage as 1970s film grain with warm tones, keep all motion and composition"
- "Remove the person in the background, keep everything else exactly as is"
- "Change her jacket to red leather, keep her face, hair, and movement unchanged"
- "Transform the street scene to a rainy night, wet reflections, moody lighting, keep character identity"

**Use when:** You have real or AI-generated footage and want to transform it without reshooting. This is the primary video editing workflow in Higgsfield.

---

### Kling 2.6 (Legacy — use Kling 3.0 for new work)
**Duration:** 5s–10s · **Resolution:** 1080p
**Best for:** Cinematic realism · character drama · emotional scenes · dialogue moments
**Strengths:** Natural human motion, subtle facial expressions, strong character consistency
**Use when:** You need a real-feeling scene with a person as the focal point and don't need the longer duration or audio of 3.0
**Prompt note:** Works beautifully with Dolly In, Arc, and Head Tracking controls

```
Example use case: A woman receives unexpected news at a café — close-up reaction shot,
natural lighting, emotional authenticity needed.
→ Kling 2.6
```

---

### Kling 2.5 Turbo
**Duration:** 5s–10s · **Resolution:** 1080p
**Best for:** Fast iteration on Kling-quality output · when speed matters more than maximum quality
**vs 2.6:** Same duration, faster generation, slightly lower quality ceiling
**Use when:** You're iterating through many prompt variations quickly and want to select the best before committing to a 2.6 or 3.0 render

---

### Kling 2.1 / Kling 2.1 Master (deprecated)
**Duration:** 5s–10s · **Resolution:** 1080p
**Best for:** Legacy workflows · lower cost when 2.5/2.6 quality isn't required
**2.1 Master:** Higher quality tier of the 2.1 generation — better motion fidelity than standard 2.1
**Note:** Older generation. Use 2.6 or 3.0 for current work unless cost is the constraint.
**⚠ Deprecated:** Removed from the platform as of March 2026. Use Kling 2.6 (legacy) or Kling 3.0 for current work.

---

### Audio Speaker Attribution Format (V3, O3, 2.6)

Use this format when prompting dialogue scenes with multiple speakers, sound effects, and ambient audio:

```
[Speaker: Character Name] "dialogue" in a [warm/confident/excited] [male/female] voice with [accent].
Add [sound: footsteps / rain / door closing] when [action].
Background ambient: [environment description].
```

---

### Multi-Shot Storyboard Format (V3/O3 only)

Use this format for multi-shot sequences with per-shot control:

```
Shot 1 ([Xs]): [Wide establishing shot]. Camera: static.
Shot 2 ([Xs]): [Medium shot, action begins]. Camera: slow push in.
Shot 3 ([Xs]): [Close-up, reaction or detail]. Camera: static.
Shot 4 ([Xs]): [Resolution]. Camera: tracking / pull back.
```

---

### Sora 2
**Best for:** Epic scale · long sequences · complex physics · action blockbuster feel
**Strengths:** Best-in-class for large-scale events — crowds, explosions, environment scale
**Weaknesses:** Characters can lose fine facial consistency over long clips
**Use when:** The scene is about spectacle, scale, or physics-heavy action
**Prompt note:** Pairs perfectly with Crane Up, 360 Orbit, and Super Dolly Out

```
Example use case: A skyscraper collapse scene from street level — massive scale, chaos,
debris, crowd fleeing.
→ Sora 2
```

---

### Wan 2.5 / Wan 2.6
**Best for:** Stylized / artistic output · fantasy · surreal · creative experimentation
**Strengths:** Excellent at non-photorealistic aesthetics, painterly looks, unusual styles
**Weaknesses:** Less photorealistic than Kling for human faces
**Use when:** The visual style matters more than strict realism
**Prompt note:** Pair with Abstract or Anamorphic visual style for best results

```
Example use case: A watercolor-style fantasy warrior emerging from mist.
→ Wan 2.5
```

---

### Seedance 2.0 — Most Advanced Seedance Tier
**Duration:** 4–15s · **Resolution:** 720p / 1080p / 2K · **Audio:** Native
**Best for:** Maximum multimodal reference control · complex motion · character consistency across scenes · professional production assets · content requiring audio-visual synchronization
**Architecture:** Unified multimodal audio-video joint generation — text, image, audio, and video all processed simultaneously in one pass (not layered)
**Status:** Coming soon to Higgsfield — document is ready for when it ships

> **⚠️ Feb 2026 platform note:** Real person face uploads are blocked. Real-celebrity likenesses, named franchise characters, and named anime/game characters trigger content filters. Use archetype descriptions and @Tag references instead. The Official Volcengine API is delayed. Web platform (Jimeng/Dreamina) is live; Higgsfield integration is incoming.

---

#### The Rule of 12 — Asset Budget

The defining feature of Seedance 2.0 is its multimodal input system. Every generation can accept up to **12 total assets**:

| Asset type | Max count | Limit |
|---|---|---|
| Images | 9 | JPG/PNG/WEBP, <30 MB each |
| Video clips | 3 | **15s TOTAL** across all 3 clips (not 15s each) |
| Audio files | 3 | **15s TOTAL**, MP3 only, <10 MB each |
| **Total files** | **12** | — |

The model reads each asset's role from your prompt. A bare `@Image1` with no instruction is weak — always assign a job:

```
@Image1's character as the subject
@Image2 as the background/environment lock
@Image3 as the last frame
Reference @Video1's camera movement throughout
BGM references @Audio1
Voice timbre references @Audio1
```

---

#### Generation Modes

| Mode | Code | Input |
|---|---|---|
| Text to Video | T2V | Prompt only |
| Image to Video | I2V | Prompt + images |
| Video to Video | V2V | Prompt + video clips |
| Reference to Video | R2V | Prompt + mixed assets |

**V2V has two distinct behaviors — be explicit:**
- `Reference @Video1's camera movement` → generate new content using that technique
- `Replace the character in @Video1 with @Image1` → directly modify the source video

These trigger different model pathways. Specifying which you want is critical.

---

#### Prompt System — The Five-Layer Stack

Build every prompt in this order. The model weights early words heavily — subject and action must come first.

```
1. SUBJECT   — who/what (identity via @Tag if using references)
2. ACTION    — primary verb + physics/timing (one action only per shot)
3. CAMERA    — framing + movement + speed + angle
4. STYLE     — 2–3 tokens max (film language, not adjectives)
5. SOUND     — ambient + SFX + music + silence decision
```

**The 6-Part Field Formula** (validated across 10,000+ generations):
```
[SHOT TYPE] + [SUBJECT] + [ACTION] + [STYLE] + [CAMERA MOVEMENT] + [AUDIO CUES]
```

**Delegation levels** — choose by complexity:

| Level | Length | Use when |
|---|---|---|
| 1 | ≤30 words | Known domains — food, sports, everyday. Let model direct. |
| 2 | 30–100 words | Subject + action + environment + camera note + style anchor |
| 3 | 100–300 words | Time-segmented: `0–3s: ... 3–7s: ... 7–END: ...` |
| 4 | 300–1000+ words | Full choreography — fight scenes, lip-sync, product demos |

**Level 1 example** — model auto-directs everything:
```
生成一个精美高级的兰州拉面广告，注意分镜编排
```

**Level 2 example:**
```
@Image1 character identity.
Young woman in red coat walks along rain-soaked street.
Slow tracking follow, medium shot. Neon reflections on wet pavement.
Soft rain ambience.
```

**Level 3 example:**
```
@Image1 character. @Image2 background lock.
0–3s: stands at window, back to camera, static wide.
3–7s: turns slowly, uncertain expression. Slow push-in to medium close-up.
7–10s: direct eye contact. MCU locked. Soft piano enters.
Golden side key, soft fill. Desaturated cinematic palette.
```

**Level 4 example** (fight choreography):
```
@Image1 Fighter A (black jacket). @Image2 Fighter B (grey hoodie).
A throws right hook → B ducks → B counters with left uppercut → A stumbles back.
Rooftop at night. Wet concrete. Neon signs background.
Handheld low-angle, whip-pan to follow impact at 4s.
0–4s slow-motion 0.3×; 4–8s real-time; 8–10s 0.5× snap on impact.
Hard side light, practical neon fill.
Crowd ambient SFX, impact punch SFX at 4s and 8s.
Maintain character identity throughout.
```

---

#### Prompt Hygiene — Anti-Slop Rules

Delete these words — they add no information the model can act on:

`cinematic` · `epic` · `masterpiece` · `ultra-real` · `stunning` · `breathtaking` · `8K` · `award-winning` · `immersive` · `ethereal`

**The one test:** Can a camera, light meter, or stopwatch measure this word? If no → delete it.

Replace with observable controls:

| ❌ Delete | ✅ Replace with |
|---|---|
| cinematic lighting | single hard key 45° camera-left, warm amber, deep shadow |
| epic scene | wide shot, dolly pull reveals environment, brass swell at 4s |
| stunning sunset | warm backlight 3200K, 5 min post-horizon, long silhouette shadows |
| high quality | stable exposure, no flicker, clean edges |

---

#### Camera Control

Every Level 2+ prompt needs all four camera parameters:

```
Framing:  wide / medium / close-up / ECU / over-shoulder / full body
Move:     locked-off / dolly push / dolly pull / pan / tilt / orbit /
          handheld / crane / tracking
Speed:    slow / moderate / "over 8 seconds" (use duration, not speed words)
Angle:    eye level / low angle / high angle / bird's eye / Dutch
```

**Reliable phrasing:**
```
locked-off static camera, no movement
slow dolly push from medium shot to tight close-up over 8 seconds
slow orbit left around the subject, constant distance
handheld tracking following the subject, subtle shake, not chaotic
Hitchcock zoom (dolly out while zooming in)
crane shot rising from ground level to overhead
```

**Anti-drift rules:**
- Never combine mutually exclusive moves: `locked-off + handheld`, `orbit + pan`, `tilt + dolly push`
- One camera move per shot only
- For subjects moving relative to camera (riding, flying): `CAMERA MOUNTED ON [SUBJECT], LOCKED-ON SHOT`

**One-Take technique** (一镜到底) — upload 3–5 scene images as sequential waypoints:
```
@Image1 @Image2 @Image3 @Image4, one continuous tracking shot,
following the runner from the street up stairs, through a corridor,
onto the rooftop. Single continuous shot, no cuts throughout.
```

**Nine-Grid storyboard method** — when text becomes unwieldy, generate a 3×3 storyboard image as @Image1, then:
```
Strictly follow the storyboard sequence from @Image1.
[Character from @Image2] performs the actions shown.
Match lighting and camera angles per panel. Smooth transitions between scenes.
```

---

#### Audio — Rules and Failure Modes

**Platform hard limits:**
```
Format:    MP3 only. WAV/AAC/OGG/FLAC/M4A → silent failure with no error message
Duration:  ≤15s per clip. Sweet spot: 3–8s for best sync
Budget:    3 audio files max (part of Rule of 12)
Bitrate:   128–320 kbps
Size:      ≤10 MB per file
```

**Negative prompts:** NOT SUPPORTED. Use positive constraints only:
```
❌  --no watermark --no distorted hands
✅  clean background, stable hands, no overlaid text
```

**Dialogue and lip-sync** — two pathways:

Text-driven (most reliable):
```
Character says: "We leave at dawn."
Framing: medium close-up, locked-off camera.
```

Audio-driven:
```
Upload MP3 as @Audio1.
Prompt: "Lip-sync matches @Audio1 exactly. Camera: medium close-up, locked."
```

**Key lip-sync rules:**
- Keep audio clips 3–8s for best accuracy (15s is the technical limit, not the sweet spot)
- Remove all head/face motion tokens from prompt — `nodding`, `turning head` compete with the lip engine
- Audio must be clean — background noise and reverb degrade phoneme recognition
- Speech slightly slower than natural pace improves sync accuracy
- One face per reference image — multiple faces break audio routing

**Timestamp anchoring** (when model replaces your audio):
```
Audio @Audio1 plays exactly as uploaded from 0s to end. Do not modify or replace the audio content.
```
Then remove all ambient/SFX/music tokens from the prompt — they invite the generative audio engine to override.

**Multi-character lip-sync — known limitation:**
ByteDance's own release notes state multi-person lip-sync matching is an unresolved problem. The workaround: generate each character separately with their own audio segment, then composite in CapCut/Premiere using picture-in-picture + linear mask (15–20% feather). Static image for the listening character; generated video for the speaking character.

**⚠️ Critical platform distinction:**
The Jimeng platform hosts two separate tools. Seedance 2.0 is the **Video Generation** tool. The **Digital Human (数字人)** tool uses OmniHuman-1 and has Master/Quick/Standard lip-sync modes. These modes do NOT exist in Seedance 2.0. Do not mix them up.

---

#### Character Identity

**Character card format** — write once, reuse across all prompts:
```
[Name]: [age range], [build], [skin tone], [hair style/color],
[defining features], [wardrobe], [emotional energy].
```

**Identity anchoring:**
```
@Image1's character as the subject                     ← specific role
@Image1 for facial features and clothing               ← explicit instruction
Use @Image1 and @Image2 for multiple angles            ← 360° coverage
```

**Multi-character pattern** — attribute every action by name, never use ambiguous pronouns:
```
Character A references @Image1.
Character B references @Image2.

Character A throws a right punch at Character B.
Character B blocks with crossed arms.
```

**360° consistency test:** Before committing to a character reference, generate them from front, side, three-quarter, and back. If identity holds across all angles → production-ready.

**Hand safety:** If hands aren't essential to the action, frame waist-up or add `"hands not in frame."` For essential hand shots: one simple action only (`picks up the glass`, `open palm facing camera`).

---

#### Beat Density — Motion Timing Rules

Too many events in one clip causes jitter and morphing:

| Duration | Max changes |
|---|---|
| 4–6s | 1 primary change |
| 8–10s | 1–2 changes |
| 12–15s | 2–3 changes (use timestamps) |

For Level 4 fight choreography: 6–8 beats per 5 seconds is achievable with precise per-beat specification.

---

#### Genre Templates — Ready-to-Use Starters

**Product ad (Level 2, T2V/I2V):**
```
[Product] hero-shot on [surface]. Camera slow orbit 90°.
Soft studio key, rim highlight, no fill. Macro depth-of-field.
No text. No people.
```

**Fight scene (Level 4, R2V):**
```
@Image1 [Fighter A]. @Image2 [Fighter B].
A throws [strike] → B blocks → B counters with [move].
[Location]. Handheld low-angle, whip-pan to follow impact.
Slow-motion 0–4s, real-time 4–10s.
Impact SFX at peak contact.
```

**Short drama dialogue (Level 3, I2V):**
```
@Image1 [Character A]. @Image2 [Character B].
A speaks [emotion]: "[line]" — cut to B reaction.
Over-the-shoulder medium shots alternating.
Interior [location], practical lamp key.
Sync lip movement to @Audio1.
```

**Music beat sync (Level 3, R2V):**
```
@Image1 through @Image6 are scene images.
@Audio1 provides rhythm and beat reference.
Cut scene transitions on musical downbeats.
Characters move with energy matching the music tempo.
Visual pacing: fast during chorus, slower during verse.
```

**Architecture walkthrough (Level 2, I2V):**
```
@Image1 building exterior reference.
Drone approaches from south at 40m altitude, slow descent.
Enters through glass lobby — interior reveal.
Golden hour warm light, clear sky. No people.
```

---

#### Compliance — Copyright and Content Policy

Before every generation, run this check:

| Gate | Check | If fail |
|---|---|---|
| Name | Real person named? | Remove name → use archetype |
| IP | Franchise/character named? | Use visual descriptor only |
| Audio | Named song/composer? | Describe texture/tempo/instrumentation |
| Scene | Specific copyrighted scene? | Reframe generically |
| Logo | Recognizable logo? | Describe geometry only |

**Substitution method — describe the look, never the name:**
```
❌ Iron Man          ✅ red-and-gold metal exoskeleton warrior, circular blue chest reactor, sleek helmet
❌ Spider-Man        ✅ blue-and-red form-fitting suit, face masked with eye-shaped lenses, web fired from wrists
❌ Eiffel Tower      ✅ iron lattice tower with illuminated night display
❌ Bohemian Rhapsody ✅ operatic rock build, piano into power chords, multi-voice choir
```

---

#### Quick Reference — Emergency Fixes

| Problem | Fix |
|---|---|
| Chaotic output | Shorten to ≤50 words; add `locked-off static camera`; one action only |
| Character drifts | Add `@Image1` + `maintain character identity from @Image1` |
| Camera wanders | Specify one explicit move or `locked-off static camera` |
| Background morphs | Add environment `@Image2` + `environment locked: [location]` |
| Audio desyncs | Trim to <10s; remove head-motion tokens; clean the audio file |
| Model replaces audio | Add timestamp anchoring phrase; remove all ambient/music tokens |
| Content blocked | Remove real name/face → use archetype descriptor |
| Lip-sync fails silently | Check audio format — MP3 only; WAV/AAC fail with no error |

---

#### Platform Parameters (Higgsfield — Coming Soon)

```
Duration:      4–15s
Resolution:    720p / 1080p / 2K
Aspect ratios: 16:9 · 9:16 · 4:3 · 3:4 · 21:9 · 1:1
Audio format:  MP3 only
Generation:    Native audio-video joint (single pass)
```

```
Example: Upload reference choreography video + 2 character images + music MP3
→ 10-second synchronized scene at 2K with matched audio.
→ Seedance 2.0
```

---

### Seedance 1.5 Pro
**Duration:** Up to 10s · **Resolution:** 1080p · **Audio:** Native
**Best for:** Native joint audio-video generation · multilingual dialogue and lip-sync · cinematic camera control with audio · character narratives requiring SFX + BGM + speech in one pass
**Architecture:** Dual-branch Diffusion Transformer — generates audio and video simultaneously in a single pass (not layered on top after the fact). This is the key architectural differentiator — eliminates lip-sync mismatches and produces spatially accurate sound without post-production.

**Audio capabilities (class-leading at this tier):**
- **Multilingual lip-sync** — English, Chinese (incl. dialects: Sichuanese, Cantonese, Taiwanese Mandarin, Shanghainese), Japanese, Korean, Spanish, Indonesian. Accurate prosody and regional vocal patterns, not just translation.
- **Multi-character dialogue** — multiple characters can speak different languages in a single scene. Model correctly assigns lip motion to the right character.
- **Audio types** — speech, singing, non-verbal vocalizations (laughter, gasps), environmental SFX, background music. All generated natively in sync with visuals.
- **Audio expressiveness** — balanced, controlled emotional alignment. More stable than Sora 2's expressive audio, better for professional tone control.
- **Audio-visual sync** — outperforms Kling 2.6 and Veo 3.1 on lip-audio synchronization benchmarks (SeedVideoBench 1.5 internal evaluation)

**Video capabilities:**
- Autonomous camera scheduling — continuous long takes, dolly zooms (Hitchcock zoom), orbital/arc/tracking shots
- Scene transitions and professional color grading
- Precise prompt intent understanding — model creatively fills narrative gaps while preserving your core intent (not just keyword matching)
- Emotional micro-expression continuity across shots — preserves character performance even in dialogue-minimal segments
- Strong in stylized scenarios: comedy timing, theatrical/opera performance styles, dramatic short dramas

**Use when:** Your content requires synchronized speech, SFX, or BGM in the video output. If audio is critical to the result, this or 2.0 is the correct tier. Pure visual content without audio requirements → use Seedance Pro for speed.

**Prompt note:** Include audio intent in the prompt — specify dialogue content, SFX expected, BGM mood, and language/dialect if non-English.

```
Example use case: A 10-second dramatic short drama scene — character delivers a line in
Cantonese, rain SFX, tense orchestral BGM, orbital camera pull-back.
→ Seedance 1.5 Pro
```

---

### Seedance Pro
**Duration:** Up to 10s · **Resolution:** 1080p (Pro) / 720p (Lite) · **Audio:** ❌ No native audio
**Best for:** Fast, high-quality multi-shot videos · VFX presets · cinematic camera control · rapid iteration · when audio is not required
**Versions:** Pro (1080p) and Lite (720p) — same model, different resolution/cost tiers
**Strengths:** Fastest Seedance generation, strong cinematic camera control, VFX presets, native multi-shot output
**Use when:** Speed and iteration matter more than audio, or when audio will be added in post-production
**vs 1.5 Pro:** No native audio — but faster generation and lower cost. Same family, different tier.

```
Example use case: Fast concept video — 5 visual directions for a brand campaign,
iterate quickly before committing to a full 1.5 Pro or 2.0 render with audio.
→ Seedance Pro
```

---

---

## Google Veo Family

Four models in Higgsfield, all generating at 1080p with native audio (Veo 3 and 3.1 series). Use the UI screenshot tiers to orient: Veo 3.1 Fast → Veo 3.1 → Veo 3 Fast → Veo 3.

---

### Veo 3.1
**Duration:** 4s / 6s / 8s · **Resolution:** 1080p (4s–8s) · **Audio:** ✅ Native · **Aspect:** 16:9 / 9:16
**Best for:** Highest-quality Veo output · reference image consistency · first/last frame interpolation · video extension · portrait video · complex dialogue scenes
**Model code:** `veo-3.1-generate-preview`

**What's new in 3.1 vs Veo 3 — the key additions:**

**Reference images (up to 3, Veo 3.1 exclusive):**
Upload up to 3 asset images to lock subjects, characters, or products across your video. Each image gets `reference_type: "asset"`. Use it to maintain a character's face, outfit, and prop together in one generation — the model preserves the subject's appearance throughout.

```
Reference images example:
  - dress_image → preserve the fashion garment
  - woman_image → preserve the character's face
  - glasses_image → preserve the accessory
→ All three maintained consistently in the output video
```

**First + last frame interpolation (Veo 3.1 exclusive):**
Specify both the opening and closing frame images. The model generates the motion between them. Critical constraint: when using reference images or first/last frames, duration must be 8 seconds and resolution 1080p.

**Video extension (Veo 3.1 exclusive):**
Extend any Veo-generated video by 7 seconds, up to 20 times (max 148s total). Input must be 720p (extension is 720p-only — downres before extending if needed). Videos are stored 2 days; the storage timer resets each time a video is referenced for extension. Voice extension only works if audio is present in the last 1 second of the source clip.

**Portrait video (9:16):**
Full portrait mode support. Landscape is the default (16:9).

**Resolution options:**
- 720p: default, supports all durations, required for extension
- 1080p: 8 seconds only
- 4K: 8 seconds only, higher latency, higher cost

**Audio generation:**
Native — dialogue, SFX, ambient sound, and music generated in a single pass. Use quotes for dialogue: `"This must be it," he murmured.` Describe SFX explicitly: `tires screeching loudly`. Describe ambient as environment soundscape.

**Negative prompts:** Supported. Describe what you don't want to see — no instructive language (`no walls` → `wall, frame`).

**Prompt elements for Veo:**
```
Subject:         the main focus — object, person, animal, scenery
Action:          what the subject is doing
Style:           sci-fi / film noir / cartoon / documentary
Camera:          dolly shot / aerial view / POV / eye-level / tracking
Composition:     wide shot / close-up / two-shot
Focus/lens:      shallow focus / macro lens / wide-angle lens
Ambiance:        blue tones / warm tones / night / sunrise
Audio (Veo 3+):  dialogue in quotes / SFX descriptions / ambient soundscape
```

**Strengths vs competitors:** Exceptional environmental realism (water, fire, weather, biology). Strong photorealistic and cinematic quality. Dialogue + audio generation is competitive with Seedance 1.5 Pro for English-language content.

**Weaknesses:** Character acting less nuanced than Kling. Multi-character lip-sync limited vs Seedance (single-character is more reliable). Reference image system (up to 3) is less flexible than Seedance 2.0's 12-asset Rule of 12.

```
Best use cases:
- Photorealistic nature / landscape / environmental hero shots
- Character + wardrobe + product consistency across a scene (reference images)
- Precise motion interpolation between two defined frames
- Long-form content via extension chain (up to 148s)
- Portrait social content (9:16)
→ Veo 3.1
```

---

### Veo 3.1 Fast
**Duration:** 4s–8s · **Resolution:** 1080p · **Audio:** ✅ Native · **Aspect:** 16:9 / 9:16
**Best for:** Rapid iteration · A/B testing · social media volume · speed-over-quality workflows
**Model code:** `veo-3.1-fast-generate-preview`
**Same capabilities as Veo 3.1** (reference images, first/last frames, extension, portrait) at lower latency and lower cost. Use when you need to iterate quickly or generate at volume before committing to a full Veo 3.1 render.

```
Use when: Rapid concept testing, high-volume social content, backend
ad generation pipelines that need speed over maximum quality.
→ Veo 3.1 Fast
```

---

### Veo 3
**Duration:** 4s / 6s / 8s · **Resolution:** 720p / 1080p (16:9 only for 1080p) · **Audio:** ✅ Native · **Aspect:** 16:9 / 9:16
**Best for:** Photorealistic nature · documentary · landscape · scientific visualization · audio-driven scenes
**Stable model** — production-grade, not preview. No reference images (3.1 exclusive). No video extension (3.1 exclusive). No first/last frame (3.1 exclusive).
**Strengths:** Same native audio generation as 3.1 (dialogue, SFX, ambient). Exceptional environmental realism — water, fire, weather, biology. 1080p at 16:9 only (no portrait 1080p).
**Use when:** The environment or phenomenon is the hero, you don't need reference image consistency, and stable (non-preview) model status matters.

```
Example: A timelapse of storm clouds forming over the ocean,
thunder rolling in, rain beginning to fall on the dark water surface.
→ Veo 3
```

---

### Veo 3 Fast
**Duration:** 8s · **Resolution:** 1080p · **Audio:** ✅ Native · **Aspect:** 16:9 / 9:16
**Best for:** Fast, good-quality video with audio · volume content · rapid prototyping
**Stable model**, optimized for speed. Same audio capabilities as Veo 3. Use when Veo 3 quality is sufficient and generation speed matters.

---

#### Veo Model Comparison

| | Veo 3.1 | Veo 3.1 Fast | Veo 3 | Veo 3 Fast |
|---|---|---|---|---|
| Audio | ✅ | ✅ | ✅ | ✅ |
| Reference images (up to 3) | ✅ | ✅ | ❌ | ❌ |
| First/last frame | ✅ | ✅ | ❌ | ❌ |
| Video extension | ✅ | ✅ | ❌ | ❌ |
| 4K output | ✅ | ✅ | ❌ | ❌ |
| Portrait (9:16) | ✅ | ✅ | ✅ | ✅ |
| Negative prompts | ✅ | ✅ | ✅ | ✅ |
| Status | Preview | Preview | Stable | Stable |
| Speed | Standard | Fast | Standard | Fast |

**Duration constraint:** When using reference images, first/last frames, or 1080p/4K → duration must be 8s.
**Extension constraint:** Input must be 720p. Output combines original + extension up to 148s total.

---

---

## Grok Imagine (xAI / Aurora)

Grok Imagine on Higgsfield consists of `grok-imagine-video` for video generation and editing. The `grok-imagine-image` model is available via the xAI API directly but is not currently in the Higgsfield platform UI. Both are powered by Aurora — xAI's autoregressive mixture-of-experts architecture that predicts the next token from interleaved text and image data. This is architecturally distinct from diffusion models (Flux, SDXL, etc.) — Aurora generates tokens sequentially, giving it tighter compositional control and stronger multi-element scene understanding.

**Aurora architecture key strengths:**
- Photorealistic rendering with detailed textures, convincing lighting, sharp compositions
- Precise text and logo rendering — one of the weakest areas for most image generators, Aurora handles it reliably
- Strong multi-person scene composition — more accurate than DALL-E for scenes with multiple people
- Precise prompt adherence — the MoE routing specializes expert networks per prompt type
- Native multimodal input — takes text and image together in one pass

---

### Grok Imagine Image (`grok-imagine-image`) — NOT available on Higgsfield

> **⚠ Platform notice:** Grok Imagine Image is available via the xAI API directly but is NOT currently available as an image model in the Higgsfield platform UI. The documentation below covers the xAI API capabilities for reference. For image generation on Higgsfield, use Soul 2.0, Nano Banana Pro, Seedream, or other listed image models.
**Type:** Image generation + image editing · **Resolution:** 1k / 2k · **Output:** URL or base64
**Best for:** Photorealistic images · precise text/logo rendering · multi-person scenes · iterative image editing chains · style transfer · batch generation for A/B testing

#### Text-to-Image
Single prompt, returns a URL. URLs are **temporary** — download immediately.

```
Model:  grok-imagine-image
Prompt: "A collage of London landmarks in a stenciled street-art style"
```

Supported aspect ratios (set via `aspect_ratio` parameter):

| Ratio | Use case |
|---|---|
| `1:1` | Social media, thumbnails |
| `16:9` / `9:16` | Widescreen, mobile, stories |
| `4:3` / `3:4` | Presentations, portraits |
| `3:2` / `2:3` | Photography |
| `2:1` / `1:2` | Banners, headers |
| `19.5:9` / `9:19.5` | Modern smartphone displays |
| `20:9` / `9:20` | Ultra-wide displays |
| `auto` | Model selects best ratio for the prompt |

Resolution options: `1k` (default) or `2k`. Batch generation: up to 10 images per request via `n` parameter.

#### Image Editing (Single Image)
Provide a source image + prompt describing the change. Output aspect ratio follows the input image's ratio by default.

```
Input:  source image (URL or base64 data URI)
Prompt: "Change the landmarks to be New York City landmarks"
Endpoint: POST /v1/images/edits
```

⚠️ **Important SDK note:** OpenAI SDK's `images.edit()` uses `multipart/form-data` which is **not supported** by xAI. Use the xAI SDK, Vercel AI SDK, or direct HTTP with `application/json` instead.

#### Editing with Multiple Images (up to 3)
Reference elements across multiple source images — pull a subject from one, drop them into another. The model interprets the ordered images and prompt to compose the output.

```
Prompt: "Add the cat from the first image to the second one."
Images: [image-edit-1.jpeg, image-edit-2.jpeg]  ← order matters
Aspect ratio: follows first input image (or override with aspect_ratio param)
```

Practical patterns:
- Character from Image 1 + Background from Image 2 → composite scene
- Product from Image 1 + Lifestyle context from Image 2 → product placement
- Three reference images → `"Combine the outfit from image 1, the setting from image 2, and the lighting from image 3"`

#### Multi-Turn Iterative Editing
Chain edits by using each output URL as the next input. Build up a scene progressively rather than trying to specify everything at once.

```
Turn 1: "A modern living room with large windows overlooking the city"
Turn 2: [previous output] + "Replace the furniture with mid-century modern pieces"
Turn 3: [previous output] + "Change the lighting to evening with warm lamps"
```

This is the recommended workflow for complex compositions — iterate rather than over-specify in one prompt.

#### Style Transfer
Describe any target aesthetic in the prompt alongside a source image:

```
"Render this image as an oil painting in the style of impressionism"
"Render this image as a pencil sketch with detailed shading"
"Render this image as pop art with bold colors and halftone dots"
"Render this image as an anime illustration"
"Render this image as a watercolor painting with soft edges"
```

Supported style range: photorealistic → anime → oil painting → pencil sketch → watercolor → pop art → and beyond.

#### What Aurora excels at vs other image models:

| Strength | Notes |
|---|---|
| Text and logos in-image | One of Aurora's top differentiators — most models fail here |
| Multi-person scenes | More accurate composition than DALL-E for groups |
| Precise prompt adherence | MoE architecture routes to specialized experts per task type |
| Photorealism | Detailed textures, convincing lighting, sharp compositions |
| Iterative editing chains | Multi-turn refinement is a first-class workflow |
| Batch variation generation | Up to 10 per request for rapid A/B testing |

**Content moderation:** `response.respect_moderation` flag — check before using the output URL. Images subject to content policy review.

```
Best use cases:
- Product photography and hero shots without a photo shoot
- Marketing creatives requiring precise text/logo rendering
- Iterative concept development via multi-turn editing
- Style transfer across a set of images
- Multi-person group compositions
→ grok-imagine-image
```

---

### Grok Imagine Video (`grok-imagine-video`)
**Duration:** 1–15s (generation) · **Resolution:** 720p · **Audio:** ✅ Native · **Aspect:** 16:9 / 4:3 / 1:1 / 9:16 / 3:4 / 3:2 / 2:3
**Best for:** Short-form video from text or image · video editing/restyling · adding/removing elements in existing footage · motion-based social content
**Architecture:** Same Aurora engine as the image model — generation is asynchronous (returns `request_id`, poll for result)

#### Generation Modes

**Text-to-video:**
```
Model:    grok-imagine-video
Prompt:   "Timelapse of a flower blooming in a sunlit garden"
Duration: 1–15s (integer)
Aspect:   16:9 (default), 4:3, 1:1, 9:16, 3:4, 3:2, 2:3
Resolution: 720p
```

**Image-to-video:**
Provide a source image URL — model animates it with your prompt describing the desired motion.
```
image_url: <publicly accessible image URL>
Prompt:    "Generate a video based on the provided image"
```

**Video editing:**
Provide an existing video URL + prompt describing what to change. High-fidelity edits that modify only what you specify, preserving the rest of the scene intact.
```
video_url: <publicly accessible video URL>
Prompt:    "Give the woman a silver necklace"
```
⚠️ **Video editing constraints:**
- Input video URL must be a **direct, publicly accessible link**
- Output resolution capped at 720p (1080p input gets downsized)
- User-defined duration is **not supported for editing** — output matches input video duration

#### Async Workflow
Video generation is asynchronous. Submit the request, receive a `request_id`, poll until `status: "done"`:

```
Step 1: POST /v1/videos/generations → {"request_id": "d97415a1-..."}
Step 2: GET  /v1/videos/{request_id} → poll until status == "done"
Step 3: Download video from response.video.url (temporary URL — save immediately)
```

SDK convenience: `client.video.generate()` handles polling automatically with configurable `timeout` and `interval` parameters. For manual control, use `client.video.start()` then `client.video.get(request_id)`.

#### Video Imagine 1.0 (Feb 2026) — Current Version
- Duration extended to 10s (was 8s previously)
- Resolution: 720p
- Significantly improved audio — dialogue, ambience, and SFX align more naturally with visuals
- xAI describes: "best-in-class instruction following for video generation"
- Video editing: restyling, adding/removing objects, controlling motion

#### Audio in Video
Native audio generation — synchronized dialogue, ambient sound, SFX, background music. Include audio intent directly in the prompt:
```
"...a crowd cheering in the background as confetti falls"
"...the character says, 'I can't believe it actually worked'"
"...wind howling, glass breaking, then silence"
```

#### Platform Limits
```
Duration:         1–15s (generation only; editing preserves source duration)
Resolution:       720p (cap for both generation and editing)
Aspect ratios:    16:9 / 4:3 / 1:1 / 9:16 / 3:4 / 3:2 / 2:3
Video editing:    Source video must be publicly accessible URL
URL expiration:   Output URLs are temporary — download promptly
```

```
Best use cases:
- Social clips and short-form content with native audio
- Animating a still image into a 10s video
- Video editing: add/remove elements, restyle footage
- Rapid iteration: generate multiple video variants concurrently
→ grok-imagine-video
```

---

#### Grok Imagine — Quick Decision

| Need | Model |
|---|---|
| Image from text | `grok-imagine-image` |
| Image editing (single or multi-image composite) | `grok-imagine-image` |
| Iterative multi-turn image refinement | `grok-imagine-image` |
| Style transfer on an existing image | `grok-imagine-image` |
| Precise text/logo in image | `grok-imagine-image` (Aurora strength) |
| 10s video with native audio from text | `grok-imagine-video` |
| Animate a still image | `grok-imagine-video` |
| Edit existing video footage | `grok-imagine-video` |

---

### Minimax Hailuo 02
**Best for:** Fluid motion · dynamic action · sports · dance
**Strengths:** Exceptional motion smoothness, great for physical performance
**Weaknesses:** Less strong on subtle facial acting
**Use when:** The motion itself is the primary visual element

---

## Image Models

### Soul 2.0
**Best for:** Fashion · portrait · high-aesthetic editorial · cultural style
**Strengths:** Built-in cultural fluency, fashion-forward, beautiful skin rendering
**Use when:** You need a stunning human portrait with style and presence
**Prompt note:** Describe clothing, lighting, and mood in detail — Soul responds to aesthetics

---

### Nano Banana Pro
**Best for:** Maximum sharpness · 4K detail · product photography · any subject requiring ultra clarity
**Strengths:** Best image quality on the platform, exceptional detail, Thinking mode reasoning, up to 14 reference images
**Use when:** Image quality is the top priority and speed is secondary
**Prompt note:** Works for any subject — not limited to portraits

---

### Seedream 4.5
**Best for:** General-purpose image generation · concept art · diverse styles
**Strengths:** Versatile, handles many styles well
**Use when:** You need a solid image and aren't locked into a specific aesthetic

---

### Flux Kontext
**Best for:** Image editing · inpainting · modifying existing images
**Strengths:** Best for making targeted edits to an existing image
**Use when:** The user wants to change or edit part of an image, not generate from scratch

---

## Quick Decision Table

| User need | Model |
|-----------|-------|
| Best cinematic video, long sequence, with audio | Kling 3.0 |
| Clone a character from reference video footage | Kling 3.0 Omni |
| Per-shot storyboard control + reference video | Kling 3.0 Omni |
| Transfer motion/choreography from reference video | Kling 3.0 Motion Control |
| Best human character, shorter clip, no audio needed | Kling 2.6 |
| Fast iteration on Kling quality | Kling 2.5 Turbo |
| Long camera-motion sequence (up to 30s) | Kling Motion Control |
| Complex multi-reference generation (up to 7 refs) | Kling O1 Video |
| Precise start-frame to end-frame motion | Kling O1 Video |
| **Edit existing footage** (relight, restyle, swap, remove) | **Kling O1 Video Edit** |
| Epic scale / action blockbuster | Sora 2 |
| Artistic / stylized / fantasy | Wan 2.5/2.6 |
| Fast iteration / social content (no audio needed) | Seedance Pro |
| Native audio + dialogue / lip-sync in video | Seedance 1.5 Pro |
| 12-asset multimodal / reference video → new scene | Seedance 2.0 (R2V) |
| Edit/replace elements in existing video | Seedance 2.0 (V2V) |
| Complex fight / synchronized motion at 2K | Seedance 2.0 |
| Nature / environment / documentary (stable) | Veo 3 |
| Subject/character consistency across scene (ref images) | Veo 3.1 |
| Define exact start + end frame | Veo 3.1 |
| Extend existing Veo video (up to 148s) | Veo 3.1 |
| Fast Veo iteration / volume generation | Veo 3.1 Fast |
| Fluid physical motion / dance/sports | Minimax Hailuo |
| Photorealistic image with precise text/logo rendering | GPT Image 1.5 |
| Multi-image composite (up to 3 source images) | Multi Reference |
| Iterative multi-turn image refinement | Flux Kontext |
| Style transfer on existing image | Flux Kontext |
| 10s video with native audio (text or image-to-video) | Grok Imagine Video |
| Edit/restyle existing video footage | Grok Imagine Video |
| Best portrait / fashion image | Soul 2.0 |
| Sharpest 4K image | Nano Banana Pro |
| Edit / modify an existing image | Flux Kontext |
| Reference-consistent editing / 4K assets | Seedream 4.5 |
| Complex layout / multi-panel / real-time data image | Seedream 5.0 Lite |
