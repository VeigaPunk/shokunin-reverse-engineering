# glob-table-onecol-v4draft.md — the ONE-COLUMN variant (pre-decision natural encoding)

What a v4 author would have written from the A1 text with the round-41 grammar
alone: 12 columns, no `failing handler` column, `dependencies` exact-set only.
The `handler` cell here is globbed over F exactly as in the two-column table —
the divergence from the A1 precedence is that the avm/legacy rows key on
membership in F (the run-wide SquashFS handler set) where the precedence keys on
membership in HF (the failing chunk's handlers). This file exists to enumerate
that divergence class precisely; it is NOT the agreed v4 grammar. Cause cells
carry an arrow because the frozen round-41 interpreter requires one.

<!-- sqfs-triage-table v4 -->
<!-- sqfs-triage-actions: none inspect-input install-extractor-be install-extractor-le salvage-partial wrap-extractor-be cross-read-legacy preserve-failure isolate-residue raise-depth audit-symlinks expect-link-absent count-gap confirm-empty -->
| label | operation | provider | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| container-depth-limited | `extract_firmware` | `unblob` | `none` | `depth-limited+` | `*` | `*` | `*` | `*` | `raise-depth` | A1 step 2 -> onecol probe | onecol |
| no-squashfs-chunk | `extract_firmware` | `unblob` | `none` | `*` | `*` | `*` | `*` | `*` | `inspect-input` | A1 step 3 -> onecol probe | onecol |
| dep-missing-be | `extract_firmware` | `unblob` | `squashfs_*` | `missing-extractor-dependency+` | `sasquatch-v4be` | `*` | `*` | `*` | `install-extractor-be` | A1 step 4 arm A -> onecol probe | onecol |
| dep-missing-le | `extract_firmware` | `unblob` | `squashfs_*` | `missing-extractor-dependency+` | `sasquatch` | `*` | `*` | `*` | `install-extractor-le` | A1 step 4 arm B -> onecol probe | onecol |
| partial-body-failure | `extract_firmware` | `unblob` | `squashfs_*` | `extractor-failure+` | `*` | `*` | `*` | `>0` | `salvage-partial` | A1 step 5 -> onecol probe | onecol |
| avm-marker-be-dropped | `extract_firmware` | `unblob` | `squashfs_v4_be` | `extractor-failure+` | `*` | `no` | `*` | `0` | `wrap-extractor-be` | A1 step 6 -> onecol probe | onecol |
| legacy-body-failure | `extract_firmware` | `unblob` | `squashfs_v[123]*` | `extractor-failure+` | `*` | `*` | `*` | `0` | `cross-read-legacy` | A1 step 7 -> onecol probe | onecol |
| body-extractor-failure | `extract_firmware` | `unblob` | `squashfs_*` | `extractor-failure+` | `*` | `*` | `*` | `0` | `preserve-failure` | A1 step 8 -> onecol probe | onecol |
| unknown-residue | `extract_firmware` | `unblob` | `squashfs_*` | `unknown-chunk-handler+` | `*` | `*` | `*` | `*` | `isolate-residue` | A1 step 9 -> onecol probe | onecol |
| depth-limited | `extract_firmware` | `unblob` | `squashfs_*` | `depth-limited+` | `*` | `*` | `*` | `*` | `raise-depth` | A1 step 10 -> onecol probe | onecol |
| mixed-symlinks | `extract_firmware` | `unblob` | `squashfs_*` | `unpublished-entry+` | `*` | `*` | `yes` | `*` | `audit-symlinks` | A1 step 11 -> onecol probe | onecol |
| escaping-symlink-removed | `extract_firmware` | `unblob` | `squashfs_*` | `none` | `*` | `*` | `yes` | `*` | `expect-link-absent` | A1 step 12 -> onecol probe | onecol |
| in-tree-symlink-metadata | `extract_firmware` | `unblob` | `squashfs_*` | `unpublished-entry` | `*` | `*` | `*` | `*` | `count-gap` | A1 step 13 -> onecol probe | onecol |
| clean | `extract_firmware` | `unblob` | `squashfs_*` | `none` | `*` | `*` | `*` | `>0` | `none` | A1 step 14 arm A -> onecol probe | onecol |
| clean-empty | `extract_firmware` | `unblob` | `squashfs_*` | `none` | `*` | `*` | `*` | `0` | `confirm-empty` | A1 step 14 arm B -> onecol probe | onecol |
