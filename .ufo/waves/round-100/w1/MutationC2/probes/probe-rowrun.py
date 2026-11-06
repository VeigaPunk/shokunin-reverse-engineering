import importlib.util, hashlib, os
S = "/fast/scratch/hyaku/kaidoku-r100/MutationC2"
CL = S + "/fixt/clone"
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
def sha(p): return hashlib.sha256(open(os.path.join(CL, p), "rb").read()).hexdigest()
mods = {"base": S + "/orig.py"}
for i in ["M16", "M17", "M18", "M19", "M22", "M26", "M27", "M31"]:
    mods[i] = S + "/mut/%s.py" % i
L = {k: load("p" + k, v) for k, v in mods.items()}
# fixture rows: (path, cells-text)
rowtxt = ("x\n%s\n"
  "| `tools/x/stderr-only.py` | g | 0=ok | `--selftest` 5 cases |\n"
  "| `tools/x/exit1.py` | g | 0=ok | `--selftest` 3 cases |\n"
  "| `tools/x/green.py` | g | 0=ok | `--selftest` 7 cases |\n"
  "| `tools/x/pinless.py` | g | 0=ok | `--selftest` 4 cases |\n"
  "| `tools/x/colfour.py` | cases=6 | 0=ok | green, exit 0 |\n"
  "%s\n") % ("<!-- instrument-registry v2 -->", "<!-- /instrument-registry -->")
open(CL + "/tools/x/pinless.py", "w").write("print('SELFTEST cases=4 failures=0')\n")
open(CL + "/tools/x/colfour.py", "w").write("print('SELFTEST cases=6 failures=0')\n")
cases = [
  ("stderr-only", "tools/x/stderr-only.py", {"tools/x/stderr-only.py": sha("tools/x/stderr-only.py")}, ["tools/x/stderr-only.py", "--selftest"]),
  ("exit1-green", "tools/x/exit1.py", {"tools/x/exit1.py": sha("tools/x/exit1.py")}, ["tools/x/exit1.py", "--selftest"]),
  ("green-ok", "tools/x/green.py", {"tools/x/green.py": sha("tools/x/green.py")}, ["tools/x/green.py", "--selftest"]),
  ("pin-wrong", "tools/x/pinless.py", {"tools/x/pinless.py": "0" * 64}, ["tools/x/pinless.py", "--selftest"]),
  ("claim-in-col2", "tools/x/colfour.py", {"tools/x/colfour.py": sha("tools/x/colfour.py")}, ["tools/x/colfour.py", "--selftest"]),
]
for key, mname in [("base", "base")] + [(k, k) for k in ["M16", "M17", "M18", "M19", "M22", "M26", "M27", "M31"]]:
    mod = L[key]
    rows, dup = mod.registry_rows(rowtxt)
    res = []
    for cname, path, pins, argv in cases:
        rec = mod.run_row(CL, S + "/fixt/work", "HEAD", path, pins, argv, rows, dup)
        res.append("%s:ok=%s" % (cname, rec["ok"]))
    print("%-5s " % key + "  ".join(res))
