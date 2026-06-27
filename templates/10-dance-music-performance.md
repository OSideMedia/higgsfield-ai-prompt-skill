# Template: Dance / Music Performance

## Genre/Use-Case
Dance sequences, music video scenes, concert performances, choreography showcases, and any prompt where physical performance and rhythm are the primary energy.

## When to use this template
User asks for dance video, music performance, choreography, concert scene, DJ set, or any prompt where the body in motion is the hero subject.

## Recommended model
**Minimax Hailuo 2.3** for best fluid body motion and dance. **Kling 3.0** for character-focused performance with audio. **Sora 2** for large-scale concert/crowd scenes.

## Example prompt

```
Model: Minimax Hailuo 2.3
Aspect: 16:9 | Duration: 10s | Style: Cinematic

A dancer in a white flowing dress performs alone in a vast black studio.
A single overhead spotlight. She moves through contemporary choreography —
slow arms, sudden explosive turns, floor work.
Camera: 360 Orbit tightening toward her as movement intensifies.
Overhead shot as she collapses to the floor in the final beat.
Style: Cinematic. Pure black and white contrast. 16:9.
Apply Glow Trace preset — her movement leaves a trail of white light.
```

## Annotation

| Prompt element | Why it works |
|---------------|-------------|
| "white flowing dress" | High-contrast clothing against black studio = maximum visual drama |
| "vast black studio" | Negative space isolates the performer — all attention on the body |
| "single overhead spotlight" | One light source creates dramatic shadows and rim lighting |
| "slow arms, sudden explosive turns, floor work" | Describes the dynamics of the dance — not specific moves |
| "Camera: 360 Orbit tightening" | Orbit + zoom builds energy — starts wide, ends close as dance peaks |
| "as movement intensifies" | Ties camera to performance energy — they escalate together |
| "Overhead shot as she collapses to the floor" | Camera shift marks the climax — top-down for the final beat |
| "Pure black and white contrast" | Removes color distraction — pure form and movement |
| "Apply Glow Trace preset" | Visual effect that extends the movement — trails of light behind her arms |

## Negative constraints to include
- **Body/Motion**: Describe energy and dynamics ("slow arms, explosive turns"), not specific named dance moves. The model can't execute "fouetté en tournant."
- **Temporal/Consistency**: One camera movement that tracks the dance energy. Don't switch cameras mid-flow.
- **Texture/Lighting**: Commit to one lighting setup. Strobing/color changes mid-clip confuse the model.

## Common mistakes
1. **Named dance moves** — "pirouette, plié, grand jeté" don't translate reliably. Describe the energy and body positions instead.
2. **Too many dancers for one generation** — one or two performers max per clip. Crowds → use Minimax Hailuo 2.3 with a wider shot.

## Variations
- **Hip-hop/street**: 9:16 vertical, Rap Flex camera (quick zooms), "sharp isolated movements", neon lighting
- **Concert/live performance**: Sora 2, wide shot, "stage lighting sweeping the crowd", Apply Live Concert preset
- **Slow/emotional dance**: Dolly In instead of Orbit, "minimal movement, arms reaching", Cinematic + shallow DOF
- **Music video energy**: Crash Zoom In on beat drops, Apply Color Rain preset, fast cuts (separate generations per beat)

### Identity Block (if using Soul ID)
```
The Soul ID character — athletic build, braided hair pulled back tight,
barefoot, wearing a white flowing contemporary dance costume.
```

### Motion Block
```
She moves through contemporary choreography — slow arms,
sudden explosive turns, floor work. Energy builds.
Camera: 360 Orbit tightening toward her.
Overhead shot as she collapses to the floor.
Apply Glow Trace preset.
```

## Beat-by-beat choreography (Seedance 2.0)

The "describe energy, not named moves" rule above (no `pirouette`, no `grand
jeté` — the model can't execute jargon) has a **Seedance-specific upgrade**:
between vague energy ("he dances") and untranslatable jargon sits the sweet
spot — **spell the move out beat by beat in plain, observable physical terms**.
"He dances" means nothing to Seedance; a named ballet step means nothing either;
but a concrete sequence of body actions renders:

```
first two crisp head nods, chin dipping on each beat; then his shoulders roll
back one at a time — right, then left; he steps off on his right foot with a
soft knee-dip and drags the left foot in to meet it with a small heel-bounce,
hips swaying side to side; halfway across he throws a loose finger-snap;
finishes with a light quarter-spin on the ball of his foot.
```

This is the dance case of `../skills/higgsfield-seedance/SKILL.md` § Voice
Rewrite (describe physics, not labels). Keep each move observable (which foot,
which direction, what the hands do) — not interpretive ("grooves", "vibes").

## `@music_track` drives the motion

When the choreography must lock to a specific track, upload it as `@music_track`
(an audio reference) and write the movement so it **responds to the beat** — the
audio is a conditioning input that the model maps to visual rhythm, not just a
soundtrack:

```
@music_track as the rhythmic foundation — the dancer's movement locks to its
beat throughout. Steps land on the downbeats, the spin releases on the drop.
```

Full beat-sync mechanics (the 3-sentence mapping, the first-15s extraction trap,
combining with `@Image`/`@Video` references): `../skills/higgsfield-audio/SKILL.md`
§ Audio as a Conditioning Input. Keep the prompt body diegetic-only and layer the
final music in post.

## Cinema Studio 3.0 (Business/Team Plan)

**Genre mapping:** Action (for high-energy) or Drama (for emotional performance)
**Prompt length target:** 50–80 words (Music Video — lead with Style)
**Speed Ramp:** Bullet Time for freeze moments, Ramp Up for drops

**@reference workflow:**
```
Reference @Video1 for dance choreography.
@Image1 as the dancer. She performs on a rooftop at sunset,
city skyline behind her. Wind catches her dress on each spin.
Camera: 360 orbit. Style: anamorphic flares, crushed blacks.
Audio: heavy bass drop, rhythmic percussion, wind through fabric.
```
