#!/usr/bin/env python3
"""Extract the v4 SquashFS triage-table region of one SKILL.md, for `cmp`.

Two extraction rules, both scoped to the `## Queue-drain craft` section:

  table      the region the round-43 claim P43-C1 freezes: from the line
             containing the v4 marker through the end of the FIRST markdown
             table after it.  This mirrors the documented rule of the frozen
             interpreter tools/round-42/sqfs-triage-v4.py ("it takes the FIRST
             markdown table that follows a line containing the marker ...
             plus the closed action vocabulary declared by the line directly
             above that table").

  ruleblock  the region tools/round-42/c2-counter.py `rule_block()` compares
             in its `v4_block_identical` binding: the marker line through the
             next `- **` bullet, ATX heading, or `<!-- sqfs-triage-table ...`
             marker.

Usage: region-extract.py --skill SKILL.md [--mode table|ruleblock]
                       [--marker '<!-- sqfs-triage-table v4 -->']
Region bytes go to stdout, nothing is written to disk.
"""

import argparse
import re
import sys

CRAFT_HEADING = '## Queue-drain craft'
DEFAULT_MARKER = '<!-- sqfs-triage-table v4 -->'


def craft_span(lines):
    start = next((i for i, l in enumerate(lines)
                  if l.lower().startswith(CRAFT_HEADING.lower())), None)
    if start is None:
        raise SystemExit('no %r heading' % CRAFT_HEADING)
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith('## '):
            end = i
            break
    return start, end


def table_region(lines, marker):
    start, end = craft_span(lines)
    mi = next((i for i in range(start, end) if marker in lines[i]), None)
    if mi is None:
        raise SystemExit('marker %r absent from the craft section' % marker)
    ts = next((i for i in range(mi + 1, end) if lines[i].lstrip().startswith('|')), None)
    if ts is None:
        raise SystemExit('no markdown table after the marker')
    te = ts
    while te + 1 < end and lines[te + 1].lstrip().startswith('|'):
        te += 1
    return lines[mi:te + 1]


def ruleblock_region(lines, marker):
    """tools/round-42/c2-counter.py rule_block(), transcribed."""
    start, end = craft_span(lines)
    mi = next((i for i in range(start + 1, end)
               if lines[i].strip().startswith(marker)), None)
    if mi is None:
        mi = next((i for i in range(start + 1, end) if marker in lines[i]
                   and not re.match(r'^\s*-\s+\*\*', lines[i])
                   and not lines[i].lstrip().startswith('#')), None)
    if mi is None:
        raise SystemExit('marker %r absent from the craft section' % marker)
    stop = end
    for i in range(mi + 1, end):
        l = lines[i]
        if re.match(r'^#{1,4} ', l) or re.match(r'^\s*-\s+\*\*', l) \
                or l.strip().startswith('<!-- sqfs-triage-table'):
            stop = i
            break
    return lines[mi:stop]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--skill', required=True)
    ap.add_argument('--mode', choices=('table', 'ruleblock'), default='table')
    ap.add_argument('--marker', default=DEFAULT_MARKER)
    ns = ap.parse_args(argv)
    with open(ns.skill, encoding='utf-8') as fh:
        lines = fh.read().splitlines()
    region = (table_region if ns.mode == 'table' else ruleblock_region)(lines, ns.marker)
    sys.stdout.write('\n'.join(region) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
