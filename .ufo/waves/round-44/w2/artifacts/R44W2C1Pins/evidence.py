#!/usr/bin/env python3
"""R44W2C1Pins evidence: frozen C1 carrier pins + v1/v2 superblock re-derivation.

Read-only over the lane. Writes nothing outside stdout. Every value is measured
from the lane blobs at the measured revision (55bcce69) and the worktree.
"""
import datetime
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

ROOT = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
REV = '55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac'
FREEZE = 'c48f8a4bfd449300c975668e59aae5b5538b6a84'
SPEC = os.path.join(ROOT, 'tools/round-44/carriers.json')
COUNTER = os.path.join(ROOT, 'tools/round-44/c1-counter.py')

# offsets of the packed legacy struct (squashfs_compat.h:38-64)
LEGACY = [('s_magic', 0, 4), ('inodes', 4, 4), ('bytes_used_2', 8, 4),
          ('uid_start_2', 12, 4), ('guid_start_2', 16, 4),
          ('inode_table_start_2', 20, 4), ('directory_table_start_2', 24, 4),
          ('s_major', 28, 2), ('s_minor', 30, 2), ('block_size_1', 32, 2),
          ('block_log', 34, 2), ('flags', 36, 1), ('no_uids', 37, 1),
          ('no_guids', 38, 1), ('mkfs_time', 39, 4), ('root_inode', 43, 8)]
FLAG_BITS = {'NOI': 0, 'NOD': 1, 'CHECK': 2, 'NOF': 3, 'NO_FRAG': 4,
             'ALWAYS_FRAG': 5, 'DUPLICATE': 6, 'EXPORT': 7, 'NOX': 8,
             'COMP_OPT': 9, 'NOID': 10, 'NO_LZMA': 11}


def u(raw, off, width, endian):
    return int.from_bytes(raw[off:off + width], 'big' if endian == 'be' else 'little')


def git(*args):
    p = subprocess.run(['git', '-C', ROOT] + list(args), capture_output=True)
    return p.returncode, p.stdout, p.stderr


