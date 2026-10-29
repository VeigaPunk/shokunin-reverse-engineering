#!/usr/bin/env python3
"""Two probes for the surviving C1 counter mutants.

P1: is `--full-history` in `all_adds` load-bearing?  Rebuild the selftest's
merge topology and compare `git log -m --diff-filter=A` with and without
`--full-history`, plus a variant where the side branch is NOT TREESAME.

P2: is the 'R' status code in frozen_drift's `code in 'MDRTU'` masked by the
endpoint blob comparison?  Rebuild a fixture where a frozen path is renamed
after the freeze and check both arms.
"""
import json
import os
import shutil
import subprocess
import sys

S = '/fast/scratch/hyaku/kaidoku-r50/w3-MutPlan'
FIX = os.path.join(S, 'probe-fixtures')


def run(cmd, cwd, check=True):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=check)


def init(d):
    if os.path.exists(d):
        shutil.rmtree(d)
    os.makedirs(d)
    run(['git', 'init', '-q'], d)
    run(['git', 'config', 'user.name', 'fx'], d)
    run(['git', 'config', 'user.email', 'fx@fx'], d)


def write(d, path, content):
    full = os.path.join(d, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as fh:
        fh.write(content)


def commit(d, msg):
    run(['git', 'add', '-A'], d)
    run(['git', 'commit', '-qm', msg, '--allow-empty'], d)
    return run(['git', 'rev-parse', 'HEAD'], d).stdout.strip()


def p1():
    """Three merge topologies over a receipt path; compare `git log -m
    --diff-filter=A` with and without `--full-history`.

    T1 is the selftest topology: the receipt is added pre-freeze on a side
    branch AND re-added post-freeze on main, then the side branch is merged.
    T2: the receipt is added pre-freeze on the side branch only; the merge
    brings it in after the freeze.
    T3: the receipt is added post-freeze on main only (the control).
    """
    out = {}
    for tag, mode in (('T1_side_add_plus_main_readd', 'both'),
                      ('T2_side_add_only_then_merge', 'side_only'),
                      ('T3_main_add_only_control', 'main_only')):
        d = os.path.join(FIX, 'p1-' + tag)
        init(d)
        write(d, 'base.txt', 'b\n')
        commit(d, 'base')
        run(['git', 'checkout', '-q', '-b', 'side'], d)
        write(d, 'rcpt/after.json', '{"a":1}\n')
        commit(d, 'side pre-freeze add')
        run(['git', 'checkout', '-q', '-'], d)
        write(d, 'main.txt', 'm\n')
        commit(d, 'main pre-freeze')
        if mode in ('both', 'main_only'):
            write(d, 'rcpt/after.json', '{"a":1}\n')
            commit(d, 'main post-freeze add')
        run(['git', 'merge', '--no-ff', '--no-commit', '-q', 'side'], d)
        commit(d, 'merge')
        head = run(['git', 'rev-parse', 'HEAD'], d).stdout.strip()
        res = {}
        for label, extra in (('with_full_history', ['--full-history']),
                             ('without_full_history', [])):
            p = run(['git', 'log', '-m'] + extra + ['--diff-filter=A',
                    '--format=%H', head, '--', 'rcpt/after.json'], d, check=False)
            res[label] = {'exit': p.returncode,
                          'commits': [x for x in p.stdout.split() if x],
                          'stdout_sha256': __import__('hashlib').sha256(
                              p.stdout.encode()).hexdigest()}
        out[tag] = {'head': head, 'log': res}
    return out


def p2():
    """frozen_drift: a frozen path renamed after the freeze."""
    d = os.path.join(FIX, 'p2-rename')
    init(d)
    write(d, 'plans/claims.md', 'plan\n')
    write(d, 'other.txt', 'x\n')
    freeze = commit(d, 'freeze')
    run(['git', 'mv', 'plans/claims.md', 'plans/claims-renamed.md'], d)
    commit(d, 'rename the frozen path')
    rev = run(['git', 'rev-parse', 'HEAD'], d).stdout.strip()
    # the walk's own arms
    p = run(['git', '-c', 'core.quotePath=false', 'log', '-m',
             '--diff-merges=first-parent', '--name-status', '--pretty=format:',
             '%s..%s' % (freeze, rev)], d, check=False)
    walk_lines = [l for l in p.stdout.splitlines() if l.strip()]
    blob_old = run(['git', 'rev-parse', '%s:plans/claims.md' % rev], d, check=False)
    blob_new = run(['git', 'rev-parse', '%s:plans/claims-renamed.md' % rev], d,
                   check=False)
    return {
        'freeze': freeze, 'rev': rev,
        'walk_lines': walk_lines,
        'old_path_at_rev_exit': blob_old.returncode,
        'old_path_at_rev_out': blob_old.stdout.strip(),
        'new_path_at_rev_exit': blob_new.returncode,
        'new_path_at_rev_out': blob_new.stdout.strip(),
    }


def main():
    os.makedirs(FIX, exist_ok=True)
    res = {'p1_full_history': p1(), 'p2_rename_drift': p2()}
    with open(os.path.join(S, 'survivor-probes.json'), 'w', encoding='utf-8') as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
    print(json.dumps(res, indent=1, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
