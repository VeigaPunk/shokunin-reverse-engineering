#!/usr/bin/env python3
"""sqfs-triage-v2-min.py — MINIMAL pre-freeze validator/classifier for table v2.

Seat R40C2Shortcuts (round 40 wave 1) wrote this because the R40C2Interp seat's
`sqfs-triage-v2.py` did not exist when the controls were built.  It is NOT the frozen
interpreter: it implements the L1 contract grammar as written in the wave dispatch and
nothing else.  The frozen interpreter stays authoritative.

Surface read: one SKILL.md, plus envelopes.  It never invokes REA, unblob or sasquatch,
never reads a carrier, never writes anything.

Grammar implemented (wave-dispatch draft, verbatim intent)
----------------------------------------------------------
  * the table is the FIRST markdown table after a line containing
    ``<!-- sqfs-triage-table v2 -->`` inside the ``## Queue-drain craft`` section
    (that heading line up to the next ``## `` heading);
  * header, exact and in order:
      label | operation | provider | handler | gap kinds | dependencies |
      -be in child argv | symlink removed | published files | action | cause | source
  * rows are tried top to bottom, first full match gives (label, action);
    no match gives (``unclassified``, ``none``);
  * labels are unique per table (duplicate -> exit 2);
  * the action vocabulary is declared in a line
    ``<!-- sqfs-triage-actions: tok1 tok2 ... -->`` directly above the table
    (tolerated: the marker line may sit between the vocabulary line and the table);
    an action cell outside the vocabulary -> exit 2;
  * features, from a bare ``data`` object or a full ``{ok,data,meta}`` envelope:
      OP = data.operation
      PV = data.provider.id
      H  = {chunk.handler : startswith 'squashfs'}      (v1 rule)
      G  = {extraction_gaps[].kind}                      (v1 rule)
      D  = union extraction_gaps[].dependencies          (v1 rule)
      BE = yes/no/n-a from a recorded sasquatch argv     (v1 rule)
      SR = MaliciousSymlinkRemoved seen                  (v1 rule)
      P  = len(normalized_result.files)                  (v1 rule)
  * condition cells, after stripping whitespace and one pair of backticks:
      operation / provider   ``*`` or an exact string (case-sensitive)
      handler                ``*`` | ``none`` (no squashfs chunk) | fnmatch pattern
      gap kinds/dependencies ``*`` | ``none`` (empty set) | ``a+b`` exact set
      -be / symlink removed  ``yes`` | ``no`` | ``n/a`` | ``*``
      published files        ``0`` | ``>0`` | ``*``
      action                 one token from the declared vocabulary
      cause / source         non-empty prose (documentation only; no ``->`` required)
  * any malformed cell, header, separator, row width, duplicate label or unknown
    action is exit 2, never a silent non-match.

Usage
  python3 -I -B sqfs-triage-v2-min.py --skill SKILL.md ENVELOPE.json...
  python3 -I -B sqfs-triage-v2-min.py --skill SKILL.md --json ENVELOPE...
  python3 -I -B sqfs-triage-v2-min.py --skill SKILL.md --table-only
  python3 -I -B sqfs-triage-v2-min.py --selftest

Exit codes: 0 ok; 2 table missing/malformed, envelope unreadable, bad invocation.
``--selftest`` exits 0 iff every case passes, 1 otherwise.

Provenance: table parsing and envelope features are copied from the round-39 frozen
interpreter ``tools/round-39/sqfs-triage.py`` (blob b5c5379a) and extended with the
``operation`` and ``provider.id`` columns and the action vocabulary.  Keeping the v1
feature code byte-identical is deliberate: a v2 control must fail on the v2 grammar,
not on a re-implemented feature extractor.
"""

import argparse
import fnmatch
import json
import os
import shlex
import subprocess
import sys
import tempfile

