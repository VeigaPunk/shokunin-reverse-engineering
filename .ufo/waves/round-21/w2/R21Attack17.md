# R21Attack17 — R21-C2 `object_predicted_null_observed`

**Axes:** calibration (agreement with the independently frozen exit); depth (distinguishing bounded observed silence from a malformed/missing observation). This report covers only the assigned C2 case.

## Recommendation

No actionable finding for this case: the single actual-successor invocation returned the frozen expected mismatch exit. This is a recommendation about the scoped case, not an admission or a claim about the full C2 battery.

## Frozen oracle

- `fixtures/battery.json:145-158` freezes the prediction as an `invalid_index` object (`index: 9`, `phase: "analysis"`) and extractor output `{"first_failure": null, "last_line": 8}`, with `extractor_exit: 0` and `expected_exit: 1`.
- `fixture-contract.json:24` independently declares this case `expected_exit: 1`, rule `well-formed but different outcomes`.

## Actual successor CLI run

The successor was the checked-out `tools/compare-first-failure.py` (SHA-256 `990bc17c6dd5a4fc80d89e27a30c26916ec9f42e012a94c1f3ea69f6bb92ef5c`). One invocation used `/usr/bin/python` with `-I -B`. Prediction, inert log input, and an extractor stub that only wrote the frozen `stdout` string and exited 0 were placed in `/tmp/kaidoku-r21-R21Attack17-jv3z5a4n`; that external temporary directory was removed after the run.

Actual argv:

```json
["/usr/bin/python", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/compare-first-failure.py", "--prediction", "/tmp/kaidoku-r21-R21Attack17-jv3z5a4n/prediction.json", "--log", "/tmp/kaidoku-r21-R21Attack17-jv3z5a4n/log.txt", "--extractor", "/tmp/kaidoku-r21-R21Attack17-jv3z5a4n/extractor.py"]
```

- Observed exit: **1**
- Expected exit (fixture and contract): **1**
- stdout (including its trailing newline): `{"finding": "failure_mismatch", "last_line": 8, "match": false, "observed": null, "predicted": {"index": 9, "kind": "invalid_index", "phase": "analysis", "va": null}}\n`
- stderr: empty
- Temporary directory removed: **yes**

This is consistent with `compare-first-failure.py:63-74`: the bounded envelope is accepted, and at line 71 an object prediction versus null observation cannot match; the mismatch returns exit 1. The exception path returns exit 2 for unevaluable input. No analyzed carrier was executed and no provider was called.

## Nearby counterexample proposal — UNRUN

Keep the same prediction but have the inert extractor emit `{"first_failure": {"kind": "invalid_index", "index": 9, "va": null, "phase": null}, "last_line": 8}`. Proposed expectation: exit 2 (unevaluable), not a match, because the observation's phase is not a string even though phase is not part of equality (`compare-first-failure.py:46-47, 70-74`). This proposed variant was not run and is not part of the frozen denominator.

## Residual risk and verification gaps

- Only the assigned case was executed; the C2 battery, retained R20 regression set, other cases, and the proposed counterexample were not run.
- The LSP device is unavailable in this environment (`read xd://lsp` returned `No such tool`); no LSP status/references/definition/diagnostics checks were possible. Text search was used only to locate the assigned case, not as semantic proof.
- This was one direct CLI invocation, with no rerouting; no saturation claim is made. Same-identity rerouting and resume behavior are not exercised by this case.
- No source or fixture was edited, and no tool was installed or updated.