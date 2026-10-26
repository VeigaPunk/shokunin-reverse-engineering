#!/usr/bin/env python3
"""Recon probe for the R40-C2 triage-table v2 contract (NOT the frozen interpreter).

Purpose: show that the L1's v2 grammar, exactly as drafted, can express the
measured zero-regular-file outcomes with a first-match table, and that the
domain guard sends a non-`extract_firmware` / non-`unblob` envelope to
(`unclassified`, `none`).

Contract implemented here (L1 draft, quoted in the report):
  * table = first markdown table after a line containing
    `<!-- sqfs-triage-table v2 -->`, inside the section that starts at a
    `## Queue-drain craft` heading and ends at the next `## ` heading;
  * exact header order:
    label | operation | provider | handler | gap kinds | dependencies |
    -be in child argv | symlink removed | published files | action | cause | source
  * rows top to bottom, first full match -> (label, action);
    no match -> (unclassified, none);
  * duplicate label -> exit 2; malformed cell -> exit 2; an action outside
    `<!-- sqfs-triage-actions: ... -->` -> exit 2;
  * condition cells: `*` any; operation/provider exact string or `*`;
    handler `none` or fnmatch (any); gap kinds/dependencies `none` or exact
    set `a+b`; -be / symlink removed yes|no|n/a; published files 0|>0|*.

Ambiguity it deliberately accepts both ways (flagged in the report): the
actions line may sit on the line directly above the marker or directly above
the table header.

Usage:
  probe-v2-rows.py --table FILE --json OUT.tsv ENVELOPE.json [...]
Exit: 0 labelled; 2 table/envelope/invocation error.
"""
import fnmatch
import json
import sys

MARKER = '<!-- sqfs-triage-table v2 -->'
ACTIONS_PREFIX = '<!-- sqfs-triage-actions:'
CRAFT_HEADING = 'queue-drain craft'
HEADER = ['label', 'operation', 'provider', 'handler', 'gap kinds', 'dependencies',
          '-be in child argv', 'symlink removed', 'published files', 'action',
          'cause', 'source']
SYMLINK_TYPENAME = 'MaliciousSymlinkRemoved'


class TableError(Exception):
    pass


class EnvelopeError(Exception):
    pass


def as_list(value):
    return value if isinstance(value, list) else []


def iter_dicts(obj):
    stack = [obj]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            yield cur
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)


def command_tokens(cmd):
    if isinstance(cmd, str):
        return cmd.split()
    if isinstance(cmd, (list, tuple)):
        return [t for t in cmd if isinstance(t, str)]
    return None


def extractor_commands(data):
    commands = []

    def take(cmd):
        tokens = command_tokens(cmd)
        if tokens and any(t.rsplit('/', 1)[-1].startswith('sasquatch') for t in tokens):
            if cmd not in commands:
                commands.append(cmd)

    nr = data.get('normalized_result') or {}
    for source in (nr.get('diagnostics'), data.get('diagnostics')):
        for diag in as_list(source):
            report = diag.get('report') if isinstance(diag, dict) else None
            if isinstance(report, dict) and 'command' in report:
                take(report['command'])
    for found in iter_dicts(data.get('raw_result')):
        if 'command' in found:
            take(found['command'])
    return commands


def envelope_data(obj, path):
    if not isinstance(obj, dict):
        raise EnvelopeError('%s: not a JSON object' % path)
    if isinstance(obj.get('normalized_result'), dict):
        return obj
    inner = obj.get('data')
    if isinstance(inner, dict) and isinstance(inner.get('normalized_result'), dict):
        return inner
    raise EnvelopeError('%s: no normalized_result' % path)


