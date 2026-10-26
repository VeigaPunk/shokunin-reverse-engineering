#!/usr/bin/env python3
"""R41C2Shortcuts v2 driver.

Planned-class tuple set
  * 13 `v2` classes  -> features parsed from the COMMITTED round-40 heldout
    envelopes (corpus/evidence/round-40/c2/heldout/H*/envelope.json)
  * 5 combined classes -> SYNTHETIC probe envelopes derived from those committed
    envelopes by adding the gap kind / symlink-removal report the class names,
    with the expected pair taken from plans/round-41-claims.md rows 1-12
    (hand-transcribed in precedence(); the round-40 independent evaluator was
    NOT read).

Every candidate table is parsed by the frozen round-40 interpreter
(tools/round-40/sqfs-triage-v2.py) -- the only grammar that exists today -- and
scored by (label, action) pair per envelope.
"""
import argparse
import copy
import glob
import importlib.util
import json
import os
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
INTERP = os.path.join(LANE, 'tools/round-40/sqfs-triage-v2.py')
HELDOUT = os.path.join(LANE, 'corpus/evidence/round-40/c2/heldout')
SKILL = os.path.join(LANE, 'SKILL.md')

spec = importlib.util.spec_from_file_location('tri', INTERP)
tri = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tri)

DEP = 'missing-extractor-dependency'
COMBINED = ['partial+in-tree', 'partial+mixed', 'depth-limited-alone',
            'depth-limited+in-tree', 'depth-limited+mixed']
UNSPEC = '<action-unspecified-in-draft>'


# ---------------------------------------------------------------- envelope I/O
def load(hid):
    with open(os.path.join(HELDOUT, hid, 'envelope.json'), 'r', encoding='utf-8') as fh:
        return json.load(fh)


def dref(env):
    return env['data'] if isinstance(env.get('data'), dict) else env


def nr(env):
    return dref(env)['normalized_result']


def _walk_commands(node):
    if isinstance(node, dict):
        for key, val in node.items():
            if key == 'command':
                yield node, key
            yield from _walk_commands(val)
    elif isinstance(node, list):
        for item in node:
            yield from _walk_commands(item)


def strip_be(env):
    """Rewrite every recorded sasquatch-v4be '-be' argv to plain sasquatch."""
    hits = 0
    for parent, key in _walk_commands(dref(env)):
        val = parent[key]
        if isinstance(val, str) and '-be' in val:
            parent[key] = val.replace('sasquatch-v4be -be', 'sasquatch').replace(' -be ', ' ')
            hits += 1
        elif isinstance(val, list) and '-be' in val:
            parent[key] = [t for t in val if t != '-be']
            parent[key][0] = 'sasquatch'
            hits += 1
    return hits


def set_chunks(env, handlers):
    c = nr(env)
    if not handlers:
        c['chunks'] = []
        return
    proto = c['chunks'][0]
    c['chunks'] = []
    for h in handlers:
        new = copy.deepcopy(proto)
        new['handler'] = h
        c['chunks'].append(new)


def add_gap(env, kind, handler=None, deps=None, rel=None):
    c = nr(env)
    c.setdefault('extraction_gaps', []).append({
        'kind': kind,
        'input_path': '$input' if rel is None else '$output/' + rel,
        'relative_path': rel,
        'handler': handler,
        'provider_id': None,
        'range': None,
        'root_file_range': None,
        'dependencies': list(deps or []),
        'continuation_id': 'probe-' + kind,
    })


def set_gap_deps(env, deps):
    for gap in nr(env).get('extraction_gaps') or []:
        if gap.get('kind') == DEP:
            gap['dependencies'] = list(deps)
    for diag in nr(env).get('diagnostics') or []:
        if isinstance(diag.get('missing_dependencies'), list):
            diag['missing_dependencies'] = list(deps)
        rep = diag.get('report')
        if isinstance(rep, dict) and isinstance(rep.get('dependencies'), list):
            rep['dependencies'] = list(deps)


def add_symlink_removed(env):
    nr(env).setdefault('diagnostics', []).append({
        'input_path': '$output/firmware.bin_extract/esc',
        'stage': 'squashfs',
        'report': {'severity': 'WARNING', '__typename__': 'MaliciousSymlinkRemoved',
                   'symlink_path': 'firmware.bin_extract/esc'},
    })


