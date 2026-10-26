#!/usr/bin/env python3
"""sqfs-triage-v2-dev.py -- DEV implementation of the L1's table-v2 grammar.

Not the frozen tool: this file is recon evidence for the round-40 freeze.  It
implements the contract exactly as drafted by the L1 (see the report section
"contract audit"), so the L1 can lift it into tools/round-40/sqfs-triage-v2.py
or diff it against their own.

Table shape (inside SKILL.md's "## Queue-drain craft" section, from the heading
line to the next "## " heading):

    <!-- sqfs-triage-table v2 -->
    ...
    <!-- sqfs-triage-actions: tok1 tok2 ... -->     <- directly above the table
    | label | operation | provider | handler | gap kinds | dependencies |
      -be in child argv | symlink removed | published files | action | cause | source |
    |---|...|

Reads nothing but the table and one envelope.  Envelope shapes accepted: a
bare ``data`` object and a full ``{"ok":..,"data":..,"meta":..}`` envelope.

Exit: 0 classified (or table-only/selftest ok), 2 malformed table, malformed
cell, duplicate label, unknown action, unusable envelope, or no table.
"""

import argparse
import fnmatch
import json
import os
import re
import shlex
import sys
import tempfile

MARKER = '<!-- sqfs-triage-table v2 -->'
ACTIONS_PREFIX = '<!-- sqfs-triage-actions:'
ACTIONS_SUFFIX = '-->'
CRAFT_PREFIX = 'queue-drain craft'
HEADER = ['label', 'operation', 'provider', 'handler', 'gap kinds',
          'dependencies', '-be in child argv', 'symlink removed',
          'published files', 'action', 'cause', 'source']
BE_VALUES = ('yes', 'no', 'n/a')
FILES_VALUES = ('0', '>0')
SYMLINK_TYPENAME = 'MaliciousSymlinkRemoved'


class TableError(Exception):
    pass


class EnvelopeError(Exception):
    pass


# ---------------------------------------------------------------------------
# table parsing
# ---------------------------------------------------------------------------
NAME_RE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.\-]*$')
ACTION_RE = re.compile(r'^[a-z][a-z0-9\-]*$')
PATTERN_RE = re.compile(r'^[A-Za-z0-9_?*.\-\[\]]+$')
SEPARATOR_RE = re.compile(r'^:?-+:?$')


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
        raise TableError('no "## Queue-drain craft" heading in the document')
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


def parse_set_cell(cell, column):
    if cell == '*':
        return ('any', None)
    if cell == 'none':
        return ('none', None)
    parts = cell.split('+')
    if any(not part for part in parts):
        raise TableError('%s cell %r has an empty set member' % (column, cell))
    for part in parts:
        if not NAME_RE.match(part):
            raise TableError('%s cell %r has a malformed member %r'
                             % (column, cell, part))
    if len(set(parts)) != len(parts):
        raise TableError('%s cell %r repeats a member' % (column, cell))
    return ('exact', frozenset(parts))


def parse_str_cell(cell, column):
    """operation / provider: exact string or '*'."""
    if cell == '*':
        return ('any', None)
    if not NAME_RE.match(cell):
        raise TableError('%s cell %r is neither * nor an exact token'
                         % (column, cell))
    return ('exact', cell)


def parse_handler_cell(cell):
    if cell == '*':
        return ('any', None)
    if cell == 'none':
        return ('none', None)
    if not PATTERN_RE.match(cell):
        raise TableError('handler cell %r is not *, none, or an fnmatch pattern'
                         % cell)
    return ('pattern', cell)


def parse_enum_cell(cell, column, values):
    if cell == '*':
        return '*'
    if cell in values:
        return cell
    raise TableError('%s cell %r is not one of %s or *'
                     % (column, cell, ', '.join(values)))


