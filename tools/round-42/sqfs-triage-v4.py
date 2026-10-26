#!/usr/bin/env python3
"""sqfs-triage-v4.py - executable SquashFS extract-firmware outcome triage, table v4.

Reads exactly two surfaces and nothing else:

  * a SKILL.md document, from which it takes the FIRST markdown table that follows a
    line containing the marker ``<!-- sqfs-triage-table v4 -->`` inside the
    ``## Queue-drain craft`` section (that heading line up to the next ``## `` heading),
    plus the closed action vocabulary declared by the line directly above that table
    (``<!-- sqfs-triage-actions: token ... -->``; blank lines between it and the table
    header are allowed, any other prose is not);
  * REA envelopes (rea-agents 6.5.0), recorded as either a bare ``data`` object or a
    full CLI envelope ``{ok, data, meta}``.

It prints one ``(label, action)`` pair per envelope.  It never invokes REA, unblob or
sasquatch, never reads a carrier, and never writes anything.

What v4 changes against v3 (round-42 draft, R42-C2; routed defect R41-CL4)
--------------------------------------------------------------------------
1. Marker ``<!-- sqfs-triage-table v4 -->``.  A document whose craft section carries a
   ``v3`` (or ``v2`` / ``v1``) marker and no v4 marker is REFUSED with exit 2: a
   superseded table is never silently evaluated by this interpreter.  A v4 marker wins
   over retained history blocks, because only a v4 marker claims a v4 table.

2. The handler domain becomes a glob over the WHOLE SquashFS handler family, split over
   TWO columns so that the precedence's two different objects stay separate:

       ``handler``          a glob over F  (``*`` any set, ``none`` F = empty, other: at
                            least one member of F matches)
       ``failing handler``  a glob over HF (``*`` matches an empty HF too, ``none`` HF =
                            empty, other: at least one member of HF matches)

   with

       H   every ``chunks[].handler`` and ``extraction_gaps[].handler`` value, nulls
           dropped (the round-41 feature definition, plans/round-41-claims.md:109-115)
       F   the ``squashfs``-prefixed members of H (the draft's F)
       HF  the ``squashfs``-prefixed ``handler`` values recorded on the gap rows whose
           ``kind`` is ``extractor-failure``; when no such row records one, HF = F

   Why two columns: draft steps 2, 3 and 9-14 ("F = the set of SquashFS handler names in
   H") are about the run-wide set, while steps 6 and 7 ("``squashfs_v4_be`` in HF",
   "HF ∩ L ≠ ∅" with L = F ∩ ``squashfs_v1*`` / ``squashfs_v2*`` / ``squashfs_v3*``) are
   about ONE failed extraction.  A single ``handler`` cell cannot say both, so steps 6
   and 7 write ``squashfs_*`` in ``handler`` (entailed once step 3 has passed) and the
   failing family glob in ``failing handler``.  A mixed chunk set with one failed v3
   chunk and one healthy v4-BE chunk therefore reads F = {v3, v4_be}, HF = {v3}, and the
   AVM row (``failing handler`` ``squashfs_v4_be``) does not fire.

   This is the repair of R41-CL4: under v3 only ``squashfs_v4_*`` could be named, so a
   v1-v3-only chunk matched no row and read ``unclassified`` while the precedence said
   ``no-squashfs-chunk``.  v4 labels a legacy chunk from the same table that labels a v4
   chunk, and it keeps the two failure populations apart (step 6 AVM marker vs step 7
   legacy body) with its own column.

3. Each handler-family glob is validated against a version-pinned vocabulary: a pattern
   must begin ``squashfs`` and must match at least one of the ten handler names unblob
   26.6.4 registers for SquashFS (``KNOWN_HANDLERS`` below).  A typo such as
   ``squashfs_v4_BE`` or ``squashfs_v9*`` is a dead cell and makes the table malformed
   (exit 2) instead of silently matching nothing at run time.

4. The ``dependencies`` column gains the same contains form the ``gap kinds`` column has
   had since v3 (``kind+``).  Draft step 3 says "D holds ``sasquatch-v4be``" and "else D
   holds ``sasquatch``" - membership, not set equality - and a v3 exact cell could not
   express it on a superset (round-41 w2 ``R41W2C2InterpMut.md`` §6 K6/K7: the
   interpreter read ``unclassified`` where the evaluator read ``dep-missing-be``).
   ``sasquatch-v4be+`` is the cell that means "D holds sasquatch-v4be".

Features (from the envelope) - round-41 definitions, with H widened to the gap rows
---------------------------------------------------------------------------------
  OP  ``data.operation`` (string), else ``''``
  PV  ``data.provider.id`` when ``provider`` is an object, the string itself when
      ``provider`` is a string, else ``''``
  H   every ``normalized_result.chunks[].handler`` and
      ``normalized_result.extraction_gaps[].handler``, nulls dropped (round 41 counted
      the chunk row only; draft step 2's F is over H, and a gap row keeps the handler of
      a chunk REA did not publish as a chunk)
  F   the ``squashfs``-prefixed members of H
  HF  the ``squashfs``-prefixed handler of every ``extractor-failure`` gap row; F when
      no such row records one
  G   set of ``normalized_result.extraction_gaps[].kind``
  D   union of ``normalized_result.extraction_gaps[].dependencies``
  BE  ``yes`` if a recorded sasquatch child argv carries a standalone ``-be`` token,
      ``no`` if such an argv exists and none does, ``n/a`` if no sasquatch argv is
      recorded.  Command sources: ``normalized_result.diagnostics[]`` and
      ``data.diagnostics[]`` entries and their nested ``report`` (keys ``command``,
      ``argv``, ``args``; a string is tokenised with shlex, a list is used as given),
      plus any dict under ``raw_result`` carrying one of those keys.  Only a command
      naming a binary whose basename starts ``sasquatch`` counts.
  SR  ``yes`` if a ``MaliciousSymlinkRemoved`` producer report is visible: a
      ``__typename__`` on a ``normalized_result.diagnostics[]`` entry or on its nested
      ``report``, or the same ``__typename__`` on any dict under ``raw_result`` (the
      producer report kept verbatim); else ``no``.  A bare substring of the token in
      ``raw_result.execution.stdout.text`` is NOT accepted: a text search asserts a
      report from a string, and the round-41 evaluator's stdout path is the one shape
      the two round-41 tools disagreed on (R41W2C2InterpMut §6 K8).  See Limits.
  P   ``len(normalized_result.files)``; an absent ``files`` list reads 0

Table grammar (columns, in this order, exact header names) - 13 columns in v4
------------------------------------------------------------------------------
  label | operation | provider | handler | failing handler | gap kinds | dependencies |
  -be in child argv | symlink removed | published files | action | cause | source

Condition cells, after stripping surrounding backticks and whitespace:

  operation          ``*`` (any), or the exact ``data.operation`` token REA records
                     (``extract_firmware`` for the verb this table is about).
  provider           ``*`` (any), or the exact ``data.provider.id`` token REA records
                     (``unblob``).  A provider recorded as a bare string is used as is;
                     an absent provider is the empty string, which no exact cell matches.
  handler            ``*`` / ``none`` / a validated glob over F.
  failing handler    ``*`` / ``none`` / a validated glob over HF.  ``*`` is the only
                     cell that matches an empty HF, which is why it is the cell every
                     row outside steps 6 and 7 carries.
  gap kinds          ``*``, ``none``, exact ``a`` / ``a+b``, or contains ``a+`` /
                     ``a,b+`` over ``G``.
  dependencies       ``*``, ``none``, exact ``a`` / ``a+b``, or contains ``a+`` /
                     ``a,b+`` over ``D``  [contains form new in v4].
  -be in child argv  ``yes`` / ``no`` / ``n/a`` / ``*``.
  symlink removed    ``yes`` / ``no`` / ``n/a`` / ``*``.
  published files    ``0`` / ``>0`` / ``*``.
  action             one token from the vocabulary line above the table; a token that
                     is not declared there makes the whole run unevaluable (exit 2).
  cause -> action    non-empty prose containing ``->``.  Documentation only.
  source             non-empty citation prose.  Documentation only.

Rules are tried top to bottom; the first rule whose every condition cell matches wins and
supplies both the label and the action.  No match prints ``unclassified`` with action
``none`` (draft step 13).  A malformed cell, header, separator, vocabulary line,
duplicate label or handler glob, and an unreadable envelope, make the whole run
unevaluable: exit 2, never a silent non-match.

Envelope readability - unchanged from v3
----------------------------------------
A bare ``data`` object is accepted when it carries ``normalized_result`` (an object) or a
string ``operation``; a full ``{ok, data, meta}`` envelope is accepted when ``data`` is
an object with the same shape.  Anything else is unreadable (exit 2).  An envelope whose
``operation`` is ``extract_firmware`` must also carry a ``normalized_result`` object
(exit 2 if not); a domain-mismatched envelope may omit it, so the domain guard stays a
label decision instead of an unreadable-envelope decision.

Usage
-----
  python3 -I -B sqfs-triage-v4.py --skill SKILL.md ENVELOPE.json...
      one ``path<TAB>label<TAB>action`` line per envelope
  python3 -I -B sqfs-triage-v4.py --skill SKILL.md --json ENVELOPE...
      features, matched row index and row cells per envelope
  python3 -I -B sqfs-triage-v4.py --skill SKILL.md --table-only
      validate the table, print the parsed rules and the action vocabulary
  python3 -I -B sqfs-triage-v4.py --selftest
      isolated selftest (temporary SKILL variants and envelopes under $TMPDIR)

Exit codes: 0 ok, 2 table missing, refused (v1/v2/v3 marker), or malformed (wrong header,
malformed cell, dead handler glob, duplicate label, unknown action, missing or misplaced
vocabulary line) or envelope unreadable, 1 only for a failed ``--selftest``.

Limits
------
* Cell text is split on ``|``; a literal pipe inside a cell is not supported.
* Header names are compared case-insensitively; every other cell is compared exactly and
  case-sensitively, and handler patterns are matched with ``fnmatch.fnmatchcase``.
* ``gap kinds`` and ``dependencies`` compare as sets: order and repetition in the
  envelope are erased.  An exact cell ignores an envelope carrying one extra gap kind; a
  contains cell tolerates extras.  Neither kind can express "every gap kind except x".
* One label may own exactly ONE row (duplicate labels are refused).  A label whose
  condition genuinely needs two disjoint condition sets therefore cannot be written.
* A handler row is a positive match: no cell can say "no handler matching a pattern".
  ``none`` is the only negative handler cell and it says F = empty, exactly like draft
  step 2.
* HF falls back to F when no ``extractor-failure`` gap records a handler (A1's rule), so
  on an envelope that mixes a failed chunk with a healthy chunk of another family and
  records no failing handler, the earliest row whose glob intersects H wins (clause
  order).  ``--json`` prints F and HF so a receipt shows which set decided.
* A row's ``failing handler`` glob is the precedence's set test, not a set equality: the
  legacy row's ``squashfs_v[123]*`` is exactly A1 step 7's ``HF ∩ L ≠ ∅``, and the AVM
  row's ``squashfs_v4_be`` is exactly step 6's ``squashfs_v4_be ∈ HF``.  Because HF falls
  back to F, a single-chunk failure with no handler on its gap row still lands on steps
  6/7.
* HF is restricted to ``squashfs``-prefixed names.  Steps 6 and 7 compare HF against
  squashfs-prefixed sets, so the restriction changes no decision; it does keep a
  non-squashfs handler on a broken gap row from widening HF.
* ``KNOWN_HANDLERS`` is pinned to unblob 26.6.4.  A handler a later unblob adds is not
  nameable until this interpreter is extended with it; that is a deliberate refusal, not
  a wildcard.
* BE counts only sasquatch-naming child argvs, so an envelope that records some other
  extractor's argv carrying a standalone ``-be`` reads ``n/a`` here.
* SR does not accept a stdout substring (see Features).  An envelope that keeps the
  producer report only as unblob's printed summary reads ``no``.
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

MARKER = '<!-- sqfs-triage-table v4 -->'
REFUSED_MARKERS = ('<!-- sqfs-triage-table v3 -->',
                   '<!-- sqfs-triage-table v2 -->',
                   '<!-- sqfs-triage-table v1 -->')
ACTIONS_PREFIX = '<!-- sqfs-triage-actions:'
ACTIONS_SUFFIX = '-->'
CRAFT_PREFIX = 'queue-drain craft'
HEADER = ['label', 'operation', 'provider', 'handler', 'failing handler', 'gap kinds',
          'dependencies', '-be in child argv', 'symlink removed', 'published files',
          'action', 'cause', 'source']
BE_VALUES = ('yes', 'no', 'n/a')
FILES_VALUES = ('0', '>0')
RESERVED_MEMBERS = ('none', '*')
SYMLINK_TYPENAME = 'MaliciousSymlinkRemoved'
DEFAULT_LABEL = 'unclassified'
DEFAULT_ACTION = 'none'
OPERATION_TOKEN = 'extract_firmware'
SQUASHFS_PREFIX = 'squashfs'
FAILURE_KIND = 'extractor-failure'

# The ten SquashFS handler names unblob 26.6.4 registers, read from the installed tree
# (`handlers/filesystem/squashfs.py` NAME constants, lines 102, 159, 200, 245, 319,
# 364, 410, 455, 514, 549).  A handler glob must match one of these.
KNOWN_HANDLERS = (
    'squashfs_v1',
    'squashfs_v2',
    'squashfs_v2_nonstandard',
    'squashfs_v3',
    'squashfs_v3_ddwrt',
    'squashfs_v3_broadcom',
    'squashfs_v3_nonstandard',
    'squashfs_v4_le',
    'squashfs_v4_be',
    'squashfs_v4_broadcom',
)

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
DEFAULT_SKILL = LANE + '/SKILL.md'

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
    """The triage table is missing, refused or malformed."""


class EnvelopeError(Exception):
    """An envelope could not be read as an REA extract-firmware result."""


class InvocationError(Exception):
    """The command line does not select a readable surface."""


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


def _parse_set_cell(cell, column, contains=False):
    """Parse one set-valued cell.

    ``contains=False`` keeps the v2/v3 grammar (``*``, ``none``, ``a``, ``a+b``).
    ``contains=True`` adds the contains form (``a+``, ``a,b+``) that both set columns
    speak in v4.
    """
    _, name_re, _, _, _, _ = _regexes()
    if cell in ('*', 'none'):
        return ('any', None) if cell == '*' else ('none', None)
    if contains and cell.endswith('+'):
        body = cell[:-1]
        parts = body.split(',')
        if any(not part for part in parts):
            raise TableError('%s cell %r has an empty contains member'
                             % (column, cell))
        for part in parts:
            if not name_re.match(part):
                raise TableError('%s cell %r has a malformed contains member %r'
                                 % (column, cell, part))
            if part in RESERVED_MEMBERS:
                raise TableError('%s cell %r uses the reserved word %r as a contains '
                                 'member' % (column, cell, part))
        if len(set(parts)) != len(parts):
            raise TableError('%s cell %r repeats a contains member' % (column, cell))
        return ('contains', frozenset(parts))
    parts = cell.split('+')
    if any(not part for part in parts):
        raise TableError('%s cell %r has an empty set member' % (column, cell))
    for part in parts:
        if not name_re.match(part):
            raise TableError('%s cell %r has a malformed member %r' % (column, cell, part))
        if part in RESERVED_MEMBERS:
            raise TableError('%s cell %r uses the reserved word %r as a member'
                             % (column, cell, part))
    if len(set(parts)) != len(parts):
        raise TableError('%s cell %r repeats a member' % (column, cell))
    return ('exact', frozenset(parts))


def _parse_handler_cell(cell, column='handler'):
    """Parse one handler-family cell: ``*``, ``none`` or a validated SquashFS glob."""
    _, _, handler_re, _, _, _ = _regexes()
    if cell == '*':
        return ('any', None)
    if cell == 'none':
        return ('none', None)
    if not handler_re.match(cell):
        raise TableError('%s cell %r is not *, none, or a glob pattern' % (column, cell))
    if not cell.startswith(SQUASHFS_PREFIX):
        raise TableError('%s cell %r does not begin %r: the cell is a glob over SquashFS '
                         'handler names, so a non-squashfs pattern is a dead cell'
                         % (column, cell, SQUASHFS_PREFIX))
    hits = [name for name in KNOWN_HANDLERS if fnmatch.fnmatchcase(name, cell)]
    if not hits:
        raise TableError('%s cell %r matches none of the %d SquashFS handler names '
                         'unblob 26.6.4 registers (%s): a dead cell'
                         % (column, cell, len(KNOWN_HANDLERS),
                            ', '.join(KNOWN_HANDLERS)))
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
        (label, operation, provider, handler, failing, gap, dep, be, sr, files, action,
         cause, source) = cells
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
            'handler': _parse_handler_cell(handler, 'handler'),
            'failing_handler': _parse_handler_cell(failing, 'failing handler'),
            'gap_kinds': _parse_set_cell(gap, 'gap kinds', contains=True),
            'dependencies': _parse_set_cell(dep, 'dependencies', contains=True),
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
    """Return (rules, info) for the craft-section v4 triage table of one SKILL.md.

    The v4 marker selects its own table, so a retained v3/v2/v1 block in the same
    section is history.  Without a v4 marker the document is REFUSED (never silently
    triaged by a superseded table): the error names the marker version it found.
    """
    lines = text.splitlines()
    start, end = craft_bounds(lines)
    marker_line = None
    for i in range(start, end):
        if MARKER in lines[i]:
            marker_line = i
            break
    if marker_line is None:
        for refused in REFUSED_MARKERS:
            for i in range(start, end):
                if refused in lines[i]:
                    raise TableError('line %d: refused marker %r; this interpreter reads '
                                     'only %r in the craft section (a superseded table is '
                                     'never evaluated as v4)'
                                     % (i + 1, refused, MARKER))
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


ARGV_KEYS = ('command', 'argv', 'args')


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


def _holders(diag):
    """A diagnostics entry and its nested ``report`` object, deduplicated by identity."""
    out = []
    if isinstance(diag, dict):
        out.append(diag)
        report = diag.get('report')
        if isinstance(report, dict) and report is not diag:
            out.append(report)
    return out


def extractor_commands(data):
    """Every recorded sasquatch child argv, in first-seen order."""
    commands = []

    def take(cmd):
        tokens = command_tokens(cmd)
        if tokens and names_sasquatch(tokens) and cmd not in commands:
            commands.append(cmd)

    nr = data.get('normalized_result')
    nr = nr if isinstance(nr, dict) else {}
    for source in (nr.get('diagnostics'), data.get('diagnostics')):
        for diag in _as_list(source):
            for holder in _holders(diag):
                for key in ARGV_KEYS:
                    if key in holder:
                        take(holder[key])
    for found in _iter_dicts(data.get('raw_result')):
        for key in ARGV_KEYS:
            if key in found:
                take(found[key])
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


def _handler_names(nr):
    """Every chunk and gap handler name in the envelope, nulls dropped (feature H)."""
    names = []
    for chunk in _as_list(nr.get('chunks')):
        handler = chunk.get('handler') if isinstance(chunk, dict) else None
        if isinstance(handler, str) and handler and handler not in names:
            names.append(handler)
    for gap in _as_list(nr.get('extraction_gaps')):
        handler = gap.get('handler') if isinstance(gap, dict) else None
        if isinstance(handler, str) and handler and handler not in names:
            names.append(handler)
    return names


def _failing_handlers(nr):
    """The handler of every ``extractor-failure`` gap row, squashfs-prefixed (HF)."""
    names = []
    for gap in _as_list(nr.get('extraction_gaps')):
        if not isinstance(gap, dict) or gap.get('kind') != FAILURE_KIND:
            continue
        handler = gap.get('handler')
        if (isinstance(handler, str) and handler.startswith(SQUASHFS_PREFIX)
                and handler not in names):
            names.append(handler)
    return names


def _symlink_removed(nr, data):
    for diag in _as_list(nr.get('diagnostics')):
        for holder in _holders(diag):
            if holder.get('__typename__') == SYMLINK_TYPENAME:
                return 'yes'
    for found in _iter_dicts(data.get('raw_result')):
        if found.get('__typename__') == SYMLINK_TYPENAME:
            return 'yes'
    return 'no'


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
    handler_names = _handler_names(nr)
    squashfs_names = [name for name in handler_names
                      if name.startswith(SQUASHFS_PREFIX)]
    failing = _failing_handlers(nr)
    candidates = failing or squashfs_names
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
    return {
        'OP': operation,
        'PV': provider_id,
        'H': sorted(handler_names),
        'F': sorted(squashfs_names),
        'HF': sorted(candidates),
        'G': sorted(gap_kinds),
        'D': sorted(dependencies),
        'BE': be,
        'SR': _symlink_removed(nr, data),
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
    if kind == 'contains':
        return payload <= frozenset(values)
    return frozenset(values) == payload


def match_glob(spec, names):
    """``*`` matches any set (including empty), ``none`` the empty set, else any member."""
    kind, payload = spec
    if kind == 'any':
        return True
    if kind == 'none':
        return not names
    return any(fnmatch.fnmatchcase(value, payload) for value in names)


def rule_matches(rule, feat):
    if rule['operation'] != '*' and rule['operation'] != feat['OP']:
        return False
    if rule['provider'] != '*' and rule['provider'] != feat['PV']:
        return False
    if not match_glob(rule['handler'], feat['F']):
        return False
    if not match_glob(rule['failing_handler'], feat['HF']):
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


def _spec_text(spec):
    kind, payload = spec
    if kind in ('any', 'none'):
        return kind
    return '%s{%s}' % (kind, ','.join(sorted(payload)))


def _handler_text(spec):
    kind, payload = spec
    if kind == 'pattern':
        return 'glob{%s}' % payload
    return kind


def _print_rules(skill, rules, info):
    print('skill: %s' % skill)
    print('marker line: %d  actions line: %d  table line: %d  rules: %d'
          % (info['marker_line'], info['actions_line'], info['table_line'],
             info['rules']))
    print('actions: %s' % ' '.join(info['actions']))
    print('handler semantics: handler globs over F = the squashfs-prefixed handler names '
          'in H (none = F empty); failing handler globs over HF = the handler of every '
          'extractor-failure gap row, falling back to F when none records one (A1); * '
          'matches an empty set')
    for rule in rules:
        print('%d. %s' % (rule['index'], rule['label']))
        print('   operation=%r provider=%r handler=%s failing_handler=%s gap_kinds=%s '
              'dependencies=%s'
              % (rule['operation'], rule['provider'], _handler_text(rule['handler']),
                 _handler_text(rule['failing_handler']),
                 _spec_text(rule['gap_kinds']), _spec_text(rule['dependencies'])))
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
# selftest harness
# --------------------------------------------------------------------------------------

SKELETON = ('# SKILL\n\n## Queue-drain craft\n\nCraft prose before the table.\n\n'
            '{block}\n\n## A later section\n\nProse after the craft section.\n')

VOCAB = ('none inspect-input install-extractor-be install-extractor-le wrap-extractor-be '
         'preserve-failure salvage-partial raise-depth audit-symlinks '
         'expect-link-absent count-gap confirm-empty cross-read-legacy isolate-residue')


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


def _expect_pair(res, path, want_label, want_action, name):
    lines = _lines_of(res, name)
    _require(len(lines) == 1, '%s: expected one output line, got %r' % (name, lines))
    got_path, _, rest = lines[0].partition('\t')
    _require(os.path.abspath(got_path) == os.path.abspath(path),
             '%s: path column %r is not %r' % (name, got_path, path))
    got_label, _, got_action = rest.partition('\t')
    _require((got_label, got_action) == (want_label, want_action),
             '%s: pair %r, expected %r'
             % (name, (got_label, got_action), (want_label, want_action)))


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


def _vocab_line(tokens=None):
    return '%s %s %s' % (ACTIONS_PREFIX, tokens or VOCAB, ACTIONS_SUFFIX)


def _block(rows, marker=MARKER, vocab_line=None, header=None, actions=True):
    header = header or HEADER
    out = []
    if marker:
        out.append(marker)
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
         failing='*', gaps='*', deps='*', be='*', sr='*', files='*', action='none',
         cause='cause -> action', source='selftest'):
    return [label, operation, provider, handler, failing, gaps, deps, be, sr, files,
            action, cause, source]


def _env(handler='squashfs_v4_be', handlers=(), gaps=(), be=None, sr=False, files=0,
         op='extract_firmware', pv='unblob', command=None, gap_handlers=None,
         files_absent=False, sr_where='raw', no_chunks=False):
    """Build one synthetic REA ``data`` object with exactly these features.

    ``handler`` is the single chunk handler (None drops the chunk row), ``handlers``
    adds further chunk rows.  ``gaps`` items are a kind string or a
    ``(kind, [dependencies])`` tuple.  ``gap_handlers`` maps a gap kind to the handler
    REA records on that gap row.  ``be`` is None for no sasquatch command (feature
    ``n/a``), True for a ``-be`` argv token, False for a sasquatch command without it;
    ``command`` overrides the recorded command.  ``sr_where`` is ``raw`` (raw_result
    report), ``diag-report`` (normalized_result.diagnostics[].report), ``diag``
    (diagnostics[] itself), ``stdout`` (only the printed token) or ``none``.
    """
    chunks = []
    if not no_chunks:
        for name in ((handler,) if handler else ()) + tuple(handlers):
            chunks.append({'handler': name})
    gap_handlers = gap_handlers or {}
    gaps_out = []
    for gap in gaps:
        if isinstance(gap, tuple):
            record = {'kind': gap[0], 'dependencies': list(gap[1])}
        else:
            record = {'kind': gap, 'dependencies': []}
        if record['kind'] in gap_handlers:
            record['handler'] = gap_handlers[record['kind']]
        gaps_out.append(record)
    diagnostics = []
    if command is not None:
        diagnostics.append({'report': {'command': command}})
    elif be is not None:
        argv = ['/usr/local/bin/sasquatch-v4be']
        if be:
            argv.append('-be')
        argv.extend(['-d', '/out', '/in'])
        diagnostics.append({'report': {'command': argv}})
    if sr and sr_where == 'diag-report':
        diagnostics.append({'report': {'__typename__': SYMLINK_TYPENAME,
                                       'link': '$output/a', 'target': '../b'}})
    if sr and sr_where == 'diag':
        diagnostics.append({'__typename__': SYMLINK_TYPENAME, 'link': '$output/a'})
    nr = {'chunks': chunks, 'extraction_gaps': gaps_out, 'diagnostics': diagnostics}
    if not files_absent:
        nr['files'] = [{'relative_path': 'f/%d.bin' % n, 'size': 1}
                       for n in range(files)]
    data = {'operation': op,
            'provider': {'id': pv, 'name': pv, 'version': '0.0'},
            'normalized_result': nr}
    if sr:
        if sr_where == 'raw':
            data['raw_result'] = {'report': [{'reports': [{'__typename__':
                                                           SYMLINK_TYPENAME}]}]}
        elif sr_where == 'stdout':
            data['raw_result'] = {'execution': {'stdout': {'text':
                                                           'WARNING ' + SYMLINK_TYPENAME}}}
    return data


def _cls(work, skill, env, name, extra=()):
    path = _dump(work, name, env)
    return _cli(['--skill', skill, *extra, path]), path


def _two(target, fallback_action='inspect-input'):
    return [target, _row('fallback', handler='*', gaps='*', deps='*', be='*', sr='*',
                         files='*', action=fallback_action)]


def _single(work, name, rows, env, want_label, want_action):
    skill = _write(work, 'sk-%s.md' % name, _skel(_block(rows)))
    res, path = _cls(work, skill, env, 'env-%s.json' % name)
    _expect_pair(res, path, want_label, want_action, name)


def _contains_case(work, name, gap_cell, gaps, want_label, files=2, be=False,
                   handler='squashfs_v4_be'):
    rows = _two(_row('target', handler='squashfs_v4_*', gaps=gap_cell, deps='*', be='*',
                     sr='*', files='*', action='salvage-partial'))
    skill = _write(work, 'sk-%s.md' % name, _skel(_block(rows)))
    env = _env(handler=handler, gaps=gaps, be=be, files=files)
    res, path = _cls(work, skill, env, 'env-%s.json' % name)
    _expect_pair(res, path, want_label, 'salvage-partial' if want_label == 'target'
                 else 'inspect-input', name)


CASES = []


def case(fn):
    CASES.append(fn)
    return fn


# ------------------------------------------------------------------ grammar: contains form

@case
def c_contains_single_matches_singleton(work):
    _contains_case(work, 'contains-singleton', 'extractor-failure+',
                   ['extractor-failure'], 'target')


@case
def c_contains_single_matches_superset(work):
    _contains_case(work, 'contains-superset', 'extractor-failure+',
                   ['extractor-failure', 'unpublished-entry'], 'target')


@case
def c_contains_single_rejects_absent(work):
    _contains_case(work, 'contains-absent', 'extractor-failure+',
                   ['unpublished-entry'], 'fallback')


@case
def c_contains_pair_requires_all(work):
    _contains_case(work, 'contains-pair-partial', 'extractor-failure,unpublished-entry+',
                   ['extractor-failure'], 'fallback')


@case
def c_contains_pair_matches(work):
    _contains_case(work, 'contains-pair', 'extractor-failure,unpublished-entry+',
                   ['extractor-failure', 'unpublished-entry'], 'target')


@case
def c_contains_pair_matches_superset(work):
    _contains_case(work, 'contains-pair-superset',
                   'extractor-failure,unpublished-entry+',
                   ['depth-limited', 'extractor-failure', 'unpublished-entry'], 'target')


@case
def c_contains_triple_matches(work):
    _contains_case(work, 'contains-triple',
                   'depth-limited,extractor-failure,unpublished-entry+',
                   ['depth-limited', 'extractor-failure', 'unpublished-entry',
                    'missing-extractor-dependency'], 'target')


@case
def c_exact_single_rejects_superset(work):
    _contains_case(work, 'exact-single-superset', 'extractor-failure',
                   ['extractor-failure', 'unpublished-entry'], 'fallback')


@case
def c_exact_single_matches_singleton(work):
    _contains_case(work, 'exact-single', 'extractor-failure', ['extractor-failure'],
                   'target')


@case
def c_exact_pair_matches(work):
    _contains_case(work, 'exact-pair', 'extractor-failure+unpublished-entry',
                   ['extractor-failure', 'unpublished-entry'], 'target')


@case
def c_exact_pair_rejects_subset(work):
    _contains_case(work, 'exact-pair-subset', 'extractor-failure+unpublished-entry',
                   ['extractor-failure'], 'fallback')


@case
def c_contains_versus_exact_differ(work):
    """The two forms give different answers on one superset tuple: that is the change."""
    rows = [_row('contains-first', handler='squashfs_v4_*', gaps='extractor-failure+',
                 deps='*', be='*', sr='*', files='*', action='salvage-partial'),
            _row('exact-second', handler='squashfs_v4_*', gaps='extractor-failure',
                 deps='*', be='*', sr='*', files='*', action='none')]
    skill = _write(work, 'sk-forms.md', _skel(_block(rows)))
    env = _env(handler='squashfs_v4_be', gaps=['extractor-failure', 'unpublished-entry'],
               be=False, files=2)
    res, path = _cls(work, skill, env, 'env-forms.json')
    _expect_pair(res, path, 'contains-first', 'salvage-partial', 'forms-differ')


@case
def c_none_gap_rejects_superset(work):
    _contains_case(work, 'none-superset', 'none', ['unpublished-entry'], 'fallback')


@case
def c_none_gap_matches_empty(work):
    _contains_case(work, 'none-empty', 'none', [], 'target')


@case
def c_star_gap_matches_any(work):
    _contains_case(work, 'star-any', '*', ['unpublished-entry', 'depth-limited'],
                   'target')


@case
def c_deps_contains_matches_superset(work):
    """v4 delta: draft step 3 says "D holds x", so a superset dependency set matches."""
    rows = _two(_row('target', handler='squashfs_v4_be', gaps='missing-extractor-dependency+',
                     deps='sasquatch-v4be+', be='*', sr='*', files='*',
                     action='install-extractor-be'))
    skill = _write(work, 'sk-depsplus.md', _skel(_block(rows)))
    env = _env(handler='squashfs_v4_be',
               gaps=[('missing-extractor-dependency', ['sasquatch-v4be', 'unsquashfs'])])
    res, path = _cls(work, skill, env, 'env-depsplus.json')
    _expect_pair(res, path, 'target', 'install-extractor-be', 'deps-contains-superset')


@case
def c_deps_exact_rejects_superset(work):
    rows = _two(_row('target', handler='squashfs_v4_be', gaps='missing-extractor-dependency+',
                     deps='sasquatch-v4be', be='*', sr='*', files='*',
                     action='install-extractor-be'))
    skill = _write(work, 'sk-depsexact.md', _skel(_block(rows)))
    env = _env(handler='squashfs_v4_be',
               gaps=[('missing-extractor-dependency', ['sasquatch-v4be', 'unsquashfs'])])
    res, path = _cls(work, skill, env, 'env-depsexact.json')
    _expect_pair(res, path, 'fallback', 'inspect-input', 'deps-exact-superset')


@case
def c_malformed_contains_empty_member(work):
    rows = [_row('x', gaps='unpublished-entry,+')]
    skill = _write(work, 'sk-badc1.md', _skel(_block(rows)))
    res = _cli(['--skill', skill, _dump(work, 'env-badc1.json', _env())])
    _exit_is(res, 2, 'malformed-contains-empty-member')
    _require('contains' in res.stderr, 'malformed-contains-empty-member: no cause named')


@case
def c_malformed_contains_trailing_comma(work):
    rows = [_row('x', gaps='unpublished-entry,')]
    skill = _write(work, 'sk-badc2.md', _skel(_block(rows)))
    res = _cli(['--skill', skill, _dump(work, 'env-badc2.json', _env())])
    _exit_is(res, 2, 'malformed-contains-trailing-comma')
    _require('gap kinds' in res.stderr,
             'malformed-contains-trailing-comma: %r' % res.stderr)


@case
def c_malformed_contains_duplicate(work):
    rows = [_row('x', gaps='depth-limited,depth-limited+')]
    skill = _write(work, 'sk-badc3.md', _skel(_block(rows)))
    res = _cli(['--skill', skill, _dump(work, 'env-badc3.json', _env())])
    _exit_is(res, 2, 'malformed-contains-duplicate')
    _require('repeats' in res.stderr, 'malformed-contains-duplicate: %r' % res.stderr)


@case
def c_malformed_contains_space(work):
    rows = [_row('x', gaps='depth limited+')]
    skill = _write(work, 'sk-badc4.md', _skel(_block(rows)))
    res = _cli(['--skill', skill, _dump(work, 'env-badc4.json', _env())])
    _exit_is(res, 2, 'malformed-contains-space')


@case
def c_malformed_contains_member_with_plus(work):
    rows = [_row('x', gaps='a+b+')]
    skill = _write(work, 'sk-badc5.md', _skel(_block(rows)))
    res = _cli(['--skill', skill, _dump(work, 'env-badc5.json', _env())])
    _exit_is(res, 2, 'malformed-contains-member-with-plus')


@case
def c_exact_cell_rejects_comma(work):
    rows = [_row('x', gaps='extractor-failure,unpublished-entry')]
    skill = _write(work, 'sk-badc6.md', _skel(_block(rows)))
    res = _cli(['--skill', skill, _dump(work, 'env-badc6.json', _env())])
    _exit_is(res, 2, 'exact-cell-rejects-comma')
    _require('malformed member' in res.stderr,
             'exact-cell-rejects-comma: %r' % res.stderr)


@case
def c_reserved_word_as_contains_member(work):
    rows = [_row('x', gaps='none+')]
    skill = _write(work, 'sk-badc7.md', _skel(_block(rows)))
    res = _cli(['--skill', skill, _dump(work, 'env-badc7.json', _env())])
    _exit_is(res, 2, 'reserved-word-contains')
    _require('reserved' in res.stderr, 'reserved-word-contains: %r' % res.stderr)


@case
def c_reserved_word_as_exact_member(work):
    rows = [_row('x', gaps='extractor-failure+none')]
    skill = _write(work, 'sk-badc8.md', _skel(_block(rows)))
    res = _cli(['--skill', skill, _dump(work, 'env-badc8.json', _env())])
    _exit_is(res, 2, 'reserved-word-exact')
    _require('reserved' in res.stderr, 'reserved-word-exact: %r' % res.stderr)


@case
def c_table_only_prints_contains_spec(work):
    rows = [_row('a', gaps='extractor-failure,unpublished-entry+',
                 deps='sasquatch+'),
            _row('b', gaps='extractor-failure+unpublished-entry', deps='sasquatch')]
    skill = _write(work, 'sk-specs.md', _skel(_block(rows)))
    res = _cli(['--skill', skill, '--table-only'])
    _exit_is(res, 0, 'table-only-specs')
    _require('contains{extractor-failure,unpublished-entry}' in res.stdout,
             'table-only-specs: contains spec not printed (%r)' % res.stdout)
    _require('exact{extractor-failure,unpublished-entry}' in res.stdout,
             'table-only-specs: exact spec not printed')
    _require('dependencies=contains{sasquatch}' in res.stdout,
             'table-only-specs: dependencies contains spec not printed')
    _require('rules: 2' in res.stdout, 'table-only-specs: rule count missing')
    _require('failing handler globs over HF' in res.stdout,
             'table-only-specs: handler semantics line missing')


# ------------------------------------------------------------------ grammar: handler globs

@case
def c_handler_star_and_none_accepted(work):
    rows = [_row('star', handler='*'), _row('none', handler='none',
                                             action='inspect-input')]
    skill = _write(work, 'sk-hstar.md', _skel(_block(rows)))
    _exit_is(_cli(['--skill', skill, '--table-only']), 0, 'handler-star-none')


@case
def c_handler_legacy_glob_accepted(work):
    rows = [_row('legacy', handler='squashfs_*', failing='squashfs_v[123]*', action='cross-read-legacy'),
            _row('v4', handler='squashfs_v4_*')]
    skill = _write(work, 'sk-hlegacy.md', _skel(_block(rows)))
    res = _cli(['--skill', skill, '--table-only'])
    _exit_is(res, 0, 'handler-legacy-glob')
    _require('glob{squashfs_v[123]*}' in res.stdout,
             'handler-legacy-glob: glob not printed (%r)' % res.stdout)


@case
def c_handler_non_squashfs_pattern_refused(work):
    rows = [_row('x', handler='gzip*')]
    skill = _write(work, 'sk-hgzip.md', _skel(_block(rows)))
    res = _cli(['--skill', skill, '--table-only'])
    _exit_is(res, 2, 'handler-non-squashfs')
    _require('squashfs' in res.stderr and 'dead cell' in res.stderr,
             'handler-non-squashfs: %r' % res.stderr)
    _require('does not begin' in res.stderr,
             'handler-non-squashfs: the prefix guard did not fire (%r)' % res.stderr)


@case
def c_handler_unknown_version_refused(work):
    rows = [_row('x', handler='squashfs_v9*')]
    skill = _write(work, 'sk-hv9.md', _skel(_block(rows)))
    res = _cli(['--skill', skill, '--table-only'])
    _exit_is(res, 2, 'handler-unknown-version')
    _require('squashfs_v9*' in res.stderr, 'handler-unknown-version: %r' % res.stderr)


@case
def c_handler_case_mismatch_refused(work):
    rows = [_row('x', handler='squashfs_V4*')]
    skill = _write(work, 'sk-hcase.md', _skel(_block(rows)))
    res = _cli(['--skill', skill, '--table-only'])
    _exit_is(res, 2, 'handler-case-mismatch')


@case
def c_handler_broadcom_name_accepted(work):
    rows = [_row('bc', handler='squashfs_v4_broadcom', action='preserve-failure'),
            _row('bc2', handler='squashfs_v3_broadcom', action='cross-read-legacy')]
    skill = _write(work, 'sk-hbc.md', _skel(_block(rows)))
    _exit_is(_cli(['--skill', skill, '--table-only']), 0, 'handler-broadcom')


# ------------------------------------------------------------------ grammar: markers

@case
def c_v3_marker_refused(work):
    rows = [_row('stale', handler='squashfs_v4_*', gaps='none', deps='none',
                 be='*', sr='no', files='>0', action='none')]
    skill = _write(work, 'sk-v3.md',
                   _skel(_block(rows, marker='<!-- sqfs-triage-table v3 -->')))
    res = _cli(['--skill', skill, _dump(work, 'env-v3ref.json',
                                        _env(handler='squashfs_v4_be', be=False,
                                             files=1))])
    _exit_is(res, 2, 'v3-marker-refused')
    _require('v3' in res.stderr, 'v3-marker-refused: stderr does not name v3 (%r)'
             % res.stderr)
    _require('refused' in res.stderr, 'v3-marker-refused: stderr does not say refused')


@case
def c_v2_marker_refused(work):
    rows = [_row('stale', handler='squashfs_v4_*', gaps='none', deps='none',
                 be='*', sr='no', files='>0', action='none')]
    skill = _write(work, 'sk-v2.md',
                   _skel(_block(rows, marker='<!-- sqfs-triage-table v2 -->')))
    res = _cli(['--skill', skill, _dump(work, 'env-v2.json',
                                        _env(handler='squashfs_v4_be', be=False, files=1))])
    _exit_is(res, 2, 'v2-marker-refused')
    _require('v2' in res.stderr, 'v2-marker-refused: stderr does not name v2 (%r)'
             % res.stderr)
    _require('refused' in res.stderr, 'v2-marker-refused: stderr does not say refused')


@case
def c_v1_marker_refused(work):
    rows = [_row('stale')]
    skill = _write(work, 'sk-v1.md',
                   _skel(_block(rows, marker='<!-- sqfs-triage-table v1 -->')))
    res = _cli(['--skill', skill, _dump(work, 'env-v1.json', _env())])
    _exit_is(res, 2, 'v1-marker-refused')
    _require('v1' in res.stderr, 'v1-marker-refused: stderr does not name v1 (%r)'
             % res.stderr)


@case
def c_v4_marker_selects_its_table_over_earlier_v3_block(work):
    stale = _block([_row('stale', action='inspect-input')],
                   marker='<!-- sqfs-triage-table v3 -->')
    live_rows = [_row('live', handler='squashfs_v4_*', gaps='none', deps='none',
                      be='*', sr='no', files='>0', action='confirm-empty')]
    live = _block(live_rows)
    text = ('# SKILL\n\n## Queue-drain craft\n\nHistory:\n\n' + stale
            + '\nLive table:\n\n' + live + '\n## A later section\n')
    skill = _write(work, 'sk-both.md', text)
    res, path = _cls(work, skill, _env(handler='squashfs_v4_be', be=False, files=1),
                     'env-both.json')
    _expect_pair(res, path, 'live', 'confirm-empty', 'v4-marker-wins')


@case
def c_marker_absent(work):
    skill = _write(work, 'sk-nomarker.md', _skel(_block([_row('x')], marker=None)))
    res = _cli(['--skill', skill, _dump(work, 'env-nomarker.json', _env())])
    _exit_is(res, 2, 'marker-absent')
    _require('absent' in res.stderr, 'marker-absent: %r' % res.stderr)


@case
def c_marker_outside_craft(work):
    block = _block([_row('x')])
    text = ('# SKILL\n\n## Queue-drain craft\n\nNo table here.\n\n'
            '## A later section\n\n' + block + '\n')
    skill = _write(work, 'sk-outside.md', text)
    res = _cli(['--skill', skill, _dump(work, 'env-outside.json', _env())])
    _exit_is(res, 2, 'marker-outside-craft')
    _require('marker' in res.stderr, 'marker-outside-craft: %r' % res.stderr)


@case
def c_no_craft_section(work):
    skill = _write(work, 'sk-nocraft.md', '# SKILL\n\n## Other\n\n' + _block([_row('x')]))
    res = _cli(['--skill', skill, '--table-only'])
    _exit_is(res, 2, 'no-craft-section')
    _require('craft' in res.stderr, 'no-craft-section: %r' % res.stderr)


@case
def c_marker_without_table(work):
    skill = _write(work, 'sk-notable.md',
                   _skel(MARKER + '\n\n' + _vocab_line()
                         + '\n\nOnly prose follows the vocabulary.\n'))
    res = _cli(['--skill', skill, '--table-only'])
    _exit_is(res, 2, 'marker-without-table')
    _require('no markdown table' in res.stderr,
             'marker-without-table: %r' % res.stderr)


# ------------------------------------------------------------------ grammar: the rest

@case
def c_duplicate_label(work):
    rows = [_row('same'), _row('same', action='inspect-input')]
    skill = _write(work, 'sk-dup.md', _skel(_block(rows)))
    res = _cli(['--skill', skill, _dump(work, 'env-dup.json', _env())])
    _exit_is(res, 2, 'duplicate-label')
    _require('duplicate' in res.stderr and 'same' in res.stderr,
             'duplicate-label: stderr does not name the duplicate (%r)' % res.stderr)


@case
def c_unknown_action(work):
    rows = [_row('x', action='levitate')]
    skill = _write(work, 'sk-badaction.md', _skel(_block(rows)))
    res = _cli(['--skill', skill, '--table-only'])
    _exit_is(res, 2, 'unknown-action')
    _require('levitate' in res.stderr, 'unknown-action: stderr does not name the token')


@case
def c_missing_actions_line(work):
    rows = [_row('x')]
    skill = _write(work, 'sk-noactions.md', _skel(_block(rows, actions=False)))
    res = _cli(['--skill', skill, '--table-only'])
    _exit_is(res, 2, 'missing-actions-line')
    _require(ACTIONS_PREFIX in res.stderr, 'missing-actions-line: %r' % res.stderr)


@case
def c_actions_line_separated_by_prose(work):
    block = [_vocab_line(), '', 'prose between vocabulary and table', '',
             '| ' + ' | '.join(HEADER) + ' |',
             '| ' + ' | '.join(['---'] * len(HEADER)) + ' |',
             '| ' + ' | '.join(_row('x')) + ' |']
    text = '# SKILL\n\n## Queue-drain craft\n\n' + MARKER + '\n\n' + '\n'.join(block) + '\n'
    skill = _write(work, 'sk-prose.md', text)
    res = _cli(['--skill', skill, '--table-only'])
    _exit_is(res, 2, 'actions-line-separated-by-prose')


@case
def c_duplicate_action_vocabulary(work):
    skill = _write(work, 'sk-dupvocab.md',
                   _skel(_block([_row('x')],
                                vocab_line=_vocab_line('none none'))))
    res = _cli(['--skill', skill, '--table-only'])
    _exit_is(res, 2, 'duplicate-vocabulary')
    _require('twice' in res.stderr, 'duplicate-vocabulary: %r' % res.stderr)


@case
def c_malformed_header(work):
    header = list(HEADER)
    header[3] = 'chunk handler'
    skill = _write(work, 'sk-badhdr.md', _skel(_block([_row('x')], header=header)))
    res = _cli(['--skill', skill, '--table-only'])
    _exit_is(res, 2, 'malformed-header')
    _require('header' in res.stderr, 'malformed-header: %r' % res.stderr)


@case
def c_malformed_operation_cell(work):
    rows = [_row('x', operation='extract firmware')]
    skill = _write(work, 'sk-badop.md', _skel(_block(rows)))
    res = _cli(['--skill', skill, '--table-only'])
    _exit_is(res, 2, 'malformed-operation-cell')
    _require('operation' in res.stderr, 'malformed-operation-cell: %r' % res.stderr)


@case
def c_malformed_files_cell(work):
    rows = [_row('x', files='many')]
    skill = _write(work, 'sk-badfiles.md', _skel(_block(rows)))
    res = _cli(['--skill', skill, '--table-only'])
    _exit_is(res, 2, 'malformed-files-cell')
    _require('published files' in res.stderr, 'malformed-files-cell: %r' % res.stderr)


@case
def c_empty_action_cell(work):
    rows = [_row('x', action='')]
    skill = _write(work, 'sk-emptyaction.md', _skel(_block(rows)))
    res = _cli(['--skill', skill, '--table-only'])
    _exit_is(res, 2, 'empty-action-cell')


@case
def c_cause_without_arrow(work):
    rows = [_row('x', cause='no arrow here')]
    skill = _write(work, 'sk-noarrow.md', _skel(_block(rows)))
    res = _cli(['--skill', skill, '--table-only'])
    _exit_is(res, 2, 'cause-without-arrow')


@case
def c_row_cell_count(work):
    row = _row('x')[:-1]
    skill = _write(work, 'sk-cellcount.md', _skel(_block([row])))
    res = _cli(['--skill', skill, '--table-only'])
    _exit_is(res, 2, 'row-cell-count')


@case
def c_first_match_order(work):
    rows = [_row('first', handler='squashfs_v4_*', gaps='none', deps='none', be='*',
                 sr='no', files='>0', action='none'),
            _row('second', handler='squashfs_v4_*', gaps='none', deps='none', be='*',
                 sr='no', files='>0', action='inspect-input')]
    skill = _write(work, 'sk-order.md', _skel(_block(rows)))
    res, path = _cls(work, skill, _env(handler='squashfs_v4_be', be=False, files=1),
                     'env-order.json')
    _expect_pair(res, path, 'first', 'none', 'first-match-order')


@case
def c_first_table_wins(work):
    first = _block([_row('first-table')])
    second = _block([_row('second-table')], marker=None)
    text = ('# SKILL\n\n## Queue-drain craft\n\n' + first + '\nprose\n\n' + second + '\n')
    skill = _write(work, 'sk-twotables.md', text)
    res, path = _cls(work, skill, _env(), 'env-twotables.json')
    _expect_pair(res, path, 'first-table', 'none', 'first-table-wins')


@case
def c_print_table_removed(work):
    """R40-CL5 M1: no embedded table, so no --print-table surface either."""
    res = _cli(['--print-table'])
    _exit_is(res, 2, 'print-table-removed')
    _require('--skill' in res.stderr, 'print-table-removed: %r' % res.stderr)


@case
def c_no_embedded_table(work):
    with open(os.path.abspath(__file__), 'r', encoding='utf-8') as handle:
        text = handle.read()
    needle = '| %s | operation |' % 'label'
    _require(needle not in text,
             'embedded-table: the module still carries a table row literal')
    assignment = 'TABLE_BLOCK' + ' ='
    _require(assignment not in text,
             'embedded-table: the module still assigns TABLE_BLOCK')


# ------------------------------------------------------------------ envelope features

@case
def c_domain_guard_operation(work):
    rows = _two(_row('target', handler='squashfs_v4_*', gaps='none', deps='none', be='*',
                     sr='no', files='>0'))
    skill = _write(work, 'sk-guard-op.md', _skel(_block(rows)))
    res, path = _cls(work, skill,
                     _env(handler='squashfs_v4_be', be=False, files=1,
                          op='inspect_firmware_regions'), 'env-guard-op.json')
    _expect_pair(res, path, 'unclassified', 'none', 'domain-guard-operation')


@case
def c_domain_guard_provider(work):
    rows = _two(_row('target', handler='squashfs_v4_*', gaps='none', deps='none', be='*',
                     sr='no', files='>0'))
    skill = _write(work, 'sk-guard-pv.md', _skel(_block(rows)))
    res, path = _cls(work, skill,
                     _env(handler='squashfs_v4_be', be=False, files=1, pv='binwalk'),
                     'env-guard-pv.json')
    _expect_pair(res, path, 'unclassified', 'none', 'domain-guard-provider')


@case
def c_domain_guard_without_normalized_result(work):
    rows = _two(_row('target', handler='none', gaps='*', deps='*', be='*', sr='*',
                     files='*', action='inspect-input'))
    skill = _write(work, 'sk-guard-bare.md', _skel(_block(rows)))
    env = {'operation': 'inspect_firmware_regions',
           'provider': {'id': 'unblob', 'name': 'Unblob', 'version': '26.6.4'}}
    res, path = _cls(work, skill, env, 'env-guard-bare.json')
    _expect_pair(res, path, 'unclassified', 'none', 'domain-guard-bare')


@case
def c_extract_envelope_without_normalized_result(work):
    skill = _write(work, 'sk-need-nr.md', _skel(_block([_row('x')])))
    res = _cli(['--skill', skill,
                _dump(work, 'env-no-nr.json', {'operation': 'extract_firmware'})])
    _exit_is(res, 2, 'extract-envelope-without-normalized-result')


@case
def c_envelope_unreadable(work):
    skill = _write(work, 'sk-unread.md', _skel(_block([_row('x')])))
    res = _cli(['--skill', skill, os.path.join(work, 'absent.json')])
    _exit_is(res, 2, 'envelope-missing')
    empty = _write(work, 'empty.json', '{}')
    _exit_is(_cli(['--skill', skill, empty]), 2, 'envelope-empty-object')
    bad = _write(work, 'bad.json', '{not json')
    _exit_is(_cli(['--skill', skill, bad]), 2, 'envelope-bad-json')
    scalar = _write(work, 'scalar.json', '7')
    _exit_is(_cli(['--skill', skill, scalar]), 2, 'envelope-scalar')


@case
def c_bare_vs_full(work):
    rows = _two(_row('target', handler='squashfs_v4_*', gaps='none', deps='none', be='*',
                     sr='no', files='>0', action='none'))
    skill = _write(work, 'sk-both.md', _skel(_block(rows)))
    bare = _env(handler='squashfs_v4_be', be=False, files=2)
    full = {'ok': True, 'data': bare, 'meta': {'command': 'extract-firmware'}}
    res = _cli(['--skill', skill, '--json', _dump(work, 'env-bare.json', bare),
                _dump(work, 'env-full.json', full)])
    payload = _json_of(res, 'bare-vs-full')
    _require(len(payload['results']) == 2, 'bare-vs-full: expected two results')
    left, right = payload['results']
    _require(left['features'] == right['features'],
             'bare-vs-full: features differ %r vs %r' % (left['features'],
                                                        right['features']))
    _require((left['label'], left['action']) == (right['label'], right['action']),
             'bare-vs-full: decisions differ')


@case
def c_be_values(work):
    skill = _write(work, 'sk-bevalues.md',
                   _skel(_block([_row('x', handler='squashfs_v4_*', gaps='none',
                                      deps='none', be='*', sr='no', files='*')])))
    yes = _dump(work, 'env-be-yes.json', _env(handler='squashfs_v4_be', be=True, files=1))
    no = _dump(work, 'env-be-no.json', _env(handler='squashfs_v4_be', be=False, files=1))
    na = _dump(work, 'env-be-na.json', _env(handler='squashfs_v4_be', be=None, files=1))
    res = _cli(['--skill', skill, '--json', yes, no, na])
    payload = _json_of(res, 'be-values')
    values = [entry['features']['BE'] for entry in payload['results']]
    _require(values == ['yes', 'no', 'n/a'], 'be-values: BE values are %r' % values)


@case
def c_be_token_not_substring(work):
    skill = _write(work, 'sk-besub.md',
                   _skel(_block([_row('avm', handler='squashfs_*', failing='squashfs_v4_be',
                                      gaps='extractor-failure+', deps='*', be='no',
                                      sr='*', files='0', action='wrap-extractor-be')])))
    env = _env(handler='squashfs_v4_be', gaps=['extractor-failure'],
               command='/usr/local/bin/sasquatch-v4be -be=1 -d /out /in')
    res, _path = _cls(work, skill, env, 'env-besub.json', extra=('--json',))
    payload = _json_of(res, 'be-token-not-substring')
    entry = payload['results'][0]
    _require(entry['features']['BE'] == 'no',
             'be-token-not-substring: BE is %r (only a standalone -be token counts)'
             % entry['features']['BE'])
    _require(entry['label'] == 'avm', 'be-token-not-substring: label is %r'
             % entry['label'])


@case
def c_be_string_command_with_token(work):
    skill = _write(work, 'sk-bestr.md',
                   _skel(_block([_row('yes', handler='squashfs_v4_be', gaps='none',
                                      deps='none', be='yes', sr='no', files='>0',
                                      action='inspect-input')])))
    env = _env(handler='squashfs_v4_be', files=1,
               command='/usr/local/bin/sasquatch-v4be -be -d /out /in')
    res, path = _cls(work, skill, env, 'env-bestr.json')
    _expect_pair(res, path, 'yes', 'inspect-input', 'be-string-command')


@case
def c_be_argv_list_key(work):
    """A report may carry the argv as a list under ``argv`` instead of ``command``."""
    skill = _write(work, 'sk-beargv.md',
                   _skel(_block([_row('yes', handler='squashfs_v4_be', gaps='none',
                                      deps='none', be='yes', sr='no', files='>0',
                                      action='inspect-input')])))
    env = _env(handler='squashfs_v4_be', files=1)
    env['normalized_result']['diagnostics'] = [
        {'report': {'argv': ['/usr/local/bin/sasquatch', '-be', '-d', '/out', '/in']}}]
    res, path = _cls(work, skill, env, 'env-beargv.json')
    _expect_pair(res, path, 'yes', 'inspect-input', 'be-argv-list-key')


@case
def c_be_ignores_non_sasquatch_argv(work):
    """BE counts sasquatch child argvs only; another extractor's -be is not ours."""
    skill = _write(work, 'sk-beother.md',
                   _skel(_block([_row('na', handler='squashfs_v4_be', gaps='none',
                                      deps='none', be='n/a', sr='no', files='>0',
                                      action='inspect-input')])))
    env = _env(handler='squashfs_v4_be', files=1,
               command='/usr/local/bin/ubireader -be -d /out /in')
    res, path = _cls(work, skill, env, 'env-beother.json')
    _expect_pair(res, path, 'na', 'inspect-input', 'be-ignores-non-sasquatch')


