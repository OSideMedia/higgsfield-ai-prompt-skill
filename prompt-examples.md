# Higgsfield Prompt Examples

High-quality examples organized by genre. Use these as references for tone,
structure, and specificity. All are original, no IP or real names.

---

## Cinematic Still Images

New in v1.3.9 — examples using the exact image prompt formula:
`[Shot size] + [Angle] + [Movement keyword] of [character/subject]. [Pose]. [Environment]. [Lighting]. [Style].`

### Sci-Fi Character Tension — Nano Banana Pro
```
Model: Nano Banana Pro
Aspect: 16:9 | Style: Cinematic

Medium Close-Up (MCU) Low Angle Dolly Zoom of a weathered space pilot in a cracked visor.
Staring intensely off-camera, jaw clenched.
The sparking, smoke-filled cockpit of a crashing starfighter.
Flashing red emergency lights, hard side-key illumination.
Photorealistic sci-fi cinematic, ultra-sharp detail.
```

### Epic Fantasy Scale — Seedream 4.5
```
Model: Seedream 4.5
Aspect: 16:9 | Style: Concept Art

Extreme Wide Shot (EWS) Overhead / Bird's Eye Crane up of a lone knight in blackened armor.
Kneeling in the snow with a glowing broadsword planted in the ground.
A vast frozen lake surrounded by jagged obsidian mountains.
Cold blue hour, soft diffused moonlight piercing through heavy clouds.
Dark fantasy concept art, high contrast, 4K resolution.
```

### Psychological Thriller Detail — Nano Banana Pro
```
Model: Nano Banana Pro
Aspect: 3:4 | Style: 1970s Thriller

Extreme Close-Up (ECU) Dutch Angle Rack Focus of a trembling hand clutching an ornate silver key.
Knuckles white from gripping too hard, skin textured and cold.
A dimly lit vintage hallway with peeling floral wallpaper in the blurred background.
Sickly yellow-green practical light, deep crushed shadows.
1970s psychological thriller, heavy film grain, muted color palette.
```

---

## Before → After — Prompt Improvement Examples

These show common weak prompts and how MCSLA transforms them into high-performing ones.

### Example 1: Vague → Specific (Action)

**Before (weak):**
```
A cool action scene in a city at night with a woman running and cameras moving dramatically.
```

**Problems:** No camera preset named, "cool" is unmeasurable, "cameras moving dramatically" is generic, no style or color grade.

**After (strong):**
```
Model: Kling 3.0
Aspect: 16:9 | Duration: 10s | Style: Cinematic

A woman in a tactical jacket sprints through a rain-soaked night market,
weaving between stalls. Steam rises from food carts, neon signs fracture in puddles.
Camera: Action Run — low behind her, matching pace.
She slides under a closing metal gate without breaking stride.
Style: Cinematic. Cold blue shadows, warm amber market light, high contrast. 16:9.
```

**What changed:** Named camera preset (Action Run), specific environment details, active verbs (sprints, slides, weaving), explicit color grade, concrete style.

---

### Example 2: Over-Described I2V → Motion-First (Image-to-Video)

**Before (weak):**
```
A beautiful woman with long dark hair and brown eyes wearing a red silk dress
is standing on a balcony with a city behind her at sunset. The sky is orange
and pink with some clouds. There are tall buildings in the background. She looks elegant.
```

**Problems:** Re-describes everything already visible in the input image. No motion cues. No camera movement. "Beautiful" and "elegant" are style slop the model can't act on.

**After (strong):**
```
Starting from the provided image as the first frame.
Her hair lifts gently in the evening breeze. She turns her head slowly to the right,
eyes narrowing slightly as if recognizing someone below.
Camera: slow Dolly In toward her profile.
Wind catches the dress fabric. City lights begin flickering on in the distance.
Style: Cinematic, warm golden hour, shallow depth of field.
```

**What changed:** Only describes what *changes* (hair, head turn, fabric, lights), adds camera movement, removes all static descriptions the model can already see.

---

### Example 3: Slop Words → Observable Controls (Drama)

**Before (weak):**
```
An epic cinematic masterpiece shot of a stunning detective in a breathtaking
noir setting. Ultra-realistic 8K quality. Award-winning cinematography.
```

**Problems:** Every word fails the "can a camera measure this?" test. No subject detail, no action, no camera, no actual style specification.

