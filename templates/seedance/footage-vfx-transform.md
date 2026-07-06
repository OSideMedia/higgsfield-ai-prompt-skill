# Template: Footage VFX Transform (Seedance 2.0, video-to-video)

Paste-ready scaffolding for transforming a clip the user **already shot** — preserve the
real subject + camera move, change only the named element. Pairs with
`../../skills/higgsfield-seedance-vfx/SKILL.md`; that skill carries the rules, this file carries
the fill-in skeleton and four worked patterns.

Derived from the Higgsfield "Seedance 2.0 in 4K" VFX walkthrough
(`higgsfield.ai/blog/vfx_4k`, tutorial `youtube.com/watch?v=Yte-UGhYkPQ`) — the source the
`higgsfield-seedance-vfx` skill is built from.

## When to use this template

The user attaches a real clip (or describes one) and wants a Seedance prompt that keeps
*them* and their camera move while swapping the world, adding a VFX element, dropping in a
creature, or syncing a timed camera move to a line. For a scene built from scratch, use
`../../skills/higgsfield-seedance/SKILL.md` instead.

Always run these in **Seedance 2.0, `mode=std`, 4K** (native 4K needs std; fast caps at
720p; Cinema Studio caps at 1080p).

---

## The skeleton

Output plain-text English, no markdown inside the prompt, easy to copy:

```text
@source: Original <clip> — <subject, wardrobe, setting, action>. Preserve identity, face,
wardrobe, performance, framing, lens, camera and motion exactly; <the one change>.
@creature: Reference photo of a real <animal/material> — <texture/anatomy notes>. Appearance
and texture reference only; ignore its background and lighting.   (only if a texture ref is used)

Photoreal. 16:9. <N>s. 4K. <look/grade>. NON-IP — generic <X>. SFX [and source dialogue] only.

<Continuous shot, same framing as source. Preserved performance. The transformation, with its
physics and how it interacts with the plate (light spill, contact shadow, refraction, parallax).
Any timed camera move with a semantic + numeric anchor. Lock-down clause: face and identity
unchanged; everything else identical to the source.>

SFX [and source dialogue] only: <specific, ordered sounds synced to the visible action>.
```

Fill order: inspect the clip → set `@source` and the runtime from what the frames actually
show → name the one change → lock everything else → close with the lock-down clause.

---

## Pattern 1 — Environment swap (moving camera)

Keep the subject and the real camera move; replace the world so it streams past with matching
parallax and relights the subject.

```text
@source: Original clip — man walking toward camera in a plaza, handheld follow. Preserve his
identity, face, walk, gestures, wardrobe and the exact handheld camera move; change only the
world around him.

Photoreal. 16:9. 6s. 4K. Warm directional late-afternoon grade. NON-IP. SFX only.

Same handheld follow and framing as the source, same walk. On his finger snap at about 2s,
transform only the environment around him into open desert at sunset — dunes and heat haze
streaming past with parallax that matches his forward motion. Keep the sun as the key from
screen-left exactly as before so his face and the light on him barely change; let a warm
bounce off the sand lift his under-jaw shadow. Face and identity unchanged; walk, wardrobe,
framing and camera move identical to the source; only the world is replaced.

SFX only: footsteps on sand, a low desert wind rising after the snap.
```

## Pattern 2 — Add an element in-frame (head on fire)

Layer an effect onto the plate; make it spill light back onto the subject; keep the
performance oblivious.

```text
@source: Original clip — man talking to camera in a parked car, golden-hour light. Preserve
his face, expression, lip movement, the car interior and the golden-hour light; add only fire
to his hair.

Photoreal. 16:9. 5s. 4K. Golden-hour grade. NON-IP. SFX only.

Same static framing as the source, same delivery to camera. His whole head of curls catches
fire — a soft whoomph as it ignites, then a low steady flame roar, individual strands
burning, occasional ember pop — while he keeps talking, unfazed. The orange firelight
flickers on his face and spills onto his shirt and the car's paint, matched to the sunset.
Face, identity and performance unchanged; only the fire is added.

SFX only: a soft whoomph on ignition, then steady flame roar and crackle with occasional
ember pops.
```

## Pattern 3 — Creature on/behind subject with a reveal pull-back

Open tight on the added creature in isolation, then pull back to a 100%-match of the source
framing with correct lip-sync.

```text
@source: Original clip — man talking to camera on a sidewalk, building rising behind him,
handheld. Preserve his identity, face, performance, lip-sync and the handheld move; add giant
lizards climbing the building, and prepend a tight reveal.
@creature: Reference photo of a real monitor lizard — pebbled scaly skin, long claws, heavy
tail, true reptile anatomy. Texture and anatomy reference only; ignore its background.

Photoreal. 16:9. 8s. 4K. Overcast daylight grade. NON-IP — generic large monitor lizards. SFX
and source dialogue only.

Open tight and telephoto on dozens of car-sized photoreal lizards swarming up the building en
masse — claws hooking window ledges and concrete, heavy tails dragging, pebbled scales matte
and mud-caked, catching the low sun, never smooth or rubbery. At about 2s the camera smoothly
pulls back to a 100% match of the source composition — same angle, headroom, horizon and lens
— landing on the man mid-sentence, his lips matching the source exactly saying: "definitely
should not be there." The handheld move then runs exactly as the source while the lizards keep
climbing behind him, lit to the same overcast daylight with real soft-edged contact shadows on
the wall. Face, identity, performance and lip-sync unchanged.

SFX and source dialogue only: claws scraping concrete, heavy scaled bodies shifting, his line
landing on the reveal.
```

## Pattern 4 — Full handheld cinematic (creature integration)

Hardest case: the camera is moving the whole time, so the effect has to track angle, parallax
and shake without falling apart.

```text
@source: Original clip — man turning and reacting, fully handheld, forest clearing. Preserve
his identity, face, reaction, wardrobe and the full handheld move frame-for-frame; replace the
setting with a rainy forest and add three giant long-necked dinosaurs behind him.

Photoreal. 16:9. 10s. 4K. Overcast rainy grade, atmospheric haze. NON-IP — generic
long-necked sauropods. SFX only.

Same handheld follow, framing, shot scale, lens, pan, tilt, speed and shake as the source —
do not re-frame, re-time, re-angle or re-cut. Three enormous photoreal sauropods tower behind
him in a rainy forest, their massive bodies dwarfing the trees, skin deeply wrinkled, cracked
and asymmetric, moving with slow heavy weight; at about 2–3s, exactly as the man turns and
looks back, one sauropod steps in closer. Veil them partly behind foreground trees with a
telephoto compression and shallow depth of field, motion blur and handheld softness matching
the plate; same overcast key and color temperature as on him, real soft-edged contact shadows,
the same rain and haze over him as the far background. Face, identity and reaction unchanged;
camera move identical to the source.

SFX only: rain on leaves, deep low sauropod calls, heavy footfalls landing on the closer step.
```

---

## Reminders

- **Match the source runtime** by default; recompute any numeric zoom mark if you change it.
- **Prepended intro?** `total − intro = surviving window` for the source performance — flag
  what falls off before promising lip-sync (`../../skills/higgsfield-seedance-vfx/SKILL.md`
  § Duration discipline).
- **Creature still reads CG?** Add a real reference photo as `@creature` (texture only), or
  generate the transformed start frame first (`../../skills/higgsfield-seedance-vfx/references/first-frame.md`).
- **Preflight** the finished prompt through the parent linter:
  `python3 scripts/seedance_lint.py --preflight --model seedance_2_0 "<prompt>"`.
