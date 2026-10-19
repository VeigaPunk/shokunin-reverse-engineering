# SEAT RV-2 | CHAIN c1 | ROLE reviewer — arc3-loop1-round3 (2026-10-19)

Task (seat line): re-run one probe leg per carrier yourself (disk-backed TMPDIR);
verify K/K, dispatch fields, envelope ids; compare vs EX-06/07/08. Seat report.

**VERDICT: ALL MEASURED CHECKS PASS.** 29/29 of my re-run legs reproduce the seats'
recorded envelope ids AND the full envelopes byte-for-byte at the same absolute
carrier paths (`evidence/verify-ids-and-envelopes.txt`, mechanical, 29/29 PASS);
K/K (recovered == oracle, zero extras) verified for **18 distinct carrier byte-sets**
(r1 reference carriers included) with independent oracles (keccak256 over compiled
ABIs / solc methodIdentifiers / a byte-identical recompile); `dispatch:"abi"` on every
function of every leg; decoded-digest binding and dispatch-offset semantics verified on
every leg (`evidence/kk-check-set1.txt` 13/13, `kk-check-set2.txt` 10/10, both exit 0).
The chain's honest-stop branches are **not triggered**: every round-3 carrier sits in
the r1-recorded `5f3560e01c` prologue class and recovers K/K.

Three findings for the record (none voids the claim; each is a measured correction or
delta):
1. **Record defect (patch text proposed):** EX-07's `Rv2TokenOpt.planted-K.json` is
   **sha3_256** — both generations (pre-probe and the 13:08:45Z "correction") — not
   keccak256. The probe is right; the planted file is wrong (its own
   `oracle_set_match: false` flag is correct but misreadable). See §2.
2. **Shape delta for the entry:** the round-3 carriers add a second dispatch shape —
   solc's GT **binary-search** dispatcher for ≥7-function tables (first compare op
   `11`/GT), while ≤6-function tables use the r1-documented EQ chain (`14`/EQ). Both
   shapes recover K/K with `dispatch:"abi"`; the optimizer does **not** change the
   shape class (VaultB nopt vs opt200 differ only in bodies), and every carrier remains
   in the r1-recorded `5f3560e01c` prologue class.
3. **Host-state change:** `/tmp` quota has cleared (92M/16G at 13:14Z): a TMPDIR-unset
   probe now exits 0 with a field-identical envelope (`evidence/my-optB-hex-6.4.0-noTMPDIR.json`
   == `evidence/my-optB-hex-6.4.0.json`). The r1 records' "disk-backed TMPDIR required"
   stands as a historical measurement; all my legs still used
   `TMPDIR=/var/tmp/rv2-r3/tmp` per the wave rule.

Repo HEAD at work: `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311`. Writes: only this
report + `claims/c1/RV-2/**`. No git mutations; custody paths never touched; scratch
under `/var/tmp/rv2-r3` plus `/dev/shm/ex06` (EX-06's recorded path, recreated with
the pinned bytes to test id re-derivation); nothing written to `/tmp` beyond one
1-byte writability control (removed).

## 1. Work performed (each item with an evidence pointer)

- **Toolchain receipt re-verified before reuse (no install):** prefix
  `tools/solc-prefix` `soljson.js` sha256 `221d7a667378b5068d913e75fe092507e061363cd1d23b64c49ae82febabad4c`
  and npm-cache tarball sha256 `0e1a1ab6d12c37f5503271b2c4679cd433459c884851920d148d6fb154575a51`
  (6,476,046 B) both match EX-02's r1 receipt; `solcjs --version` →
  `0.8.37+commit.f401782d.Emscripten.clang`.
- **Probe legs run by me** with the cached rea-agents trees (`6.4.0`
  `~/.npm/_npx/dea9475797100b20`, `6.5.0` `ad9a3fdbcad992c6`, `6.7.0`
  `a1722018f28f9df2`; `node v26.12.0`), every run with `TMPDIR=/var/tmp/rv2-r3/tmp`,
  `--format json`, stderr captured. 34 runs total → `evidence/*.json` (+`*.err`, all
  empty where written). 29 of them are the id/envelope re-derivation set (below);
  5 are controls (raw twins, creation-code, no-TMPDIR).
