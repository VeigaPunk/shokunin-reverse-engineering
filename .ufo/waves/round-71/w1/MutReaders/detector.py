import ast, concurrent.futures, contextlib, copy, difflib, hashlib, importlib.util, io, json, os, pathlib, shutil, subprocess, sys, tempfile
S=pathlib.Path(__file__).parent
F=pathlib.Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-71/w1/MutReaders')
os.environ['TMPDIR']=str(S); tempfile.tempdir=str(S)
os.environ['MUTREADERS_EXTRA']='canary'
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p):
 spec=importlib.util.spec_from_file_location('mut_target',p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
def assignments(p,name):
 return [n for n in ast.walk(ast.parse(p.read_text())) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets)]
def assign(p,name,ns):
 candidates=assignments(p,name); n=next(n for n in candidates if name!='run_root' or n.lineno>700); exec(compile(ast.Module(body=[n],type_ignores=[]),str(p),'exec'),ns); return ns[name]
def selftest(p):
 r=subprocess.run([sys.executable,'-I','-B',str(p),'--selftest'],capture_output=True,text=True,env=os.environ,timeout=30)
 return {'rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
def route_detector(p,label):
 m=load(p)
 if label=='a':
  keys=sorted(m.build_child_env(str(S))); return {'ok':keys==sorted(m.CHILD_ENV_KEYS),'keys':keys}
 if label=='b':
  log=S/'launcher.jsonl'; log.unlink(missing_ok=True)
  out=m.run(['/usr/bin/env'],env=m.build_child_env(str(S)),capture=str(log))
  raw=json.loads(log.read_text())['env']; executed=dict(line.split('=',1) for line in out['stdout'].splitlines())
  return {'ok':set(raw)==set(m.CHILD_ENV_KEYS) and set(executed)==set(m.CHILD_ENV_KEYS),'raw_keys':sorted(raw),'executed_keys':sorted(executed),'rc':out['rc']}
 if label=='c':
  ns={'os':os,'tempfile':tempfile,'work':str(S)}
  roots=[assign(p,'run_root',ns) for _ in range(3)]
  return {'ok':len(set(roots))==3,'roots':roots,'distinct':len(set(roots))}
 nonce='ab'*32; commitment=sha(nonce.encode())
 if label=='d':
  r={'run_root':str(S),'child_env_observed':{'keys':list(m.CHILD_ENV_KEYS),'records':1,'all_allowlisted':True,'home_under_run':True,'tmpdir_under_run':True,'canary_present':False}}
  failing=m.nonce_clauses(r,commitment); return {'ok':'run_nonce absent' in failing,'failing':failing}
 if label=='e':
  got=m.run_binding(nonce,'cc'*32,['dd'*32]); want=sha((nonce+':'+'cc'*32+':'+'dd'*32).encode())
  return {'ok':got==want,'got':got,'want':want}
 log=S/'polluted.jsonl'; env={**m.build_child_env(str(S)),'EXTRA':'1'}; log.write_text(json.dumps({'argv':['upx'],'env':env})+'\n')
 obs=m.observed_env(str(log),str(S)); return {'ok':obs['all_allowlisted'] is False,'observed':obs}
def probe_detector(p,label):
 mod=load(p); ns=vars(mod).copy(); ns.update(work=str(S),root='freeze-fixture',rev='b827a8b5d54f2885ec9be7786389f356c59226ce',tool='tools/round-71/packed-elf.py',pkg='fixture',instrument=str(S/'route.py'),blob_sha=sha((S/'route.py').read_bytes()),arms=[])
 if label=='g':
  # Execute the actual A8 source statements with a deterministic raw-log producer fixture.
  def invoke(*args,**kwargs):
   extra=args[5]; log=pathlib.Path(extra[extra.index('--child-env-log')+1]); out=pathlib.Path(extra[extra.index('--json-out')+1]); rr=str(log.parent/'run')
   env={'HOME':rr+'/home','TMPDIR':rr+'/tmp','LANG':'C','PATH':'/usr/bin','EXTRA':'injected'}
   log.write_text(''.join(json.dumps({'argv':[child],'env':env})+'\n' for child in ['upx','node','readelf']))
   out.write_text(json.dumps({'run_root':rr,'child_env_observed':{'records':3,'keys':sorted(mod.CHILD_ENV_KEYS),'all_allowlisted':True,'canary_present':False}})); return {'rc':0}
  ns['invoke']=invoke
  fn=next(n for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='check')
  start=next(i for i,n in enumerate(fn.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='a8_dir' for t in n.targets))
  end=next(i for i,n in enumerate(fn.body[start:],start) if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and any(isinstance(x,ast.Constant) and x.value=='A8_child_env_observed' for x in ast.walk(n)))
  exec(compile(ast.Module(body=fn.body[start:end+1],type_ignores=[]),str(p),'exec'),ns)
  return {'ok':ns['a8_ok'] is False,'arm':ns['arms'][0]}
 if label=='h':
  rr=str(S/'shared-root'); ns.update(a9_dir=str(S),bat_results=[{'rc':0}]*3,bat_dirs=[str(S/'shared-battery')]*3,route_roots=[rr]*3,route_results=[{'rc':1,'verdict_claimed':False,'records':1,'own_home':True,'own_tmp':True,'run_root':rr}]*3)
  ok=assign(p,'a9_ok',ns); return {'ok':ok is False,'arm_ok':ok,'distinct_battery_dirs':1,'distinct_run_roots':1}
 nonce='ab'*32; route=load(S/'route.py'); receipt={'run_nonce':nonce,'instrument':{'sha256':'cc'*32},'carriers':[{'packed_sha256':'dd'*32}],'run_root':str(S),'child_env_observed':{'keys':list(mod.CHILD_ENV_KEYS),'records':1,'all_allowlisted':True,'home_under_run':True,'tmpdir_under_run':True,'canary_present':False},'run_binding':'00'*32}
 # Genuine checker boundary uses the frozen route nonce clauses, not a forged success.
 ns.update(receipt_path='fixture.json',nonce_commitment=sha(nonce.encode()),bind_producer=lambda *a:(copy.deepcopy(receipt),[]),legacy_receipt=None)
 def invoke(*args,**kwargs):
  extra=args[5]; path=extra[extra.index('--check-receipt')+1]; r=receipt if path=='fixture.json' else json.loads(pathlib.Path(path).read_text()); failing=route.nonce_clauses(r,ns['nonce_commitment']); return {'rc':int(bool(failing)),'stdout':json.dumps({'failing':failing})}
 ns['invoke']=invoke
 fn=next(n for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='check')
 block=next(n for n in fn.body if isinstance(n,ast.If) and any(isinstance(x,ast.Name) and x.id=='nonce_commitment' for x in ast.walk(n.test)))
 exec(compile(ast.Module(body=[block],type_ignores=[]),str(p),'exec'),ns)
 return {'ok':ns['a10_ok'] is False,'arm':ns['arms'][0]}
results=[]
try:
 for label in 'abcdefghi':
  target=S/(label+'.py'); pristine=S/('route.py' if label<'g' else 'probe.py'); original=pristine.read_bytes(); mutated=target.read_bytes()
  F.joinpath(label+'.patch').write_text(''.join(difflib.unified_diff(original.decode().splitlines(True),mutated.decode().splitlines(True),fromfile='frozen',tofile=label+'.py')))
  detector=route_detector if label<'g' else probe_detector
  baseline={'selftest':selftest(pristine),'detector':detector(pristine,label)}
  changed={'selftest':selftest(target),'detector':detector(target,label)}
  target.write_bytes(original)
  restored={'selftest':selftest(target),'detector':detector(target,label)}
  selftest_verdict='inconclusive' if baseline['selftest']['rc'] else ('killed' if changed['selftest']['rc'] else 'not-killed')
  verdict='inconclusive' if not baseline['detector']['ok'] else ('killed' if not changed['detector']['ok'] else 'not-killed')
  results.append({'mutant':label,'frozen_sha256':sha(original),'mutated_sha256':sha(mutated),'restored_sha256':sha(target.read_bytes()),'restored_exact':target.read_bytes()==original,'baseline':baseline,'mutated':changed,'restored':restored,'selftest_verdict':selftest_verdict,'fixture_detector_verdict':verdict})
 F.joinpath('results.json').write_text(json.dumps(results,indent=2)+'\n')
 F.joinpath('detector.py').write_bytes(pathlib.Path(__file__).read_bytes())
 print(json.dumps([{'mutant':r['mutant'],'selftest':r['selftest_verdict'],'fixture':r['fixture_detector_verdict'],'restored_exact':r['restored_exact'],'mutated_output':r['mutated']['detector']} for r in results],indent=2))
finally:
 for label in 'abcdefghi':
  (S/(label+'.py')).write_bytes((S/('route.py' if label<'g' else 'probe.py')).read_bytes())
