#!/usr/bin/env python3
"""cross-check-r40.py - run the drafted v3 table on the COMMITTED round-40 C2 envelopes.

The round-41 held-out set does not exist yet (its seed is the freeze hash), so the only
real envelopes available in wave 1 are the round-40 ones, which the round-40 manifest
already labels.  This script is a sanity check, not the R41-C2 score: it confirms the
drafted v3 table reproduces the committed v2 decisions on every committed envelope, and it
shows the extracted features beside each decision so a reader can see which row fired.

Reads: the draft table, the interpreter, ``corpus/evidence/round-40/c2/heldout`` (envelopes
+ manifest).  Writes nothing but stdout.

Usage: python3 -I -B cross-check-r40.py [--table T.md] [--interp I.py] [--heldout DIR]
"""

import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
DEFAULT_TABLE = os.path.join(HERE, 'sqfs-triage-v3-table.md')
DEFAULT_INTERP = os.path.join(HERE, 'sqfs-triage-v3.py')
DEFAULT_HELDOUT = LANE + '/corpus/evidence/round-40/c2/heldout'


def main(argv=None):
    parser = argparse.ArgumentParser(prog='cross-check-r40.py')
    parser.add_argument('--table', default=DEFAULT_TABLE)
    parser.add_argument('--interp', default=DEFAULT_INTERP)
    parser.add_argument('--heldout', default=DEFAULT_HELDOUT)
    ns = parser.parse_args(argv)

    with open(os.path.join(ns.heldout, 'manifest.json'), 'r', encoding='utf-8') as handle:
        manifest = json.load(handle)
    carriers = manifest['carriers']
    paths = [os.path.join(ns.heldout, carrier['id'], 'envelope.json')
             for carrier in carriers]
    res = subprocess.run([sys.executable, '-I', '-B', ns.interp, '--skill', ns.table,
                          '--json', *paths], capture_output=True, text=True)
    if res.returncode != 0:
        print('interpreter exit %d\n%s' % (res.returncode, res.stderr))
        return 2
    results = json.loads(res.stdout)['results']
    if len(results) != len(carriers):
        print('%d results for %d carriers' % (len(results), len(carriers)))
        return 2

    bad = 0
    print('%-4s %-24s %-24s %-22s %-22s %s'
          % ('id', 'class', 'features', 'manifest', 'v3 table', 'agree'))
    for carrier, result in zip(carriers, results):
        feat = result['features']
        got = (result['label'], result['action'])
        want = (carrier['label'], carrier['action'])
        agree = got == want
        bad += 0 if agree else 1
        print('%-4s %-24s H=%-14s G=%-28s BE=%-4s SR=%-3s P=%-3d %-22s %-22s %s'
              % (carrier['id'], carrier['class'], '|'.join(feat['H']) or '-',
                 '|'.join(feat['G']) or '-', feat['BE'], feat['SR'], feat['P'],
                 '%s/%s' % want, '%s/%s' % got, 'yes' if agree else 'NO'))
    print('envelopes: %d  agree: %d  disagree: %d' % (len(carriers), len(carriers) - bad,
                                                      bad))
    print('rows fired: %s'
          % sorted({result['rule'] for result in results},
                   key=lambda value: (value is None, value)))
    return 0 if bad == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
