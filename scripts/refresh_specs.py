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

WHAT THE SELF-DIFF WATCHES (v3.37.0 — before this, only the OLD view's
params were walked and only enum+default were kept, so a NEW param such as
seedance_2_5 `start_image`, a range/type change, or a `required` flip exited 0
"Fresh" — 8 models gained params between the 08-07 baseline and 09-26 unseen):
  - models added / removed from the catalog
  - params ADDED (a media role such as `start_image` / `mask` is reported as a
    media-role change) and params gone
  - enum options, defaults, `type`, `required`, `min` / `max`
  - CEL constraint rules (`rules`)
  Views carry `"view": 2`; a pre-v3.37 baseline (no marker) is still read —
  type/required/min/max are compared only when BOTH sides carry them, so an
  old baseline never false-alarms on a channel it never recorded.

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

3D MODELS
  The CLI has NO `model list --3d` flag (1.1.23: --image/--video/--audio/--text
  only). 3d rows are taken from the UNFILTERED `model list --json` by the row's
  own `type` field ("3d") — the CLI's classification, not a guess.

Usage:
  python3 scripts/refresh_specs.py --update-baseline   # bootstrap / accept current CLI
  python3 scripts/refresh_specs.py                      # self-diff vs baseline (default)
  python3 scripts/refresh_specs.py --type video         # one type (video|image|audio|3d)
  python3 scripts/refresh_specs.py --vs-snapshot        # legacy snapshot-diff
  python3 scripts/refresh_specs.py --json               # machine-readable diff
  python3 scripts/refresh_specs.py --status-json out.json   # CI: code/kind/line/remedy

Exit codes (the three states must stay distinguishable — a silent failure would
falsely read as "fresh", which is worse than the reactive WARN we already have):
  0  fresh — no change since baseline
  3  change detected — Tier 2 refresh + audit evals/cases/, then --update-baseline
  1  pull failed — the CLI could not answer. The failure is CLASSIFIED from the
     CLI's own stderr (kind=auth "Session expired" / kind=workspace "No
     workspace selected" / kind=missing-cli / kind=no-baseline / kind=empty —
     the CLI listed zero models of a type / kind=other) and the CLI line is
     carried through — REDACTED of anything that looks like an email, token or
     id, because CI posts it in a public issue — so CI names the right remedy
     instead of always blaming the credentials
  2  usage error
  4  CLI output shape changed — the CLI's JSON no longer matches what this script
     parses (e.g. the 1.0.1 `job_set_type`→`job_type` rename, a `rules: null`, a
     non-object payload); fix the parser, do NOT re-auth
  5  this script crashed (an unexpected Python exception — a local bug, not the
     CLI). Before v3.37.0 a crash exited 1 and read as "pull failed"

--update-baseline refuses an EMPTY pull (zero models of a type): accepting
it would make every later run "Fresh" against nothing. Each type's capture
date is kept in `captured_by_type` (a partial `--type video` re-capture no
longer re-dates the image/audio/3d views); `captured` is the OLDEST of them.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys

from sync_specs import SPECS_DIR, find_snapshot, snapshot_date

CLI = "higgsfield"
# Snapshot top-level fields that the CLI represents as parameters instead.
_ASPECT_PARAM = "aspect_ratio"
# Output types this tripwire covers. 3d has no CLI list flag (see module doc).
TYPES = ("video", "image", "audio", "3d")
_LIST_FLAG = {"video": "--video", "image": "--image", "audio": "--audio"}
# Shape marker for views written by this version (extended per-param fields).
VIEW_VERSION = 2
# The CLI represents media roles as PARAMS (`start_image`, `image_references`,
# `mask`, …); models_explore lists them as `medias[].roles`. A param whose name
# matches is a media role — its arrival/departure is reported as such.
MEDIA_ROLE_RE = re.compile(
    r"^(?:mask|image|video|audio|start_image|end_image|input_\w+|\w+_references?)$")
