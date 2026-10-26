#!/usr/bin/env python3
"""v3-interp-preview — R41C2Mutants reference preview, NOT the frozen contract.

A compact preview of the round-41 v3 triage interpreter clauses named in
plans/round-41-claims.md (DRAFT): the v3 marker, a contains-form set cell in the
`gap kinds` column (`⊇kind[+kind...]` = "gap set contains these kinds, others
allowed"), and first-match row order carrying the label precedence.  It exists
so the new-clause mutants (R41-N04..N07) and their killing selftest cases can be
executed.  The v3 grammar the L1 freezes may differ; the cases, not this code,
are the deliverable.

CLI mirrors sqfs-triage-v2.py: --skill SKILL [--json] [--table-only] ENV...
exit 0 ok / 2 table or envelope error / 1 selftest failure.
"""
import argparse
import fnmatch
import json
import os
import shlex
import subprocess
import sys
import tempfile

MARKER = '<!-- sqfs-triage-table v3 -->'
ACTIONS_PREFIX = '<!-- sqfs-triage-actions:'
ACTIONS_SUFFIX = '-->'
CRAFT = '## Queue-drain craft'
OPERATION_TOKEN = 'extract_firmware'
SYMLINK_TYPENAME = 'MaliciousSymlinkRemoved'
DEFAULT_LABEL = 'unclassified'
DEFAULT_ACTION = 'none'
CONTAINS_OP = '⊇'

VOCAB = ('none inspect-input install-extractor-be install-extractor-le '
         'wrap-extractor-be preserve-failure salvage-partial audit-symlinks '
         'expect-link-absent count-gap confirm-empty audit-depth')

HEADER = ['label', 'operation', 'provider', 'handler', 'gap kinds', 'dependencies',
          '-be in child argv', 'symlink removed', 'published files', 'action',
          'cause', 'source']

# Table expressing the claims' label precedence by row order (first match wins).
TABLE_V3 = """\
<!-- sqfs-triage-table v3 -->
<!-- sqfs-triage-actions: none inspect-input install-extractor-be install-extractor-le wrap-extractor-be preserve-failure salvage-partial audit-symlinks expect-link-absent count-gap confirm-empty audit-depth -->
| label | operation | provider | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| no-squashfs-chunk | `extract_firmware` | `unblob` | `none` | `*` | `*` | `*` | `*` | `*` | `inspect-input` | no squashfs handler ran | preview |
| dep-missing-be | `extract_firmware` | `unblob` | `squashfs_v4_be` | `⊇missing-extractor-dependency` | `sasquatch-v4be` | `n/a` | `no` | `*` | `install-extractor-be` | be extractor absent | preview |
| dep-missing-le | `extract_firmware` | `unblob` | `squashfs_v4_le` | `⊇missing-extractor-dependency` | `sasquatch` | `n/a` | `no` | `*` | `install-extractor-le` | le extractor absent | preview |
| partial-body-failure | `extract_firmware` | `unblob` | `squashfs_v4_*` | `⊇extractor-failure` | `none` | `*` | `*` | `>0` | `salvage-partial` | partial success, whatever else accompanies | preview |
| avm-marker-be-dropped | `extract_firmware` | `unblob` | `squashfs_v4_be` | `⊇extractor-failure` | `none` | `no` | `*` | `0` | `wrap-extractor-be` | marker read, -be dropped | preview |
| body-extractor-failure | `extract_firmware` | `unblob` | `squashfs_v4_*` | `⊇extractor-failure` | `none` | `*` | `*` | `0` | `preserve-failure` | body failure | preview |
| depth-limited-nested | `extract_firmware` | `unblob` | `squashfs_v4_*` | `⊇depth-limited` | `none` | `*` | `*` | `*` | `audit-depth` | nested chunk not descended | preview |
| mixed-symlinks | `extract_firmware` | `unblob` | `squashfs_v4_*` | `⊇unpublished-entry` | `none` | `*` | `yes` | `*` | `audit-symlinks` | escaped and in-tree links | preview |
| escaping-symlink-removed | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `none` | `*` | `yes` | `*` | `expect-link-absent` | escaped link removed | preview |
| in-tree-symlink-metadata | `extract_firmware` | `unblob` | `squashfs_v4_*` | `unpublished-entry` | `none` | `*` | `no` | `*` | `count-gap` | in-tree links kept as metadata | preview |
| clean | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `none` | `*` | `no` | `>0` | `none` | clean | preview |
| clean-empty | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `none` | `*` | `no` | `0` | `confirm-empty` | clean and empty | preview |
"""


