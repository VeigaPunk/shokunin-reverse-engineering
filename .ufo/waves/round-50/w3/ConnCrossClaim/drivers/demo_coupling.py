#!/usr/bin/env python3
"""Fixture driver: exercise the frozen counters' freeze-integrity walks against
three simulated C3 landing shapes (branch tips in the scratch clone).

Read-only w.r.t. the lane: it loads the frozen counter modules from the clone
and calls the exact functions c1 measure() / c2 evaluate() use.
"""
import importlib.util
import json
import subprocess
import sys

CLONE = '/fast/scratch/hyaku/kaidoku-r50/w3-ConnCrossClaim/clone'
FREEZE = '435d41fd4ad9211d1579fc447936fb33d2b74467'
TIPS = {
    'A-tools-round-50': '94749500263626bd3be41b2d46bc28a986733e8d',
    'B-tools-round-50c3': '509a3d54aec9dadfd2f10f673aaf6f0d66f0f60c',
    'C-docs-only': 'd1c4dc054d4ba63a774198d198d7487fcc79cde8',
}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git(*args):
    return subprocess.run(['git', '-C', CLONE] + list(args), capture_output=True)


c1 = load('c1counter', CLONE + '/tools/round-50/c1-counter.py')
c2 = load('c2record', CLONE + '/tools/round-50/c2-record.py')

spec = json.loads(git('show', f'{FREEZE}:tools/round-50/carriers.json').stdout)

print('frozen counters loaded from clone (byte-identical to lane tip)')
print('c1 COUNTER_PATH sha256 check vs freeze:',
      c1.sha256_bytes(git('show', f'{FREEZE}:tools/round-50/c1-counter.py').stdout)
      == c1.file_sha256(CLONE + '/tools/round-50/c1-counter.py'))
print()

for label, tip in TIPS.items():
    print('=== branch', label, tip[:12], '===')
    # --- C1 side: the exact call measure() makes before any scoring
    drift = c1.frozen_drift(CLONE, FREEZE, tip, spec)
    print('c1 frozen_drift ->', json.dumps(drift))
    if drift:
        print('c1 measure() would raise FrozenPathChanged -> receipt '
              '{"reason": "frozen_path_changed", "exit_code": 2} (met_target never computed)')
    else:
        print('c1 frozen walk clean; scoring would proceed to clauses/bindings')
    # --- C2 side: the exact call evaluate() makes before scoring atoms
    g = c2.Git(CLONE)
    msg, why = c2.freeze_check(g, FREEZE, tip)
    print('c2 freeze_check ->', json.dumps({'problem': msg, 'code': why}))
    t = g.touched(FREEZE, tip)
    print('c2 touched(FROZEN pathspecs) ->', json.dumps(t))
    a, b = g.tree(FREEZE, *c2.FROZEN), g.tree(tip, *c2.FROZEN)
    diff = sorted(p for p in set(a) | set(b) if a.get(p) != b.get(p))
    print('c2 tree diff under', c2.FROZEN, '->', json.dumps(diff))
    print()