@case
def c_sr_from_raw_result(work):
    skill = _write(work, 'sk-srraw.md',
                   _skel(_block([_row('esc', handler='squashfs_v4_*', gaps='none',
                                      deps='none', be='*', sr='yes', files='*',
                                      action='expect-link-absent')])))
    res, path = _cls(work, skill, _env(handler='squashfs_v4_be', be=False, files=1,
                                       sr=True), 'env-srraw.json')
    _expect_pair(res, path, 'esc', 'expect-link-absent', 'sr-from-raw-result')


@case
def c_sr_from_diagnostics_report_only(work):
    """No raw_result at all: the diagnostics report alone must read SR = yes."""
    skill = _write(work, 'sk-srdiag.md',
                   _skel(_block([_row('esc', handler='squashfs_v4_*', gaps='none',
                                      deps='none', be='*', sr='yes', files='*',
                                      action='expect-link-absent')])))
    res, path = _cls(work, skill, _env(handler='squashfs_v4_be', be=False, files=1,
                                       sr=True, sr_where='diag-report'),
                     'env-srdiag.json')
    _expect_pair(res, path, 'esc', 'expect-link-absent', 'sr-diag-report')


@case
def c_sr_from_diag_level_holder(work):
    """A trimmed envelope may keep the typename on diagnostics[] itself."""
    skill = _write(work, 'sk-srdiaglvl.md',
                   _skel(_block([_row('esc', handler='squashfs_v4_*', gaps='none',
                                      deps='none', be='*', sr='yes', files='*',
                                      action='expect-link-absent')])))
    res, path = _cls(work, skill, _env(handler='squashfs_v4_be', be=False, files=1,
                                       sr=True, sr_where='diag'), 'env-srdiaglvl.json')
    _expect_pair(res, path, 'esc', 'expect-link-absent', 'sr-diag-level-holder')


