import importlib.util, json, copy
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec=importlib.util.spec_from_file_location('c1', LANE+'/tools/round-50/c1-counter.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
ids=['g7581','g7582','c6490','c6430']
base=json.load(open(LANE+'/tools/round-50/gap-rule.json'))
ALL13=['247:0','136:0','136:1','136:2','136:3','136:4','136:5','136:6','136:7','230:0','3:0','3:1','3:2']
envs={}; nonregs={}
for cid in ids:
    envs[cid]=json.load(open(LANE+'/corpus/evidence/round-50/c1/%s/after.json'%cid))
    nonregs[cid]=m.parse_nonregular(open(LANE+'/tools/round-50/oracle/%s.nonregular.tsv'%cid,'rb').read())[0]
def score(rule):
    model,probs=m.gap_rule_model(json.dumps(rule)); n=0; notes={}
    for cid in ids:
        env=envs[cid]; root,_=m.subject_root(env,None)
        params=env.get('parameters') or {}; od=params.get('output_directory')
        ok,why=m.disposition_check(m.gaps(env), m.diagnostics(env), nonregs[cid], model, root, od)
        n+=bool(ok); notes[cid]=(ok,(why or '').split(' on ')[0][:90])
    return n,notes,probs
def law():
    r=copy.deepcopy(base); r['required']['char-device']=False; r['removed'].get('silent',{}).pop('char-device',None); return r
cases={}
cases['A0 LAW (required char-device=false)']=law()
r=law(); r['required']['symlink']=False
cases['A1 LAW but symlink NOT required  (near-neighbour)']=r
r=law(); r['required']['dir']=True
cases['A2 LAW but dir required        (near-neighbour)']=r
r=law(); r['required']['fifo']=True
cases['A3 LAW but fifo required       (near-neighbour)']=r
r=law(); r['required']['socket']=True
cases['A4 LAW but socket required     (near-neighbour)']=r
r=law(); r['allowed']['char-device']=[]
cases['A5 LAW but char-device gaps forbidden']=r
r=law(); r['removed']['kinds']=['symlink','char-device']
cases['A6 LAW but removals may name char-device']=r
r=law(); r['removed']['silent']['char-device']=ALL13
cases['A7 LAW + all-13 whitelist      (the FORBIDDEN alternative)']=r
r=law(); r['removed']['silent']['char-device']=['247:0','136:0']
cases['A8 LAW + strict-subset whitelist (claim mutation #2)']=r
r=law(); r['required']['char-device']=True; r['removed']['silent']['char-device']=['247:0']
cases['A9 LAW, required=true + 247:0 only (claim mutation #1 = r50 rule)']=r
for k,v in cases.items():
    n,notes,probs=score(v)
    print('%-58s matched=%d probs=%s' % (k,n,probs))
    for cid,(ok,why) in notes.items():
        if not ok: print('        %-6s %s' % (cid,why))
