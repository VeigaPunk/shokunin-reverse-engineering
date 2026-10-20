# Round 19 W2 — carrier-runner review

## Scope and method

Axes named in `.ufo/waves/round-19/claims.json`: **calibration, freshness, depth**. This review targets the C3/depth runner and its pin, timeout, and result-status behavior. Baseline B is `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`; observed `refs/heads/main` was `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`. At that tip, `run-carriers.sh` is a newly added 334-line file relative to B.

No source or carrier was modified or executed. Driver and carrier-runner selftests ran from a disposable `mkdtemp` clone pinned to the observed tip. The driver’s adversarial path test used only a fake carrier and stub `carrier-run.py`; no REA/Ghidra launch occurred. LSP status/references/definition/diagnostics could not be run: `xd://lsp` returned `No such tool`; findings below use read source and direct fixture observations, not grep semantics.

## Findings

### Severity: Medium — `RUNS_DIR` is not a confinement boundary for TSV labels

**Observed:** `.ufo/waves/round-19/run-carriers.sh:264-276` appends an unchecked `label` to `RUNS_DIR`, canonicalizes it, accepts every path matching `/tmp/*`, then recursively removes it. The carrier/prediction existence checks occur only afterward at lines 277-282. In the isolated clone, a one-row fixture with `RUNS_DIR=<temp>/runs` and label `../victim` was accepted as `<temp>/victim`; the run deleted a pre-existing `victim/canary` before reporting the deliberately missing prediction. Driver status was 1. This is beyond the selected `RUNS_DIR`, despite remaining under `/tmp`.

**Inference:** A malformed or adversarial label can remove an arbitrary existing `/tmp/<path>` tree when the caller uses the documented `RUNS_DIR=/tmp/<dir>` mode. The current real carrier labels do not contain path separators, so this was not observed against the C3 TSV. The selftest’s `$HOME` guard case at lines 195-201 does not exercise traversal within the allowed `/tmp` subtree.

**Smallest remediation:** Validate labels as single path components and require the resolved output to be a strict descendant of the normalized selected run root; do input validation before deleting an existing output directory.

### Severity: Medium — the documented three-hour timeout ceiling is not established

**Observed:** The driver documents a 1,200-second per-step timeout and says a nine-row wave cannot stall longer than three hours (`run-carriers.sh:22-31`, with `TIMEOUT_S=1200` at line 54). It passes the same value to `carrier-run.py` at lines 317-322. The latter performs `inspect-go-binary` and then `analyze` as separate sequential calls with that timeout (`round-17/tools/carrier-run.py:355-381`); each is independently timed (`:158-184`, `:469-479`). There is no wave-level deadline in the driver. The current C3 TSV has eight rows (`predictions/carriers.tsv:1-8`). An injected 50 ms fake-sleeper probe of `run_step` returned `timeout=True`, `exit=None`, `stop=kill`.

**Inference:** Two steps can each consume nearly 1,200 seconds for one carrier, so eight rows can approach 5 hours 20 minutes (nine rows, 6 hours), before cleanup and pin/hash overhead. The existing timeout enforces a per-step bound, not the stated one-timeout-per-carrier / three-hour wave ceiling. The fake-sleeper probe validated only the timeout helper; it did not wait for a production-length timeout.

**Smallest remediation:** Either enforce a single per-carrier/wave wall-clock deadline, or revise the stated ceiling and its derivation to account for all sequential steps and overhead.

### Severity: Low — an unmatched single-label selector returns success

**Observed:** At lines 262-267, a nonempty selector that matches no TSV row skips every row while `overall` remains initialized to zero (line 263); line 334 exits with that value. With a valid one-row fixture, `bash run-carriers.sh absent-label` returned 0 with empty stdout/stderr and no output directory.

**Inference:** A typo in a requested carrier label is indistinguishable from a successful run to a caller that trusts the exit status, although no carrier was selected or compared. The built-in selector case covers a matching label only (`:146-165`).

**Smallest remediation:** Track whether the selector matched a row and return a nonzero input/selection result when it did not.

## Verified behavior and residual risk

- Driver selftest: `SELFTEST: CLEAN cases=26` (exit 0). It covers the explicit `rea-agents@6.5.0` argument, `--timeout 1200`, the expected pin count, mixed success/failure aggregation to exit 1, malformed TSV exits, and the outside-path guard (`run-carriers.sh:146-201`).
- `carrier-run.py --selftest`: `SELFTEST: CLEAN cases=3` (exit 0); its cases include carrier-byte drift detection and retained pin maps (`round-17/tools/carrier-run.py:680-715`).
- One canonical REA route is present in source: `REA_VERSION=6.5.0` is passed explicitly, and `carrier-run.py` builds `npx -y rea-agents@<version>` commands for static inspection/analyze (`round-17/tools/carrier-run.py:352-381`). No fallback or second runtime path was observed. The driver and source identify these operations as REA/Ghidra analysis, not direct carrier execution (`run-carriers.sh:2-4`; `carrier-run.py:728-739`). No REA command was launched in this review.
- No actual C3 carrier was run or rerun. Thus real-host runtime, real receipt/log binding, and an end-to-end 1,200-second timeout were not exercised. Pins were checked through the driver’s recorded argument/count selftest and the carrier-runner’s fake drift case; a live REA receipt was not produced.
- The path-traversal fixture remained within `/tmp`; this review did not attempt to write outside the assignment’s allowed report path.

## Commands and exit codes

```text
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse --verify refs/heads/main^{commit}
exit 0 — d0690fd44f46d8a7fe9da5f01c6be723d12abd41

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --name-status 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 refs/heads/main -- .ufo/waves/round-19/run-carriers.sh
exit 0 — A .ufo/waves/round-19/run-carriers.sh

git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr19-w2-ToolRunner.pFtFty && git -C /tmp/kr19-w2-ToolRunner.pFtFty checkout -q --detach d0690fd44f46d8a7fe9da5f01c6be723d12abd41 && git -C /tmp/kr19-w2-ToolRunner.pFtFty rev-parse HEAD
exit 0 — d0690fd44f46d8a7fe9da5f01c6be723d12abd41

bash /tmp/kr19-w2-ToolRunner.pFtFty/.ufo/waves/round-19/run-carriers.sh --selftest
exit 0 — SELFTEST: CLEAN cases=26

python3 -I -B /tmp/kr19-w2-ToolRunner.pFtFty/.ufo/waves/round-17/tools/carrier-run.py --selftest
exit 0 — SELFTEST: CLEAN cases=3

[Injected run_step fake-sleeper probe; timeout=0.05s]
result PASS — timeout=True, exit=None, stop=kill (no REA or carrier process)

[Isolated fixture invocation: cloned driver, RUNS_DIR=<temp>/runs, TSV label ../victim]
exit 1 — pre-existing <temp>/victim/canary was deleted; driver then reported the intentionally missing prediction

[Same isolated one-row fixture: cloned driver absent-label selector]
exit 0 — no stdout/stderr and no selected output
```
