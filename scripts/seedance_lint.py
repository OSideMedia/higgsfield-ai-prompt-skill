#!/usr/bin/env python3
"""
seedance_lint.py
================
Pre-flight linter for Seedance 2.0 / Seedance Pro prompts.

Seedance's content filter is an LLM reading full-scene intent, not a keyword
blacklist. But it still reliably flags prompts on a handful of patterns — this
linter catches those patterns before the user burns credits on an instant-fail.

Rules are grouped into three severities:
  FAIL  — will almost certainly be flagged. Do not generate.
  WARN  — likely to pass but weak; harden before generating.
  INFO  — style suggestion, not a flag risk.

Beyond the content-filter rules, the linter is a structural preflight driven
by the generated specs layer (specs/model-specs.json): declared shot counts,
beat-duration envelopes, ZH length caps, @handle declaration order, and
aspect-ratio / resolution / mode / duration legality per model enum — the
expensive class of failure (e.g. Seedance `fast` + 1080p, Kling 3.0 + 21:9).

Usage:
  python3 scripts/seedance_lint.py "<prompt text>"
  echo "<prompt text>" | python3 scripts/seedance_lint.py
  python3 scripts/seedance_lint.py --file prompt.txt
  python3 scripts/seedance_lint.py --model seedance_2_0 "<prompt>"   # + structural lint
  python3 scripts/seedance_lint.py --model kling3_0 --ar 21:9 "<prompt>"
  python3 scripts/seedance_lint.py --preflight --model seedance_2_0 "<prompt>"
  python3 scripts/seedance_lint.py --preflight --model seedance_2_5 \
      --mode video_extension --extension-mode forward "<prompt>"
                                                      # filter + structure + memory recall
  python3 scripts/seedance_lint.py --log "<prompt text>"      # log FAIL to filter-memory
  python3 scripts/seedance_lint.py --confirmed "<prompt>"     # log as confirmed workaround

Settings (aspect ratio / resolution / mode / duration) are read from the
prompt's settings header lines (e.g. `**Aspect ratio**: 16:9  **Duration**: 8s`)
and can be overridden per-field with --ar / --resolution / --mode / --duration.

Exit codes: 0 = PASS or WARN only, 1 = any FAIL, 2 = usage error.

Filter-memory loopback:
  --log         → on FAIL, append an entry to db/filter-memory.json with
                  outcome=unknown. Rule hits become blocked_terms + tags.
  --confirmed   → append the prompt as a confirmed workaround (outcome=
                  workaround, substitution_worked=True). Use after a rewrite
                  passes Seedance's filter in a real generation.

  To update an existing entry's outcome later:
    python3 scripts/higgsfield_memory.py update-filter <id> <outcome>
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


# ── Rule data ───────────────────────────────────────────────────────────────

# Real person / public figure name patterns. Not exhaustive — Seedance's filter
# has a much larger list internally — but these are the ones users repeatedly
# hit in our filter-memory database.
REAL_NAMES = [
    r"\belon musk\b", r"\bdonald trump\b", r"\bjoe biden\b", r"\bkamala harris\b",
    r"\bvladimir putin\b", r"\bxi jinping\b", r"\bbarack obama\b",
    r"\bkeanu reeves\b", r"\btom cruise\b", r"\bbrad pitt\b", r"\bleonardo dicaprio\b",
    r"\btaylor swift\b", r"\bbeyonc[eé]\b", r"\brihanna\b", r"\bkanye\b",
    # 'ye' (Kanye's stage name) was dropped — it collides with archaic English
    # ('ye gods', 'hear ye') and 'kanye' above already covers the artist.
    # 'drake' collides with the waterfowl / surname (Francis Drake); exclude the
    # common innocent collocations so the rapper still trips the rule but a duck
    # doesn't block an otherwise clean prompt.
    r"\bkim kardashian\b",
    r"(?<!francis )(?<!a )(?<!the )(?<!male )\bdrake\b(?!'s equation)(?! duck)",
    r"\btravis scott\b",
    r"\bmessi\b", r"\bronaldo\b", r"\blebron\b", r"\bmichael jordan\b",
    r"\bmr beast\b", r"\bmrbeast\b",
]

# Brands, IPs, trademarked characters. Same story — representative, not exhaustive.
BRANDS_IP = [
    r"\bnike\b", r"\badidas\b", r"\bpuma\b", r"\bgucci\b", r"\bprada\b", r"\blouis vuitton\b",
    r"\bcoca[- ]cola\b", r"\bpepsi\b", r"\bmcdonald'?s\b", r"\bstarbucks\b",
    r"\bapple\b(?! (pie|tree|orchard|falls|juice))", r"\biphone\b", r"\bmacbook\b",
    r"\bgoogle\b", r"\bmicrosoft\b", r"\bwindows\b(?! (are|were|of|into|into))",
    r"\btesla\b", r"\bferrari\b", r"\blamborghini\b", r"\bporsche\b", r"\brolex\b",
    r"\bmarvel\b", r"\bdc comics\b", r"\bdisney\b", r"\bpixar\b", r"\bdreamworks\b",
    r"\bspider[- ]?man\b", r"\bbatman\b", r"\bsuperman\b", r"\biron man\b",
    r"\bcaptain america\b", r"\bthor\b", r"\bhulk\b", r"\bblack widow\b",
    r"\bwolverine\b", r"\bdeadpool\b", r"\bharry potter\b", r"\bhogwarts\b",
    r"\bpok[eé]mon\b", r"\bpikachu\b", r"\bmario\b", r"\bsonic\b",
    r"\bstar wars\b", r"\bjedi\b", r"\bsith\b", r"\bdarth vader\b",
    r"\bjames bond\b", r"\b007\b",
]

# Raw violence / harm verbs. Seedance flags the verb, not the concept — the
# concept can be rendered cinematically via aftermath/tension/physics.
VIOLENCE_VERBS = [
    r"\bkill(s|ed|ing)?\b", r"\bmurder(s|ed|ing)?\b", r"\bassassinat(e|es|ed|ing)\b",
    r"\bstab(s|bed|bing)?\b", r"\bshoot(s|ing)?\b",
    # "shot" is the most common noun in film prompting (two-shot, wide shot,
    # shot 3, per shot) — flag only verb/violence constructions, never the
    # cinematography noun.
    r"\bshot\b(?=\s+(him|her|them|dead|twice|through\b|at\b|in the\b))",
    r"\b(was|is|are|being|gets?|got|been)\s+shot\b",
    r"\bslash(es|ed|ing)?\b", r"\bbehead(s|ed|ing)?\b", r"\bdecapitat(e|es|ed|ing)\b",
    r"\btortur(e|es|ed|ing)\b", r"\brap(e|es|ed|ing)\b",
    r"\bblood(y|ied|ying)?\b", r"\bgore\b", r"\bgory\b", r"\bgutted?\b",
    r"\bdismember(s|ed|ing)?\b", r"\bmutilat(e|es|ed|ing)\b",
    r"\bfight(s|ing)?\b", r"\battack(s|ed|ing)?\b", r"\bpunch(es|ed|ing)?\b",
    r"\bbeating\b", r"\bbeat(s|en)?\b(?! (the|up the) (rug|eggs|drum|heat|path|odds))",
]

WEAPON_NOUNS = [
    r"\bgun\b", r"\brifle\b", r"\bpistol\b", r"\bshotgun\b", r"\bhandgun\b",
    r"\bmachine gun\b", r"\bak[- ]?47\b", r"\bm16\b", r"\buzi\b",
    r"\bknife\b", r"\bdagger\b", r"\bsword\b(?! (fern|fish|dance))",
    r"\bbomb\b", r"\bgrenade\b", r"\bexplosive\b",
]

AGE_MARKERS = [
    r"\bchild(ren)?\b", r"\bkid(s|dies)?\b", r"\bbaby\b", r"\binfant\b", r"\btoddler\b",
    r"\bboy(s)?\b", r"\bgirl(s)?\b", r"\bteen(ager|agers|aged)?\b",
    r"\byoung (man|woman|boy|girl)\b", r"\blittle (boy|girl|kid|child)\b",
    r"\bminor(s)?\b(?! (chord|key|scale|league|issue|detail))",
    r"\bschoolboy\b", r"\bschoolgirl\b", r"\bpreschool(er)?\b",
]

# Antislop — marketing-copy adjectives that correlate with vague prompts and
# therefore with filter flags. Warn, don't fail.
ANTISLOP = [
    r"\bbreathtaking\b", r"\bstunning\b", r"\bepic\b", r"\bmesmerizing\b",
    r"\bawe[- ]inspiring\b", r"\bmasterfully\b", r"\bmeticulously\b",
    r"\bexquisitely\b", r"\bbeautifully crafted\b", r"\bcinematic masterpiece\b",
    r"\bvisual feast\b", r"\bseamlessly\b", r"\beffortlessly\b", r"\bflawlessly\b",
    r"\bcutting[- ]edge\b", r"\bstate[- ]of[- ]the[- ]art\b",
    r"\bmind[- ]blowing\b", r"\bjaw[- ]dropping\b",
]

# Antislop, ZH edition — the house-format equivalents of the EN list above.
# Source: docs/Seedance 2 Skill.md (bilingual-JSON profile), forbidden-terms
# section. Same severity logic: WARN, with a nudge toward concrete vocabulary.
ANTISLOP_ZH = [
    "令人叹为观止", "令人惊叹", "令人着迷", "精心打造", "匠心独运", "独具匠心",
    "视觉盛宴", "光影交响", "完美呈现", "极致体验", "引人入胜", "震撼人心", "巧妙融合",
]

# ZH prompt hard cap (chars). Source: docs/Seedance 2 Skill.md output contract.
ZH_CHAR_CAP = 1800
CJK_RE = re.compile(r"[一-鿿]")

# Shot-block markers. The 【镜头N】 ("shot N") marker is a community
# shot-delimiter convention, NOT a Seedance-native parse token — its absence
# across the entire audit corpus (3h47m of transcripts + 16 slides + the
# 604-line director skill + the v3.8.0 working-folder corpus) is the
# resolved-by-absence finding behind backlog G13. Flag it as a visual
# delimiter only, so users don't expect the platform to honor it structurally.
SHOT_BLOCK_MARKERS = [r"【[^】]*】", r"\[\s*镜头\s*\d+\s*\]"]

# Timed beat brackets like [0-2s]. Valid Seedance vocab (see vocab.md). Flagged
# only when malformed (empty or reversed) — a well-formed beat bracket is fine.
TIMED_BEAT_OK = re.compile(r"\[\s*\d+\s*[-–]\s*\d+\s*s\s*\]")
TIMED_BEAT_MALFORMED = re.compile(r"\[\s*[-–]?\s*s\s*\]|\[\s*\d+\s*[-–]\s*s\s*\]")

# Dual-use words that read as innocent in context but repeatedly trip
# provider-side NSFW *false* positives (the D9 finding). NOT a content
# violation — a disambiguation nudge. Real NSFW terms are out of scope here;
# these are the ambiguous-innocent ones (bare branches, wet pavement, strip of
# fabric, exposed brick, the skin of an apple).
NSFW_FALSE_POSITIVE = [
    r"\bstrip(s|ped|ping)?\b(?! (mall|club))", r"\bbare\b", r"\bexposed?\b",
    r"\bskin\b", r"\bwet\b", r"\bintimate\b", r"\bsensual\b", r"\bseductive\b",
    r"\bcaress(es|ed|ing)?\b", r"\bmoan(s|ed|ing)?\b",
]

# GREAT-tier photographer vocabulary — concrete replacements for vague,
# "good-looking" filler. Surfaced as an INFO nudge when antislop fires, so the
# rewrite has somewhere specific to go (Stage 2 Hack 2 vocabulary table).
GREAT_TIER_VOCAB = [
    "lens — 35mm / 50mm / 85mm / anamorphic",
    "lighting — golden-hour backlight, hard key + soft fill, practical neon, Rembrandt",
    "grade — teal-and-orange, bleach-bypass, desaturated film, crushed blacks",
    "texture — 35mm grain, halation, gate weave, shallow depth of field",
    "camera body — clean digital / fine film / raw 16mm",
]

# Sections the filter wants to see — presence of these clauses strongly
# correlates with passing. Detected by keyword cues, not strict parsing.
STYLE_MOOD_CUES = [
    "style", "mood", "palette", "color grade", "lighting", "atmosphere",
    "golden hour", "blue hour", "overcast", "neon", "practical", "noir",
    "desaturated", "teal and orange", "high contrast", "low[- ]key",
    "anamorphic", "vhs", "super 8", "cinematic",
]
CAMERA_CUES = [
    "camera", "dolly", "tracking", "pan", "tilt", "crane", "steadicam",
    "handheld", "aerial", "drone", "pov", "push[- ]in", "pull[- ]out",
    "orbit", "whip[- ]pan", "low[- ]angle", "high[- ]angle", "overhead",
    "wide shot", "medium shot", "close[- ]up", "ecu", "ots", "over the shoulder",
]
SETTING_CUES = [
    # Any concrete noun-ish location word. Tiny heuristic — looks for common
    # location descriptors.
    "room", "hall", "street", "alley", "forest", "desert", "beach",
    "kitchen", "bedroom", "office", "warehouse", "studio", "stage",
    "city", "town", "village", "rooftop", "stairwell", "parking",
    "interior", "exterior", "indoor", "outdoor", "indoors", "outdoors",
    "at night", "by day", "at dawn", "at dusk",
]


@dataclass
class Finding:
    severity: str  # "FAIL" | "WARN" | "INFO"
    rule: str
    hit: str
    fix: str


@dataclass
class Settings:
    """Generation settings declared for the prompt (header lines or CLI)."""
    ar: str | None = None
    resolution: str | None = None
    mode: str | None = None
    duration: int | None = None
    extension_mode: str | None = None


SPECS_DEFAULT = Path(__file__).resolve().parent.parent / "specs" / "model-specs.json"

_SETTINGS_PATTERNS = {
    # Tolerant of **bold**, fullwidth ：, and inline comma-run headers.
    "ar": re.compile(r"aspect[\s_-]*ratio\**\s*[:：]\s*\**\s*(auto|\d+:\d+)", re.I),
    "resolution": re.compile(r"\bresolution\**\s*[:：]\s*\**\s*(\d{3,4}p?|4k)", re.I),
    # extension_mode must be matched BEFORE the bare `mode` pattern can claim it —
    # merge_settings/parse order keeps them distinct because the `mode` regex
    # requires a word boundary that `extension_mode` does not satisfy.
    "extension_mode": re.compile(
        r"\bextension[\s_-]*mode\**\s*[:：]\s*\**\s*(forward|backward)", re.I),
    "mode": re.compile(r"(?<!extension[\s_-])\bmode\**\s*[:：]\s*\**\s*([a-z0-9_]+)", re.I),
    "duration": re.compile(r"\bduration\**\s*[:：]\s*\**\s*(\d+)\s*s", re.I),
}


def parse_settings_header(text: str) -> Settings:
    """Read declared settings out of the prompt's own header lines."""
    s = Settings()
    for field, pat in _SETTINGS_PATTERNS.items():
        m = pat.search(text)
        if m:
            value = m.group(1).lower()
            setattr(s, field, int(value) if field == "duration" else value)
    return s


