#!/usr/bin/env python3
"""M41-1 check (R41W2Mistakes): every held-out carrier's declared feature tuple
must sit under a key the frozen C2 counter reads.

The frozen counter (tools/round-41/c2-counter.py, lines ~1497-1503) reads the
declared tuple from `class_expected.features`, else `features`, else
`declared_features`.  The frozen generator (tools/round-41/heldout-gen-v3.py)
writes the 12 combo carriers' tuple under `declared` (with `class_expected:
null`), so the counter marks them declared-tuple-incomplete:
`observed_features_match_declared` false at scoring time.

RED on the mistaken state: the committed manifest
corpus/evidence/round-41/c2/heldout/manifest.json -> 12 unreadable combos, exit 1.
GREEN on the repaired fixture: manifest-repaired-green.json (same manifest with
each combo's tuple also copied under `features`) -> zero unreadable, exit 0.

usage: check-m41-1-declared-keys.py MANIFEST.json
"""
import json, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    HERE, 'manifest-repaired-green.json')

m = json.load(open(MANIFEST))
bad = []
for c in m['carriers']:
    cex = c.get('class_expected')
    ok = (isinstance(cex, dict) and isinstance(cex.get('features'), dict)) or \
        isinstance(c.get('features'), dict) or \
        isinstance(c.get('declared_features'), dict)
    if not ok:
        bad.append(c['id'])
print({'manifest': MANIFEST, 'carriers': len(m['carriers']),
       'unreadable_by_counter': bad})
sys.exit(1 if bad else 0)
