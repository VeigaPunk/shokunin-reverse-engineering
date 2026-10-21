# C2 review — equal index, different kind

## Finding

**No baseline behavior defect in equal-index/different-kind comparison.** `same_failure` validates both observations and returns true for object outcomes only when **both** `kind` and `index` match; `va` and `phase` are deliberately ignored (`.ufo/waves/round-20/tools/compare-first-failure.py:28-34`). Thus two otherwise valid outcomes with the same integer index and different kinds are a mismatch, not a false match.

The known extractor grammar supplies an in-scope typed pair: `_classify_failure` emits `invalid_index` with an extracted integer (`.ufo/waves/round-20/tools/first-failure-extract.py:107-111`) or `eof` with an extracted integer (`:113-116`). The latter is selected by an `Unable to read past EOF: N, M` continuation when the context contains no `Invalid index: N`; EOF/I/O exceptions without an extracted index use nullable indices (`:118-130`). This supports testing `invalid_index/41` against `eof/41` without inventing an extractor kind.

**One regression-test gap:** the comparator's in-file selftest covers same-kind/index with differing `va`/`phase`, index mismatch at same kind, and a boolean-index rejection, but has no equal-index/different-kind case (`.ufo/waves/round-20/tools/compare-first-failure.py:111-125`). The frozen C2 contract explicitly requires `kind_mismatch_equal_index` to exit 1 (`.ufo/waves/round-21/fixture-contract.json:25`). This is a missing regression case, not evidence that the comparison predicate is defective.

## Independent paired fixture proposal

Use one synthetic parseable log for both variants:

```text
2026-01-01 00:00:00 ERROR (GoTypeManager) Go analysis failure java.io.IOException: wrapper
Caused by: java.io.EOFException: Unable to read past EOF: 41, 32
```

The extractor's known grammar yields an envelope with `first_failure = {kind: "eof", index: 41, va: null, phase: "GoTypeManager"}` and a nonnegative `last_line` bound. Supply the same log and extractor for these two prediction variants:

| Variant | `first_failure.h1` prediction | Expected comparator result |
|---|---|---|
| Positive control | `{kind: "eof", index: 41, va: 4096, phase: "forecast"}` | exit **0**, `match: true`; confirms `va` and `phase` do not affect the declared equality |
| Negative control | `{kind: "invalid_index", index: 41, va: null, phase: "forecast"}` | exit **1**, `match: false`; same index, different known kind |

For the negative case the predicted and observed objects should both be included in the comparator JSON result; the observed kind remains `eof`, and the mismatch is solely the `kind` field. Keep these as the frozen `kind_index_positive` and `kind_mismatch_equal_index` cases, not supplementary cases or a denominator change.

## Retained evidence and scope

The retained R20 summary has 19/19 successful exact-artifact comparisons; its non-null records are `invalid_index` matches and the other records are null (`.ufo/waves/round-20/evidence/compare-rerun/summary.txt:1-19`; retained aggregate `measure.json:1539`). That is retrospective agreement evidence, not a cross-kind negative control. `verb-coverage.py`'s relevant `bound_evidence` function binds cited evidence IDs/files to operation tokens and refusal tokens (`.ufo/waves/round-20/tools/verb-coverage.py:136-165`); it does not compare first-failure `kind` or `index`, so it neither supplies nor contradicts this result.

## Verification gaps / parent checks

- No LSP device was mounted (`xd://lsp` returned “No such tool” and the mounted-device list contained no LSP device); therefore no LSP status, references, definition, or diagnostics were available. Used targeted source reads only; no grep was used.
- No checks or runtime commands were executed for this read-only review. Parent should include the positive and negative fixture variants above in the frozen C2 battery and run the frozen C2 command once after integration: `python3 -I -B .ufo/waves/round-21/battery.py --root <LANE> --rev <REV> --claim C2`. Confirm declared exits 0 and 1 respectively and preserve the frozen twenty-case denominator and nineteen R20 retrospective matches.
- No R20 production file was edited; no analyzer or carrier was run.

Report: .ufo/waves/round-21/w1/C2Kinds.md
