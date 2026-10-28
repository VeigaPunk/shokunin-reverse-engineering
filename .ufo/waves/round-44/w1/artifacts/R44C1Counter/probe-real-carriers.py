#!/usr/bin/env python3
"""R44C1Counter dev harness: oracle-merge snippet + a freeze-shaped scratch lane.

Two outputs, neither of them a lane file:

  carriers.oracle-merge.json
      the per-carrier `oracle` blocks the counter requires, derived from the
      R44C1Oracle measured census (members / nonregular / output_tree digest)
      and the output_tree roots already frozen in tools/round-44/carriers.json.
      The L1 merges these into the four frozen carriers before the freeze.

  <work>/lane
      a scratch git lane shaped like the lane at the freeze (the four real
      carrier blobs, the committed S138 trees, a merged carriers.json for
      exactly the four preregistered carriers, the frozen tool pins and doc
      fixtures) so the counter can be dry-run on REAL bytes without receipts
      and without touching corpus/evidence/round-44/c1.

Usage: python3 -I -B probe-real-carriers.py [--lane DIR] [--work DIR]
Exit 0 when every carrier's census rows reproduce the committed tree digest.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import importlib.util
_spec = importlib.util.spec_from_file_location(
    'c1counter', os.path.join(HERE, 'c1-counter.py'))
C1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C1)

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
ORACLE = os.path.join(LANE, '.ufo/waves/round-44/w1/artifacts/R44C1Oracle/'
                            'carriers.oracle-block.json')
SCRATCH = os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git(d, *args):
    p = subprocess.run(['git', '-C', d, *args], capture_output=True)
    if p.returncode != 0:
        raise SystemExit('git %r: %s' % (args, p.stderr.decode()))
    return p.stdout.decode().strip()


def main():
    work = os.path.join(SCRATCH, 'kaidoku-r44', 'probe-R44C1Counter')
    os.makedirs(work, exist_ok=True)
    lane = os.path.join(work, 'lane')
    if os.path.isdir(lane):
        shutil.rmtree(lane)
    os.makedirs(lane)

    table = json.load(open(os.path.join(LANE, 'tools/round-44/carriers.json')))
    art = json.load(open(ORACLE))['carriers']
    by_id = {c['id']: c for c in table['carriers']}
    merge, problems = {}, []
    for cid in C1.EXPECTED_IDS:
        c = by_id.get(cid)
        blk = art.get(cid)
        if c is None or blk is None:
            problems.append('%s: no carrier entry or no oracle block' % cid)
            continue
        members = [{'path': m['path'], 'sha256': m['sha256'], 'size': m['size']}
                   for m in blk['members']]
        digest = blk['output_tree_digest']
        written = sha(''.join('%s\t%s\n' % (m['path'], m['sha256'])
                              for m in sorted(members, key=lambda m: m['path']))
                      .encode())
        if written != digest:
            problems.append('%s: census rows do not reproduce the tree digest' % cid)
        if len(members) != c.get('expected_regular'):
            problems.append('%s: %d rows != expected_regular %r'
                            % (cid, len(members), c.get('expected_regular')))
        merge[cid] = {
            'oracle': {
                'tool': '/usr/bin/unsquashfs',
                'version': '4.7.5',
                'members': members,
                'nonregular': [{'path': n['path'], 'kind': n['kind']}
                               for n in blk.get('nonregular') or []],
            },
            'output_tree': {
                'root': c['output_tree'],
                'digest': digest,
                'digest_rule': C1.TREE_DIGEST_RULE,
            },
        }
    out = os.path.join(HERE, 'carriers.oracle-merge.json')
    with open(out, 'w') as fh:
        json.dump({'claim': 'R44-C1', 'target': C1.TARGET,
                   'note': 'merge each block into the carrier of the same id in '
                           'tools/round-44/carriers.json before the freeze',
                   'carriers': merge}, fh, indent=1, sort_keys=True)
    print('merge snippet', out, sha(open(out, 'rb').read()))

    # ---- scratch lane: real bytes, committed trees, merged frozen table
    copied = 0
    for cid, c in by_id.items():
        if cid not in C1.EXPECTED_IDS:
            continue
        for rel in (c['path'],):
            dst = os.path.join(lane, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(os.path.join(LANE, rel), dst)
            copied += 1
        troot = c['output_tree']
        for dirpath, _dirs, files in os.walk(os.path.join(LANE, troot)):
            for name in files:
                src = os.path.join(dirpath, name)
                rel = os.path.relpath(src, LANE)
                dst = os.path.join(lane, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(src, dst)
                copied += 1
    for rel in ('tools/round-27/xpin-attribute.mjs',
                'tools/round-44/rea-pkg.json' if os.path.exists(
                    os.path.join(LANE, 'tools/round-44/rea-pkg.json'))
                else 'tools/round-42/rea-pkg.json',
                'tools/round-42/prior-pins.json',
                'tools/round-42/fixtures.json',
                os.path.join(HERE, 'c1-counter.py')):
        src = rel if os.path.isabs(rel) else os.path.join(LANE, rel)
        if not os.path.isfile(src):
            problems.append('missing frozen input %r' % rel)
            continue
        dst = os.path.join(lane, 'tools/round-44/c1-counter.py'
                           if rel.endswith('c1-counter.py') else rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        copied += 1

    frozen = {
        'claim': 'R44-C1', 'round': 44, 'schema': 'kaidoku-r44-carriers-v1',
        'target': C1.TARGET, 'carriers': [],
    }
    for cid in C1.EXPECTED_IDS:
        c = dict(by_id[cid])
        c.pop('superblock_layout', None)
        c.update(merge[cid])
        c['endian'] = c.pop('endian')
        frozen['carriers'].append(c)
    with open(os.path.join(lane, 'tools/round-44/carriers.json'), 'w') as fh:
        json.dump(frozen, fh, indent=1, sort_keys=True)

    docs = {
        'plans/round-44-claims.md': '# plan (dev lane copy)\n',
        'PROVINCE.md': C1._province(),
        C1.ENTRY: C1._entry(),
        'corpus/SOURCES.md': C1._registry(),
        'corpus/README.md': C1._readme(),
        'corpus/evidence/round-44/c1/.keep': '',
    }
    for rel, content in docs.items():
        dst = os.path.join(lane, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, 'w') as fh:
            fh.write(content)
    subprocess.run(['git', '-C', lane, 'init', '-q'], check=True)
    subprocess.run(['git', '-C', lane, 'add', '-A'], check=True)
    subprocess.run(['git', '-C', lane, '-c', 'user.name=fx', '-c',
                    'user.email=fx@fx', 'commit', '-qm', 'dev lane'], check=True)
    rev = git(lane, 'rev-parse', 'HEAD')
    print(json.dumps({'lane': lane, 'rev': rev, 'files': copied,
                      'problems': problems}, sort_keys=True))
    return 0 if not problems else 1


if __name__ == '__main__':
    sys.exit(main())
