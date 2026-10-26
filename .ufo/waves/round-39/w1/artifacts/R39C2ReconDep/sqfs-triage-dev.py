#!/usr/bin/env python3
"""DEV harness for the R39-C2 triage grammar (seat R39C2ReconDep).

Implements the L1's stated contract literally so the candidate rule block can be
dev-scored before the freeze. This is NOT the frozen tools/round-39/sqfs-triage.py:
the L1 owns that file. This harness exists only to prove the grammar is
implementable and that the candidate rows separate the development envelopes.

Contract implemented
  table    : first markdown table after a line containing the marker
             `<!-- sqfs-triage-table v1 -->` (file given with --table)
  header   : label | handler | gap kinds | dependencies | -be in child argv |
             symlink removed | published files | cause -> action | source
  envelope : a bare `data` object or a full CLI envelope {ok,data,meta}
  features : H  = {normalized_result.chunks[].handler startswith 'squashfs'}
             G  = {extraction_gaps[].kind}
             D  = union(extraction_gaps[].dependencies)
             BE = over diagnostics[].report whose `command` (string or argv list)
                  names sasquatch: 'yes' if any has a standalone '-be' token,
                  'no' if such a command exists and none has it, 'n/a' if none
             SR = 'yes' if any diagnostics[].report.__typename__ ==
                  'MaliciousSymlinkRemoved' (also accepted anywhere under
                  raw_result.report) else 'no'
             P  = len(normalized_result.files)
  cells    : '*' anything; handler 'none' (H empty) or an fnmatch pattern that
             matches >= 1 element of H; gap kinds / dependencies 'none' (empty
             set) or 'a+b' (set equals exactly {a,b}); -be / symlink removed
             yes|no|n/a; published files 0|>0|*
  first matching row wins; no match -> 'unclassified'
  a malformed cell makes the whole table unevaluable -> exit 2
"""
import argparse
import fnmatch
import json
import sys

CELLS = ['label', 'handler', 'gap kinds', 'dependencies',
         '-be in child argv', 'symlink removed', 'published files',
         'cause -> action', 'source']
MARKER = '<!-- sqfs-triage-table v1 -->'


class TableError(Exception):
    pass


def strip_cell(text):
    text = text.strip()
    if len(text) >= 2 and text[0] == '`' and text[-1] == '`':
        text = text[1:-1].strip()
    return text


def parse_table(path):
    lines = open(path, encoding='utf-8').read().splitlines()
    for index, line in enumerate(lines):
        if MARKER in line:
            break
    else:
        raise TableError(f'no marker {MARKER}')
    start = None
    for index in range(index + 1, len(lines)):
        if lines[index].lstrip().startswith('|'):
            start = index
            break
    if start is None:
        raise TableError('no markdown table after the marker')

    def split_row(text):
        text = text.strip()
        if text.startswith('|'):
            text = text[1:]
        if text.endswith('|'):
            text = text[:-1]
        return [strip_cell(cell) for cell in text.split('|')]

    header = split_row(lines[start])
    if header != CELLS:
        raise TableError(f'header mismatch: {header!r}')
    rows = []
    for line in lines[start + 1:]:
        if not line.lstrip().startswith('|'):
            break
        cells = split_row(line)
        if all(set(cell) <= set('-: ') for cell in cells):
            continue  # separator row
        if len(cells) != len(CELLS):
            raise TableError(f'row has {len(cells)} cells: {line!r}')
        rows.append(dict(zip(CELLS, cells)))
    if not rows:
        raise TableError('table has no data rows')
    for row in rows:
        validate_row(row)
    return rows


def set_cell(cell, name):
    """Set cell: 'none' -> empty set, 'a+b' -> exactly {a,b}, '*' -> wildcard (None)."""
    if cell == '*':
        return None
    if cell == 'none':
        return set()
    parts = cell.split('+')
    if not parts or any(not part.strip() for part in parts):
        raise TableError(f'{name}: malformed set cell {cell!r}')
    names = [part.strip() for part in parts]
    if len(set(names)) != len(names):
        raise TableError(f'{name}: duplicate name in {cell!r}')
    return set(names)