def features(data):
    nr = data['normalized_result']
    handlers = sorted({c.get('handler') for c in as_list(nr.get('chunks'))
                       if isinstance(c, dict) and isinstance(c.get('handler'), str)
                       and c['handler'].startswith('squashfs')})
    gaps = as_list(nr.get('extraction_gaps'))
    gap_kinds = sorted({g.get('kind') for g in gaps
                        if isinstance(g, dict) and isinstance(g.get('kind'), str)})
    dependencies = sorted({d for g in gaps if isinstance(g, dict)
                           for d in as_list(g.get('dependencies'))
                           if isinstance(d, str)})
    commands = extractor_commands(data)
    if not commands:
        be = 'n/a'
    else:
        be = 'yes' if any('-be' in (command_tokens(c) or []) for c in commands) else 'no'
    sr = 'no'
    for diag in as_list(nr.get('diagnostics')):
        report = diag.get('report') if isinstance(diag, dict) else None
        if isinstance(report, dict) and report.get('__typename__') == SYMLINK_TYPENAME:
            sr = 'yes'
            break
    if sr == 'no':
        for found in iter_dicts(data.get('raw_result')):
            if found.get('__typename__') == SYMLINK_TYPENAME:
                sr = 'yes'
                break
    return {'OP': data.get('operation'),
            'PV': (data.get('provider') or {}).get('id'),
            'H': handlers, 'G': gap_kinds, 'D': dependencies,
            'BE': be, 'SR': sr, 'P': len(as_list(nr.get('files')))}


def clean_cell(raw):
    cell = raw.strip()
    if len(cell) >= 2 and cell[0] == '`' and cell[-1] == '`':
        cell = cell[1:-1]
    return cell.strip()


def split_row(line):
    return [c for c in line.strip().strip('|').split('|')]


def parse_table(path):
    lines = open(path, encoding='utf-8').read().splitlines()
    craft = None
    for i, line in enumerate(lines):
        if line.startswith('## ') and CRAFT_HEADING in line.lower():
            craft = i
            break
    if craft is None:
        raise TableError('no "## Queue-drain craft" heading')
    end = len(lines)
    for i in range(craft + 1, len(lines)):
        if lines[i].startswith('## '):
            end = i
            break
    marker = None
    for i in range(craft + 1, end):
        if MARKER in lines[i]:
            marker = i
            break
    if marker is None:
        raise TableError('marker %r absent from the craft section' % MARKER)
    start = None
    for i in range(marker + 1, end):
        if lines[i].lstrip().startswith('|'):
            start = i
            break
    if start is None:
        raise TableError('marker present but no table follows it')
    table = []
    for i in range(start, end):
        if not lines[i].lstrip().startswith('|'):
            break
        table.append(lines[i])
    actions_line = None
    for cand in (start - 1, marker - 1, marker):
        if 0 <= cand < len(lines) and ACTIONS_PREFIX in lines[cand]:
            actions_line = lines[cand]
            break
    if actions_line is None:
        raise TableError('no sqfs-triage-actions line directly above the table')
    vocab = actions_line.split(ACTIONS_PREFIX, 1)[1].split('-->', 1)[0].split()
    if not vocab:
        raise TableError('empty action vocabulary')
    header = [clean_cell(c) for c in split_row(table[0])]
    if header != HEADER:
        raise TableError('header %r != %r' % (header, HEADER))
    if len(table) < 3:
        raise TableError('table has no separator row')
    rules = []
    seen = set()
    for line in table[2:]:
        cells = [clean_cell(c) for c in split_row(line)]
        if len(cells) != len(HEADER):
            raise TableError('row has %d cells, expected %d: %r'
                             % (len(cells), len(HEADER), line))
        label, op, pv, handler, gaps, deps, be, sr, files, action = cells[:10]
        if not label:
            raise TableError('empty label')
        if label in seen:
            raise TableError('duplicate label %r' % label)
        seen.add(label)
        if op == '' or pv == '':
            raise TableError('empty domain cell in %r' % label)
        if handler == '':
            raise TableError('%s: empty handler cell' % label)
        if be not in ('*', 'yes', 'no', 'n/a'):
            raise TableError('%s: -be cell %r' % (label, be))
        if sr not in ('*', 'yes', 'no', 'n/a'):
            raise TableError('%s: symlink removed cell %r' % (label, sr))
        if files not in ('*', '0', '>0'):
            raise TableError('%s: published files cell %r' % (label, files))
        if action not in vocab:
            raise TableError('%s: action %r not in the vocabulary' % (label, action))
        rules.append({'label': label, 'op': op, 'pv': pv, 'handler': handler,
                      'gaps': parse_set(gaps, label, 'gap kinds'),
                      'deps': parse_set(deps, label, 'dependencies'),
                      'be': be, 'sr': sr, 'files': files, 'action': action})
    return rules, vocab


