# Template: Product / UGC Showcase

## Genre/Use-Case
Product reveals, commercial beauty shots, UGC-style product demos, unboxing aesthetics, and brand content where the product is the hero.

## When to use this template
User asks for a product ad, commercial, product video, "make my product look good," unboxing, packshot, or any prompt where the hero subject is an object (not a person).

## Recommended model
**Nano Banana Pro** for the hero image (maximum sharpness, 4K). **Kling 3.0** for video animation (best texture rendering). **Robo Arm** or **Lazy Susan** camera for product reveals.

## Example prompt

```
Model: Kling 3.0 (video) / Nano Banana Pro (image)
Aspect: 16:9 | Duration: 5s | Style: Cinematic commercial

A matte black insulated travel mug, minimal design, no branding.
Placed on a raw concrete countertop beside a morning window.
Camera: Robo Arm arcing slowly from the base up and around to the lid.
Hot coffee pours in — steam rises in a slow macro close-up.
A hand wraps around the mug. Camera: Dolly In to hands + warmth detail.
Style: Cinematic commercial. Warm neutral tones, soft diffused natural light. 16:9.
Sound: gentle liquid pour, soft ceramic texture.
```

## Annotation

| Prompt element | Why it works |
|---------------|-------------|
| "matte black insulated travel mug, minimal design, no branding" | Precise material + color + form. No brand names (filter safe). |
| "raw concrete countertop" | Specific surface texture — models render product-on-surface well when the surface is named |
| "beside a morning window" | Establishes light source naturally — soft, directional, warm |
| "Camera: Robo Arm arcing slowly" | Precision mechanical arc — purpose-built for product reveals |
| "from the base up and around to the lid" | Tells the model the exact path of the camera — not "orbiting" generically |
| "Hot coffee pours in — steam rises" | Hero moment: macro texture + steam = visual payoff |
| "A hand wraps around the mug" | Human interaction grounds the product emotionally |
| "Warm neutral tones, soft diffused natural light" | Measurable lighting — not "looks premium" |
| "Sound: gentle liquid pour" | Audio cue adds tactile dimension (Kling 3.0 renders this natively) |

## Negative constraints to include
- **Texture/Lighting**: Specify background surface and lighting source — generic = cheap-looking output
- **Temporal/Consistency**: One camera movement for the reveal, one for the detail shot — don't combine
- **Content Filter/Safety**: Never use brand names — describe the product by appearance only

> **Identity/Motion separation:** If a person appears in this shot and you're using Soul ID, split the prompt into Identity Block and Motion Block per the rule in `higgsfield-soul`. See template 06 (Portrait/Character Intro) for the full pattern.

## Common mistakes
1. **Naming the brand** — "A Nike sneaker" gets filtered. Say "a white athletic sneaker with a minimal swoosh-like logo" (or no logo at all).
2. **No surface/background specification** — product floating in undefined space looks amateur. Always name the surface.

## Variations
- **Dramatic/luxury feel**: Dark background, single hard side-light, use Lazy Susan for slow rotation
- **Social/UGC style**: 9:16 vertical, Handheld camera, "person holding product casually, natural daylight"
- **360 product spin**: Use 3D Rotation preset, pure black background, "sharp product detail, 4K, 1:1"
- **Food/beverage**: Use Extreme Macro lens in Cinema Studio, add steam/pour/drip as hero moment

## Cinema Studio 3.0 (Business/Team Plan)

**Genre mapping:** General
**Prompt length target:** 30–50 words (Product/E-commerce — lead with Subject)
**Speed Ramp:** Slow-mo for hero reveal, Auto for unboxing

**@reference workflow:**
```
@Image1 as the product. Smooth 360-degree orbit on a marble pedestal.
Soft studio lighting catches the matte-black finish. Subtle reflection on surface.
Camera: orbit. Style: clean white studio, shallow depth of field.
Audio: soft surface contact, gentle mechanical click.
```
