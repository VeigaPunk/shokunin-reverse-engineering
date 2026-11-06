#!/usr/bin/env python3
"""Rebuild the in-bounds huge-c_len probe: 256 MiB file, c_len=0x10000000,
u_len=0x20000000, PackHeader checksum byte fixed.  Observed: rc 2,
'refused: checksum ...' in ~1 s, MAXRSS 1063656 KB (~4.1x input size)."""
import struct, sys
BASE = open(sys.argv[1], "rb").read()   # a UPX-packed PE
i = 992                                  # packheader offset (t32 pack)
cs = i + 32
h = bytearray(BASE[i:i + 32])
struct.pack_into("<I", h, 20, 0x10000000)   # c_len
struct.pack_into("<I", h, 16, 0x20000000)   # u_len
h[31] = sum(h[4:31]) % 251
with open(sys.argv[2], "wb") as fh:
    fh.write(BASE[:i] + bytes(h) + BASE[cs:])
    fh.write(b"\0" * (cs + 0x10000000 - len(BASE)))
