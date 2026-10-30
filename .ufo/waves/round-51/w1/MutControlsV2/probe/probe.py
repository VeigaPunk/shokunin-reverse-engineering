import importlib.util, json, os, sys, copy
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec=importlib.util.spec_from_file_location('c1', LANE+'/tools/round-50/c1-counter.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

ids=['g7581','g7582','c6490','c6430']
base=json.load(open(LANE+'/tools/round-50/gap-rule.json'))

def candidate(name):
    r=copy.deepcopy(base)
    if name=='r50':
        return r
    if name=='law_required_false':
        r['required']['char-device']=False
        r['removed'].get('silent',{}).pop('char-device',None)
        return r
    if name=='whitelist_all13':
        r['removed']['silent']['char-device']=['247:0','136:0','136:1','136:2','136:3','136:4','136:5','136:6','136:7','230:0','3:0','3:1','3:2']
        return r
    if name=='whitelist_subset7':
        r['removed']['silent']['char-device']=['247:0','136:0','136:1','136:2','136:3','136:4','136:5']
        return r
    if name=='required_true_whitelist_247only':
        r['required']['char-device']=True
        r['removed']['silent']['char-device']=['247:0']
        return r
    if name=='junk_every_kind_impossible':
        for k in ('symlink','char-device','block-device','fifo','socket','dir'):
            r['required'][k]=True
        r['removed']['silent']={}
        r['allowed']={k:['no-such-gap-kind'] for k in r['allowed']}
        return r
    raise KeyError(name)

def probe(fname, rule):
    model,probs=m.gap_rule_model(json.dumps(rule))
    out={}
    for cid in ids:
        env=json.load(open(LANE+'/corpus/evidence/round-50/c1/%s/%s'%(cid,fname)))
        nr=env.get('normalized_result') or {}
        root,how=m.subject_root(env, None)
        nonreg,e=m.parse_nonregular(open(LANE+'/tools/round-50/oracle/%s.nonregular.tsv'%cid,'rb').read())
        ok,why=m.disposition_check(m.gaps(env), m.diagnostics(env), nonreg, model, root)
        out[cid]=(ok, (why or '')[:150])
    return probs, out

print('=== receipt file probe: after.json vs run.json ===')
for fname in ('after.json','run.json'):
    for rn in ('r50','law_required_false'):
        probs,out=probe(fname, candidate(rn))
        print(' %-11s rule=%-22s model_problems=%s' % (fname, rn, probs))
        for cid,(ok,why) in out.items():
            print('      %-6s gaps_ok=%-5s %s' % (cid, ok, why))
print()
print('=== rule probe on after.json ===')
for rn in ('r50','law_required_false','whitelist_all13','whitelist_subset7','required_true_whitelist_247only','junk_every_kind_impossible'):
    probs,out=probe('after.json', candidate(rn))
    n=sum(1 for ok,_ in out.values() if ok)
    print(' %-34s model_problems=%-2s matched=%d  %s' % (rn, probs, n, {c:ok for c,(ok,_) in out.items()}))
