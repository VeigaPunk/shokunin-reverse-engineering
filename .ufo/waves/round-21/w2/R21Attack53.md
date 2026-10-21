# R21Attack53 — `compare-wasm-interfaces` retained witness

**Axis:** depth. **Finding:** supported local record binding; not cryptographic authentication.

## Observed

- The cited knowledge entry is `corpus/knowledge/2026-10-20-r20-wasm-interfaces.md:24`. It names the **synthetic v1→v2 WAT modules built with WABT `wat2wasm`** and cites output Evidence ID `ev_2529e50816c83bb2f37c596678299e223a27ccca696672596a847397ada43351`.
- Independently read the retained JSON witness at `.ufo/waves/round-20/evidence/c2/wasm-compare/compare-synth-both.stdout.txt`. Its top-level `operation` is `compare_wasm_interfaces`, its top-level `evidence_id` is exactly the knowledge-entry ID, and `scope` is `both`. The summary is 1 added, 1 removed, 1 changed, 1 unchanged, 0 unknown. The two IDs inside `parameters` (`ev_6ff4…` and `ev_29d6…`) are the **input** inspection IDs, not the comparison output ID.
- `.ufo/waves/round-20/evidence/c2/wasm-compare/compare-synth-both.receipt.json` records the R20 `rea-agents@6.5.0 compare-wasm-interfaces` invocation, exit 0, stdout SHA-256 `6859943b5f2b4377c77b9a1ed57ad1f88b53bbced56185c39ccc7beea1f92e67`, and synthetic carrier paths/digests: `synth/v1.wasm` (75 bytes, `a072e4d9…`) and `synth/v2.wasm` (84 bytes, `df410091…`).
- **Synthetic/pathless scope:** this is the synthetic pair, not a real-carrier comparison. The comparison record has top-level `subject: null`; per-input artifact paths remain nested in `normalized_result`. The validator therefore reports `pathless: true` for the comparison record.

## Assigned validator

The specified command was first invoked directly; to retain exit and both streams, the identical command was invoked again with stdout/stderr capture:

```text
argv: ["python3", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/verb-coverage.py", "--evidence", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/evidence/c2/wasm-compare/compare-synth-both.stdout.txt", "--verb", "compare-wasm-interfaces", "--evidence-id", "ev_2529e50816c83bb2f37c596678299e223a27ccca696672596a847397ada43351"]
exit: 0
stdout: {"bound": true, "finding": "evidence_bound", "pathless": true}
stderr: (empty)
```

## Confidence and remaining gap

High confidence that the retained JSON record locally binds this exact comparison operation to the cited output ID. The check explicitly does not authenticate the record cryptographically; no provider or carrier was executed in this check, and this synthetic witness does not establish behavior on real carriers.