# R44W2ConnCross — cross-document consistency scan, round 44

Seat `R44W2ConnCross` (connector). Assignment: the same round is described in seven documents;
extract every statement about (a) the C1 verdict, (b) the measured revision, (c) the C2 result,
(d) the freeze defect; tabulate who says what; name every pair that disagrees with the exact
sentence pair. No claim, counter, rubric, frozen byte or production doc was modified. This file
and `.ufo/waves/round-44/w2/artifacts/R44W2ConnCross/` are the only writes.

Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Read-only git only. Scratch
`/fast/scratch/hyaku/kaidoku-r44/R44W2ConnCross/` was used for `TMPDIR` and the gate `--json-out`
and is removed before yield (see §7).

## 0. State read

| # | document (absolute path) | sha256 of the bytes read | note |
|---|---|---|---|
| 1 | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/plans/round-44-claims.md` | `369a6201b4e9171a95d8c3d346d5cf8a091237b1e9f8f85eca2697be2b99c654` | frozen claim text, 331 lines |
| 2 | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/LOG.md` | `bcfe1a8df3d385bfa520f6f8beb6d241f8dfab0785078a4adc99359aa683be83` | `## 2026-10-28 — round 44` at `:3198-3205` |
| 3 | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SCORECARD.md` | `8e3062aaa32fd3bccb62931bb2d01cd084b536ee89fa950aacaee089b4ac7af2` | `## Round 44` at `:3519-3531` |
| 4 | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-44.md` | `e1b0c73a8c5ee6b427ba5dc04c467608c6c2774ad6b6827104124610dc89f1b3` | **working tree differs from HEAD**: `git diff` = +11/−3, all inside `## Routed defects` (a new wave-1 ledger paragraph at `:54-59` and a rewritten R44-CL4). HEAD blob `d48af63c72b52b68be11607c1a5b9bfb812e551acf5ea59d2edeb29447837cb0`. None of the quoted C1/C2/revision/freeze sentences is in the delta. Line numbers below are the **working tree**; HEAD's `R44-CL1`/`R44-CL2` sit 6 lines earlier (`:54`/`:57`). |
| 5 | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md` | `f75353207b920d432cd33b335b9b6da7999cc6be8550fa65c42d831f69fc2f62` | the C1 knowledge entry |
| 6 | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/PROVINCE.md` | `e15824daf5037036e84c0939b8b987c204a394b39cf9f02afe0cf42ef8fab98b` | `:424-430` |
| 7 | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/README.md` | `8d2ea86b54b336982cf6521151498bc455c412208b528ac6255e913495668dbd` | `:104`, `:224`, `:275` |

HEAD at read time: `8bb1090a` ("round-44: land lesson, LOG/SCORECARD/QUALITY record,
frozen-path preflight, and wave-2 spec"). Commit order (read-only `git log --oneline -6 main`):
`8bb1090a` → `c86ea508` → `55bcce69` → `e9e3abd1` → `75a5cb42` → `9d3d1862` → `4cc1ac11` →
`fee6e98a` → `c48f8a4b` (freeze). `55bcce69` is an ancestor of `c86ea508`; `4cc1ac11` is an
ancestor of `55bcce69` (receipt `10-tip-commit-order`).

## 1. What each document says

Quotes are verbatim; `…` marks elision only where noted.

| doc | (a) C1 verdict | (b) measured revision | (c) C2 result | (d) freeze defect |
|---|---|---|---|---|
| claims `:157-158`, `:35`, `:137-139`, `:165-169` | not yet a verdict; Target = `carriers_matched == 4`, every binding true, `frozen_path_changed []`, `met_target true`, exit 0. "At the freeze" the counter exits 1 with `carriers_matched 0` (`:75-76`) | "At the measured revision" (`:124`), no hash; the freeze-integrity rule (`:79-90`) makes any `REV` with `FREEZE..REV` clean admissible | Target: `mismatches == 0`, `entries_evaluated >= 1`, exit 0 (`:247-248`) | `tools/round-44/` "is frozen as a DIRECTORY pathspec — a file added under it after the freeze is a change" (`:88-90`) |
| LOG `:3201` | "**C1 — honest stop (measured, not promoted).** The counter at `4cc1ac11` returned `carriers_matched 4/4`, exit 0, every carrier binding true …; at the honest-stop landing `55bcce69` the same counter returns `carriers_matched 4`, `met_target false`, exit 1, with `province_core_section`/`province_core_row`/`frontier_note` false … Cause: the frozen claim text requires `parameters.output_directory` to name BOTH a committed `corpus/evidence/round-44/c1/` path (controls amendment) AND the `/kaidoku-r44/` scratch segment (predicate); … so no run can satisfy the whole frozen …" | names `4cc1ac11` (exit 0) and `55bcce69` (exit 1); `:3202` says C2 is "met at the measured revision" with `--rev 55bcce69` | "**C2 — met at the measured revision.** … `entries_evaluated 80`, `mismatches 0`, `frozen_path_changed []`, `met_target true`, exit 0" (`:3202`) | "Inherited commit `c86ea508` wrote 8 files under the frozen `tools/round-44/control-fixtures/` after both scores, so BOTH counters now exit 2 `frozen_path_changed` at the lane tip … The admissible measured revision is therefore `55bcce69`, not the tip. Fix landed with a demonstrated red/green: `tools/round-45/frozen-path-preflight.py` exits 1 at `c86ea508` (8 touched paths) and 0 at `55bcce69`" (`:3203`) |
| SCORECARD `:3525` | R44-C1 after = "`carriers_matched 4`, `met_target false`, exit 1, `province_core_section`/`province_core_row`/`frontier_note` false: the four REA receipts publish every oracle file at its exact path with no gaps, but the frozen claim requires `parameters.output_directory` to name BOTH a committed `corpus/evidence/round-44/c1/` path and the `/kaidoku-r44/` scratch segment, so no real run can sat[isfy]" — **`4cc1ac11` and the met run are not mentioned anywhere in the round section** | header `:3521`: "C1 honest-stop landing `55bcce69`; measured revision `55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`"; C1 row "measured at `55bcce69`" | "`entries_evaluated 80`, `mismatches []`, `frozen_path_changed []`, `met_target true`, exit 0; the three corrected values re-derive from committed bytes (`137/137`, `21/21`, `81-543`)" (`:3526`); measured at `55bcce69` | "**Freeze-integrity defect (M44-2; QUALITY 77).** Both counters exit 2 `frozen_path_changed` at `c86ea508` (and at the tip) because that commit wrote 8 files … The admissible measured revision is therefore `55bcce69` … The fix is `tools/round-45/frozen-path-preflight.py`, shown red at `c86ea508` (exit 1, 8 touched paths) and green at `55bcce69` (exit 0)." (`:3530`) |
| lessons `:1`, `:4-5`, `:16`, `:60-68` | headline "measured 4/4 but not promoted"; "The honest stop is correct" (`:67`); no mention of a met counter at `4cc1ac11` | "measured revision / `55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`" (`:4-5`); "both frozen counters at the measured revision" (`:8`) | "three self-assessment mismatches repaired and scored 80/80" (`:1`) | M44-2: "`c86ea508` added/edited 8 files … after both counters had already scored at `55bcce69`. … the loss surfaced only when the counters were re-run at the lane tip, where both exit 2 `frozen_path_changed` instead of 0/1" (`:16`); R44-CL1: "Fix landed as `tools/round-45/frozen-path-preflight.py` with a demonstrated red/green pair; **wire it into the round's commit sequence before the next freeze**" (`:60-62`) |
| entry `:3-6`, `:158-160`, `:224` | "status: R44-C1 honest stop. The counter returned `carriers_matched 4/4`, exit 0 at revision `4cc1ac11657590c25b6565d6ab220f53372a94d3` … However, the frozen claim required `parameters.output_directory` under `corpus/evidence/round-44/c1/`, while the frozen counter requires the `/kaidoku-r44/` scratch provenance." (`:3-8`); "(`carriers_matched 4/4`, instrument `met_target true`, `failing []`, `gap_kinds []`). The L1's R44-C1 claim verdict is nevertheless **not met / honest stop**" (`:224`) | **`4cc1ac11657590c25b6565d6ab220f53372a94d3`** (`:4` and `:158`); `55bcce69` appears **nowhere** | silent | silent |
| PROVINCE `:424`, `:428`, `:430` | heading "## Round-44 measured, not promoted (R44-C1 honest stop)"; row: "The counter matched 4/4 and published every oracle file, but the frozen R44-C1 claim and counter disagree about `parameters.output_directory`: the claim required the committed evidence path, while the counter accepts only the `/kaidoku-r44/` scratch provenance. The score therefore does not satisfy the frozen predicate; no Core promotion is claimed." | no hash | silent | silent |
| README `:104`, `:224`, `:275` | "**Measured, not promoted** — REA 6.5.0 `extract-firmware` matched 4/4 … but R44-C1's frozen claim required an evidence-tree `parameters.output_directory` while its counter requires `/kaidoku-r44/` scratch provenance; the score is not admitted and v1/v2 remain Frontier"; knowledge row `:224` repeats "not promoted because the frozen R44-C1 claim and counter disagree on output-directory provenance; no Core claim"; `:275` "**remains Frontier** (R44-C1 honest stop…)" | no hash | silent | silent |

## 2. Agreement set (verified, not merely repeated)

- **A1 — freeze/base/control/score commits.** SCORECARD `:3521` and LOG `:3200` agree:
  base `c29360e3…`, freeze `c48f8a4b…`, controls `e9e3abd1`, C1/C2 score receipts `75a5cb42`.
  lessons `:3-4` agrees on base and freeze.
- **A2 — C2 numbers.** LOG `:3202`, SCORECARD `:3526`, lessons `:1` all say 80 entries / 0
  mismatches / exit 0 / met. The receipt confirms it exactly: `entries_count 80`,
  `entries_evaluated 80`, `mismatches []`, `mismatches_count 0`, `unevaluable_count 0`,
  `frozen_path_changed []`, `exit_code 0`, `met_target true`, all 80 `match: true` with
  `match_reason: "equal"` and `reads_subject: true`, files `SCORECARD 55 / SHONEN 22 / README 3`
  (`03-c2-55bcce69`, exit 0). The base census is 80 entries / **3** mismatches / exit 1
  (`05-c2-base-census`, exit 0 reading `CTL-C2-0.json`), so the round's "3 → 0" move is real.
- **A3 — the three repaired values.** Entries `C2-a1-owned-coverage-count`, `C2-a2-owned-depth-count`,
  `C2-a4-owned-depth-craft-range` observe `137/137`, `21/21`, `81-543`; the pinned entries
  `C2-b1`, `C2-b2`, `C2-b4`, `C2-b9` observe `133/133`, `20/20`, `81-449`. This matches
  claims `:199-205` and SCORECARD `:3526`.
- **A4 — freeze-defect facts.** All three disclosing docs agree on 8 files, commit `c86ea508`,
  both counters exit 2, admissible revision `55bcce69`. Receipts agree byte-for-byte on the path
  list: C1 tip `frozen_path_changed` = 8 paths (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-44/l1/c1-score-at-tip.json`),
  C2 tip `freeze_notes` = the same 8 `changed_under_frozen_dir` entries, gate `touched` = 8
  (`06-preflight-red` exit 1, `touched_count 8`, `blob_changed_count 8`, all `M`).
