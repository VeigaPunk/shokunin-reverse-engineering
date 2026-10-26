# CTL-C2-4 — published-only table (pre-freeze shortcut control for P39-C2)

Keyed only on `len(normalized_result.files)`; every other condition cell is `*`. The two
conditions are disjoint (`0` vs `>0`), so row order does not matter.

## Queue-drain craft

<!-- sqfs-triage-table v1 -->

| label | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | cause -> action | source |
|---|---|---|---|---|---|---|---|---|
| clean | * | * | * | * | * | >0 | files published -> nothing to triage | CTL-C2-4 published-only |
| dep-missing-be | * | * | * | * | * | 0 | nothing published -> assume dependency gap | CTL-C2-4 published-only |

The zero-file label is a free pick: four classes publish nothing (dep-missing-be,
dep-missing-le, avm-marker-be-dropped, body-extractor-failure).

Prediction (N = 14): `>0` -> 2 right (clean) + 4 wrong (escaping, in-tree);
`0` -> 2 right (one of four classes). Total 4/14; two disjoint groups cap this shape at 4.
