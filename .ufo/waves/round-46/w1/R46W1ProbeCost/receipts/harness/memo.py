import sys, os, time, json
inst, root, freeze, rev = sys.argv[1:5]
sys.path.insert(0, os.path.dirname(os.path.abspath(inst)))
sys.dont_write_bytecode = True
import gate
mode = os.environ.get("MEMO", "0")
calls = {"n": 0}
orig_show = gate.show
if mode == "1":
    cache = {}
    def show(r, rv, p):
        k = (r, rv, p)
        if k in cache:
            return cache[k]
        calls["n"] += 1
        cache[k] = orig_show(r, rv, p)
        return cache[k]
    gate.show = show
else:
    def show(r, rv, p):
        calls["n"] += 1
        return orig_show(r, rv, p)
    gate.show = show
t0 = time.perf_counter()
mod = __import__(os.path.basename(inst)[:-3])
code = mod.main(["--root", root, "--freeze", freeze, "--rev", rev])
wall = time.perf_counter() - t0
sys.stderr.write(json.dumps({"instrument": os.path.basename(inst), "memo": mode,
  "exit": code, "wall_s": round(wall, 3), "show_calls": calls["n"]}) + "\n")
