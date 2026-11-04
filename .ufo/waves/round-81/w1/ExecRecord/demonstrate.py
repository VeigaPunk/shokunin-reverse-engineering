#!/usr/bin/env python3
"""Run only the assigned frozen C2 counter against a committed candidate sandbox."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

LANE = Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
OUT = LANE / '.ufo/waves/round-81/w1/ExecRecord'
WORK = Path('/fast/scratch/hyaku/kaidoku-r81/ExecRecord')
FROZEN = 'abdcfd3c28d98288a3dc6b4e98c88d115ed42b53'


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    env = {'PATH': os.defpath, 'HOME': str(WORK), 'TMPDIR': str(WORK),
           'LANG': 'C.UTF-8', 'GIT_CONFIG_NOSYSTEM': '1'}
    repo = WORK / 'candidate-repo'
    repo.mkdir()

    def git(*args):
        return subprocess.check_output(['git', '-C', str(repo), *args], env=env)

    try:
        files = {
            'tools/round-81/strictness-battery.py': (OUT / 'strictness-battery.py').read_bytes(),
        }
        for name in ('tools/round-80/pointer-bind.py', 'tools/round-81/record-integration.py'):
            files[name] = subprocess.check_output(
                ['git', '-C', str(LANE), 'show', f'{FROZEN}:{name}'], env=env)
        for name, data in files.items():
            path = repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        git('init', '-q')
        top = git('rev-parse', '--show-toplevel').decode().strip()
        if top != str(repo):
            raise RuntimeError('fixture root mismatch')
        git('add', 'tools')
        git('-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid',
            'commit', '-q', '-m', 'bounded candidate fixture')
        rev = git('rev-parse', 'HEAD').decode().strip()
        canonical_command = [sys.executable, '-I', '-B',
                             str(repo / 'tools/round-81/strictness-battery.py'),
                             '--selftest', '--work', str(WORK / 'canonical')]
        canonical = subprocess.run(canonical_command, env=env, cwd=WORK,
                                   capture_output=True, text=True)
        (OUT / 'canonical-selftest.json').write_text(json.dumps(
            {'command': canonical_command, 'exit': canonical.returncode,
             'stdout': canonical.stdout, 'stderr': canonical.stderr}, indent=1) + '\n')
        command = [sys.executable, '-I', '-B',
                   str(repo / 'tools/round-81/record-integration.py'),
                   '--root', str(repo), '--rev', rev, '--work', str(WORK / 'counter'),
                   '--json-out', str(OUT / 'counter.json')]
        proc = subprocess.run(command, env=env, cwd=WORK, capture_output=True, text=True)
        receipt = {'command': command, 'exit': proc.returncode,
                   'stdout': proc.stdout, 'stderr': proc.stderr,
                   'fixture_toplevel': top, 'fixture_revision': rev,
                   'sha256': {name: hashlib.sha256(data).hexdigest()
                              for name, data in files.items()}}
        (OUT / 'demonstration.json').write_text(json.dumps(receipt, indent=1) + '\n')
        print(json.dumps({'exit': proc.returncode, 'receipt': str(OUT / 'counter.json')}))
        return proc.returncode
    finally:
        shutil.rmtree(WORK)
        (OUT / 'cleanup.json').write_text(json.dumps(
            {'scratch': str(WORK), 'removed': not WORK.exists()}) + '\n')


if __name__ == '__main__':
    sys.exit(main())
