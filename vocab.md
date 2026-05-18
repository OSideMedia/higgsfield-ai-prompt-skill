# Higgsfield Vocabulary Reference

## Camera Movement Terminology

### Linear Movements
- **Dolly In / Out** — smooth track toward or away from subject
- **Dolly Left / Right** — smooth lateral track
- **Dolly Zoom In / Out** — simultaneous dolly + counter-zoom (Vertigo/Hitchcock effect)
- **Super Dolly In / Out** — exaggerated fast version of dolly
- **Truck** — another term for lateral dolly movement

### Vertical Movements
- **Crane Up / Down** — vertical rise or descent
- **Crane Over The Head** — directly overhead, top-down
- **Levitation** — smooth dreamlike float upward
- **Tilt Up / Down** — camera rotates on horizontal axis (not physical movement)

### Orbit / Arc
- **360 Orbit** — complete circle around subject
- **Arc** — semi-circular sweep
- **Lazy Susan** — slow turntable rotation
- **Robo Arm** — precision mechanical arc path

### Zoom
- **Crash Zoom In / Out** — rapid sudden zoom
- **Rack Focus** — refocus between near and far subjects

### Follow / Immersive
- **Action Run** — low follow behind running subject
- **FPV Drone** — fast agile aerial weaving
- **Handheld** — organic shaky realistic movement
- **Head Tracking** — locked to character's head
- **Snorricam** — mounted on actor, background sways

### Cinematic Techniques
- **Bullet Time** — slow-motion sweep around frozen subject
- **Dutch Angle** — tilted diagonal composition
- **Fisheye** — wide distortion lens
- **Whip Pan** — fast blur pan
- **Overhead** — direct top-down
- **Flying** — free-floating aerial glide

### Camera Angles
- **Low Angle** — camera looks up at subject (power, dominance)
- **High Angle** — camera looks down at subject (vulnerability, smallness)
- **Eye Level** — neutral, conversational
- **Bird's-Eye View** — directly overhead
- **Worm's-Eye View** — extreme low, looking straight up
- **Ground Level** — camera on the ground surface
- **Canted Angle / Dutch Tilt** — tilted horizon for unease/tension
- **Static Oblique** — angled perspective, off-axis
- **Over-the-Shoulder (OTS)** — conversation framing, shot-reverse-shot
- **POV / First Person** — camera IS the character's eyes

### Time-Based
- **Hyperlapse** — moving camera + time-lapse
- **Timelapse Human / Landscape** — fixed camera, fast-forward time
- **Low Shutter** — motion blur from slow shutter speed

### Cut & Continuity Vocabulary
- **Double contrast** — every cut changes BOTH shot size AND camera character (handheld / static / stabilized tracking / crane / aerial). Never repeat the same mode across a cut.
- **Camera character** — the mode of motion itself: Handheld | Static/locked-off | Stabilized tracking | Crane/vertical | Aerial/drone
- **Re-anchoring** — after any cut returning to established space, re-state who is where and which direction they face. If a character moved left-to-right before the cut, same direction after.
- **180° rule** — keep the camera on one side of the imaginary line between subjects to preserve screen direction; crossing it flips left/right and disorients the viewer
- **Exit-frame = implicit cut** — once a character leaves frame, they are gone for the remainder of that shot. Never choreograph exit + re-entry in the same continuous shot.
- **Causally-motivated insert** — sub-second (0.3–0.5s) static detail the viewer understands WHY they see. Always name the subject ("HIS hand gripping metal"), never generic ("a hand").
- **Match cut** — cut between two shots linked by shape, motion, or composition
- **Smash cut** — abrupt, jarring cut with no transitional softening
- **Hard cut / direct cut** — standard straight cut, no effect
- **L-cut / J-cut** — audio from next shot leads picture (L) or vice versa (J). The L-cut **audio bridge** is the production-team's working name: hold the audio of the outgoing shot across the cut so the incoming visual lands inside an already-established soundscape.
- **Whip-pan transition** — blur pan that bridges two shots as a single motion
- **Camera-relative-to-previous-shot continuity** — when planning the next shot, name the camera position **relative to the previous shot's camera** (`camera now behind him, facing the same direction he was facing`) rather than absolutely. Keeps the cut from disorienting the viewer.

