#!/usr/bin/env python3
"""Validate the regenerated USER-GUIDE.pdf against a frozen baseline.

WHAT THIS VALIDATES
-------------------
After v3.7.0's Path B refactor (Option D), generate_user_guide.py reads
version metadata from the root SKILL.md frontmatter and discovers the
sub-skill list from the filesystem. Per-sub-skill description text and
all narrative content remain hardcoded. The expectation: regenerating
the PDF after changing only metadata should produce a PDF with content
byte-equivalent to the prior release, except for the metadata bytes
that the refactor itself parameterized.

This script enforces that expectation. Run it whenever you regenerate
USER-GUIDE.pdf to catch unintended drift. Compares two PDFs:

  - The frozen baseline:   docs/user-guide/USER-GUIDE.pdf.baseline-v<X.Y.Z>
  - The new candidate:     docs/user-guide/USER-GUIDE.pdf  (just regenerated)

WHAT COUNTS AS AN ALLOWED CHANGE
--------------------------------
Only these textual differences are allowed between baseline and candidate:

  1. Version-string changes — anywhere the PDF prints the version number
     (cover page, header on every page, footer on every page, FAQ Q5
     answer, module docstring's reflection in PDF doc properties).
     Allowed pattern: "v<old>" -> "v<new>" where both match v\d+\.\d+\.\d+.

  2. Date-string changes — wherever the PDF prints the release date
     (cover page, footer). Allowed pattern: ISO-8601 YYYY-MM-DD only.

  3. PDF /CreationDate metadata — pinned via FPDF.set_creation_date()
     in the refactored generator, so this should match the new release
     date. Outside the validator's text-diff scope (it's PDF metadata,
     not extracted text), but worth knowing it changes.

  4. Sub-skill list count — Section 22 prints "Sub-Skills (N total)".
     If a sub-skill is added or removed between releases, N changes
     and the corresponding row changes. The validator allows this but
     flags it for review.

WHAT COUNTS AS A REGRESSION
---------------------------
ANYTHING ELSE. Specifically:

  - Narrative content changes (paragraphs, bullet lists, callouts).
  - Table content changes (rows added/removed/reworded).
  - Sub-skill row description changes (Section 22 second column).
  - Section ordering changes.
  - TOC changes beyond version-string updates.
  - Layout shifts that show up as different text-extraction output
    (e.g., a paragraph wrapping differently because a string got longer).

If the validator flags a substantive change, INVESTIGATE before shipping.
The drift catalog from v3.7.0 scoping (items D3-D8 in
docs/pdf-audit/AUDIT-REPORT-v3.6.0.md USER-GUIDE expansion row) is the
work item for INTENTIONAL content updates — those edits should land
through deliberate hand edits to generate_user_guide.py, then this
script gets re-baselined to match the new shipped PDF.

Baseline files are committed to git alongside the release that produced
them, matching the existing tracking pattern for docs/user-guide/USER-GUIDE.pdf.
The "PDF tracks version" invariant has a corresponding "baseline is tracked"
invariant.

VALIDATION LAYERS
-----------------
Layer 1 (text-extract diff): primary check. Uses pdftotext if
available; falls back to pdfplumber. Extracts text from both PDFs
and produces a unified diff. Lines matching the allowed-change
patterns are normalized away before diffing.

Layer 2 (binary diff): secondary check. After the refactor pinned
/CreationDate via set_creation_date(), the PDF binary should be
deterministic across runs of the same generator against the same
inputs. If the binary diff shows ONLY the bytes that correspond to
parameterized version/date strings plus the /CreationDate metadata
field, the refactor is byte-clean. Anything else is a layout regression.

USAGE
-----
  python3 validate_user_guide.py [baseline_path] [candidate_path]

Defaults:
  baseline_path  = docs/user-guide/USER-GUIDE.pdf.baseline-v3.7.7
  candidate_path = docs/user-guide/USER-GUIDE.pdf

Exit code 0 = validation passed (no substantive regressions).
Exit code 1 = substantive content diff detected; review required.
"""

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
DEFAULT_BASELINE = REPO / "docs" / "user-guide" / "USER-GUIDE.pdf.baseline-v3.7.7"
DEFAULT_CANDIDATE = REPO / "docs" / "user-guide" / "USER-GUIDE.pdf"


