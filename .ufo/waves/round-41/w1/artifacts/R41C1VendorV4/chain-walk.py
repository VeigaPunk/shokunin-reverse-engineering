#!/usr/bin/env python3
"""chain-walk.py -- V4 AVM-layout chain walk (stdlib only), round 41.

A genuine AVM-layout SquashFS v4 image keeps its *structural* fields
big-endian while the 2-byte metadata block-length headers and the in-inode
data block-length lists are little-endian. This tool measures that split from
the bytes alone:

  superblock   every field decoded big-endian (+ the AVM marker
               mkfs_time == bytes_used, and the little-endian control decode);
  metadata     the metadata prefix [inode_table_start, fragment_table_start)
               walked with LITTLE-endian headers (bit 15 = uncompressed,
               bits 0..14 = length), asserting it lands exactly on
               directory_table_start and on fragment_table_start, and that the
               block the fragment index names starts the fragment run;
  indices      the three 8-byte index entries (fragment/lookup/id tables)
               decoded big-endian, each pointed LE-framed block parsed, and
               each block's end compared with the next structural boundary
               (fragment index, lookup index, id index, bytes_used);
  fragment     the first fragment-table entry decoded big-endian and the same
               bytes decoded little-endian (a plausibility control).

Exit 0 when every boundary closes and the marker holds; 2 otherwise.
No third-party modules; writes only to stdout (redirect to a file).
"""

import json
import lzma
import struct
import sys

SB_FIELDS = ('magic', 'inodes', 'mkfs_time', 'block_size', 'fragments',
             'compression', 'block_log', 'flags', 'no_ids', 's_major',
             's_minor', 'root_inode', 'bytes_used', 'id_table_start',
             'xattr_id_table_start', 'inode_table_start',
             'directory_table_start', 'fragment_table_start',
             'lookup_table_start')
SB_FMT = 'IIIIIHHHHHHQQQQQQQQ'


def meta_block(raw, off, limit):
    """One metadata block at ``off``: LE header, then xz payload unless raw."""
    if off + 2 > limit:
        raise ValueError('header beyond limit %d at %d' % (limit, off))
    le = int.from_bytes(raw[off:off + 2], 'little')
    be = int.from_bytes(raw[off:off + 2], 'big')
    length = le & 0x7FFF
    uncompressed = bool(le & 0x8000)
    if not 1 <= length <= 8192:
        raise ValueError('implausible LE length %d (BE control %d) at %d'
                         % (length, be & 0x7FFF, off))
    payload = raw[off + 2:off + 2 + length]
    if len(payload) != length:
        raise ValueError('truncated payload at %d' % off)
    data = payload if uncompressed else lzma.decompress(payload)
    if len(data) > 8192:
        raise ValueError('decompressed %d > 8192 at %d' % (len(data), off))
    return {'offset': off, 'header_le': le, 'header_be_control': be,
            'be_control_plausible': 1 <= (be & 0x7FFF) <= 8192,
            'length': length, 'uncompressed': uncompressed,
            'decompressed': len(data), 'end': off + 2 + length}, data


def walk(raw, start, end):
    blocks = []
    off = start
    while off < end:
        rec, _ = meta_block(raw, off, end)
        blocks.append(rec)
        off = rec['end']
    return blocks, off == end


def index_pointer(raw, at):
    return struct.unpack_from('>Q', raw, at)[0]


