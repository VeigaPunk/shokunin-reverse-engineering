#!/usr/bin/env python3
"""sqfs-triage-v2-proto.py — wave-1 prototype of the round-40 v2 triage grammar.

Recon prototype for R40-C2 (seat R40C2ReconDomain).  It implements the draft v2
grammar exactly as written in the round-40 claims, so the L1 can lift it into
``tools/round-40/sqfs-triage-v2.py`` after review:

  * the table is the first markdown table after a line containing
    ``<!-- sqfs-triage-table v2 -->`` inside SKILL.md's ``## Queue-drain craft``
    section (heading line to the next ``##`` heading);
  * header, in order: label | operation | provider | handler | gap kinds |
    dependencies | -be in child argv | symlink removed | published files |
    action | cause | source;
  * ``<!-- sqfs-triage-actions: tok ... -->`` must sit directly above the table
    header (blank lines allowed between) and declares the action vocabulary;
  * rows are tried top to bottom, the first full match yields (label, action);
    no match yields (``unclassified``, ``none``);
  * duplicate label, unknown action, malformed cell -> exit 2 (never a silent
    non-match);
  * features come from an REA envelope, bare ``data`` object or full
    ``{ok,data,meta}``: OP = data.operation, PV = data.provider.id, and
    H/G/D/BE/SR/P exactly as the v1 grammar (tools/round-39/sqfs-triage.py).

Usage:
    python3 sqfs-triage-v2-proto.py --skill SKILL.md [--json] ENVELOPE...
    python3 sqfs-triage-v2-proto.py --skill SKILL.md --print-table
    python3 sqfs-triage-v2-proto.py --selftest
"""

import argparse
import fnmatch
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile

MARKER = '<!-- sqfs-triage-table v2 -->'
ACTIONS_MARKER_RE = re.compile(r'^<!--\s*sqfs-triage-actions:\s*(.*?)\s*-->$')
CRAFT_PREFIX = 'queue-drain craft'
HEADER = ['label', 'operation', 'provider', 'handler', 'gap kinds', 'dependencies',
          '-be in child argv', 'symlink removed', 'published files', 'action',
          'cause', 'source']
BE_VALUES = ('yes', 'no', 'n/a')
FILES_VALUES = ('0', '>0')
SYMLINK_TYPENAME = 'MaliciousSymlinkRemoved'
UNCLASSIFIED = ('unclassified', 'none')
SEPARATOR_RE = re.compile(r'^:?-+:?$')
NAME_RE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.\-]*$')
HANDLER_RE = re.compile(r'^[A-Za-z0-9_?*.\-\[\]]+$')
ACTION_RE = re.compile(r'^[a-z][a-z0-9\-]*$')


class TableError(Exception):
    """The triage table or its action vocabulary is missing or malformed."""


class EnvelopeError(Exception):
    """An envelope could not be read as an REA result object."""


# ---------------------------------------------------------------------------
# table parsing
# ---------------------------------------------------------------------------

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
            raise TableError('%s cell %r has a malformed member %r' % (column, cell, part))
    if len(set(parts)) != len(parts):
        raise TableError('%s cell %r repeats a member' % (column, cell))
    return ('exact', frozenset(parts))


def parse_handler_cell(cell):
    if cell == '*':
        return ('any', None)
    if cell == 'none':
        return ('none', None)
    if not HANDLER_RE.match(cell):
        raise TableError('handler cell %r is not *, none, or an fnmatch pattern' % cell)
    return ('pattern', cell)


def parse_enum_cell(cell, column, values):
    if cell == '*':
        return '*'
    if cell in values:
        return cell
    raise TableError('%s cell %r is not one of %s or *' % (column, cell, ', '.join(values)))


def parse_name_cell(cell, column):
    if cell == '*':
        return '*'
    if not NAME_RE.match(cell):
        raise TableError('%s cell %r is not *, or a normalized name' % (column, cell))
    return cell


def parse_actions(lines, table_line):
    """Vocabulary from the ``sqfs-triage-actions`` line directly above the table."""
    i = table_line - 2
    while i >= 0 and not lines[i].strip():
        i -= 1
    if i < 0:
        raise TableError('no sqfs-triage-actions line above the table')
    match = ACTIONS_MARKER_RE.match(lines[i].strip())
    if not match:
        raise TableError('line %d above the table is not the sqfs-triage-actions marker'
                         % (i + 1))
    tokens = match.group(1).split()
    if not tokens:
        raise TableError('sqfs-triage-actions at line %d declares no action' % (i + 1))
    for token in tokens:
        if not ACTION_RE.match(token):
            raise TableError('action %r is not a lowercase token' % token)
    if len(set(tokens)) != len(tokens):
        raise TableError('sqfs-triage-actions repeats a token')
    return tokens, i + 1


