#!/usr/bin/env python3
"""Independent outer-CLI ZIP inventory comparator. Exit0 all matched,1 mismatch,2 unevaluable.
Reads pinned recipe oracle and reader; never extracts. Private control files only in selftest.
"""
import argparse, hashlib, json, pathlib, subprocess, sys, resource, datetime, tempfile

def digest(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def limits():
    resource.setrlimit(resource.RLIMIT_AS,(268435456,268435456))
    resource.setrlimit(resource.RLIMIT_CPU,(8,8))
    resource.setrlimit(resource.RLIMIT_FSIZE,(16777216,16777216))
def compare(reader,root,rpin,epin):
    root=pathlib.Path(root); exp=root/'expected.json'
    if digest(reader)!=rpin or digest(exp)!=epin: return {'finding':'snapshot_tampered','exit':2}
    expected=json.loads(exp.read_text()); results=[]
    if not isinstance(expected,dict) or not expected: return {'finding':'empty_oracle','exit':2}
    for name,want in expected.items():
        if '/' in name or '\\' in name or name in ('.','..'): raise ValueError('unsafe fixture id')
        p=root/(name+'.zip')
        if digest(p)!=want['archive_sha256']: return {'finding':'snapshot_tampered','exit':2,'fixture':name}
        cmd=[sys.executable,'-I','-B',str(pathlib.Path(reader).resolve()),'--archive',str(p.resolve())]
        start=datetime.datetime.now(datetime.timezone.utc).isoformat()
        try:
            run=subprocess.run(cmd,capture_output=True,text=True,timeout=12,preexec_fn=limits)
            if len(run.stdout)+len(run.stderr)>1048576: raise ValueError('output cap')
            try: got=json.loads(run.stdout)
            except (ValueError,TypeError): got=None
            checks={'exit':run.returncode==want['exit'],'body':isinstance(got,dict)}
            if isinstance(got,dict):
                checks.update(schema=got.get('schema')==1 and type(got.get('exit')) is int,body_exit=got.get('exit')==want['exit'],finding=got.get('finding')==want['finding'],reader=got.get('reader_sha256')==rpin,python=isinstance(got.get('python'),str))
                if want['exit']==0:
                    for key in ('archive_sha256','archive_size','occurrences','duplicate_groups'): checks[key]=got.get(key)==want[key]
                else: checks['no_partial_inventory']='occurrences' not in got and 'duplicate_groups' not in got
            results.append(dict(case=name,argv=cmd,utc=start,exit=run.returncode,stdout=run.stdout,stderr=run.stderr,checks=checks,passed=all(checks.values())))
        except (subprocess.TimeoutExpired,ValueError) as e:
            results.append(dict(case=name,argv=cmd,utc=start,passed=False,error=str(e)))
    return dict(finding='all_matched' if all(r['passed'] for r in results) else 'mismatch',exit=0 if all(r['passed'] for r in results) else 1,reader_sha256=rpin,expected_sha256=epin,cases=len(results),matched=sum(r['passed'] for r in results),results=results)

def selftest():
    # Canned oracle tests comparator, not ZIP implementation; outer CLI actual invocation.
    with tempfile.TemporaryDirectory(prefix='kaidoku64-comparator-') as t:
        p=pathlib.Path(t); (p/'a.zip').write_bytes(b'owned comparator sentinel')
        want=dict(exit=0,finding='inventory_complete',archive_sha256=digest(p/'a.zip'),archive_size=(p/'a.zip').stat().st_size,occurrences=[],duplicate_groups=[])
        (p/'expected.json').write_text(json.dumps({'a':want})); ep=digest(p/'expected.json')
        rows=[]
        for mode in ('positive','noop','all_false','junk','wrong_digest','partial_error'):
            body=dict(want,schema=1,python='selftest')
            if mode=='all_false': body['occurrences']=[False]
            if mode=='wrong_digest': body['archive_sha256']='0'*64
            if mode=='partial_error': body.update(exit=1,finding='malformed_zip')
            code="import json,pathlib,hashlib\nx="+repr(body)+"\nx['reader_sha256']=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()\nprint(json.dumps(x))\n"
            if mode=='noop': code='pass\n'
            if mode=='junk': code="print('junk')\n"
            f=p/(mode+'.py'); f.write_text(code)
            cmd=[sys.executable,'-I','-B',str(pathlib.Path(__file__).resolve()),'--reader',str(f),'--fixtures',t,'--expect-reader-sha256',digest(f),'--expect-oracle-sha256',ep]
            r=subprocess.run(cmd,capture_output=True,text=True,timeout=20)
            out=json.loads(r.stdout); expected=0 if mode=='positive' else 1
            rows.append(dict(case=mode,exit=r.returncode,finding=out['finding'],passed=r.returncode==expected and out['finding']==('all_matched' if expected==0 else 'mismatch')))
        return dict(exit=0 if all(r['passed'] for r in rows) else 1,finding='selftest',cases=rows)

def main():
    a=argparse.ArgumentParser(); a.add_argument('--reader'); a.add_argument('--fixtures'); a.add_argument('--expect-reader-sha256'); a.add_argument('--expect-oracle-sha256'); a.add_argument('--out'); a.add_argument('--selftest',action='store_true'); v=a.parse_args()
    try:
        r=selftest() if v.selftest else compare(v.reader,v.fixtures,v.expect_reader_sha256,v.expect_oracle_sha256)
    except (OSError,ValueError,TypeError,KeyError) as e: r=dict(exit=2,finding='unevaluable',detail=str(e))
    data=json.dumps(r,indent=2,sort_keys=True)+'\n'
    if v.out: pathlib.Path(v.out).write_text(data)
    print(data,end=''); return r['exit']
if __name__=='__main__': sys.exit(main())
