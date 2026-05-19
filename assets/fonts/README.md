# Bundled fonts — DejaVu Sans Condensed

Three TTFs ship with this repository to support Unicode rendering in
`generate_user_guide.py`:

| File                                | Style   | Size  |
|-------------------------------------|---------|-------|
| `DejaVuSansCondensed.ttf`           | regular | 665 KB |
| `DejaVuSansCondensed-Bold.ttf`      | bold    | 650 KB |
| `DejaVuSansCondensed-Oblique.ttf`   | italic  | 586 KB |

Total: ~1.9 MB.

## Why bundled

FPDF's default `helvetica` family is latin-1 only. Up through v3.7.13,
any non-ASCII glyph in `SUB_SKILL_DESCRIPTIONS` or PDF body text would
crash `build_pdf()` with `FPDFUnicodeEncodingException`. v3.7.13 caught
this exactly: an em-dash in the new `higgsfield-marketing-studio` dict
entry crashed the rendering pipeline at L1204. The workaround at the
time — "keep dict entries ASCII-only" — preserved release momentum but
left the underlying constraint in place.

v3.7.14 replaces the latin-1 core font with DejaVu Sans Condensed (DVC),
a Unicode TTF that covers em-dash, en-dash, curly quotes, ellipsis, and
the broader BMP glyph range. The constraint lifts; future dict entries
and body text can use natural punctuation.

## Why Condensed, not regular DejaVu Sans

Phase 0 verification for v3.7.14 measured glyph width drift against
Helvetica at the body 9pt + 10pt sizes used by `build_pdf()`. DejaVu
Sans **regular** runs 11-18% wider than Helvetica — wide enough that
one existing `SUB_SKILL_DESCRIPTIONS` entry (`higgsfield-cinema` at
71 chars, the empirical column ceiling) overflowed the 115mm Section
24 column. The user-stated descope threshold ("if column-width drift
exceeds ~5%, flag for descope") fired.

DejaVu Sans **Condensed** keeps drift at 0.6-2.8% on real text content
(6.4% on a synthetic 71×'x' worst case). Zero existing entries
overflow; the 71-char ceiling in `validate_user_guide.py` stays valid.
Same Unicode coverage as DV regular; close-to-Helvetica metrics.

Full measurement trail: `../../.planning/v3.7.14/PHASE-0-VERIFICATION.md`.

## Why bundled in-repo, not system-installed

DVC isn't installed on every developer machine by default (macOS ships
no DejaVu fonts; Linux is variable). Bundling guarantees deterministic
PDF regeneration across environments — anyone with a checkout of this
repository can run `python3 generate_user_guide.py` and get the same
glyph rendering. Removes a hidden system dependency that would
otherwise surface as cryptic FPDF errors on first regen.

## Source

DejaVu Fonts v2.37, official GitHub release tarball:
<https://github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/dejavu-fonts-ttf-2.37.tar.bz2>

Project home: <https://dejavu-fonts.github.io/>

## License

DejaVu Fonts are released under the Bitstream Vera Fonts Copyright
license plus the Arev Fonts Copyright additions, with derivative work
under the same terms. **Redistribution is permitted** including
embedding in PDFs and shipping inside Git repositories. License text
ships with the upstream tarball; full reference at
<https://dejavu-fonts.github.io/License.html>.

## When to update

Re-bundle when:

- DejaVu Fonts ships a newer stable release that fixes a glyph or
  rendering issue affecting USER-GUIDE.pdf
- `generate_user_guide.py` adds a font weight or style not currently
  bundled (e.g., a `BI` bold-italic combination — none used today)

The current convention uses three styles (regular, bold, oblique).
`set_font("Body", "BI", ...)` would require an additional
`DejaVuSansCondensed-BoldOblique.ttf` bundled here.

When updating: download new tarball, replace the three TTFs, update
the version reference in this README, and regenerate USER-GUIDE.pdf
to confirm glyph metrics haven't shifted (validator Layer 1 will
catch material drift).
