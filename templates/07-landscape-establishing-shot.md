# Template: Landscape / Establishing Shot

## Genre/Use-Case
Wide establishing shots, nature/environment sequences, time-lapse landscapes, epic scale reveals, and any prompt where the environment IS the subject.

## When to use this template
User asks for an establishing shot, landscape, nature video, environment reveal, aerial view, timelapse, or any prompt where no character is the primary focus.

## Recommended model
**Veo 3 / 3.1** for nature and environment (best at stable, realistic landscapes). **Sora 2** for epic scale and physics (weather, water, destruction). **Wan 2.5** for painterly/fantasy landscapes.

## Example prompt

```
Model: Veo 3.1
Aspect: 16:9 | Duration: 10s | Style: Cinematic natural

Open ocean at dusk. The horizon is dark with an approaching storm.
Waves are already running ahead of it — three-meter swells, grey-green water.
Camera: Timelapse Landscape as the storm front advances, sky darkening fast.
Lightning inside the clouds. Then the first rain hits the surface.
Style: Cinematic, natural grade, no artificial treatment. 16:9.
```

## Annotation

| Prompt element | Why it works |
|---------------|-------------|
| "Open ocean at dusk" | Specific time + location — not "beautiful nature scene" |
| "horizon is dark with an approaching storm" | Establishes narrative tension in a landscape — something is coming |
| "three-meter swells, grey-green water" | Measurable scale + specific color — observable details |
| "Timelapse Landscape" | Exact preset name for time-compressed environment footage |
| "storm front advances, sky darkening fast" | Describes what CHANGES — not a static description |
| "Lightning inside the clouds" | Specific atmospheric event — model knows how to render this |
| "first rain hits the surface" | Payoff moment — the change the entire shot builds toward |
| "natural grade, no artificial treatment" | Tells the model NOT to stylize — keep it documentary-real |

## Negative constraints to include
- **Texture/Lighting**: Specify "natural grade" to prevent the model from adding cinematic color grading to nature footage.
- **Temporal/Consistency**: One environmental change per clip. "Storm + earthquake + volcanic eruption" = chaos.

> **Identity/Motion separation:** If a person appears in this shot and you're using Soul ID, split the prompt into Identity Block and Motion Block per the rule in `higgsfield-soul`. See template 06 (Portrait/Character Intro) for the full pattern.

## Common mistakes
1. **Adding a character to a landscape shot** — if the environment is the subject, let it be the subject. Characters in establishing shots should be tiny ("a lone figure" at most).
2. **No temporal change** — landscapes need something to happen: weather moves, light shifts, tide changes. A static description produces a still image, not video.

## Variations
- **Mountain sunrise**: Timelapse Landscape, "first light crests the ridge, fog burns off the valley below"
- **Urban establishing**: Hyperlapse down a boulevard, "city wakes up from dawn to rush hour"
- **Aerial/drone**: FPV Drone or Crane Up, sweeping terrain reveal
- **Fantasy landscape**: Wan 2.5, add "jewel tones, volumetric light rays through ancient forest canopy"
- **Post-apocalyptic**: Desaturated orange and brown, dust haze, "ruined skyline, no movement except wind"

## Cinema Studio 3.0 (Business/Team Plan)

**Genre mapping:** Epic (for sweeping vistas) or General
**Prompt length target:** 30–60 words (Landscape/Travel — lead with Scene)
**Speed Ramp:** Auto (let the scene breathe)

**@reference workflow:**
```
@Image1 as the landscape reference. Dawn breaks over the volcanic ridge,
mist pouring through the caldera. Birds scatter from the tree line.
Camera: crane up revealing the full valley. Style: natural color, deep depth of field.
Audio: wind across open terrain, distant bird calls, rushing water below.
```
