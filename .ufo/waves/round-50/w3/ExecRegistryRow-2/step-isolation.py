#!/usr/bin/env python3
"""Which step of final-landing.py touches the LANE tree?

The attribution run showed the lane file `tools/round-50-c3/sqfs-triage-v5.py`
changing mtime after final-landing.py ran, while drift-extension.py did not.
This isolates the responsible step, one subprocess at a time, recording the
lane file's (size, mtime, sha256) before and after each.

Read-only measurement; the clone lives under scratch.
"""
import hashlib
import os
import shutil
import subprocess
import tempfile

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
SCRATCH = os.environ.get('TMPDIR', '/fast/scratch/hyaku/kaidoku-r50/w3-ExecRegistryRow-2')
WATCH = os.path.join(LANE, 'tools/round-50-c3/sqfs-triage-v5.py')
BASE = 'f890bbead20ca2c549487167f56876ae47f1e1a4'


def snap():
    if not os.path.exists(WATCH):
        return ('ABSENT', None, None)
    b = open(WATCH, 'rb').read()
    st = os.stat(WATCH)
    return (hashlib.sha256(b).hexdigest()[:16], st.st_size, st.st_mtime)


root = tempfile.mkdtemp(prefix='steps-', dir=SCRATCH)
clone = os.path.join(root, 'clone')
state = {'watch': snap()}
print('start           ', state['watch'])


def step(label, fn):
    before = snap()
    r = fn()
    after = snap()
    changed = 'CHANGED' if before != after else 'same'
    print('%-28s %-8s rc=%s  %s -> %s' % (label, changed, getattr(r, 'returncode', '-'),
                                         before, after))
    return r


step('git clone --shared', lambda: subprocess.run(
    ['git', 'clone', '--shared', '-q', LANE, clone], capture_output=True, text=True))
step('checkout --detach BASE', lambda: subprocess.run(
    ['git', '-C', clone, 'checkout', '--detach', '-q', BASE], capture_output=True, text=True))
step('reset --hard BASE', lambda: subprocess.run(
    ['git', '-C', clone, 'reset', '--hard', '-q', BASE], capture_output=True, text=True))
step('git clean -qfd', lambda: subprocess.run(
    ['git', '-C', clone, 'clean', '-qfd'], capture_output=True, text=True))


def write_instr():
    full = os.path.join(clone, 'tools/round-50-c3/sqfs-triage-v5.py')
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as fh:
        fh.write('#!/usr/bin/env python3\n# simulated C3 instrument\n')


step('write instrument in clone', write_instr)
step('git add -A', lambda: subprocess.run(
    ['git', '-C', clone, 'add', '-A', 'tools/round-50-c3/sqfs-triage-v5.py'],
    capture_output=True, text=True))
step('git commit', lambda: subprocess.run(
    ['git', '-C', clone, '-c', 'user.name=k', '-c', 'user.email=k@l', 'commit', '-q', '-m', 'x'],
    capture_output=True, text=True))
rev = subprocess.run(['git', '-C', clone, 'rev-parse', 'HEAD'],
                     capture_output=True, text=True).stdout.strip()
work = os.path.join(root, 'w')
os.makedirs(work, exist_ok=True)
step('c2-record.py --root clone', lambda: subprocess.run(
    ['python3', '-I', '-B', os.path.join(clone, 'tools/round-50/c2-record.py'),
     '--root', clone, '--rev', rev, '--freeze', '435d41fd4ad9211d1579fc447936fb33d2b74467',
     '--work', work, '--json-out', os.path.join(work, 'rc.json')],
    capture_output=True, text=True))

print()
print('lane watch after all steps:', snap())
print('lane file sha256 now     :', hashlib.sha256(open(WATCH, 'rb').read()).hexdigest())
print('clone file sha256        :',
      hashlib.sha256(open(os.path.join(clone, 'tools/round-50-c3/sqfs-triage-v5.py'), 'rb').read()).hexdigest())
shutil.rmtree(root, ignore_errors=True)