**After (strong):**
```
Model: Kling 3.0
Aspect: 16:9 | Duration: 8s | Style: Cinematic

A weathered detective stands at the edge of a rain-soaked harbour dock at night.
An old leather briefcase sits at his feet, open, papers scattered by the wind.
He stares at the horizon, collar turned up against the driving rain.
Harbour lights fracture on the black water below.
Camera: slow Dolly In from medium-wide to medium close-up.
Style: Cinematic. Crushed blacks, single sodium-vapour key light from the right,
cold blue fill, 2.35:1 anamorphic.
```

**What changed:** Replaced every unmeasurable word with observable detail. Specific lighting (sodium-vapour key, cold blue fill), concrete environment, physical action, named camera movement.

---

### Example 4: Camera Soup → Single Movement (Sci-Fi)

**Before (weak):**
```
Camera does a dramatic FPV drone shot while also orbiting the subject
and then crash zooming into their face with a dolly zoom effect.
The camera keeps moving the whole time.
```

**Problems:** Four contradictory camera movements in one prompt. Model can't execute all simultaneously — produces erratic, broken output.

**After (strong):**
```
Camera: FPV Drone — sweeping through the zero-gravity corridor ahead of the soldier,
debris drifting past on both sides.
```

**What changed:** One camera movement, clearly named. If four shots are needed, generate four separate clips and chain them.

---

### Example 5: No Audio Direction → Structured Sound (Dialogue)

**Before (weak):**
```
Two people talking at a café. It should sound natural.
```

**Problems:** No dialogue content, no ambient sound specification, no SFX, "natural" is unmeasurable.

**After (strong):**
```
Model: Kling 3.0
Aspect: 16:9 | Duration: 8s | Style: Cinematic

A woman and a man sit across from each other at a small café table by the window.
She leans forward: "I found something — you need to see this."
He sets down his cup slowly: "Not here."
Ambient: quiet café murmur, espresso machine hiss in background, rain on window.
Camera: Over-the-shoulder medium shots alternating. Static, locked-off.
Style: Cinematic. Warm interior, cold blue rain light through window, shallow DOF.
```

**What changed:** Dialogue in quotes for lip-sync, specific ambient sound cues, explicit camera framing, measurable lighting.

---

## Action

### Urban Chase — Night Market
```
Model: Kling 2.6
Aspect: 16:9 | Duration: 10s | Style: Cinematic

A woman in a tactical jacket sprints through a rain-soaked night market,
weaving between stalls and startled vendors. Steam rises from food carts.
Camera: Action Run — low behind her, matching pace.
A metal gate drops ahead. She slides under it without breaking stride.
Whip Pan to two men in dark coats pushing through the crowd behind her.
Camera: Bullet Time as she leaps from a loading dock onto a moving truck below.
Style: Cinematic. Cold blue shadows, amber market light, high contrast. 16:9.
```

### Rooftop Fight
```
Model: Sora 2
Aspect: 16:9 | Duration: 10s | Style: Anamorphic

Two silhouettes grapple on a rain-slicked rooftop at night, city spread below them.
Lightning illuminates the scene in strobe flashes.
Camera: FPV Drone circling just outside their reach, catching each exchange of blows.
One figure is thrown backward — slides to the edge, barely catches the ledge.
Camera: Dutch Angle as they hang there, rain hammering down.
Style: Anamorphic. Deep desaturated blue-grey. Lens flare on distant lightning. 2.35:1.
Apply Bullet Time preset at the moment of the throw.
```

### Underground Parking Pursuit — Seedance 2.0 (Reference-Based)

```
Model: Seedance 2.0 (Reference-Based mode)
Aspect: 16:9 | Duration: 8s | Style: Cinematic

[Reference image: hero character — woman, late 20s, charcoal track jacket,
short cropped hair — as the main character]

Style & Mood: cold sodium-vapor underground, deep shadows under concrete pillars,
faint exhaust haze, anamorphic flares on overhead fluorescents.

Dynamic Description: The Soul ID character sprints between two rows of parked
cars, glances back over her shoulder at footsteps gaining behind her, vaults
the hood of a sedan, lands and keeps running toward the ramp at frame right.
Camera tracks low and right, matching her pace, losing and regaining her
between pillars.

Static Description: Underground parking level, concrete pillars, sodium
overhead lighting, scattered parked cars. Wet patches on the floor catch
practical light.

Camera: Low tracking shot, parallel right, following at running pace.

Audio: foregrounded — her breath ragged and close to camera, sneakers
hitting wet concrete with each stride right under the mic, the *snap* of
impact when she lands the vault. Background drops back: a fluorescent
ballast somewhere overhead, footfalls behind her thinned by distance, no
music.
```