def set_op(env, op=None, pv=None):
    d = dref(env)
    if op is not None:
        d['operation'] = op
    if pv is not None:
        d['provider'] = {'id': pv}


def build_probes():
    P = []

    def mk(pid, klass, base, fn, why):
        env = load(base)
        fn(env)
        P.append({'id': pid, 'class': klass, 'base': base, 'why': why, 'env': env,
                  'features': tri.features(tri.envelope_data(env, pid))})

    # 5 planned combined classes, 2 replicates each
    mk('C01', 'partial+in-tree', 'H21',
       lambda e: add_gap(e, 'unpublished-entry', rel='x/i'), 'precedence 4 over 10')
    mk('C02', 'partial+in-tree', 'H22',
       lambda e: add_gap(e, 'unpublished-entry', rel='y/j'), 'replicate')
    mk('C03', 'partial+mixed', 'H21',
       lambda e: (add_gap(e, 'unpublished-entry', rel='x/i'), add_symlink_removed(e)),
       'precedence 4 over 8')
    mk('C04', 'partial+mixed', 'H22',
       lambda e: (add_gap(e, 'unpublished-entry', rel='y/j'), add_symlink_removed(e)),
       'replicate')
    mk('C05', 'depth-limited-alone', 'H01', lambda e: add_gap(e, 'depth-limited'), 'row 7')
    mk('C06', 'depth-limited-alone', 'H03', lambda e: add_gap(e, 'depth-limited'),
       'replicate on the le handler')
    mk('C07', 'depth-limited+in-tree', 'H09', lambda e: add_gap(e, 'depth-limited'),
       'row 7 over 10')
    mk('C08', 'depth-limited+in-tree', 'H10', lambda e: add_gap(e, 'depth-limited'),
       'replicate')
    mk('C09', 'depth-limited+mixed', 'H11', lambda e: add_gap(e, 'depth-limited'),
       'row 7 over 8')
    mk('C10', 'depth-limited+mixed', 'H12', lambda e: add_gap(e, 'depth-limited'),
       'replicate')

    # exposure probes (NOT planned classes): each one is a tuple where a
    # scoring shortcut table and the precedence text disagree
    mk('X01', 'damaged-le-body', 'H19',
       lambda e: (set_chunks(e, ['squashfs_v4_le']), strip_be(e)),
       'le handler, 0 files, no -be -> row 6, never row 5')
    mk('X02', 'damaged-le-body', 'H20',
       lambda e: (set_chunks(e, ['squashfs_v4_le']), strip_be(e)), 'replicate')
    mk('X03', 'non-squashfs-unpublished-entry', 'H09', lambda e: set_chunks(e, []),
       'no squashfs chunk + ue -> row 2')
    mk('X04', 'non-squashfs-extractor-failure', 'H19',
       lambda e: (set_chunks(e, []), strip_be(e)), 'no squashfs chunk + ef -> row 2')
    mk('X05', 'non-squashfs-depth-limited', 'H01',
       lambda e: (set_chunks(e, []), add_gap(e, 'depth-limited')), 'no chunk + dl -> row 2')
    mk('X06', 'no-chunk-with-files', 'H01', lambda e: set_chunks(e, []),
       'no chunk, files published -> row 2')
    mk('X07', 'dep-name-mismatch', 'H13', lambda e: set_gap_deps(e, ['sasquatch']),
       'be handler, D names sasquatch -> row 3 dep-missing-le')
    mk('X08', 'failure+depth-limited', 'H19', lambda e: add_gap(e, 'depth-limited'),
       'ef & dl, 0 files -> row 6')
    mk('X09', 'dep+failure', 'H21',
       lambda e: add_gap(e, DEP, handler='squashfs_v4_be', deps=['sasquatch-v4be']),
       'dep & ef & files -> row 3')
    mk('X10', 'op-guard-only', 'H23', lambda e: set_op(e, op='inspect_firmware_regions'),
       'verb outside, provider unblob -> row 1')
    mk('X11', 'provider-guard-only', 'H23', lambda e: set_op(e, pv='binwalk'),
       'provider outside, verb extract_firmware -> row 1')
    mk('X12', 'failure+symlinks+depth', 'H21',
       lambda e: (add_gap(e, 'unpublished-entry', rel='z/k'), add_symlink_removed(e),
                  add_gap(e, 'depth-limited')), 'ef & ue & dl & SR, files -> row 4')
    mk('X13', 'encrypted-chunk-with-files', 'H01',
       lambda e: add_gap(e, 'encrypted-chunk'),
       'gap kind precedence never names, files published -> row 12 unclassified')
    mk('X14', 'unknown-chunk-handler-with-files', 'H03',
       lambda e: add_gap(e, 'unknown-chunk-handler'),
       'gap kind precedence never names -> row 12 unclassified')
    return P


