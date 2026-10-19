# C3 verdict — custody receipt v2 (chain convergence, seat VZ-3)

Wave `arc3-loop1-round2` · chain c3 · 2026-10-19 · repo
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · HEAD
`14b1682b1128d2e41085ebc79c9addeb8786d420` (no seat commits; parent integrates).
Instrument under verdict: `.ufo/gates/custody-pair/custody-pair.py`, 889 lines,
39,157 B, sha256
`112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa`, plus
`.ufo/gates/custody-pair/README.md` sha256
`fa484d573b0debb0d2ed134d076cb9593e7c3ee910ad4487d99cb9f3a8239bba`
(both re-hashed by this seat last at 12:27Z; stable since 12:05:19Z; every
receipt the tool writes self-pins that digest).

## Verdict: **VERIFIED** — every frozen component measured and independently reproduced; the two claim words that remain structurally open ("committed", "at the round's commit") are parent-side and are the closing procedure's step 0; no measured result contradicts the claim

Rationale: the frozen claim (`claims-frozen.md:52-64`) requires (a) a v2 receipt
per path carrying sha256 + mtime epoch (UTC-rendered, correctly labeled) + inode
+ ctime, (b) the v1 label defect gone, (c) a live same-content rewrite detected
by inode/ctime movement, (d) v1 receipts still verifiable against the tool's
sha256 fields, (e) the round's own live pre/post pair (exit 0, 5/5) captured by
the tool. Items (a)–(e) are delivered and reproduced by this seat first-hand and
by ≥3 other seats each; the only unlanded clause is "exists as a **committed**
tool" — `git status --porcelain` reads `?? .ufo/gates/custody-pair/` at verdict
time, by the hard rule that only the parent commits. An unrun check has not
passed; nothing run failed.

## Claim components — status and evidence

| # | Component | Status | Evidence |
|---|---|---|---|
| 1 | `.ufo/gates/custody-pair/` ships the tool + README | DELIVERED (uncommitted) | inventory: exactly those two files (pycache residue removed by 12:12Z; see D9); EX-31 seat report §1; `git status` `??` |
| 2 | v2 receipt per path: sha256 + mtime epoch + UTC render + inode + ctime | DELIVERED | VZ-3 live captures T1 (`vz3-T1.txt`, sha `e45790d4…`) and T2 (`live-T2.txt`, sha `73b0fab7…`), each `paths=5/5 exit=0`; VZ-3 comparator vs independent capture: **5 paths × 6 fields all AGREE** (`t2-and-cycle-evidence.txt`); EX-34 epoch round-trip 10/10 (`epoch-roundtrip-table.txt`); RV-12 8-field × 5-path × 6-receipt matrix: 0 diffs |
| 3 | label defect gone | DELIVERED | VZ-3 `TZ=Asia/Tokyo` capture: `MTIME_UTC_RENDER: 2026-10-14T20:53:20Z` (correct UTC) with local render `+09:00` separate; EX-34 7-TZ sweep, RV-11 4-TZ sweep (incl. UTC+14 Kiritimati): UTC renders identical, local renders move as designed; the v1 defect itself is reproduced-as-declared: VZ-3 `verify <round-1 CU-1 stanza> --live` → exit 12, 5× `LABEL-DEFECT`, `SHA256-CONTRACT: 5/5` |
| 4 | live same-content rewrite detected (inode/ctime movement) | DELIVERED (scratch copies only, per the frozen rule) | VZ-3 cycle: rename-over → `REWRITE-DRIFT moved=inode`; in-place + mtime restored → `REWRITE-DRIFT moved=ctime_ns`; control MATCH; all three states sha-identical (`5eaa96da…`) — exit 11. EX-33: 6/6 forms; CR-4: 13/13 forms (restore class `cp -a`/`rsync`/`tar` keep the **inode** — detection is carried by ctime for those forms, a wording refinement recorded below); ns fields load-bearing (whole-second counterpart blind on 6/13, CR-4 `second-precision-window.txt`); EX-32, PL-3, RV-12, RV-14 each reproduced detection on their own fixtures |
| 5 | v1 receipts remain verifiable against the tool's sha256 fields | DELIVERED (field level; exit-code nuance below) | VZ-3: sums-form vs live → `MATCH-V1-PARTIAL 5/5`, `SHA256-CONTRACT 5/5`, exit 0; canonical stanza vs live → exit 12 with 5× `LABEL-DEFECT` and `SHA256-CONTRACT 5/5`; EX-35 cause isolation (time lines stripped → exit 0) + mutated-digest fixtures → CONTENT-DRIFT 10; RV-12/RV-14/CR-4 agree |
| 6 | round's own live pre/post pair (exit 0, 5/5) captured by the tool | DELIVERED (with revision note) | EX-32 authoritative PRE-PAIR `claims/c3/receipts/config-pre-pair-v2.txt` sha `fa9706c6…` 12:04:06Z 5/5 exit 0; EX-31 same-revision pair `capture-pre.txt`/`capture-post.txt` (both embed `112d01dc…`), `verify pre post` → `MATCH 5/5 drift=0 exit 0`; wave-spanning zero drift: EX-32 pre vs EX-31 post vs RV-12 C-final vs VZ-3 T1/T2 — payloads identical, `verify` MATCH 5/5 exit 0 (VZ-3 ran T1↔T2 and EX-32-pre vs T0). Nuance: EX-31's pair is same-instant (both `captured-utc 12:06:26Z`), so the wave-spanning claim rests on the multi-seat payload identity, not on that pair's interval |
| 7 | custody stayed read-only; no drift | DELIVERED | 5/5 sha256 = round-1 pins (`16f496e6…, 38d2a1d0…, 8cbacd48…, 7d2ca28a…, 6c6be761…`) at every capture by ≥7 seats (VZ-3 T0/T1/T2, RV-12 A/B/C, EX-31, EX-32, EX-33, EX-34, EX-37, CR-4); inodes unchanged (11341318/11341316/34530637/25991953/40274); tool source read by VZ-3: `os.lstat` + read-only `open(path,"rb")`, receipt-write guard (`custody-pair.py:189-222,551-570`) |
| 8 | the landing is inert elsewhere (scope discipline) | DELIVERED | census at HEAD with the landed files: PASS 0/0/0/0 (EX-37 `after/`; VZ-3 read its `runs/v10-head.exit` = 0 and `h1h3-head.exit` = 0); citation-drift probe at HEAD: 0 findings in both modes, selftest 13/13; 30 new paths vs the probe's 17 needle files → 0 hard resemblance (EX-38 `after-probe-*.txt`, `resemblance-real.txt`; probe/table digests unchanged from round 1); no scope-bound widening by this chain (census edits are C2's EX-16 — see the cross-chain flag D11) |