Reference-Based mode keeps the character's face and wardrobe locked from the
upload; the prompt does not re-describe them. Identity travels with the
reference; action and environment travel in the prompt.

---

## Drama

### Hospital Corridor
```
Model: Kling 2.6
Aspect: 16:9 | Duration: 8s | Style: Cinematic

A man in his 40s walks slowly down a hospital corridor. Fluorescent lights flicker above him.
He stops at a door. Hand on the handle. He doesn't open it.
Camera: slow Dolly In from behind, stopping just over his shoulder as he stands still.
His head drops slightly. A long exhale.
Style: Cinematic. Desaturated, cool blue-white light. 16:9.
```

### Reunion at the Airport
```
Model: Kling 2.6
Aspect: 16:9 | Duration: 8s | Style: Super 8MM

Arrivals hall. Crowds moving. A woman in her 30s scans faces, clutching a small sign.
Then — she sees. The sign drops. She moves forward through the crowd.
Camera: slow Arc around the moment they embrace, world blurring behind them.
Style: Super 8MM. Warm grain, soft vignette, lifted shadows. 16:9.
```

### Hospital Vigil II — Seedance 2.0 (Continuation)

```
Model: Seedance 2.0 (Continuation mode)
Aspect: 21:9 | Duration: 6s | Style: Naturalistic

Continuing from the prior clip — the husband framed at the bedside, head
bowed, his hand on hers, the heart monitor's rhythm filling the silence.

[Identity block verbatim: man in his late 40s, lined face, three-day stubble,
grey sweater frayed at the cuffs, wedding ring loose on his finger, exhausted
but composed.]

Style & Mood: Cold blue practical light from the corridor bleeding through
the half-open door, single warm lamp by the bed. Naturalistic palette,
muted, shallow depth of field on his face.

Dynamic Description: Following his bowed posture, he slowly lifts his head,
looks at her face, and his composure cracks — eyes filling but not yet
spilling, jaw tightening, breath held. Camera holds steady on his face,
unmoving, letting the change play out.

Static Description: Hospital room at night, single bed, monitor cables, the
warm bedside lamp the only source of warm light.

Camera: Locked-off medium close-up, no movement.

Audio: a single sustained low cello note enters under the held silence —
quiet at first, then swelling almost imperceptibly through the moment his
composure breaks, holding under the cracked breath without resolving.
Diegetic sound recedes beneath it: the heart monitor's tempo, a distant
intercom, the rustle of bedsheets — present but pulled low in the mix.
```

Continuation mode picks up at the final frame of the prior clip — the
last-frame anchor opens the prompt, the identity block re-pastes verbatim,
the new beat (the composure breaking) is the only new content. The five
Continuation rules in `skills/higgsfield-seedance/SKILL.md` § Continuation
Prompt Formula apply.

---

## Sci-Fi

### Zero Gravity Breach
```
Model: Sora 2
Aspect: 16:9 | Duration: 10s | Style: Cinematic

A battle-worn space station corridor, emergency lighting, debris floating in zero gravity.
A soldier in heavy tactical armor pulls herself along a handrail, rifle raised.
Ahead — a sealed blast door, sparking at the seams. She plants a charge and pushes back.
Camera: FPV Drone drifting just ahead of her through the corridor as the charge detonates.
Style: Cinematic, cold steel blue, high contrast. 2.35:1 anamorphic.
Apply Plasma Explosion preset at the detonation moment.
```

### Cyberpunk Street Level
```
Model: Kling 2.6
Aspect: 16:9 | Duration: 8s | Style: Cinematic

Ground-level view of a rain-soaked megacity street at night. Neon signs reflect in every puddle.
A figure in a long coat and AR visor walks toward camera, unhurried, through the crowd.
Holographic ads flicker and shift above the stalls on either side.
Camera: Dolly Out slowly as the figure keeps approaching — never quite reaching us.
Style: Cinematic. Deep shadows, neon magenta and cyan, shallow depth of field. 16:9.
```

### Derelict Station Approach — Seedance 2.0 (Reference-Based)

