#!/usr/bin/env python3
"""Extra probes: (a4) the second target's prose statement; (h1) destroying the
subject section at REV; (a1) the base census that the rubric's witness used."""
import hashlib
import json
import os
import subprocess
import time

S = os.path.dirname(os.path.abspath(__file__))
CLONE = os.path.join(S, 'clone')
COUNTER = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-44/c2-counter.py'
REV = '55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac'
BASE = 'c29360e3ba5381a5ab69e372d0d9577970f85018'
FREEZE = 'c48f8a4bfd449300c975668e59aae5b5538b6a84'
IDENT = {'GIT_AUTHOR_NAME': 'w2-R44W2C2Vacuity',
         'GIT_AUTHOR_EMAIL': 'vacuity@scratch.invalid',
         'GIT_AUTHOR_DATE': '2026-10-28T00:00:00+0000',
         'GIT_COMMITTER_NAME': 'w2-R44W2C2Vacuity',
         'GIT_COMMITTER_EMAIL': 'vacuity@scratch.invalid',
         'GIT_COMMITTER_DATE': '2026-10-28T00:00:00+0000'}


def git(*args, env=None):
    e = dict(os.environ)
    if env:
        e.update(env)
    p = subprocess.run(['git', '-C', CLONE] + list(args), capture_output=True,
                       text=True, env=e)
    if p.returncode:
        raise SystemExit('git %s: %s' % (' '.join(args), p.stderr))
    return p.stdout.strip()


def make(name, path, mutate, parent=REV):
    src = git('show', '%s:%s' % (parent, path)).encode('utf-8', 'surrogateescape')
    dst = mutate(src)
    if dst == src:
        raise SystemExit('no-op mutation ' + name)
    d = os.path.join(S, 'mut', name)
    os.makedirs(d, exist_ok=True)
    f = os.path.join(d, os.path.basename(path))
    with open(f, 'wb') as h:
        h.write(dst)
    env = dict(IDENT)
    env['GIT_INDEX_FILE'] = os.path.join(d, 'index')
    git('read-tree', parent, env=env)
    blob = git('hash-object', '-w', '--path', path, f)
    git('update-index', '--add', '--cacheinfo', '100644,%s,%s' % (blob, path), env=env)
    tree = git('write-tree', env=env)
    commit = git('commit-tree', tree, '-p', parent, '-m', 'probe ' + name, env=env)
    git('update-ref', 'refs/vacuity/%s' % name, commit)
    os.unlink(env['GIT_INDEX_FILE'])
    return commit, hashlib.sha256(src).hexdigest(), hashlib.sha256(dst).hexdigest()


def drop_map_section(data):
    t = data.decode()
    head = '## Coverage map\n'
    body, sep, rest = t.partition(head)
    if not sep:
        raise SystemExit('no coverage map')
    after = rest.split('\n## ', 1)[1]
    return (body + head + '\n## ' + after).encode()


def sub(old, new):
    o, n = old.encode(), new.encode()

    def f(d):
        if d.count(o) != 1:
            raise SystemExit('count %d for %r' % (d.count(o), old))
        return d.replace(o, n, 1)
    return f


def line_sub(anchor, old, new):
    a, o, n = anchor.encode(), old.encode(), new.encode()

    def f(d):
        lines = d.split(b'\n')
        hits = [i for i, l in enumerate(lines) if a in l]
        if len(hits) != 1:
            raise SystemExit('anchor %r on %d lines' % (anchor, len(hits)))
        i = hits[0]
        lines[i] = lines[i].replace(o, n, 1)
        return b'\n'.join(lines)
    return f


def counter(rev, freeze, tag, pre):
    out = os.path.join(S, 'out', tag + '.json')
    argv = ['python3', '-I', '-B', COUNTER, '--root', CLONE, '--rev', rev,
            '--freeze', freeze, '--work', os.path.join(S, 'work'),
            '--json-out', out] + (['--pre-freeze'] if pre else [])
    t0 = time.time()
    p = subprocess.run(argv, capture_output=True, text=True)
    data = None
    if os.path.exists(out):
        with open(out) as h:
            data = json.load(h)
    return {
        'tag': tag, 'exit_code': p.returncode,
        'wall_seconds': round(time.time() - t0, 3),
        'stdout_sha256': hashlib.sha256(p.stdout.encode()).hexdigest(),
        'mismatches': (data or {}).get('mismatches'),
        'frozen_path_changed': (data or {}).get('frozen_path_changed'),
        'entries_evaluated': (data or {}).get('entries_evaluated'),
        'observed': {e['id']: e.get('observed')
                     for e in (data or {}).get('entries') or []},
    }


def main():
    top = git('rev-parse', '--show-toplevel')
    assert os.path.realpath(top) == os.path.realpath(CLONE)
    out = {}

    c, s0, s1 = make('a4-prose-value', 'SCORECARD.md',
                     line_sub('20/20 queue-drain rule blocks have resolvable', 'craft section `SKILL.md:81-449`',
                              'craft section `SKILL.md:81-448`'))
    out['a4-prose-value'] = {
        'mutant': c, 'src': s0, 'dst': s1,
        'A': counter(c, FREEZE, 'a4prose.A', False),
        'B': counter(c, FREEZE, 'a4prose.B', True),
        'entry': 'C2-a4-owned-depth-craft-range'}

    c, s0, s1 = make('h1-subject-section-deleted', 'corpus/README.md',
                     drop_map_section)
    out['h1-subject-section-deleted'] = {
        'mutant': c, 'src': s0, 'dst': s1,
        'A': counter(c, FREEZE, 'h1section.A', False),
        'B': counter(c, FREEZE, 'h1section.B', True),
        'entry': 'C2-h1-readme-coverage-map-complete'}

    # the base census the rubric's witness used: run a1's own payload
    payload = open(os.path.join(S, 'cmd_C2-a1-owned-coverage-count.py')).read()
    for tag, rev in (('a1_at_base_rev_eq_freeze', BASE),):
        p = subprocess.run(['python3', '-I', '-B', '-c', payload, BASE, BASE, CLONE],
                           capture_output=True, text=True, cwd=S)
        out[tag] = {'exit_code': p.returncode, 'stdout': p.stdout.strip(),
                    'stderr': p.stderr[:300]}
    p = subprocess.run(['python3', '-I', '-B', '-c', payload, BASE, FREEZE, CLONE],
                       capture_output=True, text=True, cwd=S)
    out['a1_at_base_rev_freeze_c48f8a4'] = {'exit_code': p.returncode,
                                            'stdout': p.stdout.strip(),
                                            'stderr': p.stderr[:300]}
    print(json.dumps(out, indent=1, sort_keys=True))
    with open(os.path.join(S, 'out', 'extras.json'), 'w') as h:
        json.dump(out, h, indent=1, sort_keys=True)


if __name__ == '__main__':
    main()
