#!/usr/bin/env python3
"""Collect receipts for the r52 v6 battery measurement runs.

Every receipt: exact command, exit code, stdout sha256, UTC time.
"""
import hashlib, os, subprocess, sys, datetime

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
S = '/fast/scratch/hyaku/kaidoku-r52/w1-MutTriV6'
SEAT = LANE + '/.ufo/waves/round-52/w1/MutTriV6'
OUT = os.path.join(SEAT, 'receipts.tsv')

ENV = dict(os.environ, TMPDIR=S, PYTHONHASHSEED='0')

CMDS = [
    ('R01-v5-instrument-sha256',
     "sha256sum %s/tools/round-50-c3/sqfs-triage-v5.py" % LANE, LANE),
    ('R02-v5-controls-committed-receipts',
     "python3 -c \"import json,glob;"
     "[print(f.split('/')[-1], json.load(open(f))['pair_mismatch_count'],"
     " json.load(open(f))['verdict']) for f in sorted(glob.glob('%s/.ufo/waves/round-50/c3/ctl-*.json'))]\""
     % LANE, LANE),
    ('R03-v5-instrument-controls-run',
     "python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --controls "
     "--envelopes .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes "
     "--work %s/work --json-out %s/v5-controls.json" % (S, S), LANE),
    ('R04-census3-check-at-claims-base',
     "git show ab0eafedc41402b43b41a4362084119578dfe7ce:tools/round-51/census3.json | "
     "python3 -c \"import sys,json; d=json.load(sys.stdin); print(len(d['paths']))\"", LANE),
    ('R05-census3-selftest',
     "python3 -I -B tools/round-51/census3.py --selftest", LANE),
    ('R06-census-check-with-census2',
     "python3 -I -B tools/round-51/census3.py --root . --rev WORKTREE --check "
     "--census tools/round-48/census2.json", LANE),
    ('R07-r50-controls-scored-under-v6-evaluator',
     "python3 %s/final_measure.py" % S, S),
    ('R08-design-dependence-probe',
     "python3 %s/design_probe.py %s/design-dependence.json" % (S, SEAT), S),
    ('R09-two-scope-witness-probe',
     "python3 %s/two_scope.py %s/two-scope-witness.json" % (S, SEAT), S),
    ('R10-evidence-emit',
     "python3 %s/emit_evidence.py %s/evidence.json" % (S, SEAT), S),
    ('R10e-definitive-mutant-classification',
     "python3 %s/classify_final.py %s/mutant-classification.json" % (S, SEAT), S),
    ('R10b-census-width-probe',
     "python3 %s/census_width.py %s/census-width.json" % (S, SEAT), S),
    ('R10c-v5-reader-census-lines',
     "sed -n '150,156p' tools/round-50-c3/sqfs-triage-v5.py", LANE),
    ('R10d-corpus-ddwrt-failed-count',
     "python3 -c \"import importlib.util,os;"
     "spec=importlib.util.spec_from_file_location('v5','tools/round-50-c3/sqfs-triage-v5.py');"
     "m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);"
     "r='.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes';"
     "e=[x for x in m.envelope_entries(r)];"
     "f=[m.load_envelope(p) for _,p in e];"
     "print('ddwrt envelopes',sum(1 for x in f if 'squashfs_v3_ddwrt' in x['H']),"
     "'ddwrt FAILED',sum(1 for x in f if 'squashfs_v3_ddwrt' in x['H'] and 'extractor-failure' in x['G'] and x['P']==0))\"",
     LANE),
    ('R11-claims-base-registry-count',
     "git show ab0eafedc41402b43b41a4362084119578dfe7ce:SKILL.md | "
     "python3 -c \"import sys; t=sys.stdin.read();"
     "b=t.split('<!-- instrument-registry v2 -->',1)[1].split('<!-- /instrument-registry -->',1)[0];"
     "print(len([l for l in b.splitlines() if l.strip().startswith('|')]))\"", LANE),
    ('R12-round-50-c3-dir-contents',
     "ls tools/round-50-c3/", LANE),
    ('R13-ddwrt-reader-measurement',
     "cat .ufo/waves/round-49/w1/C1ScribeEntry/v3-readers.out", LANE),
    ('R14-fleet-repo-clean-check',
     "git -C /home/vgpnk/Projects/shokunin status --porcelain", '/home/vgpnk/Projects/shokunin'),
    ('R15-lane-repo-untracked-check',
     "git -C %s status --porcelain" % LANE, LANE),
]


def run(cmd, cwd):
    proc = subprocess.run(['bash', '-c', cmd], capture_output=True, text=True, cwd=cwd,
                          env=ENV)
    out = proc.stdout or ''
    err = proc.stderr or ''
    return {
        'cmd': cmd, 'cwd': cwd, 'exit': proc.returncode,
        'stdout_sha256': hashlib.sha256(out.encode()).hexdigest(),
        'stdout_bytes': len(out.encode()),
        'stderr_sha256': hashlib.sha256(err.encode()).hexdigest(),
        'stderr_bytes': len(err.encode()),
        'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'stdout_head': out[:600],
        'stderr_head': err[:300],
    }


rows = []
for rid, cmd, cwd in CMDS:
    r = run(cmd, cwd)
    r['id'] = rid
    rows.append(r)
    print('%-40s exit=%d stdout_sha=%s' % (rid, r['exit'], r['stdout_sha256'][:16]))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write('id\tutc\tcwd\texit\tstdout_sha256\tstdout_bytes\tstderr_sha256\tstderr_bytes\tcommand\n')
    for r in rows:
        fh.write('\t'.join([
            r['id'], r['utc'], r['cwd'], str(r['exit']), r['stdout_sha256'],
            str(r['stdout_bytes']), r['stderr_sha256'], str(r['stderr_bytes']),
            r['cmd'].replace('\t', ' ')]) + '\n')
print('wrote', OUT)
