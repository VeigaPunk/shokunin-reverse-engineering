# R21Attack02 — `wrapper_positive`

## Scope and axes

- **C1 / calibration:** the one frozen positive control `wrapper_positive`.
- **C2 / depth:** not exercised; no C2 or regression case was run.
- No other battery case, provider, analyzed carrier, build, or broad test was run.

## Frozen expectation

Read the assigned case from `round-21/fixtures/battery.json` and its independent rule from `round-21/fixture-contract.json`. Both declare exit **0**. The contract rule is: “supported `result.evidence` wrapper preserves same-record identity.” The evidence record inside `result.evidence` contains the requested `evidence_id` (`ev_` followed by 64 `a` characters) and operation `inspect_wasm_artifact`.

The local frozen-input digests matched `round-21/fixtures/expected.json`:

- `fixtures/battery.json`: `2ff59eb249f0535ec3ff840d0c10f9fbf6fcf41b952bbe1bde4874e62fb752ba`
- `fixture-contract.json`: `04f54077f09bd68f9314f2c9b9febf10cb4b0434990dee51ea797fda9aa700f6`

## One-case execution

Executed the actual successor CLI, `round-21/tools/verb-coverage.py` (SHA-256 `77db29fde196c2a0db19a522d21cf8bf315a383250c7115fda71f04bd141e2cc`), directly for this case only. The evidence input was written to an external `TemporaryDirectory` and the directory was removed after the process returned.

**Exact argv:**

```text
["/usr/bin/python", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/verb-coverage.py", "--evidence", "/tmp/kaidoku-r21-R21Attack02-pssp82of/wrapper-positive-evidence.json", "--verb", "inspect-wasm-artifact", "--evidence-id", "ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"]
```

Working directory: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`

**stdout:**

```text
{"bound": true, "finding": "evidence_bound", "pathless": false}
```

**stderr:** empty (`""`). **Observed exit:** `0`. **Expected exit:** `0` (fixture and contract). The temporary directory was confirmed removed after execution.

This is consistent with the successor implementation’s supported-wrapper traversal and exact id/operation binding (`tools/verb-coverage.py:58-99`), and its evidence CLI (`:168-192`). It establishes only this positive case, not the full C1 claim.

The C2 extractor stub was not invoked: this is a C1 case, and the successor CLI exercised here accepts evidence/verb/id inputs and does not call an extractor. No C2 observation was supplied or measured; no C2 claim is made.

## Nearby counterexample — UNRUN

An outer typed refusal around the otherwise matching wrapped record, e.g. `{"error":{"code":"execution_failure"},"result":{"evidence":{"evidence_id":"ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","operation":"inspect_wasm_artifact"}}}`, should reject with exit **1** under the frozen `error_envelope` contract (“matching id and operation remain inside typed refusal envelope”). This nearby negative was **not executed** in this assignment.

## Findings, residual risk, and verification gaps

- **Actionable findings:** none for the assigned case; observed exit and finding match its frozen positive expectation.
- **Residual risk:** one positive control does not test refusal, split-record, malformed, duplicate-member, or other negative/positive cases. The binding claim is local record binding, not cryptographic Evidence authentication.
- **Verification gap:** the `lsp` device is unavailable in this environment (`read xd://lsp` returned “No such tool”); therefore no LSP status, references, definition, or diagnostics results were available. No conclusions about broader callers or diagnostics are drawn from this one-case execution.
- No tools were installed or updated.