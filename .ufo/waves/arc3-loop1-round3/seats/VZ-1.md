# SEAT VZ-1 | CHAIN c1 | ROLE convergence — arc3-loop1-round3 (2026-10-19), LATE JOIN

Task (seat line): LATE JOIN. A verdict packet may already exist at
`claims/c1/verdict.md` — read it first, reconcile the c1 chain end-to-end:
verify each claim component has first-hand or independently recomputed
evidence (K/K recoveries, command-A projection 83/83, line-neutral map token,
honest-stop branches not needed). If complete and accurate, adopt it; if gaps
exist, fill them. Write `claims/c1/verdict.md` (final) + this seat report,
naming any seat whose evidence is missing.

**Status: COMPLETED the missing work and VERIFIED existing work.** A verdict
packet existed (rev 2, ~13:20Z). It was accurate for the state it measured, but
the wave kept delivering after it: the entry literal moved to rev 4
(`3b5f371e…`, 17,708 B, mtime 13:17:51Z local) and the map-token patch was
amended to additive-only (`9af31408…`, 13:17:15Z) — both postdating rev 2's
last read and RV-3's first grade pin. I re-measured the whole chain on the
current pair first-hand and wrote **verdict rev 3** (adopting rev 2's
structure and findings, correcting one enumeration gap and closing two debts).

## 1. Work performed (evidence pointers)

All scratch under `/var/tmp/vz1b/` (never `/tmp`). Writes: `claims/c1/verdict.md`
(rev 3), this report, `claims/c1/VZ-1/evidence2/`. No git mutations; custody
paths read-only (hash/stat only); no LOG/SCORECARD/SHONEN/corpus edits.

1. **Baseline** — command A (SCORECARD recipe, `git show` form) at HEAD
   `c07af80f…`: 82/82, 14/14, missing [], dangling [] (own run).
