#!/usr/bin/env python3
"""Retain explicit round22 measurements at immutable Git revisions.

This is an evidence producer, not a general admission gate. Final conditions
are fixed below; all child argv/stdout/stderr/exits and source digests remain.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

B = '7787fea4d6fd718726de92ed20759d11ce7b8b48'
W = '.ufo/waves/round-22'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',required=True)
    parser.add_argument('--rev',required=True)
    parser.add_argument('--out',required=True)
    args=parser.parse_args()
    root=Path(args.root).resolve()
    out=Path(args.out).resolve()
    out.mkdir(parents=True,exist_ok=False)
    def git(*argv,where=root):
        return subprocess.run(['git','-C',str(where),*argv],capture_output=True,check=True).stdout
    rev=git('rev-parse','--verify',args.rev+'^{commit}').decode().strip()
    checks=[]
    def record(name,argv,expect,validate=None):
        proc=subprocess.run(argv,capture_output=True,text=True,check=False)
        try: data=json.loads(proc.stdout)
        except ValueError: data=None
        row={'name':name,'source_rev':rev,'argv':argv,'exit':proc.returncode,
             'expected_exit':expect,'stdout':proc.stdout,'stderr':proc.stderr,
             'pass':proc.returncode==expect and (validate is None or validate(data))}
        (out/(name+'.json')).write_text(json.dumps(row,indent=2)+'\n')
        checks.append({'name':name,'pass':row['pass'],'exit':proc.returncode})
        return data
    python=[sys.executable,'-I','-B']
    sources={}
    with tempfile.TemporaryDirectory(prefix='kaidoku-r22-pinned-tools-') as directory:
        tools=Path(directory)
        # Execute the requested revision's source, not uncommitted current tools.
        for path in [W+'/tools/count-c1.py',W+'/tools/count-c2.py',W+'/tools/counter-fixtures.py']:
            content=git('show',rev+':'+path)
            dest=tools/Path(path).name; dest.write_bytes(content)
            sources[path]=hashlib.sha256(content).hexdigest()
        # Source dependencies remain byte-identical to B; counters read Git data at rev.
        dependencies=['.ufo/waves/round-20/tools/verb-coverage.py','.ufo/waves/round-21/tools/verb-coverage.py']
        dep_same={path:git('show',B+':'+path)==git('show',rev+':'+path)==(root/path).read_bytes() for path in dependencies}
        for claim in ['c1','c2']:
            counter=str(tools/('count-'+claim+'.py'))
            record('before-'+claim,python+[counter,'--root',str(root),'--rev',B],1,
                   lambda data: data is not None and data.get('t1_exercised_count',data.get('accounted_count'))==0)
            record('after-'+claim,python+[counter,'--root',str(root),'--rev',rev],1 if claim=='c1' else 0,
                   (lambda data:data is not None and data['t1_exercised_count']>=1) if claim=='c1' else
                   (lambda data:data is not None and data['accounted_count']==14 and not data['mismatched'] and not data['foreign_rows']))
            record('controls-'+claim,python+[str(tools/'counter-fixtures.py'),'--claim',claim.upper(),'--counter',counter,'--root',str(root)],0)
            record('red-'+claim,python+[str(tools/'counter-fixtures.py'),'--claim',claim.upper(),'--counter',str(root/W/'frozen'/('count-'+claim+'.py')),'--root',str(root)],1)
        record('prior-controls',python+[str(root/'.ufo/waves/round-21/controls.py'),'--root',str(root),'--before',B,'--after',rev],0)
        record('prior-C1',python+[str(root/'.ufo/waves/round-21/battery.py'),'--root',str(root),'--rev',rev,'--claim','C1'],0)
        record('prior-C2',python+[str(root/'.ufo/waves/round-21/battery.py'),'--root',str(root),'--rev',rev,'--claim','C2','--regression'],0)
        record('sources-census',['/home/vgpnk/Projects/shokunin/scripts/sources-census.sh','validate','--root','/home/vgpnk/Projects/shokunin','kaidoku'],0)
        # Full-row preservation and counts; only new rows are permitted by this round.
        def rows(revision):
            return [line for line in git('show',revision+':corpus/SOURCES.md').decode().splitlines() if line.startswith('| S')]
        old,new=rows(B),rows(rev)
        census={'before':len(old),'after':len(new),'old_rows_identical':all(row in new for row in old),
                'tiers_before':{},'tiers_after':{},'status_before':{},'status_after':{}}
        for label,lines in [('before',old),('after',new)]:
            for line in lines:
                cells=[v.strip() for v in line.split('|')]
                for key,index in [('tiers',4),('status',8)]:
                    hist=census[key+'_'+label];hist[cells[index]]=hist.get(cells[index],0)+1
        (out/'source-rows.json').write_text(json.dumps(census,indent=2)+'\n')
        checks.append({'name':'source-row-preservation','pass':census['old_rows_identical']})
        checks.append({'name':'unchanged-measurement-dependencies','pass':all(dep_same.values())})
        # Causal separation: only each claim's finite data diff applied to B.
        allpaths=git('ls-tree','-r','--name-only',rev).decode().splitlines()
        c1paths=[p for p in allpaths if p.startswith(W+'/evidence/c1/') or p.startswith('corpus/knowledge/2026-10-21-r22-')]+['corpus/SOURCES.md']
        c2paths=[p for p in allpaths if p.startswith(W+'/evidence/c2/')]+['PROVINCE.md']
        matrix={}
        for name,paths in [('C1-only',c1paths),('C2-only',c2paths)]:
            sandbox=tools/name
            subprocess.run(['git','clone','--shared','--quiet',str(root),str(sandbox)],capture_output=True,check=True)
            git('checkout','--detach',B,where=sandbox)
            for path in paths:
                target=sandbox/path;target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(git('show',rev+':'+path))
            git('add','--all',where=sandbox)
            git('-c','user.name=fixture','-c','user.email=fixture@invalid.local','commit','-qm',name,where=sandbox)
            tip=git('rev-parse','HEAD',where=sandbox).decode().strip()
            matrix[name]={}
            for claim in ['c1','c2']:
                proc=subprocess.run(python+[str(tools/('count-'+claim+'.py')),'--root',str(sandbox),'--rev',tip],capture_output=True,text=True)
                data=json.loads(proc.stdout)
                count=data.get('t1_exercised_count',data.get('accounted_count'))
                matrix[name][claim]={'argv':proc.args,'exit':proc.returncode,'count':count,'stdout':proc.stdout,'stderr':proc.stderr}
        separation=matrix['C1-only']['c1']['count']>=1 and matrix['C1-only']['c2']['count']==0 and matrix['C2-only']['c1']['count']==0 and matrix['C2-only']['c2']['count']==14
        (out/'separability.json').write_text(json.dumps({'source_rev':rev,'matrix':matrix,'pass':separation},indent=2)+'\n')
        checks.append({'name':'separability','pass':separation})
    summary={'source_rev':rev,'baseline':B,'producer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             'counter_source_sha256':sources,'dependency_equal_B_REV_worktree':dep_same,'checks':checks,
             'passed':sum(row['pass'] for row in checks),'total':len(checks),'pass':all(row['pass'] for row in checks)}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,sort_keys=True))
    return 0 if summary['pass'] else 1


if __name__=='__main__':
    raise SystemExit(main())
