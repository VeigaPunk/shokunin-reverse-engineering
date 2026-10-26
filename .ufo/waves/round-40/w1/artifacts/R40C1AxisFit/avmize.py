#!/usr/bin/env python3
"""Convert a standard big-endian SquashFS v4 image into the AVM layout.

AVM layouts differ from standard BE v4 in exactly one field class: every 2-byte
metadata block-length header is stored little-endian while the superblock stays
big-endian (Freetz). A header occupies the same 2 bytes under either encoding,
so the transform is a byte swap at each header position: no offset moves and no
payload byte changes.

Header positions come from the big-endian metadata chains (inode table, then
directory table, then any metadata block named by the fragment/id table index).
Optionally set the AVM marker `mkfs_time == bytes_used` (unblob 26.6.4's
squashfs_v4_be handler drops `-be` exactly when it holds).

Usage: avmize.py IN.sqsh OUT.sqsh [--marker|--no-marker]
Exit: 0 converted; 2 input could not be walked.
"""
import struct
import sys

SB_FMT = 'IIIIIHHHHHHQQQQQQQQ'
SB_FIELDS = ('magic', 'inodes', 'mkfs_time', 'block_size', 'fragments',
             'compression', 'block_log', 'flags', 'no_ids', 's_major',
             's_minor', 'root_inode', 'bytes_used', 'id_table_start',
             'xattr_id_table_start', 'inode_table_start',
             'directory_table_start', 'fragment_table_start',
             'lookup_table_start')
INVALID64 = 0xFFFFFFFFFFFFFFFF
METADATA_SIZE = 8192


def swap_header(buf, pos):
    raw = struct.unpack_from('>H', buf, pos)[0]
    n = raw & 0x7FFF
    if n == 0 or n > METADATA_SIZE:
        return None
    struct.pack_into('<H', buf, pos, raw)
    return n


def main():
    plain = [a for a in sys.argv[1:] if not a.startswith('--')]
    src, dst = plain[0], plain[1]
    buf = bytearray(open(src, 'rb').read())
    if buf[:4] != b'sqsh':
        raise SystemExit('not a big-endian v4 image: magic %r' % bytes(buf[:4]))
    f = dict(zip(SB_FIELDS, struct.unpack_from('>' + SB_FMT, buf, 0)))
    end = f['bytes_used']
    swapped, seen = 0, set()

    # forward chain: inode table, then directory table, then whatever metadata
    # blocks follow (the id table's blocks sit before its index at id_table_start)
    pos = f['inode_table_start']
    while pos + 2 <= end:
        n = swap_header(buf, pos)
        if n is None:
            break
        seen.add(pos)
        swapped += 1
        pos += 2 + n
    if pos > end:
        raise SystemExit('chain overruns bytes_used at %d' % pos)

    # fragment and id tables: index of u64 pointers to metadata blocks
    for count, start, entry in ((f['fragments'], f['fragment_table_start'], 16),
                                (f['no_ids'], f['id_table_start'], 4)):
        if count == 0 or start == INVALID64:
            continue
        nptr = (count * entry + METADATA_SIZE - 1) // METADATA_SIZE
        for i in range(nptr):
            ptr = struct.unpack_from('>Q', buf, start + 8 * i)[0]
            if ptr == INVALID64 or not (0 <= ptr < end) or ptr in seen:
                continue
            if swap_header(buf, ptr) is None:
                raise SystemExit('dead metadata block at index %d ptr %d' % (i, ptr))
            seen.add(ptr)
            swapped += 1

    if '--marker' in sys.argv:
        struct.pack_into('>I', buf, 8, end)
    open(dst, 'wb').write(bytes(buf))
    print('%s -> %s: swapped %d metadata headers%s'
          % (src, dst, swapped,
             ', marker set (mkfs_time=%d)' % end if '--marker' in sys.argv else ''))


main()
