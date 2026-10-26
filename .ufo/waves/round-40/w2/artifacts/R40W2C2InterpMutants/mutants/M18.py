#!/usr/bin/env python3
"""sqfs-triage-v2.py - executable SquashFS extract-firmware outcome triage, table v2.

Reads exactly two surfaces and nothing else:

  * a SKILL.md document, from which it takes the FIRST markdown table that follows a
    line containing the marker ``<!-- sqfs-triage-table v2 -->`` inside the
    ``## Queue-drain craft`` section (that heading line up to the next ``## `` heading),
    plus the closed action vocabulary declared by the line directly above that table
    (``<!-- sqfs-triage-actions: token ... -->``; blank lines between it and the table
    header are allowed, any other prose is not);
  * REA envelopes (rea-agents 6.5.0), recorded as either a bare ``data`` object or a
    full CLI envelope ``{ok, data, meta}``.

It prints one ``(label, action)`` pair per envelope.  It never invokes REA, unblob or
sasquatch, never reads a carrier, and never writes anything.

Table grammar (columns, in this order, exact header names)
---------------------------------------------------------
  label | operation | provider | handler | gap kinds | dependencies |
  -be in child argv | symlink removed | published files | action | cause | source

Condition cells, after stripping surrounding backticks and whitespace:

  operation          ``*`` (any), or the exact ``data.operation`` token REA records
                     (``extract_firmware`` for the verb this table is about).
  provider           ``*`` (any), or the exact ``data.provider.id`` token REA records
                     (``unblob``).  A provider recorded as a bare string is used as is;
                     an absent provider is the empty string, which no exact cell matches.
  handler            ``*`` (anything, including no handler), ``none`` (no squashfs chunk),
                     or an fnmatch pattern that must match at least one ``squashfs*``
                     chunk handler.
  gap kinds          ``*``, ``none`` (empty set), or ``a+b`` meaning the set of
  dependencies       ``extraction_gaps[].kind`` / ``.dependencies`` values equals exactly
                     {a, b}; a single name means exactly that singleton.
  -be in child argv  ``yes`` / ``no`` / ``n/a`` / ``*``.
  symlink removed    ``yes`` / ``no`` / ``n/a`` / ``*``.
  published files    ``0`` / ``>0`` / ``*``.
  action             one token from the vocabulary line above the table; a token that
                     is not declared there makes the whole run unevaluable (exit 2).
                     Vocabulary tokens are lowercase dashed words, declared once each.
  cause -> action    non-empty prose containing ``->``.  Documentation only.
  source             non-empty citation prose.  Documentation only.

The two domain columns are the v2 guard (round-39 routed defect R39-CL1): because every
row carries an exact operation and provider, an envelope from another REA verb or another
provider matches no row and falls through to ``unclassified`` instead of borrowing a
SquashFS label.  A ``*`` domain cell is legal and deliberately weakens the guard; the
frozen table does not use one.

Rules are tried top to bottom; the first rule whose every condition cell matches wins and
supplies both the label and the action.  No match prints ``unclassified`` with action
``none``.  A malformed cell, header, separator, vocabulary line or duplicate label, and
an unreadable envelope, make the whole run unevaluable: exit 2, never a silent non-match.

Features (from the envelope)
----------------------------
  OP  ``data.operation`` (string), else ``''``
  PV  ``data.provider.id`` when ``provider`` is an object, the string itself when
      ``provider`` is a string, else ``''``
  H   set of ``normalized_result.chunks[].handler`` values starting with ``squashfs``
  G   set of ``normalized_result.extraction_gaps[].kind``
  D   union of ``normalized_result.extraction_gaps[].dependencies``
  BE  ``yes`` if any extractor command naming sasquatch carries a standalone ``-be``
      token, ``no`` if such a command exists and none does, ``n/a`` if no sasquatch
      command is recorded.  Command sources: ``normalized_result.diagnostics[].report``,
      ``data.diagnostics[].report`` and any ``command`` member under ``raw_result``; a
      string command is tokenised with shlex, an argv list is used as given.
  SR  ``yes`` if any ``normalized_result.diagnostics[].report.__typename__`` is
      ``MaliciousSymlinkRemoved``, or that typename appears anywhere under ``raw_result``;
      else ``no``
  P   ``len(normalized_result.files)``

Envelope readability
--------------------
A bare ``data`` object is accepted when it carries ``normalized_result`` (an object) or a
string ``operation``; a full ``{ok, data, meta}`` envelope is accepted when ``data`` is an
object with the same shape.  Anything else is unreadable (exit 2).  An envelope whose
``operation`` is ``extract_firmware`` must also carry a ``normalized_result`` object
(exit 2 if not); a domain-mismatched envelope may omit it, so the domain guard stays a
label decision instead of an unreadable-envelope decision.

Usage
-----
  python3 -I -B sqfs-triage-v2.py --skill SKILL.md ENVELOPE.json...
      one ``path<TAB>label<TAB>action`` line per envelope
  python3 -I -B sqfs-triage-v2.py --skill SKILL.md --json ENVELOPE...
      features, matched row index and row cells per envelope
  python3 -I -B sqfs-triage-v2.py --skill SKILL.md --table-only
      validate the table, print the parsed rules and the action vocabulary
  python3 -I -B sqfs-triage-v2.py --selftest
      isolated selftest (temporary SKILL variants under $TMPDIR)
  python3 -I -B sqfs-triage-v2.py --print-table
      print the frozen v2 table block (marker, vocabulary line, header, rows)

Exit codes: 0 ok, 2 table missing or malformed (wrong header, malformed cell, duplicate
label, unknown action, missing or misplaced vocabulary line, marker v1 only) or envelope
unreadable, 1 only for a failed ``--selftest``.

Limits
------
* Cell text is split on ``|``; a literal pipe inside a cell is not supported.
* Header names are compared case-insensitively (the v1 interpreter's rule); every other
  cell is compared exactly and case-sensitively, and handler patterns are matched with
  ``fnmatch.fnmatchcase``.
* ``gap kinds`` and ``dependencies`` compare as sets: order and repetition in the envelope
  are erased, and an envelope carrying one extra gap kind matches no exact row (it falls
  to a ``*`` row or to ``unclassified``).  Supersets are not expressible by design.
* The table says nothing about a region wider than the envelope records; a label is a
  statement about this envelope, not about the carrier's usability.
"""

import argparse
import fnmatch
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile

