# CR-1 — c2 chain (corpus Unknown) — arc3-loop1-round6

Seat: CR-1 · chain c2 · 2026-10-19 · lane `kaidoku-shokunin` · wave `arc3-loop1-round6`.
Target claim: **C2 — close one named corpus Unknown.** Chosen Unknown: the **Vyper 0.4.3 non-default
optimizer forms** (`--no-optimize` / `-O none` / `-O codesize`) and the **hardfork variants** named as
probed-K/K-but-not-byte-characterized at `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28`.
This is the residual that names this seat's own r4 variants, so no delivered peer artifact is
duplicated (EX-7's viaIR entry stands as delivered; PL-4/SC-3 are c1/c3 and out of this chain).
Other c2 seats converged on the same Unknown in parallel; the reconciliation is in §2b below and
their values are **not** used as evidence for any row in §0 (rule #14).
Deliverable: corpus entry draft at `entry-draft/2026-10-19-arc3-r6-vyper-optimizer-forms.md`
(parent lands it) + coverage-map token patch + evidence tree under `CR-1/`.

## 0. Re-derived first-hand (rule #14) — nothing quoted from a prior seat or round

| item | verdict | first-hand evidence |
|---|---|---|
| Command A before-state at HEAD `c625d5d` | **REPRODUCED** | ran the `SCORECARD.md:88-124` recipe verbatim (`python3 - c625d5d`) → `{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "rule_blocks": 14}` |
| HEAD / work commits | **REPRODUCED** | `git log --oneline -5` → `c625d5d` (records) / `58c3db7` (work), matching the dispatch brief |
| The Unknown is real and still open | **VERIFIED** | `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28` names "CR-1's `--no-optimize` / `-O codesize` / `-O none` and hardfork variants … not byte-characterized here"; `grep -rn -i "codesize\|no-optimize\|noopt" corpus/knowledge/*.md` hits only r3 (the solc optimizer entry, different family) and `r4:28` itself — no later entry closes the Vyper forms |
| Compiler | **REPRODUCED** | `vyper --version` → `0.4.3+commit.bff19ea2`; binary sha256 `615f792c…09dd10` (r4 wave venv, read-only reuse; no new install) |
| Carrier source identity | **REPRODUCED** | `K8.vy` sha256 `62549f79…ea7d`; ABI 8 function entries, all `@view`; selectors re-derived by my own Keccak-256 (selftest 3/3 published vectors), the compiler's `method_identifiers`, and the probe payload — three agreements |
| Nine compile legs vs the pinned r4 carriers | **REPRODUCED (9/9 byte-identical)** | `evidence/compile-receipt.txt`: default 418 B `72e5d886…`; `-O none` = `--no-optimize` 617 B `1a7bf2cd…`; `-O codesize` 360 B `bf5afe48…`; paris = london 423 B `d1af44a9…`; cancun = shanghai = prague = default 418 B `72e5d886…` — every runtime and every hex-text digest equal to the r4 artifact |
| Probe legs (rea 6.4.0 / 6.7.0) | **REPRODUCED** | `evidence/probe-summary.txt`: A/B/C × hex and true raw-bin, paris/london, B/C at 6.7.0 → every leg **8/8**, zero missing/extra, decoded `bytecode.sha256` equal to my sha256 of the carrier bytes (ids `ev_13545160…`, `ev_0a200d34…`, `ev_d6383be8…`, `ev_13da3d54…`, `ev_7de5ee79…`, `ev_65d643b9…`, `ev_8f05fd7d…`, `ev_04bb7801…`, `ev_aff667b8…`, `ev_14c00481…`, `ev_771620f4…`, `ev_029e3490…`) |
| Form A default shape | **VERIFIED** (matches the r4 third class) | 418 B; `5f3560e01c`; 9-bucket `MOD` table at **0x190**, entries `[0x188,0x188,0x0fe,0x12c,0x0a2,0x018,0x188,0x15a,0x074]`, all targets JUMPDEST; buckets 0/1/6 empty; collisions 5 (`f0`,`f7`) and 4 (`f2`,`f4`); chain `PUSH4 sel DUP2 XOR PUSH2 next JUMPI`, 8 sites 25…347 stride 46; zero `EQ` in code; bodies at `push4_pc+11` (`evidence/form-summary.txt`, `offset-table.txt`) |
| Form B `--no-optimize` / `-O none` | **VERIFIED (new measured shape)** | 617 B `1a7bf2cd…`; no MOD/CODECOPY/bucket table; guard `PUSH1 4 CALLDATASIZE LT ISZERO PUSH2 0x000d JUMPI PUSH2 0x0260 JUMP`; linear **source-order** chain of 8 `PUSH4 sel DUP2 EQ ISZERO PUSH2 next JUMPI` at pcs 19,92,165,238,311,384,457,530 (stride 73), `EQ`×8, `XOR`×0; bodies fall through at **`push4_pc+12`** into `CALLVALUE ISZERO ISZERO …` / `PUSH1 0x24 CALLDATASIZE LT ISZERO ISZERO …` then `PUSH2 <arith> JUMP` |
| Form C `-O codesize` | **VERIFIED (new measured shape)** | 360 B `bf5afe48…`; **zero `PUSH4`**; header at 299 `01c3013008` = `[u16 mult=451][u16 base=0x130=304][u8 count=8]`; 8 entries × 7 B at 304…360 = end of code; entry `sel[4] | dst[2 BE] | guard-byte`; index `((451*sel)>>24)%8` is **perfect** (each entry at its own index, `evidence/formula-C.txt`); all 8 dsts JUMPDEST (91/116/141/166/191/216/241/266); guard `0x25` = calldata floor 36 + nonpayable bit |
| Guard-byte semantics | **VERIFIED (measured, not inferred)** | `K8pay.vy` (f0 `@view`→`@payable`, same selectors) compiled `-O codesize` → f0 guard byte `0x24` (payable bit 0), the seven `@view` entries `0x25`; Form A equivalent 417 B vs 418 B because the payable guard omits `CALLVALUE OR` (`evidence/payable-guard.txt`) |
| Offset convention | **CORRECTED** | Form A `push4_pc+11`, byte `0x60`; Form B `push4_pc+12`, byte `0x34`; Form C **constant 65** (`DUP1`), not per-function — per-function handler is the table dst. **0/8** offsets are JUMPDESTs in every form. Unified: offset = match-path fall-through after the compare's conditional jump; per-function only where the fall-through is. The r4 `+11`/`0x60` rule (`…r4-evm-vyper-leg.md:22`) is **Form-A-scoped** |
| Hardfork variants | **VERIFIED, with a new confound** | london = paris (423 B), cancun = shanghai = prague = default (418 B); whole delta = **five `PUSH0`→`PUSH1 00`** expansions + relocation; table base 0x190→0x195 (+5), first-body targets +2. The paris/london Form-A prologue is **`60003560e01c`** — the same head as r1's solc linear class (`…r3-evm-optimizer-shapes.md:28`, prologue list `…r1-evm-real-solc.md:29`); prologue identifies neither compiler nor pipeline (`evidence/hardfork-diff.txt`) |
| Trap class | **REPRODUCED** | hex file fed as `raw` on A/B/C → exit 0, 0 functions, decoded sha = the hex *text* file digest (A `b1f7fc88…`, B `1dfe2699…`, C `c4af8ebc…`); true raw-bin legs 8/8. Parsed-and-empty ≠ byte absence (`corpus/QUALITY.md:21`) |
| Mutability delta | **REPRODUCED on all three forms** | every function reads `payable` while the ABI says `view` for all 8 — the r4 payable-read class (`…r4-evm-vyper-leg.md:24`) persists on default, no-optimize and codesize output |
| K-dependence of the codesize shape | **VERIFIED (scope limit)** | a 2-function payable/view carrier compiled `-O codesize` = **103 B, byte-identical to `-O gas`** (linear XOR chain, no bucket table; `evidence/payable/k2-codesize.txt`). The packed-table Form C is measured at K=8 only |
| Peer-instrument cross-check | **DISCREPANCY (recorded)** | EX-08's `recon.py extract` on the current file: A → 8 via `vyper_chain` (strict chain 0); B → **8 via `dispatch_eq_selectors`** (strict chain 0); C → **0 on every counter**. The r4 source-line claim that the same script "returns 0 on the `--no-optimize` … form" is **not reproducible** against the file in the r4 tree; the codesize 0/8 claim is reproduced exactly. See `evidence/recon-crosscheck.txt`; no corpus file was modified |
| Projected command A after landing | **PROJECTED (not a post-landing measurement)** | file-based recipe over `HEAD + entry + token` (`evidence/projection.txt`): `{"knowledge_files": 85, "mapped": 85, "missing": [], "dangling": [], "citation_resolved_rules": 14, "rule_blocks": 14, "coverage_score": 10.0, "depth_score": 10.0}` |

## 1. Landing moves for the parent (command A 84 → 85)

1. Copy `CR-1/entry-draft/2026-10-19-arc3-r6-vyper-optimizer-forms.md` → `corpus/knowledge/`.
2. Append the token `2026-10-19-arc3-r6-vyper-optimizer-forms` to the **EVM** row of the coverage map (`corpus/README.md`, the row currently reading
   ``| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-evm-optimizer-shapes`, `2026-10-19-arc3-r4-evm-vyper-leg` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07) and from real solc-0.8.37-compiled runtime carriers (arc3-r1); positional encoding quirk |``). Patch text:

```diff
-| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-evm-optimizer-shapes`, `2026-10-19-arc3-r4-evm-vyper-leg` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07) and from real solc-0.8.37-compiled runtime carriers (arc3-r1); positional encoding quirk |
+| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-evm-optimizer-shapes`, `2026-10-19-arc3-r4-evm-vyper-leg`, `2026-10-19-arc3-r6-vyper-optimizer-forms` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07), real solc-0.8.37 carriers (arc3-r1/r3), Vyper 0.4.3 carriers (arc3-r4) and the Vyper optimizer/hardfork forms (arc3-r6, three dispatch topologies); positional encoding quirk |
```

3. Nothing else changes: no SKILL.md, no PROVINCE.md, no gate, no corpus erratum by this seat. The
   projected `85/85` line is a projection until the parent lands and re-runs command A.

## 2b. Peer convergence (c2 chain; reconciliation only, not evidence for §0)

Four other c2 seats independently targeted the same Vyper non-default-optimizer Unknown while this
seat ran: **CR-2** (CarrierV K=15 + Ex09Vault K=7, 15/15 and 7/7), **EX-8** (own 13-function carrier +
EX-7 verification), **EX-10** (CarrierV K=15) and **EX-12** (own 13-function carrier). Read-only
comparison of their artifacts says their first-hand measurements **converge** with mine on the rules
this seat claims: Form B = linear `EQ`+`ISZERO` chain with `push4_pc+12`; Form C = perfect-hash
dispatcher with 5-byte header `[mult:2][base:2][count:1]`, 7-byte records `[sel4][dst2][flag1]`, and a
**shared per-runtime** probe offset (their 73/68 vs my 65) with byte `0x80`; the r4 `+11` rule is
optimizer-form-scoped; the codesize flag byte tracks calldata floor + payability (their `0x04`/`0x05`
zero-arg rows are consistent with my measured payable bit).

Two integration-relevant deltas:
- **Codegen variant at larger K.** CR-2/EX-8/EX-10 describe a **two-level** perfect-hash table (a
  level-1 5-byte entry selected by selector bits) on K=15/13 carriers, whereas my K=8 carrier has a
  single 5-byte header at 299. My entry is K=8-scoped and lists other K as Unknown; the integrator
  should merge the larger-K level-1 variant from those seats rather than generalize mine.
- **Entry count.** EX-12 measured in a scratch git tree that any single r6 token gives 85/85 and
  **both** r6 tokens (viaIR + Vyper) give **86/86**. My projection (85/85) is for this entry alone;
  landing EX-7's viaIR entry and a Vyper entry together makes command A 86/86 — a wave-level decision,
  and the C2 84→85 line is per single entry.
- **Stem collision.** CR-2, EX-8, EX-10 and EX-12 propose the same entry stem
  `2026-10-19-arc3-r6-vyper-optimizer-forms`; only one file can land under that stem (or the drafts
  must be merged). This seat's draft is K=8-scoped; the integrator should select/merge with the
  larger-K evidence from those seats (EX-8/EX-10 carry K=13/15 dispatcher walks).

## 2. What this closes, and what it leaves

- Closes, for **vyper 0.4.3 on this host**, the non-default-optimizer/hardfork half of the r4 Unknown:
  both new shapes are characterized at byte level, K/K 8/8 on every leg, with recompiled byte-identity
  and the offset convention stated per form. The Entry's `Unknowns` list narrows the rest (other Vyper
  versions, other K / bucket counts / multipliers, the codesize K-threshold, B/C under non-default
  hardforks, multi-argument guard bytes, fallback-bearing carriers, the `ev_` id domain).
- Flagged for the parent/VZ: the EX-08 `recon.py` Form-B claim in the r4 entry's source line is
  stale/incorrect as written (current file returns 8, not 0). The entry records the measured behavior;
  whether to file an append-only r4 erratum is the integrator's call.

## 3. Custody & scope statement

- All evidence is retained under `.ufo/waves/arc3-loop1-round6/claims/c2/CR-1/`: `entry-draft/`,
  `evidence/{keccak.py,disasm.py,sim.py,analyze.py,selftest.txt,compile-receipt.txt,form-summary.txt,
  offset-table.txt,formula-C.txt,hardfork-diff.txt,payable-guard.txt,probe-summary.txt,
  recon-crosscheck.txt,an-K8*.json,payable/,probe/*.json}` and `manifest.sha256`.
- Scratch was `/var/tmp/cr1-r6/` (never `/tmp`); every probe leg used
  `TMPDIR=/var/tmp/cr1-r6/tmp` (the standing EDQUOT rule).
- Custody reads only: the r4 carrier/venv tree, corpus entries, README/QUALITY/SCORECARD, EX-08's
  `recon.py` (executed read-only). No tracked file was modified; git was read-only (`show`, `log`,
  `ls-tree`). Write scope ended at this artifact dir.
- Honest limits: one Vyper version, one carrier family, K=8 (plus one K=2 shape probe), one compiler
  host; REA pins 6.4.0/6.7.0 only; the projected-85 line is a projection until landing.
