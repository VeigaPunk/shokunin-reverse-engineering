import importlib.util, json
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec=importlib.util.spec_from_file_location('c1', LANE+'/tools/round-50/c1-counter.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

CABLE=[('dev/led','char-device','247:0')]
FRITZ=CABLE+[('dev/pts/%d'%i,'char-device','136:%d'%i) for i in range(8)]+\
      [('dev/tiatm','char-device','230:0')]+[('dev/ttyp%d'%i,'char-device','3:%d'%i) for i in range(3)]
ALL13=['247:0']+['136:%d'%i for i in range(8)]+['230:0']+['3:%d'%i for i in range(3)]

def verdict(rule, rows):
    model,probs=m.gap_rule_model(json.dumps(rule))
    ok,msg=m.disposition_check([], [], rows, model, root='/r')
    return ok

base=json.load(open(LANE+'/tools/round-50/gap-rule.json'))
def f3(required_char):
    r=json.loads(json.dumps(base))
    for k in ('char-device','block-device','fifo','socket'): r['allowed'][k]=[]
    r['removed']['silent'].pop('char-device',None)
    r['required']['char-device']=required_char
    return r

def m1_whitelist():
    r=f3(True); r['removed']['silent']['char-device']=ALL13; return r
def m3_partial():
    r=f3(True); r['removed']['silent']['char-device']=['247:0']; return r
def m4_subset():
    r=f3(True); r['removed']['silent']['char-device']=['247:0','136:0','136:1','136:2']; return r
FRITZ14=FRITZ+[('dev/ttyS0','char-device','4:64')]

for label, rule_fn in (
  ('F3 AS AMENDED (required.char-device UNCHANGED=true)', lambda: f3(True)),
  ('F3 FIXED (required.char-device=false)',               lambda: f3(False)),
):
    print('='*78); print(label)
    r=rule_fn()
    print(f"  CTL-NEW  cable={verdict(r,CABLE)}  fritz={verdict(r,FRITZ)}   (claim wants 4/4 = both True)")
    print(f"  M1 all-thirteen whitelist  fritz={verdict(m1_whitelist(),FRITZ)}   (claim wants RED=disposition-red)")
    print(f"  M2 fourteenth device, law rule  fritz14={verdict(r,FRITZ14)}   (claim wants GREEN under law)")
    print(f"  M2 fourteenth device, whitelist fritz14={verdict(m1_whitelist(),FRITZ14)} (claim wants RED under whitelist)")
    print(f"  M3 required=true + silent=[247:0]  fritz={verdict(m3_partial(),FRITZ)}   (claim wants RED)")
    print(f"  M4 strict-subset whitelist  fritz={verdict(m4_subset(),FRITZ)}   (claim wants RED)")
