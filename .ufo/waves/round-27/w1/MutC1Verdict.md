# Round 27 wave 1 — MutC1Verdict: mutation test of the R27-C1 counter

Seat: `KaidokuR27.MutC1Verdict` (leaf, no delegation). Lane base `cd32264f`, lane head `a4f674b3`.
Scope: verdict derivation and row accounting of `tools/round-27/c1-rename-identity.py`
(sha256 `e0a079955c16a759dc3ba4facb6d954431ce605ea2a6da680f43b20cea743bb7`, matches the frozen
instrument in `.ufo/waves/round-27/claims.json`). Observation window: 2026-10-22T14:52Z to 2026-10-22T14:58Z.

## What was attacked

The pinned counter was **not** modified. Each mutant changed one byte-level property of a green
fixture and was committed; the pinned counter was then run against the mutated commit. A mutant is
**killed** when the counter refuses it (nonzero exit) and **survived** when it still reports the
round complete (exit 0, `rows_complete=16/16 entry_ok=1`).

Detector (the same command for every run):

```
python3 -I -B tools/round-27/c1-rename-identity.py --root <case repo> --rev <mutation commit> --base <green base>
```

Green fixture: built by the counter's own `_build_green` (its selftest fixture builder), so the
fixture is the one the pinned instrument itself uses. Sandbox root
`/fast/scratch/hyaku/kaidoku-r27/seats/MutC1Verdict/clone` (green repo, base
`b0a21e5ef1d7d1b14bce8a748419dc33c9be5846`, head `2c4b94546cdde56fbe808ab2f6ba25a285728a39`);
one clone per case under `.../cases/<case>`; no REA call was made (not needed for this probe).

Baseline, pristine green fixture: **exit 0**, `rows_complete=16/16 entry_ok=1 rev=2c4b9454`; pinned
counter selftest on the same bytes: `selftest cases=22 failures=0`, exit 0.

## Results

| # | Mutant (green fixture → mutated) | Expected detector | Actual output excerpt | Exit | Verdict |
|---|---|---|---|---|---|
| m01 | jq/analyze repeat envelope gets a distinct recomputed id (base id = renamed id, repeat id different); table verdict left `content-keyed` | verdict rule re-derives `unstable` | `INCOMPLETE jq analyze: table verdict content-keyed, derived unstable` | 1 | killed |
| m02 | same id change, table verdict set to `unstable` (the derived verdict) | unstable branch accepted | `rows_complete=16/16 entry_ok=1` | 0 | survived (correct behaviour) |
| m03 | all three ids equal, table says `rename-sensitive` | verdict rule re-derives `content-keyed` | `INCOMPLETE jq analyze: table verdict rename-sensitive, derived content-keyed` | 1 | killed |
| m04 | table.tsv has 17 rows, jq/analyze duplicated | row accounting sees 2 rows for one pair | `INCOMPLETE jq analyze: table has 2 rows` | 1 | killed |
| m05 | table.tsv has 17 rows, extra row for pair `jq/strings` (outside the frozen 16) | row set checked against the frozen 16 | `rows_complete=16/16 entry_ok=1` | 0 | **survived** |
| m06 | all eight tinyxxd rows removed from table.tsv | missing rows counted incomplete | `INCOMPLETE tinyxxd analyze: table has 0 rows` (8 rows) | 1 | killed |
| m07 | table.tsv data rows reversed | order sensitivity | `rows_complete=16/16 entry_ok=1` | 0 | survived (order-independent) |
| m08 | runs.tsv rewritten with CRLF endings | structural check | `input error: runs.tsv header differs from frozen header` (stderr) | 2 | killed |
| m09 | runs.tsv gains an extra empty trailing field on every data row | cell count check | `input error: runs.tsv line 2 has 15 cells, want 14` (stderr) | 2 | killed |
| m10 | runs.tsv keeps 14 cells but `utc_end` is empty | end time validated | `rows_complete=16/16 entry_ok=1` | 0 | **survived** |
| m11 | `utc_start` = `2026-10-22T11:30:00.500Z` | timestamp parse | `INCOMPLETE jq analyze: base: utc_start 2026-10-22T11:30:00.500Z not after counter commit` | 1 | killed |
| m12 | `exit` cell = `0 ` (trailing space) | exact cell match | `INCOMPLETE jq analyze: base: exit 0 ` | 1 | killed |
| m13 | argv writes the address as `0x103FA0` | argv equals frozen template | `INCOMPLETE jq decompile: base: argv differs from frozen template; repeat: ...; renamed: ...` (5 verbs) | 1 | killed |
| m14 | runs.tsv lists jq/analyze base twice | one line per run | `INCOMPLETE jq analyze: base: runs.tsv has 2 lines` | 1 | killed |

Twelve of fourteen mutants were killed; m05 and m10 survive, plus two benign survivors (m02, m07).

## Notes on every survivor

