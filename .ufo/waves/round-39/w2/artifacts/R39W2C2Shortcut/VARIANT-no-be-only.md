# VARIANT-no-be-only — best table keeping only `symlink removed`

`-be in child argv` is `*` on every row. Blocks under {H, G, D, SR, P}: the clean and
escaping envelopes are still merged (both record `n/a` for `-be`), the AVM and body
envelopes are split by SR? No — both are SR `no`, so they stay merged and the label
must be chosen (body 4). Ceiling 18/20.

## Queue-drain craft

<!-- sqfs-triage-table v1 -->
| label | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | cause -> action | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| no-squashfs-chunk | `none` | `*` | `*` | `*` | `*` | `*` | no squashfs chunk exists -> check the magic and superblock | synthetic bound table, R39W2C2Shortcut |
| escaping-symlink-removed | `*` | `*` | `*` | `*` | `yes` | `>0` | a link escaped the root and was removed -> expect it absent | synthetic bound table, R39W2C2Shortcut |
| dep-missing-be | `*` | `missing-extractor-dependency` | `sasquatch-v4be` | `*` | `no` | `0` | the BE extractor was missing -> install sasquatch-v4be | synthetic bound table, R39W2C2Shortcut |
| dep-missing-le | `*` | `missing-extractor-dependency` | `sasquatch` | `*` | `no` | `0` | the LE extractor was missing -> install sasquatch | synthetic bound table, R39W2C2Shortcut |
| in-tree-symlink-metadata | `*` | `unpublished-entry` | `none` | `*` | `no` | `>0` | an in-tree link is gapped -> expected | synthetic bound table, R39W2C2Shortcut |
| body-extractor-failure | `*` | `extractor-failure` | `none` | `*` | `no` | `0` | the extractor failed on the image -> keep the command and stderr | synthetic bound table, R39W2C2Shortcut |
| clean | `*` | `none` | `none` | `*` | `no` | `>0` | no gap and nothing removed -> nothing to fix | synthetic bound table, R39W2C2Shortcut |