def parse_actions(lines, table_start, vocab_line):
    if vocab_line is None:
        raise TableError('no %s ... %s line directly above the table'
                         % (ACTIONS_PREFIX, ACTIONS_SUFFIX))
    text = lines[vocab_line].strip()
    if not (text.startswith(ACTIONS_PREFIX) and text.endswith(ACTIONS_SUFFIX)):
        raise TableError('actions declaration line is malformed: %r' % text)
    body = text[len(ACTIONS_PREFIX):-len(ACTIONS_SUFFIX)].strip()
    tokens = body.split()
    if not tokens:
        raise TableError('actions declaration lists no token')
    for token in tokens:
        if not ACTION_RE.match(token):
            raise TableError('action token %r is malformed' % token)
    if len(set(tokens)) != len(tokens):
        raise TableError('actions declaration repeats a token')
    if 'none' not in tokens:
        raise TableError("actions declaration must include 'none' "
                         "(the no-match default)")
    if vocab_line != table_start - 1:
        # Blank lines only: "directly above" is read as the nearest non-blank
        # line above the header, because a GFM table needs a blank line after
        # an HTML comment block.
        for j in range(vocab_line + 1, table_start):
            if lines[j].strip():
                raise TableError('actions declaration must sit directly above the '
                                 'table (stray line %d between them)' % (j + 1))
    return tokens


def parse_table(lines, first_line_no):
    if len(lines) < 3:
        raise TableError('table at line %d has no header, separator and data row'
                         % first_line_no)
    header = [clean_cell(c) for c in split_row(lines[0])]
    if [c.lower() for c in header] != [h.lower() for h in HEADER]:
        raise TableError('table at line %d: header is %r, expected %r'
                         % (first_line_no, header, HEADER))
    sep = [clean_cell(c) for c in split_row(lines[1])]
    if len(sep) != len(HEADER) or not all(SEPARATOR_RE.match(c) for c in sep):
        raise TableError('table at line %d: second row is not a %d-cell markdown '
                         'separator' % (first_line_no + 1, len(HEADER)))
    rules = []
    labels = set()
    for offset, raw in enumerate(lines[2:], start=3):
        line_no = first_line_no + offset - 1
        cells = split_row(raw)
        if len(cells) != len(HEADER):
            raise TableError('table row at line %d has %d cells, expected %d'
                             % (line_no, len(cells), len(HEADER)))
        cells = [clean_cell(c) for c in cells]
        (label, operation, provider, handler, gap, dep, be, sr, files,
         action, cause, source) = cells
        if not label:
            raise TableError('line %d: empty label' % line_no)
        if not NAME_RE.match(label):
            raise TableError('line %d: malformed label %r' % (line_no, label))
        if label in labels:
            raise TableError('line %d: duplicate label %r' % (line_no, label))
        labels.add(label)
        if not ACTION_RE.match(action):
            raise TableError('line %d: malformed action cell %r'
                             % (line_no, action))
        if not cause:
            raise TableError('line %d: empty cause cell' % line_no)
        if not source:
            raise TableError('line %d: empty source cell' % line_no)
        rules.append({
            'index': len(rules) + 1,
            'line': line_no,
            'label': label,
            'operation': parse_str_cell(operation, 'operation'),
            'provider': parse_str_cell(provider, 'provider'),
            'handler': parse_handler_cell(handler),
            'gap_kinds': parse_set_cell(gap, 'gap kinds'),
            'dependencies': parse_set_cell(dep, 'dependencies'),
            'be': parse_enum_cell(be, '-be in child argv', BE_VALUES),
            'symlink_removed': parse_enum_cell(sr, 'symlink removed', BE_VALUES),
            'files': parse_enum_cell(files, 'published files', FILES_VALUES),
            'action': action,
            'cause': cause,
            'source': source,
            'cells': cells,
        })
    if not rules:
        raise TableError('table at line %d has no rule rows' % first_line_no)
    return rules


def parse_skill(text):
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
    table_start = i
    table = []
    while i < end and lines[i].lstrip().startswith('|'):
        table.append(lines[i])
        i += 1
    vocab_line = None
    j = table_start - 1
    while j > marker_line and not lines[j].strip():
        j -= 1
    if j > marker_line and lines[j].strip().startswith(ACTIONS_PREFIX):
        vocab_line = j
    actions = parse_actions(lines, table_start, vocab_line)
    rules = parse_table(table, table_start + 1)
    for rule in rules:
        if rule['action'] not in actions:
            raise TableError('line %d: action %r is not in the declared vocabulary %s'
                             % (rule['line'], rule['action'], ' '.join(actions)))
    return rules, actions, {'marker_line': marker_line + 1,
                            'table_line': table_start + 1,
                            'rules': len(rules)}


