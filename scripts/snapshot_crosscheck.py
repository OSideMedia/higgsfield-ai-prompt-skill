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

and, per type, CATALOG MEMBERSHIP: a model only one source lists
(`snapshot-only` — in the models_explore dump, absent from `model list`;
`cli-only` — the reverse) fails like any other disagreement.

Known disagreements live in specs/crosscheck_allowlist.json — each structural
entry names the model, field, kind, the date it was seen, AND the observed
detail; a membership entry names the model, kind (snapshot-only | cli-only),
type, seen date and a note saying why. An allowlisted disagreement is still
PRINTED; if its detail changes it fails again (the allowlist accepts one
observed fact, not a class of future ones); an entry that no longer disagrees
— or whose model was never compared — is reported as stale.

NOTHING COMPARED IS NOT AGREEMENT. A type with no snapshot, or with zero
models present in both sources (an empty `model list`, 3d rows without a
`type`), is UNCHECKED and the run exits 3 — "0 shared, agree" was a pass on
an unchecked subject.

Usage:
  python3 scripts/snapshot_crosscheck.py                    # every type, live CLI
  python3 scripts/snapshot_crosscheck.py --type image
  python3 scripts/snapshot_crosscheck.py --cli-dir DIR      # recorded payloads:
        DIR/list_all.json (unfiltered `model list --json`) + DIR/get_<id>.json

Exit codes: 0 agree (allowlisted items printed), 1 disagreement,
            2 usage / bad allowlist, 3 could not compare (CLI pull or shape,
            a type with no snapshot or zero shared models).
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
# Catalog-membership kinds: a model only one source lists.
MEMBERSHIP_KINDS = ("snapshot-only", "cli-only")
_MEMBERSHIP_KEYS = ("model", "kind", "type", "seen", "note")
_MEMBERSHIP_DETAIL = {
    "snapshot-only": "in the models_explore snapshot, absent from `model list`",
    "cli-only": "in `model list`, absent from the models_explore snapshot",
}


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
    snapshot_only = sorted(set(snap) - cli_ids)
    cli_only = sorted(cli_ids - set(snap))
    for kind, ids in (("snapshot-only", snapshot_only), ("cli-only", cli_only)):
        for mid in ids:
            problems.append({"model": mid, "field": "membership", "kind": kind,
                             "type": output_type, "detail": _MEMBERSHIP_DETAIL[kind]})
    return {"type": output_type, "checked": shared, "snapshot_only": snapshot_only,
            "cli_only": cli_only, "known": sorted(set(snap) | cli_ids),
            "problems": problems}


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
        if isinstance(e, dict) and e.get("kind") in MEMBERSHIP_KINDS:
            missing = [k for k in _MEMBERSHIP_KEYS if not e.get(k)]
            if missing:
                raise ValueError(f"{path.name} entry {i}: missing {', '.join(missing)} "
                                 f"(a membership entry names model, kind, type, seen "
                                 f"date, and a note saying why)")
            if e["type"] not in sync_specs.TYPES:
                raise ValueError(f"{path.name} entry {i}: type={e['type']!r} is not one of "
                                 f"{', '.join(sync_specs.TYPES)}")
        else:
            missing = [k for k in _ALLOW_KEYS if not (isinstance(e, dict) and e.get(k))]
            if missing:
                raise ValueError(f"{path.name} entry {i}: missing {', '.join(missing)} "
                                 f"(every entry names model, field, kind, seen date, detail)")
        if not _DATE_RE.match(str(e["seen"])):
            raise ValueError(f"{path.name} entry {i}: seen={e['seen']!r} is not YYYY-MM-DD")
    return entries


def _is_membership(e: dict) -> bool:
    return e.get("kind") in MEMBERSHIP_KINDS


def apply_allowlist(problems: list, entries: list, types_checked: set) -> tuple:
    """(blocking, allowed, stale) for ONE type's problems. A structural
    problem is allowed only when model, field, kind AND detail all match an
    entry; a membership problem when model, kind and type match. A
    structural entry for a checked model that matches nothing is stale;
    membership entries are judged per type by stale_membership()."""
    key = lambda d: (d["model"], d["field"], d["kind"])  # noqa: E731
    by_key = {key(e): e for e in entries if not _is_membership(e)}
    by_member = {(e["model"], e["kind"], e["type"]): e for e in entries if _is_membership(e)}
    blocking, allowed, used = [], [], set()
    for p in problems:
        if p["kind"] in MEMBERSHIP_KINDS:
            e = by_member.get((p["model"], p["kind"], p["type"]))
            if e:
                allowed.append((p, e))
            else:
                blocking.append(p)
            continue
        e = by_key.get(key(p))
        if e and e["detail"] == p["detail"]:
            allowed.append((p, e))
            used.add(key(p))
        elif e:
            blocking.append(dict(p, allowlisted_detail=e["detail"]))
            used.add(key(p))
        else:
            blocking.append(p)
    stale = [e for e in entries if not _is_membership(e) and key(e) not in used
             and e["model"] in types_checked]
    return blocking, allowed, stale


