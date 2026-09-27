#!/usr/bin/env python3
"""
sync_specs.py
=============
Regenerate the machine-readable model specs layer from a `models_explore`
snapshot dump (Higgsfield MCP, action=list). Stdlib only.

The specs layer exists because hand-maintained model tables drift from the
live platform (model-guide.md shipped "Seedance 2.0 — 10s" while the live API
said 4-15s). Every model fact in specs/ comes from the snapshot JSON — this
script normalizes, it never invents.

Inputs:
  specs/models_explore_snapshot_<YYYY-MM-DD>.json          (video)
  specs/models_explore_snapshot_<type>_<YYYY-MM-DD>.json   (image|audio|3d)
  — each the verbatim MCP tool output. A paginated PARTIAL dump
  (`has_more: true`) is refused: specs generated from page 1 silently drop
  every model on the later pages.

Outputs (all generated — never hand-edit):
  specs/model-specs.yaml   canonical record per model (the contract other
                           docs cite; HARD RULES #3/#7 point here)
  specs/model-specs.json   byte-deterministic machine twin of the yaml —
                           consumers (validate.py, seedance_lint.py) read this
                           with stdlib json instead of growing a YAML parser
  specs/MODEL-SPECS.md     human-readable table, stamped with snapshot date
  (image-/audio-/3d-model-specs.{yaml,json} + IMAGE-/AUDIO-/3D-MODEL-SPECS.md
  for the other types)
  specs/retired-model-ids.json  APPEND-ONLY tombstones: every id the committed
                           snapshot history has seen that no current spec
                           carries. Generation-ledger rows written under a
                           since-retired id stay valid history through it.

Usage:
  python3 scripts/sync_specs.py            # regenerate from the newest snapshot
  python3 scripts/sync_specs.py --type 3d  # video|image|audio|3d
  python3 scripts/sync_specs.py --check    # verify outputs match the snapshot (CI)

Exit codes: 0 ok, 1 drift/--check failure or bad snapshot, 2 usage.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # scripts/ → repo root
SPECS_DIR = ROOT / "specs"
YAML_OUT = SPECS_DIR / "model-specs.yaml"
JSON_OUT = SPECS_DIR / "model-specs.json"
MD_OUT = SPECS_DIR / "MODEL-SPECS.md"
# Image-side outputs (Brief #2 item 9). Generated ONLY once a type=image
# snapshot (models_explore_snapshot_image_<date>.json) is committed — this
# script never fabricates image-model facts in the meantime.
IMAGE_YAML_OUT = SPECS_DIR / "image-model-specs.yaml"
IMAGE_JSON_OUT = SPECS_DIR / "image-model-specs.json"
IMAGE_MD_OUT = SPECS_DIR / "IMAGE-MODEL-SPECS.md"

AUDIO_YAML_OUT = SPECS_DIR / "audio-model-specs.yaml"
AUDIO_JSON_OUT = SPECS_DIR / "audio-model-specs.json"
AUDIO_MD_OUT = SPECS_DIR / "AUDIO-MODEL-SPECS.md"

THREED_YAML_OUT = SPECS_DIR / "3d-model-specs.yaml"
THREED_JSON_OUT = SPECS_DIR / "3d-model-specs.json"
THREED_MD_OUT = SPECS_DIR / "3D-MODEL-SPECS.md"

TYPES = ("video", "image", "audio", "3d")
# Per-type output file names (relative to a specs dir). One table so every
# consumer — --check, validate.py, higgsfield_memory — agrees on the set.
_OUTPUT_NAMES = {
    "video": ("model-specs.yaml", "model-specs.json", "MODEL-SPECS.md"),
    "image": ("image-model-specs.yaml", "image-model-specs.json", "IMAGE-MODEL-SPECS.md"),
    "audio": ("audio-model-specs.yaml", "audio-model-specs.json", "AUDIO-MODEL-SPECS.md"),
    "3d": ("3d-model-specs.yaml", "3d-model-specs.json", "3D-MODEL-SPECS.md"),
}
RETIRED_FILE = "retired-model-ids.json"

# Snapshot parameter keys carried into the specs. `nullable` joined in
# v3.37.0: it is the only field that separates "optional, no default, null is
# legal" (e.g. seedance_2_5 extension_mode, gpt_image_2_5 background) from
# "optional with a default" — a settings-legality consumer (the preflight
# linter, a ledger field check) needs it. `format` / `pattern` appeared once
# (08-07) and are gone from the 09-26 dumps, so they stay out: not widened
# blindly.
PARAM_KEYS = ("name", "required", "type", "description", "default", "options",
              "min", "max", "nullable")

GENERATOR_VERSION = 1


def output_paths(output_type: str, specs_dir: Path = None) -> tuple:
    """(yaml, json, md) paths for one type."""
    d = specs_dir or SPECS_DIR
    return tuple(d / name for name in _OUTPUT_NAMES[output_type])

# Snapshot entries that are alternate routes to the SAME model. The duplicate
# is folded into the canonical record's `aliases` after verifying its enums
# are identical (a divergent duplicate is a data problem, not an alias).
ALIAS_MAP = {
    "video_standard": "seedance_2_0",
}

# Historical catalog ids that upstream RENAMED (old id no longer in the
# snapshot, so ALIAS_MAP's same-snapshot folding can't see it). Folded into
# each model's `aliases` so ledger rows and user inputs written under the old
# id keep resolving (higgsfield_memory + seedance_lint resolve via aliases).
HISTORICAL_IDS = {
    "seedance1_5": ["seedance_1_5"],       # renamed in the 2026-07-05 catalog
    "recraft_v4_1": ["recraft-v4-1"],      # renamed in the 2026-07-05 catalog
    "seedance_2_0": ["video_standard"],    # dup id dropped from the 2026-07-05 catalog
}

# Mode/param constraints are extracted ONLY when a parameter description
# explicitly states them AND the named value is a legal enum value elsewhere
# in the same model — prose that can't be anchored to real enum values is
# reported to stderr, never guessed into the spec.
NOT_SUPPORT_RE = re.compile(
    r"(?:does\s*not|doesn't|cannot|can\s*not|not)\s+support\s+['\"]?([\w:.]+)['\"]?",
    re.IGNORECASE)
# Complement form: "supports 480p/720p only" means the option forbids every
# OTHER enum value of the referenced parameter. Deriving from the allowed list
# (not a hard-coded forbidden list) keeps the constraint correct when the enum
# grows — e.g. Seedance gaining `4k` is auto-forbidden under `fast`.
SUPPORTS_ONLY_RE = re.compile(
    r"supports?\s+([\w:.]+(?:\s*/\s*[\w:.]+)*)\s+only", re.IGNORECASE)
REQUIRES_RE = re.compile(
    r"['\"]?([\w:.]+)['\"]?\s+requires\s+(\w+)\s*=\s*['\"]?([\w:.]+)['\"]?",
    re.IGNORECASE)


def find_snapshot(specs_dir: Path = None, output_type: str = "video") -> Path:
    """Newest snapshot by the date embedded in the filename."""
    specs_dir = specs_dir or SPECS_DIR
    pattern = ("models_explore_snapshot_*.json" if output_type == "video"
               else f"models_explore_snapshot_{output_type}_*.json")
    candidates = sorted(specs_dir.glob(pattern))
    # The unprefixed pattern would also match typed snapshots — exclude them.
    if output_type == "video":
        candidates = [c for c in candidates
                      if re.fullmatch(r"models_explore_snapshot_\d{4}-\d{2}-\d{2}\.json", c.name)]
    if not candidates:
        raise FileNotFoundError(
            f"no {output_type} snapshot found in {specs_dir} "
            f"(expected {pattern}; dump `models_explore` action=list type={output_type})")
    return candidates[-1]


def snapshot_date(path: Path) -> str:
    m = re.search(r"(\d{4}-\d{2}-\d{2})\.json$", path.name)
    if not m:
        raise ValueError(f"snapshot filename must end with _<YYYY-MM-DD>.json: {path.name}")
    return m.group(1)


def _param_options(model: dict, name: str) -> list:
    for p in model.get("parameters", []):
        if p.get("name") == name:
            return list(p.get("options") or [])
    return []


def _enum_signature(model: dict) -> tuple:
    """The facts that must match for two entries to be one model."""
    return (
        tuple(model.get("aspect_ratios") or []),
        tuple((p.get("name"), tuple(p.get("options") or []))
              for p in model.get("parameters", [])),
        json.dumps(model.get("duration_range") or model.get("durations"), sort_keys=True),
    )


def extract_constraints(model: dict) -> list[dict]:
    """Pull explicitly-stated cross-parameter constraints out of descriptions.

    Two recognized phrasings:
      "'fast' = ... does not support 1080p"   -> mode_constraint (forbids)
      "1080p requires duration=8."            -> value_requires
    A captured token must be a legal enum value of another parameter (or, for
    requires-duration, a plain integer) or the sentence is skipped with a
    stderr warning — constraints are never inferred."""
    constraints: list[dict] = []
    all_options = {p.get("name"): list(p.get("options") or [])
                   for p in model.get("parameters", [])}

    for p in model.get("parameters", []):
        desc = p.get("description") or ""
        options = list(p.get("options") or [])

        # Forbids-form, attributed to the option whose quoted segment names it.
        for opt in options:
            seg_match = re.search(
                rf"['\"]{re.escape(str(opt))}['\"]\s*=\s*([^'\"]*)", desc)
            if not seg_match:
                continue
            for m in NOT_SUPPORT_RE.finditer(seg_match.group(1)):
                token = m.group(1)
                for other_name, other_opts in all_options.items():
                    if other_name != p["name"] and token in other_opts:
                        constraints.append({
                            "param": p["name"],
                            "value": str(opt),
                            "forbids": {other_name: [token]},
                            "source": f"{p['name']} description: "
                                      f"'{opt}' does not support {token}",
                        })
                        break
                else:
                    print(f"  WARN [{model['id']}] unmapped not-support claim "
                          f"for '{opt}': {token!r}", file=sys.stderr)

            # Complement form: "supports 480p/720p only" → forbid the rest.
            for m in SUPPORTS_ONLY_RE.finditer(seg_match.group(1)):
                allowed = [t.strip() for t in m.group(1).split("/") if t.strip()]
                for other_name, other_opts in all_options.items():
                    if other_name == p["name"] or not other_opts:
                        continue
                    if allowed and all(a in other_opts for a in allowed):
                        forbidden = [o for o in other_opts if o not in allowed]
                        if forbidden:
                            constraints.append({
                                "param": p["name"],
                                "value": str(opt),
                                "forbids": {other_name: forbidden},
                                "source": f"{p['name']} description: "
                                          f"'{opt}' supports {'/'.join(allowed)} only",
                            })
                        break

        # Requires-form on the parameter's own values.
        for m in REQUIRES_RE.finditer(desc):
            value, req_param, req_value = (
                m.group(1).rstrip("."), m.group(2), m.group(3).rstrip("."))
            if value not in [str(o) for o in options]:
                print(f"  WARN [{model['id']}] unmapped requires claim: "
                      f"{m.group(0)!r}", file=sys.stderr)
                continue
            constraints.append({
                "param": p["name"],
                "value": value,
                "requires": {req_param: req_value},
                "source": f"{p['name']} description: {m.group(0)}",
            })
    return constraints


_DESC_RANGE_RE = re.compile(r"\((\d+)\s*[-–]\s*(\d+)\)")


def _duration_envelope(model_id: str, lo, hi, description: str) -> dict:
    """{"min", "max"} — or, for a NEGATIVE floor (a sentinel, not a length),
    {"min", "max", "smart"}. wan3_0 ships `min: -1` meaning "the model picks
    the length (billed as 10s)", legal values -1 or 2–30; `-1–30s` would claim
    0 and 1 are legal. The real floor is taken ONLY from the description's
    own "(lo-hi)" range, and only when that range ends at the declared max and
    the description names the sentinel — otherwise the raw value is kept and
    the gap is reported, never guessed."""
    if lo is None or hi is None or lo >= 0:
        return {"min": lo, "max": hi}
    desc = description or ""
    m = _DESC_RANGE_RE.search(desc)
    names_sentinel = re.search(rf"(?<![\d.]){re.escape(str(lo))}(?!\d)", desc)
    if m and names_sentinel and int(m.group(2)) == hi and int(m.group(1)) > lo:
        return {"min": int(m.group(1)), "max": hi, "smart": lo}
    print(f"  WARN [{model_id}] duration min={lo} is a sentinel but the real floor "
          f"cannot be derived from its description — kept raw; fix the parser or "
          f"the snapshot", file=sys.stderr)
    return {"min": lo, "max": hi}


def normalize_models(snapshot: dict, output_type: str = "video") -> list[dict]:
    # A snapshot with no items — or none of the requested type — is a broken
    # dump (truncated file, wrong action, wrong type), never a valid state of
    # the platform. Writing empty specs from it would silently blind every
    # downstream enum check, so fail loudly instead.
    if not isinstance(snapshot.get("items"), list) or not snapshot["items"]:
        raise ValueError(
            "snapshot has no 'items' list — not a models_explore dump "
            "(truncated file or wrong payload); refusing to generate specs")
    # A paginated dump that stopped on page 1 looks valid (items present) but
    # silently drops every later model. Only an explicit `has_more: false` is
    # a complete catalog: every committed models_explore dump carries the key,
    # so a dump WITHOUT it is hand-trimmed or not a list response — refused
    # like a partial one (an absent key used to pass as "complete").
    if "has_more" not in snapshot or snapshot["has_more"] is not False:
        raise ValueError(
            f"snapshot is not a complete models_explore list (has_more: "
            f"{snapshot.get('has_more', '<absent>')!r}) — fetch every page of "
            "`models_explore` (action=list) and dump the complete list verbatim "
            "(it ends with has_more: false); refusing to generate specs")
    items = [m for m in snapshot["items"]
             if m.get("output_type") == output_type]
    if not items:
        raise ValueError(
            f"snapshot contains no output_type={output_type!r} models — "
            "wrong --type or a partial dump; refusing to generate specs")
    by_id = {m["id"]: m for m in items}

    # Fold aliases into canonical entries (after equivalence check).
    aliases: dict[str, list[str]] = {}
    for alias, canonical in ALIAS_MAP.items():
        if alias not in by_id:
            continue
        if canonical not in by_id:
            raise ValueError(f"alias {alias} maps to missing canonical {canonical}")
        if _enum_signature(by_id[alias]) != _enum_signature(by_id[canonical]):
            raise ValueError(
                f"snapshot entries {alias} and {canonical} are mapped as aliases "
                f"but their enums differ — fix ALIAS_MAP or the snapshot")
        aliases.setdefault(canonical, []).append(alias)
        del by_id[alias]

    models = []
    for mid in sorted(by_id):
        m = by_id[mid]
        if m.get("duration_range"):
            duration = _duration_envelope(mid, m["duration_range"]["min"],
                                          m["duration_range"]["max"],
                                          m["duration_range"].get("description", ""))
        elif m.get("durations"):
            duration = {"values": sorted(m["durations"])}
        else:
            # 2026-07 snapshots moved the envelope into a `duration` PARAMETER
            # (min/max or options) — derive it so downstream duration-legality
            # checks (seedance_lint duration-out-of-range) keep working.
            dp = next((p for p in m.get("parameters", [])
                       if p.get("name") == "duration"), None)
            if dp and dp.get("min") is not None and dp.get("max") is not None:
                duration = _duration_envelope(mid, dp["min"], dp["max"],
                                              dp.get("description", ""))
            elif dp and dp.get("options"):
                duration = {"values": sorted(dp["options"])}
            else:
                duration = None
        models.append({
            "id": mid,
            "aliases": sorted(set(aliases.get(mid, [])) | set(HISTORICAL_IDS.get(mid, []))),
            "name": m.get("name", mid),
            "provider": m.get("provider_name", ""),
            "output_type": output_type,
            "resolutions": _param_options(m, "resolution"),
            "modes": _param_options(m, "mode"),
            "aspect_ratios": list(m.get("aspect_ratios") or []),
            "duration": duration,
            "media_roles": {e.get("name", "medias"): list(e.get("roles") or [])
                            for e in m.get("medias", [])},
            "params": [
                {k: p[k] for k in PARAM_KEYS if k in p}
                for p in m.get("parameters", [])
            ],
            "constraints": extract_constraints(m),
        })
    return models


def build_spec(snapshot_path: Path, output_type: str = "video",
               specs_dir: Path = None) -> dict:
    specs_dir = specs_dir or SPECS_DIR
    raw = snapshot_path.read_bytes()
    snapshot = json.loads(raw)
    date = snapshot_date(snapshot_path)
    spec = {
        "generator_version": GENERATOR_VERSION,
        "snapshot_date": date,
        "snapshot_file": snapshot_path.name,
        "snapshot_sha256": hashlib.sha256(raw).hexdigest(),
        "models": normalize_models(snapshot, output_type),
    }
    if output_type == "video":
        # The image-side marker lives in the video spec. It was a TODO until a
        # type=image snapshot existed (Brief #2 item 9); once one is committed
        # it flips to a pointer at the generated image specs.
        image_snapshots = sorted(specs_dir.glob("models_explore_snapshot_image_*.json"))
        if image_snapshots:
            img_date = re.search(r"(\d{4}-\d{2}-\d{2})", image_snapshots[-1].name)
            stamp = img_date.group(1) if img_date else date
            spec["image_models"] = (
                f"see specs/IMAGE-MODEL-SPECS.md (snapshot {stamp}); "
                "this file covers video models only.")
        else:
            spec["image_models"] = (
                f"TODO ({date}) — pending a type=image models_explore snapshot; "
                "video models only below. Do not cite this file for image-model facts.")
    return spec


# ── Emitters (deterministic; YAML writer covers exactly the shapes above) ───

_YAML_PLAIN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 _./+-]*$")


def _yscalar(v) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    if _YAML_PLAIN.fullmatch(s) and s.lower() not in {
            "null", "true", "false", "yes", "no", "on", "off"}:
        return s
    return json.dumps(s, ensure_ascii=False)  # JSON quoting is valid YAML


def _yemit(value, indent: int, lines: list[str]):
    pad = "  " * indent
    if isinstance(value, dict):
        if not value:
            lines[-1] += " {}"
            return
        for k, v in value.items():
            if isinstance(v, (dict, list)) and v:
                lines.append(f"{pad}{_yscalar(k)}:")
                _yemit(v, indent + 1, lines)
            else:
                if isinstance(v, (dict, list)):  # empty container
                    lines.append(f"{pad}{_yscalar(k)}: " + ("{}" if isinstance(v, dict) else "[]"))
                else:
                    lines.append(f"{pad}{_yscalar(k)}: {_yscalar(v)}")
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, (dict, list)) and item:
                lines.append(f"{pad}-")
                sub: list[str] = []
                _yemit(item, indent + 1, sub)
                # Hoist the first child onto the dash line for readability.
                first = sub[0].lstrip()
                lines[-1] = f"{pad}- {first}"
                lines.extend(sub[1:])
            else:
                lines.append(f"{pad}- {_yscalar(item) if not isinstance(item, (dict, list)) else ('{}' if isinstance(item, dict) else '[]')}")
    else:
        lines.append(f"{pad}{_yscalar(value)}")


def emit_yaml(spec: dict) -> str:
    lines = [
        "# GENERATED by scripts/sync_specs.py — DO NOT HAND-EDIT.",
        f"# Source: specs/{spec['snapshot_file']} (models_explore dump, "
        f"{spec['snapshot_date']}).",
        "# Regenerate: python3 scripts/sync_specs.py   Verify: python3 scripts/sync_specs.py --check",
    ]
    _yemit(spec, 0, lines)
    return "\n".join(lines) + "\n"


def emit_json(spec: dict) -> str:
    return json.dumps(spec, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _fmt_duration(d) -> str:
    if d is None:
        return "—"
    if "values" in d:
        return "/".join(str(v) for v in d["values"]) + "s"
    if "smart" in d:
        return f"{d['min']}–{d['max']}s or {d['smart']} (smart)"
    return f"{d['min']}–{d['max']}s"


def emit_markdown(spec: dict) -> str:
    lines = [
        "# Model Specs (generated)",
        "",
        f"**Snapshot: {spec['snapshot_date']}** · source `specs/{spec['snapshot_file']}` · "
        "regenerated by `scripts/sync_specs.py` — **do not hand-edit**.",
        "",
    ]
    if spec.get("image_models"):
        lines += [f"Image models: {spec['image_models']}", ""]
    lines += [
        "| Model | id (aliases) | Duration | Resolutions | Modes | Aspect ratios | Media roles | Constraints |",
        "|-------|--------------|----------|-------------|-------|---------------|-------------|-------------|",
    ]
    for m in spec["models"]:
        ident = m["id"] + (f" ({', '.join(m['aliases'])})" if m["aliases"] else "")
        roles = "; ".join(f"{k}: {', '.join(v)}" if v else k
                          for k, v in m["media_roles"].items()) or "—"
        cons = "; ".join(
            (f"{c['param']}={c['value']} forbids "
             + ", ".join(f"{p} {'/'.join(vals)}" for p, vals in c["forbids"].items()))
            if "forbids" in c else
            (f"{c['param']}={c['value']} requires "
             + ", ".join(f"{p}={v}" for p, v in c["requires"].items()))
            for c in m["constraints"]) or "—"
        lines.append(
            f"| {m['name']} | {ident} | {_fmt_duration(m['duration'])} "
            f"| {', '.join(m['resolutions']) or '—'} | {', '.join(m['modes']) or '—'} "
            f"| {', '.join(m['aspect_ratios']) or '—'} | {roles} | {cons} |")
    otype = spec["models"][0]["output_type"] if spec["models"] else "video"
    stem = _OUTPUT_NAMES.get(otype, _OUTPUT_NAMES["video"])[1][:-len(".json")]
    lines += [
        "",
        f"Full per-model parameter schemas live in `specs/{stem}.yaml` / "
        f"`specs/{stem}.json`.",
        "",
    ]
    return "\n".join(lines)


def render_outputs(spec: dict, output_type: str, specs_dir: Path = None) -> dict:
    """{path: content} for one type's three generated files."""
    y, j, m = output_paths(output_type, specs_dir)
    return {y: emit_yaml(spec), j: emit_json(spec), m: emit_markdown(spec)}


