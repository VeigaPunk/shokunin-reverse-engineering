#!/usr/bin/env python3
"""Offline self-check of the drafted PROVINCE.md bindings for R51-C1.

Port of the documentation-binding predicates of the frozen round-50 counter
(`tools/round-50/c1-counter.py`, lines 2443-2492) with the round-51 constants
named in `plans/round-51-claims.md` (entry stem `2026-10-30-r51-avm-le-squashfs-core`,
core_heading `## Round-51 additions to Core`, frontier_mark `Round-51 frontier note`).

No REA, no network: this reads a candidate PROVINCE.md text file and reports which
bindings the counter's own predicates would find.  Exit 0 = every binding true.

Usage: python3 -I -B binding-selfcheck.py --province <candidate file> [--json-out <path>]
"""
import argparse
import json
import re
import sys

# --- constants: the round-50 counter's, with the round-51 values -----------------
HANDLER = 'squashfs_v4_le'
STEM = '2026-10-30-r51-avm-le-squashfs-core'
ENTRY = 'corpus/knowledge/%s.md' % STEM
CORE_HEADING = '## Round-51 additions to Core'
FRONTIER_MARK = 'Round-51 frontier note'
OPENED_DATES = ('2026-10-30',)

HANDLER_RE = re.compile(r'(?<![A-Za-z0-9_-])' + HANDLER + r'(?![A-Za-z0-9_-])')
AVM_MARKER_RE = re.compile(r'AVM[ _-]marker', re.IGNORECASE)
LE_AVM_RE = re.compile(r'\bLE[ _-]AVM\b|\bAVM[ _-]LE\b', re.IGNORECASE)


def section(text, heading):
    lines = text.splitlines()
    try:
        i = lines.index(heading)
    except ValueError:
        return None
    out = []
    for line in lines[i + 1:]:
        if line.startswith('## '):
            break
        out.append(line)
    return out


def cells(row):
    return [c.strip() for c in row.strip().strip('|').split('|')]


def check(prov_text):
    b = {}
    sec = section(prov_text, CORE_HEADING)
    b['province_core_section'] = sec is not None
    rows = [l for l in (sec or []) if l.lstrip().startswith('|')]
    b['province_core_row'] = any(
        HANDLER_RE.search(cells(r)[0]) and AVM_MARKER_RE.search(r.replace(ENTRY, ''))
        and ENTRY in r
        for r in rows)
    b['province_core_rows_seen'] = [
        cells(r)[0] for r in rows if HANDLER_RE.search(cells(r)[0])]
    b['frontier_note'] = any(FRONTIER_MARK in l and STEM in l
                             and LE_AVM_RE.search(l.replace(STEM, ''))
                             for l in prov_text.splitlines())
    b['frontier_note_lines'] = [
        l for l in prov_text.splitlines()
        if FRONTIER_MARK in l and STEM in l]
    return b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--province', required=True)
    ap.add_argument('--json-out')
    a = ap.parse_args()
    text = open(a.province, encoding='utf-8').read()
    b = check(text)
    res = {'candidate': a.province, 'stem': STEM, 'entry': ENTRY,
           'core_heading': CORE_HEADING, 'frontier_mark': FRONTIER_MARK,
           'bindings': {k: b[k] for k in ('province_core_section', 'province_core_row',
                                          'frontier_note')},
           'province_core_rows_seen': b['province_core_rows_seen'],
           'frontier_note_lines': b['frontier_note_lines']}
    ok = all(res['bindings'].values())
    res['all_bindings_true'] = ok
    out = json.dumps(res, indent=2, ensure_ascii=False)
    if a.json_out:
        with open(a.json_out, 'w', encoding='utf-8') as fh:
            fh.write(out + '\n')
    print(out)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
