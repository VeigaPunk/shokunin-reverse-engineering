# R45W1RegRowFormat — registry-row format the frozen R45-C2 counter accepts

Seat: `R45W1RegRowFormat`. Read-only on the lane. Frozen instrument not modified.

Axes checked: (1) what `parse_rows` / `ROW_TOOL` / `exits_ok` actually accept, (2) bare-filename vs full-path census, (3) a byte-stable append point, (4) whether headings scope a table.

## Verdict

On the **worktree** `SKILL.md` (HEAD `faa875bc0eb839d15b83c4afa6078819e5a7b381`, blob `1e0b46f6abd401940ed03dc8622f706fa4947645`, clean vs `git hash-object`), **all six** scope paths already have a matching row. Each first cell is exactly the backticked path, each third cell names `0`, `1` and `2`, none is thin.

On the **freeze blob** `f762b7273e3f6ca3c710bb37d5de92a4a4417aec:SKILL.md` the same six paths match **nothing**. The `### Round-44/45 instrument registry` section is not in the freeze; it was appended in `e715263cb51b713c342ab992d527fe9d61d6f8ff` (2026-10-28 12:33:03 -0300). Amendment `1f4b27f8` shifted that heading from line 1617 to line 1623 (net +6 lines earlier in the file) and did not edit the registry hunk.

`evaluate()` was **not run**. Row matching below is `parse_rows` + `exits_ok` imported from the frozen `tools/round-45/c2-counter.py`.

## Accepted row (source)

`tools/round-45/c2-counter.py:31` and `:43-60`, `:95-108`.

ROW_TOOL (c2-counter.py:31) is a search for a backtick, then `tools/`, then one or more of `[A-Za-z0-9._/-]`, then `.py` or `.sh`, then a backtick. Group 1 is the path with the backticks removed. It is not anchored to the whole cell.

`parse_rows` keeps a line only when `strip()` starts with `|`, the naive `|` split yields at least 3 cells, and `ROW_TOOL.search(cells[0])` hits. The captured group is the tool path. `exits_ok(cell)` is true iff the cell matches word-boundary `0` and `1` and `2`.

`evaluate` keys `by_tool.setdefault(row["tool"], row)` then `by_tool.get(path)` against `registry-scope.json` `paths`. The exit check is **always `cells[2]`** (third column), not a header named "exit". Comment at line 106.

A scope path is registered iff some parsed row's captured group **equals** that path. It is not thin iff `cells[2]` contains word-boundary `0` and `1` and `2`.

Green fixture the counter itself builds (lines 141-145 and 166):

```
| `{path}` | gate — test | `0` met; `1` not met; `2` unevaluable | `--selftest` |
```

Header in that fixture is `| tool | gate | exits | selftest |`, so exits sit in column 3. The landed section uses the same index with a wider header:

`| tool | gate or probe | verdict map (exit codes) | self-test command | pinned-value path | write scope | owner |`

### What the regex does, probed in-process (not a counter exit)

| probe | parse_rows result |
|---|---|
| bare `` `c1-counter.py` `` with 0, 1 and 2 in column 3 | no row |
| exact `` `tools/round-45/c2-counter.py` `` with 0, 1 and 2 in column 3 | tool captured, exits_ok true |
| path with no backticks | no row |
| spaces inside the backticks | no row |
| prose before the backticked path in cell 0 | still captured — search, not full-cell equality |
| cell 2 = `non-zero` | row kept, exits_ok false (thin). Selftest `red-thin-exit-cell` uses `` `0` met; non-zero otherwise `` |
| exits only in column 4 (tool, purpose, command, 0/1/2) | row kept, cells[2] is the command, exits_ok false |
| `.json` path | no row (extension must be py or sh) |
| row under a `# Notes` heading, not a registry heading | still captured |
| bare row then a later full-path row, two tables, one Round-40 heading | only the full-path row |

`parse_rows` does **not** dedupe. `evaluate` keeps the **first** row per path (`setdefault`). A later good exit cell does not repair an earlier thin row for the same path. Worktree has 45 parsed rows and 45 unique tools, so nothing is shadowed today.

Round-30 shape is the trap: `tools/round-30/c1-rust-positive.py` at worktree line 1277 is a parsed row (5 cells) but `cells[2]` is the command (`exits_ok` false) and `cells[3]` is the exit cell (`exits_ok` true). A scope path copied into that 5-column order would be **thin**. The six landed rows are 7 cells with exits in `cells[2]`.

Pipes inside a cell would shift `cells[2]` (split is naive). The six landed exit cells contain no raw pipe.

Claim prose ("first cell is exactly that path") is tighter than the code. The six landed cells happen to be exact backtick-only paths, no extra prose in cell 0.

## (a) Bare filename vs full path

Classifier (mine, not the counter): a data row under a heading whose text contains `registry`, skipping separator rows and header cells `tool` / `name…`. Bare = cell 0 is a backticked basename `.py` or `.sh` with no slash. Full = `ROW_TOOL` hit. Same bare/full split at the freeze except the six new rows.

| | worktree SKILL.md | freeze blob |
|---|---|---|
| lines / sha256 | 1645 / `19c209275bfff45f8ccdfb34af8273e9d742e397360c6ae13a4d938951d6a7a5` | 1572 / `32fb1a265da04c07c958cf04a4f4552bdec94fb527ef863cf1e08e313c03b724` |
| parse_rows hits (full `tools/…py` or `.sh` in cell 0) | **45** | **39** |
| bare filename cell 0 | **12** | **12** |
| other registry data rows (display name in cell 0) | 36 | 36 |
| scope paths matched | **6/6**, all exits_ok | **0/6** |