# ── Retired-id tombstones (append-only) ─────────────────────────────────────

_RETIRED_DOC = (
    "GENERATED + APPEND-ONLY by scripts/sync_specs.py — never edit by hand. "
    "Every model id that some committed models_explore snapshot carried and no "
    "type's NEWEST snapshot (nor any alias) carries. Generation-ledger rows "
    "written under a since-retired id stay valid history through this list "
    "(scripts/higgsfield_memory.py load_specs_models); new rows may not use "
    "a retired id. Each entry must be PROVEN by the snapshot history: an id "
    "no committed snapshot carried, or one live again in a newest snapshot, "
    "is dropped by the generator and fails validate.py until regenerated.")


def _snapshot_files(specs_dir: Path) -> list:
    return sorted(specs_dir.glob("models_explore_snapshot_*.json"),
                  key=lambda p: (snapshot_date(p), p.name))


# The fewest items a COMPLETE models_explore list dump of each type has ever
# had is far above these (video 18, image 23, audio 5, 3d 17 in the committed
# history); a "snapshot" below them is a fragment, not a catalog.
MIN_PROOF_ITEMS = {"video": 10, "image": 10, "audio": 3, "3d": 5}
_SNAPSHOT_NAME_RE = re.compile(
    r"^models_explore_snapshot_(?:(?P<type>[a-z0-9]+)_)?\d{4}-\d{2}-\d{2}\.json$")


