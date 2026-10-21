# R21Attack20 — frozen C2 `naked_null`

## Axis and result

**Axis:** C2 depth only. **Finding:** no actionable defect evidenced for the one assigned case. The actual successor CLI returned the independently frozen exit `2` for `naked_null`.

## Independent expectation and case

The expected exit was taken from `.ufo/waves/round-21/fixture-contract.json` (`C2/naked_null`: exit `2`, rule: “no observation envelope or last_line bound”), not inferred from the successor implementation. `.ufo/waves/round-21/fixtures/battery.json` independently gives the same expected exit and this input:

- prediction: `{"first_failure":{"h1":null}}`
- extractor stdout: `null`
- extractor exit: `0`

The C2 claim in `claims.json` concerns distinguishing absent/malformed observations from bounded observed silence. I read the relevant successor, `.ufo/waves/round-21/tools/compare-first-failure.py`, and ran only this case through its CLI.

The frozen-input manifest at `fixtures/expected.json` lists SHA-256 `04f54077f09bd68f9314f2c9b9febf10cb4b0434990dee51ea797fda9aa700f6` for `fixture-contract.json` and `2ff59eb249f0535ec3ff840d0c10f9fbf6fcf41b952bbe1bde4874e62fb752ba` for `fixtures/battery.json`. A `sha256sum` run returned those exact values for both files.

## One-case CLI execution

I created the prediction, log text, and inert extractor stub in `/tmp/kaidoku-r21-R21Attack20-xzmo1ffp`, outside the repository, and used the fixture values. The stub only read its input log and wrote its contents unchanged to stdout:

```python
import pathlib, sys
sys.stdout.write(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
```

**Actual successor argv:**

```json
["/usr/bin/python3", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/compare-first-failure.py", "--prediction", "/tmp/kaidoku-r21-R21Attack20-xzmo1ffp/prediction.json", "--log", "/tmp/kaidoku-r21-R21Attack20-xzmo1ffp/log.json", "--extractor", "/tmp/kaidoku-r21-R21Attack20-xzmo1ffp/extractor.py"]
```

**Successor stdout** (newline-terminated):

```json
{"error": "observation_envelope_required", "finding": "comparison_unevaluable", "match": null, "observed": null, "predicted": null}
```

**Successor stderr:** empty  
**Observed exit:** `2`  
**Expected exit:** `2` (fixture contract and frozen battery)  
**Temp cleanup:** confirmed removed after the invocation; it was outside the repository.

## Nearby counterexample proposal — UNRUN

`bounded_silent_positive` is a nearby boundary control: null prediction with an explicit envelope containing `first_failure: null` and integer `last_line`, expected exit `0` under the frozen contract. It would distinguish accepting properly bounded silence from rejecting every null observation. It was not run; this assignment exercised only `naked_null`.

## Residual risk and verification gaps

- This result covers only `naked_null`; it does not establish the complete C2 claim, the other C2 cases, retained R20 compatibility, or any C1 behavior. No full battery, selftest, build, or broad test suite was run.
- No analyzed carrier was executed and no provider/REA calls or installs were made.
- No `lsp` device/server was exposed in the available tool inventory, so LSP status, references, definition, and diagnostics could not be checked. No text grep was used as semantic proof. This is a single-case behavioral check, not a complete caller/call-graph review.

Report: `.ufo/waves/round-21/w2/R21Attack20.md`
