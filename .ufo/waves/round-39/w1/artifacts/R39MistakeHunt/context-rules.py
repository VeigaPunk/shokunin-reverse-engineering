#!/usr/bin/env python3
"""context-rules.py — a rule that lives only in a wave spec's hand-written context lapses.

Every wave spec carries a `context` string that seats inherit. A scratch/misroot rule
recorded as a lesson fix must appear in *every* spec from that round on; a rule that was
typed into one wave's context disappears the next round (M36-6 -> absent at r38/r39).

Usage:
  context-rules.py --require NAME=REGEX [--require ...] SPEC.json [SPEC.json ...]
  context-rules.py --selftest

Exit 0 = every required rule present in every spec; 1 = a spec misses a rule; 2 = unreadable.
"""
import argparse
import json
import os
import re
import sys
import tempfile

RULES = {
    # M36-6: other lanes' trees live under /fast/scratch; a find/du there is a misroot risk.
    'scratch-no-find-du': r'No\s+`?find`?\s*/\s*`?du`?\s+under\s+`?/fast/scratch',
    # M38-7: unblob writes ./unblob.log in its cwd; REA refuses a pre-existing outdir.
    'unblob-cd-scratch': r'cd\s+"\$S"',
    # every spec must pin TMPDIR into the seat's scratch
    'tmpdir-pinned': r'export\s+TMPDIR="\$S"',
}


def check(spec, rules, quiet=False):
    try:
        ctx = json.load(open(spec, encoding='utf-8')).get('context', '')
    except (OSError, json.JSONDecodeError) as e:
        print(f"UNREADABLE {spec}: {e}")
        return 2
    miss = []
    if not quiet:
        print(f"spec {spec} ({len(ctx)} B)")
    for name in rules:
        hit = bool(re.search(RULES[name], ctx))
        if not quiet:
            print(f"  {name}: {'present' if hit else 'ABSENT'}")
        if not hit:
            miss.append(name)
    if miss:
        print(f"VERDICT {os.path.basename(spec)} missing={miss}")
        return 1
    print(f"VERDICT {os.path.basename(spec)} complete")
    return 0


def selftest():
    d = tempfile.mkdtemp(prefix='cr-')
    good = os.path.join(d, 'good.json')
    json.dump({'context': 'S=/fast/scratch/hyaku/x; export TMPDIR="$S"; '
                          'No `find`/`du` under `/fast/scratch`; cd "$S" before REA.'},
              open(good, 'w'))
    bad = os.path.join(d, 'bad.json')
    json.dump({'context': 'S=/fast/scratch/hyaku/x; export TMPDIR="$S"; cd "$S" before REA.'},
              open(bad, 'w'))
    rc_good = check(good, list(RULES), quiet=True)
    rc_bad = check(bad, list(RULES), quiet=True)
    print(f"selftest green(all rules)   rc={rc_good} (want 0)")
    print(f"selftest red(missing rule)  rc={rc_bad} (want 1)")
    ok = rc_good == 0 and rc_bad == 1
    print("selftest", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--require', action='append', default=[])
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('specs', nargs='*')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    rules = []
    for r in a.require:
        name = r.split('=', 1)[0]
        if name not in RULES:
            ap.error(f'unknown rule {name}; known: {sorted(RULES)}')
        rules.append(name)
    if not rules:
        rules = list(RULES)
    rc = 0
    for s in a.specs:
        rc |= check(s, rules)
    return rc


if __name__ == '__main__':
    sys.exit(main())