```
Model: Seedance 2.0 (Reference-Based mode)
Aspect: 21:9 | Duration: 10s | Style: Hard Sci-Fi

[Reference image: hero character — figure in a battered EVA suit, helmet
off and clipped to the hip, weathered face, close-cropped grey hair — as
the main character]

Style & Mood: cold blue ambient from a dying station, single warm-amber
emergency strobe, faint particulate haze in zero-g, hard sci-fi palette,
crushed blacks.

Dynamic Description: The Soul ID character drifts forward through a
darkened corridor in zero-g, one gloved hand trailing the bulkhead for
guidance, the other steadying a tethered toolkit. The emergency strobe
flickers across her face every 2 seconds. She pauses at a junction, head
turning slowly toward a flickering panel ahead.

Static Description: Derelict station corridor, exposed conduits along the
ceiling, frost on the bulkhead seams, debris drifting in the foreground,
warning labels half-readable on the walls.

Camera: slow dolly-in following her drift, matching her pace, holding her
in center frame.

Audio: designed, not captured. The suit's life-support fan as a treated
low drone with a 4Hz pulse under it. Hull groans constructed from layered
metal-stress samples, processed for a hollow zero-g signature. The
emergency strobe's relay click as a hard transient, foregrounded each
cycle. Helmet breath EQ'd to the close, internal-mic position. No music.
```

Reference-Based mode locks the EVA suit's wear and the character's face from
the upload. The prompt drives the new environment — derelict station, zero-g
corridor, emergency lighting — without re-describing identity.

---

## Horror

### Wrong Room
```
Model: Kling 2.6
Aspect: 4:3 | Duration: 8s | Style: VHS

A woman unlocks the door to her apartment. Steps inside. Everything looks normal.
She sets down her keys. Turns toward the kitchen.
Camera: slow Dolly In toward the hallway mirror at the end.
The mirror shows the room — but the couch is against the wrong wall. 
She hasn't moved. The reflection has.
Camera: Dutch Angle as she realizes.
Style: VHS. Desaturated greens, practical light only, slight scan lines. 4:3.
Apply Horror Face preset in the mirror reflection.
```

### The Sound Below
```
Model: Wan 2.5
Aspect: 16:9 | Duration: 8s | Style: Cinematic

A man stands at the top of a dark basement staircase, holding a flashlight.
The beam cuts down into nothing. A sound below — something shifting.
Camera: Tilt Down following his flashlight beam slowly down the stairs.
At the bottom — the beam hits a rocking chair. Moving on its own. No one in it.
Style: Cinematic low key. Crushed blacks, single practical flashlight beam, near-silence. 16:9.
```

---

## Romance

### Rooftop at Dusk
```
Model: Kling 2.6
Aspect: 16:9 | Duration: 8s | Style: Cinematic

Two people on a rooftop terrace at dusk, city glowing below them.
They've been talking for hours — coffee cups empty, leaning close.
A long pause. She looks at him.
Camera: Arc slowly around both of them, city blurring behind.
He reaches over and tucks a strand of hair behind her ear.
Style: Cinematic. Golden hour warm tones, shallow depth of field. 16:9.
```

### Letters on a Train
```
Model: Kling 2.6
Aspect: 16:9 | Duration: 8s | Style: Super 8MM

A young woman sits alone in a train compartment, reading a letter.
Rain runs down the window beside her. The passing countryside blurs.
She smiles — just slightly — at something on the page.
Camera: Focus Change from the rain on the window to her face.
Style: Super 8MM. Warm grain, soft afternoon light. 16:9.
```

---

## Product / Commercial

### Coffee Mug — Morning Ritual
```
Model: Kling 2.6 (video) / Nano Banana Pro (image)
Aspect: 16:9 | Duration: 5s | Style: Cinematic commercial

A matte black insulated mug, minimal design, no branding.
Placed on raw concrete countertop beside a morning window.
Camera: Robo Arm arcing slowly from base up around to the lid.
Hot coffee pours in — steam rises in macro close-up.
A hand wraps around the mug. Camera: Dolly In to hands + warmth detail.
Style: Cinematic commercial. Warm neutral tones, soft diffused natural light. 16:9.
Sound: quiet liquid pour, subtle ceramic texture.
```

### Sneaker Drop
```
Model: Nano Banana Pro (image) → Kling 2.6 (video)
Aspect: 1:1 | Style: Cinematic

A single sneaker — white with minimal branding — suspended mid-air against a black void.
Dust particles float around it, backlit by a single strong side-light.
Camera: 3D Rotation — full 360 reveal.
Style: Cinematic. Pure black background, sharp product detail, 4K. 1:1.
```

