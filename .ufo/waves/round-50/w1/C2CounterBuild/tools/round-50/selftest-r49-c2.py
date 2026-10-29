#!/usr/bin/env python3
"""DRAFT `tools/round-50/selftest-r49-c2.py`: the `--selftest` the round-49 closure asked
`tools/round-49/c2-mismatch.py` to have, as a separate instrument (`tools/round-49/` stays
byte-frozen and is not edited).

It extracts the frozen round-49 counter from git at its FREEZE `decc5697` (refusing any
other bytes: sha256 pinned below), runs it over committed git objects of the lane
(`--root`) and compares the results with the committed expected values in
`selftest-r49-c2.expected.json` beside this file:

  freeze   `--rev decc5697 --freeze decc5697`            exit 1, mismatches 9, red A1..A9
  landing  `--rev 00b18504 --freeze decc5697 --battery`  exit 0, mismatches 0, battery
           failing [], 16 mutations, do-nothing red A1..A9
  counter  the sha256 of the extracted counter blob equals the pinned FREEZE blob.

Result JSON (`--json-out`): {"cases": N, "failures": [...], "expected_sha256": <sha256 of
the expected file>, "observed": {...}}.  Exit 0 every case equals its expected value,
1 a case differs, 2 could not run (a commit or the counter blob absent).
Usage: selftest-r49-c2.py --root LANE --work DIR [--json-out PATH]
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile

FREEZE49 = 'decc5697bfd4ec1e9de4a762ad199d9bd9c4230d'
LANDED49 = '00b185045b82af9398e7497d068a14ee3023fecb'
COUNTER = 'tools/round-49/c2-mismatch.py'
COUNTER_SHA = '9b80b3b0e3945563426510e72969a7b5fed3e66a47b567d3a8341fc1f5d8595d'


def git(root, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env['GIT_NO_REPLACE_OBJECTS'] = '1'
    return subprocess.run(['git', '-C', root] + list(args), capture_output=True, env=env)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--json-out')
    a = ap.parse_args(argv)
    here = os.path.dirname(os.path.abspath(__file__))
    raw = open(os.path.join(here, 'selftest-r49-c2.expected.json'), 'rb').read()
    expected = json.loads(raw)
    out = {'cases': 0, 'failures': [], 'expected_sha256': hashlib.sha256(raw).hexdigest(),
           'observed': {}}

    def done(code):
        if a.json_out:
            with open(a.json_out, 'w') as fh:
                json.dump(out, fh, indent=1, sort_keys=True)
        return code

    blob = git(a.root, 'cat-file', 'blob', '%s:%s' % (FREEZE49, COUNTER))
    if blob.returncode != 0:
        out['failures'].append('counter blob absent at %s' % FREEZE49[:8])
        return done(2)
    obs = out['observed']
    obs['counter_sha256'] = hashlib.sha256(blob.stdout).hexdigest()
    d = tempfile.mkdtemp(prefix='st49-', dir=a.work)
    cpath = os.path.join(d, 'c2-mismatch.py')
    with open(cpath, 'wb') as fh:
        fh.write(blob.stdout)
    env = {k: os.environ[k] for k in ('PATH', 'HOME', 'LANG', 'LC_ALL') if k in os.environ}
    env['TMPDIR'] = a.work

    def run(rev, battery):
        cmd = [sys.executable, '-I', '-B', cpath, '--root', a.root, '--rev', rev,
               '--freeze', FREEZE49]
        if battery:
            cmd.append('--battery')
        p = subprocess.run(cmd, capture_output=True, env=env, timeout=600)
        try:
            j = json.loads(p.stdout)
        except ValueError:
            return {'exit': p.returncode, 'unparsed': True}
        r = {'exit': p.returncode, 'mismatches': j.get('mismatches'),
             'red': sorted(k for k, v in j.get('atoms', {}).items() if not v['ok'])}
        if battery:
            b = j.get('battery', {})
            r['failing'] = b.get('failing')
            r['mutations'] = len(b.get('mutations', []))
            r['do_nothing_red'] = b.get('do_nothing_red')
        return r

    for name, rev, bat in (('freeze', FREEZE49, False), ('landing', LANDED49, True)):
        if git(a.root, 'cat-file', '-e', rev + '^{commit}').returncode != 0:
            out['failures'].append('commit %s absent in --root' % rev[:8])
            return done(2)
        obs[name] = run(rev, bat)
    for k in sorted(set(expected) | set(obs)):
        out['cases'] += 1
        if expected.get(k) != obs.get(k):
            out['failures'].append('%s: expected %s, observed %s' % (
                k, json.dumps(expected.get(k), sort_keys=True), json.dumps(obs.get(k), sort_keys=True)))
    return done(1 if out['failures'] else 0)


if __name__ == '__main__':
    sys.exit(main())
