# RV-1 — seat report (chain c1, reviewer)

Wave `arc3-loop1-round4` · chain c1 · seat RV-1 · 2026-10-19 · repo
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · HEAD at work
`015e1bab914713568f339fd53999bc180459cc40` (no seat commits; parent integrates).
Scratch `/var/tmp/rv1-r4` (never `/tmp`); no git mutations; custody paths
untouched (`.ufo/gates/custody-pair/` read-only, not even hashed here — the
C1 leg has no custody dependency); no LOG/SCORECARD/SHONEN/corpus/SKILL/
PROVINCE/README writes — this seat's only writes are its own seat report and
`claims/c1/RV-1/`.

**Task (seat line).** Independently recompute the planted selector set from the
Vyper source/ABI by a *different keccak path*; re-run one probe leg myself;
compare. Seat report.

**Completion statement: COMPLETED.** All three parts executed first-hand. One
factual error found in the round's draft entry (see §4); everything else
verified and agreeing.

---

## 1. Work performed (evidence pointers)

### 1.1 A fifth keccak path (path G), sharing no code or tables with the planters

`claims/c1/RV-1/keccak_g.rs` (sha256 `82ad37f6…`) — Keccak-256 written for this
seat in Rust, compiled with `rustc 1.98.1`. Round constants are **derived from
the LFSR** `rc(t)` and rho offsets are **derived from the walk** recurrence;
neither table is hardcoded in the file. It carries **two independent
formulations** in one binary — `g1` a `u64[25]` lane array, `g2` a `[u8;1600]`
bit array indexed `25z+5y+x` — and every digest is computed both ways and
compared before printing (a mismatch exits 2).

Lineage, from the artifacts on record: EX-04 planted with a hand-rolled
**Python** keccak (`EX-04/evidence/keccak256.py`); EX-05 cross-checked with
`js-sha3@0.8.0`, `node:crypto`, OpenSSL and a Python ref; VZ-1 re-derived with
`js-sha3@0.8.0`; r1/r3 used js-sha3 and a pure-Python lane array. Path G shares
no source, no language and no table with any of them.

**Self-test 7/7 PASS** (`keccak-g-selftest.txt`): the empty string
`c5d24601…`, `abc` `4e03657a…`, the quick-brown-fox digest `4d741b6f…`, plus
rate-boundary probes at 135/136/137 bytes where g1 and g2 must agree.

The derived tables were checked against the published Keccak-f[1600]
constants and match, RC[0]=`0000000000000001` … RC[23]=`8000000080008008`,
rho `[[0,1,62,28,27],[36,44,6,55,20],[3,10,43,25,39],[41,45,15,21,8],
[18,2,61,56,14]]`.

**Honest note on a self-caught defect.** My first build was wrong: I recorded
each rho offset *after* advancing the walk instead of before, producing a
transposed table. It was caught immediately because `abc` and the ERC-20
selectors failed to match the published vectors, and fixed before any
comparison against the wave's artifacts was made. No result in this report
comes from the defective build.

### 1.2 Source/ABI-driven recomputation of the planted sets

`carrierv-g-sigs.txt` (sha256 `51a6e865…`) — the 15 signatures taken from
`EX-04/out/abi.json` function entries, hashed through path G.
`smoke-g-sigs.txt` (sha256 `0936a2b2…`) — the 4 `Smoke.vy` signatures.

**CarrierV: 15/15.** Every one of the 15 path-G selectors equals the
corresponding entry in `EX-04/evidence/planted-K.json` (which stores the
8-hex-char selectors in `planted_selectors`). The **full 32-byte digests** were
cross-checked separately against `EX-05/planted-full.json`, which carries two
independent derivations per signature (`keccak256_js_sha3` and
`keccak256_node_crypto`): **30/30 agree with path G, zero mismatches.** So the
identity is established at digest level, not just by an 8-hex-char prefix
comparison.

**Smoke: 4/4**, and they equal Vyper's own `method_identifiers` output exactly
(`d09de08a`, `6d4ce63c`, `8da5cb5b`, `61bc221a`) — an independent agreement
with the compiler's own ABI-derived set.

The ABI-derived signature list and the source-derived list agree; no
`public` state-variable getter was missed and no internal function was
included.

### 1.3 Probe leg re-run by this seat (two pins, two carriers)

Run with a disk-backed `TMPDIR` (standing requirement since r1):

