# Proposed triage table v2 shape (R40MistakeHunt green fixture)

Not a claim of the round; the table the row checks accept, used to show each check can pass.
Rows are ordered first-match-wins. Every row pins the domain (operation/provider) so an
envelope outside `extract_firmware` + `unblob` matches nothing and falls to `unclassified`.

## Queue-drain craft

<!-- sqfs-triage-table v2 -->

| label | operation | provider | handler | gap kinds | dependencies | block-length endianness | -be in child argv | symlink removed | published files | cause -> action | source |
|---|---|---|---|---|---|---|---|---|---|---|---|
| no-squashfs-chunk | extract_firmware | unblob | none | * | * | * | n/a | * | * | no chunk carries a squashfs handler -> check magic and superblock before rerunning; an empty envelope is not an empty filesystem | v1 row 1 |
| dep-missing-be | extract_firmware | unblob | squashfs_v4_be | missing-extractor-dependency | sasquatch-v4be | * | n/a | no | * | the BE handler needed sasquatch-v4be on the child PATH -> install it and rerun into a fresh outdir | v1 row 2 |
| dep-missing-le | extract_firmware | unblob | squashfs_v4_le | missing-extractor-dependency | sasquatch | * | n/a | no | * | the LE handler needed sasquatch on the child PATH -> install it and rerun | v1 row 3 |
| avm-marker-be-dropped | extract_firmware | unblob | squashfs_v4_be | extractor-failure | none | BE | no | no | 0 | the block-length header decodes big-endian and mkfs_time equals bytes_used, so unblob omitted -be and the body is standard BE -> if and only if the block-length test says BE, a PATH wrapper named sasquatch-v4be appending -be is correct for this class; remove it before any AVM-layout carrier | v1 row 4, narrowed |
| avm-layout-body-flag-passed | extract_firmware | unblob | squashfs_v4_be | extractor-failure | none | LE | yes | no | 0 | the block-length header decodes little-endian, so the body is the genuine AVM layout while the recorded argv carries -be because the timestamp was normalised -> rerun with sasquatch-v4be without -be; the body is intact, never list it as damage | this seat's sasquatch-v4be matrix |
| body-extractor-failure | extract_firmware | unblob | squashfs_v4_be | extractor-failure | none | BE | yes | no | 0 | block-length endianness reads big-endian, -be was passed and the extractor still failed -> the body is damaged; keep stderr, compare with a known-good carrier | v1 row 5, narrowed |
| mixed-symlinks | extract_firmware | unblob | squashfs_v4_* | unpublished-entry | none | * | n/a | yes | >0 | both link kinds present: escaping links removed, in-tree links kept and reported -> count one unpublished-entry gap per kept link and none for the removed ones | R39-CL2 |
| escaping-symlink-removed | extract_firmware | unblob | squashfs_v4_* | * | * | * | n/a | yes | >0 | a link target resolved outside the extraction root and was removed -> expect the path absent; never materialise it | v1 row 6 |
| in-tree-symlink-metadata | extract_firmware | unblob | squashfs_v4_* | unpublished-entry | none | * | n/a | no | >0 | every link target resolved inside the extraction root -> metadata, one gap per link; publish nothing for it | v1 row 7 |
| avm-layout-clean | extract_firmware | unblob | squashfs_v4_be | none | none | LE | n/a | no | >0 | block-length header decodes little-endian and every file was published -> record the AVM layout verdict with the receipt; do not report it as a plain standard-BE clean | this seat's matrix |
| clean | extract_firmware | unblob | squashfs_v4_* | none | none | * | n/a | no | >0 | every regular file was published and no gap was recorded -> match files to an oracle by suffix and sha256 | v1 row 8 |
