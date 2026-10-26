#!/usr/bin/env python3
"""diff-controls.py - cell-level deltas between control tables (calibration).

Prints, for a pair of control documents, every row present in one and absent from the
other, and every differing cell of a shared row.  Used to state the minimum edit that
turns the best shortcut into the reference row set.

Usage: diff-controls.py LEFT.skill.md RIGHT.skill.md [--markdown]
"""

import argparse
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    'v3checkinterp', os.path.join(HERE, 'v3-check-interp.py'))
FEAT = importlib.util.module_from_spec(spec)
spec.loader.exec_module(FEAT)

COLUMNS = ['label', 'operation', 'provider', 'handler', 'gap kinds', 'dependencies',
           '-be', 'symlink removed', 'published files', 'action', 'cause', 'source']


def rows(path):
    with open(path, 'r', encoding='utf-8') as handle:
        text = handle.read()
    lines = text.splitlines()
    start, end = FEAT.craft_bounds(lines)
    marker = [i for i in range(start, end) if FEAT.MARKER in lines[i]]
    if not marker:
        raise SystemExit('%s: no v3 marker' % path)
    first = next(i for i in range(marker[0] + 1, end)
                 if lines[i].lstrip().startswith('|'))
    out = []
    while first < end and lines[first].lstrip().startswith('|'):
        cells = [FEAT.clean_cell(c) for c in FEAT.split_row(lines[first])]
        if len(cells) == len(COLUMNS) and cells[0] != 'label' \
                and not all(set(c) <= set('-: ') for c in cells):
            out.append(cells)
        first += 1
    return out


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('left')
    ap.add_argument('right')
    ap.add_argument('--markdown', action='store_true')
    ns = ap.parse_args(argv)
    left = {row[0]: row for row in rows(ns.left)}
    right = {row[0]: row for row in rows(ns.right)}
    lname = os.path.basename(ns.left)
    rname = os.path.basename(ns.right)
    print('left : %s (%d rows)' % (lname, len(left)))
    print('right: %s (%d rows)' % (rname, len(right)))
    only_left = [label for label in left if label not in right]
    only_right = [label for label in right if label not in left]
    print('rows only in left : %s' % (', '.join(only_left) or '-'))
    print('rows only in right: %s' % (', '.join(only_right) or '-'))
    shared = [label for label in left if label in right]
    order_left = [label for label in left]
    order_right = [label for label in right]
    shared_l = [label for label in order_left if label in shared]
    shared_r = [label for label in order_right if label in shared]
    if shared_l != shared_r:
        print('shared-row ORDER differs: %s vs %s' % (shared_l, shared_r))
    edits = 0
    for label in shared:
        diffs = []
        for idx, column in enumerate(COLUMNS):
            if left[label][idx] != right[label][idx]:
                diffs.append((column, left[label][idx], right[label][idx]))
        if diffs:
            print('\nrow %s' % label)
            for column, want, got in diffs:
                print('  %-16s %-40s -> %s' % (column, want[:40], got[:40]))
            edits += len(diffs)
    print('\ncell edits between shared rows: %d' % edits)
    if ns.markdown:
        print('\n| row | column | left | right |')
        print('| --- | --- | --- | --- |')
        for label in shared:
            for idx, column in enumerate(COLUMNS):
                if left[label][idx] != right[label][idx]:
                    print('| %s | %s | `%s` | `%s` |'
                          % (label, column, left[label][idx], right[label][idx]))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
