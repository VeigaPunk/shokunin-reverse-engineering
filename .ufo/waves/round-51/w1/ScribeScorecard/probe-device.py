import importlib.util, json
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec=importlib.util.spec_from_file_location('c1', LANE+'/tools/round-50/c1-counter.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

# A minimal nonregular census of DEVICE rows only (the law's subject), with NO gaps
# and NO diagnostics -- exactly what the law says an extractor produces.
dev_rows=[('dev/led','char-device','247:0'),
           ('dev/pts/0','char-device','136:0'),
           ('dev/ttyp0','char-device','3:0')]

def run(name, rule):
    model,probs=m.gap_rule_model(json.dumps(rule))
    ok,msg=m.disposition_check([], [], dev_rows, model, root='/r')
    print(f"{name}\n    gaps_ok={ok}\n    msg={msg[:190]}\n    rule_problems={probs}")

base=json.load(open(LANE+'/tools/round-50/gap-rule.json'))

r50=json.loads(json.dumps(base))
run('A. round-50 frozen rule (required.char-device=true, silent=[247:0], allowed=[unpublished-entry])', r50)

f3=json.loads(json.dumps(base))
for k in ('char-device','block-device','fifo','socket'): f3['allowed'][k]=[]
f3['removed']['silent'].pop('char-device',None)      # law: no char-device detail under silent
run('B. F3 amended AS WRITTEN (allowed=[] for device kinds; required UNCHANGED; silent lists NO device detail)', f3)

f3c=json.loads(json.dumps(f3)); f3c['required']['char-device']=False
run('C. F3 + required["char-device"]=false (a device entry needs no disposition)', f3c)

f3d=json.loads(json.dumps(f3)); f3d['required']['char-device']=False
f3d['removed']['silent']['char-device']=['247:0','136:0','3:0']
run('D. F3 + required=false + all-observed-details silent (detail whitelist)', f3d)