def snapshot_type(path: Path) -> str | None:
    """The output type a snapshot filename declares (None: not a snapshot name)."""
    m = _SNAPSHOT_NAME_RE.match(Path(path).name)
    if not m:
        return None
    t = m.group("type") or "video"
    return t if t in TYPES else None


def dump_problem(path: Path) -> str | None:
    """Why a committed snapshot file is NOT a well-formed models_explore list
    dump of its type (None when it is). Only well-formed dumps count as
    history — they alone may derive or prove a retired-id tombstone.

    ponytail: the trust boundary is the committed, reviewed snapshot set —
    this checks a proving snapshot's SHAPE (a complete, typed list dump), not
    its provenance: CI checks out shallow, so git history cannot vouch for
    when a file was dumped, and a carefully forged full-size dump would pass.
    Upgrade path: a reviewed manifest of snapshot sha256s (or requiring the
    proving snapshot's commit to predate the tombstone) once CI fetches
    history."""
    otype = snapshot_type(path)
    if otype is None:
        return "filename is not models_explore_snapshot_[<type>_]<YYYY-MM-DD>.json"
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return f"unreadable: {e}"
    if not isinstance(data, dict):
        return f"root is {type(data).__name__}, not a models_explore list response"
    if "has_more" not in data or data["has_more"] is not False:
        return f"has_more is {data.get('has_more', '<absent>')!r}, not false — not a complete list"
    items = data.get("items")
    if not isinstance(items, list) or not items:
        return "no items list"
    for i, m in enumerate(items):
        if not (isinstance(m, dict) and isinstance(m.get("id"), str) and m["id"]
                and isinstance(m.get("name"), str)):
            return f"item {i} is not a model record with an id and a name"
        if m.get("output_type") != otype:
            return (f"item {m['id']!r} has output_type {m.get('output_type')!r} in a "
                    f"{otype} snapshot")
        params = m.get("parameters", [])
        if not isinstance(params, list) or any(
                not (isinstance(q, dict) and isinstance(q.get("name"), str)) for q in params):
            return f"item {m['id']!r} has malformed parameters"
    ids = [m["id"] for m in items]
    if len(set(ids)) != len(ids):
        return "duplicate model ids"
    if len(items) < MIN_PROOF_ITEMS[otype]:
        return (f"{len(items)} {otype} item(s) — below the {MIN_PROOF_ITEMS[otype]} a "
                f"complete {otype} catalog dump has; a fragment is not history")
    return None


