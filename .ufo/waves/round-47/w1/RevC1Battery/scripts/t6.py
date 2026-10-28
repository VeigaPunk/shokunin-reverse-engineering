import json, os, sys, hashlib, subprocess
sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r47/RevC1Battery")
import attack as A

base = A.show(A.FREEZE, A.SELF)
draft = open(A.DRAFT).read()
blk = A.block_of(draft)
# one defect class only: four rows, each naming exactly one id, CL2 twice and CL3 dropped
dup = blk.replace("| R46-CL3 a row claims a routed id another row already addresses",
                  "| R46-CL2 a row claims a routed id another row already addresses", 1)
assert dup != blk and dup.count("| R46-CL2") == 2
cases = {"T6a-dup-id-block-real-counter": base,
         "T6b-dup-id-block-clause4-deleted": A.build_cases(base)["T3-clause4-deleted"][0]}
out = {}
for tag, src in cases.items():
    lane, f1, f2 = A.build_lane(tag, src, block=dup)
    rec = A.counter(tag, lane, f1, f2)
    out[tag] = A.summary(rec)
    s = out[tag]
    print(tag, "exit=%s" % s["exit"], "failing=%s" % (s["failing"] or s["reason"]),
          s["battery"], flush=True)
json.dump(out, open("runs/summary-T6.json", "w"), indent=1)
