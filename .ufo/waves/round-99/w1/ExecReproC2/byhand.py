#!/usr/bin/env python3
# Independent hand probe (ExecReproC2): own PE parser, own cut offsets, upx as oracle.
import hashlib, json, os, struct, subprocess, sys

S = os.environ["S"]
CLONE = os.environ["CLONE"]
WAVE = os.environ["WAVE"]
UPX = "/usr/bin/upx"
REPAIR = os.path.join(CLONE, "tools/round-99/upx-pe-repair.py")
DL = "/home/vgpnk/.local/share/kaidoku-pwnenv/lib/python3.11/site-packages/pip/_vendor/distlib"
OGL = "/usr/lib/python3.14/site-packages/OpenGL/DLLS"
CARRIERS = [
    ("t32", DL + "/t32.exe", "6b4195e640a85ac32eb6f9628822a622057df1e459df7c17a12f97aeabc9415b"),
    ("w64", DL + "/w64.exe", "7a319ffaba23a017d7b1e18ba726ba6c54c53d6446db55f92af53c279894f8ad"),
    ("freeglut32dll", OGL + "/freeglut32.vc14.dll", "c9c00a4ea9b9fecdcae81f6facaf27e349714d56fe7640ce9c37ed38841a0b87"),
]
WORK = os.path.join(S, "byhand")
os.makedirs(WORK, exist_ok=True)
os.makedirs(os.path.join(WORK, "tmp"), exist_ok=True)
ENV = dict(os.environ, TMPDIR=os.path.join(WORK, "tmp"))


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def sections(b):
    pe = struct.unpack_from("<I", b, 0x3C)[0]
    assert b[pe:pe + 4] == b"PE\0\0"
    n = struct.unpack_from("<H", b, pe + 6)[0]
    opt = struct.unpack_from("<H", b, pe + 20)[0]
    falign = struct.unpack_from("<I", b, pe + 24 + 36)[0]
    st = pe + 24 + opt
    secs = []
    for k in range(n):
        o = st + 40 * k
        name = bytes(b[o:o + 8]).rstrip(b"\0").decode("latin1")
        vsize, vaddr, rsize, rptr = struct.unpack_from("<IIII", b, o + 8)
        secs.append({"name": name, "rsize": rsize, "rptr": rptr, "vsize": vsize})
    return falign, secs


def run(argv):
    p = subprocess.run(argv, capture_output=True, text=True, env=ENV)
    return p.returncode, (p.stdout + p.stderr).strip()


