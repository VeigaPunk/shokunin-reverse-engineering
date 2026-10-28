# R44W2RevAttempt1 — attempt-1 stop point, and the inherited-trust matrix

Seat `R44W2RevAttempt1` (revenger, wave `r44-w2`), lane `kaidoku`, round 44. Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

Scope discipline: this seat is read-only. No claim, counter, rubric, frozen byte or production
doc was modified; no git/jj mutation was issued anywhere; no fixture repo or clone was created;
no scratch tree was created (every command below reads the lane or the orchestrator transcript),
so there is nothing to delete on exit. Findings that the L1 must act on are numbered `RA-n` in
§5 with path:line, command, exit code and observed value. Command receipts (exit code,
stdout sha256, wall seconds) are in
`.ufo/waves/round-44/w2/artifacts/R44W2RevAttempt1/receipts.json`.

## 0. Verdict in one line

Attempt 1 (callsign `KaidokuR44`) stopped on the operator's run wrap-up message at **09:57 local**;
its last own commit is `55bcce69` (committer 09:57:16), and it left its worktree dirty — **432
changed paths** against that commit (400 added, 32 modified), **8 of them under the frozen
`tools/round-44/control-fixtures/`**. The violating commit `c86ea508` was **not made by attempt 1**:
the fleet orchestrator's non-author lane sweep committed that dirty tree at **10:43:43**
(= 13:43:43Z, inside the `13:44:00Z` "landed c86ea508 … ok kaidoku" sweep). Its `author` stamp
`09:57:16` is the working-copy snapshot time, not the commit time. The round's record names the
effect correctly; it gets the actor, the commit count and the routed fix's placement wrong, and it
omits the fleet's earlier intervention in this lane — `RA-1`, `RA-2`, `RA-6`, `RA-7`.

**Record drift:** the record was rewritten by the L1 while this seat ran (report mtime 11:28:23,
`corpus/lessons/round-44.md` 11:29:57, `LOG.md` 11:29:26). Findings are re-anchored to the 11:29
text and tagged with their status at that moment; `RA-1`'s attribution half, `RA-3` and `RA-4` are
already reflected there, `RA-1`'s counts, `RA-5`, `RA-6` and `RA-7` remain open. §9 records the
mapping.

## 1. Method and sources

| source | what it gives |
|---|---|
| `git -C <lane> log --format='%h\|%ad\|%cd\|%s' --date=iso c29360e3..c86ea508` | author **and committer** stamps — the discriminator between "wrote" and "committed" |
| mtimes under `.ufo/waves/round-44/` and `tools/round-44/control-fixtures/` | when attempt 1's work actually landed on disk |
| `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` lines 1817–1840 | launches; the **absence** of a `lane-dead-no-report` line for kaidoku r44 attempt 1 |
| `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-27T07-52-07-309Z_01a17c58-598d-7507-a58f-62bb501eed98.jsonl` lines 2033–2596 (UTC stamps; local = UTC−3) | the driving orchestrator's own words: wrap-up broadcast, stop accounting, lane porcelain, commit sweep, scratch purge |
| `.ufo/waves/round-44/l1/*.json`, `corpus/evidence/round-44/**` | the score receipts and what revision each one actually measures |
| `git show c48f8a4b:<tool> \| sha256sum` vs `sha256sum <tool>` | frozen-tool byte identity |

All wall times in this file are **-03:00 local** unless marked `Z` (the orchestrator transcript
stamps UTC).

## 2. Timeline

Attempt 1 = `KaidokuR44`; orchestrator = hyaku-inline driver (`hyaku-inline attempt=1`); attempt 2
= `KaidokuR44a2`.

