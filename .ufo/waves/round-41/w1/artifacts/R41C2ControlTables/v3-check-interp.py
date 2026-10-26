#!/usr/bin/env python3
"""v3-check-interp.py - DEVELOPMENT replica of the v3 triage interpreter (control check).

Not the frozen interpreter: R41C2Interp owns `tools/round-41/sqfs-triage-v3.py`.  This
file exists so the control tables can be scored before that tool lands, and it is
written to the same contract so the harness can swap the two:

  marker     `<!-- sqfs-triage-table v3 -->` inside a `## Queue-drain craft` section
  vocabulary `<!-- sqfs-triage-actions: a b c -->` directly above the table
  columns    12, identical to v2
  set cells  `*` any | `none` empty | `m1,m2` exact | `m1,m2+` contains
  rows       first match top to bottom; no match -> (unclassified, none)
  exit       0 labelled | 2 table missing/malformed, envelope unreadable, v2 marker

Parity evidence: with a v2-row table it reproduces tools/round-40/sqfs-triage-v2.py on
every committed round-40 C2 envelope (see checks.txt).

Usage:
  v3-check-interp.py --skill SKILL.md --json ENV...   # machine readable
  v3-check-interp.py --skill SKILL.md ENV...          # path<TAB>label<TAB>action
  v3-check-interp.py --skill SKILL.md --table-only
  v3-check-interp.py --selftest
"""

import argparse
import fnmatch
import json
import os
import re
import shlex
import sys

MARKER = '<!-- sqfs-triage-table v3 -->'
MARKER_V2 = '<!-- sqfs-triage-table v2 -->'
ACTIONS_PREFIX = '<!-- sqfs-triage-actions:'
ACTIONS_SUFFIX = '-->'
CRAFT_PREFIX = 'queue-drain craft'
HEADER = ['label', 'operation', 'provider', 'handler', 'gap kinds', 'dependencies',
          '-be in child argv', 'symlink removed', 'published files', 'action', 'cause',
          'source']
BE_VALUES = ('yes', 'no', 'n/a')
FILES_VALUES = ('0', '>0')
SYMLINK_TYPENAME = 'MaliciousSymlinkRemoved'
DEFAULT_LABEL = 'unclassified'
DEFAULT_ACTION = 'none'
OPERATION_TOKEN = 'extract_firmware'

SEP_RE = re.compile(r'^:?-+:?$')
NAME_RE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.\-]*$')
HANDLER_RE = re.compile(r'^[A-Za-z0-9_?*.\-\[\]]+$')
OPERATION_RE = re.compile(r'^[a-z][a-z0-9_.\-]*$')
PROVIDER_RE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.\-]*$')
ACTION_RE = re.compile(r'^[a-z][a-z0-9]*(-[a-z0-9]+)*$')


class TableError(Exception):
    pass


class EnvelopeError(Exception):
    pass


def clean_cell(raw):
    s = raw.strip()
    if len(s) >= 2 and s[0] == '`' and s[-1] == '`' and s.count('`') == 2:
        s = s[1:-1].strip()
    return s


def split_row(line):
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|'):
        s = s[:-1]
    return s.split('|')


def craft_bounds(lines):
    start = None
    for i, line in enumerate(lines):
        if line.startswith('## ') and not line.startswith('### ') \
                and line[3:].strip().lower().startswith(CRAFT_PREFIX):
            start = i + 1
            break
    if start is None:
        raise TableError('no "## Queue-drain craft" heading in the document')
    end = len(lines)
    for j in range(start, len(lines)):
        if lines[j].startswith('## ') and not lines[j].startswith('### '):
            end = j
            break
    return start, end


def parse_set_cell(cell, column):
    if cell == '*':
        return ('any', None)
    if cell == 'none':
        return ('none', None)
    contains = cell.endswith('+')
    body = cell[:-1] if contains else cell
    members = [m for m in body.split(',')]
    if any(not m for m in members):
        raise TableError('%s cell %r has an empty set member' % (column, cell))
    for member in members:
        if not NAME_RE.match(member):
            raise TableError('%s cell %r has a malformed member %r'
                             % (column, cell, member))
    if len(set(members)) != len(members):
        raise TableError('%s cell %r repeats a member' % (column, cell))
    return ('contains' if contains else 'exact', frozenset(members))


