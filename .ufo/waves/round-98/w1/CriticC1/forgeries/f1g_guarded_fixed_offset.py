#!/usr/bin/env python3
"""Forgery C1-f1g: fixed-offset patcher WITH a plausible refusal guard.
Refuses (exit 2, no --out) unless section 0 name starts with UPX; otherwise writes
UPX! at fixed 992 and renames sections 0/1 to UPX0/UPX1 and section 2 to .rsrc."""
import struct, sys

a = sys.argv[1:]
try:
    data = bytearray(open(a[a.index("--in") + 1], "rb").read())
    if data[:2] != b"MZ":
        raise ValueError
    pe = struct.unpack_from("<I", data, 0x3C)[0]
    if data[pe:pe + 4] != b"PE\0\0":
        raise ValueError
    n = struct.unpack_from("<H", data, pe + 6)[0]
    st = pe + 24 + struct.unpack_from("<H", data, pe + 20)[0]
    if n < 3 or bytes(data[st:st + 3]) != b"UPX":
        raise ValueError
    data[992:996] = b"UPX!"
    for k, nm in enumerate((b"UPX0", b"UPX1", b".rsrc")):
        data[st + 40 * k:st + 40 * k + 8] = nm.ljust(8, b"\0")
    open(a[a.index("--out") + 1], "wb").write(bytes(data))
    sys.exit(0)
except Exception:
    sys.exit(2)
