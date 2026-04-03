---
description: Guided version bump — validate, tag, and create GitHub release
---

Walk through a release for version $ARGUMENTS (e.g. `/project:release 2.1.0`).

If no version argument is provided, check CHANGELOG.md for the latest version and ask what the new version should be.

Steps:

1. **Validate** — run `python3 validate.py`. Stop if any check fails.
2. **Changelog check** — confirm CHANGELOG.md has an entry for this version. If not, ask what to add.
3. **Commit** — stage and commit any pending changes with message: `feat: v$ARGUMENTS — <summary from changelog>`
4. **Tag** — create git tag `v$ARGUMENTS`
5. **Push** — push commit and tag: `git push && git push --tags`
6. **GitHub release** — create release from the tag: `gh release create v$ARGUMENTS --title "v$ARGUMENTS" --notes-file -` using the changelog entry as notes.

Confirm with the user before each destructive/visible step (commit, push, release).