def precedence(f):
    OP, PV, H, G, D, BE, SR, P = (f['OP'], f['PV'], set(f['H']), set(f['G']),
                                  set(f['D']), f['BE'], f['SR'], f['P'])
    if OP != 'extract_firmware' or PV != 'unblob':
        return ('unclassified', 'none')
    if not [h for h in H if h.startswith('squashfs_v4_')]:
        return ('no-squashfs-chunk', 'inspect-input')
    if DEP in G:
        if 'sasquatch-v4be' in D:
            return ('dep-missing-be', 'install-extractor-be')
        if 'sasquatch' in D:
            return ('dep-missing-le', 'install-extractor-le')
    if 'extractor-failure' in G and P > 0:
        return ('partial-body-failure', 'salvage-partial')
    if 'extractor-failure' in G and P == 0 and BE == 'no' and 'squashfs_v4_be' in H:
        return ('avm-marker-be-dropped', 'wrap-extractor-be')
    if 'extractor-failure' in G and P == 0:
        return ('body-extractor-failure', 'preserve-failure')
    if 'depth-limited' in G:
        return ('depth-limited-nested', UNSPEC)
    if SR == 'yes' and 'unpublished-entry' in G:
        return ('mixed-symlinks', 'audit-symlinks')
    if SR == 'yes' and not G:
        return ('escaping-symlink-removed', 'expect-link-absent')
    if G == {'unpublished-entry'}:
        return ('in-tree-symlink-metadata', 'count-gap')
    if not G and P > 0:
        return ('clean', 'none')
    if not G and P == 0:
        return ('clean-empty', 'confirm-empty')
    return ('unclassified', 'none')


# ---------------------------------------------------------------- table grammar
HEADER = ('| label | operation | provider | handler | gap kinds | dependencies | '
          '-be in child argv | symlink removed | published files | action | cause | source |')
SEP = '| ' + ' | '.join(['---'] * 12) + ' |'


def skill_doc(rows, actions, marker='v2'):
    return '\n'.join(['## Queue-drain craft', '',
                      '<!-- sqfs-triage-table %s -->' % marker,
                      '<!-- sqfs-triage-actions: ' + ' '.join(actions) + ' -->',
                      HEADER, SEP] + ['| ' + ' | '.join(r) + ' |' for r in rows]) + '\n'


def row(label, action, op='extract_firmware', pv='unblob', handler='squashfs_v4_*',
        gaps='*', deps='*', be='*', sr='*', files='*'):
    return [label, '`%s`' % op, '`%s`' % pv, '`%s`' % handler, '`%s`' % gaps,
            '`%s`' % deps, '`%s`' % be, '`%s`' % sr, '`%s`' % files,
            '`%s`' % action, 'probe row -> %s' % action, 'plans/round-41-claims.md rows 1-12']


ACTIONS = ['none', 'inspect-input', 'install-extractor-be', 'install-extractor-le',
           'wrap-extractor-be', 'preserve-failure', 'salvage-partial', 'audit-symlinks',
           'expect-link-absent', 'count-gap', 'confirm-empty', 'descend-depth']


