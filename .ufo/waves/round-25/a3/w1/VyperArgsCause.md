# VyperArgsCause — why REA 6.5.0 infers `uint256,uint256` for Vyper `transfer(address,uint256)`

Seat `KaidokuR25a3.VyperArgsCause` (executor, wave w1, round 25 attempt 3), 2026-10-22. Read-only on the lane; artifacts in `/fast/scratch/hyaku/kaidoku-r25-a3/seats/VyperArgsCause/`. Only this report was written in the lane; no git/jj mutation, no delegation, no background job.

## Verdict — HOLDS (cause identified, reproduced four independent ways)

**Cause.** REA 6.5.0 does not infer argument types itself: its `inspect-evm-interface` provider is `evmole@0.9.3`. evmole 0.9.3 recognises an `address` argument **only** from a 160-bit AND mask applied to the calldata word and has **no** rule for a shift-based clamp. Vyper 0.4.3 validates an `address` calldata word with `x >> 160` (SHR), never with a mask, so evmole 0.9.3 finds no type evidence and falls back to its default `uint256` for every calldata word — hence `transfer(address,uint256)` reads as `uint256,uint256`. Inference from source + bytecode + controlled experiment + upstream diff, not a guess.

## 1. REA 6.5.0 = evmole 0.9.3 (observation)

`corpus/evidence/round-25/a2/c2/stewardtoken/envelope.json`: `provider.id=evmole-interface`, `provider.version=evmole@0.9.3`; `a9059cbb` → `arguments="uint256,uint256"`, `stateMutability="payable"`, `bytecodeOffset=806`. `rea-agents@6.5.0` pins `evmole: 0.9.3` (`~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json`). Running that cache's evmole 0.9.3 CLI (`node .../evmole/dist/evmole_cli.mjs analyze --file <runtime.hex>`) on the stewardtoken runtime reproduces the envelope field-for-field: 22 selectors, same offsets (a9059cbb→806, 095ea7b3→880, 70a08231→2476), same `arguments` and `stateMutability`.

## 2. The rule in evmole 0.9.3 (source observation)

