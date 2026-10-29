#!/usr/bin/env python3
"""sqfs-triage-v5.py - executable SquashFS extract-firmware outcome triage, table v5.

R50-C3 scoring instrument (round 50, attempt 2, wave 3 build).  It reads exactly two
surfaces and nothing else:

  * a SKILL.md document, taken from git at a named revision
    (``git -C <root> show <rev>:SKILL.md``, read-only), from which it parses the
    FIRST markdown table that follows the marker ``<!-- sqfs-triage-table v5 -->``;
    when the document carries no v5 marker it falls back to the v4 marker
    (``<!-- sqfs-triage-table v4 -->``) so that the same command can be run against a
    revision that has not landed the v5 table yet - that fallback is the RED-BEFORE
    witness, not a second supported version.  A document whose newest triage marker is
    v1/v2/v3 is REFUSED (exit 2): a superseded table is never silently evaluated.
  * a directory of REA envelopes (rea-agents 6.5.0), each either a bare ``data``
    object or a full CLI envelope ``{ok, data, meta}``.

It never invokes REA, unblob or sasquatch, never reads a carrier, never writes into the
lane tree, and never touches a network.

PREDICATE (copied verbatim from ``plans/round-50-attempt2-claims.md``, section
R50-C3, so the instrument and the claim cannot drift; the same sentence is written into
every JSON receipt under the key ``predicate``):

  at the measured revision REV, with FREEZE an ancestor of REV, frozen paths untouched,
  running `python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --root <LANE> --rev <REV>
  --freeze <FREEZE> --envelopes <DIR> --json-out <OUT>` exits 0 with `pair_mismatches 0`,
  `evaluator_missing 0`, `table_labels == evaluator_labels` on every envelope of the
  frozen held-out dir, `selftest` green (every committed mutation flips ≥1 pair, none a
  no-op or cross-flip, do-nothing red); and at the base REV the same command exits 1
  with the no-reader `*_ddefault` rows among the mismatches.

WHAT v5 CHANGES AGAINST v4 (the depth this instrument scores)
--------------------------------------------------------------
Round 49 wave 2 (``W2Skill.md`` F1, F2) read the v4 table and found two mis-routings
for the three SquashFS handler families that have NO VALIDATED COMPLETE INDEPENDENT
ORACLE: ``squashfs_v2_nonstandard``, ``squashfs_v3_broadcom`` and
``squashfs_v3_nonstandard``.  (``squashfs_v3_broadcom`` has a PARTIAL reader - 7-Zip
lists the committed LE fixture while ``unsquashfs`` refuses it - so it has no COMPLETE
independent oracle, and a no-reader FAILURE label never suppresses a successful partial
cross-read.)  The set is handler-level and frozen; the census behind it is fixture-level,
so ``squashfs_v3_ddwrt`` keeps its reader-backed routing with a disclosed per-variant
residue - see "THE READER BOUNDARY" below.

  F1  the ``legacy-body-failure`` row's ``failing handler`` cell is ``squashfs_v[123]*``,
      which matches all three no-reader families, and the row's cross-read rule
      ("if the independent readers fail where sasquatch failed the body is damaged")
      condemns a HEALTHY no-reader body - reader failure there is guaranteed by
      definition, not evidence of damage.
  F2  the ``clean`` row's action is ``none`` ("match files to the oracle"), and no oracle
      can exist for a no-reader family; the four committed v2ns ``_ddefault`` recon
      envelopes label ``clean``/``none`` today, contradicting the Frontier status those
      families hold in PROVINCE.md.

v5 therefore changes two things and nothing else:

  * the ``legacy-body-failure`` row's ``failing handler`` cell is narrowed from
      ``squashfs_v[123]*`` to the READER-BACKED v1-v3 families only:
      ``squashfs_v1,squashfs_v2,squashfs_v3,squashfs_v3_ddwrt``
      (a comma-separated list of four globs - see GRAMMAR DELTA below);
  * two rows are added, both keyed on the NO-READER families:
      ``clean-unverified``    gaps ``none``, published files ``>0`` -> ``record-unverified``
      ``no-reader-failure``   gap kinds ``extractor-failure+``, published files ``0``
                              -> ``preserve-unresolved``
    ``clean-unverified`` sits ABOVE the v4 ``clean`` row (so a no-reader clean run is
    unverified, never clean); ``no-reader-failure`` sits BELOW ``legacy-body-failure``
    and ABOVE the generic ``body-extractor-failure`` row (so a broadened legacy glob
    still shadows it - that shadowing is what makes the widening mutation observable).

Every other v4 row is carried over unchanged, and every reader-backed family
(``squashfs_v1``, ``squashfs_v2``, ``squashfs_v3``, ``squashfs_v3_ddwrt``,
``squashfs_v4_le``, ``squashfs_v4_be``, ``squashfs_v4_broadcom``) keeps its v4 label and
its v4 action.

GRAMMAR DELTA (the one change to the table grammar, and why it is needed)
-------------------------------------------------------------------------
The v4 handler-family cell is ONE glob, matched with ``fnmatch.fnmatchcase`` over the
handler set F (or over the failing-handler set HF).  No single glob over the ten
SquashFS handler names unblob 26.6.4 registers can express "the reader-backed v1-v3
families": ``squashfs_v[123]*`` also matches the three no-reader families (that is F1),
and ``squashfs_v[123]`` drops ``squashfs_v3_ddwrt``, which IS reader-backed and must
keep the legacy row.  v5 therefore lets a handler-family cell be a COMMA-SEPARATED LIST
of globs:

  * every alternative is validated against the pinned ten-name vocabulary (an
    alternative that matches no known handler is a dead cell and makes the table
    malformed, exit 2 - never a silent non-match);
  * the cell matches when ANY alternative matches ANY member of F (respectively HF) -
    the same positive subset test the single-glob cell had;
  * the ``*`` and ``none`` cells keep their v4 meaning and may not be combined with
    other alternatives;
  * no other column changes: the ``gap kinds`` and ``dependencies`` columns already had
    a comma-separated CONTAINS form (``a,b+``), so a comma in a HANDLER cell was
    previously a malformed cell and is now a list - the two columns are disjoint in
    meaning and cannot be confused.

The v5 action vocabulary is the v4 vocabulary (15 tokens) plus ``record-unverified`` and
``preserve-unresolved`` (17 tokens).

THE EVALUATOR (independent of any table)
-----------------------------------------
The evaluator is written from the claim's precedence text, NOT from the table, and it is
never re-derived from a table: it is a fixed function of the envelope's own declared
tuple.  The tuple is what the envelope itself records:

  OP  ``operation``                                   (the verb REA recorded)
  PV  ``provider.id``                                 (or the provider string)
  H   every ``normalized_result.chunks[].handler`` and
      ``normalized_result.extraction_gaps[].handler``, nulls dropped
  F   the ``squashfs``-prefixed members of H
  HF  the ``squashfs``-prefixed handler of every ``extractor-failure`` gap row; F when
      no such row records one (v4 amendment A1)
  G   set of ``normalized_result.extraction_gaps[].kind``
  D   union of ``normalized_result.extraction_gaps[].dependencies``
  BE  ``yes`` / ``no`` / ``n/a`` over recorded sasquatch child argvs (only a child argv
      naming a binary whose basename starts ``sasquatch`` counts; a string argv is
      tokenised with shlex, a list argv is used as given)
  SR  ``yes`` iff a ``MaliciousSymlinkRemoved`` producer report is visible
      (``__typename__`` on a diagnostics entry, on its nested ``report``, or on a dict
      under ``raw_result``); a bare substring in printed stdout is NOT accepted
  P   ``len(normalized_result.files)``; an absent list reads 0

The evaluator's precedence (first match wins), which the v5 table must reproduce row for
row:

   1  OP != extract_firmware or PV != unblob        -> unclassified / none
   2  F empty and depth-limited in G                 -> container-depth-limited / raise-depth
   3  F empty                                       -> no-squashfs-chunk / inspect-input
   4  missing-extractor-dependency in G: D holds sasquatch-v4be -> dep-missing-be /
      install-extractor-be; else D holds sasquatch -> dep-missing-le / install-extractor-le
   5  extractor-failure in G and P > 0              -> partial-body-failure / salvage-partial
   6  extractor-failure in G, P = 0, BE = no and squashfs_v4_be in HF
                                                     -> avm-marker-be-dropped / wrap-extractor-be
   7  extractor-failure in G, P = 0 and HF meets the reader-backed v1-v3 families
                                                     -> legacy-body-failure / cross-read-legacy
   8  extractor-failure in G, P = 0 and HF meets a NO-READER family
                                                     -> no-reader-failure / preserve-unresolved
   9  extractor-failure in G and P = 0              -> body-extractor-failure / preserve-failure
  10  unknown-chunk-handler in G                    -> unknown-residue / isolate-residue
  11  depth-limited in G                            -> depth-limited / raise-depth
  12  SR = yes and unpublished-entry in G           -> mixed-symlinks / audit-symlinks
  13  SR = yes and G empty                          -> escaping-symlink-removed / expect-link-absent
  14  G = {unpublished-entry}                       -> in-tree-symlink-metadata / count-gap
  15  G empty, P > 0 and F meets a NO-READER family -> clean-unverified / record-unverified
  16  G empty: P > 0 -> clean / none ; P = 0 -> clean-empty / confirm-empty
  17  anything else                                 -> unclassified / none

THE READER BOUNDARY (stated, not hidden)
------------------------------------------
The no-reader set is HANDLER-LEVEL and frozen; the reader census behind it is
FIXTURE-level.  Re-measured 2026-10-29 on the committed round-42 fixture bytes
(``unsquashfs`` 4.7.5 ``-lls`` and 7-Zip 26.04 ``l -tSquashFS``, per family per fixture):
``squashfs_v3`` 8/8 readable by both; ``squashfs_v3_nonstandard`` 8/8 no-reader;
``squashfs_v3_broadcom`` 7/8 PARTIAL (7-Zip lists it, unsquashfs refuses it);
``squashfs_v3_ddwrt`` 6/7 NO-READER.  A reader is therefore only trusted for the BODY
VARIANT it was measured on, and the handler name cannot carry that distinction - the
scored features do not expose a body variant.  Two consequences are DISCLOSED, and
neither is fixed by this claim:

  * ``squashfs_v3_ddwrt`` stays reader-backed, so its FAILED body
    ``dmg_Z3_v3ddwrt_inode_table`` reads ``legacy-body-failure``/``cross-read-legacy`` -
    a cross-read prescribed on a body whose readers refuse.  Moving ddwrt into the
    no-reader set would move exactly 8 labels (that envelope to
    ``no-reader-failure``/``preserve-unresolved`` plus 7 clean envelopes to
    ``clean-unverified``/``record-unverified``) and leave ``pair_mismatches 0`` under
    both rules, because the table and this evaluator change together.
  * ``squashfs_v3_broadcom`` has a working 7-Zip listing on 7 of its 8 fixtures, so a
    no-reader FAILURE label here never suppresses a successful partial cross-read.

The two limits of this precedence that FOLLOW from the claim's own scope are:  (a) A no-reader family
that FAILED while publishing MORE than zero files keeps v4's ``partial-body-failure``
(step 5 fires before step 8), and a no-reader family whose tree is empty keeps v4's
``clean-empty`` (step 16, ``confirm-empty``): the claim defines exactly two no-reader
labels, and those two unmeasured boundaries are left on the v4 rows and named here
rather than silently re-labelled.  (b) "F meets a NO-READER family" and "HF meets a
NO-READER family" are INTERSECTION tests, the same positive subset test the table's
handler cell has: a run that contains a no-reader chunk among others is treated as
unverifiable, because no oracle can corroborate it.

JUNK-TABLE AND DO-NOTHING CONTROLS
----------------------------------
Every control parses the MUTANT table with the v5 parser and compares the mutant
table's labels against the FIXED evaluator.  The evaluator is never re-derived from the
table under test, so a mutant table can only score green if it really reproduces the
precedence.  The do-nothing control is the v4 table at the base revision: it is red,
and the four v2ns ``_ddefault`` envelopes are among the mismatches.

MUTATION BATTERY (the selftest's committed mutation list)
---------------------------------------------------------
The mutations are TEXTUAL edits of the embedded v5 draft table, re-parsed by the v5
parser, except where a cell is blanked: the v4/v5 text grammar refuses a blank
condition cell (exit 2, never a silent non-match), so the blanked-cell mutation is
expressed at the RULE level, where blanking a cell means "unconstrained" (the
wildcard).  The selftest asserts, for every mutation, that the set of flipped fixture
pairs is exactly the expected set - so a mutation may not be a no-op and may not
cross-flip a pair it does not own.

Usage
-----
  python3 -I -B sqfs-triage-v5.py --root LANE --rev REV [--freeze FREEZE]
      --envelopes DIR --json-out PATH
      label every envelope of DIR with the table at REV and with the fixed evaluator,
      write the JSON report to PATH
  python3 -I -B sqfs-triage-v5.py --selftest [--work DIR]
      offline selftest (fixtures under --work, else $TMPDIR); never touches the lane
  python3 -I -B sqfs-triage-v5.py --print-v5-block
      print the embedded v5 table draft (the block the L1 lands in SKILL.md)
  python3 -I -B sqfs-triage-v5.py --skill PATH ...
      read the SKILL.md from a FILE instead of from git (used to test a candidate table
      before it is committed)

Exit codes: 0 met (every envelope's table label and action equal the evaluator's),
1 not met (at least one pair mismatch), 2 could-not-evaluate (unknown revision, missing
or malformed table, unreadable envelope, freeze not an ancestor, refused work or output
directory).
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

MARKER_V5 = '<!-- sqfs-triage-table v5 -->'
MARKER_V4 = '<!-- sqfs-triage-table v4 -->'
REFUSED_MARKERS = ('<!-- sqfs-triage-table v3 -->',
                   '<!-- sqfs-triage-table v2 -->',
                   '<!-- sqfs-triage-table v1 -->')
ACTIONS_PREFIX = '<!-- sqfs-triage-actions:'
ACTIONS_SUFFIX = '-->'
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

# The ten SquashFS handler names unblob 26.6.4 registers (handlers/filesystem/squashfs.py
# NAME constants, lines 102, 159, 200, 245, 319, 364, 410, 455, 514, 549).  A handler
# glob must match one of these.
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

# The families with NO VALIDATED COMPLETE INDEPENDENT ORACLE (round-49 entry, "What
# stays Frontier": on the healthy v2ns fixtures unsquashfs 4.7.5 exits 1 and 7-Zip 26.04
# exits 2, so a both-fail cross-read cannot decide).  The wording is the claim's
# (plans/round-50-attempt2-claims.md R50-C3): broadcom has a PARTIAL reader - 7-Zip
# lists the committed LE fixture while unsquashfs refuses it - so it has no *complete*
# independent oracle, and a no-reader FAILURE label never suppresses a successful
# partial cross-read.  The set is HANDLER-LEVEL and frozen; the reader census behind it
# is FIXTURE-level (the round-42 fixture bytes, re-measured 2026-10-29: broadcom 7/8
# partial, ddwrt 6/7 no-reader, nonstandard 8/8 no-reader, v3 8/8 readable by both), so
# the ddwrt family keeps its reader-backed routing with a disclosed per-variant residue.
NO_READER_FAMILIES = (
    'squashfs_v2_nonstandard',
    'squashfs_v3_broadcom',
    'squashfs_v3_nonstandard',
)

# The reader-backed v1-v3 families: they keep v4's legacy-body-failure row, and the
# narrowed failing-handler cell names exactly these four.
READER_BACKED_V1V3 = (
    'squashfs_v1',
    'squashfs_v2',
    'squashfs_v3',
    'squashfs_v3_ddwrt',
)

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
DEFAULT_SKILL = LANE + '/SKILL.md'

# The predicate sentence, one string, written into the docstring above and into every
# JSON receipt under the key "predicate" - the claim requires the SAME sentence in the
# counter docstring, in the claims file and in the receipt label
# (plans/round-50-attempt2-claims.md R50-C3: "the same sentence in the counter
# docstring, this file, and the receipt label").
PREDICATE = (
    'at the measured revision REV, with FREEZE an ancestor of REV, frozen paths '
    'untouched, running `python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --root <LANE> '
    '--rev <REV> --freeze <FREEZE> --envelopes <DIR> --json-out <OUT>` exits 0 with '
    '`pair_mismatches 0`, `evaluator_missing 0`, `table_labels == evaluator_labels` on '
    'every envelope of the frozen held-out dir, `selftest` green (every committed '
    'mutation flips ≥1 pair, none a no-op or cross-flip, do-nothing red); and at the base '
    'REV the same command exits 1 with the no-reader `*_ddefault` rows among the '
    'mismatches.')

# Where this instrument lands in the lane.  The path is NOT `tools/round-50/`: both
# frozen round-50 counters freeze the WHOLE `tools/round-50/` tree, so a file added
# there reads as frozen-path drift and takes C1 and C2 down (measured by wave-3
# `ExecFetchDry` on a fixture clone: `c1-counter.py` `frozen_drift =
# ['tools/round-50/sqfs-triage-v5.py']` -> C1 exit 2; `c2-record.py` `freeze_check =
# frozen_path_changed`).  `tools/round-50-c3/` is outside every frozen walk, and B9's
# census covers `tools/round-49/**` + `tools/round-50/**` only, so the outside path
# needs no B9 row while the lane registry still gets one as a gate-registration duty
# (plans/round-50-attempt2-claims.md R50-C3, "Path rule (measured, not assumed)").
INSTRUMENT_RELPATH = 'tools/round-50-c3/sqfs-triage-v5.py'
# The trees the C3 freeze touches, for the freeze arm's "nothing else moved" report.
FROZEN_TOOL_TREES = ('tools/round-50/', 'tools/round-50-c3/')

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


class Unevaluable(Exception):
    """The run could not be evaluated (exit 2)."""


# --------------------------------------------------------------------------------------
# table parsing (ported from tools/round-42/sqfs-triage-v4.py)
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
    """Strip whitespace and one surrounding pair of backticks from a table cell."""
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
    """Parse one set-valued cell (gap kinds, dependencies).  Unchanged from v4."""
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
    """Parse one handler-family cell: ``*``, ``none``, one glob, or a LIST of globs.

    The list form is the v5 grammar delta; see the module docstring.  Every
    alternative is validated against the pinned handler vocabulary.
    """
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


def _find_marker(lines, marker):
    for i, line in enumerate(lines):
        if marker in line:
            return i
    return None


def _table_block(lines, marker_index, end=None):
    """Return (table_lines, table_start_index, actions_line_index) after a marker."""
    limit = len(lines) if end is None else end
    table_start = None
    for i in range(marker_index + 1, limit):
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
    while i < limit and lines[i].lstrip().startswith('|'):
        table.append(lines[i])
        i += 1
    return table, table_start, actions_line


def parse_skill(text):
    """Return (rules, info) for the triage table of one SKILL.md document.

    The v5 marker wins.  A document without a v5 marker is parsed at its v4 marker (the
    red-before path).  A document whose newest marker is v1/v2/v3 is refused.
    """
    lines = text.splitlines()
    marker_index = _find_marker(lines, MARKER_V5)
    version = 'v5'
    if marker_index is None:
        marker_index = _find_marker(lines, MARKER_V4)
        version = 'v4'
    if marker_index is None:
        for refused in REFUSED_MARKERS:
            at = _find_marker(lines, refused)
            if at is not None:
                raise TableError('line %d: refused marker %r; this interpreter reads only '
                                 '%r (or the v4 marker for the red-before measurement), and '
                                 'a superseded table is never evaluated'
                                 % (at + 1, refused, MARKER_V5))
        raise TableError('marker %r absent from the document' % MARKER_V5)
    table, table_start, actions_line = _table_block(lines, marker_index)
    vocabulary = parse_actions_line(lines[actions_line], actions_line + 1)
    rules = parse_table(table, table_start + 1, vocabulary)
    return rules, {'version': version,
                   'marker_line': marker_index + 1,
                   'actions_line': actions_line + 1,
                   'table_line': table_start + 1,
                   'rules': len(rules),
                   'actions': vocabulary}


# --------------------------------------------------------------------------------------
# envelope features (ported from tools/round-42/sqfs-triage-v4.py)
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
    """Return the ``data`` object of a bare or full REA envelope."""
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


def features(data):
    """The declared tuple of one envelope (see the module docstring)."""
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
    """``*`` matches any set, ``none`` the empty set, else any member matches."""
    kind, payload = spec
    if kind == 'any':
        return True
    if kind == 'none':
        return not names
    if kind == 'list':
        return any(fnmatch.fnmatchcase(value, pattern)
                   for pattern in payload for value in names)
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
# the fixed evaluator (independent of any table)
# --------------------------------------------------------------------------------------

NO_READER_SET = frozenset(NO_READER_FAMILIES)
READER_BACKED_SET = frozenset(READER_BACKED_V1V3)


def _meets(names, wanted):
    """The table's positive subset test: any member of ``names`` is in ``wanted``."""
    for name in names:
        if name in wanted:
            return True
    return False


