#!/usr/bin/env python3
"""
higgsfield_memory.py
====================
Database read/write operations for the Higgsfield learning memory system.
Called by Claude Cowork via the higgsfield-recall skill.

Usage:
  python3 scripts/higgsfield_memory.py add-filter <json_entry>
  python3 scripts/higgsfield_memory.py add-quality <json_entry>
  python3 scripts/higgsfield_memory.py query-filter <search_terms>
  python3 scripts/higgsfield_memory.py query-quality <search_terms>
  python3 scripts/higgsfield_memory.py update-filter <entry_id> <outcome>
  python3 scripts/higgsfield_memory.py update-quality <entry_id> <outcome> [improved_prompt] [notes]
  python3 scripts/higgsfield_memory.py stats
  python3 scripts/higgsfield_memory.py export-summary
  python3 scripts/higgsfield_memory.py health

Generation ledger (db/ledger/ — see db/ledger/README.md):
  python3 scripts/higgsfield_memory.py log-gen <project> --model X --tags a,b --outcome kept
  python3 scripts/higgsfield_memory.py log-gen <project> '<json row>'
  python3 scripts/higgsfield_memory.py last-gen <project>
  python3 scripts/higgsfield_memory.py amend-gen <id> outcome=kept   # superseding row
  python3 scripts/higgsfield_memory.py ratio <project> [--model X] [--tag Y] [--global] [--credits]
  python3 scripts/higgsfield_memory.py ab <project> [--tag Y] [--global]   # prompt_method A/B
  python3 scripts/higgsfield_memory.py agreement <project> [--global]   # vision/human agreement

Routing telemetry (item 6 — which sub-skills opened per request):
  python3 scripts/higgsfield_memory.py log-route --skills higgsfield-prompt,higgsfield-camera
  python3 scripts/higgsfield_memory.py routing            # per-skill opens + long tail
  python3 scripts/higgsfield_memory.py budget <project> --shots <manifest.json|csv>

Per-project namespacing:
  python3 scripts/higgsfield_memory.py --project <name> <command> ...

  Routes every command to db/projects/<name>-filter-memory.json /
  <name>-quality-memory.json instead of the global databases, so
  production-specific lessons (e.g. one project's dual-instance character
  workaround) don't pollute global memory. Project DBs are created lazily on
  first write; reads from a missing project DB return empty results.
"""

import json
import os
import sys
import re
from datetime import datetime, timezone
from pathlib import Path

from sub_skill_descriptions import SUB_SKILL_DESCRIPTIONS  # canonical sub-skill roster

# ── Paths ──────────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent  # scripts/ → repo root
# DB files live under the repo root (db/), one level above scripts/.
# The directory is created lazily on first write (see save_db / export_summary),
# not at import time — importing this module should have no filesystem side effects.
# HF_DB_DIR overrides the location (tests point it at a temp dir; works both
# in-process and across subprocess boundaries, unlike monkeypatched constants).
DB_DIR = Path(os.environ["HF_DB_DIR"]) if os.environ.get("HF_DB_DIR") else REPO_ROOT / "db"
FILTER_DB = DB_DIR / "filter-memory.json"
QUALITY_DB = DB_DIR / "quality-memory.json"
# Item 6: which sub-skills the dispatcher opened per request. Instrumentation —
# the data that makes "find the load-bearing skills, prune the long tail"
# answerable instead of guessed. The pruning DECISION waits for real data.
ROUTING_DB = DB_DIR / "routing-log.json"
# Set by the --project CLI option: project-namespaced DBs are created lazily,
# so load_db treats a missing file as empty instead of erroring.
PROJECT_MODE = False

# Allowed outcome values, mirroring the inline documentation on add_filter /
# add_quality. update-* commands validate against these so a typo (e.g.
# "fixedd") can't silently flip every derived boolean to False.
FILTER_OUTCOMES = {"unknown", "fixed", "workaround", "still-blocked"}
QUALITY_OUTCOMES = {"unknown", "improved", "still-failing"}

# ── Helpers ────────────────────────────────────────────────────────────────────

def load_db(path: Path) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            db = json.load(f)
    except FileNotFoundError:
        if PROJECT_MODE:
            return {"entries": []}
        print(json.dumps({"status": "error", "message": f"Database file not found: {path}"}))
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(json.dumps({"status": "error", "message": f"Database file is corrupted: {e}"}))
        sys.exit(1)
    # Guarantee the shape every caller assumes: a dict with a list "entries".
    # A valid-JSON-but-wrong-shape file should fail the clean error contract,
    # not crash later with a raw KeyError/AttributeError traceback.
    if not isinstance(db, dict):
        print(json.dumps({"status": "error", "message": f"Database root is not a JSON object: {path}"}))
        sys.exit(1)
    entries = db.setdefault("entries", [])
    if not isinstance(entries, list):
        print(json.dumps({"status": "error", "message": f"Database 'entries' must be a list: {path}"}))
        sys.exit(1)
    return db

def save_db(path: Path, data: dict):
    data["_last_updated"] = datetime.now(timezone.utc).isoformat()
    data["_total_entries"] = len(data["entries"])
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(".tmp")
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        tmp_path.replace(path)  # atomic on POSIX, best-effort on Windows
    except OSError as e:
        tmp_path.unlink(missing_ok=True)
        print(json.dumps({"status": "error", "message": f"Failed to save database: {e}"}))
        sys.exit(1)

def next_id(entries: list, prefix: str) -> str:
    if not entries:
        return f"{prefix}-001"
    # Only count ids whose suffix is purely numeric. A hand-edited id like
    # "F-abc" (or any non-numeric suffix) is skipped rather than crashing the
    # whole add command with an uncaught ValueError.
    nums = []
    for e in entries:
        eid = e.get("id", "")
        if not eid.startswith(prefix):
            continue
        suffix = eid.split("-")[-1]
        if suffix.isdigit():
            nums.append(int(suffix))
    return f"{prefix}-{(max(nums) + 1):03d}" if nums else f"{prefix}-001"

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def tokenize(text: str) -> set:
    """Tokenizer for relevance matching. Preserves hyphenated phrases as whole tokens
    in addition to their individual parts (e.g. 'real-person' → {'real-person','real','person'})."""
    lower = text.lower()
    tokens = set(re.findall(r'\b[\w-]+\b', lower))  # includes hyphenated phrases
    # also add individual words from within hyphenated terms
    for token in list(tokens):
        if '-' in token:
            tokens.update(token.split('-'))
    return tokens

def relevance_score(entry: dict, query_tokens: set) -> int:
    """Score an entry against search tokens. Higher = more relevant."""
    text = " ".join([
        entry.get("failed_prompt", ""),
        entry.get("original_prompt", ""),
        entry.get("topic", ""),
        entry.get("error_message", ""),
        entry.get("failure_description", ""),
        entry.get("category", ""),
        " ".join(entry.get("tags", [])),
        " ".join(entry.get("blocked_terms", [])),
    ]).lower()
    entry_tokens = tokenize(text)
    return len(query_tokens & entry_tokens)


# ── Generation Ledger ──────────────────────────────────────────────────────────
# Empirical hit-rate system (Brief #3). Unlike the filter/quality memories
# (failure ledgers), this logs EVERY generation attempt — kept, rejected, or
# filter-flagged — so takes-per-kept ratios have a denominator. Rows are
# APPEND-ONLY: corrections are new rows with `supersedes`, never edits.
# Full schema + vocabulary docs: db/ledger/README.md.

LEDGER_DIR = DB_DIR / "ledger"
GLOBAL_LEDGER = LEDGER_DIR / "_global.json"
PROJECT_NAME_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*")
GEN_ID_RE = re.compile(r"^(.+)-(\d{4})$")

# Controlled vocabularies (extend via PR, never ad hoc — free-text tags
# fragment and kill aggregation).
SHOT_TAGS = {
    "establishing", "dialogue-cu", "dialogue-multi", "action-melee",
    "action-chase", "insert-prop", "vfx-event", "two-char",
    "multi-char-3plus", "dual-instance", "pov", "environment-only",
    "creature-occluded",
}
REJECT_REASONS = {
    "identity-drift", "wardrobe-contamination", "extra-cuts",
    "blocking-broken", "performance", "camera-wrong", "physics",
    "text-render", "filter-flagged", "composition", "other",
}
# The split that carries the diagnostic value: structural rejections mean
# "fix the prompt, don't re-roll"; stochastic mean "re-roll territory".
# `other` belongs to neither class (counts in n only).
STRUCTURAL_REASONS = {"identity-drift", "wardrobe-contamination", "extra-cuts",
                      "blocking-broken", "text-render", "filter-flagged"}
