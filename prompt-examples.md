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
Aspect: 2.35:1 | Duration: 8s | Style: Cinematic

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
Aspect: 2.35:1 | Duration: 10s | Style: Anamorphic

Two silhouettes grapple on a rain-slicked rooftop at night, city spread below them.
Lightning illuminates the scene in strobe flashes.
Camera: FPV Drone circling just outside their reach, catching each exchange of blows.
One figure is thrown backward — slides to the edge, barely catches the ledge.
Camera: Dutch Angle as they hang there, rain hammering down.
Style: Anamorphic. Deep desaturated blue-grey. Lens flare on distant lightning. 2.35:1.
Apply Bullet Time preset at the moment of the throw.
```

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

---

## Sci-Fi

### Zero Gravity Breach
```
Model: Sora 2
Aspect: 2.35:1 | Duration: 10s | Style: Cinematic

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