MARKER = '<!-- sqfs-triage-table v2 -->'
ACTIONS_PREFIX = '<!-- sqfs-triage-actions:'
CRAFT_PREFIX = 'queue-drain craft'
HEADER = ['label', 'operation', 'provider', 'handler', 'gap kinds', 'dependencies',
          '-be in child argv', 'symlink removed', 'published files', 'action', 'cause',
          'source']
BE_VALUES = ('yes', 'no', 'n/a')
FILES_VALUES = ('0', '>0')
SYMLINK_TYPENAME = 'MaliciousSymlinkRemoved'
RESERVED_LABEL = 'unclassified'
RESERVED_ACTION = 'none'

SEPARATOR_RE = None
NAME_RE = None
HANDLER_RE = None
ACTION_RE = None


class TableError(Exception):
    """The triage table is missing or malformed."""


class EnvelopeError(Exception):
    """An envelope could not be read as an REA extract-firmware result."""


class InvocationError(Exception):
    """The command line does not select a readable surface."""


# --------------------------------------------------------------------------------------
# table parsing
# --------------------------------------------------------------------------------------

def _regexes():
    global SEPARATOR_RE, NAME_RE, HANDLER_RE, ACTION_RE
    if SEPARATOR_RE is None:
        import re
        SEPARATOR_RE = re.compile(r'^:?-+:?$')
        NAME_RE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.\-]*$')
        HANDLER_RE = re.compile(r'^[A-Za-z0-9_?*.\-\[\]]+$')
        ACTION_RE = re.compile(r'^[a-z0-9][a-z0-9\-]*$')
    return SEPARATOR_RE, NAME_RE, HANDLER_RE, ACTION_RE


def clean_cell(raw):
    s = raw.strip()
    if len(s) >= 2 and s[0] == '`' and s[-1] == '`' and s.count('`') == 2:
        s = s[1:-1].strip()
    return s


def _is_h2(line):
    return line.startswith('## ') and not line.startswith('### ')


def craft_bounds(lines):
    start = None
    for i, line in enumerate(lines):
        if _is_h2(line) and line[3:].strip().lower().startswith(CRAFT_PREFIX):
            start = i + 1
            break
    if start is None:
        raise TableError('no "## Queue-drain craft" heading in the document')
    end = len(lines)
    for j in range(start, len(lines)):
        if _is_h2(lines[j]):
            end = j
            break
    return start, end


def split_row(line):
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|'):
        s = s[:-1]
    return [c for c in s.split('|')]


def _parse_set_cell(cell, column):
    _, name_re, _, _ = _regexes()
    if cell in ('*', 'none'):
        return ('any', None) if cell == '*' else ('none', None)
    parts = cell.split('+')
    if any(not part for part in parts):
        raise TableError('%s cell %r has an empty set member' % (column, cell))
    for part in parts:
        if not name_re.match(part):
            raise TableError('%s cell %r has a malformed member %r'
                             % (column, cell, part))
    if len(set(parts)) != len(parts):
        raise TableError('%s cell %r repeats a member' % (column, cell))
    return ('exact', frozenset(parts))


def _parse_handler_cell(cell):
    _, _, handler_re, _ = _regexes()
    if cell == '*':
        return ('any', None)
    if cell == 'none':
        return ('none', None)
    if not handler_re.match(cell):
        raise TableError('handler cell %r is not *, none, or an fnmatch pattern' % cell)
    return ('pattern', cell)


def _parse_exact_cell(cell, column):
    _, name_re, _, _ = _regexes()
    if cell == '*':
        return ('any', None)
    if not name_re.match(cell):
        raise TableError('%s cell %r is not * or an exact identifier' % (column, cell))
    return ('exact', cell)


def _parse_enum_cell(cell, column, values):
    if cell == '*':
        return '*'
    if cell in values:
        return cell
    raise TableError('%s cell %r is not one of %s or *'
                     % (column, cell, ', '.join(values)))


