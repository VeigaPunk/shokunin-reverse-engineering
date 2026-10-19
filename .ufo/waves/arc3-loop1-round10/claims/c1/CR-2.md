# CR-2 — C1 coverage: Vyper EVM-target variant

**Disposition:** a bounded, evidence-backed corpus-entry draft is provided at `claims/c1/CR-2/evidence/entry-draft.md`. It tests the named Vyper hardfork/EVM-target Unknown with a fresh London-versus-Prague compile of the same retained K8 synthetic source. Frozen assignment: C1 is the corpus-Unknown chain and CR-2 maps to c1 (`claims-frozen.md:16-29,67-71`).

## Per-item verdicts

- **Candidate Unknown — VERIFIED.** The frozen C1 options explicitly name a Vyper hardfork/target variant (`claims-frozen.md:22-24`); the r4 entry records uncharacterized hardfork dispatcher forms alongside remaining Vyper version/dispatcher-form Unknowns (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28`), while the r8 draft scopes its work to optimizer forms and does not compare EVM targets (`corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:7-17`). This artifact addresses only the target-variant slice.
- **Source/compiler identity — VERIFIED.** `K8.vy` source and seat copy hash to `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d` and `cmp=0`; Vyper executable hash is `615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10`, version `0.4.3+commit.bff19ea2` (`evidence/reproduction.txt:3-8`).
- **Compile reproducibility — REPRODUCED.** Two runtime builds each compare byte-identically for Prague and London (`evidence/reproduction.txt:10-12`). Settings confirm gas optimization with explicit targets (`evidence/measurement.txt:1,13`). Runtime bytes are Prague 418 / London 423, with distinct SHA-256 identities (`evidence/measurement.txt:2,14`).
- **Selector recovery — VERIFIED.** Independent ABI-signature Keccak derivation (known-vector PASS) matches Vyper method IDs and the Prague/London sets (`evidence/keccak-check.txt:1-8`). REA returned 8 raw + 8 normalized rows per target, all `dispatch:"abi"`, selector-set match and decoded-bytecode SHA match (`evidence/measurement.txt:5-7,17-19`; raw envelopes under `evidence/probe/`).
- **Dispatcher target comparison — VERIFIED.** The byte walk verifies a modulo-9 dispatcher with 9 two-byte table entries, selected-entry `CODECOPY` to `0x1e`, then `MLOAD/JUMP`; all 9 table targets in both builds point at `JUMPDEST`. Eight selector `PUSH4` sites each use `DUP2; XOR; PUSH2; JUMPI`. The selector set/buckets agree, while table base and target offsets differ across EVM targets (`evidence/measurement.txt:8-12,20-24`).
- **Command A baseline — REPRODUCED.** Re-ran the Scorecard recipe (`SCORECARD.md:88-124`) on work commit `eb5a2c4`; exact JSON is preserved at `evidence/command-a-before.txt:1-8`: `knowledge_files=88`, `mapped=88`, `missing=[]`, `dangling=[]`, `rule_blocks=15`, `citation_resolved_rules=15`.
- **Generalization and post-landing count — UNVERIFIABLE.** No other compiler version, EVM target, source shape, non-gas optimizer under London, or deployed runtime was tested. The draft/map token has not been integrated, so 89/89 is an expected landing check only, not an observed count.

## Integration boundary

The draft proposes `corpus/knowledge/2026-10-19-arc3-r10-vyper-hardfork-targets.md` and EVM-map token `2026-10-19-arc3-r10-vyper-hardfork-targets`. No corpus file or map row was changed. Integrator must copy the draft, add the map token, then rerun Command A at the landing revision; do not report 89/89 before that check.

Evidence and reproduction are under `claims/c1/CR-2/evidence/`; `bash .ufo/waves/arc3-loop1-round10/claims/c1/CR-2/evidence/reproduce.sh` rebuilds/reprobes the pair and writes the exact transcript/results. Command A baseline output is `evidence/command-a-before.txt`.

Git remained read-only. The initial and final `git status --short` both showed the pre-existing `M .ufo/waves/arc2-loop1-round10/C3.md`; it was not touched. All new files from this seat are within this CR-2 artifact directory; scratch was placed under `/var/tmp`.
