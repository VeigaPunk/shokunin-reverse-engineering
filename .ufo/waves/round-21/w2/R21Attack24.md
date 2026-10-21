# R21-C2 `negative_last_line`

## Axes
- **Calibration:** compare the observed exit with the independently frozen C2 contract.
- **Depth:** determine whether a negative observation bound is rejected rather than treated as bounded silence.

## Findings by severity
- **No actionable finding in this assigned case.** The frozen contract (`.ufo/waves/round-21/fixture-contract.json`, C2 `negative_last_line`) declares exit **2** because `last_line` cannot be negative. The selected row in `.ufo/waves/round-21/fixtures/battery.json` supplies prediction `{"first_failure":{"h1":null}}`, extractor stdout `{"first_failure": null, "last_line": -1}`, and extractor exit 0. The expected exit here is taken from the frozen contract, not inferred from the successor.

Ran only that case through the actual successor, `.ufo/waves/round-21/tools/compare-first-failure.py`, with a temporary inert extractor stub emitting the row's frozen stdout. The stub did not execute an analyzed carrier; the log input was empty and unused by the stub.

**Actual CLI argv:**
```text
["/usr/bin/python", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/compare-first-failure.py", "--prediction", "/tmp/kaidoku-r21-negative-last-line-hts6s6nv/prediction.json", "--log", "/tmp/kaidoku-r21-negative-last-line-hts6s6nv/log.json", "--extractor", "/tmp/kaidoku-r21-negative-last-line-hts6s6nv/inert_extractor.py"]
```

**Observed stdout:**
```text
{"error": "invalid_last_line", "finding": "comparison_unevaluable", "match": null, "observed": null, "predicted": null}
```
**Observed stderr:** empty (`""`).  **Observed exit:** 2.  **Frozen expected exit:** 2.

The CLI reports an unevaluable comparison with `invalid_last_line`, matching the frozen rejection of this malformed bound. The external scratch directory `/tmp/kaidoku-r21-negative-last-line-hts6s6nv` was removed; its post-run existence check was false. No tools were installed or updated.

## Nearby counterexample (unrun)
`boolean_last_line` is the adjacent fixture row. Its `last_line: true` should remain unevaluable with exit 2 under the contract rule that a bool is not a line count. **Unrun**; no result is claimed.

## Residual risk and verification gaps
This observation covers only `negative_last_line`. It does not establish behavior for other malformed observations, valid matches/mismatches, the retained R20 pairs, or the complete C2 claim. No whole-battery run, carrier execution, or provider call was performed.
