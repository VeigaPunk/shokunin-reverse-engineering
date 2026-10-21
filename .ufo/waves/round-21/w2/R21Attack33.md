# R21-C2 retrospective: `t1246-addr2line`

**Axis:** C2 depth; this is an exact-artifact retrospective, not a fresh forecast. Frozen R21 C2 requires retaining the frozen R20 exact-artifact matches. This report establishes only the assigned label's result, not the full nineteen-label count.

## Artifact and prediction

- Binding: `.ufo/waves/round-20/runs/t1246-addr2line/comparison-log-binding.json` (`verified: true`). Bound log: `.ufo/waves/round-20/runs/t1246-addr2line/logs/rea-ghidra-P9tyVR/ghidra.log`.
- Bound SHA-256: `a64551ddd4a2e7a01710162e1b5871605f85b695098f270d8c64f101ffbb4303`; it exactly matches the binding's `log_sha256`.
- Frozen prediction: `.ufo/waves/round-20/predictions/swiss-misread-v2/t1246-addr2line.json`. `first_failure.h1` predicts `kind=invalid_index`, `index=22078465`, `phase=markup_walk`, `va=5318176`.

## Exact-artifact result

The original R20 extractor reports a Go-analysis `invalid_index` at index `22078465` (first failure line 112, cause line 186), with `last_line=239`. R21 comparison returns `failure_match`, `match=true`, exit 0. Its contract compares only `(kind,index)`: observed phase `markup` and `va=null` differ from the forecast's `markup_walk` and `5318176` but do not alter this match. This is one retained R20 match, not a claim about the other labels or whole analysis success.

The extractor returned `other_errors: []`. Regardless, unrelated analyzer diagnostics do not establish success; this observation only classifies the first qualifying Go failure in the log through line 239. The log itself records `Go analysis failure` on line 112. No REA or native carrier was run; no production files were changed.

## Captured verification

All stdout/stderr below are the captured process streams; stderr was empty for each command.

1. Bound-log digest

   - argv: `["sha256sum", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-addr2line/logs/rea-ghidra-P9tyVR/ghidra.log"]`
   - stdout: `a64551ddd4a2e7a01710162e1b5871605f85b695098f270d8c64f101ffbb4303  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-addr2line/logs/rea-ghidra-P9tyVR/ghidra.log\n`
   - stderr: empty; exit: `0`.

2. Original R20 extractor on the bound log

   - argv: `["python3", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/first-failure-extract.py", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-addr2line/logs/rea-ghidra-P9tyVR/ghidra.log"]`
   - stdout:

     ```json
     {
       "cause_line": 186,
       "first_failure": {
         "index": 22078465,
         "kind": "invalid_index",
         "phase": "markup",
         "va": null
       },
       "first_failure_line": 112,
       "last_line": 239,
       "log_path": "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-addr2line/logs/rea-ghidra-P9tyVR/ghidra.log",
       "other_errors": []
     }
     ```

   - stderr: empty; exit: `0`.

3. R21 comparator with frozen prediction, bound log, and original extractor

   - argv: `["python3", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/compare-first-failure.py", "--prediction", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/predictions/swiss-misread-v2/t1246-addr2line.json", "--log", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-addr2line/logs/rea-ghidra-P9tyVR/ghidra.log", "--extractor", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/first-failure-extract.py"]`
   - stdout: `{"finding": "failure_match", "last_line": 239, "match": true, "observed": {"index": 22078465, "kind": "invalid_index", "phase": "markup", "va": null}, "predicted": {"index": 22078465, "kind": "invalid_index", "phase": "markup_walk", "va": 5318176}}\n`
   - stderr: empty; exit: `0`.

4. Inert self-tests of the two assigned Python tools

   - Extractor argv: `["python3", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/first-failure-extract.py", "--selftest"]`; stdout: `SELFTEST: CLEAN cases=4\n`; stderr: empty; exit: `0`.
   - Comparator argv: `["python3", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/compare-first-failure.py", "--selftest"]`; stdout: `{"cases": [{"exit": 0, "finding": "failure_match", "id": "bounded_null", "ok": true}, {"exit": 0, "finding": "failure_match", "id": "nullable_eof", "ok": true}, {"exit": 1, "finding": "failure_mismatch", "id": "predicted_null", "ok": true}, {"exit": 1, "finding": "failure_mismatch", "id": "observed_null", "ok": true}, {"exit": 1, "finding": "failure_mismatch", "id": "kind_diff", "ok": true}, {"exit": 2, "finding": "comparison_unevaluable", "id": "naked_null", "ok": true}, {"exit": 2, "finding": "comparison_unevaluable", "id": "missing_bound", "ok": true}, {"exit": 2, "finding": "comparison_unevaluable", "id": "boolean_bound", "ok": true}, {"exit": 2, "finding": "comparison_unevaluable", "id": "missing_index", "ok": true}], "finding": "selftest_clean"}\n`; stderr: empty; exit: `0`.

Report: `.ufo/waves/round-21/w2/R21Attack33.md`
