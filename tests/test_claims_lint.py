"""scripts/claims_lint.py + evals/spec-claims.json — doctrine claims vs specs.

The plant (same commit as the gate): the v3.35.0 doctrine (git c0b73ab —
the release that shipped the "Seedance 2.5 caps at 720p / has no
start_image role" lines) must FAIL against today's specs with >= 5 distinct
file:line hits on the Seedance 2.5 claims, and the SAME doctrine must PASS
those claims against the 2026-08-07 specs, when they were true. One tree,
two truths: the linter discriminates on the specs, not on the text.
"""

import io
import json
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

import pytest

import claims_lint as cl

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "claims_lint.py"
REGISTRY = REPO / "evals" / "spec-claims.json"
EXCERPT = Path(__file__).parent / "fixtures" / "claims_doctrine_v3_35_0_excerpt.json"
V335 = "c0b73ab"
S25_IDS = ("s25-", "platform-start-end-frame-is-2-0-only")


def _git_has(rev: str) -> bool:
    r = subprocess.run(["git", "-C", str(REPO), "cat-file", "-e", f"{rev}^{{commit}}"],
                       capture_output=True)
    return r.returncode == 0


def _tree_from_git(dest: Path) -> None:
    raw = subprocess.run(["git", "-C", str(REPO), "archive", "--format=tar", V335],
                         capture_output=True, check=True).stdout
    with tarfile.open(fileobj=io.BytesIO(raw)) as tar:
        tar.extractall(dest, members=[
            m for m in tar.getmembers() if m.isfile() and
            (m.name.endswith(".md") or
             (m.name.startswith("evals/cases/") and m.name.endswith(".json")))])


def _tree_from_excerpt(dest: Path) -> None:
    doc = json.loads(EXCERPT.read_text(encoding="utf-8"))
    for path, lines in doc["files"].items():
        nums = {int(k): v for k, v in lines.items()}
        body = [nums.get(n, "") for n in range(1, max(nums) + 1)]
        (dest / path).parent.mkdir(parents=True, exist_ok=True)
        (dest / path).write_text("\n".join(body) + "\n", encoding="utf-8")


@pytest.fixture(scope="module")
def v335_tree(tmp_path_factory):
    """The v3.35.0 doctrine: exact files via `git archive c0b73ab` when the
    commit is reachable, else the committed excerpt (shallow CI checkout)."""
    dest = tmp_path_factory.mktemp("v3_35_0")
    (_tree_from_git if _git_has(V335) else _tree_from_excerpt)(dest)
    return dest


@pytest.fixture(scope="module")
def specs_2026_08_07(tmp_path_factory):
    """A specs dir as it stood at the 2026-08-07 snapshot (video regenerated
    from the committed snapshot; image/audio copied — no s25 claim reads them)."""
    import sync_specs
    snap = REPO / "specs" / "models_explore_snapshot_2026-08-07.json"
    if not snap.exists():
        pytest.fail("fixture premise gone: the committed 2026-08-07 snapshot is missing")
    d = tmp_path_factory.mktemp("specs_0807")
    (d / "model-specs.json").write_text(sync_specs.emit_json(sync_specs.build_spec(snap)),
                                        encoding="utf-8")
    for name in ("image-model-specs.json", "audio-model-specs.json"):
        shutil.copy(REPO / "specs" / name, d / name)
    return d


@pytest.fixture(scope="module")
def claims():
    return cl.load_registry(REGISTRY)


def s25_false(hits):
    return sorted({(h.path, h.line) for h in hits
                   if not h.ok and h.claim.id.startswith(S25_IDS)})


# ── The plant ───────────────────────────────────────────────────────────────

