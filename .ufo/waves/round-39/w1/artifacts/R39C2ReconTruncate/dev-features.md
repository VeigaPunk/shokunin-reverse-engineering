| carrier | recipe | H | G | D | BE | SR | P | coverage | bytes_used vs size | chunk@ | label |
|---|---|---|---|---|---|---|---|---|---|---|---|
| be-base-gzip | base | {squashfs_v4_be} | {} | {} | n/a | no | 6 | complete | 27033 vs 27033 | 0:squashfs_v4_be | clean |
| be-base-xz | base | {squashfs_v4_be} | {} | {} | n/a | no | 6 | complete | 27033 vs 27033 | 0:squashfs_v4_be | clean |
| be-elfwrap | elf_wrap | {squashfs_v4_be} | {} | {} | n/a | no | 7 | complete | - | 0:elf64,0:elf64,43320:squashfs_v4_be | clean |
| be-elfwrap-trunc | elf_wrap_trunc | {} | {unknown-chunk-handler} | {} | n/a | no | 2 | partial | - | 0:elf64,43320:None,0:elf64 | unclassified |
| be-oversize-plus1 | oversize_plus1 | {} | {} | {} | n/a | no | 0 | complete | 27034 vs 27033 | - | no-squashfs-chunk |
| be-oversize-plus4096 | oversize_plus4096 | {} | {} | {} | n/a | no | 0 | complete | 31129 vs 27033 | - | no-squashfs-chunk |
| be-oversize-x2 | oversize_x2 | {} | {} | {} | n/a | no | 0 | complete | 54066 vs 27033 | - | no-squashfs-chunk |
| be-prefix4k | prefix4k | {squashfs_v4_be} | {unknown-chunk-handler} | {} | n/a | no | 7 | partial | - | 0:None,4096:squashfs_v4_be | garbage-prefix-or-tail |
| be-prefix4k-trunc | prefix4k_trunc | {} | {} | {} | n/a | no | 0 | complete | - | - | no-squashfs-chunk |
| be-trailing4k | trailing4k | {squashfs_v4_be} | {unknown-chunk-handler} | {} | n/a | no | 7 | partial | 27033 vs 31129 | 27033:None,0:squashfs_v4_be | garbage-prefix-or-tail |
| be-trunc-3q | trunc_3q | {} | {} | {} | n/a | no | 0 | complete | 27033 vs 20274 | - | no-squashfs-chunk |
| be-trunc-half | trunc_half | {} | {} | {} | n/a | no | 0 | complete | 27033 vs 13516 | - | no-squashfs-chunk |
| be-trunc-half-resized | trunc_half_resized | {squashfs_v4_be} | {extractor-failure} | {} | yes | no | 0 | partial | 13516 vs 13516 | 0:squashfs_v4_be | body-extractor-failure |
| be-trunc-minus1 | trunc_minus1 | {} | {} | {} | n/a | no | 0 | complete | 27033 vs 27032 | - | no-squashfs-chunk |
| be-trunc-quarter | trunc_quarter | {} | {} | {} | n/a | no | 0 | complete | 27033 vs 6758 | - | no-squashfs-chunk |
| be-xz-prefix4k | prefix4k | {squashfs_v4_be} | {unknown-chunk-handler} | {} | n/a | no | 7 | partial | - | 0:None,4096:squashfs_v4_be | garbage-prefix-or-tail |
| be-xz-trunc-half | trunc_half | {} | {} | {} | n/a | no | 0 | complete | 27033 vs 13516 | - | no-squashfs-chunk |
| garbage-control | xorshift(0xBADC0DE,4096) | {} | {} | {} | n/a | no | 0 | complete | - | - | no-squashfs-chunk |
| le-base-gzip | base | {squashfs_v4_le} | {} | {} | n/a | no | 6 | complete | 27033 vs 27033 | 0:squashfs_v4_le | clean |
| le-base-xz | base | {squashfs_v4_le} | {} | {} | n/a | no | 6 | complete | 27033 vs 27033 | 0:squashfs_v4_le | clean |
| le-oversize-x2 | oversize_x2 | {} | {} | {} | n/a | no | 0 | complete | 54066 vs 27033 | - | no-squashfs-chunk |
| le-prefix4k | prefix4k | {squashfs_v4_le} | {unknown-chunk-handler} | {} | n/a | no | 7 | partial | - | 0:None,4096:squashfs_v4_le | garbage-prefix-or-tail |
| le-prefix4k-trunc | prefix4k_trunc | {} | {} | {} | n/a | no | 0 | complete | - | - | no-squashfs-chunk |
| le-trunc-half | trunc_half | {} | {} | {} | n/a | no | 0 | complete | 27033 vs 13516 | - | no-squashfs-chunk |
