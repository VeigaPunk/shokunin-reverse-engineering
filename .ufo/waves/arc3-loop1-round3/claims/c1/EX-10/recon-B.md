# EX-10 — carrier-B reconciliation (chain c1, arc3-loop1-round3)

Seat: EX-10 (executor). Date: 2026-10-19. Repo HEAD at work:
`c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` (`git rev-parse HEAD`, re-checked at close).
Scratch `/var/tmp/ex10-r3` (+ `/dev/shm` unused); no `/tmp` writes; custody paths
untouched; no git mutations; scratch copies only.

**Primary target** — the wave's carrier B, authored by seat EX-04:
`claims/c1/EX-04/carrierB.sol` (2-of-3 multisig vault, non-ERC-20 shape, K=11),
whose seat report directs "the probe seats" to
`evidence/carrierB.runtime-opt200.hex` + `planted-B.txt`.

**Secondary target** — this seat's own independently authored non-ERC-20 carrier
(`VaultB.sol`, K=13: payable `receive()`/`fallback()`, mixed mutability,
inlined library call, custom errors). It is extra replication evidence and is
never presented as the wave's carrier B.

## Verdict

- **Primary (EX-04 carrier B): K/K = 11/11 on both optimizer legs**, zero missing,
  zero extra. **Thirteen carrier-leg probe envelopes agree exactly** (EX-04's 4
  non-trap envelopes + this seat's 9: 8 legs = hex + raw-bin × 6.4.0/6.7.0 ×
  opt200/noopt, plus 1 rerun), alongside four independent derivations: planted
  set (3-way derivation by EX-04, re-derived here from signatures with my own
  keccak), solc ABI, my dispatch parse, my keccak scan. (This seat's remaining
  two runs — 1 creation leg, 1 raw-on-hex trap leg — are the §4 controls, not
  agreement sources.) Every probe `bytecode_offset` equals my independently parsed
  EQ-dispatch JUMPI target; every probe `bytecode.sha256` equals the runtime
  file's sha256; probes report 11 functions, all `dispatch:"abi"`.
- **Secondary (EX-10 carrier, K=13): K/K = 13/13 on both optimizer variants**
  (8 probe legs, same construction; zero extras, offsets equal).
- **Also reconciled — EX-05's `CarrierB`, K=8: K/K = 8/8** on 7 probe legs
  (4 run by this seat, 3 by EX-05), zero missing/extra, offsets and digests
  equal (§3b). The name "carrier B" resolves to three different artifacts in
  this wave tree (see §6); all three are reconciled here.
- Offset semantics re-confirmed on every target: every probe offset is a byte
  `5b` (JUMPDEST) and is the EQ comparison leg's JUMPI target
  (`dispatch_eq_targets_all_jumpdest: true` in both recon JSONs).
- The carrier is **parsed** by the tool on real solc 0.8.37 output whose
  dispatcher is **GT/EQ binary-search shaped** — a shape class not present in
  the r1 carrier cohort (see §5).

## 1. Targets and pinned identities (all sha256 re-derived first-hand)