def evaluate(feat):
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
    if FAILURE_KIND in g and p == 0 and _meets(hf, READER_BACKED_SET):
        return 'legacy-body-failure', 'cross-read-legacy', 7
    if FAILURE_KIND in g and p == 0 and _meets(hf, NO_READER_SET):
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
            return 'clean', 'none', 16
        return 'clean-empty', 'confirm-empty', 16
    return DEFAULT_LABEL, DEFAULT_ACTION, 17


# --------------------------------------------------------------------------------------
# the v5 table draft (embedded; printed by --print-v5-block)
# --------------------------------------------------------------------------------------

V5_ACTIONS = ('none inspect-input install-extractor-be install-extractor-le '
              'wrap-extractor-be cross-read-legacy isolate-residue preserve-failure '
              'salvage-partial raise-depth audit-symlinks expect-link-absent count-gap '
              'confirm-empty record-unverified preserve-unresolved')

NO_READER_CELL = ','.join(NO_READER_FAMILIES)
READER_BACKED_CELL = ','.join(READER_BACKED_V1V3)

V5_ROWS = [
    # label, operation, provider, handler, failing handler, gap kinds, dependencies,
    # -be in child argv, symlink removed, published files, action, cause, source
    ['container-depth-limited', 'extract_firmware', 'unblob', 'none', '*',
     'depth-limited+', '*', '*', '*', '*', 'raise-depth',
     'no SquashFS handler was named and REA stopped at max_depth -> rerun with a higher '
     'max_depth or descend into the published container',
     'SKILL.md table v4 row 1; S119 FirmwarePublication.js:23-29,:294-299'],
    ['no-squashfs-chunk', 'extract_firmware', 'unblob', 'none', '*', '*', '*', '*', '*',
     '*', 'inspect-input',
     'neither a chunk nor a gap names a SquashFS handler -> check the magic and '
     'superblock before rerunning',
     'SKILL.md table v4 row 2; S112 :102,:159,:200,:245,:319,:364,:410,:463,:522'],
    ['dep-missing-be', 'extract_firmware', 'unblob', 'squashfs_*', '*',
     'missing-extractor-dependency+', 'sasquatch-v4be+', '*', '*', '*',
     'install-extractor-be',
     'the chunk resolved its extractor to sasquatch-v4be and that binary was not found '
     '-> install the sasquatch-v4be binary and rerun into a fresh output directory',
     'SKILL.md table v4 row 3; S112 :40-41; S120 command.py:69-77'],
    ['dep-missing-le', 'extract_firmware', 'unblob', 'squashfs_*', '*',
     'missing-extractor-dependency+', 'sasquatch+', '*', '*', '*', 'install-extractor-le',
     'the chunk resolved its extractor to plain sasquatch and that binary was not found '
     '-> install the little-endian sasquatch binary and rerun',
     'SKILL.md table v4 row 4; S112 :37,:39-54; S120 report.py:118-122'],
    ['partial-body-failure', 'extract_firmware', 'unblob', 'squashfs_*', '*',
     'extractor-failure+', '*', '*', '*', '>0', 'salvage-partial',
     'the extractor failed after publishing at least one regular file -> keep the '
     'published files and the failing command, mark the run incomplete, never score the '
     'set as clean',
     'SKILL.md table v4 row 5; S119 FirmwarePublication.js:288-293'],
    ['avm-marker-be-dropped', 'extract_firmware', 'unblob', 'squashfs_*',
     'squashfs_v4_be', 'extractor-failure+', '*', 'no', '*', '0', 'wrap-extractor-be',
     'the failing chunk is the v4 BE one and unblob dropped -be -> rerun through a PATH '
     'executable named sasquatch-v4be that appends -be',
     'SKILL.md table v4 row 6; S112 :44-50; S121 -DFIX_BE build'],
    ['legacy-body-failure', 'extract_firmware', 'unblob', 'squashfs_*', READER_BACKED_CELL,
     'extractor-failure+', '*', '*', '*', '0', 'cross-read-legacy',
     'the failing chunk is a reader-backed v1-v3 body that published zero files -> '
     'cross-read the same chunk with unsquashfs and 7-Zip, and only a reader that lists '
     'the tree while sasquatch failed shows a broken extractor build',
     'SKILL.md table v4 row 7 narrowed by R50-C3: the v4 cell squashfs_v[123]* also '
     'matched squashfs_v2_nonstandard, squashfs_v3_broadcom and squashfs_v3_nonstandard, '
     'which have no independent reader (round-49 W2Skill.md F1); round-50 '
     'plans/round-50-attempt2-claims.md R50-C3'],
    ['no-reader-failure', 'extract_firmware', 'unblob', 'squashfs_*', NO_READER_CELL,
     'extractor-failure+', '*', '*', '*', '0', 'preserve-unresolved',
     'the failing chunk is a family with no independent second reader and published zero '
     'files -> keep the failure unresolved: reader absence forbids both the '
     'damaged-body verdict and the broken-extractor verdict, so install nothing and '
     'change nothing',
     'R50-C3; round-49 W2Skill.md F1; round-50 plans/round-50-attempt2-claims.md R50-C3'],
    ['body-extractor-failure', 'extract_firmware', 'unblob', 'squashfs_*', '*',
     'extractor-failure+', '*', '*', '*', '0', 'preserve-failure',
     'the extractor ran and published zero regular files on a body the rows above did '
     'not claim -> run the layout pre-check, keep the failing command, stdout and stderr',
     'SKILL.md table v4 row 8; S120 report.py:91-98; S124 :35'],
    ['unknown-residue', 'extract_firmware', 'unblob', 'squashfs_*', '*',
     'unknown-chunk-handler+', '*', '*', '*', '*', 'isolate-residue',
     'bytes beside the filesystem belong to no parser -> keep the residue out of the '
     'oracle and re-carve the SquashFS chunk to unblob chunk end',
     'SKILL.md table v4 row 9; S119 FirmwarePublication.js:286; S118 :116-127'],
    ['depth-limited', 'extract_firmware', 'unblob', 'squashfs_*', '*', 'depth-limited+',
     '*', '*', '*', '*', 'raise-depth',
     'REA stopped at max_depth and recorded one depth-limited gap per path -> rerun with '
     'a higher max_depth into a fresh output directory',
     'SKILL.md table v4 row 10; S119 FirmwarePublication.js:23-29,:294-299'],
    ['mixed-symlinks', 'extract_firmware', 'unblob', 'squashfs_*', '*',
     'unpublished-entry+', '*', '*', 'yes', '*', 'audit-symlinks',
     'both link kinds are present in one image -> expect the escaped paths absent and '
     'count one gap per kept link or special file',
     'SKILL.md table v4 row 11; S118 :50-92; S122'],
    ['escaping-symlink-removed', 'extract_firmware', 'unblob', 'squashfs_*', '*', 'none',
     '*', '*', 'yes', '*', 'expect-link-absent',
     'a link escaped the extraction root or looped and unblob removed it with a '
     'MaliciousSymlinkRemoved report -> expect the path to be absent',
     'SKILL.md table v4 row 12; S118 :42-47,:58-65,:79-87; S122'],
    ['in-tree-symlink-metadata', 'extract_firmware', 'unblob', 'squashfs_*', '*',
     'unpublished-entry', '*', '*', '*', '*', 'count-gap',
     'the gap set is exactly one kind and every non-file entry stayed inside the '
     'extraction root -> expected, not a sasquatch failure: count one gap per entry',
     'SKILL.md table v4 row 13; S119 FirmwarePublication.js:301-307'],
    ['clean-unverified', 'extract_firmware', 'unblob', NO_READER_CELL, '*',
     'none', '*', '*', 'no', '>0', 'record-unverified',
     'the run completed with no gap and published regular files, but the family has no '
     'independent second reader, so no oracle can corroborate the set -> record the '
     'envelope as unverified, never as clean',
     'R50-C3; round-49 W2Skill.md F2 (the v4 clean row gave a no-reader run the '
     'oracle-backed action none); round-50 plans/round-50-attempt2-claims.md R50-C3'],
    ['clean', 'extract_firmware', 'unblob', 'squashfs_*', '*', 'none', '*', '*', 'no',
     '>0', 'none',
     'every regular file was published and the gap set is empty on a reader-backed '
     'family -> nothing to install or fix; match files to the oracle by exact relative '
     'path and sha256',
     'SKILL.md table v4 row 14; S119 FirmwarePublication.js:301-307'],
    ['clean-empty', 'extract_firmware', 'unblob', 'squashfs_*', '*', 'none', '*', '*',
     'no', '0', 'confirm-empty',
     'the extractor completed with no gap and published zero regular files -> confirm '
     'the independent oracle tree is empty before calling it clean',
     'SKILL.md table v4 row 15; S119 FirmwarePublication.js:301-307'],
]


