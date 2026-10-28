# ScoutQuality — round 48, `corpus/QUALITY.md`

Axes for this seat: coverage (both numberings of rows 75/77/78 against each round-48 defect class), depth (the cell the A1 parser actually searched), calibration (column name, what A1 changed, what was not run).

No tool was installed.

## Answer

The highest row number in the admission table is **87** (`corpus/QUALITY.md:95`). The table's shape is four columns, header `# | criterion | why (lesson) | supersedes` (`corpus/QUALITY.md:9-10`). It is not a two-column table.

Rows 75 and 76 are absent from that table (the numbered rows jump 74 → 77). They exist only as prose bullets in the round-34 corrections appendix (`:135`, `:137`). Appendix bullets at `:139` and `:141` reuse the numbers 77 and 78 for different sentences than table rows 77 and 78 (`:85`, `:86`). The two-part shape among those bullets is appendix 77 and appendix 78: each is one bullet split into halves `(a)` and `(b)`. Appendix 75 and 76 are single bullets.

None of row 75, table 77, appendix 77, table 78, or appendix 78 states the round-48 defect classes below. The class that is new, and the one this seat proposes a row for, is A1: a score-cell clause that is green because the extractor returned no rows.

Proposed admission row, next free number **88**, same four-column shape. It sharpens 66, 84, and 87. It does not replace them. It does not cite "77", because that number is two sentences.

| 88 | A clause that checks named rows is met only when the extractor returns those rows. An empty extraction together with an empty disagreement list is exit 2: the clause has not checked the rows. The value comes from the column the header names. On the Owned-axes table that column is `Baseline → current score`. A search of the next `\|`-separated fragment does not count, and printing `axis_score_cells {}` does not make the empty set a pass. A later index change that parses today's card does not close the clause while a failure is appended only when the disagreement list is non-empty: a score cell that no longer matches `N → N` is silent again. Fails when the named axis rows are still in the card and the extracted set is empty. | Round-48 A1, first freeze `7fe11332781356ec3d5b0b314698de27dd25b50d`. `tools/round-48/record2.py` `axis_scores` searched `cell[1]` and returned `{}` on that commit's `SCORECARD.md`; the score-cell clause (lines 303–315) appends a failing only `if cell_bad`. The shipped forgery `axes-score-cell-off` edits the score fragment `9.72 → 10.0` to `9.72 → 9.0` and is invisible to that search (`bad_axes []`); the same forgery under `cell[0]` marks coverage. A1 `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873` changes only the index to `cell[0]`. On the depth row `cell[1]` is the Observable column; the header's Evidence column is `cell[2]`. On the coverage row a `\|` inside the observable command splits that column, so `cell[1]` is not a header cell. Replacing both score fragments with `absent` still returns `{}` and `failing []` under the A1 function. Worktree receipt `.ufo/waves/round-48/controls/ctl-c2-a1-before.json` (sha256 `c0fda7eca2640b52e75080dec72f9aa29ff19fd9be0da6cbdb64f22b10ecdf89`) records `axis_score_cells {}`, `axis_score_bad []`, and no score-cell line in `failing`. | sharpens 66, 84, 87 |

## Which rows 75 / 77 / 78 cover

`corpus/QUALITY.md` sha256 `d0935c59acea5a0d3b93803b2a6a0682680db27dc4e964a587db9e29e35c5466` (66987 bytes). Admission-table numbers present: 1–74, 77–87. Missing inside the table: 75, 76. Raw `|` split gives 4 cells on every admission row except row 13 (5 cells: the criterion contains `` `grep -o … | wc -l` ``) and row 84 (3 cells: the supersedes cell is absent, `:92`).

