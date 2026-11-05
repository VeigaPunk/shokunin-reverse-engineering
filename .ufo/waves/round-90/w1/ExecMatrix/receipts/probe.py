#!/usr/bin/env python3
"""probe.py - follow-up probes for the red/misbehaving matrix cells.

A) jq and libz, LAST block, direction -7: full recovery arms of the round-90
   output vs the intact packed bytes (bytes_equal, upx -t rc/msg, upx -d sha),
   since ooc_cell only measured changed-vs-tampered.
B) dinit, interior block 1, both directions: which bytes the round-89 repair
   changed (offsets, window check) and whether its output passes upx -t.
C) verbatim upx -t message on one tampered interior cell (jq i=1 -7).
"""
from __future__ import annotations
import hashlib, importlib.util, json, os, shutil, struct, subprocess, sys, tempfile

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r90/ExecMatrix"
UPX = "/usr/bin/upx"
R87 = ROOT + "/tools/round-87/upx-magic-repair.py"
R88 = ROOT + "/tools/round-88/upx-chain-repair.py"
R89 = ROOT + "/tools/round-89/upx-field-value-repair.py"
R90 = ROOT + "/tools/round-90/upx-break-repair.py"
CAR = {"jq": "/usr/bin/jq", "libz": "/usr/lib/libz.so.1.3.2",
       "dinit": "/usr/bin/docker-init"}
P1 = {"jq", "xxd", "dinit"}
ENV = {"HOME": os.path.expanduser("~"), "LANG": "C", "PATH": os.environ["PATH"]}
OUT = open("/fast/scratch/hyaku/kaidoku-r90/ExecMatrix/probe.txt", "w")