def parse_handler_cell(cell):
    if cell == '*':
        return ('any', None)
    if cell == 'none':
        return ('none', None)
    if not HANDLER_RE.match(cell):
        raise TableError('handler cell %r is not *, none, or an fnmatch pattern' % cell)
    return ('pattern', cell)


def parse_domain_cell(cell, column, token_re):
    if cell == '*':
        return '*'
    if not token_re.match(cell):
        raise TableError('%s cell %r is not * or a bare token' % (column, cell))
    return cell


def parse_enum_cell(cell, column, values):
    if cell == '*':
        return '*'
    if cell in values:
        return cell
    raise TableError('%s cell %r is not one of %s or *' % (column, cell, ', '.join(values)))


def parse_actions_line(line):
    s = line.strip()
    at = s.find(ACTIONS_PREFIX)
    if at < 0:
        raise TableError('no %r vocabulary line directly above the table' % ACTIONS_PREFIX)
    rest = s[at + len(ACTIONS_PREFIX):]
    if ACTIONS_SUFFIX not in rest:
        raise TableError('the action vocabulary line has no closing %r' % ACTIONS_SUFFIX)
    rest = rest[:rest.index(ACTIONS_SUFFIX)].strip()
    if not rest:
        raise TableError('the action vocabulary is empty')
    seen = []
    for token in rest.split():
        if not ACTION_RE.match(token):
            raise TableError('action token %r is not a lowercase dashed token' % token)
        if token in seen:
            raise TableError('action token %r is declared twice' % token)
        seen.append(token)
    return seen


def parse_table(lines, first_line_no, vocabulary):
    if len(lines) < 3:
        raise TableError('table at line %d has no header, separator and data row'
                         % first_line_no)
    header = [clean_cell(c) for c in split_row(lines[0])]
    if [c.lower() for c in header] != [h.lower() for h in HEADER]:
        raise TableError('table at line %d: header is %r, expected %r'
                         % (first_line_no, header, HEADER))
    sep = [clean_cell(c) for c in split_row(lines[1])]
    if len(sep) != len(HEADER) or not all(SEP_RE.match(c) for c in sep):
        raise TableError('table at line %d: second row is not a %d-cell separator'
                         % (first_line_no + 1, len(HEADER)))
    rules = []
    labels = {}
    for offset, raw in enumerate(lines[2:], start=3):
        line_no = first_line_no + offset - 1
        cells = [clean_cell(c) for c in split_row(raw)]
        if len(cells) != len(HEADER):
            raise TableError('row at line %d has %d cells, expected %d'
                             % (line_no, len(cells), len(HEADER)))
        (label, operation, provider, handler, gap, dep, be, sr, files, action, cause,
         source) = cells
        if not label or not NAME_RE.match(label):
            raise TableError('line %d: label %r is not a bare token' % (line_no, label))
        if label in labels:
            raise TableError('line %d: duplicate label %r (first on line %d)'
                             % (line_no, label, labels[label]))
        labels[label] = line_no
        if not action or action not in vocabulary:
            raise TableError('line %d: action %r is not declared in the vocabulary line'
                             % (line_no, action))
        if not cause or '->' not in cause:
            raise TableError('line %d: cause -> action cell has no "->"' % line_no)
        if not source:
            raise TableError('line %d: empty source cell' % line_no)
        rules.append({
            'index': len(rules) + 1,
            'label': label,
            'operation': parse_domain_cell(operation, 'operation', OPERATION_RE),
            'provider': parse_domain_cell(provider, 'provider', PROVIDER_RE),
            'handler': parse_handler_cell(handler),
            'gap_kinds': parse_set_cell(gap, 'gap kinds'),
            'dependencies': parse_set_cell(dep, 'dependencies'),
            'be': parse_enum_cell(be, '-be in child argv', BE_VALUES),
            'symlink_removed': parse_enum_cell(sr, 'symlink removed', BE_VALUES),
            'files': parse_enum_cell(files, 'published files', FILES_VALUES),
            'action': action,
        })
    if not rules:
        raise TableError('table at line %d has no rule rows' % first_line_no)
    return rules