MARKER = '<!-- sqfs-triage-table v2 -->'
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
DEFAULT_ACTION = 'inspect-input'
OPERATION_TOKEN = 'extract_firmware'

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
HELDOUT_DIR = LANE + '/corpus/evidence/round-39/c2/heldout'
HELDOUT_MANIFEST = HELDOUT_DIR + '/manifest.json'
C1_DIR = LANE + '/corpus/evidence/round-39/c1'
SELFTEST_SKILL = LANE + '/SKILL.md'

_SEPARATOR_RE = None
_NAME_RE = None
_HANDLER_RE = None
_OPERATION_RE = None
_PROVIDER_RE = None
_ACTION_RE = None


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
# the frozen v2 table block (printed by --print-table; integrated by the L1)
# --------------------------------------------------------------------------------------

TABLE_BLOCK = """\
<!-- sqfs-triage-table v2 -->
<!-- sqfs-triage-actions: none inspect-input install-extractor-be install-extractor-le wrap-extractor-be preserve-failure salvage-partial audit-symlinks expect-link-absent count-gap confirm-empty -->
| label | operation | provider | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| no-squashfs-chunk | `extract_firmware` | `unblob` | `none` | `*` | `*` | `*` | `*` | `*` | `inspect-input` | no chunk carries a squashfs handler: unblob's finder dropped a truncated image, a bytes_used past the end or a non-4 s_major without a report, so no sasquatch of either flavour ran -> check the magic and superblock before rerunning; an empty envelope is not an empty filesystem | S112 finder v4 patterns; knowledge 2026-10-26-r39-sqfs-outcome-triage.md :50-54; R39-CL3 |
| dep-missing-be | `extract_firmware` | `unblob` | `squashfs_v4_be` | `missing-extractor-dependency` | `sasquatch-v4be` | `n/a` | `no` | `*` | `install-extractor-be` | the big-endian v4 handler resolved its extractor to sasquatch-v4be and that binary was not on the unblob child PATH, so no command ran and no argv exists -> install the onekey-sec sasquatch-v4be 4.5.1 binary on that PATH and rerun into a fresh output directory; the image is unmeasured, not unreadable; files stay * because an AppImage before-arm publishes its ELF prefix beside the same gap | S112 :68-69; S120 command.py :69-77,101-102; round-36 K3/before.json |
| dep-missing-le | `extract_firmware` | `unblob` | `squashfs_v4_le` | `missing-extractor-dependency` | `sasquatch` | `n/a` | `no` | `*` | `install-extractor-le` | the little-endian v4 handler resolved its extractor to plain sasquatch and that binary was not on the child PATH, so no command ran -> install the little-endian sasquatch 4.5.1 binary (sasquatch-v4be alone does not satisfy this gap) and rerun into a fresh output directory; an AppImage before-arm still publishes its ELF prefix and opaque container range | S112 :25,37,68-69; S120 command.py :101-102; round-36 K3/before.json |
| avm-marker-be-dropped | `extract_firmware` | `unblob` | `squashfs_v4_be` | `extractor-failure` | `none` | `no` | `*` | `*` | `wrap-extractor-be` | mkfs_time equals bytes_used, unblob read the AVM marker and deliberately omitted -be, so sasquatch-v4be read a standard-BE body with the wrong byte order and failed; the removal of -be, not damage, decides this row -> rerun through a PATH wrapper named sasquatch-v4be that appends -be (REA has no flag passthrough) and remove the wrapper afterwards | S112 :44-50; S121 -DFIX_BE build; knowledge 2026-10-26-r39-sqfs-outcome-triage.md :29-40 |
| body-extractor-failure | `extract_firmware` | `unblob` | `squashfs_v4_*` | `extractor-failure` | `none` | `*` | `*` | `0` | `preserve-failure` | the extractor ran and still failed with zero files published, so the fault is in the image body or the extractor build rather than the endianness handshake -> keep the failing command and stderr from diagnostics, diff the carrier against a known-good arm, and never patch the envelope into a success | S120 report.py :91-98; knowledge 2026-10-26-r39-sqfs-outcome-triage.md :29-40; R39-CL3 D1 |
| partial-body-failure | `extract_firmware` | `unblob` | `squashfs_v4_*` | `extractor-failure` | `none` | `*` | `*` | `>0` | `salvage-partial` | the extractor failed after publishing at least one regular file, so the envelope is a partial success that a zero-file failure row would hide -> keep the published files and the failing command, match files to the oracle only by relative-path suffix and sha256, mark the run incomplete, and never score the set as clean | R39-CL3 D1 (full-be1-xz P>0); w2/R39W2C2TableReview.md |
| mixed-symlinks | `extract_firmware` | `unblob` | `squashfs_v4_*` | `unpublished-entry` | `none` | `*` | `yes` | `*` | `audit-symlinks` | both link kinds are present in one image: one or more symlinks escaped the extraction root and were removed with a MaliciousSymlinkRemoved report, and one or more stayed in-tree as unpublished-entry gaps -> expect the escaped paths absent, count exactly one gap per kept link or special file, and never read this as permission to ignore the in-tree gaps | S118 extractor.py :50-92; S119 firmwareAnalysis.js :137-141, FirmwarePublication.js :68-75; R39-CL2; c1/K5,K6 after.json |
| escaping-symlink-removed | `extract_firmware` | `unblob` | `squashfs_v4_*` | `*` | `*` | `*` | `yes` | `*` | `expect-link-absent` | a symlink target resolved outside the extraction root, or the link looped, so unblob removed it and reported MaliciousSymlinkRemoved, and REA records no gap for the removal -> expect the path to be absent, never materialise the link, and never match a symlink row against the regular-file oracle; check for unpublished-entry gaps separately | S118 extractor.py :50-92 (loop branch :58-65); c1/K1 after.json |
| in-tree-symlink-metadata | `extract_firmware` | `unblob` | `squashfs_v4_*` | `unpublished-entry` | `none` | `*` | `no` | `*` | `count-gap` | every non-file entry resolved inside the extraction root, so it is kept as metadata and recorded as one unpublished-entry gap per entry while only regular files are published -> expected, not a sasquatch failure; count one gap per in-tree link or special file and install nothing | S119 firmwareAnalysis.js :137-141, FirmwarePublication.js :68-75,301-308; c1/K2 after.json |
| clean | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `none` | `*` | `no` | `>0` | `none` | every regular file was published, no gap was recorded and no symlink was removed -> nothing to install or fix; match files to the oracle by relative-path suffix and sha256, and ignore nested carves | c1/K3,K4 after.json; c2/H01,H02,H03,H04 |
| clean-empty | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `none` | `*` | `no` | `0` | `confirm-empty` | the extractor completed with no gap and published zero regular files because the image tree holds no regular file -> an empty result is a fact about this image, not a silent failure: confirm the independent oracle tree is empty before calling it clean, and never confuse it with the no-chunk row | R39-CL3 D2 (full-be-dirempty-gzip clean P=0); w2/R39W2C2TableReview.md |
"""


