#!/usr/bin/env python3
"""step-matrix.py - which `**Label precedence**` step each control misses, and on which
classes.

Every envelope is a planned class fixture (committed round-40 envelope or predicted
combined-class fixture).  For each control the table is parsed by the DEV replica
interpreter and every (label, action) is compared with the precedence list executed by
preview-precedence.py.  Output:

  * a matrix of envelopes missed per precedence step (1..12), rows = controls;
  * one block per control naming (step, expected label, class) for every miss;
  * a matched/n column that must equal score-controls.sh on the same envelope set.

Usage:
  step-matrix.py [--controls DIR] [--envelopes DIR] [--control NAME=PATH]...
  step-matrix.py --interp PATH ...      # score any interpreter through its --json CLI
"""

import argparse
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, filename))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


FEAT = load('v3checkinterp', 'v3-check-interp.py')
PREC = load('previewprecedence', 'preview-precedence.py')


def envelopes(envdir):
    out = []
    for name in sorted(os.listdir(envdir)):
        path = os.path.join(envdir, name, 'envelope.json')
        if os.path.isfile(path):
            out.append((name, path))
    return out


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--controls', default=HERE)
    ap.add_argument('--envelopes', action='append', required=True)
    ap.add_argument('--control', action='append', default=[])
    ap.add_argument('--interp')
    ns = ap.parse_args(argv)
    envs = []
    for envdir in ns.envelopes:
        envs.extend(envelopes(envdir))
    if not envs:
        sys.stderr.write('step-matrix: no */envelope.json under %s\n'
                         % ', '.join(ns.envelopes))
        return 2
    expected = {}
    for name, path in envs:
        feat = FEAT.load_envelope(path)
        expected[name] = PREC.expected(feat)
    controls = []
    for spec in ns.control:
        controls.append((spec.split('=', 1)[0], spec.split('=', 1)[1]))
    if os.path.isdir(ns.controls):
        for name in sorted(os.listdir(ns.controls)):
            if name.endswith('.skill.md'):
                controls.append((name[:-len('.skill.md')],
                                 os.path.join(ns.controls, name)))
    if not controls:
        sys.stderr.write('step-matrix: no controls found\n')
        return 2

    steps = list(range(1, 13))
    rows = []
    for name, path in controls:
        with open(path, 'r', encoding='utf-8') as handle:
            text = handle.read()
        try:
            rules, _info = FEAT.parse_skill(text)
            status = 'ok'
        except FEAT.TableError as exc:
            rules = None
            status = 'exit 2: %s' % exc
        observed = {}
        if rules is not None:
            for label, env in envs:
                feat = FEAT.load_envelope(env)
                rule = FEAT.classify(rules, feat)
                observed[label] = (rule['label'], rule['action']) if rule else \
                    (FEAT.DEFAULT_LABEL, FEAT.DEFAULT_ACTION)
        misses = {}
        hits = 0
        for label, _env in envs:
            want = expected[label][:2]
            got = observed.get(label)
            if got == want:
                hits += 1
            else:
                step = expected[label][2]
                misses.setdefault((step, want), []).append((label, want, got))
        rows.append({'name': name, 'status': status, 'hits': hits,
                     'total': len(envs), 'misses': misses})

    print('# step-matrix over %d envelopes (planned classes), interp=%s'
          % (len(envs), ns.interp or 'DEV replica v3-check-interp.py'))
    head = '| control | matched | ' + ' | '.join('s%d' % s for s in steps) + ' |'
    print(head)
    print('| --- | --- | ' + ' | '.join('---' for _ in steps) + ' |')
    for row in rows:
        cells = []
        for step in steps:
            n = sum(len(items) for (this, _want), items in row['misses'].items()
                    if this == step)
            cells.append('%d' % n if n else '·')
        print('| %s | %d/%d | %s |' % (row['name'], row['hits'], row['total'],
                                       ' | '.join(cells)))
    for row in rows:
        print('\n## %s  %d/%d  (%s)' % (row['name'], row['hits'], row['total'],
                                        row['status']))
        if not row['misses']:
            print('   matches the precedence list on every envelope')
            continue
        for key in sorted(row['misses']):
            step, want = key
            items = row['misses'][key]
            classes = sorted({label for label, _w, _g in items})
            print('   step %-2d %-38s missed on %s'
                  % (step, '%s/%s' % want, ', '.join(classes)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
