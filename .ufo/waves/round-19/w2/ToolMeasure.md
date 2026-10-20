# Round 19 wave 2 — ToolMeasure review

Axes: calibration (C1), freshness (C2), depth (C3).

## Finding — High: C3 output is not the amended bound-run count

**Observation.** At the pinned main revision, `measure.py` reports 8 frozen-hash predictions, 8 `compare.json` files, 8 `compare.exit` files, 7 zero exits and 7 recorded `all_match: true` values. Its C3 status is `evaluated` and the top-level `could_not_evaluate` is false. Those values are reproduced below; they are raw committed-artifact counts.

The amended contract is narrower: `predictions/decision-rule.json:3,6` says a label counts only after `receipt-validate.py --require-mid-maps` succeeds, the bound log carrier SHA matches the prediction, and the prediction blob is unchanged from its freeze commit; the count is labels with a bound retained log and `compare.json`. `claims.json:40,46` repeats the 0→8 count and says final counts must require live receipt validation at the delivered source, rather than treating first-pass records as current.

`measure.py` does not enforce that qualification: `RUNS_RE`/`EXIT_RE` at `measure.py:75-76` match only `runs/<one-component>/compare.json|compare.exit`; `_claim_c3` at `:579-657` reads prediction JSON, compare JSON and exit blobs, counts `len(runs)` at `:613`, and copies `all_match` at `:621-623`. It does not inspect receipts, retained logs, or validation results. The path pattern also excludes the amended `runs/pass2/<label>/...` layout, even if those files are committed. The worktree showed `runs/pass2/` as untracked at review time, so it was not part of the measured main commit. Thus `c3_compare_jsons=8` is an immutable census of direct-child compare artifacts, not evidence that eight labels satisfy the amended count rule. The separate `verify.py` flow does invoke receipt validation and compares per source label (`verify.py:559-615`), but that evidence is not part of `measure.py`'s C3 status/count. This finding does not assert that any individual receipt fails; it identifies an unmeasured required predicate.

**Inference / recommendation.** Consumers must not treat this `measure.py` C3 count or `could_not_evaluate=false` as the qualified 0→8 claim. Either expose a per-label qualifying count from the live binding gate and account for the pass2 layout, or name/document these fields strictly as raw artifact counts and require the separate validation result alongside them.

## C1/C2 interface and revision results

**Observation.** The main-revision interfaces are compatible with the in-process runner. `measure.py:215-267,270-293` installs `sys.argv` for no-argument `main()` functions and passes an argv list to functions that accept one; C1 is invoked with `--root`, `--rev`, `--strict` at `:328-330`, and C2 with `--root`, `--rev` at `:461-463`. The pinned main C1 tool exposes those flags and emits its revision/count JSON (`tools/routed-r18.py:406-423,312-332`); C2 exposes `main(argv=None)`, reads `--root/--rev`, and emits `rev`/`mismatch_count` (`tools/province-pins.py:244-320,639-670`). The main-run output had both `tool_rev` values equal to `279e8b19c51658bfd05b9e31a1c0894ab2e70537`, C1 exit 0/open_count 0 and C2 exit 0/mismatch_count 0. The census `--root --json` contract is compatible too (`c1-census-v10.py:627-710`; runner `measure.py:391-398`): it returned valid JSON with exit 1 and `FAIL`, not a false PASS.

At B, both C1/C2 tool counts were JSON `null`, status `could-not-evaluate`, reason `tool_absent_at_rev`; C3's six numeric artifact counts were measured zeros and C3 status was `evaluated`. Top-level exit was 0 and `could_not_evaluate` was true. This is the correct distinction between absent tools and a measured zero: `measure.py:32-40,322-324,455-457,624-631` and its fixture assertions at `:1009-1029` agree. `measure.py` itself was added after B, so the B result necessarily used the main copy of the measurement program against B's immutable tree.

**Commands and observed exit codes** (run from the lane root; each invocation used the explicit revision):

```text
python3 -I -B .ufo/waves/round-19/measure.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0
exit=0

python3 -I -B .ufo/waves/round-19/measure.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin 279e8b19c51658bfd05b9e31a1c0894ab2e70537
exit=0
```

**Observation.** The pinned-main C3 output was `prediction_files=8`, `labels_frozen=8`, `compare_jsons=8`, `compare_exit_files=8`, `compare_exit0=7`, `matched=7`, with no unparseable predictions or compares. Main C1/C2 were evaluated as above; the C2 census still reported `FAIL`, exit 1, `stale=0`, `undeclared=2`.

## Residual risks and verification gaps

- `measure.py:84-87` explicitly says the census gate is the revision's code run against the current lane worktree and live host configs. Accordingly, the B run's embedded gate result (`stale=0`, `undeclared=2`) is not a historical B-tree census and cannot substantiate the historical `stale=4` baseline in `claims.json:20`; it is the documented live reading. No C1/C2 tool count is inferred from that gate result.
- At review time `refs/heads/main` was `279e8b19c51658bfd05b9e31a1c0894ab2e70537`, while the worktree was dirty, including a modified `tools/routed-r18.py` and untracked `runs/pass2/`. The two commands measure committed revision blobs (except the explicitly live gate input); they do not validate the later working-tree C1 source or count uncommitted pass2 files.
- LSP was unavailable: attempting `read xd://lsp` returned “No such tool” and the mounted-device list contained no LSP device. I used the literal `grep` fallback only to locate textual callers; it found the registry entry at `SKILL.md:599` and `verify.py` invocations at `:556-557`. These are textual matches, not semantic reference/definition/diagnostics proof. No selftest, mutation test, build, REA, or Ghidra run was performed.
