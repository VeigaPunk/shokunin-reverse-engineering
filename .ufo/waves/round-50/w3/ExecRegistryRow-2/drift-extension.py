#!/usr/bin/env python3
"""Does a NON-.py file added under tools/round-50/ also trip the frozen counters?

The C1 counter's frozen_drift() treats EVERY path under the FROZEN_PREFIXES
('tools/round-50/') as frozen, regardless of extension: an 'A' status under the
prefix is drift (tools/round-50/c1-counter.py, frozen_drift, code 'A' branch).
The C2 counter's FROZEN tuple is ('tools/round-50', 'plans/round-50-claims.md')
and its Git.touched() walks the same pathspec.

If that is so, the L1 cannot land C3 control fixtures (tables, manifests, any
extension) under tools/round-50/ either -- not just .py/.sh.

Measured here on a throwaway clone in scratch.  Read-only on the lane.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
FREEZE = '435d41fd4ad9211d1579fc447936fb33d2b74467'
BASE = 'f890bbead20ca2c549487167f56876ae47f1e1a4'
SCRATCH = os.environ.get('TMPDIR', '/fast/scratch/hyaku/kaidoku-r50/w3-ExecRegistryRow-2')

spec = importlib.util.spec_from_file_location(
    'c1c', os.path.join(LANE, 'tools/round-50/c1-counter.py'))
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)

root = tempfile.mkdtemp(prefix='drift-', dir=SCRATCH)
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

CASES = [
    ('tools/round-50/sqfs-triage-v5.py', '#!/usr/bin/env python3\n', 'a .py instrument'),
    ('tools/round-50/control-fixtures/c3/ctl-do-nothing.skill.md', '| a | b |\n',
     'a .md control table under control-fixtures/'),
    ('tools/round-50/control-fixtures/c3/manifest.json', '{}\n',
     'a .json control manifest under control-fixtures/'),
    ('tools/round-50/anything.txt', 'x\n', 'a .txt file directly under tools/round-50/'),
    ('tools/round-50-c3/sqfs-triage-v5.py', '#!/usr/bin/env python3\n',
     'the moved path (outside the prefix)'),
]

out = []
for path, content, label in CASES:
    subprocess.run(['git', '-C', clone, 'checkout', '--detach', '-q', BASE], check=True)
    subprocess.run(['git', '-C', clone, 'reset', '--hard', '-q', BASE], check=True)
    full = os.path.join(clone, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as fh:
        fh.write(content)
    subprocess.run(['git', '-C', clone, 'add', '-A', path], check=True)
    subprocess.run(['git', '-C', clone, 'commit', '-q', '-m', 'fixture: ' + label], check=True)
    rev = subprocess.run(['git', '-C', clone, 'rev-parse', 'HEAD'],
                         capture_output=True, text=True).stdout.strip()
    drift = c1.frozen_drift(clone, FREEZE, rev, spec_obj)
    # C2 side: does the frozen c2-record.py's own freeze_check fire?
    work = os.path.join(root, 'w-' + os.path.basename(path))
    os.makedirs(work, exist_ok=True)
    rc = subprocess.run(
        ['python3', '-I', '-B', os.path.join(clone, 'tools/round-50/c2-record.py'),
         '--root', clone, '--rev', rev, '--freeze', FREEZE,
         '--work', work, '--json-out', os.path.join(work, 'rc.json')],
        capture_output=True, text=True)
    detail = ''
    try:
        d = json.load(open(os.path.join(work, 'rc.json')))
        detail = '%s / %s' % (d.get('reason'), str(d.get('detail'))[:90])
    except Exception as exc:
        detail = 'no receipt: %r' % exc
    out.append({'label': label, 'path': path, 'c1_frozen_drift': drift,
                'c2_exit': rc.returncode, 'c2_reason': detail})
    print(json.dumps(out[-1], ensure_ascii=False))

shutil.rmtree(root, ignore_errors=True)
print(json.dumps(out, indent=1, ensure_ascii=False))
