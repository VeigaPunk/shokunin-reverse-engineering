#!/usr/bin/env python3
"""R39-C1 counter reconnaissance: run c1-counter.py against REAL round-38 receipts.

Builds a throwaway git repo under scratch that freezes the counter's own controls
(K1-K4 real carrier bytes, real oracle.tsv, a symlinks.tsv derived from the round-37
src trees and the round-38 receipts, the doc bindings) and then byte-copies the
committed round-38 after.json receipts into corpus/evidence/round-39/c1/<id>/ after
the freeze. No REA run, no K5/K6, nothing written inside the lane.

Expected: exit 1; every per-carrier clause true for K1-K4 except run_provenance_ok
(the receipts name a kaidoku-r38 output_directory), which is what refuses the
"strong copy" control (real K1-K4 receipts + genuine K5/K6 receipts would otherwise
reach 6/6).
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
ART = f'{LANE}/.ufo/waves/round-39/w1/artifacts/R39C1Counter'
PKG65 = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
S = '/fast/scratch/hyaku/kaidoku-r39/R39C1Counter/sim'
ENTRY = 'corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md'
STEM = '2026-10-26-r39-be-squashfs-v4-core'


def git(*args):
    return subprocess.run(['git', '-C', S, *args], capture_output=True, text=True)


def commit(msg):
    r = git('-c', 'user.name=fx', '-c', 'user.email=fx@fx', 'commit', '-qm', msg)
    if r.returncode != 0:
        raise SystemExit(r.stderr)
    return git('rev-parse', 'HEAD').stdout.strip()


def write(path, data):
    full = os.path.join(S, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'wb').write(data if isinstance(data, bytes) else data.encode())


def main():
    shutil.rmtree(S, ignore_errors=True)
    os.makedirs(S)
    subprocess.run(['git', 'init', '-q', S], check=True)
    top = subprocess.run(['git', '-C', S, 'rev-parse', '--show-toplevel'],
                         capture_output=True, text=True).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(S):
        raise SystemExit('fixture toplevel mismatch')

    oradir = f'{LANE}/corpus/evidence/round-37/c1'
    r38 = f'{LANE}/corpus/evidence/round-38/c1'
    # class labels as frozen by seat R39C1SymlinkK1K4 (symlinks-K*.tsv)
    links = {'K1': 'link-to-hello\t../hello.txt\tescaping\n',
             'K2': 'var/lib/run-link\t../../a/run.sh\tin-tree\n',
             'K3': '', 'K4': ''}
    carriers = []
    for k in ('K1', 'K2', 'K3', 'K4'):
        d = f'{oradir}/{k}'
        cname = 'carrier.sqsh' if os.path.exists(f'{d}/carrier.sqsh') else 'carrier.bin'
        blob = open(f'{d}/{cname}', 'rb').read()
        cp = f'corpus/evidence/round-39/c1/{k}/{cname}'
        write(cp, blob)
        write(f'corpus/evidence/round-39/c1/{k}/oracle.tsv', open(f'{d}/oracle.tsv', 'rb').read())
        write(f'corpus/evidence/round-39/c1/{k}/symlinks.tsv', links[k])
        carriers.append({'id': k, 'path': cp, 'sha256': hashlib.sha256(blob).hexdigest(),
                         'oracle': f'corpus/evidence/round-39/c1/{k}/oracle.tsv',
                         'symlinks': f'corpus/evidence/round-39/c1/{k}/symlinks.tsv',
                         'receipt': f'corpus/evidence/round-39/c1/{k}/after.json'})
    write('.ufo/waves/round-39/c1/carriers.json',
          json.dumps({'claim': 'R39-C1', 'carriers': carriers}, indent=1))
    write('tools/round-27/xpin-attribute.mjs',
          open(f'{LANE}/tools/round-27/xpin-attribute.mjs', 'rb').read())
    write('tools/round-39/c1-counter.py', open(f'{ART}/c1-counter.py', 'rb').read())
    write('tools/round-39/c1-run.sh', b'#!/bin/sh\nexit 0\n')
    write('plans/round-39-claims.md', open(f'{LANE}/plans/round-39-claims.md', 'rb').read())
    write('PROVINCE.md',
          f'# P\n\n## Round-39 additions to Core\n\n| Surface | a | Entry |\n|---|---|---|\n'
          f'| `squashfs_v4_be` | x | `{ENTRY}` |\n\n## Next\n\n'
          f'- Round-39 frontier note, 2026-10-26: the Frontier bullet big-endian part is '
          f'superseded by `{STEM}`.\n')
    write(ENTRY, '# E\n\nsource: S1121 - unblob 26.6.4 sanitiser + REA 6.5.0 gap code\n')
    write('corpus/SOURCES.md',
          '# S\n\n## Registry\n\n| id | source | kind | tier | scope | anchor | teaches '
          '| status | opened | recheck | used-by |\n'
          '|---|---|---|---|---|---|---|---|---|---|---|\n'
          f'| S1121 | unblob 26.6.4 symlink sanitiser | code | A | s | a | t | mined '
          f'| 2026-10-26 | on-release | {ENTRY} |\n')
    write('corpus/README.md',
          f'# R\n\n## Coverage map\n\n| a | b |\n|---|---|\n| x | `{STEM}` |\n\n## Other\n')
    git('add', '-A')
    freeze = commit('freeze')
    for k in ('K1', 'K2', 'K3', 'K4'):
        write(f'corpus/evidence/round-39/c1/{k}/after.json',
              open(f'{r38}/{k}/after.json', 'rb').read())
    git('add', '-A')
    rev = commit('round-38 receipts byte-copied')

    out = f'{ART}/sim-round38-copy.json'
    r = subprocess.run(['python3', '-I', '-B', f'{ART}/c1-counter.py', '--root', S,
                        '--rev', rev, '--freeze', freeze, '--pkg65', PKG65,
                        '--json-out', out], capture_output=True, text=True,
                       env=dict(os.environ, HYAKU_SCRATCH='/fast/scratch/hyaku'))
    print(r.stdout.strip())
    print(r.stderr.strip(), file=sys.stderr)
    res = json.load(open(out))
    for k, v in res['carriers'].items():
        print(k, json.dumps({x: v[x] for x in ('carrier_pin_ok', 'subject_pin_ok', 'handler_ok',
                                               'chunks_ok', 'gaps_ok', 'escaping_ok',
                                               'evidence_id_ok', 'oracle_hits', 'oracle_files',
                                               'receipt_fresh', 'run_provenance_ok', 'matched')},
                            sort_keys=True))
    print('bindings_false', sorted(x for x in res['bindings']
                                   if res['bindings'][x] is False))
    print('spec_problems', res['carriers_spec_problems'])
    return r.returncode


if __name__ == '__main__':
    sys.exit(main())
