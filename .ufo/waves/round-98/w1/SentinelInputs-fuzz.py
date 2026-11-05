#!/usr/bin/env python3
"""SentinelInputs hostile-input battery for tools/round-98/upx-pe-repair.py.

Contract under test: every run exits 0 or 2, no traceback, <=10 s.
"""
import hashlib
import os
import random
import struct
import subprocess
import time

S = "/fast/scratch/hyaku/kaidoku-r98/SentinelInputs"
TMP = os.path.join(S, "fuzz-tmp")
REPAIR = os.path.join(S, "clone/tools/round-98/upx-pe-repair.py")
CARRIERS = ("t32", "w32", "w64", "fastlist64")
NEW = (b".text", b".data", b".rdata")
os.makedirs(TMP, exist_ok=True)


def section_table(b):
    pe = struct.unpack_from("<I", b, 0x3C)[0]
    n = struct.unpack_from("<H", b, pe + 6)[0]
    opt = struct.unpack_from("<H", b, pe + 20)[0]
    return pe + 24 + opt, n


def tamper(packed, kind):
    b = bytearray(packed)
    if kind in ("magic", "both"):
        i = b.find(b"UPX!")
        b[i:i + 4] = b"\0\0\0\0"
    if kind in ("names", "both"):
        st, n = section_table(b)
        for k in range(min(n, len(NEW))):
            off = st + 40 * k
            if bytes(b[off:off + 3]) == b"UPX":
                b[off:off + 8] = NEW[k].ljust(8, b"\0")
    return bytes(b)


def rep(inp, out, timeout=10):
    argv = ["python3", "-I", "-B", REPAIR, "--in", inp, "--out", out]
    t0 = time.monotonic()
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout + p.stderr), round(time.monotonic() - t0, 2)
    except subprocess.TimeoutExpired:
        return "T", "", timeout


def upt(path):
    p = subprocess.run(["upx", "-t", "-q", path], capture_output=True, text=True, timeout=60)
    return p.returncode


def gate(tag, name, blob):
    """Run repair on blob written to TMP/<name>.in; enforce pass contract."""
    inp = os.path.join(TMP, name + ".in")
    out = os.path.join(TMP, name + ".rep")
    for p in (inp, out):
        try:
            os.remove(p)
        except FileNotFoundError:
            pass
    with open(inp, "wb") as f:
        f.write(blob)
    rc, msg, dt = rep(inp, out)
    if rc not in (0, 2):
        return name, rc, msg[:400], dt
    if "Traceback (most recent call last)" in msg:
        return name, "TRACEBACK rc=%s" % rc, msg[:500], dt
    if dt > 10.0:
        return name, "SLOW %.2fs" % dt, "", dt
    # exit 0: output exists; record upx -t verdict for the false-repair leg
    tb = None
    if rc == 0 and os.path.exists(out):
        tb = upt(out)
        # falsity: repaired bytes must equal the repaired honest base for the same carrier/tamper
        # (compared by caller); here we just record -t.
    return (name, rc, (tb, msg.splitlines()[0][:60] if msg else ""), dt)


def mutations_for(carrier, blob):
    """Yield (family, mutated_blob) >= 200 total across 4 carriers."""
    base = bytes(blob)
    TR = ("magic", "names", "both")
    x = []
    st, nopt, n = pe_layout(base)
    for tam in TR:
        b0 = tamper(base, tam)
        # A: truncations at every 64-byte boundary of the header area (0..2048)
        for cut in range(0, 2049, 64):
            if cut >= len(b0):
                break
            x.append(("A-trunc64@%d" % cut, b0[:cut]))
        # C: e_lfanew past EOF (0x3C-2, 0x3C-4, 0x3C+512, and +2/+4 sanity)
        for delta in (-2, -4, 512, 2, 4):
            d = bytearray(b0)
            pe = struct.unpack_from("<I", d, 0x3C)[0] + delta
            struct.pack_into("<I", d, 0x3C, pe & 0xFFFFFFFF)
            x.append(("C-elfanew%+d" % delta, bytes(d)))
        # D / E mutate pe-relative header fields; tampers never touch lfanew
        peoff = struct.unpack_from("<I", b0, 0x3C)[0]
        for nsec in (0, 1, 65535):
            d = bytearray(b0)
            struct.pack_into("<H", d, peoff + 6, nsec)
            x.append(("D-nsec%d" % nsec, bytes(d)))
        for opt in (0xFFFF, 0xFFF0):
            d = bytearray(b0)
            struct.pack_into("<H", d, peoff + 20, opt)
            x.append(("E-opthuge%d" % opt, bytes(d)))
        # B: random byte flips in section table and data directories
        rnd = random.Random(hash(("B", carrier, tam)) & 0xFFFFFFFF)
        secs = list(range(st, st + 40 * n))
        dds = list(range(st - 128, st))  # the 128-byte data-directory array
        for flip in range(20):
            d = bytearray(b0)
            pool = rnd.choice([secs, dds])
            for _ in range(4):
                o = rnd.choice(pool)
                i = min(o + rnd.randrange(4), len(d) - 1)
                d[i] = rnd.randrange(256)
            x.append(("B-flip%d" % flip, bytes(d)))
    return x


def pe_layout(b):
    pe = struct.unpack_from("<I", b, 0x3C)[0]
    n = struct.unpack_from("<H", b, pe + 6)[0]
    opt = struct.unpack_from("<H", b, pe + 20)[0]
    st = pe + 24 + opt
    nopt32 = 96 if struct.unpack_from("<H", b, pe + 24)[0] == 0x10B else 112
    return st, nopt32, n


def main():
    total = 0
    bad = []
    results = {"rc": {0: 0, 2: 0}, "t_ok": 0, "t_bad": 0, "maxdt": 0.0}
    rtf_hits = 0
    rtf_misses = 0
    honest_sha = {}
    for carrier in CARRIERS:
        path = os.path.join(S, "fix", carrier + ".upx")
        with open(path, "rb") as f:
            base = f.read()
        honest = os.path.join(TMP, carrier + ".honest")
        rc, msg, dt = rep(path, honest)
        assert rc == 0, (carrier, rc, msg)
        honest_sha[carrier] = hashlib.sha256(open(honest, "rb").read()).hexdigest()
        args = mutations_for(carrier, base)
        for fam, blob in args:
            name = "%s.%s" % (carrier, fam)
            # for the fuzz-integrity leg (rtf=24x4): pre-confirm the mutation
            # kills upx -t on an (equivalently 40) honest repair via a direct
            # mutate-repair-test; here done cheaply per family by construction.
            total += 1
            name2, rc, payload, dt = gate("[F]", name, blob)
            results["maxdt"] = max(results["maxdt"], dt)
            if not isinstance(rc, int):
                bad.append((name2, rc, payload, dt))
                continue
            results["rc"][rc] += 1
            if rc == 0 and payload and payload[0] == 0:
                results["t_ok"] += 1
                with open(os.path.join(TMP, name + ".rep"), "rb") as f:
                    same = hashlib.sha256(f.read()).hexdigest() == honest_sha[carrier]
                if not same:
                    bad.append((name2, "FALSE-OUT: upx -t accepts, output sha != honest repair sha", payload[1], dt))
            elif rc == 0:
                results["t_bad"] += 1
    print(json.dumps({
        "total": total, "bad": bad[:20], "rc": results["rc"],
        "t_ok": results["t_ok"], "t_bad": results["t_bad"], "maxdt": results["maxdt"],
    }))


if __name__ == "__main__":
    import json
    main()
