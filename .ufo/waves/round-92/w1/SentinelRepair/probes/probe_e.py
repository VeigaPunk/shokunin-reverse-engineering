import contextlib
import importlib.util
import io
import os
import struct
import subprocess
import sys

S = "/fast/scratch/hyaku/kaidoku-r92/SentinelRepair"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


mod = load(S + "/clone/tools/round-91/upx-stop-boundary-repair.py", "r91e")
r87 = load(S + "/clone/tools/round-87/upx-magic-repair.py", "r87e")
r88 = load(S + "/clone/tools/round-88/upx-chain-repair.py", "r88e")
r90 = load(S + "/clone/tools/round-90/upx-break-repair.py", "r90e")

data = open(S + "/work/packed-xxd", "rb").read()
blocks, b0, ph, sc, st, method = mod.classify(data, r90, r87, r88)
lb = blocks[-1]
t = bytearray(data)
struct.pack_into("<I", t, lb["block"] + 4, lb["sz_cpr"] + 7)
src = S + "/work/e/tampered.bin"
out = S + "/work/e/out-timeout"
open(src, "wb").write(bytes(t))


def boom(*a, **k):
    raise subprocess.TimeoutExpired(cmd=a[0], timeout=600)


real = mod.subprocess.run
mod.subprocess.run = boom
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    try:
        rc = mod.main(["--in", src, "--out", out])
    except BaseException as exc:
        rc = f"UNCAUGHT {type(exc).__name__}"
mod.subprocess.run = real
print("timeout-injected: rc =", rc, "| stdout =", buf.getvalue().strip()[:220])
print("timeout-injected: output written =", os.path.exists(out))
