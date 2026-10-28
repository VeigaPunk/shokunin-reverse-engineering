import sys, os, time, json
inst, root, freeze, rev = sys.argv[1:5]
sys.path.insert(0, os.path.dirname(os.path.abspath(inst)))
sys.dont_write_bytecode = True
import gate, subprocess, tempfile, shutil
rec = []
orig_mkdtemp = tempfile.mkdtemp
t0 = time.perf_counter()
orig_run = subprocess.run
def run(*a, **k):
    s = time.perf_counter(); out = orig_run(*a, **k); rec.append((a[0][:3], time.perf_counter()-s)); return out
subprocess.run = run
def mk(*a, **k):
    p = orig_mkdtemp(*a, **k)
    rec.append((["MKDIR"], time.perf_counter()))
    return p
tempfile.mkdtemp = mk
orig_rm = shutil.rmtree
rms = []
def rm(p, *a, **k):
    s = time.perf_counter()
    try: return orig_rm(p, *a, **k)
    finally: rms.append(time.perf_counter()-s)
shutil.rmtree = rm
mod = __import__(os.path.basename(inst)[:-3])
code = mod.main(["--root", root, "--freeze", freeze, "--rev", rev])
total = time.perf_counter()-t0
git_s = sum(d for a, d in rec if a[0] == "git")
print(json.dumps({"instrument": os.path.basename(inst), "exit": code, "total_s": round(total,3),
  "git_s": round(git_s,3), "git_share": round(git_s/total,3),
  "git_calls": sum(1 for a,_ in rec if a[0]=="git"),
  "rmtree_calls": len(rms), "rmtree_s": round(sum(rms),3),
  "fixture_dirs": sum(1 for a,_ in rec if a[0]=="MKDIR")}, indent=0), file=sys.stderr)