## Before → after reconciliation (the discriminating unit)

- **Before (v1 surface, re-measured read-only at HEAD):** sha256-only custody is
  blind to a same-content rewrite — VZ-3's staged pair: `v1-style-sha-before.txt`
  vs `-after.txt` diff **EMPTY** while inode moved (10950841 → 10964595) and
  ctime moved; CR-4: v1 blind on **13/13** attack forms; the canonical pre-pair
  prints local (−03) renders under `MTIME_UTC` (3 h off; VZ-3 independently
  renders epoch `1792011200` → `2026-10-14T20:53:20Z`).
- **After (v2, revision `112d01dc…`):** the same class is caught — VZ-3
  `REWRITE-DRIFT exit 11` via `inode` (rename class) or `ctime_ns` (in-place,
  mtime-restored class) with the sha contract still agreeing 3/3; label renders
  correct and TZ-independent; v1 digests verifiable.
- **Headline number:** same-content rewrite visibility v1 → v2 = **0/13 → 13/13**
  attack forms (CR-4 matrix; EX-33 6/6; VZ-3 2/2 forms; RV-12 A1/A2; PL-3; EX-40).
  The detection is *not* a content side effect: in every row the digest stays
  equal — the identity pins carry it.
- **Wording refinement the records must take (CR-4 §2, corroborated by EX-33
  forms where the inode is preserved):** the frozen parenthetical
  "(inode/ctime movement)" is right as a disjunction but must not be read as an
  inode pin — `cp -a`/`cp -p`/`rsync --inplace`/`tar`/in-place reflink preserve
  the inode, so **ctime(+ns)** is the load-bearing pin there.
- **Wording ruling for "v1 receipts remain verifiable" (EX-32 F4 / EX-35 A7 /
  RV-12 A7 asked VZ-3 to adjudicate):** satisfied at the field level the claim
  names — `SHA256-CONTRACT: 5/5` is reported for all three v1 shapes and planted
  digest drift is caught (exit 10). It is explicitly **not** an exit-0 promise:
  a time-carrying v1 receipt exits 12 by design because it carries the very
  label defect the tool reports. Both numbers (sums → 0; stanza/pipe → 12) are
  measured and must be quoted together in any record sentence.

