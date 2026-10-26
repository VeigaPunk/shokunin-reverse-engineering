#!/usr/bin/env python3
"""sqfs-triage.py - executable SquashFS extract-firmware outcome triage.

Reads exactly two surfaces and nothing else:

  * a SKILL.md document, from which it takes the FIRST markdown table that follows a
    line containing the marker ``<!-- sqfs-triage-table v1 -->`` inside the
    ``## Queue-drain craft`` section (that heading line up to the next ``## `` heading);
  * REA ``extract-firmware`` envelopes (rea-agents 6.5.0), recorded as either a bare
    ``data`` object or a full CLI envelope ``{ok, data, meta}``.

It prints one class label per envelope.  It never invokes REA, unblob or sasquatch, never
reads a carrier, and never writes anything.

Table grammar (columns, in this order, exact header names)
---------------------------------------------------------
  label | handler | gap kinds | dependencies | -be in child argv | symlink removed |
  published files | cause -> action | source

Condition cells, after stripping surrounding backticks and whitespace:

  handler            ``*`` (anything, including no handler), ``none`` (no squashfs chunk),
                     or an fnmatch pattern that must match at least one ``squashfs*``
                     chunk handler.
  gap kinds          ``*``, ``none`` (empty set), or ``a+b`` meaning the set of
  dependencies       ``extraction_gaps[].kind`` / ``.dependencies`` values equals exactly
                     {a, b}; a single name means exactly that singleton.
  -be in child argv  ``yes`` / ``no`` / ``n/a`` / ``*``.
  symlink removed    ``yes`` / ``no`` / ``n/a`` / ``*``.
  published files    ``0`` / ``>0`` / ``*``.
  cause -> action    non-empty prose containing ``->``.  Documentation only.
  source             non-empty citation prose.  Documentation only.

Rules are tried top to bottom; the first rule whose every condition cell matches wins.
No match prints ``unclassified``.  A malformed cell, header, separator or envelope makes
the whole run unevaluable: exit 2, never a silent non-match.

Features (from the envelope)
----------------------------
  H   set of ``normalized_result.chunks[].handler`` values starting with ``squashfs``
  G   set of ``normalized_result.extraction_gaps[].kind``
  D   union of ``normalized_result.extraction_gaps[].dependencies``
  BE  ``yes`` if any extractor command naming sasquatch carries a standalone ``-be``
      token, ``no`` if such a command exists and none does, ``n/a`` if no sasquatch
      command is recorded.  Command sources: ``normalized_result.diagnostics[].report``,
      ``data.diagnostics[].report`` and any ``command`` member under ``raw_result``; a
      string command is tokenised with shlex, an argv list is used as given.
  SR  ``yes`` if any ``normalized_result.diagnostics[].report.__typename__`` is
      ``MaliciousSymlinkRemoved``, or that typename appears anywhere under
      ``raw_result``; else ``no``
  P   ``len(normalized_result.files)``

Usage
-----
  python3 -I -B sqfs-triage.py --skill SKILL.md ENVELOPE.json...   label per envelope
  python3 -I -B sqfs-triage.py --skill SKILL.md --json ENVELOPE...  features and matched row
  python3 -I -B sqfs-triage.py --skill SKILL.md --table-only        validate, print rules
  python3 -I -B sqfs-triage.py --selftest                           isolated selftest
  python3 -I -B sqfs-triage.py --print-table                        print the frozen table block

``--json`` emits one object: ``skill``, ``rules``, and ``results[]`` holding ``path``, ``label``,
``rule`` (1-based matched rule or null), ``row`` (that rule's raw cells, or null) and ``features``.

Exit codes: 0 ok, 2 table missing or malformed, envelope unreadable, or bad invocation.
``--selftest`` exits 0 iff every case passes, 1 otherwise.

Limits
------
* Cell text is split on ``|``; a literal pipe inside a cell is not supported.
* Handler patterns are matched case-sensitively with ``fnmatch.fnmatchcase``.
* ``dependencies`` is compared as a set: order and repetition in the envelope are erased.
* The table says nothing about a region wider than the envelope records; a label is a
  statement about this envelope, not about the carrier's usability.
"""

import argparse
import copy
import fnmatch
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile

MARKER = '<!-- sqfs-triage-table v1 -->'
CRAFT_PREFIX = 'queue-drain craft'
HEADER = ['label', 'handler', 'gap kinds', 'dependencies', '-be in child argv',
          'symlink removed', 'published files', 'cause -> action', 'source']
SEPARATOR_RE = None  # compiled lazily to keep module import cheap for -I runs
NAME_RE = None
HANDLER_RE = None
BE_VALUES = ('yes', 'no', 'n/a')
FILES_VALUES = ('0', '>0')
SYMLINK_TYPENAME = 'MaliciousSymlinkRemoved'

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
SELFTEST_ENVELOPES = {
    'K1': LANE + '/corpus/evidence/round-38/c1/K1/after.json',
    'K2': LANE + '/corpus/evidence/round-38/c1/K2/after.json',
    'K3': LANE + '/corpus/evidence/round-38/c1/K3/after.json',
    'K4': LANE + '/corpus/evidence/round-38/c1/K4/after.json',
    'AVM': LANE + '/.ufo/waves/round-38/w2/artifacts/R38W2AvmProbe/rea-k1-avm.json',
    'ORIG': LANE + '/.ufo/waves/round-38/w2/artifacts/R38W2AvmProbe/rea-k1-orig.json',
}
SELFTEST_SKILL = LANE + '/SKILL.md'


