# MutCoverage — R66-C2 counter mutation probe (scoped findings)

Target: `tools/round-66/coverage-selfcheck.py`, frozen sha256
`1be9d046cea38a96a4b62d038f7dbc76e8ea611000af4aee3b91a6def86555aa` (never edited).
Five mutants in isolated scratch mirrors, each scored by both assigned detectors:
`--selftest` and `--selfcheck --root <lane> --rev 311079d869f068bc083a8d180977e49634120fdf`.
Full diffs, verbatim detector lines and receipt index: `.ufo/waves/round-66/w1/MutCoverage/mutants.md`.

Baseline (pristine): `--selftest` exit 0 `SELFTEST CLEAN cases=26 failures=0`;
`--selfcheck` exit 1, `equiv=true hidden=3 mismatches=1 ok=false`, atoms `A1 true` / `A2-cited-fraction false`
(claimed `[142,142]`, stem `[145,145]`).

| # | mutant | `--selftest` | `--selfcheck` @base | verdict |
|---|---|---|---|---|
| M1 | `recipe_hidden` → `[]` | exit 1, failures=1 (`recipe-a-hidden-list`) | exit 1, hidden **0**, mismatches 1 — unchanged | killed (selftest; base selfcheck masked) |
| M2 | `recipe_a_equivalence` true without running the block | exit 0, CLEAN | exit 1, hidden 3, mismatches 1 — identical to baseline | **SURVIVED** |
| M3 | A2 atom deleted | exit 0, CLEAN | **exit 0**, mismatches **0**, ok=true, one atom | killed (base exit) |
| M4 | `parse_row` supplies the observed fraction (tautology) | exit 0, CLEAN | **exit 0**, mismatches **0**, A2 true | killed (base exit / A2 flip) |
| M5 | `mismatches = 0` constant | exit 0, CLEAN | **exit 0**, mismatches **0**, ok=true, A2 still false | killed (base exit; receipt inconsistent) |

## Survivor finding — equivalence atom is unbound

`tools/round-66/coverage-selfcheck.py:200-207` (the `subprocess.run` of the extracted recipe-A block,
`json.loads(r.stdout)` and the `diffs` comprehension) and its consumer at line 269 are exercised by
neither detector. `selftest()` has no case that calls `recipe_a_equivalence` (all occurrences are outside
it: def 191, return 208, call 266, reads 269/272-273, CLI 409-411), and at the base revision the clause is
already true, so suppressing the comparison produces a receipt indistinguishable from pristine.

Proof the line is load-bearing on a disagreeing input: a synthetic fixture whose recipe-A block prints
`mapped 1 / score 1.0` while the counter computes `3 / 10.0` gives `--equiv` **rc 1, `equivalent false`,
diff keys `['coverage_score','mapped','missing']`** on pristine bytes, and **rc 0, `equivalent true`,
`{}`** under M2. A selftest case running `recipe_a_equivalence` against a doctored block would bind it.

## Mutation-suite caveat (not a defect in the counter)

M3/M4/M5 are killed only by the **base** revision. On a controlled-green synthetic revision
(all clauses satisfied: exit 0, hidden 1, mismatches 0) they are indistinguishable from pristine and
survive. The base arm is therefore load-bearing for those three; dropping it after the repair lands would
blind the suite. M1 shows the mirror case: its selfcheck signal exists only at a green revision
(pristine exit 0 vs mutant exit 1 there), while its selftest case kills it at any input.

## Byte restoration

- Frozen instrument unmodified: sha256 before and after the pass
  `1be9d046cea38a96a4b62d038f7dbc76e8ea611000af4aee3b91a6def86555aa`; `git status --porcelain -- tools/round-66`
  empty.
- Mutants and fixtures existed only under `/fast/scratch/hyaku/kaidoku-r66/MutCoverage`, deleted before
  yield after the receipts were copied into `w1/MutCoverage/mutants/`.
- Tool installs: none (no pacman, no uv, no PATH writes).