class TableError(Exception):
    pass


class EnvelopeError(Exception):
    pass


class InvocationError(Exception):
    pass


def clean_cell(raw):
    s = raw.strip()
    if len(s) >= 2 and s[0] == '`' and s[-1] == '`' and s.count('`') == 2:
        return s[1:-1].strip()
    return s


def _is_h2(line):
    return line.startswith('## ') and not line.startswith('### ')


def craft_bounds(lines):
    start = None
    for i, line in enumerate(lines):
        if line.startswith(CRAFT):
            start = i
            break
    if start is None:
        raise TableError('no %r section' % CRAFT)
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if _is_h2(lines[i]):
            end = i
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
    """('any'|'none'|'exact'|'contains', payload) for a gap-kinds/dependencies cell."""
    if cell == '*':
        return ('any', None)
    if cell == 'none':
        return ('none', None)
    contains = False
    body = cell
    if cell.startswith(CONTAINS_OP):
        if column != 'gap kinds':
            raise TableError('the %r operator is allowed only in the gap kinds column, '
                             'not in %s' % (CONTAINS_OP, column))
        contains = True
        body = cell[len(CONTAINS_OP):]
    parts = [p for p in body.split('+') if p]
    if not parts or any(not p for p in parts):
        raise TableError('malformed set cell %r' % cell)
    if len(set(parts)) != len(parts):
        raise TableError('set cell %r repeats a member' % cell)
    return ('contains' if contains else 'exact', frozenset(parts))


def _parse_handler_cell(cell):
    if cell == '*':
        return ('any', None)
    if cell == 'none':
        return ('none', None)
    return ('pattern', cell)


def _parse_domain_cell(cell, token_re):
    import re
    if cell == '*':
        return '*'
    if not re.match(r'^[A-Za-z0-9][A-Za-z0-9_.\-]*$', cell):
        raise TableError('malformed domain cell %r' % cell)
    return cell


def _parse_enum_cell(cell, values):
    if cell == '*':
        return '*'
    if cell not in values:
        raise TableError('malformed enum cell %r' % cell)
    return cell


def _parse_files_cell(cell):
    if cell == '*':
        return '*'
    if cell == '0':
        return '0'
    if cell == '>0':
        return '>0'
    raise TableError('malformed published-files cell %r' % cell)


def parse_actions_line(line, line_no):
    s = line.strip()
    if not s.startswith(ACTIONS_PREFIX) or not s.endswith(ACTIONS_SUFFIX):
        raise TableError('line %d: not an actions vocabulary line' % line_no)
    tokens = s[len(ACTIONS_PREFIX):-len(ACTIONS_SUFFIX)].split()
    if not tokens:
        raise TableError('line %d: empty action vocabulary' % line_no)
    return tokens


