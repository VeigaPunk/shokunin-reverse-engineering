#!/usr/bin/env python3
"""ExecB1Impact: A/B test of the SCORECORD section ORDER at the planned attempt-2 landing.

`v7-order-last`   : attempt-2 section appended at EOF (AFTER the corrections section)
`v8-order-before` : attempt-2 section inserted BEFORE the corrections section

Both clones carry the C3 instrument OUTSIDE tools/round-50/ (so the C2 counter's
freeze_check passes with FREEZE=435d41fd) and both carry the C1/C2 landing text.
The battery is then run at each clone's tip with FREEZE=435d41fd.
"""
import os
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
BASE = 'f890bbead20ca2c549487167f56876ae47f1e1a4'
CORR_HEAD = '## Record corrections — round 50'
ATT2 = ('## Round 50 attempt 2 — resumed C1 under the same frozen bytes, C3 depth added\n\n'
        'Base `f890bbead20ca2c549487167f56876ae47f1e1a4`.  The C1 freeze `435d41fd` is unchanged.\n')


def git(clone, *args, check=True):
    p = subprocess.run(['git', '-C', clone] + list(args), capture_output=True)
    if check and p.returncode != 0:
        raise SystemExit('git %s failed: %s' % (' '.join(args), p.stderr.decode()[:400]))
    return p.stdout.decode('utf-8', 'replace')


def write(clone, path, text):
    fp = os.path.join(clone, path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, 'w') as fh:
        fh.write(text)


def read(clone, path):
    return git(clone, 'show', 'HEAD:' + path)


def commit(clone, msg):
    git(clone, 'add', '-A', '--', '.')
    p = subprocess.run(['git', '-C', clone, 'commit', '-q', '-m', msg], capture_output=True)
    if p.returncode != 0:
        raise SystemExit(p.stderr.decode()[:400])
    return git(clone, 'rev-parse', 'HEAD').strip()


def main():
    work, mode = sys.argv[1], sys.argv[2]
    name = 'v7-order-last' if mode == 'last' else 'v8-order-before'
    clone = os.path.join(work, name)
    subprocess.run(['git', 'clone', '--shared', '-q', LANE, clone], check=True)
    git(clone, 'checkout', '-q', '--detach', BASE)
    git(clone, 'config', 'user.name', 'c2-impact-seat')
    git(clone, 'config', 'user.email', 'c2-impact-seat@invalid')
    git(clone, 'config', 'commit.gpgsign', 'false')
    subprocess.run([sys.executable, os.path.join(LANE, '.ufo/waves/round-50/w3/ExecB1Impact/mklanding.py'),
                    clone, 'outside'], check=True)
    sc = read(clone, 'SCORECARD.md')
    block = '\n\n' + ATT2
    assert block in sc
    sc = sc.replace(block, '', 1)
    if mode == 'before':
        i = sc.find(CORR_HEAD)
        assert i > 0
        sc = sc[:i] + ATT2 + '\n' + sc[i:]
    else:
        sc = sc.rstrip('\n') + '\n\n' + ATT2
    write(clone, 'SCORECARD.md', sc)
    print(commit(clone, 'variant %s' % name))


if __name__ == '__main__':
    main()
