#!/usr/bin/env python3
"""Print the RV-7 mutation matrix compactly from the per-run JSONs."""
import json
import sys
from pathlib import Path

here = Path(sys.argv[1])
label = sys.argv[2]
order = ["clean", "M1-guard-revert", "M1a-scoped-arm-revert", "M1b-inode-arm-revert",
         "M2-coverage-revert"]
rows = []
for name in order:
    p = here / ("%s-%s.json" % (label, name))
    if not p.exists():
        rows.append((name, "MISSING", "", "", "", "", "", ""))
        continue
    d = json.loads(p.read_text())
    cl, pa, st = d["clobber"], d["partial"], d["selftest"]
    sub = d.get("coverage_subversion", {})
    subverdict = sub.get("verdict", "n/a")
    if sub.get("runs"):
        subverdict += " flag5=%d" % sub["runs"]["dup5_flag5"]["exit"]
    adj = cl["adjacent"]
    rows.append((
        name,
        d["tool_src_sha256"][:12] if "tool_src_sha256" in d else "",
        cl["verdict"],
        "%s/%s/%s" % (adj["symlink_out"], adj["relpath_abs"], adj["sidecar_scope"]),
        "live1=%d" % pa["runs"]["v2live_r1"]["exit"],
        "live1+flag5=%d%s" % (pa["runs"]["v2live_r1_flag5"]["exit"],
                              "C" if pa["runs"]["v2live_r1_flag5"]["coverage_class_present"] else "-"),
        subverdict,
        "%s %d/%d" % (st["summary"].split(":")[1].strip().split()[0], st["cases"] - len(st["failed_cases"]), st["cases"]),
    ))
print("spec                  toolsha      CL(A11)     adj same/link/rel/sidecar   D3live  D3live+flag5   dup-gate        selftest")
for r in rows:
    print("%-21s %-12s %-11s %-27s %-7s %-14s %-15s %s" % r)
for name, *_ in rows:
    p = here / ("%s-%s.json" % (label, name))
    if p.exists():
        d = json.loads(p.read_text())
        for c in d["selftest"]["failed_cases"]:
            print("  selftest FAIL [%s]: %s" % (name, c.strip()))