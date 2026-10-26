# PROBE TABLE ONLY - not SKILL.md block 21

This markdown document exists so `sqfs-triage-v4.py` can be exercised on a v4 table
while the lane's `SKILL.md` still carries only v3 (base `c4a38ea`). The lane table
(block 21) is authored and integrated by the L1; this file is a test input, and the
interpreter carries no copy of it.

Its rows are the round-42 draft precedence **including amendment A1**
(`plans/round-42-claims.md` `## R42-C2`), one row per clause, in clause order. The
grammar is the L1's 13-column decision: `handler` globs over F, `failing handler` globs
over HF, `dependencies` speaks the contains form. `cause` and `source` cells are
placeholders: they are unscored prose.

## Queue-drain craft

Draft text, one row per clause.

<!-- sqfs-triage-table v4 -->
<!-- sqfs-triage-actions: none inspect-input install-extractor-be install-extractor-le wrap-extractor-be preserve-failure salvage-partial raise-depth audit-symlinks expect-link-absent count-gap confirm-empty cross-read-legacy isolate-residue -->
| label | operation | provider | handler | failing handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| container-depth-limited | `extract_firmware` | `unblob` | `none` | `*` | `depth-limited+` | `*` | `*` | `*` | `*` | `raise-depth` | F empty but the depth budget was hit -> rerun deeper | scratch |
| no-squashfs-chunk | `extract_firmware` | `unblob` | `none` | `*` | `*` | `*` | `*` | `*` | `*` | `inspect-input` | F empty -> inspect the input | scratch |
| dep-missing-be | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `missing-extractor-dependency+` | `sasquatch-v4be+` | `*` | `*` | `*` | `install-extractor-be` | D holds sasquatch-v4be -> install the BE binary | scratch |
| dep-missing-le | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `missing-extractor-dependency+` | `sasquatch+` | `*` | `*` | `*` | `install-extractor-le` | D holds sasquatch -> install the LE binary | scratch |
| partial-body-failure | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `extractor-failure+` | `*` | `*` | `*` | `>0` | `salvage-partial` | failure after a published file -> salvage | scratch |
| avm-marker-be-dropped | `extract_firmware` | `unblob` | `squashfs_*` | `squashfs_v4_be` | `extractor-failure+` | `*` | `no` | `*` | `0` | `wrap-extractor-be` | v4-BE failure without -be -> wrap the extractor | scratch |
| legacy-body-failure | `extract_firmware` | `unblob` | `squashfs_*` | `squashfs_v[123]*` | `extractor-failure+` | `*` | `*` | `*` | `0` | `cross-read-legacy` | legacy body failed -> cross-read the chunk | scratch |
| body-extractor-failure | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `extractor-failure+` | `*` | `*` | `*` | `0` | `preserve-failure` | failure with no file -> preserve | scratch |
| unknown-residue | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `unknown-chunk-handler+` | `*` | `*` | `*` | `*` | `isolate-residue` | unclaimed bytes -> isolate the residue | scratch |
| depth-limited | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `depth-limited+` | `*` | `*` | `*` | `*` | `raise-depth` | depth limit -> rerun deeper | scratch |
| mixed-symlinks | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `unpublished-entry+` | `*` | `*` | `yes` | `*` | `audit-symlinks` | both link kinds -> audit | scratch |
| escaping-symlink-removed | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `none` | `*` | `*` | `yes` | `*` | `expect-link-absent` | removed link -> expect it absent | scratch |
| in-tree-symlink-metadata | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `unpublished-entry` | `*` | `*` | `no` | `*` | `count-gap` | in-tree links -> count the gaps | scratch |
| clean | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `none` | `*` | `*` | `no` | `>0` | `none` | no gap, files -> nothing to do | scratch |
| clean-empty | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `none` | `*` | `*` | `no` | `0` | `confirm-empty` | no gap, no file -> confirm empty | scratch |

## A later section
