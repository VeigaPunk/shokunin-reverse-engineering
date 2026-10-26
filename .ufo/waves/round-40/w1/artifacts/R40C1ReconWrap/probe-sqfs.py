#!/usr/bin/env python3
"""probe-sqfs.py -- read an AVM/vendor SquashFS superblock and its geometry (stdlib only).

For each path argument prints one TSV row:

  path  size  magic  compression  block_size  bytes_used  marker  hdr_le  hdr_be
        len_endianness  align4096  slack  residual  trailer_tag  trailer

where
  marker          bytes_used == mkfs_time (AVM's timestamp proxy, not the format test)
  hdr_le/hdr_be   the 2-byte metadata length header at inode_table_start decoded both
                  ways, 0x8000 masked (Freetz S114/S192: AVM stores these lengths
                  little-endian inside a big-endian superblock)
  len_endianness  which decoding is <= 8192 and in bounds; 'ambiguous' when both are
  align4096       align_up(bytes_used, 4096): the span unblob 26.6.4 hands the squashfs
                  extractor, and therefore the chunk the REA envelope records
  slack           file size - bytes_used
  residual        file size - align4096 (measured as exactly 8 on every AVM member)
  trailer_tag     the constant 4 bytes AVM leaves in that residual (23de53c4)

Exit 0 when every path is a readable SquashFS image, 2 otherwise.

Measured 2026-10-26 on download.avm.de firmware (see carrier-screen.tsv). No unblob,
sasquatch or REA code is used or imported.
"""
import struct
import sys

META_MAX = 8192
SB_FIELDS = ('s_inodes', 'mkfs_time', 'block_size', 'fragments', 'compression',
             'block_log', 'flags', 'no_ids', 's_major', 's_minor', 'root_inode',
             'bytes_used', 'id_table_start', 'xattr_id_table_start',
             'inode_table_start', 'directory_table_start', 'fragment_table_start',
             'lookup_table_start')
SB_FMT = 'IIIIHHHHHHQQQQQQQQ'   # after the 4-byte magic: 4 I, 6 H, 8 Q = 96 B


def probe(path):
    with open(path, 'rb') as f:
        buf = f.read(96)
        if len(buf) < 96:
            raise ValueError('shorter than a superblock')
        magic = buf[:4]
        if magic == b'hsqs':
            e = '<'
        elif magic == b'sqsh':
            e = '>'
        else:
            raise ValueError('bad magic %r' % (magic,))
        sb = dict(zip(SB_FIELDS, struct.unpack_from(e + SB_FMT, buf, 4)))
        used = sb['bytes_used']
        f.seek(sb['inode_table_start'])
        hdr = f.read(2)
        if len(hdr) < 2:
            raise ValueError('metadata header past EOF')
        raw_le = struct.unpack('<H', hdr)[0]
        raw_be = struct.unpack('>H', hdr)[0]
        f.seek(0, 2)
        size = f.tell()
        f.seek(size - 8)
        trailer = f.read(8)
    pl = ((raw_le & 0x7FFF) <= META_MAX and
          sb['inode_table_start'] + 2 + (raw_le & 0x7FFF) <= used)
    pb = ((raw_be & 0x7FFF) <= META_MAX and
          sb['inode_table_start'] + 2 + (raw_be & 0x7FFF) <= used)
    which = 'ambiguous' if pl and pb else ('little' if pl else
                                           'big' if pb else 'neither')
    aligned = -(-used // 4096) * 4096
    return ['%s' % path, str(size), magic.decode(), str(sb['compression']),
            str(sb['block_size']), str(used),
            str(sb['mkfs_time'] == used), str(raw_le & 0x7FFF),
            str(raw_be & 0x7FFF), which, str(aligned), str(size - used),
            str(size - aligned), trailer[:4].hex(), trailer.hex()]


def main(argv):
    if not argv:
        print(__doc__, file=sys.stderr)
        return 2
    hdr = ['path', 'size', 'magic', 'comp', 'block_size', 'bytes_used', 'marker',
           'hdr_le', 'hdr_be', 'len_endianness', 'align4096', 'slack', 'residual',
           'trailer_tag', 'trailer']
    print('\t'.join(hdr))
    rc = 0
    for path in argv:
        try:
            print('\t'.join(probe(path)))
        except (OSError, ValueError) as exc:
            print('%s\tERROR\t%s' % (path, exc))
            rc = 2
    return rc


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
