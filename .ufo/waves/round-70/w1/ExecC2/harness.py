#!/usr/bin/env python3
"""Independent R70-C2 experiments; never imports or invokes seam-probe."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
SCRATCH = Path('/fast/scratch/hyaku/kaidoku-r70/ExecC2')
OUT = ROOT / '.ufo/waves/round-70/w1/ExecC2'
PKG = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
BASE = '5cc845ca88c90e3e8ceb816f75fe44ddb6758a6d'
FREEZE = '4737a542ae3b1b910d8fe43efbd572bc578b07c6'

def run(name, argv, env=None):
    p = subprocess.run(argv, cwd=SCRATCH, env=env, capture_output=True, text=True, timeout=1200)
    record = {'name': name, 'argv': [str(x) for x in argv], 'rc': p.returncode,
              'stdout': p.stdout, 'stderr': p.stderr, 'traceback': 'Traceback (most recent call last)' in p.stderr}
    try:
        record['payload'] = json.loads(p.stdout or p.stderr)
    except ValueError:
        record['payload'] = None
    (OUT / (name + '.json')).write_text(json.dumps(record, indent=2) + '\n')
    return record

def main():
    SCRATCH.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for name, rev, tool in [('base', BASE, 'tools/round-69/packed-elf.py'),
                            ('freeze', FREEZE, 'tools/round-70/packed-elf.py'),
                            ('battery', FREEZE, 'tools/round-70/mutation-check.py')]:
        data = subprocess.check_output(['git', '-C', str(ROOT), 'show', rev + ':' + tool])
        (SCRATCH / (name + '.py')).write_bytes(data)
        manifest[name] = {'revision': rev, 'path': tool, 'sha256': hashlib.sha256(data).hexdigest()}
    upx = SCRATCH / 'pinned-upx'
    shutil.copyfile('/usr/bin/upx', upx)
    upx.chmod(0o755)
    manifest['upx_sha256'] = hashlib.sha256(upx.read_bytes()).hexdigest()
    nodebin = SCRATCH / 'nodebin'
    nodebin.mkdir()
    node = nodebin / 'node'
    node.write_text('#!/bin/sh\nexit 7\n')
    node.chmod(0o755)
    bad = SCRATCH / 'exec-format-less'
    bad.write_text('not an executable format\n')
    bad.chmod(0o755)
    jobs = []
    logs = {}
    for world, rev in [('base', BASE), ('freeze', FREEZE)]:
        blob = SCRATCH / (world + '.py')
        jobs.append((world + '-selftest', [sys.executable, '-I', '-B', str(blob), '--selftest'], None))
        for scenario in ['impostor', 'broken-node', 'exec-format', 'pinned-copy']:
            work = SCRATCH / (world + '-' + scenario)
            work.mkdir()
            packer = upx
            env = None
            if scenario == 'impostor':
                log = work / 'executed.log'
                impostor = work / 'impostor'
                impostor.write_text('#!/bin/sh\nprintf executed >> "' + str(log) + '"\nprintf "upx 5.2.0\\n"\n')
                impostor.chmod(0o755)
                packer = impostor
                logs[world + '-' + scenario] = log
            elif scenario == 'broken-node':
                env = dict(os.environ, PATH=str(nodebin) + os.pathsep + os.environ['PATH'])
            elif scenario == 'exec-format':
                packer = bad
            argv = [sys.executable, '-I', '-B', str(blob), '--upx', str(packer), '--root', str(ROOT),
                    '--rev', rev, '--pkg', PKG, '--work', str(work)]
            jobs.append((world + '-' + scenario, argv, env))
    battery_work = SCRATCH / 'battery-work'
    battery_work.mkdir()
    for i in range(2):
        jobs.append(('battery-' + str(i + 1), [sys.executable, '-I', '-B', str(SCRATCH / 'battery.py'),
                     '--root', str(ROOT), '--rev', FREEZE, '--tool', 'tools/round-70/packed-elf.py',
                     '--patch-set', 'r70', '--work', str(battery_work), '--min-pristine-cases', '0'], None))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(run, *job) for job in jobs]
        records = [f.result() for f in futures]
    for record in records:
        if record['name'] in logs:
            record['impostor_log_exists'] = logs[record['name']].exists()
            record['impostor_log_content'] = logs[record['name']].read_text() if logs[record['name']].exists() else None
    manifest['axes'] = ['hash-before-execution', 'path-threading', 'child-environment isolation', 'typed refusal', 'per-run scratch']
    manifest['records'] = records
    (OUT / 'evidence.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({r['name']: {'rc': r['rc'], 'payload': r['payload'], 'traceback': r['traceback'],
                                'impostor_log_exists': r.get('impostor_log_exists')} for r in records}, indent=2))

if __name__ == '__main__':
    try:
        main()
    finally:
        shutil.rmtree(SCRATCH)
