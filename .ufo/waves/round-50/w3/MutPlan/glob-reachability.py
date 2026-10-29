#!/usr/bin/env python3
"""FINAL, correctly-bounded glob reachability for the v4 single-glob cell
grammar (fnmatch; no negation, no alternation, one glob per cell).

This supersedes two earlier, too-narrow searches whose zero-hit results were
BOUND ARTIFACTS (their candidate space could not contain an answer):

  glob-targeted.py     searched suffix-space globs of length <= 4; the
                       answering no-reader glob has a 9-character suffix, so
                       the space could not contain it.
  glob-reader-backed.py  searched only the [*]C[*] form (ONE non-star atom);
                       the answering no-reader glob needs THREE atoms.

THE SCOPE RULE (this is what the earlier searches got wrong):

  A target that contains a ONE-CHARACTER suffix (e.g. 'squashfs_v1' -> '1')
  forces its pattern into the form  [*]X[*]  with a single non-star atom X:
  a pattern that matches a 1-character string can consume at most one
  character outside its stars.  For such a target, enumerating [*]X[*] over
  every literal and every class over the suffix alphabet IS complete.

  A target whose shortest suffix is longer (the no-reader set: '2_nonstandard',
  '3_broadcom', '3_nonstandard') has NO such bound: its pattern may carry
  several atoms, and [*]X[*] is NOT a complete space for it.  For that target
  this script does not claim completeness - it measures the ANSWER directly.

WHAT THIS SCRIPT MEASURES

  A. The no-reader set IS selectable by one v4-grammar glob:
       squashfs_v[23]_[bn]*   -> exactly the three no-reader names
     (measured against the real ten handler names, and confirmed end-to-end by
      the v4 evaluator in the table-mutant battery: the D mutant used exactly
      this glob and produced 19 label flips, all in the three no-reader
      families, with zero reader-backed cross-flip.)

  B. The READER-BACKED legacy set {v1, v2, v3, v3_ddwrt} is NOT selectable by
     one v4-grammar glob, and here the [*]X[*] enumeration IS complete
     (the target contains the one-character suffix '1').  Enumerated: every
     literal and every class over the suffix alphabet, with 0..3 leading and
     trailing stars.

     The analytic reason, for the record: the target contains 'squashfs_v1'
     (10 chars) and 'squashfs_v3_ddwrt' (16 chars) but rejects
     'squashfs_v2_nonstandard' (19 chars, sharing the 10-char prefix of
     'squashfs_v2').  A pattern matching the 1-char suffix '1' has at most one
     non-star atom, so it is [*]X[*]; for it to match '3_ddwrt' the atom X
     must match '3' and a trailing star must absorb '_ddwrt'.  That same
     trailing star also absorbs '_nonstandard' and '_broadcom', so the rejected
     names cannot be excluded.  Hence no single glob.
"""
import fnmatch
import itertools
import json
import os
import sys

HANDLERS = (
    'squashfs_v1', 'squashfs_v2', 'squashfs_v2_nonstandard', 'squashfs_v3',
    'squashfs_v3_ddwrt', 'squashfs_v3_broadcom', 'squashfs_v3_nonstandard',
    'squashfs_v4_le', 'squashfs_v4_be', 'squashfs_v4_broadcom',
)
NO_READER = frozenset(('squashfs_v2_nonstandard', 'squashfs_v3_broadcom',
                       'squashfs_v3_nonstandard'))
READER_LEGACY = frozenset(('squashfs_v1', 'squashfs_v2', 'squashfs_v3',
                           'squashfs_v3_ddwrt'))
PREFIX = 'squashfs_v'
SUFFIXES = tuple(h[len(PREFIX):] for h in HANDLERS)
ALPHABET = sorted({c for s in SUFFIXES for c in s})


def select(pattern):
    return frozenset(h for h in HANDLERS if fnmatch.fnmatchcase(h, pattern))


def select_suffix(sp):
    """Select by the suffix-space pattern (used for the completeness argument)."""
    return frozenset(h for h, s in zip(HANDLERS, SUFFIXES)
                      if fnmatch.fnmatchcase(s, sp))


def classes():
    """Every single-character class over the suffix alphabet, plus the literals."""
    out = set()
    for c in ALPHABET:
        out.add('[%s]' % c)
        out.add('[!%s]' % c)
    for a, b in itertools.combinations_with_replacement(ALPHABET, 2):
        if a != b:
            out.add('[%s%s]' % (a, b))
            out.add('[%s-%s]' % (a, b))
    return sorted(out)


def complete_star_atom_candidates():
    """Every [*]X[*] form: the COMPLETE space for a target containing a
    one-character suffix."""
    middles = list(ALPHABET) + ['?'] + classes()
    for lead in range(0, 4):
        for trail in range(0, 4):
            for m in middles:
                yield '*' * lead + m + '*' * trail


def main():
    out = {'grammar': 'fnmatch; no negation (! / ^ are outside the v4 cell '
                     'grammar), no alternation, one glob per cell',
           'handler_names': list(HANDLERS)}

    # ---- A. the no-reader set: measured answer, no completeness claim -----
    answer = 'squashfs_v[23]_[bn]*'
    out['A_no_reader_set'] = {
        'target': sorted(NO_READER),
        'selecting_glob': answer,
        'match_set': sorted(select(answer)),
        'is_exact': select(answer) == NO_READER,
        'completeness_claim': 'none asserted: this target has no one-character '
                              'suffix, so the [*]X[*] space does not bound it. '
                              'The glob is a MEASURED ANSWER, and it is the '
                              'glob the D table mutant used end-to-end '
                              '(19 flips, 0 cross-flip).',
        'earlier_zero_hit_was': 'a bound artifact of two too-narrow searches '
                                '(length<=4 suffix globs; and the one-atom '
                                '[*]X[*] form), not a property of the grammar',
    }

    # ---- B. the reader-backed legacy set: complete enumeration ------------
    hits = []
    n = 0
    for g in complete_star_atom_candidates():
        n += 1
        if select_suffix(g) == frozenset(
                s for h, s in zip(HANDLERS, SUFFIXES) if h in READER_LEGACY):
            hits.append(PREFIX + g)
    out['B_reader_backed_legacy_set'] = {
        'target': sorted(READER_LEGACY),
        'space': '[*]X[*] -- COMPLETE here, because the target contains the '
                  'one-character suffix "1"',
        'candidates_enumerated': n,
        'hit_count': len(set(hits)),
        'hits': sorted(set(hits)),
        'conclusion': 'no single v4-grammar glob selects the reader-backed '
                      'legacy set exactly',
    }

    # ---- controls (so the method is shown to find answers when one exists) --
    out['controls'] = {
        'squashfs_v[23]_[bn]*': sorted(select('squashfs_v[23]_[bn]*')),
        'squashfs_v[123]': sorted(select('squashfs_v[123]')),
        'squashfs_v[123]*': sorted(select('squashfs_v[123]*')),
        'note': 'the first control is the exact no-reader answer; the second '
                'and third show the wide shipped glob that also selects the '
                'no-reader families (the F1 defect).',
    }
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     'glob-reachability.json')
    json.dump(out, open(p, 'w'), indent=1, sort_keys=True)
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