def malformed_snapshots(specs_dir: Path = None) -> dict:
    """{snapshot name: problem} for committed snapshots that are not
    well-formed dumps (they prove nothing, and validate.py fails on them)."""
    out = {}
    for p in _snapshot_files(specs_dir or SPECS_DIR):
        why = dump_problem(p)
        if why:
            out[p.name] = why
    return out


def _history_snapshots(specs_dir: Path) -> list:
    """The committed snapshots that count as history: well-formed dumps only."""
    return [p for p in _snapshot_files(specs_dir) if dump_problem(p) is None]


def current_model_ids(specs_dir: Path = None) -> set:
    """Ids live NOW: every item of each type's NEWEST snapshot, plus every
    alias (ALIAS_MAP, HISTORICAL_IDS). Derived from the snapshots, never from
    the generated spec files — otherwise the answer would depend on which
    --type was synced first (a first-ever 3d sync would tombstone every live
    3d id when video is synced before it), and an append-only file would keep
    that mistake forever."""
    ids = set(ALIAS_MAP)
    for olds in HISTORICAL_IDS.values():
        ids.update(olds)
    for t in TYPES:
        try:
            snap = find_snapshot(specs_dir, t)
        except FileNotFoundError:
            continue
        ids.update(m["id"] for m in json.loads(snap.read_text(encoding="utf-8")).get("items") or []
                   if isinstance(m, dict) and m.get("id"))
    return ids


