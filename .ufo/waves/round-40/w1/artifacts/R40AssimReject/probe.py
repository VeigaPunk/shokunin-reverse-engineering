#!/usr/bin/env python3
"""Pure-stdlib SquashFS v4 superblock + first-metadata-block probe (no unblob, no sasquatch).

Reports, per file:
  - magic ('sqsh' = big-endian superblock, 'hsqs' = little-endian superblock)
  - mkfs_time, bytes_used and the AVM marker test (mkfs_time == bytes_used)
  - the 2-byte metadata block-length header at inode_table_start decoded both ways,
    and which way satisfies the exact identity  len + 2 + inode_table_start == dir_table_start
    (holds for single-metadata-block images, e.g. the 4096-byte lane fixtures)

Usage: python3 probe.py FILE [FILE ...]
"""
import struct
import sys


def probe(path: str) -> int:
    data = open(path, "rb").read()
    if len(data) < 96:
        print(f"{path}: too short ({len(data)} B)")
        return 1
    magic = data[:4]
    if magic not in (b"sqsh", b"hsqs"):
        print(f"{path}: magic {magic!r} is not sqsh/hsqs")
        return 1
    be = magic == b"sqsh"
    e = ">" if be else "<"
    inodes, mkfs, block_size, fragments = struct.unpack(e + "IIII", data[4:20])
    comp, block_log, flags, no_ids, s_major, s_minor = struct.unpack(e + "HHHHHH", data[20:32])
    (root_inode, bytes_used, id_table_start, xattr_table_start,
     inode_table_start, dir_table_start, frag_table_start,
     export_table_start) = struct.unpack(e + "QQQQQQQQ", data[32:96])

    marker = mkfs == bytes_used
    hdr = data[inode_table_start:inode_table_start + 2]
    le = struct.unpack("<H", hdr)[0] if len(hdr) == 2 else None
    bev = struct.unpack(">H", hdr)[0] if len(hdr) == 2 else None
    identity_le = le is not None and le + 2 + inode_table_start == dir_table_start
    identity_be = bev is not None and bev + 2 + inode_table_start == dir_table_start

    print(f"file                     {path}")
    print(f"  encrypted?             {'yes' if flags & 0x0800 else 'no'}  (flags=0x{flags:04x})")
    print(f"  magic                  {magic.decode()}  ({'BE superblock' if be else 'LE superblock'})")
    print(f"  version                {s_major}.{s_minor}   compression id {comp}   block_size {block_size}")
    print(f"  inodes                 {inodes}")
    print(f"  mkfs_time              {mkfs}      bytes_used {bytes_used}")
    print(f"  AVM marker             {'SET (mkfs_time == bytes_used)' if marker else 'not set'}")
    print(f"  first metadata header  at inode_table_start={inode_table_start}: {hdr.hex()}  "
          f"LE={le} BE={bev}")
    print(f"  length endianness      "
          f"{'LE' if identity_le else ('BE' if identity_be else 'undetermined (multi-block inode table)')}"
          f"   [identity len+2+inode_table_start == dir_table_start={dir_table_start}: "
          f"LE {identity_le}, BE {identity_be}]")
    print(f"  tables                 inode {inode_table_start}  dir {dir_table_start}  "
          f"frag {frag_table_start}  export {export_table_start}  id {id_table_start}  xattr {xattr_table_start}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__.strip().splitlines()[-1])
        sys.exit(2)
    rc = 0
    for p in sys.argv[1:]:
        rc |= probe(p)
    sys.exit(rc)
