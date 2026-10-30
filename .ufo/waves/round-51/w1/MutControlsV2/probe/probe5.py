import importlib.util, json, os
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec=importlib.util.spec_from_file_location('c1', LANE+'/tools/round-50/c1-counter.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
root=LANE; rev='f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab'
print('=== receipt_fresh as the ported counter computes it, per carrier receipt ===')
for cid in ('g7581','g7582','c6490','c6430'):
    p='corpus/evidence/round-50/c1/%s/after.json'%cid
    adds=m.all_adds(root, rev, p)
    for freeze in (rev,):
        fresh = bool(adds) and all(a!=freeze and m.is_ancestor(root, freeze, a) for a in adds)
        print('  %-6s adds=%s' % (cid, [a[:12] for a in (adds or [])]))
        print('          receipt_fresh at freeze %s => %s' % (freeze[:12], fresh))
print()
print('=== carrier_fresh_ok (pin not in prior pins) at the r51 base ===')
cur=json.load(open(root+'/tools/round-50/carriers.json'))
pins,srcs=m.prior_pins(root, rev, cur)
print('  prior pin sources:',srcs)
for c in cur['carriers']:
    print('   %-6s pin=%s prior=%s' % (c['id'], c['sha256'][:12], c['sha256'] in pins))
print()
print('=== if tools/round-50/carriers.json were added to PRIOR_CARRIER_TABLES (the honest prior set) ===')
pins2=set(pins)
for c in json.load(open(root+'/tools/round-50/carriers.json'))['carriers']:
    pins2.add(c['sha256'])
for c in cur['carriers']:
    print('   %-6s carrier_fresh_ok would be %s' % (c['id'], c['sha256'] not in pins2))
