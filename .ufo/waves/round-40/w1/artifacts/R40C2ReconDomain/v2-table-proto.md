# Proposed v2 rule block (recon draft — seat R40C2ReconDomain)

Advisory only: the L1 owns SKILL.md. This is the table my prototype
(`sqfs-triage-v2-proto.py`) parses and the shape I validated the domain guard with.

Layout constraint the prototype enforces (and the draft grammar implies): the
`sqfs-triage-actions` line must sit **directly above the table header**, separated only by
blank lines; the `sqfs-triage-table v2` marker may sit anywhere in the block above it.

```
19. **SquashFS outcome triage, v2.** Domain guard first: every row names the operation and
    provider it was measured on, so an envelope from another REA verb falls through to
    `unclassified` instead of borrowing an unblob diagnosis. `action` is a closed
    vocabulary scored with the label.

    <!-- sqfs-triage-table v2 -->

    <!-- sqfs-triage-actions: check-superblock rerun-with-be reinstall-extractor compare-oracle expect-absent salvage-published none -->
    | label | operation | provider | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | no-squashfs-chunk | `extract_firmware` | `unblob` | `none` | `*` | `*` | `n/a` | `*` | `*` | `check-superblock` | ... | knowledge entry :50-54 |
    | dep-missing-be | `extract_firmware` | `unblob` | `squashfs_v4_be` | `missing-extractor-dependency` | `sasquatch-v4be` | `n/a` | `no` | `*` | `reinstall-extractor` | ... | S112 lines 68-69; S120 command.py:101-102 |
    | dep-missing-le | `extract_firmware` | `unblob` | `squashfs_v4_le` | `missing-extractor-dependency` | `sasquatch` | `n/a` | `no` | `*` | `reinstall-extractor` | ... | S112; S120 command.py:101-102 |
    | avm-marker-be-dropped | `extract_firmware` | `unblob` | `squashfs_v4_be` | `extractor-failure` | `none` | `no` | `no` | `0` | `rerun-with-be` | ... | S112 lines 44-50; S121 |
    | body-extractor-failure | `extract_firmware` | `unblob` | `squashfs_v4_be` | `extractor-failure` | `none` | `yes` | `no` | `0` | `compare-oracle` | ... | S120 report.py:91-98 |
    | partial-body-failure | `extract_firmware` | `unblob` | `squashfs_v4_*` | `extractor-failure` | `none` | `*` | `*` | `>0` | `salvage-published` | ... | R39-CL3 D1 (round-39 verifier spot-check §5) |
    | mixed-symlinks | `extract_firmware` | `unblob` | `squashfs_v4_*` | `unpublished-entry` | `none` | `n/a` | `yes` | `>0` | `expect-absent` | ... | R39-CL2 |
    | escaping-symlink-removed | `extract_firmware` | `unblob` | `squashfs_v4_*` | `*` | `*` | `n/a` | `yes` | `>0` | `expect-absent` | ... | S118 extractor.py:79-91 |
    | in-tree-symlink-metadata | `extract_firmware` | `unblob` | `squashfs_v4_*` | `unpublished-entry` | `none` | `n/a` | `no` | `>0` | `expect-absent` | ... | S119 FirmwarePublication.js:68-75,301-308 |
    | clean-empty | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `none` | `n/a` | `no` | `0` | `none` | ... | R39-CL3 D2 |
    | clean | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `none` | `n/a` | `no` | `>0` | `compare-oracle` | ... | S119; knowledge entry :11-19 |
```

Cause cells are elided above (`...`) so this file stays a shape reference; the SKILL
wording keeps the v1 cause prose (bytes-identical where the row is unchanged) plus a
cause sentence for the four new rows.

## Why every row repeats the domain cells

Measured on development inputs (this seat, artifacts `dev-envelopes/`):

| envelope | operation | provider | H | G | D | BE | SR | P | v1 label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| extract-firmware on random 8 KiB | `extract_firmware` | `unblob` | `[]` | `[]` | `[]` | `n/a` | `no` | 0 | `no-squashfs-chunk` |
| inspect-firmware-regions on a BE carrier | `inspect_firmware_regions` | `binwalk` | `[]` | `[]` | `[]` | `n/a` | `no` | 0 | `no-squashfs-chunk` |
| inspect-firmware-regions on a LE carrier | `inspect_firmware_regions` | `binwalk` | `[]` | `[]` | `[]` | `n/a` | `no` | 0 | `no-squashfs-chunk` |
| inspect-artifact on a zip-wrapped carrier | `inspect_artifact` | `rea-artifact-graph` | `[]` | `[]` | `[]` | `n/a` | `no` | 0 | `no-squashfs-chunk` |

The v1 feature vector is identical in all four rows, so no v1 cell can separate them:
only `operation` + `provider` can, which is exactly the guard columns.
