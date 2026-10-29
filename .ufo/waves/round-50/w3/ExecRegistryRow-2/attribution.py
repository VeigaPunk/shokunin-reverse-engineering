#!/usr/bin/env python3
"""Decisive attribution test for the 49-byte stub that appeared in the lane tree.

Question: did THIS seat's fixture scripts create the stray
`tools/round-50-c3/sqfs-triage-v5.py` (49 bytes, content
`#!/usr/bin/env python3\n# simulated C3 instrument\n`) in the lane tree and in
the fleet repo?

Evidence assembled:
  A. STATIC: every write in my scripts is `os.path.join(clone, path)` where
     `clone = os.path.join(root, 'clone')` and `root` is a mkdtemp under my
     scratch -- an ABSOLUTE path under /fast/scratch.  A relative write to
     `tools/round-50-c3/...` is impossible from them.
  B. CHRONOLOGICAL: the stray's mtime precedes the mtime of the only script of
     mine that contains that literal.
  C. EMPIRICAL: run my scripts with the lane tree under observation and check
     whether the stub appears.

Prints a verdict; writes nothing.
"""
import os
import re
import subprocess
import sys
import tempfile

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
FLEET = '/home/vgpnk/Projects/shokunin'
SCRATCH = os.environ.get('TMPDIR', '/fast/scratch/hyaku/kaidoku-r50/w3-ExecRegistryRow-2')
STUB_REL = os.path.join('tools', 'round-50-c3', 'sqfs-triage-v5.py')
STUB_TEXT = '#!/usr/bin/env python3\n# simulated C3 instrument\n'

print('== A. STATIC: write targets in my scripts ==')
for name in ('final-landing.py', 'drift-extension.py', 'validate-peer-row.py',
             'registry-couplings.py'):
    p = os.path.join(SCRATCH, name)
    if not os.path.exists(p):
        print('  %-22s (not present)' % name)
        continue
    src = open(p, encoding='utf-8').read()
    writes = [ln.strip() for ln in src.split('\n')
              if re.search(r"open\([^)]*['\"]w['\"]", ln)]
    rel = [ln for ln in writes if not re.search(r'os\.path\.join\((clone|root|D|C|LANE|SEAT)', ln)]
    print('  %-22s writes=%d  non-clone-relative=%d' % (name, len(writes), len(rel)))
    for ln in rel:
        print('      !! %s' % ln)

print()
print('== B. CHRONOLOGICAL ==')
stub_paths = [os.path.join(LANE, STUB_REL), os.path.join(FLEET, STUB_REL)]
for sp in stub_paths:
    if os.path.exists(sp):
        st = os.stat(sp)
        print('  %s  size=%d mtime=%.6f' % (sp, st.st_size, st.st_mtime))
    else:
        print('  %s  ABSENT' % sp)
for name in ('final-landing.py', 'drift-extension.py'):
    p = os.path.join(SCRATCH, name)
    if os.path.exists(p):
        st = os.stat(p)
        has = STUB_TEXT.strip() in open(p, encoding='utf-8').read()
        print('  %-22s mtime=%.6f  contains-stub-literal=%s' % (name, st.st_mtime, has))

print()
print('== C. EMPIRICAL: run my scripts, watch the lane and fleet trees ==')
watch = [os.path.join(LANE, STUB_REL), os.path.join(FLEET, STUB_REL)]
before = {p: (os.path.exists(p), os.stat(p).st_mtime if os.path.exists(p) else None)
          for p in watch}
print('  before:', before)
for name in ('drift-extension.py', 'final-landing.py'):
    p = os.path.join(SCRATCH, name)
    if not os.path.exists(p):
        continue
    r = subprocess.run(['python3', '-I', '-B', p], capture_output=True, text=True,
                       cwd=SCRATCH, env=dict(os.environ, TMPDIR=SCRATCH))
    after = {q: (os.path.exists(q), os.stat(q).st_mtime if os.path.exists(q) else None)
             for q in watch}
    print('  ran %-22s rc=%d  after=%s' % (name, r.returncode, after))
print('  VERDICT: my scripts create the stray =',
      any(os.path.exists(p) and before[p][0] is False for p in watch))
