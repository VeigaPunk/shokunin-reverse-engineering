#!/usr/bin/env python3
"""Independent C2 re-derivation: no counter code, only git blobs + the frozen interpreter."""
import json, os, subprocess, sys

L = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
REV = '42c10a58cb2cae3a4a0122af35a0cf95ac718043'
FREEZE = '7fce308631a8b457d6b7c5a4b39a923c4e9a49de'
S = os.environ['S']
OUT = os.path.join(S, 'indep')
os.makedirs(OUT, exist_ok=True)


def show(rev, path):
    p = subprocess.run(['git', '-C', L, 'show', '%s:%s' % (rev, path)], capture_output=True)
    if p.returncode:
        raise SystemExit('missing %s at %s' % (path, rev[:8]))
    return p.stdout


skill = show(REV, 'SKILL.md')
interp = show(FREEZE, 'tools/round-40/sqfs-triage-v2.py')
man = json.loads(show(REV, 'corpus/evidence/round-40/c2/heldout/manifest.json'))
open(os.path.join(OUT, 'SKILL.md'), 'wb').write(skill)
open(os.path.join(OUT, 'interp.py'), 'wb').write(interp)

paths = []
for c in man['carriers']:
    d = c['carrier'].split('/')[0]
    ep = 'corpus/evidence/round-40/c2/heldout/%s/envelope.json' % d
    fp = os.path.join(OUT, d + '.envelope.json')
    open(fp, 'wb').write(show(REV, ep))
    paths.append(fp)

p = subprocess.run([sys.executable, '-I', '-B', os.path.join(OUT, 'interp.py'),
                    '--skill', os.path.join(OUT, 'SKILL.md'), '--json'] + paths,
                   capture_output=True, text=True)
print('interp exit', p.returncode, 'stdout bytes', len(p.stdout))
if p.returncode:
    print(p.stderr[-2000:])
    raise SystemExit(1)
doc = json.loads(p.stdout)
byname = {os.path.basename(r['path']).split('.')[0]: r for r in doc['results']}
print('rules in table', doc['rules'], 'envelopes parsed', len(byname))
print('actions vocabulary', doc['actions'])
matched = 0
pairs = {}
for c in man['carriers']:
    r = byname.get(c['id'], {})
    want = (c['label'], c['action'])
    got = (r.get('label'), r.get('action'))
    ok = got == want
    matched += ok
    pairs.setdefault(want, set()).add(r.get('rule'))
    print('%s %-26s want=%-20s got=%-20s rule=%-4s %s'
          % (c['id'], c['class'], '%s/%s' % want, '%s/%s' % got, r.get('rule'),
             'OK' if ok else 'MISS'))
print('MATCHED %d/%d' % (matched, len(man['carriers'])))
uniq = {next(iter(v)) for v in pairs.values()}
print('distinct pairs', len(pairs), 'distinct rules', len(uniq),
      'one-rule-per-pair', all(len(v) == 1 for v in pairs.values()))
for k in sorted(pairs, key=str):
    print('  %-40s -> rule %s' % ('%s/%s' % k, sorted(pairs[k], key=str)))
