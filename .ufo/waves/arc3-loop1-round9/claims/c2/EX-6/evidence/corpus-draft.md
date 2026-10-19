<!-- DRAFT for parent integration only. Proposed destination: corpus/knowledge/2026-10-19-arc3-r9-viair-fallback-dispatch.md. Proposed EVM-map token: 2026-10-19-arc3-r9-viair-fallback-dispatch. No corpus or index edit was made by this seat. -->

# Solc 0.8.37 viaIR selector dispatch with payable fallback — draft

source: `.ufo/waves/arc3-loop1-round9/claims/c2/EX-6/evidence/` (`ViaIRFallback.sol`; `compile.js`; `identities.txt`; `out-a/` + `out-b/`; `probe.json`; `walk.txt`)
verified-at: 2026-10-19

## Result

This entry closes the specific r6 unknown about the `SUB`-terminated final selector leg interacting with a real `fallback()` (`corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md:30`), bounded to the synthetic source, solc-js `0.8.37+commit.f401782d`, viaIR, and optimizer runs 200 measured here. It does not generalize to other sources, compiler releases, settings, or EVM targets.

The fresh compiler ABI has three ordinary external functions (`alpha()`, `load()`, `store(uint256)`), a payable fallback, and a payable receive entry. Two separate standard-JSON compilations were byte-identical: runtime 366 B / SHA-256 `2948d578ae460119f777eb379febc2738dbec14d03c76d5f100777c9552ce6fc`; creation 392 B / `a24cb1651e78dd159425d5b27c9ba513b50b0401f5bcf3589f259b0a70d0ba9e` (`compile-a.txt`, `compile-b.txt`, `compile-compare.txt`). The source SHA-256 is `615edcdecab9a6b3b4d9b6965c416406f133d43b1144eb2e13985bf17580f11a`; the compiler and dependency identities are in `identities.txt`, and both complete inputs and outputs are retained under `out-a/` and `out-b/`.

## REA result and byte walk

A fresh `inspect-evm-interface` hex call at local `rea-agents@6.7.0` / `evmole@0.9.3` returned the same three selectors as the compiler method identifiers: `6057361d`, `86d5c4be`, `db1d0fd5`. It returned three function rows and no fallback/receive rows; decoded bytecode SHA-256 is the compiled runtime SHA-256 above. Evidence ID: `ev_5272b1d8547672b56597c8aaccc6cf675675d128ace33cb3e590545feae1bddd` (`probe.json`; command exit 0 in `probe-exit.txt`). The normalized carrier is the 733-byte hex text file, SHA-256 `4736cecce7f1977a80f9401bcce111bf2b78b65e9f1f31397b2327dff0d3488f`; the decoded runtime is 366 bytes. The three selector matches are observations about this compiled input. REA marks the result inferred, `discovery_completeness=unknown`, and `runtime_execution=not-performed`; it does not establish general completeness or execution.

The independent opcode-boundary decode (`walk.txt`) finds the three dispatch immediates at PCs `0x99`, `0xa4`, `0xae`. The last leg is `PUSH4 0xdb1d0fd5; SUB; PUSH2 0x000e; JUMPI`: a nonmatching selector branches to `0x000e`, where empty calldata branches to the receive path at `0x0087`, and nonempty calldata proceeds through the fallback body; a matching final selector falls through to `0x00b8` (decimal 184), the offset REA reports for `alpha()`. This is a static control-flow inference corroborated by the compiled source/ABI and bytes, not an executed call. The opcode walk excludes the 51-byte CBOR metadata trailer; its executable prefix is 313 B, matching REA's `bytecodeOffset=313` / `cborLength=51`. Five opcode-boundary `PUSH4` sites in that prefix include two `0x4e487b71` panic-data constants as well as the three dispatch selectors; the census is not a selector count. A third compile to `/var/tmp` reproduced both binaries, and a second REA call retained the same selector set and decoded digest; comparison results are in `verification.txt` (the path-sensitive Evidence IDs are not compared).

REA inferred `alpha()` mutability as `view` although the compiler ABI says `pure`; selector recovery matches, but this is a recorded inference delta, not an ABI correction. `store(uint256)` and `load()` inferences align with the compiler ABI for this fixture.

## Limits and reproduction

One synthetic carrier and one compiler/settings point only. No deployment identity, EVM execution, chain lookup, or runtime behavior is established. From the lane root, recompile and probe without using `/tmp`:

```sh
D=.ufo/waves/arc3-loop1-round9/claims/c2/EX-6/evidence
OUT=/var/tmp/kaidoku-r9-ex6/recheck/out
mkdir -p "$OUT"
node "$D/compile.js" "$D/ViaIRFallback.sol" "$OUT"
TMPDIR=/var/tmp/kaidoku-r9-ex6 node /home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/scripts/rea.mjs inspect-evm-interface "$OUT/runtime.hex" hex --format json
python3 "$D/walk_dispatch.py" "$OUT/runtime.bin"
```

The exact run, package identity, and scratch path are recorded in `identities.txt` and `EX-6.md`. The parent should land this entry plus the proposed EVM token shown in the draft header and rerun Command A; this seat did not edit corpus files or the coverage map.
