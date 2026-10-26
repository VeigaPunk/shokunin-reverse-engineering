#!/usr/bin/env python3
"""R39-C2 dev-corruption recipe: deterministic standard-BE SquashFS v4 body damage.

Recommended recipe (v1, "zero the id table"):

    from corrupt import corrupt
    damaged = corrupt(open('clean-be-gzip.sqsh', 'rb').read())

`corrupt()` destroys the id metadata block that the superblock's `id_table_start`
lookup table points at.  unblob still carves a valid `squashfs_v4_be` chunk
(chunk geometry comes only from the superblock header and padding) and still
runs `sasquatch-v4be -be -no-exit-code -f -d <out> <in>`, because the `-be`
token is decided by `bytes_used != mkfs_time` in unblob 26.6.4
(`unblob/handlers/filesystem/squashfs.py`, `SquashFSExtractor.extract`).
sasquatch then aborts in `read_id_table` before writing any file.

Every offset is derived from superblock fields (v4 BE, offsets per unblob's
`SquashFSv4LEHandler.C_DEFINITIONS`); nothing is hardcoded relative to a
particular tree.  Superblock: magic[4] inodes@4 mkfs_time@8 block_size@12
fragments@16 compression@20 block_log@22 flags@24 no_ids@26 major@28 minor@30
root_inode@32 bytes_used@40 id_table_start@48 xattr_id_table_start@56
inode_table_start@64 directory_table_start@72 fragment_table_start@80
lookup_table_start@88 (96 bytes total).
"""
import struct

SB_SIZE = 96
MAGIC_BE = b"sqsh"
ZERO_BYTES = 6  # v4 id metadata block header (u16, 0x8000|size) + the single u32 id


def _u32(b, off):
    return struct.unpack_from(">I", b, off)[0]


def _u64(b, off):
    return struct.unpack_from(">Q", b, off)[0]


def corrupt(image_bytes: bytes) -> bytes:
    """Return a copy of a standard-BE SquashFS v4 image with its id table zeroed.

    Raises ValueError when the input is not a standard big-endian v4 image, when
    the id table geometry cannot be resolved inside the image, or when the image
    is AVM-shaped (bytes_used == mkfs_time, for which unblob drops `-be`).
    """
    b = bytes(image_bytes)
    if len(b) < SB_SIZE:
        raise ValueError("shorter than a SquashFS v4 superblock")
    if b[0:4] != MAGIC_BE:
        raise ValueError("not a standard big-endian SquashFS image (magic %r)" % b[0:4])
    major, minor = struct.unpack_from(">HH", b, 28)
    if (major, minor) != (4, 0):
        raise ValueError("not SquashFS v4.0 (version %d.%d)" % (major, minor))

    bytes_used = _u64(b, 40)
    mkfs_time = _u32(b, 8)
    if bytes_used == mkfs_time:
        raise ValueError("AVM-shaped header (bytes_used == mkfs_time): unblob drops -be")

    id_table_start = _u64(b, 48)
    # v4 id_table_start points at the id lookup table: an array of u64 metadata
    # block offsets, one per 2048 ids.  no_ids == 1 in every image built by
    # tools/round-37/gen-squashfs.py, so the first entry is the whole table.
    if id_table_start + 8 > len(b):
        raise ValueError("id_table_start %d outside image (%d bytes)" % (id_table_start, len(b)))
    id_meta_start = _u64(b, id_table_start)
    if id_meta_start + ZERO_BYTES > len(b) or id_meta_start < SB_SIZE:
        raise ValueError("id metadata block %d outside image body" % id_meta_start)

    out = bytearray(b)
    out[id_meta_start:id_meta_start + ZERO_BYTES] = b"\x00" * ZERO_BYTES
    return bytes(out)


def describe(image_bytes: bytes) -> dict:
    """Offsets the recipe touched, for receipts."""
    b = bytes(image_bytes)
    id_table_start = _u64(b, 48)
    id_meta_start = _u64(b, id_table_start)
    return {
        "id_table_start": id_table_start,
        "id_meta_start": id_meta_start,
        "zeroed": ZERO_BYTES,
        "bytes_used": _u64(b, 40),
        "mkfs_time": _u32(b, 8),
    }