def compute_retired(specs_dir: Path = None) -> dict:
    """{id: {type, last_seen, last_snapshot}} derived from snapshot history."""
    specs_dir = specs_dir or SPECS_DIR
    current = current_model_ids(specs_dir)
    seen = {}
    for p in _history_snapshots(specs_dir):
        for m in json.loads(p.read_text(encoding="utf-8")).get("items") or []:
            if isinstance(m, dict) and m.get("id"):
                seen[m["id"]] = {"type": m.get("output_type"),
                                 "last_seen": snapshot_date(p),
                                 "last_snapshot": p.name}
    return {k: v for k, v in seen.items() if k not in current}


def load_retired(specs_dir: Path = None) -> dict:
    """The committed tombstones ({} when the file is absent)."""
    p = (specs_dir or SPECS_DIR) / RETIRED_FILE
    if not p.exists():
        return {}
    return dict(json.loads(p.read_text(encoding="utf-8")).get("retired") or {})


def snapshot_history_ids(specs_dir: Path = None) -> set:
    """Every model id a committed, WELL-FORMED models_explore dump carried
    (a one-line fake "snapshot" proves nothing — see dump_problem)."""
    ids = set()
    for p in _history_snapshots(specs_dir or SPECS_DIR):
        ids.update(m["id"] for m in json.loads(p.read_text(encoding="utf-8")).get("items") or []
                   if isinstance(m, dict) and m.get("id"))
    return ids


