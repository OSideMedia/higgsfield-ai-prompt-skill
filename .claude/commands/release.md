---
description: Guided release — branch, gates, PR, merge, tag the MERGE commit, GitHub release + PDF upload
---

Walk through a release for version $ARGUMENTS (e.g. `/release 2.1.0`).

If no version argument is provided, check CHANGELOG.md for the latest version and ask what the new version should be.

`main` is protected: nothing is committed or pushed to it directly. The release
lands through a PR, and the tag goes on the **merge commit** that PR creates on
`main` — never on the branch commit. (CLAUDE.md § Rules is the source of this
ceremony; keep the two in step.)

Steps:

0. **Sanitize the version argument** — before using `$ARGUMENTS` in any shell command, confirm it is a bare semantic version matching `^[0-9]+\.[0-9]+\.[0-9]+$` (e.g. `2.1.0`). If it contains anything else (spaces, `;`, backticks, quotes, path separators), STOP and ask the user for a clean version string — never interpolate an unvalidated argument into the `git` / `gh` shell snippets below.
1. **Release branch** — from an up-to-date `main`: `git switch main && git pull --ff-only && git switch -c release/v$ARGUMENTS` (or continue on the existing `release/v$ARGUMENTS`). Never commit on `main`.
2. **Bump + changelog** — set the root `SKILL.md` frontmatter `metadata.version` / `metadata.updated` and the README badge + footer (validate.py checks they agree); confirm CHANGELOG.md has a `v$ARGUMENTS` entry — if not, ask what to add.
3. **Release gate** — `python3 scripts/validate.py --strict`, `python3 -m pytest tests/ -q`, `python3 scripts/validate.py --evals`. Stop if any of the three fails.
4. **User guide: regenerate → refresh MANIFEST** — AFTER the version bump: `python3 scripts/generate_user_guide.py`, then `python3 scripts/validate_user_guide.py` (manifest comparison; review any flagged drift), then `python3 scripts/validate_user_guide.py --write-manifest` and stage `docs/user-guide/MANIFEST.json`. The PDF is a release artifact — git-ignored, never committed; keep the generated `docs/user-guide/USER-GUIDE.pdf` for step 9.
5. **Commit on the branch** — `feat: v$ARGUMENTS — <summary from changelog>` (or `fix:` for a fix release). Re-run the three gates if anything changed after step 3.
6. **Push the branch + open the PR** — confirm with the user first: `git push -u origin release/v$ARGUMENTS`, then `gh pr create --base main --head release/v$ARGUMENTS --title "v$ARGUMENTS — <summary>" --body-file -` with the changelog entry. Wait for the `validate` CI check to pass.
7. **Merge** — confirm with the user; merge the PR with a merge commit (`gh pr merge <number> --merge`). Then read the merge commit id from GitHub, not from local history: `MERGE=$(gh pr view <number> --json mergeCommit --jq .mergeCommit.oid)`.
8. **Tag the MERGE commit** — `git fetch origin && git tag -a v$ARGUMENTS "$MERGE" -m "v$ARGUMENTS"` and confirm `git rev-parse v$ARGUMENTS^{commit}` equals `$MERGE` and is on `origin/main` (`git merge-base --is-ancestor "$MERGE" origin/main`). Push only the tag: `git push origin v$ARGUMENTS`.
9. **GitHub release + PDF** — confirm with the user: `gh release create v$ARGUMENTS --verify-tag --title "v$ARGUMENTS" --notes-file -` using the changelog entry, then `gh release upload v$ARGUMENTS docs/user-guide/USER-GUIDE.pdf`. If anything else merged into `main` between step 4 and the merge, check out the tag, regenerate the PDF and confirm `python3 scripts/validate_user_guide.py` matches the committed MANIFEST before uploading.
10. **Clean up** — delete the release branch on both sides after the merge: `git push origin --delete release/v$ARGUMENTS` and `git branch -d release/v$ARGUMENTS`.

Confirm with the user before each visible step (push, PR, merge, tag push, release, upload). Never force-push, never tag a branch commit, never commit to `main`.