def parse_table(lines, first_line_no, actions):
    if len(lines) < 3:
        raise TableError('table at line %d has no header, separator and data row'
                         % first_line_no)
    header = [clean_cell(c) for c in split_row(lines[0])]
    if [c.lower() for c in header] != [h.lower() for h in HEADER]:
        raise TableError('table at line %d: header is %r, expected %r'
                         % (first_line_no, header, HEADER))
    sep_cells = [clean_cell(c) for c in split_row(lines[1])]
    if len(sep_cells) != len(HEADER) or not all(SEPARATOR_RE.match(c) for c in sep_cells):
        raise TableError('table at line %d: second row is not a %d-cell markdown separator'
                         % (first_line_no + 1, len(HEADER)))
    rules = []
    labels = set()
    vocab = set(actions)
    for offset, raw_line in enumerate(lines[2:], start=3):
        line_no = first_line_no + offset - 1
        cells = split_row(raw_line)
        if len(cells) != len(HEADER):
            raise TableError('table row at line %d has %d cells, expected %d'
                             % (line_no, len(cells), len(HEADER)))
        cells = [clean_cell(c) for c in cells]
        (label, operation, provider, handler, gap, dep, be, sr, files, action,
         cause, source) = cells
        if not label:
            raise TableError('line %d: empty label' % line_no)
        if label == UNCLASSIFIED[0]:
            raise TableError('line %d: label %r is reserved for the no-match outcome'
                             % (line_no, label))
        if label in labels:
            raise TableError('line %d: duplicate label %r' % (line_no, label))
        labels.add(label)
        if action not in vocab:
            raise TableError('line %d: action %r is not in the vocabulary (%s)'
                             % (line_no, action, ' '.join(actions)))
        if not cause:
            raise TableError('line %d: empty cause cell' % line_no)
        if not source:
            raise TableError('line %d: empty source cell' % line_no)
        rules.append({
            'index': len(rules) + 1,
            'line': line_no,
            'label': label,
            'operation': parse_name_cell(operation, 'operation'),
            'provider': parse_name_cell(provider, 'provider'),
            'handler': parse_handler_cell(handler),
            'gap_kinds': parse_set_cell(gap, 'gap kinds'),
            'dependencies': parse_set_cell(dep, 'dependencies'),
            'be': parse_enum_cell(be, '-be in child argv', BE_VALUES),
            'symlink_removed': parse_enum_cell(sr, 'symlink removed', BE_VALUES),
            'files': parse_enum_cell(files, 'published files', FILES_VALUES),
            'action': action,
            'cause': cause,
            'source': source,
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
    table = []
    while i < end and lines[i].lstrip().startswith('|'):
        table.append(lines[i])
        i += 1
    table_line = i - len(table) + 1
    actions, actions_line = parse_actions(lines, table_line)
    rules = parse_table(table, table_line, actions)
    return rules, actions, {'marker_line': marker_line + 1, 'table_line': table_line,
                            'actions_line': actions_line, 'rules': len(rules)}


# ---------------------------------------------------------------------------
# envelope features
# ---------------------------------------------------------------------------

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
        'OP': operation if isinstance(operation, str) else '',
        'PV': (provider.get('id') if isinstance(provider, dict) else '') or '',
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


# ---------------------------------------------------------------------------
# classification
# ---------------------------------------------------------------------------

def match_name(spec, value):
    return spec == '*' or spec == value


def match_set(spec, values):
    kind, payload = spec
    if kind == 'any':
        return True
    if kind == 'none':
        return not values
    return frozenset(values) == payload


def rule_matches(rule, feat):
    if not match_name(rule['operation'], feat['OP']):
        return False
    if not match_name(rule['provider'], feat['PV']):
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
            return rule['label'], rule['action'], rule
    return UNCLASSIFIED[0], UNCLASSIFIED[1], None


# ---------------------------------------------------------------------------
# command line
# ---------------------------------------------------------------------------

def read_skill(path):
    try:
        with open(path, 'r', encoding='utf-8') as handle:
            return handle.read()
    except OSError as exc:
        raise TableError('%s: %s' % (path, exc.strerror or exc))


def run(ns):
    if not ns.skill:
        raise TableError('--skill is required')
    rules, actions, info = parse_skill(read_skill(ns.skill))
    if ns.print_table:
        print('skill: %s' % ns.skill)
        print('marker line: %d  actions line: %d  table line: %d  rules: %d'
              % (info['marker_line'], info['actions_line'], info['table_line'],
                 info['rules']))
        print('actions: %s' % ' '.join(actions))
        for rule in rules:
            print('%d. %s [%s] op=%r pv=%r handler=%r gap=%r dep=%r be=%r sr=%r files=%r'
                  % (rule['index'], rule['label'], rule['action'], rule['operation'],
                     rule['provider'], rule['handler'], rule['gap_kinds'],
                     rule['dependencies'], rule['be'], rule['symlink_removed'],
                     rule['files']))
        return 0
    if not ns.envelopes:
        raise TableError('at least one envelope path is required')
    results = []
    for path in ns.envelopes:
        feat = load_envelope(path)
        label, action, rule = classify(rules, feat)
        results.append({'path': path, 'label': label, 'action': action,
                        'rule': rule['index'] if rule else None,
                        'features': feat})
    if ns.json:
        print(json.dumps({'results': results, 'rules': len(rules),
                          'actions': actions, 'skill': ns.skill},
                         indent=2, sort_keys=True))
    else:
        for entry in results:
            print('%s\t%s\t%s' % (entry['path'], entry['label'], entry['action']))
    return 0


# ---------------------------------------------------------------------------
# selftest
# ---------------------------------------------------------------------------

SKELETON = ('# SKILL\n\n## Queue-drain craft\n\nCraft prose before the table.\n\n'
            '{block}\n\n## A later section\n\nProse after the craft section.\n')

ROW = ('| {label} | {op} | {pv} | {h} | {g} | {d} | {be} | {sr} | {p} | {action} '
       '| cause text | selftest |')

BASE_ROWS = [
    # label, op, pv, handler, gaps, deps, be, sr, files, action
    ('no-squashfs-chunk', 'extract_firmware', 'unblob', 'none', '*', '*', 'n/a', '*', '*',
     'check-superblock'),
    ('avm-marker-be-dropped', 'extract_firmware', 'unblob', 'squashfs_v4_be',
     'extractor-failure', 'none', 'no', 'no', '0', 'rerun-with-be'),
    ('body-extractor-failure', 'extract_firmware', 'unblob', 'squashfs_v4_be',
     'extractor-failure', 'none', 'yes', 'no', '0', 'compare-oracle'),
    ('mixed-symlinks', 'extract_firmware', 'unblob', 'squashfs_v4_*',
     'unpublished-entry', 'none', 'n/a', 'yes', '>0', 'expect-absent'),
    ('escaping-symlink-removed', 'extract_firmware', 'unblob', 'squashfs_v4_*', '*', '*',
     'n/a', 'yes', '>0', 'expect-absent'),
    ('in-tree-symlink-metadata', 'extract_firmware', 'unblob', 'squashfs_v4_*',
     'unpublished-entry', 'none', 'n/a', 'no', '>0', 'expect-absent'),
    ('clean', 'extract_firmware', 'unblob', 'squashfs_v4_*', 'none', 'none', 'n/a', 'no',
     '>0', 'compare-oracle'),
]
VOCAB = 'check-superblock rerun-with-be compare-oracle expect-absent none'


def build_skill(rows=BASE_ROWS, vocab=VOCAB, extra_blank=True):
    block = ['| label | operation | provider | handler | gap kinds | dependencies '
             '| -be in child argv | symlink removed | published files | action '
             '| cause | source |',
             '| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |']
    for row in rows:
        block.append(ROW.format(label=row[0], op=row[1], pv=row[2], h=row[3], g=row[4],
                                d=row[5], be=row[6], sr=row[7], p=row[8], action=row[9]))
    parts = ['<!-- sqfs-triage-table v2 -->', '']
    if vocab:
        parts.append('<!-- sqfs-triage-actions: %s -->' % vocab)
        if extra_blank:
            parts.append('')
    parts.extend(block)
    return SKELETON.format(block='\n'.join(parts))


def _cli(args):
    return subprocess.run([sys.executable, '-I', '-B', os.path.abspath(__file__), *args],
                          capture_output=True, text=True)


def _write(work, name, text):
    path = os.path.join(work, name)
    with open(path, 'w', encoding='utf-8') as handle:
        handle.write(text)
    return path


def _dump(work, name, obj):
    return _write(work, name, json.dumps(obj, indent=1, sort_keys=True))


def _load(path):
    with open(path, 'r', encoding='utf-8') as handle:
        return json.load(handle)


def _label(res, env):
    assert res.returncode == 0, (res.returncode, res.stderr[:300])
    out = json.loads(res.stdout)
    return out['results'][0]['label'], out['results'][0]['action']


CASES = []


def case(fn):
    CASES.append(fn)
    return fn


@case
def c_guard_domain(work):
    skill = _write(work, 'sk.md', build_skill())
    env = _dump(work, 'ood.json', {'ok': True, 'data': {
        'operation': 'inspect_firmware_regions',
        'provider': {'id': 'binwalk', 'name': 'Binwalk', 'version': '3.1.0'},
        'normalized_result': {'engine': {}, 'input_size': 1, 'regions': [], 'coverage': 'x'},
    }, 'meta': {'command': 'inspect-firmware-regions'}})
    got = _label(_cli(['--skill', skill, '--json', env]), env)
    assert got == ('unclassified', 'none'), got


@case
def c_guard_at_star(work):
    rows = [list(r) for r in BASE_ROWS]
    rows[0][1] = '*'
    rows[0][2] = '*'
    skill = _write(work, 'sk.md', build_skill([tuple(r) for r in rows]))
    env = _dump(work, 'ood.json', {'ok': True, 'data': {
        'operation': 'inspect_firmware_regions',
        'provider': {'id': 'binwalk'},
        'normalized_result': {'regions': []},
    }})
    got = _label(_cli(['--skill', skill, '--json', env]), env)
    assert got[0] == 'no-squashfs-chunk', got


@case
def c_duplicate_label(work):
    rows = [BASE_ROWS[0], BASE_ROWS[0]]
    skill = _write(work, 'sk.md', build_skill(rows))
    env = _dump(work, 'e.json', {'operation': 'extract_firmware',
                                 'provider': {'id': 'unblob'},
                                 'normalized_result': {'chunks': [], 'files': []}})
    res = _cli(['--skill', skill, env])
    assert res.returncode == 2 and 'duplicate label' in res.stderr, res.stderr[:300]


@case
def c_unknown_action(work):
    rows = [list(BASE_ROWS[0])]
    rows[0][9] = 'not-in-vocab'
    skill = _write(work, 'sk.md', build_skill([tuple(rows[0])]))
    env = _dump(work, 'e.json', {'operation': 'extract_firmware',
                                 'provider': {'id': 'unblob'},
                                 'normalized_result': {'chunks': [], 'files': []}})
    res = _cli(['--skill', skill, env])
    assert res.returncode == 2 and 'vocabulary' in res.stderr, res.stderr[:300]


@case
def c_missing_vocab(work):
    skill = _write(work, 'sk.md', build_skill(vocab=''))
    env = _dump(work, 'e.json', {'operation': 'extract_firmware',
                                 'provider': {'id': 'unblob'},
                                 'normalized_result': {'chunks': [], 'files': []}})
    res = _cli(['--skill', skill, env])
    assert res.returncode == 2 and 'sqfs-triage-actions' in res.stderr, res.stderr[:300]


@case
def c_malformed_cell(work):
    rows = [list(BASE_ROWS[0])]
    rows[0][8] = 'many'
    skill = _write(work, 'sk.md', build_skill([tuple(rows[0])]))
    env = _dump(work, 'e.json', {'operation': 'extract_firmware',
                                 'provider': {'id': 'unblob'},
                                 'normalized_result': {'chunks': [], 'files': []}})
    res = _cli(['--skill', skill, env])
    assert res.returncode == 2 and 'published files' in res.stderr, res.stderr[:300]


@case
def c_marker_absent(work):
    text = build_skill().replace('<!-- sqfs-triage-table v2 -->', '')
    skill = _write(work, 'sk.md', text)
    env = _dump(work, 'e.json', {'operation': 'extract_firmware',
                                 'provider': {'id': 'unblob'},
                                 'normalized_result': {'chunks': [], 'files': []}})
    res = _cli(['--skill', skill, env])
    assert res.returncode == 2 and 'marker' in res.stderr, res.stderr[:300]


@case
def c_first_match_wins(work):
    rows = [('wide', 'extract_firmware', 'unblob', '*', '*', '*', '*', '*', '*', 'none'),
            BASE_ROWS[0]]
    skill = _write(work, 'sk.md', build_skill(rows))
    env = _dump(work, 'e.json', {'operation': 'extract_firmware',
                                 'provider': {'id': 'unblob'},
                                 'normalized_result': {'chunks': [], 'files': []}})
    got = _label(_cli(['--skill', skill, '--json', env]), env)
    assert got[0] == 'wide', got


@case
def c_bare_and_full(work):
    skill = _write(work, 'sk.md', build_skill())
    data = {'operation': 'extract_firmware', 'provider': {'id': 'unblob'},
            'normalized_result': {'chunks': [{'handler': 'squashfs_v4_be'}],
                                  'files': [{'path': 'a'}], 'extraction_gaps': []}}
    bare = _dump(work, 'bare.json', data)
    full = _dump(work, 'full.json', {'ok': True, 'data': data, 'meta': {}})
    a = _label(_cli(['--skill', skill, '--json', bare]), bare)
    b = _label(_cli(['--skill', skill, '--json', full]), full)
    assert a == b == ('clean', 'compare-oracle'), (a, b)


@case
def c_mixed_symlinks(work):
    skill = _write(work, 'sk.md', build_skill())
    env = _dump(work, 'mixed.json', {
        'operation': 'extract_firmware', 'provider': {'id': 'unblob'},
        'normalized_result': {
            'chunks': [{'handler': 'squashfs_v4_be', 'extraction_failed': False}],
            'files': [{'path': 'a'}],
            'extraction_gaps': [{'kind': 'unpublished-entry', 'dependencies': []}],
            'diagnostics': [{'report': {'__typename__': 'MaliciousSymlinkRemoved'}}],
        }})
    got = _label(_cli(['--skill', skill, '--json', env]), env)
    assert got == ('mixed-symlinks', 'expect-absent'), got


@case
def c_error_envelope(work):
    skill = _write(work, 'sk.md', build_skill())
    env = _dump(work, 'err.json', {'ok': False, 'error': {'code': 'target_unavailable'}})
    res = _cli(['--skill', skill, env])
    assert res.returncode == 2 and 'normalized_result' in res.stderr, res.stderr[:300]


@case
def c_reserved_label(work):
    rows = [('unclassified', 'extract_firmware', 'unblob', '*', '*', '*', '*', '*', '*',
             'none')]
    skill = _write(work, 'sk.md', build_skill(rows))
    env = _dump(work, 'e.json', {'operation': 'extract_firmware',
                                 'provider': {'id': 'unblob'},
                                 'normalized_result': {'chunks': [], 'files': []}})
    res = _cli(['--skill', skill, env])
    assert res.returncode == 2 and 'reserved' in res.stderr, res.stderr[:300]


@case
def c_print_table(work):
    skill = _write(work, 'sk.md', build_skill())
    res = _cli(['--skill', skill, '--print-table'])
    assert res.returncode == 0 and 'rules: 7' in res.stdout, (res.returncode, res.stdout[:300])


def selftest():
    work = tempfile.mkdtemp(dir=os.environ.get('TMPDIR') or None, prefix='sqfs-v2-')
    failed = 0
    for fn in CASES:
        try:
            fn(work)
            print('ok   %s' % fn.__name__)
        except AssertionError as exc:
            failed += 1
            print('FAIL %s: %s' % (fn.__name__, exc))
    print('%d cases, %d failed' % (len(CASES), failed))
    return 0 if failed == 0 else 1


# ---------------------------------------------------------------------------
# entry point
# ---------------------------------------------------------------------------

def main(argv=None):
    parser = argparse.ArgumentParser(
        description='SquashFS outcome triage with a domain guard (v2 prototype).')
    parser.add_argument('--skill', help='SKILL.md holding the v2 triage table')
    parser.add_argument('--json', action='store_true', help='emit JSON results')
    parser.add_argument('--print-table', action='store_true',
                        help='print the parsed rules and actions')
    parser.add_argument('--selftest', action='store_true')
    parser.add_argument('envelopes', nargs='*', help='REA envelopes to classify')
    ns = parser.parse_args(argv)
    if ns.selftest:
        return selftest()
    try:
        return run(ns)
    except (TableError, EnvelopeError) as exc:
        sys.stderr.write('sqfs-triage-v2: %s\n' % exc)
        return 2


if __name__ == '__main__':
    sys.exit(main())
