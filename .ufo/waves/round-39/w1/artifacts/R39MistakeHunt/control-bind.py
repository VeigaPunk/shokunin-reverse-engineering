#!/usr/bin/env python3
"""control-bind.py — a control receipt must name the freeze it was scored against and a
revision that exists.

QUALITY 73 (receipt states what produced it) and QUALITY 80 (controls land in the freeze)
both fail silently when a receipt is re-scored in place: the path still resolves, the exit
still looks like a control's, but `--rev/--freeze` now point at the amendment, or at nothing.

Checks, per control receipt at REV:
  argv_binds_freeze   argv contains --rev and --freeze
  freeze_is_claim     --freeze equals the claim's first freeze commit
  revision_resolves   --rev, and any output.revision, are objects in the repo
  path_is_freeze_copy (optional) the receipt bytes equal those first added at the freeze tip

Usage:
  control-bind.py --lane DIR --rev REV --freeze SHA --controls DIR [--freeze-tip REV]
  control-bind.py --selftest

Exit 0 = all controls bound; 1 = any failure; 2 = unevaluable.
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


def exists(lane, rev):
    if not rev:
        return False
    rc, _ = git(lane, 'cat-file', '-e', f'{rev}^{{commit}}')
    return rc == 0


def argv_pair(argv, key):
    for i, a in enumerate(argv[:-1]):
        if a == key:
            return argv[i + 1]
    return None


def evaluate(lane, rev, freeze, controls, freeze_tip=None, quiet=False):
    rc, out = git(lane, 'ls-tree', '-r', '--name-only', rev, '--', controls)
    if rc != 0:
        print(f"UNEVALUABLE ls-tree failed for {controls}@{rev}")
        return 2
    files = [f for f in out.splitlines() if f.endswith('.json')]
    if not files:
        print(f"UNEVALUABLE no control receipts under {controls}@{rev}")
        return 2
    fails = 0
    for f in files:
        rc, blob = git(lane, 'show', f'{rev}:{f}')
        if rc != 0:
            print(f"  {os.path.basename(f)}: UNREADABLE")
            fails += 1
            continue
        try:
            d = json.loads(blob)
        except json.JSONDecodeError:
            print(f"  {os.path.basename(f)}: UNPARSEABLE")
            fails += 1
            continue
        argv = d.get('argv') or []
        r_arg = argv_pair(argv, '--rev')
        f_arg = argv_pair(argv, '--freeze')
        out_rev = (d.get('output') or {}).get('revision')
        bad = []
        if not (r_arg and f_arg):
            bad.append('argv_binds_freeze')
        if f_arg and f_arg != freeze:
            bad.append(f'freeze_is_claim(freeze={f_arg[:8]}!=claim)')
        if r_arg and not exists(lane, r_arg):
            bad.append(f'revision_resolves(--rev {r_arg[:8]} absent)')
        if out_rev and not exists(lane, out_rev):
            bad.append(f'revision_resolves(output.revision {out_rev[:8]} absent)')
        if freeze_tip:
            rc0, at_freeze = git(lane, 'show', f'{freeze_tip}:{f}')
            if rc0 == 0 and at_freeze != blob:
                bad.append(f'path_is_freeze_copy(bytes differ from {freeze_tip[:8]})')
        if not quiet:
            print(f"  {os.path.basename(f)}: exit={d.get('exit')} "
                  f"{'BOUND' if not bad else 'FAIL ' + '; '.join(bad)}")
        fails += bool(bad)
    if fails:
        print(f"VERDICT controls_unbound={fails}/{len(files)}")
        return 1
    print(f"VERDICT controls_bound={len(files)}/{len(files)}")
    return 0


def selftest():
    d = tempfile.mkdtemp(prefix='cb-')
    subprocess.run(['git', '-C', d, 'init', '-q'], check=True)
    g = lambda *a: subprocess.run(['git', '-C', d, '-c', 'user.name=fx', '-c', 'user.email=fx@fx', *a],
                                  check=True, capture_output=True)
    os.makedirs(os.path.join(d, 'ctl'))
    open(os.path.join(d, 'ctl', 'seed'), 'w').write('x\n')
    g('add', '-A'); g('commit', '-qm', 'freeze')
    freeze = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    good = {'argv': ['gen.py', 'c1-0', '--rev', freeze, '--freeze', freeze], 'exit': 1,
            'output': {'met_target': False}}
    json.dump(good, open(os.path.join(d, 'ctl', 'good.json'), 'w'))
    g('add', '-A'); g('commit', '-qm', 'control at freeze')
    tip = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    amend = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD~0'], capture_output=True, text=True).stdout.strip()
    # red: re-pointed at a later commit and stripped of argv binding, plus an unresolvable revision
    bad = {'argv': ['gen.py', 'c1-1', '--pkg65', 'x'], 'exit': 1,
           'output': {'revision': 'deadbeef' * 5, 'met_target': False}}
    json.dump(bad, open(os.path.join(d, 'ctl', 'bad.json'), 'w'))
    g('add', '-A'); g('commit', '-qm', 'repointed')
    repointed = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    rc_good = evaluate(d, tip, freeze, 'ctl', quiet=True)
    rc_bad = evaluate(d, repointed, freeze, 'ctl', freeze_tip=tip, quiet=True)
    print(f"selftest green(bound control)   rc={rc_good} (want 0)")
    print(f"selftest red(unbound control)   rc={rc_bad} (want 1)")
    ok = rc_good == 0 and rc_bad == 1
    print("selftest", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane')
    ap.add_argument('--rev')
    ap.add_argument('--freeze')
    ap.add_argument('--controls')
    ap.add_argument('--freeze-tip')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.lane and a.rev and a.freeze and a.controls):
        ap.error('--lane --rev --freeze --controls are required')
    return evaluate(a.lane, a.rev, a.freeze, a.controls, a.freeze_tip)


if __name__ == '__main__':
    sys.exit(main())
