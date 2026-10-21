#!/usr/bin/env python3
"""Run the R21 final suite once over named source revisions; retain raw results.

Only lane-owned Python metadata validators, immutable Git reads and the fleet
source-census CLI execute. No REA producers or analyzed native carriers run.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',required=True)
    ap.add_argument('--before',required=True)
    ap.add_argument('--after',required=True)
    args=ap.parse_args()
    root=Path(args.root).resolve()
    wave=root/'.ufo/waves/round-21'
    out=wave/'verify'
    out.mkdir(exist_ok=True)
    records=[]
    def run(name,argv,expected):
        proc=subprocess.run(argv,capture_output=True,text=True,check=False,timeout=300,cwd=root)
        record={'id':name,'argv':argv,'measured_revision':args.before if name.startswith('before-') else args.after,'exit':proc.returncode,'expected_exit':expected,'stdout':proc.stdout,'stderr':proc.stderr,'pass':proc.returncode==expected}
        records.append(record)
        (out/(name+'.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
        print(name,proc.returncode,'expected',expected,flush=True)
        return record
    py=[sys.executable,'-I','-B']
    for claim in ['C1','C2']:
        base=py+[str(wave/'battery.py'),'--root',str(root),'--rev',args.before,'--claim',claim]
        run('before-'+claim,base,1)
        after=py+[str(wave/'battery.py'),'--root',str(root),'--rev',args.after,'--claim',claim]
        if claim=='C2':
            after+=['--regression']
        run('after-'+claim,after,0)
    for name in ['verb-coverage','compare-first-failure']:
        run('selftest-'+name,py+[str(wave/'tools'/(name+'.py')),'--selftest'],0)
    run('selftest-controls',py+[str(wave/'controls.py'),'--selftest'],0)
    run('selftest-isolated-control',py+[str(wave/'tools/isolated-control.py'),'--root',str(root),'--selftest'],0)
    run('no-harm',py+[str(wave/'controls.py'),'--root',str(root),'--before',args.before,'--after',args.after],0)
    run('verb-coverage',py+[str(wave/'tools/verb-coverage.py'),'--root',str(root),'--rev',args.after],0)
    with tempfile.TemporaryDirectory(prefix='kaidoku-r21-verify-') as directory:
        scratch=Path(directory)
        # No C3 run or prediction exists in this root. Only validator/pins.
        for path in ['.ufo/waves/round-17/tools/receipt-validate-v2.py','.ufo/waves/round-17/tools/pins.py']:
            target=scratch/path
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(subprocess.check_output(['git','--no-optional-locks','-C',str(root),'show',args.after+':'+path]))
        run('isolated-without-C3',py+[str(wave/'tools/isolated-control.py'),'--root',str(scratch)],0)
        # Red mutation of frozen local input; frozen Git authority unchanged.
        copy=scratch/'red'
        (copy/'fixtures').mkdir(parents=True)
        for relative in ['battery.py','fixture-contract.json','fixtures/battery.json','fixtures/expected.json']:
            shutil.copyfile(wave/relative,copy/relative)
        (copy/'fixtures/battery.json').write_text('{}\n',encoding='utf-8')
        red=run('frozen-input-red',py+[str(copy/'battery.py'),'--root',str(root),'--rev',args.after,'--claim','C1'],2)
        red['pass']=red['pass'] and 'snapshot_tampered' in red['stdout']
        (out/'frozen-input-red.json').write_text(json.dumps(red,indent=2)+'\n',encoding='utf-8')
    run('sources-census',['/home/vgpnk/Projects/shokunin/scripts/sources-census.sh','validate','--root','/home/vgpnk/Projects/shokunin','kaidoku'],0)
    summary={'before':args.before,'after':args.after,'producer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'checks':len(records),'passed':sum(r['pass'] for r in records),'failed':[r['id'] for r in records if not r['pass']],'records':[r['id'] for r in records]}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,sort_keys=True))
    return 0 if not summary['failed'] else 1


if __name__=='__main__':
    raise SystemExit(main())