def merge_settings(header: Settings, cli: Settings) -> Settings:
    """CLI flags win per-field over header-declared values."""
    return Settings(
        ar=cli.ar or header.ar,
        resolution=cli.resolution or header.resolution,
        mode=cli.mode or header.mode,
        duration=cli.duration if cli.duration is not None else header.duration,
        extension_mode=cli.extension_mode or header.extension_mode,
    )


def load_specs(path: Path) -> dict:
    """Index specs/model-specs.json by id, alias, and normalized name.

    Returns {} when the specs file is absent — structural enum checks then
    degrade to INFO, they never guess."""
    try:
        spec = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    if not spec.get("models"):
        return {}
    index: dict[str, dict] = {}
    for m in spec["models"]:
        index[m["id"]] = m
        for alias in m.get("aliases", []):
            index[alias] = m
        index[re.sub(r"[^a-z0-9]+", "", m["name"].lower())] = m
    index["_snapshot_date"] = spec.get("snapshot_date")
    return index


def snapshot_age_finding(index: dict) -> "Finding | None":
    """INFO finding when the specs snapshot is past the 30-day trust line.

    The enum checks cite the snapshot as authority (never guess enums); past
    30 days the HARD RULES say to verify live instead, so the report must say
    so rather than fail/pass with silent stale confidence."""
    stamp = index.get("_snapshot_date")
    if not stamp:
        return None
    try:
        age = (date.today() - date.fromisoformat(stamp)).days
    except ValueError:
        return None
    if age > 30:
        return Finding(
            "INFO", "stale-specs-snapshot", f"{stamp} ({age}d old)",
            "Specs snapshot exceeds the 30-day trust window (root SKILL.md "
            "HARD RULES 3/7) — enum verdicts below may be stale. Verify live "
            "(`higgsfield model get <model>` / models_explore) and refresh "
            "via scripts/sync_specs.py.")
    return None


