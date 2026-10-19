# EX-6 — C1 coverage: Vyper Cancun blob-primitives draft

**Verdict: REPRODUCED, bounded.** I chose the frozen C1 candidate “a Vyper hardfork variant” and independently built a new three-function carrier using Cancun-only blob primitives. The result closes only this source/compiler/target slice of the named Vyper hardfork/dispatcher Unknown; the general Unknown remains open.

## Re-derived items

- **Compiler/source identities — VERIFIED.** `evidence/identity.txt:1-4` records the two source SHA-256 values, re-hashed existing Vyper executable, and `0.4.3+commit.bff19ea2`. Sources are this seat’s `evidence/BlobFork.vy` and `evidence/BlobFeeOnly.vy` (`BlobFork.vy:6` uses `blobhash(index)`; `BlobFeeOnly.vy:6` uses `block.blobbasefee`).
- **Fork-specific compiler behavior — REPRODUCED.** Three pre-Cancun targets (`london`, `paris`, `shanghai`) refuse `BlobFork.vy` with `blobhash is not available pre-cancun` (`evidence/compile-results.txt:1-26`); a separate fee-only source independently refuses those targets with `block.blobbasefee is not available pre-cancun` (`:36-61`). Both sources compile for `cancun` and `prague` (`:28-35`, `:63-70`).
- **Bytecode and dispatcher — REPRODUCED.** `BlobFork` compiles to 126 bytes, SHA-256 `7569bf585ac8bb90265e5ed51a7b41c412d70085c8fcc6f09bd13a7ae98891dc`, under both Cancun and Prague; both same-target repeated builds and the cross-target outputs are byte-identical (`evidence/bytecode-verification.txt:1-9`). The fresh opcode-boundary walk finds three `PUSH4` selectors and three `XOR` checks; one `AND`, no `MOD`, and one each of `BLOBHASH` and `BLOBBASEFEE` (`:3-4`). The opcode output is retained at `evidence/compiled/BlobFork-cancun.opcodes_runtime:1`; compiler settings are `evm_version=cancun`, `optimize=gas` (`.../BlobFork-cancun.settings:1`).
- **REA extraction — REPRODUCED for selector recovery.** Fresh 6.7.0 CLI calls recovered all 3 compiler method IDs on both builds: `3acddfc1, 47c1ab88, 766d322f`; decoded size/hash match the compiled bytes (`evidence/probe-results.txt:1-15`; full envelopes `evidence/probe-cancun.json:1`, `probe-prague.json:1`). Evidence IDs are `ev_3d8a1d315412181390beaaba9e8e65a54963e9216bac5b4e8c943c330aaeb115` and `ev_121204ad90a671b8ce08112f6c6afde0d5340620b6af359b258984fcbf00d208` respectively.
- **Inference calibration — DISCREPANCY.** The compiled ABI declares `blob_hash(uint256)` as `view`; REA infers `payable` for selector `766d322f` (`evidence/compiled/BlobFork-cancun.abi:1`, `probe-cancun.json:1`, summarized in `bytecode-verification.txt:15-18`). The inferred mutability is not promoted to ABI fact. REA also reports discovery completeness and hardfork `unknown`, and runtime execution `not-performed` (`bytecode-verification.txt:16-18`).
- **Command A baseline — VERIFIED.** At frozen HEAD `e746ca79e2dbb3cb41436d612f448e81d2c6e585`, I ran the `SCORECARD.md:88-124` source-derived recipe: `knowledge_files=89`, `mapped=89`, `missing=[]`, `dangling=[]` (`evidence/command-A-before.txt:1-2`).
- **Post-integration Command A — UNVERIFIABLE.** This seat only supplies the draft; I did not edit corpus or map, and did not measure a post-landing revision.

## Draft and recheck

Copy-ready corpus draft: `entry-draft.md`. Proposed destination: `corpus/knowledge/2026-10-19-arc3-r11-vyper-cancun-blob-primitives.md`; proposed EVM-row token: `2026-10-19-arc3-r11-vyper-cancun-blob-primitives`. Parent integration must land both and rerun Command A at the landing revision; this seat makes no 90/90 claim.

From the lane root, re-derive with:

```sh
bash .ufo/waves/arc3-loop1-round11/claims/c1/EX-6/evidence/rederive.sh
bash .ufo/waves/arc3-loop1-round11/claims/c1/EX-6/evidence/probe.sh
python3 .ufo/waves/arc3-loop1-round11/claims/c1/EX-6/evidence/verify_evidence.py
```

Compiler and probe outputs are retained under `evidence/`; scratch and `TMPDIR` are under `/var/tmp/kaidoku-arc3-r11-ex6`. No tracked corpus, README/map, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md`, gate source, or peer artifact was changed. The initial wrong `block.blobhash` spelling was corrected; that exploratory attempt is not used as evidence.
