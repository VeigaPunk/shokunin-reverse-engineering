<!-- sqfs-triage-table v2 -->
<!-- sqfs-triage-actions: none inspect-input install-extractor-be install-extractor-le wrap-extractor-be preserve-failure salvage-partial audit-symlinks expect-link-absent count-gap confirm-empty -->
| label | operation | provider | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| no-squashfs-chunk | extract_firmware | * | none | * | * | * | * | * | inspect-input | no squashfs handler ran on any chunk -> inspect the magic and superblock | w2-min |
| dep-missing-be | * | * | * | * | sasquatch-v4be | * | * | * | install-extractor-be | the BE v4 handler lost sasquatch-v4be from the child PATH -> install it and rerun | w2-min |
| dep-missing-le | * | * | * | * | sasquatch | * | * | * | install-extractor-le | the LE v4 handler lost sasquatch from the child PATH -> install it and rerun | w2-min |
| avm-marker-be-dropped | * | * | * | * | * | no | * | * | wrap-extractor-be | the recorded sasquatch argv has no -be, so the AVM marker handshake dropped it -> wrap the extractor and append -be | w2-min |
| body-extractor-failure | * | * | * | * | * | yes | * | 0 | preserve-failure | the extractor ran with the recorded argv and failed publishing nothing -> keep the failing command | w2-min |
| partial-body-failure | * | * | * | extractor-failure | * | * | * | >0 | salvage-partial | the extractor failed after publishing files -> keep them and mark the run incomplete | w2-min |
| mixed-symlinks | * | * | * | unpublished-entry | * | * | yes | * | audit-symlinks | removed links and unpublished entries in one envelope -> audit both kinds | w2-min |
| in-tree-symlink-metadata | * | * | * | unpublished-entry | * | * | no | * | count-gap | every non-file entry stayed in-tree as one gap each -> count them, install nothing | w2-min |
| escaping-symlink-removed | * | * | * | none | * | * | yes | * | expect-link-absent | a link escaped the root and was removed with no gap recorded -> expect it absent | w2-min |
| clean | * | * | * | none | * | * | no | >0 | none | every regular file published, no gap, no link removed -> nothing to fix | w2-min |
| clean-empty | * | * | squashfs_v4_* | none | * | * | * | 0 | confirm-empty | the extractor completed with no gap and the image tree holds no regular file -> confirm the oracle is empty | w2-min |

## Later

x