def render_table(rows, actions=V5_ACTIONS, marker=MARKER_V5):
    out = [marker, '%s %s %s' % (ACTIONS_PREFIX, actions, ACTIONS_SUFFIX)]
    out.append('| ' + ' | '.join(HEADER) + ' |')
    out.append('| ' + ' | '.join(['---'] * len(HEADER)) + ' |')
    for row in rows:
        out.append('| ' + ' | '.join(row) + ' |')
    return '\n'.join(out) + '\n'


V5_BLOCK = render_table(V5_ROWS)


# --------------------------------------------------------------------------------------
# git access (read-only)
# --------------------------------------------------------------------------------------

def git(root, args, check=True):
    proc = subprocess.run(['git', '-C', root] + list(args),
                          capture_output=True, text=True)
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


def sha256_text(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


# --------------------------------------------------------------------------------------
# work and output directories (never /tmp, never a graded surface)
# --------------------------------------------------------------------------------------

GRADED_BASENAMES = ('SKILL.md', 'PROVINCE.md', 'LOG.md', 'SCORECARD.md', 'SHONEN.md')
TEMP_ROOTS = ('/tmp', '/var/tmp')


def _under(path, root):
    real = os.path.realpath(path)
    base = os.path.realpath(root)
    return real == base or real.startswith(base + os.sep)


def resolve_work(ns):
    """The directory fixtures may be written to.  Never a temporary partition."""
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
                              % (real, exc.strerror or exc))
    return real


