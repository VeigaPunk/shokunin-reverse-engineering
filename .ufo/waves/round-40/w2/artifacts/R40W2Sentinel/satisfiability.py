#!/usr/bin/env python3
"""R40W2Sentinel: is P40-C1's 4/4 reachable from the FROZEN C1 inputs?

No REA run and no counter code is used. For each frozen carrier the oracle and
non-regular tables are read at the freeze revision and the counter's own
`same_rel` predicate is transcribed verbatim (tools/round-40/c1-counter.py:607):

    same_rel(candidate, rel) := candidate == rel or candidate.endswith('/' + rel)

Question 1 (collision): does any oracle regular-file rel collide with any
  non-regular rel?
Question 2 (entailment): can a published set satisfy `oracle_hits_ok` (every
  oracle rel published under some prefix, same sha) while keeping
  `nonregular_unpublished_ok` true (no published path matches a non-regular
  path)? If a published path P matches oracle rel R and R itself matches
  non-regular rel N, then every P that matches R also matches N -- the suffix
  relation is transitive when R endswith '/'+N. So both clauses are jointly
  unsatisfiable for that carrier.
"""

import itertools
import json
import os
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
FREEZE = '7fce308631a8b457d6b7c5a4b39a923c4e9a49de'


def same_rel(candidate, rel):
    # c1-counter.py:607, verbatim
    return bool(candidate) and bool(rel) and (candidate == rel or candidate.endswith('/' + rel))


def show(rev, path):
    p = subprocess.run(['git', '-C', LANE, 'show', f'{rev}:{path}'], capture_output=True)
    if p.returncode != 0:
        raise SystemExit(f'absent at {rev}: {path}')
    return p.stdout.decode()


def table(rev, path):
    rows = []
    for line in show(rev, path).splitlines():
        if not line.strip():
            continue
        cells = line.split('\t')
        rows.append(cells)
    return rows


def main():
    spec = json.loads(show(FREEZE, '.ufo/waves/round-40/c1/carriers.json'))
    out = {'freeze': FREEZE, 'target': spec.get('target'), 'carriers': {}}
    unsatisfiable = []
    for c in spec['carriers']:
        cid = c['id']
        oracle = {r[0]: r[1] for r in table(FREEZE, c['oracle'])}
        non = [(r[0], r[1]) for r in table(FREEZE, c['nonregular'])]

        # Q1: an oracle rel that the non-regular matcher would also claim
        direct = [(o, n) for o in oracle for n, _k in non if same_rel(o, n)]

        # Q2: entailment -- P matches oracle rel R and R matches non-regular N
        entail = []
        for (o, n) in direct:
            # every published P with same_rel(P, o) also has same_rel(P, n)
            # when o endswith '/' + n (or n endswith o, in which case P may not)
            if o.endswith('/' + n) or o == n:
                entail.append({'published_satisfying_oracle': o.replace(o, '<prefix>/' + o),
                               'oracle_rel': o, 'nonregular_rel': n,
                               'reason': 'oracle rel %r ends with %r, so any published path '
                                         'matching %r also matches %r' % (o, '/' + n, o, n)})

        # brute check on the *bare* oracle set as it would be published (prefix 'X_extract/')
        published = ['X_extract/' + o for o in oracle]
        oracle_hits = sum(1 for o in oracle
                          if any(same_rel(p, o) for p in published))
        nonreg_claimed = [p for p in published if any(same_rel(p, n) for n, _ in non)]
        both = oracle_hits == len(oracle) and not nonreg_claimed

        out['carriers'][cid] = {
            'oracle_rows': len(oracle), 'nonregular_rows': len(non),
            'direct_collisions': direct,
            'entailed_collisions': entail,
            'publishing_the_whole_oracle_satisfies_oracle_hits': oracle_hits == len(oracle),
            'same_set_violates_nonregular_unpublished_ok': bool(nonreg_claimed),
            'nonregular_paths_claimed': nonreg_claimed,
            'jointly_satisfiable': both,
        }
        if not both:
            unsatisfiable.append(cid)
    out['carriers_with_unsatisfiable_clause_pair'] = unsatisfiable
    out['target_reachable'] = not unsatisfiable
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0 if not unsatisfiable else 1


if __name__ == '__main__':
    sys.exit(main())