def parse_set(cell, label, column):
    if cell == '*':
        return ('any', None)
    if cell == 'none':
        return ('none', None)
    parts = cell.split('+')
    if not parts or any(not p for p in parts) or len(set(parts)) != len(parts):
        raise TableError('%s: malformed %s cell %r' % (label, column, cell))
    return ('exact', frozenset(parts))


def set_matches(spec, values):
    kind, payload = spec
    if kind == 'any':
        return True
    if kind == 'none':
        return not values
    return frozenset(values) == payload


def rule_matches(rule, feat):
    if rule['op'] != '*' and rule['op'] != feat['OP']:
        return False
    if rule['pv'] != '*' and rule['pv'] != feat['PV']:
        return False
    if rule['handler'] == 'none':
        if feat['H']:
            return False
    elif not any(fnmatch.fnmatchcase(h, rule['handler']) for h in feat['H']):
        return False
    if not set_matches(rule['gaps'], feat['G']):
        return False
    if not set_matches(rule['deps'], feat['D']):
        return False
    if rule['be'] != '*' and rule['be'] != feat['BE']:
        return False
    if rule['sr'] != '*' and rule['sr'] != feat['SR']:
        return False
    if rule['files'] == '0' and feat['P'] != 0:
        return False
    if rule['files'] == '>0' and feat['P'] <= 0:
        return False
    return True


def classify(rules, feat):
    for index, rule in enumerate(rules, 1):
        if rule_matches(rule, feat):
            return rule, index
    return None, None


def main(argv):
    if '--table' not in argv or '--json' not in argv:
        print('usage: probe-v2-rows.py --table FILE --json OUT.tsv ENVELOPE...', file=sys.stderr)
        return 2
    table = argv[argv.index('--table') + 1]
    out = argv[argv.index('--json') + 1]
    envelopes = [a for a in argv[1:] if a not in (table, out) and not a.startswith('--')]
    try:
        rules, vocab = parse_table(table)
    except (TableError, OSError) as exc:
        print('probe: %s' % exc, file=sys.stderr)
        return 2
    rows = []
    for path in envelopes:
        try:
            obj = json.load(open(path, encoding='utf-8'))
            feat = features(envelope_data(obj, path))
        except (OSError, ValueError, EnvelopeError) as exc:
            print('probe: %s' % exc, file=sys.stderr)
            return 2
        rule, index = classify(rules, feat)
        label = rule['label'] if rule else 'unclassified'
        action = rule['action'] if rule else 'none'
        rows.append((path, label, action, index, feat))
    with open(out, 'w', encoding='utf-8') as handle:
        handle.write('envelope\tlabel\taction\trule\tOP\tPV\tH\tG\tD\tBE\tSR\tP\n')
        for path, label, action, index, f in rows:
            handle.write('\t'.join([path, label, action, str(index or 'none'),
                                    str(f['OP']), str(f['PV']), ','.join(f['H']) or '-',
                                    '+'.join(f['G']) or '-', '+'.join(f['D']) or '-',
                                    f['BE'], f['SR'], str(f['P'])]) + '\n')
    print('probe: %d envelopes, %d rules, vocabulary %d tokens'
          % (len(rows), len(rules), len(vocab)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
