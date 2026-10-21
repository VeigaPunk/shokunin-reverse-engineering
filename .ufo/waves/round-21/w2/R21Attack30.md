# R21-C2 `missing_phase` attack result

## Frozen oracle

- `.ufo/waves/round-21/fixtures/battery.json`, C2 `missing_phase`: `expected_exit: 2`; prediction H1 is `{kind: invalid_index, index: 9, va: null, phase: analysis}`; the frozen extractor output has the same kind/index but omits `phase`; `extractor_exit: 0`.
- `.ufo/waves/round-21/fixture-contract.json`, C2 `missing_phase`: expected exit `2`, rule: “failure shape must retain typed phase even though equality ignores it.” This independently frozen contract, not the implementation, supplies the expected result.

## One-case execution

Executed only the successor CLI `.ufo/waves/round-21/tools/compare-first-failure.py`, with an inert Python extractor stub in `/tmp`. The stub emitted the exact frozen `stdout` string and ignored its placeholder log; no carrier or provider was run. The temporary directory was removed after execution.

Actual argv:

```json
["/usr/bin/python", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/compare-first-failure.py", "--prediction", "/tmp/r21-missing-phase-0xqt32ha/prediction.json", "--log", "/tmp/r21-missing-phase-0xqt32ha/input.log", "--extractor", "/tmp/r21-missing-phase-0xqt32ha/extractor.py"]
```

Observed extractor `sys.argv`:

```json
["/tmp/r21-missing-phase-0xqt32ha/extractor.py", "/tmp/r21-missing-phase-0xqt32ha/input.log"]
```

Observed exit: `2` (expected `2`).

Stdout:

```text
{"error": "observation: missing_phase", "finding": "comparison_unevaluable", "match": null, "observed": {"index": 9, "kind": "invalid_index", "va": null}, "predicted": {"index": 9, "kind": "invalid_index", "phase": "analysis", "va": null}}
```

Stderr: empty.

The observed result is consistent with the frozen oracle: the missing typed `phase` makes this observation unevaluable, rather than a match based on kind/index alone. The report retains the actual invocation, streams, and status; `/tmp/r21-missing-phase-0xqt32ha` was confirmed removed.

## Nearby counterexample (unrun)

Keep the same prediction and observation, but supply `phase: null` instead of omitting `phase`. This is an unrun proposal; the contract requires a typed phase, so null should remain unevaluable rather than being accepted as a string.

## Residual risk and verification gaps

This was the single assigned frozen case, not the C2 battery or a real extraction. The inert stub isolates comparator behavior but does not validate extractor fidelity or carrier behavior. No production files or fixtures were changed; no builds or broad tests were run. No LSP endpoint was exposed in the available session tools, so no LSP references/definition/diagnostics were requested.

Report: `.ufo/waves/round-21/w2/R21Attack30.md`
