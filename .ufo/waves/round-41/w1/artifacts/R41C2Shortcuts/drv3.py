#!/usr/bin/env python3
"""R41C2Shortcuts v3-grammar probe.

The draft names table `v3` but no v3 interpreter or grammar exists at the base
(`tools/round-41/` absent; the only parsers are v1/v2).  This file evaluates
tables in the MINIMAL grammar delta that makes the draft's predicate satisfiable:
the same 12 columns as v2, the same unique-label rule, plus one additional set
cell form

    `+a` / `+a+b`   -> the envelope set must CONTAIN {a,b}   (superset test)

(`*` any, `none` empty, `a+b` exact-as-v2 keep their meaning).  Everything else
is delegated to the frozen v2 parser so the comparison is apples to apples:
rows are parsed by sqfs-triage-v2.parse_table-shaped code below, and features
come from sqfs-triage-v2.features.
"""
import argparse
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('d2', os.path.join(HERE, 'drv2.py'))
d2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d2)
tri = d2.tri

CONTAINS = '+'


def parse_set(cell):
    if cell == '*':
        return ('any', None)
    if cell == 'none':
        return ('none', None)
    if cell.startswith(CONTAINS):
        parts = cell[1:].split('+')
        if any(not p for p in parts):
            raise ValueError('empty member in %r' % cell)
        return ('superset', frozenset(parts))
    return ('exact', frozenset(cell.split('+')))


def matches(spec, values):
    kind, payload = spec
    if kind == 'any':
        return True
    if kind == 'none':
        return not values
    if kind == 'superset':
        return payload <= frozenset(values)
    return frozenset(values) == payload


def parse_rows(rows):
    out = []
    labels = set()
    for r in rows:
        cells = [tri.clean_cell(c) for c in r]
        label, op, pv, handler, gap, dep, be, sr, files, action = cells[:10]
        if label in labels:
            raise ValueError('duplicate label %r' % label)
        labels.add(label)
        out.append({'label': label, 'operation': op, 'provider': pv,
                    'handler': tri._parse_handler_cell(handler),
                    'gap_kinds': parse_set(gap), 'dependencies': parse_set(dep),
                    'be': be, 'symlink_removed': sr, 'files': files,
                    'action': action})
    return out


def rule_matches(rule, f):
    if rule['operation'] != '*' and rule['operation'] != f['OP']:
        return False
    if rule['provider'] != '*' and rule['provider'] != f['PV']:
        return False
    kind, payload = rule['handler']
    if kind == 'none':
        if f['H']:
            return False
    elif kind == 'pattern':
        import fnmatch
        if not any(fnmatch.fnmatchcase(v, payload) for v in f['H']):
            return False
    if not matches(rule['gap_kinds'], f['G']):
        return False
    if not matches(rule['dependencies'], f['D']):
        return False
    for col, key in (('be', 'BE'), ('symlink_removed', 'SR')):
        if rule[col] != '*' and rule[col] != f[key]:
            return False
    if rule['files'] == '0' and f['P'] != 0:
        return False
    if rule['files'] == '>0' and f['P'] <= 0:
        return False
    return True


def classify(rules, f):
    for rule in rules:
        if rule_matches(rule, f):
            return rule
    return None


def row(label, action, op='extract_firmware', pv='unblob', handler='squashfs_v4_*',
        gaps='*', deps='*', be='*', sr='*', files='*'):
    return [label, '`%s`' % op, '`%s`' % pv, '`%s`' % handler, '`%s`' % gaps,
            '`%s`' % deps, '`%s`' % be, '`%s`' % sr, '`%s`' % files,
            '`%s`' % action, 'probe row -> %s' % action, 'plans/round-41-claims.md rows 1-12']