| local | actor | event | evidence |
|---|---|---|---|
| 07:41:37 | orchestrator | `unblocked kaidoku` (round start) | transcript:2033 |
| 07:42:04 | watchdog | `launch kaidoku round=44 pgid=3257226 … attempt=1` | watchdog:1817 |
| 07:42:07 | orchestrator | `spawned KaidokuR44` | transcript:2039 |
| 08:04:06 → 08:21:40 | attempt 1 | authoring: 6 commits (draft claims → wave-1 dispatch → carriers/oracle → wave-1 receipts → freeze-review corrections); the lane-identity push later rejects them | transcript:2155 |
| 08:10:01 → 09:33:36 | wave-1 seats | 37 seats write `.ufo/waves/round-44/w1/`; last seat file `R44C1Controls.md` 09:33:36 | mtime sweep |
| 08:58:5x → 08:59:16 | orchestrator | **identity repair (first non-author intervention)**: `jj-lane: push range contains a foreign author email: kaidoku-shokunin <kaidoku-shokunin@shokunin.local> rc=3`; bookmark moved operator-side, 6 objects re-created with `--reset-author`, `landed 7ed97668cc8e…` at 08:59:16 | transcript:2155, 2159, 2167, 2171, 2196 |
| 08:21:40 (A) / 08:59:37 (C) | attempt 1 | `b2a1bd91` freeze-reviewed claims and S138/S139 rows | commit table |
| 08:59:37 (A) / 09:35:19 (C) | attempt 1 | **freeze `c48f8a4b`** (its 6 ancestors are the orchestrator-re-created objects above) | commit table |
| 09:26:05 | attempt 1 | `r44-w1-results.json` written (37 seats, names match the 37 tip-state seat reports) | mtime; `results` cross-check |
| 09:35:19 → 09:50:44 | attempt 1 | `fee6e98a` four C1 REA receipts (committer 09:37:35) · `4cc1ac11` Core docs+coverage map (committer 09:42:48) · `9d3d1862` calibration corrections **+ green C1 counter output** `counter-at-4cc1.json` (committer 09:46:41) · `75a5cb42` **C2 score only** (committer 09:49:16) · `e9e3abd1` control receipts (committer 09:50:44) | commit table; `git show --name-only 75a5cb42` |
| **09:50:09 / 09:50:30** | **attempt 1** | writes the 8 frozen-path fixture files (evidence ids re-minted for the honest-stop landing; `pos/manifest.json` 874→4630 B, entry copy 16880→20280 B) — **post-freeze, uncommitted** | `fixture-mtimes` receipt; `git diff 55bcce69 c86ea508 -- tools/round-44/control-fixtures/pos/manifest.json` |
| 09:50:44 (author) / 09:57:16 (committer) | attempt 1 | `55bcce69` honest-stop docs (PROVINCE/README/entry) | `author-vs-committer` receipt |
| **09:57:03** | orchestrator | operator wrap-up broadcast **delivered to `KaidokuR44`: injected** (39/39 peers) | transcript:2296 |
| **09:57:16** | attempt 1 | **last own commit act**: `55bcce69` committer stamp; the working copy is snapshotted at that instant (gives `c86ea508` its author stamp). Attempt 1 stops. 432 paths remain dirty vs `55bcce69`. | `author-vs-committer`; `.jj` op files at 09:57:16; `c86ea508 parent=55bcce69`, 432 paths |
| 09:58:34 | orchestrator | "**Kaidoku r44 stopped on the operator message after landing `55bcce69`.** … No fleet report yet." | transcript:2318 |
| 09:58:37 | orchestrator | "Kasegi r42 and Kaidoku r44 stopped without fleet reports, so those rounds stay unclosed" | transcript:2321 |
| 10:37:37 | orchestrator | disk-guard purge: "**kaidoku-r44 deleted**" (86 GB; `/fast/scratch/hyaku/kaidoku-r44`) | transcript:2498; 10:41:10 "Scratch is clear" (transcript:2560) |
| 10:42:35 | orchestrator | lane porcelain for kaidoku: summary `count=74` lines (untracked directories collapsed), incl. `M tools/round-44/control-fixtures/c3/…`, `M …/pos/…` | transcript:2570 |
| **10:43:43** | orchestrator | commits that dirty tree → **`c86ea508`** (`parent=55bcce69`, **432 paths**: 400 A / 32 M), author stamp preserved at 09:57:16 | committer stamp; `git show --stat c86ea508`; transcript:2592 (13:44:00Z) |
| 10:44:00 | orchestrator | `landed c86ea508188c50e2645b1f9bba65df4177cda6b1 / ok kaidoku` | transcript:2592 |
| 10:46 | orchestrator | session ends (204 MB session file last written) | session mtime |
| 11:09:13 | watchdog | `launch kaidoku round=44 pgid=943219 … attempt=2` — **no `lane-dead-no-report` line precedes it** | watchdog:1833 |
| 11:12–11:19 | attempt 2 | C2@55bcce69 (11:12:46), C1@55bcce69 (11:13:02), preflights (11:14:51), w2 dispatch (11:18:09), record commit `8bb1090a` (11:18:01), fleet report (11:19:36) | l1 mtimes; commit table |

Two clock facts drive everything below:

* In this lane every commit's **committer** stamp equals the *next* commit's **author** stamp
  (jj finalize-then-snapshot). The sole exception in the range is `c86ea508`:
  author 09:57:16, committer **10:43:43** — a 46-minute gap that is exactly the orchestrator's
  wrap-up sweep, not round work.
* `c86ea508` is therefore the **only** commit in `c29360e3..c86ea508` whose commit act happened
  after attempt 1 stopped. 15 commits are in range; 14 have committer stamps ≤ 09:57:16; 1 has
  10:43:43.

## 3. What attempt 1 actually completed

Completed and committed by attempt 1 — **8 commit objects** (`b2a1bd91`, `c48f8a4b`, `fee6e98a`,
`4cc1ac11`, `9d3d1862`, `75a5cb42`, `e9e3abd1`, `55bcce69`). The six pre-freeze objects
`e1d48d0f`…`7ed97668` were authored by attempt 1 but **re-created and landed by the fleet
orchestrator** at 08:59:16 after the lane-identity push rejection; `c86ea508` was created by the
orchestrator at 10:43:43. 15 commit objects in range: 6 + 8 + 1.

1. the claim freeze and its freeze-review corrections (`e1d48d0f` … `b2a1bd91`, `c48f8a4b`);
2. the four C1 REA after-receipts (`fee6e98a`) — the bytes the round measures;
3. a **green** C1 counter output at `4cc1ac11` (`corpus/evidence/round-44/c1/counter-at-4cc1.json`,
   exit 0, `carriers_matched 4`, `met_target true`), committed into the evidence tree by `9d3d1862`;
4. the C2 score at `9d3d1862` (`corpus/evidence/round-44/c2/c2-score-9d3d.json`, 80 entries,
   `mismatches []`, exit 0), committed by `75a5cb42`;
5. the frozen control receipts (`e9e3abd1`);
6. the C1 honest-stop landing (`55bcce69`) — a **self-retraction of (3)**: authored 09:50:44, i.e.
   eight minutes after the green output was authored (`9d3d1862`, 09:42:48) and four after it was
   committed (09:46:41).

