# R21Attack31 — R21-C2 `malformed_extractor_json`

## Finding

No actionable defect observed in this one targeted case. The successor returned the frozen unevaluable result: **expected exit 2, observed exit 2**. This is evidence for this case only, not a claim about the full C2 claim or battery.

## Frozen basis

- `kaidoku-shokunin/.ufo/waves/round-21/fixtures/battery.json:339-347` freezes `prediction.first_failure.h1: null`, extractor stdout `{`, extractor exit `0`, and expected exit `2`.
- `kaidoku-shokunin/.ufo/waves/round-21/fixture-contract.json:38` independently specifies expected exit `2` because a decode failure is unevaluable. The expected result was taken from the contract, not inferred from implementation behavior.

## Single-case execution record

Ran the actual successor CLI once, using an external `TemporaryDirectory` under `/tmp`, an empty synthetic log, the frozen null prediction, and an inert extractor stub containing `print('{', end='')`. The CLI invoked the stub, which emitted malformed JSON and exited successfully; no analyzed carrier or provider was executed or contacted. The temporary directory was removed; a subsequent `test ! -e` check printed `scratch_absent=1`.

Exact successor argv:

```json
["/usr/bin/python", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/compare-first-failure.py", "--prediction", "/tmp/r21-attack31-malformed-json-ws13rj3e/prediction.json", "--log", "/tmp/r21-attack31-malformed-json-ws13rj3e/synthetic.log", "--extractor", "/tmp/r21-attack31-malformed-json-ws13rj3e/extractor_stub.py"]
```

Exact successor stdout (one trailing newline):

```text
{"error": "Expecting property name enclosed in double quotes: line 1 column 2 (char 1)", "finding": "comparison_unevaluable", "match": null, "observed": null, "predicted": null}
```

Stderr: empty (0 bytes). Observed exit: `2`. Frozen expected exit: `2`.

## Nearby counterexample (unrun)

`extractor_nonzero` (`battery.json:350-358`; `fixture-contract.json:39`) is the adjacent frozen counterexample: valid envelope-looking stdout but extractor exit `7`; contract expected exit `2` because failed extraction is not an observation. It was not exercised, per the one-case assignment.

## Residual risk and verification gaps

- Scope was only `malformed_extractor_json`; no battery, selftest, build, or broader C2 regression was run. C1/calibration behavior was not tested.
- No LSP device is mounted: the initial `read xd://lsp` returned `No such tool: xd://lsp`. Therefore LSP status, references, definition, and diagnostics were unavailable; no text-search result is presented as semantic proof.
- No tools were installed or updated. No production files or fixtures were changed.
