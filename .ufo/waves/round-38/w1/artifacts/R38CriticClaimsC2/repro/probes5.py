#!/usr/bin/env python3
"""Fourth wave: command-B evidence rewrite (fewer/extra obligations) and the live HEAD measurement."""
import json, os, subprocess
S=os.environ['S']; FX=os.path.join(S,'fx'); BASE='77091b492cc53f8743bd0701b1e7d5e66123dd84'
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
FROZEN=os.path.join(LANE,'tools/round-38/c2-counter.py'); PATCH=os.path.join(S,'patched-c2.py')
ENV=dict(os.environ,GIT_AUTHOR_NAME='c',GIT_AUTHOR_EMAIL='c@i',GIT_COMMITTER_NAME='c',GIT_COMMITTER_EMAIL='c@i')
def git(*a): return subprocess.run(['git','-C',FX]+list(a),capture_output=True,text=True,check=True)
def read(p): return open(os.path.join(FX,p)).read()
def wri(p,t): open(os.path.join(FX,p),'w').write(t)
def repair():
    L=read('PROVINCE.md').splitlines(True)
    i=next(n for n,l in enumerate(L) if l.startswith('| REA MCP server |'))
    L[i]=L[i].replace('doctor outputs in `evidence/doctor/`','doctor outputs in `.ufo/waves/round-19/evidence/doctor/`')
    wri('PROVINCE.md',''.join(L))
def fewer_obligations():
    p='evidence/round-1-2026-10-15/result.json'; d=json.loads(read(p))
    d['obligations']=[o for o in d['obligations'] if o.get('status')=='aligned'][:2]
    wri(p,json.dumps(d,indent=1))
    s=read('SCORECARD.md'); assert '9/9 preselected reconciliation obligations aligned' in s
    wri('SCORECARD.md', s.replace('9/9 preselected reconciliation obligations aligned','2/2 preselected reconciliation obligations aligned'))
def extra_obligations():
    p='evidence/round-1-2026-10-15/result.json'; d=json.loads(read(p))
    d['obligations']=d['obligations']+[{'id':'junk%d'%i,'status':'aligned'} for i in range(5)]
    wri(p,json.dumps(d,indent=1))
    s=read('SCORECARD.md'); assert '9/9 preselected reconciliation obligations aligned' in s
    wri('SCORECARD.md', s.replace('9/9 preselected reconciliation obligations aligned','14/14 preselected reconciliation obligations aligned'))
def run(branch,fn):
    git('checkout','-q','-B',branch,BASE); git('clean','-qfd'); repair(); fn()
    git('add','-A'); git('commit','-qm',branch); rev=git('rev-parse','HEAD').stdout.strip()
    row={'branch':branch,'rev':rev}
    for lab,c in (('frozen',FROZEN),('patched',PATCH)):
        r=subprocess.run(['python3','-I','-B',c,'--root',FX,'--rev',rev,'--base',BASE],capture_output=True,text=True,env=ENV)
        o=json.loads(r.stdout)
        row[lab]={'exit':r.returncode,'met':o['met_target'],'mismatches':o['mismatches'],
                  'assert':o['assertion_mismatches'],'observed_b':None}
    full=subprocess.run(['python3','-I','-B',FROZEN,'--root',FX,'--rev',rev,'--base',BASE,'--json-out',os.path.join(S,branch+'.json')],capture_output=True,text=True,env=ENV)
    row['observed_b']=json.load(open(os.path.join(S,branch+'.json')))['observed']['command_b']
    return row
out=[run('f-fewer-obligations',fewer_obligations),run('f-extra-obligations',extra_obligations)]
for r in out:
    print(json.dumps({k:r[k] for k in ('branch','rev','observed_b')}), '| frozen', json.dumps(r['frozen']), '| patched', json.dumps(r['patched']))
# live lane HEAD
for lab,root,rev in (('lane-HEAD',LANE,subprocess.run(['git','-C',LANE,'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()),):
    for cname,c in (('frozen',FROZEN),('patched',PATCH)):
        r=subprocess.run(['python3','-I','-B',c,'--root',root,'--rev',rev,'--base',BASE],capture_output=True,text=True)
        print(lab,cname,'rev',rev,r.returncode,r.stdout.strip()[:400])
json.dump(out,open(os.path.join(S,'probes5.json'),'w'),indent=1)
