# ExecCoverage — R66-C2 counter arms, run once at base and freeze

Instrument (frozen, unedited): `tools/round-66/coverage-selfcheck.py`
sha256 before `1be9d046cea38a96a4b62d038f7dbc76e8ea611000af4aee3b91a6def86555aa`
sha256 after  `1be9d046cea38a96a4b62d038f7dbc76e8ea611000af4aee3b91a6def86555aa`
(`instrument-before.txt`, `instrument-after.txt`; byte-identical.)
Interpreter `python3 -I -B`; scratch `TMPDIR=/fast/scratch/hyaku/kaidoku-r66/ExecCoverage`.

## Arms (each run exactly once)

| arm | command (root/rev/work) | exit | receipt |
|---|---|---|---|
| selfcheck at freeze | `--selfcheck --rev 7b63dd5d5199ed30bc3f213573d8594434a18eb6 --work $S/w1` | **1** | `selfcheck-at-freeze.json` |
| selfcheck at base | `--selfcheck --rev 311079d869f068bc083a8d180977e49634120fdf --work $S/w2` | **1** | `selfcheck-at-base.json` |
| recipe a at base | `--recipe a --rev 311079d8… --work $S/w3` | **0** | `recipe-a-at-base.json` |
| recipe stem at base | `--recipe stem --rev 311079d8… --work $S/w4` | **0** | `recipe-stem-at-base.json` |
| equiv at base | `--equiv --rev 311079d8… --work $S/w5` | **0** | `equiv-at-base.json` |

`.stdout` is byte-identical to `.json` in all five arms (stderr empty; exit 1 is the
predicate verdict, not an error).

## Atoms, claimed vs observed (identical at both revisions)

| id | claimed | observed | ok |
|---|---|---|---|
| A1-head-score | 10.0 | 10.0 | true |
| A2-cited-fraction | [142, 142] | [145, 145] | **false** |

`mismatches 1`, `ok false`, `exit 1` at base AND at freeze.

## recipe_a_equivalent

`true` at base; `recipe_a_diffs {}` (empty object) — the committed SCORECARD heredoc,
re-run as a subprocess at the same revision, agrees field for field on all nine
`RECIPE_A_KEYS`. `recipe_a_block_sha256 1d697af103985da0d056f6d0113059891a7658c1a3c4fbf568720166cf44a0db`;
independently re-derived by a separate 29-line extraction of the same heredoc body
(same sha256), so the equivalence is against the bytes now committed.

recipe A at base: `knowledge_files 145`, `mapped 142`, `missing` 3, `dangling 0`,
`citation_resolved_rules 27`, `rule_blocks 27`, `coverage_score 9.79`, `depth_score 10.0`.

## recipe_a_hidden (non-empty, 3)

```
2026-11-03-r65-jsc-closure-matrix
jsc-mapper-cli-contract
jsc-mapper-release-inventory
```

`recipe_a_hidden_count 3`. Recipe A's numerator is `2026-10-\d\d-…` tokens only, so these
three admitted stems can never be mapped by it; the stem recipe maps them and reports
`mapped 145`, `mismatches 0`, `stem_score 10.0`.

## Independent re-derivations (git objects at 311079d8…)

1. knowledge file count —
   `git -C … ls-tree -r --name-only 311079d8… -- corpus/knowledge | grep -c '\.md$'` → **145**
   = counter `knowledge_files 145` and `stem.population 145`. EQUAL.
2. recipe-A missing list (non-October stems) —
   `… ls-tree … | grep '\.md$' | xargs -n1 basename | sed 's/\.md$//' | grep -v '^2026-10-' | sort`
   → the same three names in the same order as `recipe_a.missing` / `recipe_a_hidden`. EQUAL.
3. cited fraction — first `<n>/<n> knowledge files` in the `## Owned axes` coverage row:
   `… show 311079d8…:SCORECARD.md | sed -n '/^## Owned axes/,/^## /p' | grep -m1 '^| coverage |' | grep -o '[0-9]*/[0-9]* knowledge files'`
   → **142/142** = atom A2 `claimed [142,142]`. EQUAL.
   (Independent cross-check: unique `2026-10-…` tokens in the README `## Coverage map`
   section = **142** = counter `recipe_a.mapped 142`.)

Both independent counts equal the counter's; the counter's arithmetic is not the
discrepancy — the SCORECARD row's cited fraction is.

## Base-arm clause

Satisfied: at base the same counter reports A2-cited-fraction as a mismatch (exit 1,
`mismatches 1`). Note it reports the same verdict at the operative freeze, because
`SCORECARD.md` is byte-identical at both revisions (`git diff --name-status 311079d8…
7b63dd5…` lists only `.ufo/waves/round-66/**`, `LOG.md`, `SKILL.md`, `plans/round-66-claims.md`,
`tools/round-66/*`; the `## Queue-drain craft` section of SKILL.md is identical, so
recipe A is unaffected).

## Reproducibility control

`selfcheck-at-base.json` is byte-identical to the pre-freeze dry run
`.ufo/waves/round-66/l1/pre/dryrun-c2-selfcheck-at-base.json` (`cmp` clean).

## Consequence for the claim

R66-C2's first clause (`mismatches 0` across both atoms at the measured revision) is
**not yet true** at either the base or the operative freeze: the row's first cited
fraction is the round-53 landing figure `142/142`, while the repaired stem recipe
observes `145/145`. The predicate can only verify at a revision whose `## Owned axes`
coverage row cites the corrected fraction as its **first** `<n>/<n> knowledge files`
occurrence (`parse_row` uses `re.search`, i.e. first match in the row). No counter edit
is involved or permitted: the repair is a SCORECARD coverage-row edit.
