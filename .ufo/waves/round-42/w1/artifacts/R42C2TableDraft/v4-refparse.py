#!/usr/bin/env python3
r"""v4-refparse.py — reference reader for the drafted SquashFS triage table v4.

This is a WAVE-1 REFERENCE instrument for the draft in `block21.md`, not the frozen
interpreter (that is `tools/round-42/sqfs-triage-v4.py`, another seat).  It exists so the
draft can be parsed and executed before the freeze, and so the drafted grammar deltas can
be shown to be decidable.  It reads only a SKILL.md-shaped document and REA envelopes,
writes nothing, and never invokes REA, unblob or sasquatch.

Grammar, stated against the frozen v3 reader (`tools/round-41/sqfs-triage-v3.py`):

  same    columns and order, markdown separator, action vocabulary line directly above
          the table, backtick stripping, duplicate-label refusal, `cause` must hold `->`,
          `source` non-empty, gap-kinds exact (`a+b`) and contains (`a+`, `a,b+`) forms,
          `-be`/`symlink removed` in {yes,no,n/a,*}, `published files` in {0,>0,*},
          first-match-wins, no match -> (unclassified, none), no embedded table copy.

  delta 1 marker `<!-- sqfs-triage-table v4 -->`; a craft section whose only markers are
          v1/v2/v3 is refused with exit 2.
  delta 2 `dependencies` accepts the contains form as well (`sasquatch-v4be+`), because
          the precedence's dependency clauses are membership, not set equality.
  delta 3 a THIRTEENTH column, `failing handler`, sits right after `handler`.  `handler`
          is a glob over `F` — the members of `H` that start `squashfs_`, with `H` read from
          `chunks[].handler` UNION `extraction_gaps[].handler` (nulls dropped), the
          precedence text's `H`; `none` means `F` is empty.  `failing handler` is a glob
          over `HF` — the handlers of the `extractor-failure` gaps, or `F` when none of
          them carries one; `*` matches anything, an empty `HF` included.  A pattern may
          use an fnmatch character class (`squashfs_v[123]*`), which the v3 reader's
          handler-cell regex already permits.

Usage
  python3 -I -B v4-refparse.py --skill SKILL.md --table-only
  python3 -I -B v4-refparse.py --skill SKILL.md --json ENVELOPE.json...
  python3 -I -B v4-refparse.py --selftest
Exit codes: 0 ok, 2 table missing/refused/malformed or envelope unreadable, 1 selftest failure.
"""
from __future__ import annotations

import fnmatch
import json
import re
import shlex
import sys

MARKER = '<!-- sqfs-triage-table v4 -->'
REFUSED = ('<!-- sqfs-triage-table v3 -->', '<!-- sqfs-triage-table v2 -->',
           '<!-- sqfs-triage-table v1 -->')
ACTIONS_PREFIX = '<!-- sqfs-triage-actions:'
ACTIONS_SUFFIX = '-->'
CRAFT_PREFIX = 'queue-drain craft'
HEADER = ['label', 'operation', 'provider', 'handler', 'failing handler', 'gap kinds',
          'dependencies', '-be in child argv', 'symlink removed', 'published files',
          'action', 'cause', 'source']
BE_VALUES = ('yes', 'no', 'n/a')
FILES_VALUES = ('0', '>0')
RESERVED = ('none', '*')
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


# --------------------------------------------------------------------------- table
def clean_cell(raw):
    s = raw.strip()
    if len(s) >= 2 and s[0] == '`' and s[-1] == '`' and s.count('`') == 2:
        s = s[1:-1].strip()
    return s


def is_h2(line):
    return line.startswith('## ') and not line.startswith('### ')


def craft_bounds(lines):
    start = None
    for i, line in enumerate(lines):
        if is_h2(line) and line[3:].strip().lower().startswith(CRAFT_PREFIX):
            start = i + 1
            break
    if start is None:
        raise TableError('no "## Queue-drain craft" heading')
    end = len(lines)
    for j in range(start, len(lines)):
        if is_h2(lines[j]):
            end = j
            break
    return start, end


def split_row(line):
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|'):
        s = s[:-1]
    return s.split('|')