### Editing Syntax

Notation conventions for time-based and editorial structure inside prompts.

- **`[0-Ns]` bracket notation** — time-range prefix for shot phases inside a single continuous shot. Example: `[0-3s] subject enters frame, [3-7s] camera pushes in`. Used for per-second beats inside single-shot continuous motion (see `skills/higgsfield-seedance/SKILL.md` § Single-vs-multi-shot decision).
- **`Establishing → phrase → reaction` arrow notation** — editorial-flow notation for multi-cut dialogue or beat sequences. Reads as "establishing shot, then phrase/dialogue, then reaction shot." Compact prompt-side shorthand for a three-beat cut structure.

### Motion Hierarchy

The **4-layer motion hierarchy** separates simultaneous motions a shot can carry so the prompt names each layer explicitly:

1. **Subject motion** — what the character/object does (walks, turns, lifts hand)
2. **Internal motion** — micro-motion within the subject (breath, hair drift, fabric, eye motion, micro-expression)
3. **Camera motion** — what the camera does (pan, dolly, push-in, hold)
4. **Environmental motion** — what the world does (rain, leaves, traffic in background, light shifting)

Specifying each layer separately prevents the multi-motion overload failure mode (see `skills/higgsfield-seedance/FAILURE-MODES.md` § Multi-motion camera overload).

---

## Shot Size Vocabulary

| Term | Frame content |
|------|--------------|
| Extreme Long Shot (ELS) | Vast landscape, subject tiny or absent |
| Extreme Wide (EWS) | Subject tiny in environment |
| Wide Shot / Long Shot (WS/LS) | Full body + surroundings |
| Medium Long Shot / Cowboy (MLS) | Subject from mid-thigh up |
| Medium Wide (MWS) | Subject from knees up |
| Medium (MS) | Waist up |
| Medium Close-Up (MCU) | Chest up |
| Close-Up (CU) | Face |
| Extreme Close-Up (ECU) | Detail — eyes, hands, object |
| Insert Shot | Detail of an object or action |
| Over-the-Shoulder (OTS) | Looking over a character's shoulder |
| POV | First-person character perspective |
| Two-Shot | Two characters in frame |
| Cowboy Shot | Mid-thigh up, posture and readiness |

---

## Visual Style Vocabulary

### Named Platform Styles
- **Cinematic** — polished, high-contrast, professional
- **VHS** — retro grain, color bleed, analog warmth
- **Super 8MM** — warm film grain, soft vignette, nostalgic
- **Anamorphic** — ultra-wide, lens flares, epic scale
- **Abstract** — surreal, non-representational, artistic

### Aspect Ratio: output spec vs. style register

| Concern | What it is | Where it belongs in a prompt | Bound by |
|---|---|---|---|
| Output ratio | Hard platform spec — what the model actually emits | Header (e.g. "Aspect ratio: 16:9") | Per-model enum (Kling 3.0: 16:9 / 9:16 / 1:1; check `higgsfield model get <model>`) |
| Anamorphic / 2.35:1 / 2.39:1 / Scope / Cinemascope | Cinematography register — anamorphic flares, letterboxed framing aesthetic | Look line, as a style request ("anamorphic-style flares, letterboxed composition") | Stylistic — the model renders the look within the chosen output ratio |

Conflating these produces incoherent prompts. "16:9 anamorphic" requests two contradictory things at once. The model will either ignore one or produce uneven results. Separate them.

### Color Grade Language

| Mood | Description |
|------|-------------|
| Blockbuster | Teal shadows, orange highlights, high contrast |
| Cold thriller | Desaturated blue-grey, crushed blacks |
| Warm nostalgia | Golden amber, lifted shadows, soft grain |
| Cyberpunk | Neon magenta + cyan, deep shadows, HDR |
| Horror | Sickly yellow-green, low contrast, murky |
| Romance | Soft pink-gold, lifted shadows, dreamy |
| Documentary | Natural neutral, no grade |
| Epic fantasy | Deep jewel tones, volumetric light |
| Noir | High contrast black and white |
| Post-apocalyptic | Desaturated orange-brown, dust haze |

