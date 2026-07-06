#!/usr/bin/env python3
"""Spec-drift tripwire — Wave C Tier 1 (item 5).

Turns the reactive 30-day staleness WARN in validate.py into a PROACTIVE check:
pull the live model catalog from the Higgsfield CLI, diff it against the
committed `specs/models_explore_snapshot_<date>.json`, and report drift loudly.

WHY THE CLI IS A DETECTOR, NOT A SOURCE OF TRUTH
  `higgsfield model get <id> --json` returns enum VALUES but no parameter
  `description` prose, and that prose is where sync_specs.py reads the
  cross-constraints ("4k only with mode='std'"). So this tool catches the
  high-value drift — new/removed models, enum-option changes (a `resolution`
  gaining `4k` IS visible), default changes, a tracked param vanishing — but it
  CANNOT see a pure cross-constraint prose change when enum membership holds.
  That blind spot is acknowledged and logged, never silently passed.

TWO-TIER MODEL
  Tier 1 (this script, headless): detect drift → tell you WHEN to refresh.
  Tier 2 (unchanged, interactive): a full `models_explore` dump → sync_specs.py,
  the only source with the constraint prose. Human-in-loop, as today.

  This script DETECTS ONLY — it never writes specs (beyond its own CLI
  baseline), never opens a PR, never edits the curated guides. When it reports a
  change, a human runs Tier 2.

DEFAULT MODE — CLI-baseline self-diff (the trustworthy tripwire)
  Compares the live CLI against a committed baseline of the LAST-ACCEPTED CLI
  surface (`specs/cli_baseline.json`). Both sides are the same source, so the
  result is pure change-over-time — immune to the CLI↔models_explore
  disagreements that make a snapshot-diff cry wolf (the CLI reports
  gpt_image_2=2k/high where models_explore says 1k/low; baked into the baseline
  once, that disagreement never re-alarms). Bootstrap with `--update-baseline`;
  after reviewing a change, accept it the same way.

  `--vs-snapshot` keeps the legacy mode (CLI vs the models_explore snapshot —
  "is my snapshot behind the live CLI?"), which is source-disagreement-prone.

Usage:
  python3 scripts/refresh_specs.py --update-baseline   # bootstrap / accept current CLI
  python3 scripts/refresh_specs.py                      # self-diff vs baseline (default)
  python3 scripts/refresh_specs.py --type video         # one type
  python3 scripts/refresh_specs.py --vs-snapshot        # legacy snapshot-diff
  python3 scripts/refresh_specs.py --json               # machine-readable diff

Exit codes (the three states must stay distinguishable — a silent failure would
falsely read as "fresh", which is worse than the reactive WARN we already have):
  0  fresh — no change since baseline
  3  change detected — Tier 2 refresh + audit evals/cases/, then --update-baseline
  1  pull failed — CLI/auth error (e.g. session expired; run `higgsfield auth login`)
  2  usage error
  4  CLI output shape changed — the CLI's JSON no longer matches what this script
     parses (e.g. the 1.0.1 `job_set_type`→`job_type` rename); fix the parser,
     do NOT re-auth
"""
import argparse
import json
import shutil
import subprocess
import sys

from sync_specs import SPECS_DIR, find_snapshot, snapshot_date

CLI = "higgsfield"
# Snapshot top-level fields that the CLI represents as parameters instead.
_ASPECT_PARAM = "aspect_ratio"
# Committed last-accepted CLI state. The self-diff compares CLI-now against THIS
# (apples-to-apples, same source), so a persistent CLI↔models_explore
# disagreement — baked into the baseline once — never cries wolf again.
BASELINE_PATH = SPECS_DIR / "cli_baseline.json"


class PullError(RuntimeError):
    """The live pull failed (CLI missing, not authenticated, bad JSON). Kept
    distinct from "drift" so the exit code can stay loud."""


class ShapeError(RuntimeError):
    """The CLI answered, but its JSON shape is not what this script parses —
    a parser-compatibility problem, not an auth problem. Kept distinct from
    PullError so CI can say "fix the parser" instead of "re-auth" (exit 4).
    CLI 1.0.1 renaming `job_set_type` → `job_type` is the canonical case."""


# The model-id key was renamed in CLI 1.0.1; accept both, newest first.
_ID_KEYS = ("job_type", "job_set_type")


