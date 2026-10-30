#!/usr/bin/env python3
"""Read-only check of a DRAFT PROVINCE section against the round-50 counter's own
documentation-binding logic, re-used verbatim for the round-52 constants.

Usage: python3 -I -B binding-check.py --lane <LANE> --draft <draft.md> [--branch A|B]

Exit 0: every binding has the expected value for that branch.
Exit 1: a binding has the wrong value (or a draft block could not be parsed).
Exit 2: an input is missing (could-not-evaluate).

The functions `section`, `cells` and the three regexes are copied byte-for-byte from
tools/round-50/c1-counter.py (receipts `counter-binding-code`, `counter-binding-consts`);
only the round-52 constants differ.
"""
import argparse, os, re, sys

ENTRY = 'corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md'
STEM = '2026-10-30-r52-avm-le-squashfs-core'
CORE_HEADING = '## Round-52 additions to Core'
FRONTIER_MARK = 'Round-52 frontier note'
HANDLER = 'squashfs_v4_le'
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


def fenced_blocks(text):
    """Return the ```markdown fenced blocks of a draft file, in order."""
    out, cur, inside = [], [], False
    for line in text.splitlines():
        if line.startswith('```'):
            if inside:
                out.append('\n'.join(cur))
                cur, inside = [], False
            else:
                inside = True
            continue
        if inside:
            cur.append(line)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--draft', required=True)
    ap.add_argument('--branch', default='A', choices=['A', 'B'])
    a = ap.parse_args()
    prov_path = os.path.join(a.lane, 'PROVINCE.md')
    if not os.path.exists(prov_path):
        print('missing PROVINCE.md', file=sys.stderr)
        return 2
    prov = open(prov_path, encoding='utf-8').read()
    draft = open(a.draft, encoding='utf-8').read()
    blocks = fenced_blocks(draft)
    if len(blocks) < 2:
        print('draft has fewer than two fenced blocks', file=sys.stderr)
        return 2
    branch_a = blocks[0]
    branch_b = blocks[1]
    block = branch_a if a.branch == 'A' else branch_b

    # the branch blocks are appended to the real PROVINCE.md text
    text = prov.rstrip('\n') + '\n\n' + block + '\n'
    sec = section(text, CORE_HEADING)
    b = {}
    b['province_core_section'] = sec is not None
    rows = [l for l in (sec or []) if l.lstrip().startswith('|')]
    b['province_core_row'] = any(
        HANDLER_RE.search(cells(r)[0]) and AVM_MARKER_RE.search(r.replace(ENTRY, ''))
        and ENTRY in r
        for r in rows)
    b['frontier_note'] = any(FRONTIER_MARK in l and STEM in l
                             and LE_AVM_RE.search(l.replace(STEM, ''))
                             for l in text.splitlines())
    b['heading_occurrences'] = text.splitlines().count(CORE_HEADING)
    b['placeholders_in_block'] = block.count('<PLACEHOLDER')
    want = {'A': {'province_core_section': True, 'province_core_row': True,
                  'frontier_note': True},
            'B': {'province_core_section': False, 'province_core_row': False,
                  'frontier_note': True}}[a.branch]
    ok = True
    for k, v in want.items():
        got = b[k]
        flag = 'ok ' if got == v else 'FAIL'
        if got != v:
            ok = False
        print(f'{flag} {k}: got {got} want {v}')
    want_headings = 1 if a.branch == 'A' else 0
    if b['heading_occurrences'] != want_headings:
        print('FAIL heading_occurrences: got', b['heading_occurrences'],
              'want', want_headings)
        ok = False
    else:
        print('ok  heading_occurrences:', want_headings)
    print(f'info placeholders in the branch block: {b["placeholders_in_block"]}')
    # the two branches must not both carry the Core heading
    other = branch_b if a.branch == 'A' else branch_a
    print('info other branch contains the Core heading:',
          CORE_HEADING in other)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