# Extended per-param fields compared only when both views are VIEW_VERSION 2.
_EXTENDED_FIELDS = ("type", "required", "min", "max")
# Committed last-accepted CLI state. The self-diff compares CLI-now against THIS
# (apples-to-apples, same source), so a persistent CLI↔models_explore
# disagreement — baked into the baseline once — never cries wolf again.
BASELINE_PATH = SPECS_DIR / "cli_baseline.json"


class PullError(RuntimeError):
    """The live pull failed (CLI missing, not authenticated, no workspace, bad
    JSON). Kept distinct from "drift" so the exit code can stay loud.

    `kind` classifies the failure from the CLI's own words (see
    classify_cli_failure) and `line` carries the verbatim CLI line, so the
    remedy printed downstream matches the actual failure — 10 weekly CI runs
    said "expired session" while the CLI was saying "No workspace selected."."""

    def __init__(self, message: str, kind: str = "other", line: str = ""):
        super().__init__(message)
        self.kind = kind
        self.line = line


# Remedy per failure kind — one table, used by the CLI report, the status
# JSON, and (via --status-json) the spec-drift workflow's ::error:: line.
REMEDIES = {
    "auth": "the CLI session expired or is not logged in — run "
            "`higgsfield auth login` locally, then update the "
            "HIGGSFIELD_CREDENTIALS repo secret from "
            "~/.config/higgsfield/credentials.json",
    "workspace": "the CLI has no workspace selected — run "
                 "`higgsfield workspace list`, then `higgsfield workspace set "
                 "<id>` locally; in CI set the HIGGSFIELD_WORKSPACE_ID repo "
                 "secret so the workflow selects it before the pull",
    "missing-cli": "install the Higgsfield CLI "
                   "(brew install higgsfield-ai/tap/higgsfield)",
    "no-baseline": "bootstrap the baseline: python3 scripts/refresh_specs.py "
                   "--update-baseline (after a reviewed Tier 2 refresh)",
    "shape": "the CLI's JSON output shape changed — update the parser in "
             "scripts/refresh_specs.py (ShapeError sites), verify locally, and "
             "bump LAST_VERIFIED_CLI + CLI_SHA256 in .github/workflows/"
             "spec-drift.yml. Do NOT rotate credentials",
    "empty": "the CLI listed zero models of this type — a partial or failed "
             "listing (wrong workspace? CLI outage?), never an accepted state; "
             "rerun, and do not accept it as the baseline",
    "crash": "refresh_specs.py itself crashed (a local bug, not the CLI) — "
             "read the traceback, fix the script; do NOT re-auth",
    "other": "unrecognized CLI failure — read the verbatim CLI line and fix "
             "that cause; do not assume an auth problem",
}


def classify_cli_failure(text: str) -> str:
    """Map the CLI's stderr to a failure kind. Workspace is checked first: its
    message ("Error: No workspace selected.") carries no auth words, but an
    auth message may mention a workspace in passing."""
    t = (text or "").lower()
    if "no workspace selected" in t or re.search(r"workspace\b.*\b(select|not found|required)", t):
        return "workspace"
    if any(s in t for s in ("session expired", "not logged in", "not authenticated",
                            "unauthorized", "unauthenticated", "auth login",
                            "token expired", "invalid token", "login required")):
        return "auth"
    return "other"


_REDACTIONS = (
    (re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"), "<email>"),
    (re.compile(r"\beyJ[\w-]+\.[\w-]+(?:\.[\w-]+)?"), "<token>"),        # JWT
    (re.compile(r"(?i)\b(bearer|basic)\s+[^\s)\]\"',;]+"), r"\1 <token>"),
    (re.compile(r"(?i)\b(token|secret|password|passwd|api[_-]?key|key|session|"
                r"credential|auth)(\s*[=:]\s*)[^\s)\]\"',;]+"), r"\1\2<redacted>"),
    (re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
                r"[0-9a-fA-F]{12}\b"), "<id>"),                              # UUID
    (re.compile(r"\b[0-9a-fA-F]{16,}\b"), "<id>"),                          # long hex
    (re.compile(r"\b(?=[A-Za-z0-9+/=-]*\d)[A-Za-z0-9+/=-]{24,}"), "<token>"),  # base64-ish
    (re.compile(r"\b\d{6,}\b"), "<id>"),                                    # numeric id
)


