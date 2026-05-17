# Template: Speech Bubble Text Overlay

Paste-ready Seedance text-overlay template for speech bubbles —
character-attributed dialogue text rendered inside the frame next to
the speaking character. Use for comic-style scenes, social-media
clip dialogue, animated explainers.

## Prompt template

```
Character A says, "[SHORT DIALOGUE]". A clean speech bubble appears
near Character A's head, positioned in the upper-left area, with
simple readable text and no complex symbols.
```

## Field fills

- **`Character A`** — replace with the actual character handle
  (`@Image1`, Soul ID name, or "the woman in the red jacket" if
  un-referenced).
- **`[SHORT DIALOGUE]`** — keep under ~8 words. Longer dialogue
  overflows the bubble or shrinks the text below readability.
- **Bubble position** — `upper-left area` is the default; swap to
  `upper-right` if the character is screen-left and the bubble would
  cross over their face. Avoid bubbles that overlap the speaking
  character's face.

## Why "no complex symbols"

Seedance's text renderer handles letters and basic punctuation
reliably. Symbols (em-dash, curly quotes, asterisks, emoji) often
render as garbled glyphs or get dropped. Keep dialogue text plain.

## See also

- `slogan.md` (sibling template) — for display text without character
  attribution
- `subtitle.md` (sibling template) — for spoken-line text synchronized
  to dialogue audio
