# ExecC2 — independent R72-C2 re-derivation

Axes: revision fidelity, mutation discrimination, reproducibility.

## Measured results

- Exact requested r71 command, using the lane battery: exit 0; pristine 7 cases green; survivor_count 1; survivors ["A10_binding_force_true"]. Evidence: ExecC2/requested-r71.json and matching stdout/stderr.
- Exact requested r72 command targeting declaration 6316c105: exit 2, `patch site A10_binding_force_true matched 0 times (want 1)`. No requested-r72.json was produced; retained stderr is the receipt of non-evaluation, not a kill.
- The declaration's own frozen battery was also run against both requested targets: each exits 2 with `pristine selftest not green: rc=0 failed=None`. It predates the selftest-schema fix. Frozen declaration source bytes and both outputs are retained.
- Operative freeze 34fe7aa70b627d92e2d27dbce308d9f5bebda63d, explicitly distinguished from declaration: its frozen battery against r71 reports the same single survivor; against its own r72 probe reports pristine 10 cases green, survivor_count 0, killed ["A10_binding_force_true"], failed ["a10-binding-from-checker"], mutant exit 1, battery exit 0. Evidence: ExecC2/operative-r71.json and operative-r72.json.
- Independent scratch mutant: copied operative probe directly from git show; surgically changed line 176 from `binding_ok = clauses.get("run_binding") is True and present` to `binding_ok = True`, without using the battery to construct it. Selftest exit 1, cases 10, failures ["a10-binding-from-checker"]. Restored the exact original line and reran: exit 0, cases 10, failures []. Mutant bytes and both stdout/stderr pairs retained. The declaration probe lacks this assignment expression, so this independent result is explicitly for the operative freeze, not declaration.
- Landing receipt was absent on first read, then appeared before completion. A10 ok=true, genuine_rc=0; genuine_verdict present/nonce_ok/binding_ok all true. Wrong nonce: rc=1, present=true, nonce_ok=false, binding_ok=false. Broken binding: rc=1, present=true, nonce_ok=true, binding_ok=false. Retained projection and source hash: ExecC2/landing-a10.json. These are reported clause readings from the landing summary; this seat did not independently regenerate that landing run.

## Evidence and limitations

All commands, exit statuses, stdout/stderr and source SHA-256 values: ExecC2/execution-ledger.json. Sources retained as mutation-check.frozen.py, seam-probe.frozen.py (declaration), mutation-check.freeze.py, seam-probe.freeze.py (operative), and seam-probe.independent-mutant.py. Raw per-run outputs remain alongside JSON receipts. No production implementation was modified. No tool installations, git mutations, builds, linters, formatters, package checks or external-state changes. Only explicitly assigned instrument selftests were exercised. No UPX operation is needed by this selftest-only battery; --expect-upx does not apply. No LSP tool is exposed in this seat; no symbol refactor was performed.

The operative frozen state supports the requested calibration distinction; the literal declaration-target command does not establish a kill. Do not cite declaration 6316c105 as the passing target. Scratch is removed in a finally block after receipt retention. No blocker remains for this scoped investigation; revision mismatch is a retained risk for downstream command reproduction.

Report: .ufo/waves/round-72/w1/ExecC2/ExecC2.md
