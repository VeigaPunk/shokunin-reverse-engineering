# R21-C1 `same_record_positive`

**Axis:** calibration (C1). Depth/C2 was not measured.

## Frozen contract

The fixture labels `same_record_positive` with `expected_exit: 0` and supplies the exact evidence record, verb, and cited ID (`.ufo/waves/round-21/fixtures/battery.json:5-9`). The independently authored contract also sets expected exit **0** and requires the cited exact ID and exact operation in one successful supported Evidence record (`.ufo/waves/round-21/fixture-contract.json:6`). The fixture and contract SHA-256 values matched the frozen manifest in `fixtures/expected.json:3-5`:

- `fixture-contract.json`: `04f54077f09bd68f9314f2c9b9febf10cb4b0434990dee51ea797fda9aa700f6`
- `fixtures/battery.json`: `2ff59eb249f0535ec3ff840d0c10f9fbf6fcf41b952bbe1bde4874e62fb752ba`

## Single-case execution

The relevant successor is `tools/verb-coverage.py`; its C1 CLI accepts `--evidence`, `--verb`, and `--evidence-id`. I copied the fixture's inner evidence string verbatim to an external temporary file and invoked that CLI directly, not the full battery.

**Producing argv:**

```text
/usr/bin/python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/verb-coverage.py --evidence /tmp/kaidoku-r21-R21Attack01.IgQ107/evidence.json --verb inspect-wasm-artifact --evidence-id ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

**Expected exit:** `0` (fixture and contract above)  
**Observed exit:** `0`  
**stdout:** `{"bound": true, "finding": "evidence_bound", "pathless": false}\n`  
**stderr:** empty

Result: the single positive case matched its frozen expected exit. An inert C2 extractor stub was present in the same external scratch directory as a containment guard, but was **not invoked**: this C1 successor has no extractor argument. No C2 case or other fixture was executed. The temporary directory was removed after the run.

## Nearby counterexample (UNRUN)

The frozen `split_records` C1 case is a nearby negative: the cited `ev_aaaa…` record has `operation: inspect_artifact`, while `inspect_wasm_artifact` appears only in a distinct record under `ev_bbbb…` (`fixtures/battery.json:19-23`). Its frozen contract expectation is exit **1** (`fixture-contract.json:8`). It was not executed in this assignment.

## Limits and gaps

This is one local record-binding positive only; it does not establish refusal handling, negative-case calibration, broader coverage, or cryptographic Evidence authenticity. No carrier, provider, REA producer, C2 comparator, or extractor was run. LSP discovery (`read xd://lsp`) returned “No such tool”; no LSP status/references/definition/diagnostics were available. No tools were installed or updated.

Report: `.ufo/waves/round-21/w2/R21Attack01.md`