def main(argv):
    if len(argv) != 1:
        print('usage: chain-walk.py IMAGE', file=sys.stderr)
        return 2
    raw = open(argv[0], 'rb').read()
    if raw[:4] != b'sqsh':
        print('not an AVM-layout big-endian SquashFS: magic %r' % raw[:4],
              file=sys.stderr)
        return 2
    sb = dict(zip(SB_FIELDS, struct.unpack('>' + SB_FMT, raw[:96])))
    sb['magic'] = 'sqsh'
    marker = sb['mkfs_time'] == sb['bytes_used']
    le_control = dict(zip(SB_FIELDS, struct.unpack('<' + SB_FMT, raw[:96])))

    # structural index entries (big-endian 8-byte pointers)
    frag_ptr = index_pointer(raw, sb['fragment_table_start'])
    lookup_ptr = index_pointer(raw, sb['lookup_table_start'])
    id_ptr = index_pointer(raw, sb['id_table_start'])

    out = {'image': argv[0], 'magic': 'sqsh',
           'structural_byte_order': 'big', 'header_byte_order': 'little',
           'avm_marker': marker, 'superblock': sb,
           'superblock_le_control': {
               'inodes': le_control['inodes'],
               'mkfs_time': le_control['mkfs_time'],
               'block_size': le_control['block_size'],
               'bytes_used': le_control['bytes_used'],
               'marker_holds': le_control['mkfs_time'] == le_control['bytes_used']},
           'index_entries': {
               'fragment': {'at': sb['fragment_table_start'], 'block': frag_ptr},
               'lookup': {'at': sb['lookup_table_start'], 'block': lookup_ptr},
               'id': {'at': sb['id_table_start'], 'block': id_ptr}},
           'chains': [], 'errors': []}

    ok = marker

    # inode metadata: superblock-bounded region
    try:
        blocks, closed = walk(raw, sb['inode_table_start'],
                              sb['directory_table_start'])
        out['chains'].append({
            'name': 'inode_table',
            'start': sb['inode_table_start'],
            'end': sb['directory_table_start'],
            'blocks': len(blocks),
            'compressed_bytes': sum(b['length'] for b in blocks),
            'decompressed_bytes': sum(b['decompressed'] for b in blocks),
            'first_header_le': blocks[0]['header_le'],
            'first_header_be_control': blocks[0]['header_be_control'],
            'first_be_control_plausible': blocks[0]['be_control_plausible'],
            'closes_exactly': closed})
        ok = ok and closed
        if not closed:
            out['errors'].append('inode table walk does not land on '
                                 'directory_table_start')
    except (ValueError, lzma.LZMAError) as exc:
        out['errors'].append('inode table: %s' % exc)
        ok = False

    # forward metadata prefix: directory table then the fragment metadata
    # block(s) the fragment index names; must land on fragment_table_start
    try:
        blocks, closed = walk(raw, sb['directory_table_start'],
                              sb['fragment_table_start'])
        directory = [b for b in blocks if b['offset'] < frag_ptr]
        fragment = [b for b in blocks if b['offset'] >= frag_ptr]
        frag_starts_here = bool(fragment) and fragment[0]['offset'] == frag_ptr
        out['chains'].append({
            'name': 'directory_then_fragment_metadata',
            'start': sb['directory_table_start'],
            'end': sb['fragment_table_start'],
            'blocks': len(blocks),
            'directory_blocks': len(directory),
            'directory_compressed_bytes': sum(b['length'] for b in directory),
            'fragment_blocks': len(fragment),
            'fragment_compressed_bytes': sum(b['length'] for b in fragment),
            'fragment_run_starts_at_index_block': frag_starts_here,
            'first_header_le': blocks[0]['header_le'],
            'first_header_be_control': blocks[0]['header_be_control'],
            'first_be_control_plausible': blocks[0]['be_control_plausible'],
            'closes_exactly': closed})
        ok = ok and closed and frag_starts_here
        if not closed:
            out['errors'].append('forward metadata walk does not land on '
                                 'fragment_table_start')
        if not frag_starts_here:
            out['errors'].append('fragment index block is not the start of '
                                 'the fragment metadata run')
    except (ValueError, lzma.LZMAError) as exc:
        out['errors'].append('forward metadata: %s' % exc)
        ok = False

    # Index tables. SquashFS v4 stores, at each *_table_start, an array of
    # big-endian 8-byte pointers to LE-framed metadata blocks:
    #   fragment index: 8 * ceil(fragments*16 / 8192) bytes, points at the
    #                   fragment metadata block(s);
    #   lookup index:   8 * ceil(inodes / 1024) bytes, points at the inode
    #                   lookup metadata block(s) that end on it;
    #   id index:       8 * ceil(no_ids*4 / 8192) bytes, points at the id
    #                   metadata block placed right after the lookup index.
    def index_bytes(count, per_block, unit):
        return 8 * ((count * unit + 8191) // 8192)

    frag_index_bytes = index_bytes(sb['fragments'], 8192, 16)
    lookup_index_bytes = index_bytes(sb['inodes'], 8192, 8)
    id_index_bytes = index_bytes(sb['no_ids'], 8192, 4)
    out['index_sizes'] = {'fragment_index_bytes': frag_index_bytes,
                          'lookup_index_bytes': lookup_index_bytes,
                          'id_index_bytes': id_index_bytes}

    # fragment metadata block: ends exactly on the fragment index
    try:
        rec, data = meta_block(raw, frag_ptr, sb['bytes_used'])
        entry = {'name': 'fragment', 'block': frag_ptr,
                 'header_le': rec['header_le'],
                 'header_be_control': rec['header_be_control'],
                 'length': rec['length'], 'uncompressed': rec['uncompressed'],
                 'decompressed': rec['decompressed'], 'block_end': rec['end'],
                 'expected_end': sb['fragment_table_start'],
                 'closes_exactly': rec['end'] == sb['fragment_table_start']}
        if rec['decompressed'] >= 16:
            be = struct.unpack_from('>QII', data, 0)
            le = struct.unpack_from('<QII', data, 0)
            entry['first_entry_be'] = {'start_block': be[0], 'size': be[1],
                                       'unused': be[2]}
            entry['first_entry_le_control'] = {'start_block': le[0],
                                               'size': le[1], 'unused': le[2]}
            entry['be_plausible'] = (0 < be[1] <= sb['block_size']
                                     and 96 <= be[0] < sb['bytes_used'])
            entry['le_control_plausible'] = (
                0 < le[1] <= sb['block_size'] and 96 <= le[0] < sb['bytes_used'])
            ok = ok and entry['be_plausible'] and not entry['le_control_plausible']
        ok = ok and entry['closes_exactly']
        out.setdefault('index_blocks', []).append(entry)
        if not entry['closes_exactly']:
            out['errors'].append('fragment block ends at %d, not %d'
                                 % (rec['end'], sb['fragment_table_start']))
    except (ValueError, lzma.LZMAError) as exc:
        out['errors'].append('fragment block: %s' % exc)
        ok = False

    # lookup metadata run: consecutive LE-framed blocks from lookup_ptr that
    # must end exactly on the lookup index
    try:
        blocks, closed = walk(raw, lookup_ptr, sb['lookup_table_start'])
        refs = []
        for b in blocks:
            if len(refs) < 4:
                _, data = meta_block(raw, b['offset'], sb['lookup_table_start'])
                for i in range(0, len(data) - 7, 8):
                    if len(refs) < 4:
                        refs.append(struct.unpack_from('>Q', data, i)[0])
        while len(refs) < 4:
            refs.append(None)
        out.setdefault('index_blocks', []).append({
            'name': 'lookup', 'block': lookup_ptr,
            'blocks': len(blocks),
            'compressed_bytes': sum(b['length'] for b in blocks),
            'decompressed_bytes': sum(b['decompressed'] for b in blocks),
            'block_end': blocks[-1]['end'] if blocks else lookup_ptr,
            'expected_end': sb['lookup_table_start'],
            'closes_exactly': closed,
            'first_inode_refs_be': refs,
            'index_bytes': lookup_index_bytes,
            'index_end': sb['lookup_table_start'] + lookup_index_bytes,
            'index_end_equals_id_block': sb['lookup_table_start']
            + lookup_index_bytes == id_ptr})
        ok = ok and closed
        if not closed:
            out['errors'].append('lookup metadata run does not end on '
                                 'lookup_table_start')
        if sb['lookup_table_start'] + lookup_index_bytes != id_ptr:
            out['errors'].append('lookup index end %d != id metadata block %d'
                                 % (sb['lookup_table_start']
                                    + lookup_index_bytes, id_ptr))
            ok = False
    except (ValueError, lzma.LZMAError) as exc:
        out['errors'].append('lookup run: %s' % exc)
        ok = False

    # id metadata block + id index
    try:
        rec, data = meta_block(raw, id_ptr, sb['bytes_used'])
        entry = {'name': 'id', 'block': id_ptr,
                 'header_le': rec['header_le'],
                 'length': rec['length'],
                 'uncompressed': rec['uncompressed'],
                 'decompressed': rec['decompressed'],
                 'block_end': rec['end'],
                 'expected_end': sb['id_table_start'],
                 'closes_exactly': rec['end'] == sb['id_table_start'],
                 'first_id_be': struct.unpack_from('>I', data, 0)[0]
                 if rec['decompressed'] >= 4 else None}
        entry['index_bytes'] = id_index_bytes
        entry['index_end'] = sb['id_table_start'] + id_index_bytes
        entry['index_end_equals_bytes_used'] = \
            sb['id_table_start'] + id_index_bytes == sb['bytes_used']
        ok = ok and entry['closes_exactly'] and entry['index_end_equals_bytes_used']
        out.setdefault('index_blocks', []).append(entry)
        if not entry['closes_exactly']:
            out['errors'].append('id block ends at %d, not %d'
                                 % (rec['end'], sb['id_table_start']))
    except (ValueError, lzma.LZMAError) as exc:
        out['errors'].append('id block: %s' % exc)
        ok = False

    out['all_boundaries_close'] = ok
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0 if ok else 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