def T_contains():
    """12 rows = the unique-label floor; precedence rows 1-11 with contains cells."""
    return [
        row('no-squashfs-chunk', 'inspect-input', handler='none'),
        row('dep-missing-be', 'install-extractor-be', gaps='+missing-extractor-dependency',
            deps='+sasquatch-v4be'),
        row('dep-missing-le', 'install-extractor-le', gaps='+missing-extractor-dependency',
            deps='+sasquatch'),
        row('partial-body-failure', 'salvage-partial', gaps='+extractor-failure', files='>0'),
        row('avm-marker-be-dropped', 'wrap-extractor-be', handler='squashfs_v4_be',
            gaps='+extractor-failure', be='no', files='0'),
        row('body-extractor-failure', 'preserve-failure', gaps='+extractor-failure', files='0'),
        row('depth-limited-nested', 'descend-depth', gaps='+depth-limited'),
        row('mixed-symlinks', 'audit-symlinks', gaps='+unpublished-entry', sr='yes'),
        row('escaping-symlink-removed', 'expect-link-absent', gaps='none', sr='yes'),
        row('in-tree-symlink-metadata', 'count-gap', gaps='+unpublished-entry', sr='no'),
        row('clean', 'none', gaps='none', sr='no', files='>0'),
        row('clean-empty', 'confirm-empty', gaps='none', sr='no', files='0'),
    ]


def v(fn):
    def build():
        rows = T_contains()
        fn(rows)
        return rows
    return build


def v_drop(label):
    def fn(rows):
        rows[:] = [r for r in rows if r[0] != label]
    return fn


def v_handler_star_on_avm(rows):
    for r in rows:
        if r[0] == 'avm-marker-be-dropped':
            r[3] = '`*`'


def v_handler_star_all(rows):
    for r in rows[1:]:
        r[3] = '`*`'


def v_dep_star(rows):
    for r in rows:
        r[5] = '`*`'


def v_op_star(rows):
    for r in rows:
        r[1] = '`*`'


def v_pv_star(rows):
    for r in rows:
        r[2] = '`*`'


def v_no_domain(rows):
    rows[0][1] = '`*`'
    rows[0][2] = '`*`'


def v_no_be(rows):
    for r in rows:
        r[6] = '`*`'


def v_files_star(rows):
    for r in rows:
        r[8] = '`*`'


def v_gaps_exact_all(rows):
    for r in rows:
        if r[4].startswith('`+'):
            r[4] = '`' + r[4][2:-1] + '`'


def v_no_sr(rows):
    for r in rows:
        r[7] = '`*`'


def v_dep_star_by_handler(rows):
    for r in rows:
        if r[0] == 'dep-missing-be':
            r[3] = '`squashfs_v4_be`'
            r[5] = '`*`'
        if r[0] == 'dep-missing-le':
            r[3] = '`squashfs_v4_le`'
            r[5] = '`*`'


def v_wildcard_partial(rows):
    """replace the ef-contains partial row with a trailing any-gap row"""
    rows[:] = [r for r in rows if r[0] != 'partial-body-failure']
    rows.append(row('partial-body-failure', 'salvage-partial', gaps='*', files='>0'))


def v_dl_first(rows):
    dl = [r for r in rows if r[0] == 'depth-limited-nested']
    rest = [r for r in rows if r[0] != 'depth-limited-nested']
    rows[:] = dl + rest


def v_dl_first_star(rows):
    v_dl_first(rows)
    rows[0][3] = '`*`'


def v_exact_cells(rows):
    """v2 exact cells transcribed into the fake v3 grammar (the kill-rule control)"""
    for r in rows:
        if r[0] == 'partial-body-failure':
            r[4] = '`extractor-failure`'
        if r[0] in ('depth-limited-nested', 'mixed-symlinks', 'in-tree-symlink-metadata'):
            if r[4].startswith('`+'):
                r[4] = '`' + r[4][2:-1] + '`'


def v_star_default(rows):
    rows.append(row('unclassified', 'none', op='*', pv='*', handler='*', gaps='*',
                    deps='*', be='*', sr='*', files='*'))