| role | path | sha256 / value |
|---|---|---|
| carrier B source (EX-04) | `claims/c1/EX-04/carrierB.sol` | `14566042e4528cdcb35df2602385f51c1fa89f38c5f88fb0288cdf7260719648` |
| carrier B runtime opt200 | `claims/c1/EX-04/evidence/carrierB.runtime-opt200.bin` | `aaf85ceaf124bac2d3a32428927194158c9211e4472a0cf06f88a721cf239412` (1,850 B) |
| carrier B runtime noopt | `claims/c1/EX-04/evidence/carrierB.runtime-noopt.bin` | `679678e9a67aee701094a4bfeafd2a02311460658aa4b400202340b47d83d005` (3,872 B) |
| planted set (EX-04) | `claims/c1/EX-04/planted-B.txt` | `f32393c0269cf8fa297a219ffe4b60aa71998038c1e73a383da3b0b3af8c59aa` (11 sigs; my keccak AGREEMENT 11/11 — §2) |
| EX-04 claim manifest | `claims/c1/EX-04/manifest.sha256.txt` | `1528195a5f3b15f90377a73e3adbbad1d193757c12fc06216029a77a5f3bc7d7`; `sha256sum -c` → **44/44 OK** |
| my carrier source | `claims/c1/EX-10/VaultB.sol` | `6b3d04cb7ff60c7c31f361b15efd65a420481173732c66dc51eab40a402dafd0` |
| my runtime opt200 | `claims/c1/EX-10/out/VaultB.opt200.runtime.bin` | `b24a01153af943ff8ebf26a678a3bfc0b1d70e1fc563d17b05c7cc064ae340b6` (1,621 B) |
| my runtime nopt | `claims/c1/EX-10/out/VaultB.nopt.runtime.bin` | `bcdf64abcda096e3cb7ea25d552d597a1c0f93303a66340cd270e23aaa7f77fa` (3,163 B) |
| my planted set (K=13) | `claims/c1/EX-10/planted-K.json` | `dd2d63af19cf324737695610895c686f7a290b98ae71647b367f1c35eb85b629`; signatures derived pre-compile (§8 ordering) |
| compiler | `.ufo/waves/arc3-loop1-round1/tools/solc-prefix/` | receipt re-verified: `solcjs --version` → `0.8.37+commit.f401782d.Emscripten.clang`; 99-file tree manifest `f361af99fd2554f9e087cad87b7e5977e28cd65724bd7ed53fd7337be5ae032a` (`/var/tmp/ex10-r3/solc-prefix-manifest.sha256`) |
| probe pins | `rea-agents@6.4.0`, `rea-agents@6.7.0` | npm-cache-resident from r1 (index keys `…/rea-agents-6.4.0.tgz`, `-6.7.0.tgz`); run via `npx -y` with `TMPDIR=/var/tmp/ex10-r3/tmpdir` (disk-backed, r1 requirement) |

Compile inputs: standard-JSON, optimizer `{enabled:false}` and
`{enabled:true, runs:200}`; driver `claims/c1/EX-10/compile.js` (my carrier) and
EX-04's `evidence/compile-b.js` (their carrier, re-run verification).

## 2. Independent methods

- **M1 — own linear-sweep disassembler + dispatch parser** (`recon.py`; PUSH1..32
  consume immediates). Recognises both dispatch shapes: the 11-byte linear chain
  (`DUP1 PUSH4 EQ PUSH2 JUMPI`) and the **GT/EQ binary-search** shape
  (`DUP1 PUSH4 <sel> {EQ|GT|LT} PUSH2 <t> JUMPI`, navigation targets vs function
  entries). EQ sites → function entry set; GT/LT sites → navigation labels.
- **M2 — own pure-Python keccak-256** (`keccak.py`; Keccak-f[1600], rate 136,
  domain byte 0x01). Self-test `VECTORS PASS` (empty string, `abc`, ERC-20
  `transfer(address,uint256)`; `totalSupply()` selector `18160ddd`).
  Cross-validation: full-hash **AGREEMENT 13/13** with `js-sha3@0.8.0` (from the
  solc prefix dep tree) on my carrier's signatures, and **AGREEMENT 11/11** with
  EX-04's `planted-B.txt` signatures via both my keccak and js-sha3.
- Reconciliation driver: `recon.py <bin> <planted.json> <abi.json> <probes…>` →
  JSON reports `recon-EX04carrierB-{opt200,noopt}*.json`, `recon-B-{nopt,opt200}.json`.

## 3. Source-set agreement

Primary target, per leg (my parse vs the probe envelopes):