# ---------------------------------------------------------------------------
# envelope features
# ---------------------------------------------------------------------------
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


def names_sasquatch(tokens):
    return any(tok.rsplit('/', 1)[-1].startswith('sasquatch') for tok in tokens)


def extractor_commands(data):
    commands = []

    def take(cmd):
        tokens = command_tokens(cmd)
        if tokens and names_sasquatch(tokens) and cmd not in commands:
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
    if isinstance(obj.get('normalized_result'), dict):
        return obj
    inner = obj.get('data')
    if isinstance(inner, dict) and isinstance(inner.get('normalized_result'), dict):
        return inner
    if obj.get('ok') is False and isinstance(obj.get('error'), dict):
        raise EnvelopeError('%s: REA error envelope (no data object; error code %r)'
                            % (path, obj['error'].get('code')))
    raise EnvelopeError('%s: no normalized_result (neither a bare data object nor '
                        'a full {ok,data,meta} envelope)' % path)


def provider_id(data):
    provider = data.get('provider')
    if isinstance(provider, dict):
        value = provider.get('id')
        return value if isinstance(value, str) else None
    if isinstance(provider, str):
        return provider
    return None


def features(data):
    nr = data.get('normalized_result')
    if not isinstance(nr, dict):
        raise EnvelopeError('normalized_result is not an object')
    handlers = set()
    for chunk in as_list(nr.get('chunks')):
        handler = chunk.get('handler') if isinstance(chunk, dict) else None
        if isinstance(handler, str) and handler.startswith('squashfs'):
            handlers.add(handler)
    gap_kinds, dependencies = set(), set()
    for gap in as_list(nr.get('extraction_gaps')):
        if not isinstance(gap, dict):
            continue
        if isinstance(gap.get('kind'), str):
            gap_kinds.add(gap['kind'])
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
    operation = data.get('operation')
    return {
        'OP': operation if isinstance(operation, str) else None,
        'PV': provider_id(data),
        'H': sorted(handlers),
        'G': sorted(gap_kinds),
        'D': sorted(dependencies),
        'BE': be,
        'SR': symlink,
        'P': len(as_list(nr.get('files'))),
        'commands': [cmd if isinstance(cmd, str) else list(cmd) for cmd in commands],
    }


# ---------------------------------------------------------------------------
# matching
# ---------------------------------------------------------------------------
def match_str(spec, value):
    kind, payload = spec
    if kind == 'any':
        return True
    return value == payload


def match_set(spec, values):
    kind, payload = spec
    if kind == 'any':
        return True
    if kind == 'none':
        return not values
    return frozenset(values) == payload


def rule_matches(rule, feat):
    if not match_str(rule['operation'], feat['OP']):
        return False
    if not match_str(rule['provider'], feat['PV']):
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


# ---------------------------------------------------------------------------
# command line
# ---------------------------------------------------------------------------
def read_skill(path):
    try:
        with open(path, 'r', encoding='utf-8') as handle:
            return handle.read()
    except OSError as exc:
        raise TableError('%s: %s' % (path, exc.strerror or exc))


def load_envelope(path):
    try:
        with open(path, 'r', encoding='utf-8') as handle:
            obj = json.load(handle)
    except (OSError, ValueError) as exc:
        raise EnvelopeError('%s: %s' % (path, exc))
    return features(envelope_data(obj, path))


