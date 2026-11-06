#!/usr/bin/env python3
"""Re-author exec-leg probes so the static screen does not confound the verdict.
X1: one extra execve via an `os` alias (no FORBIDDEN token in text).
X2: one extra execveat(2) syscall via ctypes (ctypes is FORBIDDEN, so static arm
    fails by design; the evidence is the exec cell itself, read per arm)."""
import json, os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r100/MutationC1")
import driver as D

S = D.S
PR = f"{S}/pristine/upx-pe-repair.py"
RUNS = f"{S}/runs"
PRISTINE_BAT = f"{S}/pristine/pe-upx-corrupt-battery.py"

X1_NEW = ("_o = os\n\n\ndef _probe_child():\n    pid = _o.fork()\n    if pid == 0:\n"
          "        _o.execv(\"/bin/true\", [\"/bin/true\"])\n    _o.waitpid(pid, 0)\n\n\n"
          "def main(argv=None):\n    _probe_child()\n")
X2_NEW = ("import ctypes as _c\n_o = os\n\n\ndef _probe_child():\n    pid = _o.fork()\n    if pid == 0:\n"
          "        _l = _c.CDLL(None, use_errno=True)\n"
          "        _argv = (_c.c_char_p * 2)(b\"true\", None)\n"
          "        _envp = (_c.c_char_p * 1)(None)\n"
          "        _l.syscall(322, -100, b\"/bin/true\", _argv, _envp, 0)\n"
          "        os._exit(1)\n    os.waitpid(pid, 0)\n\n\n"
          "def main(argv=None):\n    _probe_child()\n")
X = {"X1b-extra-execve": ("def main(argv=None):\n", X1_NEW),
     "X2b-extra-execveat": ("def main(argv=None):\n", X2_NEW)}


def prep(name, old, new):
    run = f"{RUNS}/{name}"
    os.makedirs(run, exist_ok=True)
    clone = f"{run}/clone"
    if os.path.exists(clone):
        shutil.rmtree(clone)
    shutil.copytree(f"{S}/clone", clone, symlinks=True)
    p = f"{clone}/tools/round-100/upx-pe-repair.py"
    mut = D.apply_mut(open(PR, encoding="utf-8").read(), old, new)
    open(p, "w", encoding="utf-8").write(mut)
    subprocess.run(["git", "-C", clone, "add", "tools/round-100/upx-pe-repair.py"], check=True, capture_output=True)
    r = subprocess.run(["git", "-c", "user.name=MutationC1", "-c", "user.email=mut@scratch.invalid",
                        "-C", clone, "commit", "-q", "-m", name], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    rev = subprocess.run(["git", "-C", clone, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    return {"name": name, "kind": "probe2", "run": run, "clone": clone, "rev": rev,
            "mut_sha": D.sha_b(mut.encode()), "battery": PRISTINE_BAT}


jobs = []
for xn, (old, new) in X.items():
    j = prep(xn, old, new)
    jobs.append(dict(j, name=f"P-{xn}"))
for bn, xn in [("B8-exec-off-by1", "X1b-extra-execve"), ("B10-no-violations", "X1b-extra-execve"),
               ("B9-drop-execveat", "X2b-extra-execveat")]:
    base = dict(next(j for j in jobs if j["name"] == f"P-{xn}"))
    base["name"] = f"{bn}@{xn}"
    base["run"] = f"{RUNS}/y-{bn}-{xn}"
    base["battery"] = f"{RUNS}/{bn}/battery.py"
    jobs.append(base)

with ThreadPoolExecutor(max_workers=5) as ex:
    results = list(ex.map(D.run_one, jobs))
out = []
for r in results:
    rec = json.load(open(r["receipt"])) if os.path.exists(r["receipt"]) else {}
    ex_cell = next((c for c in rec.get("cells", []) if c["arm"] == "exec"), {})
    st_cell = next((c for c in rec.get("cells", []) if c["arm"] == "static"), {})
    row = {"name": r["name"], "exit": r["exit"], "met": r["met"], "label": r["label"],
           "exec_ok": ex_cell.get("ok"), "exec_invocations": ex_cell.get("invocations"),
           "exec_violations": ex_cell.get("violations", [])[:2], "static_ok": st_cell.get("ok")}
    out.append(row)
    print(f"{r['name']:40s} exit={r['exit']} met={r['met']} exec_ok={row['exec_ok']} "
          f"static_ok={row['static_ok']} :: {r['label'][:60]}")
    if row["exec_violations"]:
        print("    violation sample:", row["exec_violations"][0])
json.dump(out, open(f"{S}/probe/probes2.json", "w"), indent=1)
