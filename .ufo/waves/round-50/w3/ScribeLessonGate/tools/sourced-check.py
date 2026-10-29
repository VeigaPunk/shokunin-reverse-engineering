#!/usr/bin/env python3
"""sourced-check.py — offline replica of the frozen counter's `sourced` binding.

Seat ScribeLessonGate, wave 3, round-50 attempt 2.

The frozen counter `tools/round-50/c1-counter.py` (bytes frozen at
435d41fd4ad9211d1579fc447936fb33d2b74467) computes the `sourced` binding like
this (lines 2466-2478 of the frozen file):

    src_ids = set()
    if ent:
        for line in ent.decode(...).splitlines():
            if line.startswith('source:'):
                src_ids |= sid_tokens(line)
    reg = show(root, rev, 'corpus/SOURCES.md')
    ok_ids = []
    if reg:
        for line in reg.decode(...).splitlines():
            if not re.match(r'^ {0,3}\|\s*S\d{3,}\s*\|', line):
                continue
            c = cells(line)
            if len(c) != 11:
                continue
            used = c[10]
            if c[0] in src_ids and c[8] in OPENED_DATES and (ENTRY in used or STEM in used):
                ok_ids.append(c[0])
    b['opened_source_rows'] = sorted(ok_ids)
    b['sourced'] = bool(ok_ids)

This script reproduces that predicate on plain files (no git, no REA, no
network) so that the binding can be checked against a candidate landing tree
before the L1 lands it.  It is a REPLICA, not the counter: the counter's own
verdict still comes from `tools/round-50/c1-counter.py` at the landing REV.

Usage:
    python3 -I -B sourced-check.py --registry <SOURCES.md> --entry <entry.md> \
        [--entry-const <path>] [--stem-const <stem>]

Exit codes (lane semantics):
    0  `sourced` would be true (at least one opened source row lists the entry)
    1  `sourced` would be false
    2  could not evaluate (missing file / bad arguments)
"""

from __future__ import annotations

import argparse
import re
import sys

# The frozen constants (tools/round-50/c1-counter.py lines 377-393).
DEFAULT_ENTRY = 'corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md'
DEFAULT_STEM = '2026-10-28-r50-avm-le-squashfs-core'
OPENED_DATES = ('2026-10-28', '2026-10-29')
SID_RE = re.compile(r'(?<![0-9A-Za-z])(S\d{3,})(?![0-9A-Za-z])')
ROW_RE = re.compile(r'^ {0,3}\|\s*S\d{3,}\s*\|')


def cells(row: str) -> "list[str]":
    return [c.strip() for c in row.strip().strip('|').split('|')]


def main(argv: "list[str]") -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--registry', required=True)
    ap.add_argument('--entry', required=True)
    ap.add_argument('--entry-const', default=DEFAULT_ENTRY)
    ap.add_argument('--stem-const', default=DEFAULT_STEM)
    args = ap.parse_args(argv)

    try:
        reg = open(args.registry, encoding='utf8').read()
        ent = open(args.entry, encoding='utf8').read()
    except OSError as exc:
        print('cannot read input: %s' % exc, file=sys.stderr)
        return 2

    src_ids: "set[str]" = set()
    for line in ent.splitlines():
        if line.startswith('source:'):
            src_ids |= set(SID_RE.findall(line))

    ok_ids: "list[str]" = []
    near: "list[str]" = []
    for line in reg.splitlines():
        if not ROW_RE.match(line):
            continue
        c = cells(line)
        if len(c) != 11:
            continue
        used = c[10]
        if c[0] in src_ids and c[8] in OPENED_DATES:
            if args.entry_const in used or args.stem_const in used:
                ok_ids.append(c[0])
            else:
                near.append('%s (used-by names neither the frozen entry nor the frozen stem)' % c[0])

    print('entry_source_ids=%s' % ','.join(sorted(src_ids)))
    print('opened_source_rows=%s' % ','.join(sorted(ok_ids)))
    for n in near:
        print('NEAR-MISS\t%s' % n)
    print('sourced=%s' % bool(ok_ids))
    return 0 if ok_ids else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