# --------------------------------------------------------------------------------------
# errors
# --------------------------------------------------------------------------------------

class TableError(Exception):
    """The triage table is missing or malformed."""


class EnvelopeError(Exception):
    """An envelope could not be read as an REA extract-firmware result."""


class InvocationError(Exception):
    """The command line does not select a readable surface."""


# --------------------------------------------------------------------------------------
# the frozen triage table block (also printed by --print-table)
# --------------------------------------------------------------------------------------

TABLE_BLOCK = """\
<!-- sqfs-triage-table v1 -->
| label | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | cause -> action | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| no-squashfs-chunk | `none` | `*` | `*` | `n/a` | `*` | `*` | no chunk carries a squashfs handler, so no sasquatch of either flavour ran and the envelope says nothing about endianness -> confirm the input is a v4 image (hsqs or sqsh magic at offset 0, or at an embedded ELF end) before rerunning; an absent chunk is neither an empty filesystem nor an extractor verdict | unblob 26.6.4 handler selection; dev carrier C-nochunk.bin (round-39 w1) |
| dep-missing-be | `squashfs_v4_be` | `missing-extractor-dependency` | `sasquatch-v4be` | `n/a` | `no` | `0` | the big-endian v4 handler resolved its extractor to sasquatch-v4be and that binary was not resolvable on the child PATH, so no command ran and no -be argument exists to inspect -> install the onekey-sec sasquatch-v4be 4.5.1 binary into ~/.local/bin, confirm command -v sasquatch-v4be, rerun on a fresh output directory, and do not repack the carrier | dev C-clean-be.sqsh with ~/.local/bin stripped (round-39 w1); unblob 26.6.4 squashfs.py:25-26,69 |
| dep-missing-le | `squashfs_v4_le` | `missing-extractor-dependency` | `sasquatch` | `n/a` | `no` | `0` | the little-endian v4 handler resolved its extractor to sasquatch and that binary was not resolvable on the child PATH, so no command ran -> install the LE sasquatch 4.5.1 binary (the BE binary alone does not satisfy this gap), confirm command -v sasquatch, rerun on a fresh output directory | dev C-clean-le.sqsh with ~/.local/bin stripped (round-39 w1); unblob 26.6.4 squashfs.py:25,69 |
| avm-marker-be-dropped | `squashfs_v4_be` | `extractor-failure` | `none` | `no` | `no` | `0` | the v4 big-endian superblock has mkfs_time equal to bytes_used, unblob reads that as the AVM marker and deliberately omits -be, so sasquatch-v4be runs in little-endian mode and reports a different-endianess or id-table failure while the image itself extracts with -be -> treat it as a marker artefact: read the carrier with sasquatch-v4be -be (or pin a standard superblock whose mkfs_time differs from bytes_used) and never chase this as body damage | unblob 26.6.4 handlers/filesystem/squashfs.py:48-50; probe .ufo/waves/round-38/w2/artifacts/R38W2AvmProbe/rea-k1-avm.json |
| body-extractor-failure | `squashfs_v4_be` | `extractor-failure` | `none` | `yes` | `no` | `0` | the extractor ran with -be and still failed, so the fault is in the image body or the extractor build rather than in the endianness handshake -> keep the failing command and stderr from diagnostics, re-derive the carrier from its generator, diff it against a good arm, and never patch the envelope into a success | dev C-bodyfail-be.sqsh (round-39 w1); REA 6.5.0 cli-runtime cli.js:14260-14267 |
| escaping-symlink-removed | `squashfs_v4_be` | `*` | `*` | `n/a` | `yes` | `>0` | a symlink resolved outside the extraction root, unblob removed it and reported MaliciousSymlinkRemoved, and the publication step records no gap for it -> expect the path to be absent, never materialise the link, and never compare a symlink row against the oracle regular-file list | unblob 26.6.4 extractor.py:76-92; corpus/evidence/round-38/c1/K1/after.json |
| in-tree-symlink-metadata | `squashfs_v4_be` | `unpublished-entry` | `none` | `n/a` | `no` | `>0` | a symlink resolved inside the extraction root, so the entry is retained as metadata and recorded as exactly one unpublished-entry gap while only regular files are published -> expect the same gap in every arm, count it once per in-tree link, and do not install anything or call it a sasquatch failure | REA 6.5.0 cli-runtime cli.js:14278-14286; corpus/evidence/round-38/c1/K2/after.json; dev C-intree-be.sqsh |
| clean | `squashfs_v4_be` | `none` | `none` | `n/a` | `no` | `>0` | every regular file was published, no gap was recorded and no symlink was removed -> nothing to install or fix; match files to the oracle by relative-path suffix and sha256, and ignore nested carves | corpus/evidence/round-38/c1/K3/after.json and K4/after.json; dev C-clean-be.sqsh |
"""


# --------------------------------------------------------------------------------------
# table parsing
# --------------------------------------------------------------------------------------

