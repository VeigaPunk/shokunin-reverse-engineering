#!/usr/bin/env python3
"""ExecFetchDry receipt generator (round-50 w3).

Re-runs every cheap, offline or HEAD-only command and records: exact argv,
UTC start/end, exit code, stdout sha256, stderr sha256.  No image is
downloaded; no REA run; nothing is written into the lane tree.
"""
import datetime
import hashlib
import json
import os
import subprocess
import sys

S = '/fast/scratch/hyaku/kaidoku-r50/w3-ExecFetchDry'
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
FREEZE = '435d41fd4ad9211d1579fc447936fb33d2b74467'
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
os.environ['TMPDIR'] = S


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def rec(name, argv, cwd=None, note=''):
    t0 = utc()
    p = subprocess.run(argv, capture_output=True, cwd=cwd)
    t1 = utc()
    r = {'name': name, 'argv': argv, 'cwd': cwd or os.getcwd(),
         'utc_start': t0, 'utc_end': t1, 'exit_code': p.returncode,
         'stdout_sha256': sha(p.stdout), 'stderr_sha256': sha(p.stderr),
         'stdout_bytes': len(p.stdout), 'stderr_bytes': len(p.stderr),
         'stdout_tail': p.stdout.decode('utf-8', 'replace')[-400:],
         'stderr_tail': p.stderr.decode('utf-8', 'replace')[-400:],
         'note': note}
    with open(os.path.join(OUT, name + '.json'), 'w') as fh:
        json.dump(r, fh, indent=1, sort_keys=True)
    print('%-28s exit=%s  out_sha=%s  %s' % (name, r['exit_code'], r['stdout_sha256'][:16], t1))
    return r


recs = []
FV = LANE + '/tools/round-50/fetch-vendor.py'

recs.append(rec('01-fetch-selftest',
                ['python3', '-I', '-B', FV, '--selftest'],
                cwd=S, note='offline chain selftest, 16 cases, no network'))

for cid, url in (
    ('g7581', 'https://download.avm.de/fritzbox/fritzbox-7581/other/fritz.os/FRITZ.Box_7581-07.18.image'),
    ('g7582', 'https://download.avm.de/fritzbox/fritzbox-7582/other/fritz.os/FRITZ.Box_7582-07.18.image'),
    ('c6490', 'https://download.avm.de/fritzbox/fritzbox-6490-cable/deutschland/fritz.os/FRITZ.Box_6490_Cable-07.57.image'),
    ('c6430', 'https://download.avm.de/fritzbox/fritzbox-6430-cable/deutschland/fritz.os/FRITZ.Box_6430_Cable-07.30.image'),
):
    recs.append(rec('02-head-' + cid,
                    ['curl', '-sSI', '--max-time', '60', url],
                    cwd=S, note='HTTP HEAD only: Content-Length/ETag/Last-Modified'))

# containment + origin allowlist (real fetch path, no network reached)
recs.append(rec('03-cache-inside-lane-refused',
                ['python3', '-I', '-B', FV, '--spec', S + '/contain/ok.json',
                 '--cache', LANE + '/.ufo/waves/round-50/w3/ExecFetchDry/never-cache'],
                cwd=S, note='--cache inside the lane -> exit 2, nothing written'))
recs.append(rec('04-image-cache-inside-lane-refused',
                ['python3', '-I', '-B', FV, '--spec', S + '/contain/ok.json',
                 '--cache', S + '/contain/c',
                 '--image-cache', LANE + '/.ufo/waves/round-50/w3/ExecFetchDry/never-ic'],
                cwd=S, note='--image-cache inside the lane -> exit 2, nothing written'))
recs.append(rec('05-origin-allowlist-bad-host',
                ['python3', '-I', '-B', FV, '--spec', S + '/contain/badhost.json',
                 '--cache', S + '/contain/c'],
                cwd=S, note='https://example.com -> link=url, exit 1, no network'))
