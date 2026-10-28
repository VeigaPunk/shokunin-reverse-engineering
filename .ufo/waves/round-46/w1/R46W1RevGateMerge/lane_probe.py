#!/usr/bin/env python3
"""Lane-level receipts for seat R46W1RevGateMerge.

Measures, on the real lane repo and read-only:
  - gate.freeze_state over four candidate freeze bases against HEAD
  - the frozen attest.py / registry.py exit at the dispatch freeze
  - the landed block-23 row for R45-CL19 (the table's stated limit)
Records {cmd, exit, stdout_sha256, utc} per step.
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import time

S = os.environ["HYAKU_SCRATCH"]
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
DISPATCH_FREEZE = "31820472784284727546808acc31b3ea1e73919b"
BASES = [("dispatch", DISPATCH_FREEZE),
         ("re-freeze-1", "50862e4a"),
         ("re-freeze-2", "65678df0"),
         ("re-freeze-3", "04252247")]
REC = []
OUT = {}


def utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def run(args, cwd=None):
    r = subprocess.run(args, cwd=cwd, capture_output=True)
    REC.append({"cmd": " ".join(args), "cwd": cwd, "exit": r.returncode,
                "stdout_sha256": hashlib.sha256(r.stdout).hexdigest(),
                "stdout": r.stdout.decode("utf-8", "surrogateescape"),
                "stderr": r.stderr.decode("utf-8", "surrogateescape")[:400],
                "utc": utc()})
    return r


def main():
    spec = importlib.util.spec_from_file_location("g", os.path.join(S, "gate_frozen.py"))
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    head = run(["git", "-C", LANE, "rev-parse", "HEAD"]).stdout.decode().strip()
    OUT["lane_head_at_measure"] = head
    OUT["dispatch_freeze"] = DISPATCH_FREEZE
    OUT["freeze_state"] = {}
    for label, base in BASES:
        b = run(["git", "-C", LANE, "rev-parse", base]).stdout.decode().strip()
        code, rec = g.freeze_state(LANE, b, head)
        OUT["freeze_state"][label] = {
            "base": b, "head": head, "exit": code,
            "reason": rec.get("reason"),
            "frozen_path_changed": rec.get("frozen_path_changed"),
            "blob_changed": rec.get("blob_changed"),
            "touched": rec.get("touched"),
            "restored": rec.get("restored"),
        }
    OUT["counters"] = {}
    for name, tool in (("attest", "attest.py"), ("registry", "registry.py")):
        r = run(["python3", "-I", "-B", os.path.join(S, "frozen-tools", tool),
                 "--root", LANE, "--freeze", DISPATCH_FREEZE, "--rev", head])
        try:
            body = json.loads(r.stdout)
        except Exception:
            body = {"raw": r.stdout.decode()[:400]}
        OUT["counters"][name] = {"exit": r.returncode, "stdout_sha256":
                                 hashlib.sha256(r.stdout).hexdigest(),
                                 "reason": body.get("reason"),
                                 "has_met_target": "met_target" in body,
                                 "touched_type": type(body.get("touched")).__name__}
    # the table's stated limit, read from the commit under measurement
    r = run(["git", "-C", LANE, "show", head + ":SKILL.md"])
    lines = r.stdout.decode("utf-8", "surrogateescape").splitlines()
    rows = [(i + 1, ln) for i, ln in enumerate(lines) if "R45-CL19" in ln]
    OUT["block23_cl19_rows"] = [{"line": n, "text": t} for n, t in rows]
    r2 = run(["git", "-C", LANE, "show", head + ":tools/round-46/gate.py"])
    OUT["gate_sha_at_head"] = hashlib.sha256(r2.stdout).hexdigest()
    r3 = run(["git", "-C", LANE, "show", DISPATCH_FREEZE + ":tools/round-46/gate.py"])
    OUT["gate_sha_at_dispatch_freeze"] = hashlib.sha256(r3.stdout).hexdigest()
    r4 = run(["git", "-C", LANE, "show", head + ":tools/round-46/attest.py"])
    OUT["attest_sha_at_head"] = hashlib.sha256(r4.stdout).hexdigest()
    r5 = run(["git", "-C", LANE, "show", DISPATCH_FREEZE + ":tools/round-46/attest.py"])
    OUT["attest_sha_at_dispatch_freeze"] = hashlib.sha256(r5.stdout).hexdigest()
    # pin currently written into SKILL.md
    import re
    pins = re.findall(r"sha256:([0-9a-f]{64})", r.stdout.decode("utf-8", "surrogateescape"))
    OUT["skill_pins"] = pins
    OUT["receipts"] = REC
    p = os.path.join(S, "lane_receipts.json")
    with open(p, "w") as fh:
        json.dump(OUT, fh, indent=1, sort_keys=True)
    print(json.dumps({k: v for k, v in OUT.items() if k != "receipts"}, indent=1,
                     sort_keys=True))
    print("wrote", p)


if __name__ == "__main__":
    main()