def stale_membership(entries: list, result: dict) -> list:
    """Membership entries of this type whose model is no longer one-sided."""
    side = {"snapshot-only": set(result["snapshot_only"]),
            "cli-only": set(result["cli_only"])}
    return [e for e in entries if _is_membership(e) and e["type"] == result["type"]
            and e["model"] not in side[e["kind"]]]


def never_checked(entries: list, checked: set, known: set, all_types: bool) -> list:
    """Structural entries whose model was not compared this run: it is known
    to one source only (so nothing structural can disagree), or — when every
    type ran — to neither. Such an entry vouches for nothing: stale."""
    out = []
    for e in entries:
        if _is_membership(e) or e["model"] in checked:
            continue
        if e["model"] in known or all_types:
            out.append(e)
    return out


# ── CLI sources ─────────────────────────────────────────────────────────────

def _rows_of_type(rows, output_type: str, context: str) -> list:
    """Rows of one type, selected by the row's own `type`. A row that is not
    an object, or an unfiltered list whose rows carry no `type`, is a CLI
    shape change — filtering it would silently leave zero rows."""
    if not isinstance(rows, list):
        raise rs.ShapeError(f"{context}: expected a JSON array")
    for r in rows:
        if not isinstance(r, dict) or "type" not in r:
            raise rs.ShapeError(f"{context}: row {str(r)[:60]!r} is not an object with a "
                                f"`type` — {output_type} models cannot be selected")
    return [r for r in rows if r.get("type") == output_type]


def _live_source(output_type: str):
    rows = rs._cli_json(rs._list_args(output_type))
    if output_type not in rs._LIST_FLAG:
        rows = _rows_of_type(rows, output_type, "model list")
    elif not isinstance(rows, list):
        raise rs.ShapeError("model list: expected a JSON array")
    return rows, lambda mid: rs._cli_json(["model", "get", mid])


def _recorded_source(cli_dir: Path, output_type: str):
    rows = json.loads((cli_dir / "list_all.json").read_text(encoding="utf-8"))
    rows = _rows_of_type(rows, output_type, "list_all.json")
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

    all_blocking, all_allowed, all_stale, unchecked = [], [], [], []
    checked_ids, known_ids = set(), set()
    for t in types:
        try:
            snap_path = args.snapshot or sync_specs.find_snapshot(sync_specs.SPECS_DIR, t)
        except FileNotFoundError:
            print(f"[{t}] ? UNCHECKED — no {t} snapshot in specs/, nothing compared")
            unchecked.append(f"{t}: no snapshot")
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
        checked_ids |= set(result["checked"])
        known_ids |= set(result["known"])
        blocking, allowed, stale = apply_allowlist(result["problems"], entries,
                                                   set(result["checked"]))
        stale += stale_membership(entries, result)
        source = f"recorded CLI ({args.cli_dir})" if args.cli_dir else "live CLI"
        print(f"[{t}] {snap_path.name} vs {source}: {len(result['checked'])} shared model(s); "
              f"snapshot-only {result['snapshot_only'] or '—'}; cli-only {result['cli_only'] or '—'}")
        if not result["checked"]:
            print(f"  ? UNCHECKED — zero models are in both sources, so nothing "
                  f"structural was compared for {t}")
            unchecked.append(f"{t}: 0 shared models")
        for p in blocking:
            extra = (f"  (allowlisted detail was: {p['allowlisted_detail']})"
                     if "allowlisted_detail" in p else "")
            print(f"  ✗ DISAGREE {p['model']}.{p['field']} [{p['kind']}] {p['detail']}{extra}")
        for p, e in allowed:
            if p["kind"] in MEMBERSHIP_KINDS:
                print(f"  · allowlisted (seen {e['seen']}) {p['model']} [{p['kind']}] "
                      f"— {e['note']}")
            else:
                print(f"  · allowlisted (seen {e['seen']}) {p['model']}.{p['field']} "
                      f"[{p['kind']}] {p['detail']}")
        all_blocking += blocking
        all_allowed += allowed
        all_stale += stale
    all_stale += [e for e in never_checked(entries, checked_ids, known_ids,
                                           all_types=set(types) == set(sync_specs.TYPES))
                  if e not in all_stale]
    for e in all_stale:
        what = (f"{e['model']} [{e['kind']}] ({e['type']})" if _is_membership(e)
                else f"{e['model']}.{e['field']} [{e['kind']}]")
        why = ("its model was not compared this run" if not _is_membership(e)
               and e["model"] not in checked_ids else "no longer disagrees")
        print(f"  · STALE allowlist entry — {why}, remove it: {what} (seen {e['seen']})")
    if all_blocking:
        print(f"\n{len(all_blocking)} unadjudicated CLI↔MCP disagreement(s). Decide per item: "
              "re-dump models_explore if the snapshot is wrong/incomplete, or add an "
              "allowlist entry (model, field, kind, seen, detail — or, for catalog "
              "membership, model, kind, type, seen, note) if it is a known "
              "representation difference.")
        return 1
    if unchecked:
        print(f"\nUNCHECKED — nothing was compared for: {'; '.join(unchecked)}. "
              "Not a pass: dump the missing snapshot / fix the CLI listing, then rerun.")
        return 3
    print(f"\nsnapshot and CLI agree ({len(all_allowed)} allowlisted known difference(s), "
          f"{len(checked_ids)} model(s) compared).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