## Named debt (measured residuals; none voids the claim)

1. **D1 — capture atomicity (TOCTOU).** `capture_path` = `lstat` then a second
   path-based open for sha256; CR-4 measured 2/300 internally-inconsistent
   captures against a live writer (`toctou-measurement.py`); patch text
   `CR-4/proposed-capture-atomicity.patch.md`. Harm class: misclassification,
   not an undetected tamper.
2. **D2 — unreadable-path fail-open.** An exists-but-EACCES path records
   `exists=no` + `STAT-ERROR`, and `verify` of a both-sides-nonexistent path
   reads **MATCH exit 0** (EX-40 `real-tool-silent-match-probe.txt`); a
   `verify --live` run against an unreadable candidate dies with a traceback
   (exit 1, outside the declared map; EX-40 `real-tool-unreadable.txt.traceback`).
   Reproduced first-hand by VZ-3 (`claims/c3/VZ-3/evidence/eacces-repro.txt`:
   capture `PARTIAL paths=0/1 exit=13`; `verify --live` → `MATCH compared=0/11
   exit=0`; chmod-000 candidate → `PermissionError` at `custody-pair.py:219`
   via `:168`, exit 1). Patch text `EX-40/proposed-edge-classes.patch`.
3. **D3 — partial-reference coverage.** `verify` only compares paths present in
   receipt A: a 1-of-5 receipt vs live reads exit 0 (`1/1`), the other four
   custody paths unexamined — the H1 shape (EX-35 A5); patch text
   `EX-35/proposed-v1-verify-adapter.patch.md` (`--require-paths N`).
4. **D4 — receipt self-authentication.** `verify` never reads
   `<receipt_a>.sha256` and cannot authenticate the receipt it is given: a
   tampered receipt whose fields are made to match a rewritten file reads
   MATCH exit 0 (EX-33 §4.1 case J; CR-4 attack 6 — forged receipt plus
   regenerated sidecar; PL-3 A6b). Audit guidance: check the sidecar out of
   band or verify against a committed capture; both EX-33 and CR-4 propose the
   same fail-closed sidecar check.
5. **D5 — out-of-band/root class (threat-model boundary, not a defect).**
   CR-4 attack 4: block-level erasure of an ext4 image left inode, ctime, mtime,
   size and sha256 state-identical — no field-pinning receipt can see it; ctime
   itself is forgeable at the metadata layer (`debugfs set_inode_field`, CR-4
   attack 5). Stated scope: the tool is a **tripwire for attribution, not an
   integrity control** against an actor sharing its trust domain (root/raw
   device/receipt store). Records should carry this sentence or the equivalent.
6. **D6 — `selftest --scratch <missing dir>`** dies with a raw
   `FileNotFoundError` traceback, exit 1, outside the declared map (EX-33 §5,
   EX-34, RV-12; two patch texts propose the USAGE-class fix:
   `EX-34/proposed-scratch-dir-guard.patch.md`,
   `RV-12/proposed-scratch-mkdir.patch.md`).
7. **D7 — write-guard hardlink evasion.** `--out` resolved-path check
   (`custody-pair.py:564`) is evaded by a hardlink alias to a guarded file
   (RV-11 hardlink-guard, scratch-only proof). The guard is a self-harm guard,
   not a security boundary (an actor able to create the alias can already write
   the file); named as precision, not severity.
