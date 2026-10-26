#!/usr/bin/env python3
"""R41CritC2Draft probe: can REA 6.5.0 emit a COMBINED gap set on one carrier,
and what does a refused extract_firmware run look like?

Builds two carriers with the round-40 generator's own writer + corruption
recipes, runs REA extract-firmware once each, and prints the feature vector the
round-40 v2 table grammar would read.
"""
import contextlib
import importlib.util
import io
import json
import os
import shutil
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
GEN = os.path.join(LANE, 'tools/round-40/heldout-gen-v2.py')
WRITER = os.path.join(LANE, 'tools/round-39/gen-squashfs.py')
OUT = os.path.abspath(sys.argv[1])
SEED = sys.argv[2] if len(sys.argv) > 2 else 'deadbeefdeadbeef'

spec = importlib.util.spec_from_file_location('h', GEN)
h = importlib.util.module_from_spec(spec)
sys.modules['h'] = h
spec.loader.exec_module(h)


def features(data):
    """The round-40 v2 grammar's feature extraction, verbatim in intent."""
    nr = data.get('normalized_result') or {}
    chunks = nr.get('chunks') or []
    gaps = nr.get('extraction_gaps') or []
    diags = nr.get('diagnostics') or []
    be = 'n/a'
    for d in diags:
        rep = d.get('report') or {}
        cmd = rep.get('command')
        if isinstance(cmd, str) and cmd:
            be = 'yes' if ' -be ' in ' ' + cmd + ' ' else 'no'
    sr = any(d.get('kind') == 'MaliciousSymlinkRemoved' or
             (d.get('report') or {}).get('kind') == 'MaliciousSymlinkRemoved'
             for d in diags)
    return {
        'operation': data.get('operation'),
        'provider': (data.get('provider') or {}).get('id'),
        'handlers': sorted({c.get('handler') for c in chunks if c.get('handler')}),
        'chunk_count': len(chunks),
        'gap_kinds': sorted({g.get('kind') for g in gaps}),
        'gap_count': len(gaps),
        'deps': sorted({d for g in gaps for d in (g.get('dependencies') or [])}),
        'be_flag': be,
        'symlink_removed': sr,
        'published_files': len(nr.get('files') or []),
        'max_depth': (data.get('parameters') or {}).get('max_depth'),
        'coverage': nr.get('coverage'),
        'unpublished_entries': [u.get('relative_path') for u in (nr.get('unpublished_entries') or [])],
        'depth_limited_paths': nr.get('depth_limited_paths'),
        'diagnostic_kinds': sorted({d.get('kind') for d in diags}),
        'diag_reports': [(d.get('kind'), (d.get('report') or {}).get('kind'),
                          ((d.get('report') or {}).get('command') or '')[:90]) for d in diags],
    }


def main():
    os.makedirs(OUT, exist_ok=True)
    scratch = os.path.join(OUT, 'scratch')
    os.makedirs(scratch, exist_ok=True)
    h.WRITER_PATH = WRITER
    writer = h.load_writer(WRITER)
    h.install_block_encoder(writer)
    h.OUT_DIR = OUT
    h.RECIPES['probe-partial-in-tree'] = dict(
        label='partial-body-failure', endian='be', arm='after', comp='gzip',
        tree='random', content='pattern', symlinks=('in-tree',),
        corruption='partial')
    h.RECIPES['probe-mixed-partial'] = dict(
        label='partial-body-failure', endian='be', arm='after', comp='gzip',
        tree='random', content='pattern', symlinks=('escaping', 'in-tree'),
        corruption='partial')
    classes = ['probe-partial-in-tree', 'probe-mixed-partial']
    build_set = h.build_set
    built = build_set(SEED, classes, writer, OUT, scratch)
    carriers = built[1]
    report = {'seed': SEED, 'carriers': []}
    for entry in carriers:
        rec = h.run_rea(entry, scratch, False, False)
        path = os.path.join(OUT, entry['id'], 'envelope.json')
        row = {'id': entry['id'], 'class': entry['class'],
               'carrier_sha256': entry['sha256'],
               'rea_exit': rec.get('exit_code'), 'ok': rec.get('ok'),
               'rea_error': rec.get('error')}
        if os.path.exists(path):
            data = json.load(open(path, encoding='utf-8'))
            row['features'] = features(data)
            row['envelope_sha256'] = h.sha256_file(path)
        report['carriers'].append(row)
    # A refused run: file budget too small for the tree
    entry = carriers[0]
    carrier = os.path.join(OUT, entry['carrier'])
    import subprocess
    work = os.path.join(scratch, 'rea-refused')
    os.makedirs(work)
    outdir = os.path.join(work, 'out')
    env = h.rea_env('after')
    cmd = ['npx', '-y', h.REA_PACKAGE, 'extract-firmware', '--format', 'json',
           '--full-output', '--max-output-files', '1', carrier, outdir]
    proc = subprocess.run(cmd, cwd=work, env=env, capture_output=True, text=True)
    refused = {'argv': cmd, 'exit_code': proc.returncode,
               'stdout_head': proc.stdout[:1500], 'stderr_head': proc.stderr[-800:]}
    full = h._parse_stdout(proc.stdout)
    if full is not None:
        data, sha, shape = h._envelope_parts(full)
        refused['parsed'] = bool(data)
        refused['shape'] = shape
        if data is not None:
            refused['features'] = features(data)
            with open(os.path.join(OUT, 'refused-envelope.json'), 'w',
                      encoding='utf-8') as fh:
                json.dump(full, fh, indent=1)
    refused['ok_flag'] = None if full is None else full.get('ok')
    report['refused_run'] = refused
    with open(os.path.join(OUT, 'report.json'), 'w', encoding='utf-8') as fh:
        json.dump(report, fh, indent=1)
        fh.write('\n')
    print(json.dumps(report, indent=1))


main()