STOCHASTIC_REASONS = {"performance", "camera-wrong", "physics", "composition"}
OUTCOMES = {"kept", "rejected", "flagged"}
# Control arm for measuring framework lift: `quick` = naive/ad-hoc prompt,
# `mcsla` = full framework prompt. The field is OPTIONAL and has no default —
# absence means "unlabeled" and is excluded from the A/B comparison entirely
# (see compute_method_ab), so months of pre-field history can never masquerade
# as one arm. Extend via PR like every other vocab.
PROMPT_METHODS = {"quick", "mcsla"}

# Default planning ratios for budget estimates when the ledger has no usable
# data for a tag (n<5 or kept=0). These are DEFAULTS, NOT DATA — the brief's
# documented planning bands: 2-3:1 simple, 4-6:1 complex (midpoints used).
DEFAULT_RATIOS = {
    "establishing": 2.5, "dialogue-cu": 2.5, "insert-prop": 2.5,
    "environment-only": 2.5, "pov": 2.5,
    "dialogue-multi": 5.0, "action-melee": 5.0, "action-chase": 5.0,
    "vfx-event": 5.0, "multi-char-3plus": 5.0, "dual-instance": 5.0,
    "creature-occluded": 5.0,
    "two-char": 3.0,
}
LOW_N_THRESHOLD = 5
# Flag B (wasted-re-roll): minimum identical-prompt_hash cluster size before an
# all-structural, no-keeper cluster is called a wasted re-roll. Its own knob —
# a different concept from the ratio low-n guard, tuned independently.
WASTED_REROLL_MIN = 5
# Wave B (vision-grounded diagnosis): promotion gate for trusting a
# vision-proposed reject_reason WITHOUT human confirmation. Per reject_reason
# class, vision is trusted only once its agreement with confirmed human labels
# clears VISION_TRUST_MIN_AGREEMENT over at least VISION_AGREEMENT_MIN_N
# confirmed diagnoses (its own low-n guard — measure before trusting).
VISION_TRUST_MIN_AGREEMENT = 0.8
VISION_AGREEMENT_MIN_N = 8

_LEDGER_REQUIRED = {"id", "ts", "model", "shot_tags", "outcome", "draft_tier"}
_LEDGER_OPTIONAL = {"mode", "resolution", "aspect", "duration_s", "internal_cuts",
                    "scene_ref", "prompt_hash", "credits", "notes",
                    "supersedes", "reject_reason", "project", "prompt_method",
                    "vision_reason", "vision_evidence"}


def load_specs_models() -> dict:
    """{id_or_alias: canonical_id} from specs/model-specs.json.

    Ledger rows store CANONICAL ids only (aliases resolved at write time) so
    per-model credit averages can't fragment across an alias. Returns {} when
    the specs layer is missing — callers decide whether that's fatal."""
    path = REPO_ROOT / "specs" / "model-specs.json"
    try:
        spec = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    mapping: dict = {}
    for m in spec.get("models", []):
        mapping[m["id"]] = m["id"]
        for alias in m.get("aliases", []):
            mapping[alias] = m["id"]
    return mapping


def ledger_path(project: str) -> Path:
    if not PROJECT_NAME_RE.fullmatch(project):
        print(json.dumps({"status": "error",
                          "message": f"Invalid project name: {project!r} "
                                     "(alphanumeric, dash, underscore)"}))
        sys.exit(1)
    return LEDGER_DIR / f"{project}.json"


def load_ledger(path: Path) -> dict:
    """Ledger file shape: {project, _last_updated, _total_rows, rows}.
    A missing file is an empty ledger (projects bootstrap on first write)."""
    try:
        db = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"project": path.stem, "rows": []}
    except (OSError, json.JSONDecodeError) as e:
        print(json.dumps({"status": "error",
                          "message": f"Ledger file unreadable: {path}: {e}"}))
        sys.exit(1)
    if not isinstance(db, dict) or not isinstance(db.get("rows", []), list):
        print(json.dumps({"status": "error",
                          "message": f"Ledger file malformed (need dict with rows list): {path}"}))
        sys.exit(1)
    db.setdefault("project", path.stem)
    db.setdefault("rows", [])
    return db


def save_ledger(path: Path, db: dict):
    db["_last_updated"] = now_iso()
    db["_total_rows"] = len(db["rows"])
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(".tmp")
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=2, ensure_ascii=False)
        tmp_path.replace(path)
    except OSError as e:
        tmp_path.unlink(missing_ok=True)
        print(json.dumps({"status": "error", "message": f"Failed to save ledger: {e}"}))
        sys.exit(1)


def next_gen_id(project: str, rows: list) -> str:
    nums = []
    for r in rows:
        m = GEN_ID_RE.match(r.get("id", ""))
        if m and m.group(1) == project:
            nums.append(int(m.group(2)))
    return f"{project}-{(max(nums) + 1) if nums else 1:04d}"


def validate_ledger_row(row: dict, project: str, prior_ids: set,
                        superseded_ids: set, model_ids: dict) -> list:
    """Schema check for one row. Returns a list of problem strings.

    `prior_ids` = ids of rows EARLIER in the same file (supersedes may only
    point backward); `superseded_ids` = ids already masked by an earlier
    row's supersedes (each id is maskable at most once — amend an amendment
    by superseding the previous amendment, never the original twice)."""
    problems = []
    rid = row.get("id", "?")

    missing = _LEDGER_REQUIRED - set(row)
    if missing:
        problems.append(f"{rid}: missing required field(s): {', '.join(sorted(missing))}")
    unknown = set(row) - _LEDGER_REQUIRED - _LEDGER_OPTIONAL
    if unknown:
        problems.append(f"{rid}: unknown field(s): {', '.join(sorted(unknown))}")

    m = GEN_ID_RE.match(str(row.get("id", "")))
    if not m or m.group(1) != project:
        problems.append(f"{rid}: id must match '{project}-NNNN'")

    outcome = row.get("outcome")
    if outcome not in OUTCOMES:
        problems.append(f"{rid}: outcome must be one of {sorted(OUTCOMES)}, got {outcome!r}")

    tags = row.get("shot_tags")
    if not isinstance(tags, list):
        problems.append(f"{rid}: shot_tags must be a list")
    else:
        bad = [t for t in tags if t not in SHOT_TAGS]
        if bad:
            problems.append(f"{rid}: shot_tags not in vocabulary: {', '.join(bad)} "
                            f"(allowed: {', '.join(sorted(SHOT_TAGS))})")
        lo = 0 if outcome == "flagged" else 1
        if not lo <= len(tags) <= 3:
            problems.append(f"{rid}: shot_tags needs {lo}..3 entries, got {len(tags)}")

    model = row.get("model")
    if model_ids:
        if model not in model_ids:
            problems.append(f"{rid}: model {model!r} not in specs/model-specs.json")
        elif model_ids[model] != model:
            problems.append(f"{rid}: model {model!r} is an alias — store the "
                            f"canonical id {model_ids[model]!r}")

    if outcome == "rejected":
        reason = row.get("reject_reason")
        if reason not in REJECT_REASONS:
            problems.append(f"{rid}: rejected rows need reject_reason from "
                            f"{', '.join(sorted(REJECT_REASONS))}; got {reason!r}")
    elif row.get("reject_reason") is not None and outcome in OUTCOMES:
        problems.append(f"{rid}: reject_reason only belongs on rejected rows")

    if not isinstance(row.get("draft_tier"), bool):
        problems.append(f"{rid}: draft_tier must be true/false")

    pm = row.get("prompt_method")
    if pm is not None and pm not in PROMPT_METHODS:
        problems.append(f"{rid}: prompt_method must be one of "
                        f"{sorted(PROMPT_METHODS)} or absent (unlabeled); got {pm!r}")

    vr = row.get("vision_reason")
    if vr is not None and vr not in REJECT_REASONS:
        problems.append(f"{rid}: vision_reason must be a reject_reason value "
                        f"or absent; got {vr!r}")

    sup = row.get("supersedes")
    if sup is not None:
        if sup not in prior_ids:
            problems.append(f"{rid}: supersedes {sup!r} — no earlier row with that "
                            "id in this ledger (corrections point backward, same file)")
        elif sup in superseded_ids:
            problems.append(f"{rid}: supersedes {sup!r} which is already superseded — "
                            "amend the latest amendment instead")
    return problems


def resolve_effective(rows: list) -> list:
    """Append-only resolution: a row referenced by any supersedes is masked."""
    masked = {r.get("supersedes") for r in rows if r.get("supersedes")}
    return [r for r in rows if r.get("id") not in masked]


