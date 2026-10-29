#!/usr/bin/env python3
"""COMPLETE enumeration: can ONE fnmatch glob (the v4 cell grammar) select
exactly the reader-backed legacy set {v1, v2, v3, v3_ddwrt}?

The enumeration is complete because it is bounded by a structural fact, not by a
length budget.  Write every handler name as PREFIX + SUFFIX with
PREFIX = 'squashfs_v' (the common literal prefix of all ten names) and SUFFIX in
{'1','2','2_nonstandard','3','3_ddwrt','3_broadcom','3_nonstandard',
'4_le','4_be','4_broadcom'}.

A glob G selects exactly the target set iff G selects '1' and '3_ddwrt' and
rejects the other eight.  For G to match the ONE-CHARACTER suffix '1', every
non-wildcard character of G must lie within the first character of the suffix
(a literal or class consumes a character; '?' consumes one; '*' consumes any
number, including zero).  Hence G's suffix form is

    [*] C [*]          with C a single literal char or a single-char class,

or G's suffix form is empty (which matches only '').  So the COMPLETE set of
candidate G's is:

  G_suffix in { '1', '?' , '[c]', '[!c]', '[c-c]', '[c1c2...]' } each with an
  arbitrary number of leading and trailing '*'.

We enumerate that set exhaustively (leading/trailing star counts 0..3 and every
single-character class over the suffix alphabet), and report every G whose
selected set equals the target.
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
PREFIX = 'squashfs_v'
SUFFIXES = tuple(h[len(PREFIX):] for h in HANDLERS)
TARGET = frozenset(('squashfs_v1', 'squashfs_v2', 'squashfs_v3',
                    'squashfs_v3_ddwrt'))
NO_READER = frozenset(('squashfs_v2_nonstandard', 'squashfs_v3_broadcom',
                       'squashfs_v3_nonstandard'))
ALPHA = sorted({c for s in SUFFIXES for c in s})


def select(suffix_pat):
    return frozenset(h for h, s in zip(HANDLERS, SUFFIXES)
                      if fnmatch.fnmatchcase(s, suffix_pat))


def classes():
    """Every single-character class over the suffix alphabet (plus ranges)."""
    out = set()
    for c in ALPHA:
        out.add('[%s]' % c)
        out.add('[!%s]' % c)
    for a, b in itertools.combinations_with_replacement(ALPHA, 2):
        if a != b:
            out.add('[%s%s]' % (a, b))
            out.add('[%s-%s]' % (a, b))
    for c in ALPHA:
        out.add('[%s%s]' % (c, c))
    return sorted(out)


def candidates():
    """Every G_suffix of the complete structural form."""
    middles = ['1', '?', '2', '3', '4'] + classes()
    for lead in range(0, 4):
        for trail in range(0, 4):
            for m in middles:
                yield '*' * lead + m + '*' * trail
            # the empty-middle form: only stars
            yield '*' * lead + '*' * trail


def main():
    seen = set()
    hits = []
    n = 0
    for g in candidates():
        if g in seen:
            continue
        seen.add(g)
        n += 1
        if select(g) == TARGET:
            hits.append(PREFIX + g)
    out = {
        'target': sorted(TARGET),
        'candidates_enumerated': n,
        'hits_selecting_exactly_target': sorted(set(hits)),
        'hit_count': len(set(hits)),
        'no_reader_set_selectable_examples': sorted(
            PREFIX + g for g in sorted(seen)
            if select(g) == NO_READER)[:12],
        'no_reader_set_selectable_count': sum(
            1 for g in seen if select(g) == NO_READER),
        'note': 'the enumeration is complete for the v4 single-glob cell '
                'grammar: a glob that matches the one-character suffix "1" '
                'can carry at most one non-wildcard character before any '
                'trailing stars, so the structural form is [*]C[*].',
    }
    p = '/fast/scratch/hyaku/kaidoku-r50/w3-MutPlan/glob-reader-backed.json'
    json.dump(out, open(p, 'w'), indent=1, sort_keys=True)
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