recs.append(rec('06-origin-allowlist-bad-scheme',
                ['python3', '-I', '-B', FV, '--spec', S + '/contain/badscheme.json',
                 '--cache', S + '/contain/c'],
                cwd=S, note='http://download.avm.de -> link=url, exit 1, no network'))
recs.append(rec('07-usage-error',
                ['python3', '-I', '-B', FV, '--cache', S + '/contain/c'],
                cwd=S, note='missing --spec/--root --rev -> exit 2'))

# lane git facts (read-only)
recs.append(rec('08-carriers-blob-across-revs',
                ['git', '-C', LANE, 'rev-parse',
                 FREEZE + ':tools/round-50/carriers.json',
                 'f890bbead20ca2c549487167f56876ae47f1e1a4:tools/round-50/carriers.json',
                 '6f4aba635fc47b5823ed42afe9c8b5dc3e28127f:tools/round-50/carriers.json'],
                cwd=S, note='one blob id for all three revs'))
recs.append(rec('09-post-freeze-commits-touching-tools-round-50',
                ['git', '-C', LANE, 'log', '-m', '--diff-merges=first-parent',
                 '--name-status', '--pretty=format:COMMIT %h %s',
                 FREEZE + '..HEAD', '--', 'tools/round-50/'],
                cwd=S, note='empty output: no post-freeze commit touched tools/round-50/'))

# fixture clone: drift effect of the planned C3 instrument path
CLONE = S + '/clone'
PY = '''
import json, subprocess, importlib.util, os, sys
S, CLONE, LANE, FREEZE = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
def g(*a): return subprocess.run(['git','-C',CLONE,*a],capture_output=True,text=True).stdout.strip()
def imp(name, path):
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
c1 = imp('c1c', LANE+'/tools/round-50/c1-counter.py')
c2 = imp('c2r', LANE+'/tools/round-50/c2-record.py')
sp = json.loads(subprocess.run(['git','-C',CLONE,'show',FREEZE+':tools/round-50/carriers.json'],capture_output=True).stdout)
BASE='f890bbead20ca2c549487167f56876ae47f1e1a4'
r = c2.Git(CLONE)
out = {'c1_drift_at_base': c1.frozen_drift(CLONE, FREEZE, BASE, sp),
       'c2_freeze_at_base': list(c2.freeze_check(r, FREEZE, BASE))}
for label, path in (('planned','tools/round-50/sqfs-triage-v5.py'),
                    ('outside','tools/round-50-c3/sqfs-triage-v5.py')):
    subprocess.run(['git','-C',CLONE,'checkout','--detach',BASE],check=True,capture_output=True)
    fp = os.path.join(CLONE, path); os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp,'w').write('# fixture instrument\\n')
    subprocess.run(['git','-C',CLONE,'add',path],check=True,capture_output=True)
    subprocess.run(['git','-C',CLONE,'commit','-q','-m','fixture: C3 instrument at '+path],check=True,capture_output=True)
    rev = g('rev-parse','HEAD')
    out['case_'+label] = {'path': path, 'rev': rev,
        'c1_frozen_drift': c1.frozen_drift(CLONE, FREEZE, rev, sp),
        'c2_freeze_check': list(c2.freeze_check(r, FREEZE, rev))}
print(json.dumps(out, indent=1, sort_keys=True))
'''
open(S + '/receipts/fixture_drift.py', 'w').write(PY)
recs.append(rec('10-fixture-c3-instrument-drift',
                ['python3', '-I', '-B', S + '/receipts/fixture_drift.py', S, CLONE, LANE, FREEZE],
                cwd=S, note='in-process: c1.frozen_drift + c2.freeze_check at a fixture commit '
                            'that adds the C3 instrument at the planned path vs a path outside tools/round-50/'))
with open(os.path.join(S, 'receipts', 'fixture-drift.json'), 'w') as fh:
    fh.write(recs[-1]['stdout_tail'])
    fh.write('\n')
print('receipts written to', OUT)