### Coffee Beans — Label Iteration — Seedance 2.0 (Edit Shot)

```
Model: Seedance 2.0 (Edit Shot mode)
Aspect: 1:1 | Duration: 6s | Style: Commercial

[Source clip: the existing "Coffee Mug — Morning Ritual" generation]

Change the coffee bag in the background from the kraft-paper version to a
matte-black version with a single copper foil logo. Keep the steam, the
ceramic mug, the wooden counter, the light direction, and the camera move
unchanged.

Preserve identity, composition, lighting, and camera behavior from the
original. Preserve the morning window light, the warm tones, and the
shallow depth of field.

Camera: unchanged from source — slow push-in toward the mug.

Audio: same as source — kitchen ambience as the primary content, layered:
the low refrigerator hum two rooms over, faint traffic through a closed
window, the air itself in a quiet morning kitchen. The kettle's distant
whistle and the ceramic-on-wood touch sit inside the ambience, not on top
of it. No music.
```

Edit Shot mode is the targeted-patch tool. The prompt names exactly what to
change (the bag swap) and explicitly preserves everything else. The Keep Rule
matters — without it, the generation drifts on every variable that isn't
locked.

---

## Nature / Documentary

### Storm Over the Pacific
```
Model: Veo 3
Aspect: 16:9 | Duration: 10s | Style: Cinematic natural

Open ocean at dusk. The horizon is dark with an approaching storm.
Waves are already running ahead of it — three-meter swells, grey-green water.
Camera: Timelapse Landscape as the storm front advances, sky darkening fast.
Lightning inside the clouds. Then the first rain hits the surface.
Style: Cinematic, natural grade, no artificial treatment. 16:9.
```

### Heron at Dawn
```
Model: Veo 3
Aspect: 16:9 | Duration: 8s | Style: Cinematic

A grey heron stands motionless in a shallow estuary at first light.
Mist on the water. Absolute stillness.
Camera: Dolly In extremely slow — barely perceptible movement toward the bird.
It extends its neck. Holds. Strikes — beak into the water, emerges with a small fish.
Style: Cinematic, natural light, cool blue-grey dawn. 16:9.
```

---

## Dance / Music

### Contemporary Solo
```
Model: Minimax Hailuo 2.3
Aspect: 16:9 | Duration: 10s | Style: Cinematic

A dancer in a white flowing dress performs alone in a vast black studio.
A single overhead spotlight. She moves through contemporary choreography —
slow arms, sudden explosive turns, floor work.
Camera: 360 Orbit tightening toward her as movement intensifies.
Overhead shot as she collapses to the floor in the final beat.
Style: Cinematic. Pure black and white contrast. 16:9.
Apply Glow Trace preset — her movement leaves a trail of white light.
```

### Hip-Hop Cypher
```
Model: Minimax Hailuo 2.3
Aspect: 9:16 | Duration: 8s | Style: Cinematic

Four dancers in a circle under a single streetlight at night.
One steps into the center — starts hitting sharp isolated movements.
Camera: Rap Flex — quick zooms snapping in and out on each hit.
Crowd around the circle is a blur of energy.
Style: Cinematic. High contrast, deep shadows, neon from nearby signage. 9:16.
Apply Live Concert preset for lighting energy.
```

---

## Transformation

> **Genre vs. Seedance prompt mode:** this section collects examples of the
> *Transformation genre* — clips where the visible content of the shot is a
> state change. Distinct from the *Transformation prompt mode* in
> `skills/higgsfield-seedance/SKILL.md`, which is a Seedance-specific
> construction pattern for that kind of clip. Examples here use various models;
> for a Seedance 2.0 worked example using the Transformation prompt mode, see
> the Awakening II / Seedance 2.0 entry below.

### Awakening
```
Model: Kling 2.6
Aspect: 16:9 | Duration: 8s | Style: Cinematic

A businesswoman in a grey suit stands in a sterile office, staring at rain on the window.
The lights flicker. She turns. Her eyes begin to glow blue-white.
Camera: Crash Zoom In on her eyes.
Her form expands slowly, suit pulling at the seams.
Style: Cinematic. Cold fluorescent transitioning to deep electric blue. 16:9.
Apply Cyborg preset for the transformation sequence.
```

