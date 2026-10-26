#!/usr/bin/env python3
"""check-draft.py - seat conformance check for the round-40 triage table v2 draft.

Reads only lane bytes (SKILL-shaped block, round-39 receipts, round-39 held-out
envelopes, round-39 w2 shape files, round-26 out-of-domain envelope).  Runs no REA,
no unblob, no sasquatch, and writes nothing outside a TMPDIR work directory.

Usage: python3 -I -B check-draft.py [--block PATH] [--json]
Exit 0 iff every case passes, 1 otherwise, 2 on an unreadable input.
"""
import argparse
import copy
import fnmatch
import importlib.util
import json
import os
import re
import sys
import tempfile

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
DEFAULT_BLOCK = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'block.md')
V1 = LANE + '/tools/round-39/sqfs-triage.py'
MARKER = '<!-- sqfs-triage-table v2 -->'
ACTIONS_RE = re.compile(r'^\s*<!--\s*sqfs-triage-actions:\s*(.+?)\s*-->\s*$')
HEADER = ['label', 'operation', 'provider', 'handler', 'gap kinds', 'dependencies',
          '-be in child argv', 'symlink removed', 'published files', 'action', 'cause',
          'source']
NAME_RE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.\-]*$')
HANDLER_RE = re.compile(r'^[A-Za-z0-9_?*.\-\[\]]+$')
SEPARATOR_RE = re.compile(r'^:?-+:?$')
BE_VALUES = ('yes', 'no', 'n/a')
FILES_VALUES = ('0', '>0')


class TableError(Exception):
    pass


def load_v1():
    spec = importlib.util.spec_from_file_location('tri_v1', V1)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def clean_cell(raw):
    s = raw.strip()
    if len(s) >= 2 and s[0] == '`' and s[-1] == '`' and s.count('`') == 2:
        s = s[1:-1].strip()
    return s


def split_row(line):
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|'):
        s = s[:-1]
    return s.split('|')


def craft_bounds(lines):
    start = None
    for i, line in enumerate(lines):
        if line.startswith('## ') and not line.startswith('### ') \
                and line[3:].strip().lower().startswith('queue-drain craft'):
            start = i + 1
            break
    if start is None:
        raise TableError('no "## Queue-drain craft" heading')
    for j in range(start, len(lines)):
        if lines[j].startswith('## ') and not lines[j].startswith('### '):
            return start, j
    return start, len(lines)


def parse_doc(text):
    lines = text.splitlines()
    start, end = craft_bounds(lines)
    marker = None
    for i in range(start, end):
        if MARKER in lines[i]:
            marker = i
            break
    if marker is None:
        raise TableError('marker %r absent from the craft section' % MARKER)
    i = marker + 1
    while i < end and not lines[i].lstrip().startswith('|'):
        i += 1
    if i >= end:
        raise TableError('no markdown table after the marker')
    if i == 0:
        raise TableError('table header has no line above it')
    m = ACTIONS_RE.match(lines[i - 1])
    if not m:
        raise TableError('the line directly above the table header is not a '
                         'sqfs-triage-actions declaration: %r' % lines[i - 1])
    vocab = m.group(1).split()
    if not vocab:
        raise TableError('empty action vocabulary')
    if len(set(vocab)) != len(vocab):
        raise TableError('action vocabulary repeats a token: %r' % vocab)
    table = []
    while i < end and lines[i].lstrip().startswith('|'):
        table.append(lines[i])
        i += 1
    header = [clean_cell(c) for c in split_row(table[0])]
    if header != HEADER:
        raise TableError('header %r, expected %r' % (header, HEADER))
    sep = [clean_cell(c) for c in split_row(table[1])]
    if len(sep) != len(HEADER) or not all(SEPARATOR_RE.match(c) for c in sep):
        raise TableError('second row is not a %d-cell separator' % len(HEADER))
    rules = []
    labels = set()
    for raw in table[2:]:
        cells = [clean_cell(c) for c in split_row(raw)]
        if len(cells) != len(HEADER):
            raise TableError('row has %d cells: %r' % (len(cells), cells[0][:40]))
        label, op, prov, handler, gaps, deps, be, sr, files, action, cause, source = cells
        if not label or label in labels:
            raise TableError('empty or duplicate label %r' % label)
        labels.add(label)
        for column, cell in (('operation', op), ('provider', prov)):
            if cell != '*' and not NAME_RE.match(cell):
                raise TableError('%s cell %r is not * or an exact identifier'
                                 % (column, cell))
        for column, cell in (('-be in child argv', be), ('symlink removed', sr)):
            if cell != '*' and cell not in BE_VALUES:
                raise TableError('%s cell %r is not yes/no/n-a/*' % (column, cell))
        if files not in FILES_VALUES + ('*',):
            raise TableError('published files cell %r is not 0/>0/*' % files)
        if handler not in ('*', 'none') and not HANDLER_RE.match(handler):
            raise TableError('handler cell %r is not */none/fnmatch' % handler)
        sets = {}
        for column, cell in (('gap kinds', gaps), ('dependencies', deps)):
            if cell == '*':
                sets[column] = ('any', None)
            elif cell == 'none':
                sets[column] = ('none', None)
            else:
                parts = cell.split('+')
                if any(not NAME_RE.match(p) for p in parts) or len(set(parts)) != len(parts):
                    raise TableError('%s cell %r is malformed' % (column, cell))
                sets[column] = ('exact', frozenset(parts))
        if action not in vocab:
            raise TableError('action %r is not in the declared vocabulary' % action)
        if not cause or not source:
            raise TableError('label %r has an empty cause or source' % label)
        rules.append({'label': label, 'operation': op, 'provider': prov,
                      'handler': handler, 'gaps': sets['gap kinds'],
                      'deps': sets['dependencies'], 'be': be, 'sr': sr,
                      'files': files, 'action': action,
                      'cells': cells})
    if not rules:
        raise TableError('no rule rows')
    return rules, vocab