def parse_skill(text):
    lines = text.splitlines()
    start, end = craft_bounds(lines)
    marker_line = None
    v2_line = None
    for i in range(start, end):
        if MARKER in lines[i] and marker_line is None:
            marker_line = i
        if MARKER_V2 in lines[i] and v2_line is None:
            v2_line = i
    if marker_line is None:
        if v2_line is not None:
            raise TableError('line %d: a v2 marker is refused by the v3 interpreter'
                             % (v2_line + 1))
        raise TableError('marker %r absent from the craft section' % MARKER)
    table_start = None
    for i in range(marker_line + 1, end):
        if lines[i].lstrip().startswith('|'):
            table_start = i
            break
    if table_start is None:
        raise TableError('no markdown table after the marker inside the craft section')
    actions_line = table_start - 1
    while actions_line > start and not lines[actions_line].strip():
        actions_line -= 1
    if actions_line < start or ACTIONS_PREFIX not in lines[actions_line]:
        raise TableError('line %d: no vocabulary line directly above the table'
                         % (table_start + 1))
    vocabulary = parse_actions_line(lines[actions_line])
    table = []
    i = table_start
    while i < end and lines[i].lstrip().startswith('|'):
        table.append(lines[i])
        i += 1
    rules = parse_table(table, table_start + 1, vocabulary)
    return rules, {'marker_line': marker_line + 1, 'actions_line': actions_line + 1,
                   'table_line': table_start + 1, 'rules': len(rules),
                   'actions': vocabulary}


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
        try:
            return shlex.split(cmd)
        except ValueError:
            return cmd.split()
    if isinstance(cmd, (list, tuple)):
        return [t for t in cmd if isinstance(t, str)]
    return None


def extractor_commands(data):
    commands = []

    def take(cmd):
        tokens = command_tokens(cmd)
        if tokens and any(t.rsplit('/', 1)[-1].startswith('sasquatch') for t in tokens) \
                and cmd not in commands:
            commands.append(cmd)

    nr = data.get('normalized_result')
    nr = nr if isinstance(nr, dict) else {}
    for source in (nr.get('diagnostics'), data.get('diagnostics')):
        for diag in as_list(source):
            report = diag.get('report') if isinstance(diag, dict) else None
            if isinstance(report, dict) and 'command' in report:
                take(report['command'])
    for found in iter_dicts(data.get('raw_result')):
        if 'command' in found:
            take(found['command'])
    return commands


def envelope_data(obj, path='<envelope>'):
    if not isinstance(obj, dict):
        raise EnvelopeError('%s: not a JSON object' % path)
    candidate = None
    if isinstance(obj.get('normalized_result'), dict):
        candidate = obj
    else:
        inner = obj.get('data')
        if isinstance(inner, dict):
            candidate = inner
        elif isinstance(obj.get('operation'), str):
            candidate = obj
    if candidate is None:
        raise EnvelopeError('%s: no normalized_result or operation' % path)
    if 'normalized_result' in candidate and not isinstance(candidate['normalized_result'],
                                                           dict):
        raise EnvelopeError('%s: normalized_result is not an object' % path)
    if not isinstance(candidate.get('normalized_result'), dict) \
            and not isinstance(candidate.get('operation'), str):
        raise EnvelopeError('%s: no normalized_result object and no operation string'
                            % path)
    return candidate


def features(data):
    op = data.get('operation')
    operation = op if isinstance(op, str) else ''
    provider = data.get('provider')
    if isinstance(provider, dict):
        pid = provider.get('id')
        provider_id = pid if isinstance(pid, str) else ''
    elif isinstance(provider, str):
        provider_id = provider
    else:
        provider_id = ''
    nr = data.get('normalized_result')
    if nr is None:
        nr = {}
    if not isinstance(nr, dict):
        raise EnvelopeError('normalized_result is not an object')
    if operation == OPERATION_TOKEN and not isinstance(data.get('normalized_result'), dict):
        raise EnvelopeError('an extract_firmware envelope has no normalized_result object')
    handlers = set()
    for chunk in as_list(nr.get('chunks')):
        handler = chunk.get('handler') if isinstance(chunk, dict) else None
        if isinstance(handler, str) and handler.startswith('squashfs'):
            handlers.add(handler)
    gap_kinds = set()
    dependencies = set()
    for gap in as_list(nr.get('extraction_gaps')):
        if not isinstance(gap, dict):
            continue
        kind = gap.get('kind')
        if isinstance(kind, str):
            gap_kinds.add(kind)
        for dep in as_list(gap.get('dependencies')):
            if isinstance(dep, str):
                dependencies.add(dep)
    commands = extractor_commands(data)
    if not commands:
        be = 'n/a'
    else:
        be = 'no'
        for cmd in commands:
            if '-be' in (command_tokens(cmd) or []):
                be = 'yes'
                break
    symlink = 'no'
    for diag in as_list(nr.get('diagnostics')):
        report = diag.get('report') if isinstance(diag, dict) else None
        if isinstance(report, dict) and report.get('__typename__') == SYMLINK_TYPENAME:
            symlink = 'yes'
            break
    if symlink == 'no':
        for found in iter_dicts(data.get('raw_result')):
            if found.get('__typename__') == SYMLINK_TYPENAME:
                symlink = 'yes'
                break
    return {'OP': operation, 'PV': provider_id, 'H': sorted(handlers),
            'G': sorted(gap_kinds), 'D': sorted(dependencies), 'BE': be, 'SR': symlink,
            'P': len(as_list(nr.get('files'))), 'commands': commands}


