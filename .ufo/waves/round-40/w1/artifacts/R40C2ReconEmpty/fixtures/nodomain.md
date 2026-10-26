<!-- REcon probe input: a CANDIDATE v2 table, not the frozen SKILL.md block. -->
# SKILL (recon probe copy)

## Queue-drain craft

Prose before the table.

<!-- sqfs-triage-actions: inspect-header install-dependency rerun-with-be-wrapper keep-evidence count-gap-and-absence expect-link-absent count-gap accept-empty accept-oracle -->
<!-- sqfs-triage-table v2 -->
| label | operation | provider | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| no-squashfs-chunk | `*` | `*` | `none` | `*` | `*` | `n/a` | `*` | `*` | `inspect-header` | no chunk carries a squashfs handler | knowledge entry :50-54 |
| dep-missing-be | `*` | `*` | `squashfs_v4_be` | `missing-extractor-dependency` | `sasquatch-v4be` | `n/a` | `no` | `*` | `install-dependency` | the BE handler needed sasquatch-v4be and it was absent | S112 lines 68-69 |
| dep-missing-le | `*` | `*` | `squashfs_v4_le` | `missing-extractor-dependency` | `sasquatch` | `n/a` | `no` | `*` | `install-dependency` | the LE handler needed sasquatch and it was absent | S112 lines 68-69 |
| avm-marker-be-dropped | `*` | `*` | `squashfs_v4_be` | `extractor-failure` | `none` | `no` | `no` | `0` | `rerun-with-be-wrapper` | the AVM marker dropped -be on a standard-BE body | S112 lines 44-50 |
| body-extractor-failure | `*` | `*` | `squashfs_v4_*` | `extractor-failure` | `none` | `yes` | `no` | `*` | `keep-evidence` | the extractor ran with -be and still failed | S120 report.py:91-98 |
| mixed-symlinks | `*` | `*` | `squashfs_v4_*` | `unpublished-entry` | `none` | `n/a` | `yes` | `*` | `count-gap-and-absence` | both an escaping link (removed) and in-tree links (one gap each) | S118 79-91; S119 69-75 |
| escaping-symlink-removed | `*` | `*` | `squashfs_v4_*` | `none` | `none` | `n/a` | `yes` | `*` | `expect-link-absent` | a link escaped the root and was removed with a report and no gap | S118 extractor.py:79-91 |
| in-tree-symlink-metadata | `*` | `*` | `squashfs_v4_*` | `unpublished-entry` | `none` | `n/a` | `no` | `*` | `count-gap` | in-tree links are kept as metadata, one gap each | S119 FirmwarePublication.js:68-75 |
| clean-empty | `*` | `*` | `squashfs_v4_*` | `none` | `none` | `n/a` | `no` | `0` | `accept-empty` | the filesystem is readable and holds no regular files | recon R40C2ReconEmpty |
| clean | `*` | `*` | `squashfs_v4_*` | `none` | `none` | `n/a` | `no` | `>0` | `accept-oracle` | every regular file was published | S119; knowledge entry :11-19 |

## A later section

Prose after the craft section.
