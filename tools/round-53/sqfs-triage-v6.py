#!/usr/bin/env python
"""sqfs-triage-v6.py - executable SquashFS extract-firmware outcome triage, table v6.

R53-C1 scoring instrument (round 53, fresh-start round).  It is a port of
``tools/round-50-c3/sqfs-triage-v5.py`` (R50-C3) with the v6 changes the round-53
claims file declares, plus one host-portability fix.  It reads exactly these
surfaces and nothing else:

  * a SKILL.md document, taken from git at a named revision
    (``git -C <root> show <rev>:SKILL.md``, read-only), from which it parses the
    FIRST markdown table that follows the marker ``<!-- sqfs-triage-table v6 -->``.
    A document whose newest triage marker is v1-v5 is REFUSED (exit 2): a
    superseded table is never silently evaluated.
  * the frozen fixture-level reader census ``tools/round-53/reader-census.json``,
    read from git at the FREEZE revision (never from a worktree);
  * a directory of REA envelopes (rea-agents 6.5.0), each either a bare ``data``
    object or a full CLI envelope ``{ok, data, meta}``;
  * the round-53 claims file at the FREEZE revision, only to bind the claim's
    SOURCES row (``claim_row``) to the landing entry's ``source:`` citation.

It never invokes REA, unblob or sasquatch, never reads a carrier, never writes into
the lane tree, and never touches a network.

PREDICATE (copied verbatim from ``plans/round-53-claims.md``, section R53-C1, so the
instrument and the claim cannot drift; the same sentence is written into every JSON
receipt under the key ``predicate``):

  at a REV descending from the R53 freeze, with every frozen path unchanged, running
  `python -X utf8 -I -B tools/round-53/sqfs-triage-v6.py --root <LANE> --rev <REV>
  --freeze <FREEZE> --envelopes <DIR> --json-out <OUT>` exits 0 with
  `pair_mismatches 0`, `evaluator_missing 0`, `executability_violations 0`,
  `clean_residue 0`, and a green selftest; and at the declared base the frozen
  witness command `python -X utf8 -I -B tools/round-53/v5-baseline-witness.py
  --root <LANE> --rev 6697518f0ad8e8399567ae4c9cd0207fc7c04d8b --freeze <FREEZE>
  --envelopes <DIR> --json-out <OUT2>` exits 1 with `executability_violations 1`
  naming `dmg_Z3_v3ddwrt_inode_table` and `clean_residue 7` naming the seven
  no-reader `clean` envelopes.

WHAT v6 CHANGES AGAINST v5 (the depth this instrument scores)
-------------------------------------------------------------
Round 50's falsify wave (``.ufo/waves/round-50/w3/ExecTriageV5.md`` F10) measured the
reader boundary as FIXTURE-level while the v5 rule is FAMILY-level: ddwrt is routed
reader-backed while six of its seven census fixtures have no reader at all, so the
FAILED body ``dmg_Z3_v3ddwrt_inode_table`` is prescribed a cross-read its readers
refuse, and no-reader-fixture ``clean`` envelopes keep the oracle-backed ``clean``
label with no oracle.  The routed findings (CritTriV6 F1-F7, MutTriV6 F1-F4) resolve
as the round-53 claims file declares:

  1  a new row ``legacy-body-refused`` -> ``preserve-unresolved``, keyed on the
     FIXTURE-level census: a FAILED body (``extractor-failure+``, 0 published) whose
     subject resolves NO-READER in the frozen census is refused, never prescribed a
     cross-read.  It sits ABOVE ``legacy-body-failure`` and duplicates
     ``no-reader-failure``'s action under a census trigger - declared, not
     accidental (CritTriV6 F4).
  2  ``legacy-body-failure`` narrows to fixtures the census does NOT mark NO-READER
     (cell ``partial,readable``): a synthetic reader-backed ddwrt FAILED body still
     routes ``cross-read-legacy`` - the family-key discriminator (MutTriV6 F2).
  3  the census-conditioned ``clean`` ground: a no-reader-fixture ``clean`` run
     routes ``record-unverified`` under the new label ``clean-unverified-fixture``
     (the family row keeps the v5 label ``clean-unverified`` byte-stable for the
     three no-reader families; the grammar refuses duplicate labels); the ``clean``
     row itself narrows to ``partial,readable``.
  4  first-match precedence: the census-conditioned rows decide before the family
     rows; the evaluator implements the identical precedence as an independent code
     path over the same frozen census.
  5  the executability audit: every envelope whose prescribed action is
     ``cross-read-legacy`` while its census status is NO-READER counts a violation;
     every ``clean``-labelled envelope whose census status is NO-READER counts as
     clean residue.  The predicate requires 0/0 at the landing.

THE EVALUATOR (independent of any table; census-aware)
------------------------------------------------------
The evaluator is written from the claim's precedence text, NOT from the table.  The
declared tuple is the envelope's own record (v5's OP/PV/H/F/HF/G/D/BE/SR/P) plus
SUBJ, the envelope's ``data.subject.digest.sha256`` when present.  The census status
of an envelope resolves as (declared in reader-census.json ``resolution_rule``):

  fixture  the census row whose ``sha256_12`` equals SUBJ's first 12 chars;
  lineage  the ``derived_lineage`` row whose ``carrier_sha256_12`` equals it (the
           parent's status; dmg_Z3's carrier is a derived ddwrt body whose parent
           fixture the census marks NO-READER);
  family   fallback on the envelope's own squashfs handler names: NO-READER families
           {v2_nonstandard, v3_broadcom, v3_nonstandard} -> no-reader; reader-backed
           {v1, v2, v3, v3_ddwrt} -> readable; else unknown.

Precedence (first match wins), which the v6 table must reproduce row for row:

   1  OP != extract_firmware or PV != unblob        -> unclassified / none
   2  F empty and depth-limited in G                 -> container-depth-limited / raise-depth
   3  F empty                                       -> no-squashfs-chunk / inspect-input
   4  missing-extractor-dependency in G: D holds sasquatch-v4be -> dep-missing-be /
      install-extractor-be; else D holds sasquatch -> dep-missing-le / install-extractor-le
   5  extractor-failure in G and P > 0              -> partial-body-failure / salvage-partial
   6  extractor-failure in G, P = 0, BE = no and squashfs_v4_be in HF
                                                     -> avm-marker-be-dropped / wrap-extractor-be
   6.5 extractor-failure in G, P = 0, census(hf) = no-reader
                                                     -> legacy-body-refused / preserve-unresolved   [v6]
   7  extractor-failure in G, P = 0, HF meets the reader-backed v1-v3 families and
      census(hf) != no-reader                       -> legacy-body-failure / cross-read-legacy
   8  extractor-failure in G, P = 0, HF meets a NO-READER family and census(hf) != no-reader
                                                     -> no-reader-failure / preserve-unresolved
   9  extractor-failure in G and P = 0              -> body-extractor-failure / preserve-failure
  10  unknown-chunk-handler in G                    -> unknown-residue / isolate-residue
  11  depth-limited in G                            -> depth-limited / raise-depth
  12  SR = yes and unpublished-entry in G           -> mixed-symlinks / audit-symlinks
  13  SR = yes and G empty                          -> escaping-symlink-removed / expect-link-absent
  14  G = {unpublished-entry}                       -> in-tree-symlink-metadata / count-gap
  15  G empty, P > 0: HF/F meets a NO-READER family -> clean-unverified / record-unverified
      else census(f) = no-reader                    -> clean-unverified-fixture /
                                                       record-unverified                [v6]
      else                                          -> clean / none
  16  G empty, P = 0                                -> clean-empty / confirm-empty
  17  anything else                                 -> unclassified / none

  The fixture-level catch carries its own label ``clean-unverified-fixture`` (same
  action) because the table grammar refuses duplicate labels; the v5 family labels
  stay byte-stable.  The declared corpus effect is unchanged: the same eight label
  moves (dmg_Z3 plus the seven no-reader-fixture ``clean`` envelopes), the action
  column moves exactly as the claims text declares.

A census status is one of the closed set {no-reader, partial, readable, unknown};
unknown can occur only when the envelope names no squashfs handler at all, and every
branch that consults the census is already guarded by an HF/F family test, so the
table's census cells (`*`, or a comma-list over {no-reader, partial, readable}) make
the table and the evaluator agree on every input, not only on the corpus.

LIMITS (stated, not hidden)
---------------------------
(a) The census covers the round-42 recon families only; carriers outside it resolve
by family fallback (the v5 behaviour), so v6 changes nothing for them.  (b) The
scored corpus is the frozen round-42 recon set (126 envelopes) - depth over the
scored corpus, not held-out generalization; the same disclosed limit as R50-C3.
(c) No reader was rerun: this host has neither reader installed, every census row
stays lineage-bound to the committed round-50 receipt, and the declared kill rule (a
recapture that contradicts the lineage) never fired.  (d) The corpus holds no
reader-backed ddwrt FAILED body, so change (2) is corpus-vacuous by design and is
witnessed by the selftest's synthetic fixture instead (declared).

HOST PORTABILITY FIX (the one code-level delta that changes no verdict)
-----------------------------------------------------------------------
The v5 instrument reads ``git show`` through ``subprocess.run(..., text=True)``,
which on Windows decodes the pipe with the ANSI codepage (cp1252 on this host) and
dies on SKILL.md's UTF-8 multibyte bytes with ``UnicodeDecodeError: 'charmap' codec
can't decode byte 0x9d`` (measured 2026-10-31, receipt
``.ufo/waves/round-53/l1/host-probes/``).  v6 passes ``encoding='utf-8'`` on every
subprocess and file read, so the same command runs on POSIX and Windows both.  The
frozen v5 instrument stays byte-identical and refuses honestly (exit 2) here.

MUTATION BATTERY (the selftest's committed mutation list)
---------------------------------------------------------
The mutations are textual edits of the embedded v6 draft table, re-parsed by the v6
parser and scored against the FIXED census-aware evaluator over the selftest fixture
set (which carries a synthetic census).  The selftest asserts, for every mutation,
that the set of flipped fixture pairs is exactly the expected set - a mutation may
not be a no-op and may not cross-flip a pair it does not own.

Usage
-----
  python -X utf8 -I -B sqfs-triage-v6.py --root LANE --rev REV --freeze FREEZE
      --envelopes DIR --json-out PATH
      label every envelope of DIR with the v6 table at REV and with the fixed
      census-aware evaluator, audit the labels, write the JSON report to PATH
  python -X utf8 -I -B sqfs-triage-v6.py --selftest [--work DIR]
      offline selftest (fixtures under --work, else the dir given); never touches
      the lane
  python -X utf8 -I -B sqfs-triage-v6.py --controls --root LANE --envelopes DIR
      --json-out PATH
      score every committed mutant table against the fixed evaluator on the real
      corpus and on the selftest fixtures
  python -X utf8 -I -B sqfs-triage-v6.py --print-v6-block
      print the embedded v6 table draft (the block the L1 lands in SKILL.md)
  python -X utf8 -I -B sqfs-triage-v6.py --skill PATH ... 
      read the SKILL.md from a FILE instead of from git (pre-landing measurement)

Exit codes: 0 met (every pair equal, no evaluator abstention, audit 0/0, sources
binding green when --freeze is given); 1 not met; 2 could-not-evaluate (unknown
revision, missing or malformed table or census, unreadable envelope, freeze not an
ancestor, refused work or output directory).
"""

