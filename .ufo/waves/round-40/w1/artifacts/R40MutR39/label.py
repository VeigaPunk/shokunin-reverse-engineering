#!/usr/bin/env python3
"""Label the 20 round-39 held-out envelopes with a sqfs-triage copy; count agreements."""
import json, os, subprocess, sys

S = os.path.dirname(os.path.abspath(__file__))
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
SKILL = os.path.join(LANE, 'SKILL.md')
HELD = os.path.join(LANE, 'corpus/evidence/round-39/c2/heldout')

def run(tool):
    man = json.load(open(os.path.join(HELD, 'manifest.json')))
    exp = {}
    envs = []
    for c in man['carriers']:
        cid = c['id']
        want = c.get('label') if isinstance(c.get('label'), str) and c.get('label') else c['class']
        exp[cid] = want
        envs.append((cid, os.path.join(HELD, cid, 'envelope.json')))
    p = subprocess.run([sys.executable, '-I', '-B', tool, '--skill', SKILL] + [e for _, e in envs],
                       capture_output=True, text=True, timeout=120)
    if p.returncode != 0:
        return {'run_exit': p.returncode, 'stderr_tail': (p.stderr or '')[-300:]}
    got = {}
    for line in (p.stdout or '').splitlines():
        if '\t' not in line:
            continue
        path, lab = line.rsplit('\t', 1)
        cid = os.path.basename(os.path.dirname(path.strip()))
        got[cid] = lab.strip()
    agree = sum(1 for cid, w in exp.items() if got.get(cid) == w)
    flips = {cid: {'want': w, 'got': got.get(cid)} for cid, w in exp.items() if got.get(cid) != w}
    return {'run_exit': 0, 'agree': agree, 'n': len(exp), 'flips': flips}

if __name__ == '__main__':
    print(json.dumps(run(sys.argv[1]), sort_keys=True))
