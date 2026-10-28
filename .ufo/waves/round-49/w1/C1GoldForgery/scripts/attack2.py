import importlib.util, json, sys
sys.path.insert(0, '/fast/scratch/hyaku/kaidoku-r49/C1GoldForgery')
import attack as A
spec = importlib.util.spec_from_file_location('c1c', A.LANE + '/.ufo/waves/round-49/draft/tools/round-49/c1-controls.py')
c1c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c1c)
doc_tree, sizes = c1c._doc_landing({'doc_dir': A.LANE + '/.ufo/waves/round-49/w1/artifacts', 'root': A.CLONE, 'freeze': A.sh(['git','-C',A.CLONE,'rev-parse','HEAD']).stdout.strip()})
json.dump({k: len(v) for k, v in doc_tree.items()}, open(A.S + '/draft-doc-tree-sizes.json', 'w'), indent=1)
crs = {c['id']: c for c in A.carriers()}
r44 = {c: A.r44_env(c) for c in A.IDS}
envs_c = A.remint_all({c: A.oracle_env(crs[c], A.OUTDIR_OK % c) for c in A.IDS})
envs_r = A.remint_all({c: A.rewrite_outdir(r44[c], A.OUTDIR_OK % c) for c in A.IDS})
builds = {}
for name, envs in (('A11-oracle-plus-DRAFT-landing', envs_c), ('A12-r44-copy-plus-DRAFT-landing', envs_r)):
    files = {A.R49 % c: (json.dumps(e, indent=1, sort_keys=True) + '\n').encode() for c, e in envs.items()}
    files.update(doc_tree)
    builds[name] = A.variant(name, files)
res = {}
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=2) as ex:
    fs = {n: ex.submit(A.score, n, *builds[n]) for n in builds}
    for n in fs:
        res[n] = fs[n].result()
        print(n, 'exit', res[n]['exit'], 'matched', res[n].get('matched'), 'met', res[n].get('met'), 'stdout_sha256', res[n]['stdout_sha256'])
json.dump(res, open(A.S + '/results-attack2.json', 'w'), indent=1, sort_keys=True)
