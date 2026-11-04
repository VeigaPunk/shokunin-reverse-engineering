# Coverage-map consequence — ScribeLesson draft (row text + measured numbers)

## What the counter measures

`tools/round-66/coverage-selfcheck.py --selfcheck --rev <rev>` reads the knowledge population from
`git ls-tree` at `<rev>`, the map from `corpus/README.md`'s `## Coverage map` section, and the cited
fraction from `SCORECARD.md`'s `## Owned axes` `| coverage |` row. Measured today:

| state | population | stem recipe (map) | recipe A (date tokens `2026-10-`) | `A2-cited-fraction` | exit |
|---|---|---|---|---|---|
| `--rev ed68cd0a` (freeze) | 161 | 161/161, missing `[]`, head **10.0** | 142/161, **8.82**, hidden 19 | claimed `[157,157]` vs observed `[161,161]` → **ok false** | **1** |
| `--rev 29d2ca30` (base) | 161 | 161/161, head 10.0 | 142/161, 8.82 | `[157,157]` vs `[161,161]` → ok false | 1 |
| `--rev 749c5717` (round-77 tip) | 159 | 159/159, head 10.0 | 142/159, **8.93**, hidden 17 | `[157,157]` vs `[159,159]` → ok false | 1 |

The `157` is the round-76 count carried in `SCORECARD.md:23` (`157/157 knowledge files mapped at the
round-76 record`). Rounds 77 and 78 landed four entries and neither round restated the pair, so
`A2-cited-fraction` has been `ok false` — and `--selfcheck` exit 1 — since `749c5717`.

## What moves when the L1 lands the one knowledge entry

`corpus/knowledge/2026-11-04-r79-mutation-and-pointers.md` is present in the wave worktree
(untracked, so not yet counted). Once it is committed:

| landing state | stem recipe | head score | verdict |
|---|---|---|---|
| entry landed, **no** map row | 161/162, missing `["2026-11-04-r79-mutation-and-pointers"]` | **9.94** | `A1-head-score` fails |
| entry landed **with** the row below | 162/162, missing `[]` | **10.0** | `A1` holds |

So the row is not cosmetic: without it the head score falls 10.0 → 9.94. Recipe A's own number moves
142/161 (8.82) → 142/162 (**8.77**), because `DATE_TOKEN_RE` matches `2026-10-` only and cannot see a
November stem; that is a property of the transcribed recipe, not of the new entry.

The cited fraction must be restated to the observed pair — **`162/162`, not `158`**: `157` is the
round-76 measurement and was already four entries behind at the round-77 tip. Until
`SCORECARD.md:23` carries `162/162`, `A2-cited-fraction` stays `ok false` and `--selfcheck` keeps
exiting 1 regardless of the map row.

## The row I would add (fleet shape: `section | entries | state`)

```
| Instrument and record layer, round 79 | `2026-11-04-r79-mutation-and-pointers` | held — the selftest mutation battery (eight exact single-occurrence edits to `tools/round-78/attack-gate.py` at the measured rev, each killed only by its own declared selftest case, an absent case a survivor, and `m03`/`m05`/`m08` each caught by that one case alone) and the line-bound pointer binder (five `PROVINCE.md` pointer cells read at the 1-based line or range they name, the pointed lines retained as a sha256, with a committed `path-only` control that cannot fail); the lane's own record layer, not a new carrier class |
```

This is the row text I would add after the round-78 row (`corpus/README.md:119`). The worktree
already carries a variant of it at `corpus/README.md:120`; the text above keeps the same `held …not a
new carrier class` verdict and adds the two facts a reader needs to re-derive the row: the
sole-detector result for the three named mutants, and the `path-only` control.

## Restatement to land beside it

`SCORECARD.md:23` — replace the cited `157/157` with `162/162 knowledge files mapped at the round-79
record` and add the round-79 selfcheck receipt `.ufo/waves/round-79/l1/scores/coverage-selfcheck-at-record.json`
once the L1 has taken it; that is the receipt `A2` is compared against. The edit must be **in place**:
`coverage_row()` splits on the first `## Owned axes` (the file has exactly one, at `SCORECARD.md:19`)
and returns its first `| coverage |` line (line 23), so a second axes table appended at the end is
invisible to the counter. The parser also takes the first `<mapped>/<files> knowledge files` match in
that row, so keeping the round-76 sentence as history is fine only if the current pair comes first.
