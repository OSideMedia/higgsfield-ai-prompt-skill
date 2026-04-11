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

Usage:
  python3 seedance_lint.py "<prompt text>"
  echo "<prompt text>" | python3 seedance_lint.py
  python3 seedance_lint.py --file prompt.txt
  python3 seedance_lint.py --log "<prompt text>"      # log FAIL to filter-memory
  python3 seedance_lint.py --confirmed "<prompt>"     # log as confirmed workaround

Exit codes: 0 = PASS or WARN only, 1 = any FAIL.

Filter-memory loopback:
  --log         → on FAIL, append an entry to db/filter-memory.json with
                  outcome=unknown. Rule hits become blocked_terms + tags.
  --confirmed   → append the prompt as a confirmed workaround (outcome=
                  workaround, substitution_worked=True). Use after a rewrite
                  passes Seedance's filter in a real generation.

  To update an existing entry's outcome later:
    python3 higgsfield_memory.py update-filter <id> <outcome>
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


# ── Rule data ───────────────────────────────────────────────────────────────

# Real person / public figure name patterns. Not exhaustive — Seedance's filter
# has a much larger list internally — but these are the ones users repeatedly
# hit in our filter-memory database.
REAL_NAMES = [
    r"\belon musk\b", r"\bdonald trump\b", r"\bjoe biden\b", r"\bkamala harris\b",
    r"\bvladimir putin\b", r"\bxi jinping\b", r"\bbarack obama\b",
    r"\bkeanu reeves\b", r"\btom cruise\b", r"\bbrad pitt\b", r"\bleonardo dicaprio\b",
    r"\btaylor swift\b", r"\bbeyonc[eé]\b", r"\brihanna\b", r"\bkanye\b", r"\bye\b(?! olde)",
    r"\bkim kardashian\b", r"\bdrake\b(?!'s equation)", r"\btravis scott\b",
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
    r"\bstab(s|bed|bing)?\b", r"\bshoot(s|ing)?\b", r"\bshot\b",
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


def _matches(patterns: list[str], text: str) -> list[str]:
    hits: list[str] = []
    for pat in patterns:
        for m in re.finditer(pat, text, flags=re.IGNORECASE):
            hits.append(m.group(0))
    return hits


def _has_cue(cues: list[str], text: str) -> bool:
    lowered = text.lower()
    return any(re.search(c, lowered) for c in cues)


def lint(prompt: str) -> list[Finding]:
    findings: list[Finding] = []
    text = prompt.strip()
    word_count = len(re.findall(r"\b\w+\b", text))

    if not text:
        findings.append(Finding("FAIL", "empty", "", "Prompt is empty."))
        return findings

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

    if word_count > 220:
        findings.append(Finding(
            "FAIL", "overlength", f"{word_count} words",
            "Over 220 words often hard-fails the text encoder. Cut to "
            "30–180 words. Keep Style & Mood + camera + action; trim the rest."
        ))

    # ── WARN rules ──────────────────────────────────────────────────────────

    hits = _matches(ANTISLOP, text)
    if hits:
        findings.append(Finding(
            "WARN", "antislop", ", ".join(sorted(set(hits))),
            "Marketing-copy adjectives correlate with flags — they signal "
            "vague intent. Replace with observable, measurable details."
        ))

    if word_count > 180:
        findings.append(Finding(
            "WARN", "long", f"{word_count} words",
            "Over 180 words is risk territory. Trim the least essential "
            "details before generating."
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
        description="Preflight linter for Seedance 2.0 prompts."
    )
    parser.add_argument("prompt", nargs="?", help="Prompt text (or use --file / stdin)")
    parser.add_argument("--file", "-f", help="Read prompt from file")
    parser.add_argument("--log", action="store_true",
                        help="On FAIL, append an entry to db/filter-memory.json")
    parser.add_argument("--confirmed", action="store_true",
                        help="Log prompt as a confirmed filter workaround "
                             "(outcome=workaround, substitution_worked=True)")
    args = parser.parse_args()

    if args.file:
        prompt = open(args.file, encoding="utf-8").read()
    elif args.prompt:
        prompt = args.prompt
    elif not sys.stdin.isatty():
        prompt = sys.stdin.read()
    else:
        parser.print_help()
        return 2

    findings = lint(prompt)
    verdict, report = render(prompt, findings)
    print(report)

    if args.confirmed:
        entry_id = log_to_filter_memory(prompt, findings, confirmed=True)
        print(f"\n  logged as confirmed workaround → {entry_id}")
    elif args.log and verdict == "FAIL":
        entry_id = log_to_filter_memory(prompt, findings, confirmed=False)
        print(f"\n  logged to filter-memory → {entry_id}")

    return 1 if verdict == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
