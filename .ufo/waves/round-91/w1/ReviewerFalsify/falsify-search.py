#!/usr/bin/env python3
"""Falsification search: is the T7 last-block stop-boundary tamper decidable by a
packer-validated search?

H: for at least one of the 8 tampered cells (4 carriers x {-7,+7} on the last
walkable block's stored sz_cpr), some in-range v makes `upx -t` rc 0 on the
candidate AND `upx -d` of the candidate reproduces the carrier's pinned original
sha256.

Candidate enumeration (seat spec): v in [1, sz_unc] when sz_unc <= 20000,
otherwise v in [stored-256, stored+256] plus the values the walk makes plausible
(stored itself, the tampered values stored-7/stored+7 -- all inside the window).
Cap: 25 minutes wall from search start.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import struct
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
UPX = "/usr/bin/upx"
UPX_SHA = "cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969"
S = os.environ["SEAT_SCRATCH"]
WORK = os.path.join(S, "work")
CAND = os.path.join(S, "cand")
TMPD = os.path.join(S, "tmp")
HOMED = os.path.join(S, "home")
ENV = {"PATH": "/usr/bin:/bin", "LANG": "C", "HOME": HOMED, "TMPDIR": TMPD}
SEARCH_CAP_S = 25 * 60

CARRIERS = [
    ("jq", "/usr/bin/jq",
     "e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806"),
    ("xxd", "/usr/bin/xxd",
     "7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65"),
    ("libz", "/usr/lib/libz.so.1.3.2",
     "6c78c5e58c3bb49a1cd151a95cdf1a17fe07a91a57a59e0279b984c533075ca9"),
    ("docker-init", "/usr/bin/docker-init",
     "0bd49c8d4da5601ce955c24a515917c9a132404df633c1e2fa28855cc2e3e115"),
]
DIRECTIONS = (-7, 7)

DEADLINE = [None]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(argv, timeout=180):
    try:
        p = subprocess.run(argv, env=ENV, timeout=timeout,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return p.returncode, p.stdout.decode(errors="replace")
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT"


def sha_file(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def pack(src, cid):
    inp = os.path.join(WORK, f"src-{cid}")
    outp = os.path.join(WORK, f"packed-{cid}")
    shutil.copyfile(src, inp)
    os.chmod(inp, 0o755)
    rc, txt = run([UPX, "--best", "-q", "-o", outp, inp])
    if rc != 0 or not os.path.isfile(outp):
        raise RuntimeError(f"pack failed for {cid}: rc={rc} {txt[-200:]}")
    with open(outp, "rb") as fh:
        return fh.read()


def _winit(deadline):
    DEADLINE[0] = deadline


def probe_chunk(task):
    cid, delta, vlist, tampered, block_off, pin, tag = task
    cpath = os.path.join(CAND, f"c-{tag}.bin")
    opath = os.path.join(CAND, f"o-{tag}.bin")
    rows, capped_at = [], None
    for v in vlist:
        b = bytearray(tampered)
        struct.pack_into("<I", b, block_off + 4, v)
        with open(cpath, "wb") as fh:
            fh.write(bytes(b))
        rc, txt = run([UPX, "-t", "-q", cpath])
        d_rc, match = None, False
        if rc == 0:
            d_rc, _ = run([UPX, "-d", "-q", "-o", opath, cpath])
            if d_rc == 0:
                match = sha_file(opath) == pin
        rows.append({"cid": cid, "delta": delta, "v": v, "t_rc": rc,
                     "d_rc": d_rc, "match": match})
        if DEADLINE[0] is not None and time.time() > DEADLINE[0]:
            capped_at = v
            break
    return rows, capped_at


def main():
    t0 = time.time()
    out = {"upx_sha256": sha_file(UPX), "upx_pin": UPX_SHA,
           "instruments": {}, "carriers": {}, "cells": {}, "cap_reached": False}
    for rel, key in [(f"{LANE}/tools/round-91/stop-boundary-battery.py", "battery"),
                     (f"{LANE}/tools/round-87/upx-magic-repair.py", "r87"),
                     (f"{LANE}/tools/round-88/upx-chain-repair.py", "r88")]:
        out["instruments"][key] = sha_file(rel)
    if out["upx_sha256"] != UPX_SHA:
        print("FATAL: upx sha drift", file=sys.stderr)
        return 2
    rep = load(f"{LANE}/tools/round-87/upx-magic-repair.py", "r87rep")
    r88 = load(f"{LANE}/tools/round-88/upx-chain-repair.py", "r88walk")
    bat = load(f"{LANE}/tools/round-91/stop-boundary-battery.py", "bat91")

    tasks = []
    for cid, src, pin in CARRIERS:
        assert sha_file(src) == pin, f"carrier pin drift {cid}"
        packed = pack(src, cid)
        b0, blocks = bat.layout(packed, rep, r88)
        if not blocks:
            raise RuntimeError(f"no walkable chain for {cid}")
        last = blocks[-1]
        # pristine controls
        ppath = os.path.join(WORK, f"pristine-{cid}")
        with open(ppath, "wb") as fh:
            fh.write(packed)
        t_rc, t_txt = run([UPX, "-t", "-q", ppath])
        d_rc, d_txt = run([UPX, "-d", "-q", "-o", os.path.join(WORK, f"unp-{cid}"), ppath])
        d_match = sha_file(os.path.join(WORK, f"unp-{cid}")) == pin if d_rc == 0 else False
        out["carriers"][cid] = {
            "packed_sha256": hashlib.sha256(packed).hexdigest(),
            "packed_bytes": len(packed), "b0": b0, "n_blocks": len(blocks),
            "last_block": last["block"], "stored_sz_cpr": last["sz_cpr"],
            "sz_unc": last["sz_unc"],
            "pristine_t_rc": t_rc, "pristine_d_rc": d_rc, "pristine_d_match": d_match,
        }
        print(f"[{cid}] blocks={len(blocks)} last_off={last['block']} "
              f"stored={last['sz_cpr']} sz_unc={last['sz_unc']} "
              f"pristine -t rc={t_rc} -d rc={d_rc} match={d_match}", flush=True)
        # tamper baselines + candidate lists
        for delta in DIRECTIONS:
            value = last["sz_cpr"] + delta
            cell = f"{cid}|{delta:+d}"
            if not (0 < value <= last["sz_unc"]):
                out["cells"][cell] = {"out_of_range": True, "value": value}
                continue
            tampered = bytearray(packed)
            struct.pack_into("<I", tampered, last["block"] + 4, value)
            tampered = bytes(tampered)
            tpath = os.path.join(WORK, f"tampered-{cid}-{delta}")
            with open(tpath, "wb") as fh:
                fh.write(tampered)
            bt_rc, bt_txt = run([UPX, "-t", "-q", tpath])
            stored, sz_unc = last["sz_cpr"], last["sz_unc"]
            if sz_unc <= 20000:
                vlist = list(range(1, sz_unc + 1))
                bound = f"[1,{sz_unc}] full sweep (sz_unc<=20000)"
            else:
                lo, hi = stored - 256, stored + 256
                vlist = list(range(max(1, lo), hi + 1))
                bound = f"[max(1,{lo}),{hi}] window + plausible {sorted(set([stored, stored-7, stored+7]) & set(vlist))}"
            out["cells"][cell] = {
                "delta": delta, "stored": stored, "value": value,
                "enumeration_bound": bound, "n_candidates": len(vlist),
                "tampered_baseline_t_rc": bt_rc,
                "tampered_baseline_t_tail": bt_txt.strip().splitlines()[-2:],
            }
            print(f"[{cell}] tampered -t rc={bt_rc} enumerating {len(vlist)} candidates: {bound}", flush=True)
            CH = 32
            for i in range(0, len(vlist), CH):
                tasks.append((cid, delta, vlist[i:i + CH], tampered,
                              last["block"], pin, f"{cid}-{delta}-{i}"))

    deadline = t0 + SEARCH_CAP_S
    agg = {}
    for cell in out["cells"]:
        if not out["cells"][cell].get("out_of_range"):
            agg[cell] = {"tried": 0, "greens": [], "matches": []}
    done_cells = set()
    with ProcessPoolExecutor(max_workers=min(16, os.cpu_count() or 4),
                             initializer=_winit, initargs=(deadline,)) as ex:
        futs = {ex.submit(probe_chunk, t): t[6] for t in tasks}
        for fut in as_completed(futs):
            rows, capped_at = fut.result()
            for r in rows:
                if r.get("cid") == "DEADLINE":
                    continue
                cell = f"{r['cid']}|{r['delta']:+d}"
                a = agg[cell]
                a["tried"] += 1
                if r["t_rc"] == 0:
                    a["greens"].append(r["v"])
                    if r["match"]:
                        a["matches"].append(r["v"])
            if capped_at is not None:
                out["cap_reached"] = True
                print(f"DEADLINE hit inside chunk {futs[fut]} at v={capped_at}", flush=True)
    for cell, a in agg.items():
        out["cells"][cell]["tried"] = a["tried"]
        out["cells"][cell]["green_vs"] = sorted(a["greens"])
        out["cells"][cell]["match_vs"] = sorted(a["matches"])
        out["cells"][cell]["n_green"] = len(a["greens"])
        out["cells"][cell]["n_match"] = len(a["matches"])
    out["wall_s"] = round(time.time() - t0, 1)
    with open(os.path.join(S, "results.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps({c: {k: v for k, v in cell.items()
                          if k in ("delta", "stored", "value", "tried", "n_green",
                                   "green_vs", "n_match", "match_vs",
                                   "tampered_baseline_t_rc", "enumeration_bound",
                                   "out_of_range")}
                      for c, cell in out["cells"].items()}, indent=1))
    print(f"cap_reached={out['cap_reached']} wall_s={out['wall_s']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
