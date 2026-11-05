#!/usr/bin/env python3
"""R90-C1 reviewer arms.

Arm 1 (brute): fix the broken later block by trying sz_cpr = 1..sz_unc,
applying it, and accepting the first value for which `upx -t` passes.
Arm 2 (first-plausible-successor): scan forward from the walk break for the
first plausible successor (0 < sc <= su, method byte matches, fits in file),
derive sz_cpr = succ - (block + 12), write it.

Both shells share the same b_info walk as the counter/repair modules and only
touch the 4-byte sz_cpr window at block+4.
"""
import hashlib, json, os, struct, subprocess, sys, tempfile, importlib.util

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m); return m
rep = load(ROOT + "/tools/round-87/upx-magic-repair.py", "r87")
r88 = load(ROOT + "/tools/round-88/upx-chain-repair.py", "r88")

def layout(packed):
    ph_off, ph = rep.find_packheader(packed)
    best = None
    for m in r88.l_info_candidates(packed, ph_off, ph):
        b0 = m + 20
        if b0 + 12 > ph_off: continue
        su0, _ = struct.unpack_from("<II", packed, b0)
        if su0 == 0: continue
        method = packed[b0 + 8]
        q, blks = b0, []
        while q + 12 <= ph_off:
            su, sc = struct.unpack_from("<II", packed, q)
            if su == 0 or sc == 0 or sc > su or q + 12 + sc > ph_off or packed[q+8] not in (method, ph["method"]):
                break
            blks.append({"block": q, "sz_unc": su, "sz_cpr": sc}); q += 12 + sc
        if best is None or len(blks) > len(best[1]): best = (b0, ph_off, ph, blks, method)
    return best

def upx_t(data):
    with tempfile.NamedTemporaryFile(suffix=".upx", delete=False) as fh:
        fh.write(data); p = fh.name
    r = subprocess.run(["/usr/bin/upx", "-t", "-q", p], capture_output=True)
    os.unlink(p)
    return r.returncode == 0

def brute(data, b0, ph_off, ph, blocks, method):
    """Try sz_cpr = 1..sz_unc for the last walkable block; take the first
    value whose full chain then validates under upx -t."""
    brk = blocks[-1]
    p, su, sc_stored = brk["block"], brk["sz_unc"], brk["sz_cpr"]
    for v in range(1, su + 1):
        if v == sc_stored: continue
        t = bytearray(data); struct.pack_into("<I", t, p + 4, v)
        if upx_t(bytes(t)):
            return bytes(t), {"arm": "brute", "pos": p, "derived": v, "tries": v}
    return None, {"arm": "brute", "pos": p, "derived": None, "tries": su}

def first_succ(data, b0, ph_off, ph, blocks, method):
    """First plausible successor after the walk break."""
    brk = blocks[-1]
    p, su, sc_stored = brk["block"], brk["sz_unc"], brk["sz_cpr"]
    for s in range(p + 13, ph_off - 12):
        su2, sc2 = struct.unpack_from("<II", data, s)
        if not (0 < sc2 <= su2) or s + 12 + sc2 > ph_off or data[s+8] not in (method, ph["method"]):
            continue
        derived = s - (p + 12)
        if not (0 < derived <= su) or derived == sc_stored: continue
        t = bytearray(data); struct.pack_into("<I", t, p + 4, derived)
        return bytes(t), {"arm": "first-successor", "pos": p, "successor": s,
                          "derived": derived, "stored": sc_stored}
    return None, {"arm": "first-successor", "pos": p, "derived": None}

def main():
    cells = [("jq",1644,[844,848]),("jq",1658,[844,848]),("xxd",943,[841,845]),
             ("xxd",957,[841,845]),("libz.so.1.3.2",33567,[9521,9525]),
             ("libz.so.1.3.2",33581,[9521,9525]),("docker-init",195,[818,822]),
             ("docker-init",209,[818,822])]
    lay = json.load(open("/fast/scratch/hyaku/kaidoku-r90/ReviewerC1/work/run/lay.json"))
    results = {"brute": [], "first-successor": []}
    for name, val, window in cells:
        b0, ph_off, ph, blocks, method = layout(open("/fast/scratch/hyaku/kaidoku-r90/ReviewerC1/work/run/%s/packed" % name, "rb").read())
        data = bytearray(open("/fast/scratch/hyaku/kaidoku-r90/ReviewerC1/work/run/%s/packed" % name, "rb").read())
        struct.pack_into("<I", data, window[0], val)
        data = bytes(data)
        for arm in ("brute", "first-successor"):
            fn = brute if arm == "brute" else first_succ
            out, info = fn(data, b0, ph_off, ph, blocks, method)
            rec = {"cell": "%s-%s" % (name, "+" if val > blocks[1]["sz_cpr"] else "-"),
                   "valid_upx_t": out is not None, **info}
            if out is not None:
                ident = hashlib.sha256(out).hexdigest() == hashlib.sha256(open("/fast/scratch/hyaku/kaidoku-r90/ReviewerC1/work/run/%s/packed" % name, "rb").read()).hexdigest()
                rec["identity"] = ident
            results[arm].append(rec)
    print(json.dumps(results, indent=1))
    json.dump(results, open("/fast/scratch/hyaku/kaidoku-r90/ReviewerC1/cheap-arms.json", "w"), indent=1)

main()
