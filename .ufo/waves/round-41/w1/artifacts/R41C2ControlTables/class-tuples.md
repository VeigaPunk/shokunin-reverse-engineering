| class fixture | OP | PR | H | G | D | BE | SR | P | expected | step | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| H01 | `extract_firmware` | `unblob` | `squashfs_v4_be` | ∅ | ∅ | n/a | no | 5 | clean/none | 11 | committed: corpus/evidence/round-40/c2/heldout/H01/envelope.json |
| H02 | `extract_firmware` | `unblob` | `squashfs_v4_be` | ∅ | ∅ | n/a | no | 3 | clean/none | 11 | committed: corpus/evidence/round-40/c2/heldout/H02/envelope.json |
| H03 | `extract_firmware` | `unblob` | `squashfs_v4_le` | ∅ | ∅ | n/a | no | 8 | clean/none | 11 | committed: corpus/evidence/round-40/c2/heldout/H03/envelope.json |
| H04 | `extract_firmware` | `unblob` | `squashfs_v4_le` | ∅ | ∅ | n/a | no | 5 | clean/none | 11 | committed: corpus/evidence/round-40/c2/heldout/H04/envelope.json |
| H05 | `extract_firmware` | `unblob` | `squashfs_v4_be` | ∅ | ∅ | n/a | no | 0 | clean-empty/confirm-empty | 11 | committed: corpus/evidence/round-40/c2/heldout/H05/envelope.json |
| H06 | `extract_firmware` | `unblob` | `squashfs_v4_le` | ∅ | ∅ | n/a | no | 0 | clean-empty/confirm-empty | 11 | committed: corpus/evidence/round-40/c2/heldout/H06/envelope.json |
| H07 | `extract_firmware` | `unblob` | `squashfs_v4_be` | ∅ | ∅ | n/a | yes | 3 | escaping-symlink-removed/expect-link-absent | 9 | committed: corpus/evidence/round-40/c2/heldout/H07/envelope.json |
| H08 | `extract_firmware` | `unblob` | `squashfs_v4_le` | ∅ | ∅ | n/a | yes | 8 | escaping-symlink-removed/expect-link-absent | 9 | committed: corpus/evidence/round-40/c2/heldout/H08/envelope.json |
| H09 | `extract_firmware` | `unblob` | `squashfs_v4_be` | `unpublished-entry` | ∅ | n/a | no | 8 | in-tree-symlink-metadata/count-gap | 10 | committed: corpus/evidence/round-40/c2/heldout/H09/envelope.json |
| H10 | `extract_firmware` | `unblob` | `squashfs_v4_le` | `unpublished-entry` | ∅ | n/a | no | 5 | in-tree-symlink-metadata/count-gap | 10 | committed: corpus/evidence/round-40/c2/heldout/H10/envelope.json |
| H11 | `extract_firmware` | `unblob` | `squashfs_v4_be` | `unpublished-entry` | ∅ | n/a | yes | 5 | mixed-symlinks/audit-symlinks | 8 | committed: corpus/evidence/round-40/c2/heldout/H11/envelope.json |
| H12 | `extract_firmware` | `unblob` | `squashfs_v4_le` | `unpublished-entry` | ∅ | n/a | yes | 4 | mixed-symlinks/audit-symlinks | 8 | committed: corpus/evidence/round-40/c2/heldout/H12/envelope.json |
| H13 | `extract_firmware` | `unblob` | `squashfs_v4_be` | `missing-extractor-dependency` | `sasquatch-v4be` | n/a | no | 0 | dep-missing-be/install-extractor-be | 3 | committed: corpus/evidence/round-40/c2/heldout/H13/envelope.json |
| H14 | `extract_firmware` | `unblob` | `squashfs_v4_be` | `missing-extractor-dependency` | `sasquatch-v4be` | n/a | no | 0 | dep-missing-be/install-extractor-be | 3 | committed: corpus/evidence/round-40/c2/heldout/H14/envelope.json |
| H15 | `extract_firmware` | `unblob` | `squashfs_v4_le` | `missing-extractor-dependency` | `sasquatch` | n/a | no | 0 | dep-missing-le/install-extractor-le | 3 | committed: corpus/evidence/round-40/c2/heldout/H15/envelope.json |
| H16 | `extract_firmware` | `unblob` | `squashfs_v4_le` | `missing-extractor-dependency` | `sasquatch` | n/a | no | 0 | dep-missing-le/install-extractor-le | 3 | committed: corpus/evidence/round-40/c2/heldout/H16/envelope.json |
| H17 | `extract_firmware` | `unblob` | `squashfs_v4_be` | `extractor-failure` | ∅ | no | no | 0 | avm-marker-be-dropped/wrap-extractor-be | 5 | committed: corpus/evidence/round-40/c2/heldout/H17/envelope.json |
| H18 | `extract_firmware` | `unblob` | `squashfs_v4_be` | `extractor-failure` | ∅ | no | no | 0 | avm-marker-be-dropped/wrap-extractor-be | 5 | committed: corpus/evidence/round-40/c2/heldout/H18/envelope.json |
| H19 | `extract_firmware` | `unblob` | `squashfs_v4_be` | `extractor-failure` | ∅ | yes | no | 0 | body-extractor-failure/preserve-failure | 6 | committed: corpus/evidence/round-40/c2/heldout/H19/envelope.json |
| H20 | `extract_firmware` | `unblob` | `squashfs_v4_be` | `extractor-failure` | ∅ | yes | no | 0 | body-extractor-failure/preserve-failure | 6 | committed: corpus/evidence/round-40/c2/heldout/H20/envelope.json |
| H21 | `extract_firmware` | `unblob` | `squashfs_v4_be` | `extractor-failure` | ∅ | yes | no | 5 | partial-body-failure/salvage-partial | 4 | committed: corpus/evidence/round-40/c2/heldout/H21/envelope.json |
| H22 | `extract_firmware` | `unblob` | `squashfs_v4_be` | `extractor-failure` | ∅ | yes | no | 3 | partial-body-failure/salvage-partial | 4 | committed: corpus/evidence/round-40/c2/heldout/H22/envelope.json |
| H23 | `extract_firmware` | `unblob` | ∅ | ∅ | ∅ | n/a | no | 0 | no-squashfs-chunk/inspect-input | 2 | committed: corpus/evidence/round-40/c2/heldout/H23/envelope.json |
| H24 | `extract_firmware` | `unblob` | ∅ | ∅ | ∅ | n/a | no | 0 | no-squashfs-chunk/inspect-input | 2 | committed: corpus/evidence/round-40/c2/heldout/H24/envelope.json |
| H25 | `inspect_firmware_regions` | `binwalk` | ∅ | ∅ | ∅ | n/a | no | 0 | unclassified/none | 1 | committed: corpus/evidence/round-40/c2/heldout/H25/envelope.json |
| H26 | `inspect_firmware_regions` | `binwalk` | ∅ | ∅ | ∅ | n/a | no | 0 | unclassified/none | 1 | committed: corpus/evidence/round-40/c2/heldout/H26/envelope.json |
| depth-limited-alone-1 | `extract_firmware` | `unblob` | `squashfs_v4_be` | `depth-limited` | ∅ | n/a | no | 6 | depth-limited-nested/raise-depth | 7 | PREDICTED from corpus/evidence/round-40/c2/heldout/H01/envelope.json |
| depth-limited-alone-2 | `extract_firmware` | `unblob` | `squashfs_v4_be` | `depth-limited` | ∅ | n/a | no | 4 | depth-limited-nested/raise-depth | 7 | PREDICTED from corpus/evidence/round-40/c2/heldout/H02/envelope.json |
| depth-limited-in-tree-1 | `extract_firmware` | `unblob` | `squashfs_v4_be` | `depth-limited`, `unpublished-entry` | ∅ | n/a | no | 6 | depth-limited-nested/raise-depth | 7 | PREDICTED from corpus/evidence/round-40/c2/heldout/H01/envelope.json |
| depth-limited-in-tree-2 | `extract_firmware` | `unblob` | `squashfs_v4_be` | `depth-limited`, `unpublished-entry` | ∅ | n/a | no | 4 | depth-limited-nested/raise-depth | 7 | PREDICTED from corpus/evidence/round-40/c2/heldout/H02/envelope.json |
| depth-limited-mixed-1 | `extract_firmware` | `unblob` | `squashfs_v4_be` | `depth-limited`, `unpublished-entry` | ∅ | n/a | yes | 6 | depth-limited-nested/raise-depth | 7 | PREDICTED from corpus/evidence/round-40/c2/heldout/H01/envelope.json |
| depth-limited-mixed-2 | `extract_firmware` | `unblob` | `squashfs_v4_be` | `depth-limited`, `unpublished-entry` | ∅ | n/a | yes | 4 | depth-limited-nested/raise-depth | 7 | PREDICTED from corpus/evidence/round-40/c2/heldout/H02/envelope.json |
| partial-in-tree-1 | `extract_firmware` | `unblob` | `squashfs_v4_be` | `extractor-failure`, `unpublished-entry` | ∅ | yes | no | 5 | partial-body-failure/salvage-partial | 4 | PREDICTED from corpus/evidence/round-40/c2/heldout/H21/envelope.json |
| partial-in-tree-2 | `extract_firmware` | `unblob` | `squashfs_v4_be` | `extractor-failure`, `unpublished-entry` | ∅ | yes | no | 3 | partial-body-failure/salvage-partial | 4 | PREDICTED from corpus/evidence/round-40/c2/heldout/H22/envelope.json |
| partial-mixed-1 | `extract_firmware` | `unblob` | `squashfs_v4_be` | `extractor-failure`, `unpublished-entry` | ∅ | yes | yes | 5 | partial-body-failure/salvage-partial | 4 | PREDICTED from corpus/evidence/round-40/c2/heldout/H21/envelope.json |
| partial-mixed-2 | `extract_firmware` | `unblob` | `squashfs_v4_be` | `extractor-failure`, `unpublished-entry` | ∅ | yes | yes | 3 | partial-body-failure/salvage-partial | 4 | PREDICTED from corpus/evidence/round-40/c2/heldout/H22/envelope.json |

# 36 envelopes; 10 predicted, 26 committed
