# R99-C1 falsification (seat CriticC1, kaidoku round 99, attempt 1)

Scope: falsify R99-C1 (self-assessment mismatches 17 → 0) under the frozen command
`python3 -I -B tools/round-99/self-assessment-audit.py --root <clone> --rev <rev> --json-out <receipt>`.
Counter read from freeze `8fb5ac4f` (`git show`), sha256 `e732465b…eec0`, identical at A and Bk.
Clone `$S/clone` detached at B0 `de098f51`; fixture commits exist only in that clone. The lane
repo was read only (`git show`, `diff`, `ls-tree`, `status`, `log`). Receipts: `.ufo/waves/round-99/w1/CriticC1/`.

## 1. Reproduction at the three revisions

| rev | exit | label (receipt) |
|---|---|---|
| B0 `de098f51` | 1 | `mismatches 17; head-score mismatch; head-fraction mismatch; map-rows 176 of 182; registry 0 of 9` (`c1-b0.json`) — matches the frozen base control |
| A `64cc3e10` | 0 | `mismatches 0; head-score ok; head-fraction ok; map-rows 182 of 182; registry 14 of 14 met True` (`c1-A.json`) |
| Bk `c19d57cd` | 0 | `mismatches 0; ...; map-rows 183 of 183; registry 14 of 14 met True` (`c1-Bk.json`) |

The base receipt, A and Bk match the frozen controls and the landed claim.

## 2. Forgeries (each scored by the frozen command; commit shas in `c1-fixture-shas.txt`)

| id | commit | edit | label | exit |
|---|---|---|---|---|
| F-R | `a29200fa` | from B0: nine SKILL registry rows, each with the tool's true sha256, false kind/exit/selftest prose (`--selftest 99 cases, 0 failures (forged, not run)`) | `mismatches 8; head both mismatch; map-rows 176 of 182; registry 9 of 9` | 1 |
| F-M | `5b9d97dc` | from B0: one new map row naming the six unmapped stems, 22 filler characters | `mismatches 10; head-score ok; head-fraction mismatch; map-rows 182 of 182; registry 0 of 9` | 1 |
| F-H | `ff90d4d1` | from B0: one duplicate `| coverage |` head row above the real one, `182/182 knowledge files` plus a false round-85 sentence | `mismatches 17` (head alone is caught) | 1 |
| F-MH | `4feeca36` | F-M + F-H | `mismatches 9; head-score ok; head-fraction ok; map-rows 182 of 182; registry 0 of 9` | 1 |
| F-ALL | `1fead74c` | F-MH + F-R | `mismatches 0; head-score ok; head-fraction ok; map-rows 182 of 182; registry 9 of 9 met True` | 0 |
| F-ALL-scope | `a456f87a` | F-ALL + `tools/round-100/unregistered.py` with no registry row | `mismatches 0; ...; registry 9 of 9 met True` | 0 |
| F-PH | `54235b0f` | landed A + one map row naming `2026-11-05-r99-phantom-entry` (no such entry) | `mismatches 0; ...; map-rows 182 of 182; registry 14 of 14 met True` | 0 |

Cost of the cheapest zero: 9 registry rows + 1 map row + 1 head row (about 11 lines). Every
input is public (sha256 of committed blobs, `b0-tool-shas.txt`); no secret is needed. The
atoms are independent: F-R alone gives registry 9 of 9; F-M alone gives map 182 of 182; the head
atom needs the map atom before it can pass, which is why F-H alone stays at 17.

## 3. Named limits (admitted forgeries)

