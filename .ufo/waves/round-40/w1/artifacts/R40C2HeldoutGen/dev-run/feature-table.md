| carrier | class | endian/comp | H | G | D | -be | SR | P | operation/provider | pair |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| H01 | clean-be | be/gzip | squashfs_v4_be | none | none | n/a | no | 8 | extract_firmware/unblob | clean / none |
| H02 | clean-be | be/xz | squashfs_v4_be | none | none | n/a | no | 6 | extract_firmware/unblob | clean / none |
| H03 | clean-le | le/gzip | squashfs_v4_le | none | none | n/a | no | 3 | extract_firmware/unblob | clean / none |
| H04 | clean-le | le/xz | squashfs_v4_le | none | none | n/a | no | 3 | extract_firmware/unblob | clean / none |
| H05 | clean-empty | be/gzip | squashfs_v4_be | none | none | n/a | no | 0 | extract_firmware/unblob | clean-empty / confirm-empty |
| H06 | clean-empty | le/xz | squashfs_v4_le | none | none | n/a | no | 0 | extract_firmware/unblob | clean-empty / confirm-empty |
| H07 | escaping-symlink-removed | be/gzip | squashfs_v4_be | none | none | n/a | yes | 5 | extract_firmware/unblob | escaping-symlink-removed / expect-link-absent |
| H08 | escaping-symlink-removed | le/xz | squashfs_v4_le | none | none | n/a | yes | 7 | extract_firmware/unblob | escaping-symlink-removed / expect-link-absent |
| H09 | in-tree-symlink-metadata | be/gzip | squashfs_v4_be | unpublished-entry | none | n/a | no | 7 | extract_firmware/unblob | in-tree-symlink-metadata / count-gap |
| H10 | in-tree-symlink-metadata | le/xz | squashfs_v4_le | unpublished-entry | none | n/a | no | 6 | extract_firmware/unblob | in-tree-symlink-metadata / count-gap |
| H11 | mixed-symlinks | be/gzip | squashfs_v4_be | unpublished-entry | none | n/a | yes | 8 | extract_firmware/unblob | mixed-symlinks / audit-symlinks |
| H12 | mixed-symlinks | le/xz | squashfs_v4_le | unpublished-entry | none | n/a | yes | 6 | extract_firmware/unblob | mixed-symlinks / audit-symlinks |
| H13 | dep-missing-be | be/gzip | squashfs_v4_be | missing-extractor-dependency | sasquatch-v4be | n/a | no | 0 | extract_firmware/unblob | dep-missing-be / install-extractor-be |
| H14 | dep-missing-be | be/xz | squashfs_v4_be | missing-extractor-dependency | sasquatch-v4be | n/a | no | 0 | extract_firmware/unblob | dep-missing-be / install-extractor-be |
| H15 | dep-missing-le | le/gzip | squashfs_v4_le | missing-extractor-dependency | sasquatch | n/a | no | 0 | extract_firmware/unblob | dep-missing-le / install-extractor-le |
| H16 | dep-missing-le | le/xz | squashfs_v4_le | missing-extractor-dependency | sasquatch | n/a | no | 0 | extract_firmware/unblob | dep-missing-le / install-extractor-le |
| H17 | avm-marker-be-dropped | avm/gzip | squashfs_v4_be | extractor-failure | none | no | no | 0 | extract_firmware/unblob | avm-marker-be-dropped / wrap-extractor-be |
| H18 | avm-marker-be-dropped | avm/xz | squashfs_v4_be | extractor-failure | none | no | no | 0 | extract_firmware/unblob | avm-marker-be-dropped / wrap-extractor-be |
| H19 | body-extractor-failure | be/gzip | squashfs_v4_be | extractor-failure | none | yes | no | 0 | extract_firmware/unblob | body-extractor-failure / preserve-failure |
| H20 | body-extractor-failure | be/xz | squashfs_v4_be | extractor-failure | none | yes | no | 0 | extract_firmware/unblob | body-extractor-failure / preserve-failure |
| H21 | partial-body-failure | be/gzip | squashfs_v4_be | extractor-failure | none | yes | no | 8 | extract_firmware/unblob | partial-body-failure / salvage-partial |
| H22 | partial-body-failure | be/xz | squashfs_v4_be | extractor-failure | none | yes | no | 4 | extract_firmware/unblob | partial-body-failure / salvage-partial |
| H23 | no-squashfs-chunk | be/gzip | none | none | none | n/a | no | 0 | extract_firmware/unblob | no-squashfs-chunk / inspect-input |
| H24 | no-squashfs-chunk | le/xz | none | none | none | n/a | no | 0 | extract_firmware/unblob | no-squashfs-chunk / inspect-input |
| H25 | out-of-domain | be/gzip | none | none | none | n/a | no | 0 | inspect_firmware_regions/binwalk | unclassified / none |
| H26 | out-of-domain | le/xz | none | none | none | n/a | no | 0 | inspect_firmware_regions/binwalk | unclassified / none |
