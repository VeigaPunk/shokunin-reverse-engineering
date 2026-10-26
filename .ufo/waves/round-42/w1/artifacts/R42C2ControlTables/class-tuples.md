# R42-C2 DEV envelope tuples (A1 features)

`H` = squashfs handler names; `HF` = handlers of the extractor-failure gaps
(falls back to F); `G` gap kinds; `D` dependency names; `BE`; `SR`; `P`
published regular files. `step` is the A1 precedence step that decides the pair.

| id | class | H | HF | G | D | BE | SR | P | label | action | step |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C01 | combo | squashfs_v4_be | squashfs_v4_be | extractor-failure | - | yes | yes | 6 | partial-body-failure | salvage-partial | 5 |
| C02 | combo | squashfs_v4_le | squashfs_v4_le | - | - | n/a | yes | 3 | escaping-symlink-removed | expect-link-absent | 12 |
| C03 | combo | squashfs_v4_be | squashfs_v4_be | extractor-failure | - | yes | yes | 4 | partial-body-failure | salvage-partial | 5 |
| C04 | combo | squashfs_v4_le | squashfs_v4_le | depth-limited extractor-failure unpublished-entry | - | no | yes | 5 | partial-body-failure | salvage-partial | 5 |
| C05 | combo | squashfs_v4_le | squashfs_v4_le | depth-limited extractor-failure | - | no | yes | 7 | partial-body-failure | salvage-partial | 5 |
| C06 | combo | squashfs_v4_le | squashfs_v4_le | depth-limited extractor-failure | - | no | no | 7 | partial-body-failure | salvage-partial | 5 |
| C07 | combo | squashfs_v4_be | squashfs_v4_be | depth-limited | - | n/a | yes | 8 | depth-limited | raise-depth | 10 |
| C08 | combo | squashfs_v4_be | squashfs_v4_be | depth-limited | - | n/a | no | 7 | depth-limited | raise-depth | 10 |
| C09 | combo | squashfs_v4_be | squashfs_v4_be | extractor-failure unpublished-entry | - | yes | yes | 7 | partial-body-failure | salvage-partial | 5 |
| C10 | combo | squashfs_v4_le | squashfs_v4_le | unpublished-entry | - | n/a | no | 8 | in-tree-symlink-metadata | count-gap | 13 |
| C11 | combo | squashfs_v4_le | squashfs_v4_le | extractor-failure | - | no | no | 4 | partial-body-failure | salvage-partial | 5 |
| C12 | combo | squashfs_v4_be | squashfs_v4_be | unpublished-entry | - | n/a | yes | 7 | mixed-symlinks | audit-symlinks | 11 |
| H01 | clean-be | squashfs_v4_be | squashfs_v4_be | - | - | n/a | no | 6 | clean | none | 14 |
| H02 | clean-be | squashfs_v4_be | squashfs_v4_be | - | - | n/a | no | 8 | clean | none | 14 |
| H03 | clean-le | squashfs_v4_le | squashfs_v4_le | - | - | n/a | no | 4 | clean | none | 14 |
| H04 | clean-le | squashfs_v4_le | squashfs_v4_le | - | - | n/a | no | 7 | clean | none | 14 |
| H05 | clean-empty | squashfs_v4_be | squashfs_v4_be | - | - | n/a | no | 0 | clean-empty | confirm-empty | 14 |
| H06 | clean-empty | squashfs_v4_le | squashfs_v4_le | - | - | n/a | no | 0 | clean-empty | confirm-empty | 14 |
| H07 | escaping-symlink-removed | squashfs_v4_be | squashfs_v4_be | - | - | n/a | yes | 6 | escaping-symlink-removed | expect-link-absent | 12 |
| H08 | escaping-symlink-removed | squashfs_v4_le | squashfs_v4_le | - | - | n/a | yes | 7 | escaping-symlink-removed | expect-link-absent | 12 |
| H09 | in-tree-symlink-metadata | squashfs_v4_be | squashfs_v4_be | unpublished-entry | - | n/a | no | 4 | in-tree-symlink-metadata | count-gap | 13 |
| H10 | in-tree-symlink-metadata | squashfs_v4_le | squashfs_v4_le | unpublished-entry | - | n/a | no | 3 | in-tree-symlink-metadata | count-gap | 13 |
| H11 | mixed-symlinks | squashfs_v4_be | squashfs_v4_be | unpublished-entry | - | n/a | yes | 3 | mixed-symlinks | audit-symlinks | 11 |
| H12 | mixed-symlinks | squashfs_v4_le | squashfs_v4_le | unpublished-entry | - | n/a | yes | 6 | mixed-symlinks | audit-symlinks | 11 |
| H13 | dep-missing-be | squashfs_v4_be | squashfs_v4_be | missing-extractor-dependency | sasquatch-v4be | n/a | no | 0 | dep-missing-be | install-extractor-be | 4 |
| H14 | dep-missing-be | squashfs_v4_be | squashfs_v4_be | missing-extractor-dependency | sasquatch-v4be | n/a | no | 0 | dep-missing-be | install-extractor-be | 4 |
| H15 | dep-missing-le | squashfs_v4_le | squashfs_v4_le | missing-extractor-dependency | sasquatch | n/a | no | 0 | dep-missing-le | install-extractor-le | 4 |
| H16 | dep-missing-le | squashfs_v4_le | squashfs_v4_le | missing-extractor-dependency | sasquatch | n/a | no | 0 | dep-missing-le | install-extractor-le | 4 |
| H17 | avm-marker-be-dropped | squashfs_v4_be | squashfs_v4_be | extractor-failure | - | no | no | 0 | avm-marker-be-dropped | wrap-extractor-be | 6 |
| H18 | avm-marker-be-dropped | squashfs_v4_be | squashfs_v4_be | extractor-failure | - | no | no | 0 | avm-marker-be-dropped | wrap-extractor-be | 6 |
| H19 | body-extractor-failure | squashfs_v4_be | squashfs_v4_be | extractor-failure | - | yes | no | 0 | body-extractor-failure | preserve-failure | 8 |
| H20 | body-extractor-failure | squashfs_v4_be | squashfs_v4_be | extractor-failure | - | yes | no | 0 | body-extractor-failure | preserve-failure | 8 |
| H21 | partial-body-failure | squashfs_v4_be | squashfs_v4_be | extractor-failure | - | yes | no | 7 | partial-body-failure | salvage-partial | 5 |
| H22 | partial-body-failure | squashfs_v4_be | squashfs_v4_be | extractor-failure | - | yes | no | 8 | partial-body-failure | salvage-partial | 5 |
| H23 | no-squashfs-chunk | - | - | - | - | n/a | no | 0 | no-squashfs-chunk | inspect-input | 3 |
| H24 | no-squashfs-chunk | - | - | - | - | n/a | no | 0 | no-squashfs-chunk | inspect-input | 3 |
| H25 | out-of-domain | - | - | - | - | n/a | no | 0 | unclassified | none | 1 |
| H26 | out-of-domain | - | - | - | - | n/a | no | 0 | unclassified | none | 1 |
| H27 | partial-in-tree | squashfs_v4_be | squashfs_v4_be | extractor-failure unpublished-entry | - | yes | no | 4 | partial-body-failure | salvage-partial | 5 |
| H28 | partial-in-tree | squashfs_v4_be | squashfs_v4_be | extractor-failure unpublished-entry | - | yes | no | 7 | partial-body-failure | salvage-partial | 5 |
| H29 | partial-mixed | squashfs_v4_be | squashfs_v4_be | extractor-failure unpublished-entry | - | yes | yes | 3 | partial-body-failure | salvage-partial | 5 |
| H30 | partial-mixed | squashfs_v4_be | squashfs_v4_be | extractor-failure unpublished-entry | - | yes | yes | 5 | partial-body-failure | salvage-partial | 5 |
| H31 | depth-limited-alone | squashfs_v4_be | squashfs_v4_be | depth-limited | - | n/a | no | 6 | depth-limited | raise-depth | 10 |
| H32 | depth-limited-alone | squashfs_v4_le | squashfs_v4_le | depth-limited | - | n/a | no | 6 | depth-limited | raise-depth | 10 |
| H33 | depth-limited-in-tree | squashfs_v4_be | squashfs_v4_be | depth-limited unpublished-entry | - | n/a | no | 8 | depth-limited | raise-depth | 10 |
| H34 | depth-limited-in-tree | squashfs_v4_le | squashfs_v4_le | depth-limited unpublished-entry | - | n/a | no | 9 | depth-limited | raise-depth | 10 |
| H35 | depth-limited-mixed | squashfs_v4_be | squashfs_v4_be | depth-limited unpublished-entry | - | n/a | yes | 5 | depth-limited | raise-depth | 10 |
| H36 | depth-limited-mixed | squashfs_v4_le | squashfs_v4_le | depth-limited unpublished-entry | - | n/a | yes | 6 | depth-limited | raise-depth | 10 |
| H37 | body-extractor-failure-le | squashfs_v4_le | squashfs_v4_le | extractor-failure | - | no | no | 0 | body-extractor-failure | preserve-failure | 8 |
| H38 | body-extractor-failure-le | squashfs_v4_le | squashfs_v4_le | extractor-failure | - | no | no | 0 | body-extractor-failure | preserve-failure | 8 |
| H39 | failure-depth-limited | squashfs_v4_be | squashfs_v4_be | depth-limited extractor-failure | - | yes | no | 1 | partial-body-failure | salvage-partial | 5 |
| H40 | failure-depth-limited | squashfs_v4_le | squashfs_v4_le | depth-limited extractor-failure | - | no | no | 1 | partial-body-failure | salvage-partial | 5 |
| L01 | legacy-clean-v3-le | squashfs_v3 | squashfs_v3 | - | - | n/a | no | 2 | clean | none | 14 |
| L02 | legacy-clean-v3-be | squashfs_v3 | squashfs_v3 | - | - | n/a | no | 2 | clean | none | 14 |
| L03 | legacy-clean-v1-le | squashfs_v1 | squashfs_v1 | - | - | n/a | no | 3 | clean | none | 14 |
| L04 | legacy-clean-v1-be | squashfs_v1 | squashfs_v1 | - | - | n/a | no | 3 | clean | none | 14 |
| L05 | legacy-clean-v2-le | squashfs_v2 | squashfs_v2 | - | - | n/a | no | 4 | clean | none | 14 |
| L06 | legacy-clean-v2-nonstandard-le | squashfs_v2_nonstandard | squashfs_v2_nonstandard | - | - | n/a | no | 4 | clean | none | 14 |
| L07 | legacy-clean-v3-broadcom-le | squashfs_v3_broadcom | squashfs_v3_broadcom | - | - | n/a | no | 2 | clean | none | 14 |
| L08 | legacy-clean-v3-nonstandard-le | squashfs_v3_nonstandard | squashfs_v3_nonstandard | - | - | n/a | no | 2 | clean | none | 14 |
| L09 | legacy-clean-v3-ddwrt-le | squashfs_v3_ddwrt | squashfs_v3_ddwrt | - | - | n/a | no | 4 | clean | none | 14 |
| L10 | legacy-clean-v3-adaptive-lzma-le | squashfs_v3 | squashfs_v3 | - | - | n/a | no | 2 | clean | none | 14 |
| L11 | legacy-depth-limited-v3-le | squashfs_v3 | squashfs_v3 | depth-limited | - | n/a | no | 2 | depth-limited | raise-depth | 10 |
| L12 | legacy-dep-missing-le | squashfs_v3 | squashfs_v3 | missing-extractor-dependency | sasquatch | n/a | no | 0 | dep-missing-le | install-extractor-le | 4 |
| L13 | legacy-body-failure-v3-le | squashfs_v3 | squashfs_v3 | extractor-failure | - | no | no | 0 | legacy-body-failure | cross-read-legacy | 7 |
| L14 | legacy-body-failure-v3-be | squashfs_v3 | squashfs_v3 | extractor-failure | - | yes | no | 0 | legacy-body-failure | cross-read-legacy | 7 |
| L15 | legacy-body-failure-v1-le | squashfs_v1 | squashfs_v1 | extractor-failure | - | no | no | 0 | legacy-body-failure | cross-read-legacy | 7 |
| L16 | legacy-body-failure-v1-be | squashfs_v1 | squashfs_v1 | extractor-failure | - | yes | no | 0 | legacy-body-failure | cross-read-legacy | 7 |
| L17 | legacy-body-failure-v2-le | squashfs_v2 | squashfs_v2 | extractor-failure | - | no | no | 0 | legacy-body-failure | cross-read-legacy | 7 |
| L18 | legacy-body-failure-v2-nonstandard-le | squashfs_v2_nonstandard | squashfs_v2_nonstandard | extractor-failure | - | no | no | 0 | legacy-body-failure | cross-read-legacy | 7 |
| L19 | mixed-clean-v3-v4be | squashfs_v3 squashfs_v4_be | squashfs_v3 squashfs_v4_be | - | - | n/a | no | 8 | clean | none | 14 |
| L20 | mixed-failing-v3-empty-v4be | squashfs_v3 squashfs_v4_be | squashfs_v3 | extractor-failure | - | no | no | 1 | partial-body-failure | salvage-partial | 5 |
| L21 | container-depth-limited-tar | - | - | depth-limited | - | n/a | no | 1 | container-depth-limited | raise-depth | 2 |
| L22 | unknown-residue-v3-le | squashfs_v3 | squashfs_v3 | unknown-chunk-handler | - | n/a | no | 3 | unknown-residue | isolate-residue | 9 |
| L23 | union-dep-plus-failure-a | squashfs_v3 squashfs_v4_be | squashfs_v3 | extractor-failure missing-extractor-dependency | sasquatch-v4be | no | no | 2 | dep-missing-be | install-extractor-be | 4 |
| L24 | union-dep-plus-failure-b | squashfs_v3 squashfs_v4_be | squashfs_v3 | extractor-failure missing-extractor-dependency | sasquatch-v4be | no | no | 2 | dep-missing-be | install-extractor-be | 4 |