2. **Current-pair projection** — fresh `git clone --no-hardlinks` at HEAD;
   applied the rev-4 literal (`3b5f371e…`) + the records-drafts additive PRIMARY
   token (`786efbb2…`, byte-identical to RV-4's strict-additive patch new line);
   committed in the clone; command A = **83/83**, missing [], dangling [], 14/14;
   prior-82 byte-identical (per-file `git show` compare, zero diffs); README
   190 → 190, changed lines `[38]`, after-sha `a451ad16…`; `git diff
   --name-status` = `M corpus/README.md` + `A corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md`.
   Evidence: `VZ-1/evidence2/projection-final.json`.
3. **K/K re-derivation** — receipted `js-sha3` keccak over each compiled ABI,
   set-equality vs the planted file and the sealed envelope: VaultB opt200 13/13,
   VaultB nopt 13/13, carrierB@EX-04 opt/noopt 11/11, CarrierB 8/8,
   CarrierBErr 8/8, Rv2TokenOpt 5/5 — `abi == env == planted` **true on every
   leg**, `dispatch:"abi"` everywhere. Evidence:
   `VZ-1/evidence2/kk-rederive.txt`.
4. **Recheck line, verbatim** — 6.4.0 run reproduced `ev_d409bd50…`, envelope
   `05f76b33…` — `cmp` byte-identical to EX-10's capture and SC-2's copy;
   6.7.0 run reproduced `ev_ae5aaee0…` = the landed 6.7.0 envelope.
   Evidence: `recheck-vaultb-opt200-{640,670}.json`.
5. **Byte-exact recompile** — `node EX-10/compile.js <receipted prefix>
   EX-10/VaultB.sol <out> 1 200`: runtime 1,621 B `b24a0115…`, creation
   `ac614a6e…`, ABI `6dae6710…` — all equal to the landed `out/` files.
6. **Probe** — citation-drift at HEAD and at my projected commit, default and
   `--strict`: findings=0 exit=0 (×4); `--selftest` 13/13 exit 0; the table
   `bfc42f1b…` matches the `expected.json` digest pin.
7. **PUSH4 census (opcode-aware)** — VaultB.opt200 24 sites (13 selectors, 2
   duplicated by the GT/EQ binary search, 4 panic/error constants, 2
   trailer-derived), VaultB.nopt 16 sites (13 selectors, 2 duplicated, 1
   trailer-derived), Rv2TokenOpt 7 sites (5 selectors, `4e487b71`, trailer
   `43000825` at 971 ≥ cborStart 927). No non-selector constant reported as a
   function. Evidence: `VZ-1/evidence2/push4-census.txt`.
8. **Citation sweep** — brace-expansion over the rev-4 literal (154
   candidates): the only unresolved names are the `optB-…-rerun` set (F2).
   Evidence: `VZ-1/evidence2/citation-sweep-final.txt`.
9. **Receipt re-hash** — `soljson.js 221d7a66…abad4c`, `solc/package.json
   b3a90035…3491` = the r1 receipt pins. No install.
10. **Read (not re-run)** — rev 2 verdict + `VZ-1/verification-log.txt`;
    RV-3's rev-4 regrade (`quality-grade-rev4.md`, `proposed-entry-fixes-rev4.patch.md`)
    and its `commandA-rehearsal-rev4.txt`; RV-1's audit (§4.3 enumeration gap);
    EX-09's report; RV-2/RV-4 manifests; CR-1/CR-2 patch texts.

## 2. Proposed changes

- **None of my own** beyond the verdict rewrite. The chain's fix texts are
  already packaged by other seats and are cited in verdict rev 3 §"Named debt":
  `RV-3/proposed-entry-fixes-rev4.patch.md` (`1e191bd8…`, FIX-1..6),
  `CR-2/proposed-entry-text-fixes.patch.md`, `CR-1/proposed-entry-corrections.patch.md`,
  `RV-2/proposed-ex07-planted-K-correction.patch.md` (superseded in practice —
  EX-07's planted-K v3 is in the tree).
- **Landing choice (debt #11 in the verdict):** land the **records-drafts**
  pair — literal `3b5f371e…` + additive token `786efbb2…` (after-README
  `a451ad16…`). The SC-2 mirror's token copy (`333ca590…`, reworded,
  after-README `016b632e…`) is superseded.

## 3. Before → after measurement for the chain's claim

| quantity | before | after (rev-4 literal + additive token, clone projection) |
|---|---|---|
| command A | 82/82, missing [], dangling [], rules 14/14, 10.0/10.0 at `c07af80f` | **83/83**, same fields, scratch rev `0ca862c9…` |
| prior-82 knowledge files | — | byte-identical (per-file compare: 0 diffs) |
| README | 190 lines, `6ac43e83…` | 190 lines, changed lines `[38]`, `a451ad16…` |
| token set | 82 unique / 84 occurrences | 83 unique / 85 occurrences; added == {stem}; removed [] |
| K/K (7 primary legs) | — | abi == env == planted, true on all 7; zero extras |
| recheck | — | `05f76b33…` (6.4.0, three-way `cmp`) and `ev_ae5aaee0…` (6.7.0, = landed) |
| probe (drift) | findings=0 at HEAD | findings=0 at the projected commit (both modes) |

Honest-stop branches (HS-1..HS-7, `PL-1/plan.md:262-302`): none triggered on
any leg read or run.

## 4. Attacks / refutations attempted, with verdicts

| attack | verdict |
|---|---|
| "the rev-2 packet still covers the current state" | **SUSTAINED** — rev 4 + the amended token postdate it; I re-measured and wrote rev 3 |
| "the current pair breaks the projection" | **REFUTED** — 83/83, prior-82 identical, README line-neutral, on a fresh clone |
| "the recheck line no longer reproduces" | **REFUTED** — three-way byte-identical envelope at 6.4.0; 6.7.0 id equals the landed envelope |
| "the carriers are hand-assembled / not from the pinned solc" | **REFUTED** — byte-exact recompile of VaultB.opt200 from source + receipted prefix |
| "zero extras is vacuous" | **REFUTED** — 24/16/7 PUSH4 sites censused; non-selector constants (panic, error selectors, CBOR trailer) present and unreported |
| "planted sets ride the probe" | **REFUTED** — independent keccak from the compiled ABIs; mtimes order planted before first envelope on EX-10/EX-05 (46 s / 10 s), EX-04 same-second documented in its own report |
| "the additive token is not the one RV-4 validated" | **REFUTED** — extracted line byte-identical to RV-4's patch new line (`786efbb2…`) |
| "rev 4 resolved the prior citation defects" | **PARTIALLY SUSTAINED** — F3 fixed; F1/F2/F4 + CR-1 Edits 1-3 still present (my sweep: the `optB-…-rerun` set is the only unresolved expansion) |
| "R1 is stale (RV-3's finding)" | **CONFIRMED, independently** — my census: VaultB.nopt has no `4e487b71` PUSH4 immediate and no `3c3332b9` anywhere (0 hits over 3,163 B); the "(both variants)" clause is false |
| "the verdict's pure→view enumeration is complete" | **SUSTAINED (RV-1)** — a second instance (`c85e07b9 stamp()`, CarrierA) exists in EX-02's evidence; corrected in rev 3 |
| "EX-07's compare still says MISMATCH" | **REFUTED (stale at rev 2)** — the landed artifact now reads K/K; my independent run agrees 5/5 |

## 5. Blockers

None. Named gaps for the parent:

- **EX-14 has no seat report** (`seats/EX-14.md` absent; its projection
  artifacts landed, and its projection covered only literal revs A/B/C and the
  *reworded* token — the current pair is rev 4 + additive). Its projections
  remain valid as measurements of superseded revisions; nothing in its artifacts
  is wrong, but it is the one c1 seat whose report is missing.
- **Two literals / two token variants in the tree** — land one of each, paired,
  from the records-drafts copies (verdict debt #15).
- **`SC-2/README-identities.txt` is stale** (pins a non-existent revision
  21,585 B / `5c1818c7…`; the live draft is 22,628 B / `d9004f48…`) — re-pin at
  landing (rule #14).
- The citation-drift probe is C3's instrument; I ran it read-only (no writes to
  `.ufo/gates/citation-drift/`).

## 6. Self-identity (re-derived after the final write, rule #14)

| artifact | bytes | sha256 |
|---|---|---|
| `claims/c1/verdict.md` (rev 3) | 22,141 | `1111ada65b56dbb109fbd205ee0f2341e569c84a868af9a3dead022027233d5d` |
| `seats/VZ-1.md` (this file) | — | sidecar: `claims/c1/VZ-1/evidence2/SHA256SUMS.txt` |

The verdict row is its identity as measured after the verdict's final write.
This report's own hash is **not** self-quoted (any revision of this file voids
it — the r1 D9 class): the sidecar records it for the revision it was written
against. `sha256sum -c claims/c1/VZ-1/evidence2/SHA256SUMS.txt` passes 11/11
over every evidence artifact plus these two files; re-derive the report's row
if this file is revised (rule #14).