| id | where | what that text requires | round-48 class it states |
|---|---|---|---|
| 75 | appendix `:135` only | an axis label matches the surface the bytes move, checked before the freeze | none of the parser, meaning, floor, or quote defects. C1's label is the craft block and C2's is the record; that is label fit, scored nowhere in this report |
| 77 | table `:85` | every statement shape is counted, duplicate keys stay distinct, populations are bounded below by the base, the repaired pointer is the freeze's document | none. The population floor is a count of self-assessment statements |
| 77(a)(b) | appendix `:139` | (a) a new craft block cites `corpus/knowledge/` with a line range; (b) the scored path is executed before freeze | none. Claims clause 7 cites "QUALITY row 77(a)", which is this bullet, because the table row has no `(a)`. (b) holds for a counter that runs and still returns `{}` |
| 78 | table `:86` | a recomputed evidence id is not provenance; a non-author re-run compares the semantic payload | none |
| 78(a)(b) | appendix `:141` | (a) "exactly one token" is `re.fullmatch`, and the token sits alone in the cell the counter reads; (b) a forgery differs in the dimension it names | none. (a) is equality inside a cell already chosen. (b) requires the forgery's bytes to change. Blanking the score cell does change those bytes and the A1 clause stays silent |

Classes in `plans/round-48-claims.md` (worktree includes amendments A1, A2, and A3; HEAD at the read was `f3a7afc42c1da2457ab0ffd1883c5bdb822f2962`) and whether 75/77/78 already state them:

- **R46-CL7** — verdict digits bound, meanings unbound. Not stated above. New relative to these rows. No row proposed here.
- **R47-CL10** — an artefact that does no work still passes; the record counter measures consistency and has no completeness floor. Not stated above. New relative to these rows. No row proposed here.
- **R47-CL1** — counters grade committed bytes and execute their own code from the worktree. Not stated in 75/77/78. Rows 32, 55, and 79 already speak to revision binding. No row proposed here.
- **R47-CL2** — the axes check binds the leading fraction, and the 0–10 score cell is what should be bound. Not stated in 75/77/78. A1 is the attempt to implement this binding. The proposed row is the hole inside that attempt.
- **R47-CL13** — a number quoted from a receipt is unbound. Not stated in 75/77/78. No row proposed here.
- **R47-CL14** — an `axes` correction is inert. Not stated in 75/77/78. Row 87 is the nearer general rule (a clause the instrument does not implement). No row proposed here.
- **A1** — `axis_scores` read the wrong fragment, the extracted set was empty, and the empty disagreement list was a green clause. Not stated above. **This is the new row.**
- **A2** — exit 0 required a success token and the absence of any not-met token, so the word `failing` in a real success line was a false red. Not stated above. No row proposed here.
- **A3** — the census clause compared a derived object with the committed `paths` list, so equality could not hold on a correct census. Not stated above. No row proposed here.

## A1, measured

Owned-axes header at `SCORECARD.md:21`: `Axis | Baseline → current score, 0–10 | Observable and limitation | Evidence / counting command | Last-change round`.

`axis_scores` (`tools/round-48/record2.py:140-156`) matches `^\|\s*(coverage|depth)\s*\|(.*)$` and splits the remainder on every `|`. The first-freeze function searched `cell[1]`. A1 searches `cell[0]`. `git diff` of that function between `7fe11332` and `dc73587` is that index and nothing else.

On `SCORECARD.md` at `7fe11332` (byte-identical to the worktree card at measurement):

- Coverage splits into 6 fragments. Fragment 0 is `9.72 → 10.0`, the only fragment with an `N → N` hit. Fragment 1 starts the Observable cell and stops at the `|` inside `` `git ls-tree … | grep -c` ``. The header's Evidence text (`corpus/README.md`) is fragment 3.
- Depth has no internal `|` and splits into 5 fragments. Fragment 0 is `10 → 10`. Fragment 1 is the Observable cell. Fragment 2 is the Evidence cell (`craft section SKILL.md:…`).

So the fragment A1's prose calls the evidence cell is, on the depth row, the Observable column, and on the coverage row not a header cell at all.

Executed the two function bodies (not the CLI) on that card:

