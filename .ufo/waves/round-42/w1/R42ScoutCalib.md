# R42ScoutCalib — calibration pre-check of SHONEN.md and SCORECARD.md at `c4a38ea2`

**DEFECTS FOUND** — of ~95 checkable assertions in SHONEN.md (all 4 `asserted:` bullets), SCORECARD `## Owned axes`, `## Capabilities` and `## Round 41`, every commit hash (37/37 resolve to commits, all ancestors of base), every count from command A/B, every selftest count, every score-receipt number and every cited path that is a file at base **match**. The mismatches are 12 pieces of debt (§2), none an outcome-changing falsehood in a count, all of the kind the round-42 landing will grow if it follows the round-41 landing pattern (ranges that go stale when SKILL.md/PROVINCE.md change, pointers left behind, a placeholder, a stale column). One additional defect is in the **draft** `plans/round-42-claims.md` (§3, D-L): its R41-CL4 sentence is false against the frozen v3 interpreter.

Base `c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c` (`git cat-file -t` → commit; lane HEAD `fdabdfa4`; `git diff --stat c4a38ea2 HEAD -- SHONEN.md SCORECARD.md SKILL.md PROVINCE.md LOG.md corpus/README.md corpus/knowledge corpus/QUALITY.md tools` is empty, so base == HEAD for every checked file). All reads via `git show c4a38ea2:<path>`; runs in a `git clone --shared` sandbox checked out at base (scratch removed). No VCS mutation, no extractor on any published image (none was run).

Artifacts (`.ufo/waves/round-42/w1/artifacts/R42ScoutCalib/`): `command-a.py` (SCORECARD command A verbatim), `command-a-results.txt`, `command-b.json`, `skill-ranges.txt`, `path-existence.txt` (101 cited paths, 97 OK, 4 parser artefacts explained below), `probe-v3-legacy.{py,out}`, `draft-citations.txt`.

## 1. Table: location | asserted | observed | match?

Line refs are base lines. "S" = SHONEN.md, "SC" = SCORECARD.md.

### SHONEN.md