def run(ns):
    rules, actions, info = parse_skill(read_skill(ns.skill))
    feat = load_envelope(ns.envelope)
    rule = classify(rules, feat)
    label, action, index = ('unclassified', 'none', 0) if rule is None else \
        (rule['label'], rule['action'], rule['index'])
    if ns.json:
        print(json.dumps({'label': label, 'action': action, 'rule': index,
                          'features': feat, 'rules': info['rules']},
                         indent=1, sort_keys=True))
    else:
        print('%s\t%s' % (label, action))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--skill', help='SKILL.md holding the v2 table')
    ap.add_argument('--envelope', help='REA envelope (bare data or full CLI form)')
    ap.add_argument('--print-table', action='store_true')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    ns = ap.parse_args(argv)
    try:
        if ns.print_table:
            rules, actions, info = parse_skill(read_skill(ns.skill))
            print('skill: %s' % ns.skill)
            print('marker line %(marker_line)d, table line %(table_line)d, '
                  'rules %(rules)d' % info)
            print('actions: %s' % ' '.join(actions))
            for rule in rules:
                print('%2d line %-4d %-26s -> %s' % (rule['index'], rule['line'],
                                                     rule['label'], rule['action']))
            return 0
        if ns.selftest:
            return selftest()
        if not (ns.skill and ns.envelope):
            ap.error('--skill and --envelope are required')
        return run(ns)
    except TableError as exc:
        print('sqfs-triage-v2: table: %s' % exc, file=sys.stderr)
        return 2
    except EnvelopeError as exc:
        print('sqfs-triage-v2: envelope: %s' % exc, file=sys.stderr)
        return 2


# ---------------------------------------------------------------------------
# selftest
# ---------------------------------------------------------------------------
SKELETON = ('# SKILL\n\n## Queue-drain craft\n\nProse before the table.\n\n'
            '{block}\n\n## A later section\n\nProse after the craft section.\n')
HEADER_LINE = '| ' + ' | '.join(HEADER) + ' |'
SEP_LINE = '|' + '|'.join(['---'] * len(HEADER)) + '|'
VOCAB = ('<!-- sqfs-triage-actions: none accept-clean reject-image '
         'install-extractor use-avm-layout salvage-partial escalate '
         'review-symlinks drop-symlink -->')

CLEAN_ENV = {'operation': 'extract_firmware', 'provider': {'id': 'unblob'},
             'normalized_result': {'chunks': [{'handler': 'squashfs_v4_be',
                                              'extraction_failed': False}],
                                   'extraction_gaps': [],
                                   'unpublished_entries': [],
                                   'diagnostics': [],
                                   'files': [{'relative_path': 'a'}]}}
PARTIAL_ENV = {'operation': 'extract_firmware', 'provider': {'id': 'unblob'},
               'normalized_result': {
                   'chunks': [{'handler': 'squashfs_v4_be',
                               'extraction_failed': True}],
                   'extraction_gaps': [{'kind': 'extractor-failure',
                                        'dependencies': []}],
                   'unpublished_entries': [],
                   'diagnostics': [{'stage': 'squashfs_v4_be', 'report': {
                       '__typename__': 'ExtractCommandFailedReport',
                       'command': 'sasquatch-v4be -be -no-exit-code -f -d o i',
                       'exit_code': 1}}],
                   'files': [{'relative_path': 'a'}, {'relative_path': 'b'}]}}
BODYFAIL_ENV = {'operation': 'extract_firmware', 'provider': {'id': 'unblob'},
                'normalized_result': {
                    'chunks': [{'handler': 'squashfs_v4_le',
                                'extraction_failed': True}],
                    'extraction_gaps': [{'kind': 'extractor-failure',
                                         'dependencies': []}],
                    'unpublished_entries': [],
                    'diagnostics': [{'stage': 'squashfs_v4_le', 'report': {
                        '__typename__': 'ExtractCommandFailedReport',
                        'command': 'sasquatch -le -no-exit-code -f -d o i'}}],
                    'files': []}}


def row(label, operation='extract_firmware', provider='unblob', handler='*',
        gaps='*', deps='*', be='*', sr='*', files='*', action='none'):
    return '| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | cause | source |' % (
        label, operation, provider, handler, gaps, deps, be, sr, files, action)


def block(rows, vocab=VOCAB, marker=True, header=HEADER_LINE):
    out = []
    if marker:
        out.append(MARKER)
        out.append('')
    if vocab:
        out.append(vocab)
    out.append(header)
    out.append(SEP_LINE)
    out.extend(rows)
    return '\n'.join(out) + '\n'


def write(work, name, text):
    path = os.path.join(work, name)
    with open(path, 'w', encoding='utf-8') as handle:
        handle.write(text)
    return path


def dump(work, name, obj):
    return write(work, name, json.dumps(obj))


