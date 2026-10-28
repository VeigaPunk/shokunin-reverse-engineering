import os, sys, json, subprocess, importlib.util, shutil
S='/fast/scratch/hyaku/kaidoku-r49/C1CounterMut'
DRAFT='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/draft/tools/round-49/c1-counter.py'
spec_ = importlib.util.spec_from_file_location('c1c', DRAFT); c1 = importlib.util.module_from_spec(spec_); spec_.loader.exec_module(c1)
D = S + '/probe-freeze'
shutil.rmtree(D, ignore_errors=True); os.makedirs(D)
def g(*a):
    return subprocess.run(['git','-C',D,*a],capture_output=True,text=True)
g('init','-q')
top = g('rev-parse','--show-toplevel').stdout.strip()
assert os.path.realpath(top)==os.path.realpath(D), top
carriers = open('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/draft/tools/round-49/carriers.json').read()
def w(p, t):
    full=os.path.join(D,p); os.makedirs(os.path.dirname(full),exist_ok=True); open(full,'w').write(t)
def commit(msg):
    g('add','-A'); r=subprocess.run(['git','-C',D,'-c','user.name=probe','-c','user.email=probe@probe.invalid','commit','-qm',msg,'--allow-empty'],capture_output=True,text=True); assert r.returncode==0, r.stderr
    return g('rev-parse','HEAD').stdout.strip()
w('plans/round-49-claims.md','# plan\n'); w('tools/round-49/carriers.json',carriers); w('tools/round-49/c1-counter.py',open(DRAFT).read())
F=commit('freeze')
spec=json.loads(carriers)
out={}
out['P1_baseline_no_change']=c1.frozen_drift(D,F,F,spec)
w('tools/round-49/zz-new-helper.py','print(1)\n'); R1=commit('add new helper under tools/round-49 after freeze')
out['P1_new_file_under_tools_round49']=c1.frozen_drift(D,F,R1,spec)
w('tools/round-49/control-fixtures/ctl-x/extra.bin','x'); R2=commit('add new control fixture after freeze')
out['P2_new_file_under_control_fixtures']=c1.frozen_drift(D,F,R2,spec)
w('tools/round-49/zz-new-helper.py','print(2)\n'); R3=commit('edit the new helper (not frozen at freeze, but in tools/round-49)')
out['P3_edit_of_post_freeze_file']=c1.frozen_drift(D,F,R3,spec)
out['P4_provenance_tmp_segment']={k:c1.provenance_ok(k) for k in ['/tmp/kaidoku-r49/x','/home/x/kaidoku-r49/run','/fast/scratch/hyaku/kaidoku-r49/ok','/fast/scratch/hyaku/kaidoku-r42/x/kaidoku-r49/y']}
out['P5_under_root_probe']={'|'.join(k):c1.under_root(*k) for k in [('x_extract/a','x_extract'),('$output/x_extract/a','x_extract'),('x_extract//a','x_extract')]}
print(json.dumps(out, indent=1, default=str))