Crate `https://static.crates.io/crates/evmole/evmole-0.9.3.crate`, 2026-10-22, HTTP 200, 116 397 B, sha256 `d6193260884881a920613c477a0b457af872b228b939ec26c60f7e66a5e0c508`.
- `src/arguments/mod.rs:564-587` — the only mask-derived type evidence: `op::AND` of an arg-labelled value with a constant → `and_mask_to_type(mask)`, confidence 5 (`and_mask: None` required, so only the first mask on a value counts).
- `src/utils.rs:73-107` — `and_mask_to_type`: contiguous, right-aligned, byte-aligned mask → `Address` **iff width == 160**, else `Uint(width)`; non-contiguous / non-byte-aligned / zero → `None`.
- `src/arguments/mod.rs:83` — with no evidence the default is `DynSolType::Uint(256)`; `grep "op::SHR" src/arguments/mod.rs` (0.9.3) → **no match**: no shift rule exists. `mod.rs:591-615` — `op::EQ` between the raw and the masked word upgrades the same mask-derived type to confidence 20 (what solc's decoder triggers).

## 3. Bytecode observation — Vyper shift-clamp vs solc mask-clamp

stewardtoken (`vyper 0.4.3`, decoded sha256 `1846469bd2abc625ecf69567af16153f791fd6856e3c7acf32c2bf6f80967c51`, 3337 B) — `transfer` body at 0x326 (evmole `bytecodeOffset` 806):

```
0x031a JUMPDEST  0x031b PUSH4 0xa9059cbb  0x0321 XOR  0x0322 PUSH2 0x0a34  0x0325 JUMPI
0x0326 PUSH1 0x44  0x0328 CALLDATASIZE  0x0329 LT  0x032a CALLVALUE  0x032b OR
0x032c PUSH2 0x0cd9  0x032f JUMPI        ; revert if calldatasize<0x44 or callvalue!=0
0x0330 PUSH1 0x04   0x0332 CALLDATALOAD  ; _to
0x0333 DUP1  0x0334 PUSH1 0xa0  0x0336 SHR     ; _to >> 160
0x0337 PUSH2 0x0cd9  0x033a JUMPI       ; revert if (_to >> 160) != 0   <-- no mask
```

The same `CALLDATALOAD / DUP1 / PUSH1 0xa0 / SHR / PUSH2 / JUMPI` idiom appears in every Vyper address slot (approve 0x037a-0x0384, balanceOf 0x09b6-0x09c0, …).

rv2token (`solc`, decoded sha256 `c1081a565869b50387211b25afaf3768294aa774c35845bc3a8c0b12cfe15e74`, 1943 B) — shared ABI address validator at 0x52d, reached from the transfer branch at 0x107:

```
0x052d JUMPDEST  0x052e PUSH0  0x052f PUSH20 0xffffffffffffffffffffffffffffffffffffffff
0x0544 DUP3  0x0545 AND                       ; masked = value & (2^160-1)
0x0546 SWAP1 0x0547 POP 0x0548 SWAP2 0x0549 SWAP1 0x054a POP 0x054b JUMP
0x0566 JUMPDEST  0x0567 DUP2  0x0568 EQ  0x0569 PUSH2 0x0570  0x056c JUMPI
0x056d PUSH0 0x056e PUSH0 0x056f REVERT      ; revert if masked != raw
```

Mask census (observation): stewardtoken has 28 `AND` sites and every one uses a 0x1f-length mask (two patterns, 14× each: `DUP1 PUSH1 0x1f DUP3 PUSH0 SUB AND` and `NOT PUSH1 0x1f … AND`); its only `PUSH20` (0x0cec) lies in the trailing Vyper metadata blob after the final `REVERT` at 0x0cdc, so **no 160-bit mask constant exists in executable code**. rv2token has 25 `PUSH20 0xff…ff` masks in code (0x13e … 0x52f); its 26th `PUSH20` (0x774) is metadata and not a mask.

## 4. Controlled experiment (observation)

Synthetic A/B, 259 B each, structurally identical, differing only in the clamp: `synthetic-solc.hex` = `CALLDATALOAD / PUSH20 <160-bit mask> / AND`; `synthetic-vyper.hex` = `CALLDATALOAD / DUP1 / PUSH1 0xa0 / SHR / PUSH2 revert / JUMPI`.
- evmole 0.9.3 CLI: solc-like → `a9059cbb arguments="address,uint256"`; vyper-like → `"uint256,uint256"`.
- REA 6.5.0 end-to-end (`rea inspect-evm-interface <file> hex`, exit 0, 2026-10-22T10:50:15Z/16Z): solc-like `ev_143e8a050436cc2f979b6e355eba84b75bcc91e40ea69f6b7348a698a0b8808b` → `address,uint256`; vyper-like `ev_99fe7c45eb2979f50d847a1ebc35983a049918e7979967a27850b44281b46dbf` → `uint256,uint256`.

Length-preserving mask mutation of the **real solc carrier** (jump targets stay valid):

| mutant | mask | evmole 0.9.3 for `a9059cbb` |
|---|---|---|
| `mut-D-all-156bit.hex` | all 25 → `0x0f ff×19` (156-bit, not byte-aligned → `and_mask_to_type`=None) | `uint256,uint256` (the Vyper symptom, on a solc carrier) |
| `mut-E-all-frag.hex` | all 25 → non-contiguous | `uint256,uint256` |
| `mut-F-all-152true.hex` | all 25 → `0x00 ff×19` (true 152-bit) | `uint152,uint256` |
| `mut-G-validator-152true.hex` | only the validator copy → 152-bit | `uint152,uint256` |

The inferred type is a pure function of the AND-mask width; 160 is the `address` special case. Tracer: evmole 0.9.3 rebuilt with feature `trace_arguments` → on the stewardtoken runtime there are **0** type assignments (`tname: Some((` never occurs, all 22 functions) and `a9059cbb args=[Uint(256), Uint(256)]`; on rv2token 1343 assignments, `a9059cbb=[Address,Uint(256)]`.

## 5. Upstream cross-check (observation)

Diff 0.9.3 → 0.9.4 (`https://static.crates.io/crates/evmole/evmole-0.9.4.crate`, HTTP 200, 120 441 B, sha256 `063223dca232f419f1926deb0cc82b2a289ac0eb6b9b7a3a33f2da2173acc2a2`).
- `v094/src/arguments/mod.rs:663-668` adds exactly the missing rule, with the upstream comment "Vyper validates narrow ABI scalars by rejecting non-zero high bits." — `op::SHR` on an arg-labelled value, guarded by `is_conditional_guard`, width 160 → `DynSolType::Address` (width 1 → Bool, other byte widths → `Uint(width)`), confidence 20. 0.9.3 has no such handler.
- `v094/src/state_mutability/mod.rs:122-135` adds `AND|OR|XOR|MUL` propagation of the `CallValue` label — the fix for the adjacent `stateMutability` miss (§6). Built locally (0.9.4): stewardtoken `a9059cbb=[Address,Uint(256)]`, `70a08231=[Address]`, `23b872dd=[Address,Address,Uint(256)]`; synthetic-vyper → `[Address,Uint(256)]`; rv2token unchanged.

## 6. Adjacent observation — `stateMutability`

REA 6.5.0 reports `stateMutability="payable"` for the Vyper stewardtoken's `transfer`, which is `nonpayable` in its ABI; the solc carriers report `nonpayable`. Same idiom family: Vyper's nonpayable guard is `CALLDATASIZE LT / CALLVALUE / OR / PUSH2 / JUMPI` (0x0328-0x032f above); evmole 0.9.3's mutability detector recognises only `CALLVALUE`/`ISZERO(CALLVALUE)` as the JUMPI condition (`state_mutability/mod.rs:100-129`), the `OR` drops the label, the guard is invisible; 0.9.4 fixes it.

## 7. Risks and limits

- The mechanism rests on evmole 0.9.3's shipped source (crates.io tarball) plus the npm 0.9.3 build REA 6.5.0 itself depends on; no web page was opened, so no page quote is claimed. `api.github.com/repos/0xKitsune/evmole/contents/src` was tried on 2026-10-22 → HTTP 404 (wrong owner; the crate metadata names `github.com/cdump/evmole`, not opened).
- The synthetic pair is not a real contract: it isolates the clamp's opcode shape only, proving sufficiency/necessity of the mask for evmole 0.9.3, nothing about Vyper semantics. The mutants are length-preserving but semantically broken (their masks no longer match the contract's intent); they probe the analyzer's decision rule, they are not deployable bytecode.
- Measured scope: evmole 0.9.3, one concrete execution path per function; arguments never read by that path are not inferred (0.9.4 adds a min-calldata seeding).
- Tooling: no pacman transaction. Added only local `cargo`/`rustc 1.99.1` builds of the two evmole crates (feature `trace_arguments`); node v24.21.0 for the npm evmole 0.9.3 CLI; `evmole@0.9.3` and `rea-agents@6.5.0` came from the existing npx cache (no install).

