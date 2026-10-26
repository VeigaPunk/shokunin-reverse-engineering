#!/usr/bin/env python3
"""Rebuild the SKILL.md variants this seat scored, from the lane's SKILL.md.

  mk-variants.py --root <lane> --work <dir>

Writes into --work (default $TMPDIR or a mkdtemp):
  sk-min7.md          block 18's table replaced by the 7-cell shortcut table (artifacts/min7-table.md)
  sk-two-tables.md    block 18 unchanged + a block 19 carrying <!-- sqfs-triage-table v2 --> before the next H2
  sk-single-table.md  block 18's table bytes replaced by a pointer to the round-39 knowledge entry
Never writes outside --work.
"""
import argparse
import os
import tempfile


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True, help='lane root holding SKILL.md')
    ap.add_argument('--work', default=None)
    ap.add_argument('--table', default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                    'min7-table.md'))
    ns = ap.parse_args()
    work = ns.work or os.environ.get('TMPDIR') or tempfile.mkdtemp(prefix='r40c2-variants.')
    os.makedirs(work, exist_ok=True)
    src = open(os.path.join(ns.root, 'SKILL.md'), encoding='utf-8').read().splitlines()

    craft = next(i for i, l in enumerate(src) if l.startswith('## Queue-drain craft'))
    nxt = next(i for i in range(craft + 1, len(src)) if src[i].startswith('## '))
    marker = next(i for i, l in enumerate(src) if '<!-- sqfs-triage-table v1 -->' in l)
    j = marker + 1
    while not src[j].lstrip().startswith('|'):
        j += 1
    k = j
    while src[k].lstrip().startswith('|'):
        k += 1

    table = [l.rstrip('\n') for l in open(ns.table, encoding='utf-8')]
    # min7-table.md is marker + header + separator + 8 rows; splice only the rows
    rows = [l for l in table if l.lstrip().startswith('|')]
    open(os.path.join(work, 'sk-min7.md'), 'w', encoding='utf-8').write(
        '\n'.join(src[:j] + rows + src[k:]) + '\n')

    v2 = ['', '- **SquashFS outcome triage v2 (round 40).** draft block 19.',
          '', '  <!-- sqfs-triage-table v2 -->',
          '  | label | operation | provider | handler | gap kinds | dependencies | -be in child argv '
          '| symlink removed | published files | action | cause | source |',
          '  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |',
          '  | mixed-symlinks | `extract_firmware` | `unblob` | `squashfs_v4_*` | '
          '`unpublished-entry` | `*` | `n/a` | `yes` | `>0` | count-gaps | both kinds -> keep link '
          'absent | x |']
    open(os.path.join(work, 'sk-two-tables.md'), 'w', encoding='utf-8').write(
        '\n'.join(src[:nxt] + v2 + src[nxt:]) + '\n')

    ptr = ['', '  Table v1 moved to `corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md`; '
               'the live table is block 19.', '']
    open(os.path.join(work, 'sk-single-table.md'), 'w', encoding='utf-8').write(
        '\n'.join(src[:marker] + ptr + src[k:]) + '\n')

    print('work=%s' % work)
    for name in ('sk-min7.md', 'sk-two-tables.md', 'sk-single-table.md'):
        p = os.path.join(work, name)
        print('%s %d B' % (p, os.path.getsize(p)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
