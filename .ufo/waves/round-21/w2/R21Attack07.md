# R21-C1 `could_not_evaluate`

**Axis:** calibration (C1). Depth/C2 was not measured.

## Frozen expectation

The target fixture is `could_not_evaluate` (`.ufo/waves/round-21/fixtures/battery.json:47-51`): a matching `evidence_id` and `inspect_wasm_artifact` operation with `status: could_not_evaluate`; the fixture declares expected exit **1**. The independent contract also declares expected exit **1**, requiring a matching record with typed `could_not_evaluate` status/error (`.ufo/waves/round-21/fixture-contract.json:12`). The frozen-input manifest (`fixtures/expected.json:3-5`) pins both files, and observed SHA-256 values matched:

- `fixture-contract.json`: `04f54077f09bd68f9314f2c9b9febf10cb4b0434990dee51ea797fda9aa700f6`
- `fixtures/battery.json`: `2ff59eb249f0535ec3ff840d0c10f9fbf6fcf41b952bbe1bde4874e62fb752ba`

The relevant successor CLI is `tools/verb-coverage.py`: refusal detection includes `could_not_evaluate`, and a matching refused record returns `evidence_refused` with exit 1 (`tools/verb-coverage.py:16-20,39-55,87-101,168-189`).

## Single-case execution

I copied the fixture's Evidence JSON to an external temporary file and invoked the successor CLI directly; I did not run the battery. The external directory also contained an inert C2 extractor guard (`exit 97`), which was not passed to or invoked by this C1 CLI.

**Producing argv:**

```text
/usr/bin/python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/verb-coverage.py --evidence /tmp/kaidoku-r21-R21Attack07.Jm0b4e/evidence.json --verb inspect-wasm-artifact --evidence-id ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

The input file contained:

```json
{"evidence_id": "ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "operation": "inspect_wasm_artifact", "status": "could_not_evaluate"}
```

- **Expected exit:** `1`
- **Observed exit:** `1`
- **stdout:** `{"bound": false, "finding": "evidence_refused"}\n`
- **stderr:** empty
- **Result:** observed exit matches the independently frozen contract.

The scratch directory was removed; a subsequent existence check confirmed it was absent. No extractor, carrier, provider, REA producer, C2 comparator, or other fixture was run.

## Nearby counterexample (UNRUN)

Suggested adjacent follow-up: `error_envelope` (`fixtures/battery.json:53-58`) keeps the matching ID and operation inside an error envelope. Its contract expects exit **1** and requires rejection of that refusal envelope (`fixture-contract.json:13`). It was not executed for this assignment.

## Findings, residual risk, and verification gaps

- **Actionable findings:** none observed for this one C1 case.
- **Residual risk:** this single matching-refusal case does not establish broader C1 calibration, positive-control retention, or cryptographic Evidence authenticity; it says nothing about C2 depth.
- **LSP gap:** `read xd://lsp` returned “No such tool,” so no LSP status, references, definition, or diagnostics were available. This run was limited to the assigned direct CLI case, not a semantic caller audit. No tools were installed or updated.

Report: `.ufo/waves/round-21/w2/R21Attack07.md`
