#!/usr/bin/env python3
"""Summarize and validate a SquashFS v4 AVM member superblock."""
import argparse
import json
import os
import struct
import sys


def inspect(path):
    size = os.path.getsize(path)
    with open(path, 'rb') as stream:
        raw = stream.read(48)
    magic_raw = raw[:4]
    magic = magic_raw.decode('ascii', errors='replace')
    if len(raw) < 48 or magic_raw not in (b'hsqs', b'sqsh'):
        return {'magic': magic, 'byte_order': None, 'version': None,
                'compression_id': None, 'block_size': None, 'mkfs_time': None,
                'bytes_used': None, 'avm_marker': False,
                'bytes_used_le_file_size': None}
    endian = '<' if magic_raw == b'hsqs' else '>'
    mkfs, = struct.unpack(endian + 'I', raw[8:12])
    block_size, = struct.unpack(endian + 'I', raw[12:16])
    compression_id, = struct.unpack(endian + 'H', raw[20:22])
    major, minor = struct.unpack(endian + 'HH', raw[28:32])
    bytes_used, = struct.unpack(endian + 'Q', raw[40:48])
    return {'magic': magic, 'byte_order': 'little' if endian == '<' else 'big',
            'version': f'{major}.{minor}', 'compression_id': compression_id,
            'block_size': block_size, 'mkfs_time': mkfs, 'bytes_used': bytes_used,
            'avm_marker': mkfs == bytes_used,
            'bytes_used_le_file_size': bytes_used <= size}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--allow-nonavm', action='store_true',
                        help='waive AVM validation for control carriers; record waiver in JSON')
    parser.add_argument('member')
    args = parser.parse_args()
    try:
        result = inspect(args.member)
    except OSError as exc:
        print(json.dumps({'error': str(exc)}, sort_keys=True))
        return 2
    ok = (result['magic'] == 'hsqs' and result['version'] == '4.0' and
          result['compression_id'] == 4 and result['avm_marker'] is True and
          result['bytes_used_le_file_size'] is True)
    if args.allow_nonavm and not ok:
        result['waiver'] = {'allowed': True, 'reason': 'control carrier non-AVM superblock'}
        ok = True
    print(json.dumps(result, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
