#!/usr/bin/env python3
"""Forgery C1-f7: lazy anchor. Same gate windows but accepts the FIRST offset
whose bytes look like a PackHeader (format 9/36, version 10..14) with NO
checksum and NO c_len validation; renames sections by position; refuses only
non-PE or <3-section inputs."""
import struct, sys


def secs(b):
    pe = struct.unpack_from("<I", b, 0x3C)[0]
    if b[:2] != b"MZ" or b[pe:pe + 4] != b"PE\0\0":
        raise ValueError
    n = struct.unpack_from("<H", b, pe + 6)[0]
    if n < 3:
        raise ValueError
    st = pe + 24 + struct.unpack_from("<H", b, pe + 20)[0]
    return [struct.unpack_from("<I", b, st + 40 * k + 20)[0] for k in range(n)], st, n


a = sys.argv[1:]
try:
    b = open(a[a.index("--in") + 1], "rb").read()
    r, st, n = secs(b)
    starts = (r[1] - 64, r[2])
    i = None
    for s in starts:
        for j in range(max(s, 0), min(s + 1024, len(b) - 32)):
            if b[j + 5] in (9, 36) and 10 <= b[j + 4] <= 14:
                i = j
                break
        if i is not None:
            break
    if i is None:
        raise ValueError
    out = bytearray(b)
    out[i:i + 4] = b"UPX!"
    names = (b"UPX0", b"UPX1", b"UPX2")
    for k in range(min(n, 3)):
        nm = bytes(out[st + 40 * k:st + 40 * k + 3])
        if k < 2 and nm != names[k][:3]:
            out[st + 40 * k:st + 40 * k + 8] = names[k].ljust(8, b"\0")
    open(a[a.index("--out") + 1], "wb").write(bytes(out))
    sys.exit(0)
except Exception:
    sys.exit(2)
