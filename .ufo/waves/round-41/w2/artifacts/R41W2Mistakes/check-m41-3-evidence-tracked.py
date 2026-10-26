#!/usr/bin/env python3
"""M41-3 check (R41W2Mistakes): every C1 receipt file named by the round-41 data
procedure is present in the tree at REV.

RED on the mistaken state: at 5ca6941b (the data commit), V4/after.json is
absent because jj-lane.sh's directory commit skipped the 2.8 MiB new file
(snapshot.max-new-file-size = 1MiB).  GREEN on the repaired fixture: at
e9a24d07 (the commit that landed V4/after.json as a named file) everything is
present.

usage: check-m41-3-evidence-tracked.py LANE REV
exit 1 when any expected C1 receipt is missing from the REV tree.
"""
import subprocess, sys

LANE, REV = sys.argv[1], sys.argv[2]

# Files the c1 data procedure must publish for a full C1 landing.  run.json is
# legitimately absent for V4 (M41-5, ARG cap), so the required set is after.json
# for all four carriers plus run.json for V3/L3/L4; the V4 run-harness-failure
# log records the run.json miss.
REQUIRED = [
    'corpus/evidence/round-41/c1/V3/after.json',
    'corpus/evidence/round-41/c1/V3/run.json',
    'corpus/evidence/round-41/c1/V4/after.json',
    'corpus/evidence/round-41/c1/L3/after.json',
    'corpus/evidence/round-41/c1/L3/run.json',
    'corpus/evidence/round-41/c1/L4/after.json',
    'corpus/evidence/round-41/c1/L4/run.json',
]
tracked = set(subprocess.check_output(
    ['git', '-C', LANE, 'ls-tree', '-r', '--name-only', REV, '--',
     'corpus/evidence/round-41/c1/'],
    text=True).split())
missing = [p for p in REQUIRED if p not in tracked]
print({'rev': REV, 'missing': missing})
sys.exit(1 if missing else 0)