- **m05, table row set not checked (observation, real coverage gap).** The counter looks up each of
  the 16 frozen `(carrier, verb)` pairs and requires exactly one row each; it never compares the
  table's row set with the frozen matrix and never checks the table's row count against
  `ROWS_TOTAL`. A table holding 17 rows, one of them for a pair outside the claim (`jq/strings`),
  still reports `rows_complete=16/16 entry_ok=1`. Observation: the mutated table at commit `da80fa20…`
  has 18 lines (header + 17 rows) and the counter passes it. Inference: a claim that says "one
  complete row for each of 16 frozen pairs" is still satisfied, but any extra row is invisible to
  the receipt, so the receipt cannot show that the table holds *only* the 16 pairs: a coverage
  finding about the receipt, not a contradiction of R27-C1, and it does not falsify the 16 verdicts.
- **m10, `utc_end` is never read (observation).** `utc_end` is in the frozen `RUNS_HEADER`, and
  `read_tsv` enforces the 14-cell shape, but `count()` never reads the value. A run with an empty
  end time is counted complete. Inference: harmless for the claim (the claim is about ids and
  verdicts), but the receipt cannot show that every run was closed.
- **m02, unstable branch is reachable and accepted (observation, no finding).** With
  `base_id = renamed_id` and `repeat_id` different, the derived verdict is `unstable` and a table
  row saying `unstable` is accepted (exit 0). This matches the frozen rule text ("unstable if
  base != repeat") and the code's branch order, so it is intended behaviour, not a defect; m01
  proves the same data with a wrong verdict is refused.
- **m07, row order is not significant (observation, no finding).** The counter selects rows by
  `(carrier, verb)` and never by position, so a reversed table is accepted, which is the intended
  order-independent accounting.

## Restoration evidence

Every case was run mutated, then the case clone was restored with
`git reset --hard <green head>` + `git clean -qfd`, and the counter was run again: restore exit 0
in all 14 cases, `rows_complete=16/16 entry_ok=1` in all 14. sha256 of the touched files,
before mutation / after mutation / after restore (full-length in
`artifacts/mutation-results.json`):

| file | green | m01/m02 mutated | m05 mutated | m07 mutated | m10 mutated | restored |
|---|---|---|---|---|---|---|
| corpus/evidence/round-27/c1/runs.tsv | `12b3da600cbd329b…` | `dd7f599172db5d13…` | `12b3da600cbd329b…` | `12b3da600cbd329b…` | `eff5313749150f1e…` | `12b3da600cbd329b…` |
| corpus/evidence/round-27/c1/table.tsv | `848e17b30803e7a9…` | `c6f3a87f43ee00db…` (m01) / `627cbf768f8bf7e8…` (m02) | `84f930ade2a6d51e…` | `22ba5c1aa6859cb3…` | `848e17b30803e7a9…` | `848e17b30803e7a9…` |
| corpus/evidence/round-27/c1/envelopes/jq-analyze-repeat.json | `91ffdc230e3b2d91…` | `b812027a60a70427…` | `91ffdc230e3b2d91…` | `91ffdc230e3b2d91…` | `91ffdc230e3b2d91…` | `91ffdc230e3b2d91…` |

Byte-level confirmations of the mutations, taken from the mutation commits:
m08 header ends `… pkg_json_sha256 \r \n`; m09 data row ends `… a6c \t \n` (15 cells);
m13 line 8 argv = `decompile /usr/bin/jq 0x103FA0 --format json --full-output`;
m11 `utc_start` = `2026-10-22T11:30:00.500Z`; m12 `exit` = `0 `; m05 table = 18 lines with a
trailing `jq strings content-keyed` row; m02 jq/analyze row = `unstable`, `ev_67b973df64a…`,
`ev_8c5b35ebcc5…`, `ev_67b973df64a…`.

## Verdict on the assignment

The R27-C1 counter's verdict derivation and row accounting **hold** against the ten requested
mutants that carry a semantic defect (m01, m03, m04, m06, m08, m09, m11, m12, m13, and the extra
m14): every one is refused with a specific, correct reason, and every refused row is named in the
receipt. The two survivors are a receipt-coverage gap (extra table row outside the frozen matrix,
m05) and an unvalidated cell (empty `utc_end`, m10). Neither changes a verdict, and neither is a
contradiction of R27-C1's claim as written.

## Lane and tooling

Read-only on the lane: the only lane write by this seat is this report file
(`.ufo/waves/round-27/w1/MutC1Verdict.md`). No `git add/commit/checkout/reset/stash` in the lane, no
`jj` command anywhere, no REA run, no install or upgrade was needed (python 3.14.8 and git 2.56.0
were already present; the counter's own fixture builder produced the green fixture).

Seat artifacts (all under `/fast/scratch/hyaku/kaidoku-r27/seats/MutC1Verdict/`):

| path | sha256 |
|---|---|
| mutate.py (harness) | `7e4fa5f94d54e22c721c59a6edc81da5f6c82c7ae06e32ff51369bec9f90f369` |
| artifacts/mutation-run.txt (full stdout log) | `942d8fba46f85ffd190dc7920247eb2c2c5f3656bcd9c5b3ddfb6f55abf88e60` |
| artifacts/mutation-results.json (per case stdout, exit, before/after/restored hashes) | `c18dddfc44d32e58da0c238d81f3f96440cf0a5711502941965da144e221739f` |
| artifacts/selftest-baseline.txt (pinned counter selftest, 22 cases, 0 failures) | `fb6679a3d6d82ca8b0ab2a10792dddbfd28c4ce2d30ad58dcafb28c0b692b0b4` |
