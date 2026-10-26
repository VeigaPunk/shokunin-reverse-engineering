## Queue-drain craft

<!-- sqfs-triage-table v2 -->
<!-- sqfs-triage-actions: none inspect-input install-extractor-be install-extractor-le wrap-extractor-be preserve-failure salvage-partial audit-symlinks expect-link-absent count-gap confirm-empty descend-depth -->
| label | operation | provider | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| partial-body-failure | `extract_firmware` | `unblob` | `squashfs_v4_*` | `+extractor-failure` | `*` | `*` | `*` | `>0` | `salvage-partial` | probe row -> salvage-partial | plans/round-41-claims.md rows 1-12 |
