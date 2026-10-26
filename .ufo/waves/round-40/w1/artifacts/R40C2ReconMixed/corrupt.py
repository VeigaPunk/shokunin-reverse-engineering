#!/usr/bin/env python3
"""corrupt.py -- development-only SquashFS body damage, endianness-aware.

Two corruptions, mirroring the round-39 heldout recipes but re-implemented here:

  zero-id-table  zero the id-table metadata block (header + payload) -> sasquatch
                 fails reading the id table (the v1 ``body-extractor-failure``
                 recipe)
  bad-minor      s_minor 4 -> 5; the v4 pattern pins s_major, so the handler still
                 runs and sasquatch rejects the header -> ``extractor-failure``
  flip-data-tail XOR 0xff over 16 bytes ending at inode_table_start, i.e. inside the
                 last data block, leaving the inode/dir/id tables intact
  zero-first-data zero the first 16 bytes of the first data block (round-39
                 probe-variants v2, which yields a partial body failure)

Usage: python3 -I -B corrupt.py IN OUT zero-id-table|bad-minor
Exit 0 ok, 2 on an unusable input.
"""
import struct
import sys


def _prefix(endian):
    return '>' if endian in ('be', 'avm') else '<'


def zero_id_table(payload, endian):
    prefix = _prefix(endian)
    id_table_start = struct.unpack(prefix + 'Q', bytes(payload[48:56]))[0]
    if not 96 <= id_table_start <= len(payload) - 8:
        raise SystemExit('id_table_start %d outside image (%d bytes)'
                         % (id_table_start, len(payload)))
    id_meta_start = struct.unpack(
        prefix + 'Q', bytes(payload[id_table_start:id_table_start + 8]))[0]
    if not 96 <= id_meta_start < id_table_start <= len(payload):
        raise SystemExit('id metadata block %d..%d outside image'
                         % (id_meta_start, id_table_start))
    payload[id_meta_start:id_table_start] = bytes(id_table_start - id_meta_start)
    return payload


def bad_minor(payload, endian):
    prefix = _prefix(endian)
    major, minor = struct.unpack(prefix + 'HH', bytes(payload[28:32]))
    if (major, minor) != (4, 0):
        raise SystemExit('unexpected squashfs version %d.%d' % (major, minor))
    payload[28:32] = struct.pack(prefix + 'HH', 4, 5)
    return payload


def flip_data_tail(payload, endian):
    prefix = _prefix(endian)
    inode_table_start = struct.unpack(prefix + 'Q', bytes(payload[40:48]))[0]
    if not 112 <= inode_table_start <= len(payload):
        raise SystemExit('inode_table_start %d outside image (%d bytes)'
                         % (inode_table_start, len(payload)))
    start = inode_table_start - 16
    for i in range(start, inode_table_start):
        payload[i] ^= 0xFF
    return payload


def zero_first_data(payload, endian):
    """Zero the first 16 bytes of the first file's first data block.

    gen-squashfs.py writes the data region immediately after the 96-byte
    superblock, so the first data block starts at offset 96.
    """
    if len(payload) < 112:
        raise SystemExit('image too short for a data block')
    payload[96:112] = bytes(16)
    return payload


CORRUPTIONS = {'zero-id-table': zero_id_table, 'bad-minor': bad_minor,
               'flip-data-tail': flip_data_tail, 'zero-first-data': zero_first_data}


def main(argv):
    if len(argv) != 4 or argv[3] not in CORRUPTIONS:
        raise SystemExit(__doc__.strip().splitlines()[-1])
    src, dst, kind = argv[1], argv[2], argv[3]
    with open(src, 'rb') as fh:
        payload = bytearray(fh.read())
    magic = bytes(payload[:4])
    endian = 'le' if magic == b'hsqs' else 'be' if magic == b'sqsh' else None
    if endian is None:
        raise SystemExit('unknown magic %r' % magic)
    payload = CORRUPTIONS[kind](payload, endian)
    with open(dst, 'wb') as fh:
        fh.write(bytes(payload))
    print('corrupted', src, '->', dst, kind, endian, len(payload))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
