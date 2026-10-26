# step-matrix over 36 envelopes (planned classes), interp=DEV replica v3-check-interp.py
| control | matched | s1 | s2 | s3 | s4 | s5 | s6 | s7 | s8 | s9 | s10 | s11 | s12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CTL-C2-0-base-SKILL | 0/36 | 2 | 2 | 4 | 6 | 2 | 2 | 6 | 2 | 2 | 2 | 6 | · |
| CTL-C2-1-catch-all | 4/36 | 2 | 2 | 4 | 6 | 2 | 2 | 6 | 2 | 2 | 2 | 2 | · |
| CTL-C2-2-v2-verbatim | 26/36 | · | · | · | 4 | · | · | 6 | · | · | · | · | · |
| CTL-C2-3-actions-rotated | 2/36 | · | 2 | 4 | 6 | 2 | 2 | 6 | 2 | 2 | 2 | 6 | · |
| CTL-C2-3b-v2-actions-rotated | 2/36 | · | 2 | 4 | 6 | 2 | 2 | 6 | 2 | 2 | 2 | 6 | · |
| CTL-C2-4-no-contains | 28/36 | · | · | · | 4 | · | · | 4 | · | · | · | · | · |
| CTL-C2-5-default-row | 30/36 | · | · | · | 4 | · | · | 2 | · | · | · | · | · |
| CTL-C2-5b-all-star-default-row | 28/36 | 2 | · | · | 4 | · | · | 2 | · | · | · | · | · |
| CTL-C2-5c-inert-default-row | 26/36 | · | · | · | 4 | · | · | 6 | · | · | · | · | · |
| CTL-C2-6-depth-row-only | 32/36 | · | · | · | 4 | · | · | · | · | · | · | · | · |
| CTL-C2-REF-precedence | 36/36 | · | · | · | · | · | · | · | · | · | · | · | · |

## CTL-C2-0-base-SKILL  0/36  (exit 2: line 361: a v2 marker is refused by the v3 interpreter)
   step 1  unclassified/none                      missed on H25, H26
   step 2  no-squashfs-chunk/inspect-input        missed on H23, H24
   step 3  dep-missing-be/install-extractor-be    missed on H13, H14
   step 3  dep-missing-le/install-extractor-le    missed on H15, H16
   step 4  partial-body-failure/salvage-partial   missed on H21, H22, partial-in-tree-1, partial-in-tree-2, partial-mixed-1, partial-mixed-2
   step 5  avm-marker-be-dropped/wrap-extractor-be missed on H17, H18
   step 6  body-extractor-failure/preserve-failure missed on H19, H20
   step 7  depth-limited-nested/raise-depth       missed on depth-limited-alone-1, depth-limited-alone-2, depth-limited-in-tree-1, depth-limited-in-tree-2, depth-limited-mixed-1, depth-limited-mixed-2
   step 8  mixed-symlinks/audit-symlinks          missed on H11, H12
   step 9  escaping-symlink-removed/expect-link-absent missed on H07, H08
   step 10 in-tree-symlink-metadata/count-gap     missed on H09, H10
   step 11 clean/none                             missed on H01, H02, H03, H04
   step 11 clean-empty/confirm-empty              missed on H05, H06

## CTL-C2-1-catch-all  4/36  (ok)
   step 1  unclassified/none                      missed on H25, H26
   step 2  no-squashfs-chunk/inspect-input        missed on H23, H24
   step 3  dep-missing-be/install-extractor-be    missed on H13, H14
   step 3  dep-missing-le/install-extractor-le    missed on H15, H16
   step 4  partial-body-failure/salvage-partial   missed on H21, H22, partial-in-tree-1, partial-in-tree-2, partial-mixed-1, partial-mixed-2
   step 5  avm-marker-be-dropped/wrap-extractor-be missed on H17, H18
   step 6  body-extractor-failure/preserve-failure missed on H19, H20
   step 7  depth-limited-nested/raise-depth       missed on depth-limited-alone-1, depth-limited-alone-2, depth-limited-in-tree-1, depth-limited-in-tree-2, depth-limited-mixed-1, depth-limited-mixed-2
   step 8  mixed-symlinks/audit-symlinks          missed on H11, H12
   step 9  escaping-symlink-removed/expect-link-absent missed on H07, H08
   step 10 in-tree-symlink-metadata/count-gap     missed on H09, H10
   step 11 clean-empty/confirm-empty              missed on H05, H06

