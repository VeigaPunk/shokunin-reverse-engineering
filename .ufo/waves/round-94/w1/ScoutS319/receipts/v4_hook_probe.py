import importlib.util, io, json, sys, pathlib
p = "/fast/scratch/hyaku/kaidoku-r94/ScoutS319/clone/tools/round-94/stop-boundary-repair-battery-v4.py"
spec = importlib.util.spec_from_file_location("v4", p)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print("v4 _default on bytes:", m._default(b"abc"))
try:
    m._default(object())
    print("v4 _default on object(): NO-ERROR (unexpected)")
except TypeError as e:
    print("v4 _default on object(): TypeError:", e)
# end-to-end: bytes through json.dump with v4's hook
out = io.StringIO()
json.dump({"fresh_cells": [{"output": b"abc"}]}, out, indent=1, sort_keys=True, default=m._default)
print("json.dump via v4 hook OK:", out.getvalue().strip())
# the refused fallback: str() fallback would succeed
out2 = io.StringIO()
json.dump({"x": object()}, out2, default=lambda o: str(o))
print("str() fallback succeeds (contrast):", out2.getvalue().strip()[:60])
# writer atomicity: no .tmp left, complete JSON
import tempfile, os
work = pathlib.Path("/fast/scratch/hyaku/kaidoku-r94/ScoutS319/work"); work.mkdir(parents=True, exist_ok=True)
p2 = work / "receipt.json"
m._write_json_atomic(p2, {"fresh_cells": [{"output": b"abc"}]})
print("receipt exists:", p2.exists(), "tmp exists:", (work/'receipt.json.tmp').exists())
print("reparse OK:", json.loads(p2.read_text())["fresh_cells"][0]["output"])
