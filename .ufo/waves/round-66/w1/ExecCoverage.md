# ExecCoverage — R66-C2 frozen counter arms (w1, run once)

Seat scope: run the five assigned `tools/round-66/coverage-selfcheck.py` arms once,
re-derive three numbers from git objects at base `311079d869f068bc083a8d180977e49634120fdf`,
write findings. Instrument never edited (sha256 before == after ==
`1be9d046cea38a96a4b62d038f7dbc76e8ea611000af4aee3b91a6def86555aa`).
`--selftest` was NOT run: it is assigned to other seats (CriticPredicates / E1XfsArm).

## Exits

| arm | rev | exit |
|---|---|---|
| `--selfcheck` | 7b63dd5d5199ed30bc3f213573d8594434a18eb6 (freeze) | 1 |
| `--selfcheck` | 311079d869f068bc083a8d180977e49634120fdf (base) | 1 |
| `--recipe a` | base | 0 |
| `--recipe stem` | base | 0 |
| `--equiv` | base | 0 |

Receipts (this directory): `selfcheck-at-freeze.json`, `selfcheck-at-base.json`,
`recipe-a-at-base.json`, `recipe-stem-at-base.json`, `equiv-at-base.json`, matching
`.stdout` files (byte-identical), `instrument-before.txt`, `instrument-after.txt`,
`findings.md`. Scratch `TMPDIR=/fast/scratch/hyaku/kaidoku-r66/ExecCoverage` (w1..w5),
deleted before yield.

## Atoms (identical at base and freeze)

- A1-head-score: claimed `10.0`, observed `10.0`, ok true.
- A2-cited-fraction: claimed `[142, 142]`, observed `[145, 145]`, **ok false**.
- `mismatches 1`, `ok false`, `exit 1` at both revisions.

## Equivalence and hidden list

- `recipe_a_equivalent true`, `recipe_a_diffs {}` (empty), block sha256
  `1d697af103985da0d056f6d0113059891a7658c1a3c4fbf568720166cf44a0db`
  (independently re-derived from a separate 29-line heredoc extraction — same hash).
- recipe A at base: `knowledge_files 145`, `mapped 142`, `coverage_score 9.79`,
  `citation_resolved_rules 27`, `rule_blocks 27`, `dangling []`, `depth_score 10.0`.
- `recipe_a_hidden` (non-empty, 3): `2026-11-03-r65-jsc-closure-matrix`,
  `jsc-mapper-cli-contract`, `jsc-mapper-release-inventory`.
- stem recipe at base: `population 145`, `mapped 145`, `mismatches 0`, `stem_score 10.0`.

## Independent counts — both equal the counter's

1. `git -C … ls-tree -r --name-only 311079d8… -- corpus/knowledge | grep -c '\.md$'` → **145**
   = counter `knowledge_files 145` / `stem.population 145`.
2. non-October stems via `… | xargs -n1 basename | sed 's/\.md$//' | grep -v '^2026-10-' | sort`
   → exactly the counter's 3 `missing`/`hidden` names.
3. `… show 311079d8…:SCORECARD.md | sed -n '/^## Owned axes/,/^## /p' | grep -m1 '^| coverage |' | grep -o '[0-9]*/[0-9]* knowledge files'`
   → **142/142** = atom A2 claimed. Cross-check: unique October tokens in the README
   `## Coverage map` = 142 = `recipe_a.mapped`.

## Findings / risks

1. **R66-C2 does not verify at the operative freeze.** The predicate's `mismatches 0`
   clause is false at `7b63dd5d` exactly as at base, because `SCORECARD.md` is unchanged
   between the two revisions. The stale figure is the round-53 landing anchor
   `142/142 knowledge files` cited inside the `## Owned axes` coverage row, while the
   repaired stem recipe observes `145/145`. The base-arm clause is satisfied
   (cited fraction is a mismatch at base), but it does not discriminate base from
   freeze — discrimination must come from a revision whose coverage row cites the
   corrected head.
2. **Repair surface is SCORECARD, not the counter.** `parse_row` takes the *first*
   `<n>/<n> knowledge files` match in the coverage row; a corrected fraction must be the
   first occurrence in that row for A2 to pass. No counter byte may change.
3. `selfcheck-at-base.json` is byte-identical to the pre-freeze dry run
   `.ufo/waves/round-66/l1/pre/dryrun-c2-selfcheck-at-base.json` (`cmp` clean): the
   counter is deterministic across the freeze.
4. No writes to the repo, toolchain root or frozen instruments; only this report
   directory and scratch were written. No git/jj mutation was run.
