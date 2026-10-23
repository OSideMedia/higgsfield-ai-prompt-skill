"""build_index.py — anchors must be GitHub's, not merely self-consistent.

The pre-v3.37 slugger collapsed `\\s+`, so "A — B" became `a-b` while GitHub
renders `a--b`. Generation and verification shared the bug, so validate
certified ~303/932 INDEX anchors and 103/234 QUICK FACTS links that 404 on
GitHub. The vectors below follow github-slugger (the library GitHub-flavoured
anchors are emulated from): lowercase → strip the removed Unicode categories →
each space becomes `-`; repeats get `-1`, `-2`, … with emitted slugs reserved.
"""
import re

import pytest

import build_index as b


@pytest.mark.parametrize("heading,slug", [
    ("A — B", "a--b"),                                             # em dash between spaces
    ("Audio as a Conditioning Input — Seedance 2.0 (`@Audio1`)",
     "audio-as-a-conditioning-input--seedance-20-audio1"),
    ("Reference Roles — Say What to Use *and* What Not to Use",
     "reference-roles--say-what-to-use-and-what-not-to-use"),
    ("Naming collision — `higgsfield-soul` (theirs) vs `higgsfield-soul` (ours)",
     "naming-collision--higgsfield-soul-theirs-vs-higgsfield-soul-ours"),
    ("two  spaces", "two--spaces"),                                # no collapsing
    ("snake_case stays", "snake_case-stays"),                      # connector punct kept
    ("1. The `@source` declaration", "1-the-source-declaration"),
    ("Café Ñandú", "café-ñandú"),                                  # letters kept, not ASCII-folded
    ("Area m² ½", "area-m-"),                                      # Other_Number removed
    ("Emoji 🎬 Scene", "emoji--scene"),                            # symbols removed
])
def test_anchor_matches_github(heading, slug):
    assert b.anchor(heading) == slug


@pytest.mark.parametrize("heads,slugs", [
    (["Foo", "Foo", "Foo"], ["foo", "foo-1", "foo-2"]),
    (["Foo", "Foo", "Foo-1"], ["foo", "foo-1", "foo-1-1"]),        # emitted slugs are reserved
    (["Foo-1", "Foo", "Foo"], ["foo-1", "foo", "foo-2"]),
])
def test_duplicate_suffixes_follow_github_slugger(heads, slugs):
    assert b.anchors_for([(2, h) for h in heads]) == slugs


def test_every_quick_facts_link_resolves_on_github():
    assert b.run_checks() == []


def test_every_in_file_anchor_link_resolves():
    bad = []
    for p in b.skill_files():
        text = p.read_text(encoding="utf-8")
        valid = set(b.anchors_for(b.headings(text)))
        bad += [(p.name, a) for a in re.findall(r"\]\(#([^)]+)\)", text) if a not in valid]
    assert bad == []


def test_index_in_sync():
    assert b.INDEX.read_text(encoding="utf-8") == b.build_index_text()


# ── v3.41.0: CONTENTS blocks (#110 item 3) ──────────────────────────────────

def _doc(sections, filler=30, frontmatter=False):
    """A markdown file with a title, the given (level, text) headings and
    `filler` body lines under each — long enough to owe a CONTENTS block."""
    out = ["---", "name: x", "---", ""] if frontmatter else []
    out += ["# Title", "", "Intro line.", ""]
    for level, text in sections:
        out += [f"{'#' * level} {text}", ""] + ["body"] * filler + [""]
    return "\n".join(out) + "\n"


SECTIONS = [(2, "Alpha — one"), (3, "Alpha detail"), (2, "Beta"), (4, "Too deep"), (2, "Beta")]


def test_contents_lands_under_the_title_and_is_idempotent():
    text = _doc(SECTIONS, frontmatter=True)
    fixed = b.with_contents(text)
    lines = fixed.split("\n")
    assert lines[:5] == ["---", "name: x", "---", "", "# Title"]
    assert lines[5:8] == ["", b.CONTENTS_BEGIN, "**Contents**"]
    assert "- [Alpha — one](#alpha--one)" in lines
    assert "  - [Alpha detail](#alpha-detail)" in lines
    assert "- [Beta](#beta-1)" in lines                 # duplicate heading keeps GitHub's suffix
    assert not any("Too deep" in l for l in lines[:20])  # two levels only
    assert b.with_contents(fixed) == fixed               # the writer's no-op IS the check
    assert b.without_contents(fixed) == text


