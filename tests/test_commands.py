"""Slash-command contracts — the promises each .claude/commands/*.md must keep.

/validate declared "release-ready" from the NON-strict run while --strict was
red; /release told the agent to push to protected `main` and tag whatever HEAD
was, contradicting CLAUDE.md (branch → PR → merge → tag the MERGE commit; PDF
regenerate → MANIFEST → upload). These tests pin the corrected contracts.
"""
import re

from conftest import REPO

CMD = REPO / ".claude" / "commands"


def _code_blocks(text):
    return "\n".join(re.findall(r"```(?:bash)?\n(.*?)```", text, re.DOTALL))


def test_validate_command_readiness_needs_all_three_gates():
    text = (CMD / "validate.md").read_text(encoding="utf-8")
    code = _code_blocks(text)
    assert "python3 scripts/validate.py --strict" in code
    assert "python3 -m pytest tests/ -q" in code
    assert "python3 scripts/validate.py --evals" in code
    # the only unflagged validate.py invocation in the runnable block is strict
    assert re.findall(r"validate\.py(?! --)", code) == []
    assert "release-ready** ONLY when all three" in text


def test_release_command_follows_the_protected_main_ceremony():
    text = (CMD / "release.md").read_text(encoding="utf-8")
    assert "git push && git push --tags" not in text          # no direct push to main
    assert "git switch -c release/v$ARGUMENTS" in text
    assert "gh pr create --base main" in text
    assert "mergeCommit" in text and 'git tag -a v$ARGUMENTS "$MERGE"' in text
    assert "git push origin --delete release/v$ARGUMENTS" in text
    # regenerate → refresh MANIFEST → upload, in that order
    gen = text.index("generate_user_guide.py")
    manifest = text.index("--write-manifest")
    upload = text.index("gh release upload")
    assert gen < manifest < upload
    # tagging happens after the merge
    assert text.index("gh pr merge") < text.index('git tag -a v$ARGUMENTS')


def test_refresh_specs_command_covers_the_tier2_chain():
    text = (CMD / "refresh-specs.md").read_text(encoding="utf-8")
    for needle in ("models_explore", "has_more: true", "sync_specs.py --type",
                   "snapshot_crosscheck.py", "crosscheck_allowlist.json",
                   "--changed", "validate.py --strict", "pytest tests/",
                   "validate.py --evals", "refresh_specs.py --update-baseline"):
        assert needle in text, needle
    for t in ("video", "image", "audio", "3d"):
        assert f"`{t}`" in text
    # the order of the chain matters: dump → sync → cross-check → evals → gates → baseline
    order = [text.index(n) for n in ("models_explore", "sync_specs.py --type video",
                                     "snapshot_crosscheck.py", "--changed",
                                     "validate.py --strict", "--update-baseline")]
    assert order == sorted(order)
    assert "never call a `generate_*`" in text.lower() or "Never call a `generate_*`" in text


def test_refresh_specs_command_says_membership_and_unchecked_block():
    text = (CMD / "refresh-specs.md").read_text(encoding="utf-8")
    assert "`snapshot-only` | `cli-only`" in text      # membership entries documented
    assert "exit 3 (`UNCHECKED`" in text and "never a pass" in text


def test_refresh_specs_step6_can_go_red():
    # "--update-baseline, then the tripwire must be Fresh" could never fail:
    # the self-diff compares the live CLI with what was just captured. The
    # tripwire runs BEFORE the accept, every non-0/3 exit stops, and the
    # capture's per-type counts are checked.
    text = (CMD / "refresh-specs.md").read_text(encoding="utf-8")
    step6 = text[text.index("6. **Accept the live CLI surface**"):text.index("7. **Report")]
    before = step6.index("First the tripwire BEFORE accepting")
    assert before < step6.index("--update-baseline")
    for code in ("1 = pull failed", "4 = the CLI output", "5 = the script crashed"):
        assert code in step6, code
    assert "refuses" in step6 and "model count per type" in step6
