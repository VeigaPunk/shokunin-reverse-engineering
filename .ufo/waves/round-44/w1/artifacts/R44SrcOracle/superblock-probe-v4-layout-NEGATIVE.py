#!/usr/bin/env python3
"""Read-only superblock probe for the four frozen carriers (pre-freeze oracle evidence).

Reports endianness from the magic byte order, s_major/s_minor, compression id, flags and
block_size, so the C1 counter's frozen probe can be checked against an independent read.
No writes outside stdout.
"""
import struct
import sys

FIX = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-42/c2/fixtures"
CARRIERS = [
    ("V1LE", "v1-le--squashfs_v1.0_le.bin", "squashfs_v1", "le"),
    ("V1BE", "v1-be--squashfs_v1.0_be.bin", "squashfs_v1", "be"),
    ("V2LE", "v2-le--squashfs_v2.0_le.bin", "squashfs_v2", "le"),
    ("V2BE", "v2-be--squashfs_v2.0_be.bin", "squashfs_v2", "be"),
]
MAGIC_LE = b"hsqs"
MAGIC_BE = b"sqsh"
COMP = {1: "gzip", 2: "lzma", 3: "lzo", 4: "xz", 5: "lz4", 6: "zstd"}
# squashfs_super_block (1.x/2.x): 80 bytes, same field order as 2.x
FIELDS = [
    ("magic", "4s"), ("inodes", "I"), ("mkfs_time", "I"), ("block_size", "I"),
    ("fragments", "I"), ("compression", "H"), ("block_log", "H"), ("flags", "H"),
    ("no_ids", "H"), ("s_major", "H"), ("s_minor", "H"), ("root_inode", "Q"),
    ("bytes_used", "Q"), ("id_table_start", "Q"), ("xattr_id_table_start", "Q"),
    ("inode_table_start", "Q"), ("directory_table_start", "Q"),
]
FMT = "".join(t for _, t in FIELDS)


def main():
    bad = 0
    print(f"superblock struct size={struct.calcsize(FMT)} bytes fields={len(FIELDS)}")
    for cid, fname, handler, endian in CARRIERS:
        raw = open(f"{FIX}/{fname}", "rb").read()
        magic = raw[:4]
        detected = "le" if magic == MAGIC_LE else ("be" if magic == MAGIC_BE else "?")
        order = "<" if detected == "le" else ">"
        vals = dict(zip([n for n, _ in FIELDS], struct.unpack(order + FMT, raw[: struct.calcsize(FMT)])))
        comp = vals["compression"]
        flag_unc = bool(vals["flags"] & 0x0002)  # SQUASHFS_NOF? report raw flags instead
        ok = (
            detected == endian
            and vals["s_major"] == int(handler[-1])
            and vals["s_minor"] == 0
            and vals["magic"] in (MAGIC_LE, MAGIC_BE)
        )
        bad += 0 if ok else 1
        print(
            f"{cid} {handler} {fname}\n"
            f"  magic_bytes={magic!r} detected_endian={detected} frozen_endian={endian} "
            f"{'OK' if detected == endian else 'MISMATCH'}\n"
            f"  s_major={vals['s_major']} s_minor={vals['s_minor']} "
            f"compression_id={comp} ({COMP.get(comp, 'unknown')}) flags=0x{vals['flags']:04x} "
            f"flag_bit1={int(bool(vals['flags'] & 0x2))}\n"
            f"  block_size={vals['block_size']} block_log={vals['block_log']} "
            f"inodes={vals['inodes']} fragments={vals['fragments']} no_ids={vals['no_ids']}\n"
            f"  bytes_used={vals['bytes_used']} file_size={len(raw)} "
            f"root_inode={vals['root_inode']}\n"
            f"  bind_ok={ok}"
        )
    print(f"superblock_bind_failures={bad}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
