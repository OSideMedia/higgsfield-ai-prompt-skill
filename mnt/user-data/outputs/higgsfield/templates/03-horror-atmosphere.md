# Template: Horror / Atmospheric Dread

## Genre/Use-Case
Horror scenes, supernatural tension, psychological dread, jump-scare setups, uncanny valley moments, and any prompt where the goal is to unsettle the viewer.

## When to use this template
User asks for horror, scary, creepy, unsettling, supernatural, haunted, psychological thriller, or anything where the mood is dread rather than action.

## Recommended model
**Kling 3.0** for character horror (face control matters). **Wan 2.5** for stylized/supernatural horror (leans into surreal aesthetic). Use **VHS** or **Cinematic low key** style.

## Example prompt

```
Model: Kling 3.0
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

## Annotation

| Prompt element | Why it works |
|---------------|-------------|
| "unlocks the door... Steps inside. Everything looks normal." | False calm — establishes normalcy before breaking it |
| "Sets down her keys. Turns toward the kitchen." | Small, mundane actions create real-world grounding |
| "slow Dolly In toward the hallway mirror" | Slow movement builds dread — the viewer knows something is wrong before the character does |
| "the couch is against the wrong wall" | The "wrong detail" — something subtle and deeply unsettling, not gore |
| "She hasn't moved. The reflection has." | Payoff: the specific violation of reality that creates horror |
| "Dutch Angle as she realizes" | Camera tilt = psychological instability in the character |
| "VHS. Desaturated greens, practical light only" | VHS grain + sickly color = analog horror aesthetic that triggers unease |
| "4:3" | Narrow aspect ratio increases claustrophobia |
| "Apply Horror Face preset" | Motion preset handles the VFX scare — don't try to describe face distortion manually |

## Negative constraints to include
- **Content Filter/Safety**: Describe atmosphere ("dread", "unsettling", "something is wrong") not explicit gore. Use motion presets for horror VFX.
- **Face/Identity**: If using Soul ID, keep face description clean and separate from the horror effect.
- **Temporal/Consistency**: Slow camera movements work best for horror — fast cuts break the tension build.

## Common mistakes
1. **Describing explicit gore/injury** — gets blocked by content filters. Describe the dread and atmosphere, let the viewer's imagination do the work.
2. **Too many scares in one clip** — one "wrong detail" per generation. Stack them across a sequence, not in a single shot.

> **Identity/Motion separation:** When this horror scene features a Soul ID character, use the following block structure.

### Identity Block (if using Soul ID character)
```
The Soul ID character — pale complexion, dark circles under eyes, wearing
a grey oversized sweater, dark hair loose.
```

### Motion Block
```
She steps inside, sets down her keys. Turns toward the kitchen.
Camera: slow Dolly In toward the hallway mirror.
Dutch Angle as she freezes.
```

## Variations
- **Found footage style**: Handheld camera, VHS style, 4:3, "camera glitches occasionally"
- **Psychological (no supernatural)**: Remove Horror Face preset, rely on Dutch Angle + slow Dolly In + "wrong detail"
- **Body horror**: Use Monstrosity or Gas Transformation preset instead of Horror Face
- **Jump scare setup**: Slow Dolly In for 6s, then Crash Zoom In on the reveal for the final 2s

## Cinema Studio 3.0 (Business/Team Plan)

**Genre mapping:** Horror
**Prompt length target:** 60–100 words (Drama/Narrative range — lead with Scene)
**Speed Ramp:** Flash In for jump scares, Slow-mo for dread

**@reference workflow:**
```
@Image1 as the corridor environment. A figure appears at the far end, barely visible.
Floorboards creak. The lights flicker once, twice. Camera: slow dolly push.
Style: desaturated, single practical light source, deep shadows.
Audio: distant dripping, wood creaking, a breath that isn't the viewer's.
```
