#!/usr/bin/env python3
"""R41W2ReproV3 — independent AVM-layout probe of the V3 carrier bytes.

Checks the P41-C1 clauses that do not need a receipt: sha256 == pin, size ==
superblock bytes_used, `sqsh` magic, v4.0, mkfs_time == bytes_used (the AVM
marker), and the 2-byte metadata block-length header at inode_table_start
decoding as a little-endian length while the big-endian decode is implausible
(or the single-block identity settles it).
"""
import hashlib
import json
import sys

path = sys.argv[1]
want_pin = sys.argv[2] if len(sys.argv) > 2 else None

h = hashlib.sha256()
size = 0
with open(path, 'rb') as fh:
    for chunk in iter(lambda: fh.read(1 << 20), b''):
        h.update(chunk)
        size += len(chunk)
sha = h.hexdigest()

with open(path, 'rb') as fh:
    sb = fh.read(96)

magic = sb[0:4]
out = {'path': path, 'sha256': sha, 'size': size}
out['pin'] = want_pin
out['pin_ok'] = (want_pin is None or want_pin == sha)
out['magic'] = magic.decode('latin-1')
e = 'little' if magic == b'hsqs' else 'big'
out['superblock_endian'] = 'big' if e == '>' else 'little'
u32 = lambda o: int.from_bytes(sb[o:o + 4], e)
u64 = lambda o: int.from_bytes(sb[o:o + 8], e)
out['inodes'] = u32(4)
out['mkfs_time'] = u32(8)
out['block_size'] = u32(12)
out['compression'] = int.from_bytes(sb[20:22], e)
out['major'] = int.from_bytes(sb[28:30], e)
out['minor'] = int.from_bytes(sb[30:32], e)
out['bytes_used'] = u64(40)
out['inode_table_start'] = u64(64)
out['directory_table_start'] = u64(72)
out['version_v4'] = (out['major'], out['minor']) == (4, 0)
out['avm_marker'] = out['mkfs_time'] == out['bytes_used']
out['length_equals_bytes_used'] = out['bytes_used'] == size
its = out['inode_table_start']
dts = out['directory_table_start']
with open(path, 'rb') as fh:
    fh.seek(its)
    hdr = fh.read(2)
out['meta_header_hex'] = hdr.hex()
le = int.from_bytes(hdr, 'little')
be = int.from_bytes(hdr, 'big')
out['meta_len_le'] = le & 0x7fff
out['meta_len_be'] = be & 0x7fff
out['meta_le_in_range'] = 0 < (le & 0x7fff) <= 8192
out['meta_be_in_range'] = 0 < (be & 0x7fff) <= 8192
out['le_identity'] = its + 2 + (le & 0x7fff) == dts
out['be_identity'] = its + 2 + (be & 0x7fff) == dts
if out['meta_le_in_range'] and not out['meta_be_in_range']:
    signal = 'le-only'
elif out['le_identity']:
    signal = 'identity'
else:
    signal = 'none'
out['meta_signal'] = signal
out['layout_le'] = signal in ('le-only', 'identity')
out['ok'] = (out['pin_ok'] and out['magic'] == 'sqsh' and out['version_v4']
             and out['avm_marker'] and out['length_equals_bytes_used'] and out['layout_le'])
print(json.dumps(out, indent=1, sort_keys=True))