def cli(args, work):
    import subprocess
    return subprocess.run([sys.executable, '-I', '-B', os.path.abspath(__file__), *args],
                          capture_output=True, text=True, cwd=work)


def expect(cond, message):
    if not cond:
        raise AssertionError(message)


def exit_is(res, want, label):
    expect(res.returncode == want, '%s: exit %d, expected %d (stderr=%r)'
           % (label, res.returncode, want, res.stderr.strip()[:200]))


def pair_of(res, label):
    exit_is(res, 0, label)
    line = res.stdout.strip().splitlines()[-1]
    label_out, action = line.split('\t')
    return label_out, action


def selftest():
    work = tempfile.mkdtemp(dir=os.environ.get('TMPDIR') or None, prefix='v2-')
    cases = []

    def case(fn):
        cases.append(fn)
        return fn

    @case
    def green():
        skill = write(work, 'sk.md', SKELETON.format(block=block([
            row('partial-body-failure', handler='squashfs_v4_*',
                gaps='extractor-failure', deps='none', files='>0',
                action='salvage-partial'),
            row('body-extractor-failure', handler='squashfs_v4_*',
                gaps='extractor-failure', deps='none', files='0',
                action='escalate'),
            row('clean', gaps='none', deps='none', sr='no', be='n/a',
                action='accept-clean'),
        ])))
        got = pair_of(cli(['--skill', skill, '--envelope',
                           dump(work, 'e1.json', PARTIAL_ENV)], work), 'green')
        expect(got == ('partial-body-failure', 'salvage-partial'),
               'green: got %r' % (got,))

    @case
    def first_match_wins():
        skill = write(work, 'sk2.md', SKELETON.format(block=block([
            row('first', gaps='extractor-failure', action='escalate'),
            row('second', gaps='*', action='none'),
        ])))
        got = pair_of(cli(['--skill', skill, '--envelope',
                           dump(work, 'e2.json', PARTIAL_ENV)], work), 'order')
        expect(got == ('first', 'escalate'), 'order: got %r' % (got,))

    @case
    def domain_guard():
        skill = write(work, 'sk3.md', SKELETON.format(block=block([
            row('in-domain', action='accept-clean'),
        ])))
        env = json.loads(json.dumps(CLEAN_ENV))
        env['operation'] = 'extract_artifact'
        got = pair_of(cli(['--skill', skill, '--envelope',
                           dump(work, 'e3.json', env)], work), 'op-guard')
        expect(got == ('unclassified', 'none'), 'op-guard: got %r' % (got,))
        env = json.loads(json.dumps(CLEAN_ENV))
        env['provider'] = {'id': 'binwalk'}
        got = pair_of(cli(['--skill', skill, '--envelope',
                           dump(work, 'e4.json', env)], work), 'pv-guard')
        expect(got == ('unclassified', 'none'), 'pv-guard: got %r' % (got,))

    @case
    def duplicate_label():
        skill = write(work, 'sk5.md', SKELETON.format(block=block([
            row('same'), row('same')])))
        res = cli(['--skill', skill, '--envelope',
                   dump(work, 'e5.json', CLEAN_ENV)], work)
        exit_is(res, 2, 'duplicate-label')
        expect('duplicate label' in res.stderr, 'duplicate-label: stderr %r' % res.stderr)

    @case
    def unknown_action():
        skill = write(work, 'sk6.md', SKELETON.format(block=block([
            row('x', action='not-in-vocab')])))
        res = cli(['--skill', skill, '--envelope',
                   dump(work, 'e6.json', CLEAN_ENV)], work)
        exit_is(res, 2, 'unknown-action')

    @case
    def bad_cells():
        for name, cells in (('files', row('x', files='1')),
                            ('gap', row('x', gaps='a++b')),
                            ('be', row('x', be='maybe')),
                            ('action', row('x', action='Has Space'))):
            skill = write(work, 'sk7.md', SKELETON.format(block=block([cells])))
            res = cli(['--skill', skill, '--envelope',
                       dump(work, 'e7.json', CLEAN_ENV)], work)
            exit_is(res, 2, 'bad-%s' % name)

    @case
    def header_mismatch():
        header = '| ' + ' | '.join(HEADER[:-1]) + ' |'
        skill = write(work, 'sk8.md', SKELETON.format(block=block([row('x')], header=header)))
        exit_is(cli(['--skill', skill, '--envelope',
                     dump(work, 'e8.json', CLEAN_ENV)], work), 2, 'header')

    @case
    def marker_absent():
        skill = write(work, 'sk9.md', SKELETON.format(block=block([row('x')], marker=False)))
        exit_is(cli(['--skill', skill, '--envelope',
                     dump(work, 'e9.json', CLEAN_ENV)], work), 2, 'marker')

    @case
    def table_outside_craft():
        text = ('# SKILL\n\n## Queue-drain craft\n\nno table\n\n## Later\n\n'
                + block([row('x')]) + '\n')
        skill = write(work, 'sk10.md', text)
        exit_is(cli(['--skill', skill, '--envelope',
                     dump(work, 'e10.json', CLEAN_ENV)], work), 2, 'outside')

    @case
    def vocab_missing_or_far():
        skill = write(work, 'sk11.md', SKELETON.format(block=block([row('x')], vocab=None)))
        exit_is(cli(['--skill', skill, '--envelope',
                     dump(work, 'e11.json', CLEAN_ENV)], work), 2, 'no-vocab')
        far = block([row('x')]).replace(VOCAB + '\n', VOCAB + '\ntext\n')
        skill = write(work, 'sk12.md', SKELETON.format(block=far))
        exit_is(cli(['--skill', skill, '--envelope',
                     dump(work, 'e12.json', CLEAN_ENV)], work), 2, 'far-vocab')

    @case
    def bare_and_full():
        full = {'ok': True, 'data': PARTIAL_ENV, 'meta': {'command': 'extract-firmware'}}
        skill = write(work, 'sk13.md', SKELETON.format(block=block([
            row('p', gaps='extractor-failure', files='>0', action='salvage-partial')])))
        a = pair_of(cli(['--skill', skill, '--envelope',
                         dump(work, 'e13.json', full)], work), 'full')
        b = pair_of(cli(['--skill', skill, '--envelope',
                         dump(work, 'e14.json', PARTIAL_ENV)], work), 'bare')
        expect(a == b, 'bare-full: %r vs %r' % (a, b))

    @case
    def error_envelope_rejected():
        skill = write(work, 'sk15.md', SKELETON.format(block=block([row('x')])))
        res = cli(['--skill', skill, '--envelope',
                   dump(work, 'e15.json', {'ok': False, 'error': {'code': 'target_unavailable'},
                                           'meta': {'command': 'extract-artifact'}})], work)
        exit_is(res, 2, 'error-envelope')
        expect('error envelope' in res.stderr, 'error-envelope: stderr %r' % res.stderr)

    @case
    def be_cells():
        skill = write(work, 'sk16.md', SKELETON.format(block=block([
            row('be-yes', be='yes', action='escalate'),
            row('be-no', be='no', action='use-avm-layout'),
            row('be-na', be='n/a', action='accept-clean'),
        ])))
        partial = json.loads(json.dumps(PARTIAL_ENV))
        got = pair_of(cli(['--skill', skill, '--envelope',
                           dump(work, 'e16.json', partial)], work), 'be-yes')
        expect(got == ('be-yes', 'escalate'), 'be-yes: got %r' % (got,))
        got = pair_of(cli(['--skill', skill, '--envelope',
                           dump(work, 'e17.json', BODYFAIL_ENV)], work), 'be-no')
        expect(got == ('be-no', 'use-avm-layout'), 'be-no: got %r' % (got,))
        got = pair_of(cli(['--skill', skill, '--envelope',
                           dump(work, 'e18.json', CLEAN_ENV)], work), 'be-na')
        expect(got == ('be-na', 'accept-clean'), 'be-na: got %r' % (got,))

    passed = 0
    for fn in cases:
        try:
            fn()
        except AssertionError as exc:
            print('FAIL %s: %s' % (fn.__name__, exc))
        else:
            passed += 1
            print('ok   %s' % fn.__name__)
    print('selftest: %d/%d' % (passed, len(cases)))
    return 0 if passed == len(cases) else 1


if __name__ == '__main__':
    sys.exit(main())
