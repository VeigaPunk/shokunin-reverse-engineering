#!/usr/bin/env python3
"""Third wave: pointer-count-matched Owned-axes shadow; decoy rows with the Adjacent drift compensated."""
import json, os, subprocess
S = os.environ['S']; FX = os.path.join(S, 'fx')
BASE = '77091b492cc53f8743bd0701b1e7d5e66123dd84'
COUNTER = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-38/c2-counter.py'
ENV = dict(os.environ, GIT_AUTHOR_NAME='critic', GIT_AUTHOR_EMAIL='c@i',
           GIT_COMMITTER_NAME='critic', GIT_COMMITTER_EMAIL='c@i')
def git(*a): return subprocess.run(['git','-C',FX]+list(a),capture_output=True,text=True,check=True)
def read(p): return open(os.path.join(FX,p)).read()
def wri(p,t): open(os.path.join(FX,p),'w').write(t)
def fresh(b):
    git('checkout','-q','-B',b,BASE); git('clean','-qfd')
def repair():
    L=read('PROVINCE.md').splitlines(True)
    i=next(n for n,l in enumerate(L) if l.startswith('| REA MCP server |'))
    L[i]=L[i].replace('doctor outputs in `evidence/doctor/`','doctor outputs in `.ufo/waves/round-19/evidence/doctor/`')
    wri('PROVINCE.md',''.join(L))
def bump_adj():
    s=read('SHONEN.md'); wri('SHONEN.md', s.replace('`PROVINCE.md:97-125`','`PROVINCE.md:98-126`'))
DUP_AXIS = ('| coverage | 9.72 -> 10.0 | 124/124 knowledge files mapped after the round-36 landing '
            '(`corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`, '
            '`corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md`); command A in '
            '`tools/round-36/c2-counter.py` | `corpus/README.md` | round 36 |\n')
def shadow_axis():
    s=read('SCORECARD.md').splitlines(True)
    i=next(n for n,l in enumerate(s) if l.startswith('| coverage |'))
    assert '124/124 knowledge files mapped' in s[i]
    s[i]=s[i].replace('124/124 knowledge files mapped','7/7 knowledge files mapped')
    s.insert(i+1,DUP_AXIS); wri('SCORECARD.md',''.join(s))
def decoy_glob():
    L=read('PROVINCE.md').splitlines(True)
    i=next(n for n,l in enumerate(L) if l.startswith('| REA MCP server |'))
    L.insert(i+1,'| squashfs probe outputs | x | `corpus/evidence/round-38/c1/*` (glob pointer) |\n')
    wri('PROVINCE.md',''.join(L))
def decoy_frag():
    L=read('PROVINCE.md').splitlines(True)
    i=next(n for n,l in enumerate(L) if l.startswith('| REA MCP server |'))
    L.insert(i+1,'| squashfs probe outputs | x | `corpus/evidence/round-38/c1/K1/after.json#L5` (fragment pointer) |\n')
    wri('PROVINCE.md',''.join(L))
def chain(*fs):
    def r():
        for f in fs: f()
    return r
CASES=[('e-shadow-owned-axis',chain(repair,shadow_axis),'(b) Owned-axes duplicate row (4 pointers, count-matched) shadows 7/7'),
       ('e-decoy-glob',chain(repair,bump_adj,decoy_glob),'(f) new Core row, unresolvable glob pointer, Adjacent drift compensated'),
       ('e-decoy-frag',chain(repair,bump_adj,decoy_frag),'(f) new Core row, unresolvable fragment pointer, Adjacent drift compensated')]
out=[]
for b,fn,desc in CASES:
    fresh(b); fn(); git('add','-A'); git('commit','-qm',b); rev=git('rev-parse','HEAD').stdout.strip()
    r=subprocess.run(['python3','-I','-B',COUNTER,'--root',FX,'--rev',rev,'--base',BASE,'--json-out',os.path.join(S,b+'.json')],capture_output=True,text=True,env=ENV)
    res=json.loads(r.stdout); full=json.load(open(os.path.join(S,b+'.json')))
    rec={'branch':b,'desc':desc,'rev':rev,'exit':r.returncode,**{k:res.get(k) for k in ('mismatches','unresolved','assertion_mismatches','guards_ok','met_target')},'pointers':full.get('pointers'),'guards':full.get('guards')}
    out.append(rec); print(json.dumps({k:rec[k] for k in ('branch','rev','exit','mismatches','unresolved','assertion_mismatches','guards_ok','met_target','pointers')}))
json.dump(out,open(os.path.join(S,'probes3.json'),'w'),indent=1)
