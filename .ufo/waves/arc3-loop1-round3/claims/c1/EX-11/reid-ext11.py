#!/usr/bin/env python3
"""EX-11 re-derivation: envelope (wrapper or bare) -> evidence_id under a chosen projection.
Projection key set is switchable to match the pin: rc=yes (>=6.7.0), rc=no (<=6.4.0 style).
Usage: reid-ext11.py <envelope-or-wrapper.json> [rc|norc]
"""
import hashlib, json, sys

def _js_number(value):
    if value == int(value) and abs(value) < 1e21:
        return str(int(value))
    r = repr(value)
    if "e" in r:
        m, e = r.split("e"); ei = int(e)
        return f"{m}e{'+' if ei >= 0 else '-'}{abs(ei)}"
    return r

def _key_sort(k): return k.encode("utf-16-be")

def canon(v):
    if v is None or isinstance(v, (bool, int, str)): return json.dumps(v, ensure_ascii=False)
    if isinstance(v, float): return _js_number(v)
    if isinstance(v, list): return "[" + ",".join(canon(x) for x in v) + "]"
    if isinstance(v, dict):
        items = sorted(v.items(), key=lambda kv: _key_sort(kv[0]))
        return "{" + ",".join(json.dumps(k, ensure_ascii=False) + ":" + canon(x) for k, x in items) + "}"
    raise TypeError(type(v))

def projection(ev, rc):
    s = ev.get("subject")
    p = {
        "subject": None if s is None else {"digest": s.get("digest"), "format": s.get("format"), "architecture": s.get("architecture")},
        "provider": ev.get("provider"), "analysis_profile": ev.get("analysis_profile"),
        "predicate_type": ev.get("predicate_type"), "operation": ev.get("operation"),
        "parameters": ev.get("parameters"), "raw_result": ev.get("raw_result"),
        "normalized_result": ev.get("normalized_result"), "confidence": ev.get("confidence"),
        "authority": ev.get("authority"), "environment": ev.get("environment"),
        "limitations": ev.get("limitations"),
    }
    if rc: p["relationship_coverage"] = ev.get("relationship_coverage")
    p.update({"locations": ev.get("locations"), "evidence_links": ev.get("evidence_links")})
    return p

path, mode = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "rc")
ev = json.loads(open(path, "rb").read().decode())
if isinstance(ev, dict) and "ok" in ev and "data" in ev: ev = ev["data"]
if isinstance(ev, dict) and "evidence_bundle" in ev: ev = ev["evidence_bundle"]["records"][0]
body = canon(projection(ev, mode == "rc"))
derived = "ev_" + hashlib.sha256(body.encode()).hexdigest()
print(f"canonical_bytes: {len(body.encode())}")
print(f"derived:  {derived}")
print(f"recorded: {ev.get('evidence_id')}")
print("MATCH" if derived == ev.get("evidence_id") else "MISMATCH")
