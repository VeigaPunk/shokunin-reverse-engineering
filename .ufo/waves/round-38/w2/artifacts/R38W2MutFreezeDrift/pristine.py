#!/usr/bin/env python3
"""freeze-drift: list commits that touched a frozen claim path after its freeze.

Round-38 mistake M38-1: the round-38 attempt-1 L1 amended the frozen
predicate and counter twice (79f69347, f1010f67) after wave-1 seats had
scored carriers with the first-freeze counter, and labelled the amendment
"pre-scoring". QUALITY criterion 79 makes this gate the check: a claim's
rule is the bytes of its first freeze commit; if this gate prints any commit
between the freeze and the measured revision, the claim is scored with the
first-freeze bytes and the amendment is reported, never adopted.

Usage:
  freeze-drift.py --root LANE --freeze FREEZE --rev REV [--json-out PATH] PATH...

PATH arguments are repo-relative paths or git pathspec globs (quote them);
default set when none is given: the round-38 kill-rule set (claims doc,
both counters, carriers manifest, oracle tables).

Reads only git objects (git log over FREEZE..REV). Exit 0: no drift;
1: drift (the commits are listed); 2: unevaluable (unknown revision, or
FREEZE is not an ancestor of REV).
"""
import argparse, json, subprocess, sys

DEFAULT = [
    'plans/round-38-claims.md',
    'tools/round-38/c1-counter.py',
    'tools/round-38/c2-counter.py',
    '.ufo/waves/round-38/c1/carriers.json',
    'corpus/evidence/round-37/c1/*/oracle.tsv',
]


def git(root, *args):
    return subprocess.run(['git', '-C', root, *args], capture_output=True, text=True)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--freeze', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--json-out')
    ap.add_argument('paths', nargs='*')
    a = ap.parse_args(argv)
    paths = a.paths or DEFAULT
    res = {'tool': 'freeze-drift', 'freeze': a.freeze, 'rev': a.rev, 'paths': paths}
    for r in (a.freeze, a.rev):
        if git(a.root, 'cat-file', '-e', f'{r}^{{commit}}').returncode:
            res.update(verdict='unevaluable', reason=f'unknown revision {r}')
            return finish(res, a.json_out, 2)
    if git(a.root, 'merge-base', '--is-ancestor', a.freeze, a.rev).returncode:
        res.update(verdict='unevaluable', reason='freeze is not an ancestor of rev')
        return finish(res, a.json_out, 2)
    log = git(a.root, 'log', '--format=%H%x09%cI%x09%s', '--name-only', '--no-renames',
              f'{a.freeze}..{a.rev}', '--', *[f':(glob){p}' for p in paths])
    drift, cur = [], None
    for line in log.stdout.splitlines():
        if '\t' in line:
            h, when, subj = line.split('\t', 2)
            cur = {'commit': h, 'committed': when, 'subject': subj, 'paths': []}
            drift.append(cur)
        elif line.strip() and cur is not None:
            cur['paths'].append(line.strip())
    res['drift'] = drift
    res['verdict'] = 'drift' if drift else 'clean'
    return finish(res, a.json_out, 1 if drift else 0)


def finish(res, out, code):
    text = json.dumps(res, indent=1)
    if out:
        with open(out, 'w') as f:
            f.write(text + '\n')
    print(text)
    return code


if __name__ == '__main__':
    sys.exit(main())
