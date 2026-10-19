# EX-5 — c2 chain (corpus Unknown closure + EX-7 verification) — arc3-loop1-round6

Seat: EX-5 · chain c2 · 2026-10-19 · lane `kaidoku-shokunin` · roster per `.ufo/waves/arc3-loop1-round6/claims-frozen.md` (third delivery state; dispatch provider substitution chain recorded there, not a lane signal).
Target claim: **C2 — close one named corpus Unknown** (`claims-frozen.md` §C2).
Chosen Unknown: the **Vyper 0.4.3 non-default optimizer forms** — `--no-optimize` / `-O none` / `-O codesize` and the hardfork variants — named at `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28` as "probed K/K by the probe but their dispatcher forms were not byte-characterized here, and a shape-blind extractor returns empty on them — the false-honest-stop hazard."

**Verdict in one line:** the Unknown **CLOSES for Vyper 0.4.3 on this host**, measured first-hand on two primary carriers (K=8, K=7) and two scope probes (K=15, K=2): every leg K/K, three dispatcher classes byte-characterized, offset conventions measured (`+11` / `+12` / shared 65 or 73), `-O none` == `--no-optimize` byte-identically, hardforks shape-stable, and the packed `-O codesize` form shown to **fall back to the gas form at K=2** (a scope limit the draft states). EX-7's delivered `viaIR` entry is **independently VERIFIED** by recompiling its source byte-identically, re-probing its hex/std/creation/raw-on-hex paths, and re-walking its dispatch bytes. Four c2 peers independently closed the same Vyper Unknown while this seat ran; §5 reconciles their claims against my bytes — **agreement on every overlapping item**, with two detail corrections recorded (one to r4's CODECOPY phrasing, one to the r4 zero-arg-mutability half).

## 0. Baseline re-derived first-hand (rule #14 — nothing quoted)

| Item | Verdict | First-hand evidence |
|---|---|---|
| Command A at work commit `58c3db7` | **REPRODUCED** | ran the `SCORECARD.md:88-124` recipe verbatim → `{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "rule_blocks": 14, "revision": "58c3db7"}` |
| HEAD / work commits | **REPRODUCED** | `git log --oneline -2` → `c625d5d` (records) / `58c3db7` (work) |
| The Unknown is still open at HEAD | **VERIFIED** | `grep -rn -i "no.optimize\|codesize\|perfect.hash" corpus/knowledge/*.md` returns exactly one substantive hit — `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28` (the Unknown text); no entry byte-characterizes the forms |
| Vyper toolchain | **REPRODUCED** | `.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper --version` → `0.4.3+commit.bff19ea2`; `bin/vyper` sha256 `615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10`; interpreter `/usr/bin/python3` sha256 `d78f9cf7178ecff09963551399855543c297f37ac207e626228bfe43cb26a70c` — equal to the r4 record. Reused read-only, `PYTHONDONTWRITEBYTECODE=1`; no new install |
| solc toolchain (for EX-7 verification) | **REPRODUCED** | `node -e "require('.../r1/tools/solc-prefix/node_modules/solc').version()"` → `0.8.37+commit.f401782d.Emscripten.clang`; `soljson.js` sha256 `221d7a667378b5068d913e75fe092507e061363cd1d23b64c49ae82febabad4c` (equal to the r3/r4 record) |
| Wave dir state / write scope | **VERIFIED** | only this seat's `claims/c2/EX-5*` tree written; `git status --short` shows only the pre-existing `M .ufo/waves/arc2-loop1-round10/C3.md` and the untracked `arc3-loop1-round6/` wave tree |

## 1. What was built (all bytes first-hand this round)

