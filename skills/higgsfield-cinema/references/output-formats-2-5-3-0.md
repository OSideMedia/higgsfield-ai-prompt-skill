# Cinema Studio 2.5 + 3.0 — Per-Mode Output Templates

Companion reference for `../SKILL.md` § Cinema Studio Output Format. Moved out of the
SKILL.md body verbatim in v3.36.0 so the main file stays readable end-to-end in one
pass. The core rule (everything selectable in the UI stays out of the prompt) and the
What-goes-where table stay in `../SKILL.md`; Cinema Studio 3.5 uses the Per-Shot
Settings Strip and 4.0 its own delivery shape, both in `../SKILL.md`.

## Cinema Studio 2.5 Output Formats

### IMAGE MODE Output Format (Cinema Studio 2.5 only)

```
━━━ UI SETTINGS (select in Higgsfield) ━━━━━━━━━━━━━━━━━━
Camera:   [body name]
Lens:     [lens name]
Focal:    [focal length]
Aperture: [aperture]
↳ Why: [one sentence — what this stack gives the image and why]

━━━ PROMPT (paste into Cinema Studio) ━━━━━━━━━━━━━━━━━━━
[Scene description only. No camera/lens/aperture language.]
```

**Image Mode example:**
```
━━━ UI SETTINGS (select in Higgsfield) ━━━━━━━━━━━━━━━━━━
Camera:   Grand Format 70mm Film
Lens:     Classic Anamorphic
Focal:    50mm
Aperture: f/1.4
↳ Why: 70mm grain + anamorphic flare gives instant prestige cinema quality.
       f/1.4 puts the harbour out of focus, keeping all weight on the detective.

━━━ PROMPT (paste into Cinema Studio) ━━━━━━━━━━━━━━━━━━━
A weathered detective stands at the edge of a rain-soaked harbour dock at night.
An old leather briefcase sits at his feet, open, papers scattered by the wind.
He stares at the horizon, collar turned up against the driving rain.
Harbour lights fracture on the black water below.
```

---

### SINGLE SHOT Video Output Format (Cinema Studio 2.5)

```
━━━ UI SETTINGS (select in Higgsfield) ━━━━━━━━━━━━━━━━━━
Genre:      [genre]
Movement:   [Director Panel movement]
Speed Ramp: [mode]
Duration:   [seconds]

━━━ PROMPT (paste into Cinema Studio) ━━━━━━━━━━━━━━━━━━━
[Scene description only. No movement, genre, speed ramp, or duration language.]
```

**Single Shot example:**
```
━━━ UI SETTINGS (select in Higgsfield) ━━━━━━━━━━━━━━━━━━
Genre:      Suspense
Movement:   Dolly Out
Speed Ramp: Slow Mo
Duration:   8s

━━━ PROMPT (paste into Cinema Studio) ━━━━━━━━━━━━━━━━━━━
A weathered detective stands at the edge of a rain-soaked harbour dock at night.
An old leather briefcase sits at his feet, open, papers scattered by the wind.
He stares at the horizon, collar turned up against the driving rain.
Harbour lights fracture on the black water below.
He reaches down and slowly closes the briefcase.
```

---

### MULTI-SHOT AUTO Video Output Format (Cinema Studio 2.5)

Same structure as Single Shot — one UI settings block, one prompt. The user describes
the full scene in the prompt and Cinema Studio breaks it into shots automatically.

```
━━━ UI SETTINGS (select in Higgsfield) ━━━━━━━━━━━━━━━━━━
Genre:      [genre]
Movement:   [Director Panel movement — or Auto if varied]
Speed Ramp: [mode]
Duration:   [total seconds]

━━━ PROMPT (paste into Cinema Studio) ━━━━━━━━━━━━━━━━━━━
[Full scene description. Let Cinema Studio break it into shots.
No movement, genre, speed ramp, or duration language in here.]
```

**Multi-Shot Auto example:**
```
━━━ UI SETTINGS (select in Higgsfield) ━━━━━━━━━━━━━━━━━━
Genre:      Suspense
Movement:   Auto
Speed Ramp: Linear
Duration:   15s

━━━ PROMPT (paste into Cinema Studio) ━━━━━━━━━━━━━━━━━━━
A weathered detective pushes open the door of a rain-soaked bar and steps inside.
He scans the room — empty except for a bartender polishing glasses at the far end.
He walks slowly to the bar and sits down. The bartender slides a drink without a word.
The detective picks it up, stares at his reflection in the mirror behind the bottles.
He sets it down without drinking.
```

---

### MULTI-SHOT MANUAL Video Output Format (Cinema Studio 2.5)

One UI settings block per scene. One prompt per scene. Six scenes = six pairs.
Each scene is fully self-contained — the user configures and pastes them one at a time.

```
━━━ SCENE 1 — [short scene title] ━━━━━━━━━━━━━━━━━━━━━━━
UI SETTINGS
  Genre:      [genre]
  Movement:   [movement]
  Speed Ramp: [mode]
  Duration:   [seconds]

PROMPT
[Scene 1 description only.]

━━━ SCENE 2 — [short scene title] ━━━━━━━━━━━━━━━━━━━━━━━
UI SETTINGS
  Genre:      [genre]
  Movement:   [movement]
  Speed Ramp: [mode]
  Duration:   [seconds]

PROMPT
[Scene 2 description only.]

[...continue for each scene]
```

