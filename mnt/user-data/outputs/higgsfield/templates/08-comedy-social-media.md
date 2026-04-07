# Template: Comedy / Social Media

## Genre/Use-Case
Comedic skits, social media content, reaction videos, meme-style clips, TikTok/Reels content, and any prompt where the goal is entertainment, humor, or shareability.

## When to use this template
User asks for funny content, social video, TikTok, Reel, skit, meme, reaction, or anything designed primarily for social platforms with a comedic or entertaining tone.

## Recommended model
**Kling 3.0** for dialogue-driven comedy (native audio, lip-sync). **Minimax Hailuo 2.3** for exaggerated physical comedy (best fluid motion). **Seedance Pro** for fast iteration on multiple comedic concepts.

## Example prompt

```
Model: Kling 3.0
Aspect: 9:16 | Duration: 8s | Style: Cinematic

A man sits at a desk staring at his laptop, dead-eyed.
He takes a long sip of coffee, blinks slowly, sets the mug down.
He says flatly: "This is fine."
Behind him through the window — a building is on fire, fire trucks arriving.
He doesn't turn around.
Camera: static, locked-off, medium shot. No movement.
Style: Cinematic, bright office lighting, high-key, neutral tones. 9:16.
```

## Annotation

| Prompt element | Why it works |
|---------------|-------------|
| "sits at a desk staring at his laptop, dead-eyed" | Establishes the comic setup — mundane normalcy |
| "takes a long sip... blinks slowly... sets the mug down" | Deliberate, deadpan timing — comedy lives in the pauses |
| `"This is fine."` | Dialogue in quotes for Kling 3.0 lip-sync — the punchline |
| "building is on fire, fire trucks arriving" | Background chaos contrasts foreground calm — visual joke |
| "He doesn't turn around" | The non-reaction IS the joke — telling the model what NOT to do |
| "static, locked-off, medium shot. No movement" | Comedy often works best with a still camera — lets the audience see everything |
| "bright office lighting, high-key" | High-key lighting = comedy convention (vs. low-key for drama) |
| "9:16" | Vertical for social platforms — where this content lives |

## Negative constraints to include
- **Temporal/Consistency**: Lock the camera — static or minimal movement. Comedy timing breaks with aggressive camera work.
- **Body/Motion**: Keep physical comedy to one gag per clip. "He slips, falls, gets hit by a pie, then trips again" is too much.
- **Face/Identity**: For lip-sync comedy, remove all head/face motion tokens — they compete with the lip engine.

## Common mistakes
1. **Over-directing the humor** — "make it funny and hilarious and comedic" tells the model nothing. Set up a specific situation with a specific punchline.
2. **Too much camera movement** — comedy timing needs the viewer to see everything at once. Static wide shots let the audience be the editor.

## Variations
- **Reaction video style**: Close-up on face, Kling 3.0 with audio, exaggerated micro-expression (Frozen Shock or Suppressed Smile)
- **Physical comedy**: Minimax Hailuo 2.3, wider shot, exaggerated movement, Apply Clone Explosion or Objects Around preset
- **Talking head/monologue**: 9:16, medium close-up, static camera, dialogue-driven, "direct to camera"
- **Meme format**: 1:1 square, static, bold simple setup, use Vibe Motion for text overlay

### Identity Block (if recurring character)
```
The Soul ID character — round face, large expressive eyes, slightly disheveled hair,
wearing a wrinkled button-up with the sleeves rolled. Perpetually tired.
```

### Motion Block
```
He sits at a desk, sips coffee, says "This is fine."
Camera: static, locked-off, medium shot.
Background: visible chaos through the window.
```

## Cinema Studio 3.0 (Business/Team Plan)

**Genre mapping:** Comedy
**Prompt length target:** 40–60 words (Lifestyle/Social — lead with Action)
**Speed Ramp:** Flash In / Flash Out for comedic timing

**@reference workflow:**
```
@Image1 as the character. He opens a gift box confidently.
A spring-loaded glitter bomb erupts in his face. He freezes, blinking.
Camera: static, deadpan framing. Style: bright, evenly lit, social media aesthetic.
Audio: box opening, explosion of glitter, stunned silence, distant laughter.
```
