import json, hashlib, os, sys

def js_str(s):
    # JSON.stringify for strings: no ASCII escaping, escape control chars & quotes/backslash
    out=['"']
    for ch in s:
        o=ord(ch)
        if ch=='"': out.append('\\"')
        elif ch=='\\': out.append('\\\\')
        elif ch=='\n': out.append('\\n')
        elif ch=='\r': out.append('\\r')
        elif ch=='\t': out.append('\\t')
        elif ch=='\b': out.append('\\b')
        elif ch=='\f': out.append('\\f')
        elif o<0x20: out.append('\\u%04x'%o)
        else: out.append(ch)
    out.append('"')
    return ''.join(out)

def canon(v, buf):
    if v is None: buf.append('null'); return
    if v is True: buf.append('true'); return
    if v is False: buf.append('false'); return
    if isinstance(v, (int,float)):
        if isinstance(v,float) and v==int(v): buf.append(str(int(v)))
        else: buf.append(json.dumps(v))
        return
    if isinstance(v,str): buf.append(js_str(v)); return
    if isinstance(v,list):
        buf.append('[')
        for i,item in enumerate(v):
            if i: buf.append(',')
            canon(item,buf)
        buf.append(']'); return
    if isinstance(v,dict):
        buf.append('{')
        first=True
        for k in sorted(v.keys()):
            if v[k] is None and False: pass
            if not first: buf.append(',')
            first=False
            buf.append(js_str(k)); buf.append(':')
            canon(v[k],buf)
        buf.append('}'); return
    raise TypeError(type(v))

def project(e):
    p={
     'subject': None if e['subject'] is None else {
        'digest': e['subject']['digest'],
        'format': e['subject']['format'],
        'architecture': e['subject']['architecture']},
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
    rc=e.get('relationship_coverage')
    if rc is not None: p['relationship_coverage']=rc
    return p

def eid(e):
    buf=[]; canon(project(e),buf)
    return 'ev_'+hashlib.sha256(''.join(buf).encode('utf-8')).hexdigest()

BASE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-39/c2/heldout'
for h in sys.argv[1:]:
    e=json.load(open(os.path.join(BASE,h,'envelope.json')))
    r=eid(e)
    print(h,'committed',e['evidence_id'],'recomputed',r,'MATCH' if r==e['evidence_id'] else 'MISMATCH')
