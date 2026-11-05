# Round 96 — lesson: a kill rule must reach the gates it asserts, and a receipt must bind every field it claims (and the revision it names must be the bytes it measured)

Declaration `e4d1f7de9deae83e6d5f78d2d7f0157196002af0` (`plans/round-96-claims.md`,
`.ufo/waves/round-96/claims.json`, pins `.ufo/waves/round-96/pins.sha256`); base
`0ea695e826f2dca53dd55ac0bafead93de26b173`. Disclosed instrument supersession
`3baac2ef4b9b2830d299125b8184ca06d9e6584d` (see `claims.json` `instrument_supersessions`).
Wave `r96-w1` (twelve seats, one v1 wave, band 8–16; `.ufo/waves/round-96/w1/`). Claims:
R96-C1 (calibration, measured) and R96-C2 (depth, measured). Measured revisions: see `## Measured`.

## Motive

Round 95 closed with two verified claims and named limits. The round-95 kill rule killed five of
ten mutants (M95-h): its checks never called the counter's `main()` and never ran the probe, so
the writer fsync, the forced self-verification, the fail-closed exit, the revision binding and the
probe verdict survived. Its successor counter left six receipt fields unbound and let a green exit
happen without any receipt (M95-g). The probe's own `--json-out` followed a planted symlink (M95-i).
Round 96 takes those three as its claim and the craft row for the class as its second.

## Gate

Source opened this round (CORPUS.md rule 1). Access date 2026-11-05 for each.

| row | source | access date | bytes / sha256 / measurement | located quote (≤25 words) | used for |
|---|---|---|---|---|---|
| S321 (new, admitted) | `/usr/bin/printf` — host binary, little-endian x86-64 ELF (own-work measurement; no network fetch) | 2026-11-05 | 76 088 B; sha256 `b2265abe04a2c237be085f12c14d3c70969f34ab3370a56f399727e4b38374d7`; upx 5.2.0 packable; packed sha256 `95f2beb30d459f3080a542d29430e91f8b55664efb5c7920c8c3fa880672adb6` | `fresh-source2 repaired 2 of 2; far-refused 2 of 2; intact 1 of 1 met True exit 0` (`.ufo/waves/round-96/pre/s321-fresh-source2-at-base.json`) | the held-out arm's second fresh source: closes the round-93 carried limit "the fresh-pack arm has one source" |

Independent re-measurement of S321 (`w1/ScoutS321.md`, `w1/ExecFreshSource.md`): the digest, the
packed digest, `deterministic true`, `collides_public_packed false` and the label reproduce from a
fresh clone; a `--source-sha` of all zeros exits 2 (`fresh source sha256 drift`) and does not score.

**Admit (S321):** the row's `teaches` is the measured property (source diversity of the held-out
arm, pinned by digest, re-measurable), the anchor is the digest plus the committed receipt, and the
knowledge entry cites it.

**Reject (not admitted as a row):** `/usr/bin/head` (sha256 `313bf1f0c296d63fa9534394e22a502cfe29d9fe9e110c5b45f3c070b9ddf3e1`)
was measured by the same instrument by ExecFreshSource and also repairs 2 of 2, refuses 2 of 2 and
is intact 1 of 1 (`w1/fs2-head-repro.json`). It adds no property S321 does not carry, so it is not a
row. Flip condition: a row becomes warranted when a cited claim needs a third distinct source.

Row changes (CORPUS.md rule 2): S321 appended (`mined`, opened 2026-11-05, recheck `on-release`,
used-by the knowledge entry). No existing row edited. Registry rows 225 → 226.

Assimilation: `Assimilation: none` (`merge/kaidoku/` and `considerthese/` are absent in this lane).

## Corrections (append-only; the round-95 text is not rewritten)

- **R95-VD-2 (count without a command).** The round-95 lesson's `## Gate` says the `open(2)` page
  "states the flag five times". Counting command on the committed fetch, after tag stripping:
  `sed -e 's/<[^>]*>//g' .ufo/waves/round-95/l1/scores/s320-open2-fetch1.html | grep -o 'O_NOFOLLOW' | wc -l`
  → **6** (flag list, description, the `O_PATH` carve-out, the `O_PATH` symlink note, the ELOOP entry,
  the versions list). The round-95 text stands as filed; this line is the correction.
