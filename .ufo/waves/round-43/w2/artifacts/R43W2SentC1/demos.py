#!/usr/bin/env python3
"""R43W2SentC1 attack demos: path handling, self-report bindings. Scratch only."""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

S = '/fast/scratch/hyaku/kaidoku-r43/w2/R43W2SentC1'
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
REV = '77d196c66f4fea00d7d543728b190ebdfaf6d0f0'


def load_counter():
    spec = importlib.util.spec_from_file_location(
        'cnt', os.path.join(S, 'counter_rev.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def demo_flat_envelopes(m):
    print('\n== DEMO 1: flat_envelopes() joins the manifest id into a path ==')
    base = os.path.join(S, 'demo1')
    shutil.rmtree(base, ignore_errors=True)
    os.makedirs(base)
    victim = os.path.join(S, 'demo1-ESCAPE')
    for p in (victim + '.json',):
        if os.path.exists(p):
            os.remove(p)
    d, argmap = m.flat_envelopes(base, 'main', [(victim, b'{"escaped": true}\n')])
    print('staging dir :', d)
    print('argmap      :', argmap)
    print('victim exists outside staging dir:', os.path.isfile(victim + '.json'))
    if os.path.isfile(victim + '.json'):
        print('victim bytes:', open(victim + '.json', 'rb').read())
    print('files inside staging dir:', os.listdir(d))
    return os.path.isfile(victim + '.json')


def demo_ids_gate(m):
    print('\n== DEMO 2: ids_unique() accepts an absolute id ==')
    ids = ['/fast/scratch/x', 'H01']
    print('ids              :', ids)
    print('ids_unique idiom :', bool(ids) and len(set(ids)) == len(ids) and all(ids))
    print('counter code 1608:', 'b[\'ids_unique\'] = bool(ids) and len(set(ids)) == len(ids) and all(ids)')
    # no charset / no resolve() on ids: show resolve() rejects the same string
    print('the counter resolve() helper rejects absolute ids; ids never pass through it:')
    print('  resolve guard (line ~1680): p.startswith("/") or ".." in p.split("/") -> None')


def demo_tuple_check_traversal():
    print('\n== DEMO 3: --tuple-check reads outside the directory via a manifest id ==')
    root = os.path.join(S, 'demo3')
    shutil.rmtree(root, ignore_errors=True)
    checked = os.path.join(root, 'checked')
    outside = os.path.join(root, 'outside')
    os.makedirs(os.path.join(outside, 'SENTINEL'))
    os.makedirs(checked)
    # an envelope whose ONLY evidence is a published file count
    env = {'operation': 'extract_firmware', 'provider': {'id': 'unblob'},
           'subject': {'digest': {'sha256': '0' * 64}},
           'normalized_result': {'files': [{'path': 'x'}], 'chunks': [],
                                 'extraction_gaps': [], 'diagnostics': []}}
    with open(os.path.join(outside, 'SENTINEL', 'envelope.json'), 'w') as fh:
        json.dump(env, fh)
    man = {'carriers': [{'id': os.path.join(outside, 'SENTINEL'),
                         'class': 'combo',
                         'declared_features': {'handler_set': [], 'gap_kinds': [],
                                               'gap_dependencies': [], 'be_argv': 'n/a',
                                               'symlink_removed': False,
                                               'published': 'zero'}}]}
    with open(os.path.join(checked, 'manifest.json'), 'w') as fh:
        json.dump(man, fh)
    gen = os.path.join(S, 'gen_rev.py')
    p = subprocess.run([sys.executable, '-I', '-B', gen, '--tuple-check', checked],
                       capture_output=True, text=True)
    print('exit:', p.returncode)
    print('stdout:', p.stdout.strip())
    print('=> the observed tuple was read from', os.path.join(outside, 'SENTINEL'),
          'which is OUTSIDE', checked)
    print('files left in checked dir:', sorted(os.listdir(checked)))


def demo_same_commit(m):
    print('\n== DEMO 4: manifest_before_envelopes() is true on a SAME-COMMIT add ==')
    repo = os.path.join(S, 'demo4-repo')
    shutil.rmtree(repo, ignore_errors=True)
    os.makedirs(repo)
    env = {'SCC': {'GIT_AUTHOR_NAME': 'fx', 'GIT_AUTHOR_EMAIL': 'fx@fx',
                   'GIT_COMMITTER_NAME': 'fx', 'GIT_COMMITTER_EMAIL': 'fx@fx'}}
    env = dict(os.environ, **env['SCC'])

    def g(*a):
        return subprocess.run(['git', '-C', repo] + list(a), capture_output=True,
                              text=True, env=env)

    g('init', '-q')
    top = g('rev-parse', '--show-toplevel').stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(repo), (top, repo)
    print('toplevel verified:', top)
    os.makedirs(os.path.join(repo, 'heldout', 'H01'))
    with open(os.path.join(repo, 'heldout', 'H01', 'envelope.json'), 'w') as fh:
        fh.write('{}\n')
    with open(os.path.join(repo, 'heldout', 'manifest.json'), 'w') as fh:
        fh.write('{}\n')
    g('add', '-A')
    g('-c', 'user.name=fx', '-c', 'user.email=fx@fx', 'commit', '-q', '-m', 'both')
    rev = g('rev-parse', 'HEAD').stdout.strip()
    ma = m.first_add(repo, rev, 'heldout/manifest.json')
    fa = m.first_add(repo, rev, 'heldout/H01/envelope.json')
    fz = g('rev-list', '--max-parents=0', 'HEAD').stdout.strip()
    print('manifest first_add:', ma)
    print('envelope first_add:', fa)
    print('is_ancestor(manifest_first, envelope_first):', m.is_ancestor(repo, ma, fa))
    print('binding value:', bool(ma) and bool(fa) and m.is_ancestor(repo, ma, fa))
    print('=> a manifest written BEFORE the run but committed WITH the envelopes '
          'scores the binding True')


def main():
    m = load_counter()
    demo_flat_envelopes(m)
    demo_ids_gate(m)
    demo_tuple_check_traversal()
    demo_same_commit(m)


if __name__ == '__main__':
    main()
