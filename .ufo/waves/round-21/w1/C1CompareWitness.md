# C1 Compare-WASM Witness Review

**Verdict: PARTIAL — one concrete evidence-identity defect in the baseline matcher; the retained compare witness itself is a valid positive.**

**Axes:** C1 calibration is in scope. C2 depth is kept separate; the first-failure files were read only to confirm the distinct observation-envelope shape, not to issue a C2 finding.

## Finding — Medium, C1 calibration: nested input Evidence IDs are misbound to the comparison operation

At `.ufo/waves/round-20/tools/verb-coverage.py:136-165`, `bound_evidence` collects each cited `ev_` identifier, locates any retained blob containing it, then accepts that blob when the requested operation token is present anywhere in its bytes and no listed refusal token appears. It does not parse the Evidence record and require the cited ID to equal that record's own `evidence_id` with its `operation` field. This makes file-level co-occurrence stand in for the record-bound predicate.

The real successful comparison record demonstrates the consequence without a fabricated example:

- `.ufo/waves/round-20/evidence/c2/wasm-compare/compare-real-both.stdout.txt:1` has root `evidence_id=ev_387167...` and root `operation=compare_wasm_interfaces`. Its `parameters.left_evidence_id` / `right_evidence_id`, `normalized_result.left.evidence_id` / `right.evidence_id`, and `evidence_links` contain the input IDs `ev_4b405...` and `ev_b215...`.
- `corpus/knowledge/2026-10-20-r20-wasm-interfaces.md:15-16,24-26` identifies `ev_4b405...` and `ev_b215...` as the two `inspect_wasm_artifact` results, and `ev_387167...` as the comparison result.
- The retained `.ufo/waves/round-20/verify/round20/verb-coverage.json` target record for `compare-wasm-interfaces` nevertheless lists both input IDs as `bound_evidence` at `compare-real-both.stdout.txt`, alongside the actual root comparison ID. The root comparison is independently retained as a successful run by `compare-real-both.receipt.json` (`exit_code: 0`, stdout path and digest at lines 27, 40-44).

Thus two of the five returned `bound_evidence` pairs for this target are not comparison-record IDs; they are inspection inputs found nested inside a compare record. This is one identity-binding defect, not evidence that the actual compare operation was absent: the three root comparison IDs (`ev_2529...`, `ev_387167...`, `ev_ca8b...`) support `exercised: true`. Do not turn the two extra pairs into a claim that the current target-level boolean is false.

The current `verb-coverage.py` selftest (`:250-304`) covers ID/path co-occurrence and a missing/forged ID, but has no nested-input or split-record identity case. The separate blacklist weakness is already directly recorded in `.ufo/waves/round-20/w2/CriticQuality2325.md:18-24` (`execution_failure` is not excluded); I do not count it again as another finding. The frozen C1 refusal controls still need to remain in the battery.

## Independently specified positive/negative fixture

Use the real record structure above, with synthetic IDs in an isolated fixture repository (not a production or retained artifact): let `A = ev_` plus 64 `a` characters and `B = ev_` plus 64 `b` characters. One fixture contains an `inspect_wasm_artifact` record whose root ID is A and a successful `compare_wasm_interfaces` record whose root ID is B and whose left-input fields reference A. The knowledge-entry fixture cites the comparison evidence path.

- **Positive control:** cite B for `compare-wasm-interfaces`. B is the comparison record's own ID and its exact operation is in that same record. Expected case exit **0**, target exercised, and `(B, compare-record-path)` bound.
- **Negative control (`split_records`):** cite A for `compare-wasm-interfaces`. A belongs to the inspect record; its appearance as an input in the separate comparison record must not rebind A to the compare operation. Expected case exit **1**, target not exercised for that cited ID, and no `(A, compare-record-path)` pair.

These are the frozen `same_record_positive` and `split_records` expectations in `.ufo/waves/round-21/fixture-contract.json:6,8`; they are not new denominator cases. The old whole-blob predicate would accept the negative because the comparison file contains both A and `compare_wasm_interfaces`. A corrected record parser should retain the positive and reject the negative. The `expected_exit` values above are case outcomes, not a claim about the outer battery process exit.

## Scope, residual risk, and verification gaps

- The actual output is a useful canonical shape: root `evidence_id` and `operation`, followed by input references under `parameters` and normalized result fields. The record is a derived static comparison (`authority: analyst-inference`) with explicit limitations; it does not establish authenticity, runtime compatibility, or behavior beyond the declared interfaces.
- The C2 comparator unwraps the extractor envelope at `.ufo/waves/round-20/tools/compare-first-failure.py:72-78`; `.ufo/waves/round-20/tools/first-failure-extract.py:189-195` emits `first_failure` with `last_line`. No C2 judgment is made here.
- LSP was unavailable: attempting `xd://lsp` returned “No such tool” and listed mounted devices without an LSP device. Targeted source reads and literal grep were used as fallback; grep is not presented as semantic proof.
- No tests, selftests, battery, build, lint, live provider, REA producer, or carrier were run. No production file was edited and no tool was installed. Parent should run the frozen C1 battery (all 12 contract cases) and the stable changed-path smoke after the author changes land; retain the positive root-ID control and assert the nested-input negative is rejected. The existing C2 and 19-pair R20 regression checks remain separate.

Report: .ufo/waves/round-21/w1/C1CompareWitness.md