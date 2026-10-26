import hashlib, json, sys

def enc(v, out):
    if v is None or not isinstance(v, (dict, list)):
        out.append(json.dumps(v, ensure_ascii=False, separators=(',', ':')))
        return
    if isinstance(v, list):
        out.append('[')
        for i, it in enumerate(v):
            if i: out.append(',')
            enc(it, out)
        out.append(']')
    else:
        out.append('{')
        first = True
        for k in sorted(v):
            if not first: out.append(',')
            first = False
            out.append(json.dumps(k, ensure_ascii=False))
            out.append(':')
            enc(v[k], out)
        out.append('}')

def project(e):
    s = e['subject']
    p = {
        'subject': None if s is None else {
            'digest': s['digest'], 'format': s['format'],
            'architecture': s.get('architecture')},
        'provider': e['provider'],
        'analysis_profile': e['analysis_profile'],
        'predicate_type': e['predicate_type'],
        'operation': e['operation'],
        'parameters': e['parameters'],
        'raw_result': e['raw_result'],
        'normalized_result': e['normalized_result'],
        'confidence': e['confidence'],
        'authority': e['authority'],
        'environment': e['environment'],
        'limitations': e['limitations'],
        'locations': e['locations'],
        'evidence_links': e['evidence_links'],
    }
    if e.get('relationship_coverage') is not None:
        p['relationship_coverage'] = e['relationship_coverage']
    return p

for path in sys.argv[1:]:
    e = json.load(open(path))
    if 'data' in e and isinstance(e['data'], dict):
        e = e['data']
    out = []
    enc(project(e), out)
    h = hashlib.sha256(''.join(out).encode()).hexdigest()
    print('%s\n  stored=%s\n  recomputed=ev_%s  match=%s' % (path, e['evidence_id'], h, e['evidence_id'] == 'ev_'+h))
