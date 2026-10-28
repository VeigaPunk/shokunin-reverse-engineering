import sys, os, time, json, collections
inst, root, freeze, rev = sys.argv[1:5]
sys.path.insert(0, os.path.dirname(os.path.abspath(inst)))
sys.dont_write_bytecode = True
import gate
calls = []
orig = gate.git
def timed(r, *a, **k):
    t0 = time.perf_counter()
    out = orig(r, *a, **k)
    calls.append((r, a, time.perf_counter()-t0, out.returncode))
    return out
gate.git = timed
t0 = time.perf_counter()
mod = __import__(os.path.basename(inst)[:-3])
code = mod.main(["--root", root, "--freeze", freeze, "--rev", rev])
wall = time.perf_counter()-t0
lane = sum(1 for r, *_ in calls if r == root)
fx = len(calls) - lane
secs = sum(c[2] for c in calls)
uniq = len({(r, a[0], a[1] if len(a) > 1 else "") for r, a, *_ in calls})
verbs = collections.Counter(a[0] for r, a, *_ in calls)
sys.stderr.write(json.dumps({"instrument": os.path.basename(inst), "exit": code,
  "wall_s": round(wall,3), "git_calls": len(calls), "lane_calls": lane, "fixture_calls": fx,
  "unique_calls": uniq, "repeat_ratio": round(len(calls)/max(uniq,1),2),
  "git_s": round(secs,3), "git_share": round(secs/wall,3),
  "verbs": dict(verbs)}) + "\n")