```
TMPDIR=/var/tmp/rv1-r4/probe npx -y rea-agents@6.4.0 \
  inspect-evm-interface .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.hex hex --format json
```

- `probe-carrierv-runtime-hex-6.4.0.json` (sha256 `68415a3d…`) — exit 0,
  stderr 0 B, `ev_d1792f57…`, **15 functions**, `dispatch:"abi"` ×15, decoded
  `bytecode.sha256 57d6fd0a…` (1,562 B). Set-equal to the planted K=15,
  missing `[]`, extra `[]`.
- `probe-carrierv-runtime-hex-6.7.0.json` (sha256 `0d7171ed…`) — exit 0,
  `ev_62e1b9e6…`, same 15, same decoded sha.
- `probe-smoke-runtime-hex-6.4.0.json` (sha256 `5b2dab53…`) — exit 0,
  `ev_073f845c…`, **4 functions**, `dispatch:"abi"` ×4, decoded
  `415e6b1b…` (168 B), set-equal to the ABI-derived K=4.

The decoded digest this seat computed over the carrier bytes equals the
envelope's decoded digest in all three legs, so the bytes the tool read are the
bytes this seat hashed.

### 1.4 Structural verification of the dispatch shape (independent)

`offset-probe.txt` — a linear disassembler written for this seat (skips every
PUSH payload, so no immediate is mistaken for an opcode).

- **Jump table.** Prologue `5f3560e01c | 6002 600d 8206 | 6001 1b | 610600 01 |
  601e 39 | 5f 51 56`: `PUSH1 2 PUSH1 13 DUP3 MOD PUSH1 1 SHL PUSH2 0x600 ADD
  PUSH1 0x1e CODECOPY PUSH0 MLOAD JUMP`. `N=13` read at pc=7, table offset
  `0x600` read at pc=14. The 13 uint16 entries are
  `[668,1511,1291,1024,1452,1087,1341,1511,1424,1396,898,1511,24]`; **all 13
  land on `0x5b`**, the sentinel `0x5e7` appears **exactly 3×** (buckets
  1/7/11), and `0x600 + 13*2 = 1562` equals the runtime length exactly — the
  table is the runtime's tail, with no slack.
- **Bucket rule.** `selector % 13` reproduces the observed occupancy: bucket 12
  holds 3 selectors (`1aa02d59`, `3f4ba83a`, `d0e30db0`), buckets 5/6/10 hold
  2 each, buckets 0/2/3/4/8/9 hold 1, buckets 1/7/11 are the sentinel — 10
  distinct buckets for K=15, with 4 collisions and 3 empties.
- **Compare form.** `63 <sel:4> 81 18 61 <next:2> 57` = `PUSH4 sel; DUP2; XOR;
  PUSH2 next; JUMPI` — Vyper compares with **XOR**, not solc's `EQ`/`GT`.

### 1.5 Offset semantics — independently re-derived, and the reading is the *opposite* of the solc family

On CarrierV **0 of 15** reported `bytecode_offset` values land on a JUMPDEST.
Each is exactly `compare_pc + 11`, i.e. the **fall-through handler-body entry
immediately after the compare `JUMPI`** — a byte the dispatcher never jumps to.
Verified for all 15 selectors, and for all 4 Smoke selectors (4/4). The
preceding byte at every reported offset is `0x57` (`JUMPI`).

This is the same finding EX-09 and RV-2 recorded independently; this seat
re-derived it from the bytes rather than reading it, and it is the round's
load-bearing scoping statement — the r1/r3 sentence "every reported offset
lands on `0x5b`" is true for the solc carriers and **false for the Vyper
family**.

### 1.6 Mutability-inference delta — reproduced, 7/15

`offset-probe.txt` §TEST B. Comparing the probe's `inferred_state_mutability`
against the compiled ABI for all 15 CarrierV functions: **7 agree, 8 diverge**,
and every divergence reads `payable` where the ABI declares `view` (5),
`nonpayable` (2) or `pure` (1). No selector is misassigned and no reading is
*more* restrictive than the ABI. On Smoke the agreement is 4/4 — the divergence
appears on the larger, collision-bearing carrier, not on the minimal smoke leg.
The byte-level mechanism is visible: the mutating-looking blocks are the ones
that carry an argument-count `CALLVALUE OR` guard in their prologue
(`60243610 3417` = `PUSH1 0x24 CALLDATASIZE LT CALLVALUE OR`), which the
inference appears to read as a value-transfer guard.