def match_set(spec, values):
    kind, payload = spec
    if kind == 'any':
        return True
    if kind == 'none':
        return not values
    return frozenset(values) == payload


def matches(rule, f):
    if rule['operation'] != '*' and rule['operation'] != f['OP']:
        return False
    if rule['provider'] != '*' and rule['provider'] != f['PV']:
        return False
    if rule['handler'] == 'none':
        if f['H']:
            return False
    elif rule['handler'] != '*' and not any(
            fnmatch.fnmatchcase(h, rule['handler']) for h in f['H']):
        return False
    if not match_set(rule['gaps'], f['G']):
        return False
    if not match_set(rule['deps'], f['D']):
        return False
    if rule['be'] != '*' and rule['be'] != f['BE']:
        return False
    if rule['sr'] != '*' and rule['sr'] != f['SR']:
        return False
    if rule['files'] == '0' and f['P'] != 0:
        return False
    if rule['files'] == '>0' and f['P'] <= 0:
        return False
    return True


def classify(rules, f):
    hits = [r for r in rules if matches(r, f)]
    return hits


def deep_get_op_pv(data):
    op = data.get('operation') if isinstance(data.get('operation'), str) else ''
    prov = data.get('provider') if isinstance(data.get('provider'), dict) else {}
    pv = prov.get('id') if isinstance(prov.get('id'), str) else ''
    return op, pv


def featurise(tri, obj, path):
    data = tri.envelope_data(obj, path)
    f = tri.features(data)
    f['OP'], f['PV'] = deep_get_op_pv(data)
    return f


