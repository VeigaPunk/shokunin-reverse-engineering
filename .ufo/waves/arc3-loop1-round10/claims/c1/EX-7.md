# EX-7 — C1 coverage: Paris-target Vyper dispatch draft

## Claim and boundary

I selected the still-open Vyper EVM-target/hardfork Unknown for the synthetic `K8.vy` fixture. The prior r8 entry explicitly leaves other EVM targets unmeasured (`corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:15`); the r4 entry also names other hardfork variants as unknown (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28`). This artifact closes only the exact K8 source compiled by Vyper 0.4.3 for `--evm-version paris -O gas` on this host. It does not claim a general Paris/Vyper rule.

**Corpus entry draft:** `claims/c1/EX-7/evidence/draft-corpus-entry.md`  
**Proposed destination:** `corpus/knowledge/2026-10-19-arc3-r10-vyper-paris-dispatch-shape.md`  
**Proposed map token:** `2026-10-19-arc3-r10-vyper-paris-dispatch-shape` on the EVM row. No corpus or README edit was made; integration and the post-landing count remain parent work.

## First-hand re-derivation

The replay script is `claims/c1/EX-7/evidence/rederive.sh`; it uses only the existing Vyper venv and locally cached REA 6.7.0 package, with compile and REA `TMPDIR` under `/var/tmp`. `identity.txt` records current `HEAD=5694506a862c32d2f7aac44935778bce4b6184f2`, exact compiler/package identity, and matching hashes for the source copy. The source is SHA-256 `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`; Vyper is `0.4.3+commit.bff19ea2`, executable SHA-256 `615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10`.

`bash .ufo/waves/arc3-loop1-round10/claims/c1/EX-7/evidence/rederive.sh` compiled two Paris/gas runtime passes; `cmp` succeeded. Fresh `paris.settings.json` says `{"optimize":"gas","evm_version":"paris","experimental_codegen":false}`. The generated runtime is 423 decoded bytes, SHA-256 `d1af44a952ac9775dd45eae83e2f4d167d311f9f7f3db8bf762592eb979060d2`; the REA hex input file SHA-256 is `0f0bcb57b2aa7e2e06e2c47864564af4b4d57af76b005f9901c3df9088145629`.

`measurement.txt` is generated from the fresh ABI/method identifiers, runtime bytes, and REA envelope; exact key output:

```text
ABI_FUNCTIONS=8 METHOD_IDENTIFIERS=8
ABI_METHODID_REA_NORMALIZED_REA_RAW_SELECTOR_SETS_EQUAL=True
PUSH4_SITES=8 PUSH4_SELECTORS_ONLY=True
REA_ROWS=8 RAW_ROWS=8 DISPATCH={'abi': 8}
REA_DECODED_SHA256_MATCH=True
TABLE_OFFSET=0x195 TABLE_BYTES=18 BUCKETS=9 TABLE_HEX=018a018a0100012e00a4001a018a015c0076
BUCKETS_MATCH_SELECTOR_MODULO=True EMPTY_BUCKETS=3
```

Byte walk: `measurement.txt` records the header instructions and each table bucket. The code extracts the top nine two-byte entries at `0x195`, validates the `PUSH4; DUP2; XOR; PUSH2; JUMPI` compare pattern, and confirms the bucket contents equal each compiler selector modulo 9. Eight opcode-boundary `PUSH4` immediates equal the eight compiler method identifiers; the comparator uses eight `XOR` and zero `EQ`. REA offsets all land on `PUSH1` boundaries (handler fall-throughs), as listed in that measurement output.

REA call: `inspect-evm-interface` on `evidence/paris.runtime.hex` (`hex`), direct local `rea-agents@6.7.0`; provider `evmole-interface`, `evmole@0.9.3`. Evidence ID `ev_bdc9dd365b9d7cdb09efa5f962b20eea56a4f51a471a617ce8e48a241e51f091`; full envelope `paris.rea.json`. It labels discovery completeness `unknown`, runtime execution `not-performed`, hardfork/kind/deployment authenticity `unknown`. The EVM target here is established by the fresh compiler settings, not REA metadata.

## Per-item verdicts

- **Unknown scope — VERIFIED:** the cited r8/r4 corpus lines leave the EVM target/hardfork leg open; this run measures only Paris for the named K8/compiler/optimizer combination.
- **Source/compiler/settings — VERIFIED:** current source and compiler hashes in `identity.txt`; Paris target and gas optimizer in `paris.settings.json`.
- **Compilation — REPRODUCED:** two fresh bytecode outputs compared equal; 423 decoded bytes and digest above.
- **REA selector recovery — REPRODUCED:** 8/8 raw and normalized rows, `dispatch:"abi"`; exact match to freshly generated method identifiers and decoded-bytecode SHA-256 (`measurement.txt`, `paris.rea.json`).
- **Dispatcher structure — REPRODUCED:** the 9-entry modulo-indexed table and XOR compare chains were independently decoded and checked against compiler selectors (`measure.py`, `measurement.txt`).
- **Command A baseline — VERIFIED:** reran the `SCORECARD.md:88-124` source-derived recipe at `5694506a862c32d2f7aac44935778bce4b6184f2`; `evidence/command-A-before.json` reports `knowledge_files=88`, `mapped=88`, `missing=[]`, `dangling=[]`, `rule_blocks=15`, `citation_resolved_rules=15`. If the draft and token are both integrated, 89/89 is only a projection; post-integration measurement is **UNVERIFIABLE here** because this seat may not edit `corpus/` or `README.md`.

No discrepancy found in this scoped re-derivation. This seat changed no tracked file and performed no Git mutation. Read-only status showed `.ufo/waves/arc2-loop1-round10/C3.md` modified both before this work and at the final check; that unrelated pre-existing change was left untouched.
