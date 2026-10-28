#!/usr/bin/env python3
"""R44W2C1Pins: re-derive the four frozen C1 carrier pins and their v1/v2 superblocks.

Read-only. Parses the 32-byte unblob SquashFSv1Handler struct (S112: squashfs.py:124-140)
and the legacy squashfs-tools squashfs_compat.h:38-64 fields that follow it.
No lane writes.
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

ROOT = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
SPEC = os.path.join(ROOT, 'tools/round-44/carriers.json')
COUNTER = os.path.join(ROOT, 'tools/round-44/c1-counter.py')

# squashfs_compat.h field offsets (packed struct, see :38-64)
LEGACY = [
    ('s_magic', 0, 4), ('inodes', 4, 4), ('bytes_used_2', 8, 4),
    ('uid_start_2', 12, 4), ('guid_start_2', 16, 4),
    ('inode_table_start_2', 20, 4), ('directory_table_start_2', 24, 4),
    ('s_major', 28, 2), ('s_minor', 30, 2),
    ('block_size_1', 32, 2), ('block_log', 34, 2), ('flags', 36, 1),
    ('no_uids', 37, 1), ('no_guids', 38, 1), ('mkfs_time', 39, 4),
    ('root_inode', 43, 8), ('block_size', 51, 4), ('fragments', 55, 4),
]

# SQUASHFS_* flag bits (squashfs_fs.h / squashfs_compat.h)
FLAG_BITS = {
    'NOI': 0, 'NOD': 1, 'CHECK': 2, 'NOF': 3, 'NO_FRAG': 4,
    'ALWAYS_FRAG': 5, 'DUPLICATE': 6, 'EXPORT': 7, 'NOX': 8,
    'COMP_OPT': 9, 'NOID': 10, 'NO_LZMA': 11,
}


def u(raw, off, width, endian):
    return int.from_bytes(raw[off:off + width], 'big' if endian == 'be' else 'little')


def decode(raw, endian):
    out = {}
    for name, off, width in LEGACY:
        out[name] = u(raw, off, width, endian)
    return out


def flag_names(value):
    return [k for k, bit in FLAG_BITS.items() if value & (1 << bit)]


def main():
    spec = json.load(open(SPEC))
    layout = spec['superblock_layout']
    target_ids = spec['scope']['target_ids']
    # load the frozen counter as a module (main is __main__-guarded)
    s = importlib.util.spec_from_file_location('c1counter', COUNTER)
    mod = importlib.util.module_from_spec(s)
    s.loader.exec_module(mod)

    report = {'spec_sha256': hashlib.sha256(open(SPEC, 'rb').read()).hexdigest(),
              'counter_sha256': hashlib.sha256(open(COUNTER, 'rb').read()).hexdigest(),
              'superblock_layout_frozen': layout,
              'counter_SB_SIZE': mod.SB_SIZE,
              'counter_SB_FIELDS': [list(f) for f in mod.SB_FIELDS],
              'counter_reads_flags': any(f[0] == 'flags' for f in mod.SB_FIELDS),
              'carriers': {}}
    failures = []
    for c in spec['carriers']:
        cid = c['id']
        path = os.path.join(ROOT, c['path'])
        raw = open(path, 'rb').read()
        sha = hashlib.sha256(raw).hexdigest()
        # endianness strictly from the magic, as the counter does
        endian = {'hsqs': 'le', 'sqsh': 'be'}.get(raw[0:4].decode('latin1'))
        d = decode(raw, endian) if endian else {}
        wrong = decode(raw, 'be' if endian == 'le' else 'le') if endian else {}
        its, dts, bu = d.get('inode_table_start_2'), d.get('directory_table_start_2'), d.get('bytes_used_2')
        meta = None
        if isinstance(its, int) and its + 2 <= len(raw):
            hdr = u(raw, its, 2, endian)
            length = hdr & ~0x8000
            body = raw[its + 2:its + 2 + length]
            meta = {
                'header_hex': raw[its:its + 2].hex(),
                'header_value': hdr,
                'length': length,
                'uncompressed_bit': bool(hdr & 0x8000),
                'body_first2_hex': body[:2].hex(),
                'body_sha256': hashlib.sha256(body).hexdigest(),
                'chain_lands': its + 2 + length == dts,
            }
        # counter's own probe, with the frozen entry as expectation
        probe = mod.layout_probe(raw, c)
        # frozen expectations from carriers.json
        frozen = {'sha256': c['sha256'], 'size': c['size'], 's_major': c['s_major'],
                  's_minor': c['s_minor'], 'endian': c.get('endian', c.get('endianness')),
                  'handler': c['handler'], 'compression': c['compression'],
                  'expected_regular': c['expected_regular']}
        oracle_members = c['oracle']['members']
        tree_lines = ''.join('%s\t%s\n' % (m['path'], m['sha256'])
                             for m in sorted(oracle_members, key=lambda m: m['path'].encode()))
        tree_digest = hashlib.sha256(tree_lines.encode()).hexdigest()
        checks = {
            'sha256_matches': sha == frozen['sha256'],
            'size_matches': len(raw) == frozen['size'],
            'magic_matches_endian': {'le': b'hsqs', 'be': b'sqsh'}[frozen['endian']] == raw[0:4],
            's_major_matches': d.get('s_major') == frozen['s_major'],
            's_minor_matches': d.get('s_minor') == frozen['s_minor'],
            'handler_matches_major': {1: 'squashfs_v1', 2: 'squashfs_v2'}[d['s_major']] == frozen['handler'],
            'bytes_used_at_8_matches_frozen_layout': d.get('bytes_used_2') == c['oracle']['superblock_info']['probe_v1v2']['bytes_used'],
            'regular_member_count': len(oracle_members) == frozen['expected_regular'],
            'oracle_tree_digest_matches': tree_digest == c['oracle']['output_tree_digest'],
            'counter_layout_probe_ok': bool(probe.get('ok')),
        }
        report['carriers'][cid] = {
            'path': c['path'], 'sha256': sha, 'size': len(raw),
            'frozen': frozen, 'decoded': d, 'wrong_endian_decode': wrong,
            'flags_hex': raw[36:37].hex(), 'flags_value': raw[36],
            'flags_set_bits': flag_names(raw[36]),
            'nod_bit_clear': not (raw[36] & (1 << FLAG_BITS['NOD'])),
            'block_size_1': d.get('block_size_1'), 'block_log': d.get('block_log'),
            'metadata': meta, 'counter_probe': probe,
            'oracle_tree_digest_recomputed': tree_digest,
            'checks': checks,
        }
        failures.extend('%s: %s' % (cid, k) for k, v in checks.items() if not v)
    # spec-level: is every frozen target id present as a carrier, and is v2.1 excluded?
    got_ids = [c['id'] for c in spec['carriers']]
    report['target_ids'] = target_ids
    report['ids_ok'] = sorted(got_ids) == sorted(target_ids)
    if not report['ids_ok']:
        failures.append('carrier id set != scope.target_ids')
    report['failures'] = failures
    print(json.dumps(report, indent=1, sort_keys=True))
    return 0 if not failures else 1


if __name__ == '__main__':
    sys.exit(main())
