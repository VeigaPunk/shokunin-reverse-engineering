- **SquashFS `extract-firmware` outcome triage v4 (round 42).** <prose: what v4 adds over v3 — the whole handler
  family `squashfs_v1 squashfs_v2 squashfs_v2_nonstandard squashfs_v3 squashfs_v3_ddwrt squashfs_v3_broadcom
  squashfs_v3_nonstandard squashfs_v4_le squashfs_v4_be squashfs_v4_broadcom`, the legacy-failure row, the one
  declared-tuple key; rows tried top to bottom, more specific above more general; the interpreter parses this block
  out of `SKILL.md` and carries no embedded copy>. Supersedes the v3 table below for every envelope carrying a
  `squashfs_v1`-`squashfs_v3*` chunk (`corpus/knowledge/2026-10-26-r42-sqfs-triage-v4.md:12-30`).

  <!-- sqfs-triage-table v4 -->
  <!-- sqfs-triage-actions: none inspect-input install-extractor-be install-extractor-le wrap-extractor-be preserve-failure salvage-partial raise-depth audit-symlinks expect-link-absent count-gap confirm-empty cross-read-legacy -->
  | label | operation | provider | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | no-squashfs-chunk | `extract_firmware` | `unblob` | `none` | `*` | `*` | `*` | `*` | `*` | `inspect-input` | <cause> | <source> |
  | ... one row per label, 12 `|`-separated cells, no literal `|` inside a cell, handler cell matches `^[A-Za-z0-9_?*.\-\[\]]+$` (so `squashfs_v[123]*` is legal) ... |