def test_v3_35_0_doctrine_fails_against_todays_specs(v335_tree, claims):
    today = cl.load_specs(REPO / "specs")
    s25 = today["by_id"].get("seedance_2_5")
    if not s25 or "1080p" not in s25["resolutions"]:
        pytest.fail("fixture premise gone: today's specs no longer give seedance_2_5 "
                    "1080p — re-point the plant at the next stale claim")
    bad = s25_false(cl.lint(v335_tree, today, claims))
    assert len(bad) >= 5, bad
    files = {p for p, _ in bad}
    assert {"SKILL.md", "skills/higgsfield-seedance-2-5/SKILL.md",
            "evals/cases/seedance-2-5.json"} <= files


def test_same_doctrine_passes_when_the_claim_was_true(v335_tree, specs_2026_08_07, claims):
    then = cl.load_specs(specs_2026_08_07)
    hits = [h for h in cl.lint(v335_tree, then, claims) if h.claim.id.startswith(S25_IDS)]
    assert len({(h.path, h.line) for h in hits}) >= 5, "claims no longer matched at all"
    assert s25_false(hits) == []


def test_cli_exit_codes_on_the_plant(v335_tree, specs_2026_08_07):
    now = subprocess.run([sys.executable, str(SCRIPT), "--root", str(v335_tree)],
                         capture_output=True, text=True)
    assert now.returncode == 1 and "s25-caps-at-720p" in now.stdout


def test_excerpt_fixture_matches_git(tmp_path):
    """Provenance of the shallow-checkout fallback: every excerpted line is
    byte-identical to `git show c0b73ab:<file>` at that line number."""
    if not _git_has(V335):
        pytest.skip(f"{V335} unreachable (shallow checkout) — provenance is "
                    "checked wherever the commit exists")
    doc = json.loads(EXCERPT.read_text(encoding="utf-8"))
    for path, lines in doc["files"].items():
        real = subprocess.run(["git", "-C", str(REPO), "show", f"{V335}:{path}"],
                              capture_output=True, text=True, check=True).stdout.split("\n")
        for n, text in lines.items():
            assert real[int(n) - 1] == text, f"{path}:{n}"


def test_excerpt_tree_is_enough_for_the_plant(tmp_path, claims):
    _tree_from_excerpt(tmp_path)
    assert len(s25_false(cl.lint(tmp_path, cl.load_specs(REPO / "specs"), claims))) >= 5


# ── Unit behaviour on synthetic trees ───────────────────────────────────────

def _specs(tmp_path, s25_res=("480p", "720p"), roles=("image_references",),
           image_models=(), video_extra=()):
    d = tmp_path / "specs"
    d.mkdir()
    video = [{"id": "seedance_2_5", "name": "Seedance 2.5", "resolutions": list(s25_res),
              "aspect_ratios": [], "modes": [], "duration": {"min": 4, "max": 30},
              "media_roles": {"medias": list(roles)}, "params": []},
             {"id": "kling3_0", "name": "Kling v3.0", "resolutions": [], "aspect_ratios": [],
              "modes": [], "duration": {"min": 3, "max": 15}, "media_roles": {}, "params": []},
             *video_extra]
    (d / "model-specs.json").write_text(json.dumps({"models": video}), encoding="utf-8")
    (d / "image-model-specs.json").write_text(json.dumps({"models": [
        {"id": i, "name": i, "aspect_ratios": ["1:1", "16:9"], "media_roles": {}, "params": []}
        for i in image_models]}), encoding="utf-8")
    (d / "audio-model-specs.json").write_text(json.dumps({"models": []}), encoding="utf-8")
    return cl.load_specs(d)


def _doc(tmp_path, rel, text):
    p = tmp_path / "tree" / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return tmp_path / "tree"


def test_true_claim_passes_false_claim_fails(tmp_path, claims):
    tree = _doc(tmp_path, "guide.md", "Intro.\n\nSeedance 2.5 caps at 720p for now.\n")
    ok = cl.lint(tree, _specs(tmp_path), claims)
    assert [h.ok for h in ok if h.claim.id == "s25-caps-at-720p"] == [True]
    shutil.rmtree(tmp_path / "specs")
    bad = cl.lint(tree, _specs(tmp_path, s25_res=("480p", "720p", "1080p")), claims)
    [h] = [h for h in bad if h.claim.id == "s25-caps-at-720p"]
    assert (h.ok, h.path, h.line) == (False, "guide.md", 3)


