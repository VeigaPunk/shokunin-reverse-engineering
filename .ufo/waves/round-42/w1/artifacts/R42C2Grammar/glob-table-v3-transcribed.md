# glob-table-v3-transcribed.md — CTL-C2-0b: the round-41 v3 table (SKILL.md rule block 20, lines 434-449) transcribed under a v4 marker

Decision cells are the frozen v3 cells, byte-faithful; cause/source cells are
abbreviated pointers (the emulator does not read them). Used only to emulate
CTL-C2-0b (do-nothing on the surface) over the grammar vectors.

<!-- sqfs-triage-table v4 -->
<!-- sqfs-triage-actions: none inspect-input install-extractor-be install-extractor-le salvage-partial wrap-extractor-be preserve-failure raise-depth audit-symlinks expect-link-absent count-gap confirm-empty -->
| label | operation | provider | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| no-squashfs-chunk | `extract_firmware` | `unblob` | `none` | `*` | `*` | `*` | `*` | `*` | `inspect-input` | SKILL.md:438 | v3 |
| dep-missing-be | `extract_firmware` | `unblob` | `squashfs_v4_*` | `missing-extractor-dependency+` | `sasquatch-v4be` | `*` | `*` | `*` | `install-extractor-be` | SKILL.md:439 | v3 |
| dep-missing-le | `extract_firmware` | `unblob` | `squashfs_v4_*` | `missing-extractor-dependency+` | `sasquatch` | `*` | `*` | `*` | `install-extractor-le` | SKILL.md:440 | v3 |
| partial-body-failure | `extract_firmware` | `unblob` | `squashfs_v4_*` | `extractor-failure+` | `*` | `*` | `*` | `>0` | `salvage-partial` | SKILL.md:441 | v3 |
| avm-marker-be-dropped | `extract_firmware` | `unblob` | `squashfs_v4_be` | `extractor-failure+` | `*` | `no` | `*` | `0` | `wrap-extractor-be` | SKILL.md:442 | v3 |
| body-extractor-failure | `extract_firmware` | `unblob` | `squashfs_v4_*` | `extractor-failure+` | `*` | `*` | `*` | `0` | `preserve-failure` | SKILL.md:443 | v3 |
| depth-limited | `extract_firmware` | `unblob` | `squashfs_v4_*` | `depth-limited+` | `*` | `*` | `*` | `*` | `raise-depth` | SKILL.md:444 | v3 |
| mixed-symlinks | `extract_firmware` | `unblob` | `squashfs_v4_*` | `unpublished-entry+` | `*` | `*` | `yes` | `*` | `audit-symlinks` | SKILL.md:445 | v3 |
| escaping-symlink-removed | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `*` | `*` | `yes` | `*` | `expect-link-absent` | SKILL.md:446 | v3 |
| in-tree-symlink-metadata | `extract_firmware` | `unblob` | `squashfs_v4_*` | `unpublished-entry` | `*` | `*` | `no` | `*` | `count-gap` | SKILL.md:447 | v3 |
| clean | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `*` | `*` | `no` | `>0` | `none` | SKILL.md:448 | v3 |
| clean-empty | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `*` | `*` | `no` | `0` | `confirm-empty` | SKILL.md:449 | v3 |