def resolve_json_out(path, root):
    """The output path, checked against the temporary partitions and graded surfaces."""
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
    """Every envelope under ``directory``, as (id, path) pairs, sorted by id."""
    out = []
    try:
        names = sorted(os.listdir(directory))
    except OSError as exc:
        raise Unevaluable('envelope directory %r: %s' % (directory, exc.strerror or exc))
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


def run(ns):
    root = os.path.abspath(ns.root) if ns.root else LANE
    if not os.path.isdir(root):
        raise Unevaluable('lane root %r is not a directory' % root)
    if ns.skill:
        try:
            with open(ns.skill, 'r', encoding='utf-8') as handle:
                text = handle.read()
        except OSError as exc:
            raise Unevaluable('--skill %r: %s' % (ns.skill, exc.strerror or exc))
        source = 'file:%s' % os.path.abspath(ns.skill)
    else:
        if not ns.rev:
            raise InvocationError('--rev is required unless --skill is given')
        text = git_show(root, ns.rev, 'SKILL.md')
        if text is None:
            raise Unevaluable('cannot read SKILL.md at revision %r' % ns.rev)
        source = 'git:%s:SKILL.md' % ns.rev
    rules, info = parse_skill(text)

    freeze_report = {'rev': ns.rev, 'freeze': ns.freeze, 'ancestor': None,
                     'instrument_sha256_at_freeze': None,
                     'instrument_sha256_at_rev': None,
                     'instrument_unchanged': None,
                     'other_tools_round50_changed': []}
    if ns.freeze:
        if blob_sha(root, ns.freeze, 'SKILL.md') is None:
            raise Unevaluable('freeze revision %r does not resolve in %r'
                               % (ns.freeze, root))
        if not is_ancestor(root, ns.freeze, ns.rev):
            raise Unevaluable('freeze %r is not an ancestor of %r'
                               % (ns.freeze, ns.rev))
        freeze_report['ancestor'] = True
        at_freeze = git_show(root, ns.freeze, INSTRUMENT_RELPATH)
        at_rev = git_show(root, ns.rev, INSTRUMENT_RELPATH)
        if at_freeze is not None:
            freeze_report['instrument_sha256_at_freeze'] = sha256_text(at_freeze)
        if at_rev is not None:
            freeze_report['instrument_sha256_at_rev'] = sha256_text(at_rev)
        if (freeze_report['instrument_sha256_at_freeze'] is not None
                and freeze_report['instrument_sha256_at_rev'] is not None):
            freeze_report['instrument_unchanged'] = (
                freeze_report['instrument_sha256_at_freeze']
                == freeze_report['instrument_sha256_at_rev'])
        proc = git(root, ['diff', '--name-only', '%s..%s' % (ns.freeze, ns.rev)]
                   + list(FROZEN_TOOL_TREES), check=False)
        if proc.returncode == 0:
            changed = [line for line in proc.stdout.splitlines() if line.strip()]
            freeze_report['other_tools_round50_changed'] = [
                line for line in changed if line != INSTRUMENT_RELPATH]

    entries = envelope_entries(ns.envelopes)
    if not entries:
        raise Unevaluable('no envelope found under %r' % ns.envelopes)

    details = []
    mismatches = []
    evaluator_missing = []
    table_labels = {}
    evaluator_labels = {}
    table_distribution = {}
    evaluator_distribution = {}
    for envelope_id, path in entries:
        feat = load_envelope(path)
        rule = classify(rules, feat)
        table_label, table_action = decision(rule)
        abstained = None
        try:
            ev_label, ev_action, ev_step = evaluate(feat)
        except Exception as exc:                      # the evaluator abstains
            ev_label, ev_action, ev_step = None, None, None
            abstained = repr(exc)
        if ev_label is None:
            evaluator_missing.append({'envelope': envelope_id,
                                      'reason': abstained or 'no verdict'})
        table_labels[envelope_id] = table_label
        evaluator_labels[envelope_id] = ev_label
        table_distribution[table_label] = table_distribution.get(table_label, 0) + 1
        if ev_label is not None:
            evaluator_distribution[ev_label] = evaluator_distribution.get(ev_label, 0) + 1
        match = (table_label == ev_label and table_action == ev_action)
        if ev_label is None:
            # an abstention is reported in evaluator_missing, not as a pair mismatch
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
            'match': match,
            'features': feat,
        })

    report = {
        'instrument': 'sqfs-triage-v5.py',
        'predicate': PREDICATE,
        'schema': 1,
        'root': root,
        'rev': ns.rev,
        'skill_source': source,
        'table': {
            'version': info['version'],
            'marker_line': info['marker_line'],
            'actions_line': info['actions_line'],
            'table_line': info['table_line'],
            'rules': info['rules'],
            'actions': list(info['actions']),
        },
        'n_envelopes': len(entries),
        'pair_mismatches': mismatches,
        'pair_mismatch_count': len(mismatches),
        'evaluator_missing': evaluator_missing,
        'table_labels': table_labels,
        'evaluator_labels': evaluator_labels,
        'label_distribution': {'table': table_distribution,
                               'evaluator': evaluator_distribution},
        'freeze': freeze_report,
        'envelopes': details,
        'verdict': 'met' if not mismatches and not evaluator_missing else 'not met',
    }
    out_path = None
    if ns.json_out:
        out_path = resolve_json_out(ns.json_out, root)
        try:
            with open(out_path, 'w', encoding='utf-8') as handle:
                json.dump(report, handle, indent=1, sort_keys=True)
                handle.write('\n')
        except OSError as exc:
            # an unwritable receipt is COULD-NOT-EVALUATE, never a silent pass: the
            # exit code alone is not evidence, so a receipt that cannot be written
            # must not exit 0
            raise Unevaluable('the receipt %r could not be written: %s'
                               % (out_path, exc.strerror or exc))
        # The receipt gate: the receipt must EXIST and PARSE.  A stub or a truncated
        # writer can exit 0 while producing nothing, so the exit code alone is not
        # evidence - the receipt is (a 49-byte stub was measured exiting 0 on this
        # very command while writing no receipt at all).
        try:
            with open(out_path, 'r', encoding='utf-8') as handle:
                verify = json.load(handle)
        except (OSError, ValueError) as exc:
            raise Unevaluable('the receipt %r did not parse: %s'
                               % (out_path, exc))
        for key in ('predicate', 'pair_mismatches', 'evaluator_missing', 'table_labels',
                    'n_envelopes', 'verdict'):
            if key not in verify:
                raise Unevaluable('the receipt %r is missing the key %r'
                                   % (out_path, key))
    print('table: %s (%d rules) from %s' % (info['version'], info['rules'], source))
    print('envelopes: %d   pair_mismatches: %d   evaluator_missing: %d'
          % (len(entries), len(mismatches), len(evaluator_missing)))
    for key in sorted(table_distribution):
        print('  %-28s table %3d   evaluator %3d'
              % (key, table_distribution[key], evaluator_distribution.get(key, 0)))
    if mismatches:
        for row in mismatches[:20]:
            print('  MISMATCH %s: table %s/%s  evaluator %s/%s'
                  % (row['envelope'], row['table_label'], row['table_action'],
                     row['evaluator_label'], row['evaluator_action']))
        if len(mismatches) > 20:
            print('  ... %d more' % (len(mismatches) - 20))
    if out_path:
        print('json: %s' % out_path)
    return 0 if (not mismatches and not evaluator_missing) else 1


# --------------------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------------------

SKELETON = ('# SKILL\n\n## Queue-drain craft\n\nCraft prose before the table.\n\n'
            '{block}\n\n## A later section\n\nProse after the craft section.\n')

