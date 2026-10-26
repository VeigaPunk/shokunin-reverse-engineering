#!/usr/bin/env python3
"""feat.py -- read REA extract-firmware envelopes into one feature table.

Accepts both shapes REA 6.5.0 emits:
  * full CLI envelope {"ok": true, "data": {...}, "meta": {...}}  (--full-output)
  * a bare data object (what the lane commits as a receipt)

Per envelope it records exactly the fields the C2 v2 grammar needs plus the
context fields the recon table reports:
  operation, provider.id (the real provider field), provider.name/version,
  handlers, per-chunk extraction_failed, gap kinds, gap dependencies,
  unpublished-entry kinds, diagnostic report __typename__ values, every
  recorded `command`, len(files), published_bytes, coverage.

Usage:
  python3 -B feat.py OUT.json ENVELOPE...
  python3 -B feat.py --table OUT.md ENVELOPE...
"""

import json
import os
import sys

TYPENAME_KEYS = ('__typename__', '__typename')


def typename(report):
    if not isinstance(report, dict):
        return None
    for key in TYPENAME_KEYS:
        if key in report:
            return report[key]
    return None


def walk_commands(obj, out):
    """Every `command` value below obj, as a str or a list of argv tokens."""
    stack = [obj]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            if 'command' in cur and cur['command']:
                out.append(cur['command'])
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)


def data_of(obj):
    if isinstance(obj, dict) and 'data' in obj and isinstance(obj['data'], dict):
        return obj['data'], obj.get('ok')
    return obj, None


def features(path):
    with open(path, 'r', encoding='utf-8') as handle:
        raw = json.load(handle)
    data, ok = data_of(raw)
    nr = data.get('normalized_result') or {}
    provider = data.get('provider') or {}
    chunks = nr.get('chunks') or []
    gaps = nr.get('extraction_gaps') or []
    diagnostics = nr.get('diagnostics') or []
    unpublished = nr.get('unpublished_entries') or []
    commands = []
    walk_commands(nr, commands)
    report_typenames = []
    for diag in diagnostics:
        name = typename(diag.get('report'))
        if name and name not in report_typenames:
            report_typenames.append(name)
    gap_deps = set()
    for gap in gaps:
        for dep in gap.get('dependencies') or ():
            gap_deps.add(dep)
    return {
        'file': os.path.basename(path),
        'ok': ok,
        'operation': data.get('operation'),
        'provider_id': provider.get('id'),
        'provider_name': provider.get('name'),
        'provider_version': provider.get('version'),
        'handlers': sorted({c.get('handler') for c in chunks if c.get('handler')}),
        'chunk_failed': [bool(c.get('extraction_failed')) for c in chunks],
        'chunk_ranges': [[c.get('range', {}).get('offset'),
                          c.get('range', {}).get('length')] for c in chunks],
        'gaps': sorted({g.get('kind') for g in gaps}),
        'gap_deps': sorted(gap_deps),
        'unpublished': sorted({u.get('kind') for u in unpublished}),
        'diagnostics': report_typenames,
        'commands': commands,
        'files': len(nr.get('files') or []),
        'published_bytes': nr.get('published_bytes'),
        'coverage': nr.get('coverage'),
    }


def be_cell(row):
    """-be feature, v1/v2 grammar semantics: yes / no / n-a from recorded argv."""
    tokens = []
    for cmd in row['commands']:
        if isinstance(cmd, str):
            tokens.extend(cmd.split())
        elif isinstance(cmd, list):
            tokens.extend(str(tok) for tok in cmd)
    named = [tok for tok in tokens if os.path.basename(tok).startswith('sasquatch')]
    if not named:
        return 'n/a'
    return 'yes' if '-be' in tokens else 'no'


def p_cell(row):
    return '0' if row['files'] == 0 else '>0'


def table(rows):
    out = ['| run | operation | provider.id | handler | failed | gaps | dependencies '
           '| unpublished | diagnostics | argv | -be | P | bytes | coverage |',
           '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for row in rows:
        out.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %d | %s | %s |'
                   % (row['file'].removesuffix('.json'), row['operation'],
                      row['provider_id'], '+'.join(row['handlers']) or 'none',
                      ', '.join('true' if f else 'false' for f in row['chunk_failed']) or '-',
                      '+'.join(row['gaps']) or 'none',
                      '+'.join(row['gap_deps']) or 'none',
                      '+'.join(row['unpublished']) or 'none',
                      '+'.join(row['diagnostics']) or 'none',
                      '; '.join(row['commands']) or 'none', be_cell(row),
                      row['files'], row['published_bytes'], row['coverage']))
    return '\n'.join(out) + '\n'


def main(argv):
    if len(argv) < 3:
        print('usage: feat.py [--table OUT.md] OUT.json ENVELOPE...', file=sys.stderr)
        return 2
    args = list(argv[1:])
    out_md = None
    if args and args[0] == '--table':
        out_md, args = args[1], args[2:]
    out_json, paths = args[0], args[1:]
    rows = [features(path) for path in paths]
    with open(out_json, 'w', encoding='utf-8') as handle:
        json.dump(rows, handle, indent=1, sort_keys=True)
        handle.write('\n')
    if out_md:
        with open(out_md, 'w', encoding='utf-8') as handle:
            handle.write(table(rows))
    print('%-34s %-11s %-9s %-18s %-6s %-24s %-22s %-3s' %
          ('run', 'operation', 'provider', 'handlers', 'failed', 'gaps', 'diagnostics', 'P'))
    for row in rows:
        print('%-34s %-11s %-9s %-18s %-6s %-24s %-22s %-3d' %
              (row['file'].removesuffix('.json'), row['operation'],
               row['provider_id'], '+'.join(row['handlers']) or 'none',
               ','.join('T' if f else 'F' for f in row['chunk_failed']) or '-',
               '+'.join(row['gaps']) or 'none',
               '+'.join(row['diagnostics']) or 'none', row['files']))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