def redact(text: str) -> str:
    """The CLI line with anything that looks like an email, token or id
    replaced. The spec-drift workflow quotes this line in a PUBLIC issue and
    job log; the classified kind + remedy carry the meaning, the line is
    only corroboration. Model ids (snake_case words) survive."""
    out = text or ""
    for rx, repl in _REDACTIONS:
        out = rx.sub(repl, out)
    return out


def _verbatim_line(text: str) -> str:
    """The CLI line worth quoting: the first line that says error/expired/
    workspace, else the first non-empty line."""
    lines = [l.strip() for l in (text or "").splitlines() if l.strip()]
    for l in lines:
        if re.search(r"error|expired|workspace|denied|unauthori", l, re.IGNORECASE):
            return l
    return lines[0] if lines else ""


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


def is_media_role(name: str) -> bool:
    return bool(MEDIA_ROLE_RE.match(name or ""))


def snapshot_view(item: dict) -> dict:
    """Comparable view of one committed-snapshot model (the tracked shape).

    `source: snapshot` — its param set is NOT the CLI's (models_explore keeps
    aspect ratios and media roles outside `parameters`), so diff_model never
    counts a CLI-only param as "added" against it; the structural two-way
    comparison lives in scripts/snapshot_crosscheck.py."""
    return {
        "id": item["id"],
        "source": "snapshot",
        "output_type": item.get("output_type"),
        "aspect_ratios": _opts(item.get("aspect_ratios")),
        "params": {
            p["name"]: {"options": _opts(p.get("options")),
                        "default": p.get("default")}
            for p in item.get("parameters", [])
        },
    }


def _shape(ok: bool, what: str):
    if not ok:
        raise ShapeError(f"model get: {what} — CLI output shape changed; "
                         f"update refresh_specs.py")


