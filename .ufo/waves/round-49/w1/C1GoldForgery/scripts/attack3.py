import json, sys, copy
sys.path.insert(0, '/fast/scratch/hyaku/kaidoku-r49/C1GoldForgery')
import attack as A, importlib.util
spec = importlib.util.spec_from_file_location('c1c', A.LANE + '/.ufo/waves/round-49/draft/tools/round-49/c1-controls.py')
c1c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c1c)
FREEZE = A.sh(['git', '-C', A.CLONE, 'rev-parse', 'HEAD']).stdout.strip()
doc_tree, _ = c1c._doc_landing({'doc_dir': A.LANE + '/.ufo/waves/round-49/w1/artifacts', 'root': A.CLONE, 'freeze': FREEZE})
crs = {c['id']: c for c in A.carriers()}
lean = {}
for c in A.IDS:
    full = A.oracle_env(crs[c], A.OUTDIR_OK % c)
    nr = full['normalized_result']
    keep_nr = {k: nr[k] for k in ('files', 'chunks', 'derivations', 'diagnostics', 'extraction_gaps',
                                  'unpublished_entries', 'depth_limited_paths', 'engine',
                                  'published_bytes', 'coverage')}
    lean[c] = {'operation': 'extract_firmware', 'provider': {'id': 'unblob'},
               'subject': {'digest': {'sha256': crs[c]['sha256']}},
               'parameters': {'output_directory': A.OUTDIR_OK % c, 'max_depth': 3},
               'normalized_result': keep_nr,
               'raw_result': {'report': full['raw_result']['report']}}
lean = A.remint_all(lean)
files = {A.R49 % c: (json.dumps(e, indent=1, sort_keys=True) + '\n').encode() for c, e in lean.items()}
files.update(doc_tree)
name = 'A13-lean-oracle-envelope-plus-DRAFT-landing'
D, f, rev = A.variant(name, files)
res = A.score(name, D, f, rev)
print(name, 'exit', res['exit'], 'matched', res.get('matched'), 'met', res.get('met'), 'stdout_sha256', res['stdout_sha256'], 'rev', rev)
print('lean envelope bytes', {c: len(json.dumps(e)) for c, e in lean.items()})
json.dump(res, open(A.S + '/results-attack3.json', 'w'), indent=1, sort_keys=True)