Completed but **not** committed by attempt 1: the 8 post-freeze fixture edits (written
09:50:09–09:50:30) and the 424 remaining wave-1 / artifact / receipt paths — **432 changed paths**
against `55bcce69`, which the orchestrator committed 46 minutes later.

Not started by attempt 1: wave 2, the lesson, the LOG/SCORECARD/QUALITY record, the fleet report,
any frozen-path check. `corpus/lessons/round-44.md`, `LOG.md:3199+`, `SCORECARD.md:3519+` are all
in `8bb1090a` (11:18:01) — attempt 2's commit. No `Report:` file existed at 09:58
(orchestrator:2318 "No fleet report yet"); the fleet report is 11:19:36.

### 3.1 Correction to the inherited premise

The wave-2 brief describes attempt 1's last two works as "the score receipts at 09:46 and the
control-fixture commit at 09:57". Both halves are off, and the difference matters for the trust
matrix:

* **09:46:41 is not a two-claim score commit.** `75a5cb42` contains exactly one path,
  `corpus/evidence/round-44/c2/c2-score-9d3d.json` (C2, revision `9d3d1862`, exit 0). The C1 score
  receipt was committed four minutes earlier by `9d3d1862`
  (`corpus/evidence/round-44/c1/counter-at-4cc1.json`, revision `4cc1ac11`, green).
* **There is no 09:57 control-fixture commit by attempt 1.** The fixture bytes were written at
  09:50:09–09:50:30 (mid honest-stop edit); the commit object is `c86ea508`, created by the fleet
  orchestrator at **10:43:43**. The 09:57:16 event is `55bcce69`'s committer stamp — attempt 1's
  last commit act, the honest-stop landing itself.

So the correct statement of the stop point is: **attempt 1's last completed work is `55bcce69`
(09:57:16), and its last completed *uncommitted* work is the 8-file fixture update (09:50:30) plus
424 further wave/artifact/receipt paths, which it never committed.**

## 4. Trust matrix — what attempt 2 could reuse, and what it had to re-derive

Legend: **trust** = reuse without re-execution, pinned by digest/bytes; **re-read** = input, not
claim evidence, must be read at a named revision; **re-run** = must be executed again; **re-derive**
= must be recomputed from the frozen rule, not read from attempt 1's word.

