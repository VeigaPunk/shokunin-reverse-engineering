import importlib.util, json
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
def load(name,path):
    spec=importlib.util.spec_from_file_location(name, path)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
c1=load('c1', LANE+'/tools/round-50/c1-counter.py')
v2=load('v2', LANE+'/tools/round-51/c1-counter.py')

def nonreg(mod,cid):
    rows,err=mod.parse_nonregular(open(f'{LANE}/tools/round-50/oracle/{cid}.nonregular.tsv','rb').read())
    assert err is None, err
    return rows
def check(mod,rule,cid):
    model,probs=mod.gap_rule_model(json.dumps(rule))
    env=json.load(open(f'{LANE}/corpus/evidence/round-50/c1/{cid}/after.json'))
    root,how=mod.subject_root(env)
    od=(env.get('parameters') or {}).get('output_directory')
    ok,msg=mod.disposition_check(mod.gaps(env), mod.diagnostics(env), nonreg(mod,cid), model, root, od)
    return ok, msg[:120]

base=json.load(open(LANE+'/tools/round-50/gap-rule.json'))
def law(rc):
    r=json.loads(json.dumps(base))
    for k in ('char-device','block-device','fifo','socket'): r['allowed'][k]=[]
    r['removed']['silent'].pop('char-device',None)
    r['required']['char-device']=rc
    return r
print('--- v2 counter (tools/round-51/c1-counter.py) with the amended law rule ---')
for label,rule in (('F3 as amended (required=true)',law(True)),('F3 FIXED (required=false)',law(False))):
    res=[check(v2,rule,c) for c in ('c6430','c6490','g7581','g7582')]
    print(f"{label}: "+' '.join(f"{c}={'T' if ok else 'F'}" for c,(ok,_) in zip(('c6430','c6490','g7581','g7582'),res)))
    print('    g7581:',res[2][1])
print()
print('--- does the v2 law_shape_ok clause reject required=true and accept required=false? ---')
for label,rule in (('required=true',law(True)),('required=false',law(False))):
    model,_=v2.gap_rule_model(json.dumps(rule))
    silent=(model.get('removed') or {}).get('silent') or {}
    notes=[]
    for k in v2.DEVICE_KINDS:
        if model['allowed'].get(k): notes.append(f'allowed[{k}] not empty')
        if silent.get(k): notes.append(f'silent[{k}] not empty')
    if model.get('required',{}).get('char-device') is not False: notes.append("required[char-device] is not False")
    print(f"  {label}: law_shape_ok = {not notes}  notes={notes}")