def main():
    receipt = {"upx": run([UPX, "--version"])[1].splitlines()[0], "repair": REPAIR,
               "repair_sha256": sha(REPAIR), "carriers": [], "pass": True}
    for name, src, pin in CARRIERS:
        if sha(src) != pin:
            raise SystemExit("pin mismatch " + name)
        orig = os.path.join(WORK, name + ".orig")
        packed = os.path.join(WORK, name + ".upx")
        with open(src, "rb") as fh, open(orig, "wb") as fo:
            fo.write(fh.read())
        rc, msg = run([UPX, "--best", "-q", "-f", "-o", packed, orig])
        assert rc == 0, msg
        pb = open(packed, "rb").read()
        falign, secs = sections(pb)
        last = secs[-1]
        aligned_end = (last["rptr"] + last["rsize"] + falign - 1) // falign * falign
        u1 = secs[1]
        # my own offsets, inside the sections (battery uses end-1 and UPX1 rptr+rsize//2)
        cuts = {
            "UPX1-start+3": u1["rptr"] + 3,
            "UPX1-3/4": u1["rptr"] + (u1["rsize"] * 3) // 4,
            "last-section-mid": last["rptr"] + last["rsize"] // 2,
        }
        carrier = {"carrier": name, "size": len(pb), "falign": falign,
                   "sections": [(s["name"], s["rptr"], s["rsize"]) for s in secs],
                   "aligned_end_last": aligned_end, "cells": []}
        # uncut pack: upx -t and tool must agree on success
        rc_t, _ = run([UPX, "-t", "-q", packed])
        inp = os.path.join(WORK, name + ".uncut.in")
        out = os.path.join(WORK, name + ".uncut.out")
        with open(inp, "wb") as fh:
            fh.write(pb)
        if os.path.exists(out):
            os.unlink(out)
        rc_r, msg_r = run([sys.executable, "-I", "-B", REPAIR, "--in", inp, "--out", out, "--json"])
        same = open(out, "rb").read() == pb if rc_r == 0 and os.path.exists(out) else None
        carrier["cells"].append({"case": "uncut", "upx_t_rc": rc_t, "tool_rc": rc_r,
                                 "tool_msg": msg_r[-160:], "out_equals_input": same})
        ok = rc_t == 0 and rc_r == 0 and same is True
        carrier["cells"][-1]["agree"] = ok
        receipt["pass"] &= ok
        cut_specs = list(cuts.items()) + [("aligned-end(boundary)", aligned_end),
                                          ("aligned-end-1(boundary)", aligned_end - 1)]
        for cname, at in cut_specs:
            cin = os.path.join(WORK, "%s.%s.in" % (name, cname.replace("/", "_")))
            cout = os.path.join(WORK, "%s.%s.out" % (name, cname.replace("/", "_")))
            with open(cin, "wb") as fh:
                fh.write(pb[:at])
            if os.path.exists(cout):
                os.unlink(cout)
            trc, tmsg = run([UPX, "-t", "-q", cin])
            rrc, rmsg = run([sys.executable, "-I", "-B", REPAIR, "--in", cin, "--out", cout, "--json"])
            out_exists = os.path.exists(cout)
            trunc_refused = rrc == 2 and "truncated" in rmsg and not out_exists
            upx_fails = trc != 0
            if cname.startswith("aligned-end") and cname.endswith("(boundary)") and cname.startswith("aligned-end-1") is False and at == aligned_end:
                agree = (trc == 0) and rrc == 0 and out_exists and open(cout, "rb").read() == pb[:at]
            else:
                agree = (upx_fails == trunc_refused)
            cell = {"case": cname, "cut": at, "file_len_before_cut": len(pb),
                    "upx_t_rc": trc, "upx_t_msg": tmsg[-120:], "tool_rc": rrc,
                    "tool_msg": rmsg[-160:], "tool_out_written": out_exists,
                    "truncated_refusal": trunc_refused, "agree": agree}
            if cname == "aligned-end(boundary)" and rrc == 0:
                cell["out_equals_cut"] = open(cout, "rb").read() == pb[:at]
            carrier["cells"].append(cell)
            receipt["pass"] &= agree
        receipt["carriers"].append(carrier)
    with open(os.path.join(WAVE, "byhand.json"), "w") as fh:
        json.dump(receipt, fh, indent=1, sort_keys=True)
        fh.write("\n")
    for c in receipt["carriers"]:
        print(c["carrier"], "size", c["size"], "falign", c["falign"], "sections", c["sections"], "aligned_end", c["aligned_end_last"])
        for cell in c["cells"]:
            print("  %-26s cut=%-8s upx_t_rc=%s tool_rc=%s trunc_refusal=%s out=%s agree=%s" % (
                cell["case"], cell.get("cut", "-"), cell["upx_t_rc"], cell["tool_rc"],
                cell.get("truncated_refusal", "-"), cell.get("tool_out_written", "-"), cell["agree"]))
            print("     upx_t: %s" % cell.get("upx_t_msg", "(uncut: no upx -t message captured)").replace("\n", " | ")[:160])
            print("     tool : %s" % cell["tool_msg"].replace("\n", " | ")[:160])
    print("ALL AGREE" if receipt["pass"] else "DISAGREEMENT PRESENT")
    return 0 if receipt["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