def resolve_model(index: dict, model_arg: str) -> dict | None:
    return index.get(model_arg) or index.get(
        re.sub(r"[^a-z0-9]+", "", model_arg.lower()))


# Shot-count declarations, EN + ZH house format.
DECLARED_SHOTS_RES = [
    re.compile(r"strictly\s+(\d+)\s+shots?", re.I),
    re.compile(r"严格\s*(\d+)\s*个?镜头"),
    re.compile(r"(\d+)\s*个镜头"),
]
SHOT_BLOCK_RES = [re.compile(r"【\s*镜头\s*(\d+)\s*】"),
                  re.compile(r"\[\s*Shot\s*(\d+)\s*\]", re.I)]

# Canonical block-scaffold labels (skills/higgsfield-seedance § Official
# Prompt Architecture → Block order). A prompt opening on these blocks is the
# production regime: structure replaces the word cap (HARD RULE 8 carve-out),
# so the short-form length rules must not fire on it.
BLOCK_SCAFFOLD_LABELS = [
    "SCENE CONTEXT", "ACTIVE REFERENCES", "LOCATION MAP",
    "FIRST FRAME", "BLOCKING", "FORMAT MODE", "OPTICS", "CAMERA", "ACTION",
    "PERFORMANCE", "PHYSICS", "LIGHTING", "COLOR GRADE", "WARDROBE",
    "AUDIO", "STYLE", "OUTPUT SETTINGS", "POSITIVE LOCKS",
]
BLOCK_LABEL_RE = re.compile(
    r"^\s*(" + "|".join(re.escape(l) for l in BLOCK_SCAFFOLD_LABELS) + r")\b\s*:?",
    re.M)
