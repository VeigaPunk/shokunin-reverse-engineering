#!/usr/bin/env python3
"""Follow-up probes.

P3: is the 'R' status code in frozen_drift load-bearing for a frozen path that
did NOT exist at FREEZE (the oracle-table case)?  The endpoint blob arm only
covers paths that exist at the freeze, so a rename of a not-yet-existing frozen
path may be caught by the status code alone.

P4: is `--full-history` in all_adds inert under `-m`, or merely untested?  Try
topologies designed to trigger git's history simplification.

P5: v5 precedence gap - a no-reader family run that FAILED but published
files (>0).  Which row decides it under the v5-shaped table (D)?
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

S = '/fast/scratch/hyaku/kaidoku-r50/w3-MutPlan'
FIX = os.path.join(S, 'probe-fixtures')
OUT = os.path.join(S, 'table-mut')
EVAL = os.path.join(OUT, 'sqfs-triage-v4.py')


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


def p3():
    """A frozen path that does NOT exist at FREEZE is renamed after the freeze."""
    d = os.path.join(FIX, 'p3-rename-absent-at-freeze')
    init(d)
    write(d, 'base.txt', 'b\n')
    freeze = commit(d, 'freeze')
    write(d, 'oracle/table.tsv', 'a\tb\t1\n')
    commit(d, 'add the oracle table (frozen path, first appears after the freeze)')
    run(['git', 'mv', 'oracle/table.tsv', 'oracle/table-moved.tsv'], d)
    rev = commit(d, 'rename it')
    p = run(['git', '-c', 'core.quotePath=false', 'log', '-m',
             '--diff-merges=first-parent', '--name-status', '--pretty=format:',
             '%s..%s' % (freeze, rev)], d, check=False)
    walk = [l for l in p.stdout.splitlines() if l.strip()]
    # the counter's frozen set includes oracle tables named by carriers.json; the
    # renamed path is present at REV under a NEW name, so the blob arm cannot
    # compare it at the old name.
    old = run(['git', 'rev-parse', '%s:oracle/table.tsv' % rev], d, check=False)
    new = run(['git', 'rev-parse', '%s:oracle/table-moved.tsv' % rev], d, check=False)
    return {'freeze': freeze, 'rev': rev, 'walk_lines': walk,
            'old_at_rev_exit': old.returncode, 'new_at_rev_exit': new.returncode,
            'walk_sha256': hashlib.sha256(p.stdout.encode()).hexdigest()}


def p4():
    """Topologies that trigger git history simplification, with and without
    --full-history, under the counter's exact `-m --diff-filter=A` form."""
    out = {}
    cases = {
        # side branch adds the receipt PRE-freeze; main never touches it; the
        # merge is TREESAME to main (identical trees) -> git may prune the side
        'side_only_treesame_merge': 'side_only',
        # side branch adds pre-freeze, main adds the SAME path post-freeze with
        # the same content -> the merge tree equals main's
        'side_add_and_main_readd_same_content': 'both_same',
        # side branch adds pre-freeze with DIFFERENT content; main adds the same
        # path post-freeze with different content -> conflict-free resolution
        'side_add_and_main_readd_diff_content': 'both_diff',
    }
    for tag, mode in cases.items():
        d = os.path.join(FIX, 'p4-' + tag)
        init(d)
        write(d, 'base.txt', 'b\n')
        commit(d, 'base')
        run(['git', 'checkout', '-q', '-b', 'side'], d)
        write(d, 'rcpt/after.json', '{"a":1}\n')
        commit(d, 'side pre-freeze add')
        run(['git', 'checkout', '-q', '-'], d)
        write(d, 'main.txt', 'm\n')
        commit(d, 'main pre-freeze')
        if mode == 'both_same':
            write(d, 'rcpt/after.json', '{"a":1}\n')
            commit(d, 'main post-freeze add (same content)')
        elif mode == 'both_diff':
            write(d, 'rcpt/after.json', '{"a":2}\n')
            commit(d, 'main post-freeze add (other content)')
        m = run(['git', 'merge', '--no-ff', '--no-commit', '-q', 'side'], d,
                check=False)
        if m.returncode != 0:
            run(['git', 'merge', '--abort'], d, check=False)
            out[tag] = {'merge_exit': m.returncode, 'merge_stderr': m.stderr[-200:]}
            continue
        commit(d, 'merge')
        head = run(['git', 'rev-parse', 'HEAD'], d).stdout.strip()
        res = {}
        for label, extra in (('with_full_history', ['--full-history']),
                             ('without_full_history', [])):
            p = run(['git', 'log', '-m'] + extra + ['--diff-filter=A',
                    '--format=%H', head, '--', 'rcpt/after.json'], d, check=False)
            res[label] = {'exit': p.returncode,
                          'commits': [x for x in p.stdout.split() if x],
                          'stdout_sha256': hashlib.sha256(
                              p.stdout.encode()).hexdigest()}
        res['identical'] = (res['with_full_history']['stdout_sha256'] ==
                            res['without_full_history']['stdout_sha256'])
        out[tag] = {'head': head, 'log': res}
    return out


def p5():
    """v5 precedence gap: a no-reader family run that failed but published a
    file (files > 0)."""
    env = {'ok': True, 'data': {
        'operation': 'extract_firmware',
        'provider': {'id': 'unblob', 'name': 'Unblob', 'version': '26.6.4'},
        'subject': {'name': 'x.bin', 'digest': {'sha256': 'b' * 64}},
        'parameters': {'output_directory': '/fast/scratch/hyaku/kaidoku-r50/x',
                       'max_depth': 3},
        'normalized_result': {
            'chunks': [{'handler': 'squashfs_v2_nonstandard',
                        'range': {'offset': 0, 'length': 4096},
                        'extraction_failed': True}],
            'extraction_gaps': [{'kind': 'extractor-failure',
                                 'handler': 'squashfs_v2_nonstandard',
                                 'relative_path': 'firmware.bin_extract/firmware.bin',
                                 'dependencies': ['sasquatch']}],
            'files': [{'relative_path': 'firmware.bin_extract/partial.txt',
                       'path': '/out/partial.txt', 'size': 4, 'sha256': 'c' * 64}],
            'diagnostics': []}}}
    syn = os.path.join(S, 'synthetic-envelopes')
    os.makedirs(syn, exist_ok=True)
    p = os.path.join(syn, 'v2ns_partial_failure.json')
    with open(p, 'w', encoding='utf-8') as fh:
        json.dump(env, fh, indent=1)
    out = {}
    for tag in ('baseline', 'D_v5_shaped_minimal', 'E_v5_shaped_plus_F1_narrow'):
        skill = os.path.join(OUT, 'SKILL-%s.md' % tag)
        cmd = [sys.executable, '-I', '-B', EVAL, '--skill', skill, '--json', p]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        rec = {'exit_code': r.returncode,
               'stdout_sha256': hashlib.sha256(r.stdout.encode()).hexdigest()}
        if r.returncode == 0:
            doc = json.loads(r.stdout)
            rec['label'] = [doc['results'][0]['label'],
                            doc['results'][0]['action']]
        out[tag] = rec
    return out


def main():
    os.makedirs(FIX, exist_ok=True)
    res = {'p3_rename_absent_at_freeze': p3(), 'p4_full_history': p4(),
           'p5_v5_partial_gap': p5()}
    with open(os.path.join(S, 'survivor-probes-2.json'), 'w', encoding='utf-8') as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
    print(json.dumps(res, indent=1, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
