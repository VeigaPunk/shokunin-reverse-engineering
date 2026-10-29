#!/usr/bin/env python3
"""FINAL end-to-end verification of the simulated C3 landing.

Landing set = the peer seat's registry row + the C3 instrument at the L1's moved
path tools/round-50-c3/sqfs-triage-v5.py, committed together, then the FROZEN
counter is run at that REV with the C1 freeze:

  python3 -I -B tools/round-50/c2-record.py --root <clone> --rev <C3 landing>
          --freeze 435d41fd... --work <scratch> --json-out <receipt>

Expected: exit 0, mismatches 0, 11/11 atoms green including B9.
Control arm: the same landing with the instrument at the OLD in-tree path.
Also runs the C1 counter's frozen_drift() on both.
Read-only on the lane; all commits are in a throwaway scratch clone.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
SEAT = os.path.join(LANE, '.ufo/waves/round-50/w3/ExecRegistryRow')
FREEZE = '435d41fd4ad9211d1579fc447936fb33d2b74467'
BASE = 'f890bbead20ca2c549487167f56876ae47f1e1a4'
SCRATCH = os.environ.get('TMPDIR', '/fast/scratch/hyaku/kaidoku-r50/w3-ExecRegistryRow-2')

spec = importlib.util.spec_from_file_location(
    'c1c', os.path.join(LANE, 'tools/round-50/c1-counter.py'))
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)

row = open(os.path.join(SEAT, 'row-final.txt'), encoding='utf-8').read().rstrip('\n')
skill_head = subprocess.run(['git', '-C', LANE, 'show', BASE + ':SKILL.md'],
                             capture_output=True, text=True).stdout
close = '\n<!-- /instrument-registry -->'
skill_with = skill_head.replace(close, '\n' + row + close, 1)

root = tempfile.mkdtemp(prefix='landing-', dir=SCRATCH)
clone = os.path.join(root, 'clone')
subprocess.run(['git', 'clone', '--shared', '-q', LANE, clone], check=True)
subprocess.run(['git', '-C', clone, 'checkout', '--detach', '-q', BASE], check=True)
subprocess.run(['git', '-C', clone, 'config', 'user.name', 'kaidoku fixture'], check=True)
subprocess.run(['git', '-C', clone, 'config', 'user.email', 'fixture@localhost'], check=True)
top = subprocess.run(['git', '-C', clone, 'rev-parse', '--show-toplevel'],
                     capture_output=True, text=True).stdout.strip()
assert top == clone, (top, clone)
spec_obj = json.loads(subprocess.run(
    ['git', '-C', clone, 'show', FREEZE + ':tools/round-50/carriers.json'],
    capture_output=True, text=True).stdout)

out = []
for label, inst_path in (
        ('MOVED path tools/round-50-c3/ + registry row', 'tools/round-50-c3/sqfs-triage-v5.py'),
        ('OLD in-tree path tools/round-50/ + registry row', 'tools/round-50/sqfs-triage-v5.py')):
    subprocess.run(['git', '-C', clone, 'checkout', '--detach', '-q', BASE], check=True)
    subprocess.run(['git', '-C', clone, 'reset', '--hard', '-q', BASE], check=True)
    subprocess.run(['git', '-C', clone, 'clean', '-qfd'], check=True)
    full = os.path.join(clone, inst_path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as fh:
        fh.write('#!/usr/bin/env python3\n# simulated C3 instrument\n')
    with open(os.path.join(clone, 'SKILL.md'), 'w') as fh:
        fh.write(skill_with)
    subprocess.run(['git', '-C', clone, 'add', '-A', inst_path, 'SKILL.md'], check=True)
    subprocess.run(['git', '-C', clone, 'commit', '-q', '-m', 'fixture: ' + label], check=True)
    rev = subprocess.run(['git', '-C', clone, 'rev-parse', 'HEAD'],
                         capture_output=True, text=True).stdout.strip()
    work = os.path.join(root, 'w-' + label.split()[0])
    os.makedirs(work, exist_ok=True)
    rc = subprocess.run(
        ['python3', '-I', '-B', os.path.join(clone, 'tools/round-50/c2-record.py'),
         '--root', clone, '--rev', rev, '--freeze', FREEZE,
         '--work', work, '--json-out', os.path.join(work, 'rc.json')],
        capture_output=True, text=True)
    d = json.load(open(os.path.join(work, 'rc.json')))
    drift = c1.frozen_drift(clone, FREEZE, rev, spec_obj)
    rec = {'label': label, 'instrument_path': inst_path, 'rev': rev,
           'c2_exit': rc.returncode, 'c2_reason': d.get('reason'),
           'c2_detail': str(d.get('detail'))[:120],
           'mismatches': d.get('mismatches'), 'atoms_total': d.get('atoms_total'),
           'red_atoms': {k: v['why'] for k, v in (d.get('atoms') or {}).items() if not v['ok']},
           'B9_atom': (d.get('atoms') or {}).get('B9'),
           'c1_frozen_drift': drift}
    out.append(rec)
    print(json.dumps(rec, ensure_ascii=False))

shutil.rmtree(root, ignore_errors=True)
print(json.dumps(out, indent=1, ensure_ascii=False))
