#!/usr/bin/env python3
"""green-fixtures -- build the pass-side fixtures the five mistake gates must accept.

Everything lands under --work (default $TMPDIR/mistake-green). Nothing in the lane is written.
Writes:
  scores/       the lane's round-39 score receipts with the exit code each run actually exited
                with, appended (met_target true -> 0, false -> 1, unevaluable -> 2)
  ledgers/      the two wave ledgers with every seat status filled
  report.md     the round-39 fleet report plus one cross-domain evidence line
  ctrlrepo/     fixture git repo: a valid control table committed IN the freeze commit
  ctrlrepo-bad/ fixture git repo: same, but the table's cause cell has no `->` (format half bites)
  depthrepo/    fixture git repo: base leaves one rule block unresolved (depth 5.0), tip
                resolves it (10.0) -> a measurable delta
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
SCORES = os.path.join(LANE, '.ufo/waves/round-39/l1/scores')
LEDGERS = [os.path.join(LANE, '.ufo/waves/round-39/r39-w1-results.json'),
           os.path.join(LANE, '.ufo/waves/round-39/r39-w2-results.json')]
REPORT = '/home/vgpnk/Projects/shokunin/.ufo/reports/round-39/kaidoku.md'
VALID_TABLE = os.path.join(LANE, '.ufo/waves/round-39/controls/tables/'
                           'CTL-C2-5-round36-le-transcribed.formatfix.md')

SKILL_FIXTURE = """# fixture SKILL

## Queue-drain craft (fixture)

- **rule one.** cites `corpus/knowledge/a.md:1-2`.
- **rule two.** cites `corpus/knowledge/b.md:1`.

## Next section
"""
README_FIXTURE = """# fixture corpus

## Coverage map
- 2026-10-26-a

## Next
"""


def git(repo, *args, identity=False):
    cmd = ['git', '-C', repo]
    if identity:
        cmd += ['-c', 'user.name=fx', '-c', 'user.email=fx@fx']
    cmd += list(args)
    return subprocess.run(cmd, capture_output=True, text=True, check=True)


def new_repo(path):
    os.makedirs(path)
    git(path, 'init', '-q')
    top = git(path, 'rev-parse', '--show-toplevel').stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(path), (top, path)
    return path


def commit(repo, message):
    git(repo, 'add', '-A')
    git(repo, 'commit', '-q', '-m', message, identity=True)
    return git(repo, 'rev-parse', 'HEAD').stdout.strip()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(text)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', default=os.path.join(os.environ.get('TMPDIR', '/tmp'),
                                                   'mistake-green'))
    args = ap.parse_args(argv)
    work = os.path.abspath(args.work)
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)

    # 1. score receipts with the exit code each command actually returned
    out_scores = os.path.join(work, 'scores')
    os.makedirs(out_scores)
    for name in sorted(os.listdir(SCORES)):
        if not name.endswith('.json'):
            continue
        obj = json.load(open(os.path.join(SCORES, name), encoding='utf-8'))
        if 'unevaluable' in obj:
            code = 2
        else:
            code = 0 if obj.get('met_target') else 1
        obj['exit_code'] = code
        write(os.path.join(out_scores, name), json.dumps(obj, indent=1, sort_keys=True) + '\n')

    # 2. ledgers with seat status filled
    out_led = os.path.join(work, 'ledgers')
    os.makedirs(out_led)
    for path in LEDGERS:
        obj = json.load(open(path, encoding='utf-8'))
        for item in obj.get('results', []):
            item['status'] = 'completed'
        write(os.path.join(out_led, os.path.basename(path)),
              json.dumps(obj, indent=1, sort_keys=True) + '\n')

    # 3. report with the PROTOCOL:155 line it lacked
    text = open(REPORT, encoding='utf-8').read()
    if not text.endswith('\n'):
        text += '\n'
    text += ('\n- **Cross-domain evidence encountered.** none this round: the AVM merge theme '
             'is the same domain (PROVINCE Adjacent unchanged).\n')
    write(os.path.join(work, 'report.md'), text)

    # 4. control-table repos: freeze commit holds the table
    valid = open(VALID_TABLE, encoding='utf-8').read()
    repo = new_repo(os.path.join(work, 'ctrlrepo'))
    write(os.path.join(repo, 'controls/tables/CTL-C2-5.md'), valid)
    freeze = commit(repo, 'freeze: control table')
    write(os.path.join(repo, 'README.md'), 'later commit\n')
    commit(repo, 'after freeze')

    bad = valid.replace(' -> ', ' = ')
    repo_bad = new_repo(os.path.join(work, 'ctrlrepo-bad'))
    write(os.path.join(repo_bad, 'controls/tables/CTL-C2-5.md'), bad)
    bad_freeze = commit(repo_bad, 'freeze: malformed control table')

    # 5. depth repo with headroom at base
    repo_depth = new_repo(os.path.join(work, 'depthrepo'))
    write(os.path.join(repo_depth, 'SKILL.md'), SKILL_FIXTURE)
    write(os.path.join(repo_depth, 'corpus/README.md'), README_FIXTURE)
    write(os.path.join(repo_depth, 'corpus/knowledge/a.md'), 'line1\nline2\nline3\n')
    base = commit(repo_depth, 'base: b.md absent')
    write(os.path.join(repo_depth, 'corpus/knowledge/b.md'), 'line1\nline2\n')
    tip = commit(repo_depth, 'tip: b.md present')

    info = {
        'work': work,
        'ctrlrepo_freeze': freeze,
        'ctrlrepo_bad_freeze': bad_freeze,
        'depthrepo_base': base,
        'depthrepo_tip': tip,
    }
    with open(os.path.join(work, 'fixtures.json'), 'w', encoding='utf-8') as fh:
        json.dump(info, fh, indent=1, sort_keys=True)
        fh.write('\n')
    print(json.dumps(info, indent=1, sort_keys=True))


if __name__ == '__main__':
    sys.exit(main())
