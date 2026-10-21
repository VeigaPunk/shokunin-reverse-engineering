# C2 — naked-null extractor output

## Axis and verdict

**Axis:** C2 depth. **Finding: one medium-severity baseline defect** in `compare-first-failure.py`: a bare JSON `null` from the extractor is treated as a valid silent observation despite having no observation envelope or `last_line` bound. Do not count the resulting false match and false mismatch as separate defects.

## Finding

`kaidoku-shokunin/.ufo/waves/round-20/tools/compare-first-failure.py:12-15` explicitly accepts `None` as a valid failure value. `run_extractor` unwraps a result only when it is a dict containing both `first_failure` and `last_line` (`:72-78`), but otherwise passes the parsed JSON value directly to `validate_failure`. Thus top-level JSON `null` bypasses the envelope/bound requirement and survives validation. `same_failure` returns true for two nulls (`:28-34`); `evaluate_paths` then returns exit 0 for that match (`:81-99`). With a null prediction, an unbounded bare null can therefore be reported as a clean match. With a non-null prediction it is reported as an ordinary mismatch (exit 1), not as malformed/unobservable output (exit 2).

The extractor’s own shape is correctly bounded: its docstring defines null as “no qualifying failure … through” `last_line` (`kaidoku-shokunin/.ufo/waves/round-20/tools/first-failure-extract.py:4-8`); `parse_log` computes `last_line` (`:134-149`) and returns it alongside `first_failure` (`:189-195`). The defect is at the comparator’s acceptance boundary, not in this extraction contract. Comparator selftest checks `same_failure(None, None)` directly and exercises an unwrapped non-null object, but does not exercise a null extractor response through `run_extractor` (`compare-first-failure.py:102-145`).

### Independently specified positive/negative fixture

Use the frozen C2 contract’s `bounded_silent_positive` and `naked_null` cases; preserve their denominator and do not infer a new label (`.ufo/waves/round-21/fixture-contract.json:19-30`). In both cases use prediction `{"first_failure":{"h1":null}}` and a synthetic extractor process that exits 0:

- **Positive:** stdout is an envelope such as `{"first_failure":null,"last_line":4}`. Expected comparator exit **0**, `match: true`.
- **Negative:** stdout is bare JSON `null`, with no envelope and no bound. Expected comparator exit **2**, unevaluable/malformed extractor observation (absence is not established); it must not report a match or mismatch.

This is a fixture specification only; it was not executed. The retained normal-silence comparison at `.ufo/waves/round-20/evidence/compare-rerun/t1246-asm.json:1` is `{"match":true,"observed":null,"predicted":null}`. `verify/round20/measure.json:748-765` likewise records a matched, valid record and `first_failure_bound: true`. These are historical comparator/measurement results, not raw extractor stdout, so they establish the retained legitimate null/null result but do **not** show that the malformed bare-null case was exercised.

## Scope and residual risk

`verb-coverage.py` is a separate CLI-name/knowledge-entry/evidence counter by its own description (`.ufo/waves/round-20/tools/verb-coverage.py:1-9`) and its measurement loop (`:202-240`). Literal search found no first-failure/extractor references in that file; this is not semantic call-graph proof. No additional finding is claimed there.

## Verification gaps and parent checks

No tests, selftests, builds, validators, provider/carrier runs, or other verification were run. No LSP device/server was exposed in the supplied tool inventory, so the literal-search fallback was used; grep output is not presented as semantic proof. Static source inspection is the basis for the defect.

After a fix, parent should run the paired frozen C2 positive/negative cases above, preserving exits 0/2, and run the C2-only battery from the claims contract (`python3 -I -B .ufo/waves/round-21/battery.py --root <LANE> --rev <REV> --claim C2`). Confirm C2 remains independent of C1, then run the parent’s planned stable changed-path smoke and final suite. I did not run any of these checks.