def project_ledger_files() -> list:
    """All real project ledgers. Underscore-prefixed names are reserved
    (_global generated view, _demo test fixture) and excluded."""
    if not LEDGER_DIR.is_dir():
        return []
    return sorted(p for p in LEDGER_DIR.glob("*.json")
                  if not p.name.startswith("_"))


def build_global() -> dict:
    """The _global.json view: raw rows from every project ledger, each
    annotated with its project. Generated, never hand-written; consumers
    re-run supersedes resolution (ids are project-prefixed, so masks
    cannot cross projects). Deterministic: filename order, then file order."""
    rows = []
    sources = []
    for path in project_ledger_files():
        db = load_ledger(path)
        sources.append(path.name)
        for r in db["rows"]:
            rows.append({**r, "project": db["project"]})
    return {
        "_generated": "by scripts/higgsfield_memory.py — DO NOT HAND-EDIT; "
                      "underscore-prefixed ledgers are excluded by design",
        "generated_from": sources,
        "_total_rows": len(rows),
        "rows": rows,
    }


def write_global():
    fresh = build_global()
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    tmp = GLOBAL_LEDGER.with_suffix(".tmp")
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(fresh, f, indent=2, ensure_ascii=False)
        tmp.replace(GLOBAL_LEDGER)
    except OSError as e:
        tmp.unlink(missing_ok=True)
        print(json.dumps({"status": "error", "message": f"Failed to write _global: {e}"}))
        sys.exit(1)


def _is_structural(row: dict) -> bool:
    """Per-row boolean (a flagged lint-bridge row counts once, never twice):
    structural = filter-flagged outcome OR a structural reject_reason."""
    return (row.get("outcome") == "flagged"
            or row.get("reject_reason") in STRUCTURAL_REASONS)


def _is_stochastic(row: dict) -> bool:
    return (row.get("outcome") == "rejected"
            and row.get("reject_reason") in STOCHASTIC_REASONS)


def compute_ratio(rows: list, model: str = None, tag: str = None) -> dict:
    """Takes-per-kept statistics over a ledger's rows (pure function).

    Operates on effective (supersedes-resolved) rows. draft_tier rows are
    excluded from the headline and groups and reported as one draft-burn
    line. Per-tag groups OVERLAP (a 2-tag row counts in both groups), so
    the headline n is the effective non-draft ROW count, never the group
    sum. All ratios are exact fractions here; round at display only."""
    eff = resolve_effective(rows)
    if model:
        eff = [r for r in eff if r.get("model") == model]
    if tag:
        eff = [r for r in eff if tag in r.get("shot_tags", [])]
    final = [r for r in eff if not r.get("draft_tier")]
    drafts = [r for r in eff if r.get("draft_tier")]

    groups = {}
    for r in final:
        for t in r.get("shot_tags", []):
            groups.setdefault(t, []).append(r)

    out = []
    for t, members in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        n = len(members)
        kept = sum(1 for r in members if r.get("outcome") == "kept")
        credited = [r for r in members
                    if isinstance(r.get("credits"), (int, float))]
        credited_kept = sum(1 for r in credited if r.get("outcome") == "kept")
        out.append({
            "tag": t,
            "n": n,
            "kept": kept,
            "takes_per_kept": (n / kept) if kept else None,
            "structural_frac": sum(1 for r in members if _is_structural(r)) / n,
            "stochastic_frac": sum(1 for r in members if _is_stochastic(r)) / n,
            "low_n": n < LOW_N_THRESHOLD,
            # Subpopulation-consistent money view: numerator AND denominator
            # come from credit-logged rows only, so a missing credits field
            # can't bias the figure low.
            "credits_per_kept": (sum(r["credits"] for r in credited) / credited_kept
                                 if credited_kept else None),
            "credits_coverage": (len(credited), n),
        })
    return {
        "n": len(final),
        "groups": out,
        "untagged": sum(1 for r in final if not r.get("shot_tags")),
        "draft": {
            "n": len(drafts),
            "kept": sum(1 for r in drafts if r.get("outcome") == "kept"),
            "credits": sum(r.get("credits", 0) for r in drafts
                           if isinstance(r.get("credits"), (int, float))),
        },
    }


def fork_verdict(group: dict) -> str:
    """Iterate-vs-batch pointer for one shot-tag group (pure, display-only).

    The honest fork: a miss is either SYSTEMATIC (the prompt is wrong — same
    failure every roll) or STOCHASTIC (the prompt is right, the dice weren't).
    Structural rejects mean systematic → rewrite the prompt, one variable at a
    time. Stochastic rejects mean variance → lock the prompt and batch-and-cull.
    Below LOW_N_THRESHOLD the split is noise, so the ledger stays silent and the
    human calls it by eye. This is a POINTER, not a verdict — the human decides."""
    if group["low_n"]:
        return "low-n"
    s, k = group["structural_frac"], group["stochastic_frac"]
    if s == 0 and k == 0:
        return "—"
    if s > k:
        return "iterate"
    if k > s:
        return "batch+sel"
    return "mixed"


def plausibility_flags(groups: list) -> list:
    """Flag A — cause-agnostic ratio-plausibility (pure, advisory only).

    A tag beating its planning default by a wide margin (observed takes/kept
    under half the default) is EITHER real lift (the framework working — then
    DEFAULT_RATIOS is stale and should be re-baselined) OR under-logged failures
    (the denominator is missing rows). The ratio underdetermines which, so this
    NEVER asserts a cause — it reports the deviation and names both branches for
    a human to adjudicate. Low-n groups are excluded (reuses the same guard)."""
    out = []
    for g in groups:
        tpk, default = g["takes_per_kept"], DEFAULT_RATIOS.get(g["tag"])
        if g["low_n"] or tpk is None or default is None:
            continue
        if tpk < 0.5 * default:
            out.append(
                f"⚠ {g['tag']}: {round(tpk, 1)}:1 observed vs {default:g}:1 planning "
                f"default — beating the default by a wide margin. Either real lift "
                f"(re-baseline DEFAULT_RATIOS) or under-logged failures (check the "
                f"denominator). Verify before trusting.")
    return out


def wasted_reroll_flags(rows: list, min_cluster: int = WASTED_REROLL_MIN) -> list:
    """Flag B — wasted-re-roll detector (pure, advisory).

    A prompt_hash cluster (identical prompt, re-rolled) with >= min_cluster
    STRUCTURAL rejects and ZERO kept rows is someone re-rolling the dice on a
    prompt that needs a rewrite — burning credits on the same systematic failure.

    The discriminator is KEEPER-PRESENCE, not reason-class. A legitimate
    variance-harvest batch (item 1: same locked prompt, N rolls) also forms a
    repeated-hash cluster that can contain structural rejects — identity-drift on
    roll 7 of 10 is structural yet one-off — so reason-class alone would
    false-fire on exactly the hardest, most-batched shots. But a harvest contains
    at least one KEEPER, which proves the prompt works. No keeper + an
    all-structural pile = the prompt is broken, and that distinction is only
    sound once item 1's batch semantics are live. Operates on effective
    (supersedes-resolved) rows; clusters without a prompt_hash are unjudgeable."""
    eff = resolve_effective(rows)
    clusters = {}
    for r in eff:
        h = r.get("prompt_hash")
        if h:
            clusters.setdefault(h, []).append(r)

    out = []
    for h, members in sorted(clusters.items()):
        if any(r.get("outcome") == "kept" for r in members):
            continue  # a keeper proves the prompt works — legitimate harvest
        structural = sum(1 for r in members if _is_structural(r))
        if structural < min_cluster:
            continue
        tags = sorted({t for r in members for t in r.get("shot_tags", [])})
        tag_str = ", ".join(tags) if tags else "untagged"
        out.append(
            f"⚠ wasted re-roll: prompt_hash {h} rolled {len(members)}× — "
            f"{structural} structural reject(s), no keeper ({tag_str}). You're "
            f"re-rolling a prompt that needs a rewrite, not better dice. Stop "
            f"and fix the prompt (single-variable iteration).")
    return out


