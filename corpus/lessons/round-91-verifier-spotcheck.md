author: hyaku closure (non-author integrator, @m_zfl)

# Round 91 — non-author spot-check (kaidoku)

Non-author closure review of kaidoku round 91. I did not author this round and did not improve it:
I re-derived what is countable over committed bytes, re-opened the sources the gate judged, and
verified the committed evidence of the lane's counters without executing them (PROTOCOL §Gate
standard, closure consequence).

Lane HEAD before the round `fe1913d90a3774020bab129f4c8cc5bc10daa523`; after
`ee44eeb545e81f322bfcd1ec315f3df3b8008f6a`. Round base `2135f6e1d3f69a259b32cc5167c52ccb1a261c24`
(ancestor of `main`, verified); declaration `deb2765a55fef0e4e81500a027dfe59951b69e87`; final
instrument revision `e3ff8f01dbce8600ce3dcd368edcc4c49a4d4658`; measured revision
`6d98f52b6e53a6fde52a78fb9c37df5ff5a865de`.

Driver digest (copied from `.ufo/watchdog.log`, mutable):
`2026-11-05T01:57:18-03:00 launch kaidoku round=91 pgid=1896610 driver=hyaku-inline attempt=3`;
`01:57:51 lane-dead-no-report (attempt 3)`; `02:17:39 launch pgid=1989965 attempt=1`;
`02:18:13 lane-dead-no-report (attempt 1)`; `02:18:15 launch pgid=1993840 attempt=2`;
`02:18:53 lane-dead-no-report (attempt 2)`; `02:18:55 launch pgid=1997520 attempt=3`;
`02:19:33 lane-dead-no-report (attempt 3)`; `07:41:17 launch kaidoku round=91 pgid=153214 driver=hyaku-inline attempt=1`;
`08:15:14 complete kaidoku round=91; hyaku-inline attempt=1`.

## 1. Status ruling — a real report, `ok`

`.ufo/reports/round-91/kaidoku.md` is 16,245 B / 107 lines, carries the contract sections, the
`SHONEN` heading with four `[~]` lines plus evidence pointers, and eight lane-commit citations. It
is not a marker: the landed-changes table names real committed work and every claim names its
counting command. Conformance checks (all commands run by me):

- Attribution: the fleet commit that adds the report is `a6acba20b209d05670f2beadbd33069df29891f2`
  ("round-91: kaidoku report"), author `kaidoku-shokunin <kaidoku@shokunin.local>` — the lane
  identity. Committer time 2026-11-05T08:13:10-03:00, 26 s **after** the lane tip
  `ee44eeb5` (08:12:44-03:00): the report landed last.
- Ancestry: all eight cited commits (`deb2765a`, `f7f5153b`, `fe1913d9`, `04ba98f9`, `e3ff8f01`,
  `86bcdad9`, `6d98f52b`, `ee44eeb5`) exist and `git merge-base --is-ancestor <hash> main` holds
  for each (jj-colocated repo, tested against the `main` ref, not `@{u}`).
- Clean and pushed: `scripts/hyaku/jj-lane.sh state kaidoku-shokunin` →
  `branch=main local=ee44eeb5 remote=ee44eeb5 ahead=0 behind=0`; `git status --porcelain` empty.
- Dispatch evidence durable: `.ufo/prompts/kaidoku-round-91.md` committed under the lane identity
  (commits `2dabc718`, `a2a17e21`, `b25a3b90` across the retry attempts).
- Prompt fidelity: the dispatched prompt carries the round contract — mission/axes binding (§1),
  1–3 claims with distinct axes and the lowest-axis rule (§2), frontier step with census command
  (§2b), L2 floor ≥ 8 in one batched call (§3), commit-then-report ordering, push scope and L0
  side channel (§5), report path/filename, `SHONEN` heading and commit-hash citation rules (§4),
  and hyaku addendum §6. The quoted lane axes line "coverage + depth + calibration (reverse
  engineering with REA)" matches the lane's row in `shokunin.conf` (the route/axes source per
  MISSION.md); no L2 route-map mismatch.
