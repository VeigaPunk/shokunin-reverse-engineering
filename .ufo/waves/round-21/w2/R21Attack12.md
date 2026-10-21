# R21Attack12 — C1 `duplicate_member_ambiguity`

## Finding by severity

**No actionable finding for the assigned frozen case.** The actual C1 successor returned the independently frozen expected exit for this single case.

## Frozen contract and observed run

- `fixtures/battery.json`, C1 `duplicate_member_ambiguity`: expected exit **2**. Its Evidence JSON has two top-level `operation` members, first `inspect_artifact`, then `inspect_wasm_artifact`, with the cited Evidence ID and requested verb `inspect-wasm-artifact`.
- `fixture-contract.json`, C1 `duplicate_member_ambiguity`: independently specifies expected exit **2** because “contradictory duplicate operation names cannot select last-wins success.” The frozen case and contract agree; the expected result is taken from the contract, not inferred from the successor.
- C1 axis/context: `claims.json` describes local record-bound operation/id/refusal decisions; it expressly does not claim cryptographic Evidence authentication.
- Successor exercised: `.ufo/waves/round-21/tools/verb-coverage.py`, the C1 direct CLI. Only this case was run; the battery was not run.
- Exact producing argv (the external temporary evidence file and stub were removed on context exit):

```text
["/usr/bin/python", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/verb-coverage.py", "--evidence", "/tmp/kaidoku-r21-attack12-b3bbg2u7/duplicate_member_ambiguity.json", "--verb", "inspect-wasm-artifact", "--evidence-id", "ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"]
```

- Expected exit: **2**. Observed exit: **2**.
- Exact stdout: `{"bound": null, "error": "duplicate_member: operation", "finding": "evidence_unevaluable"}\n`
- Exact stderr: empty.
- An inert C2 extractor stub was staged in the same external temporary directory. It was **not** passed to or invoked by this C1 CLI: `verb-coverage.py` accepts the evidence/verb/id inputs for this branch, and the assignment's single target is C1. No C2 case or comparator run occurred.
- No analyzed carrier was executed and no provider call was made.

The observed `evidence_unevaluable` / exit 2 is consistent with the frozen contract's fail-closed duplicate-member rule for this record.

## Nearby counterexample — UNRUN

`[UNRUN]` Put the same contradictory duplicate `operation` members inside the supported `result.evidence` wrapper instead of at the top level, retaining the same id and requested verb. Expected under the same fail-closed duplicate-member rule: exit **2**. This checks the nearby nested representation; it was not exercised.

## Residual risk and verification gaps

- Scope is this one frozen C1 case only. No other C1 case, C2 case, full battery, or broader duplicate-member position was exercised.
- The run checks this local binding predicate only; it does not establish Evidence authenticity or cryptographic verification.
- The C2 stub was inert and unused because this is a C1-only invocation. No C2 behavior is claimed.
- No tools were installed or updated. No production or fixture file was changed.

Report: `.ufo/waves/round-21/w2/R21Attack12.md`
