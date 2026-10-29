#!/usr/bin/env python3
"""Validate the simulated full landing (branch c3-full-landing, tip below) with the
frozen counters' own code:
  1. c2 freeze_check at the landing tip (must be clean)
  2. c2 full 11-atom score at the tip (all must be green)
  3. c2 single-mutation battery + do-nothing (failing must be [])
  4. the c1 documentation-binding predicates (c1-counter.py:2439-2492 replica, using the
     counter's own compiled regexes/helpers), all 9 bindings must be true
  5. b9 row-shape rules applied to the drafted registry row (template check)
"""
import importlib.util
import json
import re
import subprocess
import sys

CLONE = '/fast/scratch/hyaku/kaidoku-r50/w3-ConnCrossClaim/clone'
WORK = '/fast/scratch/hyaku/kaidoku-r50/w3-ConnCrossClaim/val-work'
FREEZE = '435d41fd4ad9211d1579fc447936fb33d2b74467'
TIP = subprocess.run(['git', '-C', CLONE, 'rev-parse', 'c3-full-landing'],
                     capture_output=True).stdout.decode().strip()
ENTRY = 'corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md'
STEM = '2026-10-28-r50-avm-le-squashfs-core'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


c1 = load('c1c', CLONE + '/tools/round-50/c1-counter.py')
c2 = load('c2r', CLONE + '/tools/round-50/c2-record.py')
g = c2.Git(CLONE)

print('landing tip:', TIP)
msg, why = c2.freeze_check(g, FREEZE, TIP)
print('1. freeze_check:', json.dumps({'problem': msg, 'code': why}))
assert msg is None

c = c2.Ctx(g, TIP, WORK, CLONE)
res = c2.score(c)
bad = {k: v for k, v in res.items() if v}
print('2. c2 score mismatches:', json.dumps(bad) if bad else '{} (all 11 atoms green)')
assert not bad

bat = c2.battery(g, TIP, FREEZE, WORK, CLONE)
print('3. battery: mutation_count=%d failing=%s green_mismatches=%s' % (
    bat['mutation_count'], json.dumps(bat['failing']),
    json.dumps({k: v for k, v in bat['green'].items() if v})))
assert not bat['failing']

# 4. c1 documentation bindings, replica of c1-counter.py measure() tail
prov = g.show(TIP, 'PROVINCE.md').decode(errors='replace')
sec = c1.section(prov, c1.CORE_HEADING)
b = {}
b['province_core_section'] = sec is not None
rows = [l for l in (sec or []) if l.lstrip().startswith('|')]
b['province_core_row'] = any(
    c1.HANDLER_RE.search(c1.cells(r)[0]) and c1.AVM_MARKER_RE.search(r.replace(ENTRY, ''))
    and ENTRY in r for r in rows)
b['frontier_note'] = any(c1.FRONTIER_MARK in l and STEM in l
                         and c1.LE_AVM_RE.search(l.replace(STEM, ''))
                         for l in prov.splitlines())
ent = g.show(TIP, ENTRY)
b['entry_present'] = ent is not None
src_ids = set()
for line in ent.decode(errors='replace').splitlines():
    if line.startswith('source:'):
        src_ids |= c1.sid_tokens(line)
b['entry_source_ids'] = sorted(src_ids)
ok_ids = []
for line in g.show(TIP, 'corpus/SOURCES.md').decode(errors='replace').splitlines():
    if not re.match(r'^ {0,3}\|\s*S\d{3,}\s*\|', line):
        continue
    cs = c1.cells(line)
    if len(cs) != 11:
        continue
    used = cs[10]
    if cs[0] in src_ids and cs[8] in c1.OPENED_DATES and (ENTRY in used or STEM in used):
        ok_ids.append(cs[0])
b['opened_source_rows'] = sorted(ok_ids)
b['sourced'] = bool(ok_ids)
readme = g.show(TIP, 'corpus/README.md').decode(errors='replace')
cm = c1.section(readme, '## Coverage map')
b['coverage_map_row'] = bool(cm) and any(STEM in l for l in cm if l.lstrip().startswith('|'))
print('4. c1 documentation bindings:', json.dumps(b, sort_keys=True))
assert all(b[x] for x in ('province_core_section', 'province_core_row', 'frontier_note',
                          'entry_present', 'sourced', 'coverage_map_row'))

# 5. b9 row-shape rules against the drafted registry row
sk = g.show(TIP, 'SKILL.md').decode(errors='replace')
region_rows, regbad = c2.registry_region(sk)
row = region_rows['tools/round-50c3/sqfs-triage-v5.py'][0]
checks = {
    'cells==7': len(row) == 7,
    'kind gate|probe': bool(re.match(r'(?i)(gate|probe)\b', row[1])),
    'verdict map': c2.meaning_classes(row[2]) is None,
    'selftest cell': bool(re.match(r'(?:python3?|bash|sh)\s+(?:-\S+\s+)*(?:\./)?'
                                   + re.escape('tools/round-50c3/sqfs-triage-v5.py')
                                   + r'\b.*--selftest', row[3])),
    'pinned cell': bool(re.search(r'[\w.\-]+/[\w./\-]*', row[4])),
}
print('5. drafted registry row checks:', json.dumps(checks))
assert all(checks.values())

print('VALIDATION-EXIT=0')
