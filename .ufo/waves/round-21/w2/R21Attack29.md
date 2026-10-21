# R21Attack29 — C2 `string_index`

## Axes and scope

- **Depth (C2):** exercised only the frozen `string_index` case through the actual successor CLI.
- **Calibration:** no C1 predicate or C1 control was exercised; this run makes no C1 claim.
- No production or fixture files were changed. No analyzed carrier or provider was invoked.

## Findings by severity

### No actionable finding in the scoped case

The independent contract declares `string_index` exit **2**, because a string is not a failure index (`fixture-contract.json:36`). The frozen case supplies prediction index `9` as an integer and observation index `"9"` as a string (`fixtures/battery.json:307-319`). The actual successor CLI returned **2**, reporting the observation as invalid, matching the independently frozen expectation.

### Exact execution record

The external temporary directory held the fixture-derived prediction, an empty inert log placeholder, and an extractor stub that emitted the frozen case's stdout and exited with its frozen `extractor_exit` of 0. The temporary directory was removed after the run (`tempdir_removed: true`).

Actual argv:

```text
["/usr/bin/python", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/compare-first-failure.py", "--prediction", "/tmp/r21-string-index-pht8jsi7/prediction.json", "--log", "/tmp/r21-string-index-pht8jsi7/inert.log", "--extractor", "/tmp/r21-string-index-pht8jsi7/inert_extractor.py"]
```

Expected exit: `2` (frozen battery and independent contract).

Observed stdout:

```text
{"error": "observation: invalid_index", "finding": "comparison_unevaluable", "match": null, "observed": {"index": "9", "kind": "invalid_index", "phase": "analysis", "va": null}, "predicted": {"index": 9, "kind": "invalid_index", "phase": "analysis", "va": null}}
```

Observed stderr: empty.

Observed exit: `2`.

This is consistent with the successor's explicit non-`int` index rejection (`tools/compare-first-failure.py:42-45`) and its unevaluable-input exit path (`:73-74`). It demonstrates only this single fixture-driven CLI invocation, not broader C2 coverage or extractor isolation.

## Nearby counterexample — UNRUN

`boolean_index` (`fixtures/battery.json:291-304`; `fixture-contract.json:35`) keeps the predicted index as integer `9` but changes the observed index to JSON `true`; its frozen expected exit is `2`. It is a useful adjacent check that booleans are not accepted as integer failure indexes. It was **not executed** in this assignment.

## Residual risk and verification gaps

- Only `string_index` was run; no battery-wide run, retained R20 regression, other C2 case, or C1 case is covered.
- The stub reproduced fixture stdout and did not invoke an analyzed carrier. This does not establish behavior with a real extractor or carrier.
- The `lsp` route was unavailable: `read xd://lsp` returned “No such tool.” Thus no LSP status, references, definition, or diagnostics were available. After that unavailability, literal grep was used only to locate fixture line numbers, not as semantic proof.
- No installs or updates were made.

Report trailer: `.ufo/waves/round-21/w2/R21Attack29.md`
