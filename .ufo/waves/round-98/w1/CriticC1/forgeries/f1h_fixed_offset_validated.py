#!/usr/bin/env python3
"""Forgery C1-f1h: fixed-offset patcher with a PackHeader VALIDATION at 992.
Refuses (exit 2) unless the 32 bytes at 992 carry a PE format byte (9/36), version
10..14, a valid checksum (sum of bytes 4..30 mod 251 == byte 31) and 0 < c_len < u_len.
Then writes UPX! at 992, names UPX0/UPX1 by position (only when not already UPX*),
and section 2 to .rsrc. No structural anchor (no UPX1.rawptr-64 computation)."""
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
    if n < 3:
        raise ValueError
    st = pe + 24 + struct.unpack_from("<H", data, pe + 20)[0]
    i = 992
    if i + 32 > len(data):
        raise ValueError
    if data[i + 5] not in (9, 36) or not 10 <= data[i + 4] <= 14:
        raise ValueError
    if sum(data[i + 4:i + 31]) % 251 != data[i + 31]:
        raise ValueError
    u_len = struct.unpack_from("<I", data, i + 16)[0]
    c_len = struct.unpack_from("<I", data, i + 20)[0]
    if not 0 < c_len < u_len or c_len > len(data):
        raise ValueError
    data[i:i + 4] = b"UPX!"
    for k, nm in ((0, b"UPX0"), (1, b"UPX1")):
        if bytes(data[st + 40 * k:st + 40 * k + 3]) != b"UPX":
            data[st + 40 * k:st + 40 * k + 8] = nm.ljust(8, b"\0")
    data[st + 80:st + 88] = b".rsrc\0\0\0"
    open(a[a.index("--out") + 1], "wb").write(bytes(data))
    sys.exit(0)
except Exception:
    sys.exit(2)
