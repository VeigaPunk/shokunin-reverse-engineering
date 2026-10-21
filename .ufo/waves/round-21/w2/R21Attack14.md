# R21Attack14 — C2 `kind_index_positive`

**Axis:** depth (C2)  
**Finding:** No actionable defect observed in this scoped case.

## Frozen case and contract

The frozen case `fixtures/battery.json` (`C2`, `kind_index_positive`) predicts `first_failure.h1` with `kind="invalid_index"`, `index=9`, `va=null`, and `phase="analysis"`. Its inert extractor observation is `first_failure={kind:"invalid_index", index:9, va:10, phase:"different"}` with `last_line=8` and extractor exit 0. The independent frozen `fixture-contract.json` declares expected exit **0** for this case: same non-null kind/index match even when typed phase/va differ.

## One-case successor CLI run

Executed only `kind_index_positive` through the actual `tools/compare-first-failure.py` CLI. The temporary prediction, inert log, and inert extractor were under `/tmp/kaidoku-r21-attack14-ekdcztgr/`; the extractor printed only the frozen fixture observation, did not access or execute an analyzed carrier, and exited 0. The temporary directory was removed after the invocation.

Exact argv:

```text
["python3", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/compare-first-failure.py", "--prediction", "/tmp/kaidoku-r21-attack14-ekdcztgr/prediction.json", "--log", "/tmp/kaidoku-r21-attack14-ekdcztgr/inert-log.txt", "--extractor", "/tmp/kaidoku-r21-attack14-ekdcztgr/inert-extractor.py"]
```

Exact stdout:

```text
{"finding": "failure_match", "last_line": 8, "match": true, "observed": {"index": 9, "kind": "invalid_index", "phase": "different", "va": 10}, "predicted": {"index": 9, "kind": "invalid_index", "phase": "analysis", "va": null}}
```

Exact stderr: empty.  
Observed exit: **0**.  
Expected exit (frozen contract): **0**.  
Result: pass for this case.

This result agrees with the comparator's `evaluate()` equality predicate (`tools/compare-first-failure.py`, line 71), which compares non-null failures by `(kind, index)` after validating their typed shape and the explicit observation envelope. It establishes only this positive case, not the complete C2 claim.

## Nearby counterexample — unrun

Change only the observed `index` from 9 to 10 while retaining `kind="invalid_index"` and a valid phase/va shape and bounded envelope. This should be a mismatch (exit 1), corresponding to frozen contract case `index_mismatch_equal_kind`. **Unrun**; no result is claimed.

## Residual risk and verification gaps

Only this one frozen positive case was exercised. No negative or malformed C2 cases, C2 regression set, C1 behavior, caller coverage, or provider/carrier execution was tested. No LSP device is exposed in the available tool inventory, so references/definition/diagnostics checks were not performed; this report makes no semantic caller-coverage claim.
