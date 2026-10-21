# R21 C2 `boolean_index` scoped attack

## Axes
- **Depth (C2):** malformed observation/failure shape must be unevaluable, not treated as a match or mismatch.
- **Contract fidelity / isolation:** use the frozen case and independent contract; exercise only the actual C2 successor with an inert extractor stub.

## Findings by severity
- **No actionable finding for this assigned case.** `boolean_index` returned the frozen expected exit code, and the observed boolean index was rejected as malformed.

## Frozen expectation and evidence
The independent `fixtures/fixture-contract.json` C2 entry for `boolean_index` declares `expected_exit: 2` and the rule “bool is not a failure index.” The frozen `fixtures/battery.json` case independently declares exit 2; its prediction has integer index `9`, while its extractor stdout has `index: true` and `last_line: 8`.

Ran only `tools/compare-first-failure.py` for that case. The temporary prediction was loaded from the frozen case; the external `/tmp` extractor stub emitted the case's frozen stdout verbatim and exited successfully. The log was inert text. No analyzed carrier was run.

Captured successor argv:

```text
["/usr/bin/python", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/compare-first-failure.py", "--prediction", "/tmp/r21-boolean-index-acxx76ay/prediction.json", "--log", "/tmp/r21-boolean-index-acxx76ay/inert.log", "--extractor", "/tmp/r21-boolean-index-acxx76ay/inert-extractor.py"]
```

Observed stdout:

```json
{"error": "observation: invalid_index", "finding": "comparison_unevaluable", "match": null, "observed": {"index": true, "kind": "invalid_index", "phase": "analysis", "va": null}, "predicted": {"index": 9, "kind": "invalid_index", "phase": "analysis", "va": null}}
```

Observed stderr: empty. Observed process exit: **2** (expected **2**). The external temporary directory was confirmed absent after the run (`test ! -e /tmp/r21-boolean-index-acxx76ay` returned `removed`).

The relevant successor code validates `index` with `type(item) is int` (`compare-first-failure.py:42-45`), so Python's `bool` subtype does not pass as an integer. Its observation-validation error is caught as `comparison_unevaluable` and mapped to exit 2 (`:69-74`, `:116-118`). This matches the frozen contract rather than deriving the expectation from implementation.

## Nearby counterexample (UNRUN)
`string_index` is the nearby frozen C2 counterexample: it keeps the same numeric prediction but returns string `"9"` as the observation index. The fixture contract expects exit 2 for that malformed index. It was read, not executed.

## Residual risk and verification gaps
- Scope was limited to the single assigned `boolean_index` CLI run; no other case, full battery, build, or suite was run.
- No LSP device is mounted in this session (`xd://lsp` returned “No such tool”), so LSP status/references/definition/diagnostics were unavailable; no grep was used as semantic proof.
- No production file or fixture was edited. No provider call, carrier execution, or tool installation occurred.
