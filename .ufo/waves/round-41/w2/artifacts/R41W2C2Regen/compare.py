#!/usr/bin/env python3
"""R41W2C2Regen -- regeneration comparison for the R41-C2 held-out set.

Compares the committed held-out set
  corpus/evidence/round-41/c2/heldout/            (committed, at 8a1f4c73/e9a24d07)
against two fresh regenerations from the freeze seed
  $S/h    (--run --verify)
  $S/h2   (carrier-only, no REA)

Read-only; never writes into the lane.  Feature extraction is imported from the
frozen tools/round-41/c2-counter.py so the comparison uses the counter's own
vocabulary, plus a `declared` fallback (the key the frozen counter omits).
"""
import collections, hashlib, importlib.util, json, os, sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
C = f'{LANE}/corpus/evidence/round-41/c2/heldout'
S = os.environ['S']
SEED = 'd764389e9cbe61b9d1b07538ff3bff02d50bb34f'

spec = importlib.util.spec_from_file_location('c2c', f'{LANE}/tools/round-41/c2-counter.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
man = json.load(open(f'{C}/manifest.json'))
ids = [c['id'] for c in man['carriers']]
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()

def env(cid, base, which='envelope.json'):
    return m.envelope_data(json.load(open(f'{base}/{cid}/{which}')))

def pairs_interp(path):
    d = json.load(open(path))['results']
    out = {}
    for r in d:
        key = r['path'].rstrip('/').split('/')[-2]
        out[key] = (r['label'], r['action'], r.get('row'))
    return out

def pairs_eval(path):
    d = json.load(open(path))['labels']
    return {k: (v['label'], v['action']) for k, v in d.items()}

def walk(a, b, path, out):
    if type(a) is not type(b):
        out[path + ' <type>'] += 1; return
    if isinstance(a, dict):
        for k in set(a) | set(b):
            if k not in a or k not in b: out[path + '.' + k + ' <missing>'] += 1
            else: walk(a[k], b[k], path + '.' + k, out)
    elif isinstance(a, list):
        if len(a) != len(b): out[path + f' <len {len(a)}/{len(b)}>'] += 1
        for x, y in zip(a, b): walk(x, y, path + '[]', out)
    elif a != b:
        out[path] += 1

R = collections.OrderedDict()
R['seed'] = man['seed']; R['seed_is_freeze'] = man['seed'] == SEED
R['n_carriers'] = len(ids); R['n_classes'] = len(man['classes'])
R['manifest_sha_regen'] = sha(f'{S}/h/manifest.json')
R['manifest_sha_regen_norun'] = sha(f'{S}/h2/manifest.json')
R['manifest_sha_committed'] = sha(f'{C}/manifest.json')
R['manifest_identical'] = R['manifest_sha_regen'] == R['manifest_sha_committed'] == R['manifest_sha_regen_norun']

car_bad, tree_bad, car_bad2 = [], [], []
for cid in ids:
    want = next(c['sha256'] for c in man['carriers'] if c['id'] == cid)
    for base, bad in ((f'{S}/h', car_bad), (f'{S}/h2', car_bad2)):
        if sha(f'{base}/{cid}/carrier.sqsh') != want: bad.append(cid)
    if sha(f'{S}/h/{cid}/tree.json') != sha(f'{C}/{cid}/tree.json'): tree_bad.append(cid)
R['carriers_byte_identical_to_pin'] = {'run': not car_bad, 'no_run': not car_bad2, 'bad': car_bad + car_bad2}
R['trees_byte_identical'] = not tree_bad

tuple_diff, dig_comm, dig_regen, full_vs_env = [], [], [], []
decl_missing, decl_bad, decl_extras_bad = [], [], []
for c in man['carriers']:
    cid = c['id']; pin = c['sha256']
    ec, er = env(cid, C), env(cid, f'{S}/h')
    oc, orr = m.observed_features(ec), m.observed_features(er)
    if oc != orr: tuple_diff.append({'id': cid, 'committed': oc, 'regen': orr})
    if m.subject_sha(ec) != pin: dig_comm.append(cid)
    if m.subject_sha(er) != pin: dig_regen.append(cid)
    if json.load(open(f'{C}/{cid}/rea-full.json')).get('data') != json.load(open(f'{C}/{cid}/envelope.json')):
        full_vs_env.append(cid)
    cex = c.get('class_expected')
    decl = cex['features'] if isinstance(cex, dict) and isinstance(cex.get('features'), dict) else c.get('declared')
    canon = m.canon_features(decl)
    if not isinstance(canon, dict) or any(k not in canon for k in m.REQUIRED_FEATURES):
        decl_missing.append(cid); continue
    bad = [k for k in canon if k in oc and canon[k] != oc[k]]
    if bad: decl_bad.append({'id': cid, 'differ': bad})
    ex = c.get('declared_extras') or (cex or {}).get('features')
    if isinstance(ex, dict) and 'extraction_failed' in ex:
        if ex.get('extraction_failed') != oc['extraction_failed']: decl_extras_bad.append((cid, 'extraction_failed'))
    md = (c.get('rea') or {}).get('max_depth')
    if md is not None and isinstance(ex, dict) and ex.get('max_depth') != md: decl_extras_bad.append((cid, 'max_depth'))
R['envelope_tuple_diffs_committed_vs_regen'] = tuple_diff
R['subject_sha_equals_pin'] = {'committed': not dig_comm, 'regen': not dig_regen, 'bad': dig_comm + dig_regen}
R['rea_full_data_equals_envelope_json'] = not full_vs_env and True
R['declared_tuple_missing'] = decl_missing
R['declared_vs_observed_mismatch'] = decl_bad
R['declared_extras_mismatch'] = decl_extras_bad

ci, ri = pairs_interp(f'{S}/committed-interp.json'), pairs_interp(f'{S}/regen-interp.json')
ce, re_ = pairs_eval(f'{S}/committed-eval.json'), pairs_eval(f'{S}/regen-eval.json')
cie, rie = pairs_interp(f'{S}/committed-interp-env.json'), pairs_interp(f'{S}/regen-interp-env.json')
v2 = pairs_interp(f'{S}/v2interp.json')
R['pairs'] = {
    'committed_interp_equals_eval': sum(1 for k in ci if ci[k][:2] == ce[k]),
    'regen_interp_equals_eval': sum(1 for k in ri if ri[k][:2] == re_[k]),
    'committed_pairs_equal_regen_pairs': sum(1 for k in ci if ci[k][:2] == ri[k][:2]),
    'interp_reaful_equals_interp_envelope_json': sum(1 for k in ci if ci[k] == cie[k]),
    'n': len(ci),
    'distinct_labels': len({v[0] for v in ci.values()}),
    'label_counts': dict(sorted(collections.Counter(v[0] for v in ci.values()).items())),
    'rows_shared_committed_vs_regen': sum(1 for k in ci if ci[k][2] == ri[k][2]),
}
R['v2_table_on_heldout'] = {
    'pairs_differing_from_v3_evaluator': sum(1 for k in v2 if v2[k][:2] != ce[k]),
    'n': len(v2),
    'v2_labels': sorted({v[0] for v in v2.values()}),
    'v3_only_labels': sorted({v[0] for v in ce.values()} - {v[0] for v in v2.values()}),
    'differing_ids': [k for k in sorted(v2) if v2[k][:2] != ce[k]],
}

out = collections.Counter(); outmeta = collections.Counter()
for cid in ids:
    walk(json.load(open(f'{C}/{cid}/envelope.json')), json.load(open(f'{S}/h/{cid}/envelope.json')), '$', out)
    walk(json.load(open(f'{C}/{cid}/rea-full.json'))['meta'], json.load(open(f'{S}/h/{cid}/rea-full.json'))['meta'], 'meta', outmeta)
R['run_specific_field_diffs'] = dict(out.most_common())
R['run_specific_meta_diffs'] = dict(outmeta.most_common())

neg = [k for k in ('handler_set',) ]
json.dump(R, sys.stdout, indent=1)
print()
print('SUMMARY', json.dumps({k: R[k] for k in ('manifest_identical', 'carriers_byte_identical_to_pin',
      'trees_byte_identical', 'subject_sha_equals_pin', 'declared_tuple_missing',
      'declared_vs_observed_mismatch', 'envelope_tuple_diffs_committed_vs_regen')}))
