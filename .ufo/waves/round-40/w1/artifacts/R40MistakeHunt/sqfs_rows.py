#!/usr/bin/env python3
"""sqfs_rows -- minimal independent reader for a SquashFS triage table plus REA envelopes.

Shared by check-domain-guard.py, check-mixed-symlinks.py and the table row checks. It is a
second implementation on purpose: the frozen `tools/round-39/sqfs-triage.py` cannot parse a
table with the extra `operation`/`provider`/`block-length endianness` columns v2 needs, so a
green case for those columns cannot be demonstrated through it.

Table grammar: header row starting with `|`, columns recognised by name, first matching row
wins, no match is `unclassified`.
 - `*` any; `none` empty; `n/a` not applicable (for the -be / block-length cells);
 - gaps/dependencies exact set equality unless `*`;
 - published files `>0`, `0` or `*`;
 - handler `none` (no chunk), `*`, or an fnmatch glob;
 - operation/provider exact (case-insensitive) unless `*`.
"""
import fnmatch
import json
import sys

MISSING = object()


def split_row(line):
    return [c.replace('`', '').strip() for c in line.strip().strip('|').split('|')]


def parse_table(path):
    lines = open(path, encoding='utf-8').read().splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.lstrip().startswith('|') and 'label' in line.lower() and 'handler' in line.lower():
            start = i
            break
    if start is None:
        raise SystemExit(f'no triage header row in {path}')
    header = [c.strip().lower() for c in split_row(lines[start])]
    rows = []
    for line in lines[start + 1:]:
        if not line.lstrip().startswith('|'):
            break
        cells = split_row(line)
        if set(''.join(cells)) <= set('-: '):
            continue
        if len(cells) != len(header):
            continue
        rows.append(dict(zip(header, cells)))
    return header, rows


def column(header, *needles):
    for name in header:
        if all(n in name for n in needles):
            return name
    return None


def envelope(path):
    obj = json.load(open(path, encoding='utf-8'))
    if isinstance(obj.get('data'), dict) and 'operation' in obj['data']:
        obj = obj['data']
    return obj


def _walk_commands(obj, out):
    if isinstance(obj, dict):
        cmd = obj.get('command')
        if isinstance(cmd, str):
            out.append(cmd)
        for value in obj.values():
            _walk_commands(value, out)
    elif isinstance(obj, list):
        for value in obj:
            _walk_commands(value, out)


def features(obj):
    nr = obj.get('normalized_result') or {}
    handlers = {c.get('handler') for c in (nr.get('chunks') or []) if isinstance(c, dict) and c.get('handler')}
    gaps = [g for g in (nr.get('extraction_gaps') or []) if isinstance(g, dict)]
    deps = set()
    for gap in gaps:
        for dep in gap.get('dependencies') or []:
            deps.add(dep)
    sr = 'no'
    for diag in (nr.get('diagnostics') or []):
        if isinstance(diag, dict) and 'MaliciousSymlinkRemoved' in str(diag.get('report') or diag):
            sr = 'yes'
    commands = []
    _walk_commands(obj.get('normalized_result') or {}, commands)
    _walk_commands(obj.get('raw_result') or {}, commands)
    sas = [c for c in commands if 'sasquatch' in c]
    tokens = [t for c in sas for t in c.split()]
    be = 'yes' if '-be' in tokens else ('no' if sas else 'n/a')
    return {
        'operation': (obj.get('operation') or '').lower(),
        'provider': ((obj.get('provider') or {}).get('id') or '').lower(),
        'H': handlers,
        'G': {g.get('kind') for g in gaps if g.get('kind')},
        'D': deps,
        'BE': be,
        'SR': sr,
        'P': len(nr.get('files') or []),
    }


def match(row, header, feat, len_endian=MISSING):
    def get(*needles):
        name = column(header, *needles)
        return row.get(name) if name else None

    op = get('operation')
    provider = get('provider')
    handler = get('handler')
    gaps = get('gap')
    deps = get('depend')
    block = get('block') or get('len')
    be = next((row[n] for n in header if '-be' in n or n.strip() == 'be' or 'be in' in n), None)
    sr = get('symlink')
    files = get('published')

    if op is not None and op != '*' and op.lower() != feat['operation']:
        return False
    if provider is not None and provider != '*' and provider.lower() != feat['provider']:
        return False
    if handler is not None:
        if handler == 'none':
            if feat['H']:
                return False
        elif handler != '*':
            if not feat['H'] or not all(fnmatch.fnmatch(h, handler) for h in feat['H']):
                return False
    if gaps is not None:
        if gaps == 'none':
            if feat['G']:
                return False
        elif gaps != '*':
            if feat['G'] != set(gaps.split(',')):
                return False
    if deps is not None:
        if deps == 'none':
            if feat['D']:
                return False
        elif deps != '*':
            if feat['D'] != set(deps.split(',')):
                return False
    if block is not None and block != '*':
        want = None if len_endian is MISSING else len_endian
        if want is None or block.upper() != want.upper():
            return False
    if be is not None and be != '*':
        if be == 'n/a':
            if feat['BE'] != 'n/a':
                return False
        elif be.lower() != feat['BE']:
            return False
    if sr is not None and sr != '*':
        if sr.lower() != feat['SR']:
            return False
    if files is not None:
        if files == '>0':
            if feat['P'] <= 0:
                return False
        elif files == '0':
            if feat['P'] != 0:
                return False
        elif files != '*':
            return False
    return True


def classify(header, rows, feat, len_endian=MISSING):
    for index, row in enumerate(rows, start=1):
        if match(row, header, feat, len_endian):
            label = row.get(column(header, 'label'))
            cause = row.get(column(header, 'cause') or column(header, 'action'))
            return label, index, cause
    return 'unclassified', 0, None


def main():  # tiny CLI: print the table as parsed, for eyeballing a fixture
    header, rows = parse_table(sys.argv[1])
    print('columns:', header)
    for row in rows:
        print(' ', row.get('label'))


if __name__ == '__main__':
    main()
