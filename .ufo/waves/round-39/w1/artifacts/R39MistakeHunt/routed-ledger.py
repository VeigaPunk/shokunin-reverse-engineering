#!/usr/bin/env python3
"""routed-ledger.py — every routed defect of a closure must reappear, with a state,
in the round that inherits it.

A closure file (corpus/lessons/round-NN-verifier-spotcheck.md) lists routed defects as
`R<round>-CL<k>`. The next round's lesson and report must name each id. A round that
silently drops an id loses the defect: nothing else in the lane remembers it.

Usage:
  routed-ledger.py --closure FILE --next FILE[,FILE...]     real run
  routed-ledger.py --selftest                               red/green fixtures

Exit 0 = every closure id named in at least one --next file.
Exit 1 = at least one id missing (each printed), or a file unreadable.
Exit 2 = unevaluable (no routed ids found in the closure).
"""
import argparse
import re
import sys
import tempfile
import os

ID = re.compile(r'\bR(\d+)-CL(\d+)\b')


def ids_in(path, sectioned=False):
    try:
        text = open(path, encoding='utf-8').read()
    except OSError as e:
        print(f"UNREADABLE {path}: {e}")
        return None
    if sectioned:
        m = re.search(r'^#+ .*Routed defects.*$', text, re.M)
        if m:
            rest = text[m.end():]
            nxt = re.search(r'^#+ ', rest, re.M)
            text = rest[:nxt.start()] if nxt else rest
    out = []
    for m in ID.finditer(text):
        ident = f"R{m.group(1)}-CL{m.group(2)}"
        if ident not in out:
            out.append(ident)
    return out


def run(closure, nexts, quiet=False):
    want = ids_in(closure, sectioned=True)
    if want is None:
        return 2
    if not want:
        print(f"UNEVALUABLE {closure}: no R<n>-CL<k> ids")
        return 2
    have = {}
    for n in nexts:
        ids = ids_in(n)
        if ids is None:
            return 2
        for i in ids:
            have.setdefault(i, []).append(n)
    missing = [i for i in want if i not in have]
    if not quiet:
        print(f"closure {closure}: {len(want)} routed ids {want}")
        for i in want:
            state = "named in " + ",".join(os.path.basename(p) for p in have[i]) if i in have else "DROPPED"
            print(f"  {i}: {state}")
    if missing:
        print(f"VERDICT missing={len(missing)}/{len(want)} {missing}")
        return 1
    print(f"VERDICT complete={len(want)}/{len(want)}")
    return 0


def selftest():
    d = tempfile.mkdtemp(prefix='rl-')
    closure = os.path.join(d, 'closure.md')
    open(closure, 'w').write(
        "## Routed defects\n- **R41-CL1.** alpha\n- **R41-CL2.** beta\n- **R41-CL3.** gamma\n")
    good = os.path.join(d, 'lesson-good.md')
    open(good, 'w').write("| M39-1 | ... | R41-CL1 closed |\nR41-CL2 open\nR41-CL3 closed\n")
    bad = os.path.join(d, 'lesson-bad.md')
    open(bad, 'w').write("| M39-1 | ... | R41-CL1 closed |\n")
    rc_good = run(closure, [good], quiet=True)
    rc_bad = run(closure, [bad], quiet=True)
    print(f"selftest green(complete) rc={rc_good} (want 0)")
    print(f"selftest red(dropped)   rc={rc_bad} (want 1)")
    ok = rc_good == 0 and rc_bad == 1
    print("selftest", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--closure')
    ap.add_argument('--next', default='')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.closure or not a.next:
        ap.error('--closure and --next are required')
    return run(a.closure, [p for p in a.next.split(',') if p])


if __name__ == '__main__':
    sys.exit(main())