def parse_set_cell(cell, column, contains):
    if cell in RESERVED:
        return ('any', None) if cell == '*' else ('none', None)
    if contains and cell.endswith('+'):
        parts = cell[:-1].split(',')
        if any(not p for p in parts):
            raise TableError('%s cell %r has an empty contains member' % (column, cell))
        for p in parts:
            if not NAME_RE.match(p):
                raise TableError('%s cell %r: malformed member %r' % (column, cell, p))
            if p in RESERVED:
                raise TableError('%s cell %r: reserved member %r' % (column, cell, p))
        if len(set(parts)) != len(parts):
            raise TableError('%s cell %r repeats a member' % (column, cell))
        return ('contains', frozenset(parts))
    parts = cell.split('+')
    if any(not p for p in parts):
        raise TableError('%s cell %r has an empty member' % (column, cell))
    for p in parts:
        if not NAME_RE.match(p):
            raise TableError('%s cell %r: malformed member %r' % (column, cell, p))
        if p in RESERVED:
            raise TableError('%s cell %r: reserved member %r' % (column, cell, p))
    if len(set(parts)) != len(parts):
        raise TableError('%s cell %r repeats a member' % (column, cell))
    return ('exact', frozenset(parts))


def parse_handler(cell, column='handler'):
    if cell == '*':
        return ('any', None, column)
    if cell == 'none':
        return ('none', None, column)
    if not HANDLER_RE.match(cell):
        raise TableError('%s cell %r is not *, none, or an fnmatch pattern'
                         % (column, cell))
    return ('pattern', cell, column)


def parse_domain(cell, column, rx):
    if cell == '*':
        return '*'
    if not rx.match(cell):
        raise TableError('%s cell %r is not * or a bare token' % (column, cell))
    return cell


def parse_enum(cell, column, values):
    if cell != '*' and cell not in values:
        raise TableError('%s cell %r is not one of %s or *'
                         % (column, cell, ', '.join(values)))
    return cell


def parse_actions(line, line_no):
    s = line.strip()
    at = s.find(ACTIONS_PREFIX)
    if at < 0:
        raise TableError('line %d: no vocabulary line directly above the table' % line_no)
    rest = s[at + len(ACTIONS_PREFIX):]
    if ACTIONS_SUFFIX not in rest:
        raise TableError('line %d: vocabulary line has no closing %r' % (line_no,
                                                                        ACTIONS_SUFFIX))
    rest = rest[:rest.index(ACTIONS_SUFFIX)].strip()
    if not rest:
        raise TableError('line %d: empty vocabulary' % line_no)
    seen = []
    for token in rest.split():
        if not ACTION_RE.match(token):
            raise TableError('line %d: action %r is not a lowercase dashed token'
                             % (line_no, token))
        if token in seen:
            raise TableError('line %d: action %r declared twice' % (line_no, token))
        seen.append(token)
    return seen


def parse_table(lines, first_line_no, vocabulary):
    if len(lines) < 3:
        raise TableError('table at line %d has no header, separator and row' % first_line_no)
    header = [clean_cell(c) for c in split_row(lines[0])]
    if [c.lower() for c in header] != [h.lower() for h in HEADER]:
        raise TableError('table at line %d: header %r != %r'
                         % (first_line_no, header, HEADER))
    sep = [clean_cell(c) for c in split_row(lines[1])]
    if len(sep) != len(HEADER) or not all(SEP_RE.match(c) for c in sep):
        raise TableError('table at line %d: bad separator row' % (first_line_no + 1))
    rules, labels = [], {}
    for offset, raw in enumerate(lines[2:], start=3):
        line_no = first_line_no + offset - 1
        cells = split_row(raw)
        if len(cells) != len(HEADER):
            raise TableError('row at line %d has %d cells, expected %d'
                             % (line_no, len(cells), len(HEADER)))
        cells = [clean_cell(c) for c in cells]
        (label, op, prov, handler, failing, gap, dep, be, sr, files, action, cause,
         source) = cells
        if not label or not NAME_RE.match(label):
            raise TableError('line %d: label %r is not a bare token' % (line_no, label))
        if label in labels:
            raise TableError('line %d: duplicate label %r' % (line_no, label))
        labels[label] = line_no
        if action not in vocabulary:
            raise TableError('line %d: action %r not in the vocabulary line'
                             % (line_no, action))
        if not cause or '->' not in cause:
            raise TableError('line %d: cause cell is empty or has no "->"' % line_no)
        if not source:
            raise TableError('line %d: empty source cell' % line_no)
        rules.append({
            'index': len(rules) + 1, 'line': line_no, 'label': label,
            'operation': parse_domain(op, 'operation', OPERATION_RE),
            'provider': parse_domain(prov, 'provider', PROVIDER_RE),
            'handler': parse_handler(handler),
            'failing_handler': parse_handler(failing, 'failing handler'),
            'gap_kinds': parse_set_cell(gap, 'gap kinds', contains=True),
            'dependencies': parse_set_cell(dep, 'dependencies', contains=True),
            'be': parse_enum(be, '-be in child argv', BE_VALUES),
            'symlink_removed': parse_enum(sr, 'symlink removed', BE_VALUES),
            'files': parse_enum(files, 'published files', FILES_VALUES),
            'action': action, 'cells': cells,
        })
    if not rules:
        raise TableError('table at line %d has no rows' % first_line_no)
    return rules


