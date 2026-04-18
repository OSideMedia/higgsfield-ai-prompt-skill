# Template: Fashion / Editorial

## Genre/Use-Case
Fashion lookbook content, editorial-style portraits, outfit showcases, runway aesthetics, brand campaigns, and style-forward character introductions.

## When to use this template
User asks for fashion content, editorial, lookbook, outfit showcase, model portrait, style campaign, or any prompt where clothing/aesthetic is the hero.

## Recommended model
**Soul 2.0** for portrait-first fashion (best with Moodboard + Color Transfer). **Nano Banana Pro** for maximum sharpness and detail. **Kling 3.0** for video with slow, deliberate camera movement.

## Example prompt

### Identity Block
```
The Soul ID character — angular jawline, dark skin, close-cropped natural hair.
Wearing a structured black wool overcoat, wide-leg trousers, white minimalist sneakers.
Silver chain necklace. Hands in pockets.
```

### Motion Block
```
She walks slowly toward camera down an empty concrete corridor.
Camera: Dolly Out — retreating as she advances, never quite letting her fill the frame.
Style: Cinematic. High contrast, desaturated cool tones, single overhead strip light
casting a hard shadow. 2.35:1 anamorphic.
```

### Combined prompt (for non-Soul ID use)
```
Model: Kling 3.0
Aspect: 2.35:1 | Duration: 8s | Style: Cinematic

A woman with angular jawline, dark skin, and close-cropped natural hair walks slowly
toward camera down an empty concrete corridor. She wears a structured black wool overcoat,
wide-leg trousers, white minimalist sneakers. Silver chain necklace. Hands in pockets.
Camera: Dolly Out — retreating as she advances.
Style: Cinematic. High contrast, desaturated cool tones, single overhead strip light. 2.35:1.
```

## Annotation

| Prompt element | Why it works |
|---------------|-------------|
| "angular jawline, dark skin, close-cropped natural hair" | Specific face descriptors — not "beautiful model" |
| "structured black wool overcoat" | Material + color + silhouette — the model renders fabric better with material names |
| "wide-leg trousers, white minimalist sneakers" | Full outfit top-to-bottom grounds the character |
| "Silver chain necklace" | One accessory detail adds realism without over-specifying |
| "walks slowly toward camera" | Deliberate pace = editorial energy, not action energy |
| "Dolly Out — retreating as she advances" | Creates visual tension — subject and camera in opposition |
| "single overhead strip light casting a hard shadow" | Fashion-specific lighting — creates drama with minimal setup |
| "2.35:1 anamorphic" | Ultra-wide = editorial cinema feel, horizontal bokeh |

## Negative constraints to include
- **Face/Identity**: Separate Identity Block (appearance, clothing) from Motion Block (walk, camera). This prevents face drift during camera movement.
- **Texture/Lighting**: Name the light source specifically. "Good lighting" produces nothing.
- **Temporal/Consistency**: For a series, copy-paste exact clothing/appearance description across all prompts.

## Common mistakes
1. **"Beautiful model in stylish outfit"** — every word is unmeasurable. Name the clothing items, describe the face, specify the light.
2. **Too much motion for editorial** — fashion is about deliberate, minimal movement. Walk, turn, stop. Not run, jump, spin.

## Variations
- **Street style**: Handheld camera, natural light, urban environment, J-Magazine Mixed Media preset
- **High-fashion surreal**: Abstract style, Creative Tilt Lens in Cinema Studio, unusual environment
- **Lookbook grid**: Cinema Studio Grid Generation (2×2 or 4×4) with different outfit variations
- **Social/vertical**: 9:16, Arc camera slowly around subject, warm golden light

## Cinema Studio 3.0 (Business/Team Plan)

**Genre mapping:** Drama (for editorial narrative) or General (for lookbook)
**Prompt length target:** 40–60 words (Lifestyle/Social — lead with Action)
**Speed Ramp:** Slow-mo for fabric movement, Auto for walk sequences

**@reference workflow:**
```
@Image1 as the model's character reference. She turns slowly on a rooftop at golden hour,
silk jacket catching the wind. Camera: smooth 180-degree orbit.
Style: warm tones, shallow depth of field, anamorphic.
Audio: fabric rustling, distant city ambience.
```
