# R21Attack04 — C1 `operation_in_notes`

Axes: **calibration** (tested); **depth** (not tested).

## Frozen case and independent expectation

`fixtures/battery.json` C1 case `operation_in_notes` supplies evidence with `evidence_id` `ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`, record `operation: inspect_artifact`, decoy `notes: inspect_wasm_artifact`, requested verb `inspect-wasm-artifact`, and the same cited ID. The independently frozen `fixture-contract.json` C1 row says expected exit **1**: the requested operation appears only as prose/metadata while the record operation differs. I used that contract row, not the implementation, for the expected result.

## One-case execution

Ran the actual successor CLI, `.ufo/waves/round-21/tools/verb-coverage.py`, with only this case's evidence serialized to a temporary file under `/tmp`; the temporary directory was removed after execution.

- `argv`: `["/usr/bin/python", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/verb-coverage.py", "--evidence", "/tmp/kaidoku-r21-operation-in-notes-bsrul_oa/evidence.json", "--verb", "inspect-wasm-artifact", "--evidence-id", "ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"]`
- stdout: `{"bound": false, "finding": "evidence_unbound"}\n`
- stderr: empty
- expected exit: **1**
- observed exit: **1**
- temp cleanup: confirmed removed after the run

**Result:** this single frozen negative calibrated as expected: prose co-occurrence did not bind the record to the requested operation. This is only local record binding, not cryptographic authentication. No carrier or provider was executed/called; no C2 case, extractor, or battery run was performed (therefore no C2 extractor stub was needed for this C1 CLI case).

## Nearby counterexample — unrun

Try a record with the same ID and `operation: inspect_artifact`, but place `inspect_wasm_artifact` under a separate ordinary `metadata` object rather than the `notes` string. This is unrun; it would check that metadata decoys remain non-authoritative without expanding this assignment beyond the one frozen case.

## Verification limits

Only `operation_in_notes` was exercised. No positive controls, other C1 cases, C2 cases, broad suites, builds, or provider/native analysis were run. No tools were installed or updated.
