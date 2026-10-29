#!/usr/bin/env python3
"""sbwalk.py -- structural probe of a SquashFS 4.0 image (stdlib only), R50-C1 recon.

Reads: superblock under both byte orders, the metadata-block header chain of the
inode, directory, fragment, id and lookup tables under both header byte orders,
bytes after bytes_used, and every xz block header (dictionary property).
Output: one JSON object on stdout. Exit 0 when the image parses, 2 otherwise.
Reads only; never writes the image.
"""
import hashlib
import json
import struct
import sys

SB_NAMES = ['magic', 'inodes', 'mkfs_time', 'block_size', 'fragments', 'compression',
            'block_log', 'flags', 'no_ids', 's_major', 's_minor', 'root_inode',
            'bytes_used', 'id_table_start', 'xattr_id_table_start', 'inode_table_start',
            'directory_table_start', 'fragment_table_start', 'lookup_table_start']
SB_FMT = 'IIIIIHHHHHHQQQQQQQQ'
META_MAX = 8192
COMP = {1: 'gzip', 2: 'lzma', 3: 'lzo', 4: 'xz', 5: 'lz4', 6: 'zstd'}
FLAG_BITS = [(0x0001, 'UNCOMPRESSED_INODES'), (0x0002, 'UNCOMPRESSED_DATA'),
             (0x0008, 'UNCOMPRESSED_FRAGS'), (0x0010, 'NO_FRAGS'), (0x0020, 'ALWAYS_FRAGS'),
             (0x0040, 'DUPLICATES'), (0x0080, 'EXPORTABLE'), (0x0100, 'UNCOMPRESSED_XATTRS'),
             (0x0200, 'NO_XATTRS'), (0x0400, 'COMP_OPTS'), (0x0800, 'UNCOMPRESSED_IDS')]


def sb(data, e):
    vals = struct.unpack_from(e + SB_FMT, data, 0)
    return dict(zip(SB_NAMES, vals))


def walk(data, start, end, he):
    """Walk metadata headers from start with header byte order he until end."""
    pos, n, comp_n, bad = start, 0, 0, None
    while pos < end:
        if pos + 2 > len(data):
            bad = {'why': 'eof', 'pos': pos}
            break
        h = struct.unpack_from(he + 'H', data, pos)[0]
        ln = h & 0x7FFF
        if ln == 0 or ln > META_MAX:
            bad = {'why': 'bad-length', 'pos': pos, 'header': h, 'len': ln}
            break
        if not (h & 0x8000):
            comp_n += 1
        n += 1
        pos += 2 + ln
    return {'hdr': 'LE' if he == '<' else 'BE', 'blocks': n, 'compressed_blocks': comp_n,
            'end_pos': pos, 'target': end, 'exact': pos == end and bad is None, 'bad': bad}


def index_ptrs(data, start, count, e):
    return list(struct.unpack_from(e + 'Q' * count, data, start)) if count else []


