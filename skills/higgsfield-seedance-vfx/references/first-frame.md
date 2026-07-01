# Reference — First / start-frame workflow

Video credits are the expensive part of a footage transform. When the *look* is uncertain —
a new creature, an unfamiliar relight, an environment you haven't tried — lock it as a **still
first**, then animate from that still. You approve a single image cheaply, then hand it to
Seedance as the start frame so the video inherits the look instead of re-rolling it. Referenced
from [`../SKILL.md`](../SKILL.md) § First / start-frame workflow.

## When to do it

- The transform introduces something the model tends to get wrong on the first video roll — a
  photoreal creature, a full relight, a "looks pasted in" integration risk.
- You want to iterate on the *look* (softer light, bigger creature, different grade) without
  paying for a video each time.
- Skip it for simple, low-risk transforms (a background swap on a steady daylight shot) — go
  straight to video.

## Procedure

1. **Extract the source opening frame.** Pull the first frame (or the frame the transform should
   start on) from the user's clip. This is the plate you're transforming.
2. **Generate the transformed still.** Use an image model that takes the source frame plus any
   reference as input:
   - `../../higgsfield-gpt-image-2/SKILL.md` (GPT Image 2) or Nano Banana Pro — good at holding a
     real face while adding an element or swapping the world around it.
   - Prompt it with the *same* preserve/change split as the video prompt: lock identity, face,
     wardrobe, framing; apply only the one change. Attach the `@creature`/texture reference here
     too if the video will use one — the still and the video should agree on the look.
3. **Iterate on the image, not the video.** Refine the chosen still (softer light, bigger
   creature, matched grade) by passing the result back as the base and fixing only what's off.
   Cheap loop; converge here.
4. **Hand the still back to Seedance as `start_image`.** Upload the approved still and declare it
   as the start frame. `start_image` is a verified `seedance_2_0` media role
   (`../../specs/model-specs.json`). The video prompt then describes **motion + camera only** from
   that frame — do not re-describe what the still already shows, or you give the model two
   competing inputs for one subject (the I2V subject-drift trap; see
   `../../higgsfield-seedance/SKILL.md`).

## Upload mechanics

- In an Apps-UI client, local media goes through the Higgsfield **media upload widget** — the
  remote tools can't read a chat attachment. Upload the source frame / reference / approved still
  through the widget, then reference them by their assigned handles.
- Reference handles are assigned by upload order (`@Image1`, `@Image2`, …). Keep a stable
  role-per-slot convention across the still and the video prompt so the model knows which
  reference carries which property (see `../../higgsfield-seedance/SKILL.md` § Reference Roles /
  Per-Image Role Convention).

## Why pin the frame, not the roll

Seedance 2.0 exposes **no seed parameter**, so re-running an approved draft is a fresh roll — a
new performance, new camera micro-trajectory, new timing. The durable way to carry an approved
*look* into the final render is to pin the **start frame**, not to "approve cheap, re-render at
quality." Full treatment: `../../higgsfield-seedance/SKILL.md` § Drafts Validate the Prompt, Not
the Take.
