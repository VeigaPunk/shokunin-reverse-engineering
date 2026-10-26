#!/usr/bin/env python3
import json, sys, glob, os, collections

def _iter_dicts(obj):
    stack=[obj]
    while stack:
        cur=stack.pop()
        if isinstance(cur,dict):
            yield cur
            stack.extend(cur.values())
        elif isinstance(cur,list):
            stack.extend(cur)

def features(data):
    op=data.get('operation'); pr=(data.get('provider') or {}).get('id')
    nr=data.get('normalized_result') or {}
    H=[]
    for c in (nr.get('chunks') or []):
        if isinstance(c,dict) and c.get('handler'): H.append(c['handler'])
    for g in (nr.get('extraction_gaps') or []):
        if isinstance(g,dict) and g.get('handler'): H.append(g['handler'])
    G=set(); D=set()
    for g in (nr.get('extraction_gaps') or []):
        if not isinstance(g,dict): continue
        if g.get('kind'): G.add(g['kind'])
        for d in (g.get('dependencies') or []): D.add(d)
    styled=[]; argv=[]
    for d in (nr.get('diagnostics') or []):
        if not isinstance(d,dict): continue
        r=d.get('report') or {}
        t=r.get('__typename__')
        if t=='MaliciousSymlinkRemoved': sr=True
        cmd=r.get('command')
        if isinstance(cmd,str): argv.append(cmd)
        elif isinstance(cmd,list):
            for tok in cmd: argv.append(str(tok))
    sr=False
    for d in (nr.get('diagnostics') or []):
        if not isinstance(d,dict): continue
        r=d.get('report') or {}
        if r.get('__typename__')=='MaliciousSymlinkRemoved': sr=True
    if argv: be='yes' if any('-be' in a for a in argv) else 'no'
    else: be='n/a'
    P=len(nr.get('files') or [])
    return dict(OP=op, PR=pr, H=sorted(set(H)), G=sorted(G), D=sorted(D), BE=be, SR=sr, P=P)

def main():
    for path in sys.argv[1:]:
        with open(path) as f: doc=json.load(f)
        data=doc.get('data') or doc
        print(path, json.dumps(features(data), sort_keys=True))
        nr=data.get('normalized_result') or {}
        for c in (nr.get('chunks') or []):
            if isinstance(c,dict):
                print('   chunk:', json.dumps(c, sort_keys=True)[:300])
        for g in (nr.get('extraction_gaps') or []):
            if isinstance(g,dict):
                print('   gap:', json.dumps(g, sort_keys=True)[:300])
        for d in (nr.get('diagnostics') or []):
            if isinstance(d,dict):
                print('   diag:', json.dumps(d, sort_keys=True)[:300])

if __name__=='__main__': main()
