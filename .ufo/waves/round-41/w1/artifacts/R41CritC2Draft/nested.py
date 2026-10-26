#!/usr/bin/env python3
"""R41CritC2Draft probe 2.

(a) Can REA 6.5.0 emit `depth-limited` gaps at a small --max-depth, and can that
    co-occur with an `unpublished-entry` gap (the draft's depth-limited+mixed /
    depth-limited+in-tree classes)?
(b) Across several seeds, does a carrier with BOTH symlink kinds plus partial
    damage ever yield MaliciousSymlinkRemoved (SR=yes) TOGETHER with
    `extractor-failure` (the draft's `partial+mixed` class)?
"""
import importlib.util
import json
import os
import random
import shutil
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
GEN = os.path.join(LANE, 'tools/round-40/heldout-gen-v2.py')
WRITER = os.path.join(LANE, 'tools/round-39/gen-squashfs.py')
OUT = os.path.abspath(sys.argv[1])

spec = importlib.util.spec_from_file_location('h', GEN)
h = importlib.util.module_from_spec(spec)
sys.modules['h'] = h
spec.loader.exec_module(h)
h.WRITER_PATH = WRITER
writer = h.load_writer(WRITER)
h.install_block_encoder(writer)


def features(data):
    nr = data.get('normalized_result') or {}
    chunks = nr.get('chunks') or []
    gaps = nr.get('extraction_gaps') or []
    diags = nr.get('diagnostics') or []
    be = 'n/a'
    for d in diags:
        cmd = (d.get('report') or {}).get('command')
        if isinstance(cmd, str) and cmd:
            be = 'yes' if ' -be ' in ' ' + cmd + ' ' else 'no'
    sr = any((d.get('report') or {}).get('kind') == 'MaliciousSymlinkRemoved'
             for d in diags)
    return {'operation': data.get('operation'),
            'provider': (data.get('provider') or {}).get('id'),
            'handlers': sorted({c.get('handler') for c in chunks if c.get('handler')}),
            'gap_kinds': sorted({g.get('kind') for g in gaps}),
            'deps': sorted({x for g in gaps for x in (g.get('dependencies') or [])}),
            'be_flag': be, 'symlink_removed': sr,
            'published_files': len(nr.get('files') or []),
            'max_depth': (data.get('parameters') or {}).get('max_depth'),
            'depth_limited_paths': nr.get('depth_limited_paths') or [],
            'unpublished': [u.get('relative_path') for u in (nr.get('unpublished_entries') or [])],
            'chunk_depths': sorted({c.get('depth') for c in chunks if 'depth' in c})}


def run_rea(carrier, work, depth):
    os.makedirs(work, exist_ok=True)
    outdir = os.path.join(work, 'out-%d' % random.randrange(1 << 30))
    env = h.rea_env('after')
    cmd = ['npx', '-y', h.REA_PACKAGE, 'extract-firmware', '--format', 'json',
           '--full-output', '--max-depth', str(depth), carrier, outdir]
    proc = subprocess.run(cmd, cwd=work, env=env, capture_output=True, text=True)
    full = h._parse_stdout(proc.stdout)
    out = {'depth': depth, 'exit_code': proc.returncode,
           'ok': None if full is None else full.get('ok')}
    if full is None:
        out['stdout_head'] = proc.stdout[:400]
        return out
    data = full.get('data')
    if data is None:
        out['error'] = full.get('error')
        return out
    out['features'] = features(data)
    return out


def build_tree_with(root, files, links):
    os.makedirs(root)
    for rel, payload in files:
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as fh:
            fh.write(payload)
    for rel, target in links:
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        os.symlink(target, path)


def main():
    os.makedirs(OUT, exist_ok=True)
    report = {}

    # ---- (a) nested depth test -------------------------------------------
    inner_dir = os.path.join(OUT, 'inner')
    inner_img = os.path.join(OUT, 'inner.sqsh')
    build_tree_with(os.path.join(inner_dir, 'tree'),
                    [('inner_payload.bin', bytes(random.Random(7).randrange(256)
                                                 for _ in range(4096)))], [])
    writer.build_image(os.path.join(inner_dir, 'tree'), inner_img, 'le', 'gzip')
    outer_root = os.path.join(OUT, 'outer', 'tree')
    build_tree_with(outer_root,
                    [('nested/inner.sqsh', open(inner_img, 'rb').read()),
                     ('top.bin', b'A' * 2048)],
                    [('links/in_tree', '../../top.bin'),
                     ('links/escaping', '../../../etc/passwd')])
    outer_img = os.path.join(OUT, 'outer.sqsh')
    writer.build_image(outer_root, outer_img, 'le', 'gzip')
    report['nested'] = {'carrier_sha256': h.sha256_file(outer_img), 'runs': []}
    for depth in (1, 2, 3):
        try:
            report['nested']['runs'].append(
                run_rea(outer_img, os.path.join(OUT, 'work-nested', str(depth)), depth))
        except Exception as exc:  # noqa: BLE001
            report['nested']['runs'].append({'depth': depth, 'exception': repr(exc)})

    # ---- (b) partial + both link kinds, several seeds --------------------
    report['partial_mixed'] = []
    for i, seed in enumerate(['a1b2c3d4e5f60718', '1122334455667788',
                              '99aabbccddeeff00', '0f1e2d3c4b5a6978']):
        out_dir = os.path.join(OUT, 'pm%d' % i)
        scratch = os.path.join(out_dir, 'scratch')
        os.makedirs(scratch, exist_ok=True)
        h.OUT_DIR = out_dir
        h.RECIPES['probe-mixed-partial'] = dict(
            label='partial-body-failure', endian='be', arm='after', comp='gzip',
            tree='random', content='pattern', symlinks=('escaping', 'in-tree'),
            corruption='partial')
        manifest, carriers = h.build_set(seed, ['probe-mixed-partial'], writer,
                                        out_dir, scratch)
        entry = carriers[0]
        rec = {'seed': seed, 'carrier_sha256': entry['sha256'],
               'damage': entry['damage']}
        run = run_rea(os.path.join(out_dir, entry['carrier']),
                      os.path.join(out_dir, 'work'), 3)
        rec['run'] = run
        report['partial_mixed'].append(rec)

    with open(os.path.join(OUT, 'report2.json'), 'w', encoding='utf-8') as fh:
        json.dump(report, fh, indent=1)
        fh.write('\n')
    print(json.dumps(report, indent=1)[:6000])


main()