| location | asserted | observed | match? |
|---|---|---|---|
| S:6 | `SKILL.md:81-449` craft section, 20/20 rule blocks with resolvable citations, at `e1c83313` | craft heading line 81; next `## ` heading at 454 (`## Config custody…`); last non-blank before it 449. Command A at `e1c83313` and at base: `citation_resolved_rules 20 rule_blocks 20 depth_score 10.0` | yes |
| S:6 | rule block 20 triage table v3 at `SKILL.md:387-449` | block 20 starts 387, last non-blank 449; marker `<!-- sqfs-triage-table v3 -->` at 434 | yes |
| S:6 | R41-C2 stopped on a counter key mismatch, table unscored | `c2-at-e9a24d07.json`: `matched 52`, exit 1, `bindings_false ['observed_features_match_declared']` | yes |
| S:6 | 19/19 at `4d62ee5a` | command A at `4d62ee5a`: 19/19 | yes |
| S:6 | block 19 / table v2 at `SKILL.md:348-375` | at `4d62ee5a`: block 19 start 348, last non-blank 375 (yes). **At base** block 19 is 351-385 (+3 start, +10 length) | yes at the named commit; **stale as a present-tense pointer** (D-E) |
| S:6 | `tools/round-40/sqfs-triage-v2.py --selftest` 45 cases | base clone: `SELFTEST cases=45 pass=45 fail=0`, exit 0 | yes |
| S:6 | 18/18 at `52b0eb29` | command A at `52b0eb29`: 18/18 | yes |
| S:6 | block 18, marker v1, eight labels, `SKILL.md:316-343` | at `52b0eb29`: block 18 316-343, marker v1 at 333, 8 table rows/labels. **At base** block 18 is 316-349 | yes at the commit; stale as present-tense (D-E) |
| S:6 | `tools/round-39/sqfs-triage.py --selftest` 35 cases, artifact `…R39W2C2Rescore/sqfs-triage-selftest.txt` | base clone: `cases=35 pass=35 fail=0`; the artifact exists and ends `SELFTEST cases=35 pass=35 fail=0` | yes |
| S:8 | R41-C1 met 4/4 at `e9a24d07`; 5490 wrapper, 5491 nested rootfs, 6349 files | `c1-at-e9a24d07.json`: `carriers_matched 4 target 4 exit_code 0 met_target true`; `oracle_files` V3 8, V4 6349, L3 13, L4 14 | yes |
| S:8 | `corpus/evidence/round-41/c1/`, LOG round-41 entry, `.ufo/waves/round-41/w2/R41W2Repro*.md` | all exist at base (LOG.md:3164; ReproL/V3/V4 — three reports, each reads CONFIRMED, together covering V3, V4, L3, L4) | yes |
| S:8 | round 40: receipts `corpus/evidence/round-40/c1/`, `R40W2Repro*.md`, "honest stop at 3/4" | paths exist; `c1-at-42c10a58.json` `carriers_matched 3 target 4 exit 1` | yes |
| S:8 | round 39: six frozen carriers (gzip and xz), receipts `K{1..6}/`, counter 6/6 at `6fdaf4f1`, re-runs in `.ufo/waves/round-39/w2/`, `corpus/lessons/round-39.md` | K1-K6 `after.json` + `run.json` all in tree; `c1-at-6fdaf4f1.json` `carriers_matched 6 target 6 met_target true`; carriers.json mentions gzip (×3) and xz (×1) | yes (the `K{1..6}` flag in my path scan is a brace-range parser artefact) |
| S:10 | r40 table v2: 26 of 26 held-out, seed = freeze hash; `R40W2C2IndepEval.md` | `c2-at-42c10a58.json` `matched 26 n 26 exit 0`; r40 manifest `seed 7fce3086…` == freeze commit `7fce3086`; IndepEval reads "26/26, no disagreement" | yes |
| S:10 | r39: 20 of 20 held-out, seed = freeze hash; selftests 35/35 and 27/27; ten generator classes; smallest table 8 rows / 7 cells | `c2-at-6fdaf4f1.json` `matched 20 n 20`; r39 manifest seed `8fcda41c…` == freeze commit, `classes` list of 10, 20 carriers; `tools/round-39/c2-counter.py --selftest` 27/27; `sqfs-triage.py` 35/35; `R39W2C2Shortcut.md` "8 rows, 7 non-`*` cells" | yes |
| S:12 | `PROVINCE.md:97-125` Adjacent list; safety refusal `:116-118`; tooling bullet `:119-125`; installer `:110-115`; "byte-identical at `52b0eb29`" | 97 `## Adjacent`; 110-115 "Installing engines…never runs the installer"; 116-118 "Quality/safety verdicts…"; 119-125 "Tooling, dated 2026-10-26…". sha256 of lines 97-125 identical at `52b0eb29`, `4d62ee5a`, `e1c83313` and base (`f1a5cfc6…`) | yes |
| S:12 | round-39 additions `PROVINCE.md:378-384` (row `:382`, frontier note `:384`) | 378 `## Round-39 additions to Core`; 382 row `squashfs_v4_be`; 384 frontier note | yes |
| S:12 | round 40 block and note `PROVINCE.md:386-394` | 386 `## Round-40 measured, not promoted…`; 394 frontier note | yes |
| S:12 | `PROVINCE.md:157` and `:376` carry a dated round-39 pointer | 157: "Round 39: standard BE v4 is Core — see `## Round-39 additions to Core`"; 376: "Round 39: superseded for standard big-endian v4…" | yes |
| S:12 | (omission) the box describes PROVINCE only to round 40 | `## Round-41 additions to Core` is `PROVINCE.md:396-408` and is not mentioned; `:157` still ends "AVM-BE and vendor-mangled stay here" with no round-41 pointer | not a range mismatch; **omission + stale sentence** (D-A) |

### SCORECARD.md `## Owned axes` (lines 19-32)