def test_cinema_studio_2_5_is_not_seedance(tmp_path, claims):
    tree = _doc(tmp_path, "cinema.md",
                "Video capped at 720p (vs 2.5's 1080p).\nCinema Studio 2.5 caps at 720p video.\n")
    hits = cl.lint(tree, _specs(tmp_path, s25_res=("1080p",)), claims)
    assert [h for h in hits if h.claim.id == "s25-caps-at-720p"] == []


def test_denies_polarity(tmp_path, claims):
    tree = _doc(tmp_path, "evals/cases/x.json", '{"r": "2.5 has no start_image role"}\n')
    assert all(h.ok for h in cl.lint(tree, _specs(tmp_path), claims))
    shutil.rmtree(tmp_path / "specs")
    hits = cl.lint(tree, _specs(tmp_path, roles=("start_image", "image_references")), claims)
    assert [h.ok for h in hits if h.claim.id == "s25-has-no-start-image-role"] == [False]


def test_heading_binds_an_unnamed_claim(tmp_path, claims):
    text = ("### Kling 3.0\n**Strengths:** Longest clip duration on the platform (up to 15s)\n"
            "### Veo 3\n**Strengths:** Longest clip duration on the platform (up to 15s)\n")
    tree = _doc(tmp_path, "ref.md", text)
    longer = [{"id": "seedance_2_5_x", "name": "x", "duration": {"min": 4, "max": 30},
               "media_roles": {}, "params": []}]
    hits = [h for h in cl.lint(tree, _specs(tmp_path, video_extra=longer), claims)
            if h.claim.id == "kling3-longest-duration-15s"]
    assert [(h.line, h.ok) for h in hits] == [(2, False)]      # Veo's line is not bound


def test_listed_set_claim(tmp_path, claims):
    specs = _specs(tmp_path, image_models=("gpt_image_2",))
    good = _doc(tmp_path, "a.md", "GPT Image 2 aspect ratios: 16:9, 1:1\n")
    assert [h.ok for h in cl.lint(good, specs, claims)
            if h.claim.id == "gpt-image-2-aspect-ratios"] == [True]
    (good / "a.md").write_text("GPT Image 2 aspect ratios: 16:9, 1:1, 21:9\n", encoding="utf-8")
    assert [h.ok for h in cl.lint(good, specs, claims)
            if h.claim.id == "gpt-image-2-aspect-ratios"] == [False]


def test_model_presence_claims(tmp_path, claims):
    tree = _doc(tmp_path, "m.md",
                "Grok Imagine Image (`grok-imagine-image`) — NOT available on Higgsfield\n")
    assert all(h.ok for h in cl.lint(tree, _specs(tmp_path), claims))
    shutil.rmtree(tmp_path / "specs")
    hits = cl.lint(tree, _specs(tmp_path, image_models=("grok_image",)), claims)
    assert [h.ok for h in hits if h.claim.id == "grok-image-not-on-higgsfield"] == [False]


def test_model_gone_fails_closed(tmp_path):
    reg = tmp_path / "reg.json"
    reg.write_text(json.dumps({"claims": [{
        "id": "x", "finding": "f", "pattern": "Foo 9 has 4k",
        "assert": {"kind": "has", "model": "foo_9", "field": "resolutions", "value": "4k"}}]}),
        encoding="utf-8")
    tree = _doc(tmp_path, "a.md", "Foo 9 has 4k.\n")
    [h] = cl.lint(tree, _specs(tmp_path), cl.load_registry(reg))
    assert not h.ok and "no longer in specs" in h.why