def parse_actions(lines, marker_line, table_line):
    """Return (vocabulary, line_no) for the vocabulary line above the table."""
    _, _, _, action_re = _regexes()
    found = []
    for i in range(marker_line, table_line - 1):
        if ACTIONS_PREFIX in lines[i]:
            found.append(i)
    if not found:
        raise TableError('no %r vocabulary line between the marker and the table'
                         % ACTIONS_PREFIX)
    line_no = found[-1] + 1
    for j in range(found[-1] + 1, table_line - 1):
        text = lines[j].strip()
        if text and MARKER not in text and ACTIONS_PREFIX not in text:
            raise TableError('line %d: prose between the action vocabulary (line %d) and '
                             'the table (line %d); the vocabulary must sit directly above '
                             'the table' % (j + 1, line_no, table_line))
    line = lines[found[-1]]
    body = line.split(ACTIONS_PREFIX, 1)[1]
    if '-->' not in body:
        raise TableError('line %d: action vocabulary line has no closing -->' % line_no)
    tokens = body.split('-->', 1)[0].split()
    if not tokens:
        raise TableError('line %d: action vocabulary is empty' % line_no)
    if len(set(tokens)) != len(tokens):
        raise TableError('line %d: action vocabulary repeats a token' % line_no)
    for token in tokens:
        if not action_re.match(token):
            raise TableError('line %d: action token %r is not a lowercase token'
                             % (line_no, token))
        if token == RESERVED_ACTION:
            raise TableError('line %d: action token %r is reserved for the no-match result'
                             % (line_no, token))
    return frozenset(tokens), line_no


def parse_table(lines, first_line_no, vocabulary):
    """Parse the rows of one markdown table into rules.  TableError when malformed."""
    sep_re, _, _, _ = _regexes()
    if len(lines) < 3:
        raise TableError('table at line %d has no header, separator and data row'
                         % first_line_no)
    header = [clean_cell(c) for c in split_row(lines[0])]
    if [c.lower() for c in header] != [h.lower() for h in HEADER]:
        raise TableError('table at line %d: header is %r, expected %r'
                         % (first_line_no, header, HEADER))
    sep_cells = [clean_cell(c) for c in split_row(lines[1])]
    if len(sep_cells) != len(HEADER) or not all(sep_re.match(c) for c in sep_cells):
        raise TableError('table at line %d: second row is not a %d-cell markdown separator'
                         % (first_line_no + 1, len(HEADER)))
    rules = []
    seen = {}
    for offset, raw_line in enumerate(lines[2:], start=3):
        line_no = first_line_no + offset - 1
        cells = split_row(raw_line)
        if len(cells) != len(HEADER):
            raise TableError('table row at line %d has %d cells, expected %d'
                             % (line_no, len(cells), len(HEADER)))
        cells = [clean_cell(c) for c in cells]
        (label, operation, provider, handler, gap, dep, be, sr, files, action, cause,
         source) = cells
        if not label:
            raise TableError('line %d: empty label' % line_no)
        if label == RESERVED_LABEL:
            raise TableError('line %d: label %r is reserved for the no-match result'
                             % (line_no, RESERVED_LABEL))
        if label in seen:
            raise TableError('line %d: duplicate label %r (first at line %d)'
                             % (line_no, label, seen[label]))
        seen[label] = line_no
        if not action:
            raise TableError('line %d: empty action cell' % line_no)
        if action not in vocabulary:
            raise TableError('line %d: action %r is not in the declared vocabulary'
                             % (line_no, action))
        if not cause:
            raise TableError('line %d: empty cause cell' % line_no)
        if not source:
            raise TableError('line %d: empty source cell' % line_no)
        rules.append({
            'index': len(rules) + 1,
            'line': line_no,
            'label': label,
            'operation': _parse_exact_cell(operation, 'operation'),
            'provider': _parse_exact_cell(provider, 'provider'),
            'handler': _parse_handler_cell(handler),
            'gap_kinds': _parse_set_cell(gap, 'gap kinds'),
            'dependencies': _parse_set_cell(dep, 'dependencies'),
            'be': _parse_enum_cell(be, '-be in child argv', BE_VALUES),
            'symlink_removed': _parse_enum_cell(sr, 'symlink removed', BE_VALUES),
            'files': _parse_enum_cell(files, 'published files', FILES_VALUES),
            'action': action,
            'cause': cause,
            'source': source,
            'cells': cells,
        })
    if not rules:
        raise TableError('table at line %d has no rule rows' % first_line_no)
    return rules


