# R21Attack10 — C1 `objdump_wrong_parameter`

## Finding by severity

**No actionable finding for the assigned frozen case.** The successor returned the independently frozen expected failure exit.

## Frozen contract and observed run

- `fixtures/battery.json`, C1 case `objdump_wrong_parameter`: expected exit **1**. The exact evidence has the requested record id and `operation: "inspect_with_objdump"`, but `parameters.operation` is `"disassemble"`; `"architectures"` appears only in `notes`.
- `fixture-contract.json`, C1 `objdump_wrong_parameter`: independently specifies expected exit **1** and rule: “inspect_with_objdump record disassemble, architectures only unrelated prose.” The battery and contract agree.
- Successor: `.ufo/waves/round-21/tools/verb-coverage.py`, SHA-256 `77db29fde196c2a0db19a522d21cf8bf315a383250c7115fda71f04bd141e2cc`.
- Frozen evidence SHA-256: `0535e34dc5cca70dafebe5380a896322e692d1bc756a1830a461f3b92a91d23a`.
- Actual CLI argv (the temporary evidence path was removed after the run):

```text
["/usr/bin/python", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/verb-coverage.py", "--evidence", "/tmp/r21attack10-c1-qsvez154/evidence.json", "--verb", "list-objdump-architectures", "--evidence-id", "ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"]
```

- Expected exit: **1**. Observed exit: **1**.
- Exact stdout: `{"bound": false, "finding": "evidence_unbound"}\n`
- Exact stderr: empty.
- External temporary directory removed: **yes**.
- Interpreter: Python **3.14.8**.

In `bind()`, the successor maps this verb to `inspect_with_objdump`, requires the exact evidence id and operation, and additionally requires `parameters.operation == "architectures"`. This record therefore yields no matching binding; its prose note does not satisfy the parameter predicate. `evidence_unbound` / exit 1 matches the frozen contract.

## Nearby counterexample — UNRUN

An otherwise matching positive record with `parameters.operation: "architectures"` and `status: "ERROR"` may be accepted: `refused()` recognizes only exact values from its refusal set, which includes lowercase `error` and `VALIDATION_ERROR` but not uppercase `ERROR`. This is a source-derived, unexercised probe, and only matters if `ERROR` is a valid refusal status in the producer’s contract; that vocabulary was not established here. No extra case was run.

## Residual risk and verification gaps

- Scope was one frozen C1 case only. No other battery case, C1 positive control, C2 comparator case, or battery-wide run was executed.
- The battery dispatcher uses the C1 `verb-coverage.py --evidence ...` branch; the inert `--extractor` stub is created only in its C2 branch. This C1 CLI has no extractor argument, so no extractor stub was created or passed. No C2 successor was run.
- No provider call or analyzed-carrier execution occurred. No installation/update was needed.
- The `lsp` device is unavailable (`read xd://lsp` returned “No such tool”), so status/references/definition/diagnostics could not be requested. A literal search located the battery dispatcher; the relevant dispatch block was then read directly in `battery.py`. No grep result is treated as semantic proof.
- This scoped run establishes only the observed behavior of the named successor/case; it does not establish broader refusal-vocabulary completeness or cryptographic evidence authentication (the successor itself describes its binding as local, not cryptographic).
