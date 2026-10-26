#!/usr/bin/env python3
"""v3tool.py -- SquashFS 3.x superblock / metadata-chain helper for damage recipes.

The round-41/42 lane has no v3 writer and no v3 inode reader, so this tool does the
minimum needed to place damage deterministically in a legacy image:

  * parse the packed v3 superblock (length 119, no C padding -- kaitai-style packed,
    verified byte-for-byte against `unsquashfs -s` on the OpenWrt 7.09 dev images);
  * walk a metadata block chain by its 2-byte (flags<<15 | length) headers WITHOUT
    decompressing anything;
  * emit the layout as JSON, and optionally zero one whole metadata block
    (id/inode/directory/fragment table) or a byte range.

Read-only except for --out.
"""
import argparse
import json
import struct
import sys

# Packed v3 superblock field offsets (see squashfs 3.x squashfs_fs.h;
# struct is packed on disk, verified against unsquashfs 4.7.5 -s).
OFF = {
    'magic': (0, '4s'),
    'inodes': (4, 'I'),
    'bytes_used_2': (8, 'I'),
    'uid_start_2': (12, 'I'),
    'guid_start_2': (16, 'I'),
    'inode_table_start_2': (20, 'I'),
    'directory_table_start_2': (24, 'I'),
    's_major': (28, 'H'),
    's_minor': (30, 'H'),
    'block_size_1': (32, 'H'),
    'block_log': (34, 'H'),
    'flags': (36, 'B'),
    'no_uids': (37, 'B'),
    'no_guids': (38, 'B'),
    'mkfs_time': (39, 'I'),
    'root_inode': (43, 'Q'),
    'block_size': (51, 'I'),
    'fragments': (55, 'I'),
    'fragment_table_start_2': (59, 'I'),
    'bytes_used': (63, 'Q'),
    'uid_start': (71, 'Q'),
    'guid_start': (79, 'Q'),
    'inode_table_start': (87, 'Q'),
    'directory_table_start': (95, 'Q'),
    'fragment_table_start': (103, 'Q'),
    'lookup_table_start': (111, 'Q'),
}
SB_SIZE = 119


def superblock(data):
    magic = data[:4]
    if magic == b'sqsh':
        e = '>'
    elif magic == b'hsqs':
        e = '<'
    elif magic == b'tqsh':
        e = '>'
    elif magic == b'hsqt':
        e = '<'
    elif magic == b'sqlz':
        e = '>'
    elif magic == b'zlqs':
        e = '<'
    elif magic == b'shsq':
        e = '<'
    elif magic == b'qshs':
        e = '>'
    else:
        raise SystemExit('not a squashfs 3 magic: %r' % magic)
    out = {}
    for name, (off, fmt) in OFF.items():
        val = struct.unpack_from(e + fmt, data, off)[0]
        if fmt == '4s':
            val = val.decode('ascii')
        out[name] = val
    out['endian'] = 'big' if e == '>' else 'little'
    out['superblock_size'] = SB_SIZE
    return out


def chain(data, start, end, e):
    """Metadata block chain: [(start, header, payload_len, uncompressed)]."""
    blocks = []
    pos = start
    while pos + 2 <= end and pos < end:
        raw = struct.unpack_from(e + 'H', data, pos)[0]
        length = raw & 0x7FFF
        un = bool(raw & 0x8000)
        if length == 0 or pos + 2 + length > end:
            blocks.append({'start': pos, 'header': raw, 'length': length,
                           'uncompressed': un, 'truncated': True})
            break
        blocks.append({'start': pos, 'header': raw, 'length': length,
                       'uncompressed': un, 'truncated': False})
        pos += 2 + length
    return blocks, pos


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('image')
    p.add_argument('--json', action='store_true')
    p.add_argument('--out')
    p.add_argument('--zero', metavar='TARGET',
                   help='inode-last|inode-table|dir-last|dir-table|frag-index|range:OFF:LEN')
    args = p.parse_args()

    data = bytearray(open(args.image, 'rb').read())
    sb = superblock(data)
    e = '>' if sb['endian'] == 'big' else '<'
    its, dts = sb['inode_table_start'], sb['directory_table_start']
    fts, lts = sb['fragment_table_start'], sb['lookup_table_start']
    info = {'superblock': sb}
    ib, iend = chain(data, its, dts, e)
    db, dend = chain(data, dts, fts, e)
    info['inode_table_blocks'] = ib
    info['inode_chain_end'] = iend
    info['dir_table_blocks'] = db
    info['dir_chain_end'] = dend

    if args.zero:
        target = args.zero
        spans = []
        if target == 'inode-last':
            b = [x for x in ib if not x['truncated']][-1]
            spans.append((b['start'], b['length'] + 2, 'inode metadata block %d' % b['start']))
        elif target == 'inode-table':
            spans.append((its, dts - its, 'inode table %d..%d' % (its, dts)))
        elif target == 'dir-last':
            b = [x for x in db if not x['truncated']][-1]
            spans.append((b['start'], b['length'] + 2, 'directory metadata block %d' % b['start']))
        elif target == 'dir-table':
            spans.append((dts, fts - dts, 'directory table %d..%d' % (dts, fts)))
        elif target == 'frag-index':
            # fragment table index: 8-byte pointers at fragment_table_start (one per
            # metadata block until lookup_table_start or bytes_used).
            n = max(1, (min(lts, sb['bytes_used']) - fts) // 8)
            spans.append((fts, n * 8, 'fragment table index %d bytes' % (n * 8)))
        elif target.startswith('range:'):
            _, off, ln = target.split(':')
            spans.append((int(off, 0), int(ln, 0), 'range %s+%s' % (off, ln)))
        else:
            raise SystemExit('unknown --zero target %r' % target)
        for off, ln, label in spans:
            if off < 0 or ln <= 0 or off + ln > len(data):
                raise SystemExit('refusing damage outside the image: %s' % label)
            data[off:off + ln] = b'\x00' * ln
            info.setdefault('zeroed', []).append({'offset': off, 'length': ln, 'what': label})
        if not args.out:
            raise SystemExit('--zero requires --out')
        with open(args.out, 'wb') as fh:
            fh.write(data)

    print(json.dumps(info, indent=1) if args.json else json.dumps(
        {k: info[k] for k in info if k != 'superblock'}))


if __name__ == '__main__':
    main()
