# R39C2ReconDep — REA extract-firmware feature table (development carriers)

| run | carrier | H | G | D | -be | SR | P | bytes | coverage | chunk failed | ok |
|---|---|---|---|---|---|---|---|---|---|---|---|
| full-be-dirempty-gzip | be-dirempty-gzip | squashfs_v4_be | (none) | (none) | n/a | no | 0 | 0 | complete | [False] | True |
| full-be-esc-gzip | be-esc-gzip | squashfs_v4_be | (none) | (none) | n/a | yes | 3 | 34 | partial | [False] | True |
| full-be-linkonly-gzip | be-linkonly-gzip | squashfs_v4_be | (none) | (none) | n/a | no | 0 | 0 | complete | [False] | True |
| full-be-sym-gzip | be-sym-gzip | squashfs_v4_be | unpublished-entry | (none) | n/a | no | 3 | 38 | partial | [False] | True |
| full-be1-avm-native | be1-avm-native | squashfs_v4_be | extractor-failure | (none) | no | no | 0 | 0 | partial | [True] | True |
| full-be1-avm | be1-avm | squashfs_v4_be | extractor-failure | (none) | no | no | 0 | 0 | partial | [True] | True |
| full-be1-corrupt | be1-corrupt | squashfs_v4_be | extractor-failure | (none) | yes | no | 0 | 0 | partial | [True] | True |
| full-be1-gzip | be1-gzip | squashfs_v4_be | (none) | (none) | n/a | no | 6 | 9055 | complete | [False] | True |
| full-be1-xz | be1-xz | squashfs_v4_be | extractor-failure | (none) | yes | no | 6 | 19 | partial | [True] | True |
| full-be2-gzip | be2-gzip | squashfs_v4_be | (none) | (none) | n/a | no | 3 | 5018 | complete | [False] | True |
| full-le1-corrupt | le1-corrupt | squashfs_v4_le | extractor-failure | (none) | no | no | 0 | 0 | partial | [True] | True |
| full-le1-gzip | le1-gzip | squashfs_v4_le | (none) | (none) | n/a | no | 3 | 6017 | complete | [False] | True |
| full-le1-xz | le1-xz | squashfs_v4_le | extractor-failure | (none) | no | no | 3 | 0 | partial | [True] | True |
| full-le2-gzip | le2-gzip | squashfs_v4_le | (none) | (none) | n/a | no | 3 | 15 | complete | [False] | True |
| full-not-squashfs | not-squashfs | (none) | (none) | (none) | n/a | no | 0 | 0 | complete | [] | True |
| stripped-be-esc-gzip | be-esc-gzip | squashfs_v4_be | missing-extractor-dependency | sasquatch-v4be | n/a | no | 0 | 0 | partial | [True] | True |
| stripped-be-sym-gzip | be-sym-gzip | squashfs_v4_be | missing-extractor-dependency | sasquatch-v4be | n/a | no | 0 | 0 | partial | [True] | True |
| stripped-be1-avm | be1-avm | squashfs_v4_be | missing-extractor-dependency | sasquatch-v4be | n/a | no | 0 | 0 | partial | [True] | True |
| stripped-be1-gzip-repeat | be1-gzip-repeat | squashfs_v4_be | missing-extractor-dependency | sasquatch-v4be | n/a | no | 0 | 0 | partial | [True] | True |
| stripped-be1-gzip | be1-gzip | squashfs_v4_be | missing-extractor-dependency | sasquatch-v4be | n/a | no | 0 | 0 | partial | [True] | True |
| stripped-be2-gzip | be2-gzip | squashfs_v4_be | missing-extractor-dependency | sasquatch-v4be | n/a | no | 0 | 0 | partial | [True] | True |
| stripped-le1-gzip | le1-gzip | squashfs_v4_le | missing-extractor-dependency | sasquatch | n/a | no | 0 | 0 | partial | [True] | True |
| stripped-le2-gzip | le2-gzip | squashfs_v4_le | missing-extractor-dependency | sasquatch | n/a | no | 0 | 0 | partial | [True] | True |