| location | asserted | observed | match? |
|---|---|---|---|
| SC:23 | coverage 9.72 → 10.0; 133/133 after round 41; three entries named; command A at `e1c83313` `missing []` `dangling []` | command A at `e1c83313` and base: `mapped 133 knowledge_files 133 missing [] dangling []`; the three named files were added by `d764389e` (triage-v3), `042b8769` (avm-be-core), `e1c83313` (binwalk-v3) and exist; `a79945c4`: 70/72 = 9.72 | yes |
| SC:23 | 130/130 at `4d62ee5a`, two entries; 128/128 round 39 two entries; 126/126 round 38 two; 124/124 round 36 two; 122/122 at `cab59f22`; 116/116 at `c369242f`; 109/109 `ebe2cb4a`; 78/78 `3395b6d`; 107/107 `7ef837a4`; 108/108 round-25 EVM entry | command A: `4d62ee5a` 130, `52b0eb29` 128, `3b960fe5` (r38) 126, `ffc81341` (r36) 124, `cab59f22` 122, `c369242f` 116, `ebe2cb4a` 109, `3395b6d` 78, `7ef837a4` 107, `08c7a729` 108; each pair of entries per round verified from `git log --diff-filter=A -- corpus/knowledge` | yes |
| SC:23 | "116/116 at `c369242f`, round 31" | `c369242f` is the round-30 closure commit; round 31's own landing `0007731e` measures 118/118. The SC round-31 section (line 3266) calls it the "`c369242f` recount", i.e. round 31's *before* state | yes numerically; label "round 31" names the base, not a round-31 result (D-K, minor) |
| SC:23-24 | evidence column: command A is `tools/round-38/c2-counter.py`; "measured after the round-39 landing (… `52b0eb29`) and after round-38 and round-36" | files exist; but the row's own newest measurement is `e1c83313` and `4d62ee5a` | **stale column** (D-C) |
| SC:24 | coverage "Last-change round": "count refreshed rounds 25, 26, 31, 36, 38, 39 and 40" | the same row's observable records a round-41 refresh (130→133 at `e1c83313`) | **mismatch** (D-C) |
| SC:24 | depth 20/20 at `e1c83313` (block 20 `SKILL.md:387-449`; craft `81-449`); 19/19 at `4d62ee5a` (block 19 `348-375`); 18/18 at `52b0eb29` (`citation_resolved_rules 18`, block 18 `316-343`); 17/17 `c369242f` and `ebe2cb4a`; 9/9 `638fb211` | all reproduce (command A and range scan above) | yes |
| SC:24 | "rule blocks grew from 9 to 17 in eight commits from `58116aa1` to `4072ebb3` (2026-10-18 and 2026-10-19)" | 13 commits touch SKILL.md in that range; exactly 8 of them add a block (10 at `58116aa1`, 11, 12, 13, 14, 15, 16, 17 at `4072ebb3`); dates 2026-10-18 and 10-19 | yes |
| SC:24 | "row kept 9/9 until round 25 added a recount at `08c7a729`" | 17 rule blocks at `08c7a729` | yes |
| SC:24-25 | depth evidence column: craft `SKILL.md:81-343` (last non-blank 343 at `52b0eb29`; baseline `77-191` at `a79945c4`), "measured `52b0eb29` (round 39; prior recount `c369242f`)" | 81-343 at `52b0eb29` ✓; `a79945c4` heading 77, next `##` 193, last non-blank 191 ✓; but the row's newest measurement is `e1c83313` | ranges yes; **stale evidence column** (D-C) |
| SC:25 | depth "Last-change round": "count refreshed rounds 25, 26, 39 and 40" | the observable names rounds 31 (17/17 at `c369242f`) and 41 (20/20) | **mismatch** (D-C) |
| SC:26-27 | calibration 9/9; command B; count measured at `c265db9b`; "row said `75af886a` until round 26 (luna-round-2 receipt reconciliation)" | command B (verbatim, base): baseline `6645585873…` 0/9 score 0 → after `c265db9b…` 9/9 score 10; `75af886a` = "luna-round-2: per-client REA surface calibration" | yes |
| SC:30 | "Baseline source revision `6645585873…`" | equals `rubric.json` and `result.json` `baseline_revision` | yes |

### SCORECARD.md `## Capabilities` (lines 615-636)

