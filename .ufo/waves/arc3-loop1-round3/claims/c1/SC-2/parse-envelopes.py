#!/usr/bin/env python3
"""SC-2 (arc3-loop1-round3, c1 scribe): compact parser over round-3 c1 probe envelopes.
Prints: file, evidence_id, subject.sha256/name, encoding param, bytecode.sha256,
function count, selector:offset:dispatch set (sorted), stateMutability multiset, args multiset.
Read-only."""
import json, sys, glob, collections, hashlib, os

def digest(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

for path in sorted(sys.argv[1:]):
    raw = open(path, 'rb').read()
    try:
        d = json.loads(raw)
    except Exception as e:
        print(f"{path}: NOT-JSON ({e}) sha256={digest(path)[:16]}")
        continue
    ev = d.get('evidence_id', '-')
    subj = d.get('subject', {}) or {}
    sd = (subj.get('digest') or {}).get('sha256', '-')
    params = d.get('parameters', {}) or {}
    nr = d.get('normalized_result', {}) or {}
    ra = d.get('raw_result', {}) or {}
    funcs = nr.get('functions') or ra.get('functions') or []
    bc = (nr.get('bytecode') or {}).get('sha256', '-')
    bcbytes = (nr.get('bytecode') or {}).get('bytes', '-')
    mut = collections.Counter(f.get('stateMutability') for f in funcs)
    args = collections.Counter(f.get('arguments') for f in funcs)
    rows = ','.join(f"{f.get('selector')}@{f.get('bytecodeOffset')}:{f.get('dispatch')}" for f in funcs)
    print(f"{os.path.basename(path)}")
    print(f"  ev={ev[:24]}… sha256(raw)={digest(path)[:16]}…")
    print(f"  subject.name={subj.get('name')} subject.sha256={sd[:16]}… enc={params.get('encoding')}")
    print(f"  bytecode={bc[:16]}… ({bcbytes} B) nfunc={len(funcs)}")
    print(f"  funcs=[{rows}]")
    print(f"  mut={dict(mut)} args={dict(args)}")