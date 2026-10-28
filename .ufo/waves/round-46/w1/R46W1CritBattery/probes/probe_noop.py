"""Probe (a): reachability and accounting of the no-op branch.

1. apply all nine mutation functions to the landed block and to F1's token block,
   report whether any returns the block unchanged;
2. build an 8-row fixture (invalid under clause 3), call run_battery directly to
   reach the no-op branch, then call evaluate() on the same fixture.
"""
import json
import sys

sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r46/R46W1CritBattery/tools/round-46")
import attest  # noqa: E402

spec = attest.SPECS["r46"]
rep = {}

# 1. no-op survey on both valid artefacts
for label, fx in (("landed", "F2"), ("tokenised", "F1")):
    import subprocess
    skill = subprocess.run(["git", "-C", "/fast/scratch/hyaku/kaidoku-r46/R46W1CritBattery/fx/" + fx,
                            "show", "HEAD:SKILL.md"], capture_output=True, text=True).stdout
    blocks = attest.craft_blocks(skill)
    block = [b for b in blocks if spec["marker"] in b][0]
    row = {}
    for name, fn in attest.MUTATIONS:
        try:
            row[name] = "NO-OP" if fn(block, spec) == block else "changed"
        except ValueError as exc:
            row[name] = "ValueError: %s" % exc
    rep[label] = row

# 2. the no-op branch itself, on an artefact that cannot pass clause 3
import os
S = os.environ["HYAKU_SCRATCH"]
d = os.path.join(S, "fx", "F6")
rev = __import__("subprocess").run(["git", "-C", d, "rev-parse", "HEAD"],
                                  capture_output=True, text=True).stdout.strip()
scratch = os.path.join(S, "sc-noop")
os.makedirs(scratch, exist_ok=True)
bat = attest.run_battery(d, rev, "r46", scratch)
rep["eight_row_block"] = {k: v for k, v in bat.items() if k != "fixtures"}
rep["eight_row_fixtures"] = [{k: f.get(k) for k in ("name", "error", "v1_exit", "v2_exit")}
                            for f in bat.get("fixtures", [])]
code, rec = attest.evaluate(d, rev, rev, "r46", "v2", with_battery=True)
rep["eight_row_evaluate"] = {"exit": code, "battery": rec.get("battery"),
                             "failing": rec.get("failing")}
print(json.dumps(rep, indent=1, sort_keys=True))
