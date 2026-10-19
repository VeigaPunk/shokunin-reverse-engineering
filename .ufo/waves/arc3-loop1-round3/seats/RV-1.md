# RV-1 — seat report (chain c1, reviewer; LATE JOIN)

Wave `arc3-loop1-round3` · chain c1 · seat RV-1 · 2026-10-19 · repo
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · HEAD at work
`c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` (no seat commits; parent integrates).
Roster line: `claims-frozen.md` (roster "C1 chain (24): … RV-1 …"). Scratch
`/var/tmp/rv1-latejoin` (never `/tmp`); no git mutations; custody paths untouched
and read-only (hash/stat only); no LOG/SCORECARD/SHONEN/corpus/SKILL/README writes.

**Task (seat line).** Independently recompute both planted selector sets from the
carrier sources (`claims/c1/EX-02/carrierA.sol`, `claims/c1/EX-04/carrierB.sol`)
using a keccak path different from the planters; compare vs the planted files;
cross-check EX-09/EX-10 reconciliations if they exist.

**Completion statement: COMPLETED MISSING WORK + VERIFIED EXISTING WORK.**
RV-1's prior run landed `claims/c1/RV-1/tools/` (12 files) and
`claims/c1/RV-1/results/` (58 files) before the wave's token-plan lane hit its
quota; `results/poll.log` stops at poll 6 / 13:15:55Z and **no seat report was
ever written**. This seat (a) re-derived the whole claim with a *new* keccak path
and new tools, (b) independently verified the prior run's landed reconciliation,
and (c) wrote the missing report. Everything below is first-hand unless marked
"read".

---

## 1. Work performed (evidence pointers)

### 1.1 New keccak path (path D) — different from both planters

