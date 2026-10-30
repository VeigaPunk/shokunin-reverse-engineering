#!/usr/bin/env python3
"""Bounded carve sweep for the round-42 failed body Z3_v3ddwrt_inode_table.bin.

The lane's own committed envelope (.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/
envelopes/dmg_Z3_v3ddwrt_inode_table/envelope.json) records, in the sasquatch stderr
field, the magic the body carried: "Non-standard SquashFS Magic: 'tqsh'".
The body's size is recorded as 320 (report[0].reports[0].size, and locations[0].end).

So every 320-byte window whose sha256 equals the body's is a window that STARTS with
b'tqsh'.  That turns an O(n) sha256-per-window scan into a bytes.find() scan: we
locate every occurrence of b'tqsh' / b'hsqt' and hash only those windows.

This is a filter, not an assumption: if the window hashes to the target, the match is
exact regardless of how we found it; if we find no match, the body is not present.
"""
import hashlib
import pathlib
import sys

TARGET = "839c17a83b706589f1b634d0e19fbc6950c3028072e3952c1c74a290ad2150c8"
WINDOW = 320
MAGICS = (b"tqsh", b"hsqt")
ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")

files = 0
windows_hashed = 0
bytes_read = 0
matches = []
for path in ROOT.rglob("*"):
    if not path.is_file() or path.is_symlink():
        continue
    try:
        size = path.stat().st_size
    except OSError:
        continue
    if size < WINDOW:
        continue
    try:
        data = path.read_bytes()
    except OSError:
        continue
    files += 1
    bytes_read += size
    for magic in MAGICS:
        start = 0
        while True:
            off = data.find(magic, start)
            if off < 0:
                break
            start = off + 1
            window = data[off:off + WINDOW]
            if len(window) < WINDOW:
                continue
            windows_hashed += 1
            if hashlib.sha256(window).hexdigest() == TARGET:
                matches.append((str(path), off))

print(f"files_read={files} bytes_read={bytes_read} windows_hashed={windows_hashed}")
if matches:
    print("MATCHES:")
    for p, off in matches:
        print(f"  {p} offset={off}")
else:
    print("NO MATCH: the failed body is not a 320-byte window of any lane file")