def compute_method_ab(rows: list, tag: str = None) -> dict:
    """Item 3 control arm: takes-per-kept split by prompt_method (pure).

    Restricts to final-tier rows carrying a prompt_method in PROMPT_METHODS —
    UNLABELED rows are counted only as `excluded_unlabeled`, never folded into an
    arm, so pre-field history can't contaminate the A/B. Pass `tag` to compare on
    a matched shot class (the only apples-to-apples comparison)."""
    eff = resolve_effective(rows)
    if tag:
        eff = [r for r in eff if tag in r.get("shot_tags", [])]
    final = [r for r in eff if not r.get("draft_tier")]
    labeled = [r for r in final if r.get("prompt_method") in PROMPT_METHODS]

    methods = []
    for method in sorted(PROMPT_METHODS):
        members = [r for r in labeled if r.get("prompt_method") == method]
        if not members:
            continue
        n = len(members)
        kept = sum(1 for r in members if r.get("outcome") == "kept")
        methods.append({
            "method": method,
            "n": n,
            "kept": kept,
            "takes_per_kept": (n / kept) if kept else None,
            "structural_frac": sum(1 for r in members if _is_structural(r)) / n,
            "stochastic_frac": sum(1 for r in members if _is_stochastic(r)) / n,
            "low_n": n < LOW_N_THRESHOLD,
        })
    return {
        "tag": tag,
        "methods": methods,
        "n_labeled": len(labeled),
        "excluded_unlabeled": len(final) - len(labeled),
    }


def compute_vision_agreement(rows: list, min_n: int = VISION_AGREEMENT_MIN_N) -> dict:
    """Wave B: how often vision's proposed reason matched the human-confirmed
    reject_reason, per class (pure). Measures the classifier before we trust it.

    Only rows carrying BOTH a confirmed `reject_reason` and a proposed
    `vision_reason` count — a row diagnosed by vision but never human-confirmed
    isn't evidence of agreement either way. Per confirmed-reason class:
    agreement = matches / both-present. A class is `trusted` (vision may be
    logged without confirmation) only at >= VISION_TRUST_MIN_AGREEMENT over
    >= min_n diagnoses — its own low-n guard, so we never promote on a handful.
    `reject_reason` stays the verdict regardless; this only governs how much the
    human has to confirm."""
    eff = resolve_effective(rows)
    paired = [r for r in eff
              if r.get("reject_reason") in REJECT_REASONS
              and r.get("vision_reason") in REJECT_REASONS]

    classes = {}
    for r in paired:
        classes.setdefault(r["reject_reason"], []).append(r)

    out = []
    for reason, members in sorted(classes.items(),
                                  key=lambda kv: (-len(kv[1]), kv[0])):
        n = len(members)
        matches = sum(1 for r in members if r["vision_reason"] == r["reject_reason"])
        rate = matches / n
        out.append({
            "reject_reason": reason,
            "n": n,
            "matches": matches,
            "agreement": rate,
            "low_n": n < min_n,
            "trusted": (n >= min_n and rate >= VISION_TRUST_MIN_AGREEMENT),
        })
    return {
        "classes": out,
        "n_paired": len(paired),
        "n_diagnosed": sum(1 for r in eff if r.get("vision_reason") in REJECT_REASONS),
    }


_CONFIDENCE_RANK = {"project-data": 0, "global-data": 1, "default": 2}


def compute_budget(shots: list, project_rows: list, global_rows: list) -> dict:
    """Price a shot manifest from logged ratios (pure function).

    Per shot {shot_tags: [1..3], model?}: each tag resolves to the project
    tag group (only when n>=LOW_N_THRESHOLD and kept>0), else the global
    group (same bar), else DEFAULT_RATIOS (defaults, not data). Expected
    takes = MAX over the shot's tags (conservative); the shot's confidence
    label is the source of the WINNING tag (ties prefer the weaker label).
    Ratios are model-agnostic in v1; only the credit average is per-model
    (credited, non-draft, effective rows; project first, global fallback).
    Shots without a usable credit average are excluded from the money total
    and reported via coverage."""
    proj = {g["tag"]: g for g in compute_ratio(project_rows)["groups"]}
    glob = {g["tag"]: g for g in compute_ratio(global_rows)["groups"]}

    def tag_ratio(t: str):
        if t not in SHOT_TAGS:
            raise LedgerError(f"shot tag {t!r} not in vocabulary "
                              f"(allowed: {', '.join(sorted(SHOT_TAGS))})")
        for source, table in (("project-data", proj), ("global-data", glob)):
            g = table.get(t)
            if g and g["n"] >= LOW_N_THRESHOLD and g["kept"] > 0:
                return g["takes_per_kept"], source
        return DEFAULT_RATIOS[t], "default"

    def credit_avg(model_id: str):
        for rows in (project_rows, global_rows):
            credited = [r for r in resolve_effective(rows)
                        if r.get("model") == model_id
                        and not r.get("draft_tier")
                        and isinstance(r.get("credits"), (int, float))]
            if credited:
                return sum(r["credits"] for r in credited) / len(credited)
        return None

    shots_out = []
    for i, shot in enumerate(shots):
        tags = shot.get("shot_tags") or []
        if not 1 <= len(tags) <= 3:
            raise LedgerError(f"shot {i + 1}: needs 1..3 shot_tags, got {len(tags)}")
        candidates = [(takes, src, t) for t in tags
                      for takes, src in [tag_ratio(t)]]
        # MAX takes wins; on a tie prefer the weaker (less data-backed) label.
        takes, source, won_tag = max(
            candidates, key=lambda c: (c[0], _CONFIDENCE_RANK[c[1]]))
        avg = credit_avg(shot["model"]) if shot.get("model") else None
        shots_out.append({
            "shot": shot.get("shot") or f"#{i + 1}",
            "tags": tags,
            "model": shot.get("model"),
            "expected_takes": takes,
            "source": source,
            "winning_tag": won_tag,
            "credit_avg": avg,
            "expected_credits": (avg * takes) if avg is not None else None,
        })

    costed = [s for s in shots_out if s["expected_credits"] is not None]
    return {
        "shots": shots_out,
        "total_takes": sum(s["expected_takes"] for s in shots_out),
        "total_credits": (sum(s["expected_credits"] for s in costed)
                          if costed else None),
        "credit_coverage": (len(costed), len(shots_out)),
        "confidence": max((s["source"] for s in shots_out),
                          key=lambda s: _CONFIDENCE_RANK[s],
                          default="default"),
        "defaults_used": any(s["source"] == "default" for s in shots_out),
    }


class LedgerError(ValueError):
    """Raised on invalid ledger writes. The CLI maps it to a JSON error +
    exit 1; in-process callers (the seedance_lint bridge) catch it so a
    logging hiccup can never block a lint run."""


def log_gen_row(project: str, fields: dict) -> dict:
    """The single write path for ledger rows: fill id/ts, canonicalize the
    model id, schema-validate, append, regenerate _global. Raises
    LedgerError with the full problem list on invalid input — failing fast
    with the vocabulary printed is what keeps logging at one retry max."""
    model_ids = load_specs_models()
    if not model_ids:
        raise LedgerError("specs/model-specs.json missing or unreadable — "
                          "the ledger validates model ids against the specs "
                          "layer (run: python3 scripts/sync_specs.py)")
    path = ledger_path(project)
    db = load_ledger(path)

    row = {k: v for k, v in fields.items() if v is not None}
    row.setdefault("id", next_gen_id(project, db["rows"]))
    row.setdefault("ts", now_iso())
    row.setdefault("shot_tags", [])
    row.setdefault("draft_tier", False)
    if row.get("model") in model_ids:
        row["model"] = model_ids[row["model"]]  # alias → canonical

    prior_ids = {r.get("id") for r in db["rows"]}
    superseded = {r.get("supersedes") for r in db["rows"] if r.get("supersedes")}
    if row["id"] in prior_ids:
        raise LedgerError(f"duplicate id {row['id']}")
    problems = validate_ledger_row(row, project, prior_ids, superseded, model_ids)
    if problems:
        raise LedgerError("; ".join(problems))

    db["rows"].append(row)
    save_ledger(path, db)
    write_global()
    return row


def _parse_log_gen_args(argv: list):
    import argparse
    p = argparse.ArgumentParser(
        prog="scripts/higgsfield_memory.py log-gen",
        description="Log one generation attempt to a project ledger "
                    "(one line — see db/ledger/README.md).")
    p.add_argument("project")
    p.add_argument("json_row", nargs="?",
                   help="raw JSON row (alternative to the flags below)")
    p.add_argument("--model", help="specs model id or alias")
    p.add_argument("--tags", help="comma-separated shot tags (controlled vocab)")
    p.add_argument("--outcome", choices=sorted(OUTCOMES))
    p.add_argument("--reason", help="reject_reason (required when rejected)")
    p.add_argument("--mode")
    p.add_argument("--resolution")
    p.add_argument("--aspect")
    p.add_argument("--duration", type=int, help="duration_s")
    p.add_argument("--cuts", type=int, help="internal_cuts")
    p.add_argument("--scene", help="scene_ref")
    p.add_argument("--draft", action="store_true", help="mark as draft-tier roll")
    p.add_argument("--credits", type=int)
    p.add_argument("--notes")
    p.add_argument("--prompt", help="prompt text — stored only as sha1[:12] prompt_hash")
    p.add_argument("--method", choices=sorted(PROMPT_METHODS),
                   help="prompt_method control arm (quick | mcsla); omit to leave "
                        "unlabeled and out of the A/B")
    p.add_argument("--vision-reason", dest="vision_reason",
                   choices=sorted(REJECT_REASONS),
                   help="reject_reason a vision pass PROPOSED (advisory); the human "
                        "still sets --reason. Feeds the agreement gate.")
    p.add_argument("--vision-evidence", dest="vision_evidence",
                   help="one-line note of what vision saw (e.g. 'warped left hand, "
                        "center frame')")
    return p.parse_args(argv)


