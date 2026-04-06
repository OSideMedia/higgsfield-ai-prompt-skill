# Template: Portrait / Character Introduction

## Genre/Use-Case
Character reveals, protagonist introductions, talking-head setups, emotional close-ups, and any prompt where the human face and expression are the primary subject.

## When to use this template
User asks for a character intro, portrait, close-up, emotional moment, reaction shot, or any prompt centered on a single person's face and presence.

## Recommended model
**Kling 3.0** for video (best character consistency + native audio for dialogue). **Soul 2.0** or **Nano Banana Pro** for the reference image. **Soul Cinema Preview** for cinematic keyframes.

## Example prompt

### Identity Block
```
The Soul ID character — a man in his late 40s, weathered skin, deep-set eyes,
salt-and-pepper stubble, wearing a worn leather jacket over a dark henley.
A thin scar across the left eyebrow.
```

### Motion Block
```
He stands at the edge of a rain-soaked harbour dock at night.
He stares at the horizon, collar turned up against the driving rain.
Camera: slow Dolly In from medium-wide to medium close-up.
Style: Cinematic. Crushed blacks, single sodium-vapour key light from the right,
cold blue fill. 2.35:1 anamorphic.
```

### Combined prompt (for non-Soul ID use)
```
Model: Kling 3.0
Aspect: 2.35:1 | Duration: 8s | Style: Cinematic

A weathered man in his late 40s stands at the edge of a rain-soaked harbour dock at night.
Salt-and-pepper stubble, worn leather jacket, collar turned up against the driving rain.
An old leather briefcase sits at his feet, open, papers scattered by the wind.
He stares at the horizon.
Camera: slow Dolly In from medium-wide to medium close-up.
Style: Cinematic. Crushed blacks, single sodium-vapour key light from the right,
cold blue fill. 2.35:1 anamorphic.
```

## Annotation

| Prompt element | Why it works |
|---------------|-------------|
| "late 40s, weathered skin, deep-set eyes" | Observable physical traits — not "handsome" or "attractive" |
| "salt-and-pepper stubble" | Texture detail the model renders well at close range |
| "thin scar across the left eyebrow" | Distinguishing mark — helps Soul ID lock identity |
| "rain-soaked harbour dock at night" | Specific environment with atmospheric conditions |
| "collar turned up against the driving rain" | Small physical action reveals character without dialogue |
| "slow Dolly In from medium-wide to medium close-up" | Gradual intimacy build — starts environmental, ends personal |
| "sodium-vapour key light from the right, cold blue fill" | Named light types with direction — not "dramatic lighting" |
| "2.35:1 anamorphic" | Widescreen + shallow DOF = cinematic portrait standard |

## Negative constraints to include
- **Face/Identity**: Keep all face/body descriptors in the Identity Block. Keep camera and motion in the Motion Block. Mixing them causes face warping.
- **Temporal/Consistency**: For multi-shot character work, copy the Identity Block verbatim across all prompts.
- **Body/Motion**: One emotion per shot. Don't ask for "angry then sad then surprised."

## Common mistakes
1. **"A beautiful/handsome person"** — unmeasurable. Describe bone structure, skin texture, expression, clothing.
2. **Describing the face AND giving vigorous motion** — "she laughs and spins and runs" with detailed face description causes drift. For expressive movement, use micro-expression terms from `higgsfield-soul`.

## Variations
- **Dialogue intro**: Add speech in quotes: `He says quietly: "It's done."` Use Kling 3.0 for native lip-sync
- **Dramatic reveal**: Start with Overhead or Extreme Wide, Crane Down to close-up
- **Super 8MM nostalgia**: Swap style to Super 8MM, warm grain, soft vignette, 4:3
- **Editorial/fashion**: Swap to high-key lighting, Clinical Sharp Prime lens in Cinema Studio

## Cinema Studio 3.0 (Business/Team Plan)

**Genre mapping:** Drama
**Prompt length target:** 60–100 words (Drama/Narrative — lead with Scene)
**Speed Ramp:** Slow-mo for emotional weight, Auto for natural pace

**@reference workflow:**
```
@Image1 as the character. She sits at a café table, stirring coffee absently.
She notices someone through the window — expression shifts from sadness to surprise.
Camera: slow push-in. Style: warm interior light, shallow depth of field.
Audio: ceramic mug on saucer, spoon stirring, muffled street noise through glass.
```
