import importlib.util, json, copy
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec=importlib.util.spec_from_file_location('c1', LANE+'/tools/round-50/c1-counter.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
ids=['g7581','g7582','c6490','c6430']
base=json.load(open(LANE+'/tools/round-50/gap-rule.json'))
ALL13=['247:0','136:0','136:1','136:2','136:3','136:4','136:5','136:6','136:7','230:0','3:0','3:1','3:2']
def law():
    r=copy.deepcopy(base); r['required']['char-device']=False
    r['removed'].get('silent',{}).pop('char-device',None)
    for k in ('char-device','block-device','fifo','socket'): r['allowed'][k]=[]
    return r
cache={}
def verdict(rule, subset):
    model,probs=m.gap_rule_model(json.dumps(rule)); out={}
    for cid in subset:
        if cid not in cache:
            env=json.load(open(LANE+'/corpus/evidence/round-50/c1/%s/after.json'%cid))
            nonreg,_=m.parse_nonregular(open(LANE+'/tools/round-50/oracle/%s.nonregular.tsv'%cid,'rb').read())
            cache[cid]=(env,nonreg)
        env,nonreg=cache[cid]
        root,_=m.subject_root(env,None)
        params=env.get('parameters') or {}; od=params.get('output_directory')
        ok,why=m.disposition_check(m.gaps(env), m.diagnostics(env), nonreg, model, root, od)
        out[cid]=(ok,(why or '').split(' on ')[0][:70])
    return out
print('=== WRONG-CARRIER-SET (the missing control) ===')
CABLE=['c6430','c6490']; FRITZ=['g7581','g7582']
for name,rule in (('LAW',law()), ('R50-old-rule',copy.deepcopy(base))):
    for label,sub in (('all four',ids), ('ONLY the 2 Cable-class',CABLE), ('ONLY the 2 FRITZ!Box-class',FRITZ), ('ONE carrier only',['c6430'])):
        v=verdict(rule,sub); n=sum(1 for ok,_ in v.values() if ok)
        binary = 'EXIT 0 (green)' if n==len(sub) else 'exit 1 (red)'
        print('  %-12s %-28s scored=%d clean=%d  -> %s   %s' % (name,label,len(sub),n,binary,{c:o for c,(o,_) in v.items()}))
print()
print('=== rule mutations against the LAW base (what --controls mode scores) ===')
cases={}
r=law(); r['required']['char-device']=True
cases['M1 law + required[char-device]=true (no whitelist)']=r
r=law(); r['required']['char-device']=True; r['removed'].setdefault('silent',{})['char-device']=['247:0']
cases['M2 law + required=true + silent 247:0 (== r50 device shape)']=r
r=law(); r['removed'].setdefault('silent',{})['char-device']=ALL13
cases['M3 law + silent ALL-13 whitelist']=r
r=law(); r['removed'].setdefault('silent',{})['char-device']=ALL13[:7]
cases['M4 law + silent STRICT SUBSET of 13']=r
r=law(); r['allowed']['char-device']=['unpublished-entry']
cases['M5 law + allowed[char-device]=[unpublished-entry]']=r
for k,v in cases.items():
    v2=verdict(v,ids); n=sum(1 for ok,_ in v2.values() if ok)
    fails=[c for c,(ok,_) in v2.items() if not ok]
    print('  %-56s clean=%d/4  -> %s  red_carriers=%s' % (k,n,'EXIT 0 (GREEN!)' if n==4 else 'exit 1 (red)',fails))
