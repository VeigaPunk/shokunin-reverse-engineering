import contextlib, copy, hashlib, importlib.util, io, json, os, pathlib, shutil, subprocess, sys
R=pathlib.Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
S=pathlib.Path(sys.argv[1]); O=R/'.ufo/waves/round-72/w1/ReviewerGates'
sys.path.insert(0,str(R/'tools/round-72'))
def load(name,file):
 spec=importlib.util.spec_from_file_location(name,R/'tools/round-72'/file); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
p=load('probe','seam-probe.py'); a=load('audit','capsule_audit.py'); b=load('battery','capsule-audit.py'); c=load('controls','controls.py'); m=load('mutation','mutation-check.py'); route=load('route','packed-elf.py')
results={}
plan=(R/'plans/round-72-claims.md').read_text(); container=json.loads((R/'.ufo/waves/round-72/claims.json').read_text())
import re
sentences=[' '.join(x.split()) for x in re.findall(r'\*\*Predicate \(one sentence, frozen\)\.\*\* (.*?)(?=\n\n)',plan,re.S)]
results['predicate_comparison']=[{'plan':s,'container':t,'identical':s==t} for s,t in zip(sentences,container['claims'])]
results['pins']={f:{'declared':v,'actual':hashlib.sha256((R/f).read_bytes()).hexdigest()} for f,v in container['instruments'].items()}
results['instrument_supersessions']=container.get('instrument_supersessions','ABSENT')
root=str(S/'run'); env={'HOME':root+'/home','TMPDIR':root+'/tmp','PATH':'/usr/bin','LANG':'C'}
records=[{'argv':['/usr/bin/git'],'env':env},{'argv':['/usr/bin/readelf'],'env':env}]
data=('\n'.join(json.dumps(x) for x in records)+'\n').encode(); cap=S/'capsule.jsonl'; cap.write_bytes(data)
summary={'records':2,'log_sha256':hashlib.sha256(data).hexdigest(),'exact_key_sets':True,'canary_absent':True,'home_under_run':True,'tmpdir_under_run':True,'children':{'git':1,'readelf':1},'original_run_root':root}
results['audit_no_digest']=a.audit(str(cap),{k:v for k,v in summary.items() if k!='log_sha256'})
with contextlib.redirect_stdout(io.StringIO()): rc=b.tamper_battery(str(cap),summary,str(S),str(O/'two-record-battery.json'))
results['two_record_battery_rc']=rc
contradiction=dict(summary,home_under_run=False,tmpdir_under_run=False)
results['audit_summary_contradiction']=a.audit(str(cap),contradiction)
# Fake only the checker boundary: shims report clean env outside the claimed checker run root.
def fake_invoke(*args,**kwargs):
 work=pathlib.Path(args[4]); logs=pathlib.Path(args[5][args[5].index('--child-env-log')+1]).parent
 e={'HOME':str(work/'not-checker/home'),'TMPDIR':str(work/'not-checker/tmp'),'LANG':'C','PATH':'/usr/bin'}
 for n in ('git','readelf'): (logs/(n+'.environ')).write_bytes(b'\0'.join((k+'='+v).encode() for k,v in e.items())+b'\0')
 return {'rc':0,'stdout':json.dumps({'checker_child_env':{'records':2,'all_allowlisted':True,'canary_present':False,'home_under_run':True,'tmpdir_under_run':True,'children':{'git':0,'readelf':0},'run_root':str(work/'checker-root')}})}
p.invoke=fake_invoke
results['a11_outside_checker_root_no_log']=p.checker_env_arm('unused',str(R),'unused','unused',str(S),'unused','unused')
results['binding_verdict']={k:p.binding_verdict(v) for k,v in {'missing':{},'empty':{'clauses':{}},'false':{'clauses':{'run_nonce':True,'run_binding':False}},'true':{'clauses':{'run_nonce':True,'run_binding':True}}}.items()}
# Check real receipt capsule handling, keeping all writes under explicit scratch.
receipt=json.loads((R/'.ufo/waves/round-72/l1/pre/route-at-declaration.json').read_text()); rev=receipt['rev']; commitment=(R/'.ufo/waves/round-72/l1/pre/nonce-commitment.txt').read_text().strip()
for label,explicit in [('missing_implicit',None),('missing_explicit',str(S/'missing.jsonl')),('unreadable_directory',str(S))]:
 fixture=copy.deepcopy(receipt); fixture['child_env_observed']['log']=str(S/'missing.jsonl'); path=S/(label+'.json'); path.write_text(json.dumps(fixture)); stream=io.StringIO()
 with contextlib.redirect_stdout(stream): rc=route.check_receipt(str(path),str(R),rev,commitment,work=str(S/'checker'),capsule=explicit)
 results[label]={'rc':rc,'output':json.loads(stream.getvalue())}
# Named real capsule with digest removed: real checker, not a mock.
fixture=copy.deepcopy(receipt); fixture['child_env_observed'].pop('log_sha256',None); path=S/'no-digest-receipt.json'; path.write_text(json.dumps(fixture)); stream=io.StringIO()
with contextlib.redirect_stdout(stream): rc=route.check_receipt(str(path),str(R),rev,commitment,work=str(S/'checker'),capsule=str(R/'.ufo/waves/round-72/l1/pre/env-at-declaration.jsonl'))
results['checker_no_digest']={'rc':rc,'output':json.loads(stream.getvalue())}
# Exercise controls aggregation with a lying audit that accepts pollution.
responses=[{'rc':1,'json':{'arms_passed':9,'target':11,'failed':['A10_run_binding','A11_checker_env']}},{'rc':0,'json':{'survivor_count':1,'survivors':['A10_binding_force_true']}},{'rc':0,'json':{'met':True,'failing':[]}},{'rc':0,'json':{'ok':True,'failures':[]}},{'rc':1,'json':{'ok':False}},{'rc':1,'json':{'ok':False}}]
c.run=lambda *args,**kwargs: responses.pop(0)
with contextlib.redirect_stdout(io.StringIO()): rc=c.main(['--root',str(R),'--base-rev','unused','--decl-rev',rev,'--receipt',str(R/'.ufo/waves/round-72/l1/pre/route-r71-at-declaration.json'),'--commitment',commitment,'--expect-upx',str(S/'upx'),'--work',str(S),'--json-out',str(O/'controls-lying-audit.json')])
results['controls_lying_audit_rc']=rc
# Optional target pin reports matched without any declared expected pin.
m.git_blob=lambda *args: b'binding_ok = clauses.get("run_binding") is True and present\n'
responses=[{'rc':0,'ok':True,'cases':1,'failed':[],'stderr_tail':''},{'rc':1,'ok':False,'cases':1,'failed':['a10-binding-from-checker'],'stderr_tail':''}]
m.run_selftest=lambda *args: responses.pop(0)
results['mutation_no_target_pin']=m.check(str(S),str(R),'unused','unused','r72')
(O/'attacks.json').write_text(json.dumps(results,indent=1)+'\n')
print(json.dumps({'receipt':str(O/'attacks.json'),'a11_false_green':results['a11_outside_checker_root_no_log']['ok'],'two_record_battery_rc':results['two_record_battery_rc'],'controls_lying_audit_rc':results['controls_lying_audit_rc'],'capsule_cases':{k:results[k]['rc'] for k in ('missing_implicit','missing_explicit','unreadable_directory','checker_no_digest')}}))
