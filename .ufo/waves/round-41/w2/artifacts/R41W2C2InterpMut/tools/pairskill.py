#!/usr/bin/env python3
"""pairskill.py -- for every KILLED-SELFTEST mutant, would the 52 held-out pairs
alone also have killed it?  Splits 'killed by both oracles' from 'selftest-only
kill' (a held-out blind spot)."""
import json
import os
import subprocess
import sys

S = '/fast/scratch/hyaku/kaidoku-r41/R41W2C2InterpMut'
OUT = os.path.join(S, 'out')
MUT = os.path.join(S, 'mut')
PRIM = os.path.join(S, 'pristine')
ENV = os.path.join(S, 'env')
FLAT = os.path.join(S, 'evalenv')
INTERP = 'sqfs-triage-v3.py'
EVAL = 'indep-eval-v3.py'


def run(args):
    return subprocess.run(args, capture_output=True, text=True)


def interp_pairs(exe):
    paths = [os.path.join(ENV, f) for f in sorted(os.listdir(ENV))]
    r = run([sys.executable, '-I', '-B', exe, '--skill',
             os.path.join(PRIM, 'SKILL.md'), *paths])
    if r.returncode != 0:
        return None
    pairs = {}
    for line in r.stdout.splitlines():
        if line.strip():
            path, label, action = line.split('\t')
            pairs[os.path.splitext(os.path.basename(path))[0]] = [label, action]
    return pairs


def eval_pairs(exe):
    r = run([sys.executable, '-I', '-B', exe, '--envelopes', FLAT])
    if r.returncode != 0:
        return None
    doc = json.loads(r.stdout)
    return {cid: [v['label'], v['action']] for cid, v in doc['labels'].items()}


def main():
    res = json.load(open(os.path.join(OUT, 'mutants-results.json')))
    ib = res['baseline']  # not stored; recompute pristine baselines
    ip = interp_pairs(os.path.join(PRIM, INTERP))
    ep = eval_pairs(os.path.join(PRIM, EVAL))
    out = {}
    for m in res['mutants']:
        if not m['verdict'].startswith('KILLED'):
            continue
        exe = m['mutant_path']
        pairs = interp_pairs(exe) if m['tool'] == INTERP else eval_pairs(exe)
        base = ip if m['tool'] == INTERP else ep
        if pairs is None:
            out[m['id']] = {'pairs_also_kills': True, 'n_changed': 'ALL(tool-failed)'}
        else:
            changed = sorted(k for k in set(base) | set(pairs)
                             if base.get(k) != pairs.get(k))
            out[m['id']] = {'pairs_also_kills': bool(changed), 'n_changed': len(changed),
                            'changed': changed[:12]}
        print('%-5s pairs_also_kills=%-5s n_changed=%s'
              % (m['id'], out[m['id']]['pairs_also_kills'], out[m['id']]['n_changed']))
    json.dump(out, open(os.path.join(OUT, 'pairs-also-kills.json'), 'w'),
              indent=1, sort_keys=True)
    only_selftest = sorted(k for k, v in out.items() if not v['pairs_also_kills'])
    print('selftest-only kills (held-out blind):', only_selftest)
    return 0


if __name__ == '__main__':
    sys.exit(main())
