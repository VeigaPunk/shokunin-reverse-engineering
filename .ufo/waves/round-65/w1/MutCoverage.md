# MutCoverage — R65-C2 instrument mutation report

Seat MutCoverage (leaf), round-65 w1 attempt 1. Base `c99e907cb5576c13a7b22755d776b356fdfc1752`.
Instrument `tools/round-65/coverage-recipe.py` (frozen, sha256 `9434888e1bfa283f2980fb3c550b9e15409c88855ee94c944e8472fcf83995a6`).
Full per-mutant evidence: `.ufo/waves/round-65/w1/MutCoverage/mutants.md`.

## Result: 6 mutants, 6 killed, 0 survived

Detector per mutant = `--selftest` + both CLI arms at the base revision
(`--recipe stem` and `--recipe date`, `--root /home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
`--rev c99e907...`), each run with `python3 -B` and `PYTHONDONTWRITEBYTECODE=1` on a scratch copy.
Pristine before-arm: selftest `CLEAN cases=28 failures=0`; stem `mapped=144, population_dropped=0,
mismatches=0, exit=0`; date `population=142, mapped=142, population_dropped=2, mismatches=2, exit=1`.
Killed = any detector diverges from those bytes.

| id | one textual change | exit selftest/stem/date | verdict | killer |
|---|---|---|---|---|
| M1 | stem population re-filtered by `DATE_TOKEN_RE` (defect restored) | 1/1/1 | killed | selftest (8 FAIL) + cli-stem (exit 0->1, dropped 0->2, mism 0->2) |
| M2 | `missing = []` | 1/0/1 | killed | selftest (3 FAIL); CLI blind at this rev |
| M3 | `dangling = []` | 1/0/1 | killed | selftest (4 FAIL); CLI blind at this rev |
| M4 | empty population exits 0 instead of 2 | 1/0/1 | killed | selftest (1 FAIL: `empty-exit`); CLI blind at this rev |
| M5 | CLAIM filter on `raw` instead of `norm` | 1/1/1 | killed | selftest (11 FAIL) + cli-stem (mapped 144->109, mism 0->35) + cli-date (mapped 142->107) |
| M6 | `dropped = 0` | 1/0/0 | killed | selftest (4 FAIL) + cli-date (dropped 2->0, mism 2->0, exit 1->0) |

Mutant sha256s and exact diff lines are in `MutCoverage/mutants.md`.

## Findings

1. **No surviving mutant.** Every probe is discriminated; the R65-C2 instrument is not
   under-covered by its own detector set.
2. **The two predicate-halves are mutation-sensitive.** M1 (stem arm stops being clean) and M6
   (date arm stops naming the 2 hidden files) are exactly the defect-restoring changes, and both
   are killed by the CLI arms themselves — the predicate's counters are load-bearing.
3. **CLI coverage gap at this revision (instrument property, not a survivor).** Both arms already
   report `missing == []` and `dangling == []`, and neither has an empty population, so M2/M3/M4
   are invisible to the CLI and only `--selftest` kills them. An R65-C2 receipt that cited the CLI
   arms alone would not discriminate those three defects; the selftest fixtures are what cover them.
4. **M5 quantifies the tokenizer defect restoration.** Filtering before normalization rejects 184
   of 407 backticked coverage-map tokens (36 distinct `knowledge/`-prefixed norms), dropping 35
   distinct mapped stems — the strongest CLI-visible mutant after M1.

## Provenance / restoration

- Frozen instrument read-only throughout: sha256 re-checked after the pass equals the pin;
  `git -C <repo> status --porcelain -- tools/round-65/` empty.
- Mutants built by `cp` + single asserted textual replacement (`src.count(old) == 1`, bytes changed).
- Scratch `/fast/scratch/hyaku/kaidoku-r65/MutCoverage` (copies, `results.json`, driver) deleted
  after writing this report; nothing written outside the seat report dir.