BLOCK_REGIME_MIN_LABELS = 4


def detect_regime(text: str) -> str:
    """'block' (block-scaffold production prompt) or 'short' (single-shot MCSLA).

    Block regime is recognized from structure, never from length: at least
    BLOCK_REGIME_MIN_LABELS distinct canonical block labels at line starts,
    or 2+ 【镜头N】/[Shot N] shot-block markers (the shotlist copy-block form).
    """
    labels = {m.group(1) for m in BLOCK_LABEL_RE.finditer(text)}
    if len(labels) >= BLOCK_REGIME_MIN_LABELS:
        return "block"
    shots = {int(m.group(1)) for pat in SHOT_BLOCK_RES for m in pat.finditer(text)}
    if len(shots) >= 2:
        return "block"
    return "short"
TIMED_BEAT_RANGE = re.compile(r"\[\s*(\d+)\s*[–-]\s*(\d+)\s*s\s*\]")
HANDLE_RE = re.compile(r"@([\w-]+)")
HANDLE_DECL_RE = re.compile(r"^\s*[*\-•]?\s*\**@([\w-]+)\**\s*[:=（(—–]")


def structural_lint(text: str, settings: Settings, spec: dict | None) -> list[Finding]:
    """Structural preflight: the failures that waste credits, not the ones
    that trip the content filter. Enum legality comes ONLY from the specs
    layer — when no model/spec is available the checks downgrade to INFO."""
    findings: list[Finding] = []

    # ── Shot count: declared vs actual block markers ─────────────────────
    declared = None
    for pat in DECLARED_SHOTS_RES:
        m = pat.search(text)
        if m:
            declared = int(m.group(1))
            break
    actual = len({int(m.group(1)) for pat in SHOT_BLOCK_RES
                  for m in pat.finditer(text)})
    if declared is not None and actual and declared != actual:
        findings.append(Finding(
            "FAIL", "shot-count-mismatch", f"declared {declared}, found {actual} blocks",
            "The declared shot count must equal the number of 【镜头N】/[Shot N] "
            "blocks — a mismatch makes the engine improvise cuts."))
    elif declared is not None and not actual and not TIMED_BEAT_RANGE.search(text):
        findings.append(Finding(
            "WARN", "declared-shots-unstructured",
            f"declared {declared} shots, found 0 blocks and no timed beats",
            "A declared shot count needs structure to bind to — add "
            "【镜头N】/[Shot N] blocks or timed beats ([0-2s] …), otherwise "
            "the engine improvises the cuts."))

    # ── Beat durations vs envelope ───────────────────────────────────────
    beats = [(int(a), int(b)) for a, b in TIMED_BEAT_RANGE.findall(text)]
    if beats:
        for a, b in beats:
            if b <= a:
                findings.append(Finding(
                    "WARN", "reversed-beat", f"[{a}-{b}s]",
                    "Beat range end must be after its start."))
        # Timeline shape: beats must tile the clip — ordered, seamless, from 0.
        ordered = sorted(b for b in beats if b[1] > b[0])
        if ordered:
            if ordered[0][0] != 0:
                findings.append(Finding(
                    "WARN", "beats-start-late", f"first beat opens at {ordered[0][0]}s",
                    "The beat timeline should start at [0-…s] — the engine "
                    "improvises everything before the first beat."))
            for (a1, b1), (a2, b2) in zip(ordered, ordered[1:]):
                if a2 < b1:
                    findings.append(Finding(
                        "WARN", "overlapping-beats", f"[{a1}-{b1}s] overlaps [{a2}-{b2}s]",
                        "Beat ranges must not overlap — overlapping windows "
                        "give the engine two owners for the same seconds."))
                elif a2 > b1:
                    findings.append(Finding(
                        "WARN", "beat-gap", f"{b1}s → {a2}s uncovered",
                        "Gap between beats — the engine improvises uncovered "
                        "seconds. Make ranges contiguous ([0-2s][2-4s]…)."))
        end = max(b for _, b in beats)
        envelope = settings.duration
        env_src = "declared duration"
        if envelope is None and spec and spec.get("duration"):
            d = spec["duration"]
            envelope = d["max"] if "max" in d else max(d["values"])
            env_src = f"{spec['id']} max duration"
        if envelope is not None and end > envelope:
            findings.append(Finding(
                "FAIL", "beats-exceed-envelope", f"beats run to {end}s, {env_src} is {envelope}s",
                "Timed beats must fit inside the clip duration — trailing "
                "beats are silently truncated."))
        elif settings.duration is not None and end < settings.duration:
            findings.append(Finding(
                "WARN", "beats-undershoot-envelope",
                f"beats end at {end}s, declared duration is {settings.duration}s",
                "Beats should sum exactly to the clip duration — trailing "
                "uncovered seconds are improvised dead air."))

    # ── ZH house-format checks ───────────────────────────────────────────
    if CJK_RE.search(text):
        if len(text) > ZH_CHAR_CAP:
            findings.append(Finding(
                "FAIL", "zh-overlength", f"{len(text)} chars",
                f"ZH prompts hard-cap at {ZH_CHAR_CAP} characters "
                "(docs/Seedance 2 Skill.md output contract). Cut scene-setting "
                "prose; keep blocking, camera, and audio cues."))
        zh_hits = [t for t in ANTISLOP_ZH if t in text]
        if zh_hits:
            findings.append(Finding(
                "WARN", "zh-antislop", ", ".join(zh_hits),
                "ZH marketing-copy phrases correlate with vague prompts. "
                "Replace with observable detail (lens, light source, texture)."))

    # ── @handle declared before use ──────────────────────────────────────
    declared_handles: dict[str, int] = {}
    for i, line in enumerate(text.splitlines()):
        m = HANDLE_DECL_RE.match(line)
        if m:
            declared_handles.setdefault(m.group(1).lower(), i)
    if declared_handles:
        for i, line in enumerate(text.splitlines()):
            for m in HANDLE_RE.finditer(line):
                h = m.group(1).lower()
                decl_line = declared_handles.get(h)
                if decl_line is None:
                    findings.append(Finding(
                        "FAIL", "undeclared-handle", f"@{m.group(1)}",
                        "Other handles are declared in this prompt but this one "
                        "never is — declare it (`@Name: description`) before use."))
                elif i < decl_line:
                    findings.append(Finding(
                        "FAIL", "handle-used-before-declared", f"@{m.group(1)}",
                        "Move the @handle declaration above its first use."))
            # only report each handle once
        # dedupe by (rule, hit)
        seen = set()
        findings = [f for f in findings
                    if (f.rule, f.hit) not in seen and not seen.add((f.rule, f.hit))]
    else:
        used = sorted({m.group(1) for m in HANDLE_RE.finditer(text)})
        if used:
            findings.append(Finding(
                "WARN", "handles-not-declared-in-prompt",
                ", ".join(f"@{h}" for h in used),
                "No @handle declarations found in the prompt. Fine if they're "
                "bound in the UI Elements panel — otherwise declare each "
                "(`@Name: description`) before first use."))

    # ── Enum legality per specs ──────────────────────────────────────────
    declared_any = any([settings.ar, settings.resolution, settings.mode,
                        settings.duration is not None])
    if spec is None:
        if declared_any:
            findings.append(Finding(
                "INFO", "enums-not-checked", "",
                "No --model given (or specs file missing) — aspect ratio / "
                "resolution / mode / duration legality not checked. Pass "
                "--model <id> to validate against specs/model-specs.json."))
        return findings

    def enum_check(value, allowed, rule, label):
        if value is not None and allowed and value not in [str(a).lower() for a in allowed]:
            findings.append(Finding(
                "FAIL", rule, f"{label} {value!r}",
                f"{spec['name']} ({spec['id']}) supports {label}: "
                f"{', '.join(map(str, allowed))} — per specs/model-specs.json "
                f"(snapshot-driven; never guess enums)."))

    enum_check(settings.ar, spec.get("aspect_ratios"), "ar-not-supported", "aspect ratio")
    enum_check(settings.resolution, spec.get("resolutions"),
               "resolution-not-supported", "resolution")
    enum_check(settings.mode, spec.get("modes"), "mode-not-supported", "mode")

    if settings.duration is not None and spec.get("duration"):
        d = spec["duration"]
        if "min" in d:
            ok = d["min"] <= settings.duration <= d["max"]
            allowed_fmt = f"{d['min']}–{d['max']}s"
        else:
            ok = settings.duration in d["values"]
            allowed_fmt = "/".join(map(str, d["values"])) + "s"
        if not ok:
            findings.append(Finding(
                "FAIL", "duration-out-of-range", f"{settings.duration}s",
                f"{spec['name']} supports {allowed_fmt}."))

    # Cross-parameter constraints from the snapshot (e.g. fast forbids 1080p).
    declared_map = {"mode": settings.mode, "resolution": settings.resolution,
                    "aspect_ratio": settings.ar,
                    "duration": str(settings.duration) if settings.duration is not None else None}
    for c in spec.get("constraints", []):
        if declared_map.get(c["param"]) != str(c["value"]).lower():
            continue
        for other, forbidden in c.get("forbids", {}).items():
            val = declared_map.get(other)
            if val is not None and val in [str(v).lower() for v in forbidden]:
                findings.append(Finding(
                    "FAIL", "mode-constraint",
                    f"{c['param']}={c['value']} + {other}={val}",
                    f"Illegal combination on {spec['name']}: {c['source']}. "
                    f"Drop one side (e.g. std mode for 1080p)."))
        for other, required in c.get("requires", {}).items():
            val = declared_map.get(other)
            if val is None:
                findings.append(Finding(
                    "WARN", "constraint-requires",
                    f"{c['param']}={c['value']} requires {other}={required}",
                    f"{c['source']} — declare {other} explicitly so the "
                    "combination is verifiable."))
            elif val != str(required).lower():
                findings.append(Finding(
                    "FAIL", "constraint-requires",
                    f"{c['param']}={c['value']} requires {other}={required}, got {val}",
                    f"Illegal combination on {spec['name']}: {c['source']}."))

    findings.extend(_mode_pairing_findings(spec, settings))
    return findings