def test_contents_links_resolve_and_ignore_fenced_headings():
    text = _doc([(2, "Real")] + [(2, "Also real")], filler=60).replace(
        "Intro line.", "```\n## not a heading\n```")
    fixed = b.with_contents(text)
    valid = set(b.anchors_for(b.headings(fixed)))
    links = re.findall(r"\]\(#([^)]+)\)", fixed)
    assert links == ["real", "also-real"] and set(links) <= valid


def test_contents_refreshes_a_stale_block():
    fixed = b.with_contents(_doc(SECTIONS))
    renamed = fixed.replace("## Beta\n", "## Gamma\n", 1)
    assert renamed != fixed and b.with_contents(renamed) != renamed
    assert "- [Gamma](#gamma)" in b.with_contents(renamed)


@pytest.mark.parametrize("text", [
    _doc([(2, "A"), (2, "B")], filler=5),                          # 100 lines or fewer
    _doc([(2, "QUICK FACTS"), (2, "B")], filler=60),               # QUICK FACTS already opens it
    _doc([(2, "Only one section")], filler=120),                   # nothing to choose between
])
def test_contents_not_owed(text):
    assert b.with_contents(text) == text


def test_contents_not_owed_cases_are_long_enough_to_owe_one_otherwise():
    # each not-owed case above must fail on its own rule, not on length
    assert len(_doc([(2, "QUICK FACTS"), (2, "B")], filler=60).splitlines()) > b.CONTENTS_THRESHOLD
    assert b.with_contents(_doc([(2, "Quick look"), (2, "B")], filler=60)) != \
        _doc([(2, "Quick look"), (2, "B")], filler=60)


@pytest.mark.parametrize("text", [
    b.CONTENTS_BEGIN + "\n# Title\n",                                   # begin, no end
    "# Title\n" + b.CONTENTS_END + "\n",                                # end, no begin
    _doc(SECTIONS).replace("Intro line.", "\n".join(                    # two blocks
        [b.CONTENTS_BEGIN, b.CONTENTS_END, b.CONTENTS_BEGIN, b.CONTENTS_END])),
])
def test_contents_marker_damage_is_an_error(text):
    with pytest.raises(ValueError):
        b.with_contents(text)


def test_contents_markers_inside_a_code_fence_are_not_a_block():
    example = ["```markdown", b.CONTENTS_BEGIN, "- [kept](#kept)", b.CONTENTS_END, "```"]
    text = _doc(SECTIONS).replace("Intro line.", "\n".join(example))
    fixed = b.with_contents(text)
    assert "\n".join(example) in fixed                  # the example survives verbatim
    assert fixed.count(b.CONTENTS_BEGIN) == 2            # plus one real block
    assert b.with_contents(fixed) == fixed


@pytest.mark.parametrize("fence", [
    ["````", "```"],              # a shorter fence cannot close a longer one
    ["```", "~~~"],               # nor a tilde fence a backtick one
])
def test_contents_markers_inside_an_unclosed_inner_fence_are_not_a_block(fence):
    opener, inner = fence
    example = [opener, inner, b.CONTENTS_BEGIN, "EXAMPLE", b.CONTENTS_END, inner, opener]
    text = _doc(SECTIONS) + "\n".join(example) + "\n"
    fixed = b.with_contents(text)
    assert "\n".join(example) in fixed
    assert fixed.count(b.CONTENTS_BEGIN) == 2 and b.with_contents(fixed) == fixed


def test_contents_indented_backticks_are_not_a_fence():
    fixed = b.with_contents(_doc(SECTIONS))
    text = fixed.replace("## Beta\n", "    ```\n\n## Beta\n", 1)   # indented code, not a fence
    assert b.with_contents(text) == text                         # the real block still counts


def test_fence_mask_follows_commonmark_closers():
    lines = ["````md", "```", "# inside", "````", "# outside", "``` a`b", "# not fenced"]
    assert b.fence_mask(lines) == [True, True, True, True, False, False, False]


def test_contents_ignores_a_comment_line_in_frontmatter():
    text = _doc(SECTIONS, frontmatter=True).replace("name: x", "name: x\n# a yaml comment")
    lines = b.with_contents(text).split("\n")
    assert lines[:6] == ["---", "name: x", "# a yaml comment", "---", "", "# Title"]
    assert lines[7] == b.CONTENTS_BEGIN


def test_contents_moves_a_misplaced_block_back_under_the_title():
    fixed = b.with_contents(_doc(SECTIONS))
    body = b.without_contents(fixed)
    block = fixed[fixed.index(b.CONTENTS_BEGIN):fixed.index(b.CONTENTS_END) + len(b.CONTENTS_END)]
    moved = body + "\n" + block + "\n"
    assert b.with_contents(moved) == fixed