Recorded as an observed delta, not a defect and not a claim about the
contracts.

### 1.7 Negative controls on this seat's own pipeline

`negative-controls.txt`. On in-memory scratch copies of the planted table:
CONTROL intact → set-equal True; one hex digit flipped → **detected**; one
entry deleted → **detected** (missing `0776076f`); a bogus entry added →
**detected** (extra `deadbeef`). The pipeline is falsifiable, not merely
agreeing.

The leading-zero trap is demonstrated in the same file: `planted-K.json`
stores all 15 selectors as exactly 8 hex chars, while
`EX-04/out/method-identifiers.json` prints 2 of them leading-zero-**stripped**
(`0xc751377` for `fee_of`, `0x776076f` for `is_owner`). A naive string diff of
those two artifacts reports two false mismatches; a value-wise comparison
reports agreement. **This is a live trap in the round's own artifacts** — the
values are correct, the printed forms are not directly comparable, and EX-03's
`dispatch-decode.txt` shows the same stripping on a third carrier
(`0x6fdde03`, `0x95ea7b3`).

### 1.8 Identity re-derivation (rule #14)

`identities.txt`, computed by this seat at write time (2026-10-19T14:11:34Z)
with `sha256sum`/`hashlib`, nothing copied from a receipt:

| artifact | sha256 |
|---|---|
| `EX-04/out/runtime.hex` | `e0b1021c…` |
| `EX-04/out/runtime.bin` | `57d6fd0a…` |
| `EX-04/src/CarrierV.vy` | `f4f94727…` |
| `EX-04/out/abi.json` | `c7902147…` |
| `EX-04/evidence/planted-K.json` | `5161b950…` |
| `EX-04/out/method-identifiers.json` | `0d5cab2f…` |
| `EX-02/smoke/Smoke.runtime.hex` | `40650adf…` |
| `EX-02/smoke/Smoke.abi.json` | `cd535040…` |
| `RV-1/keccak_g.rs` | `82ad37f6…` |

Decoded-bytecode digests recomputed by this seat over the decoded bytes:
CarrierV `57d6fd0a…` (1,562 B), Smoke `415e6b1b…` (168 B). The CarrierV
`runtime.hex` → `runtime.bin` byte identity holds.

---

## 2. Proposed changes

**One patch text:** `claims/c1/RV-1/proposed-entry-correction.patch.md` —
corrects the `69656e74` census sentence in the draft entry (see §4). The
parent applies or rejects it; this seat wrote nothing outside its own
directory.

**No other changes proposed.** The map-token patch, the stem
`2026-10-19-arc3-r4-evm-vyper-leg`, and the entry's other observations are not
challenged by this seat.

---

## 3. Before → after measurement for the C1 claim

The C1 claim is: *at least one Vyper-compiled contract's selectors are
recovered by `inspect-evm-interface` (K/K against Vyper's own ABI-derived
selector set); the result lands as a corpus knowledge entry + line-neutral map
token; command A re-measures 83 → 84 with the prior 83 byte-identical.*

What this seat measured, as a reviewer:

