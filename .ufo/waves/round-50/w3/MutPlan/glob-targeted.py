#!/usr/bin/env python3
"""Targeted, provably-complete search: which SINGLE fnmatch glob (v4 cell
grammar: no ',', no negation) selects a given subset of the ten handler names?

Every discriminating decision happens in the SUFFIX after the common literal
prefix "squashfs_v", so it is enough to enumerate suffix globs T over the
suffix alphabet and prefix them with the literal.  (A glob that puts a wildcard
before the prefix cannot separate two names that share the prefix, so it can
only widen the selected set - it can never help select a NARROWER set.)
"""
import fnmatch, itertools, json, os, sys

HANDLERS = (
    'squashfs_v1', 'squashfs_v2', 'squashfs_v2_nonstandard', 'squashfs_v3',
    'squashfs_v3_ddwrt', 'squashfs_v3_broadcom', 'squashfs_v3_nonstandard',
    'squashfs_v4_le', 'squashfs_v4_be', 'squashfs_v4_broadcom',
)
SUFFIXES = tuple(h[len('squashfs_v'):] for h in HANDLERS)
# NOTE: the suffix excludes the trailing 'v', so patterns are written WITHOUT 'v'
READER = frozenset(('squashfs_v1', 'squashfs_v2', 'squashfs_v3', 'squashfs_v3_ddwrt'))
NOREADER = frozenset(('squashfs_v2_nonstandard', 'squashfs_v3_broadcom',
                      'squashfs_v3_nonstandard'))


def select(pat):
    return frozenset(h for h, s in zip(HANDLERS, SUFFIXES)
                      if fnmatch.fnmatchcase(s, pat))


def candidates():
    """Every suffix glob of length <= 4 over the suffix alphabet {1,2,3,4,_,
    d,b,n,o,m,e,s,t,r,l,p,a,c} with '*' and '?'."""
    alpha = sorted({c for s in SUFFIXES for c in s} | {'*', '?'})
    out = set()
    for L in range(0, 5):
        for combo in itertools.product(alpha, repeat=L):
            out.add(''.join(combo))
    return out


def main():
    cands = candidates()
    print('suffix glob candidates:', len(cands), flush=True)
    res = {}
    for name, target in (('reader_backed_legacy', READER),
                         ('no_reader', NOREADER)):
        hits = sorted(p for p in cands if select(p) == target)
        # the full pattern (literal prefix + suffix glob)
        res[name] = {'target': sorted(target), 'hits': hits, 'hit_count': len(hits),
                     'example_full_patterns': ['squashfs_v' + h for h in hits[:5]]}
    res['control_bare_123'] = sorted(select('[123]'))
    res['control_wide_123_star'] = sorted(select('[123]*'))
    res['control_23_bn_star'] = sorted(select('[23]_[bn]*'))
    p = '/fast/scratch/hyaku/kaidoku-r50/w3-MutPlan/glob-targeted.json'
    json.dump(res, open(p, 'w'), indent=1, sort_keys=True)
    print(json.dumps(res, indent=1, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
