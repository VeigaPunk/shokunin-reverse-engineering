#!/usr/bin/env python3
"""ExecReproC1 — compare repro receipts against L1/pre reference receipts."""
import json

W = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-99/w1/ExecReproC1"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
PAIRS = [
    ("B0", LANE + "/.ufo/waves/round-99/pre/c1-do-nothing-at-base.json", W + "/c1-at-B0.repro.json"),
    ("A", LANE + "/.ufo/waves/round-99/l1/scores/c1-at-64cc3e10c5d615c6454570674a265b7290b8919c.json", W + "/c1-at-A.repro.json"),
    ("Bk", LANE + "/.ufo/waves/round-99/l1/scores/c1-at-c19d57cd2e65a036478b9e78f6c5397dedfb2bcb.json", W + "/c1-at-Bk.repro.json"),
]
FIELDS = ["label", "mismatches", "exit", "met", "rev", "counter_sha256"]

out = {}
for tag, ref_path, mine_path in PAIRS:
    with open(ref_path) as fh:
        ref = json.load(fh)
    with open(mine_path) as fh:
        mine = json.load(fh)
    diffs = {f: [ref.get(f), mine.get(f)] for f in FIELDS if ref.get(f) != mine.get(f)}
    out[tag] = {
        "reference": ref_path,
        "agreement": not diffs,
        "differing_fields": diffs,
        "label_reference": ref.get("label"),
        "label_repro": mine.get("label"),
    }
    print(tag, "AGREE" if not diffs else "DIFFER " + json.dumps(diffs, sort_keys=True))
with open(W + "/compare.json", "w") as fh:
    json.dump(out, fh, indent=1)
