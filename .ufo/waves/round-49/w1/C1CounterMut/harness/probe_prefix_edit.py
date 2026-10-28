import os, json, subprocess, importlib.util, shutil
S='/fast/scratch/hyaku/kaidoku-r49/C1CounterMut'
DRAFT='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/draft/tools/round-49/c1-counter.py'
spec_=importlib.util.spec_from_file_location('c1c', DRAFT); c1=importlib.util.module_from_spec(spec_); spec_.loader.exec_module(c1)
D=S+'/probe-freeze2'; shutil.rmtree(D, ignore_errors=True); os.makedirs(D)
g=lambda *a: subprocess.run(['git','-C',D,*a],capture_output=True,text=True)
g('init','-q'); assert os.path.realpath(g('rev-parse','--show-toplevel').stdout.strip())==os.path.realpath(D)
def w(p,t):
    f=os.path.join(D,p); os.makedirs(os.path.dirname(f),exist_ok=True); open(f,'w').write(t)
def commit(m):
    g('add','-A'); r=subprocess.run(['git','-C',D,'-c','user.name=probe','-c','user.email=probe@probe.invalid','commit','-qm',m,'--allow-empty'],capture_output=True,text=True); assert r.returncode==0,r.stderr; return g('rev-parse','HEAD').stdout.strip()
car=open('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/draft/tools/round-49/carriers.json').read()
w('plans/round-49-claims.md','# plan\n'); w('tools/round-49/carriers.json',car); w('tools/round-49/c1-controls.py','# controls v1\n'); w('tools/round-49/control-fixtures/ctl-0/a.txt','a')
F=commit('freeze'); spec=json.loads(car)
w('tools/round-49/c1-controls.py','# controls v2 (edited after freeze)\n'); R1=commit('edit an unlisted existing file under tools/round-49')
print('P6_edit_existing_unlisted_file:', c1.frozen_drift(D,F,R1,spec))
w('tools/round-49/control-fixtures/ctl-0/a.txt','b'); R2=commit('edit an existing control fixture')
print('P6b_edit_existing_fixture:', c1.frozen_drift(D,F,R2,spec))
