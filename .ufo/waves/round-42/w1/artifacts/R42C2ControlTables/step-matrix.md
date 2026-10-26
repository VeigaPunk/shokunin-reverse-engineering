# R42-C2 control step matrix (A1 grammar, 15 precedence steps)

Cell = number of DEV envelopes whose expected step is that column and whose
observed (label, action) pair differs. `matched` reproduces the scorer row.
Arm: 76 envelopes (.ufo/waves/round-41/controls/c2/dev, .ufo/waves/round-42/w1/artifacts/R42C2ControlTables/dev-legacy).
Interpreter: `.ufo/waves/round-42/w1/artifacts/R42C2ControlTables/v4-check-interp.py`; evaluator: `.ufo/waves/round-42/w1/artifacts/R42C2ControlTables/preview-precedence.py`.

| control | exit | matched | combo | named | s1 | s2 | s3 | s4 | s5 | s6 | s7 | s8 | s9 | s10 | s11 | s12 | s13 | s14 | s15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `CTL-C2-0-base-SKILL.md` | 2 | 0/76 | 0/12 | 0/64 | 2 | 1 | 2 | 7 | 16 | 2 | 6 | 4 | 1 | 9 | 3 | 3 | 3 | 17 | 0 |
| `CTL-C2-0b-v3-table-v4-marker.md` | 2 | 0/76 | 0/12 | 0/64 | 2 | 1 | 2 | 7 | 16 | 2 | 6 | 4 | 1 | 9 | 3 | 3 | 3 | 17 | 0 |
| `CTL-C2-0c-v3-rows-13col.md` | 0 | 56/76 | 12/12 | 44/64 | 0 | 1 | 0 | 1 | 0 | 0 | 6 | 0 | 1 | 1 | 0 | 0 | 0 | 10 | 0 |
| `CTL-C2-1-catch-all.md` | 0 | 17/76 | 0/12 | 17/64 | 0 | 1 | 2 | 7 | 16 | 2 | 6 | 4 | 1 | 9 | 3 | 3 | 3 | 2 | 0 |
| `CTL-C2-10-no-container-residue.md` | 0 | 74/76 | 12/12 | 62/64 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| `CTL-C2-3-actions-rotated.md` | 0 | 2/76 | 0/12 | 2/64 | 0 | 1 | 2 | 7 | 16 | 2 | 6 | 4 | 1 | 9 | 3 | 3 | 3 | 17 | 0 |
| `CTL-C2-4-exact-gap-sets.md` | 0 | 60/76 | 8/12 | 52/64 | 0 | 0 | 0 | 2 | 10 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 |
| `CTL-C2-7-lookup.md` | 0 | 76/76 | 12/12 | 64/64 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `CTL-C2-7b-lookup-majority-fallback.md` | 0 | 61/76 | 12/12 | 49/64 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 15 | 0 |
| `CTL-C2-7c-lookup-discovery-order.md` | 0 | 66/76 | 10/12 | 56/64 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 9 | 0 | 0 | 0 | 0 | 0 |
| `CTL-C2-7x-lookup-exact-tuples.md` | 0 | 27/76 | 2/12 | 25/64 | 0 | 0 | 0 | 3 | 14 | 0 | 5 | 2 | 0 | 7 | 1 | 2 | 2 | 13 | 0 |
| `CTL-C2-8-no-legacy-row.md` | 0 | 70/76 | 12/12 | 58/64 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `CTL-C2-9-v4-handler-glob.md` | 0 | 2/76 | 0/12 | 2/64 | 0 | 1 | 2 | 7 | 16 | 2 | 6 | 4 | 1 | 9 | 3 | 3 | 3 | 17 | 0 |
| `SKILL.md (live v3 table)` | 2 | 0/76 | 0/12 | 0/64 | 2 | 1 | 2 | 7 | 16 | 2 | 6 | 4 | 1 | 9 | 3 | 3 | 3 | 17 | 0 |

Expected-step census: `{"1": 2, "10": 9, "11": 3, "12": 3, "13": 3, "14": 17, "2": 1, "3": 2, "4": 7, "5": 16, "6": 2, "7": 6, "8": 4, "9": 1}`

The reference row (`CTL-C2-REF`) is omitted: it is the reachability witness,
not a control.

## The same controls on the v4-only slice (52 round-41 dev envelopes)

| control | exit | matched |
|---|---|---|
| `CTL-C2-0-base-SKILL.md` | 2 | 0/52 |
| `CTL-C2-0b-v3-table-v4-marker.md` | 2 | 0/52 |
| `CTL-C2-0c-v3-rows-13col.md` | 0 | 52/52 |
| `CTL-C2-1-catch-all.md` | 0 | 6/52 |
| `CTL-C2-10-no-container-residue.md` | 0 | 52/52 |
| `CTL-C2-3-actions-rotated.md` | 0 | 2/52 |
| `CTL-C2-4-exact-gap-sets.md` | 0 | 38/52 |
| `CTL-C2-7-lookup.md` | 0 | 52/52 |
| `CTL-C2-7b-lookup-majority-fallback.md` | 0 | 52/52 |
| `CTL-C2-7c-lookup-discovery-order.md` | 0 | 44/52 |
| `CTL-C2-7x-lookup-exact-tuples.md` | 0 | 23/52 |
| `CTL-C2-8-no-legacy-row.md` | 0 | 52/52 |
| `CTL-C2-9-v4-handler-glob.md` | 0 | 2/52 |
| `CTL-C2-REF-v4-precedence.md` | 0 | 52/52 |
| `SKILL.md (live v3 table)` | 2 | 0/52 |

