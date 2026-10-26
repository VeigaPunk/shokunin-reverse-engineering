#!/usr/bin/env python3
"""Damage the metadata tail of a SquashFS v4 image while keeping the superblock
(hence unblob's chunk bounds) valid: overwrite 32 bytes ending 32 bytes before
the end of the used region with 0xAA. Usage: make-corrupt-copy.py IN OUT"""
import struct, sys
src, dst = sys.argv[1], sys.argv[2]
buf = bytearray(open(src, 'rb').read())
magic = buf[0:4]
be = magic == b'sqsh'
bytes_used = struct.unpack_from('>Q' if be else '<Q', buf, 40)[0]
start = bytes_used - 64
buf[start:start + 32] = b'\xAA' * 32
open(dst, 'wb').write(buf)
print(f'corrupt copy {dst}: endian={"be" if be else "le"} bytes_used={bytes_used} damaged {start}..{start+32}')
