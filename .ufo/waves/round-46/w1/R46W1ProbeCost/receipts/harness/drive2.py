import sys, os, time, json, threading, shutil, subprocess
inst, root, freeze, rev = sys.argv[1:5]
sys.path.insert(0, os.path.dirname(os.path.abspath(inst)))
sys.dont_write_bytecode = True
import gate
peak = {"bytes": 0, "files": 0, "dirs": 0, "t": None}
fixtures = []
stop = threading.Event()
def du(p):
    tot = files = dirs = 0
    for dp, dn, fn in os.walk(p):
        dirs += 1
        for f in fn:
            try:
                tot += os.lstat(os.path.join(dp, f)).st_size
                files += 1
            except OSError:
                pass
    return tot, files, dirs
def sampler(base):
    while not stop.is_set():
        for name in os.listdir(base):
            p = os.path.join(base, name)
            b, f, d = du(p)
            if b > peak["bytes"]:
                peak.update({"bytes": b, "files": f, "dirs": d, "t": time.time()})
        time.sleep(0.002)
orig_rm = shutil.rmtree
def rm(p, *a, **k):
    if os.path.isdir(p):
        fixtures.append({"path": os.path.basename(p), "bytes": du(p)[0], "files": du(p)[1]})
    return orig_rm(p, *a, **k)
shutil.rmtree = rm
base = os.environ["HYAKU_SCRATCH"]
th = threading.Thread(target=sampler, args=(base,), daemon=True); th.start()
t0 = time.perf_counter()
mod = __import__(os.path.basename(inst)[:-3])
code = mod.main(["--root", root, "--freeze", freeze, "--rev", rev])
wall = time.perf_counter() - t0
stop.set(); th.join(timeout=1)
sys.stderr.write(json.dumps({"instrument": os.path.basename(inst), "exit": code,
  "wall_s": round(wall, 3), "peak_bytes": peak["bytes"], "peak_files": peak["files"],
  "fixture_count": len(fixtures),
  "fixture_bytes_min_max": [min((f["bytes"] for f in fixtures), default=0), max((f["bytes"] for f in fixtures), default=0)],
  "fixture_bytes_total": sum(f["bytes"] for f in fixtures),
  "leftover": sorted(os.listdir(base))}) + "\n")
