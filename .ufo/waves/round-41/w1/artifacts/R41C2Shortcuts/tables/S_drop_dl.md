## Queue-drain craft

<!-- sqfs-triage-table v2 -->
<!-- sqfs-triage-actions: none inspect-input install-extractor-be install-extractor-le wrap-extractor-be preserve-failure salvage-partial audit-symlinks expect-link-absent count-gap confirm-empty descend-depth -->
| label | operation | provider | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| no-squashfs-chunk | `extract_firmware` | `unblob` | `none` | `*` | `*` | `*` | `*` | `*` | `inspect-input` | probe row -> inspect-input | plans/round-41-claims.md rows 1-12 |
| dep-missing-be | `extract_firmware` | `unblob` | `squashfs_v4_be` | `missing-extractor-dependency` | `sasquatch-v4be` | `*` | `*` | `*` | `install-extractor-be` | probe row -> install-extractor-be | plans/round-41-claims.md rows 1-12 |
| dep-missing-le | `extract_firmware` | `unblob` | `squashfs_v4_le` | `missing-extractor-dependency` | `sasquatch` | `*` | `*` | `*` | `install-extractor-le` | probe row -> install-extractor-le | plans/round-41-claims.md rows 1-12 |
| avm-marker-be-dropped | `extract_firmware` | `unblob` | `squashfs_v4_be` | `extractor-failure` | `*` | `no` | `*` | `0` | `wrap-extractor-be` | probe row -> wrap-extractor-be | plans/round-41-claims.md rows 1-12 |
| body-extractor-failure | `extract_firmware` | `unblob` | `squashfs_v4_*` | `extractor-failure` | `*` | `*` | `*` | `0` | `preserve-failure` | probe row -> preserve-failure | plans/round-41-claims.md rows 1-12 |
| mixed-symlinks | `extract_firmware` | `unblob` | `squashfs_v4_*` | `unpublished-entry` | `*` | `*` | `yes` | `*` | `audit-symlinks` | probe row -> audit-symlinks | plans/round-41-claims.md rows 1-12 |
| escaping-symlink-removed | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `*` | `*` | `yes` | `*` | `expect-link-absent` | probe row -> expect-link-absent | plans/round-41-claims.md rows 1-12 |
| in-tree-symlink-metadata | `extract_firmware` | `unblob` | `squashfs_v4_*` | `unpublished-entry` | `*` | `*` | `no` | `*` | `count-gap` | probe row -> count-gap | plans/round-41-claims.md rows 1-12 |
| clean | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `*` | `*` | `no` | `>0` | `none` | probe row -> none | plans/round-41-claims.md rows 1-12 |
| clean-empty | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `*` | `*` | `no` | `0` | `confirm-empty` | probe row -> confirm-empty | plans/round-41-claims.md rows 1-12 |
| partial-body-failure | `extract_firmware` | `unblob` | `squashfs_v4_*` | `*` | `*` | `*` | `*` | `>0` | `salvage-partial` | probe row -> salvage-partial | plans/round-41-claims.md rows 1-12 |
