#!/usr/bin/env python3
"""Offline field-by-field re-derivation of the landed R50-C1 receipt.

Imports the FROZEN counter (435d41fd) as a module and re-runs every clause that
does not invoke REA, using:
  - carrier bytes from the frozen-pinned carrier cache
  - frozen tables via `git show FREEZE:path`
  - committed envelopes via `git show REV:path`
Then compares against the landed receipt field by field.
The projection_ok clause is NOT re-run (no REA per seat bounds); it is checked
for internal consistency from the receipt's own recorded fields.
"""
import importlib.util
import json
import os
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
FREEZE = '435d41fd4ad9211d1579fc447936fb33d2b74467'
REV = '646d29c9df4ef77499248f95589cb9526c6dea19'
RECEIPT = os.path.join(LANE, '.ufo/waves/round-50/l1/scores/c1-after-attempt2.json')
CARRIER_CACHE = '/fast/scratch/hyaku/kaidoku-r50/carrier-cache'
WORK = '/fast/scratch/hyaku/kaidoku-r50/w4-RevC1MissReceipt/rederive-work'
PKG65 = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'

os.makedirs(WORK, exist_ok=True)

spec = importlib.util.spec_from_file_location(
    'c1frozen', '/fast/scratch/hyaku/kaidoku-r50/w4-RevC1MissReceipt/c1-counter-frozen.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def show(rev, path):
    p = subprocess.run(['git', '-C', LANE, 'show', f'{rev}:{path}'],
                       capture_output=True)
    return p.stdout if p.returncode == 0 else None


landed = json.load(open(RECEIPT))
results = {'match': [], 'mismatch': [], 'notes': []}


def check(name, got, want):
    ok = got == want
    results['match' if ok else 'mismatch'].append(name)
    print(('OK   ' if ok else 'DIFF ') + name)
    if not ok:
        print('  landed:', json.dumps(want)[:300])
        print('  rederiv:', json.dumps(got)[:300])
    return ok


# ---------- top-level scalars ----------
check('revision', REV, landed['revision'])
check('freeze', FREEZE, landed['freeze'])
check('predicate', 'P50-C1', landed['predicate'])
check('target', 4, landed['target'])
check('projection_profile', 'plus-extractor', landed['projection_profile'])
check('carrier_ids', ['g7581', 'g7582', 'c6490', 'c6430'], landed['carrier_ids'])
spec_doc = json.loads(show(FREEZE, 'tools/round-50/carriers.json'))
check('rea_parameters', {k: spec_doc['rea_parameters'][k] for k in
                         ('max_depth', 'max_output_bytes', 'max_output_files')},
      landed['rea_parameters'])

# ---------- frozen drift, spec, gap rule, prior pins (module's own code) ----------
drift = m.frozen_drift(LANE, FREEZE, REV, spec_doc)
check('frozen_path_changed', drift, landed['frozen_path_changed'])
# frozen_tables_valid: inline port of measure()'s check
plan_raw = show(FREEZE, 'tools/round-50/gap-rule.json')
plan_doc = json.loads(plan_raw)
unfrozen = []
for c in spec_doc.get('carriers') or []:
    for key in ('oracle', 'nonregular'):
        v = c.get(key)
        if isinstance(v, str) and v and show(FREEZE, v) is None:
            unfrozen.append(v)
check('tables_absent_at_freeze', sorted(unfrozen), landed['tables_absent_at_freeze'])
check('frozen_tables_valid', isinstance(plan_doc, dict) and not unfrozen,
      landed['frozen_tables_valid'])
ids, spec_probs = m.carriers_spec(spec_doc, m.TARGET, m.IDS)
check('carriers_spec_problems', spec_probs, landed['carriers_spec_problems'])
model, plan_probs = m.gap_rule_model(show(FREEZE, 'tools/round-50/gap-rule.json'))
check('gap_rule_problems', plan_probs, landed['gap_rule_problems'])
prior, prior_sources = m.prior_pins(LANE, FREEZE, spec_doc)
check('prior_pins', sorted(prior), landed['prior_pins'])
check('prior_pin_sources', prior_sources, landed['prior_pin_sources'])

# carriers.json / gap-rule blob equality (carriers_unchanged, gap_rule_unchanged)
check('carriers_unchanged',
      show(FREEZE, 'tools/round-50/carriers.json') == show(REV, 'tools/round-50/carriers.json'),
      True if landed['carriers_unchanged'] else False)
check('gap_rule_unchanged',
      show(FREEZE, 'tools/round-50/gap-rule.json') == show(REV, 'tools/round-50/gap-rule.json'),
      True if landed['gap_rule_unchanged'] else False)

# ---------- per-carrier clauses ----------
recomputed = {}
envs = {}
for c in spec_doc['carriers']:
    k = c['id']
    pin = c['sha256'].lower()
    d = {}
    fp = os.path.join(CARRIER_CACHE, pin + '.bin')
    raw = open(fp, 'rb').read() if os.path.isfile(fp) else None
    d['carrier_present'] = raw is not None
    import hashlib
    d['carrier_pin_ok'] = raw is not None and hashlib.sha256(raw).hexdigest() == pin
    d['carrier_fresh_ok'] = pin not in prior
    lay = m.layout_probe(raw)
    d['layout_ok'] = bool(lay.get('ok'))
    d['compression'] = lay.get('compression')
    ext = c.get('external')
    bu, size = lay.get('bytes_used'), lay.get('size')
    d['carve_ok'] = isinstance(ext.get('length'), int) and ext['length'] == bu == size
    d['carve'] = {'length': ext.get('length'), 'bytes_used': bu, 'size': size}

    oracle, oerr = m.parse_oracle(show(REV, c['oracle']))
    d['oracle_ok'] = oerr is None and len(oracle) > 0
    d['oracle_files'] = len(oracle)
    derived = m.rederive_oracle(raw, WORK, k)
    d['oracle_derived_files'] = len(derived)
    d['oracle_rederived_ok'] = set(oracle) == set(derived)
    if set(oracle) != set(derived):
        w, g = set(oracle), set(derived)
        d['oracle_rederived_diff'] = {'frozen_only': sorted(w - g)[:3],
                                      'derived_only': sorted(g - w)[:3]}

    nonreg, nerr = m.parse_nonregular(show(REV, c['nonregular']))
    d['nonregular_ok'] = nerr is None
    d['nonregular_entries'] = len(nonreg)
    d['nonregular_kinds'] = sorted({kind for _, kind, _d in nonreg})

    rpath = 'corpus/evidence/round-50/c1/%s/after.json' % k
    raw_receipt = show(REV, rpath)
    env = json.loads(raw_receipt)
    envs[k + '/after'] = env
    d['receipt_present'] = True
    d['receipt_digest'] = m.sha256_bytes(raw_receipt)
    adds = m.all_adds(LANE, REV, rpath)
    d['receipt_adds'] = adds
    d['receipt_first_add'] = adds[-1] if adds else None
    d['receipt_fresh'] = bool(adds) and all(a != FREEZE and m.is_ancestor(LANE, FREEZE, a)
                                            for a in adds)
    d['evidence_envelope_ok'] = not ({'counter_sha256', 'exit_code'} & set(env))
    d['subject_pin_ok'] = (env.get('subject') or {}).get('digest', {}).get('sha256') == pin
    prov = env.get('provider') or {}
    d['operation_ok'] = env.get('operation') == 'extract_firmware' and prov.get('id') == 'unblob'
    d['chunk_handlers'] = m.chunk_handlers(env)
    d['squashfs_handlers'] = m.squashfs_chunk_handlers(env)
    d['handler_ok'] = bool(d['squashfs_handlers']) and all(h == m.HANDLER for h in d['squashfs_handlers'])
    d['chunks_ok'] = not m.chunk_failed(env)
    root_value, root_how = m.subject_root(env, None)
    d['extract_root'] = root_value
    d['extract_root_source'] = root_how
    d['extract_root_confirmed'] = bool(root_value and any(m.under_root(p, root_value)
                                                          for p in m.receipt_paths(env)))
    d['chunk_roots'] = m.chunk_roots(env, None)
    files = m.published(env)
    d['published_files'] = len(files)
    nested = m.nested_roots(env, root_value)
    d['nested_roots'] = nested
    d['oracle_hits'] = m.oracle_hits(oracle, files, root_value, nested)
    d['published_rels'] = len(m.published_rels(files, root_value, nested))
    extra = m.extra_published(oracle, files, root_value, nested)
    d['extra_published'] = extra[:5]
    d['oracle_hits_ok'] = (d['oracle_ok'] and root_value is not None
                           and d['oracle_hits'] == d['oracle_files'] and not extra)
    params = env.get('parameters') or {}
    od = params.get('output_directory')
    d['output_directory'] = od
    diags = m.diagnostics(env)
    d['diagnostics'] = len(diags)
    d['removals'] = sorted(
        rel for rel, diag in
        ((m.diagnostic_rel(x, root_value, od), x) for x in diags)
        if rel is not None
        and m.diagnostic_typename(diag) == (model.get('removed') or {}).get('diagnostic'))
    ok, why = m.disposition_check(m.gaps(env), diags, nonreg, model, root_value, od)
    d['gaps_ok'] = ok
    d['gaps_note'] = why
    esc = m.nonregular_published(files, nonreg, root_value)
    d['nonregular_published'] = esc[:5]
    d['nonregular_unpublished_ok'] = root_value is not None and not esc
    shape_ok, shape_why = m.path_shape_ok(env)
    d['path_shape_ok'] = shape_ok
    d['path_shape_note'] = shape_why
    d['run_provenance_ok'] = m.provenance_ok(od)
    want_p = {kk: spec_doc['rea_parameters'][kk] for kk in
              ('max_depth', 'max_output_bytes', 'max_output_files')}
    got_p = {kk: params.get(kk) for kk in want_p}
    d['parameters_ok'] = all(isinstance(v, int) and not isinstance(v, bool)
                             for v in want_p.values()) and got_p == want_p
    recomputed[k] = d

# evidence id recompute (offline: node + package semanticProjection)
ev = m.evidence_ids(LANE, FREEZE, PKG65, envs, WORK)
for k in recomputed:
    key = k + '/after'
    recomputed[k]['evidence_id_stored'] = envs[key].get('evidence_id')
    recomputed[k]['evidence_id_recomputed'] = ev.get(key, (None, None))[0]
    recomputed[k]['evidence_id_ok'] = (key in ev and ev[key][0] == ev[key][1]
                                       and ev[key][0].startswith('ev_'))

# matched / carriers_matched / failing
matched = 0
fails = []
for k, d in recomputed.items():
    ok = all(d.get(x) is True for x in m.CLAUSES if x != 'projection_ok')
    d['matched_nonrea'] = ok
    matched += bool(ok)
    for x in m.CLAUSES:
        if x == 'projection_ok':
            continue
        if d.get(x) is not True:
            fails.append('%s:%s' % (k, x))
check('carriers_matched(non-REA clauses)', matched, landed['carriers_matched'])

# ---------- compare every recomputed field with landed ----------
COMPARE = ['carrier_present', 'carrier_pin_ok', 'carrier_fresh_ok', 'layout_ok',
           'compression', 'carve_ok', 'carve', 'oracle_ok', 'oracle_files',
           'oracle_derived_files', 'oracle_rederived_ok', 'nonregular_ok',
           'nonregular_entries', 'nonregular_kinds', 'receipt_present',
           'receipt_digest', 'receipt_adds', 'receipt_first_add', 'receipt_fresh',
           'evidence_envelope_ok', 'subject_pin_ok', 'operation_ok', 'chunk_handlers',
           'squashfs_handlers', 'handler_ok', 'chunks_ok', 'extract_root',
           'extract_root_source', 'extract_root_confirmed', 'chunk_roots',
           'published_files', 'nested_roots', 'oracle_hits', 'published_rels',
           'extra_published', 'oracle_hits_ok', 'output_directory', 'diagnostics',
           'removals', 'gaps_ok', 'gaps_note', 'nonregular_published',
           'nonregular_unpublished_ok', 'path_shape_ok', 'path_shape_note',
           'run_provenance_ok', 'parameters_ok', 'evidence_id_ok']
print()
print('=== per-carrier field comparison ===')
for k in ('g7581', 'g7582', 'c6490', 'c6430'):
    for f in COMPARE:
        check('carriers.%s.%s' % (k, f), recomputed[k].get(f),
              landed['carriers'][k].get(f))

print()
print('=== evidence ids ===')
for k in ('g7581', 'g7582', 'c6490', 'c6430'):
    print(k, 'stored=', recomputed[k]['evidence_id_stored'],
          'recomputed=', recomputed[k]['evidence_id_recomputed'],
          'equal=', recomputed[k]['evidence_id_stored'] == recomputed[k]['evidence_id_recomputed'])

# projection_ok consistency from receipt's own fields
print()
print('=== projection_ok (consistency only; REA rerun NOT re-run per seat bounds) ===')
for k in ('g7581', 'g7582', 'c6490', 'c6430'):
    lk = landed['carriers'][k]
    if k == 'g7581':
        consistent = lk['projection_ok'] is False and 'projection_error' in lk
        print(k, 'landed projection_ok=false with recorded projection_error:',
              consistent, '| error code:', lk['projection_error']['error']['code'])
    else:
        consistent = lk['projection_ok'] is True and lk.get('projection_diff') == []
        print(k, 'landed projection_ok=true with empty projection_diff:', consistent)

print()
print('SUMMARY mismatches:', len(results['mismatch']))
for name in results['mismatch']:
    print('  MISMATCH', name)
print('SUMMARY matched fields:', len(results['match']))
