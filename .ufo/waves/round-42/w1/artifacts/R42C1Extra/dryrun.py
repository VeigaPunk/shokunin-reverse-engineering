#!/usr/bin/env python3
"""Reproduce the R42C1Extra end-to-end dry run on real lane documents.

A sandbox clone of the lane at HEAD is given a synthetic round-42 landing (one
external carrier whose bytes are synthetic, tables produced by a STAND-IN oracle,
the entry, a new SOURCES row, the `Round-42 frontier note`) and then the gate is
scored green and against five red variants. The oracle tool is a stand-in on
purpose: it proves the wiring and the document bindings on real lane bytes, not the
v3 oracle chain (that is `c1-extra.py --oracle-check`).

    python3 dryrun.py --lane /path/to/kaidoku-shokunin --tool ./c1-extra.py \\
        --scratch /fast/scratch/hyaku/kaidoku-r42/<seat> --out OUTDIR

Writes one receipt JSON per scored revision into OUTDIR and prints a summary.
Nothing is written into the lane: only the clone under --scratch is committed to.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

BASE = 'c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c'
GREEN_NOTE = ('Round-42 frontier note, 2026-10-26: SquashFS v1-v3 chunks now extract '
              'through the `squashfs_v3` handler family (`squashfs_v3`, `_ddwrt`, '
              '`_broadcom`, `_nonstandard`, `_adaptive`); the Frontier text for v1-v3 is '
              'superseded for the handler family measured here, while v1/v2 images and '
              'v4 Broadcom bodies stay Frontier — see ## Round-42 additions to Core '
              '(`2026-10-26-r42-squashfs-v3-core`).\n')
ENTRY_TEXT = """---
title: SquashFS v1-v3 through REA extract-firmware
---
source: S130 — https://example.invalid/dryrun — the carrier publisher's identity row (dry run; stand-in)
source: S112 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py — the v3 handler classes

