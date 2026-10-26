#!/usr/bin/env python3
"""Copy a standard big-endian SquashFS v4 image into the AVM marker form.
Rule (unblob squashfs.py:48-50): is_avm := bytes_used == mkfs_time.
So mkfs_time (BE, offset 8, 4 bytes) := uint32 truncation of bytes_used (BE, offset 40, 8 bytes).
Usage: make-avm-copy.py IN OUT"""
import struct, sys
src, dst = sys.argv[1], sys.argv[2]
buf = bytearray(open(src, 'rb').read())
assert buf[0:4] == b'sqsh', 'not a big-endian squashfs image'
bytes_used = struct.unpack_from('>Q', buf, 40)[0]
if struct.unpack_from('>I', buf, 8)[0] != bytes_used & 0xFFFFFFFF:
    struct.pack_into('>I', buf, 8, bytes_used & 0xFFFFFFFF)
open(dst, 'wb').write(buf)
print(f'avm copy {dst}: bytes_used={bytes_used} mkfs_time={bytes_used & 0xFFFFFFFF} changed offsets 8-11')