import argparse
import fnmatch
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile

MARKER_V6 = '<!-- sqfs-triage-table v6 -->'
SUPERSEDED_MARKERS = ('<!-- sqfs-triage-table v5 -->',
                      '<!-- sqfs-triage-table v4 -->',
                      '<!-- sqfs-triage-table v3 -->',
                      '<!-- sqfs-triage-table v2 -->',
                      '<!-- sqfs-triage-table v1 -->')
ACTIONS_PREFIX = '<!-- sqfs-triage-actions:'
ACTIONS_SUFFIX = '-->'
HEADER = ['label', 'operation', 'provider', 'handler', 'failing handler', 'gap kinds',
          'dependencies', '-be in child argv', 'symlink removed', 'census',
          'published files', 'action', 'cause', 'source']
CENSUS_VALUES = ('no-reader', 'partial', 'readable')
BE_VALUES = ('yes', 'no', 'n/a')
FILES_VALUES = ('0', '>0')
RESERVED_MEMBERS = ('none', '*')
SYMLINK_TYPENAME = 'MaliciousSymlinkRemoved'
DEFAULT_LABEL = 'unclassified'
DEFAULT_ACTION = 'none'
OPERATION_TOKEN = 'extract_firmware'
SQUASHFS_PREFIX = 'squashfs'
FAILURE_KIND = 'extractor-failure'

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

NO_READER_FAMILIES = (
    'squashfs_v2_nonstandard',
    'squashfs_v3_broadcom',
    'squashfs_v3_nonstandard',
)

READER_BACKED_V1V3 = (
    'squashfs_v1',
    'squashfs_v2',
    'squashfs_v3',
    'squashfs_v3_ddwrt',
)

CENSUS_RELPATH = 'tools/round-53/reader-census.json'
CLAIMS_RELPATH = 'plans/round-53-claims.md'
CLAIM_ROW_RE = re.compile(r'claim_row:\s*(S[0-9]{3,})')
ENTRY_RE = re.compile(r'entry:\s*(corpus/knowledge/[A-Za-z0-9._\-]+\.md)')

PREDICATE = (
    'at a REV descending from the R53 freeze, with every frozen path unchanged, '
    'running `python -X utf8 -I -B tools/round-53/sqfs-triage-v6.py --root <LANE> '
    '--rev <REV> --freeze <FREEZE> --envelopes <DIR> --json-out <OUT>` exits 0 with '
    '`pair_mismatches 0`, `evaluator_missing 0`, `executability_violations 0`, '
    '`clean_residue 0`, and a green selftest; and at the declared base the frozen '
    'witness command `python -X utf8 -I -B tools/round-53/v5-baseline-witness.py '
    '--root <LANE> --rev 6697518f0ad8e8399567ae4c9cd0207fc7c04d8b --freeze <FREEZE> '
    '--envelopes <DIR> --json-out <OUT2>` exits 1 with `executability_violations 1` '
    'naming `dmg_Z3_v3ddwrt_inode_table` and `clean_residue 7` naming the seven '
    'no-reader `clean` envelopes.')

_SEPARATOR_RE = None
_NAME_RE = None
_HANDLER_RE = None
_OPERATION_RE = None
_PROVIDER_RE = None
_ACTION_RE = None


class TableError(Exception):
    """The triage table is missing, refused or malformed."""


class EnvelopeError(Exception):
    """An envelope could not be read as an REA extract-firmware result."""


class InvocationError(Exception):
    """The command line does not select a readable surface."""


class Unevaluable(Exception):
    """The run could not be evaluated (exit 2)."""


# --------------------------------------------------------------------------------------
# table parsing (grammar as v5, plus the census column)
# --------------------------------------------------------------------------------------

def _regexes():
    global _SEPARATOR_RE, _NAME_RE, _HANDLER_RE, _OPERATION_RE, _PROVIDER_RE, _ACTION_RE
    if _SEPARATOR_RE is None:
        _SEPARATOR_RE = re.compile(r'^:?-+:?$')
        _NAME_RE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.\-]*$')
        _HANDLER_RE = re.compile(r'^[A-Za-z0-9_?*.\-\[\]]+$')
        _OPERATION_RE = re.compile(r'^[a-z][a-z0-9_.\-]*$')
        _PROVIDER_RE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.\-]*$')
        _ACTION_RE = re.compile(r'^[a-z][a-z0-9]*(-[a-z0-9]+)*$')
    return (_SEPARATOR_RE, _NAME_RE, _HANDLER_RE, _OPERATION_RE, _PROVIDER_RE, _ACTION_RE)


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
    return [c for c in s.split('|')]


def _parse_set_cell(cell, column, contains=False):
    _, name_re, _, _, _, _ = _regexes()
    if cell in ('*', 'none'):
        return ('any', None) if cell == '*' else ('none', None)
    if contains and cell.endswith('+'):
        body = cell[:-1]
        parts = body.split(',')
        if any(not part for part in parts):
            raise TableError('%s cell %r has an empty contains member' % (column, cell))
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
    _, _, handler_re, _, _, _ = _regexes()
    if cell == '*':
        return ('any', None)
    if cell == 'none':
        return ('none', None)
    parts = [p.strip() for p in cell.split(',')]
    if any(not p for p in parts):
        raise TableError('%s cell %r has an empty alternative' % (column, cell))
    if len(set(parts)) != len(parts):
        raise TableError('%s cell %r repeats an alternative' % (column, cell))
    for part in parts:
        if part in ('*', 'none'):
            raise TableError('%s cell %r mixes the reserved word %r with alternatives'
                             % (column, cell, part))
        if not handler_re.match(part):
            raise TableError('%s cell %r alternative %r is not a glob pattern'
                             % (column, cell, part))
        if not part.startswith(SQUASHFS_PREFIX):
            raise TableError('%s cell %r alternative %r does not begin %r: the cell is a '
                             'glob over SquashFS handler names, so a non-squashfs '
                             'pattern is a dead cell' % (column, cell, part,
                                                         SQUASHFS_PREFIX))
        hits = [name for name in KNOWN_HANDLERS if fnmatch.fnmatchcase(name, part)]
        if not hits:
            raise TableError('%s cell %r alternative %r matches none of the %d SquashFS '
                             'handler names unblob 26.6.4 registers (%s): a dead cell'
                             % (column, cell, part, len(KNOWN_HANDLERS),
                                ', '.join(KNOWN_HANDLERS)))
    if len(parts) == 1:
        return ('pattern', parts[0])
    return ('list', tuple(parts))


def _parse_census_cell(cell, column='census'):
    """``*`` or a comma-list over the closed census status set."""
    if cell == '*':
        return ('any', None)
    parts = [p.strip() for p in cell.split(',')]
    if any(not p for p in parts):
        raise TableError('%s cell %r has an empty alternative' % (column, cell))
    if len(set(parts)) != len(parts):
        raise TableError('%s cell %r repeats a status' % (column, cell))
    for part in parts:
        if part not in CENSUS_VALUES:
            raise TableError('%s cell %r status %r is not one of %s or *'
                             % (column, cell, part, ', '.join(CENSUS_VALUES)))
    return ('list', frozenset(parts))


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
        (label, operation, provider, handler, failing, gap, dep, be, sr, census,
         files, action, cause, source) = cells
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
            'census': _parse_census_cell(census, 'census'),
            'files': _parse_enum_cell(files, 'published files', FILES_VALUES),
            'action': action,
            'cause': cause,
            'source': source,
            'cells': cells,
        })
    if not rules:
        raise TableError('table at line %d has no rule rows' % first_line_no)
    return rules


