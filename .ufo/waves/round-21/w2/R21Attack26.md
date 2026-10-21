# R21-C2 attack: `string_last_line`

**Axes:** C2 depth was exercised; calibration is not assessed by this single case.

## Findings (severity order)

No actionable defect demonstrated for the assigned case. The successor treated the string-valued observation bound as unevaluable and returned the frozen expected exit.

## Evidence and execution

- Frozen case: `.ufo/waves/round-21/fixtures/battery.json`, `C2[string_last_line]` (lines 264–272): `expected_exit` 2; prediction `first_failure.h1: null`; extractor output `{"first_failure": null, "last_line": "8"}`; extractor exit 0.
- Independent contract: `.ufo/waves/round-21/fixture-contract.json`, C2 `string_last_line`: expected exit 2 because “string is not a line count.” The result below is judged against this contract, not inferred from the implementation.
- Successor: `.ufo/waves/round-21/tools/compare-first-failure.py`.
- Actual CLI argv (captured invocation):
  ```text
  python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/compare-first-failure.py --prediction /tmp/kaidoku-r21-string-last-line.mzJV4f/prediction.json --log /tmp/kaidoku-r21-string-last-line.mzJV4f/log.txt --extractor /tmp/kaidoku-r21-string-last-line.mzJV4f/extractor.py
  ```
- Temporary inputs were external to the checkout. The prediction matched the frozen case; the log contained only inert fixture text. The extractor stub emitted the frozen JSON string and exited 0; no carrier was executed.
- CLI stdout:
  ```text
  {"error": "invalid_last_line", "finding": "comparison_unevaluable", "match": null, "observed": null, "predicted": null}
  ```
- CLI stderr: empty.
- Observed exit: **2**. Expected exit: **2**. Match.
- The same single case was invoked twice (one initial run and one stream-captured run for this report); no other fixture or battery was run. The external temporary directory was removed afterward.

## Nearby counterexample proposal — UNRUN

Use the adjacent boolean-bound shape: same null prediction and envelope, but `last_line: true` (the frozen `boolean_last_line` case). Expected exit **2** under the contract’s “bool is not a line count” rule. This distinguishes strict integer validation from implementations that accept Python booleans as integers. It was not exercised in this assignment.

## Residual risk and verification gaps

- This one case establishes only the string-bound behavior. The other C2 malformed/valid controls and the retained nineteen R20 artifact comparisons were not run; no broader C2-depth or calibration claim follows.
- No `lsp` device was mounted: `read xd://lsp` returned “No such tool.” Therefore LSP status, references, definition, and diagnostics were unavailable. No grep output is used as semantic proof; the source was read only to identify the CLI interface.
- No REA/provider calls, analyzed-carrier execution, installs, production/fixture edits, or lane Git/index mutations were performed.
