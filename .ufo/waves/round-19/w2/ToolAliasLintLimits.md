# ToolAliasLintLimits — wave 2 review

Reviewed baseline `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` against observed `refs/heads/main` tip `279e8b19c51658bfd05b9e31a1c0894ab2e70537`. Axes: calibration, freshness, depth. No production files were edited.

## Findings

### P2 — registered nested-read limit points to a stale source line

**Observation:** `SKILL.md:587` now registers the nested-read limitation and links the revpin example to `.ufo/waves/round-18/tools/revpin.py:108`. In the current source, line 108 is the `"source": None` field in the `branch_missing` result; the actual `HEAD` read is line 113. The R19 revpin wording change inserted five documentation lines at `revpin.py:5-9`, shifting the old anchor. The other link, `.ufo/waves/round-17/verify.py:83`, still points at the `HEAD` read.

**Inference:** The registered statement is substantively right, but its current `revpin.py:108` citation is stale and lands on unrelated data. Update it to `:113` (or use a stable symbol/context reference).

**Source-selection check (observation):** In round-17 `resolve_source`, `source` comes from `refs/heads/<branch>` at `verify.py:81`, `HEAD` is read separately at `:83`, and the code compares `head != source` at `:93` before returning both at `:101-102`. In round-18 `revpin.resolve_source`, `source` comes from `refs/heads/<branch>` at `revpin.py:103`; `HEAD` is read at `:113`, stored as `head_equals_source` at `:119`, and can only trigger the mismatch refusal at `:123-124`. Neither nested read selects the source revision. This agrees with `corpus/lessons/round-18-verifier-spotcheck.md:111-114`.

### Candidate-only blocker — inherited `HeadRevLintNested` patch fails its selftest

**Observation:** Applied the inherited patch only in a private clone at the observed main tip. `git apply --check` and `git apply` both succeeded. The candidate `--selftest` exits 1 with `SELFTEST: FAILED 3`; a direct traceback locates the failure at the candidate's `assert result["fixture_count"] == 2`, observing `3` (temporary clone line 1341).

The patch adds `FIXTURE_NESTED_PY` to the first selftest revision (`.ufo/waves/round-19/w1/inherited/HeadRevLintNested.patch:539-583`, especially `:580`), but the unchanged second-revision cleanup at `.ufo/waves/round-18/tools/head-rev-lint.py:856-868` removes only `live.py`, `edge.py`, and `run.sh`; it leaves `nested.py` in place. Its direct wrapper call in `nested.py`'s `selftest()` remains a fixture site, so the later expected count at `:869-873` is short by one. The baseline tool's selftest at the same tip passes (`SELFTEST: CLEAN cases=3`).

**Candidate documentation contrast:** The patch explicitly says nested sites are a separate class outside `sites[]`/`live_count` and do not affect `--strict` (`HeadRevLintNested.patch:19-21, 36-38, 63-65`). Its `nested_live_count` is defined as the subset whose *context* is `live`, not as a count of source selectors. The patch fixture makes the distinction visible: `source` is assigned from `refs/heads/` at `:561`, the separate `HEAD` value at `:562` is only returned alongside it, and the selftest read at `:569` is also only returned (`:560-570`). These fixtures do not demonstrate a source-selection bug.

**Disposition evidence:** `wave1-outcomes.json:202-205` says the W1 seat was aborted and has no delivered report; it is not a retained selftest receipt. My isolated reproduction confirms the current `SKILL.md:587` statement that the inherited patch failed its selftest, and the R19 diff leaves the canonical W18 lint implementation unchanged. Treat the failure as a blocker for reviving that candidate, not a regression in the current tool.

## Verification

Commands and results (all test/mutation work was confined to `mkdtemp` clones):

```text
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse refs/heads/main
exit 0 -> 279e8b19c51658bfd05b9e31a1c0894ab2e70537

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --name-status 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 279e8b19c51658bfd05b9e31a1c0894ab2e70537 -- .ufo/waves/round-18/tools/head-rev-lint.py .ufo/waves/round-18/contract.md .ufo/waves/round-18/final-recheck/controls.receipt.json.stdout
exit 0 -> no paths (canonical W18 lint/docs/receipt unchanged)
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --unified=3 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 279e8b19c51658bfd05b9e31a1c0894ab2e70537 -- SKILL.md .ufo/waves/round-17/verify.py .ufo/waves/round-18/tools/revpin.py .ufo/waves/round-18/tools/head-rev-lint.py .ufo/waves/round-19/w1/inherited/HeadRevLintNested.patch
exit 0 -> shows the five-line revpin documentation insertion, the SKILL row addition, and the carried patch; no `head-rev-lint.py` implementation change


git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr19-ToolAliasLintLimits-3-_ifj1ezx
exit 0

git -C /tmp/kr19-ToolAliasLintLimits-3-_ifj1ezx checkout -q --detach 279e8b19c51658bfd05b9e31a1c0894ab2e70537
exit 0

git -C /tmp/kr19-ToolAliasLintLimits-3-_ifj1ezx rev-parse --verify 279e8b19c51658bfd05b9e31a1c0894ab2e70537
exit 0 -> 279e8b19c51658bfd05b9e31a1c0894ab2e70537

git -C /tmp/kr19-ToolAliasLintLimits-3-_ifj1ezx apply --check /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/w1/inherited/HeadRevLintNested.patch
exit 0

git -C /tmp/kr19-ToolAliasLintLimits-3-_ifj1ezx apply /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/w1/inherited/HeadRevLintNested.patch
exit 0

python3 -I -B /tmp/kr19-ToolAliasLintLimits-3-_ifj1ezx/.ufo/waves/round-18/tools/head-rev-lint.py --selftest
exit 1 -> SELFTEST: FAILED 3

python3 -I -B -c 'import runpy; d=runpy.run_path("/tmp/kr19-ToolAliasLintLimits-3-_ifj1ezx/.ufo/waves/round-18/tools/head-rev-lint.py"); d["selftest"]()'
exit 1 -> AssertionError at candidate line 1341: expected fixture_count 2, got 3

git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr19-ToolAliasLintLimits-base-aidhimbw
exit 0

git -C /tmp/kr19-ToolAliasLintLimits-base-aidhimbw checkout -q --detach 279e8b19c51658bfd05b9e31a1c0894ab2e70537
exit 0

python3 -I -B /tmp/kr19-ToolAliasLintLimits-base-aidhimbw/.ufo/waves/round-18/tools/head-rev-lint.py --selftest
exit 0 -> SELFTEST: CLEAN cases=3
```

LSP status: no `lsp` device is mounted (`read xd://lsp` returned `No such tool`). Text search was only used to locate references; semantic conclusions above are based on source reads, the pinned diff, and isolated selftest results. No builds, broad suites, formatting, or installs were run.