### Into the Wild
```
Model: Wan 2.5
Aspect: 16:9 | Duration: 8s | Style: Abstract

A man stands at the edge of a forest at night, arms outstretched.
Moonlight through the canopy.
Camera: Crane Up as transformation begins — he starts to lose human form.
Style: Abstract. Deep greens and silvers, moonlight as only source. 16:9.
Apply Animalization preset — he becomes a wolf, launching into the forest dark.
```

### Awakening II — Seedance 2.0 (Transformation prompt mode)

```
Model: Seedance 2.0 (Transformation prompt mode)
Aspect: 16:9 | Duration: 8s | Style: Cinematic

Style & Mood: sterile cold-fluorescent boardroom shifting to deep electric
blue glow as the change takes hold, anamorphic flares on overhead lights,
crushed shadows on the floor.

Dynamic Description: A businesswoman in a charcoal grey suit stands at the
window, rain on the glass behind her, her reflection faintly visible. The
overhead fluorescents flicker once. She turns toward camera, her eyes
beginning to glow blue-white from within. Mid-frame, her form expands
slowly — the suit's seams pulling tight, fabric stretching at the shoulders,
hairline fissures of blue light tracing along her sternum and forearms. She
ends standing taller, the suit fully strained, her eyes fully luminous, the
boardroom now bathed in cold blue cast from her own light.

Static Description: Modern corporate boardroom at night, floor-to-ceiling
windows, rain on the glass, conference table in soft focus behind her.

Camera: slow crash-zoom in toward her face, settling on the eyes at
mid-transformation, holding through the end state.

Audio: her voice anchors the scene — a low controlled hum begins in her
throat as the fluorescents flicker, soft and human at first. Through the
mid-transformation it lowers in pitch, gains a second harmonic underneath,
and resolves at the end as something other-than-human: a sustained tone
the suit can no longer contain. Surrounding sound recedes: rain on glass,
the ballast hum dropping with her, fabric stress under the expansion. No
music.
```

Transformation prompt mode requires an explicit midpoint — the seams
pulling, the fissures of light — without which the model either snap-cuts
between start and end or renders an ambiguous blur. The arc is one
continuous take inside a single 8-second clip. See
`skills/higgsfield-seedance/SKILL.md` § Transformation for the construction
pattern.

---

## Seedance-4K Film Tutorial — Worked Examples

Curated from Higgsfield's official Seedance-4K one-minute film tutorial
[DEMO — Higgsfield Seedance-4K film tutorial, 2026-07, prompts verbatim from
the official blog]. All prompts ran on Seedance 2.0 at 4K, 16:9. Long prompts
are excerpted here to their load-bearing blocks — `[…]` marks omitted text.
Full versions of all 25 tutorial prompts are on the source blog:
higgsfield.ai/blog/seedance4k-breakdown.

### Scene 4 — Snow Leopard Super-Telephoto Zoom (Prompted Imperfection)

The reusable technique is *prompted imperfection*: real long-lens footage is
flawed, so the prompt requests the flaws — heat-haze swim, telephoto
micro-tremor, mushy digital-zoom smear, a brief focus hunt — and the clip
reads as captured, not generated. Atmosphere is quantified and ramped
(20% → 70% haze density) rather than described adjectivally, and the lens is
specified in FOV degrees (84° → 8°), never mm. 10s, one fixed tripod spot,
pure optical zoom.

```
OPTICS
A single massive optical zoom from WIDE 84° FOV to super-telephoto 8° FOV,
stopping at a HALF-BODY framing of the leopard (head, chest and shoulders,
roughly half the body). Extreme compression at the long end — mountain layers
flattened into stacked planes. Genuine long-distance super-tele character:
from the moment the zoom pushes long, and strongly by the close end, the
image swims and ripples with heat-haze and atmospheric distortion, edges
shimmering as if seen through rising air over miles; a constant nervous
telephoto micro-tremor, the framing trembling and drifting; the picture grows
softer and slightly mushy, fine sharpness falling off into gentle blur and
faint digital-zoom smear with light grain; a brief focus hunt before it
settles on the cat. The wide start is clean and crisp; these artifacts build
hard as it zooms in. Continuous push, no drift between beats.

LIGHTING
[…] Atmospheric haze builds across the shot — roughly 20% density at the wide
start rising to about 70% at the long compressed end, visible deep into the
layered peaks.

POSITIVE LOCKS
The camera stays in one fixed spot — static tripod, pure optical zoom only,
never cuts and never leaves its spot. […] The long-lens look stays clearly
realistic and imperfect — visible heat-haze swim, telephoto jitter, soft
mushy grain, all building as it zooms in. […]

[… full prompt also states camera and subject motion separately on a
second-by-second 10s clock, and describes the leopard entirely in-prompt
(no reference sheet) with an every-frame consistency lock.]
```

