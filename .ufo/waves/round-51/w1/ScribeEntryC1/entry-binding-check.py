#!/usr/bin/env python3
"""Entry-binding check for the R51-C1 knowledge entry (ScribeEntryC1, wave 1).

Re-implements, read-only, the counter's own documentation-binding logic over a
DRAFT entry file, so the L1 can see which bindings the draft satisfies and which
it cannot, before the freeze. It does NOT score the claim: it checks shape and
citation reachability only.

Bindings checked (the counter's own names):
  entry_shape        the file opens with a title line, a `status:` line, at least
                     one `source:` line, a `verified-at:` line and a `recheck:`
                     line (the round-28 house shape)
  source_ids         the S-ids the `source:` lines name
  cited_rows         of those S-ids, which ones exist in corpus/SOURCES.md
  opened_in_window   which of the cited rows have an `opened` date inside the
                     counter's window (the window is a counter constant; the
                     round-50 counter used ('2026-10-28', '2026-10-29'))
  used_by_entry      which cited+opened rows list this entry (path or stem) in
                     their `used-by` cell — this is what makes `sourced` true
  placeholders       the `<PLACEHOLDER` markers still in the file (each is
                     something the L1 must fill before the freeze)

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


def cells(line):
    # the counter strips every cell: `tools/round-50/c1-counter.py:585-586`
    return [c.strip() for c in line.strip().strip('|').split('|')]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--entry', required=True)
    ap.add_argument('--opened-date', action='append', default=[],
                    help='an `opened` date inside the counter window (repeatable)')
    ap.add_argument('--entry-path', default=None,
                    help='the entry path the SOURCES used-by cell must name')
    args = ap.parse_args()
    window = tuple(args.opened_date) or ('2026-10-28', '2026-10-29')
    try:
        with open(args.entry, encoding='utf-8') as fh:
            text = fh.read()
        with open(os.path.join(args.lane, 'corpus', 'SOURCES.md'),
                  encoding='utf-8') as fh:
            registry = fh.read()
    except Exception as exc:                                  # noqa: BLE001
        print('input unreadable: %s' % exc, file=sys.stderr)
        return 2

    lines = text.splitlines()
    src_lines = [l for l in lines if l.startswith('source:')]
    ids = set()
    for l in src_lines:
        ids |= set(SID_RE.findall(l))

    have = {
        'title': bool(lines) and lines[0].startswith('# '),
        'status': any(l.startswith('status:') for l in lines),
        'source': bool(src_lines),
        'verified_at': any(l.startswith('verified-at:') for l in lines),
        'recheck': any(l.startswith('recheck:') for l in lines),
    }
    print('entry_shape %s %r' % (all(have.values()), have))
    print('source_ids %s' % sorted(ids))

    rows = {}
    for line in registry.splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        c = cells(line)
        if len(c) != 11:
            continue
        rows[c[0]] = c
    print('cited_rows %s' % sorted(i for i in ids if i in rows))
    missing = sorted(i for i in ids if i not in rows)
    if missing:
        print('cited_rows_absent_from_registry %s' % missing)

    opened = sorted(i for i in ids if i in rows and rows[i][8] in window)
    print('opened_in_window %s (window %r)' % (opened, window))
    not_opened = sorted(i for i in ids if i in rows and rows[i][8] not in window)
    if not_opened:
        print('cited_rows_outside_window %s (opened %r)'
              % (not_opened, {i: rows[i][8] for i in not_opened}))

    entry_path = args.entry_path
    stem = None
    if entry_path:
        stem = os.path.splitext(os.path.basename(entry_path))[0]
    used_by = []
    for i in opened:
        used = rows[i][10]
        if (entry_path and entry_path in used) or (stem and stem in used):
            used_by.append(i)
    print('used_by_entry %s' % sorted(used_by))
    print('sourced_reachable %s' % bool(used_by))

    ph = text.count('<PLACEHOLDER')
    print('placeholders %d' % ph)
    if ph:
        for n, l in enumerate(lines, 1):
            if '<PLACEHOLDER' in l:
                print('  line %d: %s' % (n, l.strip()[:160]))
    ok = bool(used_by) and ph == 0
    print('verdict %s' % ('pass' if ok else 'needs-l1-fill'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