def w(*a):
    print(*a, file=OUT, flush=True)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(argv):
    p = subprocess.run(argv, env=ENV, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
    return p.returncode, p.stdout.decode("utf-8", errors="replace")


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    with open(p, "rb") as fh:
        return sha_bytes(fh.read())


rep, r88 = load(R87, "r87p"), load(R88, "r88p")


def layout(P0, ph_off, ph):
    best = None
    for m in r88.l_info_candidates(P0, ph_off, ph):
        b0 = m + 20
        if b0 + 12 > ph_off or struct.unpack_from("<I", P0, b0)[0] == 0:
            continue
        method = P0[b0 + 8]
        q, blocks = b0, []
        while q + 12 <= ph_off:
            su, sc = struct.unpack_from("<II", P0, q)
            if (su == 0 or sc == 0 or sc > su or q + 12 + sc > ph_off
                    or P0[q + 8] not in (method, ph["method"])):
                break
            blocks.append({"index": len(blocks), "block": q, "sz_unc": su,
                           "sz_cpr": sc})
            q += 12 + sc
        if best is None or len(blocks) > len(best[2]):
            best = (b0, method, blocks)
    return best


def box_run(tool, data):
    box = tempfile.mkdtemp(prefix="probe-", dir=S)
    i90, o90 = os.path.join(box, "in"), os.path.join(box, "out")
    with open(i90, "wb") as fh:
        fh.write(data)
    rc, out = run([sys.executable, "-I", "-B", tool, "--in", i90, "--out", o90,
                   "--info", o90 + ".json"])
    blob = open(o90, "rb").read() if rc == 0 and os.path.isfile(o90) else None
    rec = json.load(open(o90 + ".json")) if os.path.isfile(o90 + ".json") else None
    shutil.rmtree(box, ignore_errors=True)
    return rc, out, blob, rec


def arms(tool, T, P0, orig, blk, want_verbatim=False):
    rc, out, B, rec = box_run(tool, T)
    row = {"r90_rc": rc, "stdout": out.strip()}
    if B is not None:
        diffs = [i for i, (x, y) in enumerate(zip(P0, B)) if x != y]
        row["bytes_equal"] = B == P0
        row["diff_offsets_vs_intact"] = diffs[:8]
        tf = os.path.join(tempfile.mkdtemp(prefix="pr2-", dir=S), "o")
        with open(tf, "wb") as fh:
            fh.write(B)
        rc_t, msg_t = run([UPX, "-t", "-q", tf])
        row["test"] = {"rc": rc_t, "msg": [l.strip() for l in msg_t.splitlines() if l.strip()][-3:]}
        up = tf + ".unpacked"
        rc_d, msg_d = run([UPX, "-d", "-q", "-o", up, tf])
        row["unpack"] = {"rc": rc_d,
                         "pin": os.path.isfile(up) and sha_file(up) == orig}
        # the tampered-input upx -t verdict, verbatim
        tf2 = tf + ".t"
        with open(tf2, "wb") as fh:
            fh.write(T)
        rc_t0, msg_t0 = run([UPX, "-t", "-q", tf2])
        row["tampered_test"] = {"rc": rc_t0,
                                "msg": [l.strip() for l in msg_t0.splitlines() if l.strip()][-3:]}
        row["record_class"] = (rec or {}).get("class")
        row["record"] = {k: (rec or {}).get(k) for k in
                         ("break_index", "stored_sz_cpr", "derived_sz_cpr",
                          "uncompressed_accounted", "stored_accounted")}
    w(" ", json.dumps(row, sort_keys=True))
    return rc, out, B, rec


def main():
    w("== A. last-block -7 full arms ==")
    for cid in ("jq", "libz"):
        d = tempfile.mkdtemp(prefix="pc-", dir=S)
        orig = os.path.join(d, "orig")
        shutil.copy2(CAR[cid], orig)
        packed = os.path.join(d, "packed")
        run([UPX, "--best", "-q", "-o", packed, orig])
        P0 = open(packed, "rb").read()
        ph_off, ph = rep.find_packheader(P0)
        _b0, _method, blocks = layout(P0, ph_off, ph)
        blk = blocks[-1]
        for dl in (-7,):
            val = blk["sz_cpr"] + dl
            T = bytearray(P0)
            struct.pack_into("<I", T, blk["block"] + 4, val)
            T = bytes(T)
            w(f"{cid} last d={dl:+d} stored={blk['sz_cpr']} val={val}")
            arms(R90, T, P0, sha_file(orig), blk)
        shutil.rmtree(d, ignore_errors=True)
    w("== B. dinit i=1 r89 diff ==")
    d = tempfile.mkdtemp(prefix="pc-", dir=S)
    orig = os.path.join(d, "orig")
    shutil.copy2(CAR["dinit"], orig)
    packed = os.path.join(d, "packed")
    run([UPX, "--best", "-q", "-o", packed, orig])
    P0 = open(packed, "rb").read()
    ph_off, ph = rep.find_packheader(P0)
    _b0, _method, blocks = layout(P0, ph_off, ph)
    blk = blocks[1]
    for dl in (-7, 7):
        val = blk["sz_cpr"] + dl
        T = bytearray(P0)
        struct.pack_into("<I", T, blk["block"] + 4, val)
        T = bytes(T)
        rc, out, B, rec = box_run(R89, T)
        lo, hi = blk["block"] + 4, blk["block"] + 8
        diffs = []
        if B is not None:
            diffs = [i for i, (x, y) in enumerate(zip(T, B)) if x != y]
        w(f"dinit i=1 d={dl:+d} r89_rc={rc} changed={B is not None and B != T}")
        w("  diff_offsets_vs_tampered:", diffs[:12],
          f"(window {lo}-{hi})" if diffs else "")
        w("  stdout:", out.strip()[:160])
        if B is not None:
            tf = os.path.join(tempfile.mkdtemp(prefix="pr3-", dir=S), "o")
            with open(tf, "wb") as fh:
                fh.write(B)
            rc_t, msg_t = run([UPX, "-t", "-q", tf])
            w("  r89_output_upx_t_rc:", rc_t, [l.strip() for l in msg_t.splitlines() if l.strip()][-2:])
    shutil.rmtree(d, ignore_errors=True)
    w("== C. verbatim upx -t on tampered interior cell (jq i=1 -7) ==")
    d = tempfile.mkdtemp(prefix="pc-", dir=S)
    orig = os.path.join(d, "orig")
    shutil.copy2(CAR["jq"], orig)
    packed = os.path.join(d, "packed")
    run([UPX, "--best", "-q", "-o", packed, orig])
    P0 = open(packed, "rb").read()
    ph_off, ph = rep.find_packheader(P0)
    _b0, _method, blocks = layout(P0, ph_off, ph)
    blk = blocks[1]
    val = blk["sz_cpr"] - 7
    T = bytearray(P0)
    struct.pack_into("<I", T, blk["block"] + 4, val)
    tf = os.path.join(d, "t.bin")
    with open(tf, "wb") as fh:
        fh.write(bytes(T))
    rc_t, msg_t = run([UPX, "-t", "-q", tf])
    w("jq i=1 d=-7 upx -t rc:", rc_t)
    for ln in msg_t.splitlines():
        w("   |", ln.rstrip())
    shutil.rmtree(d, ignore_errors=True)
    OUT.close()


if __name__ == "__main__":
    main()
