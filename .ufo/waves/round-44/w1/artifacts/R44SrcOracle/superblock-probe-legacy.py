#!/usr/bin/env python3
"""Read-only superblock probe for the four frozen C1 carriers (legacy 1.x/2.x layout).

Layout authority: squashfs-tools 4.7.5 `squashfs-tools/squashfs_compat.h:38-64`
(`struct squashfs_super_block_3`, `__attribute__((packed))`): magic, inodes, bytes_used_2,
uid_start_2, guid_start_2, inode_table_start_2, directory_table_start_2, then s_major:16,
s_minor:16, block_size_1:16, block_log:16, flags:8, no_uids:8, no_guids:8, mkfs_time (i32,
un-aligned at byte 39), root_inode.  Flag bits: squashfs-tools 4.7.5 `squashfs_fs.h:64-79`
(SQUASHFS_NOD=1 = uncompressed data, SQUASHFS_NOF=3, SQUASHFS_DUPLICATE=6, SQUASHFS_EXPORT=7).

`expected` values below are transcribed from `/usr/bin/unsquashfs -s` (4.7.5) on the same
bytes, so the probe is a cross-check of a hand read against the independent reader.

`file(1)` is deliberately NOT used as a field authority: its compressed/uncompressed token for
legacy images comes from byte 20 (the v4 compression slot = legacy inode_table_start_2); see
the flip receipt.
"""
import datetime
import struct
import sys

FIX = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-42/c2/fixtures"
CARRIERS = [
    # id, file, handler, endian, expected (endian, major, minor, block_size, flags, uids, gids,
    #                                     inodes, bytes_used, mkfs_time)
    ("V1LE", "v1-le--squashfs_v1.0_le.bin", "squashfs_v1", "le", ("le", 1, 0, 32768, 0x00, 1, 0, 4, 176, 1722842331)),
    ("V1BE", "v1-be--squashfs_v1.0_be.bin", "squashfs_v1", "be", ("be", 1, 0, 32768, 0x00, 1, 0, 4, 177, 1722842338)),
    ("V2LE", "v2-le--squashfs_v2.0_le.bin", "squashfs_v2", "le", ("le", 2, 0, 65536, 0x40, 1, 0, 5, 196, 1678381552)),
    ("V2BE", "v2-be--squashfs_v2.0_be.bin", "squashfs_v2", "be", ("be", 2, 0, 65536, 0x40, 1, 0, 5, 201, 1678381590)),
]
SQUASHFS_NOD = 1        # uncompressed data
SQUASHFS_NOF = 3        # uncompressed fragments
SQUASHFS_DUPLICATE = 6  # duplicate checking on
SQUASHFS_EXPORT = 7


def main():
    bad = 0
    for cid, fname, handler, endian, exp in CARRIERS:
        raw = open(f"{FIX}/{fname}", "rb").read()
        magic = raw[:4]
        detected = "le" if magic == b"hsqs" else ("be" if magic == b"sqsh" else "?")
        o = "<" if detected == "le" else ">"
        u16 = lambda off: struct.unpack(o + "H", raw[off:off + 2])[0]  # noqa: E731
        u32 = lambda off: struct.unpack(o + "I", raw[off:off + 4])[0]  # noqa: E731
        got = (
            detected,
            u16(28),
            u16(30),
            2 ** u16(34) if u16(32) == 0 else u16(32),
            raw[36],
            raw[37],
            raw[38],
            u32(4),
            u32(8),
            struct.unpack(o + "i", raw[39:43])[0],
        )
        ok = got == exp
        bad += 0 if ok else 1
        flags = got[4]
        print(f"{cid} {handler} {fname}")
        print(f"  magic={magic!r} endian={detected} (frozen {endian})")
        print(f"  s_major={got[1]} s_minor={got[2]} block_size={got[3]} "
              f"block_size_1_raw={u16(32)} block_log={u16(34)}")
        print(f"  flags=0x{flags:02x} uncompressed_data={int(bool((flags >> SQUASHFS_NOD) & 1))} "
              f"uncompressed_fragments={int(bool((flags >> SQUASHFS_NOF) & 1))} "
              f"duplicates={int(bool((flags >> SQUASHFS_DUPLICATE) & 1))} "
              f"exportable={int(bool((flags >> SQUASHFS_EXPORT) & 1))}")
        print(f"  no_uids={got[5]} no_guids={got[6]} inodes={got[7]} bytes_used={got[8]} "
              f"file_size={len(raw)}")
        print(f"  mkfs_time={got[9]} "
              f"({datetime.datetime.fromtimestamp(got[9], datetime.UTC).isoformat()})")
        print(f"  matches_unsquashfs_s={ok}")
        if not ok:
            print(f"  expected={exp}")
            print(f"  got     ={got}")
    print(f"superblock_probe_failures={bad}")
    print("note: compression_id does not exist in the 1.x/2.x superblock; "
          "compression state is the flags word, and no carrier sets uncompressed_data")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
