# CR-2 — c2 chain (corpus Unknown closure) — arc3-loop1-round6

Seat: CR-2 · chain c2 (EX-5..EX-12, CR-1..CR-4) · 2026-10-19 · lane `kaidoku-shokunin` · dispatch lane `opencode-go-7/deepseek-v4.1-flash` (per `claims-frozen.md:1-20`).
Target claim: **C2 — close one named corpus Unknown** (`claims-frozen.md:56-68`).
Deliverable: a **second** corpus-Unknown closure, distinct from EX-7's viaIR draft: the Vyper `--no-optimize` / `-O none` / `-O codesize` dispatcher forms named at `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28` ("CR-1's `--no-optimize` / `-O codesize` / `-O none` … were probed K/K by the probe but their dispatcher forms were not byte-characterized here").
Artifacts: `entry-draft/2026-10-19-arc3-r6-vyper-optimizer-forms.md` (corpus entry draft) + `out/`, `probe/` (8 envelopes), `evidence/`, `scripts/` under this seat dir.

## 0. Why this Unknown and not a re-verification of EX-7

EX-7's viaIR entry is complete (entry draft + 15/15 probe legs + byte walk). Re-verifying it would be a duplicate c2 deliverable, and the r4 entry's Unknown is still open and explicitly names the non-default Vyper forms as **probed but not byte-characterized**. This seat closes that half. I did independently cross-check EX-7's **artifact bytes** (not its prose): see §5.

Peer context (read after their artifacts landed): CR-3, CR-4, EX-6 and EX-9 all took the "verify EX-7" branch; EX-9.md:137 and CR-4.md:187 explicitly record the Vyper `-O codesize`/`--no-optimize` Unknown as **left open for a different seat**. That is the seat, and this artifact is its closure — no overlap with the four viaIR verifications.

## 1. Re-derived first-hand (rule #14) — nothing quoted from a prior seat or round

| item | verdict | first-hand evidence |
|---|---|---|
| Command A before-state at work commit `58c3db7` | **REPRODUCED** | ran the `SCORECARD.md:88-124` recipe verbatim → `{"citation_resolved_rules":14,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":84,"mapped":84,"missing":[],"revision":"58c3db7","rule_blocks":14}` — saved `evidence/command-A-before.json`; identical JSON at records HEAD `c625d5d` (run in this seat) |
| Corpus file count discrepancy | **RECORDED** | `git ls-tree -r --name-only c625d5d -- corpus/knowledge` = 85 paths; one is `corpus/knowledge/.gitkeep` (non-`.md`, filtered by command A), so `knowledge_files=84` — the 85th is not an entry |
| HEAD state | **REPRODUCED** | `git log --oneline -3` → `c625d5d` records / `58c3db7` work / `71668cc` r4 records, matching the dispatch brief |
| The Unknown is real and still open | **VERIFIED** | `grep -rn "no-optimize\|nooptimize\|codesize\|-O none" corpus/knowledge/*.md` → only the r4 entry's source-provenance line (`:5`) and its Unknowns paragraph (`:28`); no corpus entry byte-characterizes the forms |
| Vyper toolchain (read-only reuse, no new install) | **REPRODUCED** | `.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper --version` → `0.4.3+commit.bff19ea2`; `sha256sum` → `615f792c…9dd10`; interpreter `/usr/bin/python3.14` (Python 3.14.7) |
| Carrier sources are the pinned r4 bytes | **REPRODUCED** | my scratch copies: `CarrierV.vy` sha256 `f4f94727…4b63`; `Ex09Vault.vy` sha256 `3798f8af…2ac24` — custody paths `…/arc3-loop1-round4/claims/c1/EX-04/src/CarrierV.vy`, `…/EX-09/vyper/Ex09Vault.vy` |
| Same-source/toolchain check | **REPRODUCED** | my default (`-O gas`) CarrierV runtime 1,562 B sha256 `57d6fd0a…dae0` equals the r4-receipted runtime digest — the recompile is the same bytes, not a look-alike |
| Flag identities | **VERIFIED** | no flag ≡ `-O gas` (both `57d6fd0a…`); `--no-optimize` ≡ `-O none` (both `1505210b…`); stderr 0 bytes on every leg |
| Compile determinism | **VERIFIED** | re-running `-O codesize` and `--no-optimize` reproduced the first compile byte-for-byte (runtime-text sha `0ef639c0…`, `dd93b272…`) |

## 2. What was measured (all bytes first-hand this round)

Two carriers × three optimizer modes, compiled with the pinned Vyper 0.4.3 venv from the custody sources; scratch `/var/tmp/cr2-r6` (never `/tmp`):