8. **D8 — revision churn and stale embedded identities (C1 rule-#14 surface).**
   Observed revisions: `9aad4c5a…` (12:03:47) → `4862f642…` (12:04:00) →
   `72d5231f…` (12:04:40) → `b10ad1c8…` (12:04:50) → one further mid-edit
   revision (≥12:05:10, RV-13) → **`112d01dc…`** (12:05:19, landed; stable to
   verdict time). Receipts that embed superseded shas: EX-32's authoritative
   pre-pair (`4862f642…` — the one the claim's "round pre-pair" most plausibly
   names), RV-12 A/B (`72d5231f…`), EX-34's epoch table copy (`b10ad1c8…`).
   Payloads are byte-identical across revisions (RV-12 A vs C-final; EX-32 F5),
   so comparability holds; the parent should annotate with the revision mapping
   or re-capture (PL-3 blocker 2). The landed revision's identity is stable and
   self-pinned (EX-31 `identity-rederivation.out`; RV-14 re-hash after every
   run). The `b10ad1c8…`/unhashed mid-edit revisions were transiently broken
   (`KeyError: 'sha_agree'`, selftest DIRTY 6/15; EX-32 F2, RV-12 A5, RV-13
   deterministic reconstruction `tools/no-shaagree.py`, EX-34) — not
   reproducible on the landed revision; every cited run names its revision.
9. **D9 — pycache residues.** `.ufo/gates/custody-pair/__pycache__/` existed
   12:02–12:12Z (created by verifier seats importing the module; gone at
   verdict time — inventory re-checked) and `.ufo/gates/__pycache__/
   c1-census-v10.cpython-314.pyc` (foreign, untracked) still exists — exclude
   both from the wave-artifacts commit (EX-31 §2, PL-3 blocker 1, RV-14 note).
10. **D10 — registry-row duplication and placement.** PL-3 and EX-36 each author
    a `custody-pair` row, with overlapping but non-identical texts (EX-36 also
    rewrites the registry preamble); RV-14 measured 29/29 of EX-36's clauses as
    true and flags the wording precision (state the real 0/10/11/12/13/2/3 map,
    or say nothing). The parent must land **one merged row**, not both (round-1
    precedent). Naming deviation for the parent to adjudicate: EX-32 wrote the
    chain-level `claims/c3/receipts/` (outside the per-seat convention; PL-3
    blocker 5) — kept, but the records should reference it as measured.
11. **D11 — cross-chain flag (not C3's, carried because a C3 seat measured it).**
    SC-4 §3 rev-3: at the then-newest census revision the **untouched base tree
    FAILs** `G2 positive-assertion guard: SUSPECT` (SKILL.md 0 loci against a
    1/file floor) while the drafted records text adds zero loci — i.e. an
    instrument-state red at HEAD, C2-owned. The census churned mid-wave
    (`6f1d19ff…` → `82fb807e…` → `09e270c2…`; EX-37 §2a, SC-4 §3). The parent
    must re-run the census at the records commit and not land the round section
    as if that red were green.

## Attacks attempted this round (with verdicts) — chain roll-up

| Attack class | Seats | Result |
|---|---|---|
| Same-content rewrite, in-place / mtime-restored / rename / hardlink / delete+recreate / same-second | VZ-3 (2 forms), EX-31 (2), EX-32 (2), EX-33 (6), PL-3 (3), RV-12 (2), RV-14 (2), EX-40 (edges) | **all detected**, exit 11, sha contract intact |
| Restore-tool class (`cp -a`/`cp -p`/`rsync`/`tar`/reflink) | CR-4 (13-form matrix) | **all detected**; inode preserved in most forms → ctime load-bearing |
| Whole-second granularity boundary | EX-33 `--sec`, CR-4 EXP1 | blind at seconds, **caught at ns** → ns fields load-bearing (declared, not hidden) |
| v1 receipt poisoning / label-defect regression | VZ-3, EX-31, EX-32, EX-33, EX-35, CR-4, RV-12, RV-14 | **surfaced as declared** (exit 12, named LABEL-DEFECT, sha 5/5); stripped-time fixture → exit 0 |
| Comparator vacuity (does anything ever fire?) | EX-31 A5/A6, EX-32, RV-11 sabotage S1–S3, CR-4 #10 | **selftest has teeth**: S1 neutering rewrite pins → DIRTY 2 fails; S2 utc→localtime → TZ case fails; S3 neutering sha compare → content cases fail; each exit 3. Mutated digests in v1/v2 receipts → CONTENT-DRIFT |
| Receipt tampering / forgery | EX-33 case J, CR-4 #6, PL-3 A6b | **tamper-to-match passes** → scope finding D4 (sidecar not an anchor) |
| Unreadable/blocked paths, absent, extra, type-swaps | EX-40 matrix, RV-14 #9/#10, CR-4 #7 | absent→13, symlink/type→declared, **EACCES fail-open** → D2 |
| Write-guard evasion | RV-11, EX-31 S15, RV-14 #12 | resolved-path guard holds for direct aims; **hardlink alias evades** → D7 |
| Out-of-band erasure / ctime forgery | CR-4 #4/#5 | **defeats any field-pinning receipt** — named threat-model boundary D5 |
| TOCTOU capture race | CR-4 #9 | 2/300 internally inconsistent receipts; no silent-bypass tuple measured → D1 |
| Identity staleness (C1 rule-#14 shape) | EX-32 F1, RV-12 A8, EX-37 stability watcher, PL-3 §1 | receipts self-pin the tool sha; stale-quote hazard named → D8; EX-37's early sample caught the file mid-write (stability gate needed) |

## Seat delivery status at verdict time (19-poll tally, 12:00–12:19Z)

- **C3 reports landed: 17/17** — PL-3, EX-31, EX-32, EX-33, EX-34, EX-35, EX-36,
  EX-37, EX-38 (landed 12:17:57Z, the last), EX-39, EX-40, SC-4, CR-4, RV-11,
  RV-12, RV-13, RV-14. The poller caught the wave from 0/17 (check 1, 12:00:37Z)
  to 17/17 across checks 1–19; no C3 seat is undelivered.
- Cross seats: CU-1 (round-1 custody receipt author) is represented via the
  round-1 tree; its round-2 report notes the same post-pair absence RV-12 names.

## VZ-3's own verification runs (this seat; artifacts in `claims/c3/VZ-3/`)

| Run | Command (abridged) | Result |
|---|---|---|
| reference capture | `vz3-independent-capture.sh <5 paths>` (stat+sha only) | `independent-capture-T0.txt`; devin epoch `1792011200` → `2026-10-14T20:53:20Z`, local `17:53:20` (the defect arithmetic, my own derivation) |
| selftest | `custody-pair.py selftest` | `CLEAN cases=15 passed=15 failed=0 exit=0` |
| live T1/T2 | `capture --out …` | both `paths=5/5 exit=0`; T1↔T2 `MATCH 5/5 drift=0 exit=0`; T2 vs T0 independent values 6/6 × 5 AGREE |
| label under TZ | `TZ=Asia/Tokyo capture --out -` | `MTIME_UTC_RENDER 2026-10-14T20:53:20Z` (unchanged), local `+09:00` separate |
| v1 stanza | `verify <round-1 config-pre-pair.txt> --live` | exit 12, 5× `LABEL-DEFECT`, `SHA256-CONTRACT 5/5` |
| v1 sums | `verify <sums-form> --live` | `MATCH-V1-PARTIAL 5/5`, exit 0 |
| rewrite cycle | `/var/tmp/vz3-scratch/cycle` (3-fixture, sha-equal rewrites) | `REWRITE-DRIFT moved=inode` / `moved=ctime_ns`, control `MATCH`, exit 11 |
| v1 blindness staging | same-content rewrites, sha256sum re-capture | diff EMPTY (blind) while inode/ctime moved |
| receipt cross-checks | `vz3-compare-receipt-vs-independent.py` vs EX-31 pre/post, EX-32 authoritative | all AGREE 6/6 × 5; EX-32 payload byte-identical to EX-31 capture-pre |

## Closing procedure (what flips the remaining words to green)

1. **Commit** `.ufo/gates/custody-pair/{custody-pair.py,README.md}` exactly
   (exclude `__pycache__`, `.ufo/gates/__pycache__`, and honour the standing
   `.ufo/waves/arc2-loop1-round10/C3.md` pre-existing dirty path — leave it).
   That alone closes "committed"; no tool edit should follow the receipts'
   self-pinned identity (EX-31 blocker 1).
2. **Land one merged registry row** (PL-3 + EX-36; keep the v1 exit-split and
   the real exit map; RV-14's 29/29 measurement covers EX-36's clause set).
3. **Records**: use SC-4's drafted C3 section + carried-debt lines (D1/D2/D4/D5
   at minimum), keep it pin-free per SC-4 §"pin-free discipline", and **re-run
   the census at the records commit after C2's EX-16 settles** (D11; EX-37's
   `runs/` and SC-4's simulation are the pre-flight).
4. **Optional but recommended**: re-capture the round pre-pair on the landed
   revision (`112d01dc…`), or annotate EX-32's receipt with the revision mapping
   (D8); and when a post-pair lands, run
   `verify claims/c3/receipts/config-pre-pair-v2.txt <post>` — expected
   `MATCH 5/5 drift=0 exit 0` (RV-12 §5 could not run the post half; VZ-3's T2
   and RV-12's C-final are the current stand-ins).

## Verdict basis note (evidence discipline)

Every claim component above cites a file plus a command result or a digest;
unrun checks are labelled as such (the "commit" clause; the post-pair trip
wire; CR-4's root-only snapshot-revert instance). No seat report was treated as
evidence without at least one item of first-hand measurement by this seat
against the landed bytes — including the tool's own selftest, the label
arithmetic, both v1 shapes, and both rewrite classes.