def _mode_pairing_findings(spec: dict, settings: Settings) -> list[Finding]:
    """Cross-parameter rules stated in prose that sync_specs cannot extract.

    sync_specs.py only lifts constraints whose wording it recognizes AND whose
    tokens are legal enum values elsewhere in the same model. Seedance 2.5's
    `extension_mode` rule ("required for mode 'video_extension' and not allowed
    otherwise") and its video_edit parameter-ignoring rule are stated in prose
    the extractor does not match, so they are encoded here — keyed off the
    model's OWN parameter list, never off a hard-coded model id, so the checks
    disappear if the platform drops the parameter."""
    findings: list[Finding] = []
    param_names = {p.get("name") for p in spec.get("params", [])}
    modes = [str(m).lower() for m in spec.get("modes", [])]

    if "extension_mode" in param_names and "video_extension" in modes:
        if settings.mode == "video_extension" and settings.extension_mode is None:
            findings.append(Finding(
                "FAIL", "extension-mode-missing", "mode=video_extension",
                f"{spec['name']} requires extension_mode (forward|backward) in "
                f"video_extension mode — declare it, and align the boundary "
                f"frame in the prompt before describing new content."))
        elif settings.mode is not None and settings.mode != "video_extension" \
                and settings.extension_mode is not None:
            findings.append(Finding(
                "FAIL", "extension-mode-not-allowed",
                f"mode={settings.mode} + extension_mode={settings.extension_mode}",
                f"{spec['name']} accepts extension_mode ONLY in "
                f"video_extension mode — drop one side."))

    if settings.mode == "video_edit" and "video_edit" in modes:
        ignored = [f"{k}={v}" for k, v in
                   (("duration", settings.duration), ("aspect ratio", settings.ar))
                   if v is not None]
        if ignored:
            findings.append(Finding(
                "WARN", "video-edit-ignored-params", ", ".join(ignored),
                f"{spec['name']} ignores duration and aspect ratio in video_edit "
                f"mode — both follow the source video, and the render is billed "
                f"by the source's duration. Remove them so the declaration "
                f"matches what actually runs."))
    return findings


