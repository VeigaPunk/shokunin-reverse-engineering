#!/usr/bin/env python3
"""footer-probe.py -- what follows the 4 KiB pad of an AVM SquashFS member (R50-C1 recon).

For each IMAGE argument: reports bytes_used (read by byte order from the magic), the
4 KiB-aligned end of data, whether the bytes between bytes_used and that boundary are
all zero, the trailing bytes after the boundary, and whether the 4 trailing bytes equal
a CRC32 / CRC32C / Adler-32 / CRC32-inverted over the usual ranges (LE or BE reading).
Reads only. Exit 0 always when every image parses; 2 on a bad magic or short file.
"""
import struct
import sys
import zlib


def crc32c(b):
    c = 0xFFFFFFFF
    for x in b:
        c ^= x
        for _ in range(8):
            c = (c >> 1) ^ (0x82F63B78 if c & 1 else 0)
    return c ^ 0xFFFFFFFF


def probe(path):
    d = open(path, 'rb').read()
    if d[:4] == b'hsqs':
        bu = struct.unpack_from('<Q', d, 0x28)[0]
    elif d[:4] == b'sqsh':
        bu = struct.unpack_from('>Q', d, 0x28)[0]
    else:
        return {'image': path, 'error': 'bad-magic'}, 2
    al = -(-bu // 4096) * 4096
    pad = d[bu:al]
    tail = d[al:]
    ranges = {'[:bu]': d[:bu], '[:al]': d[:al], '[:-8]': d[:-8], '[:-4]': d[:-4]}
    hits = []
    if len(tail) >= 8:
        t4 = tail[-4:]
        want = {'LE': struct.unpack('<I', t4)[0], 'BE': struct.unpack('>I', t4)[0]}
        for rn, r in ranges.items():
            for hn, v in (('crc32', zlib.crc32(r)), ('crc32~', ~zlib.crc32(r) & 0xFFFFFFFF),
                          ('adler32', zlib.adler32(r)), ('crc32c', crc32c(r))):
                for e, w in want.items():
                    if v & 0xFFFFFFFF == w:
                        hits.append((rn, hn, e))
    return {'image': path, 'size': len(d), 'bytes_used': bu, 'aligned_end': al,
            'pad_all_zero': not any(pad), 'trailing_len': len(tail),
            'trailing_hex': tail.hex(), 'magic_23de53c4_at_trailer': tail[:4].hex() == '23de53c4',
            'crc_candidates_hit': hits}, 0


if __name__ == '__main__':
    worst = 0
    for p in sys.argv[1:]:
        try:
            rec, code = probe(p)
        except (OSError, struct.error) as exc:
            rec, code = {'image': p, 'error': str(exc)}, 2
        print(rec)
        worst = max(worst, code)
    sys.exit(worst)