@case
def c_sr_stdout_text_is_not_a_report(work):
    """Deliberate: a bare token in printed stdout is not a producer report."""
    skill = _write(work, 'sk-srstdout.md',
                   _skel(_block([_row('esc', handler='squashfs_v4_*', gaps='none',
                                      deps='none', be='*', sr='no', files='>0',
                                      action='none')])))
    res, path = _cls(work, skill, _env(handler='squashfs_v4_be', be=False, files=2,
                                       sr=True, sr_where='stdout'),
                     'env-srstdout.json')
    _expect_pair(res, path, 'esc', 'none', 'sr-stdout-text')


@case
def c_published_files_split(work):
    rows = [_row('some', handler='squashfs_v4_*', gaps='none', deps='none', be='*',
                 sr='no', files='>0', action='none'),
            _row('none-at-all', handler='squashfs_v4_*', gaps='none', deps='none', be='*',
                 sr='no', files='0', action='confirm-empty')]
    skill = _write(work, 'sk-files.md', _skel(_block(rows)))
    res, path = _cls(work, skill, _env(handler='squashfs_v4_be', be=False, files=0),
                     'env-files0.json')
    _expect_pair(res, path, 'none-at-all', 'confirm-empty', 'files-zero')
    res, path = _cls(work, skill, _env(handler='squashfs_v4_be', be=False, files=3),
                     'env-files3.json')
    _expect_pair(res, path, 'some', 'none', 'files-positive')


