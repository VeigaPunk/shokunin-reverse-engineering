#!/usr/bin/env python3
"""R39-C2 recon probe: the five body-corruption variants tried on dev carriers.

NOT the deliverable recipe (that is corrupt.py `corrupt()`); this module exists so
the run-matrix in this directory can be reproduced variant by variant.  Every
offset is derived from the v4 BE superblock fields (see corrupt.py docstring).

Measured outcome (see run-matrix.json, three trees ta/tb/tc, gzip BE):
  v1 zero id table          exit 1, 0 files published  -- stable, RECOMMENDED
  v2 zero first data block  exit 0 on ta, exit 1 with partial files on tb/tc
  v3 flip inode table       exit 1, 0 files published  -- stable, runner-up
  v4 zero directory table   exit 1, 0 files published  -- stable, runner-up
  v5 corrupt block length   SIGSEGV (139), partial files on disk
"""
import struct

SB_SIZE = 96


def _u32(b, off):
    return struct.unpack_from(">I", b, off)[0]


def _u64(b, off):
    return struct.unpack_from(">Q", b, off)[0]


def _meta(b, table_start, block_off):
    """(payload_offset, header, size) of the metadata block `block_off` into a table."""
    abs_ = table_start + block_off
    hdr = struct.unpack_from(">H", b, abs_)[0]
    return abs_ + 2, hdr, hdr & 0x7FFF


def first_file_inode(b):
    """Walk root dir -> first regular file; return (file_inode_offset, start_block, file_size)."""
    itab, dtab = _u64(b, 64), _u64(b, 72)
    ref = _u64(b, 32)
    ipay, _, _ = _meta(b, itab, ref >> 16)
    ino = ipay + (ref & 0xFFFF)
    dblk = _u32(b, ino + 16)
    foff = struct.unpack_from(">H", b, ino + 26)[0]
    dpay, _, _ = _meta(b, dtab, dblk)
    p = dpay + foff
    count = _u32(b, p) + 1
    first_iblk = _u32(b, p + 4)
    first_ino = _u32(b, p + 8)
    p += 12
    for _ in range(count):
        e_off, delta, typ, nsz = struct.unpack_from(">HhHH", b, p)
        p += 8 + nsz + 1
        if typ == 2:  # regular file
            fpay, _, _ = _meta(b, itab, first_iblk)
            f = fpay + e_off
            return f, _u32(b, f + 16), _u32(b, f + 28)
    raise ValueError("no regular file in root dir")


def v_zero_id_table(b):
    b = bytes(b)
    lookup = _u64(b, 48)
    id_meta = _u64(b, lookup)
    out = bytearray(b)
    out[id_meta:id_meta + 6] = b"\x00" * 6
    return bytes(out)


def v_zero_first_data_block(b):
    b = bytes(b)
    _, data_start, file_size = first_file_inode(b)
    out = bytearray(b)
    n = min(16, file_size)
    out[data_start:data_start + n] = b"\x00" * n
    return bytes(out)


def v_flip_inode_table(b):
    b = bytes(b)
    pos = _u64(b, 64) + 2  # first payload byte = MSB of the first inode's u16 type
    out = bytearray(b)
    out[pos] ^= 0xFF
    return bytes(out)


def v_zero_directory_table(b):
    b = bytes(b)
    pos = _u64(b, 72)
    out = bytearray(b)
    out[pos:pos + 4] = b"\x00" * 4
    return bytes(out)


def v_corrupt_block_length(b):
    b = bytes(b)
    f, _, _ = first_file_inode(b)
    pos = f + 32  # first u32 block size, right after basic header + file header
    out = bytearray(b)
    struct.pack_into(">I", out, pos, 2)
    return bytes(out)


VARIANTS = {
    "v1-zero-id-table": v_zero_id_table,
    "v2-zero-first-data-block": v_zero_first_data_block,
    "v3-flip-inode-table": v_flip_inode_table,
    "v4-zero-directory-table": v_zero_directory_table,
    "v5-corrupt-block-length": v_corrupt_block_length,
}
