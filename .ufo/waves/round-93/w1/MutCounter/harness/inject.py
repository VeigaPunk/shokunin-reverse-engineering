#!/usr/bin/env python3
"""MutCounter in-process injection harness (scratch only). Loads one counter file,
applies a named injection, runs the counter's own functions/main. Same harness for
honest and mutant counters so differences are attributable to the mutant alone."""
import argparse, hashlib, importlib.util, json, os, secrets, struct, sys
ap = argparse.ArgumentParser()
ap.add_argument("--mode", required=True)
ap.add_argument("--counter", required=True)
ap.add_argument("--root", required=True)
ap.add_argument("--work", required=True)
ap.add_argument("--clone", required=True)
ap.add_argument("--expect", required=True)
ap.add_argument("--repair-cmd", default="tools/round-92/upx-stop-boundary-search-repair.py")
a = ap.parse_args()
os.makedirs(a.work, exist_ok=True)
sp = importlib.util.spec_from_file_location("ctr_under_test", a.counter)
mod = importlib.util.module_from_spec(sp); sp.loader.exec_module(mod)
v2 = mod.v2
REV = "92a240521bd1bf2213b75d18d9b176a8dafdc67c"
HONEST = os.path.join(a.clone, "tools/round-92/upx-stop-boundary-search-repair.py")
repair = os.path.join(a.root, a.repair_cmd)
env = v2.env_for(os.path.abspath(a.work))
def sha(b): return hashlib.sha256(b).hexdigest()
def fixed(v):
    secrets.token_hex = lambda n, _v=v: _v * n

def main_run(repair_cmd):
    argv = ["--root", a.root, "--repair-cmd", repair_cmd, "--work", a.work, "--rev", REV, "--expect", a.expect]
    return mod.main(argv)

def fresh_summary(out):
    return {"unevaluable": out.get("unevaluable"),
            "provenance": out.get("provenance"),
            "cells": [(c.get("kind"), c.get("delta"), c.get("class"), c.get("roundtrip")) for c in out.get("cells", [])],
            "intact_identity": (out.get("intact") or {}).get("identity")}

rep = v2._load(os.path.join(a.root, v2.R87), "r87i"); r88 = v2._load(os.path.join(a.root, v2.R88), "r88i")
if a.mode == "plain":
    code = main_run(a.repair_cmd)
elif a.mode == "m3":  # second pack differs -> determinism atom must fail
    real = v2.pack; n = [0]
    def fake(src, work, env_):
        n[0] += 1; b = real(src, work, env_)
        return b if n[0] == 1 else b[:-1] + bytes([b[-1] ^ 1])
    v2.pack = fake
    out = mod.fresh_arm(repair, env, os.path.abspath(a.work), rep, r88, set(), a.root)
    code = None; print(json.dumps(fresh_summary(out), default=str))
elif a.mode == "m4":  # fresh pack collides with a public packed image -> must be refused
    fixed("11")
    raw = open("/usr/bin/env", "rb").read()
    mut, _ = mod.mutate_source(raw, "11" * 8)
    p = os.path.join(a.work, "col-src.bin"); open(p, "wb").write(mut)
    colliding = sha(v2.pack(p, a.work, env))
    out = mod.fresh_arm(repair, env, os.path.abspath(a.work), rep, r88, {colliding}, a.root)
    code = None; print(json.dumps(fresh_summary(out), default=str))
elif a.mode == "m5none":  # upx -d roundtrip returns None for every repaired fresh cell
    mod.roundtrip_sha = lambda data, e, w: None
    code = main_run(a.repair_cmd)
elif a.mode == "m7":  # fresh intact input answered with altered bytes (intact identity must fail)
    fixed("22")
    raw = open("/usr/bin/env", "rb").read()
    mut, _ = mod.mutate_source(raw, "22" * 8)
    p = os.path.join(a.work, "intact-src.bin"); open(p, "wb").write(mut)
    FRESH = sha(v2.pack(p, a.work, env))
    W7 = os.path.join(os.path.dirname(os.path.abspath(a.work)), "w7-" + os.path.basename(os.path.abspath(a.work)) + ".py")
    open(W7, "w").write(f"""#!/usr/bin/env python3
import hashlib, subprocess, sys
FRESH = "{FRESH}"
args = sys.argv[1:]; src = args[args.index('--in') + 1]; dst = args[args.index('--out') + 1]
data = open(src, 'rb').read()
if hashlib.sha256(data).hexdigest() == FRESH:
    b = bytearray(data); b[len(b) // 2] ^= 0xFF
    open(dst, 'wb').write(bytes(b)); print('{{"class": "wrapper-altered-intact"}}'); sys.exit(0)
sys.exit(subprocess.run([sys.executable, '-I', '-B', {HONEST!r}, '--in', src, '--out', dst]).returncode)
""")
    code = main_run(W7)
elif a.mode == "f4":  # constant-nonce pinned forger
    code = main_run(os.path.join(os.path.dirname(os.path.abspath(__file__)), "f4.py"))
else:
    raise SystemExit("unknown mode")
if code is not None:
    print("EXIT", code)