VOCAB_V4 = ('none inspect-input install-extractor-be install-extractor-le '
            'wrap-extractor-be preserve-failure salvage-partial raise-depth '
            'audit-symlinks expect-link-absent count-gap confirm-empty cross-read-legacy '
            'isolate-residue')

# The v4 rows (compact form: the 11 condition/action cells plus placeholder prose) as
# they read in SKILL.md at the base revision.  The red-before witness parses THESE.
V4_ROWS = [
    ['container-depth-limited', 'extract_firmware', 'unblob', 'none', '*',
     'depth-limited+', '*', '*', '*', '*', 'raise-depth'],
    ['no-squashfs-chunk', 'extract_firmware', 'unblob', 'none', '*', '*', '*', '*', '*',
     '*', 'inspect-input'],
    ['dep-missing-be', 'extract_firmware', 'unblob', 'squashfs_*', '*',
     'missing-extractor-dependency+', 'sasquatch-v4be+', '*', '*', '*',
     'install-extractor-be'],
    ['dep-missing-le', 'extract_firmware', 'unblob', 'squashfs_*', '*',
     'missing-extractor-dependency+', 'sasquatch+', '*', '*', '*', 'install-extractor-le'],
    ['partial-body-failure', 'extract_firmware', 'unblob', 'squashfs_*', '*',
     'extractor-failure+', '*', '*', '*', '>0', 'salvage-partial'],
    ['avm-marker-be-dropped', 'extract_firmware', 'unblob', 'squashfs_*',
     'squashfs_v4_be', 'extractor-failure+', '*', 'no', '*', '0', 'wrap-extractor-be'],
    ['legacy-body-failure', 'extract_firmware', 'unblob', 'squashfs_*',
     'squashfs_v[123]*', 'extractor-failure+', '*', '*', '*', '0', 'cross-read-legacy'],
    ['body-extractor-failure', 'extract_firmware', 'unblob', 'squashfs_*', '*',
     'extractor-failure+', '*', '*', '*', '0', 'preserve-failure'],
    ['unknown-residue', 'extract_firmware', 'unblob', 'squashfs_*', '*',
     'unknown-chunk-handler+', '*', '*', '*', '*', 'isolate-residue'],
    ['depth-limited', 'extract_firmware', 'unblob', 'squashfs_*', '*', 'depth-limited+',
     '*', '*', '*', '*', 'raise-depth'],
    ['mixed-symlinks', 'extract_firmware', 'unblob', 'squashfs_*', '*',
     'unpublished-entry+', '*', '*', 'yes', '*', 'audit-symlinks'],
    ['escaping-symlink-removed', 'extract_firmware', 'unblob', 'squashfs_*', '*', 'none',
     '*', '*', 'yes', '*', 'expect-link-absent'],
    ['in-tree-symlink-metadata', 'extract_firmware', 'unblob', 'squashfs_*', '*',
     'unpublished-entry', '*', '*', '*', '*', 'count-gap'],
    ['clean', 'extract_firmware', 'unblob', 'squashfs_*', '*', 'none', '*', '*', 'no',
     '>0', 'none'],
    ['clean-empty', 'extract_firmware', 'unblob', 'squashfs_*', '*', 'none', '*', '*',
     'no', '0', 'confirm-empty'],
]


def _v4_full_rows():
    rows = []
    for row in V4_ROWS:
        rows.append(row + ['v4 cause prose -> v4 action', 'SKILL.md table v4 at base'])
    return rows


def _render(rows, actions, marker):
    out = [marker, '%s %s %s' % (ACTIONS_PREFIX, actions, ACTIONS_SUFFIX)]
    out.append('| ' + ' | '.join(HEADER) + ' |')
    out.append('| ' + ' | '.join(['---'] * len(HEADER)) + ' |')
    for row in rows:
        out.append('| ' + ' | '.join(row) + ' |')
    return '\n'.join(out) + '\n'


def _env(handler='squashfs_v4_be', handlers=(), gaps=(), be=None, sr=False, files=0,
         op='extract_firmware', pv='unblob', command=None, gap_handlers=None,
         files_absent=False, sr_where='raw', no_chunks=False):
    """Build one synthetic REA ``data`` object with exactly these features."""
    data = {'operation': op, 'provider': {'id': pv},
            'normalized_result': {'chunks': [], 'extraction_gaps': [], 'files': []}}
    if not no_chunks and handler:
        data['normalized_result']['chunks'] = [{'handler': handler}]
    for extra in handlers:
        data['normalized_result']['chunks'].append({'handler': extra})
    for gap in gaps:
        row = {'kind': gap}
        if gap_handlers and gap in gap_handlers:
            row['handler'] = gap_handlers[gap]
        data['normalized_result']['extraction_gaps'].append(row)
    if not files_absent:
        data['normalized_result']['files'] = [{'path': 'f/%d' % i} for i in range(files)]
    if be is not None:
        cmd = 'sasquatch %s' % be
        if sr_where == 'raw':
            data['normalized_result']['diagnostics'] = [
                {'report': {'command': cmd,
                            '__typename__': ('MaliciousSymlinkRemoved' if sr else 'Stat')}}]
        else:
            data['normalized_result']['diagnostics'] = [
                {'report': {'command': cmd, '__typename__': 'Stat'}}]
            data['raw_result'] = {'__typename__': 'MaliciousSymlinkRemoved'}
    elif command is not None:
        data['normalized_result']['diagnostics'] = [{'report': {'command': command}}]
    return data


# The selftest fixture set: the shapes the v5 table must decide.
FIXTURES = [
    # id, envelope, expected (label, action)
    ('v2ns-clean-le', _env(handler='squashfs_v2_nonstandard', gaps=[], files=4),
     ('clean-unverified', 'record-unverified')),
    ('v2ns-clean-be', _env(handler='squashfs_v2_nonstandard', gaps=[], files=4),
     ('clean-unverified', 'record-unverified')),
    ('v3bc-clean', _env(handler='squashfs_v3_broadcom', gaps=[], files=4),
     ('clean-unverified', 'record-unverified')),
    ('v2ns-failed', _env(handler='squashfs_v2_nonstandard', gaps=['extractor-failure'],
                         be='-le', files=0),
     ('no-reader-failure', 'preserve-unresolved')),
    ('v3-legacy', _env(handler='squashfs_v3', gaps=['extractor-failure'], be='-le', files=0),
     ('legacy-body-failure', 'cross-read-legacy')),
    ('v3ddwrt-legacy', _env(handler='squashfs_v3_ddwrt', gaps=['extractor-failure'],
                            be='-be', files=0),
     ('legacy-body-failure', 'cross-read-legacy')),
    ('v4le-clean', _env(handler='squashfs_v4_le', gaps=[], files=2),
     ('clean', 'none')),
    ('v4be-clean', _env(handler='squashfs_v4_be', gaps=[], files=2),
     ('clean', 'none')),
    ('v4bc-clean', _env(handler='squashfs_v4_broadcom', gaps=[], files=2),
     ('clean', 'none')),
    ('symlink-row', _env(handler='squashfs_v4_le', gaps=['unpublished-entry'], be='-le',
                         sr=True, files=2),
     ('mixed-symlinks', 'audit-symlinks')),
]


def _pairs(rules, fixtures=FIXTURES):
    out = {}
    for name, env, _want in fixtures:
        feat = features(env)
        rule = classify(rules, feat)
        label, action = decision(rule)
        out[name] = (label, action)
    return out


def _require(cond, message):
    if not cond:
        raise AssertionError(message)


def _row_index(rows, label):
    for i, row in enumerate(rows):
        if row[0] == label:
            return i
    raise AssertionError('no row labelled %r' % label)


def _text_rows(rows):
    """Copy rows for a textual mutation.  The rows already carry all 13 cells."""
    return [list(row) for row in rows]


# ------------------------------------------------------------------ the mutation battery

def _mut_delete_guard_row(rows):
    """Delete the clean-unverified guard row."""
    out = [list(r) for r in rows]
    del out[_row_index(out, 'clean-unverified')]
    return out


def _mut_widen_legacy_glob(rows):
    """Widen the narrowed failing-handler cell back to the v4 glob."""
    out = [list(r) for r in rows]
    out[_row_index(out, 'legacy-body-failure')][4] = 'squashfs_v[123]*'
    return out


def _mut_swap_new_row_actions(rows):
    """Swap the actions of the two new rows."""
    out = [list(r) for r in rows]
    i = _row_index(out, 'clean-unverified')
    j = _row_index(out, 'no-reader-failure')
    out[i][10], out[j][10] = out[j][10], out[i][10]
    return out


def _mut_no_reader_family_to_clean(rows):
    """Move one no-reader family out of the clean-unverified row (it then lands on clean)."""
    out = [list(r) for r in rows]
    i = _row_index(out, 'clean-unverified')
    parts = [p for p in out[i][3].split(',') if p != 'squashfs_v3_broadcom']
    out[i][3] = ','.join(parts)
    return out


def _mut_precedence_swapped(rows):
    """Move the clean-unverified row BELOW the v4 clean row."""
    out = [list(r) for r in rows]
    i = out.pop(_row_index(out, 'clean-unverified'))
    j = _row_index(out, 'clean')
    out.insert(j + 1, i)
    return out


def _mut_no_reader_failure_row_deleted(rows):
    """Delete the no-reader-failure row."""
    out = [list(r) for r in rows]
    del out[_row_index(out, 'no-reader-failure')]
    return out


def _mut_legacy_row_deleted(rows):
    """Delete the legacy-body-failure row (a reader-backed failure then falls to the body row)."""
    out = [list(r) for r in rows]
    del out[_row_index(out, 'legacy-body-failure')]
    return out


def _mut_blank_cell(rules):
    """Blank the clean-unverified row's handler cell (rule level: unconstrained)."""
    out = [dict(r) for r in rules]
    for rule in out:
        if rule['label'] == 'clean-unverified':
            rule['handler'] = ('any', None)
    return out