- **R95-VD-1 (receipts at the landing revision)** is discharged in `## Measured` below: the after-side
  receipts name the landing revision and were measured on a clean committed tree.
- **R95-VD-3 (round-95 instruments without registry rows)** is discharged by the registry rows added to
  `SKILL.md` this round (four round-95 instruments, six round-96 instruments).

## Mistakes

Each row: class · evidence pointer · captured-by · fix.

- **M96-a · a receipt named a revision whose bytes it did not measure (own, this round).** The honest
  run `honest-pos.json` was measured on the uncommitted supersession bytes but its `revision` field
  names the declaration `e4d1f7de`. CriticC1 finding 3 caught it: the receipt's `counter_sha256`
  equals the `3baac2ef` bytes, not `git show e4d1f7de:tools/round-96/stop-boundary-repair-battery-v6.py`.
  Class: attribution / landing. Captured-by: none — v6's `head` check is self-consistent (`head ==
  revision == rev_full`), and a self-consistent lie passes it. Fix: the after-side receipts are re-measured on a
  clean committed tree (`## Measured`); the declaration-time receipts are kept as evidence and named in
  the knowledge entry's provenance paragraph, not cited as clean-tree measurements. Byte binding is
  routed to round 97 (`git cat-file blob <rev>:<path>`, as `kumitate-shokunin/scripts/receipt-bind.mjs`).
- **M96-b · the honest run failed closed on its own revision (own).** v6's `resolve_rev` accepted only
  hex, so `--rev HEAD` returned `None`, the receipt's `head` was `None`, and `head-not-bound` turned the
  green verdict into exit 1. Red evidence committed: `.ufo/waves/round-96/l1/scores/honest-pos-red-head-not-bound.{json,stdout,stderr,rc}`.
  Captured-by: the fail-closed gate (not the frozen predicate). Fix: symbolic names accepted (`HEAD`
  resolves; `HEAD ` with a space does not); the fix is green in `honest-pos.json`. Shown able to fail: the red file.
- **M96-c · kill-rule harness machinery crashed five times before the first green (own).** Missing
  work directory (`FileNotFoundError` in `mkstemp`), missing copy dependencies (the round-92 battery
  import closure), a selftest convention split (the counter takes `--selftest --work`, the agreement
  takes `--selftest <dir>`), fixtures that baked the superseded v6 `counter_sha256`, and an agreement
  forgery leg on the wrong world revision. Captured-by: none before the freeze; each crash was the
  signal. Fix: the supersession commit, with the kill-rule run repeated after each fix (receipts `kr-at-decl{2..6}` in scratch, not evidence).
- **M96-d · a count double-counted (own).** The first green-arm label read `forgeries refused 14 of 10`
  because `K-forgeries` already scores the four round-95 forgeries and the sum added the agreement rows
  again. Class: number-drift. Captured-by: the label's own arithmetic (`forgeries refused N of 10`, N≠10 → met false). Fix: `forgeries = K-forgeries.refused`.
- **M96-e · the frozen 10-mutant table cannot see a `--rev ≠ HEAD` mutant (CriticC1 finding 4).** A
  mutant that sets `receipt["head"] = resolve_rev(root, args.rev)` survives the frozen rule; only a
  non-HEAD revision scenario kills it (the honest counter is correct: `honest exit 1 head-not-bound`
  versus `M11 exit 0` in `w1/CriticC1/attacks/results/rev-old-scenario.json`). Class: survivor. Captured-by:
  none under the frozen rule. Fix: routed to round 97 as a frozen-table amendment.
- **M96-f · `met_target` absent or null verifies (ReviewerInstruments H-1; CriticC1 A5/A6).** `verify_receipt`
  checks `met_target is True` and `is False` only, so a receipt without the field verifies clean and
  `main` exits 0 with `met None`. Class: unbound field (the M95-g class, a seventh instance). Captured-by:
  none; no fixture or mutant covers it. Fix: routed to round 97 (`met-not-typed`, a seventh forgery, and
  an M11 hard-coding the None-pass). Not fixed here: changing v6 after the scoring would change the rule the claim was scored under.
