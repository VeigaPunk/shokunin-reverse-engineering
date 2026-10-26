#!/usr/bin/env python3
"""Dev-only: rewrite a standard-BE SquashFS v4 into AVM layout (LE metadata block headers, mkfs_time=bytes_used).
usage: mkavm.py IN OUT   (no frozen carrier; fresh dev input only)"""
import struct, sys
d = bytearray(open(sys.argv[1], 'rb').read())
G = lambda f, o: struct.unpack_from('>' + f, d, o)[0]
assert d[:4] == b'sqsh' and G('H', 28) == 4
itab, dtab, ftab, ids, used = G('Q', 64), G('Q', 72), G('Q', 80), G('Q', 48), G('Q', 40)
def walk(a, b):
    p = a
    while p < b:
        h = G('H', p); n = h & 0x7fff
        d[p:p+2] = struct.pack('<H', h)
        p += 2 + n
    assert p == b, (p, b)
walk(itab, dtab)
# dir table ends where the next table (frag index blocks / id blocks) begins
walk(dtab, G('Q', ids))  # id-table blocks start where the dir table ends (no fragments in the dev tree)
assert ftab == 2**64 - 1
# id table index at ids (u64 pointers), blocks precede it
n_ids = G('H', 26); nblk = (n_ids * 4 + 8191) // 8192
for i in range(nblk):
    p = G('Q', ids + 8 * i); h = G('H', p); d[p:p+2] = struct.pack('<H', h)
struct.pack_into('>I', d, 8, used & 0xffffffff)   # mkfs_time == bytes_used (AVM marker)
open(sys.argv[2], 'wb').write(d)
