#!/usr/bin/env python3
"""CriticC2 held-out differential driver (scratch). Compares candidates on inputs outside the pinned set.

Usage: heldout.py --scratch <dir> --out <json> --cand name=path [--cand ...]
Inputs: host PE files (not pinned), packed with /usr/bin/upx --best; own cut points; a constructed
input whose last section raw end is not FileAlignment-aligned (cut inside the alignment gap).
"""
import argparse
import hashlib
import json
import os
import random
import shutil
import struct
import subprocess
import sys

UPX = "/usr/bin/upx"
PINNED = {
    "6b4195e640a85ac32eb6f9628822a622057df1e459df7c17a12f97aeabc9415b",
    "81a618f21cb87db9076134e70388b6e9cb7c2106739011b6a51772d22cae06b7",
    "47872cc77f8e18cf642f868f23340a468e537e64521d9a3a416c8b84384d064b",
    "7a319ffaba23a017d7b1e18ba726ba6c54c53d6446db55f92af53c279894f8ad",
    "7a98a934de5f578c3a547af873221b221d037bafa87ceee71dd4f089dd228202",
    "d1a71f9ac1728082c1b276392725c3e010b98714888579b99152e401abedbf11",
    "c9c00a4ea9b9fecdcae81f6facaf27e349714d56fe7640ce9c37ed38841a0b87",
    "b427510af633a6298481e738942f3268daedf44d6c01af74620579034bede9ce",
    "e855478acf0d36f846befb48bfd239b7ef46e568e2408091591adec274ed0879",
    "c769642c8a489e8fc078b8387fb9865ac5c5482ce22301a40d00145fa1304b27",
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run(argv, timeout=900):
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return -9, "timeout"


def layout(b):
    pe = struct.unpack_from("<I", b, 0x3C)[0]
    if b[pe:pe + 4] != b"PE\0\0":
        raise ValueError("not PE")
    n = struct.unpack_from("<H", b, pe + 6)[0]
    opt = struct.unpack_from("<H", b, pe + 20)[0]
    falign = struct.unpack_from("<I", b, pe + 24 + 36)[0]
    st = pe + 24 + opt
    secs = []
    for k in range(n):
        o = st + 40 * k
        name = bytes(b[o:o + 8]).rstrip(b"\0")
        vsize, vaddr, rsize, rptr = struct.unpack_from("<IIII", b, o + 8)
        secs.append({"off": o, "name": name, "rsize": rsize, "rptr": rptr})
    return falign, secs


def align_up(v, a):
    return (v + a - 1) // a * a


def pick_hosts(scr, want=3):
    out = []
    cands = [l.strip() for l in open(os.path.join(scr, "..", "pe-candidates.txt")) if l.strip()]
    for path in cands:
        if len(out) >= want:
            break
        try:
            data = open(path, "rb").read()
        except OSError:
            continue
        if data[:2] != b"MZ" or len(data) > 3_000_000 or len(data) < 20000 or sha(data) in PINNED:
            continue
        try:
            falign, secs = layout(data)
        except (ValueError, struct.error):
            continue
        if len(secs) < 3 or falign == 0:
            continue
        names = tuple(s["name"].decode("latin1") for s in secs)
        if any(names == o[2] for o in out):
            continue
        tag = "h%d" % len(out)
        orig = os.path.join(scr, tag + ".orig")
        shutil.copyfile(path, orig)
        packed = os.path.join(scr, tag + ".upx")
        rc, msg = run([UPX, "--best", "-q", "-f", "-o", packed, orig])
        if rc != 0:
            continue
        out.append((tag, path, packed, names))
    return out


def tamper(b, kind):
    b = bytearray(b)
    if kind in ("magic", "both"):
        i = b.find(b"UPX!")
        b[i:i + 4] = b"\0\0\0\0"
    if kind in ("names", "both"):
        _, secs = layout(bytes(b))
        for k, nm in enumerate((b".text", b".data", b".rdata")):
            if k < len(secs):
                o = secs[k]["off"]
                if bytes(b[o:o + 3]) == b"UPX":
                    b[o:o + 8] = nm.ljust(8, b"\0")
    return bytes(b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--cand", action="append", required=True)
    a = ap.parse_args()
    scr = os.path.abspath(a.scratch)
    os.makedirs(scr, exist_ok=True)
    cands = []
    for spec in a.cand:
        name, path = spec.split("=", 1)
        cands.append((name, path))
    hosts = pick_hosts(scr)
    rows = []
    for tag, path, packed, names in hosts:
        P = open(packed, "rb").read()
        falign, secs = layout(P)
        last = secs[-1]
        raw_end = last["rptr"] + last["rsize"]
        aend = align_up(raw_end, falign)
        r1 = secs[1]
        ref_path = os.path.join(scr, tag + ".ref.unp")
        rc, _ = run([UPX, "-d", "-q", "-o", ref_path, packed])
        ref = sha(open(ref_path, "rb").read()) if rc == 0 else None
        if ref is None:
            continue
        ovrng = random.Random(int(tag[1:]) * 7919 + 17)
        ov = bytes(ovrng.getrandbits(8) for _ in range(ovrng.randint(1, 4096)))
        ov_ref_path = os.path.join(scr, tag + ".ovref.unp")
        open(os.path.join(scr, tag + ".ovin"), "wb").write(P + ov)
        rc, _ = run([UPX, "-d", "-q", "-o", ov_ref_path, os.path.join(scr, tag + ".ovin")])
        ov_ref = sha(open(ov_ref_path, "rb").read()) if rc == 0 else None
        inputs = []  # (case, class, data, ref)
        inputs.append(("intact", "valid", P, ref))
        for kd in ("magic", "names", "both"):
            inputs.append(("tamper-" + kd, "valid", tamper(P, kd), ref))
        inputs.append(("overlay-intact", "valid", P + ov, ov_ref))
        inputs.append(("overlay-both", "valid", tamper(P, "both") + ov, ov_ref))
        cut_at = {
            "aend-1": aend - 1, "aend-2": aend - 2, "aend-512": aend - 512,
            "raw-end+1": raw_end + 1, "raw-end-1": raw_end - 1,
            "upx1-start+1": r1["rptr"] + 1, "upx1-mid": r1["rptr"] + r1["rsize"] // 2,
            "upx1-end-1": r1["rptr"] + r1["rsize"] - 1,
            "rand-a": ovrng.randint(1, len(P) - 2), "rand-b": ovrng.randint(1, len(P) - 2),
        }
        for base_kind, base in (("intact", P), ("both", tamper(P, "both"))):
            for ck, at in sorted(cut_at.items()):
                if 0 < at < len(base):
                    inputs.append(("cut-%s-%s" % (base_kind, ck), "cut", base[:at], None))
        mid_c = r1["rptr"] + r1["rsize"] // 2
        Cb = bytearray(P)
        Cb[mid_c] ^= 0xFF
        inputs.append(("corrupt-upx1-mid", "corrupt", bytes(Cb), None))
        # constructed: last raw size reduced by 80 so the raw end is unaligned, cut inside the gap
        d = 80
        if last["rsize"] > d and raw_end % falign == 0:
            Q = bytearray(P)
            struct.pack_into("<I", Q, last["off"] + 16, last["rsize"] - d)
            Q = bytes(Q)
            gap_cut = aend - 40
            inputs.append(("gap-cut-intact", "cut", Q[:gap_cut], None))
            inputs.append(("gap-cut-both", "cut", tamper(Q, "both")[:gap_cut], None))
        for case, cls, data, expect in inputs:
            ip = os.path.join(scr, "%s.%s.in" % (tag, case))
            open(ip, "wb").write(data)
            trc, _ = run([UPX, "-t", "-q", ip])
            row = {"host": tag, "src": path, "case": case, "class": cls, "len": len(data),
                   "packer_t_input_rc": trc, "ref_expected_sha": expect, "cand": {}}
            for cname, cpath in cands:
                op = os.path.join(scr, "%s.%s.%s.out" % (tag, case, cname))
                if os.path.exists(op):
                    os.unlink(op)
                crc, cmsg = run([sys.executable, "-I", "-B", cpath, "--in", ip, "--out", op])
                ok_out = None
                t_out = None
                if crc == 0 and os.path.exists(op):
                    t_out, _ = run([UPX, "-t", "-q", op])
                    up = os.path.join(scr, "%s.%s.%s.unp" % (tag, case, cname))
                    urc, _ = run([UPX, "-d", "-q", "-o", up, op])
                    got = sha(open(up, "rb").read()) if urc == 0 and os.path.exists(up) else None
                    want = expect if expect is not None else ref
                    ok_out = (t_out == 0 and got is not None and got == want)
                if cls == "corrupt":
                    verdict = "refused" if crc == 2 else ("INVALID_OUTPUT" if crc == 0 and not ok_out else ("accepted-valid" if crc == 0 else "rc%d" % crc))
                    bad = crc == 0 and not ok_out
                elif cls == "cut":
                    verdict = "refused" if crc == 2 else ("FALSE_ACCEPT" if crc == 0 else "rc%d" % crc)
                    bad = crc == 0
                else:
                    verdict = "accepted-valid" if (crc == 0 and ok_out) else (
                        "FALSE_REFUSE" if crc == 2 else ("INVALID_OUTPUT" if crc == 0 else "rc%d" % crc))
                    bad = not (crc == 0 and ok_out)
                row["cand"][cname] = {"rc": crc, "out_upx_t": t_out, "out_ok": ok_out,
                                      "verdict": verdict, "bad": bad, "msg": cmsg[-160:]}
            rows.append(row)
    summary = {}
    for cname, _ in cands:
        summary[cname] = {
            "cases": len(rows),
            "bad": sum(1 for r in rows if r["cand"][cname]["bad"]),
            "false_accept_cut": sum(1 for r in rows if r["class"] == "cut" and r["cand"][cname]["rc"] == 0),
            "invalid_or_refuse_valid": sum(1 for r in rows if r["class"] == "valid" and r["cand"][cname]["bad"]),
        }
    diffs = {}
    base = cands[0][0]
    for cname, _ in cands[1:]:
        diffs[cname] = [{"host": r["host"], "case": r["case"], "base": r["cand"][base]["verdict"],
                         "cand": r["cand"][cname]["verdict"]}
                        for r in rows if r["cand"][cname]["verdict"] != r["cand"][base]["verdict"]]
    json.dump({"hosts": [{"tag": h[0], "src": h[1], "names": h[3]} for h in hosts],
               "summary": summary, "diffs_vs_" + base: diffs, "rows": rows},
              open(a.out, "w"), indent=1, sort_keys=True)
    print(json.dumps({"summary": summary, "diff_counts": {k: len(v) for k, v in diffs.items()}}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