- **M96-g · a misspecified kill route (CriticC1 finding 8).** `mutants.json` declares M6 killed by
  `K-dmain shortrev`; the measured receipt shows K-selftest kills it first (the v6 selftest carries the
  wrong-revision case). The mutant is killed either way. Class: attribution. Captured-by: the receipt's
  per-check rows. Fix: the knowledge entry records the measured attribution, not the declared one.
- **M96-h · the probe's own write escape is closed by no frozen check (MutationC1 N7).** Reverting
  `symlink-probe-v2`'s receipt write to `open("w")` leaves the full frozen score green. Class: survivor.
  Captured-by: none; the public probe leg catches it (`c1-probe-writer-unbound-at-base.json` before, the v2 leg
  after), but that leg is outside the frozen label. Fix: routed to round 97 as a planted-link leg in K-probe on the v6 writer.
- **M96-j · the frozen command is cwd-dependent (MutationC1 incidental 1).** The relative `--honest-dir`
  makes the regression leg read nothing outside the tree root. Class: attribution / cwd. Captured-by: the rule's
  own red leg (it failed closed). Fix: routed to round 97 (absolute join from `--root`).
- **Misroot sweep.** `git -C /home/vgpnk/Projects/shokunin status --porcelain` is run before the report;
  its result is recorded in the report's work list (no seat wrote to the fleet root in this round).

## Measured

(Filled at the bookkeeping commit after the landing commit, from receipts measured at a clean committed
tree. See `## Wave r96-w1 — seat results` for the seat re-measurements.)

## Mutation (MutationC1: fresh mutants N1–N10, `w1/MutationC1/mutants.md`)

The baseline (pristine bytes) is green: kill rule exit 0, label `mutants killed 10 of 10; forgeries refused 10 of 10; negctl refused 3 of 3; probe consistent 1 of 1; honest accepted 1 of 1`, `identity_not_killed true`.

| mutant | edit | in-suite result | reading |
|---|---|---|---|
| N1 | `resolve_rev` back to hex-only | killed (rule exit 1; K-dmain `pos` red) | killed through the red honest arm |
| N2 | the bool clause dropped from `count_problems` | **survived** (rule exit 0) | named limit 6 |
| N3 | `met_target False` direction dropped | killed (selftest 1; rule 1) | |
| N4 | `receipt["head"]` dropped from `main` | killed (K-dmain `pos` exit 1, `head-not-bound`) | selftest blind (no head-binding case) |
| N5 | `os.fsync` restored in `c_fsync` before counting (meta) | killed, self-observed (`fsync_calls=0`) | the harness saw itself |
| N6 | `identity_not_killed = True` unconditionally (meta) | survived in-suite; observed only by a crafted probe | the identity clause is unobserved by the pristine run |
| N7 | `symlink-probe-v2` writer reverted to `open(w)` | **survived** (rule exit 0) | **M96-h, new: the probe's own write escape is closed by the public probe leg only, not by any frozen check** |
| N8 | `c_probe` consistency `and` → `or` | survived in-suite; observed by a stub-probe differential | the honest leg is consistent under both predicates |
| N9 | `count_problems` schema check skipped for dict counts | killed by a **crash** (`KeyError: 'fresh_scored'`, rule exit 1) | a crash is a red, not a semantic kill (named limit 17) |
| N10 | legacy rule forces M10 killed (before-arm tool) | survived in-suite; observed by receipt diff | the before-side receipt is still the honest record |

Net: four of eight expected kills confirmed cleanly (N1, N3, N4, N9; N9 by crash); N2 and N7 are
coverage findings; N5 is self-detected; N6, N8 and N10 are observable only by crafted probes.

**Incidental finding (M96-j · a cwd-dependent frozen command).** `kill-rule-v2.py` passes the relative
`--honest-dir .ufo/waves/round-95/l1/scores` to the round-95 battery, and the battery joins it to nothing.
From a directory other than the tree root the regression leg reads an empty path and exits 1
(`receipts/cwd-artifact-demo.json`: only `r95-battery-regression` red). Class: attribution / cwd. Captured-by:
the rule's own red leg (it did fail closed). Fix: routed to round 97 (absolute `os.path.join(root, …)`);
the frozen command is correct only from the tree root, which is where the claim's command 1 runs.

