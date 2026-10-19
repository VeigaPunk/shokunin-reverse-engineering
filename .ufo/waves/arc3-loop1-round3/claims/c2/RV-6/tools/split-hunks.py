#!/usr/bin/env python3
"""Split a unified diff into hunks and list them with added-line summaries,
so the reviewer can select exactly the closure hunks of a landed revision.

usage: python3 split-hunks.py <patch-file>
"""
import sys

path = sys.argv[1]
lines = open(path).read().splitlines(keepends=True)
hunks, cur, head = [], None, []
for ln in lines:
    if ln.startswith('@@'):
        if cur is not None:
            hunks.append(cur)
        cur = [ln]
    elif cur is None:
        head.append(ln)
    else:
        if ln.startswith('--- a/'):
            hunks.append(cur); cur = None; head.append(ln)
        else:
            cur.append(ln)
if cur is not None:
    hunks.append(cur)

print("header lines: %d, hunks: %d" % (len(head), len(hunks)))
KEY = ('uneval', 'UNEVALUABLE', 'read_error', 'READ-ERROR', 'EXIT_UNEVALUABLE', 'stat_error')
for i, h in enumerate(hunks):
    added = [l[1:].rstrip() for l in h if l.startswith('+') and not l.startswith('+++')]
    hit = any(any(k in a for k in KEY) for a in added)
    print("[%02d] %-22s +%d -%d  %s%s" % (
        i, h[0].split('@@')[1].strip(), len(added),
        sum(1 for l in h if l.startswith('-') and not l.startswith('---')),
        "CLOSURE-CANDIDATE " if hit else "",
        (added[0][:60] if added else "")))
print("\nselection helper: python3 split-hunks.py patch > /dev/null; then edit and"
      " re-run with SELECT='0 4 7' env to emit selected hunks to selected.patch")
sel = sys.argv[2] if len(sys.argv) > 2 else None
if sel:
    idx = [int(x) for x in sel.split()]
    out = head + [l for i in idx for l in hunks[i]]
    open('selected.patch', 'w').write(''.join(out))
    print("wrote selected.patch with hunks %s" % idx)