import sys, os, time, json
inst = sys.argv[1]; root = sys.argv[2]; freeze = sys.argv[3]; rev = sys.argv[4]
sys.path.insert(0, os.path.dirname(os.path.abspath(inst)))
sys.dont_write_bytecode = True
import gate
stats = {"calls":0, "secs":0.0, "by_verb":{}}
orig = gate.git
def timed(r, *a, **k):
    t0 = time.perf_counter()
    try:
        return orig(r, *a, **k)
    finally:
        dt = time.perf_counter()-t0
        stats["calls"] += 1; stats["secs"] += dt
        v = next((x for x in a if not x.startswith("-")), "?")
        d = stats["by_verb"].setdefault(v, [0,0.0]); d[0]+=1; d[1]+=dt
gate.git = timed
t0 = time.perf_counter()
mod = __import__(os.path.basename(inst)[:-3])
code = mod.main(["--root", root, "--freeze", freeze, "--rev", rev])
wall = time.perf_counter()-t0
sys.stderr.write(json.dumps({"instrument": os.path.basename(inst), "exit": code, "wall_s": round(wall,3),
    "git_calls": stats["calls"], "git_s": round(stats["secs"],3),
    "git_share": round(stats["secs"]/wall,3),
    "by_verb": {k: [v[0], round(v[1],3)] for k,v in sorted(stats["by_verb"].items(), key=lambda kv:-kv[1][1])},
    "python_s": round(wall-stats["secs"],3)})+"\n")
