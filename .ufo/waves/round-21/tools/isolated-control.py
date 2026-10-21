#!/usr/bin/env python3
"""C1-owned inert positive/decoy receipt control, with no C3 run dependency.

The fixture argv is recorded text, never executed. The old aggregate R20
checker remains historical; this is the current C1 authority for R20-SEP.
"""
import argparse
import copy
import hashlib
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time

TEMPLATE_SHA256='5346426d237cc56dc8cf7d25187206cab561b91e8b37bd402e85338d112da25c'
TEMPLATE_FREEZE='ae73ec7734c8edc70350995267ddc1f0d2f603e4'


def substitute(value, replacements):
    if isinstance(value, str):
        return replacements.get(value, value)
    if isinstance(value, list):
        return [substitute(item, replacements) for item in value]
    if isinstance(value, dict):
        return {key:substitute(item, replacements) for key,item in value.items()}
    return value


def snapshot(path):
    data=path.read_bytes()
    stat=path.stat()
    return {'taken_at_utc':datetime.now(timezone.utc).isoformat(),
            'monotonic_ns':time.monotonic_ns(),
            'entries':{str(path):{'sha256':hashlib.sha256(data).hexdigest(),
                                  'size':len(data),'mtime_ns':stat.st_mtime_ns}}}


def evaluate(root):
    validator=Path(root)/'.ufo/waves/round-17/tools/receipt-validate-v2.py'
    pins_path=validator.with_name('pins.py')
    template_path=Path(__file__).resolve().parents[1]/'fixtures/isolated-receipt-v2.json'
    template_bytes=template_path.read_bytes()
    if hashlib.sha256(template_bytes).hexdigest()!=TEMPLATE_SHA256:
        raise ValueError('snapshot_tampered: independent receipt template')
    template=json.loads(template_bytes)
    expected=template['expected']
    with tempfile.TemporaryDirectory(prefix='kaidoku-r21-control-') as directory:
        work=Path(directory)
        carrier=work/'inert.txt'
        carrier.write_text('pinned inert fixture, not an executable\n',encoding='utf-8')
        session='/tmp/rea-ghidra-r21-independent'
        digest=hashlib.sha256(carrier.read_bytes()).hexdigest()
        md5=hashlib.md5(carrier.read_bytes()).hexdigest()
        log=work/'ghidra.log'
        log.write_text(f'2026-10-20 10:00:00 INFO  (LoggingInitialization) Using log file: {session}/ghidra.log\n2026-10-20 10:00:01 INFO  (HeadlessAnalyzer) IMPORTING: file://{session}/target-{digest[:12]}.bin\nLoading file://{session}/target-{digest[:12]}.bin?MD5={md5}...\n',encoding='utf-8')
        data=substitute(template['receipt'],{'@carrier@':str(carrier),'@carrier_sha@':digest,
                         '@work@':str(work),'@log@':str(log),
                         '@log_sha@':hashlib.sha256(log.read_bytes()).hexdigest(),
                         '@instant@':datetime.now(timezone.utc).isoformat(),
                         '@python@':sys.version,'@orig_argv@':getattr(sys,'orig_argv',sys.argv)})
        pre,mid,post=snapshot(carrier),snapshot(carrier),snapshot(carrier)
        data['pins_pre'],data['pins_post']=pre,post
        data['pins_compare']={'equal':pre['entries']==post['entries'],'changed':[],
            'missing':[],'errors':[],'pre_taken_at_utc':pre['taken_at_utc'],
            'post_taken_at_utc':post['taken_at_utc']}
        data['retained_logs'][0]['files']['ghidra.log']['bytes']=log.stat().st_size
        mid_path=work/'mid.json'
        mid_path.write_text(json.dumps(mid),encoding='utf-8')
        data['steps'][0]['pin_checks']=[{'taken_at_utc':mid['taken_at_utc'],'equal':True,
            'changed':[],'missing':[],'entries':len(mid['entries']),'map_path':str(mid_path),
            'map_sha256':hashlib.sha256(mid_path.read_bytes()).hexdigest()}]
        positive=work/'positive.json'
        positive.write_text(json.dumps(data),encoding='utf-8')
        decoy=copy.deepcopy(data)
        decoy['steps'][0]['argv']=template['decoy_argv']
        negative=work/'decoy.json'
        negative.write_text(json.dumps(decoy),encoding='utf-8')
        rows=[]
        for name,path,wanted in [('independent_positive',positive,expected['positive_exit']),
                                 ('independent_decoy',negative,expected['decoy_exit'])]:
            argv=[sys.executable,'-I','-B',str(validator),'--require-mid-maps',str(path)]
            process=subprocess.run(argv,capture_output=True,text=True,check=False,timeout=120)
            payload=json.loads(process.stdout)
            finding_ok=wanted==0 or expected['decoy_finding'] in process.stdout
            rows.append({'id':name,'expected_exit':wanted,'observed_exit':process.returncode,
                'finding_ok':finding_ok,'pass':process.returncode==wanted and finding_ok,
                'argv':argv,'stdout':payload,'stderr':process.stderr})
        ok=all(row['pass'] for row in rows)
        return {'finding':'isolated_control_clean' if ok else 'isolated_control_failed',
            'cases':rows,'authority_sha256':hashlib.sha256(validator.read_bytes()).hexdigest(),
            'pins_sha256':hashlib.sha256(pins_path.read_bytes()).hexdigest(),
            'fixture_sha256':TEMPLATE_SHA256,'fixture_freeze':TEMPLATE_FREEZE,
            'limit':'independently frozen synthetic receipt template; no validator fixture builder/import; never executes fixture argv or reads C3 inputs'},0 if ok else 1


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
