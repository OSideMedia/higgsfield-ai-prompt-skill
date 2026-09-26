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
