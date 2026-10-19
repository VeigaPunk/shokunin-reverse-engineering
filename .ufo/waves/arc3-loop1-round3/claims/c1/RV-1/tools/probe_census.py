#!/usr/bin/env python3
"""RV-1 r3 — join every round-3 c1 probe envelope to my independent
source recomputation, keyed by bytecode sha256, and diff the selector sets.

Inputs: /var/tmp/rv1-r3/out/r3-recompute-*.txt  (PLANTED_SET_JSON lines)
        $W/**/probe*.json                        (REA sealed envelopes)
"""
import glob
import json
import os
import sys

R = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
W = os.path.join(R, ".ufo/waves/arc3-loop1-round3/claims/c1")
OUT = "/var/tmp/rv1-r3/out"


def norm(s):
    return str(s).replace("0x", "").lower()


recompute = {}
for f in (glob.glob(os.path.join(OUT, "*.txt")) + glob.glob(os.path.join(OUT, "final", "*.txt"))):
    for line in open(f):
        if line.startswith("# PLANTED_SET_JSON "):
            d = json.loads(line[len("# PLANTED_SET_JSON "):])
            label = os.path.basename(f)[:-4]
            if label.startswith("r3-recompute-"):
                label = label[len("r3-recompute-"):]
            recompute[label] = d
by_bc = {}
for label, d in recompute.items():
    by_bc.setdefault(d["deployed_sha256"], []).append(label)

probes = sorted(glob.glob(os.path.join(W, "**", "*.json"), recursive=True))
rows = []
for p in probes:
    base = os.path.basename(p)
    if "probe" not in base and "leg" not in base:
        continue
    try:
        d = json.load(open(p))
    except Exception:
        continue
    nr = d.get("normalized_result") if isinstance(d, dict) else None
    if not isinstance(nr, dict) or "functions" not in nr:
        continue
    sels = sorted({norm(f.get("selector", "")) for f in nr["functions"] if f.get("selector")})
    bc_sha = nr.get("bytecode", {}).get("sha256", "")
    art = nr.get("artifact", {})
    prov = d.get("provider", {})
    subj_path = d.get("subject", {}).get("local_path", "")
    rows.append({
        "probe": os.path.relpath(p, W),
        "evidence_id": d.get("evidence_id", ""),
        "provider": f"{prov.get('id','')}/{prov.get('version','')}",
        "subject": os.path.basename(subj_path) if subj_path else "",
        "bc_sha": bc_sha,
        "art_sha": art.get("sha256", ""),
        "sels": sels,
        "labels": by_bc.get(bc_sha, []),
    })

print(f"# probes parsed: {len(rows)}   recompute labels: {sorted(recompute)}")
print(f"# {'probe':<58} {'K':>3} {'bytecode sha':<12} {'recompute label':<22} set-match")
for r in rows:
    lab = ",".join(r["labels"]) if r["labels"] else "-"
    if r["labels"]:
        mine = set(recompute[r["labels"][0]]["selectors"])
        setmatch = "MATCH" if set(mine) == set(r["sels"]) else f"DIFF miss={sorted(set(mine)-set(r['sels']))} extra={sorted(set(r['sels'])-set(mine))}"
    else:
        setmatch = "no-recompute-match"
    print(f"  {r['probe']:<58} {len(r['sels']):>3} {r['bc_sha'][:12]:<12} {lab:<22} {setmatch}")

# detail: which recompute sets are ever unmatched
unmatched = [r for r in rows if not r["labels"]]
if unmatched:
    print("\n# probes with no byte-identical recompute (bytecode not reproduced from source):")
    for r in unmatched[:20]:
        print(f"  {r['probe']}  bc_sha={r['bc_sha'][:16]} K={len(r['sels'])} subject={r['subject']}")