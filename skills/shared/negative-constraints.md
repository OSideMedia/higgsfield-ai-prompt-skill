# Shared Negative Constraints Reference

When generating Higgsfield prompts, append the relevant constraint blocks below to
prevent common AI video/image generation artifacts. These are organized by category.
Sub-skills reference this file — always check the relevant categories for the prompt
you're building.

---

## Body / Motion Artifacts

These occur when the model can't resolve complex physical actions in a single generation.

| Artifact | Why it happens | Recommended prompt phrasing to prevent it |
|----------|---------------|------------------------------------------|
| **Floating / extra limbs** | Model hallucinates additional appendages when character pose is ambiguous or occluded | "Anatomically correct, all limbs visible and naturally positioned" |
| **Limb merging** | Two characters too close together — model can't distinguish whose arm is whose | Keep characters at arm's length or use separate shots; "distinct body separation between characters" |
| **Unnatural body proportions** | Over-specified conflicting body descriptors (tall + compact) or extreme angles | Pick one body descriptor, keep it consistent; avoid contradictory size cues |
| **Jittery / stuttering motion** | Too many actions requested in one clip — model oscillates between them | 1 primary action per clip + 1–2 secondary max; split complex sequences into separate generations |
| **Motion morphing on fast action** | High-speed movement exceeds model's temporal coherence | Generate in Slow Mo first, speed up in post (CapCut/Premiere/DaVinci) |
| **Specific martial arts failing** | Named moves (roundhouse kick, uppercut) require precise multi-frame choreography the model can't execute | "General fighting energy" or "struggling" instead of named combat moves; describe outcome, not technique |
| **Grappling renders as embracing** | Close-range physical contact is ambiguous to the model | Use plain text (not @ Elements) for action scenes; describe body positions, not grapple names |

---

## Face / Identity Artifacts

These occur when the model loses track of who a character is across frames or generations.

| Artifact | Why it happens | Recommended prompt phrasing to prevent it |
|----------|---------------|------------------------------------------|
| **Face morphing / shifting** | No Soul ID reference, or conflicting appearance descriptions in the prompt | Use Soul ID for multi-shot work; remove contradictory appearance descriptors |
| **Identity drift across shots** | Character description varies between prompts, or identity and motion mixed in one block | Copy-paste exact character description across all prompts; separate Identity Block from Motion Block (see `higgsfield-soul`) |
| **Character swap (two characters)** | @ Elements in action scenes — model confuses which character is which | Use @ Elements only in static/slow scenes; use plain text for action; put hero character first in prompt |
| **Face warping during camera moves** | Identity descriptors mixed with temporal/motion language cause the model to re-interpret the face each frame | Keep identity descriptors (face, clothing, body) in a static Identity Block; keep camera and motion in a separate Motion Block |
| **Wrong expression / frozen face** | No micro-expression direction, or conflicting emotion cues | Use specific micro-expression terms (see `higgsfield-soul`); one emotion per shot |
| **Plastic / waxy skin** | Wrong model for character work, or over-smoothed description | Use Kling 3.0 or Soul Cast for realistic skin; add "natural skin texture, subtle imperfections" |

---

## Texture / Lighting Artifacts

These occur when the model misinterprets visual style or rendering instructions.

| Artifact | Why it happens | Recommended prompt phrasing to prevent it |
|----------|---------------|------------------------------------------|
| **Flickering textures** | Inconsistent style description across frames, or model fighting between two visual styles | Commit to one named style (Cinematic / VHS / Super 8MM / Anamorphic / Abstract); don't mix competing styles |
| **Over-lit / flat lighting** | No lighting specification in prompt — model defaults to even, generic lighting | Always specify lighting source and quality: "single side-light", "golden hour", "practical only" |
| **VFX preset looks cartoonish** | Wrong model for the preset type, or style conflicts with the effect | Grounded presets (Explosion, Freezing) → Kling 3.0/2.6; Stylized presets (Animalization, Multiverse) → Wan 2.5; add "photorealistic, physically accurate" |
| **Product shots look cheap** | No surface/background specification, generic lighting | Specify background surface ("raw concrete", "black velvet"), add texture cues ("surface catches light on edges") |
| **Style ignored / generic output** | Style described too vaguely ("make it look cool") or style not named | Use exact named style + specific color grade: "Style: Cinematic. Cold blue shadows, warm amber highlights, high contrast" |
| **Color grade inconsistency** | Different color descriptions across shots in a sequence | Lock color grade in a Moodboard or repeat exact color language in every prompt |

---

## Temporal / Consistency Artifacts

These occur across frames in video or across multiple generations in a sequence.

