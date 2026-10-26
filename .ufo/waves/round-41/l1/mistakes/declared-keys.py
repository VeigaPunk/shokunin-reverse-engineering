#!/usr/bin/env python3
"""M41-1 check: every held-out carrier's declared feature tuple must sit under a key the frozen
C2 counter reads (class_expected.features, features, declared_features). Exit 1 if any does not.
usage: declared-keys.py MANIFEST.json"""
import json, sys
m = json.load(open(sys.argv[1]))
bad = []
for c in m['carriers']:
    cex = c.get('class_expected')
    ok = (isinstance(cex, dict) and isinstance(cex.get('features'), dict)) or \
        isinstance(c.get('features'), dict) or isinstance(c.get('declared_features'), dict)
    if not ok:
        bad.append(c['id'])
print(json.dumps({'carriers': len(m['carriers']), 'unreadable_by_counter': bad}))
sys.exit(1 if bad else 0)
