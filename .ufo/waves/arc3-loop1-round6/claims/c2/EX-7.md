# EX-7 — c2 chain (corpus Unknown closure) — arc3-loop1-round6

Seat: EX-7 · chain c2 · 2026-10-19 · lane `kaidoku-shokunin` · dispatch provider `zai-coding-plan/glm-5.3-flash` (xai lane 403'd fleet-wide, per `claims-frozen.md`).
Target claim: **C2 — close one named corpus Unknown.** Chosen Unknown: **the solc `viaIR` pipeline's dispatcher shape**, named at
`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:33` and `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28` ("the `viaIR` pipeline" — unvisited since r3).
Deliverable: corpus entry draft at `entry-draft/2026-10-19-arc3-r6-viair-dispatch-shape.md` (parent lands it) + coverage-map token patch + evidence tree under `EX-7/`.

## 0. Re-derived first-hand (rule #14) — nothing quoted from prior seats

| item | verdict | first-hand evidence |
|---|---|---|
| Command A before-state at work commit `58c3db7` | **REPRODUCED** | ran SCORECARD.md:88-124 recipe verbatim → `{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "rule_blocks": 14}` — matches the frozen 84/84 before-state |
| The Unknown is real and still open | **VERIFIED** | `grep -n -i "viaIR" corpus/knowledge/*.md` → exactly two hits, both in Unknowns lists (r3:33, r4:28); no corpus entry names a viaIR dispatcher measurement |
| solc toolchain | **REPRODUCED** | `node -e "require('solc').version()"` at `.ufo/waves/arc3-loop1-round1/tools/solc-prefix/` (read-only reuse, no new install) → `0.8.37+commit.f401782d.Emscripten.clang`; `soljson.js` sha256 `221d7a667378…abad4c`, `solc/package.json` `b3a90035cab4…33491` — equal to the r3-recorded digests |
| HEAD/work commits | **REPRODUCED** | `git log --oneline -2` → `c625d5d` (records) / `58c3db7` (work), matching the dispatch brief |
| Wave dir state | **VERIFIED** | `.ufo/waves/arc3-loop1-round6/` contained only `claims-frozen.md` before my writes; my artifact is the first c2 staging under it |

## 1. What was built (all bytes first-hand this round)

- Carrier `ViaIrVault` (`src/ViaIrVault.sol`, sha256 `f5391167…80cbbe`): 14 externals + `receive()`, ABI-verified census view ×7 / pure ×1 / nonpayable ×6 / payable ×1 (`deposit`) + payable `receive`; no ERC-20 surface.
- Planted K=15 recorded **pre-compile** (`evidence/planted-K.json`) with **three agreeing derivations**: pure-Python keccak-f[1600] written for this seat (`scripts/keccak.py`, selftest 8/8 public vectors incl. `c5d246…` empty and `transfer(address,uint256)`→`a9059cbb`), `js-sha3@0.8.0`, solc `methodIdentifiers` (`evidence/selector-derivations.txt`). Zero collisions with 9 ERC-20 selectors. One pre-compile source fix (`digestOf` pure→view) proven selector-neutral (`planted-K.preact.json`).
- Three compile legs on the receipted solc 0.8.37 (`evidence/compile-receipt-rerun.txt`, rerun byte-identical):
  `viair-opt200` runtime **1,517 B `2ec3f557…`** · `viair-noopt` **4,144 B `0cc6938c…`** · `std-opt200` control **1,921 B `c2ceabb1…`** (same source, same optimizer, `viaIR` unset).
- Seven sealed probe envelopes under `probe/` (TMPDIR=`/var/tmp/ex07-r6/tmp`, the standing EDQUOT rule):

| leg | rea pin | evidence_id | result |
|---|---|---|---|
| viair-opt200 hex | 6.4.0 | `ev_409e0442…` | **15/15**, `dispatch:"abi"` ×15, decoded sha `2ec3f557…` |
| viair-opt200 raw | 6.4.0 | `ev_c55a152c…` | 15/15 |
| viair-opt200 hex | 6.7.0 | `ev_285d13d0…` | 15/15 |
| viair-noopt hex | 6.4.0 | `ev_8ddef761…` | 15/15 |
| std-opt200 hex (control) | 6.4.0 | `ev_3b390132…` | 15/15 |
| TRAP: raw fed the hex *text* | 6.4.0 | `ev_2e7e40ba…` | parsed-and-empty (0 fns; decoded sha = hex-file sha `19838d66…`) |
| creation.hex probe | 6.4.0 | `ev_ff7ee757…` | parsed-and-empty (0 fns); runtime byte-embedded at **+43** of 1,560 B |

## 2. The finding (closes the Unknown, per-item verdicts)

- **viaIR dispatcher class — VERIFIED (fourth class).** `5f3560e01c` prologue + **inverted** calldatasize guard (`…36 10 15 61<0022> 57`, the `ISZERO` differs from legacy `…36 10 61<00e7> 57`) + **linear ascending EQ chain** `DUP1 PUSH4 <sel> EQ PUSH2 <dst> JUMPI` ×14 at a strict 11-byte stride (dsts 253–982, all JUMPDESTs; `evidence/walk-viair-opt200.json` `eq_pc_gaps=[11]×13`, `eq_sorted_ascending=true`), terminated by a 15th leg **`PUSH4 ee02438e SUB PUSH2 0x000e JUMPI`** — `SUB` (0x03), not `EQ`; dst `0x000e` = the guard's small-calldata revert-path JUMPDEST (byte 14); match falls through into `mark`'s handler (opt200: `CALLVALUE; PUSH2 0x00f9 JUMPI` at 204; noopt: `PUSH2 0x05a9 JUMP`). Same shape in `viair-noopt` (dsts 208–273).
- **Pipeline controls the shape — VERIFIED.** The std control (identical source + optimizer) compiles the r3 class instead: GT/EQ binary search, GT pivots `6e69f38c`/`90ab171e`/`3f4ba83a` (pcs 19/30/137), 15 EQ + 3 GT, three selectors appearing twice (GT pivot + EQ leaf) and correctly deduplicated by the extractor. So: legacy = binary search, viaIR = sorted linear scan with a SUB-terminated final leg — **same `5f3560e01c` head; the prologue does not identify the pipeline, the compare tree does.**
- **Offset convention — VERIFIED (fifth class).** viaIR legs: 14/15 reported offsets ≡ their EQ leg's `PUSH2` dst (JUMPDEST handler heads); the 15th (`mark`, the SUB-leg selector) = **push4_pc+10 = 204, not a JUMPDEST, not a PUSH2 target**. Legacy control: 15/15 JUMPDEST (the three apparent mismatches in my first walk were my own join taking each duplicated selector's GT-pivot site). r1 = PUSH1 immediates, r4 Vyper = push4_pc+11, viaIR = dst/pc+10 hybrid. "Offsets land on JUMPDESTs" is legacy-pipeline-scoped.
- **Zero false positives — VERIFIED.** viair-opt200: 19 opcode-boundary PUSH4 sites = 15 selectors (15 distinct, no duplication — unlike the control's 18/15) + `4e487b71` ×2, `0c2eae8d`, `3c3332b9` (solc-0.8.37 internal error constants, also seen in r3's VaultB census). None reported as functions.
- **Inference delta — VERIFIED, pipeline-scoped.** `inferred_state_mutability` vs ABI: **14/15 agree; `scale(uint256,uint256)` pure→view** — the r3-recorded pure/view class. The r4 Vyper "arg-taking → payable" pattern does **not** appear (0 payable-reads); correlate: viaIR emits per-handler value guards *after* dispatch, not the legacy fused pre-guard.
- **Traps — REPRODUCED on the new class.** raw-on-hex parsed-and-empty; creation probe parsed-and-empty with the runtime byte-embedded at +43 (stated per `corpus/QUALITY.md:21` — not "no dispatch table in initcode").
- **CBOR trailer — VERIFIED.** `ipfs` + `solc 0x000825` (= 0.8.37) at the runtime tail, r3's trailer class under viaIR too.
- **Unknown narrowed, not closed:** solc ≠ 0.8.37 under viaIR; Vyper's IR pipeline; runs ≠ 200; `fallback()`-bearing and receive-less viaIR shapes. All carried into the entry's Unknowns list.