`RV-1/latejoin/tools/keccak_bits.py` — Keccak-256 with the state as a **200-byte
string** (the spec's byte view; lanes read/written as 8 LE bytes at `8*(x+5y)`),
round constants **derived** from the LFSR `rc(t)` and rho offsets **derived** from
the `(1,0)→(y,2x+3y)` walk recurrence. **No hardcoded RC/ROT tables in the file.**
sha256 `bf275fe66fcc67dc6f34b059c593dbef15faa4054489a45b517036fdbaf36ebc`.

Lineage check (why this is a distinct path):
- EX-02 planted with **js-sha3@0.8.0** (third-party JS, lane array).
- EX-04 planted with a hand-rolled **JS BigInt lane array with hardcoded RC/ROT**
  (`EX-04/evidence/keccak.js`).
- EX-10 planted with a **pure-Python lane array** (`EX-10/keccak.py`).
- RV-1's earlier tools: slice formulation (`keccak_slice.py`) + js-sha3 + solc.
- Path D shares no code and no tables with any of the above.

Self-test: 7/7 published vectors PASS (empty, `abc`, and four ERC-20 signatures
incl. full 32-byte digests), plus 3 rate-boundary probes (135/136/137 bytes).
`results/keccak-D-selftest.txt` (sha256 `0f70975ab7b0019bbb75c3110f6202cac9c2c6a750f1e4c0210fcd00d17086ee`).

### 1.2 Source-driven recomputation

`RV-1/latejoin/tools/recompute_carriers.py` (sha256 `831da98e…`) extracts the
external/public surface **from the `.sol` text** — `function` declarations plus
**public state-variable auto-getters** — canonicalises types, and derives every
selector with path D. Compares against the planted file, the landed solc ABI
artifact, and the runtime bytecode's PUSH4 immediates.

`results/recompute-all.txt` (sha256 `c1b768e1847acb77083404cf5d4bfd520a22a60f1168e683ae95554a4250e9d1`);
per-leg files `results/recompute-carrier{A,B}-EX-0{2,4}-*.txt`; machine form
`results/recompute-c1-rv1-latejoin.json`.

### 1.3 Five-path keccak cross-check on all 19 signatures

`results/path{A,B,D,E,F}-sigs.txt` + `.norm`. Paths: A = slice formulation
(RV-1 pre-existing), B = js-sha3@0.8.0 (EX-02's planter path), D = this seat's
byte-string path, E = EX-10's Python lane array, F = EX-04's BigInt JS.
**Pairwise diff matrix: all 25 pairs = 0 differing lines.** Every path
independently produced the same 19 selectors.

### 1.4 Envelope join (35 carrier envelopes)

`RV-1/latejoin/tools/join_envelopes.py` (sha256 `6659946c…`) joins every
`*.json` under `claims/c1/**` whose `normalized_result.bytecode.sha256` is one of
the three carrier runtime digests, and diffs the selector set against the path-D
source recompute. `results/envelope-join.txt` (sha256 `e0702341…`),
`results/envelope-join.json`.

### 1.5 Offset + trap verification

`RV-1/latejoin/tools/verify_offsets.py` (sha256 `f3638247…`) —
`results/offset-verify.txt` (sha256 `3de5a3b9…`), `results/offset-check.json`:
every `bytecode_offset` is a `0x5b` JUMPDEST byte in the decoded runtime; for
CarrierA every offset equals the JUMPI target of the EQ leg carrying that
selector (my own disassembler); trap legs classified.

### 1.6 Identity re-derivation (rule #14)

`results/identities.txt`. Every sha256 this report cites was re-derived with
`sha256sum`/`hashlib` **by this seat at write time**; nothing is copied from a
receipt. `EX-04/manifest.sha256.txt` re-verified by this seat: **44/44 OK**
(manifest file sha256 `1528195a5f3b15f90377a73e3adbbad1d193757c12fc06216029a77a5f3bc7d7`).

### 1.7 Negative controls (falsification of the audit itself)

`results/negative-controls.txt` (sha256 `e31bdae2…`). On scratch copies only
(custody/claim artifacts untouched):
- CONTROL intact `planted-A` / `planted-B` → SET-EQUAL True (my pipeline agrees).
- NEGCTL planted-A one digit flipped `01681a62`→`02681a62` → **detected**
  (extra `02681a62`, missing `01681a62`).
- NEGCTL planted-A one entry deleted (`rotate(address)`) → **detected**
  (missing `3f0d861a`).
- NEGCTL planted-A bogus entry added (`deadbeef`) → **detected** (extra `deadbeef`).
- NEGCTL planted-B one digit flipped `42cde4e8`→`42cde4e9` → **detected**.
- NEGCTL planted-B selector/sig pair swapped → **detected** (missing `2f54bf6e`).
5/5 mutations detected, 0 false negatives. The agreement below is therefore
non-vacuous.

### 1.8 Pre-probe ordering, re-derived from surviving scratch

`results/scratch-ordering.txt` (sha256 `67e0eedb…`). The **landed** planted files
carry copy mtimes and cannot prove ordering; the seats' scratch trees survive on
disk, so this seat re-read the original write mtimes:
- EX-02 `/var/tmp/ex02-r3`: `planted-A.txt` **13:07:41.918Z** → first probe
  `probe-carrierA-hex-6.4.0.json` **13:08:09.377Z** = **27.459 s** (receipt §3
  claims 28 s — consistent).
- EX-04 `/dev/shm/ex04-r3`: `planted-B-opt200.txt` **13:07:18.366Z** → first probe
  `probe/probe-opt200-hex-6.4.0.json` **13:07:27.704Z** = **9.338 s** (seat report
  §1 claims 9.3 s — consistent).
- EX-10 `/var/tmp/ex10-r3`: `planted-K.out` **13:07:24.642Z** → first probe
  **13:08:10.421Z** = **45.779 s** (recon-B §8 ordering — consistent).
Scratch planted files are **byte-identical** to the landed copies:
`/var/tmp/ex02-r3/out/planted-A.txt` = `88fa4393…` = `claims/c1/EX-02/planted-A.txt`;
`/dev/shm/ex04-r3/out/planted-B-opt200.txt` = `f32393c0…` = `claims/c1/EX-04/planted-B.txt`.
Scratch sources also byte-identical to the landed sources.

### 1.9 Prior-run artifacts verified (VERIFIED EXISTING WORK)

Read and checked against my own results (not re-run wholesale):
- `RV-1/tools/` (12 files) and `RV-1/results/` (58 files) exist and are
  internally consistent; `results/recompute-table.md` lists 61 legs.
- `RV-1/results/probe-vs-recompute.txt` joins **128** parsed probe envelopes to
  **57** recompute labels (73 `MATCH`, 55 `no-recompute-match`). I re-derived the
  join for the two carrier runtimes and my rows agree with its rows on every
  entry (same labels, same MATCH verdicts, same `no-recompute-match` classification
  of the trap/creation legs).
- `RV-1/results/poll.log` records 6 polls (13:10:55Z–13:15:55Z) and no verdict —
  confirming the run was cut short, not concluded.

---

## 2. Proposed changes (patch text)

**none.** This seat is a reviewer: it wrote only
`seats/RV-1.md` and `claims/c1/RV-1/latejoin/**`. No corpus, SKILL, README,
SCORECARD, LOG or custody edit is proposed. One *finding* for the parent's
records is recorded in §4.3 (a wording correction to the c1 verdict's own
narrative, not a change to any measured result) — offered as text, not applied.

---

## 3. Before → after measurement for chain c1's claim

The chain's claim is coverage: optimizer-enabled carriers recovered **K/K, zero
extras** by `inspect-evm-interface`, planted-K recorded pre-probe. RV-1's part is
the selector-set leg. Before → after for the two carriers the seat line names:

| carrier | source sha256 | K (path D) | planted K | set-equal | selector mismatches | mutability mismatches |
|---|---|---|---|---|---|---|
| `carrierA.sol` → CarrierA | `05b2cbb0c6fd97ae…` | **9** | **9** | **True** | 0 | 0 |
| `carrierB.sol` → VaultB (opt200) | `14566042e4528cdc…` | **11** | **11** | **True** | 0 | 0 |
| `carrierB.sol` → VaultB (noopt) | `14566042e4528cdc…` | **11** | **11** | **True** | 0 | 0 |

- **Probe side:** 35 envelopes (17 CarrierA, 18 VaultB) — every one **set-equal**,
  **0 missing / 0 extra**, `dispatch:"abi"` on every entry, 0 disagreements.
- **ABI side:** set-equal to the landed solc ABI artifacts on all three legs
  (`carrierA.abi.json` `0cd46e65…`; `carrierB.abi-{opt200,noopt}.json` `2be500d7…`).
- **Byte side:** all 11 VaultB selectors and all 9 CarrierA selectors are present
  as PUSH4 immediates in the decoded runtime; the non-selector PUSH4 constants in
  the optimized code (`4e487b71` Panic, plus `30cd7471`/`43000825`/`6508d58f` on
  CarrierA) are **not** in either planted set and were reported by no probe leg —
  so zero-extras is meaningful on these bytes, not vacuous.
- **Offsets:** 351 entries checked — **0** non-JUMPDEST offsets; **0** CarrierA
  entries whose offset differs from my parsed EQ/JUMPI target.
- **Ordering:** all three planted sets recorded before their first probe
  (27.5 s / 9.3 s / 45.8 s), re-derived from surviving scratch mtimes.

**Verdict on the seat line: the planted selector sets are CONFIRMED.** Both
reproduce exactly from the carrier sources under a keccak path that shares no
code or tables with either planter, and under four further independent paths;
the planted files agree with the compiler's own ABI and with the runtime bytes.

---

## 4. Attacks / refutations attempted, with verdicts

### 4.1 Retrofitting / post-hoc planting — NOT SUSTAINED

Attack: the planted set could have been written after seeing probe output.
Evidence against: scratch mtimes show planted **before** first probe on all three
targets (27.5 s / 9.3 s / 45.8 s), re-derived by this seat from the original
writes, not from receipts; and the sets are third-party re-derivable from the
frozen sources + pinned solc, as this seat's own path-D recomputation demonstrates
without ever reading a planted file. **Verdict: not sustained.**

### 4.2 Vacuous zero-extras (decoys that should have appeared but didn't) —
NOT SUSTAINED

Attack: "zero extras" would be vacuous if the carrier code contained no
non-selector PUSH4 constants. My PUSH4 census finds 4 non-selector constants in
the optimized CarrierA code and 1 in optimized VaultB (`4e487b71` Panic); none was
reported as a function by any of the 35 envelopes. **Verdict: not sustained — the
clause is exercised on real decoys.**

### 4.3 Mutability field: probe says `view` where source says `pure` — SUSTAINED as
a *documentation* gap, NOT a plant defect

Measured exactly: **35 of 351 entries**, all of the form `pure → view`, on exactly
two selectors — `0xc85e07b9 stamp()` (CarrierA, 17 envelopes) and
`0x07bf89ab computeTxHash(address,uint256,bytes32,uint256)` (VaultB, 18
envelopes). Every other mutability class agrees perfectly
(`view` 158/158, `nonpayable` 123/123, `payable` 35/35).

- The **planted files carry the correct `pure`** (`planted-A.txt` line for
  `c85e07b9` reads `[pure]`; `planted-B.txt` for `07bf89ab` reads `[pure]`), and
  the ABI artifacts say `pure`. So no planted value is wrong.
- EX-04's own `evidence/probe-receipt.txt` already records the VaultB instance
  ("upstream inference reports pure fn computeTxHash(…) as `view`"), and EX-02's
  own `evidence/probe-vs-planted-A.txt` already flags the CarrierA instance
  ("`c85e07b9 … probe_mut=view  abi_mut=pure  <-- mutability differs`").
- However the c1 chain verdict (`claims/c1/verdict.md:56-57`) names only the
  **EX-04** instance: *"first pure-leg mutability delta (`pure → view` for EX-04's
  `computeTxHash`)"*. `grep -n 'c85e07b9\|stamp()' claims/c1/verdict.md` → **0
  hits**. The CarrierA instance is a *second* pure-leg delta of the same class,
  present in EX-02's own evidence but absent from the verdict narrative.

Suggested wording for the parent (text only; no measured result changes):
> two pure-leg mutability deltas (`pure → view`): EX-04's `computeTxHash(…)` and
> EX-02's `stamp()` — the inference layer separates mutating from non-mutating,
> not pure from view; both planted sets and both ABI artifacts carry `pure`.

**Verdict: the delta itself is a recorded upstream-inference limitation, not a
plant error; the verdict's enumeration is incomplete (one of two instances).**

### 4.4 Trap legs could silently "succeed" — NOT SUSTAINED

24 zero-function envelopes found. The raw-encoding-over-hex-text legs
(EX-02 `probe-carrierA-rawonhexfile`, EX-04 `probe-{opt200,noopt}-raw`, EX-08
`probe-VaultB-trap-raw-on-hexfile`, EX-10 `probe-EX04carrierB-opt200-rawonhex-trap`,
EX-12 `probe-carrierA-source-raw`, `probe-empty-hex`) all decode to the sha256 of
the **file's text bytes** — parsed-and-empty, no silent success. The remaining
zero-function envelopes are creation-blob / dispatchless / empty subjects, which
is the expected outcome class, not a failure. **Verdict: not sustained.**

### 4.5 EX-09 offset conventions inconsistent — NOT SUSTAINED (display convention)

EX-09's artifacts use three offset conventions. I re-derived all three from the
decoded bytes:
- `extract-carrierA-r3.json:push4_all` — **opcode pc**. My `push4_sites` output is
  **byte-identical**: 15/15 pairs identical.
- `scan-carrierA-r3.json:offsets` — **immediate offset** (pc+1). Verified for every
  selector: `scan offsets == my pc+1` → True.
- `jumpdests-carrierA-r3.txt` — **probe convention** (the PUSH2 target), e.g.
  `01681a62` at 164, which equals my parsed EQ/JUMPI target set
  `{164,214,235,266,297,331,383,437,470}`.
All three reconcile to one underlying parse. **Verdict: not sustained — a
documentation convention, no discrepancy.**

### 4.6 My own extractor / harness errors (self-attacks, all caught and fixed)

Disclosed for rule #14 honesty; each was mine, not the plants':
1. First pass extracted K=7 for CarrierA vs planted K=9 — my extractor had no rule
   for **public state-variable auto-getters** (`owner()`, `totalCredited()`).
2. Second pass: my `VAR_RE` **consumed the trailing `;`**, so consecutive
   declarations matched only the first (K=8). Fixed with a lookahead.
3. I hashed the runtime **hex text** instead of decoded bytes, producing a digest
   that matched nothing. Fixed; the corrected digests reproduce the seats' values
   exactly (`9f7392acccea…` / `aaf85ceaf124…` / `678678e9…`→`679678e9…`).
4. `verify_offsets.py` read `bytecodeOffset` (the `raw_result` camelCase key) from
   `normalized_result`, which uses `bytecode_offset` — producing 351 spurious
   "None" offsets. Fixed; 0 non-JUMPDEST offsets after the fix.
5. `join_envelopes.py` crashed on non-dict JSON envelopes. Fixed with a type guard.

Each bug was caught by the harness disagreeing with itself or with the seats —
which is the reason the negative controls in §1.7 exist.

### 4.7 Cross-check of the two reconciliations named in the seat line —
EX-09 and EX-10 both exist and both hold

- **EX-09** (`claims/c1/EX-09/`, 41 artifacts): `recon-carrierA-r3.txt` ends
  `VERDICT: ALL SOURCES AGREE (sets+offsets+pins); every offset lands on a
  JUMPDEST`, with 21 sources agreeing on n=9, 0 missing / 0 extra. My path-D
  recompute agrees. Its K=5 OptVault control (`planted-OptVault.copy.txt`,
  `sigs-OptVault.txt`) also reconciles 12/12 sources at n=5.
- **EX-10** (`claims/c1/EX-10/recon-B.md`, 15445 B): reports K/K 11/11 on 13
  carrier-B envelopes with `all_probe_offsets_are_leg_targets: true`; my
  independent parse of `carrierB.runtime-opt200.hex` reproduces its EQ targets
  exactly (`07bf89ab`→221, `0bf6cc08`→271, `0db02622`→289, `2f54bf6e`→308,
  `42cde4e8`→355, `59bf77df`→375, `797af627`→418, `960bfe04`→451, `a8c162fb`→482,
  `d0e30db0`→513, `d9caa3d2`→521; GT navigation label `59bf77df`→98) and the noopt
  set (`…→248/308/350/392/452/494/554/594/634/674/684`, GT→99). **Agreement 11/11
  on both legs, independently derived.**
- Note (naming): three different artifacts are called "carrier B" in this wave
  tree — EX-04's `VaultB` (K=11, the wave's carrier B), EX-05's `CarrierB` (K=8),
  and EX-10's own `VaultB` (K=13). The seat line's `carrierB.sol` resolves to
  EX-04's K=11 `VaultB`; I audited that one and did not conflate them.