def parse_table(lines, first_line_no, vocabulary):
    if len(lines) < 3:
        raise TableError('table too short')
    header = [clean_cell(c).lower() for c in split_row(lines[0])]
    need = ['label', 'operation', 'provider', 'handler', 'gap kinds', 'dependencies',
            '-be in child argv', 'symlink removed', 'published files', 'action']
    for col in need:
        if col not in header:
            raise TableError('header lacks %r' % col)
    idx = {name: header.index(name) for name in need}
    rules = []
    labels = set()
    for ri, line in enumerate(lines[2:]):
        if not line.lstrip().startswith('|'):
            break
        cells = split_row(line)
        if len(cells) != len(header):
            raise TableError('row %d has %d cells, header has %d'
                             % (first_line_no + 2 + ri, len(cells), len(header)))
        label = clean_cell(cells[idx['label']])
        action = clean_cell(cells[idx['action']])
        if not label:
            raise TableError('row %d: empty label' % (first_line_no + 2 + ri))
        if label in labels:
            raise TableError('row %d: duplicate label %r' % (first_line_no + 2 + ri, label))
        labels.add(label)
        if action not in vocabulary:
            raise TableError('row %d: action %r not in the vocabulary'
                             % (first_line_no + 2 + ri, action))
        rules.append({
            'label': label, 'action': action,
            'operation': _parse_domain_cell(clean_cell(cells[idx['operation']]), None),
            'provider': _parse_domain_cell(clean_cell(cells[idx['provider']]), None),
            'handler': _parse_handler_cell(clean_cell(cells[idx['handler']])),
            'gaps': _parse_set_cell(clean_cell(cells[idx['gap kinds']]), 'gap kinds'),
            'deps': _parse_set_cell(clean_cell(cells[idx['dependencies']]),
                                    'dependencies'),
            'be': _parse_enum_cell(clean_cell(cells[idx['-be in child argv']]),
                                   ('yes', 'no', 'n/a')),
            'sr': _parse_enum_cell(clean_cell(cells[idx['symlink removed']]),
                                   ('yes', 'no')),
            'files': _parse_files_cell(clean_cell(cells[idx['published files']])),
        })
    if not rules:
        raise TableError('table has no rows')
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
    vocabulary = parse_actions_line(lines[actions_line], actions_line + 1)
    table = []
    i = table_start
    while i < end and lines[i].lstrip().startswith('|'):
        table.append(lines[i])
        i += 1
    rules = parse_table(table, table_start + 1, vocabulary)
    return rules, {'marker_line': marker_line + 1, 'actions_line': actions_line + 1,
                   'table_line': table_start + 1, 'rules': len(rules),
                   'actions': vocabulary}


# ------------------------------------------------------------------ features
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
        candidate = obj
    else:
        inner = obj.get('data')
        candidate = inner if isinstance(inner, dict) else (
            obj if isinstance(obj.get('operation'), str) else None)
    if candidate is None:
        raise EnvelopeError('%s: no normalized_result or operation' % path)
    if 'normalized_result' in candidate and not isinstance(
            candidate['normalized_result'], dict):
        raise EnvelopeError('%s: normalized_result is not an object' % path)
    if not isinstance(candidate.get('normalized_result'), dict) and \
            not isinstance(candidate.get('operation'), str):
        raise EnvelopeError('%s: no normalized_result object and no operation' % path)
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
    if operation == OPERATION_TOKEN and not isinstance(data.get('normalized_result'),
                                                       dict):
        raise EnvelopeError('an %s envelope has no normalized_result object'
                            % OPERATION_TOKEN)
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
    return {'OP': operation, 'PV': provider_id, 'H': sorted(handlers),
            'G': sorted(gap_kinds), 'D': sorted(dependencies), 'BE': be,
            'SR': symlink, 'P': len(_as_list(nr.get('files'))),
            'commands': [c if isinstance(c, str) else list(c) for c in commands]}


def load_envelope(path):
    try:
        with open(path, 'r', encoding='utf-8') as handle:
            obj = json.load(handle)
    except OSError as exc:
        raise EnvelopeError('%s: %s' % (path, exc.strerror or exc))
    except ValueError as exc:
        raise EnvelopeError('%s: not valid JSON (%s)' % (path, exc))
    return features(envelope_data(obj, path))