def cmd_log_gen(argv: list):
    args = _parse_log_gen_args(argv)
    if args.json_row:
        try:
            fields = json.loads(args.json_row)
        except json.JSONDecodeError as e:
            print(json.dumps({"status": "error", "message": f"Invalid JSON: {e}"}))
            sys.exit(1)
    else:
        import hashlib
        fields = {
            "model": args.model,
            "shot_tags": [t.strip() for t in args.tags.split(",")] if args.tags else None,
            "outcome": args.outcome,
            "reject_reason": args.reason,
            "mode": args.mode,
            "resolution": args.resolution,
            "aspect": args.aspect,
            "duration_s": args.duration,
            "internal_cuts": args.cuts,
            "scene_ref": args.scene,
            "draft_tier": True if args.draft else None,
            "credits": args.credits,
            "notes": args.notes,
            "prompt_hash": (hashlib.sha1(args.prompt.strip().encode("utf-8"))
                            .hexdigest()[:12] if args.prompt else None),
            "prompt_method": args.method,
            "vision_reason": args.vision_reason,
            "vision_evidence": args.vision_evidence,
        }
    try:
        row = log_gen_row(args.project, fields)
    except LedgerError as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)
    print(json.dumps({"status": "ok", "id": row["id"], "outcome": row["outcome"],
                      "project": args.project}))


def render_ratio(label: str, result: dict, credits_mode: bool = False) -> str:
    lines = [f"{label.upper()} — generation ratios (final-tier only, n={result['n']})"]
    if not result["groups"]:
        lines.append("  (no final-tier rows yet — log generations with log-gen)")
    else:
        header = f"{'shot_tag':<18} {'n':<4} {'kept':<5} {'takes/kept':<11} {'structural%':<12} {'stochastic%':<12} {'verdict':<10}"
        if credits_mode:
            header += f" {'credits/kept':<14} coverage"
        lines.append(header)
        for g in result["groups"]:
            takes = f"{round(g['takes_per_kept'], 1)}" if g["takes_per_kept"] else "—"
            struct = f"{round(100 * g['structural_frac'])}%"
            stoch = f"{round(100 * g['stochastic_frac'])}%"
            row = (f"{g['tag']:<18} {g['n']:<4} {g['kept']:<5} {takes:<11} "
                   f"{struct:<12} {stoch:<12} {fork_verdict(g):<10}")
            if credits_mode:
                cpk = (f"{round(g['credits_per_kept'])}"
                       if g["credits_per_kept"] is not None else "—")
                k, n = g["credits_coverage"]
                row += f" {cpk:<14} (credits on {k}/{n} rows)"
            if g["low_n"]:
                row += "  low-n"
            lines.append(row)
    if result["untagged"]:
        lines.append(f"  ({result['untagged']} untagged flagged row(s) count in "
                     "n but in no group)")
    d = result["draft"]
    if d["n"]:
        burn = f"Draft burn: {d['n']} draft-tier row(s), {d['kept']} kept (excluded from the table)"
        if credits_mode and d["credits"]:
            burn += f" — {d['credits']} credits"
        lines.append(burn)
    for flag in plausibility_flags(result["groups"]):
        lines.append(flag)
    lines.append('Confidence: rows with n < '
                 f'{LOW_N_THRESHOLD} marked "low-n" — do not budget from them.')
    lines.append('Verdict (above-threshold tags): "iterate" = structural-dominant, '
                 'rewrite the prompt one variable at a time; "batch+sel" = '
                 'stochastic-dominant, lock the prompt and batch-and-cull.')
    return "\n".join(lines)


def cmd_ratio(argv: list):
    import argparse
    p = argparse.ArgumentParser(
        prog="scripts/higgsfield_memory.py ratio",
        description="Takes-per-kept ratio table from the generation ledger.")
    p.add_argument("project", nargs="?",
                   help="project ledger (omit with --global)")
    p.add_argument("--model", help="filter to one canonical model id")
    p.add_argument("--tag", help="filter to rows carrying one shot tag")
    p.add_argument("--global", dest="global_view", action="store_true",
                   help="aggregate across all (non-underscore) projects")
    p.add_argument("--credits", action="store_true",
                   help="add the credits-per-kept money view")
    args = p.parse_args(argv)

    if args.global_view:
        rows = load_ledger(GLOBAL_LEDGER)["rows"]
        label = "global"
    elif args.project:
        # Reads may target reserved (underscore) ledgers like _demo;
        # only WRITES are blocked from them.
        if re.fullmatch(r"_?[A-Za-z0-9][A-Za-z0-9_-]*", args.project):
            path = LEDGER_DIR / f"{args.project}.json"
        else:
            path = ledger_path(args.project)  # reuses the error contract
        rows = load_ledger(path)["rows"]
        label = args.project
    else:
        p.error("need a project name or --global")
    result = compute_ratio(rows, model=args.model, tag=args.tag)
    print(render_ratio(label, result, credits_mode=args.credits))
    # Flag B runs on the full (unfiltered) scope — re-roll clusters span the
    # whole ledger, independent of the --model/--tag display filters.
    for flag in wasted_reroll_flags(rows):
        print(flag)


def render_method_ab(label: str, result: dict) -> str:
    scope = f"tag={result['tag']}" if result["tag"] else "all tags"
    lines = [f"{label.upper()} — prompt_method A/B ({scope}, "
             f"n_labeled={result['n_labeled']})"]
    if not result["methods"]:
        lines.append("  (no rows carry a prompt_method yet — log with "
                     "--method quick|mcsla to start the control arm)")
    else:
        lines.append(f"{'method':<8} {'n':<4} {'kept':<5} {'takes/kept':<11} "
                     f"{'structural%':<12} {'stochastic%':<12}")
        for m in result["methods"]:
            takes = f"{round(m['takes_per_kept'], 1)}" if m["takes_per_kept"] else "—"
            row = (f"{m['method']:<8} {m['n']:<4} {m['kept']:<5} {takes:<11} "
                   f"{round(100 * m['structural_frac']):<11}% "
                   f"{round(100 * m['stochastic_frac']):<11}%")
            if m["low_n"]:
                row += "  low-n"
            lines.append(row)
    if result["excluded_unlabeled"]:
        lines.append(f"  ({result['excluded_unlabeled']} unlabeled final-tier row(s) "
                     "excluded from the comparison — not folded into either arm)")
    lines.append("Compare only matched shot classes: pass --tag <shot_tag> so quick "
                 "and mcsla are priced on the same kind of shot.")
    return "\n".join(lines)


def cmd_ab(argv: list):
    import argparse
    p = argparse.ArgumentParser(
        prog="scripts/higgsfield_memory.py ab",
        description="Prompt_method A/B (quick vs mcsla) from the generation "
                    "ledger — unlabeled rows are excluded, not bucketed.")
    p.add_argument("project", nargs="?", help="project ledger (omit with --global)")
    p.add_argument("--tag", help="restrict to one shot tag (matched-class compare)")
    p.add_argument("--global", dest="global_view", action="store_true",
                   help="aggregate across all (non-underscore) projects")
    args = p.parse_args(argv)
    if args.global_view:
        rows = load_ledger(GLOBAL_LEDGER)["rows"]
        label = "global"
    elif args.project:
        if re.fullmatch(r"_?[A-Za-z0-9][A-Za-z0-9_-]*", args.project):
            path = LEDGER_DIR / f"{args.project}.json"
        else:
            path = ledger_path(args.project)
        rows = load_ledger(path)["rows"]
        label = args.project
    else:
        p.error("need a project name or --global")
    print(render_method_ab(label, compute_method_ab(rows, tag=args.tag)))


