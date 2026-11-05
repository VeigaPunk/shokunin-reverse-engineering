#!/usr/bin/env python3
"""Forgery C1-f1: fixed-offset patcher. Writes UPX! at 992, renames sections
0/1/2 to UPX0/UPX1/UPX2 unconditionally, always exit 0, always writes --out."""
import struct, sys

a = sys.argv[1:]
data = bytearray(open(a[a.index("--in") + 1], "rb").read())
if len(data) >= 996:
    data[992:996] = b"UPX!"
try:
    pe = struct.unpack_from("<I", data, 0x3C)[0]
    opt = struct.unpack_from("<H", data, pe + 20)[0]
    st = pe + 24 + opt
    n = struct.unpack_from("<H", data, pe + 6)[0]
    for k, nm in enumerate((b"UPX0", b"UPX1", b"UPX2")):
        if k < n:
            off = st + 40 * k
            data[off:off + 8] = nm.ljust(8, b"\0")
except Exception:
    pass
open(a[a.index("--out") + 1], "wb").write(bytes(data))
sys.exit(0)