def T_min():
    """13 rows, exact-set grammar: the smallest table scoring every planned pair.

    The partial row is a trailing `*`-gap wildcard, so the precedence order
    (partial BEFORE avm/body/depth/mixed/...) is inverted and the row no longer
    tests the presence of extractor-failure.
    """
    return [
        row('no-squashfs-chunk', 'inspect-input', handler='none', gaps='*'),
        row('dep-missing-be', 'install-extractor-be', handler='squashfs_v4_be',
            gaps=DEP, deps='sasquatch-v4be'),
        row('dep-missing-le', 'install-extractor-le', handler='squashfs_v4_le',
            gaps=DEP, deps='sasquatch'),
        row('avm-marker-be-dropped', 'wrap-extractor-be', handler='squashfs_v4_be',
            gaps='extractor-failure', be='no', files='0'),
        row('body-extractor-failure', 'preserve-failure', gaps='extractor-failure', files='0'),
        row('depth-limited-nested', 'descend-depth', gaps='depth-limited'),
        row('depth-limited-nested-combined', 'descend-depth',
            gaps='depth-limited+unpublished-entry'),
        row('mixed-symlinks', 'audit-symlinks', gaps='unpublished-entry', sr='yes'),
        row('escaping-symlink-removed', 'expect-link-absent', gaps='none', sr='yes'),
        row('in-tree-symlink-metadata', 'count-gap', gaps='unpublished-entry', sr='no'),
        row('clean', 'none', gaps='none', sr='no', files='>0'),
        row('clean-empty', 'confirm-empty', gaps='none', sr='no', files='0'),
        row('partial-body-failure', 'salvage-partial', gaps='*', files='>0'),
    ]


def T_exact_faithful():
    """Precedence ORDER kept; combos need their own labels -> duplicate-label ban
    forces a distinct label per combo, so 2 of the 18 pairs cannot be reproduced."""
    return [
        row('no-squashfs-chunk', 'inspect-input', handler='none', gaps='none'),
        row('dep-missing-be', 'install-extractor-be', handler='squashfs_v4_be',
            gaps=DEP, deps='sasquatch-v4be'),
        row('dep-missing-le', 'install-extractor-le', handler='squashfs_v4_le',
            gaps=DEP, deps='sasquatch'),
        row('partial-body-failure', 'salvage-partial', gaps='extractor-failure', files='>0'),
        row('partial-body-failure-combined', 'salvage-partial',
            gaps='extractor-failure+unpublished-entry', files='>0'),
        row('avm-marker-be-dropped', 'wrap-extractor-be', handler='squashfs_v4_be',
            gaps='extractor-failure', be='no', files='0'),
        row('body-extractor-failure', 'preserve-failure', gaps='extractor-failure', files='0'),
        row('depth-limited-nested', 'descend-depth', gaps='depth-limited'),
        row('depth-limited-nested-combined', 'descend-depth',
            gaps='depth-limited+unpublished-entry'),
        row('mixed-symlinks', 'audit-symlinks', gaps='unpublished-entry', sr='yes'),
        row('escaping-symlink-removed', 'expect-link-absent', gaps='none', sr='yes'),
        row('in-tree-symlink-metadata', 'count-gap', gaps='unpublished-entry', sr='no'),
        row('clean', 'none', gaps='none', sr='no', files='>0'),
        row('clean-empty', 'confirm-empty', gaps='none', sr='no', files='0'),
    ]


def variant(fn, **kw):
    def build():
        rows = T_min()
        fn(rows, **kw)
        return rows
    return build


def v_dep_star(rows):
    for r in rows:
        r[5] = '`*`'


def v_op_star(rows):
    for r in rows:
        r[1] = '`*`'


def v_pv_star(rows):
    for r in rows:
        r[2] = '`*`'


def v_handler_star_gap_rows(rows):
    for r in rows[1:]:
        if r[3] not in ('`none`',):
            r[3] = '`*`'


def v_no_be(rows):
    for r in rows:
        r[6] = '`*`'


def v_no_sr(rows):
    for r in rows:
        r[7] = '`*`'


def v_no_domain(rows):
    rows[0][1] = '`*`'
    rows[0][2] = '`*`'


def v_nochunk_p0(rows):
    rows[0][8] = '`0`'
    rows[10][3] = '`*`'   # clean row takes any handler
    rows[11][3] = '`*`'


def v_dl_first(rows):
    dl = [r for r in rows if r[0].startswith('depth-limited')]
    rest = [r for r in rows if not r[0].startswith('depth-limited')]
    rows[:] = dl + rest


def v_dl_first_handler_star(rows):
    v_dl_first(rows)
    for r in rows[:2]:
        r[3] = '`*`'


def v_star_default(rows):
    rows.append(row('unclassified', 'none', op='*', pv='*', handler='*', gaps='*',
                    deps='*', be='*', sr='*', files='*'))


def v_drop(rows, which=()):
    rows[:] = [r for r in rows if r[0] not in which]


