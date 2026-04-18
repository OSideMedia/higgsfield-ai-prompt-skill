# Template: Cinematic Action Chase

## Genre/Use-Case
High-energy pursuit sequences — foot chases, vehicle pursuits, rooftop escapes, anything with sustained kinetic movement and urgency.

## When to use this template
User asks for a chase scene, pursuit, escape, running sequence, parkour, or any prompt where the primary energy is "someone moving fast through a space while something is at stake."

## Recommended model
**Kling 3.0** for character-focused chases (face stays consistent, native audio for footsteps/impacts). **Sora 2** for large-scale or vehicle chases where environment physics matter more than character fidelity.

## Example prompt

```
Model: Kling 3.0
Aspect: 16:9 | Duration: 10s | Style: Cinematic

A woman in a tactical jacket sprints through a rain-soaked night market,
weaving between stalls and startled vendors. Steam rises from food carts.
Neon signs fracture in every puddle.
Camera: Action Run — low behind her, matching pace.
A metal gate drops ahead. She slides under it without breaking stride.
Style: Cinematic. Cold blue shadows, warm amber market light, high contrast. 16:9.
```

## Annotation

| Prompt element | Why it works |
|---------------|-------------|
| "tactical jacket" | Specific clothing grounds the character — not "a woman running" |
| "rain-soaked night market" | Wet surfaces + neon = visual complexity the model renders well |
| "weaving between stalls and startled vendors" | Active verbs (weaving, startled) give the model motion direction |
| "Steam rises from food carts" | Atmospheric motion fills dead space in the frame |
| "Neon signs fracture in every puddle" | Reflection cue — models respond to reflective surface prompts |
| "Camera: Action Run" | Exact preset name — model knows this movement pattern |
| "low behind her, matching pace" | Clarifies the camera's spatial relationship to the subject |
| "A metal gate drops ahead. She slides under it" | One clear obstacle + one clear response = clean action beat |
| "Cold blue shadows, warm amber market light" | Dual-color grade gives the model a specific palette, not "cinematic" generically |

## Negative constraints to include
- **Body/Motion**: Limit to 1 primary action + 1 secondary. Don't ask for a chase + fight + explosion in one clip.
- **Temporal/Consistency**: Use one camera movement per shot. Don't combine Action Run + Bullet Time in a single generation — chain them as separate clips.
- **Face/Identity**: If using Soul ID, separate identity description from motion description.

> **Identity/Motion separation:** If a person appears in this shot and you're using Soul ID, split the prompt into Identity Block and Motion Block per the rule in `higgsfield-soul`. See template 06 (Portrait/Character Intro) for the full pattern.

## Common mistakes
1. **Too many camera switches in one prompt** — "Action Run then Whip Pan then Bullet Time" creates visual soup. One camera per clip, chain in post.
2. **Generic camera language** — "camera follows dramatically" does nothing. Name the exact preset.

## Variations
- **Grittier/handheld feel**: Swap camera to Handheld, add "shaky, documentary urgency" to style
- **Vehicle chase**: Use Sora 2 + Car Chasing camera preset, describe the vehicles specifically
- **Vertical/social format**: Change to 9:16, keep Action Run but note "close framing, face visible"
- **Sci-fi chase**: Add zero gravity or corridor environment, swap to FPV Drone camera

## Cinema Studio 3.0 (Business/Team Plan)

**Genre mapping:** Action
**Prompt length target:** 60–100 words (Drama/Narrative range — lead with Scene)
**Speed Ramp:** Bullet Time for impact moments, Ramp Up for acceleration

**@reference workflow:**
```
Reference @Video1 for chase choreography and pacing.
A woman sprints through a rain-soaked night market, sliding under a metal gate.
Gravel sprays, steam scatters from food carts. Camera: tracking, low angle.
Style: cold blue shadows, warm amber market light.
```
