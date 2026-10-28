# Round 44 — SquashFS v1/v2 measured 4/4 but not promoted; three self-assessment mismatches repaired and scored 80/80

Base `c29360e3ba5381a5ab69e372d0d9577970f85018`; freeze
`c48f8a4bfd449300c975668e59aae5b5538b6a84` (`plans/round-44-claims.md`); measured revision
`55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`; L1 `KaidokuR44a2` (attempt 2 of the round: attempt 1
froze both claims, ported the counters, ran wave 1 and landed the C1/C2 surfaces, then stopped on
the run wrap-up at 09:57 leaving 74 paths dirty (the fleet orchestrator's non-author lane sweep
committed them at 10:43:43 as `c86ea508`), before the lesson/LOG/SCORECARD record and before the
wave-2 falsification. Everything inherited
was re-verified this attempt — both frozen counters at the measured revision, the C1 receipt
provenance, and the wave-1 registry/results — see `## Inherited state`).

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M44-1 | `stale-premise` — a pre-freeze probe fetched `squashfs_v2.0_be.expected` by guessing the unblob fixture API shape (HTTP 404) before reading the `__output__/` directory listing, whose members are `<name>.bin_extract/` directories | red arm `.ufo/waves/round-44/l1/probe-fixture-404.txt` (committed at the freeze, claim item 10) and the reproduced pair `.ufo/waves/round-44/w1/artifacts/R44MistakeHunt/guessed-expected-404.body` (404, sha256 `d5558cd4…3512ed`) vs `tree-200.html` + `member-names.txt` (200, sha256 `e3ea23b9…3d2f46`); corroborating committed 200 at `w1/R44SrcOracle/listings/squashfs_v2__big_endian__output__.json` | the frozen-URL convention: a URL is pinned only after a successful open of its listing, never guessed | the red/green pair above: the guessed name is absent from the 200 listing (`grep -c 'squashfs_v2.0_be.expected'` = 0) while the real `bin_extract` members appear; `.ufo/waves/round-44/w1/R44MistakeHunt.md` §Verdict |
| M44-2 | `freeze-violation` — attempt 1 mutated 8 files under the frozen **directory** pathspec `tools/round-44/control-fixtures/` in the worktree at 09:50, seven minutes before its honest stop (the graded surface was already non-frozen while `55bcce69` scored) and left them uncommitted; the fleet orchestrator's non-author lane sweep committed them at 10:43:43 as `c86ea508` (author stamp 09:57:16, committer 10:43:43). No gate saw either the dirty tree or the sweep commit; the loss surfaced only when both counters were re-run at the tip, where they exit 2 `frozen_path_changed` instead of 0/1 | `git show -s --format='%h %ad %cd' --date=iso c86ea508 55bcce69` (committer 10:43:43 vs attempt 1's own 09:57:16); mtimes 09:50:09/09:50:30 on `tools/round-44/control-fixtures/{c3,pos}/…`; `.ufo/waves/round-44/l1/preflight-c86ea508.json` (8 paths, byte-identical in both counters' `frozen_path_changed`) | none — the frozen claim states the rule (`` tools/round-44/` is a directory freeze pathspec … no later tool is added there``) but the only enforcement sat inside the scoring counter, which runs after the landing | `tools/round-45/frozen-path-preflight.py` (merge-aware walk + tree blob backstop, exit 0/1/2). Shown able to fail: RED at `--freeze c48f8a4 --rev c86ea508 --pathspec tools/round-44` → exit 1, `frozen_path_changed`, 8 touched paths; GREEN at `--rev 55bcce69` → exit 0 `clean` (`.ufo/waves/round-44/l1/preflight-{c86ea508,55bcce69}.json`). Wave 2 widened the requirement (R44-CL1): add a dirty-tree arm (`git status --porcelain -- <pathspec>`) and place the gate in the fleet sweep path too, because a clean revision is insufficient while the worktree is dirty and a non-author sweep can commit the dirty state (`.ufo/waves/round-44/w2/R44W2Preflight.md` D-3, `R44W2RevAttempt1.md` RA-1/RA-2). Consequence kept honest: R44-C2's admissible score is at `55bcce69`; at the lane tip the claim is inadmissible under its own freeze rule (QUALITY 86) |
| M44-3 | `freeze-violation` (self-inflicted by the record) — the record commit `8bb1090a` appended a `## Round 44` section to `SCORECARD.md`, which the frozen C2 rubric binds as an exact 8-line append, so the tip's C2 `frozen_path_changed` carried 9 paths (`SCORECARD.md` + the 8 from `c86ea508`) | `w2/R44W2C1Satisfy.md` D-3 (symmetric difference `['SCORECARD.md']`); `tools/round-44/c2-rubric.json` `expected_edits["SCORECARD.md"].note` | the rubric's own note ("the round-44 landing section cannot ALSO be appended … the L1 must either land it elsewhere or re-freeze with it bound") — the L1 wrote first and wave 2 caught it | ledger moved to `LOG.md` (`### Round 44 claim ledger`) and `SCORECARD.md` restored to the `55bcce69` blob. Shown able to fail: the C2 counter at the final tip now lists 8 paths with `SCORECARD.md` absent (`.ufo/waves/round-44/l1/c2-score-at-final-tip.json`), where the pre-revert tip listed 9 |

## Gate

### Sources opened this round (2026-10-28)

| row | URL | opened | located quote (≤25 words) |
|---|---|---|---|
| S138 | https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs | 2026-10-28T11:10:29Z–11:12:37Z (contents API, 10 listings + 22 members, HTTP 200; `w1/R44SrcOracle/listings/`, manifest `corpus/evidence/round-44/oracle/manifest.json` sha256 `4bc53dbb…c1a13`, `failures: []`) | listing member `squashfs_v2.0_be.bin_extract` under `squashfs_v2/big_endian/__output__` — 1 token; the tree is the expected member set, "NOT handler code, NOT extractor behaviour, NOT a C1 carrier" (manifest `source.grounds`, 12 words) |
| S139 | https://github.com/plougher/squashfs-tools/releases | 2026-10-28 (page HTTP 200) | tag `4.7.5` present; `/usr/bin/unsquashfs` self-reports `unsquashfs version 4.7.5 (2026/03/01)` (sha256 `461e1fd9…b1677c`) |

### Admission and rejection

- **Admit** S138 (dataset, tier A) and S139 (docs/tool, tier A) as registry rows; both are cited by
  the C1 knowledge entry `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md` and were re-opened
  in-round (the C1 counter's `opened_source_rows` binding is true). Admission is about the registry
  rows, **not** about a Core promotion: R44-C1 stopped, and the entry/PROVINCE/README all say
  "measured, not promoted".
- **Reject** (no adoption) the kaidoku assimilation package this round: `Assimilation: none`. The
  staged package has no entry for round 44, and the full five-row quarantine slice was re-derived
  byte-identically to round 43 (sha256 `7383a90e…28e6a`) and hand-checked live: S150
  fabrication-class (the quoted Japanese heading is absent from the 174,088-byte page), S113/S136/S147
  present with anchor caveats (S113's "17 locales" is really 21 + `x-default`), S117 unverifiable
  (publisher body 0 bytes; Crossref identity matches). No staged row is cited by an admitted entry,
  so none is appended (`w1/R44Quarantine.md` §§2–4).
- `considerthese/`: **absent** in this lane (no such directory at lane root).
- Guard note: because nothing was appended, the 0–3-space id-collision guard is not required this
  round; the re-derived slice carries no new id against the 139-row registry.
- Census before → after: `corpus/SOURCES.md` **137 → 139 rows**
  (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`); round-start
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`
  → `kaidoku ok`, exit 0, 14 W04 duplicate-URL warnings (pre-existing; S138 is the 14th, a
  within-scope URL also present at another row's evidence pointer — not a duplicate id); round-end
  receipt `.ufo/waves/round-44/l1/sources-census-end.txt`. No `status`/`recheck`/`used-by` cell of an
  existing row was changed.

## Routed defects (for round 45; none changes a frozen claim)

The complete wave-1 ledger is `.ufo/waves/round-44/w1/R44ConnRouted.md` (14 rows, ids `R44-*`:
`R44-SCR-TMP`, `R44-LFS`, `R44-SASQ`, `R44-M43-2`, `R44-W2-SYM`, `R44-W2-C1`, `R44-REAP`,
`R44-V2BE`, `R44-OPATH`, `R44-CONF`, `R44-M43-1`, `R44-PROMPT`, `R44-SOURCES-ROUTE`). The six
below are the ones this round acts on or discovered itself; the ledger rows stay open under
their own ids and are not renumbered here.

- **R44-CL1 (M44-2).** No gate saw the frozen-path write: the counter enforces the freeze rule
  only at scoring time, the round had no commit-time gate, and the violating commit was made by the
  fleet orchestrator's non-author lane sweep, not by the lane. Fix landed as
  `tools/round-45/frozen-path-preflight.py` with a demonstrated red/green pair; next round it needs
  (a) a dirty-tree arm (`git status --porcelain -- <pathspec>` non-empty ⇒ exit 1), (b) a mandatory
  pathspec for a directory freeze, and (c) placement in the fleet sweep/pre-push path as well as the
  lane's own commit sequence (`w2/R44W2Preflight.md` D-1..D-3; `w2/R44W2RevAttempt1.md` RA-1/RA-2).
- **R44-CL2.** The frozen R44-C1 text's two `output_directory` clauses cannot both describe one real
  REA output directory: the controls amendment requires it to name a `corpus/evidence/round-44/c1/`
  path and the predicate requires the `/kaidoku-r44/` scratch segment. It is **not literally
  unsatisfiable**: wave 2's H2 variant (a scratch path that also contains the committed-path string,
  `…/kaidoku-r44/x/corpus/evidence/round-44/c1/v1le`) scored `met_target true`, exit 0 — a naming
  loophole, not a provenance. Every receipt this round produced is the plain scratch form
  (`/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/.../rea-out`), so the clause was *unrealized by
  this round's receipts*; the frozen counter does not implement it at all (`provenance_ok()`
  requires only an absolute path containing `/kaidoku-r44/` with no `..`), which is why its red at
  `55bcce69` is the three withdrawn documentation bindings rather than provenance: the score was
  withdrawn under the claim text, not rejected by the counter (`w2/R44W2C1Satisfy.md` V4/V5/D-1;
  `w2/R44W2Preflight.md` D-5). The next freeze must test each claim conjunct against the values its
  own instrument can compute (a satisfiability preflight) and state provenance as exact path
  equality, never "names".
- **R44-CL3.** A **projection-matched authored envelope passes every carrier clause** at
  `55bcce69`: the counter-time REA rerun is live in the scored path and stops a census-only authored
  envelope, but not one whose semantic projection matches (`w2/R44W2C1PosArm.md`; carried from
  R43, still open).
- **R44-CL8 (wave-2 D-2).** The claim's runner-binding clause ("the runner binds the scratch-produced
  tree to the verbatim committed copy under `corpus/evidence/round-44/c1/`",
  `plans/round-44-claims.md:139`) is unimplemented: the counter reads only `after.json`, so mutating
  the committed extract tree at a child of `4cc1ac11` still yields `carriers_matched 4`,
  `met_target true`, exit 0 (`w2/R44W2C1Satisfy.md` D-2). Implement it or strike it from the next
  freeze.
- **R44-CL4.** C2's rubric enumerated 80 entries over its six declared scope categories (a)–(f)
  (`tools/round-44/c2-rubric.json` `scope.categories`; counts SCORECARD 55, SHONEN 22, README 3) and
  its base census records `excluded_ids_mismatching` (`.ufo/waves/round-44/w1/artifacts/R44C2Rubric/receipts/census-base.json`);
  a future calibration claim should state the covered-category census in the claim text, not only in
  the instrument.
- **R44-CL5.** `file(1)` disagrees with the images on both BE carriers' compression token and on
  v1's block size; the C1 counter binds compression from the inode-table metadata block, never from
  `file` text. Keep that binding explicit in future v1/v2 work (`w1/R44C1FixtureAudit.md` N1,
  `w1/R44Debt.md` G11).
- **R44-CL6.** `/usr/bin/cmp -l` exits 0 for 4096-byte differing inputs on this host (diffutils
  3.12-2); all four carriers are exactly 4096 B. Counters must compare with `cmp -s`/`cmp`/sha256
  (claims file item 11; receipt `w1/artifacts/R44EntryDraft/receipt.json`).

- **R44-CL7 (wave-2 F-1/F-2/F-3).** The C2 counter's freeze check enumerates only its own
  hard-coded set — `SCORECARD.md`, `SHONEN.md`, `SKILL.md`, `tools/round-44/c2-counter.py`,
  `tools/round-44/c2-rubric.json` and the `tools/round-44` directory — never the claim file's
  `## Frozen paths`. Six claim-frozen families score green under a single post-freeze mutation,
  including `plans/round-44-claims.md` and `corpus/SOURCES.md` (the latter is frozen at
  `plans/round-44-claims.md:312` and declared NOT frozen at `:318` — the two sentences cannot both
  hold). The 80/80 at `55bcce69` is unaffected (`git log c48f8a4..55bcce69` over those paths is
  empty), but `frozen_path_changed []` does not certify the claim's freeze clause
  (`.ufo/waves/round-44/w2/R44W2C2Freeze.md` §2–§3). Derive the freeze set from the claim next
  round, and state it as exact path equality.

## Carried debt (still open; `w1/R44Debt.md`)

D-01 thin carrier set · D-02 no published v1/v2 carrier · D-03 `squashfs_v2_nonstandard` stays
Frontier · D-04 v3/v4 Broadcom + v3 nonstandard stay Frontier · D-05 gzip v3 bodies stay Frontier ·
D-06 LE AVM / AVM kernels / nested sub-images stay Frontier · D-07 no multi-block, fragment-boundary,
dedup or sparse member exercised · D-08 non-regular gap rule has no positive witness · D-09 oracle
independence rests on `unsquashfs` alone (S138 trees are unblob's) · D-10 six `__output__` trees for
four carriers (v2.1 trees unbound) · D-11 superblock probe must not be validated against `file` ·
D-12 counters dry-run on dev arms before the freeze · D-13 rerun proves projection, not provenance ·
D-14 the four carriers were round-42 held-out inputs · D-15 rubric covers only frozen statements ·
D-16 check-pass ≠ truth · D-17 append-only repair leaves the old text · D-18 declared freeze
exception · D-19 vacuity → honest stop · D-20 calibration ≠ capability · D-21 rubric admissibility ·
D-22 category-(d) escape hatch · D-23 receipt-derived verdicts not re-executed · D-24 shared
README tolerance · D-25 assimilation unexercised · D-26 `considerthese/` absent · D-27 `stale-premise`
fix (now closed by the committed 404 receipt, `## Mistakes` M44-1) · D-28 `SKILL.md` frozen whole.
Prior-round open ids unchanged: R36-CL5, R40-CL2, R41-CL3, R42-CL1, R42-CL2 (falsification wave
served in round 43), R43-CL1..CL4.

## Inherited state (attempt 1 → attempt 2)

Re-verified and kept: frozen claims, `tools/round-44/*` counters and controls, the four C1 after-receipts
(`corpus/evidence/round-44/c1/`), the C2 corrections in `SCORECARD.md`, the C1 honest-stop landing
in `PROVINCE.md`/`corpus/README.md`/the entry, and the wave-1 seat outputs
(`.ufo/waves/round-44/w1/`, 37 seats, `r44-w1-results.json`). Discarded: nothing was deleted; the
only inherited material this attempt does not use as claim evidence is the unbound v2.1 exploration
asset set, which the claims already exclude.
