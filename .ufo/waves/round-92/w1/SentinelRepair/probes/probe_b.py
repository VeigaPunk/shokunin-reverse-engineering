#!/usr/bin/env python3
"""SentinelRepair probe B: tempfile.mkstemp surface of upx_test (scratch TMPDIR only)."""
import importlib.util
import os
import subprocess

S = "/fast/scratch/hyaku/kaidoku-r92/SentinelRepair"
C = S + "/clone/tools/round-91/upx-stop-boundary-repair.py"
PKG = S + "/work/packed-xxd"
TMP = S + "/tmp"
os.makedirs(TMP, exist_ok=True)
os.environ["TMPDIR"] = TMP          # set BEFORE tempfile is first used
import tempfile
import time

print("gettempdir() in probe process:", tempfile.gettempdir())
assert tempfile.gettempdir() == TMP, "TMPDIR not honoured"

spec = importlib.util.spec_from_file_location("r91probe", C)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

data = open(PKG, "rb").read()
before = set(os.listdir(TMP))
t0 = time.perf_counter()
ok = mod.upx_test(data)
dt = time.perf_counter() - t0
after = set(os.listdir(TMP))
print(f"upx_test(intact packed carrier) = {ok}  ({dt*1000:.1f} ms)")
print(f"tmpdir entries before={len(before)} after={len(after)} leftovers={sorted(after - before)}")

# mkstemp intrinsic properties (name predictability, permissions, clobber)
names = set()
modes = []
for _ in range(200):
    fd, p = tempfile.mkstemp(prefix=".r91-test-", dir=TMP)
    names.add(os.path.basename(p))
    modes.append(os.stat(p).st_mode & 0o777)
    os.close(fd)
    os.unlink(p)
print(f"mkstemp: 200 calls -> {len(names)} distinct names; modes={sorted(set(oct(m) for m in modes))}")

# fallback dir when TMPDIR is unset (fresh process, stdlib default)
r = subprocess.run(
    ["python3", "-c",
     "import os;[os.environ.pop(k) for k in list(os.environ) if k=='TMPDIR'];"
     "import tempfile;print(tempfile.gettempdir())"],
    capture_output=True, text=True, env={"PATH": "/usr/bin"})
print("gettempdir() with TMPDIR unset:", r.stdout.strip())

# end-to-end: tool CLI with scratch TMPDIR leaves nothing behind (rc 0 path runs upx_test)
tmp2 = S + "/tmp2-e2e"
os.makedirs(tmp2, exist_ok=True)
env = dict(PATH="/usr/bin:/bin", LANG="C", HOME=tmp2, TMPDIR=tmp2)
p = subprocess.run(["python3", "-I", "-B", C, "--in", PKG, "--out", tmp2 + "/out"],
                   capture_output=True, text=True, env=env)
print(f"CLI rc={p.returncode} leftover-in-scratch-tmpdir={sorted(os.listdir(tmp2))}")

# hostile TMPDIR (nonexistent): does the no-traceback contract hold?
env_bad = dict(env, TMPDIR=S + "/tmp-does-not-exist")
p = subprocess.run(["python3", "-I", "-B", C, "--in", PKG, "--out", tmp2 + "/out2"],
                   capture_output=True, text=True, env=env_bad)
print(f"CLI with broken TMPDIR rc={p.returncode} stdout={p.stdout.strip()[:160]}")