def main():
    spec_bytes = open(SPEC, 'rb').read()
    spec = json.loads(spec_bytes)
    s = importlib.util.spec_from_file_location('c1counter', COUNTER)
    mod = importlib.util.module_from_spec(s)
    s.loader.exec_module(mod)

    ev = {
        'seat': 'R44W2C1Pins',
        'lane': ROOT, 'measured_rev': REV, 'freeze': FREEZE,
        'carriers_json_sha256_worktree': hashlib.sha256(spec_bytes).hexdigest(),
        'counter_sha256_worktree': hashlib.sha256(open(COUNTER, 'rb').read()).hexdigest(),
        'counter_SB_SIZE': mod.SB_SIZE,
        'counter_SB_FIELDS': [list(f) for f in mod.SB_FIELDS],
        'counter_reads_flags': any(f[0] == 'flags' for f in mod.SB_FIELDS),
        'frozen_layout': spec['superblock_layout'],
        'carriers': {}, 'mutations': {}, 'layout_counterfactual': {},
        'selftest_flags_coverage': {},
    }

    # carriers.json is frozen: same blob at REV as in the worktree
    rc, out, err = git('rev-parse', '%s:tools/round-44/carriers.json' % REV)
    ev['carriers_json_blob_at_rev'] = out.decode().strip()
    rc2, out2, _ = git('show', '%s:tools/round-44/carriers.json' % REV)
    ev['carriers_json_sha256_at_rev'] = hashlib.sha256(out2).hexdigest()
    rc3, out3, _ = git('rev-parse', '%s:tools/round-44/c1-counter.py' % REV)
    ev['counter_blob_at_rev'] = out3.decode().strip()

    for c in spec['carriers']:
        cid = c['id']
        path = os.path.join(ROOT, c['path'])
        rc, out, _ = git('show', '%s:%s' % (REV, c['path']))
        raw = out
        worktree = open(path, 'rb').read()
        endian = {'hsqs': 'le', 'sqsh': 'be'}[raw[0:4].decode('latin1')]
        dec = {n: u(raw, o, w, endian) for n, o, w in LEGACY}
        its, dts = dec['inode_table_start_2'], dec['directory_table_start_2']
        hdr = u(raw, its, 2, endian)
        length = hdr & ~0x8000
        body = raw[its + 2:its + 2 + length]
        pv = c['oracle']['superblock_info']['probe_v1v2']
        tree_lines = ''.join('%s\t%s\n' % (m['path'], m['sha256'])
                             for m in sorted(c['oracle']['members'],
                                             key=lambda m: m['path'].encode()))
        # physical extent of the header: first file-data byte after the superblock
        if c['s_major'] == 1:
            extent = raw.find(b'apple')
        else:
            extent = raw.find(b'\x78\xda', 51)   # first compressed data block
        checks = {
            'pin_at_rev_matches_frozen': hashlib.sha256(raw).hexdigest() == c['sha256'],
            'worktree_equals_rev_blob': raw == worktree,
            'size_matches': len(raw) == c['size'],
            'magic_is_frozen_endian_magic': raw[0:4] == {'le': b'hsqs', 'be': b'sqsh'}[endian],
            's_major_matches': dec['s_major'] == c['s_major'],
            's_minor_matches': dec['s_minor'] == c['s_minor'],
            'bytes_used_u32_at_8_matches_probe': dec['bytes_used_2'] == pv['bytes_used'],
            'handler_matches_major': {1: 'squashfs_v1', 2: 'squashfs_v2'}[dec['s_major']] == c['handler'],
            'regular_member_count_matches': len(c['oracle']['members']) == c['expected_regular'],
            'oracle_tree_digest_matches': hashlib.sha256(tree_lines.encode()).hexdigest() == c['oracle']['output_tree_digest'],
            'counter_layout_probe_ok': bool(mod.layout_probe(raw, c)['ok']),
        }
        ev['carriers'][cid] = {
            'path': c['path'], 'sha256_at_rev': hashlib.sha256(raw).hexdigest(),
            'frozen_pin': c['sha256'], 'size': len(raw),
            'decoded': dec, 'flags_hex': raw[36:37].hex(), 'flags_value': raw[36],
            'flags_bits_set': [k for k, b in FLAG_BITS.items() if raw[36] & (1 << b)],
            'nod_clear': not (raw[36] & 0x02),
            'metadata': {'header_hex': raw[its:its + 2].hex(), 'length': length,
                         'uncompressed': bool(hdr & 0x8000),
                         'body_first2_hex': body[:2].hex(),
                         'chain_lands': its + 2 + length == dts},
            'header_extent_first_data_byte': extent,
            'counter_probe': {'ok': mod.layout_probe(raw, c)['ok'],
                              'reason': mod.layout_probe(raw, c)['reason'],
                              'compression': mod.layout_probe(raw, c)['compression']},
            'checks': checks,
        }

        # counterfactual: flags NOD set while the pin is rebased over those bytes
        mut = bytearray(raw)
        mut[36] |= 0x02
        mut = bytes(mut)
        ent = dict(c)
        ent['sha256'] = hashlib.sha256(mut).hexdigest()
        ent['size'] = len(mut)
        ev['mutations'][cid] = {
            'flags_0x02_nod_set': {
                'pin_rebased_over_mutated_bytes': ent['sha256'],
                'carrier_pin_ok_if_so_pinned': hashlib.sha256(mut).hexdigest() == ent['sha256'],
                'layout_probe': {k: mod.layout_probe(mut, ent)[k]
                                 for k in ('ok', 'reason', 'compression')},
            },
            'no_mutation_baseline': {k: mod.layout_probe(raw, c)[k]
                                     for k in ('ok', 'reason', 'compression')},
        }

    # advisory detector vs the frozen layout shape
    def run_spec(sp):
        r = mod.carriers_spec(sp, 4)
        return {'problems': r[1], 'advisories': r[2]}
    import copy
    ev['layout_counterfactual']['frozen'] = run_spec(copy.deepcopy(spec))
    b = copy.deepcopy(spec)
    b['superblock_layout'].update({'bytes_used': [40, 8], 's_major': [0, 2], 'flags': [0, 1]})
    ev['layout_counterfactual']['wrong_list_shape'] = run_spec(b)
    d = copy.deepcopy(spec)
    d['superblock_layout']['bytes_used_offset'] = 40
    ev['layout_counterfactual']['bytes_used_offset_key'] = run_spec(d)

    # the selftest's own carrier model
    synth = mod.sb_v12(1, 'le')
    ev['selftest_flags_coverage'] = {
        'sb_v12_length': len(synth),
        'sb_v12_superblock_len': mod.SB_SIZE,
        'sb_v12_byte32_hex': synth[32:40].hex(),
        'sb_v12_byte36_hex': synth[36:37].hex(),
        'sb_v12_payload_starts_at': 32,
        'note': 'sb_v12 writes bytearray(SB_SIZE)=32 then b"block-payload-"; '
                'byte 36 of a synthetic carrier is payload ASCII, not flags',
        'counter_source_flags_occurrences': open(COUNTER, 'rb').read().lower().count(b'flags'),
    }
    print(json.dumps(ev, indent=1, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
