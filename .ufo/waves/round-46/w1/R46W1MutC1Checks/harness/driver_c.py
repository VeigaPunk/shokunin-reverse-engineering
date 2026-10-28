#!/usr/bin/env python3
"""Same campaign, byte-set C = the live worktree instrument (c4056131, 18 cases)."""
import concurrent.futures as cf
import json
import os
import shutil
import sys

sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r46/R46W1MutC1Checks")
import driver as D  # noqa: E402

D.HEAD = os.path.join(D.S, "cur")
jobs, meta = {}, {}
d = os.path.join(D.MUT, "cur-baseline")
shutil.rmtree(d, ignore_errors=True)
os.makedirs(d)
for f in ("attest.py", "gate.py"):
    shutil.copy2(os.path.join(D.HEAD, f), os.path.join(d, f))
jobs["cur-baseline"] = d

for mid, desc, pairs in D.MUTANTS:
    if "*" not in pairs and "cur" not in pairs:
        pairs = dict(pairs, cur=pairs["head"])
    dd, hn, ho, diff = D.build("cur", mid, pairs)
    meta[f"cur-{mid}"] = {"mutant": mid, "ver": "cur", "desc": desc,
                          "sha_mutant": hn, "sha_orig": ho, "diff": diff}
    jobs[f"cur-{mid}"] = dd

res = {}
with cf.ThreadPoolExecutor(max_workers=8) as ex:
    futs = {ex.submit(D.run_selftest, p): k for k, p in jobs.items()}
    for f in cf.as_completed(futs):
        res[futs[f]] = f.result()
json.dump({"runs": res, "meta": meta}, open(os.path.join(D.REC, "summary-cur.json"), "w"),
          indent=1, sort_keys=True)

b = res["cur-baseline"]
ok = {c["case"]: c["ok"] for c in b["case_rows"]}
print(f"cur baseline exit={b['exit']} cases={b['cases']} failures={b['failures']} "
      f"sha={b['stdout_sha256']} utc={b['utc']}")
for mid, _d, _p in D.MUTANTS:
    r = res[f"cur-{mid}"]
    fl = [c["case"] for c in (r.get("case_rows") or []) if ok.get(c["case"]) and not c["ok"]]
    print(f"{mid:22s} exit={r['exit']} failures={r.get('failures')} "
          f"{'KILLED' if fl else 'SURVIVED':8s} flipped={fl} "
          f"identical={r['stdout_sha256'] == b['stdout_sha256']}")