- **A5 — headline verdict.** All seven say not promoted / measured-not-promoted / Frontier. No
  document claims a Core row, a capability row, or a met C1. (This is the one thing the round's
  record does consistently.)
- **A6 — `tools/round-44/` scope.** The claim (`:88-90`) and both counters agree the directory is
  the freeze pathspec; no frozen path **outside** `tools/round-44` changed in
  `c48f8a4b..c86ea508` (`09-frozen-set-diff` exit 0, empty stdout, sha256 `e3b0c442…`), so the
  gate's `--pathspec tools/round-44` green is not a false green *for this range*.

## 3. Disagreements (each with the exact sentence pair)

### D1 — measured revision: the knowledge entry says `4cc1ac11`, the record says `55bcce69`

- Entry `:3-4`: "The counter returned `carriers_matched 4/4`, exit 0 at revision
  `4cc1ac11657590c25b6565d6ab220f53372a94d3` against freeze `c48f8a4b…`".
- lessons `:4-5`: "measured revision `55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`"; SCORECARD
  `:3521`: "C1 honest-stop landing `55bcce69`; measured revision
  `55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`".
- Why it matters: the two revisions do not report the same thing. At `4cc1ac11` the frozen
  counter says `met_target true, exit_code 0, bindings_false []` (`01-c1-4cc1`, exit 0). At
  `55bcce69` it says `met_target false, exit_code 1, bindings_false
  ["province_core_section","province_core_row","frontier_note"]` (`02-c1-55bcce69`, exit 0). The
  entry never names `55bcce69`; the record never names `4cc1ac11` as the met run except in LOG
  and entry `:224`. A reader who re-runs "the measured revision" per the entry's own `recheck:`
  line lands on a met claim, not on the honest stop. Verified: `55bcce69` is an ancestor of
  `c86ea508`, and `4cc1ac11` is an ancestor of `55bcce69`.