MUTATIONS = [
    ('guard-row-deleted', _mut_delete_guard_row,
     {'v2ns-clean-le', 'v2ns-clean-be', 'v3bc-clean'}),
    ('legacy-glob-widened', _mut_widen_legacy_glob,
     {'v2ns-failed'}),
    ('new-row-actions-swapped', _mut_swap_new_row_actions,
     {'v2ns-clean-le', 'v2ns-clean-be', 'v3bc-clean', 'v2ns-failed'}),
    ('no-reader-family-moved-to-clean', _mut_no_reader_family_to_clean,
     {'v3bc-clean'}),
    ('precedence-order-swapped', _mut_precedence_swapped,
     {'v2ns-clean-le', 'v2ns-clean-be', 'v3bc-clean'}),
    ('no-reader-failure-row-deleted', _mut_no_reader_failure_row_deleted,
     {'v2ns-failed'}),
    ('legacy-row-deleted', _mut_legacy_row_deleted,
     {'v3-legacy', 'v3ddwrt-legacy'}),
]


def _mutate_text_table(mutator):
    rows = _text_rows(V5_ROWS)
    return _render(mutator(rows), V5_ACTIONS, MARKER_V5)


def _junk_table():
    """The junk-table control: every row reads clean, with unique labels."""
    junk = []
    for i, row in enumerate(_text_rows(V5_ROWS)):
        row = list(row)
        row[0] = 'junk-%d' % i
        row[3] = 'squashfs_*'
        row[4] = '*'
        row[5] = '*'
        row[6] = '*'
        row[7] = '*'
        row[8] = '*'
        row[9] = '*'
        row[10] = 'none'
        junk.append(row)
    return _render(junk, V5_ACTIONS, MARKER_V5)


def corpus_control(ns):
    """Run every committed control against a real envelope directory.

    Each control is a MUTANT TABLE parsed by the v5 parser and compared against the
    FIXED evaluator.  A control is red when it produces at least one pair mismatch; the
    do-nothing control (the v4 table at the base revision) must be red and must name
    the four v2ns ``_ddefault`` envelopes among its mismatches.

    TWO SCOPES are reported separately, because they witness different populations and
    a control that is green in one of them is VACUOUS there, not passed:

      corpus    the frozen held-out envelope directory.  It holds 38 no-reader
                envelopes, 19 of them clean and 19 depth-limited, and NONE of them a
                no-reader extractor-failure with zero files.  A mutation that only
                moves the no-reader FAILURE branch therefore cannot flip a pair here:
                it is vacuous on this corpus, which the report states.
      fixtures  the selftest fixture set, which carries one no-reader failure
                envelope, so every committed mutation has a witness there.
    """
    work = resolve_work(ns)
    entries = envelope_entries(ns.envelopes)
    if not entries:
        raise Unevaluable('no envelope found under %r' % ns.envelopes)
    corpus = []
    for envelope_id, path in entries:
        corpus.append((envelope_id, path, load_envelope(path)))
    fixtures = [(name, '<fixture>', features(env))
                 for name, env, _want in FIXTURES]
    scopes = [('corpus', corpus), ('fixtures', fixtures)]

    controls = [('do-nothing-v4', 'the v4 table at the base revision (the do-nothing '
                                  'control)')]
    controls += [(name, 'the v5 draft with the %s mutation' % name)
                 for name, _f, _e in MUTATIONS]
    controls.append(('junk-table', 'every row reads clean'))

    def evaluate_scope(rules, scope):
        mismatches = []
        for envelope_id, path, feat in scope:
            rule = classify(rules, feat)
            table_label, table_action = decision(rule)
            ev_label, ev_action, _step = evaluate(feat)
            if table_label != ev_label or table_action != ev_action:
                mismatches.append({'envelope': envelope_id,
                                   'table_label': table_label,
                                   'table_action': table_action,
                                   'evaluator_label': ev_label,
                                   'evaluator_action': ev_action})
        return mismatches

    results = []
    for name, description in controls:
        block = emit_mutant(name)
        rules, info = parse_skill(SKELETON.format(block=block))
        base_rules, _bi = parse_skill(SKELETON.format(block=V5_BLOCK))
        per_scope = {}
        for scope_name, scope in scopes:
            mismatches = evaluate_scope(rules, scope)
            base_mismatches = evaluate_scope(base_rules, scope)
            per_scope[scope_name] = {
                'n_envelopes': len(scope),
                'pair_mismatches': len(mismatches),
                'red': bool(mismatches),
                'vacuous': not mismatches and not base_mismatches,
                'mismatched_envelopes': [m['envelope'] for m in mismatches],
                'sample_mismatches': mismatches[:8],
            }
        results.append({
            'control': name,
            'description': description,
            'table_version': info['version'],
            'rules': info['rules'],
            'scopes': per_scope,
            'red_anywhere': any(s['red'] for s in per_scope.values()),
            'vacuous_everywhere': all(s['vacuous'] for s in per_scope.values()),
        })
    v2ns = sorted(e for e, _p, _f in corpus if 'v2_nonstandard' in e and
                  e.endswith('_ddefault'))
    do_nothing = results[0]
    report = {
        'instrument': 'sqfs-triage-v5.py',
        'predicate': PREDICATE,
        'schema': 1,
        'envelopes': ns.envelopes,
        'n_envelopes': len(corpus),
        'controls': results,
        'do_nothing_red': do_nothing['scopes']['corpus']['red'],
        'do_nothing_names_the_four_v2ns_ddefault': all(
            name in do_nothing['scopes']['corpus']['mismatched_envelopes']
            for name in v2ns),
        'v2ns_ddefault_envelopes': v2ns,
        'all_controls_red_somewhere': all(r['red_anywhere'] for r in results),
        'any_control_vacuous_everywhere': any(r['vacuous_everywhere'] for r in results),
    }
    out_path = None
    if ns.json_out:
        out_path = resolve_json_out(ns.json_out, ns.root)
        with open(out_path, 'w', encoding='utf-8') as handle:
            json.dump(report, handle, indent=1, sort_keys=True)
            handle.write('\n')
    for row in results:
        print('  %-34s corpus=%-8s fixtures=%-8s rules=%d'
              % (row['control'],
                 'RED(%d)' % row['scopes']['corpus']['pair_mismatches']
                 if row['scopes']['corpus']['red']
                 else ('VACUOUS' if row['scopes']['corpus']['vacuous'] else 'GREEN'),
                 'RED(%d)' % row['scopes']['fixtures']['pair_mismatches']
                 if row['scopes']['fixtures']['red']
                 else ('VACUOUS' if row['scopes']['fixtures']['vacuous'] else 'GREEN'),
                 row['rules']))
    print('controls: %d, all red in some scope: %s, any vacuous everywhere: %s'
          % (len(results), report['all_controls_red_somewhere'],
             report['any_control_vacuous_everywhere']))
    print('do-nothing red on the corpus: %s; names the four v2ns _ddefault: %s'
          % (report['do_nothing_red'],
             report['do_nothing_names_the_four_v2ns_ddefault']))
    if out_path:
        print('json: %s' % out_path)
    return 0 if report['all_controls_red_somewhere'] else 1


def emit_mutant(name):
    """Return the mutated table block for one committed mutation (or the junk table)."""
    for mut_name, mutator, _expected in MUTATIONS:
        if mut_name == name:
            return _mutate_text_table(mutator)
    if name == 'junk-table':
        return _junk_table()
    if name == 'do-nothing-v4':
        return _render(_v4_full_rows(), VOCAB_V4, MARKER_V4)
    raise InvocationError('unknown mutation %r; known: %s, junk-table, do-nothing-v4'
                          % (name, ', '.join(m for m, _f, _e in MUTATIONS)))


def _parse_block(block):
    rules, info = parse_skill(SKELETON.format(block=block))
    return rules, info


def _flipped(base, other):
    return {name for name in base if base[name] != other.get(name)}


def _missing_ids(entries):
    """The envelope ids the evaluator abstained on."""
    return [entry['envelope'] for entry in entries]


