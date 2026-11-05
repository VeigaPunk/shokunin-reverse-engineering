#!/usr/bin/env python3
"""Probe: is the round-90 repair unsafe on a last-block sz_cpr tamper?"""
import importlib.util, json, os, shutil, struct, subprocess, sys, tempfile

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
WORK = "/fast/scratch/hyaku/kaidoku-r91/l1/probe"
CARRIERS = [
    {"id": "jq", "source": "/usr/bin/jq"},
    {"id": "xxd", "source": "/usr/bin/xxd"},
    {"id": "libz", "source": "/usr/lib/libz.so.1.3.2"},
    {"id": "dinit", "source": "/usr/bin/docker-init"},
]


def load(rel, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


rep = load("tools/round-87/upx-magic-repair.py", "r87")
r88 = load("tools/round-88/upx-chain-repair.py", "r88")
r90 = load("tools/round-90/upx-break-repair.py", "r90")

env = {"HOME": os.path.join(WORK, "home"), "LANG": "C",
       "PATH": os.environ.get("PATH") or "/usr/bin", "TMPDIR": os.path.join(WORK, "tmp")}
for d in (env["HOME"], env["TMPDIR"]):
    os.makedirs(d, exist_ok=True)


def run(argv, timeout=600):
    p = subprocess.run(argv, capture_output=True, text=True, env=env, timeout=timeout)
    return p.returncode, (p.stdout + p.stderr).strip().splitlines()[-2:]


def pack(src, box):
    dst = os.path.join(box, "packed")
    shutil.copy2(src, dst)
    rc, tail = run(["/usr/bin/upx", "--best", "-q", "-o", os.path.join(box, "p"), dst])
    assert rc == 0, (rc, tail)
    with open(os.path.join(box, "p"), "rb") as fh:
        return fh.read()


def layout(packed):
    ph_off, ph = rep.find_packheader(packed)
    best = (None, [])
    for m in r88.l_info_candidates(packed, ph_off, ph):
        b0 = m + 20
        su0, _ = struct.unpack_from("<II", packed, b0)
        if su0 == 0:
            continue
        method = packed[b0 + 8]
        q, blocks = b0, []
        while q + 12 <= ph_off:
            su, sc = struct.unpack_from("<II", packed, q)
            if su == 0 or sc == 0 or sc > su or q + 12 + sc > ph_off or packed[q + 8] not in (method, ph["method"]):
                break
            blocks.append({"block": q, "sz_unc": su, "sz_cpr": sc})
            q += 12 + sc
        if len(blocks) > len(best[1]):
            best = (b0, blocks)
    return ph_off, ph, best[0], best[1]


def tamper(packed, block, value):
    out = bytearray(packed)
    struct.pack_into("<I", out, block["block"] + 4, value)
    return bytes(out)


def invoke(data, box):
    src, dst = os.path.join(box, "in"), os.path.join(box, "out")
    with open(src, "wb") as fh:
        fh.write(data)
    rc, tail = run([sys.executable, "-I", "-B", os.path.join(ROOT, "tools/round-90/upx-break-repair.py"),
                    "--in", src, "--out", dst])
    out = None
    if rc == 0 and os.path.isfile(dst):
        with open(dst, "rb") as fh:
            out = fh.read()
    return rc, tail, out


os.makedirs(WORK, exist_ok=True)
rows = []
for car in CARRIERS:
    box = tempfile.mkdtemp(prefix=car["id"] + "-", dir=WORK)
    packed = pack(car["source"], box)
    ph_off, ph, b0, blocks = layout(packed)
    last = blocks[-1]
    for delta in (-7, 7):
        value = last["sz_cpr"] + delta
        if not (0 < value <= last["sz_unc"]):
            rows.append({"carrier": car["id"], "delta": delta, "skip": "out of range"})
            continue
        t = tamper(packed, last, value)
        rb = tempfile.mkdtemp(prefix="inv-", dir=WORK)
        rc, tail, out = invoke(t, rb)
        rec = {"carrier": car["id"], "nblocks": len(blocks), "tampered_index": len(blocks) - 1,
               "stored": last["sz_cpr"], "value": value, "rc": rc, "tail": tail,
               "u_len": ph["u_len"], "method": ph["method"]}
        if out is None:
            rec["unsafe_write"] = False
            rec["refused"] = rc != 0
        else:
            lo, hi = last["block"] + 4, last["block"] + 8
            outside = [i for i, (a, b) in enumerate(zip(t, out)) if a != b and not (lo <= i < hi)]
            rec.update({"out_len": len(out), "changed": [i for i, (a, b) in enumerate(zip(t, out)) if a != b][:8],
                        "outside_window": outside[:8], "unsafe_write": bool(outside),
                        "inside_window_only": not outside and len(out) == len(t),
                        "identical": out == t, "refused": False})
            rp = os.path.join(rb, "cand")
            with open(rp, "wb") as fh:
                fh.write(out)
            rec["upx_test_rc"] = run(["/usr/bin/upx", "-t", "-q", rp])[0]
        rows.append(rec)
print(json.dumps(rows, indent=1))