| location | asserted | observed | match? |
|---|---|---|---|
| SC:619 | "10-leg frozen-prediction battery" | `.ufo/waves/luna-round-6/receipts/leg-1.md … leg-10.md` | yes |
| SC:621 | "zero-drift 6-line 5-hash receipt pair" | both files 6 lines (timestamp + 5 sha256); `diff` of the hash lines empty | yes |
| SC:622 | r8 control "oom-kill" with pointer `r8-ctl-envelope.json` | the envelope records `failure_kind cancelled`, `exit_code null`; `oom-kill` appears only in `.ufo/waves/arc2-loop1-round8/C1.md:26,84` | partial: pointer supports the cancellation, the cause is two files away (D-J, minor) |
| SC:623-631 (all rows) | every backticked tool/receipt/entry path | 97/97 resolved at base; flagged `K1..6/…`, `AXES.md` handled below | yes, except `AXES.md` |
| SC:631 | "(`AXES.md` §Capabilities)" | not in the lane tree; `/home/vgpnk/Projects/shokunin/AXES.md:57` `## Capabilities — the repertoire table` | resolvable only at the fleet root (D-I, minor) |
| SC:626 | round-14 `quote-fidelity.py --selftest`; `--frozen …expected.json` | `QUOTE_FIDELITY_SELFTEST: CLEAN cases=28 passed=28`; `--frozen` `VERDICT: clean manifests=7 findings=0 exit=0` | yes (no count asserted) |
| SC:629 (r39 C1 row) | counter 6/6, exit 0 at `6fdaf4f1`; `K{1..6}/{after,run}.json` | 6/6 ✓, files ✓; the cited receipt `c1-at-6fdaf4f1.json` has **no exit-code field** | count yes; "exit 0" unrecorded (D-G) |
| SC:630 (r39 C2 row) | 20/20, exit 0 at `6fdaf4f1`; H01-H20; seed `8fcda41c…`; selftest 35; 8 rows / 7 non-`*` cells | `matched 20 n 20 interpreter_exit 0`; seed ✓; 35 ✓; 8/7 ✓; table v1 has 8 rows | yes |
| SC:631 (r40 row) | `c2-counter --rev 42c10a58… --freeze 7fce3086…` → 26/26, exit 0 | `c2-at-42c10a58.json` `matched 26 exit_code 0 revision 42c10a58… freeze 7fce3086…` | yes |
| SC:631 (r41 AVM row) | `c1-counter` 4/4 exit 0 `c1-at-e9a24d07.json`; 5491 nested rootfs 6349 files; "two lane-built images with both-direction path collisions" | 4/4, exit 0 ✓; 6349 ✓; collisions are asserted in PROVINCE/the carrier spec, not re-derived here | yes |

### SCORECARD.md `## Round 41` (lines 3455-3467)

| location | asserted | observed | match? |
|---|---|---|---|
| SC:3457 | base `49096c7e`; freeze `d764389e`; controls `9a8fb260`; C1 receipts `5ca6941b` (+ V4 `after.json` at `e9a24d07`); C2 held-out `8a1f4c73`; landing docs `042b8769`; scores `bf5286c9`; measured `e9a24d07`; assimilation `e1c83313` | all 9 are commits, ancestors of base; subjects and `git show --stat` agree (freeze holds claims, c1 carriers/gap-rule, controls/c2 + dev, knowledge entry; `5ca6941b` has V3/L3/L4 + a harness-failure log and no V4 `after.json`; `e9a24d07` adds only `V4/after.json`; `8a1f4c73` 52 carriers; `bf5286c9` `.ufo/waves/round-41/l1/scores/…`) | yes |
| SC:3457 | "Wave 1: 41 seats (`w1/`)" | 41 `.md` at base | yes |
| SC:3457 | "wave 2: 33 seats (`w2/`)" | **26** `.md` tracked at base; 33 at lane HEAD `ae5dc3f` (seven landed after base) | **mismatch at base**, repaired at HEAD (D-F) |
| SC:3461 | R41-C1 "at the freeze `carriers_matched 0`, exit 1" (`ctl-c1-0-do-nothing.json`); relabel r40 0/4 | `carriers_matched 0 exit_code 1 met_target false` both; every carrier precondition true, documentation bindings false | yes |
| SC:3461 | after: `carriers_matched 4`, every binding true, `frozen_path_changed []`, exit 0; `c1-extra` met exit 0; "at `042b8769` 3/4: V4 `after.json` not yet committed" | `c1-at-e9a24d07.json` ✓; `c1-extra-at-e9a24d07.json` `met true exit 0`; `c1-at-042b8769.json` `carriers_matched 3 exit 1`, V4 the unmatched carrier | yes |
| SC:3462 | R41-C2 at the freeze exit 2 `no_manifest_at_rev`; dev controls 0,4,34,2,38,31,42,44 of 52 vs SKILL 52 | `c2-counter-at-freeze.json` `exit_code 2 unevaluable no_manifest_at_rev`; `dev-scores-prefreeze.json` `{CTL-C2-0:0, 1:4, 2:34, 3:2, 4:38, 5:31, 6:42, 7:44, SKILL:52}`, n 52 | yes |
| SC:3462 | after: `matched 52` of 52, `distinct_decisions 13`, real-receipt binding true, `observed_features_match_declared` false, exit 1 | `matched 52 distinct_decisions 13 exit_code 1 bindings_false ['observed_features_match_declared'] real_receipts_depth_limited true` | yes |
| SC:3465 | owned scores: map proxy 130/130 → 133/133; depth 19/19 → 20/20; "stale SKILL ranges in SHONEN and the depth row repaired in this landing" | counts ✓. The repair is real for the *labelled* ranges, but see D-E/D-C: the unlabelled-as-current pointers and the Last-change column were not repaired | counts yes; repair claim partly |
| SC:3466 | planned: QUALITY 84; CTL-C2-7 8/12 on combos (`w2/R41W2C2Combos.md`); 18 host-local SOURCES rows (R41-CL3); R36-CL5, R40-CL2 open | `corpus/QUALITY.md:92` row 84 "Extends row 83…" ✓; Combos report "CTL-C2-7 scored 8/12" ✓; `local-source-gate.py --rev c4a38ea2 --json` → `rows_total 129 rows_checked 19 rows_failed 18` ✓; `corpus/lessons/round-41.md:73,82` mark both open ✓ | yes |