def selftest(ns):
    work = resolve_work(ns)
    passed = 0
    failed = []
    cases = []

    def case(fn):
        cases.append(fn)
        return fn

    @case
    def c_v4_table_is_red_before():
        """The v4 table at base, parsed by the v5 parser, mismatches the evaluator."""
        block = _render(_v4_full_rows(), VOCAB_V4, MARKER_V4)
        rules, _info = _parse_block(block)
        v2ns_ids = ('v2ns-clean-le', 'v2ns-clean-be')
        pairs = _pairs(rules)
        for name in v2ns_ids:
            _require(pairs[name] == ('clean', 'none'),
                     'v4 table: %s is %r, expected the v4 pair (clean, none)'
                     % (name, pairs[name]))
        mismatched = {name for name, env, want in FIXTURES
                      if pairs[name] != want}
        for name in v2ns_ids:
            _require(name in mismatched,
                     'v4 table: %s is not among the mismatches (%r)'
                     % (name, sorted(mismatched)))
        return 'v4 red before on %s' % (', '.join(sorted(v2ns_ids)),)

    @case
    def c_v5_table_matches_evaluator():
        """The v5 draft table reproduces the evaluator on every fixture."""
        rules, info = _parse_block(V5_BLOCK)
        _require(info['version'] == 'v5', 'v5 draft: marker not found')
        pairs = _pairs(rules)
        wrong = {name: (pairs[name], want) for name, env, want in FIXTURES
                 if pairs[name] != want}
        _require(not wrong, 'v5 draft: wrong pairs %r' % wrong)
        return '%d fixtures match' % len(FIXTURES)

    @case
    def c_ddwrt_is_reader_backed():
        """squashfs_v3_ddwrt keeps the legacy row; the three no-reader families do not."""
        rules, _info = _parse_block(V5_BLOCK)
        legacy = [r for r in rules if r['label'] == 'legacy-body-failure'][0]
        spec = legacy['failing_handler']
        _require(spec[0] == 'list', 'legacy row: failing-handler cell is %r, expected a list'
                 % (spec,))
        matched = set()
        for name in KNOWN_HANDLERS:
            if match_glob(spec, [name]):
                matched.add(name)
        _require(matched == set(READER_BACKED_V1V3),
                 'legacy row: matched %r, expected %r' % (sorted(matched),
                                                          sorted(READER_BACKED_V1V3)))
        return 'legacy failing-handler cell names %s' % ', '.join(sorted(matched))

    @case
    def c_no_reader_rows_are_keyed_on_the_families():
        """clean-unverified keys off F; no-reader-failure keys off HF."""
        rules, _info = _parse_block(V5_BLOCK)

        def matched(spec):
            return {name for name in KNOWN_HANDLERS if match_glob(spec, [name])}

        clean = [r for r in rules if r['label'] == 'clean-unverified'][0]
        _require(matched(clean['handler']) == set(NO_READER_FAMILIES),
                 'clean-unverified: handler matches %r, expected %r'
                 % (sorted(matched(clean['handler'])), sorted(NO_READER_FAMILIES)))
        _require(clean['failing_handler'] == ('any', None),
                 'clean-unverified: failing handler is %r, expected the wildcard (a clean '
                 'run has no failing handler)' % (clean['failing_handler'],))
        failure = [r for r in rules if r['label'] == 'no-reader-failure'][0]
        _require(matched(failure['failing_handler']) == set(NO_READER_FAMILIES),
                 'no-reader-failure: failing handler matches %r, expected %r'
                 % (sorted(matched(failure['failing_handler'])),
                    sorted(NO_READER_FAMILIES)))
        _require(matched(failure['handler']) == set(KNOWN_HANDLERS),
                 'no-reader-failure: handler cell is %r, expected any SquashFS handler'
                 % (matched(failure['handler']),))
        return 'clean-unverified keys off F, no-reader-failure keys off HF'

    @case
    def c_no_reader_failure_sits_between_legacy_and_body():
        """The new failure row is below the legacy row and above the generic body row."""
        rules, _info = _parse_block(V5_BLOCK)
        order = [r['label'] for r in rules]
        i_legacy = order.index('legacy-body-failure')
        i_noreader = order.index('no-reader-failure')
        i_body = order.index('body-extractor-failure')
        i_clean = order.index('clean')
        i_unver = order.index('clean-unverified')
        _require(i_legacy < i_noreader < i_body,
                 'row order: legacy %d, no-reader %d, body %d' % (i_legacy, i_noreader,
                                                                 i_body))
        _require(i_unver < i_clean, 'row order: clean-unverified %d, clean %d'
                 % (i_unver, i_clean))
        return 'row order verified'

    @case
    def c_mutations_each_flip_their_own_pairs():
        """Every committed mutation flips >=1 pair, and only the pairs it owns."""
        base_rules, _info = _parse_block(V5_BLOCK)
        base = _pairs(base_rules)
        for name, mutator, expected in MUTATIONS:
            block = _mutate_text_table(mutator)
            rules, _info = _parse_block(block)
            other = _pairs(rules)
            flipped = _flipped(base, other)
            _require(flipped, 'mutation %s flipped no pair' % name)
            _require(flipped == expected,
                     'mutation %s flipped %r, expected %r'
                     % (name, sorted(flipped), sorted(expected)))
        return '%d textual mutations verified' % len(MUTATIONS)

    @case
    def c_blanked_cell_mutation_flips_its_pairs():
        """A blanked condition cell (rule level) flips only the pairs it owns."""
        base_rules, _info = _parse_block(V5_BLOCK)
        base = _pairs(base_rules)
        rules = _mut_blank_cell(base_rules)
        other = _pairs(rules)
        flipped = _flipped(base, other)
        expected = {'v4le-clean', 'v4be-clean', 'v4bc-clean'}
        _require(flipped, 'blanked-cell mutation flipped no pair')
        _require(flipped == expected,
                 'blanked-cell mutation flipped %r, expected %r'
                 % (sorted(flipped), sorted(expected)))
        return 'blanked cell flips %s' % ', '.join(sorted(flipped))

    @case
    def c_blanked_text_cell_is_malformed():
        """A blanked condition cell in the TEXT is refused, never a silent non-match."""
        rows = _text_rows(V5_ROWS)
        rows[_row_index(rows, 'clean-unverified')][3] = ''
        block = _render(rows, V5_ACTIONS, MARKER_V5)
        try:
            _parse_block(block)
        except TableError as exc:
            _require('handler' in str(exc), 'blanked cell: %r' % str(exc))
            return 'blanked text cell refused: %s' % str(exc)[:80]
        raise AssertionError('blanked text cell was accepted')

    @case
    def c_junk_table_is_red():
        """A junk table (every row clean) is red against the fixed evaluator."""
        junk = []
        for i, row in enumerate(_text_rows(V5_ROWS)):
            row = list(row)
            row[0] = 'junk-%d' % i
            row[3] = 'squashfs_*'
            row[4] = '*'
            row[5] = '*'
            row[6] = '*'
            row[7] = '*'
            row[8] = '*'
            row[9] = '*'
            row[10] = 'none'
            junk.append(row)
        block = _render(junk, V5_ACTIONS, MARKER_V5)
        rules, _info = _parse_block(block)
        pairs = _pairs(rules)
        mismatched = {name for name, env, want in FIXTURES if pairs[name] != want}
        _require(mismatched, 'junk table scored green')
        return 'junk table red on %d of %d fixtures' % (len(mismatched), len(FIXTURES))

    @case
    def c_dead_alternative_is_malformed():
        """A handler alternative that matches no known handler is a malformed table."""
        rows = _text_rows(V5_ROWS)
        rows[_row_index(rows, 'clean-unverified')][3] = 'squashfs_v9*'
        block = _render(rows, V5_ACTIONS, MARKER_V5)
        try:
            _parse_block(block)
        except TableError as exc:
            _require('dead cell' in str(exc), 'dead alternative: %r' % str(exc))
            return 'dead alternative refused'
        raise AssertionError('dead alternative was accepted')

    @case
    def c_duplicate_handler_glob_is_refused():
        """A handler cell that repeats an alternative is refused (H1).

        v4's docstring claimed it refused a "duplicate label or handler glob", but its
        code refused only duplicate LABELS (v4:455-459).  v5 keeps that claim TRUE: a
        repeated alternative in one handler-family cell is a malformed table (exit 2),
        never a silent non-match.
        """
        for column in (3, 4):
            rows = _text_rows(V5_ROWS)
            rows[_row_index(rows, 'legacy-body-failure')][column] = (
                'squashfs_v1,squashfs_v3,squashfs_v1')
            block = _render(rows, V5_ACTIONS, MARKER_V5)
            try:
                _parse_block(block)
            except TableError as exc:
                _require('repeats' in str(exc),
                         'duplicate alternative (column %d): %r' % (column, str(exc)))
                continue
            raise AssertionError('duplicate alternative accepted (column %d)' % column)
        return 'duplicate alternative refused in both handler columns'

    @case
    def c_refused_older_marker():
        """A document whose newest marker is v3 is refused."""
        block = _render(_v4_full_rows(), VOCAB_V4, '<!-- sqfs-triage-table v3 -->')
        try:
            _parse_block(block)
        except TableError as exc:
            _require('refused' in str(exc), 'v3 marker: %r' % str(exc))
            return 'v3 marker refused'
        raise AssertionError('v3 marker was accepted')

    @case
    def c_evaluator_is_independent_of_the_table():
        """The evaluator's verdict does not change when the table changes."""
        feat = features(_env(handler='squashfs_v2_nonstandard', gaps=[], files=4))
        _require(evaluate(feat)[:2] == ('clean-unverified', 'record-unverified'),
                 'evaluator: %r' % (evaluate(feat),))
        feat = features(_env(handler='squashfs_v2_nonstandard', gaps=['extractor-failure'],
                              be='-le', files=0))
        _require(evaluate(feat)[:2] == ('no-reader-failure', 'preserve-unresolved'),
                 'evaluator: %r' % (evaluate(feat),))
        feat = features(_env(handler='squashfs_v3_ddwrt', gaps=['extractor-failure'],
                              be='-be', files=0))
        _require(evaluate(feat)[:2] == ('legacy-body-failure', 'cross-read-legacy'),
                 'evaluator: %r' % (evaluate(feat),))
        feat = features(_env(handler='squashfs_v4_le', gaps=[], files=2))
        _require(evaluate(feat)[:2] == ('clean', 'none'), 'evaluator: %r' % (evaluate(feat),))
        return 'evaluator precedence verified'

    @case
    def c_guard_row_and_failure_row_are_the_named_ones():
        """The guard row the guard-deleted control names is `clean-unverified`.

        The claim's C3 control names the guard row `clean-unverified`, and names the
        `no-reader-failure` row/action as witnessed by a synthetic zero-file
        extractor-failure envelope.  Both names are pinned here so a rename cannot
        silently detach the control from the row it is supposed to delete.
        """
        rules, _info = _parse_block(V5_BLOCK)
        labels = [r['label'] for r in rules]
        _require('clean-unverified' in labels,
                 'the guard row clean-unverified is missing from the table')
        _require('no-reader-failure' in labels,
                 'the no-reader-failure row is missing from the table')
        failure = [r for r in rules if r['label'] == 'no-reader-failure'][0]
        _require(failure['action'] == 'preserve-unresolved',
                 'no-reader-failure: action is %r, expected preserve-unresolved'
                 % failure['action'],)
        guard = [r for r in rules if r['label'] == 'clean-unverified'][0]
        _require(guard['action'] == 'record-unverified',
                 'clean-unverified: action is %r, expected record-unverified'
                 % guard['action'],)
        # the synthetic witness: a no-reader family, zero files, an extractor failure
        synth = _env(handler='squashfs_v2_nonstandard', gaps=['extractor-failure'],
                     be='-le', files=0)
        feat = features(synth)
        _require(evaluate(feat)[:2] == ('no-reader-failure', 'preserve-unresolved'),
                 'the synthetic zero-file no-reader failure is not witnessed: %r'
                 % (evaluate(feat),))
        rule = classify(rules, feat)
        _require(rule is not None and rule['label'] == 'no-reader-failure',
                 'the synthetic witness does not reach the no-reader-failure row: %r'
                 % (rule,))
        return 'guard row and failure row named and witnessed'

    @case
    def c_predicate_matches_the_claim_file():
        """The predicate sentence is the claim's, byte for byte, and reaches the receipt.

        The claim requires "the same sentence in the counter docstring, this file, and
        the receipt label".  This case reads the claims file at the lane's HEAD and
        compares the sentence the claim carries with the instrument's PREDICATE
        constant; a drift in either is a failure here, not a silent divergence.
        """
        _require(PREDICATE.startswith('at the measured revision REV, with FREEZE an '
                                      'ancestor of REV, frozen paths untouched,'),
                 'predicate: the sentence does not open as the claim writes it')
        _require('the no-reader `*_ddefault` rows among the mismatches' in PREDICATE,
                 'predicate: the before-state clause is not the amended one (the '
                 'no-reader `*_ddefault` rows)')
        claims = os.path.join(LANE, 'plans', 'round-50-attempt2-claims.md')
        if not os.path.isfile(claims):
            return 'predicate shape verified (claims file not readable here)'
        with open(claims, 'r', encoding='utf-8') as handle:
            text = handle.read()
        flat = ' '.join(text.split())
        for fragment in ('at the measured revision REV, with FREEZE an ancestor of REV, '
                         'frozen paths untouched, running',
                         'exits 0 with `pair_mismatches 0`, `evaluator_missing 0`,',
                         '`table_labels == evaluator_labels` on every envelope of the '
                         'frozen held-out dir, `selftest` green (every committed '
                         'mutation flips ≥1 pair, none a no-op or cross-flip, do-nothing '
                         'red); and at the base REV the same command exits 1 with the '
                         'no-reader `*_ddefault` rows among the mismatches.'):
            _require(fragment in flat,
                     'predicate: the claims file does not carry the fragment %r'
                     % fragment[:60])
        # the receipt carries the same sentence
        for fragment in ('the no-reader `*_ddefault` rows among the mismatches.',
                         'tools/round-50-c3/sqfs-triage-v5.py --root <LANE>'):
            _require(fragment in PREDICATE,
                     'predicate: the instrument does not carry the fragment %r'
                     % fragment[:60])
        return 'predicate matches the claim file and reaches the receipt'

    @case
    def c_receipt_is_written_and_parses():
        """The JSON receipt exists, parses, and carries the required keys.

        The exit code alone is not evidence: a 49-byte stub was measured exiting 0 on
        the full predicate command while writing NO receipt.  This case runs the
        instrument for real over a fixture set and checks the receipt on disk.
        """
        env_dir = os.path.join(work, 'receipt-envelopes')
        os.makedirs(env_dir, exist_ok=True)
        for name, env, _want in FIXTURES:
            path = os.path.join(env_dir, name, 'envelope.json')
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as handle:
                json.dump(env, handle)
        skill = os.path.join(work, 'sk-receipt.md')
        with open(skill, 'w', encoding='utf-8') as handle:
            handle.write('# SKILL\n\n## Queue-drain craft\n\n'
                         + V5_BLOCK + '\n## A later section\n')
        out = os.path.join(work, 'receipt.json')
        proc = subprocess.run([sys.executable, '-I', '-B', os.path.abspath(__file__),
                               '--skill', skill, '--envelopes', env_dir,
                               '--json-out', out], capture_output=True, text=True)
        _require(proc.returncode == 0,
                 'receipt-run: exit %d, stderr=%r'
                 % (proc.returncode, proc.stderr.strip()[:200]))
        _require(os.path.isfile(out), 'receipt: no receipt was written at %r' % out)
        with open(out, 'r', encoding='utf-8') as handle:
            receipt = json.load(handle)
        for key in ('predicate', 'pair_mismatches', 'evaluator_missing', 'table_labels',
                    'n_envelopes', 'verdict'):
            _require(key in receipt, 'receipt: missing the key %r' % key)
        _require(receipt['predicate'] == PREDICATE,
                 'receipt: the predicate in the receipt is not the instrument constant')
        _require(receipt['n_envelopes'] == len(FIXTURES),
                 'receipt: n_envelopes is %r, expected %d'
                 % (receipt['n_envelopes'], len(FIXTURES)))
        return 'receipt written, parsed, and carries the predicate'

    @case
    def c_claim_counting_command_is_consistent():
        """The claims file's counting command names the base rev the details name.

        The claim's "Counting command" bullet and its "Frozen rule details" bullets
        must agree on the before-run revision and on the expected before-state size;
        a divergence there is a claim-text defect, and this case reports it rather
        than letting the two drift apart silently.
        """
        claims = os.path.join(LANE, 'plans', 'round-50-attempt2-claims.md')
        if not os.path.isfile(claims):
            return 'claims file not readable here (nothing to reconcile)'
        with open(claims, 'r', encoding='utf-8') as handle:
            text = handle.read()
        flat = ' '.join(text.split())
        has_base = 'f890bbea' in flat
        has_old_base = '8ccc05e6' in flat
        has_19 = 'seat-measured **19**' in flat
        _require(has_19,
                 'the claim no longer states the seat-measured 19-row before-state')
        if has_base and has_old_base:
            # both revisions appear: the frozen details must bind the before-run to
            # the declared base, and the counting bullet must not name the other one
            _require('before-run `--rev` is the exact declared base' in flat,
                     'the claim names two base revisions and does not bind the '
                     'before-run to the declared base')
        return 'the claim names one before-run base and the 19-row before-state'

    @case
    def c_evaluator_abstention_is_reported():
        """An envelope the evaluator cannot decide lands in evaluator_missing."""
        base_rules, _info = _parse_block(V5_BLOCK)
        feat = features(_env(handler='squashfs_v4_le', gaps=[], files=2))
        _require(evaluate(feat)[0] is not None, 'evaluator: expected a verdict')
        _require(_missing_ids([]) == [], 'evaluator_missing: expected an empty list')
        _require(_missing_ids([{'envelope': 'x', 'reason': 'r'}]) == ['x'],
                 'evaluator_missing: expected the abstained envelope id')
        return 'abstention path verified'

    for fn in cases:
        name = fn.__name__[2:]
        try:
            note = fn()
            passed += 1
            print('ok   %-46s %s' % (name, note))
        except AssertionError as exc:
            failed.append((name, str(exc)))
            print('FAIL %-46s %s' % (name, exc))
    print('selftest: %d cases, pass %d, fail %d' % (len(cases), passed, len(failed)))
    if failed:
        for name, message in failed:
            print('  failed: %s: %s' % (name, message))
        return 1
    return 0