- **r1 reference legs (pre-round-3 baseline, re-derived):**
  Rv2Token hex@6.4.0 `ev_45849c8b…` (repo path), Rv2Many hex@6.4.0 `ev_d0d0b054…`,
  KdxToken hex@6.7.0 `ev_56d89cb4…` (path `/dev/shm/ex06/…` recreated from EX-07's
  retained bytes, sha `69a15782…`): all three field-identical to the r1 records.
- **Round-3 carrier legs (one leg minimum per carrier; extram legs for id checks):**
  every leg's id re-derived AND full envelope identical to the owning seat's record.

  | carrier | source seat | runtime sha256 (16) | K | legs (pins/encodings) | ids (prefix) |
  |---|---|---|---|---|---|
  | carrier-A (r1 CR-1 hand-asm control) | CR-1 (r1) | `a92ba15225aaddcc` | 3 | hex 6.4.0/6.5.0/6.7.0, raw 6.4.0 (2 paths) | `ev_7b642e6b…` etc. |
  | Rv2TokenOpt ("optB") | EX-07 | `ed6c8a76d05b230e` | 5 | hex 6.4.0/6.7.0, raw 6.4.0 | `ev_6ed8aa4e…` |
  | VaultB opt200 | EX-10 | `b24a01153af943ff` | 13 | hex 6.4.0/6.7.0 | `ev_d409bd50…` |
  | VaultB nopt | EX-10 | `bcdf64abcda096e3` | 13 | hex 6.4.0/6.7.0 | `ev_294431e4…` |
  | CarrierB | EX-05 | `b9c70178069601ba` | 8 | hex 6.4.0 | `ev_6da00ac5…` |
  | carrierB opt200 | EX-04 | `aaf85ceaf124bac2` | 11 | hex 6.4.0 | `ev_e0ee9bea…` |
  | carrierB noopt | EX-04 | `679678e9a67aee70` | 11 | hex 6.4.0 | `ev_ca4595f0…` |
  | OptVault | PL-1 | `544469b7…` | 5 | hex 6.4.0 | `ev_13a039e7…` |
  | MutMix | PL-1 | `6267ef53…` | 6 | hex 6.4.0 | `ev_913cb961…` |
  | MutMixOpt | PL-1 | `200bc9db…` | 6 | hex 6.4.0 | `ev_df117360…` |
  | CrVault on200 | CR-2 | `2e636c0f6b5fd499` | 7 | hex 6.4.0 | `ev_b7c10ecf…` |
  | CrWide on200 | CR-2 | `617c91cc3b17b21c` | 22 | hex 6.4.0 | `ev_65542703…` |
  | Rv2Token.opt200 | SC-1 | `ed6c8a76d05b230e` | 5 | hex 6.4.0 | `ev_42cd9da2…` |
  | VaultCourt.opt200 | SC-1 | `66024ee346226a44` | 10 | hex 6.4.0 | `ev_d1d0bc1c…` |
  | EX-03 CarrierA (assigned "carrier A") | EX-03 | hex `87d1bb03…` / bin `9f7392ac…` | 9 | hex 6.4.0/6.7.0, raw 6.4.0 (2 scratch paths) | `ev_13bdbfc0…`, `ev_36daf496…` |

  (sha column = decoded runtime bytecode sha256 (16) as measured by my probe legs
  (`normalized_result.bytecode.sha256`) and cross-checked by `sha256sum` over the
  carrier bytes — the digest-binding column of `evidence/kk-check-set*.txt`, all OK;
  the r1 CR-1 control's digest is the decoded 84-byte program.)
- **Independent K/K oracles (not the seats' planted files):** keccak256 of the
  compiled ABI signatures via the prefix tree's `js-sha3@0.8.0`
  (`tools/selectors.js`); SC-1's solc-emitted `methodIdentifiers.json`; and, for
  EX-03's CarrierA, a **byte-identical recompile** of their own `solc-input.json`
  (runtime 1426 B sha256 `9f7392acccea72cd42bdd8095a8578cab0727766f218b5399da22bc21d23741a`
  — the probed carrier) whose ABI yields the 9-selector oracle set.
- **Name resolution recorded:** EX-07's report resolves the wave's "carrier A" as
  EX-03's `CarrierA` (opt200, K=9); this seat covers that carrier via both scratch
  paths (`ex06-r3/work/ex03`, `ex07/ex03`) **and** the r1 CR-1 hand-assembled
  `carrier-A.hex/bin` control (which two seats also probed) — so both readings are
  measured.
- **Files:** `claims/c1/RV-2/evidence/` (34 probe JSONs + 32 stderr files +
  `verify-ids-and-envelopes.txt` + `kk-check-set1.txt` + `kk-check-set2.txt`),
  `tools/` (`selectors.js`, `check_legs.py`, `check_legs2.py`,
  `verify-ids-envelopes.py`), `proposed-ex07-planted-K-correction.patch.md`,
  `MANIFEST.sha256`, `report.identity.txt`.

## 2. Proposed changes

- `claims/c1/RV-2/proposed-ex07-planted-K-correction.patch.md` (sha256
  `bc5a3c4b46ef767d6f338194f04f5ba3d48b506a66b222fd0302043f6060095e`, text in file)
  — record-correction for EX-07's optB planted-K
  (wrong hash family, both generations). **Not applied** by this seat; parent-routable
  as an EX-07 artifact revision or a round-report note. The claim's K/K does not
  depend on that file: it stands on the ABI/keccak oracle, the r1 oracle, and the
  probe legs (all 5/5, ids re-derived).
- No corpus/SKILL/README/PROVINCE proposals, none applied. For the entry author
  (observational, not a required change): if the entry describes dispatch shapes,
  record the two measured classes — EQ chain (≤6 external functions) and GT
  binary search (≥7) — with the `5f3560e01c` prologue constant across both, since
  "dispatch-shape" wording is now the entry's burden.

## 3. Before→after measurement (chain c1 claim)

The claim: at least one optimizer-enabled carrier + one non-ERC-20-shaped carrier,
planted selectors recovered K/K by `inspect-evm-interface`, both pins where feasible.

**BEFORE (r1 record, the baseline this round extends):** optimizer-disabled ERC-20
carriers only; dispatch prologue classes recorded `5f3560e01c`/`60003560e01c`;
Unknowns list ("optimizer-enabled dispatch shapes beyond the smoke compile").
Offsets recorded as dispatch-target JUMPDESTs (r4 erratum), solc carriers only;
`/tmp`-defaulted probes fail EDQUOT (host condition).

**AFTER (this seat, measured):**

```
$ TMPDIR=/var/tmp/rv2-r3/tmp node <rea 6.4.0>/scripts/rea.mjs \
    inspect-evm-interface <carrier> hex --format json      # exit 0, stderr empty
# optimizer-enabled + non-ERC-20 carriers (6.4.0 unless noted):
#   VaultB opt200  13/13 dispatch=abi   ev_d409bd50…   (receive/fallback + library + 4 mutability classes)
#   CarrierB        8/8  dispatch=abi   ev_6da00ac5…   (payable receive+fallback, library-bound)
#   carrierB opt200 11/11 dispatch=abi  ev_e0ee9bea…
#   OptVault opt200  5/5  dispatch=abi  ev_13a039e7…
#   MutMix (nopt)    6/6  dispatch=abi  ev_913cb961…  ; MutMixOpt 6/6 ev_df117360…
#   CrVault 7/7, CrWide 22/22, VaultCourt 10/10, EX-03 CarrierA 9/9, optB 5/5 …
# zero missing / zero extra on every leg (set equality vs ABI oracles)
$ python3 check_legs.py ; python3 check_legs2.py      # 13/13 PASS, 10/10 PASS, exit 0
```

- **Both pins where feasible:** 6.4.0 and 6.7.0 on optB/VaultB(×2)/carrier-A/6.5.0+6.7.0
  on CR-1 carrier-A/legC; payload selector sets and decoded digests identical across
  pins; ids differ per version (as recorded in r1 — id is version+path+encoding bound).
- **Honest-stop branches NOT triggered:** every probed prologue class is the
  r1-recorded `5f3560e01c` (measured across all 18 carriers); no typed refusal or
  parse-empty on runtime carriers; creation-code legs are parsed-and-empty (0
  functions) exactly as the r1 EX-08 finding predicts — `ev_9a638f40…`, `ev_cb06a144…`.
- **hex≡raw on the new shapes:** raw legs for optB/carrier-A/VaultB/CarrierB give
  `raw_result` deeply equal and normalized function records equal to their hex twins
  (bytecode sha equal, artifact encoding/bytes differ as documented) — the r1 EX-06
  equivalence extends to optimizer and fallback shapes.
- Command A / the entry / the map token are other seats' landings (EX-14/RV-4
  before-state; SC-2/RV-4 token patch; implementer's entry); this seat's measurement
  covers the probe/selector/K-K sub-claim only.

## 4. Attacks / refutations attempted (verdicts)

1. **Id determinism/re-derivation attack** — 29 legs re-run at the seats' exact
   absolute paths on the same rea pin: **29/29 ids re-derived AND full envelopes
   byte-identical** (not just ids). Cross-version legs differ in id with identical
   selector payloads; renamed path differs in id (SC-1's `.renamed` leg mirrors this;
   EX-07's `idpath-*` legs too). Verdict: PASS (id = f(rea version, absolute path,
   encoding); no randomness).
2. **K/K oracle-independence attack** — I did not trust any planted file: sets were
   re-derived from ABIs (js-sha3 keccak), solc `methodIdentifiers`, or a recompile.
   This **caught EX-07's planted-K defect** (sha3_256 vs keccak256, both generations;
   `a613914d04…` = sha3_256("approve(address,uint256)")). Probe sets match the true
   oracles everywhere. Verdict: planted file REFUTED; probe K/K CONFIRMED.
