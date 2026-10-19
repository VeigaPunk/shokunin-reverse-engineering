#!/usr/bin/env python3
"""RV-1 LATE-JOIN — join every carrierA/carrierB probe envelope in the c1 tree
to my path-D source recomputation, keyed by decoded-bytecode sha256, and diff
the selector sets.  Also cross-check the EX-09 / EX-10 reconciliation claims.

Reads only; writes a table to stdout.
"""
import glob
import hashlib
import json
import os
import re
import sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
C1 = os.path.join(REPO, ".ufo/waves/arc3-loop1-round3/claims/c1")
sys.path.insert(0, os.path.join(C1, "RV-1/latejoin/tools"))
import keccak_bits as KD  # noqa: E402

# ---- my path-D recomputation from SOURCE --------------------------------
CARRIERS = {
    "CarrierA": dict(
        sol=os.path.join(C1, "EX-02/carrierA.sol"),
        planted=os.path.join(C1, "EX-02/planted-A.txt")),
    "VaultB": dict(
        sol=os.path.join(C1, "EX-04/carrierB.sol"),
        planted=os.path.join(C1, "EX-04/planted-B.txt")),
}

sys.path.insert(0, os.path.join(C1, "RV-1/latejoin/tools"))
from recompute_carriers import extract, parse_planted, push4_sites, sha256_file  # noqa: E402

mine = {}
for cname, info in CARRIERS.items():
    src = open(info["sol"]).read()
    fns = extract(src, cname)
    for f in fns:
        f["selector"] = KD.selector(f["sig"])
    mine[cname] = {
        "sels": sorted(f["selector"] for f in fns),
        "sigs": {f["selector"]: f["sig"] for f in fns},
        "source_sha256": sha256_file(info["sol"]),
    }
    pl = parse_planted(info["planted"])
    mine[cname]["planted_sels"] = sorted(p["selector"] for p in pl)

# ---- runtime file digests, decoded --------------------------------------
RUNTIME = {
    "9f7392acccea72cd42bdd8095a8578cab0727766f218b5399da22bc21d23741a":
        ("CarrierA", os.path.join(C1, "EX-02/evidence/carrierA.runtime.hex")),
    "aaf85ceaf124bac2d3a32428927194158c9211e4472a0cf06f88a721cf239412":
        ("VaultB", os.path.join(C1, "EX-04/evidence/carrierB.runtime-opt200.hex")),
    "679678e9a67aee701094a4bfeafd2a02311460658aa4b400202340b47d83d005":
        ("VaultB", os.path.join(C1, "EX-04/evidence/carrierB.runtime-noopt.hex")),
}

probes = sorted(glob.glob(os.path.join(C1, "**", "*.json"), recursive=True))
rows = []
for p in probes:
    base = os.path.basename(p)
    if "probe" not in base and "leg" not in base:
        continue
    try:
        d = json.load(open(p))
    except Exception:
        continue
    if not isinstance(d, dict):
        continue
    nr = d.get("normalized_result") or {}
    if not isinstance(nr, dict):
        continue
    bc = (nr.get("bytecode") or {}).get("sha256")
    if bc not in RUNTIME:
        continue
    cname, rpath = RUNTIME[bc]
    fns = nr.get("functions") or []
    got = sorted(str(f.get("selector", "")).replace("0x", "").lower() for f in fns)
    want = mine[cname]["sels"]
    rows.append({
        "envelope": os.path.relpath(p, C1),
        "carrier": cname,
        "n": len(got),
        "set_equal": got == want,
        "missing": sorted(set(want) - set(got)),
        "extra": sorted(set(got) - set(want)),
        "dispatch_all_abi": all(f.get("dispatch") == "abi" for f in fns),
        "bc_sha256": bc,
        "bc_bytes": (nr.get("bytecode") or {}).get("bytes"),
        "kind": (nr.get("bytecode") or {}).get("kind"),
        "stateMut_mismatch": [
            (f["selector"], f.get("inferred_state_mutability"))
            for f in fns
            if mine[cname]["sigs"].get(str(f["selector"]).replace("0x", "").lower())
            and False
        ],
    })

print("=== envelope vs path-D source recompute ===")
print(f"{'envelope':<62} {'carrier':<9} {'n':>3} {'eq':<6} miss extra abi")
bad = 0
for r in rows:
    flag = "OK" if r["set_equal"] else "DIFF"
    if not r["set_equal"]:
        bad += 1
    print(f"{r['envelope']:<62} {r['carrier']:<9} {r['n']:>3} {flag:<6} "
          f"{len(r['missing'])}    {len(r['extra'])}     {r['dispatch_all_abi']}")
print(f"\ntotal envelopes joined: {len(rows)}   disagreements: {bad}")

by_carrier = {}
for r in rows:
    by_carrier.setdefault(r["carrier"], []).append(r)
print("\n=== per carrier ===")
for c, rs in sorted(by_carrier.items()):
    print(f"{c}: {len(rs)} envelopes, all set-equal={all(x['set_equal'] for x in rs)}, "
          f"K={mine[c]['sels'].__len__()}, planted K={len(mine[c]['planted_sels'])}, "
          f"planted==mine={mine[c]['planted_sels'] == mine[c]['sels']}")

json.dump({"rows": rows, "mine": mine}, open("/var/tmp/rv1-latejoin/out/envelope-join.json", "w"), indent=2)
