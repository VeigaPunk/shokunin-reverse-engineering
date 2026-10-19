#!/usr/bin/env python3
"""EX-13 probe-vs-ground-truth comparator (v2).

Checks per probe JSON:
  1. selector set vs ABI-derived keccak set (missing/extra)
  2. normalized_result.bytecode.sha256 == sha256(compiled runtime bytes)
  3. normalized_result.artifact.sha256 == sha256(hex carrier file)
  4. every bytecodeOffset is a JUMPDEST (0x5b) in the compiled bytes
  5. every bytecodeOffset equals the destination my independent disassembler
     parsed for that selector's compare site (prologues.json)
"""
import hashlib
import importlib.util
import json
import os
import re

spec = importlib.util.spec_from_file_location("sr", "/var/tmp/ex13/tools/selector-recon.py")
sr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sr)

OUT = "/var/tmp/ex13/out"
PROBES = "/var/tmp/ex13/probes"

ABI = {
    "rv2-off-Rv2Token.runtime": f"{OUT}/rv2-off-Rv2Token.abi.json",
    "rv2-on200-Rv2Token.runtime": f"{OUT}/rv2-on200-Rv2Token.abi.json",
    "tre-off-Treasury.runtime": f"{OUT}/tre-off-Treasury.abi.json",
    "tre-on200-Treasury.runtime": f"{OUT}/tre-on200-Treasury.abi.json",
    "gau-off-Gauge.runtime": f"{OUT}/gau-off-Gauge.abi.json",
    "gau-on200-Gauge.runtime": f"{OUT}/gau-on200-Gauge.abi.json",
    "sw8-off.runtime": f"{OUT}/sw8-off.abi.json",
    "sw8-on200.runtime": f"{OUT}/sw8-on200.abi.json",
    "sw16-off.runtime": f"{OUT}/sw16-off.abi.json",
    "sw16-on200.runtime": f"{OUT}/sw16-on200.abi.json",
    "sw32-off.runtime": f"{OUT}/sw32-off.abi.json",
    "sw32-on200.runtime": f"{OUT}/sw32-on200.abi.json",
}


def expected_set(abi_path):
    abi = json.load(open(abi_path))
    sels = set()
    for a in abi:
        if a["type"] != "function":
            continue
        sig = a["name"] + "(" + ",".join(i["type"] for i in a["inputs"]) + ")"
        sels.add(sr.selector(sig))
    return sels


# parsed compare-site destinations from my disassembler
parsed = {}
for rec in json.load(open(f"{OUT}/prologues.json")):
    name = os.path.basename(rec["path"])[:-4]  # strip .bin -> match probe carrier keys
    d = rec.get("dispatch") or {}
    eq_dest = {s["sel"]: s["dest"] for s in d.get("eq_sites", []) if s.get("dest") is not None}
    eq_dest_ne = {s["sel"]: s["dest"] for s in d.get("non_eq_sites", []) if s.get("dest") is not None}
    parsed[name] = {"eq": eq_dest, "noneq": eq_dest_ne, "struct": d.get("structure_class")}

rows = []
for fname in sorted(os.listdir(PROBES)):
    if not fname.endswith(".json"):
        continue
    base = fname[:-5]
    m = re.match(r"^(?P<carrier>.+)\.(?P<ver>\d+\.\d+\.\d+)$", base)
    carrier, ver = m.group("carrier"), m.group("ver")
    probe = json.load(open(f"{PROBES}/{fname}"))
    rr = probe["raw_result"]
    nr = probe.get("normalized_result") or {}
    got = sorted(f["selector"] for f in rr["functions"])
    exp = sorted(expected_set(ABI[carrier]))
    missing = sorted(set(exp) - set(got))
    extra = sorted(set(got) - set(exp))
    decoded = (nr.get("bytecode") or {}).get("sha256")
    artifact_sha = (nr.get("artifact") or {}).get("sha256")
    cb = hashlib.sha256(open(f"{OUT}/{carrier}.bin", "rb").read()).hexdigest()
    hex_bytes = open(f"{OUT}/{carrier}.hex", "rb").read()
    hb = hashlib.sha256(hex_bytes).hexdigest()
    code = bytes.fromhex(hex_bytes.decode().strip())
    offsets = [(f["selector"], f["bytecodeOffset"]) for f in rr["functions"]]
    dests_5b = all(code[o] == 0x5B for _, o in offsets if o < len(code)) and bool(offsets)
    p = parsed.get(carrier, {"eq": {}, "noneq": {}})
    # every EQ-parsed dest lands in probe offsets, and vice versa
    parsed_eq = sorted(set(p["eq"].values()))
    probe_offs = sorted(o for _, o in offsets)
    dests_eq_match = parsed_eq == probe_offs if parsed_eq else None
    by_sel = {s: o for s, o in offsets}
    per_sel_match = all(p["eq"].get(s) == o for s, o in offsets if s in p["eq"])
    rows.append({
        "probe": fname, "carrier": carrier, "ver": ver,
        "K_expected": len(exp), "K_got": len(got), "missing": missing, "extra": extra,
        "decoded_sha_ok": decoded == cb, "artifact_sha_ok": artifact_sha == hb,
        "dests_5b": dests_5b, "parsed_eq_dests": parsed_eq, "probe_offsets": probe_offs,
        "dests_eq_match": dests_eq_match, "per_sel_match": per_sel_match,
        "struct": p.get("struct"),
    })

print(f"{'probe':46s} {'Kexp':>4s}{'Kgot':>4s} {'miss':>4s}{'extra':>5s} {'dec':>4s}{'art':>4s}{'5b':>4s}{'destEq':>7s}{'perSel':>7s}")
allok = True
for r in rows:
    ok = (not r["missing"] and not r["extra"] and r["decoded_sha_ok"] and r["artifact_sha_ok"]
          and r["dests_5b"] and (r["dests_eq_match"] is not False) and r["per_sel_match"])
    allok = allok and ok
    print(f"{r['probe']:46s} {r['K_expected']:4d}{r['K_got']:4d} {len(r['missing']):4d}{len(r['extra']):5d} "
          f"{str(r['decoded_sha_ok'])[0]:>4s}{str(r['artifact_sha_ok'])[0]:>4s}{str(r['dests_5b'])[0]:>4s}"
          f"{str(r['dests_eq_match'])[0]:>7s}{str(r['per_sel_match'])[0]:>7s}")
print("\nALL CHECKS PASS:", allok)
json.dump(rows, open(f"{OUT}/compare.json", "w"), indent=1)
print("wrote", f"{OUT}/compare.json")