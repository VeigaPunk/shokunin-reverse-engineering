# R21 Attack 23 — C2 `missing_last_line`

## Finding

No defect observed in the assigned frozen case. The successor returned the independently expected unevaluable result when the extractor envelope omitted `last_line`.

## Frozen basis

- `.ufo/waves/round-21/fixture-contract.json`, C2 `missing_last_line`: expected exit `2`; absence needs an explicit observation bound.
- `.ufo/waves/round-21/fixtures/battery.json`, C2 case `missing_last_line`: `expected_exit: 2`; prediction is `{"first_failure":{"h1":null}}`; extractor stdout is `{"first_failure": null}` and extractor exit is `0`.
- Successor: `.ufo/waves/round-21/tools/compare-first-failure.py`. Its SHA-256 at the working path matched the `HEAD` blob (`990bc17c6dd5a4fc80d89e27a30c26916ec9f42e012a94c1f3ea69f6bb92ef5c`; lane revision observed as `e8df818`).

## Single-case execution

Ran the actual successor with the frozen case values and an inert extractor stub in an external `mktemp` directory removed by an `EXIT` trap. Only this case was exercised; no battery or other successor tests were run.

```text
argv: python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/compare-first-failure.py --prediction /tmp/kaidoku-r21-missing-last-line.Hw9KOF/prediction.json --log /tmp/kaidoku-r21-missing-last-line.Hw9KOF/log.txt --extractor /tmp/kaidoku-r21-missing-last-line.Hw9KOF/extractor.py
stdout: {"error": "observation_envelope_required", "finding": "comparison_unevaluable", "match": null, "observed": null, "predicted": null}
stderr: (empty)
observed exit: 2
expected exit: 2
```

The CLI result agrees with the frozen expected exit. The reported error is consistent with the missing observation-envelope bound; this single run does not establish broader C2 behavior.

## Nearby counterexample — UNRUN

Try an otherwise valid envelope with `first_failure: null` and `last_line: 8.0` (JSON float). The contract requires an integer line bound, so the expected outcome would be exit `2`; this would probe typed-bound validation adjacent to the absent-bound case. Not exercised under the one-case-only assignment.

## Residual risk and verification gaps

- This is a one-case result, not a conclusion about the rest of C2, R20 regression compatibility, or the battery.
- No analyzed carrier or provider was executed or queried.
- No LSP route is exposed in this session (`xd://lsp` returned “No such tool”), so references, definition, and diagnostics were not available; no semantic caller audit is claimed.
- No tools were installed or updated.

Report: `.ufo/waves/round-21/w2/R21Attack23.md`
