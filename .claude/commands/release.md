---
description: Guided version bump — validate, tag, and create GitHub release
---

Walk through a release for version $ARGUMENTS (e.g. `/release 2.1.0`).

If no version argument is provided, check CHANGELOG.md for the latest version and ask what the new version should be.

Steps:

0. **Sanitize the version argument** — before using `$ARGUMENTS` in any shell command, confirm it is a bare semantic version matching `^[0-9]+\.[0-9]+\.[0-9]+$` (e.g. `2.1.0`). If it contains anything else (spaces, `;`, backticks, quotes, path separators), STOP and ask the user for a clean version string — never interpolate an unvalidated argument into the `git commit` / `git tag` / `gh release create` shell snippets below.
1. **Release gate** — run `python3 scripts/validate.py --strict`, `python3 -m pytest tests/ -q`, and `python3 scripts/validate.py --evals`. Stop if any of the three fails.
2. **Changelog check** — confirm CHANGELOG.md has an entry for this version. If not, ask what to add.
3. **Regenerate the user guide + manifest** — AFTER the frontmatter version/date are bumped: `python3 scripts/generate_user_guide.py`, then `python3 scripts/validate_user_guide.py` (manifest-fallback comparison; review any flagged drift), then `python3 scripts/validate_user_guide.py --write-manifest` and stage the refreshed `docs/user-guide/MANIFEST.json`. The PDF itself is a release artifact — it is git-ignored, never committed.
4. **Commit** — stage and commit any pending changes with message: `feat: v$ARGUMENTS — <summary from changelog>`
5. **Tag** — create git tag `v$ARGUMENTS`
6. **Push** — push commit and tag: `git push && git push --tags`
7. **GitHub release** — create release from the tag: `gh release create v$ARGUMENTS --title "v$ARGUMENTS" --notes-file -` using the changelog entry as notes.
8. **Attach the guide** — `gh release upload v$ARGUMENTS docs/user-guide/USER-GUIDE.pdf` so the PDF ships with the release instead of the git history.

Confirm with the user before each destructive/visible step (commit, push, release).
