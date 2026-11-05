#!/usr/bin/env python3
"""SentinelWrite symlink/path fixture for write_receipt (round-94 v4 writer).

Cases:
  A  symlink pre-existing at <json-out>.tmp  -> does the write follow the link?
  B  symlink pre-existing at <json-out>      -> does os.replace follow or replace?
  C  traversal path (../escape.json)          -> is it sanitized?
  D  relative path                            -> lands relative to cwd
  E  json-out in a nonexistent directory      -> complete-JSON-or-absent behavior
"""
import importlib.util
import json
import os
import sys

V4 = "/fast/scratch/hyaku/kaidoku-r94/SentinelWrite/clone/tools/round-94/stop-boundary-repair-battery-v4.py"
WORK = "/fast/scratch/hyaku/kaidoku-r94/SentinelWrite/fixture"

spec = importlib.util.spec_from_file_location("v4mod", V4)
v4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v4)

os.makedirs(WORK, exist_ok=True)
os.chdir(WORK)  # cwd for the relative/traversal cases
results = []


def reset():
    for n in ("victimA", "victimB", "outA.json", "outA.json.tmp", "outB.json",
              "escape.json", "rel-out.json", "rel-out.json.tmp", "missing/out.json"):
        p = os.path.join(WORK, n)
        if os.path.islink(p) or os.path.isfile(p):
            os.remove(p)


def state(p):
    if os.path.islink(p):
        return f"symlink -> {os.readlink(p)}"
    if os.path.isfile(p):
        return f"regular file size={os.path.getsize(p)}"
    return "absent"


# --- Case A: attacker-controlled symlink at <json-out>.tmp
reset()
open("victimA", "w").write("VICTIM-A-ORIGINAL")
os.symlink(os.path.join(WORK, "victimA"), "outA.json.tmp")
receipt = {"label": "sentinel-case-A", "fresh_cells": [{"output": b"ab", "rc": 0}]}
v4.write_receipt("outA.json", receipt)
results.append(("A tmp-symlink", {
    "victimA_after": open("victimA").read()[:60],
    "outA_json": state("outA.json"),
    "outA_json_tmp": state("outA.json.tmp"),
}))

# --- Case B: symlink pre-existing at <json-out> itself
reset()
open("victimB", "w").write("VICTIM-B-ORIGINAL")
os.symlink(os.path.join(WORK, "victimB"), "outB.json")
v4.write_receipt("outB.json", receipt)
results.append(("B dst-symlink", {
    "victimB_after": open("victimB").read()[:60],
    "outB_json": state("outB.json"),
    "victimB_is_still_link_target": os.path.isfile("victimB"),
}))

# --- Case C: traversal path
reset()
v4.write_receipt(os.path.join("..", "escape.json"), receipt)
results.append(("C traversal", {
    "escape_above_work": os.path.isfile(os.path.join(WORK, "..", "escape.json")),
}))

# --- Case D: plain relative path
reset()
v4.write_receipt("rel-out.json", receipt)
results.append(("D relative", {"rel_out_in_cwd": os.path.isfile("rel-out.json")}))

# --- Case E: json-out inside a nonexistent directory
reset()
try:
    v4.write_receipt(os.path.join("missing", "out.json"), receipt)
    raised = "no-raise"
except OSError as exc:
    raised = exc.__class__.__name__
results.append(("E missing-dir", {
    "raised": raised,
    "out": state(os.path.join("missing", "out.json")),
    "tmp": state(os.path.join("missing", "out.json.tmp")),
}))

for name, detail in results:
    print(f"== {name}")
    for k, v in detail.items():
        print(f"   {k}: {v}")

print(json.dumps({n: d for n, d in results}, indent=1))