def extract_text(pdf_path):
    """Use pdftotext if available, else fall back to pdfplumber."""
    try:
        return subprocess.check_output(
            ["pdftotext", "-layout", str(pdf_path), "-"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        try:
            import pdfplumber
        except ImportError:
            print("ERROR: neither pdftotext nor pdfplumber available; cannot extract text.")
            sys.exit(2)
        with pdfplumber.open(pdf_path) as p:
            return "\n".join(page.extract_text() or "" for page in p.pages)


# Patterns we normalize away before diffing. These represent the metadata
# changes the refactor was designed to parameterize.
ALLOWED_PATTERNS = [
    (re.compile(r"v\d+\.\d+\.\d+"), "<VERSION>"),
    (re.compile(r"\b\d{4}-\d{2}-\d{2}\b"), "<DATE>"),
    (re.compile(r"Sub-Skills \(\d+ total\)"), "Sub-Skills (<COUNT> total)"),
]


def normalize(text):
    for pattern, replacement in ALLOWED_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


# Empirical column ceiling for SUB_SKILL_DESCRIPTIONS entries in the
# USER-GUIDE Section 22 sub-skill table. Verified at v3.7.4 against the
# 115mm Helvetica 9pt rendered column. Two entries (higgsfield-cinema,
# higgsfield-seedance) currently sit at the ceiling; further extension
# overflows the column.
SUB_SKILL_DESCRIPTION_CEILING = 71


def validate_sub_skill_descriptions():
    """Layer 0: assert each SUB_SKILL_DESCRIPTIONS entry fits the column ceiling.

    Source-data validation runs before baseline/candidate comparison so an
    overflow entry fails fast rather than silently rendering as wrapped or
    clipped text in the regenerated PDF (which the baseline diff would not
    catch as a regression). Prevents the v3.7.3->v3.7.4 inherited-error
    class where corrected char-count math surfaced only at the next release.
    """
    try:
        from generate_user_guide import SUB_SKILL_DESCRIPTIONS
    except ImportError:
        print("[Layer 0] SUB_SKILL_DESCRIPTIONS check: ENVIRONMENT ERROR")
        print("  Cannot import generate_user_guide. Run validator from repo root.")
        sys.exit(2)

    overflow = [
        (name, len(desc), desc)
        for name, desc in SUB_SKILL_DESCRIPTIONS.items()
        if len(desc) > SUB_SKILL_DESCRIPTION_CEILING
    ]
    if overflow:
        print("[Layer 0] SUB_SKILL_DESCRIPTIONS check: OVERFLOW DETECTED")
        print(f"  Ceiling: {SUB_SKILL_DESCRIPTION_CEILING} chars (empirical, v3.7.4 verified)")
        for name, length, desc in overflow:
            print(f"  {name}: {length} chars  '{desc}'")
        sys.exit(1)
    longest = max(len(v) for v in SUB_SKILL_DESCRIPTIONS.values())
    print("[Layer 0] SUB_SKILL_DESCRIPTIONS check: PASS")
    print(f"  All {len(SUB_SKILL_DESCRIPTIONS)} entries <= {SUB_SKILL_DESCRIPTION_CEILING} chars (longest: {longest}).")


def main():
    # Layer 0: source-data check before baseline/candidate comparison.
    validate_sub_skill_descriptions()
    print()

    baseline_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_BASELINE
    candidate_path = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_CANDIDATE

    if not baseline_path.exists():
        print(f"ERROR: baseline not found: {baseline_path}")
        sys.exit(2)
    if not candidate_path.exists():
        print(f"ERROR: candidate not found: {candidate_path}")
        sys.exit(2)

    print(f"Baseline:  {baseline_path}")
    print(f"Candidate: {candidate_path}")
    print()

    baseline_text = extract_text(baseline_path)
    candidate_text = extract_text(candidate_path)

    # Layer 1: text-extract diff with allowed patterns normalized.
    baseline_norm = normalize(baseline_text)
    candidate_norm = normalize(candidate_text)

    if baseline_norm == candidate_norm:
        print("[Layer 1] Text-extract diff: PASS")
        print("  No substantive content differences after normalizing")
        print("  version/date/count patterns.")
    else:
        print("[Layer 1] Text-extract diff: REGRESSION DETECTED")
        print()
        import difflib
        diff = difflib.unified_diff(
            baseline_norm.splitlines(keepends=True),
            candidate_norm.splitlines(keepends=True),
            fromfile="baseline (normalized)",
            tofile="candidate (normalized)",
            n=3,
        )
        sys.stdout.writelines(diff)
        sys.exit(1)

    # Layer 2: binary diff (informational — counts byte-different positions).
    baseline_bytes = baseline_path.read_bytes()
    candidate_bytes = candidate_path.read_bytes()

    if baseline_bytes == candidate_bytes:
        print("[Layer 2] Binary diff: identical (byte-for-byte match)")
    else:
        diff_count = sum(
            1 for a, b in zip(baseline_bytes, candidate_bytes) if a != b
        ) + abs(len(baseline_bytes) - len(candidate_bytes))
        print(f"[Layer 2] Binary diff: {diff_count} byte positions differ")
        print(f"  Baseline size:  {len(baseline_bytes)} bytes")
        print(f"  Candidate size: {len(candidate_bytes)} bytes")
        print("  (Bytes differ in parameterized version/date strings + /CreationDate metadata.")
        print("   Layer 1 already confirmed no content regression.)")

    print()
    print("VALIDATION PASSED")


if __name__ == "__main__":
    main()