def parse_skill(text):
    """Return (rules, vocabulary, info) for the craft-section v2 table."""
    lines = text.splitlines()
    start, end = craft_bounds(lines)
    marker_line = None
    for i in range(start, end):
        if MARKER in lines[i]:
            marker_line = i
            break
    if marker_line is None:
        raise TableError('marker %r absent from the craft section' % MARKER)
    i = marker_line + 1
    while i < end and not lines[i].lstrip().startswith('|'):
        i += 1
    if i >= end:
        raise TableError('no markdown table after the marker inside the craft section')
    table = []
    while i < end and lines[i].lstrip().startswith('|'):
        table.append(lines[i])
        i += 1
    table_line = i - len(table) + 1
    vocabulary, actions_line = parse_actions(lines, marker_line, table_line)
    rules = parse_table(table, table_line, vocabulary)
    return rules, vocabulary, {'marker_line': marker_line + 1, 'table_line': table_line,
                               'actions_line': actions_line, 'rules': len(rules)}


# --------------------------------------------------------------------------------------
# envelope features (copied from tools/round-39/sqfs-triage.py, + OP/PV)
# --------------------------------------------------------------------------------------

def _as_list(value):
    return value if isinstance(value, list) else []


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


def names_sasquatch(tokens):
    for token in tokens:
        if token.rsplit('/', 1)[-1].startswith('sasquatch'):
            return True
    return False


def extractor_commands(data):
    commands = []

    def take(cmd):
        tokens = command_tokens(cmd)
        if tokens and names_sasquatch(tokens) and cmd not in commands:
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
    if isinstance(obj.get('normalized_result'), dict):
        return obj
    inner = obj.get('data')
    if isinstance(inner, dict) and isinstance(inner.get('normalized_result'), dict):
        return inner
    raise EnvelopeError('%s: no normalized_result (neither a bare data object nor a '
                        'full {ok,data,meta} envelope)' % path)


def features(data):
    nr = data.get('normalized_result')
    if not isinstance(nr, dict):
        raise EnvelopeError('normalized_result is not an object')
    operation = data.get('operation')
    provider = data.get('provider')
    if isinstance(provider, dict):
        provider_id = provider.get('id')
    else:
        provider_id = provider
    handlers = set()
    for chunk in _as_list(nr.get('chunks')):
        handler = chunk.get('handler') if isinstance(chunk, dict) else None
        if isinstance(handler, str) and handler.startswith('squashfs'):
            handlers.add(handler)
    gap_kinds = set()
    dependencies = set()
    for gap in _as_list(nr.get('extraction_gaps')):
        if not isinstance(gap, dict):
            continue
        kind = gap.get('kind')
        if isinstance(kind, str):
            gap_kinds.add(kind)
        for dep in _as_list(gap.get('dependencies')):
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
    return {
        'OP': operation if isinstance(operation, str) else None,
        'PV': provider_id if isinstance(provider_id, str) else None,
        'H': sorted(handlers),
        'G': sorted(gap_kinds),
        'D': sorted(dependencies),
        'BE': be,
        'SR': symlink,
        'P': len(_as_list(nr.get('files'))),
        'commands': [cmd if isinstance(cmd, str) else list(cmd) for cmd in commands],
    }


def load_envelope(path):
    try:
        with open(path, 'r', encoding='utf-8') as handle:
            obj = json.load(handle)
    except OSError as exc:
        raise EnvelopeError('%s: %s' % (path, exc.strerror or exc))
    except ValueError as exc:
        raise EnvelopeError('%s: not valid JSON (%s)' % (path, exc))
    return features(envelope_data(obj, path))