def recall(text: str, model_id: str | None, top_n: int = 2) -> list[Finding]:
    """Surface the most relevant past failures from the learning memory as
    INFO findings. Read-only; missing/corrupt DBs degrade to a single INFO."""
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        from higgsfield_memory import (FILTER_DB, QUALITY_DB, relevance_score,
                                       tokenize)
        query = tokenize(text + " " + (model_id or "seedance"))
        findings: list[Finding] = []
        for label, path in (("filter-memory", FILTER_DB), ("quality-memory", QUALITY_DB)):
            try:
                entries = json.loads(path.read_text(encoding="utf-8")).get("entries", [])
            except (OSError, json.JSONDecodeError):
                continue
            scored = sorted(((relevance_score(e, query), e) for e in entries),
                            key=lambda x: x[0], reverse=True)
            for score, e in scored[:top_n]:
                if score <= 0:
                    continue
                lesson = (e.get("substitution") or e.get("improved_prompt")
                          or e.get("failure_description") or e.get("notes") or "")
                findings.append(Finding(
                    "INFO", "memory-recall",
                    f"{e.get('id', '?')} ({e.get('category') or e.get('failure_type', '?')}, "
                    f"outcome={e.get('outcome', 'unknown')})",
                    f"[{label}] {str(lesson)[:180]}"))
        return findings
    except Exception as e:  # noqa: BLE001 — recall must never block a preflight
        return [Finding("INFO", "memory-recall-unavailable", "",
                        f"learning-memory lookup failed: {e}")]


def _matches(patterns: list[str], text: str) -> list[str]:
    hits: list[str] = []
    for pat in patterns:
        for m in re.finditer(pat, text, flags=re.IGNORECASE):
            hits.append(m.group(0))
    return hits


def _has_cue(cues: list[str], text: str) -> bool:
    lowered = text.lower()
    return any(re.search(c, lowered) for c in cues)


def lint(prompt: str, regime: str = "auto") -> list[Finding]:
    findings: list[Finding] = []
    text = prompt.strip()
    word_count = len(re.findall(r"\b\w+\b", text))

    if not text:
        findings.append(Finding("FAIL", "empty", "", "Prompt is empty."))
        return findings

    if regime == "auto":
        regime = detect_regime(text)
    if regime == "block":
        findings.append(Finding(
            "INFO", "block-scaffold-regime", "",
            "Block-scaffold production prompt detected — short-form word caps "
            "suspended (HARD RULE 8 regime exception; harvested production "
            "briefs run 218–2,059-word medians). All content-filter and "
            "structural rules still apply. Force with --regime short|block "
            "if the detection is wrong."
        ))

    # ── FAIL rules ──────────────────────────────────────────────────────────

    hits = _matches(REAL_NAMES, text)
    if hits:
        findings.append(Finding(
            "FAIL", "real-person-name", ", ".join(sorted(set(hits))),
            "Replace the name with an archetype: age range, build, hair, "
            "wardrobe, expression. See higgsfield-seedance rewrite playbook."
        ))

    hits = _matches(BRANDS_IP, text)
    if hits:
        findings.append(Finding(
            "FAIL", "brand-ip", ", ".join(sorted(set(hits))),
            "Describe visual traits only — geometry, color, material. Never "
            "name the brand, franchise, or character."
        ))

    hits = _matches(VIOLENCE_VERBS, text)
    if hits:
        findings.append(Finding(
            "FAIL", "violence-verb", ", ".join(sorted(set(hits))),
            "Describe aftermath, tension, force, or direction — not the act. "
            "E.g. 'driven into the car, metal buckling' instead of 'punches'."
        ))

    hits = _matches(WEAPON_NOUNS, text)
    if hits:
        findings.append(Finding(
            "FAIL", "weapon-noun", ", ".join(sorted(set(hits))),
            "Describe the standoff / silhouette / prop geometry, not the "
            "weapon by name. The filter reads named weapons as intent."
        ))

    hits = _matches(AGE_MARKERS, text)
    if hits:
        findings.append(Finding(
            "FAIL", "age-marker", ", ".join(sorted(set(hits))),
            "Seedance is age-blind. Describe by role + clothing + action: "
            "'a figure in a wool cloak', 'the rider', 'the traveler'."
        ))

    if regime == "short" and word_count > 220:
        findings.append(Finding(
            "FAIL", "overlength", f"{word_count} words",
            "Over 220 words often hard-fails the text encoder on short-form "
            "prompts. Cut to 30–180 words (Style & Mood + camera + action), "
            "or restructure as a block-scaffold production prompt "
            "(skills/higgsfield-seedance § Official Prompt Architecture) — "
            "the word cap does not govern that regime."
        ))

    # ── WARN rules ──────────────────────────────────────────────────────────

    hits = _matches(ANTISLOP, text)
    if hits:
        findings.append(Finding(
            "WARN", "antislop", ", ".join(sorted(set(hits))),
            "Marketing-copy adjectives correlate with flags — they signal "
            "vague intent. Replace with observable, measurable details. "
            "GREAT-tier vocabulary to reach for: "
            + "; ".join(GREAT_TIER_VOCAB) + "."
        ))

    hits = _matches(NSFW_FALSE_POSITIVE, text)
    if hits:
        findings.append(Finding(
            "WARN", "nsfw-false-positive", ", ".join(sorted(set(hits))),
            "Reads innocent in context but repeatedly trips a provider-side "
            "NSFW false-positive. Disambiguate the noun it modifies — "
            "'bare branches', 'wet pavement', 'strip of fabric', 'exposed "
            "brick', 'the skin of the apple' — so the filter can't misread it."
        ))

    if TIMED_BEAT_MALFORMED.search(text):
        findings.append(Finding(
            "WARN", "malformed-beat", "",
            "Malformed timed-beat bracket. Use a complete range like "
            "'[0-2s]' / '[2-4s]'. An empty or half-open bracket reads as noise."
        ))

    if regime == "short" and word_count > 180:
        findings.append(Finding(
            "WARN", "long", f"{word_count} words",
            "Over 180 words is risk territory for short-form prompts. Trim "
            "the least essential details before generating."
        ))

    if word_count < 15:
        findings.append(Finding(
            "WARN", "too-short", f"{word_count} words",
            "Too short — the filter has no scene to interpret. Add at least "
            "Style & Mood + camera + setting so the shot is legible."
        ))

    if not _has_cue(STYLE_MOOD_CUES, text):
        findings.append(Finding(
            "WARN", "no-style-mood", "",
            "No Style / Mood / lighting / palette clause detected. Add one "
            "sentence naming the palette, lighting, and atmosphere."
        ))

    if not _has_cue(CAMERA_CUES, text):
        findings.append(Finding(
            "WARN", "no-camera", "",
            "No camera move detected. Name an exact movement: 'slow dolly-in', "
            "'low-angle tracking', 'static medium'. Not 'the camera moves'."
        ))

    if not _has_cue(SETTING_CUES, text):
        findings.append(Finding(
            "WARN", "no-setting", "",
            "No concrete setting detected. Add a location so the filter has "
            "a scene to interpret (interior/exterior, room type, time of day)."
        ))

    # ── Contradictions (INFO — heuristic) ───────────────────────────────────

    lowered = text.lower()
    contradictions = [
        (("moving fast", "frozen"), "Moving fast + frozen in the same scene."),
        (("bright", "pitch black"), "Bright + pitch black in the same scene."),
        (("dolly in", "dolly out"), "Dolly in and dolly out in the same shot."),
        (("crane up", "crane down"), "Crane up and crane down in the same shot."),
        (("zoom in", "zoom out"), "Zoom in and zoom out in the same shot."),
    ]
    for (a, b), message in contradictions:
        if a in lowered and b in lowered:
            findings.append(Finding(
                "WARN", "contradiction", f"{a} + {b}",
                message + " Pick one — split into two shots if you need both."
            ))

    block_hits = _matches(SHOT_BLOCK_MARKERS, text)
    if block_hits:
        findings.append(Finding(
            "INFO", "shot-block-marker", ", ".join(sorted(set(block_hits))),
            "【镜头N】-style block markers are a community shot-delimiter "
            "convention, not a Seedance-native parse token — the platform "
            "does not honor them structurally. Use them only as a visual "
            "delimiter, or structure multi-shot prompts with timed beats "
            "([0-2s] ...) instead."
        ))

    return findings


