"""Generation ledger — ratio/budget math against hand-computed numbers.

Every expected value below was computed by hand from db/ledger/_demo.json
(see the arithmetic in comments). If you change the fixture, recompute —
these tests are the contract for the math, not a snapshot.
"""

import json
import math

import pytest

import higgsfield_memory as hm
from conftest import REPO

DEMO = REPO / "db" / "ledger" / "_demo.json"


@pytest.fixture(scope="module")
def demo_rows():
    return json.loads(DEMO.read_text(encoding="utf-8"))["rows"]


@pytest.fixture(scope="module")
def ratio(demo_rows):
    return hm.compute_ratio(demo_rows)


def group(ratio, tag):
    return next(g for g in ratio["groups"] if g["tag"] == tag)


# ── Supersedes resolution + headline ────────────────────────────────────────

def test_effective_rows(demo_rows):
    # 10 rows − 1 masked (_demo-0004, superseded by 0005) = 9 effective
    eff = hm.resolve_effective(demo_rows)
    assert len(eff) == 9
    assert "_demo-0004" not in {r["id"] for r in eff}


def test_headline_n_is_row_count_not_group_sum(ratio):
    # effective 9 − 1 draft (_demo-0007) = 8; group n's sum to 12 (overlap)
    assert ratio["n"] == 8
    assert sum(g["n"] for g in ratio["groups"]) == 12


# ── Per-tag ratio table ──────────────────────────────────────────────────────

def test_dialogue_cu_group(ratio):
    # members 0001,0002,0003,0005,0006: n=5, kept=3 (0001,0005,0006)
    g = group(ratio, "dialogue-cu")
    assert (g["n"], g["kept"]) == (5, 3)
    assert math.isclose(g["takes_per_kept"], 5 / 3)
    assert round(g["takes_per_kept"], 1) == 1.7
    # structural: 0002 extra-cuts → 1/5 = 20%; stochastic: 0003 performance → 20%
    assert round(100 * g["structural_frac"]) == 20
    assert round(100 * g["stochastic_frac"]) == 20
    assert g["low_n"] is False


def test_two_char_group_low_n(ratio):
    # members 0001,0005,0010: n=3, kept=2; structural 0010 identity-drift 1/3
    g = group(ratio, "two-char")
    assert (g["n"], g["kept"]) == (3, 2)
    assert math.isclose(g["takes_per_kept"], 1.5)
    assert round(100 * g["structural_frac"]) == 33
    assert g["stochastic_frac"] == 0
    assert g["low_n"] is True


def test_flagged_counts_as_structural(ratio):
    # vfx-event = only 0009 (flagged): kept=0 → takes None; structural 100%
    g = group(ratio, "vfx-event")
    assert (g["n"], g["kept"]) == (1, 0)
    assert g["takes_per_kept"] is None
    assert round(100 * g["structural_frac"]) == 100
    assert g["low_n"] is True


def test_zero_kept_group(ratio):
    g = group(ratio, "dialogue-multi")  # only 0010, rejected
    assert g["takes_per_kept"] is None
    assert round(100 * g["structural_frac"]) == 100


def test_masked_rejection_does_not_count(ratio):
    # 0004 (camera-wrong, stochastic) is superseded — its rejection must be
    # invisible everywhere: two-char stochastic% is 0, dialogue-cu has only
    # 0003 as its stochastic rejection.
    assert group(ratio, "two-char")["stochastic_frac"] == 0
    assert math.isclose(group(ratio, "dialogue-cu")["stochastic_frac"], 1 / 5)


def test_draft_burn_excluded(ratio):
    # 0007 is the only draft row; appears in no group, kept=0
    assert ratio["draft"] == {"n": 1, "kept": 0, "credits": 20}
    assert "establishing" in {g["tag"] for g in ratio["groups"]}
    assert group(ratio, "establishing")["n"] == 1  # only 0008, not the draft


def test_credits_per_kept_subpopulation(ratio):
    # dialogue-cu credited rows: 0001(160)+0002(160)+0003(160)+0005(120)+0006(40)
    # = 640 (superseded 0004's 120 must NOT appear); kept among credited = 3
    g = group(ratio, "dialogue-cu")
    assert math.isclose(g["credits_per_kept"], 640 / 3)
    assert round(g["credits_per_kept"]) == 213
    assert g["credits_coverage"] == (5, 5)


# ── Schema validation ────────────────────────────────────────────────────────

