#!/usr/bin/env python3
"""R41C2Mutants phase 3: derive the >=10 new mutants on the clauses v3 adds,
run each preview's --selftest, and verify each mutant is killed by its own
case while the pristine previews pass everything."""
import hashlib
import json
import os
import subprocess
import sys

S = '/fast/scratch/hyaku/kaidoku-r41/R41C2Mutants'

INTERP_SRC = open(S + '/v3-interp-preview.py', encoding='utf-8').read()
COUNTER_SRC = open(S + '/v3-counter-preview.py', encoding='utf-8').read()

INTERP_MUTANTS = [
    ('N04-contains-parsed-as-exact',
     'contains cell matched as an exact set (operator silently dropped)',
     "        return payload <= frozenset(values)",
     "        return payload == frozenset(values)",
     ('partial+in-tree',)),
    ('N05-contains-accepted-in-deps-column',
     'the ⊇ operator accepted in the dependencies column too (grammar scope widened)',
     "        if column != 'gap kinds':\n"
     "            raise TableError('the %r operator is allowed only in the gap kinds column, '\n"
     "                             'not in %s' % (CONTAINS_OP, column))\n"
     "        contains = True",
     "        contains = True",
     ('deps-contains',)),
    ('N06-contains-repeated-member-accepted',
     'repeated-member check disabled for contains cells',
     "    if len(set(parts)) != len(parts):",
     "    if len(set(parts)) != len(parts) and False:",
     ('contains-dup',)),
    ('N07-rules-reversed',
     'classify iterates reversed(rules) (last match wins; precedence rows reordered)',
     "    for rule in rules:",
     "    for rule in reversed(rules):",
     ('partial+mixed',)),
]

COUNTER_MUTANTS = [
    ('N08-evaluator-compare-label-only',
     'evaluator-vs-table comparison drops the action half',
     "    return a is not None and b is not None and list(a) == list(b)",
     "    return a is not None and b is not None and a[0] == b[0]",
     ('eval-action-dev',)),
    ('N09-evaluator-crash-backfilled',
     'a crashed evaluator is backfilled from the table answer (scored against itself)',
     "        epair[c['id']] = pe",
     "        epair[c['id']] = pe if pe is not None else pi",
     ('eval-crash',)),
    ('N10-evaluator-first-replicate-only',
     'evaluator-vs-table comparison samples only the first replicate per class',
     "        pairs_equal(tpair.get(cid), epair.get(cid)) for cid in ids)",
     "        pairs_equal(tpair.get(cid), epair.get(cid)) for cid in ids[::2])",
     ('eval-dev-second-replicate',)),
    ('N11-class-expected-dropped',
     'class_expected binding vacuated (disagreement no longer computed)',
     "    b['class_expected_agrees'] = bool(carriers) and all(\n"
     "        pairs_equal((c.get('expected_label'), c.get('expected_action')),\n"
     "                    epair.get(c['id']))\n"
     "        for c in carriers)",
     "    b['class_expected_agrees'] = True",
     ('gen-label-disagrees',)),
    ('N12-class-expected-not-gating',
     'class_expected recorded but excluded from bindings_ok (reported, not failed)',
     "    bindings_ok = all(v is True for v in b.values())",
     "    bindings_ok = all(v is True for k, v in b.items()\n"
     "                      if k != 'class_expected_agrees')",
     ('gen-label-disagrees',)),
    ('N13-class-expected-first-replicate-only',
     'class_expected binding samples only the first replicate per class',
     "        for c in carriers)",
     "        for c in carriers[::2])",
     ('gen-dev-second-replicate',)),
]


def apply(src, old, new, mid):
    n = src.count(old)
    if n != 1:
        raise SystemExit('%s: anchor count %d' % (mid, n))
    return src.replace(old, new)


def selftest(path):
    p = subprocess.run([sys.executable, '-I', '-B', path, '--selftest'],
                       capture_output=True, text=True, timeout=600)
    fails = [l[5:] for l in p.stdout.splitlines() if l.startswith('FAIL ')]
    return {'exit': p.returncode, 'fails': fails}


def main():
    os.makedirs(S + '/preview-mutants', exist_ok=True)
    results = {}
    pris_i = selftest(S + '/v3-interp-preview.py')
    pris_c = selftest(S + '/v3-counter-preview.py')
    results['pristine_interp'] = pris_i
    results['pristine_counter'] = pris_c
    print('pristine interp selftest: exit=%d fails=%d' % (pris_i['exit'], len(pris_i['fails'])))
    print('pristine counter selftest: exit=%d fails=%d' % (pris_c['exit'], len(pris_c['fails'])))
    for mid, desc, old, new, own_cases in INTERP_MUTANTS:
        mpath = S + '/preview-mutants/interp-%s.py' % mid
        open(mpath, 'w').write(apply(INTERP_SRC, old, new, mid))
        r = selftest(mpath)
        killed = r['exit'] != 0 and all(any(c in f for f in r['fails'])
                                        for c in own_cases)
        results[mid] = {'src': 'v3-interp-preview.py', 'desc': desc,
                        'mutant_sha256': hashlib.sha256(open(mpath, 'rb').read()).hexdigest(),
                        'selftest': r, 'own_cases': list(own_cases),
                        'verdict': 'KILLED' if killed else
                        ('killed-other' if r['exit'] != 0 else 'SURVIVED')}
        print('%-42s %-13s n_fail=%d %s' % (mid, results[mid]['verdict'],
                                            len(r['fails']), r['fails'][:2]), flush=True)
    for mid, desc, old, new, own_cases in COUNTER_MUTANTS:
        mpath = S + '/preview-mutants/counter-%s.py' % mid
        open(mpath, 'w').write(apply(COUNTER_SRC, old, new, mid))
        r = selftest(mpath)
        killed = r['exit'] != 0 and all(any(c in f for f in r['fails'])
                                        for c in own_cases)
        results[mid] = {'src': 'v3-counter-preview.py', 'desc': desc,
                        'mutant_sha256': hashlib.sha256(open(mpath, 'rb').read()).hexdigest(),
                        'selftest': r, 'own_cases': list(own_cases),
                        'verdict': 'KILLED' if killed else
                        ('killed-other' if r['exit'] != 0 else 'SURVIVED')}
        print('%-42s %-13s n_fail=%d %s' % (mid, results[mid]['verdict'],
                                            len(r['fails']), r['fails'][:2]), flush=True)
    with open(S + '/preview-mutant-results.json', 'w') as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
    print('WROTE preview-mutant-results.json', flush=True)


if __name__ == '__main__':
    main()
