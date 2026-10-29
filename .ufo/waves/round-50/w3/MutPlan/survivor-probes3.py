#!/usr/bin/env python3
"""Survivor analysis.

S1 (bytes-used-lower-bound): is the mutant VERDICT-equivalent (masked by the
tables_sane clause) or does it change a verdict?  Run the pristine and the
mutated layout_probe on a bytes_used == 0 carrier.

S2 (frozen-drift-rename-code): is the 'R' status code load-bearing?  Build a
fixture where a frozen path that does NOT exist at the freeze is renamed after
the freeze, and run the pristine and mutated frozen_drift.

S3 (full-history-flag): sweep topologies and compare `git log -m` with and
without `--full-history`.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

S = '/fast/scratch/hyaku/kaidoku-r50/w3-MutPlan'
FIX = os.path.join(S, 'probe-fixtures')
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
PRISTINE = os.path.join(LANE, 'tools/round-50/c1-counter.py')
MUT_BYTES = os.path.join(S, 'counter-mut/bytes-used-lower-bound/tools/round-50/c1-counter.py')
MUT_RENAME = os.path.join(S, 'counter-mut/frozen-drift-rename-code/tools/round-50/c1-counter.py')


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def s1():
    out = {}
    for tag, path in (('pristine', PRISTINE), ('mutant', MUT_BYTES)):
        if not os.path.isfile(path):
            continue
        m = load(path, 'c1_' + tag)
        blob = bytearray(m.sb_carrier(m.XZ_ID, b'probe'))
        # force bytes_used == 0 (and mkfs_time == 0 so the marker equality holds)
        blob[40:48] = (0).to_bytes(8, 'little')
        blob[8:12] = (0).to_bytes(4, 'little')
        p = m.layout_probe(bytes(blob))
        out[tag] = {'ok': p.get('ok'), 'reason': p.get('reason'),
                    'bytes_used': p.get('bytes_used'),
                    'bytes_used_sane': p.get('bytes_used_sane'),
                    'tables_sane': p.get('tables_sane'),
                    'marker': p.get('marker')}
    out['verdict_equal'] = (out.get('pristine', {}).get('ok') ==
                            out.get('mutant', {}).get('ok'))
    out['reason_differs'] = (out.get('pristine', {}).get('reason') !=
                             out.get('mutant', {}).get('reason'))
    return out


def git(d, *a, check=True):
    return subprocess.run(['git', '-C', d] + list(a), capture_output=True,
                          text=True, check=check)


def s2():
    """A frozen path (an oracle table named by carriers.json) that does NOT
    exist at the freeze is renamed after the freeze."""
    d = os.path.join(FIX, 's2-rename-after-freeze')
    if os.path.exists(d):
        shutil.rmtree(d)
    os.makedirs(d)
    git(d, 'init', '-q')
    git(d, 'config', 'user.name', 'fx')
    git(d, 'config', 'user.email', 'fx@fx')

    def w(path, content):
        full = os.path.join(d, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'w') as fh:
            fh.write(content)

    w('base.txt', 'b\n')
    git(d, 'add', '-A')
    git(d, 'commit', '-qm', 'base', '--allow-empty')
    freeze = git(d, 'rev-parse', 'HEAD').stdout.strip()
    # the oracle table appears only AFTER the freeze (a frozen path per spec)
    w('corpus/evidence/round-50/c1/g7581/oracle.tsv', 'a\tb\t1\n')
    git(d, 'add', '-A')
    git(d, 'commit', '-qm', 'add the oracle table after the freeze', '--allow-empty')
    git(d, 'mv', 'corpus/evidence/round-50/c1/g7581/oracle.tsv',
        'corpus/evidence/round-50/c1/g7581/oracle-moved.tsv')
    git(d, 'commit', '-qm', 'rename it', '--allow-empty')
    rev = git(d, 'rev-parse', 'HEAD').stdout.strip()

    spec = {'carriers': [{'id': 'g7581',
                          'sha256': 'a' * 64,
                          'oracle': 'corpus/evidence/round-50/c1/g7581/oracle.tsv',
                          'nonregular': 'corpus/evidence/round-50/c1/g7581/nonregular.tsv'}]}
    out = {'freeze': freeze, 'rev': rev, 'spec': spec}
    for tag, path in (('pristine', PRISTINE), ('mutant', MUT_RENAME)):
        if not os.path.isfile(path):
            continue
        m = load(path, 'c1r_' + tag)
        try:
            drift = m.frozen_drift(d, freeze, rev, spec)
            out[tag] = {'drift': drift, 'exception': None}
        except Exception as e:
            out[tag] = {'drift': None, 'exception': '%s: %s' % (type(e).__name__, e)}
    out['same'] = (out.get('pristine', {}).get('drift') ==
                   out.get('mutant', {}).get('drift'))
    return out


def s3():
    """Sweep merge topologies; compare `-m` with and without --full-history."""
    out = {}
    shapes = {
        'A_side_add_only': ('side', None, None),
        'B_side_add_main_same': ('side', 'main', 'same'),
        'C_side_two_commits_main_none': ('side2', None, None),
        'D_main_add_only': (None, 'main', None),
        'E_side_add_main_diff_paths': ('side', 'main', 'diffpath'),
    }
    for tag, (side, main, mode) in shapes.items():
        d = os.path.join(FIX, 's3-' + tag)
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)
        git(d, 'init', '-q')
        git(d, 'config', 'user.name', 'fx')
        git(d, 'config', 'user.email', 'fx@fx')

        def w(path, content):
            full = os.path.join(d, path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, 'w') as fh:
                fh.write(content)

        def c(msg):
            git(d, 'add', '-A')
            git(d, 'commit', '-qm', msg, '--allow-empty')

        w('base.txt', 'b\n')
        c('base')
        if side:
            git(d, 'checkout', '-q', '-b', 'side')
            w('rcpt/after.json', '{"a":1}\n')
            c('side pre-freeze add')
            if side == 'side2':
                w('other/extra.txt', 'x\n')
                c('side second commit')
            git(d, 'checkout', '-q', '-')
        w('main.txt', 'm\n')
        c('main pre-freeze')
        if main:
            if mode == 'same':
                w('rcpt/after.json', '{"a":1}\n')
            elif mode == 'diffpath':
                w('rcpt/other.json', '{"b":2}\n')
            else:
                w('rcpt/after.json', '{"a":2}\n')
            c('main post-freeze add')
        m = git(d, 'merge', '--no-ff', '--no-commit', '-q', 'side', check=False)
        if m.returncode != 0:
            git(d, 'merge', '--abort', check=False)
            out[tag] = {'merge_exit': m.returncode}
            continue
        c('merge')
        head = git(d, 'rev-parse', 'HEAD').stdout.strip()
        res = {}
        for label, extra in (('m_full_history', ['-m', '--full-history']),
                             ('m_only', ['-m']),
                             ('plain', [])):
            p = git(d, 'log', *extra, '--diff-filter=A', '--format=%H', head,
                    '--', 'rcpt/after.json', check=False)
            res[label] = {'commits': [x for x in p.stdout.split() if x],
                          'sha256': hashlib.sha256(p.stdout.encode()).hexdigest()}
        res['m_pair_identical'] = (res['m_full_history']['sha256'] ==
                                   res['m_only']['sha256'])
        out[tag] = {'head': head, 'log': res}
    return out


def main():
    os.makedirs(FIX, exist_ok=True)
    res = {'s1_bytes_used_zero': s1(), 's2_rename_load_bearing': s2(),
           's3_full_history_sweep': s3()}
    with open(os.path.join(S, 'survivor-probes-3.json'), 'w', encoding='utf-8') as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
    print(json.dumps(res, indent=1, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