| leg | probe envelope | ev_id | K | missing/extra | offsets = my EQ dests | decoded digest |
|---|---|---|---|---|---|---|
| opt200 hex 6.4.0 | EX-04 `probe-opt200-hex-6.4.0.json` | `ev_e0ee9bea73ab935…` | 11 | 0/0 | yes | = file sha256 |
| opt200 raw-bin 6.4.0 | EX-04 `probe-opt200-rawbin-6.4.0.json` | `ev_c7db1e1cab07bf3…` | 11 | 0/0 | yes | = file sha256 |
| noopt hex 6.4.0 | EX-04 `probe-noopt-hex-6.4.0.json` | `ev_ca4595f0db3f89d…` | 11 | 0/0 | yes | = file sha256 |
| noopt raw-bin 6.4.0 | EX-04 `probe-noopt-rawbin-6.4.0.json` | `ev_13895b038bd7dd2…` | 11 | 0/0 | yes | = file sha256 |
| opt200 hex 6.4.0 (rerun) | mine `probe-EX04carrierB-opt200-hex-6.4.0-rerun.json` | `ev_fc573e7dc9135…` (id equal to first run; payload equal) | 11 | 0/0 | yes | = file sha256 |
| opt200 hex 6.4.0 | mine | `ev_fc573e7dc9135f59eb63f701b0ba1dd33041be3d5019ba4ef43f71d9569257ef` | 11 | 0/0 | yes | = file sha256 |
| opt200 hex 6.7.0 | mine | `ev_a94c0e8763fd22b4…` | 11 | 0/0 | yes | = file sha256 |
| opt200 raw-bin 6.4.0 | mine | `ev_bc7f5a61c0578240…` | 11 | 0/0 | yes | = file sha256 |
| opt200 raw-bin 6.7.0 | mine | `ev_7316320ad266cad0…` | 11 | 0/0 | yes | = file sha256 |
| noopt hex 6.7.0 | mine | `ev_0ccb3214a2512815…` | 11 | 0/0 | yes | = file sha256 |
| noopt raw-bin 6.4.0 | mine | `ev_2e6bbda4414a266d…` | 11 | 0/0 | yes | = file sha256 |
| noopt raw-bin 6.7.0 | mine | `ev_12a7e8d410598cf9…` | 11 | 0/0 | yes | = file sha256 |

My independently parsed EQ dispatch targets (primary target):

- opt200: `07bf89ab`→221, `0bf6cc08`→271, `0db02622`→289, `2f54bf6e`→308,
  `42cde4e8`→355, `59bf77df`→375, `797af627`→418, `960bfe04`→451, `a8c162fb`→482,
  `d0e30db0`→513, `d9caa3d2`→521; navigation GT label: `59bf77df`→98.
- noopt: `07bf89ab`→248, `0bf6cc08`→308, `0db02622`→350, `2f54bf6e`→392,
  `42cde4e8`→452, `59bf77df`→494, `797af627`→554, `960bfe04`→594, `a8c162fb`→634,
  `d0e30db0`→674, `d9caa3d2`→684; navigation GT label: `59bf77df`→99.
- Dispatcher prologue `5f3560e01c` at pc 13 on both legs; 12 compare legs
  (11 EQ + 1 GT) = EX-04's `total_legs: 12`, `compare_ops_used: ["EQ","GT"]`,
  `all_probe_offsets_are_leg_targets: true`, `all_probe_offsets_jumpdest: true`
  (`evidence/probe/offset-check-{opt200,noopt}.json`, read and re-derived here).
- Non-dispatch PUSH4 constants: opt200 → `4e487b71` only (= keccak
  `Panic(uint256)` written by the revert helper, not a dispatch leg); noopt → none.
  Neither was reported by any probe leg (zero false positives).

Secondary target (my K=13 carrier), same construction: 13/13 on 8 legs
(`recon-B-{nopt,opt200}.json`), EQ targets all JUMPDEST, GT navigation labels
2 (`69fe0e2d`→126, `8da5cb5b`→88 on nopt), non-dispatch PUSH4 on opt200:
`1309a563`=`IsPaused()`, `1dc930eb`=`Insufficient()`, `30cd7471`=`NotOwner()`,
`3c3332b9` (unattributed; context written as SHL+MSTORE revert-data assembly),
`4e487b71`=`Panic(uint256)` — none reported by any leg.

