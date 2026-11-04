#!/usr/bin/env python3
"""Isolated outer-CLI green/red self-invocations for the round-82 gates."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--which', choices=['conjunction', 'printed', 'all'], default='all')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--json-out')
    a = ap.parse_args()
    Path(a.work).mkdir(parents=True, exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix='outer-cli-', dir=a.work))
    env = {'PATH': os.environ.get('PATH', '/usr/bin:/bin'), 'HOME': str(scratch),
           'TMPDIR': str(scratch), 'LANG': 'C.UTF-8'}
    rows = []
    def git(repo, *args):
        return subprocess.run(['git', '-C', str(repo), *args], env=env,
                              capture_output=True, text=True, check=True).stdout
    try:
        repo = scratch/'repo'
        subprocess.run(['git', 'clone', '--shared', '--no-checkout', a.root, str(repo)],
                       env=env, capture_output=True, check=True)
        git(repo, 'checkout', '--detach', a.rev)
        assert Path(git(repo, 'rev-parse', '--show-toplevel').strip()) == repo.resolve()
        def invoke(name, red=False):
            script = 'conjunction-gate.py' if name == 'conjunction' else 'printed-command.py'
            out = scratch/f'{name}-{red}.json'
            argv = ['python3', '-I', '-B', str(repo/'tools/round-82'/script),
                    '--battery', '--root', str(repo), '--rev', 'HEAD', '--json-out', str(out)]
            if name == 'printed':
                argv += ['--work', str(scratch/f'printed-{red}')]
            p = subprocess.run(argv, cwd=repo, env=env, capture_output=True, text=True, timeout=300)
            data = json.loads(out.read_text())
            if name == 'conjunction':
                finding = 'genuine_refused' if not data['genuine_ok'] else 'clean'
            else:
                bad = [x for x in data['arms'] if x['arm'] == 'c1-executed'][0]
                finding = 'SCRIPT_PIN_MISMATCH' if any('SCRIPT_PIN_MISMATCH' in d for d in bad['row']['defects']) else 'clean'
            expected = 'genuine_refused' if name == 'conjunction' and red else 'SCRIPT_PIN_MISMATCH' if red else 'clean'
            rows.append({'case': f'{name}-'+('red' if red else 'green'), 'argv': argv,
                         'exit': p.returncode, 'expected_exit': 1 if red else 0,
                         'finding': finding, 'expected_finding': expected,
                         'pass': p.returncode == (1 if red else 0) and finding == expected,
                         'stdout': p.stdout, 'stderr': p.stderr})
        for name in ['conjunction', 'printed']:
            if a.which not in ('all', name):
                continue
            if name == 'printed':
                # Isolated positive only: production deliberately withdrew duplicate S299.
                # Restore its historical bytes in the private fixture, never the lane.
                for rel in ['corpus/SOURCES.md',
                            'corpus/knowledge/2026-11-04-r82-conjunction-and-printed-commands.md']:
                    (repo/rel).write_text(git(repo, 'show',
                        'eb227c4694e16cb8fae74df0eea2f07643b46124:'+rel))
                    git(repo, 'add', rel)
                git(repo, '-c', 'user.name=fixture', '-c', 'user.email=fixture@local',
                    'commit', '-qm', 'isolated positive source fixture')
            invoke(name)
            path = repo/('.ufo/waves/round-81/l1/scores/c2-at-landing.json' if name == 'conjunction' else '.ufo/waves/round-82/claims.json')
            old = path.read_bytes()
            data = json.loads(old)
            if name == 'conjunction':
                data['binder_sha256'] = '0'*64
            else:
                data['instruments']['tools/round-82/conjunction-gate.py'] = '0'*64
            path.write_text(json.dumps(data)+'\n')
            git(repo, 'add', str(path.relative_to(repo)))
            git(repo, '-c', 'user.name=fixture', '-c', 'user.email=fixture@local', 'commit', '-qm', 'isolated red fixture')
            invoke(name, True)
            path.write_bytes(old)
            git(repo, 'add', str(path.relative_to(repo)))
            git(repo, '-c', 'user.name=fixture', '-c', 'user.email=fixture@local', 'commit', '-qm', 'restore fixture')
    finally:
        shutil.rmtree(scratch)
    result = {'rev': a.rev, 'instrument': {'path': 'tools/round-82/cli-fixtures.py',
              'sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
              'cases': rows, 'failures': [r['case'] for r in rows if not r['pass']],
              'cleanup': True}
    if a.json_out:
        Path(a.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.json_out).write_text(json.dumps(result, indent=1)+'\n')
    print(json.dumps(result))
    return 1 if result['failures'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