def model_ids():
    return hm.load_specs_models()


@pytest.mark.parametrize("mutation,fragment", [
    ({"shot_tags": ["CU dialog"]}, "not in vocabulary"),
    ({"shot_tags": ["dialogue-cu"] * 4}, "1..3"),
    ({"outcome": "rejected", "reject_reason": None}, "reject_reason"),
    ({"model": "imaginary_9000"}, "not in specs"),
    ({"outcome": "approved"}, "outcome"),
    ({"draft_tier": "yes"}, "draft_tier"),
])
def test_validate_ledger_row_rejects(mutation, fragment):
    row = {"id": "_demo-0001", "ts": "2026-06-10T09:00:00Z",
           "model": "seedance_2_0", "shot_tags": ["dialogue-cu"],
           "outcome": "kept", "draft_tier": False}
    row.update(mutation)
    problems = hm.validate_ledger_row(row, "_demo", set(), set(), model_ids())
    assert any(fragment in p for p in problems), problems


# ── v3.37.0: model ids from EVERY spec type + retired-id tombstones ──────────

@pytest.mark.parametrize("model", [
    "gpt_image_2",        # image — pre-fix, every image generation was rejected
    "seed_audio",         # audio
    "tripo_3d",           # 3d
    "seedance_2_5",       # video (unchanged)
])
def test_ledger_accepts_every_spec_type(model):
    row = {"id": "_demo-0001", "ts": "2026-09-26T09:00:00Z", "model": model,
           "shot_tags": ["dialogue-cu"], "outcome": "kept", "draft_tier": False}
    assert hm.validate_ledger_row(row, "_demo", set(), set(), model_ids()) == []


def test_retired_id_keeps_history_valid():
    """llm_text left the catalog in the 09-26 snapshot; rows logged while it
    was live must not turn append-only history red after the sync."""
    row = {"id": "_demo-0001", "ts": "2026-08-01T09:00:00Z", "model": "llm_text",
           "shot_tags": ["pov"], "outcome": "kept", "draft_tier": False}
    assert hm.validate_ledger_row(row, "_demo", set(), set(), model_ids()) == []


def test_tombstones_alone_never_fake_a_specs_layer(tmp_path, monkeypatch):
    specs = tmp_path / "specs"
    specs.mkdir()
    (specs / "retired-model-ids.json").write_text(
        json.dumps({"retired": {"llm_text": {}}}), encoding="utf-8")
    monkeypatch.setattr(hm, "SPECS_ROOT", specs)
    assert hm.load_specs_models() == {}     # no spec file → "specs missing", not a tiny map


def test_log_gen_accepts_an_image_model_end_to_end(tmp_path, monkeypatch):
    monkeypatch.setattr(hm, "LEDGER_DIR", tmp_path / "ledger")
    monkeypatch.setattr(hm, "GLOBAL_LEDGER", tmp_path / "ledger" / "_global.json")
    row = hm.log_gen_row("proj", {"model": "gpt_image_2", "shot_tags": ["insert-prop"],
                                  "outcome": "kept"})
    assert row["model"] == "gpt_image_2" and row["id"] == "proj-0001"


def test_supersedes_rules():
    base = {"ts": "t", "model": "seedance_2_0", "shot_tags": ["pov"],
            "outcome": "kept", "draft_tier": False}
    ids = model_ids()
    # forward reference: target not in prior ids
    row = {**base, "id": "_demo-0002", "supersedes": "_demo-0009"}
    assert any("no earlier row" in p for p in
               hm.validate_ledger_row(row, "_demo", {"_demo-0001"}, set(), ids))
    # double-supersede: target already masked
    row = {**base, "id": "_demo-0003", "supersedes": "_demo-0001"}
    assert any("already superseded" in p for p in
               hm.validate_ledger_row(row, "_demo", {"_demo-0001", "_demo-0002"},
                                      {"_demo-0001"}, ids))


def test_demo_fixture_is_schema_valid(demo_rows):
    ids = model_ids()
    prior, superseded, problems = set(), set(), []
    for row in demo_rows:
        problems += hm.validate_ledger_row(row, "_demo", prior, superseded, ids)
        if row.get("supersedes"):
            superseded.add(row["supersedes"])
        prior.add(row["id"])
    assert problems == []


def test_demo_excluded_from_global():
    g = json.loads((REPO / "db" / "ledger" / "_global.json").read_text(encoding="utf-8"))
    assert "_demo.json" not in g["generated_from"]
    assert all(not r["id"].startswith("_demo") for r in g["rows"])