def validate_row(row):
    if not row['label']:
        raise TableError('empty label')
    handler = row['handler']
    if handler != 'none' and handler != '*' and not handler:
        raise TableError(f'{row["label"]}: bad handler cell {handler!r}')
    set_cell(row['gap kinds'], 'gap kinds')
    set_cell(row['dependencies'], 'dependencies')
    for name in ('-be in child argv', 'symlink removed'):
        if row[name] not in ('yes', 'no', 'n/a', '*'):
            raise TableError(f'{row["label"]}: bad {name} cell {row[name]!r}')
    if row['published files'] not in ('0', '>0', '*'):
        raise TableError(f'{row["label"]}: bad published files cell '
                         f'{row["published files"]!r}')


def mismatch(row, facts):
    label = row['label']
    handler = row['handler']
    if handler == 'none':
        if facts['H']:
            return False
    elif handler != '*':
        if not any(fnmatch.fnmatchcase(name, handler) for name in facts['H']):
            return False
    gaps_cell = set_cell(row['gap kinds'], 'gap kinds')
    if gaps_cell is not None and gaps_cell != set(facts['G']):
        return False
    deps_cell = set_cell(row['dependencies'], 'dependencies')
    if deps_cell is not None and deps_cell != set(facts['D']):
        return False
    for name, key in (('-be in child argv', 'BE'), ('symlink removed', 'SR')):
        cell = row[name]
        if cell != '*' and cell != facts[key]:
            return False
    published = row['published files']
    if published == '0' and facts['P'] != 0:
        return False
    if published == '>0' and facts['P'] <= 0:
        return False
    return True


def walk_typenames(value, found):
    if isinstance(value, list):
        for item in value:
            walk_typenames(item, found)
    elif isinstance(value, dict):
        name = value.get('__typename__')
        if isinstance(name, str):
            found.add(name)
        for child in value.values():
            walk_typenames(child, found)


def features(envelope):
    data = envelope['data'] if isinstance(envelope, dict) and 'data' in envelope \
        else envelope
    normalized = data.get('normalized_result') or {}
    chunks = normalized.get('chunks') or []
    gaps = normalized.get('extraction_gaps') or []
    diagnostics = normalized.get('diagnostics') or []
    files = normalized.get('files') or []

    handlers = {c.get('handler') for c in chunks if isinstance(c.get('handler'), str)}
    H = sorted(h for h in handlers if h.startswith('squashfs'))
    G = sorted({g.get('kind') for g in gaps if isinstance(g.get('kind'), str)})
    D = sorted({name for g in gaps for name in (g.get('dependencies') or [])
                if isinstance(name, str)})

    sasquatch_commands = []
    for item in diagnostics:
        report = (item or {}).get('report')
        if not isinstance(report, dict):
            continue
        command = report.get('command')
        if isinstance(command, str):
            tokens = command.split()
        elif isinstance(command, list):
            tokens = [t for t in command if isinstance(t, str)]
        else:
            continue
        if any('sasquatch' in token for token in tokens):
            sasquatch_commands.append(tokens)
    if not sasquatch_commands:
        BE = 'n/a'
    elif any('-be' in tokens for tokens in sasquatch_commands):
        BE = 'yes'
    else:
        BE = 'no'

    typenames = set()
    for item in diagnostics:
        walk_typenames((item or {}).get('report'), typenames)
    walk_typenames(data.get('raw_result'), typenames)
    SR = 'yes' if 'MaliciousSymlinkRemoved' in typenames else 'no'

    return {'H': H, 'G': G, 'D': D, 'BE': BE, 'SR': SR, 'P': len(files)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--table', required=True)
    parser.add_argument('--envelope', action='append', default=[])
    parser.add_argument('--json-out')
    args = parser.parse_args()
    try:
        rows = parse_table(args.table)
    except TableError as error:
        print(f'unevaluable table: {error}', file=sys.stderr)
        return 2
    results = []
    for path in args.envelope:
        envelope = json.load(open(path, encoding='utf-8'))
        facts = features(envelope)
        label = 'unclassified'
        for row in rows:
            if mismatch(row, facts):
                label = row['label']
                break
        results.append({'envelope': path, 'label': label, 'features': facts})
        print(json.dumps({'envelope': path, 'label': label, **facts},
                         sort_keys=True))
    if args.json_out:
        json.dump(results, open(args.json_out, 'w', encoding='utf-8'), indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
