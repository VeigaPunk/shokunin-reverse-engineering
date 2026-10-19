# recon-A.md — carrier A 3-way reconciliation (planted vs probe vs independent keccak+PUSH4 scan)

Seat EX-09 · chain c1 · role executor (late join, provider substitution) ·
wave `arc3-loop1-round3` · 2026-10-19 · repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` ·
HEAD at work `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` (no git mutations).

**Status: reconciliation COMPLETED by the pre-interruption run of this seat (the
artifacts landed; `recon-A.md` itself had not been written), and then independently
VERIFIED by the late-join seat.** Both halves are stated separately below.

## 0. What "carrier A" means here — three readings, all reconciled

Three artifacts carry the name "carrier A" in this wave (EX-03 §1 and EX-06 §Naming
both record the ambiguity). All three are reconciled in this directory:

| id | reading | bytes (decoded) | sha256 (decoded) | K | legs reconciled |
|---|---|---|---|---|---|
| A/1 | r1 CR-1 **hand-assembled** control `carrier-A.hex` | 84 B | `a92ba152…0f6f7b` | 3 | 42 |
| A/2 | EX-02/EX-03 authored `carrierA.sol` (`--optimize --optimize-runs 200`) — the wave's assigned carrier A (EX-07 §Naming) | 1426 B | `9f7392ac…1d23741a` | 9 | 19 |
| A/3 | PL-1 plan §1.A prototype `OptVault` (optimizer runs=200) | 776 B | `544469b7…95dfde7f` | 5 | 8 |

Leg totals 42 + 19 + 8 = 69; each is the complete frozen census for its carrier
(`legs-{control,carrierA-r3,OptVault}.txt`, frozen 2026-10-19T13:16:30Z, census rule in
each header).

## 1. The three methods being reconciled

- **PLANTED** — the pre-probe selector set, copied byte-identically from the authoring
  seat's frozen pin:
  - A/2 `planted-carrierA-r3.copy.txt` `d905412a…301c586` == EX-03
    `carrier-A-EX02/planted-selectors.txt` (sha256 equal, re-derived).
  - A/3 `planted-OptVault.copy.txt` `4fc33b20…b531c8` == EX-03
    `carrier-A-plan-prototype-OptVault/OptVault.planted-selectors.txt`.
  - A/1 `planted-A-control.json` `42b3bd2f…b54c9c` — definitional (the three PUSH4
    immediates inside `DUP1 PUSH4 <sel> EQ PUSH1 <dest> JUMPI` nodes), with the
    `deadbeef@70` / `ffffffff@77` decoys excluded by construction.
- **PROBE** — every frozen `inspect-evm-interface` envelope for that carrier
  (r1, EX-02, EX-06, EX-07, EX-11, RV-2 legs; pins 6.4.0/6.5.0/6.7.0 × hex/raw).
- **INDEPENDENT** — `ex09-recon.py`, two probe-independent methods:
  - **M1** own EVM linear-sweep disassembler → EQ/GT compare sites + a strict
    linear-chain parser (handles both PUSH1-dest 10-byte and PUSH2-dest 11-byte
    strides).
  - **M2** pure-Python keccak-256 (reference implementation, no third-party deps) →
    `keccak(sig)[:4]` searched as raw bytes in the code.

The probe is never invoked by M1/M2, so a probe-side error cannot propagate into the
reference set.

## 2. Result — A/2, the assigned carrier A (9f7392ac, 1426 B, K=9)

`recon-carrierA-r3.txt` (116 lines; exit 0). 21 sources reconcile against the M1 EQ
reference, **all MATCH, zero missing, zero extra**:
`M1_eq_sites` 9, `M2_keccak_scan` 9, `PLANTED` 9, and 18 probe legs (each n=9).

- **Sets:** all 21 sources n=9 MATCH.
- **Offsets:** every probe leg's `bytecodeOffset` equals the M1-parsed EQ-leaf dest;
  offsets `164 214 235 266 297 331 383 437 470` identical across every leg.
- **Landing:** all 9 offsets are byte `5b` (JUMPDEST) in the runtime
  (`jumpdests-carrierA-r3.txt`; also re-derived by the independent verifier).
- **Digest pins:** every leg's `normalized_result.bytecode.sha256` == the decoded
  file sha `9f7392ac…`; encoding form OK per leg.
- **Dispatch shape (recorded, not a defect):** the optimizer-enabled 9-function table
  is a **GT binary search** — pivot `5ce23950` with `GT` half-split at pc 30 (dest 88),
  then EQ leaves. The strict 11-byte linear-chain parser therefore returns an **empty
  chain** on this carrier; the EQ-site scan carries the table. Prologue class is
  `5f3560e01c` @13 (`60003560e01c` absent). Both facts match EX-02 §3, EX-07 §1, EX-08 §3.
- **Non-dispatch PUSH4 constants** (never reported as functions):
  `6508d58f@453`, `30cd7471@634`, `30cd7471@1162`, `4e487b71@1309`, `43000825@1419`
  (the last lies past the metadata boundary at 1373 — a scan artifact, not code).
- **VERDICT: ALL SOURCES AGREE (sets + offsets + pins); every offset lands on a JUMPDEST.**

## 3. Result — A/3, PL-1's OptVault (544469b7, 776 B, K=5)

`recon-OptVault.txt` (67 lines; exit 0). 12 sources, **all MATCH, zero missing/extra**:
`M1_eq_sites` 5, `M1_chain` 5 (this carrier *is* linear), `M2_keccak_scan` 5, `PLANTED`
5, 8 probe legs (n=5 each).

- Offsets `75 106 137 182 248` identical across legs, all JUMPDEST
  (`jumpdests-OptVault.txt`).
- Digest pin per leg == `544469b7…`; form OK.
- Non-dispatch constant: `4e487b71@659` (Panic), unreported.
- The planted copy's own claims re-derive: source `40af90c9…1a764d` (PL-1
  `evidence/OptVault.sol`), runtime `544469b7…`, creation `919fdef4…`.
- **VERDICT: ALL SOURCES AGREE (sets + offsets + pins); every offset lands on a JUMPDEST.**

## 4. Result — A/1, the r1 hand-assembled control (a92ba152, 84 B, K=3) — LANDING ANOMALY

`recon-control.txt` (197 lines; **exit 1**). 49 sources reconcile on **sets and
offsets**: `M1_eq_sites` 3, `M1_chain` 3, `M2_keccak_scan` 3, `PLANTED` 3, and 45
probe legs (n=3 each) — all MATCH, zero missing/extra. Digest pin `a92ba152…` on every
leg; form OK.

**The anomaly.** The driver's own landing check fails on this carrier and the driver
exits 1 with:

> `VERDICT: SETS/OFFSETS/PINS AGREE — LANDING ANOMALY: 129 offset-checks hit non-0x5b bytes`

Re-derived arithmetic (this seat, mechanically): 42 frozen legs × 3 functions = 126
probe-offset checks, plus 3 `MY-PARSE` dests counted once = **129**. Independent
re-derivation over the raw envelopes: 126/126 probe offsets fail the JUMPDEST test,
+3 = 129. ✔

**Cause — the control is broken by construction, not the probe, and not the driver.**
Byte map of `target-carrier-A-control.hex` (84 B):

```
pc  6: 80                DUP1
pc  7: 63 a9 05 9c bb    PUSH4 a9059cbb
pc 12: 14                EQ
pc 13: 60 26             PUSH1 0x26      <- declared dispatch dest = 38
pc 15: 57                JUMPI
pc 36: 60 00             PUSH1 0x00
pc 38: 80                DUP1            <- offset 38 lands HERE (byte 0x80)
pc 39: fd                REVERT
pc 40: 5b                JUMPDEST        <- the real landing
```

Same pattern for `70a08231` (dest `0x30`=48, byte `0x00`; JUMPDEST at 50) and
`095ea7b3` (dest `0x3a`=58, byte `0x00`; JUMPDEST at 60). The declared dests point
**2 bytes early**, into the middle of the `PUSH1 00; DUP1; REVERT` guard. The probe
reports the declared immediates faithfully (as it does on every solc carrier); the
r1 CR-1 record shows the same 58/48/38 (`r1/claims/c1/CR-1/evidence/out-A-hex.json`),
so this is the carrier's construction, not drift.

**Three-way agreement on the facts; verdict divergence on the semantics.**
RV-2 measured the identical facts and scored them **PASS** with an explicit scope note
(`RV-2/tools/check_legs.py:58-63`, `RV-2/evidence/kk-check-set1.txt:1-5`): *"the
'offsets land on JUMPDEST' reading applies to solc-convention carriers"*. EX-09's
driver instead treats "every offset lands on a JUMPDEST" as a **hard invariant** and
exits 1. Both are internally consistent; the divergence is a **convention choice**, not
a measurement disagreement. Named for the parent to adjudicate — see §7.

## 5. Independent verification performed by the late-join seat (rule #14)

Nothing in §2–§4 was taken on trust. `verify-independent.py` (this seat, new) is a
**separate implementation**: its own instruction walk and its own keccak sponge
(flat-lane indexing), importing nothing from `ex09-recon.py`.

| check | result |
|---|---|
| keccak self-test (`""`, `"abc"` vectors) | PASS |
| keccak cross-impl vs `js-sha3` (r1 solc prefix) | PASS (14/14 sigs) |
| keccak cross-impl vs EX-04's node `keccak.js` | PASS (14/14 sigs) |
| A/2, A/3, A/1 target bytes == authoring seat's upstream pin | PASS 3/3 |
| planted set == signature-derived set (9/9, 5/5, 3/3) | PASS 3/3 |
| own EQ-table K vs planted K | PASS 3/3 |
| 69 frozen legs: set / offsets / digest / form | PASS 69/69, 0 failures |
| landing expectation (JUMPDEST on A/2+A/3; non-JUMPDEST on A/1) | PASS 3/3 |

Reproduction of the landed artifacts (not just re-derivation of the facts): re-running
`run-recon.sh`'s three reconciler invocations against the landed inputs reproduces
`recon-carrierA-r3.txt`, `recon-OptVault.txt` and `recon-control.txt`
**byte-identically**, with the same exit codes (0 / 0 / 1). `bash controls.sh` likewise
reproduces `controls.txt` byte-identically (exit 0), and `keccak-test` reproduces
`keccak-self-test.txt` byte-identically.

**Census completeness (independent).** A fresh scan of all 246 probe-shaped JSON files
under round-3 `claims/**` (unwrapping `{ok,data,meta}` and evidence bundles), keyed on
`normalized_result.bytecode.sha256`, found exactly the leg sets the frozen lists name —
A/2 19, A/3 8, A/1 42 — with **zero** empty-function legs among them. The three
excluded files are all wrong-form traps (`raw` declared on a hex-text file) whose
decoded "bytecode" digest equals the *file* digest and whose function list is empty by
design (`EX-02/probe-carrierA-rawonhexfile-6.4.0.json`,
`EX-07/attack-hextext-as-raw-6.7.0.json`, `EX-06/trap-raw-declared-on-hex.json`) —
correctly excluded by the census rule, not silently dropped.

**Byte-sensitivity controls** (`controls.sh` / `controls.txt`, re-run byte-identically):
a one-byte flip inside the `01681a62` immediate removes exactly that selector from the
M1 table *and* from the M2 keccak scan (8/9) while the other 8 are untouched; the same
on OptVault (4/5); a flip on `a9059cbb`'s last byte makes the probe's reported selector
`a9059cbc` (absent from the code) and the M2 scan 2/3. The methods are byte-sensitive in
the direction claimed — a positive control, not an assertion.

## 6. Attacks / refutations attempted (late-join seat)

| # | attack | verdict |
|---|---|---|
| 1 | *The driver is buggy — the 129 anomaly is an artifact of my own parse* | **REFUTED.** The 126 probe-side failures were re-derived directly from the raw envelopes against the control's bytes, independent of the driver; the control's declared dests really are 2 bytes before its JUMPDESTs. |
| 2 | *The A/1 landing anomaly is a driver-vs-RV-2 disagreement about measurement* | **REFUTED as a measurement claim; CONFIRMED as a convention choice.** Both seats report the same numbers (38/48/58 vs 40/50/60); they differ only on whether that violates a hard invariant. |
| 3 | *My verifier's first run said the planted sets MISMATCH — the landed sets are wrong* | **REFUTED — my own bug.** My transcription of Keccak round constant RC[11] was wrong (`0x…8000800A` for `0x…8000000A`), so every selector it computed was garbage. Found by diffing my constant table against the landed tool's and by comparing absorption state. Fixed; re-run PASS. Recorded because the failure mode (trusting an unrun/mis-transcribed check) is exactly what rule #14 exists to prevent. |
| 4 | *The frozen leg lists were trimmed to exclude inconvenient legs* | **REFUTED.** An independent census over 246 probe-shaped files reproduces the three leg counts exactly (19/8/42) and shows no empty-function leg was dropped; the 3 exclusions are wrong-form traps. |
| 5 | *Planted sets were retrofitted post-probe* | **NOT RE-ATTACKED HERE (out of this seat's reach).** A/2's planted file is byte-identical to EX-03's frozen pin and is signature-derivable from the pinned source + solc; ordering evidence is the authoring seats' (EX-02 §3, EX-04 §4 A6, EX-07 §4.1). My contribution: the derivation is reproducible by a third party from the pinned bytes alone. |
| 6 | *The 5 non-dispatch PUSH4 constants in A/2 are unreported functions (false negatives)* | **REFUTED.** None is a dispatch selector: `6508d58f` is the encoded `stamp()` literal (`<<1` = `ca11ab1e`), `30cd7471`×2 = `NotOwner()`, `4e487b71` = `Panic(uint256)`, `43000825` lies past the metadata start (1373). The probe reports zero extras. |
| 7 | *A/3's linear shape proves the optimizer does not change dispatch shape* | **REFUTED (scoped).** A/3 (K=5) is linear; A/2 (K=9) is GT binary-search. Shape tracks table size here, not the optimizer flag — consistent with RV-2 §2 finding 2 and EX-08 §4 A2. |

## 7. Finding for the parent — a false statement in the entry draft (patch text filed)

The C1 entry draft line 46 (`.ufo/.../claims/c1/records-drafts/knowledge-entry-draft.md:46`,
mirrored at `SC-2/knowledge-entry-draft.md:46` and in all three EX-14 literals
`inputs/entry-literal-rev{2,4,C}.md:30-31`) states:

> `- **Observation (carrier-A control, cross-pin):** 3/3 planted selectors, zero extras, dispatch:"abi", offsets 38/48/58 JUMPDEST, at 6.4.0/6.5.0/6.7.0 × hex/raw; …`

**"offsets 38/48/58 JUMPDEST" is false.** Offsets 38/48/58 hold bytes `0x80`/`0x00`/
`0x00`; the JUMPDESTs are at 40/50/60. The sentence's own citation
(`EX-07/legA-compare.txt`) does not support it, and RV-2's contemporaneous note
(`seats/RV-2.md:179`) records the correct reading. Neither
`CR-2/proposed-entry-text-fixes.patch.md` (F1–F7) nor
`CR-1/proposed-entry-corrections.patch.md` catches this line, and the C1 verdict
(`claims/c1/verdict.md`) carries the "all quoted offsets land on JUMPDEST bytes" claim
in row 3 while scoping it only to solc carriers — the draft line is not scoped.

Patch text filed: `proposed-entry-fix-carrier-A-control-line.patch.md` (this seat).

## 8. Blockers

None for this seat's task. Named residuals:

1. **Convention, not measurement, divergence** (§4): the parent should decide whether
   the round's "every offset lands on a JUMPDEST" invariant is scoped to
   solc-convention carriers (RV-2's reading) or global (EX-09's driver). The driver
   currently exits 1 on A/1; RV-2 scores the same carrier PASS.
2. **A/1 is a legacy r1 artifact**, not a round-3 product; its broken dests predate this
   wave and are not a round-3 regression.
3. `ex09-recon.py`'s strict linear-chain parser returns an empty chain on the
   optimizer-enabled GT-split shape (by design — the EQ-site scan covers it); recorded
   in the output itself so the empty chain cannot be read as a zero-selector result.