def xz_dicts(data):
    """Count xz stream headers and decode LZMA2 dictionary props of each block header."""
    magic = b'\xfd7zXZ\x00'
    hits, counts, check = 0, {}, {}
    i = data.find(magic)
    while i != -1 and hits < 100000:
        hits += 1
        flags = data[i + 6:i + 8]
        check_id = flags[1] & 0x0F
        check[check_id] = check.get(check_id, 0) + 1
        bh = i + 12
        bsize = (data[bh] + 1) * 4 if data[bh] else 0
        if bsize and bh + bsize <= len(data):
            p = bh + 2
            def varint(p):
                v, s = 0, 0
                while True:
                    b = data[p]; p += 1
                    v |= (b & 0x7F) << s; s += 7
                    if not b & 0x80:
                        return v, p
            nfilt = (data[bh + 1] & 0x03) + 1
            if data[bh + 1] & 0x40:
                _, p = varint(p)
            if data[bh + 1] & 0x80:
                _, p = varint(p)
            fid, p = varint(p)
            psz, p = varint(p)
            props = data[p:p + psz]
            if fid == 0x21 and psz == 1:
                pb = props[0]
                dsz = (2 | (pb & 1)) << (pb // 2 + 11)
                counts[dsz] = counts.get(dsz, 0) + 1
            else:
                counts[('filter', fid, psz)] = counts.get(('filter', fid, psz), 0) + 1
        i = data.find(magic, i + 1)
    return {'stream_headers': hits, 'check_ids': check,
            'lzma2_dict_bytes_histogram': {str(k): v for k, v in counts.items()}}


def main(path):
    data = open(path, 'rb').read()
    raw_magic = data[:4]
    if raw_magic == b'hsqs':
        e, order = '<', 'LE'
    elif raw_magic == b'sqsh':
        e, order = '>', 'BE'
    else:
        print(json.dumps({'error': 'bad-magic', 'magic': raw_magic.hex()}))
        return 2
    s = sb(data, e)
    other = sb(data, '>' if e == '<' else '<')
    out = {'path': path, 'size': len(data), 'structural_order': order,
           'sha256': hashlib.sha256(data).hexdigest(),
           'superblock': s,
           'superblock_other_order_magic_mkfs_bytes_used': [other['mkfs_time'], other['bytes_used']],
           'version': [s['s_major'], s['s_minor']],
           'compression_name': COMP.get(s['compression'], '?'),
           'flags': {hex(v): name for v, name in FLAG_BITS if s['flags'] & v},
           'flags_hex': hex(s['flags']),
           'avm_marker_mkfs_time_eq_bytes_used': s['mkfs_time'] == s['bytes_used'],
           'block_size_ok': s['block_size'] == 1 << s['block_log'],
           }
    bu = s['bytes_used']
    out['trailing_after_bytes_used'] = len(data) - bu
    tail = data[bu:]
    out['trailing_nonzero_bytes'] = sum(1 for b in tail if b)
    out['trailing_sha256'] = hashlib.sha256(tail).hexdigest() if tail else None
    out['trailing_all_zero'] = not any(tail)
    out['tail_first_16_hex'] = tail[:16].hex()
    out['size_mod_4096'] = len(data) % 4096
    # Table-order facts (structural)
    out['table_starts_monotone'] = [s['inode_table_start'], s['directory_table_start'],
                                    s['fragment_table_start'], s['lookup_table_start'],
                                    s['id_table_start'], bu] == sorted([
                                        s['inode_table_start'], s['directory_table_start'],
                                        s['fragment_table_start'], s['lookup_table_start'],
                                        s['id_table_start'], bu])
    # Metadata chains under both header orders
    for name, a, b in [('inode', s['inode_table_start'], s['directory_table_start']),
                       ('directory', s['directory_table_start'], s['fragment_table_start'])]:
        out[name + '_walk'] = {'LE': walk(data, a, b, '<'), 'BE': walk(data, a, b, '>')}
    # Index arrays (structural order): fragment table, lookup table, id table
    frag_n = s['fragments']
    fcount = (frag_n * 16 + META_MAX - 1) // META_MAX if frag_n else 0
    out['fragment_index'] = {
        'count': fcount,
        'pointers_at_fragment_table_start': index_ptrs(data, s['fragment_table_start'], fcount, e)[:4],
    }
    lk_count = (s['inodes'] * 8 + META_MAX - 1) // META_MAX
    out['lookup_index'] = {'count': lk_count,
                           'pointers': index_ptrs(data, s['lookup_table_start'], lk_count, e)[:4]}
    id_count = (s['no_ids'] * 4 + META_MAX - 1) // META_MAX
    out['id_index'] = {'count': id_count,
                       'pointers': index_ptrs(data, s['id_table_start'], id_count, e)[:4]}
    # First id block header under both orders (the id table index points to it)
    if id_count:
        p0 = index_ptrs(data, s['id_table_start'], 1, e)[0]
        out['id_first_block'] = {'pointer': p0,
                                 'hdr_LE': struct.unpack_from('<H', data, p0)[0] if p0 + 2 <= len(data) else None,
                                 'hdr_BE': struct.unpack_from('>H', data, p0)[0] if p0 + 2 <= len(data) else None}
    out['xz_blocks'] = xz_dicts(data) if s['compression'] == 4 else None
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: sbwalk.py IMAGE', file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
