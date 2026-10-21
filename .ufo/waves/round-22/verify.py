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
import os

B = '7787fea4d6fd718726de92ed20759d11ce7b8b48'
W = '.ufo/waves/round-22'


def main():
    for key in tuple(os.environ):
        if key.startswith("GIT_"):
            del os.environ[key]
    os.environ["GIT_NO_REPLACE_OBJECTS"]="1"
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
        if len(argv)>3 and argv[1:3]==['-I','-B'] and Path(argv[3]).is_file():
            row['script_sha256']=hashlib.sha256(Path(argv[3]).read_bytes()).hexdigest()
        if '--counter' in argv:
            candidate=Path(argv[argv.index('--counter')+1])
            row['counter_sha256']=hashlib.sha256(candidate.read_bytes()).hexdigest()
        (out/(name+'.json')).write_text(json.dumps(row,indent=2)+'\n')
        checks.append({'name':name,'pass':row['pass'],'exit':proc.returncode})
        return data
    python=[sys.executable,'-I','-B']
    sources={}
    with tempfile.TemporaryDirectory(prefix='kaidoku-r22-pinned-tools-') as directory:
        tools=Path(directory)
        # Execute the requested revision's source, not uncommitted current tools.
        for path in [W+'/tools/count-c1.py',W+'/tools/count-c2.py',W+'/tools/counter-fixtures.py',
                     W+'/frozen/count-c1.py',W+'/frozen/count-c2.py',W+'/frozen/count-c1-pre-envelope.py',
                     W+'/frozen/counter-fixtures-v1.py',W+'/frozen/helper-hashes.json',W+'/frozen/expected-v2.json']:
            content=git('show',rev+':'+path)
            dest=tools/('frozen' if '/frozen/' in path else '')/Path(path).name
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(content)
            sources[path]=hashlib.sha256(content).hexdigest()
        # Source dependencies remain byte-identical to B; counters read Git data at rev.
        dependencies=['.ufo/waves/round-20/tools/verb-coverage.py','.ufo/waves/round-21/tools/verb-coverage.py']
        dep_same={path:git('show',B+':'+path)==git('show',rev+':'+path)==(root/path).read_bytes() for path in dependencies}
        baseline_data={}
        for claim in ['c1','c2']:
            counter=str(tools/('count-'+claim+'.py'))
            baseline_data[claim]=record('before-'+claim,python+[counter,'--root',str(root),'--rev',B],1,
                   lambda data: data is not None and data.get('t1_exercised_count',data.get('accounted_count'))==0)
            record('after-'+claim,python+[counter,'--root',str(root),'--rev',rev],1 if claim=='c1' else 0,
                   (lambda data:data is not None and data['t1_exercised_count']>=1) if claim=='c1' else
                   (lambda data:data is not None and data['accounted_count']==14 and not data['mismatched'] and not data['foreign_rows']))
            control_root=tools/('control-'+claim)
            manifest_bytes=git('show',rev+':'+W+'/frozen/expected-v2.json')
            manifest=json.loads(manifest_bytes)
            for path in [*manifest['inputs'],W+'/frozen/expected-v2.json']:
                target=control_root/path
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(git('show',rev+':'+path))
            control_argv=python+[counter,'--selftest','--root',str(control_root)]
            record('controls-'+claim,control_argv,0,lambda data:data is not None and data.get('finding')=='counter_controls_clean')
            fixture=control_root/W/'tools/counter-fixtures.py'
            fixture.write_bytes(fixture.read_bytes()+b'\n# mutated snapshot input\n')
            record('frozen-input-red-'+claim,control_argv,2,lambda data:data is not None and data.get('finding')=='snapshot_tampered')
            record('red-'+claim,python+[str(tools/'frozen/counter-fixtures-v1.py'),'--claim',claim.upper(),'--counter',str(tools/'frozen'/('count-'+claim+'.py')),'--root',str(root)],1,
                   lambda data:data is not None and data['cases'][0]['pass'] and
                   any(case['id']==('missing_source' if claim=='c1' else 'probe_alias') and not case['pass'] and case['count']==(6 if claim=='c1' else 14) for case in data['cases']))
            record('original-after-'+claim,python+[str(tools/'frozen'/('count-'+claim+'.py')),'--root',str(root),'--rev',rev],1 if claim=='c1' else 0,
                   (lambda data:data is not None and data['t1_exercised_count']>=1) if claim=='c1' else
                   (lambda data:data is not None and data['accounted_count']==14))
            record('selftest-'+claim,python+[str(root/W/'tools'/('count-'+claim+'.py')),'--selftest'],0)
        record('source-link-stage-green',python+[str(tools/'frozen/counter-fixtures-v1.py'),'--claim','C1','--counter',str(tools/'frozen/count-c1-pre-envelope.py'),'--root',str(root)],0)
        # A genuine retained positive and the same data with only parent refusal changed.
        input_base='2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67'
        sandbox=tools/'envelope-regression'
        subprocess.run(['git','clone','--shared','--no-checkout','--quiet',str(root),str(sandbox)],capture_output=True,check=True)
        git('update-ref','--no-deref','HEAD',input_base,where=sandbox)
        git('read-tree',input_base,where=sandbox)
        for path in dependencies:
            target=sandbox/path;target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(git('show',input_base+':'+path))
        parent_path=W+'/evidence/c1/identify-godot.envelope.json'
        envelope_matrix={}
        for phase in ['positive','refused']:
            tip=input_base
            if phase=='refused':
                parent=json.loads(git('show',input_base+':'+parent_path))
                parent['ok']=False
                parent['error']={'code':'capability_unavailable'}
                mutated=(json.dumps(parent,indent=2)+'\n').encode()
                (out/'envelope-refused-input.json').write_bytes(mutated)
                target=sandbox/parent_path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(mutated)
                git('add','--',parent_path,where=sandbox)
                git('-c','user.name=fixture','-c','user.email=fixture@invalid.local','commit','-qm','parent refusal only',where=sandbox)
                tip=git('rev-parse','HEAD',where=sandbox).decode().strip()
            envelope_matrix[phase]={}
            for version,candidate in [('before',tools/'frozen/count-c1-pre-envelope.py'),('after',tools/'count-c1.py')]:
                wanted=0 if phase=='refused' and version=='after' else 1
                data=record('envelope-'+phase+'-'+version,python+[str(candidate),'--root',str(sandbox),'--rev',tip],1,
                            lambda data:data is not None and data['t1_exercised_count']==wanted and
                            data['targets']['identify-flutter-build']['exercised']==bool(wanted))
                envelope_matrix[phase][version]=data
        (out/'envelope-regression.json').write_text(json.dumps({'input_base':input_base,
                    'changed_data_path':parent_path,'matrix':envelope_matrix,
                    'limit':'private regenerated fixture, not a real REA refusal observation'},indent=2)+'\n')
        record('prior-controls',python+[str(root/'.ufo/waves/round-21/controls.py'),'--root',str(root),'--before',B,'--after',rev],0,
               lambda data:data is not None and not data['mapping_after']['dangling'])
        record('prior-C1',python+[str(root/'.ufo/waves/round-21/battery.py'),'--root',str(root),'--rev',rev,'--claim','C1'],0)
        record('prior-C2',python+[str(root/'.ufo/waves/round-21/battery.py'),'--root',str(root),'--rev',rev,'--claim','C2','--regression'],0)
        record('evidence-timestamps',python+[str(root/'.ufo/waves/round-20/tools/evidence-timestamps.py'),'--root',str(root),'--rev',rev,'--path',W,'--strict'],0)
        record('sources-census',['/home/vgpnk/Projects/shokunin/scripts/sources-census.sh','validate','--root','/home/vgpnk/Projects/shokunin','kaidoku'],0)
        # Full-row preservation and counts; only new rows are permitted by this round.
        def rows(revision):
            return [line for line in git('show',revision+':corpus/SOURCES.md').decode().splitlines() if line.startswith('| S')]
        old,new=rows(B),rows(rev)
        census={'before':len(old),'after':len(new),'old_rows_identical':new[:len(old)]==old,
                'tiers_before':{},'tiers_after':{},'status_before':{},'status_after':{}}
        for label,lines in [('before',old),('after',new)]:
            for line in lines:
                cells=[v.strip() for v in line.split('|')]
                for key,index in [('tiers',4),('status',8)]:
                    hist=census[key+'_'+label];hist[cells[index]]=hist.get(cells[index],0)+1
        (out/'source-rows.json').write_text(json.dumps(census,indent=2)+'\n')
        checks.append({'name':'source-row-preservation','pass':census['old_rows_identical']})
        checks.append({'name':'unchanged-measurement-dependencies','pass':all(dep_same.values())})
        source_same={path:hashlib.sha256((root/path).read_bytes()).hexdigest()==digest for path,digest in sources.items()}
        checks.append({'name':'selftest-source-equal-revision-at-check','pass':all(source_same.values())})
        # Causal separation: only each claim's finite data diff applied to B.
        allpaths=git('ls-tree','-r','--name-only',rev).decode().splitlines()
        pairs=[]
        for path in allpaths:
            if path.startswith(W+'/evidence/') and path.endswith('.run.json'):
                pairs.append((path,path[:-9]+('.envelope.json' if '/c1/' in path else '.json')))
        pairs.append((W+'/evidence/c1/identify-godot-run.json',W+'/evidence/c1/identify-godot.envelope.json'))
        provenance=[]
        for run_path,envelope_path in pairs:
            try:
                run=json.loads(git('show',rev+':'+run_path))
                raw=git('show',rev+':'+envelope_path).decode()
                envelope=json.loads(raw)
                argv=run['argv']
                pin=argv.index('rea-agents@6.5.0')
                verb=argv[pin+1]
                match=(run['stdout']==raw and envelope['meta']['command']==verb
                       and run['exit']==(0 if envelope['ok'] is True else 1))
                adb_control=('adb' not in verb or run.get('env_overrides',{}).get('REA_ADB_PATH')=='/usr/bin/false')
                provenance.append({'run':run_path,'envelope':envelope_path,'stdout_equal':run['stdout']==raw,
                                   'verb':verb,'env_overrides_retained':'env_overrides' in run,
                                   'explicit_adb_control_valid':adb_control,'pass':match and adb_control})
            except (ValueError,KeyError,UnicodeError,subprocess.CalledProcessError) as error:
                provenance.append({'run':run_path,'envelope':envelope_path,'error':str(error),'pass':False})
        negative_copy=json.loads(git('show',rev+':'+W+'/evidence/c1/identify-godot.evidence.json'))
        negative_envelope=json.loads(git('show',rev+':'+W+'/evidence/c1/identify-godot.envelope.json'))
        copy_equal=negative_copy==negative_envelope['data']
        (out/'provenance.json').write_text(json.dumps({'source_rev':rev,'pairs':provenance,'historical_copy_equal_data':copy_equal,
                     'limit':'local byte/argv/exit/control consistency, not authentication'},indent=2)+'\n')
        checks.append({'name':'producer-envelope-provenance','pass':copy_equal and all(row['pass'] for row in provenance)})
        c1paths=[p for p in allpaths if p.startswith(W+'/evidence/c1/') or p.startswith(W+'/evidence/sources/') or p.startswith('corpus/knowledge/2026-10-21-r22-')]+['corpus/SOURCES.md','corpus/README.md','PROVINCE.md']
        c2paths=[p for p in allpaths if p.startswith(W+'/evidence/c2/')]+['PROVINCE.md']
        base_province=git('show',B+':PROVINCE.md').decode()
        final_province=git('show',rev+':PROVINCE.md').decode()
        dispositions=final_province.split('### Round-22 catalog dispositions',1)[1].split('### Round-22 narrowly added static ground',1)[0]
        static=final_province.split('### Round-22 narrowly added static ground',1)[1]
        partition_exact=base_province+'\n### Round-22 catalog dispositions'+dispositions+'### Round-22 narrowly added static ground'+static==final_province
        checks.append({'name':'province-section-partition-exact','pass':partition_exact})
        matrix={}
        for name,paths in [('C1-only',c1paths),('C2-only',c2paths)]:
            sandbox=tools/name
            subprocess.run(['git','clone','--shared','--no-checkout','--quiet',str(root),str(sandbox)],capture_output=True,check=True)
            # Keep B's complete index/tree without materializing unrelated old evidence.
            git('update-ref','--no-deref','HEAD',B,where=sandbox)
            git('read-tree',B,where=sandbox)
            for path in paths:
                target=sandbox/path;target.parent.mkdir(parents=True,exist_ok=True)
                if path=='PROVINCE.md':
                    section=('### Round-22 narrowly added static ground'+static) if name=='C1-only' else ('### Round-22 catalog dispositions'+dispositions)
                    target.write_text(base_province+'\n'+section)
                else:
                    target.write_bytes(git('show',rev+':'+path))
            git('add','--',*paths,where=sandbox)
            git('-c','user.name=fixture','-c','user.email=fixture@invalid.local','commit','-qm',name,where=sandbox)
            tip=git('rev-parse','HEAD',where=sandbox).decode().strip()
            matrix[name]={}
            for claim in ['c1','c2']:
                proc=subprocess.run(python+[str(tools/('count-'+claim+'.py')),'--root',str(sandbox),'--rev',tip],capture_output=True,text=True)
                data=json.loads(proc.stdout)
                count=data.get('t1_exercised_count',data.get('accounted_count'))
                matrix[name][claim]={'argv':proc.args,'exit':proc.returncode,'count':count,'stdout':proc.stdout,'stderr':proc.stderr}
                without_rev=lambda value:{key:item for key,item in value.items() if key!='rev'}
                matrix[name][claim]['equals_baseline_output']=isinstance(data,dict) and isinstance(baseline_data[claim],dict) and without_rev(data)==without_rev(baseline_data[claim])
        separation=(matrix['C1-only']['c1']['count']>=1 and matrix['C1-only']['c2']['equals_baseline_output']
                    and matrix['C2-only']['c1']['equals_baseline_output'] and matrix['C2-only']['c2']['count']==14
                    and matrix['C1-only']['c2']['exit']==1 and matrix['C2-only']['c1']['exit']==1
                    and matrix['C2-only']['c2']['exit']==0
                    and matrix['C1-only']['c1']['exit']==(0 if matrix['C1-only']['c1']['count']==6 else 1))
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
