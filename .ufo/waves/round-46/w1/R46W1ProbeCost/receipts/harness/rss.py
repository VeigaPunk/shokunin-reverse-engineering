import sys, os, time, json, resource
inst, root, freeze, rev = sys.argv[1:5]
sys.path.insert(0, os.path.dirname(os.path.abspath(inst)))
sys.dont_write_bytecode = True
t0=time.perf_counter()
mod = __import__(os.path.basename(inst)[:-3])
code = mod.main(["--root", root, "--freeze", freeze, "--rev", rev])
w=time.perf_counter()-t0
self_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
kids_kb = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
sys.stderr.write(json.dumps({"instrument": os.path.basename(inst), "exit": code,
  "wall_s": round(w,3), "rss_python_self_kb": self_kb, "rss_max_child_kb": kids_kb})+"\n")
