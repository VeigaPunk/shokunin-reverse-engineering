#!/usr/bin/env python3
"""Independent frozen C1/C2 cases; baseline fallback when successor absent.

Run only owned validators/extractors on inert fixtures or retained logs. Git
writes happen in a removed external fixture repository, never the lane. A
caller-specified revision is trusted source code, not an untrusted artifact.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
PREFIX='.ufo/waves/round-21/'
BASE='.ufo/waves/round-20/tools/'
FIXTURE_REV='d93c85887d9ae77d224c82c8f56bc8cca86d1a75'
CONTRACT_REV='53166ab0aae495c964d956050ca0ca3a4f29014a'


def git(root,*args):
    return subprocess.check_output(['git','--no-optional-locks','-C',str(root),*args],stderr=subprocess.PIPE)


def materialize(root,rev,path,target):
    data=git(root,'show',rev+':'+path)
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(data)
    return hashlib.sha256(data).hexdigest()


def run(argv):
    try:
        p=subprocess.run(argv,capture_output=True,text=True,check=False,timeout=120)
        return {'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
    except (OSError,subprocess.SubprocessError) as error:
        return {'exit':None,'stdout':'','stderr':str(error)}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',required=True)
    ap.add_argument('--rev',required=True)
    ap.add_argument('--claim',choices=['C1','C2','all'],default='all')
    ap.add_argument('--regression',action='store_true')
    args=ap.parse_args()
    root=Path(args.root).resolve()
    if args.claim == 'C1' and args.regression:
        ap.error('--regression belongs to C2, not C1')
    try:
        rev=git(root,'rev-parse','--verify','--end-of-options',args.rev+'^{commit}').decode().strip()
        paths=set(git(root,'ls-tree','-r','--name-only',rev).decode().splitlines())
        frozen={'fixture-contract.json':git(root,'show',CONTRACT_REV+':'+PREFIX+'fixture-contract.json'),
                'fixtures/battery.json':git(root,'show',FIXTURE_REV+':'+PREFIX+'fixtures/battery.json')}
        fixture_bytes=frozen['fixtures/battery.json']
        fixtures=json.loads(fixture_bytes)
        out={'revision':rev,'fixture_revision':FIXTURE_REV,'contract_revision':CONTRACT_REV,'fixtures_sha256':hashlib.sha256(fixture_bytes).hexdigest(),'claims':{},'regression':[]}
        expected=json.loads((HERE/'fixtures/expected.json').read_text(encoding='utf-8'))
        if set(expected['sha256'])!=set(frozen):
            raise ValueError('snapshot_manifest_population')
        for name,data in frozen.items():
            digest=expected['sha256'][name]
            if hashlib.sha256(data).hexdigest()!=digest or hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=digest:
                print(json.dumps({'finding':'snapshot_tampered','path':name}))
                return 2
        with tempfile.TemporaryDirectory(prefix='kaidoku-r21-battery-') as directory:
            scratch=Path(directory)
            for claim in ['C1','C2']:
                if args.claim not in (claim,'all'):
                    continue
                name='verb-coverage.py' if claim=='C1' else 'compare-first-failure.py'
                successor=PREFIX+'tools/'+name in paths
                selected=(PREFIX+'tools/' if successor else BASE)+name
                tool=scratch/claim/name
                digest=materialize(root,rev,selected,tool)
                rows=[]
                if claim=='C1' and not successor:
                    fixture_repo=scratch/'fixture-repo'
                    fixture_repo.mkdir()
                    subprocess.run(['git','init','-q',str(fixture_repo)],check=True)
                    for case in fixtures[claim]:
                        path=fixture_repo/'.ufo/waves/round-20/evidence/c2'/case['id']/'evidence.json'
                        path.parent.mkdir(parents=True,exist_ok=True)
                        path.write_text(case['evidence'],encoding='utf-8')
                    subprocess.run(['git','-C',str(fixture_repo),'add','.ufo'],check=True)
                    subprocess.run(['git','-C',str(fixture_repo),'-c','user.name=kaidoku-fixture','-c','user.email=kaidoku-fixture@invalid','commit','-q','-m','frozen inert cases'],check=True)
                    fixture_rev=git(fixture_repo,'rev-parse','HEAD').decode().strip()
                    driver=scratch/'baseline-driver.py'
                    driver.write_text("import importlib.util,json,sys\np,root,rev,verb,ev,path=sys.argv[1:]\ns=importlib.util.spec_from_file_location('baseline',p)\nm=importlib.util.module_from_spec(s);s.loader.exec_module(m)\nentry=verb+' '+ev+' '+path\nfound=m.bound_evidence(root,rev,verb,[entry],[path])\nprint(json.dumps({'finding':'legacy_bound' if found else 'legacy_unbound','bound':bool(found)}))\nraise SystemExit(0 if found else 1)\n",encoding='utf-8')
                for case in fixtures[claim]:
                    if claim=='C1':
                        path=scratch/'evidence.json'
                        path.write_text(case['evidence'],encoding='utf-8')
                        if successor:
                            argv=[sys.executable,'-I','-B',str(tool),'--evidence',str(path),'--verb',case['verb'],'--evidence-id',case['evidence_id']]
                        else:
                            rel='.ufo/waves/round-20/evidence/c2/'+case['id']+'/evidence.json'
                            argv=[sys.executable,'-I','-B',str(driver),str(tool),str(fixture_repo),fixture_rev,case['verb'],case['evidence_id'],rel]
                    else:
                        prediction=scratch/'prediction.json'
                        prediction.write_text(json.dumps(case['prediction']),encoding='utf-8')
                        log=scratch/'log.txt'
                        log.write_text('inert extractor input\n',encoding='utf-8')
                        extractor=scratch/'extractor.py'
                        extractor.write_text('import sys\nsys.stdout.write('+repr(case['stdout'])+')\nraise SystemExit('+str(case['extractor_exit'])+')\n',encoding='utf-8')
                        argv=[sys.executable,'-I','-B',str(tool),'--prediction',str(prediction),'--log',str(log),'--extractor',str(extractor)]
                    result=run(argv)
                    expected=case['expected_exit']
                    try:
                        finding=json.loads(result['stdout']).get('finding')
                    except (ValueError,AttributeError):
                        finding=None
                    rows.append({'id':case['id'],'expected_exit':expected,'observed_exit':result['exit'],'pass':result['exit']==expected,'finding':finding,'stdout':result['stdout'],'stderr':result['stderr']})
                out['claims'][claim]={'source_path':selected,'source_sha256':digest,'successor':successor,'total':len(rows),'passed':sum(r['pass'] for r in rows),'violations':sum(not r['pass'] for r in rows),'false_clean':sum(r['observed_exit']==0 and r['expected_exit']!=0 for r in rows),'undeclared_crashes':sum('Traceback' in r['stderr'] for r in rows),'cases':rows}
            if args.regression:
                comparator=scratch/'regression/compare-first-failure.py'
                comp_path=PREFIX+'tools/compare-first-failure.py' if PREFIX+'tools/compare-first-failure.py' in paths else BASE+'compare-first-failure.py'
                materialize(root,rev,comp_path,comparator)
                extractor=scratch/'regression/first-failure-extract.py'
                materialize(root,rev,BASE+'first-failure-extract.py',extractor)
                predictions=sorted(p for p in paths if p.startswith('.ufo/waves/round-20/predictions/swiss-misread-v2/') and p.endswith('.json'))
                if len(predictions)!=19:
                    raise ValueError('regression_population_not_nineteen')
                for p in predictions:
                    label=Path(p).stem
                    binding_path='.ufo/waves/round-20/runs/'+label+'/comparison-log-binding.json'
                    binding=json.loads(git(root,'show',rev+':'+binding_path))
                    log_rel=str(Path(binding['log_path']).relative_to(root))
                    pred_file=scratch/'regression'/Path(p).name
                    log_file=scratch/'regression'/(label+'.log')
                    materialize(root,rev,p,pred_file)
                    log_digest=materialize(root,rev,log_rel,log_file)
                    result=run([sys.executable,'-I','-B',str(comparator),'--prediction',str(pred_file),'--log',str(log_file),'--extractor',str(extractor)])
                    out['regression'].append({'label':label,'log_sha_equal':log_digest==binding['log_sha256'],**result})
        ok=all(c['violations']==0 for c in out['claims'].values()) and all(r['exit']==0 and r['log_sha_equal'] for r in out['regression'])
        out['finding']='battery_clean' if ok else 'battery_failed'
        print(json.dumps(out,sort_keys=True))
        return 0 if ok else 1
    except (OSError,ValueError,KeyError,subprocess.SubprocessError) as error:
        print(json.dumps({'finding':'battery_unevaluable','error':str(error)}))
        return 2


if __name__=='__main__':
    raise SystemExit(main())
