# CTL-C2-7b (CTL-C2-7 plus one majority-label `*` fallback row; A1 control)

Control data for R42-C2; not instructions.

## Queue-drain craft

<!-- sqfs-triage-table v4 -->
<!-- sqfs-triage-actions: none inspect-input install-extractor-be install-extractor-le wrap-extractor-be preserve-failure salvage-partial raise-depth audit-symlinks expect-link-absent count-gap confirm-empty cross-read-legacy isolate-residue -->
| label | operation | provider | handler | failing handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `clean` | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `none` | `none` | `n/a` | `no` | `>0` | `none` | a declared class tuple -> none | control only; observed DEV tuple |
| `clean-empty` | `extract_firmware` | `unblob` | `squashfs_v4_*` | `*` | `none` | `none` | `n/a` | `no` | `0` | `confirm-empty` | a declared class tuple -> confirm-empty | control only; observed DEV tuple |
| `escaping-symlink-removed` | `extract_firmware` | `unblob` | `squashfs_v4_*` | `*` | `none` | `none` | `n/a` | `yes` | `>0` | `expect-link-absent` | a declared class tuple -> expect-link-absent | control only; observed DEV tuple |
| `in-tree-symlink-metadata` | `extract_firmware` | `unblob` | `squashfs_v4_*` | `*` | `unpublished-entry` | `none` | `n/a` | `no` | `>0` | `count-gap` | a declared class tuple -> count-gap | control only; observed DEV tuple |
| `mixed-symlinks` | `extract_firmware` | `unblob` | `squashfs_v4_*` | `*` | `unpublished-entry` | `none` | `n/a` | `yes` | `>0` | `audit-symlinks` | a declared class tuple -> audit-symlinks | control only; observed DEV tuple |
| `avm-marker-be-dropped` | `extract_firmware` | `unblob` | `squashfs_v4_be` | `*` | `extractor-failure` | `none` | `no` | `no` | `0` | `wrap-extractor-be` | a declared class tuple -> wrap-extractor-be | control only; observed DEV tuple |
| `no-squashfs-chunk` | `extract_firmware` | `unblob` | `none` | `*` | `none` | `none` | `n/a` | `no` | `0` | `inspect-input` | a declared class tuple -> inspect-input | control only; observed DEV tuple |
| `unclassified` | `extract_firmware` | `unblob` | `none` | `*` | `none` | `none` | `n/a` | `no` | `0` | `none` | a declared class tuple -> none | control only; observed DEV tuple |
| `body-extractor-failure` | `extract_firmware` | `unblob` | `squashfs_v4_*` | `*` | `extractor-failure` | `none` | `*` | `no` | `0` | `preserve-failure` | a declared class tuple -> preserve-failure | control only; observed DEV tuple |
| `legacy-body-failure` | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `extractor-failure` | `none` | `*` | `no` | `0` | `cross-read-legacy` | a declared class tuple -> cross-read-legacy | control only; observed DEV tuple |
| `container-depth-limited` | `extract_firmware` | `unblob` | `none` | `*` | `*` | `none` | `n/a` | `no` | `>0` | `raise-depth` | a declared class tuple -> raise-depth | control only; observed DEV tuple |
| `dep-missing-be` | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `missing-extractor-dependency` | `*` | `n/a` | `no` | `*` | `install-extractor-be` | a declared class tuple -> install-extractor-be | control only; observed DEV tuple |
| `dep-missing-le` | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `*` | `sasquatch` | `n/a` | `no` | `*` | `install-extractor-le` | a declared class tuple -> install-extractor-le | control only; observed DEV tuple |
| `depth-limited` | `extract_firmware` | `unblob` | `squashfs_v4_*` | `*` | `*` | `none` | `n/a` | `*` | `>0` | `raise-depth` | a declared class tuple -> raise-depth | control only; observed DEV tuple |
| `unknown-residue` | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `*` | `none` | `n/a` | `*` | `>0` | `isolate-residue` | a declared class tuple -> isolate-residue | control only; observed DEV tuple |
| `partial-body-failure` | `extract_firmware` | `unblob` | `*` | `*` | `*` | `*` | `*` | `*` | `*` | `salvage-partial` | unseen tuple -> the dev arm majority label (partial-body-failure) | control only; majority fallback |

## End
