# C2 asymmetric-null review

**Axis:** C2 depth. Calibration is unchanged by this comparator review.

## Findings by severity

- **No defect in either bounded asymmetric-null comparison.** `compare-first-failure.py:12-25` accepts `None` as the explicit no-failure value and validates a non-null failure shape; `same_failure` at `:28-34` returns true only when both values are null, so either null/object direction is a well-formed mismatch. For valid inputs, `evaluate_paths` at `:81-99` returns `match: false`, exit 1. Exit 2 is reserved for input/extractor errors caught at `:88-94`; a difference between two valid observed outcomes is not such an error. In the reverse direction, a bounded null is still an observed silence, not missing data.

  This matches the frozen C2 contract: `null_predicted_object_observed` and `object_predicted_null_observed` each require exit 1 (`fixture-contract.json:23-24`); the distinct `bounded_silent_positive` requires an explicit envelope and integer `last_line` for null/null exit 0 (`:20`). `first-failure-extract.py` defines null as no qualifying failure *through* `last_line` (`:4-8`), computes that bound, and returns it with `first_failure` (`:134-149`, `:189-195`).

- **One separate boundary defect, not an asymmetric-null defect and not two findings:** `compare-first-failure.py:69-78` conditionally unwraps an envelope only if both `first_failure` and `last_line` exist, then validates an unwrapped or raw value. Since `validate_failure(None)` succeeds (`:14-15`), a naked top-level JSON `null` can bypass the required envelope/bound and be treated as silence; with a null prediction it can yield a false match (exit 0), and with an object prediction it yields a mismatch (exit 1), rather than unevaluable (exit 2). The frozen `naked_null` case requires exit 2 (`fixture-contract.json:27`). This is the single envelope-boundary issue already described in `C2NakedSilence.md:5-20`; do not count its match and mismatch outcomes, or the two valid asymmetry directions, as additional defects.

## Fixture specification

Use one independently authored synthetic extractor-output fixture set, retaining the frozen case IDs/denominator:

| Case | Prediction | Extractor stdout | Expected |
|---|---|---|---|
| Positive `bounded_silent_positive` | `{"first_failure":{"h1":null}}` | `{"first_failure":null,"last_line":4}` | exit 0; `match: true` |
| Negative `null_predicted_object_observed` | `{"first_failure":{"h1":null}}` | `{"first_failure":{"kind":"invalid_index","index":41,"va":null,"phase":"map"},"last_line":4}` | exit 1; `match: false` |
| Negative `object_predicted_null_observed` | `{"first_failure":{"h1":{"kind":"invalid_index","index":41,"va":null,"phase":"map"}}}` | `{"first_failure":null,"last_line":4}` | exit 1; `match: false` |
| Boundary control `naked_null` | `{"first_failure":{"h1":null}}` | `null` | exit 2; unevaluable, not match/mismatch |

The last row is an adjacent shape control, not an extra asymmetry case. These are specifications only; none were executed.

## Retained evidence and scope

R20 retained records establish symmetric matches, not either asymmetry direction: `evidence/compare-rerun/summary.txt:2-19` has 19 matches, including 11 `[null,null]` and 8 non-null kind/index pairs. For a representative null case, `evidence/compare-rerun/t1246-test2json.json:1` records `match:true, observed:null, predicted:null`; its extractor envelope at `evidence/extract/t1246-test2json.json:3-5` has `first_failure:null` and `last_line:191`. These are retrospective artifacts, not a fresh run or evidence that R20 exercised the asymmetric branches.

Comparator selftest has a direct `both_silent` assertion and non-null kind/index controls (`compare-first-failure.py:111-125`), but no assertions for the two asymmetric-null cases or their end-to-end exit codes. This is a regression-coverage gap, not evidence that the implemented bounded comparison semantics are wrong. `verb-coverage.py:1-9,136-166,204-232` is a separate CLI-name/knowledge-entry/evidence counter; no null-comparison responsibility is claimed for it. `first-failure-extract.py` has a bounded-absence selftest case (`:244-256`), but it does not test comparator asymmetry.

No `lsp` device was mounted: the attempted `xd://lsp` lookup returned “No such tool” and the available-device list. Literal source searches were only used to locate sections; findings above are based on the cited source reads, not grep as semantic proof. No tests, selftests, validators, builds, provider/carrier runs, or production edits were performed. No tools were installed.

## Parent checks

Run the frozen C2 battery without changing its denominator, including both asymmetric-null cases, bounded-null positive, and naked-null negative; then run the parent-planned stable changed-path smoke and final suite once. Confirm the comparator reports exit 1/`match:false` for both valid asymmetric directions and exit 2 for the unbounded-null control. No check was run by this reviewer.

Report: `.ufo/waves/round-21/w1/C2NullAsymmetry.md`
