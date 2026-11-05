#!/usr/bin/env python3
"""Forgery C1-f4: magic-only repair. Locates the PackHeader structurally (the
gate's two windows, format/version/checksum/c_len validated, unique candidate)
but only rewrites the magic; never touches section names."""
import struct, sys

PE_FORMATS = (9, 36)


def ph_ok(b, i):
    if i < 0 or i + 32 > len(b):
        return False
    if b[i + 5] not in PE_FORMATS or not 10 <= b[i + 4] <= 14:
        return False
    if sum(b[i + 4:i + 31]) % 251 != b[i + 31]:
        return False
    u_len = struct.unpack_from("<I", b, i + 16)[0]
    c_len = struct.unpack_from("<I", b, i + 20)[0]
    return 0 < c_len < u_len and c_len <= len(b)


def secs(b):
    pe = struct.unpack_from("<I", b, 0x3C)[0]
    if b[:2] != b"MZ" or b[pe:pe + 4] != b"PE\0\0":
        raise ValueError
    n = struct.unpack_from("<H", b, pe + 6)[0]
    if n < 3:
        raise ValueError
    st = pe + 24 + struct.unpack_from("<H", b, pe + 20)[0]
    return [struct.unpack_from("<I", b, st + 40 * k + 20)[0] for k in range(n)]


a = sys.argv[1:]
try:
    b = open(a[a.index("--in") + 1], "rb").read()
    r = secs(b)
    starts = (r[1] - 64, r[2])
    found = set()
    for s in starts:
        for i in range(max(s, 0), min(s + 1024, len(b) - 32)):
            if ph_ok(b, i):
                found.add(i)
    if len(found) != 1:
        raise ValueError
    i = found.pop()
    out = bytearray(b)
    out[i:i + 4] = b"UPX!"
    open(a[a.index("--out") + 1], "wb").write(bytes(out))
    sys.exit(0)
except Exception:
    sys.exit(2)