def test_contents_keeps_crlf_line_endings():
    text = _doc(SECTIONS).replace("\n", "\r\n")
    fixed = b.with_contents(text)
    assert fixed.count(b.CONTENTS_BEGIN) == 1 and "\n" not in fixed.replace("\r\n", "")
    assert b.with_contents(fixed) == fixed


@pytest.mark.parametrize("heading", [
    "See [the guide](guide.md)", "<b>Bold</b> setup", "The _real_ rule", r"Escaped \* star",
    "__Bold__ setup", "[Guide][ref] notes", "R&amp;D",
])
def test_contents_refuses_a_heading_the_slugger_cannot_read(heading):
    with pytest.raises(ValueError, match="slugs differently"):
        b.with_contents(_doc([(2, "Fine"), (2, heading)], filler=60))


@pytest.mark.parametrize("heading", ["`snake_case_name` flag", "Duration < 5 s", "a_b_c",
                                     "Verified surface [OFFICIAL — model spec 2026-08-01]"])
def test_contents_accepts_plain_heading_punctuation(heading):
    fixed = b.with_contents(_doc([(2, "Fine"), (2, heading)], filler=60))
    assert b.CONTENTS_BEGIN in fixed and b.with_contents(fixed) == fixed


def test_quick_facts_rule_survives_marker_damage(tmp_path, monkeypatch):
    monkeypatch.setattr(b, "ROOT", tmp_path)
    sub = tmp_path / "skills" / "x" / "SKILL.md"
    sub.parent.mkdir(parents=True)
    sub.write_text("# Sub\n" + b.CONTENTS_BEGIN + "\n", encoding="utf-8")
    assert b.quick_facts_problems(sub) == []             # contents_problems() reports it
    long_body = "\n".join(["line"] * (b.QUICK_FACTS_THRESHOLD + 50))
    sub.write_text("# Sub\n" + b.CONTENTS_BEGIN + "\n" + long_body, encoding="utf-8")
    assert "no '## QUICK FACTS' block" in b.quick_facts_problems(sub)[0]   # still enforced


def test_contents_gate_flags_a_missing_block(tmp_path, monkeypatch):
    monkeypatch.setattr(b, "ROOT", tmp_path)
    monkeypatch.setattr(b, "INDEX", tmp_path / "INDEX.md")
    (tmp_path / "skills" / "x").mkdir(parents=True)
    owed = tmp_path / "skills" / "x" / "REF.md"
    owed.write_text(_doc(SECTIONS), encoding="utf-8")
    (tmp_path / "README.md").write_text(_doc(SECTIONS), encoding="utf-8")   # repo doc: exempt
    (tmp_path / "docs" / "archive").mkdir(parents=True)
    (tmp_path / "docs" / "archive" / "OLD.md").write_text(_doc(SECTIONS), encoding="utf-8")
    assert [p.split(":")[0] for p in b.contents_problems()] == ["skills/x/REF.md"]
    assert b.write_contents() == [owed]
    assert b.contents_problems() == []


def test_quick_facts_rule_skips_the_root_and_the_contents_block(tmp_path, monkeypatch):
    monkeypatch.setattr(b, "ROOT", tmp_path)
    long_body = "\n".join(["line"] * (b.QUICK_FACTS_THRESHOLD + 50))
    root = tmp_path / "SKILL.md"
    root.write_text("# Root\n" + long_body, encoding="utf-8")
    sub = tmp_path / "skills" / "x" / "SKILL.md"
    sub.parent.mkdir(parents=True)
    sub.write_text("# Sub\n" + long_body, encoding="utf-8")
    assert b.quick_facts_problems(root) == []
    assert b.quick_facts_problems(sub)                   # a long sub-skill still owes one
    short = "\n".join(["line"] * (b.QUICK_FACTS_THRESHOLD - 20))
    block = "\n".join([b.CONTENTS_BEGIN] + ["- [x](#x)"] * 40 + [b.CONTENTS_END])
    sub.write_text(f"# Sub\n{block}\n{short}", encoding="utf-8")
    assert b.quick_facts_problems(sub) == []


def test_every_contents_block_is_current():
    assert b.contents_problems() == []


def test_every_anchor_link_in_a_contents_file_resolves():
    bad = []
    for p in b.contents_files():
        text = p.read_text(encoding="utf-8")
        valid = set(b.anchors_for(b.headings(text)))
        bad += [(p.name, a) for a in re.findall(r"\]\(#([^)]+)\)", text) if a not in valid]
    assert bad == []
