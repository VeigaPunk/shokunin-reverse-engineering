#!/usr/bin/env python3
"""Make an AVM-marked copy of a big-endian SquashFS v4 image.

Documented byte offsets (SquashFS v4 superblock, big-endian, 96 bytes):
  0   magic[4]            "sqsh"
  4   inodes              u32
  8   mkfs_time           u32   <-- patched to bytes_used
  12  block_size          u32
  16  fragments           u32
  20  compression         u16
  22  block_log           u16
  24  flags               u16
  26  no_ids              u16
  28  s_major             u16
  30  s_minor             u16
  32  root_inode          u64
  40  bytes_used          u64   <-- source of the marker value (read only)
  48  id_table_start      u64
  56  xattr_id_table_start u64
  64  inode_table_start   u64
  72  directory_table_start u64
  80  fragment_table_start u64
  88  lookup_table_start  u64

The marker copy differs from the input only at offsets 8..11.
usable only when bytes_used < 2**32 (mkfs_time is u32, bytes_used u64).

Usage: make-avm-copy.py SRC DST
"""
import struct
import sys

HDR = '>4sIIIIHHHHHHQQQQQQQQ'  # 96 bytes, matches unblob's squashfs4_super_block_t


def main(src, dst):
    b = bytearray(open(src, 'rb').read())
    if len(b) < 96:
        sys.exit(f'{src}: shorter than a v4 superblock')
    f = struct.unpack(HDR, bytes(b[:96]))
    if f[0] != b'sqsh':
        sys.exit(f'{src}: magic {f[0]!r}, not BE v4 ("sqsh")')
    bytes_used = f[12]
    if bytes_used >= 2 ** 32:
        sys.exit(f'{src}: bytes_used {bytes_used} does not fit mkfs_time u32')
    b[8:12] = struct.pack('>I', bytes_used)
    open(dst, 'wb').write(bytes(b))
    f2 = struct.unpack(HDR, bytes(b[:96]))
    print(f'{dst}: mkfs_time={f2[2]} bytes_used={f2[12]} equal={f2[2] == f2[12]}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
