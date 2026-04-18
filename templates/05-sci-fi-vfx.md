# Template: Sci-Fi / VFX Spectacle

## Genre/Use-Case
Science fiction environments, zero-gravity sequences, cyberpunk streets, futuristic technology reveals, energy effects, portal/transformation moments, and any prompt involving VFX-heavy visuals.

## When to use this template
User asks for sci-fi, cyberpunk, futuristic, space, zero gravity, energy effects, transformation, portal, or any prompt requiring VFX motion presets in a speculative setting.

## Recommended model
**Sora 2** for large-scale environments and physics-heavy spectacle. **Kling 3.0** for character-driven sci-fi with audio. **Wan 2.5** for stylized/artistic sci-fi.

## Example prompt

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

## Annotation

| Prompt element | Why it works |
|---------------|-------------|
| "battle-worn space station corridor" | Specific environment — not "a spaceship" generically |
| "emergency lighting" | Establishes color palette (red/amber warning lights) naturally |
| "debris floating in zero gravity" | Atmospheric detail the model renders well — adds life to the scene |
| "pulls herself along a handrail, rifle raised" | Physics-specific action in zero-G — tells the model HOW she moves |
| "a sealed blast door, sparking at the seams" | Visual tension — something dangerous behind the door |
| "She plants a charge and pushes back" | One clear action beat leading to the VFX payoff |
| "FPV Drone drifting just ahead of her" | Camera position relative to subject — immersive but clear |
| "cold steel blue, high contrast" | Sci-fi's signature palette — measurable color direction |
| "Apply Plasma Explosion preset at the detonation moment" | VFX preset named exactly, timed to a specific moment in the action |

## Negative constraints to include
- **Body/Motion**: One action per clip. "She fights aliens while the station explodes and a portal opens" = model breakdown.
- **Temporal/Consistency**: Place VFX preset instruction at the END of the prompt, clearly timed to an action beat.
- **Texture/Lighting**: Commit to one visual style — don't mix "gritty realism" with "neon cyberpunk."

## Common mistakes
1. **Stacking VFX presets** — "Apply Plasma Explosion + Portal + Glitch" in one clip overwhelms the model. One preset per generation.
2. **Contradictory physics** — "zero gravity" + "falls to the ground" confuses the model. Pick one physics environment.

## Variations
- **Cyberpunk street**: Ground-level, neon magenta/cyan palette, Dolly Out camera, add Glitch preset
- **Portal/dimensional**: Use Portal preset, Crane Up camera, "energy builds in a ring of light"
- **Transformation**: Use Cyborg or Turning Metal preset, Crash Zoom In on the transformation point
- **Space exterior**: Sora 2 + Super Dolly Out, "vast starfield, tiny ship approaching a planet"

### Identity Block (if using Soul ID character)
```
The Soul ID character — scarred face, shaved head, tactical body armor with shoulder-mounted
flashlight, dark under-eye fatigue, determined expression.
```

### Motion Block
```
She pulls herself along a handrail in zero gravity, rifle raised.
Plants a charge on the blast door. Pushes back.
Camera: FPV Drone drifting ahead through the corridor.
Apply Plasma Explosion preset at detonation.
```

## Cinema Studio 3.0 (Business/Team Plan)

**Genre mapping:** Epic (for large-scale) or Action (for combat)
**Prompt length target:** 50–90 words (Anime/Artistic range — lead with Style)
**Speed Ramp:** Hero Moment for reveals, Bullet Time for zero-gravity

**@reference workflow:**
```
@Image1 as the environment concept. A spacecraft descends through storm clouds,
hull glowing from atmospheric friction. Debris scatters. Lightning illuminates the landing zone.
Camera: crane down tracking the descent. Style: anamorphic, teal and orange grade.
Audio: deep engine rumble, crackling electricity, wind shear.
```
