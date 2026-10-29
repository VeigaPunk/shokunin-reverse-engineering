#!/usr/bin/env python3
"""Is a given set of unblob handler names selectable by ONE glob in the v4
cell grammar (fnmatch semantics, no alternation)?

Search space: patterns built from ATOMS
  * a literal character occurring in some handler name,
  * '*',
  * '?',
  * a character class over the name alphabet: [c], [!c], [c1c2...], [c1-c2]
bounded by an atom count, with an exact prefix-compatibility oracle pruning
branches that can no longer match any name.

The search is exhaustive for the searched space; a null result is reported as
"no glob of this shape", never as a proof of impossibility.
"""
import fnmatch
import functools
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
ALPHABET = sorted({ch for n in HANDLERS for ch in n})
MAX_ATOMS = 8
CELL_RE = __import__('re').compile(r'^[A-Za-z0-9_?*.\-\[\]]+$')


def _class_hit(body, ch):
    i = 0
    while i < len(body):
        if i + 2 < len(body) and body[i + 1] == '-':
            if body[i] <= ch <= body[i + 2]:
                return True
            i += 3
        else:
            if body[i] == ch:
                return True
            i += 1
    return False


def _tokens(pattern):
    out = []
    i = 0
    while i < len(pattern):
        ch = pattern[i]
        if ch == '[':
            j = i + 1
            if j < len(pattern) and pattern[j] == '!':
                j += 1
            if j < len(pattern) and pattern[j] == ']':
                j += 1
            while j < len(pattern) and pattern[j] != ']':
                j += 1
            out.append(pattern[i:j + 1])
            i = j + 1
        else:
            out.append(ch)
            i += 1
    return tuple(out)


def partial_match(pattern, s):
    """Could `pattern` match some PREFIX of s?  (fnmatch semantics, DP.)"""
    pt = _tokens(pattern)

    @functools.lru_cache(maxsize=None)
    def go(pi, si):
        if pi == len(pt):
            return True
        tok = pt[pi]
        if tok == '*':
            return go(pi + 1, si) or (si < len(s) and go(pi, si + 1))
        if si >= len(s):
            return False
        if tok == '?':
            return go(pi + 1, si + 1)
        if tok[0] == '[':
            body = tok[1:-1]
            neg = body.startswith('!')
            if neg:
                body = body[1:]
            hit = _class_hit(body, s[si])
            if neg:
                hit = not hit
            return hit and go(pi + 1, si + 1)
        return s[si] == tok and go(pi + 1, si + 1)
    return go(0, 0)


def match_set(pattern):
    return frozenset(n for n in HANDLERS if fnmatch.fnmatchcase(n, pattern))


def atoms():
    out = ['*', '?']
    for ch in ALPHABET:
        out.append(ch)
        out.append('[%s]' % ch)
        out.append('[!%s]' % ch)
    for a in ALPHABET:
        for b in ALPHABET:
            if a < b:
                out.append('[%s-%s]' % (a, b))
    # a two-letter class over the letters that matter (n/b vs d)
    for pair in ('bn', 'bd', 'nd', 'db', 'nb', 'dn'):
        out.append('[%s]' % pair)
    return out


def search(target, max_atoms=MAX_ATOMS):
    target = frozenset(target)
    hits = set()
    seen = set()
    atoms_list = atoms()

    def dfs(pat):
        if pat in seen:
            return
        seen.add(pat)
        if match_set(pat) == target:
            hits.add(pat)
        if pat.count('*') + len(pat) >= max_atoms + 12:
            return
        if not any(partial_match(pat, n) for n in HANDLERS):
            return
        for a in atoms_list:
            dfs(pat + a)

    dfs('')
    return sorted(hits), len(seen)


def main():
    out = {'max_atoms': MAX_ATOMS, 'alphabet': ALPHABET}
    for name, target in (('reader_backed_legacy', READER_LEGACY),
                         ('no_reader', NO_READER)):
        hits, seen = search(target)
        out[name] = {'target': sorted(target), 'hits': hits, 'hit_count': len(hits),
                     'patterns_visited': seen}
    out['control_no_reader_glob'] = 'squashfs_v[23]_[bn]*'
    out['control_no_reader_glob_match_set'] = sorted(
        match_set(out['control_no_reader_glob']))
    out['bare_v123_match_set'] = sorted(match_set('squashfs_v[123]'))
    out['wide_v123_star_match_set'] = sorted(match_set('squashfs_v[123]*'))
    p = '/fast/scratch/hyaku/kaidoku-r50/w3-MutPlan/glob-search.json'
    with open(p, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print(json.dumps({k: v for k, v in out.items()
                      if k not in ('reader_backed_legacy', 'no_reader')},
                     indent=1, sort_keys=True))
    for k in ('reader_backed_legacy', 'no_reader'):
        print(k, 'hits:', out[k]['hits'][:20], 'count', out[k]['hit_count'],
              'visited', out[k]['patterns_visited'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
