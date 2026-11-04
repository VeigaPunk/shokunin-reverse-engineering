#!/usr/bin/env python3
"""Finite source-attribution self-assessment audit; not natural-language inference."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

BASE = '650344bc37ca303fb9487c1174192057af499b9b'
ENTRY = 'corpus/knowledge/2026-11-04-r82-conjunction-and-printed-commands.md'
OLD = 'tools/round-82/printed-command.py'
FIXTURES = '.ufo/waves/round-83/attribution-cases.json'
PREDICATE = 'attribution mismatches 0 across exactly eight frozen cases, with the two committed real-entry cases present and boolean outputs'

def blob(root, rev, path):
    return subprocess.check_output(['git', '-C', str(root), 'show', f'{rev}:{path}'])

def load_function(data):
    # Only the named function and imports it needs, never top-level CLI code.
    tree = ast.parse(data)
    funcs = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == 'entry_cites']
    if len(funcs) != 1 or isinstance(funcs[0], ast.AsyncFunctionDef):
        raise ValueError('ENTRY_CITES_ABSENT_OR_AMBIGUOUS')
    import re
    ns = {'re': re}
    exec(compile(ast.Module(body=funcs, type_ignores=[]), '<committed-entry-cites>', 'exec'), ns)
    return ns['entry_cites']

def score(fn, cases, actual):
    rows = []
    for case in cases:
        text = actual if case.get('real') else case['text']
        value = fn(text, case['sid'])
        rows.append({'id': case['id'], 'sid': case['sid'], 'expected': case['expected'],
                     'observed': value, 'matched': type(value) is bool and value == case['expected'],
                     'real': bool(case.get('real'))})
    return rows

def run(args):
    rev = subprocess.check_output(['git', '-C', str(args.root), 'rev-parse', '--verify', args.rev + '^{commit}'], text=True).strip()
    fixtures = blob(args.root, args.freeze, FIXTURES)
    cases = json.loads(fixtures)
    if len(cases) != 8 or len({c['id'] for c in cases}) != 8 or sum(c.get('real', False) for c in cases) != 2:
        raise ValueError('FROZEN_POPULATION_INVALID')
    actual = blob(args.root, BASE, ENTRY).decode()
    subject = blob(args.root, rev, args.target)
    rows = score(load_function(subject), cases, actual)
    mismatches = [r['id'] for r in rows if not r['matched']]
    result = {'schema': 'kaidoku-r83-attribution-v1', 'predicate': PREDICATE, 'rev': rev,
              'freeze': args.freeze, 'target': args.target,
              'target_sha256': hashlib.sha256(subject).hexdigest(),
              'fixture_sha256': hashlib.sha256(fixtures).hexdigest(),
              'entry_revision': BASE, 'entry_sha256': hashlib.sha256(actual.encode()).hexdigest(),
              'cases_total': len(rows), 'real_cases': sum(r['real'] for r in rows),
              'mismatch_count': len(mismatches), 'mismatches': mismatches, 'rows': rows,
              'ok': not mismatches,
              'instrument': {'path': 'tools/round-83/attribution-audit.py', 'sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}}
    return result, 0 if result['ok'] else 1

def selftest(args):
    # Self-invocation exercises real committed fixtures and stable finding IDs.
    failures = []
    root = Path(args.work).resolve()
    root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='outer-', dir=root) as work:
        for name, target, expected_rc, expected_id in [
            ('legacy-red', OLD, 1, 'real-withdrawn'),
            ('candidate-green', args.target, 0, None)]:
            out = Path(work) / (name + '.json')
            cmd = [sys.executable, '-I', '-B', str(Path(__file__).resolve()), '--root', str(args.root), '--rev', args.rev,
                   '--freeze', args.freeze, '--target', target, '--json-out', str(out)]
            child = subprocess.run(cmd, capture_output=True, text=True)
            receipt = json.loads(out.read_text()) if out.exists() else {}
            if child.returncode != expected_rc or (expected_id is not None and expected_id not in receipt.get('mismatches', [])):
                failures.append(name)
    return {'selftest': True, 'cases': 2, 'failures': failures, 'ok': not failures}, int(bool(failures))

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', default='.')
    p.add_argument('--rev', required=True)
    p.add_argument('--freeze', required=True)
    p.add_argument('--target', default='tools/round-83/source-bind.py')
    p.add_argument('--json-out', required=True)
    p.add_argument('--selftest', action='store_true')
    p.add_argument('--work')
    a = p.parse_args()
    try:
        if a.selftest and not a.work:
            raise ValueError('WORK_REQUIRED')
        result, code = selftest(a) if a.selftest else run(a)
    except Exception as e:
        result, code = {'ok': False, 'finding': 'UNEVALUABLE', 'error': str(e)}, 2
    out = Path(a.json_out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))
    return code

if __name__ == '__main__':
    raise SystemExit(main())
