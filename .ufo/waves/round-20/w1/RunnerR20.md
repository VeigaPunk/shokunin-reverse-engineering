# RunnerR20 handoff

**Axes:** calibration, coverage, depth.

## Files and behavior

- Patch: `.ufo/waves/round-20/w1/patches/RunnerR20.patch` adds `.ufo/waves/round-20/run-carriers.sh` (451 lines, executable; staged diff stat: `1 file changed, 451 insertions(+)`). The report is this file.
- The runner reads `predictions/carriers.tsv`, expects per-label `<label>.prediction.json`, checks the carrier SHA-256, and keeps output under `runs/<label>/`; paths, pin set, and manifest validation are at `run-carriers.sh:15-28,216-268,272-279`.
- `--dry-run` prints the guard/analyze/compare plan and checks inputs without invoking guard or REA or creating run output (`:280-299`). Each actual label invokes the required `carrier-guard.py check --manifest predictions/carriers.tsv --record evidence/carrier-guard` before run setup; any nonzero guard result aborts (`:301-307`). Carrier-run is explicitly pinned to REA 6.5.0 and timeout 1200 (`:361-369`).
- Comparison requires exactly one receipt-bound session and its matching retained `ghidra.log` record, verifies the recorded SHA-256 against the file, saves `comparison-log-binding.json`, then calls `compare-first-failure.py --prediction ... --log ... --extractor ...` (`:378-442`). This implements the D3/C3 interfaces in `contract.md:46-52,76-81`.

## Retained evidence and checks

- Clone base observed: `14f0260ad319ecc26994381b2415d5a999003375`.
- Final selftest exact last line: `SELFTEST: CLEAN cases=20`; exit **0**. It uses temporary fixtures/stubs, including dry-run, guard-abort, mismatch, and log-digest binding cases (`run-carriers.sh:36-196`). No real carrier or REA run was performed.
- Final ShellCheck: exit **0**, no diagnostics. `/usr/bin/shellcheck` was already available; no tools were installed or updated.
- Patch generation: `git -C /tmp/kr20-RunnerR20 diff --cached --binary 14f0260ad319ecc26994381b2415d5a999003375 > /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches/RunnerR20.patch`; exit **0**. Cached stat command: `git -C /tmp/kr20-RunnerR20 diff --cached --stat 14f0260ad319ecc26994381b2415d5a999003375`; exit **0**, `1 file changed, 451 insertions(+)`.
- Other commands and outcomes (including corrected iterations):
  - `git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr20-RunnerR20 && git -C /tmp/kr20-RunnerR20 checkout -q --detach 14f0260ad319ecc26994381b2415d5a999003375 && git -C /tmp/kr20-RunnerR20 rev-parse HEAD` — exit **0**, printed the base above.
  - `command -v shellcheck` — exit **0**, `/usr/bin/shellcheck`.
  - `mkdir -p /tmp/kr20-RunnerR20/.ufo/waves/round-20` — exit **0**.
  - `shellcheck /tmp/kr20-RunnerR20/.ufo/waves/round-20/run-carriers.sh` — first exit **1** (SC2319 test-helper warnings); subsequent two invocations exit **0** with no diagnostics.
  - `bash /tmp/kr20-RunnerR20/.ufo/waves/round-20/run-carriers.sh --selftest` — first exit **1** (fixture log directory and duplicate pin-count assertions); second exit **1** (selftest expected the true binding predicate to be 0); final exit **0**, exact output above.
  - `git -C /tmp/kr20-RunnerR20 add -- .ufo/waves/round-20/run-carriers.sh` — exit **0**.
  - `mkdir -p /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches` — exit **0**.

## Risks and blockers

- **Observation:** baseline B has no W20 tree/manifest or W20 tools yet. The L1 must integrate those deliverables and run the runner after predictions are frozen, as required by `claims.json:36-39` and `contract.md:83-92`.
- **Risk:** the wrapper deliberately treats zero/multiple bound sessions or any path/digest discrepancy as unevaluable (exit 2 compare record); it does not guess which log to compare. Current R19 carrier-run evidence has one bound analyze session (`round-19/tools/carrier-run.py:380-408`).
- LSP was not used: this is a new shell driver with no symbol definition/reference/refactor operation; no LSP endpoint is exposed in the available tool inventory.
