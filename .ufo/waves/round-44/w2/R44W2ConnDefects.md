# R44W2ConnDefects — consolidated routed-defect table for round 45

Seat `R44W2ConnDefects` (connector, wave 2). Lane
`<LANE> = /home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Freeze
`c48f8a4bfd449300c975668e59aae5b5538b6a84`; admissible measured revision
`55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`; base `c29360e3ba5381a5ab69e372d0d9577970f85018`;
lane tip at first pass `8bb1090af3fef64477c4337855e4347472db2701`; lane tip at write
`923fa87072cc1a728efd88f7038ecb2b8f8af8ff` (the L1's mid-wave remedy commit: M44-3 added,
SCORECARD restored to the `55bcce69` blob; detached HEAD). Rows R45-04 and R45-33 carry a
post-remedy status note.

**What this file is.** One numbered, de-duplicated, severity-ordered table for round 45, built from
(a) the R44-CL1..CL7 list in `<LANE>/corpus/lessons/round-44.md` and (b) every
`<LANE>/.ufo/waves/round-44/w2/*.md` present at snapshot: **40 reports** (34 at the first pass + five
late peers merged in §2b + this file), final list sha256
`fce3fbeed82975f85a6baec2995f368d7e01850ef172f46417106ae3c3cd3ba6` (first-pass 34-report list sha256
`7731da863127fbd7f92b61a639ec66f6df6fee4376f0d359b9ca0a096c55e0e6`); both lists are captured at
`<LANE>/.ufo/waves/round-44/w2/artifacts/R44W2ConnDefects/`. A report arriving after this write is
not merged; the wave's state is the final-list hash. Each row names the merged source ids so no
finding is lost and none is double-counted. Rows are numbered `R45-nn`; wave-1 ids (`R44-*`) and
wave-2 per-seat ids (`D-n`, `F-n`, `RA-n`, `CEN-n`, `HS-n`, `C-n`, …) are preserved in the *Sources*
column because they collide across seats. Rows `R45-01..R45-33` were built at the 34-report pass;
`R45-34..R45-43` merge the five late reports (`Axes`, `C1HonestStop`, `C2Corrections`, `C2Rescore`,
`C2Vacuity`) and are cross-referenced from the earlier rows they extend.

**What this file is not.** No claim, counter, rubric, frozen byte or production doc was changed. The
lesson, `LOG.md` and `SCORECARD.md` were being edited in the working tree while this seat ran (see
R45-33); this table reads the committed blob at `8bb1090a` unless a row says otherwise. No mutating
git/jj command was run; every git call was read-only (`show`, `log`, `diff`, `ls-tree`, `rev-parse`,
`cat-file`, `status`).

## 0. Axes (Godspeed)

1. **Completeness** — every numbered defect in the 40 wave-2 reports (34 at the first pass + 5 late peers + this file) appears in exactly one row.
2. **Grounding** — each row carries a path that resolves, and (where this seat measured it) the
   command, exit code and observed value.
3. **Classification** — new defect vs open debt id (D-01..D-28) vs a change that would move a frozen
   44 byte (next round only).
4. **Falsifiability** — each row ends in an exit condition a round-45 seat can run and get 0/1/2.

## 1. Verdicts on the three contract items (measured here, not inherited)

### R44-C1 — verdict CONFIRMED as an observation; stop correct on the intended text; record does NOT say exactly that

- `<LANE>/tools/round-44/c1-counter.py` at `--rev 55bcce69` → **exit 1**, wall 7.54 s, stdout sha256
  `eea45d374bb450f15c549ca5e7c7803ac9e6c31bb982fae45d6542ee8cac9f8d`;
  `carriers_matched 4`, `met_target false`, `failing []`, `bindings_false
  ["province_core_section","province_core_row","frontier_note"]`, `frozen_path_changed []`,
  every carrier `matched/projection_ok/run_provenance_ok/evidence_id_ok true`. All four oracle file
  sets published exactly: 3/3, 3/3, 4/4, 4/4, `gaps_ok true` on all four.
- **The red is a doc-conformance red, not a provenance red.** The three falsy bindings are the
  promotion documents the stop commit removed. The same frozen counter over the **same receipt
  bytes** returned `met_target true`, `exit_code 0`, `bindings_false []` at `4cc1ac11`
  (`<LANE>/corpus/evidence/round-44/c1/counter-at-4cc1.json`; independently re-derived by
  `w2/R44W2C1Satisfy.md` §5.2 and `w2/R44W2Province.md` D4).
- The stop is correct **only** under the reading that `parameters.output_directory` must *be* the
  committed evidence path. Under the literal frozen wording it is not the only reading:
  `w2/R44W2C1Satisfy.md` §4 tag **H2**
  (`/fast/scratch/hyaku/kaidoku-r44/…/rea-out/corpus/evidence/round-44/c1/<id>`) scores exit 0,
  `met_target true`, `failing []` — see R45-02.
- The record is honest in `LOG.md:3201`, `SCORECARD.md:3525` and the knowledge entry (they name the
  `4cc1ac11` met run), but **`PROVINCE.md:428` and `corpus/README.md:224` state the wrong cause**
  ("score therefore does not satisfy the frozen predicate" tied to `output_directory`), and the
  entry quotes only the **exit 0** run while the measured-revision exit is **1** — R45-01.

### R44-C2 — verdict CONFIRMED at `55bcce69`; non-vacuous at BASE; one repair is false at REV

- Rerun: `<LANE>/tools/round-44/c2-counter.py --rev 55bcce69 --freeze c48f8a4b` → **exit 0**, wall
  4.73 s, stdout sha256 `dd7c529bb6340c364854093937bce3d90ec980ebdea951263bb38dc52316a9b3`;
  `entries_evaluated 80`, `mismatches []`, `unevaluated 0`, `frozen_path_changed []`,
  `counter_sha256 == counter_sha256_at_freeze == 085192ea…36c277`. Matches the committed receipt and
  the independent reruns in `w2/R44W2Preflight.md`, `w2/R44W2C1ReceiptAudit.md` §4 and
  `w2/R44W2C1Satisfy.md` V8.
- Vacuity: the base census is red with exactly the three target ids (`w2/R44W2ScoutDebt.md` D-19,
  `w2/R44W2C2Freeze.md` baseline, CTL-C2-0 vector in `tools/round-44/c2-rubric.json`) → the predicate
  is not vacuous at BASE. Free-pass/note-vs-value: CTL-C2-1 seeded mismatch, CTL-C2-4 wrong-value
  note and the 80/80 mutation witnesses are present; `w2/R44W2C1ReceiptAudit.md` §4 did not falsify
  them.
- **But one repair is evaluated at the freeze tree, not at REV, and is false at REV**: the appended
  coverage value `137/137` (`<LANE>/SCORECARD.md:3512-3513`) while Command A over `55bcce69` derives
  **138/138** (the C1 entry it landed). The lane's own `tools/round-38/c2-counter.py` exits 1 at
  `55bcce69` with five mismatches; the round record never says so — R45-07.
- **The round's own closing commit adds a ninth frozen-path violation**: C2 at `8bb1090a` exits 2
  with 9 `frozen_path_changed` paths (the 8 M44-2 files **+ `SCORECARD.md`**) — R45-04, remedied at
  `923fa870` (8 paths).
- **The aggregate is sound; the composition is not.** Late reports measure: six entries are green
  generators (R45-36), the three target entries are note-driven and do not check the row they repair
  (R45-35), and 71/80 entries violate the claim's own B2 substring rule (R45-34). `mismatches == 0`
  at REV is true; "80 statements checked" is not what the instrument did.

### M44-2 / freeze defect — HONEST, NOT SUFFICIENT

- Honest: only `c86ea508` touches `tools/round-44/` in `c48f8a4..tip`; all 8 paths are `M`; both
  counters exit 2 at the tip with the same 8; `preflight-c86ea508.json` and
  `preflight-55bcce69.json` reproduce byte-for-byte (this seat: exit 1 sha `20a87d4d…a28896`,
  exit 0 sha `c8a03c26…0a870f`). `55bcce69` is admissible under the rule, which quantifies over
  `REV`.
- Not sufficient: (i) the 8 files are the **C1 control inputs**, re-captured after the freeze with
  new provider/evidence ids, and the committed `pos`/`c3` control receipts describe the post-freeze
  bytes (R45-05); (ii) the control receipts themselves are unreproducible (R45-06); (iii) the fix is a
  hand-run detector with no caller, no jj-level hook, a caller-supplied pathspec covering 1 of the
  claim's 12 frozen families, and a false-red on C2's admissible `SCORECARD.md` append (R45-08);
  (iv) the violating commit was made by the fleet orchestrator's non-author sweep at 10:43:43, not by
  the round, so a round-only gate would not have fired (R45-10).

## 2. The routed-defect table (round 45)

Severity: **P1** = a record or instrument claim is false/unsound now; **P2** = a rule is stated but
not enforced, or a receipt cannot be re-derived; **P3** = precision/hygiene. Flags:
`[debt]` = really an open debt id, not a new defect; `[frozen44]` = the fix moves a byte frozen by
round 44 and therefore belongs to the next freeze, never this round.

| id | severity | defect (one line) | evidence path (resolves at snapshot) | sources merged | owner | falsifiable exit condition | flags |
|---|---|---|---|---|---|---|---|
| R45-01 | P1 | The C1 stop is recorded as a *provenance* red, but the measured-revision red is the three withdrawn promotion-document bindings and the same counter returned `met_target true` at `4cc1ac11`; `PROVINCE.md:428`, `README.md:224` and the entry state the wrong cause and the entry quotes only exit 0. | `<LANE>/.ufo/waves/round-44/l1/c1-score-at-55bcce69.json` (`bindings_false`, `failing []`); `<LANE>/corpus/evidence/round-44/c1/counter-at-4cc1.json` (`exit_code 0`, `met_target true`); `<LANE>/PROVINCE.md:428`; `<LANE>/corpus/README.md:224`; `<LANE>/corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:3-9,158-166,224` | R44-CL2; Preflight D-5; C1Rescore D1-D3; Province D1/D3/D4; ConnCross D3/D6; C1Oracle F1-F3; Entry D1; Readme D2; ReceiptAudit D4; Quality77 D8; C1Satisfy V4/V7 | lane r45 (record) | `grep -c` of the string `met_target false` **and** of `4cc1ac11` is ≥1 in the lesson, entry, `PROVINCE.md` and `README.md`; the sentence attributing exit 1 to provenance is gone or qualified. | |
| R45-02 | P1 | "The frozen R44-C1 text is internally unsatisfiable" is false: H2 (`…/kaidoku-r44/<run>/rea-out/corpus/evidence/round-44/c1/<id>`) satisfies both prose clauses **and** the counter (exit 0, `met_target true`); "the only correct reading" is not established, and the "runner binds the verbatim committed copy" clause has no code (corrupting the committed extract tree still scores exit 0). | `<LANE>/plans/round-44-claims.md:34-36` vs `:137-139`; `w2/R44W2C1Satisfy.md` §4 (H2 commit `3c22fe42…`, H3 `372a2da5…`, §4.4 corruption `4e9880d4…`); `<LANE>/tools/round-44/c1-counter.py:246,2070` (nothing opens the tree); `w2/R44W2SentEnvelope.md` D-1/D-2 | R44-CL2; C1Satisfy V5/V6/D-1/D-2; Entry D6; Readme D3; ConnSibling D5; Province D2; C1Rescore D4; SentEnvelope D-1/D-2/D-3 | lane r45 (claim text + satisfiability preflight) | At the next freeze: (a) the claim names one provenance form as an **exact path prefix**, not "names"; (b) a pre-freeze satisfiability preflight evaluates every conjunct against a value its own counter computes and names the conjunct pair when two disagree (Quality77 §9 Row 87); (c) either the tree-copy clause is implemented or deleted; (d) `provenance_ok` anchors to the round scratch root and rejects symlinks/`..`. Round 44: no action (frozen). | `[frozen44]` |
| R45-03 | P1 | The C2 freeze check enumerates 5 hard-coded paths + `tools/round-44`, not the claim's frozen set; six families (`plans/round-44-claims.md`, `corpus/SOURCES.md`, `tools/round-43/c1-counter.py`, carrier bins, oracle tree, a cited receipt) still score **exit 0 / met true** after a single post-freeze mutation. | `<LANE>/tools/round-44/c2-counter.py:134,455-456`; `<LANE>/tools/round-44/c2-rubric.json` `frozen_paths`/`frozen_dirs`; `w2/R44W2C2Freeze.md` §2-§3 (eight arms, six green); `w2/R44W2ScribeSources.md` D-1 | R44-CL7; C2Freeze F-1..F-5; ScribeSources D-1; Simplifier S-2 | lane r45 (rubric + claim) | The freeze set is derived from a machine-readable claim manifest, not hard-coded; an arm that rewrites only `plans/round-44-claims.md` (or only `corpus/SOURCES.md`, or `tools/round-43/c1-counter.py`) exits 2 with that path in `frozen_path_changed`; the 80/80-at-`55bcce69` receipt is unchanged. Round 44: no action. | `[frozen44]` |
| R45-04 | P1 | The round's own closing commit `8bb1090a` is a **second** freeze violation: C2 at the tip reports **9** `frozen_path_changed` paths, the 8 M44-2 files **plus `SCORECARD.md`**, because the appended `## Round 44` section exceeds the rubric's exact `expected_edits`; M44-2 names only the 8. | `<LANE>/SCORECARD.md:3519-3534` (blob at `8bb1090a`); `<LANE>/tools/round-44/c2-rubric.json` `expected_edits["SCORECARD.md"].note` ("cannot ALSO be appended"); this seat's C2-at-tip run: **exit 2**, 9 paths, stdout sha256 `0a81b8b2e85b08914b5a2f1b3856601f53d8c6f491ae5e00794c9bcf9a064c64`; `w2/R44W2C1ReceiptAudit.md` D3 | C1ReceiptAudit D3; C1Satisfy V9; (this seat) | lane r45 (record) + operator (rule) | The lesson names the ninth path (or the section is moved out of `SCORECARD.md` per the rubric's own note); a re-run at the closing commit shows either 8 paths with the section elsewhere, or 9 named in the record. Consider a new `M44-3` row. **Status at write: ADDRESSED by `923fa870`** — the committed lesson
now carries `M44-3` (naming the ninth path) and SCORECARD is restored; this seat re-ran C2 at
`923fa870`: **exit 2, 8 paths, `SCORECARD.md` absent**, stdout sha
`837052522731aaef0d938b30f7c21dcb116bcbd4961f3efb106425a1e1e6c7ca`
(`artifacts/R44W2ConnDefects/c2-at-923fa870.json`). Keep the row as the record of the 8bb1090a state. | |
| R45-05 | P1 | M44-2 understates what was changed: the 8 modified files are the **C1 control inputs**, re-captured post-freeze (evidence ids `ev_4d2155ed…`→`ev_03c9cdb3…`, provider ids `1239772:1`→`2463841:1`, `/tmp/rea-firmware-*`→`probe-v21` paths, pos entry 16880→20280 B); the committed `pos`/`c3` receipts describe the **post-freeze** bytes, so `CTL-C1-POS`'s `stdout_sha256 88900939…` has no reproducible input at the tip, and promotion prose persists inside the pos fixture tree. | `w2/R44W2SentScope.md` F4/F5; `w2/R44W2FreezeViolation.md` §5 FV-3; `w2/R44W2C1Rescore.md` D5; `w2/R44W2Quality77.md` D8; this seat: `git diff c86ea508^ c86ea508 -- tools/round-44/` (8 × `M`; provider-id diff); `<LANE>/.ufo/waves/round-44/controls/pos/receipt.json` `tree` vs frozen fixture | SentScope F4/F5; FreezeViolation FV-3; C1Rescore D5; Quality77 D8; C1Oracle? (control fixture evidence) | lane r45 (record) | The M44-2 row names the file class and the digest split; either the frozen fixture's sha256 equals the receipt's `tree` sha256 at the measured revision, or the record states which side is post-freeze and why; the pos fixture tree no longer carries promotion prose without a "fixture, not landing" marker. | |
| R45-06 | P1 | The C1 control evidence is unreproducible: 12 of 14 control receipts name `--rev` commits **absent** from the object DB, all 14 name deleted sandboxes, and the wave record and lane record are two different scoring runs of the same controls. | `<LANE>/corpus/evidence/round-44/controls/{c0..c5,pos}/receipt.json` (argv, `sandbox`, `tree`); `w2/R44W2SentScope.md` F1; `w2/R44W2C1Rescore.md` D6; `w2/R44W2C1PosArm.md` D4/D5; this seat: `git cat-file -e df4aa381…^{commit}` / `fdab6b7e` / `d73d0806` → all **ABSENT** | SentScope F1/F2; C1Rescore D6; PosArm D4/D5; C1Controls D-4 | lane r45 (controls) | For every control receipt: its `--rev` resolves with `git cat-file -e`, and its planted-tree digest equals the frozen fixture's digest (or a committed sandbox copy exists); a replay of one red arm and the green arm from the lane alone reproduces the recorded exit code. | |
| R45-07 | P1 | C2's coverage repair is freeze-scoped and false at REV: `SCORECARD.md:3513` appends `137/137`, but Command A over `55bcce69` derives **138/138**; the rubric scores the entry at `FREEZE_TREE`, and the lane's own Command A exits 1 at `55bcce69` with five mismatches, never disclosed. | `<LANE>/SCORECARD.md:3512-3513`; `<LANE>/tools/round-44/c2-rubric.json` entry `C2-a1-owned-coverage-count` `check_params.__SCORING_REV__ = FREEZE_TREE`; this seat's `command_a` at `55bcce69`: `{"mapped":138,"files":138,"value":"138/138"}` (stdout sha `cef5931f…8acf`), at freeze `137/137`; `w2/R44W2ScribeShonen.md` D3 (Command A exit 1, five mismatches) | (this seat); ScribeShonen D3; C2Freeze §1; ScoutDebt D-19 | lane r45 (calibration) | Either the appended correction carries an explicit `at c48f8a4b` qualifier, or the rubric scores `C2-a1` at REV and the counter still exits 0 with the value `138/138`; and the record contains one sentence naming Command A's five mismatches at `55bcce69`. | |
| R45-08 | P1 | The M44-2 "fix" is a detector, not a gate: nothing invokes it (`.git/hooks/` holds only samples; the lane is a **jj** repo so a git hook would not fire); the demonstrated pathspec covers 1 of 12 frozen families; the bare default false-reds; and the same gate **false-reds C2's admissible `SCORECARD.md` append**. | `<LANE>/tools/round-45/frozen-path-preflight.py:29-30,63,69`; `w2/R44W2Preflight.md` D-3; `w2/R44W2C2Freeze.md` F-6; `w2/R44W2Quality77.md` D2-D4/D6; `w2/R44W2Simplifier.md` S-2/S-3; `w2/R44W2Province.md` D6; `w2/R44W2Readme.md` D4; `w2/R44W2ScribeShonen.md` D4 | R44-CL1; Preflight D-3; C2Freeze F-6; Quality77 D2/D3/D4/D6; Simplifier S-2/S-3; Province D6; Readme D4; ScribeShonen D4; ConnSibling | lane r45 + operator (jj) | A jj-level commit gate (alias/hook) reads the pathspec vector from a machine-readable manifest derived from the claim, exits 1 on a claims-only commit and on `c86ea508`, exits 0 on `55bcce69` **and** on the C2 bound SCORECARD append at the same revision, and its receipt records argv, tool sha256 and a UTC instant. | |
| R45-09 | P1 | A frozen pathspec that matches nothing at FREEZE returns **exit 0 `clean`** — a typo in a hook's pathspec makes the gate permanently green. | `<LANE>/tools/round-45/frozen-path-preflight.py:67-79`; `w2/R44W2Preflight.md` D-1 (X1); `w2/R44W2Quality77.md` D4; `w2/R44W2C1Oracle.md` F5; `w2/R44W2C1ReceiptAudit.md` D6 | Preflight D-1; Quality77 D4; C1Oracle F5; ReceiptAudit D6 | lane r45 | `--pathspec frozen/nope --rev <violating>` exits **2** with `pathspec matches nothing at freeze`; the correct pathspec on the same rev still exits 1. | |
| R45-10 | P1 | The violating commit was made by the **fleet orchestrator's non-author lane sweep** at 10:43:43 (author stamp 09:57:16, 46 min after the round stopped), so a gate wired only into the round's commit sequence would not have fired; the report also says "13 commits" where the range holds 15. | `git show -s --format='%h author=%ad committer=%cd' c86ea508` → `author=09:57:16 committer=10:43:43`; `w2/R44W2RevAttempt1.md` RA-1/§2; `<LANE>/.ufo/reports/round-44/kaidoku.md:17,19,45-46`; `w2/R44W2Province.md` D5 | RevAttempt1 RA-1; Province D5; ConnSibling D4 | **operator** (fleet commit path) | The fleet sweep runs the frozen-path gate over every lane it commits (demonstrated by a fixture lane whose sweep commit is refused), and the report/LOG state content-by-round / commit-by-sweep with author and committer distinct. | |
| R45-11 | P2 | No worktree/dirty-tree arm: the frozen fixtures were dirty from 09:50:09, seven minutes before the honest stop, and no instrument can see an uncommitted change to a frozen path. | `w2/R44W2RevAttempt1.md` RA-2 (mtimes); `<LANE>/tools/round-45/frozen-path-preflight.py` (no `status` call) | RevAttempt1 RA-2 | lane r45 | With a frozen path modified but uncommitted, the gate exits 1; a fixture arm shows it, and the same tree committed is also exit 1. | |
| R45-12 | P2 | Gate and counters disagree on the predicate: gate flags `A` under a frozen dir, C1 ignores `A` when the path did not exist at FREEZE; mode-only changes are walk-only; the gate reds C2's bound append while C2 exits 0. | `w2/R44W2Quality77.md` D5; `w2/R44W2Preflight.md` D-4; `w2/R44W2Simplifier.md` S-2; `<LANE>/tools/round-44/c1-counter.py:1662-1666` | Quality77 D5; Preflight D-4; Simplifier S-2 | lane r45 | One predicate shared by gate and both counters; arms for `A`-under-frozen-dir, mode-only and bound-append return the same verdict from all three instruments. | |
| R45-13 | P2 | The C1 score receipt omits `counter_sha256_at_freeze` (required by the frozen claim) and any sha256 of the control receipts it cites; C2's receipt has both. | `<LANE>/.ufo/waves/round-44/l1/c1-score-at-55bcce69.json` keys (no `counter_sha256_at_freeze`); `<LANE>/plans/round-44-claims.md:85-87`; `w2/R44W2C1Oracle.md` F4; `w2/R44W2Quality77.md` D7; `<LANE>/tools/round-44/c1-counter.py` (`grep -c _at_freeze` → 0) | C1Oracle F4; Quality77 D7; (this seat) | lane r45 | A re-emitted C1 receipt carries `counter_sha256_at_freeze == git rev-parse c48f8a4b:tools/round-44/c1-counter.py` (`9f2cc140…a993`) and the sha256 of each cited control receipt. | |
| R45-14 | P2 | A green C1 score and a 754 KB C2 score sit inside the stopped claim's evidence directory with no status marker; the C2 score exists twice with different bytes. | `<LANE>/corpus/evidence/round-44/c1/counter-at-4cc1.json` (`met_target true`); `<LANE>/corpus/evidence/round-44/c1/c2-score-9d3d.json` vs `<LANE>/corpus/evidence/round-44/c2/c2-score-9d3d.json`; `w2/R44W2C1ReceiptAudit.md` D1; `w2/R44W2RevAttempt1.md` RA-5; `w2/R44W2Simplifier.md` §2.6 | ReceiptAudit D1; RevAttempt1 RA-5; Simplifier §2.6 | lane r45 | One authoritative C2 score path; the C1 directory contains only carrier receipts plus a README naming the stop, or the two score files are moved under `.ufo/…/l1/`. | |
| R45-15 | P2 | `SCORECARD.md` credits the C1 score to the C2-only commit `75a5cb42`, and the report parenthesises `9d3d1862` as if the C2 receipt measured `55bcce69`; the receipt measures `9d3d1862`. | `<LANE>/SCORECARD.md:3521`; `git show --name-only 75a5cb42` (one path); `<LANE>/corpus/evidence/round-44/c2/c2-score-9d3d.json` `revision`; `w2/R44W2RevAttempt1.md` RA-3/RA-4; `w2/R44W2ConnCross.md` D1/D2/D4 | RevAttempt1 RA-3/RA-4; ConnCross D1/D2/D4 | lane r45 | The record gives one exact pointer per receipt and revision; no receipt's revision is inferred from a nearby commit. | |
| R45-16 | P2 | Wave-1 evidence exists only at the violating commit: at `55bcce69` the wave-1 tree has 28 of 38 seat `.md` and **no** `r44-w1-results.json`, yet the record presents it as re-verified measured surface; results pins are stale (`c1-controls.py` `32003f28…` vs landed `b8c55f9b…`; entry-draft pin only true at `55bcce69`) and `receipts/selftest.json` is named but absent. | `w2/R44W2RevAttempt1.md` RA-6/§4-F; `w2/R44W2Wave.md` defects 1-3; `<LANE>/.ufo/waves/round-44/r44-w1-results.json` (added in `c86ea508`) | RevAttempt1 RA-6; Wave 1-3 | lane r45 | The lesson says "wave-1 outputs read at `c86ea508`; inputs, not claim evidence"; the two stale pins are corrected; the missing `selftest.json` is named. | |
| R45-17 | P2 | The lesson's S138 Gate row cites a manifest sha256 that exists nowhere (`4bc53dbb…c1a13`; actual `06a72dd5…8f5fe`), calls a two-directory `__output__` "1 token", breaks its own ≤25-word rule (29 words) and labels the grounds "12 words" (10/18). | `<LANE>/corpus/lessons/round-44.md:24`; `<LANE>/corpus/evidence/round-44/oracle/manifest.json` (sha256 `06a72dd5…`); `w2/R44W2Sources.md` defects 1-3; `w2/R44W2LessonGate.md` D1/D4/D5; `w2/R44W2Entry.md` D2 (entry `:12` same digest) | Sources 1-3; LessonGate D1/D4/D5; Entry D2 | lane r45 | `sha256sum` of the manifest equals the string in the lesson and the entry; the listing member count equals the live API response; the quote cell is ≤25 words or the rule is restated. | |
| R45-18 | P2 | The census paragraph says the **round-start** command yields 14 W04 with S138 the 14th "pre-existing"; the BASE tree yields **13** (S138 absent), and the cited round-end receipt plus the start replay are **untracked**. | `<LANE>/corpus/lessons/round-44.md:44-50`; `w2/R44W2Census.md` CENSUS-1/CENSUS-2; `w2/R44W2ScribeCensus.md` CEN-1/CEN-2; `w2/R44W2Simplifier.md` S-4; `w2/R44W2ConnSibling.md` D1; `git status --porcelain` shows `?? …/sources-census-end.txt`, `?? …/sources-census-start-replay.txt` | Census CENSUS-1/2; ScribeCensus CEN-1/2; Simplifier S-4; ConnSibling D1 | lane r45 | The paragraph states 13 at BASE → 14 at close, S138 as the new one; every cited census receipt is committed at the revision that cites it (or the citation is dropped). | |
| R45-19 | P2 | The carried-debt paragraph misstates three ids: D-27 is marked closed though only the receipt half of its exit fired; D-19's exit **did** fire and it is still listed open; D-24 is claimed mitigated but the rubric has no `source:` arm; prior-round ids are dropped/inflated. | `<LANE>/corpus/lessons/round-44.md:87-91`; `w2/R44W2ScoutDebt.md` defects 1-3 + table; `w2/R44W2LessonGate.md` D2/D11; `<LANE>/tools/round-44/c2-rubric.json` (no `source:` in check commands) | ScoutDebt 1-3; LessonGate D2/D11 | lane r45 | D-27 = open/exercised (no URL gate), D-19 = closed (receipts cited), D-24 = open; the 28 ledger ids appear exactly once and prior-round ids are neither dropped nor inflated. | `[debt]` D-19/D-24/D-27 |
| R45-20 | P2 | M44-1's row has its columns swapped: the *remediation* sits in `captured-by`, the *defect demonstration* in `fix (shown able to fail)`; no artifact anywhere refuses a URL cell without a committed 200 listing, so the fix is not shown able to fail. | `<LANE>/corpus/lessons/round-44.md:15`; `w2/R44W2LessonGate.md` D3; `w2/R44W2Entry.md` D5 (rootfs 404/empty-listing probes have no committed capture) | LessonGate D3; Entry D5 | lane r45 | The fix cell says "process only — no executable arm, D-27 open", or a URL-cell linter with one red control (a guessed URL) and one green control exists. | `[debt]` D-27 |
| R45-21 | P2 | C1 layout prose vs instrument: the claim names `compression_family` (exists in no instrument); the byte-20 gloss is exact only for LE (the token is a u16, BE reads the high byte); "32-byte superblock" contradicts `flags@36` and header extents 51/63; the flags-NOD-clear conjunct is unenforced; S119 is cited for unblob's struct but is the rea-agents tarball (S112 is right); `carriers.json` embeds `file(1)` output with no `file`/`magic.mgc` digest. | `<LANE>/plans/round-44-claims.md:40-47,134-135`; `<LANE>/tools/round-44/carriers.json:5,248,491,764,1098`; `<LANE>/tools/round-44/c1-counter.py:289-301,1074`; `w2/R44W2C1FileHazard.md` D1/D2/D3; `w2/R44W2C1Pins.md` D1-D4 | FileHazard D1/D2/D3; C1Pins D1-D4; R44-CL5/D-11 | lane r45 (prose + next freeze) | The next claim uses the field name the instrument computes, states the u16/endianness rule, states the true header extent, binds `flags` if it names it, cites S112 for the struct, and either digests `file`+magic or drops `file_verdict` from the frozen table. Round 44: no action. | `[frozen44]` |
| R45-22 | P2 | The CL6 statement omits the conditions that make `cmp -l` false-equal (pipe/regular-file/`/dev/full` stdout **and** equal-length inputs ≥4096 B) and calls 4096 B "the boundary case"; the agent shell shadows `/usr/bin/cmp` with a builtin that returns the correct 1, so a reviewer can observe the opposite; no executable guard enforces the ban. | `<LANE>/corpus/lessons/round-44.md:81-83`; `<LANE>/plans/round-44-claims.md:69-73`; `w2/R44W2C1CmpHazard.md` D1-D4 + advisory R1 (30-run matrix at 4096/4097/…/4 MiB) | R44-CL6; CmpHazard D1-D4 | lane r45 | The durable row states the destination matrix and the equal-length condition, names `/usr/bin/cmp`, and a preflight pattern rejects `cmp -l` in new/edited instruments. | |
| R45-23 | P2 | `/tmp` citations survive: a live empty `/tmp/kaidoku-r44`; the frozen `pos`/`c3` fixtures cite `/tmp/rea-firmware-*` at `55bcce69`; wave-1 receipts cite `/tmp` scripts/TSVs; the round-42 scratch root was deleted mid-audit; the C2 measured score embeds the deleted `/tmp/c2-counter.p_yfx2x5/repo` in **all 80** entry commands, and `c2-counter.py` falls back to `gettempdir()`. | `w2/R44W2Misroot.md` Defect 1; `w2/R44W2SentScope.md` F3/F5/F6/F7/F9; `<LANE>/tools/round-44/c2-counter.py:1205-1207`; `<LANE>/.ufo/waves/round-44/l1/c2-score-at-55bcce69.json` `entries[*].command[7]`; this seat: `test -d /tmp/kaidoku-r44` → exists | Misroot 1; SentScope F3/F5/F6/F7/F9; R44-SCR-TMP/R44-REAP | lane r45 + operator (cleanup) | No committed score/control receipt contains a `/tmp` path; `c2-counter.py`'s fallback is the declared segment; `/tmp/kaidoku-r44` is gone; a re-emitted C2 receipt's every command names a re-derivable path. | `[debt]` R44-SCR-TMP/R44-REAP |
| R45-24 | P3 | C1 control documentation misstates its own arms: CTL-C1-1's stated reason includes `layout_ok` (true on every carrier), CTL-C1-4's `evidence_id_ok` (true on every carrier), the c4 note names a `corpus/` predicate that `provenance_ok` never checks, the POS docstring says "evidence path" while writing scratch, and there is no per-binding fitness arm. | `w2/R44W2C1Controls.md` D-1..D-4; `w2/R44W2C1PosArm.md` D5; `<LANE>/tools/round-44/c1-controls.py:29,640,675,795-797,929-933,1015-1080` | C1Controls D-1..D-4; PosArm D5 | lane r45 | Each control's stated reason lists only bindings that actually go false; each control has a one-binding mutation witness; the POS docstring describes the scratch path it writes. | |
| R45-25 | P3 | `QUALITY.md` now has **two "Row 77"** criteria (line 85 is the round-36 rule cited by row 81; line 139 is the new gate); the new row claims "at commit time" though the tool runs only on an existing revision and was committed after `c86ea508`; it duplicates row 79's authority without naming the extension; its receipts lack argv/tool sha256/UTC. | `<LANE>/corpus/QUALITY.md:85,139`; `w2/R44W2Quality77.md` D1/D2/D3/D6 | Quality77 D1/D2/D3/D6 | lane r45 | The new criterion is renumbered (86/87), its timing wording matches the tool, it says "extends 79", and its receipt carries argv + tool sha256 + UTC. | |
| R45-26 | P3 | CTL-C2-0 is not reproducible as written: with the round's freeze supplied (`--rev BASE --freeze c48f8a4b --pre-freeze`) the counter exits **2** `frozen_path_changed` on the rubric with 0 entries; the receipt used `--freeze BASE` and a rubric file copy. | This seat: C2 pre-freeze run → exit 2, `frozen_path_changed ["tools/round-44/c2-rubric.json"]`, `entries_evaluated 0`; `<LANE>/.ufo/waves/round-44/w1/artifacts/R44C2Controls/receipts/real-base/CTL-C2-0.json` (argv `--freeze c29360e3`, `rubric_source file`); `<LANE>/tools/round-44/c2-counter.py:39-42` | (this seat) | lane r45 | The claim/receipt names the exact CTL-C2-0 argv and the rubric source; a replay with the round's freeze either yields the 3-mismatch census or is documented as the expected exit-2 stop. | |
| R45-27 | P2 | The C2 sentinel B2 and `pin_rev` rule are implemented nowhere: `asserted_not_in_base_line`, `line_sha256`, `line_at_base` appear in no counter and in no check script; the rubric carries dead fields. | `w2/R44W2C1ReceiptAudit.md` D4; `<LANE>/tools/round-44/c2-counter.py` (`grep -c line_sha256` → 0); `<LANE>/tools/round-44/c2-rubric.json` entries carry `line_at_base`/`line_sha256`/`pin` | C1ReceiptAudit D4 | lane r45 | Either the counter implements the B2 guard centrally (a wrong `asserted` exits 2 with `asserted_not_in_base_line`), or the claim text describes the guard that exists. Round 44: no action. | `[frozen44]` |
| R45-28 | P2 | The rubric's `dropped` (10 rows) and `inventory` blocks are documentation only: the counter reads only `ENTRY_LIST_KEYS`, so the claim's "no mismatching row may be dropped without an exact disposition" has no instrument. | `w2/R44W2Simplifier.md` S-1; `<LANE>/tools/round-44/c2-counter.py:150,343-357`; `<LANE>/tools/round-44/c2-rubric.json` `dropped`/`inventory` | Simplifier S-1; ScoutDebt D-15 | lane r45 | A dropped row whose `not-checkable-because` is absent exits 2; the disposition list is read by the counter. | `[debt]` D-15 |
| R45-29 | P2 | Unbound/unsafe path surfaces in C1: the committed run manifest/provenance/run.json/extract-tree are opened by no clause (rewriting every manifest path leaves the result identical); `oracle.tool` is an absolute path from the frozen table that the counter executes; a malformed carrier table exits 1, not 2; the c2 rubric path fields accept absolute and `..` spellings. | `w2/R44W2SentEnvelope.md` D-4/D-5/D-6/D-7; `<LANE>/tools/round-44/c1-counter.py` (no manifest open); `<LANE>/tools/round-44/c2-rubric.json` path fields | SentEnvelope D-4/D-5/D-6/D-7 | lane r45 | The manifest is bound by a digest clause (rewriting a path reds); `oracle.tool` must be under the pinned toolchain digest or rejected; malformed frozen tables exit 2; rubric paths are normalized and relative. | |
| R45-30 | P3 | C1 entry precision: two `mkfs_time` cells are local time labelled `Z` (3 h early); the v2ns no-reader and rootfs-probe measurements carry no receipt pointer/capture; the control-clone evidence path is not given; the entry cites the superseded `4cc1ac11` receipt as its only counter result. | `<LANE>/corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:76-79,179-190,26-29`; `w2/R44W2Entry.md` D3/D4/D5/D7 | Entry D3/D4/D5/D7 | lane r45 | The entry's timestamps are UTC or unlabelled; each measurement cites a seat receipt path that resolves; the measured-revision receipt is the primary cite. | |
| R45-31 | P3 | Wave-shape accounting is quoted unqualified: wave-1 attack share is 8/37 = **21.6 %** under the policy's own 25 % floor (round 31.6 %); joins must key on the spec id (8 suffixed retries); `w1/` holds 38 `.md` for 37 seats; `.ready.dispatched` stamps are host-local; wave-2 results were absent at annex. | `w2/R44W2ScribeSeats.md` F1-F5; `<LANE>/.ufo/waves/round-44/{w1,w2}-spec.json` | ScribeSeats F1-F5 | **operator** | The round report quotes both shares and the spec-id rule, names the non-seat `.md`, labels the stamps, and either ships `r44-w2-results.json` or says "pending". | |
| R45-32 | P3 | The lane worktree is on a **detached HEAD** (a landing commit does not advance `main`), and the fleet adjacency registry still pins kaidoku at round 35. | `w2/R44W2ConnSibling.md` D3/D6; this seat: `git rev-parse --abbrev-ref HEAD` → `HEAD` | ConnSibling D3/D6 | **operator** | `git symbolic-ref -q HEAD` names a branch at round-45 start; the adjacency row names round 44. | |
| R45-33 | P3 | The record under review has two states at once: `corpus/lessons/round-44.md`, `LOG.md` and `SCORECARD.md` are modified in the worktree during wave 2, so a reader can quote either the committed `8bb1090a` text or the uncommitted edit. | This seat: `git status --porcelain` → ` M LOG.md`, ` M SCORECARD.md`, ` M corpus/lessons/round-44.md`; `git diff -- corpus/lessons/round-44.md` (32 insertions / 6 deletions); `w2/R44W2ConnSibling.md` D7 | ConnSibling D7; (this seat) | lane r45 | The wave-2 record edits are committed before filing, and the report names the revision it read.
**Status at write: partially resolved** — `923fa870` committed LOG/SCORECARD and the lesson, but a
7-line lesson addition (`R44-CL9`, citing this file's R45-07) was still uncommitted at the final read. | |

## 2b. Late-merged reports (five peers landed after the first table pass)

Status updates to earlier rows, from the late reports: **R45-04** — the L1's uncommitted worktree
edit already adds an `M44-3` row (`w2/R44W2Axes.md` §"The record says exactly that"); verify it names
the ninth path (`SCORECARD.md`) and does not attribute it to `c86ea508`. **R45-05/R45-06** —
`w2/R44W2C1HonestStop.md` HS-8 adds that the `c3`/`pos` receipt `tree` digests disagree with **both**
the freeze fixture and the post-freeze fixture, so the control evidence matches neither side.
**R45-07** — `w2/R44W2C2Corrections.md` C-3 independently measures the same freeze-scope blindness.
**R45-01** — `w2/R44W2Axes.md` "D-AXES-4" and `w2/R44W2C1HonestStop.md` HS-2/HS-3 repeat the
causality finding and confirm PROVINCE/README/entry state the wrong cause.

| id | severity | defect (one line) | evidence path (resolves at snapshot) | sources merged | owner | falsifiable exit condition | flags |
|---|---|---|---|---|---|---|---|
| R45-34 | P1 | The frozen claim's B2 gate is unimplemented **and incompatible with its own rubric**: `asserted` is not a substring of `line_at_base` for **71/80** entries, including all three targets (`137/137` vs base `133/133`; `21/21` vs `20/20`; `81-543` vs `81-449`), so under the claim's literal rule the frozen rubric would exit 2 on itself. | `w2/R44W2C2Vacuity.md` D1 (B2 audit, 71 offending entries, exit 0); `w2/R44W2C2Corrections.md` C-2; `w2/R44W2C1ReceiptAudit.md` D4; `<LANE>/plans/round-44-claims.md:213-216`; `<LANE>/tools/round-44/c2-rubric.json:388,438,538` | C2Vacuity D1; C2Corrections C-2; ReceiptAudit D4 (extends R45-27) | lane r45 (claim + rubric, next freeze) | The next rubric satisfies its own B2 rule (every `asserted` a substring of the base line) or the claim drops B2; a pre-freeze audit runs the rule over every entry and reports 0 violations. Round 44: no action. | `[frozen44]` |
| R45-35 | P1 | The three target entries **do not check the statement they repair**: each overrides the row-derived value with the appended `c2-correction-value`, so mutating the `## Owned axes` number leaves the entry green; only the correction line is load-bearing. | `w2/R44W2C2Vacuity.md` D2 (a1/a2/a4 prose-value mutations: a1 stays match; a2/a4 red other ids only); `w2/R44W2C2Corrections.md` §1 ("a1 confirmed only at its declared anchor"); `<LANE>/tools/round-44/c2-rubric.json` payloads for `C2-a1/a2/a4` (`eff = correction(...); stated = eff`) | C2Vacuity D2; C2Corrections §1 (extends R45-07) | lane r45 (calibration) | Mutating the row's number at REV reds the entry that claims to repair it (same id), with the correction block absent; and the record says the entry is checked at the row, not at the note. | |
| R45-36 | P2 | Six rubric entries are **green generators**: `observed` is the literal string `"steered"` (equal to `asserted`) and the counter never compares the check's `derived` field, so an entry stays green while its own check reports the declaration absent. | `w2/R44W2C2Rescore.md` D-1 (mut3 `c0742325…`: `C2-g1` match true, `derived steered-declaration-absent`); `<LANE>/tools/round-44/c2-rubric.json` entries `C2-g1,g4,g5,g6,g7,g8`; `<LANE>/tools/round-44/c2-counter.py:1253` | C2Rescore D-1; ScoutDebt D-22 | lane r45 (instrument, next freeze) | A check that emits `derived` has it compared with `asserted`; a bare literal `observed` equal to `asserted` is rejected; mut3 reds `C2-g1`. Round 44: no action. | `[frozen44]` |
| R45-37 | P2 | `C2-h1` is inert at REV (`observed := derived`) and pinned `HYAKU_FREEZE` although the claim says README checks re-derive at REV; deleting the whole `## Coverage map` section still yields exit 0 / `mismatches []`. | `w2/R44W2C2Vacuity.md` D3; `<LANE>/tools/round-44/c2-rubric.json:4563` region; `<LANE>/plans/round-44-claims.md:234-237` | C2Vacuity D3 | lane r45 | Deleting the README coverage-map section at REV reds `C2-h1`; the pin matches the claim's stated evaluation revision. | |
| R45-38 | P2 | Pinned entries (`C2-b1/b2/b3/b9`) read the **REV** statement and compare it with the **pinned** derivation, the inverse of the claim's `evaluate_at = pin` rule; the first round that legitimately refreshes `## Owned axes` turns them red on unchanged history. | `w2/R44W2C2Vacuity.md` D4 (`C2-b1` → `UNSUPPORTED:133/997` after a row mutation; `C2-b9` → `UNSUPPORTED:81-448`); `<LANE>/plans/round-44-claims.md:218-220` | C2Vacuity D4 | lane r45 | A refreshed current row leaves every `b*` entry green while the pinned statement at its pin still matches; or the claim states the actual comparison. | |
| R45-39 | P2 | The fitness claim "80/80 fails_as_required" is measured in a mode that **redefines the freeze** (`rev = freeze = mutant`) and is contaminated at `55bcce69` (a1/h1 red unconditionally); in the **scoring** configuration entry-level detection is unreachable — the frozen-path check returns exit 2 before the entry loop, so 77/80 statement mutations produce 0 entries and no failing id. | `w2/R44W2C2Vacuity.md` D5/D6; `<LANE>/tools/round-44/c2-counter.py:1199,1228`; `<LANE>/tools/round-44/c2-rubric.json:213` | C2Vacuity D5/D6 | lane r45 | In the scoring configuration, a mutated statement produces a failing id (not exit 2 with 0 entries); the fitness receipt names the mode and shows it is not the scoring mode. | |
| R45-40 | P3 | `claim_score` reads `true` on an exit-2 receipt (top level and `claim_gate`) while `usable_as_claim_score` is false — a grep trap for a reader. | `w2/R44W2C2Rescore.md` D-4; `<LANE>/tools/round-44/c2-counter.py:1052`; `<LANE>/.ufo/waves/round-44/l1/c2-score-at-tip.json` | C2Rescore D-4 | lane r45 | `claim_score` is derived from `usable_as_claim_score`/outcome, or renamed; an exit-2 receipt no longer carries a true `claim_score`. | |
| R45-41 | P2 | `SCORECARD.md:3526` points the C2 base census at `.ufo/waves/round-44/controls/c2/receipt.json`, which is **CTL-C1-2**, a C1 fabrication control, not a census. | `w2/R44W2C2Corrections.md` C-7; `<LANE>/SCORECARD.md:3526`; `<LANE>/.ufo/waves/round-44/controls/c2/receipt.json` (`claim: R44-C1`, `control: CTL-C1-2`) | C2Corrections C-7 | lane r45 | The pointer resolves to a C2 census (`base-census-summary.json` / `census-base.json`) or is re-aimed in an appended correction. | |
| R45-42 | P2 | The `## Owned axes` `Last-change` cells are stale (coverage omits round 41; depth omits rounds 31 and 41) and the class is named by no rubric entry and no `dropped` id, so the claim's "all other candidates are dispositioned by id" does not cover it. | `w2/R44W2C2Corrections.md` C-5; `<LANE>/SCORECARD.md:23-24,3464`; `<LANE>/plans/round-44-claims.md:204-205`; `w1/R44C2SentReview.md:23,48` (TRI-1..TRI-3) | C2Corrections C-5; w1 R44C2SentReview TRI-1..3 | lane r45 | The cells name every refresh round, or the class is in `dropped` with an exact `not-checkable-because`; the census is re-run over all 80 + dropped ids. | |
| R45-43 | P2 | Two frozen C2 clauses are not the implemented semantics: the "exact bytes" append binding is line identity (a trailing-space probe returns `bound_edit` while `blob_FREEZE + append` ≠ `blob_REV`, 667 vs 668 B), and `note_value_disagrees` is not a verdict the counter can emit (the wrong-note arm exits 2 `frozen_path_changed`). | `w2/R44W2C1HonestStop.md` HS-4/HS-5; `<LANE>/tools/round-44/c2-counter.py:572-579`; `<LANE>/plans/round-44-claims.md:239-240,228-230,256` | C1HonestStop HS-4/HS-5 | lane r45 (claim + counter, next freeze) | The next claim states line identity (or the counter compares `append_text` with the separator); the named note verdict exists or is removed. Round 44: no action. | `[frozen44]` |

## 3. Items that are open debt ids, not new defects (do not renumber)

These were carried as `D-nn` in `<LANE>/.ufo/waves/round-44/w1/R44Debt.md` and re-derived by
`w2/R44W2ScoutDebt.md` (state: 1 closed, 9 exercised, 18 open). Round 45 must close or carry them by
id; none becomes a new row above.

| debt | state | why it is not a new row | round-45 exit |
|---|---|---|---|
| D-13 | open | R44-CL3 and `w2/R44W2C1PosArm.md` D1 confirm it: `projection_ok` proves projection equality, not authorship; an authored projection-matched envelope passes all 22 carrier clauses (v1be in `d503bc7e`). | A provenance-bearing run artifact the counter cannot synthesize, or a decision that provenance is out of scope. |
| D-15 | open | The 80-entry rubric scores 77 excluded rows and 3 targets; `w2/R44W2C1ReceiptAudit.md` §4 shows the aggregate is not vacuous, but the claim-text census is the debt. | The claim text states the covered-category census (CL4), not only the instrument. |
| D-16 | open | "check-pass ≠ truth" — `SCORECARD.md`'s corrected coverage value is a case (R45-07). | Per-check "proves / does not prove" field or a semantic control. |
| D-17 | open (realized) | R45-35 measures the note-over-value: the appended correction is load-bearing and the statement it repairs is not checked. | The check reds when the statement is mutated, correction absent. |
| D-21 | exercised | Rubric admissibility: R45-34 (B2 71/80) and R45-39 (fitness measured in a non-scoring mode) are the concrete instances. | A rubric audit at freeze that runs the claim's own rules over all entries. |
| D-22 | exercised | R45-36: the `steer` hatch is a green generator for six entries; the marker need not cite a resolving receipt. | Marker must cite a resolving receipt path, and the entry reds without it. |
| D-11 | exercised | `file(1)` is not the probe; the counter binds compression from the metadata block (`w2/R44W2C1FileHazard.md` §4). Precision defects are R45-21. | A `file`-independent live assertion, or retirement of the row. |
| D-19 | **should close** | BASE 3 mismatches → REV 0 is exactly the exit (`w2/R44W2ScoutDebt.md` defect 2). | Mark closed in the round-45 carry list. |
| D-24 | open | The rubric has no `source:` arm; the claim sentence overstates (`w2/R44W2ScoutDebt.md` defect 3). | A map row bound to its stem's `source:` that reds when wrong. |
| D-27 | open | Only the receipt half of the exit fired; no URL gate (`w2/R44W2ScoutDebt.md` defect 1, `w2/R44W2LessonGate.md` D3). | A URL-cell linter with a red control on a guessed URL. |
| D-01..D-08, D-10, D-14, D-17, D-18, D-20, D-22, D-23, D-25, D-26, D-28 | open/exercised per ScoutDebt | Their exits did not fire; restating the limit is not exercise. | As written in `w1/R44Debt.md`. |
| R44-SCR-TMP / R44-REAP | open | The `/tmp` citations (R45-23) are instances, not a new class. | No `/tmp` in committed receipts; counter fallback anchored. |
| R36-CL5, R40-CL2, R41-CL3, R42-CL1/CL2, R43-CL1..CL4 | unchanged | Prior-round routed ids; no round-44 evidence closes them. | Carry by id. |

## 4. Items that would move a frozen 44 byte — next round only, never this round

`R45-02`, `R45-03`, `R45-21`, `R45-27`, `R45-34`, `R45-36`, `R45-43` all require edits to
`plans/round-44-claims.md`, `tools/round-44/**` or `tools/round-44/c2-rubric.json`; `R45-04`/`R45-05`
concern bytes already frozen and changed. **No row above authorises a round-44 edit.** The rule the round itself froze —
no commit in `FREEZE..REV` touches a frozen path — would make any such edit a fresh M44-2-class
violation, and a later restore does not un-block. The correct vehicle is the round-45 freeze: land
the predicate, rubric and gate *there*, with the pathspec vector derived from the claim, and keep the
round-44 measured revision `55bcce69` as the only admissible score.

## 5. What this seat confirms (no defect) — so round 45 does not re-open it

- **C1 carrier result.** 4/4 matched, every oracle regular file published at its exact relative path
  with matching sha256/size, `gaps == []`, `unpublished_entries == []`, handler exact, evidence id
  recomputed, projection equal. Independent reruns: `w2/R44W2C1Oracle.md` (12/12 checks),
  `w2/R44W2C1ReceiptAudit.md` (verdict table 1-5), `w2/R44W2C1Pins.md` (pins decoded).
- **C2 aggregate.** 80/80 at `55bcce69`, exit 0, `frozen_path_changed []`; base census red with the
  three target ids. The *composition* is not clean: six entries are green generators (R45-36), the
  three target entries are note-driven (R45-35), and 71/80 violate the claim's B2 rule (R45-34). The
  aggregate survives; it does not certify 80 checked statements.
- **M44-2 detection.** `tools/round-45/frozen-path-preflight.py` reds `c86ea508` (8 paths) and greens
  `55bcce69`; byte-identical to the committed receipts (this seat's shas match Preflight's).
- **Registry.** `corpus/SOURCES.md` is a pure append of S138/S139 (3 insertions, 0 deletions, 0
  changed cells); 137 → 139; blob identical at freeze/measured/tip; census exit 0.
- **Toolchain.** No install or upgrade in round 44; live `unsquashfs`/`7z`/`unblob`/`sasquatch`
  digests equal the frozen `carriers.json` toolchain; no pacman transaction on 2026-10-28.
- **Assimilation.** `Assimilation: none` confirmed; quarantine slice byte-identical to round 43; S150
  refused; S113 not adopted; `considerthese/` absent.

## 6. Contradictions stated, not smoothed

1. **"Unsatisfiable" vs H2.** R44-CL2's opening sentence and `w2/R44W2C1Satisfy.md` V5 cannot both be
   true; H2 is a scored counterfactual (exit 0). The accurate statement is *unrealized by this
   round's receipts*, and the fix is a provenance-spelling decision plus an anchored predicate.
2. **"Only correct reading" vs `4cc1ac11`.** The same frozen counter met the same receipts at
   `4cc1ac11`; the stop is a text-level override, and the record must say so wherever it states the
   exit code.
3. **"The tip red is `c86ea508`'s 8 files" vs the C2 9-path list.** `8bb1090a` adds `SCORECARD.md`;
   both facts are in the repo and the record currently carries one.
4. **"The fix catches it" vs "the fix would block C2's own repair".** The gate and C2 disagree in
   both directions; one predicate is needed before it is wired.
5. **"Honest and sufficient" vs the control-input re-capture.** The violation is disclosed; what it
   changed (evidence ids, provenance roots, a fixture document) is not.

## 7. This seat's receipts

All commands from `<LANE>`; no mutating git/jj; scratch
`/fast/scratch/hyaku/kaidoku-r44/R44W2ConnDefects` (removed at exit; artifacts copied to
`<LANE>/.ufo/waves/round-44/w2/artifacts/R44W2ConnDefects/`).

| # | command | exit | stdout sha256 | wall |
|---|---|---|---|---|
| 1 | `python3 -I -B tools/round-44/c1-counter.py --root . --rev 55bcce69… --freeze c48f8a4b… --pkg65 <rea-agents 6.5.0> --work <S>/final/work-c1 --json-out <S>/final/c1-at-55bcce69.json` | **1** | `eea45d374bb450f15c549ca5e7c7803ac9e6c31bb982fae45d6542ee8cac9f8d` | 7.54 s |
| 2 | `python3 -I -B tools/round-44/c2-counter.py --root . --rev 55bcce69… --freeze c48f8a4b… --work <S>/final/work-c2 --json-out <S>/final/c2-at-55bcce69.json` | **0** | `dd7c529bb6340c364854093937bce3d90ec980ebdea951263bb38dc52316a9b3` | 4.73 s |
| 3 | `python3 -I -B tools/round-44/c2-counter.py --root . --rev 8bb1090a… --freeze c48f8a4b… --work <S>/final/work-c2tip --json-out <S>/final/c2-at-tip.json` | **2** | `0a81b8b2e85b08914b5a2f1b3856601f53d8c6f491ae5e00794c9bcf9a064c64` | 0.10 s |
| 4 | `python3 tools/round-45/frozen-path-preflight.py --root . --freeze c48f8a4b… --rev c86ea508… --pathspec tools/round-44` | **1** | `20a87d4d81eedaa79defea6c0fcbbe248bd415e35460b48dd6b66fffe0a28896` | 0.10 s |
| 5 | same, `--rev 55bcce69…` | **0** | `c8a03c2673a9bfd52b23077a604e48288e44c70ff5cedd5782bc4fa6430a870f` | 0.10 s |
| 6 | `python3 -I -B tools/round-44/c2-counter.py --root . --rev c29360e3… --freeze c48f8a4b… --pre-freeze` | **2** | (see R45-26) `frozen_path_changed ["tools/round-44/c2-rubric.json"]`, 0 entries | 0.1 s |
| 7 | `python3 <S>/final/command_a.py . 55bcce69…` (the rubric's own `command_a` body) | **0** | `cef5931f2a68869589acea0bad6862d22e5b21eddd45e5881207020cdade8acf` — `138/138`, `21/21` | 0.9 s |
| 8 | `sha256sum corpus/evidence/round-44/oracle/manifest.json` | **0** | `06a72dd5b660c79adae943917abf40c24ab16554ec6c2f14985958799a78f5fe` | 0.00 s |
| 9 | `git show -s --format='%h author=%ad committer=%cd' c86ea508` | **0** | `author=09:57:16 committer=10:43:43` | 0.00 s |
| 10 | `git cat-file -e <ctl-rev>^{commit}` for `df4aa381`, `fdab6b7e`, `d73d0806` | **1** | all three absent | 0.02 s |
| 11 | `python3 -I -B tools/round-44/c2-counter.py --root . --rev 923fa870… --freeze c48f8a4b… --work <S>/w --json-out <A>/c2-at-923fa870.json` | **2** | `837052522731aaef0d938b30f7c21dcb116bcbd4961f3efb106425a1e1e6c7ca` — 8 paths, `SCORECARD.md` absent | 0.12 s |

Machine-readable copies: `<LANE>/.ufo/waves/round-44/w2/artifacts/R44W2ConnDefects/` (three counter JSON receipts, five stdout captures, `command_a.py` + its two outputs,
`w2-snapshot-list.txt` (first pass, 34), `w2-snapshot-list-final.txt` (40), the
post-remedy `c2-at-923fa870.{json,stdout}`, and
`sha256-manifest.txt` covering all of them). The `/tmp` paths named in R45-23 are **defect locations**, never evidence for
a claim; no artifact of this seat was written under `/tmp`, and none is cited from there.

## 8. Cleanup

Scratch `/fast/scratch/hyaku/kaidoku-r44/R44W2ConnDefects` (clone-free: counters ran against the
lane read-only with `--work` under scratch; two tiny fixture files under `cmp/`; no `/tmp` path
created, none cited). Removed with `rm -rf -- "$S"` before yield; verified absent. No tool was
installed or upgraded. No lane production file was written except this report and its artifacts
directory.
