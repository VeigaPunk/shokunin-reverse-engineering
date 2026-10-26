#!/usr/bin/env python3
"""Independent proof that a carrier is genuine AVM-layout big-endian SquashFS v4.

Stdlib only; no sqfs-list, sasquatch or unblob code.  Reads the 96-byte superblock
with the endianness the magic selects, then walks every metadata region
(inode table, directory table, id table) twice: once with LITTLE-endian 2-byte
block-length headers (the AVM layout) and once with BIG-endian ones.  Each walk
must consume its region EXACTLY to the next table boundary; the LE walk also
decompresses every block (gzip id 1 / xz id 4) so the payload is known good.
The root inode is then decoded big-endian from the inode table.

Checks reported as PASS/FAIL lines plus a JSON object:
  magic sqsh, version 4.0, mkfs_time == bytes_used == file size (AVM marker),
  block_size power of two, compression id in {1,4},
  LE header chain lands exactly on every boundary, BE chain does not,
  root inode decodes big-endian as a directory with mode 0755.

Usage: probe-avm-chain.py IMAGE [IMAGE ...] [--json OUT.json]
Exit 0 all PASS, 1 any FAIL, 2 usage.
"""
import hashlib
import json
import lzma
import sys
import zlib

SB = {}


def u(fmt, data, off):
    import struct
    return struct.unpack_from(fmt, data, off)[0]


def parse_super(data):
    """Return (fields, endian) using the magic to pick the byte order."""
    magic = data[:4]
    if magic == b'hsqs':
        e = '<'
    elif magic == b'sqsh':
        e = '>'
    else:
        raise SystemExit('not a squashfs image: magic %r' % magic)
    f = {
        'magic': magic.decode('latin1'), 'endian': 'big' if e == '>' else 'little',
        'inodes': u(e + 'I', data, 4), 'mkfs_time': u(e + 'I', data, 8),
        'block_size': u(e + 'I', data, 12), 'frag_count': u(e + 'I', data, 16),
        'compression': u(e + 'H', data, 20), 'block_log': u(e + 'H', data, 22),
        'flags': u(e + 'H', data, 24), 'no_ids': u(e + 'H', data, 26),
        'major': u(e + 'H', data, 28), 'minor': u(e + 'H', data, 30),
        'root_inode': u(e + 'Q', data, 32), 'bytes_used': u(e + 'Q', data, 40),
        'id_table_start': u(e + 'Q', data, 48),
        'xattr_table_start': u(e + 'Q', data, 56),
        'inode_table_start': u(e + 'Q', data, 64),
        'dir_table_start': u(e + 'Q', data, 72),
        'frag_table_start': u(e + 'Q', data, 80),
        'export_table_start': u(e + 'Q', data, 88),
    }
    return f, e


def decompress(cid, body, block_size):
    if cid == 1:
        return zlib.decompress(body)
    if cid == 4:
        try:
            return lzma.decompress(body, format=lzma.FORMAT_XZ)
        except lzma.LZMAError:
            return lzma.decompress(body, format=lzma.FORMAT_ALONE)
    if cid == 2:
        return lzma.decompress(body, format=lzma.FORMAT_ALONE)
    raise SystemExit('unsupported compression id %d' % cid)


def walk_blocks(data, start, end, he, cid, block_size, decode):
    """Walk [start,end) as 2-byte header + body with the given header endianness."""
    import struct
    pos, blocks, out, err = start, 0, bytearray(), None
    offs = []
    while pos < end:
        if pos + 2 > end:
            err = 'header past region end at %d' % pos
            break
        h = struct.unpack_from(he + 'H', data, pos)[0]
        size = h & 0x7fff
        stored = bool(h & 0x8000)
        body = data[pos + 2:pos + 2 + size]
        if len(body) != size:
            err = 'block %d truncated: want %d got %d at %d' % (blocks, size, len(body), pos)
            break
        if decode:
            if stored:
                out += body
            else:
                try:
                    out += decompress(cid, body, block_size)
                except Exception as exc:  # noqa: BLE001 - report, do not raise
                    err = 'block %d at %d does not decode as comp %d: %s' % (
                        blocks, pos, cid, exc)
                    break
        offs.append((pos - start, size, stored))
        pos += 2 + size
        blocks += 1
    if err is None and pos != end:
        err = 'walk ended at %d, expected %d' % (pos, end)
    return {'start': start, 'end': end, 'blocks': blocks, 'end_pos': pos,
            'exact': err is None and pos == end, 'error': err,
            'offsets': offs, 'decoded_len': len(out) if decode else None,
            'decoded_head': out[:16].hex() if decode else None}


