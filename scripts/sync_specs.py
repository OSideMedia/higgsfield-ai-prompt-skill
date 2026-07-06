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
  specs/models_explore_snapshot_<YYYY-MM-DD>.json   (verbatim MCP tool output)

Outputs (all generated — never hand-edit):
  specs/model-specs.yaml   canonical record per model (the contract other
                           docs cite; HARD RULES #3/#7 point here)
  specs/model-specs.json   byte-deterministic machine twin of the yaml —
                           consumers (validate.py, seedance_lint.py) read this
                           with stdlib json instead of growing a YAML parser
  specs/MODEL-SPECS.md     human-readable table, stamped with snapshot date

Usage:
  python3 scripts/sync_specs.py            # regenerate from the newest snapshot
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

GENERATOR_VERSION = 1

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


def find_snapshot(specs_dir: Path = SPECS_DIR, output_type: str = "video") -> Path:
    """Newest snapshot by the date embedded in the filename."""
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


def normalize_models(snapshot: dict, output_type: str = "video") -> list[dict]:
    items = [m for m in snapshot.get("items", [])
             if m.get("output_type") == output_type]
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
            duration = {"min": m["duration_range"]["min"],
                        "max": m["duration_range"]["max"]}
        elif m.get("durations"):
            duration = {"values": sorted(m["durations"])}
        else:
            # 2026-07 snapshots moved the envelope into a `duration` PARAMETER
            # (min/max or options) — derive it so downstream duration-legality
            # checks (seedance_lint duration-out-of-range) keep working.
            dp = next((p for p in m.get("parameters", [])
                       if p.get("name") == "duration"), None)
            if dp and dp.get("min") is not None and dp.get("max") is not None:
                duration = {"min": dp["min"], "max": dp["max"]}
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
                {k: p[k] for k in
                 ("name", "required", "type", "description", "default", "options",
                  "min", "max")
                 if k in p}
                for p in m.get("parameters", [])
            ],
            "constraints": extract_constraints(m),
        })
    return models


def build_spec(snapshot_path: Path, output_type: str = "video") -> dict:
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
        image_snapshots = sorted(SPECS_DIR.glob("models_explore_snapshot_image_*.json"))
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
    stem = {"video": "model-specs", "image": "image-model-specs",
            "audio": "audio-model-specs"}.get(otype, "model-specs")
    lines += [
        "",
        f"Full per-model parameter schemas live in `specs/{stem}.yaml` / "
        f"`specs/{stem}.json`.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[2])
    parser.add_argument("--check", action="store_true",
                        help="verify generated files match the snapshot; write nothing")
    parser.add_argument("--snapshot", type=Path, default=None,
                        help="explicit snapshot path (default: newest in specs/)")
    parser.add_argument("--type", choices=("video", "image", "audio"), default="video",
                        help="which models_explore snapshot type to sync "
                             "(image/audio require a models_explore_snapshot_"
                             "<type>_<date>.json dump — nothing is fabricated "
                             "without one)")
    args = parser.parse_args()

    try:
        snapshot_path = args.snapshot or find_snapshot(output_type=args.type)
        spec = build_spec(snapshot_path, output_type=args.type)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        if args.type in ("image", "audio"):
            print(f"Typed snapshots are dumped, never fabricated: dump "
                  f"`models_explore` (action=list, type={args.type}) verbatim "
                  f"into specs/models_explore_snapshot_{args.type}_"
                  f"<YYYY-MM-DD>.json, then rerun.", file=sys.stderr)
        return 1
    except (ValueError, json.JSONDecodeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    out_paths = {
        "video": (YAML_OUT, JSON_OUT, MD_OUT),
        "image": (IMAGE_YAML_OUT, IMAGE_JSON_OUT, IMAGE_MD_OUT),
        "audio": (AUDIO_YAML_OUT, AUDIO_JSON_OUT, AUDIO_MD_OUT),
    }[args.type]
    outputs = {
        out_paths[0]: emit_yaml(spec),
        out_paths[1]: emit_json(spec),
        out_paths[2]: emit_markdown(spec),
    }

    if args.check:
        stale = [p for p, content in outputs.items()
                 if not p.exists() or p.read_text(encoding="utf-8") != content]
        if stale:
            for p in stale:
                print(f"STALE: {p.relative_to(ROOT)}", file=sys.stderr)
            print("specs out of date — rerun: python3 scripts/sync_specs.py", file=sys.stderr)
            return 1
        print(f"specs in sync with {snapshot_path.name} "
              f"({len(spec['models'])} models)")
        return 0

    SPECS_DIR.mkdir(parents=True, exist_ok=True)
    for p, content in outputs.items():
        p.write_text(content, encoding="utf-8")
        print(f"wrote {p.relative_to(ROOT)}")
    print(f"{len(spec['models'])} models from {snapshot_path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
