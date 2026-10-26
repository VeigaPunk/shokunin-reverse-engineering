#!/usr/bin/env python3
"""R39C2ReconClean — reference implementation of the R39-C2 triage grammar (feasibility probe).

This is NOT the frozen `tools/round-39/sqfs-triage.py`; it exists to prove before the freeze
that the grammar as specified can separate the development outcome classes. It implements the
contract literally:

  * the table is the first markdown table after a line containing the marker
    `<!-- sqfs-triage-table v1 -->` inside the `## Queue-drain craft` section (heading line to
    the next `## ` heading);
  * header cells, in order: label | handler | gap kinds | dependencies |
    -be in child argv | symlink removed | published files | cause -> action | source;
  * condition cells are stripped of surrounding backticks and spaces;
  * handler: `none` (H empty) or an fnmatch pattern matching at least one element of H;
  * gap kinds / dependencies: `none` (empty set) or `a+b` = exactly {a,b};
  * -be / symlink removed: yes | no | n/a;
  * published files: 0 | >0 | *;
  * rules are tried top to bottom; first row whose every condition cell matches wins;
  * no match -> `unclassified`;
  * a malformed cell makes the whole table unevaluable -> exit 2.

Usage:
  sqfs-triage-ref.py --table <DOC> [--label] ENVELOPE...
  sqfs-triage-ref.py --selftest
Exit: 0 evaluated, 2 unevaluable.
"""
import fnmatch
import json
import shlex
import sys

MARKER = '<!-- sqfs-triage-table v1 -->'
SECTION_PREFIX = '## Queue-drain craft'
HEADER = ['label', 'handler', 'gap kinds', 'dependencies', '-be in child argv',
          'symlink removed', 'published files', 'cause -> action', 'source']
COND = 7  # first seven cells are conditions


class Unevaluable(Exception):
    pass


# ---------------------------------------------------------------- envelope features
def data_of(env):
    if isinstance(env, dict) and isinstance(env.get('data'), dict) and (
            'normalized_result' not in env):
        return env['data']
    return env


def _reports(nr):
    for d in (nr.get('diagnostics') or []):
        if isinstance(d, dict) and isinstance(d.get('report'), dict):
            yield d['report']


def _walk(obj):
    if isinstance(obj, dict):
        if '__typename__' in obj:
            yield obj
        for v in obj.values():
            yield from _walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk(v)


def _tokens(cmd):
    if isinstance(cmd, str):
        try:
            return shlex.split(cmd)
        except ValueError:
            return cmd.split()
    if isinstance(cmd, list):
        return [str(t) for t in cmd]
    return []


def features(env):
    d = data_of(env)
    nr = d.get('normalized_result') or {}
    H = {c.get('handler') for c in (nr.get('chunks') or [])
         if isinstance(c, dict) and isinstance(c.get('handler'), str)
         and c['handler'].startswith('squashfs')}
    gaps = [g for g in (nr.get('extraction_gaps') or []) if isinstance(g, dict)]
    G = {g.get('kind') for g in gaps if g.get('kind') is not None}
    D = {dep for g in gaps for dep in (g.get('dependencies') or [])}
    be, seen = 'n/a', False
    for r in _reports(nr):
        toks = _tokens(r.get('command'))
        if any('sasquatch' in t for t in toks):
            seen = True
            if '-be' in toks:
                be = 'yes'
    if seen and be != 'yes':
        be = 'no'
    sr = 'yes' if any(r.get('__typename__') == 'MaliciousSymlinkRemoved'
                      for r in _reports(nr)) else 'no'
    if sr == 'no':
        raw = d.get('raw_result') or {}
        if any(r.get('__typename__') == 'MaliciousSymlinkRemoved'
               for r in _walk(raw.get('report'))):
            sr = 'yes'
    return {'H': H, 'G': G, 'D': D, 'BE': be, 'SR': sr,
            'P': len(nr.get('files') or [])}


# ---------------------------------------------------------------- table parsing
def section(text):
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.startswith(SECTION_PREFIX):
            start = i
            break
    if start is None:
        raise Unevaluable('no `## Queue-drain craft` section')
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith('## '):
            end = j
            break
    return lines[start:end]


def cells(row):
    return [c.strip().strip('`').strip() for c in row.strip().strip('|').split('|')]


def parse_table(text):
    lines = section(text)
    mark = None
    for i, ln in enumerate(lines):
        if MARKER in ln:
            mark = i
            break
    if mark is None:
        raise Unevaluable('no triage-table marker in the craft section')
    i = mark + 1
    while i < len(lines) and not lines[i].lstrip().startswith('|'):
        i += 1
    if i >= len(lines):
        raise Unevaluable('no markdown table after the marker')
    header = cells(lines[i])
    if header != HEADER:
        raise Unevaluable(f'header mismatch: {header}')
    if i + 1 >= len(lines) or not set(lines[i + 1].strip()) <= set('|-: '):
        raise Unevaluable('missing table separator row')
    rows = []
    j = i + 2
    while j < len(lines) and lines[j].lstrip().startswith('|'):
        rows.append(cells(lines[j]))
        j += 1
    if not rows:
        raise Unevaluable('table has no rule rows')
    return [compile_row(r) for r in rows]