def cli_view(get_json) -> dict:
    """Comparable view of one `higgsfield model get` payload. The CLI calls the
    enum list `enum` (snapshot says `options`) and carries aspect ratios as an
    `aspect_ratio` param rather than a top-level field — normalize both away.

    Every structural surprise is a ShapeError (exit 4), never a TypeError /
    AttributeError that the caller would misfile as a failed pull (exit 1):
    a non-object payload, `params`/`rules` that are not lists (`rules: null`),
    a param without a name, an `enum` that is not a list."""
    _shape(isinstance(get_json, dict),
           f"payload is {type(get_json).__name__}, expected an object")
    raw_params = get_json.get("params", [])
    _shape(isinstance(raw_params, list),
           f"`params` is {type(raw_params).__name__}, expected a list")
    params = {}
    for p in raw_params:
        _shape(isinstance(p, dict) and isinstance(p.get("name"), str),
               f"param entry {str(p)[:60]!r} is not an object with a name")
        enum = p.get("enum")
        _shape(enum is None or isinstance(enum, list),
               f"param {p['name']!r} enum is {type(enum).__name__}, expected a list")
        params[p["name"]] = p
    raw_rules = get_json.get("rules", [])
    _shape(isinstance(raw_rules, list),
           f"`rules` is {type(raw_rules).__name__}, expected a list")
    rules = []
    for r in raw_rules:
        _shape(isinstance(r, dict) and (r.get("cel") or r.get("message")),
               f"rule entry {str(r)[:60]!r} has neither `cel` nor `message`")
        rules.append(str(r.get("cel") or r.get("message")))
    aspect = params.get(_ASPECT_PARAM, {})
    view_params = {}
    for name, p in params.items():
        vp = {"options": _opts(p.get("enum")), "default": p.get("default"),
              "type": p.get("type"), "required": p.get("required")}
        for bound in ("min", "max"):   # absent today; tracked the day they appear
            if p.get(bound) is not None:
                vp[bound] = p[bound]
        view_params[name] = vp
    return {
        "id": _model_id(get_json, "model get"),
        "view": VIEW_VERSION,
        "output_type": get_json.get("type"),
        "aspect_ratios": _opts(aspect.get("enum")),
        "params": view_params,
        # CLI 1.0.1 dropped per-param `enum` lists but added machine-readable
        # CEL constraint rules — the cross-constraint prose this tool was
        # historically blind to. Track them as their own comparison channel.
        "rules": sorted(rules),
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
    confirm. Returns {"drift": [...], "notice": [...]}.

    Params are walked over the UNION of both sides (the pre-v3.37 loop walked
    only the old side, so a new param was invisible). A param the new side
    adds is DRIFT — `media_role_added` when it names a media role — but only
    when both views come from the same source (both CLI): against a
    models_explore snapshot view the CLI always "adds" aspect_ratio and the
    media-role params, which is representation, not change. type / required
    / min / max are compared only when BOTH views are VIEW_VERSION 2, so a
    pre-v3.37 baseline never false-alarms on a channel it never recorded."""
    drift, notice = [], []
    aspect_added = [a for a in new["aspect_ratios"] if a not in old["aspect_ratios"]]
    aspect_gone = [a for a in old["aspect_ratios"] if a not in new["aspect_ratios"]]
    if aspect_added:
        drift.append({"kind": "aspect_ratios", "added": aspect_added})
    if aspect_gone:
        notice.append({"kind": "aspect_ratios_gone", "removed": aspect_gone})

    same_source = old.get("source", "cli") == new.get("source", "cli")
    extended = (old.get("view", 1) >= VIEW_VERSION and new.get("view", 1) >= VIEW_VERSION)
    if same_source:
        for pname in sorted(set(new["params"]) - set(old["params"])):
            np = new["params"][pname]
            entry = {"kind": "media_role_added" if is_media_role(pname) else "param_added",
                     "param": pname}
            for k in ("type", "required", "options", "default"):
                if np.get(k) not in (None, []):
                    entry[k] = np[k]
            drift.append(entry)

    for pname, op in old["params"].items():
        np = new["params"].get(pname)
        if np is None:
            notice.append({"kind": "media_role_removed" if (same_source and is_media_role(pname))
                           else "param_missing", "param": pname})
            continue
        if extended:
            for field in _EXTENDED_FIELDS:
                if op.get(field) != np.get(field):
                    drift.append({"kind": f"{field}_changed", "param": pname,
                                  "from": op.get(field), "to": np.get(field)})
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
        # Same source (CLI vs CLI baseline): a default that APPEARS or
        # DISAPPEARS is a change too — preflight fills omitted params from
        # the baseline's defaults. Across sources (snapshot vs CLI) one side
        # often simply does not state a default, so only a value change counts.
        if same_source:
            if op.get("default") != np.get("default"):
                drift.append({"kind": "default", "param": pname,
                              "from": op.get("default"), "to": np.get("default")})
        elif op["default"] is not None and np["default"] is not None \
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
        raise PullError(f"`{CLI}` CLI not found on PATH (brew install higgsfield-ai/tap/higgsfield)",
                        kind="missing-cli")
    proc = subprocess.run([CLI, *args, "--json"], capture_output=True, text=True)
    if proc.returncode != 0:
        text = "\n".join(x for x in (proc.stderr, proc.stdout) if x)
        line = redact(_verbatim_line(text)) or f"exit {proc.returncode}"
        raise PullError(f"`{CLI} {' '.join(args)}` failed: {line}",
                        kind=classify_cli_failure(text), line=line)
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        # A non-JSON answer on exit 0 is usually a login/workspace prompt or an
        # HTML error page — classify it like a failure so the remedy is right.
        line = redact(_verbatim_line(proc.stdout)) or str(e)
        raise PullError(f"`{CLI} {' '.join(args)}` returned non-JSON: {e}",
                        kind=classify_cli_failure(proc.stdout), line=line)


def _list_args(output_type: str) -> list:
    """`model list` argv for one type. 3d has no CLI flag — list everything and
    filter by the row's `type` (see pull_cli_views)."""
    flag = _LIST_FLAG.get(output_type)
    return ["model", "list", flag] if flag else ["model", "list"]


def pull_cli_views(output_type: str, ids: set = None) -> tuple:
    """Live CLI views, plus the catalog id→display_name map. `ids=None` pulls
    EVERY catalog model (the baseline self-diff wants the whole live surface);
    an id set restricts to those present (the snapshot-diff only needs tracked
    models). N+1 calls: one `model list`, one `model get` per target."""
    args = _list_args(output_type)
    ctx = " ".join(args[1:])
    catalog = _cli_json(args)
    if not isinstance(catalog, list):
        raise ShapeError(f"{ctx}: expected a JSON array, "
                         f"got {type(catalog).__name__} — update refresh_specs.py")
    for m in catalog:
        if not isinstance(m, dict):
            raise ShapeError(f"{ctx}: row {str(m)[:60]!r} is not an object — "
                             f"update refresh_specs.py")
    if output_type not in _LIST_FLAG:
        if any("type" not in m for m in catalog):
            raise ShapeError(f"{ctx}: rows carry no `type` field, so {output_type} "
                             f"models cannot be selected — update refresh_specs.py")
        catalog = [m for m in catalog if m.get("type") == output_type]
    if not catalog:
        # Zero models is never a real state of the catalog; accepted as a
        # baseline it made every later run "Fresh" against nothing.
        raise PullError(f"{ctx}: the CLI listed zero {output_type} models", kind="empty",
                        line=f"`{CLI} {' '.join(args)} --json` returned an empty "
                             f"{output_type} list")
    catalog_ids = {mid: m.get("display_name", mid)
                   for m in catalog
                   for mid in (_model_id(m, ctx),)}
    targets = set(catalog_ids) if ids is None else (ids & set(catalog_ids))
    views = {mid: cli_view(_cli_json(["model", "get", mid]))
             for mid in sorted(targets)}
    return views, catalog_ids


# ── Report + driver ──────────────────────────────────────────────────────────

def describe(mid: str, c: dict) -> list:
    """Human lines for one change record. Every kind diff_model can emit has a
    phrasing here, and an unknown kind still prints (as JSON) — a change that
    flips the exit code must never render as nothing."""
    k, p = c["kind"], c.get("param", "")
    if k == "options_added":
        return [f"{mid}.{p} gained {'/'.join(c['added'])}"]
    if k == "options_removed":
        return [f"{mid}.{p} dropped {'/'.join(c['removed'])}"]
    if k == "options_undetailed":
        return [f"{mid}.{p} options now undetailed"]
    if k == "aspect_ratios":
        return [f"{mid} aspect_ratios gained {'/'.join(c['added'])}"]
    if k == "aspect_ratios_gone":
        return [f"{mid} aspect_ratios dropped {'/'.join(c['removed'])}"]
    if k == "default":
        return [f"{mid}.{p} default {c['from']!r} → {c['to']!r}"]
    if k in ("param_added", "media_role_added"):
        what = "new media role" if k == "media_role_added" else "new param"
        extra = ", ".join(f"{f}={c[f]!r}" for f in ("type", "required", "options", "default")
                          if f in c)
        return [f"{mid} {what}: {p}" + (f" ({extra})" if extra else "")]
    if k == "param_missing":
        return [f"{mid}.{p} param gone"]
    if k == "media_role_removed":
        return [f"{mid} media role gone: {p}"]
    if k in ("type_changed", "required_changed", "min_changed", "max_changed"):
        return [f"{mid}.{p} {k[:-len('_changed')]} {c['from']!r} → {c['to']!r}"]
    if k == "rules_added":
        return [f"{mid} new constraint rule: {r}" for r in c["added"]]
    if k == "rules_removed":
        return [f"{mid} constraint rule gone: {r}" for r in c["removed"]]
    return [f"{mid}: {json.dumps(c, ensure_ascii=False)}"]


def render(output_type: str, snap_date: str, diff: dict, catalog_ids: dict,
           verbose: bool = False) -> str:
    lines = [f"[{output_type}] snapshot {snap_date} vs live CLI catalog"]
    for mid, d in diff["models_changed"].items():
        for c in d["drift"]:
            lines.extend(f"  ⚠ DRIFT — {t}" for t in describe(mid, c))
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
                notices.extend(describe(mid, c))
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
    """Pull every catalog model and snapshot the live CLI surface, dated per
    type. The views are what the self-diff compares. An empty pull raises
    PullError(kind="empty") in pull_cli_views — never accepted."""
    from datetime import date
    today = date.today().isoformat()
    out = {"captured_by_type": {}}
    for t in types:
        views, _ = pull_cli_views(t, ids=None)
        if not views:          # belt and braces: pull_cli_views already refuses
            raise PullError(f"no {t} models captured", kind="empty")
        out[t] = views
        out["captured_by_type"][t] = today
    return out


def merge_baseline(old: dict, fresh: dict) -> dict:
    """The committed baseline with the freshly captured types replaced. Each
    type keeps its OWN capture date (`captured_by_type`); `captured` is the
    oldest one, so a partial re-capture never re-dates views it did not
    pull. A pre-v3.37 baseline (one global `captured`) seeds every type it
    carries with that date."""
    by_type = dict(old.get("captured_by_type") or
                   {t: old["captured"] for t in TYPES if t in old and old.get("captured")})
    by_type.update(fresh.get("captured_by_type") or {})
    merged = {"captured": min(by_type.values()) if by_type else None,
              "captured_by_type": {t: by_type[t] for t in TYPES if t in by_type}}
    for k, v in old.items():
        if k not in ("captured", "captured_by_type"):
            merged[k] = v
    for t in TYPES:
        if t in fresh:
            merged[t] = fresh[t]
    return merged


def render_self_diff(output_type: str, baseline: dict, diff: dict) -> str:
    when = (baseline.get("captured_by_type") or {}).get(output_type) \
        or baseline.get("captured", "?")
    lines = [f"[{output_type}] live CLI vs baseline ({when})"]
    for mid in diff["models_added"]:
        lines.append(f"  ⚠ CHANGED — new model in CLI: {mid}")
    for mid in diff["models_removed"]:
        lines.append(f"  ⚠ CHANGED — model gone from CLI: {mid}")
    for mid, d in diff["models_changed"].items():
        for c in d["drift"] + d["notice"]:
            lines.extend(f"  ⚠ CHANGED — {t}" for t in describe(mid, c))
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


def _status(code: int, state: str, kind: str = None, output_type: str = None,
            line: str = "", message: str = "") -> dict:
    """The machine-readable outcome (--status-json) the spec-drift workflow
    branches on: it quotes `line` verbatim in its ::error:: and prints
    `remedy`, so CI can never again blame credentials for a workspace error."""
    return {"code": code, "state": state, "kind": kind, "type": output_type,
            "line": line, "message": message,
            "remedy": REMEDIES.get(kind, "") if kind else ""}


def main(argv=None) -> int:
    """Exit-code wrapper: any unexpected exception is a CRASH (exit 5, state
    "crashed" in --status-json), never the pull-failed 1 a traceback used to
    exit with."""
    status_path = None
    if argv is None:
        argv = sys.argv[1:]
    for i, a in enumerate(argv):
        if a == "--status-json" and i + 1 < len(argv):
            status_path = argv[i + 1]
        elif a.startswith("--status-json="):
            status_path = a.split("=", 1)[1]
    try:
        return _main(argv)
    except Exception as e:  # noqa: BLE001 — classify, never misfile as a pull failure
        import traceback
        traceback.print_exc()
        print(f"CRASHED: {type(e).__name__}: {e}\n  → remedy: {REMEDIES['crash']}",
              file=sys.stderr)
        if status_path:
            from pathlib import Path
            try:
                Path(status_path).write_text(json.dumps(
                    _status(5, "crashed", "crash", None, "", f"{type(e).__name__}: {e}"),
                    indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            except OSError:
                pass
        return 5


def _main(argv=None) -> int:
    p = argparse.ArgumentParser(
        prog="scripts/refresh_specs.py", description=__doc__.splitlines()[0])
    p.add_argument("--type", choices=(*TYPES, "both", "all"),
                   default="all",
                   help="'all' = video+image+audio+3d (default); "
                        "'both' = video+image (pre-audio alias)")
    p.add_argument("--json", action="store_true", help="machine-readable diff")
    p.add_argument("--verbose", action="store_true", help="list every param-level notice")
    p.add_argument("--update-baseline", action="store_true",
                   help="capture the current live CLI surface as the new baseline")
    p.add_argument("--vs-snapshot", action="store_true",
                   help="legacy mode: diff CLI vs the models_explore snapshot "
                        "(source-disagreement-prone)")
    p.add_argument("--status-json", metavar="PATH",
                   help="also write {code,state,kind,type,line,remedy} to PATH "
                        "(the spec-drift workflow reads it)")
    args = p.parse_args(argv)
    types = {"all": TYPES, "both": ("video", "image")}.get(args.type, (args.type,))

    def finish(st: dict) -> int:
        if args.status_json:
            from pathlib import Path
            Path(args.status_json).write_text(
                json.dumps(st, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return st["code"]

    def pull_failed(e: PullError, t: str = None) -> int:
        tag = f" [{t}]" if t else ""
        print(f"PULL FAILED{tag} kind={e.kind}: {e}", file=sys.stderr)
        if e.line:
            print(f"  CLI said: {e.line}", file=sys.stderr)
        print(f"  → remedy: {REMEDIES[e.kind]}", file=sys.stderr)
        print("  → not fresh, not changed — the live state is unknown.", file=sys.stderr)
        return finish(_status(1, "pull-failed", e.kind, t, e.line, str(e)))

    def shape_changed(e: ShapeError, t: str = None) -> int:
        tag = f" [{t}]" if t else ""
        print(f"CLI SHAPE CHANGED{tag}: {e}", file=sys.stderr)
        print("  → not fresh, not changed — the parser is blind until "
              "refresh_specs.py is updated for the new CLI output.", file=sys.stderr)
        return finish(_status(4, "shape-changed", "shape", t, "", str(e)))

    # --update-baseline: bootstrap / accept the current live surface.
    if args.update_baseline:
        try:
            fresh = capture_baseline(types)
        except ShapeError as e:
            return shape_changed(e)
        except PullError as e:
            return pull_failed(e)
        merged = merge_baseline(load_baseline(), fresh)
        BASELINE_PATH.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n",
                                 encoding="utf-8")
        counts = ", ".join(f"{t} {len(fresh[t])}" for t in types)
        print(f"baseline updated for {', '.join(types)} → {BASELINE_PATH.name} "
              f"({counts} model(s); captured {', '.join(sorted(set(fresh['captured_by_type'].values())))})")
        return finish(_status(0, "baseline-updated"))

    baseline = {} if args.vs_snapshot else load_baseline()
    if not args.vs_snapshot and not baseline:
        return pull_failed(PullError(f"no baseline yet ({BASELINE_PATH.name} missing)",
                                     kind="no-baseline"))

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
            return shape_changed(e, t)
        except PullError as e:
            return pull_failed(e, t)
        except FileNotFoundError as e:
            return pull_failed(PullError(str(e), kind="no-baseline"), t)
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
    return finish(_status(3, "changed") if changed else _status(0, "fresh"))


if __name__ == "__main__":
    sys.exit(main())
