#!/usr/bin/env python3
"""RV-6 landed-bytes mutation builder.

usage: mutate.py <base.py> <landed.py> <outdir> <mode>
  mode = full   -> revert every D2-closure runtime hunk
  mode = guard  -> revert only the compare_section guard hunk

Selects hunks by executable-code content (not index, so it survives revision
drift), writes revert.patch, reverse-applies to a copy of the landed tool, and
prints the selection + resulting sha256.
"""
import hashlib
import os
import shutil
import subprocess
import sys

base, landed, outdir, mode = sys.argv[1:5]

RUNTIME_PATTERNS = (
    'fields["read_error"] =',
    'ref_uneval = bool(',
    'unevaluable = sum(',
    'state = {EXIT_MATCH: "OK", EXIT_UNEVALUABLE:',
    'lines.append("READ-ERROR:',
    '"stat_error": re.compile(',
    '"stat_error", "read_error"',
)
GUARD_PATTERN = 'ref_uneval = bool('

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

diff = subprocess.run(['diff', '-u', base, landed], capture_output=True, text=True).stdout
lines = diff.splitlines(keepends=True)
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
# strip the original ---/+++ so patch -p4 finds the copy we name
head2 = [h for h in head if not h.startswith(('---', '+++'))]
head2 = ['--- a/custody-pair.py\n', '+++ b/custody-pair.py\n']

sel = []
for i, h in enumerate(hunks):
    added = [l[1:] for l in h if l.startswith('+') and not l.startswith('+++')]
    guard = any(GUARD_PATTERN in a for a in added)
    runtime = any(any(p in a for p in RUNTIME_PATTERNS) for a in added)
    if mode == 'guard' and guard:
        sel.append((i, h))
    if mode == 'full' and runtime and not added[0].lstrip().startswith('#') and not guard:
        sel.append((i, h))
    if mode == 'full' and guard:
        sel.append((i, h))

print("hunks total=%d selected=%d mode=%s" % (len(hunks), len(sel), mode))
for i, h in sel:
    print("  [%02d] %s" % (i, h[0].strip()))
if not sel:
    sys.exit("no hunks selected")

os.makedirs(outdir, exist_ok=True)
patch_path = os.path.join(outdir, 'revert.patch')
open(patch_path, 'w').write(''.join(head2 + [l for _, h in sel for l in h]))
shutil.copy(landed, os.path.join(outdir, 'custody-pair.py'))
r = subprocess.run(['patch', '-R', '-p1', '-i', os.path.abspath(patch_path)],
                   cwd=outdir, capture_output=True, text=True)
print(r.stdout.strip(), r.stderr.strip())
print("landed  sha256:", sha(landed))
print("mutated sha256:", sha(os.path.join(outdir, 'custody-pair.py')))