Summary: **reusable without re-derivation** — the frozen claims, both counters, the rubric, the
carrier pins (digest-identical to the freeze), and the four C1 receipt *bytes*. **Required re-run**
— both scores (attempt 1's receipts measure `4cc1ac11` and `9d3d1862`, not `55bcce69`).
**Required re-derivation** — the freeze-integrity claim (attempt 1 never checked it after its own
fixture writes). **Must be re-read at `c86ea508`, not at the measured revision** — the wave-1 corpus
(28/38 seat reports and no aggregation file exist at `55bcce69`). **Must not be trusted at all** —
the frozen fixture bytes in the worktree; only `git show c48f8a4b:…` has them.

| # | artifact | producer / commit | bytes at `55bcce69` vs tip | verdict | why |
|---|---|---|---|---|---|
| A | `plans/round-44-claims.md`, `tools/round-44/{c1,c2}-counter.py`, rubric, `carriers.json` | attempt 1, `c48f8a4b` (freeze object is attempt-1-created; its six ancestors were re-created by the orchestrator's 08:59 identity repair) | identical: claims sha256 `369a6201…c654` at freeze and tip; `c1-counter.py` `9f2cc140…a993`; `c2-counter.py` `085192ea…c277` (= its `counter_sha256_at_freeze`); `git diff c48f8a4b 55bcce69 -- tools/round-44/` = 0 paths | **trust** | static: digest-rederivable, and both counters are byte-identical to the freeze |
| B | `tools/round-44/control-fixtures/**` (frozen **directory**) | attempt 1 (content, 09:50:30) / orchestrator (commit, 10:43:43) | **differs**: 8 files | **do not trust** | the frozen-directory pathspec is violated at the tip; the freeze-time fixture bytes are only recoverable from `git show c48f8a4b:…` |
| C | four C1 after-receipts `corpus/evidence/round-44/c1/{v1le,v1be,v2le,v2be}/after.json` | attempt 1, `fee6e98a` | identical (the only corpus path that differs 55b→tip is the misplaced C2 score, see `RA-5`) | **trust the bytes**, **distrust the provenance** | digest-pinned and re-read by the counter; but `parameters.output_directory` = `/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/c1-run.<id>.1342995/rea-out` and **that tree was destroyed at 10:37:37** by the orchestrator's disk purge. No seat can inspect "the verbatim scratch tree"; only the counter's rerun projection speaks to it. |
| D | C1 score | attempt 1, revision **`4cc1ac11`** (`counter-at-4cc1.json`, committed `9d3d1862`) | n/a — wrong revision | **re-run** (attempt 2 did, 11:13) | the recorded score measures `4cc1ac11`, not the measured revision; it is green (`exit 0`, `met_target true`) because the docs still claimed the Core row there. The at-revision run is `.ufo/waves/round-44/l1/c1-score-at-55bcce69.json` (exit 1, `met_target false`). |
| E | C2 score | attempt 1, revision **`9d3d1862`** (`c2-score-9d3d.json`, committed `75a5cb42`) | n/a — wrong revision | **re-run** (attempt 2 did, 11:12:46) | the committed receipt's `revision` field is `9d3d1862…`; the measured-revision run is `.ufo/waves/round-44/l1/c2-score-at-55bcce69.json` (80 entries, `mismatches []`, exit 0). |
| F | wave-1 outputs | attempt 1 (08:10–09:33), **committed only by `c86ea508`** | **differs**: 344 A + 24 M under `.ufo/waves/round-44/w1/`; 28 of 38 top-level seat `.md` at `55bcce69` vs 38 at tip; **`r44-w1-results.json` absent at `55bcce69`** | **re-read at `c86ea508`**, not admissible as measured-revision evidence | these are claim *inputs*, not claim evidence, so no re-derivation is owed — but any sentence that places them inside the round's measured surface must name `c86ea508`, i.e. it reads a tree that already carries the frozen-path violation |
| G | freeze-integrity claim (`frozen_path_changed []` at the measured revision) | nobody, until attempt 2 | attempt 1 never checked it after its own 09:50 fixture writes | **re-derive** (attempt 2 did) | preflight `clean` at `55bcce69`, `frozen_path_changed` at `c86ea508`; both counters exit 2 at the tip. Attempt 1's own two counters could not have seen the violation pre-commit: they score a *revision*, and the tree was dirty, not committed. |
| H | control receipts `corpus/evidence/round-44/controls/c{0..5}/**`, `…/pos/**` | attempt 1, `e9e3abd1` (committer 09:50:44) | committed before the stop; bytes stable | **trust as 09:49 measurements**, **do not re-run the arms against the tip** | the arms read the fixtures that B mutates; re-running them at the tip measures mutated inputs, not the frozen ones |

Two corollaries for the other wave-2 seats:

* **C1's stop is not a counter detection.** `c1-counter.py` binds provenance only to the scratch
  segment (`PROV_SEGMENT = '/kaidoku-r44/'`, `provenance_ok()` at `tools/round-44/c1-counter.py:1176-1183`);
  `run_provenance_ok` is `True` for all four carriers in **both** the `4cc1ac11` and the
  `55bcce69` score. The frozen claim's controls-amendment conjunct (a `corpus/evidence/round-44/c1/`
  path in the same field) is **not computed anywhere**. The `55bcce69` exit 1 comes from the three
  *documentation* bindings being false because attempt 1 removed the Core row
  (`province_core_section`, `province_core_row`, `frontier_note`). So "the counter reds the
  provenance mismatch" is false; the honest stop is a prose judgement over the frozen text plus a
  retracted green score, and a falsifier must read it that way (`RA-4` is the record's version of
  this conflation).
* **Attempt 1's green C1 score is disclosed, not hidden.** `corpus/evidence/round-44/c1/counter-at-4cc1.json`
  is cited as the "counter-met precursor" by `.ufo/reports/round-44/kaidoku.md:31-33` and by
  `LOG.md:3201`. The disclosure is adequate; the defect is in the score-receipt attribution
  (`RA-3`), not in concealment.

## 5. Numbered defects (for the L1)

### RA-1 — the record's commit attribution and its two counts (attribution fixed 11:28; counts open)
* **Where (11:29 text).** `/home/vgpnk/Projects/shokunin/.ufo/reports/round-44/kaidoku.md:17-18` —
  "made **14 of the round's 15 commits**, then stopped on the run wrap-up at 09:57 (last own commit
  `55bcce69`). It left **74 paths dirty**, and the fleet orchestrator's non-author lane sweep
  committed them at 10:43:43 as `c86ea508` (author stamp 09:57:16, committer 10:43:43)";
  `corpus/lessons/round-44.md:7` ("leaving **74 paths dirty** (the fleet orchestrator's non-author
  lane sweep committed them at 10:43:43 as `c86ea508`)") and `:18` (M44-2, same attribution).
  *At the 11:19 snapshot this line read "committed 13 round-44 commits" and named no actor; the
  actor half is now correct.*
* **Command.** `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show -s --format='%h author=%ad committer=%cd' --date=iso c86ea508 55bcce69 75a5cb42` → exit 0.
* **Observed.** `c86ea508 author=2026-10-28 09:57:16 -0300 committer=2026-10-28 **10:43:43** -0300`;
  `55bcce69 author=09:50:44 committer=09:57:16`; `75a5cb42 author=09:46:41 committer=09:49:16`.
  The orchestrator's own sweep at `13:44:00Z` printed `landed c86ea508188c50e2645b1f9bba65df4177cda6b1 / ok kaidoku`
  after listing the lane's dirty paths (`count=74` porcelain lines) at `13:42:35Z` (transcript
  lines 2592 and 2570). Attempt 1 had already been accounted stopped at 09:58:34 local =
  `12:58:34Z` (transcript line 2318), i.e. 45 minutes before the sweep.
* **Count — still open.** `c29360e3..c86ea508` holds **15** commit objects: **6** created 08:59:08 by
  the orchestrator's identity repair, **8** created 08:59:37–09:57:16 by attempt 1, **1** created
  10:43:43 by the orchestrator's sweep. "14 of 15" fits none of these; attempt 1's own commit objects
  are 8.
* **Path count — still open.** "74 paths dirty" is the porcelain line count; the sweep's commit is
  **432 paths** (`c86ea508 parent=55bcce69`; `git show --stat` = "432 files changed"; diff status
  400 A / 32 M). **[INFERENCE]** the 74 counts porcelain lines with untracked directories collapsed.
  Either wording is defensible; "74 paths … committed them" is not, because 432 paths were committed.