| carrier | mode | runtime | sha256 | probe 6.4.0 | probe 6.7.0 |
|---|---|---|---|---|---|
| CarrierV (K=15) | default / `-O gas` | 1,562 B | `57d6fd0a…` | 15/15 `ev_a2ef3ba2…` | — |
| CarrierV | `--no-optimize` / `-O none` | 2,124 B | `1505210b…` | 15/15 `ev_9c8ad355…` | 15/15 `ev_981438cc…` |
| CarrierV | `-O codesize` | 1,450 B | `03a27565…` | 15/15 `ev_3d345250…` | 15/15 `ev_0c6208b4…` |
| Ex09Vault (K=7) | default | 581 B | `54b14e30…` | 7/7 `ev_9e5e7e84…` | — |
| Ex09Vault | `--no-optimize` | 806 B | `0efb8663…` | 7/7 `ev_05d53337…` | — |
| Ex09Vault | `-O codesize` | 572 B | `360e914d…` | 7/7 `ev_58859331…` | — |

Every leg: zero missing / zero extra against the compiler's ABI + `method_identifiers` oracle; every function `dispatch:"abi"`; decoded `bytecode.sha256` = runtime-file sha256; `discovery_completeness: unknown`. Full matrix: `evidence/probe-matrix.txt`; envelope digests: `evidence/probe-envelope-sha256.txt`.

### The three shapes

- **Form A (control, r4 class re-measured):** MOD-indexed 2-byte-entry CODECOPY table + 15/7 chained `PUSH4 DUP2 XOR PUSH2 next JUMPI` legs; no `EQ` in the chain. Offset = `push4_pc + 11`; 0/15 and 0/7 on JUMPDESTs.
- **Form B (`--no-optimize`/`-O none`, new):** fixed calldatasize guard in the prologue, then `PUSH4 <sel> DUP2 EQ ISZERO PUSH2 <next> JUMPI` legs (15 CarrierV / 7 Ex09Vault), monotone; every next-target is a JUMPDEST; match falls into a per-function guard stub. Offset = `push4_pc + 12`; 0/15 and 0/7 JUMPDESTs.
- **Form C (`-O codesize`, new):** two-level **perfect-hash** table dispatcher. `bucket = sel & (nbuckets−1)`; 5-byte level-1 entry `[multiplier:2][record_base:2][count:1]`; `slot = ((multiplier*sel) >> 24) % count`; 7-byte record `[selector:4][dest:2][guard:1]`; `dest` = jump target. Verified: hash-slot identity on **22/22 records**, every `dest` a JUMPDEST (22/22); CarrierV 2 buckets (multipliers `0x000a`, `0x0a1f`; counts 5, 10; bases `0x541`, `0x564`), Ex09Vault 1 bucket (mult `0x0092`, count 7, base `0x20b`). No selector-shaped `PUSH4` in the dispatch region; the probe's offset is a **single constant for every function** — 73 (CarrierV) / 65 (Ex09Vault), byte `0x80` — the shared match-path head.

Structural walk output: `evidence/form-structure.txt` (reproduce with `scripts/verify_forms.py`); disassembler `scripts/evmdis.py`, concrete stepper `scripts/minievm.py`.

## 3. Per-item verdicts

| # | item | verdict | evidence (exact) |
|---|---|---|---|
| 1 | Form B is a linear `EQ/ISZERO` chain, not the default XOR chain | **VERIFIED** | `evidence/form-structure.txt`: CarrierV noopt 15 legs `shape_ok=True`; `EQ` 22× / `XOR` 0× runtime-wide; Ex09Vault noopt 7 legs `shape_ok=True`, `EQ` 9× / `XOR` 0× |
| 2 | Form B offset rule = `push4_pc + 12` | **VERIFIED** | probe offsets minus my opcode-boundary PUSH4 pcs → distinct `[12]` on 15/15 and 7/7; bytes at offset ∈ {`0x34`,`0x60`}; 0 JUMPDESTs |
| 3 | Form C is a two-level perfect-hash table | **VERIFIED** | `evidence/form-structure.txt`: CarrierV `perfect-hash slot identity on every record: True`, `all 15 record dests are JUMPDEST: True`; Ex09Vault `True`, `True` (7). Entry bytes and multipliers listed in §2 |
| 4 | Form C's probe offset is per-function degenerate | **VERIFIED** | probe offsets `{73}` (CarrierV 15 fns) and `{65}` (Ex09Vault 7 fns); byte at 73/65 = `0x80` (`DUP1`), not a JUMPDEST; the per-function `dest` lives inside each record and *is* a JUMPDEST |
| 5 | Selector recovery is exact on all three forms | **VERIFIED** | probe matrix: 15/15 and 7/7, `missing=[] extra=[]` against ABI/`method_identifiers` (oracle filtered to ABI function names); 6.7.0 cross-pin identical decoded sha |
| 6 | Form C has no selector-shaped `PUSH4` in the dispatch region; a linear PUSH4 sweep is the wrong instrument | **VERIFIED** | opcode-boundary PUSH4 census: Form C CarrierV 7 sites = 6× `08c379a0` + one table-data coincidence `04e0749a` at pc 1371 (straddles two 7-byte records, not dispatched, not reported); Ex09Vault 2 sites, both `08c379a0` |
| 7 | Mutability inference degrades on the non-default forms | **VERIFIED** | CarrierV deltas vs ABI: 8/15 (A), 14/15 (B), 14/15 (C); Ex09Vault: 2/7, 6/7, 6/7; every delta → `payable`; no selector misassigned |
| 8 | `__default__()` phantom reproduces under all forms | **VERIFIED** | `89402a72` absent by byte search from all six runtimes; `method_identifiers` 16/8 keys vs 15/7 ABI function entries |
| 9 | Compiled bytes reproduce the r4 default digest (same source/toolchain) | **REPRODUCED** | `57d6fd0a…` for CarrierV default; `54b14e30…` for Ex09Vault default |
| 10 | Projected command A after landing this entry alone | **VERIFIED (measured in scratch repo)** | scratch git repo (`corpus/knowledge` + `README.md` with token + `SKILL.md`, entry file present) rev `31e82dae…` → `knowledge_files 85, mapped 85, missing [], dangling [], coverage 10.0, rule_blocks 14, depth 10.0` → `evidence/command-A-projected.json`. This is a **projection**, not a lane-commit measurement |