def render(prompt: str, findings: list[Finding]) -> tuple[str, str]:
    """Return (verdict, report text). Verdict is PASS / WARN / FAIL."""
    fails = [f for f in findings if f.severity == "FAIL"]
    warns = [f for f in findings if f.severity == "WARN"]

    if fails:
        verdict = "FAIL"
    elif warns:
        verdict = "WARN"
    else:
        verdict = "PASS"

    lines: list[str] = []
    lines.append(f"Seedance Preflight — {verdict}")
    lines.append("=" * 40)
    word_count = len(re.findall(r"\b\w+\b", prompt.strip()))
    lines.append(f"  words: {word_count}")
    lines.append("")

    if not findings:
        lines.append("  No issues detected. Scene reads as a filmmaker shot.")
        lines.append("  Safe to generate.")
        return verdict, "\n".join(lines)

    for f in findings:
        tag = {"FAIL": "✗", "WARN": "⚠", "INFO": "·"}[f.severity]
        head = f"  {tag} [{f.severity}] {f.rule}"
        if f.hit:
            head += f" — {f.hit}"
        lines.append(head)
        lines.append(f"      fix: {f.fix}")
        lines.append("")

    if verdict == "FAIL":
        lines.append("  Do NOT generate. Apply fixes above, re-run linter.")
    elif verdict == "WARN":
        lines.append("  Likely to pass, but harden the weak spots first.")

    return verdict, "\n".join(lines)


def render_preflight(prompt: str, filter_findings: list[Finding],
                     structural: list[Finding], memory: list[Finding]) -> tuple[str, str]:
    """Single chained report: filter lint → structural lint → memory recall."""
    all_findings = filter_findings + structural + memory
    fails = [f for f in all_findings if f.severity == "FAIL"]
    warns = [f for f in all_findings if f.severity == "WARN"]
    verdict = "FAIL" if fails else ("WARN" if warns else "PASS")

    word_count = len(re.findall(r"\b\w+\b", prompt.strip()))
    lines = [f"Seedance Preflight — {verdict}", "=" * 40,
             f"  words: {word_count}", ""]

    def section(title: str, findings: list[Finding], empty_note: str):
        lines.append(f"── {title} " + "─" * max(0, 36 - len(title)))
        if not findings:
            lines.append(f"  {empty_note}")
            lines.append("")
            return
        for f in findings:
            tag = {"FAIL": "✗", "WARN": "⚠", "INFO": "·"}[f.severity]
            head = f"  {tag} [{f.severity}] {f.rule}"
            if f.hit:
                head += f" — {f.hit}"
            lines.append(head)
            lines.append(f"      fix: {f.fix}")
        lines.append("")

    section("FILTER LINT", filter_findings, "clean — reads as a filmmaker shot")
    section("STRUCTURE", structural, "no structural issues detected")
    section("MEMORY RECALL", memory, "no relevant past failures on record")

    if verdict == "FAIL":
        lines.append("  Do NOT generate. Apply fixes above, re-run preflight.")
    elif verdict == "WARN":
        lines.append("  Likely to pass, but harden the weak spots first.")
    else:
        lines.append("  Safe to generate.")
    return verdict, "\n".join(lines)