# --------------------------------------------------------------------------------------
# table parsing
# --------------------------------------------------------------------------------------

def _regexes():
    global _SEPARATOR_RE, _NAME_RE, _HANDLER_RE, _OPERATION_RE, _PROVIDER_RE, _ACTION_RE
    if _SEPARATOR_RE is None:
        import re
        _SEPARATOR_RE = re.compile(r'^:?-+:?$')
        _NAME_RE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.\-]*$')
        _HANDLER_RE = re.compile(r'^[A-Za-z0-9_?*.\-\[\]]+$')
        _OPERATION_RE = re.compile(r'^[a-z][a-z0-9_.\-]*$')
        _PROVIDER_RE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.\-]*$')
        _ACTION_RE = re.compile(r'^[a-z][a-z0-9]*(-[a-z0-9]+)*$')
    return (_SEPARATOR_RE, _NAME_RE, _HANDLER_RE, _OPERATION_RE, _PROVIDER_RE, _ACTION_RE)


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
    _, name_re, _, _, _, _ = _regexes()
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
    _, _, handler_re, _, _, _ = _regexes()
    if cell == '*':
        return ('any', None)
    if cell == 'none':
        return ('none', None)
    if not handler_re.match(cell):
        raise TableError('handler cell %r is not *, none, or an fnmatch pattern' % cell)
    return ('pattern', cell)


def _parse_domain_cell(cell, column, token_re):
    if cell == '*':
        return '*'
    if not token_re.match(cell):
        raise TableError('%s cell %r is not * or a bare token matching %s'
                         % (column, cell, token_re.pattern))
    return cell


def _parse_enum_cell(cell, column, values):
    if cell == '*':
        return '*'
    if cell in values:
        return cell
    raise TableError('%s cell %r is not one of %s or *' % (column, cell, ', '.join(values)))


def parse_actions_line(line, line_no):
    """Return the vocabulary tokens of one ``<!-- sqfs-triage-actions: ... -->`` line."""
    _, _, _, _, _, action_re = _regexes()
    s = line.strip()
    at = s.find(ACTIONS_PREFIX)
    if at < 0:
        raise TableError('line %d: no %r vocabulary line directly above the table'
                         % (line_no, ACTIONS_PREFIX))
    rest = s[at + len(ACTIONS_PREFIX):]
    if ACTIONS_SUFFIX not in rest:
        raise TableError('line %d: the action vocabulary line has no closing %r'
                         % (line_no, ACTIONS_SUFFIX))
    rest = rest[:rest.index(ACTIONS_SUFFIX)].strip()
    if not rest:
        raise TableError('line %d: the action vocabulary is empty' % line_no)
    tokens = rest.split()
    seen = []
    for token in tokens:
        if not action_re.match(token):
            raise TableError('line %d: action token %r is not a lowercase dashed token'
                             % (line_no, token))
        if token in seen:
            raise TableError('line %d: action token %r is declared twice'
                             % (line_no, token))
        seen.append(token)
    return seen


def parse_table(lines, first_line_no, vocabulary):
    """Parse the rows of one markdown table into rules.  TableError when malformed."""
    sep_re, name_re, _, operation_re, provider_re, _ = _regexes()
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
    labels = {}
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
        if not name_re.match(label):
            raise TableError('line %d: label %r is not a bare token' % (line_no, label))
        if label in labels:
            raise TableError('line %d: duplicate label %r (first on line %d)'
                             % (line_no, label, labels[label]))
        labels[label] = line_no
        if not action:
            raise TableError('line %d: empty action cell' % line_no)
        if action not in vocabulary:
            raise TableError('line %d: action %r is not declared in the vocabulary line'
                             % (line_no, action))
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
            'operation': _parse_domain_cell(operation, 'operation', operation_re),
            'provider': _parse_domain_cell(provider, 'provider', provider_re),
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
    """Return (rules, info) for the craft-section v2 triage table of one SKILL.md."""
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
        raise TableError('line %d: no %r vocabulary line directly above the table'
                         % (table_start + 1, ACTIONS_PREFIX))
    vocabulary = parse_actions_line(lines[actions_line], actions_line + 1)
    table = []
    i = table_start
    while i < end and lines[i].lstrip().startswith('|'):
        table.append(lines[i])
        i += 1
    rules = parse_table(table, table_start + 1, vocabulary)
    return rules, {'marker_line': marker_line + 1,
                   'actions_line': actions_line + 1,
                   'table_line': table_start + 1,
                   'rules': len(rules),
                   'actions': vocabulary}


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


def _has_normalized_result(obj):
    return isinstance(obj.get('normalized_result'), dict)


