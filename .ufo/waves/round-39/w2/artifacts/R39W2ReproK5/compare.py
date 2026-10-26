#!/usr/bin/env python3
"""Compare an REA extract-firmware envelope's data payload with the committed K5 after.json.

Usage: compare.py <my-envelope.json> <my-extract-dir> <my-input-path>
Normalises only run-local values (REA temp dir, scratch paths, blob ids, evidence id,
meta duration) and prints every residual difference. 0 residual diffs == the committed
receipt is byte-for-byte reproducible modulo run-local identifiers.
"""
import json, re, sys

MY, MY_OUT, MY_IN = sys.argv[1], sys.argv[2], sys.argv[3]
L = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
TH_OUT = "/fast/scratch/hyaku/kaidoku-r39/l1/c1runs/K5-scratch/extract"
TH_CAR = L + "/corpus/evidence/round-39/c1/K5/carrier.sqsh"

mine = json.load(open(MY))["data"]
theirs = json.load(open(L + "/corpus/evidence/round-39/c1/K5/after.json"))

def norm(s):
    s = re.sub(r'[^"\s]*rea-firmware-[A-Za-z0-9]+', "<TMP>", s)      # REA staging dir
    s = s.replace(MY_OUT, "<OUT>").replace(TH_OUT, "<OUT>")
    s = s.replace(MY_IN, "<INPUT>").replace(TH_CAR, "<INPUT>")
    s = re.sub(r'"[A-Za-z_]*blob_id":\s*"[0-9]+:1"', '"<BLOBKEY>":"<BLOB>"', s)
    s = re.sub(r'"provider_id":\s*"[0-9]+:1"', '"provider_id":"<BLOB>"', s)
    s = re.sub(r'"id":\s*"[0-9]+:1"', '"id":"<BLOB>"', s)
    s = re.sub(r'"evidence_id":\s*"[^"]+"', '"evidence_id":"<EV>"', s)
    s = re.sub(r'"duration":\s*"[^"]*"', '"duration":"<D>"', s)
    return json.loads(s)

def walk(x, y, p=""):
    out = []
    if type(x) != type(y): return [(p, "type", type(x).__name__, type(y).__name__)]
    if isinstance(x, dict):
        for k in sorted(set(x) | set(y)):
            if k not in x: out.append((p + "/" + k, "missing-mine", None, y[k]))
            elif k not in y: out.append((p + "/" + k, "missing-theirs", x[k], None))
            else: out += walk(x[k], y[k], p + "/" + k)
    elif isinstance(x, list):
        if len(x) != len(y): out.append((p, "len", len(x), len(y)))
        for i, (u, v) in enumerate(zip(x, y)): out += walk(u, v, f"{p}[{i}]")
    elif x != y: out.append((p, "value", x, y))
    return out

d = walk(norm(json.dumps(mine)), norm(json.dumps(theirs)))
print(f"input: {MY}")
print(f"residual diffs after normalising run-local values: {len(d)}")
for p, k, x, y in d:
    print(f"  {k} {p}\n    mine  ={str(x)[:200]}\n    theirs={str(y)[:200]}")