## 3. Landing moves for the parent (command A 84 → 85)

1. Copy `EX-7/entry-draft/2026-10-19-arc3-r6-viair-dispatch-shape.md` → `corpus/knowledge/`.
2. Append the token to the coverage-map EVM row (`corpus/README.md:38`), patch text:

```diff
-| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-evm-optimizer-shapes`, `2026-10-19-arc3-r4-evm-vyper-leg` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07) and from real solc-0.8.37-compiled runtime carriers (arc3-r1); positional encoding quirk |
+| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-evm-optimizer-shapes`, `2026-10-19-arc3-r4-evm-vyper-leg`, `2026-10-19-arc3-r6-viair-dispatch-shape` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07), real solc-0.8.37 carriers (arc3-r1/r3), Vyper 0.4.3 carriers (arc3-r4) and the solc-0.8.37 viaIR pipeline (arc3-r6, fourth dispatcher class); positional encoding quirk |
```

3. Projected command A (computed by the SCORECARD recipe with the landed file + token overlaid, measured at this seat; **not** a substitute for the post-landing measurement): `{"knowledge_files": 85, "mapped": 85, "missing": [], "dangling": [], "coverage_score": 10.0}` — `rule_blocks`/`depth_score` untouched (c3 chain's axis).
4. Nothing else changes: no SKILL.md, no PROVINCE.md, no gate — my write scope ends at this artifact dir.

## 4. Custody & scope statement

- All evidence retained under `.ufo/waves/arc3-loop1-round6/claims/c2/EX-7/` (42 files: `src/`, `scripts/`, `evidence/` incl. `manifest.sha256`, `out/` ×3 legs, `probe/` ×7 envelopes, `entry-draft/`). Scratch was `/var/tmp/ex07-r6/` (never `/tmp`).
- Custody reads only: r1 solc prefix (read-only reuse, digests re-verified equal), r3/r4 corpus entries, README/QUALITY/SCORECARD — no tracked file modified; `git status` after this seat shows only the pre-existing `arc2-loop1-round10/C3.md` modification and the untracked `arc3-loop1-round6/` tree.
- Honest limits: single solc version, single carrier family, K=15, runtime class 1.5–4.1 KB, one 6.7.0 leg (hex only); `raw` legs at 6.4.0 only; the projected-85 line is a projection until the parent lands and re-measures.
