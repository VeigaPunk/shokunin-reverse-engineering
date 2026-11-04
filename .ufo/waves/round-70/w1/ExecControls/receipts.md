# ExecControls — round 70, attempt 1, w1

Axes: calibration, operability, coverage. No implementation changes.

## Execution and retained evidence

Both assigned commands ran concurrently with isolated work subdirectories beneath the seat scratch root. Exact argv, exit codes and output hashes are in `execution.json`; unmodified stdout/stderr are in `controls.stdout.txt`, `controls.stderr.txt`, `battery.stdout.txt`, `battery.stderr.txt`. All six working-tree instrument hashes matched the claims-container pins before execution; recorded in `evidence-manifest.json`. Child instruments were extracted by the frozen drivers with `git show` at the specified freeze/base revisions.

- Freeze: `4737a542ae3b1b910d8fe43efbd572bc578b07c6`.
- Base: `5cc845ca88c90e3e8ceb816f75fe44ddb6758a6d`.
- Base probe: `5ee94c56ce7490938ee38c2e5c10930a1fd1330a`.
- Genuine material: the explicitly assigned declaration receipt, preserved unchanged as `landing-material.json`; its recorded revision is `8b82516182a269482f3a7dc96b50cd2ac349f3a6`.
- Base material is preserved as `base-material.json`.
- `retained/` contains the ten forged input receipts, wrong-revision control receipt and both constant battery inputs, copied before scratch removal. The manifest hashes these files.

## Controls: met, seven of seven

`controls-at-freeze.json`: exit 0, `ok: true`, `failures: []`.

| Arm | Observed |
|---|---|
| c1-base-accepts-forged | exit 0, met true for wrong revision |
| c1-constant-battery | exit 1, `mutants absent or empty` |
| c2-base-execformat-crash | exit 1, traceback containing errno 8 exec-format error |
| c2-base-impostor-runs | impostor executed; exit 2 on sha256 mismatch |
| c2-new-refuses-unrun | impostor not executed; exit 2 on sha256 mismatch |
| c3-base-three-carrier | exit 0, met true, target 3, no static-exe kind |
| c3-new-rejects-old-receipt | exit 1, instrument.sha256 producer-binding failure and target 3 != 4 |

## Forged-receipt battery: not met

`battery-at-freeze.json`: exit 1, `ok: false`. Exactly two failures:

1. `genuine landing receipt rejected by the frozen checker`: checker exit 1, met false.
2. `genuine landing receipt rejected by the frozen probe`: probe exit 1, 4/6 arms passed.

All ten F1–F10 shapes were accepted by the base reader (exit 0, met true), rejected by the frozen checker (exit 1), and recorded `clause_found: true`. All five identity shapes recorded frozen probe exit 1 with A5/A6 false and base probe exit 0. The battery's wrong-pin and floor arms each exited 1 with the required named clause; work directories were distinct; constant validation exited 1.

### Revision mismatch in the assigned genuine-material arm

The supplied genuine receipt records declaration revision `8b82516182a269482f3a7dc96b50cd2ac349f3a6`, whereas the invocation requires freeze revision `4737a542ae3b1b910d8fe43efbd572bc578b07c6`. The producer hashes match; revisions do not. Static source evidence: `packed-elf.py:400-401` rejects `receipt.rev != rev`; `contract-probe.py:160-161` appends that producer failure, which feeds both A5 and A6 at lines 223-244. Thus the supplied declaration receipt is not a freeze-revision genuine receipt under these readers. [INFERENCE] This explains the measured two-arm failure; it is not evidence of unsafe reader acceptance. The battery does not retain raw genuine checker/probe output, so the exact failure clause for that invocation is inferred from the preserved input and source, not claimed as directly captured output.

Do not relabel the receipt or report the aggregate battery green. The L1 must resolve genuine-material/revision alignment for its own integration gate. This seat did not rerun or alter the prescribed measurement.

## Scope, limitations and cleanup

Only files beneath this findings directory were retained. All scratch contents and the scratch root were removed after evidence capture. No source edits, git mutations, installs, external-state changes, builds, formatters or unrelated tests. No LSP symbol operation was needed; no LSP interface is exposed to this seat. The dedicated seven-arm seam probe and fresh carrier producer run were not assigned here; controls are not substitutes for those complete claims. No independent conclusion about all of R70-C2 or landing-state R70-C3 is asserted.

The requested sibling `w1/ExecControls.md` trailer conflicts with the binding directory-only write scope; this report is intentionally retained here as `w1/ExecControls/receipts.md`.

VERDICT: not-met — controls 7/7 met; frozen forged-receipt battery fails both genuine-material arms with declaration receipt supplied to freeze-revision readers.
