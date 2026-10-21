#!/usr/bin/env python3
"""C1-owned inert positive/decoy receipt control, with no C3 run dependency.

The fixture argv is recorded text, never executed. The old aggregate R20
checker remains historical; this is the current C1 authority for R20-SEP.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def evaluate(root):
    validator=Path(root)/'.ufo/waves/round-17/tools/receipt-validate-v2.py'
    spec=importlib.util.spec_from_file_location('isolated_receipt_validator',validator)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    pins=module.load_pins()
    with tempfile.TemporaryDirectory(prefix='kaidoku-r21-control-') as directory:
        work=Path(directory)
        carrier=work/'inert.txt'
        carrier.write_text('pinned inert fixture, not an executable\n',encoding='utf-8')
        session='/tmp/rea-ghidra-selftest'
        digest=hashlib.sha256(carrier.read_bytes()).hexdigest()
        md5=hashlib.md5(carrier.read_bytes()).hexdigest()
        log=work/'ghidra.log'
        log.write_text(f'2026-10-20 10:00:00 INFO  (LoggingInitialization) Using log file: {session}/ghidra.log\n2026-10-20 10:00:01 INFO  (HeadlessAnalyzer) IMPORTING: file://{session}/target-{digest[:12]}.bin\nLoading file://{session}/target-{digest[:12]}.bin?MD5={md5}...\n',encoding='utf-8')
        data=module._carrier_receipt(work,pins,carrier,log)
        mid=pins.snapshot([str(carrier)])
        mid_path=work/'mid.json'
        mid_path.write_text(json.dumps(mid),encoding='utf-8')
        step=dict(data['steps']['inspect-go-binary'])
        step['argv']=['npx','-y','rea-agents@6.5.0','analyze',str(carrier),'--format','json']
        step['pin_checks']=[{'taken_at_utc':mid['taken_at_utc'],'equal':True,'changed':[],'missing':[],'entries':len(mid['entries']),'map_path':str(mid_path),'map_sha256':hashlib.sha256(mid_path.read_bytes()).hexdigest()}]
        data['steps']=[step]
        positive=work/'positive.json'
        positive.write_text(json.dumps(data),encoding='utf-8')
        decoy=copy.deepcopy(data)
        decoy['steps'][0]['argv']=['npx','-y','rea-agents@6.5.0','inspect-go-binary','rea-agents@6.5.0','analyze']
        negative=work/'decoy.json'
        negative.write_text(json.dumps(decoy),encoding='utf-8')
        rows=[]
        for name,path,expected in [('independent_positive',positive,0),('independent_decoy',negative,1)]:
            argv=[sys.executable,'-I','-B',str(validator),'--require-mid-maps',str(path)]
            process=subprocess.run(argv,capture_output=True,text=True,check=False,timeout=120)
            payload=json.loads(process.stdout)
            finding_ok=expected==0 or 'analyze_step_unauthenticated' in process.stdout
            rows.append({'id':name,'expected_exit':expected,'observed_exit':process.returncode,'finding_ok':finding_ok,'pass':process.returncode==expected and finding_ok,'argv':argv,'stdout':payload,'stderr':process.stderr})
        ok=all(row['pass'] for row in rows)
        return {'finding':'isolated_control_clean' if ok else 'isolated_control_failed','cases':rows,'authority_sha256':hashlib.sha256(validator.read_bytes()).hexdigest(),'limit':'synthetic recorded receipt metadata only; never executes fixture argv; no C3 forecast/run file read'},0 if ok else 1


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',required=True)
    parser.add_argument('--selftest',action='store_true')
    args=parser.parse_args()
    if args.selftest:
        process=subprocess.run([sys.executable,'-I','-B',__file__,'--root',args.root],capture_output=True,text=True,check=False)
        payload=json.loads(process.stdout)
        ok=process.returncode==0 and payload.get('finding')=='isolated_control_clean'
        print(json.dumps({'finding':'selftest_clean' if ok else 'selftest_failed','exit':process.returncode,'result':payload},sort_keys=True))
        return 0 if ok else 1
    try:
        result,code=evaluate(args.root)
    except (OSError,ValueError,subprocess.SubprocessError) as error:
        result,code={'finding':'isolated_control_unevaluable','error':str(error)},2
    print(json.dumps(result,sort_keys=True))
    return code


if __name__=='__main__':
    raise SystemExit(main())