def log_to_filter_memory(prompt: str, findings: list[Finding], confirmed: bool) -> str:
    """
    Append an entry to db/filter-memory.json. Imports the project's
    higgsfield_memory helpers (same directory) to stay schema-consistent
    with the validator's required fields.

    Returns the new entry id.
    """
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        from higgsfield_memory import load_db, save_db, next_id, now_iso, FILTER_DB
    except ImportError as e:
        print(json.dumps({"status": "error", "message": f"higgsfield_memory import failed: {e}"}))
        sys.exit(1)

    db = load_db(FILTER_DB)

    fails = [f for f in findings if f.severity == "FAIL"]
    warns = [f for f in findings if f.severity == "WARN"]

    categories = sorted({f.rule for f in fails}) or ["preflight-warn"]
    blocked = sorted({f.hit for f in fails if f.hit})
    fixes = "; ".join(f.fix for f in fails) or "; ".join(f.fix for f in warns)

    entry = {
        "id": next_id(db["entries"], "F"),
        "date_added": now_iso(),
        "category": categories[0],
        "blocked_terms": blocked,
        "error_message": (
            "Seedance preflight linter (confirmed workaround)"
            if confirmed
            else "Seedance preflight linter predicted filter rejection"
        ),
        "failed_prompt": prompt.strip()[:600],
        "substitution": fixes or None,
        "substitution_worked": True if confirmed else None,
        "fix_confirmed": confirmed,
        "outcome": "workaround" if confirmed else "unknown",
        "tags": ["seedance-2.0", "preflight-linter"] + categories,
        "notes": "",
    }

    db["entries"].append(entry)
    save_db(FILTER_DB, db)
    return entry["id"]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Preflight linter for Seedance 2.0 (and specs-known) prompts."
    )
    parser.add_argument("prompt", nargs="?", help="Prompt text (or use --file / stdin)")
    parser.add_argument("--file", "-f", help="Read prompt from file")
    parser.add_argument("--log", action="store_true",
                        help="On FAIL, append an entry to db/filter-memory.json")
    parser.add_argument("--confirmed", action="store_true",
                        help="Log prompt as a confirmed filter workaround "
                             "(outcome=workaround, substitution_worked=True)")
    parser.add_argument("--model", help="Model id/name from specs/model-specs.json "
                                        "(enables enum + constraint checks)")
    parser.add_argument("--ar", help="Declared aspect ratio (overrides prompt header)")
    parser.add_argument("--resolution", help="Declared resolution (overrides header)")
    parser.add_argument("--mode", help="Declared mode (overrides header)")
    parser.add_argument("--extension-mode", choices=["forward", "backward"],
                        help="Declared extension direction (Seedance 2.5 "
                             "video_extension mode; overrides header)")
    parser.add_argument("--duration", type=int,
                        help="Declared duration in seconds (overrides header)")
    parser.add_argument("--specs", type=Path, default=SPECS_DEFAULT,
                        help="Path to model-specs.json (default: specs/model-specs.json)")
    parser.add_argument("--preflight", action="store_true",
                        help="Full chained preflight: filter lint → structural "
                             "lint → learning-memory recall, one report")
    parser.add_argument("--regime", choices=["auto", "short", "block"],
                        default="auto",
                        help="Prompt regime: 'short' = single-shot MCSLA (word "
                             "caps apply), 'block' = block-scaffold production "
                             "prompt (word caps suspended per HARD RULE 8 "
                             "regime exception). Default 'auto' detects from "
                             "canonical block labels / shot markers.")
    parser.add_argument("--project", default="default",
                        help="Generation-ledger project for the --log bridge "
                             "(default: 'default'; see db/ledger/README.md)")
    args = parser.parse_args()

    if args.file:
        try:
            prompt = Path(args.file).read_text(encoding="utf-8")
        except OSError as e:
            print(f"ERROR: cannot read --file {args.file!r}: {e}", file=sys.stderr)
            return 2
    elif args.prompt:
        prompt = args.prompt
    elif not sys.stdin.isatty():
        prompt = sys.stdin.read()
    else:
        parser.print_help()
        return 2

    spec = None
    age_finding = None
    if args.model:
        index = load_specs(args.specs)
        age_finding = snapshot_age_finding(index)
        if not index:
            print(f"ERROR: specs file missing or invalid: {args.specs} — "
                  f"run: python3 scripts/sync_specs.py", file=sys.stderr)
            return 2
        spec = resolve_model(index, args.model)
        if spec is None:
            known = ", ".join(sorted(
                k for k in index if "_" in k and not k.startswith("_")))
            print(f"ERROR: unknown model {args.model!r}. Known ids: {known}",
                  file=sys.stderr)
            return 2

    settings = merge_settings(
        parse_settings_header(prompt),
        Settings(ar=args.ar.lower() if args.ar else None,
                 resolution=args.resolution.lower() if args.resolution else None,
                 mode=args.mode.lower() if args.mode else None,
                 duration=args.duration,
                 extension_mode=(args.extension_mode.lower()
                                 if args.extension_mode else None)))

    filter_findings = lint(prompt, regime=args.regime)
    run_structural = args.preflight or spec is not None or any(
        [settings.ar, settings.resolution, settings.mode, settings.duration is not None])
    structural = structural_lint(prompt, settings, spec) if run_structural else []
    if age_finding is not None:
        structural.insert(0, age_finding)

    if args.preflight:
        memory = recall(prompt, spec["id"] if spec else args.model)
        verdict, report = render_preflight(prompt, filter_findings, structural, memory)
        loggable = filter_findings + structural
    else:
        loggable = filter_findings + structural
        verdict, report = render(prompt, loggable)
    print(report)

    if args.confirmed:
        entry_id = log_to_filter_memory(prompt, loggable, confirmed=True)
        print(f"\n  logged as confirmed workaround → {entry_id}")
    elif args.log and verdict == "FAIL":
        entry_id = log_to_filter_memory(prompt, loggable, confirmed=False)
        print(f"\n  logged to filter-memory → {entry_id}")
        # Ledger bridge: a filter burn is a real generation attempt — it
        # belongs in the takes-per-kept denominator as outcome=flagged.
        if spec is not None:
            try:
                from higgsfield_memory import LedgerError, log_gen_row
                import hashlib
                row = log_gen_row(args.project, {
                    "model": spec["id"],
                    "shot_tags": [],
                    "outcome": "flagged",
                    "notes": "seedance preflight filter FAIL",
                    "prompt_hash": hashlib.sha1(
                        prompt.strip().encode("utf-8")).hexdigest()[:12],
                })
                print(f"  ledger row → {row['id']} (outcome=flagged, "
                      f"project={args.project})")
            except Exception as e:  # noqa: BLE001 — logging must never block lint
                print(f"  ledger row NOT written: {e}")
        else:
            print("  ledger row NOT written — pass --model <id> to record the "
                  "filter burn in the generation ledger (model ids are never "
                  "fabricated)")

    return 1 if verdict == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