### 3b. EX-05's `CarrierB` (the other artifact named "carrier B")

Runtime `claims/c1/EX-05/out/CarrierB.runtime.bin`, 1,469 B
`b9c70178069601ba766a49359981118032085b8af74861659a9edc064ebd7940`
(= the decoded digest on every leg); ABI `…/CarrierB.abi.json`
`8a11dd932c6d56ae0af92529e4d931273d8020d96088ed9f458baa29918a8f63`;
planted set K=8 (`planted-K.json`; my keccak re-derivation from its signatures
AGREEMENT 8/8). My parse: prologue `5f3560e01c` at pc 13, **8 EQ entries**
(all targets JUMPDEST) + 1 GT navigation label (`8da5cb5b`→77); no non-dispatch
PUSH4 constants.

| leg | ev_id | K | missing/extra | offsets/digest |
|---|---|---|---|---|
| EX-10 hex 6.4.0 / 6.7.0 | `probe-EX05carrierB-hex-*.json` | 8 | 0/0 | equal |
| EX-10 raw-bin 6.4.0 / 6.7.0 | `probe-EX05carrierB-rawbin-*.json` | 8 | 0/0 | equal |
| EX-05 hex 6.4.0 / 6.7.0, raw 6.4.0 | `EX-05/probe/probe-runtime-*.json` | 8 | 0/0 | equal |

Report: `recon-EX05carrierB.json` (7 legs, `offmism: {}` on each).

## 4. Attacks / refutation attempts

