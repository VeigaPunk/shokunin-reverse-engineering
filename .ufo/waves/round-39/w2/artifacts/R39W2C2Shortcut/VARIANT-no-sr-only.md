# VARIANT-no-sr-only — best table keeping only `-be in child argv`

`symlink removed` is `*` on every row. The clean and escaping envelopes merge (both
`-be` `n/a`), so the block takes `clean` (4 of 6); the AVM and body envelopes split by
`-be` `no` / `yes`. Ceiling 18/20.

## Queue-drain craft

<!-- sqfs-triage-table v1 -->
| label | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | cause -> action | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| no-squashfs-chunk | `none` | `*` | `*` | `*` | `*` | `*` | no squashfs chunk exists -> check the magic and superblock | synthetic bound table, R39W2C2Shortcut |
| dep-missing-be | `*` | `missing-extractor-dependency` | `sasquatch-v4be` | `n/a` | `*` | `0` | the BE extractor was missing -> install sasquatch-v4be | synthetic bound table, R39W2C2Shortcut |
| dep-missing-le | `*` | `missing-extractor-dependency` | `sasquatch` | `n/a` | `*` | `0` | the LE extractor was missing -> install sasquatch | synthetic bound table, R39W2C2Shortcut |
| in-tree-symlink-metadata | `*` | `unpublished-entry` | `none` | `n/a` | `*` | `>0` | an in-tree link is gapped -> expected | synthetic bound table, R39W2C2Shortcut |
| avm-marker-be-dropped | `*` | `extractor-failure` | `none` | `no` | `*` | `0` | the extractor ran without -be on a BE image -> AVM marker artefact | synthetic bound table, R39W2C2Shortcut |
| body-extractor-failure | `*` | `extractor-failure` | `none` | `yes` | `*` | `0` | the extractor ran with -be and failed -> keep the command and stderr | synthetic bound table, R39W2C2Shortcut |
| clean | `*` | `none` | `none` | `n/a` | `*` | `>0` | no gap and nothing removed -> nothing to fix | synthetic bound table, R39W2C2Shortcut |