def unproven_tombstones(specs_dir: Path = None) -> dict:
    """{id: why} for committed tombstones the snapshot history does not
    prove. A tombstone whitelists its id in the ledger, so it must be
    EARNED: the id appeared in some committed snapshot AND no type's newest
    snapshot (nor an alias) carries it. A hand-added id used to pass every
    gate, because the staleness check started from the committed file."""
    committed = load_retired(specs_dir)
    if not committed:
        return {}
    history = snapshot_history_ids(specs_dir)
    current = current_model_ids(specs_dir)
    out = {}
    for mid in sorted(committed):
        if mid not in history:
            out[mid] = "no committed, well-formed models_explore snapshot ever carried it"
        elif mid in current:
            out[mid] = "it is live in a newest snapshot (or an alias) — not retired"
    return out


def merged_retired(specs_dir: Path = None) -> dict:
    """Proven committed tombstones ∪ newly derived ones. Proven entries are
    never removed or rewritten — the file only grows, like the ledger it
    protects; an unproven entry is never carried forward."""
    unproven = unproven_tombstones(specs_dir)
    merged = {k: v for k, v in load_retired(specs_dir).items() if k not in unproven}
    for mid, info in compute_retired(specs_dir).items():
        merged.setdefault(mid, info)
    return merged


def proven_retired(specs_dir: Path = None) -> dict:
    """The committed tombstones that the snapshot history proves — what the
    ledger may trust (a hand-added id is not in it)."""
    unproven = unproven_tombstones(specs_dir)
    return {k: v for k, v in load_retired(specs_dir).items() if k not in unproven}


