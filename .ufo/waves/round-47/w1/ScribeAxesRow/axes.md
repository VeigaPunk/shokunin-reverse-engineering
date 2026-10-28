# ScribeAxesRow — replacement cells for `## Owned axes` (coverage, depth)

Deliverable: the exact text that replaces the third cell of the `coverage` and `depth`
rows of `SCORECARD.md` `## Owned axes` so that each row's leading fraction equals the
observable at the round-47 landing, with the historical chain preserved and every value
carrying its counting command and revision.

Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Base `13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5`. First landing `e856beb5` (first commit
containing craft block 24, the corrections section and the current axis heads). The
round's measured revision is `a0753786`; the lane head advanced during the seat
(`31b092d1`, then `f7d6e58d`), and both fractions re-measured identical at each. Freeze
re-derived at hand-off
`f54b3b6de9085d3db449ed5d0916296cb29c1f6d` (A6). Rows 23–24 are byte-identical from
`e856beb5` through `f7d6e58d` (rows 23–24 sha256
`bc707ae86104219dcf3827482196da6474c54152dcd600fc81a864b0341ddae4` at both ends).

## 1. Exact replacement

SCORECARD.md, `## Owned axes`, rows at lines 23 (`coverage`) and 24 (`depth`). Replace
each row's whole third cell — the text after the second `|` — with the corresponding
line below. Columns 1, 2, 4, 5 and the historical tail of column 3 stay byte-identical.

The complete replacement rows (both full single-line markdown rows, tail included) are
stored byte-exactly at
`.ufo/waves/round-47/w1/ScribeAxesRow/receipts/cell_lines.txt`
(sha256 `0d89e5433eb98a5494a65056a27f7c5f51290479f1049a6637a651d176d0be3e`).
Validated on generation: the first `\d+/\d+` in each row is `138/138` / `24/24`, each row
has exactly 6 pipes, and the text after the head clause is byte-identical to the landed
row (`assert` in the generator run at 2026-10-28T18:05Z).

### coverage — head clause (the only changed text)

```
138/138 knowledge files mapped at the round-47 head `a0753786` (no knowledge file added or remapped this round; `git ls-tree -r --name-only a0753786 -- corpus/knowledge` counts 138 `.md` files and command A reads `mapped 138`, `missing []`, `dangling []`; unchanged at the first landing `e856beb5` and at `04469ee8`; receipt `.ufo/waves/round-47/w1/ScribeAxesRow/receipts/measure-a0753786.stdout.txt`)
```

Replaces the landed head clause
`138/138 knowledge files mapped at the round-47 landing (`git ls-tree ... <rev> ...` → 138; ... receipt `.ufo/waves/round-47/l1/scores/`)`.
The historical tail from `133/133 knowledge files mapped after the round-41 landing ...`
onwards is unchanged.

### depth — head clause (the only changed text)

```
24/24 queue-drain rule blocks have resolvable file/range citations at the round-47 head `a0753786` (command A and the `axes`-scoring `tools/round-47/record.py` `depth_pair` both read 24 resolved of 24; block 24's `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:40-66` citation, added at `04469ee8`, is why recipe A agrees — at the first landing `e856beb5` recipe A read 23/24; receipt `.ufo/waves/round-47/w1/ScribeAxesRow/receipts/measure-a0753786.stdout.txt`)
```

Replaces the landed head clause
`24/24 ... at the round-47 landing (command A, new block 24 with the exactness table v3, `citation_resolved_rules 24`; receipt `.ufo/waves/round-47/l1/scores/`)`.
The historical tail from `20/20 queue-drain rule blocks ... at e1c83313...` onwards is
unchanged.

## 2. What each value is, with command and revision

Counting command used for every row of the matrix below:

```
python3 -I -B .ufo/waves/round-47/w1/ScribeAxesRow/receipts/measure_axes.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV>
```

`recipe_a` in that script is SCORECARD.md `## Measurement recipes` A verbatim (only the
revision comes from argv, as on the card). `record_pairs` are the frozen counter's own
`coverage_pair` / `depth_pair` (`tools/round-47/record.py`), i.e. the derivation the
`axes` atoms are actually scored by.