def load_envelope(path):
    try:
        with open(path, 'r', encoding='utf-8') as handle:
            obj = json.load(handle)
    except OSError as exc:
        raise EnvelopeError('%s: %s' % (path, exc.strerror or exc))
    except ValueError as exc:
        raise EnvelopeError('%s: not valid JSON (%s)' % (path, exc))
    return features(envelope_data(obj, path))


def match_set(spec, values):
    kind, payload = spec
    if kind == 'any':
        return True
    if kind == 'none':
        return not values
    got = frozenset(values)
    if kind == 'contains':
        return payload <= got
    return got == payload


def rule_matches(rule, feat):
    if rule['operation'] != '*' and rule['operation'] != feat['OP']:
        return False
    if rule['provider'] != '*' and rule['provider'] != feat['PV']:
        return False
    kind, payload = rule['handler']
    if kind == 'none':
        if feat['H']:
            return False
    elif kind == 'pattern' and not any(fnmatch.fnmatchcase(v, payload) for v in feat['H']):
        return False
    if not match_set(rule['gap_kinds'], feat['G']):
        return False
    if not match_set(rule['dependencies'], feat['D']):
        return False
    if rule['be'] != '*' and rule['be'] != feat['BE']:
        return False
    if rule['symlink_removed'] != '*' and rule['symlink_removed'] != feat['SR']:
        return False
    if rule['files'] == '0' and feat['P'] != 0:
        return False
    if rule['files'] == '>0' and feat['P'] <= 0:
        return False
    return True


def classify(rules, feat):
    for rule in rules:
        if rule_matches(rule, feat):
            return rule
    return None


def run(ns):
    if not ns.skill:
        raise TableError('--skill is required')
    with open(ns.skill, 'r', encoding='utf-8') as handle:
        text = handle.read()
    rules, info = parse_skill(text)
    if ns.table_only:
        print('skill: %s' % ns.skill)
        print('marker line: %d  actions line: %d  table line: %d  rules: %d'
              % (info['marker_line'], info['actions_line'], info['table_line'],
                 info['rules']))
        for rule in rules:
            print('%d. %s -> %s' % (rule['index'], rule['label'], rule['action']))
        return 0
    if not ns.envelopes:
        raise TableError('no envelope given')
    results = []
    for path in ns.envelopes:
        feat = load_envelope(path)
        rule = classify(rules, feat)
        results.append((path, feat, rule))
    if ns.json:
        payload = {'skill': ns.skill, 'marker_line': info['marker_line'],
                   'table_line': info['table_line'], 'rules': info['rules'],
                   'actions': list(info['actions']),
                   'results': [{'path': path,
                                'label': rule['label'] if rule else DEFAULT_LABEL,
                                'action': rule['action'] if rule else DEFAULT_ACTION,
                                'rule': rule['index'] if rule else None,
                                'features': feat}
                               for path, feat, rule in results]}
        json.dump(payload, sys.stdout, indent=1, sort_keys=True)
        sys.stdout.write('\n')
        return 0
    for path, _feat, rule in results:
        print('%s\t%s\t%s' % (path, rule['label'] if rule else DEFAULT_LABEL,
                              rule['action'] if rule else DEFAULT_ACTION))
    return 0


