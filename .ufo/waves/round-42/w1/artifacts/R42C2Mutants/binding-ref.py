#!/usr/bin/env python3
"""R42C2Mutants -- micro-reference + mutants for the A1 counter bindings.

Private harness (not a deliverable).  Implements only the three bindings the
A1 draft adds or carries for the v4 counter, each in its minimal form:

  counter_sha256            D4: the receipt records the sha256 of the counter
                            file that ran, compared to the pin by full equality
  lookup_combo_below_half   CTL-C2-7 binding: the frozen exact lookup control
                            labels strictly fewer than half of the held-out
                            combos right (denominator = the held-out total)
  combo_unseen_majority     at least half of the held-out combos have an
                            observed tuple outside the union of the dev
                            named-class declared tuples

`--selftest` pins the boundary semantics; each mutant must break exactly the
pinned case and no other.
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REF_SRC = '''import hashlib, os, sys

def counter_sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()

def lookup_combo_below_half(score, total):
    return 2 * score < total

def combo_unseen_majority(unseen, total):
    return 2 * unseen >= total

def sha_matches_pin(digest, pin):
    return digest == pin

def main():
    ok = True
    def check(name, got, want):
        nonlocal ok
        if got != want:
            ok = False
            print("FAIL %s: got %r want %r" % (name, got, want))
        else:
            print("ok %s" % name)
    check("lookup-3-of-8", lookup_combo_below_half(3, 8), True)
    check("lookup-4-of-8-exactly-half", lookup_combo_below_half(4, 8), False)
    check("lookup-5-of-8", lookup_combo_below_half(5, 8), False)
    check("lookup-3-matched-of-12-heldout", lookup_combo_below_half(3, 12), True)
    check("unseen-6-of-12-exactly-half", combo_unseen_majority(6, 12), True)
    check("unseen-5-of-12", combo_unseen_majority(5, 12), False)
    check("unseen-7-of-12", combo_unseen_majority(7, 12), True)
    me = os.path.abspath(sys.argv[0])
    digest = counter_sha256(me)
    check("sha-self-is-file-bytes", digest == hashlib.sha256(open(me, "rb").read()).hexdigest(), True)
    check("sha-pin-full-equality", sha_matches_pin(digest, digest[:8] + "0" * 56), False)
    check("sha-pin-self", sha_matches_pin(digest, digest), True)
    check("sha-pin-f64", sha_matches_pin(digest, "f" * 64), False)
    print("BINDING-SELFTEST %s" % ("pass" if ok else "FAIL"))
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
'''

MUTANTS = {
    'NM-C2-lookup-le': [(
        'def lookup_combo_below_half(score, total):\n    return 2 * score < total',
        'def lookup_combo_below_half(score, total):\n    return 2 * score <= total')],
    'NM-C3-lookup-denominator': [(
        'def lookup_combo_below_half(score, total):\n    return 2 * score < total',
        'def lookup_combo_below_half(score, total):\n'
        '    return 2 * score < 3  # denominator defect: the control output lists 3 combos')],
    'NM-C4-majority-gt': [(
        'def combo_unseen_majority(unseen, total):\n    return 2 * unseen >= total',
        'def combo_unseen_majority(unseen, total):\n    return 2 * unseen > total')],
    'NM-C5-sha-of-argv': [(
        'def counter_sha256(path):\n'
        '    with open(path, "rb") as fh:\n'
        '        return hashlib.sha256(fh.read()).hexdigest()',
        'def counter_sha256(path):\n'
        '    return hashlib.sha256(path.encode()).hexdigest()')],
    'NM-C6-sha-prefix-pin': [(
        'def sha_matches_pin(digest, pin):\n    return digest == pin',
        'def sha_matches_pin(digest, pin):\n    return digest[:8] == pin[:8]')],
}

EXPECTED_FIRST_FAIL = {
    'NM-C2-lookup-le': 'lookup-4-of-8-exactly-half',
    'NM-C3-lookup-denominator': 'lookup-3-of-8',
    'NM-C4-majority-gt': 'unseen-6-of-12-exactly-half',
    'NM-C5-sha-of-argv': 'sha-self-is-file-bytes',
    'NM-C6-sha-prefix-pin': 'sha-pin-full-equality',
}


def run(path):
    p = subprocess.run([sys.executable, '-I', '-B', path],
                       capture_output=True, text=True, timeout=60)
    fails = [l.split()[1].rstrip(':') for l in p.stdout.splitlines()
             if l.startswith('FAIL ')]
    return p.returncode, fails, p.stdout


def main():
    mutdir = os.path.join(os.path.dirname(HERE), 'muts')
    os.makedirs(mutdir, exist_ok=True)
    ref = os.path.join(mutdir, 'binding-ref.py')
    with open(ref, 'w', encoding='utf-8') as fh:
        fh.write(REF_SRC)
    rc, fails, out = run(ref)
    pristine_ok = rc == 0 and not fails
    print('pristine: exit=%d %s' % (rc, 'pass' if pristine_ok else out))
    rows = [{'probe': 'pristine', 'exit': rc, 'failures': fails, 'ok': pristine_ok}]
    for mid, patches in sorted(MUTANTS.items()):
        src = REF_SRC
        for old, new in patches:
            n = src.count(old)
            assert n == 1, '%s anchor x%d' % (mid, n)
            src = src.replace(old, new)
        mp = os.path.join(mutdir, 'binding-%s.py' % mid)
        with open(mp, 'w', encoding='utf-8') as fh:
            fh.write(src)
        rc, fails, out = run(mp)
        killed = rc != 0 and EXPECTED_FIRST_FAIL[mid] in fails
        rows.append({'probe': mid, 'exit': rc, 'failures': fails,
                     'expected_first_fail': EXPECTED_FIRST_FAIL[mid],
                     'killed': killed})
        print('%-26s exit=%d first_fail=%r killed=%s'
              % (mid, rc, fails[:1], killed))
    with open(os.path.join(os.path.dirname(HERE), 'out',
                           'binding-mutants.json'), 'w') as fh:
        json.dump(rows, fh, indent=1, sort_keys=True)
    print('DONE pristine_ok=%s all_killed=%s'
          % (pristine_ok, all(r.get('killed') for r in rows[1:])))


if __name__ == '__main__':
    main()