### D2 — C1 after-state: LOG records a met counter run, SCORECARD's round section omits it

- LOG `:3201`: "The counter at `4cc1ac11` returned `carriers_matched 4/4`, exit 0, every carrier
  binding true (`corpus/evidence/round-44/c1/counter-at-4cc1.json`)".
- SCORECARD `:3525` after cell: "`carriers_matched 4`, `met_target false`, exit 1, …" — no
  `4cc1ac11`, no `met_target true`, no exit-0 run in the whole round section.
- Why it matters: the scorecard's "after" column is the claim's state of record. It reports only
  the exit-1 revision, which is the revision *after* the honest-stop landing. The frozen claim's
  own Target (`claims:157-158`) was satisfied at `4cc1ac11`, and the frozen claim's own
  admissibility rule (`claims:79-90`) is satisfied there (`frozen_path_changed []`). The
  scorecard therefore records a measurement of the landing, not of the claim, and does not say so.

### D3 — the stated cause of the exit 1 is not the failing binding (doc vs its own receipt)

- LOG `:3201` / SCORECARD `:3525`: "Cause: the frozen claim text requires
  `parameters.output_directory` to name BOTH a committed `corpus/evidence/round-44/c1/` path
  (controls amendment) AND the `/kaidoku-r44/` scratch segment (predicate); … so no run can
  satisfy the whole frozen [text]" / "so no real run can sat[isfy]".
