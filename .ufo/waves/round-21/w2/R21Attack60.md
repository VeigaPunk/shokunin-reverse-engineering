# R21Attack60 — isolated-control second-package decoy

## Findings (severity order)

**No actionable finding against the assigned positive/decoy behavior or the stated no-C3/no-fixture-execution boundary.** One invocation of `tools/isolated-control.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin` returned `finding: isolated_control_clean`. The genuine synthetic `analyze` receipt was accepted (exit 0, valid, no findings); the second-package decoy was rejected (exit 1) with `analyze_step_unauthenticated`. The decoy also reports `mid_checks_absent`, as expected because its claimed analyze step did not authenticate.

The decoy bytes are exactly the case constructed at `isolated-control.py:43-46`: `npx -y rea-agents@6.5.0 inspect-go-binary rea-agents@6.5.0 analyze`. The validator requires the `analyze` subcommand immediately after the first pinned package token (`round-17/tools/receipt-validate-v2.py:134-156`); it does not search later argv tokens. Its unauthenticated finding is triggered when a step claims `analyze` but fails that predicate (`:614-654`). The positive is not reject-all: the returned positive receipt is `status: valid`, `findings: []`.

Source-path review supports the isolation boundary. The helper loads only the R17 validator and sibling `pins.py` (`isolated-control.py:18-23`), creates its carrier, fake log, maps, and receipt JSON under one temporary directory (`:24-46`), and passes only the validator path plus those receipt paths to `subprocess.run` (`:47-53`). The recorded fixture `step['argv']` is written as JSON metadata; no call invokes it. The validator rechecks recorded receipt fields and paths (`receipt-validate-v2.py:169-242,491-654,685-733`); it has no process-execution path (the literal source search found only its documentation saying no subprocesses). The pin snapshot receives only the temporary inert carrier path (`pins.py:62-71`). No C3 run or prediction path is formed or passed by this helper. `verify.py:51-56` independently shows the intended no-C3 check constructs a scratch root containing only the R17 validator and pins, though that full verifier was not run for this assignment.

## Run record

Working directory: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`

Top-level argv:

```text
python3 -I -B .ufo/waves/round-21/tools/isolated-control.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin
```

Top-level stdout (verbatim):

```json
{"authority_sha256": "7b7f4aba26e7ba5f2e63fcf7a31beb69c1d34de791a3a11b8d19fdabeb0f5d9b", "cases": [{"argv": ["/usr/bin/python3", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/receipt-validate-v2.py", "--require-mid-maps", "/tmp/kaidoku-r21-control-ti_og57e/positive.json"], "expected_exit": 0, "finding_ok": true, "id": "independent_positive", "observed_exit": 0, "pass": true, "stderr": "", "stdout": {"counts": {"invalid": 0, "receipts": 1, "unreadable": 0, "valid": 1}, "exit": 0, "pins_available": true, "pins_path": "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/pins.py", "receipts": [{"checks_performed": 40, "findings": [], "kind": "carrier", "receipt": "/tmp/kaidoku-r21-control-ti_og57e/positive.json", "status": "valid", "valid": true}], "require_mid_maps": true, "tool": "receipt-validate.py"}}, {"argv": ["/usr/bin/python3", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/receipt-validate-v2.py", "--require-mid-maps", "/tmp/kaidoku-r21-control-ti_og57e/decoy.json"], "expected_exit": 1, "finding_ok": true, "id": "independent_decoy", "observed_exit": 1, "pass": true, "stderr": "", "stdout": {"counts": {"invalid": 1, "receipts": 1, "unreadable": 0, "valid": 0}, "exit": 1, "pins_available": true, "pins_path": "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/pins.py", "receipts": [{"checks_performed": 40, "findings": [{"code": "analyze_step_unauthenticated", "detail": "analyze must immediately follow a rea-agents@<version> package token", "where": "$.steps[0].argv"}, {"code": "mid_checks_absent", "detail": "analyze step has no mid-run pin checks", "where": "$.steps.analyze.pin_checks"}], "kind": "carrier", "receipt": "/tmp/kaidoku-r21-control-ti_og57e/decoy.json", "status": "invalid", "valid": false}], "require_mid_maps": true, "tool": "receipt-validate.py"}}], "finding": "isolated_control_clean", "limit": "synthetic recorded receipt metadata only; never executes fixture argv; no C3 forecast/run file read"}
```

Top-level stderr: no separate stderr output was reported; both nested validator stderr fields are empty. Top-level exit: **0**, consistent with the observed clean result and the code path returning 0 when both cases pass (`isolated-control.py:54-55,69-74`); the Bash tool response did not separately print a numeric status. Nested observed exits are explicitly 0 for the positive and 1 for the decoy in the verbatim output above.

## Residual risk

This is a synthetic metadata/validator control, not an execution of REA/analyzer and not a cryptographic-authenticity or security-containment test; the C1 claim itself limits its scope. The helper is a supplementary check rather than a counted battery case: `battery.py:70-76` selects `verb-coverage.py` for C1, while `verify.py:46,51-56` runs this helper separately, including an isolated-root invocation. A C1 battery result alone therefore does not evidence this control; use the separate verifier check for that assertion.

## Verification gaps

- `xd://lsp` is not mounted in this session, so no LSP status, references, definition, or diagnostics were available. Literal text search found the helper references in `verify.py`; source review of `verify.py:43-56` and `battery.py:68-76` establishes the caller distinction, while the search itself is not treated as semantic proof.
- `git diff HEAD -- .ufo/waves/round-21/tools/isolated-control.py` and `git status --short -- .ufo/waves/round-21/tools/isolated-control.py` returned no output. This report reviews the checked-out source; no working-tree delta for the target was observable.
- Only the assigned helper mode was invoked, once. The overall `verify.py` suite and the no-C3 scratch-root invocation were inspected in source but not run here.
