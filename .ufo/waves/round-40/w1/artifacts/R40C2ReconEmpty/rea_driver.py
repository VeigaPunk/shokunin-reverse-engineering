#!/usr/bin/env python3
"""Run REA 6.5.0 extract-firmware over the zero-regular-file dev carriers."""
import json
import os
import subprocess
import sys
import time

S = os.environ.get('R40_WORK') or os.path.dirname(os.path.abspath(__file__))
HOME = os.path.expanduser('~')
UNBLOB = os.path.join(HOME, '.local', 'bin', 'unblob')
HOME_BIN = os.path.join(HOME, '.local', 'bin')

RUNS = []
for tree in ('T1', 'T2', 'T3'):
    for endian in ('le', 'be'):
        for comp in ('gzip', 'xz'):
            RUNS.append(('%s-%s-%s' % (tree, endian, comp),
                         os.path.join(S, 'carriers', '%s-%s-%s.sqsh' % (tree, endian, comp)),
                         'after'))
for endian in ('le', 'be'):
    for comp in ('gzip', 'xz'):
        RUNS.append(('T5-%s-%s' % (endian, comp),
                     os.path.join(S, 'carriers', 'T5-%s-%s.sqsh' % (endian, comp)),
                     'after'))
for endian in ('le', 'be'):
    RUNS.append(('T4-%s-gzip' % endian,
                 os.path.join(S, 'carriers', 'T4-%s-gzip.sqsh' % endian), 'after'))
    RUNS.append(('T6-%s-gzip' % endian,
                 os.path.join(S, 'carriers', 'T6-%s-gzip.sqsh' % endian), 'after'))
RUNS += [
    ('T1-avm-gzip', os.path.join(S, 'carriers', 'T1-avm-gzip.sqsh'), 'after'),
    ('T2-avm-xz', os.path.join(S, 'carriers', 'T2-avm-xz.sqsh'), 'after'),
    ('NOTSQFS-gzip', os.path.join(S, 'carriers', 'NOTSQFS-gzip.bin'), 'after'),
    ('T1-be-gzip-dep', os.path.join(S, 'carriers', 'T1-be-gzip.sqsh'), 'before'),
    ('T1-le-gzip-dep', os.path.join(S, 'carriers', 'T1-le-gzip.sqsh'), 'before'),
    ('T2-be-xz-dep', os.path.join(S, 'carriers', 'T2-be-xz.sqsh'), 'before'),
]


def env_for(arm):
    env = dict(os.environ)
    env['REA_UNBLOB_COMMAND'] = UNBLOB
    env['TMPDIR'] = S
    if arm == 'before':
        want = os.path.realpath(HOME_BIN)
        kept = [p for p in env.get('PATH', '').split(os.pathsep)
                if p and os.path.realpath(p) != want]
        env['PATH'] = os.pathsep.join(kept)
    return env


def main():
    out_dir = os.path.join(S, 'envelopes')
    os.makedirs(out_dir, exist_ok=True)
    rows = []
    for run_id, carrier, arm in RUNS:
        work = os.path.join(S, 'runs', run_id)
        os.makedirs(work, exist_ok=True)
        outdir = os.path.join(work, 'out')
        if os.path.exists(outdir):
            raise SystemExit('pre-existing outdir %s' % outdir)
        argv = ['npx', '-y', 'rea-agents@6.5.0', 'extract-firmware',
                '--format', 'json', '--full-output', carrier, outdir]
        env = env_for(arm)
        t0 = time.time()
        proc = subprocess.run(argv, cwd=work, env=env, capture_output=True, text=True)
        dur = round(time.time() - t0, 1)
        stdout = proc.stdout.strip()
        full = None
        if stdout:
            try:
                full = json.loads(stdout)
            except json.JSONDecodeError:
                start = stdout.find('{')
                if start >= 0:
                    try:
                        full = json.loads(stdout[start:])
                    except json.JSONDecodeError:
                        full = None
        with open(os.path.join(out_dir, run_id + '.full.json'), 'w', encoding='utf-8') as h:
            if full is None:
                h.write(json.dumps({'error': 'no JSON envelope',
                                    'stdout_head': stdout[:2000],
                                    'stderr_tail': proc.stderr[-2000:]}, indent=1))
            else:
                json.dump(full, h, indent=1, sort_keys=True)
            h.write('\n')
        rec = {'id': run_id, 'arm': arm, 'exit_code': proc.returncode,
               'carrier': carrier, 'rea_argv': ['rea-agents@6.5.0', 'extract-firmware',
                                                '--format', 'json', '--full-output',
                                                '<carrier>', '<fresh outdir>'],
               'unblob_command': UNBLOB, 'home_bin_on_path': HOME_BIN in env['PATH'].split(os.pathsep),
               'duration_s': dur, 'json_ok': full is not None,
               'ok': (full or {}).get('ok') if isinstance(full, dict) else None,
               'stdout_bytes': len(proc.stdout), 'stderr_tail': proc.stderr[-400:]}
        with open(os.path.join(out_dir, run_id + '.run.json'), 'w', encoding='utf-8') as h:
            json.dump(rec, h, indent=1, sort_keys=True)
            h.write('\n')
        rows.append(rec)
        print('%-16s exit=%d ok=%s json=%s %ss' % (run_id, proc.returncode, rec['ok'],
                                                   rec['json_ok'], dur))
    with open(os.path.join(out_dir, 'runs.json'), 'w', encoding='utf-8') as h:
        json.dump(rows, h, indent=1, sort_keys=True)
        h.write('\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
