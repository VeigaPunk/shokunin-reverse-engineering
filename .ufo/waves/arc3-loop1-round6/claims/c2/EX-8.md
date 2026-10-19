# EX-8 — c2 chain (corpus Unknown closure) — arc3-loop1-round6

Seat: EX-8 · chain c2 · 2026-10-19 · lane `kaidoku-shokunin` · dispatch provider `opencode-go-7/deepseek-v4.1-flash` (fourth dispatch; xai 403, zai/antigravity/cursor interrupted — per `claims-frozen.md`).
Target claim: **C2 — close one named corpus Unknown.** Work split:
1. **Verification half:** independently re-derive EX-7's delivered `viaIR` entry (same Unknown class, already landed as a draft by that seat).
2. **Own half:** close a **different** named Unknown — the Vyper 0.4.3 non-default optimizer forms (`-O codesize` / `-O none` / `--no-optimize`), named at `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28`.
Deliverables: corpus entry draft `entry-draft/2026-10-19-arc3-r6-vyper-optimizer-forms.md` + coverage-map token patch (§4) + evidence tree under `EX-8/`.

## 1. Re-derived first-hand (rule #14) — nothing quoted from prior seats or rounds

| item | verdict | first-hand evidence |
|---|---|---|
| HEAD / work commits | **REPRODUCED** | `git log --oneline -2` → `c625d5d` (records) / `58c3db7` (work), as the dispatch brief names |
| Command A before-state at `58c3db7` | **REPRODUCED** | ran the SCORECARD.md:88-124 recipe verbatim → `{"citation_resolved_rules":14,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":84,"mapped":84,"missing":[],"rule_blocks":14,"revision":"58c3db7"}` |
| solc toolchain | **REPRODUCED** | `node -e "require(<r1 solc-prefix>).version()"` → `0.8.37+commit.f401782d.Emscripten.clang` (r1 prefix reused read-only, no install) |
| Vyper toolchain | **REPRODUCED** | `.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper --version` → `0.4.3+commit.bff19ea2`; bin sha256 `615f792c…8209dd10`; venv python `3.14.7` sha256 `d78f9cf7…cb26a70c` — all equal to the r4 receipt |
| `viaIR` Unknown still open at HEAD | **VERIFIED** | `grep -rn -i viair corpus/knowledge/` → exactly two hits, both in Unknowns lists: r3:33, r4:28; no corpus entry names a viaIR measurement |
| Wave-tree write scope | **VERIFIED** | `.ufo/waves/arc3-loop1-round6/claims/c2/` held only `EX-6/`, `EX-7/`, `EX-7.md` before this seat's writes; my tree is `EX-8/` + `EX-8.md` |

## 2. Independent verification of EX-7's viaIR entry — per-item verdicts