## CTL-C2-2-v2-verbatim  26/36  (ok)
   step 4  partial-body-failure/salvage-partial   missed on partial-in-tree-1, partial-in-tree-2, partial-mixed-1, partial-mixed-2
   step 7  depth-limited-nested/raise-depth       missed on depth-limited-alone-1, depth-limited-alone-2, depth-limited-in-tree-1, depth-limited-in-tree-2, depth-limited-mixed-1, depth-limited-mixed-2

## CTL-C2-3-actions-rotated  2/36  (ok)
   step 2  no-squashfs-chunk/inspect-input        missed on H23, H24
   step 3  dep-missing-be/install-extractor-be    missed on H13, H14
   step 3  dep-missing-le/install-extractor-le    missed on H15, H16
   step 4  partial-body-failure/salvage-partial   missed on H21, H22, partial-in-tree-1, partial-in-tree-2, partial-mixed-1, partial-mixed-2
   step 5  avm-marker-be-dropped/wrap-extractor-be missed on H17, H18
   step 6  body-extractor-failure/preserve-failure missed on H19, H20
   step 7  depth-limited-nested/raise-depth       missed on depth-limited-alone-1, depth-limited-alone-2, depth-limited-in-tree-1, depth-limited-in-tree-2, depth-limited-mixed-1, depth-limited-mixed-2
   step 8  mixed-symlinks/audit-symlinks          missed on H11, H12
   step 9  escaping-symlink-removed/expect-link-absent missed on H07, H08
   step 10 in-tree-symlink-metadata/count-gap     missed on H09, H10
   step 11 clean/none                             missed on H01, H02, H03, H04
   step 11 clean-empty/confirm-empty              missed on H05, H06

## CTL-C2-3b-v2-actions-rotated  2/36  (ok)
   step 2  no-squashfs-chunk/inspect-input        missed on H23, H24
   step 3  dep-missing-be/install-extractor-be    missed on H13, H14
   step 3  dep-missing-le/install-extractor-le    missed on H15, H16
   step 4  partial-body-failure/salvage-partial   missed on H21, H22, partial-in-tree-1, partial-in-tree-2, partial-mixed-1, partial-mixed-2
   step 5  avm-marker-be-dropped/wrap-extractor-be missed on H17, H18
   step 6  body-extractor-failure/preserve-failure missed on H19, H20
   step 7  depth-limited-nested/raise-depth       missed on depth-limited-alone-1, depth-limited-alone-2, depth-limited-in-tree-1, depth-limited-in-tree-2, depth-limited-mixed-1, depth-limited-mixed-2
   step 8  mixed-symlinks/audit-symlinks          missed on H11, H12
   step 9  escaping-symlink-removed/expect-link-absent missed on H07, H08
   step 10 in-tree-symlink-metadata/count-gap     missed on H09, H10
   step 11 clean/none                             missed on H01, H02, H03, H04
   step 11 clean-empty/confirm-empty              missed on H05, H06

## CTL-C2-4-no-contains  28/36  (ok)
   step 4  partial-body-failure/salvage-partial   missed on partial-in-tree-1, partial-in-tree-2, partial-mixed-1, partial-mixed-2
   step 7  depth-limited-nested/raise-depth       missed on depth-limited-in-tree-1, depth-limited-in-tree-2, depth-limited-mixed-1, depth-limited-mixed-2

## CTL-C2-5-default-row  30/36  (ok)
   step 4  partial-body-failure/salvage-partial   missed on partial-in-tree-1, partial-in-tree-2, partial-mixed-1, partial-mixed-2
   step 7  depth-limited-nested/raise-depth       missed on depth-limited-mixed-1, depth-limited-mixed-2

## CTL-C2-5b-all-star-default-row  28/36  (ok)
   step 1  unclassified/none                      missed on H25, H26
   step 4  partial-body-failure/salvage-partial   missed on partial-in-tree-1, partial-in-tree-2, partial-mixed-1, partial-mixed-2
   step 7  depth-limited-nested/raise-depth       missed on depth-limited-mixed-1, depth-limited-mixed-2

## CTL-C2-5c-inert-default-row  26/36  (ok)
   step 4  partial-body-failure/salvage-partial   missed on partial-in-tree-1, partial-in-tree-2, partial-mixed-1, partial-mixed-2
   step 7  depth-limited-nested/raise-depth       missed on depth-limited-alone-1, depth-limited-alone-2, depth-limited-in-tree-1, depth-limited-in-tree-2, depth-limited-mixed-1, depth-limited-mixed-2

## CTL-C2-6-depth-row-only  32/36  (ok)
   step 4  partial-body-failure/salvage-partial   missed on partial-in-tree-1, partial-in-tree-2, partial-mixed-1, partial-mixed-2

## CTL-C2-REF-precedence  36/36  (ok)
   matches the precedence list on every envelope
