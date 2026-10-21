# R21Attack45 — t1246-objdump retrospective compatibility

## Axes
- **Calibration:** exact retained-log identity and faithfully recorded run result.
- **Depth:** whether the R21 comparator accepts the R20 first-failure extractor's result for the frozen R20 prediction, without treating other analyzer errors as success.

## Finding
**No actionable mismatch found for this retained artifact.** The R21 comparator returned `failure_match` (exit 0) for the bound R20 log and frozen prediction. This establishes only the comparator's first-failure kind/index match; it does not establish successful overall Ghidra analysis.

## Artifact identity
- Binding: `.ufo/waves/round-20/runs/t1246-objdump/comparison-log-binding.json`; `verified: true`.
- Bound log: `.ufo/waves/round-20/runs/t1246-objdump/logs/rea-ghidra-uLjgCv/ghidra.log`.
- Binding SHA-256: `7e3e965e5f73a03049c0f3f46d9cfa78ec0dd5aa5da750d7a07ff14d7b2e9073`.
- Observed `sha256sum` of that path: `7e3e965e5f73a03049c0f3f46d9cfa78ec0dd5aa5da750d7a07ff14d7b2e9073` (match); size 38,376 bytes.
- Frozen prediction: `.ufo/waves/round-20/predictions/swiss-misread-v2/t1246-objdump.json`; label `t1246-objdump`; `first_failure.h1` predicts `kind=invalid_index`, `index=13816064`, `phase=markup_walk`, `va=6205248`.

## Assigned comparison run
Working directory: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`

Exact argv:
```text
python3 .ufo/waves/round-21/tools/compare-first-failure.py --prediction .ufo/waves/round-20/predictions/swiss-misread-v2/t1246-objdump.json --log .ufo/waves/round-20/runs/t1246-objdump/logs/rea-ghidra-uLjgCv/ghidra.log --extractor .ufo/waves/round-20/tools/first-failure-extract.py
```

Stdout:
```json
{"finding": "failure_match", "last_line": 411, "match": true, "observed": {"index": 13816064, "kind": "invalid_index", "phase": "markup", "va": null}, "predicted": {"index": 13816064, "kind": "invalid_index", "phase": "markup_walk", "va": 6205248}}
```

Stderr: empty. Exit: `0`.

The observed failure is corroborated in the retained log: first qualifying record at line 122 (`GolangSymbolAnalyzer` Go analysis failure), with cause at line 196 (`java.io.EOFException: Invalid index: 13816064`). Extractor envelope is bounded through `last_line: 411`.

## Comparator scope and residual risk
The comparator source explicitly defines a match by equality of `(kind, index)` only. Thus `invalid_index` and `13816064` match, while phase (`markup` vs `markup_walk`) and VA (`null` vs `6205248`) are returned for inspection but are **not** compared. The result is a valid match under this tool's contract, not equivalence of every prediction field. The null case is bounded by the extractor's `last_line`; null means no qualifying failure through that line, not successful analysis.

The extractor also returned these `other_errors`, which do not establish the predicted first failure and do not turn the matching first-failure result into an overall analysis-success claim: VarnodeContext address-space errors at lines 214–215; X86Analyzer Java heap OOM at 216; Timer-already-cancelled errors at 249, 284, 317, and 382; and HeadlessAnalyzer's import-failed report at 411. The targeted first failure remains the earlier invalid-index at line 122 / cause line 196.

## Additional recorded runs
- Comparator selftest argv: `python3 .ufo/waves/round-21/tools/compare-first-failure.py --selftest` (same working directory). Stdout: `{"cases": [{"exit": 0, "finding": "failure_match", "id": "bounded_null", "ok": true}, {"exit": 0, "finding": "failure_match", "id": "nullable_eof", "ok": true}, {"exit": 1, "finding": "failure_mismatch", "id": "predicted_null", "ok": true}, {"exit": 1, "finding": "failure_mismatch", "id": "observed_null", "ok": true}, {"exit": 1, "finding": "failure_mismatch", "id": "kind_diff", "ok": true}, {"exit": 2, "finding": "comparison_unevaluable", "id": "naked_null", "ok": true}, {"exit": 2, "finding": "comparison_unevaluable", "id": "missing_bound", "ok": true}, {"exit": 2, "finding": "comparison_unevaluable", "id": "boolean_bound", "ok": true}, {"exit": 2, "finding": "comparison_unevaluable", "id": "missing_index", "ok": true}], "finding": "selftest_clean"}`. Stderr empty; exit `0`.
- Direct extractor cross-check, correct positional form argv: `python3 .ufo/waves/round-20/tools/first-failure-extract.py .ufo/waves/round-20/runs/t1246-objdump/logs/rea-ghidra-uLjgCv/ghidra.log`. Stdout reported `first_failure={kind: invalid_index, index: 13816064, phase: markup, va: null}`, `first_failure_line=122`, `cause_line=196`, `last_line=411`, and the `other_errors` listed above. Stderr empty; exit `0`.
- A preliminary direct-extractor invocation used unsupported `--log` syntax: `python3 .ufo/waves/round-20/tools/first-failure-extract.py --log .ufo/waves/round-20/runs/t1246-objdump/logs/rea-ghidra-uLjgCv/ghidra.log`. Stdout empty; stderr: `usage: first-failure-extract.py [-h] [--selftest] [log]` and `first-failure-extract.py: error: unrecognized arguments: --log`; exit `2`. Corrected by using the positional form above.

No REA or native carrier was run. No production files were changed; this report is the only write.

Report: `.ufo/waves/round-21/w2/R21Attack45.md`