def render_agreement(label: str, result: dict) -> str:
    lines = [f"{label.upper()} — vision/human agreement "
             f"(paired={result['n_paired']}, diagnosed={result['n_diagnosed']})"]
    if not result["classes"]:
        lines.append("  (no rows carry both a confirmed reject_reason and a "
                     "vision_reason yet — log diagnoses with --vision-reason)")
    else:
        lines.append(f"{'reject_reason':<22} {'n':<4} {'match':<6} "
                     f"{'agreement':<10} {'trusted':<8}")
        for c in result["classes"]:
            agree = f"{round(100 * c['agreement'])}%"
            trusted = "yes" if c["trusted"] else ("low-n" if c["low_n"] else "no")
            lines.append(f"{c['reject_reason']:<22} {c['n']:<4} {c['matches']:<6} "
                         f"{agree:<10} {trusted:<8}")
    lines.append(f'Trusted = vision agrees >= {round(100 * VISION_TRUST_MIN_AGREEMENT)}% '
                 f'over >= {VISION_AGREEMENT_MIN_N} confirmed diagnoses; until then '
                 'a human confirms every vision_reason.')
    return "\n".join(lines)


def cmd_agreement(argv: list):
    import argparse
    p = argparse.ArgumentParser(
        prog="scripts/higgsfield_memory.py agreement",
        description="Vision/human label agreement per reject_reason class — "
                    "measures the vision classifier before it is trusted.")
    p.add_argument("project", nargs="?", help="project ledger (omit with --global)")
    p.add_argument("--global", dest="global_view", action="store_true",
                   help="aggregate across all (non-underscore) projects")
    args = p.parse_args(argv)
    if args.global_view:
        rows = load_ledger(GLOBAL_LEDGER)["rows"]
        label = "global"
    elif args.project:
        if re.fullmatch(r"_?[A-Za-z0-9][A-Za-z0-9_-]*", args.project):
            path = LEDGER_DIR / f"{args.project}.json"
        else:
            path = ledger_path(args.project)
        rows = load_ledger(path)["rows"]
        label = args.project
    else:
        p.error("need a project name or --global")
    print(render_agreement(label, compute_vision_agreement(rows)))


def _load_shot_manifest(path: Path) -> list:
    """Shot manifest: JSON list of {shot?, shot_tags, model?} or CSV with
    columns shot / shot_tags / model (tags separated by ; or , in the cell)."""
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        shots = json.loads(text)
        if not isinstance(shots, list):
            raise LedgerError("JSON manifest must be a list of shot objects")
        return shots
    import csv
    import io
    shots = []
    for rec in csv.DictReader(io.StringIO(text)):
        tags = re.split(r"[;,]", rec.get("shot_tags") or "")
        shots.append({
            "shot": (rec.get("shot") or "").strip() or None,
            "shot_tags": [t.strip() for t in tags if t.strip()],
            "model": (rec.get("model") or "").strip() or None,
        })
    return shots


def render_budget(label: str, result: dict) -> str:
    lines = [f"{label.upper()} — budget estimate ({len(result['shots'])} planned shot(s))",
             f"{'shot':<8} {'tags':<34} {'takes':<7} source"]
    for s in result["shots"]:
        src = s["source"] + (" (defaults, not data)" if s["source"] == "default" else "")
        lines.append(f"{s['shot']:<8} {'+'.join(s['tags']):<34} "
                     f"{round(s['expected_takes'], 1):<7} {src}")
    lines.append("")
    lines.append(f"Expected generations: {round(result['total_takes'], 1)}")
    covered, total = result["credit_coverage"]
    if result["total_credits"] is not None:
        lines.append(f"Credit estimate: {round(result['total_credits'])} "
                     f"(credit data on {covered}/{total} shots)")
    else:
        lines.append("Credit estimate: — (no logged credit data for these models)")
    lines.append(f"Confidence: {result['confidence']}")
    if result["defaults_used"]:
        lines.append("⚠ DEFAULT planning ratios used for some shots — these are the "
                     "documented defaults (2–3:1 simple, 4–6:1 complex), NOT logged "
                     "data. Log generations to replace them with real numbers.")
    return "\n".join(lines)


def cmd_budget(argv: list):
    import argparse
    p = argparse.ArgumentParser(
        prog="scripts/higgsfield_memory.py budget",
        description="Price a shot manifest from logged generation ratios.")
    p.add_argument("project")
    p.add_argument("--shots", required=True, type=Path,
                   help="manifest file: JSON list or CSV (shot, shot_tags, model)")
    args = p.parse_args(argv)

    if re.fullmatch(r"_?[A-Za-z0-9][A-Za-z0-9_-]*", args.project):
        path = LEDGER_DIR / f"{args.project}.json"
    else:
        path = ledger_path(args.project)
    project_rows = load_ledger(path)["rows"]
    global_rows = load_ledger(GLOBAL_LEDGER)["rows"]
    try:
        shots = _load_shot_manifest(args.shots)
        result = compute_budget(shots, project_rows, global_rows)
    except (OSError, json.JSONDecodeError, LedgerError) as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)
    print(render_budget(args.project, result))


def cmd_last_gen(project: str):
    db = load_ledger(ledger_path(project))
    effective = resolve_effective(db["rows"])
    if not effective:
        print(json.dumps({"status": "empty", "project": project}))
        return
    print(json.dumps(effective[-1], indent=2, ensure_ascii=False))


def cmd_amend_gen(argv: list):
    """amend-gen <id> field=value [...] — writes a SUPERSEDING row (full
    clone of the original with overrides); history is never edited."""
    if len(argv) < 2 or "=" not in argv[1]:
        print(json.dumps({"status": "error",
                          "message": "usage: amend-gen <id> field=value [field=value ...]"}))
        sys.exit(1)
    gen_id = argv[0]
    m = GEN_ID_RE.match(gen_id)
    if not m:
        print(json.dumps({"status": "error", "message": f"Bad id: {gen_id!r}"}))
        sys.exit(1)
    project = m.group(1)
    db = load_ledger(ledger_path(project))
    original = next((r for r in db["rows"] if r.get("id") == gen_id), None)
    if original is None:
        print(json.dumps({"status": "error", "message": f"{gen_id} not found"}))
        sys.exit(1)
    superseded = {r.get("supersedes") for r in db["rows"] if r.get("supersedes")}
    if gen_id in superseded:
        latest = next(r["id"] for r in reversed(db["rows"])
                      if r.get("supersedes") == gen_id)
        print(json.dumps({"status": "error",
                          "message": f"{gen_id} is already superseded — amend the "
                                     f"latest amendment ({latest}) instead"}))
        sys.exit(1)

    clone = {k: v for k, v in original.items()
             if k not in ("id", "ts", "supersedes")}
    for pair in argv[1:]:
        key, _, value = pair.partition("=")
        if key == "shot_tags" or key == "tags":
            clone["shot_tags"] = [t.strip() for t in value.split(",") if t.strip()]
        elif value.lower() in ("true", "false"):
            clone[key] = value.lower() == "true"
        elif value.lower() in ("null", "none", ""):
            clone.pop(key, None)
        else:
            try:
                clone[key] = int(value)
            except ValueError:
                clone[key] = value
    # An outcome flip away from 'rejected' drops the now-invalid reason
    # unless the amendment explicitly set one.
    if clone.get("outcome") != "rejected":
        amended_keys = {p.partition("=")[0] for p in argv[1:]}
        if "reject_reason" not in amended_keys:
            clone.pop("reject_reason", None)
    clone["supersedes"] = gen_id
    try:
        row = log_gen_row(project, clone)
    except LedgerError as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)
    print(json.dumps({"status": "ok", "id": row["id"], "supersedes": gen_id,
                      "outcome": row.get("outcome")}))

# ── Routing telemetry (item 6) ───────────────────────────────────────────────
# The dispatcher already NAMES its routes (HARD RULE #1: the first line of every
# response lists the sub-skills routed to). This persists that declaration so
# "which skills are load-bearing vs the long tail" is answerable from data, not
# guessed. Like the ledger, it is only as complete as the logging — and pruning
# waits until enough requests accumulate to trust the distribution.

SUB_SKILLS = set(SUB_SKILL_DESCRIPTIONS)


def validate_route_entry(entry: dict) -> list:
    problems = []
    rid = entry.get("id", "?")
    skills = entry.get("skills")
    if not isinstance(skills, list) or not skills:
        problems.append(f"{rid}: skills must be a non-empty list")
    else:
        bad = [s for s in skills if s not in SUB_SKILLS]
        if bad:
            problems.append(f"{rid}: skills not in the sub-skill roster: "
                            f"{', '.join(bad)}")
    unknown = set(entry) - {"id", "ts", "skills", "scene_ref", "notes"}
    if unknown:
        problems.append(f"{rid}: unknown field(s): {', '.join(sorted(unknown))}")
    return problems


