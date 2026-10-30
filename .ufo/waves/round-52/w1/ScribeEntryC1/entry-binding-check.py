#!/usr/bin/env python3
"""Entry-binding check for the R52-C1 knowledge-entry DRAFT (ScribeEntryC1).

Read-only over the DRAFT entry file and the committed lane bytes. It does NOT
score the claim: it checks the entry's shape, the reachability of the counter's
`sourced` documentation binding, and the placeholders the L1 must fill before
the freeze.

Checks (the counter's own names):
  entry_shape      the file opens with a title line, a `status:` line, at least
                   one `source:` line, a `verified-at:` line and a `recheck:`
                   line (the round-28 house shape)
  source_ids       the S-ids the `source:` lines name
  cited_rows       of those S-ids, which ones exist in corpus/SOURCES.md
  opened_in_window which of the cited rows have an `opened` date inside the
                   counter's window (the round-52 counter's OPENED_DATES)
  used_by_entry    which cited+opened rows list this entry (path or stem) in
                   their `used-by` cell — this is what makes `sourced` true
  placeholders     the `<PLACEHOLDER` markers still in the file

Exit: 0 no unresolved placeholder and at least one cited+opened+used-by row
      (the `sourced` binding is reachable),
      1 a placeholder or an unreachable `sourced` binding remains,
      2 an input could not be read.

Usage: python3 -I -B entry-binding-check.py --lane <LANE> --entry <FILE>
       [--opened-date YYYY-MM-DD ...]
"""
import argparse
import os
import re
import sys

SID_RE = re.compile(r'(?<![0-9A-Za-z])(S\d{3,})(?![0-9A-Za-z])')
ROW_RE = re.compile(r'^ {0,3}\|\s*(S\d{3,})\s*\|')
ENTRY_PATH = 'corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md'
ENTRY_STEM = '2026-10-30-r52-avm-le-squashfs-core'


def cells(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--entry', required=True)
    ap.add_argument('--opened-date', action='append', default=['2026-10-30'])
    args = ap.parse_args()
    try:
        with open(args.entry, encoding='utf-8') as fh:
            text = fh.read()
        with open(os.path.join(args.lane, 'corpus', 'SOURCES.md'),
                  encoding='utf-8') as fh:
            reg = fh.read()
    except Exception as exc:                                  # noqa: BLE001
        print('input unreadable: %s' % exc, file=sys.stderr)
        return 2

    lines = text.splitlines()
    shape = {
        'title': bool(lines) and lines[0].startswith('# '),
        'status': any(l.startswith('status:') for l in lines),
        'source': any(l.startswith('source:') for l in lines),
        'verified_at': any(l.startswith('verified-at:') for l in lines),
        'recheck': any(l.startswith('recheck:') for l in lines),
    }
    src_ids = set()
    for line in lines:
        if line.startswith('source:'):
            src_ids |= set(SID_RE.findall(line))

    rows = {}
    for line in reg.splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        c = cells(line)
        if len(c) != 11:
            continue
        rows[c[0]] = c

    cited = sorted(i for i in src_ids if i in rows)
    missing = sorted(i for i in src_ids if i not in rows)
    opened_ok = sorted(i for i in cited if rows[i][8] in tuple(args.opened_date))
    used_by = sorted(i for i in opened_ok
                     if ENTRY_PATH in rows[i][10] or ENTRY_STEM in rows[i][10])
    placeholders = [(i + 1, l.strip()[:90])
                    for i, l in enumerate(lines) if '<PLACEHOLDER' in l]

    print('entry_shape %r' % (shape,))
    print('source_ids %r' % (sorted(src_ids),))
    print('cited_rows %r missing_rows %r' % (cited, missing))
    print('opened_in_window %r' % (opened_ok,))
    print('used_by_entry %r' % (used_by,))
    print('sourced_reachable %r' % (bool(used_by),))
    print('placeholders %d' % len(placeholders))
    for ln, txt in placeholders:
        print('   line %d: %s' % (ln, txt))

    ok = all(shape.values()) and not placeholders and bool(used_by)
    print('VERDICT %s' % ('pass' if ok else 'needs-l1-fill'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