- **Carrier K8** — the round-4 CR-1 source, copied verbatim (`src/K8.vy` sha256 `62549f79…`, 580 B). Fresh compile in four optimizer forms and five hardfork variants is **byte-identical to CR-1's custody legs** in all nine comparisons (`evidence/compile-receipt.txt`): `-O gas` 418 B `72e5d886…`; `--no-optimize` 617 B `1a7bf2cd…`; `-O none` byte-identical to `--no-optimize`; `-O codesize` 360 B `bf5afe48…`; `paris`/`london` 423 B `d1af44a9…`; `cancun`/`shanghai`/`prague` 418 B `72e5d886…`.
- **Carrier Ex05Vault** — this seat's 7-function mixed-mutability source (`src/Ex05Vault.vy` sha256 `97165346…`, 537 B): `alpha` view, `beta` pure, `gamma` nonpayable, `delta` payable (all `(uint256)`), `epsilon` view, `zeta` nonpayable, `eta` payable (zero-arg). Legs: gas 304 B `89962a90…`, noopt 473 B `a2f3b5c9…`, none identical, codesize 289 B `08eec8be…`.
- **Scope probes** — `CarrierV` (r4 custody source sha256 `f4f94727…`): fresh `-O gas` reproduces the r4-recorded 1,562 B `57d6fd0a…`; `-O codesize` 1,450 B `03a27565…` (15/15, shared offset 73). `K2` (this seat's 2-function source sha256 `2a9149e0…`): `-O codesize` is **byte-identical to `-O gas`** (103 B `726f00f3…`, 2/2).
- **Selectors** — derived independently with a pure-Python keccak-f[1600] (`scripts/keccak.py`; selftest 3/3 public vectors incl. empty-string `c5d246…` and `transfer(address,uint256)`→`a9059cbb`), agree with vyper `method_identifiers` for all 32 signatures across the four carriers, and have zero collisions with 9 known ERC-20 selectors (`evidence/selector-derivations.txt`).
- **Probes** — 18 primary sealed envelopes at 6.4.0/6.7.0 (incl. 2 traps), 4 independent EX-7 re-probes, and 2 recheck legs, all retained under `probe/` (24 files); every real leg is K/K with `dispatch:"abi"` and decoded `bytecode.sha256` equal to the runtime file (`evidence/assertions.txt`, 52 PASS lines: 48 real-leg + 4 trap; full matrix in `evidence/probe-summary.json`).
- **Byte walks** — `evidence/walk-{K8,Ex05Vault}-{gas,noopt,codesize}.json`, `evidence/two-level-codesize.txt`, `evidence/hardfork-matrix.txt`, `evidence/mutability-agreement.txt`.

## 2. Findings — per-item verdicts

| # | Item | Verdict | First-hand evidence |
|---|---|---|---|
| F1 | The named Unknown closes K/K | **VERIFIED** | K8 gas/noopt/codesize 8/8 @6.4.0+6.7.0; Ex05Vault gas 7/7, noopt/codesize 7/7 @6.4.0+6.7.0; paris/london/cancun 8/8; CarrierV codesize 15/15; K2 codesize 2/2 — zero missing/extra, decoded sha = runtime sha (`evidence/probe-summary.json`, `evidence/assertions.txt`) |
| F2 | Default `-O gas` = MOD table + XOR chains (control; r4 class) | **VERIFIED** | K8: `selector % 9`; table at 0x190 = `[0188,0188,00fe,012c,00a2,0018,0188,015a,0074]`; empty buckets 0/1/6 → sentinel 0x188; collisions 5 (`f0`,`f7`) and 4 (`f2`,`f4`); XOR legs `PUSH4;DUP2;XOR;PUSH2;JUMPI`. Ex05Vault: `% 5`, triple collisions. (`evidence/walk-*-gas.json`) |
| F2a | r4's "copies a 13-entry uint16 jump table … to memory" | **CORRECTED (detail only)** | the instruction copies **one** 2-byte entry (size operand is the earlier `PUSH1 2`; dest 30) into mem[30:32], then `MLOAD;JUMP`; the structural `bucket=sel%B → table[bucket]` conclusion stands (`evidence/walk-K8-gas.json` prologue) |
| F3 | `--no-optimize` = linear EQ+ISZERO chain, and equals `-O none` | **VERIFIED** | guard `PUSH1 4;CALLDATASIZE;LT;ISZERO;PUSH2<13>;JUMPI;PUSH2<revert>;JUMP`; then `5f3560e01c` and `PUSH4;DUP2;EQ;ISZERO;PUSH2;JUMPI` in source order; K8 legs at 19/92/…/530 (stride 73), Ex05Vault at 19/92/171/244/310/362/414; `--no-optimize` == `-O none` byte-identically on both carriers (`evidence/compile-receipt.txt`, `walk-*-noopt.json`) |
| F4 | `-O codesize` = packed perfect-hash table, one or two levels | **VERIFIED** | 5-byte header `[mult:2][base:2][count:1]`; optional level-1 selection `header_addr = base + 5*(sel & mask)`; 7-byte records `[selector:4][handler:2][tag:1]`; `index=((sel*mult)>>24)%count`; perfect on 8/8, 7/7 and 15/15; zero opcode-boundary `PUSH4` selector immediates; K8 header `01c3013008`, Ex05Vault `003700f007`, CarrierV two headers `000a054105`/`0a1f05640a` (`evidence/walk-*-codesize.json`, `evidence/two-level-codesize.txt`) |
| F4a | K-scope of the packed form | **VERIFIED (new scope limit)** | K=2 `-O codesize` == `-O gas` byte-for-byte (103 B `726f00f3…`); packed form measured at K=7, 8, 15; threshold Unknown |
| F5 | Offset conventions are form-scoped | **VERIFIED / CORRECTED (r4 rule)** | default `push4_pc+11` (14/14 legs across K8+Ex05Vault; paris/london +2 shift measured); noopt `push4_pc+12` (15/15); codesize a **single shared offset** per carrier — 65 at K=7/8, 73 at K=15 — not a per-function location. 0 reported offsets are JUMPDESTs on Vyper forms (`evidence/walk-*.json` `offset_rule`) |
| F6 | Hardfork variants: prologue substitution only | **VERIFIED** | paris==london (423 B `d1af44a9…`), cancun==shanghai==prague==default (418 B `72e5d886…`); exactly five `PUSH0`→`PUSH1 00` expansions (+5 B) plus relocation; prologue becomes `60003560e01c`; class unchanged; probes 8/8 each (`evidence/hardfork-matrix.txt`) |
| F7 | Mutability inference is optimizer-form-scoped | **VERIFIED; r4 zero-arg half CORRECTED** | K8 (all ABI `view`) reads `payable` on all forms (0/8). Ex05Vault: gas 3/7 agree (`delta`,`epsilon`,`eta`), noopt 2/7, codesize 2/7 — non-default forms read **payable for every function**. The r4 arg-taking→payable half reproduces on the default form (4/4, incl. `pure beta`); the zero-arg-agreement half does not generalize intact (`zeta()` nonpayable reads `view` on gas, `payable` on B/C) (`evidence/mutability-agreement.txt`) |
| F8 | Parsed-and-empty ≠ byte absence | **REPRODUCED** | codesize runtime.hex fed as raw → 0 functions, decoded sha = hex text sha `c4af8ebc…`; creation.hex → 0 functions, decoded sha = creation bin sha `7a019e56…`, runtime embedded at +17 of 433 B (`evidence/probe-summary.json` `trap_legs`) |
| F9 | Zero false positives | **VERIFIED** | K8/Ex05Vault default+noopt contain exactly K opcode-boundary PUSH4 sites, all planted; codesize has zero PUSH4 selector sites; no non-selector immediate reported as a function |
| F10 | Landing move 84→85 | **PROJECTED (not a post-landing measurement)** | non-mutating worktree overlay of the draft + token: `{"knowledge_files":85,"mapped":85,"missing":[],"dangling":[],"coverage_score":10.0,"rule_blocks":14,"depth_score":10.0}`; with EX-7's entry also landed: 86/86. Baseline overlay without edits reproduces 84/84 |
| F11 | Entry recheck command at the artifact path | **REPRODUCED** | `TMPDIR=/var/tmp/r6-ex05-recheck npx -y rea-agents@6.4.0 inspect-evm-interface .ufo/waves/arc3-loop1-round6/claims/c2/EX-5/out/K8.noopt.runtime.hex hex --format json` → 8 functions, decoded `1a7bf2cd…`, offsets `{31,104,177,250,323,396,469,542}` (`ev_2dcfb51f…`); codesize → 8 functions, decoded `bf5afe48…`, offset `{65}` (`ev_ea55aa49…`) — `evidence/recheck-artifact.txt` |

## 3. EX-7 independent verification (per-item verdicts)

Method: recompiled EX-7's `src/ViaIrVault.sol` with its own `scripts/compile.js` and the receipted wave-1 solc prefix (read-only, outputs in `/var/tmp/ex05-r6/ex7-recompile`), re-probed at **my own paths** (new `ev_` ids), and re-walked the bytes with this seat's disassembler.

| EX-7 claim | My verdict | My evidence |
|---|---|---|
| three compile legs byte-exact (`2ec3f557…` 1,517 B; `0cc6938c…` 4,144 B; `c2ceabb1…` 1,921 B; creation `d85fdde9…`/`f1125049…`/`4541fd49…`) | **REPRODUCED** | fresh compile produced exactly those shas/sizes for all three legs; solc 0.8.37, `soljson.js` `221d7a66…` |
| viair-opt200 hex 15/15, decoded sha = runtime sha; 6.7.0 also 15/15 | **REPRODUCED** | my probe `ev_71da9d37…`: 15 functions, dispatch abi ×15, decoded `2ec3f557…`; my `verify-ex7.json` selector set equals my own keccak derivation from the ABI (15 signatures) |
| prologue/guard: `6080604052 60043610 15 61<0022> 57 5b 3615 61<0018> 57 5f80fd 5b … 5f3560e01c` | **VERIFIED** | exact bytes in `evidence/verify-ex7.json` `prologue_hex`; inverted guard carries `ISZERO` |
| 14 `DUP1 PUSH4 sel EQ PUSH2 dst JUMPI` legs, 11-byte stride, ascending, dsts 253–982, all JUMPDESTs | **VERIFIED** | my walk: 14 EQ legs, `eq_pc_gaps=[11]`, ascending `true`, dsts exactly 253/272/311/340/374/425/485/572/631/694/723/771/935/982, all JUMPDESTs |
| 15th leg `PUSH4 ee02438e SUB PUSH2 0x000e JUMPI`; match falls through into `mark` (opt200 at 204 `CALLVALUE; PUSH2 0x00f9 JUMPI`) | **VERIFIED** | SUB leg at push4 pc 194, selector `ee02438e`, dst 14; next pc 204 = `CALLVALUE; PUSH2 0x00f9; JUMPI` |
| 19 opcode-boundary PUSH4 sites = 15 selectors + `4e487b71`×2 + `0c2eae8d` + `3c3332b9` | **VERIFIED** | exact list at pcs 553/1094/1143/1261; 15 distinct selectors, no GT-pivot duplication |
| offsets: 14/15 = EQ dst (JUMPDEST), `mark` = 204 = push4+10, byte `0x34`/`0x61`, not JUMPDEST | **VERIFIED** | my probe offsets match; `offset_rule` shows 14 equal-dst rows and `mark` {reported 204, push4 194, dst 14, is_jumpdest false} |
| std control: GT/EQ binary search, GT pivots `6e69f38c`@19, `90ab171e`@30, `3f4ba83a`@137; 15 EQ + 3 GT; 18 selector sites / 15 distinct | **VERIFIED** | my walk + my std probe (15/15, decoded `c2ceabb1…`, `ev_7e7e340c…`); GT legs exactly those three selectors/pcs/dsts 135/87/194 |
| viaIR-noopt "same shape", chain dsts 208–273, SUB final leg at 194 | **VERIFIED (nuance)** | 14 EQ legs at 11-byte stride, dsts 208..273; those dsts are 5-byte trampoline blocks (`JUMPDEST PUSH2 handler JUMP`), not handler heads — consistent with EX-7's wording ("same shape") but worth stating; SUB at 194 → dst 14; runtime `0cc6938c…` |
| creation probe parsed-and-empty, decoded sha = creation sha; runtime embedded at +43; raw-on-hex decoded sha = hex text sha `19838d66…` | **REPRODUCED** | my own probes: creation 0 functions, decoded `d85fdde9…` (`ev_5b422197…`); raw-on-hex 0 functions, decoded `19838d66…` (`ev_a8e478bf…`); embedding recomputed at +43 of 1,560 B |
| CBOR trailer: `a2 64 69706673 58 22 <ipfs 2022958d9b…5d64> 73 736f6c63 43 000825 00 33` (solc 0.8.37) | **VERIFIED** | my byte decode of the tail; solc version bytes `0x000825` |
| landing projection 84→85 | **PROJECTED** | my overlay: 85/85; with my Vyper entry also landed, 86/86 |

**EX-7 verdict: VERIFIED.** No substantive discrepancy found. One nuance (viaIR-noopt dsts are trampolines) and no arithmetic/prose correction needed on the items checked. EX-7's own `evidence_id`s are path-sensitive and differ from mine as expected; comparison is by decoded sha + function payload.

## 4. What is actually being landed (this seat's entry)

Draft: `entry-draft/2026-10-19-arc3-r6-vyper-optimizer-dispatchers.md` (17 KB), plus map-token patch in §5. Its claims are exactly §2's F1–F9; its scope statement is K=7/8/15 for the packed form, K=2 fallback measured, Vyper 0.4.3 only. It cites only wave-tree evidence and custody r4 sources, not peer entries or prior-round numbers as evidence.

## 5. Peer reconciliation (same Unknown chosen by four peers)

While this seat ran, `EX-8`, `EX-10`, `CR-1` and `CR-2` independently closed the same r4 optimizer-form Unknown, and `EX-6`, `EX-9`, `EX-11`, `EX-12`, `CR-3`, `CR-4` verified EX-7. I did not use their numbers as evidence; I re-measured the overlapping items on my own carriers.

| Peer claim (as claim under test, not evidence) | My independent measurement | Verdict |
|---|---|---|
| EX-8: `-O codesize` single 5-byte header + 13×7-byte records, zero selector PUSH4, shared offset 65; noopt `push4+12`; paris shifts +2 | same class on K8 (8 records, shared 65) and Ex05Vault (7 records, shared 65); noopt `+12`; paris +2; K=13 bucket count not re-measured (different carrier) | **AGREE in class**; their carrier-specific counts are their scope |
| EX-10: CarrierV `-O codesize` is **two-level** (2 headers, mult 10/2591, bases 0x541/0x564, counts 5/10), shared offset 73; default `+11`, noopt `+12` | fresh compile of the same custody `CarrierV.vy` reproduces 1,450 B `03a27565…`; headers and records parse exactly as two-level; 15/15 perfect; shared offset 73; `+11`/`+12` reproduced on my carriers | **AGREE** (independently reproduced) |
| CR-1: K8 forms byte-identical to custody; table entries; shared 65; hardfork `+5` PUSH0 delta; **K=2 codesize == gas** | all reproduced on K8; my own K2 carrier (different source) also gives codesize==gas, 103 B `726f00f3…` | **AGREE** (K2 reproduced on an independent carrier) |
| CR-2: CarrierV + Ex09Vault two-level; phantom `__default__()` selector absent; mutability degradation on B/C | CarrierV half reproduced (two-level, phantom 89402a72 absent from runtime); Ex09Vault not compiled by me; my Ex05Vault independently shows the B/C mutability degradation (2/7 agree) | **PARTIAL/AGREE** — CarrierV and mutability-class reproduced; Ex09Vault carrier-specific values not re-measured here |
| EX-8/EX-10/CR-1/CR-2 "one entry suffices" | four drafts target the same Unknown; landing all four would inflate the corpus by four files for one closure | **Recommendation:** land **one** Vyper optimizer-form entry. EX-10/CR-2 carry the most general two-level grammar; CR-1 and this seat carry the K-scope/fallback and an independent mixed-mutability carrier. Merge the K=2 fallback + mutability counts into the chosen draft rather than landing duplicates. |
| EX-6/EX-9/EX-11/EX-12/CR-3/CR-4 verified EX-7 | my independent verification agrees: recompile byte-identical, 15/15 (hex + std), traps reproduce, no discrepancy found | **AGREE**; no conflicting verdict observed |

## 6. Landing moves for the parent (c2)

1. Choose **one** optimizer-form draft (see §5; if this seat's is chosen, copy `EX-5/entry-draft/2026-10-19-arc3-r6-vyper-optimizer-dispatchers.md` → `corpus/knowledge/`).
2. Append the token to the EVM row (`corpus/README.md:38`). For this draft:

```diff
-| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-evm-optimizer-shapes`, `2026-10-19-arc3-r4-evm-vyper-leg` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07) and from real solc-0.8.37-compiled runtime carriers (arc3-r1); positional encoding quirk |
+| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-evm-optimizer-shapes`, `2026-10-19-arc3-r4-evm-vyper-leg`, `2026-10-19-arc3-r6-vyper-optimizer-dispatchers` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07), real solc-0.8.37 carriers (arc3-r1/r3), Vyper 0.4.3 carriers (arc3-r4) and all three Vyper 0.4.3 optimizer-form dispatcher classes (arc3-r6); positional encoding quirk |
```

3. Projected command A (non-mutating overlay, **not** a substitute for the post-landing measurement):
   - this draft alone: `{"knowledge_files":85,"mapped":85,"missing":[],"dangling":[],"coverage_score":10.0,"rule_blocks":14,"depth_score":10.0}`;
   - this draft + EX-7's viaIR draft: `86/86`, same scores.
   If a different peer draft is chosen, substitute its token/file; the projected arithmetic is the same (+1 per landed entry).
4. Nothing else: no SKILL.md, no PROVINCE.md, no gate, no corpus edit from this seat. A second Vyper entry would be duplication (§5).

## 7. Custody & scope statement

- Scratch root `/var/tmp/ex05-r6/` (never `/tmp`; EDQUOT rule). Scratch `TMPDIR=/var/tmp/ex05-r6/tmp`.
- Custody paths read-only: r4 vyper venv (executed with `PYTHONDONTWRITEBYTECODE=1`; `find … -newermt '2026-10-19 13:30'` on the venv, the CR-1 custody tree and the r1 solc prefix returns **no files**), r4 `K8.vy`/`CarrierV.vy`, r1 solc prefix (read-only; recompiled EX-7 into scratch), EX-7's tree (read-only). No tracked file was modified; `git status --short` shows only the pre-existing `M .ufo/waves/arc2-loop1-round10/C3.md` and the untracked wave tree.
- Write scope used: `.ufo/waves/arc3-loop1-round6/claims/c2/EX-5/` (93 files incl. manifest; `evidence/manifest.sha256` carries 93 hashes — 92 evidence files + this artifact, and `sha256sum -c` passes). No PROVINCE/SKILL/SCORECARD/LOG/corpus/`.ufo/gates/` edits; Git read-only.
- All evidence under `EX-5/`: `src/` (K8, Ex05Vault, CarrierV, K2), `scripts/` (keccak, disasm, walk-forms, verify-ex7, make-evidence), `out/` (pinned runtime/creation bytes), `probe/` (18 envelopes + 2 rechecks), `evidence/` (walk JSON, probe matrix, receipts, manifests, EX-7 verification, two-level and mutability tables).

## 8. Honest limits

- One Vyper version (0.4.3), two primary carriers (K=8 and K=7) + two scope probes (K=15, K=2); runtime classes 103–1,450 B; the packed-table K threshold and the multiplier-selection rule are **not derived** — only observed at K=7/8/15.
- Hardfork controls byte-characterized for the **default** form only (five versions, two byte-identical groups); hardforks under B/C not compiled here (CR-1's r4 custody bytes exist but were not re-derived).
- Mutability/argument strings are upstream inferences; only selector identity is claimed exact. The `ev_` id domain is path-sensitive; cross-seat comparison must use decoded sha + function payload.
- The 85/86 projections are overlays, not post-landing command-A measurements. EX-7 verification covers the pinned solc/carrier and the hex/std/trap paths I re-ran; their raw-bin leg envelope was not re-run (my re-probe covers hex, std, creation and raw-on-hex).
- Four peers closed the same Unknown; §5's recommendation is that one entry land, but that choice is the parent's.
