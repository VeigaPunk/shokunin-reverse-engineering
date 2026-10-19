# EX-8 — C2 coverage: viaIR final selector miss with a fallback

**Verdict: REPRODUCED**, narrowly. This seat re-derived the r6 residual in `corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md:30`: “viaIR carriers with `fallback()` (this carrier has none; the SUB-leg/fall-through interaction with a real fallback is unmeasured).” The measurement closes only that question for the synthetic `ViaIrVault` source pair, solc 0.8.37, `viaIR: true`, optimizer enabled with 200 runs. The control and fallback-bearing source compile to byte-distinct runtimes; the opcode walk shows how the same selector-miss target resolves in each. It is static evidence, not runtime execution.

## Re-derived result

- Compiled both source copies twice with `0.8.37+commit.f401782d.Emscripten.clang`, using the existing read-only solc prefix. `soljson.js` SHA-256: `221d7a667378b5068d913e75fe092507e061363cd1d23b64c49ae82febabad4c`. Settings: viaIR on, optimizer on, 200 runs. Each repeat matched its runtime and ABI byte-for-byte (`evidence/compile/compile-summary.json`).
- No-fallback source SHA-256: `f53911672f2e33eaabaeff85e75c2565bb2899638d194fb3ffe6747abe80cbbe`; runtime 1,517 B, SHA-256 `2ec3f557f6f2fb229dc49094981723c6efcce3df10f20363ec1732845c99581a`.
- Payable-fallback source SHA-256: `9c5c2d461bc2a3142984c6adb0f2082d3d3fd8ec3753105d3342bef812b51e6d`; its only added body is `fallback() external payable { fee_ += msg.value; }`; runtime 1,525 B, SHA-256 `a064b8de5b7d0aa924980f21df768e9338d41678d9e04bb0acebe8dcd029968d`.
- `inspect-evm-interface <runtime.hex> hex --format json` on both carriers returned 15 functions in raw and normalized results. Each 15-selector set matched the compiler ABI/method identifiers exactly; decoded-bytecode SHA-256 matched that variant’s runtime. Provider `evmole-interface` / `evmole@0.9.3`, rea-agents 6.7.0. Full envelopes and selector/digest checks: `EX-8/evidence/probe/{no-fallback.json,payable-fallback.json,verification.txt}`; calls and exit/size summary: `EX-8/evidence/probe/calls.txt`.
- The independently decoded opcode walk found 14 `EQ` selector legs and one final `SUB` leg (`ee02438e`) in both runtimes. The SUB mismatch branch targets PC `0x0e` in both (`EX-8/evidence/compile/dispatch-walk.txt`). In the no-fallback runtime, a nonempty unknown selector reaches that target and falls through to `PUSH0; DUP1; REVERT`. In the payable-fallback runtime, the same target tests calldata length and routes nonempty calldata through `CALLVALUE`, `SLOAD` slot 2, then `SSTORE` slot 2; this corresponds to the added fallback body. Empty calldata branches separately to the receive path. This last behavior description is a static control-flow inference from the source and bytecode, not an executed call.

REA evidence IDs for the exact calls: no-fallback `ev_a1a3f8282018daebc196d89c33ebf9329815ba0a4dddf12ef59077fdcc122482`; payable-fallback `ev_fba6be036c420d04f02b4379c50741010415e764017e190fcb65a2e603ca3019`. They identify these calls and paths only; this report makes no cross-path evidence-ID stability claim.

## Draft corpus entry and proposed map patch

- Corpus-entry draft: `.ufo/waves/arc3-loop1-round9/claims/c2/EX-8/evidence/draft-corpus-entry.md`.
- Proposed destination: `corpus/knowledge/2026-10-19-arc3-r9-viair-fallback-miss.md`.
- Proposed token: `2026-10-19-arc3-r9-viair-fallback-miss`.
- The following line-neutral replacement is patch text only; neither `corpus/README.md` nor `corpus/knowledge/` was changed by this seat:

```diff
-| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-evm-optimizer-shapes`, `2026-10-19-arc3-r4-evm-vyper-leg`, `2026-10-19-arc3-r6-viair-dispatch-shape`, `2026-10-19-arc3-r7-evm-evidence-id-domain`, `2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07) and from real solc-0.8.37-compiled runtime carriers (arc3-r1); positional encoding quirk |
+| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-evm-optimizer-shapes`, `2026-10-19-arc3-r4-evm-vyper-leg`, `2026-10-19-arc3-r6-viair-dispatch-shape`, `2026-10-19-arc3-r7-evm-evidence-id-domain`, `2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes`, `2026-10-19-arc3-r9-viair-fallback-miss` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07) and from real solc-0.8.37-compiled runtime carriers (arc3-r1); positional encoding quirk |
```

## Command A and scope

Command A was re-run on immutable HEAD `947091d6b6f52684faf9ca53adf94ff8a0f6b006`, before integration. Exact output (`EX-8/evidence/command-A-before.txt`):

```text
{"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 87, "mapped": 87, "missing": [], "revision": "947091d6b6f52684faf9ca53adf94ff8a0f6b006", "rule_blocks": 15}
```

The corpus draft plus token are expected to bring the index to 88/88 if both are integrated; **that is a projection, not a measurement**. The integrator must freshly run Command A at the integrated revision and record its output. No post-integration result is claimed here.

The recheck recipe and scope limits are in the draft. All seat evidence and generated files are under `.ufo/waves/arc3-loop1-round9/claims/c2/EX-8/`; this report is the required seat artifact. No corpus, index, gate, project-source, other-seat, or Git changes were made. The pre-existing dirty `.ufo/waves/arc2-loop1-round10/C3.md` was left untouched.