### Scene 5 — Truck vs. Snow Monster (Coordinate Blocking + Per-Segment LENS LOCKs)

The tutorial's flagship 16-second action shot, six segments in one prompt.
Three reusable techniques: **coordinate blocking** — subject and storm are
pinned to x%/y% frame positions with locked screen direction, so the chase
geometry can't drift; **timestamped cut grammar** — FORMAT MODE names the cut
type at each second (HARD, SMASH to slow-mo, MATCH); **per-segment LENS
LOCKs** — every segment carries its own FOV-degree lock so the lens holds
inside a segment and changes only on the cut.

```
FIRST FRAME AND SPATIAL BLOCKING
The first visible frame is an extreme super-wide aerial-height establishing
vista — maximum scope, @truck1 a tiny speck. The truck sits deep background,
left-of-center, x 38%, y 44%, scale tiny (under 4% of frame width), driving
left-to-right at full speed. […] The blizzard wall fills the background
behind and to the left, x 0% to 70%, upper half of frame, advancing rightward
— always behind the truck, never in the open road ahead. No empty plate — the
truck is present and moving left-to-right in frame one. […]
Truck travel direction: screen-left to screen-right, locked; clear road ahead
at screen-right. Storm and monster locked to screen-left/rear (behind). […]

FORMAT MODE
Controlled six-segment sequence in one continuous escalating beat. Seg 1
real-time push-in. Seg 2 real-time obstacle gauntlet. Seg 3 real-time
"shark-under-snow" stalk. Seg 4 slow-motion fake-out (claw miss). Seg 5
slow-motion scoop, launch, and mid-air rotations. Seg 6 low ground-level shot
as the truck rolls in and stops upside down. HARD CUT at 3.0s, HARD CUT at
6.0s, SMASH CUT to slow motion at 9.0s, continue slow motion through the
scoop, MATCH CUT to the ground angle at 13.5s. No subtitles, no music.

OPTICS
Prime-lens optical character throughout — clean, sharp center field, gentle
natural falloff, no zoom-breathing, fixed-focal clarity.
LENS LOCK SEG 1 = begin 107° wide rectilinear (immense environment, straight
horizon, truck tiny, no fisheye), settling toward 84° classic wide as it
closes on the cab. No drift beyond this push.
LENS LOCK SEG 2 = 84° classic wide, low and close, foreground wrecks and
barricades looming and ripping past the lens, immersive speed, straight lines
rectilinear.
LENS LOCK SEG 3 = 47° standard normal side profile, truck and the moving
snow-bulge both readable, grounded perspective.
LENS LOCK SEG 4 = 29° short telephoto, slight compression on the near-miss
claw and the heroes' faces, the monster looming soft behind.
LENS LOCK SEG 5 = 47° standard normal for the launch/flip — natural human-eye
proportions, no distortion as the truck tumbles.
LENS LOCK SEG 6 = 84° classic wide, low ground-level — the truck looms large
rolling toward the lens, foreground snow road across the lower frame, no
fisheye.

[… full prompt also carries SCENE CONTEXT, ACTIVE REFERENCES, LOCATION MAP,
per-segment CAMERA moves, second-by-second ACTION TIMING, PERFORMANCE,
detailed flip PHYSICS (wheels stay mounted, spinning), COLOR GRADE, LIGHTING,
WARDROBE, STYLE, OUTPUT SETTINGS, and POSITIVE LOCKS — see the source blog.]
```

### Scene 5b — Finished Clip Playing on an In-Frame TV (1:1 Video Reference + SCREEN REALISM)

How to composite a finished generation onto a screen inside a new shot: attach
the clip as `@video_1` with a 1:1 role that forbids reinterpretation, and add
a SCREEN REALISM block so the picture reads as a filmed physical panel rather
than a pasted overlay. Two rules travel with the technique: the new
generation's duration must exactly match the reference clip's (the tutorial
trimmed Scene 5 to its first 6s to feed this 6s composite — otherwise
Seedance starts making things up), and never leave in-frame screen content
unspecified.

