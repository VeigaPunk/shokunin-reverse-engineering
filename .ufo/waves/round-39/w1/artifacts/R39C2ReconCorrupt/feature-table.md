# R39-C2 corruption recon — REA feature table

| run | carrier sha256[:12] | H | G | D | BE | SR | P | extraction_failed | sasquatch exit | stderr first line |
|---|---|---|---|---|---|---|---|---|---|---|
| ta-clean | a4c5c05ef000 | squashfs_v4_be | - | - | n/a | no | 3 | [False] | 0 | Reading a different endian SQUASHFS filesystem on img/ta-be-gzip.sqsh |
| tb-clean | f58669513661 | squashfs_v4_be | - | - | n/a | no | 3 | [False] | 0 | Reading a different endian SQUASHFS filesystem on img/tb-be-gzip.sqsh |
| tc-clean | 4f0c6ddafb30 | squashfs_v4_be | - | - | n/a | no | 3 | [False] | 0 | Reading a different endian SQUASHFS filesystem on img/tc-be-gzip.sqsh |
| td-clean | af2083e5229e | squashfs_v4_be | unpublished-entry | - | n/a | yes | 1 | [False] | not run | - |
| te-clean | ae2df2044182 | squashfs_v4_be | unpublished-entry | - | n/a | no | 1 | [False] | not run | - |
| tf-clean | 8e37a8268f34 | squashfs_v4_be | - | - | n/a | yes | 1 | [False] | not run | - |
| ta-v1 | 895b83d27b02 | squashfs_v4_be | extractor-failure | - | yes | no | 0 | [True] | 1 | Reading a different endian SQUASHFS filesystem on img/ta-v1-zero-id-table.sqsh |
| tb-v1 | 6fb56e2dbf62 | squashfs_v4_be | extractor-failure | - | yes | no | 0 | [True] | 1 | Reading a different endian SQUASHFS filesystem on img/tb-v1-zero-id-table.sqsh |
| tc-v1 | 45f7ac03a219 | squashfs_v4_be | extractor-failure | - | yes | no | 0 | [True] | 1 | Reading a different endian SQUASHFS filesystem on img/tc-v1-zero-id-table.sqsh |
| td-v1 | 02f6155a45d7 | squashfs_v4_be | extractor-failure | - | yes | no | 0 | [True] | 1 | Reading a different endian SQUASHFS filesystem on img/td-be-gzip-v1.sqsh |
| ta-xz-v1 | a8a5e2cd000c | squashfs_v4_be | extractor-failure | - | yes | no | 0 | [True] | 1 | Reading a different endian SQUASHFS filesystem on img/ta-be-xz-v1.sqsh |
| ta-v2 | 7d5949f94f89 | squashfs_v4_be | - | - | n/a | no | 3 | [False] | 0 | Reading a different endian SQUASHFS filesystem on img/ta-v2-zero-first-data-block.sqsh |
| tb-v2 | 55621106ef89 | squashfs_v4_be | extractor-failure | - | yes | no | 3 | [True] | 1 | Reading a different endian SQUASHFS filesystem on img/tb-v2-zero-first-data-block.sqsh |
| tc-v2 | ddc0b078fd0e | squashfs_v4_be | extractor-failure | - | yes | no | 3 | [True] | 1 | Reading a different endian SQUASHFS filesystem on img/tc-v2-zero-first-data-block.sqsh |
| ta-v3 | 1f9d7ca9aead | squashfs_v4_be | extractor-failure | - | yes | no | 0 | [True] | 1 | Reading a different endian SQUASHFS filesystem on img/ta-v3-flip-inode-table.sqsh |
| tb-v3 | a5945ac995ce | squashfs_v4_be | extractor-failure | - | yes | no | 0 | [True] | 1 | Reading a different endian SQUASHFS filesystem on img/tb-v3-flip-inode-table.sqsh |
| tc-v3 | 6081eb012c0b | squashfs_v4_be | extractor-failure | - | yes | no | 0 | [True] | 1 | Reading a different endian SQUASHFS filesystem on img/tc-v3-flip-inode-table.sqsh |
| ta-v4 | de70b748f163 | squashfs_v4_be | extractor-failure | - | yes | no | 0 | [True] | 1 | Reading a different endian SQUASHFS filesystem on img/ta-v4-zero-directory-table.sqsh |
| tb-v4 | ef80d7d33d4e | squashfs_v4_be | extractor-failure | - | yes | no | 0 | [True] | 1 | Reading a different endian SQUASHFS filesystem on img/tb-v4-zero-directory-table.sqsh |
| tc-v4 | 8aaf5922e2a6 | squashfs_v4_be | extractor-failure | - | yes | no | 0 | [True] | 1 | Reading a different endian SQUASHFS filesystem on img/tc-v4-zero-directory-table.sqsh |
| ta-v5 | d13f477d629f | squashfs_v4_be | extractor-failure | - | yes | no | 3 | [True] | 139 | Reading a different endian SQUASHFS filesystem on img/ta-v5-corrupt-block-length.sqsh |
| tb-v5 | 6fbd2798e1de | squashfs_v4_be | extractor-failure | - | yes | no | 3 | [True] | 139 | Reading a different endian SQUASHFS filesystem on img/tb-v5-corrupt-block-length.sqsh |
| tc-v5 | 3044f8c0cd3f | squashfs_v4_be | extractor-failure | - | yes | no | 3 | [True] | 139 | Reading a different endian SQUASHFS filesystem on img/tc-v5-corrupt-block-length.sqsh |
| ta-clean-nodep | a4c5c05ef000 | squashfs_v4_be | missing-extractor-dependency | sasquatch-v4be | n/a | no | 0 | [True] | not run | - |
| ta-v1-rerun | 895b83d27b02 | squashfs_v4_be | extractor-failure | - | yes | no | 0 | [True] | 1 | Reading a different endian SQUASHFS filesystem on img/ta-v1-zero-id-table.sqsh |