def selftest():
    """Inline tables only (no embedded copy of any SKILL table)."""
    def block(rows, marker=MARKER, actions='none count-gap salvage-partial raise-depth'):
        lines = [marker, '<!-- sqfs-triage-actions: %s -->' % actions,
                 '| ' + ' | '.join(HEADER) + ' |',
                 '| ' + ' | '.join(['---'] * len(HEADER)) + ' |']
        lines.extend('| ' + ' | '.join('`%s`' % c for c in row) + ' |' for row in rows)
        return '\n'.join(lines) + '\n'

    def row(label, gap='*', files='*', action='none'):
        return [label, 'extract_firmware', 'unblob', 'squashfs_v4_*', gap, '*', '*',
                '*', files, action, 'cause -> action', 'src']

    def parse(text):
        return parse_skill('## Queue-drain craft\n\n' + block(text))[0]

    def feat(gap=(), files=1, be='n/a', sr='no'):
        return {'OP': 'extract_firmware', 'PV': 'unblob', 'H': ['squashfs_v4_be'],
                'G': sorted(gap), 'D': [], 'BE': be, 'SR': sr, 'P': files,
                'commands': []}

    cases = []

    def case(name, fn):
        cases.append((name, fn))

    def c_contains_hits():
        rules = parse([row('d', gap='depth-limited+', action='raise-depth')])
        assert classify(rules, feat(['depth-limited']))['label'] == 'd'
        assert classify(rules, feat(['depth-limited', 'unpublished-entry']))['label'] == 'd'

    case('contains form matches supersets', c_contains_hits)

    def c_exact_misses():
        rules = parse([row('e', gap='depth-limited', action='raise-depth')])
        assert classify(rules, feat(['depth-limited']))['label'] == 'e'
        assert classify(rules, feat(['depth-limited', 'unpublished-entry'])) is None

    case('exact set rejects one extra kind', c_exact_misses)

    def c_multi_contains():
        rules = parse([row('m', gap='a,b+', action='raise-depth')])
        assert classify(rules, feat(['a', 'b', 'c']))['label'] == 'm'
        assert classify(rules, feat(['a'])) is None

    case('two-member contains needs both', c_multi_contains)

    def c_first_match():
        rules = parse([row('one', gap='extractor-failure+', files='>0'),
                       row('two', gap='extractor-failure+', files='*')])
        assert classify(rules, feat(['extractor-failure'], 2))['label'] == 'one'
        assert classify(rules, feat(['extractor-failure'], 0))['label'] == 'two'

    case('first match wins', c_first_match)

    def c_v2_marker_refused():
        try:
            parse_skill('## Queue-drain craft\n\n' + block([row('x')], marker=MARKER_V2))
        except TableError:
            return
        raise AssertionError('a v2 marker was accepted')

    case('v2 marker refused', c_v2_marker_refused)

    def c_duplicate_refused():
        try:
            parse([row('x'), row('x')])
        except TableError:
            return
        raise AssertionError('a duplicate label was accepted')

    case('duplicate label refused', c_duplicate_refused)

    def c_unknown_action_refused():
        try:
            parse([row('x', action='maybe')])
        except TableError:
            return
        raise AssertionError('an unknown action was accepted')

    case('unknown action refused', c_unknown_action_refused)

    def c_star_row():
        rules = parse([row('s', gap='*', files='*')])
        assert classify(rules, feat([], 0))['label'] == 's'

    case('all-star row accepts anything', c_star_row)

    def c_no_match_default():
        rules = parse([row('d', gap='depth-limited+', action='raise-depth')])
        assert classify(rules, feat()) is None

    case('no match -> default', c_no_match_default)

    failures = 0
    for name, fn in cases:
        try:
            fn()
            print('ok   %s' % name)
        except Exception as exc:                      # noqa: BLE001 - selftest report
            failures += 1
            print('FAIL %s: %s' % (name, exc))
    print('%d/%d passed' % (len(cases) - failures, len(cases)))
    return 0 if failures == 0 else 1


def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument('--skill')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--table-only', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('envelopes', nargs='*')
    ns = ap.parse_args(argv)
    try:
        if ns.selftest:
            return selftest()
        return run(ns)
    except (TableError, EnvelopeError) as exc:
        sys.stderr.write('sqfs-triage-v3: %s\n' % exc)
        return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
