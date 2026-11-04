#!/usr/bin/env python3
"""Seat-owned bounded demonstrations; no lane mutations or integrated checks."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
FREEZE = 'abdcfd3c28d98288a3dc6b4e98c88d115ed42b53'
BASE = '5b59ae615a2ab68e3b421820d1c72751e1185385'
CASE = 'record-fixture-committed-clean'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    work = Path(args.work).resolve()
    out = Path(args.out).resolve()
    assert str(work) == '/fast/scratch/hyaku/kaidoku-r81/ExecCounter'
    work.mkdir(parents=True, exist_ok=False)
    env = {'PATH': '/usr/bin:/bin', 'HOME': str(work), 'TMPDIR': str(work), 'LANG': 'C.UTF-8'}
    commands = []

    def run(argv, timeout=180):
        p = subprocess.run(argv, cwd=work, env=env, capture_output=True, text=True, timeout=timeout)
        commands.append({'argv': argv, 'exit': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr})
        return p

    def get(rev, path):
        return subprocess.check_output(['git', '-C', LANE, 'show', f'{rev}:{path}'])

    def counter(root, rev, target, name):
        receipt = out / f'{name}.json'
        p = run([sys.executable, '-I', '-B', str(out / 'frozen-counter.py'), '--root', str(root),
                 '--rev', rev, '--target', target, '--work', str(work), '--json-out', str(receipt)])
        row = json.loads(receipt.read_text())
        return {'name': name, 'exit': p.returncode, 'killed': row.get('killed'),
                'survivors': row.get('survivors'), 'pristine': row.get('pristine', {}).get('summary'),
                'mutant': row.get('mutant', {}).get('summary')}

    try:
        frozen = get(FREEZE, 'tools/round-81/record-integration.py')
        (out / 'frozen-counter.py').write_bytes(frozen)
        (out / 'frozen-plan.md').write_bytes(get(FREEZE, 'plans/round-81-claims.md'))
        base_source = get(BASE, 'tools/round-80/strictness-battery.py')
        tree = ast.parse(base_source)
        fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'make_fixture_repo')
        anchors = [n for n in ast.walk(fn) if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
                   and any(isinstance(c, ast.Constant) and c.value == 'commit' for c in ast.walk(n))]
        (out / 'anchor.json').write_text(json.dumps({'count': len(anchors), 'spans': [
            {'lineno': n.lineno, 'end_lineno': n.end_lineno, 'col_offset': n.col_offset,
             'source': ast.get_source_segment(base_source.decode(), n)} for n in anchors]}, indent=2) + '\n')
        rows = [counter(LANE, BASE, 'tools/round-80/strictness-battery.py', 'base-control')]
        repo = work / 'classification-repo'
        repo.mkdir()
        (repo / 'tools/round-80').mkdir(parents=True)
        (repo / 'tools/round-80/pointer-bind.py').write_bytes(get(BASE, 'tools/round-80/pointer-bind.py'))
        specs = {
            'declared-failure': {},
            'absent-case': {'absent': True},
            'wrong-case': {'wrong': True},
            'crash': {'crash': True},
            'no-summary': {'summary': False},
            'duplicate-case': {'duplicate': True},
            'undersized-pristine': {'pristine_count': 1},
            'dirty-pristine-summary': {'pristine_failures': 3},
            'extra-wrong-case-failure': {'extra': True},
        }
        for name, spec in specs.items():
            source = ('import json\nimport sys\n'
                      'def make_fixture_repo():\n'
                      '    state = []\n'
                      "    state.append('commit')\n"
                      '    return bool(state)\n'
                      'clean = make_fixture_repo()\n'
                      f'spec = {spec!r}\n'
                      "if not clean and spec.get('crash'):\n    raise RuntimeError('isolated fixture crash')\n"
                      "count = spec.get('pristine_count', 11) if clean else 11\n"
                      "failures = spec.get('pristine_failures', 0) if clean else 1\n"
                      f'case = {CASE!r}\n'
                      "if not clean and spec.get('wrong'):\n    case = 'unrelated-case'\n"
                      "if clean or not spec.get('absent'):\n"
                      "    print(json.dumps({'case': case, 'pass': clean}))\n"
                      "if not clean and spec.get('duplicate'):\n"
                      "    print(json.dumps({'case': case, 'pass': False}))\n"
                      "if not clean and spec.get('extra'):\n"
                      "    print(json.dumps({'case': 'unrelated-case', 'pass': False}))\n    failures = 2\n"
                      "if clean or spec.get('summary', True):\n"
                      "    print(f'SELFTEST cases={count} failures={failures}')\n"
                      'sys.exit(0 if clean else 1)\n')
            (repo / f'{name}.py').write_text(source)
            (out / f'fixture-{name}.py').write_text(source)
        assert run(['git', '-C', str(repo), 'init', '-q']).returncode == 0
        top = run(['git', '-C', str(repo), 'rev-parse', '--show-toplevel'])
        assert top.returncode == 0 and top.stdout.strip() == str(repo)
        assert run(['git', '-C', str(repo), 'add', '.']).returncode == 0
        assert run(['git', '-C', str(repo), '-c', 'user.name=fixture', '-c',
                    'user.email=fixture@invalid', 'commit', '-q', '-m', 'bounded classification fixtures']).returncode == 0
        for name in specs:
            rows.append(counter(repo, 'HEAD', f'{name}.py', name))
        # Static executability only: no duplicate C1/C2 integrated measurements.
        ns = {'__name__': 'audit_plan_command'}
        exec(compile(get(FREEZE, 'tools/round-76/plan-command.py'), 'frozen-plan-command.py', 'exec'), ns)
        plan = (out / 'frozen-plan.md').read_text()
        printed = []
        for name in ('C1', 'C2'):
            command = ns['extract_block'](plan, name)
            item = {'block': name, 'command': command, 'static_defects': ns['static_defects'](command)}
            try:
                item['argv'] = ns['build_argv'](command, BASE, str(work), str(out / 'printed.json'), LANE)
            except ns['Refused'] as exc:
                item['refused'] = str(exc)
            printed.append(item)
        (out / 'printed-commands.json').write_text(json.dumps(printed, indent=2) + '\n')
        (out / 'summary.json').write_text(json.dumps({'axes': ['calibration', 'depth'],
            'freeze': FREEZE, 'base': BASE, 'counter_sha256': hashlib.sha256(frozen).hexdigest(),
            'results': rows}, indent=2) + '\n')
        print(json.dumps(rows, indent=2))
    finally:
        (out / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
        shutil.rmtree(work)
        (out / 'cleanup.json').write_text(json.dumps({'scratch': str(work), 'removed': not work.exists()}) + '\n')


if __name__ == '__main__':
    main()
