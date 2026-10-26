#!/usr/bin/env python3
"""Read-only clause table for the R38 draft after-receipts.

Applies the frozen C1 counter's per-carrier clauses (c1-counter.py: matched(),
chunk_handlers(), gaps(), subject digest) to the draft envelopes that wave 1
produced, WITHOUT writing into corpus/evidence/round-38 and without claiming
they are the landed receipts.

Usage:
  python3 draft-clauses.py [--root LANE]

Exit: 0 always (this is a table, not a verdict).
"""
import argparse
import glob
import json
import os

AFT = '.ufo/waves/round-38/w1/artifacts'
ORADIR = 'corpus/evidence/round-37/c1'
PINS = {
    'K1': '1cfb6c33f915aa64255465fba9f2074bb0f294a192f3e3058cb34bea8286117e',
    'K2': '403cb0a827966bbe17a70e08af7d39b43260da8201d1b9001bbc4228cbc99154',
    'K3': '9c7c523c5d1d1cafc0b679af9092ce0289d9656f6a24bc3bd0009f95b69397c0',
    'K4': 'a29ddc15f5a6abcabf28b7161837eb56b34111e48420e7392e648f2fdfe956ed',
}
RECEIPTS = [
    ('K1', 'seat', f'{AFT}/R38ExecAfterK1/after.json'),
    ('K1', 'seat-onpath', f'{AFT}/R38ExecAfterK1/after.sasquatch-on-path.json'),
    ('K1', 'patch', f'{AFT}/R38ExecProvincePatch/after-K1.json'),
    ('K2', 'seat', f'{AFT}/R38ExecAfterK2/after.json'),
    ('K2', 'patch', f'{AFT}/R38ExecProvincePatch/after-K2.json'),
    ('K3', 'seat', f'{AFT}/R38ExecAfterK3/after.json'),
    ('K3', 'seat-onpath', f'{AFT}/R38ExecAfterK3/diagnostic-after-with-declared-extractor.json'),
    ('K3', 'patch', f'{AFT}/R38ExecProvincePatch/after-K3.json'),
    ('K4', 'seat', f'{AFT}/R38ExecAfterK4/after.json'),
    ('K4', 'patch', f'{AFT}/R38ExecProvincePatch/after-K4.json'),
]


def oracle(root, k):
    rows = []
    with open(os.path.join(root, ORADIR, k, 'oracle.tsv')) as fh:
        for line in fh:
            if line.strip():
                rel, sha, _size = line.rstrip('\n').split('\t')
                rows.append((rel, sha))
    return rows


def published(env):
    nr = env.get('normalized_result') or {}
    return [(f.get('relative_path') or '', f.get('sha256') or '') for f in (nr.get('files') or [])]


def handlers(env):
    nr = env.get('normalized_result') or {}
    return [c.get('handler') for c in (nr.get('chunks') or []) if isinstance(c, dict)]


def gaps(env):
    return (env.get('normalized_result') or {}).get('extraction_gaps') or []


def hits(orc, files):
    return sum(1 for rel, sha in orc if any(sha == fs and (fp == rel or fp.endswith('/' + rel)) for fp, fs in files))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.')
    a = ap.parse_args()
    print('carrier\tvariant\treceipt\tsubject_ok\thandler_ok\tgaps\toracle_hits\toracle_rows\tpublished\tcoverage')
    for k, variant, rel in RECEIPTS:
        p = os.path.join(a.root, rel)
        if not os.path.exists(p):
            print(f'{k}\t{variant}\t{rel}\tMISSING', flush=True)
            continue
        env = json.load(open(p))
        orc = oracle(a.root, k)
        subj = ((env.get('subject') or {}).get('digest') or {}).get('sha256')
        nr = env.get('normalized_result') or {}
        g = gaps(env)
        print('\t'.join(str(x) for x in (
            k, variant, rel,
            'yes' if subj == PINS[k] else 'NO',
            'yes' if 'squashfs_v4_be' in handlers(env) else 'NO',
            len(g),
            hits(orc, published(env)),
            len(orc),
            len(published(env)),
            nr.get('coverage'),
        )))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
