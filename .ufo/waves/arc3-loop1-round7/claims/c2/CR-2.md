# CR-2 — c2 coverage Unknown: Vyper optimizer forms

## Claim and chosen Unknown

Chosen item: characterize the Vyper `--no-optimize` and `-O codesize` dispatcher forms left as an Unknown in `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28`. This is a byte-level re-derivation on Vyper 0.4.3, not an extension to other versions or arbitrary contracts. The prior entry was used only to locate the Unknown and fixture; every runtime, selector count, hash, probe result, and offset below was freshly derived by this seat.

## Work and evidence

- In `/var/tmp/kaidoku-cr2-r7-c2/`, I freshly compiled the copied eight-function `K8.vy` with Vyper `0.4.3+commit.bff19ea2` under `-O gas` (default), `--no-optimize`, and `-O codesize`; executable SHA-256 `615f792c…`, source SHA-256 `62549f79…`. Exact commands and full hashes: `evidence/reproduction.txt`.
- Ran three real `npx -y rea-agents@6.4.0 inspect-evm-interface … hex --format json` calls against the retained compiled runtimes. All three returned 8 rows / 8 unique selectors, zero missing/extra vs their fresh compiler `method_identifiers`, and decoded-byte SHA-256 equal to the respective runtime; evidence IDs and raw JSON: `evidence/probe-{gas,noopt,codesize}-6.4.0.json` and `evidence/reproduction.txt`.
- Independently decoded the retained bytecode and compared probe offsets in `bytecode-characterize.py`; output `bytecode-characterization.jsonl:1-3`. Results: `-O gas` has 8 `PUSH4/DUP2/XOR/PUSH2/JUMPI` legs and offset delta +11; `--no-optimize` has 8 `PUSH4/DUP2/EQ/ISZERO/PUSH2/JUMPI` legs and delta +12; `-O codesize` has 0 opcode-boundary `PUSH4`, the `PUSH1 05 / PUSH2 012b / PUSH1 1b / CODECOPY` window at PCs 5/7/10/12, and all eight selector byte strings in the tail starting at 0x12b. All codesize REA rows report offset 65 (`DUP1`).
- Re-ran Command A from `SCORECARD.md:88-124` at work revision `2fba56f`: `{"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 85, "mapped": 85, "missing": [], "revision": "2fba56f", "rule_blocks": 15}`. Full result: `evidence/reproduction.txt`.

## Per-item verdicts

- `--no-optimize` dispatch shape and K/K: **REPRODUCED**. All eight compiler selectors are recovered; the bytecode carries an EQ/ISZERO chain, distinct from the default gas XOR chain.
- `-O codesize` dispatch shape and K/K: **REPRODUCED**. All eight compiler selectors are recovered from a runtime with no opcode-boundary PUSH4 selector immediates; the observed selector bytes are in the code tail referenced by the table-copy prelude.
- Generalizing the Form-A `PUSH4_pc + 11` offset rule: **DISCREPANCY**. It holds for this freshly compiled gas control, but no-optimize is +12 and codesize reports one shared offset (65) for all eight selectors. These results narrow the rule; they do not establish a universal offset formula.
- Command A baseline: **VERIFIED**, 85 files / 85 mapped, no missing or dangling tokens at `2fba56f`.
- Command A after landing, 85→86: **UNVERIFIABLE in this seat**. The corpus entry and map token must remain a draft under the frozen write scope; I did not edit `corpus/knowledge/` or `corpus/README.md`. Do not record 86/86 until an integrator lands both and reruns Command A at that revision.

## Draft deliverable and boundary

The proposed knowledge entry is `evidence/entry-draft.md`; token: `2026-10-19-arc3-r7-vyper-optimizer-forms`, for addition to the EVM row at `corpus/README.md:38`. It states source/runtime identities, exact REA calls and Evidence IDs, observation/inference boundaries, and untested scope. `corpus/QUALITY.md:14-22` constraints are reflected in the draft. The draft is deliberately not counted as a landed corpus file.
