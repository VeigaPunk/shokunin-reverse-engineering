#!/usr/bin/env python3
"""Independent cross-check of the registry couplings the peer seat asserted,
re-measured here with the frozen counters' own code.

Checks:
  1. R48 meanings.py registry_extra at HEAD (pre-existing failure?) and with the
     peer row added (does the new row make it worse?).
  2. R46 registry.py at HEAD and with the peer row: does it check that every
     registry row's cell-0 path exists at the measured rev (absent_at_rev)?
     The new row names a path that does not exist until the C3 freeze lands.
  3. R45 c2-counter.py scope check is unaffected.
Read-only on the lane: only git cat-file/ls-tree/rev-parse.
"""
import importlib.util
import json
import os
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
SEAT = os.path.join(LANE, '.ufo/waves/round-50/w3/ExecRegistryRow')
PATH = 'tools/round-50-c3/sqfs-triage-v5.py'
REV = 'f890bbead20ca2c549487167f56876ae47f1e1a4'


def load(name, rel):
    s = importlib.util.spec_from_file_location(name, os.path.join(LANE, rel))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


m48 = load('m48', 'tools/round-48/meanings.py')
row = open(os.path.join(SEAT, 'row-final.txt'), encoding='utf-8').read().rstrip('\n')

out = {}

# --- 1. R48 registry_extra, before and after the peer row ---------------------
skill_head = subprocess.run(['git', '-C', LANE, 'show', REV + ':SKILL.md'],
                             capture_output=True, text=True).stdout
close = '\n<!-- /instrument-registry -->'
skill_with = skill_head.replace(close, '\n' + row + close, 1)


def r48_registry(skill_text):
    """Re-derive the R48 registry clauses only (no git needed for this part)."""
    rows = m48.registry_rows(skill_text)
    paths = [r['path'] for r in rows]
    census_body = subprocess.run(
        ['git', '-C', LANE, 'show', REV + ':tools/round-48/census2.json'],
        capture_output=True, text=True).stdout
    doc = json.loads(census_body)
    dup = sorted({p for p in paths if paths.count(p) > 1})
    missing = sorted(set(doc['paths']) - set(paths))
    extra = sorted(set(paths) - set(doc['paths']))
    bad_meaning = [{'path': r['path'], 'error': m48.meaning_classes(r['verdict']).get('error')}
                   for r in rows if 'error' in m48.meaning_classes(r['verdict'])]
    return {'registry_rows': len(paths), 'census_paths': len(doc['paths']),
            'duplicates': dup, 'missing': missing, 'extra_count': len(extra),
            'extra': extra, 'meaning_rows_failed': len(bad_meaning),
            'meaning_failures': bad_meaning[:5]}


out['R48_at_head'] = r48_registry(skill_head)
out['R48_with_peer_row'] = r48_registry(skill_with)
out['R48_peer_row_in_extra'] = PATH in out['R48_with_peer_row']['extra']

# --- 2. R46 registry.py: does it police absent_at_rev for EVERY row? ---------
r46 = load('r46', 'tools/round-46/registry.py')
import re
src = open(os.path.join(LANE, 'tools/round-46/registry.py'), encoding='utf-8').read()
i = src.find('absent_at_rev')
out['R46_absent_at_rev_context'] = src[max(0, i - 1400):i + 400]

# --- 3. R45 c2-counter scope --------------------------------------------------
r45 = load('r45', 'tools/round-45/c2-counter.py')
scope = json.loads(subprocess.run(
    ['git', '-C', LANE, 'show', REV + ':tools/round-45/registry-scope.json'],
    capture_output=True, text=True).stdout)['paths']
out['R45_scope'] = scope
out['R45_scope_contains_new_path'] = PATH in scope

print(json.dumps(out, indent=1, ensure_ascii=False))