def envelope_data(obj, path='<envelope>'):
    """Return the ``data`` object of a bare or full REA envelope.

    A bare object is preferred when it carries ``normalized_result`` or a string
    ``operation``; otherwise the ``data`` member of a full ``{ok, data, meta}``
    envelope is used.  The selected object must then comply with the readability rule
    (``normalized_result`` object, or a string ``operation`` for a domain-mismatched
    envelope).
    """
    if not isinstance(obj, dict):
        raise EnvelopeError('%s: not a JSON object' % path)
    candidate = None
    if _has_normalized_result(obj):
        candidate = obj
    else:
        inner = obj.get('data')
        if isinstance(inner, dict):
            candidate = inner
        elif isinstance(obj.get('operation'), str):
            candidate = obj
    if candidate is None:
        raise EnvelopeError('%s: no normalized_result or operation (neither a bare data '
                            'object nor a full {ok,data,meta} envelope)' % path)
    if 'normalized_result' in candidate and not isinstance(candidate['normalized_result'],
                                                           dict):
        raise EnvelopeError('%s: normalized_result is not an object' % path)
    has_op = isinstance(candidate.get('operation'), str)
    if not _has_normalized_result(candidate) and not has_op:
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
    return {
        'OP': operation,
        'PV': provider_id,
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
    if rule['operation'] != '*' and rule['operation'] != feat['OP']:
        return False
    if rule['provider'] != '*' and rule['provider'] != feat['PV']:
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


def decision(rule):
    if rule is None:
        return DEFAULT_LABEL, DEFAULT_ACTION
    return rule['label'], rule['action']


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
    print('marker line: %d  actions line: %d  table line: %d  rules: %d'
          % (info['marker_line'], info['actions_line'], info['table_line'],
             info['rules']))
    print('actions: %s' % ' '.join(info['actions']))
    for rule in rules:
        print('%d. %s' % (rule['index'], rule['label']))
        print('   operation=%r provider=%r handler=%r gap_kinds=%r dependencies=%r'
              % (rule['operation'], rule['provider'], rule['handler'],
                 rule['gap_kinds'], rule['dependencies']))
        print('   be=%r symlink_removed=%r files=%r action=%r'
              % (rule['be'], rule['symlink_removed'], rule['files'], rule['action']))
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
            'marker_line': info['marker_line'],
            'actions_line': info['actions_line'],
            'table_line': info['table_line'],
            'rules': info['rules'],
            'actions': list(info['actions']),
            'results': [{
                'path': path,
                'label': rule['label'] if rule else DEFAULT_LABEL,
                'action': rule['action'] if rule else DEFAULT_ACTION,
                'rule': rule['index'] if rule else None,
                'row': list(rule['cells']) if rule else None,
                'features': feat,
            } for path, feat, rule in results],
        }
        json.dump(payload, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write('\n')
        return 0
    for path, _feat, rule in results:
        label, action = decision(rule)
        print('%s\t%s\t%s' % (path, label, action))
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


def _lines_of(res, label):
    _exit_is(res, 0, label)
    return [line for line in res.stdout.splitlines() if line.strip()]


def _pair_of(res, path, label):
    lines = _lines_of(res, label)
    _require(len(lines) == 1, '%s: expected one output line, got %r' % (label, lines))
    got_path, _, rest = lines[0].partition('\t')
    _require(os.path.abspath(got_path) == os.path.abspath(path),
             '%s: path column %r is not %r' % (label, got_path, path))
    label_cell, _, action = rest.partition('\t')
    _require(action != '', '%s: no action column in %r' % (label, lines[0]))
    return label_cell, action


def _expect_pair(res, path, want_label, want_action, label):
    got_label, got_action = _pair_of(res, path, label)
    _require((got_label, got_action) == (want_label, want_action),
             '%s: pair %r, expected %r' % (label, (got_label, got_action),
                                           (want_label, want_action)))


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


def _fixture(group, ident):
    if group == 'H':
        return os.path.join(HELDOUT_DIR, ident, 'envelope.json')
    return os.path.join(C1_DIR, ident, 'after.json')


SKELETON = ('# SKILL\n\n## Queue-drain craft\n\nCraft prose before the table.\n\n'
            '{block}\n\n## A later section\n\nProse after the craft section.\n')

VOCAB = 'none inspect-input install-extractor-be install-extractor-le wrap-extractor-be preserve-failure salvage-partial audit-symlinks expect-link-absent count-gap confirm-empty'


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


def _row(label, operation='extract_firmware', provider='unblob', handler='*', gaps='*',
         deps='*', be='*', sr='*', files='*', action='none',
         cause='cause -> action', source='selftest'):
    return [label, operation, provider, handler, gaps, deps, be, sr, files, action,
            cause, source]


def _skill_outside(block):
    return ('# SKILL\n\n## Queue-drain craft\n\nNo table here.\n\n'
            '## A later section\n\n' + block + '\n')


def _mutate(work, name, ident, mutate, group='H'):
    env = _load(_fixture(group, ident))
    mutate(env)
    return _dump(work, name, env)


HELDOUT_EXPECT = {
    'H01': ('clean', 'none'),
    'H02': ('clean', 'none'),
    'H03': ('clean', 'none'),
    'H04': ('clean', 'none'),
    'H05': ('escaping-symlink-removed', 'expect-link-absent'),
    'H06': ('escaping-symlink-removed', 'expect-link-absent'),
    'H07': ('in-tree-symlink-metadata', 'count-gap'),
    'H08': ('in-tree-symlink-metadata', 'count-gap'),
    'H09': ('dep-missing-be', 'install-extractor-be'),
    'H10': ('dep-missing-be', 'install-extractor-be'),
    'H11': ('dep-missing-le', 'install-extractor-le'),
    'H12': ('dep-missing-le', 'install-extractor-le'),
    'H13': ('avm-marker-be-dropped', 'wrap-extractor-be'),
    'H14': ('avm-marker-be-dropped', 'wrap-extractor-be'),
    'H15': ('body-extractor-failure', 'preserve-failure'),
    'H16': ('body-extractor-failure', 'preserve-failure'),
    'H17': ('no-squashfs-chunk', 'inspect-input'),
    'H18': ('no-squashfs-chunk', 'inspect-input'),
    'H19': ('body-extractor-failure', 'preserve-failure'),
    'H20': ('body-extractor-failure', 'preserve-failure'),
}

C1_EXPECT = {
    'K1': ('escaping-symlink-removed', 'expect-link-absent'),
    'K2': ('in-tree-symlink-metadata', 'count-gap'),
    'K3': ('clean', 'none'),
    'K4': ('clean', 'none'),
    'K5': ('mixed-symlinks', 'audit-symlinks'),
    'K6': ('mixed-symlinks', 'audit-symlinks'),
}

CASES = []


def case(fn):
    CASES.append(fn)
    return fn


@case
def c_table_only(work):
    skill = _write(work, 'sk-tableonly.md', _skel(TABLE_BLOCK))
    res = _cli(['--skill', skill, '--table-only'])
    _exit_is(res, 0, 'table-only')
    _require('rules: 11' in res.stdout, 'table-only: rule count missing from output')
    tokens_line = [l for l in res.stdout.splitlines() if l.startswith('actions: ')]
    _require(len(tokens_line) == 1, 'table-only: no single actions line')
    tokens = tokens_line[0][len('actions: '):].split()
    _require(tokens == VOCAB.split(), 'table-only: vocabulary is %r' % tokens)
    for label in ('no-squashfs-chunk', 'dep-missing-be', 'dep-missing-le',
                  'avm-marker-be-dropped', 'body-extractor-failure',
                  'partial-body-failure', 'mixed-symlinks', 'escaping-symlink-removed',
                  'in-tree-symlink-metadata', 'clean', 'clean-empty'):
        _require(label in res.stdout, 'table-only: label %r missing' % label)


@case
def c_committed_heldout(work):
    skill = _write(work, 'sk-heldout.md', _skel(TABLE_BLOCK))
    paths = [_fixture('H', ident) for ident in sorted(HELDOUT_EXPECT)]
    res = _cli(['--skill', skill, *paths])
    _exit_is(res, 0, 'committed-heldout')
    lines = res.stdout.splitlines()
    _require(len(lines) == len(paths), 'committed-heldout: %d lines for %d envelopes'
             % (len(lines), len(paths)))
    for path, line in zip(paths, lines):
        cell_path, _, rest = line.partition('\t')
        label, _, action = rest.partition('\t')
        ident = os.path.basename(os.path.dirname(cell_path))
        _require((label, action) == HELDOUT_EXPECT[ident],
                 'committed-heldout: %s -> %r, expected %r'
                 % (ident, (label, action), HELDOUT_EXPECT[ident]))


@case
def c_heldout_manifest_agrees(work):
    manifest = _load(HELDOUT_MANIFEST)
    for carrier in manifest['carriers']:
        ident = carrier['id']
        _require(ident in HELDOUT_EXPECT,
                 'heldout-manifest: %s not in the selftest expectation table' % ident)
        _require(carrier['label'] == HELDOUT_EXPECT[ident][0],
                 'heldout-manifest: %s manifest label %r, selftest expects %r'
                 % (ident, carrier['label'], HELDOUT_EXPECT[ident][0]))
    _require(len(manifest['carriers']) == len(HELDOUT_EXPECT),
             'heldout-manifest: %d carriers, %d expectations'
             % (len(manifest['carriers']), len(HELDOUT_EXPECT)))


@case
def c_committed_c1(work):
    skill = _write(work, 'sk-c1.md', _skel(TABLE_BLOCK))
    for ident, want in sorted(C1_EXPECT.items()):
        path = _fixture('K', ident)
        res = _cli(['--skill', skill, path])
        _expect_pair(res, path, want[0], want[1], 'committed-c1-' + ident)


@case
def c_mixed_before_escaping(work):
    skill = _write(work, 'sk-mixed.md', _skel(TABLE_BLOCK))
    for ident in ('K5', 'K6'):
        path = _fixture('K', ident)
        res = _cli(['--skill', skill, '--json', path])
        payload = _json_of(res, 'mixed-before-escaping-' + ident)
        entry = payload['results'][0]
        _require(entry['features']['SR'] == 'yes',
                 'mixed-before-escaping-%s: SR is %r' % (ident, entry['features']['SR']))
        _require(entry['features']['G'] == ['unpublished-entry'],
                 'mixed-before-escaping-%s: G is %r' % (ident, entry['features']['G']))
        _require(entry['label'] == 'mixed-symlinks',
                 'mixed-before-escaping-%s: label %r' % (ident, entry['label']))


@case
def c_first_match_order(work):
    rows = [_row('first', handler='squashfs_v4_be', gaps='none', deps='none',
                 be='n/a', sr='no', files='>0', action='none'),
            _row('second', handler='squashfs_v4_be', gaps='none', deps='none',
                 be='n/a', sr='no', files='>0', action='inspect-input')]
    path = _write(work, 'sk-order.md', _skel(_block(rows)))
    res = _cli(['--skill', path, _fixture('H', 'H01')])
    _expect_pair(res, _fixture('H', 'H01'), 'first', 'none', 'first-match-order')


@case
def c_star_domain_cells(work):
    rows = [_row('star', operation='*', provider='*', action='inspect-input')]
    path = _write(work, 'sk-star.md', _skel(_block(rows)))
    env = _mutate(work, 'env-outofdomain-star.json', 'H01',
                  lambda e: e.__setitem__('operation', 'inspect_firmware_regions'))
    res = _cli(['--skill', path, env])
    _expect_pair(res, env, 'star', 'inspect-input', 'star-domain-cells')


@case
def c_domain_guard_operation(work):
    skill = _write(work, 'sk-guard-op.md', _skel(TABLE_BLOCK))
    env = _mutate(work, 'env-oood-op.json', 'H01',
                  lambda e: e.__setitem__('operation', 'inspect_firmware_regions'))
    res = _cli(['--skill', skill, env])
    _expect_pair(res, env, 'unclassified', 'none', 'domain-guard-operation')


@case
def c_domain_guard_provider(work):
    skill = _write(work, 'sk-guard-pv.md', _skel(TABLE_BLOCK))
    env = _mutate(work, 'env-oood-pv.json', 'H01',
                  lambda e: e.__setitem__('provider', {'id': 'binwalk', 'name': 'binwalk',
                                                       'version': '0.8'}))
    res = _cli(['--skill', skill, env])
    _expect_pair(res, env, 'unclassified', 'none', 'domain-guard-provider')


@case
def c_domain_guard_without_normalized_result(work):
    skill = _write(work, 'sk-guard-bare.md', _skel(TABLE_BLOCK))
    env = _dump(work, 'env-oood-bare.json',
                {'operation': 'inspect_firmware_regions',
                 'provider': {'id': 'unblob', 'name': 'Unblob', 'version': '26.6.4'}})
    res = _cli(['--skill', skill, env])
    _expect_pair(res, env, 'unclassified', 'none', 'domain-guard-bare')


@case
def c_extract_envelope_without_normalized_result(work):
    skill = _write(work, 'sk-need-nr.md', _skel(TABLE_BLOCK))
    env = _dump(work, 'env-no-nr.json', {'operation': 'extract_firmware'})
    res = _cli(['--skill', skill, env])
    _exit_is(res, 2, 'extract-envelope-without-normalized-result')


@case
def c_exact_gap_hit(work):
    rows = [_row('exact', handler='squashfs_v4_be', gaps='unpublished-entry', deps='none',
                 be='n/a', sr='no', files='>0', action='count-gap')]
    path = _write(work, 'sk-exact.md', _skel(_block(rows)))
    res = _cli(['--skill', path, _fixture('H', 'H07')])
    _expect_pair(res, _fixture('H', 'H07'), 'exact', 'count-gap', 'exact-gap-hit')


@case
def c_exact_gap_superset(work):
    def two_gaps(env):
        nr = env['normalized_result']
        nr['extraction_gaps'] = [{'kind': 'unpublished-entry', 'dependencies': []},
                                 {'kind': 'depth-limited', 'dependencies': []}]
        nr['diagnostics'] = []
        env.pop('raw_result', None)

    env = _mutate(work, 'env-twogaps.json', 'H01', two_gaps)
    rows = [_row('one', handler='squashfs_v4_be', gaps='unpublished-entry', deps='none',
                 be='n/a', sr='no', files='>0', action='none'),
            _row('pair', handler='squashfs_v4_be', gaps='unpublished-entry+depth-limited',
                 deps='none', be='n/a', sr='no', files='>0', action='none')]
    path = _write(work, 'sk-superset.md', _skel(_block(rows)))
    res = _cli(['--skill', path, '--json', env])
    payload = _json_of(res, 'exact-gap-superset')
    _require(payload['results'][0]['features']['G'] == ['depth-limited',
                                                        'unpublished-entry'],
             'exact-gap-superset: G is %r' % payload['results'][0]['features']['G'])
    _require(payload['results'][0]['label'] == 'pair',
             'exact-gap-superset: label is %r (a singleton row must not match a two-kind '
             'envelope)' % payload['results'][0]['label'])


@case
def c_exact_dep_superset(work):
    def two_deps(env):
        nr = env['normalized_result']
        nr['extraction_gaps'] = [{'kind': 'missing-extractor-dependency',
                                  'dependencies': ['sasquatch', 'sasquatch-v4be']}]
        nr['diagnostics'] = []
        env.pop('raw_result', None)

    env = _mutate(work, 'env-twodeps.json', 'H09', two_deps)
    rows = [_row('single', handler='squashfs_v4_be', gaps='missing-extractor-dependency',
                 deps='sasquatch', be='n/a', sr='no', files='*', action='none'),
            _row('both', handler='squashfs_v4_be', gaps='missing-extractor-dependency',
                 deps='sasquatch+sasquatch-v4be', be='n/a', sr='no', files='*',
                 action='none')]
    path = _write(work, 'sk-depsuperset.md', _skel(_block(rows)))
    res = _cli(['--skill', path, env])
    _expect_pair(res, env, 'both', 'none', 'exact-dep-superset')


@case
def c_none_handler_rejects(work):
    rows = [_row('nochunk', handler='none', gaps='none', deps='none', be='n/a', sr='yes',
                 files='>0', action='inspect-input')]
    path = _write(work, 'sk-nonereject.md', _skel(_block(rows)))
    res = _cli(['--skill', path, _fixture('K', 'K1')])
    _expect_pair(res, _fixture('K', 'K1'), 'unclassified', 'none', 'none-handler-rejects')


@case
def c_fnmatch_handler(work):
    rows = [_row('pat', handler='squashfs_v4_?e', gaps='unpublished-entry', deps='none',
                 be='n/a', sr='no', files='>0', action='count-gap')]
    path = _write(work, 'sk-pat.md', _skel(_block(rows)))
    res = _cli(['--skill', path, _fixture('H', 'H07')])
    _expect_pair(res, _fixture('H', 'H07'), 'pat', 'count-gap', 'fnmatch-handler')


@case
def c_be_values(work):
    skill = _write(work, 'sk-bevalues.md', _skel(TABLE_BLOCK))
    res = _cli(['--skill', skill, '--json', _fixture('H', 'H15'), _fixture('H', 'H13'),
                _fixture('H', 'H01')])
    payload = _json_of(res, 'be-values')
    values = [entry['features']['BE'] for entry in payload['results']]
    _require(values == ['yes', 'no', 'n/a'], 'be-values: BE values are %r' % values)
    labels = [entry['label'] for entry in payload['results']]
    _require(labels == ['body-extractor-failure', 'avm-marker-be-dropped', 'clean'],
             'be-values: labels are %r' % labels)


@case
def c_be_token_not_substring(work):
    def rewrite(env):
        nr = env['normalized_result']
        for diag in nr.get('diagnostics') or []:
            report = diag.get('report') or {}
            if 'command' in report:
                report['command'] = report['command'].replace(' -be ', ' -be=1 ')
        for found in _iter_dicts(env.get('raw_result')):
            if isinstance(found.get('command'), str):
                found['command'] = found['command'].replace(' -be ', ' -be=1 ')

    env = _mutate(work, 'env-besubstring.json', 'H15', rewrite)
    skill = _write(work, 'sk-besub.md', _skel(TABLE_BLOCK))
    res = _cli(['--skill', skill, '--json', env])
    payload = _json_of(res, 'be-token-not-substring')
    entry = payload['results'][0]
    _require(entry['features']['BE'] == 'no',
             'be-token-not-substring: BE is %r (only a standalone -be token counts)'
             % entry['features']['BE'])
    _require(entry['label'] == 'avm-marker-be-dropped',
             'be-token-not-substring: label is %r' % entry['label'])


@case
def c_be_argv_list(work):
    def to_list(env):
        nr = env['normalized_result']
        for diag in nr.get('diagnostics') or []:
            report = diag.get('report') or {}
            if isinstance(report.get('command'), str):
                report['command'] = command_tokens(report['command'])
        for found in _iter_dicts(env.get('raw_result')):
            if isinstance(found.get('command'), str):
                found['command'] = command_tokens(found['command'])

    env = _mutate(work, 'env-argv.json', 'H15', to_list)
    skill = _write(work, 'sk-argv.md', _skel(TABLE_BLOCK))
    res = _cli(['--skill', skill, '--json', env])
    payload = _json_of(res, 'be-argv-list')
    _require(payload['results'][0]['features']['BE'] == 'yes',
             'be-argv-list: BE is %r' % payload['results'][0]['features']['BE'])
    _require(payload['results'][0]['label'] == 'body-extractor-failure',
             'be-argv-list: label is %r' % payload['results'][0]['label'])


@case
def c_sr_from_diagnostics(work):
    skill = _write(work, 'sk-srdiag.md', _skel(TABLE_BLOCK))
    res = _cli(['--skill', skill, '--json', _fixture('K', 'K1')])
    payload = _json_of(res, 'sr-from-diagnostics')
    entry = payload['results'][0]
    _require(entry['features']['SR'] == 'yes',
             'sr-from-diagnostics: SR is %r' % entry['features']['SR'])


@case
def c_sr_from_raw_result(work):
    def inject(env):
        env['raw_result'] = {'report': [{'report': {'__typename__':
                                                    SYMLINK_TYPENAME,
                                                    'severity': 'WARNING'}}]}

    env = _mutate(work, 'env-srraw.json', 'H01', inject)
    skill = _write(work, 'sk-srraw.md', _skel(TABLE_BLOCK))
    res = _cli(['--skill', skill, '--json', env])
    payload = _json_of(res, 'sr-from-raw-result')
    entry = payload['results'][0]
    _require(entry['features']['SR'] == 'yes',
             'sr-from-raw-result: SR is %r' % entry['features']['SR'])
    _require(entry['label'] == 'escaping-symlink-removed',
             'sr-from-raw-result: label is %r' % entry['label'])


@case
def c_published_files(work):
    skill = _write(work, 'sk-files.md', _skel(TABLE_BLOCK))
    res = _cli(['--skill', skill, '--json', _fixture('H', 'H15'), _fixture('H', 'H01')])
    payload = _json_of(res, 'published-files')
    zero, positive = (entry['features']['P'] for entry in payload['results'])
    _require(zero == 0, 'published-files: H15 P is %r' % zero)
    _require(positive > 0, 'published-files: H01 P is %r' % positive)
    _require(payload['results'][0]['label'] == 'body-extractor-failure',
             'published-files: H15 label is %r' % payload['results'][0]['label'])
    _require(payload['results'][1]['label'] == 'clean',
             'published-files: H01 label is %r' % payload['results'][1]['label'])


@case
def c_partial_body_failure(work):
    def publish_one(env):
        nr = env['normalized_result']
        nr['files'] = [{'relative_path': 'firmware.bin_extract/part.txt',
                        'sha256': '0' * 64, 'size': 1}]

    env = _mutate(work, 'env-partial.json', 'H15', publish_one)
    skill = _write(work, 'sk-partial.md', _skel(TABLE_BLOCK))
    res = _cli(['--skill', skill, env])
    _expect_pair(res, env, 'partial-body-failure', 'salvage-partial',
                 'partial-body-failure')


@case
def c_clean_empty(work):
    def no_files(env):
        env['normalized_result']['files'] = []

    env = _mutate(work, 'env-empty.json', 'H01', no_files)
    skill = _write(work, 'sk-empty.md', _skel(TABLE_BLOCK))
    res = _cli(['--skill', skill, env])
    _expect_pair(res, env, 'clean-empty', 'confirm-empty', 'clean-empty')


@case
def c_bare_vs_full(work):
    bare = _load(_fixture('H', 'H01'))
    full = {'ok': True, 'data': bare, 'meta': {'command': 'extract-firmware'}}
    path_bare = _dump(work, 'env-bare.json', bare)
    path_full = _dump(work, 'env-full.json', full)
    skill = _write(work, 'sk-both.md', _skel(TABLE_BLOCK))
    res = _cli(['--skill', skill, '--json', path_bare, path_full])
    payload = _json_of(res, 'bare-vs-full')
    _require(len(payload['results']) == 2, 'bare-vs-full: expected two results')
    left, right = payload['results']
    _require(left['features'] == right['features'],
             'bare-vs-full: features differ %r vs %r' % (left['features'], right['features']))
    _require((left['label'], left['action']) == (right['label'], right['action']),
             'bare-vs-full: decisions differ')


@case
def c_unclassified_default(work):
    rows = [_row('narrow', handler='squashfs_v4_le', gaps='extractor-failure', deps='none',
                 be='yes', sr='no', files='0', action='preserve-failure')]
    path = _write(work, 'sk-narrow.md', _skel(_block(rows)))
    res = _cli(['--skill', path, _fixture('K', 'K1')])
    _expect_pair(res, _fixture('K', 'K1'), 'unclassified', 'none', 'unclassified-default')


@case
def c_duplicate_label(work):
    rows = [_row('same'), _row('same', action='inspect-input')]
    path = _write(work, 'sk-dup.md', _skel(_block(rows)))
    res = _cli(['--skill', path, _fixture('H', 'H01')])
    _exit_is(res, 2, 'duplicate-label')
    _require('duplicate' in res.stderr and 'same' in res.stderr,
             'duplicate-label: stderr does not name the duplicate (%r)' % res.stderr)


@case
def c_unknown_action(work):
    rows = [_row('x', action='levitate')]
    path = _write(work, 'sk-badaction.md', _skel(_block(rows)))
    res = _cli(['--skill', path, _fixture('H', 'H01')])
    _exit_is(res, 2, 'unknown-action')
    _require('levitate' in res.stderr, 'unknown-action: stderr does not name the token')


@case
def c_missing_actions_line(work):
    rows = [_row('x')]
    path = _write(work, 'sk-noactions.md', _skel(_block(rows, actions=False)))
    res = _cli(['--skill', path, _fixture('H', 'H01')])
    _exit_is(res, 2, 'missing-actions-line')
    _require(ACTIONS_PREFIX in res.stderr,
             'missing-actions-line: stderr does not name the vocabulary prefix')


@case
def c_actions_line_separated_by_prose(work):
    block = [_vocab_line(), '', 'prose between vocabulary and table', '',
             '| ' + ' | '.join(HEADER) + ' |',
             '| ' + ' | '.join(['---'] * len(HEADER)) + ' |',
             '| ' + ' | '.join(_row('x')) + ' |']
    text = '# SKILL\n\n## Queue-drain craft\n\n' + MARKER + '\n\n' + '\n'.join(block) + '\n'
    path = _write(work, 'sk-prose.md', text)
    res = _cli(['--skill', path, _fixture('H', 'H01')])
    _exit_is(res, 2, 'actions-line-separated-by-prose')


@case
def c_marker_v1_only(work):
    block = _v1_block(work)
    path = _write(work, 'sk-v1only.md', _skel(block))
    res = _cli(['--skill', path, _fixture('H', 'H01')])
    _exit_is(res, 2, 'marker-v1-only')
    _require('v2' in res.stderr, 'marker-v1-only: stderr does not name the v2 marker')


def _v1_block(work):
    """The v1 table block extracted from the real SKILL.md, else a synthetic one."""
    try:
        with open(SELFTEST_SKILL, 'r', encoding='utf-8') as handle:
            lines = handle.read().splitlines()
    except OSError:
        lines = []
    start = None
    for i, line in enumerate(lines):
        if '<!-- sqfs-triage-table v1 -->' in line:
            start = i
            break
    if start is not None:
        out = [lines[start]]
        for line in lines[start + 1:]:
            if not line.lstrip().startswith('|'):
                break
            out.append(line)
        if len(out) > 3:
            return '\n'.join(out) + '\n'
    return ('<!-- sqfs-triage-table v1 -->\n'
            '| label | handler | gap kinds | dependencies | -be in child argv | '
            'symlink removed | published files | cause -> action | source |\n'
            '| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n'
            '| x | * | * | * | * | * | * | cause -> action | selftest |\n')


@case
def c_table_outside_craft(work):
    path = _write(work, 'sk-outside.md', _skill_outside(TABLE_BLOCK))
    res = _cli(['--skill', path, _fixture('H', 'H01')])
    _exit_is(res, 2, 'table-outside-craft')
    _require('marker' in res.stderr,
             'table-outside-craft: stderr does not name the marker')


@case
def c_marker_absent(work):
    path = _write(work, 'sk-nomarker.md', _skel(_block([_row('x')], marker=False)))
    res = _cli(['--skill', path, _fixture('H', 'H01')])
    _exit_is(res, 2, 'marker-absent')


@case
def c_marker_without_table(work):
    path = _write(work, 'sk-notable.md',
                  _skel(MARKER + '\n\n' + _vocab_line()
                        + '\n\nOnly prose follows the vocabulary.\n'))
    res = _cli(['--skill', path, _fixture('H', 'H01')])
    _exit_is(res, 2, 'marker-without-table')
    _require('no markdown table' in res.stderr,
             'marker-without-table: stderr does not say the table is absent')


@case
def c_malformed_header(work):
    header = list(HEADER)
    header[3] = 'chunk handler'
    path = _write(work, 'sk-badhdr.md', _skel(_block([_row('x')], header=header)))
    res = _cli(['--skill', path, _fixture('H', 'H01')])
    _exit_is(res, 2, 'malformed-header')
    _require('header' in res.stderr, 'malformed-header: stderr does not say header')


@case
def c_malformed_domain_cell(work):
    rows = [_row('x', operation='extract firmware')]
    path = _write(work, 'sk-badop.md', _skel(_block(rows)))
    res = _cli(['--skill', path, _fixture('H', 'H01')])
    _exit_is(res, 2, 'malformed-domain-cell')
    _require('operation' in res.stderr,
             'malformed-domain-cell: stderr does not name the column')


@case
def c_malformed_set_cell(work):
    rows = [_row('x', gaps='unpublished-entry+')]
    path = _write(work, 'sk-badset.md', _skel(_block(rows)))
    res = _cli(['--skill', path, _fixture('H', 'H01')])
    _exit_is(res, 2, 'malformed-set-cell')


@case
def c_malformed_files_cell(work):
    rows = [_row('x', files='many')]
    path = _write(work, 'sk-badfiles.md', _skel(_block(rows)))
    res = _cli(['--skill', path, _fixture('H', 'H01')])
    _exit_is(res, 2, 'malformed-files-cell')
    _require('published files' in res.stderr,
             'malformed-files-cell: stderr does not name the column')


@case
def c_empty_action_cell(work):
    rows = [_row('x', action='')]
    path = _write(work, 'sk-emptyaction.md', _skel(_block(rows)))
    res = _cli(['--skill', path, _fixture('H', 'H01')])
    _exit_is(res, 2, 'empty-action-cell')


@case
def c_row_cell_count(work):
    row = _row('x')[:-1]
    path = _write(work, 'sk-cellcount.md', _skel(_block([row])))
    res = _cli(['--skill', path, _fixture('H', 'H01')])
    _exit_is(res, 2, 'row-cell-count')


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
    scalar = _write(work, 'scalar.json', '7')
    res = _cli(['--skill', skill, scalar])
    _exit_is(res, 2, 'envelope-scalar')


@case
def c_json_shape(work):
    skill = _write(work, 'sk-json.md', _skel(TABLE_BLOCK))
    res = _cli(['--skill', skill, '--json', _fixture('K', 'K1')])
    payload = _json_of(res, 'json-shape')
    entry = payload['results'][0]
    _require(entry['rule'] == 8, 'json-shape: rule index is %r' % entry['rule'])
    _require(len(entry['row']) == len(HEADER),
             'json-shape: row has %r cells' % len(entry['row']))
    _require(entry['row'][0] == 'escaping-symlink-removed',
             'json-shape: row label is %r' % entry['row'][0])
    _require(entry['row'][9] == 'expect-link-absent',
             'json-shape: row action is %r' % entry['row'][9])
    for key in ('OP', 'PV', 'H', 'G', 'D', 'BE', 'SR', 'P'):
        _require(key in entry['features'], 'json-shape: feature %r missing' % key)
    _require(entry['features']['OP'] == 'extract_firmware',
             'json-shape: OP is %r' % entry['features']['OP'])
    _require(entry['features']['PV'] == 'unblob',
             'json-shape: PV is %r' % entry['features']['PV'])
    _require(payload['actions'] == VOCAB.split(),
             'json-shape: top-level actions are %r' % payload['actions'])
    _require(payload['rules'] == 11, 'json-shape: rules is %r' % payload['rules'])


@case
def c_first_table_wins(work):
    first = _block([_row('first-table')])
    second = _block([_row('second-table')], marker=False)
    text = ('# SKILL\n\n## Queue-drain craft\n\n' + first + '\nprose\n\n' + second + '\n')
    path = _write(work, 'sk-twotables.md', text)
    res = _cli(['--skill', path, _fixture('H', 'H01')])
    _expect_pair(res, _fixture('H', 'H01'), 'first-table', 'none', 'first-table-wins')


@case
def c_print_table(work):
    res = _cli(['--print-table'])
    _exit_is(res, 0, 'print-table')
    _require(res.stdout == TABLE_BLOCK, 'print-table: stdout is not the frozen block')
    path = _write(work, 'sk-printed.md', _skel(res.stdout))
    res = _cli(['--skill', path, '--table-only'])
    _exit_is(res, 0, 'print-table-reparses')


@case
def c_real_skill(work):
    """The real SKILL.md is readable before and after the v2 table is integrated."""
    try:
        with open(SELFTEST_SKILL, 'r', encoding='utf-8') as handle:
            text = handle.read()
    except OSError as exc:
        raise AssertionError('real-skill: cannot read %s (%s)' % (SELFTEST_SKILL, exc))
    path = _fixture('H', 'H01')
    res = _cli(['--skill', SELFTEST_SKILL, path])
    if MARKER in text:
        _expect_pair(res, path, 'clean', 'none', 'real-skill')
        res = _cli(['--skill', SELFTEST_SKILL, '--table-only'])
        _exit_is(res, 0, 'real-skill-table-only')
    else:
        _exit_is(res, 2, 'real-skill-before-v2-integration')


def selftest():
    work = tempfile.mkdtemp(dir=os.environ.get('TMPDIR') or None,
                            prefix='sqfs-triage-v2-selftest.')
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
        prog='sqfs-triage-v2.py',
        description='Label REA envelopes with the SKILL.md craft-section SquashFS triage '
                    'table v2 (label and action).')
    parser.add_argument('--skill', metavar='SKILL.md',
                        help='document holding the craft-section v2 triage table')
    parser.add_argument('--json', action='store_true',
                        help='print features, the matched rule and its action as JSON')
    parser.add_argument('--table-only', action='store_true',
                        help='validate the table and print the parsed rules and actions')
    parser.add_argument('--selftest', action='store_true',
                        help='run the isolated selftest')
    parser.add_argument('--print-table', action='store_true',
                        help='print the frozen v2 table block')
    parser.add_argument('envelopes', nargs='*', metavar='ENVELOPE.json',
                        help='REA envelope (bare data object or full CLI envelope)')
    ns = parser.parse_args(argv)
    if ns.print_table:
        sys.stdout.write(TABLE_BLOCK)
        return 0
    if ns.selftest:
        return selftest()
    try:
        return _run(ns)
    except (TableError, EnvelopeError, InvocationError) as exc:
        sys.stderr.write('sqfs-triage-v2: %s\n' % exc)
        return 2


if __name__ == '__main__':
    sys.exit(main())