### Color rules

- **60/30/10 color rule** — production-direction color-palette discipline. A frame's color reads cleanest when 60% is one dominant color, 30% is a secondary, and 10% is an accent. Prompts that name a single dominant tone + supporting palette land more cohesively than prompts that list five competing colors.

### Film Stock Emulation
- Kodak Portra 400 — warm, rich skin tones, slight grain
- Fuji Velvia — vivid saturated colors, fine grain
- Kodak Vision3 500T — cinematic, natural, slight warmth
- Ilford HP5 — classic black and white, visible grain
- Kodak Ektachrome — bright, contrasty, clean slide film

---

## Lighting Vocabulary

| Type | Description |
|------|-------------|
| Golden hour / Magic hour | Warm directional, sun near horizon |
| Blue hour | Cool, soft, just after sunset |
| Overcast / Softbox | Diffused, soft, no shadows |
| Neon | Colored artificial from signs/screens |
| Volumetric | Light rays visible (fog/dust/smoke) |
| Practical only | Light from sources visible in frame |
| Side-lit | Single strong source from one side |
| Backlit / Rimlit | Light source behind subject |
| Motivated | Light that matches a logical source in scene |
| Hard light | Strong single source, defined shadows |
| Soft light | Diffused, wrapped, minimal shadows |
| Rembrandt | Triangle of light on shadowed cheek |
| Butterfly / Paramount | Overhead, shadow under nose (glamour) |
| Split lighting | Half face lit, half in shadow |
| Chiaroscuro | Extreme light/dark contrast |
| High-key | Bright, minimal shadows (comedy, commercial) |
| Low-key | Deep shadows, moody (noir, horror) |
| Harsh midday sun | Hard overhead, strong defined shadows |

### Scene-physics lighting

Lighting described as a physical event in the scene rather than as a stylistic adjective. State the source position, the surfaces it reflects off, and the resulting shadow geometry — the model uses each named piece to reconstruct illumination consistently across shots.

- **Source position** — `key light from screen-left, ~30° above eye line`
- **Reflection / bounce** — `warm bounce off the wooden floor lifting under-jaw shadow`
- **Shadow geometry** — `hard shadow on screen-right wall reading the silhouette of the desk lamp`
- **Ambient density** — `dense ambient haze in the foreground softening contrast 6m+ out from camera`

The scene-physics framing replaces stylistic adjectives (`moody`, `dramatic`, `cinematic`) with named physical mechanisms that compose. The model can render the named mechanisms; it can only approximate the adjectives.

---

## Subject & Character Vocabulary

### Body Language / Posture
- Upright, tense, coiled, relaxed, hunched, squared-off
- Arms open / crossed / raised / at sides
- Weight forward / back / centered
- Eyes wide / narrowed / cast down / direct to camera

### Movement Quality
- Fluid, jerky, precise, hesitant, confident, stumbling
- Slow-motion, overcranked (high fps = slow playback)
- Undercranked (low fps = fast playback)
- Natural, stilted, mechanical, animal-like

### Emotion Cues (for camera and performance)
- Realization: slow Dolly In, eyes widening
- Fear: Dutch Angle, Handheld
- Power: Crane Up, 360 Orbit, wide stance
- Vulnerability: Overhead, Dolly Out, small in frame
- Intimacy: Dolly In, shallow depth of field
- Chaos: FPV Drone, Handheld, fast cuts

### Emotion as Visible Behavior — Channels

