import importlib.util, json
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec=importlib.util.spec_from_file_location('c1', LANE+'/tools/round-50/c1-counter.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def nonreg(cid):
    rows,err=m.parse_nonregular(open(f'{LANE}/tools/round-50/oracle/{cid}.nonregular.tsv','rb').read())
    assert err is None, err
    return rows

def check(rule, cid):
    model,probs=m.gap_rule_model(json.dumps(rule))
    env=json.load(open(f'{LANE}/corpus/evidence/round-50/c1/{cid}/after.json'))
    run=json.load(open(f'{LANE}/corpus/evidence/round-50/c1/{cid}/run.json'))
    root,how=m.subject_root(env)
    od=(env.get('parameters') or {}).get('output_directory')
    diags=m.diagnostics(env)
    ok,msg=m.disposition_check(m.gaps(env), diags, nonreg(cid), model, root, od)
    return {'carrier':cid,'root_how':how,'gaps_ok':ok,'msg':msg[:170]}

base=json.load(open(LANE+'/tools/round-50/gap-rule.json'))
def f3(rc):
    r=json.loads(json.dumps(base))
    for k in ('char-device','block-device','fifo','socket'): r['allowed'][k]=[]
    r['removed']['silent'].pop('char-device',None)
    r['required']['char-device']=rc
    return r
for label,rule in (('R50 frozen',base), ('F3 as amended (required=true)',f3(True)), ('F3 fixed (required=false)',f3(False))):
    print('==',label)
    for cid in ('c6430','c6490','g7581','g7582'):
        r=check(rule,cid)
        print(f"   {cid}  gaps_ok={r['gaps_ok']}  root={r['root_how']}\n       {r['msg']}")
