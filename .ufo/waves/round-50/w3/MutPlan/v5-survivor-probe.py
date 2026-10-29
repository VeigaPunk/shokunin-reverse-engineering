#!/usr/bin/env python3
"""Are the two surviving v5-draft mutants REAL coverage gaps or equivalent
mutants?

S1 `clean-unverified-row-files-cell-widened`: the row's published-files cell
   goes from '>0' to '*'.  The claim says the clean-unverified label is for a
   run with gaps none AND >0 files.  If the cell widens, a no-reader family
   with ZERO published files would take clean-unverified too - a claim
   violation the selftest does not see, because no fixture has a no-reader
   family with 0 files.

S2 `clean-unverified-row-symlink-cell-widened`: the row's symlink-removed cell
   goes from 'no' to '*'.  A no-reader run that removed a symlink would then
   take clean-unverified instead of the symlink row.

For each: construct the exact envelope the mutant would mis-handle, run the
MUTANT's own table and evaluator on it, and report the (label, action) pair
against the PRISTINE draft's pair for the same envelope.
"""
import importlib.util
import json
import os
import subprocess
import sys

S = '/fast/scratch/hyaku/kaidoku-r50/w3-MutPlan'
BASE = os.path.join(S, 'v5-mut')
PRISTINE = os.path.join(S, 'v5-draft.py')


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    out = {}
    pristine = load(PRISTINE, 'v5_pristine')
    # the pristine draft's own table rows and evaluator
    tbl_rows = pristine.parse_table(
        [c for row in pristine.V5_ROWS for c in row], 0,
        pristine.V5_ACTIONS) if False else None

    def table_rules(mod):
        """The draft's table as the evaluator's rule list (the draft parses its
        embedded V5_ROWS the same way it parses SKILL.md)."""
        header = ['label', 'operation', 'provider', 'handler', 'failing handler',
                  'gap kinds', 'dependencies', '-be in child argv',
                  'symlink removed', 'published files', 'action', 'cause', 'source']
        lines = ['| ' + ' | '.join(header) + ' |',
                 '| ' + ' | '.join(['---'] * len(header)) + ' |']
        for row in mod.V5_ROWS:
            lines.append('| ' + ' | '.join(str(c) for c in row) + ' |')
        return mod.parse_table(lines, 0, mod.V5_ACTIONS.split())
        # (V5_ACTIONS is the 17-token vocabulary the draft declares)

    # --- S1: a no-reader family with ZERO published files and no gaps --------
    env0 = pristine._env(handler='squashfs_v2_nonstandard', gaps=[], files=0)
    feat0 = pristine.features(env0)
    out['s1_envelope'] = {'handler': 'squashfs_v2_nonstandard', 'gaps': [],
                          'files': 0, 'features_P': feat0['P'],
                          'features_G': feat0['G']}
    for tag, path in (('pristine', PRISTINE),
                      ('files-cell-widened',
                       os.path.join(BASE, 'clean-unverified-row-files-cell-widened',
                                    'sqfs-triage-v5.py')),
                      ('symlink-cell-widened',
                       os.path.join(BASE, 'clean-unverified-row-symlink-cell-widened',
                                    'sqfs-triage-v5.py'))):
        if not os.path.isfile(path):
            continue
        m = load(path, 'v5_' + tag)
        rules = table_rules(m)
        rule = m.classify(rules, feat0)
        lab, act = m.decision(rule)
        out.setdefault('s1_table_label', {})[tag] = [lab, act]
        out.setdefault('s1_evaluator_label', {})[tag] = list(m.evaluate(feat0)[:2])

    # --- S2: a no-reader run that removed a symlink -------------------------
    envs = pristine._env(handler='squashfs_v2_nonstandard', gaps=[], files=2,
                          sr=True)
    feats = pristine.features(envs)
    out['s2_envelope'] = {'handler': 'squashfs_v2_nonstandard', 'gaps': [],
                          'files': 2, 'symlink_removed': feats['SR'],
                          'features_P': feats['P'], 'features_G': feats['G']}
    for tag, path in (('pristine', PRISTINE),
                      ('files-cell-widened',
                       os.path.join(BASE, 'clean-unverified-row-files-cell-widened',
                                    'sqfs-triage-v5.py')),
                      ('symlink-cell-widened',
                       os.path.join(BASE, 'clean-unverified-row-symlink-cell-widened',
                                    'sqfs-triage-v5.py'))):
        if not os.path.isfile(path):
            continue
        m = load(path, 'v5b_' + tag)
        rules = table_rules(m)
        rule = m.classify(rules, feats)
        lab, act = m.decision(rule)
        out.setdefault('s2_table_label', {})[tag] = [lab, act]
        out.setdefault('s2_evaluator_label', {})[tag] = list(m.evaluate(feats)[:2])

    # --- does the mutant's own selftest notice? ----------------------------
    for tag, d in (('files-cell-widened',
                    os.path.join(BASE, 'clean-unverified-row-files-cell-widened')),
                   ('symlink-cell-widened',
                    os.path.join(BASE, 'clean-unverified-row-symlink-cell-widened'))):
        script = os.path.join(d, 'sqfs-triage-v5.py')
        if not os.path.isfile(script):
            continue
        env = dict(os.environ)
        env['TMPDIR'] = os.path.join(d, 'tmp')
        env['HYAKU_SCRATCH'] = os.path.join(d, 'hyaku')
        os.makedirs(env['TMPDIR'], exist_ok=True)
        p = subprocess.run([sys.executable, '-I', '-B', 'sqfs-triage-v5.py',
                            '--selftest'], cwd=d, capture_output=True, text=True,
                           env=env, timeout=900)
        out.setdefault('selftest', {})[tag] = {
            'exit_code': p.returncode,
            'stdout_sha256': __import__('hashlib').sha256(
                p.stdout.encode()).hexdigest(),
            'stdout_tail': p.stdout.strip().splitlines()[-2:] if p.stdout.strip() else []}
    p = os.path.join(S, 'v5-survivor-probe.json')
    json.dump(out, open(p, 'w'), indent=1, sort_keys=True)
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