# ── Budget math ──────────────────────────────────────────────────────────────

MANIFEST = [
    {"shot": "A", "shot_tags": ["dialogue-cu"], "model": "seedance_2_0"},
    {"shot": "B", "shot_tags": ["two-char"], "model": "kling3_0"},
    {"shot": "C", "shot_tags": ["action-chase", "creature-occluded"]},
]


@pytest.fixture(scope="module")
def budget(demo_rows):
    return hm.compute_budget(MANIFEST, demo_rows, global_rows=[])


def test_budget_per_shot(budget):
    a, b, c = budget["shots"]
    # A: dialogue-cu n=5>=5, kept=3 → 5/3, project-data
    assert math.isclose(a["expected_takes"], 5 / 3)
    assert a["source"] == "project-data"
    # B: two-char n=3<5 → global empty → DEFAULT two-char = 3.0
    assert (b["expected_takes"], b["source"]) == (3.0, "default")
    # C: action-chase 5.0 vs creature-occluded 5.0 → MAX 5.0, default
    assert (c["expected_takes"], c["source"]) == (5.0, "default")


def test_budget_credit_averages(budget):
    a, b, c = budget["shots"]
    # seedance_2_0 credited non-draft effective rows: 0001,0002,0003,0010
    # (0009 flagged has no credits; 0007 is draft) → 640/4 = 160
    assert math.isclose(a["credit_avg"], 160)
    assert math.isclose(a["expected_credits"], 160 * 5 / 3)  # 800/3
    # kling3_0 credited effective rows: 0005(120), 0008(120) — masked 0004 excluded
    assert math.isclose(b["credit_avg"], 120)
    assert math.isclose(b["expected_credits"], 360)
    assert c["expected_credits"] is None  # no model → excluded from money total


def test_budget_totals(budget):
    # takes 5/3 + 3 + 5 = 29/3 ≈ 9.7; credits 800/3 + 360 = 1880/3 ≈ 627
    assert math.isclose(budget["total_takes"], 29 / 3)
    assert round(budget["total_takes"], 1) == 9.7
    assert math.isclose(budget["total_credits"], 1880 / 3)
    assert round(budget["total_credits"]) == 627
    assert budget["credit_coverage"] == (2, 3)
    assert budget["confidence"] == "default"  # worst per-shot label
    assert budget["defaults_used"] is True


def test_budget_rejects_bad_tag(demo_rows):
    with pytest.raises(hm.LedgerError, match="not in vocabulary"):
        hm.compute_budget([{"shot_tags": ["talking head"]}], demo_rows, [])


def test_ratio_cli_renders(demo_rows):
    text = hm.render_ratio("_demo", hm.compute_ratio(demo_rows), credits_mode=True)
    assert "n=8" in text
    assert "1.7" in text
    assert "low-n" in text
    assert "Draft burn: 1 draft-tier row(s), 0 kept" in text
    assert "213" in text


# ── Item 1: structural/stochastic fork verdict ───────────────────────────────

def _grow(reason_or_kept, n, tag="action-melee"):
    """n rows on one tag: 1 keep + (n-1) rows of the given reason (or all kept)."""
    rows = [{"id": f"p-{i:04d}", "ts": "t", "model": "seedance_2_0",
             "shot_tags": [tag], "draft_tier": False,
             "outcome": "kept"} for i in range(n)]
    if reason_or_kept != "kept":
        for r in rows[1:]:
            r["outcome"], r["reject_reason"] = "rejected", reason_or_kept
    return rows


def test_fork_verdict_low_n_stays_silent():
    g = hm.compute_ratio(_grow("performance", 3))["groups"][0]
    assert g["low_n"] and hm.fork_verdict(g) == "low-n"


def test_fork_verdict_stochastic_dominant_batches():
    # 1 kept + 5 performance (stochastic) → batch+select
    g = hm.compute_ratio(_grow("performance", 6))["groups"][0]
    assert hm.fork_verdict(g) == "batch+sel"


def test_fork_verdict_structural_dominant_iterates():
    # 1 kept + 5 identity-drift (structural) → iterate the prompt
    g = hm.compute_ratio(_grow("identity-drift", 6))["groups"][0]
    assert hm.fork_verdict(g) == "iterate"


# ── Item 4 / Flag A: cause-agnostic ratio plausibility ───────────────────────