Method: I rebuilt the standard-JSON input myself (`scripts/compile-solc.js`, not EX-7's `compile.js`), compiled the three legs on the pinned solc, wrote my own linear disassembler (`scripts/walker.py`), ran five fresh REA legs at **my own paths** (new `ev_` ids), and recomputed the offset/mutability tables against the recompiled ABI. Evidence: `ex7-verification/{compile-e8.txt,walk-out.json,verify-ex7.json,mutability-delta.json,probe/}`.

**Compile reproduction (all three legs byte-identical to EX-7's):**

```
viair-opt200  1517 B runtime 2ec3f557f6f2fb229dc49094981723c6efcce3df10f20363ec1732845c99581a
viair-noopt   4144 B runtime 0cc6938cd768199159cbed74a7e9f5bd4273c583afbf6babca643b0ffdbd29b4
std-opt200    1921 B runtime c2ceabb163ad9c1e6d88244c29c5187602eaf4c810029d0018e76eb9643f7e27
```

| # | EX-7 claim | verdict | my measurement |
|---|---|---|---|
| 1 | carrier `ViaIrVault.sol` sha256 `f5391167…80cbbe` | **REPRODUCED** | `sha256sum src/ViaIrVault.sol` → `f5391167…80cbbe` |
| 2 | three runtime/creation hashes and sizes above | **REPRODUCED** | exact match, `compile-e8.txt` |
| 3 | `5f3560e01c` prologue + **inverted** guard `36 10 15 61<0022> 57` | **REPRODUCED** | head `60806040526004361015610022575b3615…`; `CALLDATASIZE LT ISZERO` at pc 7; std head has bare `36 10 61<00e7> 57` (no `ISZERO`) |
| 4 | 14 EQ legs, ascending, strict 11-byte stride | **REPRODUCED** | my walker: 14 EQ legs, `eq_sorted_ascending=true`, `eq_pc_gaps=[11]`; sites 41…184; dsts 253/272/311/340/374/425/485/572/631/694/723/771/935/982 |
| 5 | final leg `PUSH4 ee02438e SUB PUSH2 0x000e JUMPI`, no `EQ` | **REPRODUCED** | site pc 194, imm `ee02438e`, dst 14, JUMPI 203, fall-through 204 (opt200 and noopt identical sites) |
| 6 | noopt EQ dsts 208–273 | **REPRODUCED** | 208/213/218/223/228/233/238/243/248/253/258/263/268/273 |
| 7 | offsets: 14/15 = EQ `PUSH2` dst (JUMPDEST); `mark` = 204 = push4_pc+10, byte `0x34`/`0x61`, not a JUMPDEST/PUSH2 target | **REPRODUCED** | fresh probes: 14/14 EQ rows offset−dst = 0, all JUMPDEST; `mark` offset 204, `204−194 = 10`, byte `34` (opt200) / `61` (noopt), `is_jumpdest=false`, `is_push2_target=false` |
| 8 | std control: legacy GT/EQ binary search, 15 EQ + 3 GT, three duplicated selectors, extractor deduplicates | **REPRODUCED** | my walker: 15 EQ, 3 GT (pivots `6e69f38c`, `90ab171e`, `3f4ba83a` at pcs 19/30/137), EQ site gaps `[11,15,26]`, 15/15 tool functions |
| 9 | zero false positives: viaIR 19 PUSH4 sites = 15 selectors + `4e487b71`×2 + `0c2eae8d` + `3c3332b9`; std adds `43000825` | **REPRODUCED** | viair-opt200: 19 sites / 18 distinct, non-selector list exactly those four; std: 22 sites / 19 distinct incl. `43000825` |
| 10 | mutability delta 14/15; `scale(uint256,uint256)` ABI `pure` reads `view` | **REPRODUCED** | my recomputation against recompiled ABI: agree 14/15, only `6e69f38c` (`pure`→`view`); zero payable-reads |
| 11 | probes 15/15 (hex, raw, 6.7.0, noopt, control) | **REPRODUCED** | my ids: opt200-hex 6.4.0 `ev_57f8106a…`, raw `ev_a9ce1ad3…`, opt200-hex 6.7.0 `ev_ba2ac079…`, noopt-hex `ev_f3d97ae5…`, std-hex `ev_1ec82020…` — all 15/15, decoded sha = runtime sha |
| 12 | raw-on-hex trap: 0 functions, decoded sha = hex text sha | **REPRODUCED** | my run `ev_068c94c4…`: 0 functions, decoded sha `19838d66…` = hex file sha |
| 13 | creation probe parsed-and-empty; runtime embedded at +43 of 1,560 B | **REPRODUCED (embedding) / envelope cited (probe)** | `creation.bin.find(runtime.bin)` → 43; EX-7's creation envelope shows 0 functions, decoded sha = creation sha (I did not re-run this probe) |
| 14 | CBOR trailer `ipfs` + `solc 0x000825` (0.8.37) | **REPRODUCED** | tail `…a2 64 69706673 58 22 <32B> 64 736f6c63 43 000825 00 33` |
| 15 | **“14 explicit external functions + `receive()`”** | **CORRECTED** | source has **15** `function` definitions + `receive()` + constructor: `grep -c '^    function '` → 15; ABI = 15 function entries + 1 receive + 1 constructor; `methodIdentifiers` = 15 keys. The K=15 set is the 15 externals; `receive()` has no selector and is reached through the calldatasize==0 stub (0x0e→0x18→subroutine 0x57e), not a dispatch entry. EX-7's own mutability census (view×7/pure×1/nonpayable×6/payable×1 = 15) already implies 15; only the “14” phrase is wrong. No measurement changes — entry draft needs a one-word fix (also §2 of `entry-draft/…viair…md` repeats it) |
| 16 | entry draft's ABI facts “17 entries = 15 functions + 1 constructor + receive”, methodIdentifiers 15 keys | **REPRODUCED** | my recompiled ABI: 17 entries exactly as stated |

No measurement disagreement was found in EX-7's entry. Item 15 is a documentation count only.

## 3. Own closure — the Vyper 0.4.3 optimizer-form Unknown (r4:28)

One carrier (`VariantVault.vy`, sha256 `2d95791c…e9ad6d`; 13 externals + constructor; ABI census payable ×1 / nonpayable ×6 / view ×5 / pure ×1), one compiler (`vyper 0.4.3+commit.bff19ea2`), six compile forms, ten sealed REA envelopes. Selector set derived independently (js-sha3 keccak256 vs vyper `method_identifiers`, 13/13 agree). All numbers below are mine; evidence paths are relative to `EX-8/`.

| form | runtime | sha256 (prefix) | dispatcher class (byte-level) | probe | tool offsets |
|---|---|---|---|---|---|
| `default` (`-O gas`) | 1,790 B | `068db093…` | `5f3560e01c`; `sel % 14` uint16 jump table at `0x6e2..0x6fe` (runtime end), 8 buckets occupied / 6 sentinel `0x6da` (`5b 5f 5f fd`); per-bucket XOR chains (`PUSH4;DUP2;XOR;PUSH2;JUMPI`, 11-byte legs); 5 collision buckets | 13/13 `ev_89e53770…`; 6.7.0 `ev_86e3b205…` | `push4_pc + 11` **13/13** (re-confirms r4:22) |
| `Ocodesize` | 1,682 B | `c49c1004…` | `5f3560e01c` + perfect-hash header `a5 4e 06 37 0d` (mask `0xa54e`, table ptr `0x0637`, count 13) + 13×7-byte records `[selector 4B][handler target 2B][flag 1B]`; table ends at runtime end `0x692`; all 13 targets JUMPDEST; **zero selector PUSH4 immediates** (9 PUSH4 sites, all `08c379a0`) | 13/13 `ev_73337665…`; 6.7.0 `ev_aed7aaab…` | all 13 report the single shared **65** (not a handler target) |
| `Onone` (`-O none`) | 2,289 B | `e50f0346…` | bare `PUSH1 4 CALLDATASIZE LT ISZERO` guard then linear `PUSH4;DUP2;EQ;ISZERO;PUSH2;JUMPI` scan, handlers inline, chain order unsorted | 13/13 `ev_c61d72e1…` | `push4_pc + 12` **13/13** |
| `nooptimize` (`--no-optimize`) | 2,289 B | `e50f0346…` | **byte-identical to `-O none` on every artifact** (runtime/creation/ABI/method ids/opcodes/settings) | 13/13 `ev_7b92a24e…` | same |
| `paris-default` | 1,913 B | `bf4d8986…` | same MOD-table class; `PUSH0`→`PUSH1 0`, base `0x75d`, sentinel `0x752`, 8/6 occupancy | 13/13 `ev_2fc4192a…` | `push4_pc + 11` |
| `paris-codesize` | 1,806 B | `ecce416c…` | same perfect-hash class; shared offset 68 | 13/13 `ev_dd274ba9…` | shared 68 |

New measured facts that the r4 entry could not state:

- **The `-O codesize` records carry the true per-selector handler entry** (`deposit→0x005b`, `pause→0x02e8`, `sweep→0x024f`, …; all 13 JUMPDEST) and a **flag byte that tracks ABI arity/payability**: `0x04` zero-arg payable, `0x05` zero-arg nonpayable/view/pure, `0x25` one-arg, `0x45` two-arg — 13/13 match (`evidence/codesize-table.json`).
- **`bytecode_offset` is form-scoped**: gas `push4_pc+11`, none `push4_pc+12`, codesize a shared continuation (65/68). The r4 rule is therefore not a property of “Vyper” but of the default optimizer form.
- **The false-honest-stop hazard is measured, and it is total on Vyper**: a shape-blind `EQ;PUSH2;JUMPI` census returns **0** selectors on all six forms; it returns 14/15 on EX-7's viaIR legs (the SUB leg is invisible) and 15/15 only on the legacy solc control (`evidence/shape-blind.json`). REA's own extractor returns 13/13 on all six, so the hazard applies to hand-rolled censuses, not to the tool.
- Trap on this family: raw-on-hex → parsed-and-empty, decoded sha = hex text sha (`ev_33b00f09…`).

**Before → after for C2:** at `58c3db7`, command A = 84/84; with EX-7's entry + token alone the projection is **85/85, missing [], dangling []** (measured on a `git archive 58c3db7` overlay tree); with both r6 entries + both tokens it is **86/86, missing [], dangling []** (`evidence/projection-85.json`, `evidence/projection-86.json`; method in `evidence/projection-method.txt`). The named Unknown closes with the cited K/K evidence inside the entry.

## 4. Landing moves for the parent

1. Copy `EX-8/entry-draft/2026-10-19-arc3-r6-vyper-optimizer-forms.md` → `corpus/knowledge/`.
2. Append the token to the EVM row (`corpus/README.md:38`). The row currently reads `… \`2026-10-19-arc3-r4-evm-vyper-leg\` | held …`; EX-7's patch inserts `2026-10-19-arc3-r6-viair-dispatch-shape`. After both, the row's token list must be:

```diff
-| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-evm-optimizer-shapes`, `2026-10-19-arc3-r4-evm-vyper-leg` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07) and from real solc-0.8.37-compiled runtime carriers (arc3-r1); positional encoding quirk |
+| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-evm-optimizer-shapes`, `2026-10-19-arc3-r4-evm-vyper-leg`, `2026-10-19-arc3-r6-viair-dispatch-shape`, `2026-10-19-arc3-r6-vyper-optimizer-forms` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07), real solc-0.8.37 carriers (arc3-r1/r3, viaIR r6), Vyper 0.4.3 carriers (arc3-r4) and the Vyper 0.4.3 optimizer forms `-O gas`/`-O codesize`/`-O none` (arc3-r6); positional encoding quirk |
```

3. Projected command A (computed on the overlay tree described above, **not** a post-landing measurement): both entries → `{"knowledge_files":86,"mapped":86,"missing":[],"dangling":[],"coverage_score":10.0,"citation_resolved_rules":14,"rule_blocks":14}`. EX-7-only → `{"knowledge_files":85,"mapped":85,"missing":[],"dangling":[]}`. If the parent lands only one, the corresponding projection applies; landing order does not matter (the token row is a set).
4. No SKILL.md / PROVINCE.md / gate / tracked-file change from this seat.

## 5. Custody & scope statement

- All evidence under `.ufo/waves/arc3-loop1-round6/claims/c2/EX-8/` (94 files: `src/` ×1, `scripts/` ×7, `out/` ×54 — 6 forms × 9 artifacts, `probe/` ×10 envelopes, `evidence/` ×11 incl. `manifest.sha256`, `entry-draft/` ×1, `ex7-verification/` ×10). Scratch was `/var/tmp/ex08-r6/` (never `/tmp`, the standing EDQUOT rule); probe `TMPDIR` was disk-backed.
- Custody reads only: r1 solc prefix, r4 vyper venv and compile receipt, r3/r4 corpus entries, EX-7's artifact tree, README/QUALITY/SCORECARD — no tracked file modified; `git status` after this seat shows only the pre-existing `arc2-loop1-round10/C3.md` modification and the untracked `arc3-loop1-round6/` tree.
- Tool pins: `rea-agents@6.4.0` and `6.7.0`; EVMole `evmole@0.9.3`. Vyper 0.4.3, solc 0.8.37.
- Honest limits: single Vyper version, single carrier family, 13 externals, one bucket count (14) for the MOD form, runtime 1.68–2.29 KB, only `prague`+`paris` EVM versions, codesize perfect-hash **structure** decoded but its hash algebra not inverted, no `--experimental-codegen`, no `__default__`/fallback carriers, no creation-code probe on this carrier; projections are projections until the parent lands and re-measures.
