#!/usr/bin/env python3
"""mutants.py - single-point mutation sweep of sqfs-triage-v4.py.

Each mutant is one exact-string replacement applied to a scratch copy of the
interpreter; the mutant survives only if its ``--selftest`` still exits 0.  The point
is to show which v4 grammar rules the selftest actually holds, not to enumerate every
editable byte (round-41 w2 `R41W2C2InterpMut.md` §7 measured that the held-out pairs
kill nothing on their own, so the selftest carries the whole load).

Usage:  python3 -I -B mutants.py [--tool PATH] [--work DIR]
        WORK (or $TMPDIR) must exist; nothing is written outside it.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

MUTANTS = [
    # id, axis, exact anchor (must occur exactly once), replacement
    ('M01', 'handler/none',
     "    if kind == 'none':\n        return not names",
     "    if kind == 'none':\n        return True"),
    ('M02', 'column/column-4',
     "    if not match_glob(rule['handler'], feat['F']):",
     "    if not match_glob(rule['handler'], feat['HF']):"),
    ('M03', 'column/column-4',
     "    if not match_glob(rule['failing_handler'], feat['HF']):",
     "    if not match_glob(rule['failing_handler'], feat['F']):"),
    ('M04', 'handler/star',
     "    return any(fnmatch.fnmatchcase(value, payload) for value in names)",
     "    return any(fnmatch.fnmatchcase(value, payload) for value in names) and False"),
    ('M05', 'handler/validation',
     '    hits = [name for name in KNOWN_HANDLERS if fnmatch.fnmatchcase(name, cell)]',
     '    hits = [cell]'),
    ('M06', 'handler/validation',
     "    if not cell.startswith(SQUASHFS_PREFIX):",
     "    if False:"),
    ('M07', 'features/H',
     "    for gap in _as_list(nr.get('extraction_gaps')):\n"
     "        handler = gap.get('handler') if isinstance(gap, dict) else None\n"
     "        if isinstance(handler, str) and handler and handler not in names:\n"
     "            names.append(handler)\n"
     "    return names",
     "    return names"),
    ('M08', 'features/HF',
     "        if not isinstance(gap, dict) or gap.get('kind') != FAILURE_KIND:\n"
     "            continue",
     "        if not isinstance(gap, dict):\n            continue"),
    ('M09', 'grammar/deps-contains',
     "            'dependencies': _parse_set_cell(dep, 'dependencies', contains=True),",
     "            'dependencies': _parse_set_cell(dep, 'dependencies', contains=False),"),
    ('M10', 'features/SR',
     "    for found in _iter_dicts(data.get('raw_result')):\n"
     "        if found.get('__typename__') == SYMLINK_TYPENAME:\n"
     "            return 'yes'",
     "    pass"),
    ('M11', 'features/SR',
     "        for holder in _holders(diag):\n"
     "            if holder.get('__typename__') == SYMLINK_TYPENAME:\n"
     "                return 'yes'",
     "        if isinstance(diag, dict) and diag.get('report', {}).get(\n"
     "                '__typename__') == SYMLINK_TYPENAME:\n"
     "            return 'yes'"),
    ('M12', 'features/BE',
     '        if tokens and names_sasquatch(tokens) and cmd not in commands:',
     '        if tokens and cmd not in commands:'),
    ('M13', 'features/BE',
     "ARGV_KEYS = ('command', 'argv', 'args')",
     "ARGV_KEYS = ('command',)"),
    ('M14', 'features/P',
     "        'P': len(_as_list(nr.get('files'))),",
     "        'P': 1 if _as_list(nr.get('files')) else 0,"),
    ('M15', 'order/first-match',
     '    for rule in rules:\n        if rule_matches(rule, feat):\n            return rule',
     '    for rule in reversed(rules):\n        if rule_matches(rule, feat):\n            return rule'),
    ('M16', 'files/zero',
     "    if files == '0' and feat['P'] != 0:",
     "    if files == '0' and feat['P'] < 0:"),
    ('M17', 'marker/refusal',
     "REFUSED_MARKERS = ('<!-- sqfs-triage-table v3 -->',",
     "REFUSED_MARKERS = ("),
    ('M18', 'grammar/duplicate-label',
     "        if label in labels:",
     "        if False:"),
    ('M19', 'grammar/action-vocabulary',
     "        if action not in vocabulary:",
     "        if False:"),
    ('M20', 'domain/guard',
     "    if rule['provider'] != '*' and rule['provider'] != feat['PV']:",
     "    if False:"),
]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--tool', default=os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'sqfs-triage-v4.py'))
    ap.add_argument('--work', default=None)
    ns = ap.parse_args(argv)
    work = ns.work or os.environ.get('TMPDIR')
    work = tempfile.mkdtemp(dir=work, prefix='sqfs-v4-mutants.')
    src = open(ns.tool, encoding='utf-8').read()
    print('tool: %s  sha256: %s' % (ns.tool, __import__('hashlib').sha256(
        src.encode()).hexdigest()))
    clean = subprocess.run([sys.executable, '-I', '-B', ns.tool, '--selftest'],
                           capture_output=True, text=True)
    print('baseline selftest exit=%d  %s' % (clean.returncode,
                                             clean.stdout.strip().splitlines()[-1]))
    killed = survived = 0
    try:
        for mid, axis, anchor, replacement in MUTANTS:
            count = src.count(anchor)
            if count != 1:
                print('%s %-24s SKIP anchor occurs %d times' % (mid, axis, count))
                continue
            path = os.path.join(work, mid + '.py')
            with open(path, 'w', encoding='utf-8') as handle:
                handle.write(src.replace(anchor, replacement, 1))
            res = subprocess.run([sys.executable, '-I', '-B', path, '--selftest'],
                                 capture_output=True, text=True)
            tail = [l for l in res.stdout.splitlines() if l.startswith(('FAIL', 'SELFTEST'))]
            if res.returncode == 0:
                survived += 1
                print('%s %-24s SURVIVED %s' % (mid, axis, tail[-1] if tail else ''))
            else:
                killed += 1
                first = tail[0][5:].split(':')[0] if tail else '?'
                print('%s %-24s killed   first-failure=%s' % (mid, axis, first))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print('MUTANTS total=%d killed=%d survived=%d' % (len(MUTANTS), killed, survived))
    return 0 if survived == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
