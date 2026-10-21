# R21Attack37 — R21-C2 retrospective compatibility: `t1246-compile`

Axes: calibration; depth.

## Findings by severity

- **No actionable defect found in this assigned case.** This is one exact retained R20 artifact, not a fresh forecast. The R20 `comparison-log-binding.json` names `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-compile/logs/rea-ghidra-Q6goA3/ghidra.log` and records SHA-256 `4bb27c126d92f517a49d7f62d1ae8388493ad474193d57ab9b0394c406a29a42` (`verified: true`). The assigned `sha256sum` stdout was:

  ```text
  4bb27c126d92f517a49d7f62d1ae8388493ad474193d57ab9b0394c406a29a42  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-compile/logs/rea-ghidra-Q6goA3/ghidra.log
  ```

  This matches the binding digest.

  I ran the R21 comparator on the frozen prediction at `.ufo/waves/round-20/predictions/swiss-misread-v2/t1246-compile.json`, bound log, and original R20 extractor. Captured process details:

  - argv: `["python3", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/compare-first-failure.py", "--prediction", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/predictions/swiss-misread-v2/t1246-compile.json", "--log", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-compile/logs/rea-ghidra-Q6goA3/ghidra.log", "--extractor", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/first-failure-extract.py"]`
  - stdout (one trailing newline): `{"finding": "failure_match", "last_line": 437, "match": true, "observed": {"index": 36421889, "kind": "invalid_index", "phase": "markup", "va": null}, "predicted": {"index": 36421889, "kind": "invalid_index", "phase": "markup_walk", "va": 14607072}}\n`
  - stderr: empty
  - exit: `0`

  The predicted and observed first failures match on the comparator's declared kind/index predicate (`invalid_index`, index `36421889`), bounded by extractor line `437`. The differing phase and VA fields do not change that comparison result. This supports only this retained-label compatibility case; it does not establish all nineteen retained matches or the full C2 claim.

## Residual risk

A first-failure match is not evidence that analysis succeeded. Unrelated analyzer errors, if present, are outside this comparison and do not establish success; I did not classify them. Other retained labels and C2 malformed-observation, asymmetric-null, kind, and index controls are outside this assignment.

## Verification gaps and boundaries

- No `lsp` device/server is exposed in the available tool inventory (`read xd://lsp` returned `No such tool`). Therefore LSP status, references, definition, and diagnostics were unavailable; no text grep was used as semantic proof.
- No REA tool, native carrier, fresh forecast, broad battery, build, formatter, or production edit was used. Only the assigned retained-log hash and retrospective comparison were run; this report is the sole write.
- No installs or updates.

Report: `.ufo/waves/round-21/w2/R21Attack37.md`