- **L1 registry prose is unchecked (A4).** The atom accepts any row whose cell 2 starts with a
  kind word and ` — `, whose cell 3 has `0=` and `1=`/`2=`, whose cell 4 has ≥10 characters, and
  whose line carries the file's sha256. Kind, exit meaning and selftest counts are never compared
  with the file. F-R admits nine false rows. Landed prose I checked is true: `c1-selftest.txt`
  reads `SELFTEST cases=9 failures=0` (rc 0), `selftest-v7.txt` `cases=23 failures=0`,
  `selftest-v8.txt` `cases=24 failures=0`; the nine "no `--selftest`" rows match `grep` (zero
  mentions in those tools). Not checked: the "14 fixture cases" cited for `craft-citation-v2.py`,
  and the exit maps of the other rows.
- **L2 map rows are presence-only (A3).** A table row passes if it has ≥3 cells, a backticked
  stem, and ≥20 characters after stems, pipes, backticks, commas and whitespace are removed. F-M
  passes six stems in one row of filler. Landed rows at A checked against their entries: r93
  citation semantics (block 31 row 3, QUALITY 169; entry lines 9–19) true; r93 fresh-pack
  "NOT verified" (entry line 128) true; r96 "killed 5 of 10" and the named limits (entry lines
  22, 236, 248) true; r95 "before-side of R95-C1 is met" (entry line 159) true. r94 and r97
  rows assert verdicts whose identifiers do not occur in their own entries (R94-C1 verdict at
  SCORECARD line 6643; the v7 nine-key allow-list in SKILL's v7 row). Those verdicts are true
  as read, but they live in other documents.
- **L3 head atom reads the first match (A1/A2).** `parse_row` takes the first `| coverage |`
  line under `## Owned axes` and the first `N/M knowledge files` in it. F-H puts a false row
  above the real one. It is caught alone and passes with F-M. The landed head is true in the
  presence sense: 182 stems are present (`r66-stem-A.json`, recipe A `dangling []`).
- **L4 the dangling direction is not checked.** The frozen counter ignores map names that are
  not entries. F-PH passes at A with `mismatches 0`. The round-66 stem recipe, which the head
  row cites as its measuring tool, catches the same row: `dangling ["2026-11-05-r99-phantom-entry"]`,
  `mismatches 1`, exit 1 (`r66-stem-PH.json`). The frozen C1 counter is therefore weaker than
  the instrument it is said to re-derive.
- **L5 scope is hard-coded.** `TOOL_DIRS = (round-97, round-98, round-99)`. A round-100 tool
  without a registry row scores `mismatches 0` (F-ALL-scope). Subdirectories and round-96 tools
  are also outside the atom.
- **L6 sha256 binds bytes, not meaning.** A4's only substantive check is that the row carries
  the file's hash. Anyone can compute that hash, so the atom shows only that a row cites the
  file, not that the row describes it.
- **L7 the head's receipts are not committed.** The landed head row cites
  `.ufo/waves/round-99/l1/scores/c1-at-*.json`. On disk, `c1-at-64cc3e10…json` and
  `c1-at-c19d57cd…json` exist and agree with my runs (`mismatches 0`, exit 0), but `git status`
  shows both as untracked (`??`), so neither landed commit contains its receipt. No atom checks
  this.

## 4. Verdict on the substance (A and Bk)

- The predicate's zero is correct for the landed surfaces as far as I read them: 182 of 182
  stems are present; the registry's selftest counts and "no `--selftest`" rows are true where
  checked; the r93 and r96 map descriptions match their entries.
- The predicate cannot tell the landed state from F-ALL or F-PH. Both score exit 0. So
  "calibration 17 → 0" rests on the lane's manual reading and on the substance above, not on the
  counter. The frozen predicate is met, but it rewards presence and shape.
- Routing for the landing: the counter should check the dangling direction (L4) and the
  registry's kind and count prose against the file (L1) before C1 is treated as calibration. The
  head's receipts should be committed (L7).

## 5. Not done and limits of this seat

- R99-C2 was not in this item. Nothing was re-frozen, re-pinned or re-scored in the lane.
- No tool was installed (no pacman, no uv, no npm). No mutation ran in the lane repo.
- Scratch `$S` and the clone are removed on exit; the copied receipts above are the record.
