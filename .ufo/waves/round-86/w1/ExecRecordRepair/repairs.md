# ExecRecordRepair — C1 repair texts (candidates; no production file edited)

BASE: `2cf0b7ff93c698809bed321f7338276a22d6beb9`. Each text below was applied in a scratch copy only,
never in the lane tree, and never committed.

## A2-docstring-status — `tools/round-84/mutation-closure.py`, module docstring, line 8 (1-based)

Old line 8 (exact, `cat -A` confirmed; the line ends with `pass).` and a newline):

```text
present in the target's own output; an absent declared case is inconclusive, never a pass).
```

New line 8:

```text
present in the target's own output; an absent declared case scores survived, never a pass).
```

- Docstring-only: `diff` of BASE vs the replacement copy shows exactly one changed line (`8c8`).
- Sentence the counter extracts: `an absent declared case scores survived, never a pass).`
  (`status "survived"`, `conflicting_words []`, verified in the fixture receipt).
- Status word is the literal `survived`, the status the code assigns at its `elif not case_present:`
  branch (`entry["status"] = "survived"`), which the counter reads.

## A3-receipt-pointer — `SCORECARD.md`, row 23, `| coverage |` (last two cells, 0-indexed cells 3 and 4)

The row has five cells (`coverage` | `9.72 → 10.0` | evidence | pointer | round). Only cells 3 and 4
change; cell 2 (evidence) is kept byte-for-byte.

Cell 3 (pointer), old:

```text
`corpus/README.md` Coverage map; `tools/round-66/coverage-selfcheck.py --selfcheck` (atoms A1/A2, `recipe_a_equivalent`, `recipe_a_hidden`); the command A transcript re-run by `--equiv`
```

Cell 3 (pointer), new:

```text
`.ufo/waves/round-86/l1/scores/coverage-at-landing.json`; `corpus/README.md` Coverage map; `tools/round-66/coverage-selfcheck.py --selfcheck` (atoms A1/A2, `recipe_a_equivalent`, `recipe_a_hidden`); the command A transcript re-run by `--equiv`
```

Cell 4 (round), old:

```text
85 (self-assessment fraction re-derived at the round-85 record; score unchanged)
```

Cell 4 (round), new:

```text
86 (self-assessment fraction re-derived at the round-86 record; score unchanged)
```

Result: the row's own round R = 86 (leading integer of its last cell); the path regex finds
`.ufo/waves/round-86/l1/scores/coverage-at-landing.json`, the newest round named, so M = 86 >= R.

## A1-s303-supersede-count (not one of the two repairs requested, but required for the fixture) — `corpus/SOURCES.md`

Appended after the last registry row (`| S304 |`, BASE line 220). Frozen rule reads the newest row whose
`teaches` opens `supersedes S303`. The BASE SOURCES has 8 rows carrying `rea-agents-6.5.0.tgz`
(S079, S080, S083, S090, S092, S119, S123, S303), so the other-row count is **7**.

Synthetic row used in the fixture (the real S305 is the ScribeSources seat's to write):

```text
| S305 | rea-agents 6.5.0 package tarball supersession record — https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz | code | A | Supersedes the S303 prior-row count | Opened 2026-11-04; S303 stated five scopes while the URL is held by seven other rows | supersedes S303 — corrected prior-row count 7 (S079/S080/S083/S090/S092/S119/S123) | rejected | 2026-11-04 | on-release | corpus/lessons/round-86.md |
```

Caution for the real row: the counter collects every `S\d{3,}` after the word `count` as an id. Mentioning
`S303` anywhere after `count` (for example `S303 kept as written`) puts S303 in `declared_ids` and fails A1.
I hit this in the first fixture build and removed it.

## Fixture proof

Scratch fixture (`fxA`) = BASE `corpus/SOURCES.md`, `tools/round-84/mutation-closure.py`, `SCORECARD.md`,
plus the A2, A3 and synthetic S305 replacements above, plus
`.ufo/waves/round-86/l1/scores/coverage-at-landing.json` carrying a 40-hex `rev`.

Command: `python3 -I -B tools/round-86/record-agreement.py --worktree <fxA> --root <fxA> --json-out <receipt>`

| receipt | agreed | mismatches | exit |
|---|---|---|---|
| `after-fixture.json` (production-shaped SCORECARD, the repair above) | 2/3 | `A3-receipt-pointer` | 1 |
| `after-fixture-unique-rows.json` (conditional, see blocker) | 3/3 | none | 0 |

A1 and A2 agree in both. A3 fails in the production-shaped fixture for a reason no cell edit reaches (below).

## BLOCKER — A3 cannot be met by a cell-only change

`tools/round-86/record-agreement.py` `atom_receipt_pointer` begins with
`rows = [line ... if line.startswith("| coverage |")]` and returns `expected exactly one | coverage | row`
unless `len(rows) == 1`. BASE `SCORECARD.md` has **23** lines starting with `| coverage |`
(lines 23, 179, 258, 317, 363, 404, 450, 492, 522, 551, 605, 736, 797, 961, 1059, 1535, 2243, 2301,
2359, 2417, 2506, 2948, 3409). The counter's detail for A3 at BASE and after the repair is the same:
`expected exactly one `| coverage |` row, found 23`.

So the A3 target `mismatches` empty cannot be reached by editing the `| coverage |` row's cells. The only
ways to make the counter agree:
1. change the counter's uniqueness rule (after scoring, so it is a rule change that the plan's kill rule forbids), or
2. rewrite the leading cell of the 22 historical coverage rows (history rewrite, outside a cell-only repair).

The fixture-B variant renames those 22 rows to `| coverage-hist |` in the fixture copy only. It is a proof of
the cell logic only, not a repair. I did not apply either option to production.

Also: the frozen plan's BASE description of A3 ("row claims round 85 and names only a round-67 receipt") does
not match the BASE bytes. The row names `round-84`, `round-76`, `round-75`, `round-68` and `round-67` receipts. The round-53 and round-51 mentions are git pointers, not `l1/scores` receipts. The counter stops at
the uniqueness check before it reads them.