def log_route(skills: list, scene_ref: str = None, notes: str = None) -> dict:
    db = load_db(ROUTING_DB)
    entry = {"id": next_id(db["entries"], "R"),
             "ts": now_iso(),
             "skills": skills}
    if scene_ref:
        entry["scene_ref"] = scene_ref
    if notes:
        entry["notes"] = notes
    problems = validate_route_entry(entry)
    if problems:
        raise LedgerError("; ".join(problems))
    db["entries"].append(entry)
    save_db(ROUTING_DB, db)
    return entry


def compute_routing(entries: list) -> dict:
    """Per-skill open counts over logged requests (pure). `never_opened` is the
    long tail — roster skills with zero opens — which is what a prune review
    starts from."""
    n = len(entries)
    counts = {}
    for e in entries:
        for s in e.get("skills", []):
            counts[s] = counts.get(s, 0) + 1
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return {
        "n": n,
        "skills": [{"skill": s, "opens": c, "pct": (c / n) if n else 0.0}
                   for s, c in ranked],
        "never_opened": sorted(SUB_SKILLS - set(counts)),
    }


def render_routing(result: dict) -> str:
    lines = [f"ROUTING — sub-skill opens over {result['n']} logged request(s)"]
    if not result["skills"]:
        lines.append("  (no routes logged yet — log with log-route --skills a,b,c)")
    else:
        lines.append(f"{'sub-skill':<28} {'opens':<6} share")
        for s in result["skills"]:
            lines.append(f"{s['skill']:<28} {s['opens']:<6} {round(100 * s['pct'])}%")
    tail = result["never_opened"]
    if tail:
        lines.append(f"Never opened ({len(tail)}/{len(SUB_SKILLS)}) — prune-review "
                     f"candidates once n is large enough: {', '.join(tail)}")
    lines.append("Instrumentation only — let requests accumulate before pruning "
                 "the tail; a small n is not evidence a skill is dead.")
    return "\n".join(lines)


def cmd_log_route(argv: list):
    import argparse
    p = argparse.ArgumentParser(prog="scripts/higgsfield_memory.py log-route")
    p.add_argument("--skills", required=True,
                   help="comma-separated sub-skill names routed to this request")
    p.add_argument("--scene", help="optional scene_ref / request tag")
    p.add_argument("--notes")
    args = p.parse_args(argv)
    skills = [s.strip() for s in args.skills.split(",") if s.strip()]
    try:
        entry = log_route(skills, scene_ref=args.scene, notes=args.notes)
    except LedgerError as e:
        print(json.dumps({"status": "error", "message": str(e),
                          "roster": sorted(SUB_SKILLS)}))
        sys.exit(1)
    print(json.dumps({"status": "ok", "id": entry["id"], "skills": entry["skills"]}))


def cmd_routing(argv: list):
    db = load_db(ROUTING_DB)
    print(render_routing(compute_routing(db["entries"])))


# ── Commands ───────────────────────────────────────────────────────────────────

def add_filter(entry_json: str):
    """Add a content filter block entry."""
    db = load_db(FILTER_DB)
    try:
        entry = json.loads(entry_json)
    except json.JSONDecodeError as e:
        print(json.dumps({"status": "error", "message": f"Invalid JSON: {e}"}))
        return

    # Required fields with defaults
    entry.setdefault("id", next_id(db["entries"], "F"))
    entry.setdefault("date_added", now_iso())
    entry.setdefault("outcome", "unknown")       # unknown | fixed | workaround | still-blocked
    entry.setdefault("fix_confirmed", False)
    entry.setdefault("tags", [])
    entry.setdefault("blocked_terms", [])        # specific words/phrases that triggered the block
    entry.setdefault("substitution", None)        # what was used instead
    entry.setdefault("substitution_worked", None) # True | False | None (untested)
    entry.setdefault("notes", "")

    db["entries"].append(entry)
    save_db(FILTER_DB, db)
    print(json.dumps({"status": "ok", "id": entry["id"], "total": len(db["entries"])}))


def add_quality(entry_json: str):
    """Add a quality failure entry."""
    db = load_db(QUALITY_DB)
    try:
        entry = json.loads(entry_json)
    except json.JSONDecodeError as e:
        print(json.dumps({"status": "error", "message": f"Invalid JSON: {e}"}))
        return

    entry.setdefault("id", next_id(db["entries"], "Q"))
    entry.setdefault("date_added", now_iso())
    entry.setdefault("outcome", "unknown")        # unknown | improved | still-failing
    entry.setdefault("fix_confirmed", False)
    entry.setdefault("tags", [])
    entry.setdefault("model_used", None)
    entry.setdefault("improved_prompt", None)     # the prompt that fixed it
    entry.setdefault("improvement_confirmed", None)
    entry.setdefault("notes", "")

    db["entries"].append(entry)
    save_db(QUALITY_DB, db)
    print(json.dumps({"status": "ok", "id": entry["id"], "total": len(db["entries"])}))


def query_filter(search_terms: str, top_n: int = 5):
    """Return top N most relevant filter entries for the given search terms."""
    db = load_db(FILTER_DB)
    if not db["entries"]:
        print(json.dumps({"results": [], "total_in_db": 0}))
        return

    query_tokens = tokenize(search_terms)
    scored = [(relevance_score(e, query_tokens), e) for e in db["entries"]]
    scored.sort(key=lambda x: (x[0], x[1].get("date_added", "")), reverse=True)

    results = [e for score, e in scored if score > 0][:top_n]
    print(json.dumps({
        "results": results,
        "total_in_db": len(db["entries"]),
        "query": search_terms
    }, indent=2))


def query_quality(search_terms: str, top_n: int = 5):
    """Return top N most relevant quality entries for the given search terms."""
    db = load_db(QUALITY_DB)
    if not db["entries"]:
        print(json.dumps({"results": [], "total_in_db": 0}))
        return

    query_tokens = tokenize(search_terms)
    scored = [(relevance_score(e, query_tokens), e) for e in db["entries"]]
    scored.sort(key=lambda x: (x[0], x[1].get("date_added", "")), reverse=True)

    results = [e for score, e in scored if score > 0][:top_n]
    print(json.dumps({
        "results": results,
        "total_in_db": len(db["entries"]),
        "query": search_terms
    }, indent=2))


def update_filter(entry_id: str, outcome: str, notes: str = ""):
    """Update the outcome of a filter entry after testing a substitution."""
    if outcome not in FILTER_OUTCOMES:
        print(json.dumps({"status": "error",
                          "message": f"Invalid outcome '{outcome}'. Expected one of: {sorted(FILTER_OUTCOMES)}"}))
        return
    db = load_db(FILTER_DB)
    for entry in db["entries"]:
        if entry.get("id") == entry_id:
            entry["outcome"] = outcome
            entry["fix_confirmed"] = outcome in ("fixed", "workaround")
            entry["substitution_worked"] = outcome == "fixed"
            if notes:
                entry["notes"] = notes
            entry["date_updated"] = now_iso()
            save_db(FILTER_DB, db)
            print(json.dumps({"status": "ok", "id": entry_id, "outcome": outcome}))
            return
    print(json.dumps({"status": "error", "message": f"Entry {entry_id} not found"}))


def update_quality(entry_id: str, outcome: str, improved_prompt: str = "", notes: str = ""):
    """Update the outcome of a quality entry after testing an improved prompt."""
    if outcome not in QUALITY_OUTCOMES:
        print(json.dumps({"status": "error",
                          "message": f"Invalid outcome '{outcome}'. Expected one of: {sorted(QUALITY_OUTCOMES)}"}))
        return
    db = load_db(QUALITY_DB)
    for entry in db["entries"]:
        if entry.get("id") == entry_id:
            entry["outcome"] = outcome
            entry["fix_confirmed"] = outcome == "improved"
            entry["improvement_confirmed"] = outcome == "improved"
            if improved_prompt:
                entry["improved_prompt"] = improved_prompt
            if notes:
                entry["notes"] = notes
            entry["date_updated"] = now_iso()
            save_db(QUALITY_DB, db)
            print(json.dumps({"status": "ok", "id": entry_id, "outcome": outcome}))
            return
    print(json.dumps({"status": "error", "message": f"Entry {entry_id} not found"}))