3. **Carrier-provenance attack** — recompiled EX-03's `carrierA` from their landed
   `solc-input.json` with the receipted solc: runtime byte-identical (1426 B,
   `9f7392ac…`), ABI matches the probed 9-set; their PUSH4 site census (15 sites incl.
   error constants `6508d58f/30cd7471/4e487b71/43000825`) contains exactly my 9
   dispatch selectors as reported functions — decoys not reported. Verdict: PASS.
4. **False-positive/extra-selector attack** — per leg, recovered set == oracle set
   (zero missing, zero extra); CR-1 carrier-A's decoy `deadbeef`/`ffffffff` PUSH4
   constants unreported; CrWide's 22-function table exact. Verdict: PASS.
5. **Offset-semantics attack** — all solc carriers: every reported offset is byte
   `0x5b` (JUMPDEST). CR-1's hand-assembled control: reported offsets 38/48/58 are
   the **declared jump immediates** and its `0x5b` bytes sit at 40/50/60 (immediates
   2 short) — and r1's CR-1 record shows the same 58/48/38, so this is the carrier's
   construction, not drift; the "offsets are JUMPDESTs" reading is scoped to
   solc-convention carriers. Verdict: PASS with the scoping recorded.
6. **Dispatch-shape attack** — ≥7-function tables use GT binary search, ≤6 EQ chain;
   all recover K/K with `dispatch:"abi"`; optimizer on/off changes neither class nor
   prologue; the extractor is not defeated by the shape delta. Verdict: PASS.
