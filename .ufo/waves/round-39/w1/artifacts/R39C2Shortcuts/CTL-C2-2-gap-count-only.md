# CTL-C2-2 — gap-count-only table (pre-freeze shortcut control for P39-C2)

Keyed only on whether `normalized_result.extraction_gaps[]` is empty. Every other
condition cell is `*`. The empty-gaps row must come first because the second row's `*`
also matches the empty set.

## Queue-drain craft

<!-- sqfs-triage-table v1 -->

| label | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | cause -> action | source |
|---|---|---|---|---|---|---|---|---|
| clean | * | none | * | * | * | * | no gap -> nothing to triage | CTL-C2-2 gap-count-only |
| dep-missing-be | * | * | * | * | * | * | any gap -> assume the commonest gap class | CTL-C2-2 gap-count-only |

The non-empty label is a free pick: five classes carry gaps (dep-missing-be,
dep-missing-le, in-tree-symlink-metadata, avm-marker-be-dropped,
body-extractor-failure), two envelopes each, so every pick scores the same.

Prediction (N = 14): gaps empty -> `clean` is right for the two clean carriers and wrong
for the two escaping-symlink-removed carriers; gaps non-empty -> right for exactly one of
the five gapped classes (2). Best possible: 4/14.