---

## 5. Blockers

**None for the seat task.** Named residuals (none voids the verdict):

1. **Landing is the parent's.** No seat commits; HEAD stayed `c07af80f`. Every
   number here is measured in the worktree, not at a work commit.
2. **`/tmp` EDQUOT / scratch volatility.** Ordering evidence depends on scratch
   mtimes that still exist *today* but are not durable (`/var/tmp`, `/dev/shm`).
   EX-04 itself names this as residual 1 in its report. If the scratch trees are
   reaped, the ordering argument reverts to the receipts' own claims — though the
   *content* stays third-party re-derivable from the frozen sources, as this
   seat's recomputation shows.
3. **Two naming collisions to keep straight** (three "carrier B"s, per §4.7).
4. **`pure → view` delta is under-enumerated in `claims/c1/verdict.md`** (§4.3):
   the CarrierA `stamp()` instance is absent from the verdict's narrative though
   present in EX-02's own evidence. Text-only correction suggested; no measurement
   changes.
5. **EX-10's `planted-K.json` uses a `entries[]` JSON schema** while
   `planted-A.txt`/`planted-B.txt` use the flat `0x<sel> <sig> [mut]` text schema.
   Both were parsed correctly by my tools (and by RV-1's `parse_planted`, which
   handles both), so this is a note, not a defect.