## Named limits (round 96; none closed here unless `## Measured` says so)

1. R96-C1: the bindings bind a receipt to the world it claims and do not authenticate provenance (named before data).
2. R96-C1 (M96-a): `head == revision` is a commit pointer, not a byte binding; a dirty tree measured under a clean commit name passes (CriticC1 finding 3; ConnectorOverlap contradiction note). Routed: byte binding through `git cat-file blob`.
3. R96-C1 (M96-f): `met_target` type not bound (ReviewerInstruments H-1).
4. R96-C1 (M96-e): the frozen mutant table has no `--rev ≠ HEAD` scenario (CriticC1 finding 4, M11).
5. R96-C1: unbound fields `repair_cmd` (while its pin matches), `public_met`/`public_label`, and the imported `imported_r92_battery_sha256` / `imported_v2_sha256` (CriticC1 finding 1). Unbound counts keys outside the nine `COUNT_KEYS` (CriticC1 finding 1; ReviewerInstruments L-2).
6. R96-C1: no bool fixture; the `isinstance(v, bool)` clause is not killed (CriticC1 finding 5, M12). The agreement names the same forgery `label-not-recomputed` (misnamed, `%d` coerces True).
7. R96-C1: `kill-rule-v2.py` does not bind its own green exit to a re-read receipt; `--json-out` is optional there (ReviewerInstruments M-2).
8. R96-C1: K-probe's honest leg runs the unhardened round-94 writer; a probe that always reports `followed-symlink` survives it (CriticC1 finding 6, P2). The hardened discrimination is the separate public leg, outside the frozen label.
9. R96-C1: K-forgeries derives `rev_full` from each fixture's own revision, so `revision-not-bound` cannot fire in that battery (CriticC1 finding 7, K9).
10. R96-C1 (SentinelWrite F3/F5; ReviewerInstruments L-3): K-fsync counts one call and does not check it precedes the replace; the directory is not fsynced. Fleet model: `souji-shokunin/census/round-60/wave/w1/S60ExecRecorder/souji-receipt-write.py`.
11. R96-C1 (ConnectorOverlap): the sibling writer `kake-shokunin/scripts/instrument_receipts.py:643-646` (commit `bde9869144f69c5a459c0d2c93f5135922fe3a8d`) is unremediated; routed to kake.
12. R96-C1 (ReviewerInstruments M-1): `build_copy` does not check that a replaced file still compiles; a syntax-breaking replace would count as a kill. Static check: 11 of 11 mutant files compile at HEAD, so the frozen run is unaffected.
13. R96-C1 (ReviewerInstruments L-4, L-5, L-6, L-7): `r95-unbound-at-base.py` hard-codes its scratch root and asserts `receipt_written` as a constant; the probe-legs docstring misdescribes the writer; the probe's `subprocess.run` timeout is uncaught; `legacy-kill-rule.py` and `fresh-source2-check.py` still write their receipts with a plain `open`.
14. R96-C2: the keyword atom is a vocabulary check (QUALITY 188 residual). CriticC2 (a): a criterion with the opposite rule and the keywords passes; (b): a rule-free criterion `see (QUALITY 193)` passes; (c): a row citing QUALITY 193 for a 194 row passes when 193 also carries 194's words (the citation number is never validated directly); (d): a three-row table passes the shape floor and the padded decoy-table passes `depth-blocks-v3` (`_table_rows` merges every `|` line of the block).
15. Unchanged from earlier rounds: PE and Mach-O packed inputs remain unmeasured.
16. R96-C1 (M96-h, MutationC1 N7/N8): the frozen K-probe does not catch the probe's own write escape: its honest leg runs the unhardened round-94 writer and no check plants a link at the probe's receipt path. The hardened probe is measured only by the public leg, which is outside the frozen label. Route: the planted-link leg on the v6 writer, as a frozen K-probe check, round 97.
17. R96-C1 (MutationC1 N9): a mutant that makes a check crash counts as a kill (exit 1). A crash is not a semantic kill; the kill rule should distinguish a crash from a false verdict. Route: round 97.
18. R96-C1 (M96-j): the frozen command's relative `--honest-dir` makes the regression leg cwd-dependent (see `## Mutation`). Route: round 97.

