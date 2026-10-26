#!/usr/bin/env python3
"""Decisive endianness check of the 2-byte metadata block-length headers (independent, stdlib only).

For each lane-built carrier: read the BE superblock, then walk the inode table and the directory
table as a sequence of metadata blocks. A SquashFS metadata block is a u16 header (0x8000 = stored
uncompressed, low 15 bits = stored size) followed by that many bytes. We test both orders: the one
that decodes every block to <= block_size bytes and terminates exactly at the next table start wins.
"""
import gzip
import lzma
import struct
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'


def sb(path):
    with open(path, 'rb') as fh:
        b = fh.read(96)
    v = struct.unpack('>IIIIIHHHHHHQQQQQQQQ', b)
    names = ('magic inodes mkfs_time block_size fragments compression block_log flags no_ids '
             's_major s_minor root_inode bytes_used id_table_start xattr_id_table_start '
             'inode_table_start directory_table_start fragment_table_start lookup_table_start').split()
    return dict(zip(names, v))


def decode(data, comp):
    if comp == 1:            # gzip
        return gzip.decompress(data)
    if comp == 4:            # xz
        return lzma.decompress(data)
    raise SystemExit('unsupported compression %d' % comp)


def walk(path, start, end, comp, order):
    """Return (ok, blocks, total_out, error)."""
    out = 0
    pos = start
    n = 0
    with open(path, 'rb') as fh:
        while pos < end:
            fh.seek(pos)
            hdr = fh.read(2)
            if len(hdr) != 2:
                return False, n, out, 'short header'
            raw = struct.unpack(order + 'H', hdr)[0]
            size = raw & 0x7FFF
            uncompressed = bool(raw & 0x8000)
            if size == 0:
                return False, n, out, 'zero size'
            body = fh.read(size)
            if len(body) != size:
                return False, n, out, 'short body'
            if uncompressed:
                plain = body
            else:
                try:
                    plain = decode(body, comp)
                except Exception as exc:
                    return False, n, out, 'decode: %s' % str(exc)[:60]
            if len(plain) > 8192:
                return False, n, out, 'block decodes to %d bytes' % len(plain)
            out += len(plain)
            pos += 2 + size
            n += 1
    return (pos == end), n, out, None if pos == end else 'overran by %d' % (pos - end)


for cid in ('L1', 'L2'):
    p = '%s/corpus/evidence/round-40/c1/%s/carrier.sqsh' % (LANE, cid)
    s = sb(p)
    print('=' * 70)
    print('%s magic=%r s=%d.%d comp=%d block_size=%d bytes_used=%d mkfs_time=%d marker=%s'
          % (cid, struct.pack('>I', s['magic']), s['s_major'], s['s_minor'], s['compression'],
             s['block_size'], s['bytes_used'], s['mkfs_time'],
             s['mkfs_time'] == s['bytes_used']))
    for label, a, b in (('inode_table', s['inode_table_start'], s['directory_table_start']),
                        ('directory_table', s['directory_table_start'], s['id_table_start'])):
        for order in ('<', '>'):
            ok, n, out, err = walk(p, a, b, s['compression'], order)
            print('  %-16s region=[%d,%d) order=%s -> ok=%s blocks=%d out_bytes=%d %s'
                  % (label, a, b, 'LE' if order == '<' else 'BE', ok, n, out,
                     '' if err is None else 'err=%s' % err))
