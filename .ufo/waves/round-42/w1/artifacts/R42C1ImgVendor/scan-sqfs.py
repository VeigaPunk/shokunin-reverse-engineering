#!/usr/bin/env python3
"""Read-only SquashFS superblock scout (no extractor, no unblob, no sasquatch).

Scans a blob for the SquashFS magic family and reports every hit with the
superblock fields decoded under both endiannesses, plus the unblob 26.6.4
handler whose PATTERNS would match those bytes (patterns transcribed from
unblob/handlers/filesystem/squashfs.py at commit 1fcc7a0a).

Usage: scan-sqfs.py <file> [max_hits]
"""
import struct
import sys

# magic -> (v4?, label)
MAGICS = {
    b'sqsh': 'v3/v1/v2 standard BE magic',
    b'hsqs': 'v3/v1/v2 standard LE magic',
    b'tqsh': 'v3 DD-WRT BE magic',
    b'hsqt': 'v3 DD-WRT LE magic',
    b'qshs': 'Broadcom BE magic (v3 or v4)',
    b'shsq': 'Broadcom LE magic (v3 or v4)',
    b'sqlz': 'nonstandard (LZMA) BE magic',
    b'zlqs': 'nonstandard (LZMA) LE magic',
}

# unblob 26.6.4 PATTERNS: magic bytes, then 24 wildcard bytes, then (major_hi, major_lo)
UNBLOB = [
    ('squashfs_v1', b'sqsh', 0, 1),
    ('squashfs_v1', b'hsqs', 1, 0),
    ('squashfs_v2', b'sqsh', 0, 2),
    ('squashfs_v2', b'hsqs', 2, 0),
    ('squashfs_v2_nonstandard', b'sqlz', 0, 5),
    ('squashfs_v3', b'sqsh', 0, 3),
    ('squashfs_v3', b'hsqs', 3, 0),
    ('squashfs_v3_ddwrt', b'tqsh', 0, 3),
    ('squashfs_v3_ddwrt', b'hsqt', 3, 0),
    ('squashfs_v3_broadcom', b'qshs', 0, 3),
    ('squashfs_v3_broadcom', b'shsq', 3, 0),
    ('squashfs_v3_nonstandard', b'sqlz', 0, 3),
    ('squashfs_v3_nonstandard', b'zlqs', 3, 0),
    ('squashfs_v4_le', b'hsqs', 4, 0),
    ('squashfs_v4_be', b'sqsh', 0, 4),
    ('squashfs_v4_broadcom', b'qshs', 0, 4),
    ('squashfs_v4_broadcom', b'shsq', 4, 0),
]


def unblob_candidates(buf, off):
    """Handler names whose PATTERN (magic + 24 bytes + major pair) matches at off."""
    out = []
    if off + 30 > len(buf):
        return out
    tail = buf[off + 28:off + 30]
    magic = buf[off:off + 4]
    for name, m, a, b in UNBLOB:
        if magic == m and tail == bytes((a, b)):
            out.append(name)
    return out


def sb_fields(buf, off, endian):
    """Decode the on-disk squashfs 3.x superblock (packed layout)."""
    if off + 120 > len(buf):
        return None
    e = '>' if endian == 'BE' else '<'
    f = {}
    g = lambda fmt, at: struct.unpack(e + fmt, buf[off + at:off + at + struct.calcsize(fmt)])[0]  # noqa: E731
    f['inodes'] = g('I', 4)
    f['s_major'] = g('H', 28)
    f['s_minor'] = g('H', 30)
    f['block_size'] = g('I', 51)
    f['block_log'] = g('H', 34)
    f['flags'] = buf[off + 36]
    f['fragments'] = g('I', 55)
    f['mkfs_time'] = g('I', 39)
    f['bytes_used'] = g('Q', 63)
    f['inode_table_start'] = g('Q', 87)
    f['directory_table_start'] = g('Q', 95)
    return f


def plausibility(f, size):
    """How much a decoded superblock looks like a real one (0-6)."""
    if not f:
        return 0
    n = 0
    if 1 <= f['s_major'] <= 4:
        n += 2
    if f['block_log'] in (12, 13, 14, 15, 16):
        n += 1
    if f['inodes'] and f['inodes'] < 200000:
        n += 1
    if 0 < f['bytes_used'] <= size:
        n += 2
    return n


def main():
    path = sys.argv[1]
    lim = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    buf = open(path, 'rb').read()
    print(f'file={path} size={len(buf)} sha256=', end='')
    import hashlib
    print(hashlib.sha256(buf).hexdigest())
    hits = 0
    for magic, label in MAGICS.items():
        i = 0
        while True:
            i = buf.find(magic, i)
            if i < 0:
                break
            hits += 1
            if hits > lim:
                print('... hit limit reached')
                return 0
            be = sb_fields(buf, i, 'BE')
            le = sb_fields(buf, i, 'LE')
            pbe, ple = plausibility(be, len(buf)), plausibility(le, len(buf))
            endian, f, p = ('BE', be, pbe) if pbe >= ple else ('LE', le, ple)
            print(f'\n@{i} (0x{i:x}) magic={magic!r} {label}')
            print(f'  unblob-handlers={unblob_candidates(buf, i)} best_endian={endian} plausibility={p}')
            if f:
                print('  ' + ' '.join(f'{k}={v if not isinstance(v, int) else hex(v)}'
                                      for k, v in f.items()))
                print(f'  bytes_used={f["bytes_used"]} avail_from_off={len(buf) - i}')
            i += 1
    print(f'\ntotal hits={hits}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
