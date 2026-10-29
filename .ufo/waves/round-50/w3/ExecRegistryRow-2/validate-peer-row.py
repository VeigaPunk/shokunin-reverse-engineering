#!/usr/bin/env python3
"""Independent check of the PEER seat's row (row-final.txt) against the frozen
counter's own b9() predicates, applied by hand.

Why by hand: the L1 moved the C3 instrument to tools/round-50-c3/, which is OUTSIDE
B9's census prefix (tools/round-50).  So b9() never inspects that row at all --
the row is a gate-registration duty, not a B9 requirement, and B9 cannot police
it.  This script re-applies each b9() predicate to the row text directly, using
the frozen counter's own regexes and its own meaning_classes().

Read-only on the lane.
"""
import hashlib
import importlib.util
import json
import os
import re
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
SEAT = os.path.join(LANE, '.ufo/waves/round-50/w3/ExecRegistryRow')
PATH = 'tools/round-50-c3/sqfs-triage-v5.py'

spec = importlib.util.spec_from_file_location(
    'c2record', os.path.join(LANE, 'tools/round-50/c2-record.py'))
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)

m48_spec = importlib.util.spec_from_file_location(
    'm48', os.path.join(LANE, 'tools/round-48/meanings.py'))
m48 = importlib.util.module_from_spec(m48_spec)
m48_spec.loader.exec_module(m48)

row = open(os.path.join(SEAT, 'row-final.txt'), encoding='utf-8').read().rstrip('\n')
cs = c2.cells(row)

res = {
    'row_sha256': hashlib.sha256(row.encode('utf-8')).hexdigest(),
    'row_n_cells': len(cs),
    'cells': cs,
}

# --- each b9() predicate, verbatim from tools/round-50/c2-record.py -------------
checks = {}
checks['P1_seven_cells'] = (len(cs) == 7,
                            '%d cells, want 7' % len(cs))
checks['P2_kind_cell_opens_gate_or_probe'] = (
    bool(re.match(r'(?i)(gate|probe)\b', cs[1])),
    'kind cell does not open gate|probe' if not re.match(r'(?i)(gate|probe)\b', cs[1])
    else '')
entry = r'(?:python3?|bash|sh|node)\s+(?:-\S+\s+)*(?:\./)?' + re.escape(PATH) + r'(?![\w./\-])'
hits = [i for i, x in enumerate(cs[1:5], start=1) if re.search(entry, x)]
checks['P3_entry_command_names_path'] = (bool(hits),
                                         'no entry command naming the path' if not hits
                                         else 'cells %s' % hits)
mc = c2.meaning_classes(cs[2])
checks['P4_verdict_map_meaning_c2_port'] = (mc is None, mc or '')
mc48 = m48.meaning_classes(cs[2])
checks['P4b_verdict_map_meaning_round48'] = ('error' not in mc48, mc48.get('error', ''))
st_ok = bool(re.match(r'(?:python3?|bash|sh)\s+(?:-\S+\s+)*(?:\./)?' + re.escape(PATH) +
                      r'\b.*--selftest', cs[3]))
st_alt = bool(re.match(r'none\s*[\u2014\-:;,]\s*\S+(?:\s+\S+){2,}', cs[3]))
checks['P5_selftest_cell'] = (st_ok or st_alt,
                              'self-test cell is neither `<interpreter> <path> ... --selftest` '
                              'nor `none \u2014 <reason>`' if not (st_ok or st_alt)
                              else ('--selftest form' if st_ok else 'none form'))
pin_ok = bool(re.match(r'none\s*[\u2014\-:;,]\s*\S+(?:\s+\S+){1,}', cs[4]) or
              re.search(r'[\w.\-]+/[\w./\-]*|\b[\w\-]+\.(?:json|tsv|md|py|sh|txt|html)\b', cs[4]))
checks['P6_pinned_value_cell'] = (pin_ok,
                                  'pinned-value cell names no path and is not `none \u2014 <reason>`'
                                  if not pin_ok else '')
checks['P7_row_visible_to_registry_region'] = (
    bool(re.match(r'^ {0,3}\|\s*`', row)),
    'row line does not match the registry_region row regex')
# the row must be seen by registry_region when placed in the region
t = open(os.path.join(LANE, 'SKILL.md'), encoding='utf-8').read()
close = '\n<!-- /instrument-registry -->'
land = t.replace(close, '\n' + row + close, 1)
rows, bad = c2.registry_region(land)
checks['P8_exactly_one_row_for_path'] = (
    len(rows.get(PATH, [])) == 1,
    '%d rows for %s, want 1' % (len(rows.get(PATH, [])), PATH))
checks['P9_no_duplicate_cell0_in_region'] = (
    not [p for p in rows if len(rows[p]) > 1],
    'duplicate cell-0: %s' % [p for p in rows if len(rows[p]) > 1])
checks['P10_marker_singular'] = (bad is None, bad or '')
checks['P11_cell0_exact_path'] = (cs[0].strip('` ') == PATH,
                                  'cell0 %r != %r' % (cs[0], PATH))
# no bare pipe inside a cell (cells() would mis-split); the row's own pipe count
checks['P12_pipe_count_consistent'] = (row.count('|') == 8,
                                        'row has %d pipes, want 8 (7 cells)' % row.count('|'))

res['checks'] = {k: {'ok': bool(v[0]), 'detail': v[1]} for k, v in checks.items()}
res['all_ok'] = all(v[0] for v in checks.values())

# --- does B9 actually police this row? ---------------------------------------
g = c2.Git(LANE)
ov = c2.Overlay(g, 'f890bbead20ca2c549487167f56876ae47f1e1a4',
                {PATH: b'#!/usr/bin/env python3\n'})
ctx = c2.Ctx(ov, 'f890bbead20ca2c549487167f56876ae47f1e1a4',
             os.environ.get('TMPDIR', '/fast/scratch'), LANE)
res['b9_census_contains_path'] = PATH in c2.census_paths(ctx)
res['b9_problems_with_peer_row'] = c2.b9(ctx)
# a deliberately broken row for the same path: does B9 notice?
bad_row = ("| `" + PATH + "` | helper | 0=zero | 1=one | 2=two | none | none | none | kaidoku |")
t2 = t.replace(close, '\n' + bad_row + close, 1)
ov2 = c2.Overlay(g, 'f890bbead20ca2c549487167f56876ae47f1e1a4',
                 {PATH: b'#!/usr/bin/env python3\n', 'SKILL.md': t2.encode('utf-8')})
ctx2 = c2.Ctx(ov2, 'f890bbead20ca2c549487167f56876ae47f1e1a4',
              os.environ.get('TMPDIR', '/fast/scratch'), LANE)
res['b9_problems_with_deliberately_broken_row'] = c2.b9(ctx2)

out = json.dumps(res, indent=1, ensure_ascii=False)
print(out)
sys.stderr.write('sha256(results)=%s\n' % hashlib.sha256(out.encode('utf-8')).hexdigest())