def parse_skill(text):
    lines = text.splitlines()
    start, end = craft_bounds(lines)
    marker = None
    for i in range(start, end):
        if MARKER in lines[i]:
            marker = i
            break
    if marker is None:
        for refused in REFUSED:
            for i in range(start, end):
                if refused in lines[i]:
                    raise TableError('line %d: refused marker %r; this reader takes only '
                                     '%r' % (i + 1, refused, MARKER))
        raise TableError('marker %r absent from the craft section' % MARKER)
    table_start = None
    for i in range(marker + 1, end):
        if lines[i].lstrip().startswith('|'):
            table_start = i
            break
    if table_start is None:
        raise TableError('no markdown table after the marker')
    actions_line = table_start - 1
    while actions_line > start and not lines[actions_line].strip():
        actions_line -= 1
    if actions_line < start or ACTIONS_PREFIX not in lines[actions_line]:
        raise TableError('line %d: no vocabulary line directly above the table'
                         % (table_start + 1))
    vocabulary = parse_actions(lines[actions_line], actions_line + 1)
    table = []
    i = table_start
    while i < end and lines[i].lstrip().startswith('|'):
        table.append(lines[i])
        i += 1
    rules = parse_table(table, table_start + 1, vocabulary)
    return rules, {'marker_line': marker + 1, 'actions_line': actions_line + 1,
                   'table_line': table_start + 1, 'rules': len(rules),
                   'actions': vocabulary}


# --------------------------------------------------------------------------- features
def _as_list(v):
    return v if isinstance(v, list) else []


