#!/usr/bin/env python3
"""Record R24 before/after commands from one committed snapshot in a scratch clone.

Not independent admission. --root LANE --rev REV --out NEW_DIR; retains each
argv/exit/stdout/stderr and executed script digest, with exact expected finite
outcomes. Final census is separately recorded on the live lane.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

B = 'fe10219ec6e92c32b7eb40d83fbcac888756c6c1'
F = '5dc49bfe25d21139693161c786e69c5a11a65bcc'
W = '.ufo/waves/round-24'

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--rev', required=True)
    p.add_argument('--out', type=Path, required=True)
    a=p.parse_args()
    root=a.root.resolve()
    env={k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_NO_REPLACE_OBJECTS='1', GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    def git(repo,*args):
        return subprocess.run(['git','-C',str(repo),*args],capture_output=True,check=True,env=env).stdout
    rev=git(root,'rev-parse',a.rev+'^{commit}').decode().strip()
    a.out.mkdir(parents=True,exist_ok=False)
    parent=Path('/fast/scratch/hyaku/kaidoku-r24');parent.mkdir(parents=True,exist_ok=True)
    temp=Path(tempfile.mkdtemp(prefix='final-',dir=parent))
    checks=[]
    try:
        clone=temp/'lane'
        subprocess.run(['git','clone','-q','--shared',str(root),str(clone)],check=True,env=env)
        git(clone,'checkout','-q','--detach',rev)
        def record(name,argv,expected,predicate):
            r=subprocess.run(argv,cwd=clone,capture_output=True,text=True,env=env)
            try: data=json.loads(r.stdout)
            except ValueError: data={}
            ok=r.returncode==expected and predicate(data,r.stdout)
            script=Path(argv[3]) if argv[:3]==[sys.executable,'-I','-B'] else None
            item={'source_rev':rev,'argv':argv,'cwd':str(clone),'exit':r.returncode,
                  'expected_exit':expected,'stdout':r.stdout,'stderr':r.stderr,'passed':ok}
            if script and script.is_file(): item['executed_sha256']=hashlib.sha256(script.read_bytes()).hexdigest()
            (a.out/(name+'.json')).write_text(json.dumps(item,indent=2)+'\n')
            checks.append({'name':name,'passed':ok})
        def py(rel,*args):return [sys.executable,'-I','-B',str(clone/rel),*args]
        for name,at,n,code in [('before-c1',B,0,1),('after-c1',rev,4,0)]:
            record(name,py(W+'/tools/count-c1.py','--root',str(clone),'--rev',at),code,
                   lambda d,s,n=n:d.get('t2_held_count')==n and d.get('t2_total')==4)
        ga=['--root',str(clone),'--require-clean','round-24','--disclosures','corpus/claim-freezes.tsv']
        record('before-c2',py(W+'/tools/freeze-gate.py',*ga,'--rev',B),1,
               lambda d,s:d.get('disclosures',{}).get('exact')==0 and d['disclosures']['of']==10)
        record('after-c2-revised',py(W+'/tools/freeze-gate.py',*ga,'--rev',rev),0,
               lambda d,s:d.get('disclosures',{}).get('exact')==11 and not d.get('required_failed'))
        frozen=temp/'frozen-gate.py';frozen.write_bytes(git(root,'show',F+':'+W+'/tools/freeze-gate.py'))
        record('after-c2-frozen', [sys.executable,'-I','-B',str(frozen),*ga,'--rev',rev],1,
               lambda d,s:d.get('disclosures',{}).get('exact')==9 and d['disclosures']['mismatched']==['round-17','round-18'])
        for r,n,expected,key in [('23',4,1,'t1_exercised_count'),('22',1,1,'t1_exercised_count')]:
            record('r'+r+'-c1',py('.ufo/waves/round-'+r+'/tools/count-c1.py','--root',str(clone),'--rev',rev),expected,
                   lambda d,s,n=n,key=key:d.get(key)==n)
        record('r22-c2',py('.ufo/waves/round-22/tools/count-c2.py','--root',str(clone),'--rev',rev),0,
               lambda d,s:d.get('accounted_count')==14)
        record('selftest',py(W+'/tools/selftest.py','--root',str(clone),'--rev',rev),0,
               lambda d,s:'"cases": 17, "passed": 17, "exit": 0' in s)
        record('prior-controls',py('.ufo/waves/round-21/controls.py','--root',str(clone),'--before',B,'--after',rev),0,
               lambda d,s:d.get('finding')=='controls_clean')
        def retained(old,new):
            it=iter(new)
            return all(any(x==line for x in it) for line in old)
        old_readme=[x for x in git(root,'show',B+':corpus/README.md').decode().splitlines() if x]
        new_readme=[x for x in (clone/'corpus/README.md').read_text().splitlines() if x]
        old_source_lines=git(root,'show',B+':corpus/SOURCES.md').decode().splitlines()
        new_source_lines=(clone/'corpus/SOURCES.md').read_text().splitlines()
        preserve={'old_readme_nonempty_retained':retained(old_readme,new_readme),
                  'whole_old_sources_retained':retained(old_source_lines,new_source_lines)}
        # Named red controls exercise the preservation predicates, not just the green tree.
        preserve['red_readme_row_loss']=not retained(old_readme,[x for x in new_readme if x!=old_readme[10]])
        preserve['red_source_nonrow_loss']=not retained(old_source_lines,[x for x in new_source_lines if x!=old_source_lines[0]])
        preserve['red_separator_loss']=not all(i==0 or ['## A','| row |','## B'][i-1]=='' for i,l in enumerate(['## A','| row |','## B']) if l.startswith('## '))
        (a.out/'preservation-controls.json').write_text(json.dumps(preserve,indent=2)+'\n')
        checks.append({'name':'preservation-controls','passed':all(preserve.values())})
        readme=(clone/'corpus/README.md').read_text().splitlines()
        separator_ok=all(i==0 or readme[i-1]=='' for i,l in enumerate(readme) if l.startswith('## '))
        row={'source_rev':rev,'before_headings_blank':separator_ok,'prior_sources_unchanged':True,
             'knowledge_count':len(list((clone/'corpus/knowledge').glob('*.md')))}
        old=[x for x in git(root,'show',B+':corpus/SOURCES.md').decode().splitlines() if x.startswith('| S')]
        new=[x for x in (clone/'corpus/SOURCES.md').read_text().splitlines() if x.startswith('| S')]
        row['prior_sources_unchanged']=new[:len(old)]==old
        row.update(sources_before=len(old),sources_after=len(new))
        (a.out/'readme-sources.json').write_text(json.dumps(row,indent=2)+'\n')
        checks.append({'name':'readme-sources','passed':separator_ok and row['prior_sources_unchanged']})
        summary={'source_rev':rev,'checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks),'failed':[x['name'] for x in checks if not x['passed']]}
        (a.out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
        print(json.dumps(summary));return 1 if summary['failed'] else 0
    finally:shutil.rmtree(temp,ignore_errors=True)

if __name__=='__main__':sys.exit(main())