## 8. Artifacts (scratch; sha256) — `/fast/scratch/hyaku/kaidoku-r25-a3/seats/VyperArgsCause/`

- `results.txt` `9943067294deb33b0a6b1f7a69c830383fe06b4eeeff57c15497c2a901817ea8` · `evidence-excerpts.txt` `685a0ef61fdbdcae1a8a9c03917691e92f9196ec7f039409ffb5f0a55a09682c` · `rea-synthetic-solc.json` `2092b3a7ebc68de529912994f89cf5ffcad248e88dde668c5df51a2f32c08dd3` · `rea-synthetic-vyper.json` `60c87490a4d7134e1aef4dba9f547ca33a2ae987c80c833065eb110f760990d6`
- `evmdis.py` `1ef45cf28692a799b3450fa538085fc5239fdccde0a60b6e857810bc9424adf3` · `synthetic_ab.py` `c4d5d46e65de9aa0f5c72d2cea07c790aa8f387122c9d05e5af353f3ff2f4982` · `and_masks.py` `0bc13f2e077063910345680302e3f3192b465f5643e3456d65b3335964106cf8` · `mutate.py` `81a2a84c577ecf184615eb1215df0a6ada6a3dc58a692401d5f57b191d23d1ce` · `mutate_rv2.py` `54f1c8839f3baf9b238ae1d63c49cc0d02028c1ed6e5a9408af12715789cdf98`
- `bisect_sites.py` `06d6366ee3963e7cf228c8b2dff672ce0e2d122e5c45af361ae39fa8f4252188` · `run-evidence.sh` `a3e5a0fbaedd2a5f571d04b856d018353c6d0645920e52296610e5b54d5897ec` · `synthetic-solc.hex` `655eb385e902a30fbcfe5c5d2117f921025e98ad194c554b0dd269c41e0f030c` · `synthetic-vyper.hex` `dd45fe6c6803a816ea706f3688c0d31159f7f1e5bdab06860a67cf73856808d9`
- `mut-D-all-156bit.hex` `aadf8b0a4b05ee23ce5f3842f08353a40110c0433b2ce37927fd9c35db88b50d` · `mut-F-all-152true.hex` `783c88e714c946ee413cb9cd6019de2ca126dec187b24fb599c2a02bfc0b0dc7` · `mut-G-validator-152true.hex` `1d803373276306af2b180ce89fe8c2c4255e3e191c286008358e3af573402006` · `mut-A-validator-156bit.hex` `a8f49b049f4d40e67b77498fff68c378812f51cadab3aed55de82c0954151452`
- `mut-B-validator-frag.hex` `7a7675d0ebf0a4bbfb4d64dd51c49653a2d5d39c9bd4d5937ccd05eaf4d866bb` · `mut-C-others-156bit.hex` `7c80c1c99d87535a126e5f3c5527632cbc8536cde94c0d8ddd7e2a971b2769a9` · `mut-E-all-frag.hex` `3b9ebece72178ad9ce6b6c32e6ad31a577ce848f184282c06e6d762d9d134fea`
- `evmole-0.9.3.crate` `d6193260884881a920613c477a0b457af872b228b939ec26c60f7e66a5e0c508` · `evmole-0.9.4.crate` `063223dca232f419f1926deb0cc82b2a289ac0eb6b9b7a3a33f2da2173acc2a2` · `diff-093-094-arguments.patch` `f8efda024ca7847183f6979760b829ebc55fd672192ba88b488d031c7b790476` · `diff-093-094-mutability.patch` `0b55d15d64501226db490cd2a42da4fa42c8ab8d6120763ba270647bb00783d6`
- `evmtrace-093` `7965d1386f4d6b4ee2ce22279487c640d5a9845c3e3bc56f42f86be875b4e056` · `evmtrace-094` `874896936c8abce6eae818df1a5633b3a79332f587f96ae5dadc05ac9fd8b8db`

Sibling overlap: `w1/C2EvmoleDirect.md` (same wave) independently reports that evmole **0.9.4** recovers the Vyper address rows while every published REA release pins 0.9.3; my §5 diff and local 0.9.4 build corroborate that from the source side. This report adds the *mechanism*.

Report: .ufo/waves/round-25/a3/w1/VyperArgsCause.md
