#!/usr/bin/env python3
"""Independent inode metadata-chain walk: headers decoded LE vs BE.

For each carrier, walk the metadata block chain from inode_table_start to
directory_table_start (the inode table), decoding each 2-byte block-length
header both as little-endian and big-endian. A correct decoding terminates
EXACTLY at directory_table_start with every block length in [0, 8192]
(metadata blocks are ≤ 8192 bytes; bit 15 = uncompressed). The wrong
endianness typically overshoots or lands off the boundary.
"""
import os
import struct
import sys

CARRIERS = {
    'V3': '/fast/scratch/hyaku/kaidoku-r41/R41W2C1Oracle/cache/c4f74f54a65e861e22f5d6a47977cdbb3b5345819174f33bc86c63d3d10f872a.bin',
    'V4': '/fast/scratch/hyaku/kaidoku-r41/R41W2C1Oracle/cache/ce27ebca903a1574465ddfa0626943339ce6bc8155f31f88d04049afb570087f.bin',
    'L3': '/fast/scratch/hyaku/kaidoku-r41/R41W2C1Oracle/lcar/L3/carrier.sqsh',
    'L4': '/fast/scratch/hyaku/kaidoku-r41/R41W2C1Oracle/lcar/L4/carrier.sqsh',
}
SB_FMT = 'IIIIIHHHHHHQQQQQQQQ'
SB_FIELDS = ('magic', 'inodes', 'mkfs_time', 'block_size', 'fragments',
             'compression', 'block_log', 'flags', 'no_ids', 's_major',
             's_minor', 'root_inode', 'bytes_used', 'id_table_start',
             'xattr_id_table_start', 'inode_table_start', 'directory_table_start',
             'fragment_table_start', 'lookup_table_start')
META_UNCOMPRESSED = 1 << 15
META_MAX = 8192


def walk(buf, start, end, endian):
    e = '<' if endian == 'le' else '>'
    pos = start
    blocks = []
    lengths = []
    while pos < end:
        if pos + 2 > len(buf):
            return {'ok': False, 'reason': 'truncated header at %d' % pos}
        h = struct.unpack_from(e + 'H', buf, pos)[0]
        length = h & ~META_UNCOMPRESSED
        blocks.append({
            'offset': pos,
            'header_hex': '%04x' % h,
            'length': length,
            'uncompressed': bool(h & META_UNCOMPRESSED),
        })
        lengths.append(length)
        if length > META_MAX:
            return {'ok': False, 'reason': 'length %d > 8192 at %d' % (length, pos)}
        pos += 2 + length
        if len(blocks) > 100000:
            return {'ok': False, 'reason': 'runaway chain'}
    return {
        'ok': pos == end and bool(blocks),
        'blocks': len(blocks),
        'first10': lengths[:10],
        'terminal_pos': pos,
        'end': end,
        'compressed_blocks': sum(1 for b in blocks if not b['uncompressed']),
        'uncompressed_blocks': sum(1 for b in blocks if b['uncompressed']),
    }


def main():
    out = {}
    for cid, path in CARRIERS.items():
        with open(path, 'rb') as fh:
            buf = fh.read()
        vals = struct.unpack_from('>' + SB_FMT, buf, 0)
        sb = dict(zip(SB_FIELDS, vals))
        rec = {
            'size': len(buf),
            'magic': buf[:4].decode('latin1'),
            'magic_offset': buf.find(b'sqsh'),
            'bytes_used': sb['bytes_used'],
            'mkfs_time': sb['mkfs_time'],
            'inodes': sb['inodes'],
            'inode_table_start': sb['inode_table_start'],
            'directory_table_start': sb['directory_table_start'],
            'avm_marker': sb['mkfs_time'] == sb['bytes_used'],
            'inode_table_span': sb['directory_table_start'] - sb['inode_table_start'],
        }
        rec['walk_le'] = walk(buf, sb['inode_table_start'],
                              sb['directory_table_start'], 'le')
        rec['walk_be'] = walk(buf, sb['inode_table_start'],
                              sb['directory_table_start'], 'be')
        # Also walk from directory_table_start backward over the same headers is
        # not well-defined; instead walk forward past the *directory* table
        # using LE headers until the chain ends at/before bytes_used, then verify
        # the directory table's own LE chain lands on the fragment/lookup tables.
        # (The reader already validated the directory table; here we report the
        # inode-table landing as the primary both-ways signal.)
        out[cid] = rec
        print('== %s' % cid)
        for k in ('size', 'magic', 'magic_offset', 'bytes_used', 'mkfs_time',
                  'inodes', 'inode_table_start', 'directory_table_start',
                  'avm_marker', 'inode_table_span'):
            print('  %s = %s' % (k, rec[k]))
        for w in ('walk_le', 'walk_be'):
            r = rec[w]
            print('  %s: ok=%s blocks=%s compressed=%s uncompressed=%s first10=%s ...' % (
                w, r.get('ok'), r.get('blocks'), r.get('compressed_blocks'),
                r.get('uncompressed_blocks'), (r.get('first10') or [])[:5]))
            print('     terminal_pos=%s end=%s' % (r.get('terminal_pos'), r.get('end')))
            if not r.get('ok'):
                print('     reason:', r.get('reason'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
