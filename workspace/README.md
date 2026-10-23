# workspace/ — file handling for Cowork

This folder gives the skill a predictable place to read your material from and
write its results to, so uploaded documents and generated work never get
scattered across the project root.

| Folder | What goes here | Who puts it there |
|--------|----------------|-------------------|
| `input/` | Anything you want the skill to read — scripts, story bibles, briefs, character sheets, reference notes, shot lists, brand docs. | You (drop files here). The skill also copies stray uploads here, leaving the original in place. |
| `output/` | Anything the skill produces as a file — prompt packs, shot breakdowns, batch CSVs, reports, exported docs. | The skill. |
| `processed/` | Inputs the skill has finished consuming. Keeps `input/` clean without deleting your originals. | The skill (moves files here when a task is done). |

## How to use it in Cowork

1. **Giving the skill a document** → drop it in `workspace/input/`. When the skill
   asks you for a script, bible, or reference, that's where it expects to find it.
2. **Getting work back** → check `workspace/output/`. Finished files land there.
3. **Cleanup** → once a task is complete the skill moves the source from
   `input/` to `processed/`. Your originals are preserved, just relocated.

Your files in `input/`, `output/`, and `processed/` stay **local** — they are
git-ignored and never pushed. Only these README files ship with the skill.

**Claude Code with the skill installed in `~/.claude/skills/higgsfield/`:** this
folder is not used. The skill creates `workspace/` inside the project you are
working in instead, so a reinstall of the skill never touches your files.
In that project the folders are not git-ignored unless you ignore them.