# SquashFS v1-v3 (dry run of the round-42 landing text)
"""
V4_ONLY_NOTE = ('Round-42 frontier note, 2026-10-26: the `squashfs_v4` handler family '
                'supersedes the Frontier text; v1/v2 images and v4 Broadcom bodies stay '
                'Frontier — see ## Round-42 additions to Core '
                '(`2026-10-26-r42-squashfs-v3-core`).\n')
ENTRY = 'corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md'
PROVINCE = 'PROVINCE.md'
TABLE_O = 'corpus/evidence/round-42/c1/D1/oracle.tsv'
CARRIERS = '.ufo/waves/round-42/c1/carriers.json'
FROZEN_SELF = 'tools/round-42/c1-extra.py'


def git(lane, *args):
    return subprocess.run(['git', '-C', lane] + list(args), check=True,
                          capture_output=True, text=True).stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    for k in ('--lane', '--tool', '--scratch', '--out'):
        ap.add_argument(k, required=True)
    a = ap.parse_args()
    os.makedirs(a.scratch, exist_ok=True)
    os.makedirs(a.out, exist_ok=True)
    spec = importlib.util.spec_from_file_location('c1x', a.tool)
    c1x = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(c1x)

    clone = os.path.join(a.scratch, 'lane')
    if os.path.exists(clone):
        raise SystemExit('clone path exists: ' + clone)
    subprocess.run(['git', 'clone', '-q', '--shared', a.lane, clone], check=True)
    if os.path.realpath(git(clone, 'rev-parse', '--show-toplevel')) != \
            os.path.realpath(clone):
        raise SystemExit('clone toplevel mismatch')

    def put(rel, data):
        p = os.path.join(clone, rel)
        os.makedirs(os.path.dirname(p) or clone, exist_ok=True)
        with open(p, 'wb') as fh:
            fh.write(data if isinstance(data, bytes) else data.encode())

    def read(rel):
        return open(os.path.join(clone, rel), 'rb').read()

    def commit(msg):
        git(clone, 'add', '-A')
        git(clone, '-c', 'user.name=fx', '-c', 'user.email=fx@fx', 'commit', '-q',
            '-m', msg)
        return git(clone, 'rev-parse', 'HEAD')

    # carrier cache + stand-in oracle
    cache = os.path.join(a.scratch, 'cache')
    os.makedirs(cache, exist_ok=True)
    image = b'SQF3' + b'dry-run-rootfs' * 100
    pin = hashlib.sha256(image).hexdigest()
    open(os.path.join(cache, pin + '.bin'), 'wb').write(image)
    stub = os.path.join(a.scratch, 'stand-in-oracle.py')
    open(stub, 'w').write(c1x.stub_oracle('flag'))
    tabdir = os.path.join(a.scratch, 'stand-in-out')
    os.makedirs(tabdir, exist_ok=True)
    p = subprocess.run([sys.executable, stub, os.path.join(cache, pin + '.bin'),
                        '--out', tabdir], capture_output=True)
    if p.returncode:
        raise SystemExit('stand-in oracle failed: %r' % p.stderr)
    tab_o = open(os.path.join(tabdir, 'oracle.tsv'), 'rb').read()
    tab_n = open(os.path.join(tabdir, 'nonregular.tsv'), 'rb').read()

    carriers = {'claim': 'R42-C1', 'target': 1, 'projection': 'plus-extractor',
                'carriers': [{'id': 'D1', 'sha256': pin, 'kind': 'distribution',
                              'external': {'url': 'https://example.invalid/dryrun.bin',
                                           'image_sha256': '0' * 64,
                                           'carve': {'offset': 0,
                                                     'length': len(image)},
                                           'product': 'dry-run stand-in'},
                              'oracle': 'corpus/evidence/round-42/c1/D1/oracle.tsv',
                              'nonregular':
                                  'corpus/evidence/round-42/c1/D1/nonregular.tsv'}]}
    put(CARRIERS, json.dumps(carriers, indent=1))
    put('corpus/evidence/round-42/c1/D1/oracle.tsv', tab_o)
    put('corpus/evidence/round-42/c1/D1/nonregular.tsv', tab_n)
    put('tools/round-42/sqfs3-oracle.py', open(stub, 'rb').read())
    freeze = commit('freeze: carriers + oracle tool + tables')
    put(ENTRY, ENTRY_TEXT)
    lines = read('corpus/SOURCES.md').decode().splitlines(True)
    idx = max(i for i, l in enumerate(lines) if l.startswith('| S129 |'))
    lines.insert(idx + 1, '| S130 | dry-run carrier publisher identity | dataset | A | '
                          'scope | anchor | teaches | mined | 2026-10-26 | on-release | '
                          '%s |\n' % ENTRY)
    put('corpus/SOURCES.md', ''.join(lines))
    with open(os.path.join(clone, PROVINCE), 'ab') as fh:
        fh.write(('\n' + GREEN_NOTE).encode())
    green = commit('landing: entry + SOURCES row + round-42 frontier note')

    results = []

    def score(tag, rev, fz=freeze, expect=None):
        out = os.path.join(a.out, 'dryrun-%s.json' % tag)
        p = subprocess.run([sys.executable, a.tool, '--root', clone, '--rev', rev,
                            '--freeze', fz, '--base', BASE, '--carrier-cache', cache,
                            '--json-out', out], capture_output=True, text=True)
        d = json.load(open(out))
        row = {'tag': tag, 'rev': rev, 'exit': p.returncode, 'met': d.get('met'),
               'failing': sorted(k for k, v in (d.get('bindings') or {}).items()
                                 if v is not True),
               'counter_matches_rev': d.get('counter_matches_rev'),
               'counter_pin_ok': d.get('counter_pin_ok'),
               'expected_met': expect, 'ok': d.get('met') == expect,
               'receipt': os.path.basename(out)}
        if 'detail' in d and 'oracle_rederived' in d['detail']:
            row['oracle_detail'] = {
                k: {kk: vv for kk, vv in v.items()
                    if kk in ('match', 'fatal', 'bytes', 'oracle_exit')}
                for k, v in d['detail']['oracle_rederived'].items()
                if isinstance(v, dict)}
        results.append(row)
        return d

    score('green', green, expect=True)

    put(PROVINCE, read(PROVINCE).replace(
        b'v1/v2 images and v4 Broadcom bodies stay Frontier',
        b'v4 Broadcom bodies stay Frontier'))
    score('note-omits-v1v2', commit('note drops the v1/v2 residual'), expect=False)
    # a note that names only the v4 family (the explicit red shape for round 42)
    put(PROVINCE, b''.join(read(PROVINCE).splitlines(True)[:-1]) + V4_ONLY_NOTE.encode())
    score('note-names-v4-only', commit('note names v4 only'), expect=False)
    put(PROVINCE, b''.join(read(PROVINCE).splitlines(True)[:-1]) + GREEN_NOTE.encode())
    score('green-after-note-restore', commit('green note restored'), expect=True)

    rows = tab_o.decode().splitlines()
    rel, digest, size = rows[0].split('\t')
    rows[0] = '\t'.join((rel, ('0' if digest[0] != '0' else '1') + digest[1:], size))
    put(TABLE_O, '\n'.join(rows) + '\n')
    score('oracle-row-edited', commit('frozen oracle row sha256 flipped'), expect=False)
    put(TABLE_O, tab_o)
    score('green-after-table-restore', commit('oracle table restored'), expect=True)

    spec2 = json.loads(json.dumps(carriers))
    spec2['carriers'][0]['oracle'] = 'corpus/evidence/round-41/c1/D1/oracle.tsv'
    put(CARRIERS, json.dumps(spec2, indent=1))
    relabelled = commit('relabelled oracle path (own freeze)')
    score('oracle-path-relabelled', relabelled, fz=relabelled, expect=False)
    put(CARRIERS, json.dumps(carriers, indent=1))
    commit('carriers restored')

    put(ENTRY, ENTRY_TEXT.replace('source: S130', 'source: S129'))
    score('entry-cites-S129', commit('entry cites the base-highest id'),
          expect=False)
    put(ENTRY, ENTRY_TEXT)
    commit('entry restored')

    put(FROZEN_SELF, open(a.tool, 'rb').read())
    d = score('counter-installed-at-rev', commit('counter installed at its frozen path'),
              expect=True)
    results.append({'tag': 'counter-matches-rev', 'rev': d['revision'],
                    'counter_sha256': d['counter_sha256'],
                    'counter_at_rev_sha256': d['counter_at_rev_sha256'],
                    'counter_matches_rev': d['counter_matches_rev'],
                    'counter_pin_ok': d['counter_pin_ok'], 'ok': True,
                    'expected': 'counter_matches_rev true and met true'})
    results[-1]['ok'] = (d['counter_matches_rev'] is True and d['met'] is True
                         and d['counter_sha256'] == d['counter_at_rev_sha256'])
    put(FROZEN_SELF, open(a.tool, 'rb').read() + b'\n# drift\n')
    d = score('counter-drifted-at-rev', commit('counter modified after installation'),
              expect=False)
    results.append({'tag': 'counter-drifted-pin', 'rev': d['revision'],
                    'met': d['met'], 'bindings': d['bindings'],
                    'counter_matches_rev': d['counter_matches_rev'],
                    'counter_pin_ok': d['counter_pin_ok'], 'ok': True,
                    'expected': 'counter_pin_ok false, all bindings true, met false'})
    results[-1]['ok'] = (d['counter_matches_rev'] is False
                         and d['counter_pin_ok'] is False and d['met'] is False
                         and all(d['bindings'].values()))
    put(FROZEN_SELF, open(a.tool, 'rb').read())
    score('green-final', commit('counter restored'), expect=True)

    summary = {'lane': os.path.abspath(a.lane), 'clone': clone, 'base': BASE,
               'freeze': freeze, 'landing': green, 'carrier_pin': pin,
               'tool_sha256': hashlib.sha256(open(a.tool, 'rb').read()).hexdigest(),
               'results': results}
    with open(os.path.join(a.out, 'dryrun-summary.json'), 'w') as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)
    print(json.dumps(summary, indent=1, sort_keys=True))
    bad = [r['tag'] for r in results if r.get('ok') is not True]
    print('DRYRUN tags=%d ok=%d bad=%s' % (len(results),
                                          len(results) - len(bad), bad))
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(main())