## 4. Landing moves for the parent (command A 84 → 85)

1. Copy `.ufo/waves/arc3-loop1-round6/claims/c2/CR-2/entry-draft/2026-10-19-arc3-r6-vyper-optimizer-forms.md` → `corpus/knowledge/`.
2. Append the token to the EVM row (`corpus/README.md:38`):

```diff
-| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-evm-optimizer-shapes`, `2026-10-19-arc3-r4-evm-vyper-leg` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07) and from real solc-0.8.37-compiled runtime carriers (arc3-r1); positional encoding quirk |
+| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-evm-optimizer-shapes`, `2026-10-19-arc3-r4-evm-vyper-leg`, `2026-10-19-arc3-r6-vyper-optimizer-forms` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07), real solc-0.8.37 carriers (arc3-r1/r3), Vyper 0.4.3 carriers (arc3-r4) and Vyper 0.4.3's non-default optimizer forms (arc3-r6: linear EQ chain and two-level perfect-hash table); positional encoding quirk |
```

3. Post-landing command A must be re-run; the measured projection is 85/85/[]/[] with `rule_blocks` untouched (depth is the c3 chain's axis). If EX-7's viaIR entry lands in the same commit, the file count is 86 (85 + 1) and its token must be added too — the parent should land one measurable commit and re-measure, not add projections.
4. No SKILL.md, PROVINCE.md, gate, or tracked file was touched. Write scope ended at this artifact dir.

## 5. Independent cross-check of EX-7's delivered viaIR artifact (not a re-verification of prose)

Read-only, first-hand this seat:
- Recompiled EX-7's `src/ViaIrVault.sol` (sha256 `f5391167…80cbbe`) with their `scripts/compile.js` and the pinned solc `0.8.37+commit.f401782d` (wave-1 prefix) into `/var/tmp/cr2-r6/ex7-recheck/`: viair-opt200 runtime **1,517 B `2ec3f557…`**, viair-noopt **4,144 B `0cc6938c…`**, std-opt200 control **1,921 B `c2ceabb1…`** — all equal to the digests their artifacts record.
- My own disassembly of `viair-opt200/runtime.bin`: prologue `5f3560e01c` at pc 35; 14 `PUSH4 <sel> EQ PUSH2 <dst> JUMPI` legs at pcs 41..184, strict 11-byte stride (41,52,63,…,184); 15th leg at pc 194 is `PUSH4 ee02438e SUB PUSH2 0x000e JUMPI` (`SUB` 0x03, not `EQ`), next pc 204. Their sealed envelope reports offsets equal to each EQ leg's `PUSH2` destination for 14/15, and 204 for the `ee02438e` leg (= `push4_pc + 10`, the post-`JUMPI` fall-through) — matching the shape claim.
- Verdict: **VERIFIED** for byte reproducibility and the dispatch-shape claim. I did **not** re-run their probe legs (their envelopes are sealed; my check is compile + bytes). Landing of their entry remains their chain's/parent's call.

## 6. Custody & scope

- All evidence retained under `.ufo/waves/arc3-loop1-round6/claims/c2/CR-2/`: `entry-draft/` (1), `out/` (26: 6 legs × {runtime.hex, runtime.bin, abi.json, methodids.json} + 2 retained sources), `probe/` (8 sealed envelopes), `evidence/` (compile receipt, probe matrix, form structure, envelope digests, command-A before/projected JSON, 2 repo-path rechecks + stderr), `scripts/` (3).
- Scratch `/var/tmp/cr2-r6` only; `TMPDIR=/var/tmp/cr2-r6/tmp` for every probe (a `/tmp`-defaulted run fails EDQUOT, errno −122).
- Custody reads only: r4 vyper venv and carrier sources (read-only), prior corpus entries, SCORECARD/QUALITY/README — no tracked file modified. `git status` after this seat: the pre-existing ` M .ufo/waves/arc2-loop1-round10/C3.md` plus untracked `.ufo/waves/arc3-loop1-round6/`; nothing else.
- Honest limits: one compiler version (0.4.3), two carriers (K=15, 7), one source family, runtime 572–2,124 B; 6.7.0 cross-pin on CarrierV B/C only; the Form C `guard` byte is only partially decoded; the perfect-hash multipliers are observed values, not a derived rule; the projected 85 is a scratch-repo projection, not a lane measurement.