def _model_id(obj: dict, context: str) -> str:
    """The model id from a `model list` row or `model get` payload, tolerating
    the 1.0.1 key rename. Any future rename lands here as a loud ShapeError."""
    for key in _ID_KEYS:
        if obj.get(key):
            return obj[key]
    raise ShapeError(
        f"{context}: no model-id key found (tried {'/'.join(_ID_KEYS)}) in "
        f"keys={sorted(obj)[:12]} — CLI output shape changed; update refresh_specs.py")


# ── Normalization: snapshot item ↔ CLI `model get`, into one comparable view ──

def _opts(values) -> list:
    return sorted(str(v) for v in (values or []))


def snapshot_view(item: dict) -> dict:
    """Comparable view of one committed-snapshot model (the tracked shape)."""
    return {
        "id": item["id"],
        "output_type": item.get("output_type"),
        "aspect_ratios": _opts(item.get("aspect_ratios")),
        "params": {
            p["name"]: {"options": _opts(p.get("options")),
                        "default": p.get("default")}
            for p in item.get("parameters", [])
        },
    }


def cli_view(get_json: dict) -> dict:
    """Comparable view of one `higgsfield model get` payload. The CLI calls the
    enum list `enum` (snapshot says `options`) and carries aspect ratios as an
    `aspect_ratio` param rather than a top-level field — normalize both away."""
    try:
        params = {p["name"]: p for p in get_json.get("params", [])}
    except (KeyError, TypeError) as e:
        raise ShapeError(f"model get params shape changed ({e!r}) — "
                         f"update refresh_specs.py")
    aspect = params.get(_ASPECT_PARAM, {})
    return {
        "id": _model_id(get_json, "model get"),
        "output_type": get_json.get("type"),
        "aspect_ratios": _opts(aspect.get("enum")),
        "params": {
            name: {"options": _opts(p.get("enum")), "default": p.get("default")}
            for name, p in params.items()
        },
        # CLI 1.0.1 dropped per-param `enum` lists but added machine-readable
        # CEL constraint rules — the cross-constraint prose this tool was
        # historically blind to. Track them as their own comparison channel.
        "rules": sorted(r.get("cel") or r.get("message") or ""
                        for r in get_json.get("rules", [])),
    }


# ── The diff (pure) ──────────────────────────────────────────────────────────

def diff_model(old: dict, new: dict) -> dict:
    """Classify drift in one model into DRIFT vs NOTICE, comparing only the
    TRACKED params (those the snapshot carries).

    The two sources diverge in DETAIL, not just coverage: the CLI's `model get`
    sometimes returns `enum: null` where the snapshot enumerates options (e.g.
    clipify fonts), and omits some params/models the snapshot has. So a
    capability the snapshot has but the CLI lacks is usually the CLI
    under-reporting, NOT a real withdrawal. The reliable, apples-to-apples
    signal is the OTHER direction: a value the live CLI has that the snapshot
    LACKS — a new capability shipped (the Seedance-4K staleness case). That is
    DRIFT. Removals / missing things are NOTICE: real-or-artifact, Tier 2 to
    confirm. Returns {"drift": [...], "notice": [...]}."""
    drift, notice = [], []
    aspect_added = [a for a in new["aspect_ratios"] if a not in old["aspect_ratios"]]
    aspect_gone = [a for a in old["aspect_ratios"] if a not in new["aspect_ratios"]]
    if aspect_added:
        drift.append({"kind": "aspect_ratios", "added": aspect_added})
    if aspect_gone:
        notice.append({"kind": "aspect_ratios_gone", "removed": aspect_gone})

    for pname, op in old["params"].items():
        np = new["params"].get(pname)
        if np is None:
            notice.append({"kind": "param_missing", "param": pname})
            continue
        # New option only counts when BOTH sides enumerate (else it's the CLI
        # simply not listing options, not a real membership change).
        if op["options"] and np["options"]:
            added = [o for o in np["options"] if o not in op["options"]]
            removed = [o for o in op["options"] if o not in np["options"]]
            if added:
                drift.append({"kind": "options_added", "param": pname, "added": added})
            if removed:
                notice.append({"kind": "options_removed", "param": pname, "removed": removed})
        elif op["options"] != np["options"]:
            notice.append({"kind": "options_undetailed", "param": pname})
        if op["default"] is not None and np["default"] is not None \
                and op["default"] != np["default"]:
            drift.append({"kind": "default", "param": pname,
                          "from": op["default"], "to": np["default"]})

    # CEL rules: only comparable when BOTH sides carry the channel (snapshot
    # views and pre-1.0.1 baselines don't — never alarm on a missing channel).
    if old.get("rules") is not None and new.get("rules") is not None:
        rules_added = [x for x in new["rules"] if x not in old["rules"]]
        rules_gone = [x for x in old["rules"] if x not in new["rules"]]
        if rules_added:
            drift.append({"kind": "rules_added", "added": rules_added})
        if rules_gone:
            notice.append({"kind": "rules_removed", "removed": rules_gone})
    return {"drift": drift, "notice": notice}


