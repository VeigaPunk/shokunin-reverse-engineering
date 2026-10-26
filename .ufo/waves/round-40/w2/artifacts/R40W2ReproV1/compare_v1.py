#!/usr/bin/env python3
"""Independent semantic diff: committed V1 after.json vs my fresh REA run."""
import json, sys, collections

committed = json.load(open(sys.argv[1]))
mine      = json.load(open(sys.argv[2]))
out       = {}

def norm_rel(prefix_from, rel):
    # strip the extractor's staged-input directory so only the suffix inside the
    # extraction root is compared
    if rel.startswith(prefix_from + '/'):
        return rel[len(prefix_from)+1:]
    return rel

def chunks(d):
    nr = d['normalized_result']
    return [{'handler': c.get('handler'), 'offset': (c.get('range') or {}).get('offset'),
             'length': (c.get('range') or {}).get('length'),
             'extraction_failed': c.get('extraction_failed'),
             'encrypted': c.get('encrypted'),
             'root_range': c.get('root_file_range')} for c in nr.get('chunks') or []]

def fileset(d):
    nr = d['normalized_result']
    out = {}
    for f in nr['files']:
        rel = f['relative_path']
        pre = rel.split('/')[0]
        out[norm_rel(pre, rel)] = {'sha256': f['sha256'], 'size': f['size']}
    return out

def gaps(d):
    nr = d['normalized_result']
    g = collections.Counter()
    for x in nr.get('extraction_gaps') or []:
        rel = x.get('relative_path')
        if rel:
            pre = rel.split('/')[0]
            rel = norm_rel(pre, rel)
        g[(x.get('kind'), rel)] += 1
    return g

def unpublished(d):
    nr = d['normalized_result']
    s = set()
    for x in nr.get('unpublished_entries') or []:
        rel = x['relative_path']; pre = rel.split('/')[0]
        s.add((norm_rel(pre, rel), x.get('kind'), x.get('link_target')))
    return s

def diagnostics(d):
    dn = collections.Counter()
    for x in d['normalized_result'].get('diagnostics') or []:
        dn[x.get('__typename__') or x.get('typename') or x.get('type') or json.dumps(sorted(x))[:80]] += 1
    return dn

cf, mf = fileset(committed), fileset(mine)
cg, mg = gaps(committed), gaps(mine)
cu, mu = unpublished(committed), unpublished(mine)

res = {
 'chunks': {'committed': chunks(committed), 'mine': chunks(mine),
            'equal': chunks(committed) == chunks(mine)},
 'file_count': {'committed': len(cf), 'mine': len(mf)},
 'files_missing_in_mine': sorted(set(cf) - set(mf)),
 'files_extra_in_mine': sorted(set(mf) - set(cf)),
 'file_sha_size_mismatch': sorted(p for p in set(cf) & set(mf) if cf[p] != mf[p]),
 'gap_counts': {'committed': dict(sorted(collections.Counter(k for k, _ in cg.elements()).items())),
                'mine': dict(sorted(collections.Counter(k for k, _ in mg.elements()).items()))},
 'gap_sets_equal': set(cg) == set(mg),
 'gaps_missing_in_mine': sorted(x for x in set(cg) - set(mg)),
 'gaps_extra_in_mine': sorted(x for x in set(mg) - set(cg)),
 'unpublished_counts': {'committed': len(cu), 'mine': len(mu)},
 'unpublished_equal': cu == mu,
 'unpublished_missing_in_mine': sorted(cu - mu)[:20],
 'unpublished_extra_in_mine': sorted(mu - cu)[:20],
 'diagnostics_typenames': {'committed': dict(diagnostics(committed)), 'mine': dict(diagnostics(mine))},
 'coverage': {'committed': committed['normalized_result']['coverage'],
              'mine': mine['normalized_result']['coverage']},
 'published_bytes': {'committed': committed['normalized_result'].get('published_bytes'),
                     'mine': mine['normalized_result'].get('published_bytes')},
 'depth_limited_paths': {'committed': committed['normalized_result'].get('depth_limited_paths'),
                         'mine': mine['normalized_result'].get('depth_limited_paths')},
 'evidence_id': {'committed': committed['evidence_id'], 'mine': mine['evidence_id']},
 'selection': {'committed': committed['normalized_result'].get('selection'),
               'mine': mine['normalized_result'].get('selection')},
 'engine': {'committed': committed['normalized_result'].get('engine'),
            'mine': mine['normalized_result'].get('engine')},
 'parameters': {'committed': committed.get('parameters'), 'mine': mine.get('parameters')},
}
# summary line
diffs = [k for k in ('files_missing_in_mine','files_extra_in_mine','file_sha_size_mismatch',
                     'gaps_missing_in_mine','gaps_extra_in_mine') if res[k]]
res['nonzero_differences'] = diffs + ([] if res['gap_sets_equal'] else ['gap_sets'])
res['chunk_equal'] = res['chunks']['equal']
res['unpublished_equal_flag'] = res['unpublished_equal']
print(json.dumps(res, indent=1, sort_keys=False))
