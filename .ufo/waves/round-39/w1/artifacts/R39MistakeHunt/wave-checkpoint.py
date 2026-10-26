#!/usr/bin/env python3
"""wave-checkpoint.py — a wave's reports must be committed by the time the wave is done.

The wave results ledger (`<wave>-results.json`) names every seat's report path. If the
ledger or any named report is absent from the tree at a revision, that wave's output
existed only in the working tree: a dead L1 or a lost workspace takes it with it.

Usage:
  wave-checkpoint.py --lane DIR --rev REV --wave PATH/TO/<wave>-results.json   real run
  wave-checkpoint.py --selftest                                              fixtures

credits WAVE-DONE only when, at REV:
  * the ledger file exists,
  * every report path named in results[].output.report exists,
  * every *.md directly in the ledger's directory is named by the ledger.

Exit 0 = checkpoint present, 1 = checkpoint missing/incomplete, 2 = unevaluable.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile


def git(lane, *args):
    p = subprocess.run(['git', '-C', lane, *args], capture_output=True, text=True)
    return p.returncode, p.stdout


def tree_files(lane, rev, path):
    rc, out = git(lane, 'ls-tree', '-r', '--name-only', rev, '--', path)
    if rc != 0:
        return None
    return [l for l in out.splitlines() if l]


def evaluate(lane, rev, ledger, quiet=False):
    rc, blob = git(lane, 'show', f'{rev}:{ledger}')
    if rc != 0:
        print(f"ledger absent at {rev}: {ledger}")
        return 1
    try:
        data = json.loads(blob)
    except json.JSONDecodeError as e:
        print(f"ledger unparseable at {rev}: {e}")
        return 2
    results = data.get('results') or []
    named, unbound = [], []
    for r in results:
        out = r.get('output')
        try:
            j = json.loads(out) if isinstance(out, str) else (out or {})
        except json.JSONDecodeError:
            j = {}
        rep = None
        if isinstance(j, dict):
            for key in ('report', 'report_path', 'artifact'):
                if isinstance(j.get(key), str) and j[key].strip():
                    rep = j[key].strip()
                    break
        if not rep:
            unbound.append(r.get('name'))
            continue
        # normalise: first whitespace-delimited token, absolute lane path -> repo-relative
        rep = rep.split()[0]
        if rep.startswith(lane.rstrip('/') + '/'):
            rep = rep[len(lane.rstrip('/')) + 1:]
        named.append(rep)
    wdir = os.path.dirname(ledger)
    present = set(tree_files(lane, rev, wdir) or [])
    missing = [p for p in named if p not in present]
    on_disk_reports = {p for p in present if p.endswith('.md') and os.path.dirname(p) == wdir}
    unnamed = sorted(on_disk_reports - set(named))
    if not quiet:
        print(f"ledger {ledger} at {rev}: results={len(results)} named_reports={len(named)} unbound_rows={len(unbound)}")
        print(f"  reports present in tree: {len(named) - len(missing)}/{len(named)}")
        for p in missing[:10]:
            print(f"  MISSING {p}")
        if unnamed:
            print(f"  unnamed report files ({len(unnamed)}): {unnamed[:5]}")
    if unbound:
        print(f"  rows with no report pointer ({len(unbound)}): {unbound[:8]}")
        print(f"VERDICT checkpoint_incomplete unbound_rows={len(unbound)} of {len(results)}")
        return 1
    if missing:
        print(f"VERDICT checkpoint_incomplete missing_reports={len(missing)}")
        return 1
    if unnamed:
        print(f"VERDICT checkpoint_incomplete unnamed_reports={len(unnamed)}")
        return 1
    print(f"VERDICT checkpoint_ok reports={len(named)}")
    return 0


def selftest():
    d = tempfile.mkdtemp(prefix='wc-')
    subprocess.run(['git', '-C', d, 'init', '-q'], check=True)
    g = lambda *a: subprocess.run(['git', '-C', d, '-c', 'user.name=fx', '-c', 'user.email=fx@fx', *a],
                                  check=True, capture_output=True)
    os.makedirs(os.path.join(d, 'w1'))
    open(os.path.join(d, 'w1', 'A.md'), 'w').write('a\n')
    open(os.path.join(d, 'w1', 'B.md'), 'w').write('b\n')
    ledger = os.path.join(d, 'w1', 'w1-results.json')
    open(ledger, 'w').write(json.dumps({'results': [
        {'output': json.dumps({'report': 'w1/A.md'})},
        {'output': json.dumps({'report': 'w1/B.md'})}], 'seats': 2}))
    g('add', '-A'); g('commit', '-qm', 'wave')
    good = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    # red case: the ledger claims a report that the tree no longer holds
    os.remove(os.path.join(d, 'w1', 'B.md'))
    open(os.path.join(d, 'w1', 'w1-results.json'), 'w').write(json.dumps({'results': [
        {'output': json.dumps({'report': 'w1/A.md'})},
        {'output': json.dumps({'report': 'w1/B.md'})}], 'seats': 2}))
    g('add', '-A'); g('commit', '-qm', 'ledger claims B')
    red = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    rc_good = evaluate(d, good, 'w1/w1-results.json', quiet=True)
    rc_red = evaluate(d, red, 'w1/w1-results.json', quiet=True)
    print(f"selftest green(committed wave) rc={rc_good} (want 0)")
    print(f"selftest red(lost report)      rc={rc_red} (want 1)")
    ok = rc_good == 0 and rc_red == 1
    print("selftest", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane')
    ap.add_argument('--rev')
    ap.add_argument('--wave')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.lane and a.rev and a.wave):
        ap.error('--lane --rev --wave are required')
    return evaluate(a.lane, a.rev, a.wave)


if __name__ == '__main__':
    sys.exit(main())
