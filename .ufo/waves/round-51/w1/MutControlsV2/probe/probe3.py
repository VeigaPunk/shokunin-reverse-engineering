import importlib.util, json, copy
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec=importlib.util.spec_from_file_location('c1', LANE+'/tools/round-50/c1-counter.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
ids=['g7581','g7582','c6490','c6430']
base=json.load(open(LANE+'/tools/round-50/gap-rule.json'))
ALL13=['247:0','136:0','136:1','136:2','136:3','136:4','136:5','136:6','136:7','230:0','3:0','3:1','3:2']
def law():
    r=copy.deepcopy(base); r['required']['char-device']=False; r['removed'].get('silent',{}).pop('char-device',None); return r
def score(rule):
    model,probs=m.gap_rule_model(json.dumps(rule)); n=0; note={}
    for cid in ids:
        env=json.load(open(LANE+'/corpus/evidence/round-50/c1/%s/after.json'%cid))
        root,_=m.subject_root(env,None)
        nonreg,_=m.parse_nonregular(open(LANE+'/tools/round-50/oracle/%s.nonregular.tsv'%cid,'rb').read())
        params=env.get('parameters') or {}; od=params.get('output_directory')
        ok,why=m.disposition_check(m.gaps(env), m.diagnostics(env), nonreg, model, root, od)
        n+=bool(ok); note[cid]=(ok,(why or '').split(',')[-1].strip())
    return n,note
cases={}
cases['LAW base (required char-device=false)']=law()
r=law(); r['removed'].setdefault('silent',{})['char-device']=['247:0','136:0','136:1']
cases['LAW + whitelist subset(3 of 13)  <- claim mutation #2']=r
r=law(); r['removed'].setdefault('silent',{})['char-device']=ALL13
cases['LAW + whitelist ALL 13          <- forbidden, untested']=r
r=copy.deepcopy(base); cases['R50 rule (required true, silent 247:0)  <- CTL-OLD / mutation #1']=r
r=copy.deepcopy(base); r['removed']['silent']['char-device']=['247:0','136:0','136:1','136:2','136:3','136:4','136:5']
cases['R50-shape + whitelist subset 7']=r
r=copy.deepcopy(base); r['removed']['silent']['char-device']=ALL13
cases['R50-shape + whitelist ALL 13']=r
for k,v in cases.items():
    n,note=score(v)
    print('%-58s gaps_ok_matched=%d  %s' % (k,n,{c:o for c,(o,_) in note.items()}))
