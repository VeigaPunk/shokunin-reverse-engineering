#!/usr/bin/env python3
"""Lane admissibility probes: does the frozen_path_changed arm admit the landing rev?"""
import hashlib
import json
import os
import subprocess
import datetime

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r46/R46W1ExecGap"
os.environ["TMPDIR"] = S
os.environ["HYAKU_SCRATCH"] = S
DECLARED = "65678df0f1666e83cdeea7233bfb31ffe73ec709"
LANDING = "0425224756791b414454df28a9abf93dcdf154ce"


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=S, timeout=900)
    return {"cmd": " ".join(cmd), "exit": p.returncode,
            "stdout_sha256": hashlib.sha256(p.stdout.encode()).hexdigest(),
            "stdout": p.stdout[:3000], "stderr_tail": p.stderr[-400:], "utc": utc()}


head = subprocess.run(["git", "-C", LANE, "rev-parse", "HEAD"],
                      capture_output=True, text=True).stdout.strip()
attest = os.path.join(S, "bin", "r46-head", "attest.py")
regdir = os.path.join(S, "bin", "r46-head")
out = {"head_at_probe": head, "utc": utc(), "declared_freeze": DECLARED,
       "landing_commit": LANDING, "probes": {}}
for label, tool, rev in (
    ("attest_declared_landing", attest, LANDING),
    ("attest_declared_head", attest, head),
    ("registry_declared_landing", os.path.join(regdir, "registry.py"), LANDING),
    ("registry_declared_head", os.path.join(regdir, "registry.py"), head),
):
    out["probes"][label] = run(
        ["/usr/bin/python3", "-I", "-B", tool, "--root", LANE, "--freeze", DECLARED,
         "--rev", rev, "--no-battery"])

# the registry bytes whose edit the arm catches
for name, ref in (("registry_at_declared_freeze", DECLARED),
                  ("registry_at_F4", LANDING),
                  ("registry_at_head", head)):
    body = subprocess.run(["git", "-C", LANE, "show", f"{ref}:tools/round-46/registry.py"],
                          capture_output=True).stdout
    out.setdefault("registry_sha256", {})[name] = hashlib.sha256(body).hexdigest()

with open(os.path.join(S, "lane-admissibility.json"), "w") as fh:
    json.dump(out, fh, indent=1)
for k, v in out["probes"].items():
    print(k, "exit", v["exit"], "sha", v["stdout_sha256"][:12])
print(out["registry_sha256"])
print("head", head)
