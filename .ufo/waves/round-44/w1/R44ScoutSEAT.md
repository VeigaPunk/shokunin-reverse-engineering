# R44ScoutSEAT — recommended WAVE-2 seat plan for round 44

Seat type: bounded planner data-walk riding a scout (planner ruling: the wave validator rejects
`planner` as a swarm role; recorded in `plans/round-44-claims.md`). Read-only walk; this file is the
only write. No fixture/clone/tool mutation was performed.

## Inputs read

| source | what it gave |
|---|---|
| `plans/round-44-claims.md` (DRAFT at fc5eb54a; freeze pending) | both claim predicates, control sets, frozen-path list, kill rules, disclosed limits |
| `.ufo/waves/round-44/w1-spec.json` | the 37-seat wave-1 roster + roles |
| `.ufo/waves/round-44/w1-dispatch.json` | validator band `waveMinLanes 32` / `waveMaxLanes 64`; registry schema |
| `tools/round-44/carriers.json` (committed, `kaidoku-r44-carriers-v1`) | carrier ids `v1le v1be v2le v2be`, pins, superblock layout, oracle definition |
| `.ufo/waves/round-43/w2-spec.json`, `round-41/w2-spec.json` | wave-2 conventions: read-only falsification, per-surface attack seats, 32–33 seats |
| `w1/R44RevKill.md` | 3 blocking + 5 non-blocking findings wave-2 must regression-check (K1 frozen-path vs landing contradiction, K2 vacuous seeded control, K3 red-only controls) |
| `w1/R44ConnPattern.md` | freeze-walk variants; recommends porting the round-43 walk (merge-aware + blob backstop), not round-42's |
| `w1/R44C1FixtureAudit.md`, `w1/R44Quarantine.md`, `w1/R44Debt.md` | fixture byte-audit, quarantine verdict, debt ledger seed |

## Facts that shape the plan