7. **hex≡raw divergence** — raw twins deeply-equal payloads (optB, carrier-A, VaultB
   opt200, CarrierB); wrong-form traps visible in EX-06's round-3 battery reproduce
   their r1 hazard notes. Verdict: no divergence found on any measured leg.
8. **Silent-empty blind spot (EX-08's r1 hazard)** — I used set-equality against
   pre-derived oracles (not emptiness) as the discriminating check, exactly as EX-08
   recommended; creation-code controls return 0 functions (honest parsed-and-empty).
   Verdict: PASS.
9. **Environment confounds** — TMPDIR-unset leg now exits 0 with field-identical
   envelope (`/tmp` quota cleared; measured); every primary leg still disk-backed.
   Verdict: environmental, recorded.
10. **Bookkeeping sweep of the seats' cited numbers** — EX-10's planted-K (K=13,
    recorded pre-compile) verified ABI-consistent by my keccak; EX-05's K=8 likewise;
    EX-06's EX03 PUSH4 census consistent with my recompile; SC-1/EX-04/CR-2/PL-1
    probe records reproduce field-identically. No mismatch beyond the EX-07 item.

## 5. Blockers

- None for this seat's deliverable; all dependencies (other seats' carriers and probe
  records) landed while I worked, and the gaps that existed at open were polled and
  closed rather than guessed.
- Notes for the parent: (i) route the EX-07 planted-K patch text (or record its note);
  (ii) the entry author should state the EQ-vs-GT dispatch-shape delta if the entry
  describes shapes; (iii) the r1 recheck line's "disk-backed TMPDIR required" host
  condition no longer reproduces (quota cleared) — the requirement remains sound
  practice but is not currently falsifiable as written.

Identity (rule #14): this report's own byte-identity (sha256, plus the
`MANIFEST.sha256` family hash) is in `claims/c1/RV-2/report.identity.txt`,
written after this file's final revision; nothing in this report claims a hash of
itself that predates that derivation.