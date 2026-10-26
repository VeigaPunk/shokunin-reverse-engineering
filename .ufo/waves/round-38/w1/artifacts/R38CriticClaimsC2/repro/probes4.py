#!/usr/bin/env python3
"""Pointer-count-matched SCORECARD Owned-axes shadow + full guard detail for the frozen c2-2/c2-3 controls."""
import importlib.util, json, os, shutil, subprocess
S = os.environ['S']; FX = os.path.join(S, 'fx'); LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
BASE='77091b492cc53f8743bd0701b1e7d5e66123dd84'; COUNTER=os.path.join(LANE,'tools/round-38/c2-counter.py')
ENV=dict(os.environ,GIT_AUTHOR_NAME='critic',GIT_AUTHOR_EMAIL='c@i',GIT_COMMITTER_NAME='critic',GIT_COMMITTER_EMAIL='c@i')
def git(*a): return subprocess.run(['git','-C',FX]+list(a),capture_output=True,text=True,check=True)
def read(p): return open(os.path.join(FX,p)).read()
def wri(p,t): open(os.path.join(FX,p),'w').write(t)
def repair():
    L=read('PROVINCE.md').splitlines(True)
    i=next(n for n,l in enumerate(L) if l.startswith('| REA MCP server |'))
    L[i]=L[i].replace('doctor outputs in `evidence/doctor/`','doctor outputs in `.ufo/waves/round-19/evidence/doctor/`')
    wri('PROVINCE.md',''.join(L))
DUP=('| coverage | 9.72 -> 10.0 | 124/124 knowledge files mapped (`corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`, '
     '`corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md`); command A `tools/round-36/c2-counter.py` | '
     '`corpus/README.md`; `plans/round-36-claims.md`; `.ufo/waves/round-31/w1/ScribeScorecardRows.md` | round 36 |\n')
git('checkout','-q','-B','e2-shadow-owned-axis',BASE); git('clean','-qfd')
repair()
s=read('SCORECARD.md').splitlines(True)
i=next(n for n,l in enumerate(s) if l.startswith('| coverage |'))
s[i]=s[i].replace('124/124 knowledge files mapped','7/7 knowledge files mapped')
s.insert(i+1,DUP); wri('SCORECARD.md',''.join(s))
git('add','-A'); git('commit','-qm','e2'); rev=git('rev-parse','HEAD').stdout.strip()
r=subprocess.run(['python3','-I','-B',COUNTER,'--root',FX,'--rev',rev,'--base',BASE,'--json-out',os.path.join(S,'e2.json')],capture_output=True,text=True,env=ENV)
print('OWNED-AXIS SHADOW:',r.returncode,r.stdout.strip())
print('first-row-token-still-in-file:', '7/7 knowledge files mapped' in read('SCORECARD.md'))
# full guard detail for the frozen c2-2 / c2-3 fixtures, importing the counter directly
spec=importlib.util.spec_from_file_location('c2',COUNTER); c2=importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
spec2=importlib.util.spec_from_file_location('gc',os.path.join(LANE,'tools/round-38/gen-controls.py')); gc=importlib.util.module_from_spec(spec2); spec2.loader.exec_module(gc)
out={}
for kind,defect in (('c2-2','delete'),('c2-3','substitute')):
    d,b,rv,c=gc.c2_fixture(kind,defect)
    res=c2.measure(d,rv,b)
    chg=[p for p in subprocess.run(['git','-C',d,'diff','--name-only',b,rv],capture_output=True,text=True).stdout.split()]
    sc_base=subprocess.run(['git','-C',d,'show',f'{b}:SCORECARD.md'],capture_output=True,text=True).stdout
    sc_rev=subprocess.run(['git','-C',d,'show',f'{rv}:SCORECARD.md'],capture_output=True,text=True).stdout
    pv_base=subprocess.run(['git','-C',d,'show',f'{b}:PROVINCE.md'],capture_output=True,text=True).stdout
    pv_rev=subprocess.run(['git','-C',d,'show',f'{rv}:PROVINCE.md'],capture_output=True,text=True).stdout
    out[kind]={'exit':0 if res['met_target'] else 1,'mismatches':res['mismatches'],'pointers':res['pointers'],
               'guards':res['guards'],'guards_ok':res['guards_ok'],'changed_files':chg,
               'province_diff':[x for x in pv_base.splitlines() if x not in pv_rev.splitlines()],
               'scorecard_diff':[x for x in sc_base.splitlines() if x not in sc_rev.splitlines()]}
    print(kind,json.dumps({k:out[kind][k] for k in ('exit','mismatches','pointers','guards_ok','changed_files')}))
    print(kind,'guards:',json.dumps(out[kind]['guards']))
    shutil.rmtree(d,ignore_errors=True)
json.dump(out,open(os.path.join(S,'controls_detail.json'),'w'),indent=1)
