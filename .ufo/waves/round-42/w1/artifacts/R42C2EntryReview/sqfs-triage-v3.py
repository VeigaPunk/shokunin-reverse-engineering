#!/usr/bin/env python3
"""sqfs-triage-v3.py - executable SquashFS extract-firmware outcome triage, table v3.

Reads exactly two surfaces and nothing else:

  * a SKILL.md document, from which it takes the FIRST markdown table that follows a
    line containing the marker ``<!-- sqfs-triage-table v3 -->`` inside the
    ``## Queue-drain craft`` section (that heading line up to the next ``## `` heading),
    plus the closed action vocabulary declared by the line directly above that table
    (``<!-- sqfs-triage-actions: token ... -->``; blank lines between it and the table
    header are allowed, any other prose is not);
  * REA envelopes (rea-agents 6.5.0), recorded as either a bare ``data`` object or a
    full CLI envelope ``{ok, data, meta}``.

It prints one ``(label, action)`` pair per envelope.  It never invokes REA, unblob or
sasquatch, never reads a carrier, and never writes anything.

What v3 changes against v2 (round-40 defect R40-CL5)
----------------------------------------------------
1. Marker ``<!-- sqfs-triage-table v3 -->``.  A document whose craft section carries a
   ``v2`` marker (or only a ``v1`` marker) is REFUSED with exit 2: a superseded table is
   never silently evaluated by this interpreter.  The v3 marker wins when both a v3
   marker and an older block are present, because only a v3 marker claims a v3 table;
   SKILL.md keeps its v1/v2 blocks as history above and below the live block.
2. The ``gap kinds`` cell gains a CONTAINS form beside the v2 exact-set form:

     ``none``            the gap-kind set is empty
     ``*``               any gap-kind set, including the empty one
     ``a``               the gap-kind set is exactly {a}          (v2 exact)
     ``a+b``             the gap-kind set is exactly {a, b}       (v2 exact)
     ``a+``              the gap-kind set contains a   (others allowed)  [new]
     ``a,b+``            the gap-kind set contains a and b (others allowed)  [new]

   The contains form is what makes COMBINED outcomes labelable: a partial failure that
   also kept in-tree symlinks, a depth-limited carve that also reports symlink gaps, and
   a missing-extractor-dependency envelope that carries further gaps.  The exact form
   and the contains form differ on a superset envelope by design, so a table can say
   "exactly this" where the fact is exclusive and "at least this" where it is not.
   The separator follows the form: ``+`` joins an exact set, ``,`` joins a contains set,
   and a comma inside an exact cell is a malformed member, never an alternate syntax.
   ``none`` and ``*`` are reserved words in both forms and cannot appear as members, so
   ``none+`` and ``a+none`` are refused instead of naming a gap kind that cannot exist.
   Only the ``gap kinds`` column has the contains form; ``dependencies`` keeps the v2
   exact form, because no precedence rule in the round-41 claims needs otherwise.
3. NO table is embedded in this file.  The v2 ``TABLE_BLOCK`` plus ``--print-table``
   went stale against the documents it was supposed to describe (R40-CL5 M1: the
   embedded copy and the SKILL block disagreed), so the only table surface is a
   document read through ``--skill``.  The selftest builds its tables inline.

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
  gap kinds          ``*``, ``none``, exact ``a`` / ``a+b``, or contains ``a+`` /
                     ``a,b+`` as above, over ``extraction_gaps[].kind``.
  dependencies       ``*``, ``none``, or ``a+b`` meaning the set of
                     ``extraction_gaps[].dependencies`` values equals exactly {a, b};
                     a single name means exactly that singleton.
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

Features (from the envelope) - identical to v2
---------------------------------------------
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
  python3 -I -B sqfs-triage-v3.py --skill SKILL.md ENVELOPE.json...
      one ``path<TAB>label<TAB>action`` line per envelope
  python3 -I -B sqfs-triage-v3.py --skill SKILL.md --json ENVELOPE...
      features, matched row index and row cells per envelope
  python3 -I -B sqfs-triage-v3.py --skill SKILL.md --table-only
      validate the table, print the parsed rules and the action vocabulary
  python3 -I -B sqfs-triage-v3.py --selftest
      isolated selftest (temporary SKILL variants and envelopes under $TMPDIR)

Exit codes: 0 ok, 2 table missing, refused (v1/v2 marker), or malformed (wrong header,
malformed cell, duplicate label, unknown action, missing or misplaced vocabulary line) or
envelope unreadable, 1 only for a failed ``--selftest``.

Limits
------
* Cell text is split on ``|``; a literal pipe inside a cell is not supported.
* Header names are compared case-insensitively (the v1 interpreter's rule); every other
  cell is compared exactly and case-sensitively, and handler patterns are matched with
  ``fnmatch.fnmatchcase``.
* ``gap kinds`` and ``dependencies`` compare as sets: order and repetition in the
  envelope are erased.  An exact cell ignores an envelope carrying one extra gap kind; a
  contains cell tolerates extras.  Neither kind can express "every gap kind except x".
* One label may own exactly ONE row (duplicate labels are refused).  A label whose
  condition genuinely needs two disjoint condition sets therefore cannot be written; the
  round-41 draft table records the two feature tuples where that bites (a non-v4 squashfs
  handler, and a dependency gap naming both sasquatch binaries) instead of widening a
  row to ``*``.
* A handler cell is a positive match: no cell can say "no handler matching a pattern",
  which is the same reason the non-v4 handler tuple above cannot be labelled.
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

MARKER = '<!-- sqfs-triage-table v3 -->'
REFUSED_MARKERS = ('<!-- sqfs-triage-table v2 -->', '<!-- sqfs-triage-table v1 -->')
ACTIONS_PREFIX = '<!-- sqfs-triage-actions:'
ACTIONS_SUFFIX = '-->'
CRAFT_PREFIX = 'queue-drain craft'
HEADER = ['label', 'operation', 'provider', 'handler', 'gap kinds', 'dependencies',
          '-be in child argv', 'symlink removed', 'published files', 'action', 'cause',
          'source']
BE_VALUES = ('yes', 'no', 'n/a')
FILES_VALUES = ('0', '>0')
RESERVED_MEMBERS = ('none', '*')
SYMLINK_TYPENAME = 'MaliciousSymlinkRemoved'
DEFAULT_LABEL = 'unclassified'
DEFAULT_ACTION = 'none'
OPERATION_TOKEN = 'extract_firmware'

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

    ``contains=False`` keeps the v2 grammar (``*``, ``none``, ``a``, ``a+b``).
    ``contains=True`` adds the v3 contains form (``a+``, ``a,b+``).
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
            'gap_kinds': _parse_set_cell(gap, 'gap kinds', contains=True),
            'dependencies': _parse_set_cell(dep, 'dependencies', contains=False),
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
    """Return (rules, info) for the craft-section v3 triage table of one SKILL.md.

    The v3 marker selects its own table, so a retained v1/v2 block in the same section is
    history.  Without a v3 marker the document is REFUSED (never silently triaged by a
    superseded table): the error names the marker version it found.
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
                                     'never evaluated as v3)'
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
# envelope features (identical to v2)
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
    if kind == 'contains':
        return payload <= frozenset(values)
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


