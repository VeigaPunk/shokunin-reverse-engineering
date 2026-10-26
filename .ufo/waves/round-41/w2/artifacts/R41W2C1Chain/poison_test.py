import importlib.util, json, os, sys
S='/fast/scratch/hyaku/kaidoku-r41/R41W2C1Chain'
spec=importlib.util.spec_from_file_location('c1c','/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-41/c1-counter.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def stub(carrier_bytes, cid, params=None): return ('error','stub: rerun not executed for this probe')
res=m.measure('/home/vgpnk/Projects/shokunin/kaidoku-shokunin',
              '7a24ff74736e84b1903db7ba01891c406a6e32a2',
              'd764389e9cbe61b9d1b07538ff3bff02d50bb34f',
              '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents',
              rerun=stub, carrier_cache=S+'/poison')
print('carriers_matched', res['carriers_matched'], 'met_target', res['met_target'])
for k,d in res['carriers'].items():
    print(k, {x: d.get(x) for x in ('carrier_present','carrier_pin_ok','layout_ok','carve_ok',
          'oracle_hits_ok','projection_ok','projection_skipped','evidence_id_ok','matched')})
out={k:res[k] for k in ('carriers_matched','met_target','bindings')}
json.dump({'carriers':res['carriers'],'carriers_matched':res['carriers_matched'],'met_target':res['met_target']},
          open(S+'/poison-result.json','w'), indent=1, sort_keys=True)
