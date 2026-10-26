# MIN-8row-7cell — smallest grammar table that labels all 20 held-out envelopes

Eight rows (the floor: eight distinct labels, one per row) and seven non-`*` cells
(the floor: only the last row may be all-`*`, since an all-`*` row placed earlier makes
every later row unreachable). Seven one-cell lookups, then a default row that catches
the remainder (`clean`).

## Queue-drain craft

<!-- sqfs-triage-table v1 -->
| label | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | cause -> action | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| no-squashfs-chunk | `none` | `*` | `*` | `*` | `*` | `*` | no squashfs chunk exists -> check the magic and superblock | synthetic minimal table, R39W2C2Shortcut |
| escaping-symlink-removed | `*` | `*` | `*` | `*` | `yes` | `*` | a link escaped the extraction root and was removed -> expect the path absent | synthetic minimal table, R39W2C2Shortcut |
| dep-missing-be | `*` | `*` | `sasquatch-v4be` | `*` | `*` | `*` | the BE extractor was not on the child PATH -> install sasquatch-v4be and rerun | synthetic minimal table, R39W2C2Shortcut |
| dep-missing-le | `*` | `*` | `sasquatch` | `*` | `*` | `*` | the LE extractor was not on the child PATH -> install sasquatch and rerun | synthetic minimal table, R39W2C2Shortcut |
| in-tree-symlink-metadata | `*` | `unpublished-entry` | `*` | `*` | `*` | `*` | an in-tree link is kept as metadata and gapped -> expected, not a failure | synthetic minimal table, R39W2C2Shortcut |
| avm-marker-be-dropped | `*` | `*` | `*` | `no` | `*` | `*` | the extractor ran without -be on a BE image -> AVM marker artefact | synthetic minimal table, R39W2C2Shortcut |
| body-extractor-failure | `*` | `extractor-failure` | `*` | `*` | `*` | `*` | the extractor failed on the body or header -> keep the command and stderr | synthetic minimal table, R39W2C2Shortcut |
| clean | `*` | `*` | `*` | `*` | `*` | `*` | nothing above matched and no gap was recorded -> nothing to fix | synthetic minimal table, R39W2C2Shortcut |