| # | attack | expectation | result |
|---|---|---|---|
| A1 | **constants-only decoy** (`attack/decoy1-constants-no-dispatch.bin`: selector-looking PUSH4 constants, no dispatch chain) | K=0, no false positives | K=0 on both pins (`ev_17591e0fdc41…`, `ev_6fc0dbb2ae6b…`) |
| A2 | **extra-dispatched-selector decoy** (`attack/decoy2-extra-selector-dispatch.bin`; hand-assembled EQ chain for `deadbeef`, JUMPDEST at 0x1a) | tool follows dispatch, reports 1 at 26 | K=1, `0xdeadbeef` @26 on both pins (`ev_f4b7d847bfdd…`, `ev_8a0579d98b57…`) — positive control: "zero extras" on the real carriers is meaningful, not blind |
| A3 | **raw-on-hex trap** (raw encoding over the hex text file) | parsed-and-empty, not an error | K=0, exit 0, decoded bytes ≠ runtime (mine `ev_d4b06355dc2519…`; EX-04's two trap legs `ev_704ce585…`, `ev_dc045815…` reproduce) |
| A4 | **creation-code legs** | parsed-and-empty (r1 class) | opt200 creation K=0 (`ev_af363ec9a823cc…`), bytecode digest ≠ runtime digest; `kind:"unknown"` |
| A5 | **evidence-id identity** | same request re-derives same id on this carrier | rerun `ev_fc573e7dc9135…` = first run; `normalized_result` payload byte-equal |
| A6 | **planted-set laundering** (my keccak could rubber-stamp EX-04's file) | require independent re-derivation from signatures | my keccak re-derived all 11 from the signature text of `planted-B.txt` → AGREEMENT 11/11 (js-sha3 cross-check also 11/11) |

## 5. Round deltas measured (feed the C1 claim's "optimizer-enabled dispatch shapes" leg)

- **Shape class:** both carrier-B optimizer legs use the GT/EQ binary-search
  dispatcher. The prologue class is unchanged (`5f3560e01c`), so the r1 named
  unknown "dispatcher prologues other than `5f3560e01c`/`60003560e01c`" stays
  open; what changes this round is the **leg layout after the prologue**.
- **Shape census** (`shape-census/census.py`, synthetic 1-line functions,
  std-JSON, pinned solc; results `shape-census/census-results.{txt,json}`):
  linear chain for k ∈ {4,5,6}; GT/EQ binary search for k ∈ {7,8,9,10,11,13} —
  **in both optimizer modes** (the switch threshold is selector count, not the
  optimizer; optimizer changes sizes only: e.g. k=11 691 B → 290 B). r1's K=5/6
  carriers were linear, consistent; EX-04's K=11 carrier and my K=13 carrier are
  binary-search, consistent. The "optimizer-enabled" delta for this round is
  therefore **not** a shape change; the honest reading: the shape boundary is
  k=7 independent of `--optimize --optimize-runs 200`.
- **Inference-class observations (EX-04 carrier, 4 legs × 11 fns):** probe
  `inferred_state_mutability` matches the solc ABI 40/44; the 4 divergences are
  `pure` → `view` on `computeTxHash` (declared `pure`) — an upstream-inference
  granularity, consistent with the tool's `evidence_kind:"inferred"` label.
  `inferred_arguments` matches the ABI 44/44 once `bytes32` is width-normalized
  to `uint256` (the probe renders the bytes32 argument as `uint256`).

## 6. Gaps / blockers

- **Carrier A was not reconciled here** (out of seat scope; sibling seats' target).
  Naming resolved while in flight, recorded for the parent: the wave's **carrier A**
  is EX-03's `CarrierA` (optimizer-enabled, K=9; EX-07's `legC-*` legs, EX-11's
  id-rerun legs); the seat-line "author carrier B" task belongs to **EX-04**
  (`VaultB`, K=11) — but **EX-05's `CarrierB`** (K=8) and this seat's own
  `VaultB.sol` also carry the name, so all three are reconciled above;
  EX-07 independently flagged the same ambiguity (`seats/EX-07.md` §5).
- EX-05's `CarrierB` was reconciled from its bytes while its seat report was
  still in flight; `seats/EX-05.md` landed afterwards with matching pins
  (runtime 1,469 B `b9c70178…` — equal to the bytes reconciled here), so the two
  are consistent. `seats/EX-08.md` (the assigned carrier-B probe seat) reports
  the same 11/11 on the 6.7.0 pin for EX-04's carrier, independent of this
  seat's legs.
- EX-04 ran its probe legs at pin 6.4.0 only (plus a 6.7.0-absent note); this seat
  supplies 6.7.0 legs for the same carrier bytes (4 of the legs above).
- Not examined, by scope: mainnet/deployment identity (never claimed by the tool),
  Vyper, carriers above this size class, `--encoding` flag-form rejection.

## 7. Reproduction (verbatim forms)

```bash
# probe a carrier leg (disk-backed TMPDIR is required on this host)
TMPDIR=/var/tmp/ex10-r3/tmpdir npx -y rea-agents@6.4.0 inspect-evm-interface \
  .ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/carrierB.runtime-opt200.hex hex --format json

# my reconciliation over a carrier + probed legs
python3 .ufo/waves/arc3-loop1-round3/claims/c1/EX-10/recon.py \
  <runtime.bin> <planted.json> <abi.json> <probe.json...>

# keccak self-test
python3 .ufo/waves/arc3-loop1-round3/claims/c1/EX-10/keccak.py vectors
```

## 8. Identity discipline (rule #14)

All identities above were re-derived at write time (`sha256sum` over the actual
files; EX-04's manifest re-verified 44/44 from its claim dir). Ordering evidence
for the planted sets: my `planted-K.json` signatures were derived at
10:07:04 -03 (`evidence/planted-raw-precompile.txt`, mtime 10:07:04) before the
first compile (10:07:14) and the first probe (10:08:10); EX-04 records its own
9.3 s planted→probe ordering. No file claimed its own byte-identity inside itself
(the seat report carries this file's post-revision sha256, re-derived after the
last write). Manifest: `claims/c1/EX-10/manifest.sha256.txt` (generated last).