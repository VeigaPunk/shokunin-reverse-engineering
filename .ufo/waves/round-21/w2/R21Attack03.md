# R21Attack03 — `split_records`

Axes: **C1 calibration** (directly exercised); **C2 depth** (not exercised).

## Finding

**No actionable defect observed in the assigned case.** This is a one-case result, not a judgment on the whole C1 claim or round.

The frozen fixture at `fixtures/battery.json:19-23` cites ID `ev_aaaa…` from one record whose operation is `inspect_artifact`, while `inspect_wasm_artifact` belongs to the distinct record with ID `ev_bbbb…`; the requested verb is `inspect-wasm-artifact`. The independently frozen contract at `fixture-contract.json:8` declares expected exit **1** for precisely that split-record condition. The frozen-input manifest `fixtures/expected.json:4-5` matches the observed SHA-256 digests: contract `04f54077f09bd68f9314f2c9b9febf10cb4b0434990dee51ea797fda9aa700f6`; battery `2ff59eb249f0535ec3ff840d0c10f9fbf6fcf41b952bbe1bde4874e62fb752ba`.

The actual C1 successor is `tools/verb-coverage.py` (the C1 selection is also shown in `battery.py:70-75`). Its `bind` logic requires the cited ID and normalized operation on the same record and returns `evidence_unbound`, exit 1, when none matches (`verb-coverage.py:85-99`).

Executed exactly this fixture case through that CLI, using an external `/tmp` evidence file that was removed when the temporary directory closed. Actual argv:

```text
["/usr/bin/python", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/verb-coverage.py", "--evidence", "/tmp/kaidoku-r21-attack03-xysphw94/split_records-evidence.json", "--verb", "inspect-wasm-artifact", "--evidence-id", "ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"]
```

Observed stdout (exact):

```text
{"bound": false, "finding": "evidence_unbound"}
```

Observed stderr: empty. Observed exit: **1**. Fixture expected exit: **1**. Contract expected exit: **1**. The result matches both independent expectations.

The C2 extractor stub was not used: this assigned case is C1 and its actual successor CLI accepts evidence, verb, and evidence ID, not an extractor. No C2 case/tool was run, preserving the one-case scope. No analyzed carrier was executed and no provider was called.

## Nearby counterexample

`operation_in_notes` is nearby in `fixtures/battery.json:25-30`; `fixture-contract.json:9` specifies expected exit **1** when the requested operation appears only in prose/metadata and the record operation differs. **Unrun**; proposed as a separate supplementary case only.

## Residual risk and verification gaps

- Only `split_records` was exercised; no conclusion about other C1 controls, overall calibration, or C2 depth.
- The `lsp` device is unavailable in this tool session (`read xd://lsp` and a status request to `write xd://lsp` both reported “No such tool”). Therefore no LSP status/references/definition/diagnostics checks could be made; no text-grep output is relied on as semantic proof.
- Canonical-runtime, same-identity rerouting, and saturation behavior were outside this case and were not assessed.
