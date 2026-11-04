#!/usr/bin/env python3
"""Anchor census for round-84 mutants table (read-only)."""
import json, subprocess, hashlib, sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = "e0de2088a7bddc16305357f90ac7e889fa0a0d11"
BASE = "043b89a25241710a68b45526c3287fb3c8d907c3"

table = json.load(open(f"{REPO}/.ufo/waves/round-84/mutants.json"))
mutants = table["mutants"]

def blob(rev, path):
    return subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"],
                          capture_output=True, check=True).stdout

targets = sorted({m["target"] for m in mutants})
blobs = {}
print("== target blob sha256 (rev %s) ==" % REV)
for t in targets:
    b = blob(REV, t)
    blobs[t] = b
    bb = blob(BASE, t)
    print(f"{t}\n  sha256_rev  = {hashlib.sha256(b).hexdigest()}\n  sha256_base = {hashlib.sha256(bb).hexdigest()}\n  identical   = {b == bb}\n  bytes       = {len(b)}")

print("\n== anchor census ==")
rows = []
for m in mutants:
    edits = m.get("edits") or [{"find": m["find"], "replace": m["replace"]}]
    tgt = m["target"]
    text = blobs[tgt].decode()
    for i, e in enumerate(edits):
        find = e["find"]
        occ = []
        start = 0
        while True:
            k = text.find(find, start)
            if k < 0:
                break
            occ.append(k)
            start = k + 1
        claimed = m.get("anchor_occurrences")
        rows.append(dict(id=m["id"], target=tgt, edit_index=i, occurrences=len(occ),
                         offsets=occ, declared_occurrences=claimed,
                         declared_case=m["declared_case"], find=find,
                         replace=e["replace"]))
        print(f"{m['id']:20s} edit[{i}] target={tgt}")
        print(f"    find        : {find!r}")
        print(f"    occurrences : {len(occ)} (declared anchor_occurrences={claimed})")
        print(f"    offsets     : {occ}")
        print(f"    declared_case: {m['declared_case']}")

json.dump(rows, open("/fast/scratch/hyaku/kaidoku-r84/ScoutLoci/anchors.json", "w"), indent=1)

bad = [r for r in rows if r["occurrences"] != 1]
print(f"\nANCHORS NOT EXACTLY ONCE: {len(bad)}")
for r in bad:
    print("  ", r["id"], r["edit_index"], r["occurrences"], r["offsets"])
