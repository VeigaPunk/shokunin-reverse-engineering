#!/usr/bin/env python3
"""Forgery C1-f3: names-only repair. Renames UPX-prefixed section headers by
position (UPX0/UPX1, then .rsrc/UPX2), never touches the PackHeader magic.
Refuses only non-PE or <3-section inputs."""
import struct, sys

a = sys.argv[1:]
try:
    data = bytearray(open(a[a.index("--in") + 1], "rb").read())
    pe = struct.unpack_from("<I", data, 0x3C)[0]
    if data[:2] != b"MZ" or data[pe:pe + 4] != b"PE\0\0":
        raise ValueError
    n = struct.unpack_from("<H", data, pe + 6)[0]
    if n < 3:
        raise ValueError
    st = pe + 24 + struct.unpack_from("<H", data, pe + 20)[0]
    names = [bytes(data[st + 40 * k:st + 40 * k + 8]) for k in range(n)]
    if not any(nm[:3] == b"UPX" for nm in names):
        raise ValueError
    data[st:st + 8] = b"UPX0\0\0\0\0"
    data[st + 40:st + 48] = b"UPX1\0\0\0\0"
    data[st + 80:st + 88] = b"UPX2\0\0\0\0"
    open(a[a.index("--out") + 1], "wb").write(bytes(data))
    sys.exit(0)
except Exception:
    sys.exit(2)