@pytest.mark.parametrize("rel", ["CHANGELOG.md", "INDEX.md", "docs/archive/HISTORY.md",
                                 "specs/MODEL-SPECS.md", "workspace/notes.md",
                                 "evals/other/x.json"])
def test_historical_and_generated_files_are_not_scanned(tmp_path, claims, rel):
    tree = _doc(tmp_path, rel, "Seedance 2.5 caps at 720p.\n")
    assert cl.lint(tree, _specs(tmp_path, s25_res=("1080p",)), claims) == []


# ── Registry integrity (fail closed) ────────────────────────────────────────

def test_committed_registry_loads_and_every_entry_names_its_finding(claims):
    assert len(claims) >= 10
    for c in claims:
        assert c.finding.strip() and "audit" in c.finding.lower(), c.id


@pytest.mark.parametrize("entry,msg", [
    ({"id": "a", "pattern": "x", "assert": {"kind": "has", "model": "m",
      "field": "resolutions", "value": "4k"}}, "finding"),
    ({"id": "a", "finding": "f", "pattern": "x", "assert": {"kind": "nope", "model": "m"}},
     "kind"),
    ({"id": "a", "finding": "f", "pattern": "(", "assert": {"kind": "model_present",
      "model": "m"}}, "regex"),
    ({"id": "a", "finding": "f", "pattern": "x", "assert": {"kind": "listed_set_equals",
      "model": "m", "field": "resolutions"}}, "list"),
])
def test_malformed_registry_is_an_error(tmp_path, entry, msg):
    reg = tmp_path / "reg.json"
    reg.write_text(json.dumps({"claims": [entry]}), encoding="utf-8")
    with pytest.raises(cl.RegistryError, match=msg):
        cl.load_registry(reg)
    r = subprocess.run([sys.executable, str(SCRIPT), "--registry", str(reg)],
                       capture_output=True, text=True)
    assert r.returncode == 2


def test_empty_registry_is_an_error(tmp_path):
    reg = tmp_path / "reg.json"
    reg.write_text(json.dumps({"claims": []}), encoding="utf-8")
    with pytest.raises(cl.RegistryError):
        cl.load_registry(reg)


def test_v3_36_0_true_phrasings_do_not_fire_but_the_old_ones_still_do(tmp_path, claims):
    # v3.36.0 wrote these TRUE sentences; the first registry patterns flagged them (false
    # positives found at integration). The old v3.35.0 phrasing must keep failing.
    true_text = (
        "Both do 1080p and platform start/end frames (2.5 only in `omni_reference`); 2.5 caps at 1080p\n"
        "> up to 1080p, up to 30 s, many references, platform start/end frames in `omni_reference` —\n"
        "> utility/system entries — AutoSprite, upscalers. (**LLM text left the video catalog in the 2026-09-26 snapshot.**)\n"
    )
    old_text = (
        "needs 4K/1080p, a platform start/end frame, or a `genre` hint → `higgsfield-seedance`\n"
        "> needs 4K, a genre hint, or platform-level start/end frame pinning, it is a Seedance 2.0 job\n"
        "> The catalog also lists utility/system entries — AutoSprite, MS Image, LLM text, upscalers\n"
    )
    ids = {"platform-start-end-frame-is-2-0-only", "llm-text-utility-in-catalog"}
    specs = _specs(tmp_path, roles=("start_image", "end_image", "image_references"))
    good = [h for h in cl.lint(_doc(tmp_path, "new.md", true_text), specs, claims) if h.claim.id in ids]
    assert all(h.ok for h in good), [(h.claim.id, h.line) for h in good if not h.ok]
    bad_tree = _doc(tmp_path / "old", "old.md", old_text)
    bad = [h for h in cl.lint(bad_tree, specs, claims) if h.claim.id in ids and not h.ok]
    assert {h.claim.id for h in bad} == ids and len(bad) == 3
