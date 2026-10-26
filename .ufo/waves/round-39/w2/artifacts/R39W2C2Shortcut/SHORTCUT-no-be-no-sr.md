# SHORTCUT-no-be-no-sr — best table with no `-be` cell and no `symlink removed` cell

Both hidden columns are `*` on every row. Six rows, one label per block that survives
under {H, G, D, P}. Ties resolved toward the commoner label in each block
(clean 4 vs escaping 2; body-extractor-failure 4 vs avm-marker-be-dropped 2).

## Queue-drain craft

<!-- sqfs-triage-table v1 -->
| label | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | cause -> action | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| no-squashfs-chunk | `none` | `*` | `*` | `*` | `*` | `*` | no squashfs chunk exists -> check the magic and superblock | synthetic bound table, R39W2C2Shortcut |
| dep-missing-be | `*` | `missing-extractor-dependency` | `sasquatch-v4be` | `*` | `*` | `0` | the BE extractor was missing -> install sasquatch-v4be | synthetic bound table, R39W2C2Shortcut |
| dep-missing-le | `*` | `missing-extractor-dependency` | `sasquatch` | `*` | `*` | `0` | the LE extractor was missing -> install sasquatch | synthetic bound table, R39W2C2Shortcut |
| in-tree-symlink-metadata | `*` | `unpublished-entry` | `none` | `*` | `*` | `>0` | an in-tree link is gapped -> expected | synthetic bound table, R39W2C2Shortcut |
| body-extractor-failure | `*` | `extractor-failure` | `none` | `*` | `*` | `0` | the extractor failed on the image -> keep the command and stderr | synthetic bound table, R39W2C2Shortcut |
| clean | `*` | `none` | `none` | `*` | `*` | `>0` | no gap and nothing removed -> nothing to fix | synthetic bound table, R39W2C2Shortcut |
