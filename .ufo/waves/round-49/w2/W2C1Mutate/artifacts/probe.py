import importlib.util, json, os, subprocess, sys, tempfile
S = "/fast/scratch/hyaku/kaidoku-r49/W2C1Mutate"
def load(tag, path):
    spec = importlib.util.spec_from_file_location("c1_" + tag, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
mods = {"base": load("base", S + "/base/tools/round-49/c1-counter.py"),
        "m10": load("m10", S + "/mut/m10-no-quotepath/tools/round-49/c1-counter.py"),
        "m01": load("m01", S + "/mut/m01-prov-substring/tools/round-49/c1-counter.py")}
D = tempfile.mkdtemp(prefix="fx-", dir=S + "/probe")
def git(*a):
    return subprocess.run(["git", "-C", D] + list(a), capture_output=True, text=True, check=True).stdout.strip()
subprocess.run(["git", "init", "-q", D], check=True)
top = git("rev-parse", "--show-toplevel"); assert os.path.realpath(top) == os.path.realpath(D), top
os.makedirs(D + "/tools/round-49", exist_ok=True)
open(D + "/tools/round-49/c1-counter.py", "w").write("# frozen\n")
ident = ["-c", "user.name=fx", "-c", "user.email=fx@fx"]
subprocess.run(["git", "-C", D, "add", "-A"], check=True)
subprocess.run(["git", "-C", D] + ident + ["commit", "-qm", "freeze"], check=True)
freeze = git("rev-parse", "HEAD")
out = {}
for name, fn in (("ascii_added", "tools/round-49/plain.py"), ("nonascii_added", "tools/round-49/\u00e4.py")):
    open(D + "/" + fn, "w").write("x\n")
    subprocess.run(["git", "-C", D, "add", "-A"], check=True)
    subprocess.run(["git", "-C", D] + ident + ["commit", "-qm", name], check=True)
    rev = git("rev-parse", "HEAD")
    out[name] = {}
    for tag, m in mods.items():
        if tag == "m01":
            continue
        try:
            d = m.frozen_drift(D, freeze, rev, {})
            out[name][tag] = d
        except Exception as e:
            out[name][tag] = "EXC %s: %s" % (type(e).__name__, e)
    # rev for next iteration is the same chain: freeze..HEAD grows; record per-commit view
    out[name]["range"] = git("log", "--oneline", freeze + ".." + rev)
print(json.dumps(out, indent=1, ensure_ascii=False))
prov = ["/fast/scratch/hyaku/kaidoku-r49/x", "/tmp/a/fast/scratch/hyaku/kaidoku-r49/x",
        "/home/u/lane/fast/scratch/hyaku/kaidoku-r49/x", "/fast/scratch/hyaku/kaidoku-r42/x", "/fast/scratch/hyaku/kaidoku-r49/../kaidoku-r42/x"]
pv = {}
for p in prov:
    pv[p] = {t: m.provenance_ok(p) for t, m in mods.items() if t != "m10"}
print(json.dumps(pv, indent=1, ensure_ascii=False))
