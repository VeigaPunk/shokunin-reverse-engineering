#!/usr/bin/env python3
"""Pinned receipts for the RevC1Ids review. Every line: cmd, exit, stdout sha256, UTC."""
import hashlib
import json
import os
import subprocess
import sys
import time

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = os.environ["HYAKU_SCRATCH"]
REV = "1e2c3102952dc636650095643c1963c833859019"   # tip at review time
FREEZES = {"F1": "5017e1f7299c3a812e87e7950148f54313dd279e",
           "A1": "9018c53b16503c8d06d398b75503406508119946",
           "A2": "62e33f7dd75c8e3285967b26419842c106f6c965"}

CMDS = [
    ("c1-at-declared-freeze-A2",
     ["python3", "-I", "-B", "tools/round-47/exact.py", "--root", ".", "--freeze",
      FREEZES["A2"], "--rev", REV, "--no-battery"]),
    ("c1-at-A1-paragraph-freeze",
     ["python3", "-I", "-B", "tools/round-47/exact.py", "--root", ".", "--freeze",
      FREEZES["A1"], "--rev", REV, "--no-battery"]),
    ("c1-at-first-freeze",
     ["python3", "-I", "-B", "tools/round-47/exact.py", "--root", ".", "--freeze",
      FREEZES["F1"], "--rev", REV, "--no-battery"]),
    ("c1-do-nothing-control",
     ["python3", "-I", "-B", "tools/round-47/exact.py", "--root", ".", "--freeze",
      FREEZES["F1"], "--rev", FREEZES["F1"], "--no-battery"]),
    ("c1-self-referential-freeze-eq-rev",
     ["python3", "-I", "-B", "tools/round-47/exact.py", "--root", ".", "--freeze", REV,
      "--rev", REV, "--no-battery"]),
    ("c1-battery-at-tip",
     ["python3", "-I", "-B", "tools/round-47/exact.py", "--root", ".", "--freeze", REV,
      "--rev", REV, "--json-out", ".ufo/waves/round-47/w1/RevC1Ids/c1-battery-tip.json"]),
    ("c1-selftest-documented-form",
     ["python3", "-I", "-B", "tools/round-47/exact.py", "--selftest", "--root", ".",
      "--freeze", "0", "--rev", "0"]),
    ("c1-selftest-bare",
     ["python3", "-I", "-B", "tools/round-47/exact.py", "--selftest"]),
    ("c2-at-tip",
     ["python3", "-I", "-B", "tools/round-47/record.py", "--root", ".", "--rev", REV,
      "--json-out", ".ufo/waves/round-47/w1/RevC1Ids/c2-at-tip.json"]),
    ("c2-selftest",
     ["python3", "-I", "-B", "tools/round-47/record.py", "--selftest", "--root", ".",
      "--rev", "0"]),
    ("freeze-derivation-claims",
     ["git", "log", "--format=%H", "-1", "--", "plans/round-47-claims.md"]),
    ("post-freeze-touches",
     ["git", "log", "--format=%h %s", FREEZES["A2"] + ".." + REV, "--",
      "tools/round-47/", "plans/round-47-claims.md"]),
    ("record-py-diff-A2-to-tip",
     ["git", "diff", "--stat", FREEZES["A2"] + ".." + REV, "--", "tools/round-47/record.py"]),
    ("claims-file-has-no-A3-or-A4",
     ["git", "log", "--format=%h", FREEZES["A2"] + ".." + REV, "--", "plans/round-47-claims.md"]),
]


def main():
    env = dict(os.environ, HYAKU_SCRATCH=S, TMPDIR=S)
    out = []
    for name, cmd in CMDS:
        t = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        p = subprocess.run(cmd, cwd=LANE, capture_output=True, text=True, env=env)
        blob = (p.stdout or "") + (p.stderr or "")
        rec = {"receipt": name, "cmd": " ".join(cmd), "cwd": LANE, "utc": t,
               "exit": p.returncode, "stdout_sha256": hashlib.sha256(blob.encode()).hexdigest(),
               "stdout_bytes": len(blob)}
        if cmd[0] == "python3" and name != "c1-selftest-bare" and p.stdout.startswith("{"):
            try:
                d = json.loads(p.stdout)
                rec["reason"] = d.get("reason")
                rec["failing"] = d.get("failing")
                rec["met_target"] = d.get("met_target")
                if "battery" in d:
                    rec["battery"] = d["battery"]
            except Exception:
                pass
        if name in ("c1-selftest-documented-form", "c1-selftest-bare", "c2-selftest"):
            rec["tail"] = blob.strip().splitlines()[-1:] or [""]
        if name in ("freeze-derivation-claims", "post-freeze-touches", "record-py-diff-A2-to-tip",
                    "claims-file-has-no-A3-or-A4"):
            rec["stdout"] = blob.strip()
        out.append(rec)
        print("%-34s exit=%d %s" % (name, p.returncode, rec.get("reason") or rec.get("tail") or ""))
    with open(os.path.join(S, "receipts.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
