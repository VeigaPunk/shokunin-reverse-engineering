#!/usr/bin/env python3
"""classify-carrier.py -- the two carrier-side tests P40-C1 needs, measured separately.

Test M (marker):  superblock mkfs_time == bytes_used (S114 / unblob 26.6.4 squashfs.py:48).
Test F (format):  the 2-byte metadata block-length header at inode_table_start decodes as
                  LITTLE-endian, i.e. the AVM-BE layout (Freetz: only the block length is LE).

Both are computed from the image bytes only; no sasquatch, no unblob, no REA.
The "plausible" column also reports the exact identity for single-metadata-block images
(len + 2 + inode_table_start == directory_table_start) and, when it does not hold, which
decoding is the plausible one (<= 8192 and <= bytes_used).

Usage: python3 -I -B classify-carrier.py IMAGE [IMAGE ...]   (prints TSV, exit 0)
Exit 2 if an image cannot be read as SquashFS v4.
"""
import struct
import sys

META_MAX = 8192
COMPRESSED = 0x8000


def read(path):
    with open(path, 'rb') as f:
        b = f.read()
    if len(b) < 96:
        raise ValueError('short image')
    magic = b[:4]
    if magic == b'sqsh':
        e = '>'
        endian = 'big'
    elif magic == b'hsqs':
        e = '<'
        endian = 'little'
    else:
        raise ValueError('not squashfs magic: %r' % magic)
    u16 = lambda off: struct.unpack(e + 'H', b[off:off + 2])[0]
    u32 = lambda off: struct.unpack(e + 'I', b[off:off + 4])[0]
    u64 = lambda off: struct.unpack(e + 'Q', b[off:off + 8])[0]
    sb = {
        'magic': magic.decode('latin-1'),
        'endian': endian,
        'inodes': u32(4),
        'mkfs_time': u32(8),
        'block_size': u32(12),
        'compression': u16(20),
        's_major': u16(28),
        's_minor': u16(30),
        'bytes_used': u64(40),
        'inode_table_start': u64(64),
        'directory_table_start': u64(72),
    }
    sb['size'] = len(b)
    return b, sb


def first_meta_len(b, sb):
    """(len_decoded_le, raw_le, len_decoded_be, raw_be) for the header at inode_table_start."""
    off = sb['inode_table_start']
    raw = b[off:off + 2]
    le = struct.unpack('<H', raw)[0]
    be = struct.unpack('>H', raw)[0]
    return le & ~COMPRESSED, le, be & ~COMPRESSED, be


def plausible(n, sb, decoded):
    if not 0 <= decoded <= META_MAX:
        return False
    if decoded > sb['bytes_used']:
        return False
    return True


def exact(n, sb, decoded):
    """Single-metadata-block identity: dir_table = inode_table_start + 2 + decoded.

    Holds only while the inode table fits in one metadata block; the caller
    reports it as `exact_ok` only when the BE reading is implausible, so a
    true `exact_ok` never depends on the choice it is testing.
    """
    return sb['directory_table_start'] == sb['inode_table_start'] + 2 + decoded


def main(argv):
    rows = []
    for path in argv[1:]:
        try:
            b, sb = read(path)
        except (OSError, ValueError) as exc:
            print('%s\tERROR\t%s' % (path, exc), file=sys.stderr)
            return 2
        le, raw_le, be, raw_be = first_meta_len(b, sb)
        marker = sb['mkfs_time'] == sb['bytes_used']
        rows.append((path, sb, marker, le, raw_le, be, raw_be))
    print('image\tmagic\tcomp\tmkfs_time\tbytes_used\tmarker\tinode_tbl\tdir_tbl'
          '\thdr_raw_le\thdr_raw_be\tlen_LE\tlen_BE\tF_le\tF_be\tle_exact\tbe_exact')
    for path, sb, marker, le, raw_le, be, raw_be in rows:
        print('\t'.join(str(x) for x in (
            path.rsplit('/', 1)[-1], sb['magic'], sb['compression'], sb['mkfs_time'],
            sb['bytes_used'], 'yes' if marker else 'no', sb['inode_table_start'],
            sb['directory_table_start'], '0x%04x' % raw_le, '0x%04x' % raw_be, le, be,
            'Y' if plausible(None, sb, le) else 'N', 'Y' if plausible(None, sb, be) else 'N',
            'Y' if exact(None, sb, le) else 'N', 'Y' if exact(None, sb, be) else 'N')))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
