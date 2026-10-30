#!/usr/bin/env python3
"""Probe 4: the wrong-carrier-set hole and the census-reader detail format.

Q1. Do CTL-OLD (2/4) and CTL-NEW (4/4) together pin the IDENTITY of the four
    scored carriers, or only a count?  Enumerate every 4-multiset of the four
    carrier ids that satisfies BOTH claimed expectations.
Q2. The law's fail-closed clause ("a gap landing on a device row is a
    violation") -- is it witnessed by ANY committed receipt?  (probe A said no.)
    Therefore no claimed control can detect a counter that breaks it.
Q3. The census reader's device-detail format: the committed oracle tables use
    `247:0` (major:minor).  What does `unsquashfs -lln` emit, and can a
    census re-derivation (F7) recover `247:0` from it?
"""
import importlib.util
import itertools
import json
import os
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
IDS = ('c6430', 'c6490', 'g7581', 'g7582')

spec = importlib.util.spec_from_file_location(
    'r50c', os.path.join(LANE, 'tools/round-50/c1-counter.py'))
M = importlib.util.module_from_spec(spec)
sys.modules['r50c'] = M
spec.loader.exec_module(M)

NONREG, ENV = {}, {}
for cid in IDS:
    raw = open(os.path.join(LANE, 'tools/round-50/oracle/%s.nonregular.tsv' % cid),
               'rb').read()
    rows, err = M.parse_nonregular(raw)
    NONREG[cid] = rows
    ENV[cid] = json.load(open(os.path.join(
        LANE, 'corpus/evidence/round-50/c1/%s/after.json' % cid)))

LAW = {
    'claim': 'R52-C1',
    'allowed': {'symlink': ['unpublished-entry'], 'char-device': [],
                'block-device': [], 'fifo': [], 'socket': [], 'dir': []},
    'required': {'symlink': True, 'char-device': False, 'block-device': False,
                 'fifo': False, 'socket': False, 'dir': False},
    'removed': {'diagnostic': 'MaliciousSymlinkRemoved', 'kinds': ['symlink'],
                'disposition': 'exclusive', 'silent': {}},
    'structural': {'depth-limited': 1, 'unknown-chunk-handler': 0},
}
R50 = json.load(open(os.path.join(LANE, 'tools/round-50/gap-rule.json')))


def green(cid, rule):
    model, _ = M.gap_rule_model(json.dumps(rule).encode())
    env = ENV[cid]
    root, _ = M.subject_root(env, None)
    od = (env.get('parameters') or {}).get('output_directory')
    ok, _ = M.disposition_check(
        (env.get('normalized_result') or {}).get('extraction_gaps') or [],
        M.diagnostics(env), NONREG[cid], model, root, od)
    esc = M.nonregular_published(M.published(env), NONREG[cid], root)
    return bool(ok and root is not None and not esc)


print('=== Q1. which 4-multisets satisfy BOTH CTL-OLD=2/4 and CTL-NEW=4/4? ===')
print('    (CTL-OLD expects 2, CTL-NEW expects 4, per the claims)')
good = []
for combo in itertools.combinations_with_replacement(IDS, 4):
    old = sum(1 for c in combo if green(c, R50))
    new = sum(1 for c in combo if green(c, LAW))
    if old == 2 and new == 4:
        good.append(combo)
for g in good:
    names = sorted(set(g))
    ok_identity = (names == sorted(IDS))
    print('    %-46s OLD=%d NEW=%d  identity=%s'
          % (str(g), sum(1 for c in g if green(c, R50)),
             sum(1 for c in g if green(c, LAW)),
             'YES' if ok_identity else 'NO  <-- passes both claimed controls'))
print('    %d of %d multisets pass both controls; %d of them score the WRONG set.'
      % (len(good), len(list(itertools.combinations_with_replacement(IDS, 4))),
         sum(1 for g in good if sorted(set(g)) != sorted(IDS))))

print('\n=== Q2. is the law fail-closed clause witnessed by any committed receipt? ===')
tot_dev = tot_devgap = 0
for cid in IDS:
    env = ENV[cid]
    root, _ = M.subject_root(env, None)
    rows_at = {}
    for rel, kind, _d in NONREG[cid]:
        rows_at.setdefault(M.strip_rel(rel), []).append(kind)
    devrows = [r for r in NONREG[cid] if r[1] == 'char-device']
    gaps = (env.get('normalized_result') or {}).get('extraction_gaps') or []
    hits = 0
    for g in gaps:
        rp = g.get('relative_path')
        if rp is None:
            continue
        rel = M.extract_rel(rp, root)
        h = rows_at.get(rel, []) if rel else []
        if len(h) == 1 and h[0] == 'char-device':
            hits += 1
    tot_dev += len(devrows)
    tot_devgap += hits
    print('    %-6s device census rows=%2d  gaps landing on a device row=%d'
          % (cid, len(devrows), hits))
print('    TOTAL: %d device census rows, %d gaps on a device row.'
      % (tot_dev, tot_devgap))
print('    -> the law clause "a gap landing on a device row is a violation"')
print('       has ZERO witnesses in the committed corpus.')

print('\n=== Q3. census reader device-detail format vs the committed table ===')
img = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'm2fix', 'img.sqsh')
if os.path.isfile(img):
    out = subprocess.run(['unsquashfs', '-lln', img], capture_output=True,
                         text=True).stdout
    print('    unsquashfs -lln on a fixture with a pseudo char device:')
    for line in out.splitlines():
        if 'dev/ttyS0' in line:
            print('      %r' % line.strip())
    print('    committed oracle detail format: %r'
          % sorted({r[2] for r in NONREG['g7581'] if r[1] == 'char-device'})[:3])
    print('    -> the reader emits "major, minor" (comma+space); the committed')
    print('       table uses "major:minor". A census re-derivation that compares')
    print('       detail strings verbatim cannot match the frozen table.')
else:
    print('    (fixture image absent; skipped)')