Bare rows are **only** `### Round-40 instrument registry` (heading line 1604), lines 1610-1621:

`c1-counter.py`, `c1-extra.py`, `fetch-vendor.py`, `sqfs-list.py`, `gen-squashfs.py`, `mk-l-carriers.py`, `c1-run.sh`, `sqfs-triage-v2.py`, `heldout-gen-v2.py`, `c2-counter.py`, `score-receipt.sh`, `ledger-status.py`.

None of those strings equals a scope path. `parse_rows` drops all 12. Round-40 `c1-counter.py` does not register `tools/round-44/c1-counter.py` or `tools/round-45/c1-counter.py`.

Full-path rows by section (worktree):

| section | rows |
|---|---|
| Round-30 measurement registry | 6 |
| Round-31 measurement registry | 5 |
| Round-34 run-6 instrument registry | 5 |
| Round-36 instrument registry | 2 |
| Round-35/37/38/39 instrument registry | 21 |
| Round-44/45 instrument registry | 6 |
| outside any registry heading | 0 |

Scope hits (worktree only), all exact backtick cells and cells[2] has 0, 1 and 2:

| path | line |
|---|---|
| `tools/round-44/c1-counter.py` | 1636 |
| `tools/round-44/c1-run.sh` | 1637 |
| `tools/round-44/c2-counter.py` | 1638 |
| `tools/round-45/frozen-path-preflight.py` | 1639 |
| `tools/round-45/c1-counter.py` | 1640 |
| `tools/round-45/c2-counter.py` | 1641 |

The 36 other rows are name-first tables (rounds 22-29, 32, 33, 34 main, and the local gate registry). The counter never sees them.

## (b) Where a new section can be appended without moving an existing section

**Current file.** The heading asked for is **already present** at line 1623 (`### Round-44/45 instrument registry`), after the blank line 1622 that follows the Round-40 table's last row (line 1621, `` `ledger-status.py` ``). Bytes of that section start at offset 255437 (end of line 1622). File ends at line 1645 with a trailing newline (259477 bytes). Last line: `unregistered until a round censuses them (R45-CL3).`

The only append that leaves every existing section's bytes alone is **after line 1645 (EOF)**. Preceding heading: `### Round-44/45 instrument registry` at line 1623. A second copy of that heading there would not be required for the predicate (the six rows already match) and would not move lines 1-1645.

Inserting another table **under** the Round-40 heading (between line 1621 and line 1623) **does** move the Round-44/45 section.

**Freeze file (the pre-landing slot).** Ended at line 1572 on the `` `ledger-status.py` `` row, trailing newline, no blank line after the table. Preceding heading: `### Round-40 instrument registry` at freeze line 1555. That EOF was the byte-stable place to append. The land commit used it. Freeze line numbers are not the worktree's: `e715263c` put the new heading at 1617; `1f4b27f8` moved it to 1623.

## (c) Second table under Round-40 — does the counter care about headings?

**No.** `parse_rows` never reads headings, blank lines, or table boundaries. The function body cited above is the whole scan. A second markdown table placed directly under `### Round-40 instrument registry` is **not** joined to that table as a table. Its data rows are just more lines. A row whose cell 0 matches `ROW_TOOL` is kept; the bare Round-40 rows stay ignored; header and `|---|` lines do not match. Probe `two_tables` (bare `c1-counter.py` under that heading, then a second table with `tools/round-45/c1-counter.py`) returned only the full path, `exits_ok` true.

So a second table of the six **full** paths, exits in column 3, would satisfy `unregistered` / `thin` wherever it sits, including under the Round-40 heading. A second table of bare names would not. Headings do not partition the row set, and the first row for a path wins.

## Receipt

In-process import of frozen `tools/round-45/c2-counter.py` (`parse_rows`, `ROW_TOOL`, `exits_ok`) on worktree `SKILL.md` and `git show f762b7273e3f6ca3c710bb37d5de92a4a4417aec:SKILL.md`, plus the probes above. UTC `2026-10-28T15:40:58Z`. The JSON summary's sha256 is `6ba1612d0f94c3d77e0eade0ee695b9d5e33fe4613151ef6c8962ebd283fb4a1`. No install. `c2-counter.py` was not executed as a scorer (`--selftest` / `evaluate` not run).

Git (read-only), exit 0 unless noted:

- `git rev-parse HEAD` -> `faa875bc0eb839d15b83c4afa6078819e5a7b381`
- `git hash-object SKILL.md` = `git rev-parse HEAD:SKILL.md` = `1e0b46f6abd401940ed03dc8622f706fa4947645` (worktree clean for this path)
- `git merge-base --is-ancestor f762b727… HEAD` -> exit 0
- `git log --oneline f762b727…HEAD -- SKILL.md` -> `1f4b27f8` then `e715263c`
- `git grep -n '### Round-44/45' e715263c -- SKILL.md` -> line 1617
- `git grep -c 'Round-44/45' e715263c^ -- SKILL.md` -> no match (exit non-zero)
- `git diff --stat e715263c 1f4b27f8 -- SKILL.md` -> 8 lines, +7/-1; diff hunks did not contain the registry heading

## Unknowns

- Counter exit at HEAD was not measured. The six rows meet the two row clauses as `parse_rows`/`exits_ok` implement them; `scope_size`, freeze-ancestry, and `frozen_path_changed` were not scored here.
- Whether every Round-40 bare row's column 3 would pass `exits_ok` if the first cell were rewritten to a `tools/round-40/…` path: not measured, because those cells never enter `parse_rows`.
