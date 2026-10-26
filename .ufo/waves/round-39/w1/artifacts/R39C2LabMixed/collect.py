#!/usr/bin/env python3
"""Collect the R39C2LabMixed dev evidence bundle from scratch into the seat
artifacts dir: carriers, envelopes, feature table, classification output.

Usage: collect.py <scratch-dir> <artifacts-dir> <lane-root>
Reads only scratch + lane evidence (read-only); writes only artifacts.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

S, A, LANE = sys.argv[1], sys.argv[2], sys.argv[3]
ENVDIR = os.path.join(A, 'envelopes')
CARDIR = os.path.join(A, 'carriers')
for d in (ENVDIR, CARDIR):
    os.makedirs(d, exist_ok=True)

CARRIERS = [
    ('D1-in-first', 'a'), ('D1-in-first', 'b'),
    ('D2-out-first', 'a'), ('D2-out-first', 'b'),
    ('D3-nested-multi', 'a'), ('D3-nested-multi', 'b'),
    ('D4-chase-first', 'a'), ('D4-chase-first', 'b'),
    ('D5-escape-first', 'a'), ('D5-escape-first', 'b'),
    ('D6-two-escaping', 'a'), ('D6-two-escaping', 'b'),
    ('C1-target-first', 'a'), ('C1-target-first', 'b'),
    ('C2-chase-first', 'a'), ('C2-chase-first', 'b'),
    ('C3-root-escape', 'a'), ('C3-root-escape', 'b'),
    ('C4-root-chase', 'a'), ('C4-root-chase', 'b'),
    ('D7-corrupt-body', 'a'), ('D7-corrupt-body', 'b'),
    ('D8-dir-links', 'a'), ('D8-dir-links', 'b'),
]
PLAIN = ('plain', 'a'), ('plain', 'b')

COPIED = []
for name, tag in CARRIERS:
    src = os.path.join(S, 'env-%s-%s.json' % (name, tag))
    dst = os.path.join(ENVDIR, 'env-%s-%s.json' % (name, tag))
    shutil.copyfile(src, dst)
    COPIED.append(dst)
    img = os.path.join(S, 'images', name + '.sqsh')
    shutil.copyfile(img, os.path.join(CARDIR, name + '.sqsh'))
for name, tag in PLAIN:
    src = os.path.join(S, 'env-%s%s.json' % (name, '' if tag == 'a' else '-b'))
    dst = os.path.join(ENVDIR, 'env-plain%s.json' % ('' if tag == 'a' else '-b'))
    shutil.copyfile(src, dst)
    COPIED.append(dst)
shutil.copyfile(os.path.join(S, 'plain-input.bin'),
                os.path.join(CARDIR, 'plain-input.bin'))

# carrier hashes
with open(os.path.join(A, 'carriers.sha256'), 'w') as f:
    for fn in sorted(os.listdir(CARDIR)):
        p = os.path.join(CARDIR, fn)
        h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
        f.write('%s  %s\n' % (h, fn))

# features + labels
sys.path.insert(0, A)
import importlib.util
spec = importlib.util.spec_from_file_location('triage', os.path.join(A, 'sqfs-triage.py'))
triage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(triage)
rules = triage.parse_table(open(os.path.join(A, 'SKILL-fixture.md'), encoding='utf-8').read())

rows = []
for dst in COPIED:
    env = json.load(open(dst))
    f = triage.features(env)
    data = env.get('data') if 'data' in env else env
    nr = data['normalized_result']
    diags = nr.get('diagnostics') or []
    tn = sorted(r.get('report', {}).get('__typename__', '?')
                for r in diags if isinstance(r, dict))
    rows.append({
        'envelope': os.path.basename(dst),
        'carrier_sha256': (data.get('subject') or {}).get('digest', {}).get('sha256'),
        'evidence_id': data.get('evidence_id'),
        'ok': env.get('ok'),
        'H': sorted(f['H']), 'G': sorted(f['G']), 'D': sorted(f['D']),
        'BE': f['BE'], 'SR': f['SR'], 'P': f['P'],
        'coverage': f['coverage'], 'published_bytes': f['published_bytes'],
        'gap_count': len(nr.get('extraction_gaps') or []),
        'unpublished_count': len(nr.get('unpublished_entries') or []),
        'diagnostics': tn,
        'label': triage.classify(rules, f),
    })
with open(os.path.join(A, 'features.tsv'), 'w') as f:
    cols = ['envelope', 'carrier_sha256', 'evidence_id', 'label', 'H', 'G', 'D',
            'BE', 'SR', 'P', 'gap_count', 'unpublished_count', 'diagnostics',
            'coverage', 'published_bytes', 'ok']
    f.write('\t'.join(cols) + '\n')
    for r in rows:
        f.write('\t'.join('+'.join(r[c]) if isinstance(r[c], list) else
                          ('n/a' if r[c] is None else str(r[c]))
                          for c in cols) + '\n')
print(json.dumps(rows, indent=1))
