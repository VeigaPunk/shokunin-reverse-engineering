#!/usr/bin/env python3
"""Independent finite R83 oracle; never imports the frozen counter or candidate."""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
BASE = '650344bc37ca303fb9487c1174192057af499b9b'
FREEZE = 'de4e58b2c22bf4376dc81bd32dfe0b9ac605e17e'
LEGACY = 'tools/round-82/printed-command.py'
ENTRY = 'corpus/knowledge/2026-11-04-r82-conjunction-and-printed-commands.md'
CASES = '.ufo/waves/round-83/attribution-cases.json'
OUT = Path(__file__).resolve().parent


def committed(rev: str, path: str) -> bytes:
    return subprocess.check_output(
        ['git', '-C', str(ROOT), 'show', f'{rev}:{path}'], timeout=20)


def positive_ids(text: str) -> tuple[str, ...]:
    """Parse the declared header by delimiters and ASCII character checks."""
    lines = text.splitlines()
    fields = [(index, line[7:]) for index, line in enumerate(lines)
              if line.startswith('source:')]
    if len(fields) != 1 or fields[0][0] >= 12:
        return ()
    value = fields[0][1].lstrip(' ')
    leading, separator, _commentary = value.partition(' — ')
    if not separator:
        return ()
    ids = tuple(piece.strip(' ') for piece in leading.split(','))
    for sid in ids:
        if (len(sid) < 4 or sid[0] != 'S'
                or not all('0' <= char <= '9' for char in sid[1:])):
            return ()
    return ids


def main() -> int:
    legacy_bytes = committed(BASE, LEGACY)
    entry_bytes = committed(BASE, ENTRY)
    case_bytes = committed(FREEZE, CASES)
    tree = ast.parse(legacy_bytes.decode('utf-8'))
    functions = [node for node in tree.body
                 if isinstance(node, ast.FunctionDef) and node.name == 'entry_cites']
    assert len(functions) == 1
    function = functions[0]
    namespace = {'re': re}
    module = ast.Module(body=[function], type_ignores=[])
    exec(compile(module, f'{BASE}:{LEGACY}', 'exec'), namespace)
    lexical = namespace['entry_cites']
    cases = json.loads(case_bytes)
    expected_ids = ['real-primary', 'real-withdrawn', 'plain-positive',
                    'multi-positive', 'commentary-only', 'withdrawn-head',
                    'absent-source', 'embedded-id']
    assert [case['id'] for case in cases] == expected_ids
    assert sum(case.get('real') is True for case in cases) == 2
    assert all(type(case['expected']) is bool for case in cases)
    entry = entry_bytes.decode('utf-8')
    rows = []
    for case in cases:
        text = entry if case.get('real') is True else case['text']
        ids = positive_ids(text)
        values = {'independent_oracle': case['sid'] in ids,
                  'legacy_lexical': lexical(text, case['sid']),
                  'refuse_everything': False, 'accept_everything': True}
        assert all(type(value) is bool for value in values.values())
        rows.append({'id': case['id'], 'real': case.get('real') is True,
                     'sid': case['sid'], 'expected': case['expected'],
                     'positive_ids': ids, 'outputs': values,
                     'mismatches': {name: value != case['expected']
                                    for name, value in values.items()}})
    counts = {name: {'total': sum(row['mismatches'][name] for row in rows),
                     'real': sum(row['mismatches'][name] for row in rows if row['real']),
                     'case_ids': [row['id'] for row in rows if row['mismatches'][name]]}
              for name in rows[0]['outputs']}
    ok = (counts['independent_oracle']['total'] == 0
          and counts['legacy_lexical']['total'] == 3
          and counts['refuse_everything']['total'] == 3
          and counts['accept_everything']['total'] == 5
          and all(counts[name]['real'] == 1 for name in
                  ('legacy_lexical', 'refuse_everything', 'accept_everything')))
    artifacts = [('legacy-committed.py', legacy_bytes, BASE, LEGACY),
                 ('entry-committed.md', entry_bytes, BASE, ENTRY),
                 ('cases-declaration.json', case_bytes, FREEZE, CASES)]
    provenance = []
    for filename, data, revision, path in artifacts:
        (OUT / filename).write_bytes(data)
        provenance.append({'revision': revision, 'path': path, 'snapshot': filename,
                           'sha256': hashlib.sha256(data).hexdigest()})
    receipt = {'scope': 'author-side finite oracle; not outside admission',
               'axes': ['positive-attribution correctness', 'control discrimination',
                        'committed-byte reproducibility'],
               'python': sys.version, 'base': BASE, 'freeze': FREEZE,
               'probe_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               'provenance': provenance,
               'legacy_function_lines': [function.lineno, function.end_lineno],
               'real_source_line': entry.splitlines()[0],
               'population': len(rows), 'real_population': 2, 'rows': rows,
               'mismatch_counts': counts, 'ok': ok}
    (OUT / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'ok': ok, 'mismatch_counts': counts}, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