def diff_catalog(old_views: dict, new_views: dict) -> dict:
    """Diff committed-snapshot views (old) against live-CLI views (new).

    Only ADDED capabilities on shared models flip the drift state (high
    confidence, low false-positive — see diff_model). Catalog membership
    differences are NOTICE: the CLI list is a superset on one axis (utility
    jobs) and a subset on another (it omits some models the snapshot tracks),
    so neither `models_added` nor `models_removed` is a reliable alarm."""
    old_ids, new_ids = set(old_views), set(new_views)
    per_model = {}
    for mid in sorted(old_ids & new_ids):
        d = diff_model(old_views[mid], new_views[mid])
        if d["drift"] or d["notice"]:
            per_model[mid] = d
    return {
        "models_changed": per_model,
        "models_removed": sorted(old_ids - new_ids),   # notice
        "models_added": sorted(new_ids - old_ids),      # notice
    }


def has_drift(diff: dict) -> bool:
    """Drift = a live ADDED capability on a tracked model. Catalog membership
    and any removal/under-detail are notices, not drift."""
    return any(m["drift"] for m in diff["models_changed"].values())


# ── The live pull (impure — isolated so the diff stays unit-testable) ─────────

def _cli_json(args: list) -> object:
    if shutil.which(CLI) is None:
        raise PullError(f"`{CLI}` CLI not found on PATH (brew install higgsfield-ai/tap/higgsfield)")
    proc = subprocess.run([CLI, *args, "--json"], capture_output=True, text=True)
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip().splitlines()
        hint = err[0] if err else f"exit {proc.returncode}"
        raise PullError(f"`{CLI} {' '.join(args)}` failed: {hint}")
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        raise PullError(f"`{CLI} {' '.join(args)}` returned non-JSON: {e}")


def pull_cli_views(output_type: str, ids: set = None) -> tuple:
    """Live CLI views, plus the catalog id→display_name map. `ids=None` pulls
    EVERY catalog model (the baseline self-diff wants the whole live surface);
    an id set restricts to those present (the snapshot-diff only needs tracked
    models). N+1 calls: one `model list`, one `model get` per target."""
    catalog = _cli_json(["model", "list", f"--{output_type}"])
    if not isinstance(catalog, list):
        raise ShapeError(f"model list --{output_type}: expected a JSON array, "
                         f"got {type(catalog).__name__} — update refresh_specs.py")
    catalog_ids = {mid: m.get("display_name", mid)
                   for m in catalog
                   for mid in (_model_id(m, f"model list --{output_type}"),)}
    targets = set(catalog_ids) if ids is None else (ids & set(catalog_ids))
    views = {mid: cli_view(_cli_json(["model", "get", mid]))
             for mid in sorted(targets)}
    return views, catalog_ids


# ── Report + driver ──────────────────────────────────────────────────────────

def render(output_type: str, snap_date: str, diff: dict, catalog_ids: dict,
           verbose: bool = False) -> str:
    lines = [f"[{output_type}] snapshot {snap_date} vs live CLI catalog"]
    for mid, d in diff["models_changed"].items():
        for c in d["drift"]:
            if c["kind"] == "options_added":
                lines.append(f"  ⚠ DRIFT — {mid}.{c['param']} gained {'/'.join(c['added'])}")
            elif c["kind"] == "aspect_ratios":
                lines.append(f"  ⚠ DRIFT — {mid} aspect_ratios gained {'/'.join(c['added'])}")
            elif c["kind"] == "default":
                lines.append(f"  ⚠ DRIFT — {mid}.{c['param']} default "
                             f"{c['from']!r} → {c['to']!r}")
            elif c["kind"] == "rules_added":
                for rule in c["added"]:
                    lines.append(f"  ⚠ DRIFT — {mid} new constraint rule: {rule}")
    if not has_drift(diff):
        lines.append("  ✓ no tracked drift (no new live capability the snapshot lacks)")

    # Notices: real-or-artifact, surfaced for review, never flip the exit code.
    notices = []
    if diff["models_removed"]:
        notices.append(f"snapshot models absent from CLI catalog: "
                       f"{', '.join(diff['models_removed'])}")
    if diff["models_added"]:
        notices.append(f"CLI catalog models not in snapshot (new or utility): "
                       f"{', '.join(diff['models_added'])}")
    n_model_notices = sum(len(d["notice"]) for d in diff["models_changed"].values())
    if verbose:
        for mid, d in diff["models_changed"].items():
            for c in d["notice"]:
                notices.append(f"{mid}: {c['kind']} "
                               f"{c.get('param', '') or '/'.join(c.get('removed', []))}".strip())
    elif n_model_notices:
        notices.append(f"{n_model_notices} param-level note(s) (CLI under-detail / "
                       f"removals) — rerun with --verbose to list")
    for n in notices:
        lines.append(f"  · {n}")
    return "\n".join(lines)


