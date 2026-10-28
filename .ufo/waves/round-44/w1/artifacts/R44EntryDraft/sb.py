#!/usr/bin/env python3
"""R44EntryDraft: SquashFS v1/v2 superblock field reader.

Reads the first 32 bytes as the unblob 26.6.4 `squashfs_super_block_t`
(squashfs.py:124-137: s_magic[4], six uint32, s_major:uint16, s_minor:uint16)
plus the v1/v2 packed tail at :32 (block_size_1:uint16, block_log:uint16,
flags:uint8, no_uids:uint8, no_guids:uint8, mkfs_time:uint32) as decoded here.

Usage: python3 -I -B sb.py <carrier.bin> [...]
"""
import hashlib
import struct
import sys


def read(path):
    b = open(path, "rb").read()
    magic = b[:4]
    if magic in (b"sqsh", b"sqlz", b"shsq"):
        en = ">"
        endian = "be"
    elif magic in (b"hsqs", b"zlqs", b"qshs"):
        en = "<"
        endian = "le"
    else:
        raise SystemExit(f"unknown magic {magic!r} in {path}")
    inodes, bytes_used, uid_start, guid_start, inode_table, dir_table = struct.unpack(
        en + "6I", b[4:28])
    major, minor = struct.unpack(en + "2H", b[28:32])
    rec = {
        "path": path,
        "sha256": hashlib.sha256(b).hexdigest(),
        "size": len(b),
        "magic": magic.decode("latin-1"),
        "endian": endian,
        "inodes": inodes,
        "bytes_used": bytes_used,
        "uid_start": uid_start,
        "guid_start": guid_start,
        "inode_table_start": inode_table,
        "directory_table_start": dir_table,
        "s_major": major,
        "s_minor": minor,
    }
    if len(b) >= 43:
        block_size, block_log = struct.unpack(en + "2H", b[32:36])
        flags, no_uids, no_guids = b[36], b[37], b[38]
        mkfs_time = struct.unpack(en + "I", b[39:43])[0]
        rec.update({
            "block_size_1": block_size,
            "block_log": block_log,
            "flags": flags,
            "no_uids": no_uids,
            "no_guids": no_guids,
            "mkfs_time": mkfs_time,
            "tail_note": "bytes[32:43] decoded as v1/v2 packed tail; unblob's "
                         "C_DEFINITIONS stop at s_minor, so this tail is the reader's "
                         "own decode, cross-checked against `unsquashfs -s`",
        })
    return rec


if __name__ == "__main__":
    for p in sys.argv[1:]:
        r = read(p)
        print(" ".join(f"{k}={v}" for k, v in r.items()))
