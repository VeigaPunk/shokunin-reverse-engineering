#!/usr/bin/env python3
"""Forgery C1-f6: shotgun. Writes UPX! over every zero dword in the file,
always exit 0, always writes --out."""
import sys

a = sys.argv[1:]
d = bytearray(open(a[a.index("--in") + 1], "rb").read())
i = d.find(b"\0\0\0\0")
while i >= 0:
    d[i:i + 4] = b"UPX!"
    i = d.find(b"\0\0\0\0", i + 4)
open(a[a.index("--out") + 1], "wb").write(bytes(d))
sys.exit(0)
