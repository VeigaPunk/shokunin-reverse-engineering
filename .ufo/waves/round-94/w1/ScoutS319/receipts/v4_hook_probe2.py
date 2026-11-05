import importlib.util, json, pathlib, sys
p = "/fast/scratch/hyaku/kaidoku-r94/ScoutS319/clone/tools/round-94/stop-boundary-repair-battery-v4.py"
spec = importlib.util.spec_from_file_location("v4", p)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
work = pathlib.Path("/fast/scratch/hyaku/kaidoku-r94/ScoutS319/work"); work.mkdir(parents=True, exist_ok=True)
p2 = work / "receipt.json"
m.write_receipt(str(p2), {"fresh_cells": [{"output": b"abc"}]})
print("receipt exists:", p2.exists(), "| tmp left:", (work/'receipt.json.tmp').exists())
print("reparse:", json.loads(p2.read_text())["fresh_cells"][0]["output"])
# failure path: unknown type -> no receipt file, no tmp left
p3 = work / "receipt_bad.json"
try:
    m.write_receipt(str(p3), {"x": object()})
    print("write_receipt unknown type: NO-ERROR (unexpected)")
except TypeError as e:
    print("write_receipt unknown type: TypeError:", e)
print("bad receipt exists:", p3.exists(), "| bad tmp left:", (work/'receipt_bad.json.tmp').exists())