def _find_marker(lines, marker):
    for i, line in enumerate(lines):
        if marker in line:
            return i
    return None


def _table_block(lines, marker_index):
    table_start = None
    for i in range(marker_index + 1, len(lines)):
        if lines[i].lstrip().startswith('|'):
            table_start = i
            break
    if table_start is None:
        raise TableError('no markdown table after the marker')
    actions_line = table_start - 1
    while actions_line >= 0 and not lines[actions_line].strip():
        actions_line -= 1
    if actions_line < 0 or ACTIONS_PREFIX not in lines[actions_line]:
        raise TableError('line %d: no %r vocabulary line directly above the table'
                         % (table_start + 1, ACTIONS_PREFIX))
    table = []
    i = table_start
    while i < len(lines) and lines[i].lstrip().startswith('|'):
        table.append(lines[i])
        i += 1
    return table, table_start, actions_line


def parse_skill(text):
    lines = text.splitlines()
    marker_index = _find_marker(lines, MARKER_V6)
    if marker_index is None:
        for refused in SUPERSEDED_MARKERS:
            at = _find_marker(lines, refused)
            if at is not None:
                raise TableError('line %d: refused marker %r; this interpreter reads only '
                                 '%r, and a superseded table is never evaluated'
                                 % (at + 1, refused, MARKER_V6))
        raise TableError('marker %r absent from the document' % MARKER_V6)
    table, table_start, actions_line = _table_block(lines, marker_index)
    vocabulary = parse_actions_line(lines[actions_line], actions_line + 1)
    rules = parse_table(table, table_start + 1, vocabulary)
    return rules, {'marker_line': marker_index + 1,
                   'actions_line': actions_line + 1,
                   'table_line': table_start + 1,
                   'rules': len(rules),
                   'actions': vocabulary}


# --------------------------------------------------------------------------------------
# envelope features (as v5, plus SUBJ)
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
    out = []
    if isinstance(diag, dict):
        out.append(diag)
        report = diag.get('report')
        if isinstance(report, dict) and report is not diag:
            out.append(report)
    return out


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


def subject_digest(data):
    subject = data.get('subject')
    if isinstance(subject, dict):
        digest = subject.get('digest')
        if isinstance(digest, dict):
            sha = digest.get('sha256')
            if isinstance(sha, str) and re.match(r'^[0-9a-f]{64}$', sha):
                return sha
    return ''


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
    squashfs_names = [name for name in handler_names if name.startswith(SQUASHFS_PREFIX)]
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
        'SUBJ': subject_digest(data),
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
# the frozen census (read from git at the freeze revision)
# --------------------------------------------------------------------------------------

class Census(object):
    """The fixture-level reader census, resolved per the declared resolution_rule."""

    def __init__(self, raw, source):
        if not isinstance(raw, dict) or raw.get('schema') != 1:
            raise Unevaluable('census %s: schema must be 1' % source)
        fixtures = raw.get('fixtures')
        if not isinstance(fixtures, list) or not fixtures:
            raise Unevaluable('census %s: no fixtures' % source)
        self.by_digest = {}
        self.rows = []
        for row in fixtures:
            if not isinstance(row, dict):
                raise Unevaluable('census %s: malformed fixture row' % source)
            key = row.get('sha256_12')
            status = row.get('status')
            if (not isinstance(key, str) or not re.match(r'^[0-9a-f]{12}$', key)
                    or status not in ('no-reader', 'partial', 'readable')):
                raise Unevaluable('census %s: bad fixture row %r' % (source, row))
            self.rows.append(row)
            self.by_digest.setdefault(key, status)
        self.lineage = {}
        for row in _as_list(raw.get('derived_lineage')):
            carrier = row.get('carrier_sha256_12')
            parent = row.get('parent_sha256_12')
            status = row.get('parent_status')
            if (not isinstance(carrier, str) or not isinstance(parent, str)
                    or status not in ('no-reader', 'partial', 'readable')):
                raise Unevaluable('census %s: bad lineage row %r' % (source, row))
            self.lineage[carrier] = {'parent_sha256_12': parent, 'status': status,
                                     'envelope': row.get('envelope')}
        self.source = source
        self.raw = raw
        self.recaptures = _as_list(raw.get('recaptures'))

    def status(self, digest, families):
        """Resolve one envelope's census status; (status, how) per resolution_rule."""
        if digest:
            short = digest[:12]
            if short in self.by_digest:
                return self.by_digest[short], 'fixture'
            if short in self.lineage:
                return self.lineage[short]['status'], 'lineage'
        for fam in families:
            if fam in NO_READER_FAMILIES:
                return 'no-reader', 'family'
            if fam in READER_BACKED_V1V3:
                return 'readable', 'family'
        return 'unknown', 'none'


def load_census(root, freeze):
    raw = git_show(root, freeze, CENSUS_RELPATH)
    if raw is None:
        raise Unevaluable('cannot read %s at freeze revision %r'
                          % (CENSUS_RELPATH, freeze))
    try:
        data = json.loads(raw)
    except ValueError as exc:
        raise Unevaluable('census at %s does not parse: %s' % (freeze, exc))
    return Census(data, 'git:%s:%s' % (freeze, CENSUS_RELPATH))


# --------------------------------------------------------------------------------------
# classification from the parsed table
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
    kind, payload = spec
    if kind == 'any':
        return True
    if kind == 'none':
        return not names
    if kind == 'list':
        return any(fnmatch.fnmatchcase(value, pattern)
                   for pattern in payload for value in names)
    return any(fnmatch.fnmatchcase(value, payload) for value in names)


def rule_matches(rule, feat, census_status):
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
    kind, payload = rule['census']
    if kind == 'list' and census_status not in payload:
        return False
    files = rule['files']
    if files == '0' and feat['P'] != 0:
        return False
    if files == '>0' and feat['P'] <= 0:
        return False
    return True


def classify(rules, feat, census_status):
    for rule in rules:
        if rule_matches(rule, feat, census_status):
            return rule
    return None


def decision(rule):
    if rule is None:
        return DEFAULT_LABEL, DEFAULT_ACTION
    return rule['label'], rule['action']


# --------------------------------------------------------------------------------------
# the fixed census-aware evaluator (independent of any table)
# --------------------------------------------------------------------------------------

NO_READER_SET = frozenset(NO_READER_FAMILIES)
READER_BACKED_SET = frozenset(READER_BACKED_V1V3)


def _meets(names, wanted):
    for name in names:
        if name in wanted:
            return True
    return False


def evaluate(feat, census):
    """Return (label, action, step) for one declared tuple.  Never reads a table."""
    op = feat['OP']
    pv = feat['PV']
    f = feat['F']
    g = set(feat['G'])
    d = set(feat['D'])
    be = feat['BE']
    sr = feat['SR'] == 'yes'
    p = feat['P']
    hf = feat['HF']

    if op != OPERATION_TOKEN or pv != 'unblob':
        return DEFAULT_LABEL, DEFAULT_ACTION, 1
    if not f and 'depth-limited' in g:
        return 'container-depth-limited', 'raise-depth', 2
    if not f:
        return 'no-squashfs-chunk', 'inspect-input', 3
    if 'missing-extractor-dependency' in g:
        if 'sasquatch-v4be' in d:
            return 'dep-missing-be', 'install-extractor-be', 4
        if 'sasquatch' in d:
            return 'dep-missing-le', 'install-extractor-le', 4
    if FAILURE_KIND in g and p > 0:
        return 'partial-body-failure', 'salvage-partial', 5
    if FAILURE_KIND in g and p == 0 and be == 'no' and 'squashfs_v4_be' in hf:
        return 'avm-marker-be-dropped', 'wrap-extractor-be', 6
    st_hf, _how_hf = census.status(feat['SUBJ'], hf)
    if FAILURE_KIND in g and p == 0 and st_hf == 'no-reader':
        return 'legacy-body-refused', 'preserve-unresolved', '6.5'
    if (FAILURE_KIND in g and p == 0 and _meets(hf, READER_BACKED_SET)
            and st_hf != 'no-reader'):
        return 'legacy-body-failure', 'cross-read-legacy', 7
    if (FAILURE_KIND in g and p == 0 and _meets(hf, NO_READER_SET)
            and st_hf != 'no-reader'):
        return 'no-reader-failure', 'preserve-unresolved', 8
    if FAILURE_KIND in g and p == 0:
        return 'body-extractor-failure', 'preserve-failure', 9
    if 'unknown-chunk-handler' in g:
        return 'unknown-residue', 'isolate-residue', 10
    if 'depth-limited' in g:
        return 'depth-limited', 'raise-depth', 11
    if sr and 'unpublished-entry' in g:
        return 'mixed-symlinks', 'audit-symlinks', 12
    if sr and not g:
        return 'escaping-symlink-removed', 'expect-link-absent', 13
    if g == {'unpublished-entry'}:
        return 'in-tree-symlink-metadata', 'count-gap', 14
    if not g:
        if p > 0:
            if _meets(f, NO_READER_SET):
                return 'clean-unverified', 'record-unverified', 15
            st_f, _how_f = census.status(feat['SUBJ'], f)
            if st_f == 'no-reader':
                return 'clean-unverified-fixture', 'record-unverified', 15
            return 'clean', 'none', 15
        return 'clean-empty', 'confirm-empty', 16
    return DEFAULT_LABEL, DEFAULT_ACTION, 17


