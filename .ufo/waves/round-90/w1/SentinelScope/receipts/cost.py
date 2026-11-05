#!/usr/bin/env python3
"""Round-90 sentinel: cost of tools/round-90/upx-break-repair.py on crafted
carriers.

A  real carriers (jq, xxd, dinit, libz), later-block tamper, no decoration
B  l_info candidates 0 / 800 / 3,200 / 12,800 (the round-88 axis): each decoy
   candidate carries a one-block b_info walk, planted after the end-of-chain
   sentinel so the carrier still repairs
C  successor density 0 / 50 / 200 / 800: plausible b_info records planted in
   the tampered block's own payload, i.e. inside derive_break's successor scan
   window -- the scan's quadratic term
"""
import hashlib, importlib.util, json, os, shutil, statistics, struct, subprocess, sys, time

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
TOOL = os.path.join(LANE, "tools/round-90/upx-break-repair.py")
S = "/fast/scratch/hyaku/kaidoku-r90/SentinelScope"
C = os.path.join(S, "cost")
FX = os.path.join(S, "fx")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


rep = load(os.path.join(LANE, "tools/round-87/upx-magic-repair.py"), "rep")
r88 = load(os.path.join(LANE, "tools/round-88/upx-chain-repair.py"), "r88")
r90 = load(TOOL, "r90")
REC = []


def sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def run(path, reps=3, timeout=150):
    times = []
    last = None
    for _ in range(reps):
        out = path + ".out"
        if os.path.exists(out):
            os.unlink(out)
        t0 = time.monotonic()
        try:
            p = subprocess.run([sys.executable, "-I", "-B", TOOL, "--in", path,
                                "--out", out], capture_output=True, text=True,
                               timeout=timeout)
            rc, stdout, err = p.returncode, p.stdout, p.stderr
        except subprocess.TimeoutExpired:
            times.append(timeout)
            last = {"rc": None, "timeout": True}
            break
        times.append(time.monotonic() - t0)
        last = {"rc": rc, "stdout": stdout.strip()[:400],
                "stderr_tail": err.strip().splitlines()[-2:]}
    last = dict(last or {})
    last.update({"wall_s_median": round(statistics.median(times), 3),
                 "wall_s_all": [round(t, 3) for t in times],
                 "input_size": os.path.getsize(path)})
    return last


def build_later(cid):
    packed = open(os.path.join(FX, cid + ".packed"), "rb").read()
    ph_off, ph = rep.find_packheader(packed)
    b0, blocks = None, None
    for m in r88.l_info_candidates(packed, ph_off, ph):
        cand = m + 20
        su, _sc = struct.unpack_from("<II", packed, cand)
        if su == 0:
            continue
        method = packed[cand + 8]
        q, bl = cand, []
        while q + 12 <= ph_off:
            a, b = struct.unpack_from("<II", packed, q)
            if a == 0 or b == 0 or b > a or q + 12 + b > ph_off \
                    or packed[q + 8] not in (method, ph["method"]):
                break
            bl.append({"block": q, "sz_unc": a, "sz_cpr": b})
            q += 12 + b
        if blocks is None or len(bl) > len(blocks):
            b0, blocks = cand, bl
    blk = blocks[1]
    t = bytearray(packed)
    struct.pack_into("<I", t, blk["block"] + 4, blk["sz_cpr"] - 7)
    return packed, bytes(t), ph_off, ph, b0, blocks


def add_l_info_decoys(data, ph_off, ph, n, recsize=48):
    """n l_info candidates, each with a one-block b_info walk at m+20."""
    body = bytearray(data[:ph_off])
    tail = data[ph_off:]
    recs = bytearray()
    for _ in range(n):
        r = bytearray(recsize)
        r[6] = ph["version"]
        r[7] = ph["format"]
        struct.pack_into("<I", r, 12, ph["u_file_size"])
        struct.pack_into("<II", r, 20, 64, 16)
        r[28] = ph["method"]
        recs += r
    return bytes(body + recs + tail)


def add_successors(data, blk, su_p, n, stride=12):
    """n plausible b_info headers inside the tampered block's payload window."""
    out = bytearray(data)
    lo = blk["block"] + 12
    hi = min(len(out), blk["block"] + 12 + su_p - 16)
    step = max(12, (hi - lo) // max(1, n)) if n else 0
    for k in range(n):
        s = lo + 4 + k * step
        if s + 12 > hi:
            break
        struct.pack_into("<II", out, s, 32, 16)
        out[s + 8] = 0x02
        out[s + 9] = out[s + 10] = out[s + 11] = 0
    return bytes(out)


def main():
    shutil.rmtree(C, ignore_errors=True)
    os.makedirs(C)
    # C-A real carriers
    print("== A: real carriers ==")
    for cid in ("jq", "xxd", "libz", "dinit"):
        src = {"jq": "/usr/bin/jq", "xxd": "/usr/bin/xxd",
               "libz": "/usr/lib/libz.so.1.3.2", "dinit": "/usr/bin/docker-init"}[cid]
        packed = os.path.join(FX, cid + ".packed")
        if not os.path.isfile(packed):
            real = os.path.realpath(src)
            p2 = packed
            r = subprocess.run(["/usr/bin/upx", "--best", "-q", "-o", p2, real],
                               capture_output=True, text=True)
            if r.returncode != 0:
                REC.append({"exp": "A", "carrier": cid, "pack_rc": r.returncode,
                            "stderr": r.stderr.strip()[:200]})
                print(cid, "pack failed", r.returncode, r.stderr.strip()[:120])
                continue
        packed, tampered, ph_off, ph, b0, blocks = build_later(cid)
        tp = os.path.join(C, f"A-{cid}.later")
        open(tp, "wb").write(tampered)
        r = run(tp, reps=5)
        r.update({"exp": "A", "carrier": cid, "u_len": ph["u_len"],
                  "sz_cpr": blocks[1]["sz_cpr"], "sz_unc": blocks[1]["sz_unc"],
                  "successor_window": blocks[1]["sz_unc"]})
        REC.append(r)
        print(cid, json.dumps({k: r[k] for k in ("rc", "wall_s_median", "input_size")}))

    # C-B l_info candidates
    print("== B: l_info candidates ==")
    packed, tampered, ph_off, ph, b0, blocks = build_later("jq")
    blk = blocks[1]
    for n in (0, 800, 3200, 12800):
        data = add_l_info_decoys(tampered, ph_off, ph, n)
        p = os.path.join(C, f"B-linfo{n}")
        open(p, "wb").write(data)
        r = run(p, reps=1, timeout=150)
        same = None
        if r.get("rc") == 0:
            same = sha(p + ".out") == sha(os.path.join(FX, "jq.packed"))
        r.update({"exp": "B", "l_info_candidates": n + 1, "decoys": n,
                  "repairs_to_pin": same})
        REC.append(r)
        print(n, json.dumps({k: r.get(k) for k in ("rc", "wall_s_median",
                                                   "input_size", "repairs_to_pin")}))

    # C-C successor density
    print("== C: successor density ==")
    for n in (0, 50, 200, 800):
        data = add_successors(tampered, blk, blk["sz_unc"], n)
        p = os.path.join(C, f"C-succ{n}")
        open(p, "wb").write(data)
        r = run(p, reps=1, timeout=150)
        r.update({"exp": "C", "planted_successors": n,
                  "scan_window": blk["sz_unc"]})
        REC.append(r)
        print(n, json.dumps({k: r.get(k) for k in ("rc", "wall_s_median", "input_size")}))

    json.dump(REC, open(os.path.join(S, "cost.json"), "w"), indent=1, sort_keys=True)


main()
