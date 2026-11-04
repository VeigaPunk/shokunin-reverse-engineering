import concurrent.futures, contextlib, difflib, hashlib, importlib.util, io, json, os, pathlib, subprocess, sys
ROOT=pathlib.Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
OUT=ROOT/'.ufo/waves/round-74/w1/CriticClaims'
S=pathlib.Path(os.environ['TMPDIR'])
DECL='b3a7e28089582ce5fb002a1b88e5295caf696b9f'
def blob(path):
 return subprocess.check_output(['git','-C',str(ROOT),'show',DECL+':'+path]).decode()
text=blob('tools/round-74/seam-probe.py')
patches=[
 ('home-truthy-not-boolean','and s.get("home_under") is True','and s.get("home_under")'),
 ('last-named-sample','        out.setdefault(name or "?", sample)','        out[name or "?"] = sample'),
 ('double-forged-producer','    forged = forged_producer()','    forged = forged_producer()\n    forged = forged_producer()'),
 ('lie-clean-keys-unchecked','        sorted(s.get("keys") or []) == allow and not s.get("canary_present")','        not s.get("canary_present")'),
]
def run(item):
 name,src=item
 path=S/(name+'.py'); path.write_text(src)
 p=subprocess.run([sys.executable,'-I','-B',str(path),'--selftest'],cwd=ROOT,env={**os.environ,'TMPDIR':str(S)},capture_output=True,text=True)
 try: payload=json.loads(p.stdout)
 except ValueError: payload=None
 verdict='unevaluable'
 if payload and payload.get('cases')==20:
  verdict='survived' if p.returncode==0 and payload.get('failures')==[] else 'killed' if p.returncode==1 and payload.get('failures') else 'unevaluable'
 return {'name':name,'command':[sys.executable,'-I','-B',str(path),'--selftest'],'rc':p.returncode,'payload':payload,'stderr':p.stderr,'verdict':verdict}
items=[('pristine',text)]
for name,anchor,replacement in patches:
 assert text.count(anchor)==1,(name,text.count(anchor))
 mutated=text.replace(anchor,replacement,1)
 (OUT/(name+'.patch')).write_text(''.join(difflib.unified_diff(text.splitlines(True),mutated.splitlines(True),fromfile='declared/seam-probe.py',tofile=name+'/seam-probe.py')))
 items.append((name,mutated))
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 rows=list(pool.map(run,items))
# Load frozen audit without bytecode; no git fixture or lane mutation.
audit_source=blob('tools/round-74/record-audit.py')
ns={'__name__':'critic_audit','__file__':str(S/'record-audit.py')}
exec(compile(audit_source,ns['__file__'],'exec'),ns)
cosmetics={
 'D10':('## Search log\nround 73 round 74 Identified\n', 'atom_search_log'),
 'D12':('## 2026-11-04 — round 74:\ncensus erratum W04: 24 is correct; 23 is incorrect.\n','atom_census_erratum'),
 'D9':('## Registry\n| S275 | url | a | b | c | d | e | f | g | h | NOT used by corpus/knowledge/2026-11-04-r73-kernel-witness-record.md |\n','atom_s275_used_by'),
 'D11':('## Registry\n'+''.join('| x | '+page+' | a | b | c | d | e | rejected | | | |\n' for page in ns['R73_REJECTED_PAGES']),'atom_rejected_rows')}
atom_results=[]
for name,(fixture,fn) in cosmetics.items():
 ns['show']=lambda root,rev,path,f=fixture:f
 result=ns[fn](str(ROOT),'synthetic-cosmetic-fixture')
 atom_results.append({'name':name,'fixture':fixture,'result':result})
# Evaluate the actual frozen control met expression with adverse scorer output.
import ast
control=ast.parse(blob('tools/round-74/controls.py'))
expr=None
for node in ast.walk(control):
 if isinstance(node,ast.Dict):
  fields={k.value:v for k,v in zip(node.keys,node.values) if isinstance(k,ast.Constant)}
  arm=fields.get('arm')
  if isinstance(arm,ast.Constant) and arm.value=='c1_no_declared_cases':expr=fields['met']
assert expr is not None
expect=['a-drop-genuine-canary','b-unreadable-empty','b-first-sample-only','b-drop-canary-field','c-swap-verdict-inputs','c-skip-forged-subrun']
control_result=eval(compile(ast.Expression(expr),'<frozen-control-met>','eval'),{'sorted':sorted,'len':len},{'wrong':expect,'expect':expect,'killed':['x1','x2','x3','x4']})
result={'declaration':DECL,'probe_sha256':hashlib.sha256(text.encode()).hexdigest(),'independent_runs':rows,'cosmetic_atom_counterexamples':atom_results,'control_adverse_input':{'pristine_ok':False,'wrong':expect,'killed':['x1','x2','x3','x4'],'actual_frozen_met_expression':ast.unparse(expr),'met':control_result}}
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
