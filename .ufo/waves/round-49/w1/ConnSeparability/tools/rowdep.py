import importlib.util, json, re, sys, os
S = '/fast/scratch/hyaku/kaidoku-r49/ConnSeparability'
Z = S + '/Z'
ZREV = __import__('subprocess').run(['git', '-C', Z, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
FREEZE = '352e24c6728df9da4b7aa2e410cfbc4ab4a70622'
PKG = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
c1 = load('c1c', Z + '/tools/round-49/c1-counter.py')
c2 = load('c2c', Z + '/tools/round-49/c2-mismatch.py')
c1.WORK_OVERRIDE = S + '/work/inproc-c1'
orig_show = c1.show
REG = 'corpus/SOURCES.md'
g = c2.Git(Z)
reg = g.show(ZREV, REG).decode()
lines = reg.split('\n')
rows = [(i, c2.ROW_RE.match(l).group(1)) for i, l in enumerate(lines) if c2.ROW_RE.match(l)]
def boom(raw, cid, params=None):
    return 'no_data', {'ok': False, 'exit': 1, 'stderr': 'rowdep: rerun disabled (bindings only)'}
def c1_eval(new):
    c1.show = lambda root, rev, path: (new.encode() if (rev == ZREV and path == REG) else orig_show(root, rev, path))
    try:
        res = c1.measure(Z, ZREV, FREEZE, PKG, rerun=boom)
    finally:
        c1.show = orig_show
    b = res['bindings']
    return {'sourced': b['sourced'], 'opened_source_rows': b['opened_source_rows'],
            'false_bindings': sorted(k for k, v in b.items() if v is False),
            'carriers_matched_rerun_disabled': res.get('carriers_matched')}
def c2_eval(new):
    sc = c2.score(c2.Overlay(g, ZREV, {REG: new.encode()}), ZREV)
    return sorted(k for k, v in sc.items() if v)
def perturb(i, kind):
    l = lines[i]
    if kind == 'trailing_space':
        nl = l + ' '
    elif kind == 'date_cell':  # cell index 8 is the `opened` column of the 11-column table
        parts = l.split('|')
        parts[9] = ' 2026-10-27 '
        nl = '|'.join(parts)
    out = list(lines); out[i] = nl
    return '\n'.join(out)
base = {'c1': c1_eval(reg), 'c2': c2_eval(reg)}
print('BASE', json.dumps(base))
res = {'rev': ZREV, 'base': base, 'rows': {}}
for i, rid in rows:
    row = {}
    for kind in ('trailing_space', 'date_cell'):
        new = perturb(i, kind)
        row[kind] = {'c1': c1_eval(new), 'c2_red': c2_eval(new)}
    res['rows'][rid] = row
json.dump(res, open(S + '/out/rowdep.json', 'w'), indent=1, sort_keys=True)
print('rows swept', len(rows))
changed_c1 = {r: v['date_cell']['c1']['false_bindings'] for r, v in res['rows'].items() if v['date_cell']['c1']['false_bindings'] != base['c1']['false_bindings'] or v['date_cell']['c1']['sourced'] != base['c1']['sourced']}
changed_c1_trail = {r: v['trailing_space']['c1']['false_bindings'] for r, v in res['rows'].items() if v['trailing_space']['c1']['false_bindings'] != base['c1']['false_bindings']}
changed_c2 = {r: (v['trailing_space']['c2_red'], v['date_cell']['c2_red']) for r, v in res['rows'].items() if v['trailing_space']['c2_red'] or v['date_cell']['c2_red']}
print('C1 sensitive rows (date_cell):', sorted(changed_c1))
print('C1 sensitive rows (trailing_space):', sorted(changed_c1_trail))
print('C2 sensitive rows (red atoms: trailing_space, date_cell):', json.dumps(changed_c2, sort_keys=True))