# ------------------------------------------------------------------ matching
def match_set(spec, values):
    kind, payload = spec
    if kind == 'any':
        return True
    if kind == 'none':
        return not values
    if kind == 'contains':
        return payload <= frozenset(values)
    return frozenset(values) == payload


def match_handler(spec, handlers):
    kind, payload = spec
    if kind == 'any':
        return True
    if kind == 'none':
        return not handlers
    return any(fnmatch.fnmatchcase(value, payload) for value in handlers)


def rule_matches(rule, feat):
    if rule['operation'] != '*' and rule['operation'] != feat['OP']:
        return False
    if rule['provider'] != '*' and rule['provider'] != feat['PV']:
        return False
    if not match_handler(rule['handler'], feat['H']):
        return False
    if not match_set(rule['gaps'], feat['G']):
        return False
    if not match_set(rule['deps'], feat['D']):
        return False
    if rule['be'] != '*' and rule['be'] != feat['BE']:
        return False
    if rule['sr'] != '*' and rule['sr'] != feat['SR']:
        return False
    if rule['files'] == '>0' and feat['P'] <= 0:
        return False
    if rule['files'] == '0' and feat['P'] != 0:
        return False
    return True


def classify(rules, feat):
    for rule in reversed(rules):
        if rule_matches(rule, feat):
            return rule
    return None


def decision(rule):
    if rule is None:
        return DEFAULT_LABEL, DEFAULT_ACTION
    return rule['label'], rule['action']


# ------------------------------------------------------------------ CLI
def _read_skill(path):
    try:
        with open(path, 'r', encoding='utf-8') as handle:
            return handle.read()
    except OSError as exc:
        raise InvocationError('--skill: %s' % (exc.strerror or exc))


def _run(ns):
    if not ns.skill:
        raise InvocationError('--skill is required with envelopes or --table-only')
    text = _read_skill(ns.skill)
    rules, info = parse_skill(text)
    if ns.table_only:
        for i, rule in enumerate(rules):
            print('%d. %s' % (i, rule['label']))
        return 0
    if not ns.envelopes:
        raise InvocationError('no envelopes given')
    out = []
    for path in ns.envelopes:
        feat = load_envelope(path)
        rule = classify(rules, feat)
        label, action = decision(rule)
        row = {'path': path, 'label': label, 'action': action,
               'rule': rules.index(rule) if rule is not None else None,
               'row': rules.index(rule) if rule is not None else None}
        if ns.json:
            row['features'] = feat
        out.append(row)
    if ns.json:
        print(json.dumps({'results': out}, indent=1, sort_keys=True))
    else:
        for row in out:
            print('%s\t%s\t%s\t%s' % (row['path'], row['label'], row['action'],
                                      row['rule']))
    return 0


# ------------------------------------------------------------------ selftest
SKELETON = ('# SKILL\n\n## Queue-drain craft\n\nCraft prose before the table.\n\n'
            '{block}\n\n## A later section\n\nProse after the craft section.\n')


def _vocab_line(tokens=None):
    return '%s %s %s' % (ACTIONS_PREFIX, tokens or VOCAB, ACTIONS_SUFFIX)


def _block(rows, marker=True, vocab_line=None, header=None, actions=True):
    header = header or HEADER
    out = []
    if marker:
        out.append(MARKER)
    if actions:
        out.append(vocab_line if vocab_line is not None else _vocab_line())
    out.append('| ' + ' | '.join(header) + ' |')
    out.append('| ' + ' | '.join(['---'] * len(header)) + ' |')
    for row in rows:
        out.append('| ' + ' | '.join(row) + ' |')
    return '\n'.join(out) + '\n'


def _skel(block):
    return SKELETON.format(block=block)


def _row(label, operation='extract_firmware', provider='unblob', handler='*',
         gaps='*', deps='*', be='*', sr='*', files='*', action='none',
         cause='cause -> action', source='selftest'):
    return [label, operation, provider, handler, gaps, deps, be, sr, files, action,
            cause, source]


