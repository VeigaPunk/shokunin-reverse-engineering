# C1 operation/id record-binding review

## Scope and result

Reviewed only the requested Round-20 tool sections: `.ufo/waves/round-20/tools/verb-coverage.py`, `compare-first-failure.py`, and `first-failure-extract.py`, with the retained C2 measurement/mutation notes and the frozen Round-21 fixture contract. **One baseline defect is present**: `verb-coverage.py` can bind an evidence ID to the requested operation when both merely occur somewhere in the same cited evidence file, even if they belong to different Evidence records. This is a record-association false accept, not Evidence authentication. I found no second operation/id-binding defect in the first-failure comparator or extractor; they compare forecast failure objects with extracted log results and do not bind Evidence IDs to operations.

## Concrete defect

In `verb-coverage.py:136-165`, `bound_evidence()` extracts IDs from the knowledge-entry text (`:149`), finds retained paths containing each ID (`:150-160`), then accepts if every operation token occurs anywhere in the entire decoded file and no refusal token occurs anywhere in it (`:162-164`). It never parses or associates an ID and operation within one record. Thus this cited file is sufficient to falsely count `compare-wasm-interfaces` as exercised:

```json
{"evidence_id":"ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","operation":"inspect_wasm_artifact","exit_code":0}
{"evidence_id":"ev_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","operation":"compare_wasm_interfaces","exit_code":0}
```

If the knowledge entry cites the first ID and this file, the first ID is found in the blob and the requested operation token is also found in the blob. The `all(t in blob for t in tokens)` check therefore passes despite the cited ID belonging only to the inspection record. For the objdump special case, `OP_TOKENS` at `:120-123` requires the cooccurrence of `inspect_with_objdump` and the string `"architectures"`, but has the same file-wide rather than record-wide association; a `disassemble` record plus unrelated `architectures` text can meet it.

This is narrower than saying the current retained R20 results are all wrong: the R20 measurement reports its selected C2 targets exercised (`.ufo/waves/round-20/verify/round20/verb-coverage.json`, target records), and those observations do not by themselves demonstrate split-record binding. The defect is the acceptance predicate's false-positive path. The retained mutation report independently records that the shipped coverage selftest missed operation-binding negatives: `.ufo/waves/round-20/w2/MutateGuardsAndLint.md:35,44-45` says the operation-removal mutant survived and its forged-ID test could not catch removal of an operation conjunct. Do not count that test gap as a second defect.

`compare-first-failure.py:28-35,50-78` validates and compares predicted/observed `kind` and `index` and unwraps the extractor's result; `first-failure-extract.py:134-196` emits parsed log failure details and a bounded `last_line`. Neither handles Evidence IDs or operation fields, so neither is implicated in this C1 defect. Their separate C2 observation-envelope issues are outside this review.

## Independent positive/negative fixture proposal

Use a new scratch Git fixture repository with one knowledge entry naming `compare-wasm-interfaces`, citing one full `ev_…` ID and the same evidence path. Keep the evidence file byte-identical between two cases except for record arrangement/identity:

- **Positive control:** one successful supported record contains both `evidence_id: ev_a…` and `operation: compare_wasm_interfaces`. Expected: target `exercised=true`, with `(ev_a…, path)` in `bound_evidence`; fixture assertion passes.
- **Negative control (`split_records`):** record 1 is successful `inspect_wasm_artifact` with `evidence_id: ev_a…`; record 2 is successful `compare_wasm_interfaces` with a different ID. The knowledge entry cites only `ev_a…`. Expected: `exercised=false`, no bound pair; fixture assertion passes. Under the current predicate this negative is falsely accepted because the ID and operation tokens cooccur in the file.

The frozen contract already specifies the same boundary as C1 `same_record_positive` (expected exit 0) and `split_records` (expected exit 1); retain those denominator cases, rather than adding another counted case. For the tool's API, a normal measurement invocation returns exit 0 even when a target is not exercised (`verb-coverage.py:323-347`), so assert the `exercised`/`bound_evidence` fields in the fixture harness; the harness should return exit 0 when both controls match expectations and exit 1 if either assertion fails. No `verb-coverage.py --selftest` or other check was run here.

## Verification and limitations

- Read the named production source sections and retained R20 mutation/measurement records; no checks, tests, builds, or runtimes were executed.
- Attempted to discover/use the LSP device first (`read xd://lsp`); the mounted-device response reported no such tool. No LSP status/references/definition/diagnostics server was available, so this is a direct source-and-retained-evidence review, not LSP semantic proof. Literal grep was used only to locate the retained review note after confirming the device was unavailable; the finding above is grounded in the cited source lines.
- Parent should run the changed-path C1 battery/selftest against the frozen `same_record_positive` and `split_records` cases and confirm the existing R20 regression records remain unchanged. I did not run them.
- No tools were installed or updated.
Report: `.ufo/waves/round-21/w1/C1OperationRecord.md`