| extractor | card | rows returned | score-clause `failing` |
|---|---|---|---|
| `cell[1]` (first freeze) | genuine | `{}` | `[]` |
| `cell[0]` (A1) | genuine | coverage `9.72 → 10.0` over `138/138`; depth `10 → 10` over `24/24` | `[]` because `round(10 * n / d, 2)` equals the current score |
| `cell[0]` (A1) | both score fragments replaced with `absent` | `{}` | `[]` |
| `cell[1]` on `axes-score-cell-off` | coverage score edited `9.72 → 10.0` → `9.72 → 9.0` (the mutation at `record2.py:400-412`, first matched row only) | `{}` | `[]` |
| `cell[0]` on that same edit | same | coverage current score `9.0` against `138/138`; depth unchanged | coverage |

`cells[2]` inside `_m_axes_cell_off` is the score column of a whole-row split (leading empty, axis name, score). It is the same column as `axis_scores`' `cell[0]`. It is not a second scorer.

The clause loop is `record2.py:303-315`: a failing line is appended only `if cell_bad`. An empty `scores` dict leaves `cell_bad` empty. That transcription was checked equal to those file lines.

Worktree `ctl-c2-a1-before.json` (sha256 `c0fda7eca2640b52e75080dec72f9aa29ff19fd9be0da6cbdb64f22b10ecdf89`) has `"freeze": "7fe11332…"`, `"axis_score_cells": {}`, `"axis_score_bad": []`, and `failing` equal to the seat-floor line, the missing corrections section, and one unbound quote. The score clause is absent from `failing` while the card is `met_target: false` for those other clauses.

The A1 paragraph names `.ufo/waves/round-48/controls/ctl-c2-0-do-nothing.json` as that empty receipt. The worktree bytes at that path (sha256 `f0bf3d66c54b8d954b6f6e0bec2916d31b1afccde806da2ce20ae2260c1ab6be`) carry `"freeze": "dc73587…"`, with coverage and depth both filled, and the same three non-score failures. `git show` of either control path at `7fe11332`, `dc73587`, and `HEAD` exited 128. The controls are untracked. The empty-cell bytes that match the A1 story are `ctl-c2-a1-before.json`.

A1 therefore makes the genuine card's two score cells visible, and makes the shipped decrement forgery visible to this clause. The empty-extraction path is still silent under the A1 function. Full `record2.py` / `meanings.py` CLIs were not run, so this does not say the whole counter exits 0 on a blanked card.

## Receipts

Scratch `$S=/fast/scratch/hyaku/kaidoku-r48/ScoutQuality`, `TMPDIR` and `HYAKU_SCRATCH` set there. Disk-guard status was run first (exit 0; `/fast/scratch/hyaku` 32% used, 546.7G free). Copies of the two JSON receipts are in `.ufo/waves/round-48/w1/ScoutQuality/`.

1. Cell split, both extractors, blanked score, QUALITY census. UTC `2026-10-28T18:54:13Z`. Exit 0. Captured JSON sha256 `e97df17427af4f0c57394152b29ee2b1e101f06cc963be55292743ebfb5f1188`. Command: `python3` heredoc in the lane, reading `git show 7fe11332:tools/round-48/record2.py`, `git show dc73587:tools/round-48/record2.py`, `git show 7fe11332:SCORECARD.md`, and the worktree `SCORECARD.md`, `record2.py`, `corpus/QUALITY.md`. `fn_diff` in that JSON is the one-line `cell[1]` → `cell[0]` change. `cards_same` is true. `clause_lines_303_315_match_transcription` is true.

2. Shipped `axes-score-cell-off` under both indexes. UTC `2026-10-28T18:55:56Z`. Exit 0. Captured JSON sha256 `be81cdea0b54ee542989f4bd68fd892c11ec05a11a4e931878ae5913a6d02b4a`. Command: `python3` heredoc applying the mutation body at `record2.py:400-412` to `git show 7fe11332:SCORECARD.md`.

Not run: `tools/round-48/record2.py` CLI, `tools/round-48/meanings.py` CLI, any fixture repo, any claim score.
