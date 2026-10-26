| `a1` | `squashfs_v4_be` | false | none | none | n/a | no | none | 4 | 244 | complete | - | - |
| `a2` | `squashfs_v4_be` | false | none | none | n/a | no | none | 3 | 6039 | complete | - | - |
| `b1` | `squashfs_v4_le` | false | none | none | n/a | no | none | 3 | 57 | complete | - | - |
| `b2` | `squashfs_v4_le` | false | none | none | n/a | no | none | 3 | 3031 | complete | - | - |
| `c1` | `squashfs_v4_be` | false | none | none | n/a | yes | none | 2 | 28 | partial | MaliciousSymlinkRemoved | - |
| `c2` | `squashfs_v4_be` | false | none | none | n/a | yes | none | 2 | 21 | partial | MaliciousSymlinkRemoved | - |
| `d1` | `squashfs_v4_be` | false | `unpublished-entry` | none | n/a | no | `symlink` | 2 | 19 | partial | - | - |
| `d2` | `squashfs_v4_be` | false | `unpublished-entry` | none | n/a | no | `symlink` | 2 | 19 | partial | - | - |
| `c2-twolevel` | `squashfs_v4_be` | false | `unpublished-entry` | none | n/a | no | `symlink` | 2 | 21 | partial | - | - |
| `e1` | `squashfs_v4_be` | false | `unpublished-entry` | none | n/a | yes | `symlink` | 2 | 18 | partial | MaliciousSymlinkRemoved | - |
| `f1` | `squashfs_v4_be` | false | `unpublished-entry` | none | n/a | no | `symlink` | 2 | 19 | partial | - | - |
| `f2` | `squashfs_v4_be` | false | none | none | n/a | yes | none | 1 | 10 | partial | MaliciousSymlinkRemoved | - |
| `be-body-damaged` | `squashfs_v4_be` | false | none | none | n/a | no | none | 4 | 244 | complete | - | - |
| `be-meta-damaged` | `squashfs_v4_be` | true | `extractor-failure` | none | yes | no | none | 0 | 0 | partial | ExtractCommandFailedReport | `sasquatch-v4be -be -no-exit-code -f -d /tmp/rea-firmware-FZQ5wr/extracted/firmware.bin_extract /tmp/rea-firmware-FZQ5wr/firmware.bin` |
| `k3-after` | `squashfs_v4_be` | false | none | none | n/a | no | none | 4 | 28 | complete | - | - |
| `k4-after` | `squashfs_v4_be` | false | none | none | n/a | no | none | 4 | 28 | complete | - | - |
| `k1-after` | `squashfs_v4_be` | false | none | none | n/a | yes | none | 5 | 9656 | partial | MaliciousSymlinkRemoved | - |
| `orig-k1` | `squashfs_v4_be` | false | none | none | n/a | yes | none | 5 | 9656 | partial | MaliciousSymlinkRemoved | - |
| `k2-after` | `squashfs_v4_be` | false | `unpublished-entry` | none | n/a | no | `symlink` | 3 | 10283 | partial | - | - |
| `k1-before` | `squashfs_v4_be` | true | `missing-extractor-dependency` | `sasquatch-v4be` | n/a | no | none | 0 | 0 | partial | ExtractorDependencyNotFoundReport | - |
| `avm-k1` | `squashfs_v4_be` | true | `extractor-failure` | none | no | no | none | 0 | 0 | partial | ExtractCommandFailedReport | `sasquatch-v4be -no-exit-code -f -d /tmp/rea-firmware-SuWPba/extracted/firmware.bin_extract /tmp/rea-firmware-SuWPba/firmware.bin` |