## 2. Debt the round-42 landing must not grow

- **D-A** (S:12, PROVINCE). `PROVINCE.md:157` (the sasquatch bullet) still ends "AVM-BE and vendor-mangled stay here"; `:384` and `:394` likewise. Round 41 appended a supersession block at `:402-408` but did not touch `:157`, the pointer round-39 wave-2 (`R39W2C1AxisFit.md` D2) explicitly repaired for the previous promotion. Round 42 moves SquashFS v3 from Frontier to Core: the `:157` bullet, the `## Frontier` text and the `no REA run on a v3 chunk` statements must get dated pointers in the same landing. SHONEN S:12 also stops its PROVINCE inventory at round 40 (the Round-41 block `:396-408` is unnamed); the landing should extend the range list to Round 41 *and* Round 42.
- **D-B** (PROVINCE:400, inside the round-41 Core row). Placeholder text was committed: `` counter `tools/round-41/c1-counter.py` `carriers_matched scored after this commit` exit see `.ufo/waves/round-41/l1/scores/` at `the commit that adds this text` ``. The real numbers exist (4/4, exit 0, `e9a24d07`). Do not repeat the pattern: the Round-42 Core row must name the measured revision and score file, written after the score.
- **D-C** (SC:23-25 "Last-change round" and evidence columns). Coverage lists refreshes "25, 26, 31, 36, 38, 39 and 40" (no 41); depth lists "25, 26, 39 and 40" (no 31, no 41); the coverage evidence column says "measured after the round-39 landing (`52b0eb29`)" and the depth evidence column "measured `52b0eb29` (round 39…)" while the observable column's newest measurement is `e1c83313`. The landing must update all three cells per axis together (observable, evidence, last-change) with one measured revision.
- **D-E** (SKILL.md ranges). `SKILL.md:81-449` and `:387-449` are correct only because block 20 is last and the next `##` is at 454. Round 42 adds rule block 21 (and a supersession sentence on block 20): block 20 grows, `81-449` becomes `81-<new end>`, and SHONEN S:6, SC:24 (observable and depth rows), SC:3457-3462 and the Capabilities rows that quote `:387-449` all go stale at once. Already today the at-commit ranges `348-375` (block 19) and `316-343` (block 18) are 351-385 and 316-349 at base; they are labelled by commit in S:6 and SC:24 but read as current. Rule for the landing: every range names the commit it was read at, and a fresh `git show <REV>:SKILL.md` range scan (artifact `skill-ranges.txt` is the recipe) is run at the final commit.
- **D-F** (SC:3457). "wave 2: 33 seats" was true of the directory only after `ae5dc3f3`; at the base the SCORECARD cited, 26 reports were tracked. Landing text should state the seat count only after the last report is committed.
- **D-G** (receipt gaps). `c1-at-6fdaf4f1.json` (round 39) has no exit-code field, though SC:629 asserts "exit 0 at `6fdaf4f1`"; the round-41 score receipts record no `counter_sha256` (round-41 closure D4; the round-42 draft already requires it).
- **D-H** (selftest counts not asserted for the live table). S:6 cites selftest counts for the v1 and v2 interpreters only; the live v3 interpreter (`tools/round-41/sqfs-triage-v3.py --selftest`: 69/69 at base), `tools/round-41/c2-counter.py --selftest` (70/70) and `tools/round-40/c2-counter.py --selftest` (42/42) appear nowhere. When v4 lands, state its observed count (and read it from a run), and note `tools/round-41/c1-counter.py --selftest` is not a working invocation (TypeError in a subprocess call at base) so the round-42 C1 counter's selftest path should be exercised before the freeze.
- **D-I** (SC:631). `AXES.md §Capabilities` is a fleet-root file, not in the lane; cite it as `../AXES.md` or the fleet path.
- **D-J** (SC:622). The r8 control row's evidence pointer shows `cancelled`, `exit_code null`; "oom-kill" lives in `arc2-loop1-round8/C1.md`. Add the second pointer if the row is touched.
- **D-K** (SC:23). `c369242f` is labelled "round 31"; it is the round-30 closure and round 31's before-state (round 31's landing `0007731e` is 118/118).

