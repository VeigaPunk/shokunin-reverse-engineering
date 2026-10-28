"""Resolve each round-45 tool's scratch root WITHOUT touching the filesystem.

os.makedirs and tempfile.mkdtemp are replaced by recorders, so the intent is
observed and nothing is created. Import is -B (no __pycache__).
"""
import importlib.util
import json
import os
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"

seen = []


def rec_makedirs(path, *a, **k):
    seen.append({"call": "makedirs", "path": str(path)})
    return None


def rec_mkdtemp(*a, **k):
    seen.append({"call": "mkdtemp", "dir": str(k.get("dir")), "prefix": k.get("prefix")})
    return os.path.join(str(k.get("dir")), (k.get("prefix") or "") + "STUB")


os.makedirs = rec_makedirs
tempfile.mkdtemp = rec_mkdtemp


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


out = {}
env = {k: os.environ.get(k) for k in ("HYAKU_SCRATCH", "TMPDIR")}
out["env"] = env

pf = load(os.path.join(LANE, "tools/round-45/frozen-path-preflight.py"), "pf")
del seen[:]
out["preflight.scratch_root"] = pf.scratch_root()
out["preflight.calls"] = list(seen)

c1 = load(os.path.join(LANE, "tools/round-45/c1-counter.py"), "c1")
del seen[:]
out["c1.scratch_dir"] = c1.scratch_dir()
out["c1.calls"] = list(seen)

c2 = load(os.path.join(LANE, "tools/round-45/c2-counter.py"), "c2")
del seen[:]
out["c2.run_selftest_workroot"] = None
# replicate the two lines of run_selftest that pick the root (lines 173-177)
base = os.environ.get("HYAKU_SCRATCH") or os.environ.get("TMPDIR") or tempfile.gettempdir()
root = os.path.join(base, "kaidoku-r45")
out["c2.makedirs"] = root
out["c2.calls"] = list(seen)

for name, mod in (("preflight", pf), ("c1", c1), ("c2", c2)):
    ap = getattr(mod, "main", None)
    out[name + ".has_work_flag"] = None

print(json.dumps(out, indent=2, sort_keys=True))
