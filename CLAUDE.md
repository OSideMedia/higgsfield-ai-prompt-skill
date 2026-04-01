# CLAUDE.md

- Every SKILL.md must have frontmatter: `name`, `description`, `metadata.version`, `metadata.updated`, `metadata.parent`
- Never rename or move `mnt/user-data/outputs/higgsfield/` — it mirrors the Cowork filesystem layout
- Update `CHANGELOG.md` for every user-facing change
- Run `python3 validate.py` before any release
- Version bumps require a git tag + GitHub release, not just a commit
- Commit format: `feat: vX.Y.Z — description` or `fix: vX.Y.Z — description`
