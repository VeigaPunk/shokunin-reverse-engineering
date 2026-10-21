# R21 C2 — `extractor_nonzero`

**Axis assessed:** C2 depth. C1 calibration and all other C2 cases are out of scope.

## Scoped result

No actionable defect found in this one case. The independently frozen contract assigns `extractor_nonzero` exit 2 because failed extraction is not an observation (`fixture-contract.json:39`). The frozen case supplies prediction `{"first_failure":{"h1":null}}`, an otherwise-valid bounded-silence extractor payload, and extractor exit 7 (`fixtures/battery.json:350-358`). The actual R21 successor checks the extractor return code before decoding stdout and maps a nonzero return to `comparison_unevaluable` / exit 2 (`tools/compare-first-failure.py:60-74`).

I executed only that case through the actual successor CLI with a temporary inert extractor and inert log under `/tmp`; the temporary directory was removed after the run. The stub emitted the fixture's exact stdout (`{"first_failure": null, "last_line": 8}`), then exited 7.

**Producing argv:**
```json
["/usr/bin/python", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/compare-first-failure.py", "--prediction", "/tmp/kaidoku-r21-extractor-nonzero-sgmpj0qr/prediction.json", "--log", "/tmp/kaidoku-r21-extractor-nonzero-sgmpj0qr/log.txt", "--extractor", "/tmp/kaidoku-r21-extractor-nonzero-sgmpj0qr/extractor.py"]
```

**Observed successor stdout (exact):**
```text
{"error": "extractor_nonzero: 7", "finding": "comparison_unevaluable", "match": null, "observed": null, "predicted": null}
```
There is a trailing newline. **Observed stderr:** empty. **Observed exit:** 2. **Frozen expected exit:** 2. External temporary directory removed: yes.

## Nearby proposed counterexample — unrun

An inert extractor emits the same valid envelope but is terminated by SIGTERM before normal exit. Expected under the frozen failed-extraction rule: exit 2, not a comparison against the emitted envelope. This variant was not exercised and is not part of the frozen denominator.

## Limits and verification gaps

- This is one assigned case only: no full battery, regression, baseline run, or other case was run. No analyzed carrier or provider was executed or queried.
- LSP was unavailable: reading `xd://lsp` returned “No such tool” and listed mounted devices, so no LSP status/references/definition/diagnostics were available. Targeted source reads and the single actual CLI run provide the evidence above; literal grep was used only as a locator, not as semantic proof.
- No tools were installed or updated. No production or fixture files were edited.