def _spec_text(spec):
    kind, payload = spec
    if kind in ('any', 'none'):
        return kind
    return '%s{%s}' % (kind, ','.join(sorted(payload)))


def _print_rules(skill, rules, info):
    print('skill: %s' % skill)
    print('marker line: %d  actions line: %d  table line: %d  rules: %d'
          % (info['marker_line'], info['actions_line'], info['table_line'],
             info['rules']))
    print('actions: %s' % ' '.join(info['actions']))
    for rule in rules:
        print('%d. %s' % (rule['index'], rule['label']))
        print('   operation=%r provider=%r handler=%r gap_kinds=%s dependencies=%s'
              % (rule['operation'], rule['provider'], rule['handler'],
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

VOCAB = 'none inspect-input install-extractor-be install-extractor-le wrap-extractor-be preserve-failure salvage-partial audit-symlinks expect-link-absent count-gap confirm-empty raise-depth'

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


def _row(label, operation='extract_firmware', provider='unblob', handler='*', gaps='*',
         deps='*', be='*', sr='*', files='*', action='none',
         cause='cause -> action', source='selftest'):
    return [label, operation, provider, handler, gaps, deps, be, sr, files, action,
            cause, source]


def _env(handler=None, gaps=(), be=None, sr=False, files=0, op='extract_firmware',
         pv='unblob', command=None):
    """Build one synthetic REA ``data`` object with exactly these features.

    ``gaps`` items are a kind string or a ``(kind, [dependencies])`` tuple; ``be`` is
    None for no sasquatch command (feature ``n/a``), True for a ``-be`` argv token, False
    for a sasquatch command without it.  ``command`` overrides the recorded command.
    """
    chunks = [] if handler is None else [{'handler': handler}]
    gaps_out = []
    for gap in gaps:
        if isinstance(gap, tuple):
            gaps_out.append({'kind': gap[0], 'dependencies': list(gap[1])})
        else:
            gaps_out.append({'kind': gap, 'dependencies': []})
    diagnostics = []
    if command is not None:
        diagnostics.append({'report': {'command': command}})
    elif be is not None:
        argv = ['/usr/local/bin/sasquatch-v4be']
        if be:
            argv.append('-be')
        argv.extend(['-d', '/out', '/in'])
        diagnostics.append({'report': {'command': argv}})
    data = {'operation': op,
            'provider': {'id': pv, 'name': pv, 'version': '0.0'},
            'normalized_result': {'chunks': chunks,
                                  'extraction_gaps': gaps_out,
                                  'diagnostics': diagnostics,
                                  'files': [{'relative_path': 'f/%d.bin' % n, 'size': 1}
                                            for n in range(files)]}}
    if sr:
        data['raw_result'] = {'report': [{'reports': [{'__typename__':
                                                       SYMLINK_TYPENAME}]}]}
    return data


def _cls(work, skill, env, name, extra=()):
    path = _dump(work, name, env)
    return _cli(['--skill', skill, *extra, path]), path


def _two(target, fallback_action='inspect-input'):
    return [target, _row('fallback', handler='*', gaps='*', deps='*', be='*', sr='*',
                         files='*', action=fallback_action)]


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
def c_deps_cell_has_no_contains_form(work):
    rows = [_row('x', handler='squashfs_v4_be', gaps='none', deps='sasquatch+',
                 be='*', sr='no', files='>0', action='none')]
    skill = _write(work, 'sk-depsplus.md', _skel(_block(rows)))
    res = _cli(['--skill', skill, _dump(work, 'env-depsplus.json',
                                        _env(handler='squashfs_v4_be', be=False, files=1))])
    _exit_is(res, 2, 'deps-cell-no-contains')
    _require('dependencies' in res.stderr,
             'deps-cell-no-contains: stderr does not name the column (%r)'
             % res.stderr)


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
    rows = [_row('a', gaps='extractor-failure,unpublished-entry+'),
            _row('b', gaps='extractor-failure+unpublished-entry', deps='sasquatch')]
    skill = _write(work, 'sk-specs.md', _skel(_block(rows)))
    res = _cli(['--skill', skill, '--table-only'])
    _exit_is(res, 0, 'table-only-specs')
    _require('contains{extractor-failure,unpublished-entry}' in res.stdout,
             'table-only-specs: contains spec not printed (%r)' % res.stdout)
    _require('exact{extractor-failure,unpublished-entry}' in res.stdout,
             'table-only-specs: exact spec not printed')
    _require('rules: 2' in res.stdout, 'table-only-specs: rule count missing')


# ------------------------------------------------------------------ grammar: markers

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
def c_v3_marker_selects_its_table_over_earlier_v2_block(work):
    stale = _block([_row('stale', action='inspect-input')],
                   marker='<!-- sqfs-triage-table v2 -->')
    live_rows = [_row('live', handler='squashfs_v4_*', gaps='none', deps='none',
                      be='*', sr='no', files='>0', action='confirm-empty')]
    live = _block(live_rows)
    text = ('# SKILL\n\n## Queue-drain craft\n\nHistory:\n\n' + stale
            + '\nLive table:\n\n' + live + '\n## A later section\n')
    skill = _write(work, 'sk-both.md', text)
    res, path = _cls(work, skill, _env(handler='squashfs_v4_be', be=False, files=1),
                     'env-both.json')
    _expect_pair(res, path, 'live', 'confirm-empty', 'v3-marker-wins')


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
                   _skel(_block([_row('avm', handler='squashfs_v4_be',
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
def c_sr_from_raw_result(work):
    skill = _write(work, 'sk-srraw.md',
                   _skel(_block([_row('esc', handler='squashfs_v4_*', gaps='none',
                                      deps='none', be='*', sr='yes', files='*',
                                      action='expect-link-absent')])))
    res, path = _cls(work, skill, _env(handler='squashfs_v4_be', be=False, files=1,
                                       sr=True), 'env-srraw.json')
    _expect_pair(res, path, 'esc', 'expect-link-absent', 'sr-from-raw-result')


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
    for key in ('OP', 'PV', 'H', 'G', 'D', 'BE', 'SR', 'P'):
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
                 deps='sasquatch', be='*', sr='*', files='*',
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


@case
def c_full_precedence_shape(work):
    """A twelve-row table shaped like the round-41 draft: order decides all combined sets."""
    rows = [
        _row('no-squashfs-chunk', handler='none', gaps='*', deps='*', be='*', sr='*',
             files='*', action='inspect-input'),
        _row('dep-missing-be', handler='squashfs_v4_*', gaps='missing-extractor-dependency+',
             deps='sasquatch-v4be', be='*', sr='*', files='*',
             action='install-extractor-be'),
        _row('dep-missing-le', handler='squashfs_v4_*', gaps='missing-extractor-dependency+',
             deps='sasquatch', be='*', sr='*', files='*', action='install-extractor-le'),
        _row('partial-body-failure', handler='squashfs_v4_*', gaps='extractor-failure+',
             deps='*', be='*', sr='*', files='>0', action='salvage-partial'),
        _row('avm-marker-be-dropped', handler='squashfs_v4_be', gaps='extractor-failure+',
             deps='*', be='no', sr='*', files='0', action='wrap-extractor-be'),
        _row('body-extractor-failure', handler='squashfs_v4_*', gaps='extractor-failure+',
             deps='*', be='*', sr='*', files='0', action='preserve-failure'),
        _row('depth-limited', handler='squashfs_v4_*', gaps='depth-limited+',
             deps='*', be='*', sr='*', files='*', action='raise-depth'),
        _row('mixed-symlinks', handler='squashfs_v4_*', gaps='unpublished-entry+', deps='*',
             be='*', sr='yes', files='*', action='audit-symlinks'),
        _row('escaping-symlink-removed', handler='squashfs_v4_*', gaps='none', deps='none',
             be='*', sr='yes', files='*', action='expect-link-absent'),
        _row('in-tree-symlink-metadata', handler='squashfs_v4_*', gaps='unpublished-entry',
             deps='none', be='*', sr='no', files='*', action='count-gap'),
        _row('clean', handler='squashfs_v4_*', gaps='none', deps='none', be='*', sr='no',
             files='>0', action='none'),
        _row('clean-empty', handler='squashfs_v4_*', gaps='none', deps='none', be='*',
             sr='no', files='0', action='confirm-empty'),
    ]
    skill = _write(work, 'sk-shape.md', _skel(_block(rows)))
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
        ('shape-dep-le', _env(handler='squashfs_v4_le',
                              gaps=[('missing-extractor-dependency', ['sasquatch'])]),
         'dep-missing-le', 'install-extractor-le'),
        ('shape-dep-be', _env(handler='squashfs_v4_be',
                              gaps=[('missing-extractor-dependency', ['sasquatch-v4be'])]),
         'dep-missing-be', 'install-extractor-be'),
        ('shape-avm', _env(handler='squashfs_v4_be', gaps=['extractor-failure'],
                           be=False, files=0), 'avm-marker-be-dropped',
         'wrap-extractor-be'),
        ('shape-body', _env(handler='squashfs_v4_le', gaps=['extractor-failure'],
                            be=False, files=0), 'body-extractor-failure',
         'preserve-failure'),
        ('shape-partial', _env(handler='squashfs_v4_be', gaps=['extractor-failure'],
                               be=False, files=3), 'partial-body-failure',
         'salvage-partial'),
        ('shape-depth', _env(handler='squashfs_v4_be', gaps=['depth-limited'], be=False,
                             files=2), 'depth-limited', 'raise-depth'),
        ('shape-nochunk', _env(handler=None, be=None, files=0), 'no-squashfs-chunk',
         'inspect-input'),
        ('shape-unknown-gap', _env(handler='squashfs_v4_be', gaps=['mystery-gap'],
                                   be=False, files=2), 'unclassified', 'none'),
        ('shape-domain', _env(handler='squashfs_v4_be', be=False, files=2,
                              op='inspect_firmware_regions'), 'unclassified', 'none'),
    ]
    for name, env, want_label, want_action in checks:
        res, path = _cls(work, skill, env, 'env-%s.json' % name)
        _expect_pair(res, path, want_label, want_action, name)


@case
def c_real_skill(work):
    """The real SKILL.md parses once the v3 block is integrated, refuses before that."""
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
        _require('v2' in res.stderr or 'v3' in res.stderr,
                 'real-skill: stderr names no marker version (%r)' % res.stderr)


def selftest():
    work = tempfile.mkdtemp(dir=os.environ.get('TMPDIR') or None,
                            prefix='sqfs-triage-v3-selftest.')
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
        prog='sqfs-triage-v3.py',
        description='Label REA envelopes with the SKILL.md craft-section SquashFS triage '
                    'table v3 (label and action).')
    parser.add_argument('--skill', metavar='SKILL.md',
                        help='document holding the craft-section v3 triage table')
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
        sys.stderr.write('sqfs-triage-v3: %s\n' % exc)
        return 2


if __name__ == '__main__':
    sys.exit(main())