def _iter_dicts(obj):
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
        if tokens and any(t.rsplit('/', 1)[-1].startswith('sasquatch') for t in tokens):
            if cmd not in commands:
                commands.append(cmd)

    nr = data.get('normalized_result')
    nr = nr if isinstance(nr, dict) else {}
    for source in (nr.get('diagnostics'), data.get('diagnostics')):
        for diag in _as_list(source):
            report = diag.get('report') if isinstance(diag, dict) else None
            if isinstance(report, dict) and 'command' in report:
                take(report['command'])
    for found in _iter_dicts(data.get('raw_result')):
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
        raise EnvelopeError('%s: no normalized_result object and no operation string' % path)
    if 'normalized_result' in candidate and not isinstance(candidate['normalized_result'],
                                                           dict):
        raise EnvelopeError('%s: normalized_result is not an object' % path)
    op = candidate.get('operation')
    if not isinstance(candidate.get('normalized_result'), dict) and not isinstance(op, str):
        raise EnvelopeError('%s: neither normalized_result nor operation' % path)
    if op == OPERATION_TOKEN and not isinstance(candidate.get('normalized_result'), dict):
        raise EnvelopeError('%s: an extract_firmware envelope has no normalized_result'
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
    nr = data.get('normalized_result') if isinstance(data.get('normalized_result'),
                                                     dict) else {}
    handlers = set()
    for chunk in _as_list(nr.get('chunks')):
        h = chunk.get('handler') if isinstance(chunk, dict) else None
        if isinstance(h, str) and h.startswith('squashfs'):
            handlers.add(h)
    gaps = [g for g in _as_list(nr.get('extraction_gaps')) if isinstance(g, dict)]
    for gap in gaps:                       # delta 3: H is chunks UNION gap handlers
        h = gap.get('handler')
        if isinstance(h, str) and h.startswith('squashfs'):
            handlers.add(h)
    gap_kinds, deps, failing = set(), set(), set()
    for gap in gaps:
        kind = gap.get('kind')
        if isinstance(kind, str):
            gap_kinds.add(kind)
        if kind == 'extractor-failure':
            h = gap.get('handler')
            if isinstance(h, str) and h.startswith('squashfs'):
                failing.add(h)
        for dep in _as_list(gap.get('dependencies')):
            if isinstance(dep, str):
                deps.add(dep)
    commands = extractor_commands(data)
    if not commands:
        be = 'n/a'
    else:
        be = 'yes' if any('-be' in (command_tokens(c) or []) for c in commands) else 'no'
    symlink = 'no'
    for diag in _as_list(nr.get('diagnostics')):
        report = diag.get('report') if isinstance(diag, dict) else None
        if isinstance(report, dict) and report.get('__typename__') == SYMLINK_TYPENAME:
            symlink = 'yes'
            break
    if symlink == 'no':
        for found in _iter_dicts(data.get('raw_result')):
            if found.get('__typename__') == SYMLINK_TYPENAME:
                symlink = 'yes'
                break
    fam = sorted(h for h in handlers if h.startswith('squashfs_'))
    return {'OP': operation, 'PR': provider_id,
            'H': sorted(handlers),
            'F': fam,
            'L': [h for h in fam if h.startswith(('squashfs_v1', 'squashfs_v2',
                                                 'squashfs_v3'))],
            'HF': sorted(failing) or fam,
            'G': sorted(gap_kinds), 'D': sorted(deps), 'BE': be, 'SR': symlink,
            'P': len(_as_list(nr.get('files'))),
            'HFAIL': sorted(failing),
            'commands': [c if isinstance(c, str) else list(c) for c in commands]}


def load_envelope(path):
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            obj = json.load(fh)
    except OSError as exc:
        raise EnvelopeError('%s: %s' % (path, exc.strerror or exc))
    except ValueError as exc:
        raise EnvelopeError('%s: not valid JSON (%s)' % (path, exc))
    return features(envelope_data(obj, path))


# --------------------------------------------------------------------------- matching
def match_set(spec, values):
    kind, payload = spec
    if kind == 'any':
        return True
    if kind == 'none':
        return not values
    if kind == 'contains':
        return payload <= frozenset(values)
    return frozenset(values) == payload


def rule_matches(rule, feat):
    if rule['operation'] != '*' and rule['operation'] != feat['OP']:
        return False
    if rule['provider'] != '*' and rule['provider'] != feat['PR']:
        return False
    for column, feat_name in (('handler', 'F'), ('failing_handler', 'HF')):
        kind, payload, _ = rule[column]
        if kind == 'none':
            if feat.get(feat_name):
                return False
        elif kind == 'pattern':
            values = feat.get(feat_name) or []
            if not any(fnmatch.fnmatchcase(v, payload) for v in values):
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


def decision(rule):
    if rule is None:
        return DEFAULT_LABEL, DEFAULT_ACTION, None
    return rule['label'], rule['action'], rule['index']


# --------------------------------------------------------------------------- cli
def read_skill(path):
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            return fh.read()
    except OSError as exc:
        raise TableError('%s: %s' % (path, exc.strerror or exc))


def spec_text(spec):
    kind, payload, scope = spec
    if kind in ('any', 'none'):
        return kind
    return '%s:%s{%s}' % (scope, kind, payload)


def print_rules(skill, rules, info):
    print('skill: %s' % skill)
    print('marker line: %d  actions line: %d  table line: %d  rules: %d'
          % (info['marker_line'], info['actions_line'], info['table_line'],
             info['rules']))
    print('actions (%d): %s' % (len(info['actions']), ' '.join(info['actions'])))
    for rule in rules:
        print('%d. %s  (line %d)' % (rule['index'], rule['label'], rule['line']))
        print('   operation=%r provider=%r handler=%r failing=%r gap_kinds=%s '
              'dependencies=%s'
              % (rule['operation'], rule['provider'], rule['handler'],
                 rule['failing_handler'], spec_text(rule['gap_kinds']),
                 spec_text(rule['dependencies'])))
        print('   be=%r symlink_removed=%r files=%r action=%r'
              % (rule['be'], rule['symlink_removed'], rule['files'], rule['action']))


def selftest():
    """Refusals and parses of small inline documents.  Prints one ok line per case."""
    import os
    import tempfile
    ok = 0
    fail = 0

    cells = ['clean', '`extract_firmware`', '`unblob`', '`squashfs_*`', '`*`',
             '`none`', '`*`', '`*`', '`*`', '`>0`', '`none`', 'x -> y', 's']
    assert len(cells) == len(HEADER)

    def variant(**over):
        row = list(cells)
        for col, value in over.items():
            row[HEADER.index(col)] = value
        return ('  <!-- sqfs-triage-table v4 -->\n'
                '  <!-- sqfs-triage-actions: none a-token -->\n'
                '  | ' + ' | '.join(HEADER) + ' |\n'
                '  | ' + ' | '.join(['---'] * len(HEADER)) + ' |\n'
                '  | ' + ' | '.join(row) + ' |\n')

    def doc(block):
        return ('# t\n\n## Queue-drain craft (rounds 5-12)\n\n' + block +
                '\n## Config custody\n')

    good = variant()
    cases = [
        ('good', good, 0),
        ('v3-only-refused', good.replace('table v4', 'table v3'), 2),
        ('no-marker', good.replace('<!-- sqfs-triage-table v4 -->', ''), 2),
        ('dep-contains-ok', variant(**{'gap kinds': '`missing-extractor-dependency+`',
                                       'dependencies': '`sasquatch+`'}), 0),
        ('handler-class-ok', variant(**{'handler': '`squashfs_v[123]*`'}), 0),
        ('failing-handler-class-ok',
         variant(**{'failing handler': '`squashfs_v[123]*`'}), 0),
        ('twelve-cells-refused', good.replace(' | `*` | `none`', ' | `none`', 1), 2),
        ('cause-without-arrow', good.replace('x -> y', 'x to y'), 2),
        ('unknown-action', good.replace('| `none` | x -> y', '| `nope` | x -> y'), 2),
        ('duplicate-label', good + good.split('\n', 4)[4], 2),
    ]

    for name, block, expect in cases:
        with tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR') or None) as td:
            path = os.path.join(td, 'SKILL.md')
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(doc(block))
            try:
                parse_skill(read_skill(path))
                got = 0
            except TableError:
                got = 2
        if got == expect:
            ok += 1
            print('ok   %-32s exit %d' % (name, got))
        else:
            fail += 1
            print('FAIL %-32s exit %d, expected %d' % (name, got, expect))

    rules, _ = parse_skill(doc(good))
    feat = {'OP': 'extract_firmware', 'PR': 'unblob', 'H': ['squashfs_v3'],
            'F': ['squashfs_v3'], 'L': ['squashfs_v3'], 'HF': ['squashfs_v3'],
            'G': [], 'D': [], 'BE': 'n/a', 'SR': 'no', 'P': 2, 'commands': []}
    if decision(classify(rules, feat))[:2] == ('clean', 'none'):
        ok += 1
        print('ok   %-32s %s' % ('match-single-row', decision(classify(rules, feat))[:2]))
    else:
        fail += 1
        print('FAIL match-single-row')
    if decision(classify(rules, dict(feat, OP='inspect_firmware_regions')))[:2] == \
            ('unclassified', 'none'):
        ok += 1
        print('ok   %-32s domain guard' % 'domain-mismatch')
    else:
        fail += 1
        print('FAIL domain-mismatch')
    print('cases: %d, failures: %d' % (ok, fail))
    return 0 if fail == 0 else 1


def main(argv):
    import argparse
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument('--skill')
    ap.add_argument('--table-only', action='store_true')
    ap.add_argument('--json', nargs='*', default=[])
    ap.add_argument('--selftest', action='store_true')
    ns = ap.parse_args(argv)
    try:
        if ns.selftest:
            return selftest()
        if not ns.skill:
            print('--skill is required', file=sys.stderr)
            return 2
        rules, info = parse_skill(read_skill(ns.skill))
        if ns.table_only:
            print_rules(ns.skill, rules, info)
            return 0
        if not ns.json:
            print('no envelope given', file=sys.stderr)
            return 2
        for path in ns.json:
            feat = load_envelope(path)
            label, action, idx = decision(classify(rules, feat))
            print('%s\t%s\t%s\t%s' % (path, label, action, idx if idx else '-'))
        return 0
    except (TableError, EnvelopeError) as exc:
        print('error: %s' % exc, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