- The receipt they cite, `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-44/l1/c1-score-at-55bcce69.json`:
  `bindings_false = ["province_core_section", "province_core_row", "frontier_note"]`,
  `failing = []`, and `run_provenance_ok = true` on **all four** carriers; `evidence_id_ok = true`
  on all four (`02-c1-55bcce69`, exit 0). The provenance clause passed. The only failures are the
  three documentation bindings, and those are false **because `55bcce69` is the honest-stop
  landing**, which replaces the `## Round-44 additions to Core` row with `## Round-44 measured,
  not promoted`. The exit 1 is guaranteed by the landing independently of the provenance defect;
  the cited receipt cannot discriminate the two explanations.
- Additional: the counter does not implement the controls-amendment clause at all. `PROV_SEGMENT =
  '/kaidoku-r44/'` is the only path test (`tools/round-44/c1-counter.py:258`, `provenance_ok`
  `:1176-1183`), and `AFTERDIR = 'corpus/evidence/round-44/c1'` is used only to *read*
  `<id>/after.json` (`:246`, `:2070`, `:2856`). So "no run can satisfy the whole frozen text" is an
  assertion about the prose, not a measured result; and the frozen predicate as implemented could
  not have observed a violation of `claims:35` if one existed. That is the second-order defect the
  record's own cause hides.

### D4 — SCORECARD's C2 "before" evidence pointer is an R44-C1 control

- SCORECARD `:3526`: "the rubric's own base census (80 entries, per-id verdict vector) is committed
  with the rubric (`.ufo/waves/round-44/controls/c2/receipt.json`)".
- That path is the C1 red control: `{"claim": "R44-C1", "control": "CTL-C1-2", "title":
  "oracle-only fabrication with a re-minted evidence id", "exit_code": 1, "verdict":
  "as_expected"}` (`04-c2-pointer`, exit 0). The actual C2 base census is
  `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-44/w1/artifacts/R44C2Controls/receipts/real-base/CTL-C2-0.json`:
  `control CTL-C2-0`, `rev c29360e3…` (base), `entries_evaluated 80`, `mismatches 3`, `exit_code 1`,
  `verdict "ok"` (`05-c2-base-census`, exit 0).
- Why it matters: a verifier following the scorecard's pointer to check C2's before-state instead
  lands on an R44-C1 fabrication control and would conclude the C2 base census is missing.

### D5 — "the fix" vs "wire it": LOG/SCORECARD overstate the preflight

- LOG `:3203`: "Fix landed with a demonstrated red/green: `tools/round-45/frozen-path-preflight.py`
  exits 1 at `c86ea508` (8 touched paths) and 0 at `55bcce69`". SCORECARD `:3530`: "The fix is
  `tools/round-45/frozen-path-preflight.py`, shown red at `c86ea508` (exit 1, 8 touched paths) and
  green at `55bcce69` (exit 0)."
- lessons `:60-62`: "Fix landed as `tools/round-45/frozen-path-preflight.py` with a demonstrated
  red/green pair; **wire it into the round's commit sequence before the next freeze**."
