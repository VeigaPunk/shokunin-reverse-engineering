#!/usr/bin/env python3
"""matrix.py - seat ExecMatrix-5; the round-90 R90-C1 tamper matrix driver.

Reproduces the battery's carrier production (copy pinned source -> upx 5.2.0
--best -q, pinned upx sha256 preflighted), then for every pinned carrier x
interior first-segment block index x in-range sampled direction {-7,+7}
(stored+7 full arms on sampled indices, stored-7 on every interior index)
builds the P1 tamper (b_info.sz_cpr := stored+delta at block+4, LE) and
measures the cell: upx -t verdict before repair, whether the unchanged
round-89 repair changes any byte, whether the round-90 repair recovers
(bytes equal intact packed, upx -t rc 0, upx -d sha equal the carrier pin),
stored/derived sz_cpr, stored/repaired accounted totals, u_len.

Out-of-class shapes recorded too: the last block before the chain stop
(index n-1, both directions where in range) and the libz interior cells, with
the tool's verbatim stdout.  Per-carrier temp dirs are removed on exit; JSON
receipts land directly in the seat receipts dir; matrix JSON is rewritten
after every cell so partial progress is durable.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import time

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r90/ExecMatrix"
SEAT = ROOT + "/.ufo/waves/round-90/w1/ExecMatrix"
RECEIPTS = SEAT + "/receipts"
UPX = "/usr/bin/upx"
PIN = "cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969"
R87 = ROOT + "/tools/round-87/upx-magic-repair.py"
R88 = ROOT + "/tools/round-88/upx-chain-repair.py"
R89 = ROOT + "/tools/round-89/upx-field-value-repair.py"
R90 = ROOT + "/tools/round-90/upx-break-repair.py"
CARRIERS = [
    {"id": "jq", "source": "/usr/bin/jq",
     "sha256": "e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806"},
    {"id": "xxd", "source": "/usr/bin/xxd",
     "sha256": "7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65"},
    {"id": "libz", "source": "/usr/lib/libz.so.1.3.2",
     "sha256": "6c78c5e58c3bb49a1cd151a95cdf1a17fe07a91a57a59e0279b984c533075ca9"},
    {"id": "dinit", "source": "/usr/bin/docker-init",
     "sha256": "0bd49c8d4da5601ce955c24a515917c9a132404df633c1e2fa28855cc2e3e115"},
]
P1_IDS = {"jq", "xxd", "dinit"}
N_PER = 4
cellno = 0
ENV = {"HOME": os.path.expanduser("~"), "LANG": "C", "PATH": os.environ["PATH"]}


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    with open(p, "rb") as fh:
        return sha_bytes(fh.read())


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(argv, timeout=900):
    p = subprocess.run(argv, env=ENV, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, timeout=timeout)
    return p.returncode, p.stdout.decode("utf-8", errors="replace")


def layout(P0, rep, r88):
    """Same candidate walk as the battery's layout(): (b0, ph, ph_off, blocks)."""
    ph_off, ph = rep.find_packheader(P0)
    best = None
    for m in r88.l_info_candidates(P0, ph_off, ph):
        b0 = m + 20
        if b0 + 12 > ph_off or struct.unpack_from("<I", P0, b0)[0] == 0:
            continue
        method = P0[b0 + 8]
        _s, blocks = None, []
        q = b0
        while q + 12 <= ph_off:
            su, sc = struct.unpack_from("<II", P0, q)
            if (su == 0 or sc == 0 or sc > su or q + 12 + sc > ph_off
                    or P0[q + 8] not in (method, ph["method"])):
                break
            blocks.append({"index": len(blocks), "block": q, "sz_unc": su,
                           "sz_cpr": sc})
            q += 12 + sc
        if best is None or len(blocks) > len(best[3]):
            best = (b0, ph, ph_off, blocks)
    return best


def accounted_of(d, rep, r88, b0, ph_off, method, ph):
    ok, sinfo = rep_find_ok(d, rep, b0, ph_off, ph)
    if not ok:
        return None
    return account(d, rep, r88, b0, ph_off, method, ph, sinfo)


def rep_find_ok(d, rep, b0, ph_off, ph):
    try:
        end, info = rep.find_sentinel(d, b0, ph_off, ph["method"])
        return True, {"sentinel": end, **info}
    except rep.Refused:
        return False, None


def account(d, rep, r88, b0, ph_off, method, ph, info):
    _s, _n, total = r88.segment(d, b0, ph_off, method, ph["method"])
    if info.get("resume") is not None:
        _q, _n2, su2 = r88.segment(d, info["resume"], ph_off, method, ph["method"])
        total += su2
    return total


def emit(doc, path):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)