CANDIDATES = [
    ('T_contains', T_contains, '12 rows, contains cells: the precedence-faithful minimum'),
    ('S_avm_handler_star', v(v_handler_star_on_avm),
     'handler cell dropped from the AVM row only'),
    ('S_handler_star_all', v(v_handler_star_all), 'handler cell dropped from every row but no-chunk'),
    ('S_dep_star', v(v_dep_star), 'dependencies cells dropped'),
    ('S_dep_star_by_handler', v(v_dep_star_by_handler),
     'dependencies dropped, dep rows split on the handler cell'),
    ('S_op_star', v(v_op_star), 'operation cell dropped everywhere'),
    ('S_pv_star', v(v_pv_star), 'provider cell dropped everywhere'),
    ('S_no_domain', v(v_no_domain), 'no operation/provider guard at all'),
    ('S_files_star', v(v_files_star), 'published-files column dropped'),
    ('S_no_be', v(v_no_be), '-be column dropped'),
    ('S_no_sr', v(v_no_sr), 'symlink-removed column dropped'),
    ('S_wildcard_partial', v(v_wildcard_partial), 'partial row widened to any gap set, moved last'),
    ('S_dl_first', v(v_dl_first), 'depth-limited row moved to the top'),
    ('S_dl_first_star', v(v_dl_first_star), 'depth-limited row first AND handler dropped'),
    ('S_exact_cells', v(v_exact_cells), 'v2 exact cells transcribed into v3 (kill-rule control)'),
    ('S_star_default', v(v_star_default), 'all-* default row appended'),
]
for _lbl in ('mixed-symlinks', 'depth-limited-nested', 'partial-body-failure', 'clean-empty',
             'no-squashfs-chunk', 'escaping-symlink-removed', 'in-tree-symlink-metadata',
             'body-extractor-failure', 'avm-marker-be-dropped', 'dep-missing-be',
             'dep-missing-le', 'clean'):
    CANDIDATES.append(('S_drop__' + _lbl, v(v_drop(_lbl)), 'row %r removed' % _lbl))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ns = ap.parse_args()
    os.makedirs(os.path.join(ns.out, 'tables-v3'), exist_ok=True)

    planned, probes = [], d2.build_probes()
    import glob
    for d in sorted(glob.glob(os.path.join(d2.HELDOUT, 'H*'))):
        hid = os.path.basename(d)
        with open(os.path.join(d, 'run.json')) as fh:
            run = json.load(fh)
        env = d2.load(hid)
        planned.append({'id': hid, 'class': run['class'],
                        'features': tri.features(tri.envelope_data(env, hid))})
    combined = [p for p in probes if p['id'].startswith('C')]
    exposure = [p for p in probes if p['id'].startswith('X')]
    classes = sorted({p['class'] for p in planned} | {p['class'] for p in combined})

    report = {'classes': classes, 'candidates': []}
    for name, fn, why in CANDIDATES:
        rows = fn()
        rules = parse_rows(rows)
        res = []
        for item in planned + combined + exposure:
            rule = classify(rules, item['features'])
            got = (rule['label'], rule['action']) if rule else ('unclassified', 'none')
            want = d2.precedence(item['features'])
            label_ok = got[0] == want[0]
            pair_ok = label_ok and (want[1] == d2.UNSPEC or got[1] == want[1])
            res.append({'id': item['id'], 'class': item['class'], 'got': got, 'want': want,
                        'pair_ok': pair_ok})
        by_class = {}
        for r in res:
            if r['class'] in classes:
                by_class.setdefault(r['class'], []).append(r['pair_ok'])
        passed = sum(1 for c, v_ in by_class.items() if all(v_))
        missed = sorted(c for c, v_ in by_class.items() if not all(v_))
        xdiv = sorted(r['id'] for r in res if r['id'].startswith('X') and not r['pair_ok'])
        report['candidates'].append({'name': name, 'why': why, 'rows': len(rows),
                                     'classes_passed': passed, 'classes_total': len(by_class),
                                     'missed': missed, 'exposure_divergences': xdiv})
        d2_rows = rows
        with open(os.path.join(ns.out, 'tables-v3', name + '.md'), 'w') as fh:
            fh.write(d2.skill_doc(d2_rows, d2.ACTIONS, marker='v3-pseudo'))
            fh.write('')  # keep v3-pseudo marker: v2 parser must reject it
    for c in report['candidates']:
        print('%-28s rows=%2d %2d/%2d missed=%s Xdiv=%s'
              % (c['name'], c['rows'], c['classes_passed'], c['classes_total'],
                 ','.join(c['missed']) or '-', ','.join(c['exposure_divergences']) or '-'))
    with open(os.path.join(ns.out, 'score-v3grammar.json'), 'w') as fh:
        json.dump(report, fh, indent=2, sort_keys=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