@case
def c_files_absent_reads_zero(work):
    rows = [_row('empty', handler='squashfs_*', gaps='none', deps='none', be='*',
                 sr='no', files='0', action='confirm-empty'),
            _row('some', handler='squashfs_*', gaps='none', deps='none', be='*',
                 sr='no', files='>0', action='none')]
    skill = _write(work, 'sk-filesabsent.md', _skel(_block(rows)))
    res, path = _cls(work, skill, _env(handler='squashfs_v4_le', be=False,
                                       files=0, files_absent=True),
                     'env-filesabsent.json')
    _expect_pair(res, path, 'empty', 'confirm-empty', 'files-absent')


@case
def c_handler_none_rejects_squashfs(work):
    rows = _two(_row('nochunk', handler='none', gaps='*', deps='*', be='*', sr='*',
                     files='*', action='inspect-input'))
    skill = _write(work, 'sk-nonereject.md', _skel(_block(rows)))
    res, path = _cls(work, skill, _env(handler='squashfs_v4_le', be=False, files=1),
                     'env-nonereject.json')
    _expect_pair(res, path, 'fallback', 'inspect-input', 'handler-none-rejects')


@case
def c_handler_none_matches_bare(work):
    rows = _two(_row('nochunk', handler='none', gaps='*', deps='*', be='*', sr='*',
                     files='*', action='inspect-input'))
    skill = _write(work, 'sk-nonehit.md', _skel(_block(rows)))
    res, path = _cls(work, skill, _env(handler=None, be=None, files=0),
                     'env-nonehit.json')
    _expect_pair(res, path, 'nochunk', 'inspect-input', 'handler-none-matches')