| quantity | before | after (this seat's re-run) | verdict |
|---|---|---|---|
| CarrierV recovered selectors | 15 (planted K) | **15**, missing `[]`, extra `[]` | K/K holds |
| CarrierV legs run by this seat | — | 2 (6.4.0 + 6.7.0 hex) | both 15/15 |
| Smoke recovered selectors | 4 (ABI) | **4** | K/K holds |
| CarrierV offset-on-JUMPDEST | (r1/r3 reading: yes) | **0/15** | reading does NOT generalize |
| CarrierV mutability agreement | (unmeasured) | **7/15** | delta recorded |
| path-G vs Vyper's own set (Smoke) | — | 4/4 identical | independent agreement |
| knowledge files at HEAD | 83 | **83** (entry not landed; patch text only) | pending parent |

Command A at HEAD (`015e1bab`), from RV-2's pinned run: `knowledge_files 83,
mapped 83, missing [], dangling [], rules 14/14`. The 83 → 84 step is the
parent's landing action; this seat did not write `corpus/`, so it cannot and
does not claim the after-state. **The entry's selector-count claims are
independently verified; the corpus-count claim remains open at landing.**

---

## 4. Attacks / refutations attempted, with verdicts

1. **Attack: is the planted table itself fitted to the probe output?**
   — *Refuted (table is honest).* `planted-K.json` records
   `recorded_utc 2026-10-19T14:05:46.622429Z`; the probe envelopes this seat
   ran are timestamped later, and this seat recomputed the same 15 values from
   the ABI through an unrelated implementation. A fitted table could not
   survive a fifth independent path.

2. **Attack: is the "non-selector `PUSH4` immediate `69656e74`" claim true?**
   — **REFUTED.** `69656e74` occurs once, at byte offset 732, **inside a
   `PUSH32` payload** at pc=723 (the ASCII string `insufficient` plus zero
   padding). It is not an opcode-boundary immediate. The correct
   opcode-boundary `PUSH4` census of the same runtime is **16 distinct
   immediates: the 15 selectors plus `08c379a0` only.** The claim's
   *conclusion* (zero false positives) is **unchanged and still true** — the
   probe reported exactly the 15 planted selectors — but the stated mechanism
   is wrong and unreproducible by the method it names. Full evidence:
   `push4-census-corrected.txt`; proposed repair:
   `proposed-entry-correction.patch.md`. **This is the round's one finding that
   requires an edit before landing.** It appears in **four** places
   (`EX-05/runtime-presence.txt:5`, `EX-05/verify-planted.py:151`,
   `RV-2/evidence/push4-census.txt:14`, `seats/EX-05.md:70` — and the draft
   entry's literal text repeats the same wording), so a repair should
   touch all of them or the corpus will contradict a sibling artifact.

3. **Attack: does the `% 13` bucket reading survive an independent parse?**
   — *Not refuted.* `N` read at pc=7, table offset read at pc=14, 13 entries
   all JUMPDESTs, sentinel exactly 3×, `table_off + N*2 == len(runtime)`
   exactly, and `selector % 13` reproduces the occupancy including the 3-way
   collision in bucket 12. Four independent quantities agree.

4. **Attack: is the offset rule "offsets are JUMPDESTs" still safe to assert
   generally?** — **Refuted for Vyper.** 0/15 and 0/4 offsets are JUMPDESTs;
   each is `compare_pc + 11`. The r1/r3 wording must carry a solc-convention
   scope or it is false for this family. (The draft already states this
   correctly; this seat's attack confirms rather than corrects it.)

5. **Attack: is `method_identifiers` a safe oracle to compare against?**
   — *Partially refuted.* It over-counts by one per carrier (the
   `__default__()` phantom, whose bytes this seat confirmed are **absent** from
   the runtime — `89402a72` occurs 0 times) and it prints two selectors
   leading-zero-stripped, which a string comparison will read as mismatches.
   It is usable only with value-wise comparison and ABI-function filtering.
   The draft's own note about the phantom is correct; the stripping trap is
   recorded here as a reviewer's caution.

6. **Attack: is the mutability divergence a selector-recovery failure in
   disguise?** — *Refuted.* All 15 selectors are recovered with zero
   extras; the divergence is confined to the mutability string. The two are
   independent fields.

---

## 5. Blockers

**None.** The task was fully executable: no install was needed for this seat
(path G is self-contained Rust; the probes use the already-cached
`rea-agents` tarballs), no other seat's output was required, and no custody
path was touched.

Two caveats the parent should carry:

- **The entry is not yet landed**, so the C1 claim's corpus-side half
  (83 → 84, prior-83 byte-identical) is outside this seat's measurement — it
  is a landing-time check.
- **The `69656e74` error is live in three artifacts** (§4.2). If the entry
  lands uncorrected, the corpus will assert a `PUSH4` census that cannot be
  reproduced, and `EX-05/runtime-presence.txt` will agree with the corpus while
  both are wrong. RV-1 recommends the parent apply
  `proposed-entry-correction.patch.md` (or an equivalent edit) before landing.

---

## 6. Self-identity (rule #14)

Re-derived at write time; see `identities.txt` for the full list.

- `keccak_g.rs` `82ad37f6…`; `carrierv-g-sigs.txt` `51a6e865…`;
  `smoke-g-sigs.txt` `0936a2b2…`
- `probe-carrierv-runtime-hex-6.4.0.json` `68415a3d…`;
  `probe-carrierv-runtime-hex-6.7.0.json` `0d7171ed…`;
  `probe-smoke-runtime-hex-6.4.0.json` `5b2dab53…`
- `push4-census-corrected.txt`, `offset-probe.txt`, `negative-controls.txt`,
  `keccak-g-selftest.txt`, `proposed-entry-correction.patch.md` — hashed in
  `identities.txt` at final revision.
