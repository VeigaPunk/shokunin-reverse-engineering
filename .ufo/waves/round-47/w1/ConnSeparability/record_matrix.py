#!/usr/bin/env python3
"""Round-47 causal separability recorder: every cell logged with command, exit,
stdout sha256 and UTC time. Mutates nothing; reads the scratch clone only."""
import hashlib
import json
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

S = "/fast/scratch/hyaku/kaidoku-r47/ConnSeparability"
R = os.path.join(S, os.environ.get("SEP_CLONE", "repo"))
A4 = os.environ.get("SEP_OLD_FREEZE", "1e2c3102952dc636650095643c1963c833859019")
OUT = os.path.join(S, os.environ.get("SEP_OUT", "receipts"))
os.makedirs(OUT, exist_ok=True)
ENV = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S)

states = [l.split() for l in open(os.path.join(S, os.environ.get("SEP_STATES", "states/index.txt"))).read().splitlines() if l.strip()]


def run(state, rev, claim, freeze):
    exe = "tools/round-47/exact.py" if claim == "c1" else "tools/round-47/record.py"
    argv = ["python3", "-I", "-B", exe, "--root", R, "--rev", rev]
    if claim == "c1":
        argv[4:4] = ["--freeze", freeze]
        label = f"{state}.{claim}.{'selffreeze' if freeze == rev else 'A4freeze'}"
    else:
        label = f"{state}.{claim}"
    t0 = datetime.now(timezone.utc).isoformat(timespec="seconds")
    p = subprocess.run(argv, cwd=R, capture_output=True, text=True, env=ENV)
    rec = {"state": state, "claim": claim, "rev": rev,
           "freeze": freeze if claim == "c1" else None,
           "cmd": " ".join(argv), "start_utc": t0,
           "exit": p.returncode,
           "stdout_sha256": hashlib.sha256(p.stdout.encode()).hexdigest(),
           "stderr_tail": p.stderr.strip()[-200:]}
    path = os.path.join(OUT, label + ".json")
    open(path, "w").write(p.stdout)
    try:
        d = json.loads(p.stdout)
    except ValueError:
        d = {}
    rec["failing"] = d.get("failing")
    rec["reason"] = d.get("reason")
    rec["mismatches"] = [m["atom"] + " => claimed " + json.dumps(m["derived"].get("claimed"))
                         + " derived " + json.dumps(m["derived"].get("derived"))
                         for m in (d.get("mismatches") or [])]
    rec["counter_counts"] = {k: d.get(k) for k in
                             ("rule_blocks", "marker_occurrences", "block_present",
                              "atoms", "corrections", "refs") if d.get(k) is not None}
    rec["battery"] = ({k: d["battery"].get(k) for k in
                       ("forgeries_total", "v2_green", "v3_green", "genuine_green",
                        "crash", "correction_forgeries", "forgeries_green")}
                      if isinstance(d.get("battery"), dict) else d.get("battery"))
    rec["receipt"] = path
    return rec


jobs = []
for state, rev in states:
    jobs.append((state, rev, "c1", rev))
    jobs.append((state, rev, "c1", A4))
    jobs.append((state, rev, "c2", None))
with ThreadPoolExecutor(max_workers=10) as ex:
    recs = list(ex.map(lambda j: run(*j), jobs))

order = {s: i for i, (s, _) in enumerate(states)}
recs.sort(key=lambda r: (order[r["state"]], r["claim"], r["freeze"] or ""))
with open(os.path.join(OUT, "matrix.jsonl"), "w") as fh:
    for r in recs:
        fh.write(json.dumps(r, sort_keys=True) + "\n")
rows = {}
for r in recs:
    key = r["state"]
    col = "C1/self" if r["claim"] == "c1" and r["freeze"] == r["rev"] else \
          "C1/A4" if r["claim"] == "c1" else "C2"
    rows.setdefault(key, {})[col] = r["exit"]
print("state            C1/self  C1/A4  C2")
for state, _ in states:
    v = rows[state]
    print(f"{state:<17}{v.get('C1/self')!s:>7}{v.get('C1/A4')!s:>7}{v.get('C2')!s:>4}")
print(json.dumps({r["state"] + "|" + ("C1/self" if r["claim"] == "c1" and r["freeze"] == r["rev"] else "C1/A4" if r["claim"] == "c1" else "C2"):
                  {"exit": r["exit"], "sha": r["stdout_sha256"][:12], "utc": r["start_utc"],
                   "failing": r["failing"], "mismatches": r["mismatches"]} for r in recs}, indent=1))
