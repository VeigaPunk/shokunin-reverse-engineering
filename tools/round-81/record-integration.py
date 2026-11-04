#!/usr/bin/env python3
"""R81-C2: commit-omission mutation at the real record integration boundary."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

CASE = 'record-fixture-committed-clean'

def get(root, rev, path):
    return subprocess.check_output(['git', '-C', root, 'show', f'{rev}:{path}'])

def omit_commit(source):
    tree = ast.parse(source)
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'make_fixture_repo')
    sites = [n for n in ast.walk(fn) if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
             and any(isinstance(c, ast.Constant) and c.value == 'commit' for c in ast.walk(n))]
    if len(sites) != 1:
        raise ValueError(f'commit omission anchors {len(sites)} != 1')
    n = sites[0]
    lines = source.splitlines(keepends=True)
    lines[n.lineno-1:n.end_lineno] = [' ' * n.col_offset + 'pass  # frozen omitted-commit mutant\n']
    return ''.join(lines)

def run(path, scratch):
    env = {'PATH': os.environ.get('PATH', '/usr/bin:/bin'), 'HOME': str(scratch),
           'LANG': 'C.UTF-8', 'TMPDIR': str(scratch)}
    p = subprocess.run([sys.executable, '-I', '-B', str(path), '--selftest'],
                       capture_output=True, text=True, env=env, timeout=180)
    cases = []
    for line in p.stdout.splitlines():
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict) and 'case' in row:
            cases.append(row)
    summaries = re.findall(r'SELFTEST cases=(\d+) failures=(\d+)', p.stdout)
    return {'exit': p.returncode, 'cases': cases, 'summary': list(map(int, summaries[-1])) if summaries else None,
            'stdout': p.stdout, 'stderr': p.stderr}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--target', default='tools/round-81/strictness-battery.py')
    ap.add_argument('--work', required=True)
    ap.add_argument('--json-out', required=True)
    a = ap.parse_args()
    Path(a.work).mkdir(parents=True, exist_ok=True)
    result = {'rev': a.rev, 'target': a.target, 'declared_case': CASE,
              'instrument': {'path': 'tools/round-81/record-integration.py',
                             'sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}}
    try:
        data = get(a.root, a.rev, a.target)
        binder = get(a.root, a.rev, 'tools/round-80/pointer-bind.py')
        result['target_sha256'] = hashlib.sha256(data).hexdigest()
        result['binder_sha256'] = hashlib.sha256(binder).hexdigest()
        with tempfile.TemporaryDirectory(prefix='record-integration-', dir=a.work) as d:
            scratch = Path(d)
            target = scratch / 'strictness-battery.py'
            (scratch / 'pointer-bind.py').write_bytes(binder)
            target.write_bytes(data)
            result['pristine'] = run(target, scratch)
            target.write_text(omit_commit(data.decode()))
            result['mutant'] = run(target, scratch)
        mutant = result['mutant']
        detector = [r for r in mutant['cases'] if r.get('case') == CASE]
        killed = (result['pristine']['exit'] == 0 and result['pristine']['summary'] is not None
                  and mutant['summary'] is not None and mutant['exit'] == 1
                  and len(detector) == 1 and detector[0].get('pass') is False)
        result.update({'mutants': 1, 'killed': int(killed), 'survivors': int(not killed),
                       'ok': killed, 'cleanup': True})
        code = 0 if killed else 1
    except (OSError, ValueError, StopIteration, subprocess.SubprocessError) as e:
        result.update({'ok': False, 'unevaluable': str(e)})
        code = 2
    Path(a.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.json_out).write_text(json.dumps(result, indent=1) + '\n')
    print(json.dumps(result))
    return code

if __name__ == '__main__':
    sys.exit(main())