def _write(work, name, text):
    path = os.path.join(work, name)
    with open(path, 'w', encoding='utf-8') as handle:
        handle.write(text)
    return path


def _dump(work, name, obj):
    return _write(work, name, json.dumps(obj, indent=1, sort_keys=True))


def _cli(args):
    return subprocess.run([sys.executable, '-I', '-B', os.path.abspath(__file__), *args],
                          capture_output=True, text=True)


def _pair(res, label):
    if res.returncode != 0:
        raise AssertionError('%s: exit %d (stderr=%r)'
                             % (label, res.returncode, res.stderr.strip()[:200]))
    lines = [l for l in res.stdout.splitlines() if l.strip()]
    if len(lines) != 1:
        raise AssertionError('%s: expected one line, got %r' % (label, lines))
    parts = lines[0].split('\t')
    return parts[1:3]


def _expect(res, want_label, want_action, label):
    got = _pair(res, label)
    if got != [want_label, want_action]:
        raise AssertionError('%s: pair %r, expected %r' % (label, got,
                                                          [want_label, want_action]))


def _env(gaps=(), deps=(), handlers=('squashfs_v4_le',), files=1, be_cmds=(),
         sr=False, provider={'id': 'unblob'}, op='extract_firmware'):
    diags = []
    for cmd in be_cmds:
        diags.append({'report': {'command': cmd}})
    if sr:
        diags.append({'report': {'__typename__': SYMLINK_TYPENAME}})
    return {'operation': op, 'provider': provider,
            'normalized_result': {
                'extraction_gaps': [{'kind': k, 'dependencies': list(d)} for k, d in gaps],
                'files': [{'relative_path': 'f%d.txt' % i} for i in range(files)],
                'chunks': [{'handler': h} for h in handlers],
                'diagnostics': diags}}


CASES = []


def case(fn):
    CASES.append(fn)
    return fn


@case
def c_table_v3_parses(work):
    skill = _write(work, 'sk-v3.md', _skel(TABLE_V3))
    res = _cli(['--skill', skill, '--table-only'])
    if res.returncode != 0:
        raise AssertionError('table-v3: exit %d' % res.returncode)


@case
def c_combined_partial_in_tree(work):
    """G = {extractor-failure, unpublished-entry}, P>0 -> partial-body-failure."""
    skill = _write(work, 'sk-c1.md', _skel(TABLE_V3))
    env = _dump(work, 'env-partial-in-tree.json',
                _env(gaps=[('extractor-failure', []), ('unpublished-entry', [])],
                     handlers=('squashfs_v4_be',), files=2))
    _expect(_cli(['--skill', skill, env]), 'partial-body-failure', 'salvage-partial',
            'partial+in-tree')


@case
def c_combined_partial_mixed(work):
    """partial precedence beats mixed: SR=yes + extractor-failure + P>0."""
    skill = _write(work, 'sk-c2.md', _skel(TABLE_V3))
    env = _dump(work, 'env-partial-mixed.json',
                _env(gaps=[('extractor-failure', []), ('unpublished-entry', [])],
                     handlers=('squashfs_v4_le',), files=1, sr=True))
    _expect(_cli(['--skill', skill, env]), 'partial-body-failure', 'salvage-partial',
            'partial+mixed')


@case
def c_combined_depth_in_tree(work):
    """G = {depth-limited, unpublished-entry}, P>0 -> depth-limited-nested."""
    skill = _write(work, 'sk-c3.md', _skel(TABLE_V3))
    env = _dump(work, 'env-depth-in-tree.json',
                _env(gaps=[('depth-limited', []), ('unpublished-entry', [])],
                     files=1))
    _expect(_cli(['--skill', skill, env]), 'depth-limited-nested', 'audit-depth',
            'depth+in-tree')


