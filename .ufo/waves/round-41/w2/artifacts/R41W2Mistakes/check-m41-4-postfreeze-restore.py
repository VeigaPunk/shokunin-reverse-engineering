#!/usr/bin/env python3
"""M41-4 check (R41W2Mistakes): seat R41C1Counter rewrote its artifacts after the
freeze; the lane restored the freeze bytes and kept the post-freeze versions
aside.

Verifies:
  1. every file under .ufo/waves/round-41/w1/artifacts/R41C1Counter/ at the tip
     7a24ff74 is byte-identical to the freeze-committed blob (d764389e) -- the
     freeze bytes were restored, so the rewrite never entered any tree;
  2. the kept-aside dir R41C1Counter-postfreeze/ at the tip differs from the
     freeze bytes for the files it holds (the rewrite is preserved, not hidden);
  3. the frozen counter tools/round-41/c1-counter.py differs from BOTH the
     freeze artifact copy and the post-freeze copy (three distinct byte sets).

RED on the mistaken state: point --mistaken-fixture at a directory holding the
post-freeze bytes over the frozen artifact path (as the seat left them after the
rewrite); check 1 then fails -> exit 1.
GREEN on the repaired fixture: the real lane tree at the tip -> exit 0.

usage: check-m41-4-postfreeze-restore.py LANE [--mistaken-fixture DIR]
"""
import argparse, hashlib, os, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument('lane')
ap.add_argument('--mistaken-fixture')
a = ap.parse_args()

FREEZE = 'd764389e9cbe61b9d1b07538ff3bff02d50bb34f'
TIP = '7a24ff74736e84b1903db7ba01891c406a6e32a2'
ART = '.ufo/waves/round-41/w1/artifacts/R41C1Counter'
PF = '.ufo/waves/round-41/w1/artifacts/R41C1Counter-postfreeze'
TOOL = 'tools/round-41/c1-counter.py'

def blob(path, rev):
    out = subprocess.check_output(['git', '-C', a.lane, 'cat-file', 'blob',
                                   f'{rev}:{path}'],
                                  stderr=subprocess.DEVNULL)
    return hashlib.sha256(out).hexdigest()

def tree_files(path, rev):
    out = subprocess.check_output(['git', '-C', a.lane, 'ls-tree', '-r',
                                   '--name-only', rev, '--', path], text=True)
    return [l for l in out.split() if l.startswith(path + '/')]

def disk_sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()

art_dir = (a.mistaken_fixture if a.mistaken_fixture
           else os.path.join(a.lane, ART))

# artifact bytes at the "committed" site: git tip tree, or the mistaken fixture
# on disk
def artifact_sha(rel):
    if a.mistaken_fixture:
        return disk_sha(os.path.join(art_dir, rel))
    return blob(ART + '/' + rel, TIP)

fail = []
for p in tree_files(ART, FREEZE):
    rel = p[len(ART) + 1:]
    bf = blob(p, FREEZE)
    bt = artifact_sha(rel)
    if bf != bt:
        fail.append(f'{rel}: freeze {bf[:12]} != committed {bt[:12]}')
for p in tree_files(PF, TIP):
    rel = p[len(PF) + 1:]
    frez = os.path.join(ART, rel)
    try:
        bf = blob(frez, FREEZE)
    except subprocess.CalledProcessError:
        continue  # file did not exist at freeze
    bp = blob(p, TIP)
    if bf == bp:
        fail.append(f'{p}: kept-aside copy identical to freeze bytes')
bf = blob(ART + '/' + 'c1-counter.py', FREEZE)
bp = blob(PF + '/' + 'c1-counter.py', TIP)
bt = blob(TOOL, TIP)
if len({bf, bp, bt}) != 3:
    fail.append(f'expected three distinct counter byte sets, got '
                f'freeze={bf[:12]} postfreeze={bp[:12]} tool={bt[:12]}')
print({'artifact_files': len(tree_files(ART, FREEZE)),
       'freeze_c1_counter_sha': bf[:12],
       'postfreeze_c1_counter_sha': bp[:12],
       'frozen_tool_sha': bt[:12],
       'failures': fail})
sys.exit(1 if fail else 0)