def _setcell(cell, name):
    if cell == 'none':
        return None  # empty set
    parts = cell.split('+')
    if not parts or any(not p or p != p.strip() for p in parts):
        raise Unevaluable(f'malformed {name} cell: {cell!r}')
    if len(set(parts)) != len(parts):
        raise Unevaluable(f'duplicate name in {name} cell: {cell!r}')
    return set(parts)


def compile_row(row):
    if len(row) != len(HEADER):
        raise Unevaluable(f'row has {len(row)} cells, want {len(HEADER)}: {row}')
    label, handler, gaps, deps, be, sr, pub = row[:COND]
    if not label:
        raise Unevaluable('empty label cell')
    if handler != 'none' and not handler:
        raise Unevaluable('empty handler cell')
    # `*` is accepted in every condition cell ("`*` matches anything" is stated before the
    # per-cell grammars); the candidate table uses explicit values so it is safe under either
    # reading of the spec.
    if be not in ('yes', 'no', 'n/a', '*'):
        raise Unevaluable(f'malformed -be cell: {be!r}')
    if sr not in ('yes', 'no', 'n/a', '*'):
        raise Unevaluable(f'malformed symlink-removed cell: {sr!r}')
    if pub not in ('0', '>0', '*'):
        raise Unevaluable(f'malformed published-files cell: {pub!r}')
    return {'label': label, 'handler': handler,
            'gaps': _setcell(gaps, 'gap kinds'), 'deps': _setcell(deps, 'dependencies'),
            'be': be, 'sr': sr, 'pub': pub}


def row_matches(rule, f):
    if rule['handler'] == 'none':
        if f['H']:
            return False
    elif not any(fnmatch.fnmatchcase(h, rule['handler']) for h in f['H']):
        return False
    if rule['gaps'] is None:
        if f['G']:
            return False
    elif f['G'] != rule['gaps']:
        return False
    if rule['deps'] is None:
        if f['D']:
            return False
    elif f['D'] != rule['deps']:
        return False
    if rule['be'] != '*' and rule['be'] != f['BE']:
        return False
    if rule['sr'] != '*' and rule['sr'] != f['SR']:
        return False
    if rule['pub'] == '0' and f['P'] != 0:
        return False
    if rule['pub'] == '>0' and f['P'] <= 0:
        return False
    return True


def classify(rules, env):
    f = features(env)
    for rule in rules:
        if row_matches(rule, f):
            return rule['label'], f
    return 'unclassified', f


