#!/usr/bin/env python3
import ast, hashlib, importlib.util, json, os, pathlib, shutil, subprocess, sys
R=pathlib.Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
D=R/'.ufo/waves/round-72/w1/CriticClaims'
S=pathlib.Path('/fast/scratch/hyaku/kaidoku-r72/CriticClaims')
S.mkdir(parents=True,exist_ok=True)
def dump(p,x): p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
try:
 for name in ('seam-probe.py','capsule_audit.py'):
  blob=subprocess.run(['git','-C',str(R),'show','34fe7aa70b627d92e2d27dbce308d9f5bebda63d:tools/round-72/'+name],check=True,capture_output=True).stdout
  (S/name).write_bytes(blob)
 p=load('probe',S/'seam-probe.py')
 a=load('audit',S/'capsule_audit.py')
 wrapper=S/'fake-checker.py'
 wrapper.write_text('''import argparse,json,os,pathlib,subprocess,sys
ap=argparse.ArgumentParser();ap.add_argument('--root');ap.add_argument('--rev');ap.add_argument('--pkg');ap.add_argument('--work');ap.add_argument('--check-receipt');ap.add_argument('--child-env-log');ap.add_argument('--nonce-commitment');x=ap.parse_args()
w=pathlib.Path(x.work); r=w/'fake-run';r.mkdir(exist_ok=True)
e={'HOME':str(r/'home'),'TMPDIR':str(r/'tmp'),'LANG':'C','PATH':os.environ['PATH']}
if x.child_env_log:
 rows=[]
 for name in ('git','readelf'):
  subprocess.run([name,'--version'],env=e,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  (pathlib.Path(x.child_env_log).parent/(name+'.environ')).write_bytes(b'\\0'.join((k+'='+v).encode() for k,v in e.items())+b'\\0')
  rows.append({'argv':[name,'--version'],'env':e})
 pathlib.Path(x.child_env_log).write_text(''.join(json.dumps(row)+'\\n' for row in rows))
 with open(w/'real-child.environ','wb') as f: subprocess.run(['/usr/bin/env','-0'],env=os.environ,stdout=f)
 print(json.dumps({'met':True,'checker_child_env':{'records':2,'children':{'git':1,'readelf':1},'all_allowlisted':True,'canary_present':False,'home_under_run':True,'tmpdir_under_run':True,'run_root':str(r)}}));sys.exit(0)
receipt=json.loads(pathlib.Path(x.check_receipt).read_text());mode=receipt.get('mode')
clauses={} if mode=='absent' else {'run_nonce':'wrong-nonce' not in x.check_receipt,'run_binding':'broken-binding' not in x.check_receipt}
print(json.dumps({'met':False,'failing':['deliberate contradictory checker failure'],'clauses':clauses}));sys.exit(1 if ('wrong-nonce' in x.check_receipt or 'broken-binding' in x.check_receipt) else 0)
''')
 c1=p.checker_env_arm(str(wrapper),str(R),'fixture','unused',str(S),'unused','unused')
 child=(S/'real-child.environ').read_bytes()
 c1['real_child_canary_present']=b'KAIDOKU_ENV_CANARY=probe-canary-r72\0' in child
 c1['real_child_keys']=sorted(z.split(b'=',1)[0].decode() for z in child.split(b'\0') if z)
 dump(D/'c1-wrapper.json',c1)
 # Execute precisely the frozen A10 branch, with real subprocess invocation and
 # producer binding; preceding A1-A9 and following A11 intentionally not executed.
 tree=ast.parse((S/'seam-probe.py').read_text())
 check=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='check')
 branch=next(n for n in check.body if isinstance(n,ast.If) and {x.id for x in ast.walk(n.test) if isinstance(x,ast.Name)}=={'receipt_path','nonce_commitment'})
 stop=next(n.lineno for n in branch.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='a11' for t in n.targets))
 body=[n for n in branch.body if n.lineno<stop]
 code=compile(ast.Module(body=body,type_ignores=[]),'frozen-A10','exec')
 c2={}
 for mode in ('absent','contradictory'):
  receipt=S/(mode+'.json');sha=hashlib.sha256(wrapper.read_bytes()).hexdigest()
  dump(receipt,{'mode':mode,'instrument':{'path':'fake-checker.py','sha256':sha},'rev':'fixture','run_nonce':'a'*64,'run_binding':'b'*64})
  ns=dict(p.__dict__);ns.update(receipt_path=str(receipt),root=str(R),rev='fixture',tool='fake-checker.py',blob_sha=sha,instrument=str(wrapper),pkg='unused',work=str(S),nonce_commitment='unused',legacy_receipt=None,arms=[])
  exec(code,ns)
  c2[mode]=ns['arms'][0]
 c2['direct_absent']=p.binding_verdict({'met':True})
 c2['direct_contradictory']=p.binding_verdict({'met':False,'clauses':{'run_nonce':True,'run_binding':True}})
 dump(D/'c2-verdict.json',c2)
 original=R/'.ufo/waves/round-71/l1/scores/c1-env-at-landing.jsonl'
 summary=json.loads((original.parent/'c1-env-audit.json').read_text())
 forged=[{'argv':['/usr/bin/'+name,'invented'],'env':{'HOME':str(S/'invented/home'),'TMPDIR':str(S/'invented/tmp'),'LANG':'C','PATH':'/usr/bin'}} for name in ('git','readelf')]
 capsule=S/'forged.jsonl';capsule.write_text(''.join(json.dumps(x)+'\n' for x in forged))
 forged_summary={'records':2,'children':{'git':1,'readelf':1},'exact_key_sets':True,'canary_absent':True,'home_under_run':True,'tmpdir_under_run':True,'original_run_root':str(S/'invented')}
 c3={'genuine':a.audit(str(original),summary),'forged_no_digest':a.audit(str(capsule),forged_summary)}
 forged_summary['log_sha256']=hashlib.sha256(capsule.read_bytes()).hexdigest()
 c3['forged_matching_digest']=a.audit(str(capsule),forged_summary)
 # A lying clean summary over actually polluted bytes still fails.
 forged[0]['env']['KAIDOKU_ENV_CANARY']='present';capsule.write_text(''.join(json.dumps(x)+'\n' for x in forged));forged_summary.pop('log_sha256')
 c3['polluted_no_digest']=a.audit(str(capsule),forged_summary)
 dump(D/'c3-capsule.json',c3)
 counts={}
 for name in ('c1-at-base.json','c2-at-base.json','c2-mutant-test.json','controls-at-declaration.json'):
  x=json.loads((R/'.ufo/waves/round-72/l1/pre'/name).read_text())
  counts[name]={k:x[k] for k in ('arms_passed','target','failed','survivor_count','survivors','ok','passed') if k in x}
 counts['capsule_records']=len([x for x in original.read_bytes().splitlines() if x.strip()]); counts['capsule_census_sum']=sum(summary['children'].values())
 counts['wave_roles']={'executor':5,'scribe':3,'reviewer':2,'mutation-tester':2,'critic':1,'sentinel':1,'scout':1,'connector':1}
 counts['wave_total']=sum(counts['wave_roles'].values());counts['attack_fraction']=5/16;counts['attack_percent']=100*5/16
 dump(D/'denominators.json',counts)
 shutil.copy2(wrapper,D/'fake-checker.py')
 print(json.dumps({'A11':c1['ok'],'real_child_canary':c1['real_child_canary_present'],'A10_absent':c2['absent']['ok'],'A10_contradictory':c2['contradictory']['ok'],'forged_no_digest':c3['forged_no_digest']['ok'],'forged_digest_clause':c3['forged_no_digest']['clauses']['log_sha256'],'polluted':c3['polluted_no_digest']['ok'],'counts':counts},indent=2))
finally:
 shutil.rmtree(S)
