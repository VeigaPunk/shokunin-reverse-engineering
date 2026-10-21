# C1 ID-to-operation record-binding review

Axes: **C1 calibration**. This is one baseline false-accept finding, not a claim about Evidence authentication or security. C2 comparator/extractor behavior is outside this finding.

## Finding — medium: file-level co-occurrence accepts an ID from another Evidence record

At `.ufo/waves/round-20/tools/verb-coverage.py:149-164`, `bound_evidence` finds a cited `ev_` ID anywhere in a knowledge entry, locates a retained evidence file containing that ID, verifies the file is cited, then accepts if every operation token occurs anywhere in that file and no refusal token occurs. In particular, line 163 checks `all(t in blob for t in tokens)`, not that the ID and operation belong to the same Evidence record. `measure` turns any such pair into `exercised: true` at lines 227-232. This is a single identity-binding defect: the code establishes file co-presence, not record identity.

A reproducer-shaped fixture for the frozen `split_records` negative is:

- Knowledge entry: names `compare-wasm-interfaces`, cites `ev_A` and `.ufo/waves/round-20/evidence/c2/wasm-inspect/id-record.json`.
- Retained JSON envelope: outer record has `evidence_id: ev_A`, `operation: inspect_wasm_artifact`; its normalized result contains a distinct `result.evidence` record with `evidence_id: ev_B`, `operation: compare_wasm_interfaces`, successful status, and no refusal/error tokens. Use `ev_A = ev_` plus 64 `a` characters and `ev_B = ev_` plus 64 `b` characters.
- Expected: the cited ID does **not** bind the requested operation; target `exercised` is false. The frozen contract's negative `split_records` decision is exit **1**. A same-record positive control, including the supported `result.evidence` wrapper with `ev_A` and `compare_wasm_interfaces` in that same record, is expected exit **0** and `exercised: true`.

Static prediction, not an executed test: the R20 implementation accepts the negative pair because the retained file contains `ev_A` and the `compare_wasm_interfaces` token, so `bound_evidence` returns a pair and `exercised` becomes true. The measurement CLI's exit code is still 0 for valid inputs; the expected exit 1 above is the frozen fixture/battery decision, not the CLI's per-target status. A regression selftest should assert false for the negative and true for the positive; against this baseline that selftest would fail (exit 1).

The shipped selftest at `verb-coverage.py:250-304` covers absent/forged IDs, citation/path pairing, and positive file co-occurrence, but has no split-record operation/ID negative. Retained `.ufo/waves/round-20/w2/MutateGuardsAndLint.md:35,44-45` independently reports that its V-operation mutant survived the shipped tests and that wrong-operation evidence can alter accepted bound pairs. That retained mutation is supporting context, not a direct execution of this exact outer-ID/separate-record fixture; the exact expected false acceptance here follows from the source predicate above.

## Scope boundary and verification gaps

`compare-first-failure.py:50-78` consumes an extractor JSON envelope and compares first-failure observations; `first-failure-extract.py:134-196` emits `first_failure` with `last_line`. Neither implements the C1 Evidence-ID/operation binding predicate, so I make no additional finding against those files in this report.

The frozen contract was read at `.ufo/waves/round-21/fixture-contract.json:5-17`; this proposed case fits `split_records` and does not change its denominator. Retained `.ufo/waves/round-20/w2/EntryHarmonyClaims.md:7` also records distinct outer and nested Evidence IDs in a real retained result, demonstrating why wrapper/record identity must be explicit; it does not by itself prove the synthetic misclassification.

LSP is unavailable in this tool environment (`read xd://lsp` returned “No such tool”), so no semantic references/definition/diagnostics were available. Text reads are source observations, not LSP proof. No checks, tests, builds, formatters, or validators were run; no production files were edited. No tools were installed.

Parent should run the frozen C1 battery after implementation (`python3 -I -B .ufo/waves/round-21/battery.py --root <LANE> --rev <REV> --claim C1`) and the changed-path smoke once, confirming all frozen positives/negatives retain their declared decisions and the negative is not accepted. No C2 claim is made here.

Report: .ufo/waves/round-21/w1/C1IdRecord.md