#!/usr/bin/env python3
"""Verify the LANDED SKILL.md row for the C3 instrument against every frozen predicate.

The L1 has landed a row in SKILL.md (uncommitted, `git diff` shows it at line 1774).
This checks the LANDED bytes (not the peer's draft) against:
  - each b9() predicate (re-applied by hand, because the path is outside B9's census),
  - the round-48 meaning rule,
  - exactly-one-row / no-duplicate-cell-0 in the region,
  - the entry command against the landed instrument's real CLI.
Read-only on the lane.
"""
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
PATH = 'tools/round-50-c3/sqfs-triage-v5.py'


def load(name, rel):
    s = importlib.util.spec_from_file_location(name, os.path.join(LANE, rel))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


c2 = load('c2record', 'tools/round-50/c2-record.py')
m48 = load('m48', 'tools/round-48/meanings.py')

skill = open(os.path.join(LANE, 'SKILL.md'), encoding='utf-8').read()
rows, bad = c2.registry_region(skill)
cs = (rows.get(PATH) or [None])[0]

res = {'landed_row_present': cs is not None}
if cs is None:
    print(json.dumps(res, indent=1))
    sys.exit(1)

res['landed_row_sha256'] = hashlib.sha256(
    ('| ' + ' | '.join(cs) + ' |\n').encode('utf-8')).hexdigest()
res['n_cells'] = len(cs)
res['cells'] = cs

checks = {}
checks['seven_cells'] = (len(cs) == 7, '%d cells' % len(cs))
checks['kind_cell_opens_gate_or_probe'] = (
    bool(re.match(r'(?i)(gate|probe)\b', cs[1])), cs[1][:40])
entry = r'(?:python3?|bash|sh|node)\s+(?:-\S+\s+)*(?:\./)?' + re.escape(PATH) + r'(?![\w./\-])'
hits = [i for i, x in enumerate(cs[1:5], 1) if re.search(entry, x)]
checks['entry_command_names_path'] = (bool(hits), 'cells %s' % hits)
checks['verdict_meaning_c2_port'] = (c2.meaning_classes(cs[2]) is None, c2.meaning_classes(cs[2]) or '')
mc48 = m48.meaning_classes(cs[2])
checks['verdict_meaning_round48'] = ('error' not in mc48, mc48)
st = bool(re.match(r'(?:python3?|bash|sh)\s+(?:-\S+\s+)*(?:\./)?' + re.escape(PATH) +
                    r'\b.*--selftest', cs[3]))
st_alt = bool(re.match(r'none\s*[\u2014\-:;,]\s*\S+(?:\s+\S+){2,}', cs[3]))
checks['selftest_cell'] = (st or st_alt, '--selftest form' if st else ('none form' if st_alt else 'BAD'))
pin = bool(re.match(r'none\s*[\u2014\-:;,]\s*\S+(?:\s+\S+){1,}', cs[4]) or
           re.search(r'[\w.\-]+/[\w./\-]*|\b[\w\-]+\.(?:json|tsv|md|py|sh|txt|html)\b', cs[4]))
checks['pinned_value_cell'] = (pin, cs[4][:80])
checks['cell0_exact_path'] = (cs[0].strip('` ') == PATH, cs[0])
checks['exactly_one_row_for_path'] = (len(rows.get(PATH, [])) == 1,
                                      '%d rows' % len(rows.get(PATH, [])))
dups = sorted({p for p in rows if len(rows[p]) > 1})
checks['no_duplicate_cell0'] = (not dups, dups)
checks['markers_singular'] = (bad is None, bad or '')
# the pinned-value paths must exist and be tracked at HEAD (a trailing-slash path is a
# directory: it is tracked when git ls-files lists files under it)
paths = re.findall(r'\.ufo/[\w./-]+', cs[4])
tracked = set(subprocess.run(['git', '-C', LANE, 'ls-files'],
                             capture_output=True, text=True).stdout.split('\n'))
missing = []
for p in paths:
    p = p.rstrip('/')
    if p in tracked:
        continue
    if any(t.startswith(p + '/') for t in tracked):
        continue
    missing.append(p)
checks['pinned_paths_tracked'] = (not missing, 'missing %s' % missing if missing else paths)
# the entry command must match the landed instrument's real CLI
ip = os.path.join(LANE, PATH)
cli = {}
if os.path.exists(ip):
    src = open(ip, encoding='utf-8', errors='replace').read()
    cli['flags'] = sorted(set(re.findall(r"'--([a-z0-9-]+)'", src)))
    cli['has_selftest'] = 'selftest' in cli['flags']
    cli['sha256'] = hashlib.sha256(open(ip, 'rb').read()).hexdigest()
    cli['bytes'] = os.path.getsize(ip)
    need = ['root', 'rev', 'freeze', 'envelopes', 'json-out', 'selftest']
    checks['entry_command_matches_real_cli'] = (
        all(f in cli['flags'] for f in need), 'missing flags %s' %
        [f for f in need if f not in cli['flags']])
else:
    checks['entry_command_matches_real_cli'] = (False, 'instrument not at %s' % PATH)

res['checks'] = {k: {'ok': bool(v[0]), 'detail': v[1]} for k, v in checks.items()}
res['all_ok'] = all(v[0] for v in checks.values())
res['landed_instrument'] = cli
res['region_rows'] = len(rows)

out = json.dumps(res, indent=1, ensure_ascii=False)
print(out)
sys.stderr.write('sha256(results)=%s\n' % hashlib.sha256(out.encode('utf-8')).hexdigest())
