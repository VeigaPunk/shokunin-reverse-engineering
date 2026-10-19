# arc3-loop1-round1 — wave summary (VZ-4, wave-integrator)

Seat VZ-4 | chain cross | wave arc3-loop1-round1, 2026-10-19.
HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab` (immobile at every sample; seats do
not commit). Wave window opened ~06:49 local (wave dir created 06:49; `claims-frozen.md`
06:52). This seat's writes: this file, `claims/cross/VZ-4/*` (poll log, census script,
independent verification captures), and `seats/VZ-4.md`. No git mutations; no custody
path touched (sha256-capture only); no install; scratch under this seat's artifact dir
(host `/tmp` is EDQUOT-broken — see §5).

Method: 25×60 s polls of `seats/` (log `claims/cross/VZ-4/poll-log.txt`), mechanical
roster census (`claims/cross/VZ-4/roster-census.sh`), plus VZ-4's own first-hand
re-verification of the two landed real-target edits and the custody receipt (§3, §4).

## 1. Seats delivered vs the frozen roster

Roster source: `claims-frozen.md:90-98` (64 seats; enumerated per chain). Census
command: `bash claims/cross/VZ-4/roster-census.sh`.

- **Delivered: 51/64** at 07:20:49 (`claims/cross/VZ-4/census-at-write.txt`).
- C1 24/26 — undelivered: EX-03 (source only, landed 07:11, no report),
  EX-14 (manifest churning, no report).
- C2 15/20 — undelivered: EX-17, EX-25, SC-5, RV-5, VZ-2.
- C3 9/14 — undelivered: EX-27, EX-28 (edit landed, report pending), EX-31,
  RV-9, VZ-3.
- Cross 3/4 — VZ-4 (this seat; report lands after this summary).
- Closing census (check 25, 07:25): `[[updated in §1a]]`.

Per the r5 counting lesson, the count above is against the frozen roster artifact,
not against another round's roster. No stray seat files (census §"stray" = none).

## 2. Per-chain verdicts

### C1 — coverage (owned): EVM real-bytecode leg — VERIFIED (with named debts)

Verdict from the VZ-1 packet (`seats/VZ-1.md`, mirrored `claims/c1/verdict.md`,
sha256 `75cc664a…`), corroborated by VZ-4's reads of the underlying artifacts:

- Real solc 0.8.37 compiled on-host (wave-isolated prefix, EX-02 receipt; tarball
  sha256 `0e1a1ab6…`); **ambient global solc pre-existed** — the receipted isolated
  copy is what keeps provenance falsifiable (EX-02 §6).
- K/K recovery on real dispatchers, zero missing/zero extra, `dispatch:"abi"`
  throughout: Rv2Token 5/5, KdxToken 6/6, Smoke 5/5, plus VZ-1's own compile+probe
  of EX-03's landed source 9/9 (`ev_92b7e2fc…`). RV-2 re-derived evidence ids
  byte-exactly on both pins (6.4.0/6.7.0); RV-1 recomputed selector sets with an
  independent from-spec keccak (MATCH on all three landed sets).
- After-state measured at tree level twice (VZ-1 E7): recipe A 82/82, missing [],
  dangling [], 13/13 on the applied entry+map-token patch.
- Named debts (VZ-1 D4/D5/D9 + CR-2 F1–F5): the entry patch churned mid-wave
  (three applied identities 8,598/8,316/9,513 B) and its self-hash + `recheck:`
  line are stale (the recheck line fails as written — EDQUOT-dependent); the map
  row prose still says "synthetic dispatcher" after the token edit; RV-1's
  carrier-vs-decoded-digest conflation (labeling, cosmetic).
- **Residual owed**: command A *at the records commit* (the 82/82 end-state is
  proven tree-level, not yet at a commit).

### C2 — operability (fleet): citation-drift frozen-run guard — VERIFIED

No VZ-2 packet landed at close; verdict below is VZ-4's own first-hand after-state
verification of the landed edit plus the chain's reviewer evidence.

- Landed by EX-16 (the only authorized writer): probe `e2665074…` (before
  `3067621a…`), expected.json `ff47bfd6…` (before `4e28ba90…`), pointer-table.json
  byte-stable `738b3a56…` (the pinned digest). Probe+expected are byte-identical to
  PL-2's independently validated prototype.
- **VZ-4's own runs** (`claims/cross/VZ-4/c2-after-verify.txt`): selftest
  **13/13 exit 0** (new cases `table_tampered`, `table_absent`, both exit 2);
  clean HEAD run `reported findings=0 exit=0`; my own emptied-table fixture →
  `pointer_table_tampered` exit 2; absent table → `pointer_table_unreadable`
  exit 2. All four checks reproduce the claim's declared classes.
- EX-16's matrix additionally covers: whitespace-append → exit 2 (byte-level pin),
  unpinned expected → exit 2 (`pointer_table_unpinned`), malformed JSON → exit 2,
  frozen rev 679af5d → 16 findings with probe/strict rc 0/1 (probe kind preserved).
- Behavior change to name: custom `--table` + committed expected now exits 2
  (RV-8's D1 design; r10-style experiment recipes are affected; the escape hatch is
  custom table + custom pinned expected → exit 0, EX-16 case I).
- Outstanding: `SKILL.md:371` registry-row patch (EX-20, re-verified by SC-4 and
  EX-16) still un-applied — the claim's "row states the guard semantics" clause
  depends on the parent landing it.

### C3 — freshness (fleet): census scope-table re-key at HEAD — VERIFIED (disposition)

No VZ-3 packet landed at close; verdict below is VZ-4's own first-hand verification
plus the chain's evidence.

- Census at HEAD is **PASS 0/0/0/0 exit 0** both before and after EX-28's edit; the
  verdict output is byte-identical (`3b677b8e…`, 5 independent captures pre-edit).
- EX-28 landed a header disposition + one marker-line re-key + a new G18 assertion
  (`marker_line ∈ [start, end]` for every DATED row). **VZ-4 independently confirmed
  the claimed latent defect**: the committed row `("PROVINCE.md", 45, 62, "DATED", 40,
  …)` declared marker line 40 — the table-intro line, outside its own range — while
  G15 only checked that line 40 carried the marker. Re-keyed to 45 (own dated receipt
  text). CR-5's creep-diff audit on the landed edit (`scope-diff.py`): rows 20→20,
  0 added/removed, 1 marker re-key, **CREEP FLAGS: []**.
- Reconciliation of the two framings: EX-26/PL-3 measured "nothing to re-key at
  HEAD" at the *verdict* level (PASS, 0 stale) — that stands; EX-28's re-key is at
  the *marker-line* level and does not change the verdict or the SCOPE ranges. The
  frozen claim's "FAIL undeclared=2 → PASS" before→after does **not** describe HEAD
  (it describes v9 at the r4 tree); the discriminating record is the disposition
  itself, not a verdict flip.
- Outstanding: SC-6's disposition draft (`claims/c3/SC-6/e22-disposition.draft.md`)
  and EX-28's report; the census output is unchanged so command A is unaffected.

## 3. Custody outcome

- **Pre-pair**: CU-1 `claims/cross/receipts/config-pre-pair.txt`, 5/5 paths,
  capture 2026-10-19T09:57:18Z at HEAD `e845c2b`; self-hash `b8ed1936…`
  (VZ-4 re-verified: match). Genuinely pre-install: the solc prefix dir post-dates
  the receipt by 7.4 s.
- **VZ-4's independent recompute** at 10:03:33Z: all five paths byte-identical to
  the pre-pair — zero drift across the install/probe window (sha256s in §6).
- Corroborations: EX-01 (three hash implementations, 5/5), EX-10 (stanza-level pin
  `rea-agents@6.7.0` + file hash), EX-15 (T0/T1 pair + filesystem mtime/ctime
  argument), VZ-1 E5 (~07:10).
- Findings: (a) CU-1 metadata labels local (-03) times as `MTIME_UTC` — label
  defect, digests unaffected (EX-01 A4, EX-10); (b) sha256-only custody is blind to
  a same-content rewrite — mitigated by inode/ctime pins in the metadata receipt
  (CU-1 attack 3, measured); (c) custody-set scope note: sidecars/siblings receive
  live writes and are outside the frozen 5 (adjacent baselines captured).
- **Post-pair: PENDING** — CU-1's report is a draft ("post-pair section pending")
  as of 07:20. The wave's custody close is CU-1's artifact; VZ-4's recompute stands
  as an interim post-install zero-drift check.

## 4. Parent-facing admission-recommendation inputs

1. **C1** — claim verified in substance (install receipt; K≥3 real-solc carriers,
   K/K with zero extras; tree-level 82/82). To admit: land EX-12's entry patch (with
   CR-2's F1 recheck-line fix + F2 identity re-derivation), EX-13's map token
   (line-neutral, verified), EX-02's receipt patch; run command A at the records
   commit. Do not inherit VZ-1's D4/D5/D9 into the record silently.
2. **C2** — claim verified (VZ-4's independent after-state). To admit: commit the
   landed gate diff (EX-16's two files), land EX-20's SKILL.md row patch, exclude
   the untracked `__pycache__` dirs from the commit. Note the D1 behavior change
   for custom-table recipes in the round record.
3. **C3** — claim verified as a disposition: the E22 finding does not reproduce at
   HEAD; one latent marker-line defect found, re-keyed, G18 added, creep audit
   clean. To admit: land SC-6's disposition draft / EX-28's header (already in the
   worktree) and record the PASS→PASS honest shape rather than a manufactured flip.
4. **Wave-level**: the frozen roster/items assertion held (64 = 64; no strays); the
   undelivered seats are named in §1 and per the counting lesson are not
   backfilled; the two authorized real-target writers both landed and were
   independently re-verified; the two VZ chain packets (VZ-2/VZ-3) are the
   named process gap — their function was covered by VZ-4's first-hand
   re-verification of both landed edits.
5. **Environment (record, don't absorb)**: `/tmp` EDQUOT is fleet-wide and
   pre-existing (12.1 G per-UID quota saturated; 24 stale pre-wave dirs ≈ 6.9 G);
   147 zero-byte scratch casualties; seats relocated to `/dev/shm` or in-repo
   scratch. The recipe-A invocation form in SCORECARD.md is a trap
   (`REV=HEAD python3 - "$REV"` expands before assignment — EX-11, CN-1).

## 5. Attacks / refutations run by this seat (verdicts)

- EX-14 manifest re-check (`sha256sum -c`): 6 entries FAILED → **refuted as a
  defect**: all 6 mtimes post-date the 07:04:54 snapshot (live-wave churn, not
  corruption; manifest is a rolling snapshot, not frozen).
- CU-1 pre-pair self-hash: recomputed → match (`b8ed1936…`).
- C2 after-state: four independent runs (above) → declared classes reproduce.
- C3 after-state: my run + before/after output diff (IDENTICAL) + EX-28's latent
  row re-derived from the committed file via `git show HEAD:…` → confirmed.
- CR-5 creep audit executed by VZ-4 on the landed edit → 0 flags.
- `/tmp` writability probed → EDQUOT on 1-byte writes while 0-byte creates
  succeed (space quota, not inodes) — matches EX-15's mechanism.

## 6. Custody sha256s (VZ-4 capture, 2026-10-19T10:03:33Z, = pre-pair)

```
16f496e663d0c91252d17dcb8094d141a8feb713466e2fb4f14267bf744263a4  ~/.config/devin/mcp_config.json
38d2a1d0e5e67da09266c4611b34ab32b394371063f307c5104b6cb0de1b926b  ~/.omp/agent/mcp.json
8cbacd48ab85ea86e122bae102d8ee63e2fd3181aa551603b3923b912573c38d  ~/.kimi-code/config.toml
7d2ca28a245c44a1f5458921f0dff54823aa1e74ffa02eac2013b486e6a26598  ~/.bashrc
6c6be761d3b199c964c95e724d7cdc9f4f902e0c3bdd6a532361b20a53db4f30  ~/.profile
```

## 7. Gaps named (not blocked on)

- VZ-2, VZ-3 packets; CU-1 post-pair; EX-28 report; EX-17/EX-25/SC-5/RV-5 (C2),
  EX-27/EX-31/RV-9 (C3), EX-03/EX-14 reports (C1).
- Untracked hygiene items for the integration commit: `.ufo/gates/__pycache__/`
  and `.ufo/gates/citation-drift/__pycache__/` (both created in-wave; not
  gitignored).
- `[[updated in §1a]]` placeholder resolved below at close.
