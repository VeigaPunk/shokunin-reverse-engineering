#!/usr/bin/env python3
"""Mutation sweep on the round-41 C2 counter's own selftest battery.

Each mutant is a single textual substitution of c2-counter.py; the mutant is
run with `--selftest` and the sweep records the pass count and the cases that
caught it.  A mutant that survives (all 60 cases still pass) is a hole in the
battery, not a property of the claim.

Usage: python3 mutants.py [--jobs N]
Writes one JSON line per mutant to stdout and a summary table to stderr.
Scratch: $HYAKU_SCRATCH/kaidoku-r41/R41C2Counter/mutants (removed at exit).
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'c2-counter.py')

SPAN_FIRST_ROW = """    stop = end
    for i in range(mi + 1, end):
        l = lines[i]
        if re.match(r'^#{1,4} ', l) or re.match(r'^\\s*-\\s+\\*\\*', l) \\
                or l.strip().startswith('<!-- sqfs-triage-table'):"""
SPAN_MUT = """    mi = next((i for i in range(mi + 1, end)
               if lines[i].lstrip().startswith('|')), mi)
    stop = end
    for i in range(mi + 1, end):
        l = lines[i]
        if re.match(r'^#{1,4} ', l) or re.match(r'^\\s*-\\s+\\*\\*', l) \\
                or l.strip().startswith('<!-- sqfs-triage-table'):"""

MUTANTS = [
    ('M1 block starts at the first table row (drops the actions line)',
     SPAN_FIRST_ROW, SPAN_MUT),
    ('M2 no SKILL block drift scan (path check only)',
     '    scanned, drift = skill_block_drift(root, freeze, rev, skill_fz)',
     '    scanned, drift = [], []'),
    ('M3 writer never frozen',
     '    scope = writer_scope(root, freeze, as_text(gen_b), declared)',
     '    scope = {}'),
    ('M4 no-match pair accepts any single row (round-40 D2)',
     '                if v != {None}:\n                    ok_rows = False',
     '                pass'),
    ('M5 expected pair taken from class_expected, not the evaluator',
     '            e = exp.get(cid)',
     '            e = ce.get(cid) or exp.get(cid)'),
    ('M6 declared feature tuple not bound',
     "        b['observed_features_match_declared'] = N > 0 and not feat_missing \\",
     "        b['observed_features_match_declared'] = True or N > 0 and not feat_missing \\"),
    ("M7 a plain creation counts as a frozen touch",
     "            if st in ('M', 'D', 'R', 'T', 'U'):",
     "            if st in ('A', 'M', 'D', 'R', 'T', 'U'):"),
    ('M8 row consistency not bound (round-40 D2 shortcut unbound)',
     "        b['row_decisions_consistent'] = bool(reported and ok_rows)",
     "        b['row_decisions_consistent'] = True"),
    ('M9 real-receipt binding not bound',
     "        b['real_receipts_depth_limited'] = bool(real_ok)",
     "        b['real_receipts_depth_limited'] = True"),
    ('M10 combo family size not bound',
     "    b['combo_family_wellformed'] = len(combos) == COMBO_COUNT and \\",
     "    b['combo_family_wellformed'] = True or len(combos) == COMBO_COUNT and \\"),
]


def run_one(idx, name, old, new, root, src):
    d = tempfile.mkdtemp(prefix='mut%d.' % idx, dir=root)
    text = open(src).read()
    if old not in text:
        return {'mutant': name, 'status': 'PATTERN-MISSING'}
    path = os.path.join(d, 'c2-counter.py')
    with open(path, 'w') as fh:
        fh.write(text.replace(old, new, 1))
    env = dict(os.environ)
    env['TMPDIR'] = d
    env['HYAKU_SCRATCH'] = root
    pr = subprocess.run([sys.executable, '-I', '-B', path, '--selftest'],
                        capture_output=True, text=True, env=env, cwd=d, timeout=1800)
    doc = None
    for line in pr.stdout.splitlines():
        if line.startswith('{'):
            try:
                doc = json.loads(line)
            except Exception:
                pass
            break
    shutil.rmtree(d, ignore_errors=True)
    if doc is None:
        return {'mutant': name, 'status': 'NO-RESULT', 'exit': pr.returncode,
                'stderr': pr.stderr[-400:]}
    killed = doc['fail'] > 0
    return {'mutant': name, 'status': 'KILLED' if killed else 'SURVIVED',
            'cases': doc['cases'], 'pass': doc['pass'], 'fail': doc['fail'],
            'caught_by': [f.split(':')[0] for f in doc['failures']][:6],
            'exit': pr.returncode}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--jobs', type=int, default=4)
    a = ap.parse_args()
    root = os.path.join(os.environ.get('HYAKU_SCRATCH') or tempfile.gettempdir(),
                        'kaidoku-r41', 'R41C2Counter', 'mutants')
    os.makedirs(root, exist_ok=True)
    try:
        with ThreadPoolExecutor(max_workers=a.jobs) as ex:
            rows = list(ex.map(lambda t: run_one(t[0], *t[1], root, SRC),
                               list(enumerate(MUTANTS))))
        for r in rows:
            print(json.dumps(r, sort_keys=True))
        killed = sum(1 for r in rows if r['status'] == 'KILLED')
        print('MUTANTS total=%d killed=%d survived=%d' % (
            len(rows), killed,
            sum(1 for r in rows if r['status'] == 'SURVIVED')), file=sys.stderr)
        return 0 if killed == len(rows) else 1
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
