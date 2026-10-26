#!/usr/bin/env python3
"""dev-score.py -- score the candidate v2 table and its kill controls.

Reads tables/dev-expectations.json (label, action per development envelope),
runs sqfs-triage-v2-dev.py over every envelope in envelopes/, and repeats the
score for each control table in controls/.  Nothing here touches the lane's
frozen tools or any held-out carrier: every envelope was produced by this seat
from fresh trees in scratch.

Usage: python3 -B dev-score.py [--table PATH] [--envelopes DIR]
Exit 0 when the candidate table matches every expectation, 1 otherwise.
"""

import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.join(HERE, 'sqfs-triage-v2-dev.py')


def classify(table, envelope, work):
    res = subprocess.run([sys.executable, '-I', '-B', DEV, '--skill', table,
                          '--envelope', envelope],
                         capture_output=True, text=True, cwd=work)
    if res.returncode != 0:
        return ('exit-%d' % res.returncode, res.stderr.strip()[:80])
    line = res.stdout.strip().splitlines()[-1]
    return tuple(line.split('\t'))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--table', default=os.path.join(HERE, 'candidate-triage-v2.md'))
    ap.add_argument('--envelopes', default=os.path.join(HERE, 'envelopes'))
    ap.add_argument('--quiet', action='store_true')
    ns = ap.parse_args(argv)
    with open(os.path.join(HERE, 'tables', 'dev-expectations.json'), 'r',
              encoding='utf-8') as handle:
        exp = json.load(handle)
    work = os.environ.get('TMPDIR') or HERE

    def score(table):
        ok = 0
        rows = []
        for name in sorted(exp):
            want = tuple(exp[name])
            got = classify(table, os.path.join(ns.envelopes, name + '.json'), work)
            good = got == want
            ok += good
            rows.append((name, want, got, good))
        return ok, rows

    ok, rows = score(ns.table)
    print('candidate table: %s' % os.path.basename(ns.table))
    if not ns.quiet:
        for name, want, got, good in rows:
            print('  %s %-30s want %-26s got %-26s'
                  % ('PASS' if good else 'FAIL', name, '/'.join(want), '/'.join(got)))
    print('dev-score: %d/%d' % (ok, len(rows)))

    controls = sorted(name for name in os.listdir(os.path.join(HERE, 'controls'))
                      if name.endswith('.md'))
    for name in controls:
        path = os.path.join(HERE, 'controls', name)
        cok, crows = score(path)
        tally = {}
        for _n, _w, got, _g in crows:
            tally['/'.join(got)] = tally.get('/'.join(got), 0) + 1
        print('control %-32s %2d/%d  %s' % (name, cok, len(crows),
                                            ', '.join('%s x%d' % (k, v)
                                                      for k, v in sorted(tally.items()))))
    return 0 if ok == len(rows) else 1


if __name__ == '__main__':
    sys.exit(main())
