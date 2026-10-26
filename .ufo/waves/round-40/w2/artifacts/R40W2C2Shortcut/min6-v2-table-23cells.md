<!-- sqfs-triage-table v2 -->
<!-- sqfs-triage-actions: none inspect-input install-extractor-be install-extractor-le wrap-extractor-be preserve-failure salvage-partial audit-symlinks expect-link-absent count-gap confirm-empty -->
| label | operation | provider | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| no-squashfs-chunk | * | unblob | none | * | * | * | * | * | inspect-input | no squashfs chunk -> inspect input | w2-min |
| dep-missing-be | * | * | squashfs_v4_be | missing-extractor-dependency | * | * | * | * | install-extractor-be | BE v4 handler without its extractor binary -> install sasquatch-v4be | w2-min |
| dep-missing-le | * | * | squashfs_v4_le | missing-extractor-dependency | * | * | * | * | install-extractor-le | LE v4 handler without its extractor binary -> install sasquatch | w2-min |
| avm-marker-be-dropped | * | * | * | * | * | no | * | * | wrap-extractor-be | argv without -be -> wrap and rerun | w2-min |
| body-extractor-failure | * | * | * | * | * | yes | * | 0 | preserve-failure | ran and failed, nothing published -> preserve | w2-min |
| partial-body-failure | * | * | * | extractor-failure | * | * | * | >0 | salvage-partial | failed after publishing -> salvage | w2-min |
| mixed-symlinks | * | * | * | unpublished-entry | * | * | yes | * | audit-symlinks | both link outcomes -> audit | w2-min |
| in-tree-symlink-metadata | * | * | * | unpublished-entry | * | * | no | * | count-gap | in-tree entries only -> count gaps | w2-min |
| escaping-symlink-removed | * | * | * | none | * | * | yes | * | expect-link-absent | link removed, no gap -> expect absent | w2-min |
| clean | * | * | * | none | * | * | no | >0 | none | no gap, files published -> clean | w2-min |
| clean-empty | * | * | squashfs_v4_* | none | * | * | * | 0 | confirm-empty | no gap, no files -> confirm empty | w2-min |

## Later

x