# --------------------------------------------------------------------------------------
# classification
# --------------------------------------------------------------------------------------

def match_set(spec, values):
    kind, payload = spec
    if kind == 'any':
        return True
    if kind == 'none':
        return not values
    return frozenset(values) == payload


def rule_matches(rule, feat):
    kind, payload = rule['operation']
    if kind == 'exact' and feat['OP'] != payload:
        return False
    kind, payload = rule['provider']
    if kind == 'exact' and feat['PV'] != payload:
        return False
    kind, payload = rule['handler']
    if kind == 'none':
        if feat['H']:
            return False
    elif kind == 'pattern':
        if not any(fnmatch.fnmatchcase(value, payload) for value in feat['H']):
            return False
    if not match_set(rule['gap_kinds'], feat['G']):
        return False
    if not match_set(rule['dependencies'], feat['D']):
        return False
    if rule['be'] != '*' and rule['be'] != feat['BE']:
        return False
    if rule['symlink_removed'] != '*' and rule['symlink_removed'] != feat['SR']:
        return False
    files = rule['files']
    if files == '0' and feat['P'] != 0:
        return False
    if files == '>0' and feat['P'] <= 0:
        return False
    return True


def classify(rules, feat):
    for rule in rules:
        if rule_matches(rule, feat):
            return rule
    return None


# --------------------------------------------------------------------------------------
# command line
# --------------------------------------------------------------------------------------

def _read_skill(path):
    try:
        with open(path, 'r', encoding='utf-8') as handle:
            return handle.read()
    except OSError as exc:
        raise TableError('%s: %s' % (path, exc.strerror or exc))


def _print_rules(skill, rules, vocabulary, info):
    print('skill: %s' % skill)
    print('marker line: %d  actions line: %d  table line: %d  rules: %d'
          % (info['marker_line'], info['actions_line'], info['table_line'],
             info['rules']))
    print('actions: %s' % ' '.join(sorted(vocabulary)))
    for rule in rules:
        print('%d. %s -> %s' % (rule['index'], rule['label'], rule['action']))
        print('   operation=%r provider=%r handler=%r gap_kinds=%r dependencies=%r'
              % (rule['operation'], rule['provider'], rule['handler'],
                 rule['gap_kinds'], rule['dependencies']))
        print('   be=%r symlink_removed=%r files=%r' % (rule['be'],
                                                        rule['symlink_removed'],
                                                        rule['files']))
        print('   cause: %s' % rule['cause'])
        print('   source: %s' % rule['source'])


