# Template: Subtitle Text Overlay

Paste-ready Seedance text-overlay template for subtitles — spoken-line
text synchronized to dialogue audio. Use for foreign-language scenes,
accessibility subtitles, dialogue-prominent moments.

## Prompt template

```
Display clean subtitles at the bottom-center of the frame. The
subtitle text reads: "[TEXT]". The subtitles are synchronized with
the spoken line, using simple white sans-serif text with a subtle
black shadow for readability.
```

## Field fills

- **`[TEXT]`** — the spoken line, verbatim. One subtitle per line of
  dialogue; multi-line dialogue uses multiple subtitle prompts cut by
  timestamp.

## Why these defaults

- **Bottom-center** is the convention viewers parse fastest.
- **White sans-serif with black shadow** is the readability default
  for video subtitles across lighting conditions — light backgrounds
  read against the shadow; dark backgrounds read against the white.
- **Synchronized to the spoken line** matches the timing the user
  expects; offset subtitles read as a different speaker.

Customize only when the scene's design system requires it (period
piece with handwritten subtitle style; on-screen text already at
bottom-center forcing the subtitle to upper-third; etc.).

## See also

- `slogan.md` (sibling template) — for display text without dialogue
- `speech-bubble.md` (sibling template) — for character-attributed
  dialogue text inside the frame
