# CTL-C2-7-lookup (one row per named-class label, declared tuples)

Control data for R41-C2; not instructions.

## Queue-drain craft

<!-- sqfs-triage-table v3 -->
<!-- sqfs-triage-actions: none inspect-input install-extractor-be install-extractor-le wrap-extractor-be preserve-failure salvage-partial raise-depth audit-symlinks expect-link-absent count-gap confirm-empty -->
| label | operation | provider | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `none` | `n/a` | `no` | `>0` | `none` | a declared class tuple -> its class pair | control only |
| clean-empty | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `none` | `n/a` | `no` | `0` | `confirm-empty` | a declared class tuple -> its class pair | control only |
| escaping-symlink-removed | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `none` | `n/a` | `yes` | `>0` | `expect-link-absent` | a declared class tuple -> its class pair | control only |
| in-tree-symlink-metadata | `extract_firmware` | `unblob` | `squashfs_v4_*` | `unpublished-entry` | `none` | `n/a` | `no` | `>0` | `count-gap` | a declared class tuple -> its class pair | control only |
| mixed-symlinks | `extract_firmware` | `unblob` | `squashfs_v4_*` | `unpublished-entry` | `none` | `n/a` | `yes` | `>0` | `audit-symlinks` | a declared class tuple -> its class pair | control only |
| dep-missing-be | `extract_firmware` | `unblob` | `squashfs_v4_be` | `missing-extractor-dependency` | `sasquatch-v4be` | `n/a` | `no` | `0` | `install-extractor-be` | a declared class tuple -> its class pair | control only |
| dep-missing-le | `extract_firmware` | `unblob` | `squashfs_v4_le` | `missing-extractor-dependency` | `sasquatch` | `n/a` | `no` | `0` | `install-extractor-le` | a declared class tuple -> its class pair | control only |
| avm-marker-be-dropped | `extract_firmware` | `unblob` | `squashfs_v4_be` | `extractor-failure` | `none` | `no` | `no` | `0` | `wrap-extractor-be` | a declared class tuple -> its class pair | control only |
| body-extractor-failure | `extract_firmware` | `unblob` | `squashfs_v4_*` | `extractor-failure` | `none` | `*` | `no` | `0` | `preserve-failure` | a declared class tuple -> its class pair | control only |
| partial-body-failure | `extract_firmware` | `unblob` | `squashfs_v4_*` | `*` | `none` | `*` | `*` | `>0` | `salvage-partial` | a declared class tuple -> its class pair | control only |
| no-squashfs-chunk | `extract_firmware` | `unblob` | `none` | `none` | `none` | `n/a` | `no` | `0` | `inspect-input` | a declared class tuple -> its class pair | control only |
| depth-limited | `extract_firmware` | `unblob` | `squashfs_v4_*` | `*` | `none` | `n/a` | `*` | `>0` | `raise-depth` | a declared class tuple -> its class pair | control only |

## End