def test_flag_a_fires_on_too_good_complex_tag():
    # action-melee default 5.0; 5 straight keeps → 1.0:1, well under 0.5*default
    flags = hm.plausibility_flags(hm.compute_ratio(_grow("kept", 5))["groups"])
    assert len(flags) == 1
    msg = flags[0]
    # cause-agnostic: names BOTH explanations, asserts neither
    assert "re-baseline" in msg and "under-logged" in msg


def test_flag_a_silent_when_ratio_near_default():
    # 1 kept + 5 stochastic on action-melee → 6.0:1, above default 5.0 → no flag
    assert hm.plausibility_flags(hm.compute_ratio(_grow("performance", 6))["groups"]) == []


def test_flag_a_excludes_low_n():
    assert hm.plausibility_flags(hm.compute_ratio(_grow("kept", 3))["groups"]) == []


# ── Item 3: prompt_method control arm ────────────────────────────────────────

def test_prompt_method_validation():
    base = {"id": "_demo-0001", "ts": "t", "model": "seedance_2_0",
            "shot_tags": ["pov"], "outcome": "kept", "draft_tier": False}
    ids = model_ids()
    assert hm.validate_ledger_row(base, "_demo", set(), set(), ids) == []  # absent ok
    assert hm.validate_ledger_row({**base, "prompt_method": "mcsla"},
                                  "_demo", set(), set(), ids) == []
    bad = hm.validate_ledger_row({**base, "prompt_method": "full"},
                                 "_demo", set(), set(), ids)
    assert any("prompt_method must be one of" in p for p in bad)


def test_method_ab_excludes_unlabeled():
    def r(i, outcome, method=None, reason=None):
        row = {"id": f"p-{i:04d}", "ts": "t", "model": "seedance_2_0",
               "shot_tags": ["action-melee"], "outcome": outcome, "draft_tier": False}
        if method:
            row["prompt_method"] = method
        if reason:
            row["reject_reason"] = reason
        return row
    rows = [r(0, "kept", "quick"), r(1, "rejected", "quick", "performance"),
            r(2, "kept", "mcsla"), r(3, "kept", "mcsla"),
            r(4, "kept"), r(5, "kept")]  # last two unlabeled
    ab = hm.compute_method_ab(rows)
    assert ab["n_labeled"] == 4 and ab["excluded_unlabeled"] == 2
    by = {m["method"]: m for m in ab["methods"]}
    assert by["quick"]["n"] == 2 and by["quick"]["kept"] == 1
    assert by["mcsla"]["n"] == 2 and by["mcsla"]["kept"] == 2
    # matched-class filter
    assert hm.compute_method_ab(rows, tag="dialogue-cu")["n_labeled"] == 0


# ── Flag B (PR 2): wasted-re-roll detector ───────────────────────────────────

def _cluster(h, outcomes, tag="action-melee"):
    """Rows sharing one prompt_hash. outcomes: list of 'kept' or reject_reason."""
    rows = []
    for i, o in enumerate(outcomes):
        r = {"id": f"p-{i:04d}", "ts": "t", "model": "seedance_2_0",
             "shot_tags": [tag], "draft_tier": False, "prompt_hash": h}
        if o == "kept":
            r["outcome"] = "kept"
        else:
            r["outcome"], r["reject_reason"] = "rejected", o
        rows.append(r)
    return rows


def test_flag_b_fires_on_all_structural_no_keeper():
    rows = _cluster("deadbeef0001", ["identity-drift"] * 6)
    flags = hm.wasted_reroll_flags(rows)
    assert len(flags) == 1 and "wasted re-roll" in flags[0]
    assert "deadbeef0001" in flags[0]


def test_flag_b_silent_when_cluster_has_a_keeper():
    # variance-harvest: same locked prompt, a structural one-off, but a KEEPER
    # proves the prompt works → must NOT fire (keeper-presence discriminator)
    rows = _cluster("cafe00002222", ["kept"] + ["identity-drift"] * 6)
    assert hm.wasted_reroll_flags(rows) == []


def test_flag_b_silent_below_min_cluster():
    rows = _cluster("aaaa11112222", ["identity-drift"] * 3)
    assert hm.wasted_reroll_flags(rows) == []


def test_flag_b_ignores_stochastic_pile():
    # no keeper, but all stochastic (re-roll territory) → not a wasted re-roll
    rows = _cluster("bbbb33334444", ["performance"] * 6)
    assert hm.wasted_reroll_flags(rows) == []


