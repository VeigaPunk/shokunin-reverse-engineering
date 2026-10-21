# R21Attack46 — R21-C2 retrospective: `t1246-pack`

Axes: calibration; depth. Scope is the one retained R20 label and its frozen prediction, not a fresh forecast.

## Exact-artifact result

The binding file `.ufo/waves/round-20/runs/t1246-pack/comparison-log-binding.json` names `logs/rea-ghidra-Dhu23X/ghidra.log`, records SHA-256 `e4a85f0b6ec058d05c76b1b1354ce89574e221f76a511c894ad59f411247ed06`, and says `verified: true`. `sha256sum` of that exact path returned the same digest; **digest match: yes**.

Comparator argv:

```text
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/compare-first-failure.py --prediction /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/predictions/swiss-misread-v2/t1246-pack.json --log /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-pack/logs/rea-ghidra-Dhu23X/ghidra.log --extractor /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/first-failure-extract.py
```

- stdout: `{"finding": "failure_match", "last_line": 164, "match": true, "observed": null, "predicted": null}`
- stderr: empty
- exit: `0`

The frozen prediction's `first_failure.h1` is `null`; the original R20 extractor, invoked by the comparator on the bound log, returned a null first failure with observation bound `last_line: 164`. This is a match for this exact retained artifact. It means no qualifying first failure was observed through the extractor's reported bound; **it does not establish general analyzer success**. Unrelated analyzer errors do not establish success either.

## Findings by severity

- **No actionable per-artifact mismatch found.** The one assigned retained comparison matched. This does not verify the other eighteen retained results or independently authored malformed-observation controls.

## Residual risk and verification gaps

- Evidence is limited to `t1246-pack`; no new prediction or carrier execution was performed. No REA or native carrier was run.
- No LSP device was available: `read xd://lsp` returned “No such tool” and listed the mounted tools. No LSP status/references/definition/diagnostics query or source grep was performed; this task's conclusion is based on the bound artifact digest and exact comparator result, not semantic source analysis.
- No installs or production edits were made. The only write is this assigned report.