* **Why it matters.** `R44-CL1` as it stood at 11:19 ("wire the gate into the round's commit
  sequence") would **not** have caught the incident: the violating commit was made by a non-author
  fleet sweep. The 11:29 lesson (`:63-69`) now routes exactly that — (a) dirty-tree arm, (b)
  mandatory pathspec, (c) placement in the fleet sweep/pre-push path — citing `RA-1`/`RA-2`; the
  gate itself still has none of the three (`tools/round-45/frozen-path-preflight.py`, mtime
  11:14:46, unchanged).
* **Action.** Correct the two counts (8 attempt-1 objects / 7 fleet objects; 432 committed paths, or
  label 74 as porcelain lines).

### RA-2 — the frozen-path violation existed in the worktree 7 minutes before the honest stop, and no gate in the round can see a dirty tree *(record now reflects it; fix still unimplemented)*
* **Where (11:29 text).** `corpus/lessons/round-44.md:18` (M44-2) now states the worktree timing
  ("attempt 1 mutated 8 files … in the worktree at 09:50, seven minutes before its honest stop …
  No gate saw either the dirty tree or the sweep commit"); `:63-69` (R44-CL1) routes the three
  fixes — (a) dirty-tree arm, (b) mandatory pathspec, (c) fleet sweep/pre-push placement — citing
  `w2/R44W2RevAttempt1.md` RA-1/RA-2. **Unimplemented:** `tools/round-45/frozen-path-preflight.py`
  (mtime 11:14:46, unchanged) still has no worktree arm — only `git log -m … --name-status` at :48
  and a blob backstop at :67. *At the 11:19 snapshot the M44-2 row said "a post-freeze **commit**
  wrote into a frozen directory pathspec … No commit-time gate existed", with no worktree-timing
  statement.*
* **Command.** `ls -la --time-style=full-iso tools/round-44/control-fixtures/{c3,pos}/manifest.json tools/round-44/control-fixtures/{c3,pos}/corpus/evidence/round-44/c1/v1le/after.json` → exit 0.
* **Observed.** `c3/manifest.json` 09:50:09.711963479 · `c3/…/v1le/after.json` 09:50:09.711747429 ·
  `pos/…/v1le/after.json` 09:50:30.361577291 · `pos/manifest.json` 09:50:30.362234721 — i.e. attempt 1
  mutated the frozen fixtures in the same minute it authored the honest-stop landing, then left
  them uncommitted. Orchestrator porcelain at `10:42:35` lists them as `M tools/round-44/control-fixtures/…`
  (transcript 2570, porcelain summary `count=74` lines; the swept commit is 432 paths).
* **Why it matters.** A commit-time-only gate fires at the wrong moment for this failure mode: for
  53 minutes the round's surface was already non-frozen, while the counters scored `55bcce69`
  (`frozen_path_changed []`, exit 1/0) and the preflight would also have returned `clean` for
  `--rev 55bcce69`. Any seat or sweep that later commits makes the loss retroactive.
* **Action.** Add a dirty-tree arm to `tools/round-45/frozen-path-preflight.py`
  (`git status --porcelain -- <pathspec>` non-empty ⇒ exit 1) and state in `R44-CL1` that a clean
  revision is insufficient while the worktree is dirty. Also make `--pathspec` mandatory for a
  directory freeze: without it the tool's default is "tree backstop only", which cannot catch a
  newly *added* file under a frozen directory.

### RA-3 — `SCORECARD.md` credited the C1 score receipt to the C2-only commit *(fixed at 11:29: the ledger moved to `LOG.md:3220` with the three exact pointers)*
* **Where (11:19 snapshot).** `SCORECARD.md:3521` — "controls `e9e3abd1`; C1/C2 score receipts
  `75a5cb42`". The current text is `LOG.md:3218-3220` (`### Round 44 claim ledger`), which now reads
  "C1 precursor receipt `9d3d1862:corpus/evidence/round-44/c1/counter-at-4cc1.json` (rev `4cc1ac11`,
  exit 0); C2 receipt `75a5cb42:corpus/evidence/round-44/c2/c2-score-9d3d.json` (rev `9d3d1862`,
  exit 0)" — i.e. this finding is already adopted.
* **Command.** `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show --name-only --format='' 75a5cb42` → exit 0.
* **Observed.** `75a5cb42` contains **one** path: `corpus/evidence/round-44/c2/c2-score-9d3d.json`.
  The C1 score receipt actually in the evidence tree is `corpus/evidence/round-44/c1/counter-at-4cc1.json`
  (added by `9d3d1862`, revision `4cc1ac11`, green); the measured-revision C1 run is
  `.ufo/waves/round-44/l1/c1-score-at-55bcce69.json` (added by `8bb1090a`, attempt 2).
* **Action.** Replace the single-sha sentence with three exact pointers: controls `e9e3abd1`;
  C1 precursor `9d3d1862:corpus/evidence/round-44/c1/counter-at-4cc1.json` (rev `4cc1ac11`, exit 0);
  C2 `75a5cb42:corpus/evidence/round-44/c2/c2-score-9d3d.json` (rev `9d3d1862`, exit 0); measured-rev
  C1/C2 runs at `.ufo/waves/round-44/l1/{c1,c2}-score-at-55bcce69.json` (attempt 2).

### RA-4 — the record conflated the `9d3d1862` C2 receipt with a `55bcce69` derivation *(fixed at 11:28)*
* **Where (11:19 snapshot).** `/home/vgpnk/Projects/shokunin/.ufo/reports/round-44/kaidoku.md:47-50`
  — "the frozen 80-entry rubric re-derives every asserted value at `55bcce69` … (`9d3d1862`; receipt
  `corpus/evidence/round-44/c2/c2-score-9d3d.json` and the re-run above)". The current text
  (`:58-61`) separates them: "(the committed receipt `corpus/evidence/round-44/c2/c2-score-9d3d.json`
  measures `9d3d1862`, exit 0; the `55bcce69` derivation is the re-run
  `.ufo/waves/round-44/l1/c2-score-at-55bcce69.json`)" — already adopted.
