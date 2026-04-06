---
name: higgsfield-vibe-motion
description: >
  Use when the user asks about Vibe Motion, motion graphics, kinetic typography,
  animated text, brand animations, logo animations, infographic animation,
  presentation animation, data-driven video, or prompt-to-motion-graphic workflows.
  Vibe Motion is fundamentally different from video generation — it creates
  deterministic code-based motion graphics, not AI-predicted pixel sequences.
user-invocable: true
metadata:
  tags: [higgsfield, vibe-motion, motion-graphics, typography, brand, animation, code, Remotion]
  version: 3.0.0
  updated: 2026-04-06
  parent: higgsfield
---

# Higgsfield Vibe Motion

## What Vibe Motion Actually Is (And How It Differs from Video Generation)

This is the most important thing to understand about Vibe Motion:

| Standard AI Video Generation | Vibe Motion |
|------------------------------|------------|
| Predicts pixel sequences | Generates Remotion code |
| Text can hallucinate or distort | Text is always crisp (it's code) |
| Each change = full re-render | Real-time edits on live canvas |
| Physics is emergent/unpredictable | Physics is a slider you control |
| Output: video file | Output: motion graphic + deployable code |
| Good for: cinematic scenes | Good for: brand, typography, data, structure |

**Vibe Motion is powered by Claude (Anthropic) and Remotion** — the open-source
React framework for programmatic video. It generates actual code that renders
deterministically, meaning the same prompt always produces the same output.
Text never breaks. Colors stay exact. Brand consistency is guaranteed.

**Location:** higgsfield.ai/vibe-motion

---

## What Vibe Motion Is Built For

Use Vibe Motion when your content is about **structure, timing, and information**
rather than cinematic storytelling.

✅ **Perfect use cases:**
- Kinetic typography and text animations
- Logo animations and brand intros/outros
- Product feature explainer animations
- Infographic animations and data visualization
- Presentation slide animations
- Social media motion graphics (lower thirds, title cards, CTAs)
- App demo animations
- Countdown timers, score boards, data dashboards
- Launch campaign motion assets

❌ **Wrong tool for:**
- Cinematic scenes with characters (use Kling/Sora/Cinema Studio)
- Photorealistic video (use standard video generation)
- Nature/environment footage (use Veo 3)
- Anything requiring actor performance (use Kling + Lipsync)

---

## The Vibe Motion Workflow

### Step 1: Start in Chat
Describe your motion idea in natural language — as if briefing a motion designer.
Upload any assets you want animated: logo, product image, brand photos, PDFs.

**The AI remembers the full conversation** — you can refine iteratively through
follow-up messages without starting over.

```
Example opening prompts:
"Create a kinetic typography intro for a productivity app called Flowstate.
The tagline is 'Do less. Achieve more.' Brand colors: deep navy and electric lime."

"Animate this logo [upload] with a clean reveal — letters coming in one by one,
finishing with a subtle pulse. Professional, not flashy."

"Build an infographic animation showing our 3 key stats:
42% faster, 10x more leads, $2M saved. Minimal style, white background."
```

---

### Step 2: Choose a Format or Template
Vibe Motion has templates for common formats — start from one to skip setup:

| Template category | Examples |
|-------------------|---------|
| **Text Animation** | Kinetic typography, quote cards, lyric videos |
| **Infographics** | Stat reveals, bar charts, comparison slides |
| **Posters** | Animated poster with text + image |
| **Brand** | Logo animation, brand intro/outro, bumper |
| **Social** | Story animations, Reels titles, YouTube intros |
| **Product** | Feature callouts, spec animations, launch reveals |

**When to use a template:** Always for standard formats. Templates have complex
motion logic already built in — you just replace the content.

**When to start from scratch:** Custom motion systems, unusual layouts, highly
specific brand behavior.

---

### Step 3: Set the Vibe (Color + Energy)

**Color palette presets:** Mosaic · Prism · Candy · Minimal · Dark · Brand (custom)

**Animation Speed slider:** Controls the Physics parameter
- **Slow:** Smooth, luxurious, editorial — good for fashion, premium brand
- **Medium:** Balanced, professional — good for most business content
- **Fast/Sharp:** Energetic, snappy — good for tech, sports, trend content

---

### Step 4: Real-Time Editing Controls

After generation, every element is directly editable:

| Control | What you can change |
|---------|-------------------|
| **Font Family** | Any typeface — click text element to change |
| **Text Color** | Exact color — use hex for brand accuracy |
| **Font Size** | Scale text elements independently |
| **Background Color** | Global or per-element background |
| **Animation Speed** | Global physics slider — dial up or down |

**Iterating with chat:** Any follow-up instruction adjusts the existing animation
without regenerating from scratch:

```
"Make the entrance faster — cut the timing in half"
"Change the headline font to something more geometric"
"The blue is too bright, move it to #1A2B8C"
"Add a subtle particle effect in the background"
"Make it feel more like an Apple keynote"
```

---

## Prompting Patterns for Vibe Motion

### Typography / Text Animation

Structure: `[What text] + [how it enters] + [timing feel] + [style]`

```
"The words 'CLARITY. SPEED. RESULTS.' appear one at a time, each letter
scaling in from small with a sharp snap. Inter font, all caps, white on black.
Each word holds for 0.8 seconds then the next appears. Total: 4 seconds."
```

```
"A single sentence builds word by word from left to right:
'The future of [pause] design [pause] is [pause] here.'
Clean sans-serif, navy blue, minimal white background.
Elegant timing — feels like Apple copy."
```

---

### Logo Animation

Structure: `[Logo behavior] + [reveal style] + [hold duration] + [feel]`

```
"The logo [upload] fades in letterform by letterform, left to right.
Once fully revealed, it pulses once subtly — scale up 3%, back down.
Clean, professional. White background. Total: 2.5 seconds."
```

```
"The icon [upload] draws itself on — like a pen tracing the outline —
then the wordmark slides in from the right. Bold, confident, tech brand feel.
Dark background, logo in white."
```

---

### Infographic / Stats Animation

Structure: `[What data] + [reveal animation] + [visual hierarchy] + [style]`

```
"Three statistics animate in sequence:
1. '10M+' — counter counts up from 0, large number, small label 'users'
2. '99.9%' — percentage fills like a progress arc, label 'uptime'
3. '$4B' — slides in from right, label 'saved annually'
White background, company blue (#0057FF), minimal, each stat holds 1.5s."
```

```
"Animated bar chart comparing our product vs. competitors across 4 metrics.
Bars grow upward on a staggered reveal — ours last, tallest, highlighted.
Clean grid, no clutter. Corporate presentation style."
```

---

### Social Media Motion Graphics

Structure: `[Format + platform] + [content] + [timing] + [style]`

```
"A 9:16 Instagram Story title card.
Headline: 'How We 10X'd Our Revenue in 6 Months'
Subtext fades in below: 'The strategy nobody talks about'
Bottom: '@ourhandle' with subtle slide-up
Warm gradient background — amber to deep orange. 5 seconds total."
```

```
"YouTube intro bumper — 5 seconds.
Channel name 'SIGNAL' appears with a glitch effect — letters scrambling
before snapping into place. Icon [upload] animates in beside it.
Dark background, neon blue accent. Energetic."
```

---

### Product / Feature Animation

```
"Three feature callouts appear in sequence for a project management app:
Feature 1: 'Instant sync' — icon [upload] + text slides in from left
Feature 2: 'AI summaries' — icon [upload] + text slides in from right
Feature 3: 'One-click export' — icon [upload] + text slides in from left
Clean white background, product blue, 1.5s per feature. Total: 6s."
```

---

## Vibe Motion vs Other Higgsfield Tools

| Need | Right tool |
|------|-----------|
| Animated brand logo | Vibe Motion |
| Cinematic scene with actors | Cinema Studio / Kling |
| Talking head with speech | Lipsync Studio |
| Product photo brought to life | I2V (image-to-video) |
| Text-over-video lower third | Vibe Motion (export) + video editor |
| Data visualization that updates | Vibe Motion (code export) |
| Social story with motion text | Vibe Motion |
| Short film scene | Cinema Studio |
| One-click product ad | Click to Ad App |

---

## Combining Vibe Motion with Video Generation

The real power is combining both:

**Pattern 1: Vibe Motion titles + cinematic video body**
```
1. Generate cinematic scene in Kling 2.6 (the video)
2. Create title card and lower thirds in Vibe Motion
3. Combine in editing workflow (DaVinci, Premiere, CapCut)
```

**Pattern 2: Vibe Motion intro + product video**
```
1. Create animated logo intro in Vibe Motion (3–5s)
2. Generate product demo video with Click to Ad or manual prompt
3. Create animated CTA/outro in Vibe Motion
4. Assemble: intro → product video → outro
```

**Pattern 3: Full social ad**
```
1. Vibe Motion: animated hook text (0–2s) — stops the scroll
2. Kling 2.6: product or lifestyle footage (2–8s) — shows the thing
3. Vibe Motion: CTA + offer card (8–12s) — drives the action
```

---

## Technical Notes

**Output:** Video file (.mp4) + Remotion source code
**Max resolution:** 4K
**Text quality:** Pixel-perfect — text is rendered from code, not pixel-predicted
**Aspect ratios:** All standard ratios supported including 9:16, 16:9, 1:1, 4:5
**Editing:** All changes are non-destructive — iterate without starting over
**Code export:** Remotion code can be deployed for data-driven or programmatic use cases
  (auto-generate 10,000 personalized videos from a database, responsive video that
  adapts to different platforms, etc.)

---

## Related skills
- `higgsfield-pipeline` — Vibe Motion as a stage in the full production pipeline
- `higgsfield-cinema` — Cinema Studio for cinematic content (not motion graphics)
- `higgsfield-style` — Visual styles for the video content Vibe Motion overlays
- `higgsfield-apps` — One-click Apps as alternatives for simple motion tasks