def _run(ns):
    if not ns.skill:
        raise InvocationError('--skill is required with envelopes or --table-only')
    text = _read_skill(ns.skill)
    rules, vocabulary, info = parse_skill(text)
    if ns.table_only:
        _print_rules(ns.skill, rules, vocabulary, info)
        return 0
    if not ns.envelopes:
        raise InvocationError('no envelope given')
    results = []
    for path in ns.envelopes:
        feat = load_envelope(path)
        rule = classify(rules, feat)
        results.append((path, feat, rule))
    if ns.json:
        payload = {
            'skill': ns.skill,
            'rules': info['rules'],
            'actions': sorted(vocabulary),
            'results': [{
                'path': path,
                'label': rule['label'] if rule else 'unclassified',
                'action': rule['action'] if rule else 'none',
                'rule': rule['index'] if rule else None,
                'row': list(rule['cells']) if rule else None,
                'features': feat,
            } for path, feat, rule in results],
        }
        json.dump(payload, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write('\n')
        return 0
    for path, _feat, rule in results:
        print('%s\t%s\t%s' % (path, rule['label'] if rule else 'unclassified',
                              rule['action'] if rule else 'none'))
    return 0


# --------------------------------------------------------------------------------------
# selftest (proves this validator can fail)
# --------------------------------------------------------------------------------------

ACTIONS = ('<!-- sqfs-triage-actions: a b c -->')
SKELETON = ('# SKILL\n\n## Queue-drain craft\n\nProse before.\n\n{block}\n\n'
            '## A later section\n\nProse after.\n')
HEAD = ('| label | operation | provider | handler | gap kinds | dependencies | '
        '-be in child argv | symlink removed | published files | action | cause | '
        'source |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | '
        '--- |\n')


def _block(rows, marker=True, actions=ACTIONS):
    out = []
    if marker:
        out.append(MARKER)
    if actions:
        out.append(actions)
    out.append(HEAD.rstrip('\n'))
    out.extend(rows)
    return '\n'.join(out) + '\n'


def _row(label, op='*', pv='*', handler='*', gaps='*', deps='*', be='*', sr='*',
         files='*', action='a', cause='cause prose', source='selftest'):
    return '| %s |' % ' | '.join([label, op, pv, handler, gaps, deps, be, sr, files,
                                  action, cause, source])


CASES = []


def case(fn):
    CASES.append(fn)
    return fn


def _cli(args):
    return subprocess.run([sys.executable, '-I', '-B', os.path.abspath(__file__), *args],
                          capture_output=True, text=True)


def _require(cond, message):
    if not cond:
        raise AssertionError(message)


def _write(work, name, text):
    path = os.path.join(work, name)
    with open(path, 'w', encoding='utf-8') as handle:
        handle.write(text)
    return path


def _env(work, name, op='extract_firmware', pv='unblob', handler='squashfs_v4_be',
         gaps=(), deps=(), be=None, sr=False, files=1):
    nr = {'chunks': [{'handler': handler}] if handler else [],
          'extraction_gaps': [{'kind': k, 'dependencies': list(deps)} for k in gaps],
          'files': [{'path': 'f%d' % i} for i in range(files)],
          'diagnostics': []}
    if be is not None:
        cmd = ['/x/sasquatch-v4be', '-f', '-d'] + (['-be'] if be else []) + ['img', 'out']
        nr['diagnostics'].append({'report': {'__typename__': 'ExtractorRan',
                                            'command': cmd}})
    if sr:
        nr['diagnostics'].append({'report': {'__typename__': SYMLINK_TYPENAME}})
    data = {'operation': op, 'provider': {'id': pv, 'name': 'X', 'version': '1'},
            'normalized_result': nr}
    return _write(work, name, json.dumps({'ok': True, 'data': data, 'meta': {}}))


@case
def c_green(work):
    path = _write(work, 'sk.md', SKELETON.format(block=_block(
        [_row('clean', op='extract_firmware', pv='unblob', handler='squashfs_v4_*',
              gaps='none', deps='none', sr='no', files='>0')])))
    res = _cli(['--skill', path, '--table-only'])
    _require(res.returncode == 0, 'green: exit %d (%r)' % (res.returncode, res.stderr))
    _require('rules: 1' in res.stdout, 'green: rule count missing')


@case
def c_no_marker(work):
    path = _write(work, 'sk.md', SKELETON.format(block=_block([_row('x')], marker=False)))
    res = _cli(['--skill', path, '--table-only'])
    _require(res.returncode == 2 and 'marker' in res.stderr,
             'no-marker: exit %d stderr %r' % (res.returncode, res.stderr))


@case
def c_duplicate_label(work):
    path = _write(work, 'sk.md', SKELETON.format(block=_block(
        [_row('x'), _row('x', files='>0')])))
    res = _cli(['--skill', path, '--table-only'])
    _require(res.returncode == 2 and 'duplicate' in res.stderr,
             'duplicate-label: exit %d stderr %r' % (res.returncode, res.stderr))


@case
def c_unknown_action(work):
    path = _write(work, 'sk.md', SKELETON.format(block=_block([_row('x', action='zzz')])))
    res = _cli(['--skill', path, '--table-only'])
    _require(res.returncode == 2 and 'vocabulary' in res.stderr,
             'unknown-action: exit %d stderr %r' % (res.returncode, res.stderr))


@case
def c_missing_actions_line(work):
    path = _write(work, 'sk.md', SKELETON.format(block=_block([_row('x')], actions=None)))
    res = _cli(['--skill', path, '--table-only'])
    _require(res.returncode == 2 and 'sqfs-triage-actions' in res.stderr,
             'no-actions-line: exit %d stderr %r' % (res.returncode, res.stderr))


@case
def c_bad_header(work):
    head = HEAD.replace('| action |', '| actions |')
    path = _write(work, 'sk.md', SKELETON.format(
        block='\n'.join([MARKER, ACTIONS, head.rstrip('\n'), _row('x')]) + '\n'))
    res = _cli(['--skill', path, '--table-only'])
    _require(res.returncode == 2 and 'header' in res.stderr,
             'bad-header: exit %d stderr %r' % (res.returncode, res.stderr))


@case
def c_bad_file_cell(work):
    path = _write(work, 'sk.md', SKELETON.format(block=_block([_row('x', files='many')])))
    res = _cli(['--skill', path, '--table-only'])
    _require(res.returncode == 2 and 'published files' in res.stderr,
             'bad-file-cell: exit %d stderr %r' % (res.returncode, res.stderr))


@case
def c_domain_guard(work):
    path = _write(work, 'sk.md', SKELETON.format(block=_block(
        [_row('clean', op='extract_firmware', pv='unblob', handler='squashfs_v4_*',
              gaps='none', deps='none', sr='no', files='>0')])))
    good = _env(work, 'good.json')
    bad = _env(work, 'bad.json', op='binary_overview')
    res = _cli(['--skill', path, '--json', good, bad])
    _require(res.returncode == 0, 'domain: exit %d (%r)' % (res.returncode, res.stderr))
    payload = json.loads(res.stdout)
    _require(payload['results'][0]['label'] == 'clean', 'domain: in-domain label')
    _require(payload['results'][1]['label'] == 'unclassified'
             and payload['results'][1]['action'] == 'none', 'domain: fall-through')


@case
def c_first_match(work):
    path = _write(work, 'sk.md', SKELETON.format(block=_block(
        [_row('first', files='>0'), _row('second', files='*')])))
    env = _env(work, 'e.json')
    res = _cli(['--skill', path, env])
    _require(res.returncode == 0, 'first-match: exit %d' % res.returncode)
    _require(res.stdout.strip().split('\t')[1:] == ['first', 'a'],
             'first-match: %r' % res.stdout)


def selftest():
    work = tempfile.mkdtemp(dir=os.environ.get('TMPDIR') or None, prefix='triage2min.')
    passed = 0
    try:
        for fn in CASES:
            try:
                fn(work)
            except AssertionError as exc:
                print('FAIL %s: %s' % (fn.__name__, exc))
            else:
                passed += 1
                print('ok   %s' % fn.__name__)
    finally:
        import shutil
        shutil.rmtree(work, ignore_errors=True)
    print('cases %d, passed %d' % (len(CASES), passed))
    return 0 if passed == len(CASES) else 1


# --------------------------------------------------------------------------------------
# entry point
# --------------------------------------------------------------------------------------

def main(argv=None):
    parser = argparse.ArgumentParser(
        description='Minimal pre-freeze validator for the SquashFS triage table v2.')
    parser.add_argument('--skill', help='SKILL.md carrying the v2 table')
    parser.add_argument('--json', action='store_true', help='print features as JSON')
    parser.add_argument('--table-only', action='store_true',
                        help='validate and print the parsed rules')
    parser.add_argument('--selftest', action='store_true', help='run the selftest')
    parser.add_argument('envelopes', nargs='*', help='REA extract-firmware envelopes')
    ns = parser.parse_args(argv)
    if ns.selftest:
        return selftest()
    try:
        return _run(ns)
    except (TableError, EnvelopeError, InvocationError) as exc:
        sys.stderr.write('sqfs-triage-v2-min: %s\n' % exc)
        return 2


if __name__ == '__main__':
    sys.exit(main())
