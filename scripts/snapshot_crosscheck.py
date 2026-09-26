#!/usr/bin/env python3
"""
snapshot_crosscheck.py
======================
Two-way STRUCTURAL cross-check: a committed `models_explore` snapshot (MCP) vs
the raw `higgsfield model get --json` payloads (CLI), per model present in both.
Stdlib only. Read-only: `higgsfield model list/get` calls, never a generation.

Why: the two sources are independent views of one catalog. The Tier-2 refresh
writes specs from the MCP dump; the tripwire (refresh_specs.py) watches the CLI.
A disagreement between them is either an MCP dump that is wrong/incomplete or a
known representation difference — it must be ADJUDICATED, never silently
tolerated. Checks, per shared model:

  params_missing_in_cli       a snapshot param the CLI does not have
  param_missing_in_snapshot   a CLI ENUM param the snapshot lacks (aspect_ratio
                              excluded: models_explore carries it top-level)
  options                     enum membership differs (both sides enumerate)
  default                     defaults differ (both sides state one)
  aspect_ratios               snapshot aspect_ratios vs the CLI aspect_ratio enum
  media_roles                 snapshot medias[].roles vs the CLI's media-role
                              params (start_image, image_references, mask, …)

Known disagreements live in specs/crosscheck_allowlist.json — each entry names
the model, field, kind, the date it was seen, AND the observed detail. An
allowlisted disagreement is still PRINTED; if its detail changes it fails again
(the allowlist accepts one observed fact, not a class of future ones); an entry
that no longer disagrees is reported as stale.

Usage:
  python3 scripts/snapshot_crosscheck.py                    # every type, live CLI
  python3 scripts/snapshot_crosscheck.py --type image
  python3 scripts/snapshot_crosscheck.py --cli-dir DIR      # recorded payloads:
        DIR/list_all.json (unfiltered `model list --json`) + DIR/get_<id>.json

Exit codes: 0 agree (allowlisted items printed), 1 disagreement,
            2 usage / bad allowlist, 3 could not compare (CLI pull or shape).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import refresh_specs as rs
import sync_specs

ALLOWLIST_PATH = sync_specs.SPECS_DIR / "crosscheck_allowlist.json"
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_ALLOW_KEYS = ("model", "field", "kind", "seen", "detail")


def _norm(v) -> str:
    return str(v).lower()


def _fmt(values) -> str:
    return "[" + ", ".join(sorted(str(v) for v in values)) + "]"


def compare_model(item: dict, cli_get) -> list:
    """Disagreement records for one model: {model, field, kind, detail}.
    `detail` is deterministic so an allowlist entry can pin it."""
    view = rs.cli_view(cli_get)                     # ShapeError on a bad payload
    mid = item["id"]
    out = []

    def add(field, kind, detail):
        out.append({"model": mid, "field": field, "kind": kind, "detail": detail})

    snap_params = {p["name"]: p for p in item.get("parameters", []) if p.get("name")}
    cli_params = view["params"]
    for name, sp in sorted(snap_params.items()):
        cp = cli_params.get(name)
        if cp is None:
            add(name, "param_missing_in_cli", "in snapshot, absent from `model get`")
            continue
        s_opts = sp.get("options")
        if s_opts and cp["options"] and {_norm(o) for o in s_opts} != {_norm(o) for o in cp["options"]}:
            snap_only = sorted({str(o) for o in s_opts if _norm(o) not in {_norm(c) for c in cp["options"]}})
            cli_only = sorted({str(o) for o in cp["options"] if _norm(o) not in {_norm(s) for s in s_opts}})
            add(name, "options", f"snapshot-only={_fmt(snap_only)} cli-only={_fmt(cli_only)}")
        if sp.get("default") is not None and cp.get("default") is not None \
                and _norm(sp["default"]) != _norm(cp["default"]):
            add(name, "default", f"snapshot={sp['default']!r} cli={cp['default']!r}")
    for name, cp in sorted(cli_params.items()):
        if name == rs._ASPECT_PARAM or name in snap_params or not cp["options"]:
            continue
        if rs.is_media_role(name):
            continue                                 # compared under media_roles
        add(name, "param_missing_in_snapshot", f"cli enum={_fmt(cp['options'])}")

    s_aspect = {str(a) for a in item.get("aspect_ratios") or []}
    c_aspect = set(view["aspect_ratios"])
    if s_aspect != c_aspect:        # one-sided (a list vs none) disagrees too
        add("aspect_ratios", "aspect_ratios",
            f"snapshot-only={_fmt(s_aspect - c_aspect)} cli-only={_fmt(c_aspect - s_aspect)}")

    s_roles = {r for md in item.get("medias") or [] for r in (md.get("roles") or [])}
    c_roles = {n for n in cli_params if rs.is_media_role(n)}
    if s_roles != c_roles:
        add("media_roles", "media_roles",
            f"snapshot-only={_fmt(s_roles - c_roles)} cli-only={_fmt(c_roles - s_roles)}")
    return out


def crosscheck(snapshot: dict, output_type: str, catalog: list, get_payload) -> dict:
    """Compare every model present in both. `catalog` = CLI list rows already
    filtered to this type; `get_payload(id)` returns the raw `model get` JSON."""
    snap = {m["id"]: m for m in snapshot.get("items", [])
            if isinstance(m, dict) and m.get("output_type") == output_type}
    cli_ids = {rs._model_id(r, "model list") for r in catalog}
    shared = sorted(set(snap) & cli_ids)
    problems = []
    for mid in shared:
        problems.extend(compare_model(snap[mid], get_payload(mid)))
    return {"type": output_type, "checked": shared,
            "snapshot_only": sorted(set(snap) - cli_ids),
            "cli_only": sorted(cli_ids - set(snap)), "problems": problems}


def load_allowlist(path: Path = None) -> list:
    """Entries, validated: every entry names model, field, kind, a YYYY-MM-DD
    `seen` date and the observed `detail`. A malformed list is a usage error."""
    path = path or ALLOWLIST_PATH
    if not path.exists():
        return []
    doc = json.loads(path.read_text(encoding="utf-8"))
    entries = doc.get("entries")
    if not isinstance(entries, list):
        raise ValueError(f"{path.name}: `entries` must be a list")
    for i, e in enumerate(entries):
        missing = [k for k in _ALLOW_KEYS if not (isinstance(e, dict) and e.get(k))]
        if missing:
            raise ValueError(f"{path.name} entry {i}: missing {', '.join(missing)} "
                             f"(every entry names model, field, kind, seen date, detail)")
        if not _DATE_RE.match(str(e["seen"])):
            raise ValueError(f"{path.name} entry {i}: seen={e['seen']!r} is not YYYY-MM-DD")
    return entries


def apply_allowlist(problems: list, entries: list, types_checked: set) -> tuple:
    """(blocking, allowed, stale). A problem is allowed only when model, field,
    kind AND detail all match an entry; an entry for a checked model that
    matches nothing is stale."""
    key = lambda d: (d["model"], d["field"], d["kind"])  # noqa: E731
    by_key = {key(e): e for e in entries}
    blocking, allowed, used = [], [], set()
    for p in problems:
        e = by_key.get(key(p))
        if e and e["detail"] == p["detail"]:
            allowed.append((p, e))
            used.add(key(p))
        elif e:
            blocking.append(dict(p, allowlisted_detail=e["detail"]))
            used.add(key(p))
        else:
            blocking.append(p)
    stale = [e for e in entries if key(e) not in used and e["model"] in types_checked]
    return blocking, allowed, stale


# ── CLI sources ─────────────────────────────────────────────────────────────

def _live_source(output_type: str):
    rows = rs._cli_json(rs._list_args(output_type))
    if not isinstance(rows, list):
        raise rs.ShapeError("model list: expected a JSON array")
    if output_type not in rs._LIST_FLAG:
        rows = [r for r in rows if isinstance(r, dict) and r.get("type") == output_type]
    return rows, lambda mid: rs._cli_json(["model", "get", mid])


def _recorded_source(cli_dir: Path, output_type: str):
    rows = json.loads((cli_dir / "list_all.json").read_text(encoding="utf-8"))
    rows = [r for r in rows if isinstance(r, dict) and r.get("type") == output_type]
    return rows, lambda mid: json.loads((cli_dir / f"get_{mid}.json").read_text(encoding="utf-8"))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="scripts/snapshot_crosscheck.py",
                                 description=__doc__.splitlines()[3])
    ap.add_argument("--type", choices=(*sync_specs.TYPES, "all"), default="all")
    ap.add_argument("--cli-dir", type=Path, help="recorded CLI payloads instead of live calls")
    ap.add_argument("--snapshot", type=Path, help="explicit snapshot (single --type only)")
    ap.add_argument("--allowlist", type=Path, default=None)
    args = ap.parse_args(argv)
    types = sync_specs.TYPES if args.type == "all" else (args.type,)
    if args.snapshot and len(types) != 1:
        ap.error("--snapshot needs a single --type")

    try:
        entries = load_allowlist(args.allowlist)
    except (ValueError, json.JSONDecodeError) as e:
        print(f"ALLOWLIST INVALID: {e}", file=sys.stderr)
        return 2

    all_blocking, all_allowed, all_stale = [], [], []
    for t in types:
        try:
            snap_path = args.snapshot or sync_specs.find_snapshot(sync_specs.SPECS_DIR, t)
        except FileNotFoundError:
            print(f"[{t}] no snapshot — skipped")
            continue
        snapshot = json.loads(snap_path.read_text(encoding="utf-8"))
        try:
            rows, getter = (_recorded_source(args.cli_dir, t) if args.cli_dir
                            else _live_source(t))
            result = crosscheck(snapshot, t, rows, getter)
        except rs.ShapeError as e:
            print(f"[{t}] CLI SHAPE CHANGED: {e}", file=sys.stderr)
            return 3
        except rs.PullError as e:
            print(f"[{t}] PULL FAILED kind={e.kind}: {e}\n  → {rs.REMEDIES[e.kind]}",
                  file=sys.stderr)
            return 3
        blocking, allowed, stale = apply_allowlist(result["problems"], entries,
                                                   set(result["checked"]))
        source = f"recorded CLI ({args.cli_dir})" if args.cli_dir else "live CLI"
        print(f"[{t}] {snap_path.name} vs {source}: {len(result['checked'])} shared model(s); "
              f"snapshot-only {result['snapshot_only'] or '—'}; cli-only {result['cli_only'] or '—'}")
        for p in blocking:
            extra = (f"  (allowlisted detail was: {p['allowlisted_detail']})"
                     if "allowlisted_detail" in p else "")
            print(f"  ✗ DISAGREE {p['model']}.{p['field']} [{p['kind']}] {p['detail']}{extra}")
        for p, e in allowed:
            print(f"  · allowlisted (seen {e['seen']}) {p['model']}.{p['field']} "
                  f"[{p['kind']}] {p['detail']}")
        for e in stale:
            print(f"  · STALE allowlist entry — no longer disagrees, remove it: "
                  f"{e['model']}.{e['field']} [{e['kind']}] (seen {e['seen']})")
        all_blocking += blocking
        all_allowed += allowed
        all_stale += stale
    if all_blocking:
        print(f"\n{len(all_blocking)} unadjudicated CLI↔MCP disagreement(s). Decide per item: "
              "re-dump models_explore if the snapshot is wrong/incomplete, or add an "
              "allowlist entry (model, field, kind, seen, detail) if it is a known "
              "representation difference.")
        return 1
    print(f"\nsnapshot and CLI agree ({len(all_allowed)} allowlisted known difference(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
