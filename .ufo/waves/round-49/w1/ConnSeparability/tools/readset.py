import json, re, subprocess, sys, collections
S = '/fast/scratch/hyaku/kaidoku-r49/ConnSeparability'
revs = dict(l.split('=') for l in open(f'{S}/out/revs.txt').read().split())
FREEZE, XREV, YREV = revs['FREEZE'], revs['XREV'], revs['YREV']
LABEL = {FREEZE: 'FREEZE', XREV: 'XREV', YREV: 'YREV', 'e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9': 'LANE_BASE',
         '61b87d742032e65fca9c38267d7d6ed7e555edad': 'R48_BASE', '8847042a140b044dbf335210c965bf7b06b09b4f': 'R48_TIP'}
def lab(r): return LABEL.get(r, r)
SUB = {'show', 'rev-parse', 'ls-tree', 'log', 'diff', 'cat-file', 'merge-base'}
def parse(path):
    reads = collections.defaultdict(set)   # (label) -> set of paths read by content (show / rev-parse REV:PATH)
    other = []
    for line in open(path):
        t = line.rstrip('\n').split('\t')
        if t[0] != 'git': continue
        a = t[1:]
        if a[:1] == ['-C']: a = a[2:]
        if not a: continue
        sub = a[0]
        if sub in ('show', 'rev-parse') and len(a) >= 2 and ':' in a[1] and not a[1].endswith('^{commit}'):
            rev, p = a[1].split(':', 1)
            reads[lab(rev)].add(p)
        elif sub == 'ls-tree':
            other.append(('ls-tree', lab(a[-2]) if len(a) >= 2 else '', a[-1]))
        elif sub == 'log':
            if '--' in a:
                i = a.index('--'); other.append(('log', ' '.join(lab(x) for x in a[i-1:i]) if i else '', ' '.join(a[i+1:])))
            else:
                other.append(('log', a[-1], ''))
        elif sub == 'diff':
            other.append(('diff', ' '.join(lab(x) for x in a[-2:]), '--name-only'))
    return reads, other
out = {}
for tag in ['c1-X', 'c1-Y', 'c1-F', 'c2-X', 'c2-Y', 'c2-F']:
    r, o = parse(f'{S}/trace/{tag}.log')
    out[tag] = {'content_reads': {k: sorted(v) for k, v in r.items()},
                'name_or_tree_ops': sorted(set(map(tuple, o)))}
    print('==', tag, 'trace lines:', sum(1 for _ in open(f'{S}/trace/{tag}.log')))
    for k, v in sorted(r.items()):
        print('  ', k, len(v))
        for p in sorted(v): print('      ', p)
    for x in sorted(set(map(tuple, o))): print('   op', x)
json.dump(out, open(f'{S}/out/readsets.json', 'w'), indent=1, sort_keys=True)
