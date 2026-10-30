# Independent offline disposition verdict

Axes: disposition correctness; receipt completeness; expectation reproducibility.

**Recommendation: retain CTL-OLD = 2/4 (semantic exit 1), CTL-NEW = 4/4 (semantic exit 0).** No disagreement with claims lines 115–125. These are computed rule-scoped verdicts, not full-counter runs or admission of the future freeze.

| Carrier | Nonregular census (dir / symlink / char) | Path-resolved gaps | Structural gaps | Removals | R50 silent chars | R50 gaps_ok | Law gaps_ok | nonregular_unpublished_ok | R50 verdict | Law verdict |
|---|---:|---:|---:|---:|---:|---|---|---|---|---|
| c6430 | 255 / 568 / 1 | 567 | 1 | 1 | 1 | true | true | true | PASS | PASS |
| c6490 | 300 / 613 / 1 | 612 | 1 | 1 | 1 | true | true | true | PASS | PASS |
| g7581 | 349 / 639 / 13 | 636 | 1 | 3 | 1 | false | true | true | FAIL | PASS |
| g7582 | 349 / 639 / 13 | 636 | 1 | 3 | 1 | false | true | true | FAIL | PASS |

Each structural gap is `depth-limited` with null `relative_path`; count 1 meets allowance 1. Each path-resolved gap maps exactly below `firmware.bin_extract` to an oracle symlink and has allowed kind `unpublished-entry`. Every named removal maps to an oracle symlink below the trusted extraction tree and does not overlap a gap. All nonregular paths are absent from published files. The law admits zero silent rows because device rows are not required.

Both FRITZ!Box receipts fail the R50 rule solely within this disposition calculation because twelve required char-device rows lack a disposition: `dev/pts/0`–`dev/pts/7`, `dev/tiatm`, `dev/ttyp0`–`dev/ttyp2`. `dev/led` detail `247:0` alone gets R50 silent admission. The law sets device required flags false, clears allowed device gap kinds and removes device silent allowances; it therefore passes every carrier without allowing a device gap. No fifo/socket/block-device rows occur in these tables.

## Source and JSON paths read

For each `<id>` in `{c6430,c6490,g7581,g7582}`:

- `corpus/evidence/round-50/c1/<id>/run.json`: `$.receipt.sha256`, `$.receipt.gaps`, `$.receipt.gaps_detail`; the SHA-256 matches the complete `after.json` bytes.
- `corpus/evidence/round-50/c1/<id>/after.json`: `$.parameters.output_directory`; `$.normalized_result.derivations[*].{handler,child_path}`; `$.normalized_result.extraction_gaps[*].{kind,relative_path}`; `$.normalized_result.diagnostics[*].report.{__typename__,link}`; `$.normalized_result.files[*].relative_path`. The canonical cross-check also reads normalized files' hashes/sizes through `published`.
- `tools/round-50/oracle/<id>.nonregular.tsv`: all relative-path/kind/detail rows.
- `tools/round-50/gap-rule.json`: `$.allowed`, `$.required`, `$.removed.{diagnostic,kinds,disposition,silent}`, `$.structural`; law model is saved in `derivation.json`.

Source: `tools/round-50/c1-counter.py:1458–1569` defines the three families and final required-row check; `:1427–1437` defines the unpublished clause. Independent row accounting in `derive.py` agrees with direct calls to the existing `disposition_check` on every carrier/rule pair. Importing the counter does not invoke its main/selftests or REA.

## Findings, residual risk and verification gaps

1. **Input-integrity caution (not a claims defect): `run.json` alone cannot establish this verdict.** Every `$.receipt.gaps_detail` has only 20 elements while `$.receipt.gaps` is 568, 613, 637, 637 respectively. The complete normalized envelopes are necessary. Claims lines 117–119 explicitly require `after.json`, NOT harness receipts, so the claims already avoid this trap. Preserve that distinction in the control driver.
2. No expectation discrepancy found: all eight independently derived outcomes match the requested CTL expectations. This does not establish full-counter projection, freshness, provenance, runtime rerouting, saturation, or resume behavior; none is in this offline assignment.
3. LSP unavailable: `read xd://lsp` reports no such mounted tool. Source was inspected textually; no semantic-reference or diagnostics proof is claimed.

Execution: exact argv, actual exit 0, stdout SHA-256 and UTC are in `execution.json`; complete output is `derivation.json`. No REA, network download, carrier extraction, full counter, or instrument selftest was run. No tools were installed. Comparison reports for ExecGrammar and LB2OfflineClause were not present when searched after completing the independent derivation; no peer output was read before derivation.

Self-evaluation: accuracy 4/5 (no live/frozen-control run, deliberately outside scope); completeness 4/5 (comparison reports unavailable); clarity 5/5 (per-carrier table plus exact JSON paths); actionability 5/5 (retain both expectations; require complete envelopes); conciseness 4/5 (raw receipts carry detail separately). Overall 4.4/5. The residual limitation is explicitly scoped rather than represented as a pass.