def _regexes():
    global SEPARATOR_RE, NAME_RE, HANDLER_RE
    if SEPARATOR_RE is None:
        import re
        SEPARATOR_RE = re.compile(r'^:?-+:?$')
        NAME_RE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.\-]*$')
        HANDLER_RE = re.compile(r'^[A-Za-z0-9_?*.\-\[\]]+$')
    return SEPARATOR_RE, NAME_RE, HANDLER_RE


def clean_cell(raw):
    """Strip whitespace and one surrounding pair of backticks from a table cell."""
    s = raw.strip()
    if len(s) >= 2 and s[0] == '`' and s[-1] == '`' and s.count('`') == 2:
        s = s[1:-1].strip()
    return s


def _is_h2(line):
    return line.startswith('## ') and not line.startswith('### ')


def craft_bounds(lines):
    """Return (start, end) line indexes of the craft section body."""
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
    sep, name_re, _ = _regexes()
    if cell in ('*', 'none'):
        return ('any', None) if cell == '*' else ('none', None)
    parts = cell.split('+')
    if any(not part for part in parts):
        raise TableError('%s cell %r has an empty set member' % (column, cell))
    for part in parts:
        if not name_re.match(part):
            raise TableError('%s cell %r has a malformed member %r' % (column, cell, part))
    if len(set(parts)) != len(parts):
        raise TableError('%s cell %r repeats a member' % (column, cell))
    return ('exact', frozenset(parts))


def _parse_handler_cell(cell):
    _, _, handler_re = _regexes()
    if cell == '*':
        return ('any', None)
    if cell == 'none':
        return ('none', None)
    if not handler_re.match(cell):
        raise TableError('handler cell %r is not *, none, or an fnmatch pattern' % cell)
    return ('pattern', cell)


def _parse_enum_cell(cell, column, values):
    if cell == '*':
        return '*'
    if cell in values:
        return cell
    raise TableError('%s cell %r is not one of %s or *' % (column, cell, ', '.join(values)))


def parse_table(lines, first_line_no):
    """Parse the rows of one markdown table into rules.  TableError when malformed."""
    sep_re, _, _ = _regexes()
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
    for offset, raw_line in enumerate(lines[2:], start=3):
        line_no = first_line_no + offset - 1
        cells = split_row(raw_line)
        if len(cells) != len(HEADER):
            raise TableError('table row at line %d has %d cells, expected %d'
                             % (line_no, len(cells), len(HEADER)))
        cells = [clean_cell(c) for c in cells]
        label, handler, gap, dep, be, sr, files, cause, source = cells
        if not label:
            raise TableError('line %d: empty label' % line_no)
        if not cause:
            raise TableError('line %d: empty cause -> action cell' % line_no)
        if '->' not in cause:
            raise TableError('line %d: cause -> action cell has no "->" separator' % line_no)
        if not source:
            raise TableError('line %d: empty source cell' % line_no)
        rules.append({
            'index': len(rules) + 1,
            'line': line_no,
            'label': label,
            'handler': _parse_handler_cell(handler),
            'gap_kinds': _parse_set_cell(gap, 'gap kinds'),
            'dependencies': _parse_set_cell(dep, 'dependencies'),
            'be': _parse_enum_cell(be, '-be in child argv', BE_VALUES),
            'symlink_removed': _parse_enum_cell(sr, 'symlink removed', BE_VALUES),
            'files': _parse_enum_cell(files, 'published files', FILES_VALUES),
            'cause': cause,
            'source': source,
            'cells': cells,
        })
    if not rules:
        raise TableError('table at line %d has no rule rows' % first_line_no)
    return rules


def parse_skill(text):
    """Return (rules, info) for the craft-section triage table of one SKILL.md."""
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
    rules = parse_table(table, i - len(table) + 1)
    return rules, {'marker_line': marker_line + 1, 'table_line': i - len(table) + 1,
                   'rules': len(rules)}


# --------------------------------------------------------------------------------------
# envelope features
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
    """Every recorded command that names a sasquatch binary, in first-seen order."""
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
    """Return the ``data`` object of a bare or full REA extract-firmware envelope."""
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


def _print_rules(skill, rules, info):
    print('skill: %s' % skill)
    print('marker line: %d  table line: %d  rules: %d'
          % (info['marker_line'], info['table_line'], info['rules']))
    for rule in rules:
        print('%d. %s' % (rule['index'], rule['label']))
        print('   handler=%r gap_kinds=%r dependencies=%r be=%r symlink_removed=%r files=%r'
              % (rule['handler'], rule['gap_kinds'], rule['dependencies'], rule['be'],
                 rule['symlink_removed'], rule['files']))
        print('   cause: %s' % rule['cause'])
        print('   source: %s' % rule['source'])


