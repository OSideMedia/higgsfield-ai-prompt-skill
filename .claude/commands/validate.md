---
description: Run the release gate (validate --strict + pytest + evals) and report whether the repo is release-ready
---

"Release-ready" means the full release gate is green — never the plain
`validate.py` run, which lets optional-dependency SKIPs and stale generated
views pass (before v3.37.0 this command certified readiness from the
non-strict run while `--strict` was red).

Run all three, in order, and keep going after a failure so the report is complete:

```bash
python3 scripts/validate.py --strict
python3 -m pytest tests/ -q
python3 scripts/validate.py --evals
```

Report:

- For each command: PASS or FAIL, plus every failing check / test / eval case
  with its file path and what needs fixing (quote the checker's own line).
- Say **release-ready** ONLY when all three exited 0. If any failed, say
  "not release-ready" and list the blockers — do not soften it because the
  non-strict run would pass.
- If `--strict` fails only on items the non-strict run would merely WARN or
  SKIP (stale snapshot, stale `db/memory-summary.md` / `db/ledger/_global.json`,
  missing fpdf2), name the fix command the failure line gives.

For a quick iteration check while editing (NOT a readiness verdict), the plain
`python3 scripts/validate.py` is fine — report it as "health check", never as
release-ready.