# ---------------------------------------------------------------- selftest
def selftest():
    fails = []

    def case(name, text, env, want):
        try:
            rules = parse_table(text)
        except Unevaluable as e:
            fails.append(f'{name}: unexpected unevaluable ({e})')
            return
        got, _ = classify(rules, env)
        if got != want:
            fails.append(f'{name}: got {got!r} want {want!r}')

    def bad(name, text):
        try:
            parse_table(text)
        except Unevaluable:
            return
        fails.append(f'{name}: expected unevaluable')

    head = ('## Queue-drain craft\n\n' + MARKER + '\n\n| ' + ' | '.join(HEADER) + ' |\n'
            + '|' + '---|' * len(HEADER) + '\n')
    good = head + ('| clean | `squashfs_v4*` | `none` | `none` | `n/a` | `no` | `>0` | x | y |\n')
    clean = {'normalized_result': {'chunks': [{'handler': 'squashfs_v4_be'}], 'files': [{}]}}
    case('clean match', good, clean, 'clean')
    case('unclassified', good,
         {'normalized_result': {'chunks': [{'handler': 'squashfs_v4_le'}],
                                'files': [], 'extraction_gaps': [
                                    {'kind': 'extractor-failure', 'dependencies': []}]}},
         'unclassified')
    case('full envelope', good, {'ok': True, 'data': clean, 'meta': {}}, 'clean')
    case('bare data object', good, clean, 'clean')
    # -be yes / no from the child argv
    be = head + ('| avm | `squashfs_v4_be` | `extractor-failure` | `none` | `no` | `no` | `0` | x | y |\n'
                 '| body | `squashfs_v4_be` | `extractor-failure` | `none` | `yes` | `no` | `0` | x | y |\n')
    env_avm = {'normalized_result': {
        'chunks': [{'handler': 'squashfs_v4_be', 'extraction_failed': True}],
        'files': [], 'extraction_gaps': [{'kind': 'extractor-failure', 'dependencies': []}],
        'diagnostics': [{'report': {'command': 'sasquatch-v4be -no-exit-code -f -d o i',
                                    '__typename__': 'ExtractCommandFailedReport'}}]}}
    env_be = {'normalized_result': {
        'chunks': [{'handler': 'squashfs_v4_be', 'extraction_failed': True}],
        'files': [], 'extraction_gaps': [{'kind': 'extractor-failure', 'dependencies': []}],
        'diagnostics': [{'report': {'command': ['sasquatch-v4be', '-be', '-f'],
                                    '__typename__': 'ExtractCommandFailedReport'}}]}}
    case('avm (no -be)', be, env_avm, 'avm')
    case('body (-be argv list)', be, env_be, 'body')
    # set equality, not containment
    deps = head + ('| d | `squashfs_v4_be` | `missing-extractor-dependency` | `sasquatch-v4be` '
                   '| `n/a` | `no` | `0` | x | y |\n')
    case('dep exact', deps, {'normalized_result': {
        'chunks': [{'handler': 'squashfs_v4_be'}], 'files': [],
        'extraction_gaps': [{'kind': 'missing-extractor-dependency',
                             'dependencies': ['sasquatch-v4be']}]}}, 'd')
    case('dep superset is a non-match', deps, {'normalized_result': {
        'chunks': [{'handler': 'squashfs_v4_be'}], 'files': [],
        'extraction_gaps': [{'kind': 'missing-extractor-dependency',
                             'dependencies': ['sasquatch-v4be', 'sasquatch']}]}}, 'unclassified')
    case('two-name set', head + ('| two | `squashfs_v4*` | `a+b` | `none` | `n/a` | `no` | `*` | x | y |\n'),
         {'normalized_result': {'chunks': [{'handler': 'squashfs_v4_le'}], 'files': [{}],
                                'extraction_gaps': [{'kind': 'b', 'dependencies': []},
                                                    {'kind': 'a', 'dependencies': []}]}}, 'two')
    # symlink removed accepted from raw_result.report
    sr = head + ('| esc | `squashfs_v4*` | `none` | `none` | `n/a` | `yes` | `>0` | x | y |\n')
    case('sr from raw report', sr, {'normalized_result': {'chunks': [{'handler': 'squashfs_v4_be'}],
                                                          'files': [{}], 'diagnostics': []},
                                    'raw_result': {'report': [{'reports': [
                                        {'__typename__': 'MaliciousSymlinkRemoved'}]}]}}, 'esc')
    # malformed
    bad('missing section', '## Other\n' + MARKER + '\n| a |\n')
    bad('missing marker', '## Queue-drain craft\n\n| x |\n')
    bad('missing table', '## Queue-drain craft\n\n' + MARKER + '\n\nno table here\n')
    bad('header wrong order', '## Queue-drain craft\n\n' + MARKER + '\n\n| handler | label | gap kinds | '
        'dependencies | -be in child argv | symlink removed | published files | cause -> action | source |\n'
        + '|' + '---|' * len(HEADER) + '\n')
    bad('bad -be cell', head + '| x | `squashfs_v4*` | `none` | `none` | `maybe` | `no` | `>0` | x | y |\n')
    bad('bad published cell', head + '| x | `squashfs_v4*` | `none` | `none` | `n/a` | `no` | `many` | x | y |\n')
    bad('empty set token', head + '| x | `squashfs_v4*` | `a++b` | `none` | `n/a` | `no` | `>0` | x | y |\n')
    bad('short row', head + '| x | `squashfs_v4*` | `none` | `none` | `n/a` | `no` | `>0` | x |\n')
    for f in fails:
        print('FAIL', f)
    print(f'selftest: {len(fails)} failure(s)')
    return 1 if fails else 0


def main(argv):
    if '--selftest' in argv:
        return selftest()
    table_path = None
    label_only = False
    envs = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == '--table':
            i += 1
            table_path = argv[i]
        elif a == '--label':
            label_only = True
        else:
            envs.append(a)
        i += 1
    if not table_path:
        print('usage: sqfs-triage-ref.py --table <DOC> [--label] ENVELOPE...', file=sys.stderr)
        return 2
    try:
        rules = parse_table(open(table_path, encoding='utf-8').read())
    except Unevaluable as e:
        print(f'unevaluable: {e}', file=sys.stderr)
        return 2
    out = {}
    for p in envs:
        label, f = classify(rules, json.load(open(p)))
        out[p.rsplit('/', 1)[-1][:-5]] = {
            'label': label,
            'features': {'H': sorted(f['H']), 'G': sorted(f['G']), 'D': sorted(f['D']),
                         'BE': f['BE'], 'SR': f['SR'], 'P': f['P']}}
    if label_only:
        for k, v in out.items():
            print(f'{k}\t{v["label"]}')
    else:
        print(json.dumps(out, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
