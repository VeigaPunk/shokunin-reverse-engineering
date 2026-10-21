# R21Attack08 — C1 `error_envelope`

## Finding

No actionable discrepancy was observed for this one frozen case. The independent contract sets `error_envelope` to expected exit `1` because the matching Evidence ID and operation remain inside a typed refusal envelope (`.ufo/waves/round-21/fixture-contract.json`, C1 rule). The frozen fixture carries `error.code = execution_failure` above `result.evidence`, whose record has the requested ID and `inspect_wasm_artifact` operation (`.ufo/waves/round-21/fixtures/battery.json:54-58`). The successor traverses supported wrappers while inheriting an ancestor refusal and returns `evidence_refused`/exit 1 for matching blocked records (`.ufo/waves/round-21/tools/verb-coverage.py:39-99`).

## One-case execution

Expected exit was read from the independently frozen contract, not inferred from the implementation. Executed only this fixture against the actual successor CLI, in an external `/tmp` temporary directory that was removed on normal exit. An inert C2 extractor stub was created in that directory but was not invoked: this is the C1 path and its CLI has no extractor argument. No whole battery, C2 case, provider call, or analyzed carrier was run.

```text
argv: ["/usr/bin/python", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/verb-coverage.py", "--evidence", "/tmp/kaidoku-r21-error-envelope-qhgrsxrj/evidence.json", "--verb", "inspect-wasm-artifact", "--evidence-id", "ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"]
expected exit (fixture-contract.json): 1
observed exit: 1
stdout: {"bound": false, "finding": "evidence_refused"}\n
stderr: (empty)
```

## Proposed nearby counterexample — UNRUN

Move the same typed refusal inside `result` while retaining the matching record below it:

```json
{"result":{"error":{"code":"execution_failure"},"evidence":{"evidence_id":"ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","operation":"inspect_wasm_artifact"}}}
```

The contract's typed-refusal-envelope rule implies expected exit `1`; this proposed variant was not exercised.

## Residual risk and verification gaps

- This result supports only C1 `error_envelope`; it says nothing about the other frozen cases, C1's overall claim, or C2 depth.
- No LSP device/server was available (`read xd://lsp` returned “No such tool”), so references/definition/diagnostics could not be requested. Source citations above come from direct reads; any initial text search was only a locator, not semantic proof.
- No tools were installed or updated.
