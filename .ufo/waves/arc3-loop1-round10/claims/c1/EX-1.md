# EX-1 — C1 corpus Unknown: Vyper EVM target pair

## Finding

**Chosen Unknown:** explicit Vyper hardfork target variation for K8 was not characterized in the r8 entry, which lists other EVM targets as outside its evidence (`corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:15`). This seat freshly compared `cancun` and `paris` using the same synthetic source, Vyper 0.4.3, and `-O gas`.

**Bounded verdict: VERIFIED for this fixture and target pair.** Eight compiler-derived selectors are recovered by REA on both fresh runtimes; all REA offsets reconcile to an independent opcode-boundary walk. Cancun and Paris have distinct runtime code layouts: total runtime grows 418→423 bytes, executable code 400→405 bytes, the 18-byte jump table stays the same size, and each selector offset and table destination moves by +2. This does not generalize to other source shapes, optimizer options, targets, compiler versions, or deployed behavior.

**Corpus integration: pending.** Copy-ready entry and EVM coverage-map token are drafted in `evidence/entry-draft.md`. No `corpus/knowledge/` or `corpus/README.md` edit was made; no after-landing Command A result is claimed.

## First-hand re-derivation

- Copied K8 source SHA-256: `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`; Vyper `0.4.3+commit.bff19ea2`, executable SHA-256 `615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10` (`evidence/vyper/identity.txt:1-6`). The re-derive script rebuilt both targets twice and compares each pair byte-identically; the full script, fresh REA calls, opcode outputs, and verifier all completed with exit 0 (`evidence/vyper/reproduction.txt:1-21`; `evidence/vyper/run-status.txt:1`). Scratch is under `/var/tmp/kaidoku-ex1-vyper-r10`, not `/tmp`.
- Cancun runtime: 418 bytes / SHA-256 `72e5d886da7ccaf633b957738456323e22043275092e001fbc06847b57b06814`; code ends at 400 and table is 18 bytes at offset 400. Paris runtime: 423 bytes / SHA-256 `d1af44a952ac9775dd45eae83e2f4d167d311f9f7f3db8bf762592eb979060d2`; code ends at 405 and table is 18 bytes at offset 405 (`evidence/vyper/verification.json:44-64,267-287`). The selector-modulo-9 prologue scales by two and `CODECOPY`s one table entry; all nine 16-bit big-endian entries in each target point to independently walked `JUMPDEST`s. The trailing table was not decoded as opcodes or assumed to be Solidity CBOR.
- Compiler ABI/method identifiers and opcode-boundary `PUSH4` sites match the eight REA selectors on both targets; all eight compare legs have shape `PUSH4; DUP2; XOR; PUSH2; JUMPI`. REA's eight byte offsets all equal the independent fallthrough after that sequence, and every corresponding Cancun→Paris delta is +2 (`verification.json:121-258,345-484`). Full evidence IDs: Cancun `ev_a0de67e1037b7dcdf9d32e9a49a38e225830f0c4d8c384c7503de224870ea83a`; Paris `ev_bc35619673cc8e22dd065ad7f21cb5d1317e51626e63d8966c57526cd0c8fff5`.
- The compiler ABI says `view`; REA infers `payable`. The latter is explicitly an upstream inference, not treated as fact. Both probe envelopes report `discovery_completeness=unknown` and `runtime_execution=not-performed`; no execution, deployment attribution, chain/RPC lookup, or network request is claimed.

## Command A baseline and exclusions

Command A, following `SCORECARD.md:88-124`, was freshly measured against revision `5694506a862c32d2f7aac44935778bce4b6184f2`: `knowledge_files=88`, `mapped=88`, `missing=[]`, `dangling=[]`, `citation_resolved_rules=15`, `rule_blocks=15` (`evidence/command-A-before.json:1`). The frozen C1 contract expects the eventual corpus+map landing to move 88→89 (`.ufo/waves/arc3-loop1-round10/claims-frozen.md:16-29`); that after-state is expected, not measured. This artifact-only draft does not change corpus counts.

A separate solc 0.8.28 exploration exists in this EX-1 evidence directory but is excluded from the chosen finding: the frozen task explicitly notes that 0.8.28 ViaIrVault was already characterized at r9 (`.ufo/waves/arc3-loop1-round10/claims-frozen.md:18-20`). The selected C1 move is solely the previously open Vyper EVM-target pair.

## Per-item verdicts and boundary

- Cancun/Paris explicit target comparison for K8 / Vyper 0.4.3 / `-O gas`: **VERIFIED** by fresh builds, fresh REA calls, and independent byte walk.
- Repeat-build stability: **VERIFIED** for each target (`cmp` passed twice per target).
- REA selector and offset reconciliation: **VERIFIED**, 8/8 selectors per target and 8/8 offsets per target; all 13 checks pass on each.
- Command A before: **VERIFIED**, 88 files / 88 mapped at the recorded revision. Command A after integration: **UNMEASURED**; parent integration must land both entry and token and rerun the command.
- Other Vyper sources/targets/settings/versions, deployment identity, completeness of REA discovery, and runtime execution: **UNKNOWN / not established**.

No `corpus/`, README, SKILL, PROVINCE, SCORECARD, LOG, gate, or peer-seat artifact was edited. Persistent work and evidence are contained under `.ufo/waves/arc3-loop1-round10/claims/c1/EX-1/`.
