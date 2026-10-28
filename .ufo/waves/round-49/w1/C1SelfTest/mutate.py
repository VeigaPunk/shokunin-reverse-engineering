import sys,os,shutil,subprocess,json
S='/fast/scratch/hyaku/kaidoku-r49/C1SelfTest'
L='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
D=L+'/.ufo/waves/round-49/draft/tools/round-49/c1-counter.py'
M=sys.argv[1]
src=open(D).read()
A="d['matched'] = all(d.get(x) is True for x in CLAUSES)"
B="and all(b[x] is True for x in BINDINGS))"
assert src.count(A)==1 and src.count(B)==1
if M=='NOOP': pass
elif M in ('carrier_present','carrier_pin_ok','carrier_size_ok','carrier_fresh_ok','layout_ok','carve_ok','oracle_ok','tree_ok','receipt_present','receipt_fresh','evidence_envelope_ok','subject_pin_ok','operation_ok','handler_ok','chunks_ok','oracle_hits_ok','gaps_ok','nonregular_unpublished_ok','path_shape_ok','run_provenance_ok','evidence_id_ok','projection_ok'):
    src=src.replace(A,"d['matched'] = all(d.get(x) is True for x in CLAUSES if x != %r)"%M)
else:
    src=src.replace(B,"and all(b[x] is True for x in BINDINGS if x != %r))"%M)
d=f'{S}/mut/{M}'
shutil.rmtree(d,ignore_errors=True); os.makedirs(d+'/tools/round-49')
os.symlink(L+'/tools/round-27',d+'/tools/round-27')
open(d+'/tools/round-49/c1-counter.py','w').write(src)
env=dict(os.environ,TMPDIR=d)
r=subprocess.run(['python3','-I','-B',d+'/tools/round-49/c1-counter.py','--selftest','--work',d+'/w'],capture_output=True,text=True,env=env)
try: j=json.loads(r.stdout); f=j['failures']; n=j['cases']
except Exception: f=['PARSE '+r.stdout[-200:]+r.stderr[-300:]]; n=None
print(json.dumps({'mut':M,'exit':r.returncode,'cases':n,'nfail':len(f),'fail':[x[:110] for x in f][:4]}))
shutil.rmtree(d,ignore_errors=True)
