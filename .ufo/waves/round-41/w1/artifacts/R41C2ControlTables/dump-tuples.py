#!/usr/bin/env python3
"""dump-tuples.py - the planned-class feature tuples the controls are scored on.

Reads every */envelope.json under --envelopes with the DEV replica reader, runs the
precedence list, and prints one markdown row per envelope: class, the seven features
(OP, PR, H, G, D, BE, SR, P), the expected (label, action) and its precedence step,
plus provenance (committed round-40 envelope or predicted fixture).

Usage: dump-tuples.py --envelopes DIR
"""

import argparse
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, filename))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


FEAT = load('v3checkinterp', 'v3-check-interp.py')
PREC = load('previewprecedence', 'preview-precedence.py')


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--envelopes', required=True)
    ns = ap.parse_args(argv)
    rows = []
    for name in sorted(os.listdir(ns.envelopes)):
        path = os.path.join(ns.envelopes, name, 'envelope.json')
        if not os.path.isfile(path):
            continue
        with open(path, 'r', encoding='utf-8') as handle:
            obj = json.load(handle)
        fixture = obj.get('_control_fixture') or {}
        feat = FEAT.load_envelope(path)
        label, action, step = PREC.expected(feat)
        rows.append((name, fixture, feat, label, action, step))
    print('| class fixture | OP | PR | H | G | D | BE | SR | P | expected | step | source |')
    print('| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |')
    for name, fixture, feat, label, action, step in rows:
        source = fixture.get('derived_from', 'committed: corpus/evidence/round-40/c2/'
                                            'heldout/%s/envelope.json' % name)
        if fixture.get('predicted'):
            source = 'PREDICTED from ' + source
        print('| %s | `%s` | `%s` | %s | %s | %s | %s | %s | %d | %s/%s | %d | %s |'
              % (name, feat['OP'], feat['PV'],
                 ', '.join('`%s`' % h for h in feat['H']) or '∅',
                 ', '.join('`%s`' % g for g in feat['G']) or '∅',
                 ', '.join('`%s`' % d for d in feat['D']) or '∅',
                 feat['BE'], feat['SR'], feat['P'], label, action, step, source))
    print('\n# %d envelopes; %d predicted, %d committed'
          % (len(rows), sum(1 for row in rows if row[1].get('predicted')),
             sum(1 for row in rows if not row[1].get('predicted'))))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
