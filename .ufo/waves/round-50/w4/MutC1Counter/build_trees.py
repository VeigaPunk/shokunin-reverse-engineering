#!/usr/bin/env python3
"""Build synthetic roots for the R50-C1 counterfactual.

The frozen counter binds its OWN bytes to the freeze commit
(`measure()`: `own_sha` must equal `sha256(show(root, freeze,
COUNTER_PATH))`, else `CounterNotFrozen`).  A mutated counter therefore
cannot be scored against a root whose freeze carries the pristine counter.

So each arm gets a synthetic two-commit repo:

  F (synthetic freeze) : tree = the real lane tree at 435d41fd
  R (synthetic rev)    : tree = the real lane tree at 646d29c9

with ONE mutation applied IDENTICALLY at both commits (so the counter's
frozen-path drift check still sees no drift):

  A0  no mutation                          (baseline: the landed state)
  A1  tools/round-50/c1-counter.py  mutated (char-device not required)
  A2  tools/round-50/c1-counter.py  mutated (any char-device admitted silently)
  A3  tools/round-50/gap-rule.json  mutated (required.char-device = false)
  A4  A3 + PROVINCE.md at R carrying the "## Round-50 additions to Core"
      section, i.e. the counterfactual landing a green measurement would
      have produced (the L1 landed an honest stop instead)

Everything else is the real lane tree, byte for byte.

Writes only inside $S.  No lane write, no lane git mutation.
"""
import json
import os
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
FREEZE = '435d41fd4ad9211d1579fc447936fb33d2b74467'
REV = '646d29c9df4ef77499248f95589cb9526c6dea19'
S = os.path.dirname(os.path.abspath(__file__))
COUNTER_PATH = 'tools/round-50/c1-counter.py'
GAPRULE_PATH = 'tools/round-50/gap-rule.json'
ENTRY = 'corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md'

CORE_SECTION = (
    '\n## Round-50 additions to Core\n\n'
    '| Surface | Layout | Probe | Entry |\n'
    '|---|---|---|---|\n'
    '| `squashfs_v4_le` | AVM marker | x | `%s` |\n' % ENTRY)

ENV = dict(os.environ,
           GIT_AUTHOR_NAME='MutC1Counter', GIT_AUTHOR_EMAIL='mutc1@example.invalid',
           GIT_COMMITTER_NAME='MutC1Counter', GIT_COMMITTER_EMAIL='mutc1@example.invalid')


def git(repo, *args, **kw):
    p = subprocess.run(['git', '-C', repo, *args], capture_output=True,
                       env=ENV, **kw)
    if p.returncode != 0:
        raise SystemExit('git %s failed: %s' % (' '.join(args),
                                               p.stderr.decode(errors='replace')))
    return p.stdout


def blob(repo, data):
    p = subprocess.run(['git', '-C', repo, 'hash-object', '-w', '--stdin'],
                       input=data, capture_output=True, env=ENV)
    if p.returncode != 0:
        raise SystemExit('hash-object failed: ' + p.stderr.decode())
    return p.stdout.decode().strip()


def build(repo, mut_counter=None, mut_rule=None, province_core=False):
    """mut_counter/mut_rule: bytes to write at the given path (both commits)."""
    os.makedirs(repo, exist_ok=True)
    git(repo, 'init', '-q')
    git(repo, 'fetch', '-q', LANE, FREEZE)
    git(repo, 'fetch', '-q', LANE, REV)

    index = os.path.join(repo, 'index')
    trees = {}
    for name, rev in (('F', FREEZE), ('R', REV)):
        env = dict(ENV, GIT_INDEX_FILE=index)
        subprocess.run(['git', '-C', repo, 'read-tree', rev], check=True,
                       env=env, capture_output=True)
        if mut_counter is not None:
            b = blob(repo, mut_counter)
            subprocess.run(['git', '-C', repo, 'update-index', '--cacheinfo',
                            '100644,%s,%s' % (b, COUNTER_PATH)],
                           check=True, env=env, capture_output=True)
        if mut_rule is not None:
            b = blob(repo, mut_rule)
            subprocess.run(['git', '-C', repo, 'update-index', '--cacheinfo',
                            '100644,%s,%s' % (b, GAPRULE_PATH)],
                           check=True, env=env, capture_output=True)
        if province_core and name == 'R':
            prov = git(repo, 'show', '%s:PROVINCE.md' % REV)
            b = blob(repo, prov + CORE_SECTION.encode())
            subprocess.run(['git', '-C', repo, 'update-index', '--cacheinfo',
                            '100644,%s,PROVINCE.md' % b],
                           check=True, env=env, capture_output=True)
        p = subprocess.run(['git', '-C', repo, 'write-tree'], check=True,
                           env=env, capture_output=True)
        trees[name] = p.stdout.decode().strip()
    if os.path.exists(index):
        os.remove(index)

    f = git(repo, 'commit-tree', trees['F'], '-m',
            'synthetic freeze: real lane tree at %s' % FREEZE).decode().strip()
    r = git(repo, 'commit-tree', trees['R'], '-p', f, '-m',
            'synthetic rev: real lane tree at %s' % REV).decode().strip()
    git(repo, 'update-ref', 'refs/heads/synth', r)
    return f, r


def main():
    arms = {}

    muts = {
        'A1': ('c1-counter-M1.py', None),
        'A2': ('c1-counter-M2.py', None),
    }
    for name in ('A0', 'A1', 'A2', 'A3', 'A4'):
        repo = os.path.join(S, 'repo-' + name)
        mc = mr = None
        if name in muts:
            mc = open(os.path.join(S, muts[name][0]), 'rb').read()
        if name in ('A3', 'A4'):
            mr = open(os.path.join(S, 'gap-rule-M3.json'), 'rb').read()
        f, r = build(repo, mut_counter=mc, mut_rule=mr,
                     province_core=(name == 'A4'))
        arms[name] = {'root': repo, 'freeze': f, 'rev': r,
                       'mutated_counter': muts.get(name, (None,))[0],
                       'mutated_rule': 'gap-rule-M3.json' if name in ('A3', 'A4') else None,
                       'province_core_added': name == 'A4'}
        print('%s root=%s freeze=%s rev=%s' % (name, repo, f, r))

    # A5: the mutant counter scored against a root whose FREEZE carries the
    # PRISTINE counter -> the counter's own-byte binding must refuse it.
    repo = os.path.join(S, 'repo-A5')
    f, r = build(repo)                     # pristine at both ends
    arms['A5'] = {'root': repo, 'freeze': f, 'rev': r,
                  'mutated_counter': 'c1-counter-M1.py',
                  'mutated_rule': None, 'province_core_added': False,
                  'note': 'M1 counter bytes vs a PRISTINE freeze: must refuse '
                          '(counter_not_frozen)'}
    print('A5 root=%s freeze=%s rev=%s' % (repo, f, r))

    with open(os.path.join(S, 'arms.json'), 'w') as fh:
        json.dump(arms, fh, indent=1, sort_keys=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
