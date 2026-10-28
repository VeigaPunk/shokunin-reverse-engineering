#!/usr/bin/env python3
"""Headline receipts for R46W1RevScratch, each with command, exit, stdout sha256, UTC."""
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r46/R46W1RevScratch"
F = "31820472784284727546808acc31b3ea1e73919b"      # freeze named by the assignment
F2 = "50862e4a041499dd2ce0da68d10301b765bb9997"     # "authoritative" freeze (50862e4a)
F3 = "65678df0f1666e83cdeea7233bfb31ffe73ec709"     # freeze used by the L1 C2 receipt
R1 = "6e018068aaf9beb3c66ed270aeee08b300531976"
R2 = "781e19ae674225b6be0b5de56ee8574679bac0b6"
R3 = "04252247"
R4 = "1e32827b"

CASES = [
    ("c1_donothing_at_freeze", "attest.py", F, F, True),
    ("c2_donothing_at_freeze", "registry.py", F, F, True),
    ("c1_freeze_to_landing", "attest.py", F, R4, True),
    ("c2_freeze_to_landing", "registry.py", F, R4, True),
    ("c1_green_selfpinned", "attest.py", R1, R1, True),
    ("c2_green_selfpinned", "registry.py", R2, R2, True),
    ("c1_landing_pair", "attest.py", R3, R4, True),
    ("c2_landing_pair", "registry.py", R3, R4, True),
    ("c1_no_scratch_root", "attest.py", R1, R1, False),
    ("c2_no_scratch_root", "registry.py", R2, R2, False),
]


def utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main():
    base_env = {k: v for k, v in os.environ.items()
                if k not in ("HYAKU_SCRATCH", "TMPDIR")}
    good_env = dict(base_env, HYAKU_SCRATCH=S, TMPDIR=S)
    out = {"seat": "R46W1RevScratch", "utc_start": utc(),
           "python": sys.version.split()[0],
           "lane_head": subprocess.run(["git", "-C", LANE, "rev-parse", "HEAD"],
                                       capture_output=True, text=True).stdout.strip(),
           "driver_sha256": hashlib.sha256(
               open(os.path.join(LANE, "tools/round-46/attest.py"), "rb").read()).hexdigest(),
           "gate_sha256": hashlib.sha256(
               open(os.path.join(LANE, "tools/round-46/gate.py"), "rb").read()).hexdigest(),
           "registry_sha256": hashlib.sha256(
               open(os.path.join(LANE, "tools/round-46/registry.py"), "rb").read()).hexdigest(),
           "runs": []}
    for name, counter, freeze, rev, want_scratch in CASES:
        cmd = [sys.executable, "-I", "-B",
               os.path.join(LANE, "tools/round-46", counter),
               "--root", LANE, "--freeze", freeze, "--rev", rev]
        env = good_env if want_scratch else base_env
        t = utc()
        p = subprocess.run(cmd, env=env, cwd=LANE, capture_output=True, text=True,
                           timeout=600)
        rec = {"case": name, "cmd": " ".join(cmd),
               "env": "HYAKU_SCRATCH=<seat scratch>" if want_scratch else "unsetset",
               "started_utc": t, "exit": p.returncode,
               "stdout_sha256": hashlib.sha256(p.stdout.encode()).hexdigest(),
               "stderr_sha256": hashlib.sha256(p.stderr.encode()).hexdigest()}
        try:
            d = json.loads(p.stdout)
            rec["reason"] = d.get("reason")
            rec["met_target"] = d.get("met_target")
            rec["failing"] = d.get("failing")
            rec["frozen_path_changed"] = d.get("frozen_path_changed")
            b = d.get("battery") or {}
            rec["battery"] = {k: b.get(k) for k in
                              ("forgeries_total", "v1_green", "v2_green", "genuine_green",
                               "skipped")}
        except Exception:
            rec["stdout_head"] = p.stdout[:160]
            rec["stderr_head"] = p.stderr[:160]
        out["runs"].append(rec)
    # selftest case counts per freeze candidate, using that freeze's own bytes
    st = []
    for rev in (F, F2, F3):
        for counter in ("attest.py", "registry.py"):
            d = os.path.join(S, "frozen-" + rev)
            cmd = [sys.executable, "-I", "-B", os.path.join(d, counter),
                   "--root", LANE, "--freeze", rev, "--rev", rev, "--selftest"]
            p = subprocess.run(cmd, env=good_env, cwd=LANE, capture_output=True,
                               text=True, timeout=900)
            st.append({"counter": counter, "interpreter_at": rev, "cmd": " ".join(cmd),
                       "started_utc": utc(), "exit": p.returncode,
                       "stdout_sha256": hashlib.sha256(p.stdout.encode()).hexdigest(),
                       "line1": p.stdout.splitlines()[0] if p.stdout else ""})
    # the current working-tree bytes at HEAD
    for counter in ("attest.py", "registry.py"):
        cmd = [sys.executable, "-I", "-B", os.path.join(LANE, "tools/round-46", counter),
               "--root", LANE, "--freeze", R1, "--rev", R1, "--selftest"]
        p = subprocess.run(cmd, env=good_env, cwd=LANE, capture_output=True, text=True,
                           timeout=900)
        st.append({"counter": counter, "interpreter_at": "working tree",
                   "cmd": " ".join(cmd), "started_utc": utc(), "exit": p.returncode,
                   "stdout_sha256": hashlib.sha256(p.stdout.encode()).hexdigest(),
                   "line1": p.stdout.splitlines()[0] if p.stdout else ""})
    out["selftests"] = st
    out["utc_end"] = utc()
    path = os.path.join(S, "receipts.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print(path)
    for r in out["runs"]:
        print("%-26s exit=%s %s" % (r["case"], r["exit"],
                                    r.get("reason") or r.get("met_target")))
    for r in out["selftests"]:
        print("%-12s %-12s exit=%s %s" % (r["counter"], r["interpreter_at"][:12],
                                          r["exit"], r["line1"]))


if __name__ == "__main__":
    sys.exit(main())
