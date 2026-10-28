#!/usr/bin/env python3
"""Seat C1Ids — the same clause-4 fixtures scored under the ported v2 profile.

v2 (round-46 semantics) accepts a routed id that appears in some row and does not require
the four ids once each; this run measures the hole the v3 clause-4 arm closes.
"""
import hashlib
import json
import os
import subprocess
import sys
import time

S = "/fast/scratch/hyaku/kaidoku-r47/C1Ids"
COUNTER = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-47/exact.py"
CASES = ["dup-id", "multi-id-cell", "id-in-hole-cell", "permute-ids",
         "landed-worktree-draft"]


def main():
    env = dict(os.environ, HYAKU_SCRATCH=os.path.join(S, "scratch"),
               TMPDIR=os.path.join(S, "scratch"))
    os.makedirs(env["HYAKU_SCRATCH"], exist_ok=True)
    out = []
    for name in CASES:
        d = os.path.join(S, "fx", name)
        rev = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                             capture_output=True, text=True).stdout.strip()
        assert os.path.realpath(subprocess.run(
            ["git", "-C", d, "rev-parse", "--show-toplevel"],
            capture_output=True, text=True).stdout.strip()) == os.path.realpath(d)
        cmd = [sys.executable, "-I", "-B", COUNTER, "--root", d, "--freeze", rev,
               "--rev", rev, "--profile", "v2", "--json-out", ".ufo/v2-%s.json" % name]
        t = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        r = subprocess.run(cmd, cwd=d, capture_output=True, text=True, env=env)
        rec = {"case": name, "profile": "v2", "fixture": d, "rev": rev, "utc": t,
               "cmd": " ".join(cmd), "exit": r.returncode,
               "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
               "stderr": r.stderr[-300:] if r.stderr else ""}
        try:
            rec.update(json.loads(r.stdout))
        except ValueError:
            rec["stdout_head"] = r.stdout[:300]
        out.append(rec)
        print("%-26s v2 exit=%s failing=%s" % (name, rec["exit"],
              json.dumps(rec.get("failing"))[:260]))
    with open(os.path.join(S, "clause4-v2-receipts.json"), "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