## Planned (next steered round only)

(a) A round-97 declaration (frozen before scoring) closing named limits 2–5 and 7: byte binding of the pins and the revision through `git cat-file blob`, `met_target` typed, the unbound fields bound or allow-listed, the `--json-out` requirement on `kill-rule-v2.py` with a re-read of its own receipt, the bool and extra-key fixtures, and an M11 `--rev ≠ HEAD` scenario added to the kill rule. (b) The durability gate: fsync-before-replace ordering and the directory fsync, as the souji model, with a kill for each. (c) C2's successor: the criterion cell must restate at least one of its own row's keywords; `table_shape` counts only the snippet-carrying table. (d) Route the kake writer defect to the kake lane through the report; do not edit kake. (e) Carried: the fresh-pack arm now has two sources (S321); a third is not planned.

## Wave r96-w1 — seat results (twelve seats, one v1 wave)

Attack seats = reviewer 2 + critic 2 + mutation-tester 1 + sentinel 1 = 6 of 12 (50 %; the
policy band 8–16, residual none). One connector. The L1 held the planner seat.

- **ExecRepro (executor):** the v6 selftest 13/13, the kill-rule selftest, and the frozen kill rule
  reproduce at the supersession commit (`w1/ExecRepro.md`).
- **ExecFreshSource (executor):** S321 reproduces; `/usr/bin/head` as a supplementary candidate (not admitted).
- **ScribeKnowledge (scribe):** drafts of the knowledge entry, the S321 row, the Gate and the correction
  (`w1/ScribeKnowledge/`). The L1 corrected two provenance statements in the draft (see M96-a).
- **ScribeBlock35 (scribe):** block 35, QUALITY 193/194, and ten registry rows; applied in a clone,
  V1 exit 0, V2 junk exit 1 on keyword atoms, V3 and V4 exit 0 (`w1/ScribeBlock35/verify.txt`).
  The L1 landed them in the lane after one check against the census (exit 0).
- **ScoutS321 (scout):** independent re-measurement of S321 (`w1/ScoutS321.md`).
- **ConnectorOverlap (connector):** no sibling round-96 declaration overlaps; the unremediated sibling
  writer (named limit 11) (`w1/ConnectorOverlap.md`).
- **ReviewerInstruments (reviewer):** H-1 (high), M-1, M-2 and L-1…L-8 (named limits 3, 12, 7, 13).
- **ReviewerScope (reviewer):** PASS on all four declaration items; pins 0 mismatches
  (`w1/ReviewerScope.md`).
- **CriticC1 (critic):** the claim reproduces at HEAD; falsified in part (named limits 1–5, 8, 9; M96-a, M96-e).
- **CriticC2 (critic):** the R96-C2 vocabulary land reproduces; the non-author check of block 34 agrees
  on 4 of 4 rows (named limit 14; `w1/CriticC2.md`).
- **MutationC1 (mutation-tester):** fresh mutants N1–N10 (`w1/MutationC1/`); see `## Mutation` below.
- **SentinelWrite (sentinel):** write-path review of the three receipt writers (`w1/SentinelWrite.md`); findings F3/F5 are named limit 10.

## Verdict (per claim; the frozen predicate, not the broader wording)

- **R96-C1 — verified on the frozen predicate** (kill rule 10 of 10, forgeries 10 of 10, negctl 3 of 3,
  probe 1 of 1, honest 1 of 1; before side 5 of 10 with the survivors M2/M3/M4/M6/M10 and the unbound
  receipts). The broader wording "every unbound field is bound" is **not established**: the wave's
  attacks show named limits 1–13 (M96-a, M96-e, M96-f). The claim's prose is narrowed here by
  disclosure, not by moving the frozen target.
- **R96-C2 — verified on the frozen predicate** at the landing (block 35 present; V1 exit 0; junk
  exit 1; depth v2 and v3 exit 0). The predicate is a vocabulary check; named limit 14.
- Harm check: coverage, depth, calibration and freshness scores unchanged (10.0 proxies); no axis
  harmed by the measurements.
- Exploratory claims: none.
- Non-author spot-check: pending (`corpus/lessons/round-96-verifier-spotcheck.md` will be written by a
  non-author closure, not by this lane).
