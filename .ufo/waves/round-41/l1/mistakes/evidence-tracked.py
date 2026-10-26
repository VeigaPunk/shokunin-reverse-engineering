#!/usr/bin/env python3
"""M41-3 check: every file the round wrote under an evidence dir is in the commit.
usage: evidence-tracked.py LANE REV DIR... -> exit 1 if a file on disk under DIR is absent from REV."""
import os, subprocess, sys
lane, rev, dirs = sys.argv[1], sys.argv[2], sys.argv[3:]
tracked = set(subprocess.check_output(['git', '-C', lane, 'ls-tree', '-r', '--name-only', rev, '--'] + dirs,
                                      text=True).split())
missing = []
for d in dirs:
    for root, _, files in os.walk(os.path.join(lane, d)):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), lane)
            if rel not in tracked:
                missing.append(rel)
print({'rev': rev, 'missing': sorted(missing)})
sys.exit(1 if missing else 0)