def check_type(output_type: str, verbose: bool = False) -> tuple:
    """Snapshot-diff mode (--vs-snapshot): is the committed `models_explore`
    snapshot behind the live CLI? Source-disagreement-prone — see module docs.
    Returns (report_text, diff_dict). Raises PullError on a failed pull."""
    snap_path = find_snapshot(output_type=output_type)
    snapshot = json.loads(snap_path.read_text(encoding="utf-8"))
    old_views = {m["id"]: snapshot_view(m)
                 for m in snapshot.get("items", [])
                 if m.get("output_type") == output_type}
    new_views, catalog_ids = pull_cli_views(output_type, set(old_views))
    diff = diff_catalog(old_views, new_views)
    return render(output_type, snapshot_date(snap_path), diff, catalog_ids, verbose), diff


# ── v2: CLI-baseline self-diff (the trustworthy tripwire) ────────────────────

def any_change(diff: dict) -> bool:
    """In self-diff BOTH sides are the live CLI, so EVERY difference is a real
    change worth a refresh — adds, removals, membership, defaults alike. (The
    drift/notice split only mattered against the models_explore snapshot, where
    removals were the CLI under-reporting.)"""
    return bool(diff["models_added"] or diff["models_removed"]
                or any(m["drift"] or m["notice"]
                       for m in diff["models_changed"].values()))


def load_baseline() -> dict:
    if not BASELINE_PATH.exists():
        return {}
    return json.loads(BASELINE_PATH.read_text(encoding="utf-8"))


def capture_baseline(types) -> dict:
    """Pull every catalog model and snapshot the live CLI surface. The captured
    date is informational; the views are what the self-diff compares."""
    from datetime import date
    out = {"captured": date.today().isoformat()}
    for t in types:
        views, _ = pull_cli_views(t, ids=None)
        out[t] = views
    return out


def render_self_diff(output_type: str, baseline: dict, diff: dict) -> str:
    when = baseline.get("captured", "?")
    lines = [f"[{output_type}] live CLI vs baseline ({when})"]
    for mid in diff["models_added"]:
        lines.append(f"  ⚠ CHANGED — new model in CLI: {mid}")
    for mid in diff["models_removed"]:
        lines.append(f"  ⚠ CHANGED — model gone from CLI: {mid}")
    for mid, d in diff["models_changed"].items():
        for c in d["drift"] + d["notice"]:
            if c["kind"] in ("options_added",):
                lines.append(f"  ⚠ CHANGED — {mid}.{c['param']} gained {'/'.join(c['added'])}")
            elif c["kind"] == "options_removed":
                lines.append(f"  ⚠ CHANGED — {mid}.{c['param']} dropped {'/'.join(c['removed'])}")
            elif c["kind"] == "aspect_ratios":
                lines.append(f"  ⚠ CHANGED — {mid} aspect_ratios gained {'/'.join(c['added'])}")
            elif c["kind"] == "aspect_ratios_gone":
                lines.append(f"  ⚠ CHANGED — {mid} aspect_ratios dropped {'/'.join(c['removed'])}")
            elif c["kind"] == "default":
                lines.append(f"  ⚠ CHANGED — {mid}.{c['param']} default "
                             f"{c['from']!r} → {c['to']!r}")
            elif c["kind"] == "param_missing":
                lines.append(f"  ⚠ CHANGED — {mid}.{c['param']} param gone")
            elif c["kind"] == "options_undetailed":
                lines.append(f"  ⚠ CHANGED — {mid}.{c['param']} options now undetailed")
            elif c["kind"] == "rules_added":
                for rule in c["added"]:
                    lines.append(f"  ⚠ CHANGED — {mid} new constraint rule: {rule}")
            elif c["kind"] == "rules_removed":
                for rule in c["removed"]:
                    lines.append(f"  ⚠ CHANGED — {mid} constraint rule gone: {rule}")
    if not any_change(diff):
        lines.append("  ✓ no change since baseline")
    return "\n".join(lines)


