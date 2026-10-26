| case | d | H | G | D | BE | SR | P | depth-limited paths | inner image published | v2 label | draft-v3 label |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `sh-alone-le-d1` | 1 | squashfs_v4_le | depth-limited | ∅ | n/a | no | 3 | `firmware.bin_extract` | yes (inner.sqsh) | unclassified | depth-limited-nested |
| `sh-alone-le-d2` | 2 | squashfs_v4_le | depth-limited | ∅ | n/a | no | 5 | `firmware.bin_extract/inner.sqsh_extract` | yes (inner.sqsh) | unclassified | depth-limited-nested |
| `sh-alone-le-d3` | 3 | squashfs_v4_le | ∅ | ∅ | n/a | no | 5 | ∅ | yes (inner.sqsh) | clean | clean |
| `sh-intree-le-d1` | 1 | squashfs_v4_le | depth-limited,unpublished-entry | ∅ | n/a | no | 3 | `firmware.bin_extract` | yes (inner.sqsh) | unclassified | depth-limited-nested |
| `sh-intree-le-d2` | 2 | squashfs_v4_le | depth-limited,unpublished-entry | ∅ | n/a | no | 5 | `firmware.bin_extract/inner.sqsh_extract` | yes (inner.sqsh) | unclassified | depth-limited-nested |
| `sh-intree-le-d3` | 3 | squashfs_v4_le | unpublished-entry | ∅ | n/a | no | 5 | ∅ | yes (inner.sqsh) | in-tree-symlink-metadata | in-tree-symlink-metadata |
| `sh-escaping-le-d1` | 1 | squashfs_v4_le | depth-limited | ∅ | n/a | yes | 3 | `firmware.bin_extract` | yes (inner.sqsh) | escaping-symlink-removed | depth-limited-nested |
| `sh-escaping-le-d2` | 2 | squashfs_v4_le | depth-limited | ∅ | n/a | yes | 5 | `firmware.bin_extract/inner.sqsh_extract` | yes (inner.sqsh) | escaping-symlink-removed | depth-limited-nested |
| `sh-escaping-le-d3` | 3 | squashfs_v4_le | ∅ | ∅ | n/a | yes | 5 | ∅ | yes (inner.sqsh) | escaping-symlink-removed | escaping-symlink-removed |
| `sh-both-le-d1` | 1 | squashfs_v4_le | depth-limited,unpublished-entry | ∅ | n/a | yes | 3 | `firmware.bin_extract` | yes (inner.sqsh) | escaping-symlink-removed | depth-limited-nested |
| `sh-both-le-d2` | 2 | squashfs_v4_le | depth-limited,unpublished-entry | ∅ | n/a | yes | 5 | `firmware.bin_extract/inner.sqsh_extract` | yes (inner.sqsh) | escaping-symlink-removed | depth-limited-nested |
| `sh-both-le-d3` | 3 | squashfs_v4_le | unpublished-entry | ∅ | n/a | yes | 5 | ∅ | yes (inner.sqsh) | mixed-symlinks | mixed-symlinks |
| `dp-alone-le-d3` | 3 | squashfs_v4_le | depth-limited | ∅ | n/a | no | 7 | `firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract` | yes (inner.sqsh) | unclassified | depth-limited-nested |
| `dp-alone-le-d2` | 2 | squashfs_v4_le | depth-limited | ∅ | n/a | no | 5 | `firmware.bin_extract/inner.sqsh_extract` | yes (inner.sqsh) | unclassified | depth-limited-nested |
| `lk-links-le-d3` | 3 | squashfs_v4_le | depth-limited,unpublished-entry | ∅ | n/a | yes | 7 | `firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract` | yes (inner.sqsh) | escaping-symlink-removed | depth-limited-nested |
| `tw-two-le-d1` | 1 | squashfs_v4_le | depth-limited | ∅ | n/a | no | 4 | `firmware.bin_extract` | yes (inner_a.sqsh,inner_b.sqsh) | unclassified | depth-limited-nested |
| `tw-two-le-d2` | 2 | squashfs_v4_le | depth-limited | ∅ | n/a | no | 8 | `firmware.bin_extract/inner_a.sqsh_extract`, `firmware.bin_extract/inner_b.sqsh_extract` | yes (inner_a.sqsh,inner_b.sqsh) | unclassified | depth-limited-nested |
| `pf-partial-le-d3` | 3 | squashfs_v4_le | depth-limited,extractor-failure | ∅ | no | no | 8 | `firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract` | yes (inner.sqsh) | unclassified | partial-body-failure |
| `my-unknown-le-d3` | 3 | squashfs_v4_le | depth-limited | ∅ | n/a | no | 8 | `firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract` | yes (inner.sqsh) | unclassified | depth-limited-nested |
| `ta-tail-le-d3` | 3 | squashfs_v4_le | depth-limited,unknown-chunk-handler | ∅ | n/a | no | 11 | `firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract` | yes (inner.sqsh) | unclassified | depth-limited-nested |
| `sh-alone-be-d1` | 1 | squashfs_v4_be | depth-limited | ∅ | n/a | no | 3 | `firmware.bin_extract` | yes (inner.sqsh) | unclassified | depth-limited-nested |
| `sh-alone-be-d2` | 2 | squashfs_v4_be | depth-limited | ∅ | n/a | no | 5 | `firmware.bin_extract/inner.sqsh_extract` | yes (inner.sqsh) | unclassified | depth-limited-nested |
| `sh-alone-be-d3` | 3 | squashfs_v4_be | ∅ | ∅ | n/a | no | 5 | ∅ | yes (inner.sqsh) | clean | clean |
| `sh-intree-be-d1` | 1 | squashfs_v4_be | depth-limited,unpublished-entry | ∅ | n/a | no | 3 | `firmware.bin_extract` | yes (inner.sqsh) | unclassified | depth-limited-nested |
| `sh-intree-be-d2` | 2 | squashfs_v4_be | depth-limited,unpublished-entry | ∅ | n/a | no | 5 | `firmware.bin_extract/inner.sqsh_extract` | yes (inner.sqsh) | unclassified | depth-limited-nested |
| `sh-intree-be-d3` | 3 | squashfs_v4_be | unpublished-entry | ∅ | n/a | no | 5 | ∅ | yes (inner.sqsh) | in-tree-symlink-metadata | in-tree-symlink-metadata |
| `sh-escaping-be-d1` | 1 | squashfs_v4_be | depth-limited | ∅ | n/a | yes | 3 | `firmware.bin_extract` | yes (inner.sqsh) | escaping-symlink-removed | depth-limited-nested |
| `sh-escaping-be-d2` | 2 | squashfs_v4_be | depth-limited | ∅ | n/a | yes | 5 | `firmware.bin_extract/inner.sqsh_extract` | yes (inner.sqsh) | escaping-symlink-removed | depth-limited-nested |
| `sh-escaping-be-d3` | 3 | squashfs_v4_be | ∅ | ∅ | n/a | yes | 5 | ∅ | yes (inner.sqsh) | escaping-symlink-removed | escaping-symlink-removed |
| `sh-both-be-d1` | 1 | squashfs_v4_be | depth-limited,unpublished-entry | ∅ | n/a | yes | 3 | `firmware.bin_extract` | yes (inner.sqsh) | escaping-symlink-removed | depth-limited-nested |
| `sh-both-be-d2` | 2 | squashfs_v4_be | depth-limited,unpublished-entry | ∅ | n/a | yes | 5 | `firmware.bin_extract/inner.sqsh_extract` | yes (inner.sqsh) | escaping-symlink-removed | depth-limited-nested |
| `sh-both-be-d3` | 3 | squashfs_v4_be | unpublished-entry | ∅ | n/a | yes | 5 | ∅ | yes (inner.sqsh) | mixed-symlinks | mixed-symlinks |
| `dp-alone-be-d3` | 3 | squashfs_v4_be | depth-limited | ∅ | n/a | no | 7 | `firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract` | yes (inner.sqsh) | unclassified | depth-limited-nested |
| `dp-alone-be-d2` | 2 | squashfs_v4_be | depth-limited | ∅ | n/a | no | 5 | `firmware.bin_extract/inner.sqsh_extract` | yes (inner.sqsh) | unclassified | depth-limited-nested |
| `lk-links-be-d3` | 3 | squashfs_v4_be | depth-limited,unpublished-entry | ∅ | n/a | yes | 7 | `firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract` | yes (inner.sqsh) | escaping-symlink-removed | depth-limited-nested |
| `tw-two-be-d1` | 1 | squashfs_v4_be | depth-limited | ∅ | n/a | no | 4 | `firmware.bin_extract` | yes (inner_a.sqsh,inner_b.sqsh) | unclassified | depth-limited-nested |
| `tw-two-be-d2` | 2 | squashfs_v4_be | depth-limited | ∅ | n/a | no | 8 | `firmware.bin_extract/inner_a.sqsh_extract`, `firmware.bin_extract/inner_b.sqsh_extract` | yes (inner_a.sqsh,inner_b.sqsh) | unclassified | depth-limited-nested |
| `pf-partial-be-d3` | 3 | squashfs_v4_be | depth-limited,extractor-failure | ∅ | yes | no | 8 | `firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract` | yes (inner.sqsh) | unclassified | partial-body-failure |
| `my-unknown-be-d3` | 3 | squashfs_v4_be | depth-limited | ∅ | n/a | no | 8 | `firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract` | yes (inner.sqsh) | unclassified | depth-limited-nested |
| `ta-tail-be-d3` | 3 | squashfs_v4_be | depth-limited,unknown-chunk-handler | ∅ | n/a | no | 11 | `firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract` | yes (inner.sqsh) | unclassified | depth-limited-nested |

OK: 40 cases, every invariant held
