# ExecRecordRepair — round 86 (kaidoku), R86-C1 repairs

Seat: ExecRecordRepair (executor). L1 KaidokuR86. BASE `2cf0b7ff93c698809bed321f7338276a22d6beb9`.
No production file edited, no commit, no subagent dispatched. Scratch removed after the receipts were copied.
No tools installed or upgraded.

## Outcome

| item | result |
|---|---|
| A2 docstring replacement | done: one docstring line, `--selftest` unchanged (cases=10, failures=0, exit 0) |
| A3 cell replacement | written; **does not reach agreement** (blocker below) |
| A1 supersession row | synthetic row in fixture only; count 7 with ids S079/S080/S083/S090/S092/S119/S123 |
| record-agreement on production-shaped fixture | **agreed 2/3, exit 1** (`A3-receipt-pointer`) |
| record-agreement on conditional fixture (22 other coverage rows renamed, fixture only) | agreed 3/3, exit 0 |

Acceptance asked for `after-fixture.json` at 3/3 exit 0. The production-shaped result is 2/3 exit 1, and I saved
it under that name because it is the honest result. The 3/3 receipt is `after-fixture-unique-rows.json` and is
conditional.

## Blocker (frozen rule vs counter)

A3 cannot be met by a cell-only change. The counter (`tools/round-86/record-agreement.py`,
`atom_receipt_pointer`) requires exactly one line starting `| coverage |`. BASE `SCORECARD.md` has 23
(lines 23, 179, 258, 317, 363, 404, 450, 492, 522, 551, 605, 736, 797, 961, 1059, 1535, 2243, 2301, 2359,
2417, 2506, 2948, 3409). The `| coverage |` row's cells cannot change that count. Satisfying the counter needs
either a rule change after scoring (kill rule) or a history rewrite of 22 rows. I did neither.

The plan's BASE description of A3 ("row claims 85, names only a round-67 receipt") also does not match the bytes.
The row names round-84, -76, -75, -68 and -67 receipts; the counter stops at the uniqueness check first.

## Repairs (exact text in `w1/ExecRecordRepair/repairs.md`)

- A2: `mutation-closure.py` line 8 (1-based). Old `… an absent declared case is inconclusive, never a pass).`
  New `… an absent declared case scores survived, never a pass).` Docstring-only; `diff` shows one line.
- A3: `SCORECARD.md` row 23, cell 3 (pointer) prefixed with `` `.ufo/waves/round-86/l1/scores/coverage-at-landing.json`; ``,
  cell 4 (round) `85 (…round-85 record; …)` → `86 (…round-86 record; …)`. Cell 2 (evidence) untouched.
- A1 (for the real S305, ScribeSources' seat): count must be 7. Do not mention `S303` after `count`; the counter
  collects every `S\d{3,}` there.

## Frontier notes

- S255/S305 are the ScribeSources seat's. The synthetic S305 here matches the BASE registry: 8 rows carry the URL
  (S079/S080/S083/S090/S092/S119/S123/S303), so the other-row count is 7.
- The round-86 receipt `.ufo/waves/round-86/l1/scores/coverage-at-landing.json` does not exist yet. The counter
  checks only that it is a blob at `--rev` with a 40-hex `rev`, not that the rev is the measured tree.

## Checks the main agent should run

- `python3 -I -B tools/round-86/record-agreement.py --root . --rev <rev> --json-out …` after the scribe and the
  L1 land the SCORECARD change. Expect A3 to stay red unless the uniqueness blocker is resolved by the L1.
- `python3 -I -B tools/round-84/mutation-closure.py --selftest` expects `SELFTEST cases=10 failures=0`, exit 0.

## Tooling

No installs. Scratch fixture edits used scripted replacement (Python with `assert count == 1`) on scratch copies
only; production files were not touched.
