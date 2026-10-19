# CR-2 — c2 coverage seat

Chain: c2 (corpus Unknown). Selected the residual Vyper optimizer-form boundary: whether `--no-optimize` and `-O none` have any remaining byte-level distinction on the pinned K8 fixture. The source file was copied into my scratch from the existing fixture, then freshly hashed, compiled and REA-probed; prior-round output values are not used as evidence.

## Findings and per-item verdicts

- **Compiler output boundary — REPRODUCED.** Fresh Vyper 0.4.3 runs with both options produced byte-identical `bytecode`, `bytecode_runtime`, `abi`, `method_identifiers`, and `settings` outputs (`cmp -s` passed for every pair). Decoded creation bytecode: 687 bytes, SHA-256 `b09398d8eb89f1ec1a73de9cbec27a54ce79d185094a4253a384cfffe62e2598`; decoded runtime: 617 bytes, SHA-256 `1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc`. Both settings objects read `optimize: none`, `experimental_codegen: false`; each ABI and method-identifier object has eight entries. Full measured command/output transcript: `CR-2/evidence/rederive.txt`.
- **REA cross-check — REPRODUCED.** Pinned `rea-agents@6.7.0` / `evmole@0.9.3` returned 8 raw and 8 normalized rows per runtime, all `dispatch:"abi"`; both returned the same eight selectors and decoded runtime SHA-256. Full envelopes: `CR-2/evidence/rea-noopt.json` and `CR-2/evidence/rea-none.json`. The IDs are separate run records; the comparison is on compiler bytes, decoded SHA-256 and function payload, not on evidence-ID equality.
- **Scope beyond this fixture — UNVERIFIABLE.** The result covers exactly the copied K8 source bytes (SHA-256 `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`) and the local Vyper executable (SHA-256 `615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10`, version `0.4.3+commit.bff19ea2`). It does not prove equivalence for other sources or compiler versions. REA reported `confidence=inferred`, `discovery_completeness=unknown`, and `runtime_execution=not-performed`; no deployed-contract identity is claimed.
- **Corpus landing / after-count — UNVERIFIABLE pending integration.** The ready-to-land draft is `CR-2/entry-draft.md`, proposing `corpus/knowledge/2026-10-19-arc3-r9-vyper-noopt-alias-boundary.md` and coverage token `2026-10-19-arc3-r9-vyper-noopt-alias-boundary`. Command A was run read-only at frozen base `947091d6b6f52684faf9ca53adf94ff8a0f6b006`; exact output is in `CR-2/evidence/command-a-before.json`: 87 knowledge files / 87 mapped, `missing: []`, `dangling: []`. The draft and map token have not been integrated, so the required post-landing 87→88 result is not claimed and remains for the integrator to verify.

## Deliverable and scope

- Corpus-entry draft: `CR-2/entry-draft.md`.
- First-hand inputs, both compiler-output sets, both complete REA JSON envelopes and transcript: `CR-2/evidence/`.
- Scratch stayed under `/var/tmp/kaidoku-cr2-r9.h4dc2U`; no `/tmp` use. No corpus, coverage map, tracked file, gate, or custody path was edited. Git was used read-only.
