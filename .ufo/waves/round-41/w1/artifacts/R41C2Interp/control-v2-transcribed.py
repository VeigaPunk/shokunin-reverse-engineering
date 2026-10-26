#!/usr/bin/env python3
"""control-v2-transcribed.py - build the claims' "v2 table transcribed into v3 grammar" control.

The round-41 C2 kill rule names six control tables.  Two of them are pure grammar
experiments that need no new rows, and this script builds the first: it lifts the frozen
round-40 v2 table out of ``tools/round-40/sqfs-triage-v2.py`` (read through ``git show`` at
a named rev), rewrites ONLY the marker to v3 and re-emits it inside a mini SKILL document,
so ``check-precedence.py --table <output>`` scores the transcribed v2 table against the
round-41 precedence text.  The comparison is the control: if a v2-shaped table already
agrees, the contains form and the new row earn nothing.

It writes one file (the transcribed table) and prints its path.  Usage:

  python3 -I -B control-v2-transcribed.py --rev <rev> --out <path.md>
                                          [--lane DIR] [--path tools/round-40/sqfs-triage-v2.py]
"""

import argparse
import os
import re
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
SOURCE_PATH = 'tools/round-40/sqfs-triage-v2.py'
V2_MARKER = '<!-- sqfs-triage-table v2 -->'
V3_MARKER = '<!-- sqfs-triage-table v3 -->'

SKELETON = ('# SKILL (control: the frozen v2 table transcribed into v3 grammar)\n\n'
            '## Queue-drain craft\n\n'
            'Control table lifted verbatim from %s at %s; only the marker changed.\n\n'
            '%s\n'
            '## A later section\n')


def extract_block(text):
    match = re.search(r'^TABLE_BLOCK = """\\\n(.*?)^"""$', text, re.S | re.M)
    if match is None:
        raise SystemExit('no TABLE_BLOCK literal in the source')
    block = match.group(1)
    if V2_MARKER not in block:
        raise SystemExit('the extracted block carries no v2 marker')
    return block.replace(V2_MARKER, V3_MARKER)


def main(argv=None):
    parser = argparse.ArgumentParser(prog='control-v2-transcribed.py')
    parser.add_argument('--rev', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--lane', default=LANE)
    parser.add_argument('--path', default=SOURCE_PATH)
    ns = parser.parse_args(argv)
    shown = subprocess.run(['git', '-C', ns.lane, 'show', '%s:%s' % (ns.rev, ns.path)],
                           capture_output=True, text=True)
    if shown.returncode != 0:
        raise SystemExit('git show failed: %s' % shown.stderr.strip())
    block = extract_block(shown.stdout)
    with open(ns.out, 'w', encoding='utf-8') as handle:
        handle.write(SKELETON % (ns.path, ns.rev, block))
    rows = sum(1 for line in block.splitlines() if line.startswith('|'))
    print('%s  (rows incl. header+separator: %d)' % (ns.out, rows))
    return 0


if __name__ == '__main__':
    sys.exit(main())