# --------------------------------------------------------------------------------------
# the v6 table draft (embedded; printed by --print-v6-block)
# --------------------------------------------------------------------------------------

V6_ACTIONS = ('none inspect-input install-extractor-be install-extractor-le '
              'wrap-extractor-be cross-read-legacy isolate-residue preserve-failure '
              'salvage-partial raise-depth audit-symlinks expect-link-absent count-gap '
              'confirm-empty record-unverified preserve-unresolved')

NO_READER_CELL = ','.join(NO_READER_FAMILIES)
READER_BACKED_CELL = ','.join(READER_BACKED_V1V3)
NOT_NO_READER_CELL = 'partial,readable'

V6_ROWS = [
    # label, operation, provider, handler, failing handler, gap kinds, dependencies,
    # -be in child argv, symlink removed, census, published files, action, cause, source
    ['container-depth-limited', 'extract_firmware', 'unblob', 'none', '*',
     'depth-limited+', '*', '*', '*', '*', '*', 'raise-depth',
     'no SquashFS handler was named and REA stopped at max_depth -> rerun with a higher '
     'max_depth or descend into the published container',
     'SKILL.md table v4 row 1; S119 FirmwarePublication.js:23-29,:294-299'],
    ['no-squashfs-chunk', 'extract_firmware', 'unblob', 'none', '*', '*', '*', '*', '*',
     '*', '*', 'inspect-input',
     'neither a chunk nor a gap names a SquashFS handler -> check the magic and '
     'superblock before rerunning',
     'SKILL.md table v4 row 2; S112 :102,:159,:200,:245,:319,:364,:410,:463,:522'],
    ['dep-missing-be', 'extract_firmware', 'unblob', 'squashfs_*', '*',
     'missing-extractor-dependency+', 'sasquatch-v4be+', '*', '*', '*', '*',
     'install-extractor-be',
     'the chunk resolved its extractor to sasquatch-v4be and that binary was not found '
     '-> install the sasquatch-v4be binary and rerun into a fresh output directory',
     'SKILL.md table v4 row 3; S112 :40-41; S120 command.py:69-77'],
    ['dep-missing-le', 'extract_firmware', 'unblob', 'squashfs_*', '*',
     'missing-extractor-dependency+', 'sasquatch+', '*', '*', '*', '*',
     'install-extractor-le',
     'the chunk resolved its extractor to plain sasquatch and that binary was not found '
     '-> install the little-endian sasquatch binary and rerun',
     'SKILL.md table v4 row 4; S112 :37,:39-54; S120 report.py:118-122'],
    ['partial-body-failure', 'extract_firmware', 'unblob', 'squashfs_*', '*',
     'extractor-failure+', '*', '*', '*', '*', '>0', 'salvage-partial',
     'the extractor failed after publishing at least one regular file -> keep the '
     'published files and the failing command, mark the run incomplete, never score the '
     'set as clean',
     'SKILL.md table v4 row 5; S119 FirmwarePublication.js:288-293'],
    ['avm-marker-be-dropped', 'extract_firmware', 'unblob', 'squashfs_*',
     'squashfs_v4_be', 'extractor-failure+', '*', 'no', '*', '*', '0',
     'wrap-extractor-be',
     'the failing chunk is the v4 BE one and unblob dropped -be -> rerun through a PATH '
     'executable named sasquatch-v4be that appends -be',
     'SKILL.md table v4 row 6; S112 :44-50; S121 -DFIX_BE build'],
    ['legacy-body-refused', 'extract_firmware', 'unblob', 'squashfs_*', '*',
     'extractor-failure+', '*', '*', '*', 'no-reader', '0', 'preserve-unresolved',
     'the failing body published zero files and the fixture-level reader census marks '
     'its bytes NO-READER (fixture digest, derived lineage, or a no-reader family), so '
     'the cross-read the legacy row prescribes cannot run -> keep the failure '
     'unresolved: reader absence forbids both the damaged-body verdict and the '
     'broken-extractor verdict; this row sits above legacy-body-failure and duplicates '
     'no-reader-failure\'s action under a census trigger (declared, R53-C1)',
     'R53-C1 (plans/round-53-claims.md); CritTriV6 F1-F7; reader census '
     'tools/round-53/reader-census.json (round-50 receipt); CritTriV6 F5: the measured '
     'fact is reader refusal, never damage'],
    ['legacy-body-failure', 'extract_firmware', 'unblob', 'squashfs_*', READER_BACKED_CELL,
     'extractor-failure+', '*', '*', '*', NOT_NO_READER_CELL, '0', 'cross-read-legacy',
     'the failing chunk is a reader-backed v1-v3 body whose census status is not '
     'NO-READER and that published zero files -> cross-read the same chunk with '
     'unsquashfs and 7-Zip, and only a reader that lists the tree while sasquatch '
     'failed shows a broken extractor build; a NO-READER fixture is taken by '
     'legacy-body-refused above, and a synthetic reader-backed ddwrt FAILED body still '
     'routes here (the family-key discriminator, MutTriV6 F2)',
     'SKILL.md table v4 row 7; narrowed by R50-C3 (families) and R53-C1 (fixtures); '
     'reader census tools/round-53/reader-census.json'],
    ['no-reader-failure', 'extract_firmware', 'unblob', 'squashfs_*', NO_READER_CELL,
     'extractor-failure+', '*', '*', '*', NOT_NO_READER_CELL, '0',
     'preserve-unresolved',
     'the failing chunk is a no-reader FAMILY body whose census status is not NO-READER '
     '(a partial reader such as 7-Zip on broadcom) and published zero files -> keep the '
     'failure unresolved; a partial reader that DOES list the tree is not suppressed, '
     'so keep that cross-read result; NO-READER-fixture bodies are taken by '
     'legacy-body-refused above',
     'R50-C3; round-49 W2Skill.md F1; narrowed by R53-C1 (census)'],
    ['body-extractor-failure', 'extract_firmware', 'unblob', 'squashfs_*', '*',
     'extractor-failure+', '*', '*', '*', '*', '0', 'preserve-failure',
     'the extractor ran and published zero regular files on a body the rows above did '
     'not claim -> run the layout pre-check, keep the failing command, stdout and stderr',
     'SKILL.md table v4 row 8; S120 report.py:91-98; S124 :35'],
    ['unknown-residue', 'extract_firmware', 'unblob', 'squashfs_*', '*',
     'unknown-chunk-handler+', '*', '*', '*', '*', '*', 'isolate-residue',
     'bytes beside the filesystem belong to no parser -> keep the residue out of the '
     'oracle and re-carve the SquashFS chunk to unblob chunk end',
     'SKILL.md table v4 row 9; S119 FirmwarePublication.js:286; S118 :116-127'],
    ['depth-limited', 'extract_firmware', 'unblob', 'squashfs_*', '*', 'depth-limited+',
     '*', '*', '*', '*', '*', 'raise-depth',
     'REA stopped at max_depth and recorded one depth-limited gap per path -> rerun with '
     'a higher max_depth into a fresh output directory',
     'SKILL.md table v4 row 10; S119 FirmwarePublication.js:23-29,:294-299'],
    ['mixed-symlinks', 'extract_firmware', 'unblob', 'squashfs_*', '*',
     'unpublished-entry+', '*', '*', 'yes', '*', '*', 'audit-symlinks',
     'both link kinds are present in one image -> expect the escaped paths absent and '
     'count one gap per kept link or special file',
     'SKILL.md table v4 row 11; S118 :50-92; S122'],
    ['escaping-symlink-removed', 'extract_firmware', 'unblob', 'squashfs_*', '*', 'none',
     '*', '*', 'yes', '*', '*', 'expect-link-absent',
     'a link escaped the extraction root or looped and unblob removed it with a '
     'MaliciousSymlinkRemoved report -> expect the path to be absent',
     'SKILL.md table v4 row 12; S118 :42-47,:58-65,:79-87; S122'],
    ['in-tree-symlink-metadata', 'extract_firmware', 'unblob', 'squashfs_*', '*',
     'unpublished-entry', '*', '*', '*', '*', '*', 'count-gap',
     'the gap set is exactly one kind and every non-file entry stayed inside the '
     'extraction root -> expected, not a sasquatch failure: count one gap per entry',
     'SKILL.md table v4 row 13; S119 FirmwarePublication.js:301-307'],
    ['clean-unverified', 'extract_firmware', 'unblob', NO_READER_CELL, '*', 'none', '*',
     '*', 'no', '*', '>0', 'record-unverified',
     'the run completed with no gap and published regular files on a FAMILY with no '
     'validated complete independent oracle (a broadcom partial listing is never a '
     'complete oracle), so no oracle can corroborate the set -> record the envelope as '
     'unverified, never as clean',
     'R50-C3; round-49 W2Skill.md F2; census-conditioned sibling added by R53-C1'],
    ['clean-unverified-fixture', 'extract_firmware', 'unblob', 'squashfs_*', '*', 'none',
     '*', '*', 'no', 'no-reader', '>0', 'record-unverified',
     'the run completed with no gap and published regular files, but the FIXTURE-level '
     'reader census marks these bytes NO-READER (the ddwrt pad fixtures and '
     'nonstandard fixtures among the recon corpus) and no no-reader FAMILY owns them, '
     'so no oracle can corroborate the set -> record the envelope as unverified, never '
     'as clean; this row sits below clean-unverified (a family catch decides first) '
     'and carries its own label because the table grammar refuses duplicate labels',
     'R53-C1 (plans/round-53-claims.md); CritTriV6 F2; reader census '
     'tools/round-53/reader-census.json'],
    ['clean', 'extract_firmware', 'unblob', 'squashfs_*', '*', 'none', '*', '*', 'no',
     NOT_NO_READER_CELL, '>0', 'none',
     'every regular file was published, the gap set is empty, and the fixture-level '
     'census does not mark these bytes NO-READER (or a no-reader FAMILY owns them, '
     'taken by the rows above) -> nothing to install or fix; match files to the oracle '
     'by exact relative path and sha256',
     'SKILL.md table v4 row 14; census-narrowed by R53-C1 (the v5 row gave a '
     'no-reader-fixture run the oracle-backed action none)'],
    ['clean-empty', 'extract_firmware', 'unblob', 'squashfs_*', '*', 'none', '*', '*',
     'no', '*', '0', 'confirm-empty',
     'the extractor completed with no gap and published zero regular files -> confirm '
     'the independent oracle tree is empty before calling it clean',
     'SKILL.md table v4 row 15; S119 FirmwarePublication.js:301-307'],
]