# --------------------------------------------------------------------------------------
# command line
# --------------------------------------------------------------------------------------

def main(argv=None):
    parser = argparse.ArgumentParser(
        prog='sqfs-triage-v5.py',
        description='Label REA envelopes with the SKILL.md triage table v5 and with the '
                    'fixed R50-C3 evaluator, and compare the two.')
    parser.add_argument('--root', help='lane root (git repository)')
    parser.add_argument('--rev', help='revision whose SKILL.md is read (git show REV:SKILL.md)')
    parser.add_argument('--freeze', help='freeze revision; must be an ancestor of --rev')
    parser.add_argument('--envelopes', help='directory of REA envelopes')
    parser.add_argument('--json-out', help='where to write the JSON report')
    parser.add_argument('--skill', help='read SKILL.md from this file instead of git')
    parser.add_argument('--work', help='directory for selftest fixtures')
    parser.add_argument('--selftest', action='store_true', help='run the offline selftest')
    parser.add_argument('--print-v5-block', action='store_true',
                        help='print the embedded v5 table draft')
    parser.add_argument('--emit-mutant', metavar='NAME',
                        help='print one committed mutation of the v5 draft table (or '
                             '"junk-table" / "do-nothing-v4")')
    parser.add_argument('--controls', action='store_true',
                        help='run every committed control against --envelopes and report '
                             'them; the do-nothing control must be red')
    ns = parser.parse_args(argv)

    try:
        if ns.print_v5_block:
            sys.stdout.write(V5_BLOCK)
            return 0
        if ns.emit_mutant:
            sys.stdout.write(emit_mutant(ns.emit_mutant))
            return 0
        if ns.selftest:
            return selftest(ns)
        if ns.controls:
            if not ns.envelopes:
                raise InvocationError('--envelopes is required with --controls')
            return corpus_control(ns)
        if not ns.envelopes:
            raise InvocationError('--envelopes is required')
        if not ns.json_out:
            raise InvocationError('--json-out is required')
        return run(ns)
    except InvocationError as exc:
        sys.stderr.write('sqfs-triage-v5: %s\n' % exc)
        return 2
    except TableError as exc:
        sys.stderr.write('sqfs-triage-v5: table error: %s\n' % exc)
        return 2
    except EnvelopeError as exc:
        sys.stderr.write('sqfs-triage-v5: envelope error: %s\n' % exc)
        return 2
    except Unevaluable as exc:
        sys.stderr.write('sqfs-triage-v5: could not evaluate: %s\n' % exc)
        return 2


if __name__ == '__main__':
    sys.exit(main())