@case
def c_handler_none_matches_non_squashfs_handler(work):
    """R41-CL4: a chunk that is not SquashFS is F = empty, not 'unclassified'."""
    rows = [_row('nochunk', handler='none', gaps='*', deps='*', be='*', sr='*',
                 files='*', action='inspect-input')]
    skill = _write(work, 'sk-nonegzip.md', _skel(_block(rows)))
    res, path = _cls(work, skill, _env(handler='gzip', be=None, files=3),
                     'env-nonegzip.json')
    _expect_pair(res, path, 'nochunk', 'inspect-input', 'handler-none-non-squashfs')


@case
def c_handler_from_gap_row(work):
    """H is chunks ∪ gaps: a gap row keeps the handler of a chunk not published."""
    rows = [_row('none', handler='none', gaps='*', deps='*', be='*', sr='*', files='*',
                 action='inspect-input'),
            _row('seen', handler='squashfs_*', gaps='*', deps='*', be='*', sr='*',
                 files='*', action='none')]
    skill = _write(work, 'sk-gaphandler.md', _skel(_block(rows)))
    env = _env(handler=None, be=None, files=0,
               gaps=[('depth-limited', [])], gap_handlers={'depth-limited':
                                                           'squashfs_v4_be'})
    res, path = _cls(work, skill, env, 'env-gaphandler.json')
    _expect_pair(res, path, 'seen', 'none', 'handler-from-gap-row')


@case
def c_fnmatch_handler(work):
    rows = _two(_row('pat', handler='squashfs_v4_?e', gaps='unpublished-entry',
                     deps='none', be='*', sr='no', files='*', action='count-gap'))
    skill = _write(work, 'sk-pat.md', _skel(_block(rows)))
    res, path = _cls(work, skill,
                     _env(handler='squashfs_v4_le', gaps=['unpublished-entry'], be=False,
                          files=2), 'env-pat.json')
    _expect_pair(res, path, 'pat', 'count-gap', 'fnmatch-handler')


@case
def c_json_shape(work):
    rows = [_row('esc', handler='squashfs_v4_*', gaps='none', deps='none', be='*',
                 sr='yes', files='*', action='expect-link-absent')]
    skill = _write(work, 'sk-json.md', _skel(_block(rows)))
    res, _path = _cls(work, skill, _env(handler='squashfs_v4_be', be=False, files=1,
                                        sr=True), 'env-json.json', extra=('--json',))
    payload = _json_of(res, 'json-shape')
    entry = payload['results'][0]
    _require(entry['rule'] == 1, 'json-shape: rule index is %r' % entry['rule'])
    _require(len(entry['row']) == len(HEADER), 'json-shape: row has %r cells'
             % len(entry['row']))
    _require(entry['row'][0] == 'esc', 'json-shape: row label is %r' % entry['row'][0])
    for key in ('OP', 'PV', 'H', 'F', 'HF', 'G', 'D', 'BE', 'SR', 'P'):
        _require(key in entry['features'], 'json-shape: feature %r missing' % key)
    _require(entry['features']['G'] == [], 'json-shape: G is %r'
             % entry['features']['G'])
    _require(payload['actions'] == VOCAB.split(), 'json-shape: actions are %r'
             % payload['actions'])
    _require(payload['rules'] == 1, 'json-shape: rules is %r' % payload['rules'])


@case
def c_invocation_requires_skill(work):
    res = _cli(['--table-only'])
    _exit_is(res, 2, 'skill-required')
    _require('--skill' in res.stderr, 'skill-required: %r' % res.stderr)
    skill = _write(work, 'sk-noenv.md', _skel(_block([_row('x')])))
    res = _cli(['--skill', skill])
    _exit_is(res, 2, 'no-envelope')


# ------------------------------------------------------------------ combined gap sets

@case
def c_combined_partial_plus_in_tree(work):
    rows = [_row('partial', handler='squashfs_v4_*', gaps='extractor-failure+',
                 deps='*', be='*', sr='*', files='>0', action='salvage-partial'),
            _row('in-tree', handler='squashfs_v4_*', gaps='unpublished-entry',
                 deps='none', be='*', sr='no', files='*', action='count-gap')]
    skill = _write(work, 'sk-comb1.md', _skel(_block(rows)))
    res, path = _cls(work, skill,
                     _env(handler='squashfs_v4_be', gaps=['extractor-failure',
                                                          'unpublished-entry'],
                          be=False, files=4), 'env-comb1.json')
    _expect_pair(res, path, 'partial', 'salvage-partial', 'combined-partial-in-tree')


@case
def c_combined_partial_plus_mixed(work):
    rows = [_row('partial', handler='squashfs_v4_*', gaps='extractor-failure+',
                 deps='*', be='*', sr='*', files='>0', action='salvage-partial'),
            _row('mixed', handler='squashfs_v4_*', gaps='unpublished-entry+',
                 deps='*', be='*', sr='yes', files='*', action='audit-symlinks')]
    skill = _write(work, 'sk-comb2.md', _skel(_block(rows)))
    res, path = _cls(work, skill,
                     _env(handler='squashfs_v4_be', gaps=['extractor-failure',
                                                          'unpublished-entry'],
                          be=False, sr=True, files=4), 'env-comb2.json')
    _expect_pair(res, path, 'partial', 'salvage-partial', 'combined-partial-mixed')


@case
def c_combined_depth_plus_mixed(work):
    rows = [_row('depth', handler='squashfs_v4_*', gaps='depth-limited+', deps='*',
                 be='*', sr='*', files='*', action='raise-depth'),
            _row('mixed', handler='squashfs_v4_*', gaps='unpublished-entry+', deps='*',
                 be='*', sr='yes', files='*', action='audit-symlinks')]
    skill = _write(work, 'sk-comb3.md', _skel(_block(rows)))
    res, path = _cls(work, skill,
                     _env(handler='squashfs_v4_be', gaps=['depth-limited',
                                                          'unpublished-entry'],
                          be=False, sr=True, files=2), 'env-comb3.json')
    _expect_pair(res, path, 'depth', 'raise-depth', 'combined-depth-mixed')


@case
def c_combined_dependency_plus_failure(work):
    rows = [_row('dep-le', handler='squashfs_v4_*', gaps='missing-extractor-dependency+',
                 deps='sasquatch+', be='*', sr='*', files='*',
                 action='install-extractor-le'),
            _row('partial', handler='squashfs_v4_*', gaps='extractor-failure+',
                 deps='*', be='*', sr='*', files='>0', action='salvage-partial')]
    skill = _write(work, 'sk-comb4.md', _skel(_block(rows)))
    res, path = _cls(work, skill,
                     _env(handler='squashfs_v4_le',
                          gaps=[('missing-extractor-dependency', ['sasquatch']),
                                'extractor-failure'], be=False, files=2),
                     'env-comb4.json')
    _expect_pair(res, path, 'dep-le', 'install-extractor-le', 'combined-dep-failure')


# ------------------------------------------------------------------ v4: legacy family

LEGACY_HANDLERS = ('squashfs_v1', 'squashfs_v2', 'squashfs_v2_nonstandard',
                   'squashfs_v3', 'squashfs_v3_ddwrt', 'squashfs_v3_broadcom',
                   'squashfs_v3_nonstandard')


@case
def c_non_failure_gap_handler_is_not_the_failing_handler(work):
    """HF is the extractor-failure row only; another gap's handler must not steer it."""
    rows = [_row('avm', handler='squashfs_*', failing='squashfs_v4_be', gaps='extractor-failure+', deps='*',
                 be='no', sr='*', files='0', action='wrap-extractor-be'),
            _row('legacy', handler='squashfs_*', failing='squashfs_v[123]*', gaps='extractor-failure+',
                 deps='*', be='*', sr='*', files='0', action='cross-read-legacy')]
    skill = _write(work, 'sk-hfonly.md', _skel(_block(rows)))
    env = _env(handler='squashfs_v4_be', handlers=('squashfs_v3',),
               gaps=['extractor-failure', 'depth-limited'], be=False, files=0,
               gap_handlers={'extractor-failure': 'squashfs_v3',
                             'depth-limited': 'squashfs_v4_be'})
    res, path = _cls(work, skill, env, 'env-hfonly.json')
    _expect_pair(res, path, 'legacy', 'cross-read-legacy', 'hf-is-failure-row-only')


@case
def c_p_count_is_exact(work):
    """P is a count, not a boolean: the feature must survive to --json unchanged."""
    skill = _write(work, 'sk-pcount.md',
                   _skel(_block([_row('clean', handler='squashfs_*', gaps='none',
                                      deps='none', be='*', sr='no', files='>0',
                                      action='none')])))
    res, _path = _cls(work, skill, _env(handler='squashfs_v4_le', be=False, files=5),
                      'env-pcount.json', extra=('--json',))
    payload = _json_of(res, 'p-count')
    entry = payload['results'][0]
    _require(entry['features']['P'] == 5,
             'p-count: P is %r, expected 5' % (entry['features']['P'],))
    _require(entry['label'] == 'clean', 'p-count: label is %r' % entry['label'])


