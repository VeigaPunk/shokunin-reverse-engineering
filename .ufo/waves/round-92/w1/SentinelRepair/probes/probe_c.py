#!/usr/bin/env python3
"""SentinelRepair probe C: layout-walker resource bounds (scratch only).

C1  sz_unc near 2^31 through the round-91 tool end-to-end (rc + wall time).
C2  single-walk scaling (rare-pattern chain, su=sc=1): N = 100k/200k/400k.
C3  candidate-fruitful chain (quadratic): N = 5000/10000/20000, layout() only.
C4  upx -t verdict cost per cell (small carrier; carrier+64MiB; carrier+192MiB).
"""
import importlib.util
import json
import os
import struct
import subprocess
import sys
import time

S = "/fast/scratch/hyaku/kaidoku-r92/SentinelRepair"
CLONE = S + "/clone"
WORK = S + "/work/c"
TMP = S + "/tmp"
os.makedirs(WORK, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

rep = load(CLONE + "/tools/round-87/upx-magic-repair.py", "r87probe")
r88 = load(CLONE + "/tools/round-88/upx-chain-repair.py", "r88probe")
r90 = load(CLONE + "/tools/round-90/upx-break-repair.py", "r90probe")
bat = load(CLONE + "/tools/round-91/stop-boundary-battery.py", "batprobe")
RES = {}

# ---------- builders ----------
def ph_bytes(version, fmt, method, u_len, c_len, u_file_size):
    ph = bytearray(rep.MAGIC + bytes([version, fmt, method, 10])
                   + struct.pack("<IIIII", 1, 2, u_len, c_len, u_file_size)
                   + bytes([0, 0, 0, 0]))
    ph[31] = rep.ph_checksum(bytes(ph))
    return bytes(ph)

def build_linear(n_records):
    """Rare-pattern chain, su=sc=1 (13-byte records): maximal single-walk length."""
    ufs = 1
    body = bytearray(b"\x7fELF\x02\x01\x01" + b"\0" * 57)
    body += struct.pack("<I", 0x11223344) + rep.MAGIC + struct.pack("<HBB", 3000, 14, 22)
    body += struct.pack("<III", 0, ufs, ufs)
    for _ in range(n_records):
        body += struct.pack("<IIBBBB", 1, 1, 14, 0, 0, 0) + b"A"
    body += struct.pack("<II", 0, struct.unpack("<I", rep.MAGIC)[0]) + b"\0" * 4  # sentinel
    body += ph_bytes(14, 22, 14, n_records, 64, ufs) + struct.pack("<I", 0)
    return bytes(body)

def build_fruitful(n_records):
    """Candidate-fruitful chain: one valid l_info candidate PER record, each
    walking the whole chain -> candidates x walk length (quadratic).
    Record (28 B): su=16, sc=16, meth=14, 000, payload[2]=14 (version),
    payload[3]=22 (format), payload[8:12]=LE(u_file_size)=14 00 0E 16."""
    ufs = 0x160E0014
    payload = bytes([0, 0, 14, 22, 0, 0, 0, 0, 20, 0, 14, 22, 0, 0, 0, 0])
    assert struct.pack("<I", ufs) == payload[8:12]
    body = bytearray(b"\x7fELF\x02\x01\x01" + b"\0" * 57)
    for _ in range(n_records):
        body += struct.pack("<IIBBBB", 16, 16, 14, 0, 0, 0) + payload
    body += ph_bytes(14, 22, 14, 16 * n_records, 64, ufs) + struct.pack("<I", 0)
    return bytes(body)

def build_big_szunc():
    """r87 fixture shape with block0 sz_unc patched near 2^31."""
    d = bytearray(rep._fixture())
    # block 0 b_info sits right after the p_info/l_info region; locate via walker
    ph_off, ph = rep.find_packheader(bytes(d))
    found = r90.longest_prefix(bytes(d), rep, r88)
    _m, b0, _ph, blocks, _method = found
    struct.pack_into("<I", d, blocks[0]["block"], 0x7FFFFF00)  # sz_unc ~ 2^31
    return bytes(d), blocks[0]["block"]

def timed(fn):
    t0 = time.perf_counter()
    out = fn()
    return out, time.perf_counter() - t0

TOOL = CLONE + "/tools/round-91/upx-stop-boundary-repair.py"
env = dict(PATH="/usr/bin:/bin", LANG="C", HOME=TMP, TMPDIR=TMP)

def tool_run(tag, src):
    dst = os.path.join(WORK, tag + "-out")
    t0 = time.perf_counter()
    try:
        p = subprocess.run(["timeout", "120", "python3", "-I", "-B", TOOL,
                            "--in", src, "--out", dst],
                           capture_output=True, text=True, env=env)
        rc, tail, dt = p.returncode, (p.stdout + p.stderr).strip()[:220], time.perf_counter() - t0
    except subprocess.TimeoutExpired:
        rc, tail, dt = "TIMEOUT-120s", "", time.perf_counter() - t0
    return {"case": tag, "rc": rc, "wall_s": round(dt, 3), "tail": tail}

# ---------- C1 ----------
src, blk = build_big_szunc()
p1 = os.path.join(WORK, "c1-big-szunc.bin")
open(p1, "wb").write(src)
r, dt = timed(lambda: bat.layout(src, rep, r88))
RES["C1_layout_big_szunc"] = {"blocks": len(r[1]), "sz_unc_patched": "0x7FFFFF00",
                              "block": blk, "wall_s": round(dt, 3)}
RES["C1_tool"] = tool_run("c1", p1)

# ---------- C2 linear ----------
RES["C2_linear"] = []
for n in (100_000, 200_000, 400_000):
    d = build_linear(n)
    f = os.path.join(WORK, f"c2-linear-{n}.bin")
    open(f, "wb").write(d)
    (b0, blocks), dt = timed(lambda: bat.layout(d, rep, r88))
    RES["C2_linear"].append({"n_records": n, "file_bytes": len(d),
                             "blocks_walked": len(blocks), "layout_wall_s": round(dt, 3)})
    os.unlink(f)

# ---------- C3 quadratic ----------
RES["C3_fruitful"] = []
for n in (5000, 10000, 20000):
    d = build_fruitful(n)
    f = os.path.join(WORK, f"c3-fruitful-{n}.bin")
    open(f, "wb").write(d)
    (_b0, blocks), dt = timed(lambda: bat.layout(d, rep, r88))
    RES["C3_fruitful"].append({"n_records": n, "file_bytes": len(d),
                               "blocks_longest": len(blocks), "layout_wall_s": round(dt, 3)})
    RES[f"C3_tool_n{n}"] = tool_run(f"c3-{n}", f)
    os.unlink(f)

# ---------- C4 upx -t per-cell verdict cost ----------
RES["C4_upx_test"] = []
pkg = S + "/work/packed-xxd"
big64 = os.path.join(WORK, "packed-plus-64M")
big192 = os.path.join(WORK, "packed-plus-192M")
with open(pkg, "rb") as fh:
    base = fh.read()
for path, extra in ((big64, 64 << 20), (big192, 192 << 20)):
    with open(path, "wb") as fh:
        fh.write(base + b"\0" * extra)
def upx_t(path):
    t0 = time.perf_counter()
    p = subprocess.run(["timeout", "300", "/usr/bin/upx", "-t", "-q", path],
                       capture_output=True, text=True,
                       env=dict(PATH="/usr/bin:/bin", LANG="C", HOME=TMP, TMPDIR=TMP))
    return {"file": os.path.basename(path), "bytes": os.path.getsize(path),
            "rc": p.returncode, "wall_s": round(time.perf_counter() - t0, 3)}
RES["C4_upx_test"].append(upx_t(pkg))
RES["C4_upx_test"].append(upx_t(big64))
RES["C4_upx_test"].append(upx_t(big192))
os.unlink(big64)
os.unlink(big192)

print(json.dumps(RES, indent=1))
with open(S + "/logs/probe_c.json", "w") as fh:
    json.dump(RES, fh, indent=1)