def stats():
    """Print summary statistics for both databases."""
    f_db = load_db(FILTER_DB)
    q_db = load_db(QUALITY_DB)

    f_entries = f_db["entries"]
    q_entries = q_db["entries"]

    f_fixed = sum(1 for e in f_entries if e.get("fix_confirmed"))
    f_unknown = sum(1 for e in f_entries if e.get("outcome") == "unknown")

    q_fixed = sum(1 for e in q_entries if e.get("fix_confirmed"))
    q_unknown = sum(1 for e in q_entries if e.get("outcome") == "unknown")

    # Most common filter categories
    categories = {}
    for e in f_entries:
        cat = e.get("category", "uncategorized")
        categories[cat] = categories.get(cat, 0) + 1

    print(json.dumps({
        "filter_memory": {
            "total_entries": len(f_entries),
            "fixes_confirmed": f_fixed,
            "still_unknown": f_unknown,
            "last_updated": f_db.get("_last_updated"),
            "categories": categories
        },
        "quality_memory": {
            "total_entries": len(q_entries),
            "improvements_confirmed": q_fixed,
            "still_unknown": q_unknown,
            "last_updated": q_db.get("_last_updated")
        }
    }, indent=2))


def build_summary() -> str:
    """Render the markdown summary of both databases (no file writes).

    Split out from export_summary so validate.py can compare a fresh render
    against db/memory-summary.md without side effects."""
    f_db = load_db(FILTER_DB)
    q_db = load_db(QUALITY_DB)

    lines = ["# Higgsfield Memory Summary\n"]
    lines.append(f"Generated: {now_iso()}\n")

    lines.append("\n## Content Filter Memory\n")
    lines.append(f"Total entries: {len(f_db['entries'])}\n")
    for e in f_db["entries"]:
        lines.append(f"\n### {e['id']} — {e.get('category', 'uncategorized')}")
        lines.append(f"- **Date:** {e.get('date_added', 'unknown')}")
        lines.append(f"- **Failed prompt:** {e.get('failed_prompt', '')[:200]}")
        lines.append(f"- **Error:** {e.get('error_message', 'not recorded')}")
        lines.append(f"- **Blocked terms:** {', '.join(e.get('blocked_terms', []))}")
        lines.append(f"- **Substitution:** {e.get('substitution', 'none')}")
        lines.append(f"- **Outcome:** {e.get('outcome', 'unknown')}")
        lines.append(f"- **Notes:** {e.get('notes', '')}")

    lines.append("\n---\n\n## Quality Memory\n")
    lines.append(f"Total entries: {len(q_db['entries'])}\n")
    for e in q_db["entries"]:
        lines.append(f"\n### {e['id']} — {e.get('failure_type', 'unknown')}")
        lines.append(f"- **Date:** {e.get('date_added', 'unknown')}")
        lines.append(f"- **Model:** {e.get('model_used', 'unknown')}")
        lines.append(f"- **Original prompt:** {e.get('original_prompt', '')[:200]}")
        lines.append(f"- **What was wrong:** {e.get('failure_description', '')}")
        lines.append(f"- **Improved prompt:** {e.get('improved_prompt', 'not yet found')[:200]}")
        lines.append(f"- **Outcome:** {e.get('outcome', 'unknown')}")
        lines.append(f"- **Notes:** {e.get('notes', '')}")

    # Generation ledger — current ratios at a glance (real projects only;
    # underscore-prefixed ledgers are reserved/fixture data).
    lines.append("\n---\n\n## Generation Ledger\n")
    projects = project_ledger_files()
    if not projects:
        lines.append("No project ledgers yet — log generations with "
                     "`scripts/higgsfield_memory.py log-gen <project> ...`.")
    for path in projects:
        db = load_ledger(path)
        lines.append("\n```")
        lines.append(render_ratio(db["project"], compute_ratio(db["rows"])))
        lines.append("```")

    return "\n".join(lines)


def export_summary():
    """Write the markdown summary of both databases to db/memory-summary.md."""
    summary = build_summary()
    DB_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DB_DIR / "memory-summary.md"
    tmp_path = out_path.with_suffix(".tmp")
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(summary)
        tmp_path.replace(out_path)
    except OSError as e:
        tmp_path.unlink(missing_ok=True)
        print(json.dumps({"status": "error", "message": f"Failed to write summary: {e}"}))
        sys.exit(1)
    f_db = load_db(FILTER_DB)
    q_db = load_db(QUALITY_DB)
    print(json.dumps({"status": "ok", "path": str(out_path), "filter_entries": len(f_db["entries"]), "quality_entries": len(q_db["entries"])}))


def health():
    """Run a quick integrity check on both database files."""
    issues = []
    results = {}

    for label, path in [("filter", FILTER_DB), ("quality", QUALITY_DB)]:
        if not path.exists():
            issues.append(f"{label}: file missing ({path})")
            results[label] = {"ok": False, "reason": "file missing"}
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                db = json.load(f)
        except json.JSONDecodeError as e:
            issues.append(f"{label}: corrupted JSON — {e}")
            results[label] = {"ok": False, "reason": f"corrupted JSON: {e}"}
            continue

        entry_count = len(db.get("entries", []))
        declared = db.get("_total_entries", -1)
        count_ok = entry_count == declared
        if not count_ok:
            issues.append(f"{label}: _total_entries mismatch (declared {declared}, actual {entry_count})")

        results[label] = {
            "ok": count_ok,
            "entries": entry_count,
            "declared_total": declared,
            "last_updated": db.get("_last_updated"),
        }

    print(json.dumps({
        "status": "ok" if not issues else "issues_found",
        "databases": results,
        "issues": issues,
    }, indent=2))


# ── Entry Point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Global --project option: redirect both DBs to a per-project namespace
    # under db/projects/ so production-specific lessons stay scoped.
    if "--project" in sys.argv:
        idx = sys.argv.index("--project")
        if idx + 1 >= len(sys.argv):
            print(json.dumps({"status": "error",
                              "message": "--project requires a project name"}))
            sys.exit(1)
        project = sys.argv[idx + 1]
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", project):
            print(json.dumps({"status": "error",
                              "message": f"Invalid project name: {project!r} "
                                         "(alphanumeric, dash, underscore)"}))
            sys.exit(1)
        del sys.argv[idx:idx + 2]
        PROJECT_MODE = True
        FILTER_DB = DB_DIR / "projects" / f"{project}-filter-memory.json"
        QUALITY_DB = DB_DIR / "projects" / f"{project}-quality-memory.json"

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "add-filter" and len(sys.argv) >= 3:
        add_filter(sys.argv[2])
    elif cmd == "add-quality" and len(sys.argv) >= 3:
        add_quality(sys.argv[2])
    elif cmd == "query-filter" and len(sys.argv) >= 3:
        try:
            top_n = int(sys.argv[3]) if len(sys.argv) >= 4 else 5
        except ValueError:
            print(json.dumps({"status": "error", "message": f"top_n must be an integer, got: {sys.argv[3]}"}))
            sys.exit(1)
        query_filter(sys.argv[2], top_n)
    elif cmd == "query-quality" and len(sys.argv) >= 3:
        try:
            top_n = int(sys.argv[3]) if len(sys.argv) >= 4 else 5
        except ValueError:
            print(json.dumps({"status": "error", "message": f"top_n must be an integer, got: {sys.argv[3]}"}))
            sys.exit(1)
        query_quality(sys.argv[2], top_n)
    elif cmd == "update-filter" and len(sys.argv) >= 4:
        notes = sys.argv[4] if len(sys.argv) >= 5 else ""
        update_filter(sys.argv[2], sys.argv[3], notes)
    elif cmd == "update-quality" and len(sys.argv) >= 4:
        improved = sys.argv[4] if len(sys.argv) >= 5 else ""
        notes = sys.argv[5] if len(sys.argv) >= 6 else ""
        update_quality(sys.argv[2], sys.argv[3], improved, notes)
    elif cmd == "log-gen" and len(sys.argv) >= 3:
        cmd_log_gen(sys.argv[2:])
    elif cmd == "ratio":
        cmd_ratio(sys.argv[2:])
    elif cmd == "ab":
        cmd_ab(sys.argv[2:])
    elif cmd == "agreement":
        cmd_agreement(sys.argv[2:])
    elif cmd == "log-route":
        cmd_log_route(sys.argv[2:])
    elif cmd == "routing":
        cmd_routing(sys.argv[2:])
    elif cmd == "budget":
        cmd_budget(sys.argv[2:])
    elif cmd == "last-gen" and len(sys.argv) >= 3:
        cmd_last_gen(sys.argv[2])
    elif cmd == "amend-gen" and len(sys.argv) >= 3:
        cmd_amend_gen(sys.argv[2:])
    elif cmd == "stats":
        stats()
    elif cmd == "export-summary":
        export_summary()
    elif cmd == "health":
        health()
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)