- The facts agree (my independent run: red exit 1 with 8 `M` paths; green exit 0). The completeness
  claim does not: nothing calls the gate. `grep -rln frozen-path-preflight tools corpus plans
  LOG.md SCORECARD.md` returns only the script itself, `corpus/lessons/round-44.md`,
  `corpus/QUALITY.md`, `LOG.md`, `SCORECARD.md` (`11-preflight-callers`, exit 0) — no hook, wrapper,
  Makefile target or commit driver. The gate is red at the record commit `8bb1090a` with
  `--pathspec tools/round-44` (exit 1, 8 touched, 8 blob_changed: `12-preflight-at-record-head`),
  so it cannot be wired into round 44 at all: every commit after `c86ea508` includes the violating
  commit in `FREEZE..REV`. Its only reachable use is a *future* freeze with a *new* range.

### D6 — PROVINCE/README say "does not satisfy the frozen predicate" without saying the counter met

- PROVINCE `:428`: "The counter matched 4/4 … The score therefore does not satisfy the frozen
  predicate; no Core promotion is claimed." README `:104`: "… the score is not admitted".
- Against the frozen predicate *as the claim names it* (`claims:124`: "Predicate P44-C1
  (`tools/round-44/c1-counter.py` …)") the counter at `4cc1ac11` returned `met_target true`, exit 0,
  `bindings_false []` (`01-c1-4cc1`). The sentence is true only of the claim *prose* (item 3,
  `claims:35`), which neither PROVINCE nor README distinguishes. A reader of PROVINCE/README cannot
  reproduce "not admitted"; a reader of LOG/entry `:224` learns the counter met. The record needs
  one sentence: the instrument met, the prose did not, and the prose governs.

### D7 — "measured revision" is the revision of the landing, not of the measurement

- SCORECARD `:3521`: "C1 honest-stop landing `55bcce69`; measured revision
  `55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`". lessons `:4-5` repeats it. LOG `:3202` uses the
  same hash for C2 ("met at the measured revision … `--rev 55bcce69`").
- The same commit is both the landing that flips the C1 doc bindings and the "measured revision"
  for C1. The C1 exit 1 at that revision is therefore a restatement of the landing, not a
  measurement of the claim. The round does have a measurement revision — `4cc1ac11`, where the
  counter met with `frozen_path_changed []` — but the record calls the landing the measurement.
  This is the root of D2/D3/D6: one label ("measured revision") is doing two jobs.

## 4. Verdicts on the three assigned attacks

### 4.1 R44-C1 — is the honest stop correct, is it the only reading, does the record say exactly that?

- **The stop is correct under the frozen claim text.** `claims:35` requires the receipt's
  `parameters.output_directory` to name a `corpus/evidence/round-44/c1/` path and the evidence id
  to be minted over that path; `claims:137-139` requires the same field to name the `/kaidoku-r44/`
  scratch segment and the id to be minted over *that* provenance. The committed receipts carry the
  scratch form only (`corpus/evidence/round-44/c1/v1le/after.json:121`:
  `"/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/c1-run.v1le.1342995/rea-out"`; same for
  v1be `:121`, v2le `:139`, v2be `:139`). A frozen claim is satisfied by its text, so
  "not promoted" is right. The claim's own data procedure (`claims:165-169`: REA's output directory
  "is in the private `/kaidoku-r44/` scratch segment, and the runner … copies the produced tree
  verbatim into `corpus/evidence/round-44/c1/<id>/`") confirms the receipts did what the procedure
  says and that item 3 is the contradictory clause.
- **"No run can satisfy the whole frozen text" is asserted, not measured.** The counter enforces
  only `claims:137`; it has no binding for `claims:35`. So the record's claim is a reading of the
  prose (defensible if "minted over that path" means the committed path), not a result any receipt
  in the round establishes. The one artifact that could have tested it — a counter binding for
  `claims:35` — does not exist.
- **The stop is not the only correct reading.** The claim also fixes a Target (`claims:157-158`:
  `met_target true`, exit 0) and names the counter as the predicate. At `4cc1ac11`, an admissible
  revision under the claim's own freeze rule, the named predicate returned exactly the Target
  (`01-c1-4cc1`: `carriers_matched 4`, `met_target true`, `exit_code 0`, `bindings_false []`,
  `frozen_path_changed []`). "Not promoted" is a prose-first override of an instrument-first
  reading; the record never states that choice or why the prose wins. A round that can report
  "the instrument met and I reject it" must say so; this one reports only "the instrument failed"
  (and at a revision where it failed for a different reason).
- **The record does not say exactly that.** It says the stop was caused by the provenance clause
  (D3), cites an exit 1 that is produced by the landing (D2/D7), and pins two different measured
  revisions (D1). The headline is honest; the justification is not.

### 4.2 R44-C2 — confirm or falsify

- **Confirmed at the receipt level.** `03-c2-55bcce69` (exit 0): 80 entries, 80 evaluated,
  `mismatches []`, `unevaluable_count 0`, `frozen_path_changed []`, `met_target true`, exit 0; all
  80 `match: true`, `match_reason: "equal"`, `reads_subject: true`; no entry lacks a command; no
  entry's pass rests on a note (no `note` text in any entry, and `match_reason` is `equal`
  throughout, so the claims' `note_value_disagrees` arm never fires vacuously). Base census
  `05-c2-base-census` is 80 entries / 3 mismatches / exit 1, so the counter is not vacuous at the
  base. The three repaired entries re-derive their claimed values (A3). This is a receipt-level
  confirmation, not an independent re-run of the 80 checks (the counter is frozen and I did not
  re-execute it against the lane, which would be a mutating-free but claim-scoring action; the
  seat's job is the record).
- **One defect, in the record only:** SCORECARD `:3526` points the C2 before-state at an R44-C1
  control (D4). The numbers themselves are consistent across LOG, SCORECARD and lessons.
- **Free-pass caveat, stated not resolved:** the 80/80 is over the rubric's own enumerated set.
  The claims' disclosed limit D-15 ("the rubric enumerates only frozen statements") still binds;
  nothing here shows the 80 statements are the right 80. That is a calibration limit, not a
  cross-document inconsistency.

### 4.3 M44-2 / freeze defect — honest? sufficient? does the preflight really catch it?

- **Honest: yes.** Three docs disclose it with the same 8 paths, the same commit, both exit-2
  receipts retained, and the admissible revision named. No doc claims a tip re-derivation.
- **Sufficient: no.**
  1. **No caller.** `11-preflight-callers` (exit 0) finds only the script and prose references.
  2. **Red at the record commit.** `12-preflight-at-record-head` (exit 1, 8 touched, 8
     blob_changed, pathspec `tools/round-44`). Any `REV ≥ c86ea508` is red, so the gate cannot be
     wired into round 44's commit sequence; lessons' R44-CL1 instruction ("wire it into the
     round's commit sequence before the next freeze") is unexecutable this round and must be read
     as round-45-only.
  3. **Unsafe default.** `13-preflight-no-pathspec-55` (exit 1, `touched_count 110`, statuses
     `A`/`M`, `blob_changed_count 0`, `pathspec []`): omitting `--pathspec` at the *admissible*
     revision `55bcce69` returns a false red over every non-frozen edit. `--pathspec` is mandatory
     in practice but the script does not require it (no error when absent), and with no pathspec
     the tree backstop is skipped. A gate whose default is "red for everyone" will be ignored.
  4. **Covers one pathspec of many.** The green arm covers only `tools/round-44`. The claim's
     frozen set also includes `plans/round-44-claims.md`, `SKILL.md`, `corpus/SOURCES.md`,
     `tools/round-42/fixtures.json`, `tools/round-42/c1-counter.py`, `tools/round-43/c1-counter.py`,
     the four carrier bins, the four oracle trees and pinned historical receipts
     (`claims:78-90`). For this range none of them changed (`09-frozen-set-diff`, exit 0, empty),
     so the green is not false — but the green does not exercise them.
- **Does it really catch it?** The class yes: the status filter includes `A` (`M/D/R/T/U/A/C`,
  `tools/round-45/frozen-path-preflight.py:67-69`), so a new file under a frozen dir is flagged,
  and the actual violation is caught with the exact 8 paths. The *demonstration* only ever shows
  `M`; no receipt in the round exercises an `A` under the frozen dir, a rename out of it, or an
  add-then-delete. The gate is correct on the observed case, unproven on the class, and inert
  until called.

## 5. Defects for the L1 (numbered; each with path:line, command, exit, observed)

1. **`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SCORECARD.md:3526` — wrong C2 base-census
   pointer.** Command: `python3 -I -B -c 'import json;d=json.load(open(".ufo/waves/round-44/controls/c2/receipt.json"));print(d["claim"],d["control"],d["title"])'`
   (cwd lane) → exit 0 → `R44-C1 CTL-C1-2 oracle-only fabrication with a re-minted evidence id`.
   The C2 census is `.ufo/waves/round-44/w1/artifacts/R44C2Controls/receipts/real-base/CTL-C2-0.json`
   (`entries_evaluated 80`, `mismatches 3`, `exit_code 1`). Fix: repoint the parenthetical.

2. **`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/LOG.md:3201` and
   `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SCORECARD.md:3525` — cause of the C1 exit 1 is
   misattributed.** Command: `python3 -I -B -c 'import json;d=json.load(open(".ufo/waves/round-44/l1/c1-score-at-55bcce69.json"));print(d["bindings_false"],d["failing"],{k:v["run_provenance_ok"] for k,v in d["carriers"].items()})'`
   → exit 0 → `['province_core_section','province_core_row','frontier_note'] [] {'v1be': True, 'v1le': True, 'v2be': True, 'v2le': True}`.
   The provenance clause passed; the three doc bindings are false because the honest-stop landing
   removed the Core row. Fix: state the three doc bindings as the failing set, and state that the
   landing itself produced them.

3. **`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:3-4`
   and `:158` — measurement pinned to `4cc1ac11`, which the frozen counter scores met.** Command:
   `python3 -I -B -c 'import json;d=json.load(open("corpus/evidence/round-44/c1/counter-at-4cc1.json"));print(d["revision"],d["carriers_matched"],d["met_target"],d["exit_code"],d["bindings_false"])'`
   → exit 0 → `4cc1ac11657590c25b6565d6ab220f53372a94d3 4 True 0 []`. The entry's `recheck:` line
   (`:16`) says to re-run "at the measured revision"; doing so at the revision the entry names
   reproduces a met claim, not the honest stop. Fix: name `4cc1ac11` as the 4/4 met run and
   `55bcce69` as the honest-stop landing, and state which one the verdict rests on.

4. **`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SCORECARD.md:3525` — the C1 after-cell omits
   the met run.** Command: `python3 -I -B -c 'import json;d=json.load(open(".ufo/waves/round-44/l1/c1-score-4cc1.json"));print(d["revision"],d["met_target"],d["exit_code"],d["bindings_false"])'`
   → exit 0 → `4cc1ac11657590c25b6565d6ab220f53372a94d3 True 0 []`. The scorecard's only C1 state is
   the landing's exit 1. Fix: add the met run as an intermediate after-state, or state explicitly
   that the landing revision is the state of record and why the instrument's met verdict is
   rejected.

5. **`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/LOG.md:3203` and
   `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SCORECARD.md:3530` — "the fix" is not wired and
   cannot gate round 44.** Commands: (a) `grep -rln frozen-path-preflight tools corpus plans
   LOG.md SCORECARD.md` → exit 0 → five matches, none a caller (script + lessons + QUALITY + LOG +
   SCORECARD); (b) `python3 -I -B tools/round-45/frozen-path-preflight.py --root <LANE> --freeze
   c48f8a4b --rev 8bb1090a --pathspec tools/round-44` → exit 1 → `frozen_path_changed`,
   `touched 8`, `blob_changed 8`. Fix: say "gate landed, not wired; red at every revision at or
   after `c86ea508`; usable from the next freeze", matching the lessons' wording.

6. **`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-45/frozen-path-preflight.py:55-70`
   — unsafe default and unexercised class.** Command: `python3 -I -B
   tools/round-45/frozen-path-preflight.py --root <LANE> --freeze c48f8a4b --rev 55bcce69`
   (no `--pathspec`) → exit 1 → `touched_count 110`, `blob_changed_count 0`, statuses `A`/`M`.
   Fix: require `--pathspec` (or default it from the claim), and add one red receipt for an `A`
   under a frozen dir so the class, not only the incident, is demonstrated.

## 6. What the L1 should re-run after the fixes

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
python3 -I -B -c 'import json;d=json.load(open("corpus/evidence/round-44/c1/counter-at-4cc1.json"));print(d["met_target"],d["exit_code"],d["bindings_false"])'      # expect True 0 []
python3 -I -B -c 'import json;d=json.load(open(".ufo/waves/round-44/l1/c1-score-at-55bcce69.json"));print(d["bindings_false"],{k:v["run_provenance_ok"] for k,v in d["carriers"].items()})'  # expect 3 doc rows; all True
python3 -I -B -c 'import json;d=json.load(open(".ufo/waves/round-44/l1/c2-score-at-55bcce69.json"));print(d["entries_evaluated"],d["mismatches_count"],d["exit_code"])'  # expect 80 0 0
python3 -I -B -c 'import json;d=json.load(open(".ufo/waves/round-44/controls/c2/receipt.json"));print(d["claim"],d["control"])'  # currently R44-C1 CTL-C1-2
python3 -I -B tools/round-45/frozen-path-preflight.py --root . --freeze c48f8a4b --rev c86ea508 --pathspec tools/round-44  # exit 1, 8
python3 -I -B tools/round-45/frozen-path-preflight.py --root . --freeze c48f8a4b --rev 55bcce69 --pathspec tools/round-44  # exit 0
```
After the pointer and sentence fixes, both SCORECARD rows and both LOG bullets should be
re-readable without the receipts: the revision label, the failing set and the instrument's met
verdict should each appear in the prose.

## 7. Receipts and scratch

All receipts are in
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-44/w2/artifacts/R44W2ConnCross/`;
each carries seat `R44W2ConnCross`, exact argv, cwd, exit code, stdout sha256, stdout bytes,
wall seconds and the first 3–4 KB of stdout.

| receipt | exit | wall (s) | what it observed |
|---|---|---|---|
| `01-c1-4cc1.receipt.json` | 0 | 0.011 | `met_target true`, exit 0, `bindings_false []`, all four `run_provenance_ok`/`evidence_id_ok` true |
| `02-c1-55bcce69.receipt.json` | 0 | 0.011 | `met_target false`, exit 1, `bindings_false` = 3 doc rows, `failing []`, all four `run_provenance_ok` true |
| `03-c2-55bcce69.receipt.json` | 0 | 0.014 | 80/80, 0 mismatches, 0 unevaluable, all `match_reason equal`, files 55/22/3 |
| `04-c2-pointer.receipt.json` | 0 | 0.011 | `controls/c2/receipt.json` = `R44-C1` `CTL-C1-2` |
| `05-c2-base-census.receipt.json` | 0 | 0.012 | `CTL-C2-0` at base: 80 evaluated, 3 mismatches, exit 1 |
| `06-preflight-red.receipt.json` + `.gate.json` | 1 | 0.089 | `c86ea508`, pathspec `tools/round-44`, 8 touched / 8 blob_changed |
| `07-preflight-green.receipt.json` + `.gate.json` | 0 | 0.088 | `55bcce69`, pathspec `tools/round-44`, clean |
| `08-preflight-no-pathspec.receipt.json` | 1 | 0.029 | `55bcce69` without pathspec: 110 touched, 0 blob_changed (false red) |
| `09-frozen-set-diff.receipt.json` | 0 | 0.001 | empty diff over the non-`tools/round-44` frozen paths, `c48f8a4b..c86ea508` |
| `10-tip-commit-order.receipt.json` | 0 | 0.001 | commit order; `55bcce69` ancestor of `c86ea508` |
| `11-preflight-callers.receipt.json` | 0 | 0.007 | five prose/script matches, no caller |
| `12-preflight-at-record-head.receipt.json` | 1 | 0.094 | `8bb1090a`: 8 touched, 8 blob_changed → gate red at the record commit |
| `13-preflight-no-pathspec-55.receipt.json` | 1 | 0.031 | 110 touched (A/M), 0 blob_changed → unsafe default |

Scratch `/fast/scratch/hyaku/kaidoku-r44/R44W2ConnCross/` held only `TMPDIR` and the two gate
`--json-out` files (copied into the artifacts dir as `06-preflight-red.gate.json` /
`07-preflight-green.gate.json`) and is removed before yield. No tool was installed or upgraded;
no package manager was invoked. No mutating git or jj command was run; the only writes are this
file and the artifacts above.

## 8. One-line answer

The C1 honest stop is defensible on the frozen claim's prose but the record's *reasons* are wrong
in four places: the counter it cites passed the provenance binding (`run_provenance_ok` true on all
four carriers at `55bcce69`), failed only the doc bindings that the honest-stop landing itself
removed, returned `met_target true` at `4cc1ac11` under the claim's own Target and admissibility
rule, and the knowledge entry pins the measurement to that met revision while the scorecard pins it
to the landing. C2 is confirmed 80/80/exit 0 with a base census of 3 mismatches; its only record
defect is a wrong base-census pointer. M44-2 is honestly disclosed and the gate does catch the
incident and the `A` class, but it has no caller, is red at the record commit, has a false-red
default, and exercises one pathspec of the claim's frozen set.