def check_type_vs_baseline(output_type: str, baseline: dict) -> tuple:
    """Self-diff mode (default): live CLI vs the committed CLI baseline. Both
    sides are the same source, so the result is pure change-over-time — immune to
    the CLI↔models_explore disagreements that made the snapshot-diff noisy."""
    if output_type not in baseline:
        raise FileNotFoundError(
            f"no '{output_type}' baseline in {BASELINE_PATH.name} — "
            f"bootstrap it: python3 scripts/refresh_specs.py --update-baseline")
    old_views = baseline[output_type]
    new_views, _ = pull_cli_views(output_type, ids=None)
    diff = diff_catalog(old_views, new_views)
    return render_self_diff(output_type, baseline, diff), diff


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        prog="scripts/refresh_specs.py", description=__doc__.splitlines()[0])
    p.add_argument("--type", choices=("video", "image", "audio", "both", "all"),
                   default="all",
                   help="'all' = video+image+audio (default); "
                        "'both' = video+image (pre-audio alias)")
    p.add_argument("--json", action="store_true", help="machine-readable diff")
    p.add_argument("--verbose", action="store_true", help="list every param-level notice")
    p.add_argument("--update-baseline", action="store_true",
                   help="capture the current live CLI surface as the new baseline")
    p.add_argument("--vs-snapshot", action="store_true",
                   help="legacy mode: diff CLI vs the models_explore snapshot "
                        "(source-disagreement-prone)")
    args = p.parse_args(argv)
    types = {"all": ("video", "image", "audio"),
             "both": ("video", "image")}.get(args.type, (args.type,))

    # --update-baseline: bootstrap / accept the current live surface.
    if args.update_baseline:
        try:
            fresh = capture_baseline(types)
        except ShapeError as e:
            print(f"CLI SHAPE CHANGED: {e}", file=sys.stderr)
            return 4
        except PullError as e:
            print(f"PULL FAILED: {e}\n  → run: higgsfield auth login", file=sys.stderr)
            return 1
        merged = {**load_baseline(), **fresh}
        BASELINE_PATH.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n",
                                 encoding="utf-8")
        print(f"baseline updated for {', '.join(types)} → {BASELINE_PATH.name} "
              f"(captured {fresh['captured']})")
        return 0

    baseline = {} if args.vs_snapshot else load_baseline()
    if not args.vs_snapshot and not baseline:
        print(f"no baseline yet — bootstrap it: python3 scripts/refresh_specs.py "
              f"--update-baseline", file=sys.stderr)
        return 1

    reports, diffs, changed = [], {}, False
    for t in types:
        try:
            if args.vs_snapshot:
                text, diff = check_type(t, verbose=args.verbose)
                changed = changed or has_drift(diff)
            else:
                text, diff = check_type_vs_baseline(t, baseline)
                changed = changed or any_change(diff)
        except ShapeError as e:
            print(f"CLI SHAPE CHANGED [{t}]: {e}", file=sys.stderr)
            print("  → not fresh, not changed — the parser is blind until "
                  "refresh_specs.py is updated for the new CLI output.", file=sys.stderr)
            return 4
        except PullError as e:
            print(f"PULL FAILED [{t}]: {e}", file=sys.stderr)
            print("  → not fresh, not changed — the live state is unknown. "
                  "If the session expired, run: higgsfield auth login", file=sys.stderr)
            return 1
        except FileNotFoundError as e:
            print(f"MISSING [{t}]: {e}", file=sys.stderr)
            return 1
        reports.append(text)
        diffs[t] = diff

    if args.json:
        print(json.dumps(diffs, indent=2))
    else:
        print("\n".join(reports))
        if changed:
            print("\nCHANGE DETECTED → refresh the snapshot (Tier 2): dump "
                  "`models_explore`, run `python3 scripts/sync_specs.py`, audit "
                  "`evals/cases/` in the same PR (v3.11.2/v3.11.3), then accept "
                  "the new live surface with `--update-baseline`.")
        else:
            print("\nFresh. (Blind spot: a cross-constraint prose change with no "
                  "enum movement is invisible here — Tier 2 is authoritative.)")
    return 3 if changed else 0


if __name__ == "__main__":
    sys.exit(main())