@case
def c_files_zero_cell_ordered_first(work):
    """A ``0`` cell written first must still reject a non-zero count."""
    rows = [_row('must-be-empty', handler='squashfs_*', gaps='none', deps='none',
                 be='*', sr='no', files='0', action='confirm-empty'),
            _row('some', handler='squashfs_*', gaps='none', deps='none', be='*',
                 sr='no', files='>0', action='none')]
    skill = _write(work, 'sk-zerofirst.md', _skel(_block(rows)))
    res, path = _cls(work, skill, _env(handler='squashfs_v4_le', be=False, files=3),
                     'env-zerofirst.json')
    _expect_pair(res, path, 'some', 'none', 'zero-cell-ordered-first')
    res, path = _cls(work, skill, _env(handler='squashfs_v4_le', be=False, files=0),
                     'env-zerofirst0.json')
    _expect_pair(res, path, 'must-be-empty', 'confirm-empty', 'zero-cell-ordered-first-0')


@case
def c_legacy_clean_labelled_by_family_cell(work):
    rows = _two(_row('clean', handler='squashfs_*', gaps='none', deps='none', be='*',
                     sr='no', files='>0', action='none'))
    skill = _write(work, 'sk-legacyclean.md', _skel(_block(rows)))
    for handler in LEGACY_HANDLERS:
        res, path = _cls(work, skill,
                         _env(handler=handler, be=False, files=2),
                         'env-legacyclean-%s.json' % handler)
        _expect_pair(res, path, 'clean', 'none', 'legacy-clean-%s' % handler)


@case
def c_v4_cell_rejects_legacy_handler(work):
    """CTL-C2-9 boundary: squashfs_v4_* cannot see a legacy-only chunk (R41-CL4)."""
    rows = [_row('v4only', handler='squashfs_v4_*', gaps='none', deps='none', be='*',
                 sr='no', files='>0', action='none')]
    skill = _write(work, 'sk-v4only.md', _skel(_block(rows)))
    res, path = _cls(work, skill, _env(handler='squashfs_v3', be=False, files=2),
                     'env-v4only.json')
    _expect_pair(res, path, 'unclassified', 'none', 'v4-cell-rejects-legacy')


@case
def c_legacy_failure_each_handler(work):
    rows = [_row('avm', handler='squashfs_*', failing='squashfs_v4_be', gaps='extractor-failure+', deps='*',
                 be='no', sr='*', files='0', action='wrap-extractor-be'),
            _row('legacy', handler='squashfs_*', failing='squashfs_v[123]*', gaps='extractor-failure+',
                 deps='*', be='*', sr='*', files='0', action='cross-read-legacy'),
            _row('body', handler='squashfs_*', gaps='extractor-failure+', deps='*',
                 be='*', sr='*', files='0', action='preserve-failure')]
    skill = _write(work, 'sk-legacyfail.md', _skel(_block(rows)))
    for handler in LEGACY_HANDLERS:
        env = _env(handler=handler, gaps=[('extractor-failure', [])], be=False,
                   files=0, gap_handlers={'extractor-failure': handler})
        res, path = _cls(work, skill, env, 'env-legacyfail-%s.json' % handler)
        _expect_pair(res, path, 'legacy', 'cross-read-legacy',
                     'legacy-failure-%s' % handler)


@case
def c_legacy_failure_be_yes(work):
    """Step 6 has no BE condition; a legacy failure with -be recorded is still step 6."""
    rows = [_row('avm', handler='squashfs_*', failing='squashfs_v4_be', gaps='extractor-failure+', deps='*',
                 be='no', sr='*', files='0', action='wrap-extractor-be'),
            _row('legacy', handler='squashfs_*', failing='squashfs_v[123]*', gaps='extractor-failure+',
                 deps='*', be='*', sr='*', files='0', action='cross-read-legacy'),
            _row('body', handler='squashfs_*', gaps='extractor-failure+', deps='*',
                 be='*', sr='*', files='0', action='preserve-failure')]
    skill = _write(work, 'sk-legacybe.md', _skel(_block(rows)))
    env = _env(handler='squashfs_v3', gaps=[('extractor-failure', [])], be=True,
               files=0, gap_handlers={'extractor-failure': 'squashfs_v3'})
    res, path = _cls(work, skill, env, 'env-legacybe.json')
    _expect_pair(res, path, 'legacy', 'cross-read-legacy', 'legacy-failure-be-yes')


@case
def c_legacy_dependency_resolves_plain_sasquatch(work):
    rows = [_row('be', handler='squashfs_*', gaps='missing-extractor-dependency+',
                 deps='sasquatch-v4be+', be='*', sr='*', files='*',
                 action='install-extractor-be'),
            _row('le', handler='squashfs_*', gaps='missing-extractor-dependency+',
                 deps='sasquatch+', be='*', sr='*', files='*',
                 action='install-extractor-le')]
    skill = _write(work, 'sk-legacydep.md', _skel(_block(rows)))
    env = _env(handler='squashfs_v3',
               gaps=[('missing-extractor-dependency', ['sasquatch'])])
    res, path = _cls(work, skill, env, 'env-legacydep.json')
    _expect_pair(res, path, 'le', 'install-extractor-le', 'legacy-dependency-le')


@case
def c_dep_both_names_choose_be(work):
    rows = [_row('be', handler='squashfs_*', gaps='missing-extractor-dependency+',
                 deps='sasquatch-v4be+', be='*', sr='*', files='*',
                 action='install-extractor-be'),
            _row('le', handler='squashfs_*', gaps='missing-extractor-dependency+',
                 deps='sasquatch+', be='*', sr='*', files='*',
                 action='install-extractor-le')]
    skill = _write(work, 'sk-depsboth.md', _skel(_block(rows)))
    env = _env(handler='squashfs_v4_be',
               gaps=[('missing-extractor-dependency',
                      ['sasquatch', 'sasquatch-v4be'])])
    res, path = _cls(work, skill, env, 'env-depsboth.json')
    _expect_pair(res, path, 'be', 'install-extractor-be', 'deps-both-names')


@case
def c_dep_gap_naming_neither_falls_through(work):
    rows = [_row('dep', handler='squashfs_*', gaps='missing-extractor-dependency+',
                 deps='sasquatch+', be='*', sr='*', files='*',
                 action='install-extractor-le')]
    skill = _write(work, 'sk-depnone.md', _skel(_block(rows)))
    env = _env(handler='squashfs_v4_be',
               gaps=[('missing-extractor-dependency', ['unsquashfs'])], files=1)
    res, path = _cls(work, skill, env, 'env-depnone.json')
    _expect_pair(res, path, 'unclassified', 'none', 'dep-gap-naming-neither')


@case
def c_mixed_v3_v4_failing_v3_is_legacy(work):
    """Mixed chunk set: the failing chunk decides, not the run-wide handler."""
    rows = [_row('avm', handler='squashfs_*', failing='squashfs_v4_be', gaps='extractor-failure+', deps='*',
                 be='no', sr='*', files='0', action='wrap-extractor-be'),
            _row('legacy', handler='squashfs_*', failing='squashfs_v[123]*', gaps='extractor-failure+',
                 deps='*', be='*', sr='*', files='0', action='cross-read-legacy'),
            _row('body', handler='squashfs_*', gaps='extractor-failure+', deps='*',
                 be='*', sr='*', files='0', action='preserve-failure')]
    skill = _write(work, 'sk-mix-v3fail.md', _skel(_block(rows)))
    env = _env(handler='squashfs_v4_be', handlers=('squashfs_v3',),
               gaps=[('extractor-failure', [])], be=False, files=0,
               gap_handlers={'extractor-failure': 'squashfs_v3'})
    res, path = _cls(work, skill, env, 'env-mix-v3fail.json')
    _expect_pair(res, path, 'legacy', 'cross-read-legacy', 'mixed-v3-failing-v3')


@case
def c_mixed_v3_v4_failing_v4be_is_avm(work):
    rows = [_row('avm', handler='squashfs_*', failing='squashfs_v4_be', gaps='extractor-failure+', deps='*',
                 be='no', sr='*', files='0', action='wrap-extractor-be'),
            _row('legacy', handler='squashfs_*', failing='squashfs_v[123]*', gaps='extractor-failure+',
                 deps='*', be='*', sr='*', files='0', action='cross-read-legacy'),
            _row('body', handler='squashfs_*', gaps='extractor-failure+', deps='*',
                 be='*', sr='*', files='0', action='preserve-failure')]
    skill = _write(work, 'sk-mix-v4fail.md', _skel(_block(rows)))
    env = _env(handler='squashfs_v4_be', handlers=('squashfs_v3',),
               gaps=[('extractor-failure', [])], be=False, files=0,
               gap_handlers={'extractor-failure': 'squashfs_v4_be'})
    res, path = _cls(work, skill, env, 'env-mix-v4fail.json')
    _expect_pair(res, path, 'avm', 'wrap-extractor-be', 'mixed-v3-failing-v4be')


@case
def c_mixed_no_failing_handler_uses_run_wide_set(work):
    """Documented boundary: no failing handler recorded -> HF = F, and order decides."""
    rows = [_row('avm', handler='squashfs_*', failing='squashfs_v4_be', gaps='extractor-failure+', deps='*',
                 be='no', sr='*', files='0', action='wrap-extractor-be'),
            _row('legacy', handler='squashfs_*', failing='squashfs_v[123]*', gaps='extractor-failure+',
                 deps='*', be='*', sr='*', files='0', action='cross-read-legacy')]
    skill = _write(work, 'sk-mix-nohf.md', _skel(_block(rows)))
    env = _env(handler='squashfs_v4_be', handlers=('squashfs_v3',),
               gaps=[('extractor-failure', [])], be=False, files=0)
    res, path = _cls(work, skill, env, 'env-mix-nohf.json')
    _expect_pair(res, path, 'avm', 'wrap-extractor-be', 'mixed-no-failing-handler')


@case
def c_two_failing_handlers_first_row_wins(work):
    """No draft clause names two failed chunks; HF holds both, so clause order decides."""
    rows = [_row('avm', handler='squashfs_*', failing='squashfs_v4_be', gaps='extractor-failure+', deps='*',
                 be='no', sr='*', files='0', action='wrap-extractor-be'),
            _row('legacy', handler='squashfs_*', failing='squashfs_v[123]*', gaps='extractor-failure+',
                 deps='*', be='*', sr='*', files='0', action='cross-read-legacy')]
    skill = _write(work, 'sk-twofail.md', _skel(_block(rows)))
    env = _env(handler='squashfs_v4_le', handlers=('squashfs_v4_be', 'squashfs_v3'),
               gaps=['extractor-failure'], be=False, files=0,
               gap_handlers={'extractor-failure': 'squashfs_v3'})
    env['normalized_result']['extraction_gaps'].append(
        {'kind': 'extractor-failure', 'dependencies': [], 'handler': 'squashfs_v4_be'})
    res, path = _cls(work, skill, env, 'env-twofail.json')
    _expect_pair(res, path, 'avm', 'wrap-extractor-be', 'two-failing-handlers-order')
    flipped = [_row('legacy', handler='squashfs_*', failing='squashfs_v[123]*', gaps='extractor-failure+',
                    deps='*', be='*', sr='*', files='0', action='cross-read-legacy')]
    flipped.append(rows[0])
    skill = _write(work, 'sk-twofail-rev.md', _skel(_block(flipped)))
    res, path = _cls(work, skill, env, 'env-twofail-rev.json')
    _expect_pair(res, path, 'legacy', 'cross-read-legacy', 'two-failing-handlers-flipped')


@case
def c_v4_broadcom_failure_is_body(work):
    """v4-Broadcom is a v4 handler but not the AVM marker population (step 5)."""
    rows = [_row('avm', handler='squashfs_*', failing='squashfs_v4_be', gaps='extractor-failure+', deps='*',
                 be='no', sr='*', files='0', action='wrap-extractor-be'),
            _row('legacy', handler='squashfs_*', failing='squashfs_v[123]*', gaps='extractor-failure+',
                 deps='*', be='*', sr='*', files='0', action='cross-read-legacy'),
            _row('body', handler='squashfs_*', gaps='extractor-failure+', deps='*',
                 be='*', sr='*', files='0', action='preserve-failure')]
    skill = _write(work, 'sk-bcbod.md', _skel(_block(rows)))
    env = _env(handler='squashfs_v4_broadcom', gaps=[('extractor-failure', [])],
               be=False, files=0,
               gap_handlers={'extractor-failure': 'squashfs_v4_broadcom'})
    res, path = _cls(work, skill, env, 'env-bcbod.json')
    _expect_pair(res, path, 'body', 'preserve-failure', 'v4-broadcom-body')


@case
def c_avm_be_yes_is_body(work):
    rows = [_row('avm', handler='squashfs_*', failing='squashfs_v4_be', gaps='extractor-failure+', deps='*',
                 be='no', sr='*', files='0', action='wrap-extractor-be'),
            _row('body', handler='squashfs_*', gaps='extractor-failure+', deps='*',
                 be='*', sr='*', files='0', action='preserve-failure')]
    skill = _write(work, 'sk-avmyes.md', _skel(_block(rows)))
    res, path = _cls(work, skill,
                     _env(handler='squashfs_v4_be', gaps=['extractor-failure'],
                          be=True, files=0), 'env-avmyes.json')
    _expect_pair(res, path, 'body', 'preserve-failure', 'avm-be-yes')


@case
def c_avm_be_na_is_body(work):
    """BE = n/a never satisfies step 5 (round-41 claims, features paragraph)."""
    rows = [_row('avm', handler='squashfs_*', failing='squashfs_v4_be', gaps='extractor-failure+', deps='*',
                 be='no', sr='*', files='0', action='wrap-extractor-be'),
            _row('body', handler='squashfs_*', gaps='extractor-failure+', deps='*',
                 be='*', sr='*', files='0', action='preserve-failure')]
    skill = _write(work, 'sk-avmna.md', _skel(_block(rows)))
    res, path = _cls(work, skill, _env(handler='squashfs_v4_be', gaps=['extractor-failure'],
                                       be=None, files=0), 'env-avmna.json')
    _expect_pair(res, path, 'body', 'preserve-failure', 'avm-be-na')