---

## 6. Artifacts written by this seat

- `seats/RV-1.md` — this report.
- `claims/c1/RV-1/latejoin/tools/keccak_bits.py` — path-D keccak (sha256 `bf275fe6…`).
- `claims/c1/RV-1/latejoin/tools/recompute_carriers.py` (sha256 `831da98e…`).
- `claims/c1/RV-1/latejoin/tools/join_envelopes.py` (sha256 `6659946c…`).
- `claims/c1/RV-1/latejoin/tools/verify_offsets.py` (sha256 `f3638247…`).
- `claims/c1/RV-1/latejoin/results/` — 24 files: `keccak-D-selftest.txt`
  (`0f70975a…`), `recompute-all.txt` (`c1b768e1…`), `recompute-carrier*.txt` ×3,
  `path{A,B,D,E,F}-sigs.txt` + `.norm` ×10, `envelope-join.txt` (`e0702341…`)
  + `.json`, `offset-verify.txt` (`3de5a3b9…`) + `.json`, `identities.txt`,
  `negative-controls.txt` (`e31bdae2…`), `scratch-ordering.txt` (`67e0eedb…`),
  `all20-sigs.txt`, `recompute-c1-rv1-latejoin.json`.
- Scratch (not landed): `/var/tmp/rv1-latejoin/**`.

`__pycache__` was removed from the landed tree before finishing (the r2 precedent
excludes pycache from commits). All sha256 values in this report were re-derived
at write time from the files as landed; none is quoted from a receipt.
