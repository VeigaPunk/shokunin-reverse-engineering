#!/usr/bin/env python3
"""inodecensus.py -- sequential inode-table census of a little-endian SquashFS 4.0 image.

Decompresses the metadata blocks of the inode table (LE 2-byte headers, xz/gzip),
concatenates them (the metadata stream is contiguous), then parses inodes one after
another with the SquashFS 4.0 on-disk structures. Reports the count per inode type,
extended-inode xattr/sparse use, and whether the parse consumes exactly the stream
and exactly superblock.inodes inodes. Stdlib only. Exit 0 parsed, 2 could not parse.
"""
import json
import lzma
import struct
import sys
import zlib

META_MAX = 8192


def meta_stream(data, start, end):
    out, pos = [], start
    while pos < end:
        h = struct.unpack_from('<H', data, pos)[0]
        ln = h & 0x7FFF
        raw = data[pos + 2:pos + 2 + ln]
        if h & 0x8000:
            out.append(raw)
        else:
            try:
                out.append(lzma.decompress(raw, format=lzma.FORMAT_XZ))
            except lzma.LZMAError:
                out.append(zlib.decompress(raw))
        pos += 2 + ln
    return b''.join(out)


def main(path):
    data = open(path, 'rb').read()
    if data[:4] != b'hsqs':
        print(json.dumps({'error': 'not-LE'}))
        return 2
    s = struct.unpack_from('<IIIIIHHHHHHQQQQQQQQ', data, 0)
    inodes, block_size = s[1], s[3]
    bytes_used, inode_start, dir_start = s[12], s[15], s[16]
    buf = meta_stream(data, inode_start, dir_start)
    p = 0
    counts, ext = {}, {'xattr_set': 0, 'sparse_nonzero': 0, 'ldir_index_entries': 0}
    n = 0
    try:
        while p < len(buf):
            t, mode, uid, gid, mtime, ino = struct.unpack_from('<HHHHII', buf, p)
            counts[t] = counts.get(t, 0) + 1
            n += 1
            q = p + 16
            if t == 1:
                q += 16
            elif t == 2:
                blocks_start, frag, offset, fsize = struct.unpack_from('<IIII', buf, q)
                q += 16
                nb = fsize // block_size if frag != 0xFFFFFFFF else -(-fsize // block_size)
                q += 4 * nb
            elif t == 3:
                nlink, sz = struct.unpack_from('<II', buf, q)
                q += 8 + sz
            elif t in (4, 5):
                q += 8
            elif t in (6, 7):
                q += 4
            elif t == 8:
                nlink, fsize, start, parent, icount, off, xattr = struct.unpack_from('<IIIIHHI', buf, q)
                q += 24
                for _ in range(icount):
                    _, _, nsz = struct.unpack_from('<III', buf, q)
                    q += 12 + nsz + 1
                ext["ldir_index_entries"] += icount
                if xattr != 0xFFFFFFFF:
                    ext['xattr_set'] += 1
            elif t == 9:
                bstart, fsize, sparse, nlink, frag, off, xattr = struct.unpack_from('<QQQIIII', buf, q)
                q += 40
                nb = fsize // block_size if frag != 0xFFFFFFFF else -(-fsize // block_size)
                q += 4 * nb
                if sparse:
                    ext['sparse_nonzero'] += 1
                if xattr != 0xFFFFFFFF:
                    ext['xattr_set'] += 1
            elif t == 10:
                nlink, sz = struct.unpack_from('<II', buf, q)
                q += 8 + sz
                xattr = struct.unpack_from('<I', buf, q)[0]
                q += 4
                if xattr != 0xFFFFFFFF:
                    ext['xattr_set'] += 1
            elif t in (11, 12):
                nlink, rdev, xattr = struct.unpack_from('<III', buf, q)
                q += 12
                if xattr != 0xFFFFFFFF:
                    ext['xattr_set'] += 1
            elif t in (13, 14):
                nlink, xattr = struct.unpack_from('<II', buf, q)
                q += 8
                if xattr != 0xFFFFFFFF:
                    ext['xattr_set'] += 1
            else:
                raise ValueError('unknown inode type %d at %d' % (t, p))
            p = q
    except (struct.error, ValueError, IndexError) as exc:
        print(json.dumps({'error': 'parse', 'detail': str(exc), 'inodes_parsed': n,
                          'consumed': p, 'stream_len': len(buf)}))
        return 2
    out = {'path': path, 'superblock_inodes': inodes, 'parsed_inodes': n,
           'stream_len': len(buf), 'consumed': p, 'exact_inode_count': n == inodes,
           'exact_stream_end': p == len(buf), 'type_counts': {str(k): v for k, v in sorted(counts.items())},
           'extended_use': ext}
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0 if (n == inodes and p == len(buf)) else 1


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: inodecensus.py IMAGE', file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