```
ACTIVE REFERENCES
[…]
@video_1 — the footage playing on the TV: on-screen content matches the
source 1:1 — same image, timing, framing, motion and colors, never
reinterpreted, re-edited, cropped, looped early, or replaced.

SCREEN REALISM
The TV picture reads as a real physical panel being filmed, not a clean
digital overlay: the picture sits behind the glass panel and carries a faint
glass sheen and soft glare, dim reflections of the room and window on the
screen surface, a subtle pixel/sub-pixel grid and gentle moiré, slight bloom
on the brightest areas, mild panel contrast and color shift, and a small
off-axis perspective from the side viewing angle. The underlying picture
stays fully recognizable as @video_1.

[… full prompt also blocks the watcher low and to one side so the screen
stays unobstructed, locks the camera static for the full 6 seconds, and
repeats the 1:1 and screen-size locks in POSITIVE LOCKS — see the source
blog.]
```

### Scene 6 — Remote Close-Up (Red-Arrow Annotation + Exactly-One-Press Lock)

The actor kept pressing the wrong button, so the fix happened on the *asset*:
a red arrow drawn onto the prop reference sheet, then encoded in the prompt
text so the model reads the annotation. The single press is then locked three
times — in the blocking, on the action clock, and in POSITIVE LOCKS — and the
buttons to avoid are steered with positive phrasing ("stays clear of"), never
negation. 4s static macro at 12° FOV.

```
ACTIVE REFERENCES
@REMOTE — matte black household streaming remote. 100% matches the reference.
[…] a CH rocker on the RIGHT (UP chevron ˄ top, "CH" mid, DOWN chevron ˅
bottom). The reference's red arrow points precisely to the CH-UP chevron (˄)
directly above the "CH" label.

ACTION
0.0s–1.0s — the left hand rests on the left thigh holding @REMOTE, thumb
resting on the lower-right face just over the CH-UP chevron (˄) directly
above the "CH" label, where the red arrow points; matte black surface
catching soft cool ambient light.
1.0s–2.0s — the thumb presses the CH-UP chevron (˄) one single time — a
deliberate press, the button giving slightly under the pad, one soft
mechanical click as the channel changes. The thumb stays clear of the VOL
rocker to the left, the navigation pad above, and the CH-DOWN chevron (˅)
below — only CH-UP.
2.0s–4.0s — the thumb lifts off and settles back, the hand resting steady on
the thigh, @REMOTE held still, no further presses.

POSITIVE LOCKS
[…] The thumb presses the CH-UP chevron (˄) directly above "CH" on the
lower-right CH rocker, where the reference red arrow points — exactly ONE
time, a single clear press-and-release, then it lifts off and the hand holds
still. […]
```

### Scene 8 — Battle v1 → v2: the VARIETY-Reference Fix (Clone Army)

**Before (v1):** the elven army used a single-character reference labeled a
STYLE reference, with "every elf unique" asked for in prose — and produced an
army of identical clones, because references outrank text. **After (v2):**
the fix is not better wording but a better asset — a lineup sheet of FOUR
fully distinct elves, attached in place of the single character and relabeled
a **VARIETY reference**. The rest of the prompt is unchanged; only the `@elf`
role line and its POSITIVE LOCKS sentence differ (plus the matching cape /
filigree accents in COLOR GRADE).

v1 — `@elf` role line (produced the clone army):
```
@elf — STYLE reference for the elven army: silver-and-gold leaf-filigree
armor, pale-blue capes, elven swords. The army is a varied host — men and
women, each a distinct face, hair color, build, helmet and cape, every elf
unique while keeping this armor-and-weapon style, each fighting with a sword
and striking only at orcs. 100% matches the reference style.
```

v2 — only the changed lines (with the 4-elf lineup sheet attached as `@elf`):
```
@elf — VARIETY reference for the elven army: a sheet of FOUR different elves
— men and women, blonde / dark / auburn / silver hair, silver-, gold- and
rose-toned leaf-filigree armor with capes, elven swords. The army is a varied
host drawn from these four types — a mix of men and women with different
faces, hair colors, builds and armor tones, every elf unique, no two alike,
each fighting with a sword and striking only at orcs.

POSITIVE LOCKS
[…] The elven army is a VARIED host built from the four elf types in @elf —
men and women, mixed hair colors and silver/gold/rose armor tones, every elf
unique and no two alike — each fighting with a sword in hand. […]
```

The general rule: one character reference = one identity, everywhere it
appears. When a reference should seed a *population*, attach a multi-character
lineup sheet and name its role VARIETY reference — diversity has to live in
the pixels, not just the prose.