## 3. Defect in the draft (affects the round-42 landing)

- **D-L** `plans/round-42-claims.md:11` says "the v3 table sends every SquashFS v1–v3 chunk to `no-squashfs-chunk`" and `:63` hedges "`no-squashfs-chunk` or `unclassified`". Observed: the frozen v3 interpreter (`tools/round-41/sqfs-triage-v3.py --skill SKILL.md`, base clone) prints **`unclassified none`** for every one of 48 envelopes built from the round-41 held-out classes (`clean-le`, `clean-be`, `dep-missing-le`, `body-extractor-failure`, `partial-body-failure`, `escaping-symlink-removed`) with every squashfs handler string rewritten to each of `squashfs_v1`, `_v2`, `_v2_nonstandard`, `_v3`, `_v3_ddwrt`, `_v3_broadcom`, `_v3_nonstandard` (`probe-v3-legacy.out`; rc 0). Never `no-squashfs-chunk`. That is what the cited `corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md:22-25` says (interpreter handler `none` ⇒ `unclassified`; precedence step 2 ⇒ `no-squashfs-chunk`; the lesson row R41-CL4 calls it a divergence, not a routing to `no-squashfs-chunk`). The control CTL-C2-0b prediction on `:63` should therefore be a single label, `unclassified`, for the interpreter, and `no-squashfs-chunk` only for the evaluator.
  Side facts for the table's handler cells, read from unblob 26.6.4 `handlers/filesystem/squashfs.py` `NAME =`: `squashfs_v1`, `squashfs_v2`, `squashfs_v2_nonstandard`, `squashfs_v3`, `squashfs_v3_ddwrt`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, `squashfs_v4_le`, `squashfs_v4_be`, `squashfs_v4_broadcom` — there are **no** `squashfs_v3_le`/`_be` names. The v3 interpreter already routes `squashfs_v4_broadcom` through its `squashfs_v4_*` glob (the probe labelled it `clean`, `dep-missing-le`, `body-extractor-failure`, … like v4_le), so a "whole family" table must decide that handler explicitly. The draft's other file:line citations (`round-41-claims.md:109-115`) are in range (`draft-citations.txt`).

## 4. Commands and limits

- `git cat-file -t c4a38ea2…` → `commit`; 37 distinct hashes from the three sections plus SHONEN checked with `git rev-parse --verify <h>^{commit}` and `git merge-base --is-ancestor <h> c4a38ea2` (all exit 0).
- Command A: `python3 -I command-a.py <REV>` run from the lane root at 22 revisions (`command-a-results.txt`); command B verbatim (`command-b.json`).
- Selftests (sandbox clone at base, `python3 -I -B <tool> --selftest`): r39 `sqfs-triage.py` 35/35, r40 `sqfs-triage-v2.py` 45/45, r41 `sqfs-triage-v3.py` 69/69, r39 `c2-counter.py` 27/27, r40 `c2-counter.py` 42/42, r41 `c2-counter.py` 70/70; r41 `c1-counter.py --selftest` crashes (TypeError); `.ufo/waves/round-14/tools/quote-fidelity.py --selftest` 28/28.
- Not checked: the semantic content of the 130+ historical numbers outside SHONEN, the three listed sections and the Round-41 section (the `Verdicts`, `Saturation` and earlier round sections); the oracle/sha256 content of carriers; re-running REA/unblob (none run — no extractor touched any published image). "6349 files" etc. are read from score receipts, not recomputed. Tool installs: none.
- Scratch `/fast/scratch/hyaku/kaidoku-r42/R42ScoutCalib` removed.

Report: .ufo/waves/round-42/w1/R42ScoutCalib.md