| Artifact | Why it happens | Recommended prompt phrasing to prevent it |
|----------|---------------|------------------------------------------|
| **Static I2V output (barely moves)** | Prompt re-describes the static image instead of what should animate | Only describe what CHANGES or MOVES; add explicit camera movement and atmospheric motion ("dust floats", "steam rises") |
| **Camera movement not working** | Camera described vaguely instead of using exact preset names | Use exact preset names on their own line: "Camera: Dolly In" — not "the camera slowly moves forward" |
| **Contradictory camera movements** | Multiple conflicting cameras in one prompt (Dolly In + Dolly Out, Crane Up + Crane Down) | One primary camera movement per shot; if you need multiple, generate separate clips and chain them |
| **Scene continuity breaking** | Different character/environment descriptions between shots | Copy-paste character description verbatim; use Reference Anchor in Cinema Studio; lock Moodboard style |
| **Motion preset not visible** | Preset not named exactly, or scene doesn't support the effect contextually | Name preset exactly as listed: "Apply Explosion preset"; place instruction at end of prompt; ensure scene context supports the effect |
| **Lip-sync desync** | Audio > 8s, head motion tokens competing with lip engine, or non-MP3 format | Trim dialogue clips to 3–8s; remove all head/face motion tokens; use MP3 only for Seedance 2.0 (when available); lock camera to static or slow Dolly In |
| **Background music overriding dialogue** | Ambient/music tokens invite the generative audio engine to replace uploaded audio | Add timestamp anchoring: "Audio @Audio1 plays exactly as uploaded from 0s to end"; remove ALL ambient/SFX/music tokens |

---

## Content Filter / Safety Artifacts

These cause generations to be blocked or produce sanitized output.

| Artifact | Why it happens | Recommended prompt phrasing to prevent it |
|----------|---------------|------------------------------------------|
| **Generation blocked (horror/dark content)** | Platform safety filters triggered by explicit content descriptions | Describe atmosphere, not explicit acts: "unsettling", "something is wrong", "dread"; use motion presets for horror effects |
| **Named real person blocked** | Content filter on celebrity / public figure names | Use character descriptions instead of real names; create original characters with Soul Cast |
| **Brand / IP name blocked** | Trademark/copyright filter on brand names | Describe the product by appearance ("a matte black insulated mug, minimal design, no branding") — never use brand names |
| **Weapon / violence filtered** | Explicit weapon or injury language triggers moderation | Describe "tension", "aftermath", or "impact" rather than graphic injury; use motion presets for VFX |

---

## Cinema Studio–Specific Artifacts

These only apply when working in Cinema Studio 2.5.

| Artifact | Why it happens | Recommended prompt phrasing to prevent it |
|----------|---------------|------------------------------------------|
| **Prompt rejected (too long)** | Cinema Studio has a 512-character hard limit; @ Element chips consume ~80–100 hidden chars each | Max 2 @ tags per prompt; keep visible text under ~250 chars with 2 tags, ~350 with 1, ~450 with 0 |
| **@ Elements cause character swap in action** | AI re-processes reference data per @ tag, competing with action choreography | Use @ Elements in Scene 1 to lock characters, then use plain text descriptions in subsequent scenes |
| **3D Mode geometry holes** | Gaussian splatting can't reconstruct fully occluded areas | Use 3D Mode on images with clear depth and minimal occlusion; avoid extreme angles from the original generation |
| **Optical stack mismatch** | Camera/lens/aperture names put in the prompt field instead of the UI dropdowns | Never put optical stack language in the prompt — it belongs in the UI settings only |

---

## Cinema Studio 3.0 Notes

> **No negative prompt support:** Cinema Studio 3.0's generation engine does not support negative prompt syntax. Do not write "no blur", "avoid shaky camera", or any negation-based constraints. Instead, use positive alternatives:

| Negative (don't use with 3.0) | Positive alternative |
|-------------------------------|---------------------|
| "no shaky camera" | "locked-off static camera, no movement" |
| "no blur" | "sharp focus throughout, deep depth of field" |
| "don't make it dark" | "bright, evenly lit, overcast daylight" |
| "avoid jittery motion" | "smooth, fluid motion, one action per shot" |
| "no extra limbs" | "anatomically correct, all limbs naturally positioned" |
| "don't change the character" | "consistent character appearance, same outfit and features throughout" |

> **Prevention phrasing for 3.0:** All the prevention phrases in the tables above still work with Cinema Studio 3.0 — they are written as positive constraints by design. The key difference is that Cinema Studio 3.0 requires ALL constraints to be positive. The constraint blocks in this file are already compatible.

---

## How to Use This File

When building a prompt, scan the categories above that match the prompt's content:

1. **Character-focused prompt** → check Face/Identity + Body/Motion
2. **Action/chase prompt** → check Body/Motion + Temporal/Consistency
3. **Horror/dark prompt** → check Content Filter/Safety + Face/Identity
4. **Product/commercial prompt** → check Texture/Lighting
5. **Multi-shot sequence** → check Temporal/Consistency + Face/Identity
6. **Cinema Studio prompt** → check Cinema Studio–Specific + all relevant categories
6b. **Cinema Studio 3.0 prompt** → check Cinema Studio 3.0 Notes + all relevant categories (use positive alternatives only)
7. **Audio/dialogue prompt** → check Temporal/Consistency (lip-sync section)

Append the relevant prevention phrases to your prompt, or use them to catch and fix issues before the user generates.