def retired_problems(specs_dir: Path = None) -> list:
    """Human reasons the committed tombstone file is not what sync_specs
    would write: unproven entries, missing ids, a non-canonical file."""
    rp = (specs_dir or SPECS_DIR) / RETIRED_FILE
    if not rp.exists():
        return [f"{RETIRED_FILE} is missing"]
    probs = [f"unproven tombstone {mid!r}: {why}"
             for mid, why in unproven_tombstones(specs_dir).items()]
    probs += [f"snapshot {name} proves nothing: {why}"
              for name, why in malformed_snapshots(specs_dir).items()]
    missing = sorted(set(compute_retired(specs_dir)) - set(load_retired(specs_dir)))
    probs += [f"retired id {mid!r} is not tombstoned" for mid in missing]
    if not probs and rp.read_text(encoding="utf-8") != emit_retired(merged_retired(specs_dir)):
        probs.append(f"{RETIRED_FILE} is not in canonical generated form")
    return probs


def emit_retired(retired: dict) -> str:
    return json.dumps({"_doc": _RETIRED_DOC, "retired": retired},
                      indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def stale_outputs(output_type: str, specs_dir: Path = None,
                  snapshot_path: Path = None) -> tuple:
    """(snapshot path, [stale file names]) — regenerate `output_type` from its
    NEWEST snapshot (or `snapshot_path`) and compare with the committed files.
    The one comparison both `--check` and validate.py run. Raises
    FileNotFoundError / ValueError / json.JSONDecodeError on a missing or
    broken snapshot."""
    specs_dir = specs_dir or SPECS_DIR
    snap = snapshot_path or find_snapshot(specs_dir, output_type)
    spec = build_spec(snap, output_type, specs_dir)
    stale = [p.name for p, content in render_outputs(spec, output_type, specs_dir).items()
             if not p.exists() or p.read_text(encoding="utf-8") != content]
    return snap, stale


def retired_is_stale(specs_dir: Path = None) -> bool:
    """True when the committed tombstone file is missing an id the snapshot
    history says is retired, carries an unproven one, is absent / not in
    canonical form — or when a committed snapshot is not a well-formed dump
    (the history the tombstones rest on is then in doubt)."""
    rp = (specs_dir or SPECS_DIR) / RETIRED_FILE
    return (not rp.exists()
            or bool(malformed_snapshots(specs_dir))
            or rp.read_text(encoding="utf-8") != emit_retired(merged_retired(specs_dir)))


def _snapshots_of_type(specs_dir: Path, output_type: str) -> list:
    pattern = ("models_explore_snapshot_*.json" if output_type == "video"
               else f"models_explore_snapshot_{output_type}_*.json")
    files = sorted(specs_dir.glob(pattern), key=lambda p: (snapshot_date(p), p.name))
    if output_type == "video":
        files = [f for f in files
                 if re.fullmatch(r"models_explore_snapshot_\d{4}-\d{2}-\d{2}\.json", f.name)]
    return files


def changed_models(output_type: str, specs_dir: Path = None) -> dict:
    """Models added / removed / changed between the PREVIOUS and the NEWEST
    snapshot of one type (a model "changed" when its dumped record differs in
    any field). Feeds the Tier-2 evals audit (v3.11.3 lesson)."""
    specs_dir = specs_dir or SPECS_DIR
    files = _snapshots_of_type(specs_dir, output_type)
    if not files:
        raise FileNotFoundError(f"no {output_type} snapshot in {specs_dir}")
    load = lambda p: {m["id"]: m for m in json.loads(p.read_text(encoding="utf-8")).get("items") or []  # noqa: E731
                      if isinstance(m, dict) and m.get("id")}
    new = load(files[-1])
    old = load(files[-2]) if len(files) > 1 else {}
    same = sorted(set(new) & set(old))
    return {
        "previous": files[-2].name if len(files) > 1 else None,
        "newest": files[-1].name,
        "added": sorted(set(new) - set(old)),
        "removed": sorted(set(old) - set(new)),
        "changed": [m for m in same if json.dumps(new[m], sort_keys=True)
                    != json.dumps(old[m], sort_keys=True)],
        "names": {m: (new.get(m) or old.get(m) or {}).get("name", m)
                  for m in set(new) | set(old)},
    }


def evals_referencing(model_ids, names: dict = None, cases_dir: Path = None) -> dict:
    """{model_id: [eval case ids]} — cases whose JSON mentions the id (whole
    token: `seedance_2_5` never matches `seedance_2_5_mini`) or the model's
    display name (case-insensitive)."""
    cases_dir = cases_dir or ROOT / "evals" / "cases"
    names = names or {}
    hits = {m: [] for m in model_ids}
    for path in sorted(cases_dir.glob("*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        for case in doc.get("cases", []):
            text = json.dumps(case, ensure_ascii=False)
            for m in model_ids:
                needles = [rf"(?<![\w]){re.escape(m)}(?![\w])"]
                if names.get(m) and names[m] != m:
                    needles.append(rf"(?<![\w]){re.escape(names[m])}(?![\w])")
                if any(re.search(n, text, re.IGNORECASE) for n in needles):
                    hits[m].append(f"{path.name}:{case.get('id', '?')}")
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[2])
    parser.add_argument("--changed", action="store_true",
                        help="list models added/removed/changed between the previous "
                             "and newest snapshot of --type, and the evals/cases/ "
                             "entries that reference them; write nothing")
    parser.add_argument("--check", action="store_true",
                        help="verify generated files match the snapshot; write nothing")
    parser.add_argument("--snapshot", type=Path, default=None,
                        help="explicit snapshot path (default: newest in specs/)")
    parser.add_argument("--type", choices=TYPES, default="video",
                        help="which models_explore snapshot type to sync "
                             "(image/audio/3d require a models_explore_snapshot_"
                             "<type>_<date>.json dump — nothing is fabricated "
                             "without one)")
    args = parser.parse_args()

    if args.changed:
        try:
            ch = changed_models(args.type)
        except FileNotFoundError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1
        print(f"[{args.type}] {ch['previous'] or '(no previous snapshot)'} → {ch['newest']}")
        for label in ("added", "removed", "changed"):
            print(f"  {label}: {', '.join(ch[label]) or '—'}")
        touched = ch["added"] + ch["removed"] + ch["changed"]
        refs = evals_referencing(touched, ch["names"])
        cited = {m: c for m, c in refs.items() if c}
        print(f"  evals/cases/ entries referencing them: {sum(len(c) for c in cited.values())}")
        for m, cases in sorted(cited.items()):
            print(f"    {m}: {', '.join(cases)}")
        return 0

    try:
        snapshot_path = args.snapshot or find_snapshot(output_type=args.type)
        if args.check:
            snapshot_path, stale = stale_outputs(args.type, snapshot_path=snapshot_path)
            if retired_is_stale():
                stale.append(RETIRED_FILE)
            if stale:
                for name in stale:
                    print(f"STALE: specs/{name}", file=sys.stderr)
                print(f"specs out of date — rerun: python3 scripts/sync_specs.py "
                      f"--type {args.type}", file=sys.stderr)
                return 1
            n = len(json.loads(output_paths(args.type)[1].read_text(encoding="utf-8"))["models"])
            print(f"specs in sync with {snapshot_path.name} ({n} models)")
            return 0
        spec = build_spec(snapshot_path, output_type=args.type)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        if args.type != "video":
            print(f"Typed snapshots are dumped, never fabricated: dump "
                  f"`models_explore` (action=list, type={args.type}) verbatim "
                  f"into specs/models_explore_snapshot_{args.type}_"
                  f"<YYYY-MM-DD>.json, then rerun.", file=sys.stderr)
        return 1
    except (ValueError, json.JSONDecodeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    outputs = render_outputs(spec, args.type)
    retired_path = SPECS_DIR / RETIRED_FILE

    SPECS_DIR.mkdir(parents=True, exist_ok=True)
    for p, content in outputs.items():
        p.write_text(content, encoding="utf-8")
        print(f"wrote {p.relative_to(ROOT)}")
    # Tombstones AFTER the outputs: "current" must be the spec just written.
    before = load_retired()
    after = merged_retired()
    retired_path.write_text(emit_retired(after), encoding="utf-8")
    for mid in sorted(set(after) - set(before)):
        print(f"tombstoned retired id: {mid} (last seen {after[mid]['last_seen']})")
    print(f"{len(spec['models'])} models from {snapshot_path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
