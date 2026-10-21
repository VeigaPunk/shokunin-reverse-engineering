# C2 review — phase/VA equality and validation

## Scope and evidence

Read-only review of the assigned round-20 `tools/compare-first-failure.py`, `tools/first-failure-extract.py`, `tools/verb-coverage.py`, the R20 C3 interface, the frozen R21 fixture contract, and retained comparator replay/mutation reports. The three assigned R20 tool paths have no diff from baseline `2dd430cb6bcad60ff4db720c052074f1f75eecbc` to observed HEAD `d93c85887d9ae77d224c82c8f56bc8cca86d1a75`; none is locally modified. No production file was edited. No comparator/extractor test, forecast, carrier, REA/provider operation, or other check was executed. No new prediction claim is made.

No `lsp` device is mounted (`xd://lsp` returned “No such tool”); source locations below come from direct reads. A text search was used only to scope `verb-coverage.py`, not as semantic proof.

## Findings by severity

**No behavioral defect found in the assigned equality/type-validation behavior.** `compare-first-failure.py:12-25` validates a non-null failure's kind, integer-or-null index and VA (explicitly rejecting booleans), and string phase. `same_failure` validates both inputs first (`:28-31`), then compares only kind and index (or requires both null; `:32-34`). Thus valid differing VA/phase values are intentionally ignored for equality but are not bypasses around type validation. Its error path maps `ValueError` to `match: null`, exit 2, while match/mismatch return 0/1 (`:81-99`). The extractor produces a string phase and `va: null` for classified failures (`first-failure-extract.py:71-81,107-130`) and returns these in its observation envelope (`:189-195`).

This matches the declared R20 C3 object shape and exit contract (`.ufo/waves/round-20/contract.md:76-81`) and the frozen R21 C2 `kind_index_positive` case (same kind/index, typed phase/VA may differ; expected exit 0). Existing comparator selftest `kind_index_only` uses differing valid VA/phase (`compare-first-failure.py:111-115`). Retained R20 evidence is consistent: `w2/AttackCompareRerun.md:37` describes equality as kind+index, and `w2/MutateCompareFF.md:57-81` records eight historical non-null pairs whose phases differed and whose observed VA was null, with matches retained. These are retrospective records, not new forecasts or a fresh run.

`verb-coverage.py` concerns CLI-verb coverage/evidence binding and is not part of this comparator path; no phase/VA equality behavior is assigned to it.

## Independent supplementary fixture proposal

Keep the frozen 20-case C2 denominator unchanged; add this as a supplemental synthetic matrix, not as a new prediction or replay:

- **Positive:** prediction `first_failure.h1 = {kind:"invalid_index", index:9, va:4096, phase:"markup"}`; extractor envelope has `first_failure = {kind:"invalid_index", index:9, va:null, phase:"analysis"}` and integer `last_line`. Expected: exit 0, `match:true`, both original objects retained in output.
- **Negative VA-type control:** same kind/index, but make one side's `va:true`. Expected: exit 2, `match:null`, validation error identifying `va` as not an integer or null. Python bool-as-int must not pass.
- **Negative phase-type control:** same kind/index and well-typed VA, but make one side's `phase` a number. Expected: exit 2, `match:null`, validation error identifying phase as not a string.

These inputs isolate the equality rule from observation data. The fixed positive overlaps the existing frozen expectation; the two malformed-field controls are supplementary and must not be counted as frozen cases.

## Residual risk and verification gaps

The built-in comparator selftest covers a differing-valid-fields positive and a boolean **index** rejection (`compare-first-failure.py:111-125`), but has no malformed-VA or malformed-phase control. This is a regression-test gap, not evidence of a current behavior defect. No check was run here. If these scripts or their tests are changed, parent should run both bounded selftests and the three synthetic cases above, then the required stable changed-path smoke/final suite once; do not replay/reroute historical predictions or invoke a carrier/provider for this check.

No tools were installed or updated.

Report: .ufo/waves/round-21/w1/C2PhaseVa.md