def test_flag_b_skips_rows_without_prompt_hash():
    rows = [{"id": f"p-{i:04d}", "ts": "t", "model": "seedance_2_0",
             "shot_tags": ["action-melee"], "draft_tier": False,
             "outcome": "rejected", "reject_reason": "identity-drift"}
            for i in range(6)]
    assert hm.wasted_reroll_flags(rows) == []


def test_flag_b_respects_supersedes():
    # a superseding keeper masks the original structural reject → keeper present
    rows = _cluster("dddd55556666", ["identity-drift"] * 6)
    rows.append({"id": "p-0099", "ts": "t", "model": "seedance_2_0",
                 "shot_tags": ["action-melee"], "draft_tier": False,
                 "prompt_hash": "dddd55556666", "outcome": "kept",
                 "supersedes": "p-0000"})
    # cluster now has a keeper among effective rows → silent
    assert hm.wasted_reroll_flags(rows) == []


# ── Wave B: vision_reason + vision/human agreement ───────────────────────────

def _diag(i, reason, vision, outcome="rejected"):
    """A row carrying a human reject_reason and/or a proposed vision_reason."""
    r = {"id": f"p-{i:04d}", "ts": "t", "model": "seedance_2_0",
         "shot_tags": ["action-melee"], "draft_tier": False, "outcome": outcome}
    if reason:
        r["reject_reason"] = reason
    if vision:
        r["vision_reason"] = vision
    return r


def test_vision_reason_validation():
    base = {"id": "_demo-0001", "ts": "t", "model": "seedance_2_0",
            "shot_tags": ["pov"], "outcome": "kept", "draft_tier": False}
    ids = model_ids()
    assert hm.validate_ledger_row(base, "_demo", set(), set(), ids) == []  # absent ok
    assert hm.validate_ledger_row({**base, "vision_reason": "physics"},
                                  "_demo", set(), set(), ids) == []
    bad = hm.validate_ledger_row({**base, "vision_reason": "warped-hand"},
                                 "_demo", set(), set(), ids)
    assert any("vision_reason must be a reject_reason" in p for p in bad)


def test_agreement_trusts_a_high_agreement_class_above_min_n():
    # 8 paired physics rows, 7 match → 87.5% ≥ 80% over ≥ 8 → trusted
    rows = [_diag(i, "physics", "physics") for i in range(7)]
    rows.append(_diag(7, "physics", "composition"))  # one miss
    c = hm.compute_vision_agreement(rows)["classes"][0]
    assert c["n"] == 8 and c["matches"] == 7
    assert math.isclose(c["agreement"], 7 / 8)
    assert c["trusted"] is True and c["low_n"] is False


def test_agreement_low_n_is_not_trusted():
    rows = [_diag(i, "composition", "composition") for i in range(3)]
    c = hm.compute_vision_agreement(rows)["classes"][0]
    assert c["low_n"] is True and c["trusted"] is False


def test_agreement_high_rate_but_below_min_n_not_trusted():
    # perfect agreement but only 4 rows → below VISION_AGREEMENT_MIN_N → not trusted
    rows = [_diag(i, "physics", "physics") for i in range(4)]
    c = hm.compute_vision_agreement(rows)["classes"][0]
    assert math.isclose(c["agreement"], 1.0) and c["trusted"] is False


def test_agreement_excludes_unpaired_rows():
    # vision proposed but no human reject_reason (kept row) → diagnosed, not paired
    rows = [_diag(0, None, "physics", outcome="kept")]
    ag = hm.compute_vision_agreement(rows)
    assert ag["n_paired"] == 0 and ag["n_diagnosed"] == 1 and ag["classes"] == []


def test_agreement_respects_supersedes():
    # original physics/physics match superseded by a corrected physics/composition miss
    rows = [_diag(i, "physics", "physics") for i in range(8)]
    rows.append({**_diag(99, "physics", "composition"), "supersedes": "p-0000"})
    c = hm.compute_vision_agreement(rows)["classes"][0]
    # 8 effective rows (0000 masked, 0099 added): 7 match → still trusted, miss counted
    assert c["n"] == 8 and c["matches"] == 7


def test_agreement_cli_renders():
    rows = [_diag(i, "physics", "physics") for i in range(8)]
    text = hm.render_agreement("_demo", hm.compute_vision_agreement(rows))
    assert "physics" in text and "100%" in text and "yes" in text