Eight named channels through which emotion becomes visible to the
camera. Use these to decompose abstract emotion language ("she is
afraid," "he is angry") into observable physical behavior the model
can stage.

- **Breath** — rate, depth, hold, exhale character
- **Eye behavior** — fixation, blink rate, gaze direction
- **Jaw tension** — clenched, slack, working, set
- **Loss of focus** — gaze drifting, attention slipping, response delay
- **Scanning pattern** — eye/head sweep direction, tracked target
- **Delayed recovery** — lag between stimulus and adjustment back to baseline
- **Control attempt** — visible suppression or regulation effort
- **Emotional residue after the peak** — what reads on the body after the dominant beat

The Micro-Expression Vocabulary section below catalogs named endpoint
expressions (Suppressed Smile, Cold Calculation, etc.) — those are
combinations of these channels. The channels above are the substrate;
the named expressions are what the substrate produces.

---

## Environment & Atmosphere Vocabulary

### Time of Day
- Dawn — first light, mist, cool blue to warm orange
- Golden hour — 1hr after sunrise / before sunset
- Midday — harsh overhead light, deep shadows
- Overcast day — flat, diffused, neutral
- Blue hour — after sunset, cool soft glow
- Night — dark, pools of light, shadow-heavy

### Weather / Atmosphere
- Rain: wet surfaces, reflections, steam rising
- Fog/mist: soft depth, reduced contrast, mystery
- Snow: muted colors, diffused light, silence implied
- Heat haze: shimmering air, warm distortion
- Wind: moving elements, hair/fabric/trees
- Dust/smoke: volumetric light opportunities

### Environment Types
- Urban: concrete, glass, neon, crowds, traffic
- Industrial: metal, rust, machinery, steam pipes
- Natural: organic textures, varied light, scale
- Interior: controlled light, props, intimacy
- Wilderness: raw, unpredictable, vast
- Fantasy: designed, non-real, heightened

### World Through Recurrence

Eight named substrate axes through which a world becomes legible
to the audience across multiple shots. Use these to identify what
should repeat consistently across scenes — a world emerges from
what recurs, not from what gets explained.

- **Recurring spaces** — locations that return, space-types echoed across acts
- **Light behavior** — how light enters, falls, decays in repeated patterns
- **Silence** — the texture and timing of quiet, what gets withheld between beats
- **Materials** — surface vocabulary, substance choices, tactile signature
- **Architecture** — corridor logic, threshold use, the way built form constrains motion
- **Props** — physical objects that reappear with consistent meaning
- **Emotional conditions** — recurring affective states, dread density, what lingers after a beat resolves
- **Camera distance / rhythm** — proximity choices, when to step back, pacing patterns

---

## Audio / Sound Vocabulary (for Kling 3.0 and audio-capable models)

| Sound type | Description for prompt |
|------------|----------------------|
| Ambient | "soft city hum", "distant traffic", "forest insects"  |
| Weather | "rain on cobblestones", "wind through trees", "thunder rumble" |
| Movement | "footsteps on gravel", "fabric movement", "glass crunch" |
| Mechanical | "engine revving", "metal scrape", "hydraulic hiss" |
| Human | "breathing", "heartbeat rising", "crowd murmur" |
| Music cue | "tense strings build", "low bass drone", "electronic pulse" |

---

## Platform Feature Vocabulary

| Term | Definition |
|------|-----------|
| Soul ID | Upload 20+ photos of a real person to train identity consistency across generations |
| Soul Cast | Generate AI actors from parameters (no photos needed) — Cinema Studio 2.5 feature, powered by Nano Banana 2 |
| Soul HEX | Extract color palettes from reference photos for brand-consistent, color-matched visuals |
| Soul Cinema Preview | Higgsfield proprietary cinematic-grade image model, prompt-driven only, excels at close-ups |
| Elements 3.0 | Reference system using `@element_name` syntax for cross-shot subject consistency (Kling 3.0) |
| Voice Binding | Lock specific voice profiles to specific characters across shots (Kling 3.0) |
| Performance Cloning | Act out a scene on camera → AI re-renders preserving likeness and voice (Kling 3.0 Omni) |
| Motion Control | Transfer motion from reference video to new character/scene (Kling 3.0 Motion Control) |
| Reference Anchor | Cinema Studio system that locks character geometry across all shots |
| Hero Frame | Key image generated before video to define visual tone, lighting, and composition |

### Image Reference Notations — `@Image1` vs `<<<image_1>>>`

Both notations refer to the same underlying @-reference mechanic; the bracket style
is contextual to which surface is being addressed.

- **`@Image1`** — the platform-side reference syntax used in actual prompts to the
  Higgsfield generation engine. Capital `I`, no underscore, single `@`. Used across
  `templates/` and most sub-skill prompt examples (e.g., `templates/02-product-ugc-showcase.md`,
  `MODELS-DEEP-REFERENCE.md` § The Rule of 12). Pattern in prompts:
  `@Image1 as the character`, `@Image2 as the background`.
- **`<<<image_1>>>`** — the Seedance 2 Skill's internal explicit-reference notation,
  used in user requests to the `docs/Seedance 2 Skill.md` bilingual EN+ZH prompt
  director. Lowercase `image`, underscore, triple angle bracket. Recognized by the
  Seedance Skill when typed in a user request, then mapped to the appropriate scene
  element (per `docs/Seedance 2 Skill.md:178` § Image reference system).

**Per-slot role convention** — production practice locks a stable role assignment per `@Image` slot, kept identical across every prompt in a shot list: `@Image1 = character identity`, `@Image2 = costume`, `@Image3 = environment + lighting`, `@Image4 = composition`, `@Video1 = motion`, `@Video2 = camera movement`, `@Audio1 = rhythm + atmosphere`. The convention is team-side discipline, not model-enforced; the payoff is reference-stability across long shot lists (see `skills/higgsfield-seedance/SKILL.md` § Per-Image Role Convention).

---

## Composition Vocabulary

Vocabulary for what's IN the frame and where it sits — distinct from camera-side language (which describes how the camera moves) and lighting (which describes illumination).

- **Negative space** — the deliberately-empty area of the frame that isolates or weighs the subject. Production-direction language: `negative space sits center-left of frame, narrowing as the character advances`. Naming negative space as a compositional element prevents the model from filling it with incidental detail.
- **Crossing rule** — film-grammar clause for whether characters may cross positions on-screen within a shot or across a cut. Distinct from the camera-side 180° rule (which is about the imaginary line between subjects): the crossing rule names what subjects may do, the 180° rule names what the camera may do. Example: `Character A stays on the left, Character B stays on the right, neither crosses the central vertical axis`.
- **Coordinate notation** — paired qualitative + percentage spatial anchors for in-frame placement. `Character A stands in the right third, x-position 70%, y-position 50%, frame occupancy 25%`. The qualitative term gives the film-language hook; the percentage gives the precision target. See `skills/higgsfield-seedance/SKILL.md` § Frame Coordinate System for the full coordinate system + caveats.

---

## Production Vocabulary

Terminology imported from traditional film production into AI-cinema practice — names for disciplines that recur in production workflow.

- **Script supervising** — the traditional-film-production discipline of tracking every character's state (injuries, clothing, props, hair) across shots so continuity holds across cuts. Imported into AI-cinema via per-state character anchor sheets: a character with five stages (e.g., initial / fight-injuries / partially-transformed / almost-fully / completely-transformed) gets five distinct Soul ID sheets, one per stage. See `skills/higgsfield-soul/SKILL.md` § Multi-Form State Tracking.
- **State lock** — the per-shot directive that names the character's current emotional or physical state (calm, exhausted, injured, soaked, in motion) inside the Character Anchor Block. Distinct from `pose` (physical configuration) and `facial expression` (emotional register): state lock names the persistent condition that should hold across the shot's duration. See `skills/higgsfield-soul/SKILL.md` § Character Anchor Block.

---

## Micro-Expression Vocabulary

The Emotion as Visible Behavior — Channels section above catalogs the
eight substrate channels these endpoint expressions decompose into.

Performance directions for Soul Cast actors and character prompting:

| Expression | Description |
|-----------|-------------|
| Deadpan Neutral | Flat affect, no visible emotion |
| Fierce Focus | Intense locked gaze, total attention |
| Suppressed Smile | Fighting back a grin, corner of mouth twitching |
| Quiet Devastation | Eyes glassy, jaw tight, holding it together |
| Cold Calculation | Eyes scanning, no emotional leakage, clinical |
| Bitter Amusement | One-sided smirk, eyes not smiling |
| Frozen Shock | Mouth slightly open, eyes fixed, body still |
| Simmering Rage | Clenched jaw, flared nostrils, steady stare |
| Vulnerable Openness | Soft eyes, slightly parted lips, unguarded |