def main():
    if len(sys.argv) < 2 or sys.argv[1] != "--run":
        print("usage: matrix.py --run")
        return 2
    os.makedirs(S, exist_ok=True)
    os.makedirs(RECEIPTS, exist_ok=True)
    assert sha_file(UPX) == PIN, "upx pin mismatch"
    rep = load(R87, "r87x")
    r88 = load(R88, "r88x")
    doc = {"schema": "r90-tamper-matrix-v1", "seat": "ExecMatrix-5",
           "upx": UPX, "upx_sha256": PIN, "rows": [], "out_of_class": [],
           "carriers": {}, "skipped": [], "failed": []}
    jout = SEAT + "/tamper-matrix.json"
    emit(doc, jout)
    try:
        for c in CARRIERS:
            d = tempfile.mkdtemp(prefix="car-", dir=S)
            try:
                run_carrier(c, d, rep, r88, doc, jout)
            finally:
                shutil.rmtree(d, ignore_errors=True)
    finally:
        emit(doc, jout)
    p1_fail = [f for f in doc["failed"]]
    print(f"DONE rows={len(doc['rows'])} ooc={len(doc['out_of_class'])} "
          f"failed={p1_fail}")
    return 1 if p1_fail else 0


def run_carrier(c, d, rep, r88, doc, jout):
    assert sha_file(c["source"]) == c["sha256"], c["id"]
    boxed = os.path.join(d, "orig")
    shutil.copy2(c["source"], boxed)
    packed_p = os.path.join(d, "packed")
    rc, msg = run([UPX, "--best", "-q", "-o", packed_p, boxed])
    assert rc == 0, (c["id"], msg)
    _rc, tok = run([UPX, "-t", "-q", packed_p])
    assert "[OK]" in tok, (c["id"], tok)
    with open(packed_p, "rb") as fh:
        P0 = fh.read()
    b0, ph, ph_off, blocks = layout(P0, rep, r88)
    method = P0[b0 + 8]
    n = len(blocks)
    ok_stored, sinfo = rep_find_ok(P0, rep, b0, ph_off, ph)
    stored_total = (account(P0, rep, r88, b0, ph_off, method, ph, sinfo)
                    if ok_stored else None)
    hdr = {"id": c["id"], "source": c["source"], "orig_sha256": c["sha256"],
           "packed_sha256": sha_bytes(P0), "packed_bytes": len(P0),
           "b0": b0, "ph_off": ph_off, "u_len": ph["u_len"],
           "blocks": n, "stored_total": stored_total,
           "sentinel_ok": ok_stored,
           "sentinel": {k: sinfo[k] for k in sinfo} if ok_stored else None,
           "upx_t_intact": tok.strip().splitlines()[-1] if tok else None,
           "block_list": blocks}
    doc["carriers"][c["id"]] = hdr
    emit(doc, jout)
    print(f"{c['id']}: n={n} u_len={ph['u_len']} stored_total={stored_total} "
          f"ph_off={ph_off}", flush=True)
    # direction availability per interior index
    dirs = {}
    for b in blocks[1:n - 1]:
        i = b["index"]
        dirs[i] = [dl for dl in (-7, 7) if 0 < b["sz_cpr"] + dl <= b["sz_unc"]]
        if not dirs[i]:
            doc["skipped"].append({"carrier": c["id"], "index": i,
                                   "why": "no in-range direction in {-7,+7}"})
    idxs = [b["index"] for b in blocks[1:n - 1]]
    step = max(1, (len(idxs) + N_PER - 1) // N_PER)
    sampled = idxs[::step][:N_PER]
    cand = [(i, dl) for i in sampled for dl in dirs.get(i, [])]
    cand += [(j, -7) for j in idxs if -7 in dirs.get(j, [])]
    seen = set()
    for (i, dl) in cand:
        if (i, dl) in seen:
            continue
        seen.add((i, dl))
        cell(c, d, P0, blocks[i], dl, rep, r88, b0, ph, ph_off, method,
             stored_total, n, doc, jout, out_of_class=False)
    # out-of-class: last block before the stop, both in-range directions
    last = blocks[n - 1]
    for dl in [v for v in (-7, 7) if 0 < last["sz_cpr"] + v <= last["sz_unc"]]:
        ooc_cell(c, d, P0, last, dl, rep, r88, b0, ph, ph_off, method, n, doc, jout)
    return 0


def cell(c, d, P0, blk, dl, rep, r88, b0, ph, ph_off, method, stored_total,
         n, doc, jout, out_of_class=False):
    global cellno
    cellno += 1
    t0 = time.time()
    val = blk["sz_cpr"] + dl
    off = blk["block"]
    buf = bytearray(P0)
    struct.pack_into("<I", buf, off + 4, val)
    T = bytes(buf)
    row = {"cell": cellno, "carrier": c["id"], "index": blk["index"],
           "n_blocks": n, "direction": dl, "block": off,
           "sz_unc": blk["sz_unc"], "u_len": ph["u_len"],
           "stored": blk["sz_cpr"], "value": val, "shape": "interior"}
    box = tempfile.mkdtemp(prefix="inv-", dir=S)
    tf, o90, i90 = (os.path.join(box, x) for x in ("in", "out", "info.json"))
    with open(tf, "wb") as fh:
        fh.write(T)
    rc_t, msg_t = run([UPX, "-t", "-q", tf])
    row["upx_t"] = {"rc": rc_t,
                    "msg": [ln.strip() for ln in msg_t.splitlines() if ln.strip()]}
    r89_rc, r89_out = run([sys.executable, "-I", "-B", R89, "--in", tf,
                           "--out", o90])
    r89_b = open(o90, "rb").read() if r89_rc == 0 and os.path.isfile(o90) else None
    row["r89"] = {"rc": r89_rc,
                  "changed": (None if r89_b is None else r89_b != T),
                  "msg": r89_out.strip()}
    if r89_b is not None and os.path.isfile(o90):
        os.unlink(o90)
    t1 = time.time()
    r90_rc, r90_out = run([sys.executable, "-I", "-B", R90, "--in", tf,
                           "--out", o90, "--info", i90])
    dt = time.time() - t1
    row["r90"] = {"rc": r90_rc, "seconds": round(dt, 2), "stdout": r90_out.strip()}
    rec = None
    if r90_rc == 0 and os.path.isfile(o90):
        B = open(o90, "rb").read()
        if os.path.isfile(i90):
            rec = json.load(open(i90))
        rp = o90 + ".rp"
        os.rename(o90, rp)
        rc_t2, msg_t2 = run([UPX, "-t", "-q", rp])
        up = rp + ".unpacked"
        rc_d, msg_d = run([UPX, "-d", "-q", "-o", up, rp])
        pin_ok = os.path.isfile(up) and sha_file(up) == c["sha256"]
        if os.path.isfile(up):
            os.unlink(up)
        ok2, si2 = rep_find_ok(B, rep, b0, ph_off, ph)
        rep_total = (account(B, rep, r88, b0, ph_off, method, ph, si2)
                     if ok2 else None)
        derived = struct.unpack_from("<I", B, off + 4)[0]
        arms = {"repair_rc0": True, "bytes_equal": B == P0, "upx_t_rc0": rc_t2 == 0,
                "unpack_pin": pin_ok}
        row["recovery"] = {**arms,
                           "upx_t_msg": [ln.strip() for ln in msg_t2.splitlines() if ln.strip()],
                           "upx_d_rc": rc_d,
                           "accounted_after": rep_total,
                           "derived": derived,
                           "record": rec}
        row["recovered"] = all(arms.values())
        if not row["recovered"] and c["id"] in P1_IDS:
            doc["failed"].append(f"{c['id']}:{blk['index']}:{dl}")
    else:
        row["recovered"] = False
        row["refusal"] = r90_out.strip()
        if c["id"] in P1_IDS and out_of_class is False:
            doc["failed"].append(f"{c['id']}:{blk['index']}:{dl}:refused")
    os.unlink(tf)
    shutil.rmtree(box, ignore_errors=True)
    doc["rows"].append(row)
    with open(os.path.join(RECEIPTS, f"cell-{cellno:03d}-{c['id']}-i{blk['index']}{dl:+d}.json"),
              "w", encoding="utf-8") as fh:
        json.dump(row, fh, indent=1, sort_keys=True)
    emit(doc, jout)
    print(f"cell {cellno}: {c['id']} i={blk['index']} d={dl:+d} "
          f"r90_rc={row['r90']['rc']} recovered={row.get('recovered')} "
          f"({time.time()-t0:.1f}s)", flush=True)


def ooc_cell(c, d, P0, blk, dl, rep, r88, b0, ph, ph_off, method, n, doc, jout):
    global cellno
    cellno += 1
    val = blk["sz_cpr"] + dl
    buf = bytearray(P0)
    struct.pack_into("<I", buf, blk["block"] + 4, val)
    T = bytes(buf)
    box = tempfile.mkdtemp(prefix="ooc-", dir=S)
    tf, o90 = os.path.join(box, "in"), os.path.join(box, "out")
    with open(tf, "wb") as fh:
        fh.write(T)
    rc_t, msg_t = run([UPX, "-t", "-q", tf])
    r90_rc, r90_out = run([sys.executable, "-I", "-B", R90, "--in", tf,
                           "--out", o90])
    unchanged = (open(o90, "rb").read() == T
                 if r90_rc == 0 and os.path.isfile(o90) else None)
    row = {"cell": cellno, "carrier": c["id"], "shape": "last-before-stop",
           "index": blk["index"], "n_blocks": n, "direction": dl,
           "block": blk["block"], "stored": blk["sz_cpr"], "value": val,
           "u_len": ph["u_len"],
           "upx_t": {"rc": rc_t, "msg": [ln.strip() for ln in msg_t.splitlines() if ln.strip()]},
           "r90_rc": r90_rc, "r90_stdout": r90_out.strip(),
           "unchanged": unchanged}
    doc["out_of_class"].append(row)
    with open(os.path.join(RECEIPTS, f"ooc-{cellno:03d}-{c['id']}-last{dl:+d}.json"),
              "w", encoding="utf-8") as fh:
        json.dump(row, fh, indent=1, sort_keys=True)
    emit(doc, jout)
    print(f"ooc {cellno}: {c['id']} last d={dl:+d} rc={r90_rc} "
          f"unchanged={unchanged}", flush=True)
    shutil.rmtree(box, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
