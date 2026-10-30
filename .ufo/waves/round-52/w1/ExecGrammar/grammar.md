# R52-C1 controls receipt grammar — ExecGrammar

## Input contract and exact paths

The round-50 counter's disposition input is the committed evidence envelope `after.json`, not the harness wrapper `run.json`. In each run wrapper, the evidence receipt locator is `$.receipt.path` (the value is `after.json`); the normalized result is read from the resolved envelope's `$.normalized_result`. The v2 controls mode must follow that same envelope shape when it reads the four committed round-50 carriers. The receipt references below were checked in `run.json` for each of `c6430`, `c6490`, `g7581`, and `g7582`; each points to `after.json`, has claim R50-C1, operation `extract_firmware`, and has the single `squashfs_v4_le` handler.

| Controls input | Exact JSON path(s) | Meaning |
|---|---|---|
| Published regular-file list | `$.normalized_result.files[*].relative_path`, `$.normalized_result.files[*].sha256`, `$.normalized_result.files[*].size` | The disposition check itself does not use published files; the counter's coverage checks consume these triples. |
| Extraction gaps | `$.normalized_result.extraction_gaps[*].kind`, `$.normalized_result.extraction_gaps[*].relative_path`; structural evidence additionally `$.normalized_result.extraction_gaps[*].input_path`, `$.normalized_result.extraction_gaps[*].continuation_id` | The three-family disposition clause uses kind and relative path. Null-path depth-limited gaps are structural. |
| Removal diagnostics | `$.normalized_result.diagnostics[*].report.__typename__`, `$.normalized_result.diagnostics[*].report.link`; when recording or validating the diagnostic envelope also `$.normalized_result.diagnostics[*].input_path` | A named removal diagnostic is mapped using `report.link` (inside the trusted run root), not `input_path`, which is the chunk task input. |
| Subject digest | `$.subject.digest.sha256` | Carrier subject SHA-256; the normalized `selection` also carries the selection digest. |
| Handler list | `$.normalized_result.chunks[*].handler` | The receipt's chunks provide the handlers; `$.handlers` in the wrapper is the envelope summary, while `$.receipt.handlers` in run.json is the wrapper's recorded handler list. The v2 controls data should use the normalized envelope path. |

`run.json` is a harness receipt, not a substitute for the envelope: its `$.receipt` object gives path/hash/size/evidence id and summary metadata; its `$.envelope_data_summary` is a summary, not the disposition input. Controls open the committed `after.json` envelope and pass its `normalized_result` and the frozen nonregular oracle rows to the disposition clause.

Verified per-carrier envelope facts (all four `run.json` wrappers): `$.receipt.path == "after.json"`; `$.receipt.operation == "extract_firmware"`; `$.receipt.handlers == ["squashfs_v4_le"]`; the wrappers report `receipt_written: true`. Envelope-level field paths were checked on c6430's committed envelope and the same structure is consumed by the witness for all four envelopes.

## Executable expectation witness

`disposition-witness.py` reads only the four committed `after.json` envelopes and their committed `tools/round-50/oracle/<id>.nonregular.tsv` tables. It implements the disposition families (path-resolved gaps, structural gaps, and named removals), then required-entry disposition and silent-detail admission. It compares the round-50 frozen `gap-rule.json` to the law arm (device kinds required false and no silent-detail exception); it does not invoke REA or touch vendor bytes.

Receipt: `disposition-witness.stdout` is the output of
`python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-52/w1/ExecGrammar/disposition-witness.py`
(exit 0; UTC `2026-10-30T10:48:47Z`; stdout SHA-256 `1444e90dbc24a658195cc5dbcfb283a61ff8db2b1775ada4fbaa3cf771f32ac5`). The committed stdout gives: c6430 R50 PASS/law PASS (824 nonregular rows, 568 gaps, 1 removal); c6490 R50 PASS/law PASS (914, 613, 1); g7581 R50 FAIL with 12 missing dispositions/law PASS (1001, 637, 3); g7582 R50 FAIL with 12 missing/law PASS (1001, 637, 3). This matches the claims' CTL-OLD 2/4 and CTL-NEW 4/4 expected disposition outcomes. Counts here are the witness counts; script exit zero means it completed the comparison, not that CTL-OLD is green.
