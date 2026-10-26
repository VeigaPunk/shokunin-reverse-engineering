import importlib.util, json, sys
spec = importlib.util.spec_from_file_location('cf', '/fast/scratch/hyaku/kaidoku-r40/R40W2C1Rescore/counter-frozen.py')
cf = importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)

def strict_nonregular_published(files, nonreg):
    """Counter's clause, but comparing the extract-stripped relative path exactly."""
    links = {r for r, k in nonreg if k != 'dir'}
    return [fp for fp, _, _ in files if cf.rel_suffix(fp) in links]

cf.nonregular_published = strict_nonregular_published
res = cf.measure('/home/vgpnk/Projects/shokunin/kaidoku-shokunin',
                 '42c10a58cb2cae3a4a0122af35a0cf95ac718043',
                 '7fce308631a8b457d6b7c5a4b39a923c4e9a49de',
                 '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents',
                 carrier_cache='/fast/scratch/hyaku/kaidoku-r40/R40W2C1Rescore/cache')
out = {k: res[k] for k in ('revision','carriers_matched','target','met_target','frozen_path_changed','bindings')}
out['carriers'] = {k: {x: v.get(x) for x in ('matched','nonregular_published','nonregular_unpublished_ok','projection_ok','gaps_ok','oracle_hits','oracle_files')} for k, v in res['carriers'].items()}
out['exit_code_if_cli'] = 0 if res['met_target'] else 1
print(json.dumps(out, indent=1, sort_keys=True))