@case
def c_partial_precedes_avm(work):
    rows = [_row('partial', handler='squashfs_*', gaps='extractor-failure+', deps='*',
                 be='*', sr='*', files='>0', action='salvage-partial'),
            _row('avm', handler='squashfs_*', failing='squashfs_v4_be', gaps='extractor-failure+', deps='*',
                 be='no', sr='*', files='0', action='wrap-extractor-be')]
    skill = _write(work, 'sk-partavm.md', _skel(_block(rows)))
    res, path = _cls(work, skill, _env(handler='squashfs_v4_be',
                                       gaps=['extractor-failure'], be=False, files=2),
                     'env-partavm.json')
    _expect_pair(res, path, 'partial', 'salvage-partial', 'partial-precedes-avm')


# ------------------------------------------------------------------ v4: step boundaries

def _precedence_table():
    """The v4 table amendment A1 describes, one row per clause, in clause order."""
    return [
        _row('container-depth-limited', handler='none', gaps='depth-limited+', deps='*',
             be='*', sr='*', files='*', action='raise-depth'),
        _row('no-squashfs-chunk', handler='none', gaps='*', deps='*', be='*', sr='*',
             files='*', action='inspect-input'),
        _row('dep-missing-be', handler='squashfs_*',
             gaps='missing-extractor-dependency+', deps='sasquatch-v4be+', be='*',
             sr='*', files='*', action='install-extractor-be'),
        _row('dep-missing-le', handler='squashfs_*',
             gaps='missing-extractor-dependency+', deps='sasquatch+', be='*', sr='*',
             files='*', action='install-extractor-le'),
        _row('partial-body-failure', handler='squashfs_*', gaps='extractor-failure+',
             deps='*', be='*', sr='*', files='>0', action='salvage-partial'),
        _row('avm-marker-be-dropped', handler='squashfs_v4_be',
             gaps='extractor-failure+', deps='*', be='no', sr='*', files='0',
             action='wrap-extractor-be'),
        _row('legacy-body-failure', handler='squashfs_v[123]*',
             gaps='extractor-failure+', deps='*', be='*', sr='*', files='0',
             action='cross-read-legacy'),
        _row('body-extractor-failure', handler='squashfs_*',
             gaps='extractor-failure+', deps='*', be='*', sr='*', files='0',
             action='preserve-failure'),
        _row('unknown-residue', handler='squashfs_*', gaps='unknown-chunk-handler+',
             deps='*', be='*', sr='*', files='*', action='isolate-residue'),
        _row('depth-limited', handler='squashfs_*', gaps='depth-limited+', deps='*',
             be='*', sr='*', files='*', action='raise-depth'),
        _row('mixed-symlinks', handler='squashfs_*', gaps='unpublished-entry+', deps='*',
             be='*', sr='yes', files='*', action='audit-symlinks'),
        _row('escaping-symlink-removed', handler='squashfs_*', gaps='none', deps='*',
             be='*', sr='yes', files='*', action='expect-link-absent'),
        _row('in-tree-symlink-metadata', handler='squashfs_*', gaps='unpublished-entry',
             deps='*', be='*', sr='no', files='*', action='count-gap'),
        _row('clean', handler='squashfs_*', gaps='none', deps='*', be='*', sr='no',
             files='>0', action='none'),
        _row('clean-empty', handler='squashfs_*', gaps='none', deps='*', be='*', sr='no',
             files='0', action='confirm-empty'),
    ]


@case
def c_step1_domain(work):
    skill = _write(work, 'sk-step1.md', _skel(_block(_precedence_table())))
    checks = [
        ('step1-op', _env(handler='squashfs_v4_be', be=False, files=2,
                          op='inspect_firmware_regions'), 'unclassified', 'none'),
        ('step1-provider', _env(handler='squashfs_v4_be', be=False, files=2,
                                pv='binwalk'), 'unclassified', 'none'),
        ('step1-op-legacy', _env(handler='squashfs_v3', be=False, files=2,
                                 op='carve'), 'unclassified', 'none'),
    ]
    for name, env, want_label, want_action in checks:
        res, path = _cls(work, skill, env, 'env-%s.json' % name)
        _expect_pair(res, path, want_label, want_action, name)


@case
def c_step2_no_squashfs_chunk(work):
    skill = _write(work, 'sk-step2.md', _skel(_block(_precedence_table())))
    checks = [
        ('step2-bare', _env(handler=None, be=None, files=0), 'no-squashfs-chunk',
         'inspect-input'),
        ('step2-gzip', _env(handler='gzip', be=None, files=3), 'no-squashfs-chunk',
         'inspect-input'),
        ('step2-tar', _env(handler='tar', be=None, files=1), 'no-squashfs-chunk',
         'inspect-input'),
        ('step2-residue-no-depth', _env(handler=None, be=None, files=0,
                                        gaps=['unknown-chunk-handler']),
         'no-squashfs-chunk', 'inspect-input'),
    ]
    for name, env, want_label, want_action in checks:
        res, path = _cls(work, skill, env, 'env-%s.json' % name)
        _expect_pair(res, path, want_label, want_action, name)


@case
def c_step3_dependencies(work):
    skill = _write(work, 'sk-step3.md', _skel(_block(_precedence_table())))
    checks = [
        ('step3-be', _env(handler='squashfs_v4_be',
                          gaps=[('missing-extractor-dependency', ['sasquatch-v4be'])]),
         'dep-missing-be', 'install-extractor-be'),
        ('step3-be-superset', _env(handler='squashfs_v4_be',
                                   gaps=[('missing-extractor-dependency',
                                          ['sasquatch-v4be', 'unsquashfs'])]),
         'dep-missing-be', 'install-extractor-be'),
        ('step3-le', _env(handler='squashfs_v4_le',
                          gaps=[('missing-extractor-dependency', ['sasquatch'])]),
         'dep-missing-le', 'install-extractor-le'),
        ('step3-legacy-le', _env(handler='squashfs_v3',
                                 gaps=[('missing-extractor-dependency', ['sasquatch'])]),
         'dep-missing-le', 'install-extractor-le'),
        ('step3-both', _env(handler='squashfs_v4_be',
                            gaps=[('missing-extractor-dependency',
                                   ['sasquatch', 'sasquatch-v4be'])]),
         'dep-missing-be', 'install-extractor-be'),
        ('step3-dep-plus-failure', _env(handler='squashfs_v4_be',
                                        gaps=[('missing-extractor-dependency',
                                               ['sasquatch-v4be']),
                                              'extractor-failure'], files=3),
         'dep-missing-be', 'install-extractor-be'),
        ('step3-dep-plus-depth', _env(handler='squashfs_v4_le',
                                      gaps=[('missing-extractor-dependency',
                                             ['sasquatch']), 'depth-limited']),
         'dep-missing-le', 'install-extractor-le'),
    ]
    for name, env, want_label, want_action in checks:
        res, path = _cls(work, skill, env, 'env-%s.json' % name)
        _expect_pair(res, path, want_label, want_action, name)


@case
def c_step4_partial(work):
    skill = _write(work, 'sk-step4.md', _skel(_block(_precedence_table())))
    checks = [
        ('step4-single', _env(handler='squashfs_v4_be', gaps=['extractor-failure'],
                              be=False, files=1), 'partial-body-failure',
         'salvage-partial'),
        ('step4-legacy', _env(handler='squashfs_v3', gaps=['extractor-failure'],
                              be=False, files=2), 'partial-body-failure',
         'salvage-partial'),
        ('step4-mixed-gaps', _env(handler='squashfs_v4_le',
                                  gaps=['extractor-failure', 'depth-limited',
                                        'unpublished-entry'], be=False, sr=True,
                                  files=5), 'partial-body-failure', 'salvage-partial'),
        ('step4-nonzero-one', _env(handler='squashfs_v4_broadcom',
                                   gaps=['extractor-failure'], be=False, files=1),
         'partial-body-failure', 'salvage-partial'),
    ]
    for name, env, want_label, want_action in checks:
        res, path = _cls(work, skill, env, 'env-%s.json' % name)
        _expect_pair(res, path, want_label, want_action, name)


@case
def c_step5_avm(work):
    skill = _write(work, 'sk-step5.md', _skel(_block(_precedence_table())))
    checks = [
        ('step5-hf', _env(handler='squashfs_v4_be', gaps=['extractor-failure'],
                          be=False, files=0), 'avm-marker-be-dropped',
         'wrap-extractor-be'),
        ('step5-hf-explicit', _env(handler='squashfs_v4_be',
                                   gaps=[('extractor-failure', [])], be=False, files=0,
                                   gap_handlers={'extractor-failure': 'squashfs_v4_be'}),
         'avm-marker-be-dropped', 'wrap-extractor-be'),
        ('step5-extra-gaps', _env(handler='squashfs_v4_be',
                                  gaps=['extractor-failure', 'unpublished-entry'],
                                  be=False, files=0), 'avm-marker-be-dropped',
         'wrap-extractor-be'),
    ]
    for name, env, want_label, want_action in checks:
        res, path = _cls(work, skill, env, 'env-%s.json' % name)
        _expect_pair(res, path, want_label, want_action, name)


@case
def c_step6_legacy_body(work):
    skill = _write(work, 'sk-step6.md', _skel(_block(_precedence_table())))
    for handler in LEGACY_HANDLERS:
        env = _env(handler=handler, gaps=['extractor-failure'], be=False, files=0,
                   gap_handlers={'extractor-failure': handler})
        res, path = _cls(work, skill, env, 'env-step6-%s.json' % handler)
        _expect_pair(res, path, 'legacy-body-failure', 'cross-read-legacy',
                     'step6-%s' % handler)


@case
def c_step7_body(work):
    skill = _write(work, 'sk-step7.md', _skel(_block(_precedence_table())))
    checks = [
        ('step7-le', _env(handler='squashfs_v4_le', gaps=['extractor-failure'],
                          be=False, files=0), 'body-extractor-failure',
         'preserve-failure'),
        ('step7-broadcom', _env(handler='squashfs_v4_broadcom',
                                gaps=['extractor-failure'], be=False, files=0),
         'body-extractor-failure', 'preserve-failure'),
        ('step7-be-yes', _env(handler='squashfs_v4_be', gaps=['extractor-failure'],
                              be=True, files=0), 'body-extractor-failure',
         'preserve-failure'),
        ('step7-extra-gaps', _env(handler='squashfs_v4_le',
                                  gaps=['extractor-failure', 'depth-limited'],
                                  be=False, files=0), 'body-extractor-failure',
         'preserve-failure'),
    ]
    for name, env, want_label, want_action in checks:
        res, path = _cls(work, skill, env, 'env-%s.json' % name)
        _expect_pair(res, path, want_label, want_action, name)


@case
def c_step8_depth(work):
    skill = _write(work, 'sk-step8.md', _skel(_block(_precedence_table())))
    checks = [
        ('step8-single', _env(handler='squashfs_v4_be', gaps=['depth-limited'],
                              be=None, files=2), 'depth-limited', 'raise-depth'),
        ('step8-legacy', _env(handler='squashfs_v3', gaps=['depth-limited'], be=None,
                              files=4), 'depth-limited', 'raise-depth'),
        ('step8-plus-in-tree', _env(handler='squashfs_v4_be',
                                    gaps=['depth-limited', 'unpublished-entry'],
                                    be=False, files=3), 'depth-limited', 'raise-depth'),
        ('step8-plus-sr', _env(handler='squashfs_v4_be',
                               gaps=['depth-limited', 'unpublished-entry'],
                               be=False, sr=True, files=3), 'depth-limited',
         'raise-depth'),
    ]
    for name, env, want_label, want_action in checks:
        res, path = _cls(work, skill, env, 'env-%s.json' % name)
        _expect_pair(res, path, want_label, want_action, name)


@case
def c_step9_mixed_and_step10_escaping(work):
    skill = _write(work, 'sk-step9.md', _skel(_block(_precedence_table())))
    checks = [
        ('step9-mixed', _env(handler='squashfs_v4_be', gaps=['unpublished-entry'],
                             be=False, sr=True, files=2), 'mixed-symlinks',
         'audit-symlinks'),
        ('step9-legacy-mixed', _env(handler='squashfs_v3', gaps=['unpublished-entry'],
                                    be=False, sr=True, files=2), 'mixed-symlinks',
         'audit-symlinks'),
        ('step10-escaping', _env(handler='squashfs_v4_be', gaps=[], be=False, sr=True,
                                 files=2), 'escaping-symlink-removed',
         'expect-link-absent'),
        ('step10-legacy-escaping', _env(handler='squashfs_v3', gaps=[], be=False,
                                        sr=True, files=2),
         'escaping-symlink-removed', 'expect-link-absent'),
        ('step9-unknown-gap-not-escaping', _env(handler='squashfs_v4_be',
                                                gaps=['encrypted-chunk'], be=False,
                                                sr=True, files=2), 'unclassified',
         'none'),
    ]
    for name, env, want_label, want_action in checks:
        res, path = _cls(work, skill, env, 'env-%s.json' % name)
        _expect_pair(res, path, want_label, want_action, name)


@case
def c_step11_in_tree(work):
    skill = _write(work, 'sk-step11.md', _skel(_block(_precedence_table())))
    checks = [
        ('step11-single', _env(handler='squashfs_v4_be', gaps=['unpublished-entry'],
                               be=False, files=3), 'in-tree-symlink-metadata',
         'count-gap'),
        ('step11-legacy', _env(handler='squashfs_v3', gaps=['unpublished-entry'],
                               be=False, files=0), 'in-tree-symlink-metadata',
         'count-gap'),
        ('step11-two-kinds', _env(handler='squashfs_v4_be',
                                  gaps=['unpublished-entry', 'encrypted-chunk'],
                                  be=False, files=3), 'unclassified', 'none'),
    ]
    for name, env, want_label, want_action in checks:
        res, path = _cls(work, skill, env, 'env-%s.json' % name)
        _expect_pair(res, path, want_label, want_action, name)