def v_partial_exact(rows):
    """the two exact partial rows instead of the trailing wildcard (14 rows)"""
    rows[12] = row('partial-body-failure', 'salvage-partial',
                   gaps='extractor-failure', files='>0')
    rows.insert(12, row('partial-body-failure-combined', 'salvage-partial',
                        gaps='extractor-failure+unpublished-entry', files='>0'))


def v_dl_single_wildcard(rows):
    """try to drop one depth row by widening it: must fail on a planned pair"""
    rows[:] = [r for r in rows if r[0] != 'depth-limited-nested-combined']
    for r in rows:
        if r[0] == 'depth-limited-nested':
            r[4] = '`*`'
            rows.remove(r)
            rows.append(r)


CANDIDATES = [
    ('T_min', T_min, 'smallest table scoring every planned pair (13 rows, wildcard partial)'),
    ('T_exact_faithful', T_exact_faithful,
     'precedence order kept, exact cells, distinct combo labels (14 rows)'),
    ('S_dep_star', variant(v_dep_star), 'dependencies column dropped'),
    ('S_op_star', variant(v_op_star), 'operation column dropped'),
    ('S_pv_star', variant(v_pv_star), 'provider column dropped'),
    ('S_handler_star', variant(v_handler_star_gap_rows),
     'handler cell dropped from every row but no-chunk'),
    ('S_no_be', variant(v_no_be), '-be column dropped'),
    ('S_no_sr', variant(v_no_sr), 'symlink-removed column dropped'),
    ('S_no_domain', variant(v_no_domain), 'no operation/provider guard'),
    ('S_nochunk_p0', variant(v_nochunk_p0), 'no-chunk pinned to 0 files, clean rows any handler'),
    ('S_dl_first', variant(v_dl_first), 'depth-limited rows first'),
    ('S_dl_first_star', variant(v_dl_first_handler_star),
     'depth-limited rows first AND handler dropped on them'),
    ('S_star_default', variant(v_star_default), 'all-* default row appended'),
    ('S_drop_mixed', variant(v_drop, which=('mixed-symlinks',)), 'mixed row removed'),
    ('S_drop_dl', variant(v_drop, which=('depth-limited-nested',
                                         'depth-limited-nested-combined')),
     'both depth rows removed'),
    ('S_drop_dl_combined', variant(v_drop, which=('depth-limited-nested-combined',)),
     'combined depth row removed'),
    ('S_drop_partial', variant(v_drop, which=('partial-body-failure',)), 'partial row removed'),
    ('S_drop_nochunk', variant(v_drop, which=('no-squashfs-chunk',)), 'no-chunk row removed'),
    ('S_partial_exact', variant(v_partial_exact), 'two exact partial rows instead of wildcard'),
    ('S_dl_wildcard_last', variant(v_dl_single_wildcard),
     'one wildcard depth row at the end instead of two'),
    ('T_v2_committed', None, 'the committed round-40 v2 table (baseline, R40-CL5)'),
]


def score_exact(rows, envelopes):
    text = skill_doc(rows, ACTIONS)
    rules, info = tri.parse_skill(text)
    out = []
    for item in envelopes:
        rule = tri.classify(rules, item['features'])
        got = tri.decision(rule)
        want = precedence(item['features'])
        label_ok = got[0] == want[0]
        pair_ok = label_ok and (want[1] == UNSPEC or got[1] == want[1])
        out.append({'id': item['id'], 'class': item['class'], 'got': got, 'want': want,
                    'label_ok': label_ok, 'action_specified': want[1] != UNSPEC,
                    'pair_ok': pair_ok,
                    'features': {k: item['features'][k] for k in
                                 ('OP', 'PV', 'H', 'G', 'D', 'BE', 'SR', 'P')}})
    return out, info


