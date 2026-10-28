#!/usr/bin/env python3
"""Freeze-identity probes on the real lane, captured as citable receipts."""
import hashlib
import json
import os
import subprocess
import datetime

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r46/R46W1ExecGap"
os.environ["TMPDIR"] = S
os.environ["HYAKU_SCRATCH"] = S
FREEZE = "31820472784284727546808acc31b3ea1e73919b"
FREEZE_MID = "50862e4a041499dd2ce0da68d10301b765bb9997"
AUTHORITATIVE = "65678df0f1666e83cdeea7233bfb31ffe73ec709"


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=S, timeout=900)
    return {"cmd": " ".join(cmd), "exit": p.returncode,
            "stdout_sha256": hashlib.sha256(p.stdout.encode()).hexdigest(),
            "stdout": p.stdout, "stderr_tail": p.stderr[-500:], "utc": utc()}


head = subprocess.run(["git", "-C", LANE, "rev-parse", "HEAD"],
                      capture_output=True, text=True).stdout.strip()
out = {"lane": LANE, "head_at_probe": head, "head_utc": utc(),
       "freeze_per_claims_file": FREEZE,
       "freeze_per_commit_message": AUTHORITATIVE}

out["re_derive_claims"] = run(["git", "-C", LANE, "log", "--format=%H", "-1", "--",
                               "plans/round-46-claims.md"])
out["re_derive_tools"] = run(["git", "-C", LANE, "log", "--format=%H", "-1", "--",
                              "tools/round-46/"])
out["post_freeze_log"] = run(["git", "-C", LANE, "log", "--format=%H %ci %s",
                              FREEZE + ".." + head])
out["frozen_scope_touches"] = run(
    ["git", "-C", LANE, "log", "-m", "--diff-merges=first-parent", "--name-status",
     "--format=%H", FREEZE + ".." + head, "--", "plans/round-46-claims.md",
     "tools/round-46/"])
out["diffstat_freeze_head"] = run(
    ["git", "-C", LANE, "diff", "--stat", FREEZE + ".." + head, "--",
     "plans/round-46-claims.md", "tools/round-46/"])
out["sha256_frozen_bytes"] = run(
    ["git", "-C", LANE, "show", FREEZE + ":tools/round-46/attest.py"])
for p in ("attest.py", "gate.py", "registry.py"):
    a = subprocess.run(["git", "-C", LANE, "show", f"{FREEZE}:tools/round-46/{p}"],
                       capture_output=True).stdout
    b = subprocess.run(["git", "-C", LANE, "show", f"HEAD:tools/round-46/{p}"],
                       capture_output=True).stdout
    out.setdefault("frozen_byte_sha256", {})[p] = {
        "at_freeze": hashlib.sha256(a).hexdigest(),
        "at_head_probe": hashlib.sha256(b).hexdigest()}

att_free = os.path.join(S, "bin", "r46-freeze", "attest.py")
att_head = os.path.join(S, "bin", "r46-head", "attest.py")
out["probes"] = {
    "freeze_bytes_3182047_rev_head": run(
        ["/usr/bin/python3", "-I", "-B", att_free, "--root", LANE, "--freeze", FREEZE,
         "--rev", head, "--no-battery"]),
    "head_bytes_3182047_rev_head": run(
        ["/usr/bin/python3", "-I", "-B", att_head, "--root", LANE, "--freeze", FREEZE,
         "--rev", head, "--no-battery"]),
    "head_bytes_50862e4a_rev_head": run(
        ["/usr/bin/python3", "-I", "-B", att_head, "--root", LANE, "--freeze", FREEZE_MID,
         "--rev", head, "--no-battery"]),
    "head_bytes_65678df0_rev_head": run(
        ["/usr/bin/python3", "-I", "-B", att_head, "--root", LANE,
         "--freeze", AUTHORITATIVE, "--rev", head, "--no-battery"]),
}

with open(os.path.join(S, "freeze-probes.json"), "w") as fh:
    json.dump(out, fh, indent=1)
for k, v in out["probes"].items():
    print(k, "exit", v["exit"], "sha", v["stdout_sha256"][:12])
print("head", head)
print("claims->", out["re_derive_claims"]["stdout"].strip())
print("tools->", out["re_derive_tools"]["stdout"].strip())
print(out["frozen_byte_sha256"])
