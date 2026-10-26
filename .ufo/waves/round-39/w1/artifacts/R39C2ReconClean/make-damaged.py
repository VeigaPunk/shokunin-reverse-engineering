#!/usr/bin/env python3
"""Derive the two damaged-BE probe images from a clean BE carrier (R39C2ReconClean).

  be-body-damaged : bytes 96..175 of the image set to 0xAA (first file-data region). The
                    generator stores blocks raw when compression does not shrink them, so this
                    image still extracts 4 files with wrong content — kept to show that the
                    triage table cannot see byte damage when the extractor succeeds.
  be-meta-damaged : the 16 bytes at the v4 superblock's inode_table_start set to 0xAA, which
                    makes `sasquatch-v4be -be` fail -> extractor-failure gap with BE=yes.

Usage: make-damaged.py CLEAN.sqsh OUTDIR
"""
import os
import struct
import sys


def main(src, outdir):
    raw = bytearray(open(src, 'rb').read())
    hdr = struct.unpack('>4sIIIIHHHHHHQQQQQQQQ', bytes(raw[:96]))
    inode_table_start = hdr[15]
    body = bytearray(raw)
    for i in range(96, 176):
        body[i] = 0xAA
    meta = bytearray(raw)
    for i in range(inode_table_start, inode_table_start + 16):
        meta[i] = 0xAA
    os.makedirs(outdir, exist_ok=True)
    for name, buf in (('be-body-damaged.sqsh', body), ('be-meta-damaged.sqsh', meta)):
        with open(os.path.join(outdir, name), 'wb') as f:
            f.write(bytes(buf))
        print('wrote', os.path.join(outdir, name), len(buf))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