* **Command.** `python3 -c "import json;print(json.load(open('corpus/evidence/round-44/c2/c2-score-9d3d.json'))['revision'])"` → exit 0.
* **Observed.** `9d3d1862e565e345c4e73c7f76360d84d48499f7` — the committed receipt measures
  `9d3d1862`, not `55bcce69`. The measured-revision derivation is attempt 2's
  `.ufo/waves/round-44/l1/c2-score-at-55bcce69.json` (`entries_evaluated 80`, `mismatches []`,
  `frozen_path_changed []`, exit 0).
* **Action.** Two pointers, two revisions; do not parenthesise a revision marker as if it were the
  receipt's revision.

### RA-5 — a duplicate, non-identical C2 score is filed under the C1 evidence tree (advisory)
* **Where.** `corpus/evidence/round-44/c1/c2-score-9d3d.json` (added by `c86ea508` from attempt 1's
  dirty tree) vs `corpus/evidence/round-44/c2/c2-score-9d3d.json` (added by `75a5cb42`).
* **Command.** `sha256sum` both → exit 0.
* **Observed.** `56df064fe9148b38…ceb63` vs `0c051cc325cec60c…02ad`; both carry
  `revision = 9d3d1862…`, `exit_code 0`, `entries_evaluated 80`; they differ only in
  `wall_seconds` (4.439709 vs 4.227988).
* **Impact.** None on either claim: the C1 counter reads only `c1/<id>/after.json`, so the stray
  file is inert. It is still a reader hazard (a C2 receipt inside the C1 evidence directory) and a
  second non-identical copy of one measurement. **Action:** name the authoritative copy
  (`corpus/evidence/round-44/c2/…`) in the record and delete or annotate the `c1/` copy next round;
  no frozen byte is at stake.

