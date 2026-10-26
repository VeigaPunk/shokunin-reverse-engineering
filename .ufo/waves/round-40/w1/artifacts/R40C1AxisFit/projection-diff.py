#!/usr/bin/env python3
"""Compare two REA 6.5.0 extract-firmware envelopes: full semantic projection vs a
path-free derived projection. Pure stdlib. Usage: projection-diff.py A.json B.json"""
import hashlib, json, sys

PROJ_KEYS = ('subject','provider','analysis_profile','predicate_type','operation','parameters',
             'raw_result','normalized_result','confidence','authority','environment',
             'limitations','relationship_coverage','locations','evidence_links')

def load(p):
    d = json.load(open(p, 'rb'))
    return d['data'] if 'data' in d and isinstance(d['data'], dict) else d

def projection(ev):
    return {k: (ev.get(k) if ev.get(k) is not None else None) for k in PROJ_KEYS
            if not (k == 'relationship_coverage' and ev.get(k) is None)}

def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',',':'),
                                     ensure_ascii=False).encode()).hexdigest()

def rel(p):
    """Strip everything before the extraction root's last '/extract/' segment."""
    if not isinstance(p, str):
        return p
    for anchor in ('/extracted/', '/extract/'):
        i = p.find(anchor)
        if i >= 0:
            return '$output' + p[i + len(anchor) - 1:]
    return p

def derived(ev):
    nr = ev['normalized_result']
    return {
        'subject_sha256': ev['subject']['digest']['sha256'],
        'subject_format': ev['subject']['format'],
        'provider': [ev['provider']['id'], ev['provider']['version']],
        'operation': ev['operation'],
        'engine': [nr['engine']['name'], nr['engine']['version'],
                   nr['engine']['executable_sha256'], nr['engine']['worker_count']],
        'selection': [nr['selection']['offset'], nr['selection']['length'], nr['selection']['sha256']],
        'coverage': nr['coverage'],
        'published_bytes': nr['published_bytes'],
        'chunks': sorted([c['range']['offset'], c['range']['length'], c['handler'],
                          c['encrypted'], c['extraction_failed']] for c in nr['chunks']),
        'files': sorted([f['relative_path'], f['size'], f['sha256']] for f in nr['files']),
        'gaps': sorted([g['kind'], g.get('relative_path') or rel(g.get('input_path')),
                        sorted(g.get('dependencies') or []), g.get('continuation_id')]
                       for g in nr['extraction_gaps']),
        'unpublished': sorted([u['relative_path'], u['kind'], u['link_target']]
                              for u in nr['unpublished_entries']),
        'diagnostics': sorted([json.dumps(d.get('report', {}), sort_keys=True) .replace(
                                  json.dumps(d.get('report', {}), sort_keys=True), '') +
                               json.dumps(rel_diag(d.get('report', {})), sort_keys=True)
                               for d in nr['diagnostics']]),
        'derivations': sorted([rel(d['parent_path']), rel(d['child_path'])]
                              for d in nr['derivations']),
        'locations': ev['locations'],
        'raw_file_order': [f['relative_path'] for f in nr['files']],
        'raw_gap_order': [g.get('relative_path') for g in nr['extraction_gaps']],
    }

def rel_diag(r):
    return {k: (rel(v) if k in ('link', 'target') else v) for k, v in r.items()}

def walk_diff(a, b, path='', out=None):
    if out is None: out = []
    if type(a) is not type(b):
        out.append((path, 'type', type(a).__name__, type(b).__name__)); return out
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append((path + '/' + str(k), 'missing', k in a, k in b))
            else:
                walk_diff(a[k], b[k], path + '/' + str(k), out)
    elif isinstance(a, list):
        if len(a) != len(b):
            out.append((path, 'len', len(a), len(b)))
        for i, (x, y) in enumerate(zip(a, b)):
            walk_diff(x, y, path + '[%d]' % i, out)
    elif a != b:
        out.append((path, 'value', a, b))
    return out

def main():
    A, B = load(sys.argv[1]), load(sys.argv[2])
    full = walk_diff(projection(A), projection(B))
    der = walk_diff(derived(A), derived(B))
    print(json.dumps({
        'evidence_id_A': A['evidence_id'], 'evidence_id_B': B['evidence_id'],
        'evidence_id_equal': A['evidence_id'] == B['evidence_id'],
        'full_projection_digest_equal': digest(projection(A)) == digest(projection(B)),
        'full_projection_diff_count': len(full),
        'full_projection_diff_top': sorted({d[0].split('/')[1] for d in full if d[0].count('/') >= 1}),
        'derived_projection_digest_equal': digest(derived(A)) == digest(derived(B)),
        'derived_projection_diff': der[:40],
        'derived_diff_count': len(der),
    }, indent=1))

main()