**Multi-Shot Manual example — 3 scenes (same pattern scales to 6):**

```
━━━ SCENE 1 — Arrival ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UI SETTINGS
  Genre:      Suspense
  Movement:   Handheld
  Speed Ramp: Linear
  Duration:   5s

PROMPT
A weathered detective steps through the door of a dimly lit bar.
Rain drips from his coat. He pauses, eyes adjusting to the dark.
The bar is nearly empty. A jukebox plays quietly in the corner.

━━━ SCENE 2 — The Walk ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UI SETTINGS
  Genre:      Suspense
  Movement:   Camera Follows
  Speed Ramp: Linear
  Duration:   4s

PROMPT
He walks slowly down the length of the bar, boots on wet floorboards.
A bartender watches without expression. One other patron doesn't look up.
He reaches the end stool and sits down deliberately.

━━━ SCENE 3 — The Mirror ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UI SETTINGS
  Genre:      Suspense
  Movement:   Dolly In
  Speed Ramp: Slow Mo
  Duration:   6s

PROMPT
A glass of whiskey sits untouched on the bar in front of him.
He stares at his own reflection in the mirror behind the bottles.
His jaw tightens. He picks up the glass, holds it, sets it back down.
```

---

## Cinema Studio 3.0 Output Formats

**3.0 does NOT have:** Camera body, Lens, Focal length, Aperture, Color grading, 3D Mode, Grid generation. Never include these in 3.0 output.

**3.0 has:** Genre (7: General, Action, Horror, Comedy, Noir, Drama, Epic), Director Panel, Speed Ramp (7: Auto, Slow-mo, Ramp Up, Flash In, Flash Out, Bullet Time, Hero Moment), Duration (up to 15s), Audio (On/Off native stereo), Smart shot control, 21:9 ultrawide.

**Version guard — values that do NOT exist in 3.0 (never output these):**
- Speed Ramp: ~~Linear~~, ~~Slow Mo~~, ~~Speed Up~~, ~~Impact~~, ~~Custom~~
- Genre: ~~Western~~, ~~Suspense~~, ~~Intimate~~, ~~Spectacle~~
- UI fields: ~~Camera body~~, ~~Lens~~, ~~Focal length~~, ~~Aperture~~, ~~Color grading~~, ~~3D Mode~~, ~~Grid generation~~

---

### IMAGE MODE Output Format (Cinema Studio 3.0)

No optical stack in 3.0. Image output uses Soul Cast modes only.

```
━━━ UI SETTINGS (select in Higgsfield) ━━━━━━━━━━━━━━━━━━
Soul Cast Mode: [General / Character / Location]
Genre:          [genre]
↳ Why: [one sentence — what this combination gives the image and why]

━━━ PROMPT (paste into Cinema Studio) ━━━━━━━━━━━━━━━━━━━
[Scene description only. No camera/lens/aperture language — these don't exist in 3.0.]
```

---

### SINGLE SHOT / SMART Video Output Format (Cinema Studio 3.0)

```
━━━ UI SETTINGS (select in Higgsfield) ━━━━━━━━━━━━━━━━━━
Genre:      [genre — General, Action, Horror, Comedy, Noir, Drama, or Epic]
Shot Mode:  [Smart / Custom]
Movement:   [Director Panel movement — or Smart for auto camera planning]
Speed Ramp: [Auto / Slow-mo / Ramp Up / Flash In / Flash Out / Bullet Time / Hero Moment]
Duration:   [up to 15s]
Audio:      [On / Off]

━━━ PROMPT (paste into Cinema Studio) ━━━━━━━━━━━━━━━━━━━
[Scene description only. Use @ to reference uploaded images/video/audio.
No movement, genre, speed ramp, or duration language in here.]
```

**Single Shot 3.0 example:**
```
━━━ UI SETTINGS (select in Higgsfield) ━━━━━━━━━━━━━━━━━━
Genre:      Action
Shot Mode:  Smart
Movement:   Jib Down
Speed Ramp: Slow-mo
Duration:   5s
Audio:      On

━━━ PROMPT (paste into Cinema Studio) ━━━━━━━━━━━━━━━━━━━
@CypressLookout packed with cars and people at night. @R34GTR parked
prominently in the center, @240SX and @AE86 visible nearby. Crowd
gathered between the cars, neon underglow reflecting on wet pavement.
City skyline glowing across the water in the distance. Engine noise,
crowd murmur, tension in the air.
```

---

### MULTI-SHOT MANUAL Video Output Format (Cinema Studio 3.0)

Same per-scene structure as 2.5 but with 3.0 options. Up to 6 scenes, 15s max total.

```
━━━ SCENE 1 — [short scene title] ━━━━━━━━━━━━━━━━━━━━━━━
UI SETTINGS
  Genre:      [genre]
  Movement:   [movement]
  Speed Ramp: [Auto / Slow-mo / Ramp Up / Flash In / Flash Out / Bullet Time / Hero Moment]
  Duration:   [seconds]
  Audio:      [On / Off]

PROMPT
[Scene 1 description only. Use @ for references.]
```