| value at the head of the cell | revision | derivation | receipt (stdout sha256) |
|---|---|---|---|
| `138/138` | head `a0753786`; unchanged at `e856beb5`, `04469ee8` | recipe A `mapped 138`, `missing []`, `dangling []`; `record.coverage_pair` `(138, 138)` | `receipts/measure-a0753786.stdout.txt` (`c2da1640…`) |
| `24/24` | head `a0753786` (both derivations); at `e856beb5`–`07d2894e` only `depth_pair` (recipe A read 23/24) | `record.depth_pair` `(24, 24)`; recipe A `citation_resolved_rules 24` / `rule_blocks 24` | same receipt; `receipts/measure-e856beb5.stdout.txt` (`9ff6c59e…`) for the 23/24 probe |
| `133/133` (retained history) | `e1c83313` as written in the cell | command A | cell text unchanged |
| `20/20` (retained history) | `e1c83313f33a3d97edbd8fef402db2d06172fcdc` as written in the cell | command A | cell text unchanged |

Measurement matrix (same command, each revision; all exit 0):

| rev | recipe A coverage | record coverage | recipe A depth | record depth |
|---|---|---|---|---|
| `13a9e9e1` (base) | 138/138 | 138/138 | 23/23 | 23/23 |
| `5017e1f7` (first freeze) | 138/138 | 138/138 | 23/23 | 23/23 |
| `9018c53b` (A1) | 138/138 | 138/138 | 23/23 | 23/23 |
| `e856beb5` (first landing) | 138/138 | 138/138 | **23/24** | **24/24** |
| `1e2c3102` (A4) | 138/138 | 138/138 | **23/24** | **24/24** |
| `07d2894e` (A5) | 138/138 | 138/138 | **23/24** | **24/24** |
| `04469ee8` (block 24 knowledge citation) | 138/138 | 138/138 | **24/24** | **24/24** |
| `a0753786` (measured revision) | 138/138 | 138/138 | **24/24** | **24/24** |
| `31b092d1` (head at hand-off) | 138/138 | 138/138 | **24/24** | **24/24** |

Counters at the measured head:

```
python3 -I -B tools/round-47/record.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev a0753786
python3 -I -B tools/round-47/exact.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --freeze f54b3b6d --rev a0753786
```

`record` exit 0, `mismatches []`, `corrections_bad []`, `met_target true`
(`receipts/record-a0753786.stdout.txt`, sha256 `f80d5805…`). `exact` exit 0,
`forgeries_total 4 / v2_green 4 / v3_green 0 / genuine_green 1 / crash 0`
(`receipts/exact-a0753786-freeze-f54b3b6d.stdout.txt`, sha256 `68ea3e3f…`). Re-measured at
the hand-off head `31b092d1` with the same freeze: `record` `met_target true`,
`mismatches []` (`receipts/record-31b092d1.stdout.txt`, sha256 `d24410d1…`); `exact`
`met_target true` (`receipts/exact-31b092d1-freeze-f54b3b6d.stdout.txt`, sha256
`216f33a8…`); fractions unchanged (`receipts/measure-31b092d1.stdout.txt`, sha256
`4d145bd6…`).

Draft validation (no lane write): `SCORECARD.md` at `a0753786` with lines 23–24 replaced
in memory by `receipts/cell_lines.txt`, everything else unchanged, scored by
`record.evaluate_text` → exit 0, `mismatches []`, `corrections_bad []`, `met_target true`,
`verified 41` (`receipts/draft-validated.stdout.txt`, sha256 `894ffa9d…`).

## 3. Findings

**F1 — the depth derivation is not command A; the two disagreed at the landing (calibration).**
`tools/round-47/record.py:116` documents `depth_pair` as "exactly as command A reads them",
but `record.py:42` is `HARD_REF = (?:corpus|plans|tools)/…`, while SCORECARD
measurement-recipe A (`SCORECARD.md:105`) matches only `corpus/knowledge/(…).md`. At
`e856beb5`, `1e2c3102` and `07d2894e` block 24 cited no `corpus/knowledge` file, so
`depth_pair` returned `(24, 24)` while recipe A returned `citation_resolved_rules 23`,
`rule_blocks 24` at the same revisions. Commit `04469ee8` added
`corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:40-66` to block
24; from `04469ee8` on both derivations read 24/24. Consequences:

