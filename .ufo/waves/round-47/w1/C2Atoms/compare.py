#!/usr/bin/env python3
"""Per-atom verdict comparison: pinned counter copy vs C2Atoms independent derivation."""
import json, os, sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
SCR = "/fast/scratch/hyaku/kaidoku-r47/C2Atoms"
CREV, REV, MYJSON = sys.argv[1], sys.argv[2], sys.argv[3]
mydata = json.load(open(MYJSON))

sys.path.insert(0, os.path.join(SCR, "counter", CREV, "tools/round-47"))
sys.path.insert(0, os.path.join(SCR, "counter", CREV, "tools/round-46"))
import record, gate

tip = gate.resolve(LANE, REV)
card = gate.show(LANE, tip, "SCORECARD.md")
files = lambda p: gate.show(LANE, tip, p)
cache = {}

def spawns(rnd):
    rnd = str(rnd)
    if rnd not in cache:
        cache[rnd] = record.dispatch_counts(files, rnd)
    return cache[rnd]

atoms = []
for rnd, text in record.sections(card):
    atoms.extend(record.collect(text, rnd, files, LANE, tip))
atoms.extend(record.collect_axes(card))

def key(cls, k, text):
    return (cls, str(k)) if cls == "axes" else (cls, str(k), text)

counter = {}
for i, a in enumerate(atoms):
    ok, detail = record.derive(a, files, LANE, tip, spawns)
    counter[key(a["class"], a["key"], a["atom"]) + (i,)] = (ok, detail)
mine = {}
for i, a in enumerate(mydata["atoms"]):
    mine[(a["class"], str(a["key"])) if a["class"] == "axes"
         else (a["class"], str(a["key"]), a["atom"])] = a["ok"]

ck = {k[:-1]: v for k, v in counter.items()}
disagree = [k for k in set(ck) & set(mine) if ck[k][0] != mine[k]]
print(json.dumps({
    "counter_rev": CREV, "card_rev": tip,
    "atoms_counter": len(ck), "atoms_mine": len(mine),
    "only_in_counter": sorted(map(str, set(ck) - set(mine))),
    "only_in_mine": sorted(map(str, set(mine) - set(ck))),
    "disagreements": [str(k) for k in disagree],
    "counter_false": sorted(f"{k[0]} {k[1]}" for k, v in ck.items() if not v[0]),
}, indent=1))