def _run(ns):
    if not ns.skill:
        raise InvocationError('--skill is required with envelopes or --table-only')
    text = _read_skill(ns.skill)
    rules, info = parse_skill(text)
    if ns.table_only:
        _print_rules(ns.skill, rules, info)
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
            'results': [{
                'path': path,
                'label': rule['label'] if rule else 'unclassified',
                'rule': rule['index'] if rule else None,
                'row': list(rule['cells']) if rule else None,
                'features': feat,
            } for path, feat, rule in results],
        }
        json.dump(payload, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write('\n')
        return 0
    for path, _feat, rule in results:
        print('%s\t%s' % (path, rule['label'] if rule else 'unclassified'))
    return 0


# --------------------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------------------

def _cli(args):
    return subprocess.run([sys.executable, '-I', '-B', os.path.abspath(__file__), *args],
                          capture_output=True, text=True)


def _require(cond, message):
    if not cond:
        raise AssertionError(message)


def _exit_is(res, expected, label):
    _require(res.returncode == expected,
             '%s: exit %d, expected %d (stderr=%r)'
             % (label, res.returncode, expected, res.stderr.strip()[:300]))


def _label_of(res, path, label):
    _exit_is(res, 0, label)
    lines = [line for line in res.stdout.splitlines() if line.strip()]
    _require(len(lines) == 1, '%s: expected one output line, got %r' % (label, lines))
    got_path, _, got = lines[0].partition('\t')
    _require(os.path.abspath(got_path) == os.path.abspath(path),
             '%s: path column %r is not %r' % (label, got_path, path))
    return got


def _expect_label(res, path, want, label):
    got = _label_of(res, path, label)
    _require(got == want, '%s: label %r, expected %r' % (label, got, want))


def _json_of(res, label):
    _exit_is(res, 0, label)
    try:
        return json.loads(res.stdout)
    except ValueError as exc:
        raise AssertionError('%s: --json output is not JSON (%s)' % (label, exc))


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


SKELETON = ('# SKILL\n\n## Queue-drain craft\n\nCraft prose before the table.\n\n'
            '{block}\n\n## A later section\n\nProse after the craft section.\n')


def _skel(block):
    return SKELETON.format(block=block)


def _block(rows, marker=True, extra_header=None):
    header = extra_header or HEADER
    out = []
    if marker:
        out.append(MARKER)
    out.append('| ' + ' | '.join(header) + ' |')
    out.append('| ' + ' | '.join(['---'] * len(header)) + ' |')
    for row in rows:
        out.append('| ' + ' | '.join(row) + ' |')
    return '\n'.join(out) + '\n'


def _row(label, handler='*', gaps='*', deps='*', be='*', sr='*', files='*',
         cause='cause -> action', source='selftest'):
    return [label, handler, gaps, deps, be, sr, files, cause, source]


def _skill_outside(block):
    return ('# SKILL\n\n## Queue-drain craft\n\nNo table here.\n\n'
            '## A later section\n\n' + block + '\n')


def _variant_dep(work, name, handler, dep):
    env = copy.deepcopy(_load(SELFTEST_ENVELOPES['K1']))
    nr = env['normalized_result']
    nr['chunks'] = [{'handler': handler, 'input_path': '$input', 'range': {'offset': 0, 'length': 10}}]
    nr['files'] = []
    nr['unpublished_entries'] = []
    nr['diagnostics'] = []
    nr['extraction_gaps'] = [{'kind': 'missing-extractor-dependency',
                              'handler': handler,
                              'input_path': '$input',
                              'dependencies': [dep]}]
    env.pop('raw_result', None)
    return _dump(work, name, env)


def _variant_gaps(work, name, gaps):
    env = copy.deepcopy(_load(SELFTEST_ENVELOPES['K1']))
    nr = env['normalized_result']
    nr['extraction_gaps'] = gaps
    nr['diagnostics'] = []
    env.pop('raw_result', None)
    return _dump(work, name, env)


def _variant_command(work, name, transform):
    env = copy.deepcopy(_load(SELFTEST_ENVELOPES['AVM']))
    nr = env['data']['normalized_result']
    for diag in nr.get('diagnostics') or []:
        report = diag.get('report') or {}
        if 'command' in report:
            report['command'] = transform(report['command'])
    for found in _iter_dicts(env['data'].get('raw_result')):
        if 'command' in found:
            found['command'] = transform(found['command'])
    return _dump(work, name, env)


CASES = []


def case(fn):
    CASES.append(fn)
    return fn


@case
def c_green_parse(work):
    path = _write(work, 'sk-green.md', _skel(TABLE_BLOCK))
    res = _cli(['--skill', path, SELFTEST_ENVELOPES['K1']])
    _expect_label(res, SELFTEST_ENVELOPES['K1'], 'escaping-symlink-removed', 'green-parse')


@case
def c_first_match_order(work):
    rows = [_row('first', 'squashfs_v4_be', 'none', 'none', 'n/a', 'yes', '>0'),
            _row('second', 'squashfs_v4_be', 'none', 'none', 'n/a', 'yes', '>0')]
    path = _write(work, 'sk-order.md', _skel(_block(rows)))
    res = _cli(['--skill', path, SELFTEST_ENVELOPES['K1']])
    _expect_label(res, SELFTEST_ENVELOPES['K1'], 'first', 'first-match-order')


@case
def c_star_handler(work):
    rows = [_row('star', '*', 'unpublished-entry', 'none', '*', '*', '>0')]
    path = _write(work, 'sk-star.md', _skel(_block(rows)))
    res = _cli(['--skill', path, SELFTEST_ENVELOPES['K2']])
    _expect_label(res, SELFTEST_ENVELOPES['K2'], 'star', 'star-handler')


@case
def c_none_cells(work):
    env = copy.deepcopy(_load(SELFTEST_ENVELOPES['K1']))
    nr = env['normalized_result']
    nr['chunks'] = []
    nr['extraction_gaps'] = []
    path_env = _dump(work, 'env-nochunk.json', env)
    rows = [_row('noneall', 'none', 'none', 'none', 'n/a', 'yes', '>0')]
    path = _write(work, 'sk-none.md', _skel(_block(rows)))
    res = _cli(['--skill', path, path_env])
    _expect_label(res, path_env, 'noneall', 'none-cells')


@case
def c_exact_gap_hit(work):
    rows = [_row('exact', 'squashfs_v4_be', 'unpublished-entry', 'none', 'n/a', 'no', '>0')]
    path = _write(work, 'sk-exact.md', _skel(_block(rows)))
    res = _cli(['--skill', path, SELFTEST_ENVELOPES['K2']])
    _expect_label(res, SELFTEST_ENVELOPES['K2'], 'exact', 'exact-gap-hit')


@case
def c_exact_gap_miss(work):
    rows = [_row('both', 'squashfs_v4_be', 'unpublished-entry+extractor-failure', 'none',
                 'n/a', 'no', '>0'),
            _row('single', 'squashfs_v4_be', 'unpublished-entry', 'none', 'n/a', 'no', '>0')]
    path = _write(work, 'sk-exactmiss.md', _skel(_block(rows)))
    res = _cli(['--skill', path, SELFTEST_ENVELOPES['K2']])
    _expect_label(res, SELFTEST_ENVELOPES['K2'], 'single', 'exact-gap-miss')


@case
def c_exact_gap_superset(work):
    env = _variant_gaps(work, 'env-twogaps.json',
                        [{'kind': 'unpublished-entry', 'dependencies': []},
                         {'kind': 'depth-limited', 'dependencies': []}])
    rows = [_row('one', 'squashfs_v4_be', 'unpublished-entry', 'none', 'n/a', 'no', '>0'),
            _row('pair', 'squashfs_v4_be', 'unpublished-entry+depth-limited', 'none',
                 'n/a', 'no', '>0')]
    path = _write(work, 'sk-superset.md', _skel(_block(rows)))
    res = _cli(['--skill', path, '--json', env])
    payload = _json_of(res, 'exact-gap-superset')
    _require(sorted(payload['results'][0]['features']['G']) == ['depth-limited',
                                                                'unpublished-entry'],
             'exact-gap-superset: G is %r' % payload['results'][0]['features']['G'])
    _require(payload['results'][0]['label'] == 'pair',
             'exact-gap-superset: label is %r (a singleton row must not match a two-kind '
             'envelope)' % payload['results'][0]['label'])


@case
def c_exact_dep_superset(work):
    env = _variant_gaps(work, 'env-twodeps.json',
                        [{'kind': 'missing-extractor-dependency',
                          'dependencies': ['sasquatch', 'sasquatch-v4be']}])
    rows = [_row('single', 'squashfs_v4_be', 'missing-extractor-dependency', 'sasquatch',
                 'n/a', 'no', '>0'),
            _row('both', 'squashfs_v4_be', 'missing-extractor-dependency',
                 'sasquatch+sasquatch-v4be', 'n/a', 'no', '>0')]
    path = _write(work, 'sk-depsuperset.md', _skel(_block(rows)))
    res = _cli(['--skill', path, env])
    _expect_label(res, env, 'both', 'exact-dep-superset')


@case
def c_none_handler_rejects(work):
    rows = [_row('nochunk', 'none', 'none', 'none', 'n/a', 'yes', '>0')]
    path = _write(work, 'sk-nonereject.md', _skel(_block(rows)))
    res = _cli(['--skill', path, SELFTEST_ENVELOPES['K1']])
    _expect_label(res, SELFTEST_ENVELOPES['K1'], 'unclassified', 'none-handler-rejects')


@case
def c_be_token_not_substring(work):
    def rewrite(_cmd):
        return 'sasquatch-v4be --be=1 -be-check -no-exit-code -f -d out in'
    env = _variant_command(work, 'env-besubstring.json', rewrite)
    skill = _write(work, 'sk-besub.md', _skel(TABLE_BLOCK))
    res = _cli(['--skill', skill, '--json', env])
    payload = _json_of(res, 'be-token-not-substring')
    _require(payload['results'][0]['features']['BE'] == 'no',
             'be-token-not-substring: BE is %r (only a standalone -be token counts)'
             % payload['results'][0]['features']['BE'])


@case
def c_exact_dep_be(work):
    env = _variant_dep(work, 'env-depbe.json', 'squashfs_v4_be', 'sasquatch-v4be')
    path = _write(work, 'sk-depbe.md', _skel(TABLE_BLOCK))
    res = _cli(['--skill', path, env])
    _expect_label(res, env, 'dep-missing-be', 'exact-dep-be')


@case
def c_exact_dep_le(work):
    env = _variant_dep(work, 'env-deple.json', 'squashfs_v4_le', 'sasquatch')
    path = _write(work, 'sk-deple.md', _skel(TABLE_BLOCK))
    res = _cli(['--skill', path, env])
    _expect_label(res, env, 'dep-missing-le', 'exact-dep-le')


@case
def c_fnmatch_handler(work):
    rows = [_row('pat', 'squashfs_v4_?e', '*', '*', 'n/a', '*', '>0')]
    path = _write(work, 'sk-pat.md', _skel(_block(rows)))
    res = _cli(['--skill', path, SELFTEST_ENVELOPES['K2']])
    _expect_label(res, SELFTEST_ENVELOPES['K2'], 'pat', 'fnmatch-handler')


@case
def c_malformed_header(work):
    header = list(HEADER)
    header[2] = 'gaps'
    rows = [_row('x')]
    path = _write(work, 'sk-badhdr.md', _skel(_block(rows, extra_header=header)))
    res = _cli(['--skill', path, SELFTEST_ENVELOPES['K1']])
    _exit_is(res, 2, 'malformed-header')
    _require('header' in res.stderr, 'malformed-header: stderr does not say header')


@case
def c_malformed_cell(work):
    rows = [_row('x', '*', '*', '*', '*', '*', 'many')]
    path = _write(work, 'sk-badcell.md', _skel(_block(rows)))
    res = _cli(['--skill', path, SELFTEST_ENVELOPES['K1']])
    _exit_is(res, 2, 'malformed-cell')
    _require('published files' in res.stderr, 'malformed-cell: stderr does not name the column')


@case
def c_malformed_set_cell(work):
    rows = [_row('x', '*', 'unpublished-entry+', '*')]
    path = _write(work, 'sk-badset.md', _skel(_block(rows)))
    res = _cli(['--skill', path, SELFTEST_ENVELOPES['K2']])
    _exit_is(res, 2, 'malformed-set-cell')


@case
def c_table_outside_section(work):
    path = _write(work, 'sk-outside.md', _skill_outside(TABLE_BLOCK))
    res = _cli(['--skill', path, SELFTEST_ENVELOPES['K1']])
    _exit_is(res, 2, 'table-outside-section')
    _require('marker' in res.stderr, 'table-outside-section: stderr does not name the marker')


@case
def c_marker_absent(work):
    path = _write(work, 'sk-nomarker.md', _skel(_block([_row('x')], marker=False)))
    res = _cli(['--skill', path, SELFTEST_ENVELOPES['K1']])
    _exit_is(res, 2, 'marker-absent')


@case
def c_marker_without_table(work):
    path = _write(work, 'sk-notable.md',
                  _skel(MARKER + '\n\nOnly prose follows the marker.\n'))
    res = _cli(['--skill', path, SELFTEST_ENVELOPES['K1']])
    _exit_is(res, 2, 'marker-without-table')
    _require('no markdown table' in res.stderr,
             'marker-without-table: stderr does not say the table is absent')


@case
def c_bare_vs_full(work):
    bare = _load(SELFTEST_ENVELOPES['K1'])
    full = {'ok': True, 'data': bare, 'meta': {'verb': 'extract-firmware'}}
    path_bare = _dump(work, 'env-bare.json', bare)
    path_full = _dump(work, 'env-full.json', full)
    skill = _write(work, 'sk-both.md', _skel(TABLE_BLOCK))
    res = _cli(['--skill', skill, '--json', path_bare, path_full])
    payload = _json_of(res, 'bare-vs-full')
    _require(len(payload['results']) == 2, 'bare-vs-full: expected two results')
    left, right = payload['results']
    _require(left['features'] == right['features'],
             'bare-vs-full: features differ %r vs %r' % (left['features'], right['features']))
    _require(left['label'] == right['label'], 'bare-vs-full: labels differ')


@case
def c_be_yes(work):
    def add_be(cmd):
        tokens = command_tokens(cmd)
        if isinstance(cmd, str):
            return 'sasquatch-v4be -be ' + cmd.split(None, 1)[1] if len(tokens) > 1 else cmd + ' -be'
        return ['sasquatch-v4be', '-be'] + tokens[1:]
    env = _variant_command(work, 'env-be-yes.json', add_be)
    skill = _write(work, 'sk-beyes.md', _skel(TABLE_BLOCK))
    res = _cli(['--skill', skill, '--json', env])
    payload = _json_of(res, 'be-yes')
    _require(payload['results'][0]['features']['BE'] == 'yes',
             'be-yes: BE is %r' % payload['results'][0]['features']['BE'])
    _require(payload['results'][0]['label'] == 'body-extractor-failure',
             'be-yes: label is %r' % payload['results'][0]['label'])


@case
def c_be_no(work):
    skill = _write(work, 'sk-beno.md', _skel(TABLE_BLOCK))
    res = _cli(['--skill', skill, '--json', SELFTEST_ENVELOPES['AVM']])
    payload = _json_of(res, 'be-no')
    features = payload['results'][0]['features']
    _require(features['BE'] == 'no', 'be-no: BE is %r' % features['BE'])
    _require(payload['results'][0]['label'] == 'avm-marker-be-dropped',
             'be-no: label is %r' % payload['results'][0]['label'])


@case
def c_be_na(work):
    skill = _write(work, 'sk-bena.md', _skel(TABLE_BLOCK))
    res = _cli(['--skill', skill, '--json', SELFTEST_ENVELOPES['K3']])
    payload = _json_of(res, 'be-na')
    features = payload['results'][0]['features']
    _require(features['BE'] == 'n/a', 'be-na: BE is %r' % features['BE'])
    _require(payload['results'][0]['label'] == 'clean',
             'be-na: label is %r' % payload['results'][0]['label'])


@case
def c_be_argv_list(work):
    def to_list(cmd):
        tokens = command_tokens(cmd)
        return tokens
    env_list = _variant_command(work, 'env-argv.json', to_list)
    skill = _write(work, 'sk-argv.md', _skel(TABLE_BLOCK))
    res = _cli(['--skill', skill, '--json', env_list])
    payload = _json_of(res, 'be-argv-list')
    _require(payload['results'][0]['features']['BE'] == 'no',
             'be-argv-list: BE is %r' % payload['results'][0]['features']['BE'])
    _require(payload['results'][0]['label'] == 'avm-marker-be-dropped',
             'be-argv-list: label is %r' % payload['results'][0]['label'])


@case
def c_sr_from_diagnostics(work):
    skill = _write(work, 'sk-srdiag.md', _skel(TABLE_BLOCK))
    res = _cli(['--skill', skill, '--json', SELFTEST_ENVELOPES['K1']])
    payload = _json_of(res, 'sr-diagnostics')
    _require(payload['results'][0]['features']['SR'] == 'yes',
             'sr-diagnostics: SR is %r' % payload['results'][0]['features']['SR'])


@case
def c_sr_from_raw_result(work):
    env = copy.deepcopy(_load(SELFTEST_ENVELOPES['K3']))
    env['raw_result']['report'] = [{'report': {'__typename__': SYMLINK_TYPENAME,
                                               'severity': 'WARNING'}}]
    path = _dump(work, 'env-srraw.json', env)
    skill = _write(work, 'sk-srraw.md', _skel(TABLE_BLOCK))
    res = _cli(['--skill', skill, '--json', path])
    payload = _json_of(res, 'sr-raw-result')
    _require(payload['results'][0]['features']['SR'] == 'yes',
             'sr-raw-result: SR is %r' % payload['results'][0]['features']['SR'])
    _require(payload['results'][0]['label'] == 'escaping-symlink-removed',
             'sr-raw-result: label is %r' % payload['results'][0]['label'])


@case
def c_published_files(work):
    skill = _write(work, 'sk-files.md', _skel(TABLE_BLOCK))
    res = _cli(['--skill', skill, '--json', SELFTEST_ENVELOPES['AVM'], SELFTEST_ENVELOPES['K3']])
    payload = _json_of(res, 'published-files')
    zero, positive = (entry['features']['P'] for entry in payload['results'])
    _require(zero == 0, 'published-files: AVM P is %r' % zero)
    _require(positive > 0, 'published-files: K3 P is %r' % positive)
    _require(payload['results'][0]['label'] == 'avm-marker-be-dropped',
             'published-files: AVM label is %r' % payload['results'][0]['label'])
    _require(payload['results'][1]['label'] == 'clean',
             'published-files: K3 label is %r' % payload['results'][1]['label'])


@case
def c_json_row_cells(work):
    skill = _write(work, 'sk-jsonrow.md', _skel(TABLE_BLOCK))
    res = _cli(['--skill', skill, '--json', SELFTEST_ENVELOPES['K1']])
    payload = _json_of(res, 'json-row-cells')
    entry = payload['results'][0]
    _require(len(entry['row']) == len(HEADER),
             'json-row-cells: row has %r cells' % len(entry['row']))
    _require(entry['row'][0] == 'escaping-symlink-removed',
             'json-row-cells: row label is %r' % entry['row'][0])
    _require(entry['row'][4] == 'n/a' and entry['row'][5] == 'yes',
             'json-row-cells: row condition cells are %r' % entry['row'])
    _require(entry['rule'] == 6, 'json-row-cells: rule index is %r' % entry['rule'])


@case
def c_unclassified(work):
    rows = [_row('narrow', 'squashfs_v4_be', 'extractor-failure', 'none', 'yes', 'no', '0')]
    path = _write(work, 'sk-unclassified.md', _skel(_block(rows)))
    res = _cli(['--skill', path, SELFTEST_ENVELOPES['K2']])
    _expect_label(res, SELFTEST_ENVELOPES['K2'], 'unclassified', 'unclassified')


@case
def c_envelope_unreadable(work):
    skill = _write(work, 'sk-unread.md', _skel(TABLE_BLOCK))
    missing = os.path.join(work, 'absent.json')
    res = _cli(['--skill', skill, missing])
    _exit_is(res, 2, 'envelope-missing')
    empty = _write(work, 'empty.json', '{}')
    res = _cli(['--skill', skill, empty])
    _exit_is(res, 2, 'envelope-no-normalized-result')
    bad = _write(work, 'bad.json', '{not json')
    res = _cli(['--skill', skill, bad])
    _exit_is(res, 2, 'envelope-bad-json')


@case
def c_table_only(work):
    skill = _write(work, 'sk-tableonly.md', _skel(TABLE_BLOCK))
    res = _cli(['--skill', skill, '--table-only'])
    _exit_is(res, 0, 'table-only')
    for label in ('no-squashfs-chunk', 'dep-missing-be', 'dep-missing-le',
                  'avm-marker-be-dropped', 'body-extractor-failure',
                  'escaping-symlink-removed', 'in-tree-symlink-metadata', 'clean'):
        _require(label in res.stdout, 'table-only: label %r missing from output' % label)
    _require('rules: 8' in res.stdout, 'table-only: rule count missing from output')


@case
def c_real_skill(work):
    with open(SELFTEST_SKILL, 'r', encoding='utf-8') as handle:
        lines = handle.read().splitlines()
    start = None
    for i, line in enumerate(lines):
        if _is_h2(line) and line[3:].strip().lower().startswith(CRAFT_PREFIX):
            start = i
            break
    _require(start is not None, 'real-skill: no craft heading in %s' % SELFTEST_SKILL)
    inserted = lines[:start + 1] + ['', TABLE_BLOCK] + lines[start + 1:]
    path = _write(work, 'sk-real.md', '\n'.join(inserted) + '\n')
    res = _cli(['--skill', path, SELFTEST_ENVELOPES['K2']])
    _expect_label(res, SELFTEST_ENVELOPES['K2'], 'in-tree-symlink-metadata', 'real-skill')


@case
def c_first_table_wins(work):
    two = _block([_row('first-table')], marker=True, extra_header=None)
    second = _block([_row('second-table')])
    path = _write(work, 'sk-twotables.md',
                  '# SKILL\n\n## Queue-drain craft\n\n' + MARKER + '\n\n'
                  + two + '\nprose\n\n' + second + '\n')
    res = _cli(['--skill', path, SELFTEST_ENVELOPES['K2']])
    _expect_label(res, SELFTEST_ENVELOPES['K2'], 'first-table', 'first-table-wins')


@case
def c_print_table(work):
    res = _cli(['--print-table'])
    _exit_is(res, 0, 'print-table')
    _require(res.stdout == TABLE_BLOCK, 'print-table: stdout is not the frozen block')
    path = _write(work, 'sk-printed.md', _skel(res.stdout))
    res = _cli(['--skill', path, '--table-only'])
    _exit_is(res, 0, 'print-table-reparses')


@case
def c_avm_and_clean_committed(work):
    skill = _write(work, 'sk-committed.md', _skel(TABLE_BLOCK))
    for key, want in (('K1', 'escaping-symlink-removed'),
                      ('K2', 'in-tree-symlink-metadata'),
                      ('K3', 'clean'),
                      ('K4', 'clean'),
                      ('AVM', 'avm-marker-be-dropped'),
                      ('ORIG', 'escaping-symlink-removed')):
        path = SELFTEST_ENVELOPES[key]
        _require(os.path.exists(path), 'committed: %s envelope missing' % key)
        res = _cli(['--skill', skill, path])
        _expect_label(res, path, want, 'committed-' + key)


def selftest():
    work = tempfile.mkdtemp(dir=os.environ.get('TMPDIR') or None,
                            prefix='sqfs-triage-selftest.')
    passed = 0
    failures = []
    try:
        for fn in CASES:
            name = fn.__name__[2:].replace('_', '-')
            try:
                fn(work)
            except AssertionError as exc:
                failures.append((name, str(exc)))
                print('FAIL %s: %s' % (name, exc))
            except Exception as exc:  # noqa: BLE001 - a crashing case is a failing case
                failures.append((name, '%s: %s' % (type(exc).__name__, exc)))
                print('FAIL %s: %s: %s' % (name, type(exc).__name__, exc))
            else:
                passed += 1
                print('ok %s' % name)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    total = len(CASES)
    print('SELFTEST cases=%d pass=%d fail=%d' % (total, passed, total - passed))
    return 0 if passed == total else 1


# --------------------------------------------------------------------------------------
# entry point
# --------------------------------------------------------------------------------------

def main(argv=None):
    parser = argparse.ArgumentParser(
        prog='sqfs-triage.py',
        description='Label REA extract-firmware envelopes with the SKILL.md craft-section '
                    'SquashFS triage table.')
    parser.add_argument('--skill', metavar='SKILL.md',
                        help='document holding the craft-section triage table')
    parser.add_argument('--json', action='store_true',
                        help='print features and the matched rule as JSON')
    parser.add_argument('--table-only', action='store_true',
                        help='validate the table and print the parsed rules')
    parser.add_argument('--selftest', action='store_true',
                        help='run the isolated selftest')
    parser.add_argument('--print-table', action='store_true',
                        help='print the frozen triage table block')
    parser.add_argument('envelopes', nargs='*', metavar='ENVELOPE.json',
                        help='REA extract-firmware envelope (bare data or full CLI envelope)')
    ns = parser.parse_args(argv)
    if ns.print_table:
        sys.stdout.write(TABLE_BLOCK)
        return 0
    if ns.selftest:
        return selftest()
    try:
        return _run(ns)
    except (TableError, EnvelopeError, InvocationError) as exc:
        sys.stderr.write('sqfs-triage: %s\n' % exc)
        return 2


if __name__ == '__main__':
    sys.exit(main())