1. At `e856beb5`–`07d2894e` the landed depth head clause and the correction lines
   `- corrects axes depth: 24/24 — command A at the round-47 landing → `rule_blocks 24`,
   `citation_resolved_rules 24`` (`SCORECARD.md:3677-3678`) were not reproducible by the
   card's own command A (true value 23/24); the counter stayed green because it reads only
   the leading fraction and re-derives it with `depth_pair`. From `04469ee8` the sentence
   is reproducible.
2. The frozen claims row for `axes` (`plans/round-47-claims.md:154`) still says the depth
   atom is "command A's citation-resolution count", which misdescribes the frozen scorer.
3. Structural forgery surface (unchanged by the `04469ee8` repair): a craft block whose
   only citation is the counter itself scores as a resolved depth block under `depth_pair`
   and as unresolved under recipe A. Isolated one-commit fixture: `record_depth_pair
   (1, 1)` vs `recipe_a 0/1`, `divergence true`
   (`receipts/fixture-selfcite.stdout.txt`, sha256 `0e5e13f8…`; fixture removed with the
   scratch root). The axis is movable by a non-domain citation; only the current block's
   own knowledge citation keeps the two readings equal.
4. The coverage head clause and the `- corrects axes coverage` line
   (`SCORECARD.md:23`, `:3675-3676`) still embed a literal `<rev>` placeholder in the
   `git ls-tree` command; my draft replaces it with the measured revision.

Recommendation (does not touch frozen bytes): keep the fraction `24/24` and state
`depth_pair` plus command A as two named derivations (as in my draft); widen recipe A to
the counter's `HARD_REF` or narrow `depth_pair` to `corpus/knowledge` so the two cannot
diverge again; replace `<rev>` with the measured revision.

**F2 — R47-C1 failed at the first landing and passed only after A2 (depth).**
At `e856beb5` with the then-declared freeze `9018c53b`, `tools/round-47/exact.py --profile v3`
exits 1 with
`arm cells not exact vocabulary tokens: ['symbol: the arm cell must equal one token …', 'once: …', "digest: …", "order: …"]`
(`receipts/exact-e856beb5-freeze9018c53b.stdout.txt`, sha256 `26fade63…`; `battery` skipped:
"artefact fails a structural clause first"). Commit `62e33f7d` (A2) reduced the four arm
cells to bare tokens; at `a0753786`/freeze `f54b3b6d` exact exits 0 with the battery green
under v3 and all four forgeries green under v2.

**F3 — the freeze is a disclosed seven-commit series, not the seat prompt's `5017e1f`.**
`git log --format=%H -1 -- plans/round-47-claims.md tools/round-47/` prints
`f54b3b6d…` (A6) at hand-off. The `## Round 47` section (at `31b092d1`) records the series
`5017e1f7`, `9018c53b` A1, `62e33f7d` A2, `2e4ae43` A3, `1e2c310295` A4, `07d2894e` A5,
`f54b3b6d` A6, declares **A6 as the freeze**, and measures both claims at `a0753786`
(`c1-at-A7.json`, `c2-at-A7.json`). `exact.py` and `record.py` changed at A6, so
`exact.py --freeze 07d2894e --rev a0753786` exits 2
`frozen_path_changed ["tools/round-47/", "tools/round-47/exact.py"]`
(`receipts/exact-07d2894e-freeze07d2894e-at-a0753786-stale.stdout.txt`, sha256
`24abc378…`); `--freeze 5017e1f` fails the same way. The seat prompt's freeze hash is
therefore stale at measurement time; the counter's freeze must be re-derived by the
command above and is `f54b3b6d` for the measured revision `a0753786`.

**F4 — evidence paths (record).** The landed cells cite the directory
`.ufo/waves/round-47/l1/scores/` rather than a file; it was empty at 14:52Z and populated
by 18:00Z. My draft cites the actual receipt for the measured revision.

## 4. Artifacts

- `receipts/cell_lines.txt` — the two byte-exact replacement rows (sha256 `0d89e543…`).
- `receipts/measure_axes.py` — recipe A verbatim + the counter's `coverage_pair`/`depth_pair`.
- `receipts/fixture_selfcite.py` — the isolated self-citation depth fixture.
- `receipts/validate_draft.py` — in-memory substitution + `record.evaluate_text` scorer.
- `receipts/runs.jsonl` — one line per command: exact argv, cwd, UTC, exit, stdout sha256.
- `receipts/*.stdout.txt` — captured output for every run cited above.
- `ScribeAxesRow.md` — the seat report.
