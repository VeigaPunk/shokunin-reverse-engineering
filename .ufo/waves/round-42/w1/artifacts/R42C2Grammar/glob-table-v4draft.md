# glob-table-v4draft.md — the A1 v4 table in executable form (grammar seat's reference transcription)

This is the natural first-match encoding of the A1 15-step precedence
(`plans/round-42-claims.md` `## R42-C2`) under the L1 grammar decision of
2026-10-26: 13 columns, a `failing handler` glob matched against HF
(`*` matches anything including an empty HF), the `handler` cell globbed over F
(`none` = F empty), and a contains form `name+` in `dependencies`. Row order =
step order; steps 1 and 15 are realized by the per-row OP/PR pinning plus the
no-match fallback `(unclassified, none)`. Cause/source cells are pointers, not
prose — the knowledge entry owns them.

<!-- sqfs-triage-table v4 -->
<!-- sqfs-triage-actions: none inspect-input install-extractor-be install-extractor-le salvage-partial wrap-extractor-be cross-read-legacy preserve-failure isolate-residue raise-depth audit-symlinks expect-link-absent count-gap confirm-empty -->
| label | operation | provider | handler | failing handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| container-depth-limited | `extract_firmware` | `unblob` | `none` | `*` | `depth-limited+` | `*` | `*` | `*` | `*` | `raise-depth` | F empty + depth gap: a SquashFS chunk may sit inside a container below the depth budget; no SquashFS handler at this depth is not evidence of no SquashFS image -> rerun with a higher `max_depth` | A1 step 2 |
| no-squashfs-chunk | `extract_firmware` | `unblob` | `none` | `*` | `*` | `*` | `*` | `*` | `*` | `inspect-input` | no `squashfs_` handler at all and no depth gap -> check the magic and superblock before rerunning | A1 step 3 |
| dep-missing-be | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `missing-extractor-dependency+` | `sasquatch-v4be+` | `*` | `*` | `*` | `install-extractor-be` | D holds `sasquatch-v4be` (membership; tested first) -> install sasquatch-v4be | A1 step 4 arm A |
| dep-missing-le | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `missing-extractor-dependency+` | `sasquatch+` | `*` | `*` | `*` | `install-extractor-le` | D holds `sasquatch` (membership; every v1-v3 chunk and every v4 LE chunk resolves plain `sasquatch`) -> install sasquatch | A1 step 4 arm B |
| partial-body-failure | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `extractor-failure+` | `*` | `*` | `*` | `>0` | `salvage-partial` | extractor failed after publishing at least one regular file | A1 step 5 |
| avm-marker-be-dropped | `extract_firmware` | `unblob` | `squashfs_*` | `squashfs_v4_be` | `extractor-failure+` | `*` | `no` | `*` | `0` | `wrap-extractor-be` | failing handler is `squashfs_v4_be` (membership in HF), BE argv recorded without `-be` | A1 step 6 |
| legacy-body-failure | `extract_firmware` | `unblob` | `squashfs_*` | `squashfs_v[123]*` | `extractor-failure+` | `*` | `*` | `*` | `0` | `cross-read-legacy` | failing handler is a v1-v3 handler (HF intersect L); no byte-order handshake or AVM pre-check applies -> cross-read with a non-sasquatch reader | A1 step 7 |
| body-extractor-failure | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `extractor-failure+` | `*` | `*` | `*` | `0` | `preserve-failure` | residual zero-file extractor failure (failing handler neither v4_be nor legacy) | A1 step 8 |
| unknown-residue | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `unknown-chunk-handler+` | `*` | `*` | `*` | `*` | `isolate-residue` | unclaimed bytes beside the SquashFS chunk; re-carve to unblob's chunk end, never match the residue file against a filesystem oracle | A1 step 9 |
| depth-limited | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `depth-limited+` | `*` | `*` | `*` | `*` | `raise-depth` | REA stopped at `max_depth` | A1 step 10 |
| mixed-symlinks | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `unpublished-entry+` | `*` | `*` | `yes` | `*` | `audit-symlinks` | both link kinds present | A1 step 11 |
| escaping-symlink-removed | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `none` | `*` | `*` | `yes` | `*` | `expect-link-absent` | removal report, empty gap set | A1 step 12 |
| in-tree-symlink-metadata | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `unpublished-entry` | `*` | `*` | `*` | `*` | `count-gap` | gap set exactly one kind | A1 step 13 |
| clean | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `none` | `*` | `*` | `*` | `>0` | `none` | every regular file published, no gaps | A1 step 14 arm A |
| clean-empty | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `none` | `*` | `*` | `*` | `0` | `confirm-empty` | extractor completed, no gaps, zero files | A1 step 14 arm B |
