import json, re, subprocess, sys, hashlib
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
FLEET = '/home/vgpnk/Projects/shokunin'
E = 'e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9'
T = '8847042a140b044dbf335210c965bf7b06b09b4f'
S = '/fast/scratch/hyaku/kaidoku-r49/C2LogPtr'
W1 = '.ufo/waves/round-48/w1'
def git(*a, repo=LANE):
    return subprocess.run(['git', '-C', repo] + list(a), capture_output=True).stdout
def sha(b): return hashlib.sha256(b).hexdigest()
log = git('show', E + ':LOG.md').decode('utf-8', 'replace').split('\n')
print('LOG.md@base lines(split \\n)=', len(log), 'sha256(blob)=', sha(git('show', E + ':LOG.md')))
print('LOG.md@tip == base:', git('show', T + ':LOG.md') == git('show', E + ':LOG.md'))
print('## A3 pointer line sets (8-hex substring, base blob)')
for h in ['2e785632', '33f65a91', 'c093e798', '7fe11332', '663f30ee', '0d76deed', '577a02a5', '8847042a', '0f06251b']:
    print(h, [i + 1 for i, l in enumerate(log) if h in l])
print('## A4 wave accounting')
res = json.loads(git('show', E + ':.ufo/waves/round-48/r48-w1-results.json'))['results']
names = [x['name'] for x in res]
tree = [p for p in git('ls-tree', '-r', '--name-only', E, '--', W1).decode().split('\n') if p]
print('results.json sha256=', sha(git('show', E + ':.ufo/waves/round-48/r48-w1-results.json')), 'seats=', len(names), 'unique=', len(set(names)))
print('w1 tree entries=', len(tree), 'tree sha256(newline-joined)=', sha(('\n'.join(tree) + '\n').encode()))
def has(n, mode):
    top = f'{W1}/{n}.md' in tree
    if mode == 'md_bound':
        return top or any(p.startswith(f'{W1}/{n}/') and p.endswith('.md') for p in tree)
    if mode == 'any_bound':
        return top or any(p.startswith(f'{W1}/{n}/') for p in tree)
    if mode == 'any_nobound':
        return any(p.startswith(f'{W1}/{n}') for p in tree)
for mode in ['md_bound', 'any_bound', 'any_nobound']:
    miss = [n for n in names if not has(n, mode)]
    print(f'{mode}: reports={len(names)-len(miss)} missing={miss}')
reg = json.loads(git('show', E + ':.ufo/waves/round-48/w1/swarm-registry.json'))['members']
print('swarm-registry members=', len(reg), 'same name set as results:', set(reg) == set(names))
import collections
print('registry role mix:', dict(collections.Counter(v['role'] for v in reg.values())))
print('registry agentId null:', sum(1 for v in reg.values() if v['agentId'] is None), 'planner:', [k for k, v in reg.items() if v['role'] == 'planner'])
print('results C1Meaning/C1Battery/ScribeReportNumbers blocked-or-aborted notes:')
for x in res:
    if x['name'] in ('C1Meaning', 'C1Battery', 'ScribeReportNumbers'):
        print(' ', x['name'], 'frozen_worktree_dirty' in x['output'], 'dirty-worktree' in x['output'], 'aborted' in x['output'])
print('## fleet report (commit 7b845bef) citations of LOG.md with hashes')
fl = git('show', '7b845bef80a797b7b90944c6ab2752dbbc9afaa9:.ufo/reports/round-48/kaidoku.md', repo=FLEET).decode('utf-8').split('\n')
for i, l in enumerate(fl, 1):
    cites = [(int(m.group(1)), int(m.group(2) or m.group(1))) for m in re.finditer(r'LOG\.md:(\d+)(?:-(\d+))?', l)]
    if not cites: continue
    for h in sorted(set(x[:8] for x in re.findall(r'\b[0-9a-f]{8}(?:[0-9a-f]{32})?\b', l))):
        ls = [j + 1 for j, x in enumerate(log) if h in x]
        for a, b in cites:
            inr = [x for x in ls if a <= x <= b]
            if not ls or inr != ls:
                print(f'fleet L{i} cite LOG.md:{a}-{b} hash {h} LOG lines {ls} within-cite {inr}')
print('## fleet L14 wave claim:', [l for l in fl if 'Dispatched one v2 wave' in l][0][:260])
