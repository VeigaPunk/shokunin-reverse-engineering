#!/usr/bin/env python3
"""Pre-freeze self-check for the R40-C1 documentation bindings.

Mirrors the peer counter's constants and regexes (artifacts/R40C1Counter/c1-counter.py:174-203,
247-266) so the L1 can see a red binding before the freeze commit. This is a convenience: the
counter, not this script, decides the claim.

  python3 check-doc-bindings.py <lane-root>     # exit 0 all green, 1 any red
  python3 check-doc-bindings.py --selftest      # green fixture, then a red one that must fail
"""
import os
import re
import sys
import tempfile

ENTRY = 'corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md'
STEM = '2026-10-26-r40-avm-be-squashfs-core'
CORE_HEADING = '## Round-40 additions to Core'
FRONTIER_MARK = 'Round-40 frontier note'
HANDLER = 'squashfs_v4_be'
HANDLER_RE = re.compile(r'(?<![A-Za-z0-9_-])' + HANDLER + r'(?![A-Za-z0-9_-])')
AVM_LAYOUT_RE = re.compile(r'AVM[ _-]layout', re.IGNORECASE)
SID_RE = re.compile(r'(?<![0-9A-Za-z])(S\d{3,})(?![0-9A-Za-z])')
OPENED = '2026-10-26'


def read(root, rel):
    p = os.path.join(root, rel)
    try:
        with open(p, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except OSError:
        return None


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


def check(root):
    b = {}
    prov = read(root, 'PROVINCE.md') or ''
    sec = section(prov, CORE_HEADING)
    b['province_core_section'] = sec is not None
    rows = [l for l in (sec or []) if l.lstrip().startswith('|')]
    b['province_core_row'] = any(HANDLER_RE.search(cells(r)[0])
                                 and AVM_LAYOUT_RE.search(r) and ENTRY in r for r in rows)
    b['frontier_note'] = any(FRONTIER_MARK in l and STEM in l and AVM_LAYOUT_RE.search(l)
                             for l in prov.splitlines())
    ent = read(root, ENTRY)
    b['entry_present'] = ent is not None
    src_ids = set()
    for line in (ent or '').splitlines():
        if line.startswith('source:'):
            src_ids |= set(SID_RE.findall(line))
    b['entry_source_ids'] = sorted(src_ids)
    reg = read(root, 'corpus/SOURCES.md') or ''
    ok = []
    for line in reg.splitlines():
        if not re.match(r'^ {0,3}\|\s*S\d{3,}\s*\|', line):
            continue
        c = cells(line)
        if len(c) != 11:
            continue
        if c[0] in src_ids and c[8] == OPENED and (ENTRY in c[10] or STEM in c[10]):
            ok.append(c[0])
    b['opened_source_rows'] = sorted(ok)
    b['sourced'] = bool(ok)
    readme = read(root, 'corpus/README.md') or ''
    cm = section(readme, '## Coverage map')
    b['coverage_map_row'] = bool(cm) and any(
        STEM in l for l in cm if l.lstrip().startswith('|'))
    return b


GREEN = {
    'PROVINCE.md': (
        '# P\n\n'
        + CORE_HEADING + '\n\n'
        '| capability | evidence |\n|---|---|\n'
        '| standard AVM-layout big-endian SquashFS v4 (`squashfs_v4_be`) | **Core** — entry '
        + ENTRY + ' |\n\n'
        'Round-40 frontier note, 2026-10-26: the AVM clause is superseded; a genuine AVM-layout '
        'image is Core (`' + STEM + '`).\n'),
    ENTRY: 'source: S777 — fixture row\nverified-at: 2026-10-26\n',
    'corpus/SOURCES.md': (
        '# R\n\n| id | source | kind | tier | scope | anchor | teaches | status | opened | '
        'recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n'
        '| S777 | fixture | docs | A | s | a | t | mined | ' + OPENED + ' | 180d | ' + ENTRY + ' |\n'),
    'corpus/README.md': '# R\n\n## Coverage map\n\n| x | y |\n|---|---|\n| a | `' + STEM + '` |\n',
}


def materialise(root, files):
    for rel, body in files.items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(body)


def selftest():
    with tempfile.TemporaryDirectory() as d:
        materialise(d, GREEN)
        green = check(d)
        assert all(v is True for k, v in green.items() if k not in
                   ('province_core_rows_seen', 'entry_source_ids', 'opened_source_rows')), green
        red_files = dict(GREEN)
        red_files['PROVINCE.md'] = '\n'.join(
            l for l in GREEN['PROVINCE.md'].splitlines() if not l.startswith(FRONTIER_MARK)) + '\n'
        with tempfile.TemporaryDirectory() as d2:
            materialise(d2, red_files)
            red = check(d2)
            if red['frontier_note'] is not False:
                print('SELFTEST FAIL: the red fixture still passes frontier_note')
                return 1
        # second red case: a SOURCES row with 12 cells must not satisfy `sourced`
        bad_row = ('# R\n\n| id | source | kind | tier | scope | anchor | teaches | status | opened | '
                   'recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n'
                   '| S777 | fixture | docs | A | s | a | t | mined | ' + OPENED + ' | 180d | '
                   + ENTRY + ' | extra |\n')
        with tempfile.TemporaryDirectory() as d3:
            f = dict(GREEN)
            f['corpus/SOURCES.md'] = bad_row
            materialise(d3, f)
            if check(d3)['sourced'] is not False:
                print('SELFTEST FAIL: a 12-cell row still satisfies sourced')
                return 1
        # third red case: the frontier note wrapped over two physical lines must fail
        with tempfile.TemporaryDirectory() as d4:
            f = dict(GREEN)
            f['PROVINCE.md'] = GREEN['PROVINCE.md'].replace(
                'superseded; a genuine AVM-layout image is Core',
                'superseded; a genuine AVM-layout\nimage is Core')
            materialise(d4, f)
            if check(d4)['frontier_note'] is not False:
                print('SELFTEST FAIL: a wrapped frontier note still satisfies frontier_note')
                return 1
        print('SELFTEST OK: green passes; missing note, wrapped note and 12-cell row each fail')
        return 0


def main(argv):
    if len(argv) == 2 and argv[1] == '--selftest':
        return selftest()
    if len(argv) != 2:
        print(__doc__)
        return 2
    b = check(os.path.abspath(argv[1]))
    red = []
    for k, v in b.items():
        if isinstance(v, bool):
            print(f'{k}\t{"OK" if v else "RED"}')
            if not v:
                red.append(k)
        else:
            print(f'{k}\t{v}')
    return 0 if not red else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
