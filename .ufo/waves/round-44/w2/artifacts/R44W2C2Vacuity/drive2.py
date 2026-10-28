#!/usr/bin/env python3
"""Grid runs: for each mutant ref, the scored configuration and the
--pre-freeze isolation configuration (freeze walk reported, not enforced)."""
import hashlib
import json
import os
import subprocess
import time

S = os.path.dirname(os.path.abspath(__file__))
CLONE = os.path.join(S, 'clone')
COUNTER = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-44/c2-counter.py'
FREEZE = 'c48f8a4bfd449300c975668e59aae5b5538b6a84'


def counter(rev, freeze, tag, pre_freeze=False):
    out = os.path.join(S, 'out', tag + '.json')
    argv = ['python3', '-I', '-B', COUNTER, '--root', CLONE, '--rev', rev,
            '--freeze', freeze, '--work', os.path.join(S, 'work'),
            '--json-out', out]
    if pre_freeze:
        argv.append('--pre-freeze')
    t0 = time.time()
    p = subprocess.run(argv, capture_output=True, text=True)
    wall = time.time() - t0
    data = None
    if os.path.exists(out):
        with open(out) as h:
            data = json.load(h)
    rec = {'exit_code': p.returncode, 'wall_seconds': round(wall, 3),
           'stdout_sha256': hashlib.sha256(p.stdout.encode()).hexdigest(),
           'argv': argv[3:]}
    if data:
        rec.update({
            'entries_evaluated': data.get('entries_evaluated'),
            'mismatches': data.get('mismatches'),
            'frozen_path_changed': data.get('frozen_path_changed'),
            'unevaluable': [u.get('reason') for u in data.get('unevaluable') or []],
            'observed_by_id': {e['id']: e.get('observed')
                               for e in data.get('entries') or []},
        })
    return rec


def main():
    with open(os.path.join(S, 'out', 'probes.json')) as h:
        probes = json.load(h)['probes']
    grid = []
    for p in probes:
        commit = p['mutant_commit']
        a = counter(commit, FREEZE, p['probe'] + '.A')
        b = counter(commit, FREEZE, p['probe'] + '.B', pre_freeze=True)
        row = {
            'probe': p['probe'], 'entry': p['entry'], 'class': p['class'],
            'path': p['path'], 'note': p['note'],
            'mutant_commit': commit,
            'scored_A': {k: a[k] for k in ('exit_code', 'mismatches',
                                           'frozen_path_changed',
                                           'entries_evaluated',
                                           'stdout_sha256', 'wall_seconds')},
            'isolation_B': {k: b[k] for k in ('exit_code', 'mismatches',
                                               'frozen_path_changed',
                                               'entries_evaluated',
                                               'stdout_sha256', 'wall_seconds')},
            'observed_of_entry_B': b['observed_by_id'].get(p['entry']),
            'entry_matched_B': p['entry'] not in (b['mismatches'] or []),
        }
        grid.append(row)
        print(json.dumps(row, sort_keys=True))
    with open(os.path.join(S, 'out', 'grid.json'), 'w') as h:
        json.dump(grid, h, indent=1, sort_keys=True)


if __name__ == '__main__':
    main()
