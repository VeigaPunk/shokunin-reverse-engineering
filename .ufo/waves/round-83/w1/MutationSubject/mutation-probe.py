#!/usr/bin/env python3
"""Author-side finite mutation probe; does not alter frozen audit or fixtures."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
OWN = ROOT / '.ufo/waves/round-83/w1/MutationSubject'
SCRATCH = Path('/fast/scratch/hyaku/kaidoku-r83/MutationSubject')
FREEZE = 'de4e58b2c22bf4376dc81bd32dfe0b9ac605e17e'
BASE = '650344bc37ca303fb9487c1174192057af499b9b'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def blob(rev, path):
    return subprocess.check_output(['git', '-C', str(ROOT), 'show', f'{rev}:{path}'], timeout=10)


def replace_function(data, replacement):
    tree = ast.parse(data)
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'entry_cites']
    if len(nodes) != 1:
        raise ValueError('Expected exactly one entry_cites')
    node = nodes[0]
    lines = data.decode().splitlines(keepends=True)
    return (''.join(lines[:node.lineno - 1]) + replacement + ''.join(lines[node.end_lineno:])).encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--subject', required=True, type=Path)
    args = parser.parse_args()
    if os.environ.get('TMPDIR') != str(SCRATCH):
        raise ValueError('TMPDIR must equal the assigned scratch path')
    if SCRATCH.exists():
        raise ValueError('Scratch already exists; refusing to remove unknown files')
    original = args.subject.read_bytes()
    audit = blob(FREEZE, 'tools/round-83/attribution-audit.py')
    fixture = blob(FREEZE, '.ufo/waves/round-83/attribution-cases.json')
    actual = blob(BASE, 'corpus/knowledge/2026-11-04-r82-conjunction-and-printed-commands.md').decode()
    tree = ast.parse(audit)
    helpers = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in {'load_function', 'score'}]
    namespace = {'ast': ast}
    exec(compile(ast.Module(body=helpers, type_ignores=[]), '<frozen-audit-helpers>', 'exec'), namespace)
    cases = json.loads(fixture)
    if len(cases) != 8 or sum(bool(c.get('real')) for c in cases) != 2:
        raise ValueError('Frozen population mismatch')
    # Supplemental witnesses are separate: they never enter the eight-case score.
    witnesses = [
        {'id': 'late-header', 'text': '\n' * 12 + 'source: S299 — late\n', 'sid': 'S299', 'expected': False},
        {'id': 'duplicate-header', 'text': 'source: S299 — first\nsource: S286 — second\n', 'sid': 'S299', 'expected': False},
    ]

    def detector(data):
        try:
            fn = namespace['load_function'](data)
            rows = namespace['score'](fn, cases, actual)
            extra = namespace['score'](fn, witnesses, actual)
            bad = [r['id'] for r in rows if not r['matched']]
            return {'rc': int(bool(bad)), 'mismatches': bad, 'rows': rows,
                    'supplemental_mismatches': [r['id'] for r in extra if not r['matched']],
                    'supplemental_rows': extra}
        except Exception as exc:
            return {'rc': 2, 'error': f'{type(exc).__name__}: {exc}'}

    # Wrappers keep candidate behavior except at the named mutation boundary.
    tree = ast.parse(original)
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'entry_cites')
    if len(node.args.args) != 2:
        raise ValueError('Expected two positional function arguments')
    first, second = [arg.arg for arg in node.args.args]
    lines = original.decode().splitlines(keepends=True)
    body = ''.join(lines[node.body[0].lineno - 1:node.end_lineno])
    signature = f'def entry_cites({first}, {second}):\n'
    variants = {
        'lexical-presence': signature + f'    return bool(re.search(r"\\b" + re.escape({second}) + r"\\b", {first}))\n',
        'allfalse': signature + '    return False\n',
        'alltrue': signature + '    return True\n',
        'drop-multi-id': signature + f'    {first} = re.sub(r"(source: S[0-9]{{3,}})(?:, *S[0-9]{{3,}})+", r"\\1", {first})\n' + body,
        'ignore-header-position': signature + f'    {first} = "\\n".join(line for line in {first}.splitlines() if line.startswith("source:"))\n' + body,
        'ignore-header-duplicates': signature + f'    _seen = False\n    _lines = []\n    for _line in {first}.splitlines():\n        if _line.startswith("source:"):\n            if _seen:\n                continue\n            _seen = True\n        _lines.append(_line)\n    {first} = "\\n".join(_lines)\n' + body,
    }
    expectations = {
        'lexical-presence': ['real-withdrawn', 'commentary-only', 'withdrawn-head'],
        'allfalse': ['real-primary', 'plain-positive', 'multi-positive'],
        'alltrue': ['real-withdrawn', 'commentary-only', 'withdrawn-head', 'absent-source', 'embedded-id'],
        'drop-multi-id': ['multi-positive'],
        'ignore-header-position': [],
        'ignore-header-duplicates': [],
    }
    receipt = {'subject': str(args.subject.resolve()), 'subject_sha256': digest(original),
               'freeze': FREEZE, 'fixture_sha256': digest(fixture), 'audit_sha256': digest(audit),
               'actual_entry_sha256': digest(actual.encode()), 'cases_total': len(cases), 'real_cases': 2,
               'scope': 'Author-side frozen score helpers on file bytes, not committed CLI admission',
               'axes': ['defect sensitivity', 'real-entry relevance', 'exact restoration'], 'mutants': []}
    SCRATCH.mkdir(parents=True)
    subject = SCRATCH / 'source-bind.py'
    try:
        subject.write_bytes(original)
        (OWN / 'subject-snapshot.py').write_bytes(original)
        for name, replacement in variants.items():
            baseline = detector(subject.read_bytes())
            mutated = replace_function(original, replacement)
            item = {'mutant': name, 'expected_frozen_mismatches': expectations[name],
                    'before_sha256': digest(subject.read_bytes()), 'baseline': baseline,
                    'mutant_sha256': digest(mutated)}
            try:
                subject.write_bytes(mutated)
                item['mutated'] = detector(subject.read_bytes())
            finally:
                subject.write_bytes(original)
                item['restored'] = detector(subject.read_bytes())
                item['after_sha256'] = digest(subject.read_bytes())
                item['exact_restoration'] = subject.read_bytes() == original
            if baseline['rc'] != 0 or item['restored']['rc'] != 0:
                item['verdict'] = 'inconclusive'
            elif item['mutated']['rc'] == 0:
                item['verdict'] = 'survived'
            else:
                item['verdict'] = 'killed'
            receipt['mutants'].append(item)
    finally:
        shutil.rmtree(SCRATCH)
        receipt['scratch_removed'] = not SCRATCH.exists()
        (OWN / 'mutation-results.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'subject_sha256': receipt['subject_sha256'], 'scratch_removed': receipt['scratch_removed'],
                      'results': [{'mutant': x['mutant'], 'verdict': x['verdict'],
                                   'mismatches': x['mutated'].get('mismatches'),
                                   'supplemental_mismatches': x['mutated'].get('supplemental_mismatches'),
                                   'restored': x['exact_restoration']} for x in receipt['mutants']]}, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
