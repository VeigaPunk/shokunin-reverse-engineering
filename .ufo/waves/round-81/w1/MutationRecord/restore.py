#!/usr/bin/env python3
import argparse, hashlib, importlib.util, json, os, pathlib, shutil
p=argparse.ArgumentParser(); p.add_argument('--work',required=True); p.add_argument('--out',required=True); a=p.parse_args(); s=pathlib.Path(a.work); out=pathlib.Path(a.out)
counter=pathlib.Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-81/record-integration.py')
spec=importlib.util.spec_from_file_location('counter',counter); c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
result={}
for label,source in [('candidate',s/'fixture-repo/tools/round-81/strictness-battery.py'),('base',s/'round80-battery-base.py')]:
    d=s/('restore-'+label); d.mkdir(exist_ok=True); target=d/'strictness-battery.py'; original=source.read_bytes(); target.write_bytes(original); (d/'pointer-bind.py').write_bytes((s/'pointer-bind.py').read_bytes())
    before=hashlib.sha256(original).hexdigest(); target.write_text(c.omit_commit(original.decode())); mutant=hashlib.sha256(target.read_bytes()).hexdigest()
    try: pass
    finally: target.write_bytes(original)
    restored=c.run(target,d); (out/(label+'-restored.json')).write_text(json.dumps(restored,indent=1)+'\n')
    result[label]={'before_sha256':before,'mutant_sha256':mutant,'after_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'restored_exit':restored['exit'],'restored_summary':restored['summary']}
for name in ['base-control.json','kill-run.json']:
    shutil.copyfile(s/name,out/name)
result['counter_sha256']=hashlib.sha256(counter.read_bytes()).hexdigest()
(out/'restoration.json').write_text(json.dumps(result,indent=1)+'\n'); print(json.dumps(result,indent=1))
