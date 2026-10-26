# CTL-C2-3 — gap-kind-only table (pre-freeze shortcut control for P39-C2)

Keyed only on `extraction_gaps[].kind`; handler, dependencies, `-be`, symlink removal and
published-file count are all `*`. One row per gap-kind group observed in recon:
`none` (clean + escaping), `unpublished-entry` (in-tree), `missing-extractor-dependency`
(dep-missing-be + dep-missing-le), `extractor-failure` (avm-marker + body failure).

## Queue-drain craft

<!-- sqfs-triage-table v1 -->

| label | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | cause -> action | source |
|---|---|---|---|---|---|---|---|---|
| clean | * | none | * | * | * | * | no gap -> nothing to triage | CTL-C2-3 gap-kind-only |
| in-tree-symlink-metadata | * | unpublished-entry | * | * | * | * | symlink kept as metadata -> do not chase | CTL-C2-3 gap-kind-only |
| dep-missing-le | * | missing-extractor-dependency | * | * | * | * | dependency gap -> install the extractor | CTL-C2-3 gap-kind-only |
| avm-marker-be-dropped | * | extractor-failure | * | * | * | * | extractor failed -> treat as marker drop | CTL-C2-3 gap-kind-only |

Labels for the two ambiguous groups are free picks (each group holds two classes with two
envelopes each), so the score does not depend on which one is named.

Prediction (N = 14): `none` -> 2 right (clean) + 2 wrong (escaping);
`unpublished-entry` -> 2; `missing-extractor-dependency` -> 2 (one of two classes);
`extractor-failure` -> 2 (one of two classes). Total 8/14. Four gap-kind groups cap this
shape at 2 per group, so 8 is its maximum.
