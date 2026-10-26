#!/usr/bin/env python3
"""avm-row-guard -- a SquashFS triage table may not key AVM diagnosis on the timestamp marker.

Measured basis (this seat, 2026-10-26; genuine AVM body = shokuknow round11 `avm-be.squashfs`,
sha256 c7f74691...d32d32, copied read-only into scratch):

  magic sqsh, mkfs_time 365 == bytes_used 365, metadata block lengths decode LITTLE-endian
  sasquatch-v4be  (no flag)  -> exit 0, 4 files
  sasquatch-v4be -be         -> exit 1, 0 files
  same bytes with mkfs_time normalised to 1700000000 (marker stripped):
  sasquatch-v4be  (no flag)  -> exit 0, 4 files
  sasquatch-v4be -be         -> exit 1, 0 files   <-- this is the shape unblob produces,
                                                    because the -be branch keys on the marker
  => the marker mispredicts BOTH ways; the discriminant is the metadata block-length endianness.

Round-39's SKILL table v1 (`<!-- sqfs-triage-table v1 -->`, SKILL.md:333-346) keys its only AVM
row on `mkfs_time == bytes_used` and prescribes a global `sasquatch-v4be` PATH wrapper that
appends `-be`; the same wrapper makes every genuine AVM-layout body (marker present -> unblob
correctly omits -be) fail. Its `body-extractor-failure` row then calls the marker-stripped
genuine-AVM shape "damaged" and forbids the one remedy that works (drop -be).

Checks on a table file:
  R1 a column expresses the metadata block-length endianness;
  R2 no row prescribes a `-be`-appending extractor wrapper without a scope cue;
  R3 no (squashfs_v4_be, extractor-failure, -be=yes) row attributes the failure to damage
     without naming the AVM/block-length alternative;
  R4 some (extractor-failure, -be=yes) row names the without--be remedy.
Exit 0 clean; 1 findings; 2 usage. Red on SKILL.md; green on table-v2-proposed.md.
"""
import argparse
import re
import sys

HEADER_KEYS = ('label', 'handler', 'gap', 'depend', 'block', 'be', 'symlink', 'published')
LAYOUT_RX = re.compile(r'(?i)(block[\s_-]*len|len[\s_-]*endian|metadata[^|]*endian|layout)')
SCOPE_CUES = ('only when', 'if and only if', 'only for', 'this class', 'this row',
              'scoped', 'remove it', 'never for')
NEG_BE_RX = re.compile(r'(?i)(without\s+`?-be|drop\s+`?-be|noflag|omit\s+`?-be|no\s+`?-be)')
DAMAGE_RX = re.compile(r'(?i)(damag|corrupt|truncat)')


def split_row(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def norm(value):
    return value.replace('`', '').strip()


def parse_table(path):
    lines = open(path, encoding='utf-8').read().splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip().startswith('|') and 'label' in line.lower() and 'handler' in line.lower():
            start = i
            break
    if start is None:
        raise SystemExit(f'USAGE {path}: no triage header row')
    header = [c.strip().lower() for c in split_row(lines[start])]
    rows = []
    for line in lines[start + 1:]:
        if not line.strip().startswith('|'):
            break
        cells = split_row(line)
        if set(''.join(cells)) <= set('-: '):
            continue
        if len(cells) != len(header):
            continue
        rows.append(dict(zip(header, cells)))
    return header, rows


def col(header, *needles):
    for name in header:
        if all(n in name for n in needles):
            return name
    return None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--table', required=True, help='SKILL.md or a control/table file')
    args = ap.parse_args(argv)
    header, rows = parse_table(args.table)

    findings = []
    layout_col = col(header, 'block') or col(header, 'len')
    if not layout_col:
        findings.append('R1 table has no metadata block-length endianness column; '
                        'the marker mispredicts in both directions')

    handler_c = col(header, 'handler')
    gaps_c = col(header, 'gap')
    be_c = next((n for n in header if '-be' in n or n.strip() == 'be' or 'be in' in n), None)
    action_c = col(header, 'cause') or col(header, 'action')
    label_c = col(header, 'label')

    for row in rows:
        label = row.get(label_c, '?')
        action = row.get(action_c, '')
        handler = norm(row.get(handler_c, ''))
        gaps = norm(row.get(gaps_c, ''))
        be = norm(row.get(be_c, ''))
        if 'wrapper' in action.lower() and '-be' in action:
            if not any(cue in action.lower() for cue in SCOPE_CUES):
                findings.append(f'R2 row "{label}" prescribes a -be-appending extractor wrapper '
                                f'without a scope cue; it would break every genuine AVM body')
        if ('squashfs_v4_be' in handler and 'extractor-failure' in gaps
                and be.strip().lower() in ('yes', 'true', '1')):
            if not LAYOUT_RX.search(action) and not LAYOUT_RX.search(handler + ' ' + gaps):
                if DAMAGE_RX.search(action):
                    findings.append(f'R3 row "{label}" (be handler, extractor-failure, -be=yes) '
                                    f'calls the failure damage without naming the AVM-layout / '
                                    f'block-length alternative')

    neg_rows = [r for r in rows
                if 'extractor-failure' in norm(r.get(gaps_c, ''))
                and norm(r.get(be_c, '')).lower() in ('yes', 'true', '1')
                and NEG_BE_RX.search(norm(r.get(action_c, '')))]
    if not neg_rows:
        findings.append('R4 no row names the without--be remedy for the '
                        '(extractor-failure, -be=yes) shape')

    print(f'table={args.table} columns={len(header)} rows={len(rows)} layout_col={layout_col!r}')
    for f in findings:
        print(f'FINDING {f}')
    print(f'findings={len(findings)}')
    return 0 if not findings else 1


if __name__ == '__main__':
    sys.exit(main())
