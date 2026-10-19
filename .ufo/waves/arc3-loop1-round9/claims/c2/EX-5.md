# EX-5 — C2 corpus coverage

**Chain:** c2 (coverage). **Selected Unknown:** solc versions other than 0.8.37 under `viaIR`, named in `corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md:30`.

## Findings and verdicts

- **Alternate compiler measurement — REPRODUCED.** Recompiled the supplied `ViaIrVault.sol` source (fresh source SHA-256 `f53911672f2e33eaabaeff85e75c2565bb2899638d194fb3ffe6747abe80cbbe`) with solc 0.8.28, optimizer enabled/runs=200 and `viaIR=true`. Runtime: 1,517 bytes, SHA-256 `3f28f35ea804ce431cca75f3c2b6602aaeaf17938f4d4a773654e19a95f07967`; creation: 1,560 bytes, SHA-256 `e25a51428510bf212744962909d658d37e447ac245498294e0f08cc0269c38f3`. Exact compiler stdout: `evidence/compile/solc-0.8.28/compile-output.jsonl:1`.
- **Selector recovery — REPRODUCED.** A first-hand REA 6.7.0 `inspect-evm-interface` call on the fresh 0.8.28 runtime returns 15 selectors; all match ABI-derived selectors and the decoded SHA-256 equals the compiled runtime (`evidence/probe/solc-0.8.28/viair-opt200.json:1`, Evidence ID `ev_ac9382b85ef15d7cde9195af11b984c0c7f99b2ee3a03b2f996e2ab84164ae0b`). Byte-level decode: inverted `LT; ISZERO` guard, 14 `EQ` plus final `SUB`, selector set sorted; exact measurements are in `evidence/byte-characterization.json`.
- **Version comparison — REPRODUCED.** A newly compiled 0.8.37 control from the identical source and settings has the same 1,517-byte length and byte-identical pre-metadata region `[0,1464)` (SHA-256 `34a46554c003760ddc41c3e7c2ec94cdc08b0d162a75a763d6f06c49ed03ed15`); only metadata differs. The alternate version therefore does not introduce a different dispatcher shape for this fixture. A 0.8.28 non-viaIR control has the distinct `LT` guard and 15 `EQ` / 3 `GT` compare sites over 15 selectors; REA also returns 15 matching rows.
- **Command A before measurement — VERIFIED.** At immutable HEAD `947091d6b6f52684faf9ca53adf94ff8a0f6b006`, output was `knowledge_files=87, mapped=87, missing=[], dangling=[]` (`evidence/commandA-baseline.json:1`).
- **Post-landing corpus/map count — UNVERIFIABLE by this seat.** The knowledge entry is a draft and the EVM map is protected by the assignment. A landing that adds exactly one new `.md` entry and its map token should measure 88/88; that must be confirmed by the integrator after landing.

## Deliverables

- Corpus knowledge draft: `entry-draft.md` (proposed token `2026-10-19-arc3-r9-solc-028-viair-dispatch-shape`).
- Full compile/REA outputs, byte census scripts, identities, source copy and exact reproduction notes: `EX-5/evidence/`.
- No `corpus/`, `README`, `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, gate source, or other custody path was modified. All scratch was under `/var/tmp`.