- Wave shape: `.ufo/waves/round-91/r91-w1-results.json` — 12 seats in one wave (≥ 8 L2 floor):
  3 executor, 2 reviewer, 1 critic, 1 mutation-tester, 1 sentinel, 1 scout, 2 scribe, 1 connector;
  attack share 4/12 = 33 % ≥ 25 %; one connector; results handoff committed. No planner seat — the
  L1 held that seat, disclosed in the report (run-15 round shape; a disclosed deviation from
  prompt §3's role split, status-neutral).

## 2. Claim re-checks (evidence-verified, not re-executed)

Both claims rest on lane-owned gates/counters; per PROTOCOL §Gate standard (closure consequence) I
verified their committed evidence — frozen-run verdicts, self-test tallies, named revisions,
registry rows at the lane's registry home (`SKILL.md`) — and did not execute the batteries.

**R91-C1 (coverage, capability acquisition) — verified, improved.**

- Frozen predicates at `deb2765a` in `plans/round-91-claims.md` and `.ufo/waves/round-91/claims.json`
  (both committed before scoring); `claims.json` pins the instrument sha256 values.
- Base receipt `.ufo/waves/round-91/pre/c1-base-round90-repair.json`: label
  `refused 0 of 8; unsafe 2; intact 4 of 4` (all four intact carriers identity rc 0) — matches the
  report's before-arm.
- After receipts `l1/scores/c1-at-6d98f52b.json` and `l1/scores/c1-at-e3ff8f01.json` (and
  `c1-at-04ba98f9.json`): `label = expect = "refused 8 of 8; unsafe 0; intact 4 of 4"`,
  `met_target: true`, `exit: 0`, each naming its `revision`. Per-cell records: all eight tampered
  cells `rc 2` with no output file; `counts` = refused 8, unsafe 0, silent 0, recovered 0, intact 4.
  This exceeds the label's "nonzero, no output" arm: every scored cell is typed rc 2.
- Regression receipt `l1/scores/c1-regression-at-e3ff8f01.json`: `P1 6 of 6; P2 4 of 4; P3 4 of 4`,
  `met_target true`, controls N1 (typed rc 2 refusal, all four carriers) and N2/N3 true.
- Instrument digests re-hashed by me from committed bytes: receipt `repair_sha256 3779d35f…`
  equals `git show 6d98f52b:tools/round-91/upx-stop-boundary-repair.py | sha256sum` **and** the same
  file at the tip; receipt `counter_sha256 5998b6bd…` equals the battery at both revisions. The
  disclosed supersession chain (declared `473bb3a9…` → MED-1 `845013c4…` → MED-2 `3779d35f…`) is
  recorded in `claims.json` `instrument_supersessions` with reasons and reproductions; the final
  bytes are the tip bytes. The frozen label was met before and after each supersession
  (`c1-at-declaration.json`, `c1-at-04ba98f9.json`, `c1-at-e3ff8f01.json`).
- Capability row entered: SCORECARD `last-block stop-boundary refusal` first working round 91;
  registry rows for the repair (verdict map 0/2/1) and the battery (0/1/2, pin-drift
  could-not-evaluate) exist in `SKILL.md` with self-test spellings and write scope.

**R91-C2 (depth, rule block 31) — verified, improved.**

- Before `pre/c2-depth-at-base.json`: `blocks 30, resolved 30, required-shaped 0/0` at
  `2135f6e1d`. After `l1/scores/c2-at-6d98f52b.json` (and `c2-at-e3ff8f01.json`):
  `blocks 31, resolved 31, required-shaped 1/1`, `met_target true`, `exit 0`, revision named.
- Prose control `l1/scores/c2-prose-at-e3ff8f01.json`: `control_killed true` — v3 refuses a
  rows-0 prose fixture v2 accepts (`table:rows:0<3`, `table:cells:0<4`) while accepting the real
  3-row table.
- `SKILL.md` block 31 exists (`stop-boundary-refusal-table v1`): three routed rows citing
  base-present criteria (167, 169, 176) plus a Refs line; shape-floored from 31, history not
  retrofitted. Counter digest pin `bcf6c4ea…` in `claims.json` equals
  `git show 6d98f52b:tools/round-91/depth-blocks-v3.py | sha256sum`.
- Self-test tallies (committed, `.ufo/waves/round-91/w1/ExecSelftests/logs/lane/summary.tsv`,
  mirrored in a declaration clone with identical exits): record-cells 4 cases / 0 failures,
  depth-v3 6/0, stop-boundary-repair 4/0, r90-break-repair 17/0, r89-depth-v2 10/0,
  r90-later-block-battery 8/0, all rc=0; `depth-v3-prose-proof` control_killed true.

**Calibration diagnostic (not claimed) — verified.** `pre/c3-at-base.json` mismatches 5 →
`l1/scores/c3-at-e3ff8f01.json` mismatches 1 (R89-C1 A3 only: its receipts carry no revision field
at all; unrepairable without rewriting a receipt — disclosed, pinned instead). SCORECARD round-89/90
rows corrected as new rows with named revisions and after-receipts (verified in the
`fe1913d9..ee44eeb5` diff); no in-place rewrites.

**Axis-harm sweep.** `git diff fe1913d9 ee44eeb5 -- SCORECARD.md` contains only corrections to the
round-89/90 record rows and the round-91 section's final-receipt pins; no owned axis score moved
down. Spot reads of `SKILL.md`, `PROVINCE.md`, `corpus/README.md`, `QUALITY.md` show additions
(block 31, round-91 Core section, coverage/index/lesson/frontier rows, criteria 178-183), no
deletions or contradictions. No axis harmed.

## 3. Discernment spot-check (LEARNING.md)

`corpus/lessons/round-91.md` `## Gate` records one admit (S313 re-ground) and **no rejects this
round** (no new rows opened; consistent with the census 221 → 221 in the committed receipts and my
re-count). The reject sample is therefore vacuous by honest absence — the zero-reject claim carries
its sweep, not a skipped duty.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S313 re-ground for `corpus/knowledge/2026-11-05-r91-stop-boundary-refusal.md` (the sourced claim) | admit | `https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp` fetched by me: 24,181 B, sha256 `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e` — byte-identical to the row and the lesson; line 496 is exactly `if (sz_cpr > sz_unc || sz_unc > (int)blocksize)` with `throwCantUnpack("corrupt b_info")` at 497 and `fi->readx(ibuf+j, sz_cpr)` at 504; lines 476/485 also match | **agree** | the quote and its location are exact, the tier-A `code` scoping (block loop of `unpackExtent`, not `un_shlib_1`) is accurate, and the entry's claim ("the decoder's only per-block arithmetic bound; the next header is not cross-checked") is supported by the re-opened bytes |
| reject sample | none this round | — (Gate records no rejects; census receipts show 221 → 221) | n/a | no gate rejection exists to sample; recorded honestly rather than invented |

SOURCES.md rows newly written this round: none (the report says so; the committed census receipts
and my `grep -cE '^\|\s*S[0-9]{3,}\s*\|'` count of 221 confirm). I therefore re-opened the one
*touched* row, S313 (its `used-by` old→new change is logged in the lesson), and checked its
located quote — pass, above. `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
kaidoku` exits 0 ("ok") in my re-run; the live run reports 29 W04 duplicate-URL warnings — see
defect D-91-1.

## 4. Trend verdicts (mine, with evidence)

- **expansion — improved.** One knowledge entry on ground the coverage map did not hold
  (`corpus/README.md` line 132: the last-block stop boundary enters **Core (refusal only)**; the
  frontier note at line 387 moves the class from Frontier to Core-as-refusal), `source:` citing
  S313 (`mined`, re-opened 2026-11-05, quote verified). Registry did not grow (221 → 221), stated
  honestly by the lane; the move is a measured refusal entering Core, which is coverage ground.
- **quality — improved.** Entries and instruments re-verified at named revisions with no admitted
  entry failing its re-check: receipts `met_target true` at every revision; two instrument defects
  found in-wave and fixed as disclosed supersessions with the label met before and after; six
  QUALITY criteria added (178-183), three grounded in this round's own defects (181, 182, 183).
  Named limits are measured and disclosed (label admits two cheat repairs and an rc-1 exit; three
  counter mutants survive), with the amendment work routed to round 92 — recorded, not hidden.
- **discernment — improved.** The falsified premise ("the class is not decidable") became M91-8
  and QUALITY 182 with the bounded-search evidence (`ReviewerFalsify`: `upx -t` green on exactly
  the pristine value per cell, 2.1 s/sweep) — a disagreement that became a grounded criterion, the
  LEARNING.md improved path. Six real defects in the round's own work were found by attack seats
  (M91-5, M91-7, MED-1, MED-2, the mis-citation, plus the L1's own M91-3/M91-4 caught pre-wave);
  three closed before landing, three disclosed with routed fixes. Nothing is left unlearned: the
  label amendments (rc assertion, cheat arms, QUALITY-row resolution) sit in the lesson's named
  limits with an owner (round 92). The lane's own grade "mixed" is not protocol vocabulary —
  recorded as defect D-91-2; the underlying facts support improved.

## 5. Routed defects for round 92

- **D-91-1 (report inaccuracy, status-neutral).** The report's Sources & frontier table says the
  end census "reports 7 W04 duplicate-URL warnings (S276, S298, S299, S300, S303, S311, S316)";
  the committed receipts (`.ufo/waves/round-91/l1/census-before.txt` and `census-after.txt`) each
  carry **29** W04 lines, and my live re-run agrees (29). The seven named ids are a subset and
  "none is new or touched this round" holds for all 29; exit 0 both runs. Fix: quote the receipt's
  count verbatim; corrections are appended, never rewritten.
- **D-91-2 (trend vocabulary, status-neutral).** The report grades discernment "mixed, and
  reported as such". The protocol vocabulary is `improved | harmed | unchanged |
  unprovable-but-better`; a split verdict must be stated as one word with the trade reported in
  the evidence. My grade: improved (§4).
- **D-91-3 (carried from the lane's own disclosure).** Block 31's third row cites QUALITY 169, but
  169 is "a superseding instrument inherits its predecessor's guards and refusal contract" — not
  "never refuse an intact input". The lane disclosed it and did not edit the frozen predicate (the
  C2 kill rule makes any post-declaration edit of block 31 a failure); the correction must land in
  round 92 as a new craft-block revision or a superseding criterion row, with the frozen-predicate
  discipline preserved.
- **D-91-4 (label amendments, carried).** The frozen C1 label measures "refused without output",
  not "typed rc-2 refusal by the intended mechanism": two cheat repairs (carrier-read, hash-table)
  and an rc-1 exit pass it (`w1/CriticClaims.md` ATTACK-2, receipts committed). Round 92 should
  add the rc-2 assertion and cheat arms as new counter arms rather than editing the frozen
  predicate.
- **D-91-5 (nit, status-neutral).** `corpus/README.md`'s round-91 lesson row says "six own errors
  mined (M91-1..M91-6)"; the lesson carries eight mistake rows (M91-7, M91-8 were added after the
  wave settled). A count carries its command and its date; refresh the row next round.

## 6. SHONEN and promotion note

The report assesses all four SHONEN boxes `[~]` with resolvable evidence pointers; `SHONEN.md`
itself carries no `[x]` (correct — only a non-author may write one). All four boxes look fully
checkable by a non-author from committed evidence (decision tables with cited criteria; the
end-to-end stop-boundary task measured and logged; selftests that run without oral context;
PROVINCE accurate, no cross-domain bleed per `w1/ConnectorOverlap.md`). Noted for the operator:
promotion is operator-owned; this closure writes no `[x]`.

## 7. Verdict

Round 91 is **admitted**: both claims verify on committed evidence (C1 and C2 evidence-verified;
receipt digests re-hashed against committed bytes; S313 re-opened by me), no axis is harmed, and
the two disclosed supersessions strengthen rather than invalidate the frozen receipts. Defects
D-91-1 through D-91-5 are routed to round 92 and are status-neutral.