- **Wave-2 is the after-side falsification wave** (r43 convention: "falsify frozen claims, controls,
  landed evidence"). It opens only after: freeze commit `FREEZE`, L1's `c1-run.sh` data run,
  committed score/control/dev-arm receipts, and the C1/C2 landing diffs. Wave-2 seats never run
  `c1-run.sh` and never write lane files; scratch only under `probe-<seat>`.
- **C1 target**: `carriers_matched == 4` over `v1le/v1be/v2le/v2be`, every binding true,
  `frozen_path_changed []`, exit 0. Bindings to attack: per-carrier handler EXACT equality; published
  regular files at exact relative path with matching sha256+size; non-regular rows via the gap rule
  (one `unpublished-entry` or one `MaliciousSymlinkRemoved` per symlink; ≤1 structural
  `depth-limited`; no `unknown-chunk-handler`); subject digest = pin; evidence-id recompute;
  carrier bytes hash to pin + superblock probe (magic/s_major/endian/compression); counter-time REA
  rerun semantic-projection equality; PROVINCE row; README map row; S138/S139 source wiring.
- **C2 target**: `mismatches == 0` over the frozen `c2-rubric.json` at REV, every check evaluable,
  `frozen_path_changed []`, exit 0. Rubric categories (a)–(f): evidence-pointer existence; headline
  numbers; SHONEN `path:line`/`N of M`; planned-vs-worked; claim-table verdict vs receipt exit code;
  README row count vs `corpus/knowledge/*.md` count (reads at REV, tolerates the C1 row).
- **Controls wave-2 must re-attack**: C1 CTL-C1-0..3 (+ the RevKill-K3 dev-arm positive if the
  amendment adds it); C2 CTL-C2-0..3 (+ K2 positive clean-clone if added). Each red control must have
  produced the *named* exit and `bindings_false`, not a generic non-zero.
- **Amendments in flight**: RevKill K1 requires per-claim frozen sets and row-identity/append-only
  binding for `README/SOURCES/SCORECARD/SHONEN/SKILL` instead of whole-file blobs; K2 requires a
  positive control per rubric category; K3 requires a C1 dev-arm positive. Wave-2 verifies the
  disposition of every one (implemented or explicitly refused), plus ConnPattern's round-43-walk port.
- **Contingency**: if the wave-1 C2 census froze a rubric that finds ZERO mismatches at base, C2
  stopped honestly — the C2 attack block collapses to the stop-evidence seats (see Contingencies).

## Wave-1 roster (37 seats) — what is already bought

37 seats, all axes `[coverage, depth, calibration]`:
`R44C1Revenger`(revenger) `R44C1Mutants`(mutation-tester) `R44C2Sentinel`(sentinel)
`R44CritC1` `R44CritC2` `R44MistakeHunt`(critics) `R44RevFreeze` `R44RevKill` `R44C1FixtureAudit`
`R44C2SentReview`(reviewers) `R44ConnPattern` `R44ConnSibling` `R44ConnRouted`(connectors)
`R44ScoutCalib` `R44C2Shonen` `R44ScoutSkill` `R44ScoutSEAT` `R44LabV2ns` `R44C2Readme`
`R44C2Plan`(scouts) `R44SrcOracle` `R44EntryDraft` `R44Quarantine` `R44Debt` `R44Shonen` `R44C1Doc`
`R44Assim` `R44Watchdog`(scribes) `R44C1Oracle` `R44C1Counter` `R44C1Run` `R44C1Controls` `R44C2Rubric`
`R44C2Counter` `R44C2Controls` `R44Prefile`(executors) `R44Simplify`(simplifier).

Wave-1 builds and *pre-attacks the draft*; wave-2 attacks the **landed** claim — frozen bytes,
committed receipts, landed diffs — so no wave-1 seat is re-run and no wave-1 verdict is re-used as
wave-2 evidence.

## Recommended wave-2 size: **40 seats** (band [32,64] satisfied; validator floor 32)

40 keeps one seat per independently falsifiable surface without padding: C1 has ~11 separable
bindings, C2 has a 6-category rubric × {re-derive, mutate} plus repair/scope surfaces, and the
cross-claim/report surfaces inherit the r43-w2 shape. Role mix: reviewer 15, critic 7,
mutation-tester 4, connector 4, scribe 3, scout 2, revenger 2, sentinel 2, executor 1.
Attack-share (critic+mt+sentinel+revenger) = 15/40 = 37.5%, consistent with wave-1's 35%.

## Shared wave-2 context (every seat)

- Read the FROZEN `plans/round-44-claims.md` at FREEZE first, then lane tip and the committed
  receipts. Attack whether frozen claims/tools/receipts/landing meet the frozen predicates; do not
  re-open design or change predicates.
- Read-only on the lane; all clones/reruns in `probe-<seat>` scratch (`/fast/scratch/hyaku/kaidoku-r44/`
  or `$HYAKU_SCRATCH`; TMPDIR honored). Reports to `.ufo/waves/round-44/w2/<Seat>.md`, artifacts to
  `.ufo/waves/round-44/w2/artifacts/<Seat>/`.
- Reserved inputs: REA/unblob/sasquatch may only ever see the four pinned MIT unblob 26.6.4 fixtures
  (`corpus/evidence/round-42/c2/fixtures/v{1,2}-{le,be}--*.bin`). The only sanctioned REA execution is
  inside the frozen `c1-counter.py`'s own rerun binding on those carriers; no seat runs REA directly
  on anything else, and nobody runs `c1-run.sh`.
- Receipts carry {seat, command, exit_code, stdout_sha256, wall_s}; semantic exits: 0 met/clean,
  1 failed, 2 could-not-evaluate (never counts toward target). Honest capture beats a pass.
- Report findings as paths+symbols+observed values; an honest stop is reported, never loosened.

## Per-seat task list (40)

### C1 attack block (11)

| seat | role | task |
|---|---|---|
| R44W2C1Predicate | reviewer | Line-by-line P44-C1 audit: every frozen clause → implementing binding in `c1-counter.py` and the committed field in the final score receipt. Flag any clause scored off a summary field rather than re-derived bytes; flag missing/extra bindings. |
| R44W2C1Rerun | revenger | Rerun the frozen `tools/round-44/c1-counter.py --root <lane> --rev <REV> --freeze <FREEZE> --pkg65 <rea 6.5.0 pkg> --work <scratch> --json-out` in own scratch. Byte-diff the JSON vs the committed score receipt modulo wall-time fields; verify `counter_sha256` == sha256(installed file) == `counter_sha256_at_freeze` (r41-closure D4) and that cited post-freeze control receipts hash-match. |
| R44W2C1Oracle | critic | Re-derive both oracles per carrier in scratch: `/usr/bin/unsquashfs -lls` census + extracted regular-file sha256, and the committed `corpus/evidence/round-44/oracle/*__output__` tree. Diff vs `carriers.json` frozen oracle and vs the after-receipts' published members (exact relative path, sha256, size; expected_regular 3/3/4/4). Attack whether sasquatch-derived receipt bytes could have been laundered through the unsquashfs oracle. |
| R44W2C1HandlerMut | mutation-tester | On scratch copies of each after-receipt, mutate the handler string: `squashfs_v10`, `squashfs_v1x`, `SQUASHFS_V1`, `squashfs_v1`→`squashfs_v2` swap, trailing-space and empty strings. Each must flip the per-carrier handler binding red — EXACT equality, never prefix/case. Also a receipt claiming `squashfs_v2_nonstandard` must not match a v2 carrier. |
| R44W2C1ReceiptMut | mutation-tester | Independent receipt mutations per binding: drop one published regular file; flip one sha256 nibble; change a size; insert `unknown-chunk-handler`; convert a symlink's gap into a claimed file; add a second `depth-limited`; corrupt `subject.digest`; break the evidence-id recompute. Each mutation must red exactly the named binding, nothing else. |
| R44W2C1RerunBind | critic | Attack the counter-time REA-rerun binding: a replayed/fabricated envelope (CTL-C1-2 class) and a real-but-edited receipt must fail the semantic-projection equality even if every other binding passes. Verify the comparison is over projection (published set + handler + gaps), not captured stdout bytes. |
| R44W2C1FreezePath | reviewer | Scratch git histories against the frozen walk: merge commit itself editing a frozen blob (the ConnPattern r42-walk hole — must be caught post-port); delete/re-add identical blob; side-branch edit merged; non-ancestor FREEZE; one-byte edit to `carriers.json`/a fixture/`c1-run.sh`. Expect exit 2 `frozen_path_changed` naming the path; a later restore must not un-block. |
| R44W2C1Controls | reviewer | Replay committed CTL-C1-0..3 (+ dev-arm positive if the K3 amendment landed): verify named exits and named `bindings_false` (do-nothing: exit 1, `carriers_matched 0`, all doc bindings false; CTL-1: v3 receipts fail subject/superblock/handler; CTL-2: rerun-projection red; CTL-3: `missing-extractor-dependency` gap, not a clean match). Flag any control that reached `carriers_matched==4` — that is the kill arm. |
| R44W2C1Docs | reviewer | Landed docs vs predicate: PROVINCE `## Round-44 additions to Core` row names `squashfs_v1` AND `squashfs_v2` citing the entry; the round-44 frontier note supersedes ONLY the v1/v2 Frontier text (v2ns/v3bc/v3ns/v4bc/gzip-v3/hsqs/AVM/nested stay Frontier); `corpus/README.md` coverage-map maps the entry stem; no unrelated row touched. |
| R44W2C1Sources | reviewer | SOURCES wiring: S138 (`__output__` trees) and S139 (squashfs-tools releases grounding `/usr/bin/unsquashfs` 4.7.5) exist with `used-by` naming the entry and the entry's `source:` citing them. Spot-verify S138 anchors the committed oracle-tree bytes (sha256 of fetched members vs manifest). If the K1 fix put S138/S139 in at FREEZE, verify they were. |
| R44W2C1Entry | critic | The landed `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md` line-by-line vs receipts/oracle: counts (3,3,4,4), superblock fields, v2be-uncompressed disclosure, Frontier remainders, no overclaim ("promotes the handler family through REA on the frozen carriers, not every v1/v2 image"); `source:`/`verified-at:`/`recheck: 180d` present. |

### C2 attack block (13)

| seat | role | task |
|---|---|---|
| R44W2C2Predicate | reviewer | Line-by-line P44-C2 audit vs the final c2 score receipt + `c2-rubric.json` + appended repairs: every clause measured, no check evaluable-but-skipped, exit 0 iff `mismatches==0` and `frozen_path_changed []`. |
| R44W2C2Rerun | revenger | Rerun frozen `c2-counter.py --root <lane> --rev <REV> --freeze <FREEZE> --work <scratch> --json-out` in own scratch; diff vs committed receipt; verify `counter_sha256`/`counter_sha256_at_freeze` and the rubric blob equality FREEZE→REV. |
| R44W2C2RubricA | reviewer | Re-run every rubric check of categories (a) evidence-pointer existence and (b) headline `## Owned axes` numbers at REV in a scratch clone; compare observed vs rubric-asserted vs counter verdict per entry id. |
| R44W2C2RubricB | reviewer | Same for (c) SHONEN `path:line`/`N of M` at pinned-revision qualifier AND at REV (or `superseded` marker) and (d) `planned (round N+1)` vs actually-worked incl. steer markers. |
| R44W2C2RubricC | reviewer | Same for (e) claim-table `met`/`not met` vs the cited receipt's exit code + headline fields and (f) README map-row count vs `corpus/knowledge/*.md` count at REV, tolerating exactly one new C1 row. |
| R44W2C2Repair | critic | Adversarial repair audit (K6): each repair note must make the rubric check pass at REV by re-derivation, not by note presence. In scratch: appended note with a wrong value → still red; number rewritten without reality fixed → red; a rubric-bound edit differing by one byte from the expected edit block → `frozen_path_changed`/row-identity binding fires. |
| R44W2C2Seeded | mutation-tester | Seeded-mismatch matrix on a scratch clone of the repaired REV tree: corrupt one statement per rubric category (a)–(f) → counter exits non-zero naming that entry id; count uncaught mutations. Plus one-byte rubric edit → exit 2. |
| R44W2C2Controls | reviewer | Replay committed CTL-C2 arms: do-nothing (non-zero iff mismatches>0), positive clean-clone exit 0 (if K2 landed — report if absent), seeded exit 1 per category, malformed-rubric exit 2, rubric-edit exit 2. Verify kill-rule arithmetic: any green seeded control must have stopped C2. |
| R44W2C2Frozen | reviewer | C2 frozen-set integrity at REV post-amendment (K1): whole-blob frozen files byte-equal; row-identity/append-only files still contain every frozen row byte-for-byte with only appended dated blocks; no in-place edit of `SCORECARD.md`/`SHONEN.md`/`corpus/README.md`. |
| R44W2C2Sent | sentinel | Security review of `c2-counter.py`: rubric `check.argv` → subprocess (no `shell=True` string concatenation; env not leaked; cwd pinned to scratch clone), scratch writes confined to `--work`, git invocations read-only/no-network, JSON parsed not eval'd. Rubric is frozen, so exploit attempts must tamper the rubric — confirm that trips exit 2. |
| R44W2C2Stop | critic | Honest-stop chain either way: if the frozen rubric scored 0 mismatches at BASE → verify the recorded stop (claim stops, report says so, no repair landing attempted); if >0 → the recorded base count must equal the rubric's frozen expected value and the frozen rubric must be the census output, not a later edit. |
| R44W2C2CountMut | mutation-tester | Count/verdict mutations in scratch REV clones: drop/add a `corpus/knowledge/*.md`; remove a README map row; flip a cited receipt's exit code; delete an evidence-pointer target; corrupt an `## Owned axes` pinned count. Each flips exactly the rubric check that owns it. |
| R44W2C2Scope | scout | Completeness sweep: enumerate self-assessment statements at REV NOT in the frozen rubric (LOG.md verdict lines, revision pins, any statement class the four wave-1 censuses missed). Each must appear in the report as a new-found defect/lesson item — never silently absorbed into the claim. |

### Cross-claim / landing audit (8)

| seat | role | task |
|---|---|---|
| R44W2CrossClaims | connector | Separability at REV: shared `corpus/README.md` (C1 adds a map row; C2's row-count check reads at REV — verify the rubric tolerates exactly that), `corpus/SOURCES.md` (C1 appends S138/S139; C2 pins no row count); no score/control receipt reused across claims; no mutually dependent assertion. |
| R44W2CrossFreeze | connector | Union frozen-path walk both claims: every path in each amended per-claim frozen set verified FREEZE→REV (merge diffs included); cross-check against wave-1 R44RevFreeze's completeness list — every path it named must be in the frozen sets or dispositioned. |
| R44W2KillRules | critic | Post-hoc kill-rule audit: committed control receipts vs kill-rule text for both claims; any green control → the claim must show the stop. Verify the amendment dispositions of RevKill K1/K2/K3 (per-claim frozen sets; positive controls exist and are green) and ConnPattern's round-43 freeze-walk port (the r42 walk must NOT be what shipped). |
| R44W2SentC1 | sentinel | Security/provenance review of `c1-counter.py`, `c1-oracle.py`, `c1-controls.py`, `c1-run.sh`: path traversal via receipt `child_path`, symlink-following in oracle census, untrusted JSON, unsafe subprocess argv, out-of-scratch writes, fabricated `subject.digest`. Code/receipt inspection only. |
| R44W2AmendCheck | reviewer | Disposition ledger: every blocking wave-1 review finding (RevKill K1–K7, ConnPattern freeze-walk, C2Sentinel bypasses, CritC1/CritC2, RevFreeze gaps) is either fixed in the frozen text/amendments section or explicitly refused with reason. Any silently unresolved blocker = finding. |
| R44W2Ledger | connector | Ledger audit at REV: every disclosed limit still true (v2ns/broadcom/nonstandard/gzip-v3/hsqs/AVM/nested>1 still Frontier — no commit promoted one); R44Debt rows; quarantine 5-row verdict table; `Assimilation: none`/`considerthese` line accurate. |
| R44W2Watchdog | scout | Fleet hygiene: `.ufo/watchdog.log` round-44 entries; no wave wrote outside lane/scratch (spot-check commit paths); TMPDIR honored in installed `tools/round-44/*` (no hardcoded `/tmp`); sibling lanes' surfaces untouched. |
| R44W2ToolHashes | reviewer | Hash-integrity sweep: sha256 of every frozen `tools/round-44/*`, `carriers.json`, `c2-rubric.json`, `c1-run.sh`, fixtures, `tools/round-42/{fixtures.json,c1-counter.py}` at FREEZE vs REV vs the `counter_sha256` values the receipts claim. Any receipt citing a hash ≠ blob = finding. |

### Report & closure block (8)

| seat | role | task |
|---|---|---|
| R44W2FinalRun | executor | Author the wave-2 results collector + run it in scratch: validate every committed round-44 receipt carries {seat, command, exit_code, stdout_sha256, wall_s, counter_sha256, counter_sha256_at_freeze}; emit `.ufo/waves/round-44/w2/artifacts/R44W2FinalRun/r44-w2-results.json` manifest for the L1. Never committed as a tool; artifacts only. |
| R44W2Scorecard | connector | Final SCORECARD/SHONEN/LOG/PROVINCE/README audit at closure: before/after counts, axis deltas, `planned (round 45)` rows, assertion citations; C1/C2 rows consistent with receipts; every post-base line append-only vs the K1 row-identity binding. |
| R44W2Skill | reviewer | `SKILL.md` freeze verification at REV (whole-file or row-identity per the amended frozen set); instrument-registry rows unchanged; any tool-install statement matches the installed file's sha256. |
| R44W2Mistakes | critic | Adversarial review of mined mistakes (the stale-premise probe-404 plus any added): each has captured-by rule, evidence pointer (`.ufo/waves/round-44/l1/probe-fixture-404.txt`), and an implemented fix; no duplicated class; no overclaimed closure. |
| R44W2ReportA | scribe | Assemble the round-44 report draft for the L1: claim verdicts with receipt citations, control verdict table, wave results, frontier step (S138/S139 + located quotes), assimilation line, mined mistakes, debt ledger. Artifacts only — the L1 files it. |
| R44W2Closure | scribe | Verify the assembled report against committed evidence before filing: every hash, count, command, control verdict, claim status, residual-risk line factual; return corrections only, not a second verdict (r43 Closure convention). |
| R44W2Lesson | scribe | Draft `corpus/lessons/round-44.md` sections: claim table, control verdict table, `## Gate` with S138/S139 located quotes, mistakes mined, verifier-spotcheck stubs; artifacts for L1 landing. |
| R44W2Prefile | reviewer | Run the installed `tools/round-44/prefile-check.sh` at pre-file time (scratch mode): WAVE-DONE precedes report, claims frozen-path list non-empty, report path discipline; capture the run receipt. |

## Contingencies

- **C2 honest stop** (frozen rubric finds 0 mismatches at base): the claim stops — keep
  `R44W2C2Stop`, `R44W2C2Controls`, `R44W2C2Frozen`, `R44W2C2Scope` (stop evidence + frozen
  integrity + disclosure completeness); the other 9 C2 seats retire. `waveMinLanes 32` then binds:
  swap in from this alternate bench — `R44W2C1Oracle2` (second independent re-derivation via the
  `__output__` tree only), `R44W2C1Superblock` (per-byte superblock probe vs `file` output on all 4
  carriers), `R44W2Carriers` (fixture pin/byte audit + `tools/round-42/fixtures.json` linkage),
  `R44W2ReadmeMap` (README map-row identity check beyond count), `R44W2DocLineage` (frontier-note
  supersession text diff), `R44W2DevArm` (dev-arm dry-run receipt completeness — every binding
  evaluated per QUALITY 84), `R44W2FreezeWalk2` (merge-diff walk second implementation),
  `R44W2SourcesAudit2` (SOURCES row-schema conformance vs sibling rows), `R44W2GapRule` (gap-rule
  combinatorial enumeration on synthetic receipts). Wave stays ≥32.
- **Any C1 control green** (kill arm): wave-2 still runs — the seats attack the stop evidence and the
  failure analysis; report remains due.
- **Amendment lands late** (frozen set changes before FREEZE): `R44W2AmendCheck` + `R44W2C2Frozen`
  re-derive against the frozen text at FREEZE, not the draft cited here.

## Sequencing for the L1

1. Freeze commit `FREEZE` (claims + `tools/round-44/*` + rubric + oracle tree + control tables).
2. Dev-arm dry-runs + all control receipts scored and committed (before any data).
3. L1 runs `c1-run.sh` → commits `corpus/evidence/round-44/c1/` receipts.
4. Score receipts at REV (both counters) committed; landing diffs applied.
5. Wave-2 opens (this plan), read-only falsification at REV.
6. Wave-2 results → report assembly (R44W2ReportA/Closure/Lesson) → prefile gate → file.

## Residual unknowns (not resolved by this walk)

- Whether the RevKill K1–K3 amendments land as predicted (per-claim frozen sets, positive controls);
  the plan covers both branches via the amendment-disposition and contingency seats.
- Whether the C2 census freezes a >0-mismatch rubric (decides the C2 block vs the bench).
- Exact names/shape of the final score receipts (depend on `c1-counter.py`/`c2-counter.py` as
  installed) — seats key on the frozen JSON fields, not this plan's guesses.