def bio(tri, path, mutate=None):
    with open(path, 'r', encoding='utf-8') as handle:
        obj = json.load(handle)
    if mutate is not None:
        obj = mutate(copy.deepcopy(obj))
    return featurise(tri, obj, path)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--block', default=DEFAULT_BLOCK)
    ap.add_argument('--skill', default=None,
                    help='parse a whole SKILL document instead of wrapping --block')
    ap.add_argument('--json', action='store_true')
    ns = ap.parse_args(argv)
    tri = load_v1()
    try:
        with open(ns.block, 'r', encoding='utf-8') as handle:
            block = handle.read()
    except OSError as exc:
        print('block unreadable: %s' % exc, file=sys.stderr)
        return 2
    work = tempfile.mkdtemp(prefix='sqfs-v2-check-')
    if ns.skill:
        skill = ns.skill
    else:
        skill = os.path.join(work, 'SKILL.md')
        with open(skill, 'w', encoding='utf-8') as handle:
            handle.write('# SKILL\n\n## Queue-drain craft\n\nProse.\n\n'
                         + block + '\n## A later section\n\nTail.\n')
    cases = []
    fails = []

    def add(name, feat, want_label, want_action, note=''):
        cases.append({'case': name, 'features': feat, 'want_label': want_label,
                      'want_action': want_action, 'note': note})

    # ---- round-39 held-out envelopes (real bytes, published) -------------------------
    held = LANE + '/corpus/evidence/round-39/c2/heldout'
    if os.path.isdir(held):
        with open(os.path.join(held, 'manifest.json'), 'r', encoding='utf-8') as handle:
            manifest = json.load(handle)
        for carrier in manifest['carriers']:
            path = os.path.join(held, carrier['id'], 'envelope.json')
            f = bio(tri, path)
            add('held:%s/%s' % (carrier['id'], carrier['class']), f,
                carrier['label'], ACTION[carrier['label']],
                'manifest label %r' % carrier['label'])

    # ---- round-39 Core receipts (real bytes) ----------------------------------------
    for key, want in (('K1', 'escaping-symlink-removed'), ('K2', 'in-tree-symlink-metadata'),
                      ('K3', 'clean'), ('K4', 'clean'),
                      ('K5', 'mixed-symlinks'), ('K6', 'mixed-symlinks')):
        path = LANE + '/corpus/evidence/round-39/c1/%s/after.json' % key
        if os.path.exists(path):
            add('c1:%s' % key, bio(tri, path), want, ACTION[want])

    # ---- measured round-39 w2 shapes, given the domain fields REA emits --------------
    shapes = LANE + '/.ufo/waves/round-39/w2/artifacts/R39W2C2TableReview'
    dom = lambda o: dict(o, operation='extract_firmware',
                         provider={'id': 'unblob', 'name': 'Unblob', 'version': '26.6.4'})
    for name, want in (('xz-shape.json', 'partial-body-failure'),
                       ('dirempty-shape.json', 'clean-empty')):
        path = os.path.join(shapes, name)
        if os.path.exists(path):
            add('w2:%s' % name, bio(tri, path, dom), want, ACTION[want])

    # ---- out of domain ---------------------------------------------------------------
    k1 = LANE + '/corpus/evidence/round-39/c1/K1/after.json'
    for name, mutate in (
            ('ood:operation', lambda o: dict(o, operation='analyze_function')),
            ('ood:operation-inspect', lambda o: dict(o, operation='inspect_firmware_regions')),
            ('ood:provider', lambda o: dict(o, provider={'id': 'ghidra', 'name': 'Ghidra'})),
            ('ood:provider-binwalk', lambda o: dict(o, provider={'id': 'binwalk'})),
            ('ood:no-domain', lambda o: {k: v for k, v in o.items()
                                         if k not in ('operation', 'provider')})):
        add(name, bio(tri, k1, mutate), 'unclassified', 'none')

    # ---- parse and classify ----------------------------------------------------------
    try:
        rules, vocab = parse_doc(open(skill, 'r', encoding='utf-8').read())
    except TableError as exc:
        print('TABLE ERROR: %s' % exc, file=sys.stderr)
        return 2

    star_cells = sum(1 for r in rules for c in r['cells'] if c == '*')
    for case in cases:
        hits = classify(rules, case['features'])
        case['rules'] = [r['label'] for r in hits]
        if len(hits) > 1:
            fails.append('%s: %d rows match (%s) - vectors are not disjoint'
                         % (case['case'], len(hits), ','.join(case['rules'])))
            continue
        got_label = hits[0]['label'] if hits else 'unclassified'
        got_action = hits[0]['action'] if hits else 'none'
        case['got_label'] = got_label
        case['got_action'] = got_action
        case['ok'] = (got_label == case['want_label'] and got_action == case['want_action'])
        if not case['ok']:
            fails.append('%s: got (%s, %s), want (%s, %s)'
                         % (case['case'], got_label, got_action,
                            case['want_label'], case['want_action']))

    # ---- controls: each must lose at least one case ----------------------------------
    controls = []

    def control(name, mutate_fn, expect_wrong):
        text = '| ' + ' | '.join(HEADER) + ' |\n| ' + ' | '.join(['---'] * len(HEADER)) + ' |\n'
        text += ''.join('| ' + ' | '.join(mutate_fn(r) or r['cells']) + ' |\n' for r in rules)
        doc = ('# SKILL\n\n## Queue-drain craft\n\nProse.\n\n' + MARKER + '\n'
               '<!-- sqfs-triage-actions: ' + ' '.join(vocab) + ' -->\n' + text
               + '\n## A later section\n\nTail.\n')
        try:
            ctl_rules, _ = parse_doc(doc)
        except TableError as exc:
            controls.append({'control': name, 'outcome': 'exit 2: %s' % exc, 'passed': False})
            return
        wrong = 0
        for case in cases:
            hits = classify(ctl_rules, case['features'])
            if len(hits) > 1:
                wrong += 1
                continue
            got = (hits[0]['label'], hits[0]['action']) if hits else ('unclassified', 'none')
            if got != (case['want_label'], case['want_action']):
                wrong += 1
        controls.append({'control': name, 'wrong': wrong, 'of': len(cases),
                         'expect_wrong': expect_wrong, 'passed': wrong == expect_wrong})

    def catch_all(row):
        cells = list(row['cells'])
        cells[1] = cells[2] = cells[3] = cells[4] = cells[5] = '*'
        cells[6] = cells[7] = cells[8] = '*'
        return cells

    control('catch-all domain/default row', catch_all, len(cases))
    control('label-right/action-wrong (clean)',
            lambda r: (lambda c: (c.__setitem__(9, 'check-superblock'), c)[1])(list(r['cells']))
            if r['label'] == 'clean' else None,
            sum(1 for c in cases if c['want_label'] == 'clean'))

    try:
        parse_doc('# SKILL\n\n## Queue-drain craft\n\n' + MARKER + '\n'
                  '<!-- sqfs-triage-actions: accept -->\n| '
                  + ' | '.join(HEADER) + ' |\n| ' + ' | '.join(['---'] * len(HEADER)) + ' |\n'
                  + '| a | `extract_firmware` | `unblob` | `none` | `none` | `none` | `n/a` '
                  '| `no` | `0` | `accept` | c | s |\n| a | `extract_firmware` | `unblob` '
                  '| `none` | `none` | `none` | `n/a` | `no` | `0` | `accept` | c | s |\n')
        duplicate = 'NOT REFUSED'
    except TableError:
        duplicate = 'exit 2'
    try:
        parse_doc('# SKILL\n\n## Queue-drain craft\n\n' + MARKER + '\n'
                  '<!-- sqfs-triage-actions: accept -->\n| '
                  + ' | '.join(HEADER) + ' |\n| ' + ' | '.join(['---'] * len(HEADER)) + ' |\n'
                  + '| a | `extract_firmware` | `unblob` | `none` | `none` | `none` | `n/a` '
                  '| `no` | `0` | `accept-and-more` | c | s |\n')
        unknown = 'NOT REFUSED'
    except TableError:
        unknown = 'exit 2'

    # ---- ablation: which condition columns carry the decisions -----------------------
    ablation = []
    for idx, column in ((1, 'operation'), (2, 'provider'), (3, 'handler'),
                        (4, 'gap kinds'), (5, 'dependencies'), (6, '-be in child argv'),
                        (7, 'symlink removed'), (8, 'published files')):
        text = '| ' + ' | '.join(HEADER) + ' |\n| ' + ' | '.join(['---'] * len(HEADER)) + ' |\n'
        for rule in rules:
            cells = list(rule['cells'])
            cells[idx] = '*'
            text += '| ' + ' | '.join(cells) + ' |\n'
        doc = ('# SKILL\n\n## Queue-drain craft\n\nProse.\n\n' + MARKER + '\n'
               '<!-- sqfs-triage-actions: ' + ' '.join(vocab) + ' -->\n' + text
               + '\n## A later section\n\nTail.\n')
        abl_rules, _ = parse_doc(doc)
        lost = []
        for case in cases:
            hits = classify(abl_rules, case['features'])
            if hits:
                got = (hits[0]['label'], hits[0]['action'])
            else:
                got = ('unclassified', 'none')
            if got != (case['want_label'], case['want_action']):
                lost.append(case['case'])
        ablation.append({'column': column, 'lost': len(lost), 'of': len(cases),
                         'cases': lost})
        if not lost:
            fails.append('column %r is decorative: dropping it loses no case' % column)

    # ---- control: the frozen v1 table transcribed into the v2 shape ------------------
    v1_rows = []
    for raw in tri.TABLE_BLOCK.strip().splitlines():
        if not raw.lstrip().startswith('|'):
            continue
        cells = [clean_cell(c) for c in split_row(raw)]
        if len(cells) != 9 or cells[0].lower() == 'label' or set(cells[0]) == {'-'}:
            continue
        v1_rows.append(cells)
    text = '| ' + ' | '.join(HEADER) + ' |\n| ' + ' | '.join(['---'] * len(HEADER)) + ' |\n'
    for label, handler, gaps, deps, be, sr, files, cause, source in v1_rows:
        text += '| ' + ' | '.join([label, '*', '*', handler, gaps, deps, be, sr, files,
                                   ACTION[label], 'transcribed cause', source]) + ' |\n'
    v1_doc = ('# SKILL\n\n## Queue-drain craft\n\nProse.\n\n' + MARKER + '\n'
              '<!-- sqfs-triage-actions: ' + ' '.join(vocab) + ' -->\n' + text
              + '\n## A later section\n\nTail.\n')
    v1_rules, _ = parse_doc(v1_doc)
    v1_lost = []
    for case in cases:
        hits = classify(v1_rules, case['features'])
        got = (hits[0]['label'], hits[0]['action']) if hits else ('unclassified', 'none')
        if got != (case['want_label'], case['want_action']):
            v1_lost.append(case['case'])
    v1_control = {'control': 'v1 rows transcribed with `*` domain cells',
                  'rows': len(v1_rules), 'wrong': len(v1_lost), 'of': len(cases),
                  'cases': v1_lost}
    must = ['ood:operation', 'ood:provider', 'w2:xz-shape.json', 'w2:dirempty-shape.json',
            'c1:K5', 'c1:K6']
    missing = [name for name in must if name not in v1_lost]
    if missing:
        fails.append('v1 transcription control keeps %r; the v2 rows for them are not '
                     'load-bearing' % missing)

    by_label = {}
    for case in cases:
        if 'got_label' in case:
            by_label.setdefault(case['got_label'], set()).add(case['got_action'])
    shared = {k: sorted(v) for k, v in by_label.items() if len(v) > 1}
    if shared:
        fails.append('one label carries two actions: %r' % shared)
    if duplicate != 'exit 2':
        fails.append('duplicate label was not refused')
    if unknown != 'exit 2':
        fails.append('action outside the vocabulary was not refused')
    for ctl in controls:
        if not ctl['passed']:
            fails.append('control %r did not behave (%r)' % (ctl['control'], ctl))

    report = {
        'block': ns.block,
        'skill': skill,
        'rules': len(rules),
        'labels': [r['label'] for r in rules],
        'vocabulary': vocab,
        'cells': len(rules) * len(HEADER),
        'bare_star_cells': star_cells,
        'cases': cases,
        'controls': controls,
        'ablation': ablation,
        'v1_transcription': v1_control,
        'duplicate_label': duplicate,
        'unknown_action': unknown,
        'failures': fails,
        'verdict': 'PASS' if not fails else 'FAIL',
    }
    if ns.json:
        json.dump(report, sys.stdout, indent=1, sort_keys=True)
        sys.stdout.write('\n')
    else:
        print('block: %s' % ns.block)
        print('rules: %d  vocabulary: %d  cells: %d  bare * cells: %d'
              % (len(rules), len(vocab), len(rules) * len(HEADER), star_cells))
        for case in cases:
            print('%-42s %-26s %-30s %s'
                  % (case['case'], case.get('got_label', '-'),
                     case.get('got_action', '-'), 'ok' if case.get('ok') else 'FAIL'))
        for ctl in controls:
            print('control: %-40s %s' % (ctl['control'], 'ok' if ctl['passed'] else 'FAIL'))
        print('v1 transcription control: %d/%d wrong  %s'
              % (v1_control['wrong'], v1_control['of'], ','.join(v1_control['cases'])))
        for ab in ablation:
            print('ablate %-20s loses %d/%d %s'
                  % (ab['column'], ab['lost'], ab['of'],
                     ','.join(ab['cases']) if 0 < ab['lost'] <= 6 else ''))
        print('duplicate label: %s   unknown action: %s' % (duplicate, unknown))
        print('verdict: %s%s' % (report['verdict'],
                                 '' if not fails else '  (' + '; '.join(fails) + ')'))
    return 0 if not fails else 1


ACTION = {
    'no-squashfs-chunk': 'check-superblock',
    'dep-missing-be': 'install-sasquatch-v4be',
    'dep-missing-le': 'install-sasquatch',
    'avm-marker-be-dropped': 'rerun-with-be-wrapper',
    'body-extractor-failure': 'keep-failure-evidence',
    'partial-body-failure': 'accept-partial-published',
    'mixed-symlinks': 'expect-removed-and-unpublished',
    'escaping-symlink-removed': 'expect-removed',
    'in-tree-symlink-metadata': 'resolve-unpublished',
    'clean': 'accept',
    'clean-empty': 'accept',
}

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