def summarise(res, wanted_classes):
    by_class = {}
    for r in res:
        if r['class'] not in wanted_classes:
            continue
        by_class.setdefault(r['class'], []).append(r)
    passed = [c for c, rs in by_class.items() if all(x['pair_ok'] for x in rs)]
    missed = sorted(c for c in by_class if c not in passed)
    return len(passed), len(by_class), missed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ns = ap.parse_args()
    for sub in ('tables', 'probes'):
        os.makedirs(os.path.join(ns.out, sub), exist_ok=True)

    planned = []
    run_meta = {}
    for d in sorted(glob.glob(os.path.join(HELDOUT, 'H*'))):
        hid = os.path.basename(d)
        with open(os.path.join(d, 'run.json')) as fh:
            run = json.load(fh)
        env = load(hid)
        planned.append({'id': hid, 'class': run['class'],
                        'features': tri.features(tri.envelope_data(env, hid))})
        run_meta[hid] = {'class': run['class'], 'operation': run['operation'],
                         'provider': run['provider'], 'handlers': run['handlers'],
                         'gap_kinds': run['gap_kinds'], 'files': run['files'],
                         'exit_code': run['exit_code']}
    probes = build_probes()
    combined_probes = [p for p in probes if p['id'].startswith('C')]
    exposure = [p for p in probes if p['id'].startswith('X')]
    planned_classes = sorted({p['class'] for p in planned} | {p['class'] for p in combined_probes})

    # committed v2 table, parsed from the real SKILL.md by the real interpreter
    with open(SKILL, 'r', encoding='utf-8') as fh:
        v2_rules, v2_info = tri.parse_skill(fh.read())

    report = {'planned_classes': planned_classes, 'candidates': [],
              'v2_baseline': {'rules': v2_info['rules'], 'actions': v2_info['actions']},
              'planned_tuples': {}, 'exposure_probes': {}}
    for c in planned + combined_probes:
        f = c['features']
        report['planned_tuples'][c['id']] = {
            'class': c['class'],
            'features': {k: f[k] for k in ('OP', 'PV', 'H', 'G', 'D', 'BE', 'SR', 'P')},
            'precedence': precedence(f)}
    for c in exposure:
        f = c['features']
        report['exposure_probes'][c['id']] = {
            'class': c['class'], 'why': c['why'],
            'features': {k: f[k] for k in ('OP', 'PV', 'H', 'G', 'D', 'BE', 'SR', 'P')},
            'precedence': precedence(f)}
    report['committed_runs'] = run_meta

    all_env = planned + combined_probes
    for name, fn, why in CANDIDATES:
        if fn is None:
            res = []
            for item in all_env + exposure:
                rule = tri.classify(v2_rules, item['features'])
                got = tri.decision(rule)
                want = precedence(item['features'])
                res.append({'id': item['id'], 'class': item['class'], 'got': got,
                            'want': want, 'label_ok': got[0] == want[0],
                            'pair_ok': got == want,
                            'features': {k: item['features'][k] for k in
                                         ('OP', 'PV', 'H', 'G', 'D', 'BE', 'SR', 'P')}})
            info = {'rules': v2_info['rules']}
            rows = None
        else:
            rows = fn()
            res, info = score_exact(rows, all_env + exposure)
        passed, total, missed = summarise(res, set(planned_classes))
        exp = {r['id']: {'want': r['want'], 'got': r['got'], 'ok': r['pair_ok']}
               for r in res if r['id'].startswith('X')}
        exp_div = sorted(k for k, v in exp.items() if not v['ok'])
        report['candidates'].append({
            'name': name, 'why': why, 'rows': info['rules'],
            'classes_passed': passed, 'classes_total': total, 'missed': missed,
            'exposure_divergences': exp_div, 'exposure': exp,
            'envelope_pairs_ok': sum(1 for r in res if r['pair_ok']),
            'envelopes': len(res),
            'detail': res if name in ('T_min', 'T_exact_faithful', 'T_v2_committed',
                                      'S_handler_star', 'S_dl_first_star', 'S_no_be',
                                      'S_no_sr', 'S_no_domain', 'S_dep_star')
            else None})
        if rows is not None:
            with open(os.path.join(ns.out, 'tables', name + '.md'), 'w') as fh:
                fh.write(skill_doc(rows, ACTIONS))

    for cand in report['candidates']:
        print('%-22s rows=%2d planned %2d/%2d  envelope %2d/%2d  missed=%s  Xdiv=%s'
              % (cand['name'], cand['rows'], cand['classes_passed'], cand['classes_total'],
                 cand['envelope_pairs_ok'], cand['envelopes'],
                 ','.join(cand['missed']) or '-', ','.join(cand['exposure_divergences']) or '-'))
    with open(os.path.join(ns.out, 'score.json'), 'w') as fh:
        json.dump(report, fh, indent=2, sort_keys=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