@case
def c_step12_clean(work):
    skill = _write(work, 'sk-step12.md', _skel(_block(_precedence_table())))
    checks = [
        ('step12-clean', _env(handler='squashfs_v4_be', gaps=[], be=False, files=2),
         'clean', 'none'),
        ('step12-clean-legacy', _env(handler='squashfs_v3', gaps=[], be=False, files=2),
         'clean', 'none'),
        ('step12-empty', _env(handler='squashfs_v4_le', gaps=[], be=False, files=0),
         'clean-empty', 'confirm-empty'),
        ('step12-empty-legacy', _env(handler='squashfs_v1', gaps=[], be=False, files=0),
         'clean-empty', 'confirm-empty'),
        ('step12-files-absent', _env(handler='squashfs_v4_le', gaps=[], be=False,
                                     files_absent=True), 'clean-empty',
         'confirm-empty'),
    ]
    for name, env, want_label, want_action in checks:
        res, path = _cls(work, skill, env, 'env-%s.json' % name)
        _expect_pair(res, path, want_label, want_action, name)


@case
def c_step2_container_depth_limited(work):
    """A1 step 2: no SquashFS handler at this depth is not evidence of no image."""
    skill = _write(work, 'sk-container.md', _skel(_block(_precedence_table())))
    checks = [
        ('container-trx', _env(handler='trx_v1', be=None, files=0,
                               gaps=['depth-limited']), 'container-depth-limited',
         'raise-depth'),
        ('container-nongzip', _env(handler='gzip', be=None, files=1,
                                   gaps=['depth-limited']), 'container-depth-limited',
         'raise-depth'),
        ('container-no-chunks', _env(handler=None, be=None, files=0,
                                     gaps=['depth-limited', 'unknown-chunk-handler']),
         'container-depth-limited', 'raise-depth'),
        ('container-no-squashfs-not-depth', _env(handler='trx_v1', be=None, files=1),
         'no-squashfs-chunk', 'inspect-input'),
    ]
    for name, env, want_label, want_action in checks:
        res, path = _cls(work, skill, env, 'env-%s.json' % name)
        _expect_pair(res, path, want_label, want_action, name)


@case
def c_step9_unknown_residue(work):
    """A1 step 9: residue beside a SquashFS chunk, decided before depth-limited."""
    skill = _write(work, 'sk-residue.md', _skel(_block(_precedence_table())))
    checks = [
        ('residue-alone', _env(handler='squashfs_v4_le', be=False, files=3,
                               gaps=['unknown-chunk-handler']), 'unknown-residue',
         'isolate-residue'),
        ('residue-legacy', _env(handler='squashfs_v3', be=False, files=2,
                                gaps=['unknown-chunk-handler']), 'unknown-residue',
         'isolate-residue'),
        ('residue-beats-depth', _env(handler='squashfs_v4_le', be=False, files=2,
                                     gaps=['unknown-chunk-handler', 'depth-limited']),
         'unknown-residue', 'isolate-residue'),
        ('residue-after-partial', _env(handler='squashfs_v4_be',
                                       gaps=['extractor-failure',
                                             'unknown-chunk-handler'], be=False,
                                       files=2), 'partial-body-failure',
         'salvage-partial'),
        ('residue-after-body', _env(handler='squashfs_v4_le',
                                    gaps=['extractor-failure',
                                          'unknown-chunk-handler'], be=False, files=0),
         'body-extractor-failure', 'preserve-failure'),
        ('residue-with-links', _env(handler='squashfs_v4_le', be=False, sr=True,
                                    files=2, gaps=['unknown-chunk-handler',
                                                   'unpublished-entry']),
         'unknown-residue', 'isolate-residue'),
    ]
    for name, env, want_label, want_action in checks:
        res, path = _cls(work, skill, env, 'env-%s.json' % name)
        _expect_pair(res, path, want_label, want_action, name)


@case
def c_ctl10_without_container_and_residue_rows(work):
    """CTL-C2-10: dropping both A1 rows loses exactly the two new decisions."""
    rows = [row for row in _precedence_table()
            if row[0] not in ('container-depth-limited', 'unknown-residue')]
    skill = _write(work, 'sk-ctl10.md', _skel(_block(rows)))
    res, path = _cls(work, skill, _env(handler='trx_v1', be=None, files=0,
                                       gaps=['depth-limited']), 'env-ctl10a.json')
    _expect_pair(res, path, 'no-squashfs-chunk', 'inspect-input', 'ctl10-container')
    res, path = _cls(work, skill, _env(handler='squashfs_v4_le', be=False, files=3,
                                       gaps=['unknown-chunk-handler']),
                     'env-ctl10b.json')
    _expect_pair(res, path, 'unclassified', 'none', 'ctl10-residue')


@case
def c_failing_handler_column_separates_f_and_hf(work):
    """The two handler columns test different sets; that is the whole point of column 4."""
    rows = [_row('avm-by-hf', handler='squashfs_*', failing='squashfs_v4_be',
                 gaps='extractor-failure+', deps='*', be='no', sr='*', files='0',
                 action='wrap-extractor-be'),
            _row('by-f', handler='squashfs_v4_be', failing='*',
                 gaps='extractor-failure+', deps='*', be='no', sr='*', files='0',
                 action='preserve-failure')]
    skill = _write(work, 'sk-twocols.md', _skel(_block(rows)))
    env = _env(handler='squashfs_v4_be', handlers=('squashfs_v3',),
               gaps=['extractor-failure'], be=False, files=0,
               gap_handlers={'extractor-failure': 'squashfs_v3'})
    res, path = _cls(work, skill, env, 'env-twocols.json')
    _expect_pair(res, path, 'by-f', 'preserve-failure', 'columns-separate-f-and-hf')


@case
def c_failing_handler_star_matches_empty_hf(work):
    """``*`` is the only failing-handler cell that matches an empty HF."""
    rows = [_row('needs-hf', handler='none', failing='squashfs_v4_be', gaps='*',
                 deps='*', be='*', sr='*', files='*', action='inspect-input'),
            _row('any-hf', handler='none', failing='*', gaps='*', deps='*', be='*',
                 sr='*', files='*', action='preserve-failure')]
    skill = _write(work, 'sk-emptyhf.md', _skel(_block(rows)))
    res, path = _cls(work, skill, _env(handler='gzip', be=None, files=2),
                     'env-emptyhf.json')
    _expect_pair(res, path, 'any-hf', 'preserve-failure', 'star-matches-empty-hf')


@case
def c_twelve_column_table_refused(work):
    """The v3 header (no failing-handler column) is a malformed v4 table."""
    header = [h for h in HEADER if h != 'failing handler']
    rows = [['x'] + ['*'] * (len(header) - 1)]
    skill = _write(work, 'sk-12col.md', _skel(_block(rows, header=header)))
    res = _cli(['--skill', skill, '--table-only'])
    _exit_is(res, 2, 'twelve-column-table')
    _require('header' in res.stderr, 'twelve-column-table: %r' % res.stderr)


@case
def c_step13_unclassified(work):
    skill = _write(work, 'sk-step13.md', _skel(_block(_precedence_table())))
    checks = [
        ('step13-unknown-gap', _env(handler='squashfs_v4_be', gaps=['mystery-gap'],
                                    be=False, files=2), 'unclassified', 'none'),
        ('step13-dep-neither', _env(handler='squashfs_v4_be',
                                    gaps=[('missing-extractor-dependency',
                                           ['unsquashfs'])]), 'unclassified', 'none'),
        ('step13-encrypted', _env(handler='squashfs_v4_le', gaps=['encrypted-chunk'],
                                  be=False, files=1), 'unclassified', 'none'),
    ]
    for name, env, want_label, want_action in checks:
        res, path = _cls(work, skill, env, 'env-%s.json' % name)
        _expect_pair(res, path, want_label, want_action, name)


@case
def c_full_v4_precedence_shape(work):
    """The 13-row v4 table on the tuples the precedence names, in one pass."""
    skill = _write(work, 'sk-shape.md', _skel(_block(_precedence_table())))
    checks = [
        ('shape-clean', _env(handler='squashfs_v4_be', be=False, files=2),
         'clean', 'none'),
        ('shape-clean-empty', _env(handler='squashfs_v4_le', be=False, files=0),
         'clean-empty', 'confirm-empty'),
        ('shape-escape', _env(handler='squashfs_v4_be', be=False, files=2, sr=True),
         'escaping-symlink-removed', 'expect-link-absent'),
        ('shape-in-tree', _env(handler='squashfs_v4_be', gaps=['unpublished-entry'],
                               be=False, files=2), 'in-tree-symlink-metadata',
         'count-gap'),
        ('shape-mixed', _env(handler='squashfs_v4_be', gaps=['unpublished-entry'],
                             be=False, files=2, sr=True), 'mixed-symlinks',
         'audit-symlinks'),
        ('shape-depth', _env(handler='squashfs_v4_be', gaps=['depth-limited'], be=False,
                             files=2), 'depth-limited', 'raise-depth'),
        ('shape-dep-le', _env(handler='squashfs_v4_le',
                              gaps=[('missing-extractor-dependency', ['sasquatch'])]),
         'dep-missing-le', 'install-extractor-le'),
        ('shape-dep-be', _env(handler='squashfs_v4_be',
                              gaps=[('missing-extractor-dependency', ['sasquatch-v4be'])]),
         'dep-missing-be', 'install-extractor-be'),
        ('shape-avm', _env(handler='squashfs_v4_be', gaps=['extractor-failure'],
                           be=False, files=0), 'avm-marker-be-dropped',
         'wrap-extractor-be'),
        ('shape-legacy', _env(handler='squashfs_v3', gaps=['extractor-failure'],
                              be=False, files=0,
                              gap_handlers={'extractor-failure': 'squashfs_v3'}),
         'legacy-body-failure', 'cross-read-legacy'),
        ('shape-body', _env(handler='squashfs_v4_le', gaps=['extractor-failure'],
                            be=False, files=0), 'body-extractor-failure',
         'preserve-failure'),
        ('shape-partial', _env(handler='squashfs_v4_be', gaps=['extractor-failure'],
                               be=False, files=3), 'partial-body-failure',
         'salvage-partial'),
        ('shape-nochunk', _env(handler=None, be=None, files=0), 'no-squashfs-chunk',
         'inspect-input'),
        ('shape-nochunk-gzip', _env(handler='gzip', be=None, files=2),
         'no-squashfs-chunk', 'inspect-input'),
        ('shape-container', _env(handler='trx_v1', be=None, files=0,
                                 gaps=['depth-limited']), 'container-depth-limited',
         'raise-depth'),
        ('shape-residue', _env(handler='squashfs_v4_le', be=False, files=3,
                               gaps=['unknown-chunk-handler']), 'unknown-residue',
         'isolate-residue'),
        ('shape-legacy-clean', _env(handler='squashfs_v3', be=False, files=2),
         'clean', 'none'),
        ('shape-unknown-gap', _env(handler='squashfs_v4_be', gaps=['mystery-gap'],
                                   be=False, files=2), 'unclassified', 'none'),
        ('shape-domain', _env(handler='squashfs_v4_be', be=False, files=2,
                              op='inspect_firmware_regions'), 'unclassified', 'none'),
    ]
    for name, env, want_label, want_action in checks:
        res, path = _cls(work, skill, env, 'env-%s.json' % name)
        _expect_pair(res, path, want_label, want_action, name)


@case
def c_v3_handler_cell_left_at_v4_star(work):
    """CTL-C2-9: the same table with every handler cell at squashfs_v4_* loses legacy."""
    rows = _precedence_table()
    for row in rows:
        for column in (3, 4):
            if row[column] == 'squashfs_*':
                row[column] = 'squashfs_v4_*'
            elif row[column] == 'squashfs_v[123]*':
                row[column] = 'squashfs_v4_*'
    skill = _write(work, 'sk-ctl9.md', _skel(_block(rows)))
    res, path = _cls(work, skill, _env(handler='squashfs_v3', be=False, files=2),
                     'env-ctl9.json')
    _expect_pair(res, path, 'unclassified', 'none', 'ctl9-legacy-blind')


@case
def c_without_legacy_row(work):
    """CTL-C2-8: dropping the legacy row sends a legacy body failure to step 7."""
    rows = [row for row in _precedence_table()
            if row[0] != 'legacy-body-failure']
    skill = _write(work, 'sk-ctl8.md', _skel(_block(rows)))
    env = _env(handler='squashfs_v3', gaps=['extractor-failure'], be=False, files=0,
               gap_handlers={'extractor-failure': 'squashfs_v3'})
    res, path = _cls(work, skill, env, 'env-ctl8.json')
    _expect_pair(res, path, 'body-extractor-failure', 'preserve-failure', 'ctl8-no-legacy')


@case
def c_real_skill(work):
    """The real SKILL.md parses once the v4 block is integrated, refuses before that."""
    try:
        with open(DEFAULT_SKILL, 'r', encoding='utf-8') as handle:
            text = handle.read()
    except OSError as exc:
        raise AssertionError('real-skill: cannot read %s (%s)' % (DEFAULT_SKILL, exc))
    res = _cli(['--skill', DEFAULT_SKILL, '--table-only'])
    if MARKER in text:
        _exit_is(res, 0, 'real-skill-after-integration')
        _require('rules: ' in res.stdout, 'real-skill: no rule count (%r)'
                 % res.stdout[:200])
    else:
        _exit_is(res, 2, 'real-skill-before-integration')
        _require('v3' in res.stderr or 'v2' in res.stderr,
                 'real-skill: stderr names no marker version (%r)' % res.stderr)


def selftest():
    work = tempfile.mkdtemp(dir=os.environ.get('TMPDIR') or None,
                            prefix='sqfs-triage-v4-selftest.')
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


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog='sqfs-triage-v4.py',
        description='Label REA envelopes with the SKILL.md craft-section SquashFS triage '
                    'table v4 (label and action).')
    parser.add_argument('--skill', metavar='SKILL.md',
                        help='document holding the craft-section v4 triage table')
    parser.add_argument('--json', action='store_true',
                        help='print features, the matched rule and its action as JSON')
    parser.add_argument('--table-only', action='store_true',
                        help='validate the table and print the parsed rules and actions')
    parser.add_argument('--selftest', action='store_true',
                        help='run the isolated selftest')
    parser.add_argument('envelopes', nargs='*', metavar='ENVELOPE.json',
                        help='REA envelope (bare data object or full CLI envelope)')
    ns = parser.parse_args(argv)
    if ns.selftest:
        return selftest()
    try:
        return _run(ns)
    except (TableError, EnvelopeError, InvocationError) as exc:
        sys.stderr.write('sqfs-triage-v4: %s\n' % exc)
        return 2


if __name__ == '__main__':
    sys.exit(main())