def render_table(rows, actions=V6_ACTIONS, marker=MARKER_V6):
    out = [marker, '%s %s %s' % (ACTIONS_PREFIX, actions, ACTIONS_SUFFIX)]
    out.append('| ' + ' | '.join(HEADER) + ' |')
    out.append('| ' + ' | '.join(['---'] * len(HEADER)) + ' |')
    for row in rows:
        out.append('| ' + ' | '.join(row) + ' |')
    return '\n'.join(out) + '\n'


V6_BLOCK = render_table(V6_ROWS)


# --------------------------------------------------------------------------------------
# git access (read-only, utf-8 explicit - the host-portability fix)
# --------------------------------------------------------------------------------------

def git(root, args, check=True):
    proc = subprocess.run(['git', '-C', root] + list(args), capture_output=True,
                          text=True, encoding='utf-8')
    if check and proc.returncode != 0:
        raise Unevaluable('git %s failed: %s' % (' '.join(args),
                                                 (proc.stderr or '').strip()[:200]))
    return proc


def git_show(root, rev, path):
    proc = git(root, ['show', '%s:%s' % (rev, path)], check=False)
    if proc.returncode != 0:
        return None
    return proc.stdout


def is_ancestor(root, older, newer):
    proc = git(root, ['merge-base', '--is-ancestor', older, newer], check=False)
    if proc.returncode not in (0, 1):
        raise Unevaluable('git merge-base --is-ancestor failed: %s'
                          % (proc.stderr or '').strip()[:200])
    return proc.returncode == 0


def blob_sha(root, rev, path):
    proc = git(root, ['rev-parse', '%s:%s' % (rev, path)], check=False)
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def _self_sha256():
    try:
        with open(os.path.abspath(__file__), 'rb') as handle:
            return hashlib.sha256(handle.read()).hexdigest()
    except OSError:
        return None


