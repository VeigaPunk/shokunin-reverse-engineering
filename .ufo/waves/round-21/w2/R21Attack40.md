# R21Attack40 — C2 retrospective compatibility: `t1246-doc`

## Finding by severity

**No actionable finding for the assigned frozen case.** The added R21 comparator returned a bounded null/null `failure_match` for `t1246-doc`, consistent with the frozen prediction, after the exact retained log digest matched its R20 binding. This is one retrospective compatibility result only; it does not establish the full nineteen-result population or overall analyzer success.

## Frozen contract and observed run

- Frozen `.ufo/waves/round-21/claims.json:9` defines C2 as distinguishing absent/malformed observations from bounded observed silence while preserving the frozen nineteen exact-artifact matches. This review is limited to the assigned retained label `t1246-doc`.
- `.ufo/waves/round-20/runs/t1246-doc/comparison-log-binding.json` names `logs/rea-ghidra-wQaOa9/ghidra.log`, records SHA-256 `e6d79231c2e91399a3347feeec7ca932d3e71629b60961c96e70071f6ffead18`, and says `verified: true`. The frozen prediction `.ufo/waves/round-20/predictions/swiss-misread-v2/t1246-doc.json` has `first_failure.h1: null` (and `h0: null`).
- Exact bound-log hash invocation:

```text
argv: sha256sum -- /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-doc/logs/rea-ghidra-wQaOa9/ghidra.log
stdout: e6d79231c2e91399a3347feeec7ca932d3e71629b60961c96e70071f6ffead18  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-doc/logs/rea-ghidra-wQaOa9/ghidra.log
stderr: empty
exit: 0
```

  The computed digest equals the binding. The same log was counted as 183 lines / 19216 bytes (`wc -lc`); the comparator envelope reported `last_line: 183`.
- R21 `.ufo/waves/round-21/tools/compare-first-failure.py` requires `first_failure.h1`, validates a non-null failure's required fields/types, requires an extractor envelope with `first_failure` and a nonnegative integer `last_line`, and compares only kind/index (or both-null). The bound R20 extractor was explicitly passed. The R21 regression caller in `.ufo/waves/round-21/battery.py:118-136` likewise selects the R21 comparator, materializes the original R20 extractor and checks each retained log digest against its binding.
- Runtime: Python 3.14.8; working directory `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. The exact comparator command was invoked once for the initial result and repeated once to capture stdout/stderr separately; both returned the same result. Captured invocation argv:

```text
["python3", "-I", "-B", ".ufo/waves/round-21/tools/compare-first-failure.py", "--prediction", ".ufo/waves/round-20/predictions/swiss-misread-v2/t1246-doc.json", "--log", ".ufo/waves/round-20/runs/t1246-doc/logs/rea-ghidra-wQaOa9/ghidra.log", "--extractor", ".ufo/waves/round-20/tools/first-failure-extract.py"]
```

```text
stdout: {"finding": "failure_match", "last_line": 183, "match": true, "observed": null, "predicted": null}\n
stderr: empty
exit: 0
```

The extractor's observed null is bounded through line 183, covering this log's full reported line count; it matches the prediction's `h1: null` under the declared equality. The result is limited to qualifying first-failure comparison. The comparator's own docstring says null is not successful analysis, and the retained log includes three `GoTypeManager` WARN records at lines 130–132; these warnings are not cleared or adjudicated by a null/null match. In particular, the log's “Analysis succeeded” line does not upgrade this comparator result into a claim of globally clean analysis.

## Residual risk and verification gaps

- Only this one R20 label was run. The other eighteen retained artifacts, the C2 malformed/asymmetric-null/kind/index controls, the full C2 battery, and comparator selftest were not run under this assignment; no nineteen-of-nineteen claim is made.
- The LSP device is unavailable: `read xd://lsp` returned “No such tool.” Literal search located R21 battery/selftest references only; it is not semantic proof. Relevant regression caller wiring was read directly in `battery.py` as cited above; no LSP references/definition/diagnostics were available.
- No REA producer or native carrier was run. No tools were installed or updated. No production file was changed; only this scoped report was written.

Report: `.ufo/waves/round-21/w2/R21Attack40.md`
