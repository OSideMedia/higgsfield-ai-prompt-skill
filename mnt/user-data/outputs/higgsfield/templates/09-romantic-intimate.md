# Template: Romantic / Intimate Moment

## Genre/Use-Case
Romance scenes, intimate character moments, love stories, emotional connection beats, wedding/couple content, and any prompt centered on tenderness between characters.

## When to use this template
User asks for romance, love scene, intimate moment, couple content, wedding video, emotional connection, or any prompt where the energy is warmth and closeness.

## Recommended model
**Kling 3.0** for character-focused romance with audio (soft ambient, dialogue whispers). **Kling 2.6** (legacy) for no-audio emotional scenes. Style: **Cinematic** or **Super 8MM**.

## Example prompt

```
Model: Kling 3.0
Aspect: 16:9 | Duration: 8s | Style: Cinematic

Two people on a rooftop terrace at dusk, city glowing below them.
They've been talking for hours — coffee cups empty, leaning close.
A long pause. She looks at him.
Camera: Arc slowly around both of them, city blurring behind.
He reaches over and tucks a strand of hair behind her ear.
Style: Cinematic. Golden hour warm tones, shallow depth of field. 16:9.
Ambient: quiet city hum, distant traffic, gentle wind.
```

## Annotation

| Prompt element | Why it works |
|---------------|-------------|
| "rooftop terrace at dusk, city glowing below" | Romantic setting with natural warm light — environment does the work |
| "been talking for hours — coffee cups empty" | Tells a story in two details — implies history without exposition |
| "leaning close" | Physical proximity signals intimacy without explicit direction |
| "A long pause. She looks at him." | The moment before the moment — tension lives in the pause |
| "Arc slowly around both of them" | Arc camera isolates two people from the world — classic romance movement |
| "city blurring behind" | Shallow DOF makes the world disappear — only they matter |
| "tucks a strand of hair behind her ear" | One small, specific, tender gesture = more powerful than a grand action |
| "Golden hour warm tones" | Warm palette = emotional warmth — universal cinema convention |
| "quiet city hum, distant traffic" | Ambient audio creates intimacy — the world is far away |

## Negative constraints to include
- **Face/Identity**: If using Soul ID for both characters, use separate Identity Blocks for each. Reference clearly ("Character A" and "Character B").
- **Body/Motion**: One tender gesture per shot. Don't stack "he touches her face, holds her hand, pulls her close" — one moment, held.
- **Temporal/Consistency**: Slow camera movements only. Fast cuts destroy romantic tension.

## Common mistakes
1. **Too many actions in the romantic beat** — the moment should breathe. One gesture, one look, one pause.
2. **Generic emotion words** — "they look lovingly at each other" is unmeasurable. Describe the physical action: "she tilts her head slightly, eyes softening."

## Variations
- **Super 8MM nostalgia**: Swap to Super 8MM style, warm grain, soft vignette, 4:3 — instant home movie feel
- **Rain romance**: Add rain, "they don't move to shelter", Dolly In instead of Arc
- **First meeting**: Two-shot, slight Focus Change between faces, "their eyes meet for the first time"
- **Bittersweet/farewell**: Dolly Out instead of Arc — camera retreating = emotional distance growing

### Identity Block (Character A)
```
A woman in her early 30s, dark wavy hair, wearing a light linen jacket,
delicate silver earrings. Relaxed posture, feet tucked under her on the chair.
```

### Identity Block (Character B)
```
A man in his early 30s, short beard, kind eyes, wearing a soft navy sweater
with the sleeves pushed up. Leaning forward slightly, elbows on his knees.
```

### Motion Block
```
A long pause. She looks at him.
Camera: Arc slowly around both of them.
He reaches over and tucks a strand of hair behind her ear.
Ambient: quiet city hum, distant traffic, gentle wind.
```

## Cinema Studio 3.0 (Business/Team Plan)

**Genre mapping:** Drama
**Prompt length target:** 60–100 words (Drama/Narrative — lead with Scene)
**Speed Ramp:** Slow-mo for emotional moments, Auto for natural pacing

**@reference workflow:**
```
@Image1 as Character A. @Image2 as Character B.
They walk along a beach at sunset, waves lapping at their feet.
She laughs, he reaches for her hand. Camera: slow tracking alongside.
Style: golden hour, warm tones, shallow depth of field, Super 8MM grain.
Audio: waves, sand underfoot, distant seagulls, soft laughter.
```
