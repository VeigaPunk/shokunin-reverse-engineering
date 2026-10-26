import json, sys
def proj(path):
    env = json.load(open(path))
    d = env['data'] if ('data' in env and 'subject' not in env) else env
    nr = d.get('normalized_result') or {}
    chunks = sorted((c.get('handler'), bool(c.get('extraction_failed'))) for c in (nr.get('chunks') or []))
    gaps = sorted((g.get('kind'), g.get('relative_path')) for g in (nr.get('extraction_gaps') or []))
    files = sorted((f.get('relative_path'), f.get('sha256'), f.get('size')) for f in (nr.get('files') or []))
    diag = sorted((x.get('report') or {}).get('__typename__') for x in (nr.get('diagnostics') or []))
    return {'operation': d.get('operation'), 'provider': (d.get('provider') or {}).get('id'),
            'chunks': chunks, 'gaps': gaps, 'files': files, 'diag': diag,
            'coverage': nr.get('coverage'), 'published_bytes': nr.get('published_bytes')}
p1 = proj(sys.argv[1]); p2 = proj(sys.argv[2])
print('EQUAL' if p1 == p2 else 'DIFFER')
for k in p1:
    if p1[k] != p2[k]:
        print(' differs:', k, '\n  1:', json.dumps(p1[k])[:400], '\n  2:', json.dumps(p2[k])[:400])
print(json.dumps(p1, indent=1)[:1500])
