#!/usr/bin/env python3
"""w2-R44W2C2Vacuity: per-entry mutation probes against the frozen C2 rubric.

Mutants are built with git plumbing only (hash-object / update-index on a
throwaway index / write-tree / commit-tree / update-ref), inside the seat's own
scratch clone.  The lane, its index and its refs are never touched.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

S = os.path.dirname(os.path.abspath(__file__))
CLONE = os.path.join(S, 'clone')
COUNTER = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-44/c2-counter.py'
REV = '55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac'
FREEZE = 'c48f8a4bfd449300c975668e59aae5b5538b6a84'
IDENT = {
    'GIT_AUTHOR_NAME': 'w2-R44W2C2Vacuity',
    'GIT_AUTHOR_EMAIL': 'vacuity@scratch.invalid',
    'GIT_AUTHOR_DATE': '2026-10-28T00:00:00+0000',
    'GIT_COMMITTER_NAME': 'w2-R44W2C2Vacuity',
    'GIT_COMMITTER_EMAIL': 'vacuity@scratch.invalid',
    'GIT_COMMITTER_DATE': '2026-10-28T00:00:00+0000',
}


def run(argv, env=None, cwd=None):
    e = dict(os.environ)
    if env:
        e.update(env)
    return subprocess.run(argv, capture_output=True, text=True, env=e, cwd=cwd)


def git(*args, env=None):
    p = run(['git', '-C', CLONE] + list(args), env=env)
    if p.returncode:
        raise SystemExit('git %s failed: %s' % (' '.join(args), p.stderr))
    return p.stdout.strip()


def blob_at(path):
    p = subprocess.run(['git', '-C', CLONE, 'show', '%s:%s' % (REV, path)],
                       capture_output=True)
    if p.returncode:
        raise SystemExit('absent: ' + path)
    return p.stdout


def make_mutant(name, path, mutate):
    """mutate(bytes) -> bytes; builds a commit child of REV, returns its sha."""
    src = blob_at(path)
    dst = mutate(src)
    if dst == src:
        raise SystemExit('mutation was a no-op for ' + name)
    d = os.path.join(S, 'mut', name)
    os.makedirs(d, exist_ok=True)
    fpath = os.path.join(d, os.path.basename(path))
    with open(fpath, 'wb') as h:
        h.write(dst)
    idx = os.path.join(d, 'index')
    env = dict(IDENT)
    env['GIT_INDEX_FILE'] = idx
    git('read-tree', REV, env=env)
    blob = git('hash-object', '-w', '--path', path, fpath)
    git('update-index', '--add', '--cacheinfo', '100644,%s,%s' % (blob, path),
        env=env)
    tree = git('write-tree', env=env)
    commit = git('commit-tree', tree, '-p', REV, '-m',
                 'vacuity probe %s: %s' % (name, path), env=env)
    git('update-ref', 'refs/vacuity/%s' % name, commit)
    os.unlink(idx)
    return commit, hashlib.sha256(src).hexdigest(), hashlib.sha256(dst).hexdigest()


def counter(rev, freeze, tag):
    out = os.path.join(S, 'out', tag + '.json')
    argv = ['python3', '-I', '-B', COUNTER, '--root', CLONE, '--rev', rev,
            '--freeze', freeze, '--work', os.path.join(S, 'work'),
            '--json-out', out]
    t0 = time.time()
    p = run(argv)
    wall = time.time() - t0
    data = None
    if os.path.exists(out):
        with open(out) as h:
            data = json.load(h)
    rec = {
        'tag': tag,
        'rev': rev,
        'freeze': freeze,
        'exit_code': p.returncode,
        'wall_seconds': round(wall, 3),
        'stdout_sha256': hashlib.sha256(p.stdout.encode()).hexdigest(),
        'stderr_head': p.stderr[:400],
    }
    if data:
        rec.update({
            'entries_evaluated': data.get('entries_evaluated'),
            'mismatches': data.get('mismatches'),
            'mismatches_count': data.get('mismatches_count'),
            'frozen_path_changed': data.get('frozen_path_changed'),
            'unevaluable': [u.get('reason') for u in data.get('unevaluable') or []],
            'observed_by_id': {e['id']: e.get('observed')
                               for e in data.get('entries') or []},
            'match_by_id': {e['id']: e.get('match')
                            for e in data.get('entries') or []},
        })
    return rec


def sub(old, new, expect=1):
    o = old.encode() if isinstance(old, str) else old
    n = new.encode() if isinstance(new, str) else new

    def f(data):
        c = data.count(o)
        if c != expect:
            raise SystemExit('occurrence count %d != %d for %r' % (c, expect, old))
        return data.replace(o, n, expect)
    return f


def line_sub(anchor, old, new, expect_one_line=1):
    """Replace `old` with `new` only on the line containing `anchor`."""
    a = anchor.encode() if isinstance(anchor, str) else anchor
    o = old.encode() if isinstance(old, str) else old
    n = new.encode() if isinstance(new, str) else new

    def f(data):
        lines = data.split(b'\n')
        hits = [i for i, l in enumerate(lines) if a in l]
        if len(hits) != expect_one_line:
            raise SystemExit('anchor %r on %d lines' % (anchor, len(hits)))
        i = hits[0]
        if lines[i].count(o) != 1:
            raise SystemExit('target %r count %d on anchored line'
                             % (old, lines[i].count(o)))
        lines[i] = lines[i].replace(o, n, 1)
        return b'\n'.join(lines)
    return f


def del_map_stem(data):
    stem = b'`2026-10-13-asar-surface`, '
    if data.count(stem) != 1:
        raise SystemExit('map stem occurrence %d' % data.count(stem))
    return data.replace(stem, b'', 1)


PROBES = [
    # id, entry-id, class, path, mutate, note
    ('a1-correction-value', 'C2-a1-owned-coverage-count', 'count (correction block)',
     'SCORECARD.md', sub('c2-correction-value: 137/137', 'c2-correction-value: 137/998'),
     'mutate the machine-readable correction value the check reads'),
    ('a1-prose-value', 'C2-a1-owned-coverage-count', 'count (prose statement)',
     'SCORECARD.md', sub('137/137 knowledge files mapped', '137/998 knowledge files mapped'),
     'mutate the human statement claim; correction block still says 137/137'),
    ('h1-readme-map-stem', 'C2-h1-readme-coverage-map-complete', 'count (derived invariant)',
     'corpus/README.md', del_map_stem,
     'the asserted composite never appears in README; mutate the map data instead'),
    ('c01-pointer', 'C2-c01-cap-pointer', 'pointer',
     'SCORECARD.md',
     sub('.ufo/waves/luna-round-6/receipts/', '.ufo/waves/luna-round-6/receipts/-missing'),
     'break one evidence pointer of the checked row'),
    ('g1-planned-marker', 'C2-g1-planned-r34-to-35', 'expected-value (append marker)',
     'SCORECARD.md',
     line_sub('- **planned (round 35', 'after a steer', 'as first written'),
     'remove the steer marker from the planned row'),
    ('b1-pinned-occurrence', 'C2-b1-owned-coverage-count-pin', 'count (historical pin)',
     'SCORECARD.md', sub('133/133 knowledge files mapped', '133/997 knowledge files mapped'),
     'mutate the only live occurrence of the pinned asserted value'),
    ('d14-contains-range', 'C2-d14-province-round39-core-row', 'contains (cited range)',
     'SHONEN.md', sub('`PROVINCE.md:378-384`', '`PROVINCE.md:378-999`'),
     'push the cited range past EOF'),
]


def main():
    top = git('rev-parse', '--show-toplevel')
    assert os.path.realpath(top) == os.path.realpath(CLONE), (top, CLONE)
    results = {'baseline': None, 'probes': []}
    results['baseline'] = counter(REV, FREEZE, 'baseline')
    for name, eid, cls, path, mutate, note in PROBES:
        commit, src_sha, dst_sha = make_mutant(name, path, mutate)
        fit = counter(commit, commit, name + '.fit')
        scored = counter(commit, FREEZE, name + '.scored')
        results['probes'].append({
            'probe': name, 'entry': eid, 'class': cls, 'path': path,
            'note': note, 'mutant_commit': commit,
            'src_sha256': src_sha, 'mutant_sha256': dst_sha,
            'fitness_mode': {
                'exit_code': fit['exit_code'],
                'mismatches': fit['mismatches'],
                'observed_of_entry': (fit.get('observed_by_id') or {}).get(eid),
                'match_of_entry': (fit.get('match_by_id') or {}).get(eid),
                'entries_evaluated': fit['entries_evaluated'],
                'frozen_path_changed': fit['frozen_path_changed'],
                'wall_seconds': fit['wall_seconds'],
                'stdout_sha256': fit['stdout_sha256'],
            },
            'scored_mode': {
                'exit_code': scored['exit_code'],
                'mismatches': scored['mismatches'],
                'frozen_path_changed': scored['frozen_path_changed'],
                'entries_evaluated': scored['entries_evaluated'],
                'unevaluable': scored['unevaluable'],
                'wall_seconds': scored['wall_seconds'],
                'stdout_sha256': scored['stdout_sha256'],
            },
        })
        print(json.dumps(results['probes'][-1], sort_keys=True))
    with open(os.path.join(S, 'out', 'probes.json'), 'w') as h:
        json.dump(results, h, indent=1, sort_keys=True)
    print('BASELINE', json.dumps({k: results['baseline'][k] for k in
                                  ('exit_code', 'entries_evaluated', 'mismatches',
                                   'frozen_path_changed', 'wall_seconds')},
                                 sort_keys=True))


if __name__ == '__main__':
    main()
