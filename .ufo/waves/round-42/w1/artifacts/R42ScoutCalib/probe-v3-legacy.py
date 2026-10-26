#!/usr/bin/env python3
"""Probe: what does the frozen round-41 v3 interpreter print for an envelope whose only SquashFS
handler is a v1-v3 unblob handler name?  Usage: probe-v3-legacy.py LANE_CLONE_AT_BASE WORKDIR
Takes the round-41 held-out envelope of a class, rewrites every squashfs* handler string, runs the
interpreter on the rewritten copy under WORKDIR (honours the argument; no /tmp)."""
import copy, json, subprocess, sys, pathlib
lane, work = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); work.mkdir(parents=True, exist_ok=True)
man = json.load(open(lane/'corpus/evidence/round-41/c2/heldout/manifest.json'))
byc = {}
for c in man['carriers']: byc.setdefault(c['class'], c['id'])
def rewrite(o, h):
    if isinstance(o, dict):
        for k, v in list(o.items()):
            if k == 'handler' and isinstance(v, str) and v.startswith('squashfs'): o[k] = h
            else: rewrite(v, h)
    elif isinstance(o, list):
        for x in o: rewrite(x, h)
for cls in ('clean-le', 'clean-be', 'dep-missing-le', 'body-extractor-failure', 'partial-body-failure', 'escaping-symlink-removed'):
    e = json.load(open(lane/f'corpus/evidence/round-41/c2/heldout/{byc[cls]}/envelope.json'))
    for h in ('squashfs_v1', 'squashfs_v2', 'squashfs_v3', 'squashfs_v3_ddwrt', 'squashfs_v3_broadcom', 'squashfs_v3_nonstandard', 'squashfs_v2_nonstandard', 'squashfs_v4_broadcom'):
        e2 = copy.deepcopy(e); rewrite(e2, h)
        p = work/f'{cls}-{h}.json'; json.dump(e2, open(p, 'w'))
        r = subprocess.run(['python3', '-I', '-B', str(lane/'tools/round-41/sqfs-triage-v3.py'), '--skill', str(lane/'SKILL.md'), str(p)], capture_output=True, text=True, cwd=work)
        print(f'{cls}\t{h}\trc={r.returncode}\t{r.stdout.strip().split(chr(9),1)[-1]}')
