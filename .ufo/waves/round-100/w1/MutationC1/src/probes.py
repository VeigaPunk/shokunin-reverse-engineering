#!/usr/bin/env python3
"""Probes for survivors. (a) crafted-layout inputs exercising repair()'s own
compressed-data bound check, scored directly against the true candidate and
R10/R12/R14. (b) harmless-defect candidates X1..X5 (true candidate + one
change each), scored by the pristine battery and by the battery mutant that
survived on the true candidate."""
import json, math, os, shutil, struct, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r100/MutationC1")
import driver as D

S = D.S
PR = f"{S}/pristine/upx-pe-repair.py"
RUNS = f"{S}/runs"
os.makedirs(f"{S}/probe", exist_ok=True)

# ---------- (a) crafted layout ----------
src = f"{RUNS}/BASELINE/work/t32.upx"
b0 = bytearray(open(src, "rb").read())
pe = struct.unpack_from("<I", b0, 0x3C)[0]
n = struct.unpack_from("<H", b0, pe + 6)[0]
opt = struct.unpack_from("<H", b0, pe + 20)[0]
st = pe + 24 + opt
i = b0.find(b"UPX!")
c_len = struct.unpack_from("<I", b0, i + 20)[0]
cs = i + 32
last = st + 40 * (n - 1)
struct.pack_into("<I", b0, last + 16, 0)   # SizeOfRawData = 0
struct.pack_into("<I", b0, last + 20, 0)   # PointerToRawData = 0
crafted = {"eq": bytes(b0[:cs + c_len]), "minus1": bytes(b0[:cs + c_len - 1])}
print("t32 sections", n, "PackHeader", i, "cs", cs, "c_len", c_len, "file", len(b0))

cands = {"true": PR,
         "R10": f"{RUNS}/R10-bound-ge/clone/tools/round-100/upx-pe-repair.py",
         "R12": f"{RUNS}/R12-trunc-token/clone/tools/round-100/upx-pe-repair.py",
         "R14": f"{RUNS}/R14-clamp-len/clone/tools/round-100/upx-pe-repair.py"}
crafted_rows = []
for cname, cpath in cands.items():
    for iname, data in crafted.items():
        inp = f"{S}/probe/crafted-{iname}.in"
        out = f"{S}/probe/crafted-{iname}-{cname}.out"
        open(inp, "wb").write(data)
        if os.path.exists(out):
            os.unlink(out)
        p = subprocess.run([sys.executable, "-I", "-B", cpath, "--in", inp, "--out", out],
                           capture_output=True, text=True)
        crafted_rows.append({"cand": cname, "input": iname, "len": len(data), "rc": p.returncode,
                             "out_written": os.path.exists(out), "msg": (p.stdout + p.stderr).strip()[-160:]})
        print(f"crafted {iname:7s} len={len(data)} cand={cname:5s} rc={p.returncode} "
              f"out={os.path.exists(out)} :: {(p.stdout+p.stderr).strip()[-120:]}")

# ---------- (b) harmless-defect candidates ----------
X = {}
X["X1-extra-execve"] = ("def main(argv=None):\n",
    "def _probe_exec():\n    pid = os.fork()\n    if pid == 0:\n"
    "        os.execv(\"/bin/true\", [\"/bin/true\"])\n    os.waitpid(pid, 0)\n\n\n"
    "def main(argv=None):\n    _probe_exec()\n")
X["X2-extra-execveat"] = ("def main(argv=None):\n",
    "def _probe_exec():\n    pid = os.fork()\n    if pid == 0:\n"
    "        fd = os.open(\"/\", os.O_RDONLY)\n"
    "        os.execveat(fd, \"bin/true\", [\"true\"], os.environ)\n    os.waitpid(pid, 0)\n\n\n"
    "def main(argv=None):\n    _probe_exec()\n")
X["X3-write-then-refuse"] = ("    except (Refuse, struct.error) as e:\n        return refuse(",
    "    except (Refuse, struct.error) as e:\n        if str(e).startswith(\"checksum\"):\n"
    "            with open(a.out, \"wb\") as fh:\n                fh.write(data)\n"
    "        return refuse(")
X["X4-uncaught-checksum"] = ('raise Refuse("checksum', 'raise RuntimeError("checksum')
X["X5-integrity-check-token"] = ('"checksum: adler32 of compressed data',
                                  '"integrity check: adler32 of compressed data')

def prep(name, old, new):
    run = f"{RUNS}/{name}"
    os.makedirs(run, exist_ok=True)
    clone = f"{run}/clone"
    shutil.copytree(f"{S}/clone", clone, symlinks=True)
    p = f"{clone}/tools/round-100/upx-pe-repair.py"
    text = open(PR, encoding="utf-8").read()
    mut = D.apply_mut(text, old, new)
    open(p, "w", encoding="utf-8").write(mut)
    subprocess.run(["git", "-C", clone, "add", "tools/round-100/upx-pe-repair.py"], check=True, capture_output=True)
    r = subprocess.run(["git", "-c", "user.name=MutationC1", "-c", "user.email=mut@scratch.invalid",
                        "-C", clone, "commit", "-q", "-m", name], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    rev = subprocess.run(["git", "-C", clone, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    return {"name": name, "kind": "probe-candidate", "run": run, "clone": clone, "rev": rev,
            "mut_sha": D.sha_b(mut.encode()), "battery": f"{RUNS}/BASELINE/../../pristine/pe-upx-corrupt-battery.py"}

PRISTINE_BAT = f"{S}/pristine/pe-upx-corrupt-battery.py"
jobs = []
for xn, (old, new) in X.items():
    j = prep(xn, old, new)
    j["battery"] = PRISTINE_BAT
    jobs.append(dict(j, name=f"P-{xn}"))  # pristine battery on the probe candidate
    pass
xclones = {xn: f"{RUNS}/{xn}" for xn in X}
cross = [("B4-rc-neq-0", "X4-uncaught-checksum"), ("B5-token-broader", "X5-integrity-check-token"),
         ("B6-drop-outfile", "X3-write-then-refuse"), ("B8-exec-off-by1", "X1-extra-execve"),
         ("B9-drop-execveat", "X2-extra-execveat"), ("B10-no-violations", "X1-extra-execve"),
         ("B13-corrupt-ctr", "X5-integrity-check-token"), ("B13-corrupt-ctr", "X3-write-then-refuse")]
for bn, xn in cross:
    base = dict(jobs[[j["name"] for j in jobs].index(f"P-{xn}")])
    base["name"] = f"{bn}@{xn}"
    base["run"] = f"{RUNS}/x-{bn}-{xn}"
    base["battery"] = f"{RUNS}/{bn}/battery.py"
    jobs.append(base)

with ThreadPoolExecutor(max_workers=8) as ex:
    results = list(ex.map(D.run_one, jobs))
for r in results:
    print(f"{r['name']:46s} exit={r['exit']} met={r['met']} :: {r['label'][:150]}")

# B11 kill probability: its drawn set differs from the true set by one byte at each end
cells = json.load(open(f"{RUNS}/BASELINE/receipt.json"))["cells"]
cl = {}
for c in cells:
    if c["arm"] == "corrupt":
        cl[c["carrier"]] = c["c_len"]
p_kill = sum(4 / v for v in cl.values())  # 4 corrupt cells per carrier; kill only if off == cstart-1
print("B11 per-run kill probability (sum 4/c_len):", round(p_kill, 6), "carriers:", len(cl))
json.dump({"crafted": crafted_rows, "probe_results": results,
           "B11_kill_prob": p_kill, "c_len": cl},
          open(f"{S}/probe/probes.json", "w"), indent=1)