@case
def c_combined_depth_mixed(work):
    """depth precedence beats mixed: SR=yes + depth-limited."""
    skill = _write(work, 'sk-c4.md', _skel(TABLE_V3))
    env = _dump(work, 'env-depth-mixed.json',
                _env(gaps=[('depth-limited', []), ('unpublished-entry', [])],
                     files=0, sr=True))
    _expect(_cli(['--skill', skill, env]), 'depth-limited-nested', 'audit-depth',
            'depth+mixed')


@case
def c_depth_alone(work):
    skill = _write(work, 'sk-c5.md', _skel(TABLE_V3))
    env = _dump(work, 'env-depth.json', _env(gaps=[('depth-limited', [])], files=1))
    _expect(_cli(['--skill', skill, env]), 'depth-limited-nested', 'audit-depth',
            'depth-alone')


@case
def c_plain_partial_still_partial(work):
    """A single-gap envelope must not be swallowed by a direction-flipped contains."""
    skill = _write(work, 'sk-c6.md', _skel(TABLE_V3))
    env = _dump(work, 'env-partial.json',
                _env(gaps=[('extractor-failure', [])], handlers=('squashfs_v4_be',),
                     files=1))
    _expect(_cli(['--skill', skill, env]), 'partial-body-failure', 'salvage-partial',
            'plain-partial')


@case
def c_contains_in_deps_rejected(work):
    """⊇ is a gap-kinds operator only; a deps cell carrying it is malformed."""
    rows = [_row('x', gaps='none', deps='⊇sasquatch-v4be')]
    skill = _write(work, 'sk-deps-contains.md', _skel(_block(rows)))
    res = _cli(['--skill', skill, _dump(work, 'env-simple.json', _env())])
    if res.returncode != 2:
        raise AssertionError('deps-contains: exit %d, expected 2' % res.returncode)


@case
def c_contains_repeated_member_rejected(work):
    rows = [_row('x', gaps='⊇unpublished-entry+unpublished-entry')]
    skill = _write(work, 'sk-contains-dup.md', _skel(_block(rows)))
    res = _cli(['--skill', skill, _dump(work, 'env-simple.json', _env())])
    if res.returncode != 2:
        raise AssertionError('contains-dup: exit %d, expected 2' % res.returncode)


@case
def c_two_markers_first_wins(work):
    first = _block([_row('first-table')])
    second = _block([_row('second-table', action='inspect-input')])
    skill = _write(work, 'sk-two-markers.md',
                   _skel(first + '\nprose between the two tables\n\n' + second))
    _expect(_cli(['--skill', skill, _dump(work, 'env-simple.json', _env())]),
            'first-table', 'none', 'two-markers')


@case
def c_none_set_cell_rejects_nonempty(work):
    rows = [_row('trap', handler='squashfs_v4_le', gaps='none', deps='*',
                 be='*', sr='no', files='>0', action='inspect-input'),
            _row('right', handler='squashfs_v4_le', gaps='unpublished-entry',
                 deps='none', be='n/a', sr='no', files='>0', action='count-gap')]
    skill = _write(work, 'sk-none-trap.md', _skel(_block(rows)))
    env = _dump(work, 'env-gapped.json',
                _env(gaps=[('unpublished-entry', [])], files=1))
    _expect(_cli(['--skill', skill, env]), 'right', 'count-gap', 'none-trap')


@case
def c_repeated_set_member_rejected(work):
    rows = [_row('dup', gaps='unpublished-entry+unpublished-entry')]
    skill = _write(work, 'sk-repeated-member.md', _skel(_block(rows)))
    res = _cli(['--skill', skill, _dump(work, 'env-simple.json', _env())])
    if res.returncode != 2:
        raise AssertionError('repeated-member: exit %d, expected 2' % res.returncode)