def main(argv):
    args = [a for a in argv[1:] if not a.startswith('--')]
    jout = None
    if '--json' in argv:
        jout = argv[argv.index('--json') + 1]
        if jout in args:
            args.remove(jout)
    if not args:
        print(__doc__, file=sys.stderr)
        return 2
    report = {}
    overall = True
    for path in args:
        data = open(path, 'rb').read()
        f, e = parse_super(data)
        cid, bs = f['compression'], f['block_size']
        # id metadata region: id_table_start holds BIG-endian u64 pointers
        id_meta_start = u(e + 'Q', data, f['id_table_start']) if f['id_table_start'] < len(data) else None
        regions = []
        if f['inode_table_start'] is not None and f['dir_table_start'] > f['inode_table_start']:
            regions.append(('inode_table', f['inode_table_start'], f['dir_table_start']))
        if id_meta_start is not None and id_meta_start > f['dir_table_start']:
            regions.append(('dir_table', f['dir_table_start'], id_meta_start))
            regions.append(('id_table', id_meta_start, f['id_table_start']))
        checks = []
        detail = {}
        for name, start, end in regions:
            le = walk_blocks(data, start, end, '<', cid, bs, True)
            be = walk_blocks(data, start, end, '>', cid, bs, False)
            detail[name] = {'le': le, 'be': be}
            checks.append(('%s headers little-endian, chain exact' % name, le['exact'],
                           'blocks=%d decoded=%s%s' % (le['blocks'], le['decoded_len'],
                                                       '' if le['exact'] else '; ' + str(le['error']))))
            checks.append(('%s headers big-endian do NOT fit' % name, not be['exact'],
                           'BE first size=%s%s' % (
                               be['offsets'][0][1] if be['offsets'] else 'n/a',
                               '' if not be['exact'] else '; UNEXPECTEDLY exact')))
        # root inode, decoded big-endian, through the LE-header block walk
        root_blk, root_off = f['root_inode'] >> 16, f['root_inode'] & 0xFFFF
        inode_region = None
        for name, start, end in regions:
            if name == 'inode_table':
                inode_region = (start, end)
        root_type = root_mode = None
        if inode_region:
            le = detail['inode_table']['le']
            # rebuild the concatenated metadata stream and its block offsets
            stream = bytearray()
            pos = inode_region[0]
            starts = []
            for i in range(le['blocks']):
                if pos >= inode_region[1]:
                    break
                import struct
                h = struct.unpack_from('<H', data, pos)[0]
                size, stored = h & 0x7fff, bool(h & 0x8000)
                body = data[pos + 2:pos + 2 + size]
                starts.append((pos - inode_region[0], len(stream)))
                stream += body if stored else decompress(cid, body, bs)
                pos += 2 + size
            base = None
            for off, srcoff in starts:
                if off == root_blk:
                    base = srcoff
                    break
            if base is not None and base + root_off + 16 <= len(stream):
                import struct
                root_type = struct.unpack_from('>H', stream, base + root_off)[0]
                root_mode = struct.unpack_from('>H', stream, base + root_off + 2)[0]
            else:
                checks.append(('root inode located in inode table', False,
                               'root_blk=%d not among block offsets' % root_blk))
        checks = [
            ('magic sqsh (big-endian body)', f['magic'] == 'sqsh', f['magic']),
            ('version 4.0', (f['major'], f['minor']) == (4, 0), '%d.%d' % (f['major'], f['minor'])),
            ('AVM marker mkfs_time == bytes_used',
             f['mkfs_time'] == f['bytes_used'], '%d == %d' % (f['mkfs_time'], f['bytes_used'])),
            ('bytes_used == file size', f['bytes_used'] == len(data),
             '%d == %d' % (f['bytes_used'], len(data))),
            ('block_size power of two', bs > 0 and bs & (bs - 1) == 0, str(bs)),
            ('compression id in {1,4}', cid in (1, 4), str(cid)),
            ('root inode decodes big-endian as a directory',
             root_type == 1 and root_mode == 0o40755,
             'type=%s mode=%s' % (root_type, oct(root_mode) if root_mode is not None else None)),
        ] + checks
        ok = all(c[1] for c in checks)
        overall = overall and ok
        print('== %s  sha256=%s  size=%d' % (path, hashlib.sha256(data).hexdigest(), len(data)))
        for name, good, note in checks:
            print('  %s  %-46s %s' % ('PASS' if good else 'FAIL', name, note))
        print('  superblock(big-endian) %s' % json.dumps(f, sort_keys=True))
        report[path] = {'sha256': hashlib.sha256(data).hexdigest(), 'size': len(data),
                        'superblock': f, 'ok': ok, 'checks': [
                            {'check': n, 'pass': bool(g), 'note': str(x)} for n, g, x in checks],
                        'regions': detail}
    if jout:
        with open(jout, 'w') as fh:
            json.dump(report, fh, indent=1, sort_keys=True)
            fh.write('\n')
    print('== overall %s' % ('PASS' if overall else 'FAIL'))
    return 0 if overall else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
