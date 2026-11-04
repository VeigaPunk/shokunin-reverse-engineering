#!/usr/bin/env python3
"""Run frozen R81 counter on two intentionally invalid detector controls."""
import argparse, hashlib, importlib.util, json, os, pathlib, shutil, subprocess
p=argparse.ArgumentParser(); p.add_argument('--work', required=True); p.add_argument('--out', required=True); a=p.parse_args()
s=pathlib.Path(a.work).resolve(); out=pathlib.Path(a.out).resolve(); out.mkdir(parents=True,exist_ok=True)
lane=pathlib.Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
counter=lane/'tools/round-81/record-integration.py'
spec=importlib.util.spec_from_file_location('counter',counter); c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
results={}
for label in ('mock','crash'):
    repo=s/('repo-'+label); (repo/'tools/round-81').mkdir(parents=True,exist_ok=True); (repo/'tools/round-80').mkdir(parents=True,exist_ok=True)
    target=repo/'tools/round-81/strictness-battery.py'; source=(s/(label+'-impostor.py')).read_bytes(); target.write_bytes(source)
    (repo/'tools/round-80/pointer-bind.py').write_bytes((s/'pointer-bind.py').read_bytes())
    def git(*args): return subprocess.check_output(['git','-C',str(repo),*args],text=True).strip()
    git('init','-q'); top=git('rev-parse','--show-toplevel'); assert top==str(repo)
    git('add','tools'); git('-c','user.name=fixture','-c','user.email=fixture@invalid','commit','-q','-m',label+' detector control')
    rev=git('rev-parse','HEAD'); env=os.environ.copy(); env['TMPDIR']=str(s/'tmp')
    run=subprocess.run(['python3','-I','-B',str(counter),'--root',str(repo),'--rev',rev,'--work',str(s/('work-'+label)),'--json-out',str(out/(label+'-control.json'))],env=env,capture_output=True,text=True)
    d=json.loads((out/(label+'-control.json')).read_text()); results[label]={'counter_exit':run.returncode,'toplevel':top,'pristine':{'exit':d['pristine']['exit'],'summary':d['pristine']['summary']},'mutant':{'exit':d['mutant']['exit'],'summary':d['mutant']['summary']},'killed':d['killed'],'survivors':d['survivors']}
    (out/(label+'-impostor.py')).write_bytes(source)
    # Same bounded detector on restored bytes, then confirm exact restoration.
    before=hashlib.sha256(source).hexdigest(); target.write_text(c.omit_commit(source.decode())); mutated=hashlib.sha256(target.read_bytes()).hexdigest()
    try: pass
    finally: target.write_bytes(source)
    restored=c.run(target,s/('work-'+label))
    results[label]['restoration']={'before_sha256':before,'mutant_sha256':mutated,'after_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'exit':restored['exit'],'summary':restored['summary']}
    (out/(label+'-restored.json')).write_text(json.dumps(restored,indent=1)+'\n')
(out/'controls-summary.json').write_text(json.dumps(results,indent=1)+'\n'); print(json.dumps(results,indent=1))