@case
def c_string_provider_used(work):
    rows = [_row('strprov', provider='unblob')]
    skill = _write(work, 'sk-strprov.md', _skel(_block(rows)))
    env = _dump(work, 'env-strprov.json',
                {'operation': 'extract_firmware', 'provider': 'unblob',
                 'normalized_result': {'extraction_gaps': [],
                                       'files': [{'relative_path': 'a.txt'}],
                                       'chunks': [{'handler': 'squashfs_v4_le'}],
                                       'diagnostics': []}})
    _expect(_cli(['--skill', skill, env]), 'strprov', 'none', 'string-provider')


@case
def c_blank_lines_tolerated(work):
    blk = _block([_row('x')])
    blk = blk.replace(_vocab_line() + '\n| ', _vocab_line() + '\n\n\n| ', 1)
    skill = _write(work, 'sk-blank-lines.md', _skel(blk))
    _expect(_cli(['--skill', skill, _dump(work, 'env-simple.json', _env())]),
            'x', 'none', 'blank-lines')


@case
def c_nr_diagnostics_be_source(work):
    rows = [_row('avmR', handler='squashfs_v4_be', gaps='extractor-failure',
                 deps='none', be='no', sr='*', files='0', action='preserve-failure')]
    skill = _write(work, 'sk-nrdiag.md', _skel(_block(rows)))
    env = _dump(work, 'env-nrdiag.json',
                _env(gaps=[('extractor-failure', [])], handlers=('squashfs_v4_be',),
                     files=0, be_cmds=('/opt/sasquatch-v4be 4 /tmp/c.sqsh /out',)))
    _expect(_cli(['--skill', skill, env]), 'avmR', 'preserve-failure', 'nr-diag-be')


@case
def c_marker_absent(work):
    skill = _write(work, 'sk-nomarker.md',
                   _skel(_block([_row('x')], marker=False)))
    res = _cli(['--skill', skill, _dump(work, 'env-simple.json', _env())])
    if res.returncode != 2:
        raise AssertionError('marker-absent: exit %d, expected 2' % res.returncode)


@case
def c_no_contains_operator_rejected(work):
    """Kill-control 'no contains-operator': a v3 table without any ⊇ cell must
    not be able to express the combined rows — here: a table whose partial row
    uses the exact form must NOT give the partial label to a combined envelope."""
    rows = [_row('partial-exact', handler='squashfs_v4_*',
                 gaps='extractor-failure+unpublished-entry', deps='none', be='*',
                 sr='*', files='>0', action='salvage-partial')]
    skill = _write(work, 'sk-no-contains.md', _skel(_block(rows)))
    env = _dump(work, 'env-partial-only.json',
                _env(gaps=[('extractor-failure', [])], files=1))
    res = _cli(['--skill', skill, env])
    got = None if res.returncode else _pair(res, 'no-contains')[0]
    if got == 'partial-exact':
        raise AssertionError('no-contains: exact row matched a single-gap envelope')


def selftest():
    work = tempfile.mkdtemp(dir=os.environ.get('TMPDIR') or None,
                            prefix='v3-interp-preview-selftest.')
    failures = []
    for fn in CASES:
        try:
            fn(work)
        except AssertionError as exc:
            failures.append(str(exc))
        except Exception as exc:  # noqa: BLE001
            failures.append('%s: %s' % (fn.__name__, exc))
    print('SELFTEST cases=%d pass=%d fail=%d'
          % (len(CASES), len(CASES) - len(failures), len(failures)))
    for f in failures:
        print('FAIL %s' % f)
    return 0 if not failures else 1


def main(argv=None):
    parser = argparse.ArgumentParser(prog='v3-interp-preview.py')
    parser.add_argument('--skill')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--table-only', action='store_true')
    parser.add_argument('--selftest', action='store_true')
    parser.add_argument('envelopes', nargs='*', metavar='ENVELOPE.json')
    ns = parser.parse_args(argv)
    if ns.selftest:
        return selftest()
    try:
        return _run(ns)
    except (TableError, EnvelopeError, InvocationError) as exc:
        print('error: %s' % exc, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