### RA-6 — "wave 1 is 37/37 settled" is a `c86ea508` fact, not a measured-revision fact
* **Where (11:29 text).** `corpus/lessons/round-44.md:139-141` ("the wave-1 seat outputs
  (`.ufo/waves/round-44/w1/`, 37 seats, `r44-w1-results.json`)" inside *Inherited state …
  Re-verified and kept*); `/home/vgpnk/Projects/shokunin/.ufo/reports/round-44/kaidoku.md:26` ("wave 1
  is 37/37 settled in `r44-w1-results.json` with no dead seats" beside the `55bcce69` re-runs) and
  `:94` (same sentence in the wave summary); `LOG.md:3204` ("Wave 1 (37 seats … `r44-w1-results.json`):
  … 0 dead"). None of the four names the revision at which the wave-1 corpus exists.
* **Command.** `git -C … ls-tree -r --name-only 55bcce69 .ufo/waves/round-44 | grep -v '/w1/'` → exit 0;
  `git -C … diff --name-status 55bcce69 c86ea508 -- .ufo/waves/round-44/w1 | awk '{print $1}' | sort | uniq -c` → exit 0.
* **Observed.** At `55bcce69` the wave-1 tree carries **28** of the **38** top-level seat `.md`
  files and **no** `r44-w1-results.json`; five seat reports differ from their tip bytes
  (`R44C1Mutants.md`, `R44C1Oracle.md`, `R44C1Revenger.md`, `R44C2Counter.md`, `R44C2Sentinel.md`)
  plus one artifact copy (`artifacts/R44EntryDraft/corpus/knowledge/…entry.md`); the tip delta is
  **344 A / 24 M**. The aggregation
  file was written at 09:26:05 — seven minutes before the last seat file (09:33:36) — so it is a
  snapshot, not a close-out.
* **Impact.** Neither claim reads wave-1 output, so no claim verdict moves. The risk is
  evidentiary: the only revision carrying the wave-1 corpus is `c86ea508`, the violating commit,
  and the record presents that as part of the round's re-verified, measured surface.
* **Action.** One sentence: "wave-1 outputs read at `c86ea508`; they are round inputs, not claim
  evidence." Optionally regenerate the aggregation at the tip and record its seat/name cross-check
  (37 registry names, 37 matching tip report files; the 38th tip `.md`,
  `R44C1Oracle-r48-ready.md`, is a readiness marker, not a seat).

### RA-7 — the record omits the 08:59 stranded-chain identity repair, though it re-created six pre-freeze objects
* **Where (11:29 text).** `corpus/lessons/round-44.md:136-141` (*Inherited state*) and
  `/home/vgpnk/Projects/shokunin/.ufo/reports/round-44/kaidoku.md:16-29` describe attempt 1's work as
  a single actor's commit sequence plus one fleet sweep; neither mentions the 08:59 repair.
* **Command.** `git log --format='%h|%ad|%cd' --date=iso c29360e3..c86ea508` → exit 0 (receipt
  `commit-table`), read with the orchestrator transcript.
* **Observed.** Six commits (`e1d48d0f`, `08d4bc43`, `c1ff9e89`, `b33a4738`, `2081dc06`, `7ed97668`)
  share committer stamp **08:59:08** (histogram receipt `committer-histogram`: `6 08:59:08`, then one
  commit per later stamp); the transcript at `11:55:20Z`–`11:59:16Z` shows the cause:
  `jj-lane: push range contains a foreign author email: kaidoku-shokunin <kaidoku-shokunin@shokunin.local> rc=3`,
  then an operator-side bookmark move, `--reset-author` across the range, and `landed 7ed97668cc8e…`
  at 08:59:16 local (transcript:2155, 2159, 2167, 2171, 2196). The freeze `c48f8a4b` is
  attempt-1-created, but its six ancestors are fleet-created objects.
* **Impact.** None on either claim: every claim binding pins `c48f8a4b` and later, and the freeze
  commit itself is intact. The impact is on the *provenance narrative*: a reader of the record is
  told one actor made the pre-freeze chain, when the chain was re-authored by the fleet.
* **Action.** One sentence in the lesson's *Inherited state* and the report's timeline: the six
  pre-freeze objects were re-created by the fleet's identity repair at 08:59:16; the freeze and the
  post-freeze objects are the round's.

## 6. What the record gets right (so the wave does not overstate)

* `M44-2`'s **effect** is accurate: `git log --oneline c48f8a4b..c86ea508 -- tools/round-44/` shows
  only `c86ea508`; both counters exit 2 `frozen_path_changed` at the tip with the **same 8 paths**;
  the gate reds at `c86ea508` and greens at `55bcce69` — re-observed by this seat as
  `frozen-path-preflight.py --freeze c48f8a4b --pathspec tools/round-44`: `55bcce69` exit **0**
  (`clean`, 0 paths), `c86ea508` exit **1** (8 paths), and the record tip `8bb1090a` exit **1**
  (same 8 paths) — the round's own record commit therefore inherits the violation, which the report
  discloses at `:148` ("inadmissible at the lane tip (`c86ea508` and later)").
* Measuring at `55bcce69` rather than the tip is the only admissible reading under the frozen
  freeze-integrity rule, and the record says so in `LOG.md:3203` / `:3229` and the report.
* The freeze and both counters are byte-identical at the freeze and at the tip; the claims file is
  byte-identical at the freeze and at the tip; no reviewer needs to suspect post-freeze tool drift.
* Attempt 1's green C1 precursor is committed and cited; the honest-stop retraction is committed
  (`55bcce69`) with the entry, PROVINCE and README saying "measured, not promoted".
* The 11:12–11:13 re-runs by attempt 2 are the first receipts that actually measure `55bcce69` for
  both claims; they match the task's quoted values (`carriers_matched 4`, `met_target false`, exit 1;
  `entries_evaluated 80`, `mismatches []`, `frozen_path_changed []`, exit 0).

## 7. Residual uncertainty

* **[INFERENCE]** The exact prompt text of the wrap-up broadcast is not in the transcript excerpt
  read here (only the delivery line, `KaidokuR44: injected`); its content is inferred from the
  orchestrator's next-turn accounting ("stopped on the operator message") and from the sibling
  lanes' recorded stops. No lane-dead line exists for kaidoku round 44, so the watchdog ledger
  cannot corroborate the stop reason at all — this is a property of the relaunch being an
  operator restart rather than a `lane-dead` retry, and it should not be read as a silent death.
* **[INFERENCE]** That the 10:43:43 commit was executed by `jj-lane.sh`-style tooling under the
  orchestrator is inferred from the `.jj` op files at 10:43:42–10:43:46 and the transcript's
  `landed … ok kaidoku` line; committer **identity** cannot distinguish the actor because every
  commit in this lane carries `kaidoku-shokunin <kaidoku@shokunin.local>`.
* The orchestrator's porcelain line for kaidoku reads `count=74` while the sweep it then made is
  **432 paths** (`git diff --name-status 55bcce69 c86ea508` → 400 A / 32 M; `git show --stat` agrees).
  **[INFERENCE]** the 74 counts porcelain *lines*, with untracked directories collapsed; the
  per-file set is the 432-path diff. Either way the violating commit carries 8 frozen-path files,
  which is what both counters and the preflight report.

## 8. Receipts

Seat `R44W2RevAttempt1`; cwd `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; all commands read-only.

| # | command | exit | stdout sha256 (first 16) | wall s |
|---|---|---|---|---|
| 1 | `git log --format='%h\|%ad\|%cd\|%s' --date=iso c29360e3..c86ea508` | 0 | `d2ce438d c8d643d6` | 0.002 |
| 2 | `git show -s --format='%h author=%ad committer=%cd' --date=iso c86ea508 55bcce69 75a5cb42` | 0 | `e5199765 e198d252` | 0.002 |
| 3 | `git diff --name-status 55bcce69 c86ea508 -- .ufo/waves/round-44/w1 \| awk '{print $1}' \| sort \| uniq -c` | 0 | `3fe4a377 8cef750c` | 0.003 |
| 4 | `git ls-tree -r --name-only {55bcce69,c86ea508} .ufo/waves/round-44/w1 \| grep -Ec '^…/w1/[^/]+\.md$'` | 0 | `a51f5b59 44ba1356` (`28`,`38`) | 0.004 |
| 5 | `git ls-tree -r --name-only 55bcce69 .ufo/waves/round-44 \| grep -v '/w1/'` | 0 | `ec3359cb 328f1e2d` | 0.002 |
| 6 | `git show c48f8a4b:tools/round-44/{c1,c2}-counter.py \| sha256sum` vs `sha256sum` worktree copies | 0 | `8d19c4fe 22bedea4` | 0.005 |
| 7 | `ls -la --time-style=full-iso` on the 4 frozen fixture paths | 0 | `bf598175 a73109f8` | 0.002 |
| 8 | `sed -n '1176,1183p' tools/round-44/c1-counter.py; grep -n PROV_SEGMENT …` | 0 | `4d5277f2 f6b69f80` | 0.003 |
| 9 | `git show --name-only --format='' 75a5cb42; git log --diff-filter=A -- …/c1-score-*.json` | 0 | `c1b26158 994dafdb` | 0.005 |
| 10 | `python3 -c` revision/exit/met/ bindings diff of `c1-score-4cc1.json` vs `c1-score-at-55bcce69.json` | 0 | `9bdcfcb8 6a253fca` | 0.012 |
| 11 | `python3 -I -B tools/round-45/frozen-path-preflight.py --root . --freeze c48f8a4b --rev {55bcce69,c86ea508,8bb1090a} --pathspec tools/round-44` | **0 / 1 / 1** | stdout sha256 `c8a03c26…bfd5` / `20a87d4d…daa7` / `c302813c…f581`; verdicts `clean / frozen_path_changed / frozen_path_changed` (8 / 8 paths) | 0.128 / 0.124 / 0.122 s |
| 12 | `git log --format='%cd' --date=format:'%H:%M:%S' c29360e3..c86ea508 \| sort \| uniq -c` | 0 | `70e4ca26 d4c2ce94` (`6 08:59:08`, then 1 each at 08:59:37 … 10:43:43) | 0.002 |
| 13 | transcript grep for `push range contains a foreign author email…` and `landed 7ed97668…` | 0 | `7f2e8001 6a8ea7e1` (both present) | 0.152 |
| 14 | transcript `grep -c 'landed c86ea508188c50e2645b1f9bba65df4177cda6b1'` | 0 | `4355a46b 19d348dc` → `1` | 0.053 |

Full records (exact command strings, byte counts, stderr tails):
`.ufo/waves/round-44/w2/artifacts/R44W2RevAttempt1/receipts.json`; the three preflight outputs are
`.ufo/waves/round-44/w2/artifacts/R44W2RevAttempt1/preflight-{55bcce69,c86ea508,8bb1090a}.json`.

Tool installs this seat: **none** (no `pacman`, no `uv`, no binary added). Scratch trees created:
**none**. Fixture repos created: **none**. Git/jj mutations: **none**.

## 9. Record drift during this seat — per-defect status at 11:31

The record is being edited by the L1 while wave 2 runs. This seat read it at 11:19 (report 14,274 B)
and again at 11:29–11:31 (report 19,787 B, mtime 11:31:22; lesson 143 lines, 11:31:22; `LOG.md`
11:31:31; the `SCORECARD.md` round-44 section moved to `LOG.md:3218+` under M44-3). Two findings
were adopted in that window; four are still open, re-checked against the 11:31 bytes. A closure
reading this file should re-check the *text anchors*, not the line numbers.

| id | finding | status at 11:31 | current anchor |
|---|---|---|---|
| RA-1 | violating commit attributed to attempt 1, "13" commits (11:19 text) | **actor FIXED** (`report:17-18`, `lesson:7,18`); **counts open** ("14 of 15", "74 paths") | `report:17-18`, `lesson:7` |
| RA-2 | worktree dirty at 09:50, seven minutes before the stop; no gate can see it | **reflected** in `M44-2` (`lesson:18`) and routed in `R44-CL1` (`lesson:63-69`, citing `RA-1`/`RA-2`); **fix unimplemented** — `tools/round-45/frozen-path-preflight.py` unchanged (mtime 11:14:46, no `git status` arm) | `lesson:18`, `:63-69` |
| RA-3 | C1 score receipt credited to the C2-only commit | **FIXED** — ledger moved to `LOG.md:3218-3220` with "C1 precursor receipt `9d3d1862:…counter-at-4cc1.json`" and "C2 receipt `75a5cb42:…c2-score-9d3d.json`" | `LOG.md:3220` |
| RA-4 | `9d3d1862` C2 receipt presented as a `55bcce69` derivation | **FIXED** — report now names both receipts and both revisions | `report:58-61` |
| RA-5 | duplicate, non-identical C2 score under `corpus/evidence/round-44/c1/` | **open** (file still present, 753,998 B, mtime 09:47) | `corpus/evidence/round-44/c1/c2-score-9d3d.json` |
| RA-6 | "wave 1 37/37 settled" presented without a revision, though the corpus exists only at `c86ea508` | **open** — same sentence in four places, no revision | `report:26`, `:94`; `lesson:139-141`; `LOG.md:3204` |
| RA-7 | 08:59 identity repair omitted; six pre-freeze objects are fleet-created | **open** — no mention of the repair in the report or the lesson | `lesson:136-141`; `report:16-29` |

The two remaining numeric corrections (RA-1) and the two remaining record-completeness items (RA-6,
RA-7) are one-line edits; neither moves a claim verdict, a counter value or a score.
