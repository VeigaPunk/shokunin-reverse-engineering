#!/usr/bin/env python3
"""Metadata-block chain test for SquashFS v4 superblocks (kaidoku R40-C1 critique).

The AVM layout differs from standard big-endian SquashFS v4 in exactly one field
class: every 2-byte metadata block-length header is stored little-endian while the
superblock stays big-endian (Freetz). A *first-header* plausibility test is not
sound (both readings can be plausible); walking the whole header chain of every
metadata table and requiring it to land exactly on the next table's start is
decisive.

Metadata blocks are always 8 KiB (SQUASHFS_METADATA_SIZE), independent of the
superblock's data block_size, so a header value outside (0, 8192] is impossible
under any reading.

Usage: meta-chain.py IMAGE [IMAGE...]   (pure stdlib, read-only)
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


def superblock(buf):
    magic = buf[:4]
    order = {b'hsqs': '<', b'sqsh': '>'}.get(magic)
    if order is None:
        raise SystemExit('bad magic %r' % magic)
    f = dict(zip(SB_FIELDS, struct.unpack_from(order + SB_FMT, buf, 0)))
    f['_order'] = order
    f['_endian'] = 'little' if order == '<' else 'big'
    return f


def walk(buf, start, end, order):
    """Walk 2-byte metadata headers from start to end; return (blocks, landed, lens)."""
    pos, lens = start, []
    while pos < end:
        if pos + 2 > len(buf) or len(lens) > 100000:
            return len(lens), None, lens
        raw = struct.unpack_from(order + 'H', buf, pos)[0]
        n = raw & 0x7FFF
        lens.append((raw, n, bool(raw & 0x8000)))
        if n == 0 or n > METADATA_SIZE:
            return len(lens) + 1, None, lens      # impossible header: chain dead
        pos += 2 + n
        if pos == end:
            return len(lens), True, lens
        if pos > end:
            return len(lens), False, lens
    return len(lens), pos == end, lens


def tables(f):
    """(name, start, next-name, next-start) for each table whose end is a table start."""
    ref = f['lookup_table_start'] if f['lookup_table_start'] != INVALID64 else f['id_table_start']
    # Only the two adjacent chains: the fragment and id tables are reached
    # through a u64 index of pointers, not by walking on from fragment_table_start.
    rows = [
        ('inode_table_start', f['inode_table_start'], 'directory_table_start', f['directory_table_start']),
        ('directory_table_start', f['directory_table_start'], 'fragment_table_start', f['fragment_table_start']),
    ]
    out = []
    for name, start, nxt, end in rows:
        if start == INVALID64 or end == INVALID64:
            continue
        if not (0 <= start < end <= f['bytes_used']):
            continue
        out.append((name, start, nxt, end))
    return out


def report(path):
    buf = open(path, 'rb').read()
    f = superblock(buf)
    rows = tables(f)
    print('== %s  magic=%s comp=%d block_size=%d marker=%s bytes_used=%d'
          % (path.rsplit('/', 1)[-1], buf[:4].decode('latin1'), f['compression'],
             f['block_size'], 'YES' if f['mkfs_time'] == f['bytes_used'] else 'no',
             f['bytes_used']))
    lands = {}
    for name, start, nxt, end in rows:
        for order, label in (('<', 'LE'), ('>', 'BE')):
            blocks, landed, lens = walk(buf, start, end, order)
            lands.setdefault(label, []).append(landed)
            print('  %-22s -> %-24s %s: blocks=%d landed_exactly=%s first_len=%d (%s)'
                  % (name, nxt, label, blocks, landed,
                     lens[0][1] if lens else -1, 'uncomp' if lens and lens[0][2] else 'comp'))
    if rows:
        _, s0, _, _ = rows[0]
        le = struct.unpack_from('<H', buf, s0)[0] & 0x7FFF
        be = struct.unpack_from('>H', buf, s0)[0] & 0x7FFF
        ok = lambda v: 0 < v <= METADATA_SIZE
        verdict = ('AMBIGUOUS(both plausible)' if ok(le) and ok(be)
                   else ('LE' if ok(le) else 'BE'))
        print('  first inode-table length: LE=%d %s | BE=%d %s -> first-length-only verdict: %s'
              % (le, 'plausible' if ok(le) else 'impossible',
                 be, 'plausible' if ok(be) else 'impossible', verdict))
        print('  chain decisive: LE lands on every table=%s | BE lands on every table=%s'
              % (all(lands['LE']) if lands.get('LE') else None,
                 all(lands['BE']) if lands.get('BE') else None))


for path in sys.argv[1:]:
    report(path)
