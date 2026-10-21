# R21Attack36 — R21-C2 retrospective compatibility: `t1246-cgo`

Axes: calibration; depth.

## Findings by severity

- **No actionable defect found in this assigned case.** This is one exact retained R20 artifact, not a fresh forecast. The R20 binding identifies the log as `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-cgo/logs/rea-ghidra-I0zRdH/ghidra.log` and records SHA-256 `54fad0465e638329ee95861dc38c373db0aa070540668bc70acf9c87bdedeee0`. Independent `sha256sum` output was `54fad0465e638329ee95861dc38c373db0aa070540668bc70acf9c87bdedeee0  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-cgo/logs/rea-ghidra-I0zRdH/ghidra.log`; it matches the binding digest.

  The frozen prediction at `.ufo/waves/round-20/predictions/swiss-misread-v2/t1246-cgo.json` has `first_failure.h1: null`. The assigned comparison used the R21 comparator with the original R20 extractor on that prediction and bound log. Captured process details:

  - argv: `["python3", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/compare-first-failure.py", "--prediction", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/predictions/swiss-misread-v2/t1246-cgo.json", "--log", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-cgo/logs/rea-ghidra-I0zRdH/ghidra.log", "--extractor", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/first-failure-extract.py"]`
  - stdout: `{"finding": "failure_match", "last_line": 177, "match": true, "observed": null, "predicted": null}\n`
  - stderr: empty
  - exit: `0`

  Therefore this artifact retains a match for the comparator's null/null first-failure result, bounded by the extractor's reported final line 177. This supports the `t1246-cgo` compatibility case only; it does not establish all nineteen retained matches.

## Residual risk

A null first-failure match means no qualifying failure was observed by this extractor through line 177; it is not evidence that analysis succeeded. Unrelated analyzer errors, if present, are outside this comparison and do not establish success. The comparator output does not expose the extractor's `other_errors`, and I did not classify them. Other retained labels and C2 malformed-observation / kind / index cases are outside this assignment.

## Verification gaps and boundaries

- No `lsp` device/server is exposed in the available tool inventory, so LSP status, references, definition, and diagnostics could not be queried. No text grep was used as semantic proof.
- No REA tool, native carrier, fresh forecast, broad battery, build, formatter, or production edit was used. Only the bound-log hash and assigned retrospective comparison were run; this report is the sole write.
- No installs or updates.