#!/usr/bin/env python3
"""ExecB1Impact: build atom-isolation variants of the simulated attempt-2 landing.

Each variant is one commit in its own fixture clone of the lane.  The C2 counter is then
run with --rev == --freeze == the variant commit, which isolates the ATOM verdicts from the
freeze-drift arm (the counter's own bytes are unchanged, so `counter_not_frozen` still
passes and every atom is read exactly as it would be at the final landing).

Variants:
  v1-inside      : C3 instrument at tools/round-50/sqfs-triage-v5.py WITH its registry row
  v2-noreg       : same, but the registry row for the instrument is absent        -> B9 red
  v3-head139     : the Owned-axes coverage row still reads 139/139               -> B1 red
  v4-nomap       : README Coverage map has no row for the new entry stem         -> B1 red
  v5-dupcorr     : a SECOND '## Record corrections -- round 50 attempt 2' section -> 5 atoms red
  v6-beforecorr  : the attempt-2 SCORECARD section sits BEFORE the corrections section
"""
import os
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
BASE = 'f890bbead20ca2c549487167f56876ae47f1e1a4'
STEM = '2026-10-28-r50-avm-le-squashfs-core'
INSTR = 'tools/round-50/sqfs-triage-v5.py'
CORR_HEAD = '## Record corrections — round 50'
ATT2 = ('\n\n## Round 50 attempt 2 — resumed C1 under the same frozen bytes, C3 depth added\n\n'
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


def build(name, work):
    clone = os.path.join(work, name)
    subprocess.run(['git', 'clone', '--shared', '-q', LANE, clone], check=True)
    git(clone, 'checkout', '-q', '--detach', BASE)
    git(clone, 'config', 'user.name', 'c2-impact-seat')
    git(clone, 'config', 'user.email', 'c2-impact-seat@invalid')
    git(clone, 'config', 'commit.gpgsign', 'false')
    subprocess.run([sys.executable, os.path.join(LANE, '.ufo/waves/round-50/w3/ExecB1Impact/mklanding.py'),
                    clone, 'inside'], check=True)
    return clone


def main():
    work, name = sys.argv[1], sys.argv[2]
    clone = build(name, work)
    if name == 'v1-inside':
        pass
    elif name == 'v2-noreg':
        sk = read(clone, 'SKILL.md')
        lines = [l for l in sk.split('\n') if not l.startswith('| `%s`' % INSTR)]
        write(clone, 'SKILL.md', '\n'.join(lines))
    elif name == 'v3-head139':
        sc = read(clone, 'SCORECARD.md')
        new = ('140/140 knowledge files mapped at the round-50 attempt-2 landing '
               '(the round-50 attempt-1 landing read 139/139; the C1 entry `%s` made it 140)' % STEM)
        sc = sc.replace(new, '139/139 knowledge files mapped at the round-50 landing', 1)
        write(clone, 'SCORECARD.md', sc)
    elif name == 'v4-nomap':
        rd = read(clone, 'corpus/README.md')
        write(clone, 'corpus/README.md', '\n'.join(l for l in rd.split('\n') if STEM not in l))
    elif name == 'v5-dupcorr':
        sc = read(clone, 'SCORECARD.md')
        sc = sc.rstrip('\n') + '\n\n## Record corrections — round 50 attempt 2\n\n- B3 seats=75\n'
        write(clone, 'SCORECARD.md', sc)
    elif name == 'v6-beforecorr':
        sc = read(clone, 'SCORECARD.md')
        # remove the attempt-2 section appended at EOF, then re-insert it BEFORE the corrections section
        sc = sc.replace(ATT2, '', 1)
        i = sc.find(CORR_HEAD)
        assert i > 0
        sc = sc[:i] + ATT2.lstrip('\n') + '\n' + sc[i:]
        write(clone, 'SCORECARD.md', sc)
    else:
        raise SystemExit('unknown variant')
    print(commit(clone, 'variant %s' % name))


if __name__ == '__main__':
    main()
