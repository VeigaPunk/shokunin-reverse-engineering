# R21Attack15 — C2 `nullable_eof_positive`

## Frozen contract

The independently frozen `fixture-contract.json` declares `nullable_eof_positive` expected exit **0**: “legitimate eof kind with explicit null index retains matching semantics.” The matching `battery.json` C2 row also declares exit 0. It predicts `first_failure.h1 = {kind: "eof", index: null, va: null, phase: "analysis"}`; the fixture's extractor stdout contains the same failure and `last_line: 8`, with extractor exit 0.

## One-case successor CLI run

Executed only this case through `tools/compare-first-failure.py`. The external temporary directory held the prediction, log, and an inert extractor that only prints the supplied log text; it was removed on completion. No analyzed carrier was executed.

Producing argv:

```text
/usr/bin/python -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/compare-first-failure.py --prediction /tmp/kaidoku-r21-attack15-z8dr6kcc/prediction.json --log /tmp/kaidoku-r21-attack15-z8dr6kcc/log.json --extractor /tmp/kaidoku-r21-attack15-z8dr6kcc/extractor.py
```

Observed stdout (verbatim):

```text
{"finding": "failure_match", "last_line": 8, "match": true, "observed": {"index": null, "kind": "eof", "phase": "analysis", "va": null}, "predicted": {"index": null, "kind": "eof", "phase": "analysis", "va": null}}
```

Observed stderr: empty.

| Expected exit (fixture contract) | Expected exit (battery) | Observed exit |
| ---: | ---: | ---: |
| 0 | 0 | 0 |

The observed result matches both independently frozen exits and preserves the explicit null index as part of a valid `eof` failure.

## Nearby counterexample — unrun

Perturb the observed `eof` failure by removing the `index` member while retaining `kind`, `va`, and `phase` and the bounded envelope. This is adjacent to the tested null-versus-present distinction. It was **not run**. The frozen contract's separate `missing_index` rule declares exit 2 because the index member must exist and nullable differs from absent; this is a contract-based proposal, not an observed result.

## Residual risk and verification gaps

This was one isolated frozen C2 case, not the battery or the retained R20 regression set. The inert extractor only echoed the fixture's supplied stdout, so this run checks successor comparison behavior for this input, not extractor fidelity or any carrier behavior. No other case, malformed variant, or counterexample was executed.