def sha256_text(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


# --------------------------------------------------------------------------------------
# work and output directories (never a temporary partition, never a graded surface)
# --------------------------------------------------------------------------------------

GRADED_BASENAMES = ('SKILL.md', 'PROVINCE.md', 'LOG.md', 'SCORECARD.md', 'SHONEN.md')
TEMP_ROOTS = ('/tmp', '/var/tmp')


def _under(path, root):
    real = os.path.realpath(path)
    base = os.path.realpath(root)
    return real == base or real.startswith(base + os.sep)


def resolve_work(ns):
    if ns.work:
        base = os.path.abspath(ns.work)
    else:
        base = os.environ.get('TMPDIR') or ''
        if not base:
            raise InvocationError('no work directory: pass --work or set TMPDIR')
    real = os.path.realpath(base)
    for temp in TEMP_ROOTS:
        if real == temp or real.startswith(temp + os.sep):
            raise InvocationError('work directory %r is on a temporary partition; use a '
                                  'scratch path (nothing under /tmp is citable)' % real)
    try:
        os.makedirs(real, exist_ok=True)
    except OSError as exc:
        raise InvocationError('work directory %r cannot be created: %s'
                              % (real, exc))
    return real


def resolve_json_out(path, root):
    real = os.path.realpath(os.path.abspath(path))
    for temp in TEMP_ROOTS:
        if real == temp or real.startswith(temp + os.sep):
            raise InvocationError('--json-out %r is on a temporary partition; receipts '
                                  'must live in the lane tree' % real)
    if root:
        if _under(real, root):
            rel = os.path.relpath(real, os.path.realpath(root))
            head = rel.split(os.sep)[0]
            if head in ('tools', 'plans', 'corpus') or rel in GRADED_BASENAMES:
                raise InvocationError('--json-out %r would write into the graded or '
                                      'frozen surface %r' % (real, rel))
    parent = os.path.dirname(real)
    if parent and not os.path.isdir(parent):
        raise InvocationError('--json-out directory %r does not exist' % parent)
    return real


# --------------------------------------------------------------------------------------
# the run
# --------------------------------------------------------------------------------------

def envelope_entries(directory):
    out = []
    try:
        names = sorted(os.listdir(directory))
    except OSError as exc:
        raise Unevaluable('envelope directory %r: %s' % (directory, exc))
    for name in names:
        full = os.path.join(directory, name)
        if os.path.isdir(full):
            for leaf in ('envelope.json', 'rea-full.json', 'after.json'):
                candidate = os.path.join(full, leaf)
                if os.path.isfile(candidate):
                    out.append((name, candidate))
                    break
        elif name.endswith('.json'):
            out.append((os.path.splitext(name)[0], full))
    return out


def sources_binding(root, rev, freeze):
    """The claim's SOURCES row must be the landing entry's new-source citation."""
    text = git_show(root, freeze, CLAIMS_RELPATH)
    if text is None:
        raise Unevaluable('cannot read %s at freeze %r' % (CLAIMS_RELPATH, freeze))
    row = CLAIM_ROW_RE.search(text)
    entry = ENTRY_RE.search(text)
    if not row or not entry:
        return {'claim_row': None, 'entry': None, 'ok': False,
                'why': 'claims file names no claim_row/entry'}
    entry_text = git_show(root, rev, entry.group(1))
    ok = False
    why = 'entry absent at rev'
    if entry_text is not None:
        for line in entry_text.splitlines():
            if line.startswith('source:') and row.group(1) in line:
                ok = True
                why = 'cited on the source: line'
                break
        if not ok:
            why = 'entry %s does not cite %s on its source: line' % (entry.group(1),
                                                                     row.group(1))
    return {'claim_row': row.group(1), 'entry': entry.group(1), 'ok': ok, 'why': why}


def run(ns):
    root = os.path.abspath(ns.root) if ns.root else os.getcwd()
    if not os.path.isdir(root):
        raise Unevaluable('lane root %r is not a directory' % root)
    if not ns.freeze:
        raise InvocationError('--freeze is required (the census and the claim bind to it)')
    if not ns.rev:
        raise InvocationError('--rev is required unless --skill is given')
    if ns.skill:
        try:
            with open(ns.skill, 'r', encoding='utf-8') as handle:
                text = handle.read()
        except OSError as exc:
            raise Unevaluable('--skill %r: %s' % (ns.skill, exc))
        source = 'file:%s' % os.path.abspath(ns.skill)
    else:
        text = git_show(root, ns.rev, 'SKILL.md')
        if text is None:
            raise Unevaluable('cannot read SKILL.md at revision %r' % ns.rev)
        source = 'git:%s:SKILL.md' % ns.rev
    rules, info = parse_skill(text)
    census = load_census(root, ns.freeze)

    if not is_ancestor(root, ns.freeze, ns.rev):
        raise Unevaluable('freeze %r is not an ancestor of %r' % (ns.freeze, ns.rev))
    freeze_report = {'rev': ns.rev, 'freeze': ns.freeze, 'ancestor': True,
                     'instrument_sha256_at_freeze': None,
                     'instrument_sha256_at_rev': None,
                     'instrument_unchanged': None,
                     'census_unchanged': None,
                     'other_tools_round53_changed': []}
    at_freeze = git_show(root, ns.freeze, 'tools/round-53/sqfs-triage-v6.py')
    at_rev = git_show(root, ns.rev, 'tools/round-53/sqfs-triage-v6.py')
    if at_freeze is not None:
        freeze_report['instrument_sha256_at_freeze'] = sha256_text(at_freeze)
    if at_rev is not None:
        freeze_report['instrument_sha256_at_rev'] = sha256_text(at_rev)
    if at_freeze is not None and at_rev is not None:
        freeze_report['instrument_unchanged'] = at_freeze == at_rev
    census_freeze = git_show(root, ns.freeze, CENSUS_RELPATH)
    census_rev = git_show(root, ns.rev, CENSUS_RELPATH)
    freeze_report['census_unchanged'] = (census_freeze == census_rev
                                         and census_rev is not None)
    proc = git(root, ['diff', '--name-only', '%s..%s' % (ns.freeze, ns.rev)]
               + ['tools/round-53/'], check=False)
    if proc.returncode == 0:
        changed = [line for line in proc.stdout.splitlines() if line.strip()]
        freeze_report['other_tools_round53_changed'] = [
            line for line in changed
            if line not in ('tools/round-53/sqfs-triage-v6.py', CENSUS_RELPATH)]
    binding = sources_binding(root, ns.rev, ns.freeze)

    entries = envelope_entries(ns.envelopes)
    if not entries:
        raise Unevaluable('no envelope found under %r' % ns.envelopes)

    details = []
    mismatches = []
    evaluator_missing = []
    executability_violations = []
    clean_residue = []
    table_labels = {}
    evaluator_labels = {}
    table_distribution = {}
    evaluator_distribution = {}
    for envelope_id, path in entries:
        feat = load_envelope(path)
        st_hf, how_hf = census.status(feat['SUBJ'], feat['HF'])
        rule = classify(rules, feat, st_hf)
        table_label, table_action = decision(rule)
        abstained = None
        try:
            ev_label, ev_action, ev_step = evaluate(feat, census)
        except Exception as exc:                      # the evaluator abstains
            ev_label, ev_action, ev_step = None, None, None
            abstained = repr(exc)
        if ev_label is None:
            evaluator_missing.append({'envelope': envelope_id,
                                      'reason': abstained or 'no verdict'})
        # the census status the table row saw (clean rows consult F, failed rows HF)
        st_for_row, how_for_row = (census.status(feat['SUBJ'], feat['F'])
                                   if table_label in ('clean', 'clean-unverified',
                                                      'clean-unverified-fixture',
                                                      'clean-empty')
                                   else (st_hf, how_hf))
        if table_action == 'cross-read-legacy' and st_hf == 'no-reader':
            executability_violations.append({
                'envelope': envelope_id, 'census_status': st_hf, 'how': how_hf,
                'label': table_label, 'action': table_action})
        if table_label == 'clean' and st_for_row == 'no-reader':
            clean_residue.append({
                'envelope': envelope_id, 'census_status': st_for_row, 'how': how_for_row})
        table_labels[envelope_id] = table_label
        evaluator_labels[envelope_id] = ev_label
        table_distribution[table_label] = table_distribution.get(table_label, 0) + 1
        if ev_label is not None:
            evaluator_distribution[ev_label] = evaluator_distribution.get(ev_label, 0) + 1
        match = (table_label == ev_label and table_action == ev_action)
        if ev_label is None:
            match = False
        if not match:
            mismatches.append({
                'envelope': envelope_id,
                'path': path,
                'table_label': table_label,
                'table_action': table_action,
                'evaluator_label': ev_label,
                'evaluator_action': ev_action,
                'features': feat,
            })
        details.append({
            'envelope': envelope_id,
            'path': path,
            'table_label': table_label,
            'table_action': table_action,
            'table_rule': rule['index'] if rule else None,
            'evaluator_label': ev_label,
            'evaluator_action': ev_action,
            'evaluator_step': ev_step,
            'census_status': st_for_row,
            'census_how': how_for_row,
            'match': match,
            'features': feat,
        })

    met = (not mismatches and not evaluator_missing
           and not executability_violations and not clean_residue and binding['ok'])
    report = {
        'instrument': 'sqfs-triage-v6.py',
        'instrument_sha256': _self_sha256(),
        'predicate': PREDICATE,
        'schema': 1,
        'root': root,
        'rev': ns.rev,
        'freeze': ns.freeze,
        'skill_source': source,
        'table': {
            'marker_line': info['marker_line'],
            'actions_line': info['actions_line'],
            'table_line': info['table_line'],
            'rules': info['rules'],
            'actions': list(info['actions']),
        },
        'census': {'source': census.source, 'fixtures': len(census.rows),
                   'lineage_rows': len(census.lineage),
                   'recaptures': len(census.recaptures)},
        'sources_binding': binding,
        'n_envelopes': len(entries),
        'pair_mismatches': mismatches,
        'pair_mismatch_count': len(mismatches),
        'evaluator_missing': evaluator_missing,
        'executability_violations': executability_violations,
        'executability_violation_count': len(executability_violations),
        'clean_residue': clean_residue,
        'clean_residue_count': len(clean_residue),
        'table_labels': table_labels,
        'evaluator_labels': evaluator_labels,
        'label_distribution': {'table': table_distribution,
                               'evaluator': evaluator_distribution},
        'freeze': freeze_report,
        'envelopes': details,
        'verdict': 'met' if met else 'not met',
    }
    out_path = None
    if ns.json_out:
        out_path = resolve_json_out(ns.json_out, root)
        try:
            with open(out_path, 'w', encoding='utf-8') as handle:
                json.dump(report, handle, indent=1, sort_keys=True)
                handle.write('\n')
        except OSError as exc:
            raise Unevaluable('the receipt %r could not be written: %s'
                              % (out_path, exc))
        try:
            with open(out_path, 'r', encoding='utf-8') as handle:
                verify = json.load(handle)
        except (OSError, ValueError) as exc:
            raise Unevaluable('the receipt %r did not parse: %s' % (out_path, exc))
        for key in ('predicate', 'pair_mismatches', 'evaluator_missing',
                    'executability_violations', 'clean_residue', 'table_labels',
                    'n_envelopes', 'verdict', 'rev'):
            if key not in verify:
                raise Unevaluable('the receipt %r is missing the key %r'
                                  % (out_path, key))
    print('table: v6 (%d rules) from %s' % (info['rules'], source))
    print('census: %d fixtures, %d lineage rows from %s'
          % (len(census.rows), len(census.lineage), census.source))
    print('envelopes: %d   pair_mismatches: %d   evaluator_missing: %d   '
          'executability_violations: %d   clean_residue: %d'
          % (len(entries), len(mismatches), len(evaluator_missing),
             len(executability_violations), len(clean_residue)))
    for key in sorted(table_distribution):
        print('  %-28s table %3d   evaluator %3d'
              % (key, table_distribution[key], evaluator_distribution.get(key, 0)))
    for row in mismatches[:20]:
        print('  MISMATCH %s: table %s/%s  evaluator %s/%s'
              % (row['envelope'], row['table_label'], row['table_action'],
                 row['evaluator_label'], row['evaluator_action']))
    for row in executability_violations:
        print('  EXECUTABILITY-VIOLATION %s: %s/%s on a no-reader fixture (%s)'
              % (row['envelope'], row['label'], row['action'], row['how']))
    for row in clean_residue:
        print('  CLEAN-RESIDUE %s: clean on a no-reader fixture (%s)'
              % (row['envelope'], row['how']))
    if not binding['ok']:
        print('  SOURCES-BINDING: %s' % binding['why'])
    if out_path:
        print('json: %s' % out_path)
    return 0 if met else 1


# --------------------------------------------------------------------------------------
# selftest fixtures (a synthetic census; the corpus discriminators live in --controls)
# --------------------------------------------------------------------------------------

def _env(handler='squashfs_v4_le', handlers=(), gaps=(), be=None, sr=False, files=0,
         op='extract_firmware', pv='unblob', command=None, gap_handlers=None,
         digest=None):
    data = {'operation': op, 'provider': {'id': pv},
            'normalized_result': {'chunks': [], 'extraction_gaps': [], 'files': []}}
    if handler:
        data['normalized_result']['chunks'] = [{'handler': handler}]
    for extra in handlers:
        data['normalized_result']['chunks'].append({'handler': extra})
    for gap in gaps:
        row = {'kind': gap}
        if gap_handlers and gap in gap_handlers:
            row['handler'] = gap_handlers[gap]
        data['normalized_result']['extraction_gaps'].append(row)
    data['normalized_result']['files'] = [{'path': 'f/%d' % i} for i in range(files)]
    if be is not None:
        cmd = 'sasquatch %s' % be
        data['normalized_result']['diagnostics'] = [
            {'report': {'command': cmd,
                        '__typename__': ('MaliciousSymlinkRemoved' if sr else 'Stat')}}]
    elif command is not None:
        data['normalized_result']['diagnostics'] = [{'report': {'command': command}}]
    if digest:
        data['subject'] = {'digest': {'sha256': digest}}
    return data


def _dig(n):
    """A synthetic 64-hex digest whose FIRST 12 chars carry the census id."""
    return ('%012x' % n) + '0' * 52


SYNTHETIC_CENSUS = {
    'aa0000000001': 'no-reader',
    'aa0000000002': 'readable',
    'aa0000000003': 'partial',
    'bb0000000001': 'no-reader',
    'bb0000000002': 'readable',
    'cc0000000001': 'partial',
    'cc0000000002': 'readable',
    'dd0000000001': 'no-reader',
    'dd0000000002': 'readable',
    'ee0000000001': 'readable',
}


def _synth_census():
    raw = {
        'schema': 1,
        'fixtures': [{'family': fam, 'fixture': name, 'sha256_12': dig,
                      'unsquashfs_exit': 0 if st == 'readable' else 1,
                      'sevenzip_exit': 0 if st in ('readable', 'partial') else 2,
                      'status': st}
                     for (fam, name, dig, st) in [
                         ('squashfs_v3_ddwrt', 'np.bin', 'aa0000000001', 'no-reader'),
                         ('squashfs_v3_ddwrt', 'le.bin', 'aa0000000002', 'readable'),
                         ('squashfs_v3', 'x.bin', 'bb0000000001', 'readable'),
                         ('squashfs_v3', 'y.bin', 'bb0000000002', 'readable'),
                         ('squashfs_v3_broadcom', 'p.bin', 'cc0000000001', 'partial'),
                         ('squashfs_v3_broadcom', 'q.bin', 'cc0000000002', 'readable'),
                         ('squashfs_v2_nonstandard', 'n.bin', 'dd0000000001', 'no-reader'),
                         ('squashfs_v2_nonstandard', 'm.bin', 'dd0000000002', 'readable'),
                         ('squashfs_v4_le', 'v.bin', 'ee0000000001', 'readable')]],
        'derived_lineage': [{'envelope': 'z3-like', 'carrier_sha256_12': 'ff0000000001',
                             'parent_sha256_12': 'aa0000000001', 'parent_status':
                             'no-reader'}],
        'recaptures': [],
    }
    return Census(raw, 'synthetic')


# id, envelope, expected (label, action)
FIXTURES = [
    ('z3-like', _env(handler='squashfs_v3_ddwrt', gaps=['extractor-failure'], be='-be',
                     files=0, digest=_dig(0xff0000000001)),
     ('legacy-body-refused', 'preserve-unresolved')),
    ('ddwrt-failed-readable', _env(handler='squashfs_v3_ddwrt', gaps=['extractor-failure'],
                                   be='-be', files=0, digest=_dig(0xaa0000000002)),
     ('legacy-body-failure', 'cross-read-legacy')),
    ('v3-legacy', _env(handler='squashfs_v3', gaps=['extractor-failure'], be='-le',
                       files=0, digest=_dig(0xbb0000000001)),
     ('legacy-body-failure', 'cross-read-legacy')),
    ('v2ns-failed-noreader', _env(handler='squashfs_v2_nonstandard',
                                  gaps=['extractor-failure'], be='-le', files=0,
                                  digest=_dig(0xdd0000000001)),
     ('legacy-body-refused', 'preserve-unresolved')),
    ('v3bc-failed-partial', _env(handler='squashfs_v3_broadcom',
                                 gaps=['extractor-failure'], be='-le', files=0,
                                 digest=_dig(0xcc0000000001)),
     ('no-reader-failure', 'preserve-unresolved')),
    ('ddwrt-clean-noreader', _env(handler='squashfs_v3_ddwrt', files=4,
                                  digest=_dig(0xaa0000000001)),
     ('clean-unverified-fixture', 'record-unverified')),
    ('ddwrt-clean-readable', _env(handler='squashfs_v3_ddwrt', files=4,
                                  digest=_dig(0xaa0000000002)),
     ('clean', 'none')),
    ('v2ns-clean', _env(handler='squashfs_v2_nonstandard', files=4,
                        digest=_dig(0xdd0000000001)),
     ('clean-unverified', 'record-unverified')),
    ('v3bc-clean-partial', _env(handler='squashfs_v3_broadcom', files=4,
                                digest=_dig(0xcc0000000001)),
     ('clean-unverified', 'record-unverified')),
    ('v3bc-clean-readable', _env(handler='squashfs_v3_broadcom', files=4,
                                 digest=_dig(0xcc0000000002)),
     ('clean-unverified', 'record-unverified')),
    ('v3-clean', _env(handler='squashfs_v3', files=4, digest=_dig(0xbb0000000001)),
     ('clean', 'none')),
    ('v4le-clean', _env(handler='squashfs_v4_le', files=2, digest=_dig(0xee0000000001)),
     ('clean', 'none')),
    ('symlink-row', _env(handler='squashfs_v4_le', gaps=['unpublished-entry'], be='-le',
                         sr=True, files=2, digest=_dig(0xee0000000001)),
     ('mixed-symlinks', 'audit-symlinks')),
]


def _pairs(rules, census, fixtures=FIXTURES):
    out = {}
    for name, env, _want in fixtures:
        feat = features(env)
        st, _how = census.status(feat['SUBJ'], feat['HF'])
        rule = classify(rules, feat, st)
        out[name] = decision(rule)
    return out


def _require(cond, message):
    if not cond:
        raise AssertionError(message)


def _row_index(rows, label):
    for i, row in enumerate(rows):
        if row[0] == label:
            return i
    raise AssertionError('no row labelled %r' % label)


# ------------------------------------------------------------------ the mutation battery

def _mut_refused_row_deleted(rows):
    out = [list(r) for r in rows]
    del out[_row_index(out, 'legacy-body-refused')]
    return out


def _mut_refused_family_keyed(rows):
    """Widen the refused row's census cell to * (a family-keyed mutant)."""
    out = [list(r) for r in rows]
    out[_row_index(out, 'legacy-body-refused')][9] = '*'
    return out


def _mut_legacy_census_narrowed_wrong(rows):
    out = [list(r) for r in rows]
    out[_row_index(out, 'legacy-body-failure')][9] = 'no-reader'
    return out


def _mut_clean_fixture_row_deleted(rows):
    out = [list(r) for r in rows]
    del out[_row_index(out, 'clean-unverified-fixture')]
    return out


def _mut_clean_family_row_deleted(rows):
    out = [list(r) for r in rows]
    del out[_row_index(out, 'clean-unverified')]
    return out


def _mut_clean_fixture_census_widened(rows):
    out = [list(r) for r in rows]
    out[_row_index(out, 'clean-unverified-fixture')][9] = '*'
    return out


def _mut_clean_census_narrowed_wrong(rows):
    out = [list(r) for r in rows]
    out[_row_index(out, 'clean')][9] = 'partial'
    return out


def _mut_refused_action_swapped(rows):
    """Swap the refused row's action with the legacy row's (cross-read on no-reader)."""
    out = [list(r) for r in rows]
    i = _row_index(out, 'legacy-body-refused')
    j = _row_index(out, 'legacy-body-failure')
    out[i][11], out[j][11] = out[j][11], out[i][11]
    return out


def _mut_clean_fixture_precedence_swapped(rows):
    """Move clean-unverified-fixture BELOW the clean row."""
    out = [list(r) for r in rows]
    i = out.pop(_row_index(out, 'clean-unverified-fixture'))
    j = _row_index(out, 'clean')
    out.insert(j + 1, i)
    return out


def _mut_no_reader_failure_row_deleted(rows):
    out = [list(r) for r in rows]
    del out[_row_index(out, 'no-reader-failure')]
    return out


def _mut_junk(rows):
    out = []
    for i, row in enumerate(rows):
        row = list(row)
        row[0] = 'junk-%d' % i
        row[3] = 'squashfs_*'
        row[4] = '*'
        row[5] = '*'
        row[6] = '*'
        row[7] = '*'
        row[8] = '*'
        row[9] = '*'
        row[10] = '*'
        row[11] = 'none'
        out.append(row)
    return out


MUTATIONS = [
    ('refused-row-deleted', _mut_refused_row_deleted,
     {'z3-like', 'v2ns-failed-noreader'}),
    ('refused-family-keyed', _mut_refused_family_keyed,
     {'ddwrt-failed-readable', 'v3-legacy', 'v3bc-failed-partial'}),
    ('legacy-census-narrowed-wrong', _mut_legacy_census_narrowed_wrong,
     {'v3-legacy', 'ddwrt-failed-readable'}),
    ('clean-fixture-row-deleted', _mut_clean_fixture_row_deleted,
     {'ddwrt-clean-noreader'}),
    ('clean-fixture-census-widened', _mut_clean_fixture_census_widened,
     {'ddwrt-clean-readable', 'v3-clean', 'v4le-clean'}),
    ('clean-census-narrowed-wrong', _mut_clean_census_narrowed_wrong,
     {'ddwrt-clean-readable', 'v3-clean', 'v4le-clean'}),
    ('refused-action-swapped', _mut_refused_action_swapped,
     {'z3-like', 'v2ns-failed-noreader', 'v3-legacy', 'ddwrt-failed-readable'}),
    ('clean-unverified-family-row-deleted', _mut_clean_family_row_deleted,
     {'v2ns-clean', 'v3bc-clean-partial', 'v3bc-clean-readable'}),
    ('no-reader-failure-row-deleted', _mut_no_reader_failure_row_deleted,
     {'v3bc-failed-partial'}),
    ('junk-table', _mut_junk,
     frozenset(name for name, _e, _w in FIXTURES)),
]


def _mutate_text_table(mutator):
    return render_table(mutator([list(r) for r in V6_ROWS]))


def emit_mutant(name):
    for mut_name, mutator, _expected in MUTATIONS:
        if mut_name == name:
            return _mutate_text_table(mutator)
    raise InvocationError('unknown mutation %r; known: %s'
                          % (name, ', '.join(m for m, _f, _e in MUTATIONS)))


def _parse_block(block):
    return parse_skill('# SKILL\n\n## c\n\n' + block + '\n\n## z\n\n')


# --------------------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------------------

def selftest(ns):
    work = resolve_work(ns)
    passed = 0
    failed = []
    cases = []

    def case(fn):
        cases.append(fn)
        return fn

    @case
    def c_v6_table_matches_evaluator():
        census = _synth_census()
        rules, info = _parse_block(V6_BLOCK)
        _require(info['rules'] == len(V6_ROWS), 'rule count %d' % info['rules'])
        pairs = _pairs(rules, census)
        wrong = {name: (pairs[name], want) for name, env, want in FIXTURES
                 if pairs[name] != want}
        _require(not wrong, 'v6 draft: wrong pairs %r' % wrong)
        return '%d fixtures match' % len(FIXTURES)

    @case
    def c_superseded_marker_refused():
        for marker in SUPERSEDED_MARKERS:
            block = render_table([list(r) for r in V6_ROWS], V6_ACTIONS, marker)
            try:
                _parse_block(block)
            except TableError:
                continue
            raise AssertionError('superseded marker %r was not refused' % marker)
        return '%d superseded markers refused' % len(SUPERSEDED_MARKERS)

    @case
    def c_mutations_exact_flip():
        census = _synth_census()
        rules, _info = _parse_block(V6_BLOCK)
        base = _pairs(rules, census)
        for name, mutator, expected in MUTATIONS:
            mrules, _i = _parse_block(_mutate_text_table(mutator))
            flipped = {n for n in base if base[n] != _pairs(mrules, census).get(n)}
            _require(flipped == expected,
                     'mutation %s flipped %r, expected %r' % (name, sorted(flipped),
                                                              sorted(expected)))
        return '%d mutations exact' % len(MUTATIONS)

    @case
    def c_dead_cell_refused():
        rows = [list(r) for r in V6_ROWS]
        rows[_row_index(rows, 'clean')][9] = 'no-such-status'
        block = render_table(rows)
        try:
            _parse_block(block)
        except TableError:
            return 'dead census cell refused'
        raise AssertionError('a census cell over an unknown status was accepted')

    @case
    def c_family_key_discriminator():
        """MutTriV6 F2: a family-keyed refused row must flip the readable ddwrt body."""
        census = _synth_census()
        mrows = _mut_refused_family_keyed([list(r) for r in V6_ROWS])
        mrules, _i = _parse_block(render_table(mrows))
        pairs = _pairs(mrules, census)
        _require(pairs['ddwrt-failed-readable'] == ('legacy-body-refused',
                                                    'preserve-unresolved'),
                 'family-keyed mutant did not condemn the readable ddwrt body: %r'
                 % (pairs['ddwrt-failed-readable'],))
        return 'family-key mutant is red on the synthetic witness'

    @case
    def c_census_source_binding():
        raw = {'schema': 1, 'fixtures': [], 'derived_lineage': [], 'recaptures': []}
        try:
            Census(raw, 'empty')
        except Unevaluable:
            return 'empty census refused'
        raise AssertionError('an empty census was accepted')

    @case
    def c_lineage_resolution():
        census = _synth_census()
        st, how = census.status(_dig(0xff0000000001)[:64], [])
        _require(st == 'no-reader' and how == 'lineage',
                 'lineage resolution gave %r/%r' % (st, how))
        st, how = census.status('', ['squashfs_v3_ddwrt'])
        _require(st == 'readable' and how == 'family',
                 'family fallback gave %r/%r' % (st, how))
        return 'lineage and family resolution verified'

    for fn in cases:
        try:
            note = fn()
            passed += 1
            print('  ok   %s — %s' % (fn.__name__, note))
        except AssertionError as exc:
            failed.append(fn.__name__)
            print('  FAIL %s — %s' % (fn.__name__, exc))
        except Exception as exc:                            # noqa: BLE001
            failed.append(fn.__name__)
            print('  FAIL %s — %r' % (fn.__name__, exc))
    print('selftest: %d cases, pass %d, fail %d' % (len(cases), passed, len(failed)))
    report = {'instrument': 'sqfs-triage-v6.py', 'selftest_schema': 1,
              'instrument_sha256': _self_sha256(), 'cases': len(cases),
              'pass': passed, 'fail': len(failed), 'failed': failed,
              'work': work}
    out_path = None
    if ns.json_out:
        out_path = resolve_json_out(ns.json_out, ns.root or None)
        with open(out_path, 'w', encoding='utf-8') as handle:
            json.dump(report, handle, indent=1, sort_keys=True)
            handle.write('\n')
        print('json: %s' % out_path)
    return 0 if not failed else 1


# --------------------------------------------------------------------------------------
# controls (scored on the real corpus and on the selftest fixtures)
# --------------------------------------------------------------------------------------

def corpus_control(ns):
    root = os.path.abspath(ns.root) if ns.root else os.getcwd()
    census = load_census(root, ns.freeze)
    synth = _synth_census()
    entries = envelope_entries(ns.envelopes)
    if not entries:
        raise Unevaluable('no envelope found under %r' % ns.envelopes)
    corpus = []
    for envelope_id, path in entries:
        feat = load_envelope(path)
        corpus.append((envelope_id, path, feat))
    fixtures = [(name, '<fixture>', features(env)) for name, env, _want in FIXTURES]
    # the corpus scope scores against the REAL frozen census; the fixture scope
    # scores against the synthetic census (the synthetic digests exist nowhere in
    # the real one, so a family fallback would silently decide there)
    scopes = [('corpus', corpus, census), ('fixtures', fixtures, synth)]

    rules, _info = _parse_block(V6_BLOCK)
    base_pairs_fixture = _pairs(rules, synth)

    def evaluate_scope(mut_block, scope, scope_census):
        mrules, _i = _parse_block(mut_block)
        mismatches = []
        for envelope_id, path, feat in scope:
            st, _how = scope_census.status(feat['SUBJ'], feat['HF'])
            rule = classify(mrules, feat, st)
            t_label, t_action = decision(rule)
            try:
                e_label, e_action, _s = evaluate(feat, scope_census)
            except Exception:                               # noqa: BLE001
                e_label, e_action = None, None
            if t_label != e_label or t_action != e_action:
                mismatches.append({'envelope': envelope_id, 'table_label': t_label,
                                   'table_action': t_action, 'evaluator_label': e_label,
                                   'evaluator_action': e_action})
        return mismatches

    results = []
    for name, mutator, expected in MUTATIONS:
        block = _mutate_text_table(mutator)
        per_scope = {}
        for scope_name, scope, scope_census in scopes:
            mismatches = evaluate_scope(block, scope, scope_census)
            per_scope[scope_name] = {
                'n_envelopes': len(scope),
                'pair_mismatches': len(mismatches),
                'red': bool(mismatches),
                'mismatched_envelopes': sorted({m['envelope'] for m in mismatches})[:12],
            }
        # the mutation must also flip exactly its declared fixture set
        mrules, _i = _parse_block(block)
        base = base_pairs_fixture
        flipped = {n for n in base if base[n] != _pairs(mrules, synth).get(n)}
        results.append({
            'control': name, 'declared_fixture_flip': sorted(expected),
            'fixture_flip_observed': sorted(flipped),
            'fixture_flip_exact': flipped == set(expected),
            'scopes': per_scope,
            'red_anywhere': any(s['red'] for s in per_scope.values()),
        })
    report = {
        'instrument': 'sqfs-triage-v6.py', 'instrument_sha256': _self_sha256(),
        'predicate': PREDICATE, 'schema': 1, 'envelopes': ns.envelopes,
        'n_envelopes': len(corpus), 'census': census.source,
        'fixture_census': 'synthetic', 'controls': results,
        'all_controls_red_somewhere': all(r['red_anywhere'] for r in results),
        'all_fixture_flips_exact': all(r['fixture_flip_exact'] for r in results),
    }
    work = None
    out_path = None
    if ns.json_out:
        out_path = resolve_json_out(ns.json_out, root)
        with open(out_path, 'w', encoding='utf-8') as handle:
            json.dump(report, handle, indent=1, sort_keys=True)
            handle.write('\n')
        print('json: %s' % out_path)
    for row in results:
        print('  %-34s corpus=%-8s fixtures=%-8s flip_exact=%s'
              % (row['control'],
                 'RED(%d)' % row['scopes']['corpus']['pair_mismatches']
                 if row['scopes']['corpus']['red'] else 'GREEN-or-VACUOUS',
                 'RED(%d)' % row['scopes']['fixtures']['pair_mismatches']
                 if row['scopes']['fixtures']['red'] else 'GREEN-or-VACUOUS',
                 row['fixture_flip_exact']))
    print('controls: %d, all red somewhere: %s, fixture flips exact: %s'
          % (len(results), report['all_controls_red_somewhere'],
             report['all_fixture_flips_exact']))
    return 0 if (report['all_controls_red_somewhere']
                 and report['all_fixture_flips_exact']) else 1


# --------------------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------------------

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--root', default=None)
    parser.add_argument('--rev', default=None)
    parser.add_argument('--freeze', default=None)
    parser.add_argument('--envelopes', default=None)
    parser.add_argument('--json-out', default=None)
    parser.add_argument('--skill', default=None)
    parser.add_argument('--work', default=None)
    parser.add_argument('--selftest', action='store_true')
    parser.add_argument('--controls', action='store_true')
    parser.add_argument('--print-v6-block', action='store_true')
    ns = parser.parse_args(argv)
    try:
        if ns.print_v6_block:
            sys.stdout.write(V6_BLOCK)
            return 0
        if ns.selftest:
            return selftest(ns)
        if ns.controls:
            if not ns.envelopes or not ns.freeze:
                raise InvocationError('--controls needs --envelopes and --freeze')
            return corpus_control(ns)
        if not ns.envelopes:
            raise InvocationError('--envelopes is required')
        return run(ns)
    except (TableError, EnvelopeError, InvocationError, Unevaluable) as exc:
        print('sqfs-triage-v6: %s' % exc, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
